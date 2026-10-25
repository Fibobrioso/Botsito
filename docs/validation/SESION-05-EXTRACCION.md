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

## Estado

EN CURSO.
