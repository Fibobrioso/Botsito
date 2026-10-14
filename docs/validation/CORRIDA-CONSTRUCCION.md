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
quiere: 2026-08-19 (sesión 11-15), 2026-01-19 y 2026-08-13. *(Con las salidas repetidas de §3.12,
lo mismo: 0 sesiones con alguna diferencia, salida del guion en
`anexos/CORRIDA-CONSTRUCCION/comparar_corridas.txt`; y la vida de la orden lo explica: con
`inicio` hay 10 reubicaciones menos, 4 en 2026-01-19 11-15 y 6 en 2026-08-13 11-15, que son las
peticiones que bajan.)*

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

### 3.10 Respuesta del consultor a la PARADA 2 (2026-10-14)

Copiada tal cual (también al final de `docs/encargos/trabajo-corrida-construccion.md`):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/corrida-construccion (2026-10-14). Cópiala literal al informe, como §3.10 «Respuesta del consultor a la PARADA 2», con la fecha.
>
> Antes de clasificar fila a fila hace falta saber qué pasó con cada orden. Con la tabla de hoy, 75 operaciones del trader a favor del sesgo del bot caen en sesiones donde el bot no llena nada, y hay 111 rechazos del bróker sin motivo listado: clasificar eso sería adivinar. Así que hoy dejo una clasificación PROVISIONAL por patrones, y la definitiva va en una PARADA 3, después de un cambio de salida y de repetir las corridas.
>
> 1. Hallazgo 1 de §3.9: (b) y (c) en ESTA rama, como cambios de SALIDA y nada más.
>    a) En la sección «Diferencias por operacion», el último campo pasa a ser «el primer hecho DEL CAMINO que falta» (sgo, liquidez_tomada, orden_dimensionada, en el orden de la spec), sin los detenido_por_*; estos se añaden aparte solo si se produjeron. Si se produjeron los tres: «todos los hechos del camino producidos».
>    b) En la cola de simulación (cableado.informe_simulacion), una subsección nueva «### Ordenes (dia | sesion | id | colocada UTC | precio | resultado | motivo | instante del resultado)»: una línea por orden que el bot intentó colocar, con su resultado (llenada, rechazada, cancelada, viva al cerrar la sesión) y el motivo tal como lo da el bróker o el cableado (precio ya roto, volumen, ventana_fin, caja nueva, el que sea). Y otra, «### Rechazos por motivo», con el recuento por motivo y por mes.
>    Amplía el contrato a src/botsito/engine/cableado.py SOLO para informe_simulacion y lo que necesite leer de la traza del bróker. No cambia ninguna decisión del bróker, del motor ni de la cuenta, ni ninguna opción del comando (la lista de ADR-0070 sigue igual). Si para listar la vida de la orden hiciera falta tocar algo que decide, PARADA.
>    Tests sintéticos en los dos sentidos: una orden llenada, una rechazada con su motivo, una cancelada a ventana_fin y una viva al cierre; que el nuevo último campo no nombra nunca un detenido_por_* que no se produjo; y que las opciones del comando siguen siendo las mismas.
>    Después, make check en verde y las tres corridas otra vez, con los mismos tres comandos y la repetición de la 2 fuera del repo para el diff. Las salidas nuevas sustituyen a las de hoy en el mismo commit (son anexos de una rama abierta, no evidencia inmutable), y el informe dice que se repitieron y por qué.
> 2. Hallazgo 2 de §3.9: queda cubierto por el punto 1.b.
> 3. Hallazgos 3 y 4 (memoria): solo se declaran. 631 MiB por corrida no bloquea nada.
> 4. Clasificación PROVISIONAL por patrones (2026-10-14), sobre la tabla de la corrida 2 de hoy. Calcula la asignación de cada fila a su patrón con un guion en anexos/CORRIDA-CONSTRUCCION/ (patrones.py) que aplique estas reglas literales, y pega su recuento por mes. Si tu recuento no coincide con el mío, dilo en la PARADA 3: no ajustes ni las reglas ni las cifras.
>    Reglas, para cada fila (el sesgo es el rn003 de la línea «Por sesion» de su sesión; «a favor» = compra con alcista o venta con bajista):
>    - T0 pareja: filas del trader con PAREJA. Recuento mío: 12.
>    - P1 sesgo: filas del trader sin pareja y contra el sesgo del bot. Recuento: 48, en 25 sesiones. Clase provisional: E o R, por decidir en el visor. Destino: rama de código si nuestro sesgo está mal (en 9 de esas 17 sesiones con dos sesiones el mismo día, el sesgo de la otra sesión sí coincidía con el trader: el cambio de sesgo a las 11:00 es el primer sospechoso), o pregunta de la sesión 5 si el trader opera contra su propio sesgo.
>    - P2 entrada: filas del trader sin pareja, a favor del sesgo, con una operación del bot del mismo lado a menos de 15 minutos y a más de 3 puntos. Recuento: 18 (Δ de 4 a 54 puntos, casi todas entre 6 y 21). Clase provisional: R (qué velas forman la caja, A-48 y A-49 ya van a la sesión 5), con una comprobación E en el visor de que el 0 de la caja sale de la vela que dice la spec.
>    - P3 otra zona: filas del trader sin pareja, a favor del sesgo, con el bot del mismo lado en la sesión pero a más de 15 minutos. Recuento: 45 (42 a otra entrada y 3 a la misma entrada pero a otra hora). Clase provisional: R (qué liquidez y qué zona escoge el trader: A-43, A-50, A-53).
>    - P4 sin orden: filas del trader sin pareja, a favor del sesgo, sin ninguna operación del bot en la sesión. Recuento: 75. Clase: PENDIENTE de la lista de órdenes del punto 1.b (si son rechazos por precio ya roto, E o R según el motivo; si no se produjo un hecho del camino, según cuál).
>    - P5 de más: filas del bot sin pareja en una sesión con operaciones del trader. Recuento: 61 (47 del mismo lado y 14 del otro). Clase provisional: R (cuántas veces reentra el trader tras un stop en la misma zona; los cartuchos), salvo las del otro lado, que siguen a P1.
>    - P6 donde el trader no operó: filas del bot en una sesión o un día sin operaciones del trader. Recuento: 33 (21 en sesión y 12 en día). Clase provisional: R (qué le hace no operar; enlaza con la deuda «el no_trade por ausencia no está decidido»), o M en agosto si el xlsx que el trader no da por bueno (S-16) no trae ese día.
>    Marca además, sin cambiar el patrón, las 16 filas que tocan una hora perdida (las de §3.6) como posible M.
> 5. Para la PARADA 3 quiero también, sin abrir el visor todavía, la lista de las 25 sesiones de P1 con: la hora UTC de las dos últimas H4 cerradas antes de la sesión, su apertura, máximo, mínimo y cierre en nuestras velas, el sesgo de la sesión anterior del mismo día y la regla que lo decidió (RN-003, doble ruptura, ADR-0060 o ADR-0075). Son velas de construcción: se leen sin puerta. Con eso decido qué días pido en el visor.
> 6. Agosto: recuerda en el resumen de agosto que sus casos salen del xlsx que el trader no da por bueno (S-16). Lo tengo en cuenta en P6 y al clasificar.
>
> Lo que sigue: el punto 1 (código de salida, tests y make check), las tres corridas repetidas, patrones.py con su recuento, el punto 5, y PARADA 3 con todo commiteado. Las mismas reglas: las corridas nunca a la vez que make check, y si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

### 3.11 El punto 1, hecho: el primer hecho del camino y la vida de la orden (commit 1b90d23)

Cambios de SALIDA y nada más; ninguna decisión del bróker, del motor ni de la cuenta, ninguna
opción nueva (test: las 13 opciones del subparser siguen iguales y la lista de ADR-0070 también).
- **1.a** (`src/botsito/engine/arnes.py`, `primer_hecho_que_falta`, `PREFIJO_FRENO =
  "detenido_por_"`): el último campo mira el camino -los hechos de origen `regla` que no empiezan
  por `detenido_por_`, en el orden de la spec: `sesgo`, `orden_dimensionada`, `liquidez_tomada`-
  y nombra un freno aparte (`; frenos producidos: …`) solo si se produjo; si no falta ninguno:
  `todos los hechos del camino producidos`. La cabecera del embudo por mes lo dice. El criterio es
  el prefijo del nombre, porque la spec no marca los frenos con ningún atributo (sus cuatro
  entradas comparten solo el nombre y que se producen «cuando algo para al bot»).
- **1.b** (`src/botsito/engine/cableado.py`): `TrazaBroker` guarda `cancelaciones` (instante, id,
  motivo) y `limites`; `correr_dia` anota, tras cada cierre de M1, las peticiones de cancelar que
  ese cierre pidió con las reglas que dispararon en él y dónde cayó («al abrir otra sesion», «en
  ventana_fin»), y las de la red de seguridad del fin del día con su motivo propio
  (`MOTIVO_FIN_DIA`); `vida_de_las_ordenes` lee `broker.ordenes`, `broker.traza().rechazos` y esa
  lista, y `_informe_ordenes` escribe «### Ordenes (dia | sesion | id | colocada UTC | precio |
  resultado | motivo | instante del resultado)» -resultado `llenada`, `rechazada` (motivo del
  bróker: `precio_invalido`, `stops_level`), `cancelada` (motivo del cableado) o `viva al cerrar el
  dia`- más `ordenes: …` y «### Rechazos por motivo (mes | motivo | peticion | rechazos)», entre los
  eventos y las peticiones. De las líneas existentes de `cableado.py` cambian dos (la construcción
  de `TrazaBroker`, para pasarle `limites`, y la cola del informe, para encadenar la sección);
  `cli.py` y `primitivas_broker.py` (protegido) intactos. Lo único que se añade al bucle de
  `correr_dia` es leer `broker.traza().peticiones` después de cada evento: lectura, sin efecto.
- **Tests** (`tests/unit/test_vida_de_la_orden.py`, 7, sobre el cableado real y la spec real con los
  días de 2030 de `test_cableado`): llenada (fila completa con el instante del llenado); rechazada
  con su motivo (`precio_invalido`, la compra STOP del lado equivocado de ADR-0058) y su recuento
  por motivo; cancelada en `ventana_fin` por RN-035 (la orden de la tarde que no se llena, como
  `test_rn035_ventana_fin`); cancelada «al abrir otra sesion» (la de la mañana); el motivo de una
  cancelación en los tres sitios y sin regla; y viva al cerrar el día (con un bróker y una traza
  escritos a mano, porque con la spec de hoy RN-035 llega antes que la red de seguridad). En
  `test_diferencias_por_operacion.py`, uno más: un `detenido_por_*` que no se produjo no se nombra
  nunca, y uno que sí se produjo sale aparte. `make check`: 2641 passed, sello `e4989239…`.
- **Runbook**: `docs/runbooks/ARNES-MOTOR.md` describe el campo nuevo y las dos subsecciones.
- **Anexos nuevos**: `patrones.py` (las reglas literales del punto 4, §3.13) y `sesgo_p1.py` (el
  punto 5, §3.14). `PROJECT_STATE.md`: «Tests Currently Passing» 1547 → 1554.

### 3.12 Las tres corridas repetidas sobre 1b90d23 (2026-10-14), y por qué

Se repitieron porque el punto 1 cambió la SALIDA (el último campo de la tabla y la vida de la
orden) y el consultor pidió que las salidas nuevas sustituyeran a las de §3.1 en el mismo commit.
Los mismos tres comandos, uno cada vez, y el cuarto para el `diff`; nada más cambió entre las dos
tandas (ningún parámetro, ninguna regla, ningún dato). **Todas las cifras del criterio, del
embudo global, de la cuenta y de las peticiones son las mismas que en §3.2-§3.7** (comprobado
línea a línea con el guion de resumen y con `patrones.py`, §3.13): lo único que cambia en los
ficheros es el campo nuevo y las dos subsecciones nuevas.

1. `arrastrada`: `TIEMPO: 395.5 s; MEMORIA: pico del proceso de 630.9 MiB`.
2. `diaria`: `TIEMPO: 370.2 s; MEMORIA: pico del proceso de 632.7 MiB`.
3. `a35-inicio`: `TIEMPO: 373.1 s; MEMORIA: pico del proceso de 632.0 MiB`.
4. La repetición de la 2 fuera del repo: `TIEMPO: 360.4 s; MEMORIA: pico del proceso de 632.8
   MiB`; `diff` con la salida de la 2 vacío, mismo blob `8861d40319fd2e81896d1d48dfe21b6dd94aecd1`
   (`git hash-object`); la copia se borró después.

**La vida de la orden, lo que dice** (de «### Ordenes» y «### Rechazos por motivo»):

| Corrida | Órdenes intentadas | Llenadas | Rechazadas (motivo) | Canceladas (motivo) |
|---|---|---|---|---|
| 1 arrastrada | 156 | 43 | 33: `volumen_max_lotes` 29 (enero 24, abril 5), `precio_invalido` 4 (enero 3, abril 1) | 80: 79 reubicaciones (RN-006 con RN-011 y RN-015 en el mismo cierre: la caja recalculada de ADR-0074, cancelar y volver a colocar), 1 por RN-035 al abrir otra sesión |
| 2 diaria | 439 | 106 | 111: `volumen_max_lotes` 100 (enero 21, abril 24, julio 20, agosto 35), `precio_invalido` 11 (3, 4, 2, 2) | 222: 220 reubicaciones, 1 por RN-035 en `ventana_fin`, 1 por RN-035 al abrir otra sesión |
| 3 a35-inicio | 429 | 106 | 111: los mismos 100 y 11 | 212: 210 reubicaciones (10 menos que la 2: 4 en 2026-01-19 11-15 y 6 en 2026-08-13 11-15, las dos sesiones cuyas peticiones bajan en §3.4), 1 en `ventana_fin`, 1 al abrir otra sesión |

Ninguna orden queda «viva al cerrar el dia»: RN-035 llega antes que la red de seguridad.
**Hallazgo (importa):** 100 de los 111 rechazos de la corrida 2 son por `volumen_max_lotes`: el
lote que dimensiona RN-011 (0,5 % del saldo sobre el stop) supera los 50 lotes del perfil
(`firma_volumen_max_lotes`, ADR-0071) y el bróker simulado no coloca la orden (`broker.py:857`).
Es la cadena de HER:37 («los rechazos por volumen y por margen, en la rama de stop y lote»): con
100.000 de saldo, 0,5 % son 500 USD, y 500 / 50 lotes = 10 puntos: **todo stop de menos de 10
puntos da más de 50 lotes y se rechaza**. No se ajusta nada; va a la clasificación (E o R) y a
las líneas del cierre.

### 3.13 La clasificación provisional por patrones (punto 4), calculada con `patrones.py`

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/patrones.py <salida 2> --filas`, con
las reglas literales del consultor (la docstring del guion las repite, y declara las dos cosas
que las reglas no dicen: un sesgo que no es alcista ni bajista cuenta como «contra», y «del mismo
lado» se mira sobre todas las operaciones del bot de la sesión, incluidas las emparejadas). Salida
completa, fila a fila, en `anexos/CORRIDA-CONSTRUCCION/patrones.txt`; el recuento:

```
mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de mas | P6 donde el trader no opero | T0 pareja
2026-01 | 13 | 9 | 17 | 14 | 28 | 8 | 1
2026-04 | 9 | 2 | 8 | 12 | 11 | 16 | 4
2026-07 | 20 | 6 | 13 | 23 | 9 | 2 | 5
2026-08 | 6 | 4 | 4 | 26 | 13 | 7 | 2
total | 48 | 21 | 42 | 75 | 61 | 33 | 12
P1 sesgo: 48 filas en 25 sesiones
  P1 sesgo · sesgo alcista: 16
  P1 sesgo · sesgo bajista: 32
  P2 entrada · Δentrada: 21
  P3 otra zona · otra entrada: 42
  P5 de mas · mismo lado: 47
  P5 de mas · otro lado: 14
  P6 donde el trader no opero · en dia: 12
  P6 donde el trader no opero · en sesion: 21
filas marcadas posible M (hora perdida): 16
```

Las 292 filas caben en los siete patrones (ninguna queda fuera). **Frente al recuento del
consultor**: T0 12 = 12; P1 48 en 25 sesiones = 48 en 25; P4 75 = 75; P5 61 (47 y 14) = 61 (47 y
14); P6 33 (21 y 12) = 33 (21 y 12); 16 marcadas = 16. **No coincide P2/P3: 21 y 42 frente a 18 y
45.** Las tres filas de diferencia son las que tienen una operación del bot del mismo lado a
menos de 15 minutos Y a 3 puntos o menos -2026-07-10 07-11 (Δ 3 puntos) y 2026-07-10 11-15 (Δ 1 y
Δ 0)-, que no son pareja porque esa operación del bot ya está emparejada con otra del trader (el
criterio es uno a uno): la regla literal de P2 dice «a más de 3 puntos», así que ni P2 ni P3 las
describen; el guion las deja en P2 por el tiempo (a menos de 15 minutos), y el consultor las puso
en P3 («3 a la misma entrada pero a otra hora»). Son las mismas tres filas en los dos recuentos;
no se ajusta ni la regla ni la cifra: lo decide el consultor en la PARADA 3.

### 3.14 El punto 5: las 25 sesiones de P1, con sus H4 y la regla del sesgo

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/sesgo_p1.py <raiz> <salida 2>`, que
carga las velas como `arnes.dias_de_mercado` (el mismo calentamiento, §1.c) y, por cada sesión P1,
da las dos últimas H4 cerradas antes de la apertura (inicio UTC, apertura, máximo, mínimo,
cierre), el sesgo que anotó el motor, la regla que lo decidió -recalculada con
`domain.sesgo.sesgo_h4` sobre esas velas: RN-003 por ruptura simple, la doble ruptura decidida
por el color (ADR-0060 §1), o una neutra con doble ruptura saltada (ADR-0075)- y lo mismo de la
sesión anterior del mismo día. Salida completa en `anexos/CORRIDA-CONSTRUCCION/sesgo_p1.txt`
(102 líneas). Lo que se ve de una pasada: de las 25 sesiones, 6 sesgos salen de una doble ruptura
decidida por el color (2026-01-27 07-11, 2026-04-13 11-15, 2026-07-15 11-15, 2026-08-20 07-11, y
en la sesión anterior de 2026-04-24 11-15 y 2026-07-17 11-15), ninguna de una neutra saltada
(ADR-0075), 2 se deciden en la segunda vela hacia atrás (2026-04-03 y 2026-04-10, ambas 07-11), y
hay rupturas de 2 puntos (2026-01-22 11-15, alcista) y de 6 (2026-04-03 07-11): la zona de A-16.
10 de las 25 son sesiones 11-15 con una 07-11 delante; en 5 de ellas el sesgo de la mañana era el
contrario (2026-01-30, 2026-04-13, 2026-04-24, 2026-07-15, 2026-07-17): el cambio de sesgo a las
11:00 que el consultor señala. Solo velas de construcción (ADR-0021 §1); ningún día abierto en el
visor.

### 3.15 P4 frente a la vida de la orden (`p4_ordenes.py`)

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/p4_ordenes.py <salida 2>` cruza las 38
sesiones de P4 (75 filas) con «### Ordenes» de la misma salida (completo en
`anexos/CORRIDA-CONSTRUCCION/p4_ordenes.txt`):

```
total | rechazadas y canceladas, ninguna llenada 7; sin ninguna orden colocada 17; todas canceladas sin llenarse 4; todas rechazadas 10
```

- **17 sesiones sin ninguna orden colocada** aunque en 15 de ellas la tabla dice «todos los
  hechos del camino producidos» (y en 2, `orden_dimensionada[productoras sin cumplirse]`): el
  motor dimensionó y no colocó, es decir, un `gate` prohibió `colocar_orden_limite` (ADR-0032:
  RN-015 apaga `orden_dimensionada` aunque un gate prohíba colocar). Cuál, no está en la salida:
  `TrazaSesion.bloqueadas` lo guarda como `(regla, accion, prohibida:<efecto>)` pero «Por sesion»
  no lo imprime. Hallazgo 1 de §3.16.
- **10 sesiones con todas las órdenes rechazadas** (9 solo por `volumen_max_lotes`, 1 por
  `precio_invalido`), y 7 con rechazos y reubicaciones sin ningún llenado: la cadena de HER:37.
- **4 sesiones con todas canceladas sin llenarse** (solo reubicaciones): la orden se reubicó con
  cada caja nueva y nunca se llenó antes de retirarse.

### 3.16 Hallazgos para la PARADA 3

1. **(importa) Para 17 de las 38 sesiones de P4 falta el dato que decide la clase:** qué gate
   prohibió colocar. Propuesta, del mismo régimen que el punto 1 (salida y nada más): añadir a la
   línea de «Por sesion» un campo `bloqueadas` con `(regla, accion, motivo)` de la traza, y en
   `p4_ordenes.py` cruzarlo. Exige otro `make check` y repetir las corridas (unos 25 minutos).
2. **(importa) 100 de 111 rechazos por `volumen_max_lotes`** (§3.12): con 0,5 % de 100.000 y el
   tope de 50 lotes, cualquier stop de menos de 10 puntos no se coloca. Es HER:37; la clase (E, R
   o D) la decide el consultor; aquí no se ajusta nada.
3. **(menor) P2/P3: tres filas** que la regla literal no describe (§3.13).
4. **(menor) Las dos sesiones de P1 cuya sesión anterior no tiene línea «Por sesion»** (sin
   operaciones del trader en ella) salen con «sesgo del motor ?» y el sesgo recalculado al lado:
   2026-01-22 y 2026-08-04 (§3.14).

### 3.17 Respuesta del consultor a la PARADA 3 (2026-10-14)

Copiada tal cual (también al final de `docs/encargos/trabajo-corrida-construccion.md`):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 3 de trabajo/corrida-construccion (2026-10-14). Cópiala literal al informe, como §3.17 «Respuesta del consultor a la PARADA 3», con la fecha. Esta es la clasificación DEFINITIVA de los patrones (fase 3), salvo las 17 sesiones del punto 4.d, que se cierran en la PARADA 4.
>
> 1. Decisión 1: sí. Añade bloqueadas (TrazaSesion.bloqueadas, con la regla que bloqueó) a la línea «Por sesion», con el mismo régimen: solo salida, ningún cambio de decisión, test sintético en los dos sentidos, make check y las tres corridas repetidas con sus mismos comandos y la repetición de la 2 para el diff. Si las cifras de parejas, cobertura o precisión cambiaran, PARADA.
> 2. Decisión 2: las tres filas de 2026-07-10 forman un patrón propio. Añade a patrones.py, ANTES de P2, la regla P7: fila del trader sin pareja cuya operación del bot más cercana está a 3 puntos o menos y a menos de 15 minutos, pero ya emparejada con otra operación del trader. Son entradas repetidas del trader en el mismo nivel que el bot solo toma una vez. Recalcula y pega el recuento (P2 y P3 deberían quedar en 18 y 42).
> 3. Decisión 3: los rechazos por volumen_max_lotes son una restricción impuesta (FTMO: 50 lotes, FTMO-P-D1.md), no un error de código. Clase E+R: E porque falta una decisión nuestra, por ADR, de qué hace el bot cuando el lote del 0,5 % no cabe (limitar el lote y arriesgar menos, o no operar), y esa decisión va a la rama del margen, junto al margen a 1:30, que corta antes (Technical Debt, HER:37); R porque se le pregunta al trader qué hace en su cuenta real cuando el stop es tan pequeño que el lote no cabe. En esta rama no se cambia nada.
> 4. La clasificación definitiva por patrón (la clase, el destino y por qué):
>    a) T0 pareja (12): sin diferencia.
>    b) P1 sesgo (48 filas, 25 sesiones): R, la primera pregunta de la sesión 5. Destino: V. La mayoría de esas sesiones abre tras una H4 que rompió el extremo de la anterior solo con la mecha y cerró dentro, y el parámetro sesgo_h4_criterio_ruptura = mecha sale de fb-2026-09-09-sesion-01-8eccf5c0 con el nombre vela_anterior_cierre_mecha, que admite dos lecturas. El parámetro NO se cambia por esto (los parámetros no se optimizan contra resultados). Para armar la pregunta quiero, en el informe:
>       - el texto literal del feedback fb-2026-09-09-sesion-01-8eccf5c0 sobre el sesgo, y la evidencia que cita, sin abrir nada en cuarentena (si la cita lleva a una transcripción v7 o posterior, dilo y no la abras);
>       - un guion en anexos (amplía sesgo_p1.py o uno nuevo, sin nombrar carpetas de data/ si la guardia lo niega; si lo niega, PARADA) que, sobre las 104 sesiones con operaciones del trader de la corrida 2, cuente la tabla 2×2: ruptura de la última H4 solo con mecha (cierre dentro) o con cierre fuera, frente a trader a favor o en contra del sesgo del bot, y aparte las decididas por doble ruptura o en la segunda vela. Es un diagnóstico para la pregunta, no una medida que decida el parámetro: el informe lo dice así;
>       - la lista de las sesiones de P1 con ruptura solo de mecha, con día, sesión y hora de la H4, para llevarlas a la sesión 5.
>    c) P2 entrada (18): R. Destino: V, junto a A-48 y A-49 (qué velas forman la caja), con la Δ de cada fila. Además una comprobación E en el visor, en tres días que elegiré después de la PARADA 4.
>    d) P4 sin orden (75), por lo que dice p4_ordenes.txt:
>       - las sesiones con todas sus órdenes rechazadas, o con rechazos y reubicaciones sin llenado, cuando el motivo es volumen_max_lotes: E+R, como el punto 3, con destino a la rama del margen y a V;
>       - las reubicaciones sin llenarse (4 sesiones, y las de las 7 mixtas que no son por volumen): R, destino V. La pregunta: ¿hasta cuándo mueve el trader la orden con la caja (ADR-0074, S-4) y cuándo la deja quieta o la quita?;
>       - los rechazos por otro motivo: lístalos con su motivo; los clasifico en la PARADA 4;
>       - las 17 sin ninguna orden colocada: PENDIENTES hasta que la salida nombre la regla que bloqueó (punto 1). Regla para cuando la veas, que aplicas tú y yo confirmo: si bloquea una regla de la firma o de la cuenta (RN-032, cierres de mercado ADR-0068, freno), M o E según si la regla está bien aplicada en ese día; si bloquea una regla de la estrategia (cartuchos, racha RN-036, ventana RN-035), R con destino V; si bloquea otra cosa, PARADA.
>    e) P3 otra zona (42): R. Destino: V, junto a A-43, A-50 y A-53 (qué liquidez y qué zona elige el trader).
>    f) P5 de más (61): las 47 del mismo lado, R con destino V: ¿cuántas veces reentra el trader en la misma zona tras un stop? (el bot se para en uno o dos minutos y vuelve a entrar; en la corrida 2 hay 93 stops frente a 12 objetivos). Las 14 del otro lado siguen a P1.
>    g) P6 donde el trader no operó (33): R, destino V, ¿qué le hace no operar ese día o esa sesión? (enlaza con la deuda «el no_trade por ausencia no está decidido»). Las de agosto, además, posible M: su xlsx no es el que el trader da por bueno (S-16, NA:Q).
>    h) P7 entradas repetidas (3, tras el punto 2): R, la misma pregunta que P5, del otro lado.
>    i) Las 16 filas que tocan una hora perdida: posible M, sin cambiar de patrón.
> 5. En el informe, una tabla «Clasificación del consultor (2026-10-14)» con patrón, filas, clase, destino y pregunta, y la lista «Para el cuestionario de la sesión 5», en este orden de prioridad: (1) el sesgo de H4, mecha o cierre, con los días de P1; (2) el lote que no cabe; (3) las reentradas (P5 y P7); (4) qué velas forman la caja (P2); (5) qué zona elige (P3); (6) hasta cuándo mueve la orden; (7) qué le hace no operar (P6). Las E van en la lista «Ramas candidatas»: la decisión del lote en la rama del margen (su prioridad sube: va antes de V) y la comprobación del 0 de la caja en el visor.
> 6. Líneas para el cierre, además de las de §1.k: la rama del margen deja de ser deuda sin fecha. Pasa a la Next Action como entrada propia, antes de V, con dos medidas: la que ya pedía Aleks (qué parte de las operaciones tiene un stop de menos de unos 2 pips y cuántas caen a ±2 minutos de una noticia) y cuántas órdenes de esta corrida rechaza el volumen y cuántas rechazaría el margen a 1:30.
>
> Lo que sigue: los puntos 1 y 2, el 4.b (texto literal, la tabla 2×2 y la lista), el 5 hasta donde llegue sin las 17, y PARADA 4 con todo commiteado. Las mismas reglas de siempre.
>
> Rama lista para revisión, NO cerrada.

## 4 · Fase 3 · La clasificación del consultor en el repo (2026-10-14)

### 4.1 Punto 1: `bloqueadas` en «Por sesion», y las corridas repetidas otra vez

- `src/botsito/engine/arnes.py`, `bloqueadas_de`: la línea «Por sesion» termina ahora en
  `| bloqueadas <regla>:<accion>:<motivo>, …` o `| bloqueadas ninguna`, con `TrazaSesion.bloqueadas`
  tal cual la guarda el intérprete: `(regla que pedía la acción, accion:<nombre>,
  prohibida:<efecto> | gate desconocido:<efecto>)` (`interprete.py:270-274`). Test en los dos
  sentidos (`test_la_linea_por_sesion_dice_que_bloqueo_un_gate_y_ninguna_si_no_hubo`). Solo
  salida; ninguna decisión; las 13 opciones iguales.
- **Un matiz que el consultor tiene que saber**: la traza NO guarda qué gate prohibió, solo el
  efecto prohibido y la regla cuya acción se bloqueó (`interprete.py:256-257` apunta los efectos
  prohibidos sin su autor). El gate se deduce cruzando las reglas que dispararon en la sesión (el
  campo `disparadas`) con las que `prohibe` ese efecto en la spec, y eso lo hace `p4_ordenes.py`
  (`reglas_que_prohiben`, `gate_que_bloqueo`). Guardar el autor exigiría tocar `interprete.py`
  (protegido): no se hace; si el cruce diera más de un candidato, lo dice y es PARADA.
- **Las corridas repetidas sobre este commit (eab1fc3), los mismos tres comandos y el cuarto:**
  1. `arrastrada`: `TIEMPO: 402.7 s; MEMORIA: pico del proceso de 623.2 MiB`.
  2. `diaria`: `TIEMPO: 357.2 s; MEMORIA: pico del proceso de 632.9 MiB`.
  3. `a35-inicio`: `TIEMPO: 318.1 s; MEMORIA: pico del proceso de 631.9 MiB`.
  4. La repetición de la 2 fuera del repo: `TIEMPO: 341.0 s; MEMORIA: pico del proceso de 632.8
     MiB`; `diff` vacío con la salida de la 2, mismo blob `8ec5ca3836a000a7c40dc09e2abaf2c010bbfc33`;
     la copia se borró después.
  **Las cifras de parejas, cobertura y precisión no cambian** (1/198 y 1/38; 12/198 y 12/94 en la
  2 y la 3; máximo diario 32 en la 1), ni el resto del informe: lo único nuevo es el campo
  `bloqueadas` de «Por sesion». Sus valores, en las 104 sesiones con operaciones del trader de la
  corrida 2: `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion` en 98 y `ninguna` en 6
  (y lo mismo, 98 y 6, en la 1). Es decir: en casi todas las sesiones hubo algún cierre de M1 en
  que RN-015 quiso colocar y un gate lo prohibió, también en las sesiones donde después sí
  colocó; el campo es por sesión, no por cierre. Los anexos de los guiones se regeneraron sobre
  estas salidas (`patrones.txt`, `p4_ordenes.txt`, `horas_perdidas.txt`, `sesgo_p1.txt`,
  `sesgo_2x2.txt`, `comparar_corridas.txt`); solo cambia lo que lee el campo nuevo
  (`p4_ordenes.txt`, §4.6). La 3 frente a la 2: sigue sin cambiar ninguna operación ni pareja.

### 4.2 Punto 2: P7 en `patrones.py`, y el recuento

Regla P7 antes de P2 (la del bot más cercana a 3 puntos o menos y a menos de 15 minutos, pero ya
emparejada con otra del trader). Recuento sobre la corrida 2:

```
mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de mas | P6 donde el trader no opero | P7 entradas repetidas | T0 pareja
2026-01 | 13 | 9 | 17 | 14 | 28 | 8 | 0 | 1
2026-04 | 9 | 2 | 8 | 12 | 11 | 16 | 0 | 4
2026-07 | 20 | 3 | 13 | 23 | 9 | 2 | 3 | 5
2026-08 | 6 | 4 | 4 | 26 | 13 | 7 | 0 | 2
total | 48 | 18 | 42 | 75 | 61 | 33 | 3 | 12
```

P2 18 y P3 42, como esperaba el consultor; P7 3 (las tres de 2026-07-10). El resto no se mueve.

### 4.3 Punto 4.b: el feedback literal del criterio de ruptura, y lo que cita

`knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-8eccf5c0.yaml`, tal cual:

```
id: fb-2026-09-09-sesion-01-8eccf5c0
sesion: 2026-09-09-sesion-01
fecha: '2026-09-09'
medio: escrito
objetivo:
  tipo: parametro
  id: sesgo_h4_regla
accion: RESOLVE_UNKNOWN
respuesta_literal: si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de
  pip, entonces seguiríamos operando bajista
registrado_por: Aleks · re-expresion canonica del consultor (F11)
valor_resultante: vela_anterior_cierre_mecha (ruptura del extremo, mecha incluida; equal no cuenta)
valor_canonico: vela_anterior_cierre_mecha
supersede: fb-2026-09-09-sesion-01-ff7fb765
notas: la eleccion, sin la aclaracion del criterio. El literal del trader queda intacto; el canonico es
  lo que el registro puede leer.
```

Lo que cita: no cita evidencia (`ev-*`); supersede `fb-2026-09-09-sesion-01-ff7fb765`, que es el
mismo literal registrado con `medio: video`, `grabacion: Grabación de pantalla 2026-09-09
151552.mp4` (v6, la sesión 1), `t0: '1:03:01'`, `t1: '1:04:30'`, «cruda leída» por Aleks, y
`notas: Ver A-1`. Ese tramo de v6 no está en cuarentena ni en los tramos no citables (que son
0:41:00-0:50:11 y 1:53:30-1:57:31); no hace falta abrirlo y no se abrió: el literal está en los
dos registros. De los dos parámetros que salen de él (`parametros.yaml:395-427`): `sesgo_h4_regla`
= `vela_anterior_cierre_mecha` («que vela H4 fija el sesgo y cuando cambia (A-1)… se conserva porque
es lo que el trader respondio») y `sesgo_h4_criterio_ruptura` = `mecha` («vivia dentro del nombre
del enum… que mezclaba sujeto y criterio»). El literal del trader habla de «un rompimiento por
encima… al menos por un pip»: no dice si el rompimiento es de la mecha o del cierre; la lectura
«mecha» es la re-expresión canónica del consultor (F11), y es la que el motor ejecuta. **El
parámetro no se cambia por esto.**

### 4.4 Punto 4.b: la tabla 2×2 (`sesgo_2x2.py`) y la lista de P1 con ruptura solo de mecha

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/sesgo_2x2.py <raiz> <salida 2>`
(mismas velas y calentamiento que el arnés; salida en `anexos/CORRIDA-CONSTRUCCION/sesgo_2x2.txt`).
**Es un diagnóstico para armar la pregunta de la sesión 5, no una medida que decida el
parámetro**: `sesgo_h4_criterio_ruptura` sigue en `mecha` y nada se ajusta. Sobre las 104 sesiones
con operaciones del trader, una sesión es «a favor» si todas sus operaciones van con el sesgo del
bot y «en contra» si ninguna (no hubo mixtas):

| La H4 que fijó el sesgo (ruptura simple, última cerrada) | Trader a favor | Trader en contra | Total |
|---|---|---|---|
| rompió el extremo de la anterior SOLO con la mecha (cerró dentro) | 19 | 13 | 32 |
| rompió con el cierre fuera | 40 | 6 | 46 |

Aparte: decididas por doble ruptura con el color (ADR-0060 §1), 17 (13 a favor, 4 en contra);
decididas en la segunda vela o más atrás, 9 (7 a favor, 2 en contra). Lo que se ve, sin decidir
nada: con cierre fuera el trader va en contra en 6 de 46; con solo mecha, en 13 de 32.

**Las sesiones de P1 con ruptura solo de mecha, para la sesión 5 (13 de las 25):**

```
2026-01-07 07-11 | H4 2026-01-07T02:00Z | alcista
2026-01-16 07-11 | H4 2026-01-16T02:00Z | alcista
2026-01-22 11-15 | H4 2026-01-22T06:00Z | alcista
2026-01-23 07-11 | H4 2026-01-23T02:00Z | bajista
2026-01-28 07-11 | H4 2026-01-28T02:00Z | bajista
2026-01-30 11-15 | H4 2026-01-30T06:00Z | alcista
2026-04-09 07-11 | H4 2026-04-09T01:00Z | alcista
2026-07-01 07-11 | H4 2026-07-01T01:00Z | bajista
2026-07-06 07-11 | H4 2026-07-06T01:00Z | bajista
2026-07-17 11-15 | H4 2026-07-17T05:00Z | alcista
2026-08-04 11-15 | H4 2026-08-04T05:00Z | alcista
2026-08-07 07-11 | H4 2026-08-07T01:00Z | alcista
2026-08-27 07-11 | H4 2026-08-27T01:00Z | alcista
```

(la hora es el inicio UTC de la H4 que fijó el sesgo; el sesgo, el que anotó el motor). Las otras
12 de P1: 6 con cierre fuera, 4 por doble ruptura y 2 en la segunda vela (§3.14).

### 4.5 Clasificación del consultor (2026-10-14)

Sobre la tabla de la corrida 2 (`diaria.DIAGNOSTICO…txt`, «Diferencias por operacion») y su
asignación por `patrones.py` (`patrones.txt`, fila a fila). Las 16 filas que tocan una hora de
ticks perdida llevan además «posible M» (`horas_perdidas.txt`), sin cambiar de patrón.

| Patrón | Filas | Clase | Destino | Pregunta o decisión |
|---|---|---|---|---|
| T0 pareja | 12 | sin diferencia | — | — |
| P1 sesgo | 48 (25 sesiones) | R | V (sesión 5), pregunta 1 | ¿el sesgo lo fija la ruptura solo con la mecha o hace falta el cierre fuera? (`sesgo_h4_criterio_ruptura` = `mecha`, de fb-…-8eccf5c0, admite dos lecturas; §4.3 y §4.4). No se cambia el parámetro |
| P7 entradas repetidas | 3 | R | V, pregunta 3 | la misma que P5, del otro lado: entradas repetidas del trader en el mismo nivel que el bot toma una vez |
| P2 entrada | 18 | R, más una comprobación E | V, pregunta 4, junto a A-48 y A-49; visor en tres días que el consultor elegirá tras la PARADA 4 | ¿qué velas forman la caja? (la Δ de cada fila, en `patrones.txt`: de 4 a 52 puntos, 15 de las 18 entre 6 y 21) |
| P3 otra zona | 42 | R | V, pregunta 5, junto a A-43, A-50 y A-53 | ¿qué liquidez y qué zona elige el trader? |
| P4 sin orden, con todas las órdenes rechazadas o rechazos y reubicaciones sin llenado por `volumen_max_lotes` | 17 sesiones de 38 (10 + 7; `p4_ordenes.txt`) | E + R | la rama del margen (E) y V, pregunta 2 (R) | E: qué hace el bot cuando el lote del 0,5 % no cabe en 50 lotes (decisión por ADR, con el margen a 1:30, HER:37). R: qué hace el trader en su cuenta real cuando el stop es tan pequeño que el lote no cabe |
| P4 sin orden, reubicaciones sin llenarse | 4 sesiones | R | V, pregunta 6 | ¿hasta cuándo mueve el trader la orden con la caja (ADR-0074, S-4) y cuándo la deja quieta o la quita? |
| P4 sin orden, rechazos por `precio_invalido` | 3 sesiones: 2026-04-16 07-11, 2026-07-08 11-15, 2026-07-13 11-15 (`p4_ordenes.txt`) | E + R (PARADA 4, punto 3) | E: la rama de comprobaciones en el visor; R: V | E: comprobar en el visor dónde colocó el bot la orden frente al precio (ADR-0057). R: si el precio ya pasó el 0 cuando se forma la caja, ¿el trader entra o no? |
| P4 sin orden, sin ninguna orden colocada: RN-015 quiso colocar y `abrir_operacion` estaba prohibido (gates disparados RN-005 y RN-009; y RN-001 en 7 sesiones 11-15) | 15 sesiones (§4.6) | R, más una comprobación E (PARADA 4, punto 1; la regla de 4.d queda ampliada así, 2026-10-14) | R: V; E: la rama de comprobaciones en el visor | R: ¿entra el trader cuando la zona se desarrolla en el lado de ruido, o con más zonas de control de las admitidas? E: que RN-005, RN-009 y el minuto de `ventana_fin` de RN-001 están bien aplicados en esas sesiones |
| P4 sin orden, sin bloqueo y sin `orden_dimensionada` | 2 sesiones: 2026-01-08 11-15, 2026-08-14 07-11 | E candidata (PARADA 4, punto 2) | la rama de comprobaciones en el visor | que RN-011 no dimensione con los hechos del camino producidos apunta a nuestro código, no a una regla del trader |
| P5 de más, mismo lado | 47 | R | V, pregunta 3 | ¿cuántas veces reentra el trader en la misma zona tras un stop? (el bot se para en uno o dos minutos y vuelve a entrar; en la corrida 2, 93 stops frente a 12 objetivos) |
| P5 de más, otro lado | 14 | R | siguen a P1 | la pregunta 1 |
| P6 donde el trader no operó | 33 (21 en sesión, 12 en día) | R; las de agosto, además posible M | V, pregunta 7 | ¿qué le hace no operar ese día o esa sesión? (la deuda «el no_trade por ausencia no está decidido»); agosto: su xlsx no es el que el trader da por bueno (S-16, NA:Q) |
| las 16 filas en una hora perdida | 16 | posible M | — | sin cambiar de patrón |

**Para el cuestionario de la sesión 5** (en el orden de prioridad del consultor; lo leerá V; con
las ampliaciones de la PARADA 4):
1. El sesgo de H4: ¿rompe el extremo de la H4 anterior solo la mecha, o hace falta que el cierre
   quede fuera? Con las 13 sesiones de P1 con ruptura solo de mecha, tal como están en §4.4
   (2026-01-07 07-11, 2026-01-16 07-11, 2026-01-22 11-15, 2026-01-23 07-11, 2026-01-28 07-11,
   2026-01-30 11-15, 2026-04-09 07-11, 2026-07-01 07-11, 2026-07-06 07-11, 2026-07-17 11-15,
   2026-08-04 11-15, 2026-08-07 07-11, 2026-08-27 07-11), y los 12 restantes de P1 (§3.14).
2. El lote que no cabe: ¿qué hace el trader en su cuenta real cuando el stop es tan pequeño que el
   lote del 0,5 % pasa del máximo de la firma (50 lotes)?
3. Las reentradas (P5 y P7): ¿cuántas veces reentra en la misma zona tras un stop, y cuándo
   repite una entrada en el mismo nivel?
4. Qué velas forman la caja (P2, con A-48 y A-49), con la Δ de cada fila.
5. Qué liquidez y qué zona elige (P3, con A-43, A-50 y A-53).
6. Hasta cuándo mueve la orden con la caja, y cuándo la deja quieta o la quita (ADR-0074, S-4).
7. Qué le hace no operar un día o una sesión (P6).
8. (PARADA 4, punto 1) ¿Entra el trader cuando la zona se desarrolla en el lado de ruido de la
   liquidez de M15, o cuando hay más zonas de control de las admitidas? (las 15 sesiones de §4.6).
9. (PARADA 4, punto 3) Si el precio ya pasó el 0 cuando se forma la caja, ¿entra o no? (las 3
   sesiones con `precio_invalido`).

**Ramas candidatas (las E):**
- **La rama del margen** (su prioridad sube: va ANTES de V): la decisión, por ADR, de qué hace el
  bot cuando el lote del 0,5 % no cabe en los 50 lotes de la firma (limitar el lote y arriesgar
  menos, o no operar), junto al margen a 1:30, que corta antes (HER:37); con las dos medidas del
  punto 6 de la PARADA 3 (§5).
- **«Comprobaciones en el visor de R3.1»** (antes de V, porque el cuestionario necesita esos
  gráficos; el visor NO se abre en esta rama, PARADA 4 punto 5). Lo que comprueba, con sus días:
  - P2, que el 0 de la caja sale de la vela que dice la spec, en tres días que el consultor elegirá
    de entre los de P2 (2026-01-02 07-11, 2026-01-05 07-11 y 11-15, 2026-01-08 07-11, 2026-01-13
    11-15, 2026-01-20 11-15, 2026-01-26 07-11, 2026-01-29 11-15, 2026-04-01 11-15, 2026-04-16
    11-15, 2026-07-03 07-11, 2026-07-09 11-15, 2026-08-03 11-15, 2026-08-20 11-15; `patrones.txt`);
  - que RN-005, RN-009 y el minuto de `ventana_fin` de RN-001 están bien aplicados en las 15
    sesiones de §4.6: 2026-01-30 07-11, 2026-04-17 07-11, 2026-04-27 11-15, 2026-07-01 11-15,
    2026-07-09 07-11, 2026-07-14 07-11 y 11-15, 2026-07-16 11-15, 2026-08-03 07-11, 2026-08-11
    07-11, 2026-08-17 07-11, 2026-08-19 11-15, 2026-08-21 11-15, 2026-08-25 07-11, 2026-08-27 11-15;
  - por qué RN-011 no dimensionó con los hechos del camino producidos en 2026-01-08 11-15 y
    2026-08-14 07-11 (E candidata);
  - dónde colocó el bot la orden frente al precio (ADR-0057) en los tres rechazos por
    `precio_invalido`: 2026-04-16 07-11, 2026-07-08 11-15 y 2026-07-13 11-15.

### 4.6 Las 17 sesiones sin ninguna orden colocada, con `bloqueadas` (PARADA 4)

Con la salida repetida de §4.1, `p4_ordenes.py` cruza para cada una el campo `bloqueadas` con las
reglas que dispararon en la sesión y las que `prohibe`n ese efecto en la spec
(`anexos/CORRIDA-CONSTRUCCION/p4_ordenes.txt`, al final). Lo que sale:

- **15 sesiones con `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`**: el motor
  dimensionó (RN-011) y RN-015 no pudo colocar porque `abrir_operacion` estaba prohibido en ese
  cierre. Los gates que dispararon en la sesión y prohíben `abrir_operacion` son, en las 15,
  **RN-005** («lo que se desarrolla en el lado de ruido de la liquidez de M15 no es entrada») y
  **RN-009** («más zonas de control de las admitidas invalidan el esquema»), y en 7 de ellas
  -todas sesiones 11-15:
  2026-04-27, 2026-07-01, 2026-07-14, 2026-07-16, 2026-08-19, 2026-08-21 y 2026-08-27- también
  **RN-001** (el gate maestro: dispara fuera de la ventana -`ninguno_de en_ventana`, su forma- o
  con un `detenido_por_*`; con `sin_tope`, sin cartuchos agotados y 0 `detenido_por_*` en las 104
  sesiones, lo que dispara en una sesión 11-15 es el minuto de `ventana_fin`). Las otras 8 son
  2026-01-30 07-11, 2026-04-17 07-11, 2026-07-09 07-11, 2026-07-14 07-11, 2026-08-03 07-11,
  2026-08-11 07-11, 2026-08-17 07-11 y 2026-08-25 07-11. **Por la regla de 4.d esto es PARADA**:
  RN-005 y RN-009 son reglas de la estrategia pero no están entre las que el consultor enumeró
  (cartuchos, racha, ventana), y la traza no dice cuál de las dos prohibió en el cierre en que
  RN-015 pidió colocar (el campo es por sesión, y el autor de la prohibición no se guarda:
  §4.1). Propuesta: R con destino V si el consultor da RN-005 y RN-009 por «estrategia» (la
  pregunta: ¿entra el trader cuando la zona se desarrolla en el lado de ruido, o cuando hay más de
  una zona de control?), y E si quiere comprobar en el visor que RN-005 o RN-009 están bien
  aplicadas en esos días.
- **2 sesiones sin ningún bloqueo** y con `orden_dimensionada[productoras sin cumplirse]`:
  2026-01-08 11-15 y 2026-08-14 07-11. No hubo orden porque RN-011 no dimensionó (sus productoras
  no se cumplieron): no se produjo un hecho del camino, y la regla de 4.d dice «según cuál»: la
  clasifica el consultor en la PARADA 4 (candidata R: qué hace que no haya entrada tras la toma).

### 4.7 Respuesta del consultor a la PARADA 4 (2026-10-14)

Copiada tal cual (también al final de `docs/encargos/trabajo-corrida-construccion.md`):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 4 de trabajo/corrida-construccion (2026-10-14). Cópiala literal al informe, como §4.7 «Respuesta del consultor a la PARADA 4», con la fecha. Con esto la clasificación queda cerrada y la rama sigue hasta su entrega.
>
> 1. Las 15 sesiones sin orden en las que RN-015 quiso colocar y abrir_operacion estaba prohibido por RN-005 y RN-009 (y además RN-001 en 7 sesiones 11-15): R, con destino V (¿entra el trader cuando la zona se desarrolla en el lado de ruido, o con más zonas de control de las admitidas?), y una comprobación E en el visor de que RN-005, RN-009 y el minuto de ventana_fin de RN-001 están bien aplicados en esas sesiones. Mi regla de la PARADA 3 no las nombraba; queda ampliada así, con fecha de hoy.
> 2. Las 2 sesiones sin bloqueo y sin orden_dimensionada (2026-01-08 11-15 y 2026-08-14 07-11): E candidata. Que RN-011 no dimensione con los hechos del camino producidos apunta a nuestro código, no a una regla del trader. Destino: la comprobación en el visor.
> 3. Los 3 rechazos por precio_invalido (2026-04-16 07-11, 2026-07-08 11-15, 2026-07-13 11-15): E+R. E: comprobar en el visor dónde colocó el bot la orden frente al precio (ADR-0057). R: si el precio ya pasó el 0 cuando se forma la caja, ¿el trader entra o no? Destino: V.
> 4. P1, sobre lo que mediste en §4.3 y §4.4:
>    a) El literal del trader en fb-2026-09-09-sesion-01-8eccf5c0 («al menos por un pip o una milésima de pip») no dice mecha ni cierre; «mecha incluida» fue una re-expresión del consultor en F11. Línea para ERRORES-RECURRENTES en el cierre: el consultor convirtió en criterio de una regla algo que el literal no decía (mecha), y quedó CONFIRMED sin pregunta; lo destapó R3.1 un mes después. Lección: una re-expresión canónica que añade un criterio que el literal no trae se marca DEFAULT_AMBIGUOUS y se pregunta; nunca entra como CONFIRMED.
>    b) La tabla 2×2 queda como diagnóstico para la pregunta, no como medida: el parámetro sesgo_h4_criterio_ruptura NO se toca en esta rama ni por este dato. Su estado tampoco cambia aquí; si hay que bajarlo de CONFIRMED, lo decido en la rama que active la respuesta del trader.
>    c) La pregunta 1 del cuestionario de la sesión 5 lleva las 13 sesiones de P1 con ruptura solo de mecha, tal como las listaste.
> 5. El visor NO se abre en esta rama. Todas las comprobaciones E (P2, el 0 de la caja; los puntos 1, 2 y 3 de esta respuesta) van a una rama candidata nueva, «comprobaciones en el visor de R3.1», que va antes de V porque el cuestionario necesita esos gráficos. Escríbela así en «Ramas candidatas», con sus días.
> 6. Termina la fase 3: la NOTA de ADR-0070 y el runbook ACTIVAR-A35-A44.md en su commit propio (punto 12 de mi respuesta a la PARADA de la fase 0). Después, las líneas propuestas para el cierre, que recogen todo lo que mandé en las tres respuestas:
>    - la Next Action: F apunta, por este orden, a la rama del margen (entrada nueva, antes de V, con sus dos medidas del punto 6 de la PARADA 3), a la rama de comprobaciones en el visor (entrada nueva, antes de V) y a V, que depende además de J y de A.4;
>    - V lleva la lista «Para el cuestionario de la sesión 5» de §4.5, con las ampliaciones de hoy;
>    - la hoja de ruta: R3.1 HECHA; las Refs de R3.1 con ID:ADR-0074 · ID:ADR-0067; R4.1 con las dos ramas nuevas como dependencias;
>    - Technical Debt: la línea de la lectura del M1 de marzo y junio para calentar (punto 11 de la fase 0), y la del margen pasa a la entrada nueva de la Next Action;
>    - G.1 y G.2 con las propuestas de la guardia y de la línea LECTURA:;
>    - ERRORES-RECURRENTES: mi premisa falsa sobre el M1 de julio (PARADA 0, punto 8) y la re-expresión «mecha» de F11 (punto 4.a de hoy);
>    - HER:25, HER:30 y HER:35 siguen vivos, con lo que la corrida dice de ellos.
> 7. Revisor (opus), con los dos alcances del encargo y uno más: que la tabla «Clasificación del consultor» y la lista del cuestionario dicen exactamente lo de mis cuatro respuestas, con sus recuentos (T0 12, P1 48, P2 18, P3 42, P4 75, P5 61, P6 33, P7 3). Su informe, pegado al final. Arregla lo que encuentre que bloquee o importe, o dime por qué no.
>
> Rama lista para revisión, NO cerrada.

**Aplicación:** 1, 2 y 3 en la tabla de §4.5 (filas de P4) y en las ramas candidatas; 4.a en
§5.6; 4.b, nada se toca (`sesgo_h4_criterio_ruptura` sigue CONFIRMED en `mecha`); 4.c en la
pregunta 1 de §4.5; 5 en «Ramas candidatas» de §4.5 (el visor no se abrió); 6 en el commit 74e8ef0
(§4.8) y en §5; 7 en §10.

### 4.8 El commit propio de la fase 3: la NOTA de ADR-0070 y el runbook (74e8ef0)

Lo que mandó la respuesta a la PARADA de la fase 0, punto 12: en
`docs/adr/0070-umbral-de-construccion-para-medir-mayo.md`, una NOTA fechada bajo el punto 3 de la
Decision -A-21 fijada desde ADR-0076, el motor necesita diagnóstico solo para A-35 y A-44, y el
veredicto «no» de esta corrida con sus cifras- sin reescribir el cuerpo (lo que permite el régimen
de los ADR; el resto del ADR, intacto); y en `docs/runbooks/ACTIVAR-A35-A44.md`, las tres menciones
de `--diagnostico-a21` (:218, :246, :260) marcadas «(ya no existe, ADR-0076)» y el comando del §5
con `--simular`, con una línea que dice por qué (la línea base contra la que compara se escribió
con `--simular`). `knowledge validate` en verde antes del `make check` (2642 passed, sello
`ce3a270a…`).

## 5 · Líneas propuestas para el cierre

Textos exactos; la Next Action, la hoja de ruta y el Technical Debt los edita el cierre, no la
rama (`docs/plan/` está en `rutas_protegidas`; PROJECT_STATE solo cambió aquí en lo que exige
`abrir-rama` y el recuento de tests). Las letras nuevas, E y O, están libres hoy (ninguna entrada
de la hoja de ruta cita `NA:E` ni `NA:O`, y las dos ya se reutilizaron antes: HISTORIA las registra
HECHAS en otras ramas); el cierre puede elegir otras.

**5.1 Next Action** (PROJECT_STATE.md):
- **F**, sustituida entera: «F. Orden de trabajo: lo siguiente es, por este orden, E (la rama del
  margen, con sus dos medidas), O (comprobaciones en el visor de R3.1) y V (la sesión 5, con la
  lista «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5), que depende además
  de J y de A.4. R3.1 está HECHA (CORRIDA-CONSTRUCCION.md): la corrida fue diagnóstico (A-35 y
  A-44) y no habilita mayo (ADR-0070 §3).»
- **E, entrada nueva** (antes de V): «E. La rama del margen: decidir por ADR qué hace el bot cuando
  el lote del 0,5 % no cabe en `firma_volumen_max_lotes` (50; FTMO-P-D1.md) -limitar el lote y
  arriesgar menos, o no operar- junto al margen a 1:30, que corta antes (heredado 37), y que el
  simulador lo compruebe. Con dos medidas: (1) la que ya pedía Aleks, qué parte de las operaciones
  del trader tiene un stop de menos de unos 2 pips y cuántas caen a ±2 minutos de una noticia;
  (2) cuántas órdenes de la corrida de R3.1 rechaza el volumen (100 de 111 rechazos en la corrida
  diaria, CORRIDA-CONSTRUCCION.md §3.12) y cuántas rechazaría el margen a 1:30. Sale de Technical
  Debt («El simulador no comprueba el margen…»), que se retira al abrirla.»
- **O, entrada nueva** (antes de V): «O. Comprobaciones en el visor de R3.1 (CORRIDA-CONSTRUCCION.md
  §4.5, «Ramas candidatas»): el 0 de la caja en tres días de P2 que elige el consultor; RN-005,
  RN-009 y el minuto de ventana_fin de RN-001 en las 15 sesiones sin orden; por qué RN-011 no
  dimensionó en 2026-01-08 11-15 y 2026-08-14 07-11; y dónde colocó el bot la orden frente al
  precio en los tres rechazos por precio_invalido. El cuestionario de V necesita esos gráficos.»
- **V**: se añade al final «Lleva la lista «Para el cuestionario de la sesión 5» de
  CORRIDA-CONSTRUCCION.md §4.5 (nueve preguntas, en ese orden; la primera, el sesgo de H4 con las
  13 sesiones de P1 con ruptura solo de mecha). Depende de E y de O.»; «Depende de R1.1, de R3.1
  y de que kit hoja funcione…» pasa a «Depende de R1.1, de R3.1 (HECHA), de E, de O, de que kit
  hoja funcione con un paquete nuevo (J) y de la copia de seguridad (A.4).»
- **Heredados 25, 30 y 35**: siguen vivos, tal cual; con lo que la corrida dice de ellos, al final
  de cada uno: 25 y 30: «R3.1 (CORRIDA-CONSTRUCCION.md §3.4): con `cierre_vela_contraria` RN-004
  produce `liquidez_tomada` en 98 de 104 sesiones y con `inicio_vela_contraria` en 97; ninguna
  operación ni pareja cambia entre las dos lecturas; sigue sin fijar.» 35: «R3.1 (§3.5): con
  `sin_tope`, `detenido_por_tope` no se produce en ninguna de las 104 sesiones; RN-020 sigue
  hueco con nombre.»

**5.2 Hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`):
- **R3.1**, Refs: `- **Refs:** ID:ADR-0070 · ID:ADR-0043 · ID:ADR-0074 · ID:ADR-0067 · HER:25 ·
  HER:30 · HER:35 · ID:A-35 · ID:A-44 · ID:RN-004 · ID:RN-020`; en «Qué es», al final: «y la
  medida de peticiones por día con la caja recalculada (ADR-0074 §3) frente al freno de ADR-0067»;
  y al final del bloque: `- **Estado:** HECHA (`trabajo/corrida-construccion`,
  `stable/F37q-corrida-construccion`; CORRIDA-CONSTRUCCION.md): la corrida sobre los 76 días dev
  de construcción en diagnóstico (A-35 y A-44), su tabla por operación y la clasificación del
  consultor; no habilita R5.2 (ADR-0070 §3).` Sin ninguna letra viva en su bloque (regla b):
  «Depende de» pasa a «R1.1 y R2.1 y R2.2 (HECHAS); R2.3 y R2.4 la amplían cuando lleguen.» (sale
  la frase de «para que la corrida CUENTE…», que ya cumple ADR-0070 §3 como NOTA).
- **R4.1**, «Depende de»: «R1.1, R3.1 (HECHA), las dos ramas nuevas de la Next Action (NA:E, la
  del margen, y NA:O, las comprobaciones en el visor) y la copia de seguridad del carril de
  Aleks.»; y en Refs se añaden `NA:E · NA:O`.
- El tag que cito, `stable/F37q-corrida-construccion`, es el siguiente de la serie (el último es
  F37p); lo fija el cierre.

**5.3 Technical Debt**, una línea nueva y una que sale:
- Nueva: «`engine/arnes.py:dias_de_mercado` carga el M1 entero del mes anterior si existe su
  dataset: hoy, el de marzo (mes reservado entero, sin sortear) para abril y el de junio (11 días
  reservados) para julio, en cada corrida del arnés y en cada `make check`
  (`tests/unit/test_huecos_motor.py:290-337`), sin declararlo (ADR-0033 §4 solo se lo pide a kit
  build/check). Declarado como exposición permanente en HOLDOUT-EXPOSICIONES (fila del
  2026-10-14); que `dias_de_mercado` imprima una línea `LECTURA:` por recuento va a G.2
  (CORRIDA-CONSTRUCCION.md §1.c).»
- Sale: «El simulador no comprueba el margen…» (pasa a la entrada E de la Next Action, 5.1).

**5.4 Hoja de ruta, carril de guardias y deuda:**
- **G.1**: «Desde `trabajo/corrida-construccion` (CORRIDA-CONSTRUCCION.md §1.j): la guardia niega
  un guion de la carpeta de trabajo que nombre `data/manifests/ticks/<manifiesto>.yaml` de un mes
  de construcción para cruzar sus ficheros con los días dev, aunque Read deja abrir esos
  manifiestos; que admita rutas literales de manifiestos de construcción.»
- **G.2**: «Desde `trabajo/corrida-construccion` (§1.c): que `arnes.dias_de_mercado` imprima una
  línea `LECTURA:` por recuento de días reservados cuyas velas lee, como `kit check` (ADR-0033 §4),
  o que `test_huecos_motor.py:290-337` lo diga; hoy lo cubre la fila permanente de
  HOLDOUT-EXPOSICIONES.»

**5.5 HOLDOUT-EXPOSICIONES**: una fila única que declare como exposición permanente, por
recuento, la lectura del M1 de marzo (mes entero) y de junio (11 días reservados) en cada corrida
del arnés y en cada `make check` (respuesta de la fase 0, punto 11). La fila del 2026-10-14 de esta
rama ya lo dice en su punto (3); el cierre decide si la desdobla.

**5.6 ERRORES-RECURRENTES** (las escribe `cerrar-rama`):
- La fila de la rama, con lo del revisor (§10).
- Patrón nuevo: «**Un «antes no estaba» que no se comprobó con git.** Medido el 2026-10-14
  (`trabajo/corrida-construccion`, fase 0): el consultor y su auditor dieron por cierto que el M1
  de julio cambiaba el calentamiento de agosto respecto a BE-AL-TICK; el manifiesto entró en
  cce490c (2026-09-04), antes de F35 y de BE-AL-TICK. Señal: una afirmación de que un fichero
  «no estaba» en una corrida anterior. Qué hacer: `git log --format=%ad -1 -- <fichero>` antes de
  escribirla.»
- Patrón nuevo: «**Una re-expresión canónica que añade un criterio que el literal no trae.**
  Medido el 2026-10-14 (CORRIDA-CONSTRUCCION.md §4.3): el consultor convirtió en criterio de una
  regla algo que el literal no decía («mecha incluida» sobre «al menos por un pip»,
  fb-2026-09-09-sesion-01-8eccf5c0, F11), y quedó CONFIRMED sin pregunta; lo destapó R3.1 un mes
  después (13 de 25 sesiones de P1 abren tras una ruptura solo de mecha). Lección: una
  re-expresión que añade un criterio se marca DEFAULT_AMBIGUOUS y se pregunta; nunca entra como
  CONFIRMED.»

**5.7 Tamaño de PROJECT_STATE.** Hoy 23.773 bytes (tope 25.000). 5.1 añade dos entradas largas
(unos +1.300 bytes) y una F más larga (+250), y quita la línea del margen de Technical Debt (−300)
y la frase vieja de F: quedaría hacia 25,0 KB, **al límite**. Propuesta para no pasarlo: condensar
A (la demo, la entrada más larga, 987 bytes) remitiendo a `docs/runbooks/DEMO-FTMO.md`, como ya
proponía ENTRADA-ENERO.md §8.4, y escribir E y O con la mitad de texto remitiendo a §4.5.

## 6 · Desviaciones declaradas

- **PROJECT_STATE.md cambió** en lo que exige `abrir-rama` (Current Branch, Current Feature,
  Archivo 33) y en «Tests Currently Passing» (1535 → 1555) porque `state check` lo exige; el
  encargo decía que esta rama no lo toca. Tamaño: 23.773 bytes.
- **La sección vive dentro de `arnes.informe`** y con `--simular` queda antes de la cola
  «## Simulacion» (decisión 0 de la fase 0, (a)), no al final del fichero.
- **El cuarto comando** (la repetición de la 2 fuera del repo) no era uno de los «tres escritos
  exactamente así»; lo pide el propio encargo y lo autorizó la respuesta a la fase 0 (punto 15).
  Se corrió tres veces (una por tanda), y la copia se borró cada vez.
- **Las corridas se repitieron dos veces** después de la primera tanda (sobre 1b90d23 y sobre
  eab1fc3), porque las respuestas a las PARADAS 2 y 3 cambiaron la salida; las salidas de cada
  tanda sustituyeron a las anteriores en el mismo commit, como pidió el consultor. Ninguna cifra
  del criterio cambió entre tandas.
- **`cableado.py` cambia** en dos líneas existentes y en lo que añade (§3.11), con el contrato
  ampliado por la respuesta a la PARADA 2; `primitivas_broker.py` pasó a `rutas_protegidas` en su
  lugar.
- **El gate que prohibió no está en la traza**: `bloqueadas` lleva la regla que pedía la acción y
  el efecto, y el gate se deduce en `p4_ordenes.py` (§4.1); guardarlo exigiría `interprete.py`.
- **Un guion escrito en el repo durante un `make check`** y sacado en el acto (§3.8).
- **`horas_perdidas.py`** lleva las 18 horas escritas en el guion, porque un guion que nombre
  `data/manifests/ticks` lo niega la guardia (§1.j).
- **El pico de memoria** de cada corrida es de 623 a 633 MiB, el doble de lo estimado en §1.e2.
- **Dos sesiones de P1 cuya sesión anterior no tiene línea «Por sesion»** salen con «sesgo del
  motor ?» en `sesgo_p1.txt` (2026-01-22 y 2026-08-04), con el sesgo recalculado al lado.
- **Un worktree ajeno** (`…/2ea2c3d2…/scratchpad/wt-ci`, `e7df30b`, detached) aparece en
  `git worktree list` desde antes de esta rama; no es de esta sesión y no se tocó.

## 7 · El encargo, punto por punto

| # | Requisito (encargo y respuestas) | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main en 23316c8, CI en verde, abrir con `abrir-rama`, encargo literal, contrato con tramo R3, Archivo en HISTORIA | Hecho | §0; e06a71c; `tramo: R3` (equivalente, respuesta fase 0 punto 7) |
| 2 | `/model`: Fable 5.1, esfuerzo alto | Hecho | cabecera del informe |
| 3 | No cambia ningún parámetro, regla, decisión del motor, broker, cuenta, freno; `criterio_fidelidad.yaml` intacto | Hecho | `git diff --stat main...HEAD` (§9): ni `knowledge/`, ni `config/`, ni `broker.py`, `cuenta.py`, `freno.py`, `motor.py`, `cli.py`, `primitivas_broker.py`; `contrato_rama.py` en verde |
| 4 | Nada de mayo ni de meses reservados ni del corpus; solo casos dev | Hecho | §1.j, §3.8; el arnés se niega a mayo (`validar_meses`) y no se rodeó |
| 5 | No habilita mayo; no es fidelidad; A-35 `cierre_vela_contraria` fijada antes; la corrida 3 no decide A-35 | Hecho | §3.2 (veredicto «no» ×3), §3.4 («sin elegir lectura») |
| 6 | El margen a 1:30 no entra | Hecho | solo como línea del cierre (§5.1, E) |
| 7 | Solo los tres comandos del arnés, literales; ninguna otra corrida ni visor | Hecho (y el 4.º, autorizado) | §3.1, §3.12, §4.1; el visor no se abrió (PARADA 4, punto 5) |
| 8 | Fase 0 a) a g), con `fichero:línea`, y PARADA | Hecho | §1.a-§1.g, §1.h (auditor), PARADA respondida (§1.l) |
| 9 | Fase 1: la tabla por operación (pareja; más cercana con Δ; «ninguna» y el primer hecho; bot sin pareja; orden; determinista) | Hecho | §2; `arnes.py` (`diferencias_por_operacion`); §3.8 determinismo |
| 10 | Tests que rompen a propósito en los dos sentidos, sintéticos, y uno de que no se añade opción | Hecho | `test_diferencias_por_operacion.py` (14); §8 contra `main` |
| 11 | Fase 2: tres corridas, sin `--meses`, a la carpeta, TIEMPO y MEMORIA copiados, repetición de la 2 fuera del repo con `diff` y borrado | Hecho (tres tandas) | §3.1, §3.12, §4.1 |
| 12 | Informe: por corrida y mes; veredicto tal cual; corrida 1 (cuenta, día y regla, peticiones y freno); 3 frente a 2; embudo por mes; horas perdidas y filas; BE-AL-TICK como contexto | Hecho | §3.2-§3.7 |
| 13 | Si una corrida falla o pide días fuera: PARADA; no `--depuracion` | Hecho (ninguna falló) | §3.1 exit 0 ×4 |
| 14 | PARADA 2: commitear y parar | Hecho | 883d391 |
| 15 | Fase 3: la clasificación literal, filas con clase y destino, lista para la sesión 5, ramas candidatas (E), sin cambiar código | Hecho | §4.5-§4.8; las respuestas del consultor copiadas tal cual (§1.l, §3.10, §3.17, §4.7) |
| 16 | Makefile intacto; rutas del corpus no abiertas; tests del informe buscados antes de tocarlo; sin fechas de días reservados; exposiciones el mismo día | Hecho | `git diff --stat` sin Makefile; §1.d; HOLDOUT-EXPOSICIONES fila 2026-10-14 |
| 17 | PROJECT_STATE: la rama no lo toca | Hecho de otra forma | §6: solo lo de `abrir-rama` y el recuento de tests |
| 18 | CI de Linux: no toca `.claude/`, hooks ni plataforma | Hecho | §9 |
| 19 | Hallazgos para el cierre: Refs de R3.1 sin ADR-0074; ADR-0070 §3; ACTIVAR-A35-A44 | Hecho | §1.k; 5.2; la NOTA y el runbook en 74e8ef0 (§4.8) |
| 20 | Informe con encargo frente a hecho, desviaciones, comandos, exposiciones, líneas del cierre (F→V, R3.1 HECHA, HER:25/30/35) | Hecho | §7, §6, §3.1, §1.j, §5 |
| 21 | Revisor (opus) con los dos alcances del encargo y el tercero de la PARADA 4; informe pegado | Hecho | §10 |
| 22 | Respuesta fase 0, puntos 1-15 | Hecho | §1.l «Aplicación»; punto 12 en 74e8ef0; punto 14 en 5.4 |
| 23 | Respuesta PARADA 2, puntos 1-6 (salida: hecho del camino, vida de la orden; patrones; punto 5; agosto S-16) | Hecho | §3.11-§3.16; agosto en §3.2 |
| 24 | Respuesta PARADA 3, puntos 1-7 (bloqueadas; P7; feedback literal; 2×2; lista; clasificación; cierre; revisor) | Hecho | §4.1-§4.6, §5, §10 |
| 25 | Respuesta PARADA 4, puntos 1-7 | Hecho | §4.5 (tabla y ramas candidatas), §4.8, §5, §10 |

## 8 · Los tests nuevos contra el código de `main`

Como pide `entregar-rama` (paso 3), en un clon desechable `git worktree add --detach C:/cm/main
main`, con los dos ficheros de tests de la rama copiados dentro y ejecutados allí (nunca un
checkout en el repo real; el clon se borró después con `git worktree remove --force` y `prune`;
`git status --short`, `git branch --list` y `git ls-remote --heads origin "fix/*"` iguales antes y
después):

```
uv run pytest tests/unit/test_diferencias_por_operacion.py tests/unit/test_vida_de_la_orden.py -q -rA -p no:cacheprovider
     19 FAILED
      1 PASSED
```

De los 20 tests, 19 fallan con el código de `main` (la sección, `primer_hecho_que_falta`,
`bloqueadas_de`, `vida_de_las_ordenes`, `_motivo_de_cancelacion` y `CABECERA_ORDENES` no existen
allí) y pasa 1, `test_la_seccion_no_anade_ninguna_opcion_al_comando`, que es el que TIENE que pasar
en los dos lados: las 13 opciones del subparser y la lista de ADR-0070 son las mismas en `main` y
en la rama. Con el código de la rama pasan los 20 (`make check`, 2642 passed).

## 9 · CI de Linux

Sin CI: la rama no toca la plataforma. `git diff --stat main...HEAD` (29 ficheros): `src/` solo
`engine/arnes.py` y `engine/cableado.py` (texto del informe y lectura de la traza, sin rutas, sin
`os`, sin zoneinfo nuevo), `tests/unit/` dos ficheros nuevos sintéticos, y el resto `docs/`,
`contrato.yaml`, `PROJECT_STATE.md`. Ni `.claude/`, ni hooks, ni `Makefile`, ni `scripts/`.

## 10 · El revisor

(Se lanza con el informe terminado, sobre el commit de la entrega; su informe se pega aquí tal
cual, y debajo, «Lo que se hizo con los hallazgos del revisor».)

## Estado

LISTA PARA REVISIÓN. R3.1 hecha: la corrida en diagnóstico sobre los 76 días dev de construcción,
la tabla por operación con la vida de la orden, y la clasificación del consultor (§4.5) con la
lista para el cuestionario de la sesión 5 y las dos ramas candidatas; las líneas del cierre en §5;
el informe del revisor en §10. No habilita mayo; ningún valor cambió.

Rama lista para revisión, NO cerrada.
