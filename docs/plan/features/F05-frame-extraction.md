# F05 · frame-extraction

**Rama:** `feature/F05-frame-extraction` · **Fase:** 1 · **Depende de:** F03, F04

## Objetivo
Fotogramas con marca de tiempo de los cuatro videos del corpus, indexados y reproducibles, para
que F07 pueda citar lo que se ve en pantalla (Excel, herramienta de posicion, caja, configuracion
del grafico) igual que hoy cita lo que se oye (F04), y para que F08 responda "que hay en V4
0:44:56" con audio y fotograma. Incluye los fotogramas obligatorios de las marcas que F04 no pudo
verificar por audio. Los fotogramas heredados de Bot v2 (`_procesado/frames`, 29+118+78+113 con
huecos de hasta 11 min) se conservan como historia y no se citan (misma regla que la
transcripcion heredada).

## Decision de diseno: cobertura completa a 1 fps, no "tramos con decision"
El plan (tabla A, H.2) preveia extraccion densa solo en "tramos con decision" derivados de la
transcripcion mas los huecos heredados, y pedia que este brief fijara la regla (senales, palabras
clave, ventana). Antes de fijarla se midio sobre las cuatro crudas activas (`tr-*`) que fraccion
del video quedaria marcada por reglas razonables (segmento con palabra clave abre una ventana;
ventanas cercanas se fusionan):

| Regla | v1 (29 min) | v2 (69 min) | v3 (78 min) | v4 (94 min) |
|---|---|---|---|---|
| 25 palabras del dominio (entrada, stop, proteg-, break even, zona de control, cartucho, lotaje, caja, liquidez, mape-, limit, cierr-, riesgo, esquema, romp-, vela, sesgo, flujo, retroceso, pullback, objetivo, profit...), ventana ±10 s, fusion 20 s | 75 % | 46 % | 83 % | 77 % |
| Misma lista, ventana ±15 s, fusion 30 s | 86 % | 52 % | 90 % | 83 % |
| Deicticos (aqui, esto, este, mira, aca), ±10 s, fusion 20 s | 93 % | 56 % | 89 % | 85 % |
| Palabras del dominio + deicticos, ±15 s, fusion 30 s | 97 % | 79 % | 97 % | 99 % |

Hechos: (1) el trader habla del sistema casi todo el tiempo; el unico video con tramos "sin
decision" claros es V2, y son el bloque [MUSICA] 0:38-0:56 y el audio malo 0:58-0:59 ya
detectados por F04. (2) Coste medido de la cobertura completa (V3, 1762x884, ffmpeg 9,
`fps=1`, JPEG `-q:v 2`): 60 fotogramas = 9,3 MiB (159 KiB por fotograma) en 2,1 s. Extrapolado
a los 16 180 s de video: unos 16 200 fotogramas, ~2,5 GiB en `data/` (fuera de git) y ~10 min
de CPU. (3) El fotograma V3 0:28:56 en JPEG q=2 (176 KB) es legible cifra a cifra (ver
"Hallazgo durante el diseno"); el PNG del mismo instante pesa 470 KB. (4) Dos extracciones del
mismo instante dan el mismo sha256.

Inferencia: una regla de tramos ahorraria entre un 7 % (regla amplia) y un 29 % (regla
estricta) del disco, ponderado por duracion, a cambio de introducir
una frontera discutible ("quien declara el tramo", H.2) y de arriesgar que la evidencia de F07
caiga justo fuera. Decision propuesta: extraer TODO el video a 1 fps (sin huecos > 2 s en
ningun punto: el criterio de la tabla A se cumple globalmente), mas los instantes obligatorios
con precision de fotograma. El concepto "tramo con decision" desaparece de F05; si F07 o F08
necesitan priorizar, lo hacen desde la transcripcion. La deteccion de escenas del HTML original
("por escena y a 1 fps") tampoco hace falta: 1 fps la subsume. Es un cambio del plan (tabla A
fila F05 y H.2 fila F05) y por tanto decision del usuario (ver seccion final); si se acepta,
entra en el Change Log de MASTER_PLAN como hizo F04.

Hechos adicionales (ffprobe sobre los cuatro MP4, revision de diseno): `start_time = 0` en video
y audio, `r_frame_rate = avg_frame_rate`, `nb_frames` coherente con la duracion. El `t` del
video y el `t_ms` de la cruda comparten origen: es lo que hace comparable `fr-<id>/<t_ms>` con
`t0/t1` de la evidencia (ADR-0007 punto 7). Va al ADR-0008.

## Alcance cerrado (que SI)
Nota (auditoria de cierre): las menciones a JPEG `-q:v 2`, `%06d.jpg`, `<t_ms>.jpg`, "~2,5 GiB"
y "si otro obligatorio no se lee, PNG solo ese" quedaron superadas por la decision del usuario
(PNG sin perdida, 8,9 GiB reales; ver "Decisiones del usuario"). La funcion `referencias_conocidas`
vive en `corpus/manifiestos_fotogramas.py` y la carpeta de trabajo es `png-1fps[-<huella8>]`.
- `src/botsito/corpus/fotogramas.py` (puro salvo la llamada a ffmpeg, aislada):
  - Regla unica de seleccion, para regulares y obligatorios: "primer fotograma fuente con
    `t >= instante`". Regulares en una pasada con
    `-vf "select='isnan(prev_selected_t)+gte(floor(t),floor(prev_selected_t)+1)',showinfo"
    -fps_mode passthrough` (medido: da los fotogramas fuente con `t = n` exacto y conserva el
    `pts` original; `fps=1` NO sirve: elige el fotograma en `n + 0,47 s` y reescribe el `pts` a
    `0, 1, 2...`). Obligatorios con fraccion de segundo: `-ss <t> -copyts -i video -frames:v 1
    -vf showinfo` (sin `-copyts` el `pts` sale 0). Un obligatorio en segundo entero ES el regular
    (misma imagen, mismo hash): no se extrae dos veces.
  - `pts_ms` real parseado de `showinfo` (despues de `select`, no antes: en V4 serian 168 499
    lineas); `t_ms` nominal = `pts_ms // 1000 * 1000` para regulares, el instante pedido para
    obligatorios. ffmpeg escribe una secuencia `%06d.jpg`; Python renombra a `<t_ms>.jpg` con el
    `pts` parseado (el nombre no depende del patron de image2).
  - JPEG `-q:v 2` con `-fflags +bitexact -flags +bitexact` (sin la etiqueta `Lavc...`: el hash
    no cambia con la version del encoder; sigue dependiendo del decodificador H.264, no
    verificado entre builds), como el WAV de F04.
  - `plan_instantes(obligatorios_ms, ultimo_pts_ms)`: obligatorio mayor que el ultimo `pts`
    real o repetido = error (sin tolerancia: un fotograma que no existe no se cita). El numero
    esperado de regulares sale del ultimo `pts` real, no de `duracion_s` del manifiesto.
  - `Fotograma(n, t_ms, pts_ms, ruta, sha256, bytes, origen: regular | obligatorio)`;
    `index.jsonl` con ida y vuelta y rechazos; `huecos(index, umbral_ms)` sobre `pts_ms`
    consecutivos (`select` no fabrica fotogramas: un salto de la fuente se ve); umbral 2 s como
    constante tecnica con `# no-negocio` (el literal `2000` esta prohibido por el test de
    literales); `escribir_atomico` reutilizado de `transcripcion.py`.
  - Idempotente, no reanudable por tramos: una pasada por video son 2-3 min. El indice se
    escribe al final y de forma atomica; una interrupcion deja JPEG sin indice y la siguiente
    ejecucion rehace la pasada (`-y`, determinista). Si ya existe un manifiesto para esa carpeta,
    se compara `sha256_index` como F04 compara la cruda; distinto = error de inmutabilidad.
  - Carpeta de trabajo por huella (`data/fotogramas/<video>/<huella8>/`), con `video.sha256`
    como en F04: un video cambiado va a otra carpeta antes de decodificar.
- Manifiesto inmutable `knowledge/corpus/fotogramas/fr-<video>-<hash8>.yaml` (mismo regimen
  que `tr-*`: hook, `tests/contract`, `reemplaza_a`): `video_id`, `sha256_video`,
  `duracion_video_s`, `ffmpeg`, parametros (`fps`, `formato` (png), escala nativa), resolucion,
  `n_fotogramas`, `ultimo_pts_ms`, `sha256_index` (del `index.jsonl`, que vive en `data/`),
  `extra` (instantes con fraccion extraidos ademas de los regulares: `t_ms`, `pts_ms`, `sha256`),
  `huecos` (> 2 s sobre `pts`; el esquema los ACEPTA porque son un hecho medido, como
  `cortes_forzados_m` en F04; el criterio de aceptacion exige `[]` en los cuatro videos),
  `generado_el`. Sin campo `transcripcion`: los fotogramas no dependen de ella y el `tr-*` de
  hoy quedara reemplazado antes de F07 (glosario v2); `frames show` resuelve la activa al
  consultar. Exactamente un `fr-*` activo por video; un cambio de parametros (p. ej. una zona a
  mas fps) es una re-extraccion completa con `reemplaza_a` (10 min), no un manifiesto paralelo.
- `knowledge/corpus/fotogramas_obligatorios.yaml` (escrito a mano, versionado, sin regimen
  inmutable): lista `video_id, t, motivo, marca_heredada`; `knowledge validate` comprueba que
  cada uno existe en el indice del manifiesto activo (regular si es segundo entero, `extra` si
  no). Anadir un obligatorio en segundo entero no toca ningun manifiesto. Contenido inicial:
  - `v3 0:28:56` · Excel del trader: decide 2,3/3,23 (heredado) frente a 2.83/3.33 (large-v3).
  - `v2 0:33:21` · herramienta de posicion 4,08 / 3,94 (golden de F21).
  - `v4 0:12:30` · caja: nivel 0,75 = 1,19537.
  - V3 0:12:26 (marca heredada "huecos de fotogramas al dibujar sobre el mismo grafico") NO
    entra: era un defecto de la extraccion antigua, no un dato del trader; la cobertura completa
    contiene ese segundo y el informe lo anota como "cubierta".
  - Configuracion del grafico (A-9): no hay un instante conocido. Este brief NO inventa uno.
    F05 entrega (a) la cobertura completa, que incluye el eje de tiempo del grafico en
    cualquier fotograma con velas H4 visibles, y (b) en el informe, la lista de candidatos
    obtenida buscando en las crudas `hora`, `zona horaria`, `UTC`, `huso`, `configur`,
    `temporalidad`, `sesion`, `New York`, `Londres`, `Madrid`. Elegir el fotograma y registrar
    la evidencia es de F07 (H.2, fila "anclaje de la vela H4").
- CLI: `corpus frames extract --video v1 [--reemplaza-a fr-...]` (idempotente),
  `corpus frames check` (manifiestos contra `data/`: `sha256_index`, hashes de los obligatorios
  y de una muestra determinista de regulares, huecos), `corpus frames show --video v3 --t
  0:28:56 [--n 3]` (rutas de los fotogramas mas cercanos por `pts_ms`, con el segmento `n` de la
  transcripcion activa que cubre ese instante; `--t` fuera de duracion es error). `knowledge
  validate` gana la capa de fotogramas (esquema, historial de git, `reemplaza_a` resoluble y del
  mismo video, un activo por video, obligatorios presentes; si `data/fotogramas` no existe solo
  avisa, como con las transcripciones; NUNCA hashea los 16 000 JPEG: lee `index.jsonl`, ~2,5 MB).
- Modulo nuevo `manifiestos_fotogramas.py` sobre `comun/documentos.py` (`cargar_directorio`,
  `activos`, `ciclos_de_supersede`, `sha256_hex`), copiando la estructura de `cargar_todos` de
  transcripciones; no se reutiliza `manifiestos_transcripcion.py` (importa pipeline y glosario).
  `comun/ids.py` gana el patron `fotogramas` (`fr-<video>-<hash8>`) y `comun/historial.py` la
  constante `DIRECTORIO_FOTOGRAMAS`, que usan la guardia de historial y el test de contrato.
- `corpus.fotogramas.referencias_conocidas(repo) -> set[str]`: referencias citables de la forma
  `fr-<id>/<t_ms>` (`t_ms` nominal, tiempo de video) de TODOS los manifiestos `fr-*`, activos o
  reemplazados (un item que cito un `fr-*` luego reemplazado sigue siendo valido: el manifiesto
  es inmutable y no se borra), mas las rutas del manifiesto del corpus con papel
  `material_adicional` (FXReplay y capturas). `heredado_v2` queda EXCLUIDO explicitamente (hoy
  `validar_contra_manifiesto` acepta cualquier ruta de `ficheros`, incluidas las 477 heredadas:
  laxitud de F06 que F07 cierra con esta funcion). La firma de `evidence.validar_contra_manifiesto`
  NO cambia en F05 (evidence y corpus son hermanos independientes en el contrato de capas): F07
  anade el parametro y lo alimenta desde `validation/knowledge.py` y desde el `comprobar` de
  `evidence new` en `cli.py` (dos puntos, no uno), y actualiza el README de evidencia.
- Informe: tabla de los obligatorios con lo legible en cada uno (hechos, sin registrar evidencia:
  eso es F07), recuento por video, tiempo y disco reales, huecos (esperado: ninguno),
  determinismo verificado (re-extraer un minuto y comparar sha256), candidatos A-9.

## Fuera de alcance (que NO)
Registrar evidencia (F07). OCR o lectura automatica de cifras (los fotogramas se leen a mano en
F07). Deteccion de escenas. Recorte o realce de imagen. Fotogramas a mas de 1 fps. Video V4 partido en dos (era un artefacto heredado; el MP4 original es uno). Subir los
fotogramas a Drive (los 2,5 GiB se regeneran en 10 min desde los videos, que si estan en Drive).

## Entradas
Los cuatro MP4 del manifiesto F03 (v1 1920x1080 60 fps, 1752 s; v2 1898x1074 30 fps, 4134 s;
v3 1762x884 30 fps, 4676 s; v4 30 fps, 5617 s; tasa constante segun ffprobe), ffmpeg 9,
transcripciones activas `tr-*` (para `show` y el campo informativo), tabla de 33 marcas del
informe F04 (obligatorios), `EvidenceItem.fotogramas` (formato de referencia).

## Salidas (ficheros)
`src/botsito/corpus/fotogramas.py`, `src/botsito/corpus/manifiestos_fotogramas.py`,
`src/botsito/cli.py`, `src/botsito/validation/knowledge.py`, `src/botsito/comun/{ids,historial}.py`,
`scripts/git-hooks/pre-commit` (directorio `knowledge/corpus/fotogramas`),
`knowledge/corpus/fotogramas_obligatorios.yaml`, `knowledge/corpus/fotogramas/fr-*.yaml` (4),
`knowledge/corpus/README.md`, `tests/unit/test_fotogramas.py`,
`tests/integration/test_fotogramas_ffmpeg.py`, `tests/contract/test_fotogramas_history.py`,
`docs/adr/0008-fotogramas-cobertura-completa.md`, `docs/adr/README.md`,
`docs/validation/F05-frame-extraction.md`, `docs/plan/MASTER_PLAN.md` (tabla A, H.2, Change
Log). `data/fotogramas/` ya esta ignorado por `/data/*`.

## Tests
- Unit (puros, sin ffmpeg): `plan_instantes` (obligatorio mayor que el ultimo `pts` o duplicado
  rechazado; obligatorio en segundo entero no genera extra), `huecos` sobre `pts` (indice vacio
  = un hueco entero; falta de un segundo no es hueco; falta de tres si), JSONL ida y vuelta y
  rechazos (t negativo, sha mal formado, n repetido), esquema del manifiesto (campos, `huecos`
  no vacio se acepta, `reemplaza_a` del mismo video, un activo por video), id estable por
  contenido, parseo de `showinfo` (lineas ajenas ignoradas, `pts_time` a ms), nominal desde
  `pts`.
- Integracion (ffmpeg, fixture `tests/fixtures/clip_2s.mp4`, 10 fps, copiado a un nombre con
  acento como los reales): regulares con `pts_ms` EXACTOS (`0`, `1000`, `2000`), no solo "dentro
  del clip"; obligatorio `0:00:01.25` con `pts_ms == 1300`; obligatorio `0:00:01` byte-identico
  al regular (mismo sha256: es lo que sostiene "no se duplica"); JPEG sin etiqueta `Lavc`;
  dos ejecuciones dan sha256 identicos (misma maquina: la CI usa el ffmpeg de apt, sin goldens
  de hash); segunda ejecucion no decodifica ni reescribe (mtime intacto); `extract` con
  manifiesto existente e indice distinto = error de inmutabilidad; fixture con salto (clip
  filtrado quitando 1,5 s y remuxado) produce hueco > umbral en indice y manifiesto; `check`
  detecta fotograma alterado, borrado y `index.jsonl` editado; `show` devuelve el mas cercano
  por `pts`, error fuera de duracion, y el segmento de una transcripcion `MotorFalso` con
  `t0 == t1` en borde de segmento; `referencias_conocidas` incluye `fr-*/t_ms` de manifiestos
  activos y reemplazados y `material_adicional`, excluye `heredado_v2`; CLI `extract`, `check`,
  `show`; `knowledge validate` con la capa nueva, y sin `data/fotogramas` AVISA (no error);
  obligatorio ausente del indice activo = error; ffmpeg ausente = error explicito.
- Contrato: historial de git de `knowledge/corpus/fotogramas/` (modificar o borrar un `fr-*`
  se detecta); test AST: el literal `"ffmpeg"`/`"ffprobe"` como argumento de `subprocess` solo
  en `corpus.audio`, `corpus.inventario` y `corpus.fotogramas` (no "solo estos importan
  subprocess": `cli`, `comun.historial` y `motor_whisper` tambien lo usan).
- Real (no en CI): cuatro videos extraidos; muestra determinista de 20 fotogramas por video
  re-extraida con `-ss -copyts` y la MISMA regla `select`, comparada por hash en el informe
  (verificado en la revision que asi da los mismos fotogramas fuente que la pasada completa).

## Criterio de aceptacion
`make check` verde; los cuatro videos con manifiesto `fr-*` inmutable y `huecos: []`; todos
los obligatorios de `fotogramas_obligatorios.yaml` (los tres de H.2 mas los que decida el
usuario) presentes en el indice activo, con `pts_ms == t_ms` pedido y legibles (tabla en el
informe); `frames show` responde para cualquier instante de los cuatro videos; muestra de
re-extraccion identica por hash; material heredado intacto; ADR-0008 con la medida de cobertura
que justifica la cobertura completa; lista de candidatos A-9 en el informe.

## Riesgos
- Disco: ~2,5 GiB en `data/fotogramas/`. Mitigacion: fuera de git, regenerable en ~10 min;
  `check` avisa si falta.
- Determinismo del JPEG: con bitexact el hash no depende de la version del encoder, pero si
  del decodificador H.264 de la build (no verificado entre builds). Otra build con otro hash es
  otro manifiesto con `reemplaza_a` (mismo tratamiento que otra GPU en F04). `pts_ms` y nominal
  no dependen de la build.
- Video de tasa variable: ffprobe reporta tasa constante en los cuatro; si la fuente tiene
  saltos, `huecos` sobre `pts` los registra en el manifiesto y el informe los lista.
- `showinfo` por stderr: ~16 000 lineas por video (~3 MB); F04 ya captura stderr completo con
  `silencedetect`.
- V4: `duracion_video_s` (ffprobe) y el WAV difieren 9 ms (F04); F05 usa la del video.
- Excel y herramienta de posicion con cifras pequenas: legibilidad verificada a q=2 en V3
  0:28:56; si otro obligatorio no se lee, se extrae en PNG solo ese instante (campo `formato`
  en la lista de obligatorios) y se dice en el informe.

## Hallazgo durante el diseno (hecho, pendiente de F07)
Al medir la legibilidad se extrajo V3 0:28:56. Se ve el Excel del trader con la celda C11
seleccionada y la barra de formulas mostrando `2,83`; la fila 11 (23-abr-26) muestra `2,83`
y `-0,75`, la fila 12 (24-abr-26) `-0,5`, `3,3`, `-0,75`, `-0,5`. Es decir: large-v3 acierta
en 2,83 (la heredada decia 2,3) y la tercera cifra es 3,3 (ni 3,23 heredado ni 3,33 de
large-v3). No se registra como evidencia aqui: F07 lo hara citando `fr-v3-.../<t_ms>`.

## Revision de diseno (agente, 2026-09-05, antes de programar)
El revisor leyo plan, ADR, codigo y contrato de capas y ejecuto experimentos con ffmpeg sobre un
clip sintetico y sobre los MP4 reales. Veredicto: listo con cambios (sin rehacer). Todo lo
aceptado ya esta aplicado en las secciones anteriores.

Aceptados (bloqueantes):
- A1 `fps=1` elige el fotograma en `n + 0,47 s`, distinto del de `-ss n`; "no se duplica"
  sustituiria en silencio el exacto. Verificado tambien sobre V3 (hashes distintos).
  Regla unica `select` "primer fotograma con `t >= n`" + `-fps_mode passthrough`.
- A2 `showinfo` tras `fps` y `-ss` sin `-copyts` no dan el `pts` real (salia 0, 1, 2...):
  los tests de `pts_ms` habrian pasado sin probar nada. Verificado. Corregido con `select` y
  `-copyts`; tests con valores exactos.
- A3 `huecos` sobre un indice de `fps` era vacuo (ffmpeg duplica para rellenar) y el esquema
  que rechaza `huecos` contradecia "el informe lo lista". Ahora sobre `pts`, esquema que
  acepta, aceptacion que exige `[]`, literal `2000` con `# no-negocio`.
- A4 `referencias_conocidas` incluia rutas heredadas que el propio brief dice que no se citan.
  Excluido `heredado_v2`; incluidos `material_adicional` y manifiestos reemplazados.
- A5 "cinco obligatorios" no existian. Criterio reformulado.
- A6 Faltaban `comun/ids.py`, `comun/historial.py`, `docs/adr/README.md`, MASTER_PLAN;
  sobraba `.gitignore`.
- A7 Test AST sobre `subprocess` fallaria de partida (cli, historial, motor_whisper lo usan).
  Reformulado sobre el literal `"ffmpeg"`.
Aceptados (diseno): B1 bitexact; B2 nombre por `pts` parseado, no por patron de image2; B3
obligatorios fuera del manifiesto inmutable (lista mutable validada contra el indice activo);
B4 sin campo `transcripcion`; B5 un `fr-*` activo por video, cambio de parametros =
re-extraccion completa; B6 modulo nuevo sobre `comun/documentos`; B7 idempotente con indice
atomico al final; B8 ultimo regular por `pts` real, sin tolerancia en obligatorios; B9
`validate` no hashea JPEG; B10 test con nombre acentuado; B11 `showinfo` tras `select`; B12
ahorro corregido a 7-29 %; B13 relojes al ADR-0008; C1-C11 tests.
Decisiones (seccion D): la 1 se reformula como cambio de plan con Change Log; la 2 (V3 0:12:26)
se retira porque la evidencia la decide; la 3 (Excel) se remite al bloque de preguntas de F10
junto a 40 %/50 %; se anaden B1, B3 y B5 porque afectan a F07.
Descartados: ninguno. No verificado por el revisor: las fracciones de la tabla de cobertura
(script en el scratchpad de esta sesion; se reproducira en el informe), la legibilidad del Excel
(vista en esta sesion), el determinismo del decodificador entre builds, el `MASTER_PLAN.html`.

## Decisiones del usuario (2026-09-05)
Instruccion literal: "aplica lo que tenga mayor eficacia y porcentaje de fidelidad para extraer
todo lo necesario, no importa el tiempo o cantidad de recursos que demande". Se aplica asi:
1. Cobertura completa a 1 fps (decision 1 aceptada; cambio de plan al Change Log).
2. Formato SIN PERDIDA: PNG en lugar de JPEG q=2. Medido en V3 con la regla `select` y
   bitexact: 60 fotogramas = 26 MiB en 1,4 s (~7 GiB y ~10 min para los cuatro videos; 179 GB
   libres en disco); dos extracciones dan el mismo sha256. La legibilidad deja de depender de la
   calidad JPEG y el riesgo "si otro obligatorio no se lee, PNG solo ese" desaparece.
3. Decisiones 2, 3 y 4 (un `fr-*` activo por video, obligatorios en lista mutable, bitexact):
   aceptadas tal como estan, porque ninguna reduce fidelidad y las tres la protegen.
4. Instantes obligatorios con precision de fotograma (regla `select`, `-ss -copyts`).
Lo que sigue abajo es la lista de decisiones tal como se planteo antes de la instruccion.

## Que debe decidir el usuario (planteado antes de la instruccion anterior; resuelto)
1. Cambio de plan: cobertura completa a 1 fps (~2,5 GiB fuera de git, ~10 min) en lugar de
   "tramos con decision" (tabla A fila F05 y H.2). Ahorro medido de la alternativa: 7-29 %.
   Si se acepta, entra en el Change Log de MASTER_PLAN.
2. Un solo `fr-*` activo por video; una zona a mas fps seria re-extraccion completa con
   `reemplaza_a`, nunca un manifiesto paralelo (afecta a como F07 cita).
3. Obligatorios fuera del manifiesto inmutable: lista mutable `fotogramas_obligatorios.yaml`
   validada contra el indice activo; anadir uno en segundo entero no genera manifiesto nuevo.
4. Bitexact como parte de la promesa de reproducibilidad (el hash no cambia con la version del
   encoder; si con el decodificador de otra build).
El hallazgo del Excel (2,83 / 3,3) no se decide aqui: va al bloque de preguntas de F10 con el
40 %/50 % de A-12.

## Que habilita
F07 (evidencia `modalidad: pantalla` con al menos una referencia `fr-<id>/<t_ms>` o
`material_adicional`; `validar_contra_manifiesto` y el `comprobar` de `evidence new` ganan el
parametro de referencias conocidas; README de evidencia actualizado; resolucion de A-9 con la
configuracion del grafico; golden 4,08/3,94 para F21; Excel 2,83/3,3), F08 (`at v4 0:44:56`
con fotograma mas cercano), F10 (casos ilustrados con el fotograma del trader).
