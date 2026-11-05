# Sesión 6 con el trader: la extracción por pregunta

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras ni en la
> hoja de ruta. Cada «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de
> cada respuesta lo decide el consultor en otra rama (encargo del 2026-11-04,
> `docs/encargos/trabajo-sesion-06.md`).

Rama `trabajo/sesion-06`, abierta el 2026-11-04 desde `main` en `136280d` (commit de estado sobre el
merge `1cbf403`, tag `stable/F38l-guardia-g1`). Tramo R4 de la hoja de ruta (R4.2, NA:F). Skill
`ingerir-sesion`, de principio a fin. Plantilla: `SESION-05-EXTRACCION.md`. Tag de cierre previsto:
`stable/F38m-sesion-06`.

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse --short main` = `136280d`; `git rev-parse main origin/main` da dos veces
  `136280d11873a3bfcf38e937deace14c74525b97`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F38l-guardia-g1`;
  `git rev-parse "stable/F38l-guardia-g1^{commit}"` = `git rev-parse main^1` =
  `1cbf4038b8cc6789bea81728a1cd08bd5ab450a2`; `git ls-remote --tags origin stable/F38l-guardia-g1`
  da `a9cc6b0… refs/tags/stable/F38l-guardia-g1` (el objeto del tag anotado). Es también el primero
  de `git tag --list 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 41935014939`:
  `completed`, `success`, `headSha` `136280d11873a3bfcf38e937deace14c74525b97`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`
  (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"06": {` en la línea 216 de
  `CODIGOS_DE_SESION_TEXTO`, con 23 textos; `"06": ORDEN_SESION_06` en `HOJAS` (línea 250), con 23
  códigos; `SESION_EN_CURSO = "06"` (línea 252).

## 0. Lo primero

### 0.1 Las respuestas de Aleks a las preguntas a) a d) del encargo (2026-11-04), copiadas tal cual

Preguntadas en el terminal antes del registro de v17 (encargo, «ENTRADAS»), con dos preguntas de la
sesión tras medir el vídeo (la duración de casi 2 h y los tres silencios):

> a) solo habló ejemplos sobre julio nomás, sobre diciembre dijo que aún no lo ha grabado. b) las preguntas fueron en orden, las que no se hicieron fueron las de gráficos y ejemplos que me diste, eso lo verás en la grabación junto a la sugerencias. C) en la llamada lo ha contado. D) no tengo notas de la reu

> no, las 2h fueron toda la reu. los silencios fueron porque se fue al baño xd. o sea en julio explicó conceptos de las preguntas mostrando el gráfico de julio, pero tengo entendido que ese material ya está procesado es un "mes libre"

Lo que se sigue de ellas:
- **a)** El trader enseñó su gráfico de julio, días sin precisar. Julio no tiene ningún día en
  `casos_ocultos`, pero solo del 1 al 17 es construcción, y un día del 18 en adelante es PARADA
  (encargo, «Extracción»). Aleks lo vio en directo: se declara en `HOLDOUT-EXPOSICIONES.md`.
  **Decisión de la sesión, con el precedente de la decisión 1 del consultor en la sesión 5
  (`SESION-05-EXTRACCION.md` §0.1): ningún fotograma de los tramos en que el trader enseña su
  replay.** En la imagen puede salir un día del 18 en adelante o cifras de resultados, y el encargo
  solo permite abrirlos por instante localizado. Si una respuesta dependiera de la pantalla, se
  avisa a Aleks y no se abre sin su orden.
- **b)** Según Aleks, las preguntas fueron en orden y no se hicieron las de los gráficos y los
  ejemplos; lo demás, incluidas las sugerencias del trader, se lee en la grabación. Qué códigos
  exactos son lo mide esta extracción: por eso la `naturaleza` de v17 no da una lista cerrada.
- **c)** «Para cerrar» se contó en la llamada: no se saltó y no hay capturas.
- **d)** No hay hoja con notas: no entra nada en `Sesiones/`.
- **La duración:** las 2 h son la reunión entera, sin un corte de la grabadora ni un segundo vídeo.
- **Los silencios:** una pausa, no un corte de la grabación. Ninguna respuesta queda incompleta por
  el audio. Van igualmente a `tramos_no_citables.yaml` como «SIN AUDIO» (encargo, «Audio»).

### 0.2 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-04`: `False`. **Desviación del paso 1, declarada** (encargo): la sesión se adelantó del 3
  al 4, y este día se comprobó DESPUÉS de grabar, no antes. Declarada también en
  `HOLDOUT-EXPOSICIONES.md` (2026-11-04).

### 0.3 El vídeo

Es el único vídeo del primer nivel de `corpus/Estrategia del trader/` que no estaba en
`fuentes.yaml`, que acababa en v16. v17 es el siguiente id libre. La sesión no se partió: un solo
vídeo y un solo día.

| | v17 |
|---|---|
| Fichero | `Grabación de pantalla 2026-11-04 142903.mp4` |
| Bytes | 7.574.611.265 |
| Fecha (del nombre) | 2026-11-04 |
| Duración (ffprobe, formato) | **7199,19 s = 1:59:59** |
| Vídeo | h264 1844×1062, 30 fps |
| Audio | AAC estéreo 48 kHz, 7199,19 s |
| Audio extraído (fuera del repo) | `C:\Users\USER\Desktop\sesion-06-audio\sesion-06-v17.wav` |

## 1. El registro (v17)

- **`fuentes.yaml`**: v17 con `drive_id: null`, su fecha y una `naturaleza` que describe el vídeo
  entero, también el gráfico de julio que enseñó el trader (respuesta a). Encima, el comentario de
  la sesión 6.
- **`tests/unit/test_inventario.py`**: `range(1, 17)` → `range(1, 18)`.

### 1.1 El test roto a propósito

Con v17 ya en `fuentes.yaml` y ANTES de añadirlo a `SESIONES_EN_CUARENTENA`:

```
uv run pytest -q tests/unit/test_cuarentena.py \
  "tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena" \
  "tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo" -p no:randomly
E       AssertionError: assert ['v17: es una... EXCEPCIONES'] == []
E         Left contains one more item: 'v17: es una sesion (drive_id null) y no esta en SESIONES_EN_CUARENTENA ni en EXCEPCIONES'
E       AssertionError: assert frozenset({'v...', 'v8', ...}) == frozenset({'v..., 'v8', 'v9'})
E         'v17'
E       AssertionError: assert frozenset({'v...', 'v8', ...}) == {'v10', 'v15'...', 'v8', 'v9'}
E         'v17'
FAILED tests/unit/test_cuarentena.py::test_la_lista_cuadra_con_fuentes - Asse...
FAILED tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena
FAILED tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo
```

La guardia ve v17 en cuarentena en cuanto entra en `fuentes.yaml`, porque lo deduce de allí; el
módulo todavía no lo tiene, y el conjunto esperado del tercer test está escrito a mano.

Después:
- `src/botsito/corpus/cuarentena.py`: `SESIONES_EN_CUARENTENA` con `"v17"`;
- `tests/unit/test_guardia_claude.py:152`: el conjunto esperado con v17 (lo que la skill no nombra);
- `tests/unit/test_cuarentena.py`: el ejemplo sintético de
  `test_la_comprobacion_de_la_lista_no_es_decorativa` lleva v17, y la sesión sin listar que sondea
  pasa a v18 (ídem).

Las mismas tres pruebas pasan, y con ellas todo el fichero de inventario: `pytest -rA` de
`test_cuarentena.py`, `test_inventario.py` y las dos de `test_guardia_claude.py` da **55 `PASSED`** y
0 `FAILED`/`ERROR`.

### 1.2 Inventario y hashes

- `uv run botsito corpus inventory`: `OK: manifiesto escrito · heredado_v2: 477 ficheros,
  117,626,282 bytes · material_adicional: 73 ficheros, 6,850,662 bytes · video_original: 17
  ficheros, 71,348,208,794 bytes`. El manifiesto gana una entrada y nada más: v17 (sha256
  `6d61b77a…c30fcb5c`, `duracion_s` 7199.192, 1844×1062). Los vídeos pasan de 16 a 17 y el material
  adicional sigue en 73.
- `uv run botsito corpus check --hashes`: `OK: el corpus coincide con el manifiesto (hashes)`.

## 2. Audio, cuarentena y holdout

### 2.1 Los cortes de audio

Con las formas de la skill (paso 2): `silencedetect=noise=-50dB:d=30` y `volumedetect`.

| Vídeo | silencedetect -50 dB, 30 s | volumedetect (vídeo entero) |
|---|---|---|
| v17 | **tres silencios:** 4543,92–4717,17 s (173,3 s) = 1:15:43–1:18:38; 4731,20–4804,75 s (73,6 s) = 1:18:51–1:20:05; 4807,74–4914,82 s (107,1 s) = 1:20:07–1:21:55 | media −22,4 dB, máximo 0,0 dB |

**Son una pausa de la reunión** (respuesta de Aleks, §0.1), no un corte de la grabación: no se midió
a −90 dB porque la causa ya está dicha y el encargo pide estas formas. Entre ellos quedan 14 s y 3 s
con audio. Van los tres a `tramos_no_citables.yaml`, redondeados hacia fuera (el criterio de «Los
límites de un tramo», `SESION-DE-PREGUNTAS.md`), con motivo «SIN AUDIO», y a la `naturaleza` y al
comentario de v17 en `fuentes.yaml`. La puerta del ASR se pasa tras la transcripción.

## 7. Desviaciones y negativas de la guardia

Las negativas de la guardia de Claude Code se declaran aquí, como manda el encargo («Reglas de esta
rama»; `docs/runbooks/DECISIONES-DE-PROCESO.md`).
1. **El primer `make check` de la rama salió en rojo** (`1 failed, 3209 passed`) en
   `test_hoja_de_ruta`: el informe todavía no tenía tabla final ni decía que era una PLANTILLA. La
   misma trampa de la sesión 5, y `abrir-rama` no la nombra. Se añadió la línea de PLANTILLA. Ese
   `make check` corrió a la vez que la medida y la extracción del audio, que no escriben en el
   repositorio.
2. **`uv run pytest ... -o addopts=""`, negado por la guardia** («`pytest -o` cambia su
   configuracion, que puede cargar plugins o ficheros que la guardia no lee»). Solo se buscaba la
   línea de resumen. Se siguió la forma que propone su mensaje: sin `-o`, con `-rA` y `grep -c`. No
   es un paso que mande la skill.

## Estado

EN CURSO.
