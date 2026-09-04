# F15 · market-data-ohlc

**Rama:** `feature/F15-market-data-ohlc` · **Fase:** 4 (abierta por el orden E antes de cerrar la
fase 1) · **Depende de:** F02

## Objetivo
Velas M1 reproducibles del instrumento del trader, congeladas por hash, y su agregacion a M15 y H4
con anclaje configurable y huso explicito, correcta en los dos cambios de hora. Es la base de los
casos con datos reales (F10, F14), del motor (F18+) y de la paridad con MQL5 (F29, F33).

## Alcance cerrado (que SI)
- `src/botsito/domain/velas.py` (dominio puro, sin `datetime`, `float` ni `Decimal`): `Vela`
  (`inicio: MinutoUtc` = minutos enteros desde la epoca UTC, `abierta/maxima/minima/cierre:
  Puntos`, `volumen: int`, `duracion_min`, `n_m1`, `completa`), `SerieVelas` (simbolo, periodo,
  `escala`, `escala_volumen`, velas ordenadas), `combinar`. `Puntos = NewType(int)` en
  `valores.py`. El dominio consumira velas desde F18, por eso no viven en `data/`.
- `src/botsito/data/velas.py`: conversion `datetime` <-> `MinutoUtc` y CSV determinista
  (`ts_utc,abierta,maxima,minima,cierre,volumen`; el agregado anade `duracion_min,n_m1,completa`),
  LF sin BOM, ascendente, sin duplicados, todo entero; lectura estricta (sin espacios ni `+`).
- `src/botsito/data/agregacion.py`: `agregar(velas_m1, periodo_min, anclaje: HoraLocal)` con
  **particion de la recta UTC por reloj de pared**: limite = todo instante UTC cuya hora de pared
  en el huso del anclaje cumple `minuto_del_dia ≡ anclaje (mod periodo)`, enumerando los dias
  locales con margen y deduplicando en UTC. Salto de primavera: el limite inexistente se omite
  (vela de `periodo - 60`). Hora repetida de otono: los dos instantes son limites (vela de 60 min
  si un limite cae dentro, `periodo + 60` si no). Una M1 pertenece al ultimo limite <= inicio; no
  se inventan velas; `completa` = su limite de cierre ya paso. `1440 % periodo == 0` obligatorio.
  Invariantes: limites estrictamente crecientes, duraciones en `{periodo-60, periodo, periodo+60,
  60}`, cada M1 en exactamente una vela, `M1->M15->H4 == M1->H4`. En FX los cuatro cambios de
  hora caen con el mercado cerrado: lo observable en datos reales es que los limites UTC se
  desplazan una hora entre semanas, y solo para el anclaje cuyo huso cambio.
- `src/botsito/data/dukascopy.py` (hechos del proveedor, no de negocio): `BID_candles_min_1.bi5`
  por dia (mes en base 0, LZMA, 24 bytes `>iiiiif` = `t_s, abierta, cierre, minima, maxima,
  volumen`), funcion de red **inyectada**, reintentos con espera creciente, `User-Agent`
  obligatorio; velas planas de volumen cero (sin ticks; MT5 tampoco las construye) descartadas y
  contadas, con recuento aparte de las descartadas en laborable y de las de volumen cero no
  planas (conservadas); volumen float32 -> entero en milesimas (`escala_volumen = 1000`);
  `filtro_planas` y `decodificador_version` en el manifiesto.
- `src/botsito/data/dataset.py`: `data/ohlc/<dataset_id>/<SIMBOLO>_M1_<AAAA-MM>.csv` (ignorado)
  + `data/manifests/<dataset_id>.yaml` (versionado, INMUTABLE: guardia de historial y hook; H.2).
  `dataset_id = <nombre>-<8 hex del sha256 de los sha256 de los ficheros>`: bytes distintos son
  otro dataset (`reemplaza_a` enlaza). Campos: `schema_version`, `proveedor`, `tipo_precio`,
  `simbolo`, `simbolo_proveedor`, `escala`, `escala_volumen`, `huso_datos: UTC` (fijo, validado),
  `periodo_min`, `filtro_planas`, `decodificador_version`, `desde/hasta` (`hasta` < hoy: el dia en
  curso es parcial), `descargado_el`, `generado_por`, ficheros (`ruta, bytes, sha256, filas,
  primera, ultima`), `dias` (presentes, ausentes = 404, sin_datos = cuerpo vacio, registros,
  descartes) y `huecos` (recuento < 60 min, lista >= 60 min). `comprobar` (tamanos/hashes),
  `cargar_serie(manifiesto, carpeta, desde, hasta)` con ventana por dias (F10/F14 cargan la
  ventana de un caso). Esta capa no importa registro ni historial: la CLI se los pasa.
- CLI: `botsito data download --dataset <nombre> --simbolo <S> --escala <n> --desde --hasta
  [--reemplaza-a]`, `data check --dataset <id|nombre> [--hashes]`, `data aggregate --dataset
  --periodo --anclaje "HH:MM Zona/IANA" [--desde --hasta --salida --incluir-incompletas]` (omite
  por defecto las velas de borde sin cerrar). `knowledge validate` valida los manifiestos y su
  historial; el hook protege `data/manifests/`.
- Registro (`knowledge/spec/parametros.yaml`, commit con `Fuente: ADR-0005`): `huso_operativa`
  (`texto`, `ejecucion`, CONFIRMED `Europe/Madrid`: huso de informes, journal y "dia del trader";
  no sustituye al `huso` de cada `hora`, ADR-0004) y `anclaje_h4` (`hora`, `estrategia`,
  **UNKNOWN**, sin `huso`: el huso es parte de A-9). `huso_datos` NO es parametro: lo declara cada
  manifiesto (una sola puerta por valor, ADR-0002). El CLI exige `--anclaje` explicito mientras
  `anclaje_h4` sea UNKNOWN. El test "registro vacio de valores" pasa a "sin valores de estrategia".
- El reloj de servidor del broker se representa como `17:00 America/New_York` (= 00:00 servidor
  en brokers GMT+2/+3 con DST de Nueva York). Es una **aproximacion declarada**, verificable solo
  en F17 contra el terminal; el riesgo (brokers con DST europeo u offset fijo) va a H.2.
- Fixtures reales en `tests/fixtures/ohlc/` (bi5 sin tocar, 3-12 KB cada uno, sha256 en su
  README): viernes + domingo + lunes de cada cambio de hora (UE 2026-03-29 y 2025-10-26; EE. UU.
  2026-03-08 y 2025-11-02), los domingos anteriores (desplazamiento semanal) y 2026-07-02 (dia
  del caso del trader). Goldens H4 de 2026-07-02 con dos anclajes en `tests/golden/ohlc/`.
- ADR-0005: fuente de datos, formato entero en puntos, tres relojes y regla de anclaje.

## Fuera de alcance (que NO)
Ticks (F16), grabador de demo (F17), descarga desde MetaTrader 5 (no hay terminal en la maquina de
desarrollo; el adaptador MT5 llega con F17/F33), Parquet (F16 decide), velas ASK o spread (F16),
golden contra la captura del grafico del trader (F07, sobre estos mismos fixtures), valores de
`anclaje_h4` (A-9, sesion 1).

## Entradas
Dukascopy datafeed (publico, sin cuenta), `HoraLocal` y `zoneinfo` (ADR-0004), `yaml_estricto`,
`historial.py` (guardia generalizada).

## Salidas (ficheros)
`src/botsito/domain/velas.py`, `src/botsito/domain/valores.py` (`Puntos`),
`src/botsito/data/{velas,agregacion,dukascopy,dataset}.py`, `src/botsito/cli.py` (`data`),
`knowledge/spec/parametros.yaml` (2 parametros), `docs/adr/0005-datos-de-mercado-fuente-formato-y-relojes.md`,
`data/manifests/README.md` (esquema) y `data/manifests/eurusd-m1-2026-{01,07,08}-<hash>.yaml`,
`scripts/git-hooks/pre-commit` (data/manifests inmutable), `tests/unit/test_velas.py`,
`test_agregacion.py`, `test_agregacion_dst.py`, `test_dukascopy.py`, `test_dataset.py`,
`test_cli_data.py`, `test_golden_ohlc.py`, `tests/contract/test_data_manifest_history.py`,
`tests/fixtures/ohlc/*.bi5` (+ README con sha256), `tests/golden/ohlc/*.csv`.

## Tests
- Unit: invariantes de `Vela` y `SerieVelas`; CSV ida y vuelta determinista (M1 y agregado; CR,
  BOM, espacios y `+` rechazados); decodificacion bi5 sobre bytes sinteticos y sobre los ficheros
  reales; filtro de velas planas con sus recuentos; reintentos y fallo cerrado de la descarga.
- Agregacion: M15 y H4 sobre M1 sintetico con valores conocidos; propiedad (hypothesis): maxima
  agregada = max de las M1, minima = min, abierta = primera, cierre = ultima, volumen = suma; sin
  velas inventadas; causalidad (truncar la serie no cambia las velas cerradas anteriores).
- DST con datos reales: limites UTC esperados a mano para viernes y lunes de las cuatro semanas
  de cambio con ambos anclajes; desplazamiento semanal (primera H4 del domingo X vs. X+7 se
  mueve una hora solo para el anclaje cuyo huso cambio); semana completa sin duplicar limites.
- DST con M1 sintetico 24/7: vela de 3 h (primavera, ambos husos), 5 h (otono UE), 1 h + 4 h
  (otono EE. UU. con anclaje de servidor), M15 sin vela de 75 min en la hora repetida, vela de
  borde incompleta al inicio de un dataset, y un semestre entero con las duraciones admisibles.
- Asociatividad: `M1->M15->H4 == M1->H4` y `M1->H1->H4 == M1->H4` sobre el dia real.
- Golden: H4 del 2026-07-02 con ambos anclajes, fichero esperado versionado (dos velas
  comprobadas a mano en el informe).
- Dataset: descarga simulada con dias 404, vacios y con tarde plana; manifiesto determinista e
  inmutable (mismo contenido = mismo id; distinto = otro id con `reemplaza_a`); `comprobar`
  detecta tamano, hash y ausencia; ventana por dias; manifiesto editado o corrupto (12 casos);
  fichero inesperado; historial de git (modificar/borrar detectados, README exento).
- CLI: `download` -> `check --hashes` -> `aggregate` (fichero y salida estandar, borde omitido)
  en un repo temporal con descarga inyectada; fechas y repo invalidos; anclaje invalido.
- Contrato: `domain/` no importa `data/` ni `datetime`; `data/` no importa `engine/`; sin
  `EURUSD`, `Europe/Madrid`, `America/New_York` ni horas literales en `src/` (detector).

## Criterio de aceptacion
`make check` verde; DST correcto en los cuatro cambios de hora con dos anclajes (real y
sintetico); golden del 2026-07-02 revisado; tres datasets reales (enero, julio y agosto de 2026)
descargados en local con manifiesto versionado y `data check --hashes` en verde; `anclaje_h4`
UNKNOWN en el registro con A-9. Lo que el plan llamaba "H4 = las del trader" se verifica en F07
con su captura.

## Riesgos
- Dukascopy es un proveedor distinto del broker (FundedNext): precios BID y horario de mercado
  pueden diferir en minutos aislados. Se declara en el manifiesto; F16/F33 comparan con la demo.
- El servidor exige `User-Agent` y a veces tarda >15 s: reintentos con espera creciente y
  descarga por dias con reanudacion (los ficheros ya presentes con hash correcto no se repiten).
- Un anclaje a una hora inexistente o ambigua del dia de cambio: regla explicita arriba y test.
- El reloj de servidor como `17:00 America/New_York` es una aproximacion: F11 declara
  `dst_servidor` y `offset_base_servidor` (categoria `broker`, por ADR) y F17 registra el offset
  real por evento; el modulo `MetaTrader5` de Python devuelve `time` en hora de servidor.

## Que habilita
F16 (ticks contra M1), F10 y F14 (casos con datos reales), F18+ (motor), F29/F33 (paridad H4).
