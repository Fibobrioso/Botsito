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

## 5. Estado

Criterio de §1 commiteado antes de medir (4c9c0cd). Fase 2 en este commit; las fases 3 y 4 van en
el siguiente.
