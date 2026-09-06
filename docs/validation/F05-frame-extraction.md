# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F05 · frame-extraction
**Rama:** `feature/F05-frame-extraction`
**Objetivo:** fotogramas con marca de tiempo de los videos del corpus (cuatro al abrir la rama;
cinco tras el material del 2026-09-05, ver seccion propia), indexados y
reproducibles, para que F07 cite lo que se ve en pantalla (Excel, herramienta de posicion, caja,
configuracion del grafico) igual que F04 cita lo que se oye, y F08 responda "que hay en V4
0:44:56" con audio y fotograma. Instruccion del usuario (2026-09-05): maxima eficacia y
fidelidad para extraer todo lo necesario, sin restriccion de tiempo ni recursos.

## Que se construyo
- `src/botsito/corpus/fotogramas.py` (ADR-0008): cobertura COMPLETA de cada video a 1 fps, sin
  perdida (PNG, `-fflags +bitexact -flags +bitexact`), con una regla unica de seleccion "primer
  fotograma fuente con `t >= instante`": regulares en una pasada con
  `select='isnan(prev_selected_t)+gte(floor(t),floor(prev_selected_t)+1)'` y `-fps_mode
  passthrough` (conserva el `pts` original), `showinfo` DESPUES de `select` para leer el
  `pts_ms` real; obligatorios con fraccion de segundo con `-ss <t> -copyts` (misma regla). Un
  obligatorio en segundo entero ES el regular (misma imagen, mismo hash). `index.jsonl` (`n`,
  `t_ms` nominal, `pts_ms` real, fichero `<t_ms>.png`, sha256, bytes, origen) validado (n
  consecutivos, t unicos y crecientes, pts crecientes, regulares en segundo entero). `huecos`
  sobre `pts` consecutivos (> 2 s, constante tecnica). `plan_instantes` (obligatorios en o
  despues del fin del video, o repetidos: error). `mas_cercanos` por `pts`. Idempotente: si el
  indice esta completo en disco no se decodifica; indice escrito al final y atomico.
  Carpeta de trabajo `data/fotogramas/<video>/png-1fps[-<huella8>]/` con `video.sha256` y
  huella (build de ffmpeg + parametros + instantes extra): otra huella es otra carpeta, la
  anterior nunca se pisa. Guardias previas a decodificar: un video tiene exactamente una
  extraccion activa (extraer a otra carpeta exige `--reemplaza-a` = la activa; repetir la
  misma carpeta no lleva `--reemplaza-a`); y si un manifiesto ya registra la carpeta, el
  indice de hoy debe tener su sha256 (inmutabilidad; delata otra build de ffmpeg).
- `src/botsito/corpus/manifiestos_fotogramas.py`: manifiesto INMUTABLE
  `knowledge/corpus/fotogramas/fr-<video>-<hash8 del sha256 de index.jsonl>.yaml` (esquema:
  video, sha256 del video, duracion, resolucion, build de ffmpeg, parametros con la regla de
  seleccion, carpeta, recuentos, `ultimo_pts_ms`, `huecos` (el esquema los ACEPTA; la
  aceptacion de F05 exige `[]`), `extra`, `sha256_index`, `reemplaza_a`); `cargar_todos`
  (ids repetidos, `reemplaza_a` inexistente, de otro video o ciclico, y MAS DE UNA ACTIVA POR
  VIDEO son error); `comprobar` (sha256 de `index.jsonl`, recuentos, ultimo pts, huecos y extra
  recomputados desde el indice; existencia y tamano de cada fichero; hash de los extra y de una
  muestra determinista de 20 regulares; carpeta ausente = aviso); `comprobar_obligatorios`
  (cada instante de la lista existe en la extraccion activa); `referencias_conocidas`
  (`fr-<id>/<t_ms>` de TODOS los manifiestos, activos o reemplazados, mas rutas del corpus con
  papel `material_adicional`; `heredado_v2` excluido).
- `knowledge/corpus/fotogramas_obligatorios.yaml` (manual, versionado): V3 0:28:56 (Excel),
  V2 0:33:21 (herramienta de posicion 4,08/3,94), V4 0:12:30 (caja 0,75 = 1,19537).
- CLI: `corpus frames extract --video v1 [--reemplaza-a fr-...]`, `corpus frames check`,
  `corpus frames show --video v3 --t 0:28:56 [--n 3]` (referencia citable, `pts` real, ruta
  y el segmento de la transcripcion activa que cubre el instante). `knowledge validate` suma
  la capa de fotogramas (esquema, un activo por video, historial de git, `index.jsonl` por
  hash y recomputo, obligatorios presentes; sin `data/fotogramas` avisa; NUNCA hashea los
  16 182 PNG). Hook protege `knowledge/corpus/fotogramas/`. `comun/ids.py` gana `fotogramas`
  (`fr-<video>-<hash8>`) y `referencia_fotograma` (`fr-<id>/<t_ms>`); `comun/historial.py`,
  `DIRECTORIO_FOTOGRAMAS`.
- ADR-0008; `knowledge/corpus/README.md` con los dos regimenes nuevos; MASTER_PLAN (tabla A
  fila F05 reescrita, H.2 fila F05 resuelta, Change Log); `tests/integration/` estrenado.

## Archivos creados
```
src/botsito/corpus/{fotogramas,manifiestos_fotogramas}.py
knowledge/corpus/fotogramas_obligatorios.yaml
knowledge/corpus/fotogramas/fr-v1-5a2a42c3.yaml  fr-v2-c5a09508.yaml  fr-v3-982da728.yaml  fr-v4-9ad0ebb8.yaml
docs/adr/0008-fotogramas-cobertura-completa.md  docs/plan/features/F05-frame-extraction.md
docs/validation/F05-frame-extraction.md
tests/unit/test_fotogramas.py  tests/integration/{__init__,test_fotogramas_ffmpeg}.py
tests/contract/test_fotogramas_history.py
```

## Archivos modificados
`src/botsito/cli.py` (subcomando `frames`), `src/botsito/validation/knowledge.py` (capa),
`src/botsito/comun/{ids,historial}.py`, `scripts/git-hooks/pre-commit`,
`tests/contract/test_import_contracts.py` (test AST: argv que empiece por `ffmpeg`/`ffprobe`
solo en `corpus/{audio,inventario,fotogramas}.py`), `knowledge/corpus/README.md`,
`docs/adr/README.md`, `docs/plan/MASTER_PLAN.md`, `PROJECT_STATE.md`.

## Decisiones tomadas
1. **Cobertura completa, no "tramos con decision"** (cambio del plan, decidido por el usuario).
   Medida sobre las cuatro crudas `tr-*` antes de fijar la regla que pedia H.2:

   | Regla | v1 (29 min) | v2 (69 min) | v3 (78 min) | v4 (94 min) |
   |---|---|---|---|---|
   | 25 palabras del dominio, ±10 s, fusion 20 s | 75 % | 46 % | 83 % | 77 % |
   | Misma lista, ±15 s, fusion 30 s | 86 % | 52 % | 90 % | 83 % |
   | Deicticos (aqui, esto, este, mira, aca), ±10 s, fusion 20 s | 93 % | 56 % | 89 % | 85 % |
   | Dominio + deicticos, ±15 s, fusion 30 s | 97 % | 79 % | 97 % | 99 % |

   Ponderado por duracion, filtrar ahorraria del 7 % al 29 % del disco. El unico tramo sin
   decision claro es la musica y el audio malo de V2 que F04 ya lista.
2. **PNG sin perdida** en lugar de JPEG q=2 (instruccion de maxima fidelidad). Coste real
   abajo. Bitexact: el hash no depende de la version del codificador; si del decodificador
   H.264 de la build (no verificado entre builds).
3. **Regla `select` con `pts` real; `fps=1` descartado** (revision de diseno, verificado
   tambien sobre V3): `fps=1` elige el fotograma en `n + 0,47 s`, reescribe el `pts` a
   `0, 1, 2...` y duplica fotogramas en los saltos de la fuente; los tests de `pts` habrian
   pasado sin probar nada y `huecos` habria sido vacuo.
4. **Un `fr-*` activo por video**; obligatorios fuera del manifiesto inmutable (lista mutable
   validada contra el indice activo); `referencias_conocidas` sin `heredado_v2`.
5. **A-9 sin instante inventado**: F05 entrega la cobertura y la lista de candidatos (abajo);
   elegir el fotograma y registrar la evidencia es de F07.
6. V3 0:12:26 (marca heredada "huecos de fotogramas") no entra en los obligatorios: era un
   defecto de la extraccion antigua; la cobertura completa contiene ese segundo.

## Como ejecutarlo
```
uv run botsito corpus frames extract --video v1        # idempotente; ~1,5 min por hora de video
uv run botsito corpus frames check                     # manifiestos frente al disco y obligatorios
uv run botsito corpus frames show --video v3 --t 0:28:56 --n 3
uv run botsito knowledge validate
```
Los PNG viven en `data/fotogramas/<video>/png-1fps/` (8,9 GiB = 9,5 GB en total, fuera de git); si no
estan, `knowledge validate` avisa y `extract` los regenera en ~10 min con el mismo id.

## Como probarlo
`make check` (lint, mypy strict, contratos, 264 funciones de test, state, config, knowledge).
Los tests con ffmpeg usan `tests/fixtures/clip_2s.mp4` (10 fps, 2 s) copiado a un nombre con
acento y `ñ`, y un clip sintetico con un salto real de 3 s (lavfi `testsrc` + `select`,
codificado con `mpeg4`) para el test de huecos; en CI ffmpeg es obligatorio (nunca se salta en
silencio). No hay goldens de sha256 (la CI usa el ffmpeg de apt; el determinismo se afirma
entre dos ejecuciones en la misma maquina).

## Tests ejecutados
- Unit (puros): `parsear_showinfo` (orden, lineas ajenas, numeracion), nominal y referencias
  (`ids`), `plan_instantes` (fraccion, fin del video, repetido), `huecos` sobre `pts` (falta
  de un segundo no es hueco; de tres si; inicial), JSONL ida y vuelta y rechazos, `Fotograma`
  (negativos, pts < t, nombre, origen), `validar_indice`, `mas_cercanos` (empate al anterior,
  fuera de rango), `cargar_obligatorios` (formato, repetidos, vacios), esquema del manifiesto
  (13 rechazos), `cargar_todos` (dos activas, `reemplaza_a` de otro video o inexistente),
  `referencias_conocidas` (excluye `heredado_v2` y `video_original`, incluye reemplazados y
  `material_adicional`), `comprobar_obligatorios`, `comprobar` sin datos = aviso.
- Integracion (ffmpeg, clip con nombre acentuado): regulares con `pts_ms` EXACTOS (0, 1000),
  obligatorio 0:00:01.250 con `pts_ms == 1300`, obligatorio 0:00:01 byte-identico al regular,
  PNG sin etiqueta `Lavc`, fin del video y video inexistente como error, ffmpeg ausente como
  error explicito; `extraer_video` (manifiesto, `extra`, resolucion, `video.sha256`),
  determinismo (segunda extraccion, mismos sha256), idempotencia (mtime intacto, manifiesto
  sin reescribir, "no se decodifica"), obligatorio nuevo con fraccion exige `--reemplaza-a`
  (tres errores distintos) y con el crea otra carpeta y otro manifiesto dejando el anterior
  intacto, manifiesto con otro `sha256_index` para la carpeta = error de inmutabilidad, video
  cambiado, obligatorio fuera del video; `comprobar` detecta PNG alterado (mismo tamano),
  tamano distinto, fichero borrado, `index.jsonl` editado, carpeta ausente (aviso); clip con
  salto real produce hueco > 2 s; CLI `extract`, `check`, `show` (n=2, error fuera de video,
  video inexistente, `--reemplaza-a` inexistente), obligatorio pendiente reclamado por `check`
  y por `knowledge validate`, `knowledge validate` en verde con la capa y sin `data/` con
  AVISO; `show` con transcripcion activa (`MotorFalso`) imprime el segmento que cubre el
  instante.
- Contrato: historial de git de `knowledge/corpus/fotogramas/` (modificar y borrar se
  detectan; repositorio real intacto), hook protege el directorio, argv `ffmpeg`/`ffprobe`
  solo en los tres modulos de corpus.
- Real (esta maquina): cuatro videos; muestra determinista de 20 fotogramas por video
  re-extraida con `-ss -copyts` y comparada por `pts` y sha256 con el indice.

## Resultados
### Extracciones reales (ffmpeg 9.0.1 gyan, Windows, CPU)

| Video | Resolucion | Fotogramas | `ultimo_pts_ms` | Huecos > 2 s | Tamano | Por fotograma | Tiempo |
|---|---|---|---|---|---|---|---|
| v1 | 1920x1080 | 1753 | 1 752 000 | ninguno | 795 MiB | 465 KiB | ~1,5 min |
| v2 | 1898x1074 | 4135 | 4 134 000 | ninguno | 2538 MiB | 628 KiB | 2,9 min |
| v3 | 1762x884 | 4677 | 4 676 000 | ninguno | 2326 MiB | 509 KiB | 3,0 min |
| v4 | 1778x952 | 5617 | 5 616 000 | ninguno | 3420 MiB | 624 KiB | 4,0 min |

Total 16 182 fotogramas, 8,9 GiB (9,52 GB, `du -sb`), ~11 min. `ultimo_pts_ms` = `floor(duracion)` en los cuatro
(existe fotograma en el ultimo segundo entero). Ningun extra: los tres obligatorios caen en
segundo entero y son regulares. Ids: `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`,
`fr-v4-9ad0ebb8`. `frames check` y `knowledge validate` en verde.

### Determinismo e idempotencia
- 20 fotogramas por video (80 en total) re-extraidos con `-ss <t> -copyts` y la misma regla:
  80/80 identicos en `pts` y sha256 (17 s).
- Segunda ejecucion de `extract` en los cuatro videos: "indice ya completo, no se decodifica",
  mismo id. (Durante la construccion la huella de la carpeta gano los instantes extra; las
  marcas `huella.txt` de las cuatro carpetas se reescribieron al valor final y la re-ejecucion
  devolvio los mismos cuatro ids: el contenido no cambio.)

### Obligatorios (lo legible, hechos; registrar la evidencia es de F07)

| Instante | Referencia | Que se ve |
|---|---|---|
| V3 0:28:56 | `fr-v3-982da728/1736000` | Excel del trader, celda C11 seleccionada, barra de formulas `2,83`. Fila 11 (23-abr-26): `2,83`, `-0,75`. Fila 12 (24-abr-26): `-0,5`, `3,3`, `-0,75`, `-0,5`. Fila 13: `-0,75`, `-0,75`, `9`. Inferencia (no hecho): si la marca heredada describia este Excel, sus cifras `2,3 / 3,23` no coinciden con la pantalla; large-v3 (`2.83 ... 3.33`) coincide en la primera y no en la segunda (`3,3`). Audio 0:28:51 "Aqui pueden ver como es los ratios de beneficios que he estado trabajando" |
| V2 0:33:21 | `fr-v2-c5a09508/2001000` | TradingView, EURUSD 1 min FXCM, dos herramientas de posicion: "Cerrado PyG: -0,00013, Cantidad: 7, ratio riesgo/beneficio: **4,08**" y "Cerrado PyG: 0,00063, Cantidad: 6, ratio riesgo/beneficio: **3,94**"; "Stop: 0,00013 (0,011 %) 1,3, Importe: 9900" y "Stop: 0,00016 (0,014 %) 1,6, Importe: 9900"; eje X con "jue 02 jul '26 12:24 / 12:41 / 13:10"; reloj del grafico **15:36:46 UTC+2**. Coincide con el golden de F21. Sin segmento de transcripcion en ese instante |
| V4 0:12:30 | `fr-v4-9ad0ebb8/750000` | FXReplay, EUR/USD 1 min, caja de Gann con niveles 0 / 0,25 / 0,5 / 0,75 / 1 y el precio en el 0,75 = **1,19537** (etiqueta del eje); "Fri 30 Jan '26 14:29 / 15:00"; reloj **14:29:59 UTC+2**. Audio 0:12:24 "que este 0.75 se desplace lo suficiente como para que este de acuerdo al split [spread] del momento" |

### Candidatos para A-9 (configuracion del grafico), buscados en las crudas
Palabras: zona horaria, huso, UTC, hora de, configur-, temporalidad, Nueva York, Londres,
Madrid, sesion, GMT, medianoche. Hechos relevantes (F07 elige y registra):
- **V3 0:01:41** "yo lo tengo configurado como utc mas 2 que son ahora ya madrid" (el fotograma
  `fr-v3-982da728/101000` muestra la ficha de reglas del trader en Word, no el grafico: el
  grafico esta en los segundos siguientes).
- **V2 0:33:21** y **V4 0:12:30**: el reloj del grafico marca `UTC+2` en TradingView y en
  FXReplay (fotogramas obligatorios de arriba).
- V4 1:14:29-1:14:55 "3 pm en el horario UTC... de 7 a 3 pm utc mas 2"; V4 1:24:34 "UTC mas 2";
  V1 0:00:54-0:00:56 "la zona horaria... en Peru no tengo ni idea... 7 de la manana"; V2
  0:03:10 "22 [dos] sesiones que serian la de nueva york y londres"; V3 0:04:51 "9 y 45 horas
  espana cierra... la bolsa de nueva york"; V3 0:05:39 "lo fija la vela de 4 previa cerrada".
- Sin decidir aqui: que el grafico este en UTC+2 no dice por si solo a que hora abre su H4
  (TradingView y FXReplay anclan la H4 segun el proveedor); es exactamente lo que A-9 pregunta.

### Hallazgo colateral (hecho, para F07)
`fr-v3-982da728/101000` (V3 0:01:41): documento Word "Ficha de especificaciones" con la tabla
"Confirmaciones rapidas (reglas ya definidas)" y la columna "¿Confirmas? / Ajuste" rellenada
por el trader: ventana operativa 07:00-15:00 hora Espana (Londres + Nueva York) "Si"; sesgo
direccional lo fija la vela H4 previa ya cerrada (n-1) "Si"; marco H4/M15/M1/M5 "Ajuste:
todavia no hay que anadir m5 por ahora"; solo velas japonesas "Si"; entrada por orden limite en
el origen del quiebre (sin respuesta visible); limite estricto de 2 cartuchos por barrido "si";
ratio minimo 1:3 "si"; parciales 30-40 % "Creo que lo ideal seria probar sin la toma de
parciales, cumple objetivo o no de rr"; cierre agresivo opcional al vencimiento de la H4 "si";
sizing 1 % cuenta propia, 0,50-0,75 % en fondeo "si"; break-even tecnico al confirmarse una
2.a zona de control en M1 "Si"; caja de Gann nivel 0,75 "Si". Las contradicciones "2 cartuchos (ficha) frente a 3 (V4 0:48:41)" y "parciales 30-40 %
frente a sin parciales" YA constan en PROJECT_STATE (Known Contradictions, heredadas de Bot v2);
lo nuevo es que ahora existe un fotograma citable de la ficha. No se registra aqui.

## Material adicional recibido el 2026-09-05 (carpeta "Info extra de backtesting")
Instruccion del usuario: analizarlo y anadirlo donde sea pertinente antes de validar F05. Se
integro en el corpus con los mismos regimenes que el resto (hechos; la evidencia la registra F07):

- **Video v5** `2026-09-05 21-03-59.mkv` (121,5 MB, 1280x720, 30 fps, H.264 + AAC, 365,0 s,
  `start_time` 0; no esta en Drive: `drive_id` lo declara en `fuentes.yaml`). El trader graba su
  pantalla en FXReplay (sesion "Backtest ABRIL 2026", EURUSD M1, 29 de abril de 2026, reloj del
  grafico en UTC+2 segun la exportacion) mientras explica. Transcrito con el pipeline de F04:
  `tr-v5-large-v3-int8-float16-01a1ae03` (99 segmentos, 318 s con habla, sin huecos >= 30 s) y
  extraido con el de F05: `fr-v5-718ecabb` (366 fotogramas, `huecos: []`, sin segundos
  ausentes). Lo que dice (cruda, hechos con marca; sin inferir reglas):
  - 0:00:01 "estoy bacteseando [backtesteando] el mes de abril de este ano... queria agregar
    algunas cosas, yo lo habia comentado con anterioridad".
  - 0:00:39-0:00:53 "aqui no hay entrada... porque no me genera el esquema 2 de entrada... sino
    que genera un flujo de ordenes, entonces esa entrada queda descartada".
  - 0:01:05-0:01:13 "aqui se cumple todas las condiciones, quita liquidez por encima de ese alto,
    lo hace con cuerpo".
  - 0:01:27-0:01:50 "yo lo marcaria desde aqui... si es desde aqui pues igual se toma la entrada
    y no pasa nada, se gana, se va a cumplir 13 [1:3]... pero yo lo tomaria desde aqui por el
    hecho de que al hacer mapeo estructural".
  - 0:01:56-0:02:58 "este decisional seria suficiente para validar una entrada aqui, pero ocurre
    que el precio llega, activa la entrada y se regresa... hay casos donde no llega hasta el 0.80
    ... en la mayoria de casos suele retroceder... no llega a romper ese nivel que seria el tope
    ... luego cae... cuando hay un equal [igual] que no lo vamos a poder anticipar porque se va a
    activar la entrada como tal, es una reentrada... contarlo como perdida, pero reentrar
    nuevamente si el precio te llega a romper nuevamente esta zona".
  - 0:03:21-0:03:30 "si yo protejo a 0.80, que es el SL por defecto, que no me permite dejarlo".
  - 0:03:34-0:04:23 "se activa la entrada... continua desarrollandose... nos mitiga y nuevamente
    seria cuestion de poner otra reentrada... lo validan los datos, no porque yo lo diga".
  - 0:04:27-0:04:47 "se cumplen las condiciones para poner break even... el precio sigue asi por
    caida ya lo podemos poner en BE... manejamos el calculo del RR en base al 1 %".
  - 0:04:56-0:05:23 "yo todo lo backtestee buscando el 1.3 [1:3]... existe la posibilidad de
    amplificar a 1.4 [1:4] el RR, pero creo que eso ya lo veremos mas adelante si es factible".
  - 0:05:27-0:05:59 "como esto es un igual... esperariamos a que el precio rompa por arriba para
    poder nosotros en la reentrada... sabemos de un flujo bajista... entrariamos aqui".
  Pantalla (fotogramas `fr-v5-718ecabb/240000` y `/355000`): caja con niveles 0 / 0,25 / 0,5 /
  **0,8** / 1 (no 0,75) sobre una vela bajista; lineas horizontales de liquidez en M1; zigzag de
  mapeo estructural dibujado a mano. Relacion con ambiguedades abiertas: A-10 (0,8 fijo frente a
  0,75 + spread: aqui dice "0.80, que es el SL por defecto"), A-7 (reentrada tras un igual /
  equal: contar la primera como perdida y reentrar si rompe de nuevo), A-4 (BE "cuando se cumplen
  las condiciones"), objetivo 1:3 con 1:4 como posibilidad futura (F21). No se decide nada aqui.
- **`backtesting-analytics ABRIL 2026.xlsx`** (papel `material_adicional`; misma estructura de
  22 columnas que enero y agosto): 38 operaciones EURUSD (OANDA) del 2026-04-01 al 2026-04-29,
  17 ganadoras, 19 perdedoras, 2 en cero; PnL +872 sobre 100 000; RR medio de las ganadoras
  3,64; 3 filas sin `initialSL`; horas de inicio entre las 05 y las 12 UTC. Para comparar: enero
  58 operaciones (18/36/4, +1102, RR 3,72), agosto 47 (20/22/5, +853, RR 3,33). Entrada de F07 y
  golden de F26 (fidelidad caso a caso), igual que los otros dos meses.
- **6 capturas** `WhatsApp Image 2026-09-05 at 2.30.5x PM*.jpeg` (papel `material_adicional`):
  pestana Analytics de FXReplay del "Backtest ABRIL 2026 - b7cd" (filtros long/short, wins/losses,
  Etc/UTC, 00:00-23:59): Total PnL $872, balance $100 872, win rate 47,22 %, 38 trades (17/19),
  breakeven 2; Average RR 3,64, Max RR 5,05, Ideal Average RR 19,88; Expectancy $22,95 (+30,58 /
  -7,63), Profit factor 4,01; ganadoras: mejor 0,14 %, media 0,07 %, duracion media 13 min, 5
  consecutivas; perdedoras: peor -0,05 %, media -0,01 %, duracion media 3 min, 6 consecutivas;
  por lado 47,4 % buy / 52,6 % sell; por hora (UTC) 5:00-12:00 con maximos a las 6:00 y 12:00;
  por dia: lunes 50 %, martes 25 %, miercoles 71,43 %, jueves 25 %, viernes 55,56 %; calendario
  con 2,37 trades/dia, 7,6/semana. Las cifras coinciden con el xlsx (38, 17/19/2, 872, 3,64).
- Cambios en el repo: `fuentes.yaml` (v5 y descripcion de la carpeta), `manifest.yaml`
  regenerado con `corpus inventory` (5 videos, 25 ficheros de material adicional),
  `knowledge/corpus/transcripciones/tr-v5-*.yaml`, `knowledge/corpus/fotogramas/fr-v5-*.yaml`,
  test de regresion del corpus real actualizado. `knowledge validate`, `transcript check` y
  `frames check` en verde con 5 videos. Deuda: v5 no esta en Drive (subirlo junto a los otros
  cuatro; `fuentes.yaml` lo declara) y su cruda entra en la copia pendiente de F07.

## Que deberia observar el usuario
`frames check` y `knowledge validate` en verde; `frames show --video v3 --t 0:28:56` devuelve
la referencia y la ruta del PNG; abrir ese PNG y leer `2,83` en la barra de formulas; los
cuatro manifiestos con `huecos: []`.

## Que casos funcionan
Todo el alcance del brief: cuatro videos a 1 fps sin perdida, indice y manifiesto inmutable por
video, obligatorios presentes y legibles, `show` con referencia citable y segmento de la
transcripcion, guardias (activa unica, inmutabilidad, historial, hook), `validate` barato.

## Que casos todavia no funcionan
- La evidencia aun no acepta `fr-<id>/<t_ms>`: `validar_contra_manifiesto` y el `comprobar`
  de `evidence new` siguen comparando contra las rutas de `manifest.yaml` (incluidas las
  heredadas). F07 anade el parametro alimentado por `referencias_conocidas` en los dos puntos
  y actualiza `knowledge/evidence/README.md`.
- `show` no abre la imagen: imprime la ruta.

## Limitaciones
Volver a un conjunto anterior de obligatorios (quitar uno con fraccion) reproduce el indice y el
id de un manifiesto ya reemplazado y `extract` lo rechaza: dejar el obligatorio en la lista o
aceptar que un `fr-*` reemplazado no vuelve a ser activo. `extraer_regulares` borra los PNG de la
carpeta antes de decodificar: si ffmpeg falla a medias, la siguiente pasada rehace todo (2-4 min).
8,9 GiB fuera de git: otra maquina valida esquema, historial y obligatorios pero no el indice
salvo que copie `data/fotogramas/` o re-extraiga (~10 min, mismo id si la build de ffmpeg
decodifica igual; si no, `extract` lo delata como error de inmutabilidad y la salida es otro
manifiesto con `--reemplaza-a`). `duracion_video_s` viene de ffprobe (en V4 difiere 9 ms del
WAV; aqui no importa: el fin del video se usa solo para rechazar obligatorios imposibles).

## Riesgos
Un cambio de build de ffmpeg cambia los hashes de PNG aunque los pixeles sean iguales (el
manifiesto lo delata). El hash de la etiqueta `Lavc` esta eliminado; el del decodificador no se
ha comparado entre builds. Los fotogramas no son evidencia: lo que se lee en ellos entra en
F07 con `extractor` y `reviewed_by`.

## Impacto sobre funcionalidades anteriores
`knowledge validate` suma una capa; el hook protege un directorio mas; `comun/ids.py` gana dos
patrones; `tests/integration/` deja de estar vacio; el test AST de ffmpeg restringe donde se
construye un argv de ffmpeg. Nada de F03/F04 cambia; la evidencia (F06) no cambia hasta F07.

## Auditoria de cierre (dos agentes: codigo/tests y docs/proceso)
CI en la rama: run 33992054088 (Ubuntu, ffmpeg de apt) verde sobre `af4b980`: la regla `select`,
`-copyts` y el clip con salto pasan en otra build de ffmpeg.

### Docs y proceso (agente, 2026-09-05)
Verifico contra los PNG y las crudas las cuatro lecturas de fotogramas y los siete pasajes de
audio de A-9 (coinciden); `state check`, `knowledge validate` y `frames check` en verde; ningun
commit toca `knowledge/spec` ni `knowledge/cases`; los cuatro `fr-*` con un solo commit; hook,
instalador y `.gitignore` correctos. Hallazgos aplicados: resolucion de v4 copiada mal en la
tabla (1898x1074 -> 1778x952); "9,1 GiB" era la suma de MiB dividida por 1000 (real: 8,9 GiB =
9,52 GB; corregido aqui, en PROJECT_STATE y en el README de corpus, que decia la estimacion de
7 GiB); `knowledge/corpus/fotogramas/` faltaba en Change Regimes de PROJECT_STATE; el brief
conservaba el texto JPEG bajo la decision PNG (nota anadida al alcance) y decia
`corpus.fotogramas.referencias_conocidas` y `<huella8>` donde el codigo tiene
`manifiestos_fotogramas.referencias_conocidas` y `png-1fps[-<huella8>]`; cabecera de
`fotogramas_obligatorios.yaml` sin `--reemplaza-a`; READMEs de tests y raiz sin `frames`; la
fila del Excel mezclaba hecho e inferencia (separados); la ficha de Word ya constaba como
contradiccion (dicho); "Que debe decidir" mezclaba ratificaciones con decisiones (etiquetado).
Anotado y no aplicado en la rama: HANDOFF desactualizado (se actualiza en el cierre, como en
F04); MASTER_PLAN H fila "cita de evidencia" no menciona `fr-<id>/<t_ms>` (lo trae el brief de
F07). No verificable desde fuera: la reescritura de las cuatro `huella.txt` durante la
construccion (declarada arriba).

### Codigo y tests (agente, 2026-09-05)
Leyo los modulos, ejecuto los tests, `lint-imports`, `validate`, `check` y siete experimentos
con ffmpeg sobre el clip y clips sinteticos; verifico en los cuatro `index.jsonl` reales que
`pts_ms == t_ms` en el 100 %, ningun segundo ausente y `n` consecutivos. Bugs confirmados y
corregidos en la rama (todos con test nuevo):
- A1 (alta) callejon sin salida en otra maquina u otra build: la carpeta de trabajo se elegia
  solo por marcas locales que no viajan en git; tras el error de inmutabilidad, `--reemplaza-a`
  chocaba con "no hay nada que reemplazar". Ahora `_carpeta_para` consulta ademas los
  manifiestos (huella recomputada desde `ffmpeg` + `extra`, y `sha256_video`) y abre otra
  carpeta; repetir la activa sin `--reemplaza-a` es idempotente y no error.
- A2 (media) `referencias()` fabricaba `fr-<id>/<t_ms>` para segundos sin fotograma (un salto
  de la fuente <= 2 s que se lleva un segundo entero no es hueco). Campo opcional
  `segundos_ausentes_ms` en el manifiesto (recomputado en `check`/`validate`); sin el campo
  el esquema exige cobertura densa (`n_regulares + ausentes == ultimo_pts_ms // 1000 + 1`),
  que los cuatro manifiestos reales cumplen sin cambiar (mismo esquema aceptado, no se
  editaron). Test con clip sintetico sin fotogramas entre 0,95 y 1,95 s.
- A3 (media) con `start_time != 0` el `pts` de `-ss -copyts` (absoluto) y el `t` de `select`
  (relativo) no comparten reloj: `extraer_video` lee `start_time` con ffprobe y rechaza el
  video si no es 0 (los cuatro reales lo son). Test con `-output_ts_offset 0.5`.
- A4/A5 (baja) traceback con un `fr-*.yaml` mal formado o un `index.jsonl` con un escalar:
  ahora `FotogramasError` (YAML estricto en las guardias).
- A7 (baja) `frames show` acotado por `duracion_video_s` del manifiesto.
- B1/B2 tests corregidos: el "empate" de `mas_cercanos` no era empate (ahora 1533 frente a
  1033/2033) y `show` con transcripcion prueba el borde exacto del segmento.
Documentado, no cambiado: A6 (volver a un conjunto anterior de obligatorios reproduce el
indice y el id de un manifiesto ya reemplazado: es una limitacion del id por indice; ver
Limitaciones); `extraer_regulares` borra los PNG de la carpeta antes de lanzar ffmpeg (pasada
no reanudable por diseno). Hipotesis no verificadas por el auditor: precision de `pts_time`
en `showinfo` de ffmpeg < 7 con `t >= 1000 s` (posible desvio de ms en extra; en ffmpeg 9 son
6 decimales); MP4 con `pts` negativo (fallaria ruidosamente).
CI tras la auditoria: run 33992911952 verde sobre `a118352` (Ubuntu, ffmpeg de apt).

## Que debe decidir el usuario
1. RATIFICAR (ya aplicado por su instruccion "maxima fidelidad sin restriccion de recursos";
   interpretada por el constructor como cobertura completa) el cambio de plan (tabla A fila F05
   y H.2): cobertura completa a 1 fps sin perdida; el concepto "tramo con decision" desaparece.
2. DECISION que anticipa al brief de F07: que el hallazgo del Excel (pantalla `2,83 / 3,3`; heredada `2,3 / 3,23`; large-v3
   `2.83 / 3.33`) y la ficha de reglas en Word (V3 0:01:41) entren en F07 como evidencia
   `modalidad: pantalla` y, lo que contradiga (2 frente a 3 cartuchos), como pregunta de F10.
3. DECISION de respaldo: copia de `data/fotogramas/` (8,9 GiB) fuera de esta maquina NO se
   propone (se regenera en ~11 min desde los videos, que si estan en Drive; sin los MP4 en
   `corpus/` no se puede regenerar); confirmar.
4. RATIFICAR: los candidatos A-9 se quedan como lista de hechos para F07 (el brief ya lo fijaba).

## Que puede comprobar sin recursos especiales
`make check`; `uv run botsito knowledge validate` (los cuatro manifiestos validan por esquema,
historial y obligatorios; sin `data/` avisa); `uv run botsito corpus frames check`; `git log --
knowledge/corpus/fotogramas/` (un commit, nunca editados). Con `data/fotogramas/` de esta
maquina: `frames show` sobre cualquier instante y abrir los tres PNG de la tabla; `frames extract
--video v1` termina en segundos ("indice ya completo"). Antes de commitear en esta maquina,
`make hooks` (el hook nuevo protege `knowledge/corpus/fotogramas/`).

## Estado
WAITING_FOR_USER_VALIDATION (ampliado el 2026-09-05 con el material adicional: v5 transcrito y
extraido, xlsx y capturas de abril en el corpus)
