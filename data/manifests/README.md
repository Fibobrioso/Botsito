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
