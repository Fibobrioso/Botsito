# Sesión 5 con el trader (v15 y v16): la extracción por pregunta

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final (§5) entra con la extracción.

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
  «Para cerrar». Nada quedó para WhatsApp ni para la sesión 6, aunque `PREGUNTAS.md:83` lo preveía
  para S-23 y S-18. El código de S-17 se busca igual en las dos filtradas, como pide el encargo.
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
- **Dónde y qué.** v16, línea `[31:04]`, dentro de S-25. Enmascarada: «el backtest hasta el [N],».
  El trader enseña su replay de julio («[30:41] … voy a mostrar yo hice el bates hasta el final») y
  dice hasta qué día llegó: el final del rango del mes. Ninguna operación, ningún resultado y ningún
  detalle de ese día.
- **Por qué no la paró el detector antes de leer.** `detector_julio.py` solo marcaba un número junto
  a «julio» o «día» en la misma línea o en la contigua. Esta línea no tiene ninguna de las dos
  palabras, y «julio» sale seis líneas más abajo (31:20). El detector no la marcó, se leyó la
  filtrada entera y se vio al leerla.
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

## Estado

EN CURSO.
