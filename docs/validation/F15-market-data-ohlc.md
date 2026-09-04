# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F15 · market-data-ohlc
**Rama:** `feature/F15-market-data-ohlc`
**Objetivo:** velas M1 del instrumento del trader reproducibles y congeladas por hash, y su
agregacion a M15 y H4 con anclaje configurable y huso explicito, correcta en los cuatro cambios
de hora del ano. Base de los casos con datos reales (F10, F14), del motor (F18+) y de la paridad
con MQL5 (F29, F33).

## Que se construyo
- `src/botsito/domain/velas.py` (dominio puro, sin `datetime`, `float` ni `Decimal`): `Vela`
  (`inicio: MinutoUtc` = minutos enteros desde la epoca UTC, precios `Puntos` enteros, `volumen`
  entero, `duracion_min`, `n_m1`, `completa`), `SerieVelas` (simbolo, periodo, `escala`,
  `escala_volumen`), `combinar`. `Puntos = NewType(int)` en `valores.py`.
- `src/botsito/data/velas.py`: conversion `datetime` <-> `MinutoUtc` y CSV determinista, LF sin
  BOM, ascendente, sin duplicados, todo entero, lectura estricta.
- `src/botsito/data/agregacion.py`: particion de la recta UTC por reloj de pared del huso del
  anclaje (ADR-0005): limite = todo instante UTC cuya hora de pared cumple `minuto ≡ anclaje
  (mod periodo)`; salto de primavera omite el limite; hora repetida de otono los duplica; una M1
  pertenece al ultimo limite <= inicio; no se inventan velas; `completa` = el limite de cierre ya
  paso.
- `src/botsito/data/dukascopy.py`: proveedor publico (bi5: LZMA, 24 bytes `>iiiiif`, mes en base
  0), red inyectada, reintentos, `User-Agent`; velas planas de volumen cero descartadas y
  contadas (y aparte: descartadas dentro de sesion, volumen cero no planas conservadas).
- `src/botsito/data/dataset.py`: dataset por meses en `data/ohlc/<id>/` (ignorado) + manifiesto
  INMUTABLE en `data/manifests/<id>.yaml` con `dataset_id = <nombre>-<hash8 del contenido>`,
  `reemplaza_a`, `hasta < hoy`, `comprobar` (tamanos/hashes), `cargar_serie` con ventana por dias.
- CLI: `botsito data download | check | aggregate`; `knowledge validate` valida los manifiestos
  y su historial de git; el hook rechaza editar, renombrar o borrar un manifiesto.
- Registro (`Fuente: ADR-0005`): `huso_operativa` (`ejecucion`, CONFIRMED `Europe/Madrid`) y
  `anclaje_h4` (`estrategia`, UNKNOWN, sin huso: A-9). `huso_datos` no es parametro (lo declara
  cada manifiesto, una puerta por valor).
- ADR-0005. 16 fixtures reales bi5 (sha256 en `tests/fixtures/ohlc/README.md`). Goldens H4 del
  2026-07-02 con dos anclajes en `tests/golden/ohlc/`.
- Descarga con cache por dia del fichero crudo (`<datos>/raw/<SIMBOLO>/`, 404 recordado): una
  descarga interrumpida se reanuda (hallazgo de la auditoria de cierre: el brief lo prometia).

## Archivos creados
```
src/botsito/domain/velas.py  src/botsito/data/{velas,agregacion,dukascopy,dataset}.py
docs/adr/0005-datos-de-mercado-fuente-formato-y-relojes.md
docs/plan/features/F15-market-data-ohlc.md  docs/validation/F15-market-data-ohlc.md
tests/unit/test_{velas,dukascopy,agregacion,agregacion_dst,dataset,cli_data,golden_ohlc}.py
tests/contract/test_data_manifest_history.py  tests/fixtures/ohlc/*.bi5 (+ README)
tests/golden/ohlc/EURUSD_2026-07-02_H4_{madrid,servidor}.csv
data/manifests/eurusd-m1-2026-{01,07,08}-<hash>.yaml
```

## Archivos modificados
`src/botsito/cli.py` (`data`, validacion de manifiestos), `src/botsito/domain/valores.py`
(`Puntos`), `knowledge/spec/parametros.yaml`, `scripts/git-hooks/pre-commit`, `.gitattributes`,
`data/manifests/README.md`, `docs/adr/README.md`, `docs/plan/MASTER_PLAN.md` (H.2),
`tests/contract/test_no_business_literals.py` (husos prohibidos), `tests/unit/test_registro.py`,
`PROJECT_STATE.md`.

## Decisiones tomadas
- **Revision de diseno antes de programar** (agente revisor sobre el brief). Cambios aceptados:
  las velas de 3 h o 5 h no existen en datos reales de divisas (los cambios de hora caen con el
  mercado cerrado; lo observable es un desplazamiento de una hora de los limites UTC entre
  semanas), `Vela` en `domain/` sin `Decimal`, volumen entero en milesimas, `huso_datos` fuera
  del registro, `anclaje_h4` sin huso mientras sea UNKNOWN, id de dataset con hash del contenido,
  velas de borde `completa`, `hasta < hoy`, regla de anclaje formulada como particion de UTC.
- **Dukascopy y no MetaTrader 5**: no hay terminal en la maquina de desarrollo y el proveedor
  publico es reproducible por hash sin cuenta; el adaptador MT5 llega con F17/F33.
- **Reloj de servidor como `17:00 America/New_York`**: aproximacion declarada (brokers MT5 con
  DST de Nueva York), verificable solo en F17; F11 declara `dst_servidor` (H.2).
- **Velas planas de volumen cero descartadas tambien dentro de la sesion**: significan "sin
  ticks" y MT5 tampoco construye esa vela; se cuentan aparte para revisarlas.
- **`huso_operativa` en categoria `ejecucion`**: es un hecho del entorno del trader que no se le
  pregunta; ADR-0005 lo deja escrito como ampliacion de ADR-0004.

## Como ejecutarlo
```
make check
uv run botsito data download --dataset eurusd-m1-2026-07 --simbolo EURUSD --escala 100000 \
  --desde 2026-07-01 --hasta 2026-07-31        # ~15 s por dia; crea eurusd-m1-2026-07-<hash8>
uv run botsito data check --dataset eurusd-m1-2026-07 --hashes
uv run botsito data aggregate --dataset eurusd-m1-2026-07 --periodo 240 \
  --anclaje "00:00 Europe/Madrid" --desde 2026-07-02 --hasta 2026-07-02
uv run botsito data aggregate --dataset eurusd-m1-2026-07 --periodo 240 \
  --anclaje "17:00 America/New_York" --desde 2026-07-02 --hasta 2026-07-02
uv run botsito knowledge validate
```

## Como probarlo
- Comparar la salida de `aggregate` del 2026-07-02 con `tests/golden/ohlc/*.csv` (identica).
- Editar a mano un manifiesto de `data/manifests/` e intentar commitear: el hook lo rechaza; con
  `--no-verify`, `knowledge validate` y el test de historial fallan. Probado en un repo temporal
  por la auditoria: anadir OK; editar, borrar, renombrar y renombrar `_tmp.yaml` a un id
  rechazados; README y `_tmp.yaml` exentos.
- Cambiar un byte de un CSV de `data/ohlc/`: `data check --hashes` lo detecta; `aggregate`
  se niega a cargarlo ("dataset alterado").
- `aggregate --anclaje "00:00 Europe/Madrid"` de la semana del 2026-03-29 frente a la del 22:
  la primera H4 del domingo pasa de 19:00Z a 18:00Z; con `17:00 America/New_York` no se mueve.

## Tests ejecutados
`make check` en `feature/F15-market-data-ohlc`, Windows 11, Python 3.12 (`.python-version`), desde
Git Bash y desde PowerShell 7 (ambos verdes).

## Resultados
- ruff, mypy strict (63 ficheros), 3 contratos KEPT.
- pytest: 317 passed (203 funciones). De F15: velas (invariantes, CSV, propiedad), dukascopy
  (bi5 sintetico y real, planas, reintentos), agregacion (sintetico, propiedad hypothesis,
  causalidad, limites por dia, 18 casos reales sobre 11 dias de las semanas de cambio con
  limites derivados a mano), agregacion_dst (3 h, 5 h, 1 h + 4 h, M15 en la hora repetida,
  desplazamiento semanal con 8 pares de domingos reales, asociatividad, borde incompleto,
  semestre con los cuatro cambios),
  dataset (descarga simulada con 404/vacio/planas, inmutabilidad, comprobar, ventana, 12
  manifiestos corruptos), cli_data, golden_ohlc, data_manifest_history.
- Goldens: dos velas H4 del 2026-07-02 comprobadas a mano contra las M1 (Madrid 22:00Z-02:00Z:
  120 M1, o=113773 h=113857 l=113749 c=113814; servidor 09:00Z-13:00Z: 240 M1, o=114198
  h=114727 l=113953 c=114512).
- `state`, `config`, `knowledge validate` (2 parametros, 1 sin confirmar; manifiestos de datos
  validos, historial intacto): OK.
- CI GitHub Actions (ubuntu-latest, historial completo): verde, run 33917006801 (fa2eefa).
- Datasets reales: PENDIENTE DE ANOTAR (enero, julio y agosto de 2026; `data check --hashes`).

## Que deberia observar el usuario
Los tres manifiestos en `data/manifests/` con sus recuentos (dias ausentes = fines de semana,
planas descartadas, huecos mayores); la H4 del 2026-07-02 con ambos anclajes; el registro con
`anclaje_h4` UNKNOWN; `knowledge validate` en verde.

## Que casos funcionan
Todo el alcance del brief, incluida la reanudacion de descargas (cache por dia).

## Impacto sobre funcionalidades anteriores
`test_fichero_real_vacio_de_valores` pasa a `test_fichero_real_sin_valores_de_estrategia`; el
detector de literales prohibe ademas `Europe/Madrid` y `America/New_York` en `src/`;
`knowledge validate` valida manifiestos de datos; `valores.py` gana `Puntos`; ADR-0004 anota que
`huso_datos` no es parametro.

## Que casos todavia no funcionan
- No hay verificacion contra la captura del grafico del trader (F07): el anclaje real de su H4
  sigue abierto (A-9) y el CLI exige `--anclaje` explicito.
- El reloj de servidor es una aproximacion hasta F17.
- Sin ticks ni spread (F16); sin descarga desde MT5 (F17/F33).

## Limitaciones
Dukascopy es un proveedor distinto del broker (FundedNext): precios BID y minutos aislados
pueden diferir; queda declarado en el manifiesto (`proveedor`, `tipo_precio`) y H.2 asigna a
F16/F17/F33 la comparacion con la demo. El servidor exige `User-Agent` y tarda de 15 s a un
minuto por dia. La convencion `Fuente: ADR-0005` en los commits de manifiestos no la exige
ninguna guardia (solo vigila `knowledge/spec` y `knowledge/cases`).

## Riesgos
Un cambio en el decodificador o en la regla de descarte obliga a un dataset nuevo
(`decodificador_version`, `filtro_planas` en el manifiesto). Un broker con DST europeo u offset
fijo alinearia su H4 distinto que `17:00 America/New_York` en las semanas de desfase (H.2, F11/F17).

## Estado
WAITING_FOR_USER_VALIDATION
