# Sesión 5 con el trader (v15 y v16): la extracción por pregunta

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos ni en las cifras. Cada
> «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de cada respuesta lo
> decide el consultor en otra rama (V, R4.1; encargo del 2026-10-25,
> `docs/encargos/trabajo-sesion-05.md`).

Rama `trabajo/sesion-05`, abierta el 2026-10-25 desde `main` en `7eef8cf` (commit de estado sobre
el merge `68eaa83`, tag `stable/F38c-guardia-alias`). Tramo R4 de la hoja de ruta (R4.1, NA:V).
Skill `ingerir-sesion`, de principio a fin, para los dos vídeos de la sesión (v15, 2026-10-23, y
v16, 2026-10-25). Plantilla: `SESION-04-EXTRACCION.md`. Tag de cierre previsto:
`stable/F38d-sesion-05`.

## Base comprobada al abrir

- `git fetch --prune origin`; en `main`, `git status --short` vacío.
- `git rev-parse --short main` = `7eef8cf`; `git rev-parse main origin/main` da dos veces
  `7eef8cff93b7d5665a21345c10971ba52de775bd`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F38c-guardia-alias`;
  `git rev-parse "stable/F38c-guardia-alias^{commit}"` = `git rev-parse main^1` =
  `68eaa836b9825cb666420accd5abb3e37438af87`; `git ls-remote --tags origin stable/F38c-guardia-alias`
  da `2de0a82… refs/tags/stable/F38c-guardia-alias` (el objeto del tag anotado). Es también el
  primero de `git tag --list 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta a la API de check-runs con el sha literal:
  `python  completed  success  …/actions/runs/40161007232/…`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`
  (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"05": {` en la línea 176, `"05": ORDEN_SESION_05` en
  `HOJAS` (línea 212) y `SESION_EN_CURSO = "05"` (línea 214).
- `docs/runbooks/DECISIONES-DE-PROCESO.md`: la entrada `- 2026-10-21 · Para los encargos, dos
  reglas del consultor…` (línea 28).

## 0. Lo primero

### 0.1 Las respuestas de Aleks a las preguntas a) a d) del encargo (2026-10-25), copiadas tal cual

Preguntadas en el terminal antes del registro de v15 y v16 (encargo, «ENTRADAS»). Las cuatro
decisiones numeradas de a) son del consultor y mandan en esta rama:

> a) v15 (23-oct): SÍ. A lo largo del vídeo el trader compartió su FX Replay y enseñó ejemplos de su operativa con JULIO como mes. NO sé qué días de julio enseñó (puede haber días del 18 al 31, que no son de construcción) ni en qué minutos; tampoco recuerdo si en pantalla se veían cifras de resultados. No habló de septiembre, marzo ni diciembre, que yo recuerde.
>    v16 (25-oct): trátalo igual que v15 (puede que también enseñara el replay de julio; no lo recuerdo con seguridad).
>    Decisión del consultor para esto: (1) en esta rama NO se abre NINGÚN fotograma de v15 ni de v16; frames extract y frames check sí se hacen, pero nadie los mira, y las citas salen solo de la filtrada. (2) Las frases que nombren julio con un día, u otro mes fuera de lo libre, las bloquea la cuarentena por condición del guion; verifica en el registro de cada filtrada cuántos bloques cayeron por eso y decláralo. (3) Declara en HOLDOUT-EXPOSICIONES.md, con fecha de hoy, que Aleks vio en directo el replay de julio del trader en las dos grabaciones, días sin precisar. (4) Si en la filtrada aparece un día de julio del 18 en adelante fuera de un bloque en cuarentena, PARADA sin copiarlo.
> b) v15: de S-1 a S-18 en el orden del PDF; S-18 quedó incompleta al final de v15. v16: S-18 se repitió desde el principio y se siguió hasta S-25, y después «Para cerrar». Se hicieron TODAS: no quedó ninguna para WhatsApp ni para la sesión 6. S-17 está entera en v15. S-18 está en los dos vídeos: la respuesta que vale es la de v16; la de v15 se informa como incompleta.
> c) No lo leí, y ya no hace falta: S-24 se le preguntó directamente al trader en esta sesión. Lo que diga en S-24 sustituye al dato de 1:44:49; en el informe, di qué pasa con H con esa respuesta.
> d) No tengo hoja con notas; solo los vídeos.
>
> Además: el trader confirmó por WhatsApp lo de marzo el 2026-10-25 a las 13:58 (Lima). La captura está en corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-25-1358.png. No la abras ni la registres todavía: el consultor te pasará el texto transcrito en un añadido al encargo.

El añadido llegó el mismo día y está copiado en el encargo como «Ampliación declarada del
2026-10-25: la confirmación escrita de marzo».

Lo que se sigue de ellas:
- **a)** Ningún fotograma de v15 ni de v16 se abre (§2). La cuarentena por condición se mide en el
  registro de cada filtrada, y la exposición del replay de julio se declara en
  `HOLDOUT-EXPOSICIONES.md`. Un día de julio del 18 en adelante fuera de la cuarentena es PARADA.
- **b)** v15 lleva S-1 a S-17 enteras y el arranque de S-18. v16 lleva S-18 entera, S-19 a S-25 y
  «Para cerrar». Nada quedó para WhatsApp ni para la sesión 6, aunque `PREGUNTAS.md` (§1, «Si falta
  tiempo») lo preveía para S-25 y S-23 (WhatsApp) y S-18 (sesión 6). El código de S-17 se busca igual en las dos filtradas, como pide el encargo.
- **c)** El minuto 1:44:49 de v10 no se leyó: no entra ningún dato de Aleks. S-24 de esta sesión
  sustituye a ese dato.
- **d)** No hay hoja con notas: no entra nada en `Sesiones/`.

### 0.2 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), una vez por día, imprime solo `True` o
`False`:
- `2026-10-23`: `False`;
- `2026-10-25`: `False`. **Desviación del paso 1, declarada** (encargo): este día se comprobó
  DESPUÉS de grabar, no antes. Declarada también en `HOLDOUT-EXPOSICIONES.md` (2026-10-25).

Además, el recuento de casos de `casos_ocultos` de `2026-07`, sin imprimir ninguna clave: **0**.
Julio no tiene ningún día oculto.

### 0.3 Los dos vídeos

Son los dos únicos vídeos del primer nivel de `corpus/Estrategia del trader/` que no estaban en
`fuentes.yaml`, que acababa en v14. v15 y v16 son los dos siguientes ids libres.

| | v15 | v16 |
|---|---|---|
| Fichero | `Grabación de pantalla 2026-10-23 174536.mp4` | `Grabación de pantalla 2026-10-25 140140.mp4` |
| Bytes | 6.740.009.101 | 2.324.823.273 |
| Fecha (del nombre) | 2026-10-23 | 2026-10-25 |
| Duración (ffprobe, formato) | **6057,16 s = 1:40:57** (Aleks: 1 h 40 min) | **2089,99 s = 34:50** (Aleks: unos 35 min) |
| Vídeo | h264 1920×1080, 30 fps | h264 1920×1080, 30 fps |
| Audio | AAC estéreo 48 kHz, 6057,16 s | AAC estéreo 48 kHz, 2089,99 s |
| Audio extraído (fuera del repo) | `C:\Users\USER\Desktop\sesion-05-audio\sesion-05-v15.wav`, 193.828.942 bytes | `C:\Users\USER\Desktop\sesion-05-audio\sesion-05-v16.wav`, 66.879.566 bytes |

### 0.4 Dos vídeos para un mismo id de sesión: medido antes del registro

El encargo pide medir si el repositorio admite dos vídeos para un mismo id de sesión antes del
registro. **Lo admite sin tocar código:**
- **`fuentes.yaml`** no tiene campo de sesión: cada vídeo lleva su `fecha_grabacion`, y la sesión
  va en la `naturaleza` y en el comentario. `fecha_grabacion` solo la lee el inventario
  (`corpus/inventario.py:40,82,264`); nada la cruza con la fecha de una sesión.
- **La evidencia** no tiene campo de sesión: cada ítem lleva su `video_id` (por ejemplo
  `knowledge/evidence/v10/ev-v10-011021-02f5dcf3.yaml`). Una respuesta repartida entre los dos
  vídeos se cita en dos ítems, uno por vídeo.
- **El feedback** exige que `fecha` sea la del id de la sesión (`feedback/modelo.py:247-248`) y
  admite `recibido_el` posterior (`:302-307`). La línea que lo dice es `modelo.py:113`: «`fecha`
  es la de la SESION y esta bien asi: fecha la PREGUNTA. `recibido_el` fecha la RESPUESTA.»
  **Para la activación:** un registro de feedback que cite v16 llevará `fecha` 2026-10-23 y
  `recibido_el` 2026-10-25. Desde `CORTE_PROCEDENCIA` los dos campos son obligatorios
  (`:293-299`).
- **La cuarentena** es una lista de vídeos (`SESIONES_EN_CUARENTENA`) y la guardia de Claude Code
  la deduce de `fuentes.yaml` (`drive_id: null` menos v6, `.claude/hooks/guardia.py:327`). Dos
  vídeos con `drive_id: null` entran los dos.
- **`scripts/transcribir_sesion.py`** procesa un audio por ejecución con su `--video`
  (`main`, «uno por ejecucion, porque cada uno lleva los tramos de su video»). Comprueba que el
  sha256 del WAV es el de la transcripción del corpus de ese vídeo (`comprobar_audio_del_video`)
  y nombra sus salidas por el nombre del audio (`salidas_de`). Por eso los dos audios llevan
  nombres distintos.
- **Precedente:** la sesión 2 se partió el mismo día en v7 y v8, sin campo de sesión en ningún
  sitio (`fuentes.yaml`, `SESION-02-VIDEO-V8.md`).

## 1. El registro (v15 y v16)

- **`fuentes.yaml`**: v15 y v16 con `drive_id: null`, su fecha y una `naturaleza` que describe el
  vídeo entero, también el replay de julio que enseñó el trader (respuesta a). Encima, un
  comentario de la sesión partida en dos días. En la descripción de `Mensajes del trader`, la
  captura de marzo (ampliación del encargo).
- **`tests/unit/test_inventario.py`**: `range(1, 15)` → `range(1, 17)`.
- **La captura de marzo** llegó con doble extensión (`mensaje-whatsapp-2026-10-25-1358.png.png`).
  La guardia no deja renombrarla desde la sesión, así que Aleks la renombró con `mv` antes del
  inventario.

### 1.1 El test roto a propósito

Con v15 y v16 ya en `fuentes.yaml` y ANTES de añadirlos a `SESIONES_EN_CUARENTENA`:

```
uv run pytest -q tests/unit/test_cuarentena.py \
  "tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena" \
  "tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo" -p no:randomly
E       AssertionError: assert ['v15: es una... EXCEPCIONES'] == []
E         Left contains 2 more items, first extra item: 'v15: es una sesion (drive_id null) y no esta en SESIONES_EN_CUARENTENA ni en EXCEPCIONES'
E       AssertionError: assert frozenset({'v..., 'v8', 'v9'}) == frozenset({'v..., 'v8', 'v9'})
E         'v16'
E         'v15'
E       AssertionError: assert frozenset({'v..., 'v8', 'v9'}) == {'v10', 'v7', 'v8', 'v9'}
E         'v16'
E         'v15'
FAILED tests/unit/test_cuarentena.py::test_la_lista_cuadra_con_fuentes - Asse...
FAILED tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena
FAILED tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo
```

La guardia ve v15 y v16 en cuarentena en cuanto entran en `fuentes.yaml`, porque los deduce de
allí. Por eso fallan las dos de `test_guardia_claude.py`:
- la segunda, porque la guardia los tiene y el módulo todavía no;
- la tercera, porque el conjunto esperado está escrito a mano.

La primera falla porque el módulo no los tiene en su lista.

Después:
- `src/botsito/corpus/cuarentena.py`: `SESIONES_EN_CUARENTENA` con `"v15"` y `"v16"`;
- `tests/unit/test_guardia_claude.py:152`: el conjunto esperado con v15 y v16;
- `tests/unit/test_cuarentena.py`: el ejemplo sintético de `test_la_comprobacion_de_la_lista_no_es_decorativa`
  lleva v15 y v16, y la sesión sin listar que sondea pasa a v17.

Las mismas tres pruebas pasan (el resultado, en §1.2 con el inventario).

### 1.2 Inventario y hashes

- `uv run botsito corpus inventory`: `OK: manifiesto escrito · heredado_v2: 477 ficheros,
  117,626,282 bytes · material_adicional: 73 ficheros, 6,850,662 bytes · video_original: 16
  ficheros, 63,773,597,529 bytes`. El manifiesto gana tres entradas y nada más: v15 (sha256
  `a91b7f35…2c47f66`), v16 (`4fe72e14…25b43dfb`) y la captura de marzo (`75f9eda2…4577e2c1`).
  Los vídeos pasan de 14 a 16 y el material adicional de 72 a 73.
- `uv run botsito corpus check --hashes`: `OK: el corpus coincide con el manifiesto (hashes)`.
- Las tres pruebas de §1.1 y `tests/unit/test_inventario.py`, después del alta: **55 passed**.

## 2. Audio, cuarentena y holdout

### 2.1 Los cortes de audio

Con las formas de la skill (paso 2): `silencedetect=noise=-50dB:d=30` y `volumedetect` sobre cada
vídeo.

| Vídeo | silencedetect -50 dB, 30 s | volumedetect (vídeo entero) |
|---|---|---|
| v15 | **un silencio: 4946,245–5012,143 s (65,9 s) = 1:22:26–1:23:33** | media −22,7 dB, máximo −0,1 dB |
| v16 | ninguno | media −22,1 dB, máximo 0,0 dB |

**El de v15 es un corte de cero digital.** La misma forma, con `noise=-90dB`, da 4946,570–5011,977 s
(65,4 s): el audio está por debajo de −90 dB. Va a `tramos_no_citables.yaml` como 1:22:26–1:23:33,
redondeado hacia fuera como los de v10, con motivo «SIN AUDIO», y a la `naturaleza` y el
comentario de v15 en `fuentes.yaml`. La puerta del ASR (ningún segmento con `t1` dentro del
corte) se pasa tras la transcripción (§2.2).

### 2.2 v15: transcripción, cuarentena y puerta del ASR

- **Transcripción del corpus**, tras el «listo» de Aleks: `uv run botsito corpus transcribe --video
  v15` → `tr-v15-large-v3-int8-float16-2ec65e67`, **1344 segmentos**. `corpus transcript check`:
  `OK: 16 transcripciones coherentes con el disco y el glosario`.
- **El guion de `main`** (`git diff --quiet main -- scripts/transcribir_sesion.py`: idéntico):
  `--audio C:/Users/USER/Desktop/sesion-05-audio/sesion-05-v15.wav --sesion 05 --video v15`, a
  continuación, nunca a la vez. El registro (`sesion-05-v15.registro.txt`) dice:
  - hoja: la de la sesión 05;
  - audio comprobado: el sha256 de su WAV (`796fbb1c7aea…`) es el de la transcripción del corpus de
    v15;
  - ASR de 1188,6 s (factor 0,20); **1344 segmentos**, los mismos que la transcripción del corpus;
  - **segmentos en cuarentena: 0 en 0 bloques**; segmentos tapados por tramos: 0; bloques
    `[NO CITABLE]`: 0;
  - códigos detectados: S-1 00:10, S-2 01:51, S-3 03:59 (×2), S-4 07:40, S-5 16:02, S-6 19:31,
    S-7 28:19, S-8 36:26, S-9 41:19, S-10 51:41, S-11 51:46, S-12 58:50, S-14 80:27, S-15 80:29,
    S-16 86:45; sin código detectado, S-13, S-17 a S-25.
- **La cuarentena por condición (decisión 2 del consultor): 0 bloques.** Ningún segmento de v15
  nombra un mes con días reservados o sin demostrar libre, ni trae una fecha numérica ni un día de
  la semana con número.
- **La premisa de la decisión 2, medida (CLAUDE.md, «Como se trabaja»: gana la medida).** La
  decisión dice que la cuarentena por condición bloquea las frases que nombran julio con un día. **No
  es así para julio.** Julio es un mes libre (`meses_libres`: 1, 4, 7, 8, 10, 11 y 12), y la regla
  de fecha solo casa formas numéricas. Con frases SINTÉTICAS, sin leer ninguna transcripción
  (`motivos_cuarentena` con los meses libres):
  - «el 21 de julio», «veintiuno de julio», «el día 21», «aquí en julio, el 24» y «julio 28» → no
    se tapan;
  - «el lunes 21» → día de la semana con número; «21/07» → fecha numérica; «el 21 de marzo» → mes.

  Por eso la decisión 4 (PARADA ante un día de julio del 18 en adelante fuera de cuarentena) se
  aplicó con un detector propio ANTES de leer. `detector_julio.py`, en la carpeta de trabajo,
  imprime solo marcas de tiempo, el tipo de coincidencia y un booleano «18-31». En v15 dio:
  `lineas con texto: 1344; lineas que nombran julio: 0` y una coincidencia «día + número»
  (08:47) con `18-31=no`. **Ningún día de julio, sin PARADA.**
- **La puerta del ASR del corte SIN AUDIO.** El guion tapa todo segmento que SOLAPE un tramo
  (`tapados_por_tramos`, `s.t1_ms > a and s.t0_ms < b`, `scripts/transcribir_sesion.py:307`) y tapó
  **0**. Ningún segmento solapa 1:22:26–1:23:33, así que tampoco hay ninguno con `t1` dentro. Las
  marcas de la filtrada alrededor, impresas solas, saltan de `[82:10]` a `[84:00]`.

### 2.3 v15: lo que enseñó el trader, y los tramos que se marcaron al leer

**Lo que se enseñó.** Los esquemas inventados de la hoja se enseñaron en pantalla, y el trader los
comenta y corrige varias veces («el ejemplo del esquema inventado está mal planteado», 61:59). Para
responder, **el trader compartió su FX Replay** (respuesta a de Aleks): traza ejemplos sobre su
replay y dibuja un esquema propio «con un paint» (S-14, 72:46).

**Los meses que nombra en voz: ninguno.** El detector no encuentra «julio» y la cuarentena no tapa
nada.

**Tramos de precaución (ADR-0021 §2), marcados al leerlos** en `tramos_no_citables.yaml` y
declarados en `HOLDOUT-EXPOSICIONES.md` (2026-10-25). Aquí solo se dice dónde están; **ninguna
cifra se copia y ninguna se usa** (la lección de la sesión 4: `HOLDOUT-EXPOSICIONES.md`, filas del
2026-10-04).
- **0:10:21–0:14:43** (dentro de S-4): sobre su replay, cuenta resultados de operaciones y de
  sesiones concretas y da cifras agregadas de esos días.
- **1:14:41–1:16:52** (dentro de S-14): busca «el día más reciente» de su backtest y comenta el
  resultado de sus operaciones y de sus sesiones.
- **1:17:52–1:18:06** (dentro de S-14): dos cifras agregadas, porcentajes, de las sesiones de su
  replay.

Fuera de ellos, al explicar una regla sobre su replay, nombra el resultado de alguna operación
suelta (gana, pierde, queda en break even), sin cifras.

**Tramos ajenos a la operativa**, no citables y sin describir: 0:41:22–0:41:36, 0:59:09–1:00:03
(conversación personal) y 1:40:37–1:40:58 (el final de la grabación, tras cortarse S-18).

### 2.4 Fotogramas: ninguno abierto

Decisión 1 del consultor (respuesta a): en esta rama no se abre ningún fotograma de v15 ni de v16.
`frames extract` y `frames check` sí se hacen (paso 5 de la skill); las citas salen solo de la
filtrada.
- v15: `uv run botsito corpus frames extract --video v15` → `OK: fr-v15-5dcfa8d3 (6058 fotogramas,
  0 extra)`; `uv run botsito corpus frames check` → `OK: 11 extracciones coherentes con el disco; 3
  obligatorios presentes`.
- v16: `uv run botsito corpus frames extract --video v16` → `OK: fr-v16-21754f20 (2090 fotogramas,
  0 extra)`; `uv run botsito corpus frames check` → `OK: 12 extracciones coherentes con el disco; 3
  obligatorios presentes`.

### 2.5 v16: transcripción y cuarentena

- **Transcripción del corpus**, tras el segundo «listo» de Aleks: `uv run botsito corpus transcribe
  --video v16` → `tr-v16-large-v3-int8-float16-dc91b386`, **526 segmentos** (cuatro fragmentos:
  148, 117, 167 y 94). `corpus transcript check`: `OK: 17 transcripciones coherentes con el disco y
  el glosario`.
- **El guion de `main`**, igual que para v15: `--audio
  C:/Users/USER/Desktop/sesion-05-audio/sesion-05-v16.wav --sesion 05 --video v16`. El registro
  (`sesion-05-v16.registro.txt`) dice:
  - hoja: la de la sesión 05; tramos no citables del vídeo: 0 (aún no había ninguno);
  - audio comprobado: el sha256 de su WAV (`1ae80e35e431…`) es el de la transcripción del corpus de
    v16;
  - ASR de 674,8 s (factor 0,32); **526 segmentos**;
  - **segmentos en cuarentena: 7 en 2 bloques**, tapados solo por meses; motivos «mes» 3 y
    «vecino» 4; bloques `[NO CITABLE]`: 0;
  - códigos detectados: S-18 00:10, S-19 06:33, S-20 18:52, S-21 18:53, S-22 21:37, S-23 26:48,
    S-25 29:02; sin código detectado, S-1 a S-17 (de v15) y S-24.
- **La cuarentena por condición (decisión 2 del consultor): 2 bloques**, `[CUARENTENA 32:58–33:07]`
  y `[CUARENTENA 33:11–33:22]`, los dos en «Para cerrar» y caídos por un mes (más el vecino de cada
  uno). No se leen. Por el contexto visible (§3, «Para cerrar»), son la petición de la confirmación
  escrita de marzo; su contenido se da por la declaración de Aleks, como manda el añadido.
- **Los dos bloques, a `tramos_no_citables.yaml`**, sin contenido y en un commit propio (paso 4 de
  la skill; encargo, «El recorrido»), con el criterio de «Los límites de un tramo»
  (`SESION-DE-PREGUNTAS.md`): **0:32:58–0:33:08** y **0:33:11–0:33:23** (el fin de cada bloque más
  un segundo). Control positivo: cada bloque cabe entero en su tramo. El segundo de margen del
  segundo tramo toca la primera línea visible tras el bloque (`[33:22]`), que por eso tampoco se
  cita.
- **Sin corte de audio** (§2.1), así que no hay puerta del ASR que pasar en v16.

### 2.6 v16: lo que enseñó el trader, y los tramos que se marcaron al leer

**El detector antes de leer** (`detector_julio.py`, hoy en `anexos/SESION-05/`): `lineas con texto:
519; lineas que nombran julio: 7`, 6 coincidencias, dos con `18-31=SI` (29:02 `julio+num` y 32:10
`vecino`). Con el número enmascarado (`enmascarar_lineas.py`, en la carpeta de trabajo) las dos son
el código de voz de S-25 («pregunta ese [N]», «ese [N] cerrada»), no un día: sin PARADA, y se leyó
la filtrada entera.

**Los meses que nombra en voz**, fuera de los dos bloques: julio (el Excel de julio de S-25 y los
días «del 1 al 17», que no llegan al 18), agosto (la exportación, «Para cerrar») y diciembre
(pendiente de grabar). Ninguno tiene días en `casos_ocultos`. Y la fecha de la grabación, «Hoy, [N]
del 10», que la cuarentena no tapa (§2.7, segundo hallazgo).

**La PARADA (§2.7).** Al leer, en 0:31:04, dentro de S-25, el trader dice hasta qué día de julio
llegó su backtest: un día del 18 en adelante, fuera de los bloques. El detector no la había marcado;
la vio después el barrido ancho. El número no se escribe en ningún sitio.

**Tramos de precaución**, en `tramos_no_citables.yaml` y declarados en `HOLDOUT-EXPOSICIONES.md`
(2026-10-25, fila de v16). Aquí solo se dice dónde están; **ninguna cifra se copia y ninguna se
usa**:
- **0:20:02–0:21:16** (entre S-20 y S-21): cifras agregadas de sus backtests, una racha de pérdidas
  de un mes y cuántas operaciones caben en un día, sobre un rango que puede incluir meses
  reservados. Decisión de la sesión con la regla de ADR-0021 §2.
- **0:30:41–0:31:37** (dentro de S-25): enseña su replay de julio y dice hasta qué día llegó su
  backtest. Decisión del consultor (§2.7, punto 1). La respuesta a S-25, desde 0:31:37, queda fuera.

**Tramos ajenos a la operativa: ninguno.** El final (33:36–34:41) es la disponibilidad del trader
para más sesiones y la explicación de Aleks del error de fidelidad de agosto; es de la operativa y se
cita (§3, «Para cerrar»).

### 2.7 La PARADA de v16 y la respuesta del consultor

**La PARADA (2026-10-25)**, por la decisión 4 del consultor («Si en la filtrada aparece un día de
julio del 18 en adelante fuera de un bloque en cuarentena, PARADA sin copiarlo»):
- **Dónde y qué.** v16, en 0:31:04, dentro de S-25 y dentro de lo que hoy es el tramo de precaución
  0:30:41–0:31:37. Lo que pasa ahí se dice solo con el motivo de ese tramo: el trader enseña su
  replay de julio y dice hasta qué día llegó su backtest, un día del 18 en adelante. Ninguna
  operación, ningún resultado y ningún detalle de ese día. *(Corregido tras el revisor, hallazgo a3:
  la primera redacción, escrita antes de que el tramo existiera, citaba dos frases de dentro del
  tramo y describía dónde aparecía la palabra «julio».)*
- **Por qué no la paró el detector antes de leer.** `detector_julio.py` solo marcaba un número junto
  a «julio» o «día» en la misma línea o en la contigua, y esa línea no tiene ninguna de las dos
  palabras. El detector no la marcó, se leyó la filtrada entera y se vio al leerla.
- **El barrido ancho, después** (`barrido_18_31.py`, hoy en `anexos/SESION-05/`): toda línea con un
  entero suelto de 18 a 31, impresa con el número sustituido por `[N]`. En v15 no hay ningún día de
  julio (salen pips, minutos, horas de la pregunta, el 29 de abril de la hoja y un código). En v16
  esta línea es la única que es un día de julio; las otras seis son códigos de voz, «[N] páginas» y
  la fecha de hoy.
- **Segundo hallazgo, que no bloquea.** La regla de fecha numérica de la cuarentena no tapa una fecha
  seguida de coma. Con texto sintético: `motivos_cuarentena('hoy 25 del 10')` da
  `['fecha numerica']`, y `motivos_cuarentena('hoy, 25 del 10,')` da `[]`. El lookahead `(?![\d.,])`
  excluye la coma para no tapar precios como «10,5», y con ello deja pasar fechas en prosa. Aquí
  solo dejó a la vista la fecha de la propia grabación.

**La respuesta del consultor (2026-10-25)**, copiada tal cual:

> Respuesta del consultor a la PARADA de v16 (2026-10-25). Cópiala al informe, en su sección.
>
> 1. SÍ, opción (a): v16 de 0:30:41 a 0:31:37 entra en tramos_no_citables.yaml como tramo de precaución (motivo: el trader enseña su replay de julio y dice hasta qué día llegó su backtest, un día del 18 en adelante). El número no se escribe en ningún sitio: ni en el informe, ni en HOLDOUT-EXPOSICIONES.md, ni en un commit, ni en el chat. La respuesta a S-25 (0:31:37 a 0:32:10) queda fuera del tramo y se puede citar.
> 2. HOLDOUT-EXPOSICIONES.md, con fecha de hoy: la sesión leyó, al leer la filtrada de v16, el día en que acaba el backtest de julio del trader (un día del 18 al 31), sin ninguna operación, resultado ni detalle de ese día; el número no se registra. Y por qué pasó: el detector de la sesión (detector_julio.py, en el scratchpad) era más estrecho que la regla del encargo (solo un número junto a «julio» o «día»).
> 3. Para el resto de la rama: antes de leer cualquier filtrada (o volver a leer una), se pasa primero el barrido ancho (barrido_18_31.py, con el número enmascarado), y solo después se lee. Si sale otra línea con un día de julio del 18 en adelante, PARADA como esta. Copia los dos scripts del scratchpad a docs/validation/anexos/SESION-05/ para que el revisor los vea.
> 4. El segundo hallazgo (la fecha numérica seguida de coma que la cuarentena no tapa, con la prueba sintética) va preparado en el informe como una línea de Technical Debt para la orden de cierre, del carril de guardias y de la cuarentena por condición. No se arregla en esta rama.
> 5. El dato de hasta dónde llega el backtest de julio NO se usa para U (julio del 20 al 31) ni para nada más. Cuando toque U, el consultor se lo pregunta a Aleks o al trader por su vía.
>
> Sigue con v16 (tramos, informe, commit) y con lo que quede, como dice el encargo.

**Cómo se aplicó, punto por punto:**
1. Hecho: el tramo 0:30:41–0:31:37 de v16 en `tramos_no_citables.yaml`, con el motivo del punto 1 y
   sin el número.
2. Hecho: fila de v16 en `HOLDOUT-EXPOSICIONES.md` (2026-10-25), punto (3) de la fila.
3. Hecho: los dos guiones, en `docs/validation/anexos/SESION-05/` (el contrato se amplió con esa
   carpeta en el commit de v16). `barrido_18_31.py` va tal cual; `detector_julio.py` va con su
   expresión `DIA_NUM` partida en tres líneas por `ruff format` (la misma cadena; su salida sobre la
   filtrada de v16, repetida desde el anexo, es idéntica). El barrido se pasó otra vez sobre v16
   antes de releer las líneas de los límites de los tramos: da las mismas siete líneas y solo la de
   31:04 es un día de julio. `enmascarar_lineas.py`, con el que se leyeron enmascaradas las
   coincidencias del detector, sigue en la carpeta de trabajo (no lo pidió el punto 3).
4. Preparado en §6 (la línea de Technical Debt).
5. Queda dicho: el dato no se usa para nada.

## 3. Por pregunta

**Cómo se leen las filas.** Cada código lleva su vídeo y su tramo (mm:ss, minutos totales desde el
inicio del audio de ESE vídeo), el literal de la FILTRADA y la propuesta: resuelve / resuelve en
parte / no resuelve. La transcripción no separa voces: la pregunta la lee Aleks en voz alta y el
trader contesta, a menudo repitiendo la pregunta o sus opciones en la misma línea; el hablante se
atribuye por contexto y, donde una línea mezcla a los dos, se dice. Las citas se copian sin
corregir el ASR (por ejemplo «salsista» por «alcista», «break event» por «break even»).

**Cómo se agrupó la filtrada de v15.** El guion agrupa por el primer código que detecta. El ASR oyó
«Pregunta S3» a las 66:09 donde se dijo S-13, así que la cabecera `## S-3` de la filtrada junta S-3
(03:59–07:40) con S-13 y S-14 (65:54–79:56). S-17 (93:03–98:07) y el arranque de S-18 (98:07–100:37)
van bajo `## S-16`, porque sus códigos no se detectaron. La localización se hizo a mano, por los
códigos dichos en voz («pregunta S7», «ese 6 cerrada», «S15 cerrada»…), que están todos en la
filtrada.

### 3.1 Las dos bloqueantes

#### S-3 · Cuándo das por formado un alto o un bajo de M15 · A-35 (bloqueante)

- **Vídeo y tramo:** v15, 03:59–07:40.
- **La respuesta:** «[04:47] Vale, en este caso sería pues en cuanto la vela roja de después ya
  cerrado, de esa manera pues nosotros tenemos de una manera más clara como trazar la zona lineal de
  liquidez en M15, la B.»
- **Para precisar, la vela sin cuerpo:** «[05:30] No cuenta como vela de después, no cuenta como
  vela de después si cierra sin cuerpo.»
- **Para precisar, la mecha que pasa el alto y vuelve:** «[05:53] Ah, se actualiza el de la mecha»
  / «[05:54] Se actualiza el de la mecha». Lo enseña en su replay: «[06:49] y así ahora mira qué pasa
  qué pasaría si por ejemplo aquí no nos deja una mecha nos deja una [06:58] mecha y cierra roja por
  debajo entonces nosotros actualizaríamos allí de esa manera lo ubicaríamos».
- **Para precisar, el bajo:** «[07:07] vale ahora sí eso por ejemplo en cuanto a bajista pues sería
  lo mismo como es operativa bajista».
- **Propuesta: RESUELVE la primera mitad.** Es la opción (b), que `ACTIVAR-A35-A44.md` §1 lee como
  `liquidez_m15_pivote_formado = cierre_vela_contraria`. Cae en una lectura documentada: **no hay
  PARADA de §4** por esta mitad.
- **Lo que pide el runbook para activarla:** dos registros, uno sobre A-35 (RESOLVE_UNKNOWN) y otro
  sobre `liquidez_m15_pivote_formado` con `--valor cierre_vela_contraria`, con esta cita y su tramo
  (fecha 2026-10-23, recibido_el 2026-10-23); después los cinco sitios de §3 y los tests de §2.
- **La segunda mitad («¿qué haces si después el precio lo supera un poco?») no tiene parámetro hoy**
  (§1 del runbook): se lleva al consultor con los candidatos de `PREPARACION-A35-A44.md` §5. Lo que
  dijo añade dos cosas que el mecanismo de hoy tiene fijas y visibles (`domain/pivotes_m15.py`): una
  vela sin cuerpo no cuenta como vela de después, y **cuando el precio pasa el alto solo con la mecha
  y vuelve, el alto pasa a ser el de la mecha** («se actualiza el de la mecha»). Lo segundo no casa a
  la primera con lo que dijo en la sesión 4 («lo tiene que pasar con cuerpo, no con mecha»,
  `ev-v10-012456-9dc1d221`): allí hablaba de cuándo un alto queda TOMADO, y aquí de qué alto se usa
  después. Es una lectura que hay que mirar: no se decide aquí.
- **Regla general:** sí (la da como regla y la enseña). **«creo»:** no. **Compra y venta:** sí (07:07).

#### S-4 · El tope de la semana · A-44 (bloqueante)

- **Vídeo y tramo:** v15, 07:40–15:59. Dentro va un tramo de precaución (10:21–14:43, §2.3) que no
  se cita.
- **La respuesta:** «[08:57] no» / «[08:58] solo el del día y las» / «[09:00] 9 seguidas» /
  «[09:03] la respuesta es la A».
- **Para precisar, el 9 % de la sesión 1:** «[09:13] bueno, creo que» / «[09:14] aquí hay un error,
  sería 9 pérdidas seguidas» / «[09:17] planteándolo» / «[09:18] a porcentajes, sería un 4,5».
- **Para precisar, el miércoles:** primero «[09:36] Sí, vuelvo el lunes siguiente»; al volver a la
  pregunta, se corrige: «[15:20] si se llega a tener 9 pérdidas seguidas» / «[15:24] que traducido
  a porcentaje» / «[15:26] sería un 4.5» / «[15:28] pues volveríamos a lo mejor» / «[15:30] el
  próximo lunes» / «[15:31] o inclusive yo diría» / «[15:32] en lugar del próximo lunes» / «[15:34] al
  día siguiente» … «[15:46] tienes tope de semana y lo tocas un miércoles» / «[15:49] vuelves el
  lunes siguiente» / «[15:50] no, vuelvo el día siguiente» / «[15:52] y ya está».
- **Propuesta: RESUELVE EN PARTE.**
  - El alcance es la opción (a): `perdida_trader_alcance: dia` (`ACTIVAR-A35-A44.md` §1).
  - La unidad, porcentaje: «a porcentajes, sería un 4,5» (con «creo»).
  - **La magnitud no la dijo** (saldo o equity). La confirmación final de la hoja («del saldo con
    el que empiezo el día») no se oye leída en v15. El runbook pide «dia, más magnitud y unidad».
    Con esta respuesta la magnitud solo tiene `fb-2026-09-09-sesion-01-bff260ea`, un CORRECT sobre
    `perdida_maxima_diaria`, que el consultor ya dijo que no basta (decisión del 2026-10-19 sobre
    b10, `PREGUNTAS.md` S-4).
  - **No tiene tope de semana**, y del 9 % de la sesión 1 dice que es un error. Eso contradice
    `perdida_maxima_semanal = 9` (CONFIRMED): según la tabla del runbook, «un tope distinto de los
    de la sesión 1» no se sobrescribe aquí; es un CORRECT que revisa el consultor.
  - Liga el 4,5 % del día a las 9 pérdidas seguidas («traducido a porcentaje»).
  - El reinicio, «al día siguiente», sin reloj: `perdida_trader_reinicio_huso` se queda UNKNOWN
    (tabla del runbook).
- **¿PARADA de §4?** No por el alcance, que cae en (a). **Sí por la magnitud**: con lo dicho en
  voz falta un valor que el runbook pide. Decide el consultor.
- **Regla general:** sí. **«creo»:** sí (09:13). **Compra y venta:** no aplica.

### 3.2 Las dos de las que dependen los ADR provisionales

#### S-5 · El lote que no cabe · A-57 (de ella depende ADR-0081)

- **Vídeo y tramo:** v15, 16:02–19:27.
- **La respuesta:** «[17:57] Bueno, eso es un buen punto.» / «[17:58] Pero en este caso lo más
  óptimo por ahora, planteándolo, creo que sería pues no usar una gestión, o sea, fija en cierta
  parte.» / «[18:08] O sea, opción A.» / «[18:11] Claro, bajo el lote y a lo que cabe y entro igual.»
- **Para precisar** (cuenta real; si cambia el stop o el objetivo): «[18:36] … no me ha pasado yo he
  estado trabajando o sea y no he tenido [18:45] problemas … [18:53] … en cuanto al otaje y todo eso
  se seguía [19:00] manteniendo el rr o sea no he tenido problemas».
- **Antes de contestar**, el trader pregunta a Aleks qué recomienda («[17:10] ¿Tú qué
  recomendación planteas»), y la respuesta de Aleks nombra un riesgo máximo posible («[17:29] lo
  máximo que vas a poder arriesgar» …) y plantea la disyuntiva («[17:39] … si mantener [17:41] Tener
  una gestión de riesgo fija o por ende poder como variarse»). **La respuesta del trader viene
  después de la del consultor**, que se atribuye por contexto: lo hace notar el informe para que lo
  pese quien la active.
- **Propuesta: RESUELVE.** Es la (a), que es lo que hace hoy el bot (`lote_si_no_cabe = limitar`,
  ADR-0081). No ha vivido el caso en su cuenta; con menos lote no cambia nada más, porque «se seguía
  manteniendo el rr».
- **Regla general:** sí, pero con «por ahora». **«creo»:** sí (17:58). **Compra y venta:** no
  aplica.

#### S-6 · Las reentradas en el mismo punto tras un stop, y su caja (la «pregunta 3» de ADR-0083)

- **Vídeo y tramo:** v15, 19:31–28:19.
- **La lectura de la pregunta y el arranque** van en una línea larga que mezcla a los dos («[20:01] …
  cuántas reentradas en el mismo que traes un stop, dos hasta agotar los tres cartuchos y la caja de
  la negación, vale, para precisar, y traes un break even, vuelves al mismo punto, traes un break,
  vale, creo que esto más que nada lo ha planteado, sabes que, por el hecho de los equal que nos
  suele generar,»).
- **Lo que dice:**
  - de las reentradas en el mismo nivel: «[20:29] pero, si soy sincero hermano» / «[20:32] me lo estoy
    pensando» / «[20:34] y me da unas ganas» / «[20:36] de replantearme para poder quitar esa» /
    «[20:37] condicional cuando hay break even» / «[20:39] porque siento yo» / «[20:40] que las veces
    que he hecho backtesting» / «[20:43] o sea, son las que nos generan» / «[20:46] un gran» /
    «[20:47] cúmulo de pérdidas»;
  - en un ejemplo de su replay, reentra en el mismo nivel tras cada stop, con la caja actualizada:
    «[23:25] … nosotros sería cuestión de actualizar la zona aquí [23:33] o sea sigue quedándose en el
    mismo punto nosotros lo validamos y lo que lo actualizaríamos allí [23:41] y mira nuevamente nos
    saca» y «[24:41] O sea, solo vemos el punto, si te das cuenta» / «[24:43] El punto 1» / «[24:45]
    Que allí, solo que» / «[24:47] Se actualiza del nivel 0» / «[24:49] Allí abajo, y ya está»;
  - y la valoración: «[25:05] … estas entradas yo lo he estado viendo como [25:15] como que no
    deberían creo yo de estar o sea cuando tenemos el equal mejor esperamos solo [25:21] y lo ideal
    sería pues una vela contraria con una vela roja independientemente de estos equals»;
  - de repetir la entrada en el mismo nivel sin haber perdido antes: «[26:10] … si es un nivel, o
    sea, nuevo que ha generado el precio, pues es a donde nosotros tratamos de buscar la operativa,
    pero si es un nivel donde el precio, pues ya, digámoslo así, se ha perdido, o sea, ha roto y todo
    eso quedaría invalidado,» y «[27:11] entonces al final de» / «[27:12] cabo son decisiones
    diferentes, o sea» / «[27:14] puede volver a coincidir en algunos» / «[27:16] casos, sí, por el
    desarrollo» … «[27:26] … para nosotros validar» / «[27:29] una zona de aquí de» / «[27:30] un
    posible punto» / «[27:31] breaker tiene que haber roto por encima» / «[27:32] porque si no está
    roto por» / «[27:34] encima, nosotros no lo validamos».
- **Propuesta: RESUELVE EN PARTE, y no confirma ADR-0083 tal cual.**
  - **No da un número de reentradas.** Cada reentrada es una decisión independiente, que puede
    caer en el mismo nivel si el precio vuelve a validar el punto, y para validarlo tiene que haber
    roto.
  - **La caja de la reentrada se actualiza en parte.** En su ejemplo dice «actualizar la zona» y
    «se actualiza del nivel 0 allí abajo», pero «el punto 1» sigue y «aquí sigue marcando el mismo
    nivel» (24:51). Si es la caja del primer intento o una nueva no lo dice con esas palabras.
    *(Corregido tras el revisor, hallazgo a2: la primera redacción decía «no es la del primer
    intento», y la cita no lo sostiene.)*
  - **Sobre las reentradas en niveles iguales («equals») duda en voz alta**: le dan «ganas de
    replantearme» y cree que «no deberían de estar». Es una opinión con «creo», no una regla.
  - **Tras un break even:** lo que dice («quitar esa condicional cuando hay break even») no llega
    a responder si vuelve al mismo punto.
  - ADR-0083 (hoy: vuelve tras pérdida o break even, con la caja que dé el productor, hasta tres
    pérdidas por liquidez) sigue PROVISIONAL: la respuesta no lo confirma ni lo niega con una regla.
- **Regla general:** en parte (lo de validar el punto de nuevo). **«creo»:** sí (25:15). **Compra y
  venta:** no lo dice.

### 3.3 El resto, en el orden de la hoja

#### S-1 · Con el sesgo bajista, una H4 rompe el máximo de la anterior solo con la mecha y cierra roja

- **Vídeo y tramo:** v15, 00:10–01:48.
- **La respuesta:** «[00:49] sigue bajista, claramente» / «[00:53] porque la regla» / «[00:55] O sea,
  dice que para que pueda hacer al menos eso, al cambiar el sesgo, pues tendría que cerrar con mecha
  por arriba del sesgo bajista anterior, con cuerpo, con mecha.» / «[01:09] Pero en este caso, como
  cierra bajista, pues sigue siendo bajista.»
- **Para precisar:**
  - lo lejos que llega la mecha: «[01:21] no, no importa» / «[01:22] o sea, basta que sea» /
    «[01:25] por un pip» / «[01:26] o un punto, pues sirve»;
  - el tamaño del cuerpo: «[01:30] el cuerpo rojo, tampoco importa»;
  - cuándo se decide: «[01:38] se decide al cierre de esa vela» / «[01:40] nunca se cambia» /
    «[01:42] la idea durante la vela siguiente».
- **Propuesta: RESUELVE: (b), sigue bajista.**
  - **Casa con la regla del color activa** (ADR-0080; el caso 3 del WhatsApp del 2026-10-14, «sigue
    bajista»), que es lo que hace hoy el motor.
  - **Choca con la sesión 1**, tal como la lleva `SESGO-H4-COLOR.md` §1.c (v6 1:04:30–1:05:35, el
    2026-09-09: «aunque fue roja la vela, pues es indiferente … la siguiente operativa es alcista»).
    Es la contradicción de ADR-0080 §9. Esta respuesta, en voz y sobre el esquema, va con el
    WhatsApp y contra la sesión 1.
  - Añade que se decide al cierre de la vela y no se cambia durante la siguiente.
- **Regla general:** sí («porque la regla … tendría que cerrar … por arriba»). **«creo»:** no.
  **Compra y venta:** solo el caso bajista.

#### S-2 · La H4 que rompe con la mecha y cierra sin cuerpo

- **Vídeo y tramo:** v15, 01:51–03:57.
- **La respuesta:** «[02:56] Claro, en este caso sería la respuesta B, no, sigue el sesgo que había,
  que en este caso es alcista, como con la vela neutra que rompe por los dos lados, o sea, la
  respuesta es la B.»
- **Para precisar**, la mecha que pasa por mucho: «[03:32] No, es indiferente, o sea, si cierra de
  manera neutra, o sea, sin cuerpo» / «[03:37] Pues independientemente del número de recorridos que
  desarrolle su mecha» / «[03:44] Sigue planteándose el sesgo, en este caso anterior, que sería
  alcista».
- **Propuesta: RESUELVE: (b).** Casa con ADR-0080 §4 (la decisión provisional del consultor sobre
  la ruptura simple sin cuerpo; hoy el motor hace (b)).
  - La subpregunta del caso al revés (rompe el máximo con el sesgo bajista y cierra sin color) se
    leyó (03:17), pero la respuesta vuelve al ejemplo alcista («sería alcista»). La regla que da,
    «sigue el sesgo anterior», cubre los dos lados, pero el caso bajista no lo dijo con sus
    palabras.
  - Con la sesión 1 no hay choque: allí el caso era una vela con color.
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** la regla sí; el caso bajista no.

#### S-7 · Los dos extremos de la caja: dónde pones el 0 y hasta dónde llevas el 1 · A-48 y A-49

(Hoja: el texto del recuadro del 2026-10-21; se oye leído: «[28:19] … dicen los dos extremos de la
caja» / «[28:40] Donde pones el 0 y hasta donde llevas el 1».)
- **Vídeo y tramo:** v15, 28:19–36:26.
- **Lo que dice:**
  - del esquema: «[31:17] o sea, aquí el ejemplo lo ha planteado» / «[31:19] un poco mal creo yo»;
  - cómo se traza: «[30:00] … el punto breaker sería aquí, en este caso sería aquí, y aquí tiene
    obviamente que la vela terminar por encima,» / «[30:41] con mecha al menos en M1» / «[30:42]
    porque todo esto es contexto de M1» … «[31:23] sería esta, o sea que el precio» / «[31:25] en
    M1, contexto de M1» / «[31:27] pues llegue, retrocede» / «[31:29] hasta allí está bien, genera
    una subida» / «[31:31] la vela cierre con cuerpo con mecha» / «[31:32] por arriba, o sea tenemos»
    / «[31:35] que esperar, por eso es muy importante» / «[31:36] esperar el cierre de cómo termina
    esta vela verde»;
  - en una venta de su replay: «[32:44] … entonces nosotros tendríamos el trazo desde aquí hasta
    aquí, esperamos el cierre, o sea, sea una vela verde o una vela roja, entonces trazaríamos el
    nivel 0 desde aquí y el nivel 1 desde el punto más alto, donde cierra, …»;
  - del 0 en el último alto de M1: «[34:02] el 0, porque» / «[34:05] es que no entiendo porque lo
    tendría» / «[34:08] que poner en el último alto de m1 que se formó porque como digo el ejemplo lo
    tiene mal planteado …»;
  - de si actualiza siempre: «[34:41] … claro sea usualmente la caja se va a ir actualizando …» y
    «[35:16] formando otra vela roja se sigue manteniendo el punto breaker porque no se nos ha
    desarrollado [35:22] otro posible punto breaker entonces vamos actualizando así» y «[36:03] … así
    continuamente hasta que obviamente pues o se desarrolla otra zona de liquidez [36:14] otra zona
    de liquidez no otro posible punto breaker … [36:19] … como estamos en un flujo alcista vamos
    utilizando el 1» / «[36:26] conforme va desarrollándose».
- **Propuesta: RESUELVE EN PARTE.**
  - No elige ninguna opción con su letra.
  - De lo que dice salen dos cosas. La caja se traza al CIERRE de la vela que rompe («tenemos que
    esperar … el cierre»), lo que va hacia A-49 con velas cerradas. Y el 1 se va actualizando
    mientras el precio se desarrolla y no aparece otro punto («vamos utilizando el 1 conforme va
    desarrollándose»), lo que se parece a la (c) (`caja_bloque = r6`, el valor de hoy) más que a
    (a) o (b).
  - Del 0 en el último alto de M1 (`orden_stop_punto`) dice que no entiende la pregunta y corrige el
    esquema: no resuelve.
  - «Usualmente» la caja se va actualizando: no dice «siempre».
- **Regla general:** en parte. **«creo»:** sí (31:19, sobre el esquema). **Compra y venta:** sí
  (enseña una venta, 32:44).

#### S-8 · Una vela sin cuerpo dentro del tramo que marca el punto de breaker

- **Vídeo y tramo:** v15, 36:26–41:17.
- **Lo que dice:** «[39:59] Ahora, entonces, otra cual sería lo que he descrito con anterioridad,
  ahora para precisar, cambia algo si son 3 velas sin cuerpo en vez de una, es indiferente, o sea,
  las velas sin cuerpo pues no cuentan, en venta lo mismo revés es igual, …» y «[40:29] Ahora, para
  confirmar al final, si entre la vela verde y la vela roja hay velas en cuerpo, el máximo de la
  verde es un punto breaker.» / «[40:37] Sí, sería un punto breaker, pero claro, como digo, tiene que
  cumplir esa condicional de que el precio, pues, haya venido de un order flow bajista.» / «[40:46]
  Esto haya llegado hasta aquí por debajo, aquí puede haber todas las velas que quiera, no pasa
  nada, pero luego nos tiene que romper, o sea, tiene que cerrar por debajo.»
- **Propuesta: RESUELVE: (a) con una condición.** Las velas sin cuerpo no cortan el tramo, y da
  igual cuántas sean. El máximo de la verde es punto de breaker si el precio viene de un flujo
  bajista y después rompe, cerrando por debajo. Lo que hoy no ve el bot (`VISOR-CONSTRUCCION.md`
  §3.2, pregunta A) él sí lo ve, con esa condición.
- **Regla general:** sí. **«creo»:** sí, solo sobre el esquema («[37:43] no, no creo yo»).
  **Compra y venta:** sí (39:59).

#### S-9 · Qué liquidez eliges cuando hay varias

- **Vídeo y tramo:** v15, 41:19–46:44 (con el tramo ajeno 41:22–41:36, que no se cita).
- **Lo que dice:** «[44:19] claro como se ha planteado y es una regla que siempre pues tratamos de
  dar mayor importancia [44:27] en cierta parte al desarrollo de liquidez en M15 más reciente» /
  «[44:32] entonces en este caso pues sería este de aquí» … «[44:48] pero por lo general se toma» /
  «[44:51] se da prioridad pues a la liquidez más reciente»; para precisar, «[45:41] … ya no nos
  importa mucho con que tome el más reciente …» y «[46:07] … no tiene nada que ver porque el mapeo
  de los bajos de m15 en este caso sea para la liquidez [46:16] de compra …» / «[46:27] en M15, no
  usamos otra» / «[46:28] temporalidad ni de una ni de cuatro» / «[46:31] horas».
- **Propuesta: RESUELVE: (a), la más reciente**, aunque él lo llame «otra cuál» (45:15) porque
  explica antes que otros bajos «también se validan». Basta con que tome la más reciente, y no mira
  ni H1 ni H4. Casa con A-24 DECIDIDA (ADR-0045).
- **Regla general:** sí («es una regla»). **«creo»:** no. **Compra y venta:** solo la compra.

#### S-10 · La misma liquidez tomada dos veces, antes y después de las 7 · A-43 (segunda parte)

- **Vídeo y tramo:** v15, 46:48–51:41.
- **Lo que dice:** «[50:00] Entonces es así, o sea, en el ejemplo está mal planteado, o sea, la
  respuesta sería C, otra cual, con los descritos pues anteriormente con los ejemplos que hemos
  brindado.»; «[48:35] Después de la 7, que esto de aquí para adelante sería nuestro horario de
  operativa,» / «[48:40] en este caso el precio te genera esto, o sea, completamente validado» /
  «[48:46] para una nueva zona de liquidez lineal en M15.» … «[48:56] Entonces esto ya quedaría
  invalidado.»; para precisar, «[51:07] como digo, es indiferente» … «[51:15] se toma, o sea, se toma
  pero luego» / «[51:18] claro, se va actualizando conforme hemos» / «[51:20] visto en los ejemplos»;
  y la confirmación: «[51:26] para confirmar al final» / «[51:28] si una liquidez se toma antes de las
  7» / «[51:29] y otra después, mi toma es» / «[51:31] la más reciente».
- **Propuesta: RESUELVE EN PARTE.**
  - Contesta «otra» y corrige el esquema (la línea está mal trazada).
  - La regla que da es la de siempre: la liquidez se actualiza y vale la más reciente. Con eso, la
    toma de las 7:20 sería la que vale.
  - Pero no dice con esas palabras si la MISMA liquidez, tomada dos veces, vale la segunda vez.
- **Regla general:** sí (la más reciente). **«creo»:** no. **Compra y venta:** solo la compra.

#### S-11 · Una toma de la sesión de la mañana con el sesgo contrario

- **Vídeo y tramo:** v15, 51:46–58:48.
- **La respuesta:** «[58:30] Para confirmar al final, ¿una toma de la sesión de la mañana con el
  sesgo de la tarde a su favor vale para la tarde?» / «[58:39] Si hay una continuidad de sesgo, sí.»
  / «[58:41] Pero si no, no.» / «[58:43] Esa es la respuesta que daría.»
- **Además:** «[57:13] … el [57:21] trazo se va a variar el trazo dependiendo el vallas que nos dé la
  vela [57:27] de cuatro horas anterior …» y, al revés, «[58:11] … obviamente se va a ver al revés no
  se va a seguir los mismos [58:18] criterios o sea se va a seguir trazando una zona lineal de m15
  conforme al sesgo anterior que ya [58:26] Ya, o sea, se nos ha cambiado para la siguiente sesión.»
- **Propuesta: RESUELVE: (b).** En el caso de la pregunta el sesgo cambia a las 11, no hay
  continuidad y la toma de la mañana no vale. Es lo que hace hoy el bot (ADR-0066). **A-46 no se
  reabre**: la respuesta no es la (a).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí (58:11).
- De paso, pide a Aleks que en los esquemas no alargue la línea de M15 más allá del cuerpo de la vela
  (53:19–53:40).

#### S-12a · De qué lado del nivel tomado va tu caja (RN-005)

(Hoja: el texto del recuadro del 2026-10-21.)
- **Vídeo y tramo:** v15, 58:50–65:53 (con el tramo personal 59:09–1:00:03, que no se cita).
- **La respuesta:** «[61:04] sabido eso qué pasa si la caja queda en una compra después que el
  precio tomable que tu [61:13] caja tiene que quedar por encima o por debajo claro en una compra
  sería bien pues queda por [61:20] debajo ahora lo muestro en el ejemplo …» (la línea mezcla la
  pregunta leída y la respuesta); y «[61:25] … si está por encima es lo más [61:36] probable es
  busquemos operativas pues de alcista a bajista estamos buscando operativas bajistas [61:44] a por
  debajo es que estamos buscando operativas alcistas …»; sobre su replay, «[64:42] … tiene similitud
  con el esquema planteado como es que me ha inventado vale o pues [64:51] va a estar por debajo
  pero no puede estar por encima de 15 …».
- **Antes**, a la frase de RN-005 leída: «[60:31] Claro, eso es, pero eso creo que va referido más
  que nada a lo de planteamiento de desarrollo de liquidez en M15».
- **Propuesta: RESUELVE: (b), por debajo.** En una compra, la caja queda por debajo del nivel
  tomado. **Coincide con RN-005** (`ev-v1-001306-f98e12e9`, lo que hace hoy el bot) y **contradice
  `ev-v9-004919-c6bfb3ee`** («tiene que ser todo por encima»). RN-005 no se reabre con esta
  respuesta; la contradicción con ev-v9-004919 la decide el consultor.
- **Regla general:** sí. **«creo»:** sí, solo en la frase de 60:31. **Compra y venta:** sí («en
  venta, claro, sería a revés», 65:33).

#### S-12b · Si la caja queda a caballo del nivel · A-50

- **Vídeo y tramo:** v15, 64:51–65:53.
- **Lo que dice:** «[64:51] … ahora y si el 0 queda justo en la [65:00] la línea ni por encima ni por
  debajo eso es indiferente aquí no está por [65:06] debajo pero es indiferente o sea el cero en este
  caso está por encima pero lo [65:12] importante es eso o sea validar correctamente nuestro posible
  breaker [65:16] porque desde una vez validado de nuestro posible breaker la regla pues o sea nos
  [65:21] dice que ya podemos ir trazando pues desde allí nuestro nuestra caja en venta [65:28] lo
  mismo a revés, ah vale».
- **Propuesta: RESUELVE EN PARTE, y contra lo que hace hoy el bot.**
  - El 0 justo en la línea es «indiferente».
  - En su ejemplo real el 0 queda POR ENCIMA del nivel (del lado de ruido en una compra) y la caja
    vale: «lo importante es validar correctamente nuestro posible breaker».
  - Hoy el bot mira solo el 0 y no opera una caja con el 0 del lado de ruido
    (`se_desarrolla_en_el_lado_de_ruido`).
  - No contesta con sus palabras la pregunta de la caja a caballo, «una parte de tu lado y otra del
    otro»: se deduce de su ejemplo.
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** sí (65:21).

#### S-13 · Hasta cuándo mueves una orden sin llenar, y cuándo la quitas · A-53

(En la filtrada, bajo `## S-3`: el ASR oyó «Pregunta S3», 66:09.) **La hoja llevaba el recuadro del
2026-10-21** («Si el 1 de la caja baja mucho»), **pero en voz se leyó el texto sin corregir**:
«[68:44] … ahora si el 1 de la caja sube mucho lo sigues moviendo». Se dice para quien la active.
- **Vídeo y tramo:** v15, 65:54–69:10.
- **Lo que dice:** «[66:50] siempre nuestras órdenes» / «[66:52] se van a ir actualizando» /
  «[66:53] conforme se vaya actualizando» / «[66:56] pues nuestro punto» / «[66:58] breaker, nunca va
  a ir una orden …» y «[67:18] reglas entonces en este caso pues el precio que hace con la orden pues
  la orden se va a [67:28] ir actualizando …»; del tiempo máximo, «[68:18] es indiferente el tiempo,
  o sea» … «[68:26] claro, o sea, justamente aquí» / «[68:28] en m1 o sea podemos ir actualizando
  puede pasar 10 15 20 minutos pero si no se nos desarrolla [68:36] otro otro punto de otro punto
  breaker entonces es eso no se va a ir actualizando conforme se [68:44] vaya desarrollando el orden
  flow pues en m1 …»; y la confirmación, «[68:50] … para confirmar al final con la orden sin
  llenarse el precio toma [68:56] otra liquidez la orden con la orden se actualiza la orden actualiza
  la orden pero la orden se [69:03] actualiza en m1 conforme se va desarrollando pues un nuevo punto
  breaker».
- **Propuesta: RESUELVE EN PARTE, hacia la (b)** (`orden_pendiente_al_abrir_escenario = se_mueve`,
  lo de hoy).
  - La orden no se quita: se actualiza al punto nuevo de M1, sin tiempo máximo.
  - La letra se oye mal («sería la respuesta la sé», 67:41).
  - **No dice si una orden que se llena antes de aparecer el punto nuevo vale.**
  - La subpregunta del 1 que «baja mucho» no se hizo con ese texto (arriba).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** no lo dice.

#### S-14 · Qué te hace no operar un día o una sesión

(En la filtrada, bajo `## S-3`. Dentro van dos tramos de precaución, 74:41–76:52 y 77:52–78:06,
que no se citan.)
- **Vídeo y tramo:** v15, 69:10–80:27.
- **Lo que dice:**
  - «[70:23] Vale, puede haber que no hubo toma de liquidez de M15.» y «[71:27] este tipo de
    escenarios cuando hay un order flow demasiado fuerte en M15, o sea, donde no [71:34] llegamos a
    ver ningún rompimiento o toma de liquidez en M15, …»; en su esquema, «[73:21] entonces en estos
    días [73:23] pues no nos opera simplemente porque no hay operación no se llega a ver …»;
  - «[73:50] La respuesta sería» / «[73:54] E» / «[73:55] Con la explicación»;
  - del break even en sus backtests: «[69:21] a lo mejor» … «[69:28] me he saltado» / «[69:30] en
    lugar de poner break even no he operado» / «[69:32] puede que en ese día solo ha habido» /
    «[69:34] break even y no se ve reflejado» / «[69:36] en el backtest»;
  - de dejar de operar tras ganar o perder: «[77:22] la respuesta es» … «[77:28] no, seguimos
    operando» / «[77:30] todas las operaciones que encontremos» / «[77:32] tanto en la primera como
    segunda sesión» / «[77:34] pero, pero» / «[77:36] aquí viene el pero, esto ya es algo que» /
    «[77:38] a lo mejor pues más adelante» / «[77:40] pueda variar», y «[79:04] Pero, en este caso,
    la respuesta sería» / «[79:08] no dejamos de operar.»;
  - de saltarse sesiones: «[79:12] … En los backtest te saltabas [79:18] en una sesión entera a
    propósito. Solo me he saltado a lo mejor para cuando en una sesión [79:26] había break events, me
    lo he saltado. Cuando en una sesión no lo he contabilizado porque sé que [79:33] es break event,
    entonces para evitar todo eso, poner la orden y demás, quitarme tiempo, pues me [79:38] de
    saltado pero en los últimos partes que se ha enviado con vídeo y todo pues no se está tal cual»;
  - y la confirmación: «[79:56] … si un día no opero normalmente es porque, bueno, como vamos a
    operar en este caso, uno cuenta con noticias, pues no habría excusas, o sea, si un día no se
    opera es porque estaba enfermo, estaba enfermo.»
- **Propuesta: RESUELVE EN PARTE.** Las causas que da son tres:
  - no hubo toma de liquidez de M15, o un flujo de M15 tan fuerte que no rompe en M1 (es la (a));
  - **en sus backtests anteriores se saltaba las sesiones que sabía que iban a acabar en break
    even**, y no en los últimos, los grabados en vídeo;
  - un día sin operar «es porque estaba enfermo».

  Esto pesa en la deuda «el no_trade por ausencia no está decidido» (P6 de
  `CORRIDA-CONSTRUCCION.md` §4.5) y en cualquier medida de fidelidad sobre backtests antiguos. No
  deja de operar tras ganar o perder, «por ahora».
  Pide además los días en que el bot opera y él no (69:57).
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** no aplica.

#### S-15 · Entrar en la segunda zona después de la toma

- **Vídeo y tramo:** v15, 80:29–86:41. **Dentro cae el corte SIN AUDIO 1:22:26–1:23:33**: el trader
  dice antes «[82:10] Perdón, voy al baño.» y la respuesta empieza al volver (84:00). No se puede
  saber si se dijo algo en el corte; la respuesta no parece afectada.
- **La respuesta:** «[84:59] Bueno, la C, la respuesta C con lo explicado anteriormente, o sea, se va
  actualizando pues conforme se vaya dando las condiciones …»; antes, «[84:00] Cuando validemos este
  punto, que sería el tercer punto breaker,» / «[84:05] esté validado correctamente entonces esta
  orden de aquí se actualiza aquí no se deja aquí o se [84:12] va poniendo órdenes no es que se va
  actualizando para no tener varias órdenes …»; para precisar, «[85:27] … si el primer retroceso no
  estaba limpio el segundo cuenta como el primero o sea no usaría [85:35] no lo plantearía de esa
  manera la pregunta sería trabajaría más que nada en base actualización [85:41] nos actualizaría del
  primero al segundo retroceso si es que cumple pues con las condiciones …» y «[85:51] … cuántas zonas
  espero con mucho no está definido o sea las zonas que [85:59] espero o sea no no está definido
  porque se puede seguir desarrollando o sea indefinidamente hasta [86:04] que se llegue a dar …»; y
  la confirmación, «[86:16] Entro en la zona, no número» / «[86:18] Sino entro en la zona en la que
  el precio llega a activar» … «[86:36] O sea, siempre al más reciente trabajamos».
- **Propuesta: RESUELVE, y contra lo que hace hoy el bot.**
  - Entra en la zona más reciente que valide el punto, sin límite de zonas tras la toma: la orden se
    actualiza de la primera a la segunda.
  - Hoy el bot no entra porque cuenta dos zonas de control desde la toma (RN-009,
    `zonas_control_max_por_esquema = 1`): es justo el caso de los dos días de
    `VISOR-CONSTRUCCION.md` §3.2.
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** no lo dice (su ejemplo es una venta).

#### S-16 · El precio ya está más allá del 0 cuando se forma la caja

- **Vídeo y tramo:** v15, 86:45–92:54.
- **Lo que dice:** «[89:45] el ejemplo no concuerda con lo que nos pregunta»; con una venta propia:
  «[90:24] es un esquema sería así una vez validado el punto breaker ya tienes validado también pues
  [90:32] un punto cero o sea donde en este caso estamos buscando entradas bajistas y tu orden pues
  ya [90:40] está activada allí tu orden en este caso stop creo que es con la que estamos trabajando
  …»; «[91:04] … ahora la respuesta sería de otra cual con lo descrito anteriormente»; «[91:58]
  entonces cambia algo si estás en un punto por encima o 10 pues no no cambia nada …»; y la
  confirmación, «[92:20] esa pregunta» / «[92:21] no está bien planteada, como digo» … «[92:30] no» /
  «[92:31] no podría responder a esa pregunta porque» / «[92:33] no coincide con lo de esto …».
- **Propuesta: NO RESUELVE.** Dice que el esquema no casa con la pregunta y que no puede
  responderla. Lo único firme: validado el punto, la orden (stop) va en el 0. Lo que pasa si el
  precio ya está más allá del 0 no lo dice. Pide que los esquemas lleven escrito el marco temporal
  (87:16–87:35 y 92:44–92:49).
- **Regla general:** no. **«creo»:** sí (90:40, sobre el tipo de orden). **Compra y venta:** —.

#### S-17 · Cuándo pasas el stop a la entrada · A-13

**Entera en v15** (respuesta b de Aleks), bajo `## S-16` en la filtrada (su código, «uno más,
S17», 93:03, no se detectó). **Su código se buscó también en la filtrada de v16: §3.4.**
- **Vídeo y tramo:** v15, 93:03–98:07.
- **Lo que dice:**
  - «[93:47] vale, la respuesta» / «[93:48] es la B, aunque cierre con la» / «[93:50] la B, a ver» /
    «[93:51] A ver, no, no voy a, a ver, voy a responder esa pregunta, pero lo ideal sería en estos
    casos, …, que el ejemplo se nos brinde con gráfico de velas, ¿vale?»;
  - sobre su replay en M1: «[95:00] nosotros la zona de control sería esta de aquí» … «[95:04] el
    precio llega, nos rompe» / «[95:06] una vez, cierre por debajo de aquí» / «[95:09] o sea» /
    «[95:10] esté por debajo, nosotros la podemos poner en break even» … «[95:16] tiene que cerrar
    por debajo» / «[95:18] o sea, con mecho o con cuerpo»;
  - después, en 5 segundos: «[96:05] event en 5 segundos el precio llega y toca ya se pone en break
    event que cuando nos vamos m1 ya [96:15] aquí estaría la condicional para nosotros poner en
    break event o sea inmediatamente apenas toque [96:20] que se pone en break y en la entrada y ya
    apenas toque …»;
  - la zona de una sola vela: «[97:00] … pues no cambia nada o sea la misma regla es lo mismo en
    compra y en venta así»;
  - y la confirmación: «[97:48] está una vez validado pues según la usa según el criterio que tenemos
    apenas el precio rompe [97:55] aquí está nuestra entrada estuve retrocede apenas todo aquí se pone
    en break y ven la entrada ya».
- **Propuesta: RESUELVE EN PARTE: se contradice dentro de la misma respuesta.**
  - Empieza por la (b) y la explica en M1 («tiene que cerrar por debajo … con mecha o con cuerpo»).
  - Al pasar a 5 segundos dice «apenas toque», y con eso cierra la confirmación.
  - Lo último que dice es la (a), que es lo de hoy (`break_even_condicion = tocar`, CONFIRMED;
    ADR-0065).
  - Lo primero que dijo, la (b), contradice ese CONFIRMED. Decide el consultor.
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** sí (97:00).

#### S-18 · Una línea de M1 que, rota con la mecha, te quite la entrada · A-32 — la de v15, INCOMPLETA

- **Vídeo y tramo:** v15, 98:07–100:37. Se lee «lo que nos has dicho» y la pregunta («[98:40] … lo
  que todavía no sabemos [98:42] si existe alguna línea en M1 …»), el trader empieza a explicarlo
  sobre su replay (99:02–100:27) y la grabación se corta. **Por la respuesta b de Aleks, la que vale
  es la de v16** (§3.4); esta se informa como incompleta y no se propone nada con ella.

### 3.4 v16: S-18 a S-25

**Cómo se agrupó la filtrada de v16.** S-20 se abrió en voz a las 09:24 («pasamos a pregunta S20»)
y el guion no lo detectó ahí: lo detectó al cerrarla (18:52, «Pregunta S20 cerrada»), así que su
contenido va bajo `## S-19` y el bloque `## S-20` solo trae esa línea. S-24 se abrió en la misma
línea en que se cerró S-23 (26:48), y va bajo `## S-23`; el registro la da como «sin código
detectado». La localización se hizo a mano por los códigos dichos en voz. **Ningún código salió
como «veinte y N»** (encargo, «La hoja que se llevó», punto 2): la palabra «veinte» no sale ni una
vez en ninguna de las dos filtradas, y el bloque `## S-20` de v16 es solo la línea de cierre (v15 no
tiene bloque `## S-20`). **El código de S-17 no está en v16**: ni «17» como código ni «diecisiete»
(las dos veces que sale «17» son «del 1 al 17», en S-25); S-17 está entera en v15, como dijo Aleks.

#### S-18 · Una línea de M1 que, rota con la mecha, te quite la entrada · A-32 — la de v16, la que vale

- **Vídeo y tramo:** v16, 00:10–06:21 (cierra «S18 cerrada», 06:33). La de v15 (§3.3), incompleta.
- **La respuesta:** «[02:34] F18, la respuesta es» / «[02:36] no, en M1 la mecha siempre vale» /
  «[02:38] pero, claro» / «[02:40] teniendo en cuenta el contexto también» / «[02:42] en el que se
  desarrolla, porque si es con una zona lineal» / «[02:44] de M15» … «[02:50] Pues, en este caso es
  de alcista a bajista y de bajista a alcista, pues, dentro de esta zona de aquí, el rompimiento,
  para habilitar la zona lineal de M15, tiene que ser con cuerpo.» / «[03:03] Pero, si no, ya
  posterior a ello, se puede ser con mecha.» / «[03:07] Entonces, la respuesta es la A.»
- **Antes, sobre su replay:** «[01:15] puede validar, no es como en M15» … «[01:34] nos tiene que
  romper con cuerpo» / «[01:35] pero después pasando eso» … «[01:46] es válido, o sea, el
  rompimiento» / «[01:48] con mecha posterior».
- **Para precisar, otras líneas en M1:** «[04:08] … se suele ir dibujando o sea mientras uno va
  [04:14] desarrollando estructura en m1 pues se va teniendo en cuenta el posible punto breaker
  [04:20] que luego lo valida si cumple con las reglas …»: lo que dibuja son posibles puntos de
  breaker; no nombra otra línea.
- **Para precisar, la línea que viene de M15:** «[06:03] ahora si es una línea que viene» / «[06:05]
  de M15 la cuentas como M15» / «[06:06] aunque la mires en M1» / «[06:11] claro, o sea, claro, la
  cuento como» / «[06:14] de M15 aunque la mire de M1 …».
- **Propuesta: RESUELVE: (a).** En M1 la mecha siempre vale. La única ruptura que pide cuerpo es la
  de la zona lineal de liquidez de M15 («para habilitar la zona lineal de M15, tiene que ser con
  cuerpo»), y una línea que viene de M15 cuenta como de M15 aunque se mire en M1. Casa con lo que ya
  dijo en la sesión 4 (`ev-v10-020142-30fd2569`). La confirmación final de la hoja no se oye leída.
- **Regla general:** sí. **«creo»:** solo sobre si ya la había respondido («[00:33] … creo que sí
  llegué a responder esa pregunta»). **Compra y venta:** sí («de alcista a bajista y de bajista a
  alcista», 02:50).

#### S-19 · Una vela sin cuerpo en medio del retroceso

- **Vídeo y tramo:** v16, 06:33–09:19.
- **La respuesta:** «[08:27] … y se encuentra como alternar sin [08:35] válida no cuenta sigue como
  si no estuvieran en la respuesta es la vez no cuenta sigue como [08:39] estuviera o sea se
  mantiene el análisis …» (la línea mezcla la opción leída y la respuesta; «la vez» es la «b» del
  ASR).
- **Para precisar:** «[08:51] casi no tiene un cuerpo, uno o dos puntos» / «[08:53] igual, o sea, no
  pasa nada» / «[08:55] simplemente no se toma en cuenta» / «[08:57] o sea, y si son dos velas» /
  «[08:59] sin cuerpos seguidas, tampoco, o sea» / «[09:01] no afecta» / «[09:03] no afecta, sigo
  manteniendo» / «[09:04] la estructura …»; y «[09:06] esta es la vela, o sea, neutral» / «[09:09]
  entonces trazaríamos pues» / «[09:10] el punto breaker en esa zona» … «[09:15] pues la parte más
  alta, y si es al revés, en la parte» / «[09:17] baja».
- **Propuesta: RESUELVE: (b).** La vela sin cuerpo no cuenta como alternancia, tampoco una de uno o
  dos puntos ni dos seguidas. Es lo que pregunta ADR-0076 §4 (pregunta 1). **Ojo con S-24:** aquí una
  vela de uno o dos puntos «no se toma en cuenta» en el retroceso; en S-24, una de uno o dos puntos
  vale para trazar un punto de breaker. Son dos usos distintos (la alternancia del retroceso y el
  trazo del punto), pero el umbral no es el mismo: lo mira el consultor (§4).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí (09:15).

#### S-20 · El punto de breaker roto solo con la mecha de una vela contraria

- **Vídeo y tramo:** v16, 09:24–18:46 (en la filtrada, bajo `## S-19`).
- **Lo que dice:** del esquema, «[14:40] algo que me acabo de dar cuenta es que» / «[14:42] el ejemplo
  está mal planteado» / «[14:44] en cierta parte» / «[14:45] esta zona breaker como digo se tiene
  que ir actualizando no se puede poner aquí o sea [14:52] siempre el punto breaker al más reciente y
  el más reciente y que cumple con las condiciones …»; la letra, «[17:07] Entonces, vale, la
  respuesta sería la C.» / «[17:12] ¿Cuál? O sea, es C otra cual con la explicación que hemos
  brindado anteriormente.»; del color, «[18:31] ¿Qué color es la vela que rompe?» / «[18:34] no, esto
  es una muy buena pregunta» / «[18:36] no importa el color de» / «[18:37] la vela que rompe, puede
  ser una vela verde» … «[18:44] o sea ha roto esto» / «[18:45] el punto breaker» / «[18:46]
  entonces se valida».
- **Para precisar, sin alternancia antes:** «[17:50] Es lo más probable que a veces no nos llegue a
  activar la entrada», y se corrige: «[18:11] … no no perdón si la activaría la activaría y
  activaría [18:17] esta orden de aquí pero nos sacaría en pérdida también …».
- **Propuesta: RESUELVE EN PARTE.**
  - Contesta «otra» y corrige el esquema: el punto de breaker se actualiza al más reciente que
    cumpla las condiciones, y en el esquema estaría mal puesto.
  - La mecha de una vela contraria rompe el punto: «no importa el color de la vela que rompe … se
    valida».
  - Lo que pregunta ADR-0076 §4 (pregunta 2: qué pesa más, la mecha o la alternancia de antes) no lo
    contesta con esas palabras; lo lleva al punto que se actualiza.
  - Enseña sobre su replay una operación suya que acaba en pérdida (16:08–17:00), sin cifras.
- **Regla general:** en parte. **«creo»:** no («si no me equivoco», 11:32, sobre el tipo de orden).
  **Compra y venta:** no lo distingue (sí que el color no importa).

#### S-21 · La racha después de la novena pérdida

- **Vídeo y tramo:** v16, 18:53–21:35. **Dentro va el tramo de precaución 20:02–21:16** (§2.6), que
  no se cita: ahí cae también la segunda de «Para precisar» (si le ha pasado en sus backtests).
- **Lo que dice:** «[19:21] o sea después de parar por nueve pérdidas seguidas en un día que nuestro
  tope pues esperamos al día [19:28] siguiente y nuevamente pues nos ponemos a operar …»; de la
  pérdida de más, «[19:52] también al día siguiente no solemos hacer una operación más después de
  [19:57] nueve pérdidas consecutivas en pérdida ojo que no se cuentan los break even» (la línea
  mezcla la subpregunta leída y la respuesta); y la confirmación, «[21:26] Al día siguiente de parar
  por nueve pérdidas, la racha empieza en...» / «[21:31] Pues al día siguiente» / «[21:32]
  Nuevamente en cero, o sea, se sigue continuando».
- **Propuesta: RESUELVE: (a), empieza de cero.** Va **contra lo que hace hoy el bot**: ADR-0077 §5
  (lectura PROVISIONAL) hace (b). Repite que los break even no cuentan para las 9
  (`fb-2026-10-04-sesion-04-8e2d728a`).
- **Regla general:** sí. **«creo»:** no, fuera del tramo. **Compra y venta:** no aplica.

#### S-22 · El último minuto: a qué hora quitas la orden sin llenar

- **Vídeo y tramo:** v16, 21:37–23:47.
- **La respuesta:** «[22:09] voy a decir que es la C, otra cual» … «[22:48] perfecto, la respuesta es
  aquí, siempre menos» / «[22:50] un minuto, es justamente lo que iba a comentar» / «[22:53] Siempre
  se cierra» / «[22:54] Si está abierta o todavía no se ha llenado la orden» / «[22:57] Un minuto
  antes» … «[23:13] Entonces se quita un minuto antes».
- **Para precisar:** «[23:23] Pues lo cierro enseguida» / «[23:25] Lo cierro enseguida, nunca se
  deja»; «[23:32] Y la respuesta es no» / «[23:34] No se pone ninguna orden» / «[23:36] En el último
  minuto antes de las 11 o de las 3».
- **Propuesta: RESUELVE: un minuto antes**, para la orden sin llenar igual que para la operación
  abierta. Lo dice como «otra», pero es la (b). Si la orden se llena en ese último minuto, la cierra
  enseguida, y en el último minuto no pone órdenes. Para la ORDEN, «un minuto antes» lo dice ahora
  el trader (en la sesión 4 lo había dicho el consultor; `PREGUNTAS.md`, «Para Aleks» de S-22).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** no aplica.

#### S-23 · La vela de 4 horas sin color, con el sesgo bajista

- **Vídeo y tramo:** v16, 23:49–26:46.
- **La respuesta:** «[24:22] se mantiene bajista exactamente …» y la confirmación, «[26:41] la
  respuesta es» / «[26:42] con el sesgo bajista una vela neutra de 4 horas» / «[26:44] deja el sesgo
  bajista todavía».
- **Para precisar, dos neutras:** «[25:21] llegamos a trazar otra vela neutra que también ha hecho lo
  mismo nuestro sesgo todavía se sigue [25:27] manteniendo bajista entonces tenemos unas dos velas
  neutras pero nuestro sesgo todavía está [25:32] aquí hasta que posteriormente pues se llegue a
  haber un rompimiento con cuerpo …».
- **Para precisar, el lunes:** «[25:51] Esto va a depender» … «[25:57] Que sigas arrastrando» …
  «[26:02] Podemos ir arrastrando todo un sesgo» / «[26:05] Y que nos dure 5 días»: el lunes sigue
  el sesgo que se arrastra.
- **Propuesta: RESUELVE: (a).** Con el sesgo bajista, la vela neutra lo mantiene, también con dos
  seguidas, hasta una ruptura con cuerpo. Es lo de hoy (ADR-0075) y completa el caso alcista de la
  sesión 4 (`ev-v10-014005-7e2228f4`). La reserva de `fb-2026-10-04-sesion-04-ca0afae6` queda
  contestada en voz.
- **Regla general:** sí. **«creo»:** solo en un ejemplo («[26:00] Que creo que justamente es en
  julio»). **Compra y venta:** sí, con la sesión 4.

#### S-24 · La vela casi plana: de cuántos puntos · RN-007 (H)

- **Vídeo y tramo:** v16, 26:48–28:55 (en la filtrada, bajo `## S-23`).
- **La respuesta:** «[27:46] … tres velas de M1, vale, dice, ¿cuál de estas es casi plana? Si no lo
  sabe, trazar un punto breaker, solo la 1, las 3 de las 12, las 3 son válidas para trazar un punto
  breaker, entonces la respuesta sería D, otra cual, pues las 3, o sea, que se muestran visualmente,
  sea un punto, dos puntos o 12 puntos,» / «[28:15] sirve para nosotros poder trazar …».
- **Antes:** «[27:17] Esto creo yo, o sea, a ver, no creo yo, o sea, esto por lo general, como digo,
  va a ser dependiendo del broker» y «[27:35] ¿Cómo nos ha cerrado la vela? Pues visualmente, y de
  qué color, si nos ha cerrado alcista o bajista».
- **Para precisar:** «[28:15] … para precisar mira solo el cuerpo también las mechas se mira [28:21]
  los dos tanto las mechas como el cuerpo es lo mismo en m15 en m15 ya hemos hemos dicho que [28:28]
  tiene pues ahí es un poco diferente …» (en M15 el punto pide romper con cuerpo).
- **La confirmación:** «[28:41] … para confirmar al final una vela de casi planas y su cuerpo es de
  bueno [28:48] tiene que ser cero puntos tiene que ser cero puntos o sea no casi o sea si no tiene
  que ser [28:55] plana totalmente porque estas velas pues pueden servir también como trazo a punto
  breaker perfecto».
- **Propuesta: RESUELVE: (d), el umbral es cero.** Solo la vela plana del todo (cero puntos de
  cuerpo) cuenta como si no existiera; las de 1, 2 y 12 puntos valen para trazar un punto de
  breaker. Mira cuerpo y mechas. **Contradice lo que dijo en la sesión 4** («casi plana con 1 o 2
  puntos», `ev-v10-014310-2296423b`) y está en tensión con S-19 (arriba). El minuto 1:44:49 de v10
  ya no hace falta (respuesta c de Aleks): qué pasa con H, en §4.2.
- **Regla general:** sí. **«creo»:** lo dice y se corrige al momento («no creo yo», 27:17).
  **Compra y venta:** no aplica.

#### S-25 · El Excel de julio y los tres primeros vídeos

- **Vídeo y tramo:** v16, 29:02–32:10. **Dentro va el tramo de precaución 30:41–31:37** (§2.6 y
  §2.7), que no se cita ni se describe más.
- **Antes de contestar:** «[29:20] es una buena pregunta bro porque no sé si está en orden» /
  «[29:22] yo creo que sí o sea» … «[29:32] o sea creo que si está en orden».
- **La respuesta a la pregunta:** «[30:10] Entonces, creo que sí estaba en orden, porque justamente
  él como que miraba las partes del inicio del video, y el último video era el que no procesó.» /
  «[30:20] O sea, el último video era el que traía este tramo final, entonces, yo creería que sí,
  igual lo puede corroborar el propio bot, creería yo.» El hablante se atribuye por contexto.
- **Después del tramo de precaución:** «[31:42] ¿cuál sería la respuesta del cuarto?» / «[31:43] a
  ver» / «[31:45] voy a decirle que sí, entonces, sí, sí». Ese «sí» contesta a «la respuesta del
  cuarto» y no nombra el Excel. *(Corregido tras el revisor, hallazgo a2: la primera redacción daba
  este «sí» como la respuesta a la pregunta y no citaba 30:10–30:20.)*
- **Para precisar:** «[31:49] el cuarto video» / «[31:51] el del final del mes no tiene Excel,
  exacto»; y «[31:54] hiciste todos los días de julio» / «[31:56] te saltaste alguno» / «[31:57] todo
  está tal cual» / «[31:59] todo está grabado está todo está grabado todas las entradas pérdidas
  ganancias todos los break [32:04] events …».
- **Propuesta: RESUELVE EN PARTE, hacia la (a).** Cree que el Excel está en orden («creo»,
  «creería», «no sé si está en orden») y dice que lo puede corroborar el bot. No dice con sus
  palabras que sea la exportación de los tres primeros vídeos. Después dice que hizo todo julio sin
  saltarse nada, y se lee que el cuarto vídeo no tiene Excel. La rama de T (transcribir v11 a v14)
  lo medirá además (`PREGUNTAS.md`, «Para Aleks» de S-25).
- **Regla general:** no aplica. **«creo»:** sí (29:22, 29:32, 30:10, 30:20). **Compra y venta:** no
  aplica.

### 3.5 «Para cerrar» (v16, sin código de voz)

- **Vídeo y tramo:** v16, 32:10–34:41. Dentro, los dos bloques en cuarentena (32:58–33:07 y
  33:11–33:22), que no se leen.
- **Diciembre (NA:I).** Leída la petición de la hoja (32:10), «[32:28] Que nos
  mandaste, lo grabaste con tu video» / «[32:30] Vos, como los otros meses» / «[32:33] Ah, todavía no
  envió a diciembre» / «[32:36] Ah, cierto, ¿no?» / «[32:38] Sí, todavía está pendiente diciembre» /
  «[32:40] Ya, pero cuando se necesite» / «[32:42] Lo grabas con video y vos, pues» / «[32:44] Sí,
  sí, sí, lo grabo tal cual». **Lo que dijo:** que diciembre está pendiente y que, cuando se
  necesite, lo graba en vídeo con su voz «tal cual». Las voces no se separan y el diálogo no deja
  claro si lo pendiente es el envío del backtest o su vídeo; NA:I dice que el backtest llegó el
  2026-10-09 sin vídeo. No se decide nada.
- **Agosto (NA:Q).** «[32:49] Agosto» / «[32:51] ¿Nos puedes mandar la exportación de bactrias»
  / «[32:52] De agosto, al que grabaste el video y das por bueno?» / «[32:55] Sí, lo tiene, creo que
  sí está, bro». **Lo que dijo, citado:** que cree que ya está («lo tiene»), con «creo».
  **Lo que queda sin cita.** La línea siguiente, la de 32:56, toca el tramo de cuarentena que
  empieza en 0:32:58: su segmento llega a 0:32:58.116, y `evidence new` la rechaza (respuesta del
  consultor del 2026-10-25, punto 4: es correcto no citarla). **Sin citarla, lo que se entiende:**
  se repite, ya sin «creo», que lo de agosto está, es decir, que la exportación existe. La
  transcripción no separa voces y la línea se atribuye al trader solo por contexto (hallazgo a8 del
  revisor). No dice si ya la mandó ni cuándo la manda. Lo decide el consultor en la activación; aquí no se
  decide nada.
- **Marzo: la confirmación escrita** (encargo, «Ampliación declarada del 2026-10-25»).
  - **La petición en voz cae en la cuarentena**: los dos bloques (32:58–33:07 y 33:11–33:22) caen
    por el mes (motivos «mes» y «vecino»), así que la petición no se leyó. **El contexto es la
    declaración de Aleks**: «en la llamada le pedí que me lo confirmara por escrito y en ese momento
    me lo envió». Después de los bloques (la línea de 33:22 cae en el segundo de margen del tramo y
    no se cita) se oye «[33:24] Si, mandame un mensaje para que confirme que eres tú» / «[33:27] Y
    lo firma».
  - **El literal**, transcrito por el consultor de la captura (la sesión no la abre, ADR-0038):
    **«Confirmado backtest de marzo»**, mensaje del trader del **2026-10-25 a las 13:58 (hora de
    Lima)**, por WhatsApp. **Es una confirmación ESCRITA**, que es lo que pide `REGISTRO-MARZO.md`
    §2 (paso 0; F09): decirlo en voz no bastaba. El mensaje solo nombra el mes: ninguna fecha y
    ningún resultado. El mensaje siguiente de la captura no se registra ni se interpreta. Registrado
    en `fuentes.yaml` (descripción de «Mensajes del trader») y declarado en `HOLDOUT-EXPOSICIONES.md`
    (2026-10-25).
  - **Una medida, sin decidir nada.** El vídeo v16 tiene `mtime` 2026-10-25 14:01:40 −05:00, la hora
    de su nombre (`stat`); si esa es la hora en que terminó de grabarse, 33:22 de v16 cae hacia las
    14:00:12 del reloj del ordenador, y las 13:58 del mensaje son del reloj del teléfono, unos dos
    minutos antes. Los dos relojes no se han comparado; no cambia el literal ni la confirmación.
    **Esta medida no la pide el encargo** (hallazgo b4 del revisor). Se dejó porque el añadido manda
    dar el «contexto» de la confirmación, y ese contexto es la declaración de Aleks («en ese momento
    me lo envió»). La medida no la contradice ni la confirma, y si el consultor la ve de más, se
    quita.
- **El final de v16** (33:36–34:41): el trader se ofrece para más sesiones, y Aleks explica que el
  error de fidelidad de agosto venía de las operaciones de break even que se saltaba: «[34:21] ok,
  ok, porque claro, el error que hubo de pensar» / «[34:23] que no había fidelidad en agosto era
  necesariamente porque no es que tengas una operativa distinta» / «[34:29] sino porque habías
  evitado ciertas operaciones que eran de breakeven correcto exacto exacto es …». El «correcto
  exacto exacto» es del trader, por contexto. Va con S-14 (§3.3).

## 4. Contradicciones, cobertura de V y cosas que el consultor tiene que mirar

### 4.1 Contradicciones y cosas que mirar

1. **S-1 contra la sesión 1.** Va con la regla del color activa (ADR-0080) y con el WhatsApp del
   2026-10-14, y contra v6 1:04:30–1:05:35 (`SESGO-H4-COLOR.md` §1.c; ADR-0080 §9).
2. **S-3, la mecha que pasa el alto y vuelve:** «se actualiza el de la mecha», frente a «lo tiene
   que pasar con cuerpo, no con mecha» de la sesión 4 (`ev-v10-012456-9dc1d221`). Hablan de cosas
   distintas (qué alto se usa y cuándo queda tomado), pero hay que mirarlo.
3. **S-4:** no tiene tope de semana y llama «error» al 9 % de la sesión 1: contradice
   `perdida_maxima_semanal = 9` (CONFIRMED). La magnitud del tope diario (saldo o equity) no la
   dijo: **es la PARADA de §4 de `ACTIVAR-A35-A44.md`** para A-44.
4. **S-5:** el trader contesta después de que Aleks plantee la disyuntiva.
5. **S-6:** no da número de reentradas y duda de las de niveles iguales; ADR-0083 sigue PROVISIONAL.
6. **S-12a contra `ev-v9-004919-c6bfb3ee`:** la caja de una compra va por debajo del nivel tomado
   (RN-005), no «todo por encima».
7. **S-12b contra el bot:** en su ejemplo el 0 queda del lado de ruido y la caja vale
   (`se_desarrolla_en_el_lado_de_ruido`).
8. **S-13:** en voz se leyó el texto sin el recuadro del 2026-10-21; la subpregunta corregida («si el
   1 de la caja baja mucho») no se hizo.
9. **S-14 y el final de v16:** en sus backtests anteriores se saltaba las sesiones que iban a acabar
   en break even; en los grabados en vídeo, no. Pesa en toda medida de fidelidad sobre backtests
   antiguos (y es la explicación de Aleks del error de agosto, v16 34:21–34:36).
10. **S-15 contra el bot:** entra en la zona más reciente, sin límite de zonas tras la toma; el bot
    cuenta dos zonas de control y no entra (RN-009, `zonas_control_max_por_esquema = 1`).
11. **S-17 se contradice dentro de la respuesta:** empieza por (b), al cierre, y acaba en «apenas
    toque», que es la (a) de hoy (`break_even_condicion = tocar`, CONFIRMED; ADR-0065).
12. **S-19, S-24 y la sesión 4: el umbral de la vela casi plana.** S-24: solo la de cero puntos es
    plana; las de 1, 2 y 12 valen para trazar el punto. S-19: en el retroceso, una de uno o dos
    puntos «no se toma en cuenta» como alternancia. Sesión 4: «casi plana con 1 o 2 puntos»
    (`ev-v10-014310-2296423b`).
13. **S-21 contra el bot:** la racha empieza de cero al día siguiente; ADR-0077 §5 (PROVISIONAL) hace
    (b).
14. **S-25, en parte:** cree que el Excel está en orden («creo», «creería»), sin decir con sus
    palabras que sea la exportación de los tres primeros vídeos. La rama de T lo mide.
15. **Diciembre (NA:I):** el diálogo dice «pendiente»; NA:I dice que el backtest llegó sin vídeo.
16. **La hora del mensaje de marzo** frente al reloj de la grabación (§3.5): unos dos minutos, en
    relojes distintos. No se decide nada.

### 4.2 Qué pasa con H tras S-24

H (`PROJECT_STATE.md`, Next Action) esperaba el umbral de la vela casi plana de RN-007, y desde la
sesión 4 el literal de v10 1:44:49, que Aleks iba a leer en su terminal. **Aleks no lo leyó, y ya no
hace falta** (respuesta c): S-24 se le preguntó al trader en esta sesión y su respuesta lo
sustituye.
- **La respuesta:** el umbral es **cero puntos**: solo la vela plana del todo cuenta como si no
  existiera, y las de 1, 2 y 12 puntos valen para trazar un punto de breaker (v16 27:46–28:55,
  §3.4). Mira cuerpo y mechas.
- **Con esto, H ya no espera a ninguna pregunta ni a ningún literal**: la respuesta está grabada y
  se puede citar fuera de todo tramo. El punto 8 de la respuesta del consultor del 2026-10-11 (que
  Aleks leyera 1:44:49) queda sin objeto.
- **Lo que no se decide aquí** (esta rama no toca la spec): si RN-007 cambia de texto (hoy dice
  «una vela casi plana, sin color claro, cuenta como si no existiera»), si su forma ejecutable
  cambia y si hay rama de código. Lo decide el consultor en V (R4.1), con las dos tensiones del
  punto 12 de §4.1.

### 4.3 Cobertura de V

Lo que V (`PROJECT_STATE.md`, Next Action) pedía a la sesión 5, con el código que lo preguntó:

| Lo que pedía V | De dónde | Código | Cubierta |
|---|---|---|---|
| A-13 (break even al toque o al cierre) | `ACTIVAR-SESION-04.md` §0.e.2 | S-17 | en parte: se contradice dentro de la respuesta |
| A-32 (la línea de M1 rota con mecha) | §0.e.8 | S-18 (v16) | sí: (a), con la zona de M15 aparte |
| A-35 (el alto de M15 formado) | §0.e.4 | S-3 | en parte: la primera mitad sí, en una lectura documentada; la segunda no tiene parámetro |
| A-43, segunda parte | §0.e.5 | S-10 | en parte: la más reciente, sin decir si la misma toma vale dos veces |
| A-44 (el tope de la semana) | §0.e.3 | S-4 | en parte: el alcance sí; la magnitud no (PARADA de §4) |
| A-49 (la caja con la vela abierta o cerrada) | §0.e.1, con CORRIDA §4.5, pregunta 4 | S-7 | en parte: la traza al cierre; no elige opción |
| A-50 (la caja a caballo) | §0.e.6 | S-12b | en parte, y contra el bot |
| A-53 (la orden sin llenar) | §0.e.7, con CORRIDA §4.5, pregunta 6 | S-13 | en parte; la subpregunta del recuadro no se hizo |
| S-14 de la sesión 4, que es H (RN-007) | NA:H | S-24 | sí: el umbral es cero (§4.2) |
| Si el xlsx de julio es la exportación de v11 a v13 | `ENTRADA-JULIO.md` §8 | S-25 | en parte: cree que está en orden; no lo dice con esas palabras |
| A-57 (el lote que no cabe) | `MARGEN-LOTE.md` §5 | S-5 | sí: (a), «por ahora» y con «creo» |
| `VISOR-CONSTRUCCION.md` §3.2, pregunta 8 | CORRIDA §4.5, pregunta 8 | S-15 (el lado, S-12a/S-12b) | sí, y contra el bot |
| `VISOR-CONSTRUCCION.md` §3.2, pregunta 9 | CORRIDA §4.5, pregunta 9 | S-16 | no: dice que el esquema no casa y no la responde |
| `VISOR-CONSTRUCCION.md` §3.2, pregunta 5 | CORRIDA §4.5, pregunta 5 | S-9 | sí en abstracto (la más reciente); el día de ejemplo no se enseñó (ningún día real en la hoja) |
| `VISOR-CONSTRUCCION.md` §3.2, pregunta 3 | CORRIDA §4.5, pregunta 3 | S-6 | en parte |
| `VISOR-CONSTRUCCION.md` §3.2, A | — | S-8 | sí: (a), con una condición |
| `VISOR-CONSTRUCCION.md` §3.2, B | — | S-11 | sí: (b); A-46 no se reabre |
| La pregunta 3 de `PUNTO-USADO.md` (la caja de la reentrada) | `PUNTO-USADO.md` §5 | S-6 | en parte: en su ejemplo se actualiza el nivel 0 y el 1 sigue; si la caja es nueva y el número de reentradas, no los dice |

Lo demás que V nombra también se preguntó: las dos de `SESGO-H4-COLOR.md` §4.4 (S-1 y S-2, las dos
sí), las de ADR-0076 §4 (S-19 sí y S-20 en parte), ADR-0077 §5 (S-21 sí), RN-035 (S-22 sí), ADR-0075
(S-23 sí) y la pregunta 7 de CORRIDA §4.5 (S-14, en parte).

## 5. Tabla final

| Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|---|
| **S-3** | A-35 | v15 | 03:59–07:40 | en parte: la primera mitad **resuelve**, (b) = `cierre_vela_contraria`, sin PARADA; la segunda no tiene parámetro | sí | no | sí |
| **S-4** | A-44 | v15 | 07:40–15:59 | en parte: alcance (a), el día; la magnitud no la dijo: **PARADA de §4** | sí | sí | n/a |
| **S-5** | A-57 | v15 | 16:02–19:27 | **resuelve**: (a), bajar el lote a lo que cabe | sí, «por ahora» | sí | n/a |
| **S-6** | pregunta 3 (ADR-0083) | v15 | 19:31–28:19 | en parte: se actualiza el nivel 0 y el 1 sigue; sin número de reentradas; ADR-0083 ni confirmado ni negado | en parte | sí | no lo dice |
| S-1 | ADR-0080 | v15 | 00:10–01:48 | **resuelve**: (b), sigue bajista; casa con ADR-0080 y choca con la sesión 1 | sí | no | solo bajista |
| S-2 | ADR-0080 §4 | v15 | 01:51–03:57 | **resuelve**: (b), sigue el sesgo anterior | sí | no | la regla sí; el caso bajista no |
| S-7 | A-48, A-49 | v15 | 28:19–36:26 | en parte: la traza al cierre; el 1 se actualiza; no elige opción | en parte | sí, sobre el esquema | sí |
| S-8 | VISOR §3.2, A | v15 | 36:26–41:17 | **resuelve**: (a), con una condición | sí | sobre el esquema | sí |
| S-9 | CORRIDA §4.5, p. 5 | v15 | 41:19–46:44 | **resuelve**: (a), la más reciente | sí | no | solo compra |
| S-10 | A-43 (2.ª parte) | v15 | 46:48–51:41 | en parte | sí | no | solo compra |
| S-11 | VISOR §3.2, B | v15 | 51:46–58:48 | **resuelve**: (b); A-46 no se reabre | sí | no | sí |
| S-12a | RN-005 (el lado) | v15 | 58:50–65:53 | **resuelve**: (b), por debajo; contra `ev-v9-004919-c6bfb3ee` | sí | solo en 60:31 | sí |
| S-12b | A-50 | v15 | 64:51–65:53 | en parte, y contra el bot | en parte | no | sí |
| S-13 | A-53 | v15 | 65:54–69:10 | en parte, hacia (b); la subpregunta del recuadro no se hizo | sí | no | no lo dice |
| S-14 | CORRIDA §4.5, p. 7 | v15 | 69:10–80:27 | en parte | en parte | no | n/a |
| S-15 | CORRIDA §4.5, p. 8 | v15 | 80:29–86:41 | **resuelve**: (c), la zona más reciente; contra el bot | sí | no | no lo dice |
| S-16 | CORRIDA §4.5, p. 9 | v15 | 86:45–92:54 | no resuelve | no | sí, sobre el tipo de orden | — |
| S-17 | A-13 | v15 | 93:03–98:07 | en parte: se contradice dentro de la respuesta | en parte | no | sí |
| S-18 | A-32 | v15 y v16 | v15 98:07–100:37 (incompleta); v16 00:10–06:21 | **resuelve** (la de v16): (a) | sí | solo sobre si ya la había respondido | sí |
| S-19 | ADR-0076 §4, p. 1 | v16 | 06:33–09:19 | **resuelve**: (b) | sí | no | sí |
| S-20 | ADR-0076 §4, p. 2 | v16 | 09:24–18:46 | en parte | en parte | no | no lo distingue |
| S-21 | ADR-0077 §5 | v16 | 18:53–21:35 | **resuelve**: (a), de cero; contra el bot | sí | no | n/a |
| S-22 | RN-035 | v16 | 21:37–23:47 | **resuelve**: un minuto antes | sí | no | n/a |
| S-23 | ADR-0075 | v16 | 23:49–26:46 | **resuelve**: (a) | sí | solo en un ejemplo | sí, con la sesión 4 |
| S-24 | RN-007 (H) | v16 | 26:48–28:55 | **resuelve**: (d), el umbral es cero; contradice la sesión 4 | sí | lo dice y se corrige | n/a |
| S-25 | `ENTRADA-JULIO.md` §8 | v16 | 29:02–32:10 | en parte, hacia (a): cree que está en orden | n/a | sí | n/a |
| Para cerrar | NA:I, NA:Q, marzo | v16 | 32:10–34:41 | marzo: confirmación escrita recibida; diciembre y agosto: lo que dijo, sin decidir | n/a | sí (agosto) | n/a |

Resuelve: 14. En parte: 11. No resuelve: 1 (S-16). Más «Para cerrar». (S-25 pasó de «resuelve,
con dudas» a «en parte» tras el revisor, hallazgo a2.)

## 6. Para la orden de cierre (preparado, sin aplicar)

Nada de esto se aplica en la rama: ni registro de cierre en HISTORIA ni cambios de la Next Action
(encargo, «Cierre de la rama»).

**a) A.3 pasa a HECHA** (`docs/plan/HOJA-DE-RUTA.md`, «A.3 · La agenda con el trader»). Texto nuevo
de su línea de Estado:

> - **Estado:** HECHA (2026-10-25). La sesión 5 se grabó en dos días, el 2026-10-23 (v15) y el
>   2026-10-25 (v16), con un solo id, `2026-10-23-sesion-05` (SESION-05-EXTRACCION.md). La
>   confirmación escrita del trader sobre marzo llegó por WhatsApp el 2026-10-25 a las 13:58 (hora
>   de Lima), «Confirmado backtest de marzo», registrada en `fuentes.yaml` («Mensajes del trader») y
>   en SESION-05-EXTRACCION.md §3.5. Lo que queda del paso 0 de marzo, marzo en `vistos.yaml`, es de
>   R5.3.

**b) El heredado 2 de `PROJECT_STATE.md`** («Pendientes heredados»), que pedía la confirmación.
Texto nuevo:

> - 2. Marzo: faltan vistos.yaml y el paso a (hoja de ruta, R5.3); la confirmacion escrita del
>   trader llego el 2026-10-25 (A.3 HECHA; SESION-05-EXTRACCION.md §3.5).

Son unos 40 bytes más que la línea de hoy (`PROJECT_STATE.md` está en 23.796).

**c) Lo que sigue pendiente del paso 0 de marzo:** marzo en `knowledge/corpus/vistos.yaml`
(`REGISTRO-MARZO.md` §2, paso 0), que esta rama no toca (encargo, «Lo que no se hace en esta
rama»). Después, el paso a (la columna de fechas, que lee Aleks una vez y antes del sorteo). **Lo
que dice todavía que falta la confirmación**, y que la orden de cierre tendrá que mirar
(`grep -i "confirmacion escrita"`, lección de `trabajo/adelgazar-estado` en
`ERRORES-RECURRENTES.md`): `CLAUDE.md:180`, `docs/runbooks/ENTRADA-MARZO.md:35` y `:111`, y R5.3 de
`docs/plan/HOJA-DE-RUTA.md` («Qué es» y «Depende de»).

**d) Una línea de Technical Debt** (respuesta del consultor a la PARADA de v16, punto 4), del carril
de guardias y de la cuarentena por condición; no se arregla en esta rama:

> - LA CUARENTENA POR CONDICION NO TAPA UNA FECHA NUMERICA SEGUIDA DE COMA (2026-10-25,
>   trabajo/sesion-05, SESION-05-EXTRACCION.md §2.7): `motivos_cuarentena('hoy 25 del 10')` da
>   `['fecha numerica']` y `motivos_cuarentena('hoy, 25 del 10,')` da `[]`; el lookahead
>   `(?![\d.,])` excluye la coma para no tapar precios como «10,5» y deja pasar las fechas en
>   prosa. Carril de guardias y cuarentena por condicion.

Unos 380 bytes. Con a), b) y d), `PROJECT_STATE.md` quedaría hacia 24.220 bytes, bajo 25.000.

**e) Para la activación (V, R4.1):** un registro de feedback que cite v16 lleva `fecha` 2026-10-23
y `recibido_el` 2026-10-25 (`feedback/modelo.py:113`, comprobado en §0.4).

## 7. Desviaciones y negativas de la guardia

Las negativas de la guardia de Claude Code (`.claude/hooks/guardia.py`) se declaran aquí, como manda
el encargo («Reglas de esta rama»; `docs/runbooks/DECISIONES-DE-PROCESO.md`). **Ninguna negó un paso
que mande la skill `ingerir-sesion`**, así que ninguna es el hallazgo de PARADA del encargo.
1. **Comandos compuestos, por descuido de la sesión.** La guardia negó siete veces un comando que
   ejecutaba código detrás de otro o con `$(...)`: un `sed` con `$(...)`; `wc -c` seguido de `state
   check`; `git add` seguido de `pytest`; `git status` seguido de `contrato_rama.py`; `cat` de un log
   seguido de `frames check`; `ls` y `cat` de un ítem con `$(...)`; y `rm` de un ítem sin commitear
   seguido del guion de citas. Cada uno se rehízo en la forma que la propia guardia propone en su
   mensaje: llamadas separadas y rutas literales.
2. **`PYTHONIOENCODING=utf-8` delante de un guion** (para que la salida no saliera en cp1252): la
   guardia lo niega porque el nombre no está en `NOMBRES_DE_ENTORNO`. Se rehízo como propone, sin la
   variable: el guion de la carpeta de trabajo (`cita_de_rango.py`) reconfigura su propia salida.
3. **`uv run botsito corpus transcript show --help`**: la guardia lo lee como imprimir la cruda. Se
   abandonó, no se reescribió; la ayuda no hacía falta.
4. **El detector más estrecho que la regla del encargo**, y la PARADA de v16: §2.7.
5. **El día 2026-10-25 se comprobó después de grabar** (encargo): §0.2 y `HOLDOUT-EXPOSICIONES.md`.
6. **El primer `make check` de la rama salió en rojo** en `test_hoja_de_ruta`: el informe todavía
   no tenía tabla final ni decía que era una PLANTILLA. Se añadió la línea de PLANTILLA, que este
   informe ya no necesita y quita.
7. **Los dos bloques en cuarentena de v16 entraron en `tramos_no_citables.yaml` después del commit
   de v16** (`7b4b463`), en su commit propio (`5f47908`), y antes de crear ningún ítem de
   evidencia: se habían quedado fuera del primero por descuido.
8. **`detector_julio.py` en el anexo** lleva su expresión `DIA_NUM` partida en tres líneas por `ruff
   format`; la cadena y la salida son las mismas (§2.7).
9. **Un ítem de evidencia se creó y se borró antes de commitear** (el de S-12a, en 1:01:04): su
   cita acababa en «queda por» y se rehízo con la línea siguiente (`ev-v15-010104-23adba23`).
   **Dos `evidence new` fallaron y se rehicieron**: modalidad `ambas` sin fotograma (en esta rama no
   se abre ninguno: `audio`), y la cita de agosto con la línea de 32:56, que toca un tramo de
   cuarentena.

### 7.1 La PARADA del `make check` de la extracción, y la respuesta del consultor

**El rojo (2026-10-25).** El primer `make check` con la evidencia y este informe estadiados salió
con `7 failed, 2911 passed`, por tres causas:
1. **Un id que no existe, error de la sesión.** El §7 citaba el id del ítem de S-12a que se creó y
   se borró antes de commitear. Lo cazaron tres ficheros de tests, que llaman a `knowledge
   validate` y vieron su `ERROR: id citado que no existe: docs/validation/SESION-05-EXTRACCION.md:1272`:
   `tests/unit/test_cli.py` (dos tests), `tests/unit/test_citas_supersedidas.py` y
   `tests/unit/test_historial_sin_git.py` (dos tests). Se redactó sin el id, y los tres ficheros
   pasan. **La lección: un id de evidencia se cita solo después de que su fichero esté escrito,
   nunca antes** (punto 1 de la respuesta).
2. **`test_en_parte_no_se_cierra.py::test_la_sesion_4_deja_en_parte_lo_que_dice_su_tabla`.** Leía
   todas las extracciones y exigía que A-32 siguiera «solo en parte». La sesión 5 la resuelve
   (S-18, v16).
3. **`test_hoja_de_ruta.py::test_d_…`**: «A-48: SESION-05-EXTRACCION.md la da por respondida, sigue
   ABIERTA y no esta en R1 ni R4». La sesión 5 deja A-48 en parte (S-7), y R4.1 no la nombraba.

**La respuesta del consultor (2026-10-25)**, copiada tal cual:

> Respuesta del consultor a la PARADA del make check de la extracción (2026-10-25). Cópiala al informe, en su sección.
>
> 1. El id inexistente del §7: bien corregido. Declara en el informe cómo se cazó (los tres tests) y la lección: un id de evidencia se cita solo después de que su fichero esté escrito, nunca antes.
> 2. SÍ: test_la_sesion_4_deja_en_parte_lo_que_dice_su_tabla lee solo SESION-04-EXTRACCION.md (es una comprobación de que el lector lee algo de la sesión 4, como dice su docstring). Amplía el contrato a ese fichero de test en un commit propio que lo declare. El test de la regla (una «en parte» no puede estar RESUELTA) sigue leyendo TODAS las extracciones y no se toca. Enseña en el informe que sigue pasando y que se rompe a propósito.
> 3. SÍ, opción (a): levanto la prohibición del añadido de marzo SOLO para este cambio. Se añade ID:A-48 a las Refs de R4.1 en docs/plan/HOJA-DE-RUTA.md, y nada más de la hoja de ruta (A.3 sigue preparada para la orden de cierre, no se aplica aquí). Amplía el contrato a HOJA-DE-RUTA.md en el mismo commit propio, declarándolo. La fila de S-7 se queda como está («A-48, A-49», «en parte»): no se toca la extracción para que pase un test.
> 4. El hallazgo de agosto (32:56 toca el tramo en cuarentena que empieza en 0:32:58 y evidence new lo rechaza): correcto no citarlo. En «Para cerrar», di que lo de agosto queda sin cita por ese motivo y qué se entiende sin citar (si dice que la exportación está o no), para que yo lo decida en la activación.
>
> Después: make check sellado, commit, push a fix/sesion-05, CI con un gh run view suelto y el revisor, como dice el encargo.

**Cómo se aplicó, punto por punto:**
1. Hecho: arriba, y en el §7, punto 9.
2. Hecho en el commit propio `36490d6`, sellado con `make check` (`SELLO … 9b9731d8…`, exit 0). Para
   que ese sello viera solo sus tres ficheros, la extracción se apartó con `git stash` y se recuperó
   después. El test lee solo `SESION-04-EXTRACCION.md` y comprueba que ese fichero está entre los
   que lee el otro test. El contrato se amplía con ese fichero, declarado en su comentario y en el
   mensaje del commit. **El test de la regla (`test_ninguna_en_parte_esta_resuelta`) no se ha
   tocado y sigue leyendo todas las extracciones.** Con la sesión 5 ya en el árbol:
   - `pytest -rA` de los dos ficheros: `18 passed`, entre ellos
     `test_ninguna_en_parte_esta_resuelta`, `test_la_sesion_4_deja_en_parte_lo_que_dice_su_tabla`
     y `test_se_rompe_a_proposito_si_una_en_parte_figura_resuelta`.
   - **Roto a propósito sobre el repo real** (`romper_en_parte.py`, carpeta de trabajo; importa las
     funciones del test y no escribe nada):
     ```
     extracciones leidas: ['SESION-02-EXTRACCION.md', 'SESION-03-EXTRACCION.md', 'SESION-04-EXTRACCION.md', 'SESION-05-EXTRACCION.md']
     solo en parte (todas): ['A-13', 'A-35', 'A-43', 'A-44', 'A-48', 'A-49', 'A-50', 'A-53']
     real -> en_parte_cerradas: []
     A-13 puesta RESUELTA a proposito -> ['A-13 (RESUELTA)']
     A-48 puesta RESUELTA a proposito -> ['A-48 (RESUELTA)']
     ```
     Con la sesión 5, A-32 sale de «solo en parte» porque S-18 la resuelve, y A-48 y A-49 entran,
     porque S-7 las deja en parte.
3. Hecho en el mismo commit propio `36490d6`: `ID:A-48` en las Refs de R4.1 y nada más de la hoja
   de ruta. A.3 no se toca: sigue preparada en §6. El contrato se amplía con
   `docs/plan/HOJA-DE-RUTA.md`, declarado. La fila de S-7 de la tabla final no cambia. Con eso,
   `test_d_lo_que_el_trader_respondio_y_sigue_abierto_esta_en_un_tramo_de_sesion` pasa.
4. Hecho: «Para cerrar», agosto (§3.5).

## 8. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` (v15, v16 y la captura de marzo en «Mensajes del trader») y
  `manifest.yaml`.
- Las transcripciones `tr-v15-large-v3-int8-float16-2ec65e67` y
  `tr-v16-large-v3-int8-float16-dc91b386`, y los fotogramas `fr-v15-5dcfa8d3` y `fr-v16-21754f20`.
- `knowledge/corpus/tramos_no_citables.yaml`: 11 tramos nuevos. De v15, 7: 1 SIN AUDIO, 3 de
  precaución y 3 ajenos. De v16, 4: 2 de precaución y 2 de cuarentena.
- **55 ítems de evidencia, 49 vivos** (abajo). En `0f173b3` entraron 49: 31 de v15 y 18 de v16.
  Tras el revisor (hallazgo a1) entraron 6 más, 3 de cada vídeo, que supersedan cada uno a uno de
  aquellos con el mismo tema, porque la evidencia commiteada no se edita. `evidence contradictions`
  da `0 contradicciones abiertas`, y `knowledge validate` está en verde (§10).
- `src/botsito/corpus/cuarentena.py` (v15 y v16 en `SESIONES_EN_CUARENTENA`) y sus tests
  (`test_inventario`, `test_cuarentena`, `test_guardia_claude`).
- `docs/sesion-5/HOJA-USADA.md` y el recuadro de `docs/sesion-5/PREGUNTAS.md`.
- `tests/unit/test_en_parte_no_se_cierra.py` (la comprobación de la sesión 4 lee solo su informe) y
  `ID:A-48` en las Refs de R4.1 de `docs/plan/HOJA-DE-RUTA.md` (§7.1).
- `docs/validation/HOLDOUT-EXPOSICIONES.md`: cuatro filas del 2026-10-25.
- `docs/validation/anexos/SESION-05/`: `detector_julio.py` y `barrido_18_31.py`.

**La evidencia, por código:**

| Código | Ítems |
|---|---|
| S-1 | `ev-v15-000049-3b294480`, `ev-v15-000138-ef123dfc` |
| S-2 | `ev-v15-000256-f3c52278` |
| S-3 | `ev-v15-000447-6699c708`, `ev-v15-000530-234d4a81`, `ev-v15-000553-9d95178a` |
| S-4 | `ev-v15-000856-ee8f7ba3`, `ev-v15-000913-bdb12f92`, `ev-v15-001546-0dadd11e` |
| S-5 | `ev-v15-001758-c27d9c4c` |
| S-6 | `ev-v15-002029-1ac081ae`, `ev-v15-002441-2e609b87` (supersede a `ev-v15-002441-ec3c910c`), `ev-v15-002729-30480ec5` |
| S-7 | `ev-v15-003244-dcd8a834`, `ev-v15-003619-9fbc7f08` (supersede a `ev-v15-003619-60121c7d`) |
| S-8 | `ev-v15-003959-5898c61e`, `ev-v15-004037-a2ab3980` |
| S-9 | `ev-v15-004448-aac87b77` |
| S-10 | `ev-v15-005126-5baccf2a` |
| S-11 | `ev-v15-005839-f2e43c27` |
| S-12a | `ev-v15-010104-23adba23` |
| S-12b | `ev-v15-010451-5b123278` |
| S-13 | `ev-v15-010818-cc8e1e08`, `ev-v15-010850-f0728663` (supersede a `ev-v15-010850-e3c57529`) |
| S-14 | `ev-v15-011023-5f0f2dd1`, `ev-v15-011728-b5bd4d05`, `ev-v15-011912-0ae32588`, `ev-v15-011956-dce80292` |
| S-15 | `ev-v15-012616-d534455a` |
| S-16 | — (no resuelve) |
| S-17 | `ev-v15-013510-6364e7e0`, `ev-v15-013605-c041b814` |
| S-18 | `ev-v16-000234-9a4fa375`, `ev-v16-000603-6955d127` (la de v15, incompleta, sin ítem) |
| S-19 | `ev-v16-000851-f5ae3b6f` |
| S-20 | `ev-v16-001445-7ca4f033`, `ev-v16-001834-732a76b6` |
| S-21 | `ev-v16-001952-9fe00b36` (supersede a `ev-v16-001952-63c96f1f`), `ev-v16-002126-d2376f71` |
| S-22 | `ev-v16-002248-08e9600f`, `ev-v16-002323-515b9da4` |
| S-23 | `ev-v16-002521-02c1be20`, `ev-v16-002641-e8e6eafc` |
| S-24 | `ev-v16-002746-31cbc565`, `ev-v16-002841-8cfe382a` (supersede a `ev-v16-002841-b47d0461`) |
| S-25 | `ev-v16-003010-e455f173` (supersede a `ev-v16-003142-bb737430`), `ev-v16-003149-b3b79c79` |
| Para cerrar | `ev-v16-003228-b515b93e` (diciembre), `ev-v16-003249-49af3f8b` (agosto), `ev-v16-003421-b824b770` (el error de agosto, con S-14) |

Marzo no tiene ítem: la petición cae en la cuarentena y la confirmación es un mensaje escrito, que
va en `fuentes.yaml`.

## 9. El cierre de la rama: sellos, push y CI

**Los commits**, cada uno con su `make check` sellado (exit 0, ningún `failed`, la línea `SELLO`):

| Commit | Qué | SELLO (árbol) |
|---|---|---|
| `c6d7cef` | abre la rama: encargo, contrato y Archivo 46 | sellado; el hash no se guardó (el log se reescribe en cada `make check`) |
| `1e86611` | registro de v15 y v16, en cuarentena; corte SIN AUDIO de v15 | ídem |
| `334a49b` | v15 transcrita, filtrada y con fotogramas; sus tramos | ídem |
| `7b4b463` | v16 transcrita, filtrada y con fotogramas; sus tramos de precaución; la PARADA de julio | `9cb61644…` |
| `5f47908` | los dos bloques en cuarentena de v16, en su commit propio | `7592a346…` |
| `36490d6` | commit propio de §7.1: el test de la sesión 4 y `ID:A-48` en R4.1 | `9b9731d8…` |
| `0f173b3` | la extracción, la evidencia y la hoja usada | `1d75befb…` |

El último `make check`, el de `0f173b3`: `SELLO: make check en verde sobre el arbol
1d75befbda8808508abad5305298b5d33f5a7e49`, `DURACION de make check: 1122 s`, `PICO DE MEMORIA de
make check: 298 MiB`, `exit=0`. Comprobaciones del contrato sobre ese commit:
- `git diff --name-status main...HEAD -- knowledge/evidence knowledge/corpus/transcripciones
  knowledge/corpus/fotogramas data/manifests`: `53 A`, nada más;
- `knowledge validate`: `OK: 552 items de evidencia, 0 contradicciones abiertas, historial
  intacto`;
- `evidence contradictions`: `0 contradicciones abiertas`.

**`PROJECT_STATE.md`**: 23.796 bytes, lo mismo que tras abrir la rama. La rama no lo toca más, y
con lo preparado en §6 quedaría hacia 24.220, bajo 25.000.

**Push**: `git push origin trabajo/sesion-05:refs/heads/fix/sesion-05`, `* [new branch]
trabajo/sesion-05 -> fix/sesion-05`. El clasificador no lo negó.

**CI de Linux, run 40254117212** (`fix/sesion-05`, sobre `0f173b3`). Se esperó con un `sleep` en
segundo plano y se consultó con un solo `gh run view` suelto. **Falla solo el test esperado**:
`FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` con `ERROR: PROJECT_STATE declara
la rama 'trabajo/sesion-05'; la rama actual es 'fix/sesion-05'`. El resultado:
`1 failed, 2871 passed, 46 skipped in 215.45s`.

Este §9 entra en un commit posterior a `0f173b3`, que se empuja igual a `fix/sesion-05`. Su run va
en la sección del revisor.

## 10. El encargo, punto por punto

El encargo (cuatro mensajes, el añadido de marzo y las dos respuestas del consultor a las PARADAS,
copiadas al final de `docs/encargos/trabajo-sesion-05.md`), partido en requisitos:

| # | Requisito | Estado | Dónde |
|---|---|---|---|
| 1 | Abrir con `abrir-rama`: encargo, contrato y Archivo en HISTORIA | Hecho | `c6d7cef`; «Base comprobada al abrir» |
| 2 | Comprobar la base: main, tag, CI, ramas, hoja 05 en el guion y regla del 2026-10-21 | Hecho | «Base comprobada al abrir» |
| 3 | Copiar el encargo tal cual con Write, y después las respuestas del consultor | Hecho | `docs/encargos/trabajo-sesion-05.md` (las respuestas, añadidas tras el revisor, b2) |
| 4 | Duraciones exactas con ffprobe | Hecho | §0.3 |
| 5 | v15 y v16, siguientes ids libres, con `drive_id` null y en `SESIONES_EN_CUARENTENA` | Hecho | §0.3, §1 |
| 6 | Medir si se admiten dos vídeos por id de sesión, con el precedente | Hecho | §0.4 |
| 7 | Nota para la activación: un feedback de v16 lleva `fecha` 2026-10-23 y `recibido_el` 2026-10-25, con la línea verificada | Hecho | §0.4; §6 e) |
| 8 | Buscar el código de S-17 en las dos filtradas | Hecho | §3.3 (S-17), §3.4 |
| 9 | No resolver nada; no tocar `transcribir_sesion.py`; ADR-0081 y ADR-0083 siguen PROVISIONALES | Hecho | rutas protegidas sin tocar (§9); «Estado» |
| 10 | Negativas de la guardia: PARADA, o la forma que propone, declarada | Hecho | §7 |
| 11 | Los dos días con `casos_ocultos`; la desviación del 25 declarada | Hecho | §0.2 |
| 12 | Preguntas a) a d) antes del registro, y sus respuestas tal cual | Hecho | §0.1 |
| 13 | Toda consulta de casos y toda lectura de una filtrada, declarada el mismo día | Hecho | `HOLDOUT-EXPOSICIONES.md`, cinco filas del 2026-10-25 (la quinta, tras el revisor, a4) |
| 14 | `HOJA-USADA.md` con la forma de la de la sesión 4, sin citas del trader | Hecho | `docs/sesion-5/HOJA-USADA.md` |
| 15 | Recuadro en `PREGUNTAS.md` que apunte a `HOJA-USADA.md` | Hecho | `PREGUNTAS.md`, recuadro del 2026-10-25 |
| 16 | Verificar que los recuadros de la hoja son S-7, S-12, S-13 y S-15 | Hecho | `HOJA-USADA.md` §4 |
| 17 | Filtradas con el guion de `main` y `--sesion 05`; revisar «veinte y N» en el bloque de S-20 | Hecho | §2.2, §2.5, §3.4 |
| 18 | Registro: `naturaleza` del vídeo entero, `test_inventario`, `corpus inventory` y `check --hashes` | Hecho | §1, §1.2 |
| 19 | Test roto a propósito antes de la cuarentena, y después pasando | Hecho | §1.1 |
| 20 | Audio con las formas de la skill, en WAV de nombres distintos fuera del repo | Hecho | §0.3, §2.1 |
| 21 | Antes de la segunda transcripción, comprobar que los ficheros de v15 siguen ahí | **Parcial** | no consta en el informe que se hiciera; lo que se ve después, sí (§11, b3) |
| 22 | Corte SIN AUDIO en los tramos, y la puerta del ASR | Hecho | §2.1, §2.2 |
| 23 | «Listo» de Aleks antes de cada transcripción; bloques de cuarentena en un commit propio por vídeo | Hecho; v16 en un commit posterior, declarado | §2.2, §2.5; §7, punto 7 |
| 24 | `frames extract` y `frames check` de los dos | Hecho | §2.4 |
| 25 | Ningún fotograma abierto; citas solo de la filtrada | Hecho | §2.4 |
| 26 | Día de julio del 18 en adelante fuera de la cuarentena: PARADA sin copiarlo | Hecho | §2.7 |
| 27 | Informe con la forma de la sesión 4 y la tabla final con sus columnas | Hecho | §3, §5 |
| 28 | Orden: S-3 y S-4 con `ACTIVAR-A35-A44.md`, después S-5 y S-6, después el resto | Hecho | §3.1, §3.2, §3.3 |
| 29 | S-12 en dos filas | Hecho | §3.3, §5 |
| 30 | S-1 y S-2 frente a ADR-0080 y la sesión 1 | Hecho | §3.3 |
| 31 | «Para cerrar»: diciembre, agosto y marzo, solo lo que dijo | Hecho | §3.5 |
| 32 | Evidencia fuera de todos los tramos; `evidence contradictions` y `knowledge validate` en verde | Hecho | §8; §11 (a1) |
| 33 | Cobertura de V, y qué pasa con H tras S-24 | Hecho | §4.3, §4.2 |
| 34 | Lista para la copia A.4, al final del informe | Hecho | §12 (se movió al final tras el revisor, b5) |
| 35 | `PROJECT_STATE.md` bajo 25.000 bytes | Hecho | 23.796 (§9) |
| 36 | Cierre: sello, push a `fix/`, CI con solo el fallo esperado, número de run; sin registro de cierre en HISTORIA | Hecho | §9; §11 |
| 37 | Añadido de marzo: `fuentes.yaml`, literal, hora, contexto, HOLDOUT, A.3 y heredado 2 preparados, lo que queda del paso 0 | Hecho | §3.5, §6 |
| 38 | Añadido de marzo: no tocar `vistos.yaml` ni la hoja de ruta | Hecho de otra forma, declarado | `vistos.yaml` sin tocar; en la hoja de ruta solo `ID:A-48`, por la respuesta del consultor (§7.1) |
| 39 | Respuesta a la PARADA de v16: tramo, HOLDOUT, barrido antes de leer, anexo, línea de Technical Debt, el dato sin usar | Hecho | §2.7, §6 d) |
| 40 | Respuesta a la PARADA del `make check`: lección, test de la sesión 4, `ID:A-48`, agosto sin cita | Hecho | §7.1, §3.5 |
| 41 | Revisor con el informe terminado y su informe pegado al final | Hecho | «Informe del revisor» |
| 42 | «Rama lista para revisión, NO cerrada» | Hecho | «Estado» |

## 11. Lo que se hizo con los hallazgos del revisor

El revisor (subagente `revisor`) revisó `90a1da5`: **eje (a), 0 bloquea, 4 importa y 4 menor;
eje (b), 0 bloquea, 4 importa y 1 menor.** Su informe está al final, tal cual salvo lo que se dice
allí. Uno por uno:
- **a1 (importa), afirmaciones que dicen más que su cita.** Arreglado con seis ítems nuevos que
  supersedan a los seis con el mismo tema (`evidence new --supersede`; la evidencia commiteada no se
  edita):

  | Superseded | Nuevo | Qué cambia |
  |---|---|---|
  | `ev-v15-002441-ec3c910c` | `ev-v15-002441-2e609b87` | la cita llega a 24:51; la afirmación dice que se actualiza el 0 y el 1 sigue, sin «no es la del primer intento» |
  | `ev-v16-003142-bb737430` | `ev-v16-003010-e455f173` | la cita es la respuesta a la pregunta (30:10–30:20), con «creo»; confianza baja |
  | `ev-v15-003619-60121c7d` | `ev-v15-003619-9fbc7f08` | sin la condición de fuera de la ventana |
  | `ev-v15-010850-e3c57529` | `ev-v15-010850-f0728663` | sin «no se quita» |
  | `ev-v16-001952-63c96f1f` | `ev-v16-001952-9fe00b36` | la cita trae el arranque de la línea; «no suelen», sin «ese día» |
  | `ev-v16-002841-b47d0461` | `ev-v16-002841-8cfe382a` | sin «y no se usa para trazar el punto» |

  `evidence contradictions`: `0 contradicciones abiertas`. `knowledge validate`: `OK: 558 items de
  evidencia, 0 contradicciones abiertas, historial intacto`.
- **a2 (importa), dos propuestas que dicen más que su cita.** S-6 corregida en §3.2, §4.3 y §5: se
  actualiza el 0 y el 1 sigue. S-25 corregida en §3.4, §4.1, §4.3 y §5: cita 30:10–30:20 y pasa a
  «en parte». El recuento de §5 queda en 14, 11 y 1.
- **a3 (importa), citas de dentro del tramo 0:30:41–0:31:37.** Retiradas de §2.7: queda solo el
  motivo del tramo, con una nota. Tampoco van en el informe del revisor pegado abajo.
- **a4 (importa), un día de diciembre leído y no declarado.** Declarado en `HOLDOUT-EXPOSICIONES.md`
  (fila nueva del 2026-10-25) sin copiar el número; el número tampoco va en el informe del revisor
  pegado abajo (ver allí). **Para el consultor:** la cuarentena por condición trata diciembre como
  libre (`meses_libres` incluye el 12) mientras NA:I no ha decidido si es construcción o reservado.
  Es un caso de la línea de Technical Debt de §6 d) o de una nueva, y lo decide él.
- **a5 (menor), la remisión a `PREGUNTAS.md:83`.** Arreglada en §0.1: remite a la sección, porque el
  recuadro nuevo de esta rama movió las líneas.
- **a6 (menor), la marca de S-4.** Arreglada: «[08:57] no».
- **a7 (menor), `barrido_18_31.py` solo ve cifras.** Sin cambio: el consultor mandó copiar los dos
  guiones tal cual, y el revisor midió que en estas dos filtradas no hay ningún número de 18 a 31
  escrito en letra. Queda para el consultor si la puerta se amplía.
- **a8 (menor), agosto sin aviso de voces.** Arreglado en §3.5.
- **b1 (importa), falta «El encargo, punto por punto».** Arreglado: §10.
- **b2 (importa), las respuestas del consultor no están al final del encargo.** Arreglado: están
  copiadas tal cual al final de `docs/encargos/trabajo-sesion-05.md`.
- **b3 (importa), no consta la comprobación de los ficheros de v15 antes de la segunda
  transcripción.** No se puede arreglar a posteriori, y no se afirma que se hiciera. Lo que se ve
  después: en `C:\Users\USER\Desktop\sesion-05-audio\` siguen los ficheros de v15
  (`sesion-05-v15.wav`, `.cruda-NO-LEER.*`, `.filtrada.md` y `.registro.txt`, de las 15:17 y las
  16:21) junto a los de v16 (17:27), con nombres distintos (§12). Requisito 21 de §10: parcial.
- **b4 (importa), la medida del reloj de v16.** Contestado en §3.5: se deja, porque el añadido pide
  el contexto de la confirmación, y la medida ni lo cambia ni decide nada. Si el consultor la ve de
  más, se quita.
- **b5 (menor), la lista A.4 no estaba al final, y «Estado» seguía EN CURSO.** Arreglado: la lista
  es §12, la última sección antes de «Estado», y el informe del revisor va pegado después, como en
  la sesión 4. «Estado» ya no dice EN CURSO.
- **Lo que el revisor declaró de sí mismo.** Su lectura de las filtradas, en la fila nueva de
  `HOLDOUT-EXPOSICIONES.md`. La consulta de CI de más (`--log-failed`) y la guardia que le negó un
  `python -c`: quedan dichas aquí.

**Después de los arreglos:** `make check` sellado, commit, push a `fix/sesion-05` y la CI de ese
commit (el run va en el mensaje final a Aleks: este informe no puede llevar el run de su propio
commit). No se lanzó otra pasada del revisor: el encargo pide una.

## 12. Para la copia de seguridad A.4: lo nuevo fuera de git

Lo que esta rama dejó en la máquina y no está en el repositorio:
- **Los vídeos**, en `corpus/Estrategia del trader/`:
  - `Grabación de pantalla 2026-10-23 174536.mp4` (v15, 6.740.009.101 bytes);
  - `Grabación de pantalla 2026-10-25 140140.mp4` (v16, 2.324.823.273 bytes).
- **La captura de marzo**, en `corpus/Estrategia del trader/Material adicional de su
  operativa/Mensajes del trader/mensaje-whatsapp-2026-10-25-1358.png` (sin abrir).
- **Las transcripciones del corpus**, `data/transcripciones/v15/` y `data/transcripciones/v16/`: en
  cada una, `audio.wav`, `audio.sha256_video` y la carpeta `large-v3-int8-float16/` (`cruda.jsonl`,
  `cruda.txt`, `corregida.jsonl`, `correcciones.jsonl`, `huella.txt`, `video.sha256`, `fragmentos/`
  y `parciales/`).
- **Los audios y las salidas del guion**, en `C:\Users\USER\Desktop\sesion-05-audio\`:
  `sesion-05-v15.wav` (193.828.942 bytes) y `sesion-05-v16.wav` (66.879.566 bytes); de cada vídeo,
  `.cruda-NO-LEER.jsonl`, `.cruda-NO-LEER.txt`, `.filtrada.md` y `.registro.txt`; y las carpetas
  `sesion-05-v15-trabajo/` y `sesion-05-v16-trabajo/`.
- **Los fotogramas**, `data/fotogramas/v15/` (2,7 GB) y `data/fotogramas/v16/` (772 MB): se
  regeneran desde el vídeo con `corpus frames extract`, así que copiarlos o no lo decide Aleks.

## Estado

Extracción terminada el 2026-10-25, con los hallazgos del revisor arreglados o contestados (§11):
- los dos vídeos ingeridos: registro, audio, transcripción, cuarentena y fotogramas;
- las 25 preguntas y «Para cerrar», extraídas con su propuesta;
- 55 ítems de evidencia, de los que 49 están vivos;
- la tabla final.

**Esta rama no resuelve nada**: ni feedback, ni ambigüedades, ni spec, ni motor, ni casos. ADR-0081
y ADR-0083 siguen PROVISIONALES. Lo decide el consultor, en V (R4.1):
- la **PARADA de §4 de `ACTIVAR-A35-A44.md` para A-44** (S-4: la magnitud del tope no se dijo);
- las contradicciones de §4.1;
- qué hace con H (§4.2) y con lo preparado para la orden de cierre (§6);
- diciembre en `meses_libres` (§11, a4) y la puerta del barrido (§11, a7).

Rama lista para revisión, NO cerrada.

## Informe del revisor

Pegado tal cual. Sus encabezados bajan dos niveles para que queden dentro de esta sección y ninguna
de sus tablas se lea como la tabla final del informe. Y salvo tres cosas, que se marcan entre
corchetes donde estaban:
- **dos citas retiradas** porque son de dentro de un tramo no citable (`entregar-rama`, paso 8): en
  a3, las del tramo de precaución de v16 0:30:41–0:31:37; en a8, la línea de 32:56, que toca el
  tramo de cuarentena de 0:32:58;
- **el número del día de diciembre, enmascarado como `[N]` las tres veces que sale** (a4 dos veces
  y el comando 31). Es decisión de la sesión, con el mismo criterio que el consultor fijó para el
  día de julio: diciembre está sin sortear (NA:I).

### Informe del revisor · trabajo/sesion-05 · 2026-10-25

Revisión de HEAD `90a1da5` sobre la base `7eef8cf`: 8 commits y 72 ficheros, con el árbol limpio.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 4 importa, 4 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **Hay ítems nuevos cuya afirmación dice más que su cita (punto 10).** Los dos que más pesan son los primeros: (1) `ev-v15-002441-ec3c910c`. La cita dice «El punto 1 Que allí, solo que Se actualiza del nivel 0 Allí abajo, y ya está», es decir, el 1 se queda y solo cambia el 0; la línea siguiente de la filtrada, `[24:51]`, dice «aquí sigue marcando el mismo nivel». La afirmación dice otra cosa: «en la reentrada en el mismo punto tras un stop, la caja se vuelve a trazar: se actualiza desde el nivel 0, no es la del primer intento». Ni «reentrada tras un stop» ni «no es la del primer intento» están en la cita. (2) `ev-v16-003142-bb737430`. La cita es «¿cuál sería la respuesta del cuarto? a ver voy a decirle que sí, entonces, sí, sí», cuyo referente es «el cuarto». La afirmación dice «el Excel de julio es la exportacion de los tres primeros videos de julio (opcion a de S-25)», y la cita no nombra ni el Excel ni los tres vídeos. Los otros cuatro añaden menos: (3) `ev-v15-003619-60121c7d` añade la condición «y no aparece otro punto de breaker», que está en 36:03–36:14, fuera de la ventana; (4) `ev-v15-010850-e3c57529` añade «no se quita»; (5) `ev-v16-001952-63c96f1f` cambia «no solemos hacer una operación más» por «no hace una operacion mas ese dia» («ese día» no está en la cita, y la línea de la filtrada empieza con «también al día siguiente», que la cita deja fuera); (6) `ev-v16-002841-b47d0461` añade «y no se usa para trazar el punto». Los ítems ya están commiteados, así que se corrigen con un ítem nuevo que los supersede, no editándolos. | Read de los 49 ítems (`knowledge/evidence/v15/`, `v16/`); filtrada de v15, líneas 628-633; filtrada de v16, líneas 277-279 y 483-488 |
| a2 | importa | **El informe afirma más que su cita en dos propuestas, por la misma razón que a1.** (1) S-6 dice «La caja de la reentrada se vuelve a trazar … no es la del primer intento», y lo repite en la cobertura de V y en la tabla final. La cita solo dice que se actualiza el 0. (2) S-25 se da como «RESUELVE, con dudas: (a)» apoyándose en el «sí» de 31:45, que contesta a «la respuesta del cuarto». La respuesta del trader a la pregunta principal está en 30:10–30:20 («creo que sí estaba en orden … yo creería que sí, igual lo puede corroborar el propio bot, creería yo»), es citable (antes de 30:41) y el informe no la usa. | `SESION-05-EXTRACCION.md:515-516, 1165, 1178`; `:1030-1037, 1157, 1200`; filtrada de v16, líneas 457-458 y 483-488 |
| a3 | importa | **El informe cita y describe texto de dentro de un tramo no citable** (v16, 0:30:41–0:31:37): [retirado: dos citas y una descripción de dentro del tramo de precaución de v16 0:30:41–0:31:37]. Además se contradice: el mismo informe dice que ese tramo «no se cita ni se describe más». El motivo del tramo ya cubre lo necesario; esas citas deberían salir. | `SESION-05-EXTRACCION.md:333-340` frente a `:1026-1027`; `tramos_no_citables.yaml` (entrada v16 0:30:41) |
| a4 | importa | **En la filtrada de v16 hay una fecha de diciembre que no se declaró.** La línea `[32:10]` termina en «ahora sí ya lo último el [N] de diciembre». Lo más probable es que el ASR haya oído así «el backtest de diciembre» (la hoja dice «El backtest de diciembre que nos mandaste», `PREGUNTAS.md:816`). La sesión la leyó (cita 32:10), pero la fila de v16 de `HOLDOUT-EXPOSICIONES.md` solo dice «diciembre (pendiente de grabar)». La cuarentena no la tapa porque `meses_libres` cuenta el 12 como libre, aunque `PROJECT_STATE.md:42` (NA:I) dice que el consultor aún no ha decidido si diciembre es de construcción o reservado. Medido: `motivos_cuarentena('el [N] de diciembre')` da `['mes']` sin meses libres y `[]` con {1,4,7,8,10,11,12}. | filtrada de v16, línea 494; `HOLDOUT-EXPOSICIONES.md` (fila de v16, punto 2); `SESION-05-EXTRACCION.md:214`; comando de abajo |
| a5 | menor | El informe remite a `PREGUNTAS.md:83` para «lo preveía para S-23 y S-18». Esa línea está vacía: el texto está en `:88-89` y nombra también S-25. `HOJA-USADA.md:61-62` lo dice bien. | `SESION-05-EXTRACCION.md:58-59` |
| a6 | menor | S-4 cita «[08:56] no», pero en la filtrada esa línea es `[08:57] no` (el ítem trae `t0: 0:08:56`). El literal tiene que llevar la marca de la filtrada. | `SESION-05-EXTRACCION.md:431`; filtrada de v15, línea 356 |
| a7 | menor | `barrido_18_31.py` (la puerta que ordenó el consultor) solo detecta cifras: no pasa el texto por `numeros_a_cifras`, como sí hace `detector_julio.py:38`, así que un «veintiocho» escrito en letra pasaría. En estas dos filtradas no cambia nada: medido, no hay ninguna palabra que empiece por «dieciocho», «diecinueve», «veinte», «veinti» o «treinta». | `anexos/SESION-05/barrido_18_31.py:14,20-25`; Grep (recuento) en las dos filtradas: 0 |
| a8 | menor | En agosto, la línea de 32:56 ([retirado: cita de una línea que toca el tramo de cuarentena de v16 que empieza en 0:32:58]) se atribuye al trader («el trader repite») sin avisar de que la transcripción no separa voces, cuando en el resto del informe sí se avisa. | `SESION-05-EXTRACCION.md:1058-1060`; filtrada de v16, línea 508 |

Comprobado sin hallazgos:
- **El contrato.** `contrato_rama.py` dice «CONTRATO: 72 ficheros dentro del contrato de trabajo/sesion-05 (riesgo medio, artefacto docs/validation/SESION-05-EXTRACCION.md, tramo 'R4', 7 comprobaciones para el revisor)», exit 0. Las comprobaciones que no escriben salen así:
  - `corpus check --hashes`: «OK: el corpus coincide con el manifiesto (hashes)»;
  - `transcript check`: «OK: 17 transcripciones coherentes…»;
  - `frames check`: «OK: 12 extracciones coherentes con el disco; 3 obligatorios presentes»;
  - el diff de los directorios inmutables: `53 A` y nada más.
- **`make check`.** `make-check.log`:
  - línea 102: «SELLO: make check en verde sobre el arbol 95141fff…», que es `HEAD^{tree}`; el último commit está sellado;
  - línea 104: «PICO DE MEMORIA … 297 MiB»;
  - línea 100: `knowledge validate` «OK: 552 items de evidencia, 0 contradicciones abiertas, historial intacto».
- **Tests de los ficheros que toca la rama.** pytest (sin caché) de `test_cuarentena`, `test_inventario`, `test_en_parte_no_se_cierra`, `test_hoja_de_ruta` y las dos de cuarentena de `test_guardia_claude`: exit 0.
- **Lista de ficheros con texto oculto.** `scripts/ficheros_con_ocultos.py` (modo comprobar): «OK: .claude/hooks/ficheros_con_ocultos.txt coincide».
- **CI del último commit.** Run 40256865471 sobre `fix/sesion-05`: solo falla `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, con «PROJECT_STATE declara la rama 'trabajo/sesion-05'; la rama actual es 'fix/sesion-05'». Resultado: `1 failed, 2871 passed, 46 skipped`.
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`, así que no aplica.
- **Holdout y regímenes.** Nada en `knowledge/cases/holdout`, `knowledge/feedback`, `libros.yaml`, `vistos.yaml`, `docs/adr`, `scripts/` ni `.claude/` (0 ficheros). `HISTORIA.md` solo crece (0 líneas quitadas). `HOLDOUT-EXPOSICIONES.md` solo gana cuatro filas.
- **Ambigüedades, ADR y sitios con `cita` en la spec.** No hay cambios.
- **Ventanas de los 49 ítems frente a los 11 tramos nuevos.** Ninguna solapa. El caso límite es `ev-v16-001952` (t1 0:20:02 frente al tramo que empieza en 0:20:02): `verificacion.py:358-408` usa intervalos semiabiertos y comprueba también los segmentos, y lo acepta.
- **El día de julio y las cifras.** En el diff y en los mensajes de commit, con los enteros del 18 al 31 enmascarados, solo aparecen los usos conocidos (códigos S-18 y S-25, fechas de octubre, los rangos «18 al 31» y «20-31»). Ninguna línea con «hasta el [N]» fuera de la ya enmascarada de §2.7.
- **Ningún número de teléfono** en las líneas añadidas.
- **Afirmaciones medidas.** `motivos_cuarentena('hoy 25 del 10')` da `['fecha numerica']` y `('hoy, 25 del 10,')` da `[]`, como dice §2.7. `feedback/modelo.py:113`, `:247-248` y `:293-307` dicen lo que cita §0.4.
- **Citas del informe comprobadas contra la filtrada:** S-3 (04:47, 05:30, 05:53), S-4 (08:57–09:36, 15:20–15:52), S-7 (36:19), S-12a (60:31, 61:04–61:20, 61:59), S-21 (19:52), S-25 (29:20–29:32, 31:42–32:04) y «Para cerrar» (32:28–32:55). Salvo lo señalado en a1, a2, a6 y a8, coinciden.

#### Eje (b) · Encargo
Resumen: 0 bloquea, 4 importa, 0 menor. Requisitos: 34 hechos, 1 parcial, 0 no hechos (uno, la frase final, queda pendiente hasta después del revisor; uno, hecho de otra forma y declarado).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con `abrir-rama`: encargo, contrato y archivo en HISTORIA | Hecho | `c6d7cef`; `HISTORIA.md` «# Archivo 46» |
| 2 | Comprobar la base (main, tag, CI, ramas, hoja 05, regla del 2026-10-21) | Hecho | informe:15-32 |
| 3 | Copiar el encargo tal cual, con Write y la fecha | Hecho (sin el original no se puede comparar) | `docs/encargos/trabajo-sesion-05.md` |
| 4 | Duraciones exactas con ffprobe | Hecho | informe:85 |
| 5 | v15/v16 son los siguientes ids libres, con `drive_id` null y en `SESIONES_EN_CUARENTENA` | Hecho | `fuentes.yaml` (diff); `cuarentena.py:51` |
| 6 | Medir si se admiten dos vídeos por id de sesión, con el precedente | Hecho | informe §0.4 |
| 7 | Buscar el código de S-17 en las dos filtradas | Hecho | informe:870-872 |
| 8 | Nota de feedback de v16: `fecha` 2026-10-23 y `recibido_el` 2026-10-25, con la línea verificada | Hecho | informe:100-105, 1247-1248; `modelo.py:113` |
| 9 | No resolver nada; no tocar `transcribir_sesion.py` | Hecho | diff de las rutas protegidas: 0 ficheros |
| 10 | Negativas de la guardia: PARADA o la forma que propone, declarada | Hecho | informe §7 |
| 11 | Los dos días con `casos_ocultos`, y la desviación del 25 declarada | Hecho | informe:66-73; fila de HOLDOUT |
| 12 | Preguntas a) a d) antes del registro, y sus respuestas | Hecho | informe §0.1 |
| 13 | Declarar cada consulta de casos y cada lectura de filtrada en HOLDOUT | Hecho, con la salvedad de a4 | cuatro filas del 2026-10-25 |
| 14 | `HOJA-USADA.md`: tabla, orden, no hechas, recuadros, esquemas, «Para cerrar», dos días; sin citas del trader | Hecho | `docs/sesion-5/HOJA-USADA.md` |
| 15 | Recuadro en `PREGUNTAS.md` | Hecho | `PREGUNTAS.md:39-43` |
| 16 | Verificar que los recuadros son S-7, S-12, S-13 y S-15 | Hecho | `HOJA-USADA.md:64-82` |
| 17 | Filtradas con el guion de main y `--sesion 05`; el registro dice la hoja; «veinte y N» en el bloque de S-20 | Hecho | informe:197-208, 276-286, 868-871; Grep «veinte»: 0 |
| 18 | Registro: `naturaleza` del vídeo entero, `test_inventario`, `inventory`, `check --hashes` | Hecho | informe §1, §1.2 |
| 19 | Test roto a propósito y después pasando, con sus salidas | Hecho | informe §1.1, 172 |
| 20 | Audio con las formas de la skill y WAV con nombres distintos fuera del repo | Hecho (las formas exactas, no verificables) | informe §2.1, :88 |
| 21 | Antes de la segunda transcripción, comprobar que los ficheros de v15 siguen ahí | **Parcial** | no está en el informe (Grep: 0); el resultado sí se ve: `ls` de la carpeta de audio, v15 a las 16:21 y v16 a las 17:27, con nombres distintos |
| 22 | Corte SIN AUDIO en tramos, y la puerta del ASR | Hecho | tramos (v15 1:22:26); informe:226-229 |
| 23 | Transcripción con el «listo» de Aleks; bloques en cuarentena en commit propio por vídeo | Hecho (v16 tarde, declarado en §7.7) | `5f47908` |
| 24 | `frames extract` y `frames check` de los dos | Hecho | informe §2.4 |
| 25 | Verificación final: solo `A` en los directorios inmutables | Hecho | `53 A` |
| 26 | Informe con la forma de SESION-04 y la tabla final con sus columnas | Hecho | informe §5 |
| 27 | Por código: tramo, literal, propuesta, regla general, «creo», compra y venta | Hecho, con la salvedad de a2 | informe §3 |
| 28 | Orden: S-3 y S-4 con `ACTIVAR-A35-A44`, después S-5 y S-6, después el resto | Hecho | informe §3.1-§3.3 |
| 29 | S-12 en dos filas | Hecho | informe:679-717 |
| 30 | S-1 y S-2 frente a ADR-0080 y la sesión 1 | Hecho | informe:541-569 |
| 31 | «Para cerrar»: diciembre, agosto y marzo | Hecho | informe §3.5 |
| 32 | Evidencia fuera de los tramos; `contradictions` y `validate` en verde | Hecho | `make-check.log:100` |
| 33 | Cobertura de V y qué pasa con H tras S-24 | Hecho | informe §4.2, §4.3 |
| 34 | Lista de copia A.4; `PROJECT_STATE` por debajo de 25.000 | Hecho | informe §8.1; `git show HEAD:PROJECT_STATE.md \| wc -c` = 23796 |
| 35 | Cierre: sello, push a `fix/`, CI con solo el fallo esperado, número de run, sin cierre en HISTORIA | Hecho | informe §9; run 40256865471 (arriba) |
| 36 | Ampliación de marzo: `fuentes.yaml`, inventario, literal y contexto, HOLDOUT, A.3 y heredado 2 preparados, lo que queda del paso 0 | Hecho | diff de `fuentes.yaml`; informe §3.5, §6 |
| 37 | Ampliación: no tocar `vistos.yaml` ni la hoja de ruta | Hecho de otra forma, y declarado | `vistos.yaml` sin tocar; `HOJA-DE-RUTA.md` solo `ID:A-48`, con la respuesta del consultor (§7.1) y el comentario del contrato (`contrato.yaml:29`) |
| 38 | «Rama lista para revisión, NO cerrada» | Pendiente: se pone después del revisor | informe:1459 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Falta la tabla «El encargo, punto por punto»** que pide la skill `entregar-rama` (E5 de `trabajo/entorno-code`). Las dos secciones «Cómo se aplicó, punto por punto» solo cubren las respuestas del consultor. | `.claude/skills/entregar-rama/SKILL.md:46-50, 97`; Grep «punto por punto» en el informe: solo líneas 364 y 1310 |
| b2 | importa | **Las respuestas del consultor a las dos PARADAS** (la de v16 y la del `make check`) **no están al final del encargo**, solo en el informe. El encargo termina en la ampliación de marzo. | `fase-cero/SKILL.md:90`; `entregar-rama/SKILL.md:18`; `docs/encargos/trabajo-sesion-05.md:74-97` |
| b3 | importa | **No consta la comprobación que pide el encargo antes de la segunda transcripción** (que los ficheros de v15 siguen ahí). El resultado es bueno, pero el informe no dice que se hizo. | encargo:52; informe §2.5 (sin mención) |
| b4 | importa | **Hay algo de más que el encargo no pide y el informe no justifica:** la medida del `mtime` de v16 frente a la hora del WhatsApp (`stat` del vídeo), y el punto 16 de §4.1 que sale de ella. El encargo pide «solo lo que dijo, sin decidir nada». | informe:1076-1079, 1122-1123 |
| b5 | menor | La lista A.4 tenía que ir «al final del informe» y está en §8.1, con §9 y «Estado» detrás. Además, «Estado» sigue en «EN CURSO», y `entregar-rama` pide quitarlo. | encargo:66; informe:1392, 1459; `entregar-rama/SKILL.md:56` |

#### Lo que no pude comprobar
- **`uv run botsito evidence contradictions`:** la guardia de solo lectura lo niega («ese subcomando u opcion de `botsito` escribe»). Lo sustituye `make-check.log:100` («0 contradicciones abiertas»).
- **`knowledge validate > knowledge-validate.log` y `make check`:** escriben, así que no los ejecuté. Los sustituyen `make-check.log:100-104` y que el sello sea igual a `HEAD^{tree}` (95141fff…). `knowledge-validate.log` no existe.
- **Que el día de julio y las cifras de los tramos de precaución no estén en el diff:** no se puede comprobar del todo sin conocer el número ni las cifras, y no los leí. Solo hice búsquedas con los números enmascarados (ver eje a).
- **Sin registro con el que comprobarlas:** las formas exactas de ffprobe y ffmpeg, el «listo» de Aleks antes de cada transcripción, que no corrió ningún `make check` en la ventana prohibida, que no se abrió ningún fotograma, y que el encargo se copió tal cual.
- **Mi propia lectura de las filtradas (fuera del repo), que hay que declarar hoy en `HOLDOUT-EXPOSICIONES.md`:**
  - el barrido ancho de las dos, como manda el consultor; enseñó enmascaradas [59:22] (dentro del tramo personal de v15) y [31:04] (dentro del tramo de precaución de v16);
  - de las dos, listados de solo marcas de tiempo, y un recuento de números escritos en letra (0);
  - de v16, las líneas 274-279 (19:21-19:57), 427-459 (29:02-30:29) y 482-508 (31:40-32:56); la de 32:56 toca el tramo de cuarentena que empieza en 0:32:58;
  - de v15, las líneas 88-127 (04:47-07:30), 339-381 (07:40-09:51), 466-497 (15:01-15:59), 619-637 (23:25-24:59), 771-797 (35:09-36:56) y 1108-1124 (60:03-61:59).
  - Nada entre 30:41 y 31:37 de v16, ninguna cruda, ningún fotograma y ninguna captura.
- **Una consulta de CI de más:** además del `gh run view 40256865471` suelto, hice una consulta suelta con `--log-failed` (filtrada con grep) para saber qué test fallaba. Es una desviación de «un único gh run view».
- **Bloqueo de la guardia:** negó un `python -c` que recorría `knowledge/evidence/*` para cruzar ventanas con tramos. Lo hice con Grep de `t0`/`t1` y comparándolos a mano.

#### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read de `docs/encargos/trabajo-sesion-05.md` y de `contrato.yaml`
3. `uv run python scripts/contrato_rama.py`
4. `uv run botsito corpus check --hashes`; `uv run botsito corpus transcript check`; `uv run botsito corpus frames check`
5. `uv run botsito evidence contradictions` (negado por la guardia de solo lectura)
6. `git diff --name-status main...HEAD -- knowledge/evidence knowledge/corpus/transcripciones knowledge/corpus/fotogramas data/manifests | awk | sort | uniq -c`
7. `ls -la make-check.log knowledge-validate.log`; grep de `SELLO`, `PICO` y `passed` en `make-check.log`
8. `git diff --name-status` de las rutas protegidas y reguladas, y de todo lo que no es `A`
9. `git rev-parse HEAD^{tree} 0f173b3^{tree}`; `cat .git/botsito-sello`
10. `git diff main...HEAD` de `PROJECT_STATE.md`, `HOJA-DE-RUTA.md`, `PREGUNTAS.md`, `HOLDOUT-EXPOSICIONES.md`, `cuarentena.py`, `tests/`, `tramos_no_citables.yaml` y `fuentes.yaml`
11. Read y grep de `docs/adr/0021-que-cuenta-como-abrir-un-holdout.md`
12. Read entero de `docs/validation/SESION-05-EXTRACCION.md`
13. `cat` de los 49 ítems de evidencia; grep de `revisado_por` en v10
14. `uv run python -c …` que recorría la evidencia (negado por la guardia); Grep de `^t[01]:` en v15 y v16
15. Read de `src/botsito/evidence/verificacion.py:345-424`
16. Read de los dos guiones del anexo; `uv run python docs/validation/anexos/SESION-05/barrido_18_31.py` sobre la filtrada de v16 y sobre la de v15
17. Grep de `diciembre` en `PREGUNTAS.md`; grep de `meses_libres`; Read de `cases/holdout.py:548-657`; Read de `PREGUNTAS.md:805-834`; grep de `diciembre` en `guardia.py` y en `PROJECT_STATE.md`
18. `git diff main...HEAD … | grep … | sed` (dos búsquedas enmascaradas de los enteros 18-31) y el mismo enmascarado sobre `git log --format=%B`
19. `git diff … HISTORIA.md | grep -c`; `wc -c PROJECT_STATE.md` en `main` y en HEAD; `git log` de las rutas protegidas
20. `gh run view 40256865471`; `gh run view 40256865471 --log-failed | grep … | cut | head`
21. Grep de marcas de tiempo (solo con `-o`) y Read por tramos de las dos filtradas (líneas listadas arriba); Grep (recuento) de números en letra
22. Read de `docs/sesion-5/HOJA-USADA.md`; Read y Grep de `PREGUNTAS.md` (recuadros y WhatsApp)
23. Grep de `siguen ah…` en el informe; `sed -n` de `src/botsito/feedback/modelo.py`; `ls -la` de `C:/Users/USER/Desktop/sesion-05-audio/`
24. grep de las tres citas de v10; grep de `SESGO-H4-COLOR.md` y de `ACTIVAR-SESION-04.md`; Read de `SESGO-H4-COLOR.md:929-948`
25. Grep y Read de `docs/runbooks/ACTIVAR-A35-A44.md`
26. `git log --format='--- %h%n%B' main..HEAD`
27. `git diff --name-only` de las rutas protegidas; `git log` de `contrato.yaml`
28. `sed` de `scripts/ficheros_con_ocultos.py`; `uv run python scripts/ficheros_con_ocultos.py` (modo comprobar)
29. `uv run pytest -p no:cacheprovider` de los cinco ficheros de test (exit 0)
30. grep de `knowledge validate` en el `Makefile` y en `make-check.log`
31. `uv run python -c` con `motivos_cuarentena` (las dos fechas sintéticas, y «el [N] de diciembre» con y sin meses libres)
32. Read de `.claude/skills/entregar-rama/SKILL.md` y de `fase-cero/SKILL.md:80-109`; Grep de «punto por punto» en los informes de las sesiones 4 y 5
33. grep de «confirmacion escrita» en `CLAUDE.md`, `ENTRADA-MARZO.md`, `HOJA-DE-RUTA.md` y `PROJECT_STATE.md`
34. Grep de números con forma de teléfono en las líneas añadidas
