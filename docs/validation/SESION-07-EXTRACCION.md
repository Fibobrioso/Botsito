# Sesión 7a con el trader: la extracción por pregunta y por sesión del bloque de días

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras, en
> `PREGUNTAS-7B.md`, en `SESION_EN_CURSO` ni en la hoja de ruta (R4.3 sigue ABIERTA). Cada
> «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de cada respuesta lo
> decide el consultor en la rama de activación de la 7a (encargo del 2026-11-17,
> `docs/encargos/trabajo-sesion-07.md`).

Rama `trabajo/sesion-07`, abierta el 2026-11-17 desde `main` en `ed5f9eef` (commit de estado sobre
el merge `0f420593`, tag `stable/F39c-skills-metodo`). Tramo R4 de la hoja de ruta (R4.3, NA:F).
Skill `ingerir-sesion`, de principio a fin, y ADR-0093 §2. Plantilla: `SESION-06-EXTRACCION.md`.
Tag de cierre previsto: `stable/F39d-sesion-07` (no existe ni en local ni en origin:
`git tag -l` y `git ls-remote --tags origin` vacíos).

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse main origin/main` da dos veces `ed5f9eef606488417d3a305a29714b4407cb3304`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F39c-skills-metodo`;
  `git rev-parse "stable/F39c-skills-metodo^{commit}"` = `git rev-parse main^1` =
  `0f420593008338e5140747443bee673df00ee81a`; `git ls-remote --tags origin` da
  `4691f0eb… refs/tags/stable/F39c-skills-metodo` (el objeto del tag anotado) y su `^{}`,
  `0f420593…`. Es también el primero de `git tag -l 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 43654960018`: `completed`,
  `success`, `headSha` `ed5f9eef606488417d3a305a29714b4407cb3304`, `push` en `main`.
- `git branch -a` solo da `main` y `origin/main`; `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"07": {` en la línea 251 de
  `CODIGOS_DE_SESION_TEXTO`, con 6 textos que son los títulos de S-1 a S-6 de
  `docs/sesion-7/PREGUNTAS-7A.md` (líneas 85, 125, 160, 192, 229 y 267) con la primera letra en
  minúscula; `"07": ORDEN_SESION_07` en `HOJAS` (línea 276); `SESION_EN_CURSO = "07"` (línea 281).
- `PROJECT_STATE.md` tras abrir: 23.519 bytes (`wc -c`; 23.428 en `main`).

## Decisiones de proceso de la rama

- Al buscar el contrato de `trabajo/sesion-06` como modelo, la guardia negó (solo lectura) un bucle
  `git log ... | while read h; do git show $h:contrato.yaml ...; done`: «`read` fija `h`, que no esta
  en la lista cerrada (`NOMBRES_DE_ENTORNO`)». Seguí la forma que propone su mensaje (sin `$(...)`,
  detrás solo `grep`/`head`): `git log --all --full-history --format='%h %s' -- contrato.yaml | grep
  -i 'abre trabajo/sesion'` y `git show 6c96499a:contrato.yaml` (`docs/runbooks/DECISIONES-DE-PROCESO.md`).
- La guardia negó `uv run botsito state check ...; uv run python scripts/contrato_rama.py ...` en un
  solo comando («antes, en el mismo comando, va `uv run botsito state check`»), y lo mismo con
  `git diff --quiet main -- scripts/transcribir_sesion.py` delante de `transcribir_sesion.py --help`;
  seguí su forma: una llamada por ejecutable. Y negó, en la ruta de un `cat`, un nombre de fichero
  montado con `$(ls ...)` (solo lectura, un ítem de evidencia de v17 como modelo): seguí su forma, la
  ruta literal y Read.
- **El primer `make check` de la apertura salió en rojo y sin sello** (exit 2; `1 failed, 3512
  passed, 6 xfailed in 1173.28s`): `tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths`,
  «rutas ignoradas no previstas: ['.claude/settings.local.json']». La causa: un
  `.claude/settings.local.json` de 298 bytes creado FUERA de esta sesión el 2026-11-16 a las 21:30
  (unas reglas `deny` de un MCP ajeno al proyecto). No lo toqué ni amplié el test (fuera del
  contrato): PARADA. Aleks lo resolvió sacándolo del repo. Primero dijo que ya lo había movido a su
  Escritorio, pero el fichero seguía en el repo con la misma hora; con su autorización expresa busqué la
  copia solo en el primer nivel de `C:\Users\USER\Desktop` (ni `settings.local.json` ni ningún
  `.json`; ninguna carpeta abierta) y, al no encontrarla, no borré nada: lo moví a
  `C:\Users\USER\Desktop\respaldo-settings\settings.local.json` (298 bytes, la misma hora) por orden
  suya, y comprobé que ya no está en el repo. Después, el sello de apertura se relanzó con lo mismo
  estadiado más estas líneas y la desviación de 0.1.

- **Ninguna herramienta de NotebookLM ni de Gemini Notebook** (`nlm`, `notebooklm-mcp`,
  `mcp__gemini-notebook-mcp`) en esta rama: nada del repo ni del corpus sale a un servicio externo;
  si alguna vez parece que hace falta, PARADA (orden de Aleks del 2026-11-17, tras sacar del repo el
  `settings.local.json` que las denegaba). Ninguna se usó.

## 0. Lo primero

### 0.0 Las respuestas de Aleks a las preguntas a) a d) del encargo (2026-11-17), copiadas tal cual

Llegaron en un solo mensaje, antes del registro. Copiadas tal cual, **salvo los paréntesis con
cuántas láminas se enseñaron de cada sesión**, que el encargo manda no escribir en ningún fichero
(REGLAS DE ESTA RAMA): van sustituidos por «[recuento de láminas: solo en el terminal]».

> Respuestas a las preguntas del encargo, por vídeo.
>
> VÍDEO 1 (v18, primer día)
> a) No salió nada en pantalla que no tocara: solo los esquemas inventados del PDF, el replay de cada sesión del bloque abierto por el trader y las láminas. El trader no habló de operaciones de días fuera de construcción ni dio cifras de resultados de su cuenta.
> b) Las seis preguntas, en orden: S-1, S-2, S-3, S-4, S-5 y S-6, todas hechas. Frases de «Para confirmar al final»: no estoy seguro de si se leyeron; compruébalo en la transcripción. Bloque de días: sesión 1 (7 de julio, 11-15) y sesión 2 (2 de julio, 11-15), en ese orden. Minuto en que empieza cada una: no lo sé; localízalas por la voz. Si el trader abrió el replay antes de compartir pantalla: no estoy seguro, así que no abras ningún fotograma de esos arranques. Láminas enseñadas (solo para el terminal): las de su carpeta, sin saltarme ninguna que yo recuerde [recuento de láminas: solo en el terminal].
> c) El trader no ha contestado nada por WhatsApp.
> d) No tengo hoja de notas.
>
> VÍDEO 2 (v19, segundo día)
> a) No salió nada en pantalla que no tocara, igual que en el primero.
> b) Ninguna pregunta técnica. Bloque de días: sesión 3 (3 de julio, 07-11), sesión 4 (15 de julio, 11-15) y la reserva del 13 de abril (07-11), en ese orden. La reserva del 6 de julio no se hizo. Minuto en que empieza cada una: no lo sé; localízalas por la voz. Si el trader abrió el replay antes de compartir pantalla: no estoy seguro, así que no abras ningún fotograma de esos arranques. Láminas enseñadas (solo para el terminal): las de su carpeta, sin saltarme ninguna que yo recuerde [recuento de láminas: solo en el terminal].
> c) Nada por WhatsApp.
> d) No tengo hoja de notas.

Y, preguntado después por los silencios del audio (§2.1) y por el paso 1 de «Antes» (§0.1), el
mismo día: «los silencios son porque el trader se fue al baño o simplemente no habló, en todo
momento el audio estuvo claro y no cortado»; y, a si comprobó los dos días antes de grabar, «nou».

Contraste con lo que el encargo anticipaba («ENTRADAS», b): cuadra. v18 lleva el bloque técnico y
las sesiones 1 y 2; v19, las sesiones 3 y 4 y la reserva del 13 de abril; la reserva del 6 de julio
no se hizo. Las cinco sesiones son las de la tabla de `PREGUNTAS-7A.md` §1 (orden 1 a 4 y la
primera reserva). Sin hoja de notas (d): nada entra en `corpus/.../Sesiones/`. Nada por WhatsApp
(c): ninguna captura nueva en «Mensajes del trader».

### 0.1 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-16`: `False`.
- `2026-11-17`: `False`.

**Desviación del paso 1, declarada**: según Aleks (2026-11-17), los dos días NO se comprobaron antes
de grabar; se comprobaron hoy, después, por la sesión. Declarada también en
`HOLDOUT-EXPOSICIONES.md` (2026-11-17). Precedente: `SESION-06-EXTRACCION.md` §0.2.

### 0.2 Los vídeos

Son los dos únicos vídeos del primer nivel de `corpus/Estrategia del trader/` que no estaban en
`fuentes.yaml`, que acababa en v17:
- `Grabación de pantalla 2026-11-16 145418.mp4`, 7.507.070.830 bytes (v18, el primer día);
- `Grabación de pantalla 2026-11-17 135357.mp4`, 6.332.347.809 bytes (v19, el segundo día).

La Next Action F daba la 7a para el domingo 2026-11-15: se grabó el 2026-11-16 y el 2026-11-17, y el
id de la sesión es `2026-11-16-sesion-07` (el del primer día; encargo, ENTRADAS). La orden de cierre
lo recoge.

## 1. El registro (v18 y v19)

- `knowledge/corpus/fuentes.yaml`: v18 (`2026-11-16`, 1:52:26) y v19 (`2026-11-17`, 1:35:55), los
  dos con `drive_id: null`, su `fecha_grabacion` (del nombre del fichero) y una `naturaleza` que
  empieza por «sesion» y describe el vídeo entero, también el bloque de días (el replay de FX Replay
  que abre el trader y las láminas del bot), sin número de láminas ni carpetas; la procedencia, en
  el comentario. Id de sesión de los dos: `2026-11-16-sesion-07`.
- `tests/unit/test_inventario.py`: `esperados = [f"v{n}" for n in range(1, 20)]` (era
  `range(1, 18)`, línea 171).
- v18 y v19 en `SESIONES_EN_CUARENTENA` (`src/botsito/corpus/cuarentena.py`), en el conjunto
  literal de `test_contra_el_repo_real_ve_lo_mismo_que_el_codigo` (`tests/unit/test_guardia_claude.py`,
  línea 152; el sintético de la 146 no se toca) y en el dict `reales` de
  `test_la_comprobacion_de_la_lista_no_es_decorativa` (`tests/unit/test_cuarentena.py`), cuya sonda
  «sesión sin listar» pasa de v18 a v20.

### 1.1 Los tests rotos a propósito

Con v18 y v19 ya en `fuentes.yaml` y ANTES de añadirlos a `SESIONES_EN_CUARENTENA`:

```
uv run pytest tests/unit/test_cuarentena.py \
  "tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena" \
  "tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo" --tb=no
F.......................................FF                               [100%]
FAILED tests/unit/test_cuarentena.py::test_la_lista_cuadra_con_fuentes - Asse...
FAILED tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena
FAILED tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo
3 failed, 39 passed in 6.11s
```

Los mensajes: `'v18: es una sesion (drive_id null) y no esta en SESIONES_EN_CUARENTENA ni en
EXCEPCIONES'` («Left contains 2 more items»: v18 y v19), y en los dos de la guardia, «Extra items in
the left set: 'v19' 'v18'» (la guardia los deduce ya de `fuentes.yaml`, el módulo todavía no los
lista). Fallaron tres, como en la sesión 6 (`SESION-06-EXTRACCION.md` §1.1).

Después del alta, el mismo comando:

```
..........................................                               [100%]
42 passed in 7.37s
```

### 1.2 Inventario y hashes

- `uv run botsito corpus inventory`: «OK: manifiesto escrito · heredado_v2: 477 ficheros,
  117,626,282 bytes · material_adicional: 73 ficheros, 6,850,662 bytes · video_original: 19
  ficheros, 85,187,627,433 bytes». El diff de `manifest.yaml` solo añade v18 (sha256
  `7af418e4…`, 6746,4 s) y v19 (sha256 `cb57ad69…`, 5755,52 s) y sube el recuento de vídeos de 17 a 19;
  el material adicional no cambia.
- `uv run botsito corpus check --hashes`: «OK: el corpus coincide con el manifiesto (hashes)».

## 2. Audio, cuarentena y holdout

### 2.1 Los cortes de audio

Con las formas exactas del paso 2 de la skill `ingerir-sesion`, sin ninguna negativa de la guardia:

| Vídeo | ffprobe | volumedetect (medio / máximo) | silencedetect a -50 dB y 30 s |
|---|---|---|---|
| v18 | 6746,4 s (1:52:26), h264 1920x1080 a 30 fps, AAC estéreo a 48 kHz | -22,7 dB / -0,1 dB | uno: 2429,3 s a 2470,3 s (41,0 s) |
| v19 | 5755,5 s (1:35:55), h264 1898x1080 a 30 fps, AAC estéreo a 48 kHz | -24,0 dB / -0,2 dB | cinco: 1612,3–1675,4 s (63,2 s); 2696,9–2747,4 s (50,5 s); 2919,2–2958,3 s (39,1 s); 5578,5–5656,3 s (77,8 s); 5661,6–5694,3 s (32,7 s) |

Según Aleks (§0.0), los silencios son pausas: el trader se ausentó o no habló, y el audio no se
cortó. Los seis entran en `knowledge/corpus/tramos_no_citables.yaml` con motivo «SIN AUDIO»
(segundo inicial hacia abajo y final hacia arriba, como los de v17): v18 0:40:29–0:41:11; v19
0:26:52–0:27:56, 0:44:56–0:45:48, 0:48:39–0:49:19, 1:32:58–1:34:17 y 1:34:21–1:34:55. La puerta del
ASR (ningún segmento con `t1` dentro de un corte), tras cada transcripción (§2.2).

El audio de cada vídeo, extraído FUERA del repositorio y de cualquier carpeta que lo contenga, para
`transcribir_sesion.py --audio`: `C:\Users\USER\Desktop\sesion-07-audio\sesion-07-v18.wav`
(210.825 KiB) y `sesion-07-v19.wav` (179.860 KiB), mono a 16 kHz.

### 2.2 v18: transcripción, cuarentena y puerta del ASR

Aleks dejó dado su «listo» para las dos transcripciones antes de ausentarse (mensaje del
2026-11-17: programas pesados cerrados, una transcripción cada vez, ninguna junto a un `make check`).
Cada orden, medida con `scripts/pico_memoria.py ejecutar` (el medidor de `make check`).

- **Transcripción del corpus**: `uv run botsito corpus transcribe --video v18` →
  `tr-v18-large-v3-int8-float16-ba2d4fca`, **1320 segmentos**; PICO DE MEMORIA **5532 MiB** (suma de
  sus procesos; el mayor, 5481 MiB). `corpus transcript check`: `OK: 25 transcripciones coherentes
  con el disco y el glosario`.
- **El guion de `main`** (`git diff --quiet main -- scripts/transcribir_sesion.py`: exit 0,
  idéntico): `--audio C:/Users/USER/Desktop/sesion-07-audio/sesion-07-v18.wav --sesion 07 --video
  v18`, después y nunca a la vez; PICO DE MEMORIA **5499 MiB** (el mayor, 5448 MiB). El registro
  (`sesion-07-v18.registro.txt`, fuera del repositorio) dice:
  - hoja: la de la sesión 07; tramos no citables del vídeo: 1 (el silencio);
  - audio comprobado: el sha256 de su WAV (`7e29f2836bcd…`) es el de la transcripción del corpus de v18;
  - ASR de 1349,1 s (factor 0,20), en cuda; **1320 segmentos**, los mismos que la del corpus;
  - **segmentos en cuarentena: 15 en 4 bloques**; tapados solo por meses 15, solo por tramos 1, por
    ambos 0; bloques `[NO CITABLE]`: 1; motivos «fecha numérica» 6 y «vecino» 9;
  - códigos detectados: S-1 00:10, S-2 09:57, S-5 27:40 y S-6 34:28; sin código detectado, S-3 y
    S-4 (cómo se localizaron, §3).
- **La puerta del ASR del silencio.** El guion tapó **1** segmento por el tramo (bloque
  `[NO CITABLE 40:05–41:17]`): empieza antes del corte (0:40:29–0:41:11) y acaba después, a las
  41:17, así que **ningún segmento tiene `t1` dentro del corte**. El segmento entero queda tapado en la
  filtrada, aunque solo su parte central es «SIN AUDIO»; no se cita.
- **Los cuatro bloques de cuarentena, a `tramos_no_citables.yaml`**, sin contenido y en el commit
  de este vídeo, con el fin de cada uno más un segundo («Los límites de un tramo»):
  **0:52:04–0:52:15**, **0:57:52–0:58:14**, **1:09:09–1:09:16** y **1:51:08–1:51:39**. Control
  positivo: cada bloque cabe entero en su tramo. El segundo de margen toca la primera línea visible
  tras el bloque en tres de ellos (`[52:14]`, `[58:13]` y `[69:16]`), que por eso tampoco se citan.

### 2.3 v18: el barrido, antes de leer

Con `scripts/barrido_dias.py` de `main`, antes de leer una sola línea de la filtrada de v18:
- **Del 1 al 31: 155 líneas** con un entero suelto: horas, cantidades, números de lámina y de
  esquema, niveles, y los días que se dicen en voz. Los que llevan mes son todos de julio, y la
  pasada por defecto dice que ninguno cae del 18 al 31.
- **Rango por defecto (18 a 31): 4 líneas**, `[50:02]` («de [N] y tantos», una cantidad),
  `[86:46]` (una hora con minutos), `[99:12]` y `[111:00]` (recuentos). **Ninguna es un día.**

**Sin PARADA por el barrido**: todos los días con mes que se dicen en voz en v18 son de julio del 1 al
17, de construcción. Los que sitúan el bloque, visibles en la filtrada: «el 7 de julio» (`[39:28]`,
la sesión 1) y «el día 2 de julio» (`[63:15]` a `[66:18]`, la sesión 2). Una línea de la
presentación de la sesión 2 lleva, junto al día, un número que puede identificar una carpeta de
láminas: **no se copia** a ningún fichero ni se cita (encargo, «REGLAS DE ESTA RAMA»; lecciones de
`trabajo/preparacion-sesion-7`).

### 2.4 v19: transcripción, cuarentena, puerta del ASR y barrido

Lanzada sin esperar a Aleks tras el commit de v18 (su «listo» dado de antemano), sola y sin ningún
`make check` a la vez.

- **Transcripción del corpus**: `uv run botsito corpus transcribe --video v19` →
  `tr-v19-large-v3-int8-float16-d6b9cc45`, **979 segmentos**; PICO DE MEMORIA **5533 MiB** (el mayor,
  5482 MiB). `corpus transcript check`: `OK: 26 transcripciones coherentes con el disco y el glosario`.
- **El guion de `main`** (idéntico: `git diff --quiet main -- scripts/transcribir_sesion.py`, exit 0)
  con `--audio C:/Users/USER/Desktop/sesion-07-audio/sesion-07-v19.wav --sesion 07 --video v19`;
  PICO DE MEMORIA **5532 MiB** (el mayor, 5482 MiB). El registro dice: hoja de la sesión 07; tramos no
  citables del vídeo: 5 (los silencios); el sha256 del WAV (`3754a953fc77…`) es el de la transcripción
  del corpus; ASR de 961,9 s (factor 0,17); **979 segmentos**; **8 en cuarentena en 3 bloques**
  (solo por meses 8, solo por tramos 5, ambos 0; bloques `[NO CITABLE]`: 4; motivos «fecha numérica» 3
  y «vecino» 5); **ningún código detectado**, como se esperaba (v19 no lleva preguntas técnicas).
- **La puerta del ASR de los cinco silencios**, por los bloques `[NO CITABLE]` (marca = principio del
  primer segmento y fin del último, al segundo):
  - `[26:12–28:07]` cubre el silencio 26:52–27:56: su segmento acaba en 28:07, fuera. Pasa.
  - `[45:47–45:48]`: un segmento de un segundo que empieza dentro del silencio 44:56–45:47,4 y acaba en
    el segundo 45:48, ya fuera (el silencio acaba en 2747,37 s). Pasa.
  - `[48:20–49:24]` cubre el silencio 48:39–49:19: acaba en 49:24, fuera. Pasa.
  - `[94:15–94:16]`: un segmento de un segundo al final del silencio 1:32:58–1:34:16,3 (5656,28 s).
    Con la resolución de la filtrada (el segundo) **no se puede decir si su `t1` cae dentro**: acaba
    en el segundo 94:16, y el silencio acaba a las 94:16,28. Si cae dentro, es un segmento del ASR
    sobre silencio; está tapado entero y no se cita. Se dice, sin leer la cruda.
  - El silencio 1:34:21–1:34:55: ningún segmento (la línea siguiente es `[94:59]`). Pasa.
- **Los tres bloques de cuarentena, a `tramos_no_citables.yaml`**, con el fin más un segundo:
  **0:00:00–0:00:07**, **0:14:18–0:14:39** y **1:03:40–1:03:48**. Las líneas `[00:07]`, `[14:38]` y
  `[63:47]` caen en el segundo de margen y tampoco se citan. **El primero tapa el arranque del vídeo,
  donde se dice el día de la sesión que abre v19** (§4.3, PARADA 2).
- **El barrido**, antes de leer: del 1 al 31, **137 líneas**; por defecto (18 a 31), **4 líneas**
  (`[09:36]` un recuento, `[17:46]` y `[17:47]` niveles, `[42:54]` una hora): ninguna es un día. Los
  días con mes que se dicen visibles: el 2 y el 15 de julio, el 13 y el 15 de abril y el 6 de julio,
  todos de construcción. `[50:04]` dice «015 de abril»: el guion no enmascara un número de tres cifras,
  y se leyó a mano (el 15 de abril, construcción). **Sin PARADA por el barrido.**

### 2.5 Fotogramas: ninguno abierto

`corpus frames extract` de v18 (PICO DE MEMORIA 355 MiB; manifiesto `fr-v18-8b58f680`) y de v19
(abajo, §8), y `corpus frames check`. **No se abrió ningún fotograma.** El encargo los permitía en un
instante localizado de una sesión ya situada por la voz en un día de construcción; no hizo falta
ninguno para la extracción, y con cuatro tramos de gráfico real de v18 y la sesión 3 de v19 en PARADA,
abrir uno era riesgo sin necesidad. Ningún lote, así que ninguna fila de lote en
`HOLDOUT-EXPOSICIONES.md`.

## 3. Por pregunta

**Cómo se localizaron.** El guion detectó los códigos de S-1, S-2, S-5 y S-6 («pregunta S1», «S5
cerrada»…); S-3 y S-4 se localizaron a mano por el texto leído de la pregunta: S-3 empieza en
`[19:37]` («ese 3 que son las cuentas como zona de control de un esquema») y S-4 en `[22:42]` («ahora
la mecha que pasa a tu alto de M15»). El orden fue el de la hoja, S-1 a S-6, todas en v18, de
`[00:10]` a `[39:19]`. **Quién habla**: la transcripción no separa voces. En estas seis preguntas
el que lee en voz la hoja (el título, «Lo que nos has dicho», la pregunta y sus opciones, «Para
precisar» y «Para confirmar al final») es el trader, que tiene el PDF delante, y él mismo contesta;
Aleks interviene poco («pregunta S1», «cerrada»). Se atribuye por contexto y se declara en
`revisado_por` de cada ítem.

**«Para confirmar al final».** Las seis frases se leyeron y el trader las completó, cada una **al
final de su pregunta**, no juntas al final como pedía `PREGUNTAS-7A.md` §3: S-1 `[09:38]`, S-2
`[19:00]`, S-3 `[22:29]`, S-4 `[27:18]`, S-5 `[34:05]` y S-6 `[38:36]`. Dos quedaron a medias (S-3 y
S-4: abajo).

**Gráfico real.** En S-1, S-2, S-4 y S-5 el trader pasa del esquema inventado a su gráfico real con
marcas para explicarse. Esos cuatro tramos están **declarados no citables por precaución** (§2.2 y
§7, PARADA 1): lo que dijo ahí no se cita aquí, y se dice solo, sin literal, que lo hubo. Dos citas
que el guion de evidencia rechazó por pisar esos tramos por menos de un segundo (`[04:51]` y
`[14:13]`) tampoco se copian.

### 3.1 S-4 · La mecha que pasa tu alto de M15, y la vela que lo toma · A-35 (bloqueante)

Tramo `[22:42]`–`[27:36]` (v18). El trader lee «Lo que nos has dicho» y «Lo que todavía no sabemos»,
lee la pregunta 1 dos veces (`[24:00]` y, tras una pausa, `[24:20]`), y entonces dice que va a
empezar por la otra:

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| **Pregunta 1** (¿la mecha de M1 que pasa el alto y vuelve lo mueve?) | `[24:34]` «Esto hace referencia a la mitigación de liquidez, o sea, cómo tiene que mitigar en M1 el desarrollo de una zona lineal de liquidez.»; `[25:00]` «Primero vamos a empezar respondiendo a la pregunta que sería,» `[25:08]` «¿tu alto es la punta de esa mecha o el alto de las verdes?». Lo siguiente es el gráfico real (tramo de precaución) y, después, `[26:57]` «La respuesta sería la», cortado. | **no resuelve**: no elige ninguna opción (ni a, ni b, ni «otra») |
| **Pregunta 2** (¿el alto es la punta de la mecha de la roja o el de las verdes?) | `[25:11]` «La respuesta es la punta de la mecha.» (`ev-v18-002511-eec0acec`) | **resuelve**: opción **a** |
| Para precisar: «¿y si la mecha es de una vela verde?» | `[27:04]` «Pues si la mecha llega a ser más alto Que este alto De aquel alto O sea, sería así Entonces se trazaría desde aquí se trazaría desde allí» (`ev-v18-002704-8b01e191`) | en parte: la mecha de una verde también da el alto si queda más alta |
| Para confirmar al final: «Mi alto de M15 es ___, y lo toma la vela que ___» | `[27:21]` «y la toma la vela que» … `[27:27]` «aquí si me dejó pensativo» `[27:29]` «pero bueno, mi alto de M15 es la punta de la mecha en el esquema planteado» (`ev-v18-002729-38609240`) | **a medias**: la primera mitad; la vela que lo toma, no |

**La combinación, contra el «Para Aleks» de `PREGUNTAS-7A.md`** (valores verificados en
`parametros.yaml:551`, `liquidez_m15_mecha_que_vuelve`, opciones `no_mueve`, `solo_la_contraria` y
`cualquier_mecha`): pregunta 1 a + pregunta 2 a → `solo_la_contraria` (lo de hoy); 1 b + 2 a →
`cualquier_mecha`; 1 a + 2 b → `no_mueve`. **Aquí la pregunta 1 no tiene respuesta, y la pregunta 2
sola no da valor: la combinación no cae en ninguno. Lo decide el consultor.** Lo único que se suma:
la respuesta a la mecha de la verde (`[27:04]`) dice que una mecha que no es la de la roja también
puede fijar el alto en la formación, que va más allá de lo que describe `solo_la_contraria` («la
mecha de la propia vela contraria que forma el pivote»); no dice nada de una M1 posterior.
Regla general: no; habla «en el esquema planteado». «Creo»: no. Compra y venta: no lo dice (la
pregunta pide «lo mismo en un bajo», y no se contesta).

### 3.2 S-2 · Cuándo pasas el stop a la entrada · A-13

Tramo `[09:57]`–`[19:37]` (v18). Sobre los tres casos del esquema (toca y vuelve; cierra con cuerpo
por encima; rompe fuerte con hueco):

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| La pregunta (en cada caso, ¿ya mueves el stop?) | `[13:27]` «control para pues poder poner en break y la entrada tiene que cerrar por encima de su nivel alto de su de su máximo nivel para nosotros pues poder poner en break even porque nosotros esperamos a que cierre la vela y si cierra por debajo no vamos a poder no no no se nos va a» (`ev-v18-001327-70f1d014`); el caso 2 «aquí no hay ninguna zona de control» (`[12:09]`) | **resuelve en parte**: ni (a) al toque ni (b) a secas: **«otra»**, el break even cuando se desarrolla y se valida una zona de control (una vela que mitiga el alto y otra que cierra con cuerpo por encima de su máximo), esperando al cierre |
| La excepción del imbalance | `[11:45]` «el imbalance nosotros como tal no lo usamos, para análisis ahora no lo usamos no es una regla el uso del imbalance, entonces el caso 3» (`ev-v18-001145-6446f1de`) | **resuelve**: no hay excepción del imbalance; el caso 3 queda descartado |
| El margen («cierra con cuerpo, no necesariamente por encima de aquí, pero sí de la zona de entrada») | El trader lo lee en voz (`[10:49]`) y no vuelve a él. | **no resuelve** |
| Para precisar: ¿igual en una venta? | `[19:00]` «igual en la venta al revés sí» | **resuelve**: sí, al revés |
| Para confirmar al final | `[19:00]` «para confirmar al final pasas el stop de la entrada cuando se» `[19:07]` «se desarrolla una zona de control completamente validada» (`ev-v18-001900-1581efbe`) | **resuelve**: la zona de control validada; el «salvo ___» no se completa con nada claro (`[19:14]`–`[19:37]`) |

Regla general: sí (la condición es la zona de control validada, con un ejemplo en el gráfico real que
no se cita). «Creo»: no. Compra y venta: sí. Ver
también el bloque de días, sesión 2 (§4.2), donde vuelve a ponerlo así.

### 3.3 S-1 · Qué vela es tu rango de H4, y cuándo lo das por actualizado · VIDEO-JULIO.md §7 #1 a #3

Tramo `[00:10]`–`[09:57]` (v18).

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| La pregunta (¿cuál es tu rango y qué lado operas tras la roja?) | `[02:49]` «La respuesta es la letra A, claramente. El rango es la vela verde grande y sigo buscando compras.» (`ev-v18-000249-bb7b1c07`) | **resuelve**: opción **a** (el «Para Aleks» la lleva a regla nueva de sesgo por rango, con ADR) |
| Cómo cambia el lado | `[04:08]` «Entonces, se puede decir que, en resumen, para nosotros ver una continuidad o una reversión, bastaría con mecha o con cuerpo un rompimiento, pero para poder tener el enfoque, se tiene que definir el color de la vela. Si es verde, o sea, el cista rompe por encima, pues continuamos al cista.» (`ev-v18-000408-c48297b1`) | coincide con lo fijado (mecha o cuerpo, y el color: ADR-0080) |
| Para precisar: ¿qué vela pasa a ser tu rango nuevo? | Lo contesta dentro del tramo de precaución de S-1 (`[08:22]`–`[08:42]`): no se cita. En el bloque de días lo dice citable: al mitigarse el rango, «lo actualizamos a ese nivel» (§4.2, `ev-v18-011054-fbf8e9ae`) | **en parte** |
| Para precisar: **«rango mayor»** | Lo contesta sobre el gráfico real del 2 de julio (`[08:42]`–`[09:35]`), dentro del tramo de precaución de S-1: no se cita. Sin literal, dice que el rango mayor es el que no se ha mitigado por arriba ni por abajo y que se tiene en cuenta primero | **en parte, sin cita** hasta que el consultor decida sobre el tramo (§7, PARADA 1); el bloque de días lo dice citable (§4.1) |
| Para confirmar al final | `[09:43]` «mi rango es alcista» … «mi lado cambia cuando la vela de» `[09:47]` «4 horas genera un rompimiento» `[09:50]` «y también depende» `[09:51]` «del tipo de vela, si es alcista o bajista» `[09:53]` «sea por arriba o por debajo» (`ev-v18-000943-f0b82566`) | **en parte**: dice «alcista», no qué vela es el rango |

Regla general: sí, con el esquema y con su gráfico. «Creo»: no. Compra y venta: sí (habla de los dos
lados). En el bloque de días lo aplica: corrige el sesgo del bot por un rango mayor no mitigado
(§4.1).

### 3.4 S-3 · Qué zonas cuentas como zonas de control de un esquema · RN-009

Tramo `[19:37]`–`[22:42]` (v18).

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| La pregunta (A, B y C; solo una; ninguna; otra) | `[21:15]` «como zona de control en ese esquema a y b o sea a y b la respuesta sería esa de allí entonces es» `[21:24]` «de otra cual solo a y b» (`ev-v18-002115-bf40ec0b`) | **resuelve**: **«otra»: A y B**, no C |
| Para precisar: qué tiene que tener un bajo | `[21:37]` «pues no es que tenga que tener algún bajo un alto simplemente que se tiene que haber una mitigación» (`ev-v18-002137-54ff3a12`) | en parte |
| Para precisar: **el bajo que deja la propia toma** | `[22:23]` «una zona de control en la zona control por lo general es todo el esquema no existe un bajo» (`ev-v18-002223-fa0fc6ab`) | **no resuelve** con claridad: no dice sí ni no |
| Para confirmar al final | `[22:29]` «como tal ahora para confirmar al final una zona de control es pues él es el desarrollo es la mitigación en un orden flow alcista del punto más alto a la condicional es que hay una vela roja vale luego una vela verde y cierre con cuerpo por encima» (`ev-v18-002229-2be4ecf1`) | **a medias**: la definición; «si en el esquema hay dos, lo descarto», no |

Regla general: una definición («la mitigación del punto más alto»: una roja y una verde que cierra con
cuerpo por encima), sobre el esquema. «Creo»: no. Compra y venta: habla del order flow alcista y dice
«si es al revés» (`[22:01]`). **Ojo**: A y B son dos zonas, y RN-009 descarta el esquema con dos
(«si hay dos se descarta», que el trader lee en `[19:41]`); no dice si este esquema se descarta. En
el bloque de días: «se desarrolla demasiada zona de control antes que rompa» (§4.2).

### 3.5 S-5 · En qué momento pones la orden respecto de la ruptura de tu punto · ADR-0064; F7 #6

Tramo `[27:40]`–`[34:27]` (v18).

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| La pregunta (a: puesta antes; b: al cierre por encima; c: otra) | No elige letra: `[28:43]` «si aquí sale a nuestra no el esquema aquí está está errado el esquema aquí tiene una rata porque», y lo explica en el gráfico real (tramo de precaución, no citable). | **en parte** (por «Para precisar») |
| Para precisar: ¿la vela de la mecha te habría metido? | `[32:37]` «Claro, esta mecha de aquí ya activaría la entrada como tal, ¿vale?» (`ev-v18-003237-df38be59`); `[33:41]` «La primera vela de la mecha, ¿te habría metido la operación?» `[33:44]` «Sí.» (`ev-v18-003341-ce760e43`) | **resuelve**: sí; equivale a la **a** (la orden ya está y la mecha la llena) |
| **«Ese cierre con cuerpo que dices en el vídeo, ¿lo miras en la vela de un minuto o en la de 15 minutos?»** | `[33:51]` «En la vela de un minuto.» `[33:53]` «O sea, porque el cierre con cuerpo para la toma de líquidas de DM15,» `[33:56]` «de la zona lineal de DM15, tiene que ser en la temporalidad de DM1.» `[34:01]` «Un par de velas de DM1 lo tiene que mitigar con cuerpo.» (`ev-v18-003351-5bf50a14`) | **resuelve**: **M1**; y explica que ese cuerpo es el de la toma de la liquidez de M15 |
| Para confirmar al final | `[34:05]` «para confirmar al final pongo la orden» … «tu posible punto breaker» … «y entras cuando» `[34:17]` «pues se va a activar a través de una orden» `[34:20]` «stop limit» `[34:21]` «creo que era lo que manejábamos» (`ev-v18-003405-b0def171`) | **resuelve**: la orden al validar el punto y la entrada al activarse, con «creo» sobre el tipo de orden |

Sobre M1 o M15: el trader dice **M1**, no M15, así que el supuesto del «Para Aleks» («si dice M15,
no hay contradicción con S-18 de la sesión 5») no se da tal cual. Pero lo que añade es que ese cierre
con cuerpo es el de la **toma de la liquidez de M15**, medido en M1, no el de la ruptura del punto;
y en el esquema la mecha sí le mete. Leído así no contradice `ev-v16-000234-9a4fa375` («en M1 la mecha
siempre vale», salvo para habilitar la zona lineal de M15, que «tiene que ser con cuerpo»). **Sin
decidir: lo decide el consultor.** Regla general: sí. «Creo»: sí, en el tipo de orden. Compra y venta:
habla de compras; no lo dice para ventas.

### 3.6 S-6 · Las entradas que dejas sin tomar en el backtest · VIDEO-JULIO.md, F7 #10

Tramo `[34:28]`–`[39:13]` (v18).

| Fila | Literal de la filtrada | Resuelve |
|---|---|---|
| La pregunta (a: no, las tomo todas; b: sí, a veces; c: otra) | `[36:34]` «espera en tus partes dejas entradas válidas sin tomar la respuesta sería la no las tomo todas» `[36:44]` «todas las entradas validadas o sea sea perdedora o ganadora pues se toman y están se encuentra» `[36:52]` «explícitamente en los stats de excel» (`ev-v18-003634-de26ff65`) | **resuelve**: opción **a**, con un matiz (abajo) |
| Para precisar: ¿qué es «no afectar al muestreo»? | `[37:06]` «muestreo es que nosotros o sea excluimos los trace and break even porque no afectan para» `[37:13]` «el cálculo posterior de nuestra tasa de win rate u otros stats estadísticos» (`ev-v18-003706-83ce78dd`) | **resuelve**: deja fuera las que acaban en break even |
| Para precisar: ¿también en real? | `[38:08]` «pues en real simplemente no puedes obviar eso» `[38:12]` «porque te va a marcar tanto los trades en break-even» (`ev-v18-003808-c08babd3`) | resuelve: en real, no |
| Para confirmar al final | `[38:51]` «vale que quedan en break even pero como digo en los últimos backtest que se ha realizado se llega» … «entonces por lo general abarcamos todo» (`ev-v18-003851-cbc5657e`) | **resuelve**: las que quedan en break even; y en los últimos backtests grabados, también esas |

El matiz: antes de elegir dice «no se toman todas las entradas» (`[36:27]`), y después elige la a; lo
que deja fuera son las que acaban en break even, que ya conoce el desenlace. Para el «Para Aleks»
(las operaciones de más del bot): según esto, una operación del bot que el trader no tiene puede ser
una que él tomó y acabó en break even y no apuntó. Regla general: sí. «Creo»: no. Compra y venta: no
aplica.

## 4. El bloque de días

Sin códigos de voz: cada sesión se localizó por la voz (el día dicho y visible en la filtrada) y por
la respuesta b) de Aleks. Lo que hizo cada sesión, sin desenlaces de operaciones en R ni en dinero
(la activación no los usa), sin números de lámina y sin el número dicho junto al día de la sesión 2.
Cada corrección se identifica por la sesión y su minuto en el vídeo. **La pregunta «¿siempre, solo en
este caso, o de qué depende?» no se hizo en ninguna corrección de v18** (búsqueda en la filtrada:
ninguna aparición fuera de las preguntas técnicas); donde el trader generaliza por su cuenta («siempre
por debajo», «la regla es»), se dice. **Ningún fotograma abierto** (§2.5).

**Cómo se hizo, frente a `PREGUNTAS-7A.md` §1.** El orden pedía que el trader abriera el replay antes
de compartir pantalla, marcara y operara la sesión, y después corrigiera las láminas. Si abrió el
replay antes de compartir, la filtrada no lo dice (y Aleks no lo sabe: respuesta b). Lo demás, por
sesión, abajo.

### 4.1 Sesión 1 · 2026-07-07, de 11 a 15 · sirve a S-1 (v18, `[39:22]`–`[63:12]`)

- **Situada por la voz**: `[39:28]` «empecemos con el primero que es el 7 de julio».
- **El método no fue el de §1**: el trader no marcó ni operó la sesión primero ante la cámara. Tras
  el silencio (`[40:05]`–`[41:17]`, no citable) empieza directamente por la primera lámina
  (`[41:17]`) y la compara con trazos que ya tenía en su replay: `[44:14]` «Me gusta porque he hecho
  los trazos» `[44:17]` «Correspondientes». Aleks había pedido `[39:31]` «haz el tránsito de cómo
  operarías» `[39:33]` «hace ese día y después vamos a ver qué hizo el bolo».
- **Sesgo de H4 y su rango**: el bot dice bajista (la H4 que lo fija rompió el bajo anterior y cerró
  roja); el trader lo corrige a **alcista** por un rango mayor sin mitigar de días atrás:
  `[46:39]` «lo está definiendo bajista y aquí está mal nuestro sesgo no bajista porque tenemos que
  tener en» `[46:46]` «cuenta que todavía no ha sido mitigado un sesgo que llevamos ya desde hace
  algunos días atrás» (`ev-v18-004639-96f84da4`); `[47:18]` «… si estuviéramos tratando con estas
  velas de aquí» `[47:25]` «perfectamente diría que sí pero como digo nosotros estamos arrastrando un
  sesgo mayor y que es alcista» `[47:31]` «que no ha sido mitigado todavía ni por arriba ni por
  debajo» (`ev-v18-004718-01861c91`). Lo repite en otra lámina, y sitúa ese rango en el 6 de julio
  (`[51:25]`–`[51:45]`, día de construcción). **Corrección al sesgo, en varias láminas; sirve a S-1.**
  Generaliza: «tomando en cuenta las reglas originales en cuanto a rango» (`[51:47]`–`[51:52]`).
- **Liquidez de M15**: sus trazos coinciden con los del bot (`[44:18]`), y solo por debajo, porque
  opera compras: `[44:36]` «entonces cuando hay una operativa alcista …» … «siempre la liquidez»
  `[44:51]` «por debajo ahí está bien trazado» (`ev-v18-004436-8c3026c1`). Los trazos por encima del
  bot, de más (`[61:23]`–`[62:11]`), consecuencia del sesgo.
- **Punto de breaker**: da por buena una lámina, porque la toma de M15 fue con mecha: `[45:14]` «no lo
  ha considerado todavía esto un punto de posible punto breaker por el hecho de que la» … «tiene que
  haber una ruptura de la liquidez de m15 con» `[45:37]` «cuerpo» (`ev-v18-004514-0d48f2cc`). **Sirve
  a S-5** (el cuerpo es el de la toma de M15).
- **Correcciones**: `[52:19]`–`[53:21]`, ve una entrada que la lámina no enseña; `[53:21]`–`[55:49]`,
  el punto de breaker del bot está «demasiado alto» y marcado en M15: `[54:38]` «bueno el escenario de
  ejecución es en m1 no en m15 entonces aquí hay un problema» (`ev-v18-005438-b0a75ae4`);
  `[55:49]`–`[57:51]`, la vela de M1 que cierra por encima del alto de M15 y la caja, mal, porque con
  el sesgo alcista la ruptura tiene que ser «por debajo siempre por debajo» (`[57:15]`);
  `[58:27]`–`[60:23]`, la orden, mal colocada, y donde no hay ruptura de la zona lineal de M15 «no
  habría ninguna orden» (`[60:14]`).
- **0 y 0,8; dónde pondría la orden**: no los dice con números en esta sesión; corrige la caja y la
  orden del bot (arriba).
- **Su resumen**: `[62:40]` «es eso, o sea, hay cositas» `[62:42]` «a corregir, creo yo» `[62:44]`
  «más que nada en M1» … «por eso es muy importante» `[62:52]` «definir bien el bias»
  (`ev-v18-010240-3a2088a1`, con «creo yo»).
- **Contra la pregunta técnica**: coherente con S-1 (opción a: el rango que se arrastra manda hasta
  que se mitiga) y con S-5 (el cuerpo de la toma de M15 en M1).

### 4.2 Sesión 2 · 2026-07-02, de 11 a 15 · sirve a S-3 (v18, `[63:12]`–`[111:08]`)

- **Situada por la voz**: `[63:15]` «que revises los del día 2 de julio» y, al abrir, `[66:09]` «es
  el 6 de julio» `[66:12]` «o era el 2» `[66:18]` «es el día 2». Un número dicho junto al día en
  `[63:22]` no se copia (puede identificar una carpeta de láminas).
- **El replay tenía trazos de antes**: `[66:18]` «vale tengo trazos del modelo de continuidad que lo
  voy a borrar porque no tiene» `[66:47]` «nada que ver»; los borra y traza de nuevo. Después sí
  **marca y opera ante la cámara**, y luego pasa a las láminas (`[82:04]`): el método de §1.
- **Sesgo de H4 y su rango**: `[67:11]`–`[67:43]`, un rango alcista «hasta que se mitigue sea por
  arriba o por debajo»; opera compras. Entre una sesión y otra lo actualiza: `[70:54]` «Ahora
  actualizamos nuestro bias, nos vamos a 4H, o sea, cuando ya finaliza la sesión nos vamos a 4H y pues
  actualizamos.» … «este rango ya ha sido mitigado» `[71:11]` «entonces lo actualizamos» `[71:13]` «a
  ese nivel» (`ev-v18-011054-fbf8e9ae`). **Sirve a S-1** (cuándo se actualiza el rango).
- **Opera también la sesión de 7 a 11** del mismo día (`[67:43]`, construcción), sin ninguna
  operación: `[69:18]` «¿qué pasa aquí? aquí no hay ninguna» … «no es una zona de control linealmente
  limpia» (`ev-v18-010918-23724712`) y `[70:08]` «… en este caso de 7 a 11, donde no hay la
  posibilidad de tomar ningún trade …» (`ev-v18-011008-7fde5c4d`).
- **La de 11 a 15**, operada (`[71:18]`–`[81:52]`): liquidez de M15 por debajo, tomas con cuerpo en
  M1 (con mecha no le sirve, `[75:12]`–`[75:31]`), punto de breaker que se actualiza, break even al
  formarse la zona de control (`[77:19]`–`[77:39]`), y una sola orden que se mueve: `[78:01]`
  «nosotros pues actualizando también la orden» … «se maneja una sola orden, no es que se deja
  pendiente» `[78:09]` «otra orden aquí, otra orden aquí, no» `[78:10]` «se va actualizando la orden»
  (`ev-v18-011801-037f841e`). Para ver una ruptura, mira un gráfico de 5 segundos (`[74:01]`–`[74:08]`).
- **Correcciones a las láminas**:
  - `[83:43]`, el sesgo alcista del bot es correcto, pero el alto anterior es el del rango que arrastra:
    «nuestro alto anterior ojo que no sería este aquí sino que sería este aquí que ese rango que
    veníamos arrastrando» (`ev-v18-012343-2468628a`). **Sirve a S-1.**
  - `[84:22]`–`[84:33]`, la liquidez por encima, de más (opera compras).
  - `[85:16]` «se desarrolla demasiada zona de control antes que rompa la entrada o sea no cumple con
    el esquema ni» `[85:22]` «uno ni dos de entrada por lo cual no no se nos operaría»
    (`ev-v18-012516-15f69903`): el bot pone caja y orden donde no hay esquema. **Sirve a S-3.**
  - `[87:44]`–`[87:52]` «… no, no es válido» `[87:50]` «porque nosotros solo trabajamos con estos dos
    esquemas» (`ev-v18-012744-83f3c314`). **Sirve a S-3.**
  - `[93:53]` «Mira, has sabido diferenciar, o sea, que esta toma de liquidez con hora 12 no es válida,
    sino que la vela de M1 de las 12.1 cerró con cuerpo por debajo de M15 y eso es muy importante.»
    (`ev-v18-013353-90f56a8a`): da por buena la lámina. **Sirve a S-5.**
  - `[96:14]` «… no necesariamente tiene que haber una vela contraria sino que si la este» `[96:19]`
    «pongamos vela 1 vela 2 y la vela 2 tiene la mecha más larga la anterior en este caso bajista por»
    `[96:26]` «encima se podría considerar como un posible punto breaker» (`ev-v18-013614-cfd2b45d`):
    explica una entrada que el bot no tomó. Lo repite en `[104:31]`.
  - `[98:16]`–`[98:33]`, la zona de control que se forma después de romper el punto es la del break even
    (`ev-v18-013816-7b464c66`). **Sirve a S-2.**
  - `[100:33]`–`[101:31]`, la regla del bot «el esquema tiene más zona de control de las que admite»
    aplica en un sitio y no en otro, porque solo hay dos esquemas. **Sirve a S-3.**
  - `[105:43]` «aquí, no se puede trazar en cierta parte» `[105:45]` «en una sola vela como se ha trazado
    allí» `[105:48]` «la caja» (`ev-v18-014543-3b194627`).
  - `[109:29]`–`[110:20]`, los intentos en una misma liquidez y el recuento de órdenes que da la lámina;
    no se copian sus cifras.
  - Lo que da por bueno: los trazos de liquidez de M15 («la está clavando», `[88:30]`), varias tomas con
    cuerpo y una caja (`[95:34]`–`[95:50]`).
- **0 y 0,8**: no los dice con números; corrige el punto de breaker y la caja del bot.
- **Termina sin cerrar**: en `[111:08]` entra un bloque de cuarentena, y después se despiden; no hay
  resumen de la sesión.
- **Contra las preguntas técnicas**: coherente con S-2 (break even por la zona de control), con S-3 (en
  la práctica descarta por «demasiada zona de control») y con S-5.

### 4.3 Sesión 3 · 2026-07-03, de 7 a 11, según la respuesta b) · sirve a S-5 (v19, `[00:00]`–`[26:12]`) · PARADA 2

**La voz no sitúa esta sesión.** v19 empieza con un bloque de cuarentena, `[CUARENTENA 00:00–00:06]`,
que cayó por «fecha numérica» y su vecino: es donde se dice el día. Después, la voz no lo vuelve a
decir de forma visible; solo nombra, en `[00:39]`, el día desde el que viene el rango (el 2 de julio),
que no es el que se opera. El encargo es explícito: si el día dicho en voz sale tapado, la voz no
sitúa el tramo, y el minuto de la respuesta b) no basta; **PARADA con el minuto** (§7). Por eso:
- se leyó hasta `[07:34]` (antes de saberlo) y las líneas del barrido, y nada más de esta sesión;
- **no se cita nada** de ella y entra entera, por precaución, en `tramos_no_citables.yaml`
  (0:00:08–0:26:11);
- ningún fotograma.

Lo leído, sin citas: el trader dice que ya tenía las zonas de M15 trazadas, para ir más rápido, y
opera la sesión de 7 a 11 y sigue con la de 11 a 3. Si el
consultor confirma el día, se lee y se extrae en la rama de activación o en un anexo, como decida.

### 4.4 Sesión 4 · 2026-07-15, de 11 a 15 · sirve a S-1 (v19, `[28:42]`–`[44:02]`)

- **Situada por la voz**: `[28:42]` «voy a este es con fecha 15 15 de julio vamos a 15 de julio de
  julio que sería la fecha está aquí» (tras el silencio de 26:52–27:56).
- **Borra las marcas de antes**: `[29:44]` «vale perfecto voy a eliminar todo eso aquí que lo tenía
  marcó antes nuevamente hacia los trazos vale», y **marca y opera** ante la cámara la sesión de 7 a 11
  y la de 11 a 15 (`[35:08]`), y después pasa a las láminas (`[40:03]`): el método de §1.
- **Sesgo de H4 y su rango**: `[30:04]` «Similar al caso anterior, tenemos todavía un rango que no ha
  sido mitigado, …, y luego pues aquí tenemos el rango más reciente que todavía nos permite a nosotros
  buscar operaciones alcistas hasta que se actualice, ¿vale?» (`ev-v19-003004-439c43f1`). Liquidez de
  M15 por debajo (`[30:24]`).
- **Lo que no opera**: una toma con mecha no le vale (`[32:15]`); un punto invalidado por dos zonas de
  control: `[37:20]` «esta entrada, este posible punto breaker» … «porque nos genera más de una zona de
  control interna» `[37:25]` «antes de generar rompimiento al posible» `[37:27]` «punto breaker,
  entonces aquí no habría» `[37:29]` «ninguna entrada, vale» (`ev-v19-003720-f6e527fb`). **Sirve a S-3.**
  Después opera un esquema 1 y un esquema 2 (`[38:10]`–`[39:57]`), con el break even al formarse la
  zona de control tras la ruptura.
- **Correcciones a las láminas** (`[40:03]`–`[43:57]`): el bot dice sesgo de H4 **bajista** (la H4 que
  lo fija rompió los extremos de la anterior y cerró roja); el trader, **alcista** por el rango mayor:
  - `[41:04]` «definir mal tu rango lo que hagas después o bien podría estar bien o bien podría estar
    mal» … `[41:25]` «simplemente mejor bueno es considerable por eso ver si tienes un rango mayor y
    tratar de corregir» `[41:33]` «eso antes de meterte a operar confirmar el rango»
    (`ev-v19-004104-6d9d48cc`). **Sirve a S-1.**
  - `[42:04]`–`[42:30]` «… con nuestro modelo de ejecución de entrada va inclinado a lo que nosotros
    estamos buscando en base a h4 al sesgo … las reglas están planteadas para … montarnos en
    operaciones bajistas como tal y no en contratendencia aunque claro a veces indirectamente se puede
    desarrollar una contratendencia» (`ev-v19-004204-bd43e17d`): concede que, con el sesgo del bot, sus
    reglas sí buscarían ventas.
  - Y deja de corregir: `[43:34]` «eso está bien, eso está mal, porque como digo» `[43:36]` «hay un
    error» `[43:38]` «en cuanto al sesgo, entonces» `[43:41]` «no me voy a explayar» `[43:42]` «más»
    (`ev-v19-004334-2bb6a9a1`). **No revisa las láminas siguientes una por una**: las da por erradas por
    el sesgo.
- **0 y 0,8; dónde pone la orden**: no lo dice con números.
- **Contra la pregunta técnica**: coherente con S-1 (opción a).

### 4.5 La reserva · 2026-04-13, de 7 a 11 · sirve a S-3 (v19, `[44:03]`–`[92:24]`)

- **Situada por la voz**: `[44:03]` «Entonces, a ver, este es la fecha, vale, estamos ahora, nos vamos
  a 13 de abril, …», y después, ya operado, `[82:55]` «vamos a ver es 13 de abril» y `[92:13]` «… 13 de
  abril pues cerrado».
- **Abre por error otro día, el 15 de abril** (lo dice en voz en `[44:49]` y en `[50:04]`), lo marca y
  lo opera, y al comparar con la primera lámina ve que las velas no coinciden; Aleks le pregunta si es
  la fecha, y él reconoce que se había fijado en el 15 y vuelve al 13 (`[65:28]`–`[68:44]`). El 15 de
  abril es de construcción, pero es **un replay de otro día** que la respuesta a) no nombraba: el tramo
  0:44:49–1:08:49 entra por precaución en `tramos_no_citables.yaml` y no se cita (§7, PARADA 3). En ese
  tramo dice también que el 13 lo tenía en otro backtest suyo, y crea una sesión de replay nueva.
- **El 13 de abril, operado** (`[68:50]`–`[82:33]`): las dos sesiones, de 7 a 11 y de 11 a 3.
  - Sesgo: `[69:24]` «Lo primero, pues, para mis sesiones, de 7 a 11 y de 11 a 3, definimos nuestro
    rango, ¿vale? … el rango es alcista, todavía nos mantenemos alcistas, ¿vale? Tiene que romper por
    debajo y con vela roja, o sea, no importa si la vela roja termina con mecha o con cuerpo,»
    (`ev-v19-010924-bb54723f`). Coincide con el bot.
  - Punto de breaker que se actualiza con la mecha de la segunda vela del mismo color (`[71:38]`,
    `ev-v19-011138-12205799`).
  - **Se corrige a sí mismo sobre el break even**: `[73:59]` «… no no espera no haber corrección
    corrección interpretación mala» `[74:12]` «mía por si necesaria yendo en contra de lo que había
    dicho en los vídeos …». Y lo precisa: `[74:37]` «vale, pero que pasa, nosotros» … «tenemos la
    condicional de que para poner» … «tendría» `[74:44]` «que haber una vela verde y tendría» `[74:46]`
    «que cerrar con cuerpo por encima de» … (`ev-v19-011437-dbfc20b5`); **con un margen**: `[75:29]`
    «pero hemos dicho que tiene que romper» `[75:31]` «cerrar por encima de este alto» `[75:33]` «a ver
    una vela verde, cerrar con cuerpo» `[75:35]` «sea mínimo al menos por un par de puntos» `[75:37]` «o
    un pip, pero» … (`ev-v19-011529-8ae8b581`). **Sirve a S-2: es lo único de la 7a sobre el margen.**
  - Y la diferencia con el esquema 2: `[76:40]` «pero es que el esquema 2 nos dice que antes que ocurra
    el rompimiento se desarrolla la zona de control» … `[76:57]` «será después, o sea la zona de control
    después de haber activado la entrada» `[77:04]` «es la que a nosotros nos habilita pues poner en
    break even» (`ev-v19-011640-1fdc33a7`). **Sirve a S-2 y a S-3.**
- **Correcciones a las láminas** (`[82:33]`–`[92:13]`):
  - `[82:55]`–`[83:43]`, la lámina dice que el bot «se saltó 3 velas de h4» y nombra una vela de M1 de
    antes de las 7; el trader: no tiene que ver con las dos sesiones.
  - `[85:29]` «liquidez de m15 pero que se llega a mitigar ojo con esto se llega a mitigar con velas de
    m1 pero» `[85:38]` «de la sesión del 7 en adelante si es una vez la mitigación antes de las 7 que
    antes del inicio de» `[85:45]` «la sesión o de cada sesión no es válido tiene que mitigarse con la
    liquidez pues de esa sesión que» (`ev-v19-012529-685ae24d`), y `[86:50]`–`[87:03]` «… la toma tiene
    que ser con las velas de menos después de 7» (`ev-v19-012650-4f9f20ec`). Generaliza («ojo con
    esto»). Toca A-43 y la S-6 de la 7b.
  - `[86:05]`–`[86:50]`, una entrada dudosa: «esto ya sería algo subjetivo» y no la toma porque «no
    cumple con las reglas como tal».
  - `[88:22]`–`[89:30]`, una vela que en su gráfico sale de un color y en los datos del bot de otro:
    `[89:24]` «es una confusión de datos» `[89:27]` «vale, porque aquí marca» `[89:28]` «alcista en 90 y
    en Ducascopy» `[89:30]` «y pues marca bajista pero no pasa nada» (`ev-v19-012924-64367863`); con esos
    datos, la lógica del bot «estaría bien» (`[88:41]`–`[88:43]`). **Para el consultor**: una diferencia
    de datos entre su plataforma y Dukascopy, sin medir aquí.
  - `[90:59]`–`[91:16]`, la caja se va actualizando; y la regla del bot «el esquema tiene más zonas de
    la que admite» aplicada aquí, sin corregirla.
  - Su resumen: `[91:40]` «… pero pero bueno hay a ratas y en cuanto hay una interpretación correcta»
    `[91:49]` «creo yo hasta ahora en cuanto a la mitigación de la liquidez de m15 …» … «hay cosas que
    corregir como» `[92:02]` «la en m1 el trazo de las cajas también desde donde a donde se traza»
    (`ev-v19-013140-ced156e9`, «creo yo»).
- **0 y 0,8**: en el 13 de abril no los dice con números (`[73:06]` «nuestro nivel está a 0.80» cae en
  él, sin más).
- **Contra las preguntas técnicas**: con S-2 añade el margen («un par de puntos o un pip») y se corrige
  a sí mismo («interpretación mala mía»), sin contradecir lo que dijo en S-2 (la zona de control
  validada). Con S-3, coherente (una sola zona de control antes de romper).

### 4.6 La reserva del 2026-07-06: no se hizo

Respuesta b) de Aleks, y la voz al final de v19: `[94:59]` «6 de julio» `[95:06]` «el 6 de julio»
`[95:08]` «ya le hicimos crevallero o no» `[95:09]` «ah vale vale pues quedaría pendiente».

## 5. Contradicciones, cobertura y cosas que el consultor tiene que mirar

### 5.1 Contradicciones y cosas que mirar (sin decidir)

1. **S-4 / A-35**: la pregunta 1 no tiene respuesta y la 2 sola no da valor (§3.1). La combinación
   no cae en ninguno de los tres valores; **lo decide el consultor**. Lo que añade la mecha de la verde
   (`ev-v18-002704-8b01e191`) va más allá de `solo_la_contraria` en la formación del alto.
2. **S-2 / A-13**: ni (a) al toque ni (b) a secas: el break even cuando se forma y se valida una zona
   de control, al cierre (§3.2). Frente a lo fijado (`break_even_condicion` = `tocar` y
   `break_even_criterio_ruptura` = `mecha`, los dos CONFIRMED, según el «Para Aleks»), **va hacia el
   cierre con cuerpo**, como en la sesión 6 (`ev-v17-005111-8933dab2`). En la reserva añade un margen
   («un par de puntos o un pip», `ev-v19-011529-8ae8b581`) y se corrige a sí mismo
   («interpretación mala mía»).
3. **S-1**: opción **a** (el rango es la vela verde grande): según su «Para Aleks», regla nueva de sesgo
   por rango, con ADR. En el bloque de días la aplica tres veces contra el bot (sesiones 1 y 4: el bot
   dice bajista con la H4 anterior; él, alcista por el rango mayor), y en la 4 deja de corregir por eso.
4. **S-3 / RN-009**: cuenta A y B (dos zonas) y no dice si ese esquema se descarta; RN-009 descarta el
   de dos. Puede ser que A y B sean zonas del retroceso y no «antes de romper»: lo dice en la sesión 2 y
   en la reserva (la zona de control del esquema 2 es antes de romper el punto; la del break even,
   después: `ev-v19-011640-1fdc33a7`).
5. **S-5**: dice **M1**, no M15; el supuesto del «Para Aleks» («si dice M15») no se da tal cual, pero
   lo que explica (el cuerpo es el de la toma de la liquidez de M15) es compatible con
   `ev-v16-000234-9a4fa375`. **Sin decidir.**
6. **S-6**: «no, las tomo todas», salvo las que acaban en break even, que deja fuera del muestreo (y
   en los últimos backtests grabados, también esas toma). Para leer las operaciones de más del bot.
7. **Una diferencia de datos** entre la plataforma del trader y Dukascopy (el color de una vela, en la
   reserva, `ev-v19-012924-64367863`). Sin medir aquí.
8. **El método del bloque, en tres sesiones, no fue el de §1**: en la 1, el trader no marcó ni operó
   antes de las láminas; en la 2 y la 4, borró trazos que ya tenía; en la reserva abrió primero otro
   día. Si abrió el replay antes de compartir pantalla, no se sabe.

### 5.2 Cobertura de lo que la 7a tenía que cubrir

| Qué | Ambigüedad o fuente | Cubierto |
|---|---|---|
| S-1, el rango de H4 | `VIDEO-JULIO.md` §7 #1 a #3 | **sí** (opción a); «rango mayor», en parte (en el tramo de precaución; el bloque lo dice citable) |
| S-2, el break even | A-13 | **en parte**: hacia el cierre con cuerpo por la zona de control; el imbalance, sí; el margen, solo en la reserva |
| S-3, las zonas de control | RN-009 | **sí** la pregunta (A y B); el bajo de la toma, no |
| S-4, la mecha que vuelve | A-35 | **en parte**: la pregunta 2 sí (a), la 1 no; sin valor |
| S-5, cuándo se coloca la orden | ADR-0064; F7 #6 | **sí** por «Para precisar» (la mecha mete; M1) |
| S-6, las entradas sin tomar | F7 #10 | **sí** (a, salvo las de break even) |
| Sesión 1 (07-07), sirve a S-1 | — | **sí**: corrige el sesgo por el rango mayor |
| Sesión 2 (07-02), sirve a S-3 | — | **sí**: «demasiada zona de control», «solo dos esquemas» |
| Sesión 3 (07-03), sirve a S-5 | — | **no**: PARADA 2, la voz no la sitúa |
| Sesión 4 (07-15), sirve a S-1 | — | **sí**: corrige el sesgo y deja de corregir |
| Reserva (04-13), sirve a S-3 | — | **sí**: una zona antes de romper; y el break even con margen |
| Reserva (07-06), sirve a S-1 | — | no se hizo |

## 6. Tabla final

| Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|---|
| **S-4, pregunta 1** | A-35 | v18 | 24:00–25:08 | no resuelve: la lee y no elige; sin valor | no | no | no lo dice |
| **S-4, pregunta 2** | A-35 | v18 | 25:08–25:17 | **resuelve**: (a), la punta de la mecha; sola no da valor de `liquidez_m15_mecha_que_vuelve` | no, «en el esquema planteado» | no | no lo dice |
| S-4, la mecha de una verde | ADR-0084 | v18 | 27:01–27:17 | en parte: también fija el alto si queda más alta | no | no | no lo dice |
| **S-2** | A-13 | v18 | 09:57–19:37 | en parte: «otra», el break even al formarse y validarse una zona de control, al cierre; contra lo fijado (`tocar`, `mecha`) | sí | no | sí |
| S-2, el imbalance | A-13 | v18 | 11:44–11:58 | **resuelve**: no lo usa, no hay excepción | sí | no | n/a |
| S-2, el margen | A-13 | v18 · v19 | v18 10:49; v19 75:29–75:43 | en parte: en S-2 no lo contesta; en la reserva, «un par de puntos o un pip» | sí | no | habla de compras |
| S-1 | VIDEO-JULIO.md §7 #1 a #3 | v18 | 00:10–09:57 | **resuelve**: (a), el rango es la vela verde grande; lado por ruptura con mecha o cuerpo y color | sí | no | sí |
| S-1, «rango mayor» | VIDEO-JULIO.md §7 #1 a #3 | v18 | 08:42–09:35 | en parte: en el tramo de precaución, sin cita; el bloque de días, citable | sí | no | sí |
| S-3 | RN-009 | v18 | 19:37–22:42 | **resuelve**: «otra», A y B; no dice si el esquema se descarta | sí, como definición | no | sí («al revés») |
| S-3, el bajo de la propia toma | RN-009 | v18 | 22:18–22:29 | no resuelve: «todo el esquema», sin sí ni no | no | no | n/a |
| S-5 | ADR-0064; F7 #6 | v18 | 27:40–34:27 | en parte: sin letra; por «Para precisar», hacia (a): la mecha mete | sí | sí, en el tipo de orden | habla de compras |
| S-5, ¿M1 o M15? | ADR-0064; F7 #6 | v18 | 33:46–34:05 | **resuelve**: M1, el cuerpo de la toma de M15; sin decidir frente a S-18 de la sesión 5 | sí | no | n/a |
| S-6 | F7 #10 | v18 | 34:28–39:13 | **resuelve**: (a), salvo las de break even | sí | no | n/a |
| Sesión 1 del bloque | 2026-07-07 | v18 | 39:22–63:12 | corrige el sesgo del bot por un rango mayor; M1 como escenario de ejecución | sí, «las reglas originales» | sí, en el resumen | compras |
| Sesión 2 del bloque | 2026-07-02 | v18 | 63:12–111:08 | demasiada zona de control; solo dos esquemas; toma con cuerpo en M1; break even por zona de control | sí | no | compras |
| Sesión 3 del bloque | 2026-07-03 (respuesta b) | v19 | 00:00–26:12 | **PARADA 2**: la voz no la sitúa; sin extraer | — | — | — |
| Sesión 4 del bloque | 2026-07-15 | v19 | 28:42–44:02 | corrige el sesgo por el rango mayor y deja de corregir | sí | no | compras |
| Reserva del bloque | 2026-04-13 | v19 | 44:03–92:24 | margen del break even; toma con velas de la sesión; diferencia de datos | sí | sí, en el resumen | compras |

Por códigos de la hoja (6): se hicieron los 6, en v18. En filas: **resuelve** 6 (S-4 pregunta 2, S-2
el imbalance, S-1, S-3, S-5 M1 o M15, y S-6); **en parte** 5 (S-4 la mecha de una verde, S-2, S-2 el
margen, S-1 «rango mayor» y S-5); **no resuelve** 2 (S-4 pregunta 1 y S-3 el bajo de la toma). Del
bloque, 4 sesiones extraídas y 1 en PARADA; la reserva del 07-06 no se hizo.

## 7. PARADAS, desviaciones y negativas de la guardia

### 7.1 Las PARADAS (esperan la respuesta de Aleks)

Aleks se ausentó con la orden de seguir el encargo hasta «Rama lista para revisión» y dejar apuntado,
con su porqué, lo que no cuadrara con lo medido (mensaje del 2026-11-17). Lo que no cuadró:

- **PARADA 1 · El gráfico real con marcas del bloque técnico (v18).** La respuesta a) decía que en
  pantalla solo salieron los esquemas, el replay de cada sesión del bloque y las láminas. La filtrada
  dice que en S-1, S-2, S-4 y S-5 el trader pasó a su gráfico real con marcas: S-1 `[05:00]`–`[09:37]`
  (el 2 de julio de 2026: construcción y día de la sesión 2 del bloque, enseñado ANTES de ella);
  S-2 `[14:20]`–`[18:48]`, S-4 `[25:18]`–`[26:56]` y S-5 `[28:51]`–`[32:17]`, de días que la voz no
  dice, con desenlaces de operaciones. El encargo (a) manda declarar no citable «un replay con marcas o
  de otro día». **Hecho por precaución**: los cuatro, en `tramos_no_citables.yaml`, y en
  `HOLDOUT-EXPOSICIONES.md` como exposición posible (si alguno fuera de un día reservado, sus palabras
  serían su etiqueta). **Decide Aleks**: mantenerlos (y si los de día desconocido van a algo más), o
  levantar alguno (el de S-1 es de construcción y lleva la respuesta a «rango mayor»).
- **PARADA 2 · La sesión que abre v19 (la 3 según b).** Su día se dice dentro de
  `[CUARENTENA 00:00–00:06]` y la voz no lo vuelve a decir visible: no la sitúa. Minuto: v19
  `[00:00]`–`[26:12]`. **Hecho**: no se sigue leyendo ni se cita; entra entera por precaución en
  `tramos_no_citables.yaml` (0:00:08–0:26:11); lo leído antes de saberlo, declarado. **Decide Aleks**
  si se da por el 2026-07-03 y se extrae, y cómo.
- **PARADA 3 · El 15 de abril, abierto por error en la reserva (v19 `[44:49]`–`[68:49]`).** Día de
  construcción, pero un replay de otro día que la respuesta a) no nombraba. **Hecho**: por precaución,
  no citable y declarado. **Decide Aleks** si se levanta.
- **PARADA 4 · S-4 / A-35 sin valor** (§3.1): la combinación no cae en ninguno; lo decide el
  consultor (el encargo ya lo preveía: «lo decido yo»).

### 7.2 Desviaciones y negativas de la guardia

- La guardia negó `subprocess.run(...)` dentro de un guion de la carpeta de trabajo que creaba los ítems
  de evidencia («el programa que lanza no se calcula»). Se siguió su forma: la CLI
  `botsito evidence new` con argumentos literales, una llamada por ítem. (Las otras dos negativas,
  en «Decisiones de proceso», arriba.)
- La puerta de `evidence new` rechazó tres citas que pisaban un tramo de precaución (`[04:51]`,
  `[14:13]` y la segunda mitad de `[25:11]`) y pidió ajustar la ventana de otra (`[42:04]`): las tres
  primeras no se citan; la cuarta se ajustó.
- **El commit de la cuarentena de v19 no es «propio»**: lleva también la evidencia de v18 y v19, los
  tramos de precaución, los fotogramas, la hoja usada y el informe, porque `make check` sella el árbol
  ESTADIADO entero y no deja nada sin estadiar (y `git add -p` es interactivo). Los bloques de v19 van
  en él, con su `Fuente:`.
- **Ningún push ni CI**: el encargo pedía, al cerrar, el push a `fix/sesion-07` y la CI de Linux; la
  orden de Aleks del 2026-11-17 al ausentarse («No cierres la rama, no hagas push ni merge») manda: se
  deja sin lanzar (§10).
- Las seis frases de «Para confirmar al final» se leyeron al final de cada pregunta, no juntas.

## 8. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` y `manifest.yaml`: v18 y v19.
- `knowledge/corpus/transcripciones/`: `tr-v18-large-v3-int8-float16-ba2d4fca` (1320 segmentos) y
  `tr-v19-large-v3-int8-float16-d6b9cc45` (979).
- `knowledge/corpus/fotogramas/`: `fr-v18-8b58f680` (6747 fotogramas, 0 extra; PICO DE MEMORIA 355 MiB)
  y `fr-v19-c477861e` (5756, 0 extra; 358 MiB). `corpus frames check`: «OK: 19 extracciones coherentes
  con el disco; 3 obligatorios presentes». Ninguno abierto.
- `knowledge/corpus/tramos_no_citables.yaml`: 6 «SIN AUDIO», 7 de cuarentena (4 de v18 y 3 de v19) y 6
  de precaución (4 de v18 y 2 de v19).
- `knowledge/evidence/v18/` (38 ítems) y `knowledge/evidence/v19/` (14).
- v18 y v19 en `SESIONES_EN_CUARENTENA` y sus tests.
- `docs/sesion-7/HOJA-USADA-7A.md` y el recuadro de `PREGUNTAS-7A.md`.
- Las filas del 2026-11-17 en `HOLDOUT-EXPOSICIONES.md`.

## 9. Para la orden de cierre (preparado, sin aplicar)

- **La F nueva** de la Next Action (hoy, la línea 28 de `PROJECT_STATE.md`, **1249 bytes** con su fin
  de línea, `wc -c`); la propuesta, **1082 bytes**:

  > F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7. La re-corrida que
  > cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; línea
  > base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Trazas y ablación (TRAZAS-ABLACION.md;
  > `motor decisiones`) y láminas (LAMINAS.md; `motor laminas`; R4.5), hechas. La sesión 7, en dos días
  > con el método de ADR-0093 (PREPARACION-SESION-7.md; R4.3; pivote en
  > docs/plan/PIVOTES-SESION-7.yaml): la 7a, grabada el 2026-11-16 y el 2026-11-17 (v18 y v19, id
  > 2026-11-16-sesion-07), está ingerida (SESION-07-EXTRACCION.md, con sus PARADAS). Siguiente, en este
  > orden: (1) activar la 7a; su activación genera las láminas de la 7b con su motor, revisa
  > PREGUNTAS-7B.md y pasa SESION_EN_CURSO a "08"; (2) grabar, ingerir y activar la 7b, con la rama de
  > S-22 y S-19; (3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6). El vídeo de mapeo,
  > si llega, SIN ABRIR y fuera del repo, por su propia rama. C y R6a en los huecos; R5.7 después de
  > (3), sobre esa corrida.

- **R4.3**, la línea de Estado: `- **Estado:** ABIERTA (la 7a, grabada el 2026-11-16 y el 2026-11-17 e
  ingerida en trabajo/sesion-07, SESION-07-EXTRACCION.md; falta activarla, y la 7b).`
- **La copia de seguridad** en Technical Debt de `PROJECT_STATE.md` (línea 140; hoy **95 bytes**):
  `- Copia de seguridad de las crudas y los WAV … falta v18 y v19 (entera en HISTORIA, Technical Debt ACORTADA)`
  (**111 bytes**).
- **Lo nuevo fuera de git, para la copia de seguridad**:
  - los vídeos: `corpus/Estrategia del trader/Grabación de pantalla 2026-11-16 145418.mp4` y
    `Grabación de pantalla 2026-11-17 135357.mp4`;
  - `C:\Users\USER\Desktop\sesion-07-audio\`: `sesion-07-v18.wav` y `sesion-07-v19.wav`, las crudas
    (`sesion-07-v18.cruda-NO-LEER.jsonl` y `.txt`, y las de v19), las filtradas (`.filtrada.md`), los
    registros (`.registro.txt`) y las carpetas `sesion-07-v18-trabajo` y `sesion-07-v19-trabajo`;
  - `data/transcripciones/v18/` (416 MB) y `data/transcripciones/v19/` (354 MB);
  - `data/fotogramas/v18/` (4,0 GB) y `data/fotogramas/v19/`.
- **La fecha**: la 7a se grabó el 2026-11-16 y el 2026-11-17, no el domingo 2026-11-15 de la F de hoy.

## 10. El cierre de la rama: sellos, push y CI

Los sellos de la rama, con su PICO DE MEMORIA:
- apertura (`d1829d14`): primero rojo y sin sello (`settings.local.json`); relanzado, 3513 passed,
  sello sobre `f9e69e81`, **316 MiB**;
- registro (`5bbc694d`): 3513 passed, sello sobre `67c70678`, **319 MiB**;
- cuarentena de v18 (`f1310b44`): 3513 passed, sello sobre `41bdf8d8`, **318 MiB**;
- el de este commit, y el final, abajo.

**Push y CI: no lanzados**, por la orden de Aleks del 2026-11-17 (§7.2). La orden del encargo, para
cuando la dé: `git push origin trabajo/sesion-07:refs/heads/fix/sesion-07` y una consulta suelta de
`gh run view` (el fallo esperado, el de `state check`).

## Estado

EN CURSO.
