# data/manifests/ — manifiestos INMUTABLES de los datasets congelados (F15, ADR-0005)

Los datos no entran en git (`/data/*` esta ignorado salvo esta carpeta). Cada dataset de velas
M1 tiene aqui `<dataset_id>.yaml`, GENERADO por `botsito data download`, y sus ficheros viven en
`data/ohlc/<dataset_id>/<SIMBOLO>_M1_<AAAA-MM>.csv`. Un manifiesto no se edita ni se borra: el
hook `pre-commit` y `knowledge validate` (guardia de historial de git) lo rechazan. Una
re-descarga que cambie datos es un `dataset_id` nuevo.

## Esquema (`schema_version: 1`)

| Campo | Contenido |
|---|---|
| `dataset_id` | `<nombre>-<8 hex>`: sufijo = sha256 de los sha256 de los ficheros; nombre del fichero |
| `proveedor`, `tipo_precio`, `simbolo`, `simbolo_proveedor` | `dukascopy`, `BID`, simbolo y su nombre en el proveedor |
| `escala`, `escala_volumen` | puntos por unidad (EURUSD: 100000) y milesimas de volumen (1000) |
| `huso_datos`, `periodo_min` | `UTC` (fijo, validado) y `1` para M1 |
| `filtro_planas`, `decodificador_version` | version de la regla de descarte y del decodificador |
| `desde`, `hasta`, `descargado_el` | rango inclusivo (`hasta` < dia de descarga) y fecha de descarga |
| `generado_por`, `reemplaza_a` | commit de botsito (opcional) y dataset al que sustituye (opcional) |
| `ficheros[]` | `ruta` (relativa a la carpeta `[rutas].data` de settings, por defecto `data/`), `bytes`, `sha256`, `filas`, `primera`, `ultima` |
| `dias` | `presentes`, `ausentes[]` (404), `sin_datos[]` (cuerpo vacio), `registros`, `descartadas_planas_sin_volumen`, `descartadas_dentro_de_sesion`, `volumen_cero_no_planas`, `velas` |
| `huecos` | `menores_de_60_min` (recuento) y `mayores[]` con `desde`, `hasta`, `minutos` (fines de semana, festivos, caidas) |

CSV M1: `ts_utc,abierta,maxima,minima,cierre,volumen`, LF sin BOM, ascendente, sin duplicados,
todo entero (precios en puntos, volumen en milesimas); `ts_utc` como `AAAA-MM-DDTHH:MMZ`. El CSV
agregado (`data aggregate`) anade `duracion_min,n_m1,completa`.

## Comandos
```
botsito data download --dataset eurusd-m1-2026-07 --simbolo EURUSD --escala 100000 \
  --desde 2026-07-01 --hasta 2026-07-31          # crea eurusd-m1-2026-07-<hash8>
botsito data check --dataset eurusd-m1-2026-07 --hashes
botsito data aggregate --dataset eurusd-m1-2026-07 --periodo 240 --anclaje "00:00 Europe/Madrid" \
  --desde 2026-07-02 --hasta 2026-07-02 [--salida h4.csv] [--incluir-incompletas]
```
`--anclaje` es obligatorio mientras `anclaje_h4` siga UNKNOWN en el registro (A-9). El reloj de
servidor de un broker MT5 tipico se expresa como `17:00 America/New_York`. Las velas de borde sin
cerrar se omiten salvo `--incluir-incompletas`. Por convencion, el commit del manifiesto cita
`Fuente: ADR-0005` (la guardia de trailers solo vigila `knowledge/spec` y `knowledge/cases`). La
descarga cachea cada dia crudo en `<datos>/raw/<SIMBOLO>/` y se reanuda si se interrumpe.

## Ticks (`ticks/`, rama `trabajo/ticks-llenado`, ADR-0051)

Los ticks de CONSTRUCCION (abril y agosto de 2026) se congelan con el mismo procedimiento y la
misma politica: `botsito data download-ticks` descarga hora a hora en streaming
(`{SIMBOLO}/{AAAA}/{MM-1}/{DD}/{HH}h_ticks.bi5`, `>IIIff` = ms en la hora, ASK, BID, volumenes),
escribe `data/ticks/<dataset_id>/<SIMBOLO>_TICKS_<AAAA-MM-DD>.csv` (un fichero por dia:
`ts_utc,ask,bid,volumen_ask,volumen_bid`, ms en `AAAA-MM-DDTHH:MM:SS.mmmZ`, volumenes en
milesimas) y el manifiesto INMUTABLE `data/manifests/ticks/<dataset_id>.yaml` (`schema_ticks: 1`;
`horas`: presentes, ausentes_404, vacias y `perdidas[]` -las que fallaron tras 5 intentos con
espera creciente-; `ticks`: total y cotizaciones cruzadas). La cache cruda va a
`raw/<SIMBOLO>/ticks/<AAAA-MM-DD>/<HH>.bi5`. El comando SE NIEGA a cualquier mes que no sea de
construccion (`criterio_fidelidad.yaml`). `botsito data check-ticks --dataset <id> --hashes`
compara con el disco. Commit del manifiesto con Fuente: ADR-0051.

## Demo de FTMO (`demo_ftmo/`, rama `trabajo/demo-ejecucion-1`)

Cada CSV de `tools/mql5/MedirDemoFTMO.mq5` que se use para fijar un valor se congela aqui
(`docs/runbooks/DEMO-FTMO.md`, «Dónde queda el fichero y a dónde va»). El CSV vive en
`data/demo_ftmo/`, fuera de git, con el nombre que le da MetaTrader; el manifiesto
`data/manifests/demo_ftmo/<dataset_id>.yaml` es INMUTABLE como los demas (misma guardia: todo `.yaml`
bajo `data/manifests/`). No hay comando que lo genere: se escribe a mano con `sha256sum` y el lector
(`scripts/leer_demo_ftmo.py`) delante, y `knowledge validate` no lo carga como dataset de velas
(solo lee la raiz). Esquema (`schema_demo_ftmo: 1`):

| Campo | Contenido |
|---|---|
| `dataset_id` | `demo-ftmo-<AAAA-MM-DD del servidor>-<8 hex>`: el sufijo son los 8 primeros del sha256 del CSV |
| `ejecucion` | 1, 2 o 3 (`DEMO-FTMO.md`, «Cuándo: tres veces») |
| `fichero` | `ruta` (relativa a `data/`), `bytes`, `sha256`, `filas` de datos sin la cabecera y `fin_de_linea` |
| `script` | `ruta`, `version` (la columna `version_script`), `sha256` del `.mq5` y el `commit` que lo trajo |
| `cuenta` | `servidor`, `empresa`, `moneda`, `tipo` y `build_terminal`, de las filas de contexto |
| `hora_servidor_primera`, `hora_servidor_ultima`, `hora_gmt_primera` | de la primera y la ultima fila |
| `terminado`, `quedan_abiertas_al_terminar` | las filas `terminado` y `quedan_abiertas_al_terminar` |
| `declarado_por`, `congelado_el`, `rama`, `informe` | quien lo copio y como, cuando y donde se congelo |

El valor que salga de un CSV entra en `knowledge/` citando el ADR que cita su manifiesto y su fila
(el trailer `Fuente:` no admite un manifiesto).

## Historial de ticks de FTMO (`f17/`, rama `trabajo/f17-historial`)

Lo que exporta `tools/mql5/ExportarTicksFTMO.mq5` desde la demo de FTMO (F17, ADR-0099 §5): por dia
de un mes de construccion, `F17_<AAAA-MM-DD>_ticks.csv` (`time_msc,bid,ask,flags`) y
`F17_<AAAA-MM-DD>_m1.csv` (`time,open,high,low,close,tick_volume,spread,real_volume`), y un
`F17_control_<AAAAMMDD_HHMMSS>.csv` (`clave,valor,nota`) con los relojes y lo pedido. Los CSV viven
en `data/f17/<AAAA-MM>/`, fuera de git, con el nombre que les da el script, en ANSI y CRLF; el
manifiesto, `data/manifests/f17/<dataset_id>.yaml`, uno por mes, es INMUTABLE como los demas. Va
aparte de `demo_ftmo/` porque `tests/unit/test_manifiestos_demo_ftmo.py` exige alli exactamente las
ejecuciones 1, 2 y 3, y no es un dataset de velas del bot (el esquema v2 `mt5_demo` de MASTER_PLAN
§H no existe en `src/`). Se escribe a mano con `sha256sum` y el lector
(`scripts/leer_historial_f17.py`) delante; el esquema lo comprueba su `validar_manifiesto` en
`tests/unit/test_manifiestos_f17.py` (la CLI del lector todavía no lo llama); el runbook es `docs/runbooks/F17-HISTORIAL.md`. Que un mes
CUBRA no autoriza a usar sus ticks como fuente de una medida: eso pide un ADR que enmiende ADR-0005 y
ADR-0024 §4. Esquema (`schema_f17_historial: 1`):

| Campo | Contenido |
|---|---|
| `dataset_id` | `f17-historial-<AAAA-MM>-<8 hex>`: el sufijo son los 8 primeros del sha256 de los sha256 de sus ficheros, ordenados por su ruta |
| `mes` | el mes, de `construccion` de `criterio_fidelidad.yaml` |
| `ficheros[]` | `ruta` (relativa a `data/`), `tipo` (`ticks`, `m1` o `control`), `bytes`, `sha256`, `filas` de datos sin la cabecera y `fin_de_linea` (medido con Python o `grep -U`, no con `grep` a secas) |
| `dias` | `pedidos`, `con_ticks` y `sin_ticks[]`, de las filas `dia_*` del control |
| `primer_tick_msc_servidor` | el primer tick del mes, buscado dentro de ese mes (fila `mes_<AAAA-MM>_primer_msc`) |
| `primera_m1_servidor_s` | la primera M1 del servidor, por `SeriesInfoInteger` (metadato de la serie) |
| `control` | `time_trade_server_s`, `time_gmt_s`, `desfase_servidor_gmt_min` y `cuadra`: si ese desfase es el que da el registro (`broker_offset_base` y `broker_dst`) en ese instante |
| `script` | `ruta`, `version` (la fila `version_script`), `sha256` del `.mq5` y el `commit` que lo trajo |
| `cuenta` | `servidor`, `empresa` y `build`, del control |
| `declarado_por`, `congelado_el`, `rama`, `informe` | quien lo copio y como, cuando y donde se congelo |

## La medida de las ordenes stop y el grabador de FTMO (`f17-ordenes/` y `f17-grabador/`, rama `trabajo/f17-ordenes`)

Lo que graban `tools/mql5/MedirOrdenesFTMO.mq5` y `tools/mql5/GrabarTicksFTMO.mq5` en la demo de
FTMO (F17, ADR-0099 §5): de la medida, `F17M_<estrato>_<AAAAMMDD_HHMMSS>.csv` por ejecucion y
`F17M_ticks_<deal>.csv` (`time_msc,bid,ask,flags`) por llenado; del grabador,
`F17G_<AAAA-MM-DD>_<HH>.csv` (`time_msc,bid,ask,flags`) por hora del servidor y
`F17G_control_<AAAAMMDD_HHMMSS>.csv` (`clave,valor,nota`) por arranque. Los CSV viven en
`data/f17-ordenes/<AAAA-MM-DD>/` y `data/f17-grabador/<AAAA-MM-DD>/`, fuera de git, con el nombre que
les da el script, en ANSI y CRLF. Los manifiestos van en sus carpetas, `data/manifests/f17-ordenes/` y
`data/manifests/f17-grabador/`, **nunca en `f17/`**: `tests/unit/test_manifiestos_f17.py` valida todo
lo de alli con el esquema del historial, que exige un mes de construccion, y estos dias nunca lo son.
Son INMUTABLES como los demas, y en esas carpetas solo van `.yaml` (`knowledge validate`). Se escriben a
mano con `sha256sum` y el lector (`scripts/leer_ordenes_f17.py`) delante; los esquemas los comprueba
su `validar_manifiesto` en `tests/unit/test_manifiestos_f17_ordenes.py`; el runbook es
`docs/runbooks/F17-ORDENES.md`. Que se lean no los convierte en fuente de una medida: eso pide un ADR
que enmiende ADR-0005 y ADR-0024 §4 (ADR-0099 §5). Esquemas (`schema_f17_ordenes: 1` y
`schema_f17_grabador: 1`):

| Campo | Contenido |
|---|---|
| `schema_f17_ordenes` o `schema_f17_grabador` | 1 |
| `dataset_id` | `f17-ordenes-<AAAA-MM-DD>-<8 hex>` o `f17-grabador-<AAAA-MM-DD>-<8 hex>`: el sufijo, como en el historial |
| `estrato` | solo en la medida: `uno` o `bot`, el de la ejecucion |
| `ficheros[]` | `ruta` (relativa a `data/`), `tipo` (la medida: `medida` o `ticks`; el grabador: `hora` o `control`), `bytes`, `sha256`, `filas` de datos sin la cabecera y `fin_de_linea` |
| `dias` | cuantos dias cubre, por recuento (para HOLDOUT-EXPOSICIONES, sin fechas: D6) |
| `script` | `ruta`, `version` (la de su CSV), `sha256` del `.mq5` y el `commit` que lo trajo |
| `control` | `time_trade_server_s`, `time_gmt_s`, `desfase_servidor_gmt_min` y `cuadra`: si ese desfase es el que da el registro (`broker_offset_base` y `broker_dst`) en ese instante |
| `cuenta` | DEMO, con `servidor`, del CSV; **nunca el `login`** que apunta el control del grabador (el repositorio es público) |
| `declarado_por`, `congelado_el`, `rama`, `informe` | quien lo copio y como, cuando y donde se congelo |
