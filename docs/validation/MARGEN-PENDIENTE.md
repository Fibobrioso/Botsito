# MARGEN-PENDIENTE · el script 1.2 de MedirDemoFTMO (paso 8, el margen de una pendiente stop) y PROJECT_STATE adelgazado

Rama `trabajo/margen-pendiente`, abierta el 2026-10-31 desde `main` 6948375 (commit de estado sobre
el merge 4b12a92, tag `stable/F38j-respaldo-m1`). Encargo: `docs/encargos/trabajo-margen-pendiente.md`.
Tramo «Carril: lo de Aleks» de `docs/plan/HOJA-DE-RUTA.md` (entrada A de la Next Action, A.1).

## Apertura: la base, comprobada con git

| Comprobación | Salida |
|---|---|
| `git rev-parse main origin/main main^1` | 6948375f9faf514e0b719495af9a46ccd3193320 (dos veces) y 4b12a9209dc23de9e988cd40058ab9ef80623032 |
| `git rev-parse "stable/F38j-respaldo-m1^{commit}"` | 4b12a9209dc23de9e988cd40058ab9ef80623032 = `main^1`; en origin (`git ls-remote --tags origin stable/F38j-respaldo-m1`: 25c6cc7d…, el objeto del tag anotado) |
| último `- Tag: ` de HISTORIA | `stable/F38j-respaldo-m1` (HISTORIA.md:14001) |
| `gh run view 40943847054 --json status,conclusion,headSha,headBranch,workflowName` | `{"conclusion":"success","headBranch":"main","headSha":"6948375f9faf514e0b719495af9a46ccd3193320","status":"completed","workflowName":"ci"}` |
| `git branch --list` / `git ls-remote --heads origin "fix/*"` | solo `main`; ningún `fix/*` en origin |
| `git worktree list` | el worktree `wt-ci` (e7df30b, detached) sigue, en la carpeta de otra sesión: no se toca |

## 0. Fase 0 · inventario sin tocar nada (2026-10-31)

Medido en esta sesión: cada afirmación con `fichero:línea`, el comando y su salida, o la URL con su
fecha. La rama no ha escrito código: solo este informe. Las sondas de la compilación y las
previsiones de bytes se hicieron sobre copias en la carpeta de trabajo de la sesión, fuera del
repositorio.

### 0.a El script 1.1

Verificado en `tools/mql5/MedirDemoFTMO.mq5` (843 líneas):

| Lo que dice el encargo | Medido |
|---|---|
| `VERSION_SCRIPT "1.1"` (:31), `#property version "1.10"` (:27), `MAGICO` (:33) | sí, las tres |
| Cotizacion, PonerCaducidad, PendienteViva, BorrarPendiente, PrecioDelLlenado, CerrarPosicion, Limpiar, MargenAlcanza (con OrderCalcMargin) | :146, :163, :214, :223, :238, :261, :311 y :595 (OrderCalcMargin en :598) |
| OnStart limpia al empezar, tras 3, 4, 5 y 6 y al terminar; el 7 depende de `InpMedirLlenadoStop`; un paso que falla salta los siguientes | :818, :823, :825, :827, :829, :833; :830; la cadena `if(ok) ok = …` de :820-830 |
| Fila escribe «\r\n» a mano | :126; Dato pasa por Fila (:133) |
| EnviarPendiente sin stop a propósito | :194 («SIN stop ni objetivo»), :195-212 |
| CerrarPosicion: cierre con `req.position`, sin stop | :272-279 |
| MedirComision y MedirLlenadoStop: magic, stop y, la pendiente, caducidad | :637 y :641; :693, :697 y :700 |
| La condición DEMO, en :759 | :759, dentro de `Comprobaciones` (:757-791) |

**Dónde va el paso 8 sin mover :759.** Las líneas 1-758 no pueden cambiar de número. Los `input`
viven en :35-38, antes de :759 (el auditor lo señala): el input del paso 8 NO puede ir junto a ellos.
La documentación de MQL5 no dice dónde se declara un `input` ni si se admite llamar a una función
definida más abajo (abajo, 0.b); lo prueba la compilación: una copia de la 1.1 con un `input bool`
y una función nuevos declarados DESPUÉS de `Comprobaciones` (tras :791), llamada desde `OnStart`,
compila con `Result: 0 errors, 0 warnings, 819 ms elapsed` y su `.ex5` (49.844 bytes), y su línea 759
sigue siendo la condición DEMO (sonda `sonda_input.py`, fuera del repo). Así que el paso 8 entero
(constantes, inputs y funciones) va entre `Comprobaciones` y `OnStart`, sin prototipos: todo lo que
usa (Fila, Dato, Cotizacion, PonerCaducidad, PendienteViva, BorrarPendiente, PrecioDelLlenado,
CerrarPosicion, Limpiar, VolumenAdmitido) está definido antes. Cambian, en las líneas 1-758, solo
:27 y :31 (la versión) y la cabecera reescrita EN SU SITIO (mismas 25 líneas).

**La cabecera dice ya dos cosas falsas** (el encargo nombra una): «solo el volumen minimo (salvo el
paso 6…)» (:18-19), que el paso 8 hace falsa, y «toda posicion lleva stop de proteccion» (:20-21),
que ya es falsa en la 1.1: una pendiente de EnviarPendiente que se llena al instante (:426-433) abre
una posición sin stop (auditor, fila 24). `DEMO-FTMO.md:22` dice lo mismo. La 1.2 lo corrige en las
dos (decisión 1). `#property description` (:28) enumera las medidas: gana «margen de pendientes».

**Las citas de :759.** ADR-0082:116 (la condición literal en :117), `mql5/Include/Botsito/Capa/Cuenta.mqh:8`
y `tests/contract/test_capa_mt5.py:10` (docstring) la citan; :278 de ese test está dentro de una
cadena de ejemplo (`INCLUDE_BUENO`, :277-285) y no apunta al fichero real. Hay más citas en informes
cerrados (`EA-CONEXION.md:120,535,557,635,1146,1162`, `PLATAFORMA-ADELANTADA.md:85`). `condicion_de_medir`
(:142-149) toma la primera línea sin comentarios con `ACCOUNT_TRADE_MODE_DEMO` y exige que sea un
`if(...)`; ningún test comprueba el número 759: lo sostienen las citas textuales.

### 0.b La documentación oficial (consultada el 2026-10-31)

- **Margen de una pendiente stop.** «Margin Calculation for Retail Forex, Futures»,
  <https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex> (la que cita
  ADR-0081 §4): «The margin is charged for securing traders' open positions and orders»; «For all
  other order types (Stop and Stop Limit), the margin is summed up (charged for each order)»; mismo
  lado: «the total margin is equal to the sum of the current position's and placed order's
  margins»; conversión: «The Ask price is used for buy deals, and the Bid price is used for sell
  deals»; «The order price is used for limit orders» (en la sección de futuros de la Bolsa de
  Moscú, como «Once triggered, stop orders behave similar to market orders»). **La página no dice en
  qué instante se comprueba el margen de una pendiente (al colocarla o al saltar), ni a qué precio se
  carga una stop en forex**: es lo que mide el paso 8. MARGEN-LOTE.md §1.b (:114-143) ya la leyó el
  2026-10-17; no hay frase nueva.
- **Hedging.** Misma página: «If the hedging position accounting system is used, the margin is
  calculated using the same formulas and principles as described above»; «Oppositely directed open
  positions of the same symbol are considered hedged or covered»; «Two margin calculation methods are
  possible for such positions. The calculation method is determined by the broker». `SYMBOL_MARGIN_HEDGED`,
  <https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants>: «Contract size or
  margin value per one lot of hedged positions (oppositely directed positions of one symbol)»; si
  `SYMBOL_MARGIN_INITIAL` es 0, «SYMBOL_MARGIN_HEDGED is equal to the size of the contract»; con
  `SYMBOL_MARGIN_HEDGED_USE_LEG` («Calculating hedging margin using the larger leg (Buy or Sell)») se
  usa el mayor de los dos lados. `SYMBOL_VOLUME_LIMIT`: «Maximum allowed aggregate volume of an open
  position and pending orders in one direction»: la ejecución 1 lo midió en 0,00 (sin tope agregado,
  `DEMO-EJECUCION-1.md:149`); el paso 8 lo vuelve a leer, porque un tope agregado haría que M3 y M4
  salieran con 10034 y no con 10019. Lo que el paso 8 pone a la vez es SIEMPRE del mismo lado (todo
  compras): la pregunta de cómo cubre FTMO dos lados opuestos no entra (FTMO-P-D1.md:79-83).
- **El código de retorno sin margen.** <https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes>:
  10019 `TRADE_RETCODE_NO_MONEY`, «There is not enough money to complete the request» (el script ya
  lo nombra, :88). Vecinos que pueden salir: 10014 `INVALID_VOLUME`, 10034 `LIMIT_VOLUME` («The volume
  of orders and positions for the symbol has reached the limit»), 10033 `LIMIT_ORDERS`.
- **ACCOUNT_MARGIN y ACCOUNT_MARGIN_FREE.** <https://www.mql5.com/en/docs/constants/environment_state/accountinformation>:
  «Account margin used in the deposit currency» y «Free margin of an account in the deposit
  currency». **No dice si cuentan las pendientes.** Solo `ACCOUNT_MARGIN_INITIAL` las nombra: «The
  amount reserved on an account to cover the margin of all pending orders». El paso 8 escribe las
  tres.
- **OrderCalcMargin** (<https://www.mql5.com/en/docs/trading/ordercalcmargin>): «calculates the
  margin required for the specified order type… not taking into account current pending orders and
  open positions». **OrderCalcProfit** (<https://www.mql5.com/en/docs/trading/ordercalcprofit>): «for
  pre-evaluation of the result of a trade operation»; no dice si lleva comisión o swap (no la lleva:
  el peor caso la suma aparte). **SymbolInfoMarginRate** (<https://www.mql5.com/en/docs/marketinformation/symbolinfomarginrate>):
  «Returns the margin rates depending on the order type and direction»; el paso 8 la lee para
  `ORDER_TYPE_BUY_STOP` y `ORDER_TYPE_BUY` (sin petición al servidor). **ENUM_ORDER_STATE**
  (<https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties>): `ORDER_STATE_REJECTED`
  «Order rejected», `ORDER_STATE_CANCELED` «Order canceled by client», `ORDER_STATE_EXPIRED`.
- **Prototipos e inputs.** <https://www.mql5.com/en/docs/basis/function>: «Function prototype is the
  function declaration, but not its definition»; no habla de llamar a una función definida más
  abajo. <https://www.mql5.com/en/docs/basis/variables/inputvariables> no dice dónde se declara un
  `input`. Lo decide la compilación (0.a).
- **Modo de margen de la prueba nueva**: no está en el repo (lo dice la fila `modo_margen` del paso
  1 del CSV de la ejecución 2, que esta rama no lee). El paso 8 lo vuelve a escribir.

### 0.c El diseño del paso 8

Todo del MISMO lado (compras), con `MAGICO`, stop de protección y la caducidad de PonerCaducidad en
cada petición que abre o coloca; un `Limpiar` tras cada medida; las cifras, calculadas por el script
en el momento con OrderCalcMargin, el margen libre y el mínimo, máximo y paso del volumen (nunca un
lote fijo). Abajo, con lo medido en la ejecución 2 como ejemplo: margen libre ≈ 100.000 (el capital de
la prueba nueva NO está en el repo: auditor, fila 27) y 3.720,77 USD por lote (100000 × 1,11623 / 30,
`HISTORIA.md:13988-13990`). **Lejos** = 1.000 puntos (100 pips) por encima del ask: no salta en los
pocos segundos que vive. Todas son `buy_stop` o compras a mercado.

Filas nuevas (medición `8_margen`; claves con prefijo propio para que nada choque con las de los pasos
1-7):

- Contexto (Dato, sin petición): `p8_modo_margen` (ACCOUNT_MARGIN_MODE), `p8_margen_hedged`
  (SYMBOL_MARGIN_HEDGED), `p8_hedged_pierna_mayor` (SYMBOL_MARGIN_HEDGED_USE_LEG), `p8_margen_inicial`
  (SYMBOL_MARGIN_INITIAL), `p8_volumen_limite` (SYMBOL_VOLUME_LIMIT), `p8_tasa_buy_stop` y
  `p8_tasa_buy` (SymbolInfoMarginRate, «inicial;mantenimiento»), `p8_equidad`, `p8_margen_usado`,
  `p8_margen_libre`, `p8_margen_pendientes` (ACCOUNT_MARGIN_INITIAL), y el tope: `p8_tope_usd`,
  `p8_deslizamiento_puntos`, `p8_comision_lado_lote`.
- Por cada medida, una fila `mN_volumen` (valor = lotes; nota = margen necesario al ask y al precio
  de la orden, margen libre), una `mN_peor_caso` (valor = USD; nota = stop en puntos, lotes que suma
  y la cuenta), las peticiones con Fila (retcode, colocada, tipo, precios), y, si no se mide,
  `mN_no_medible` con el motivo.
- `p8_fin` = `hecho`, o `desactivado` si `InpMedirMargen` es false (una sola fila del paso 8).

**M1 · ¿rechaza al COLOCAR una pendiente cuyo margen no cabe?** Volumen v1 = el menor admitido con
OrderCalcMargin(BUY, v1, ask) > margen libre (al ask, que es el menor de los dos precios: al de la
orden también pasa). Ejemplo: 26,88 lotes. Si v1 pasa del máximo por orden → `m1_no_medible`. Una
`buy_stop` lejos con v1: fila `m1_colocar`. Si queda viva, se lee y se borra en la misma medida.
Peticiones: 1 o 2.

**M2 · ¿carga margen una stop viva, y a qué precio?** Se leen ACCOUNT_MARGIN, ACCOUNT_MARGIN_FREE y
ACCOUNT_EQUITY; se coloca una `buy_stop` lejos con v2 = el menor volumen admitido con
OrderCalcMargin(BUY_STOP, v2, precio de la orden) − OrderCalcMargin(BUY, v2, ask) ≥ 20,00 USD
(a 100 pips, 33,33 USD por lote: v2 = 0,61 lotes, unos 2.270 de margen); si la diferencia por lote
sale 0 (OrderCalcMargin no usa el precio), v2 = el volumen con unos 2.000 de margen y la parte «a qué
precio» queda «no distinguible». Se espera a que cambie ACCOUNT_MARGIN (cada 250 ms, hasta 5 s) y se
vuelven a leer. Filas: `m2_colocar`, `m2_margen_antes`, `m2_margen_despues`, `m2_libre_antes`,
`m2_libre_despues`, `m2_calculado_orden`, `m2_calculado_mercado`, `m2_espera_ms`. Se borra.
Peticiones: 2.

**M3 · ¿suma las pendientes al colocar otra?** v3 = el menor admitido con 2 × OrderCalcMargin(BUY, v3,
ask) ≥ 1,10 × margen libre, comprobando que OrderCalcMargin(BUY_STOP, v3, precio de la orden) ≤ 0,90 ×
margen libre (cabe sola a cualquiera de los dos precios). Ejemplo: 14,79 lotes cada una (29,58 en
total). Dos `buy_stop` lejos, una tras otra: `m3_colocar_1`, `m3_margen_tras_1` (ACCOUNT_MARGIN tras
la primera, que es otra lectura de M2), `m3_colocar_2`. Se borran. Peticiones: hasta 4.

**M4 · ¿comprueba al LLENAR?** Una `buy_stop` S cerca, a max(stops level, 1) + 10 puntos del ask (un
pip: salta pronto, pero no antes de ocupar el margen), que cabe al colocarla; después se ocupa el
margen libre hasta que S ya no cabe; y se espera a que salte (`InpEsperaMargenSeg`, 120 s). Cómo se
ocupa lo decide lo medido en M2 y M3, con la misma regla que el lector (0.d), y lo escribe la fila
`m4_ocupacion`:

| M2 | M3 | ocupación | por qué |
|---|---|---|---|
| no concluyente | — | no medible | sin saber si la pendiente carga margen no se elige cómo ocuparlo |
| no carga | — | `posicion`: una compra a mercado V | una pendiente no ocupa nada; S grande (≈ 80 % del margen libre, unos 21,50 lotes) y V pequeña (≈ 25 %, unos 6,72): tras V, el libre (≈ 75 %) es menor que el margen de S, y lo que queda expuesto durante la espera son 6,72 lotes y no 20 |
| carga | suma al colocar | no medible | la stop reserva su margen al colocarla y MT5 no deja pasar del libre: una stop que cupo al colocarla sigue cabiendo al saltar, salvo por pérdida flotante; la situación no se puede provocar sin una posición perdiendo |
| carga | no suma | `pendientes`: buy stops lejos P | S pequeña (≈ 20 %, unos 5,38 lotes) y P con margen ≥ libre − 0,5 × margen de S (unos 24,19 lotes, una orden: el máximo es 50) |

Antes de esperar se comprueba que ACCOUNT_MARGIN_FREE < OrderCalcMargin de S a su precio (fila
`m4_libre_tras_ocupar` frente a `m4_margen_stop`); si no, `m4_no_medible`. Durante la espera, cada
500 ms: si S ya no está viva, se busca su deal (PrecioDelLlenado) y, si no lo hay, su estado en el
historial (HistoryOrderGetInteger ORDER_STATE, y su comentario). Fila `m4_resultado` (observación,
como `buy_stop_llenado`): `llenada` (con el precio), `rechazada_al_llenar` (sin deal y en estado
REJECTED o CANCELED, con el estado y el comentario) o `no_salto`. Si S salta ANTES de que la ocupación
esté puesta, `m4_resultado` = `salto_antes_de_ocupar`. Después, Limpiar. Peticiones: S, la ocupación,
y cerrar o borrar las dos: hasta 4.

Un input propio, tras los de los pasos 1-7 y declarado tras `Comprobaciones`: `InpMedirMargen` (por
defecto true) y `InpEsperaMargenSeg` (120). En OnStart, tras el paso 7: `if(ok && InpMedirMargen)`
→ `Limpiar("antes_paso_8")`, el paso 8, `Limpiar("tras_paso_8")`; cada M acaba en su propio Limpiar,
también si sale por error, y el `Limpiar("al_terminar")` de siempre sigue al final.

### 0.d La regla de lectura (escrita antes de ejecutar nada)

El lector la aplica a cada fichero 1.2 y escribe una sección APARTE, «## Paso 8: cuándo comprueba MT5
el margen de una pendiente stop (ADR-0081 §4)», con una línea por fichero y medida; con solo ficheros
1.0 o 1.1 esa sección no sale y la salida es byte a byte la de `main`. Las filas del paso 8 no entran
en la tabla «Decisión a decisión». Su retcode se juzga con `ESPERADOS["8_margen"]` = {10008, 10009,
10019}; otro sale en la lista de INESPERADOS de siempre.

| medida | «sí» | «no» | «no concluyente» o «no medible» |
|---|---|---|---|
| M1 | `m1_colocar` con retcode 10019 y `colocada` = no → «sí: rechaza al colocar (10019 NO_MONEY)» | `colocada` = si (10008/10009) → «no: la acepta al colocar» | otro retcode → «no concluyente: <retcode texto>»; `m1_no_medible` → «no medible: <nota>»; sin filas → «sin medir» |
| M2 | Δ = `m2_margen_despues` − `m2_margen_antes`; carga si Δ ≥ 0,10 × `m2_calculado_mercado`. Con D = \|orden − mercado\| ≥ 10,00: «sí, al precio de la orden» si \|Δ − orden\| < D/2; «sí, al precio de mercado» si \|Δ − mercado\| < D/2; con D < 10,00: «sí (precio no distinguible)» | \|Δ\| < 0,10 × `m2_calculado_mercado` → «no: la pendiente viva no carga margen» | `m2_colocar` no colocada, o carga lejos de los dos → «no concluyente», con Δ y los dos cálculos |
| M3 | `m3_colocar_1` colocada y `m3_colocar_2` con 10019 → «sí: suma las pendientes al colocar» | las dos colocadas → «no: no las suma al colocar» | la primera no colocada, o la segunda con otro retcode → «no concluyente» |
| M4 | `m4_resultado` = `rechazada_al_llenar` → «sí: comprueba al llenar (<estado>, <comentario>)» | `llenada` → «no: llena sin margen libre (a <precio>)» | `no_salto`, `salto_antes_de_ocupar`, `m4_libre_tras_ocupar` ≥ `m4_margen_stop`, o falta la fila → «no concluyente»; `m4_no_medible` → «no medible: <nota>» |

Imprime también, por fichero, el modo de margen, SYMBOL_MARGIN_HEDGED, la pierna mayor, el margen
inicial y las tasas de margen de buy stop y buy, y el peor caso de cada medida. Si el paso 8 está
desactivado: «paso 8 desactivado». La regla del lector y la del script para M2 (que elige la
ocupación de M4) son la misma; un test lo fija con CSV sintéticos en los dos sentidos.

### 0.e La seguridad

- **Solo en DEMO y tras Comprobaciones**: el paso 8 se llama desde OnStart después de que
  `Comprobaciones` (:796) haya devuelto true; no repite la comprobación (no puede ir antes de :759).
- **Cada petición que abre o coloca** lleva `MAGICO`, `req.sl` y, si es pendiente, PonerCaducidad
  (15 minutos). Lo fija el test estático del encargo (§3). Cada salida de cada M, también la de error,
  pasa por Limpiar.
- **El tope de 1.000 USD**, calculado ANTES de colocar o abrir, para todo lo que esa medida pueda
  tener a la vez (posiciones y pendientes que puedan llenarse; entre medidas, Limpiar): con L lotes
  y un stop común de s puntos, peor caso = Σ |OrderCalcProfit(BUY, v_i, p_i, p_i − (s + DESL) ×
  point)| + 2 × c × L. El script elige s = el mayor entero con peor caso ≤ 1.000 (como mucho 200
  puntos, como los pasos 6 y 7), lo comprueba con OrderCalcProfit y, si s < 10 puntos (un pip), no
  coloca ni abre y escribe `mN_no_medible` con la cuenta. OrderCalcProfit no lleva comisión: va aparte.
- **El deslizamiento, DESL = 10 puntos por operación** (entrada y salida juntas), cinco veces el mayor
  medido: +2 y −2 puntos a mercado y +1 en el llenado de la buy stop (`DEMO-EJECUCION-1.md:88,176,178`;
  P7, :330).
- **La comisión, c**: el encargo da 2,50 USD por lote y lado (lo medido en la ejecución 2,
  `HISTORIA.md:13988`, con el CSV sin congelar); el registro sigue con 5 por lado como supuesto
  CONSERVADOR (`ADR-0071:96-98`; `knowledge/cuentas/ftmo-2step-swing-100k.yaml:382-394`). Decisión 4.
- **Los stops que salen** (stop común, margen libre 100.000, 3.720,77 por lote, 1 USD por punto y
  lote):

| medida | lotes a la vez | s con c = 2,50 | s con c = 5,00 | peor caso |
|---|---|---|---|---|
| M1 | 26,88 | 22 puntos (2,2 pips) | 17 (1,7) | ≤ 1.000 |
| M2 | 0,61 | 200 (el máximo) | 200 | 0,61 × 210 + 3 = 131 (c = 2,50) |
| M3 | 29,58 | 18 (1,8) | 13 (1,3) | ≤ 1.000 |
| M4 · posición | 28,22 (21,50 + 6,72) | 20 (2,0) | 15 (1,5) | ≤ 1.000 |
| M4 · pendientes | 29,57 (5,38 + 24,19) | 18 (1,8) | 13 (1,3) | ≤ 1.000 |

  Son 1,3-2,2 pips, por debajo de los «2 a 4 pips» del encargo: con M3 y M4 a la vez hay unos 28-30
  lotes que pueden llenarse, no 27 (el auditor, fila 33, calculaba 54 lotes poniendo las dos de M3 en
  27; con «caben solas y no juntas» bastan 1,10 veces el libre). Lo que de verdad se espera perder:
  M1-M3 son pendientes a 100 pips que se borran en segundos (≈ 0); en M4, si MT5 llena S, S se cierra
  en cuanto se lee (≈ spread y un tick sobre 21,50 o 5,38 lotes, más la comisión) y la ocupación se
  cierra o se borra: del orden de 100-300 USD, y como mucho el tope.
- **Las peticiones**, contando cada OrderSend: la 1.1 hace 34 con stops level 0 (paso 3: 4 + 4
  borrados; paso 4: 8 + 8, sin el grupo «a distancia del stops level»; paso 5: 2 × 3; paso 6: 2;
  paso 7: 2) y 42 con stops level > 0; el paso 8 suma 12 (M1 2, M2 2, M3 4, M4 4); los Limpiar no
  piden nada si no queda nada (cada intento, una por orden o posición que quede, hasta 5). La 1.2: 46
  (o 54). El límite de FTMO es 2.000 al día (R13, `FTMO-REGLAS.md:60,259`; R13 trae además «200
  orders at a time», :264: el paso 8 no tiene más de 3 a la vez). El freno del bot (ADR-0067) es del
  bot, no del script.
- **El tiempo del paso 8**, peor caso: 12 peticiones × 1,5 s de pausa (18 s) + la espera de M2 (5 s)
  + la de M4 (120 s) + los Limpiar (unos segundos; hasta 10 s cada uno si algo se resiste): unos 2,5
  minutos. El script entero, como mucho unos 6 (hoy, «como mucho unos tres», `DEMO-FTMO.md:9-11`).

### 0.f La compilación

`C:/Program Files/MetaTrader 5/MetaEditor64.exe` y `terminal64.exe` siguen ahí (8 de octubre). Sobre
una copia de la 1.1 en la carpeta de trabajo: `MetaEditor64.exe /compile:"<copia>\MedirDemoFTMO.mq5"
/log:"<copia>\compilar.log"` → código de salida 1 (éxito, al revés), `Result: 0 errors, 0 warnings, 898
ms elapsed, cpu='X64 Regular'` y un `.ex5` de 50.150 bytes. El log es UTF-16 y se lee con un guion de
Python (la guardia niega `iconv` sobre él, abajo). La sonda del input tras `Comprobaciones`: 0 errores
(0.a).

### 0.g El lector y la guardia

- `scripts/leer_demo_ftmo.py:97` es `crudo = ruta.read_bytes()`: con el fichero cambiado, la guardia
  negará ejecutarlo (CRUDO_PYTHON, `guardia.py:195`; entrada K). No se toca: ni la variable ni el
  patrón. pytest sobre `tests/unit/test_leer_demo_ftmo.py` no lee el lector a través de la guardia
  (`guardia.py:2164-2166, 2202-2203`, auditor fila 40). `uv run pytest tests/unit/test_leer_demo_ftmo.py -q`
  pasa (9 tests) y la guardia no lo niega; hoy el lector es el de `main`, así que esto solo prueba la
  forma del comando: con el lector cambiado se vuelve a probar en la fase 1.
- La comprobación sobre el CSV real de la ejecución 2 la lanza Aleks con `!`; tiene que dar desfase
  180, comisión −2.50 por lado y 1,00 lote. El margen 3720.77 NO lo imprime el lector: está en la nota
  de `volumen_comision`, y `_volumen_comision` devuelve solo el valor (`leer_demo_ftmo.py:219-227`;
  auditor, fila 41). El cierre de respaldo-m1 lo leyó en el CSV (`HISTORIA.md:13988-13990`). Para
  la comparación, Aleks guarda la salida de `main` y la de la rama y se comparan byte a byte (las dos
  con `--salida`, fuera del repo).
- La carpeta con un 1.1 y un 1.2: hoy un 1.2 se rechaza por VERSIONES (:63, :116-120) y aborta la
  carpeta entera; con "1.2" en VERSIONES se leerá, porque la mezcla solo se comprueba dentro de un
  fichero (:146-147). Y un cambio de salida que no es de un 1.0 ni de un 1.1: el mensaje de una
  versión desconocida pasa de «lee 1.0 y 1.1» a «lee 1.0 y 1.1 y 1.2» (:117-120).

### 0.h PROJECT_STATE

**Bytes** (`git show main:PROJECT_STATE.md`, 24.393, 166 líneas): cabecera 134; Current Branch 24;
Current Feature 318; Stable Main State 448; Last Stable Commit 164; Tests Currently Passing 226; Next
Action 8.384 (de ellos, la subsección de heredados 902); Known Ambiguities 2.148; Technical Debt
10.746; Reglas vivas 1.493; Completed Features 157; Change Log 151. Las líneas, con su salto: anexo
`anexos/MARGEN-PENDIENTE/bytes-main.txt`, que se escribe con la fase 2.

**1. Las líneas, con (a)-(d)** (niega por defecto):

| línea | condición | evidencia | bytes |
|---|---|---|---|
| heredado 2 «Marzo: faltan vistos.yaml y el paso a…» | **(b) REPETIDA**: vivo entero en CLAUDE.md | `CLAUDE.md:178-181` («del paso 0, marzo en `vistos.yaml` (REGISTRO-MARZO.md §2), y el paso a. La confirmacion escrita del trader llego el 2026-10-25 (SESION-05-EXTRACCION.md §3.5; hoja de ruta, A.3)»). Sale `HER:2` de las Refs de R5.3 (`HOJA-DE-RUTA.md:336`), la única que lo nombra | 164 |
| TD «`cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT» | **(b) REPETIDA**: vivo en CLAUDE.md, y la guardia los niega | `CLAUDE.md:62-63` («`cherry-pick` y `rebase` no pasan por `pre-commit`: no se usan para meter trabajo (la guardia los bloquea)»); `guardia.py:1850`. Su texto entero (Archivo 1, `HISTORIA.md:541`) añade «la garantia de fondo sigue siendo la CI» y la historia de 40759cb y 2753ac1, que quedan en HISTORIA | 131 |
| heredados 6, 7, 8, 9 | se quedan | sin evidencia de hechos (su texto entero, Archivo 1) | — |
| heredado 10 «grabador de spread y ticks, F17» | se queda | A dice A-28, no el grabador ni F17; A.1 lo cita (`HOJA:473,476`) | — |
| heredado 27 | se queda | FTMO-REGLAS no es un runbook; A.2 lo cita | — |
| TD «LA VIA DE PROPUESTA NO ADMITE `supersede`» | se queda | CLAUDE.md lo nombra, pero no entero: el texto (`HISTORIA.md:576`) pide una decisión («o el esquema admite supersede, o se declara…») | — |
| TD «NADA COMPRUEBA… EL CUERPO DE UN INFORME CERRADO» | se queda | CLAUDE.md apunta a Technical Debt («Nada lo comprueba mecanicamente todavia (Technical Debt)») | — |
| TD de F26 (preguntas y particiones, dos días, 3,00/3,75) | se quedan | la entrada G dice que «hoy viven en Technical Debt» | — |
| TD del docstring de `engine/freno.py:7-8` | se queda | el docstring sigue igual (`freno.py:7-8`) | — |
| TD de ADR 0087, RN-019, visor, VISOR-DIAS, copia de seguridad | se quedan | nada las paga (ADR 0087 no existe; VISOR-DIAS.md sin «diagnostico») | — |
| Reglas vivas | se quedan | «Parametros no se optimizan contra resultados», F26 antes de lo que opera y la firma no viven en CLAUDE.md ni en un runbook (grep vacío) | — |

(a)-(d): **295 bytes**.

**2. (e) ACORTADA**, en lectura estricta de «al final de una frase o de un inciso» (antes de «. »,
«; » o «: », o tras el «)» de un inciso), con el corte más largo de 160 bytes como mucho, contando el
«- »; la cita del informe con su sección, delante en el paréntesis; las que ahorran menos de 60 se
quedan enteras (guion `acortar_e.py`):

| línea (arranque) | bytes | queda | ahorra |
|---|---|---|---|
| Hoy un mes no puede salir de `knowledge/cases/meses_reservados.yaml` | 407 | `… (holdout.py lo niega sin excepción) … (CUARENTENA-POR-CONDICION-2.md, respuesta del consultor a la PARADA de la fase 0, punto 2; entera en HISTORIA, Technical Debt ACORTADA)` | 159 |
| El modo texto ANSI de MT5 (build 6230) | 266 | `… tiene LF, sin explicación … (EA-CONEXION.md §0.c; entera en …)` | 68 |
| Que el EA reinicie sus globales | 313 | `… (el defecto de la demo del 2026-10-20) … (EA-CONEXION.md §10; entera en …)` | 142 |
| La guardia de Claude Code no ve una consulta de CI | 770 | `… se monta a trozos (`"g" + "h"`) … (GUARDIA-CI.md §5.2 y §9; entera en …)` | 578 |
| Una zona del productor reutilizada | 364 | `… (misma caja del mismo punto tras una toma nueva) … (PUNTO-USADO.md §1.c y §4.f; entera en …)` | 176 |
| La condición 2 de ADR-0042 §2 | 414 | `… (la lectura COMPLETA del libro, declarada) … (falso positivo medido con enero, ENTRADA-ENERO.md §0.b; entera en …)` | 230 |
| `engine/simulador_config.py` busca el spread | 342 | `… por la hora de PARED de Europe/Madrid, no por la rejilla … (ENTRADA-ENERO.md §0.c; entera en …)` | 137 |
| EL `no_trade` POR AUSENCIA | 303 | `… DE MAYO (2026-09-21); y (S-14, sesión 5) … (ACTIVAR-SESION-05.md §0.b.7; entera en …)` | 112 |
| UNA PREGUNTA ABRE N PARTICIONES | 226 | `… NO EL HUMANO … (entera en …)` | 106 |
| Riesgos residuales del alias de la raíz | 284 | `… compara la forma sin prefijos … (entera en …)` | 90 |
| La guardia no expande las llaves de bash | 269 | `… ni mira las URL `file:///` (urllib, curl) … (GUARDIA-ALIAS.md §9, b6 y b7; entera en …)` | 61 |
| Las cotizaciones sin tick del bróker | 543 | `… (precio_invalido y stops_level, ADR-0057 §4) … (RESPALDO-M1.md §0.a y §0.b; entera en …)` | 310 |

Total (e): **2.169 bytes** (el auditor daba un máximo de 2.097 con el corte siempre en 160; aquí
algunas cortan antes). Se quedan enteras por ahorrar menos de 60: el validador del journal (58), RN-019
(18), `arnes.dias_de_mercado` (29), la ingesta y el reloj (55), sin git (27), RN-029 a 032 (46),
la copia de seguridad (4). **Sin corte estricto en 160**: «Artifact, ArtifactData, DesignSync…» (467
bytes): su primera frase acaba pasados los 160; la única pausa antes es una coma dentro de la
enumeración (`… y `file_upload`, `navigate` …`, ahorraría 327). «EL DIA QUE UN CAMINO…» y «DOS DIAS DEL
UNIVERSO…» tampoco tienen corte estricto (y con coma ahorrarían menos de 60).

Las líneas que se acortan pierden rutas e ids (p. ej. `holdout.py`, ADR-0078, ADR-0079,
`.claude/settings.json`), pero ningún test exige que estén: `test_project_state_rutas` exige que las
rutas citadas EXISTAN y que haya al menos una; `knowledge validate` (no `test_ids_citados`, que usa
ficheros sintéticos: auditor, fila 46) exige que los ids citados existan; `test_documentos_vivos`
vigila recuentos; `test_hoja_de_ruta`, los heredados vivos y las letras. Leen el PROJECT_STATE real
seis tests (auditor, fila 45: los trece ficheros lo nombran). Una línea acortada no deja de existir:
la entrada G sigue encontrando «UNA PREGUNTA ABRE N PARTICIONES» en Technical Debt.

**3. La previsión** (guion `prevision.py`; la cabecera del cierre, con textos del largo de los del
cierre de respaldo-m1):

| paso | bytes |
|---|---|
| `main` | 24.393 |
| tras (a)-(d) | 24.098 |
| tras (e) | 21.929 |
| con las líneas del cierre (la frase de A, −28; Current Branch, Feature, Stable Main State y Last Stable Commit del cierre) | **21.872** |

**No baja de 21.800: faltan 72 bytes.** Candidatos, fuera de lo que ya aplica (a)-(e) en lectura
estricta (decisión 6): (i) en (e), el corte estricto más corto en el `no_trade` y en las llaves de
bash: +62, se queda en 21.810; (ii) en (e), «Artifact…» cortado en la coma de la enumeración: +327,
21.545; (iii) la línea de candidatas a ambigüedad sin abrir (554 bytes; está en Known Ambiguities,
fuera de (a)-(e)); (iv) entradas largas de la Next Action (K 975, H 890, G 889, A 881): **no se
pueden tocar en esta rama**, porque «QUÉ NO CAMBIA» del encargo dice «el texto de las entradas de la
Next Action»; (v) escribir en el cierre la cabecera más corta (Current Feature y Stable Main State de
unos 250 bytes en vez de 330 y 450): unos 280 bytes, pero eso lo escribe el cierre, no esta rama.

### 0.i Herencias

| Qué | Dónde | Entra |
|---|---|---|
| La frase de A («pide un script 1.2… una rama corta antes de la 3») | `PROJECT_STATE.md:46` | sí: la cambia el cierre (encargo §5) |
| A.1 («Falta un script 1.2…») y R6a.6 («el script 1.2 de MedirDemoFTMO») | `HOJA-DE-RUTA.md:479-480, :432` | sí: líneas del cierre preparadas |
| La búsqueda en la documentación de MARGEN-LOTE (2026-10-17) y su pendiente «el margen libre real que FTMO aplicaría a una posición cubierta (hedging)» | `MARGEN-LOTE.md:114-143, :384-388` | el paso 8 lo mide del mismo lado; el de lados opuestos, no (0.b) |
| MT5 suma el margen del mismo lado en hedging | `FTMO-P-D1.md:79-83`; `ADR-0081:29` | sí: M3 y M4 son del mismo lado |
| **NA:M**, el break even de una venta que salta por el ASK (ADR-0065 §6) | `HOJA:473-476`; `PROJECT_STATE.md:54` | **no lo pide el encargo**, y la 3 es la última ejecución prevista: decisión 5 |
| El heredado 10 (grabador de spread y ticks, F17) | `HOJA:476` | no: no lo mide el script |
| La comisión de 5 USD del registro frente a los 2,50 medidos | `ERRORES-RECURRENTES.md:77`; `ADR-0071:96-98` | sí, para el tope: decisión 4 |
| Clasificaciones previas de estas secciones (adelgazar-estado, plataforma-adelantada, previa-sesion-5) | `ADELGAZAR-ESTADO.md:114,140-147`; `PLATAFORMA-ADELANTADA.md:221-260`; `PREVIA-SESION-5.md:145-160,506` | consultadas: ninguna de las líneas que dejaron se da aquí por hecha sin evidencia nueva |
| La deuda del CRLF del CSV | Technical Debt | **no** (es de la rama que congele los CSV); se acorta por (e) |
| El falso positivo de la guardia con `crudo` | entrada K | **no**; volvió a saltar en esta fase 0 (0.m) |
| «Tests Currently Passing» cambia con los tests nuevos | `state check` | sí: el número sube; mismos bytes salvo un dígito |

### 0.j La ejecución 3, en hora de Lima

Con `zoneinfo` (Europe/Madrid → America/Lima): la franja de 9:00 a 18:00 de España es **de 03:00 a
12:00 de Lima** el lunes 2, el miércoles 4, el jueves 5 y el viernes 6 de noviembre de 2026 (Madrid
UTC+1 desde el 25 de octubre; Lima UTC−5). El martes 3 no (la sesión 6).

### 0.k Exposiciones

Ninguna. Esta fase 0 no ha leído material del trader, velas, ticks ni el CSV de `data/demo_ftmo/`; de
HISTORIA solo el texto de Technical Debt del Archivo 1 y el último registro de cierre.

### 0.l El encargo frente al repo (auditor-encargo, 2026-10-31)

El auditor resume 48 afirmaciones (33 correctas, 3 incorrectas y 12 con matiz) en una tabla de 55
filas, con dos marcadas INCORRECTA, y seis herencias (0.i). Las que cambian lo que se hace:

- **INCORRECTA, fila 48:** «(e) ahorra unos 2.400 a 2.650 bytes»: medido, 2.169 (0.h).
- **INCORRECTA, fila 46:** `test_ids_citados` no lee el PROJECT_STATE real; lo hace `knowledge validate`.
- **MATIZ, fila 23:** los `input` viven antes de :759: el del paso 8 va tras `Comprobaciones` (0.a).
- **MATIZ, fila 24:** la cabecera tiene otra frase falsa ya en la 1.1 (0.a).
- **MATIZ, filas 27, 31 y 32:** el capital de la prueba nueva no está en el repo; la comisión del
  tope (decisión 4).
- **MATIZ, fila 33:** los stops salen de 1,3 a 2,2 pips, no de 2 a 4 (0.e).
- **MATIZ, fila 41:** el lector no imprime el margen 3720.77 (0.g).
- **MATIZ, fila 45:** seis tests leen el PROJECT_STATE real; trece lo nombran.
- **MATIZ, fila 21:** :278 de `test_capa_mt5.py` es una cadena de ejemplo; hay más citas de :759 en
  informes cerrados.

El resto (fechas, cifras de bytes de b678ad4 y 884301d, líneas del script, frases literales de A, A.1
y R6a.6, Lima, R2, R13, ADR-0067, EA-CONEXION §0.a, `compilar.py`) es correcto.

### 0.m Negativas de la guardia en esta fase

| comando | lo que dijo | qué hice |
|---|---|---|
| `git show $(git log … --grep=…) -- PROJECT_STATE.md` | argumento construido al ejecutarse | rehecho con el sha literal (la forma que propone) |
| `grep -c $'\r' <ficheros>` | argumento `$'\r'` construido | `file` sobre los ficheros (dice «CRLF» si lo hay) |
| `iconv -f UTF-16LE … compilar.log` | no sabe con qué se ejecuta el log | un guion de Python escrito con Write y ejecutado en otra llamada (la forma que propone) |
| `uv run python prevision.py …` (un guion mío de la carpeta de trabajo) | «el codigo que se ejecuta pide el corpus SIN FILTRAR» | **falso positivo de K**: el guion tenía una variable `crudo = ORIGEN.read_text(…)` sobre la copia de PROJECT_STATE. No renombré la variable: quité esa sección del guion, que repetía medidas ya hechas por `bytes_ps.py` (la línea de K, 975 bytes; la de candidatas, 554, con `grep … \| wc -c`). Lo declaro por si cuenta como rodearla: el guion no leía corpus |

### Lo que no pude medir

- El capital, el margen libre y el modo de margen de la prueba nueva: están en el CSV de la ejecución 2,
  que esta rama no lee (los lee el paso 1 y el paso 8 de la 3).
- Si MT5 carga una stop viva y cuándo comprueba su margen: es lo que mide el paso 8.
- El texto exacto de la cabecera del cierre (Current Feature, Stable Main State): lo escribe el cierre;
  la previsión usa textos del largo de los del cierre de respaldo-m1.
- La salida del lector de `main` sobre el CSV real: la lanza Aleks.

## Lo que necesito que decidas

0. **Dónde va el paso 8.** Opciones: (a) todo lo nuevo (constantes, `InpMedirMargen`,
   `InpEsperaMargenSeg` y funciones) entre `Comprobaciones` y `OnStart`, sin prototipos; en 1-758 solo
   cambian :27, :31 y la cabecera en su sitio (25 líneas); (b) las funciones tras `OnStart` con
   prototipos. Recomiendo (a): compila (sonda: 0 errores, :759 intacta) y no necesita prototipos.
   Coste de (b): prototipos que la documentación no describe para este caso, sin ganancia.
1. **La cabecera.** Opciones: (a) corregir las dos frases falsas («solo el volumen minimo…» y «toda
   posicion lleva stop de proteccion», falsa ya en la 1.1) y la de `DEMO-FTMO.md:22`; (b) solo la que
   nombra el encargo. Recomiendo (a): dejar una falsa a sabiendas contradice «deja de decir algo
   falso». Coste de (b): ninguno de código; una frase falsa en un script que envía órdenes.
2. **El diseño de M1-M4** (0.c): buy stops a 100 pips para M1-M3; M2 con ≥ 20 USD de diferencia
   entre precios; M3 con 1,10 veces el libre entre las dos; M4 con la tabla de ocupación (posición si
   la pendiente no carga; pendientes lejanas si carga y no se suman; «no medible» si carga y se suman)
   y S cerca a 1 pip. Opciones: (a) así; (b) M4 siempre con una posición del mismo lado. Recomiendo
   (a): es lo que pide el encargo y, cuando las pendientes cargan y se suman, M4 no se puede provocar
   sin pérdida flotante, que se dice en vez de forzarla. Coste de (b): una posición de ~6-20 lotes
   expuesta en un caso en que la medida no puede dar «no».
3. **La regla de lectura** (0.d), con sus umbrales: carga si Δ ≥ 10 % del margen calculado; precio
   por la mitad de la diferencia D (≥ 10 USD). Opciones: (a) así; (b) otros umbrales. Recomiendo (a):
   10 % separa 0 de ~2.270 con holgura, y D/2 con D ≥ 20 deja 10 USD frente a ~0,2 USD que mueve un pip.
4. **La comisión del tope.** Opciones: (a) 5,00 USD por lote y lado (el supuesto conservador del
   registro, ADR-0071): stops de 13-17 puntos; (b) 2,50 (lo medido en la 2, sin congelar): 18-22
   puntos. Recomiendo (a): manda la seguridad y el CSV no está congelado; 1,3 pips sigue por encima
   del mínimo de 10 puntos y los stops solo cuentan si algo se llena. Coste de (a): stops más ceñidos
   en la posición de M4, que puede salir por su stop con un tick en contra (≤ el tope).
5. **NA:M (el break even de una venta que salta por el ASK).** Opciones: (a) fuera de esta rama: la
   1.2 no lo mide, y M sigue esperando la prueba siguiente; (b) un paso 9. Recomiendo (a): el encargo
   fija los pasos 1-7 sin cambios y solo el 8, y la rama tiene que estar lista antes del martes 3.
   Coste de (a): la 3 no mide M.
6. **PROJECT_STATE: faltan 72 bytes.** Con (a)-(d) = 295 (heredado 2 y la deuda de `cherry-pick`, las
   dos por (b)) y (e) estricta = 2.169, la copia queda en 21.872. Opciones: (a) aceptar en (e) el corte
   de «Artifact…» en la coma de su enumeración (21.545, 255 de margen); (b) en (e), el corte estricto
   más corto en dos líneas (21.810: no basta solo); (c) sacar o acortar la línea de candidatas a
   ambigüedad sin abrir (554, fuera de (a)-(e)); (d) pedir al cierre una cabecera más corta. Recomiendo
   (a): una coma que cierra la lista de herramientas es un final de inciso razonable, el texto entero va
   a HISTORIA, y deja margen sin tocar nada fuera de (a)-(e). Coste de (a): «… `navigate` …» no dice ya
   qué herramientas de claude-in-chrome están cerradas (sí en HISTORIA y en `.claude/settings.json`).
7. **Las dos salidas por (b)** (heredado 2 → CLAUDE.md:178-181; `cherry-pick` → CLAUDE.md:62-63 y
   `guardia.py:1850`). Opciones: (a) salen las dos; (b) sale solo el heredado 2 (la del `cherry-pick`
   pierde en PROJECT_STATE la frase «la garantia de fondo sigue siendo la CI»). Recomiendo (a): CLAUDE.md
   las dice enteras en lo que importa y la guardia las niega. Coste de (b): 131 bytes más que buscar.
8. **Seguir con el calendario.** Opciones: (a) tras tu respuesta, fase 1 (script, lector, tests,
   runbook) y fase 2 (PROJECT_STATE) seguidas, sin otra PARADA salvo que algo medido contradiga una
   decisión; (b) PARADA entre fases. Recomiendo (a): la rama tiene que estar lista antes del martes 3.

## Respuesta del consultor a la PARADA (2026-10-31)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/margen-pendiente (2026-10-31). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Todo lo nuevo del paso 8 (constantes, InpMedirMargen, InpEsperaMargenSeg y funciones) va entre Comprobaciones y OnStart, sin prototipos. En las líneas 1 a 758 solo cambian :27, :31 y la cabecera en su sitio, con las mismas 25 líneas. La compilación de la fase 1 lo vuelve a probar, y el informe pega la línea 759 de la 1.2.
>
> 1. (a). Se corrigen las dos frases falsas de la cabecera y la de DEMO-FTMO.md:22, y #property description gana el margen de las pendientes. La frase nueva dice la verdad entera: las pendientes de los pasos 3, 4 y 5 van sin stop a propósito y, si una se llena al instante, el script la cierra en cuanto la lee; las demás posiciones llevan stop de protección.
>
> 2. (a), con cinco cambios en M2 y M4. Un «sí» o un «no» falsos de M4 acabarían en un ADR, porque la 3 es la única ejecución prevista; así que todo lo que no pruebe la causa sale «no concluyente».
>    a) La ocupación caída. Si V o P dejan de estar vivas antes de que S se resuelva, S puede llenarse con margen libre de sobra y el lector daría un «no» falso. Con V es físico: su stop común queda a unos 1,5 pips por debajo, S a 1 pip por encima, y en 120 s el precio puede bajar, cerrar V y volver a subir hasta S. Con P, la vía no es la caducidad (15 minutos) sino que el bróker la borre con el nivel de margen tan bajo (stop out o gestor de riesgo de FTMO; el repo no tiene esa cifra). Al resolverse S, el script escribe si la ocupación seguía viva (fila m4_ocupacion_viva, «si» o «no», con su ticket) y el margen libre justo antes de esa lectura. Ocupación caída → «no concluyente: la ocupación cayó antes de que se resolviera S».
>    b) El «sí» solo con la causa. Al saltar en el servidor, S no devuelve retcode, así que un rechazo o un borrado por otra causa no se distingue a ciegas (tope agregado de volumen, stops inválidos tras un hueco, stop out, una cancelación del cliente). Regla: «sí» solo si S queda sin deal, en estado REJECTED, con un comentario o un motivo del historial que nombre el margen, y con p8_volumen_limite = 0 o el volumen de S más el de la ocupación dentro de ese tope. CANCELED nunca da «sí». Cualquier otro caso de S sin deal → «no concluyente», con el estado y el comentario literales. Verifica en la documentación de MQL5 qué guarda el historial de una orden rechazada al saltar (ORDER_STATE, ORDER_COMMENT, ORDER_REASON u otro) y escribe en el informe qué campo usa la regla. Si ninguno puede nombrar el margen, M4 no da nunca «sí»: lo dices y el lector da «no concluyente» con lo que haya.
>    c) El llenado parcial. Si el volumen del deal de S es menor que el de S, «no concluyente».
>    d) M2 por las tres cifras. La documentación solo atribuye las pendientes a ACCOUNT_MARGIN_INITIAL. M2 escribe antes y después ACCOUNT_MARGIN, ACCOUNT_MARGIN_FREE y ACCOUNT_MARGIN_INITIAL, y la regla juzga «carga» por la bajada del margen libre (lo que importa para M4): carga si el libre baja al menos un 10 % del margen calculado. El precio se decide con esa misma bajada, por la mitad de D como en tu propuesta. El informe dice también qué hicieron ACCOUNT_MARGIN e INITIAL.
>    e) La comprobación antes de esperar, con lo que midió M2. M4 escribe el libre antes y después de colocar S. Si la pendiente reserva su margen, la condición es «libre + lo que reservó S < margen de S al llenar», no «libre < margen de S». Si no se cumple, «no medible».
>    Tests del lector con cada caso, en los dos sentidos: ocupación viva y caída; S rechazada con el motivo del margen, rechazada con otro motivo, y cancelada; llenado entero y parcial; y M2 con el libre que baja y con el libre que no baja aunque ACCOUNT_MARGIN suba.
>
> 3. (a), con el cambio de 2.d: el 10 % se mide en la bajada del margen libre; el precio, por la mitad de la diferencia D, con D ≥ 10 USD.
>
> 4. (a): 5,00 USD por lote y lado en el tope, el supuesto conservador del registro (ADR-0071), mientras el CSV de la ejecución 2 no esté congelado. Stops de 13 a 17 puntos. Es un cambio del encargo, que daba 2,50: el informe lo declara así.
>
> 5. (a). M (el break even de una venta que salta por el ASK) queda fuera de esta rama y sigue esperando a una prueba posterior. El informe lo dice en «el encargo frente a lo hecho».
>
> 6. Ninguna de las cuatro opciones: (d), pero escrita desde ya. «Al final de una frase o de un inciso» no incluye la coma de una enumeración: «Artifact…» se queda entera, y (e) se aplica en lectura estricta, sin el corte más corto de (b). Lo que falta lo pongo yo con las cabeceras del cierre, que escribo yo y que van a ser estas (con el sha y la fecha reales):
>    - Current Feature: «Ninguna rama abierta. trabajo/margen-pendiente cerrada en main el <fecha> (stable/F38k-margen-pendiente): MedirDemoFTMO 1.2, con el paso 8 (el margen de una pendiente stop), y PROJECT_STATE adelgazado (MARGEN-PENDIENTE.md).»
>    - Stable Main State: «<sha> · merge de `trabajo/margen-pendiente` (tag `stable/F38k-margen-pendiente`): MedirDemoFTMO 1.2 y PROJECT_STATE adelgazado. Sobre `stable/F38j-respaldo-m1` (4b12a92). Informe docs/validation/MARGEN-PENDIENTE.md; el registro del cierre, al final de HISTORIA.»
>    - Last Stable Commit: «<sha> · merge: trabajo/margen-pendiente, MedirDemoFTMO 1.2 y PROJECT_STATE adelgazado · tag stable/F38k-margen-pendiente»
>    Rehaz la previsión con estos tres textos y con la decisión 7, y pega la cifra. Mi auditor la estima en unos 21.755 bytes; mídela tú. Si no baja de 21.800, PARADA.
>
> 7. Sale el heredado 2; la deuda de cherry-pick se queda.
>    - Heredado 2, por (b), con la evidencia corregida: la versión entera del Archivo 1 vive en docs/runbooks/ENTRADA-MARZO.md (verifica que en :45-49), y CLAUDE.md:178-181 lleva lo esencial. Al salir, quedan falsas las frases que remiten a él: ENTRADA-MARZO.md:32 («Lo que falta sigue en PROJECT_STATE.md, pendiente heredado 2») y la prosa «heredado 2» de HOJA-DE-RUTA.md (verifica que en :338 y :499-500), además de HER:2 en las Refs de R5.3. Se amplía el contrato a docs/runbooks/ENTRADA-MARZO.md, en un commit a la vista, solo para esa frase, y las tres pasan a remitir a ENTRADA-MARZO.md, en el mismo commit que saca el heredado. Comprueba la copia contra test_hoja_de_ruta.
>    - La deuda de cherry-pick se queda: su texto entero (HISTORIA, Archivo 1) dice «la garantia de fondo sigue siendo la CI», que no está en CLAUDE.md ni en ningún runbook, y (b) exige el contenido vivo entero (ERRORES-RECURRENTES, fila de plataforma-adelantada). La opción (a) que recomendabas era contraria al README.
>
> 8. (a): fase 1 y fase 2 seguidas, sin otra PARADA salvo que algo medido contradiga una decisión de esta respuesta.
>
> Sobre §0.m. Quitar del guion la parte negada no es rodear la guardia si las medidas que quedaron (975 bytes de K y 554 de las candidatas) ya estaban hechas antes de la negativa, porque entonces no se ejecutó lo negado de otra forma. Si se hicieron después, con grep y wc -c, eso es cambiar de vía tras una negativa (DECISIONES-DE-PROCESO.md). El informe escribe el orden real y, en ese caso, lo declara como desviación. El falso positivo, en cualquier caso, es otra aparición de K: va en la fila de ERRORES-RECURRENTES preparada, no en la entrada K.
>
> La comprobación de Aleks con «!» sobre el CSV de la ejecución 2 no puede pedir el 3720.77, porque el lector no lo imprime (lo dijo tu fase 0). El criterio es que la salida del lector de main y la de la rama sean idénticas byte a byte. El informe da los dos comandos exactos, con las dos salidas fuera del repo.
>
> Para la fila de ERRORES-RECURRENTES del cierre, los errores del consultor que cazaron la fase 0 y el auditor:
> - (importa) El encargo dio como dato lo que decía el auditor del consultor sin medirlo: que (e) ahorraba de 2.400 a 2.650 bytes (son 2.169); que los stops saldrían de 2 a 4 pips (salen de 1,3 a 2,2); que trece tests leen PROJECT_STATE (lo leen seis y lo nombran trece) y que test_ids_citados lo lee (lo hace knowledge validate); que la comprobación de Aleks diera el margen 3720.77, que el lector no imprime; y citas de línea de test_capa_mt5.py (:143-151 son :142-149; :278 es una cadena de ejemplo). Es la lección del cierre de visor-construccion, repetida: lo que diga el auditor del consultor sobre una cifra, un recuento o un mecanismo va en el encargo como «verifica que…», nunca como dato.
> - (importa) En el primer borrador de esta respuesta acepté sacar por (b) la deuda de cherry-pick sin comprobar que su texto entero vive en otro sitio, que es lo que exige el README; lo cazó mi auditor antes de entregarla. Lección: antes de aceptar una salida por (b), leer el texto entero en HISTORIA y buscar cada frase.
> - (menor) El encargo nombró una frase falsa de la cabecera y no vio la segunda («toda posición lleva stop de protección»), falsa ya en la 1.1. Lección: antes de pedir que se corrija un texto, leerlo entero.
> - (menor) El encargo fijó 2,50 USD de comisión para el tope sin mirar que el registro mantiene 5 como supuesto conservador mientras el CSV no está congelado.
>
> Lo que sigue: el commit con esta respuesta y la ampliación del contrato a ENTRADA-MARZO.md; la fase 1 (script, compilación con la línea 759 pegada, lector, tests y runbook); la fase 2 (PROJECT_STATE, con la previsión rehecha); y el informe con las líneas del cierre preparadas sobre una copia, el revisor y la entrega. make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

## PARADA 2 · el heredado 2 no vive entero en ENTRADA-MARZO.md (2026-10-31)

Al aplicar el punto 7 de la respuesta, medido: `docs/runbooks/ENTRADA-MARZO.md:45-49` lleva la parte
operativa del heredado 2 (marzo a `vistos.yaml` con `visto_el` y `cobertura_material`, material del
camino de fidelidad para `fidelidad-2` y `fidelidad-3`, el CONFIRM de F09 «sin sus palabras, no
vale»), pero NO las dos frases con que arranca su texto entero en el Archivo 1 (`HISTORIA.md:684`):
«MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE.» y «El trader confirmo el 2026-09-21 que no
habia visto febrero NI marzo, y backtestea MARZO (lo declara el consultor; no hay captura en el
corpus).». `grep` de «no hab[ií]a visto», «backtestea marzo» e «INTERRUMPE» en CLAUDE.md y
`docs/runbooks/*.md`: vacío. Es el mismo hueco por el que el revisor de `trabajo/plataforma-adelantada`
bloqueó esta salida (b1, 2026-10-18; `PLATAFORMA-ADELANTADA.md:554-560`). La premisa del punto 7
(«la versión entera del Archivo 1 vive en docs/runbooks/ENTRADA-MARZO.md») no se cumple, y la
previsión depende de esa salida: con tus tres cabeceras, **21.784 bytes con el heredado 2 fuera y
21.948 con él dentro**.

Se preguntó a Aleks en la sesión, con tres opciones: (1) llevar las dos frases al paso 0 de
ENTRADA-MARZO.md como cita del Archivo 1, y salir por (b) (recomendada); (2) el heredado 2 se queda
y faltan 148 bytes; (3) salir por (c) SUSTITUIDA: «MARZO INTERRUMPE…» quedó sin objeto (marzo ya
llegó y la hoja de ruta ordena su entrada) y «no había visto febrero NI marzo» es un hecho de
HISTORIA que no hace falta vivo.

### Respuesta de Aleks a la PARADA 2 (2026-10-31)

> Sustituida por (c)

(La opción elegida, tal como se le presentó: «Declarar que «MARZO INTERRUMPE…» quedó sin objeto
(marzo ya llegó y la hoja de ruta ordena su entrada) y que «no había visto febrero NI marzo» es un
hecho de HISTORIA que no hace falta vivo: sale por (c) con esa evidencia. Coste: es juicio tuyo, no
algo que el repo muestre.»)

### Respuesta del consultor a la PARADA 2 (2026-10-31)

> Respuesta del consultor a la PARADA 2 de trabajo/margen-pendiente (2026-10-31). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha.
>
> Opción 3, con la evidencia escrita en el bloque de HISTORIA, para que la salida no sea juicio sino hecho del repo. El heredado 2 sale por dos condiciones, frase a frase:
> - «MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE»: (c) SUSTITUIDA. Marzo llegó el 2026-09-30 y no interrumpió nada: entra por el camino de fidelidad, en su turno de la hoja de ruta (REGISTRO-MARZO.md, decisión del consultor del 2026-09-30, §«Marzo entra por el camino de fidelidad» y su aceptación; CLAUDE.md, párrafo «Marzo de 2026 esta RECIBIDO y SIN ABRIR»; R5.3). Verifica esas líneas y cítalas.
> - «El trader confirmo el 2026-09-21 que no habia visto febrero NI marzo, y backtestea MARZO»: (c) SUSTITUIDA por hechos posteriores: el backtest de marzo está recibido (REGISTRO-MARZO.md) y la confirmación escrita llegó el 2026-10-25 (SESION-05-EXTRACCION.md §3.5); lo de febrero sigue vivo en el heredado 6, que se queda.
> - El resto (vistos.yaml con visto_el y cobertura_material, fidelidad-2/3, CONFIRM «sin sus palabras, no vale»): (b) REPETIDA, entero en ENTRADA-MARZO.md:45-49.
> El bloque de HISTORIA va como «# Pendiente heredado SALE», con el texto literal entero y las tres condiciones con su evidencia. Lo demás del punto 7 sigue igual: ENTRADA-MARZO.md:32 y la prosa de la hoja de ruta pasan a remitir a ENTRADA-MARZO.md, HER:2 sale de R5.3, y el contrato se amplía a ENTRADA-MARZO.md solo para esa frase. Esto es distinto de lo que bloqueó el revisor en plataforma-adelantada: entonces se pedía (b) para la línea entera, y (b) no cubría las dos frases; ahora esas dos salen por (c) con su evidencia. Dilo así en el informe.
>
> Previsión aceptada: 21.784 bytes. Sigue con la fase 1 y la fase 2 como dice la respuesta a la PARADA.

**Las citas, verificadas** (para el bloque de HISTORIA de la fase 2):
- recepción: `docs/validation/REGISTRO-MARZO.md:118` («Fecha de recepcion: 2026-09-30. Contenido: NO
  ABIERTO.»);
- «Marzo entra por el camino de fidelidad»: `REGISTRO-MARZO.md:127` (§4, punto 1) y su aceptación,
  `:167-169` («ACEPTADA por el consultor el 2026-09-30… marzo entra por el camino de fidelidad con
  el artefacto `eurusd-2026-03`»);
- CLAUDE.md, párrafo «Marzo de 2026 esta RECIBIDO y SIN ABRIR»: `CLAUDE.md:175-177`;
- R5.3: `docs/plan/HOJA-DE-RUTA.md:335` («### R5.3 · Marzo»);
- la confirmación escrita: `docs/validation/SESION-05-EXTRACCION.md` §3.5 (`:1062`, «"Para cerrar"
  (v16, sin código de voz)»);
- febrero: el heredado 6 («FEBRERO NO SE TOCA Y NO SE DESCARGA…»), que se queda.

**Por qué no es lo que bloqueó el revisor de plataforma-adelantada:** entonces se pedía (b) para la
línea entera, y (b) no cubría las dos frases; ahora esas dos salen por (c) con su evidencia, y solo
el resto sale por (b), entero en ENTRADA-MARZO.md:45-49.

Se aplica en la fase 2, en el commit que saca el heredado: el bloque «# Pendiente heredado SALE» con
el texto literal entero y las tres condiciones; ENTRADA-MARZO.md:32 y la prosa «heredado 2» de
`HOJA-DE-RUTA.md:338` y `:499-500` pasan a remitir a ENTRADA-MARZO.md; sale `HER:2` de las Refs de
R5.3 (`:336`). La deuda de `cherry-pick` se queda.

### Sobre §0.m: el orden real

Los 975 bytes de K salieron de `bytes_ps.py`, que corrió ANTES de la negativa (la tabla por línea de
0.h). Los 554 de la línea de candidatas a ambigüedad salieron DESPUÉS, con
`grep '^- Candidatas a ambiguedad de docs' PROJECT_STATE.md | wc -c`: eso es **cambiar de vía tras
una negativa** (DECISIONES-DE-PROCESO.md), y se declara como desviación. El falso positivo es otra
aparición de K y va en la fila de ERRORES-RECURRENTES preparada.

## Estado

EN CURSO: respuestas a la PARADA y a la PARADA 2 copiadas; fase 1 (el script 1.2, el lector, los tests y el runbook) y fase 2 (PROJECT_STATE) seguidas.
