# El bloque de la caja: qué velas de M1 elige el trader

Rama `trabajo/bloque-de-la-caja`, 2026-09-28, tarea autónoma sobre `main` en
`stable/F20-orden-stop-o-limite`. **Descriptivo**: no cambia el motor, ni el productor, ni RN-011,
ni ningún parámetro, regla, ambigüedad, evidencia o registro de feedback. Nada se resuelve.

**Pregunta.** En v7 y v8 el trader traza en M1 una caja de niveles 0 · 0,25 · 0,5 · 0,8 · 1. ¿Qué
vela o velas de M1 elige como bloque para trazarla? `ORDEN-STOP-O-LIMITE.md` midió que ninguna de
sus 77 entradas de construcción es una límite de antemano esperando el retroceso, y
`VERIFICACION-A21.md` que su entrada casi nunca cae en la zona del motor ni en su nivel de breaker:
el bloque que elige el productor no es el suyo, y esta rama mide cuál es.

**Lo que la medición corrige del brief, antes de empezar.** `bloque_de_origen` no está en
`engine/zonas.py` sino en `src/botsito/domain/estructura_m1.py`; `engine/zonas.py` solo lo usa a
través de `detectar_esquema`.

## 1. El criterio, escrito ANTES de medir (2026-09-28)

Este apartado se escribe y se commitea antes de abrir ningún fotograma para leer cajas y antes de
cruzar ninguna vela. **No se cambia después**: si hay que corregirlo, se añade una nota y se
presentan las dos versiones.

### 1.1 Qué operaciones entran

- **Material**: solo los días de agosto de 2026 que enseñan v7 (3, 4, 5, 6, 7, 10 y 11) y el tramo
  CON audio de v8 (12, 13, 14, 17, 18 y 19). Todos son de desarrollo; se comprueba con
  `casos_reservados(repo)` y `casos_ocultos(repo)` antes de leer nada.
- **Candidatas**: las operaciones de las tablas de `SESION-02-VIDEO.md` §3.2 (n.º 1 a 25) y
  `SESION-02-VIDEO-V8.md` §3.2 (n.º 1 a 18), **sin las DUDOSAS**: v7 n.º 23 (recuadro de
  corrección del 2026-09-27) y v8 n.º 4, 7 y 10 (decisión (a) de su §11). Quedan 24 de v7 y 15 de
  v8: 39 candidatas.
- **Entran** las que tienen **los dos niveles, 0 y 1, legibles** en un fotograma localizado (§1.2).
  Las que no, quedan fuera y se dice por qué, una a una.

### 1.2 Cómo se leen el 0 y el 1 de cada caja en pantalla

- **Fotogramas**: SOLO los que ya citan los dos informes para esa operación y su vecindario
  inmediato (±10 s), por instante localizado (ADR-0038). El tramo sin audio de v8 (desde 0:40:00) no
  se abre.
- **La caja**: la herramienta de niveles que el trader dibuja en M1, con sus etiquetas «0», «0.25»,
  «0.5», «0.8» y «1» a los lados. Se toma la caja que está dibujada cuando se coloca la orden de esa
  operación (la más cercana a la etiqueta de la orden, en el mismo tramo de tiempo). Si hay varias
  y no se sabe cuál es, la operación queda fuera.
- **Precio de cada nivel**, por orden de preferencia: (1) si una etiqueta de precio del eje o de la
  plataforma (orden, stop, objetivo, línea) coincide con la línea del nivel, ese precio exacto; (2)
  si no, se interpola la altura de la línea entre las dos marcas del eje de precios más cercanas.
  **Legibilidad declarada: ±1 punto** en (1), y en (2) lo que dé la escala del eje en ese
  fotograma, que se anota (a M1 suele ser de ±1 a ±2 puntos). Si un nivel no se puede leer así,
  la operación queda fuera.
- **Se anota además**, sin que decida la entrada, a qué nivel de la caja está la orden y a cuál el
  stop. El brief dice orden en el 0 y stop en el 0,8; se comprueba, y si no es así se dice.
- **Hora de colocación**: la del reloj del gráfico (UTC+2 fijo, CLAUDE.md) en el primer fotograma
  que enseña la etiqueta de la orden; se pasa a UTC restando dos horas. Si la orden se movió, la de
  su última posición antes del llenado.
- **Dirección**: la de la orden (venta o compra).

### 1.3 Cómo se busca en M1

- **Velas**: las M1 de Dukascopy del repositorio (`eurusd-m1-2026-08-0d42230e`, precio BID, reloj
  `ts_utc` en UTC). **Husos fijados antes de comparar**: pantalla en UTC+2 fijo; velas en UTC. La
  hora de colocación se pasa a UTC antes de buscar.
- **Proveedores**: FX Replay dibuja OANDA y el repositorio tiene Dukascopy. Difieren 1–2 puntos
  (A-16), y eso se dice en cada comparación.
- **Ventana**: las M1 **cerradas antes** de la hora de colocación T, en [T − 90 min, T).
- **Una vela «da» un nivel** si alguno de sus extremos (máxima o mínima) está a ≤ τ puntos del nivel.
  τ = 2 puntos (el margen de A-16, `criterio_huso.yaml`); **sensibilidad con τ = 1 y τ = 3**. Se
  anota si lo que coincide es una mecha o un cuerpo (apertura o cierre a ≤ τ).
- Si ninguna vela de la ventana da un nivel dentro de τ, ese nivel queda **«sin explicación»**.

### 1.4 Las reglas candidatas

Todas se escriben para una VENTA; una COMPRA es la simétrica (se cambian máximas por mínimas y los
colores). En una venta, la vela **contraria** es la alcista (cierre > apertura); **del color de la
entrada**, la bajista; **sin cuerpo**, cierre = apertura. El 0 de una caja de venta es su mínimo (el
borde más cercano al precio después de la ruptura, mecha incluida) y el 1 su máximo. Todas miran solo
velas cerradas antes de T.

- **R1 · la última vela contraria antes del impulso** (`bloque_de_origen` de
  `domain/estructura_m1.py`, anclado en T): desde la última M1 cerrada antes de T hacia atrás, se
  saltan las del color de la entrada y las sin cuerpo; la primera contraria es el bloque. 0 = su
  mínima; 1 = su máxima.
- **R2 · el par cubierto por la mecha** (v7 0:24:27, «que la vela siguiente cubra, con mecha por
  debajo, a la vela anterior, no importa si es del mismo color»): la vela de R1 (k) y la siguiente
  (k+1), si k+1 existe antes de T y su mínima pasa por debajo de la mínima de k. 0 = mínima de k+1;
  1 = la máxima de las dos. Si k+1 no cubre a k, R2 no da caja.
- **R3 · la envolvente de una sola vela** (v7 0:47–0:50, «una vela roja… con una mecha por arriba y
  una mecha por debajo… cubriendo tanto por arriba y por debajo, y bajista… aquí por debajo
  tendríamos nosotros la order limit»): la última M1 bajista antes de T cuya máxima es ≥ la máxima
  de la anterior y cuya mínima es ≤ la mínima de la anterior. 0 = su mínima; 1 = su máxima.
- **R4 · el grupo de contrarias consecutivas**: la racha máxima de velas contrarias consecutivas que
  termina en la vela de R1. 0 = la mínima de la racha; 1 = la máxima.
- **R5 · la vela del pivote de M1 cuya ruptura da la entrada**: el último pivote BAJO de M1 formado
  antes de T (`pivotes_formados` con `cierre_vela_contraria`, la misma función que usa
  `referencia_del_breaker`). 0 = el nivel del pivote; 1 = la máxima de las velas desde la que marca
  el nivel hasta la contraria que lo forma, incluidas.
- **R6 · del punto de breaker al punto más alto** (sugerida por v7 0:15:50, «trazamos el GAN desde
  el posible punto de breaker hasta el punto más alto»): 0 = el nivel de R5; 1 = la máxima más alta
  de las velas entre ese pivote y T.

**Una regla «acierta» una operación** si su 0 y su 1 están los dos a ≤ τ del 0 y del 1 leídos
(τ = 2; sensibilidad 1 y 3). Se cuenta también cuántas aciertan solo el 0 o solo el 1.

**Lo que dibuja hoy el productor para ese mismo instante** se mide aparte, no como regla: la zona
que `detectar_esquema` tiene viva en T, con los supuestos de `scripts/verificacion_a21_entradas.py`
(zona desde la primera toma del día, lado del sesgo de la sesión de la toma, A-35
`cierre_vela_contraria`, A-44 `sin_tope`, A-21 en cada lectura, en DIAGNÓSTICO). Su entrada y su
extremo se comparan con el 0 y el 1 del trader con la misma τ.

**No se elige ganadora.** Se dice qué explica cada regla y qué casos no explica ninguna.

### 1.5 Notas de corrección del criterio (2026-09-28, después de ver la primera versión)

El criterio de §1.1–§1.4 no se reescribe. Al ver los resultados de la versión que lo sigue al pie de
la letra (**v1**) aparecieron dos cosas medibles que obligan a añadir dos versiones más. Las tres se
presentan siempre juntas (§3) y la salida las lleva por separado.

- **v2 · la vela en curso en T.** Todos los fotogramas en los que se leyó la hora de colocación caen
  en el segundo :59 del reloj del gráfico, así que a la vela de ese minuto le falta un segundo para
  cerrar. v1 la excluía («M1 cerradas antes de T»). La leyenda OHLC del gráfico en esos fotogramas
  enseña que el 1 de la caja es, varias veces, la máxima de esa vela: en v7 n.º 1 la leyenda dice
  `H 1.15370` y el 1 es 1.15370; en la n.º 4, `H 1.15322` y el 1 es 1.15322; en la n.º 7, `H 1.15268`
  y el 1 es 1.15268. v2 incluye la M1 en curso en T.
- **v3 · el desfase medido entre proveedores.** Las mismas leyendas dan el OHLC de OANDA de una vela
  que también está en el repositorio (Dukascopy), así que miden la diferencia vela a vela (§2.3):
  OANDA queda **por encima** de Dukascopy con mediana +2 puntos. Con τ = 2, un desfase sistemático
  de +2 deja la tolerancia coja por un lado. v3 es v2 con los niveles del trader desplazados en esa
  mediana (−2 puntos) antes de cruzar. **Es una corrección posterior, y se dice**: el desfase se midió
  con los mismos fotogramas y se aplica a todas las cajas por igual, sin tocarlo caja a caja.

## 2. Fase 2 · Las cajas del trader

Script: `scripts/bloque_de_la_caja.py`. Salida completa, con las tres versiones:
`BLOQUE-DE-LA-CAJA-SALIDA.txt`. Los 13 días de agosto de v7 y v8 son de desarrollo (0 de 13
reservados u ocultos, medido con `casos_reservados` y `casos_ocultos` antes de leer nada).

### 2.1 Cuántas cajas entran y cuántas no

**De 39 candidatas, entran 12; quedan fuera 27, todas por el mismo motivo: en los fotogramas citados
no hay caja de niveles de esa operación.**

- **v7, dentro (11)**: n.º 1, 2, 3, 4, 5, 7, 9, 10, 11, 12 y 15.
- **v7, fuera (13)**: n.º 6 (la única `Sell limit`: sin caja, solo la etiqueta), 8, 13 (en M15), 14,
  y de la **16 a la 25** salvo la 23 (DUDOSA): **desde la n.º 16 el trader deja de dibujar la caja**.
  Lo dice en v7 0:53:13: «aquí me salté el GAN para poder hacer el cálculo». Coloca la orden con su
  stop y su objetivo sin trazar la caja.
- **v8, dentro (1)**: n.º 1, con la caja dibujada DESPUÉS de colocar la orden (08:37:59, ya llena;
  a las 08:35:59 la orden está y la caja no).
- **v8, fuera (14)**: n.º 2, 3, 5, 6, 8, 9, 11 a 18. En sus fotogramas citados (ya abiertos en esta
  sesión en la rama de v8) solo hay etiquetas de orden, de stop y de objetivo, la herramienta de
  posición (riesgo/beneficio) o cajas «be» de operaciones anteriores.

Las 12 cajas son **ventas**: no hay ninguna compra con caja legible, así que nada de esta rama dice
nada de las compras.

### 2.2 Las 12 cajas leídas

Hora de colocación en el reloj del gráfico (UTC+2 fijo) y en UTC. «Leído» dice de dónde sale cada
nivel. La escala del eje va de 3,3 a 15 píxeles por punto según el fotograma; la legibilidad es ±1
punto donde el nivel coincide con una etiqueta de precio y ±1–2 donde se interpola.

| caja | día | colocación UTC+2 (UTC) | 0 | 1 | puntos | leído | orden en | stop en | fotograma |
|---|---|---|---|---|---|---|---|---|---|
| v7-1 | 08-03 | 07:47:59 (05:47:59) | 1.15358 | 1.15370 | 12 | 0 = etiqueta de la orden; 1 interpolado | el 0 | el 0,8 (±1) | v7/000227000 |
| v7-2 | 08-03 | 08:00:59 (06:00:59) | 1.15352 | 1.15376 | 24 | 0 = marca del eje; 1 = etiqueta del stop | **el 0,5** | **el 1** | v7/000404000 |
| v7-3 | 08-03 | 08:06:59 (06:06:59) | 1.15364 | 1.15389 | 25 | 1 = etiqueta del stop; 0 interpolado | **2 puntos bajo el 0** | **el 1** (luego al 0,8) | v7/000510000 |
| v7-4 | 08-03 | 09:33:59 (07:33:59) | 1.15306 | 1.15322 | 16 | 0 = orden; 1 = stop | el 0 | **el 1** | v7/000710000 |
| v7-5 | 08-03 | 11:46:59 (09:46:59) | 1.15274 | 1.15290 | 16 | 0 = posición; 1 = marca del eje | el 0 | el 0,8 | v7/000955000 |
| v7-7 | 08-03 | 13:11:59 (11:11:59) | 1.15256 | 1.15268 | 12 | 0 = orden; 1 interpolado | el 0 | el 0,8 | v7/001210000 |
| v7-9 | 08-03 | 14:09:59 (12:09:59) | 1.15338 | 1.15352 | 14 | 0 = marca del eje; 1 interpolado | el 0 | **el 1** | v7/001535000 |
| v7-10 | 08-04 | 09:44:59 (07:44:59) | 1.15129 | 1.15172 | 43 | 0 = posición; 1 desde el 0,8 del stop | el 0 | el 0,8 | v7/001930000 |
| v7-11 | 08-04 | 13:32:59 (11:32:59) | 1.15184 | 1.15210 | 26 | 0 = marca del eje; 1 = etiqueta del eje | el 0 | **el 1** | v7/002110000 |
| v7-12 | 08-04 | 13:56:59 (11:56:59) | 1.15174 | 1.15234 | 60 | 0 = posición; 1 desde el 0,8 del stop | el 0 | el 0,8 | v7/002180000 |
| v7-15 | 08-06 | 08:01:59 (06:01:59) | 1.15491 | 1.15516 | 25 | 0 = marca del eje; 1 desde el 0,8 = etiqueta del stop | el 0 | **el 1** | v7/002654000 |
| v8-1 | 08-12 | 08:35:59 (06:35:59) | 1.15354 | 1.15362 | 8 | 0 = posición; 1 = marca del eje | el 0 | el 0,8 (±1) | v8/000200000 |

**Lo que la lectura ya dice, antes de cruzar ninguna vela, y contradice en parte el brief**:

- **La orden va en el 0 en 10 de 12**. En v7 n.º 2 va en el 0,5, y en v7 n.º 3 dos puntos por debajo
  del 0.
- **El stop va en el 0,8 en 6 de 12 y en el 1 en otras 6** (v7 n.º 2, 3, 4, 9, 11 y 15). El brief
  decía «el stop en el 0,8». Las seis del 1 son de los días 3, 4 y 6. En v7 n.º 3 el stop empieza en
  el 1 y luego se mueve al 0,8, que es lo que el trader describe en voz («primer cálculo… desde el
  punto 1 y luego se recalcula… a 0,80», v7 0:06:07). Esto toca A-18 y no se resuelve aquí.

### 2.3 El desfase entre proveedores, medido en las leyendas

La leyenda OHLC del gráfico da la vela en curso de OANDA en el minuto del fotograma, y el repositorio
tiene esa misma vela de Dukascopy (BID). **Tres leyendas no valen**: en v7 n.º 9, 11 y 12 algún valor
difiere más de 10 puntos, porque la leyenda de TradingView enseña la vela que está bajo el cursor y no
la vela en curso (en v7 n.º 12 el cursor está sobre la vela de las 13:52). Sobre las otras 9 velas (36
valores):

| | |
|---|---|
| OANDA − Dukascopy, mediana | **+2 puntos** |
| máximo absoluto | 4 |
| a ≤ 1 punto | 13 de 36 |
| a ≤ 2 puntos | 27 de 36 |
| media con signo | +1,7 |

Es la primera medida de A-16 sobre agosto con vela entera: el desfase es de 1–2 puntos, como decía
A-16, **y con signo: OANDA por encima**. Con ese desfase y τ = 2, v1 y v2 pierden coincidencias que
existen por un lado. De ahí v3 (§1.5).

### 2.4 Qué velas dan el 0 y el 1 (v3; la salida trae v1 y v2)

Con la vela en curso incluida y los niveles corregidos (v3), **todos los niveles de las 12 cajas
tienen al menos una vela que los explica a ≤ 2 puntos**. En v1 quedaban sin explicación el 1 de cuatro
cajas (v7 n.º 1, 9 y 11, y v8 n.º 1); en v2, uno (v8 n.º 1). **En 10 de las 12 el 1 lo da la máxima de
la vela en curso en T o de la inmediatamente anterior**; solo en v7 n.º 10 y n.º 12 viene de velas de 20 y
12 minutos antes (y en las dos la posición ya estaba abierta cuando se ve la caja).

| caja | velas que dan el 1 (mecha) | velas que dan el 0 (las más recientes) | respecto a la toma de M15 del productor | respecto al llenado |
|---|---|---|---|---|
| v7-1 | 07:47 verde, la vela en curso | 07:44 a 07:47, mínimas de verdes y roja | ANTES: toma a las 08:00 UTC+2 | antes (llena 07:48) |
| v7-2 | 07:56 a 07:59 (verde y rojas) | 07:49 a 07:54, mínimas | en la toma (08:00) | antes (llena 08:01–08:04) |
| v7-3 | 08:05 verde | 07:58, 08:00 y 08:03, mínimas | después | antes (llena 08:07–08:11) |
| v7-4 | 09:33 verde, la vela en curso (y máximas de 08:29–08:34) | 09:32 verde, mínima; máximas de 09:15 y 09:30 | después | antes |
| v7-5 | 11:43 y 11:45 verdes | 11:41 a 11:43 verdes, mínimas | después | antes (llena 11:46) |
| v7-7 | 13:05 verde, 13:10 verde y 13:11 roja en curso | 13:05 a 13:10, mínimas | después | antes |
| v7-9 | 14:08 roja y 14:09 verde en curso | 14:08 roja y 14:09 verde, mínimas | después | antes |
| v7-10 | 09:24 verde y 09:25 roja (20 min antes) | 09:21 y 09:29 mínimas; **09:40 a 09:42 máximas** | después (toma 09:15) | la posición ya estaba abierta a las 09:44:59 |
| v7-11 | 13:32 verde, la vela en curso | 13:25 a 13:31, mínimas | después | antes (llena 13:33–13:39) |
| v7-12 | **13:44 verde (12 min antes)** | 13:43 verde, mínima | después | la posición ya estaba abierta a las 13:56:59 |
| v7-15 | 08:00 verde y 08:01 roja en curso | 07:55 a 08:00, mínimas | en la toma (08:00) | antes (llena 08:07) |
| v8-1 | 08:34 y 08:35 verdes (en curso) | 08:34 y 08:35 verdes, mínimas | después (toma 08:30) | la orden ya estaba; la caja se dibuja a las 08:37 |

Todas las velas del bloque están **antes del llenado**, que es la ruptura del 0. Respecto a la toma de
liquidez de M15 que calcula el productor (A-35 en diagnóstico, `cierre_vela_contraria`), una caja es
anterior a esa toma (v7-1), dos se colocan en el mismo minuto (v7-2 y v7-15) y nueve después. Eso
dice que la toma del productor y la del trader no son la misma, no qué toma usa el trader.

## 3. Fase 3 · Qué regla da el mismo 0 y el mismo 1

Una regla **acierta** una caja cuando da el 0 y el 1 del trader a ≤ τ puntos los dos. Las velas son
de Dukascopy (BID, UTC) y los niveles del trader se leyeron en OANDA (reloj UTC+2): en v1 y v2 se
cruzan tal cual, con el desfase de 1–2 puntos de A-16 dentro de la tolerancia; en v3 se restan los
+2 medidos en §2.3. Las lecturas «a» y «b» del productor (las dos de A-21) dan la misma zona en todas
las cajas, así que van en una sola fila.

### 3.1 Recuento sobre las 12 cajas

| regla | v1: a 1 / 2 / 3 | v2: a 1 / 2 / 3 | v3: a 1 / 2 / 3 | v3: solo el 0 a 2 | v3: solo el 1 a 2 |
|---|---|---|---|---|---|
| R1 · última vela contraria | 0 / 1 / 4 | 1 / 3 / 7 | 2 / **5** / 6 | 5 | 9 |
| R2 · R1 y la siguiente | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 | 1 |
| R3 · última envolvente contraria | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 1 | 0 | 1 |
| R4 · tramo de contrarias seguidas | 0 / 1 / 2 | 2 / 3 / 5 | 2 / **5** / 5 | 5 | 9 |
| R5 · último pivote BAJO de M1 | 1 / 1 / 1 | 2 / 2 / 2 | 1 / 2 / 2 | 3 | 2 |
| R6 · pivote y máxima hasta T | 1 / 1 / 1 | 3 / 4 / 4 | 2 / 3 / 4 | 3 | 9 |
| productor en T (a y b) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 1 | 0 |

**Con el criterio tal como se escribió (v1), ninguna regla explica más de una caja de 12 a 2 puntos.**
Las cinco de R1 y de R4 aparecen solo con las dos notas de §1.5, que son posteriores a ver v1. La
sensibilidad tampoco es monótona entre versiones: R1 a 3 puntos pasa de 7 en v2 a 6 en v3.

### 3.2 Caja a caja (v3, τ = 2)

Cada celda es «regla − trader» en el 0 / en el 1, en puntos. **Negrita**: acierta. «—»: la regla no
da caja.

| caja | R1 | R2 | R3 | R4 | R5 | R6 | productor |
|---|---|---|---|---|---|---|---|
| v7-1 | **+2 / 0** | — | −24 / −28 | **−1 / 0** | +1 / −4 | **+1 / 0** | sin zona: aún no hay toma de M15 |
| v7-2 | +13 / +3 | — | +15 / 0 | +13 / +3 | +18 / +3 | +18 / +3 | sin zona: toma sin esquema antes de T |
| v7-3 | +7 / +1 | — | +6 / −4 | +6 / +1 | +6 / −10 | +6 / +1 | +1 / −10 |
| v7-4 | +3 / −1 | — | −62 / −52 | −23 / −1 | −26 / −27 | −26 / −1 | +59 / +57 |
| v7-5 | +4 / −1 | −4 / −1 | −44 / −44 | −33 / 0 | −31 / −33 | −31 / 0 | +91 / +89 |
| v7-7 | **+2 / −1** | — | −56 / −55 | **+2 / −1** | −5 / −6 | −5 / 0 | +109 / +111 |
| v7-9 | **+2 / +1** | — | −19 / −18 | **+2 / +1** | **+1 / +1** | **+1 / +1** | +27 / +27 |
| v7-10 | −15 / −41 | — | −15 / −41 | −15 / −41 | −13 / −41 | −13 / −41 | −42 / −56 |
| v7-11 | +12 / +1 | — | +3 / −6 | **+2 / +1** | +3 / −6 | +3 / +1 | −97 / −94 |
| v7-12 | −24 / −44 | — | +13 / −30 | −24 / −44 | −20 / −62 | −20 / −44 | −87 / −118 |
| v7-15 | **0 / +1** | — | −5 / −28 | **0 / +1** | **+2 / +1** | **+2 / +1** | sin zona: toma sin esquema antes de T |
| v8-1 | **+1 / −1** | — | −3 / −3 | −13 / −1 | −10 / −10 | −10 / −1 | −3 / −4 |

R1 y R4 aciertan las mismas cuatro (v7-1, 7, 9 y 15) y **se separan en dos**: en v7-11 el 0 del
trader es la mínima del tramo entero de velas verdes (R4) y no la de la última (R1, +12); en v8-1 es
al revés, la mínima de la última verde (R1) y no la del tramo (R4, −13).

### 3.3 Lo que ninguna regla explica

A 2 puntos en v3 quedan **seis cajas sin regla**: v7-2, 3, 4, 5, 10 y 12. A 3 puntos entra v7-4 (R1,
+3 / −1) y quedan cinco.

- **v7-10 y v7-12: la medida no las puede juzgar.** En sus fotogramas la posición ya está abierta, así
  que T no es la hora de colocación sino la del primer fotograma citado con la caja. La ventana de las
  reglas acaba después de la colocación verdadera, y la última vela contraria ya es otra. Todas fallan
  por 13 a 62 puntos.
- **v7-2: la orden va en el 0,5 de la caja**, no en el 0. Todas las reglas dan el 1 a ≤ 3 puntos y el 0
  entre 13 y 18 puntos por encima: la caja del trader mide 24 puntos y la de R1 14.
- **v7-3: el 0 del productor y el 1 de las reglas.** R1, R4 y R6 dan el 1 a +1 y fallan el 0 por 6–7;
  el productor da el 0 a +1 y falla el 1 por 10. La orden va 2 puntos por debajo del 0.
- **v7-5: el 0 cae entre dos reglas.** R1 lo da a +4 y R2 a −4, las dos con el 1 a −1.

De las diez cajas en las que T sí es la colocación, R1 o R4 explican seis a 2 puntos y siete a 3.

### 3.4 Frente a lo que dibuja el productor en ese instante

**El productor no da la caja del trader en ninguna de las 12**, ni a 3 puntos. Solo da el 0 de v7-3
(+1). En tres no dibuja nada: en v7-1 aún no hay toma de M15, y en v7-2 y v7-15 la toma es de ese
mismo minuto y no hay esquema antes de T. En el resto **la zona del productor no se mueve en todo el
día** (día 3: 1.15363 / 1.15377 para cinco cajas; día 4: 1.15085 / 1.15114 para tres), porque sale de
la primera toma del día; **el trader traza una caja nueva en cada operación**, pegada al precio del
momento. La más cercana es v8-1 (−3 / −4).

No se elige ganadora.

## 4. Lo que la medida sostiene, lo que no, y las preguntas del martes

### 4.1 Lo que sostiene

- **El 1 es casi siempre la máxima de la última vela alcista.** En v3, R1, R4 y R6 dan el 1 a
  ≤ 2 puntos en 9 de 12, y en 10 de 12 lo da la vela en curso en T o la inmediatamente anterior (§2.4).
- **El 0 es donde las reglas se separan.** R1 y R4 lo dan en 5 de 12, y se contradicen en v7-11 y v8-1.
- **R2, R3 y R5 no describen lo que hace el trader** en estas cajas: aciertan como mucho dos.
- **La zona del productor en T no coincide con ninguna caja** y no sigue al precio durante el día.
- **La orden va en el 0 en 10 de 12, y el stop va en el 0,8 en seis y en el 1 en otras seis** (§2.2).

### 4.2 Lo que no sostiene

- **Ninguna regla.** Son 12 cajas, todas ventas, de cuatro días, y once del mismo video. Nada de esto
  dice nada de las compras, ni de las operaciones de v7 desde la n.º 16 y de v8, donde el trader no
  dibuja caja.
- **Las cifras altas dependen de dos correcciones posteriores.** Con el criterio al pie de la letra
  (v1) ninguna regla pasa de una caja. La vela en curso (v2) y el desfase de +2 (v3) salen de los mismos
  fotogramas que se miden; están declarados, pero no son un criterio escrito antes.
- **La tolerancia es del tamaño del ruido.** La lectura en pantalla es de ±1–2 puntos y el desfase
  entre proveedores de 1–2. A 1 punto ninguna regla pasa de tres cajas en ninguna versión.
- **Tres T no son la colocación de la caja.** En v7-10 y v7-12 la posición ya estaba abierta; en v8-1
  la caja se dibujó después de la orden, aunque ahí T sí es la colocación de la orden (08:35:59).
- **Nada dice que el trader elija el bloque en M1.** Solo que, en M1, sus niveles caen donde caen.

### 4.3 Preguntas para la sesión del martes

Cerradas, sobre días de agosto (todos de desarrollo), sin el resultado de la operación. **Choque que
hay que resolver antes**: el brief pide enseñar el gráfico cortado antes de la entrada, y la regla 2
de `docs/runbooks/SESION-DE-PREGUNTAS.md` dice «No se enseña ningún gráfico de ningún día». Por eso
cada pregunta está escrita para hacerse con palabras; enseñar el gráfico exige que el consultor cambie
antes esa regla, y no se cambia en esta rama.

1. **«Cuando antes de la caída hay varias velas verdes seguidas, ¿el bloque es solo la última verde, o
   todas las verdes seguidas?»** (a) solo la última, (b) todas las seguidas, (c) depende, y de qué.
   Casos: 4 de agosto, venta colocada a las 13:32 (reloj del gráfico), donde el 0 es la mínima de todo
   el tramo verde; 12 de agosto, venta colocada a las 08:35, donde el 0 es la mínima de la última
   verde. Es la diferencia entre R1 y R4 (§3.2).
2. **«¿Trazas la caja cuando la vela del bloque ya ha cerrado, o mientras se está formando?»**
   (a) cerrada, (b) formándose, (c) las dos. Casos: 3 de agosto a las 07:47 y a las 13:11, donde el 1
   de la caja es la máxima de la vela del minuto en curso, a un segundo de cerrar. Decide si el motor
   puede quedarse con velas cerradas (§1.5, v2).
3. **«¿El stop va en el 0,8 de la caja o en el 1?»** (a) siempre en el 0,8, (b) siempre en el 1,
   (c) primero en el 1 y luego se recalcula al 0,8, (d) depende, y de qué. Casos: 3 de agosto, venta de
   las 09:33 con el stop en el 1, y venta de las 11:46 con el stop en el 0,8. Toca A-18; no se resuelve
   aquí.

## 5. Estado

Fases 1 a 4 completas. Criterio commiteado antes de medir (4c9c0cd); cajas y medida, en los commits
siguientes. No se ha cambiado el motor, el productor, RN-011 ni ningún parámetro, regla, ambigüedad,
evidencia o feedback. **Rama lista para revisión, NO cerrada.**
