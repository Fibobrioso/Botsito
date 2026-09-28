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

## 2. Estado

Criterio escrito y commiteado antes de medir. Las fases 2 a 4 van en los commits siguientes.
