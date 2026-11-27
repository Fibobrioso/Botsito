# RENOVAR-CIERRES-2025 · El calendario de cierres de EURUSD del perfil FTMO 2-Step Swing 100k, renovado hacia atrás hasta cubrir 2025 (R5.4 y R5.6, letra I)

> PLANTILLA: informe de la rama `trabajo/renovar-cierres-2026-11-26`. Estado: lista para revisión, NO cerrada (la PARADA (a)
> acotada a la Navidad de 2024, con su decisión en §3; el YAML renovado hasta el 2025-01-09). La fase 0, las Trading Updates leídas, los cierres que entran y los que no, las desviaciones, las
> comprobaciones, las líneas del cierre y el informe del revisor se escriben aquí según avanza la rama.

Rama `trabajo/renovar-cierres-2026-11-26`, abierta el 2026-11-26 desde `main` en 93a4fc29 (commit de
estado sobre el merge 4581f529 del tag `stable/F39q-f17-ordenes`). Encargo:
`docs/encargos/trabajo-renovar-cierres-2026-11-26.md`. Tramo: R5 (R5.4 y R5.6 de
`docs/plan/HOJA-DE-RUTA.md`; la letra I de la Next Action). Tag previsto:
`stable/F39r-renovar-cierres-2026-11-26`.

## Base comprobada (abrir-rama, paso 1)

- `git fetch origin`; `git status --short` vacío; `git rev-parse main origin/main`:
  `93a4fc2991b8a912b51072de7b8593cf0974883f` dos veces.
- `git rev-parse "stable/F39q-f17-ordenes^{commit}"` = `git rev-parse main^1` =
  `4581f529f2b5e7d3ff05d189fd2907746547a842`; en origin, `4ca20840…` (el objeto del tag anotado) y
  `4581f529…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 21967) y el último `stable/*`
  (`git tag --sort=-creatordate`: F39q, F39p, F39o).
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal
  `93a4fc2991b8a912b51072de7b8593cf0974883f` da el check `python` en `completed` / `success`, run
  **45922991122** (job 140257827342): confirma el número que vio el consultor.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## 0. Fase 0 · Inventario, sin escribir el YAML

### Por qué esta renovación, y por qué hacia atrás y por adelantado

El runbook solo pide renovar, en su condición 1, cuando una simulación pide días posteriores a
`hasta` (`docs/runbooks/RENOVAR-CIERRES.md`:14-18). Esta rama renueva HACIA ATRÁS y POR ADELANTADO:
lo piden como paso previo la letra I de la Next Action («Entra por su propia rama después de
renovar hacia atrás el calendario de cierres», `PROJECT_STATE.md`:36), R5.4
(`docs/plan/HOJA-DE-RUTA.md`:504-512) y R5.6 («el calendario de cierres renovado hacia atrás hasta
enero de 2025 (NA:N, condición 1)», `HOJA-DE-RUTA.md`:521-530), con la lectura que da ADR-0092 §5.
D7 deja esa lectura escrita en el runbook (§2).

### 0.1 La fila de HOLDOUT del día

Escrita y estadiada ANTES del primer `make check` (fila del 2026-11-26 de
`docs/validation/HOLDOUT-EXPOSICIONES.md` que nombra la rama): esta rama lee documentos del repo y
las Trading Updates públicas de FTMO; ningún material del trader ni de días reservados, ninguna vela
ni tick de 2025.

### 0.2 Lo leído, con fichero:línea

- **El runbook** (`docs/runbooks/RENOVAR-CIERRES.md`, 64 líneas). Se renueva por condición, no a
  fecha fija (:9-27): (1) una simulación pide días posteriores a `hasta`, y entonces se renueva
  «hacia atrás, hasta cubrir esos días» (:14-18); (2) antes de correr en tiempo real (:19-27). En
  rama propia `trabajo/renovar-cierres-<AAAA-MM-DD>` (:32-37). El dato sale de las Trading Updates
  (:41-43), cada cierre extraordinario del Forex con su `fuente` -URL y fecha de consulta- (:44-45),
  `cubre.hasta` hasta el día antes del jueves siguiente a la última leída (:46-47), lo que no tiene
  fuente no entra (:48-49), y FTMO limita el ritmo, HTTP 429 (:50). Se comprueba con
  `knowledge validate`, los dos tests y el arnés (:54-55), y se regenera la capa en el MISMO commit
  (:57-64).
- **`docs/validation/CIERRES-DE-MERCADO.md` §0.2 y §0.3.** Nombre `trading-update-<día>-<mes>-<año>`,
  con excepciones (`11-december-2025`, :113); la del 25-12-2025 no existe (:109); las 43 leídas del
  4-12-2025 al 1-10-2026 el 2026-10-03 entre las 00:35 y las 01:00 UTC (:104-118), en tres tandas
  por el HTTP 429 (:111-117); solo las de Navidad nombraban el Forex (:118-121). Cada
  `extraordinarios` lleva fecha, inicio, fin, huso y fuente: «la URL de la Trading Update y el día de
  lectura» (:142-143). Fuera de `cubre`, se niega con `cierre_sin_calendario` (:158-162).
- **El YAML del perfil** (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`). Cabecera :1-15
  (huso `America/New_York` por la Trading Update del 5-mar-2026 y A-28, ADR-0090); `cubre` :18-23
  (`desde` 2025-12-04, `hasta` 2026-10-07, el comentario con las horas de lectura :19-20); `semanal`
  :24-30 y `diario` :31-36, de la API de símbolos leída en 2026; tres `extraordinarios` :37-54
  (Navidad 2025, Año Nuevo 2026 y la parada del 2026-03-08, esta con husos `Etc/GMT-2` y
  `Etc/GMT-3`).
- **ADR-0068** (`docs/adr/0068-la-ventana-antes-de-un-cierre-de-mercado-vive-en-el-puerto-del-broker.md`).
  Cierre largo: el de `minimo` o más (dos horas, R15); la ventana, desde `margen` (dos horas) antes
  hasta que acaba (:25-31); fuera de `cubre`, `cierre_sin_calendario` (:32-33); el simulador no
  corre fuera del calendario (§7, :101-104). La premisa: «ningún cierre largo de EURUSD en FTMO
  empieza antes de las 17:00 de Madrid entre el 4-12-2025 y el 7-10-2026» (:127-129). Alternativas
  descartadas (:113-123): una condición en la spec, solo las sesiones de MT5, solo el calendario,
  la ventana en el reloj del servidor, seguir abriendo fuera del calendario. Huso confirmado por
  ADR-0090 (recuadro :16-20).
- **R15** (`docs/validation/FTMO-REGLAS.md`:62): «two hours or less before a relevant financial
  market is closed for at least two hours».
- **El cargador** (`src/botsito/engine/calendario_cierres.py`): `hasta < desde` da
  `CalendarioError("cubre: hasta va antes que desde")` (:96-97); `cubre` va de las 00:00 de `desde`
  a las 00:00 del día siguiente a `hasta`, en su huso (:98-99); se expande una semana más a cada
  lado (:100-101); un extraordinario sin `fuente` no entra (:164-165); su etiqueta es
  `extraordinario <fecha de inicio>` (:179). Los cierres que se tocan se juntan, con las fuentes
  unidas por « + » (`domain/cierres.py`:135-146).
- **Los tests que leen el calendario**, y cuál fija una fecha de `cubre` como literal:
  - `tests/unit/test_cierres_de_mercado.py`: lee el YAML real en `FTMO` (:63). :356-364 exige
    Navidad y Año Nuevo de 2025 (:359), que `cubre` vaya de antes del 1-4-2026 a después del 1-9-2026
    (:360, lee el YAML y compara con fechas literales), y que ningún cierre largo empiece antes de
    las 17:00 de Madrid en laborable (:361-364). :388-399 en `main` (:410-421 en la rama, con el test nuevo delante), el caso parametrizado: cambia
    `hasta: "2026-10-07"` por `"2025-01-01"` y espera el error de `hasta` (:393). **Es el único que
    fija un literal de `cubre` que esta renovación toca** (D5 a). :347-353 lee `cubre_desde_ms` del
    YAML (no fija fecha).
  - `tests/unit/test_renovar_cierres.py`: lee el YAML (:113-118) y recorta `hasta` a un literal
    propio, 2026-04-01 (:150-161); no fija `desde`.
  - `tests/unit/test_capa_generada.py`: cambia `hasta: "2026-10-07"` por `"2026-10-06"` en una copia
    (:110-113); no fija `desde`. El fichero del repo tiene que ser lo que da el generador.
  - `tests/unit/test_f17_historial_criterio.py`:100-108: los meses de construcción dentro de `cubre`,
    leído del YAML.
  - `git grep -n cubre_desde -- tests src scripts` da además `scripts/leer_historial_f17.py`:682,
    `src/botsito/domain/cierres.py`:52/56/96, `src/botsito/engine/cableado.py`:778/1265,
    `src/botsito/mql5bridge/generar_capa.py`:304: todos leen el YAML, ninguno fija fecha.
- **`knowledge validate` no lee el calendario**: `git grep` de `calendario_cierres`,
  `cargar_calendario` y `ruta_calendario` en `src/` solo da `engine/cableado.py`:68-71/765 y
  `mql5bridge/generar_capa.py`:52/302/344; nada de `knowledge/`. Lo comprueban el cargador, los
  tests y el generador de la capa.

### 0.3 El reloj del servidor en 2025

Medido en las Trading Updates de 2025 (§1), las mismas transiciones que la cabecera del YAML apoya
en 2026:
- 20-feb, 27-feb y 6-mar-2025: «On Sunday, 9 Mar 2025, the USA will transition to Daylight Saving
  Time (DST)»; desde ese día, el desfase entre Praga y MetaTrader (GMT+3) son 2 horas, y la del
  6-mar anuncia que las plataformas no operan «between 07:00 GMT+2 and 11:00 (GMT+3)». Hasta el
  9-mar las horas van en «GMT+2», desde ahí en «GMT+3» (cabeceras de cada una).
- 13-mar, 20-mar y 27-mar-2025: Europa cambia el 30-mar y «trading will not be interrupted»; el
  desfase con Praga vuelve a 1 hora.
- 23-oct y 30-oct-2025: «Starting Sunday, 2 Nov 2025, the United States will end Daylight Saving
  Time. The corresponding change in platform occurs at 09:00, when clocks are moved back one hour to
  08:00» (la del 23-oct decía 10:00 y 09:00; la del 30-oct lo corrige). Desde el 3-nov, «GMT+2».
- 6-nov-2025 en adelante: «GMT+2».

El servidor cambia de hora con EE. UU. en 2025: 02:00 de Nueva York son las 09:00 del servidor
(GMT+3) el 2-nov, y `America/New_York` sigue valiendo. **No hay PARADA (c).**

### 0.4 La lista de Trading Updates, medida

El archivo `https://ftmo.com/en/blog/trading-updates/` **no se pudo leer**: `curl` (200, 8 bytes:
el texto `ftmo.com`, una página en la caché de Cloudflare, `CF-Cache-Status: HIT`), el subagente
`web-fetch` (lo mismo) y con `?lectura=1` y `/page/2/` (lo mismo). El navegador lo negó el permiso
de la sesión, y la API REST de WordPress (`/wp-json/wp/v2/posts`) la negó el clasificador: no se
insistió por ninguna de las dos.

La lista sale del **sitemap oficial de FTMO** (`https://ftmo.com/sitemap_index.xml`, Yoast), que
publica `trading-updates-sitemap.xml` y `trading-updates-sitemap2.xml` (1566 URL, 218 en `/en/`).
En el orden del sitemap, del 28-nov-2024 al 11-dic-2025, salen 56 entradas `/en/`, todas con el
patrón `trading-update-<día>-<mes>-<año>` salvo `11-december-2025`; una es de agosto de 2024
(`trading-update-15-aug-2024`, con `lastmod` del 2024-12-18: se descargó y es el festivo británico
de 2024), y ninguna `/en/` con `lastmod` en el tramo queda fuera de ellas. Jueves sin entrada: **26-dic-2024** y **1-may-2025** (los dos, HTTP 404 con el
patrón). La semana del 1-may la cubre la del martes **29-abr-2025** (y la del 8-may); la del 26-dic,
las tablas de Navidad de las del 19-dic-2024 y 2-ene-2025... que no se pueden leer (abajo). Hay
además una del lunes 23-jun-2025 (tensiones geopolíticas, nada de horarios).

**Las tablas de Navidad de 2024 no están en ninguna de las fuentes de FTMO que se buscaron.** Las
del 19-dic-2024 y del 2-ene-2025 dicen «Kindly refer to the schedule below for specific details:» y
detrás no hay nada, ni tabla ni imagen. Se buscó en:
- la del 19-dic-2024 en inglés, checo, alemán, español y portugués;
- la del 2-ene-2025 en inglés y checo (la checa remite igual a «níže uvedené tabulce» y detrás no hay
  nada); la francesa del 2-ene da 301 y, seguida (tras el revisor, a2), lleva a la portada de
  FTMO en francés;
- tras el revisor (a2), los otros sitemaps del índice (`post-sitemap.xml`, `post-sitemap2.xml`,
  `post-sitemap3.xml`, `page-sitemap.xml`, `faq-sitemap.xml` y `press-release-sitemap.xml`,
  consultados el 2026-11-27 hacia las 04:20 UTC): ninguna entrada `/en/` con `lastmod` del 5-dic-2024
  al 10-ene-2025 salvo un artículo sobre el verano («holiday mode in the markets»: se descargó y no trae
  horarios), y ninguna otra con «christmas», «holiday» o «new-year» que, por su título, trate
  horarios de 2024;
- el Wayback Machine: el CDX de la URL del 19-dic-2024 da tres capturas, todas de 2026 (17-ene,
  16-mar y 18-jul; ninguna de 2024 ni de 2025). Se abrió la primera: trae un `instruments-table`
  vacío, sin filas. Las otras dos son posteriores.

Es decir: **en lo buscado, FTMO ya no publica si el Forex cerró el 25-dic-2024 o el 1-ene-2025, ni
con qué horario el 24 y el 31**. Es la PARADA (a): §3.

### 0.5 La aritmética de `cubre.desde`

`desde` es el primer jueves revisado (comentario de `cubre`, YAML:19, y runbook :46-47 por
simetría). Con la tabla de Navidad de 2024 sin fuente, las semanas del 19-dic-2024 (que incluye el
25-dic), del 26-dic (sin Trading Update) y del 2-ene-2025 (cuya tabla repite la de Navidad y puede
llevar el 2-ene, como la de 2025 llevaba el «2nd January») no se pueden certificar. El primer jueves
con su Trading Update entera y sin remisiones vacías es el **9-ene-2025**: `desde: "2025-01-09"`.

**No llega al 2025-01-01 que pide el encargo (§1): le faltan los días del 1 al 8 de enero.** Cubre
diciembre de 2025 entero (R5.4, letra I; hoy empieza el 2025-12-04), junio a noviembre de 2025 (la
medida de R5.6) y de febrero a mayo de 2025. **No cubre enero de 2025 entero, y la extensión de
ADR-0092 §5 sí puede llegar a él**: «se añaden con la misma spec mayo, abril, marzo, febrero y enero
de 2025, en ese orden y de uno en uno, hasta N ≥ 100» (`docs/adr/0092-…`:131-134); por eso el paso
previo dice «hasta enero de 2025» (:145-146). Enero solo hace falta si, con mayo a febrero, N sigue
por debajo de 100 (revisor, a1).

## 1. Las Trading Updates leídas

Descargadas con `curl` de una en una (una llamada por página y 4 s de pausa entre ellas: la guardia
niega un bucle de `curl` con espera), sin ningún HTTP 429. La hora de consulta es la cabecera `Date`
de la respuesta, en UTC; el sha256 es el de los bytes descargados, que no se versionan (son de
FTMO). El índice completo (URL, código, `Date`, bytes, sha256 entero y título) está en
`docs/validation/anexos/RENOVAR-CIERRES-2025/indice.tsv`.

Lo que se buscó en cada una, en el cuerpo del artículo (del `<h1>` al primer artículo
relacionado): `Forex`, `EUR/USD`, `EURUSD`, `FX`, `currenc`, `Exotic`, `all symbols`,
`all instruments` (las de `CIERRES-DE-MERCADO.md` §0.2), y además `all platforms`, `DST`,
`Daylight`, `GMT`, `interrupt` y «trading … unavailable/disabled», y las tablas fila a fila.

| # | Trading Update | HTTP | Consulta (UTC, cabecera `Date`) | sha256 (16) | Qué anuncia para el Forex |
|---|---|---|---|---|---|
| 1 | [5-dec-2024](https://ftmo.com/en/blog/trading-updates/trading-update-5-dec-2024/) | 200 | 2026-11-27 02:34:14 | `b5e4d75df9c936c3` | fuera del tramo (anterior al primer jueves); nada del Forex |
| 2 | [12-dec-2024](https://ftmo.com/en/blog/trading-updates/trading-update-12-dec-2024/) | 200 | 2026-11-27 02:28:10 | `9805105f8df8a347` | horarios nuevos de EU50, FRA40, SPN35, AUS200 y HK50; alta de HEATOIL.c. Nada del Forex |
| 3 | [19-dec-2024](https://ftmo.com/en/blog/trading-updates/trading-update-19-dec-2024/) | 200 | 2026-11-27 02:28:18 | `43a1117a7dcb3ac9` | «Christmas and New Year's Eve»: remite a «the schedule below» y **no hay tabla** (PARADA a) |
| 4 | [26-dec-2024](https://ftmo.com/en/blog/trading-updates/trading-update-26-dec-2024/) | 404 | 2026-11-27 02:34:32 | `995e1be9b63ce9b5` | **no existe** (404; no está en el sitemap) |
| 5 | [2-jan-2025](https://ftmo.com/en/blog/trading-updates/trading-update-2-jan-2025/) | 200 | 2026-11-27 02:28:23 | `8479cecb38c4feaf` | la misma remisión a la tabla de Navidad, **sin tabla** (PARADA a) |
| 6 | [9-jan-2025](https://ftmo.com/en/blog/trading-updates/trading-update-9-jan-2025/) | 200 | 2026-11-27 02:28:50 | `2519a56d3f407726` | cierres anticipados de índices y materias primas («National Day of Mourning» del 9-ene y Martin Luther King del 20-ene); mantenimiento del sábado 11-ene; alta de XCUUSD. Nada del Forex |
| 7 | [16-jan-2025](https://ftmo.com/en/blog/trading-updates/trading-update-16-jan-2025/) | 200 | 2026-11-27 02:28:55 | `d32026a545a7cafa` | cierres anticipados de índices (Martin Luther King); alta de HEATOIL.c y DXY.cash. Nada del Forex |
| 8 | [23-jan-2025](https://ftmo.com/en/blog/trading-updates/trading-update-23-jan-2025/) | 200 | 2026-11-27 02:29:02 | `49c1c317e184f06e` | HK50 (Año Nuevo lunar), AUS200 (Australia Day), FB por META en cTrader. Nada del Forex |
| 9 | [30-jan-2025](https://ftmo.com/en/blog/trading-updates/trading-update-30-jan-2025/) | 200 | 2026-11-27 02:29:08 | `4216f3306be16a7d` | HK50 cerrado del 29 al 31-ene. Nada del Forex |
| 10 | [6-feb-2025](https://ftmo.com/en/blog/trading-updates/trading-update-6-feb-2025/) | 200 | 2026-11-27 02:29:15 | `02b104cc9210454f` | mantenimiento de cTrader el sábado 8-feb. Nada del Forex |
| 11 | [13-feb-2025](https://ftmo.com/en/blog/trading-updates/trading-update-13-feb-2025/) | 200 | 2026-11-27 02:29:20 | `492e6f0e8b37bf29` | cierres anticipados de índices (Presidents' Day); DXY, COTTON.c, SUGAR.c. Nada del Forex |
| 12 | [20-feb-2025](https://ftmo.com/en/blog/trading-updates/trading-update-20-feb-2025/) | 200 | 2026-11-27 02:29:25 | `adcddb49acb70112` | anuncia el cambio de hora de EE. UU. del 9-mar (servidor a GMT+3, 2 h con Praga). Nada del Forex |
| 13 | [27-feb-2025](https://ftmo.com/en/blog/trading-updates/trading-update-27-feb-2025/) | 200 | 2026-11-27 02:29:30 | `01fe1879b6f80dab` | lo mismo que la del 20-feb. Nada del Forex |
| 14 | [6-mar-2025](https://ftmo.com/en/blog/trading-updates/trading-update-6-mar-2025/) | 200 | 2026-11-27 02:29:50 | `389999e18cc1ee22` | **parada de todas las plataformas el domingo 9-mar-2025, de 07:00 GMT+2 a 11:00 GMT+3** (entra) |
| 15 | [13-mar-2025](https://ftmo.com/en/blog/trading-updates/trading-update-13-mar-2025/) | 200 | 2026-11-27 02:29:55 | `78d75485ffc892b1` | Europa cambia el 30-mar: «trading will not be interrupted». Nada del Forex |
| 16 | [20-mar-2025](https://ftmo.com/en/blog/trading-updates/trading-update-20-mar-2025/) | 200 | 2026-11-27 02:30:00 | `05e0c437a7ee0ddc` | lo mismo que la del 13-mar. Nada del Forex |
| 17 | [27-mar-2025](https://ftmo.com/en/blog/trading-updates/trading-update-27-mar-2025/) | 200 | 2026-11-27 02:30:04 | `f7d45f82ed73525b` | Europa sin interrupción; alta de USDSGD y USDCNH; HK50, GER40, UK100; DST de Australia. Nada del Forex (EURUSD) |
| 18 | [3-apr-2025](https://ftmo.com/en/blog/trading-updates/trading-update-3-apr-2025/) | 200 | 2026-11-27 02:30:09 | `6d8a922d88f0cbf2` | mantenimiento del sábado 5-abr; HK50 (Ching Ming); USDSGD y USDCNH en todas. Nada del Forex (EURUSD) |
| 19 | [10-apr-2025](https://ftmo.com/en/blog/trading-updates/trading-update-10-apr-2025/) | 200 | 2026-11-27 02:30:13 | `565d29cb58aa3349` | mantenimiento de un servidor MT5 el sábado 12-abr; Semana Santa (índices). Nada del Forex |
| 20 | [17-apr-2025](https://ftmo.com/en/blog/trading-updates/trading-update-17-apr-2025/) | 200 | 2026-11-27 02:30:18 | `9e978c82cec912de` | Semana Santa: cierran índices, metales, acciones, NATGAS, HEATOIL, DXY el 18-abr; **el Forex no**. Mantenimiento de cTrader el sábado |
| 21 | [24-apr-2025](https://ftmo.com/en/blog/trading-updates/trading-update-24-apr-2025/) | 200 | 2026-11-27 02:30:23 | `a09aeab0e4476397` | mantenimiento de todas las plataformas el sábado 26-abr, 01:00-02:00. Nada del Forex |
| 22 | [29-apr-2025](https://ftmo.com/en/blog/trading-updates/trading-update-29-apr-2025/) | 200 | 2026-11-27 02:30:28 | `42457a90318ad0ae` | (martes; cubre la semana del 1-may) mantenimiento de todas el sábado 3-may, 08:00-18:00. Nada del Forex |
| 23 | [1-may-2025](https://ftmo.com/en/blog/trading-updates/trading-update-1-may-2025/) | 404 | 2026-11-27 02:34:38 | `e984dc88cd6d6cf9` | **no existe** (404; no está en el sitemap); la semana la cubren la del 29-abr y la del 8-may |
| 24 | [8-may-2025](https://ftmo.com/en/blog/trading-updates/trading-update-8-may-2025/) | 200 | 2026-11-27 02:30:58 | `041909823478b121` | mantenimiento de todas el sábado 10-may, 12:00-13:00. Nada del Forex |
| 25 | [15-may-2025](https://ftmo.com/en/blog/trading-updates/trading-update-15-may-2025/) | 200 | 2026-11-27 02:31:03 | `4d237bbaef38963f` | mantenimiento de todas el sábado 17-may, 04:00-05:00. Nada del Forex |
| 26 | [22-may-2025](https://ftmo.com/en/blog/trading-updates/trading-update-22-may-2025/) | 200 | 2026-11-27 02:31:08 | `0c5bdcd3789d0cfb` | mantenimiento de todas el sábado 24-may, 04:00-05:00. Nada del Forex |
| 27 | [29-may-2025](https://ftmo.com/en/blog/trading-updates/trading-update-29-may-2025/) | 200 | 2026-11-27 02:31:14 | `f7f78d1f6572ab61` | mantenimiento de todas el sábado 31-may, 08:00-13:00. Nada del Forex |
| 28 | [5-jun-2025](https://ftmo.com/en/blog/trading-updates/trading-update-5-jun-2025/) | 200 | 2026-11-27 02:31:21 | `0a146ad196528b6e` | mantenimiento de todas el sábado 7-jun, 01:00-03:00. Nada del Forex |
| 29 | [12-jun-2025](https://ftmo.com/en/blog/trading-updates/trading-update-12-jun-2025/) | 200 | 2026-11-27 02:31:25 | `dfe8f7ba036bf9af` | mantenimiento de todas el sábado 14-jun y el domingo 15-jun (12:00-14:00). Nada del Forex |
| 30 | [19-jun-2025](https://ftmo.com/en/blog/trading-updates/trading-update-19-jun-2025/) | 200 | 2026-11-27 02:31:31 | `e177db773d8e109c` | mantenimiento de todas el domingo 22-jun, 09:00-13:00. Nada del Forex |
| 31 | [23-jun-2025](https://ftmo.com/en/blog/trading-updates/trading-update-23-jun-2025/) | 200 | 2026-11-27 02:31:36 | `ff218b1ca6a7f990` | (lunes) aviso de volatilidad por tensiones geopolíticas; ningún horario |
| 32 | [26-jun-2025](https://ftmo.com/en/blog/trading-updates/trading-update-26-jun-2025/) | 200 | 2026-11-27 02:31:41 | `aa96cbb0273e3865` | mantenimiento de todas el sábado 28-jun, 13:00-18:00. Nada del Forex |
| 33 | [3-jul-2025](https://ftmo.com/en/blog/trading-updates/trading-update-3-jul-2025/) | 200 | 2026-11-27 02:31:46 | `d932cfaed3331d30` | mantenimiento de todas el sábado 5-jul, 08:00-13:00; Independence Day (cierres anticipados de índices, el 3-jul y otros días); JP225. Nada del Forex |
| 34 | [10-jul-2025](https://ftmo.com/en/blog/trading-updates/trading-update-10-jul-2025/) | 200 | 2026-11-27 02:31:51 | `fb29ff7964853284` | sin mantenimiento. Nada del Forex |
| 35 | [17-jul-2025](https://ftmo.com/en/blog/trading-updates/trading-update-17-jul-2025/) | 200 | 2026-11-27 02:31:56 | `be6d3bd138dc9d77` | servidores de prueba y dos MT4 el sábado 19-jul; cambio de las cripto. Nada del Forex |
| 36 | [24-jul-2025](https://ftmo.com/en/blog/trading-updates/trading-update-24-jul-2025/) | 200 | 2026-11-27 02:32:01 | `372b5d12da632cba` | todas las plataformas sin servicio el sábado 26 y el domingo 27-jul (00:00-23:59, por las cripto). Nada del Forex |
| 37 | [31-jul-2025](https://ftmo.com/en/blog/trading-updates/trading-update-31-jul-2025/) | 200 | 2026-11-27 02:32:07 | `f116b6621bc091a1` | mantenimiento de todas el sábado 2-ago y el domingo 3-ago (11:00-13:30). Nada del Forex |
| 38 | [7-aug-2025](https://ftmo.com/en/blog/trading-updates/trading-update-7-aug-2025/) | 200 | 2026-11-27 02:32:15 | `3369c61de30425ba` | sin mantenimiento. Nada del Forex |
| 39 | [14-aug-2025](https://ftmo.com/en/blog/trading-updates/trading-update-14-aug-2025/) | 200 | 2026-11-27 02:32:22 | `15d041c80d5c0b7b` | mantenimiento el sábado 16-ago (un servidor MT5 y, de 18:00 a 23:59, todas). Nada del Forex |
| 40 | [21-aug-2025](https://ftmo.com/en/blog/trading-updates/trading-update-21-aug-2025/) | 200 | 2026-11-27 02:32:28 | `4e32d0ff234baf4a` | mantenimiento de todas el sábado 23-ago, 17:00-23:59. Nada del Forex |
| 41 | [28-aug-2025](https://ftmo.com/en/blog/trading-updates/trading-update-28-aug-2025/) | 200 | 2026-11-27 02:32:35 | `1eef372bd4a4a1dd` | mantenimiento de todas el sábado 30-ago, el día entero; Labor Day (cierres anticipados de índices, metales y energía el 1-sep). Nada del Forex |
| 42 | [4-sep-2025](https://ftmo.com/en/blog/trading-updates/trading-update-4-sep-2025/) | 200 | 2026-11-27 02:33:03 | `c26ba95366466a4c` | mantenimiento de todas el sábado 6-sep, el día entero. Nada del Forex |
| 43 | [11-sep-2025](https://ftmo.com/en/blog/trading-updates/trading-update-11-sep-2025/) | 200 | 2026-11-27 02:33:08 | `aa6c76b9e4a96330` | mantenimiento de todas el sábado 13-sep (y de los servidores de prueba y DXtrade el domingo 14-sep, 12:00-23:59); Volume Bands; baja de MKRUSD; comisión del Forex de 1,50 a 2,50 por lote y lado. Ningún cierre |
| 44 | [18-sep-2025](https://ftmo.com/en/blog/trading-updates/trading-update-18-sep-2025/) | 200 | 2026-11-27 02:33:15 | `635fe69f365b29c8` | mantenimiento de MT5 el sábado 20-sep. Nada del Forex |
| 45 | [25-sep-2025](https://ftmo.com/en/blog/trading-updates/trading-update-25-sep-2025/) | 200 | 2026-11-27 02:33:19 | `f41542174858fc4c` | mantenimiento de todas el sábado 27-sep y el domingo 28-sep (17:00-23:59); comisiones. Ningún cierre |
| 46 | [2-oct-2025](https://ftmo.com/en/blog/trading-updates/trading-update-2-oct-2025/) | 200 | 2026-11-27 02:33:24 | `02c72b4b7c750bba` | mantenimiento el sábado 4-oct; DST de Australia (AUS100). Nada del Forex |
| 47 | [9-oct-2025](https://ftmo.com/en/blog/trading-updates/trading-update-9-oct-2025/) | 200 | 2026-11-27 02:33:31 | `a5130a80ff334e17` | mantenimiento de MT5 el sábado 11-oct. Nada del Forex |
| 48 | [16-oct-2025](https://ftmo.com/en/blog/trading-updates/trading-update-16-oct-2025/) | 200 | 2026-11-27 02:33:36 | `52e220e6aaa7c358` | mantenimiento de todas el sábado 18-oct; DST de Europa (acciones e índices europeos). Nada del Forex |
| 49 | [23-oct-2025](https://ftmo.com/en/blog/trading-updates/trading-update-23-oct-2025/) | 200 | 2026-11-27 02:33:41 | `7fef6b2bcd483d84` | mantenimiento el sábado 25-oct; Europa cambia el 26-oct; anuncia el cambio de EE. UU. del 2-nov (10:00 a 09:00 del servidor); HK50 el 29-oct. Nada del Forex |
| 50 | [30-oct-2025](https://ftmo.com/en/blog/trading-updates/trading-update-30-oct-2025/) | 200 | 2026-11-27 02:33:46 | `5378923db1e618a8` | **mantenimiento de todas las plataformas el domingo 2-nov-2025, de 07:00 a 11:00, el día del cambio de hora de EE. UU. (09:00 a 08:00 del servidor)** (entra) |
| 51 | [6-nov-2025](https://ftmo.com/en/blog/trading-updates/trading-update-6-nov-2025/) | 200 | 2026-11-27 02:33:53 | `87369b935e467924` | mantenimiento el sábado 8-nov; desde aquí, GMT+2. Nada del Forex |
| 52 | [13-nov-2025](https://ftmo.com/en/blog/trading-updates/trading-update-13-nov-2025/) | 200 | 2026-11-27 02:33:57 | `b69a0bd0981e4195` | sin mantenimiento; split de NFLX. Nada del Forex |
| 53 | [20-nov-2025](https://ftmo.com/en/blog/trading-updates/trading-update-20-nov-2025/) | 200 | 2026-11-27 02:34:02 | `4259b13e8a35f4c1` | mantenimiento de todas el sábado 22-nov, 13:00-18:00. Nada del Forex |
| 54 | [27-nov-2025](https://ftmo.com/en/blog/trading-updates/trading-update-27-nov-2025/) | 200 | 2026-11-27 02:34:09 | `44e2926b3d0d037b` | sin mantenimiento; Thanksgiving (cierres anticipados de índices, metales y energía). Nada del Forex (última del tramo: el jueves anterior al 4-dic) |
| 55 | [4-dec-2025](https://ftmo.com/en/blog/trading-updates/trading-update-4-dec-2025/) | 200 | 2026-11-27 02:34:25 | `c003a907b46fb4cb` | ya leída en `trabajo/renovar-cierres` (2026-10-03); releída como control |
| 56 | [15-aug-2024](https://ftmo.com/en/blog/trading-updates/trading-update-15-aug-2024/) | 200 | 2026-11-27 02:34:20 | `4c0e2fa4991a0776` | agosto de 2024, fuera del tramo; está en el sitemap entre las de diciembre de 2024 por su `lastmod` (2024-12-18) |

## 2. Los cierres que entran, y los que no

### Entran (2)

| Cierre | Desde | Hasta | ¿Largo? | Fuente | Efecto |
|---|---|---|---|---|---|
| Parada por el cambio de hora de EE. UU. | dom 09-03-2025 07:00 GMT+2 (05:00 UTC) | 11:00 GMT+3 (08:00 UTC) | sí (3 h) | Trading Update del 6-mar-2025, consultada a las 02:29:50 UTC | dentro del fin de semana: se junta con él (`diario + semanal + extraordinario 2025-03-09`, del vie 07-03 21:55 UTC al dom 09-03 21:05 UTC) |
| Mantenimiento del día del cambio de hora de EE. UU. | dom 02-11-2025 07:00 GMT+3 (04:00 UTC) | 11:00 GMT+2 (09:00 UTC) | sí (5 h en instantes) | Trading Update del 30-oct-2025, consultada a las 02:33:46 UTC | dentro del fin de semana: `diario + semanal + extraordinario 2025-11-02`, del vie 31-10 20:55 UTC al dom 02-11 22:05 UTC |

Las dos, como la del 2026-03-08 (D1): husos fijos `Etc/GMT-2` y `Etc/GMT-3`, y la `fuente` con la
URL y la hora de consulta en UTC. La de noviembre la llama FTMO «Weekend Maintenance», pero es la
del día del cambio y la anuncia junto a él. La lectura de sus horas: «07:00» antes del cambio
(GMT+3) y «11:00» después (GMT+2), porque el cambio es a las 09:00; la cabecera de esa Trading Update
dice «GMT+3 (until 3 Nov 2025) and GMT+2 thereafter», y leídas las dos en GMT+3 la parada acabaría a
las 08:00 UTC en vez de las 09:00. Se toma la más larga (más restrictiva); cae dentro del fin de
semana con cualquiera de las dos y no cambia nada.

### No entran

- **Ningún cierre del Forex de 2025, porque ninguna Trading Update del tramo lo anuncia** (§1). Las
  únicas menciones del Forex son la tabla de comisiones (11-sep y 25-sep: de 1,50 a 2,50 por lote y
  lado) y el ejemplo de Volume Bands con EUR/USD (11-sep y 16-oct). Semana Santa (18 y 21-abr-2025)
  cierra índices, metales, acciones y materias primas, no el Forex (17-abr), como en 2026.
- **Los mantenimientos de fin de semana** (los de la tabla de §1, del 11-ene al 22-nov-2025:
  sábados, y domingos antes de las 00:05 del lunes del servidor; ninguno en día laborable). Caen todos dentro del cierre semanal y no
  cambiarían ningún instante; la rama anterior tampoco los metió (el de DXtrade del 20-dic-2025 no
  está en el YAML). Entra solo el del 2-nov, por ser el del cambio de hora (D1). **Es una lectura
  de D1, y el consultor la puede cambiar** (desviación 3).
- **Lo que no es EURUSD** (D2): índices, materias primas, metales, acciones, cripto, DXY, USDSGD y
  USDCNH.
- **La Navidad y el Año Nuevo de 2024-25**: sin fuente legible (§0.4). PARADA (a), §3.

### El horario `semanal` y `diario`

Sale de la API de símbolos leída el 2026-10-03 (YAML:24-36), no de una fuente de 2025 (D2). Ninguna
Trading Update de 2025 anuncia otro horario del Forex: **no hay PARADA (b)**. Con el servidor en el
reloj de Nueva York (§0.3), la pauta de 2026 se aplica igual a 2025.

### La premisa de ADR-0068

Medido con el cargador sobre el YAML renovado (ensayo en la carpeta de trabajo, antes de escribirlo
en el repo): 463 cierres juntos, 95 de dos horas o más, **ninguno empieza antes de las 17:00 de
Madrid en día laborable**. No hay PARADA (e).

## 3. PARADA (a): la Navidad de 2024, sin fuente

**Qué falta.** La tabla «Christmas and New Year's Eve» de las Trading Updates del 19-dic-2024 y del
2-ene-2025 (la del 26-dic-2024 no existe). FTMO la publicaba como un componente
(`instruments-table`) que hoy sale vacío; en la captura del Wayback Machine del 17-ene-2026 ya salía
vacío, y no hay capturas anteriores. Ninguna de las otras fuentes de FTMO que se buscaron la trae
(§0.4: otros idiomas, los demás sitemaps); no se buscó fuera de `ftmo.com` y del Wayback.

**Qué se ha hecho, por §4 (a).** `cubre.desde` no pasa del hueco: queda en el **2025-01-09**, el
primer jueves después de él con su Trading Update entera. Todo lo demás está hecho (§4).

**Qué no cubre.** Del 1 al 8 de enero de 2025, que el encargo pide (§1: «como mínimo el
2025-01-01»). R5.4 (diciembre de 2025) y la medida de R5.6 (junio a noviembre de 2025) quedan
dentro; **el último mes de la extensión de R5.6, enero de 2025, no entero** (§0.5, revisor a1).

**Las opciones, para el consultor:**

1. **Dejarlo en el 2025-01-09**: cumplido el paso previo de R5.4 y el de la medida de R5.6; el de su
   extensión, salvo del 1 al 8 de enero. Si la extensión llega a enero (N < 100 tras febrero), la
   rama de R5.6 se encontraría el hueco: el simulador se niega por fecha (ADR-0068 §7), y enero no
   se podría añadir entero sin decidir antes qué hacer con esos ocho días.
2. **Pedírsela a FTMO** (soporte, en inglés): el horario del Forex del 24-12-2024 al 2-01-2025 en
   los servidores MT5. Con la respuesta, una rama nueva lleva `desde` al 2024-12-12 (el primer
   jueves con Trading Update entera antes del hueco) y `test_cierres_de_mercado.py` aprieta su
   límite al 2025-01-01.
3. **Medirlo**: las velas M1 o los ticks de FTMO de esos días, si algún día se tienen (hoy no: no se
   descargan en esta rama, §2 del encargo).

No se mete el horario de 2025 («Forex: 25th December Closed», «1st January: Closed») como si fuera
el de 2024: no tiene fuente (D1, «lo que no tenga fuente no entra»).

### Lo que necesito que decidas

**1. La Navidad de 2024 (del 24-dic-2024 al 8-ene-2025, sin fuente legible).**
- (a) Dejar `desde` en el 2025-01-09 (opción 1). Coste: ninguno ahora; si la extensión de R5.6
  llega a enero, ese mes no entra entero y hay que volver aquí.
- (b) Preguntar a soporte de FTMO el horario del Forex en MT5 del 24-12-2024 al 2-01-2025 (opción
  2) y, con la respuesta escrita, una rama corta que lleve `desde` al 2024-12-12. Coste: un correo
  y una rama de una hora; la respuesta es una fuente escrita como las de R15 (ticket VDW-DPMWR-965).
- (c) Medirlo con velas o ticks de FTMO de esos días (opción 3). Coste: no hay datos de FTMO de
  2024, y bajarlos es de otra rama.

**Recomiendo (a) ahora, y (b) en paralelo**: la pregunta a FTMO no bloquea nada, y la rama de R5.6
solo necesita enero si con mayo a febrero N < 100, lo que se sabrá al correrla. Si se elige (a), las
líneas de §8 ya lo dicen así.

## 4. Lo hecho tras la fase 0 (la PARADA es condicional: §4 del encargo)

Con la PARADA (a) acotada a la Navidad de 2024, lo demás cuadra (no hay (b), (c), (d) ni (e)), así
que se siguió con §5 sobre el tramo que sí tiene fuente.

- **D1 y D2, el YAML** (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`). Las tres entradas
  de hoy, intactas. Dos `extraordinarios` nuevos al final, con un comentario que nombra la rama y el
  informe (§2): `2025-03-09` y `2025-11-02`, cada `fuente` con la URL y la hora de consulta en UTC.
- **D3, `cubre`.** `desde: "2025-01-09"` (no el 2024-12-12: PARADA a); `hasta` sin tocar; el
  comentario de `cubre` añade las fechas y horas de lectura del tramo nuevo y por qué la Navidad de
  2024 queda fuera; la cabecera cita `docs/validation/RENOVAR-CIERRES-2025.md`.
- **D4, la capa**, en el mismo commit que el YAML:
  `uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k`
  dio «escrito (capa_hash 6c846ba7…)», y con `--comprobar`, «al dia». `CIERRES_CUBRE_DESDE` pasa de
  1764824400 (2025-12-04T05:00:00Z) a 1736398800 (2025-01-09T05:00:00Z) y `CIERRES_N` de 228 a 463;
  `CIERRES_CUBRE_HASTA`, igual. **Compilada** con lo estadiado:
  `uv run python src/botsito/mql5bridge/compilar.py compilar --repo . --metaeditor "C:/Program Files/MetaTrader 5/MetaEditor64.exe" --salida docs/validation/anexos/RENOVAR-CIERRES-2025/compilacion mql5/Experts/Botsito.mq5 mql5/Scripts/BotsitoPruebasCapa.mq5`
  → `Botsito.mq5: PASA (0 errores, 0 avisos)` y `BotsitoPruebasCapa.mq5: PASA (0 errores, 0 avisos)`;
  los logs, en `anexos/RENOVAR-CIERRES-2025/compilacion/`. La guardia no lo negó. El script de
  pruebas no se ejecutó en el terminal: el encargo pide compilar.
- **D5, los tests** (`tests/unit/test_cierres_de_mercado.py`):
  - (a) el caso parametrizado pasa de `hasta: "2025-01-01"` a `"2024-01-01"`. Con `desde` en el
    2025-01-09 el viejo dato todavía fallaba por `hasta`, pero dejaría de hacerlo en cuanto `desde`
    llegue al 2024-12-12 (opción 2 de §3); su intención no cambia.
  - (b) `test_el_calendario_renovado_hacia_atras_cubre_2025_y_niega_por_el_cierre`: `cubre` empieza
    en o antes del 2025-01-09 (no del 2025-01-01: PARADA a) y cubre de junio a diciembre de 2025; el
    viernes 7-mar-2025 a las 15:30 de Nueva York se niega con `MOTIVO_CIERRE` y el cierre lleva
    `extraordinario 2025-03-09` en su fuente (las paradas de 2025 caen en fin de semana y se juntan
    con él: sin mirar la fuente, el test no probaría la entrada, como avisó el auditor); a las 14:54,
    nada.
  - **Contra `main`** (skill `comparar-con-main`, «Para probar un test con el codigo de main»):
    `git worktree add --detach C:/cm/main main`, el fichero de test de la rama copiado dentro, y
    `uv run pytest` del test nuevo y del parametrizado: **`1 failed, 4 passed`**, el nuevo con
    `AssertionError: assert 1764824400000 <= 1736398800000` (`cubre` de `main` empieza el
    2025-12-04). El motivo que daba `main` en ese instante, medido aparte en el mismo clon con
    `ventana_prohibida_por_cierre`: `cierre_sin_calendario`, sin cierre; en la rama,
    `cierre_mercado` con `diario + semanal + extraordinario 2025-03-09`. Clon quitado con
    `git worktree remove --force` (quedaban el test copiado y su `.venv`) y `git worktree prune`;
    `git status`, `git branch --list` y los 177 tags, iguales que antes.
  - (c) `PROJECT_STATE.md`, «Tests Currently Passing»: 2233 → 2234 funciones de test.
- **Los tests de 0.2**, en la rama: `uv run pytest tests/unit/test_cierres_de_mercado.py
  tests/unit/test_renovar_cierres.py tests/unit/test_capa_generada.py
  tests/unit/test_f17_historial_criterio.py` → **52 passed**; `ruff check` y `ruff format --check`
  del test, limpios.
- **D8, lo que cambia sin aviso.** La cabecera que el arnés escribe del calendario
  (`src/botsito/engine/cableado.py`:1264-1270) en la línea base vigente
  (`docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`:3123) dice 228 cierres; con
  el calendario renovado, la próxima corrida dirá **463 cierres** y empezará el 2025-01-09 a las
  05:00 UTC (medido con el cargador). Ningún golden lleva esa línea con un calendario: los cinco que
  tienen la sección dicen «sin calendario» (`tests/golden/cuenta_por_mes/main-dentro-de-un-mes.txt`:56,
  `main-diaria-dos-meses.txt`:56 y `tests/golden/informe_simulacion/main-{hueco,stop,viva}.txt`:51;
  auditor, fila 49). Los días medidos (2026) no cambian: los 218 cierres que tocan el `cubre` de `main` son idénticos en
  los dos calendarios (cargador sobre `git show main:` del YAML y sobre el de la rama; los 10 que
  faltan hasta 228 son de la semana de más que se expande a cada lado).

## 5. El auditor del encargo (0.6)

`auditor-encargo`, contra el encargo y el repo, solo leyendo: **52 afirmaciones, 36 correctas, 0
incorrectas, 16 con matiz**, y 9 cosas que el repo pide y el encargo no dice. Lo que cambió el
trabajo, y qué se hizo:

1. **El test de D5(b) podía no probar la entrada**: las paradas de 2025 caen en domingo y se juntan
   con el fin de semana. → El test mira `p.cierre.fuente` (§4).
2. **El runbook comprueba también con el arnés** (`RENOVAR-CIERRES.md`:54-55) y el encargo lo
   prohíbe sobre 2025 (§2). → Desviación 1.
3. **«Hacia atrás» quiere decir dos cosas**: en el runbook (:17), leer Trading Updates ya publicadas
   para días POSTERIORES a `hasta`; en ADR-0092 §5, cubrir días ANTERIORES a `desde`. → El párrafo
   de D7 los distingue.
4. La premisa de ADR-0068 está escrita con fechas (4-12-2025 a 7-10-2026, :127-129) y el ADR no se
   toca: **este informe es el único sitio donde la premisa se mide sobre 2025** (§2, «La premisa»).
5. La PARADA (e) dice que un cierre así «cambia días medidos»: ningún día de 2025 está medido
   todavía (`knowledge/cases/criterio_fidelidad.yaml`:47-48); cambiaría la medida futura de R5.6.
6. **El margen de `PROJECT_STATE.md`**: 846 bytes contra `main` (24.154 frente a 25.000), pero en
   la rama, con la apertura, quedan menos (§7).
7. R5.6 atribuye la renovación a NA:N y ADR-0092 §5 a «como la lee NA:I»: las líneas del cierre
   (§7) cuadran las dos.
8. La renovación no está en la entrada F de la Next Action (los huecos son C y R6a): el encargo la
   adelanta con su porqué (§1), y se dice aquí.

Los demás matices son de líneas (el parametrizado va de :388 a :399; la cabecera de `cableado.py`,
de :1264 a :1270) y de dónde se define `desde` (en `CIERRES-DE-MERCADO.md`:121, no en el runbook).

## 6. Desviaciones

1. **El arnés no se corre sobre 2025**, aunque el runbook lo pide como comprobación
   (`RENOVAR-CIERRES.md`:54-55): lo prohíbe el encargo (§2: «no se corre el arnés sobre 2025»), y las
   velas de 2025 no se descargan en esta rama. Lo hará la rama de R5.6.
2. **`cubre.desde` es el 2025-01-09, no el 2025-01-01 o antes** que pide §1: PARADA (a), §3.
3. **Los mantenimientos de fin de semana no entran** (lectura de D1, §2): solo las dos paradas del
   cambio de hora. Si el consultor quiere todos, son entradas nuevas que no cambian ningún instante.
4. **La lista de Trading Updates sale del sitemap de FTMO, no de la página del archivo**, que no se
   pudo leer (§0.4). El sitemap es de FTMO y lista las mismas entradas; el archivo pedía JavaScript o
   estaba roto en la caché, y los dos caminos que quedaban (navegador, API REST) los negaron el
   permiso y el clasificador.
5. **`knowledge validate` no lee el calendario** (0.2), aunque el runbook lo nombra entre las
   comprobaciones (:54); se corre igual, dentro de `make check`.

## 7. Comprobaciones

**`make check`, cada commit con su sello** (`make check > make-check.log 2>&1`, el log leído entero:
exit 0, ningún `failed`, `CONTRATO:`, `G2:` y `SELLO`):

| Commit | Qué | pytest | Sello | Pico |
|---|---|---|---|---|
| `dbae5f7c` | apertura (encargo, contrato, Archivo 86, fila del día) | 3815 passed, 6 xfailed (28 min 33 s) | árbol `df5f46e5…` | 323 MiB |
| `dcd680e4` | el YAML, `Generado.mqh`, los tests, este informe y sus anexos | 3816 passed, 6 xfailed (27 min 12 s) | árbol `57d6312d…` | 320 MiB |

Antes de cada uno, `uv run botsito state check` (OK), `uv run python scripts/contrato_rama.py`
(`CONTRATO:` y `G2:` en verde) y `uv run botsito knowledge validate` (sin `ERROR`, log fuera del
repo). El del commit del runbook, y el del último, en §9.

**El generador de la capa**: `--comprobar` da «al dia (capa_hash 6c846ba7…)» (§4).

**La CI de Linux** (D6): `git push origin
trabajo/renovar-cierres-2026-11-26:refs/heads/fix/renovar-cierres-2026-11-26`, run
**45935357680** sobre `dcd680e4`. Resultado, en §9.

**`PROJECT_STATE.md`**: 24.322 bytes en la rama (tope 25.000, `tests/unit/test_project_state.py`:21);
en `main`, 24.154 (los 846 de margen del encargo).

## 8. Para el cierre: las líneas propuestas

Van en el commit del cierre (la hoja de ruta y `PROJECT_STATE.md`), si el consultor las acepta y
según lo que decida sobre la PARADA (a). Escritas para la opción 1 de §3 (dejarlo en el 2025-01-09).

**`docs/plan/HOJA-DE-RUTA.md`, R5.4** (`:506-507`), en «Qué es», donde dice «antes, renovar hacia
atrás el calendario de cierres (RENOVAR-CIERRES.md, condición 1)»:

> antes, renovar hacia atrás el calendario de cierres (hecho en `trabajo/renovar-cierres-2026-11-26`:
> cubre desde el 2025-01-09, RENOVAR-CIERRES-2025.md)

R5.4 no pasa a HECHA: falta ingerir diciembre o declararlo reservado (su «Hecho cuando»).

**R5.6** (`:526-527`), en «Antes:», donde dice «el calendario de cierres renovado hacia atrás hasta
enero de 2025 (NA:N, condición 1)»:

> el calendario de cierres renovado hacia atrás hasta enero de 2025 (hecho hasta el 2025-01-09,
> `trabajo/renovar-cierres-2026-11-26`: del 1 al 8 de enero, sin fuente de FTMO, y solo los pide la
> extensión si llega a enero; NA:N, condición 1, leída como NA:I por ADR-0092 §5)

**N** (`PROJECT_STATE.md`:46): cambia una palabra, «cubre hasta el 7-10-2026» → «cubre del 9-1-2025 al
7-10-2026»; lo demás sigue siendo verdad (la condición 2, R6a.5 sin hacer).

**I** (`PROJECT_STATE.md`:36; hoy 738 bytes), más corta, porque ya no espera la renovación:

> I. Backtest de DICIEMBRE de 2025, recibido el 2026-10-09 (xlsx y capturas de Analytics, que no se
> abren nunca; SIN vídeo), SIN ABRIR y fuera del repo. El calendario de cierres ya lo cubre
> (RENOVAR-CIERRES-2025.md): entra por su propia rama cuando el consultor decida si es construcción
> o reservado, teniendo en cuenta que no trae vídeo. En v10 el trader ya comentó operaciones de
> diciembre (HOLDOUT-EXPOSICIONES, 2026-10-04); en la sesión 6 dijo que aún no lo ha grabado con su
> voz (SESION-06-EXTRACCION.md §3.5). Pesa más desde la 7a: el sesgo de enero depende de diciembre
> (Technical Debt).

Quita «julio ya entró (ADR-0078)», que ya no explica nada de I, y «(declaración de Aleks, …)», que
lleva el informe citado. Medida con Python sobre la línea: 738 bytes la de hoy, 600 la propuesta (138 menos); el cambio de N
añade 7.

**La fila de `docs/runbooks/ERRORES-RECURRENTES.md`** (la escribe el cierre), con las lecciones de la
rama:

1. **El archivo de Trading Updates de FTMO puede servirse vacío** (8 bytes, `ftmo.com`, desde la
   caché de Cloudflare): la lista se mide en el sitemap oficial (`trading-updates-sitemap*.xml`).
2. **Una Trading Update vieja puede haber perdido su tabla** (componente `instruments-table` que hoy
   sale vacío): se busca «below» seguido de nada en cada una antes de darla por leída.
3. **La guardia niega un bucle de `curl` con espera** (puede ser una consulta de la CI): varias
   llamadas `curl` LITERALES en una sola orden, con `sleep` entre ellas, sí pasan.
4. **Una parada de fin de semana se junta con el cierre semanal**: un test que quiera probar la
   entrada mira la `fuente` del cierre, no solo el motivo (auditor).

## 9. El commit del runbook, la CI, y lo que queda para el último

- **`make check` de `8b0011a4`** (el runbook y el informe al día): 3816 passed, 6 xfailed (24 min 38
  s), `CONTRATO:` y `G2:` en verde, `SELLO` sobre el árbol `ec6d26a3…`, pico de 322 MiB.
- **La CI de Linux, run 45935357680 sobre `dcd680e4`**: `failure`, con **`1 failed, 3719 passed,
  102 skipped`**; el único fallo es `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`
  («PROJECT_STATE declara la rama 'trabajo/renovar-cierres-2026-11-26'; la rama actual es
  'fix/renovar-cierres-2026-11-26'»), el aceptado en D6. Los tests del calendario pasan en Linux con
  el `zoneinfo` del sistema.
- **El último commit** (este informe con el revisor) lleva su propio `make check` y se empuja otra vez
  a `fix/renovar-cierres-2026-11-26` (revisor, a3): su run no puede ir dentro del commit que lo
  dispara, así que lo da el resumen final de la sesión.

## 10. El encargo, punto por punto

| Punto | Qué pide | Estado | Dónde |
|---|---|---|---|
| §0 | Base 93a4fc29, tag F39q, CI 45922991122 confirmada, ninguna otra rama | Hecho | «Base comprobada» |
| §0 | `abrir-rama`: encargo tal cual, contrato (R5, alto, lista blanca y protegidas), Archivo 86 | Hecho | `dbae5f7c` |
| §0 | Fila de HOLDOUT antes del primer `make check`; `state check` antes | Hecho | 0.1; §7 |
| §1 | `cubre` hacia atrás hasta ≤ 2025-01-01 | **Parcial**: hasta el 2025-01-09, PARADA (a) | §0.5, §3 |
| §1 | Decir que la lectura hacia atrás la da ADR-0092 §5 y D7 | Hecho | §0, «Por qué» |
| §2 | Nada fuera de la lista; entradas del YAML y `hasta` intactos; ni velas, ni ticks, ni arnés de 2025 | Hecho | `git diff --name-status main...HEAD`; desviación 1 |
| 0.1-0.5 | Inventario, reloj de 2025, lista medida, aritmética de `desde` | Hecho (la lista, por el sitemap: desviación 4) | §0 |
| 0.6 | El auditor | Hecho | §5 |
| §4 | Seguir salvo (a)-(e) | Hecho: solo (a), acotada | §3 |
| D1 | Extraordinarios con URL y hora UTC; paradas de marzo y noviembre | Hecho | §2; YAML |
| D2 | Nada que no sea EURUSD; horario de la API de 2026, declarado | Hecho | §2 |
| D3 | `desde` al primer jueves revisado, comentario y cabecera | Hecho | §4 |
| D4 | La capa en el mismo commit, su test, compilada con logs | Hecho | §4; anexos |
| D5 | (a) parametrizado a 2024-01-01; (b) test nuevo que rompe en `main`; (c) recuento | Hecho; (b) con el 2025-01-09 | §4 |
| D6 | Tests de 0.2, generador, `make check` sellado, CI por `fix/` con su run | Hecho; el run del último commit, en el resumen final | §7, §9 |
| D7 | Párrafo del runbook en su commit | Hecho | `8b0011a4` |
| D8 | La cabecera del arnés, los recuentos y los goldens | Hecho | §4 |
| §6 | Informe completo, líneas del cierre, revisor pegado, frase final | Hecho | §8, §11, §12 |

## 11. Lo que encontró el revisor, y qué se hizo

| # | Qué | Qué se hizo |
|---|---|---|
| a1 | La extensión de ADR-0092 §5 llega a enero de 2025 entero, y el informe decía que nadie necesitaba del 1 al 8 de enero | Corregido en §0.5, §3 (con la decisión y la recomendación) y la línea propuesta de R5.6 (§8) |
| a2 | «Ninguna otra fuente oficial» afirmaba más de lo buscado | Buscado lo que faltaba: los otros seis sitemaps, la francesa del 2-ene (lleva a la portada) y la checa del 2-ene (vacía igual); nada. El texto dice ahora lo buscado (§0.4, §3) y el comentario del YAML, «ninguna de las fuentes de FTMO buscadas» (solo comentario: `--comprobar` sigue «al dia») |
| a3 | La CI corrió sobre `dcd680e4`, no sobre el último commit | El último commit se empuja otra vez a `fix/` (§9) |
| a4 | «02:36»: la última del tramo es de las 02:34:38 | Se deja: la franja 02:28-02:36 es la de todas las descargas de esa tanda, que acaba con las versiones en otros idiomas (02:35:53); la del tramo cabe dentro |
| a5 | El CDX da tres capturas, no una | Corregido (§0.4) |
| a6 | La fila de HOLDOUT del día no nombraba lo leído después | Una fila más del 2026-11-26 con lo de después (sitemaps, Wayback, clon de `main`, compilación, revisor) |
| a7 | Líneas corridas en 0.2 | Corregidas |
| b1 | Faltaba «El encargo, punto por punto» | §10 |
| b2 | La PARADA (a) sin «Lo que necesito que decidas» | Añadido en §3, con recomendación |
| b3 | §7 remitía a un §9 que no existía | §9 |
| b4 | Filas de la tabla de §1 sin los avisos que no son del Forex | Completadas (3-jul, 28-ago, 11-sep, 13-nov, 27-nov) |

## 12. Informe del revisor

### Informe del revisor · trabajo/renovar-cierres-2026-11-26 · 2026-11-26

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 4 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El informe dice que ninguna rama necesita los días del 1 al 8 de enero de 2025, y ADR-0092 §5 dice lo contrario.** El informe: «Cubre de sobra lo que lo pide como paso previo: [...] junio a noviembre de 2025 (R5.6, ADR-0092 §5)» y «No lo necesita ninguna de las ramas que lo esperan» (`docs/validation/RENOVAR-CIERRES-2025.md`:158-160 y :289-291). La opción 1 «da por cumplido el paso previo de R5.4 y R5.6» (:295-297), y la línea que se propone para R5.6 lo marca «hecho» (:444-445). Pero la extensión de la medida de ADR-0092 llega hasta enero de 2025 ENTERO: «se añaden con la misma spec mayo, abril, marzo, febrero y enero de 2025, en ese orden y de uno en uno, hasta N ≥ 100» (`docs/adr/0092-...md`:131-134). Por eso el paso previo dice «hasta enero de 2025» (:145-146), y R5.6 incluye «y su extensión» (`docs/plan/HOJA-DE-RUTA.md`:523-524). Con `desde` en el 2025-01-09, un mes de extensión «enero» no cabe entero en `cubre`. El patrón de `tests/unit/test_f17_historial_criterio.py`:105-107 exige `cubre_desde <= día 1 del mes`. El consultor tiene que decidir la opción 1 sabiéndolo. | las citas de la celda |
| a2 | importa | **«Ninguna otra fuente oficial de FTMO la cubre» (informe :283-284) afirma más de lo que se buscó.** El YAML dice además «no se puede leer en ninguna fuente de FTMO» (`ftmo-2step-swing-100k.yaml`:24). Es justo la condición literal de la PARADA (a). Lo que se buscó: las versiones cs, de, es y pt del 19-dic-2024 y la captura del Wayback Machine. Lo que no: (1) el índice del sitemap publica `post-sitemap.xml`, `post-sitemap2.xml`, `post-sitemap3.xml`, `page-sitemap.xml`, `faq-sitemap.xml` y `press-release-sitemap.xml`, y ninguno se descargó; (2) la francesa del 2-ene da `301` hacia `https://ftmo.com/fr/?post_type=trading-updates&p=647370`, que no se siguió; (3) del 2-ene-2025 no se probó ninguna versión cs, de, es ni pt, aunque el informe (:143-145) las atribuye a «las del 19-dic-2024 y del 2-ene-2025». | `grep -o "<loc>[^<]*</loc>" sitemap.xml` (10 sitemaps); `ls` de `C:\Users\USER\.claude\jobs\630cf772\tmp\tu\`: solo `cs/de/es/pt-19-dec-2024.html`, ningún `post-sitemap*`; `h-fr-2-jan-2025.txt`: `HTTP/1.1 301`, `Location: ...p=647370` |
| a3 | importa | **La CI corrió sobre `dcd680e4`, no sobre el último commit (`8b0011a4`).** `entregar-rama` dice: «El run que cuenta es el del ULTIMO commit» (`.claude/skills/entregar-rama/SKILL.md`:85, y la verificación en :108). `8b0011a4` solo cambia documentos, pero el commit que pegue este informe también necesita su push a `fix/` y su run. | `gh run list --branch fix/renovar-cierres-2026-11-26`: un único run, 45935357680, sobre `dcd680e4`; `git log`: HEAD = `8b0011a4` |
| a4 | menor | El YAML (:23 y :61) y el mensaje de `dcd680e4` dicen que se revisaron «entre las 02:28 y las 02:36 UTC». La cabecera `Date` más tardía del tramo en `indice.tsv` es la de las 02:34:38 (1-may, 404), y la del 27-nov es de las 02:34:09. Las 02:36 no salen del índice. | `docs/validation/anexos/RENOVAR-CIERRES-2025/indice.tsv`:24 y :55 |
| a5 | menor | El informe (:146) dice «la única captura del 19-dic-2024 anterior a hoy (17-ene-2026)». El CDX descargado da tres, todas anteriores a hoy: 2026-01-17, 2026-03-16 y 2026-07-18. Solo se abrió la primera. La conclusión no cambia, porque las otras son posteriores. | `wb-cdx4.txt`: `20260117220407`, `20260316082659` y `20260718174415`; `wb-19dec.json`: closest = `20260117220407` |
| a6 | menor | La fila de HOLDOUT del día cubre solo «la apertura y la fase 0» y «las Trading Updates [...] de diciembre de 2024 a noviembre de 2025». Faltan cosas que se leyeron después: la del 15-ago-2024, la del 4-dic-2025, los sitemaps, el Wayback, el clon de `main` para D5(b), la compilación y el revisor. El precedente de `trabajo/f17-ordenes` declara cada tanda en su fila. Nada de eso es material del trader. | `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md` (una fila); las filas de f17-ordenes del mismo fichero, justo encima |
| a7 | menor | Referencias de línea corridas en 0.2. «sin `fuente` no entra (:165-166)»: el `if` está en :164 y el `raise` en :165 (`calendario_cierres.py`). El parametrizado «:388-410» mezcla la línea de `main` (:388) con la de la rama (:410). | `src/botsito/engine/calendario_cierres.py`:164-165; `tests/unit/test_cierres_de_mercado.py`:410 |

Comprobado sin hallazgos:
- **El contrato.** `contrato_rama.py` da: «CONTRATO: 13 ficheros dentro del contrato [...] (riesgo alto, artefacto docs/validation/RENOVAR-CIERRES-2025.md, tramo 'R5', 6 comprobaciones para el revisor)» y «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-26 para trabajo/renovar-cierres-2026-11-26, estadiada».
- **Las comprobaciones que no escriben:**
  - `state check`: OK.
  - `generar_capa.py --comprobar`: «al dia (capa_hash 6c846ba7…)».
  - pytest de los cuatro ficheros: 52 tests, todos en verde.
- **`make check`, los tres sellos.** Cada uno coincide con el árbol de su commit: `df5f46e5`, `57d6312d` y `ec6d26a3` (`git rev-parse <c>^{tree}`). El `make-check.log` vigente es el del tercero: «3816 passed, 6 xfailed in 1478.88s», `SELLO ... ec6d26a399c0...` y `PICO DE MEMORIA 322 MiB`, y `knowledge validate` dentro, en OK.
- **La CI.** El run 45935357680 sobre `dcd680e4cc75…` acaba «1 failed, 3719 passed, 102 skipped». El único fallo es `test_state_check_ok_on_real_repo`, con «PROJECT_STATE declara la rama 'trabajo/...'; la rama actual es 'fix/...'».
- **Trailers `Fuente:`:** no aplican; ningún commit toca `knowledge/spec` ni `knowledge/cases`.
- **El holdout y el material:** la rama no toca nada de `holdout/` ni material del trader.
- **Los regímenes de cambio:**
  - Nada en `evidence/`, `feedback/`, `manifests/`, `corpus/` ni `libros.yaml`.
  - HISTORIA y el runbook solo añaden líneas (`--numstat`: 179/0 y 7/0).
  - `PROJECT_STATE.md` tiene 24.322 bytes, por debajo de 25.000.
- **Ambigüedades, ADR, informes cerrados y las tres guardias de una `cita`:** la rama no toca ninguno.
- **Afirmación de items de evidencia nuevos:** no hay ninguno.
- **Los índices y las citas de FTMO:**
  - Los sha256 y tamaños de las 56 filas de `indice.tsv` coinciden con las descargas (0 discrepancias).
  - Las citas de las `fuente` del 6-mar y del 30-oct-2025 coinciden con el HTML.
  - Las tablas de Navidad del 19-dic-2024 y del 2-ene-2025 están vacías («Kindly refer to the schedule below», y detrás un `<hr />`), y el `instruments-table` del Wayback del 17-ene-2026 no tiene filas.
  - El 23-oct dice 10:00→09:00 y el 30-oct, 09:00→08:00.
  - Ningún 429 en las cabeceras.
  - Los domingos con mantenimiento acaban a las 23:59 del servidor como muy tarde.
- **El calendario, cargado en memoria** (el de `main` con `git show` y el de la rama):
  - 228 → 463 cierres, con 95 largos, y ninguno empieza antes de las 17:00 de Madrid en día laborable.
  - Los 218 cierres que tocan el `cubre` de `main` son idénticos en los dos.
  - El 7-mar-2025 a las 15:30 de Nueva York: en `main`, `cierre_sin_calendario`; en la rama, `cierre_mercado` con «diario + semanal + extraordinario 2025-03-09». A las 14:54, `main` da `cierre_sin_calendario` y la rama, nada.
- **Tres citas del informe:** `test_renovar_cierres.py`:150, `test_capa_generada.py`:110-113 y ADR-0068:127-129 sostienen lo que dice el informe; también D8 (`cuenta-por-mes.txt`:3123 dice 228 cierres, y los cinco goldens dicen «sin calendario»).

#### Eje (b) · Encargo
Resumen: 0 bloquea, 3 importa, 1 menor. Requisitos: 26 hechos, 2 hechos de otra forma (declarados), 3 parciales y 2 no hechos (pendientes por orden: el revisor y la frase final).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | §0 Base en 93a4fc29; CI de main 45922991122 confirmada con `gh` | Hecho | informe :15-24 |
| 2 | §0 Abrir con `abrir-rama`: encargo tal cual, contrato y Archivo | Hecho | `dbae5f7c`; HISTORIA +179 líneas, «# Archivo 86» |
| 3 | §0 Tramo R5, riesgo alto, ningún ADR | Hecho | `contrato.yaml`:2, :4 y :46 |
| 4 | §0 Lista blanca, protegidas (el perfil exacto y PREREGISTRO) y comprobaciones | Hecho | `contrato.yaml`:5-53 |
| 5 | §0/0.1 Fila de HOLDOUT antes del primer `make check` | Hecho | diff de HOLDOUT; G2 en verde |
| 6 | §1 `cubre` hacia atrás hasta ≤ 2025-01-01 | **Parcial**: `desde` en el 2025-01-09, con la PARADA (a) que prevé §4 | YAML :25; informe §3 |
| 7 | §1 Decir que la lectura hacia atrás la da ADR-0092 §5 y que D7 la escribe | Hecho | informe :28-36 |
| 8 | §2 Nada fuera de la lista (src, scripts, .claude, mql5 salvo Generado, spec, casos, evidencia, feedback, corpus, data, perfil, ADR, informes cerrados, hoja de ruta) | Hecho | `git diff --name-status main...HEAD`: 13 rutas, todas en la lista |
| 9 | §2 Las entradas del YAML no se editan; `hasta` intacto | Hecho | diff del YAML: solo cambian `desde`, comentarios y dos entradas nuevas al final |
| 10 | §2 Ni velas ni ticks de 2025, ni arnés sobre 2025 | Hecho (por el informe; `data/manifests` sin cambios) | desviación 1, informe :392-394 |
| 11 | 0.2 Inventario con fichero:línea; qué test fija un literal; `knowledge validate` no lee el calendario | Hecho | informe :45-104 (con a7) |
| 12 | 0.3 El reloj del servidor de 2025 | Hecho, sin PARADA (c) | informe :106-122; el HTML del 23 y el 30-oct |
| 13 | 0.4 La lista medida en el archivo de FTMO | **Hecho de otra forma** (con el sitemap), declarado | desviación 4; 1566 URL y 218 `/en/`, recontadas |
| 14 | 0.4 Pausa entre descargas | Hecho | las `Date` del índice, separadas unos 5 s |
| 15 | 0.5 La aritmética de `desde` | Hecho | informe :150-160 |
| 16 | 0.6 El auditor | Hecho | informe §5 |
| 17 | §4 Escribir la fase 0 y seguir, o parar por (a)-(e) | Hecho (PARADA (a) acotada) | informe §3-§4 (ver b2) |
| 18 | D1 Los extraordinarios, con URL y hora UTC de consulta | Hecho | YAML :63-81 |
| 19 | D2 Nada que no sea EURUSD; el horario sale de la API de 2026, y se declara | Hecho | informe :262-270 |
| 20 | D3 `desde` = el primer jueves revisado, el comentario con las horas y la cabecera que cita el informe | Hecho (con a4) | YAML :16 y :20-25 |
| 21 | D4 La capa en el mismo commit, su test y la compilación con logs | Hecho | `dcd680e4`; `--comprobar` al día; `compilacion/*.log`: «0 errors, 0 warnings» |
| 22 | D5(a) El parametrizado pasa a `"2024-01-01"` | Hecho | `test_cierres_de_mercado.py`:415 |
| 23 | D5(b) Test nuevo: `cubre` ≤ 2025-01-01, el motivo `MOTIVO_CIERRE` y que rompa en `main` | **Hecho de otra forma**: ≤ 2025-01-09, declarado | :370-386; informe :332-346; el motivo en `main`, reproducido en memoria |
| 24 | D5(c) El recuento de tests | Hecho | PS: 2234; `state check` OK |
| 25 | D6 La CI de Linux por `fix/` y el número de run | **Parcial**: el run es de `dcd680e4` y su resultado no está en el informe | `gh run list`; informe :421-423 |
| 26 | D7 El párrafo del runbook, con su cita y en un commit de la rama | Hecho | `RENOVAR-CIERRES.md`:20-25; `8b0011a4` |
| 27 | D8 La cabecera del arnés y los goldens | Hecho | informe :352-361; `cuenta-por-mes.txt`:3123 |
| 28 | §6 Cada commit con su `make check` sellado | Hecho | tres sellos = tres árboles |
| 29 | §6 El YAML y Generado juntos; el runbook en su commit | Hecho | `git show --stat` de `dcd680e4` y de `8b0011a4` |
| 30 | §6 El informe con la salida de `make check` y el run de la CI | **Parcial** | ver b3 |
| 31 | §6 Las líneas del cierre (R5.4, R5.6, N, e I más corta) | Hecho (I: 738 → 600 bytes, medido) | informe :428-462 (ver a1 sobre R5.6) |
| 32 | §6 El revisor, pegado | No hecho (pendiente: este informe) | informe :478 |
| 33 | §6 «Rama lista para revisión, NO cerrada.» | No hecho (pendiente) | informe :476-478: «EN CURSO» |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Falta la tabla «El encargo, punto por punto»** que piden `entregar-rama` y E5. | `Grep "punto por punto"` en el informe: sin coincidencias; `.claude/skills/entregar-rama/SKILL.md`:46-50 y :107 |
| b2 | importa | **La PARADA (a) no tiene «Lo que necesito que decidas»**, con su forma: una decisión por punto, sus opciones, «Recomiendo…» y el coste. El §3 da tres opciones y no recomienda ninguna. Además, la opción 1 está planteada con la premisa de a1. | informe :293-303; `.claude/skills/fase-cero/SKILL.md`:70-79 |
| b3 | importa | **El §7 remite a un §9 que no existe**, para el `make check` del commit del runbook y para el resultado de la CI. El informe acaba en §8 y «## Estado». Faltan los dos datos: el tercer `make check` (sello `ec6d26a3…` = árbol de `8b0011a4`, «3816 passed, 6 xfailed», 24 min 38 s, 322 MiB) y el resultado del run 45935357680 (failure, con solo `test_state_check_ok_on_real_repo`). El encargo los pide en §6. | informe :417 y :423; `make-check.log` (líneas `SELLO` y `PICO`); `gh run view 45935357680 --log-failed` |
| b4 | menor | En la tabla del §1, varias filas no nombran los avisos que no son del Forex: el Independence Day (3-jul), el Labor Day (28-ago), Thanksgiving y el mantenimiento (27-nov), y el domingo 14-sep (11-sep). La conclusión, «nada del Forex», es correcta en todas: lo comprobé con grep de Forex, currenc, EURUSD y EUR/USD, y con sus `<h3>`. | informe :209, :217, :219 y :230; `grep "<h3"` en esos HTML |

#### Lo que no pude comprobar
- **La salida del clon de `main`** («1 failed, 4 passed», con `assert 1764824400000 <= 1736398800000`): el clon ya no existe (`git worktree list` solo da el repo). Lo sustituye que reproduje en memoria los motivos de `main` y de la rama en los dos instantes.
- **El CDX del Wayback:** no sé con qué consulta se hicieron `wb-cdx3.txt` y `wb-cdx4.txt`. `wb-cdx.txt` está vacío y `wb-cdx2.txt` es un «504 Gateway Time-out». Así que «no hay capturas de 2024 ni de 2025» no lo puedo confirmar.
- **Si existe otra fuente oficial de FTMO** (blog, FAQ, notas de prensa): no tengo red para mirarla. Solo constato que no se buscó (a2).
- **Qué `Generado.mqh` compiló MetaEditor:** el log trae el sha256 del `.mq5`, no el de la capa incluida.
- **El informe del auditor** (52, 36, 0 y 16): no está en el repo.
- **Que el YAML y el runbook se editaron con Edit:** no deja rastro.
- **La orden de las «56 entradas en el orden del sitemap»:** no la comprobé. Sí comprobé que hay Trading Update `/en/` para cada jueves del 9-ene al 27-nov-2025 salvo el 1-may, y que faltan el 26-dic-2024 y nada más de diciembre de 2024.
- **`knowledge validate` suelto:** no lo lancé. La evidencia es su bloque en `make-check.log`, todo en OK.
- **Aviso:** son las 23:10 de Lima (04:10 UTC). Si el `make check` que selle este informe empieza pasada la medianoche local, G2 exige antes la fila de HOLDOUT del 2026-11-27.

#### Comandos ejecutados
1. `git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`
2. `date -u`
3. `git log --format='%h %ad | %cd | %s' --date=iso main..HEAD`
4. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md docs/runbooks/RENOVAR-CIERRES.md knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml tests/unit/test_cierres_de_mercado.py PROJECT_STATE.md`
5. `uv run python scripts/contrato_rama.py`
6. `uv run botsito state check`
7. `uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k --comprobar`
8. `uv run pytest tests/unit/test_cierres_de_mercado.py tests/unit/test_renovar_cierres.py tests/unit/test_capa_generada.py tests/unit/test_f17_historial_criterio.py -q -p no:cacheprovider`
9. `gh run view 45935357680 --log-failed`; `gh run view 45935357680 --json headSha,headBranch,status,conclusion,databaseId`; `gh run list --branch fix/renovar-cierres-2026-11-26 --limit 5`
10. `ls -la` de `C:/Users/USER/.claude/jobs/630cf772/tmp/tu/`; `sha256sum trading-update-*.html`; `python -I -c` que compara `indice.tsv` con sha256 y bytes (56 filas, 0 discrepancias)
11. `grep` de solo texto sobre las descargas: 6-mar, 30-oct, 23-oct, 19-dic y 2-ene (`schedule below`), `instruments-table`, `<table`, la Semana Santa, Thanksgiving, el Independence Day, Forex/currenc/EURUSD, Sunday, días laborables, cabeceras HTTP, `sitemap.xml`, `tu-sitemap1/2.xml`, `wb-*`
12. `uv run python -c` que carga en memoria el calendario de `main` (`git show`) y el de la rama: recuentos, los 218 iguales, los largos, las 17:00 de Madrid y los extraordinarios de 2025
13. `uv run python -c` con `ventana_prohibida_por_cierre` en `main` y en la rama, el 7-mar-2025 a las 15:30 y a las 14:54 de Nueva York
14. `git diff main...HEAD -- mql5/Include/Botsito/Capa/Generado.mqh | grep ...`
15. `sed -n` de `cuenta-por-mes.txt`:3120-3125 y de `cableado.py`:1262-1271; `git grep -n -i cierres -- tests/golden`
16. `git log --format='%h' main..HEAD -- knowledge/spec knowledge/cases`; `git grep -n DIRECTORIOS_CON_FUENTE -- src`; `git diff --name-status main...HEAD`; `git log --format='%h%n%B' main..HEAD`
17. `ls -la make-check.log`; `grep` de `SELLO`, `PICO`, `passed` y `knowledge` en `make-check.log`; `sed -n '112,131p' make-check.log`
18. `git rev-parse HEAD^{tree} dcd680e4^{tree} dbae5f7c^{tree}`
19. `git diff --numstat main...HEAD -- docs/state/HISTORIA.md docs/runbooks/RENOVAR-CIERRES.md docs/validation/HOLDOUT-EXPOSICIONES.md`
20. `wc -c PROJECT_STATE.md`; `sed -n '36p;46p' PROJECT_STATE.md`; `python -I -c` que mide las líneas I (738 y 600 bytes)
21. `sed -n` de `test_renovar_cierres.py`, `test_capa_generada.py`, `test_f17_historial_criterio.py`, `FTMO-REGLAS.md`:62, ADR-0068:125-130, `CIERRES-DE-MERCADO.md`:104-144 y `RITUAL.md`:95-110
22. `git show --stat` de los tres commits; `git worktree list`; `git branch --list`; `git ls-files docs/validation/anexos/RENOVAR-CIERRES-2025`
23. Read de: el encargo, `contrato.yaml`, el informe, `indice.tsv`, el YAML, `test_cierres_de_mercado.py` (:1-80 y :340-429), `calendario_cierres.py`:82-206, ADR-0092:125-159, `HOJA-DE-RUTA.md`:500-534, el log de compilación de Botsito y las skills `entregar-rama` y `fase-cero`; Grep de «renovado hacia atr» en `docs/` y de «punto por punto» en el informe y en las skills

## Estado

Lista para revisión. Pendiente del consultor: la decisión de §3 (la Navidad de 2024) y las líneas
del cierre de §8.

Rama lista para revisión, NO cerrada.
