# Sesión 02 con el trader, segunda grabación: el vídeo v8, rescatado, y la segunda mitad de agosto

Rama `trabajo/sesion-02`, 2026-09-27, tarea autónoma. Sin merge, sin tag, sin push. **Nada se
resuelve aquí**: ni evidencia, ni feedback, ni cambios en `ambiguedades.yaml`, `parametros.yaml` o
`strategy_spec.yaml`. Continúa `SESION-02-VIDEO.md` (v7) con el mismo método; lo que aquí no se
repite, está allí.

## 0. Lo que la medida dice del brief

1. **v8 CONTINÚA la misma sesión de FX Replay de v7.** El primer fotograma abierto (0:00:20,
   `000020000`) muestra el H4 con el cursor en el martes 11 de agosto a las 15:00:59 UTC+2 y el
   saldo de la cuenta de replay en 100 042,00 $: exactamente donde v7 terminó. El tramo con audio
   recorre el 12, 13, 14, 17, 18 y el 19 de agosto hasta las 11:13 (§3). Con v7 (3–11) y v8, la
   sesión 2 cubre del 3 al 19 de agosto en pantalla con audio, y desde el 19 hasta donde llegara
   sin audio (no abierto).
2. **El audio real acaba en 0:40:00 y el ASR no alucina en el silencio** (§2): 229 segmentos, todos
   con `t0` antes de 0:40:00; ninguno solapa el tramo de relleno.
3. **Tampoco hay códigos de pregunta**: como en v7, el trader backtestea en voz alta. El cuestionario
   de la hoja se repetirá entero en la próxima sesión, así que esta grabación vale por lo que se ve.
4. **Las órdenes siguen siendo STOP**: 11 `Sell stop` y 3 `Buy stop` legibles, 4 no legibles, ninguna
   `limit` (§3.2). En dos fotogramas se ve el menú contextual de FX Replay con las dos opciones
   —«Buy … limit» y «Sell … stop» al mismo precio— y el trader elige la STOP (0:36:20, `002180000`;
   0:39:35, `002375000`).

## 1. Fase 1 · Ingesta como v8 y la procedencia

| pieza | id / fichero | commit |
|---|---|---|
| fuente | `knowledge/corpus/fuentes.yaml`, `video_id: v8`, `fichero: "intento-3-audio-relleno.mp4"`, sin `drive_id`, `naturaleza: sesion 2 … RESCATADA …` | `9725e0c` |
| inventario | `manifest.yaml` regenerado: 8 vídeos, sha256 `697c5146…`, 7248,4 s, 1920×1080, 30 fps, audio | `9725e0c` |
| fotogramas | `fr-v8-ee53cbde`: 7249 PNG a 1 fps, 0 huecos, 0 extra (5 min) | `9725e0c` |
| transcripción | `tr-v8-large-v3-int8-float16-34b7e90f`: 229 segmentos en 12 fragmentos (7,4 min en GPU) | `9725e0c` |
| test | `test_fuentes_y_manifiesto_reales_coherentes`: `v1..v7` → `v1..v8` | `9725e0c` |

**El nombre.** La convención de v1–v7 guarda el nombre original del fichero en `fuentes.yaml`,
`manifest.yaml` y los dos manifiestos. El nombre que Aleks le dio al copiarlo al corpus,
`intento-3-audio-relleno.mp4`, no lleva fecha ni nada que nombrar un día: entra tal cual.

**La procedencia.** El esquema de `fuentes.yaml` (`corpus/inventario.py`, `FuenteVideo`) no tiene
campo de notas: sus campos son `video_id`, `fichero`, `drive_id`, `bytes`, `fecha_grabacion` y
`naturaleza`. Por eso la procedencia va en DOS sitios de la entrada de v8: un comentario YAML de
cinco líneas encima de `naturaleza`, y el propio texto de `naturaleza` (que es lo que el manifiesto
copia). Dice: vídeo rescatado, laptop suspendida en el minuto 40, grabación seguida sin audio,
flujo de vídeo entero copiado sin recodificar, audio real solo hasta 40:00 y silencio de relleno
de 40:00 a 2:00:48. La carpeta `rescate` del Escritorio (cinco ficheros, 31 GB) **no se tocó**: no
se borró, movió ni renombró nada; `marcas-v8.txt` no existe en ella.

**Lo medido sobre el audio, con `ffmpeg silencedetect` (umbral −50 dB, mínimo 30 s)**: silencio
continuo desde 2400,17 s (0:40:00,17) hasta el final, 7248,4 s. Antes del corte hay tres silencios
largos, de 31,6 s (hasta 774 s), 35,0 s (1286–1321 s) y 103,7 s (1865–1969 s): son pausas del
trader dentro del tramo con audio, no relleno.

## 2. Fase 2 · Transcripción, cuarentena y la prueba de alucinación

- **ASR**: el del corpus, sin cambios (`botsito corpus transcribe --video v8`). Ver `SESION-02-VIDEO.md`
  §2 para los parámetros.
- **Cuarentena**: `scratchpad/cuarentena_v8.py` importa `en_cuarentena` de `scripts/transcribir_sesion.py`
  y lo aplica a la cruda antes de leer nada. **0 segmentos en cuarentena, 0 bloques** (229 segmentos,
  1617 s de habla según el ASR). Ninguna mención a septiembre, marzo, mayo o febrero, ninguna fecha
  numérica. Por eso **no hay tramo que registrar** en `tramos_no_citables.yaml` y no hay commit de
  tramos.
- **Alucinación en el silencio**: el script cuenta los segmentos cuyo `t1` pasa de 2400,17 s:
  **0**. El último segmento empieza en 0:39:53 y acaba antes de 0:40:00. El ASR no escribió nada
  sobre el silencio de relleno, así que no hay texto alucinado que declarar no citable. Si en una
  retranscripción apareciera, el script ya lo registra como tramo con motivo «silencio de relleno
  (alucinación del ASR)».
- **Solo se ha leído la versión filtrada** (`scratchpad/v8.filtrada.txt`, fuera del repositorio).

## 3. Fase 3 · Días y operaciones (SOLO el tramo con audio)

**Regla aplicada.** Hasta 0:40:00, fotogramas por instante localizado en la transcripción y su
vecindario (ADR-0038). Desde 0:40:00, **ninguno**: `marcas-v8.txt` no existe, así que los 4848
fotogramas del tramo sin audio (`002400000` a `007248000`) están en disco y **no se abrió ni uno**.
Se abrieron **74 PNG distintos**, todos con marca de tiempo menor que 0:40:00 (§3.3). Reloj de
pantalla: `UTC+2` en todos.

Una particularidad de esta grabación: desde 0:19:25 la pantalla es la vista de Discord de la
pantalla compartida del trader (cabecera «720p 30FPS EN DIRECTO» y el nombre de usuario del trader,
que no se copia aquí), no la captura directa; los fotogramas siguen siendo legibles.

### 3.1 Los días, comprobados ANTES de escribirlos

`casos_reservados` y `casos_ocultos`: 34 casos ocultos, ninguno de `2026-08`. `scratchpad/comparar.py`
lo repite por día antes de leer ningún caso.

| día (pantalla) | qué se ve | operaciones | fotograma que fija el día |
|---|---|---|---|
| miércoles 2026-08-12 | 07:00–15:00 | 6 (n.º 1–6; la 4 DUDOSA) | 000180000 (`Wed 12 Aug '26`, 08:35:59) |
| jueves 2026-08-13 | 07:00–15:00 | 5 (7–11; la 7 y la 10 DUDOSAS) | 000740000 (`Thu 13 Aug '26`, 09:21:59) |
| viernes 2026-08-14 | la sesión, sin entradas: «el precio explotó directamente y no nos generó ninguna entrada» (0:22:04–0:22:38) | 0 | 001330000 (M15, `Fri 14 Aug '26 15:00` en el eje) |
| lunes 2026-08-17 | 07:00–15:00 | 3 (12–14) | 001478000 (`Mon 17 Aug '26`, 07:15:59) |
| martes 2026-08-18 | 07:00–15:00 | 3 (15–17) | 001870000 (`Tue 18 Aug '26`, 07:58:59) |
| miércoles 2026-08-19 | hasta las 11:13 | 1 (18, resultado no visto) | 002375000 (`Wed 19 Aug '26`, 11:01:59) |

### 3.2 La tabla por operación

Todas vienen del **tramo con audio**; del tramo sin audio no hay ninguna fila, por regla. Misma
lectura que v7: etiquetas de la orden, del stop (USD negativos) y del objetivo (USD positivos),
avisos de la plataforma, y el saldo. Hora = la del llenado si hay aviso o posición abierta; si no,
la ventana entre la orden y el primer fotograma con la posición, y se dice. «—» = no legible en los
fotogramas abiertos. **DUDOSA** = el trader dice que no se toma, o la pantalla no permite fijar la
operación; las dudosas no entran en la comparación de §4.

| n.º | día | hora UTC+2 | dir. | entrada | stop | objetivo | etiqueta FX Replay | min. v8 | fotogramas | cómo se fijó |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 08-12 | 08:36–08:37 | venta | 1.15354 | 1.15361 | 1.15323 | `Sell stop` | 0:03:00–0:03:35 | 000180000, 000200000, 000215000 | orden 08:35:59; caja 0=1.15354, 1=1.15362; «Take profit moved to 1.15323» y +4 abierto a las 08:37:59; «Closed … Sell 100000 at 1.15354 … now flat» a las 08:42:59 (BE) |
| 2 | 08-12 | 09:21–09:25 | venta | 1.15379 | 1.15395 | 1.15331 | `Sell stop` | 0:04:10–0:04:50 | 000250000, 000270000, 000290000 | «Entry price moved to 1.15379» a las 09:20:59; abierta (−3) a las 09:25:59; «be» y saldo previo a las 10:27:59 (BE) |
| 3 | 08-12 | 10:46–11:00 | venta | 1.15389 | 1.15401 | 1.15356 | `Sell stop` | 0:05:40–0:06:10 | 000340000, 000355000, 000370000 | orden con «Take profit added» a las 10:45:59; abierta (+11) a las 11:00:59 y **cerrada a mano en la vela de cierre de la sesión** (saldo +11); el trader: «se lo cuenta como ganada pero yo no lo contaría» (0:05:54) |
| 4 | 08-12 | 13:33–13:51 | venta | 1.15384 | — | — | `Sell stop` | 0:07:50–0:08:20 | 000470000, 000500000 | orden 13:32:59; saldo −30 a las 13:51:59. **DUDOSA**: en ese tramo dice «aquí hay dos entradas que son las erróneas entonces … no lo tomo» (0:07:35–0:08:37) |
| 5 | 08-12 | 14:18–14:22 | venta | 1.15436 | 1.15459 | 1.15370 | `Sell stop` | 0:08:20–0:09:40 | 000500000, 000525000, 000540000, 000560000, 000580000 | la orden se coloca en 1.15398 (13:51:59), se **actualiza** a 1.15412 (14:04:59) y a 1.15436 (14:17:59); abierta (+2) a las 14:22:59; «BE» y saldo previo a las 14:34:59 |
| 6 | 08-12 | 14:30 | venta | 1.15413 | 1.15482 | 1.15257 | `Sell stop` | 0:10:05–0:10:20 | 000605000, 000620000 | **tras rebobinar el replay a las 14:30** (el fotograma anterior iba por 14:34:59): «Stop order executed: Sell 100000 at 1.15413» a las 14:30:59 sobre la vela de las 14:30; saldo −69 a las 14:56:59 |
| 7 | 08-13 | 09:21–09:30 | venta | 1.15188 | 1.15207 | — | `Sell stop` | 0:12:20–0:12:40 | 000740000, 000760000 | orden 09:21:59; a las 09:30:59 «Closed your open position: Sell 100000 at 1.15205, closed from avg entry 1.15205» y saldo −32. **DUDOSA**: dice «aquí no podríamos tomar la entrada … no lo tomamos» (0:12:15–0:13:07) y las cifras no cuadran entre sí |
| 8 | 08-13 | ≤11:31 | venta | 1.15302 | 1.15321 | — | — | 0:16:55–0:17:15 | 001015000, 001035000 | abierta (+4) a las 11:31:59; saldo −21 a las 11:38:59 |
| 9 | 08-13 | 11:39–11:46 | venta | 1.15318 | 1.15328 | 1.15288 | `Sell stop` | 0:17:15–0:17:50 | 001035000, 001050000, 001070000 | orden 11:38:59; abierta a las 11:46:59; sin etiquetas y saldo −2 a las 11:56:59 |
| 10 | 08-13 | 12:02–12:08 | venta | — | — | — | — | 0:18:05–0:18:30 | 001085000, 001110000 | «be» y una línea en 1.15342 a las 12:02:59; saldo −14 a las 12:08:59. **DUDOSA**: ni entrada ni etiqueta legibles |
| 11 | 08-13 | 12:07–13:03 | venta | 1.15349 | 1.15366 | — | `Sell stop` | 0:18:50–0:22:10 | 001130000, 001165000, 001330000 | orden con «Stop loss added» a las 12:06:59; «be» a las 13:03:59; saldo +48 a las 13:14:59 (3 × 16) |
| 12 | 08-17 | 07:16–07:53 | compra | 1.15842 | 1.15828 | 1.15874 | `Buy stop` | 0:24:38–0:25:00 | 001478000, 001500000 | orden a las 07:15:59; saldo +42 a las 07:53:59 |
| 13 | 08-17 | 12:15–12:30 | compra | 1.15938 | — | — | — | 0:26:50–0:27:20 | 001610000, 001640000 | «Closed … Buy 100000 at 1.15938, closed from avg entry 1.15938: now flat» a las 12:30:59 (BE); la orden no se vio |
| 14 | 08-17 | 12:59–13:07 | compra | 1.15914 | 1.15896 | — | `Buy stop` | 0:28:10–0:29:22 | 001690000, 001720000, 001745000, 001762000 | etiquetas en 1.15924/1.15912 a las 12:49:59 (orden previa); `Buy stop` 1.15914 a las 12:58:59; abierta (+21) a las 13:07:59; «Closed … Buy 100000 at 1.15914 … now flat» a las 13:13:59 (BE) |
| 15 | 08-18 | ≤07:58 | compra | 1.15734 | 1.15707 | — | — | 0:31:10–0:34:20 | 001870000, 002060000 | etiquetas en 1.15743 / 1.15734 / 1.15707 (−27) a las 07:58:59; dirección deducida del stop por debajo; saldo +41 a las 13:29:59 |
| 16 | 08-18 | 11:34–11:40 | venta | 1.15778 | → 1.15778 (BE) | 1.15733 | `Sell stop` | 0:35:10–0:36:00 | 002110000, 002125000, 002160000 | orden 11:33:59; «Stop loss moved to 1.15778» con +30 abierto a las 11:40:59; saldo sin cambio a las 12:03:59 (BE); stop original no legible |
| 17 | 08-18 | 12:00–12:08 | venta | 1.15773 | → 1.15773 (BE) | 1.15695 | `Sell stop` | 0:36:20–0:37:35 | 002180000, 002205000, 002255000 | menú contextual «Sell 1 OANDA:EURUSD @ 1.15773 stop» a las 11:59:59; «Stop loss moved to 1.15773» a las 12:08:59; saldo de vuelta al previo a las 14:34:59 (BE) |
| 18 | 08-19 | 11:02 | compra | 1.15983 | 1.15964 | 1.16036 | `Buy stop` | 0:39:35–0:39:59 | 002375000, 002390000, 002399000 | menú contextual «Buy 1 OANDA:EURUSD @ 1.15982 stop» a las 11:01:59; abierta (+1) a las 11:02:59 y (+18) a las 11:13:59; **resultado no visto**: el audio acaba en 0:40:00 |

**Etiquetas de orden** (18 filas): `Sell stop` 11, `Buy stop` 3, no legible 4, `limit` 0.

Tres cosas descriptivas para el consultor: (a) en la n.º 5 la orden stop se **mueve tres veces** a
medida que aparece un punto de breaker nuevo (A-29/A-38); (b) en la n.º 6 el trader **rebobina el
replay** y repite la entrada de las 14:30 de otra forma (la primera versión, n.º 5, cerró en BE); (c)
en la n.º 3 cierra a mano en la vela de cierre de la sesión y dice que él no la contaría (A-30).

### 3.3 Fotogramas abiertos (74, todos < 0:40:00)

`data/fotogramas/v8/png-1fps/`: 000020000, 000080000, 000150000, 000180000, 000200000, 000215000,
000235000, 000250000, 000270000, 000290000, 000310000, 000320000, 000340000, 000355000, 000370000,
000390000, 000460000, 000470000, 000500000, 000525000, 000540000, 000560000, 000580000, 000605000,
000620000, 000650000, 000740000, 000760000, 000790000, 000900000, 000930000, 000950000, 000960000,
000980000, 001015000, 001035000, 001050000, 001070000, 001085000, 001110000, 001130000, 001165000,
001205000, 001330000, 001370000, 001420000, 001450000, 001478000, 001500000, 001540000, 001570000,
001585000, 001610000, 001640000, 001690000, 001720000, 001745000, 001762000, 001800000, 001830000,
001870000, 002060000, 002110000, 002125000, 002160000, 002180000, 002205000, 002255000, 002285000,
002330000, 002355000, 002375000, 002390000, 002399000. Ninguno es una captura de Analytics; el
único agregado en ellos es el saldo de la cuenta de replay (§6).

## 4. Fase 4 · Comparación con el backtest original, y el recuento conjunto v7 + v8

Solo los días del tramo con audio (12, 13, 14, 17, 18 y 19 de agosto), todos `dev`; solo sus filas
ya ingeridas (`knowledge/cases/dev/caso-eurusd-2026-08-*.yaml`); sin abrir el libro ni ningún
agregado. Criterio de ADR-0043 por `emparejar` (§4 de `SESION-02-VIDEO.md`). Las tres DUDOSAS
quedan fuera. Script: `scratchpad/comparar.py ops_v8.json v8`.

| | |
|---|---|
| operaciones del vídeo comparadas | 15 (18 menos 3 dudosas) |
| filas del backtest original en esos días | 7 (12: 1; 13: 2; 14: 1; 17: 1; 18: **sin caso**; 19: 2) |
| parejas | 2 |
| solo en el vídeo | 13 |
| solo en el backtest | 5 |

| día | backtest original (UTC / UTC+2, dir., entrada, stop) | vídeo (UTC+2, dir., entrada, stop, n.º) | resultado |
|---|---|---|---|
| 08-12 | 05:25:20 / 07:25, compra, 1.15330, 1.15322 | — | solo en el backtest |
| 08-12 | — | 08:36, venta, 1.15354, 1.15361, n.º 1 | solo en el vídeo |
| 08-12 | — | 09:23, venta, 1.15379, 1.15395, n.º 2 | solo en el vídeo |
| 08-12 | — | 10:53, venta, 1.15389, 1.15401, n.º 3 | solo en el vídeo |
| 08-12 | — | 14:20, venta, 1.15436, 1.15459, n.º 5 | solo en el vídeo |
| 08-12 | — | 14:30, venta, 1.15413, 1.15482, n.º 6 | solo en el vídeo |
| 08-13 | 07:33:55 / 09:33, venta, 1.15204, 1.15213 | — (la DUDOSA n.º 7 se cierra a las 09:30:59 desde 1.15205) | solo en el backtest |
| 08-13 | 07:49:40 / 09:49, venta, 1.15247, 1.15263 | — | solo en el backtest |
| 08-13 | — | 11:31, venta, 1.15302, 1.15321, n.º 8 | solo en el vídeo |
| 08-13 | — | 11:43, venta, 1.15318, 1.15328, n.º 9 | solo en el vídeo |
| 08-13 | — | 12:30, venta, 1.15349, 1.15366, n.º 11 | solo en el vídeo |
| 08-14 | 06:30:10 / 08:30, compra, 1.15404, 1.15388 | — (el vídeo no muestra entradas ese día) | solo en el backtest |
| 08-17 | 05:17:15 / 07:17, compra, 1.15842, 1.15828 | 07:30, compra, 1.15842, 1.15828, n.º 12 | **coincide** en entrada y stop; hora 12 min (la del vídeo es el centro de la ventana 07:16–07:53) |
| 08-17 | — | 12:20, compra, 1.15938, —, n.º 13 | solo en el vídeo |
| 08-17 | — | 13:03, compra, 1.15914, 1.15896, n.º 14 | solo en el vídeo |
| 08-18 | (sin caso) | 07:58, compra, 1.15734, 1.15707, n.º 15 | solo en el vídeo |
| 08-18 | (sin caso) | 11:37, venta, 1.15778, → BE, n.º 16 | solo en el vídeo |
| 08-18 | (sin caso) | 12:04, venta, 1.15773, → BE, n.º 17 | solo en el vídeo |
| 08-19 | 09:03:00 / 11:03, compra, 1.15984, 1.15964 | 11:02, compra, 1.15983, 1.15964, n.º 18 | difiere: entrada 1 pt, hora 1 min; stop igual |
| 08-19 | 11:46:15 / 13:46, compra, 1.16030, 1.15997 | — (el audio acaba antes) | solo en el backtest |

Descriptivo: las dos parejas son las dos primeras compras de cada día (17 y 19) y coinciden a 0–1
punto en entrada y en stop; **las once ventas del vídeo no tienen pareja** en el libro, y las ventas
del libro del día 13 (09:33 y 09:49) no tienen pareja en el vídeo. La DUDOSA n.º 7 cierra desde
1.15205 a las 09:30:59, un punto y tres minutos de la fila del libro de las 09:33 (1.15204): si el
consultor la cuenta, sería pareja. El propio trader, a 0:33:32, dice del backtest que envió: «no sé
si yo he estado operando, o sea, lo he tomado con las mechas, o sea, validando el breaker con
mechas, porque como te das cuenta hay muchos trades que han sido ganadores pero solo con el
Breaker, no recuerdo muy bien».

**Recuento conjunto v7 + v8** (v7: `SESION-02-VIDEO.md` §3.2 y §4; v8: esta sección):

| | v7 (3–11 ago) | v8 (12–19 ago, con audio) | conjunto |
|---|---|---|---|
| operaciones leídas en pantalla | 25 | 18 (3 dudosas) | 43 |
| etiqueta `Sell stop` | 21 | 11 | 32 |
| etiqueta `Buy stop` | 3 | 3 | 6 |
| etiqueta `Sell limit` | 1 | 0 | 1 |
| etiqueta `Buy limit` | 0 | 0 | 0 |
| etiqueta no legible | 0 | 4 | 4 |
| **stop frente a limit (legibles)** | 24 / 1 | 14 / 0 | **38 / 1** |
| filas del backtest original en los días vistos | 15 | 7 | 22 |
| parejas (ADR-0043) | 8 | 2 | 10 |
| solo en el vídeo (no dudosas) | 17 | 13 | 30 |
| solo en el backtest | 7 | 5 | 12 |

## 5. Fase 5 · Qué aporta el tramo con audio a cada pregunta

Citas literales de la versión filtrada de v8 (ASR, sin corregir), SOLO de 0:00:00 a 0:40:00. Del
tramo sin audio no hay nada: ni cita ni pantalla, porque no se abrió ningún fotograma. Las
opciones son las de `SESION-02-EXTRACCION.md`; nada se elige.

### A-21 · qué es una zona de control limpia (`solo_una_zona_de_control` · `sin_mecha_mas_alla_del_extremo`)

Es la pregunta sobre la que v8 más habla, y con una frase que va directa al título:

- 0:39:53 «Vale, aquí es muy importante, **la zona de control no necesariamente se va a desarrollar
  limpia, tiene que romper allí**.» (última frase con audio; fotograma 002399000, n.º 18 recién
  abierta).
- 0:02:09 «Bueno, aquí no hay operativa porque ya se rompe el esquema como tal, demasiado ruido.»
- 0:12:55–0:13:07 «sería la primera, segunda, la segunda / como en anteriores ejemplos hemos visto /
  tendría que dar el equal para poder / tomar la operativa / en este caso no lo tomamos esto / Si
  hubiera estado, esta vela bajista aquí, hubiera llevado algún cuerpo con mecha tomando aquí, se
  hubiera tomado. Entonces, ese flujo estaría escrito así. Aquí no hay entrada por el hecho de que,
  vamos, nos hace esto aquí. Entonces, no es igual al segundo esquema de entrada. Entonces, no lo
  queramos.»
- 0:16:00–0:16:19 «porque como digo, vela 1, vela 2 / deberían de darnos el equal, hay una tercera
  vela / donde se genera el equal / como este ejemplo aquí / está aquí, entonces / no hay entrada, o
  sea suele haber a veces / variaciones en el precio, que uno se da cuenta / pero no es eso, o sea /
  cuando uno hace el mapeo / pues no se toma en cuenta».
- 0:19:18–0:19:25 «porque no cumple ninguno de los dos esquemas / que tampoco se toma».
- 0:23:36–0:24:16 «este trade aquí no lo tomaríamos porque / porque necesitamos más desarrollo de
  precio o sea para poder validar sería que rompa este / de esta zona a esta zona de aquí / para
  luego validar / el punto / el posible punto / el breaker o el posible punto de entrada».
- 0:25:15–0:25:20 «no hay entrada hasta aquí / no genera ningún esquema / no rompe el esquema / no
  dan ni el primer esquema ni el segundo esquema, entonces no hay entrada.»
- 0:33:11–0:33:25 «a ver, lo principal / tendencia al respetar / los dos, o sea, muy importante
  respetar / los dos esquemas de / cómo se arman los dos esquemas de entrada / la mitigación / de
  liquidez, que por debajo no se toma ninguno / si no empieza por arriba y todo ese flujo por debajo
  si llega a romperse pues se toma ahora».
- 0:36:41–0:37:39 «aquí desarrollas una control que no podía poner el b y el presionado retroceder no
  sé qué va a / hacer después pero está aquí aquí la entrada no entra porque no cumple con rompe por
  aquí / por encima nos tendrá un igual a favor de la operativa pero qué pasa lo que nos genera /
  esto aquí entonces linealmente si lo vemos no coincide con el esquema de entrada no se / se tome, a
  pesar de que sea ganador, no sé.»
- Pantalla, lo que pedía el brief de v7 y se repite: caja 0/0,25/0,5/0,8/1 en M1 sobre el bloque
  contrario (n.º 1: 0=1.15354, 1=1.15362, fotograma 000200000; n.º 2: 000250000), orden stop en el 0,
  stop en el 0,8, y la línea azul de M15 por encima (ventas) ya rota.
- **Posible lectura nueva**, la misma que en v7 y ahora dicha con más palabras: lo que valida o
  invalida es el ESQUEMA (el «equal» de la primera y segunda vela, «no cumple ninguno de los dos
  esquemas», «demasiado ruido») y no un atributo de limpieza de la zona; y 0:39:53 dice literalmente
  que la zona de control «no necesariamente se va a desarrollar limpia». Lo decide el consultor.

### Los «equals» (fuera de las dos opciones documentadas; ya señalado en v7)

- 0:18:01–0:18:24 «notar este igual aquí estaría validado porque cumple primera segunda en la segunda
  pues ésta / sí / y salto que hay un pequeño y por primera y segunda entonces / saca los iguales
  marcamos aquí todavía se mantiene aquí».
- 0:28:18–0:28:47 «vamos aquí, tenemos ese equal / que en este caso bajista, que a nosotros / nos
  habilita para poder, o sea, avaliarlo como un punto / de posible breaker y entrada, vale, este se
  desarrolla / el esquema 2, o sea, visualmente quedaría algo así».
- 0:39:24–0:39:33 «el breaker con cuerpo como tenemos el igual aquí entonces lo es lo que lo óptimo /
  es tomarlo aquí respetando las reglas aquí pero si no hubiera ese aquí pues sería tomarlo aquí».
- Es un mecanismo que ninguna ambigüedad nombra («equal»: dos velas cuyo extremo coincide, que
  «habilita» el punto de breaker). **Posible lectura nueva.**

### A-45 y A-32 · cuerpo frente a mecha

- 0:03:53 «vale, en este caso no hay entrada porque nos rompe con mecha».
- 0:13:07 «Si hubiera estado, esta vela bajista aquí, hubiera llevado algún cuerpo con mecha
  tomando aquí, se hubiera tomado.»
- 0:33:32–0:34:01 «mira quiero mencionar algo porque no sé de verdad o sea en el backtest que te he
  enviado bueno eso / ya lo vemos al final claro que todavía nos quedan un par de días más para ver
  porque no sé si yo / he estado operando o sea lo he tomado con las mechas o sea baleando el breaker
  con mechas / porque como te das cuenta / hay muchos trades que han sido ganadores / pero solo con
  el Breaker / no recuerdo muy bien la verdad / no recuerdo muy bien / al final vamos a ver».
- 0:35:53–0:35:55 «Vale, rompimiento de… / de m 15 por encima un cuerpo y esquema de entrada».
- 0:39:11–0:39:24 «ahora aquí en ese caso así que lo hace y lo hace con cuerpo muy / importante el
  breaker con cuerpo».
- Lo de 0:33:32 es material para §4 y para la fidelidad: el trader duda de si en su backtest
  original validó breakers con mecha.

### A-34 · vela H4 previa (lectura libre) y el sesgo

- 0:01:15–0:01:28 «Aquí bajista, alcista, alcista, alcista, y aquí está el breaker, entonces bajista.
  / O sea, al final nos termina cerrando por debajo con mecha, vela bajista, / entonces en la
  siguiente operativa nos enfocamos a la escena bajista.»
- 0:06:37–0:06:56 «Vale, todavía seguimos buscando operativas bajistas / a pesar de que esta vela sea
  aquí verde, / ¿por qué bajista? / porque como bien decía con anterioridad también y lo solía repetir
  nosotros buscamos que el precio / al menos se establezca por encima finalizando alcista o sea verde
  para poder en esta sección / buscar operativas alcistas como no lo hizo seguimos buscando
  operativas bajistas».
- 0:15:16–0:15:23 «vale, bajista / continuamos bajistas / vela roja por debajo, cierre por debajo /
  con mecha».
- 0:20:02 «El enfoque es alcista, alcista porque desde aquí hasta aquí está planteado el rango, no
  llega a romper esta tabla roja por debajo para poder validarlo, o sea, con operativo bajistas, las
  siguientes, entonces, nada, nos encontramos en un rango alcista».
- 0:34:21–0:34:27 «es bajista porque / porque el precio no nos llega a romper por encima de manera
  alcista, / entonces estamos en un rango bajista.»
- 0:38:09–0:38:17 «esta es la intuición, el breaker, / aquí, operativo alcista, / enfoca alcista».
- Misma lectura que en v7 (el sesgo se mantiene hasta que una vela «termina» más allá, «con mecha»
  cuenta); no toca la vela que rompe ambos extremos.

### A-13 y A-40 · el break even

- 0:02:55 «Para poner el break-even necesitamos, cuando aquí se desarrolla, se llega a desarrollar
  lo que sería la zona control, entonces aquí ya podemos proteger la entrada, nos sacan B, tenemos
  otro B».
- 0:17:22 «30 protegemos al menos desarrollar el control».
- 0:24:37 «aquí voy a proteger a B».
- 0:27:10–0:28:14 «Vamos a ver, no sé si me llevo a cerrar, pero sí, me llevo a sacar. / ¿Me llevo a
  sacar o no me llevo a sacar? / Yo creo que sí, sí, esto está en B. / Aquí no, no sé, lo voy a
  trazar hasta aquí. / Vale, esto está en B porque cumple. / ya está aquí / nos habilita para poner
  un break en la entrada» (fotogramas 001610000–001640000, n.º 13).
- 0:29:01–0:29:22 «vale, protegemos / protegemos a B / pero antes se va a calcular / 18 / 24 / 5, 4,
  5, 4 / el precio nos saca / nos saca en B».
- 0:36:41 «aquí desarrollas una control que no podía poner el b».
- Pantalla: «Stop loss moved to 1.15778» (002125000) y «… to 1.15773» (002205000): el stop va al
  precio de entrada y no se ve ningún movimiento posterior (A-40).

### A-30 · la orden o la posición al llegar el fin de la ventana

- 0:05:54–0:06:20 «en la vela de cierre cerramos la operación se lo cuenta como ganada pero yo no lo
  contaría / porque tampoco es que llegue al uno o sea al objetivo final entonces pero bueno para /
  para que esté allí y eso lo cierro allí. / Aprendo un backtesting, / los backtesting que yo hago no
  lo suelo complementar / porque afecta, o sea, está ahí, siga. / Mostró los datos como tal, /
  entonces lo dejo allí ahora.» (n.º 3: cerrada a mano a las 11:00:59 con +11, fotograma 000355000).
- 0:22:47–0:23:06 «si luego se / decide operar la siguiente sesión es lo mismo se hace sigue la misma
  lógica de vale tomás como / vayas en la vela anterior en h4 y pues aquí por aquí estaría la
  entrada 2 m1 y llegas a adoptarlo / aquí aquí estaría la entrada para esa sesión pero como sólo
  estamos trabajando con estas dos / dos sesiones entonces no no lo tomo».
- Con v7 (1:06:26–1:08:01) son ya dos tramos sobre el cierre al fin de la sesión.

### A-29, A-36 y A-38 · la orden stop en el punto de breaker, y su actualización

- Pantalla: n.º 5 (orden movida 1.15398 → 1.15412 → 1.15436 en 26 minutos, fotogramas
  000500000–000540000); n.º 2 («Entry price moved to 1.15379», 000250000); menús contextuales con
  «Sell … stop» elegido frente a «Buy … limit» (002180000, 002375000).
- 0:26:21–0:26:46 «Vale, el trade estaría aquí. / Como hemos visto con anterioridad, o sea, a bajista
  alcista en este caso, / tenemos que una sola vela se desarrolla pues el es el flujo de la
  continuidad del flujo de órdenes / en la cual nosotros o sea esta vela termina será por debajo y
  por encima y una mitad por / debajo y por encima y termina el sistema entonces sólo en esta vela se
  podría atrasar y se podría / Podría trazar, se podría poner el límite, en este caso el sistema.»
  (la vela envolvente de M1 como bloque, igual que en v7, A-37).
- **Posible lectura nueva**, la de v7: orden STOP en el punto de breaker candidato, movida a cada
  actualización.

### A-25 y A-24 · las líneas de M15

- 0:01:55–0:02:02 «Vale, ya tenemos trazadas las zonas de liquidez que esperamos, / o sea, siempre
  por arriba, por debajo, lo que sea por debajo de la zona de líneas de liquidez, / no nos importa, de
  M15, sino todo lo que sea por arriba y tratar de buscar un [breaker] de flow.»
- 0:29:52–0:30:26 «no lo tomamos, y ahora continuamos con la siguiente sesión, luego de H4, a ver la
  direccionalidad, en este caso bajista, claramente, entonces trazo mis zonas de liquidez en M15, /
  como he hecho este breaker, pues no nos importa, es con breaker, este no nos interesa, entonces lo
  dejamos allí».
- 0:34:30–0:34:36 «Ahora nos vamos a M15, / marcamos las zonas para que trabajemos.»
- No dice cuándo muere una marca ni por qué elige un pivote y no otro.

### A-18 · el 1:3

- Solo cifras sueltas al calcular la caja: 0:17:04 «vamos a ir arriba 10 a 30»; 0:24:35 «14, 30, 40»;
  0:29:07–0:29:16 «18 / 24 / 5, 4, 5, 4»; 0:35:18 «25, vale, me saco en P»; 0:37:47 «contamos con el
  3». Pantalla: n.º 1 TP movido a 1.15323 (31 puntos, caja de 8: 3,9× la caja o 4,4× el stop de 7);
  n.º 2 stop 16 / objetivo 48 (3,0×); n.º 5 stop 23 / objetivo 66 (2,9×); n.º 18 stop 19 / objetivo
  53 (2,8×). No repite la explicación de v7 sobre «desde el punto 1» y «recalcular a 0,80».

### A-42 y A-43 · el reloj y las sesiones

- 0:00:03–0:00:07 «Nos quedamos en esta sesión de aquí, / nuevamente ahora vamos a marcar / para
  poder separar las distintas sesiones.» y 0:22:47–0:23:06 (arriba): solo se operan «estas dos
  sesiones». Pantalla: reloj `UTC+2`, sombreados en 07:00, 11:00 y 15:00.
- A-43: las líneas de M15 se trazan sobre pivotes de la noche (001450000, 07:01:59 del día 17, líneas
  sobre las 05:00–06:00). No lo dice en voz.

### Lo que NO toca

A-35 (en M15), A-44, A-46, A-26 (el conflicto), A-33 (parciales), A-31, A-39, A-41 (el día 12
lleva 6 órdenes, 3 por sesión, sin comentario), doji, vela que vuelve a su color, antigüedad
máxima del pivote. Del tamaño del retroceso, solo 0:23:36–0:24:16 («necesitamos más desarrollo de
precio»), sin cifra.

## 6. Lo que se perdió, y cómo se trató

- **Perdido**: el audio de 0:40:00 a 2:00:48 (80 min, dos tercios de la grabación). En ese tramo el
  trader siguió backtesteando desde el 19 de agosto a las 11:13 en adelante (v7 dice «hasta el 30»).
  Lo que dijo ahí no existe en ningún sitio: ni en el corpus ni en la carpeta del rescate
  (`audio-completo.m4a` es el audio del rescate, con el mismo corte).
- **Cómo se trató**: el vídeo entra ENTERO (los 7249 fotogramas están en disco y en el manifiesto,
  como manda F05: cobertura completa), la transcripción cubre solo lo que hay, y **ningún fotograma
  posterior a 0:40:00 se abrió**, porque no había `marcas-v8.txt` y la regla del brief es «sin marcas,
  ninguno». Las operaciones del 19 (desde las 11:13) al final de la sesión quedan sin leer. Si Aleks
  escribe `marcas-v8.txt` con instantes localizados a mano, se abren SOLO esos, en una tarea nueva;
  el manifiesto y la transcripción no cambian.
- **Riesgo que esto deja**: la comparación de §4 para el 19 de agosto es parcial (una de las dos
  filas del libro cae después del corte), y los días 20–31 no tienen ninguna lectura de pantalla.

## 7. Exposiciones, declaradas hoy

Fila añadida a `docs/validation/HOLDOUT-EXPOSICIONES.md` (mismo commit). Resumen: 74 fotogramas de v8
abiertos por instante localizado, todos antes de 0:40:00; el saldo de la cuenta de replay en ellos
(de 99 898,00 $ a 100 077,00 $, con las etiquetas en USD de cada orden); ningún fotograma de
Analytics (el trader no la abre en los 40 minutos con audio, y no se leyó ninguna cifra agregada
en voz); ningún fotograma del tramo sin audio; el libro de agosto no se abrió. Agosto no tiene
ningún día reservado (medido antes de abrir nada). Nada se usa.

## 8. Commits y sello

- `9725e0c` · `data(corpus)`: fuentes, inventario, fotogramas, transcripción y el test v1..v8. `make
  check` en verde: 1288 tests, 4 contratos, sello escrito.
- `<informe>` · `docs(validation)`: este informe y la fila de exposiciones. `make check` en verde
  antes del commit.
- No hay commit de tramos no citables: la cuarentena dio 0 bloques y el ASR no alucinó en el
  silencio (§2).

## 9. Riesgos y dudas para el consultor

1. **Tres DUDOSAS con saldo que se mueve** (n.º 4, 7 y 10): el trader dice que no se toman o la
   pantalla no da la entrada, pero el saldo baja 30, 32 y 14 $. Puede ser que la orden se llenara
   antes de que la quitara. Se anotan y no se comparan; si el consultor las cuenta, la n.º 7 sería
   pareja de la fila del libro de las 09:33 del día 13.
2. **Legibilidad**: la vista de Discord (desde 0:19:25) reescala la pantalla y las etiquetas de
   USD se leen peor; en las n.º 8, 13 y 15 la etiqueta de la orden no se ve, y en la 15 la dirección
   se dedujo del stop. Precios a ±1 punto como en v7.
3. **El replay se rebobina** (n.º 5 → n.º 6, y 13 Aug entre las 14:44 y las 11:16): una misma hora de
   mercado puede aparecer dos veces con órdenes distintas. La tabla lista las dos versiones y lo
   dice; el consultor decide cuál cuenta.
4. **Once ventas sin pareja en el libro y dos compras que sí casan**: no se explica aquí. El propio
   trader duda (0:33:32) de si en el libro validó breakers con mecha.
5. **v8 continúa la sesión de replay de v7**: el saldo enlaza (100 042,00 $). Las cifras de saldo son
   agregados de la propia grabación y no se usan.
6. **El tramo sin audio** (§6) y los días 20–31 de agosto: sin lectura. `marcas-v8.txt` es la única
   vía para abrirlos sin muestreo.

## 10. Estado

Rama lista para revisión, NO cerrada.

## 11. Decisiones del consultor (2026-09-27)

Tomadas tras revisar este informe, rama `trabajo/sesion-02`. No cambian ninguna cifra de §3 ni de §4.

a) **Las DUDOSAS n.º 4, 7 y 10 quedan fuera de la métrica principal de ADR-0043** y se reportan
   aparte, como sensibilidad. La n.º 7 también, aunque sería pareja de la fila del libro de las
   09:33 del día 13: pesa más la palabra del trader («no se toman») que una coincidencia de hora.
   Las cifras de §4 no cambian.

b) **Cuando el replay se rebobina, se conservan las dos versiones de la misma hora de mercado**,
   como ya hace la tabla de §3.2 (n.º 5 y n.º 6).

c) **Las once ventas sin pareja NO se tratan como error de cruce.** El huso (UTC → UTC+2) está
   confirmado por las dos parejas a 0–1 punto, y el libro tiene ventas propias el día 13. Se leen
   como una nueva pasada del trader sobre los mismos días. Se anota como **riesgo de fidelidad**: el
   libro de referencia no es del todo reproducible por el propio trader (0:33:32). No se abre
   sesión de diagnóstico.
