# F17-ORDENES · La medida de las órdenes stop y el grabador de ticks de la demo de FTMO, con sus herramientas y sin correr (R4.7, entrada F)

> PLANTILLA: informe de la rama `trabajo/f17-ordenes`. Estado: EN CURSO (respuesta a la PARADA, aplicándose). La fase 0 y su
> PARADA, lo hecho tras la respuesta, el encargo punto por punto, las desviaciones, las líneas del
> cierre, la fila de ERRORES y el informe del revisor se escriben aquí según avanza la rama.

Rama `trabajo/f17-ordenes`, abierta el 2026-11-26 desde `main` en e8c20a80 (commit de estado sobre
el merge 8066b377 del tag `stable/F39p-f17-historial`). Encargo:
`docs/encargos/trabajo-f17-ordenes.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la A.5 se
cita en el informe; la F de la Next Action). Tag previsto: `stable/F39q-f17-ordenes`.

## Base comprobada (abrir-rama, paso 1)

- `git fetch origin`; `git status --short` vacío; `git rev-parse main origin/main`:
  `e8c20a808e60b7cffe333a60f2c3fbdc53712086` dos veces.
- `git rev-parse "stable/F39p-f17-historial^{commit}"` = `git rev-parse main^1` =
  `8066b377a4534348529c90fe89974a208409f19d`; en origin, `83a4e4d2…` (el objeto del tag anotado) y
  `8066b377…` (`^{}`). Es el último `- Tag: ` de HISTORIA y el último `stable/*` de origin
  (`git ls-remote --tags origin "refs/tags/stable/*"`, ordenado: F39n, F39o, F39p al final).
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal da el check `python` en
  `completed` / `success`, del run 45864298815 (el que cita el encargo).
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*" "trabajo/*"
  "feature/*"` sale vacío.

## 0. Fase 0

Sin escribir código. Lo leído, en la fila de HOLDOUT del 2026-11-26 de esta rama (0.1). Sesión en
Opus 5.5 (`/model`); el esfuerzo lo fija Aleks en `/effort` y la sesión no lo puede leer.

### 0.1 La fila de HOLDOUT del día

Escrita y estadiada antes del primer `make check` de la rama (el de la apertura), en
`docs/validation/HOLDOUT-EXPOSICIONES.md`; G2 la vio estadiada. Una precisión que se añade en el
commit de la fase 0: para comprobar `meses_reservados.yaml` (D6) la sesión leyó solo sus CLAVES
(`2025-12`, `2026-02`, `2026-03`, `2026-10`, `2026-11`) y, al buscar el fichero, listó los NOMBRES
de primer nivel de `knowledge/cases/` (`dev`, `fidelidad`, `holdout`, ...), sin entrar en ninguna
carpeta. Va en la fila de hoy.

### 0.2 Lo leído, con fichero:línea

**`tools/mql5/MedirDemoFTMO.mq5`** (1.560 líneas, versión 1.2):

- `MAGICO` 57057000 (:33); `SIMBOLO` "EURUSD" (:32); `InpPausaMs` = 1500, un `input` (:37), que
  cada petición duerme tras `OrderSend` (:210, :233, :284, :647, :703, :946 y :967; `ColocarBuyStop`
  solo si `pausar`, :945).
- `Comprobaciones` (:757-791): la negativa DEMO es la :759, literal, la PRIMERA comprobación;
  después el símbolo, el trading algorítmico, `SYMBOL_TRADE_MODE_FULL`, la cotización y que no tenga
  más de 120 s. `OnStart` la llama lo primero y sale con `Alert` si falla (:1506-1513).
- La limpieza: `QuedanAbiertas` (:293-309) y `Limpiar` (:311-342) cuentan y borran pendientes y
  cierran posiciones **solo del `MAGICO` y de EURUSD**, hasta 5 intentos con 2 s entre ellos, y
  escriben `quedan_abiertas_<cuando>`; `OnStart` limpia al empezar (:1531), tras cada paso
  (:1536-1542) y al terminar (:1551).
- `Llenado()` (:153-161): FOK si el símbolo lo admite, si no IOC, si no RETURN. `PonerCaducidad`
  (:163-173): `ORDER_TIME_SPECIFIED` a `TimeTradeServer() + 15 min` si el símbolo admite
  `SYMBOL_EXPIRATION_SPECIFIED`; si no, GTC (es decir: sin caducidad).
- El paso 7, `MedirLlenadoStop` (:678-752): una buy stop a `ask + (max(stops,1)+1)` puntos con
  `g_volumen` (el volumen mínimo, :1516), stop de protección a 200 + stops level; espera hasta
  `InpEsperaStopSeg` (120 s) a que la pendiente desaparezca y escribe **el precio del llenado menos
  el NIVEL** (:739-741). No registra el tick que la dispara ni el instante del llenado.
- El paso 8: `P8_TOPE_USD` 1000.0 (:804), `P8_COMISION_LADO` 5.00 (:805; ADR-0090 §3 midió 2,50:
  el tope queda del lado seguro), `P8_DESLIZ` 10 puntos (:806), `P8_STOP_MIN` 10 y `P8_STOP_MAX` 200
  (:809-810). `PeorCaso` (:882-894) suma, de cada compra, `OrderCalcProfit(ORDER_TYPE_BUY, ...)`
  hasta `precio - (stop + P8_DESLIZ)` más la comisión de ida y vuelta: **solo compras**. `StopDelTope`
  (:899-925) baja el stop de 200 al mínimo hasta que el peor caso quepa en el tope; 0 si ni el
  mínimo cabe.
- Su contrato, `tests/contract/test_medir_demo_ftmo.py`: toda función que llama a `OrderSend` con
  `TRADE_ACTION_DEAL` o `TRADE_ACTION_PENDING` lleva `.magic`, `.sl` distinto de 0 y, si es pendiente,
  `PonerCaducidad` (:78-102), salvo la lista cerrada `SIN_STOP` (`EnviarPendiente`, `CerrarPosicion`,
  :25-29); una acción por variable o sin `.action` es un problema (:86-90); la lista de las que
  envían está fijada (:125-136); la condición DEMO sigue en la :759 (:139-145); y cada regla rompe
  con el fuente mutado (:161-234).

**`tools/mql5/ExportarTicksFTMO.mq5`** (275 líneas) y su contrato
`tests/contract/test_exportar_ticks_ftmo.py`: no llama a ninguna función de trading
(`llamadas_de_trading` de `test_capa_mt5.py`, :62-64), lleva la condición DEMO literal (:65-71) y
`OnStart` comprueba antes de pedir nada (:74-81); solo EURUSD (:89-91); `CopyTicksRange` con hasta
3 intentos y 1 s entre ellos (:134-148 del .mq5); escribe con `FileOpen(... FILE_ANSI)` y CRLF
(:156-163), no de forma atómica.

**`scripts/leer_historial_f17.py`**: `RelojServidor` (:75-122) pasa el reloj del servidor a UTC con
`broker_offset_base` y `broker_dst` del registro y el `dst()` de zoneinfo, sin cifras, y falla en la
hora repetida o saltada; `percentil` (:179-184) es el de rango más cercano de `ticks_spread.py`, y
`mediana` (:187-188); `a_puntos` (:442-447) pasa un precio a puntos exactos; `_filas` (:433-439) lee
el CSV de MQL5 en cp1252 y con CRLF; `leer_ticks` y `leer_m1` (:459-503) pasan cada instante a UTC.
El esquema del manifiesto (:558-624) exige un mes de construcción (:595-597), y
`tests/unit/test_manifiestos_f17.py`:126-128 valida con él todo `data/manifests/f17/*.yaml`: un
manifiesto de esta rama ahí rompería (D7 lo evita).

**`src/botsito/mql5bridge/compilar.py`**: el camino `herramienta` (:117-156 y `_herramienta`,
:328-344) copia del ÍNDICE de git un `.mq5` directamente bajo `tools/mql5/` (`_HERRAMIENTA`, :122) y
lo instala en `MQL5/Scripts/Botsito/`: solo scripts. Acepta varias fuentes en una llamada. No hay
que cambiarlo.

**Los ADR y reglas:**

- ADR-0092 §4 (:99-115): a cada llenado de orden stop y a cada cierre por stop o a mercado se le
  resta la MEDIANA medida, y la esperanza con el percentil `percentil_deslizamiento_f17` tiene que
  ser > 0; la puerta no da «pasa» antes de F17.
- ADR-0099 §5 (:152-180): las tres partes de F17; la medida coloca órdenes stop «con lotes del orden
  de los del bot, espaciadas y muy por debajo del tope de peticiones (ADR-0067)» y registra el nivel,
  el tick que la dispara, el precio y el instante del llenado y los lotes, y lo mismo en los cierres;
  la referencia es el precio del llenado menos el del tick que dispara.
- ADR-0090 §3 (:102-128): la comisión medida, 2,50 USD por lote y lado. §4 (:130-165): la tasa de
  margen de una buy stop es 0;0 en la prueba (una pendiente no reserva margen) y la fórmula del
  margen, `lotes × 100.000 × precio / 30`, con 1,12329 → 3.744,30 USD por lote. §7 y su recuadro
  (:231-240): las siete observaciones de deslizamiento (con 0,01 y 1,00 lotes), «no un modelo».
- ADR-0067 (:30-39): `freno_peticiones_aviso` 1000, `freno_peticiones_corte` 1500, por debajo de
  `firma_mensajes_dia_max` (2.000).
- ADR-0081 D2 (:53-61): lote = mín(lote del riesgo, `firma_volumen_max_lotes`, lo que cabe en
  `margen_libre × lote_margen_libre_fraccion`), hacia abajo al paso. `lote_margen_libre_fraccion`
  (parametros.yaml:2192) vale 0,95; `firma_apalancamiento` 30 y `firma_volumen_max_lotes` 50
  (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`:270-300); `riesgo_por_operacion` 0,5 %.
- ADR-0068 §4 (:75-87): las sesiones de `SymbolInfoSessionTrade` se unen al calendario; no traen los
  festivos. `firma_gap_margen_minutos` y `firma_gap_cierre_minimo_minutos` = 120 (§5).
- ADR-0082 D6 (:134-138; está en su §7): la capa solo en DEMO hasta F35, con la condición de
  `MedirDemoFTMO.mq5:759`.
- ADR-0021 §1: las velas no son holdout.
- `knowledge/cases/criterio_fidelidad.yaml`:81-83: `deslizamiento: pendiente_F17` y
  `percentil_deslizamiento_f17: 90`.
- `entrada_tipo_orden` = `stop_en_ruptura` (parametros.yaml:1032-1052; A-47 RESUELTA): el bot entra
  por stop. Y `stop_en_orden_pendiente` (:1053): el stop va en la orden (lo usa D1, abajo).
- `FTMO-REGLAS.md`: R2 (:49), el límite diario se recalcula a las 00:00 CE(S)T con el saldo de ese
  instante menos el 5 % del capital inicial; R3 (:50), estático en el capital menos el 10 %; R13
  (:60) y su recuadro (:69-79), solo cuentan las acciones de trading (abrir, cerrar y modificar,
  también mover el stop), no las lecturas, y no se sabe si una rechazada cuenta (A-54); R15 (:62),
  nada a dos horas o menos de un cierre de al menos dos horas; R16 (:63) y R17 (:64), que prohíbe
  «opening substantially larger position sizes compared to your other simulated trades».
- `DEMO-FTMO.md`:158-166: el aviso de pérdida del día se restablece a las 00:00 de España y no a la
  medianoche del servidor (declarado por Aleks el 2026-11-07); :189 y :210, las pruebas son 2-Step,
  Swing, USD, 100.000, servidor FTMO-Demo; y la cuenta es HEDGING, medido (:194-200).
- `reloj_dia_riesgo` (parametros.yaml:1730): `civil_operativa`, la medianoche de `huso_operativa`.
- `AUDITORIA-PROFUNDA-2026-11.md`:447 (qué tiene que medir F17), :996 (P4-06: «Mediana a ±0,37
  puntos (±0,05 R)»; el p90, cota con n ≥ 29; «100-400 por clase»; una prueba da unos 56-62
  llenados del bot) y :1231-1232 (P4-08, si la prueba ejecuta como la cuenta real, PREGUNTA
  PENDIENTE).
- `docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.txt`:67: «mediana de D: 18 puntos».
- `ADR-0071`:39-48 y `ADR-0090`:191: stops level y freeze level 0 en las tres ejecuciones.
- `engine/llenado.py`: la stop de entrada (:205-266) salta con el ASK (compra) o el BID (venta) que
  toca o pasa el nivel, y se llena a ese tick; el stop de una posición (:305-330) con el BID (larga)
  o el ASK (corta).
- Lo que ya vive: `mql5/Include/Botsito/Capa/Sesiones.mqh`:6-9 dice que las sesiones van en
  «segundos desde las 00:00 de un dia de la semana del servidor»; **es lo que dice la capa, no la
  documentación** (0.3).

### 0.3 La documentación de MQL5 (subagente `web-fetch`)

Leídas, todas con HTTP 200: orderproperties, dealproperties, positionproperties, copyticksrange,
copyticks, mqltick, ordercalcmargin, ordercalcprofit, timegmt, timetradeserver, timecurrent,
symbolinfosessiontrade, mqltradetransaction, mqltraderequest, historyselect, historyorderselect,
marketinfoconstants, filemove, filedelete, fileisexist, filefindfirst, isstopped, runtime/running y
timetostruct (todas bajo `https://www.mql5.com/en/docs/`).

| qué | lo que dice la documentación | lo que no dice |
|---|---|---|
| `ORDER_TIME_SETUP_MSC` | «The time of placing an order for execution in milliseconds since 01.01.1970» (`long`) | — |
| `ORDER_TIME_DONE_MSC` | ejecución **o cancelación**, en ms | — |
| `DEAL_TIME_MSC` | «The time of a deal execution in milliseconds» | — |
| el instante en que se pone el stop de una posición | ninguna propiedad lo fija; `POSITION_TIME_UPDATE_MSC` es «Position changing time», sin decir si mover el SL la cambia | → D1 lo esquiva: el stop va en la orden pendiente, así que vive desde el deal de entrada |
| cierre por stop / a mercado | `DEAL_REASON_SL`: «as a result of Stop Loss activation»; `DEAL_REASON_EXPERT`: «placed from an MQL5 program, i.e. an Expert Advisor or a script»; `DEAL_ENTRY_IN` / `DEAL_ENTRY_OUT`; `ORDER_REASON_SL` en la orden | que distinga script de EA |
| `CopyTicksRange` | `(símbolo, ticks[], flags, from_msc, to_msc)`, ticks con `time >= from_msc` y `<= to_msc`, el 0 el más antiguo; `ERR_HISTORY_TIMEOUT`: «ticks synchronization waiting time is up, the function has sent all it had» | cuánto espera, si un script espera, hasta dónde llega hacia atrás |
| `CopyTicks` | `(símbolo, ticks[], flags, from, count)`; «can wait for the result for 45 seconds in Expert Advisors and scripts» y devuelve lo que tenga; caché de 4.096 ticks por símbolo | — |
| banderas | `COPY_TICKS_INFO` (cambios de Bid o Ask), `COPY_TICKS_TRADE`, `COPY_TICKS_ALL`; `TICK_FLAG_BID`, `TICK_FLAG_ASK`, ... | sus valores numéricos |
| `OrderCalcMargin` | en la moneda de la cuenta, «as if there were no pending orders and open positions» | — |
| `OrderCalcProfit` | solo `ORDER_TYPE_BUY` u `ORDER_TYPE_SELL`; en la moneda de la cuenta | si incluye comisión (el paso 8 la suma aparte, :891) |
| `TimeGMT` | «calculated taking into account the DST switch by the local time on the computer» | — |
| `TimeTradeServer` | calculado en el terminal, «depends on the time settings on your computer» | — |
| `TimeCurrent` | «The time value is formed on a trade server and does not depend on the time settings on your computer» | — |
| `HistorySelect` | «for the specified period of server time» | — |
| `SymbolInfoSessionTrade` | «seconds from 00 hours 00 minutes», `session_index` desde 0 | **en qué huso**: no lo dice ninguna página leída |
| órdenes rechazadas | existe `ORDER_STATE_REJECTED`; «canceled or have led to a transaction» van a la pestaña Historia | si una rechazada entra en el historial |
| `FileMove` | sin `FILE_REWRITE` no sobrescribe y devuelve false; dentro del sandbox | — |
| `IsStopped` | al pedir parar, el programa tiene 3 s o se termina desde fuera | — |
| un script tras reiniciar el terminal | los scripts se descargan al terminar; los EA y los **servicios** vuelven a cargarse solos | que un script vuelva (por omisión: no) |

### 0.4 La aritmética

Cifras: riesgo 0,5 % de 100.000 = 500 USD; stop mediano de construcción, 18 puntos
(`premisa.txt`:67); el valor de un punto con 1,00 lote de EURUSD en una cuenta en USD, 1 USD
(contrato 100.000 × 0,00001); comisión 2,50 por lote y lado (ADR-0090 §3); tasa de margen
`lotes × 100.000 × precio / 30` (ADR-0090 §4).

**El lote del bot (ADR-0081 D2):**

- lote del riesgo: 500 / 18 = 27,78 → 27,77 lotes;
- `firma_volumen_max_lotes`: 50;
- lo que cabe en el margen: 100.000 × 0,95 × 30 / (100.000 × precio) = 28,5 / precio: con 1,12329
  (el de ADR-0090 §4), **25,37 lotes**; con 1,16, 24,56.

El mínimo es el margen: **unos 25 lotes, limitado por margen**, como dice el auditor del consultor.
Con un precio por debajo de 1,026 mandaría el riesgo (27,77). En vivo, con `OrderCalcMargin` del
momento y el margen libre del momento (D1), sale lo que dé la cuenta.

**El tope (a) con el lote del bot.** El peor caso de `PeorCaso` con 25,37 lotes, stop 18 y
`P8_DESLIZ` 10: 25,37 × 28 × 1 + 2 × 5 × 25,37 = 710,4 + 253,7 = **964 USD**, por debajo de 1.000,
pero justo: con un precio de 1,08 (26,39 lotes) da 1.003 y no cabe. Ver decisión 2.

**El coste de un ciclo.** Si el precio es una martingala en esos minutos (SUPUESTO declarado: no
se ha medido), el resultado esperado del movimiento es 0 y el coste esperado es la comisión, el
spread y el deslizamiento: por lote, 5 + s + d USD, con s el spread y d el deslizamiento de las dos
patas en puntos. El spread de FTMO está sin medir (es lo que mide F17); con s + d entre 1 y 3:

| estrato | lotes | coste esperado por ciclo | peor ciclo (stop 18, `P8_DESLIZ` 10, comisión 5 por lado) |
|---|---|---|---|
| «uno» | 1,00 | 6-8 USD | 38 USD |
| «bot» | ~25 | 150-200 USD | ~964 USD |

**Cuántos ciclos de cada clase.** Cada ciclo da una entrada stop y una salida, que es por stop o a
mercado. Si p es la fracción de ciclos que salen por stop dentro del tiempo T, para n muestras de
cada clase hacen falta N = n / mín(p, 1 − p) ciclos. p no está medido. Con un paseo aleatorio y una
σ de unos 10 puntos por minuto en la ventana (SUPUESTO, no medido), p = 2·(1 − Φ(18 / (σ·√T))): con
T = 300 s, p ≈ 0,42. Propongo **stop a 18 puntos y T = 300 s** y, como mín(p, 1 − p) es lo que
cuenta, la aritmética va con p = 0,4 (N = 2,5 n):

| estrato | n por clase (D3) | ciclos | coste esperado |
|---|---|---|---|
| «uno» | 100 | 250 | 1,5-2 k USD |
| «bot» | 30 | 75 | 11-15 k USD |
| «bot» si el lote importa | 100 | 250 | 37-50 k USD |

**Lo que cabe en una prueba.** El tope (c) deja 8.000 USD de pérdida en toda la prueba (14 días, una
sola activa). El tope (b), 3.000 al día. Las peticiones: un ciclo pide 2 (colocar, y cerrar a
mercado si no salta el stop) o 3 (si la pendiente no se llena y se borra); con 1,5 s de pausa, un
ciclo dura de 1 a 6 minutos y caben unos 80-100 en las 8 horas de la ventana: ~250 peticiones al
día, por debajo de las 500 de (d).

- «uno»: 250 ciclos son unos 3 días de ventana y ~2 k USD;
- «bot»: con lo que queda en la primera prueba (~6 k USD), unos 30-40 ciclos; al día, el tope (b) da
  unos 15-20 (y la varianza, unos 25 lotes × ~15 puntos ≈ 375 USD por ciclo, lo hace saltar antes).

**Cuántas pruebas.** La primera: el historial, el grabador en marcha, «uno» entero y lo que quepa
de «bot» (~35 ciclos). La segunda: «bot» hasta 75 ciclos. **Dos pruebas para el estrato «bot», tres
con margen**, como estima el auditor del consultor. Si el lote importa (100 por clase en «bot»): 250
ciclos «bot», a ~6 k USD por prueba, **seis o siete pruebas más**; el auditor estima de siete a diez.
La diferencia es p y el coste por ciclo, que no están medidos: la primera prueba los mide, y el
runbook dice que el plan de las siguientes se rehace con ellos.

**Una precisión sobre P4-06.** «±0,37 puntos (±0,05 R)» supone un R de 7,4 puntos; con la mediana de
D de `premisa.txt`:67 (18 puntos), ±0,05 R son ±0,9 puntos. D3 no depende de eso: dice que cualquier
diferencia entera rompe la precisión, y con 18 puntos 1 punto son 0,056 R, por encima de 0,05 R; la
regla se mantiene.

### 0.5 El auditor

(Ver «El encargo frente al repo», abajo.)

## 1. El diseño propuesto (PARADA)

### 1.1 `tools/mql5/MedirOrdenesFTMO.mq5` (D1)

Un script, versión 1.0, con `#property script_show_inputs`. Lo que copia de `MedirDemoFTMO.mq5`
sin editarlo: `Comprobaciones` con la condición DEMO literal en su primera línea, `Llenado()`,
`PonerCaducidad`, `QuedanAbiertas` y `Limpiar` (con su propio número mágico), `VolumenHaciaAbajo`,
`Margen` y el cálculo de `PeorCaso` / `StopDelTope`, ampliado a las ventas.

- **Número mágico** `57057100` (MedirDemoFTMO usa 57057000; la capa de `mql5/` no usa ninguno: no
  envía órdenes y `grep` de `magic` en `mql5/` no da nada).
- **Entradas**: `InpEstrato` (`uno` o `bot`), `InpCiclos` (cuántos, como mucho), y nada más que
  cambie la seguridad: la distancia del stop, el tiempo T, la pausa y los topes son constantes.
- **El ciclo** (uno cada vez, nunca dos vivos a la vez; alterna compra y venta):
  1. comprueba los topes (1.4) y el tope (a) con lo que haya vivo del número mágico;
  2. lee la cotización y coloca la stop a `DISTANCIA_ENTRADA` puntos (decisión 8; la regla de
     `MedirLlenadoStop`, :684, daría `max(stops level, 1) + 1` = 2 con el stops level 0 medido)
     por encima del ASK (compra) o por debajo
     del BID (venta), con el lote del estrato, el **stop en la orden** a `STOP_PUNTOS` (18) del
     nivel y la caducidad de `PonerCaducidad`; la petición, en una fila;
  3. espera hasta `ESPERA_LLENADO_S` (120 s, como el paso 7) a que se llene; si no, la borra (fila);
  4. lleno: espera hasta `T_SALIDA_S` (300 s) a que salte el stop; si no salta, lee la cotización
     (`SymbolInfoTick`) y cierra a mercado con `req.position` (cuenta HEDGING, medido) y la escribe;
  5. tras cada llenado (entrada, stop o cierre), espera `ESPERA_TICKS_MS` (5 s, para que el terminal
     tenga los ticks) y copia con `CopyTicksRange(EURUSD, COPY_TICKS_ALL, puesta_msc, llenado_msc)`
     a un CSV por llenado, hasta 3 intentos como `ExportarTicksFTMO`, y escribe cuántos y el error;
  6. comprueba que no queda nada del número mágico; si queda, `Limpiar` y para.
- **El instante en que se pone la orden o el stop**: la entrada, `ORDER_TIME_SETUP_MSC` de la orden;
  el cierre por stop, `DEAL_TIME_MSC` del deal de entrada (el stop vive en la orden desde que se
  coloca y en la posición desde que nace: ninguna propiedad documentada da el instante de un SL
  puesto después, 0.3, y así no hace falta); el cierre a mercado, `ORDER_TIME_SETUP_MSC` de su orden.
- **La clase de un cierre**, del historial: `DEAL_ENTRY_OUT` con `DEAL_REASON_SL` es «cierre_stop»;
  el que pide el script (`DEAL_REASON_EXPERT`) es «cierre_mercado». Cualquier otro motivo (`SO`, `TP`,
  ...) sale con su nombre y el lector no lo usa.
- **El lote del estrato «bot»**, en vivo antes de cada ciclo: `mín(VolumenHaciaAbajo(0,005 × saldo
  / (STOP_PUNTOS × valor del punto por lote)), SYMBOL_VOLUME_MAX, VolumenHaciaAbajo(margen libre ×
  0,95 / margen de 1 lote))`, con el margen de 1 lote de `OrderCalcMargin(ORDER_TYPE_BUY` o
  `ORDER_TYPE_SELL`, al ASK o al BID del momento)`, **nunca con el tipo stop**: en esta prueba la
  tasa de margen de una buy stop es 0;0 y `OrderCalcMargin` a la orden dio 0,00
  (DEMO-EJECUCIONES-2-3.md:84-86; ADR-0090 §4), con lo que el límite por margen desaparecería y el
  lote subiría al del riesgo, 27,77, con el que el stop de 18 ya no cabe en el tope (a); es como lo
  pide `MedirDemoFTMO.mq5`:1076 (hallazgo 2 del auditor). El valor del punto,
  `SYMBOL_TRADE_TICK_VALUE / SYMBOL_TRADE_TICK_SIZE × SYMBOL_POINT`. Las tres cifras (0,005, 0,95 y
  el 18) son constantes del `.mq5` que un test compara con `riesgo_por_operacion`,
  `lote_margen_libre_fraccion` y el yaml de D3 (decisión 1).

**Columnas de `F17M_<estrato>_<AAAAMMDD_HHMMSS>.csv`** (una fila por evento; ANSI y CRLF, como el
resto de herramientas):

`version_script,fila,ciclo,estrato,evento,clase,lado,orden,deal,posicion,nivel,lotes,precio,instante_msc,puesta_msc,cot_bid,cot_ask,cot_msc,motivo,retcode,ticks_fichero,ticks_n,ticks_error,comision,hora_servidor,hora_gmt,nota`

- `evento`: `peticion` (cada `OrderSend`, con su retcode, ANTES de la siguiente), `llenado`,
  `tope`, `limpieza`, `contexto` (versión, cuenta DEMO, los relojes de `MedirReloj`, la ficha) y
  `fin`;
- `clase` (solo en `llenado`): `entrada_stop`, `cierre_stop` o `cierre_mercado`; `lado`: `compra` o
  `venta`, **el de la ejecución** (el cierre de una compra es una venta);
- `precio` e `instante_msc`: `DEAL_PRICE` y `DEAL_TIME_MSC`; `puesta_msc`: lo de arriba;
  `cot_*`: la cotización leída justo antes de pedir un cierre a mercado (vacía en los demás);
  `motivo`: `DEAL_REASON` por su nombre.

**Ticks de cada llenado**: `F17M_ticks_<deal>.csv`, `time_msc,bid,ask,flags`, como `ExportarTicksFTMO`.

### 1.2 `tools/mql5/GrabarTicksFTMO.mq5` (D2)

Un script de solo lectura (su contrato reutiliza `llamadas_de_trading` de `test_capa_mt5.py`, como
el del exportador), con la negativa DEMO literal y solo EURUSD. En bucle `while(!IsStopped())`:

- cada `PAUSA_MS` (1 s) pide con `CopyTicks(EURUSD, COPY_TICKS_ALL, desde_msc, 0)` los ticks desde el
  último `time_msc` escrito (los de ese mismo milisegundo ya escritos se saltan por recuento, porque
  pueden repetirse);
- escribe en `F17G_<AAAA-MM-DD>_<HH>.part` (hora del servidor) y, cuando la hora se cierra, lo pasa
  con `FileMove(..., FILE_REWRITE)` a `F17G_<AAAA-MM-DD>_<HH>.csv`: el `.csv` solo aparece entero
  (atómico: temporal y renombrado; `FileMove` sin `FILE_REWRITE` no sobrescribe, 0.3);
- **la primera vez** (sin ningún `F17G_*.csv`): empieza al inicio (minuto 00) de la hora del servidor
  en que se lanza, nunca en «el primer tick disponible» (fue el error (3) del consultor en F39p,
  ERRORES-RECURRENTES.md:136, y esa primera llamada puede descargar historial del servidor, el
  heredado 6; hallazgo H9 del auditor);
- **al relanzarlo**: busca el último `.csv` completo con `FileFindFirst("F17G_*.csv")`,
  descarta el `.part` que hubiera, y rehace con `CopyTicksRange` desde el inicio de la hora siguiente
  al último `.csv` hasta ahora, una hora cada vez, del servidor: sin hueco, mientras el servidor
  guarde esos ticks; lo que no devuelva, sale en el control;
- un `F17G_control_<AAAAMMDD_HHMMSS>.csv` por arranque, como el del exportador: versión, cuenta DEMO,
  servidor, los relojes y, por hora rehecha o grabada, cuántos ticks, el error, los intentos y el
  desfase `TimeTradeServer() − TimeGMT()` al cerrarla (MASTER_PLAN.md:285 lo pide «en cada evento»;
  hallazgo H1 del auditor: aquí, en cada hora, que es lo que el lector necesita para pasar a UTC y
  para ver si el reloj cambia a mitad de una grabación).

Columnas de cada hora: `time_msc,bid,ask,flags`. Un script no vuelve solo tras reiniciar el
terminal (0.3: los EA y los servicios sí; un script, por omisión, no): el runbook dice que Aleks lo
relanza (decisión 6).

### 1.3 Los lectores (D5): `scripts/leer_ordenes_f17.py`

Uno solo, con dos formas, como `leer_historial_f17.py`:

    uv run python scripts/leer_ordenes_f17.py medida <carpeta> --salida <fichero>
    uv run python scripts/leer_ordenes_f17.py grabador <carpeta> --salida <fichero>

Importa de `leer_historial_f17.py` (por ruta, como sus tests, sin editarlo) `RelojServidor`,
`percentil`, `mediana`, `a_puntos` y `_filas`.

- **medida**: por cada `llenado`, el tick que dispara en `F17M_ticks_<deal>.csv`: el primero con
  `puesta_msc < time_msc <= instante_msc` (el borde de la puesta fuera, como el simulador,
  `llenado.py`:233-234; el del llenado dentro, porque el tick que llena puede llevar su mismo
  milisegundo; `CopyTicksRange` da los dos bordes, 0.3; decisión 9) cuyo ASK (si el lado es compra) o BID (venta) toca o pasa
  el `nivel` por el lado que ejecuta (compra: `ask >= nivel`; venta: `bid <= nivel`); el
  deslizamiento, en puntos con «+ en contra», es `precio − tick` en una compra y `tick − precio` en
  una venta. Un cierre a mercado usa `cot_ask` o `cot_bid`. Sin tick: `sin_tick`; y, aparte, una
  entrada cuyo nivel ya lo había pasado la cotización leída antes de colocarla (o un tick entre esa
  lectura y la puesta) sale `al_colocar` (decisión 8). La ventana: el
  instante UTC del llenado dentro de `[ventana_inicio, ventana_fin)` del día por
  `reloj_de_las_sesiones` (sin el calendario de cierres). Por clase y estrato: n, mediana, p90 (de
  `percentil_deslizamiento_f17`), máximo, `sin_tick`, fuera de ventana; y el veredicto de D3.
  Imprime solo puntos y recuentos.
- **grabador**: el spread (ASK − BID, en puntos) por hora de la ventana en los días grabados, con
  p50, p90 y p99 de `percentil` y el máximo; y los recuentos de ticks y de horas. Nada más (D5: la
  comparación con Dukascopy no es de esta rama).
- Los dos validan los manifiestos de D7 (`validar_manifiesto_ordenes`, `validar_manifiesto_grabador`).

### 1.4 Los topes (D4), cada uno desde la cuenta y su historial

Constantes del `.mq5`, que un test compara con las del runbook. Cada ciclo, antes de colocar:

- **(a) Peor caso ≤ 1.000 USD** (`TOPE_PEOR_CASO_USD`): `PeorCaso` sobre TODO lo vivo del número
  mágico leído de la terminal (`OrdersTotal` y `PositionsTotal`, no de una variable) más la orden
  que se va a colocar, con `OrderCalcProfit(ORDER_TYPE_BUY o ORDER_TYPE_SELL)` según el lado: la
  venta pierde hacia arriba, `precio + (stop + P8_DESLIZ)`. Si con el stop de 18 puntos no cabe, el
  ciclo no se hace (decisión 2).
- **(b) Diario**: el saldo al empezar el día de riesgo se rehace del historial de la cuenta
  (`saldo − Σ (DEAL_PROFIT + DEAL_COMMISSION + DEAL_SWAP + DEAL_FEE)` de los deals desde ese
  instante); para si la equity baja de ese saldo menos `TOPE_DIA_USD` (3.000). Con el peor caso de
  (a) vivo, como mucho 4.000 de los 5.000 de R2. Es de toda la cuenta, no solo del número mágico,
  porque la regla de FTMO lo es (más estricto que lo escrito en D4).
- **(c) Total**: para si la equity baja del capital inicial menos `TOPE_TOTAL_USD` (8.000). El capital
  inicial, del historial: la suma de los deals `DEAL_TYPE_BALANCE` (si no es `CAPITAL_INICIAL` =
  100.000, el perfil de la cuenta, el script se niega: no adivina).
- **(d) Peticiones**: las del día de riesgo, contadas del historial del número mágico (cada orden
  cuenta una; una `ORDER_STATE_CANCELED`, otra más por su borrado; una caducada, no) más las
  `peticion` rechazadas que escribió el propio script en sus CSV de ese día (0.3: no se sabe si una
  rechazada entra en el historial; decisión 4). Para en `TOPE_PETICIONES` (500). La pausa,
  `PAUSA_MS` = 1.500, constante.
- **(e) El cierre de la sesión**: no coloca nada si faltan menos de `MARGEN_CIERRE_MIN` (150) minutos
  para el fin de la sesión de hoy de `SymbolInfoSessionTrade`, en la hora del servidor de
  `TimeCurrent` (la documentación no dice el huso: la capa lo da por servidor, `Sesiones.mqh`:6-9;
  el runbook y la primera ejecución lo contrastan con la ficha de MT5). Y el runbook: no se lanza un
  día con cierre anunciado por FTMO ni el hábil anterior.

Cada tope que salta escribe su fila `tope`, `Limpiar("tope_<x>")` y termina; con `quedan` ≠ 0, la
fila lo grita y `Alert`, como `MedirDemoFTMO`. Relanzado el mismo día, (a) a (d) dan lo mismo porque
se leen de la cuenta y de su historial, no de lo que recuerde el script.

### 1.5 Cuándo empieza el día de riesgo (decisión 3)

Lo que se sabe: el límite diario se restablece a las 00:00 de España (R2; DEMO-FTMO.md:158-166), y
el servidor va 120 minutos por delante de UTC con el cambio de hora de EE. UU. (A-28 DECIDIDA,
ADR-0090 §1). **Medido con zoneinfo** (un guion en la carpeta de trabajo, fuera del repo, con
`America/New_York` para el servidor y `Europe/Madrid`), día a día de 2026 a 2030: la medianoche de
España cae a las **01:00 del servidor 1.707 días y a las 02:00 119 días** (las semanas en que EE. UU.
y la UE no han cambiado de hora a la vez), siempre en el mismo día del servidor.

**Propuesta: que no haga falta saber cuál de las dos es.** El script no coloca nada ni tiene nada
abierto entre las 22:00 y las 03:00 del servidor (`TimeCurrent`, formado en el servidor, 0.3). Así
ningún deal cae entre las dos medianoches, y el saldo a las 00:00 del servidor es el mismo que a
las 00:00 de España: el día de riesgo se cuenta desde las 00:00 del servidor con `HistorySelect`,
que va en hora del servidor (0.3), sin ninguna cifra de huso en el script. Un test en Python
comprueba con zoneinfo (`broker_offset_base`, `broker_dst` y `huso_operativa` del registro) que, de
2026 a 2030, la medianoche de España cae siempre en `[00:00, 03:00)` del servidor, a los dos lados
de cada cambio de hora de la UE y de EE. UU.; y otro, que las dos constantes del `.mq5` son esas.
La ventana del bot (07:00-15:00 España, 08:00-16:00 o 09:00-17:00 del servidor) queda dentro.

### 1.6 El manifiesto (D7)

`data/manifests/f17-ordenes/<dataset_id>.yaml` y `data/manifests/f17-grabador/<dataset_id>.yaml`,
uno por ejecución congelada, con esquemas `schema_f17_ordenes: 1` y `schema_f17_grabador: 1`
escritos en `data/manifests/README.md`: `dataset_id` (`f17-ordenes-<AAAA-MM-DD>-<8 hex>` y
`f17-grabador-<AAAA-MM-DD>-<8 hex>`, el sufijo como en el historial), `ficheros` (ruta, tipo,
sha256, bytes, filas, fin de línea), `dias` (los días que cubre, por recuento), `script` (nombre y
versión), `estrato` (solo ordenes), `control` (los relojes de su CSV y si cuadra con el registro),
`cuenta` (DEMO), `declarado_por`, `congelado_el`, `rama` e `informe`. Su test, sobre un manifiesto
sintético en un temporal, rompe cada regla a propósito.

### 1.7 La compilación (D8)

Por el camino `herramienta`, sin cambiar `compilar.py`. Tras la revisión del diff por el consultor,
Aleks lanza con «!» el comando de D8 tal cual. Si la guardia niega a la sesión compilar, no se rodea.

### 1.8 El borrador de `docs/plan/F17-ORDENES.yaml` (D3)

No se escribe en el repo hasta la respuesta. Las cifras:

```yaml
schema_f17_ordenes_criterio: 1
escrito_el: <fecha de la respuesta>   # antes de cualquier llenado
regla: ADR-0092 §4            # la mediana y el percentil; no cambia
referencia: ADR-0099 §5       # el precio del llenado menos el del tick que dispara
precisiones_nuevas: >-        # escritas antes de cualquier dato; ningun ADR las escribe
  la referencia de un cierre a mercado; el estrato «uno»; sin_tick; los tamaños; que estrato vale
clases: [entrada_stop, cierre_stop, cierre_mercado]
signo: mas_en_contra
tick_que_dispara:
  desde: {entrada_stop: puesta de la orden, cierre_stop: deal de entrada}   # excluido
  hasta: el llenado                                                           # incluido
  al_colocar: se cuenta aparte, no entra en la mediana ni en sin_tick         # decision 8
  lado: {compra: ask, venta: bid}
  toca: {compra: ask >= nivel, venta: bid <= nivel}
cierre_mercado_referencia: cotizacion del lado que ejecuta leida justo antes de pedirlo
sin_tick:
  entra_en_la_mediana: false
  fraccion_maxima_por_clase: "0.05"      # con mas, la clase no da veredicto
estadistico:
  mediana: rango mas cercano (leer_historial_f17.percentil)
  percentil: criterio_fidelidad.yaml#percentil_deslizamiento_f17
estratos:
  uno: {lotes: "1.00", minimo_por_clase: 100}
  bot: {lotes: ADR-0081 D2 en vivo, minimo_por_clase: 30, se_usa: maximo}
que_estrato_vale:
  si_mediana_bot_no_pasa_de_uno: {mediana: uno, percentil: max(p90 uno, maximo bot)}
  si_la_pasa_en_1_punto_o_mas: {vale: bot, insuficiente_hasta: 100}
ventana: [ventana_inicio, ventana_fin]   # instante UTC del llenado, por la rejilla; sin calendario de cierres
fuera_de_ventana: se cuenta aparte
como_entra_en_adr_0092: no lo decide esta rama (ADR de Aleks que resuelva C, o la rama que la lea); deslizamiento sigue pendiente_F17
lo_que_no_dice: que la prueba gratuita ejecute como el Challenge y la cuenta real (P4-08)
spread_del_grabador: si el historial no cubre, la regla de comparacion se escribe antes de leer el grabador
lo_visto_antes:   # ADR-0090 §7 (dice «siete»; enumera nueve valores, tres por ejecucion)
  buy_stop_llenado_menos_nivel: {lotes: volumen minimo (0,01), valores: [+1, 0, 0]}
  mercado_llenado_menos_cotizacion_previa:
    ejecucion_1: {lotes: 0,01, apertura: +2, cierre: -2}
    ejecuciones_2_y_3: {lotes: 1,00, apertura: [+2, 0], cierre: [0, 0]}
parametros_del_guion: {stop_puntos: 18, t_salida_s: 300, espera_llenado_s: 120, distancia_entrada_puntos: 5}
```

**Una corrección del encargo, con su porqué** (hallazgo 1 del auditor, afirmación 31; comprobado en
ADR-0090:231-236): «las siete observaciones de ADR-0090 §7, con la referencia vieja (llenado menos
nivel) y 0,01 lotes o el volumen mínimo» no es lo que dice el ADR. El ADR escribe «siete» pero
enumera **nueve valores**; solo los **tres de la buy stop** son llenado menos nivel (con el volumen
mínimo); los **seis a mercado** son el llenado menos la cotización leída antes de pedirlo
(`MedirDemoFTMO.mq5`:650-651 y :666-667), **dos con 0,01 lotes (la 1) y cuatro con 1,00 (la 2 y la
3)**. Como el yaml se fija por su sha y no cambia tras la respuesta, va con la lista medida. Y los
seis a mercado son ya la referencia de un cierre a mercado que el encargo llama «pieza nueva»: ningún
ADR la escribe como regla, pero el paso 6 la usa desde la 1.1 (afirmación 32; el yaml lo dice).

## Lo que necesito que decidas

0. **La distancia del stop y el tiempo de salida (D1).** Opciones: (a) stop a 18 puntos (la mediana
   de D, `premisa.txt`:67) y T = 300 s; (b) antes de fijar T, medir p sobre la M1 de construcción
   (velas, no holdout) con su fila de HOLDOUT, y fijar T para p ≈ 0,5. Recomiendo (a): el número de
   ciclos depende de mín(p, 1 − p) y con p entre 0,3 y 0,6 la aritmética no cambia más que un 30 %;
   la primera prueba mide p de verdad. Coste de (b): un guion más en la rama y su exposición, para
   afinar un supuesto que la primera prueba reemplaza.
1. **Cómo comprueba el test las constantes del lote** (0,005, 0,95, 18). Opciones: (a) el test lee
   `riesgo_por_operacion` y `lote_margen_libre_fraccion` del registro y el 18 del yaml de D3, y las
   compara con el `.mq5`; (b) el `.mq5` las lleva como `input`. Recomiendo (a): un `input` deja
   cambiar el lote al lanzarlo. Coste de (b): ninguno de código, pero el estrato «bot» dejaría de
   ser el lote del bot si alguien teclea otro número.
2. **Si con el lote del bot no cabe el stop de 18 en el tope de 1.000 USD** (precio por debajo de
   ~1,09, 0.4). Opciones: (a) se baja el lote hasta que quepa (el estrato sigue siendo «del orden de
   los del bot», y la fila lo dice); (b) el ciclo no se hace (D4 (a) al pie de la letra: «si el
   tope no deja el stop mínimo, el ciclo no se hace»). Recomiendo (a), porque con (b) un precio de
   1,08 dejaría sin estrato «bot» toda la prueba; D4 (a) habla del stop MÍNIMO, y aquí el stop es
   fijo. Coste de (a): el lote «bot» depende del precio y no siempre es el de D2 (se escribe cada
   vez).
3. **El inicio del día de riesgo** (D4 b). Opciones: (a) la ventana muerta de 22:00 a 03:00 del
   servidor (1.5), sin cifras de huso en el script, con un test en Python contra zoneinfo; (b) lo
   que pide D4: `TimeGMT` y la regla de la UE escrita en el script, con tests a los dos lados.
   Recomiendo (a): (b) depende del reloj del ordenador (`TimeGMT`, 0.3) y las reglas de cambio de
   hora escritas en MQL5 no se pueden probar con pytest (solo con un script de pruebas en el
   terminal, como `BotsitoPruebasCapa.mq5`); (a) es la regla conservadora de D4, pero exacta.
   Coste de (a): el script no opera en esas cinco horas, que están fuera de la ventana del bot.
4. **Las peticiones rechazadas en el recuento (d)**, que la documentación no dice si entran en el
   historial (0.3). Opciones: (a) historial más las rechazadas que el propio script escribió en sus
   CSV del día (relee sus ficheros al arrancar); (b) solo el historial, y un contador en memoria
   para la ejecución en curso. Recomiendo (a): vale igual tras relanzarlo, que es lo que pide D4.
   Coste de (a): el script lee sus propios CSV (`FileFindFirst("F17M_*.csv")`), unas 40 líneas más.
5. **Los topes (b) y (c) sobre toda la cuenta, no solo el número mágico.** Lo escrito en D4 es
   «calculado desde el historial de deals y órdenes de su número mágico»; la pérdida diaria y la
   total de FTMO son de la cuenta. Opciones: (a) la equity y el saldo de la cuenta, y el historial
   entero para el saldo al empezar el día; (b) solo el número mágico. Recomiendo (a): es lo que mide
   FTMO; si en la misma prueba corre otra cosa (el historial no opera; el grabador tampoco), (a) la
   cuenta. Coste de (b): con otra posición abierta a mano, el tope no la vería.
6. **El grabador: script (D2) o servicio.** Un servicio de MQL5 vuelve a arrancar solo al reiniciar
   el terminal (0.3), un script no. Opciones: (a) script, como dice D2, y Aleks lo relanza; (b)
   servicio, que pide cambiar `compilar.py` (que solo instala scripts) y por tanto `src/`. Recomiendo
   (a): D8 no cambia y el relanzado retoma sin hueco desde el servidor. Coste de (a): si el terminal
   se reinicia de noche, el hueco lo rellena el siguiente arranque mientras el servidor guarde esos
   ticks; si no los guarda, el control lo dice.
7. **Los dos estratos en la misma cuenta (R17).** R17 prohíbe abrir «substantially larger
   position sizes compared to your other simulated trades»: mezclar 1,00 y ~25 lotes en la misma
   cuenta es eso, en una prueba gratuita. Opciones: (a) seguir con los dos estratos y declararlo en el
   runbook; (b) un estrato por prueba. Recomiendo (a): (b) dobla las pruebas, y lo que FTMO haga con
   una prueba gratuita que incumpla R17 (R18: desde quitar operaciones hasta cerrar el acceso) no
   está escrito en el repo. Coste de (a): si cierra la prueba, se pierde lo que quedara de ella; la
   pregunta, si Aleks quiere, va a FTMO antes (A.2). Lo encontró el auditor (H5): el encargo cita
   R16 y no R17.
8. **La distancia de la entrada y las que se llenan al colocarlas** (hallazgo 3 del auditor). En la
   ejecución 3, la buy stop y la sell stop puestas en el nivel exacto se llenaron al instante
   (ADR-0090:168-173): con el stops level 0, una stop a 2 puntos puede llegar al servidor con el
   precio ya pasado, y entonces el tick que la dispara es ANTERIOR a su puesta y la muestra no tiene
   el tick de D3. Opciones: (a) `DISTANCIA_ENTRADA` = 5 puntos, y las que se llenen con la cotización
   ya pasada se cuentan aparte como `al_colocar`, fuera de la mediana y de la cuenta del 5 % de
   `sin_tick` (es otra cosa: un llenado a mercado, no una stop que salta); (b) 2 puntos («tan cerca
   como deje el servidor», D1) y que esas cuenten como `sin_tick`. Recomiendo (a): con (b) la clase
   de entradas puede pasar del 5 % de `sin_tick` y quedarse sin veredicto por un efecto que no es el
   que se mide; 5 puntos siguen siendo «cerca» frente al stop de 18. Coste de (a): las entradas
   tardan algo más en llenarse (sin medir; la espera es de 120 s y la que no se llena se borra, una
   petición más).
9. **Los bordes de la búsqueda del tick que dispara.** El simulador busca en `(desde, hasta)`, con
   los dos bordes fuera (`llenado.py`:233-236), y `CopyTicksRange` da los dos dentro (0.3); y el stop
   de una posición lo busca desde el llenado (afirmación 33 del auditor). Opciones: (a) en
   `(puesta, llenado]`: la puesta fuera, como el simulador; el llenado dentro, porque el tick que llena
   puede compartir milisegundo con el deal; y para el cierre por stop, la puesta es el deal de entrada,
   que es desde donde lo busca el simulador; (b) `[puesta, llenado]`, los dos dentro. Recomiendo (a):
   es la convención del simulador, que es lo que el deslizamiento corrige. Coste de (a): un tick en el
   mismo milisegundo que la puesta no cuenta (con 5 puntos de distancia, raro).

## Respuesta del consultor a la PARADA (2026-11-26)

Copiada tal cual (también al final del encargo):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA de `trabajo/f17-ordenes` (2026-11-26, 14:20, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA, y al final del encargo.
>
> La fase 0 cumple y corrige al encargo; acepto sus correcciones. Errores del consultor, para la fila de ERRORES-RECURRENTES: (1) «las siete observaciones de ADR-0090 §7 ... 0,01 lotes» copiado del ADR sin contar la lista (son nueve, tres llenado menos nivel y seis a mercado, cuatro con 1,00 lote); (2) R17 no citado, solo R16; (3) `OrderCalcMargin` pedido sin decir el tipo de orden, con la tasa 0;0 de la stop ya escrita en ADR-0090; (4) «tan cerca como deje el servidor» sin mirar los llenados al colocar de la ejecución 3 (ADR-0090:168-173). Menores: las 2 h 30 min atribuidas a R15 (son un margen del encargo); los festivos citados en ADR-0068 §4 (están en «Alternativas», 2); la fila F:F17 situada en el «Marcador» (está en «F01-F35 · Estado medido»). Lección: lo que el consultor copia de un ADR también se cuenta y se cruza con el resto del ADR antes de escribirlo.
>
> 0. Stop a 18 puntos y salida a mercado a los 300 s, opción (a). La primera prueba mide p y el coste por ciclo de verdad; el runbook dice que el plan de las pruebas siguientes se rehace con esas medidas, y da las dos estimaciones (la tuya, con el supuesto de martingala, y la del auditor, unos 20 ciclos «bot» por prueba), las dos como supuestos.
> 1. (a): constantes fijas en el `.mq5`, con el test que las compara con `riesgo_por_operacion` y `lote_margen_libre_fraccion` del registro y con el 18 del yaml. Un `input` dejaría cambiar el estrato al lanzarlo.
> 2. (a), con un control: el guion baja el lote hasta que quepa en el tope de 1.000 USD y escribe en la fila el lote usado y el lote de ADR-0081 D2 de ese momento. El lector cuenta la muestra como «bot» solo si el lote usado es al menos el 90 % del de D2; si no, la cuenta aparte como `bot_reducido`, fuera de los dos estratos. El yaml lo dice. Por qué: con un precio normal, la rebaja es de pocos puntos porcentuales y el estrato sigue siendo el lote del bot; el 90 % impide que deje de serlo sin que se vea.
> 3. (a): la ventana muerta de 22:00 a 03:00 del servidor, sin cifras de huso en el guion, con el test de zoneinfo de 2026 a 2030 a los dos lados de cada cambio de hora. Añade al test que, a las 22:00 del servidor, el guion no tiene nada abierto ni pendiente (lo comprueba el contrato en el texto, como los demás topes), porque la igualdad de los dos saldos depende de eso. `TimeGMT` depende del reloj del ordenador y no se puede probar con pytest.
> 4. (a): historial más las rechazadas de sus propios CSV del día. Vale igual tras relanzarlo, que es lo que pide D4.
> 5. (a): los topes (b) y (c) sobre la equity y el saldo de toda la cuenta, porque así cuenta FTMO. El runbook dice además que, mientras corre la medida, en esa cuenta no opera nada más (el exportador y el grabador solo leen).
> 6. (a): script, como dice D2. El runbook dice cómo se relanza y que el control declara el hueco si el servidor ya no guarda esos ticks.
> 7. (a): los dos estratos en la misma cuenta, alternados, que es lo que hace comparables las medianas, y declarado en el runbook. Con una condición nueva, que amplía el alcance y por eso lo digo: Aleks preguntó a FTMO por correo el 2026-11-26 si la prueba gratuita ejecuta como el Challenge y la cuenta real (P4-08) y si medir con un guion propio, con 1 lote y unos 25 lotes, es práctica prohibida o hiperactividad o afecta a un Challenge futuro (R13, R16 y R17). El runbook dice que la medida (no el historial ni el grabador) no se lanza hasta que FTMO conteste. Si la respuesta dice que mezclar los dos tamaños incumple R17, la opción es (b), un estrato por prueba; y si dice que la medida está prohibida, no se corre. En los dos casos, PARADA al consultor en la rama de la prueba. La respuesta entra parafraseada, nunca literal, por esa rama o por la orden de cierre de esta, lo que llegue antes. Copia el correo literal en el informe, en un recuadro como el de FTMO-REGLAS.md:174-179, con este encabezado: «Correo LITERAL de Aleks a soporte de FTMO (2026-11-26). Fuente escrita: correo de abriosotapia@gmail.com a support@ftmo.com, enviado el 2026-11-26 en un hilo nuevo, con el asunto «Question on Free Trial execution conditions and measuring order execution with my own MQL5 script (Swing, MT5)». Respuesta pendiente.», y este texto, tal cual:
>
> > Hello,
> >
> > I am preparing an FTMO 2-Step Swing account (100,000 USD, MT5) for my own automated EURUSD strategy. Before buying the Challenge, I would like to measure in a Free Trial how my orders are executed, and I have two questions so that I do it correctly.
> >
> > 1. Does the Free Trial execute orders under the same conditions as the paid FTMO Challenge and the FTMO Account? In particular: the same spreads, the same commission, the same execution and slippage of buy stop and sell stop orders and of stop losses, and the same margin rates. If any of these differ, could you tell me which ones?
> >
> > 2. Is it allowed, in a Free Trial, to run my own MQL5 script that measures execution? The script would place one buy stop or sell stop order close to the current price, and once it is filled, close the position either by its stop loss or at market after a short time. It would repeat this a few hundred times over the 14 days, only on EURUSD and only during European trading hours. It would keep at least 1.5 seconds between trading requests, stay below 500 trading requests per day, and never have more than a few orders open at the same time. Most cycles would use 1 lot, and some would use the lot size of my strategy (around 25 lots). Every position would have a stop loss, and the script would stop itself well before the daily or maximum loss limits. Would this be considered a forbidden trading practice or hyperactivity, and could it affect a future paid Challenge on my account?
> >
> > Thank you in advance for your help.
> >
> > Best regards,
> > Alex
>
>    Para el cierre, en las líneas de la hoja: la A.2 nombra esta pregunta como pendiente, sin recuentos (HOJA:12-13).
> 8. (a): `DISTANCIA_ENTRADA` de 5 puntos, y las que se llenan con la cotización ya pasada se cuentan aparte como `al_colocar`, fuera de la mediana y fuera del 5 % de `sin_tick`. Son un llenado a mercado, no una stop que salta.
> 9. (a): la búsqueda va en `(puesta, llenado]`, con la puesta fuera, como el simulador, y el llenado dentro. Para el cierre por stop, la puesta es el deal de entrada.
>
> Y en el yaml: «Lo visto antes» con la lista medida (las nueve, con su referencia y sus lotes); y en «Qué estrato vale», la precisión de 0.4 escrita así: con el R de 18 puntos de `premisa.txt`:67, ±0,05 R son ±0,9 puntos, y 1 punto son 0,056 R, así que la regla de «1 punto o más» se mantiene. El yaml se commitea primero, fijado por su sha, antes del código que lo lee.
>
> Después: el código y los tests de D1 a D9 tal como quedan con esto, cada test que rompe a propósito con su prueba contra `main` (skill `comparar-con-main`), la fila de HOLDOUT de cada día antes de su primer `make check`, y el diff de los dos `.mq5` en la entrega, para que lo revise el consultor. El comando de compilar con «!» lo da el consultor en un mensaje aparte, después de esa revisión (ERRORES-RECURRENTES.md:136). Luego, la CI de `fix/f17-ordenes` sobre el último commit (el número del run, con el único fallo esperado de `state check`), el revisor con los alcances de §7 más los puntos 2, 3 y 7 de esta respuesta, y termina con «Rama lista para revisión, NO cerrada.»

### El correo a FTMO del punto 7

> **Correo LITERAL de Aleks a soporte de FTMO (2026-11-26).** Fuente escrita: correo de
> `abriosotapia@gmail.com` a `support@ftmo.com`, enviado el **2026-11-26** en un hilo nuevo, con
> el asunto «Question on Free Trial execution conditions and measuring order execution with my
> own MQL5 script (Swing, MT5)». **Respuesta pendiente.** El texto lo copia el consultor en su
> respuesta a la PARADA (punto 7), y aquí va tal cual:
>
> Hello,
>
> I am preparing an FTMO 2-Step Swing account (100,000 USD, MT5) for my own automated EURUSD strategy. Before buying the Challenge, I would like to measure in a Free Trial how my orders are executed, and I have two questions so that I do it correctly.
>
> 1. Does the Free Trial execute orders under the same conditions as the paid FTMO Challenge and the FTMO Account? In particular: the same spreads, the same commission, the same execution and slippage of buy stop and sell stop orders and of stop losses, and the same margin rates. If any of these differ, could you tell me which ones?
>
> 2. Is it allowed, in a Free Trial, to run my own MQL5 script that measures execution? The script would place one buy stop or sell stop order close to the current price, and once it is filled, close the position either by its stop loss or at market after a short time. It would repeat this a few hundred times over the 14 days, only on EURUSD and only during European trading hours. It would keep at least 1.5 seconds between trading requests, stay below 500 trading requests per day, and never have more than a few orders open at the same time. Most cycles would use 1 lot, and some would use the lot size of my strategy (around 25 lots). Every position would have a stop loss, and the script would stop itself well before the daily or maximum loss limits. Would this be considered a forbidden trading practice or hyperactivity, and could it affect a future paid Challenge on my account?
>
> Thank you in advance for your help.
>
> Best regards,
> Alex

## El encargo frente al repo (auditor-encargo, 0.5)

El subagente `auditor-encargo` comprobó 73 afirmaciones: 58 correctas, 1 incorrecta y 14 con matiz,
y 9 cosas que el repo pide y el encargo no dice. Lo que la sesión comprobó y cómo entra:

| # | qué | cómo entra |
|---|---|---|
| 31 (INCORRECTA) | «las siete observaciones de ADR-0090 §7 ... 0,01 lotes»: son nueve valores, tres llenado menos nivel y seis a mercado, cuatro con 1,00 lote | comprobado en ADR-0090:231-236; el borrador del yaml (1.8) va con la lista medida |
| 28 (MATIZ) | `OrderCalcMargin` con el tipo stop da 0 en esta prueba (tasa 0;0) | comprobado en DEMO-EJECUCIONES-2-3.md:84-86; 1.1 lo pide con BUY o SELL al mercado |
| 39 (MATIZ) | las stops cerca del precio se llenaron al instante en la 3 | comprobado en ADR-0090:168-173; decisión 8 |
| 33 (MATIZ) | el simulador excluye los bordes y busca el stop desde el llenado | comprobado en `llenado.py`:233-236; decisión 9 |
| 6 (MATIZ) | el cálculo de llenado menos nivel está en la :739, no en la :735 | 0.2 cita la :739 |
| 3 (MATIZ) | si salen dos lectores, el contrato crece | sale uno con dos formas (1.3) |
| 32 (MATIZ) | la referencia de un cierre a mercado ya la usa el paso 6 | 1.8 lo dice |
| 38 (MATIZ) | las 30 de «bot» solo valen para la cota del máximo; P4-06 da 100-400 por clase | es lo que D3 hace con «bot» (su máximo), sin cambio |
| 43, 71 (MATIZ) | con ~25 lotes el stop máximo en el tope es de 19-20 puntos; 18 cabe por poco; y el auditor estima unos 20 ciclos «bot» por prueba (cuenta el coste de un ciclo que sale por stop, ~575 USD, y de uno a mercado, ~175) | 0.4 da 964 USD con 25,37 lotes; la diferencia en ciclos es el supuesto de martingala de 0.4, que no está medido: con el del auditor, 30 por clase piden unas 3 pruebas y 100 unas 10. La primera prueba lo mide |
| 49 (MATIZ) | las 2 h 30 min no salen de R15 (dos horas o menos, y solo antes de un cierre de dos horas o más; la pausa diaria es de 10 minutos) | es un margen del encargo: el runbook y el script lo dicen así |
| 50 (MATIZ) | lo de los festivos está en ADR-0068, «Alternativas», 2 (:117-118), no en §4 | se cita así |
| 55 (MATIZ) | en F39p lo de otro mes se descartaba sin leerlo; aquí los lectores no filtran por mes | es lo que dice D6; la fila del día que corran lo declara por recuento |
| 58 (MATIZ) | el comando de F39p está en `docs/validation/F17-HISTORIAL.md`:588 | se cita así |
| 61 (MATIZ) | PROJECT_STATE pesa 24.131 en `main` y 24.220 en la rama | las líneas del cierre se miden contra `main` |
| 63 (MATIZ) | la fila F:F17 está en «## F01-F35 · Estado medido» (HOJA:925), no en el «## Marcador» | se cita así en las líneas del cierre |
| H1 | el desfase servidor-UTC en cada evento del grabador (MASTER_PLAN.md:285) | 1.2: por hora, en el control |
| H2 | usar ticks de FTMO como fuente de una medida pide un ADR que enmiende ADR-0005 y ADR-0024 §4 (ADR-0099:164-165) | el yaml y el runbook lo dicen para el spread del grabador |
| H3 | comportamientos de MT5 fuera de la lista de 0.3 | la segunda tanda del `web-fetch` los leyó (0.3); lo que no está documentado queda POR MEDIR en el runbook |
| H4 | la hoja de ruta no admite recuentos («Se nombran ids, nunca recuentos que caducan», HOJA:12-13) | las líneas del cierre de la A.5 no dirán «cuántas pruebas» con un número: remiten al runbook |
| H5 | R17 | decisión 7 |
| H6 | en una subcarpeta de `data/manifests/` solo van `.yaml` (y README, `_*`), y es inmutable | D7 lo respeta: las carpetas nacen con su primer manifiesto, en la rama de la prueba |
| H7 | el comando para «!» va en un mensaje aparte, tras la respuesta (ERRORES-RECURRENTES.md:136) | así se hará en D8 |
| H8 | `herramienta` exige el `.mq5` en el índice de git | D8: se compila lo commiteado |
| H9 | desde dónde empieza el grabador sin CSV | 1.2: desde el inicio de la hora en que se lanza |

## 2. Lo hecho tras la respuesta

### 2.1 El criterio de D3, primero y fijado por su sha

`docs/plan/F17-ORDENES.yaml`, escrito con la respuesta (puntos 0, 2, 8 y 9, y «Y en el yaml»)
ANTES de cualquier llenado (no hay ninguno: la medida no ha corrido) y commiteado antes del código
que lo lee, fijado por su sha256 `3d453e901a77ed698e702b4388c189757d09e48f7c4fa91717443a34f8d8ba84`
en `tests/unit/test_f17_ordenes_criterio.py` (seis tests: el sha, LF, las cifras, el percentil que
nombra, una cifra cambiada que rompe y «siete en vez de nueve» que rompe). Lo que lleva de la
respuesta: «lo visto antes» con los nueve valores de ADR-0090 §7, con su referencia y sus lotes;
`bot_reducido` por debajo del 90 % del lote de D2 (punto 2); `al_colocar` fuera de la mediana y del
5 % de `sin_tick` (punto 8); la búsqueda en `(puesta, llenado]` (punto 9); y la precisión de «Qué
estrato vale» con el R de 18 puntos, con la frase de la respuesta.

## Estado

EN CURSO: la respuesta a la PARADA aplicada en el criterio de D3 (2.1); viene el código de D1 a D9.
