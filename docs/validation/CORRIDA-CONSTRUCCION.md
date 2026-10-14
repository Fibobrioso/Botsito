# CORRIDA-CONSTRUCCION · R3.1, la corrida del arnés sobre la construcción vigente y la tabla de diferencias

Rama `trabajo/corrida-construccion`, abierta el 2026-10-14 desde `main` en 23316c8 (commit de
estado sobre el merge 87391b7, tag `stable/F37p-entrada-enero`). Encargo:
`docs/encargos/trabajo-corrida-construccion.md`. Tramo: R3 (R3.1 de `docs/plan/HOJA-DE-RUTA.md`;
F de la Next Action). Modelo de la sesión: Fable 5.1, esfuerzo alto (`/model`, comprobado al abrir).

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git rev-parse HEAD main origin/main` → tres veces `23316c8484198a7d11185c48c7e3309411e0bad6`;
  `git status --short` vacío.
- Último tag de `docs/state/HISTORIA.md`: `stable/F37p-entrada-enero`;
  `git rev-parse "stable/F37p-entrada-enero^{commit}"` = `git rev-parse main^1` =
  `87391b7afde1b557122b805f26619a90cf5cd3d6`; `git ls-remote --tags origin stable/F37p-entrada-enero`
  → `3a7e46d1… refs/tags/stable/F37p-entrada-enero`.
- CI de `main` sobre `23316c8484198a7d11185c48c7e3309411e0bad6` por la API de check-runs con el sha
  literal: `python  completed  success` (run 38574376055).
- `git branch --list` → solo `main`; `git ls-remote --heads origin "fix/*"` vacío.

El commit de apertura (e06a71c) lleva el sello de `make check` (2622 passed, exit 0, árbol
`4fcacaef…`, pico 293 MiB).

## 1 · Fase 0 · Inventario sin tocar nada (2026-10-14)

Todo leído en el repo y medido en esta sesión; no se corrió el arnés ni el visor. Un guion de la
carpeta de trabajo (`medir_fase0.py`, fuera del repo) solo imprimió recuentos, parseó los tres
comandos sin ejecutarlos y calculó los nombres de salida. El auditor del encargo corrió en paralelo;
su informe está en §1.h.

### 1.a Los comandos de la fase 2, tal como el parser los acepta

- El subparser `motor arnes` (`src/botsito/cli.py:3079-3095`): `--salida` obligatoria (:3082),
  `--meses` (:3083-3085), `--tracemalloc` (:3086-3091), y después `_opciones_simulacion`
  (:2330-2353: `--simular`, `--depuracion`, `--perfil`, `--fase`) y `_opciones_diagnostico`
  (:2282-2327: `--diagnostico-a35` con `choices=LECTURAS`, `--diagnostico-a44` con
  `choices=MODOS_A44`, `--diagnostico-a47`, `--diagnostico-a27`, `--diagnostico-cuenta-diaria`).
  Las opciones largas del subparser hoy, leídas del parser construido (no de `--help`):
  `--depuracion --diagnostico-a27 --diagnostico-a35 --diagnostico-a44 --diagnostico-a47
  --diagnostico-cuenta-diaria --fase --help --meses --perfil --salida --simular --tracemalloc`
  (13). `LECTURAS = (inicio_vela_contraria, cierre_vela_contraria)`
  (`src/botsito/domain/pivotes_m15.py:44`); `MODOS_A44 = (sin_tope, marcador, marcador_cero)`
  (`src/botsito/engine/diagnostico.py:48`). `--diagnostico-cuenta-diaria` exige `--simular`
  (`cli.py:2250-2251`); los tres comandos lo llevan.
- Los tres comandos parsean y, por `opciones_de_la_corrida` (`cli.py:2218`) frente a
  `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` (`src/botsito/engine/arnes.py:73-75`), el veredicto de
  ADR-0070 verá fuera de la lista:
  1. `arrastrada`: opciones `(--diagnostico-a35, --diagnostico-a44, --salida, --simular)`; fuera
     `--diagnostico-a35, --diagnostico-a44`.
  2. `diaria`: fuera `--diagnostico-a35, --diagnostico-a44, --diagnostico-cuenta-diaria`.
  3. `a35-inicio`: fuera las mismas tres.
  La línea del informe será `habilita medir el conjunto de medida (2026-05) (ADR-0070): no (opción
  fuera de la lista: --diagnostico-a35; opción fuera de la lista: --diagnostico-a44[; …cuenta-diaria])`
  (`arnes.py:348-349`; `criterio_fidelidad.py:196`). Ninguna lleva `--depuracion`, `--perfil` ni
  `--fase`: el perfil efectivo es el único de `knowledge/cuentas/` y la fase la primera, `reto`
  (`cableado.py:436-450`, `:485`).
- **El nombre real que escribirá cada una** (`diagnostico.nombre_etiquetado`, `diagnostico.py:168-184`:
  la marca una vez y cada etiqueta en forma compacta, en el orden de `Diagnostico.etiquetas`,
  `:82-94`: a35, a44, a47, a27, cuenta):
  1. `docs/validation/anexos/CORRIDA-CONSTRUCCION/arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt`
     (ruta absoluta de 138 caracteres en este repo; límite 259, `diagnostico.py:159`);
  2. `…/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (148);
  3. `…/a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (152).
  Cada línea del fichero irá con el prefijo `[DIAGNOSTICO-A35-<lectura>][DIAGNOSTICO-A44-sin_tope]`
  (y `[DIAGNOSTICO-CUENTA-diaria]` en la 2 y la 3), más la cabecera de `_cabecera_diagnostico`
  (`cli.py:2265-2279`, `diagnostico.etiquetar` :129-140).
- **No hace falta `--diagnostico-a27`**: `firma_stops_level_puntos` está CONFIRMED a 0 en el perfil
  (`knowledge/cuentas/ftmo-2step-swing-100k.yaml:431-445`, fuente ADR-0071), y con valor en el
  perfil `construir_motor_cableado` RECHAZA el diagnóstico (`cableado.py:480-484`). **Ni
  `--diagnostico-a47`**: `entrada_tipo_orden` CONFIRMED `stop_en_ruptura`
  (`knowledge/spec/parametros.yaml:808-829`, fuente `fb-2026-09-29-sesion-03-8f091ed8`).
  **A-21 ya no tiene diagnóstico**: el comentario de `cli.py:2295-2296` y `diagnostico.py:28-29`
  y `:61-63` (ADR-0076); `zona_control_limpia` tiene valor (`parametros.yaml:894-`). Y los dos
  diagnósticos que sí hacen falta siguen UNKNOWN: `liquidez_m15_pivote_formado`
  (`parametros.yaml:492-508`, `estado: UNKNOWN`) y `perdida_trader_alcance`
  (`parametros.yaml:1335-1346`, `estado: UNKNOWN`); sin ellos el motor se niega
  (`diagnostico.py:120-126`, `tope_trader.py:146-153`).
- **La carpeta `docs/validation/anexos/CORRIDA-CONSTRUCCION/` NO existe** (medido:
  `is_dir()` False) y `motor_arnes` no la crea: `comprobar_ruta` solo mide la longitud
  (`cli.py:2403-2406`) y `salida.write_text` va al final, fuera del `try` (`cli.py:2472`). Tal como
  está, cada corrida calcularía los cuatro meses y moriría al escribir. Decisión 3.

### 1.b Ticks: cada día dev tiene ticks, y qué hace el cableado con las horas perdidas

- Días `dev` de cada reparto (`knowledge/cases/visto/<mes>/particiones.yaml`, `cupos.dev`):
  enero 21, abril 21, julio 13, agosto 21 (76). Ficheros de ticks por manifiesto
  (`data/manifests/ticks/`, `ruta: ticks/...`): `eurusd-ticks-2026-01-1ce59681` 21,
  `eurusd-ticks-2026-04-1d189bdd` 21, `eurusd-ticks-2026-07-6e7dc7cd` 13,
  `eurusd-ticks-2026-08-75bd3a08` 21. Comparadas fecha a fecha con la asignación `dev` de cada
  mes: **coinciden una a una en los cuatro meses; ningún día dev sin ticks, ningún fichero de un
  día no dev.** No hay PARADA por ticks.
- Horas, por manifiesto (`horas:`): enero presentes 184, perdidas 5, ausentes_404 0, vacías 0
  (189 pedidas: 21 días × 9 horas, `--horas 06-14` inclusivo, ENTRADA-ENERO.md §0.e); abril
  presentes 182, perdidas 7 (189); julio presentes 114, perdidas 3 (117 = 13 × 9); agosto
  presentes 186, perdidas 3 (189). **Total 18 perdidas**, lista en §1.e.
- Qué hace el cableado con una hora perdida: nada por horas. Cada minuto sin ticks cae al
  respaldo M1 en `Mercado.cotizacion` (`src/botsito/engine/llenado.py:93-113`: el último tick
  anterior si lo hay; si no, la última M1 cerrada, bid = cierre y ask = cierre + spread supuesto,
  fuente `respaldo_m1`), y los llenados, stops y objetivos sobre una M1 siguen la regla pesimista
  de ADR-0051 (`llenado.py:160-166`, `:184-220`, `:290-309`). El spread supuesto sale de
  `llenado.yaml` por hora local (`llenado.py:346-354`), medido solo sobre abril y agosto
  (ADR-0051 §6; ENTRADA-JULIO.md:213-214). `MercadoDia.horas_perdidas` se guarda
  (`simulacion.py:62` y `:203`) pero ningún informe lo imprime; el informe de simulación solo
  da «por fuente: respaldo_m1 N» (`cableado.py:670-673`).
- Frente a un **día sin ningún tick**: `MotorCableado.correr_dia` lo rechaza con
  `CableadoError` salvo con `--depuracion` (`cableado.py:157-161`), y `--depuracion` está fuera
  de la lista de ADR-0070 (`test_umbral_mayo.py:178-183`: «no (opción fuera de la lista:
  --depuracion)»). No se da el caso.

### 1.c Calentamiento: qué mes anterior carga cada mes de construcción

- `arnes.dias_de_mercado` (`src/botsito/engine/arnes.py:172-209`): por cada mes de los días,
  carga las M1 de `(_mes_anterior(mes), mes)` si `buscar_manifiesto` encuentra el dataset
  (`:194-199`; sin el anterior, «el calentamiento empieza en el mes»), y agrega H4 y M15 con
  `anclaje_h4` (`:200-205`). Datasets M1 en `data/manifests/` hoy: 2026-01, 03, 04, 05, 06, 07,
  08 y 09; **ninguno de 2025-12** (`git ls-files data/manifests | grep -c eurusd-m1-2025-12` → 0).
  Así que:
  - **enero** calienta desde su propio mes (ENTRADA-ENERO.md §0.f: 0 INSUFICIENTE medido);
  - **abril** carga el M1 de **marzo** (`eurusd-m1-2026-03-989392e8`, en el repo desde 04f1ed9,
    2026-09-24): un mes **reservado entero y sin sortear** (`knowledge/cases/meses_reservados.yaml`;
    `casos_reservados` da 0 para 2026-03 porque no tiene casos);
  - **julio** carga el M1 de **junio** (`eurusd-m1-2026-06-9c45983f`, desde bf9471c, 2026-09-08),
    que tiene **11 días reservados** (`casos_reservados` y `casos_ocultos` por recuento: 11 y 11
    en 2026-06; `meses_libres` → {1, 4, 7, 8, 10, 11, 12}, junio fuera);
  - **agosto** carga el M1 de **julio** (`eurusd-m1-2026-07-aa162170`), 0 reservados; los días
    20 a 31 no tienen libro (R2.4) y no están en ninguna partición.
- **Leer esas velas no es abrir un holdout**: ADR-0021 §1 (`docs/adr/0021-…md:15-19`: abrir es
  leer etiquetas o medir una cifra del bot sobre esos días; las velas no son ninguna de las dos),
  ADR-0033 §4 (`0033-…md:36-45`: «las velas de mercado no pasan por la puerta… Lo que se exige es
  declararlo», por recuento y sin fechas) y CLAUDE.md, «Que se puede mirar y que no», punto 2.
  El arnés no lo declara solo (`dias_de_mercado` no imprime ninguna línea `LECTURA:`; ADR-0033 §4
  solo se lo pide a `kit build` y `kit check`), así que lo declara esta rama.
- **Lo que se declara hoy en `HOLDOUT-EXPOSICIONES.md`** (fila del 2026-10-14), por recuento y
  nunca por fechas: las corridas de la fase 2 leerán, para calentar, el dataset M1 **entero** de
  marzo de 2026 (mes reservado entero, sin sortear: ningún día suyo tiene caso, así que el
  recuento de ADR-0033 es «el mes entero») y el de junio de 2026 (11 días reservados por
  `casos_reservados`: holdout-1 2, holdout-2 4, holdout-3 5, el recuento de la fila del
  2026-10-04), además del M1 de julio y de los cuatro meses de construcción. Ninguna etiqueta,
  ningún libro, ningún precio en ninguna salida: el calentamiento solo produce el sesgo H4 y las
  M15 de los días dev.
- **Hallazgo (importa):** las corridas anteriores ya leían marzo y nadie lo declaró. El M1 de
  marzo entró el 2026-09-24 y el de junio el 2026-09-08; F35-ORDEN-STOP-PIVOTE (2ea0390,
  2026-09-30), BE-AL-TICK (a3f3bde, 2026-10-01) y la corrida de ACTIVACION-A42 §9.5 (fila del
  2026-10-06, que declara solo «las velas M1 de esos días» de abril y agosto) calentaron abril con
  marzo sin decirlo. **Y sigue pasando en cada `make check`**:
  `tests/unit/test_huecos_motor.py:290-337` llama a `arnes.dias_de_mercado` sobre toda la
  construcción con las velas de `data/` presentes, así que cada `make check` lee el M1 de marzo
  (para abril) y el de junio (para julio) sin declararlo. Va a la fila de hoy y a las líneas del
  cierre (G.2).
- **La llegada del M1 de julio NO cambia el calentamiento de agosto respecto a BE-AL-TICK**: el
  encargo parte de una premisa que el repo contradice (auditor, afirmación 28). El manifiesto
  `eurusd-m1-2026-07-aa162170` entró en cce490c (2026-09-04, F15), antes de F35 y de BE-AL-TICK;
  con el manifiesto presente, `arnes.py:194-199` lo carga, y si su fichero hubiera faltado la
  corrida habría fallado (`cargar_serie`). Abril y agosto calientan hoy exactamente igual que
  entonces. Lo que sí separa esta corrida de BE-AL-TICK: el motor desde ADR-0066 (no solo
  ADR-0074 a ADR-0077: también ADR-0067, 0068, 0069 -las sesiones por la rejilla-, 0071, 0073,
  0075, y los casos por la rejilla de `trabajo/cases-rejilla`), y que la **cuenta arrastrada
  recorre los días por fecha** (`validar_meses` ordena, `arnes.py:114`; `cli.py:2447`): enero,
  abril, julio, agosto, con huecos de meses entre medias. En BE-AL-TICK el tramo empezaba en
  abril; ahora empieza en enero, así que las cifras de abril y agosto de la corrida 1 no salen
  del mismo camino de cuenta. La corrida 2 (cuenta diaria) no tiene ese camino.

### 1.d Qué da hoy el informe y cómo se produce la tabla

**Lo que da hoy.** `arnes.informe` (`arnes.py:250-391`): cabecera (motor, conjunto, días,
sesiones), «## Criterio de fidelidad (ADR-0043)» con UNA medida para todos los meses (n trader,
puntuables, fuera, cobertura, precisión, mismo minuto y la línea de ADR-0070), «## Embudo sobre el
grafo de hechos» agregado, «## Reglas disparadas por sesion», «## Avisos de orden», «## RN-003 al
abrir la sesion» y «## Por sesion» (una fila por (día, sesión) con operaciones del trader: `trader
n | bot n | rn003 | hecho:si/no[primitivas] | disparadas`, `:300-304`). Con `--simular`, `cli.py:2453-2454`
le pega detrás `cableado.informe_simulacion` (`cableado.py:611-678`: «## Simulacion», veredicto de
la cuenta, curva de equity, eventos del broker uno a uno con su fuente, peticiones por día frente
a `firma_mensajes_dia_max`, el freno de ADR-0067 y los cierres de ADR-0068). **Lo que falta para
clasificar**: ninguna línea por operación del trader ni del bot, ni las parejas con su Δ, ni la
operación más cercana cuando no hay pareja, ni cifras por mes. El emparejamiento ya existe y es
puro: `criterio_fidelidad.emparejar` y `medir` (`criterio_fidelidad.py:110-156`), que devuelve
`Medida.parejas` con `delta_segundos` y `delta_puntos` por pareja; el arnés lo llama en
`medida_de` (`arnes.py:244-247`). BE-AL-TICK (`BE-AL-TICK.md:98-99`) sacó su volcado con un
envoltorio de `informe_simulacion` fuera del repo: por eso aquí va commiteado.

**Lo que depende del formato o del final del informe, buscado** (grep de `arnes.informe`,
`informe_simulacion` y `LINEA-BASE` en `tests/`, `src/`, `scripts/`, `Makefile` y `docs/`):

| Qué | Dónde | Qué mira | ¿Rompe con una sección nueva al final de `arnes.informe`? |
|---|---|---|---|
| `test_umbral_mayo.py:129-140` (`_linea`) y sus 20 tests | tests/unit | que haya UNA línea `habilita medir` y que sea la última de la sección del criterio (corta en el primer `\n\n` tras el encabezado) | No: la sección nueva va después y no toca el criterio |
| `test_umbral_mayo.py:299-338` | tests/unit | `informe` exige `opciones` y `simulacion`; por `ast`, que `cli.py` llame a `arnes.informe` UNA vez con esos dos argumentos | No, si la sección se escribe dentro de `informe` o en otra función con otro nombre; SÍ si se añadiera una segunda llamada a `arnes.informe` |
| `test_arnes_motor.py:180-201, 310-358` | tests/unit | substrings (`- predicado:… : 1 de 1`, `cobertura: 3/3 (100.0 %)`, `cuantas se paran…\n- ninguna`) y determinismo byte a byte | No (substrings; determinismo se conserva si la sección es determinista) |
| `test_huecos_motor.py:608-641` | tests/unit | substrings de «Avisos de orden» y «RN-003: 2 de 2; 0 de 0» | No |
| `test_cableado.py:497-508, 605-620, 511-541` | tests/unit | determinismo de `informe + informe_simulacion`; substrings de peticiones y freno | No |
| `test_preparar_a35.py:419-450` (lo señala el auditor) | tests/unit | cada línea del fichero etiquetada (corre el arnés real sobre `construccion[0]`) | No, si la sección no lleva líneas vacías sin prefijo: `etiquetar` prefija todas las líneas, incluidas las vacías (`diagnostico.py:134-140`) |
| `ARNES-MOTOR-LINEA-BASE.txt`, `CABLEADO-SIMULADOR-LINEA-BASE.txt`, `HUECOS-MOTOR-LINEA-BASE.txt` | docs/validation (82f3ae2, a0d0599, 7c7fcd3: 25 y 26 de septiembre) | **nada las compara mecánicamente**: `LINEA-BASE` no aparece en tests/, src/, scripts/ ni Makefile (UMBRAL-MAYO.md:267 ya lo midió); se comparan a mano con `diff` (ARNES-MOTOR.md:128-129; ACTIVAR-A35-A44.md:185-186; HER:30 y HER:35) | No rompe nada: un `diff` futuro mostrará la sección como líneas añadidas. Las tres son inmutables por práctica y no se tocan |
| `docs/runbooks/ARNES-MOTOR.md` | runbook | describe las secciones del informe («Cómo leer el embudo») | Hay que añadirle un párrafo (está en `rutas_permitidas`) |

**Propuesta (decisión 0 por defecto, (a)):** una función nueva en `arnes.py`,
`diferencias_por_operacion(corrida, criterio, vocabulario) -> list[str]`, que `informe` añade
como ÚLTIMA sección de su texto, «## Diferencias por operacion (ADR-0043)». No añade ninguna
opción al comando; `cli.py` no se toca; la lista de ADR-0070 no cambia. Con `--simular` la sección
queda ANTES de la cola «## Simulacion» (auditor, afirmación 31), porque esa cola la pega `cli.py`
detrás de todo el informe; ponerla al final del fichero exigiría tocar `cli.py` (decisión 0, (b)).
Contenido, una línea por fila, campos separados por ` | ` como «Por sesion», determinista:

```
## Diferencias por operacion (ADR-0043: 3 puntos, 15 min)
### Resumen por mes (en el orden de construccion)
mes | dias | trader | bot puntuables | bot en dias sin trader | parejas | cobertura | precision
### Embudo por mes: primer hecho que falta en las sesiones con operaciones del trader y sin operacion del bot
mes | hecho[primitivas] | sesiones
### Por operacion (trader primero, bot sin pareja despues; por mes de construccion y por dia)
quien | dia | sesion | lado | instante UTC | entrada | resultado
```

donde `resultado` es, para una operación del trader, `PAREJA bot <instante> <entrada> (Δentrada
+n puntos, Δinstante +m min s)`, o `SIN PAREJA; bot mas cercano en la sesion: <lado> <instante>
<entrada> (Δentrada, Δinstante)` o `SIN PAREJA; ninguna operacion del bot en la sesion`, seguido de
`primer hecho que falto: <hecho>[<primitivas NO_IMPLEMENTADA> | productoras sin cumplirse]` o
`todos los hechos producidos`; y para una operación del bot sin pareja, lo mismo del otro lado
(`trader mas cercano en la sesion` o `ninguna operacion del trader en la sesion` / `en el dia`).
«Más cercano» = el mismo orden del criterio (`criterio_fidelidad.py:13-16`): menor |Δinstante|,
luego menor |Δentrada|, luego el más temprano, sin exigir lado; los Δ van con signo (bot − trader).
Las cifras por mes salen de la MISMA `Medida` global partida por mes: una pareja exige el mismo
día (`compatibles`, `:103-107`) y el voraz global solo compite dentro de un día, así que la
partición por mes es idéntica a medir cada mes aparte. El embudo por mes usa `hechos_de_regla`
y las trazas como «Por sesion» (`arnes.py:282-293`).

**Por qué no el guion en `anexos/`:** volvería a correr el motor fuera de los tres comandos
autorizados, y un guion nuevo de la rama es código sin revisar para la guardia (CLAUDE.md, «Solo
un guion idéntico al de `main`…»; auditor, afirmación 34). La sección en `arnes.py` corre dentro
de los tres comandos, con tests sintéticos que no tocan `data/`.

**Tests de la fase 1** (`tests/unit/test_diferencias_por_operacion.py`, con `arnes.Corrida`,
`ResultadoDia` y `TrazaSesion` sintéticos como `test_umbral_mayo._corrida`): los cuatro casos que
pide el encargo en los dos sentidos (emparejada; a 4 puntos y a 16 minutos sin pareja con su Δ;
sesión sin operación del bot con «ninguna» y el hecho que faltó; bot sin pareja en un día sin
trader), el orden por construcción, el determinismo, y uno que compruebe que las opciones largas
del subparser `motor arnes` son exactamente las 13 de hoy y que `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`
sigue siendo la de la enmienda (la lista de ADR-0070 sigue igual).

### 1.e Las 18 horas de ticks perdidas, por día y hora (UTC)

De los cuatro manifiestos (`horas.perdidas`); todas caen en días `dev`:

| Mes | Horas perdidas | Dentro de la ventana de sesiones |
|---|---|---|
| enero (ventana 06:00-14:00Z, ADR-0069 §5) | 2026-01-05T10Z, 2026-01-14T07Z, 2026-01-20T11Z, 2026-01-23T11Z, 2026-01-29T11Z | 5 de 5 |
| abril (05:00-13:00Z) | 2026-04-03T09Z, 2026-04-06T10Z, 2026-04-07T10Z, 2026-04-22T07Z, 2026-04-22T10Z, 2026-04-22T13Z, 2026-04-23T05Z | 6 de 7: la hora 13Z del 22 es «la ventana más una hora» (ENTRADA-ENERO.md §0.e), después del cierre de la segunda sesión |
| julio (05:00-13:00Z) | 2026-07-10T05Z, 2026-07-14T12Z, 2026-07-16T11Z | 3 de 3 |
| agosto (05:00-13:00Z) | 2026-08-14T07Z, 2026-08-17T11Z, 2026-08-20T07Z | 3 de 3 |

Total 18 (17 dentro de las sesiones). Marcarlas en la tabla desde `arnes.informe` no es posible sin
pasarle los manifiestos o `MotorCableado.mercados` (`cableado.py` está protegido): la propuesta es
que el informe de la rama (este fichero) liste qué filas de la tabla tienen su instante -del
trader o del bot- dentro de una de estas horas, contrastado a mano contra esta lista (decisión 2).

### 1.e2 Tiempo y memoria esperados

- F35-ORDEN-STOP-PIVOTE.md y BE-AL-TICK.md no publican ni tiempo ni memoria (grep de `TIEMPO`,
  `MEMORIA`, `MiB`, `segundos`: nada).
- MEMORIA-SUITE.md:57-61: `motor arnes --simular --diagnostico-a27 0` sobre 42 días, 92,1 s
  después de quitar `tracemalloc` (582,7 s antes); sin `--simular`, 54,5 s y 85,5 MiB de pico del
  proceso (:68-69). CABLEADO-SIMULADOR.md:174-175, antes de memoria-suite: 320,5 s y 247,5 MiB
  con `--simular` sobre 42 días. ARNES-MOTOR.md:46-47: «abril entero tarda unos tres minutos»
  (2026-09-26, con tracemalloc).
- Estimación para 76 días: unos 170 s por corrida si escala con los días (76/42 × 92 s), y más
  si escala con las operaciones (julio trae 67 en 13 días); con ADR-0074 cada orden viva cuesta
  más peticiones y más eventos. Orden de magnitud: 3 a 6 minutos y menos de 300 MiB por corrida.
  Las tres corridas y la repetición de la 2 caben en una sesión (menos de media hora en total),
  sin solaparse con `make check` (que tarda 20 min: 1184 s en el de apertura).

### 1.f Recuentos de partida, contados en el repo

| Mes | Días dev (`particiones.yaml`) | Casos dev con fichero | Operaciones del trader (`- direccion:` en `knowledge/cases/dev/caso-eurusd-<mes>-*.yaml`) |
|---|---|---|---|
| 2026-04 | 21 | 16 (5 días sin operaciones, sin fichero: `arnes.py:156-159` los corre con 0) | 35 |
| 2026-07 | 13 | 13 | 67 |
| 2026-08 | 21 | 19 (2 sin operaciones) | 42 |
| 2026-01 | 21 | 21 | 54 |
| **Total** | **76** | **69** | **198** |

Abril y agosto: 42 días y 77 operaciones, lo mismo que BE-AL-TICK §2. ADR-0079:78 dice 76 días
dev; coincide.

### 1.g Herencias que entran en esta rama

- **HER:25** (PROJECT_STATE.md:72): «RN-004, bloqueada SOLO por A-35»; **HER:30** (:74): «RN-004
  tras A-35, medida con el arnés y mirada con el visor… Desde ADR-0076 el arnés corre con
  `--diagnostico-a35` y `--diagnostico-a44`»; **HER:35** (:76): «RN-020 tras A-44… el modelo es lo
  que hace RN-036». Los tres en las Refs de R3.1 (`HOJA-DE-RUTA.md:113-117`). No se mueven: A-35 y
  A-44 siguen «en parte» (R1.1, :59-61; R4.1, :128-129) y esta corrida es diagnóstico. Lo que la
  corrida dirá de ellos: cuántas sesiones producen `liquidez_tomada` con cada lectura de A-35
  (corridas 2 y 3) y si RN-020 bloquea alguna vez con `sin_tope` (no puede: `A44_SIN_TOPE`
  «RN-020 nunca bloquea», `parametros.yaml:1343`), que es lo que irá a las líneas del cierre.
- **ADR-0074 §3** (`0074-…md:42-60`): «la cadena entera por el cableado real es de la rama de
  motor y de R3.1»; la medida que hereda: peticiones por día con `caja_se_fija =
  en_cada_cierre_m1` frente a los umbrales del freno de ADR-0067 (aviso 1000, corte 1500, bucle 5
  iguales en 1 min: `parametros.yaml:1690-1755`; `test_cableado.py:529`) y a
  `firma_mensajes_dia_max` 2000 (perfil :323-334). F35 §4.3 midió en diagnóstico hasta 14 al día
  y 59 en 42 días con esa lectura (`F35-ORDEN-STOP-PIVOTE.md:217-224`). El informe de simulación
  da el total por día y el máximo (`cableado.py:681-713`) y el freno por día (`:716-733`); el
  total del tramo no lo imprime: se suma de la tabla.
- Otras que nombran R3.1 o «la corrida», encontradas con grep:
  - ACTIVAR-SESION-04-MOTOR.md:252 (h1: ADR-0074 §3 «a las líneas del cierre (R3.1)»; no se
    aplicó en el cierre de esa rama: Refs de R3.1 sin ADR-0074, §1.k) y :989-990 (ADR-0070 §3
    «hoy A-21, A-35 y A-44», lo dice R3.1).
  - ACTIVAR-SESION-04.md:194-198 (cerrar A-21 no habilita R3.1) y :662 («la medida real es
    R3.1»: las peticiones con la caja recalculada).
  - ENTRADA-JULIO.md:125-127 (un día dev de julio sin ticks dejaría sin corrida a R3.1: no pasa,
    §1.b) y :215-218 (`make check` corre el sesgo H4 sobre julio: no es la corrida).
  - ENTRADA-ENERO.md:673 («R3.1 depende de R2 entera») y :752 (la corrida de `ticks_spread.py`
    lee los cuatro meses: no es esta).
  - HOJA-DE-RUTA.md:137 (R4.1 depende de R3.1) y :155-157 (R5.2 depende de una corrida que
    cuente, sin diagnóstico: esta no).
  - ADR-0078:70 y ADR-0079:78 (42 → 55 → 76 días dev «antes de la corrida de R3.1»).

### 1.h El encargo frente al repo (auditor, 2026-10-14)

El subagente `auditor-encargo` contrastó 56 afirmaciones: 40 correctas, 1 incorrecta, 15 con
matiz; y 8 cosas que el repo pide y el encargo no dice. Lo que cambia el trabajo:

| # | Afirmación del encargo | Veredicto | Evidencia y qué se hace |
|---|---|---|---|
| 28 | «la llegada del M1 de julio cambia el calentamiento de agosto respecto a BE-AL-TICK» | **INCORRECTA** | el manifiesto de julio es de cce490c (2026-09-04); §1.c. Se mide lo que sí cambia: motor desde ADR-0066 y el tramo de la cuenta desde enero |
| — | la carpeta de salida no existe y el arnés no la crea | repo | `cli.py:2472`; §1.a. Decisión 3 |
| 31 | «sección al final del informe del arnés» | MATIZ | con `--simular` el final del fichero es `informe_simulacion` (`cli.py:2453-2454`). Decisión 0 |
| 43 | «por corrida y por mes: … cobertura y precisión» y «embudo por mes» | MATIZ | el arnés da una sola medida y un solo embudo (`arnes.py:334-357`) y `--meses` está vetado. La sección trae el resumen y el embudo por mes (§1.d). Decisión 1 |
| 39 | «ordenado por mes en el orden de construccion» | MATIZ | el arnés ordena por fecha (`arnes.py:114`); la sección reordena por `criterio.construccion` |
| 22 | «las 18 horas sobre respaldo M1» | MATIZ | 18 en los manifiestos, 17 dentro de las sesiones (2026-04-22T13Z es la hora de después del cierre). §1.e |
| 21 | «el cableado cubre [las horas] con el respaldo M1 y el spread supuesto» | MATIZ | por minuto, no por hora; `horas_perdidas` no se imprime. §1.b. Decisión 2 |
| 24 | «M1 de 2026-03 y 2026-06, que tienen días reservados» | MATIZ | junio, 11 días; marzo es un mes reservado ENTERO sin sortear (`casos_reservados` 0). La declaración nombra marzo entero. §1.c |
| 35 | tiempo y memoria «de F35, BE-AL-TICK, MEMORIA-SUITE» | MATIZ | solo MEMORIA-SUITE y CABLEADO-SIMULADOR los publican. §1.e2 |
| 5 | «siete ficheros de tests toman construccion[0]» | CORRECTA | ocho ficheros lo nombran; `test_criterio_fidelidad.py:108` solo en un comentario; siete lo usan |
| 11 | «ADR-0070 lo permite para medir» | MATIZ | ADR-0070 no autoriza correr: fija cuándo una corrida habilita. La autorización es el encargo; la repetición de la 2 con otro `--salida` (fase 2) es un cuarto comando que el propio encargo pide: se entiende autorizada por él |
| 46 | «el motor de antes de ADR-0074 a ADR-0077» | MATIZ | BE-AL-TICK (F36h) es anterior también a ADR-0066 a 0069, 0071, 0073, 0075 y a cases por la rejilla. §1.c |
| 48 | «PROJECT_STATE… esta rama no lo toca» | MATIZ | abrir la rama lo tocó (23.624 → 23.773 bytes: Current Branch, Current Feature y Archivo 33), como pide `abrir-rama`; no se vuelve a tocar hasta el cierre |
| 53 | «ACTIVAR-A35-A44.md todavía cita --diagnostico-a21» | MATIZ | en :218, :246 y :260, bajo la NOTA de :196-200 que ya lo da por histórico; y su §5 (:185-186) compara una corrida SIN `--simular` con una línea base escrita CON `--simular`. §1.k |
| 54 | línea del cierre «F pasa a apuntar a V» | MATIZ | V depende también de J (`kit hoja`, PROJECT_STATE.md:52; HOJA-DE-RUTA.md:135-137, :287) y R4.1 de A.4. §1.k |
| 2 | `tramo: «R3 · Una corrida…»` | MATIZ | el contrato lleva `tramo: R3`, el id, que `scripts/contrato_rama.py:123-131` acepta como equivalente |

Lo que el repo pide y el encargo no dice (auditor): (1) la carpeta de salida (decisión 3); (2) la
cuenta arrastrada recorre enero, abril, julio, agosto (§1.c); (3) los 19 casos dev de agosto
salen de un xlsx que el trader no da por bueno (S-16, ADR-0073:70-77; NA:Q): sus diferencias son
candidatas a (M); (4) el simulador no comprueba el margen (HER:37): en la corrida 1 pueden salir
llenadas operaciones que FTMO rechazaría por margen, y el informe lo dirá junto al veredicto de
la cuenta; (5) V depende de J y A.4; (6) y (7) cifras por mes y horas perdidas (decisiones 1 y
2); (8) HER:30 y HER:35 miden «contra la línea base vigente» (`CABLEADO-SIMULADOR-LINEA-BASE.txt`,
42 días): las salidas de esta rama son diagnóstico etiquetado y no pueden ser una línea base
(`diagnostico.py:169-170`), así que no la sustituyen (decisión 4).

### 1.i Lo que no pude medir

- Que las tres corridas lleguen al final sin otro parámetro estricto que se niegue, y su tiempo y
  memoria reales: exige correr el arnés (fase 2).
- Que la guardia de Claude Code y el clasificador dejen pasar los tres comandos: se sabrá al
  lanzarlos; si niegan, PARADA con el comando exacto.
- Cuántas velas de marzo y junio se leen de verdad para calentar: `dias_de_mercado` carga el
  dataset entero del mes anterior (`arnes.py:194-199`); el manifiesto de marzo dice 31 días
  presentes y 31.800 velas (sus 30 primeras líneas, sin fechas de días de mercado), y el de junio
  no lo abrí. Se declara «el mes entero».
- Si los ficheros M1 de 2026-03, 2026-06 y 2026-07 están en disco: no se listó `data/` (la
  guardia lo niega, y no hace falta: si faltan, la corrida falla y es PARADA).

### 1.j Exposiciones de hoy (declaradas en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-14)

- Ningún libro, ninguna imagen, ningún fotograma, ninguna transcripción, nada de marzo, mayo,
  septiembre ni febrero. Los repartos solo por RECUENTO (`casos_reservados` y `casos_ocultos`:
  34 y 34, 11 de ellos en junio; 0 en 2025-12, 2026-01, 03, 04, 07 y 08).
- Leídos: los cuatro manifiestos de ticks de construcción (enteros); las `particiones.yaml` de
  los cuatro repartos dev-visto (solo `dev`, material de desarrollo); un caso dev de enero
  (`caso-eurusd-2026-01-02.yaml`, para ver el formato); las 30 primeras líneas del manifiesto M1 de
  marzo (recuentos de velas y cuatro sábados sin datos; ninguna etiqueta, ningún precio); y un
  `ls data/manifests/` que enseñó NOMBRES de manifiestos (M1 de 2026-01 a 2026-09, sin contenido).
  El auditor contó los M1 con `git ls-files data/manifests | grep -c`, que es la forma que
  ERRORES-RECURRENTES.md prohíbe (filtro detrás de la carpeta madre): solo salió un recuento.
- **La guardia bloqueó una medida legítima** (se declara, no se rodea): el primer guion de la
  fase 0 nombraba `data/manifests/ticks` para cruzar los ficheros de ticks con los días dev y fue
  bloqueado («el codigo nombra la carpeta data»). El cruce se hizo leyendo los cuatro manifiestos
  con rutas literales (Grep) y el guion se reescribió sin esa parte. Propuesta para G.1: que la
  guardia admita en un guion las rutas literales de `data/manifests/ticks/*.yaml` de meses de
  construcción, que Read sí deja abrir.
- Lo que leerán las corridas de la fase 2 (§1.c): el M1 entero de marzo (mes reservado entero) y
  de junio (11 días reservados), para calentar; y la exposición permanente de
  `test_huecos_motor.py:290-337` en cada `make check`, que es la misma lectura.

### 1.k Hallazgos para las líneas del cierre

1. **Refs de R3.1 en `HOJA-DE-RUTA.md:113-114`** sin `ID:ADR-0074` aunque hereda su §3 (h1 de
   ACTIVAR-SESION-04-MOTOR.md:252, no aplicado en ese cierre). Corrección: añadir `ID:ADR-0074 ·
   ID:ADR-0067` a las Refs, y en «Qué es» la frase «y la medida de peticiones por día con la caja
   recalculada (ADR-0074 §3) frente al freno de ADR-0067». Va en el commit del contrato del cierre
   (`docs/plan/` está protegido en la rama).
2. **ADR-0070 §3 (`0070-…md:62`, también :57-58, :129-130 y :149)** sigue diciendo «hoy A-21,
   A-35 y A-44». No se edita en la rama (lo manda el encargo). Corrección propuesta: una NOTA en
   el ADR, en el cierre o en la rama que toque `docs/adr/`: «NOTA (2026-10-14,
   `trabajo/corrida-construccion`): desde ADR-0076 (2026-10-12) A-21 está fijada y
   `--diagnostico-a21` no existe; el motor necesita diagnóstico solo para A-35 y A-44. La corrida
   de R3.1 (CORRIDA-CONSTRUCCION.md) corrió con los dos y dio «no», como dice el punto 3».
3. **`docs/runbooks/ACTIVAR-A35-A44.md`** cita `--diagnostico-a21` en :218, :246 y :260 bajo una
   NOTA (:196-200) que ya lo da por histórico. Corrección: tachar las tres menciones con «(ya no
   existe, ADR-0076)» o reescribir el paso 2 de §6 sin ellas; y además su §5 (:185-186) compara
   `motor arnes --salida` SIN `--simular` con `CABLEADO-SIMULADOR-LINEA-BASE.txt`, que se escribió
   CON `--simular` (CABLEADO-SIMULADOR.md:174-175): el comando del runbook tiene que llevar
   `--simular`. Fuera del contrato de esta rama (solo ARNES-MOTOR.md y ERRORES-RECURRENTES.md
   están permitidos); se propone para la rama que lo toque o para ampliar el contrato si el
   consultor lo decide.
4. **Nuevo:** la lectura del M1 de marzo y junio para calentar, en cada `make check`
   (`test_huecos_motor.py:290-337`) y en toda corrida del arnés, sin declaración automática
   (§1.c). Propuesta para G.2: que `dias_de_mercado` imprima una línea `LECTURA:` por recuento
   como `kit check` (ADR-0033 §4), o que el test lo diga en su docstring y HOLDOUT lo recoja una
   vez como exposición permanente.
5. **Nuevo:** F de la Next Action, al cerrar: «lo siguiente es V (sesión 5) con la lista de (R)
   de CORRIDA-CONSTRUCCION.md §…; antes, J (`kit hoja` con un paquete nuevo), del que V depende, y
   la copia de seguridad A.4 antes de grabar» (auditor, 54).
6. **Fila propuesta para `docs/runbooks/ERRORES-RECURRENTES.md`** (respuesta del consultor,
   punto 8): «`trabajo/corrida-construccion` · El consultor y su auditor dieron por cierto que la
   llegada del M1 de julio cambiaba el calentamiento de agosto respecto a BE-AL-TICK, sin mirar
   cuándo entró el manifiesto (cce490c, 2026-09-04, antes de F35 y de BE-AL-TICK). Lo vio el
   auditor del encargo en la fase 0 (afirmación 28). Lección: un «antes no estaba» se comprueba
   con la fecha de entrada del fichero en git (`git log --format=%ad -1 -- <fichero>`), no con la
   memoria de cuándo se usó». Se escribe en la fase de entrega, con las demás filas de la rama.
7. **Segunda fila propuesta para ERRORES-RECURRENTES** (§3.8): «`trabajo/corrida-construccion` ·
   La sesión escribió un fichero nuevo dentro del repositorio mientras corría `make check` (un
   guion de anexo) y lo sacó en el acto; el sello no se rompió porque la huella se toma al empezar
   y al sellar, pero la regla es «nada escribe mientras corre `make check`», también lo que no está
   seguido. Señal: un Write a una ruta del repositorio con un `make check` en segundo plano. Qué
   hacer: escribir en la carpeta de trabajo y copiar al repositorio cuando llegue el sello».

## Lo que necesito que decidas

0. **Dónde vive la sección «Diferencias por operacion».** Opciones: (a) dentro de
   `arnes.informe`, como última sección de SU texto: `cli.py` intacto, ninguna opción nueva, el
   test por `ast` de `test_umbral_mayo.py:307-338` sigue igual; con `--simular` queda antes de la
   cola «## Simulacion» (eventos del broker, peticiones, freno, cierres). (b) una función aparte,
   `arnes.diferencias_por_operacion`, que `cli.py` pega DESPUÉS de `informe_simulacion`, al final
   del fichero: toca `cli.py` (una llamada; hay que sacarlo de `rutas_protegidas` del contrato) y
   el diff de `src/` del revisor cubre dos ficheros. Recomiendo (a): la sección se encuentra por
   su encabezado y nada del contrato ni de la lista cerrada se mueve. Coste de (b): ampliar el
   contrato y tocar el comando que ADR-0070 vigila.
1. **El resumen y el embudo por mes.** Opciones: (a) van en la sección, calculados en `arnes.py`
   desde la misma `Medida` global partida por mes y desde las trazas (§1.d), con tests
   sintéticos; (b) no van en la salida: el informe de la rama los deriva a mano de la tabla.
   Recomiendo (a): deterministas, commiteados y comprobables por el revisor. Coste de (b): cifras
   escritas a mano, sin test.
2. **Las horas perdidas en la tabla.** Opciones: (a) la tabla no las marca; el informe de la rama
   lista las filas cuyo instante cae en una de las 18 horas de §1.e, cruzado a mano (18 horas
   contra unas 200 filas); (b) pasar `horas_perdidas` de `MotorCableado.mercados` a la sección
   desde `cli.py` (toca `cli.py`, y en una corrida sin `--simular` no existe). Recomiendo (a).
   Coste de (b): `cli.py` en el contrato y una firma de `informe` con un argumento que solo vale
   con `--simular`.
3. **La carpeta de salida.** Opciones: (a) la fase 1 commitea
   `docs/validation/anexos/CORRIDA-CONSTRUCCION/README.md` (qué es cada fichero y los tres
   comandos literales), así la carpeta existe antes de la fase 2 y git la sigue; (b) `mkdir` a
   mano antes de correr, sin fichero. Recomiendo (a): queda en el repo y el revisor lo ve. Coste
   de (b): nada en git hasta las salidas, y un paso manual que no está escrito.
4. **HER:30 y HER:35 y la «línea base vigente».** Opciones: (a) las salidas de esta rama NO son
   una línea base (son diagnóstico etiquetado, `diagnostico.py:169-170`) y HER:30/35 siguen
   apuntando a `CABLEADO-SIMULADOR-LINEA-BASE.txt` hasta que A-35 y A-44 tengan valor; (b) declarar
   `arrastrada.DIAGNOSTICO….txt` como la referencia de comparación de esos heredados. Recomiendo
   (a): una línea base no puede llevar nombre de diagnóstico. Coste de (b): contradice la regla
   del nombre.
5. **El orden de las filas.** Opciones: (a) por mes en el orden de `construccion` (04, 07, 08, 01),
   como dice el encargo; (b) cronológico, como «Por sesion» y el resto del informe. Recomiendo (a),
   porque lo pide el encargo y enero, el material más nuevo, queda al final. Coste de (b): no
   coincide con el encargo.

Lo que NO pregunto porque el encargo ya lo fija y el repo lo sostiene: los tres comandos tal cual
(§1.a), la repetición de la 2 fuera del repo para el `diff` (la pide el propio encargo), la lectura
de A-35 de la corrida principal (`cierre_vela_contraria`, fijada antes de correr), y la declaración
de hoy en HOLDOUT-EXPOSICIONES (hecha).

### 1.l Respuesta del consultor a la PARADA (2026-10-14)

Copiada tal cual (también al final de `docs/encargos/trabajo-corrida-construccion.md`):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/corrida-construccion (2026-10-14). Cópiala literal al informe, §1, bajo «Respuesta del consultor», con la fecha.
>
> 1. Decisión 0: (a). La sección «## Diferencias por operacion» es la última de arnes.informe; con --simular queda antes de la cola «## Simulacion», y cli.py no se toca. Porque nada del comando ni de la lista cerrada de ADR-0070 se mueve, y se encuentra por su encabezado.
> 2. Decisión 1: (a). El resumen y el embudo por mes van en la sección, calculados en arnes.py a partir de la misma Medida partida por mes, con tests sintéticos. Porque las cifras escritas a mano no tienen test.
> 3. Decisión 2: (a). La tabla no marca las horas perdidas; el informe lista las filas que caen en una de las 17 horas que caen dentro de las sesiones (y dice que la 18.ª queda fuera). Haz el cruce con un comando o guion que quede escrito en el informe, no a ojo, y pega su salida. Porque tocar cli.py para esto no compensa, pero el cruce tiene que poder repetirse.
> 4. Decisión 3: (a). La fase 1 commitea docs/validation/anexos/CORRIDA-CONSTRUCCION/README.md con qué es cada fichero y los tres comandos literales. Porque así la carpeta existe en git antes de correr.
> 5. Decisión 4: (a). Las salidas son diagnóstico etiquetado y no son una línea base; HER:30 y HER:35 siguen apuntando a CABLEADO-SIMULADOR-LINEA-BASE.txt hasta que A-35 y A-44 tengan valor. Porque una línea base no puede llevar nombre de diagnóstico.
> 6. Decisión 5: (a). Por mes en el orden de construccion (04, 07, 08, 01). Porque lo pide el encargo.
> 7. tramo: R3 en el contrato vale (scripts/contrato_rama.py lo acepta como equivalente).
> 8. La afirmación 28 del encargo era INCORRECTA y el error es mío: dije que el M1 de julio cambiaba el calentamiento de agosto sin mirar la fecha del manifiesto. En el informe, sustituye esa comparación por lo que mediste: lo que separa esta corrida de BE-AL-TICK es el motor desde ADR-0066 (con 0067, 0068, 0069, 0071, 0073 a 0077 y cases por la rejilla) y que la cuenta arrastrada recorre ahora enero, abril, julio y agosto. Propón en §1.k la fila para ERRORES-RECURRENTES: consultor y auditor del consultor dieron por cierto un cambio de calentamiento sin mirar cuándo entró el manifiesto. Lección: un «antes no estaba» se comprueba con la fecha de entrada del fichero en git.
> 9. Corrida 1 (cuenta arrastrada): se corre tal cual, sin cambiar el orden ni partir el tramo. El informe dice que el tramo no es continuo (enero, y luego de abril a agosto con huecos), que su veredicto de cuenta y su curva son indicativos, y que la clasificación se hace sobre la corrida 2. Junto al veredicto, la nota del margen que propones: el simulador no comprueba el margen (HER:37), así que puede llenar operaciones que FTMO rechazaría.
> 10. Agosto: sus casos dev salen de un xlsx que el trader no da por bueno (S-16, ADR-0073; NA:Q). En la tabla no se marca nada; en el informe, una línea que lo recuerda junto al resumen de agosto. Yo decido al clasificar si alguna diferencia de agosto es (M).
> 11. La lectura del M1 de marzo y junio para calentar: queda bien declarada la de hoy. Lo permanente (cada make check por test_huecos_motor.py:290-337 y cada corrida del arnés) va a las líneas del cierre como una línea de Technical Debt nueva y una fila única en HOLDOUT-EXPOSICIONES que la declare como exposición permanente por recuento. La propuesta de que dias_de_mercado imprima una línea LECTURA: va a G.2, en esa misma línea. No se cambia código para esto en esta rama.
> 12. Hallazgo 1.k.2 (ADR-0070) y 1.k.3 (runbook ACTIVAR-A35-A44.md): entran en ESTA rama, en la fase 3 y en un commit propio. Amplía el contrato con docs/adr/0070-umbral-de-construccion-para-medir-mayo.md (solo para añadir la NOTA, que es lo que permite el régimen de los ADR; el cuerpo no se edita) y docs/runbooks/ACTIVAR-A35-A44.md. La NOTA es la que propones en 1.k.2, añadiendo al final la cifra del veredicto que dé la corrida. En el runbook: las tres menciones de --diagnostico-a21 se marcan como «(ya no existe, ADR-0076)», y el comando del §5 lleva --simular para que se compare con una línea base escrita con --simular. Porque los dos llevan dos ramas pendientes y son texto.
> 13. Hallazgos 1.k.1 (Refs de R3.1 con ID:ADR-0074 · ID:ADR-0067 y la frase de las peticiones) y 1.k.5 (F apunta a V; antes, J y A.4): van a las líneas del cierre tal como los propones.
> 14. La guardia que bloqueó tu guion por nombrar data/manifests/ticks: bien declarado y bien no rodeado. Tu propuesta para G.1 va a las líneas del cierre como texto de G.1; no se toca .claude/ en esta rama.
> 15. La repetición de la corrida 2 con --salida fuera del repo, para el diff, queda autorizada como cuarto comando. Escríbelo literal en el README y en el informe, y borra la copia después.
>
> Sigue con la fase 1. Recuerda: make check en verde antes de cada commit, las corridas nunca a la vez que make check, y si la guardia o el clasificador niegan un comando, PARADA con el comando exacto y lo lanza Aleks con «!». Después, la fase 2 y la PARADA 2.
>
> Rama lista para revisión, NO cerrada.

**Aplicación, punto por punto:** 1 a 6, en la fase 1 (§2); 7, nada que hacer; 8, §1.c ya dice lo
medido y §1.k.6 trae la fila propuesta; 9 y 10, en el informe de la fase 2 (§3); 11, 13 y 14, en
las líneas del cierre (§5); 12, en la fase 3 con el contrato ampliado (`docs/adr/0070-*.md` y
`docs/runbooks/ACTIVAR-A35-A44.md`, ampliados en el commit de la fase 1, que es el primero tras la
respuesta); 15, el cuarto comando literal en el README y en §3.

## 2 · Fase 1 · La sección «Diferencias por operacion» (2026-10-14)

Con las decisiones 0 a 5 en (a). Ningún parámetro, ninguna regla, ninguna decisión del motor, ni
el broker, ni la cuenta, ni el freno, ni `criterio_fidelidad.yaml`, ni `cli.py` cambian: el diff
de `src/` es solo `src/botsito/engine/arnes.py`, y en él **0 líneas quitadas o cambiadas**
(`git diff HEAD -- src/botsito/engine/arnes.py | grep -c '^-[^-]'` → 0): se añade.

- **El código** (`src/botsito/engine/arnes.py`): `informe` termina ahora con
  `*diferencias_por_operacion(corrida, criterio, vocabulario, medida=medida)` tras «## Por
  sesion» (:389-393), pasándole la MISMA `Medida` que acaba de imprimir en el criterio.
  `diferencias_por_operacion` (:480-) escribe los tres bloques de §1.d con las tolerancias del
  criterio en la cabecera (ninguna cifra en el código, `test_no_business_literals`):
  - el resumen por mes, con los meses en el orden de `criterio.construccion`
    (`_meses_en_orden`, :414-419) y las cifras partidas por mes de la misma `Medida`;
  - el embudo por mes, con `primer_hecho_que_falta` (:462-470: el primer hecho de origen `regla`,
    en el orden de `hechos_de_regla`, que la traza no produjo, con las primitivas
    `NO_IMPLEMENTADA` de sus productoras, como «Por sesion»);
  - una fila por operación del trader (pareja, o la del bot más cercana en la sesión con
    `_mas_cercana`, :445-459, el orden del criterio sin exigir el lado, o «ninguna», más el primer
    hecho que faltó) y una por operación del bot sin pareja. Las parejas se buscan por identidad
    de objeto (`medir` devuelve los mismos objetos que recibe), los Δ llevan signo
    (`_delta_con_signo`, :422-426) y el formato es `Δentrada +n puntos, Δinstante +m min s s`.
- **Tests** (`tests/unit/test_diferencias_por_operacion.py`, 12, todos sintéticos: `arnes.Corrida`,
  `ResultadoDia` y `TrazaSesion` escritos a mano, ninguno corre el arnés ni lee velas): los cuatro
  que pide el encargo en los dos sentidos -emparejada con su Δ (+1 punto, +30 s); a 4 puntos SIN
  PAREJA con «Δentrada +4 puntos» y a 3 PAREJA; a 16 minutos SIN PAREJA con «Δinstante +16 min 0
  s» y a 15 PAREJA; una sesión sin operación del bot que dice «ninguna operacion del bot en la
  sesion; primer hecho que falto: liquidez[predicado:alcanza_nivel]» y lo cuenta en el embudo del
  mes; una operación del bot en un día sin trader que sale «SIN PAREJA; ninguna operacion del
  trader en el dia» y cuenta como «bot en dias sin trader»-, más el «más cercano» por el orden del
  criterio sin exigir lado, el primer hecho que falta en el orden de la spec, dos sesiones del
  mismo día (una pareja y una sin bot), el bot en otra sesión del día del trader, el orden por
  `construccion` (una lista a propósito NO cronológica, `("2030-03", "2030-01")`), que la sección es
  la última del informe y el informe sigue determinista byte a byte, y **que la sección no añade
  ninguna opción**: `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` es la de la enmienda y las opciones largas
  del subparser `motor arnes` son exactamente las 13 de §1.a. Sin la sección, cada test que llama
  a `_seccion` falla en su primera aserción (`texto.count("## Diferencias por operacion") == 1`).
- **Lo que depende del formato, comprobado**: `test_arnes_motor.py`, `test_umbral_mayo.py`,
  `test_huecos_motor.py`, `test_cableado.py` (94 tests), `test_preparar_a35.py` y
  `test_rutas_windows.py` (los que corren el arnés real sobre `construccion[0]`) en verde con la
  sección; `ruff check`, `ruff format --check` y `mypy` limpios sobre los dos ficheros.
- **La carpeta de salida** (decisión 3): `docs/validation/anexos/CORRIDA-CONSTRUCCION/README.md`,
  con qué es cada fichero, los tres comandos literales y el cuarto (la repetición de la 2 fuera
  del repo, punto 15 de la respuesta).
- **Runbook**: `docs/runbooks/ARNES-MOTOR.md` describe la sección en «Qué hace» y en «Cómo leer
  “Diferencias por operacion”».
- **Contrato ampliado** (punto 12 de la respuesta): entran `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md`
  (solo la NOTA) y `docs/runbooks/ACTIVAR-A35-A44.md`, para la fase 3; `docs/adr/` deja de estar
  protegida entera (solo 0070 está permitida, así que cualquier otro ADR sigue fuera).
- **Desviación declarada**: `PROJECT_STATE.md` cambia en una cifra, «Tests Currently Passing» 1535
  → 1547, porque `state check` lo exige al final de `make check` con los 12 tests nuevos
  (CONTRATO-DE-RAMA.md: «anadir tests cambia el recuento»); el encargo decía que esta rama no lo
  toca, y no se toca nada más (23.773 bytes).

## 3 · Fase 2 · Las tres corridas (2026-10-14)

Sobre el código de la fase 1 commiteado (d63b30f), sin `--meses`, una corrida cada vez y ninguna a
la vez que `make check`. **Todo es DIAGNÓSTICO etiquetado: no es fidelidad, no habilita mayo
(ADR-0070 §3) y ninguna cifra de aquí fija ni cambia ningún valor.** La lectura de A-35 de la
corrida principal, `cierre_vela_contraria`, quedó fijada antes de correr (§1.a). Ni la guardia ni
el clasificador negaron ninguno de los cuatro comandos. Las salidas están en
`docs/validation/anexos/CORRIDA-CONSTRUCCION/` con el rótulo que les puso `nombre_etiquetado`; sus
líneas `TIEMPO` y `MEMORIA` salieron por pantalla y se copian aquí tal cual.

### 3.1 Los comandos literales y lo que escribieron

1. `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/arrastrada.txt`
   → `arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt` (974 líneas; exit 0).
   `TIEMPO: 367.3 s; MEMORIA: pico del proceso de 631.3 MiB`.
2. `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/diaria.txt`
   → `diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (exit 0).
   `TIEMPO: 353.5 s; MEMORIA: pico del proceso de 631.8 MiB`.
3. `uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/a35-inicio.txt`
   → `a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (exit 0).
   `TIEMPO: 306.8 s; MEMORIA: pico del proceso de 631.2 MiB`.
4. La repetición de la 2 fuera del repo (punto 15 de la respuesta), para el determinismo:
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida <carpeta temporal de la sesión>/diaria.txt`
   → `<carpeta temporal>/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
   (exit 0). `TIEMPO: 319.9 s; MEMORIA: pico del proceso de 632.1 MiB`. `diff` con la salida de
   la 2: idénticos (`git hash-object` de los dos: `f8f0f5992774671dcafd6eff3bef526136c42c38`);
   la copia se borró después.

**Tiempo y memoria frente a lo estimado (§1.e2):** el tiempo cuadra (5 a 6 minutos por corrida);
la memoria no: 631 MiB de pico frente a los «menos de 300» estimados a partir de 42 días. El
proceso carga los ticks de los 76 días y las M1 de siete meses (los cuatro de construcción y los
tres de calentamiento); ningún informe anterior había medido cuatro meses. Queda medido para la
próxima estimación, y es lo que hay que tener en cuenta con el recorte de procesos en segundo plano
de Claude Code (CLAUDE.md, «Trampas medidas»): ninguna corrida murió.

### 3.2 Por corrida y por mes

Del «Resumen por mes» de cada salida (la misma `Medida` del criterio, partida por mes) y de su
sección del criterio. Abril y agosto son los meses de BE-AL-TICK; julio y enero son nuevos.

| Corrida | Mes | Días | Trader | Bot puntuables | Bot en días sin trader | Parejas | Cobertura | Precisión |
|---|---|---|---|---|---|---|---|---|
| 1 arrastrada | 2026-04 | 21 | 35 | 3 | 5 | 0 | 0/35 (0.0 %) | 0/3 (0.0 %) |
| 1 arrastrada | 2026-07 | 13 | 67 | 0 | 0 | 0 | 0/67 (0.0 %) | sin definir |
| 1 arrastrada | 2026-08 | 21 | 42 | 0 | 0 | 0 | 0/42 (0.0 %) | sin definir |
| 1 arrastrada | 2026-01 | 21 | 54 | 35 | 0 | 1 | 1/54 (1.9 %) | 1/35 (2.9 %) |
| 1 arrastrada | **total** | 76 | 198 | 38 | 5 | 1 | 1/198 (0.5 %) | 1/38 (2.6 %) |
| 2 diaria | 2026-04 | 21 | 35 | 20 | 11 | 4 | 4/35 (11.4 %) | 4/20 (20.0 %) |
| 2 diaria | 2026-07 | 13 | 67 | 16 | 0 | 5 | 5/67 (7.5 %) | 5/16 (31.2 %) |
| 2 diaria | 2026-08 | 21 | 42 | 21 | 1 | 2 | 2/42 (4.8 %) | 2/21 (9.5 %) |
| 2 diaria | 2026-01 | 21 | 54 | 37 | 0 | 1 | 1/54 (1.9 %) | 1/37 (2.7 %) |
| 2 diaria | **total** | 76 | 198 | 94 | 12 | 12 | 12/198 (6.1 %) | 12/94 (12.8 %) |
| 3 a35-inicio | los cuatro | 76 | 198 | 94 | 12 | 12 | 12/198 (6.1 %) | 12/94 (12.8 %) |

La corrida 3 da, mes a mes, las mismas cuatro filas que la 2 (§3.4: ninguna operación del bot ni
ninguna pareja cambia). Parejas en el mismo minuto: 1 (corrida 1), 7 (2 y 3).

**La línea de veredicto de ADR-0070, tal cual** (todas dicen «no», como estaba previsto):
- corrida 1: `habilita medir el conjunto de medida (2026-05) (ADR-0070): no (opción fuera de la lista: --diagnostico-a35; opción fuera de la lista: --diagnostico-a44; cobertura 0.5 % por debajo de 70.0 %; precision 2.6 % por debajo de 60.0 %)`
- corrida 2: `habilita medir el conjunto de medida (2026-05) (ADR-0070): no (opción fuera de la lista: --diagnostico-a35; opción fuera de la lista: --diagnostico-a44; opción fuera de la lista: --diagnostico-cuenta-diaria; cobertura 6.1 % por debajo de 70.0 %; precision 12.8 % por debajo de 60.0 %)`
- corrida 3: la misma que la 2.

**Agosto** (punto 10 de la respuesta): sus 19 casos dev salen de un xlsx que el trader no da por
bueno (S-16, ADR-0073; NA:Q); la tabla no lo marca y el consultor decide al clasificar si alguna
diferencia de agosto es (M).

### 3.3 La corrida 1: la cuenta sobre el tramo, y las peticiones (ADR-0074 §3)

- **El tramo no es continuo**: la cuenta arrastrada recorre los días por fecha, enero (21 días) y
  después abril, julio y agosto (con los huecos de febrero, marzo, mayo y junio entre medias;
  §1.c). Su veredicto y su curva son INDICATIVOS; la clasificación se hace sobre la corrida 2.
- **Veredicto de la cuenta**: `estado: EN_CURSO`, `motivo: sin objetivo alcanzado ni limite
  infringido`, `PRIMERO EN TOCAR UN LIMITE: ninguno`; saldo y equity finales 90.571,27 (−9,43 %
  sobre 100.000); `dias de trading: 22`; `RACHA DE PERDIDAS (RN-036, A-51): 4 seguidas; la ultima
  el 2026-04-07`. **La cuenta no corta el tramo por un límite, pero lo deja sin operar desde el
  2026-04-08**: el saldo baja a 90.571,27 al cierre del 2026-04-07 (curva de equity) y desde la
  sesión 07-11 del 2026-04-08 **RN-032** («no se abre una operacion cuyo riesgo no cabe antes del
  limite de la firma»: `firma_perdida_total_max` 10 % menos `firma_margen_seguridad` 0,5 %) dispara
  en todas las sesiones -101 de las 152 corridas- y el bot no coloca nada más: 0 operaciones del
  bot en abril desde el 8, en julio y en agosto (§3.2). Es el mismo mecanismo que F35 §4.4 vio «el
  22 de abril»; ahora llega antes porque el tramo empieza en enero y entra en abril con 92.905
  (−7,1 %). La fila del día y la regla: `2026-04-08 07-11 | … | disparadas … RN-032`.
- **Nota del margen (HER:37, respuesta punto 9)**: el simulador no comprueba el margen, así que en
  esta corrida pueden salir llenadas operaciones que FTMO rechazaría por margen; el veredicto de
  la cuenta no lo tiene en cuenta.
- **Peticiones al servidor** (la medida que hereda ADR-0074 §3, con `caja_se_fija =
  en_cada_cierre_m1` por el cableado real): **256 en el tramo** (suma de la tabla por día de la
  firma, 76 días), **máximo diario 32** (el 2026-01-02 y el 2026-04-07) frente a
  `firma_mensajes_dia_max` 2000; **el freno de ADR-0067 no saltó**: `umbrales: aviso 1000, corte
  1500, bucle 5 iguales en 1 min` y `ningun aviso ni ninguna peticion negada`; cierres de mercado
  (ADR-0068): `ninguna peticion negada ni ninguna pendiente cancelada`. Rechazos del broker: 33;
  eventos 104 (ticks 95, respaldo_m1 9). Como contexto, F35 §4.3 midió en diagnóstico hasta 14 al
  día y 59 en 42 días con esta lectura de la caja; aquí, con 76 días y el tramo desde enero, 32 y
  256. Lejos de los umbrales en los dos casos.
- La corrida 2 (cuenta reiniciada cada día) da 703 peticiones en el tramo, máximo diario 34
  (2026-04-15), sin aviso ni corte, 111 rechazos del broker y 253 eventos (ticks 239,
  respaldo_m1 14); la 3, 683 y el mismo máximo.

### 3.4 La corrida 3 frente a la 2: qué cambia con `inicio_vela_contraria`

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/comparar_corridas.py <salida 2>
<salida 3>` (lee solo las filas de «Diferencias por operacion» de los dos ficheros commiteados):

```
A = diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt; B = a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt; sesiones con alguna diferencia: 0; operaciones del bot A 106, B 106; parejas A 12, B 12
```

**Ninguna operación del bot y ninguna pareja cambian** entre las dos lecturas de A-35: las 106
operaciones del bot y las 12 parejas son las mismas, día a día. Lo que sí cambia (diff de las dos
salidas sin su prefijo, 96 líneas):
- **2026-08-19 11-15**: con `inicio_vela_contraria` la sesión no produce `orden_dimensionada` ni
  `liquidez_tomada` (con `cierre`, sí); en las dos el bot no opera y el trader tiene 2 operaciones.
  Es la única sesión cuya traza de hechos cambia: `liquidez_tomada` pasa de 98 a 97 de 104.
- **Las peticiones**: 703 → 683; en dos días, 2026-01-19 (21 → 13) y 2026-08-13 (16 → 4), sin que
  cambie ninguna operación.
- **Los avisos de orden de ADR-0049 (H3)**: 25 avisos menos con `inicio` (RN-004 empatando con
  RN-014, RN-011, RN-012 o RN-006 en sesiones de los cuatro meses), porque RN-004 dispara en 2
  sesiones menos.
Sin elegir lectura: esto NO decide A-35. Los días para preguntarle al trader, si el consultor los
quiere: 2026-08-19 (sesión 11-15), 2026-01-19 y 2026-08-13.

### 3.5 El embudo agregado, por mes (corrida 2) y lo que (no) dice

Del «Embudo por mes» de la salida 2 (sesiones con operaciones del trader y sin operación del bot,
y el primer hecho de origen `regla` que falta, en el orden de la spec):

| Mes | Sesiones con trader | Sin operación del bot | `detenido_por_tope[productoras sin cumplirse]` | `orden_dimensionada[productoras sin cumplirse]` |
|---|---|---|---|---|
| 2026-04 | 23 | 11 | 10 | 1 |
| 2026-07 | 25 | 13 | 13 | 0 |
| 2026-08 | 26 | 18 | 16 | 2 |
| 2026-01 | 30 | 11 | 8 | 3 |
| total | 104 | 53 | 47 | 6 |

Global (sección del embudo de la salida 2): sesgo 104 de 104, orden_dimensionada 98, liquidez_tomada
98, los cuatro `detenido_por_*` 0, operación del bot 51 de 104; ninguna primitiva NO_IMPLEMENTADA.

**Hallazgo (importa, para la PARADA 2): con la definición del encargo, «el primer hecho que no se
produjo» es casi siempre `detenido_por_tope`, y eso no dice dónde se para la sesión.** Los hechos
de origen `regla` van en la spec en este orden: `sesgo`, `orden_dimensionada`, `detenido_por_tope`,
`detenido_por_tope_total`, `detenido_por_cartuchos`, `detenido_por_racha`, `liquidez_tomada`
(`strategy_spec.yaml`, `hechos:`). Los cuatro `detenido_por_*` son FRENOS: solo se producen cuando
un tope para al bot, y con `sin_tope` el primero no se produce nunca. Así que en cuanto una sesión
produce `sesgo` y `orden_dimensionada`, el «primer hecho que falta» es `detenido_por_tope`, que no
faltó: no tocaba. Medido aparte, saltando los frenos (un guion de la carpeta de trabajo sobre las
líneas «Por sesion» de la salida 2; salida pegada tal cual):

```
2026-01 | todos los del camino | 8
2026-01 | orden_dimensionada:no[productoras sin cumplirse] | 3
2026-04 | todos los del camino | 10
2026-04 | orden_dimensionada:no[productoras sin cumplirse] | 1
2026-07 | todos los del camino | 13
2026-08 | todos los del camino | 16
2026-08 | orden_dimensionada:no[productoras sin cumplirse] | 2
```

En 47 de las 53 sesiones sin operación del bot se produjeron los tres hechos del camino (`sesgo`,
`orden_dimensionada`, `liquidez_tomada`): el bot llegó a dimensionar y a colocar, y lo que faltó
está DESPUÉS del grafo de hechos, en la vida de la orden -el broker la rechazó (111 rechazos en la
corrida 2, que el informe cuenta pero no lista), no se llenó antes de retirarse (RN-035 a
`ventana_fin`, la red de seguridad del fin de día) o se llenó en otra sesión-, que es el embudo de
F35 §4.4 (nace, punto, bróker, reubica, llenado) y no el de ADR-0048 §5. En las otras 6, falta
`orden_dimensionada` (RN-011 o RN-015 no se cumplieron). La tabla por operación sigue siendo
válida para clasificar (pareja, más cercana, Δ), pero su último campo no ayuda. Propuesta en §3.9.

### 3.6 Las 18 horas sobre respaldo M1 y qué filas caen en ellas

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/horas_perdidas.py <salida>` (las 18
horas de §1.e escritas en el guion; una fila cae si el instante del trader, del bot emparejado o
del más cercano está dentro de la hora UTC; la 18.ª, 2026-04-22T13Z, queda fuera de las sesiones y
el guion lo marca si saliera: no sale en ninguna corrida). Sobre la corrida 2 (la que se
clasifica), salida tal cual:

```
diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt: 292 filas por operacion
- 2026-04-06T10Z: bot | 2026-04-06 | 11-15 | compra | 2026-04-06T10:01:00+00:00 | 1.15509 | SIN PAREJA; ninguna operacion del trader en la sesion
- 2026-04-07T10Z: bot | 2026-04-07 | 11-15 | compra | 2026-04-07T10:32:00+00:00 | 1.15564 | SIN PAREJA; ninguna operacion del trader en el dia
- 2026-04-23T05Z: trader | 2026-04-23 | 07-11 | venta | 2026-04-23T05:30:00+00:00 | 1.17018 | SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-04-23T05Z: trader | 2026-04-23 | 07-11 | venta | 2026-04-23T05:53:30+00:00 | 1.17038 | SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-07-10T05Z: trader | 2026-07-10 | 07-11 | compra | 2026-07-10T05:36:35+00:00 | 1.14382 | SIN PAREJA; bot mas cercano en la sesion: compra 2026-07-10T07:05:19.163000+00:00 1.14399 (Δentrada +17 puntos, Δinstante +88 min 44 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-07-10T05Z: trader | 2026-07-10 | 07-11 | compra | 2026-07-10T05:45:20+00:00 | 1.14382 | SIN PAREJA; bot mas cercano en la sesion: compra 2026-07-10T07:05:19.163000+00:00 1.14399 (Δentrada +17 puntos, Δinstante +79 min 59 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-07-16T11Z: trader | 2026-07-16 | 11-15 | compra | 2026-07-16T11:19:40+00:00 | 1.1462 | SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-07-16T11Z: trader | 2026-07-16 | 11-15 | compra | 2026-07-16T11:55:40+00:00 | 1.1467 | SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-08-20T07Z: bot | 2026-08-20 | 07-11 | venta | 2026-08-20T07:02:00+00:00 | 1.16847 | SIN PAREJA; trader mas cercano en la sesion: compra 2026-08-20T05:47:10+00:00 1.16709 (Δentrada -138 puntos, Δinstante -74 min 50 s)
- 2026-08-20T07Z: bot | 2026-08-20 | 07-11 | venta | 2026-08-20T07:45:00+00:00 | 1.16896 | SIN PAREJA; trader mas cercano en la sesion: compra 2026-08-20T05:47:10+00:00 1.16709 (Δentrada -187 puntos, Δinstante -117 min 50 s)
- 2026-01-05T10Z: trader | 2026-01-05 | 11-15 | venta | 2026-01-05T10:57:45+00:00 | 1.1687 | SIN PAREJA; bot mas cercano en la sesion: venta 2026-01-05T10:54:00+00:00 1.16877 (Δentrada +7 puntos, Δinstante -3 min 45 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-01-05T10Z: trader | 2026-01-05 | 11-15 | venta | 2026-01-05T11:04:15+00:00 | 1.16889 | SIN PAREJA; bot mas cercano en la sesion: venta 2026-01-05T10:54:00+00:00 1.16877 (Δentrada -12 puntos, Δinstante -10 min 15 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-01-05T10Z: bot | 2026-01-05 | 11-15 | venta | 2026-01-05T10:54:00+00:00 | 1.16877 | SIN PAREJA; trader mas cercano en la sesion: venta 2026-01-05T10:57:45+00:00 1.1687 (Δentrada -7 puntos, Δinstante +3 min 45 s)
- 2026-01-23T11Z: trader | 2026-01-23 | 11-15 | venta | 2026-01-23T11:52:10+00:00 | 1.17382 | SIN PAREJA; bot mas cercano en la sesion: venta 2026-01-23T11:04:00+00:00 1.17331 (Δentrada -51 puntos, Δinstante -48 min 10 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-01-23T11Z: trader | 2026-01-23 | 11-15 | venta | 2026-01-23T12:55:35+00:00 | 1.17428 | SIN PAREJA; bot mas cercano en la sesion: venta 2026-01-23T11:04:00+00:00 1.17331 (Δentrada -97 puntos, Δinstante -111 min 35 s); primer hecho que falto: detenido_por_tope[productoras sin cumplirse]
- 2026-01-23T11Z: bot | 2026-01-23 | 11-15 | venta | 2026-01-23T11:04:00+00:00 | 1.17331 | SIN PAREJA; trader mas cercano en la sesion: venta 2026-01-23T11:52:10+00:00 1.17382 (Δentrada +51 puntos, Δinstante +48 min 10 s)
filas con algun instante en una hora perdida: 16 de 292
```

Sobre la corrida 1: 14 de 240 filas (las mismas horas; julio y agosto sin filas del bot); sobre
la 3: las mismas 16 de 292 que la 2. **Dato para (M):** las seis operaciones del bot con instante
en segundo `:00` exacto (2026-04-06 10:01:00, 2026-04-07 10:32:00, 2026-08-20 07:02:00 y 07:45:00,
2026-01-05 10:54:00 y 2026-01-23 11:04:00) son llenados sobre el respaldo M1 -la M1 llena al cierre
del minuto, `llenado.py:166`- dentro de una hora sin ticks: la corrida 2 tiene 14 eventos de fuente
`respaldo_m1`. Ninguna de las 12 parejas cae en una hora perdida.

### 3.7 Contexto, no referencia: BE-AL-TICK §2 frente a abril y agosto de esta corrida

BE-AL-TICK §2 (2026-10-01, 42 días dev, 77 operaciones, motor `stable/F36h`) dio 2 de 77 con la
cuenta arrastrada y 7 de 77 con la cuenta diaria. Hoy, sobre los mismos 42 días y 77 operaciones
(dentro de una corrida de 76 días):

| | BE-AL-TICK | Esta corrida |
|---|---|---|
| arrastrada, abril + agosto | 2 de 77 | **0 de 77** (0/35 y 0/42; el bot no opera desde el 2026-04-08, §3.3) |
| diaria, abril + agosto | 7 de 77 | **6 de 77** (4/35 y 2/42) |

Qué los separa, sin ajustar nada para acercarlos: (1) **el motor** desde ADR-0066 (cartuchos),
ADR-0067 (freno), ADR-0068 (cierres de mercado y la ventana de R15), ADR-0069 (las sesiones por la
rejilla H4, con el reloj de invierno), ADR-0071 (stops level 0 medido, sin diagnóstico A-27),
ADR-0073, ADR-0074 (la caja se recalcula en cada cierre de M1 hasta el llenado: en F35 esa lectura
dio 1 de 77 frente a 2 con la caja fija), ADR-0075 (el sesgo ambiguo), ADR-0076 (A-21 fijada en vez
del diagnóstico `solo_una_zona_de_control`), ADR-0077 (RN-036, la racha) y los casos por la rejilla
(`trabajo/cases-rejilla`); (2) **el calentamiento no cambia** (§1.c: julio y marzo ya estaban);
(3) **en la arrastrada, el camino de la cuenta**: el tramo empieza ahora en enero y entra en abril
con 92.905, así que RN-032 cierra el grifo el 8 de abril y no el 22. En la diaria no hay camino de
cuenta: 7 → 6 es efecto del motor.

### 3.8 Determinismo y lo que se leyó

- Dos corridas iguales, mismo fichero byte a byte: la corrida 2 y su repetición fuera del repo
  (§3.1, comando 4) dan el mismo blob, `f8f0f599…`, con `diff` vacío.
- Las corridas leyeron lo declarado el 2026-10-14 en HOLDOUT-EXPOSICIONES (§1.j): las velas M1 de
  marzo y junio para calentar, además de julio y de los cuatro meses de construcción, y los ticks
  de los 76 días dev. Ninguna etiqueta nueva, ningún libro, nada de mayo. No hay exposición nueva.
- Un desliz de la sesión, declarado: mientras corría el `make check` de la fase 1 escribí
  `horas_perdidas.py` dentro de `docs/validation/anexos/CORRIDA-CONSTRUCCION/` y lo saqué del repo
  en el acto, antes del sello; la huella de `make check` cuenta los ficheros sin seguir
  (`scripts/sello_make_check.py:100`) y el sello salió en verde porque el fichero no existía ni al
  empezar ni al sellar. Fila propuesta para ERRORES-RECURRENTES en §1.k.6, junto a la otra.

### 3.9 Hallazgos de la fase 2 para la PARADA 2

1. **(importa) El «primer hecho que falta» no sirve para clasificar** (§3.5): con la definición
   del encargo da `detenido_por_tope` en 47 de 53 sesiones. Opciones: (a) dejar la sección como
   está y leer, para cada fila, su línea de «Por sesion» (que trae los siete hechos) y el embudo de
   la vida de la orden a mano; (b) un commit más en esta rama que cambie el último campo por «el
   primer hecho DEL CAMINO que falta» (sin los `detenido_por_*`, que se listan aparte solo si se
   produjeron) y, cuando se produjeron los tres, `todos los hechos del camino producidos`; exige
   repetir las tres corridas (unos 20 minutos) y otro `make check`; (c) además de (b), que la fila
   diga qué pasó con la orden (colocada, rechazada, cancelada a `ventana_fin`, llenada en otra
   sesión), que es lo que de verdad falta, pero eso vive en el broker (`TrazaBroker`,
   `cableado.py`, protegido) y no llega a `arnes.informe` sin tocar `cli.py` o `cableado.py`.
   Recomiendo (b) ahora y (c) como rama de código si el consultor la quiere; coste de (a): la
   clasificación tiene que mirar dos sitios por fila.
2. **(importa) 111 rechazos del broker en la corrida 2** (33 en la 1), que el informe cuenta pero
   no lista por día ni por motivo (`cableado.py:655-674`, solo el total; el visor sí los enseña
   por día). Para clasificar las sesiones con «todos los hechos del camino» y sin operación del bot
   hace falta saber si la orden se rechazó (ADR-0057/0058: precio ya roto, volumen) o se canceló.
   Propuesta: que la cola de simulación liste los rechazos por día con su motivo (rama de código,
   `cableado.py`), o que el consultor pida por el visor los días que quiera (no abiertos aquí).
3. **(menor) 631 MiB de pico** por corrida de cuatro meses, el doble de lo estimado (§3.1).
4. **(menor) La memoria del estimador**: §1.e2 extrapoló por días; la memoria escala con los
   ticks y las M1 cargadas, no con los días corridos.

## Estado

EN CURSO. Fase 0 entregada y respondida el 2026-10-14; fase 1 hecha; fase 2 hecha el 2026-10-14:
**PARADA 2, entrega para clasificar** (la tabla de la corrida 2 en
`docs/validation/anexos/CORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`,
sección «## Diferencias por operacion»). Pendientes: la clasificación del consultor (fase 3), la
NOTA de ADR-0070 y el runbook (fase 3), el revisor y las líneas del cierre.
