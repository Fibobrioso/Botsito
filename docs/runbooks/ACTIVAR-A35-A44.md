# Activar RN-004 y RN-020 con la respuesta del trader (A-35 y A-44)

Para ejecutarlo minutos después de la reunión con el trader. Desde `trabajo/preparar-a35-a44`
(2026-09-26) activar cada regla es **escribir UN valor y correr UN comando**: el mecanismo ya
está construido y probado; lo único que falta es lo que el trader diga. **Nada de lo que hay aquí
decide por él.** Si su respuesta no encaja en ninguna lectura documentada, se PARA (§4).

Antes, lo que no cambia de `SESION-DE-PREGUNTAS.md`: **pedir permiso para grabar** y que el sí
quede grabado (sin grabación no hay registro, y sin registro no se fija ningún valor); **no mostrar
ningún gráfico de ningún día**; **reconducir la conversación si salen operaciones concretas de
septiembre** (tiene días reservados); y **no abrir el backtest de marzo**, que sigue en el paso 0
de `ENTRADA-MARZO.md`, con PARADA antes del sorteo mientras A-42 no esté RESUELTA.

## 0. El estado de partida, comprobado y no supuesto

```
uv run botsito motor arnes --meses 2026-04 --salida /tmp/x.txt
```
→ Tiene que salir `ERROR: A-35 sin fijar: ...` y código 2, sin escribir nada. Es la prueba de que
el selector sigue UNKNOWN. Con `--diagnostico-a35 <lectura> --diagnostico-a44 sin_tope` corre
etiquetado; eso NO cuenta para nada (`docs/validation/PREPARACION-A35-A44.md`).

Los dos selectores viven en `knowledge/spec/parametros.yaml`, los dos `estado: UNKNOWN`:

| ambigüedad | parámetro(s) | opciones cerradas |
|---|---|---|
| A-35 | `liquidez_m15_pivote_formado` | `inicio_vela_contraria`, `cierre_vela_contraria` |
| A-44 | `perdida_trader_alcance` | `sin_tope`, `dia`, `semana`, `ambos` |
| A-44 | `perdida_trader_magnitud` | `saldo`, `equity` |
| A-44 | `perdida_trader_unidad` | `porcentaje`, `usd` |
| A-44 | `perdida_trader_dia_usd`, `perdida_trader_semana_usd` | decimal, solo con `usd` |
| A-44 | `perdida_trader_reinicio_huso` | nombre IANA; si el trader no lo dice, se queda UNKNOWN y el motor usa el corte del perfil marcándolo SUPUESTO |

## 1. Qué escribe cada respuesta posible

**Una respuesta, un registro de feedback**, con la cita copiada de la transcripción CRUDA
(`data/transcripciones/<vN>/<modelo>/cruda.txt`) y su tramo. El registro sobre la AMBIGÜEDAD es el
que la cierra (ADR-0022); el registro sobre cada PARÁMETRO es el que `feedback apply` lleva al
registro (ADR-0012 §7). Los dos van en el mismo commit con `Fuente:` y los ids `fb-*` nuevos.

### A-35 · «¿en qué momento das un alto o un bajo de M15 por bueno?»

| lo que dice el trader, en sustancia | valor que se escribe | dónde |
|---|---|---|
| en cuanto empieza la vela contraria, aunque siga en curso («apenas se inicia», v4 #942) | `inicio_vela_contraria` | `liquidez_m15_pivote_formado` |
| cuando la vela contraria ya cerró («uno ya formado», v4 #846) | `cierre_vela_contraria` | `liquidez_m15_pivote_formado` |
| **otra cosa** (por ejemplo, un número de velas a cada lado, o «cuando el precio ya lo probó») | **NINGUNO: PARAR, §4** | — |

Y la segunda mitad de la pregunta, **«¿qué haces si después el precio lo supera un poco?»**, NO
tiene parámetro hoy: se registra como respuesta a A-35 y se lleva al consultor con los candidatos
de `PREPARACION-A35-A44.md` §5 (la mecha de la vela contraria, el doji, la vela en curso que
vuelve a su color, y qué vela cierra con cuerpo, M1 o M15). El mecanismo actual tiene esas cuatro
cosas fijas y visibles en `domain/pivotes_m15.py` y `engine/primitivas.py`; si el trader las
contradice, se abren como ambigüedades nuevas, no se ajustan por lo bajo.

Los dos registros (la ambigüedad y el parámetro):

```
uv run botsito feedback new --sesion <AAAA-MM-DD-sesion-02> --fecha <AAAA-MM-DD> --medio video \
  --grabacion "<ruta en el corpus>" --t0 <h:mm:ss> --t1 <h:mm:ss> \
  --objetivo-tipo ambiguedad --objetivo-id A-35 --accion RESOLVE_UNKNOWN \
  --respuesta "<literal de la cruda>" --registrado-por Aleks \
  --recibido-el <AAAA-MM-DD> --procedencia trader_grabado

uv run botsito feedback new --sesion <AAAA-MM-DD-sesion-02> --fecha <AAAA-MM-DD> --medio video \
  --grabacion "<ruta en el corpus>" --t0 <h:mm:ss> --t1 <h:mm:ss> \
  --objetivo-tipo parametro --objetivo-id liquidez_m15_pivote_formado --accion RESOLVE_UNKNOWN \
  --respuesta "<literal de la cruda>" --valor <inicio_vela_contraria|cierre_vela_contraria> \
  --registrado-por Aleks --recibido-el <AAAA-MM-DD> --procedencia trader_grabado
```

### A-44 · «¿hay alguna pérdida a partir de la cual dejas de operar? ¿cuándo vuelves a contar?»

| lo que dice el trader, en sustancia | valores que se escriben |
|---|---|
| **no tiene tope**, sigue operando | `perdida_trader_alcance: sin_tope`. Nada más: es una respuesta válida y RN-020 nunca bloquea. OJO: contradice la sesión 1 (`perdida_maxima_diaria` 4,5 % y `perdida_maxima_semanal` 9 %, CONFIRMED). No se toca ninguno de los dos aquí: se registra como RESOLVE_CONTRADICTION sobre cada uno y lo decide el consultor |
| un tope **al día** | `perdida_trader_alcance: dia`, más magnitud y unidad (abajo). La cifra del día ya está: `perdida_maxima_diaria` (4,5 %) si es porcentaje; si la da en dinero, `perdida_trader_dia_usd` |
| un tope **a la semana** | `perdida_trader_alcance: semana`, más magnitud y unidad. La cifra: `perdida_maxima_semanal` (9 %) o `perdida_trader_semana_usd` |
| **los dos** | `perdida_trader_alcance: ambos`, y las dos cifras según la unidad |
| la pérdida es **sobre lo cerrado** («lo que he perdido», «el saldo») | `perdida_trader_magnitud: saldo` |
| la pérdida **cuenta lo abierto** («si voy perdiendo con la posición abierta también») | `perdida_trader_magnitud: equity` |
| la cifra es un **porcentaje** | `perdida_trader_unidad: porcentaje` (las bases ya están CONFIRMED: día sobre el saldo inicial del día, semana sobre el saldo actual) |
| la cifra es **dinero** | `perdida_trader_unidad: usd` y la cifra en `perdida_trader_dia_usd` / `perdida_trader_semana_usd` |
| **cuándo vuelve a contar**: «al día siguiente», «a medianoche», sin más | `perdida_trader_reinicio_huso` se queda UNKNOWN: el motor usa el corte del perfil (la medianoche de `firma_huso_corte`) y la traza lo marca SUPUESTO |
| **cuándo vuelve a contar**, con un reloj concreto («a las 12 de la noche de aquí», «cuando abre Nueva York») | `perdida_trader_reinicio_huso: <IANA>` si es una medianoche de un huso nombrable; si no es una medianoche, **PARAR, §4** |
| un tope distinto de los de la sesión 1 (otro porcentaje, otra base) | **no se sobrescribe aquí**: CORRECT sobre `perdida_maxima_diaria` / `_semanal` / `base_calculo_*`, y lo revisa el consultor antes de `feedback apply` |

Un registro por parámetro que la respuesta fije, con `--objetivo-tipo parametro --objetivo-id
<nombre> --valor <valor>`, más el registro sobre `A-44` con `--objetivo-tipo ambiguedad`. La
respuesta a una pregunta compuesta suele fijar tres o cuatro parámetros: son tres o cuatro
registros con la misma cita y el mismo tramo.

## 2. El comando, y el test que tiene que pasar

```
uv run botsito feedback apply --sesion <AAAA-MM-DD-sesion-02> --check
uv run botsito feedback apply --sesion <AAAA-MM-DD-sesion-02>
```
→ `--check` lista lo que escribiría; sin `--check` reescribe `knowledge/spec/parametros.yaml`
(cada parámetro pasa a CONFIRMED con su `fuente: feedback` y su `fb-*`). Después, siempre:

```
uv run botsito spec manifest --escribir
uv run botsito spec docs --escribir
uv run botsito motor arnes --salida arnes-activado.txt
```
→ El manifiesto: **sube `spec_version`** antes (un valor nuevo es un parche: `13.2.0` → `13.2.1`)
y regenera. El arnés a secas, **sin `--diagnostico-*`**, tiene que CORRER: si sale «A-35 sin
fijar» o «A-44 sin fijar», falta un valor. Si sale «ya esta fijado ... no admite --diagnostico»,
sobra la opción de diagnóstico: quitarla. La corrida a secas ya cuenta y su fichero no lleva
etiqueta. Con `--simular` corre además la cuenta (ADR-0053), y RN-020 se evalúa con la pérdida
real del bot.

Los tests que tienen que pasar, por respuesta:

| respuesta | tests |
|---|---|
| A-35, cualquiera de las dos lecturas | `uv run pytest tests/unit/test_pivotes_m15.py tests/unit/test_preparar_a35.py -q` (el test «con el valor fijado el diagnóstico se rechaza» es exactamente lo que ocurre ahora con el registro real) |
| A-44, `sin_tope` | `uv run pytest tests/unit/test_preparar_a44.py -q` |
| A-44, un valor concreto | `uv run pytest tests/unit/test_preparar_a44.py tests/unit/test_cableado.py -q` |
| siempre, antes del commit | estadiar → `make check > make-check.log 2>&1` → `grep SELLO make-check.log` → commit |

**Dos tests cambian de sentido al activar y hay que tocarlos a propósito, no por accidente:**
- `tests/unit/test_preparar_a35.py::test_la_cli_se_niega_sin_lectura_y_no_escribe_nada` y
  `tests/unit/test_preparar_a44.py::test_la_cli_se_niega_sin_a44_aunque_a35_vaya_en_diagnostico`
  comprueban la negativa con el registro REAL sin fijar: con el valor puesto pasan a comprobar el
  rechazo del diagnóstico (mismo mensaje que el test del registro sintético). Se reescriben con
  ese sentido y se dice en el commit.
- `tests/unit/test_visor.py::test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos` corre
  hoy con `--diagnostico-*` porque a secas se niega; activado, vuelve a correr a secas y la página
  vuelve a llamarse `<caso>.html`.

## 3. Cerrar la ambigüedad: los cuatro sitios, y los dos tests que los congelan

Con el registro `fb-*` sobre la ambigüedad hecho (`CLAUDE.md`, «Cerrar una ambigüedad toca cuatro
sitios»):

1. `knowledge/spec/ambiguedades.yaml`: `estado: RESUELTA` en A-35 (o A-44), y una nota con el
   `fb-*` y el tramo. Los `parametros` ya están listados.
2. La tabla «Known Ambiguities» de `PROJECT_STATE.md`: el estado de la fila (mismo id y título).
3. La regla de la spec que la citaba: RN-004 y el token `liquidez_m15` (A-35), RN-020 y los
   acumuladores `perdida_dia` / `perdida_semana` (A-44) llevan notas que dicen «hasta que el trader
   responda»: se actualizan citando el `fb-*`. Cambiar solo notas es un parche de versión.
4. `uv run botsito spec docs --escribir` (los cuatro documentos de `docs/spec/` se regeneran).

Y los tests que congelan el estado, que tienen que cambiar EN EL MISMO COMMIT:
- `tests/unit/test_kit.py::test_ambiguedades_reales_y_esquema`: el conjunto de bloqueantes
  ABIERTAS (`{"A-21", "A-35", "A-42", "A-44"}`) pierde la que se cierra, y el conjunto de RESUELTAS
  la gana.
- La hoja de la sesión 02 (`scripts/hoja_preguntas.py`, `ORDEN_SESION_02`, y su test
  `tests/unit/test_hoja_preguntas.py`): una RESUELTA hace fallar la hoja a propósito; se quita del
  orden en los dos sitios.

Commit con trailer `Fuente:` que cite los `fb-*` nuevos (y ADR-0045 / ADR-0053). El cierre en
`main` lo hace el ritual, con la orden de Aleks (`RITUAL.md`).

## 4. Si la respuesta no encaja en ninguna lectura documentada: PARAR

No se fuerza en la lectura más cercana. Se hace esto, y nada más:

1. Se registra la respuesta como feedback sobre la ambigüedad (**RESOLVE_UNKNOWN** con la cita
   literal), sin registro sobre ningún parámetro: la ambigüedad sigue ABIERTA con la nota «responde,
   pero con una lectura que la spec no tiene», y el tramo.
2. Se apunta la lectura nueva **con su fuente** (la cita de la cruda y el tramo) en
   `docs/validation/PREPARACION-A35-A44.md` §5 como candidata, y en el informe de la sesión.
3. **Se avisa al consultor.** Añadir una opción al enum (`opciones` del parámetro en
   `parametros.yaml`, y el mecanismo que la lea en `domain/pivotes_m15.py` o
   `engine/tope_trader.py`) es decisión suya, con su ADR si toca la forma de la spec.
4. Mientras tanto, el motor sigue negándose a secas y corriendo solo en diagnóstico etiquetado:
   es lo correcto, porque el valor no existe.

Lo mismo si el trader responde a medias, con un ejemplo o en dos sentidos (`SESION-DE-PREGUNTAS.md`,
«Después», 7): no cierra nada.

## 5. Después de activar: lo que se mide y lo que se mira

```
uv run botsito motor arnes --salida arnes-activado.txt
diff docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt arnes-activado.txt
uv run botsito motor visor --caso <caso dev de construccion>
```
Con A-35 fijada RN-004 dispara y `liquidez_tomada` aparece en el embudo; lo que sigue parando el
embudo es la geometría de la entrada (`toca_colocar_orden_limite`, A-21 y las demás) y los
cartuchos (`PREPARACION-A35-A44.md` §3). Con A-44 fijada, RN-020 deja de ser hueco. Cobertura 0
sigue siendo lo esperado hasta que la geometría exista: **no es un fallo de la activación**.
