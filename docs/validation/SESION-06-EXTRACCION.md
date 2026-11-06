# Sesión 6 con el trader (v17): la extracción por pregunta

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

Las mismas tres pruebas pasan. La salida de `pytest -rA` de `test_cuarentena.py` y las dos de
`test_guardia_claude.py` (de sus 42 líneas `PASSED` y 0 `FAILED`/`ERROR`, las de las tres que fallaban):

```
PASSED tests/unit/test_cuarentena.py::test_la_lista_cuadra_con_fuentes
PASSED tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena
PASSED tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo
```

Con `test_inventario.py`, **55 `PASSED`** y 0 `FAILED`/`ERROR`.

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

**Lo que enseñó el trader.** Compartió su pantalla (respuesta de Aleks; cuánto rato, no se ha medido:
no se abre ningún fotograma): dibuja sobre los esquemas de la hoja («vamos a abrir el paint», 05:25) y
va a su gráfico de FX Replay para explicar. Lo dice él:
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

**Un tramo de precaución por el mes: 0:06:52–0:08:04** (en `tramos_no_citables.yaml`; marcado tras el
revisor, b7). Ahí abre el replay de un mes que no es de los libres de la respuesta a), y nombra un trade
de ese mes, sin ningún día ni cifra. La respuesta a) manda declararlo no citable, y ninguna cita de la
rama cae dentro. Aquí solo se dice dónde está.

**Tramos ajenos a la operativa**, no citables y sin describir: 1:35:11–1:35:30 y 1:44:19–1:44:30.

### 2.5 Fotogramas: ninguno abierto

Decisión de la sesión, con el precedente de la sesión 5 (§0.1): `frames extract` y `frames check` sí
se hacen (paso 5 de la skill) y las citas salen solo de la filtrada.
- `uv run botsito corpus frames extract --video v17` → `OK: fr-v17-db232fc6 (7200 fotogramas, 0
  extra)`; `uv run botsito corpus frames check` → `OK: 13 extracciones coherentes con el disco; 3
  obligatorios presentes`.

## 3. Por pregunta

**Cómo se leen las filas.** «S-n» es siempre el código de la SESIÓN 6. Cada código lleva su tramo
(mm:ss, minutos totales desde el inicio del audio de v17), el literal de la FILTRADA y la propuesta:
resuelve / resuelve en parte / no resuelve. La transcripción no separa voces: la pregunta la lee en voz
alta el propio trader o Aleks, y a menudo la misma línea mezcla la lectura con la respuesta; el
hablante se atribuye por contexto y, donde una línea mezcla, se dice. Las citas se copian sin corregir
el ASR («break up» por «break even», «Vaya Salsista» por «bias alcista»).

**Cómo se agrupó la filtrada.** El guion agrupa por el primer código que detecta, y solo detectó siete.
Bajo `## S-2` van S-2, S-3, S-4 y S-5 (02:25–30:27). Bajo `## S-5` van S-6 y S-7 y S-8 (30:45–50:04),
porque el ASR oyó «La pregunta S5» a las 30:45 donde se decía S-6; bajo `## S-6`, solo sus primeras
líneas, 30:28–30:44. Bajo `## S-13`, S-13 y S-14. Bajo `## S-15`, S-15 y S-16. Bajo `## S-17`, de S-17
hasta el final. **No hay bloque `## S-20`, y ningún código salió como «veinte y N»** (encargo, «La hoja
que se llevó», punto 2): S-20 a S-23 se oyen como «S20 abierta», «S21», «Ese 21» y «Pregúntese 22» y
«23», y se localizaron a mano, como todos los demás, por los códigos dichos en voz.

### 3.1 Las dos bloqueantes

#### S-1 · La pérdida del día: solo con las cerradas o también con la abierta · A-44

- **Tramo:** 00:00–02:23.
- **La respuesta:** «[02:18] Pues en este caso sería solo cerradas» / «[02:20] Solo las operaciones
  cerradas». Antes, en una línea que mezcla la lectura: «[01:01] … esto la respuesta es la sólo»
  / «[01:07] con las cerradas …».
- **Para precisar** (si cierra o la deja seguir cuando la abierta toca ese punto): «[01:34] cerramos» /
  «[01:35] nosotros, por lo general» / «[01:36] si toca ya el stop loss» … «[01:52] Si el trade se
  pierde o se gana, si se pierde automáticamente y llega al 4.5, tendríamos que en cierta parte parar
  ese día y continuar al siguiente.»
- **Propuesta: RESUELVE.** Es la opción (a). `ACTIVAR-A35-A44.md` §1 la lee como «la pérdida es sobre
  lo cerrado» → `perdida_trader_magnitud: saldo`, que es lo que hace hoy el bot como
  DEFAULT_AMBIGUOUS bajo A-44, lectura del consultor. **Cae en una lectura documentada: sin PARADA.**
  La segunda subpregunta (en cada momento o al cierre de la vela) queda sin objeto con esta
  respuesta.
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** no aplica.

#### S-2 · Cuándo vuelves a contar desde cero · A-44

- **Tramo:** 02:25–04:38. Dentro van dos bloques en cuarentena (§2.2), que no se leen.
- **La respuesta:** «[02:50] … La respuesta es la C, la primera sesión del día siguiente, ya que de esa
  manera pues» / «[02:57] nosotros, o sea, cada día por lo general estamos trabajando dos sesiones que
  están planteadas,» / «[03:03] entonces si en esas dos sesiones se llega al 4.5 obviamente se detiene,
  pero al día siguiente a la» / «[03:09] primera sesión nuevamente después seguimos operando.»
- **Para precisar, «tu hora»:** «[03:21] la del proveedor de datos que sería try and view o broker
  también podría ser se maneja en base a» / «[03:29] eso UTC más 2 si no me equivoco es lo que se suele
  manejar a ver para confirmar si UTC más 2 ahora» / «[03:37] ahora Madrid.» El reloj de sus gráficos
  está medido (Europe/Madrid con cambio de hora, ADR-0069): UTC+2 fijo no lo es.
- **Para precisar, el viernes:** «[03:53] se vuelve a contar desde cero el día lunes.» / «[03:56]
  Exactamente, o sea, siempre es de sesión» / «[03:57] en sesión, …».
- **La confirmación final** no se completa: «[04:36] este planteamiento está» / «[04:37] mal, creo que»
  … y pasa a la siguiente.
- **Propuesta: RESUELVE EN PARTE, y es PARADA de §4.** La opción es la (c), al abrir la primera sesión
  del día siguiente. **No cae en ninguna lectura documentada**: `perdida_trader_reinicio_huso` es un
  nombre IANA de huso, y la tabla de `ACTIVAR-A35-A44.md` §1 dice «si no es una medianoche, PARAR, §4».
  `PREGUNTAS.md` ya lo preveía: «(c) no cabe en ese parámetro: si la elige, la activación necesita otro
  parámetro con su ADR». **Decide el consultor.**
- **Regla general:** sí. **«creo»:** no en la regla; «si no me equivoco» en el reloj. **Compra y
  venta:** no aplica.

#### S-3 · La mecha que mueve tu alto de M15, y la vela que lo toma después · A-35

- **Tramo:** 04:38–19:32. Dentro van dos bloques en cuarentena (0:07:13–0:07:24 y 0:07:33–0:07:39).
  Responde dibujando en el esquema y sobre su gráfico (§2.4).
- **La pregunta principal** (qué mecha mueve el alto: la de la contraria o también una posterior):
  «[13:19] bueno es que si vuelve al alto eso es indiferente tiene que cerrar con cuerpo» / «[13:24] o
  sea tiene que cerrar con cuerpo por encima de la zona lineal de m15». **No elige.** Sobre su gráfico
  sí dice que la zona se actualiza con otra vela verde de M15: «[10:36] suponiendo que esto te deja
  otra vela verde entonces actualizas tu zona lineal de m15 aquí». Y de un rompimiento con mecha:
  «[15:43] Simplemente no podemos validar nosotros esta entrada, o sea, tiene que haber un rompimiento
  con cuerpo para poder validar».
- **El primer «Para precisar»** (la mecha sube el alto; una M1 cierra con cuerpo por encima del alto de
  antes y por debajo de la mecha; ¿ha tomado?): «[16:10] sí, sí claramente» / «[16:13] o sea, si está
  conforme al bias» y «[17:12] Entonces, ¿si cerró con cuerpo por encima del alto de antes?» / «[17:16]
  La respuesta es sí, cerró con cuerpo por encima del alto de antes.» Es la **(a)**, con esa condición
  del bias. Que la vela quede por debajo de la mecha está en el enunciado de la hoja, no en su frase.
- **El bajo:** «[18:47] es todo igual pero al revés».
- **La confirmación final**, a medias: «[18:50] la mecha que mueve mi alto es la» / «[18:52] de» /
  «[18:54] o sea, de M1» … «[19:09] La vela que lo toma tiene que cerrar con cuerpo por encima de el
  alto o el bajo de M15.»
- **Propuesta: RESUELVE EN PARTE, y es PARADA de §4 por la pregunta principal, porque no elige.** Frente a
  las tres lecturas de `liquidez_m15_mecha_que_vuelve` (hoy `cualquier_mecha`, lectura del consultor):
  - `cualquier_mecha`: la (a) es difícil de casar con ella, porque esa vela no tomaría;
  - `no_mueve`: «es indiferente», la (a) y que la zona se actualice solo con otra vela (10:36) **pueden
    leerse hacia ahí**, y no lo dice; `PREGUNTAS.md` la reserva para «la mecha no mueve nada»;
  - `solo_la_contraria`: no la nombra. La única frase que rellena el blanco de la confirmación es «de M1»
    (18:54), que no es ninguna de las opciones y no se entiende sola.
  No se fuerza ninguna. **Y la (a) contradice lo que hace hoy el bot**: `PREGUNTAS.md`, S-3, dice que con (a)
  la decisión de ADR-0084 «no se sostiene y hace falta ADR». **Decide el consultor.**
- **Frente a la sesión 5:** allí dijo «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`), y ahora
  que si vuelve es indiferente.
- **Regla general:** sí en la toma con cuerpo; no en qué mecha mueve. **«creo»:** no. **Compra y
  venta:** sí (18:47).

**Por separado, «el nivel se congela al tomarse» (ADR-0084:41-48, decisión del consultor).** A la
pregunta «¿una vez una vela de M1 cierra con cuerpo por encima y toma tu alto, una mecha que venga
después lo vuelve a mover?»: «[17:28] No, no, eso ya nos es indiferente.» / «[17:32] La vela que genere
el rompimiento o la toma de liquidez de M15» / «[17:36] Tiene que hacerlo con cuerpo» / «[17:38] Las velas
que vengan después, no sé si es indiferente» / «[17:41] Si luego hace una mecha o demás». **Propuesta:
RESUELVE EN PARTE:** contesta «no» y «ya nos es indiferente», que va hacia lo que decidió el consultor (tras
la toma una mecha no mueve el nivel), y añade ese «no sé si», que se oye más veces en la sesión y aquí no
se puede tener por una duda ni por una muletilla. La otra mitad de la decisión (la M1 que cierra con
cuerpo sobre el nivel ORIGINAL ya no es toma si una mecha anterior lo movió) es la que contradice la (a)
de arriba. **El bajo en espejo** (ADR-0084:49-50): 18:47. **Regla general:** en parte. **«creo»:** no, con
ese «no sé si». **Compra y venta:** sí.

#### S-4 · En M15, una vela sin cuerpo entre las verdes y la roja · A-35

- **Tramo:** 19:33–23:58.
- **La respuesta:** corrige el esquema («[21:07] Vale, aquí este ejemplo está mal planteado porque la
  zona lineal se tendría que marcar desde aquí.») y contesta: «[21:55] … vale en este caso sería la
  respuesta c y la vela roja nos» / «[22:02] permitiría a nosotros si anterior a esta tenemos una vela
  neutra puedes plantear el máximo por» / «[22:09] encima de la mecha de la vela neutra …».
- **Para precisar, si el alto puede ser la mecha:** «[22:50] entonces como hemos mencionado con
  anterioridad la respuesta sería puede ser la mecha de la vela» / «[22:55] sin cuerpo y si son dos o
  tres velas sin cuerpo seguidas pues se va a la mecha …». **El bajo:** «[22:17] venimos de un orden flow
  bajista o sea vela roja vela roja en m15 tenemos una vela neutra pero» / «[22:24] pero luego tenemos
  una vela verde, entonces nosotros trazaríamos desde la mecha más baja.»
- **Propuesta: RESUELVE.** Marca (c). La conclusión de este informe, que él no dice con esa palabra: la
  vela sin cuerpo no corta la racha, y el alto es el punto más alto, también su mecha. **Va contra el
  bot**: hoy M15 usa `corta_la_racha`, que es la
  (b). **No hay parámetro**, y `no_cuenta` (lo que `PREGUNTAS.md` prevé para (a), con su ADR) no dice
  que la mecha de esa vela sirva de alto. **Decide el consultor, con ADR.**
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí.

### 3.2 S-18 · Las reentradas en el mismo punto · ADR-0083 (PROVISIONAL)

- **Tramo:** 87:42–100:24, con un tramo ajeno a la operativa dentro (§2.4).
- **Tras un stop:** «[99:39] … entonces tras un stop en un punto vuelvo a entrar en él o sea en el
  posible» / «[99:50] punto breaker o sea las veces que las veces que sean necesarias pero el punto
  breaker tiene que» / «[99:56] ser avaliado como lo hemos estado mencionando …». Marca «otra»: «[90:26]
  … la respuesta sería otra» / «[90:35] cual». Y lo matiza: «[90:09] … tiene que haber un igual para
  poder repetir entre comillas» / «[90:15] esa misma entrada pero por lo general o sea si hay un error
  flow normal y demás o bien se gane» / «[90:21] se pierde y no se vuelve a repetir el mismo punto
  porque el precio va a ir desarrollando».
- **Tras un break even:** «[98:06] Entonces tras un breaker en ese punto» / «[98:08] vuelves a entrar
  en él la respuesta era sí o sea si cumple los criterios que hemos estado» / «[98:15] mencionando …»
  («breaker» es el ASR: lo que se lee es la subpregunta del break even).
- **El 0 y el 1 al volver a entrar:** «[98:15] … si al volver a entrar que haces en el 0 y con el 1 de
  la caja como digo o sea nuevamente» / «[98:21] lo repito vamos a estar en constante actualización».
  La confirmación final no la completa: «[100:04] … no sé cómo» / «[100:12] ¿Cómo podría complementarlo
  allí?» / «[100:16] Tampoco.»
- **Corrige, con dudas, lo que se le lee de la sesión 5:** la duda de quitar la condición cuando hay break
  even (`ev-v15-002029-1ac081ae`): «[89:17] a lo mejor me habré» / «[89:20] equivocado y no quise decir
  breakeven» / «[89:21] eran los equals, o sea los equals» / «[89:23] más que nada cuando hay equals» /
  «[89:25] o sea, eso quería replantearme» / «[89:28] pero los break-evens, que raro» / «[89:31] no, eso» /
  «[89:32] bueno, lo he dicho, sí, pero» / «[89:33] a lo mejor me habré confundido». Y sigue pendiente de
  medir: «[88:31] pero por ahora todavía lo trabajamos» / «[88:34] tendría que ser un backtest como digo» /
  «[88:35] de los peores meses más que nada».
- **¿Da la regla que D1 necesita?** D1 pide cuántas veces reentra, si la caja es la del primer intento
  o una nueva y qué hace tras un break even (recuadro del 2026-10-26 de ADR-0083).
  - **Reentra tras un stop y tras un break even, si el punto se vuelve a validar**, y a la vez dice que el
    mismo punto casi no se repite: «[90:03] … o sea es muy difícil o sea tendría que condicionarse todo el
    escenario …», hace falta «un igual», y con un flujo normal «no se vuelve a repetir». **Las dos cosas se
    confrontan con D1 así:** que se pueda volver si el punto se valida casa con D1 (el llenado no gasta el
    punto; la reentrada por la vía normal, D5); pero D1 deja volver a colocar el punto, con la misma caja
    o con otra, sin pedir un igual, y si esa condición limita D1 no lo contesta. Lo mira el consultor.
  - **El número:** «las veces que sean necesarias», sin tope; `cartuchos_max` = 3 por liquidez sigue
    delante, y la frase de los 3 intentos solo se lee en voz (87:44), sin que la comente.
  - **La caja:** «constante actualización». Si es la del primer intento o una nueva, no lo dice.
  - **Propuesta: RESUELVE EN PARTE.** Da la regla de fondo, y no la da entera. **ADR-0083 sigue
    PROVISIONAL**; si se confirma lo decide el consultor.
- **Regla general:** sí, condicionada a validar el punto. **«creo»:** no. **Compra y venta:** no lo
  distingue.

### 3.3 S-7 a S-12 · Los gráficos

**Sin ningún día ni fecha**: la clave gráfico → día vive solo en `clave.txt`, fuera del repo, y esta
rama no la abre. Cómo se enseñaron, y qué preguntó el trader por la fecha, §2.4.

#### S-7 · Gráfico 1

- **Tramo:** 34:08–46:49. Limpio y marcado (respuesta de Aleks, §0.1).
- **Qué decidió: no operaría, por la opción (a)**: «[43:38] … la primera sesión que es más claro está ahí
  pues no hubo toma justamente aquí lo suelta la respuesta» / «[43:46] no hubo toma de liquidez de m15 es
  por ello que no se entró …»; «[46:21] … en el gráfico 1 entre porque» / «[46:30] pues no hubo toma de
  liquidez de m15».
- **Si coincide con la línea del marcado:** no lo dice. No se pronuncia sobre el nivel de la línea, y
  no dice dónde pondría su orden, porque no entra.
- **Lo que lee sobre el gráfico:** «[37:59] definimos que el bias es alcista o sea alcista tanto para de las 7
  a 11 y de» / «[38:05] las 11 a 3 es alcista …»; marca liquidez de M15 («[38:31] aquí un trazo aquí otro
  trazo …», sin que la filtrada diga dónde) y concluye que no hay entrada: «[38:51] aquí el precio pues en
  ningún momento nos permite a nosotros poder entrar …».
- **Sus reservas:** no ve claro M15 en el gráfico («[39:49] … aquí está definido muy bien, o sea, la zona
  lineal de M15, pero aquí no se puede definir muy bien …») y, para explicarlo, va a su gráfico de julio
  y escoge otra sesión (40:11–41:23), con lo que lo que dice en 41:23–43:15 es de esa sesión, no del
  gráfico 1. De la sesión de las 11 del gráfico 1 solo supone: «[44:07] … y después el de las 11 el de las
  11 pues en m1 pues» / «[44:19] posiblemente también ha habido break events y eso no algún los pero no no
  me dice en qué sesión …».
- **«¿Qué habrías esperado ver?»:** lo de siempre (44:38–44:48). **«¿Dónde marcarías tu liquidez?»:** en esa
  respuesta no da un nivel, y da una sugerencia para el bot (§3.6); los trazos de antes, arriba.
- **Propuesta: RESUELVE EN PARTE:** (a) para la primera sesión del gráfico, sobre un M15 que dice no ver
  claro.
- **Regla general:** no, un ejemplo. **«creo»:** en la sesión de las 11 («no creo que», 44:07, y
  «posiblemente»). **Compra y venta:** no aplica.

#### S-8 · Gráfico 2

- **Tramo:** 46:49–50:04. Limpio y marcado (respuesta de Aleks, §0.1).
- **Qué decidió: nada.** Describe lo que ve y se pierde: «[48:25] … quiero creer que aquí me tengo un poco
  me tiene un poco liado». Y: «[49:10] O sea, el bot ha hecho, suponiendo que ha hecho esta entrada así»
  / «[49:14] Pero no me dice los criterios por qué» / «[49:17] O sea, no veo los trazos de M15 y todo
  eso». Pide la fecha (§2.4). Acuerdan parar: «[49:46] … un gráfico cerrado a medias, ¿no? Y los otros
  como que queden para poder trabajarlos de nuevo …».
- **Propuesta: NO RESUELVE.** **Regla general:** no. **«creo»:** sí, sobre lo que ve. **Compra y venta:**
  no aplica.

#### S-9 a S-12 · Gráficos 3 a 6

**No se hicieron** (49:20–50:04; al final, «[119:46] porque han quedado seis preguntas al aire»). **Lo
que pide el trader para retomarlos:** la fecha, los criterios del bot y los trazos de M15. Lo de la fecha
va al consultor (§4.1). Más contexto lo pide también para los esquemas, dentro de S-18 (§3.6).

### 3.4 El resto, en el orden de la hoja

#### S-5 · Después de la toma, un retroceso con alternancia y un punto nuevo limpio

- **Tramo:** 23:58–30:27.
- **Sobre el esquema:** «[25:16] Es que aquí no habría entradas» / «[25:18] En estos retrocesos» /
  «[25:19] no habría entradas». Luego, sobre su gráfico: «[28:03] … este nivel para poder trazar todos
  puntos breakers pero aquí lo que haga» / «[28:07] después a nosotros no nos interesa, por eso puede ser
  muy ruidoso». **Y no acepta la premisa:** «[29:54] si el primer retroceso, bueno, no existe como tal una
  alternancia, aunque yo, a ver, me gustaría saber cómo es que tú defines, o sea, lo de alternancia en
  el precio …».
- **Propuesta: RESUELVE EN PARTE.** No elige letra. Hacia (b) en ese dibujo, pero por otro motivo: lo que
  cuenta es el flujo anterior a la toma («la izquierda»), no la alternancia del retroceso. **Pide que se
  le defina «alternancia»**, y sobre eso descansa S-21 y RN-009 (§4.1).
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** no lo dice.

#### S-6 · La orden puesta en el primer punto que se llena antes de que haya alternancia

- **Tramo:** 30:28–34:08.
- **La respuesta:** «[32:22] más de información desarrollada como digo para poder responder o sea porque
  estas preguntas van» / «[32:30] van dirigidas a este punto aquí pero este punto aquí por lo general o
  sea no operamos nosotros» / «[32:36] solemos operar pues la liquidez por así decirlo izquierda …» y
  «[33:56] … tampoco puedo responder esa pregunta como dios y va enfocado» / «[34:01] a esto aquí que por
  lo general no lo esperamos …».
- **Propuesta: NO RESUELVE.** Dice que no puede responder. **Regla general:** no. **«creo»:** no.
  **Compra y venta:** no lo dice.

#### S-13 · Cuándo pasas el stop a la entrada · A-13

- **Tramo:** 50:05–56:37.
- **La respuesta se corrige a sí misma:** «[51:11] La respuesta es simple» / «[51:13] Apenas toque» /
  «[51:14] Se pone en break up» / «[51:16] No, no» / «[51:17] no es apenas toque es que la vela la
  siguiente vela cierre por encima es la condición cierre». Y: «[52:00] la vela tiene que cerrar con un
  cuerpo por encima o sea de esta zona de aquí para poder poner en» / «[52:10] break even …».
- **Sobre su gráfico, con dudas:** «[52:58] Claro, es que aquí, ahora me he puesto a dudar un poco de este
  ejemplo …»; y un caso en que basta la mecha, con la transcripción dudosa al arrancar: «[53:52] no
  bastaría con mecha porque ya hay o sea hay un imbalance entonces si ya hay» / «[54:01] un rompimiento
  con cuerpo demasiado fuerte en que sólo bastaría que llegue» / «[54:05] la mecha para yo poder poner en
  break y en la operativa». El margen: «[54:54] Pero lo ideal sería dar como un poco de margen.» …
  «[54:58] O sea, cierra con cuerpo, no necesariamente por encima de aquí.» / «[55:01] Pero sí por encima
  de la zona de entrada.» Las condiciones: «[55:54] rompimiento con cuerpo» / «[55:56] desarrollo de zona
  de control» / «[55:58] cierre con cuerpo».
- **Propuesta: RESUELVE EN PARTE, hacia (b), al cierre y con cuerpo**, con la excepción de la mecha ante un
  imbalance. **Contradice lo que está fijado**: `break_even_condicion` = `tocar`, CONFIRMED. Cae de un lado de
  una tensión que ya había: en la sesión 1 dijo «apenas toca» (`ev-v6-005701-7ae2b8d3`), en la 4 «cae ya apenas
  cierra» (`ev-v10-020453-2d41dd25`) y en la 5 las dos cosas en la misma respuesta
  (`ev-v15-013510-6364e7e0`, `ev-v15-013605-c041b814`). No se cierra aquí.
- **Regla general:** sí, con dudas sobre los ejemplos. **«creo»:** no, pero «me he puesto a dudar».
  **Compra y venta:** no contesta (los ejemplos van en los dos sentidos).

#### S-14 · La orden sin llenar cuando el precio toma otra liquidez de M15 · A-53

- **Tramo:** 56:37–60:09.
- **La letra:** «[57:30] Tomar la liquidez más reciente» / «[57:32] O sea, la quito en ese momento» /
  «[57:34] Y espero el punto de la liquidez nueva» / «[57:36] O sea, la respuesta es la A» / «[57:37] la A» /
  «[57:39] la verdad no, como lo planteé aquí» …. Ese «la verdad no» puede ir por el esquema, que corrige
  a continuación, o por la letra: no se puede saber sin más.
- **Al explicarlo sobre el dibujo:** «[58:46] … este es el punto nuevo más» / «[58:57] tarde y este sería
  el que todavía seguiría activo porque para nosotros poder actualizar nuestro» / «[59:02] punto break
  posible mundo breaker tendríamos que esperar a que el precio llegue rompa allí». **Para precisar:**
  «[59:14] … a es igual en compra y en venta o sea con lo explicado aquí sí o sea pero al revés y» /
  «[59:21] si antes de que aparezca el nuevo punto el precio toma todavía otra liquidez pues se va
  actualizando».
- **Propuesta: RESUELVE EN PARTE.** Dice la letra (a), `se_retira`, contra lo de hoy (`se_mueve`), con ese «la
  verdad no» detrás, y su explicación va hacia (b): el punto anterior sigue activo hasta que rompa. En la
  confirmación, «la orden siempre se va a ir actualizando» (59:31). **Cae de un lado de una tensión que ya
  había**: en la sesión 4 dijo que la deja y la mueve y, en la misma frase, «La A es verdadera» (`PREGUNTAS.md`,
  S-14). Decide el consultor.
- **Regla general:** sí. **«creo»:** sobre el ejemplo («[58:38] lo más probable creo yo no 100% seguro»).
  **Compra y venta:** sí.

#### S-15 · La misma liquidez tomada antes de las 7 y otra vez después · A-43

- **Tramo:** 60:09–64:39.
- **La respuesta:** no elige. «[63:21] Entonces, como hemos visto en el gráfico, solo nos enfocamos, o sea,
  si vamos a usar el trazo de liquidez en M15,» / «[63:28] solo nos enfocamos, o sea, para el bias y demás,
  y saber qué hacer luego, a partir de las 7 a después,» / «[63:36] pues solo el trazo de liquidez de M15,
  como hemos visto aquí.» Y: «[64:24] a ver operas operas enfocándote o sea después de las 7 de las 7 en
  adelante pero en m1 o sea» / «[64:33] O sea, antes de las 7 solo se usa para trazo de liquidez.»
- **Propuesta: RESUELVE EN PARTE, y no contesta lo preguntado** (si la segunda toma vale). Lo que dice,
  que antes de las 7 solo se usa para trazar, **no casa a la primera** con `toma_antes_de_la_ventana` =
  `cuenta`, CONFIRMED (`ev-v10-014613-6cf002b2`, «¿lo usas para operar a partir de las 7? Sí»). Hay que
  mirarlo; no se decide aquí.
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** solo compra.

#### S-16 · Los dos extremos de la caja · A-48 y A-49

- **Tramo:** 64:39–75:14. Da el esquema por bueno («[73:43] … usando este esquema inventado que está bien
  planteado …») y pierde unos minutos porque se le congela la pantalla (67:31–70:13).
- **A-48, de qué velas sale el 1:** «[65:22] A ver, entonces sería, vale, este es el punto cero, y el punto 1
  estaría aquí, en el A,» / «[65:33] claramente, porque es la mecha más alta.» y «[65:41] … entonces la
  respuesta sería al punto más» / «[65:50] alto de todas las velas desde el punto …». **Propuesta: RESUELVE
  el 1: (c), `caja_bloque` = `r6`, lo de hoy.** **El 0 no queda claro:** «[73:35] Para confirmar el final,
  el 0 de la caja va en el punto más reciente,» y a continuación «[73:49] desde el punto más bajo,» /
  «[73:52] cuando se tomó la liquidez», sin elegir entre `ultimo_pivote_m1` y `referencia_de_la_toma`.
  **En una compra:** «[73:28] Una compra al revés, exactamente como lo hemos visto en el gráfico,» /
  «[73:32] sería el arriba del 0 y el 1 abajo.»
- **A-49, cuándo la traza:** «[72:54] apenas ocurre el rompimiento yo ya voy trazando la caja ocurre el
  rompimiento suponiendo en este» / «[73:01] caso sería desde aquí hasta aquí ocurre el rompimiento y atraso
  y cierra la vela ojo con» / «[73:07] esto tiene que cerrar la vela rompimiento cierra de la vela no importa
  con mecha o sea con cuerpo». Y mientras no aparece otro punto: «[74:19] si no se llega a actualizar, o sea,
  por ejemplo» / «[74:21] actualizar de aquí a aquí» / «[74:23] pues simplemente se mantiene» / «[74:25] en el
  punto anterior …». **Propuesta: RESUELVE: al cierre de la vela que rompe**, con mecha o con cuerpo, que casa
  con `caja_se_fija` = `en_cada_cierre_m1` (lo de hoy).
- **Regla general:** sí en las dos. **«creo»:** no. **Compra y venta:** sí.

#### S-17 · Frente al nivel tomado: solo el 0 o la caja entera · A-50

- **Tramo:** 75:14–87:40. La pausa (§2.1) cae aquí; la pregunta se lee después, desde 83:20.
- **La respuesta:** «[84:21] descarto la B» y «[85:00] quedaría» / «[85:00] el dibujo B, la caja entera por
  encima» / «[85:03] quedaría descartado». **Su motivo:** «[84:41] simplemente la caja va a estar por debajo»
  / «[84:43] de M15, pero no va a estar por arriba» y «[87:15] … frente al nivel tomado descarto» / «[87:23]
  la caja cuando por ejemplo en este caso sería el dibujo B o sea si no existe una toma debajo» / «[87:29] no
  puedes tú trazar la caja …». **Para precisar:** «[85:49] es indiferente la verdad», y no entiende la
  pregunta de cuánto se pasa el 0 (86:37–86:41).
- **Propuesta: RESUELVE: (b), `caja_entera`, lo de hoy.** Con un matiz: su motivo es que en el dibujo B no
  ve la toma, no la posición de la caja frente a una toma dada. De la caja a caballo (dibujo A) solo dice
  que puede ir «entre» (84:34, 85:27).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí (85:04).

#### S-19 · El precio ya está más allá del 0 cuando se forma la caja

- **Tramo:** 100:25–104:13. Aquí el esquema le gusta («[100:45] Me gusta.»).
- **La respuesta:** «[101:03] si, o sea, se pone la orden igual, aquí ya se activaría la orden, es más, o sea,
  al ocurrir este rompimiento de aquí, ya a mí me habilita …», y a media línea duda del 0 del dibujo y va al
  gráfico. **El tipo de orden:** «[102:35] … con qué tipo de orden pues estamos» / «[102:41] trabajando el stop
  order si el precio está por encima vamos actualizando o sea el nivel de caja». **La confirmación:** «[103:50]
  … como digo este 0 el» / «[103:56] el nivel del cero se tiene que ir actualizando» / «[103:58] conforme se
  vaya desarrollando, pues,» / «[104:00] nuevos, en este caso, serían nuevos» / «[104:02] altos.»
- **Propuesta: RESUELVE EN PARTE.** Dice (a), que se pone igual, y con stop order; y lo que explica es que el
  0 va subiendo con los altos nuevos, con lo que el precio no se queda más allá. **Hoy el bot** hace (b) sin
  parámetro: la orden del lado equivocado la rechaza el bróker y ese rechazo gasta el punto. No aclara qué
  pasa con una orden stop de compra por debajo del precio.
- **Regla general:** en parte. **«creo»:** no. **Compra y venta:** no lo dice.

#### S-20 · La vela de 1 o 2 puntos en el retroceso, y la vela sin cuerpo con mechas largas

- **Tramo:** 104:13–108:02, con un tramo ajeno a la operativa al abrir (§2.4).
- **La vela de 1 o 2 puntos:** «[106:03] … entonces una vela de uno con cambio de color cuenta como cambio de
  color sería la» / «[106:13] respuesta c otra cual con lo que hemos explicado aquí o sea influye influye
  claramente …», y la confirmación: «[107:36] Sí, es que, claro, a ver, una vela de uno o dos puntos con cuerpo
  en el retroceso, o sea, el retroceso, pues, es válido, o sea, como cambio de color para trazar el punto, y de
  una vela sin cuerpo sus mechas, pues, también cuentan …».
- **Las mechas de la vela sin cuerpo:** «[106:44] en M1 cuenta, la mecha» / «[106:46] cuenta en M1, o sea, si
  solo es» / «[106:48] contexto de M1, cuenta» / «[106:49] si es combinación con contexto de M15» / «[106:52]
  para validar una toma de liquidez» / «[106:54] de M15, no cuenta».
- **Propuesta: RESUELVE.** Marca (c), y su contenido cae en (a) y en (b) de la subpregunta en M1: las dos
  DECISIONES DEL CONSULTOR de ADR-0085:72-78. Añade el matiz de M15: para validar una toma, no cuenta. **Frente a
  la sesión 5:** «no se toma en cuenta» (`ev-v16-000851-f5ae3b6f`).
- **Regla general:** sí, en M1. **«creo»:** no. **Compra y venta:** sí (106:01, en un ejemplo).

#### S-21 · El punto de breaker roto con la mecha después de una alternancia

- **Tramo:** 108:02–110:47.
- **La respuesta:** «[109:45] esta alternancia, o sea» / «[109:46] la respuesta sería C» / «[109:47] o sea, y
  seguir, o sea» / «[109:50] el flujo, o sea, que apenas toque nos activa» / «[109:52] la entrada y después» /
  «[109:53] haga lo que tenga que hacer …», y la confirmación: «[110:29] Entonces, si el punto se rompe con la
  mecha después de una alternancia, pues, como digo, o sea, que ocurra lo que tenga que suceder, pero claro, antes
  de eso tiene que cumplirse los criterios de validar el posible punto breaker correctamente, tener la order stop y
  la caja, …». **«¿Cambia algo si es de una sola vela?»:** «[110:06] me salta esta pregunta porque».
- **Propuesta: RESUELVE EN PARTE: marca (c).** Con el punto validado y la orden puesta, entra; **hacia la (a), lo
  cual es una lectura**, porque exige que se cumplan los criterios y **no comparte qué es alternancia** (S-5). Si
  se lee así, **va contra el bot**, que hace (b) por RN-009; es la fila DISTINTO de ADR-0085:87-91.
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí (110:02).

#### S-22 · Para que el máximo de la verde sea tu punto, ¿qué tiene que hacer la roja?

- **Tramo:** 110:47–114:48.
- **La respuesta:** primero marca la (c) y dice que falta contexto («[112:21] la respuesta de la C no sé si es
  indiferente, o sea» … «[112:25] aquí falta un poco más» / «[112:27] de contexto …»), y después:
  «[113:07] porque tendría que el precio haber roto aquí» / «[113:10] con cuerpo o con mecha» / «[113:12] cualquiera
  de los dos para yo poder validar este punto breaker» y «[113:18] la roja cierra dentro de la verde sin pasar su
  mínimo» / «[113:23] pues en este caso no podríamos nosotros» … «[113:29] no podríamos nosotros trazar aquí» /
  «[113:31] como un punto breaker …». **La confirmación:** «[114:11] … el máximo de la vela verde es mi punto cuando
  la roja de» / «[114:18] después haya roto haya roto con mecha con cuerpo pues sus rangos al nivel más bajo de aquí».
  **Si vale solo con la mecha:** «[114:04] que lo pase sólo con la mecha exacta no va en m como digo sólo en el
  contexto de m15 relacional» / «[114:11] m15 pues con mecha con cuerpo es válido …»: el ASR deja dudoso ese «m15».
  **El flujo bajista:** «[113:49] pensé» / «[113:49] que venía de un flujo bajista aquí»: lo da por supuesto.
- **Propuesta: RESUELVE EN PARTE: hacia (b) en la forma de romper**: en el dibujo, si la roja no pasa el mínimo no hay
  punto (113:18–113:33), y al final tiene que haber roto, con mecha o con cuerpo; marcó antes la (c). **Si se lee
  así, va contra el motor**, que forma el punto con cualquier roja que cierra tras una racha verde (ADR-0085:79-83,
  decisión del consultor). Frente a A-32 («en M1 la mecha siempre vale»): la frase de la mecha va ligada a ese «m15»
  dudoso, y si choca o no lo mira el consultor. Es lo que `ev-v15-004037-a2ab3980` decía y no se aplicó.
- **Regla general:** sí. **«creo»:** no; dudas sobre el esquema. **Compra y venta:** no lo dice.

#### S-23 · Una toma de la mañana, y por la tarde el mismo sesgo · A-46 (RESUELTA)

- **Tramo:** 114:48–118:19.
- **La respuesta:** contesta sobre el sesgo de H4 y el rango, no sobre la toma: «[115:39] … para cambiar de sesgo a
  bajista, en este caso, tendría que haber una vela roja que haya roto con mecha o con cuerpo, pues, el bajo de la
  vela verde.» Y: «[117:26] Ahora, y si en la mañana ya operaste esa toma, pues si todavía no se rompe el rango que
  tenemos planteado,» / «[117:33] pues seguimos operando, o sea, en este caso sería alcista.». Lo primero contesta al
  «Para precisar», que en la hoja empieza «Si vale, ¿y si en la mañana ya operaste esa toma?». Y al blanco de la
  confirmación («con el mismo sesgo por la tarde, la toma de la mañana ______»): «[117:41] sesgo por la tarde, la toma
  de la mañana» … «[117:49] como digo, o sea» / «[117:50] va a depender si se rompe o no el rango» … «[117:57] tiene que
  ser H4» / «[117:59] para poderlo balear, no nos sirve» / «[118:00] M15, tiene que ser H4».
- **Propuesta: A DECIDIR POR EL CONSULTOR, sin veredicto de esta sesión.** No elige letra. Lo que dice, que
  depende de si se rompe el rango de H4 y que mientras no se rompa sigue operando, **puede leerse hacia (a)**, y (a)
  contradiría A-46 RESUELTA (hoy, (b)): sería un `REOPEN`, que en esta rama no se hace. **También puede leerse como
  una respuesta sobre el sesgo y no sobre la toma**, porque casi toda su explicación es del sesgo. Si la reabre lo
  decide el consultor; A-46 no se toca.
- **Regla general:** no sobre la toma; sí sobre el sesgo. **«creo»:** no. **Compra y venta:** sí («si es bajista,
  pues bajista», 117:36).

### 3.5 «Para cerrar» (sin código de voz)

Se hizo en voz (respuesta c): 118:22–119:28. Lo que dijo, sin decidir nada:

- **Diciembre (NA:I).** Lo que contesta cae en el bloque en cuarentena y su margen (1:58:24–1:58:27): **queda sin
  cita y aquí no se parafrasea.** Lo que hay es la declaración de Aleks (respuesta a): «sobre diciembre dijo que aún no
  lo ha grabado». En la sesión 5, «lo grabo tal cual» (`ev-v16-003228-b515b93e`). La línea del margen se leyó antes
  de que existiera el tramo (`HOLDOUT-EXPOSICIONES.md`, 2026-11-05).
- **Agosto (NA:Q).** «[118:29] agosto» / «[118:29] creo que sí» / «[118:30] creo que está» / «[118:31] en el drive» /
  «[118:32] creo» / «[118:32] no sé si está allí subido» / «[118:36] Creo que no está» … «[118:54] No, sí, creo que
  está» / «[118:55] En el drive». **No afirma que esté.** Y, en S-3, del replay: «[05:59] si me vuelves a pedir, por
  ejemplo» / «[06:01] de agosto, el de agosto no lo» / «[06:02] tengo aquí, como te había comentado» / «[06:04] de la
  actualización de la cuenta» / «[06:05] y que había perdido». Hay también una mención de vídeos que no se entiende sin
  contexto: «[119:03] Porque pasé los videos solo de los meses que...» / «[119:05] O sea, de los días que tenías.» …
  «[119:08] Porque había un video extra, pero ese video no lo pasé» / «[119:11] porque eso no lo teníamos en datos.»

### 3.6 Lo demás que dijo: el vídeo de mapeo y las sugerencias

Sin código, y no resuelve nada:
- **Un vídeo de mapeo, ofrecido por él.** «[94:22] bro, ¿te sirve que yo» / «[94:24] haga un video» / «[94:26] de cómo
  mapeo» … y «[97:55] Lo voy a hacer» / «[97:57] Y te lo subiré al drive». Cree que de ahí parte lo que el bot hace
  mal (95:39–95:49, 96:00). Si llega, es material nuevo: no se usa sin registrarlo.
- **Más contexto en los ejemplos**, dicho en S-18 sobre su esquema: «[93:35] a ver lo que me gustaría que hagas es que
  en cierta parte también me des un contexto un poco» / «[93:41] más claro o sea de lo que ha ocurrido antes también
  el precio …».
- **Una próxima sesión pronto:** Aleks la anuncia por las preguntas pendientes y el trader dice que le va bien
  el fin de semana (119:44–119:54). La grabación acaba a media frase («[119:58] pero antes»).
- **Cómo marcar la liquidez, consejo al bot:** «[45:26] yo suelo utilizar la trendline por defecto …», hasta donde haya
  rompimiento y sin extenderla (45:00–46:08).

## 4. Contradicciones, cobertura de F y cosas que el consultor tiene que mirar

### 4.1 Contradicciones y cosas que mirar

1. **S-2:** la (c) no cabe en `perdida_trader_reinicio_huso`: PARADA de §4 de `ACTIVAR-A35-A44.md`. El reloj que da
   (UTC+2 «si no me equivoco») no es el medido en sus gráficos (ADR-0069).
2. **S-3, la pregunta principal:** no elige entre las lecturas de `liquidez_m15_mecha_que_vuelve` (§3.1 las confronta
   una a una): PARADA de §4.
3. **S-3, el primer «Para precisar»:** la (a), con la condición del bias, contradice la parte de ADR-0084 que dice que
   una M1 que cierra con cuerpo sobre el nivel original ya no es toma. Pide ADR. La otra parte, que tras la toma no se
   mueve, va en esa dirección, con el «no sé si» de 17:38.
4. **S-3 contra la sesión 5:** «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`).
5. **S-4 contra el bot:** la vela sin cuerpo no corta la racha en M15; hoy sí. Sin parámetro.
6. **S-5 y S-21: el trader no comparte la premisa de «alternancia»** y pide que se defina. De eso dependen las dos y
   RN-009, y es lo que más separa al bot de él (`RECORRIDA-CONSTRUCCION.md` §2.6).
7. **S-13 contra lo fijado:** al cierre y con cuerpo, frente a `break_even_condicion` = `tocar`, CONFIRMED; en las
   sesiones 4 y 5 dijo las dos cosas.
8. **S-14:** la letra (a) contra su propia explicación, hacia (b), con el «la verdad no» de 57:39; la sesión 4 ya tenía
   las dos.
9. **S-15 contra lo fijado:** «antes de las 7 solo se usa para trazo de liquidez», frente a
   `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED. No contesta si vale la segunda toma.
10. **S-18:** «las veces que sean necesarias» frente a `cartuchos_max` = 3 por liquidez, y un «igual» que D1 no pide. Y
    corrige, con dudas, el `ev-v15-002029-1ac081ae`, citado en el recuadro de ADR-0083: cree que su duda era de los
    equals, no del break even.
11. **S-19 contra el bot:** pone la orden igual; hoy el bróker la rechaza y gasta el punto.
12. **S-20 contra la sesión 5:** la vela de 1 o 2 puntos ahora cuenta en el retroceso (casa con ADR-0085, y lo contrario
    era `ev-v16-000851-f5ae3b6f`).
13. **S-21 y S-22, si se leen hacia (a) y (b), contra el motor:** ADR-0085:87-91 y :79-83, decisiones del consultor.
14. **S-23 frente a A-46:** puede leerse hacia (a), que sería un `REOPEN` (§3.4). Lo decide el consultor.
15. **Los gráficos.** (a) Fueron por WhatsApp, no en la pantalla de Aleks como dice la hoja: el trader tiene los ficheros
    de esos dos. (b) Pide la fecha, y en la llamada queda que se le pondrá (49:46). **Eso va contra la regla 2 de
    `SESION-DE-PREGUNTAS.md`** («sin la fecha visible») y, aunque sean días de construcción, le permitiría buscar el día en
    su replay. **Lo decide el consultor antes de rehacerlos.** (c) No dice si coincide con la línea del marcado en
    ningún gráfico. (d) Pide ver criterios y trazos: es otro gráfico, no este, y `scripts/graficos_sesion.py` no los dibuja.
16. **El trader responde a menudo sobre su gráfico, no sobre el dibujo**, y su juicio de los esquemas, para hacer los
    siguientes: mal planteados, en todo o en parte, los de S-4 (21:07), S-6 (31:30), S-14 (57:39), S-15 (63:10), S-18
    (91:05, «algo que no me cuadra») y S-22 (112:13). De S-5 dice las dos cosas: le gusta el ejemplo (24:35) y sobre su gráfico
    «no es la aplicación de la regla» (28:11). Bien, los de S-1 (01:14), S-13 (50:59), S-16 (73:43) y S-19 (100:45). S-2 no lleva
    esquema: lo que da por mal planteado es la frase de confirmación (04:36).
17. **Diciembre y agosto:** §3.5. Lo de diciembre sin cita; lo de agosto, con dudas y sin decir que esté subido.

### 4.2 Cobertura de F

Lo que la sesión 6 tenía que cubrir (encargo, «Cobertura de F»), con el código que lo preguntó. «S-n» es de la sesión 6:

| Lo que tenía que cubrir | Código | Cubierta |
|---|---|---|
| A-13 (al toque o al cierre) | S-13 | en parte: hacia el cierre con cuerpo, con una excepción y contra lo fijado |
| A-35, qué mecha mueve el nivel | S-3 | en parte: PARADA de §4 en la pregunta principal |
| A-35, la vela sin cuerpo en M15 | S-4 | sí, y contra el bot |
| A-43 (la misma toma dos veces) | S-15 | no contesta lo preguntado; dice otra cosa, que choca con lo fijado |
| A-44, la magnitud | S-1 | sí: solo cerradas, `saldo` |
| A-44, el reloj del reinicio | S-2 | en parte: (c), PARADA de §4 |
| A-48 (de qué velas sale el 1) | S-16 | sí el 1, (c); el 0 no queda claro |
| A-49 (la caja cerrada o en formación) | S-16 | sí: al cierre de la vela que rompe |
| A-50 (la caja a caballo) | S-17 | sí: (b), con otro motivo |
| A-53 (la orden sin llenar) | S-14 | en parte: dice la letra, y la explicación va en otro sentido |
| ADR-0083 D1 | S-18 | en parte: vuelve si se valida, pide «un igual», sin número y sin decir qué caja |
| ADR-0084, «el nivel se congela» | S-3 | en parte: lo posterior a la toma va en esa dirección, con un «no sé si»; lo anterior lo contradice la (a) |
| S-14 de la sesión 5 (por qué no entró) | S-7 a S-12 | muy en parte: gráfico 1 (a), gráfico 2 sin decisión, 3 a 6 sin hacer |
| S-15 de la sesión 5, dibujo 2 | S-5 | en parte: no comparte la premisa |
| S-15 de la sesión 5, dibujo 3 | S-6 | no: dice que no puede responder |
| S-16 de la sesión 5 (el precio más allá del 0) | S-19 | en parte |
| S-11 de la sesión 5 (la toma de la mañana) | S-23 | en parte: «va a depender si se rompe o no el rango»; lo decide el consultor |
| S-22 de la sesión 4 (A-36, la orden en el 0 con mecha) | ninguno | **no se preguntó, y el encargo no dice por qué se pide.** A-36 está RESUELTA desde esa sesión (`SESION-04-EXTRACCION.md`, tabla final; `fb-2026-10-04-sesion-04-bbfb5c98`) y no hay nada pendiente de ella en la hoja de ruta ni en `PREGUNTAS.md`: el consultor dirá si se refería a otra cosa |
| La condición de `ev-v15-004037-a2ab3980` (`ACTIVAR-SESION-05-MOTOR.md` §2.4) | S-22 | en parte: hacia (b) en la forma de romper; marcó antes la (c) |
| A-46 | S-23 | a decidir: puede leerse hacia (a), que sería un `REOPEN`; esta rama no lo hace |
| S-19 frente a S-24 de la sesión 5 (la vela de 1 o 2 puntos) | S-20 | sí |

## 5. Tabla final

| Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|---|
| **S-1** | A-44 | v17 | 00:00–02:23 | **resuelve**: (a), solo cerradas = `saldo`, sin PARADA | sí | no | n/a |
| **S-2** | A-44 | v17 | 02:25–04:38 | en parte: (c), al abrir la primera sesión; no cabe en el parámetro: **PARADA de §4** | sí | solo en el reloj | n/a |
| **S-3** | A-35 | v17 | 04:38–19:32 | en parte: no elige, «indiferente», **PARADA de §4**; el primer «Para precisar», (a) con la condición del bias, contradice ADR-0084 | en parte | no | sí |
| **S-3, el nivel se congela** | ADR-0084 | v17 | 17:22–17:42 | en parte: «no» y «ya nos es indiferente», con un «no sé si» detrás | en parte | ese «no sé si» | sí |
| **S-4** | A-35 | v17 | 19:33–23:58 | **resuelve**: (c); el alto puede ser la mecha de la vela sin cuerpo, y que no corta es la conclusión del informe; contra el bot, sin parámetro | sí | no | sí |
| **S-18** | ADR-0083 | v17 | 87:42–100:24 | en parte: vuelve si se valida, pide «un igual» y dice que casi no se repite; sin número; sin decir qué caja | sí, condicionada | no | no lo distingue |
| S-7 | gráfico 1 | v17 | 34:08–46:49 | en parte: (a), no hubo toma; no ve claro M15 y no dice de la línea | no | sí, la sesión de las 11 | n/a |
| S-8 | gráfico 2 | v17 | 46:49–50:04 | no resuelve: sin decisión; pide fecha y criterios | no | sí | n/a |
| S-9 a S-12 | gráficos 3 a 6 | — | — | no se hicieron | — | — | — |
| S-5 | ACTIVAR-MOTOR §2.5, dibujo 2 | v17 | 23:58–30:27 | en parte: hacia (b) en ese dibujo; no comparte la premisa de alternancia | en parte | no | no lo dice |
| S-6 | ACTIVAR-MOTOR §2.5, dibujo 3 | v17 | 30:28–34:08 | no resuelve: dice que no puede responder | no | no | no lo dice |
| S-13 | A-13 | v17 | 50:05–56:37 | en parte: hacia (b), al cierre con cuerpo; contra lo fijado | sí | no; «me he puesto a dudar» | no contesta |
| S-14 | A-53 | v17 | 56:37–60:09 | en parte: dice (a) y explica hacia (b) | sí | sobre el ejemplo | sí |
| S-15 | A-43 | v17 | 60:09–64:39 | en parte: no contesta lo preguntado; choca con `toma_antes_de_la_ventana` | en parte | no | solo compra |
| S-16 | A-48 | v17 | 64:39–75:14 | **resuelve** el 1: (c) = `r6`, lo de hoy; el 0 no queda claro | sí | no | sí |
| S-16 | A-49 | v17 | 72:46–74:27 | **resuelve**: al cierre de la vela que rompe, con mecha o con cuerpo | sí | no | sí |
| S-17 | A-50 | v17 | 75:14–87:40 | **resuelve**: (b) = `caja_entera`, lo de hoy, con otro motivo | sí | no | sí |
| S-19 | ACTIVAR §3.9 | v17 | 100:25–104:13 | en parte: (a) y el 0 se actualiza; contra el bot | en parte | no | no lo dice |
| S-20 | ACTIVAR §3.10 | v17 | 104:13–108:02 | **resuelve**: cuenta en M1, y la mecha también; para una toma de M15, no | sí, en M1 | no | sí, en un ejemplo |
| S-21 | ACTIVAR §3.11 | v17 | 108:02–110:47 | en parte: marca (c), hacia (a); depende de qué es alternancia; contra el bot si se lee así | sí | no | sí |
| S-22 | ACTIVAR-MOTOR §2.4 | v17 | 110:47–114:48 | en parte: marca (c) y después hacia (b), romper con mecha o con cuerpo; contra el motor si se lee así | sí | no; dudas del esquema | no lo dice |
| S-23 | A-46 (RESUELTA) | v17 | 114:48–118:19 | a decidir por el consultor: «va a depender si se rompe o no el rango»; puede leerse hacia (a), que sería un `REOPEN`, y no se hace aquí | sí del sesgo; de la toma, no la da | no | sí, del sesgo |
| Para cerrar | NA:I, NA:Q | v17 | 118:22–119:28 | diciembre, sin cita; agosto, con dudas; lo que dijo, sin decidir | n/a | sí (agosto) | n/a |

Por códigos de la hoja (23): se hicieron 19 y no se hicieron 4 (S-9 a S-12). De esos 19, en filas: **resuelve** 6 (S-1, S-4, S-16 dos veces, S-17 y
S-20); **en parte** 12 (S-2, S-3, el nivel se congela, S-18, S-7, S-5, S-13, S-14, S-15, S-19, S-21 y S-22); **no resuelve** 2 (S-8 y S-6); **a decidir**,
sin veredicto, 1 (S-23). Más «Para cerrar».

> **RECUADRO DE CORRECCIÓN del 2026-11-05 (`trabajo/activar-sesion-06-motor`; la tabla y el cuerpo
> no se tocan).** La fila de S-2 dice «en parte … no cabe en el parámetro: PARADA de §4», con regla
> general «sí»: la «en parte» lo era por falta de opción en el parámetro, no por la respuesta. La
> rama de motor añade la opción (`perdida_trader_reinicio = primera_sesion_dia_siguiente`, ADR-0089,
> `fb-2026-11-04-sesion-06-6886938e`) y, con S-1, A-44 queda RESUELTA
> (`fb-2026-11-04-sesion-06-c56ec7cf`; `ACTIVAR-SESION-06-MOTOR.md`, fase 1). Las demás filas no
> cambian.

## 6. Para la orden de cierre (preparado, sin aplicar)

Nada de esto se aplica en la rama (encargo, «Cierre de la rama»).

**a) El texto nuevo de F** en la Next Action, con la activación como entrada propia:

> F. Activar la sesión 6 (R4.2): celebrada el miércoles 2026-11-04 (v17, 1:59:59) e ingerida en trabajo/sesion-06
> (SESION-06-EXTRACCION.md, tabla final y §4). Dos PARADAS de §4 de ACTIVAR-A35-A44.md para el consultor: S-2 (la (c)
> no cabe en perdida_trader_reinicio_huso) y S-3 (la mecha, y la (a) contra ADR-0084). Los gráficos 3 a 6 y el 2 quedan
> sin contestar: antes de rehacerlos, decidir lo de la fecha (regla 2 de SESION-DE-PREGUNTAS.md). H va después de esta
> activación. R6a en los huecos.

Sustituye a la F de hoy, y con ella la fecha equivocada que el encargo manda recoger: unos 340 bytes más.
`PROJECT_STATE.md` está en 22.212 bytes (§9): con a) y c), hacia 22.650, bajo 25.000.

**b) Lo que R4.2 gana** en `docs/plan/HOJA-DE-RUTA.md`, en una línea de Estado:

> - **Estado:** la sesión 6 se celebró el 2026-11-04 (v17) y está ingerida (SESION-06-EXTRACCION.md, stable/F38m-sesion-06). Falta la
>   activación, que decide el consultor. De los gráficos 1 a 6 solo se contestó el 1; el 2 quedó a medias y del 3 al 6 no se hicieron.

**c) La línea de la copia de seguridad** (Technical Debt):

> - Copia de seguridad de las crudas y los WAV: hecha hasta v10 (2026-10-22, Drive privado de Aleks, con SHA256SUMS); v15, v16 y v17 según lo que confirme Aleks (SESION-06-EXTRACCION.md §12). Cada sesión nueva se añade tras su ingesta; los vídeos de las sesiones, recomendado, sin hacer.

**d) Dos filas para `ERRORES-RECURRENTES.md`**, que esta rama no toca: el commit que toca `tramos_no_citables.yaml` sin
`Fuente:`, que `make check` no ve hasta el commit siguiente (§7, punto 3); y la línea de PLANTILLA, que `abrir-rama` no nombra y
ya ha salido dos veces (§7, punto 1). Las dos piden una línea en las skills.

**e) Para la activación:** el feedback de esta sesión lleva `fecha` y `recibido_el` 2026-11-04, con el id
`2026-11-04-sesion-06`; es un solo vídeo. **Para H**: va después de esa activación (encargo, «Objetivo»).

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
5. **Un ítem de evidencia se creó y se borró antes de commitear** (el del reloj de S-2): su afirmación
   decía de un bloque en cuarentena más de lo que se sabe. Se rehízo sin eso (`ev-v17-000321-37cebf44`).
6. **Los días.** Lo escrito hasta el 2026-11-04 lleva esa fecha; desde la medianoche, la evidencia y lo
   siguiente son del 2026-11-05, y por eso `HOLDOUT-EXPOSICIONES.md` lleva una fila de ese día. El id de
   la sesión y `revisado_por` siguen con el 2026-11-04, porque es el del encargo.
7. **Lo que el encargo daba por hecho y la medida matiza** (`CLAUDE.md`, «Como se trabaja»): la hoja dice que
   los gráficos los enseña Aleks en pantalla, y se pasaron por WhatsApp (§2.4). Ninguna negativa de la guardia
   cayó sobre un paso que mande la skill `ingerir-sesion`, así que ninguna es el hallazgo de la rama de guardias.
8. **Tres negativas al revisor**, que no rodeó (el detalle, en su informe): un `python -c` que imprime la evidencia de v17, porque
   la guardia lee `C:` en un `print` como una carpeta protegida (falso positivo, para la rama de guardias); y, por ser de solo
   lectura, `evidence contradictions` y `knowledge validate` con redirección. `knowledge validate` lo repitió sin redirigir, y
   `evidence contradictions` lo lanzó la sesión tras las correcciones (§11). Hizo además una consulta a la CI con un repo equivocado,
   que dio 404.
9. **El encargo y `S-22 de la sesión 4`:** §4.2. No se encuentra qué le quedaba pendiente.
10. **`grep -c $'\r' docs/validation/SESION-06-EXTRACCION.md`, negado por la guardia** («el argumento `$'\r'` se construye al
    ejecutarse»). Solo era una comprobación de saltos de línea tras pegar el informe del revisor con un guion de la carpeta de
    trabajo. Se abandonó: lo mira `make check`. No es un paso que mande la skill.

## 8. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` (v17) y `manifest.yaml`.
- La transcripción `tr-v17-large-v3-int8-float16-9d44007a` y los fotogramas `fr-v17-db232fc6`.
- `knowledge/corpus/tramos_no_citables.yaml`: 12 tramos nuevos de v17: 3 SIN AUDIO, 6 de cuarentena, 1 de precaución y 2 ajenos.
- **82 ítems de evidencia, 65 vivos** (abajo): en `b368016` entraron 64, y tras el revisor 18 más, 17 que supersedan y uno nuevo.
  `evidence contradictions`: `0 contradicciones abiertas`. `knowledge validate`: `OK: 640 items de evidencia, 0 contradicciones
  abiertas, historial intacto`.
- `src/botsito/corpus/cuarentena.py` (v17 en `SESIONES_EN_CUARENTENA`) y sus tests.
- `docs/sesion-6/HOJA-USADA.md` y el recuadro de `docs/sesion-6/PREGUNTAS.md`.
- `docs/validation/HOLDOUT-EXPOSICIONES.md`: tres filas del 2026-11-04 y dos del 2026-11-05.

**La evidencia viva, por código** (todos llevan `ev-v17-` delante; qué supersede a qué, en §11 y en cada ítem):

| Código | Ítems |
|---|---|
| S-1 | `000218-001b08fb`, `000134-725523bf` |
| S-2 | `000250-a468bcec`, `000321-37cebf44`, `000351-331daa6d` |
| S-3 | `001319-419307f6`, `001543-c92f549c`, `001610-c43239a9`, `001712-dc155b5d`, `001728-b7b9a32c`, `001847-4e7b7c0b`, `001036-e7bdd027` |
| S-4 | `002155-f2c95111`, `002250-d6ca3ef8`, `002217-af442f84` |
| S-5 | `002516-426ce5b2`, `002803-4c5ea744`, `002954-613d9421` |
| S-6 | `003356-f27b96e3`, `003222-85f12e6b` |
| S-7 | `004338-c8befc62`, `004407-42808be7` |
| S-8 | `004841-7f53bbb0`, `004910-11d48393` |
| S-9 a S-12 | — (no se hicieron) |
| S-13 | `005111-8933dab2`, `005200-4f93afa0`, `005352-cda6245d`, `005454-90ce4feb`, `005554-172ecbb2` |
| S-14 | `005730-76948af1`, `005846-0891a9c9`, `005914-55580dc0` |
| S-15 | `010321-352430e3`, `010424-6d7f2d3f` |
| S-16 | `010541-05a69879`, `011328-a701a547`, `011254-542726f6`, `011419-0862662c` |
| S-17 | `012500-39e18f12`, `012441-2ade00be`, `012715-8aaaa59f` |
| S-18 | `013939-860b33e0`, `013009-5e47afdb`, `013806-e8869c2a`, `013815-9cf6f076`, `012917-46a2c561` |
| S-19 | `014103-8cf3e7fb`, `014235-f3375358`, `014350-ec133d13` |
| S-20 | `014603-63d190df`, `014644-674966b7`, `014736-30d2947b` |
| S-21 | `014945-9e7de278`, `015029-bc697500` |
| S-22 | `015307-0870a8ca`, `015318-1256caf7`, `015404-06ac0e9d` |
| S-23 | `015726-ce2e42e4`, `015741-8f9fd638` |
| Para cerrar | `015829-7ba798f5`, `015854-de425918` (agosto), `000559-5a0a1597` (el replay de agosto, dicho en S-3); diciembre, sin ítem (§3.5) |
| Fuera de la hoja | `013422-7e8af905`, `013755-a08cc10e` (el vídeo de mapeo), `013335-b77b5fa2` (más contexto en los ejemplos) |

## 9. El cierre de la rama: sellos, push y CI

**Los commits**, cada uno con su `make check` sellado:

| Commit | Qué | SELLO (árbol) | PICO DE MEMORIA |
|---|---|---|---|
| `6c96499` | abre la rama: encargo, contrato y Archivo 55 | `d374be36…` | 307 MiB en `test` |
| `b2ddfeb` | registro de v17, en cuarentena; los tres silencios (§7, punto 3) | `2948d728…` | 305 MiB en `test` |
| `d4d33bd` | v17 transcrita, filtrada y con fotogramas; sus bloques en cuarentena | `77aed208…` | 306 MiB en `test` |
| `b368016` | la extracción, la evidencia y la hoja usada | `b6c7c916…` | 308 MiB en `test` |

Todos con `exit=0` y `3210 passed`, en unos 1.200 s (el último, `DURACION de make check: 1273 s`). Dos `make check` salieron en
rojo y no se commitearon, cada uno con `1 failed, 3209 passed` (§7, puntos 1 y 3). El commit con los arreglos del revisor (§11) lleva
su propio sello: va en el mensaje final a Aleks, porque este informe no puede llevar el de su propio commit.

**Comprobaciones del contrato sobre `b368016`** (con los arreglos de §11, se repiten antes de su commit):
- `git diff --name-status main...HEAD -- knowledge/evidence knowledge/corpus/transcripciones knowledge/corpus/fotogramas
  data/manifests`: solo `A` (66: 64 ítems, la transcripción y los fotogramas);
- `knowledge validate`: `OK: 622 items de evidencia, 0 contradicciones abiertas, historial intacto`;
- `evidence contradictions`: `0 contradicciones abiertas`;
- `corpus check --hashes`, `corpus transcript check` y `corpus frames check`: §1.2, §2.2 y §2.5.

**`PROJECT_STATE.md`**: 22.212 bytes. La rama no lo toca más que al abrir, y lo preparado en §6 lo deja bajo 25.000.

**Push:** `git push origin trabajo/sesion-06:refs/heads/fix/sesion-06`, `* [new branch] trabajo/sesion-06 ->
fix/sesion-06`. El clasificador no lo negó.

**CI de Linux, run 41976558765** (`fix/sesion-06`, sobre `b368016`). Se esperó con `sleep` en segundo plano. El número se tomó
de una consulta suelta a la API de check-runs con el sha literal (aún `in_progress`); el resultado, de un `gh run view` suelto y
`--log-failed`. **Falla solo el test esperado:** `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` con `ERROR:
PROJECT_STATE declara la rama 'trabajo/sesion-06'; la rama actual es 'fix/sesion-06'`. El resultado: `1 failed, 3162 passed, 47
skipped in 391.19s`.

Este §9 entra en un commit posterior a `b368016`, que se empuja igual a `fix/sesion-06`; su run va en el mensaje final a Aleks.

## 10. El encargo, punto por punto

| # | Requisito | Estado | Dónde |
|---|---|---|---|
| 1 | `git fetch --prune`; base entera: main, tag último y en origin, CI con un `gh run view` suelto, ninguna otra rama, hoja 06 en el guion | Hecho | «Base comprobada al abrir» |
| 2 | Abrir con `abrir-rama`: encargo con Write, contrato y Archivo | Hecho | `6c96499` |
| 3 | No resolver nada; `transcribir_sesion.py` sin tocar; ADR-0083 sigue PROVISIONAL | Hecho | `rutas_protegidas`; §3.2 |
| 4 | Negativas de la guardia: PARADA, o la forma que propone, declarada | Hecho | §7 |
| 5 | CI con `gh run view` suelto | Hecho | «Base…»; §9 |
| 6 | La cruda no la lee nadie; fotogramas solo por instante localizado | Hecho: ninguno abierto | §0.1, §2.5 |
| 7 | `corpus/Estrategia del trader/` solo en su primer nivel | Hecho | §0.3 |
| 8 | Consultas de `casos_ocultos` y lecturas de la filtrada, declaradas el mismo día | Hecho | `HOLDOUT-EXPOSICIONES.md` |
| 9 | Nada escribe mientras corre `make check`; ninguno entre el registro y el alta; PICO DE MEMORIA de cada sello | Hecho | §9 |
| 10 | Aviso y «listo» de Aleks antes de la transcripción | Hecho | §2.2 |
| 11 | El día, con la línea del paso 1, y la desviación declarada | Hecho | §0.2; `HOLDOUT-EXPOSICIONES.md` |
| 12 | Un vídeo sin registrar; duración con ffprobe | Hecho | §0.3 |
| 13 | Preguntas a) a d) antes del registro | Hecho; el limpio y el marcado, después de leer | §0.1 |
| 14 | `HOJA-USADA.md`, recuadro en `PREGUNTAS.md`; gráfico solo como «gráfico N»; la clave fuera | Hecho | `docs/sesion-6/`; §3.3 |
| 15 | Filtrada con `--sesion 06`; el bloque de S-20 y «veinte y N» | Hecho: no hay ni uno ni otro | §2.2, §3 |
| 16 | Registro, `test_inventario`, `corpus inventory` y `check --hashes` | Hecho | §1, §1.2 |
| 17 | Test roto a propósito, y lo que la skill no nombra (`test_guardia_claude`, el dict de `test_cuarentena`) | Hecho | §1.1 |
| 18 | Audio con las formas exactas, WAV fuera del repo; cortes y su puerta | Hecho | §2.1, §2.2 |
| 19 | Bloques en cuarentena sin contenido, en un commit propio del vídeo | Hecho | `d4d33bd` |
| 20 | `frames extract` y `frames check` | Hecho | §2.5 |
| 21 | Barrido en dos pasadas antes de leer | Hecho, sin PARADA | §2.3 |
| 22 | Informe: bloqueantes con `ACTIVAR-A35-A44.md` §1, S-3 con «se congela» aparte, S-18, S-7 a S-12, el resto, S-16 en dos filas, S-23 frente a A-46, «Para cerrar», tabla final | Hecho | §3, §5 |
| 23 | Evidencia fuera de todos los tramos; un id, citado cuando existe; `contradictions` y `validate` en verde | Hecho | §8 |
| 24 | Cobertura de F | Hecho | §4.2 |
| 25 | Preparado para la orden de cierre: F, R4.2, copia de seguridad, lista A.4 | Hecho | §6, §12 |
| 26 | `PROJECT_STATE.md` bajo 25.000 | Hecho | §9 |
| 27 | Sello, push a `fix/sesion-06`, CI de Linux con solo el fallo esperado, número de run | Hecho | §9 |
| 28 | Sin registro de cierre en HISTORIA ni cambios de la Next Action más allá de abrir la rama | Hecho | §6, sin aplicar |
| 29 | Revisor con el informe terminado y su informe pegado al final | Hecho | §11; «Informe del revisor» |
| 30 | «Rama lista para revisión, NO cerrada» | Hecho | «Estado» |

## 11. Lo que se hizo con los hallazgos del revisor

El revisor (subagente `revisor`) revisó `b368016` más el §9, cuatro filas de §10 y «Estado» sin commitear: **eje (a), 0 bloquea, 11
importa y 3 menor; eje (b), 1 bloquea, 6 importa y 2 menor.** Su informe está al final, tal cual salvo lo que se dice allí.
La evidencia commiteada no se edita: cada corrección es un ítem nuevo que supersede, con el mismo tema. Uno por uno:

| Hallazgo | Qué se hizo |
|---|---|
| **b1 (bloquea), la `naturaleza` de v17** | Arreglado en `fuentes.yaml`: dice lo que se preguntó y lo que se enseñó, con los SVG sin su día, según la medida |
| a1, S-3 «se congela» | `ev-v17-001728-b7b9a32c` supersede: la cita llega hasta la duda, confianza media. Propuesta y tabla pasan a «en parte» |
| a2, S-3 la (a) | `ev-v17-001712-dc155b5d` supersede, y `ev-v17-001610-c43239a9`, nuevo, con la condición del bias. §3.1 los recoge |
| a3, S-14 | `ev-v17-005730-76948af1` supersede: la cita llega a «la verdad no», confianza baja. §3.4 lo dice |
| a4, «contra la sesión 4» en S-13 y S-14 | Reescrito en §3.4 y §4.1: caen de un lado de una tensión que ya había |
| a5, S-18 frente a D1 | §3.2 confronta con D1 la condición del «igual» y el «no se repite», y la tabla la recoge |
| a6, S-18, los equals | `ev-v17-012917-46a2c561` supersede: la cita lleva el titubeo y la afirmación ya no dice «la sesión 5». §3.2 y §4.1 |
| a7, S-18 tras un break even | `ev-v17-013806-e8869c2a` supersede: la cita arranca en «Entonces tras un breaker» |
| a8, la paráfrasis de una línea del margen | §3.5 ya no parafrasea: queda sin cita y lo que hay es la declaración de Aleks. **Sin mover a «bloquea»: lo juzga el consultor.** La lectura de esa línea, antes de existir el tramo, en `HOLDOUT-EXPOSICIONES.md` |
| a9, afirmaciones con más que su cita | Las ocho de más peso, superseded: `ev-v17-010321-352430e3`, `ev-v17-004841-7f53bbb0`, `ev-v17-000134-725523bf`, que además trae la respuesta directa a S-1, `ev-v17-002155-f2c95111`, `ev-v17-014103-8cf3e7fb`, `ev-v17-000250-a468bcec`, `ev-v17-000351-331daa6d` y `ev-v17-001543-c92f549c`. **Las quince de «contexto añadido menor» (marco, lado o «gráfico N», que salen de la pregunta) no se tocan**: no cambian lo que dice la cita y cada una lleva su código en `notas` |
| a10, temas que dan por decidido lo que el ítem niega | **No se puede arreglar**: la corrección de un ítem exige el MISMO tema (`CLAUDE.md`, «Regímenes de cambio»). `ev-v17-015726-ce2e42e4` y `ev-v17-015741-8f9fd638` dejan de negarlo en su afirmación, y sus `notas` y este informe dicen que el nombre del tema (`sesgo.toma_de_la_manana_vale_si_continuidad`, heredado de v15) no decide nada; igual `ev-v17-013815-9cf6f076` |
| a11, §4.1.16 | Reescrito, con su marca por esquema |
| a12, S-21, las marcas | Corregidas, y `ev-v17-014945-9e7de278` supersede con el `t0` bueno |
| a13, S-22 | `ev-v17-015404-06ac0e9d` supersede (con b5) |
| a14, «casi toda la sesión» | Quitado: §2.4 dice que no se ha medido |
| b2, S-3 frente a `no_mueve` | §3.1 confronta las tres lecturas y la frase «de M1»; la PARADA es porque no elige |
| b3, S-7 | §3.3 recoge lo que lee sobre el gráfico (37:59–38:51), y «no da un nivel» se ciñe a la respuesta de 44:48 |
| b4, S-23 | «no resuelve» y «no es un REOPEN» se quitan: **a decidir por el consultor**, sin veredicto; se declara que un «en parte» sobre A-46 haría fallar `test_en_parte_no_se_cierra.py`, porque está RESUELTA, y que eso es justo lo que tiene que decidir él (reabrirla o no). `ev-v17-015726-ce2e42e4` y `ev-v17-015741-8f9fd638` supersedan |
| b5, S-22 | «en parte», con la (c) que marcó antes y el «m15» dudoso; «no choca con A-32» se quita |
| b6, S-21 | «en parte», y «en sustancia es la (a)» pasa a ser una lectura dicha como tal |
| b7, octubre y noviembre | Tramo de precaución 0:06:52–0:08:04 en `tramos_no_citables.yaml`, por la respuesta a) (§2.4) y en `HOLDOUT-EXPOSICIONES.md`. **El informe pegado abajo enmascara sus dos frases de ese tramo** |
| b8, el 93:35 | Pasa de §3.3 a §3.6, dicho en S-18 |
| b9, la forma | Hay §11, la tabla de §10 no se parte, y §1.1 lleva la salida de «pasan» |
| Los dos tramos ajenos, con `acordado` de la sesión | Sin cambio; quedan a la vista del consultor |
| La salida de `knowledge validate`, `AVISO: 4 citas localizadas con tiempos de segmento o parciales` | Tras las correcciones son 5. Es un aviso, y `evidence new` y `knowledge validate` dan las citas por buenas; cuáles son no se ha mirado: la cruda no se lee |
| Las tres negativas de la guardia al revisor | Ver §7, punto 8 |

**Después de los arreglos:** `knowledge validate`: `OK: 640 items de evidencia, 0 contradicciones abiertas, historial intacto`;
`evidence contradictions`: `0 contradicciones abiertas`; `make check` sellado, commit y push a `fix/sesion-06`; su run, en el mensaje
final a Aleks (este informe no puede llevar el de su propio commit). No se lanzó otra pasada del revisor: el encargo pide una.

## 12. Para la copia de seguridad A.4: lo nuevo fuera de git

Lo que esta rama dejó en la máquina y no está en el repositorio:
- **El vídeo**, en `corpus/Estrategia del trader/`: `Grabación de pantalla 2026-11-04 142903.mp4` (v17, 7.574.611.265 bytes).
- **La transcripción del corpus**, `data/transcripciones/v17/`: `audio.wav`, `audio.sha256_video` y la carpeta
  `large-v3-int8-float16/` (`cruda.jsonl`, `cruda.txt`, `corregida.jsonl`, `correcciones.jsonl`, `huella.txt`,
  `video.sha256`, `fragmentos/` y `parciales/`).
- **El audio y las salidas del guion**, en `C:\Users\USER\Desktop\sesion-06-audio\`: `sesion-06-v17.wav` (230.374.136
  bytes), `.cruda-NO-LEER.jsonl`, `.cruda-NO-LEER.txt`, `.filtrada.md`, `.registro.txt` y la carpeta `sesion-06-v17-trabajo/`.
- **Los fotogramas**, `data/fotogramas/v17/` (3,5 GB): se regeneran desde el vídeo con `corpus frames extract`, así que
  copiarlos o no lo decide Aleks.

`PREGUNTAS.md` pedía, antes de grabar, la copia de v15 y v16 en ese Drive; este informe no sabe si se hizo: lo confirma Aleks.

## Estado

Extracción terminada el 2026-11-05, con los hallazgos del revisor arreglados o contestados (§11):
- v17 ingerido: registro, audio, transcripción, cuarentena y fotogramas;
- 19 de las 23 preguntas hechas y extraídas con su propuesta, y «Para cerrar»; S-9 a S-12 no se hicieron;
- 65 ítems de evidencia vivos, con las citas fuera de todos los tramos;
- para el consultor: dos PARADAS de §4 de `ACTIVAR-A35-A44.md` (S-2 y S-3), S-23 frente a A-46 y lo de la fecha de los gráficos
  (§4.1, puntos 14 y 15).

Esta rama no resuelve nada. ADR-0083 sigue PROVISIONAL. Rama lista para revisión, NO cerrada.

## Informe del revisor

Revisó `b368016` más el §9, cuatro filas de §10 y «Estado» sin commitear. Pegado tal cual, salvo dos cosas: **las dos frases de b7 van enmascaradas**, porque hoy caen en el tramo de precaución 0:06:52–0:08:04 que su propio hallazgo trajo, y sus niveles de título bajan uno para no romper los `## ` de este informe. Lo hecho con cada hallazgo, en §11. Los ítems que cita son los de `b368016`, antes de superseder, y sus líneas del informe son las de entonces.

### Informe del revisor · trabajo/sesion-06 · 2026-11-05

**Veredicto corto:** la mecánica de la rama está bien: contrato, regímenes, tramos, sellos y CI. La rama no está lista: hay 1 bloquea en el eje (b). Los hallazgos de fondo son propuestas y afirmaciones que dicen más que su cita, sobre todo en S-3, S-14, S-18, S-22 y S-23. No decido ninguna lectura: las señalo para el consultor.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 11 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **S-3, «se congela»: el literal se corta justo antes de la duda.** La propuesta dice «RESUELVE» y «creo: no», y el ítem lleva confianza `alta`. La línea siguiente no se muestra. Además la afirmación dice «no lo vuelve a mover», y la cita solo dice «indiferente». | Informe:324-329; `ev-v17-001728-5c9af43c` (t1 0:17:38). Cita: «No, no, eso ya nos es indiferente. La vela que genere el rompimiento o la toma de liquidez de M15 Tiene que hacerlo con cuerpo». Afirmación: «una vez tomado el alto con cuerpo, una mecha posterior ya no lo vuelve a mover». Filtrada [17:38]: «Las velas que vengan después, no sé si es indiferente» |
| a2 | importa | **S-3, la (a): la afirmación es el enunciado de la pregunta, no la cita, y se omite su condición.** La confianza es `alta`. El informe tampoco recoge «si está conforme al bias». | `ev-v17-001716-c64cb04b`. Cita: «La respuesta es sí, cerró con cuerpo por encima del alto de antes.» Afirmación: «una M1 que cierra con cuerpo por encima del alto de antes, aunque por debajo de una mecha posterior, toma la liquidez». Filtrada [16:13]: «o sea, si está conforme al bias» |
| a3 | importa | **S-14: el literal se corta en «la respuesta es la A» y omite lo que sigue.** Puede referirse al esquema o a la letra, y eso es lo que hay que declarar. La tabla dice «dice (a)». | Informe:479-480, :724; `ev-v17-005730-76652ed8` (t1 0:57:39). Filtrada [57:37] «la A», [57:39] «la verdad no, como lo planteé aquí» |
| a4 | importa | **S-14 y S-13: «contra la sesión 4» y «lo que dijo en las sesiones anteriores» dicen más que sus fuentes.** En la sesión 4 también dijo «La A es verdadera» en la misma frase. En las sesiones 4 y 5 también dijo cerrar. Las respuestas caen de un lado de una tensión que ya existía. | Informe:487, :661, :471-472. `PREGUNTAS.md:353-354` y :316-319; filtrada [57:05]-[57:07] |
| a5 | importa | **S-18: la conclusión sobre D1 pierde la condición que el propio informe cita.** Dice que «casa con lo que hace D1» y la tabla pone «vuelve tras stop y break even si se valida». Pero el trader dijo que hace falta «un igual», que por lo general el mismo punto no se repite y que es «muy difícil». Falta confrontar esto con D1. | Informe:355-358 frente a :373-374 y :717. `ev-v17-013009-5e47afdb`. Filtrada [90:03] «es muy difícil», [90:21] «y no se vuelve a repetir el mismo punto» |
| a6 | importa | **S-18, la corrección de la sesión 5: se presenta como firme y la cita recorta el titubeo.** La confianza es `alta` y la afirmación añade «la sesion 5», que la cita no trae. | Informe:366-369, :665; `ev-v17-012920-3722f822`. Filtrada [89:17] «a lo mejor me habré», [89:28] «pero los break-evens, que raro», [89:32] «bueno, lo he dicho, sí, pero», [89:33] «a lo mejor me habré confundido» |
| a7 | importa | **S-18: la condición clave de un ítem queda fuera de su cita.** La afirmación habla de la «transcripcion» y de «breaker», y la cita no contiene esa palabra. | `ev-v17-013808-19198ce8`. t0 1:38:08, y la línea [98:06] «Entonces tras un breaker en ese punto» queda fuera. Cita: «vuelves a entrar en él la respuesta era sí o sea si cumple los criterios…». Afirmación: «tras un break even en ese punto vuelve a entrar…» |
| a8 | importa | **Paráfrasis de una línea dentro de un tramo no citable.** El informe dice qué contestó el trader de diciembre usando el contenido de [118:26], dentro de 1:58:24-1:58:27. El propio §2.2 dice que esa línea no se cita. `CLAUDE.md`, sobre los tramos: «tampoco se leen». Si el consultor aplica esa regla al segundo de margen, sube a **bloquea**: lo decide él. Aleks da el mismo dato por otra vía. | Informe:181-182 y :624 («Lo que se entiende, sin citar, es que todavía no lo ha grabado»). `tramos_no_citables.yaml:489-495` |
| a9 | importa | **Afirmaciones con un momento o una condición que su cita no trae (punto 10).** Son las de más peso, con las dos frases tal cual en la lista de abajo. | Ver «Afirmación frente a cita» |
| a10 | importa | **Temas que dan por decidido lo que el ítem niega.** `ev-v17-015726-4127fcca` y `ev-v17-015749-e8ff8754` llevan el tema `sesgo.toma_de_la_manana_vale_si_continuidad`, el mismo de `ev-v15-005839-f2e43c27`, cuya afirmación es que la toma vale con continuidad. El primero dice «no dice si la toma de la mañana vale por la tarde». `ev-v17-013815-9cf6f076` lleva `reentrada.caja_se_vuelve_a_trazar` y dice «no dice si es la caja del primer intento o una nueva». | Los tres YAML citados |
| a11 | importa | **§4.1.16: «da por mal planteados» S-2 y S-5 no se sostiene tal cual, y la lista no está completa.** En S-5 también dijo «me gusta este ejemplo» y «está clavado», y «este planteamiento está correcto». S-2 no lleva esquema según HOJA-USADA. S-18 («algo que no me cuadra») y S-14 no aparecen. El informe la usa como guía para rehacer esquemas. | Informe:676-677 y :60-61. Filtrada [24:35]-[24:46], [25:26], [91:05]. `HOJA-USADA.md:65` |
| a12 | menor | Dos marcas desplazadas en S-21: el informe da [109:46] y [109:47], y la filtrada [109:45] y [109:46]. `ev-v17-014946` arranca en 1:49:46 con un texto que empieza en 109:45. | Informe:577-578; filtrada líneas 1511-1512 |
| a13 | menor | `ev-v17-015411-a67c830c` afirma «hasta el nivel mas bajo» sobre un fragmento dudoso del ASR («pues sus rangos al nivel más bajo de aquí»), con confianza `alta`. | El YAML citado |
| a14 | menor | «Compartió su pantalla casi toda la sesión» no tiene medida: no se abrió ningún fotograma y la filtrada no da esa proporción. | Informe:201 |

**Afirmación frente a cita (punto 10, las de más peso, además de a1, a2, a6 y a7):**
- `ev-v17-010321-b5b11bcb`. Cita: «…y saber qué hacer luego, a partir de las 7 a después, pues solo el trazo de liquidez de M15…». Afirmación: «antes de las 7 solo se atiende al bias y al trazo de liquidez de M15». El momento no está en la cita, y es lo que el informe contrapone a `toma_antes_de_la_ventana` (el apoyo literal está en `ev-v17-010424-6d7f2d3f`).
- `ev-v17-004841-b3d07ba4`. Cita: «…pongas la fecha para poder pues yo contemplarlo…». Afirmación: «…; no se le da y no deduce ningun dia». Lo segundo no está en la cita.
- `ev-v17-000152-8a1d398e`. Cita: «Si el trade se pierde o se gana, si se pierde automáticamente y llega al 4.5…». Afirmación: «se mira al acabar el trade…». El momento es una lectura. La respuesta más directa, [01:34]-[01:36] «cerramos nosotros, por lo general si toca ya el stop loss», no se cita en ningún sitio, aunque contesta al primer «Para precisar» de S-1.
- `ev-v17-002155-855bdfeb`. Cita: «en este caso sería la respuesta c y la vela roja nos permitiría…». Afirmación: «en M15 la vela sin cuerpo entre las verdes y la roja no corta». «No corta» no lo dice: es la conclusión (también en informe:343).
- `ev-v17-014103-02e0163f`. La afirmación añade «a continuacion duda del 0 del esquema y va a su grafico», y eso queda fuera de la cita.
- `ev-v17-000250-8c79c37a`. Añade «que no es una medianoche»: inferencia.
- `ev-v17-000353-84052b99`. Añade «si para un viernes»: la cita no lo trae.
- `ev-v17-001543-6393c5b3`. Añade «de la zona de M15 solo con mecha»: la cita no lo trae.
- Con contexto añadido menor (marco, lado o «gráfico N» tomados de la pregunta): `004338`, `004407`, `004910`, `011419` («la caja», donde se preguntaba por «el 1»), `012441`, `012500`, `014603`, `014946`, `001036`, `002217`, `002516`, `002803`, `005554`, `000559` («FX Replay»), `001847`.

Un ítem commiteado no se edita: si se corrige, se supersede. Estos 64 aún no están en `main`, y si se tocan o no lo decide el consultor.

**Comprobado sin hallazgos:**
- **Contrato:** `CONTRATO: 81 ficheros dentro del contrato de trabajo/sesion-06 (riesgo medio, artefacto docs/validation/SESION-06-EXTRACCION.md, tramo 'R4', 7 comprobaciones para el revisor)`.
- **Comprobaciones ejecutadas:**
  - `corpus check --hashes`: OK.
  - `corpus transcript check`: `OK: 18 transcripciones`.
  - `corpus frames check`: `OK: 13 extracciones`.
  - `knowledge validate` a stdout: todo OK, incluido `OK: 622 items de evidencia, 0 contradicciones abiertas`.
- **`make-check.log`:** `3210 passed`, SELLO `b6c7c916…`, que es el árbol de `b368016`, y `PICO DE MEMORIA … 308 MiB`. Los cuatro sellos de §9 coinciden con `git rev-parse <commit>^{tree}`.
- **Trailers:** ningún commit toca `knowledge/spec` ni `knowledge/cases`. Los tres que tocan `knowledge/` llevan `Fuente: ADR-0021`.
- **Holdout:** nada en `knowledge/cases/holdout`. Hay filas en HOLDOUT de los días 11-04 y 11-05. Se declara que no se abrió ningún fotograma.
- **Regímenes:** 66 `A` y nada más en evidencia, transcripciones, fotogramas y manifiestos. Sin cambios en feedback ni en `libros.yaml`. `HISTORIA.md` y HOLDOUT, solo líneas añadidas.
- **Otros puntos:** sin cambios en ambigüedades ni en ADR. Ningún informe cerrado tocado. Ningún sitio nuevo con `cita`. Rutas protegidas intactas.
- **Tramos:** ninguno de los 64 t0/t1 ni ninguna marca citada en el informe cae en los 11 tramos de v17 (comparado a mano, ver «Lo que no pude comprobar»).
- **Citas contra su fuente:** `ev-v15-002029`, `ev-v16-000851`, `ev-v16-003228`, ADR-0084:41-50 y ADR-0085:72-91 sostienen lo que el informe les atribuye. La de `fb-2026-10-04-sesion-04-bbfb5c98` existe. Los literales del informe coinciden con la filtrada salvo a12.

#### Eje (b) · Encargo
Resumen: 1 bloquea, 6 importa, 2 menor. Requisitos: 32 hechos, 3 parciales, 0 no hechos, 1 hecho de otra forma, 2 pendientes de entregar.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base verificada | Hecho | Informe «Base…», no repetible hoy; el log parte de `136280d` |
| 2 | `abrir-rama`: encargo, contrato, Archivo 55 | Hecho | `6c96499` |
| 3 | No resuelve nada; guion sin tocar; ADR-0083 PROVISIONAL | Hecho | Diff sin spec, feedback, cases, engine ni scripts |
| 4 | Negativas de la guardia: PARADA o forma propuesta | Hecho | §7.2 y §7.4 |
| 5 | CI con `gh run view` suelto | Hecho de otra forma, declarado | §9: el número, por la API de check-runs |
| 6 | Cruda, fotogramas, primer nivel | Hecho (por declaración) | §0.1, §2.5, §0.3 |
| 7 | Exposiciones declaradas el mismo día | Hecho | Diff de HOLDOUT |
| 8 | `make check` por fase y sus picos | Hecho | §9; log |
| 9 | «Listo» de Aleks antes de transcribir | Hecho (por declaración) | §2.2 |
| 10 | Vídeo único, ffprobe, fecha | Hecho | §0.3; manifest |
| 11 | Día en False y desviación declarada | Hecho | §0.2; HOLDOUT |
| 12 | Preguntas a) a d) antes del registro | Hecho | §0.1 |
| 13 | HOJA-USADA con su forma, sin citas | Hecho | `HOJA-USADA.md` |
| 14 | Recuadro en PREGUNTAS | Hecho | `PREGUNTAS.md:12-15` |
| 15 | Gráfico solo como «gráfico N», sin día ni clave | Hecho | §3.3 |
| 16 | `--sesion 06`; bloque S-20 y «veinte y N» | Hecho | §3; filtrada [104:13] |
| 17 | `naturaleza` del vídeo entero, con lo enseñado en pantalla | **Parcial** | Hallazgo b1 |
| 18 | `test_inventario`, `inventory`, `check --hashes` | Hecho | Diff; ejecutado OK |
| 19 | Test roto y luego verde; conjunto literal; dict y sonda v18 | Hecho | §1.1; diff de tests. De «pasan» hay recuento, no salida (b9) |
| 20 | Audio, WAV fuera, cortes, puerta | Hecho | §2.1-2.2; `tramos:440-459` |
| 21 | Transcripción, cuarentena y bloques, commit por vídeo | Hecho | `d4d33bd`; `transcript check` OK |
| 22 | `frames extract` y `check` | Hecho | §2.5; ejecutado OK |
| 23 | Solo `A` | Hecho | 66 `A` |
| 24 | Barrido en dos pasadas | Hecho | Reproducido: 9 y 107 líneas, ninguna con mes y día |
| 25 | S-1 a S-4 con `ACTIVAR-A35-A44.md` §1 y S-3 «se congela» aparte | **Parcial** | Forma hecha; S-3 con b2 y a1 |
| 26 | S-18 frente a D1 | Hecho, con a5 a a7 | §3.2 |
| 27 | S-7 a S-12: decisión y línea, sin día | **Parcial** | Hallazgo b3 |
| 28 | Petición de fecha declarada | Hecho | HOLDOUT; §2.4 |
| 29 | El resto en orden; S-16 en dos filas | Hecho | §3.4 |
| 30 | S-23 frente a A-46 | Hecho, con b4 | §3.4 |
| 31 | «Para cerrar» | Hecho, con a8 | §3.5 |
| 32 | Evidencia fuera de tramos; validate y contradictions | Hecho | §8; `validate` ejecutado; `contradictions` negado (abajo), el log da 0 |
| 33 | Tabla de cobertura de F, todas las filas pedidas | Hecho | §4.2 |
| 34 | Preparado para el cierre: F, R4.2, copia, lista A.4 | Hecho | §6, §12 |
| 35 | PROJECT_STATE bajo 25.000 | Hecho | `wc -c`: 22212 |
| 36 | Sello, push y CI con solo el fallo esperado | Hecho sobre `b368016` | Run: `failure`, sha `b3680161…`, rama `fix/sesion-06`; `1 failed, 3162 passed, 47 skipped`; solo `test_state_check_ok_on_real_repo` |
| 37 | Sin registro de cierre ni cambio de F | Hecho | `PROJECT_STATE.md:28` sigue con la F antigua |
| 38 | Informe del revisor pegado y «Rama lista…» | Pendiente | Este informe lo pegas tú |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | **bloquea** | **La `naturaleza` de v17 no describe lo que se enseñó, y la medida ya la dejó atrás.** El encargo la pide «también lo que se enseñó en pantalla: los SVG de los gráficos, sin su día». Dice que los gráficos y los ejemplos no se hicieron, cuando el informe mide que el gráfico 1 se contestó, el 2 quedó a medias, S-5 y S-6 se preguntaron y el trader abrió los gráficos enviados. Tampoco nombra el replay de octubre. El informe no declara esta diferencia. Si es un «falta algo que el encargo pide» o basta con declararlo, lo juzga el consultor. | `fuentes.yaml` (diff), «salvo las de los graficos y los ejemplos, que segun Aleks no se hicieron (lo mide la extraccion)»; informe:56-61, :207-212; encargo:36 |
| b2 | importa | **S-3: «no cae en ninguna de las tres lecturas» dice más de lo que se ha medido.** `PREGUNTAS.md:161` da «la mecha no mueve nada» → `no_mueve`. «Es indiferente», la (a) y que la zona solo se actualice con otra vela ([10:36]) no se confrontan por escrito con `no_mueve`, solo con `cualquier_mecha`. Y la única frase que rellena el blanco de la confirmación, «de M1», se cita sin analizarla. No digo que sea `no_mueve`: digo que el descarte no está hecho. | Informe:311-314. Filtrada [13:19], [18:50]-[18:54] |
| b3 | importa | **S-7 omite lo más usable, y «no marca un nivel» choca con la filtrada.** Sobre el gráfico 1 lee el sesgo y traza liquidez. Sin fotograma no se sabe dónde, pero «no marca un nivel» solo es cierto para la respuesta de 44:48. | Informe:403-404. Filtrada [37:59]-[38:05] «el bias es alcista… tanto para de las 7 a 11 y de las 11 a 3», [38:23]-[38:31] «aquí un trazo aquí otro trazo», [38:51]-[38:56] |
| b4 | importa | **S-23: «no resuelve» y «no es un REOPEN» deciden más de lo que el encargo pide.** El encargo pide decir si contradice A-46. El informe no señala que [117:39]-[117:50] es el blanco de la confirmación («con el mismo sesgo por la tarde, la toma de la mañana…» → «va a depender si se rompe o no el rango»), y que [117:26] contesta a un «Para precisar» que empieza «Si vale» (`PREGUNTAS.md:623`). «No dice si la toma de la mañana vale» es más fuerte que eso. Si eso reabre A-46 es del consultor. | Informe:613-615, :670; filtrada [117:26]-[117:50] |
| b5 | importa | **S-22: «resuelve (b)» omite dos pasajes.** Primero dice la C, y lo de la mecha va ligado a un «M15» dudoso. El informe apoya en eso que «no choca con A-32». | Informe:598-601, :732. Filtrada [112:19]-[112:21] «la respuesta de la C no sé si es indiferente»; [114:04]-[114:11] «no va en m como digo sólo en el contexto de m15 relacional m15 pues con mecha con cuerpo es válido» |
| b6 | importa | **S-21 marcada «resuelve» mientras el propio informe dice que depende de una definición que el trader no comparte.** Hay inconsistencia con S-5. «Que en sustancia es la (a)» es lectura, porque exige «cumplirse los criterios». | Informe:583-585 y :658-659; filtrada [29:54], [110:29] |
| b7 | importa | **Replay de octubre y trade de noviembre: no se dice por qué no van a `tramos_no_citables.yaml`.** La respuesta a) manda declarar no citables los tramos de «cualquier mes que no sea abril, julio del 1 al 17, agosto o enero» si habló de operaciones concretas. Está en HOLDOUT y en §2.3 y §2.4 sin ese razonamiento. Ninguna cita cae ahí. | Encargo:25. Filtrada [06:52]-[06:54] [enmascarado], [07:51] [enmascarado]; informe:195-197, :204 |
| b8 | menor | §3.3 pone [93:35] entre lo que pide para retomar los gráficos, y se dijo en S-18 sobre su esquema. §8 lo clasifica «fuera de la hoja». | Informe:424-426 y :842; filtrada [91:49]-[93:41] |
| b9 | menor | Forma: no hay §11 (de §10 salta a §12), la tabla de §10 se parte con una línea en blanco tras la fila 26, y de «pasan» en §1.1 hay recuento y no salida, cuando el encargo pedía «las salidas». | Informe:908, :914, :127-129 |

**Lo hecho sin que el encargo lo pida:**
- Dos tramos ajenos a la operativa, declarados en §2.4. Su `acordado` es «decision de la sesion» (`tramos:509`, :516): que lo vea el consultor.
- Los ítems «Fuera de la hoja» y §3.6, declarados en §8.
- §6 d), filas propuestas para `ERRORES-RECURRENTES.md`, sin aplicar.

Sin hallazgo por sí mismos.

**Lo que el encargo dice que no se toca:** intacto, según el diff y `contrato_rama.py`.

**FASE 0:** el encargo no la pide. La tabla «El encargo, punto por punto» está en §10. Su fila 3 y su fila 14 son correctas, pero las filas 16 y 22 dicen «Hecho» sin más donde este informe da parcial (mis requisitos 17 y 25).

#### Lo que no pude comprobar
- **`uv run botsito evidence contradictions`:** negado (abajo). Lo sustituye `knowledge validate`: «0 contradicciones abiertas».
- **El cruce mecánico de literales contra la filtrada:** negado por la guardia y no lo rodeé. Comparé a mano las citas del informe y t0/t1 de los 64 ítems. No es una comprobación exhaustiva byte a byte.
- **A qué gráfico se refiere S-7 en 41:23-43:15:** el informe dice que es otra sesión de su julio, y [42:43] «ya no me permite ver más» deja dudas. Sin fotograma no se puede saber.
- **Si un segmento mío leído solapa un tramo por su fin:** la filtrada solo da el inicio. Por eso salté también las líneas vecinas, listadas abajo.
- **`knowledge validate` da `AVISO: 4 citas localizadas con tiempos de segmento o parciales`:** no sé cuáles son, y puede incluir ítems de v17 como `014946` (a12).
- **El «listo» de Aleks, lo que vio en directo, que la cruda no se leyera y que no se abriera ningún fotograma:** solo por declaración.
- **El árbol actual no está sellado:** el informe tiene cambios sin commitear, y `make check` no lo lancé. El siguiente commit necesita su propio sello.
- **`make check` y pytest:** no ejecutados. Evidencia: `make-check.log`.

#### Lo leído de la filtrada (para declarar en `HOLDOUT-EXPOSICIONES.md`, 2026-11-05)
**Antes de leer**, el barrido de `scripts/barrido_dias.py` en sus dos pasadas: 18-31, 9 líneas; 1-31, 107 líneas. Ninguna es un día de un mes fuera de construcción: sin PARADA.

**Leído de `sesion-06-v17.filtrada.md`, por líneas del fichero:** 1-66, 68-83, 85-136, 138-1274, 1286-1392, 1399-1666, 1668-1691, 1693-1710. Es decir, de [00:00] a [119:58], salvo lo de abajo.

**NO leído (ni copiado):**
- línea 67, [03:51];
- línea 84, [04:29];
- línea 137, [07:38];
- líneas 1275-1285, [95:10]-[95:30];
- líneas 1393-1398, [104:17]-[104:30];
- línea 1667, [118:26];
- línea 1692, [119:22].

**Un listado mío por Grep** imprimió solo las marcas de tiempo (sin texto) de varias líneas de esas zonas, para localizarlas.

**No abrí:** ningún fotograma, cruda, libro, caso reservado, `clave.txt`, carpeta de gráficos, registro del guion ni `corpus/`.

#### Comandos ejecutados
1. `git branch --show-current`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `tail -n 15 make-check.log`
4. `uv run python scripts/barrido_dias.py "…/sesion-06-v17.filtrada.md"`, y otra vez con `--desde 1 --hasta 31`
5. `git diff main...HEAD -- knowledge/corpus/fuentes.yaml knowledge/corpus/manifest.yaml docs/validation/HOLDOUT-EXPOSICIONES.md docs/sesion-6/PREGUNTAS.md PROJECT_STATE.md src/botsito/corpus/cuarentena.py tests/unit/test_cuarentena.py tests/unit/test_guardia_claude.py tests/unit/test_inventario.py`
6. `git diff --name-status main...HEAD -- <rutas inmutables y protegidas> | cut -c1-1 | sort | uniq -c` → `66 A`
7. `git log --format='%h%n%B' main..HEAD`
8. `wc -l` de la filtrada
9. **NEGADO** `uv run python -X utf8 -c "<imprime id, t0, t1, cita y afirmacion de knowledge/evidence/v17>"`. Mensaje: «GUARDIA (.claude/hooks/guardia.py) bloquea: el codigo nombra la carpeta C:, que contiene material protegido, y no se puede decidir que abrira dentro. […] Como reescribirlo: rutas LITERALES de ficheros que se puedan leer, o la CLI del proyecto». No se rodeó; es un falso positivo por la etiqueta `C:` de un `print`, y va a la rama de guardias. La evidencia se leyó con Grep y Read.
10. `git rev-parse 6c96499^{tree} b2ddfeb^{tree} d4d33bd^{tree} b368016^{tree}`
11. `wc -c PROJECT_STATE.md`; `grep -n -E "exit=|failed|passed" make-check.log | tail -n 8`
12. `uv run botsito corpus check --hashes`; `corpus transcript check`; `corpus frames check`
13. **NEGADO** `uv run botsito evidence contradictions`. Mensaje: «SOLO LECTURA bloquea: ese subcomando u opcion de `botsito` escribe.»
14. **NEGADO** `uv run botsito knowledge validate > "<scratchpad>/knowledge-validate.log" 2>&1`. Mensaje: «SOLO LECTURA bloquea: redireccion […] escribe un fichero.» Seguí sin redirección, que es lo que pedía ese límite de no escribir: `uv run botsito knowledge validate`.
15. `git diff --stat -- docs/validation/SESION-06-EXTRACCION.md`
16. `gh run view 41976558765 --repo Fibobrioso/Bot-v3 --json …`: 404, nombre de repo supuesto por mí. Repetido sin `--repo`: `conclusion failure`, `headBranch fix/sesion-06`, `headSha b3680161…`
17. `gh run view 41976558765 --log-failed | grep -E " (FAILED|ERROR) |[0-9]+ failed"`
18. `git diff --name-status main...HEAD -- docs/validation/`
19. Además, Read y Grep de: encargo, contrato, informe, skill `ingerir-sesion`, `HOJA-USADA.md`, `PREGUNTAS.md`, `ACTIVAR-A35-A44.md`, ADR-0083, ADR-0084 y ADR-0085 (por tramos), `ambiguedades.yaml` (A-46 y A-53), `parametros.yaml` (opciones), `tramos_no_citables.yaml` (v17), `BARRIDO-SESION-6.md`, HOJA-DE-RUTA R4.2, los 64 ítems de `knowledge/evidence/v17/` y tres ítems de v15 y v16.

**Ficheros relevantes:**
- `C:\Users\USER\Desktop\Bot v3\docs\validation\SESION-06-EXTRACCION.md`
- `C:\Users\USER\Desktop\Bot v3\knowledge\corpus\fuentes.yaml`
- `C:\Users\USER\Desktop\Bot v3\knowledge\evidence\v17\`
- `C:\Users\USER\Desktop\Bot v3\docs\validation\HOLDOUT-EXPOSICIONES.md`

## Orden de cierre (2026-11-05)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/sesion-06 (consultor, 2026-11-05). Cópiala tal cual al final del encargo y del informe, en «Orden de cierre», en su propio commit (sellado), antes del commit del contrato. Después, el ritual de docs/runbooks/RITUAL.md con la skill cerrar-rama, que lanzo yo con /cerrar-rama.
>
> Revisión del consultor: la rama cumple el encargo. Base de cierre: 5bab3ae (make check sellado, 3210 passed; CI de fix/sesion-06 run 41983104063, solo el fallo esperado de state check; los dos datos vienen del informe final de la sesión, no del repo, y el registro del cierre los cita así). Un auditor independiente comprobó sobre 5bab3ae que ninguna cita de v17 cae en un tramo no citable, que no hay ids de caso ni días reservados nuevos en el diff y que las cinco filas de HOLDOUT-EXPOSICIONES están.
>
> 1. Tag: stable/F38m-sesion-06. Comprueba antes que no existe ni en local ni en origin. Mensaje del merge: «merge: trabajo/sesion-06, la sesión 6 ingerida (v17) y su extracción por pregunta».
>
> 2. Decisiones del consultor que el informe deja abiertas (van copiadas aquí para que consten; ninguna cambia la rama):
>    a) a8 (la línea del margen de diciembre): aceptado como está, sin paráfrasis y declarado; no sube a bloquea.
>    b) El mes del replay del tramo de precaución 0:06:52–0:08:04 está nombrado en §2.4, §11 y el informe del revisor mientras el motivo del tramo y la fila de HOLDOUT lo evitan: no es exposición (sin día ni cifra), se deja, y va a la fila como menor.
>    c) Los dos tramos ajenos (1:35:11–1:35:30 y 1:44:19–1:44:30) con «acordado: decisión de la sesión»: los ratifica el consultor en esta orden; el fichero no se toca.
>    d) La fecha de los gráficos NO se pone (regla 2 de SESION-DE-PREGUNTAS.md sigue). Lo que se le dará en la siguiente tanda es contexto: el H4 y los trazos de M15 del bot, que es otro gráfico y se decide en la activación.
>    e) S-2, S-3, S-4, S-23/A-46 y la alternancia se deciden en el encargo de la activación, no aquí.
>    f) «S-22 de la sesión 4» del encargo: error del consultor; era la misma pregunta con el mismo código en la hoja 04 (A-36, RESUELTA), ya cubierta por S-22 de la 6. Nada pendiente.
>
> 3. Hallazgos del consultor que el revisor no vio, para la fila de ERRORES-RECURRENTES (columna del consultor):
>    - (menor, del consultor) el encargo citó «S-22 de la sesión 4» sin leerlo (punto 2.f); lección: un código de sesión se cita leyendo la hoja de esa sesión, nunca de memoria.
>    - (menor) el enmascarado incoherente del mes del replay (punto 2.b).
>    - (menor) 5bab3ae no tiene segunda pasada del revisor ni su sello en el informe; aceptado, lo cita el registro del cierre.
>    Y en la misma fila, lo que §6 d) propone como dos filas: el commit a tramos_no_citables.yaml sin trailer Fuente: que make check no ve hasta el commit siguiente, y la línea de PLANTILLA que abrir-rama no nombra (segunda vez). Lección para la sesión: todo commit que toque knowledge/corpus/tramos_no_citables.yaml lleva Fuente:, y el informe nace con su línea de PLANTILLA.
>
> 4. En el commit del contrato (chore(cierre)), además de lo que manda RITUAL.md:
>    a) PROJECT_STATE.md, Next Action: F se sustituye por el texto a) de §6 del informe, con este añadido al final, antes de «H va después»: «Decisión del consultor (2026-11-05): los gráficos se rehacen SIN fecha; lo que se añade es contexto (H4 y los trazos de M15 del bot), que decide la activación. El trader ofreció un vídeo de cómo mapea (§3.6): si llega, es material nuevo, SIN ABRIR y fuera del repo hasta su rama.» La F de hoy, con su fecha equivocada, se va: no pasa a HECHA (la sesión 6 sigue viva hasta activarse), así que no entra en HISTORIA como HECHA.
>    b) PROJECT_STATE.md, I gana al final: « En la sesión 6 el trader dijo que aún no lo ha grabado con su voz (declaración de Aleks, SESION-06-EXTRACCION.md §3.5).» Q gana al final: « En la sesión 6 no afirmó que la exportación esté en el Drive (§3.5); Aleks se la vuelve a pedir.»
>    c) PROJECT_STATE.md, Technical Debt: la línea de la copia de seguridad se sustituye por el texto c) de §6; y entra: «La skill ingerir-sesion no nombra el trailer Fuente: de tramos_no_citables.yaml y abrir-rama no nombra la línea de PLANTILLA del informe (SESION-06-EXTRACCION.md §7, puntos 1 y 3; segunda vez): rama corta de skills.»
>    d) docs/plan/HOJA-DE-RUTA.md, R4.2: gana la línea de Estado del texto b) de §6. Es un fichero de la puerta del commit del contrato: su línea M está autorizada por esta orden.
>    e) docs/runbooks/ERRORES-RECURRENTES.md: la fila de la rama, con el revisor (1 bloquea, 17 importa, 5 menor en los dos ejes) y el punto 3.
>    Mide PROJECT_STATE con wc -c ANTES de commitear: hoy 22.212; con estas líneas tiene que quedar por debajo de 23.200. Si pasa de 24.000, PARADA antes de recortar nada.
>
> 5. Lo demás, según RITUAL.md: merge --no-ff a main con el mensaje del punto 1, el tag sobre el merge, y el commit de estado, que solo reemplaza Current Branch (main), Current Feature, Stable Main State y Last Stable Commit. Current Feature: «Ninguna rama abierta. trabajo/sesion-06 cerrada en main el 2026-11-05 (stable/F38m-sesion-06): la sesión 6 con el trader (2026-11-04, v17, 1:59:59) ingerida, en cuarentena, con su extracción por pregunta y 65 ítems de evidencia vivos (SESION-06-EXTRACCION.md). Nada resuelto: la activación la decide el consultor.» Stable Main State y Last Stable Commit, con la forma del cierre anterior. Después: make check sellado, push atómico de main y el tag (yo confirmo la regla ask con «1. Yes»), la CI de main con un gh run view suelto, y, con la CI en verde, el borrado de la rama local y de fix/sesion-06 en origin.
>
> 6. Informe final: sha de main y del merge, el tag y a qué commit apunta, el run de la CI de main y su resultado, las ramas que quedan en local y en origin, el tamaño de PROJECT_STATE.md y el siguiente tag (F38n).
