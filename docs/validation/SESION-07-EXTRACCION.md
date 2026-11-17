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
  solo comando («antes, en el mismo comando, va `uv run botsito state check`»); seguí su forma: una
  llamada por ejecutable.
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

## Estado

EN CURSO.
