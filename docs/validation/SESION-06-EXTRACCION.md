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
- **Para precisar** (si cierra o la deja seguir cuando la abierta toca ese punto): «[01:52] Si el trade
  se pierde o se gana, si se pierde automáticamente y llega al 4.5, tendríamos que en cierta parte
  parar ese día y continuar al siguiente.»
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
  antes y por debajo de la mecha; ¿ha tomado?): «[16:10] sí, sí claramente» y «[17:16] La respuesta es
  sí, cerró con cuerpo por encima del alto de antes.» Es la **(a)**.
- **El bajo:** «[18:47] es todo igual pero al revés».
- **La confirmación final**, a medias: «[18:50] la mecha que mueve mi alto es la» / «[18:52] de» /
  «[18:54] o sea, de M1» … «[19:09] La vela que lo toma tiene que cerrar con cuerpo por encima de el
  alto o el bajo de M15.»
- **Propuesta: RESUELVE EN PARTE, y es PARADA de §4 por la pregunta principal.** «Es indiferente» no
  cae en ninguna de las tres lecturas de `liquidez_m15_mecha_que_vuelve` (`solo_la_contraria`,
  `cualquier_mecha`, `no_mueve`; hoy `cualquier_mecha`, lectura del consultor). Lo que dice junto con
  la (a) es difícil de casar con `cualquier_mecha`, y tampoco elige otra: no se fuerza. **Y la (a)
  contradice lo que hace hoy el bot**: `PREGUNTAS.md`, S-3, dice que con (a) la decisión de ADR-0084 «no
  se sostiene y hace falta ADR». **Decide el consultor.**
- **Frente a la sesión 5:** allí dijo «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`), y ahora
  que si vuelve es indiferente.
- **Regla general:** sí en la toma con cuerpo; no en qué mecha mueve. **«creo»:** no. **Compra y
  venta:** sí (18:47).

**Por separado, «el nivel se congela al tomarse» (ADR-0084:41-48, decisión del consultor).** A la
pregunta «¿una vez una vela de M1 cierra con cuerpo por encima y toma tu alto, una mecha que venga
después lo vuelve a mover?»: «[17:28] No, no, eso ya nos es indiferente.» / «[17:32] La vela que genere
el rompimiento o la toma de liquidez de M15» / «[17:36] Tiene que hacerlo con cuerpo». **Propuesta:
RESUELVE, y confirma esa parte**: tras la toma, una mecha no mueve el nivel. La otra mitad de la
decisión (la M1 que cierra con cuerpo sobre el nivel ORIGINAL ya no es toma si una mecha anterior lo
movió) es la que contradice la (a) de arriba. **El bajo en espejo** (ADR-0084:49-50) queda confirmado
por 18:47. **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí.

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
- **Propuesta: RESUELVE.** Marca (c), y su contenido es: la vela sin cuerpo no corta la racha y el alto
  es el punto más alto, también su mecha. **Va contra el bot**: hoy M15 usa `corta_la_racha`, que es la
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
- **Corrige lo que dijo en la sesión 5:** la duda de quitar la condición cuando hay break even
  (`ev-v15-002029-1ac081ae`) no era del break even: «[89:20] equivocado y no quise decir breakeven» /
  «[89:21] eran los equals, o sea los equals» / «[89:23] más que nada cuando hay equals» / «[89:25] o
  sea, eso quería replantearme». Y sigue pendiente de medir: «[88:31] … pero por ahora todavía lo
  trabajamos» / «[88:34] tendría que ser un backtest como digo» / «[88:35] de los peores meses».
- **¿Da la regla que D1 necesita?** D1 pide cuántas veces reentra, si la caja es la del primer intento
  o una nueva y qué hace tras un break even (recuadro del 2026-10-26 de ADR-0083).
  - **Reentra tras un stop y tras un break even, si el punto se vuelve a validar:** casa con lo que hace
    D1 (el llenado no gasta el punto; la reentrada por la vía normal, D5).
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
- **Sus reservas:** no ve claro M15 en el gráfico («[39:49] … aquí está definido muy bien, o sea, la zona
  lineal de M15, pero aquí no se puede definir muy bien …») y, para explicarlo, va a su gráfico de julio
  y escoge otra sesión (40:11–41:23), con lo que lo que dice en 41:23–43:15 es de esa sesión, no del
  gráfico 1. De la sesión de las 11 del gráfico 1 solo supone: «[44:07] … y después el de las 11 el de las
  11 pues en m1 pues» / «[44:19] posiblemente también ha habido break events y eso no algún los pero no no
  me dice en qué sesión …».
- **«¿Qué habrías esperado ver?»:** lo de siempre (44:38–44:48). **«¿Dónde marcarías tu liquidez?»:**
  no marca un nivel; da una sugerencia para el bot (§3.6).
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
que pide el trader para retomarlos:** la fecha, los criterios del bot, los trazos de M15 y más contexto
(«[93:35] a ver lo que me gustaría que hagas es que en cierta parte también me des un contexto un
poco» / «[93:41] más claro …»). Lo de la fecha va al consultor (§4.1).

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
  imbalance. **Contradice lo que está fijado**: `break_even_condicion` = `tocar`, CONFIRMED, y lo que dijo
  en las sesiones anteriores (`ev-v6-005701-7ae2b8d3`, `ev-v15-013605-c041b814`). No se cierra aquí.
- **Regla general:** sí, con dudas sobre los ejemplos. **«creo»:** no, pero «me he puesto a dudar».
  **Compra y venta:** no contesta (los ejemplos van en los dos sentidos).

#### S-14 · La orden sin llenar cuando el precio toma otra liquidez de M15 · A-53

- **Tramo:** 56:37–60:09.
- **La letra:** «[57:30] Tomar la liquidez más reciente» / «[57:32] O sea, la quito en ese momento» /
  «[57:34] Y espero el punto de la liquidez nueva» / «[57:36] O sea, la respuesta es la A».
- **Al explicarlo sobre el dibujo:** «[58:46] … este es el punto nuevo más» / «[58:57] tarde y este sería
  el que todavía seguiría activo porque para nosotros poder actualizar nuestro» / «[59:02] punto break
  posible mundo breaker tendríamos que esperar a que el precio llegue rompa allí». **Para precisar:**
  «[59:14] … a es igual en compra y en venta o sea con lo explicado aquí sí o sea pero al revés y» /
  «[59:21] si antes de que aparezca el nuevo punto el precio toma todavía otra liquidez pues se va
  actualizando».
- **Propuesta: RESUELVE EN PARTE.** Dice la letra (a), `se_retira`, contra la sesión 4 y contra lo de hoy
  (`se_mueve`), y su explicación va hacia (b): el punto anterior sigue activo hasta que rompa. En la
  confirmación, «la orden siempre se va a ir actualizando» (59:31). **La letra, por fin dicha, no casa con
  lo que explica.** Decide el consultor.
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
- **La respuesta:** «[109:46] esta alternancia, o sea» / «[109:47] la respuesta sería C» / «[109:47] o sea, y
  seguir, o sea» / «[109:50] el flujo, o sea, que apenas toque nos activa» / «[109:52] la entrada y después» /
  «[109:53] haga lo que tenga que hacer …», y la confirmación: «[110:29] Entonces, si el punto se rompe con la
  mecha después de una alternancia, pues, como digo, o sea, que ocurra lo que tenga que suceder, pero claro, antes
  de eso tiene que cumplirse los criterios de validar el posible punto breaker correctamente, tener la order stop y
  la caja, …». **«¿Cambia algo si es de una sola vela?»:** «[110:06] me salta esta pregunta porque».
- **Propuesta: RESUELVE: (c), que en sustancia es la (a)**: con el punto validado y la orden puesta, entra. **Va
  contra el bot**, que hace (b) por RN-009; es la fila DISTINTO de ADR-0085:87-91. Depende de qué llame él
  alternancia (S-5).
- **Regla general:** sí. **«creo»:** no. **Compra y venta:** sí (110:02).

#### S-22 · Para que el máximo de la verde sea tu punto, ¿qué tiene que hacer la roja?

- **Tramo:** 110:47–114:48.
- **La respuesta:** tras decir que falta contexto («[112:25] aquí falta un poco más» / «[112:27] de contexto …»):
  «[113:07] porque tendría que el precio haber roto aquí» / «[113:10] con cuerpo o con mecha» / «[113:12] cualquiera
  de los dos para yo poder validar este punto breaker» y «[113:18] la roja cierra dentro de la verde sin pasar su
  mínimo» / «[113:23] pues en este caso no podríamos nosotros» … «[113:29] no podríamos nosotros trazar aquí» /
  «[113:31] como un punto breaker …». **La confirmación:** «[114:11] … el máximo de la vela verde es mi punto cuando
  la roja de» / «[114:18] después haya roto haya roto con mecha con cuerpo pues sus rangos al nivel más bajo de aquí».
  **El flujo bajista:** «[113:49] pensé» / «[113:49] que venía de un flujo bajista aquí»: lo da por supuesto.
- **Propuesta: RESUELVE: (b) en la forma de romper**: tiene que pasar por debajo, con mecha o con cuerpo; no le hace
  falta «cerrar». **Va contra el motor**, que forma el punto con cualquier roja que cierra tras una racha verde
  (ADR-0085:79-83, decisión del consultor), y **no choca con A-32** («en M1 la mecha siempre vale»): la mecha le
  sirve. Es lo que `ev-v15-004037-a2ab3980` decía y no se aplicó.
- **Regla general:** sí. **«creo»:** no; dudas sobre el esquema. **Compra y venta:** no lo dice.

#### S-23 · Una toma de la mañana, y por la tarde el mismo sesgo · A-46 (RESUELTA)

- **Tramo:** 114:48–118:19.
- **La respuesta:** contesta sobre el sesgo de H4 y el rango, no sobre la toma: «[115:39] … para cambiar de sesgo a
  bajista, en este caso, tendría que haber una vela roja que haya roto con mecha o con cuerpo, pues, el bajo de la
  vela verde.» Y: «[117:26] Ahora, y si en la mañana ya operaste esa toma, pues si todavía no se rompe el rango que
  tenemos planteado,» / «[117:33] pues seguimos operando, o sea, en este caso sería alcista.»; «[117:49] como digo, o
  sea» / «[117:50] va a depender si se rompe o no el rango» … «[117:57] tiene que ser H4» / «[117:59] para poderlo
  balear, no nos sirve» / «[118:00] M15, tiene que ser H4».
- **Propuesta: NO RESUELVE.** No elige letra ni dice si la toma de la mañana vale por la tarde. «Seguimos
  operando» mientras no se rompa el rango **puede leerse hacia (a)**, y (a) contradiría A-46 RESUELTA, pero no lo
  dice: **no es un REOPEN con esta respuesta, y aquí no se hace ninguno.** A-46 no se toca.
- **Regla general:** no sobre la toma; sí sobre el sesgo. **«creo»:** no. **Compra y venta:** sí («si es bajista,
  pues bajista», 117:36).

### 3.5 «Para cerrar» (sin código de voz)

Se hizo en voz (respuesta c): 118:22–119:28. Lo que dijo, sin decidir nada:

- **Diciembre (NA:I).** La pregunta y el arranque de la respuesta caen en el bloque en cuarentena y su margen
  (1:58:24–1:58:27), y `evidence new` lo rechazaría: **queda sin cita.** Lo que se entiende, sin citar, es que todavía
  no lo ha grabado, que es lo que dice Aleks (respuesta a). Frente a la sesión 5, donde dijo que lo grababa
  (`ev-v16-003228-b515b93e`).
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
- **Una próxima sesión pronto:** Aleks la anuncia por las preguntas pendientes y el trader dice que le va bien
  el fin de semana (119:44–119:54). La grabación acaba a media frase («[119:58] pero antes»).
- **Cómo marcar la liquidez, consejo al bot:** «[45:26] yo suelo utilizar la trendline por defecto …», hasta donde haya
  rompimiento y sin extenderla (45:00–46:08).

## 4. Contradicciones, cobertura de F y cosas que el consultor tiene que mirar

### 4.1 Contradicciones y cosas que mirar

1. **S-2:** la (c) no cabe en `perdida_trader_reinicio_huso`: PARADA de §4 de `ACTIVAR-A35-A44.md`. El reloj que da
   (UTC+2 «si no me equivoco») no es el medido en sus gráficos (ADR-0069).
2. **S-3, la pregunta principal:** «indiferente» no cae en ninguna lectura de `liquidez_m15_mecha_que_vuelve`: PARADA
   de §4.
3. **S-3, el primer «Para precisar»:** la (a) contradice la parte de ADR-0084 que dice que una M1 que cierra con
   cuerpo sobre el nivel original ya no es toma. Pide ADR. La otra parte, que tras la toma no se mueve, la confirma.
4. **S-3 contra la sesión 5:** «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`).
5. **S-4 contra el bot:** la vela sin cuerpo no corta la racha en M15; hoy sí. Sin parámetro.
6. **S-5 y S-21: el trader no comparte la premisa de «alternancia»** y pide que se defina. De eso dependen las dos y
   RN-009, y es lo que más separa al bot de él (`RECORRIDA-CONSTRUCCION.md` §2.6).
7. **S-13 contra lo fijado:** al cierre y con cuerpo, frente a `break_even_condicion` = `tocar`, CONFIRMED.
8. **S-14:** la letra (a) contra su propia explicación, hacia (b), y contra la sesión 4.
9. **S-15 contra lo fijado:** «antes de las 7 solo se usa para trazo de liquidez», frente a
   `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED. No contesta si vale la segunda toma.
10. **S-18:** «las veces que sean necesarias» frente a `cartuchos_max` = 3 por liquidez. Y corrige el
    `ev-v15-002029-1ac081ae`, citado en el recuadro de ADR-0083: su duda era de los equals, no del break even.
11. **S-19 contra el bot:** pone la orden igual; hoy el bróker la rechaza y gasta el punto.
12. **S-20 contra la sesión 5:** la vela de 1 o 2 puntos ahora cuenta en el retroceso (casa con ADR-0085, y lo contrario
    era `ev-v16-000851-f5ae3b6f`).
13. **S-21 y S-22 contra el motor:** ADR-0085:87-91 y :79-83, decisiones del consultor.
14. **S-23:** no reabre A-46, pero el sentido de «seguimos operando» hay que mirarlo.
15. **Los gráficos.** (a) Fueron por WhatsApp, no en la pantalla de Aleks como dice la hoja: el trader tiene los ficheros
    de esos dos. (b) Pide la fecha, y en la llamada queda que se le pondrá (49:46). **Eso va contra la regla 2 de
    `SESION-DE-PREGUNTAS.md`** («sin la fecha visible») y, aunque sean días de construcción, le permitiría buscar el día en
    su replay. **Lo decide el consultor antes de rehacerlos.** (c) No dice si coincide con la línea del marcado en
    ningún gráfico. (d) Pide ver criterios y trazos: es otro gráfico, no este, y `scripts/graficos_sesion.py` no los dibuja.
16. **El trader responde a menudo sobre su gráfico, no sobre el dibujo**, y da por mal planteados los de S-2, S-4, S-5,
    S-6 y S-22, y parcialmente el de S-15. Los que da por buenos: S-1, S-13, S-16 y S-19. Vale para hacer los siguientes.
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
| ADR-0083 D1 | S-18 | en parte: vuelve si se valida, sin número y sin decir qué caja |
| ADR-0084, «el nivel se congela» | S-3 | sí para lo posterior a la toma; lo anterior lo contradice la (a) |
| S-14 de la sesión 5 (por qué no entró) | S-7 a S-12 | muy en parte: gráfico 1 (a), gráfico 2 sin decisión, 3 a 6 sin hacer |
| S-15 de la sesión 5, dibujo 2 | S-5 | en parte: no comparte la premisa |
| S-15 de la sesión 5, dibujo 3 | S-6 | no: dice que no puede responder |
| S-16 de la sesión 5 (el precio más allá del 0) | S-19 | en parte |
| S-11 de la sesión 5 (la toma de la mañana) | S-23 | no: contesta sobre el sesgo |
| S-22 de la sesión 4 (A-36, la orden en el 0 con mecha) | ninguno | **no se preguntó, y el encargo no dice por qué se pide.** A-36 está RESUELTA desde esa sesión (`SESION-04-EXTRACCION.md`, tabla final; `fb-2026-10-04-sesion-04-bbfb5c98`) y no hay nada pendiente de ella en la hoja de ruta ni en `PREGUNTAS.md`: el consultor dirá si se refería a otra cosa |
| La condición de `ev-v15-004037-a2ab3980` (`ACTIVAR-SESION-05-MOTOR.md` §2.4) | S-22 | sí: (b) en la forma de romper, y contra el motor |
| A-46 | S-23 | no se reabre: no resuelve |
| S-19 frente a S-24 de la sesión 5 (la vela de 1 o 2 puntos) | S-20 | sí |

## 5. Tabla final

| Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|---|
| **S-1** | A-44 | v17 | 00:00–02:23 | **resuelve**: (a), solo cerradas = `saldo`, sin PARADA | sí | no | n/a |
| **S-2** | A-44 | v17 | 02:25–04:38 | en parte: (c), al abrir la primera sesión; no cabe en el parámetro: **PARADA de §4** | sí | solo en el reloj | n/a |
| **S-3** | A-35 | v17 | 04:38–19:32 | en parte: «indiferente», **PARADA de §4**; el primer «Para precisar», (a), contradice ADR-0084 | en parte | no | sí |
| **S-3, el nivel se congela** | ADR-0084 | v17 | 17:22–17:38 | **resuelve**: tras la toma una mecha no lo mueve; confirma esa parte | sí | no | sí |
| **S-4** | A-35 | v17 | 19:33–23:58 | **resuelve**: (c), no corta la racha y el alto puede ser la mecha; contra el bot, sin parámetro | sí | no | sí |
| **S-18** | ADR-0083 | v17 | 87:42–100:24 | en parte: vuelve tras stop y break even si se valida; sin número; sin decir qué caja | sí, condicionada | no | no lo distingue |
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
| S-21 | ACTIVAR §3.11 | v17 | 108:02–110:47 | **resuelve**: (c), que es la (a); contra el bot | sí | no | sí |
| S-22 | ACTIVAR-MOTOR §2.4 | v17 | 110:47–114:48 | **resuelve**: (b), romper con mecha o con cuerpo; contra el motor | sí | no; dudas del esquema | no lo dice |
| S-23 | A-46 (RESUELTA) | v17 | 114:48–118:19 | no resuelve: contesta sobre el sesgo; no reabre | no | no | sí, del sesgo |
| Para cerrar | NA:I, NA:Q | v17 | 118:22–119:28 | diciembre, sin cita; agosto, con dudas; lo que dijo, sin decidir | n/a | sí (agosto) | n/a |

Por códigos de la hoja (23): se hicieron 19 y no se hicieron 4 (S-9 a S-12). De esos 19, en filas: **resuelve** 9 (S-1, el nivel se congela,
S-4, S-16 dos veces, S-17, S-20, S-21 y S-22); **en parte** 9 (S-2, S-3, S-18, S-7, S-5, S-13, S-14, S-15 y S-19); **no resuelve** 3 (S-8, S-6 y S-23).

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

## 8. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` (v17) y `manifest.yaml`.
- La transcripción `tr-v17-large-v3-int8-float16-9d44007a` y los fotogramas `fr-v17-db232fc6`.
- `knowledge/corpus/tramos_no_citables.yaml`: 11 tramos nuevos de v17: 3 SIN AUDIO, 6 de cuarentena y 2 ajenos.
- **64 ítems de evidencia** (abajo). `evidence contradictions`: `0 contradicciones abiertas`. `knowledge validate`:
  `OK: 622 items de evidencia, 0 contradicciones abiertas, historial intacto`.
- `src/botsito/corpus/cuarentena.py` (v17 en `SESIONES_EN_CUARENTENA`) y sus tests.
- `docs/sesion-6/HOJA-USADA.md` y el recuadro de `docs/sesion-6/PREGUNTAS.md`.
- `docs/validation/HOLDOUT-EXPOSICIONES.md`: tres filas del 2026-11-04 y una del 2026-11-05.

**La evidencia, por código** (todos llevan `ev-v17-` delante):

| Código | Ítems |
|---|---|
| S-1 | `000218-001b08fb`, `000152-8a1d398e` |
| S-2 | `000250-8c79c37a`, `000321-37cebf44`, `000353-84052b99` |
| S-3 | `001319-419307f6`, `001543-6393c5b3`, `001716-c64cb04b`, `001728-5c9af43c`, `001847-4e7b7c0b`, `001036-e7bdd027` |
| S-4 | `002155-855bdfeb`, `002250-d6ca3ef8`, `002217-af442f84` |
| S-5 | `002516-426ce5b2`, `002803-4c5ea744`, `002954-613d9421` |
| S-6 | `003356-f27b96e3`, `003222-85f12e6b` |
| S-7 | `004338-c8befc62`, `004407-42808be7` |
| S-8 | `004841-b3d07ba4`, `004910-11d48393` |
| S-9 a S-12 | — (no se hicieron) |
| S-13 | `005111-8933dab2`, `005200-4f93afa0`, `005352-cda6245d`, `005454-90ce4feb`, `005554-172ecbb2` |
| S-14 | `005730-76652ed8`, `005846-0891a9c9`, `005914-55580dc0` |
| S-15 | `010321-b5b11bcb`, `010424-6d7f2d3f` |
| S-16 | `010541-05a69879`, `011328-a701a547`, `011254-542726f6`, `011419-0862662c` |
| S-17 | `012500-39e18f12`, `012441-2ade00be`, `012715-8aaaa59f` |
| S-18 | `013939-860b33e0`, `013009-5e47afdb`, `013808-19198ce8`, `013815-9cf6f076`, `012920-3722f822` |
| S-19 | `014103-02e0163f`, `014235-f3375358`, `014350-ec133d13` |
| S-20 | `014603-63d190df`, `014644-674966b7`, `014736-30d2947b` |
| S-21 | `014946-45736f86`, `015029-bc697500` |
| S-22 | `015307-0870a8ca`, `015318-1256caf7`, `015411-a67c830c` |
| S-23 | `015726-4127fcca`, `015749-e8ff8754` |
| Para cerrar | `015829-7ba798f5`, `015854-de425918` (agosto), `000559-5a0a1597` (el replay de agosto, dicho en S-3); diciembre, sin ítem (§3.5) |
| Fuera de la hoja | `013422-7e8af905`, `013755-a08cc10e` (el vídeo de mapeo), `013335-b77b5fa2` (más contexto en los ejemplos) |

## 9. El cierre de la rama: sellos, push y CI

**Los commits**, cada uno con su `make check` sellado:

| Commit | Qué | SELLO (árbol) | PICO DE MEMORIA |
|---|---|---|---|
| `6c96499` | abre la rama: encargo, contrato y Archivo 55 | `d374be36…` | 307 MiB en `test` |
| `b2ddfeb` | registro de v17, en cuarentena; los tres silencios (§7, punto 3) | `2948d728…` | 305 MiB en `test` |
| `d4d33bd` | v17 transcrita, filtrada y con fotogramas; sus bloques en cuarentena | `77aed208…` | 306 MiB en `test` |

Lo que falta de esta sección entra al sellar la extracción.

**`PROJECT_STATE.md`**: 22.212 bytes. La rama no lo toca más que al abrir, y lo preparado en §6 lo deja bajo 25.000.

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

Lo demás del encargo (sello final, push a `fix/sesion-06`, CI y revisor) entra al entregar.

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

EN CURSO: extracción escrita; falta la entrega.
