# A-35, los fotogramas: la medición

Rama `trabajo/a35-pivote-formado`, 2026-09-24. Sin merge, sin tag y sin push.

La medición se hizo con el criterio congelado en `A35-FOTOGRAMAS-CRITERIO.md` (commit `14ed54e`), sin
cambiarlo.

**El registro de lo abierto** es `A35-FOTOGRAMAS-REGISTRO.txt`, la salida tal cual de
`uv run python scripts/a35_fotogramas.py`:
- 89 líneas `INTEGRIDAD … = indice F05: OK`, una por fotograma de la lista cerrada;
- para cada fotograma, los píxeles distintos del anterior.

**Todos cambian**, así que por el criterio se abrieron los 89, porque el vídeo comprimido nunca repite
un fotograma exacto.

**Cómo se leyó:** a mano, con la imagen delante, y cada nota se escribió al terminar su lote. Lo que no
se lee con claridad se escribe «no legible». Las horas del gráfico son las del eje de FX Replay, en
UTC+2 (CLAUDE.md). Los precios son los que marca el eje o el cursor en ese fotograma.

**Exposiciones: ninguna.** Ningún fotograma de los 89 muestra Analytics ni un agregado. Las fechas
que se ven en los gráficos son de **enero**, material de desarrollo que no tiene ningún día en
ninguna partición. No hay nada que declarar en `HOLDOUT-EXPOSICIONES.md`.

## P4 · v3 #976 · 1:15:40-1:15:59 · `fr-v3-982da728/4540000`-`/4559000`

**Los 20 fotogramas** muestran un **documento de Word, sin gráfico**. Es el cuestionario, en su
sección «2 · Precisiones estructurales (para codificar)», con la pregunta «2.1 · Swing (estructura):
¿cuántas velas a cada lado validan un máximo o mínimo estructural?» y su casilla vacía, con el cursor
dentro.

| campo | valor |
|---|---|
| (a) temporalidad | no aplica: no hay gráfico |
| (b)-(e) | no aplica: no hay gráfico |
| (f) la marca se mueve | no aplica |
| (g) el gráfico avanza | no aplica |
| (h) marca ya presente | no aplica |

## P5 · v4 #461-#462 · 0:28:01-0:28:14 · `fr-v4-9ad0ebb8/1681000`-`/1694000`

Recorrido:
- **1681-1684** (0:28:01-0:28:04): dibuja un zigzag con la herramienta «path» («Double-click to
  finish Path»). Va desde el alto de ~08:36 (1.19750) por los bajos y altos de ~08:40-08:45 hasta
  ~08:46 (1.19672). La línea azul horizontal larga de 1.19750 ya estaba.
- **1685-1690:** el cursor pasa por las velas. En 1690 elige la herramienta de línea.
- **1691 (0:28:11): PRIMER fotograma con la marca nueva.** Es una línea horizontal, seleccionada, de
  ~08:45 a ~08:54, que el eje da en **1.19715**. Su extremo izquierdo está en el techo del cuerpo de
  la roja de ~08:45; la mecha de esa vela sube más, y el cursor la marca en 1.19719.
- **1692:** el zigzag se borra y la línea sigue en ~1.19715.
- **1693:** la línea **se mueve** a 1.19720 (de ~08:43 a ~08:52).
- **1694:** **se mueve otra vez**, a **1.19739** (de ~08:40 a ~08:49), a la altura de las mechas
  superiores de ~08:40-08:42.
- El reloj del replay marca **08:46:59 UTC+2 en los 14 fotogramas**. La última vela es la verde de
  08:46, y no hay ninguna a su derecha.

| campo | valor (fotograma 1691, 0:28:11, salvo que se diga otro) |
|---|---|
| (a) temporalidad | **1m**: el botón «1m» resaltado y la leyenda «EUR/USD · 1» |
| (b) vela del extremo cerrada | la roja de ~08:45, donde arranca la línea, está cerrada: la sigue la de 08:46 |
| (c) vela contraria | no legible cuál es la contraria de este flujo. La última vela, la verde de 08:46, cierra a la hora del reloj (08:46:59), y el reloj no avanza en toda la ventana |
| (d) la mecha de la contraria supera el extremo | no legible |
| (e) mecha o cuerpo | en 1691, **cuerpo**: el techo del cuerpo de la roja de ~08:45, a 1.19715. En 1694, a la altura de **mechas**, a 1.19739 |
| (f) la marca se mueve | **sí**: 1.19715 (1691) → 1.19720 (1693) → 1.19739 (1694) |
| (g) el gráfico avanza | **no**: el reloj está parado en 08:46:59 |
| (h) marca ya presente | **no**: la línea aparece en 1691, dentro de la ventana |

## P6 · v4 #597-#601 · 0:35:07-0:35:24 · `fr-v4-9ad0ebb8/2107000`-`/2124000`

Recorrido:
- **2107 (0:35:07): la línea ya está.** Es horizontal, bajo el flujo bajista de ~06:45-07:30, y va
  de ~06:45 a ~08:15. También están ya otras líneas y un esquema a la izquierda (~01:00-03:00).
- **2108-2111:** dibuja un zigzag desde el alto de ~06:45 hasta el bajo de ~07:30. Ese vértice queda
  ligeramente **por debajo** de la línea. Después el zigzag sube por la verde de ~07:45-08:00,
  hasta ~1.1745.
- **2112-2118:** desplaza la vista y cambia el zoom. El cursor pasa por la roja de ~07:30 (1.17438)
  y la verde de ~07:45-08:00 (1.17451).
- **2119-2124:** el cursor pasa sobre la línea y el eje la marca en 1.17408-1.17420. En **2120** da
  **1.17414**, y en **2123** la línea está seleccionada, con asas en ~06:45 y ~08:15, en
  **1.17415**. En 2124 se deselecciona y sigue en el mismo sitio.
- El reloj del replay marca **15:14:59 UTC+2 en los 18**. La última vela es la de ~15:00: todo el
  tramo de la línea es de horas antes.

| campo | valor (fotograma 2107, 0:35:07, el primero de la ventana) |
|---|---|
| (a) temporalidad | **15m**: el botón «15m» resaltado y la leyenda «EUR/USD · 15» |
| (b) vela del extremo cerrada | **sí**: el bajo de ~07:30, a unas 7 h de la última vela |
| (c) vela contraria | las verdes de ~07:45-08:00, **cerradas**, por encima de la línea (gráfico parado) |
| (d) la mecha de la contraria supera el extremo | a la vista, no cruzan la línea. Al punto: no legible |
| (e) mecha o cuerpo | no legible: el vértice del bajo queda un poco por debajo de la línea (~1.1741 frente a 1.17415) |
| (f) la marca se mueve | **no** se mueve ni se borra en la ventana |
| (g) el gráfico avanza | **no**: el reloj está parado en 15:14:59 |
| (h) marca ya presente | **sí**, desde 2107 |

## P8 · v4 #844-#849 · 0:50:44-0:50:56 · `fr-v4-9ad0ebb8/3044000`-`/3056000`

Recorrido:
- **3044 (0:50:44): las líneas ya están.**
  - Una en ~1.1724, de ~11:45 a ~13:00.
  - Otra en ~1.1727, sobre los altos de ~13:30-14:00.
  - La etiqueta «m15 lq», en ~1.1728, a la izquierda (~09:00-10:15).
  - Un zigzag en ~13:00-13:30.
- **3045-3049:** mueve el cursor y el zoom. En **3048**, el fotograma citado, no hay ninguna línea
  nueva.
  - Hay marcadores circulares azules en varias velas; qué son no es legible.
  - A la derecha de la verde de ~15:00 hay un rectángulo translúcido rojo y verde, no legible.
- **3050-3056:** dibuja un **zigzag**: alto de ~10:45 → bajo de ~11:15-11:30 → alto de ~11:45 → bajo
  de ~12:30 → sube hacia ~13:00.
  - El vértice del alto de ~11:45 cae sobre el arranque de la línea de ~1.1724, que ya estaba.
  - En **3053-3054** se ve que esa línea arranca en la **punta de la mecha superior** de la verde de
    ~11:45; su cuerpo acaba más abajo.
  - No se traza ninguna línea horizontal nueva.
- El reloj del replay marca **15:29:59 UTC+2 en los 13**.

| campo | valor (fotograma 3044, el primero de la ventana; (e) en 3053-3054) |
|---|---|
| (a) temporalidad | **15m**: el botón «15m» resaltado y la leyenda «EUR/USD · 15» |
| (b) vela del extremo cerrada | **sí**: la verde de ~11:45, horas antes de la última vela |
| (c) vela contraria | cerrada: todo el tramo es histórico (gráfico parado) |
| (d) la mecha de la contraria supera el extremo | no legible |
| (e) mecha o cuerpo | **mecha**: la punta de la mecha superior de la verde de ~11:45 (3053-3054) |
| (f) la marca se mueve | **no**: ninguna línea horizontal se mueve ni se borra. Solo se dibuja el zigzag |
| (g) el gráfico avanza | **no**: el reloj está parado en 15:29:59 |
| (h) marca ya presente | **sí**, desde 3044 |

## P9 · v4 #942 · 0:58:06-0:58:29 · `fr-v4-9ad0ebb8/3486000`-`/3509000`

Recorrido:
- **3486 (0:58:06): las marcas ya están.**
  - La etiqueta «m15 lq», en una línea de ~1.1741 (~06:45-08:45).
  - «m1 lq» (~1.1733).
  - «15 lq», en una línea de ~1.1731 (~09:15-10:15).
  - Una línea en el bajo de ~09:15-09:30 (~1.1723).
  - Otra en ~1.1723, de ~11:45 a ~13:00.
  - Zigzags y marcadores circulares.
- **3487-3499:** desplaza la vista (01:00-16:00, luego 03:00-16:00). El cursor pasa por la roja de
  ~11:00, la roja de ~11:15 (1.17127-1.17144) y la verde de ~11:30 (1.17153-1.17181). En **3493**
  selecciona un zigzag ya dibujado, con vértices en el bajo de ~11:15 y el alto de ~11:45, sin
  moverlo.
- **3500-3501:** **selecciona la línea del bajo de ~09:15** (asas en ~09:00 y ~10:15), y el eje la
  da en **1.17238-1.17239**. Tiene la barra de edición abierta y **no la mueve**.
- **3502-3509:** la deselecciona y lleva la vista a la izquierda (~21:30-09:30). Se ve la verde
  contraria de ~09:30, **cerrada**, por encima de la línea del bajo. No aparece ninguna marca nueva.
- El reloj del replay marca **18:44:59 UTC+2 en los 24**. Hay velas hasta ~15:15.

| campo | valor (fotograma 3486, el primero de la ventana; la línea del bajo en 3500-3501) |
|---|---|
| (a) temporalidad | **15m**: el botón «15m» resaltado y la leyenda «EUR/USD · 15» |
| (b) vela del extremo cerrada | **sí**: el bajo de ~09:15, horas antes de la última vela |
| (c) vela contraria | la verde de ~09:30, **cerrada** (3507-3508; gráfico parado) |
| (d) la mecha de la contraria supera el extremo | no legible |
| (e) mecha o cuerpo | no legible |
| (f) la marca se mueve | **no**: se selecciona en 3500-3501 y no se mueve ni se borra |
| (g) el gráfico avanza | **no**: el reloj está parado en 18:44:59 |
| (h) marca ya presente | **sí**, desde 3486 |

## Estado

MEDIDO. La tabla frente al criterio va en el commit siguiente.
