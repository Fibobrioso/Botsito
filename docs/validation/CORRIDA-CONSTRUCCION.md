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

## Estado

EN CURSO. Fase 0 entregada el 2026-10-14; PARADA: esperando la respuesta del consultor a «Lo que
necesito que decidas». No se ha escrito código ni se ha corrido el arnés.
