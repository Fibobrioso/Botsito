# F17-ORDENES · La medida de las órdenes stop y el grabador de ticks de la demo de FTMO, con sus herramientas y sin correr (R4.7, entrada F)

> PLANTILLA: informe de la rama `trabajo/f17-ordenes`. Estado: EN CURSO (arreglos del revisor hechos; falta recompilar y la CI del último commit). La fase 0 y su
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

### 2.2 El código y los tests de D1 a D9

| pieza | fichero | tests |
|---|---|---|
| D1 y D4, el guion que coloca órdenes | `tools/mql5/MedirOrdenesFTMO.mq5` (1.0) | `tests/contract/test_medir_ordenes_ftmo.py` |
| D2, el grabador | `tools/mql5/GrabarTicksFTMO.mq5` (1.0) | `tests/contract/test_grabar_ticks_ftmo.py` |
| D5, los lectores (uno, con `medida` y `grabador`) | `scripts/leer_ordenes_f17.py` | `tests/unit/test_leer_ordenes_f17.py` |
| D7, los manifiestos | `data/manifests/README.md` (los dos esquemas) y `validar_manifiesto` del lector | `tests/unit/test_manifiestos_f17_ordenes.py` |
| D7, el runbook | `docs/runbooks/F17-ORDENES.md`; una línea en `F17-HISTORIAL.md`; el índice | (las constantes de la tabla, en el contrato del guion) |
| los README | `scripts/README.md`, `tools/mql5/README.md` | — |

Cómo entra cada punto de la respuesta:

- **0.** `STOP_PUNTOS` 18 y `SALIDA_A_MERCADO_S` 300, del bloque `guion` del yaml, comparadas por el
  contrato; el runbook da las dos estimaciones como SUPUESTOS y dice que el plan se rehace con la
  primera prueba.
- **1.** Las constantes del lote (`RIESGO_FRACCION` 0,005, `MARGEN_LIBRE_FRACCION` 0,95) y las del
  criterio son `#define`, comparadas con `riesgo_por_operacion` (porcentaje) y
  `lote_margen_libre_fraccion` del registro y con el yaml; las únicas entradas son `InpEstrato` e
  `InpCiclos` (el contrato rompe con cualquier otra).
- **2.** `Ciclo` baja el lote, de paso en paso, hasta que el peor caso cabe en 1.000 USD, y la fila
  lleva `lotes` (el usado) y `lote_d2` (el de ADR-0081 D2 de ese momento); el lector cuenta
  `bot_reducido` por debajo del 90 %. El margen de 1 lote, con `OrderCalcMargin(ORDER_TYPE_BUY` o
  `ORDER_TYPE_SELL)` a mercado (el contrato rompe con un tipo pendiente).
- **3.** `EnHoraMuerta`: de `HORA_MUERTA_DESDE` (22) a `HORA_MUERTA_HASTA` (3) del servidor, con
  `TimeCurrent`. `PuedeEmpezarCiclo` no coloca si el ciclo, en su duración máxima
  (`DURACION_MAXIMA_CICLO_S`, 120 + 300 + 60 s), puede llegar a ella, y `HayQueCortar` cierra en las
  dos esperas al entrar: así a las 22:00 no hay nada abierto ni pendiente (lo comprueba el contrato en
  el texto, con tres mutaciones). El test de zoneinfo, de 2026 a 2030 y con `RelojServidor` del
  registro: la medianoche de `huso_operativa` cae siempre en `[00:00, 03:00)` del mismo día del
  servidor, la ventana del bot nunca toca la ventana muerta, los dos lados de cada cambio de hora
  aparecen (la 01:00 y las 02:00), y una ventana más corta rompe.
- **4.** `PeticionesDelDia`: las órdenes del número mágico con `ORDER_REASON_EXPERT` desde las 00:00
  del servidor (la que crea el servidor al saltar un stop no es una petición), una más por cada
  borrada, las vivas, las rechazadas de los CSV de hoy de ejecuciones anteriores (`RechazadasDeHoy`,
  al arrancar) y las de esta; `Pedir` escribe cada petición antes de la siguiente, como `peticion` o
  `peticion_rechazada`, y duerme `PAUSA_MS`.
- **5.** `SaldoAlEmpezarElDia` rehace el saldo de las 00:00 del servidor con los deals de TODA la
  cuenta; `CapitalDelHistorial`, la suma de los `DEAL_TYPE_BALANCE` (si no es 100.000, el guion se
  niega); el runbook dice que mientras corre la medida no opera nada más en la cuenta.
- **6.** El grabador es un script; el runbook dice cómo se relanza y que el control escribe HUECO si
  el servidor ya no da una hora.
- **7.** Los dos estratos en la misma cuenta, alternados; el runbook abre con «Antes de nada: la
  pregunta a FTMO»: la medida no se lanza hasta que FTMO conteste, y lo que pasa con cada respuesta.
- **8.** `DISTANCIA_ENTRADA_PUNTOS` 5; el guion guarda la cotización leída antes de colocar y los
  ticks desde ella, y el lector cuenta `al_colocar` aparte.
- **9.** `tick_que_dispara` busca en `(puesta, llenado]`; la puesta de un cierre por stop es el deal de
  entrada (`DEAL_TIME_MSC`), que el guion escribe en `puesta_msc`.

**Dos añadidos de la sesión, que el consultor revisa en el diff:** (i) toda pendiente lleva, además
del stop, un **objetivo de respaldo** a `3 × STOP_PUNTOS` (54 puntos), para que una posición no
quede abierta sin fin si el script muere; con 300 s de salida a mercado casi nunca salta, y si salta
sale `otro_TP` y el lector no la usa; (ii) el grabador **no reabre una hora ya cerrada** con un tick
tardío (la truncaría): lo cuenta en el control como `tick_tarde`.

Lo que se ensayó y cómo (CLAUDE.md, «Ensayos aislados»): el lector solo escribe su `--salida`, y sus
tests la escriben en el temporal de pytest; los `.mq5` no se pueden ejecutar fuera de MetaTrader:
los prueban sus contratos en el texto, y la compilación (D8) la lanza Aleks tras la revisión.

### 2.3 Los tests de la rama con el código de `main` (skill `comparar-con-main`)

Antes: `git status --short` con 13 líneas (lo de esta parte, sin commitear), `git branch --list`
con `main` y la rama, 176 tags, `git worktree list` solo con el repo. Un clon desacoplado,
`git worktree add --detach C:/cm/main main` (e8c20a80), con los cinco ficheros de test de la rama
copiados dentro, y en él:

- `uv run pytest tests/unit/test_leer_ordenes_f17.py tests/unit/test_manifiestos_f17_ordenes.py`:
  **no recogen** (`FileNotFoundError: ... scripts\leer_ordenes_f17.py`);
- `uv run pytest tests/contract/test_medir_ordenes_ftmo.py tests/contract/test_grabar_ticks_ftmo.py
  tests/unit/test_f17_ordenes_criterio.py`: **57 FAILED y 3 PASSED**. Los tres que pasan solo miran
  lo que `main` ya tiene: `test_la_condicion_demo_es_la_de_medir_demo_ftmo` (la :759 de
  `MedirDemoFTMO.mq5`) y los dos de zoneinfo que no leen el `.mq5`
  (`test_la_medida_tiene_los_dos_lados_de_cada_cambio_de_hora` y
  `test_una_ventana_muerta_mas_corta_rompe`, sobre `RelojServidor` y el registro).

En la rama, los mismos y sus vecinos (`test_leer_historial_f17.py`, `test_exportar_ticks_ftmo.py`,
`test_medir_demo_ftmo.py`, `test_f17_ordenes_criterio.py`): 148 PASSED, 0 FAILED. Después:
`git worktree remove --force C:/cm/main` (con `--force` por los tests copiados, sin seguir) y
`git worktree prune`; `git worktree list` solo con el repo, las mismas ramas, 176 tags, y en origin
solo `refs/heads/main`.

## 3. La revisión del consultor de los dos `.mq5` y del yaml (2026-11-26)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> REVISIÓN DEL CONSULTOR de los dos `.mq5` y del yaml de `trabajo/f17-ordenes` (2026-11-26, 16:20, hora de Lima). Cópiala tal cual al informe. El yaml de D3 queda como está.
>
> Los dos añadidos se quedan: (1) el objetivo de respaldo a 54 puntos, con su salida `otro_TP` fuera de las clases, porque acota una posición si el guion muere; (2) el grabador no reabre una hora cerrada y apunta `tick_tarde`, porque reabrirla truncaría el fichero.
>
> Arreglos antes de compilar, cada uno con su test (contrato en el texto, como los demás) y en un commit sellado:
>
> 1. IMPORTA · MedirOrdenesFTMO.mq5, `SaldoAlEmpezarElDia` (:481-496): resta todos los deals del día, también el `DEAL_TYPE_BALANCE` del depósito. El día en que se activa la prueba, el depósito de 100.000 está en el historial de hoy, el saldo al empezar el día sale ≈ 0 y el tope (b) queda en −3.000, así que no salta nunca, justo el día en que se piensa correr la medida. Arreglo: `movido` solo suma los deals de trading (`DEAL_TYPE_BUY` y `DEAL_TYPE_SELL`); un depósito u otro movimiento de saldo no es pérdida del día. El test exige que la función filtre por esos dos tipos. Lección para el revisor: un tope que se calcula del historial se prueba también el primer día de la cuenta.
> 2. IMPORTA · GrabarTicksFTMO.mq5, `SiguienteAlUltimo` y el bucle de `OnStart` (:265-274): al relanzarlo rehace desde el último `F17G_*.csv` que encuentre, sin límite. Con los CSV de una prueba anterior en `MQL5/Files`, bajaría semanas de ticks, como un exportador sin la guardia de meses de ExportarTicksFTMO. Arreglo: una constante `MAX_HORAS_REHACER` de 72 (cubre un fin de semana y una noche). Si la hora siguiente al último CSV está más atrás, no rehace nada, empieza como la primera vez y escribe en el control `hueco_largo` con las horas que faltan. El control apunta además `ACCOUNT_LOGIN` al empezar. Y el runbook: al empezar cada prueba, los `F17G_*` y `F17M_*` de la anterior se mueven a una carpeta propia antes de lanzar nada. Test: la constante existe, vale 72 y el bucle la usa.
> 3. MENOR · MedirOrdenesFTMO.mq5, `Comprobaciones`: si `SYMBOL_TRADE_STOPS_LEVEL` es mayor que `DISTANCIA_ENTRADA_PUNTOS`, el guion se niega al empezar y lo dice, en vez de gastar peticiones rechazadas ciclo tras ciclo.
> 4. MENOR · MedirOrdenesFTMO.mq5, `Ciclo` (:860-863): si la salida falta porque se paró el guion (`IsStopped`), la fila dice «parado por el usuario» y no «la posición no se pudo cerrar».
> 5. MENOR · GrabarTicksFTMO.mq5, `RehacerHora`: una hora sin ticks en sábado o domingo del servidor se apunta como `mercado_cerrado`, no como `HUECO`; el lector y el runbook las distinguen.
> 6. MENOR · runbook: los estratos van por ejecución (`InpEstrato`), así que el runbook reparte las ejecuciones «bot» entre los días y las horas de la ventana en que corre «uno», para que las medianas se comparen en las mismas condiciones (lo que pedía el punto 7 de la PARADA con «alternados»).
>
> Después: compilar con el comando que el consultor da en un mensaje aparte (Aleks lo lanza con «!»); los logs a los anexos y su commit; empujar `fix/f17-ordenes` para la CI (si el clasificador niega el push, lo lanza Aleks con «!») y darme el número del run; el revisor con los alcances de §7 más los puntos 2, 3 y 7 de la PARADA y los arreglos 1 y 2 de esta revisión; las líneas del cierre y la fila de ERRORES-RECURRENTES. Termina con «Rama lista para revisión, NO cerrada.»

### 3.1 Lo hecho con la revisión

Los dos añadidos se quedan. Cada arreglo, con su test en el contrato (en el texto, con su mutación
que rompe):

| arreglo | dónde | test |
|---|---|---|
| 1 · el saldo al empezar el día solo resta `DEAL_TYPE_BUY` y `DEAL_TYPE_SELL` | `SaldoAlEmpezarElDia` | el filtro, antes de sumar; dos mutaciones (sin filtro, filtro que no filtra) |
| 2 · `MAX_HORAS_REHACER` 72; más atrás, `hueco_largo` y como la primera vez; `login` en el control | `GrabarTicksFTMO.mq5`, `OnStart` | la constante vale 72 y el bucle la usa; cuatro mutaciones (500, sin la rama, sin empezar de nuevo, sin el login) |
| 3 · se niega si el stops level pasa de `DISTANCIA_ENTRADA_PUNTOS` | `Comprobaciones` | una mutación |
| 4 · «parado por el usuario» si falta la salida porque se paró | `Ciclo` | una mutación |
| 5 · una hora vacía de sábado o domingo, `mercado_cerrado` | `RehacerHora`; el lector la cuenta (`controles_del_grabador`) | una mutación; y un test del lector con HUECO, `mercado_cerrado`, `hueco_largo` y `tick_tarde` |
| 6 · los estratos repartidos en los mismos días y horas; mover los ficheros de la prueba anterior | `docs/runbooks/F17-ORDENES.md` | — |

Una precisión del arreglo 2: el control del grabador apunta el `login`, pero el CSV vive fuera de
git y ese número no se copia al manifiesto ni a ningún informe, porque el repositorio es público
(`DEMO-FTMO.md`, «La prueba de octubre de 2026»); lo dicen el runbook y el esquema de
`data/manifests/README.md`. Tests de la rama: 108 PASSED, 0 FAILED.

### 3.2 La compilación (D8)

Lanzada por Aleks con «!» el 2026-11-26, desde la raíz del repo, sobre los ficheros de `8178c600`,
con el comando de D8 tal cual, sin `--instalar`:

    tools/mql5/MedirOrdenesFTMO.mq5: PASA (0 errores, 0 avisos)
    tools/mql5/GrabarTicksFTMO.mq5: PASA (0 errores, 0 avisos)

Los logs, en `docs/validation/anexos/F17-ORDENES/MedirOrdenesFTMO.log` y `GrabarTicksFTMO.log`
(«Result: 0 errors, 0 warnings»). El sha256 de la fuente que cada log dice haber compilado es el
del fichero commiteado (`sha256sum`: `91fdda77…` y `46b229dc…`). El camino `herramienta` de
`compilar.py` no cambió (D8). El `.ex5` no se versiona; la instalación en el terminal
(`--instalar`) va con el runbook, en la rama de la prueba.

## 4. Lo hecho con los hallazgos del revisor

El revisor (opus, una pasada, con los alcances de §7 del encargo, los puntos 2, 3 y 7 de la PARADA y
los arreglos 1 y 2 de la revisión del consultor) sobre `24987139`: eje (a) 0 bloquea, 0 importa, 2
menor; eje (b) 0 bloquea, 4 importa, 3 menor. Su informe, pegado al final (§10). Lo hecho:

| # | hallazgo | lo hecho |
|---|---|---|
| a1 | el estado del informe, desfasado | cabecera y `## Estado` al día |
| a2 | el README decía que el lector valida los manifiestos, y el diseño y el código difieren en dos detalles | `scripts/README.md`: «su `validar_manifiesto` comprueba los esquemas en los tests (la CLI no lo llama)», también en la entrada de `leer_historial_f17.py`, que decía lo mismo; las dos diferencias, en las desviaciones (§6, 2) |
| b1 | el contrato llamaba a cada tope pero no comprobaba su comparación | el contrato exige cada comparación con su constante (`equity < saldo_dia - TOPE_DIA_USD` y `equity < CAPITAL_INICIAL - TOPE_TOTAL_USD` en `PuedeEmpezarCiclo` y en `HayQueCortar`, `peticiones + 3 > TOPE_PETICIONES`, `peor > TOPE_PEOR_CASO_USD`, `MARGEN_CIERRE_MIN * 60`), la suma de las rechazadas, el borrado contado, `ORDER_REASON_EXPERT`, `RechazadasDeHoy` al arrancar, `g_rechazadas++` y el bucle que baja el lote; con diez mutaciones nuevas, una por cada una que el revisor dio |
| b2 | faltaban las secciones de entrega | §5 a §9 |
| b3 | el lector leía una carpeta; el veredicto de D3 pide juntar días y pruebas | `leer_ordenes_f17.py` lee juntas todas las carpetas que se le den (`ficheros_de`), y los ticks de cada llenado junto a su CSV; test nuevo con dos carpetas y el mismo nombre de ticks en cada una; el runbook lo dice |
| b4 | la caducidad caía a GTC | `PonerCaducidad` siempre `ORDER_TIME_SPECIFIED`; `Comprobaciones` se niega si EURUSD no admite `SYMBOL_EXPIRATION_SPECIFIED`; el contrato rompe con `ORDER_TIME_GTC` en el fuente y sin la negativa |
| b5 | la salida a mercado iba a ≥305 s y las esperas no miraban los topes | la salida se cuenta desde que se ve el llenado, por `TimeLocal` (las esperas no dependen de que lleguen ticks); los ticks de la entrada se copian DESPUÉS de cerrar la posición; `DURACION_MAXIMA_CICLO_S` acota lo que está vivo (la espera del llenado, la de la salida y un minuto, que cubre las del historial) |
| b6 | una colocación rechazada seguía con el ciclo siguiente | la ejecución para, con su fila `colocacion_rechazada` |
| b7 | (i) el deal de salida se buscaba una vez; (ii) el de una pendiente llena al borrarla también; (iii) ticks desde 0 | `EsperarDealDeSalida` y `EsperarDealDeLaOrden`, hasta `ESPERA_HISTORIAL_MS` (10 s); sin puesta, los ticks desde la cotización previa, y `GuardarTicks` no pide nada desde 0; los datos de la salida se leen antes de escribir nada (lo que el revisor no pudo medir de la selección del historial en los argumentos); cada uno con su mutación |

Lo que el revisor no pudo medir de MT5 (las esperas por `TimeCurrent`, si `CopyTicksRange` bloquea,
`OrderSend` tras `IsStopped`, si FTMO-Demo admite `SYMBOL_EXPIRATION_SPECIFIED`, otros tipos de deal
que muevan el saldo) sigue sin medir y lo dice el runbook en «Lo que no se sabe de MetaTrader»; dos de
ellos ya no importan (las esperas van por `TimeLocal`, y sin caducidad el guion se niega).

**Los `.mq5` cambiaron tras la compilación de `24987139`** (b4 a b7): los logs de §3.2 son de la
versión anterior. Hace falta que el consultor revise el diff (`git diff 8178c600 -- tools/mql5/`) y
dé otra vez el comando de compilar, y que la CI corra sobre el último commit.

## 5. El encargo, punto por punto

| punto | qué pide | hecho | dónde |
|---|---|---|---|
| §0 | base, apertura, tramo R4, ningún ADR, lista blanca, lecciones | sí | «Base comprobada»; `contrato.yaml`; ningún ADR en el diff |
| §1 | las dos partes, hechas, probadas y compiladas, sin correr | sí (falta recompilar tras §4) | §2, §3, §4 |
| §2 | qué no cambia | sí: diff vacío (revisor, requisito 3) | §10 |
| §3 | fase 0: 0.1 a 0.5 | sí | §0 |
| §4 | PARADA | sí, y la respuesta tal cual | §1, «Lo que necesito que decidas», «Respuesta del consultor» |
| D1 | `MedirOrdenesFTMO.mq5` y su contrato | sí | §2.2, §3.1, §4 |
| D2 | `GrabarTicksFTMO.mq5`, de solo lectura | sí | §2.2, §3.1 |
| D3 | el yaml, antes de cualquier llenado, fijado por su sha | sí (`3d453e90`, commiteado antes que el lector) | §2.1 |
| D4 | los topes, del historial, con tests que rompen | sí (b1 reforzado) | §2.2, §4 |
| D5 | los lectores y sus tests | sí (uno, con dos formas; junta carpetas) | §2.2, §4 |
| D6 | holdout: no filtran por mes, no imprimen precios | sí | el lector; el runbook |
| D7 | los manifiestos fuera de `f17/`, el runbook, la línea en F17-HISTORIAL y el índice | sí | §2.2 |
| D8 | la compilación por `herramienta`, sin cambiar `compilar.py` | sí sobre `8178c600`; **pendiente la recompilación** tras §4 | §3.2 |
| D9 | la CI de `fix/f17-ordenes` | sí sobre `24987139` (run 45904547776); **pendiente sobre el último commit** | §9 |
| §6 | las líneas del cierre con sus bytes | sí | §7 |
| §7 | el informe, el revisor, «Rama lista para revisión, NO cerrada.» | el informe y el revisor sí; la frase, tras la recompilación y la CI | §10, `## Estado` |

## 6. Desviaciones

1. **Una lectura antes de su fila de HOLDOUT** (fase 0): las claves de `meses_reservados.yaml` y los
   nombres de primer nivel de `knowledge/cases/` se leyeron antes de escribir su fila; se declararon
   el mismo día, en la segunda fila del 2026-11-26 (ADR-0021 §4). Nada de dentro de `holdout/`.
2. **El código y el diseño de la PARADA difieren en dos detalles**, sin cambiar lo decidido: una sola
   `validar_manifiesto(doc, tipo)` en lugar de dos funciones; y el valor del punto con
   `OrderCalcProfit` de un punto (documentado: la moneda de la cuenta) en lugar de
   `SYMBOL_TRADE_TICK_VALUE / SYMBOL_TRADE_TICK_SIZE`. Y en las filas que no son de llenado, el valor
   va en la columna `motivo`.
3. **§2.2 decía más de lo que probaba el contrato** («cada tope con un test que rompe»): las
   comparaciones no tenían test (revisor, b1). Corregido en §4; queda dicho aquí.
4. **La compilación se repite**: los arreglos de §4 cambian los dos `.mq5` después de compilarlos.
5. **`git worktree remove --force`** en la prueba contra `main` (§2.3), por los tests copiados sin
   seguir; dicho allí.
6. **El informe del revisor** va pegado entero, con las rutas de «Ficheros» relativas a la raíz (las
   daba absolutas).
7. Nada se ensayó con datos reales: no existe ninguno (la medida y el grabador no han corrido); los
   lectores se prueban con CSV sintéticos en un temporal.

## 7. Las líneas del cierre, con sus bytes

Medidas sobre los ficheros de `main` (PROJECT_STATE en 24.131 bytes; el tope es 25.000,
`tests/unit/test_project_state.py`). Antes de proponerlas, `grep` en `tests/`, `docs/`, `scripts/`,
`src/`, `.claude/skills/` y PROJECT_STATE de cada texto que cambia: solo los citan informes cerrados
y `docs/state/HISTORIA.md` (F17-HISTORIAL.md:1045, :1220, :1276 y :1314; HISTORIA.md:21682, :21746 y
:21809), que no se tocan; ningún test.

- **PROJECT_STATE, la F de la Next Action:** «F17 (ADR-0099 §5; el historial: F17-HISTORIAL.md) y el
  backtest del trader con costes (ADR-0100, R4.10), pendientes.» → «F17 (ADR-0099 §5;
  F17-HISTORIAL.md y F17-ORDENES.md, sin correr) y el backtest del trader con costes (ADR-0100,
  R4.10), pendientes.» **+15 bytes**: 24.146 de 25.000 (con `Current Branch` y `Current Feature`
  devueltos a los de `main` y el recuento de tests con los mismos dígitos).
- **HOJA-DE-RUTA, A.5, «Qué es»:** «El historial: herramientas hechas y sin correr
  (trabajo/f17-historial, F17-HISTORIAL.md); la corrida, en una prueba gratuita, en su rama.» → «Las
  tres partes, en código y sin correr: el historial (trabajo/f17-historial, F17-HISTORIAL.md), y el
  grabador y la medida de las órdenes stop (trabajo/f17-ordenes, F17-ORDENES.md). Las corridas, en
  pruebas gratuitas y en su rama; la medida pide varias (cuántas, en F17-ORDENES.md) y no se lanza
  hasta que FTMO conteste el correo del 2026-11-26 (A.2).» **+217 bytes**. Sin recuentos
  (HOJA:12-13). Ninguna entrada pasa a HECHA.
- **HOJA-DE-RUTA, «F01-F35 · Estado medido», fila F:F17** (no está en el «Marcador»: error menor del
  consultor): «PARCIAL: el script de medición (tres ejecuciones, ADR-0071 y ADR-0090) y las
  herramientas del historial, sin correr; no el grabador ni la medida de las órdenes stop» → «PARCIAL:
  el script de medición (tres ejecuciones, ADR-0071 y ADR-0090) y las tres partes de ADR-0099 §5 (el
  historial, el grabador y la medida de las órdenes stop), en código y sin correr», y en sus
  documentos `F17-ORDENES.md`. **+43 bytes**.
- **HOJA-DE-RUTA, A.2, «Estado»** (punto 7 de la respuesta), al final: «Enviado el 2026-11-26 (hilo
  nuevo): si la prueba gratuita ejecuta como el Challenge y la cuenta real (P4-08), y si medir con un
  guion propio, con dos tamaños de lote, es práctica prohibida, hiperactividad o afecta a un
  Challenge futuro (R13, R16 y R17); respuesta pendiente, y la medida de F17 no se lanza sin ella
  (F17-ORDENES.md).» Sin recuentos.
- **Nada sale ni cambia de nombre** (ninguna Ref, heredado ni línea de Technical Debt).

## 8. La fila de ERRORES-RECURRENTES, preparada

Con las cuatro columnas de la tabla (`Rama | Hallazgos del revisor | Hallazgos del consultor despues |
Que se le escapo`):

| `trabajo/f17-ordenes` | Una pasada, opus, con los alcances de §7, los puntos 2, 3 y 7 de la PARADA y los arreglos 1 y 2 de la revisión de los `.mq5` (F17-ORDENES.md, §10; lo hecho, en §4): eje (a) 0 bloquea, 0 importa, 2 menor; eje (b) 0 bloquea, 4 importa, 3 menor. b1 (el contrato comprobaba que cada tope se LLAMA, no que COMPARA con su `TOPE_*`: una prueba que no prueba lo que dice), b3 (el lector leía una carpeta y el veredicto de D3 pide juntar días y pruebas), b4 (la caducidad caía a GTC, heredado de MedirDemoFTMO), b2 (las secciones de entrega) y b5 a b7 (tiempos y robustez del ciclo); arreglados todos | En la fase 0 (la sesión y el auditor): (1) «las siete observaciones de ADR-0090 §7 ... 0,01 lotes», copiado del ADR sin contar la lista (son nueve; seis a mercado, cuatro con 1,00 lote); (2) R17 no citado, solo R16; (3) `OrderCalcMargin` sin decir el tipo de orden, con la tasa 0;0 de la stop ya escrita en ADR-0090; (4) «tan cerca como deje el servidor» sin mirar los llenados al colocar de la ejecución 3; menores: las 2 h 30 min atribuidas a R15, los festivos en ADR-0068 §4 y la fila F:F17 en el «Marcador». En la revisión de los `.mq5` (consultor): el saldo del día restaba el depósito del primer día, así que el tope (b) no saltaba nunca ese día; y el grabador rehacía sin límite desde los CSV de una prueba anterior | Lo que el consultor copia de un ADR se cuenta y se cruza con el resto del ADR antes de escribirlo; un tope que se calcula del historial se prueba también el primer día de la cuenta y tras relanzar; y un contrato en el texto que comprueba que una función se llama no comprueba que compara: cada tope necesita la mutación de su comparación |

## 9. La CI de `fix/f17-ordenes`

- **Run 45904547776**, sobre `24987139` (empujado con
  `git push origin trabajo/f17-ordenes:refs/heads/fix/f17-ordenes`): `failure` con **un solo fallo, el
  esperado**, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (PROJECT_STATE declara
  `trabajo/f17-ordenes` y la rama es `fix/f17-ordenes`, RITUAL.md); «1 failed, 3701 passed, 102
  skipped».
- **Pendiente:** la CI sobre el último commit, tras la recompilación de §4.

## 10. Informe del revisor (subagente `revisor`, sobre `24987139`)

Pegado tal cual, con los títulos bajados un nivel:


He revisado HEAD 24987139 contra la base e8c20a80: 6 commits y 23 ficheros, con el árbol de trabajo limpio. La rama no está lista: el eje (a) no tiene nada que bloquee, pero en el eje (b) quedan cuatro hallazgos importa, dos de ellos en código y tests.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | menor | El estado del informe está desfasado. La cabecera dice «EN CURSO (respuesta a la PARADA, aplicándose)» y el `## Estado` final dice «viene el código de D1 a D9», cuando el código ya está commiteado (1d483ce6, 8178c600) y compilado (24987139). | `docs/validation/F17-ORDENES.md`:3 y :802-804 |
| a2 | menor | Afirmaciones sobre el lector que el código no sostiene. `scripts/README.md` dice «Valida los manifiestos de `data/manifests/f17-ordenes/` y `f17-grabador/`», pero `main()` nunca llama a `validar_manifiesto`: solo la usa el test. El diseño de la PARADA hablaba de `validar_manifiesto_ordenes` y `validar_manifiesto_grabador` (§1.3) y de un valor del punto `SYMBOL_TRADE_TICK_VALUE/...` (§1.1). El código hace otra cosa (una sola `validar_manifiesto(doc, tipo)` y `OrderCalcProfit`) y §2 no lo declara. El README de `leer_historial_f17` tiene la misma frase. | `scripts/README.md` (diff, línea «Valida los manifiestos…»); `scripts/leer_ordenes_f17.py`:541 (def) y :582-614 (`main` sin llamada); `MedirOrdenesFTMO.mq5`:384-390; informe :288 y :363 |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da «CONTRATO: 23 ficheros dentro del contrato… G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-26 para trabajo/f17-ordenes, estadiada», exit 0.
- **Comprobaciones del contrato.**
  - `uv run botsito state check`: OK.
  - `uv run botsito knowledge validate` (a stdout): todo OK, solo con los dos AVISO de config congelado de siempre.
  - `make check` no lo ejecuté. Su `make-check.log` trae «3798 passed, 6 xfailed», «SELLO: make check en verde sobre el arbol f49b0da2…», que es `git rev-parse HEAD^{tree}`, y «PICO DE MEMORIA … 322 MiB».
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout y material.** No se toca `knowledge/cases/holdout`. Hay seis filas de HOLDOUT del 2026-11-26 que nombran la rama. La segunda declara, el mismo día, que la lectura de las claves de `meses_reservados.yaml` y de los nombres de primer nivel de `knowledge/cases/` se hizo antes de escribir la fila: cumple ADR-0021 §4. No hay libros, imágenes, fotogramas ni crudas.
- **Regímenes de cambio.** Nada en `knowledge/evidence`, `knowledge/feedback`, `data/manifests` ni `corpus`. `HISTORIA.md` y `data/manifests/README.md` tienen 0 líneas quitadas.
- **Ambigüedades, ADR y citas.** No hay ambigüedades, ningún ADR cambia y no se añade ningún sitio con `cita`. No hay items de evidencia nuevos.
- **Informes cerrados.** No se cambia ninguno; HOLDOUT-EXPOSICIONES solo gana filas.
- **Cifras.** Las del `.mq5` se comparan con el registro y el yaml (test :170-175).
- **Citas del informe comprobadas contra su fuente (5):**
  - `premisa.txt`:67, «mediana de D: 18 puntos»;
  - ADR-0090:168-173, la 3 con la sell stop y la buy stop «llenada al instante»;
  - `DEMO-EJECUCIONES-2-3.md`:84-86, «tasas de margen buy stop 0.0000;0.0000… calculado a la orden 0.00»;
  - `DEMO-FTMO.md`:158-166, el reinicio a las 00:00 de España;
  - ADR-0068 «Alternativas» 2 (:117-118), las sesiones no traen los festivos.
- **Copias literales.** La respuesta a la PARADA es idéntica en el encargo (:86-120) y en el informe (:564-598): `diff` sin salida. El correo literal está en :600-619; frente al pedido solo cambia el formato (negritas y comillas de código) y una frase de enlace añadida.

#### Eje (b) · Encargo
Resumen: 0 bloquea, 4 importa, 3 menor. Requisitos: 38 hechos, 5 parciales, 6 no hechos.

**Requisitos**

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | §0 base verificada, apertura, tramo R4, ningún ADR, lista blanca | Hecho | informe :12-23; `contrato.yaml`:4; `diff --stat` de `docs/adr` vacío; contrato_rama OK |
| 2 | §0 fila HOLDOUT antes del primer `make check` | Hecho | HOLDOUT, cinco filas nuevas en el diff |
| 3 | §2 diff vacío (motor, simulador, `knowledge/`, `src/`, `mql5/`, MedirDemo, ExportarTicks, `leer_historial_f17`, F17-HISTORIAL.yaml, `f17/`, `demo_ftmo/`, criterio, PREMISA, PUENTE, ADR, MASTER_PLAN, sus tests, config, Makefile, `.claude`, `.gitignore`) | Hecho | `git diff --stat main...HEAD -- <todas>`: sin salida |
| 4 | Fase 0, puntos 0.1 a 0.5 | Hecho | informe :25-244, :621-651 |
| 5 | PARADA con diseño, yaml en borrador y decisiones | Hecho | informe :246-558 |
| 6 | D1, la condición DEMO de :759 la primera, antes de cualquier petición | Hecho | `MedirOrdenesFTMO.mq5`:899 y :956; test :115-125 y :256-257 |
| 7 | D1, solo EURUSD y mágico propio | Hecho | :50-51 (57057100 frente a 57057000 en `MedirDemoFTMO.mq5`:33); `grep` de `magic` en `mql5/` vacío |
| 8 | D1, limpieza al empezar, al terminar y si falla, solo lo suyo, y comprobada | Hecho | :294-344, :808, :835, :889, :987, :995 |
| 9 | D1, toda pendiente con caducidad | **Parcial** | `PonerCaducidad` :204-214, que cae a GTC (hallazgo b4) |
| 10 | D1, toda posición con stop desde que nace | Hecho | stop en la orden, :245 |
| 11 | D1, ciclo alterno a 5 puntos, stop 18, salida a mercado a 300 s | Hecho (b5) | :54-57, :783, :847, :992 |
| 12 | D1, estrato «bot» con `OrderCalcMargin` a mercado y ADR-0081 D2 | Hecho | :375-402; test :212-216 y :447-451 |
| 13 | D1, columnas del CSV y ticks por llenado | Hecho | :179-181, :727-754 |
| 14 | D2, grabador de solo lectura con contrato | Hecho | `Grep` de OrderSend, CTrade, Position, OrderCalc, HistorySelect y OrdersTotal en el fuente: 0 coincidencias; test :31-36 con las 33 de `FUNCIONES_DE_TRADING` |
| 15 | D2, DEMO y EURUSD; `CopyTicks` desde el último `time_msc`; atómico por hora; prefijo `F17G_` | Hecho | `GrabarTicksFTMO.mq5`:99-112, :118-141, :300-326 |
| 16 | D3, yaml antes de cualquier llenado, fijado por sha y commiteado antes que su lector | Hecho | sha256 3d453e90… igual al del test :23; yaml en 1cac097f (14:56) y lector en 1d483ce6 (15:35); `git diff 1cac097f HEAD` del yaml y su test vacío; no existe `data/f17*` ni `data/manifests/f17-*` |
| 17 | D4 (a), peor caso con compras y ventas ≤ 1.000, de la terminal | Hecho | :406-458; test :207-211 y :440-445 |
| 18 | D4 (b) y (c), desde la cuenta y el historial | Hecho en código (b1) | :484-517, :629-638, :664-667 |
| 19 | D4 (d), 500 peticiones y pausa fija de 1.500 ms | Hecho en código (b1) | :218-232, :523-577, :639 |
| 20 | D4 (e), 150 min, y los festivos en el runbook | Hecho | :582-605; runbook :74-81 |
| 21 | D4, constantes comparadas con el runbook | Hecho | test :66-75 y :176-180 |
| 22 | D4, cada tope con un test que rompe | **Parcial** | hallazgo b1 |
| 23 | D4, cada tope que salta escribe su fila | Hecho | :652, :670, :799 |
| 24 | D5, lector `medida` y `grabador` con `RelojServidor`, sin cifras | Hecho | `leer_ordenes_f17.py`:100-105, :594 |
| 25 | D5, los seis tests que rompen (ASK/BID con otro tick, `sin_tick`, >5 %, «bot» +1, p90 = máx(p90 uno, máx bot), fuera de ventana) | Hecho | `test_leer_ordenes_f17.py`:81-95, :139, :238, :229, :218, :194 |
| 26 | D5, sin comparación con Dukascopy | Hecho | yaml :65 |
| 27 | D6, no filtra por mes y no imprime precios | Hecho | lector :396-437, :461-472 |
| 28 | D7, manifiestos fuera de `f17/`, esquema en el README y test | Hecho | test :120-146; README :37 |
| 29 | D7, el runbook con su contenido | Hecho | `F17-ORDENES.md` entero |
| 30 | D7, «cómo se lee» | **Parcial** | hallazgo b3 |
| 31 | D7, línea en F17-HISTORIAL e índice | Hecho | diff de los dos ficheros |
| 32 | D8, compilación PASA en los dos; `compilar.py` sin diff; logs de los fuentes commiteados | Hecho | logs: «Result: 0 errors, 0 warnings», sha 91fdda77… y 46b229dc…, iguales a `git show HEAD:<f> \| sha256sum` |
| 33 | D9, CI de `fix/f17-ordenes` en verde salvo `state check` | **Parcial** | run 45904547776 en curso; no lo consulté |
| 34 | Punto 0, las dos estimaciones como supuestos y el replanteo | Hecho | runbook :41-48 |
| 35 | Punto 1, constantes fijas sin `input` | Hecho | test :181-183 |
| 36 | Punto 2, lote bajado, lote usado y lote D2 en la fila, `bot_reducido` <90 %, margen a mercado | Hecho (bucle sin test, b1) | `.mq5` :786-796 y :159; lector :212-221; test :202-205 |
| 37 | Punto 3, ventana 22-03, zoneinfo 2026-2030 a los dos lados, nada vivo a las 22:00 en el contrato | Hecho (b5) | test :521-553 y :424-438 |
| 38 | Punto 4, historial más las rechazadas de los CSV | Hecho en código (b1) | :523-577, :969 |
| 39 | Punto 5, toda la cuenta; en el runbook, que no opera nada más | Hecho | runbook :77-78 |
| 40 | Punto 6, script; relanzado; hueco en el control | Hecho | runbook :110-118 |
| 41 | Punto 7, la medida no se lanza sin la respuesta de FTMO, qué pasa con cada respuesta, y el correo literal | Hecho | runbook :13-21; informe :600-619 |
| 42 | Puntos 8 y 9, `al_colocar` y búsqueda en `(puesta, llenado]` | Hecho | lector :167-197; yaml :19-35 |
| 43 | Revisión, arreglo 1, solo `DEAL_TYPE_BUY` y `DEAL_TYPE_SELL` | Hecho | :495-497; test :219-224 y :389-398 |
| 44 | Revisión, arreglo 2: `MAX_HORAS_REHACER` 72, `hueco_largo`, login en el control y no en el repo | Hecho | grabador :40, :264, :282-290; `git grep -i login` no da ningún valor; manifiestos README :136 |
| 45 | Revisión, arreglos 3 a 6 | Hecho | informe :774-781 |
| 46 | §7, el encargo punto por punto (la tabla de `entregar-rama`, E5) | **No hecho** | `grep` de «punto por punto» en el informe: solo la cabecera :4 |
| 47 | §7, desviaciones y fila de ERRORES-RECURRENTES preparada | **No hecho** | el informe acaba en :804 |
| 48 | §6, las líneas de cierre (Next Action F, A.5 y F:F17, A.2 del punto 7) con sus bytes | **No hecho** | ídem |
| 49 | §7, informe del revisor pegado y «Rama lista para revisión, NO cerrada.» | **No hecho** | pendiente; no lo pego yo |

En el conteo del resumen, las filas 46 a 49 suman seis requisitos no hechos (la 47 y la 49 cuentan dos cada una). Los 5 parciales son 9, 22, 30, 33 y la 49 vista como «pendiente de entrega».

**Hallazgos**

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Los topes (a) a (d) tienen test, pero su comparación no.** El contrato solo exige que `PuedeEmpezarCiclo` contenga las llamadas (`"SaldoAlEmpezarElDia()"`, `"PeticionesDelDia()"`, `"PeorCaso("`…) y que las funciones lean `HistorySelect` y similares. No mira que cada comparación use su `TOPE_*`. Mutaciones como estas pasarían el contrato: borrar `\|\| equity < saldo_dia - TOPE_DIA_USD` en `PuedeEmpezarCiclo` (:629) o en `HayQueCortar` (:664); cambiar `peticiones + 3 > TOPE_PETICIONES` (:639) por `false`; borrar el `peor > TOPE_PEOR_CASO_USD` (:644) o el bucle que baja el lote (:790-796, punto 2); quitar `+ g_rechazadas_previas + g_rechazadas` (:549) o el `n++` de la borrada (:537-538); dejar `RechazadasDeHoy` en 0 (:969), que es justo lo que vale «tras relanzarlo»; o quitar el `MARGEN_CIERRE_MIN` de :600. El docstring del test (:18-19) y el informe (:694) dicen más de lo que el test prueba. Es «una prueba que no prueba lo que dice», justo en el alcance «cada uno con un test que rompe». | `tests/contract/test_medir_ordenes_ftmo.py`:78-92, :185-193 y :199-202. `Grep` de `TOPE_\|peticiones \+\|g_rechazadas\|RechazadasDeHoy\|CANCELED` en el test: `TOPE_*` solo sale en `DEL_RUNBOOK` (:67-70) y en las mutaciones de `#define` (:345-362); `g_rechazadas` solo como sustituto en :415. No pude ejecutar las mutaciones: la guardia negó el import (abajo). |
| b2 | importa | **Faltan las secciones de entrega de §7.** No están la tabla «El encargo, punto por punto» (E5 de `trabajo/entorno-code`), las desviaciones (entre ellas la lectura previa a la fila de HOLDOUT que la fila llama «desviación del informe»), las líneas de §6 con sus bytes (incluida la A.2 que pide el punto 7) ni la fila de ERRORES-RECURRENTES. | informe :748-804; HOLDOUT, segunda fila nueva («desviación del informe») |
| b3 | importa | **El lector no puede dar el veredicto de D3 por el camino que documenta el runbook.** El lector lee una sola carpeta, sin recursión. El runbook congela y lee por día. Los tamaños de D3 (100 por clase en «uno», unos 3 días; «bot» en 2 o 3 pruebas) solo se alcanzan juntando días y pruebas, así que cada lectura por día saldrá «insuficiente». Nada dice cómo se agregan, y el informe no lo declara. | `leer_ordenes_f17.py`:381 (`carpeta.iterdir()`); runbook :141 (`data/f17-ordenes/<AAAA-MM-DD>/`) y :148 (`medida data/f17-ordenes/<dia>`); runbook :35 («unos 3 días de ventana») |
| b4 | importa | **«Toda pendiente lleva caducidad» (D1) no está garantizado.** Si el símbolo no admite `SYMBOL_EXPIRATION_SPECIFIED`, `PonerCaducidad` pone `ORDER_TIME_GTC`, es decir, sin caducidad (el propio informe :55 lo dice de MedirDemoFTMO). El nuevo guion hereda ese camino sin negarse, y la cabecera (:19) y el runbook (:58-59) afirman «y caducidad». El contrato solo exige la llamada a `PonerCaducidad(req)` (test :141-142). No está declarado como decisión. Leído al pie de la letra («falta algo que el encargo pide explícitamente») podría ser bloquea; lo dejo en importa porque el patrón viene de `MedirDemoFTMO`, que el encargo manda reutilizar. | `MedirOrdenesFTMO.mq5`:204-214, :19; runbook :58-59 |
| b5 | menor | **El ciclo dura más de lo que dicen T y `DURACION_MAXIMA_CICLO_S`.** Los 300 s empiezan a contar después de copiar los ticks de la entrada (`fin` en :847, tras `FilaDeLlenado` en :843, que duerme 5.000 ms y hasta 3×1.000 ms en :729 y :739). La salida a mercado es, por tanto, a ≥305 s del llenado, no «a los 300 s» (runbook :60; yaml `salida_a_mercado_s`). `DURACION_MAXIMA_CICLO_S` (120+300+60, :78), que el informe llama «duración máxima» (:693), no cuenta las dos esperas de ticks ni las pausas de `Pedir`. Sin bloqueos el ciclo cabe (unos 440 s); si `CopyTicksRange` bloquea, no. Durante esas esperas no se consulta `HayQueCortar`. | :78, :729-740, :843-847 |
| b6 | menor | **Una colocación rechazada no para la ejecución.** Si `ColocarStop` es rechazada, `Ciclo` sigue con el ciclo siguiente cuando `Limpiar` da 0. Ante un rechazo persistente se envían hasta `InpCiclos` peticiones rechazadas, acotadas solo por (d). Es lo que el arreglo 3 quería evitar, y A-54 no sabe si FTMO las cuenta. | :807-808; :990-994 |
| b7 | menor | **Tres caminos de robustez que pierden muestras o piden de más.** (i) Un cierre aceptado se busca en el historial una sola vez, tras 500 ms. Si el historial va con retraso, sale `sin_salida` y se para toda la ejecución, aunque `rc.deal` ya traía el deal. (ii) Si la pendiente se llena justo al borrarla y el deal aún no está en el historial, sale `sin_llenado` y `Limpiar` cierra la posición sin registrar la entrada. (iii) Si fallan `OrderSelect` y `HistoryOrderSelect`, `puesta` queda en 0 y `GuardarTicks` pide desde `MathMin(cot.time_msc, 0)` = 0, es decir, desde 1970. Los tres son seguros (no dejan nada abierto). | (i) :858-862, :866-871; (ii) :820-836; (iii) :810, :837-844 |

Lo que la rama añade sin que el encargo lo pida: el objetivo de respaldo a 54 puntos y `tick_tarde`. Los dos están declarados (informe :716-720) y el consultor los aceptó (§3, :756). No hay más añadidos sin justificar.

**Lo demás de los alcances:**
- **Grabador.** No puede enviar órdenes (fila 14).
- **Reloj del servidor a UTC.** `RelojServidor` se importa sin editar el guion y sin cifras: lector :87-105; test :386.
- **Manifiestos.** No caen en `f17/`: test :120-125; ninguno existe todavía.
- **Arreglo 1, prueba mental del primer día y del relanzado:**
  - Primer día: el depósito de 100.000 es un `DEAL_TYPE_BALANCE` y se salta (:496). `movido` = P y el saldo es 100.000 + P, así que el saldo del día da 100.000, (b) salta en 97.000 y (c) da un capital de 100.000 (:505-517).
  - Relanzado el mismo día: da lo mismo, porque todo se lee del historial.
  - Día siguiente: 100.000 + P1.
  - Se sostiene.

#### Lo que no pude comprobar
- **Las mutaciones de b1.** La guardia negó `uv run python -B -c "import tests.contract.test_medir_ordenes_ftmo …"` («no se pudo resolver el modulo `tests.contract.test_capa_mt5`»), y antes la variable `PYTHONDONTWRITEBYTECODE`. No la rodeé: la evidencia de b1 es el texto del test.
- **`make check`**, porque escribe. Su evidencia es `make-check.log`: el SELLO cae sobre el árbol de HEAD, «3798 passed», 322 MiB.
- **La CI**, run 45904547776, por indicación del encargo.
- **Comportamientos de MT5 sin medir:**
  - si `HistoryOrderSelect` en los argumentos de :885-888 (orden de evaluación) deja sin selección el deal antes de `HistoryDealGetInteger(salida, DEAL_ORDER)`;
  - si `CopyTicksRange` bloquea en un script (b5);
  - si las esperas basadas en `TimeCurrent` (:812, :847) se alargan cuando no llegan ticks;
  - si `OrderSend` funciona en los 3 s que siguen a `IsStopped` (el `Limpiar("al_terminar")` cuando se para a mano);
  - si FTMO-Demo admite `SYMBOL_EXPIRATION_SPECIFIED` (eso volvería teórico b4);
  - si FTMO mueve el saldo con deals de otros tipos (`CHARGE`, `COMMISSION` diaria, `CORRECTION`), que `SaldoAlEmpezarElDia` no resta y que estrecharían el margen de (b).
- **Los recuentos de tests del informe** (108, 148 y 57 FAILED contra `main`) no los rehíce. Los seis ficheros de la rama más `test_manifiestos_f17.py` pasan todos en `pytest -q` (salida sin F).

#### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read: el encargo y `contrato.yaml`
3. `uv run python scripts/contrato_rama.py`
4. `git diff --name-status main...HEAD` y `git log … --name-status main..HEAD`
5. Read: `tools/mql5/MedirOrdenesFTMO.mq5` y `tools/mql5/GrabarTicksFTMO.mq5`
6. `sed -n 750,775p tools/mql5/MedirDemoFTMO.mq5`; `grep` de MAGICO y `#define`; `grep -rn magic mql5/`
7. Read: los dos contratos, `leer_ordenes_f17.py`, el yaml, `test_f17_ordenes_criterio.py` y `test_manifiestos_f17_ordenes.py`
8. `sha256sum` del yaml; `git diff --stat 1cac097f HEAD -- <yaml, test>`; `git show --stat 1cac097f`; `git diff --stat main...HEAD -- <rutas de §2>`
9. `PYTHONDONTWRITEBYTECODE=1 uv run … pytest …` (negado por la guardia)
10. `uv run python -B -m pytest -p no:cacheprovider -q` con los 6 ficheros (todo pasa)
11. `Grep` en `test_capa_mt5.py`
12. `grep` de los `def test_` del lector y de los manifiestos; Read de `test_leer_ordenes_f17.py`:36-265
13. `sed -n 120,132p tests/unit/test_manifiestos_f17.py`; `Grep` de rglob y manifests en `src/botsito`
14. `cat` de los dos logs de compilación
15. `git show HEAD:<mq5> | sha256sum` (los dos) y `git show 8178c600:…`; `git diff --stat 8178c600 HEAD -- tools/`; `git diff main...HEAD --stat -- compilar.py`
16. Read del informe (:1-804); `Grep` de GTC y caducidad
17. Read del runbook `F17-ORDENES.md`
18. `git diff main...HEAD` de F17-HISTORIAL, el índice de runbooks, los dos README, PROJECT_STATE y HOLDOUT
19. `git diff … data/manifests/README.md | grep`; `git grep -n -i login HEAD`
20. `Grep` de `validar_manifiesto` en los dos lectores
21. `sed` de las citas (premisa, DEMO-EJECUCIONES, DEMO-FTMO, parametros) y `ls docs/adr | grep`; `sed` de ADR-0090, ADR-0068 y ADR-0099
22. `uv run python -B -c "import tests.contract…"` (negado por la guardia)
23. `Grep` de `TOPE_` y demás en el contrato de la medida
24. `uv run botsito state check`
25. `uv run botsito knowledge validate`
26. `ls -la make-check.log; grep SELLO/PICO`; `git rev-parse HEAD^{tree} HEAD~1^{tree}`
27. `diff <(sed …encargo) <(sed …informe)`: la primera forma, negada; la segunda, IGUALES
28. `ls data/manifests | grep f17; ls data | grep f17`; `grep` de secciones en el informe
29. `Grep` de funciones de trading en `GrabarTicksFTMO.mq5` (0)

Ficheros:
- tools/mql5/MedirOrdenesFTMO.mq5
- tools/mql5/GrabarTicksFTMO.mq5
- tests/contract/test_medir_ordenes_ftmo.py
- scripts/leer_ordenes_f17.py
- docs/runbooks/F17-ORDENES.md
- docs/validation/F17-ORDENES.md

(Las rutas de «Ficheros», relativas a la raíz del repo; el informe original las daba absolutas.)

## Estado

EN CURSO: el código, los tests, la compilación de `8178c600`, la CI de `24987139` y el revisor,
hechos; los arreglos del revisor (§4) cambian los `.mq5`, así que faltan la revisión del diff por
el consultor, la recompilación con su comando y la CI sobre el último commit. La rama NO está
lista todavía.
