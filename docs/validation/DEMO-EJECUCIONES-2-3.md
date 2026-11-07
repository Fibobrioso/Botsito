# DEMO-EJECUCIONES-2-3 · las ejecuciones 2 y 3 de MedirDemoFTMO, congeladas y decididas

Rama `trabajo/demo-ejecuciones-2-3`, abierta el 2026-11-06 desde `main` (a46eadd, commit de estado
sobre el merge 4fa0920 del tag `stable/F38o-activar-sesion-06-motor`). Encargo:
`docs/encargos/trabajo-demo-ejecuciones-2-3.md`. Tramo «Carril: lo de Aleks».

## Base comprobada al abrir (2026-11-06)

- `git rev-parse main origin/main`: `a46eaddc424d99c9caaf7eba5afd6af052894095` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38o-activar-sesion-06-motor^{commit}"` =
  `4fa09201a352dd46e6b4b78cbfec6ca9220ce6fa`; el tag esta en origin (`git ls-remote --tags`).
- CI de `main` sobre su HEAD: `gh run view 42300034254` → `completed` / `success`, headSha
  `a46eaddc424d99c9caaf7eba5afd6af052894095`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacio.

## 0. Fase 0 · inventario sin tocar knowledge/, docs/adr/ ni src/ (2026-11-06)

«Fila N» es la columna `fila` del CSV (la línea N+1 del fichero, con la cabecera), como en
ADR-0071. Ninguna fecha reservada: los tres CSV son de octubre y noviembre de 2026 en la prueba de
FTMO, no material del trader, y la única salida del arnés que se leyó (§0.f) es de los meses de
desarrollo (enero, abril, julio y agosto), contada sin imprimir filas.

### 0.a El lector, contra cada lectura del consultor

`uv run python scripts/leer_demo_ftmo.py data/demo_ftmo`, entera (redirigida a un fichero, sale en
cp1252 con CRLF; aquí, decodificada y con LF):

```
# Demo de FTMO: lo medido (3 fichero(s))

Solo lee: ningun valor pasa a los parametros ni cierra ninguna decision desde aqui.

- MedirDemoFTMO_20261009_153552.csv: completo (script 1.0)
- MedirDemoFTMO_20261029_194056.csv: completo (script 1.1)
- MedirDemoFTMO_20261105_203519.csv: completo (script 1.2)

## Decision a decision

| decision | que se mide | MedirDemoFTMO_20261009_153552.csv | MedirDemoFTMO_20261029_194056.csv | MedirDemoFTMO_20261105_203519.csv |
|---|---|---|---|---|
| ADR-0057 d1 | llenado de una buy stop: precio - nivel | 1.0 puntos (nivel 1.11999, llenado 1.12000) | 0.0 puntos (nivel 1.11628, llenado 1.11628) | 0.0 puntos (nivel 1.12331, llenado 1.12331) |
| FTMO-REGLAS R12 | lotes de la compra a mercado | 0.01 (la 1.0 usa el volumen minimo) | 1.00 | 1.00 |
| ADR-0057 d1 · DN-3 | compra a mercado | comision -0.03; deslizamiento 2.0 puntos | comision -2.50; deslizamiento 2.0 puntos | comision -2.50; deslizamiento 0.0 puntos |
| ADR-0057 d1 · DN-3 | cierre a mercado | comision -0.03; deslizamiento -2.0 puntos | comision -2.50; deslizamiento 0.0 puntos | comision -2.50; deslizamiento 0.0 puntos |
| ADR-0057 d2 | pendiente en el nivel exacto | sell_stop si (10009 DONE); buy_stop no (10015 INVALID_PRICE); sell_limit llenada (10009 DONE) a 1.11993; buy_limit no (10015 INVALID_PRICE) | sell_stop si (10009 DONE); buy_stop si (10009 DONE); sell_limit si (10009 DONE); buy_limit llenada (10009 DONE) a 1.11624 | sell_stop llenada (10009 DONE) a 1.12328; buy_stop llenada (10009 DONE) a 1.12329; sell_limit si (10009 DONE); buy_limit si (10009 DONE) |
| ADR-0057 d2 · d3 | sell stop por encima del bid | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | buy stop por debajo del ask | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | sell limit por debajo del bid | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | buy limit por encima del ask | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) | no (10015 INVALID_PRICE) |
| ADR-0057 d3 | modificar una sell stop al lado equivocado | si_sin_cambios (10015 INVALID_PRICE) | si_sin_cambios (10015 INVALID_PRICE) | si_sin_cambios (10015 INVALID_PRICE) |
| ADR-0057 d3 | modificar una buy limit al lado equivocado | si_sin_cambios (10015 INVALID_PRICE) | si_sin_cambios (10015 INVALID_PRICE) | si_sin_cambios (10015 INVALID_PRICE) |
| ADR-0057 d4 | cotizacion al enviar (bid/ask en cada fila del CSV) | en el CSV, fila a fila | en el CSV, fila a fila | en el CSV, fila a fila |
| ADR-0057 d5 · A-27 | stops level (puntos) | 0 | 0 | 0 |
| ADR-0057 d5 · A-27 | a la distancia del stops level | sin medir | sin medir | sin medir |
| ADR-0057 d5 · A-27 | un punto dentro del stops level | sell_stop no (10015 INVALID_PRICE); buy_stop no (10015 INVALID_PRICE); sell_limit no (10015 INVALID_PRICE); buy_limit no (10015 INVALID_PRICE) | sell_stop no (10015 INVALID_PRICE); buy_stop no (10015 INVALID_PRICE); sell_limit no (10015 INVALID_PRICE); buy_limit no (10015 INVALID_PRICE) | sell_stop no (10015 INVALID_PRICE); buy_stop no (10015 INVALID_PRICE); sell_limit no (10015 INVALID_PRICE); buy_limit no (10015 INVALID_PRICE) |
| ADR-0057 d5 | freeze level (puntos) | 0 | 0 | 0 |
| A-27 | digits | 5 | 5 | 5 |
| A-27 | point | 0.00001000 | 0.00001000 | 0.00001000 |
| A-27 | contrato | 100000.00 | 100000.00 | 100000.00 |
| A-27 | volumen minimo | 0.01 | 0.01 | 0.01 |
| A-27 | paso de volumen | 0.01 | 0.01 | 0.01 |
| A-27 | modos de llenado | FOK IOC (bits 3) | FOK IOC (bits 3) | FOK IOC (bits 3) |
| A-27 | modo de ejecucion | SYMBOL_TRADE_EXECUTION_MARKET | SYMBOL_TRADE_EXECUTION_MARKET | SYMBOL_TRADE_EXECUTION_MARKET |
| FTMO-REGLAS R11 | volumen maximo | 50.00 | 50.00 | 50.00 |
| FTMO-REGLAS R12 | swap largo | -9.4100 | -9.7400 | -10.0600 |
| FTMO-REGLAS R12 | swap corto | 0.1000 | 0.4200 | 0.4000 |
| FTMO-REGLAS R12 | modo de swap | SYMBOL_SWAP_MODE_POINTS | SYMBOL_SWAP_MODE_POINTS | SYMBOL_SWAP_MODE_POINTS |
| FTMO-REGLAS R12 | dia del triple swap | WEDNESDAY | WEDNESDAY | WEDNESDAY |

## A-28: desfase del servidor frente a GMT, por fecha

| fecha (servidor) | desfase (min) | hora del servidor | hora GMT | fichero |
|---|---|---|---|---|
| 2026.10.09 | 180 | 2026.10.09 15:35:52 | 2026.10.09 12:35:52 | MedirDemoFTMO_20261009_153552.csv |
| 2026.10.29 | 180 | 2026.10.29 19:40:56 | 2026.10.29 16:40:56 | MedirDemoFTMO_20261029_194056.csv |
| 2026.11.05 | 120 | 2026.11.05 20:35:19 | 2026.11.05 18:35:19 | MedirDemoFTMO_20261105_203519.csv |

## Paso 8: cuando comprueba MT5 el margen de una pendiente stop (ADR-0081 §4)

La regla se escribio antes de ejecutar (MARGEN-PENDIENTE.md). Lo que no prueba la causa es «no concluyente».

### MedirDemoFTMO_20261105_203519.csv

- contexto: modo de margen ACCOUNT_MARGIN_MODE_RETAIL_HEDGING; SYMBOL_MARGIN_HEDGED 200000.00; pierna mayor no; margen inicial 0.00; tope agregado de volumen 0.00; tasas de margen buy stop 0.0000;0.0000; buy 1.0000;1.0000
- M1 · rechaza al colocar una pendiente sin margen libre: no: la acepta al colocar (10009 DONE)
- M2 · una stop viva carga margen, y a que precio: no: la pendiente viva no carga margen (el libre baja 0.00; ACCOUNT_MARGIN +0.00; ACCOUNT_MARGIN_INITIAL +0.00; calculado a la orden 0.00 y al mercado 2021.94)
- M3 · suma las pendientes al colocar otra: no: no las suma al colocar (10009 DONE)
- M4 · comprueba el margen al llenar: no concluyente: no_salto (no salto en 120 s)
- peor caso M1: 988.27 USD (stop 17 puntos; 26.71 lotes a la vez; tope 1000.00 USD; comision 5.00 por lote y lado; deslizamiento 10 puntos)
- peor caso M2: 118.80 USD (stop 200 puntos; 0.54 lotes a la vez; tope 1000.00 USD; comision 5.00 por lote y lado; deslizamiento 10 puntos)
- peor caso M3: 998.92 USD (stop 14 puntos; 29.38 lotes a la vez; tope 1000.00 USD; comision 5.00 por lote y lado; deslizamiento 10 puntos)
- peor caso M4: 981.40 USD (stop 15 puntos; 28.04 lotes a la vez; tope 1000.00 USD; comision 5.00 por lote y lado; deslizamiento 10 puntos)

## Retcodes INESPERADOS: esas filas no miden lo que dicen

- ninguno

## Avisos de seguridad

- ninguno: el script no dejo nada abierto
```

| lectura del consultor | medida | veredicto |
|---|---|---|
| tres CSV; 9907 / 10167 / 18991 bytes; sha256 `86f0df8b…`, `1b82f61b…`, `59565621…` | `sha256sum`: `86f0df8b24f632102f0207b62a298a7776a164868e9a2d820ceb133c144b3c6e`, `1b82f61b8322f787132696cab51ead21943a60d2150633b6b14303b07eed823d`, `595656215c0efa679c54b661382b87b42609a35a39b1ca00b8d281b22f294924`; `ls -la`: 9907, 10167, 18991 | CORRECTA |
| fila 31 `desfase_servidor_gmt_min` 180, 180, 120 | 180, 180, 120 (líneas 32 de los tres ficheros) | CORRECTA |
| fila 32 `desfase_local_gmt_min` −300 en las tres | −300 en las tres; fila 33 `horario_verano_local_seg` 0 en las tres | CORRECTA |
| paso 6 de la 2 y la 3, 1,00 lote: −2,50 al abrir y −2,50 al cerrar | 2: filas 54-55 −2,50 y −2,50; 3: filas 54-55 −2,50 y −2,50; fila 53 `volumen_comision` 1.00 en las dos | CORRECTA |
| la 2, 2,0 puntos en contra al abrir; el resto 0 | 2: apertura pedida 1.11623, llenada 1.11625 (+2,0); cierre 0,0. 3: 0,0 y 0,0. (La 1, con 0,01 lotes: +2 y −2, ADR-0071 §5) | CORRECTA |
| paso 7: 0,0 en las dos | fila 58 `buy_stop_llenado` 0.0 en la 2 (1.11628 a 1.11628) y en la 3 (1.12331 a 1.12331) | CORRECTA |
| paso 4 de la 2: la buy limit se llenó al instante y las otras tres quedaron vivas | buy limit llenada a 1.11624 (fila 42). Sell stop y sell limit, vivas y borradas con 10009. **La buy stop (fila 40) estaba viva al leerla, pero su borrado devolvió 10013** («borrada con retcode 10013»): el script borra justo después de comprobar que vive (`MedirDemoFTMO.mq5:414-419`), con el ask en el nivel (1.11627); lo más probable es que saltara entre la lectura y el borrado, y el CSV no lo distingue | MATIZ: la buy stop «quedó viva» solo en el instante de la lectura |
| paso 4 de la 3: las dos stop llenadas al instante y las dos limit vivas | sell stop llenada a 1.12328 y buy stop a 1.12329 (filas 39-40); sell limit y buy limit vivas y borradas con 10009 (filas 41-42) | CORRECTA |
| paso 8 de la 3: `p8_tasa_buy_stop` 0;0 | fila 65 `0.0000;0.0000` (inicial;mantenimiento); la de una compra, fila 66, `1.0000;1.0000` | CORRECTA |
| `m1_colocar` DONE con 26,71 lotes, margen al ask por encima del margen libre | fila 74: margen al ask 100010.25, libre 99989.55; fila 76: 10009 DONE, colocada | CORRECTA |
| m2: el margen y el margen libre no cambian | filas 81-86: ACCOUNT_MARGIN 0,00 → 0,00; libre 99989.55 → 99989.55; INITIAL 0,00 → 0,00 | CORRECTA |
| m3: las dos colocadas | filas 94 y 97: 10009 DONE las dos | CORRECTA |
| `m4_resultado` no_salto | fila 111: `no_salto`, «no salto en 120 s» | CORRECTA |

Lo que el lector dice además y el consultor no leyó: retcodes INESPERADOS «ninguno» y avisos de
seguridad «ninguno» en los tres; la ficha (filas 4-15 y 24-25) es la misma en la 1, la 2 y la 3
salvo los swaps (§0.c). Y la fórmula del margen de ADR-0081 §4 casa con las dos notas del paso 6:
1,00 × 100.000 × 1,11623 / 30 = 3720,77 (la 2, fila 53) y 1,12329 → 3744,30 (la 3, fila 53).

### 0.b Los originales de `MQL5\Files` frente a las copias

La guardia dejó leer la carpeta de datos del terminal
(`C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files`),
así que no hizo falta el comando para Aleks. Medido con un guion del scratchpad que lee los bytes
(`len`, `hashlib.sha256`, `count(b"\r")`, `count(b"\n")`, `count(b"\r\n")`, BOM):

| fichero | lado | bytes | sha256 | CR | LF | CRLF | BOM |
|---|---|---|---|---|---|---|---|
| `MedirDemoFTMO_20261009_153552.csv` | copia y original | 9907 | `86f0df8b…3c6e` | 60 | 60 | 60 | no |
| `MedirDemoFTMO_20261029_194056.csv` | copia y original | 10167 | `1b82f61b…823d` | 61 | 61 | 61 | no |
| `MedirDemoFTMO_20261105_203519.csv` | copia y original | 18991 | `59565621…4924` | 116 | 116 | 116 | no |

**Los tres originales coinciden con sus copias byte a byte, y LOS TRES son CRLF en todas sus
líneas, también el de la ejecución 1.** Es la cabecera más 59, 60 y 115 filas.

**La deuda del CRLF se explica, y lo que estaba mal era la medida.** EA-CONEXION.md §0.c (y antes
DEMO-EJECUCION-1.md:49) contaron los retornos de carro con `grep -c $'\r'` en Git Bash, y el `grep`
de Git para Windows QUITA el CR del final de cada línea antes de comparar, salvo con `-U`
(`--binary`). Medido hoy sobre el mismo fichero:

```
$ grep -c -P '\r' data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv
0
$ grep -U -c -P '\r' data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv
60
```

El sha256 del CSV de la 1 es el congelado el 2026-10-09 (`86f0df8b…3c6e`), así que el fichero no
cambió: **siempre fue CRLF**, que es justo lo que EA-CONEXION.md §0.c midió que escribe el modo
texto ANSI de MT5. No hay contradicción ni residual. La consecuencia que sí queda: **el manifiesto
inmutable de la ejecución 1 declara `fin_de_linea: LF` y es falso**
(`data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml:11`). No se toca (D1); ningún código
ni test lee ese campo (`grep -rn fin_de_linea src tests scripts`: 0). Lo corrige ADR-0090 por
escrito y los dos informes que lo afirmaron reciben su recuadro (decisión 0).

### 0.c La tabla medida → decisión de las ejecuciones 2 y 3

| fila(s) | a qué responde | qué dice hoy el repo | la 2 (2026-10-29, 1.1) | la 3 (2026-11-05, 1.2) | decisión |
|---|---|---|---|---|---|
| 31 | A-28, desfase servidor − GMT | `broker_offset_base`, `broker_dst` UNKNOWN; A-28 ABIERTA (`parametros.yaml:140-165`, `ambiguedades.yaml:700-740`) | 180 | 120 | D3: con la 1 (180 el 9-oct), solo base 120 + `us` casa (§0.c.1) |
| 32-33 | contexto: el reloj del ordenador | — | −300, DST 0 | −300, DST 0 | acota la medida (§0.c.1) |
| 53-55 | R12, tarifa de la comisión | `firma_comision_usd_por_lote` 5 por lado, «supuesto CONSERVADOR … hasta medirla con 1,00 lote en la ejecucion 2» (perfil :382-396; ADR-0071 §3) | 1,00 lote: −2,50 y −2,50 | 1,00 lote: −2,50 y −2,50 | D6: 2,50 por lote y lado |
| 54-55 | DN-3, deslizamiento a mercado | `deslizamiento_fijo_puntos` 0 (`knowledge/simulador/llenado.yaml`) | +2,0 al abrir, 0,0 al cerrar | 0,0 y 0,0 | D10: no cambia; se registra |
| 57-58 | ADR-0057 §1, llenado de la buy stop | coincide (ADR-0071 §4, +1 en la 1) | 0,0 | 0,0 | sin cambio: nunca mejor que el nivel |
| 39-42 | ADR-0057 §2, el nivel exacto | PROVISIONAL (ADR-0071 §4) | sell stop viva, buy stop viva al leer y borrado 10013, sell limit viva, buy limit llenada | sell stop y buy stop llenadas, sell limit y buy limit vivas | D8: sigue PROVISIONAL; tres patrones distintos |
| 34-37, 43-46, 49, 51 | ADR-0057 §3, lado equivocado | MEDIDO (ADR-0071 §4) | las ocho 10015; las dos modificaciones 10015 sin cambios | igual | sin cambio: lo repiten |
| 4-15 | A-27 y la ficha | los cinco de A-27 CONFIRMED (ADR-0071 §1); stops level 0 y volumen máximo 50 (perfil) | igual que la 1 | igual que la 1 | D9: coincide (tabla de §0.c.2) |
| 16-19 | R12, swaps | `firma_swap_largo_puntos` −9,49 y `firma_swap_corto_puntos` 0,36, CONFIRMED con fuente ADR-0050 (la web del 2026-09-25) | −9,74 y 0,42 | −10,06 y 0,40 | **difieren del perfil** (como la 1: −9,41 y 0,10); ver decisión 1 |
| 24-25 | apalancamiento y modo de margen | `firma_apalancamiento` 30; hedging (ADR-0071 §7) | 30; HEDGING | 30; HEDGING | coincide |
| 60-73 | ADR-0081 §4, contexto del paso 8 | «una pendiente stop RESERVA margen mientras vive» y se comprueba al colocar (ADR-0081 §4; `broker.py:521-525`, `:1014-1030`) | — | tasa de margen de la buy stop 0;0; margen inicial 0,00; SYMBOL_MARGIN_HEDGED 200000 | D7 |
| 74-111 | ADR-0081 §4, M1-M4 (regla de MARGEN-PENDIENTE.md §0.d) | supuesto conservador del bróker simulado | — | M1 no, M2 no (Δ 0,00 < 0,10 × 2021,94), M3 no, M4 no concluyente (`no_salto`) | D7: ADR-0090 ENMIENDA ADR-0081 §4 |

#### 0.c.1 A-28: la regla de lectura y el reloj del ordenador

La regla de D3, aplicada con `zoneinfo` (guion del scratchpad `derivacion_anclaje.py`; Europa
cambió de hora el 2026-10-25 y EE. UU. el 2026-11-01, comprobado con la misma librería):

```
dias: 730; la medianoche del servidor NO cae a las 17:00 de Nueva York: 0
  eu       2026.10.09: 180 (medido 180); 2026.10.29: 120 (medido 180); 2026.11.05: 120 (medido 120) -> no casa
  us       2026.10.09: 180 (medido 180); 2026.10.29: 180 (medido 180); 2026.11.05: 120 (medido 120) -> CASA
  ninguno  2026.10.09: 120 (medido 180); 2026.10.29: 120 (medido 180); 2026.11.05: 120 (medido 120) -> no casa
  casa: base 120, us
```

Probadas las bases 60, 120 y 180 con los tres calendarios, **solo «base 120, us» casa con las tres
medidas**: una sola opción, sin PARADA.

**Cuánto depende del reloj del ordenador.** El script calcula `desfase = TimeTradeServer() −
TimeGMT()` en minutos enteros (`MedirDemoFTMO.mq5:389-395`), y `TimeGMT()` sale del reloj y del huso
del ordenador. Dos cosas lo acotan:
- **La fila 32** (`desfase_local_gmt_min` = −`TimeGMTOffset()`/60) es −300 en las tres, con
  horario de verano 0 (fila 33): el ordenador estaba en el huso de Lima, sin cambio de hora, las tres
  veces. Un huso mal puesto o un cambio de hora del propio ordenador movería `TimeGMT()` en horas
  enteras y se vería ahí; no lo hay. Lo que la fila 32 NO acota es que el reloj esté en hora.
- **La fila 27** (`time_current`, la hora del último tick, que manda el servidor y no depende del
  ordenador) frente a la fila 29 (`time_gmt`): 15:35:51 vs 12:35:52, 19:40:55 vs 16:40:56 y
  20:35:19 vs 18:35:19. La diferencia es 180, 180 y 120 minutos menos 0 o 1 segundo: el reloj del
  ordenador iba en hora con el del servidor a menos de un par de segundos las tres veces. Para
  confundir 120 con 180 haría falta un error de 30 minutos o más.

**Observación concordante:** el journal del EA del 2026-10-21
(`docs/validation/anexos/EA-CONEXION/demo-20261021-cierre/journal_20261021.jsonl`, línea 1 y
siguientes) da `desfase_s` 10800 (180 min). Ese día los dos calendarios dan 180: concuerda, no
discrimina.

#### 0.c.2 La ficha (D9)

| dato | registro / perfil (CONFIRMED) | la 1 | la 2 | la 3 |
|---|---|---|---|---|
| `instrumento_digitos` (fila 6) | 5 | 5 | 5 | 5 |
| point (fila 7) | 0,00001 | 0.00001000 | 0.00001000 | 0.00001000 |
| `instrumento_contrato` (fila 8) | 100000 | 100000.00 | 100000.00 | 100000.00 |
| `instrumento_lote_minimo` (fila 9) | 0.01 | 0.01 | 0.01 | 0.01 |
| `instrumento_lote_paso` (fila 11) | 0.01 | 0.01 | 0.01 | 0.01 |
| `instrumento_stops_level` / `firma_stops_level_puntos` (fila 4) | 0 / 0 | 0 | 0 | 0 |
| freeze level (fila 5) | 0 (ADR-0071 §2, sin parámetro) | 0 | 0 | 0 |
| `firma_volumen_max_lotes` (fila 10) | 50 | 50.00 | 50.00 | 50.00 |
| volumen límite (fila 12) | 0 (ADR-0071 §2, sin parámetro) | 0.00 | 0.00 | 0.00 |
| modos de llenado, ejecución, caducidad (13-15) | FOK IOC, MARKET, 15 (ADR-0071 §7) | igual | igual | igual |
| `firma_apalancamiento` (fila 24) | 30 | 30 | 30 | 30 |
| modo de margen (fila 25) | hedging (ADR-0071 §7, sin parámetro) | HEDGING | HEDGING | HEDGING |
| modo de swap y triple (18-19) | puntos, miércoles (ADR-0050) | POINTS, WEDNESDAY | igual | igual |
| `firma_swap_largo_puntos` (fila 16) | −9,49 | −9,41 | −9,74 | −10,06 |
| `firma_swap_corto_puntos` (fila 17) | 0,36 | 0,10 | 0,42 | 0,40 |

Todo coincide salvo los dos swaps, que no coinciden en ninguna de las tres (decisión 1).


#### 0.c.3 La hora de cada ejecución (D11)

Con `zoneinfo` (guion `derivacion_anclaje.py`):

```
Hora de la ejecucion 3 (GMT 2026-11-05 18:35:19):
  servidor (120+us): 20:35
  UTC: 18:35 UTC
  Madrid: 19:35 CET
  Lima: 13:35 -05
  Nueva York: 13:35 EST
  Londres: 18:35 GMT
  ejecucion 1: Madrid 14:35 CEST, Lima 07:35, NY 08:35 EDT
  ejecucion 2: Madrid 17:40 CET, Lima 11:40, NY 12:40 EDT
```

La 3 corrió a las 20:35 del servidor = 18:35 UTC = 19:35 de España = 13:35 de Lima: fuera de la franja de 9 a 18 de España del runbook (`DEMO-FTMO.md:66`), con Nueva York abierto (13:35 EST) y Londres ya cerrado (18:35 GMT). Puede afectar al spread, al deslizamiento y al llenado de los pasos 6 y 7; no afecta al desfase, a la comisión ni a la ficha. La 1 (14:35 de España) y la 2 (17:40 de España) cayeron dentro.

### 0.d Quién lee los tres parámetros, y por dónde llega la comisión

`grep -rn "broker_offset_base\|broker_dst\|firma_comision_usd_por_lote" src tests scripts`
(en `.py`):

- **`broker_offset_base` y `broker_dst`: ningún lector** en `src/`, `tests/` ni `scripts/`. Solo los
  nombran la spec y su documento generado (`parametros.yaml:136-165`, `docs/spec/parametros.md`) y
  A-28. Decidirlos no cambia ninguna corrida.
- **`firma_comision_usd_por_lote`:** un lector, `engine/simulacion.py:140` (`reglas_broker_de`, a
  `ReglasBroker.comision_por_lote`, `broker.py:129-130`), y un test, `tests/unit/test_perfil_cuenta.py:214-215`.

El camino de la comisión, verificado (el auditor del consultor apuntaba a `cableado.py`,
`cuenta.py` y `primitivas_broker.py`: correcto, y falta `simulacion.py`):

| a dónde llega | fichero:línea |
|---|---|
| se lee del perfil | `engine/simulacion.py:140-141` |
| al llenar, se carga en la cuenta viva (siempre) | `engine/cableado.py:427-428` → `engine/cuenta.py:454-457` (`cargar` resta del saldo y observa) |
| al cerrar, el segundo lado (si `comision_por_lado`) | `engine/cableado.py:433-434` |
| en la operación que se informa (los dos cargos) | `engine/broker.py:1105-1110` |
| al saldo y a la equidad | `engine/cuenta.py:456`, `:516-522` |
| a los límites de la firma (pérdida del día y total, sobre la vigilada) | `engine/cuenta.py:471-484` (`_observar` → `infracciones`), `:495-514` (`acumuladores`), con `infracciones` en `:356` |
| al tope del trader (saldo o equidad, con el saldo al corte) | `engine/tope_trader.py:250-278`, que recibe el saldo de la cuenta |
| al margen libre | `engine/broker.py:1032-1037` (`self.saldo()` es el saldo de la cuenta, ADR-0081 §4) |
| al lote | por el saldo: `engine/primitivas_broker.py:604-605` (el riesgo sobre el saldo); por el margen libre: `:543` (`margen_libre() × lote_margen_libre_fraccion`) |

La comisión NO entra en ningún cálculo del lote como coste: solo baja el saldo, y por él el lote
siguiente, el margen libre y los frenos.

### 0.e Qué tests rompen con la comisión a 2,50 (comparar-con-main)

Dos clones desechables (`git worktree add --detach C:/cm/m main` y `C:/cm/r HEAD`, con su
`config/settings.local.toml` apuntando al `data/` real, que los tests solo leen). En `C:/cm/r`, un
solo cambio: `valor: "5"` → `valor: "2.50"` en `knowledge/cuentas/ftmo-2step-swing-100k.yaml:394`.
La guardia niega `pytest tests` («tests es un directorio: la guardia no sabe que ficheros
ejecutara»), así que se pasaron los ficheros nombrados: los 165 `test_*.py` de `git ls-files`
menos los que no leen el perfil ni el motor (los de la guardia, skills, hooks, revisor, rutas de
Windows, memoria, sello, push, árbol, transcripción y `tests/integration`). Llegó al 100 %; tres
fallos:

| test | por qué | qué es |
|---|---|---|
| `tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths` | «rutas ignoradas no previstas: ['config/settings.local.toml']» | del clon (el repo real no tiene ese fichero): no es de la comisión |
| `tests/unit/test_perfil_cuenta.py::test_la_comision_por_lado_esta_medida_y_su_importe_sigue_conservador` | `assert Decimal('2.50') == 5` | fija el importe: se cambia (D6) |
| `tests/regression/test_cuenta_7_de_agosto.py::test_la_cuenta_del_7_de_agosto_marca_la_perdida_diaria_en_el_pico` | `assert EN_CURSO is SUSPENDIDA` | **cambia el estado de la cuenta**: decisión 3 |

**La cuenta del 7 de agosto, medida con los dos perfiles** (guion `cuenta_7_agosto.py` del
scratchpad, que repite el test con el perfil del clon; caso dev de construcción, agosto):

| | comisión por lote y lado | comisión de las cuatro operaciones (83,33 + 100 + 22,72 + 13,15 lotes) | estado | peor equidad del día frente al límite (95.000) |
|---|---|---|---|---|
| `main` | 5 | 833,30 + 1.000,00 + 227,20 + 131,50 = 2.192,00 | SUSPENDIDA, «perdida diaria … [marca de t4]», 12:30:01.312 UTC | 94.485,53: **−514,47** |
| rama | 2,50 | 1.096,00 | EN_CURSO | 95.515,78: **+515,78** |

La diferencia, 1.096 USD de comisión, es justo lo que separa la infracción del aprobado ese día. El
test no fija un importe ni un saldo: fija que la cuenta SE SUSPENDE y en qué tick, que es la
regresión del corte (`trabajo/corregir-evaluar-fase`). Con 2,50 el corte no llega a ocurrir y el
test pierde lo que prueba. **D6 manda PARADA si rompe cualquier otra cosa: PARADA solo para este
test, y con él el punto 4 de la fase 1 (la comisión en el perfil), que no puede commitearse con
`make check` en rojo.** Los puntos 1, 2, 3 y 5 no dependen de ello y siguen.

Ningún otro test del motor, del cableado, del arnés, del margen ni del tope rompe con 2,50: ninguno
fija la comisión del perfil real.

### 0.f Rechazos por `margen_libre` en el arnés sobre construcción, sin ejecutar nada

La salida más reciente del arnés sobre construcción es la de `trabajo/respaldo-m1`
(`docs/validation/anexos/RESPALDO-M1/`, commit e808391 del 2026-10-29), posterior a la de
RECORRIDA-CONSTRUCCION.md. Recuento con `grep -c "margen_libre"` sobre las dos corridas de cada
una: **0** en `RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt`, `RESPALDO-M1/cuenta-arrastrada.txt`,
`RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt` y
`RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`. Su «### Rechazos por motivo» (diaria de
RESPALDO-M1, `:3399-3403`) solo trae `precio_invalido | colocar` (8, 10, 9 y 10 por mes); ningún
rechazo al llenar. RECORRIDA-CONSTRUCCION.md §2.7 (`:832-834`) dice lo mismo de las suyas.
**Ningún rechazo por margen libre: no hay PARADA por D7(b).**

**¿Puede la reserva cambiar el lote con una sola orden viva a la vez?** No, por el código:
- al COLOCAR, el bot dimensiona con `margen_libre()` (`primitivas_broker.py:543`), que resta la
  reserva de las OTRAS stop vivas (`broker.py:1023-1027`); con ninguna otra viva, la reserva no
  existe todavía y el lote es el mismo con y sin ella. La reubicación cancela la vieja ANTES de
  dimensionar la nueva (ADR-0081 §4);
- al LLENAR, el bróker devuelve la reserva de la propia orden como `libre_extra`
  (`broker.py:851-862`): margen al precio del llenado ≤ (libre − reserva propia) + reserva propia,
  que es la misma comprobación que sin reserva. Sin efecto en el resultado.
- La reserva solo muerde con DOS O MÁS stop vivas a la vez. Medido sobre la sección «### Ordenes» de
  las dos corridas de RESPALDO-M1 (guion `solapes.py` del scratchpad, solo recuentos): de 1329
  órdenes de la diaria y 215 de la arrastrada, **0 se colocaron con otra orden viva** (colocada antes
  y con su resultado después). Y la orden que se coloca en el mismo instante en que se cancela la
  anterior lleva el margen libre entero (100000.00 en la segunda orden del primer día de enero,
  `diaria…:2065`): la reserva vieja ya no contaba.

### 0.g Las frases de los documentos vivos que quedan falsas

Por A-28 (búsqueda de «A-28», «broker_offset_base», «broker_dst», «ejecución 2», «ejecuciones 2 y
3» y «la rama que congele» en `knowledge/`, `docs/runbooks`, `docs/plan`, `docs/spec`,
`PROJECT_STATE.md`, los README y `tools/`; sin `knowledge/evidence|feedback|corpus`):

| sitio | frase | qué pasa |
|---|---|---|
| `parametros.yaml:52-60` (cabecera) | «los dos del reloj del servidor pasan a UNKNOWN bajo A-28» … «los dos del reloj siguen UNKNOWN bajo A-28» | se añade: desde ADR-0090 son CONFIRMED (120, `us`) y A-28 está DECIDIDA |
| `parametros.yaml:136-150` (`broker_offset_base`) | «se mide en su demo (A-28)»; `estado: UNKNOWN`; el comentario «F17 lo mide contra el terminal de la demo» | valor 120, CONFIRMED, fuente ADR-0090; el comentario dice que lo midió MedirDemoFTMO y que F17 y F33 lo vuelven a leer |
| `parametros.yaml:152-165` (`broker_dst`) | «se mide en su demo (A-28) … por eso A-28 no se cierra antes del cambio de octubre»; «si decide si anclaje_h4 … cae de verdad en la medianoche del servidor»; UNKNOWN | valor `us`, CONFIRMED; la transición la observó la 2 (29-oct); lo de anclaje_h4 pasa a derivación (D4) |
| `parametros.yaml:289-290` (`huso_grafico`) | «se mide en la demo de FTMO (A-28)» | «se midió en la demo de FTMO (ADR-0090)» |
| `parametros.yaml:306-311` (`anclaje_h4`) | «En FTMO esta SIN VERIFICAR: se contrasta con su rejilla H4 real al medir A-28» | D4: la derivación con 120 y `us`, y la medida real en R6a.1 (iTime en el journal), antes de R6a.7 y F33 |
| `parametros.yaml:1626-1629` (`reloj_dia_riesgo`) | «se comprueba en el panel de la prueba gratuita de FTMO dentro de A-28» | D5: apunta a la línea propia para Aleks |
| `parametros.yaml:1699-1700` (`cuenta_pruebas`) | «donde se miden A-27 y A-28» | «donde se midieron A-27 y A-28 (ADR-0071, ADR-0090)» |
| `ambiguedades.yaml:400` (A-19, DECIDIDA) | «Lo que SI queda por medir -el reloj del servidor…- es A-28» | se añade que A-28 quedó DECIDIDA por ADR-0090 |
| `ambiguedades.yaml:700-740` (A-28) | ABIERTA; «NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE»; la VERIFICACION EXPLICITA | DECIDIDA, `decision: ADR-0090`, `decidida_el: '2026-11-06'`; nota de que la verificación del panel pasa a su línea (D5) |
| `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:8-10` | «PROVISIONAL: es lo que A-28 (broker_dst) mide observando una transicion, y sigue abierta; se revisa con ella» | revisado: A-28 DECIDIDA con `us` (ADR-0090), el huso America/New_York queda medido; ningún cierre cambia |
| `docs/runbooks/DEMO-FTMO.md:107`, `:143`, `:151`, `:205` | la 2 «dice qué calendario»; el panel; la hora del cierre «justo lo que mide A-28» | punto 5 de la fase 1 (D11), con «Cuándo: tres veces» |
| `docs/spec/parametros.md`, `docs/spec/ambiguedades.md` | generados | `spec docs --escribir` |
| `PROJECT_STATE.md:74` (Known Ambiguities) | la fila de A-28 | sale en la rama (D3) |
| `PROJECT_STATE.md:42`, `:65`, `:66` | A, heredados 10 y 27 | líneas del cierre (§0.h) |
| `docs/plan/HOJA-DE-RUTA.md` A.1 (`:494-508`), R6a.1, R6a.6, R6a.7, F:F17, «Fechas fijas» | | líneas del cierre (§0.h) |
| `tests/unit/test_kit.py:417-423` | «el reloj del servidor sigue sin valor» y `"A-28": "ABIERTA"` | D3: A-28 entre las DECIDIDAS |

Por la comisión (búsqueda de «comision», «commission», «5 por lado», «5 USD», «USD/LOT»):

| sitio | frase | qué pasa |
|---|---|---|
| perfil `:382-396` (`firma_comision_usd_por_lote`) | «este perfil carga 5 por lado … queda como supuesto CONSERVADOR … hasta medirla con 1,00 lote en la ejecucion 2»; valor «5»; fuente ADR-0071 | valor «2.50», fuente ADR-0090, descripción con las filas 54-55 de la 2 y la 3 y la lectura del «commission: 5» |
| perfil `:398-410` (`firma_comision_por_lado`) | «La tarifa por lote NO la fija esa medida (firma_comision_usd_por_lote)» | sigue siendo verdad de la 1; se añade que la fijó ADR-0090 |
| `docs/runbooks/DEMO-FTMO.md:30` | el paso 8 «contando la comisión (5 USD por lote y lado)» | verdad del script 1.2 (`p8_comision_lado_lote` 5.00, fila 73): se queda y se dice que es el supuesto del tope de la 3 |
| `knowledge/spec/parametros.yaml:2086-2090` (`firma_apalancamiento`) | «La ejecucion 2 … comprobara la formula con MargenAlcanza» | ya comprobada: 3720,77 (la 2) y 3744,30 (la 3) casan con la fórmula |
| ADR-0071 §3 | «queda como supuesto CONSERVADOR … La tarifa se mide en la ejecución 2» | recuadro (D6) |
| `scripts/README.md:67` (`viabilidad_comision.py`, comisiones de ida y vuelta 3, 5 y 10) | | no es falsa: el 5 de ida y vuelta es justo la tarifa medida |
| `tests/unit/test_perfil_cuenta.py:214-215` | `== 5` | §0.e |

Y la del paso 8: ADR-0081 §4 («Una pendiente stop RESERVA margen mientras vive»; «cuándo lo
comprueba MT5 de verdad se mide en la demo (ejecución 3…)»), los comentarios de `broker.py:521-523`
y `:1012-1016` (código: no se tocan, D7(b); la línea de Technical Debt los nombra) y
`parametros.yaml:2084-2085` («Lo comprueba el BROKER SIMULADO desde ADR-0081: rechazo `margen_libre`
al colocar y al llenar»: verdad del simulador, se queda).

### 0.h Las líneas del cierre, preparadas sobre una copia (sin aplicar en la rama)

Las escribe el consultor en su orden de cierre; aquí van preparadas y probadas sobre una copia de
`PROJECT_STATE.md` y `docs/plan/HOJA-DE-RUTA.md` en un clon desechable (§0.h.1).

**Next Action**

- **A sale** a HISTORIA (HECHA: RITUAL.md punto 3), con su lo «Opcional» mudado a la entrada nueva de
  abajo para que no se pierda.
- **M se queda** igual: ninguna ejecución la mide (D12).
- **Entra una línea para Aleks** (D5), con la letra que libera A:
  > A. Para Aleks, en el panel de la prueba gratuita de FTMO: a qué hora se recalcula el límite de
  > pérdida diaria, con fecha y hora (la «verificación explícita» que A-28 llevaba dentro, ADR-0090
  > §1). Medianoche de España: `reloj_dia_riesgo` no cambia. Medianoche del servidor: se reabre A-19
  > y `reloj_dia_riesgo` vuelve a DEFAULT_AMBIGUOUS (ADR-0027). Opcional: el calendario de las
  > noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en
  > corpus/noticias/ como CSV fecha_utc,hora_utc,divisa,evento; stops_cortos.py --noticias <csv>
  > --ventana-min 2 da la medida (MARGEN-LOTE.md §2.b).
- **F**: «Siguiente: la rama corta de la demo (A), H, R…» → «Siguiente: H (fase 0: …), R y la
  re-corrida que cuenta (ADR-0070 §3); …» (sin la demo, que es esta rama).

**Pendientes heredados**

- 10 → «De la demo de FTMO queda el grabador de spread y ticks, F17.» (A-28 sale: DECIDIDA por
  ADR-0090; NA:A sale de la línea).
- 27 → «Para Aleks con FTMO: la «maximum capital allocation rule» y el asterisco de «USD/LOT*»
  (hoja de ruta, A.2); la medida de ADR-0090 §3 casa con leer «commission: 5» como ida y vuelta.»
  («A-28 va con A» sale).

**Technical Debt**

- **Sale** «El modo texto ANSI de MT5 (build 6230) escribe CRLF y el CSV de la ejecución 1 … tiene
  LF, sin explicación …», por (a) de `docs/state/README.md`: medido en esta rama, el CSV siempre fue
  CRLF y el LF era el `grep` de Git para Windows (ADR-0090, «La medida»). En HISTORIA, el registro
  del cierre lo anota.
- **Entra** (D7(c)): «El bróker simulado reserva margen por cada pendiente stop viva y comprueba el
  margen al colocarla (ADR-0081 §4); la prueba de FTMO no (tasa de margen de la buy stop 0, M1-M3
  «no», ADR-0090 §4). Sin efecto medido en construcción (DEMO-EJECUCIONES-2-3.md §0.f). Se decide
  antes de R6a.6, que no la porta al EA sin esa decisión.»
- **Entra** (decisión 0): «El manifiesto inmutable de la ejecución 1 de la demo declara
  `fin_de_linea: LF` y el CSV es CRLF (ADR-0090): ningún código lo lee; un manifiesto nuevo de esa
  ejecución no tiene sentido, así que la verdad vive en ADR-0090.» (O no entra, si el consultor lo
  da por pagado con el ADR y los recuadros.)

**Known Ambiguities**: la fila de A-28 sale EN LA RAMA (D3), no en el cierre.

**Hoja de ruta**

- **A.1** → Estado: «HECHA (`trabajo/demo-ejecuciones-2-3`, ADR-0090; DEMO-EJECUCIONES-2-3.md): los
  tres CSV congelados, A-28 DECIDIDA, la comisión a 2,50 por lado y ADR-0081 §4 enmendado.» Sus
  Refs pierden NA:M y HER:10 (una HECHA no nombra letras vivas): `ID:A-28 · ID:ADR-0090 · F:F17`.
- **Entra A.5 · Lo que queda de la demo de FTMO** (para que M y el heredado 10 tengan entrada viva):
  > - **Refs:** NA:A · NA:M · HER:10 · F:F17
  > - **Qué es:** el panel del límite diario (NA:A); el BE de una venta que salta por el ASK (NA:M,
  >   ADR-0065 §6); y el grabador de spread y ticks de F17 (heredado 10), que también mide el
  >   deslizamiento (ADR-0090 §7).
  > - **Depende de:** una prueba gratuita de FTMO viva (la del 2026-10-29, si dura 14 días como la del 2026-10-08, vence hacia el 12-nov; sin comprobar).
  > - **Quién:** Aleks mira el panel; la sesión, con el encargo del consultor, lo demás.
  > - **Hecho cuando:** el panel declarado, M medida y el grabador hecho.
- **R6a.1**: sigue HECHA; la medida de la rejilla H4 real va en una entrada nueva (decisión 2, por
  (a)):
  > ### R6a.8 · La rejilla H4 real en el journal
  > - **Refs:** ID:ADR-0090 · ID:ADR-0027 · F:F33
  > - **Qué es:** el EA de R6a.1 escribe en el journal de la demo la hora de apertura de las velas
  >   H4 (`iTime`), para medir `anclaje_h4` contra la rejilla real del servidor (ADR-0027 §4,
  >   recuadro de ADR-0090 §2).
  > - **Depende de:** R6a.1.
  > - **Quién:** la sesión, con el encargo del consultor; Aleks pone el EA en la demo.
  > - **Hecho cuando:** el journal trae las aperturas H4 de una semana con un cambio de día y
  >   coinciden con 17:00 de Nueva York, o se abre una ambigüedad.
- **R6a.6** → Depende de: «… el script 1.2 de MedirDemoFTMO (HECHO, trabajo/margen-pendiente), la
  ejecución 3 de la demo (HECHA, ADR-0090 §4: M1-M3 no, M4 sin medir) y la decisión sobre la reserva
  de margen del bróker simulado (Technical Debt).»
- **R6a.7** → Qué es, al final: «… y la tasa de margen de las pendientes stop
  (`SymbolInfoMarginRate`), que en la prueba es 0 y la cuenta Swing no garantiza (ADR-0090 §4 (d)).
  El desfase del reloj se compara con 120 y `us` (ADR-0090 §1).» Depende de: «R6a.1 a R6a.6 y
  R6a.8».
- **F:F17** → «PARCIAL: el script de medición (tres ejecuciones, ADR-0071 y ADR-0090), no el
  grabador» | `DEMO-EJECUCION-1.md`, `DEMO-EJECUCIONES-2-3.md`.
- **«Fechas fijas»**: sale «La ejecución 2, hecha el 2026-10-29 …» (ya no es una fecha por venir, y
  nombra NA:A); entra «La prueba gratuita de FTMO del 2026-10-29 vence (si dura 14 días, como la
  del 2026-10-08) hacia el 12 de noviembre de 2026: el panel (NA:A) va antes.» (sin comprobar la
  duración) La de la semana del 26 al 30 de octubre se queda o sale a juicio
  del consultor (ya pasó).

#### 0.h.1 La prueba sobre una copia, y la previsión de PROJECT_STATE

En un clon desechable de la rama (`git worktree add --detach C:/cm/h HEAD`, con un borrador de
ADR-0090 copiado dentro para que existan sus referencias), aplicadas las líneas de arriba a
`PROJECT_STATE.md` y a `docs/plan/HOJA-DE-RUTA.md` (sin la línea de deuda de la decisión 0, que
depende de la respuesta):

- primera pasada: `test_hoja_de_ruta.py::test_b_cada_referencia_existe_y_ninguna_hecha_sigue_viva`
  falló con «A.1 …: NA:M esta HECHA y la letra sigue viva»: el «Qué es» de A.1 también nombra
  «(NA:M)». **Línea añadida:** en A.1, «el BE de una venta que salta por el ASK (NA:M); y, …» pierde
  el «(NA:M)»;
- segunda pasada: `tests/unit/test_hoja_de_ruta.py` y `tests/unit/test_project_state.py`, **todos
  verdes**;
- **`wc -c PROJECT_STATE.md` = 22.582 bytes**, por debajo de 23.000 (el tope del test es 25.000,
  `tests/unit/test_project_state.py:21`; los 23.000 son el margen del encargo). La copia parte del
  `PROJECT_STATE.md` de la rama al abrir (22.729 bytes con la línea EN CURSO); el `Current Feature`
  del cierre lo escribe el consultor.

### El encargo frente al repo (auditor-encargo, 2026-11-06)

46 afirmaciones: 33 correctas, 0 incorrectas, 13 con matiz; 9 herencias que el encargo no recoge.
Lo que importa, con lo que hago (el informe entero del auditor está en la conversación de la sesión;
aquí, cada matiz con su evidencia y su efecto):

| # | matiz o herencia | evidencia | qué hago |
|---|---|---|---|
| 8, 10 | «fila 31/32» son la columna `fila`; la fila 32 fija el huso del PC, no la deriva de su reloj | `.mq5:395-396` | §0.c.1: la deriva la acota la fila 27 (hora del tick del servidor), a ±1 s |
| 17 | las tres muestras de deslizamiento de la 1 están en ADR-0071 §5, no en §4 | `0071:128-129` | ADR-0090 cita §5 |
| 23 | el 5,00 del punto 4 de MARGEN-PENDIENTE es la constante del tope del script 1.2 (`P8_COMISION_LADO`, `.mq5:805`; fila 73 de la 3) | `MARGEN-PENDIENTE.md:500` | se cumple así: el peor caso de la 3 se calculó con 5,00, más caro que los 2,50 medidos, así que sus topes (988,27, 118,80, 998,92 y 981,40 USD, todos ≤ 1000) quedan del lado seguro; no hay más ejecuciones y el script no cambia |
| 28 | la deuda del CRLF pedía comprobar el CRLF del CSV 2 en `MQL5\Files` «ANTES de copiarlo», y ya se copió | `HISTORIA.md:11296` | se comprobó el original contra la copia (§0.b), que es más fuerte: mismos bytes; y la medida de la 1 era un artefacto de `grep` |
| 36 | quien lee la comisión por su nombre es `simulacion.py:140`; `primitivas_broker.py` no la nombra (la ve por el saldo) | | §0.d |
| 39 | de los cinco sitios, A-28 no tiene regla de la spec ni entrada en la hoja de preguntas | `grep A-28 strategy_spec.yaml scripts/hoja_preguntas.py`: 0 | quedan `ambiguedades.yaml`, el registro, Known Ambiguities y `test_kit` |
| 42 | **la 1.2 tiene dos contenidos con `VERSION_SCRIPT "1.2"`**: 2688f8b y a90cd45 | `git log -- tools/mql5/MedirDemoFTMO.mq5` | **resuelto por medida**: el `.mq5` que hay en `MQL5\Scripts` del terminal tiene sha256 `f9903c6f…9151`, el de a90cd45 (y el de `main`), y el `.ex5` se compiló el 2026-11-05 a las 13:34 de Lima, un minuto antes de la ejecución. El manifiesto de la 3 lleva a90cd45 y lo declara así |
| 43 | **D9 para seguro por los swaps**, que ADR-0071 §5 ya dice que cambian con la fecha; freeze level y modo de margen no tienen parámetro | `0071:124-126`, perfil `:413-432` | decisión 1 (PARADA solo para los swaps) |
| 46 | en la hoja de ruta el literal es «congelar los tres CSV» (`HOJA:508`), no «sin congelar» | | la fila de ERRORES-RECURRENTES lo dice |
| — | D4 es una derivación por construcción: con 120 + `us` el servidor es Nueva York + 7 h siempre, y su PARADA no puede dispararse | | se escribe así en ADR-0090: comprueba el modelo, no la rejilla; la medida es la de R6a (decisión 2) |
| H1 | la fórmula del margen con la 2 (FTMO-P-D1 §3, ADR-0081 Impacto, recuadro de ADR-0026) | `FTMO-P-D1.md:85-92` | medida en §0.a: 3720,77 y 3744,30 casan; ADR-0090 lo registra y la frase de `firma_apalancamiento` (`parametros.yaml:2086-2090`) se reescribe |
| H2 | ADR-0068: «Cuando A-28 se cierre, el huso del calendario se revisa con ella» | `0068:9-14`, `:57-58` | recuadro en ADR-0068 y su fila del índice, en el commit del ADR (el huso `America/New_York` queda medido) |
| H3, H4 | la entrada F de la Next Action («Siguiente: la rama corta de la demo (A)») y lo «Opcional» de A (las noticias restringidas) se quedan sin destino si A sale | `PS:28`, `PS:42` | líneas del cierre (§0.h) |
| H5 | R6a.1 está HECHA y D4 le da la medida de la rejilla | `HOJA:391-408` | decisión 2 |
| H6, H7, H8 | frases en futuro de la ficha (`parametros.yaml:69, :85, :100, :115, :131`; A-27 `ambiguedades.yaml:673-674`), `huso_grafico` (:289-290) y las de DEMO-FTMO.md | | entran en g) y se reescriben |
| H9 | ADR-0082:153 y `cli.py:758` | | ADR-0082 recibe recuadro; `cli.py` es un comentario de historia y `src/` no se toca |

### Lo que no pude medir

- **A qué hora se reinicia el límite diario en el panel** (D5): Aleks no lo ha declarado en esta
  sesión. Pasa a una línea propia (§0.h).
- **Qué hizo la buy stop del nivel exacto de la 2 entre la lectura y el borrado** (fila 40, 10013):
  el CSV no lo registra.
- **M4** (si MT5 comprueba el margen al llenar): `no_salto` en 120 s; no hay más ejecuciones.
- **La rejilla H4 real del servidor**: ninguna de las tres ejecuciones la lee (D4).

### Exposiciones

Ninguna. Los CSV de la demo no son material del trader ni tienen días de ninguna partición; la salida
del arnés leída en §0.f es de meses de desarrollo y se contó sin imprimir filas.

### Negativas de la guardia en esta fase

1. `grep -c $'\r' …` (el recuento de CR sobre los CSV): la guardia lo niega porque `$'\r'` se
   construye al ejecutarse. Se midió con un guion del scratchpad que lee los bytes y con
   `grep -U -c -P '\r'`, que es la forma literal que la guardia propone; no se rodeó.
2. El mismo guion, lanzando `grep` desde `subprocess`, negado por la misma regla. No se insistió.
3. `sed -i … && uv run botsito state check` en una sola llamada, negado por la regla del mismo
   comando; partido en dos llamadas, como propone.

## Lo que necesito que decidas

Dos PARADAS condicionales, cada una solo para lo suyo: los swaps (D9, decisión 1) y la regresión
del 7 de agosto con la comisión medida (D6, decisión 3). Lo demás cuadra con D1-D12, y **sigo con la
fase 1 sin esperar** en todo lo que no dependa de ellas (puntos 1, 2, 3 y 5; el 4 espera).

0. **El `fin_de_linea: LF` falso del manifiesto inmutable de la 1.** Opciones: (a) el manifiesto no se
   toca; ADR-0090 lo corrige por escrito y DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c reciben un
   recuadro con la medida de §0.b; (b) solo ADR-0090. Recomiendo (a): los dos informes cerrados
   afirman un hecho falso, y la regla de la casa para eso es el recuadro. Coste de (b): dos informes
   que siguen diciendo LF. **Lo hago por (a)** en el commit del ADR, porque no contradice ninguna
   decisión; si prefieres (b), los recuadros salen.
1. **Los swaps (D9).** Las tres ejecuciones dan −9,41/0,10, −9,74/0,42 y −10,06/0,40; el perfil dice
   −9,49 y 0,36 (CONFIRMED, ADR-0050, la web del 2026-09-25). D9 manda PARADA si algo difiere. Opciones:
   (a) el perfil no cambia: ADR-0071 §5 ya dice que los swaps cambian con la fecha y no se fijan con
   una ejecución, el bot cierra a las 15:00 y el simulador solo los cobra si una operación pasa la
   noche; ADR-0090 registra las tres lecturas y no reabre A-27, que no los incluye; (b) el perfil pasa
   a la última lectura (−10,06 y 0,40) con fuente ADR-0090. Recomiendo (a): una cifra que cambia cada
   día no se fija con una ejecución, y ADR-0071 §5 ya lo razonó así con la 1 (el bot cierra a las
   15:00). Coste de (b): un valor que la próxima lectura vuelve a dejar viejo. **PARADA solo para
   esto: ADR-0090 deja los swaps escritos como «pendiente de la decisión 1» hasta tu respuesta.**
2. **Dónde vive la medida de la rejilla H4 real (D4), con R6a.1 ya HECHA.** Opciones: (a) una entrada
   nueva de la hoja, R6a.8 «La rejilla H4 real en el journal», que depende de R6a.1 y de la que
   dependen R6a.7 y F33; (b) R6a.1 vuelve a pendiente con esa pieza. Recomiendo (a): R6a.1 se cerró
   con su «Hecho cuando» cumplido, y reabrirla mezcla dos cosas. Coste de (b): una entrada HECHA que
   deja de estarlo. ADR-0090 y la descripción de `anclaje_h4` dicen «R6a» sin número hasta tu
   respuesta; la línea preparada va por (a).
3. **La regresión de la cuenta del 7 de agosto con la comisión medida (§0.e).** Con 2,50 la cuenta no
   se suspende ese día (+515,78 sobre el límite, frente a −514,47 con 5), y el test que fija la
   suspensión en el tick del pico deja de pasar. Opciones: (a) la regresión DECLARA su comisión, como
   ya declara su volumen máximo (`VOLUMEN_MAX_DE_LA_REGRESION`): `COMISION_DE_LA_REGRESION = 5` por
   `dataclasses.replace(..., comision_por_lote=...)`, y sigue probando el corte en el pico; más un test
   nuevo, en el mismo fichero, que con el perfil real (2,50) la cuenta de ese día queda EN_CURSO con la
   peor equidad 95.515,78; (b) cambiar lo que espera a EN_CURSO, y la regresión del corte se queda sin
   un caso real que la pruebe; (c) buscar otro día de construcción que se suspenda con 2,50. Recomiendo
   (a): conserva la regresión del corte y deja escrita la consecuencia de la medida. Coste de (b):
   perder la regresión; de (c), leer más días para encontrar uno, sin necesidad. **Hasta tu respuesta,
   el punto 4 de la fase 1 (la comisión en el perfil y sus tests) espera**; ADR-0090 dice la tarifa
   medida y el valor del perfil se cambia en el commit del punto 4.

## Respuesta del consultor a la PARADA (2026-11-06)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/demo-ejecuciones-2-3 (2026-11-06). Cópiala tal cual en el informe (skill fase-cero) y aplícala punto por punto.
>
> 0. Fin de línea de la ejecución 1: (a), como lo hiciste. El manifiesto no se toca, ADR-0090 lo corrige y DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c llevan su recuadro. Porqué: un informe cerrado que afirma algo falso se corrige con un recuadro, y el sha256 del manifiesto sigue fijando los bytes buenos.
>
> 1. Swaps: (a), el valor del perfil no cambia. Porqué: un swap cambia cada día y no se fija con una lectura (ADR-0071 §5). Añadidos:
>    - ADR-0090 registra las tres lecturas con su fecha y sustituye el «pendiente de la decisión 1» por esta decisión.
>    - La descripción de firma_swap_largo_puntos y de firma_swap_corto_puntos dice que su valor es el de la API del 2026-09-25, que cambia con la fecha (las tres lecturas de la demo, en ADR-0090) y que no se renueva porque no decide nada. Trailer Fuente: ADR-0090.
>    - Verifica, y escribe en ADR-0090 con fichero:línea, que ninguna operación del bot puede seguir abierta a la medianoche del servidor (la ventana de la operativa y el cierre un minuto antes del fin de la H4). Si alguna puede, PARADA solo para esto.
>    - Que no se reabre A-27 lo dejas dicho en una línea, citando sus cinco parámetros.
>
> 2. La rejilla H4 real: (a), una entrada nueva R6a.8 «La rejilla H4 real en el journal», que depende de R6a.1 y de la que dependen R6a.7 y F33. Porqué: R6a.1 se cerró con su «Hecho cuando» cumplido. Va como línea preparada para el cierre. ADR-0090 y la descripción de anclaje_h4 citan R6a.8 por su nombre en el commit del punto 4, y test_hoja_de_ruta tiene que pasar con la línea aplicada sobre la copia.
>
> 3. La regresión del 7 de agosto: (a). La regresión declara COMISION_DE_LA_REGRESION = 5, igual que VOLUMEN_MAX_DE_LA_REGRESION y por el mismo camino (dataclasses.replace), con un comentario de una línea: es la tarifa supuesta hasta ADR-0090, y se conserva para que el corte en el tick del pico siga teniendo un caso real que lo pruebe. Test nuevo en el mismo fichero: con el perfil real (2,50 por lado), la cuenta de ese día queda EN_CURSO y su peor equidad es 95.515,78. Porqué: no se pierde la regresión del corte y la consecuencia de la medida queda escrita en un test.
>    - El informe y ADR-0090 dicen, en una línea, que con 5 USD por lado el simulador suspendía cuentas que con la tarifa medida no se suspenden. Las corridas anteriores a esta rama eran pesimistas en las suspensiones, y la re-corrida que cuenta (ADR-0070 §3) es la primera con la tarifa medida.
>    - Punto 4 de la fase 1: la comisión a 2,50 en el perfil, las dos regresiones, R6a.8 en ADR-0090 y anclaje_h4, en un commit con Fuente: ADR-0090. Los dos tests que rompen a propósito (2,50 frente a 5 en test_perfil_cuenta y EN_CURSO frente a SUSPENDIDA), con su salida contra main pegada (comparar-con-main).
>
> 4. Fila de ERRORES-RECURRENTES preparada: añade, del consultor, «(menor) D9 metió los swaps entre los datos que tenían que coincidir, cuando ADR-0071 §5 ya dice que cambian con la fecha, y costó una PARADA. Lección: antes de poner un valor en una comparación de igualdad, mirar si el repo lo da por variable».
>
> 5. Lo que sigue: el punto 4, make check en cada commit, el revisor (opus, con los alcances del encargo, más las dos regresiones y que la comisión no aparezca con 5 en ningún documento vivo salvo la constante declarada) y la entrega con entregar-rama, que incluye las líneas del cierre aplicadas sobre una copia y la previsión de PROJECT_STATE con wc -c. Al terminar, quita los clones C:\cm\m y C:\cm\r con git worktree remove y dilo en el informe. Si de aquí sale otra PARADA, es solo para lo suyo: sigue con lo demás. Nunca cierres.
>
> Rama lista para revisión, NO cerrada.

## 1. Fase 1 · lo hecho sin esperar (2026-11-06)

La PARADA es condicional (encargo): sigo con lo que no depende de las decisiones 1 y 3. Un commit por
punto; antes de cada uno, estadiar, `uv run botsito state check`, `make check > make-check.log 2>&1`
y leer el log (exit 0, ningún `failed`, la línea `SELLO`); `ruff format`, `ruff check` y `mypy` sobre
el único `.py` nuevo o cambiado de cada punto.

| punto | commit | qué | `make check` |
|---|---|---|---|
| fase 0 | 49805c3 | el informe con la fase 0 | 3231 passed, SELLO `8142589c…` |
| 1 | dedc121 | los manifiestos de la 2 y la 3 + `tests/unit/test_manifiestos_demo_ftmo.py` (recuento de PROJECT_STATE 1857 → 1860) | 3236 passed, SELLO `f7571ccd…` |
| 2 | c1a2798 | ADR-0090; recuadros en ADR-0081 §4 (enmienda), ADR-0071 §3 y §4, ADR-0057 §2, ADR-0027 §4, ADR-0068 y ADR-0082; filas del índice; recuadros en DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c (decisión 0); sale el bloque `ids-inexistentes` del encargo y del informe; el contrato se amplía a esos dos informes | 3236 passed, SELLO `4a75f6af…` |
| 3 | d53bb2d | A-28 DECIDIDA en sus sitios, `broker_offset_base` 120 y `broker_dst` `us` CONFIRMED, las frases de g), `test_kit`, `spec_version` 18.6.1 → 18.6.2, `spec manifest` y `spec docs`, el yaml de cierres; trailer `Fuente: ADR-0090` | 3236 passed, SELLO `6d9da3ca…` |
| 4 | — | **espera a la decisión 3**: la comisión en el perfil y sus tests | — |
| 5 | 86dfa75 | `docs/runbooks/DEMO-FTMO.md`: las tres ejecuciones con su hora («Cuándo: tres veces»), la prueba del 2026-10-29, el panel como pendiente, los CSV congelados y el `grep -U` | 3236 passed, SELLO `27b16e72…` |

### 1.1 Los tests que rompen a propósito, contra `main` (comparar-con-main)

Mecanismo de la skill: el test de la rama, copiado en el clon `C:/cm/m` (`git worktree add --detach
C:/cm/m main`) y ejecutado allí. La guardia solo deja ejecutar en el clon un test IDÉNTICO al del
árbol del repo o al de `main` (negativas 4 y 5 de abajo), así que cada test se copia al clon después
de escribirlo en la rama.

**A-28 entre las DECIDIDAS de `test_kit` (falla en `main`):**

```
$ cd C:/cm/m && uv run pytest -q -p no:cacheprovider tests/unit/test_kit.py
E       AssertionError: assert {'A-15', 'A-1..., 'A-24', ...} == {'A-15', 'A-1..., 'A-24', ...}
E         Extra items in the right set:
E         'A-28'
FAILED tests/unit/test_kit.py::test_ambiguedades_reales_y_esquema - Assertion...
```

En la rama pasa (dentro de los `make check` de los puntos 3 y 5).

**El sufijo del `dataset_id` de un manifiesto de la demo** (no había test; `tests/unit/test_manifiestos_demo_ftmo.py`
es nuevo). Con un manifiesto cuyo sufijo no casa, copiado solo en el clon `C:/cm/r` junto al test
de la rama:

```
$ cd C:/cm/r && uv run pytest -q -p no:cacheprovider tests/unit/test_manifiestos_demo_ftmo.py
E       Left contains one more item: "sufijo '00000000' no son los 8 primeros del sha256 ('59565621')"
FAILED tests/unit/test_manifiestos_demo_ftmo.py::test_el_dataset_id_casa_con_el_sha256_y_la_fecha[demo-ftmo-2026-11-05-00000000.yaml-]
```

Con los tres manifiestos reales, 5 passed (en la rama). Además, `test_un_sufijo_que_no_casa_se_caza`
prueba el comprobador con un sufijo y una fecha falsos sin tocar ningún fichero.

**La comisión a 2,50 por lado (falla con 5):** escrita y probada en el clon de `main`
(`test_la_comision_por_lado_y_su_importe_estan_medidos`, que pide 2.50, CONFIRMED, fuente
ADR-0090 y las filas 54 y 55), pero no ejecutable allí hasta que exista en la rama, y entra en la
rama con el punto 4, que espera a la decisión 3. Su salida contra `main` se pega en ese commit.

### 1.2 El encargo, punto por punto

| punto del encargo | estado | dónde |
|---|---|---|
| Rama con abrir-rama, base comprobada, contrato (tramo, riesgo alto, artefacto) | hecho | «Base comprobada al abrir»; fd368ee |
| grep de «0090» en docs/ y Technical Debt antes de usarlo | hecho: libre (auditor, 4; sesión) | §«El encargo frente al repo» |
| FASE 0 a) a h) | hecho | §0.a-§0.h |
| D1 manifiestos | hecho; la 1.2 se ata a a90cd45 por el `.mq5` del terminal (auditor, 42) | dedc121 |
| D2 originales y deuda del CRLF | hecho: coinciden, la deuda se explica (artefacto de `grep`) y sale por (a) en el cierre | §0.b; ADR-0090 |
| D3 A-28 DECIDIDA | hecho | d53bb2d; ADR-0090 §1 |
| D4 anclaje_h4 como derivación | hecho; la medida, en R6a (decisión 2) | ADR-0090 §2; recuadro de ADR-0027 §4 |
| D5 el panel | Aleks no lo declaró: línea propia preparada (§0.h), `reloj_dia_riesgo` apunta a ella | d53bb2d |
| D6 comisión | **PARADA (decisión 3)**: ADR-0090 §3 y el recuadro de ADR-0071 §3 escritos; el perfil y sus tests esperan | §0.e |
| D7 paso 8 | hecho: ADR-0090 ENMIENDA ADR-0081 §4; (a)-(d); f sin rechazos; (c) y (d) entre las líneas del cierre | ADR-0090 §4; §0.f; §0.h |
| D8 nivel exacto | hecho: PROVISIONAL, recuadros en ADR-0057 §2 y ADR-0071 §4 | ADR-0090 §5 |
| D9 ficha y swaps | ficha: coincide (tabla); **swaps: PARADA (decisión 1)** | ADR-0090 §6 |
| D10 deslizamiento | hecho: sin cambio, observaciones registradas | ADR-0090 §7 |
| D11 la hora de la 3 | hecho, con `zoneinfo` | §0.c.3; ADR-0090; DEMO-FTMO.md |
| D12 M y el grabador | siguen vivos: A.5 preparada | §0.h |
| Herencias del encargo | cumplidas o dichas en §«El encargo frente al repo»; añadidas ADR-0068 y ADR-0082 | c1a2798 |
| Tests que rompen a propósito | `test_kit` y el del `dataset_id`, pegados; el de la comisión, con el punto 4 | §1.1 |
| CI | la rama no toca hooks, rutas, `.claude/` ni `src/`: sin `fix/` | — |
| Revisor | **no pasado todavía**: va cuando las dos PARADAS estén contestadas y aplicadas, para que revise la rama entera | — |
| «Rama lista para revisión» | **no**: faltan el punto 4 y los swaps | — |

### 1.3 Negativas de la guardia en la fase 1 (además de las de la fase 0)

4. `uv run pytest … tests` sobre todo el directorio en el clon: «tests es un directorio: la guardia no
   sabe que ficheros ejecutara». Se pasaron los ficheros nombrados (§0.e).
5. `pytest` en el clon de `main` con un test cambiado que aún no estaba en la rama: «el codigo nombra
   la carpeta /…» y «no se pudo resolver el modulo `tests.unit.perfil_stops_level_unknown`». Es el
   riesgo residual de `trabajo/guardia-g1` que ya está en Technical Debt: el test del clon solo se
   ejecuta si es el de `main` o el del árbol del repo. Se escribió primero en la rama.
6. Varios comandos compuestos (`wc -c … && pytest`, `rm … && make check`, `git add … && state
   check`, dos guiones en una llamada): partidos en llamadas sueltas, como propone la guardia.

### 1.4 La fila de ERRORES-RECURRENTES, preparada (la escribe el cierre)

| Rama | Hallazgos del revisor | Hallazgos del consultor despues | Que se le escapo |
|---|---|---|---|
| `trabajo/demo-ejecuciones-2-3` | (tras su pasada) | **(importa, del consultor)** la orden de cierre de F38n escribió en la Next Action «los tres CSV en data/demo_ftmo/ sin congelar» (y en la hoja de ruta «congelar los tres CSV»), cuando la 1 está congelada desde el 2026-10-09. Lección: antes de dar por pendiente un paso, buscar su artefacto (aquí, `data/manifests/demo_ftmo/`). **(menor)** el resumen del consultor del 2026-11-06 dio «deslizamiento 0», y la 2 trae 2,0 puntos en contra al abrir a mercado. Lección: una cifra de un CSV se lee por ejecución, no se resume. **(importa)** el plan del consultor era una NOTA en ADR-0081 §4, cuando la medida desmiente lo que §4 da por hecho y lo que modela el bróker simulado; lo cazó su auditor antes de entregar el encargo. Lección: antes de decidir entre nota y enmienda, leer qué da por hecho el ADR y qué hace el código. **(importa, de la sesión, fase 0)** el LF de la ejecución 1, medido dos veces con `grep -c $'\r'` (DEMO-EJECUCION-1 y EA-CONEXION) y apuntado en un manifiesto inmutable, era el `grep` de Git para Windows, que quita el CR sin `-U`. Lección: un recuento de bytes se hace leyendo bytes (o con `grep -U`), no con un `grep` de texto. **(importa, del encargo)** D6 contaba con que la comisión solo rompería tests de importe o de saldo, y rompe la regresión del corte del 7 de agosto (§0.e). Lección: antes de cambiar un coste, medir qué estado de cuenta cambia con él. | (tras la revisión) |

### 1.5 Lo que no pude medir, añadido en la fase 1

- La salida contra `main` del test de la comisión: va con el punto 4 (§1.1).

## Estado

EN CURSO, en PARADA (2026-11-06): fase 0 entregada y fase 1 hecha en sus puntos 1, 2, 3 y 5. Esperan a la respuesta del consultor la decisión 1 (los swaps) y la decisión 3 (la regresión del 7 de agosto con la comisión medida), y con ella el punto 4. Después: el revisor y la entrega. NO lista para revisión.
