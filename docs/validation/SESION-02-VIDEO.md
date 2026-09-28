# Sesión 02 con el trader: el vídeo v7, la primera mitad de agosto en directo

Rama `trabajo/sesion-02`, 2026-09-27, tarea autónoma sobre `main` en `stable/F25-preparar-a21`.
Sin merge, sin tag, sin push. **Nada se resuelve aquí**: ni un ítem de evidencia, ni un registro de
feedback, ni un cambio en `ambiguedades.yaml`, `parametros.yaml` o `strategy_spec.yaml`. Es material
para el consultor.

## 0. Lo que la medida contradice del brief, dicho primero

1. **No es la segunda mitad de agosto: es la PRIMERA.** El brief decía que el trader hacía
   backtesting de la segunda mitad. Medido en pantalla (§3): la sesión de FX Replay arranca con el
   cursor en el lunes 3 de agosto de 2026 (fotograma 0:00:40, eje `Mon 03 Aug '26`), recorre el 3, 4,
   5, 6, 7, 10 y 11 de agosto, y para el martes 11 a las 15:00 (fotograma 1:12:10). El trader lo dice
   en voz: «dejado esta sesión de aquí del día 04 de agosto» (0:33:02) y «me faltaría todavía, claro,
   15 días creo, ¿no? hasta el 30» (1:12:19–1:12:21). **Siete días, todos de DESARROLLO** (§3.1).
2. **No es una sesión de preguntas con código.** El filtro de `scripts/transcribir_sesion.py`
   detecta **0 segmentos** que abran una pregunta («pregunta A-NN») y 0 «fin de pregunta» en los 602
   segmentos de la cruda (medido con `codigo_en` y `fin_de_pregunta`, sin leer el texto, 32 códigos
   válidos). El trader backtestea en voz alta y Aleks interviene poco; las preguntas de la hoja no
   se recorren por código. Por eso la Fase 5 se hace por lectura completa de la versión filtrada, no
   por tramos de pregunta.
3. **Las órdenes que coloca en FX Replay son STOP, no límite.** Las etiquetas de la plataforma dicen
   `Sell stop` en 21 de las 25 órdenes vistas, `Buy stop` en 3 y `Sell limit` en 1 (§3.2). Él las
   llama «orden límite» / «order limit» en voz. Es una lectura descriptiva de la pantalla, no una
   corrección de la spec: se lleva al consultor (§5, A-29 y A-36).

## 1. Fase 1 · Ingesta con la convención de v1-v6

Cómo entró v6 (la sesión 01): tres commits, `2df4e56` (entrada en `fuentes.yaml` + `manifest.yaml`
regenerado), `205881e` (manifiesto de fotogramas) y `99290d0` (manifiesto de transcripción). v7 entra
igual, con el siguiente id libre (`v7`; no existía en `knowledge/`, `src/`, `tests/` ni `docs/`):

| pieza | id / fichero | commit |
|---|---|---|
| fuente | `knowledge/corpus/fuentes.yaml`, `video_id: v7`, sin `drive_id` (nace en local, ADR-0011), `naturaleza: sesion 2 ...` (la guardia de `inventario.py` exige que empiece por «sesion» si no hay `drive_id`) | `cebc887` |
| inventario | `knowledge/corpus/manifest.yaml` regenerado por `botsito corpus inventory`: 7 vídeos, sha256 `6cdca768…`, 4413,1 s, 1920×1080, 30 fps, audio | `cebc887` |
| fotogramas | `knowledge/corpus/fotogramas/fr-v7-40427216.yaml`: 4414 PNG a 1 fps en `data/fotogramas/v7/png-1fps/`, cobertura completa, 0 huecos, 0 obligatorios extra (3,5 min) | `7b60b06` |
| transcripción | `knowledge/corpus/transcripciones/tr-v7-large-v3-int8-float16-87297562.yaml`: 602 segmentos en 8 fragmentos; texto en `data/transcripciones/v7/large-v3-int8-float16/` (fuera de git) | `7b60b06` |
| test | `tests/unit/test_inventario.py::test_fuentes_y_manifiesto_reales_coherentes` congela la lista de vídeos: pasa de `v1..v6` a `v1..v7` | `cebc887` |

Fotogramas y transcripción van en un solo commit (v6 los llevó en dos): salieron de la misma tanda y
ninguno se había leído todavía.

**El nombre del fichero.** La convención OBLIGA a guardar el nombre original: `fuentes.yaml`
(`fichero:`), `manifest.yaml` (`fichero:`) y los dos manifiestos (`fichero_video:`) lo llevan, igual
que v6. El nombre trae la fecha de grabación, un domingo de septiembre. Antes de commitear se
comprobó si alguna guardia lo rechaza: **ninguna revisa fechas en texto commiteado**. Las que
existen (`tests/contract/test_ingesta_fidelidad.py`, `test_ensayo_marzo.py`, `test_cobertura.py`,
`tests/unit/test_huso_por_velas.py`) vigilan que las SALIDAS de la CLI no nombren un día reservado, y
`casos_reservados`/`casos_ocultos` no pueden contener un domingo. No chocó, así que no se renombró
nada; el vídeo original no se ha movido ni borrado. Fuera de esos cuatro sitios generados, la fecha no
se escribe en ningún otro texto de esta rama (este informe la evita).

**Lo que se hizo al vídeo**: nada. Sigue en `corpus/Estrategia del trader/` con su nombre.

## 2. Fase 2 · Transcripción y cuarentena, ANTES de leer nada

- **ASR**: el del corpus (F04, ADR-0007), por `botsito corpus transcribe --video v7`: faster-whisper
  `large-v3`, `int8_float16`, CUDA, `beam_size=5`, `temperature=0`, `vad_filter`,
  `condition_on_previous_text=False`, el vocabulario de `knowledge/corpus/glosario_asr.yaml` como
  `initial_prompt`, el mismo corte por silencios. 12,5 min para 73,5 min de vídeo. El comando no
  imprime texto (solo recuentos por fragmento).
- **Cuarentena**: `scratchpad/cuarentena_v7.py` (fuera del repo) importa `en_cuarentena` de
  `scripts/transcribir_sesion.py` —el mismo código, sin duplicarlo— y lo aplica a
  `data/transcripciones/v7/.../cruda.jsonl` antes de que nadie la lea. Escribe fuera del repo la
  versión filtrada (lo ÚNICO que se ha leído), el bloque de tramos y un registro sin contenido.
- **Resultado**: 602 segmentos; **3 en cuarentena, en 1 bloque: `0:15:34–0:15:48`** (segmentos
  128–130 de la cruda; motivos: 1 «fecha numérica», 2 «vecino»); 13 s de 3678 s de habla (0,3 %).
  Ni un «mes» ni un «backtest con mes»: el trader habla de agosto y enero, que no se filtran.
- **Registro en el repositorio**: `knowledge/corpus/tramos_no_citables.yaml` gana el tramo de v7
  (commit `3718889`), con `motivo` y `acordado` SIN contenido. Desde ese commit, `evidence propose
  --check` y `evidence new` rechazan cualquier cita que lo solape (`tramo_no_citable`).
- **Lo que NO se ha hecho**: leer, escuchar ni reconstruir el bloque. `botsito corpus frames show`
  imprime el segmento crudo más cercano al instante pedido; por eso solo se usó una vez (en 0:00:40,
  fuera del bloque) y las rutas de los PNG se calcularon a mano (`<ms>.png`).

## 3. Fase 3 · Qué días y qué operaciones

**Reloj.** El gráfico de FX Replay marca `UTC+2` en la esquina inferior derecha en todos los
fotogramas abiertos (ej. `07:47:59 UTC+2`, 0:03:47). Toda hora de esta sección es **UTC+2 de
pantalla** (en agosto coincide con Europe/Madrid). El trader configura el huso al arrancar: «lo
primero que hago es configurar la zona horaria que sería en este caso pues UTC Madrid ya que me ubico
en España» (0:00:01).

**Cómo se abrió cada fotograma**: por instante localizado en la versión filtrada (ADR-0038), en los
tramos donde el trader dice que coloca, activa, protege o cierra una entrada, o que cambia de día o
de sesión; y su vecindario inmediato. **Cero muestreo.** Se abrieron **81 PNG** (lista en §3.3).
**No se abrió ningún fotograma** de los cuatro tramos en que la transcripción dice que va a la
pestaña Analytics (§6).

### 3.1 Los días, comprobados ANTES de escribirlos

`casos_reservados(repo)` y `casos_ocultos(repo)` (medido el 2026-09-27, antes de abrir ningún
fotograma): 34 casos ocultos —mayo 13, junio 11, septiembre 10, uno retirado— y **ninguno de
`2026-08`**. Los 21 días de agosto son `dev` en `knowledge/cases/visto/2026-08/particiones.yaml`.
`scratchpad/comparar_v7.py` lo vuelve a comprobar por día antes de leer ningún caso.

| día (pantalla) | sesiones vistas | operaciones vistas | fotograma que fija el día |
|---|---|---|---|
| lunes 2026-08-03 | 07-11 y 11-15 | 9 (n.º 1–9) | 000227000 (`Mon 03 Aug '26`, 07:47:59) |
| martes 2026-08-04 | 07-11 y 11-15 | 3 (10–12) | 001740000 (`Tue 04 Aug '26`, 08:29:59) |
| miércoles 2026-08-05 | 07-11 y 11-15 | 1 (13) | 002455000 (`Wed 05 Aug '26`, 14:49:59) |
| jueves 2026-08-06 | 07-11 y 11-15 | 5 (14–18) | 002654000 (`Thu 06 Aug '26`, 08:07:59) |
| viernes 2026-08-07 | 07-11 y 11-15 | 3 (19–21) | 003470000 (`Fri 07 Aug '26`, 11:57:59) |
| lunes 2026-08-10 | 07-11 y 11-15 | 2 (22–23; la 23 «no se toma», simulada) | 003920000 (`Mon 10 Aug '26`, 14:04:59) |
| martes 2026-08-11 | 07-11 y 11-15 | 2 (24–25; la 25 sin llenado visto) | 004280000 (`Tue 11 Aug '26`, 13:21:59) |

### 3.2 La tabla por operación

Lo que se lee en pantalla: las etiquetas de precio de la orden (`Sell stop`/`Buy stop`/`Sell limit`
a un precio), la línea de stop (etiqueta en USD negativa) y la de objetivo (etiqueta positiva o
`TP`), y los avisos de la plataforma («Stop order executed on EURUSD: Sell 100000 at 1.15358»,
«Position Updated: Stop loss moved to …», «Closed your open position …»). **La hora es la del
llenado cuando hay aviso o posición abierta en el fotograma; si no, la ventana entre la orden y el
primer fotograma que la muestra llena o cerrada, y se dice.** Un guion es «no legible en los
fotogramas abiertos». Los precios son de etiqueta (legibles a ±1 punto por la compresión del vídeo).

| n.º | día | hora UTC+2 | dir. | entrada | stop | objetivo | minuto v7 | fotogramas | cómo se fijó |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 08-03 | 07:48 | venta | 1.15358 | 1.15368 | 1.15322 | 0:03:47–0:05:30 | 000227000, 000263000, 000271000, 000330000 | aviso «Sell … at 1.15358» a las 07:48:59; cerrada a saldo 100 000 (BE) a las 07:58:59 |
| 2 | 08-03 | 08:01–08:04 | venta | 1.15364 | 1.15377 | — | 0:06:44–0:08:00 | 000404000, 000450000, 000480000 | orden 08:00:59; saldo −17 a las 08:04:59 |
| 3 | 08-03 | 08:07–08:11 | venta | 1.15362 | 1.15383 | — | 0:08:19–0:10:20 | 000499000, 000510000, 000565000, 000620000 | abierta (−2) a las 08:11:59; stop primero en el nivel 1 (1.15389) y luego en 0,8 (1.15383); BE |
| 4 | 08-03 | ≥09:34 | venta | 1.15306 | 1.15322 | — | 0:11:00–0:11:50 | 000660000, 000700000, 000710000 | orden a las 09:33:59; llenado no visto (el tramo siguiente va a Analytics y no se abre) |
| 5 | 08-03 | 11:46 | venta | 1.15274 | 1.15287 | — | 0:15:55–0:16:17 | 000955000, 000977000 | abierta (−7) a las 11:46:59; aviso «Closed … Sell 100000 at 1.15274» a las 11:48:59 |
| 6 | 08-03 | 13:05–13:12 | venta | 1.15253 | — | — | 0:18:00–0:18:40 | 001080000, 001120000 | etiqueta **`Sell limit`** a las 13:04:59; saldo −7 a las 13:12:59 |
| 7 | 08-03 | 13:12–13:15 | venta | 1.15256 | 1.15266 | 1.15219 | 0:20:10–0:21:10 | 001210000, 001240000, 001270000 | orden 13:11:59; «Stop loss moved to 1.15256» a las 13:15:59; BE |
| 8 | 08-03 | 14:03–14:09 | venta | 1.15320 | 1.15344 | 1.15264 | 0:22:45–0:24:05 | 001365000, 001415000, 001445000 | orden 14:02:59; saldo −24 a las 14:09:59 |
| 9 | 08-03 | 14:10–14:24 | venta | 1.15338 | 1.15352 | 1.15296 | 0:25:10–0:25:35 | 001510000, 001535000 | orden 14:09:59; saldo +42 a las 14:24:59 |
| 10 | 08-04 | ≤09:44 | venta | 1.15129 | 1.15163 | — | 0:32:10–0:32:42 | 001930000, 001962000 | abierta (+28) a las 09:44:59; cerrada a saldo previo (BE) a las 10:06:59 |
| 11 | 08-04 | 13:33–13:39 | venta | 1.15184 | 1.15210 | 1.15123 | 0:34:30–0:35:10 | 002070000, 002110000 | orden 13:32:59; abierta (−21) a las 13:39:59 |
| 12 | 08-04 | ≤13:56 | venta | 1.15174 | 1.15222 | — | 0:36:20 | 002180000 | abierta (−12) a las 13:56:59 |
| 13 | 08-05 | 14:49 | compra | 1.15488 | 1.15472 | — | 0:40:25–0:41:00 | 002425000, 002445000, 002450000, 002455000, 002460000 | aviso «Buy 100000 at 1.15488» a las 14:49:59 (`Buy stop` 1.15488, stop 1.15473→1.15472); saldo −16 a las 14:54:59 |
| 14 | 08-06 | 07:55–08:01 | venta | 1.15499 | 1.15505 | 1.15482 | 0:43:10–0:43:40 | 002590000, 002620000 | orden 07:54:59; saldo −6 a las 08:01:59 |
| 15 | 08-06 | 08:07 | venta | 1.15491 | 1.15516 | 1.15417 | 0:43:40–0:46:30 | 002620000, 002654000, 002790000 | aviso «Sell 100000 at 1.15491» a las 08:07:59; saldo +76 a las 09:55:59 |
| 16 | 08-06 | 12:33–12:39 | venta | 1.15420 | 1.15428 | 1.15399 | 0:50:25–0:51:00 | 003025000, 003030000, 003060000 | orden 12:32:59; «Stop loss moved to 1.15421» a las 12:39:59; BE |
| 17 | 08-06 | 13:08–13:28 | venta | 1.15428 | 1.15444 | — | 0:51:35–0:53:20 | 003095000, 003200000 | orden 13:07:59; saldo −23 a las 13:28:59 |
| 18 | 08-06 | 13:29–13:39 | venta | 1.15454 | 1.15469 | 1.15422 | 0:53:20–0:53:55 | 003200000, 003235000 | orden 13:28:59; saldo +45 a las 13:39:59 |
| 19 | 08-07 | 11:58–12:10 | venta | 1.15293 | 1.15312 | 1.15248→1.15220 | 0:57:50–0:58:35 | 003470000, 003500000, 003515000 | orden 11:57:59; abierta (+13) a las 12:10:59 con el objetivo movido a 1.15220; a las 13:50:59 saldo igual al previo |
| 20 | 08-07 | 13:55–13:57 | venta | 1.15314 | 1.15330 | 1.15278 | 0:59:20–0:59:30 | 003560000, 003570000 | orden 13:54:59; abierta (−11) a las 13:57:59; saldo −3 después («6-6… sería un B», 0:59:59) |
| 21 | 08-07 | 14:05–14:31 | venta | 1.15345 | 1.15365 | 1.15281 | 1:00:10–1:00:40 | 003610000, 003640000 | orden `Sell stop` 1.15346 a las 14:04:59; avisos «Sell … at 1.15345» y «Closed … at 1.15345» vistos a las 14:31:59 |
| 22 | 08-10 | 13:54–14:04 | compra | 1.15503 | — (al entrar, BE) | 1.15542 | 1:05:00–1:05:50 | 003900000, 003920000, 003950000 | `Buy stop` 1.15544 a las 13:53:59; a las 14:04:59 posición de compra desde 1.15503 con «0.00 USD» en la entrada y +39 en 1.15542; saldo +39 a las 14:13:59 |
| 23 | 08-10 | 14:50–14:59 | compra | 1.15476 | 1.15450 | — | 1:06:26–1:08:01 | 003990000, 004025000 | «ya no se toma porque quedó un par de 10 minutos» (1:06:26); la simula: abierta (−6) a las 14:59:59 y cerrada al fin de sesión (saldo −6 a las 06:59:59 del 11) |
| 24 | 08-11 | 13:06–13:21 | venta | 1.15410 | — (al entrar, BE) | 1.15332 | 1:10:40–1:11:20 | 004240000, 004280000 | orden 13:05:59; «Stop loss moved to 1.15410» a las 13:21:59 (+24 abierto); saldo previo a las 14:50:59 (BE) |
| 25 | 08-11 | (orden 14:50) | venta | 1.15399 | 1.15419 | 1.15360 | 1:11:50–1:12:10 | 004310000, 004330000 | `Sell stop` colocada a las 14:50:59; el vídeo acaba a las 15:00:59 con el saldo sin cambio: **llenado no visto** |

Tres cosas legibles en la tabla que van al consultor sin interpretarlas: (a) el tipo de orden
(§0.3); (b) la relación objetivo/stop en las 15 operaciones con los tres precios legibles va de 1,95
(n.º 25) a 3,7 (n.º 7), y el trader dice en voz que el «primer cálculo es de 1:3 normal, o sea desde
el punto 1, y luego se recalcula obviamente a 0,80» (0:06:07–0:06:15): material de A-18, §5; (c) el
stop cambia de nivel dentro de la misma operación (n.º 3: 1.15389 → 1.15383; n.º 19: objetivo
1.15248 → 1.15220).

**Lo que no cuadra y se deja dicho**: los saldos de pantalla no siempre cuadran con las etiquetas
de stop (n.º 2: stop a 13 puntos y saldo −17; n.º 21: stop a 20 y saldo −52). No se ha intentado
reconstruir el lotaje de cada orden. El resultado (win/loss/BE) NO es dato de esta rama: se anota
solo donde un aviso o el saldo lo dice, y nunca se usa.

### 3.3 Fotogramas abiertos (81)

`data/fotogramas/v7/png-1fps/`: 000040000, 000227000, 000263000, 000271000, 000330000, 000404000,
000450000, 000480000, 000499000, 000510000, 000565000, 000620000, 000660000, 000700000, 000710000,
000955000, 000977000, 001080000, 001120000, 001210000, 001240000, 001270000, 001365000, 001415000,
001445000, 001510000, 001535000, 001670000, 001719000, 001740000, 001801000, 001930000, 001962000,
002010000, 002070000, 002110000, 002180000, 002320000, 002425000, 002430000, 002445000, 002450000,
002455000, 002460000, 002480000, 002505000, 002590000, 002620000, 002654000, 002790000, 002810000,
003025000, 003030000, 003060000, 003095000, 003200000, 003235000, 003330000, 003395000, 003430000,
003470000, 003500000, 003515000, 003560000, 003570000, 003610000, 003640000, 003765000, 003790000,
003840000, 003900000, 003920000, 003950000, 003990000, 004025000, 004110000, 004150000, 004240000,
004280000, 004310000, 004330000. Ninguno es una captura de Analytics; el único agregado visto en ellos
es el saldo de la cuenta de replay, declarado en §6.

## 4. Fase 4 · Comparación con el backtest original de agosto

Solo los 7 días del vídeo, todos `dev`; solo sus filas, que ya están ingeridas como
`knowledge/cases/dev/caso-eurusd-2026-08-*.yaml` (F14a, `casos-agosto-abril`), sin abrir el libro ni
ningún agregado. Criterio de ADR-0043 tal cual lo implementa `cases/criterio_fidelidad.py::emparejar`
(mismo día, sesión y dirección; |Δentrada| ≤ 3 puntos; |Δinstante| ≤ 15 min; 1:1, voraz y
determinista), con las tolerancias leídas de `knowledge/cases/criterio_fidelidad.yaml`. El instante
del vídeo es la hora de la tabla de §3.2 (estimada donde se dice) en UTC+2; el del caso es
`instante_utc`. Script: `scratchpad/comparar_v7.py` (fuera del repo; salida en
`scratchpad/comparacion_v7.txt`).

| | |
|---|---|
| operaciones del vídeo | 25 (incluida la 23 «no se toma» y la 25 sin llenado) |
| filas del backtest original en esos 7 días | 15 (el 2026-08-05 **no tiene caso**: el libro no trae fila ese día) |
| parejas | 8 |
| solo en el vídeo | 17 |
| solo en el backtest | 7 |

| día | backtest original (UTC / UTC+2, dir., entrada, stop) | vídeo (UTC+2, dir., entrada, stop, n.º) | resultado |
|---|---|---|---|
| 08-03 | — | 07:48, venta, 1.15358, 1.15368, n.º 1 | solo en el vídeo |
| 08-03 | 06:03:05 / 08:03, venta, 1.15364, 1.15380 | 08:03, venta, 1.15364, 1.15377, n.º 2 | difiere: stop 3 pt |
| 08-03 | 06:07:40 / 08:07, venta, 1.15362, 1.15388 | 08:10, venta, 1.15362, 1.15383, n.º 3 | difiere: hora 2 min, stop 5 pt |
| 08-03 | — | 09:40, venta, 1.15306, 1.15322, n.º 4 | solo en el vídeo |
| 08-03 | 09:46:15 / 11:46, venta, 1.15274, 1.15284 | 11:46, venta, 1.15274, 1.15287, n.º 5 | difiere: stop 3 pt |
| 08-03 | 09:52:50 / 11:52, venta, 1.15280, 1.15316 | — | solo en el backtest |
| 08-03 | — | 13:08, venta, 1.15253, —, n.º 6 | solo en el vídeo |
| 08-03 | — | 13:13, venta, 1.15256, 1.15266, n.º 7 | solo en el vídeo |
| 08-03 | 12:03:25 / 14:03, venta, 1.15320, 1.15337 | 14:05, venta, 1.15320, 1.15344, n.º 8 | difiere: hora 1 min, stop 7 pt |
| 08-03 | 12:10:55 / 14:10, venta, 1.15322, 1.15352 | — | solo en el backtest |
| 08-03 | — | 14:15, venta, 1.15338, 1.15352, n.º 9 | solo en el vídeo |
| 08-04 | — | 09:40, venta, 1.15129, 1.15163, n.º 10 | solo en el vídeo |
| 08-04 | 11:34:50 / 13:34, venta, 1.15184, 1.15193 | 13:36, venta, 1.15184, 1.15210, n.º 11 | difiere: hora 1 min, stop 17 pt |
| 08-04 | — | 13:55, venta, 1.15174, 1.15222, n.º 12 | solo en el vídeo |
| 08-05 | (sin caso) | 14:49, compra, 1.15488, 1.15472, n.º 13 | solo en el vídeo |
| 08-06 | — | 07:58, venta, 1.15499, 1.15505, n.º 14 | solo en el vídeo |
| 08-06 | 06:07:25 / 08:07, venta, 1.15488, 1.15516 | 08:07, venta, 1.15491, 1.15516, n.º 15 | difiere: entrada 3 pt |
| 08-06 | — | 12:36, venta, 1.15420, 1.15428, n.º 16 | solo en el vídeo |
| 08-06 | — | 13:15, venta, 1.15428, 1.15444, n.º 17 | solo en el vídeo |
| 08-06 | — | 13:34, venta, 1.15454, 1.15469, n.º 18 | solo en el vídeo |
| 08-07 | 05:14:55 / 07:14, venta, 1.15248, 1.15254 | — | solo en el backtest |
| 08-07 | — | 12:04, venta, 1.15293, 1.15312, n.º 19 | solo en el vídeo |
| 08-07 | 11:47:55 / 13:47, venta, 1.15318, 1.15323 | — | solo en el backtest |
| 08-07 | — | 13:56, venta, 1.15314, 1.15330, n.º 20 | solo en el vídeo |
| 08-07 | 12:09:10 / 14:09, venta, 1.15346, 1.15368 | — | solo en el backtest |
| 08-07 | 12:14:55 / 14:14, venta, 1.15345, 1.15383 | 14:18, venta, 1.15345, 1.15365, n.º 21 | difiere: hora 3 min, stop 18 pt |
| 08-10 | 11:57:15 / 13:57, compra, 1.15503, 1.15490 | 13:59, compra, 1.15503, —, n.º 22 | difiere: hora 1 min; stop no legible en el vídeo |
| 08-10 | 12:38:45 / 14:38, compra, 1.15484, 1.15477 | — | solo en el backtest |
| 08-10 | — | 14:55, compra, 1.15476, 1.15450, n.º 23 («no se toma») | solo en el vídeo |
| 08-11 | 08:08:55 / 10:08, compra, 1.15330, 1.15318 | — | solo en el backtest |
| 08-11 | — | 13:13, venta, 1.15410, —, n.º 24 | solo en el vídeo |
| 08-11 | — | 14:55, venta, 1.15399, 1.15419, n.º 25 (sin llenado visto) | solo en el vídeo |

Descriptivo, sin explicar: las 8 parejas coinciden en entrada a 0–3 puntos y en hora a 0–3 min; en
6 de las 8 el stop del vídeo difiere del stop del libro (3 a 18 puntos), y en la n.º 22 no se lee.
Ocho operaciones del vídeo se colocan en el mismo día y sesión que una del libro pero a otra hora u
otro precio, y siete del libro no aparecen en el vídeo (entre ellas dos compras, el 10 y el 11, y una
a las 07:14 del día 7). La n.º 20 del vídeo (13:56, 1.15314) y la fila del libro de las 13:47
(1.15318) quedan a 4 puntos: fuera de la tolerancia por 1.

## 5. Fase 5 · Qué dice el vídeo de cada pregunta abierta

Citas literales de la versión filtrada (ASR, sin corregir), con su minuto; «fotograma» cuando uno
de los abiertos enseña ese instante. **Ninguna lectura se elige aquí.** Las «opciones» son las de
`SESION-02-EXTRACCION.md`. Cuando lo dicho no encaja en ninguna, va como «posible lectura nueva».

### A-35 · cuándo un pivote de M15 está formado (opciones: `inicio_vela_contraria` · `cierre_vela_contraria`)

- 0:02:04 «vale, esta es una línea de M15 en M15 y así las demás»; 0:13:57–0:14:26 «vale el mapeo es
  este en M15 si iniciamos el mapeo para trazar la zona de liquidez es desde este punto hasta este
  punto. Llega aquí, llega aquí, sube. Llega aquí, llega aquí, sube. Y entonces ahí voy trazando, o
  sea, esa manera liquidez de 9.15» (fotogramas 001740000, 001801000: M15 con las líneas de
  liquidez trazadas sobre los altos y bajos previos, incluidos los de antes de las 07:00).
- 1:04:26 «vemos ya hasta aquí se llega a desarrollar una vela M15, entonces está marcada, pues no
  sirve para seguir».
- No dice en ningún momento en qué vela da el pivote por formado. Lo que sí dice, sobre M1 y no
  sobre M15, es la condición de la vela que «actualiza» un punto de breaker (0:24:03–0:24:38, abajo
  en A-21/candidatos).
- **No lo responde.** El vídeo lo toca menos que a A-21.

### A-45 · en qué granularidad se evalúa «cierra con cuerpo» (opciones: `cuerpo` · `mecha`; cierre de M15, M1 o tick)

- 0:28:56 «Como es con Mecha, ya lo he dicho también en anteriores videos, o sea, si hay un breaker,
  o sea, una toma de liquidez con Mecha, no se toma la operativa. A pesar de, independientemente, si
  está bien o no, pues no. O sea, no se toma.» 0:29:29 «yo por el momento, lo que yo tengo testeado
  es mejor no tomarlo si hay un breaker con mecha.» 0:29:48 «Entonces, esta operativa no se da»
  (fotograma 001740000, M15 del martes 4 a las 08:29:59: la mecha de las 08:15 por encima de la
  línea).
- 0:37:23–0:37:31 «este tipo de breakers o sea se valida está la zona lineal de liquidez que nosotros
  que nosotros usamos para poder entrar, tiene que ser un rompimiento con cuerpo y en ese caso, no
  sé si lo iba a romper, no, no lo iba a romper tampoco, entonces no hay entrada».
- 0:52:35 «y como nos rompió con cuerpo, no con mecha, entonces este punto de aquí se valida».
- 1:02:52 «y aquí tampoco hay entrada porque genera el breaker con mecha».
- La temporalidad en que mira ese cuerpo no la nombra; en 0:28:56 está en M15 (fotograma) y en
  0:52:35 en M1 (fotograma 003095000).

### A-21 · qué es una zona de control limpia (opciones: `solo_una_zona_de_control` · `sin_mecha_mas_alla_del_extremo`)

Lo que dice en voz:

- 0:16:40–0:17:30 «vale, aquí se invalida / aquí ya se invalidaría esta posible entrada / ¿por qué?
  porque nos dejó / dos zonas de control y nos rompe el esquema / porque si nosotros hacemos un
  mapeo / rápido, pues / tenemos esto aquí, vale / en el cual tenemos / una y 2 indiferentemente si
  después se dé o no esto que esté este esquema de / osa linealmente lo vemos así este esquema de
  entrada queda invalidado o / sea si llega a romper o ya apenas se desarrolla aquí al con
  anterioridad uno / se puede adelantar y decir pues queda invalidado porque al final lo que /
  buscamos en nosotros que sería el segundo esquema de entrada es que se / desarrolle de esta manera
  y aquí sólo desarrollo nacional control luego / genere el breaker, pero en ese caso ya quedaría
  invaliado, entonces no habría entrada, vamos / a dejar correr casi el precio, a pesar de que
  después llegue al 1.3, pero son las reglas.»
- 0:32:02–0:32:21 «vale tenemos hasta aquí claro aquí ya completa lo que sería la zona de control
  aquí nos da / entrada esquema 2 como podemos ver tal cual limpio entonces luego sería esperar el
  desarrollo de / de la otra zona de control, que sería esta de aquí / para poder poner en breakeven
  la entrada» (fotograma 001930000: n.º 10).
- 0:39:10–0:39:23 «Aquí no hay entrada / no entraba por el hecho de que el esquema que nos genera
  pues es este aquí que no está contemplado / dentro de los dos esquemas que usamos… entonces en
  esta sesión pues no hay trade».
- 1:03:39–1:04:48 «hay entrada porque se nos rompe el esquema / entonces aquí / pues quedaría
  invalidado / vamos aquí, tampoco / aquí tampoco / no hay esquema / y aquí por debajo tampoco…
  vemos el breaker por debajo, tampoco hay esquema aquí».
- 0:56:35 «esto aquí entonces quedaría invalidado si hay una posible entrada».

**Lo que se ve en cada entrada, que es lo que pedía el brief** (fotogramas de §3.2):

- **Qué zona marca y en qué temporalidad**: en M1, una caja (herramienta de niveles 0 / 0,25 / 0,5 /
  0,8 / 1) cuyo lado 0 es el extremo de la última vela o grupo de velas contrarias al lado de la
  entrada (el bajo, en las ventas) y cuyo lado 1 es el extremo opuesto de ese mismo bloque. Ejemplos
  legibles: n.º 1, caja 1.15358–1.15369 (000227000); n.º 3, caja 1.15362–1.15389 (000499000); n.º 7,
  caja 1.15256–1.15268 (001210000); n.º 11, caja 1.15184–1.15210 (002110000); n.º 15, caja
  1.15491–1.15516 (002654000). La liquidez de M15 es otra línea, azul y horizontal, que en 000271000
  y 000510000 lleva la etiqueta manuscrita «zlq m15».
- **Qué velas incluye**: una vela en la mayoría; en 0:24:03–0:24:38 y 0:52:46–0:53:13 dice que
  pueden ser «velas consecutivas del mismo color» y «este par de velas», con la condición de que
  «la vela siguiente… cubra, o sea, con mecha por debajo a la vela anterior, no importa si es del
  mismo color» (ver candidatos, «varias velas como un solo bloque»).
- **Antes o después de la toma de liquidez de M15**: después. 0:42:36–0:42:56 «como está por debajo
  de la zona lineal de M15, no hay, o sea, todo lo que haga por debajo no nos importa a nosotros,
  otros hay breakers o lo que sea no nos importa esperamos a que rompa y luego / después de
  rompimiento de la zona lineal de m15 se rompa el flujo de m1». En los fotogramas de las órdenes la
  caja está siempre del lado ya roto de la línea de M15.
- **Dónde pone la orden y el stop respecto a la caja**: la orden en el nivel 0 (el extremo cercano
  del bloque, mecha incluida), como orden STOP en la dirección de la ruptura (`Sell stop` bajo el
  precio; `Buy stop` sobre él); el stop en el 0,8 de la caja («dejamos en ese punto, en 0.80, el stop
  loss», 0:04:23), y en dos entradas primero en el 1 y luego en el 0,8 (n.º 3; 0:06:07 «primer
  cálculo es de 13 a normal o sea desde el punto 1 y luego se recalcula obviamente a 080»).
- **Posible lectura nueva** (no está en las dos opciones): la validez de la entrada la fija el
  ESQUEMA —una sola zona de control entre la ruptura de M15 y el breaker, y «dos zonas de control»
  lo rompen— y NO un atributo de la zona en sí (ruido, mechas). Es la primera opción dicha con otras
  palabras o es otra cosa: lo decide el consultor.

### A-46 · si una toma de liquidez de una sesión anterior del mismo día sigue valiendo (lectura libre)

- 0:13:10–0:14:26 (arranca la sesión 11-15 del día 3): «ahora nos vamos a la segunda sesión… vale el
  mapeo es este en M15 si iniciamos el mapeo para trazar la zona de liquidez es desde este punto
  hasta este punto». Vuelve a mapear, no dice si la toma de la mañana sigue valiendo.
- 0:46:45–0:47:29 (sesión 11-15 del día 6): «Ahora para operar esa sesión de aquí / Vemos nuevamente,
  nos vamos a H4… en esta primera de / esta sesión de zona lineal de liquidez en m15 tenemos / nos
  enfocamos en el orden flow».
- 0:57:00–0:57:19 «sesión el enfoque todavía sigue siendo bajista entonces marcamos liquidez por /
  encima no por debajo aquí tenemos el breaker de las líneas / de m15».
- **No lo responde**: cada sesión empieza por H4 y vuelve a marcar M15; no consta ninguna toma
  heredada ni descartada por ser de la sesión anterior.

### A-44 · magnitud y corte del tope de pérdida propio (opciones del registro `perdida_trader_*`)

- **No lo toca.** Ninguna mención a tope diario, semanal, saldo ni equity. Lo más cercano es el
  comentario sobre el break even como protección «en unas rachas malas» (0:20:44–0:21:05, A-13).

### A-43 · si una liquidez de M15 tomada antes de las 7 cuenta para operar después (lectura libre)

- 0:13:59–0:14:26 (arriba): las líneas de M15 se trazan sobre los altos y bajos previos sin
  distinguir hora. Fotogramas 001740000 (M15 del día 4 a las 08:29:59: líneas sobre pivotes de las
  04:00–06:00), 002505000 (M15 del día 6 a las 07:14:59: línea sobre un pivote de la tarde-noche del
  día 5) y 004110000 (M15 del día 11 a las 06:59:59).
- 0:42:36–0:42:56 (arriba, A-21): lo que pasa «por debajo de la zona lineal de M15» antes de la
  ruptura «no nos importa».
- **No lo responde en voz**; lo que hay es pantalla: los pivotes de M15 que marca incluyen los
  formados antes de las 07:00.

### A-24 · qué hace que marque un pivote de M15 y no otro (lectura libre)

- 0:14:07 «Llega aquí, llega aquí, sube. Llega aquí, llega aquí, sube. Y entonces ahí voy trazando».
- 0:51:50–0:52:27 «tenemos ahora esta zona aquí esta es una línea de liquidez de aquí que lo usamos /
  o sea porque es el más bajo a ver esto tampoco creo que lo mencionado en otros / otros vídeos o no
  recuerdo muy bien a ver si se ve o sea si el bot lo está / leyendo tal cual o sea y le han estado
  analizando los patrones se va a dar / cuenta que o sea estas zonas de aquí por ejemplo de las zonas
  anteriores sirve / sabe poder inclusive marcarlos desde aquí aquí solo que aquí no hay entraja /
  hay una entrada también que creo que la que tomamos y después está la otra zona / la liquidez
  lineal de M15» (fotograma 003095000).
- Lo que dice: «porque es el más bajo», y que «las zonas anteriores sirven». No da un criterio
  ejecutable.

### A-42 · con qué reloj cuenta su horario de 07:00 a 15:00 (`huso_operativa`, texto)

- 0:00:01 «Vale, pues lo primero que hago es configurar la zona horaria que sería en este caso pues
  UTC Madrid ya que me ubico en España, vale, ahora pues en 4 horas marco lo que serían, separo mis
  sesiones con las cuales voy a operar, sería la sesión de las 7 y 7 y 11, o sea de 7 a 11 y de 11 a
  3».
- Pantalla: el reloj del gráfico marca `UTC+2` y los sombreados de sesión del eje están en 07:00,
  11:00 y 15:00 de ese reloj (p. ej. 002425000). En agosto UTC+2 y Madrid coinciden, así que la
  pantalla no separa las dos lecturas; lo que aporta es la frase «UTC Madrid… ya que me ubico en
  España».

### A-26 · el flujo de M15 cuando va contra el sesgo de H4 (lectura libre)

- 0:01:16–0:01:40 «este caso nosotros ya sabemos que el bias o el tren principal la tendencia /
  principal lo tomamos como referencia en base a la vela anterior o sea el / movimiento anterior en
  este caso es bajista porque la vela / pues finalizó roja terminó por debajo de este load aquí y
  nos dirigimos en m15 / pues para atrasar las posibles zonas de de liquidez y reversión pues a favor
  de / la tendencia».
- 0:02:26 «toda nuestra operativa, al menos en esta sesión de aquí, se engloba a operativas
  bajistas, por lo cual ya sabemos que tenemos dos escenarios, dos esquemas».
- **No toca el caso de conflicto**: en los siete días nunca describe un flujo de M15 contrario al
  sesgo; siempre «a favor de la tendencia».

### A-25 · la vida de la marca de liquidez de M15 (opciones `cartuchos_reinicio`: `siguiente_liquidez_m15` · `fin_de_dia` · `nunca`)

- 0:05:36–0:05:51 «Mapeando, o sea, dando continuidad, haciendo el mapeo, pues vemos que tenemos
  ahora la próxima ruptura de liquidez que tenemos aquí. / ¿Vale? O sea, aquí tendríamos una order
  limit, nuevamente bajista.»
- 0:08:06–0:08:18 «nuevamente pues actualizamos / aquí tendríamos el posible / pero todavía no
  actualizamos / tendríamos que esperar a que rompa eso aquí / para poder validar un posible
  breaker».
- 0:16:22–0:16:31 «actualizamos el / actualizamos el punto de / el punto de breaker / posible punto
  de breaker».
- 1:09:11 «Tampoco llega a mitigar la liquidez de M15. / entonces tampoco hay entrada.»
- Lo que se ve: tras cada operación pasa a «la próxima» línea de M15 (n.º 1 → 2 → 3 el día 3, con
  la línea «zlq m15» en 000271000 y otra más abajo en 000510000). No dice qué pasa con una marca no
  tomada al cambiar de día.

### A-32 · el nivel que al romperse con mecha invalida la entrada (`breaker_m1_criterio_ruptura`: `mecha` · `cuerpo`)

- Las mismas citas de A-45 (0:28:56–0:29:48; 0:37:23; 0:52:35; 1:02:52). En 0:28:56 el nivel es la
  línea de M15 (fotograma 001740000); en 1:02:52 dice «genera el breaker con mecha» sin fotograma
  que diga qué nivel.
- 1:10:28–1:10:39 «nuevamente lo repito para ser claros, pues aquí tenemos una vela bajista, / pero
  se llega a actualizar por esta mecha de aquí, / entonces cumplió con los criterios para poder
  actualizar esa zona / y validarlo como pues nuestra este punto aquí como nuestra posible
  movimiento del flow y entra» (fotograma 004240000): aquí una MECHA sí actualiza un punto de
  breaker en M1. Contrasta con «breaker con mecha no se toma» de 0:28:56, que es sobre la línea de
  M15. Va tal cual al consultor.

### A-36 · en qué punto de la mecha va la orden límite (lectura libre)

- Pantalla: en las 25 órdenes la etiqueta de la orden está en el nivel 0 de la caja, que es el
  extremo (mecha incluida) del bloque; p. ej. 000227000 (n.º 1, orden 1.15358 = lado 0), 001210000
  (n.º 7, orden 1.15256 = lado 0), 002654000 (n.º 15, orden 1.15491 = lado 0). No dice nada en voz
  sobre entrar «un poco dentro».
- 0:24:27–0:24:38 «la condición es esta, que la vela siguiente, en este caso esta vela, / cubra, o
  sea, con mecha por debajo a la vela anterior, no importa si es del mismo color».

### A-37 · en qué temporalidad se busca la vela contraria de la que sale el stop (lectura libre)

- Pantalla: la caja de la que sale el 0,8 está trazada en M1 en todas las entradas de §3.2.
- 0:47:37–0:50:21 «aquí hay una entrada porque en 5 segundos en 5 / segundos esta vela roja esto creo
  que no lo tocado en anteriores vídeos pero es / algo más cosa que tiene que ver con el mapeo de
  estructura o sea el flujo… / no será cinco segundos para ver lo mejor lo tenemos / aquí porque en
  cinco segundos también hay un flujo de órdenes entonces mira es / es algo así… ya en M1, pues
  nosotros, / si vemos este tipo de vela, o sea, que una vela roja, en este caso, como, o sea, una /
  vela roja, en este flujo alcista, tiene una mecha por arriba y una mecha por debajo, entonces /
  aquí se desarrolla… vas a ver / que terminó / por encima de la mecha, o sea, cubriendo / tanto por
  arriba y por debajo, y bajista / entonces / aquí por debajo tendríamos nosotros / la order limit…
  ¿Qué es lo que hace? Claro, en un marco temporal menor, pero en este caso lo hace en una sola vela,
  por así decirlo, y ya con eso nos basta.» (fotograma 003025000, n.º 16, con el eje de 5 s visible
  en la barra de temporalidades).
- **Posible lectura nueva**: una vela de M1 que «cubre» la anterior por arriba y por abajo (una
  envolvente) vale como el bloque contrario entero «en una sola vela», y él lo explica mirando la
  estructura en 5 segundos dentro de esa vela.

### A-29 · cuándo nace la orden límite (`orden_limite_nace`: `al_darse_el_esquema` · `al_tomarse_la_liquidez`)

- 0:03:16–0:03:25 «aquí tenemos un breaker entonces aquí allí habría una entrada siempre con el / el
  orden límite obviamente entonces ubicamos esto aquí».
- 0:14:57–0:15:14 «un punto de breaker, mejor dicho. No una posible entrada, sino un punto de
  breaker. Que si / lo rompe el precio, pues se opera. Vale, lo activo.»
- 0:21:59–0:22:37 «si no se nos / desarrolla de esta manera todavía no existe / la posibilidad de
  nosotros poder marcar / este punto como / un posible breaker / para una posible entrada sino
  nuestro punto estaría aquí solo que nosotros / luego pues vamos actualizando para que pueda
  validarse esta zona de aquí pues / lo que sería es que se valide se desarrolla una nueva zona de
  control / o sea apenas con una mecha aquí y ya podríamos validar ese punto como / un posible
  breaker en este caso lo hace ahí actualizamos nuestro posible breaker y / pues lo fijamos».
- 0:44:14–0:46:11 «lo de la protección de 080 obviamente es casi de / inmediato sólo que como
  estamos calculando esta manera pues lo podemos / después pero es inmediato literalmente antes…
  nosotros, o sea, no nos da tiempo / para pensar, solo que como se va avanzando con / el Skip Candle
  / ya nos da la formación completa… inclusive en vela de 5 segundos / apenas genera el / breaker,
  pues… es una simulación previa que se hace / simplemente pero la operación se introduce digamos el
  límite se introduce ya como con / 0.080».
- 0:49:50–0:50:21 «aquí por debajo tendríamos nosotros / la order limit / o sea, nuestra order limit
  estaría actualizada / aquí… Entonces aquí tendríamos nosotros nuestro order limit actualizado.»
- Pantalla: la orden existe ANTES de la ruptura, como stop en el nivel del breaker, y se «actualiza»
  (se mueve) cuando aparece otro punto de breaker candidato; el llenado lo produce la propia ruptura
  (avisos «Stop order executed» en 000263000, 002455000, 002654000, 003640000).
- **Posible lectura nueva**: ninguna de las dos opciones describe «orden stop en el punto de
  breaker candidato, movida a cada actualización». Lo decide el consultor.

### A-30 · la orden límite pendiente al llegar el fin de la ventana (lectura libre)

- 1:06:26–1:08:01 «Sí, bueno, ya no se toma porque quedó un par de 10 minutos, entonces no hay trade
  aquí. / Aunque lo podría tomar, sí. O sea, si lo tomaría, pues, que es lo más probable que haga el
  bot, que lo tome. / Y si lo va a cerrar, a ver. / A ver, si lo toma, ¿en qué quedaría? / O sea, se
  cierra cuando finaliza la sesión, ¿sí o no? / Claro. / Claro, en este caso se cerraría por aquí,
  por debajo. / O sea, si yo lo calculo aquí, me contaría con un negativo, pero es un negativo
  insignificante… / Si yo lo cierro aquí, va a contar con / Como un 3 negativo, o sea, a menos 1 /
  ¿Entiendes? Lo va a marcar como negativo / O sea, lógicamente sí lo va a contar / Porque está en
  las reglas, ¿no? / Claro, claro / Pero claro, es algo insignificante… / Bueno, igual ya / Lo cierro
  en eso / pero se cerraría allí, sí.» (fotogramas 003990000 y 004025000: n.º 23, abierta a las
  14:59:59 y cerrada al cierre de la sesión).
- 1:11:42–1:12:10: la n.º 25 se coloca a las 14:50:59 del día 11 y el vídeo termina a las 15:00:59
  sin llenado visto (004310000, 004330000).
- Es de las preguntas sobre las que el vídeo más aporta: una entrada a 10 minutos del cierre «no se
  toma», y si se tomara «se cierra cuando finaliza la sesión» (esto último lo dice Aleks y el
  trader lo confirma con «Claro»). Quién dice cada frase se distingue mal en el ASR: va al
  consultor con esa cautela.

### A-38 · cuándo se da por anulada una orden límite que el precio deja sin llenar (lectura libre)

- 0:16:40–0:17:30 (A-21): «se invalida… porque nos dejó dos zonas de control y nos rompe el esquema».
- 0:21:59–0:22:37 (A-29): el punto de breaker se «actualiza» al formarse una zona nueva.
- 0:51:21–0:51:27 «que no tendremos entrar aquí aquí está aquí habría una entrada así / tenemos una
  posible entrada y se quita eso».
- 1:03:39–1:03:45 «hay entrada porque se nos rompe el esquema / entonces aquí / pues quedaría
  invalidado».
- No nombra un plazo ni una distancia: la anulación que describe es por esquema roto o por
  actualización a un punto nuevo.

### A-18 · base sobre la que se mide el objetivo 1:3 (`base_calculo_objetivo`: `caja_completa` · `riesgo_real`; `objetivo_rr`)

- 0:03:25–0:04:10 «obviamente me estaba oliendo en contra de la gestión pues sabemos que trazamos /
  cuadro de gas entonces trazamos desde allí o sea desde esas desde esa zona / hasta allí y lo
  ubicamos en nuestro grado 080 era / vale tenemos hasta allí tenemos como objetivo 13 pero desde
  aquí está / está calculando desde aquí hasta aquí, 1.3, pero obviamente luego se recalcula de esta
  manera.»
- 0:05:51–0:06:30 «lo ubicaríamos aquí en ese punto digamos cuadro de gas primero calculamos el /
  primer cálculo es de 13 a normal o sea desde el punto 1 y luego se recalcula / obviamente a 080
  cosa que ahí nos da el margen a 3 con 79 o sea ese más 79 es el / margen de beneficio / un margen
  de beneficio adicional a lo que buscamos que es el 13».
- 0:11:36 «Aquí trazo el cuadro, ahí hay un más 92% adicional de margen de beneficio».
- 0:20:04 «Vale, 1-3, obviamente sabemos que, para confirmar… configurando aquí el nuevo ajuste, 3
  más 6, es 0.6 de beneficio, de margen de beneficio adicional.»
- 0:25:39–0:25:52 «sabrás el 13 que está aquí vale recalculando a 0 80 más 0 75 de / beneficio
  entonces tenemos / más 386 más 3.75».
- 0:45:01–0:46:11 «me he preguntado algo, ¿cómo sería? / Porque el primer cálculo es, del 1, 3, es
  aquí, aquí, o sea, claro, nosotros buscamos el 1, 3, / ¿por qué me da 3 con 2? Con 2, no, 3, vale,
  aquí sería, por aquí estaría el tp. / Ahora, o sea, el primer cálculo, que no, creo yo, no sería
  con lotaje, sería aquí, / pero más o menos para calcular o sea el beneficio la principal de 13 es
  allí sólo que después / nosotros lo que hacemos el cálculo original es este aquí a 380 para tener
  ese 0.75 en ese caso / de beneficio o sea pero claro si nosotros damos aquí ya él estaría protegido
  aquí también o sea / directamente de aquí antes de que llega a romper o sea es una simulación
  previa que se hace / simplemente pero la operación se introduce digamos el límite se introduce ya
  como con / 0.080 y ahí claro por el tacto si sólo es referencia de la caja entera el clave /
  referencial es referencial más o menos para poder hacer el cálculo y todo eso».
- 0:50:35–0:50:49 «yo lo que suelo hacerlo para / bactecer un poco más rápido, calcular así / desde el
  punto más alto allí, lo multiplico por 3 / y ya / pero pasa que a veces / el 1, 3, ah coincide».
- 0:53:42–0:53:53 «ya recalculando y todo, sería así, desde allí hasta allí, pasando 0.8, sería 3.7,
  / tiene más 0.75 adicionales de beneficio.»
- 1:05:56–1:06:10 «mira por ejemplo aquí no coincide a 080 exacto si o no por los pips entonces iba
  a / tirar por debajo o por de o por arriba por debajo para tener más margen de protección / vale
  no no no bueno vale entonces nos quedaría más 55 de beneficio adicional».
- Pantalla (§3.2): en las 15 operaciones con los tres precios legibles, objetivo/stop va de 1,95 a
  3,7; en la n.º 7 el objetivo (37 puntos bajo la entrada) es 3× la caja 0→1 (12 puntos) y el stop
  está en el 0,8 (10 puntos): 3,7 sobre el stop; en la n.º 9, objetivo 42 = 3× stop 14; en la n.º 8,
  objetivo 56 y stop 24 (2,3).
- Es la pregunta sobre la que el vídeo más habla, y en dos sentidos que van tal cual al consultor:
  «desde el punto 1» como primer cálculo y «se recalcula a 0,80» con «beneficio adicional».

### A-13 · break even al toque o con cuerpo (`break_even_criterio_ruptura`: `mecha` · `cuerpo`)

- 0:04:31–0:05:08 «O sea, para poder poner break even, pues esperamos a que nos desarrolle una zona
  de control después de la ruptura, / o sea, después de que se inicie la entrada, tenemos el
  desarrollo de una zona de control, / la validación de la zona de control a través / de este
  rompimiento de aquí, en este caso / de este bajo, bajo, bajo… / porque ya aquí ya se llega a
  validar / pues / Pues aquella zona de control que nos permite a nosotros poner en break-even la
  entrada.»
- 0:09:01–0:09:15 «esperar a que nos desarrolle / la zona de control, si nos desarrolla la zona de
  control / nos da posibilidades a poner break even / y si no lo hace, pues / a esperar, o sea, a lo
  mejor nos quita / es más probable que si no desarrolla la zona de control / nos / termine tocando
  en SL».
- 0:09:35–0:09:43 «porque aquí ya, como digo, entra ese margen de A por poco, pero ya llega a
  activar, o sea, / este igual es como si hubiera hecho un breaker, entonces aquí también
  protegemos.»
- 0:20:34–0:21:08 «aquí nuevamente / podríamos poner break even / nos saca / y luego va / parece muy
  prematuro si a veces el break even / por eso con anterioridad a veces lo preguntaba / si era no
  considerable / pero bueno, a la larga no sirve / para protegernos porque / es nuestra manera a
  veces de / tratar de protegernos / en unas rachas malas / poner el break y B / vale, estos nos
  sacó en B» (fotograma 001240000: «Stop loss moved to 1.15256»).
- 0:57:41–0:58:19 «vale aquí nos genera para poner el break even / la zona de control / que si lo
  mapeamos / entonces ya podemos poner el breakeven».
- 0:59:59 «aquí no sería stop loss, sería un B, porque aquí, ahí ya nos pelearía ese movimiento para
  poder poner en B, y luego nos saca».
- Lo que dispara el BE en el vídeo es «el desarrollo/validación de una zona de control» tras la
  entrada, con «por poco, pero ya llega a activar» en 0:09:35. Si «al toque» o «con cuerpo» aplica a
  ese rompimiento no lo dice con esas palabras.

### A-31 · el stop entero de una entrada que se activó sin ruptura (lectura libre)

- 0:59:18–0:59:27 «va a ocurrir que, por ejemplo / aquí nos va a activar la entrada / No genera el
  breaker como tal, pero ya allí activaría la entrada. / Entonces, vamos a hacer 80, aunque es lo
  mismo que perder a uno.» (fotogramas 003560000, 003570000: n.º 20).
- 0:59:59 «6-6, bueno, aquí no sería stop loss, sería un B».
- Lo dice de pasada: la entrada activada sin breaker lleva el stop al 0,80 «aunque es lo mismo que
  perder a uno». No dice si gasta intento.

### A-40 · qué se hace con el stop después del break even (lectura libre)

- 0:36:12–0:36:31 «aquí ya tenemos el break even / entonces bueno aquí ya nos variaría el break even
  está este desarrollo del precio aquí nos / nos va a llevar y entonces protegemos».
- 1:05:18 «protegemos a B / pero recalculando».
- Pantalla: los avisos «Stop loss moved to …» mueven el stop al precio de entrada (001240000,
  003060000, 004280000) y no se ve ningún movimiento posterior. No toca la protección progresiva.

### A-33 · tres ganadoras que cierran por debajo de 3R (`parciales`: `si` · `no`; `objetivo_rr`)

- 0:17:23–0:17:30 «vamos / a dejar correr casi el precio, a pesar de que después llegue al 1.3, pero
  son las reglas.»
- Los cuatro tramos de cifras agregadas (§6) hablan del «RR promedio» de la sesión de replay; se
  citan solo por su minuto: 0:12:43, 0:26:14–0:26:22, 0:54:06–0:54:51, 1:12:43–1:13:18. Ninguna cifra
  se usa.
- No dice nada de parciales.

### A-34 · vela H4 previa que rompe ambos extremos (lectura libre)

- 0:27:59–0:28:35 «bajista porque para nosotros si queremos buscar / una operativa alcista al menos
  la vela verde debe de haber terminado por encima / sea con cuerpo con mecha a esta vela roja o
  para dar o sea si no lo hace entonces / pues continuamos como creativa bajista inclusive si hay
  una vela vela verde por / con poco sea una pequeña mecha pero no ha llegado a romper esa mecha
  igual / igual seguimos buscando operativas bajistas ya estamos como que en este / rango aquí pero
  con un enfoque bajista».
- 0:33:10–0:33:24 «todavía seguimos bajista porque no hemos / llegado a capturar ese movimiento desde
  aquí arriba nave la alcista verde con / cierre con mecho con cuerpo entonces seguimos bajista».
- 0:38:24–0:38:45 «Vemos que haya sido / roto esta zona de rango / por una vela verde alcista en 4H
  / y nuestra última vela / es alcista también, entonces esto no / da a entender que ahora / las
  operativas que vamos a buscar en esta sesión / son alcistas».
- 0:39:51–0:40:06 «para poder nosotros operar bajistas, sería que esta vela bajista con mecha o con
  cuerpo debió de haber terminado por debajo. / Por debajo de esta zona de aquí, de esta vela de
  aquí. Como no lo hizo, pues seguimos buscando operativas alcistas.»
- 0:59:59–1:02:14 «el enfoque es bajista, archista, perdón, porque nos ha roto por debajo, /
  estamos en un rango calcista».
- **Posible lectura nueva**: el sesgo se MANTIENE hasta que una vela de H4 «termina» más allá del
  extremo de la anterior «sea con cuerpo con mecha», y una mecha pequeña que no llega no lo cambia.
  No toca el caso de la vela que rompe ambos extremos.

### A-41 · si hay un tope de entradas por día (lectura libre)

- No lo dice. Pantalla: el día 3 lleva 9 órdenes (§3.2), 4 en la sesión 07-11 y 5 en la 11-15.

### A-39 · qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo (lectura libre)

- 0:33:02–0:33:24 (fin de una sesión: «nos vamos a 4h para ver que / cuál es nuestro bias o nuestra
  tendencia principal / para la siguiente sesión»); 0:37:52–0:38:45 (cambio a alcista al arrancar la
  sesión); 0:46:46 «Vemos nuevamente, nos vamos a H4 para ver qué onda».
- No hay ninguna posición abierta ni orden pendiente que cruce el cambio; no lo toca.

### Los candidatos del consultor

- **Doji como vela contraria**: no lo toca.
- **Vela contraria que vuelve a su color antes de cerrar**: 0:10:47–0:11:35 «Ahora se torna
  interesante porque no sé si te diste cuenta que, al menos, si me, bueno, tendría que irme para
  constatar a TradingView y retroceder hasta, ¿cómo se llama esta vaina? / hasta agosto, a esta fecha
  / para ver si esta vela era roja o no, porque estaba roja / pero luego se tornó, o sea / en este
  color en verde / si es rojo, no sé, a ver / voy a retrocederlo, voy a tratar de validar / porque a
  veces cuando se actualiza, cuando estás / ya ves, ahí llega / solo que cuando lo retrocedo, que se
  yo / se desconfigura algo y ya, pero / a lo que te vote primero / como en este caso, ustedes en el
  / actez, es fijo que es roja / en TradingView / entonces estaría ubicado aquí» (fotogramas
  000660000 y 000700000: retrocede el replay de 09:35:59 a 09:33:59 y coloca la n.º 4). También
  0:47:37–0:50:21 (A-37: la vela de M1 vista en 5 segundos).
- **Varias velas como un solo bloque**: 0:19:14–0:19:32 «que antes de desarrollar tele y cual pues
  te genere o bien / este esquema de aquí con anterioridad como sería este de aquí o bien pues en /
  un par de en un par de cúmulos de velas entre tres o cuatro pues te desarrolla / esto aquí te
  genera el breaker»; 0:24:03–0:24:55 «ya es cuando pueden ser velas consecutivas del mismo color sí
  o / sea pero no necesitamos que sea roja para poder decir vale esta zona puede / Puede ser un
  posible breaker… / la condición es esta, que la vela siguiente, en este caso esta vela, / cubra, o
  sea, con mecha por debajo a la vela anterior, no importa si es del mismo color. / Bajista también
  funciona igual… / y luego la vela roja, esto es parte de la mecha, y luego cae y cierra por debajo,
  / pues ahí también actualizaríamos»; 0:52:46–0:53:13 «esta / combinación de velas, este par de
  velas / ya no sirve, no necesariamente / el color, porque usualmente para marcar el flujo / de
  órdenes y demás, y marcar la posible entrada / o sea, el posible breaker / tener una vela roja luego
  una vela verde pero con esto de aquí pues no nos sirve». **Posible lectura nueva**: el bloque no
  se define por el color sino por que la vela siguiente cubra con la mecha el extremo de la anterior.
- **Tamaño del pequeño retroceso**: no da tamaño. 0:48:05–0:48:16 «la idea original es / que se nos
  rompa ese flujo de órdenes para poder entrar independientemente no esperamos retroceso / en nada si
  no entramos directamente protegemos y ya».
- **Antigüedad máxima del pivote del breaker**: 0:51:50–0:52:27 (A-24: «las zonas anteriores
  sirven»); no da un máximo.
- **Zona invalidada por una mecha o por otra zona posterior**: 0:16:40–0:17:30 (dos zonas de control
  invalidan); 0:21:59–0:22:37 y 0:16:22–0:16:31 (el punto se «actualiza» al aparecer otro);
  1:10:28–1:10:39 (una mecha «actualiza» la zona en M1); 0:28:56–0:29:48 (breaker con mecha sobre la
  línea de M15 no se toma).
- **Fuera de los candidatos, y que no encaja en nada documentado** (posibles lecturas nuevas):
  (1) los «equals»: 0:18:52–0:19:32 «Vale, aquí hay un equal. / Este, como había dicho con
  anterioridad y en anteriores videos, los equals lo operamos al final. / La manera de operar es la
  siguiente. / Para nosotros operar primero, comprender y saber que estamos buscando operativas
  bajistas. / Los equals que se operan bajistas son estos de aquí…»; (2) la orden STOP y su
  actualización (A-29); (3) la entrada que «se activa sin generar el breaker» (A-31); (4) la vela
  envolvente de M1 como bloque «en una sola vela» (A-37).

### Resumen para el consultor: dónde aporta más y dónde no toca

- **Más**: A-18 (once pasajes y quince operaciones con los tres precios), A-21 (la geometría de las
  25 entradas en pantalla y la regla de «dos zonas de control»), A-29/A-36 (la orden es stop en el
  punto de breaker y se actualiza), A-30 (la entrada a 10 minutos del cierre y el cierre al fin de
  sesión), A-45/A-32 (cuerpo frente a mecha, dicho cuatro veces).
- **Algo**: A-13, A-34, A-37, A-25, A-42, A-43, A-24, A-31, A-38, A-40.
- **No toca**: A-35 (en M15), A-44, A-26 (el conflicto), A-46, A-33 (parciales), A-39, A-41, doji,
  tamaño del retroceso, antigüedad máxima.

## 6. Exposiciones, declaradas hoy

Fila añadida a `docs/validation/HOLDOUT-EXPOSICIONES.md` (mismo commit que este informe). Resumen:

- **Agosto es DESARROLLO** (§3.1): ninguna partición tocada. Se declara igual, como el 2026-09-21,
  22 y 23.
- **Agregados vistos en el TEXTO de la transcripción**, sin abrir ninguna captura: en 0:11:07–0:12:43,
  0:26:06–0:26:22, 0:54:06–0:54:51 y 1:12:43–1:13:18 el trader lee en voz alta la pestaña Analytics
  de SU sesión de replay (la que graba, sobre el 3–11 de agosto): «tengo un loss y un win»; «RR
  promedio… entre 3.4… 3.6»; «dos win, cuatro loss y tres break even»; «3,71, 7,42 menos 4, a un
  beneficio de 3,42 en esta sesión»; «tres positivos y nueve negativos a 3.47»; «3 con 47, por 4, 13
  con 88, menos 9, a 4 con 48»; «serían 12 entonces a 3 con 30… 3.36». Son agregados de la propia
  grabación, no del backtest original. **Ninguna se usa.**
- **El saldo de la cuenta de replay** en los fotogramas abiertos (de $100 000,00 a $100 042,00, con
  los USD de cada etiqueta de orden). Es el mismo agregado, en pantalla. **No se usa** (los
  resultados de §3.2 se anotan y no cuentan).
- **Los fotogramas de Analytics NO se abrieron**: 0:11:40–0:12:43, 0:26:06–0:26:40, 0:54:02–0:54:55 y
  1:12:43–1:13:30 quedaron cerrados a propósito (ADR-0038 §2 y §3).
- **El libro de agosto no se abrió**: la Fase 4 leyó solo los `caso-*.yaml` `dev` ya ingeridos.

## 7. Riesgos y dudas para el consultor

1. **El brief y el material no coinciden** (§0): primera mitad de agosto, no segunda; sin códigos de
   pregunta. Si la sesión con la hoja se grabó aparte, ese audio no está en el corpus.
2. **Las horas de llenado son estimadas en 12 de las 25** (ventanas de 2 a 26 minutos entre la orden
   y el primer fotograma con la posición). Para ADR-0043 (±15 min) alcanza en todas menos quizá la
   n.º 4 (≥09:34, sin llenado visto) y la n.º 21 (ventana 14:05–14:31). Afinarlas exige abrir más
   fotogramas: están localizados y se puede hacer sin muestreo.
3. **Precios a ±1 punto**: las etiquetas se leen sobre vídeo comprimido a 1920×1080. Las tres
   parejas «difiere: entrada/stop 3 pt» de §4 están justo en el borde de la tolerancia.
4. **Los tipos de orden**: `Sell stop` frente a «orden límite». Puede ser vocabulario de FX Replay o
   una diferencia real con RN-008/RN-011. No se ha tocado la spec.
5. **La operación 23 «no se toma» pero se cuenta**: está en la tabla y en la comparación porque el
   trader la abre y la cierra en pantalla. Si el consultor la excluye, la n.º 23 pasa a «no
   operación» y nada más cambia.
6. **El día 5 no tiene caso en el libro y sí una compra en el vídeo** (n.º 13). Puede ser que el
   libro no tenga fila ese día o que la ingesta de F14a no lo trajera: no se ha mirado el libro.
7. **Quién habla**: el ASR no separa voces. En A-30 la frase «se cierra cuando finaliza la sesión, ¿sí
   o no?» parece de Aleks y el «Claro» del trader; se cita con esa duda.
8. **Fotogramas y transcripción en un solo commit** (§1), a diferencia de v6.

## 8. Estado

Rama lista para revisión, NO cerrada.
