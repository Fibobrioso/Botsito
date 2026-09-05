---
status: ACTIVE
date: 2026-09-04
phase: F15
---

# 0005 · Datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje

## Decision
1. **Fuente de M1 para F15**: el datafeed publico de Dukascopy (`BID_candles_min_1.bi5`, un
   fichero por dia y simbolo, LZMA, 24 bytes por vela, precios como enteros con escala declarada,
   volumen en float). No requiere cuenta y es reproducible por hash. El adaptador de MetaTrader 5
   (terminal + cuenta) se anade en F17/F33, donde el terminal es imprescindible de todos modos.
2. **Formato interno**: la vela vive en el dominio (`domain/velas.py`), sin `datetime`, `float`
   ni `Decimal`: `inicio` es un `MinutoUtc` (minutos enteros desde la epoca UTC; MQL5 usa
   segundos, `* 60`), los precios son `Puntos` (enteros) con la `escala` de la serie (EURUSD:
   100000) y el volumen un entero con `escala_volumen` (milesimas del float del proveedor).
   `escala` y `escala_volumen` van en `SerieVelas` y en el manifiesto, no en cada vela. El CSV
   congelado tiene columnas fijas `ts_utc,abierta,maxima,minima,cierre,volumen` (el agregado
   anade `duracion_min,n_m1,completa`), LF sin BOM, ascendente, sin duplicados, todo entero.
3. **Tres relojes explicitos** (ADR-0004): los datos van en UTC (`huso_datos: UTC` es un campo
   fijo y validado de cada manifiesto, NO un parametro: una sola puerta por valor, ADR-0002);
   `huso_operativa = Europe/Madrid` (el trader; huso de informes, journal y "dia del trader") es
   un parametro `texto` de categoria `ejecucion` CONFIRMED por este ADR (esto amplia `ejecucion`,
   definida en ADR-0004 como magic number, llenado y latencia, a los hechos del entorno del
   trader que no se le preguntan); el reloj del servidor del
   broker se representa como `17:00 America/New_York` = 00:00 de servidor (convencion de los
   brokers MT5 con GMT+2/+3 que siguen el DST de Nueva York), **aproximacion declarada** que solo
   F17 puede verificar contra el terminal (H.2). El anclaje de la vela H4 (`anclaje_h4`, tipo
   `hora`) es un parametro de `estrategia` en UNKNOWN, sin `huso`, porque la ambiguedad A-9 es
   precisamente hora y huso del grafico del trader.
4. **Regla de anclaje: particion de la recta UTC por reloj de pared**. Limite = todo instante
   UTC cuya hora de pared en el huso del anclaje cumple `minuto_del_dia ≡ anclaje (mod P)`, con
   `1440 % P == 0`. Salto de primavera: el limite inexistente se omite (vela de `P - 60`). Hora
   repetida de otono: los dos instantes son limites (vela de 60 min si un limite cae dentro,
   `P + 60` si no). Una M1 pertenece al ultimo limite menor o igual que su inicio; no se inventan
   velas; una vela esta `completa` cuando su limite de cierre ya paso. Invariantes: limites
   estrictamente crecientes, cada M1 en exactamente una vela, `M1->M15->H4 == M1->H4`. En FX los
   cambios de hora caen con el mercado cerrado: en datos reales no aparece la vela larga, sino
   un desplazamiento de una hora de los limites UTC entre semanas, solo para el anclaje cuyo
   huso cambio. El huso del grafico de TradingView solo reetiqueta; MT5 realinea las barras al
   reloj de servidor durante el cierre. La regla reproduce ambos comportamientos observables.
5. **Velas planas de volumen cero** (sin ticks: el proveedor rellena los 1440 minutos, tambien
   dentro de la sesion) se descartan al descargar y se cuentan en el manifiesto, con recuento
   aparte de las descartadas dentro de sesion (entre la primera y la ultima vela activa del dia) y de las de volumen cero no planas (conservadas,
   dato dudoso). La regla lleva version (`filtro_planas`), como el decodificador.
6. **Manifiestos de datos inmutables** en `data/manifests/<dataset_id>.yaml` (versionados; los
   datos no). `dataset_id = <nombre>-<8 hex del sha256 de los sha256 de los ficheros>`: bytes
   distintos son otro dataset, `reemplaza_a` enlaza con el anterior y el anterior no se edita.
   `hasta` es anterior al dia de descarga (el dia en curso llegaria parcial). Campos en
   `data/manifests/README.md`. La descarga guarda el fichero crudo de cada dia en
   `<datos>/raw/<SIMBOLO>/` (y recuerda los 404): una descarga interrumpida se reanuda sin
   repetir dias.

## Problema que resuelve
El plan exige velas reproducibles con el anclaje H4 y el huso del trader antes de construir casos
y motor (H.2: tres relojes, anclaje H4, manifiestos inmutables). Sin una fuente sin cuenta, sin
un formato entero y sin una regla de anclaje escrita, cada modulo posterior inventaria la suya.

## Alternativas consideradas
1. Descargar desde MetaTrader 5 (paquete `MetaTrader5` + terminal + cuenta).
2. CSV de terceros (HistData y similares) con horas en huso del proveedor.
3. Precios como `Decimal` o `float` en vez de enteros en puntos.
4. Anclaje fijo en UTC (limites cada 4 h desde 00:00 UTC).

## Por que elegimos esta opcion
Dukascopy es publico, por dia, con hash estable y precios ya enteros; el formato entero elimina
el redondeo fraccion → puntos (H.2) desde el origen; los tres relojes explicitos evitan el error de
factor "una hora" en la mitad de los dias; la regla de reloj de pared coincide con lo que el trader
ve en su grafico.

## Por que descartamos las demas
(1) No habia terminal en la maquina de desarrollo al decidirlo (nota 2026-09-05: ya hay MT5 con
la demo de FundedNext; la decision se mantiene porque ata la reproducibilidad a una cuenta) y se
anade cuando el terminal es obligatorio (F17). (2) Husos implicitos y ficheros mensuales sin hash
por dia. (3) `float` no es admisible en precios (H.2) y `Decimal` obliga a redondear al exportar a
MQL5; el entero en puntos es el tipo nativo del terminal. (4) Un anclaje UTC no reproduce las H4
del trader la mitad del ano.

## Impacto
`src/botsito/domain/velas.py` y `valores.py` (`Puntos`), `src/botsito/data/{velas,agregacion,
dukascopy,dataset}.py`, `src/botsito/cli.py` (`data`), `knowledge/spec/parametros.yaml`
(`huso_operativa`, `anclaje_h4`), `data/manifests/README.md`, hook y `knowledge validate`
(manifiestos inmutables), `.gitattributes` (`*.bi5` binario), fixtures reales en
`tests/fixtures/ohlc/`, goldens en `tests/golden/ohlc/`, detector de literales (`Europe/Madrid`
y `America/New_York` prohibidos en `src/`). Desviacion respecto a ADR-0004 y H.2 ("F15 declara
`huso_datos` y `huso_operativa`"): solo `huso_operativa` es parametro, por lo dicho en (3). F16
reutiliza el formato y el manifiesto; F29 agrega H4 desde M1 con la misma regla; F33 compara con
el terminal.

## Fecha / fase
2026-09-04 · F15

## Estado
ACTIVE
