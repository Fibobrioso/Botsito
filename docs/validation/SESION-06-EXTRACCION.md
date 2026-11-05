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

Y al preguntarle, tras leer la filtrada, si enseñó el limpio antes que el marcado:

> si, en los 2 primeros gráficos, primero el limpio, luego marcado de gráfico 1 y 2

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
  exactos son lo mide esta extracción: por eso la `naturaleza` de v17 no da una lista cerrada. **La
  medida matiza el recuerdo** (§2.4): el gráfico 1 se contestó, el 2 quedó a medias y solo no se
  hicieron del 3 al 6; los ejemplos de S-5 y S-6 sí se preguntaron, y el trader los da por mal
  planteados.
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
comentario de v17 en `fuentes.yaml`. La puerta del ASR se pasa tras la transcripción (§2.2).

### 2.2 v17: transcripción, cuarentena y puerta del ASR

- **Transcripción del corpus**, tras el «listo» de Aleks: `uv run botsito corpus transcribe --video
  v17` → `tr-v17-large-v3-int8-float16-9d44007a`, **1701 segmentos**. `corpus transcript check`:
  `OK: 18 transcripciones coherentes con el disco y el glosario`.
- **El guion de `main`** (`git diff --quiet main -- scripts/transcribir_sesion.py`: idéntico, exit
  0): `--audio C:/Users/USER/Desktop/sesion-06-audio/sesion-06-v17.wav --sesion 06 --video v17`, a
  continuación, nunca a la vez. El registro (`sesion-06-v17.registro.txt`) dice:
  - hoja: la de la sesión 06; tramos no citables del vídeo: 3 (los tres silencios);
  - audio comprobado: el sha256 de su WAV (`32c54faabf58…`) es el de la transcripción del corpus de
    v17;
  - ASR de 1462,7 s (factor 0,20); **1701 segmentos**, los mismos que la transcripción del corpus;
  - **segmentos en cuarentena: 21 en 6 bloques**, tapados solo por meses; motivos «día de la semana
    con número» 2, «mes» 5 y «vecino» 14; **tapados por tramos: 0**; bloques `[NO CITABLE]`: 0;
  - códigos detectados: S-1 00:00, S-2 02:25, S-5 30:45, S-6 30:28, S-13 50:05, S-15 60:09 y S-17
    75:14; sin código detectado, S-3, S-4, S-7 a S-12, S-14, S-16 y S-18 a S-23 (cómo se localizaron,
    §3).
- **La puerta del ASR de los silencios.** El guion tapa todo segmento que SOLAPE un tramo y tapó
  **0**: ningún segmento solapa los tres cortes, así que tampoco hay ninguno con `t1` dentro. La
  filtrada salta de `[75:21]` a `[83:20]`.
- **Los seis bloques, a `tramos_no_citables.yaml`**, sin contenido y en este commit, con el criterio
  de «Los límites de un tramo» (el fin de cada bloque más un segundo): **0:03:46–0:03:51**,
  **0:04:23–0:04:30**, **0:07:13–0:07:24**, **0:07:33–0:07:39**, **1:58:24–1:58:27** y
  **1:59:16–1:59:23**. Control positivo: cada bloque cabe entero en su tramo. El segundo de margen
  toca la primera línea visible tras el bloque en cuatro de ellos (`[04:29]`, `[07:38]`, `[118:26]`
  y `[119:22]`), que por eso tampoco se citan. **Lo de `[118:26]` cuesta una cita**: es lo que el
  trader contesta de diciembre (§3, «Para cerrar»).

### 2.3 El barrido, antes de leer

Con `scripts/barrido_dias.py` de `main`, antes de leer una sola línea de la filtrada:
- **Rango por defecto (18 a 31): 9 líneas**, todas en `[100:21]`–`[118:19]`, y son los códigos de voz
  de S-18 a S-23 y la conversación sobre el código que toca al final de S-23 («ese [N] cerrado»,
  «preguntese [N] cerrada», «[N] creo», «[N] cerrada»). **Ninguna es un día.**
- **Del 1 al 31: 107 líneas**: horas, cantidades («[N] puntos», «[N] sesiones»), marcos de tiempo,
  niveles de la caja y códigos. Ninguna nombra un mes con un día. Dos se miraron con cuidado al leer:
  `[24:11]` «sesión [N]» y `[24:12]` «día [N]», que por el contexto son el rótulo de una cita de la
  hoja leído en voz (el primer día de la sesión 5), sin ningún mes: no son una fecha.

**Sin PARADA.** Los meses que el trader nombra en voz fuera de los bloques: julio (su gráfico), agosto
(«Para cerrar» y su replay perdido), octubre y noviembre (lo que está haciendo ahora, 06:52–07:51),
y ninguno con un día. `casos_ocultos` no se volvió a consultar para ellos.

### 2.4 Lo que se enseñó, y lo que se marcó al leer

**Lo que enseñó el trader.** Compartió su pantalla casi toda la sesión: dibuja sobre los esquemas de
la hoja («vamos a abrir el paint», 05:25) y va a su gráfico de FX Replay para explicar. Lo dice él:
«gráfico más adelante, solo en julio, para no cruzar datos» (05:45–05:49), y lo pregunta a mitad de
S-7 (40:11–40:26). Al buscar el de julio abre primero el que tiene a mano (06:52–07:51; octubre,
según él) y vuelve a julio (08:01–08:04). Ningún día de julio se nombra.

**Los gráficos de S-7 a S-12 no se enseñaron como dice la hoja, y solo dos llegaron a pantalla.**
Medido en la filtrada, contra lo que recordaba Aleks («no se hicieron»):
- **Se pasaron por WhatsApp al trader durante la llamada**, no en la pantalla de Aleks (35:42–36:21).
  Hubo un problema de formato y el trader solo abre imágenes sueltas. **Gráfico 1** (S-7) sí se
  contestó, y **gráfico 2** (S-8) se abrió y quedó «cerrado a medias» (49:46, Aleks por el contexto).
  Los gráficos 3 a 6 (S-9 a S-12) no se hicieron.
- **El limpio, antes que el marcado, en los dos** (respuesta de Aleks, §0.1). La filtrada no lo
  dice; el trader habla de «esta entrada» que habría hecho el bot (49:10–49:14), que casa con que vio
  la marca del gráfico 2. No se abrió un fotograma para saberlo (§0.1).
- **El trader preguntó por la fecha de los gráficos, sin que se le diera:** pide que se ponga
  (48:41–48:50), y la conversación acaba en que «te ponga la fecha» en la siguiente tanda (49:46). No
  dedujo ningún día. Declarado en `HOLDOUT-EXPOSICIONES.md` (2026-11-04). **Para el consultor:** poner
  la fecha va contra la regla 2 de `SESION-DE-PREGUNTAS.md` («sin la fecha visible»), §4.2.

**Tramos de precaución por cifras: ninguno.** No dio ningún agregado ni ninguna cifra de resultados de
un periodo. Al explicar sobre su gráfico nombra el resultado de alguna operación suelta (saca en
stop, queda en break even), sin cifras, como en la sesión 5.

**Tramos ajenos a la operativa**, no citables y sin describir: 1:35:11–1:35:30 y 1:44:19–1:44:30.

### 2.5 Fotogramas: ninguno abierto

Decisión de la sesión, con el precedente de la sesión 5 (§0.1): `frames extract` y `frames check` sí
se hacen (paso 5 de la skill) y las citas salen solo de la filtrada.
- `uv run botsito corpus frames extract --video v17` → `OK: fr-v17-db232fc6 (7200 fotogramas, 0
  extra)`; `uv run botsito corpus frames check` → `OK: 13 extracciones coherentes con el disco; 3
  obligatorios presentes`.

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
3. **El commit del registro se rehízo, por un error de la sesión.** El primer commit del registro
   (`3761b97`, nunca empujado) tocaba `tramos_no_citables.yaml` sin trailer `Fuente:`. Su `make check`
   salió verde, porque el test mira los commits y ese aún no existía; lo cazó el `make check`
   siguiente (`1 failed, 3209 passed`: `tests/contract/test_tramos_fuente.py::test_repositorio_real`,
   `3761b97: toca tramos_no_citables.yaml sin trailer 'Fuente:'`). La skill `ingerir-sesion` no nombra
   ese trailer, y `CLAUDE.md` tampoco (solo el de `knowledge/spec/` y `knowledge/cases/`). `--amend`
   no valía: el hook pide un sello y ese test impide obtenerlo mientras el commit siga ahí. Se
   guardó la fase de v17 con `git stash`, **`git reset --soft HEAD~1` lo lanzó Aleks con «!»** (punto
   siguiente), y `make check` sobre el mismo árbol (`2948d728…`, idéntico al primer sello: el contenido
   no cambió) dejó el commit `b2ddfeb`, con `Fuente: ADR-0021`.
4. **`git reset --soft HEAD~1`, negado por la guardia, PARADA** («`git reset`: subcomando fuera de la
   lista cerrada; puede ejecutar codigo»), y **`git write-tree`, negado igual**, que solo era una
   comprobación y se abandonó. El primero no se reescribió en un guion; lo lanzó Aleks. No es un paso
   que mande la skill.

## Estado

EN CURSO.
