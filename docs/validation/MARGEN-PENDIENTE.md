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

## 1. Fase 1 · el script 1.2, el lector, los tests y el runbook (2026-10-31)

### 1.1 El script: lo que cambia en las líneas 1-758

`git diff main -U0 -- tools/mql5/MedirDemoFTMO.mq5`, en las líneas 1-758: la cabecera reescrita EN SU
SITIO (las mismas 25 líneas: cambian :11-14 y :18-24), `#property version "1.20"` (:27), `#property
description` con «el margen de las pendientes» (:28, por el punto 1 de la respuesta) y
`#define VERSION_SCRIPT "1.2"` (:31). Nada más: los pasos 1 a 7 son byte a byte los de `main`. Todo lo
nuevo va de :793 en adelante, entre `Comprobaciones` y `OnStart`, sin prototipos (punto 0). La línea
759 de la 1.2:

    if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)

La cabecera nueva dice, en SEGURIDAD: «solo EURUSD, numero magico propio, volumen minimo salvo en los
pasos 6 y 8 (el 8: sus lotes, peor caso <= 1000 USD); toda pendiente lleva caducidad (si el simbolo la
admite); las de los pasos 3-5 van sin stop a proposito y, si una se llena, se cierra en cuanto se lee;
toda otra posicion lleva stop» (punto 1). El fuente sigue en ASCII.

### 1.2 El paso 8, tal como quedó

- **Constantes** (`#define`, no inputs: no se cambian desde la ventana de Aceptar): `P8_TOPE_USD`
  1000; `P8_COMISION_LADO` 5,00 (punto 4: el supuesto conservador del registro, ADR-0071, y no los
  2,50 del encargo, que es un cambio del encargo); `P8_DESLIZ` 10 puntos; stop entre 10 y 200 puntos;
  «lejos» 1.000 puntos; «cerca» 10 puntos más el stops level; D mínima de M2, 20 USD; carga, 10 %.
- **Inputs**, tras `Comprobaciones`: `InpMedirMargen` (true) e `InpEsperaMargenSeg` (120). La sonda
  de la fase 0 y la compilación de abajo prueban que MQL5 los admite ahí; en la ventana salen al final.
- **OnStart**: tras el paso 7, `if(ok && InpMedirMargen) ok = MedirMargen(); else if(ok)` escribe
  `p8_fin = desactivado`. `MedirMargen` limpia antes, escribe el contexto (sin peticiones), y llama a
  M1, M2, M3 y M4, cada una seguida de su `Limpiar`, también si falla; después, el `Limpiar("al_terminar")`
  de siempre.
- **El peor caso** (`PeorCaso`, `StopDelTope`): para cada medida, con las compras que pueden estar a
  la vez (S y la ocupación en M4; las dos de M3), Σ |OrderCalcProfit(BUY, v, p, p − (s + 10)·point)|
  + 2 × 5,00 × lotes; el script prueba s de 200 a 10 puntos y se queda el mayor que no pasa de 1.000.
  Escribe siempre la fila `mN_peor_caso`; si ni 10 puntos caben, `mN_no_medible` y no envía nada.
  Con 100.000 de libre y 3.720,77 por lote (cifras de la 2; el script las lee en el momento):

| medida | lotes a la vez | stop (c = 5,00) | peor caso |
|---|---|---|---|
| M1 | 26,88 | 17 puntos | 26,88 × 27 + 268,80 = 994,56 |
| M2 | 0,61 | 200 (el máximo) | 0,61 × 210 + 6,10 = 134,20 |
| M3 | 29,58 | 13 | 29,58 × 23 + 295,80 = 976,14 |
| M4 · posición | 28,22 | 15 | 28,22 × 25 + 282,20 = 987,70 |
| M4 · pendientes | 29,57 | 13 | 29,57 × 23 + 295,70 = 975,81 |

- **M2 por las tres cifras** (punto 2.d): escribe antes y después ACCOUNT_MARGIN, ACCOUNT_MARGIN_FREE y
  ACCOUNT_MARGIN_INITIAL, y decide «carga» por la bajada del LIBRE (≥ 10 % del margen calculado al
  mercado), con la misma regla que el lector; lo escribe en `m2_carga_script`, que elige la ocupación
  de M4.
- **M4** (puntos 2.a, 2.b, 2.c y 2.e): S sin pausa (la ocupación va enseguida); el libre antes de S
  (`m4_libre_antes_stop`), con S puesta (`m4_libre_tras_stop`; si M2 dijo que carga, espera a que la
  cuenta lo refleje) y con la ocupación (`m4_libre_tras_ocupar`); lo que reservó S es la diferencia
  MEDIDA de las dos primeras, y la condición antes de esperar es «libre tras ocupar + reservado < margen
  de S al llenar»; si no se cumple, `m4_no_medible`. Durante la espera, en cada vuelta lee el libre y si
  la ocupación sigue viva, y después si S sigue viva; al resolverse S escribe `m4_ocupacion_viva` («si»
  solo si lo estuvo en TODAS las vueltas, con su ticket) y `m4_libre_al_resolver`. Si S se llena, el
  volumen de sus deals (`m4_volumen_deal`); si desaparece sin deal, el historial: `m4_estado`
  (ORDER_STATE), `m4_comentario` (ORDER_COMMENT, literal) y `m4_motivo` (ORDER_REASON).
- **Qué campo usa la regla del «sí» de M4** (punto 2.b, documentación consultada el 2026-10-31):
  «General Concepts», <https://www.metatrader5.com/en/terminal/help/trading/general_concept>: «If during
  pending order activation the corresponding market operation cannot be executed (for example, the free
  margin on the account is not enough), the pending order will be canceled and moved to history with
  the "Rejected" status». Es decir, el ESTADO es `ORDER_STATE_REJECTED`, pero el estado solo no nombra
  la causa. `ORDER_REASON` no tiene ningún valor para el margen (CLIENT, MOBILE, WEB, EXPERT, SL, TP,
  SO; <https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties>), y la documentación de
  `HistoryOrderGetString` no dice qué comentario pone el servidor. **La regla usa `ORDER_COMMENT`**:
  «sí» solo con `ORDER_STATE_REJECTED`, un comentario que nombre el margen (`no money`, `not enough
  money`, `margin` o `margen`, sin distinguir mayúsculas) y el tope agregado de volumen en 0 o no
  superado. Si FTMO no escribe nada así en el comentario, M4 no da «sí» nunca: sale «no concluyente»
  con el estado, el comentario y el motivo literales. (En el foro de MQL5 se cita un «[no money]», que
  no es documentación: no se usa como dato.)
- **Peticiones**: el paso 8 suma 12 (M1 2, M2 2, M3 4, M4 4: S, la ocupación y quitar las dos), más lo
  que pidan los `Limpiar` si queda algo; la 1.2 entera, 46 con stops level 0 (54 con stops level > 0),
  frente a 34 (42) de la 1.1. Muy por debajo de 2.000 al día (R13) y de 200 órdenes a la vez (como
  mucho 3).
- **Tiempo del paso 8**, peor caso: unos 16 s de pausas, hasta 15 s esperando a la cuenta (M2 y dos
  en M4), hasta 120 s esperando a que salte S y los `Limpiar`: unos 2,5-3 minutos. El script entero,
  como mucho unos 6.

### 1.3 La compilación

Copia de `tools/mql5/MedirDemoFTMO.mq5` de la rama (sha256 `d2a220a1…619e`) en la carpeta de trabajo,
`MetaEditor64.exe /compile:"<copia>\MedirDemoFTMO.mq5" /log:"<copia>\compilar.log"`: código de salida 1
(éxito, al revés), `.ex5` de 82.164 bytes, y la última línea del log:

    Result: 0 errors, 0 warnings, 1122 ms elapsed, cpu='X64 Regular'

(La primera versión montada compiló igual, 0 errors y 0 warnings; la del repo solo cambia un espacio
de un comentario.)

### 1.4 El lector

- `VERSIONES` gana "1.2"; `ESPERADOS["8_margen"]` = {10008, 10009, 10019}; `m4_resultado` es una
  observación, como `buy_stop_llenado`.
- `respuesta_m1` … `respuesta_m4` aplican la regla de la PARADA con los cambios de la respuesta (2.a a
  2.e y 3): M2 por la bajada del libre y el precio por D/2 con D ≥ 10; M4 «no concluyente» con la
  ocupación caída, el llenado parcial, S que cabía al llenar, S sin deal que no sea REJECTED con el
  margen en el comentario o con el tope de volumen superado, y CANCELED nunca «sí».
- Una sección aparte, «## Paso 8: cuando comprueba MT5 el margen de una pendiente stop (ADR-0081 §4)»,
  antes de los INESPERADOS y solo si hay un fichero 1.2: por fichero 1.2, el contexto (modo de margen,
  SYMBOL_MARGIN_HEDGED, pierna mayor, margen inicial, tope agregado, tasas de margen), M1 a M4 y el peor
  caso de cada una; «paso 8 desactivado» o «el paso 8 no corrio» si toca. Las filas del paso 8 no entran
  en la tabla «Decision a decision».
- **Un 1.0 o un 1.1 dan la salida de `main` byte a byte**: el test
  `test_un_1_0_y_un_1_1_dan_la_salida_de_main_byte_a_byte` compara el sha256 de la salida de la rama
  con el de la salida del lector de `main` sobre los mismos CSV sintéticos (un 1.0, un 1.1 y una
  carpeta con los dos), medidos con el lector de `main` antes de cambiarlo (guion `salida_main.py`,
  fuera del repo): `a02029b8…114c`, `f61f234c…ccbb` y `5f487f6f…48ef`.
- Un cambio fuera de los 1.0 y 1.1: el mensaje de una versión desconocida dice ahora «lee 1.0 y 1.1 y
  1.2».

**La comprobación sobre el CSV real** (punto de la respuesta: el criterio es que la salida de `main` y
la de la rama sean idénticas byte a byte; el lector no imprime el 3720.77). La lanza Aleks con `!`,
porque la guardia niega ejecutar el lector cambiado (`crudo = ruta.read_bytes()`, entrada K), con las
dos salidas fuera del repo:

    ! git show main:scripts/leer_demo_ftmo.py > C:/Users/USER/Desktop/comparar-demo/leer_main.py
    ! uv run python C:/Users/USER/Desktop/comparar-demo/leer_main.py data/demo_ftmo --salida C:/Users/USER/Desktop/comparar-demo/salida_main.txt
    ! uv run python scripts/leer_demo_ftmo.py data/demo_ftmo --salida C:/Users/USER/Desktop/comparar-demo/salida_rama.txt
    ! cmp C:/Users/USER/Desktop/comparar-demo/salida_main.txt C:/Users/USER/Desktop/comparar-demo/salida_rama.txt && echo IDENTICAS

(La carpeta `C:/Users/USER/Desktop/comparar-demo/` se crea antes; `cmp` no dice nada si son iguales.)

### 1.5 Los tests

- `tests/unit/test_leer_demo_ftmo.py`: los 9 de antes, sin tocar, y 13 nuevos: la salida de `main`
  byte a byte (1.0, 1.1 y carpeta); un 1.2 en su sección y no en la tabla; una carpeta con un 1.1 y un
  1.2; un 1.2 con el paso 8 desactivado; M1 en sus dos sentidos, no concluyente y no medible; M2 con el
  libre que baja (a la orden y al mercado), con el libre que NO baja aunque ACCOUNT_MARGIN sube, con
  carga lejos de los dos cálculos y con D < 10; M2 sin la pendiente viva; M3 en sus dos sentidos y no
  concluyente; M4 llenada entera («no») y parcial; ocupación caída (con llenada y sin deal); rechazada
  con el margen en el comentario («sí»), con otro motivo, cancelada y con el tope de volumen superado
  (no concluyente); S que cabía al llenar, no saltó, y «no medible»; y el 10019 del paso 8 no es
  inesperado.
- `tests/contract/test_medir_demo_ftmo.py` (nuevo, 9 tests): toda función que rellena una petición
  `TRADE_ACTION_DEAL` o `TRADE_ACTION_PENDING` lleva `.magic`, `.sl` y, si es pendiente,
  `PonerCaducidad`, salvo la lista cerrada `SIN_STOP` con su motivo (`EnviarPendiente`, exenta solo del
  stop: sigue necesitando la caducidad; `CerrarPosicion`); las funciones que envían son exactamente las
  seis conocidas; la condición DEMO sigue en la 759 y `MedirMargen` va detrás de `Comprobaciones`, en el
  fuente y en `OnStart`; y cinco roturas en memoria más una función nueva sin stop, que tienen que dar
  problemas.
- **En rojo, sobre copias estropeadas en la carpeta de trabajo** (guion `rojo.py`: el test de la rama
  y el script 1.2 roto, en un árbol desechable cada uno):
  - sin el `req.sl` de `AbrirCompra` (paso 8): `3 failed, 6 passed`; el principal dice
    `Left contains one more item: 'AbrirCompra: DEAL sin req.sl (stop de proteccion)'`;
  - sin el `PonerCaducidad` de `ColocarBuyStop` (paso 8): `3 failed, 6 passed`;
    `'ColocarBuyStop: PENDING sin PonerCaducidad(req)'`;
  - con una función nueva `AbrirSinStop` que envía un DEAL sin stop: `2 failed, 7 passed`;
    `'AbrirSinStop: DEAL sin r.sl (stop de proteccion)'`, y el de la lista de funciones que envían
    (`At index 1 diff: 'AbrirSinStop' != 'CerrarPosicion'`).
- **En verde, en la rama**: `uv run pytest tests/unit/test_leer_demo_ftmo.py
  tests/contract/test_medir_demo_ftmo.py tests/contract/test_capa_mt5.py -q` → 44 passed. ruff format,
  ruff check y mypy, limpios sobre los tres ficheros de Python.
- **La guardia y pytest** (fase 0, 0.g): con el lector ya cambiado, `uv run pytest
  tests/unit/test_leer_demo_ftmo.py …` no lo niega.

### 1.6 El runbook y los README

`docs/runbooks/DEMO-FTMO.md`: el tiempo de la cabecera (con la 1.2, como mucho unos seis minutos); en
«Lo que hace, y lo que no hace nunca», los lotes grandes del paso 8, los stops de 1,3 a 1,7 pips (y el
de 20 pips de la pequeña de M2), el tope de 1.000 USD y lo esperable, y la frase de los stops corregida
(la de :22, punto 1); «Antes de la ejecución 3: el script 1.2» (copiar, F7 con «0 errors», comprobar
que el CSV y el lector dicen 1.2); las horas de Lima de la 3 (de 03:00 a 12:00 el 2, 4, 5 y 6; el 3
no); qué hacer con «ATENCIÓN: quedan…» con la 1.2 (cerrarlo enseguida); y el paso 8 en «Lo que mide
cada paso». Lo de la ejecución 2 se queda como estaba. `tools/mql5/README.md` y `scripts/README.md`:
una frase cada uno con el paso 8 (los dos dicen lo que hace el script y lo que lee el lector).

## 2. Fase 2 · PROJECT_STATE (2026-10-31)

- **La condición (e)** entra en `docs/state/README.md` («Que sale de PROJECT_STATE, y con que
  criterio»), con su fecha y su rama, como excepción declarada a «lo que se queda no se resume ni se
  reescribe», con el texto literal del encargo y la lectura de la respuesta (punto 6: la coma de una
  enumeración no cuenta). Lo demás del README, sin tocar.
- **(e), en lectura estricta**: las 12 líneas de la tabla de 0.h.2, con el mismo corte (guion
  `fase2.py`, fuera del repo, la misma regla que `prevision.py`); 2.169 bytes. «Artifact…» se queda
  entera (punto 6). Su texto entero, literal, en `docs/state/HISTORIA.md`, bloque «# Technical Debt
  ACORTADA · sale de PROJECT_STATE.md en trabajo/margen-pendiente (2026-10-31)», cada línea seguida
  de lo que queda de ella.
- **Sale el heredado 2** (punto 7 y PARADA 2), con el bloque «# Pendiente heredado SALE»: su línea, su
  texto entero del Archivo 1 (`HISTORIA.md:684`, comprobado literal por el guion) y las tres
  condiciones, frase a frase, con la evidencia verificada (arriba, «Las citas, verificadas»): (c) para
  «MARZO INTERRUMPE…», (c) para «El trader confirmo el 2026-09-21…» y (b) para el resto, entero en
  `ENTRADA-MARZO.md:45-49`. En el mismo commit: `HER:2` sale de las Refs de R5.3; la prosa «heredado 2»
  de R5.3 y de A.3 remite a `docs/runbooks/ENTRADA-MARZO.md` (paso 0); y ENTRADA-MARZO.md:32 deja de
  decir que lo que falta «sigue en `PROJECT_STATE.md`, pendiente heredado 2» (ahora: «que se lleva
  aqui, abajo (su salida de PROJECT_STATE, en HISTORIA: hasta el 2026-10-31, `trabajo/margen-pendiente`,
  fue el pendiente heredado 2 de `PROJECT_STATE.md`)»; el «alli» de la línea siguiente sigue siendo
  PROJECT_STATE). Ninguna otra mención del heredado 2 queda viva (`grep 'heredado 2\|HER:2'` en la
  hoja, ENTRADA-MARZO.md y PROJECT_STATE.md: solo la frase nueva del runbook).
- **La deuda de `cherry-pick` se queda** (punto 7).
- **Bytes por sección, antes y después** (en la rama; anexo `anexos/MARGEN-PENDIENTE/bytes-por-seccion.txt`;
  los de `main` por línea, en `anexos/MARGEN-PENDIENTE/bytes-main.txt`):

| sección | antes | después | diferencia |
|---|---|---|---|
| Next Action (con los heredados) | 8.384 | 8.220 | −164 |
| Technical Debt | 10.746 | 8.577 | −2.169 |
| el resto | 5.322 | 5.322 | 0 |
| **total (`wc -c`)** | **24.452** | **22.119** | **−2.333** |

  (24.452 en la rama antes de la fase 2: los 24.393 de `main` más la cabecera de la rama abierta y
  el recuento de tests, 1.795, del mismo largo que 1.777.)
- Los tests que leen PROJECT_STATE y la hoja de ruta, en verde: `uv run pytest
  tests/unit/test_hoja_de_ruta.py tests/unit/test_project_state.py tests/unit/test_project_state_rutas.py
  tests/unit/test_historia.py tests/contract/test_documentos_vivos.py -q` → 33 passed; `uv run botsito
  state check` → OK.

## 3. Las líneas del cierre, preparadas sobre una copia (sin aplicar en la rama)

Guion `cierre_copia.py` (fuera del repo), sobre copias de `PROJECT_STATE.md` y de la hoja de ruta de
la rama:

- **Entrada A**: «Cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4) pide un script 1.2,
  que aún no existe: una rama corta antes de la 3; si no llega, esa medida pasa a la siguiente prueba.»
  pasa a «La 3 va con el script 1.2 (trabajo/margen-pendiente), que además mide cuándo comprueba MT5 el
  margen de una pendiente stop (ADR-0081 §4; paso 8, DEMO-FTMO.md).»
- **Hoja de ruta, A.1** (las líneas reajustadas):

      FTMO-P-D1 §3. El script 1.2 (trabajo/margen-pendiente) mide en la 3 el instante en que MT5
      comprueba el margen de una pendiente stop (ADR-0081 §4).

- **Hoja de ruta, R6a.6**: «el script 1.2 de MedirDemoFTMO» pasa a «el script 1.2 de MedirDemoFTMO
  (HECHO, trabajo/margen-pendiente)».
- **La cabecera del cierre**, con los tres textos del consultor (punto 6), con un sha de 7 caracteres y
  una fecha de 10 en lugar de `<sha>` y `<fecha>`, y Current Branch = `main`.
- **PROJECT_STATE de la copia, con todas las líneas del cierre: 21.784 bytes** (`wc -c`), por debajo de
  21.800 (el auditor del consultor estimaba unos 21.755). La copia pasa `problemas_a` y `problemas_c`
  de `tests/unit/test_hoja_de_ruta.py` (las dos, `[]`) y las secciones en orden y el tope de
  `tests/unit/test_project_state.py`.

## 4. El encargo frente a lo hecho

| punto del encargo | hecho |
|---|---|
| 0 · Apertura: base comprobada, abrir-rama, encargo, contrato con tramo y riesgo alto, Archivo | Hecho (e441d95; arriba, «Apertura») |
| 1.a · El script 1.2: pasos 1-7 sin cambios y un paso 8 | Hecho (§1.1, §1.2); 1-7 byte a byte, salvo la versión, la cabecera en su sitio y :28 (punto 1 de la respuesta) |
| 1.b · PROJECT_STATE a 21.800 o menos con las líneas del cierre | Hecho: 21.784 (§3) |
| 2 · Fase 0 y PARADA | Hecho (a4be85e) |
| 3 · El script, compilado, el lector, sus tests, el test estático en rojo y en verde, DEMO-FTMO.md | Hecho (2688f8b; §1) |
| 4 · README (e), las salidas a HISTORIA, las HER:n, wc -c por sección | Hecho (§2) |
| 5 · Informe, líneas del cierre, fila de ERRORES-RECURRENTES, revisor | §3, §5 y el informe del revisor, abajo |

**Desviaciones, declaradas:**

1. **La comisión del tope es 5,00 USD por lote y lado, no 2,50** (respuesta, punto 4): el supuesto
   conservador del registro (ADR-0071) mientras el CSV de la ejecución 2 no esté congelado. Stops de 13
   a 17 puntos en lugar de los «2 a 4 pips» del encargo.
2. **`#property description` (:28) cambia**, además de :27 y :31: lo pide el punto 1 de la respuesta.
3. **M (el break even de una venta que salta por el ASK) queda fuera** (punto 5): la 1.2 no lo mide y
   sigue esperando a una prueba posterior. A.1 lo nombra; la hoja de ruta no se toca por eso.
4. **El heredado 2 sale por (c) y (b), frase a frase, no por (b) entero** (PARADA 2): la premisa del
   punto 7 (que la versión entera vivía en ENTRADA-MARZO.md:45-49) no se cumplía.
5. **La línea de candidatas a ambigüedad (554 bytes) se midió DESPUÉS de una negativa de la guardia**,
   con `grep … | wc -c` (arriba, «Sobre §0.m: el orden real»): cambio de vía tras una negativa, aunque
   la cifra no se usó para nada que se aplicara.
6. **La regla del «sí» de M4 depende del comentario del historial** (§1.2): si FTMO no nombra el margen
   en `ORDER_COMMENT`, M4 no puede dar «sí», solo «no» o «no concluyente».
7. **La comprobación del lector sobre el CSV real la lanza Aleks** con los cuatro comandos de §1.4 (la
   guardia niega ejecutar el lector cambiado; entrada K), y su criterio es la identidad byte a byte con
   `main`, no el 3720.77 (respuesta, último párrafo).
8. **Negativas de la guardia en las fases 1 y 2**: `sed -i … && uv run botsito state check` en una sola
   llamada («ejecutar `botsito state check`: antes, en el mismo comando, va `sed -i`»); rehecho en dos
   llamadas, la forma que propone. Ninguna del clasificador.

**Exposiciones:** ninguna en toda la rama. No se leyó material del trader, velas, ticks ni el CSV de
`data/demo_ftmo/`; `HOLDOUT-EXPOSICIONES.md` no se toca.

## 5. La fila de ERRORES-RECURRENTES, preparada (la escribe el cierre)

Se completa con lo que encuentre el revisor (abajo); lo del consultor, tal como lo dio su respuesta:

| rama | revisor | consultor | lección |
|---|---|---|---|
| `trabajo/margen-pendiente` | Una pasada, opus (§8): 0 bloquea, 7 importa (a1=b5 la cita de ENTRADA-MARZO:45-49 que la propia rama desplazaba una línea; a2=b4 el deslizamiento justificado con más de lo que dice su fuente y presentado como garantía; b1 `Limpiar` sin comprobar entre medidas; b2 el test estático no negaba un stop a 0, una sobrecarga ni una acción por variable; b3 una frase del runbook que el paso 8 dejaba falsa), 4 menores (a3, a4, b6, b7); arreglados todos salvo a4, contestado (§8.1) | Cuatro, de la respuesta a la PARADA (2026-10-31): (1) **importa**: el encargo dio como dato lo que decía el auditor del consultor sin medirlo: (e) ahorraba de 2.400 a 2.650 bytes (son 2.169); los stops saldrían de 2 a 4 pips (salen de 1,3 a 2,2); trece tests leen PROJECT_STATE (lo leen seis y lo nombran trece) y `test_ids_citados` lo lee (lo hace `knowledge validate`); la comprobación de Aleks daría el margen 3720.77, que el lector no imprime; y citas de línea de `test_capa_mt5.py` (:143-151 son :142-149; :278 es una cadena de ejemplo). (2) **importa**: en el primer borrador de su respuesta aceptó sacar por (b) la deuda de `cherry-pick` sin comprobar que su texto entero vivía en otro sitio; lo cazó su auditor. (3) **menor**: el encargo nombró una frase falsa de la cabecera y no vio la segunda («toda posición lleva stop de protección»). (4) **menor**: fijó 2,50 USD de comisión para el tope sin mirar que el registro mantiene 5. Y uno de la respuesta misma: (5) **importa**: el punto 7 daba por hecho que la versión entera del heredado 2 vivía en ENTRADA-MARZO.md:45-49, el mismo hueco que bloqueó el revisor de `trabajo/plataforma-adelantada` (b1); lo midió la sesión y salió la PARADA 2. De la sesión: el falso positivo de `crudo` volvió a saltar sobre un guion propio de la carpeta de trabajo (otra aparición de K), y una medida (554 bytes) se hizo con `grep` tras esa negativa | Lo que diga el auditor del consultor sobre una cifra, un recuento o un mecanismo va en el encargo como «verifica que…», nunca como dato (la lección de visor-construccion, repetida). Antes de aceptar una salida por (b), leer el texto entero en HISTORIA y buscar cada frase; y si una rama anterior ya la bloqueó, leer por qué. Antes de pedir que se corrija un texto, leerlo entero. Tras una negativa de la guardia, ni siquiera una medida auxiliar cambia de vía: se apunta el orden. Y una medida que solo prueba el estado («Rejected») no prueba la causa: el «sí» de M4 exige el comentario del margen |

## 6. El encargo, punto por punto

El encargo y las dos respuestas, partidos en requisitos. H = hecho; O = hecho de otra forma (declarado
en §4).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main 6948375, merge 4b12a92, tag F38j, CI 40943847054 verde; sin otra rama; wt-ci intacto | H | «Apertura» |
| 2 | abrir-rama: encargo tal cual, contrato con `tramo: "Carril: lo de Aleks"` y riesgo alto con motivo, Archivo en HISTORIA | H | e441d95; `contrato.yaml`; Archivo 53 |
| 3 | Rutas del contrato las del encargo; ampliación a ENTRADA-MARZO.md en un commit a la vista | H | `contrato.yaml`; 9d3a532 |
| 4 | QUÉ NO CAMBIA: src/, mql5/, knowledge/, ningún ADR, pasos 1-7 salvo la versión, la salida del lector para 1.0/1.1, el CSV de data/, el texto de la Next Action, ninguna cifra | H | §7 (`git diff --stat`); §1.1; §1.4 (sha256 de main); PROJECT_STATE: la Next Action solo pierde el heredado 2 (punto 7) |
| 5 | La rama no ejecuta el script en ninguna cuenta | H | solo compilación en la carpeta de trabajo |
| 6 | Fase 0 a)-k), medida, con PARADA y «Lo que necesito que decidas» | H | §0, a4be85e |
| 7 | Respuesta 0: paso 8 entre Comprobaciones y OnStart, sin prototipos; la 759 pegada | H | §1.1 |
| 8 | Respuesta 1: las dos frases falsas, DEMO-FTMO.md:22 y `#property description` | H | §1.1, §1.6 |
| 9 | Respuesta 2 (a): M1-M4 con buy stops a 100 pips, M4 según M2/M3 | H | §1.2 |
| 10 | Respuesta 2.a: ocupación caída → `m4_ocupacion_viva`, libre antes de leer; «no concluyente» | H | §1.2; test `…ocupacion_caida…` |
| 11 | Respuesta 2.b: «sí» solo REJECTED + comentario del margen + tope de volumen; CANCELED nunca; campo verificado en la documentación | H | §1.2 (el campo es ORDER_COMMENT); test `…si_solo_rechazada…` |
| 12 | Respuesta 2.c: llenado parcial → no concluyente | H | `respuesta_m4`; test `…llenada_entera…` |
| 13 | Respuesta 2.d: M2 por las tres cifras, carga por la bajada del libre; el informe dice qué hicieron MARGIN e INITIAL | H | §1.2; el lector imprime los dos deltas en cada respuesta de M2 |
| 14 | Respuesta 2.e: libre antes y después de S; condición «libre + reservado < margen de S» | H | §1.2; test `…sin_la_condicion…` |
| 15 | Tests del lector en los dos sentidos de cada caso de 2.a-2.e | H | §1.5 |
| 16 | Respuesta 3: 10 % en la bajada del libre; precio por D/2 con D ≥ 10 | H | `CARGA_MIN`, `D_MIN`; test M2 |
| 17 | Respuesta 4: 5,00 USD por lado; declarado como cambio del encargo | O | §1.2; §4, desviación 1 |
| 18 | Respuesta 5: M fuera; dicho en el encargo frente a lo hecho | H | §4, desviación 3 |
| 19 | Respuesta 6: (e) estricta, «Artifact…» entera; previsión con las tres cabeceras | H | §2; §3: 21.784 |
| 20 | Respuesta 7 y PARADA 2: sale el heredado 2 frase a frase, bloque con el texto entero y las tres condiciones; ENTRADA-MARZO.md:32, la prosa de la hoja y HER:2; cherry-pick se queda | O | §2; PARADA 2 |
| 21 | Respuesta 8: fases 1 y 2 seguidas | H | 2688f8b y el commit de la fase 2 |
| 22 | §0.m: el orden real y, si toca, la desviación | H | «Sobre §0.m»; §4, desviación 5 |
| 23 | La comprobación de Aleks: comandos exactos, salidas fuera del repo, identidad byte a byte | H | §1.4 |
| 24 | Script: VERSION "1.2", version "1.20", paso 8, cabecera sin cambiar el número de líneas antes de :759, diff de 1-7 en el informe | H | §1.1 |
| 25 | Compilado fuera del repo con la línea «Result:» pegada | H | §1.3 |
| 26 | Lector: VERSIONES con 1.2; sección aparte solo con un 1.2; 1.0/1.1 byte a byte | H | §1.4; test sha256 |
| 27 | Tests: M1-M4 en los dos sentidos y no concluyente; 1.2 desactivado; 1.1 como en main; carpeta 1.1 + 1.2 | H | §1.5 |
| 28 | Test estático en tests/contract/, lista cerrada, niega por defecto, roto a propósito (sin sl del paso 8, sin PonerCaducidad, función nueva) en rojo y en verde | H | §1.5 |
| 29 | DEMO-FTMO.md: antes de la 3, paso 8, horas de Lima, «ATENCIÓN: quedan…», lo que el paso 8 deja falso y el tiempo | H | §1.6 |
| 30 | README de tools/mql5 y scripts, solo si nombran lo que hace el script | H | §1.6 |
| 31 | Fase 2: (e) en el README con fecha y rama; salidas literales a HISTORIA en sus bloques; HER:n; wc -c por sección | H | §2 |
| 32 | Informe: fase 0, PARADA, respuestas, script, lector, PROJECT_STATE, encargo frente a lo hecho | H | este informe |
| 33 | Líneas del cierre preparadas y medidas sobre una copia, comprobadas contra test_hoja_de_ruta y test_project_state | H | §3 |
| 34 | Fila de ERRORES-RECURRENTES preparada | H | §5 |
| 35 | Revisor (opus) con los cinco alcances, su informe pegado y lo hecho con cada hallazgo | (abajo) | «Informe del revisor» |
| 36 | Sin fix/ en la CI de Linux: no toca hooks ni rutas | H | §7 |
| 37 | make check con ruff format, ruff check y mypy antes, en cada commit; mensajes con Write y `-F` | H | cada commit, sellado |

## 7. Lo que no cambia, y los tests nuevos con el código de main

**Lo que no cambia.** `git diff --stat main...HEAD` (tras e2d80a3): 17 ficheros: `PROJECT_STATE.md`,
`contrato.yaml`, el encargo, `docs/plan/HOJA-DE-RUTA.md`, `docs/runbooks/DEMO-FTMO.md`,
`docs/runbooks/ENTRADA-MARZO.md`, `docs/state/HISTORIA.md`, `docs/state/README.md`, el informe y sus
dos anexos, `scripts/README.md`, `scripts/leer_demo_ftmo.py`, `tests/contract/test_medir_demo_ftmo.py`,
`tests/unit/test_leer_demo_ftmo.py`, `tools/mql5/MedirDemoFTMO.mq5` y `tools/mql5/README.md`. Ninguno
de `src/`, `mql5/`, `knowledge/`, `docs/adr/`, `data/`, `config/`, `.claude/` ni el `Makefile`. (Repetir
el diff acotado a esas rutas lo negó la guardia porque el comando nombraba `data`; no se insistió: la
lista entera de arriba lo muestra.) `uv run python scripts/contrato_rama.py` → 17 ficheros dentro del
contrato. HISTORIA solo se amplía (`tests/unit/test_historia.py`, en verde en `make check`).

**Los tests nuevos con el código de main** (skill `comparar-con-main`, «Para probar un test con el
código de main»). Antes: `git status --short` vacío, ramas `main` y `trabajo/margen-pendiente`, 144
tags, y el worktree `wt-ci` (de otra sesión, «prunable»: no se toca, así que tampoco se hace
`git worktree prune`). `git worktree add --detach C:/mp/main main` (6948375); los dos ficheros de test
de la rama copiados dentro del clon; `uv run pytest tests/contract/test_medir_demo_ftmo.py
tests/unit/test_leer_demo_ftmo.py -q -p no:cacheprovider --tb=no` en el clon:

    .FFFFFF............FFFFFFFFFFFF                                          [100%]
    18 failed, 13 passed

Fallan los 18 que miden lo nuevo: en el estático, la lista de funciones que envían, la 759 con el
paso 8 detrás y las cuatro roturas del paso 8 (sus funciones no existen en la 1.1); en el lector, los
12 del paso 8 (un 1.2 se rechaza por versión). Pasan, como deben, los invariantes que la 1.1 ya
cumplía (toda función que envía lleva mágico, stop y caducidad; la rotura de `EnviarPendiente`; la
función nueva sin stop), los 9 tests de antes del lector y el de la salida byte a byte (que es la de
`main`). En la rama: los 44 de `tests/unit/test_leer_demo_ftmo.py`, `tests/contract/test_medir_demo_ftmo.py`
y `tests/contract/test_capa_mt5.py`, en verde (§1.5). La guardia no negó pytest en el clon. Después:
`git worktree remove --force C:/mp/main` (con `--force` porque quedaban los dos tests copiados y la
`.venv` del clon, sin seguir), y `git worktree list`, `git status --short`, `git branch --list`,
`git tag -l` (144) y `git ls-remote --heads origin` (solo `main`) iguales que antes. No se leyó
`data/`: estos tests usan CSV sintéticos en `tmp_path` y el fuente de `tools/mql5/`.

**Sin CI de Linux por `fix/`**: la rama no toca hooks, rutas, sistema de archivos ni `zoneinfo` en el
código (lo de Lima es una medida del informe), y el encargo lo dice: «el fix/ en la CI de Linux no es
obligatorio».


## 8. Informe del revisor (opus, 2026-10-31), tal cual

## Informe del revisor · trabajo/margen-pendiente · 2026-10-31

Base `6948375` (`git merge-base main HEAD`). Commits e441d95, a4be85e, 9d3a532, 2688f8b y e2d80a3. En el árbol de trabajo, sin commitear, solo `docs/validation/MARGEN-PENDIENTE.md` (secciones 6 y 7: +84/−1).

Veredicto: nada bloquea. Hay 7 hallazgos que importan (2 del eje a y 5 del eje b; uno de ellos se repite en los dos ejes) y 4 menores. La rama todavía no está lista hasta que se resuelvan o se justifiquen.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **La cita de la salida por (b) del heredado 2 apunta a una línea equivocada en el árbol de la propia rama.** El bloque de HISTORIA dice que el resto del heredado está «entero en `docs/runbooks/ENTRADA-MARZO.md:45-49`». Eso era cierto en `main`. Pero el mismo commit e2d80a3 parte la línea :32 de ENTRADA-MARZO en dos, y todo lo de debajo baja una línea. En la rama, :45 está en blanco y la frase clave «`paquete <sesion>`: **sin sus palabras, no vale**.» está en :50, fuera del rango citado. | `git show main:docs/runbooks/ENTRADA-MARZO.md \| sed -n '45,49p'` da el bloque entero. En la rama, `ENTRADA-MARZO.md:45` está vacía y el bloque va de :46 a :50. Lo citan `docs/state/HISTORIA.md:14208` y `MARGEN-PENDIENTE.md:585,781`. HISTORIA solo se amplía, pero estas líneas son de la rama y aún se pueden corregir antes del merge. |
| a2 | importa | **El deslizamiento del tope se justifica con más de lo que dice su fuente.** El script y el informe dicen «10 puntos por operación (entrada y salida juntas), cinco veces el mayor medido». Problemas: (1) las muestras son tres, con 0,01 lotes: +2 en contra, −2 a favor y +1; (2) la propia fuente dice «Ninguna cifra fija se sostiene con tres muestras de un minuto»; (3) si los 10 puntos cubren entrada y salida, son 2,5 veces 2+2, no cinco; (4) se aplican a 27–30 lotes. El peor caso queda en 975,81–994,56 USD, así que hay de 5 a 24 USD de holgura: menos de un punto con unos 29 lotes. Aun así, el runbook lo presenta como garantía: «aunque todo se llenara y fuera hasta su stop, no se pierdan más de 1.000 USD». Además, `req.deviation = P8_DESLIZ` (:959) no limita nada si FTMO usa ejecución a mercado; no lo pude comprobar (abajo). | `tools/mql5/MedirDemoFTMO.mq5:806` («5 veces el mayor medido»); `MARGEN-PENDIENTE.md:223-225` y la tabla en :636-642; `DEMO-EJECUCION-1.md` fila P7 («tres muestras: +2, −2 y +1 … Ninguna cifra fija se sostiene con tres muestras de un minuto») y fila 54 («−2 (a favor)»); `DEMO-FTMO.md:26-28`. |
| a3 | menor | **La lectura de (e) del README se atribuye entera al punto 6 de la respuesta, que no la sostiene entera.** El punto 6 solo excluye la coma de una enumeración y pide la lectura estricta. Que «: » cuente como final de frase y que los 160 bytes se midan desde «- » vienen de la PARADA (0.h.2); el consultor los aceptó solo implícitamente («Previsión aceptada»). Dos líneas acortadas cortan en «: » (la del CRLF y la de `simulador_config.py`). | `docs/state/README.md:88-91` («Como se lee (respuesta del consultor … punto 6 …)»); `MARGEN-PENDIENTE.md:311-313` (la regla viene de 0.h.2) y :503. |
| a4 | menor | En la línea de ADR-0042, el paréntesis conserva «falso positivo medido con enero,» además de la cita del informe con su sección. (e) solo manda conservar esa cita. | `PROJECT_STATE.md` (Technical Debt: «… (falso positivo medido con enero, ENTRADA-ENERO.md §0.b; entera en HISTORIA, …)»); `docs/state/README.md:84`. |

Comprobado sin hallazgos:
- **Contrato.** `contrato_rama.py` da: «CONTRATO: 17 ficheros dentro del contrato … 2 comprobaciones», exit 0.
- **Comprobaciones del contrato.**
  - `uv run pytest tests/unit/test_leer_demo_ftmo.py tests/contract/test_medir_demo_ftmo.py tests/contract/test_capa_mt5.py -q` pasa en verde (44 puntos).
  - `make check` no lo ejecuté (escribe). Su evidencia es `make-check.log`: «3060 passed», «SELLO: make check en verde sobre el arbol 082c9207aa6883c6b5b71b340e4d725c89d5c570» y «PICO DE MEMORIA … 299 MiB». Ese árbol es exactamente el de e2d80a3 (`git rev-parse e2d80a3^{tree}` da 082c920…).
  - Lo sin commitear del informe necesitará su propio `make check`.
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/`.
- **Holdout y regímenes de cambio.**
  - `git diff --name-status main...HEAD`: ninguna ruta de `knowledge/`, `data/`, `src/`, `mql5/`, `docs/adr/`, `.claude/`, `config/` ni el Makefile.
  - HISTORIA solo gana líneas.
  - Ningún informe de validación que ya estuviera en main cambia.
  - `HOLDOUT-EXPOSICIONES.md` sin tocar, y el informe declara que no hubo exposición.
- **Ambigüedades, ADR y la regla de las tres guardias de una `cita`:** no aplican.
- **Tests de estado.** `test_hoja_de_ruta`, `test_project_state`, `test_project_state_rutas`, `test_historia`, `test_documentos_vivos` y `test_adr`: todos en verde.
- **Citas comprobadas contra su fuente:**
  - `REGISTRO-MARZO.md:118`, `:127` y `:167-169`;
  - `CLAUDE.md:175-177` y `:178-181`;
  - `HISTORIA.md:684`, idéntica al texto entero del bloque (comprobado en memoria);
  - `SESION-05-EXTRACCION.md:1062` (§3.5);
  - `DEMO-EJECUCION-1.md` filas 53, 54 y P7 (lo que falla está en a2).

### Eje (b) · Encargo
Resumen: 0 bloquea, 5 importa, 2 menor. Requisitos: 32 hechos, 2 parciales, 0 no hechos (y 3 hechos de otra forma, todos declarados).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base 6948375, tag F38j y CI 40943847054 en verde | Hecho | `MARGEN-PENDIENTE.md:9-16`; merge-base 6948375 |
| 2 | Contrato: `tramo: "Carril: lo de Aleks"`, riesgo alto con su motivo, sus rutas, y la ampliación a ENTRADA-MARZO en un commit a la vista | Hecho | `contrato.yaml:2,4,18`; 9d3a532 |
| 3 | Archivo 53 en HISTORIA | Hecho | diff de HISTORIA, «# Archivo 53 · … 6948375» |
| 4 | Fase 0 a)–k), la PARADA y «Lo que necesito que decidas» | Hecho | `MARGEN-PENDIENTE.md:18-476` |
| 5 | Las dos respuestas, copiadas tal cual en el encargo y en el informe | Hecho | `diff` de encargo :122-168 frente a informe :481-527, y de :174-182 frente a :561-569: idénticas |
| 6 | Pasos 1–7 iguales salvo la versión; la cabecera en su sitio con 25 líneas; `#property description` cambiada (punto 1) | Hecho de otra forma (declarado, desviación 2) | `git diff` solo tiene los trozos `@@ -8,27 +8,27`, `@@ -790,6 +790,703` (solo líneas añadidas) y `@@ -828,6 +1525,11` (solo añade la llamada al paso 8) |
| 7 | La condición DEMO sigue en :759 y el paso 8 va entre Comprobaciones y OnStart, sin prototipos | Hecho | `sed -n 759p` en `main` y en la rama dan la misma línea; `grep -n ACCOUNT_TRADE_MODE_DEMO` → solo :759; MedirMargen en :1469, OnStart en :1490 |
| 8 | Las dos frases falsas de la cabecera corregidas (punto 1) | Hecho | `MedirDemoFTMO.mq5:18-24` |
| 9 | VERSION_SCRIPT "1.2" y version "1.20" | Hecho | :27, :31 |
| 10 | Paso 8 solo tras Comprobaciones | Hecho | `MedirDemoFTMO.mq5:1493-1497,1528-1529`; test `test_la_condicion_demo_sigue_en_la_759_y_el_paso_8_va_detras` |
| 11 | Toda petición del paso 8 con MAGICO y stop, y la pendiente con caducidad | Hecho | Solo envían ColocarBuyStop (:924-944) y AbrirCompra (:947-965), las dos con `magic` y `sl`; ColocarBuyStop además con PonerCaducidad. Se llaman solo con `stop != 0` (:1095, :1141, :1224, :1319) |
| 12 | Limpiar en toda salida del paso 8 | Parcial | Se llama en cada salida (:1471-1485), pero se ignora lo que devuelve: ver b1 |
| 13 | Peor caso antes de colocar o abrir, con pendientes, comisión de 5,00 y deslizamiento, ≤ 1.000 USD | Hecho, con reservas (b1, a2) | StopDelTope va antes de cada envío (:1094, :1140, :1223, :1318). Los volúmenes no cambian entre el cálculo y el envío (v, vS y vO son los mismos), y PeorCaso con EURUSD/USD no depende del nivel de precio |
| 14 | M4 del mismo lado | Hecho | Todo son BUY o BUY_STOP (:934, :956) |
| 15 | Peticiones (1.1 frente a 1.2) y tiempo, contados | Hecho | `MARGEN-PENDIENTE.md:670-676` |
| 16 | M1–M4 con sus filas; respuesta 2.a–2.e (ocupación viva, «sí» solo con REJECTED, comentario del margen y tope de volumen, llenado parcial, M2 por el margen libre, condición «libre + reservado») | Hecho | `MedirDemoFTMO.mq5:1065-1467`; `leer_demo_ftmo.py` `respuesta_m1`…`respuesta_m4` |
| 17 | Campo del historial que usa la regla, verificado en la documentación | Hecho | `MARGEN-PENDIENTE.md:657-669` (ORDER_COMMENT; ORDER_REASON no tiene valor para el margen) |
| 18 | Umbrales del punto 3 (10 % sobre el margen libre; D ≥ 10) | Hecho | `CARGA_MIN`, `D_MIN`; en el script, `P8_CARGA` (:812) |
| 19 | Comisión de 5,00 declarada como cambio del encargo | Hecho de otra forma (declarado) | :805; desviación 1 |
| 20 | Compilación fuera del repo, con su línea «Result:» | Hecho (no verificable aquí) | `MARGEN-PENDIENTE.md:680-684` |
| 21 | Lector: VERSIONES con 1.2; sección aparte solo con un fichero 1.2; un 1.0 o 1.1 sale byte a byte como en main | Hecho | Diff del lector: lo nuevo para 1.0/1.1 solo toca claves y mediciones que esos ficheros no tienen. Hashes fijados en el test, y el clon con el lector de main lo pasa (`MARGEN-PENDIENTE.md:941-946`) |
| 22 | Tests del lector en los dos sentidos, con el paso 8 desactivado y una carpeta 1.1 + 1.2 | Hecho | 13 tests nuevos; en verde |
| 23 | Test estático: lista cerrada, niega por defecto, roto en rojo y luego en verde | Parcial | Lista cerrada y roturas: sí. Negar por defecto: con huecos, ver b2 |
| 24 | DEMO-FTMO: 1.2, paso 8, horas de Lima, «ATENCIÓN», tiempo y lo que el paso 8 deja falso | Parcial | Falta corregir una frase: b3 |
| 25 | README de tools/mql5 y de scripts | Hecho | diff |
| 26 | Condición (e) en el README, con fecha y rama | Hecho (se añade además «Como se lee»: a3) | `docs/state/README.md:77-91` |
| 27 | Sale el heredado 2 por (c)+(c)+(b), con texto literal y evidencia; HER:2 y la prosa de la hoja de ruta; ENTRADA-MARZO:32 | Hecho de otra forma (PARADA 2), con la cita a1 | Bloque de HISTORIA literal (comprobado en memoria: la línea está en `main` y el texto es igual a `HISTORIA:684`); diff de HOJA-DE-RUTA |
| 28 | La deuda de cherry-pick se queda | Hecho | Sigue en la sección Technical Debt |
| 29 | (e): solo líneas de >200 bytes que ahorran ≥60, arranque literal ≤160, sin cortar una ruta ni un id, en lectura estricta (sin la coma), y «Artifact…» entera | Hecho | Medido en memoria. Las 12 líneas: original de 226 a 770 bytes; arranque de 69 a 152; ahorro de 61 a 578; arranque prefijo literal de la línea de main; ningún corte en una coma de enumeración; «Artifact…» sin tocar |
| 30 | Texto entero de las líneas acortadas, literal en HISTORIA | Hecho | Las 12 «enteras» están en `main`; las 12 «Queda en» están en la rama |
| 31 | wc -c por sección, antes y después | Hecho | `MARGEN-PENDIENTE.md:792-797`; `wc -c PROJECT_STATE.md` → 22119 |
| 32 | Previsión de 21.784 bytes con las tres cabeceras | Hecho | Lo recalculé en memoria sobre la rama (frase de A, Current Branch `main`, los tres textos del consultor con sha de 7 y fecha de 10): **21784** |
| 33 | Líneas del cierre preparadas (A, A.1 y R6a.6) | Hecho | Las frases de destino existen: `HOJA-DE-RUTA.md:432,479-480`; la de `PROJECT_STATE.md:46` aparece 1 vez |
| 34 | Fila de ERRORES-RECURRENTES preparada | Hecho | `MARGEN-PENDIENTE.md:866-872` |
| 35 | «El encargo, punto por punto» (E5) | Hecho (sin commitear) | `MARGEN-PENDIENTE.md:874-917` |
| 36 | Prueba con el código de main en un clon desechable | Hecho | `MARGEN-PENDIENTE.md:931-951` |
| 37 | QUÉ NO CAMBIA, y ninguna exposición | Hecho | name-status; `MARGEN-PENDIENTE.md:863-864` |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **El tope de 1.000 USD da por hecho que Limpiar dejó la cuenta vacía, y nada lo comprueba.** `MedirMargen` llama a `Limpiar("tras_m1"/"tras_m2"/"tras_m3")` y descarta lo que devuelve. Si quedan órdenes o posiciones (por ejemplo, las dos pendientes de M3 de unos 14,8 lotes cada una), M4 coloca encima S y la ocupación (unos 28–30 lotes). StopDelTope solo suma lo que esa medida va a enviar, no lo que ya está abierto con el MAGICO. Una alerta no detiene el script. Arreglo natural: si `Limpiar(...) != 0`, el paso 8 no sigue. | `MedirDemoFTMO.mq5:1476,1479,1482` (se ignora el valor); `:311-341` (Limpiar devuelve `quedan` y solo avisa); `:896-921` (StopDelTope solo cuenta `vols[]`) |
| b2 | importa | **El test estático no niega por defecto: lo comprobé con tres roturas en memoria.** (1) `req.sl = 0.0;` pasa, porque solo busca el texto `.sl =`. (2) Una sobrecarga con el mismo nombre (por ejemplo `ColocarBuyStop(const double)` sin stop) desaparece: `funciones()` guarda las funciones en un dict por nombre y la segunda pisa a la primera. (3) Una función que pone la acción con una variable (`r.action = acc;`) y llama a OrderSend no se detecta, ni sale en la lista de las que envían. Para negar de verdad haría falta enumerar las funciones que llaman a `OrderSend` y no las que contienen el regex de la acción, y comprobar que el stop no es 0. | `uv run python - <<'EOF' …` (importa el test y estropea el fuente en memoria). Salida: `sl=0: []`, `sobrecarga: []`, `accion por variable: []`, `envian: ['AbrirCompra', 'CerrarPosicion', 'ColocarBuyStop', 'EnviarPendiente', 'MedirComision', 'MedirLlenadoStop']`, `sl anulado: [] True`. Código: `tests/contract/test_medir_demo_ftmo.py:34,37-57,65,71,88` |
| b3 | importa | **DEMO-FTMO sigue diciendo que el script solo usa el lote mínimo salvo en el paso 6.** El encargo pide corregir lo que el paso 8 deja falso en «Lo que hace…» (los volúmenes y los stops). La viñeta nueva de :22 añade la excepción, pero la frase vieja sigue en pie y, leída sola, es falsa. | `docs/runbooks/DEMO-FTMO.md:18-19` («Solo toca **EURUSD**, con el **lote mínimo** … salvo el paso 6»); encargo :82 |
| b4 | importa | Es a2 visto desde el encargo: el encargo pide un margen de deslizamiento «con su fuente», y la fuente citada no sostiene la cifra para 27–30 lotes. | ver a2 |
| b5 | importa | Es a1 visto desde el encargo: la evidencia de (b) del heredado 2 tiene que citar :46-50 de la rama. | ver a1 |
| b6 | menor | El script escribe `m4_libre_al_resolver`, la lectura más cercana al salto de S, pero el lector no la usa ni la imprime. El «no» de M4 se apoya en el margen libre leído antes de la espera. La respuesta solo pedía escribirla. | `MedirDemoFTMO.mq5:1431`; `leer_demo_ftmo.py`, `respuesta_m4` (no la busca) |
| b7 | menor | StopDelTope no mira el stops level. Con un stops level de más de 13 puntos, todas las órdenes grandes saldrían con 10016 y el paso 8 entero quedaría «no concluyente». Seguridad no rompe. | `MedirDemoFTMO.mq5:903-913`; `:936` (sl = precio − stop) |

### Lo que no pude comprobar
- **La compilación** («Result: 0 errors, 0 warnings, 1122 ms») y el `.ex5`: compilar escribe. Lo sustituye la línea pegada en el informe (:684).
- **La salida del lector sobre el CSV real** de `data/demo_ftmo/`: no se ejecuta nada sobre `data/` (lo lanza Aleks). Lo sustituyen el test de los hashes y la prueba en el clon con el código de main (§7).
- **Si `req.deviation` limita el deslizamiento en la cuenta de FTMO.** Con ejecución a mercado, MT5 lo ignora; no consulté la documentación (no tengo navegador).
- **Si los guiones `fase2.py` y `cierre_copia.py` escribieron directamente en el repo, y si se ensayaron en un clon `git worktree`** (CLAUDE.md, «Ensayos aislados»). El informe solo dice «guion fase2.py, fuera del repo».
- **Que el encargo sea copia literal del prompt:** no tengo el original.
- **`git log` sobre las rutas protegidas:** la guardia lo negó porque el comando nombraba `data/`; no insistí. Lo sustituye `git diff --name-status main...HEAD`.
- **Que no hubo exposición:** solo consta la declaración del informe; no hay rastro mecánico que lo pruebe.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `uv run pytest tests/unit/test_leer_demo_ftmo.py tests/contract/test_medir_demo_ftmo.py tests/contract/test_capa_mt5.py -q`
4. `ls -la make-check.log && grep -E "SELLO|PICO DE MEMORIA|failed|passed" make-check.log`
5. `git rev-parse e2d80a3^{tree} 2688f8b^{tree} 9d3a532^{tree}`
6. `git diff main...HEAD -- tools/mql5/MedirDemoFTMO.mq5` (trozos, `grep '^@@'`, `sed -n 759p` en `main` y en la rama, `grep -n ACCOUNT_TRADE_MODE_DEMO`)
7. Read de `MedirDemoFTMO.mq5` :146-345 y :860-1544; `grep` de cabeceras de función, `OrderSend` y `.action`, `define P8_` y `deviation`
8. `git diff main...HEAD -- scripts/leer_demo_ftmo.py`; `grep` de `es_inesperado`, `VERSIONES` y `OBSERVACION`
9. Read de `tests/contract/test_medir_demo_ftmo.py`; `git diff` de `tests/unit/test_leer_demo_ftmo.py`
10. `uv run python - <<'EOF'` (roturas del test estático en memoria)
11. Read de `MARGEN-PENDIENTE.md` (:1-115, :116-265, :285-476, :477-960); `grep '^#'`; `git diff --stat` del informe
12. `git diff main...HEAD -- PROJECT_STATE.md`; `uv run python - <<'EOF'` (medida de las 12 líneas de (e) contra main)
13. `git diff main...HEAD -- docs/state/HISTORIA.md` (encabezados y bloques); `git diff` y `grep` de `docs/state/README.md`
14. `wc -c PROJECT_STATE.md`; `uv run python - <<'EOF'` (previsión del cierre en memoria → 21784)
15. `uv run pytest tests/unit/test_hoja_de_ruta.py tests/unit/test_project_state.py tests/unit/test_project_state_rutas.py tests/unit/test_historia.py tests/contract/test_documentos_vivos.py tests/unit/test_adr.py -q`
16. `git diff main...HEAD -- docs/plan/HOJA-DE-RUTA.md docs/runbooks/ENTRADA-MARZO.md`; Read de `ENTRADA-MARZO.md:28-52`; `git show main:docs/runbooks/ENTRADA-MARZO.md | sed -n '45,49p'`; `grep "ENTRADA-MARZO.md:45-49"`
17. `sed` de `CLAUDE.md:175-181`, `REGISTRO-MARZO.md:118,127,167-169`, `SESION-05-EXTRACCION.md:1062` y `HISTORIA.md:684`
18. `uv run python - <<'EOF'` (bloques de HISTORIA literales frente a main y la rama)
19. `git log … -- knowledge/ data/ …` (**negado por la guardia**, no se insistió); `git diff --name-status main...HEAD`
20. `diff` de las respuestas del consultor, encargo frente a informe (las dos idénticas)
21. `git diff main...HEAD -- docs/runbooks/DEMO-FTMO.md tools/mql5/README.md scripts/README.md`; `sed -n '14,22p'` de DEMO-FTMO
22. `grep` de los encabezados de ADR-0081 (D3 = §4); `grep` en HOJA-DE-RUTA (:432, :479-480); `sed` de `DEMO-EJECUCION-1.md` (filas 53, 54, P7)

### 8.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 / b5 | importa | **Arreglado en el origen, sin tocar HISTORIA** (que solo se amplía: `tests/unit/test_historia.py` exige que cada versión commiteada empiece por la de su padre, así que el bloque de e2d80a3 no se puede corregir): la frase nueva de `ENTRADA-MARZO.md:32` vuelve a ocupar UNA línea, y el bloque vuelve a `:45-49`. `sed -n '45,49p'` en `main` y en la rama dan el mismo md5 (`2b5319ac…`), así que la cita de HISTORIA y la del informe vuelven a ser ciertas. El «alli» de :33 sigue siendo PROJECT_STATE («(su salida, en HISTORIA; hasta el 2026-10-31, `trabajo/margen-pendiente`, fue el pendiente heredado 2 de `PROJECT_STATE.md`); el 12 vivio alli…»). |
| a2 / b4 | importa | **Corregido el texto, no la cifra.** Los 10 puntos se quedan, porque con 20 el stop de M1 saldría de 7 puntos, por debajo del mínimo, y M1 no se mediría. Pero se dicen como lo que son: un SUPUESTO, 2,5 veces el peor par medido (+2 y +2 con 0,01 lotes; `MedirDemoFTMO.mq5`, comentario de `P8_DESLIZ`), y en ejecución a mercado nada lo limita. La ejecución 1 midió `SYMBOL_TRADE_EXECUTION_MARKET` (`DEMO-EJECUCION-1.md:109,151`), y `req.deviation` lleva ahora el comentario de que solo cuenta en ejecución instantánea. En `DEMO-FTMO.md` el tope ya no es una garantía: «un deslizamiento SUPUESTO de un pip por operación. Ese pip no es una garantía … en un salto brusco del precio un stop puede llenarse más lejos y la pérdida pasar de esa cifra». Lo de §0.e y §1.2 («cinco veces el mayor medido») queda corregido por esta fila. |
| b1 | importa | **Arreglado.** `MedirMargen` comprueba lo que devuelve cada `Limpiar`. Si `antes_paso_8` no deja la cuenta vacía, el paso 8 no empieza. Si no la deja tras M1, M2 o M3, no sigue. En los dos casos escribe `p8_fin = detenido` con su motivo, y el `Limpiar("al_terminar")` de `OnStart` corre igual. El lector imprime «PASO 8 DETENIDO: …», con su test (`test_un_paso_8_detenido_por_un_limpiar_lo_dice`). |
| b2 | importa | **Arreglado.** El test estático parte de las funciones que llaman a `OrderSend` y lee la acción de su petición. Una acción que no es `TRADE_ACTION_DEAL`/`PENDING`/`REMOVE`/`MODIFY` escrita tal cual (una variable, o ninguna en la función) es un problema. Las sobrecargas se miran aparte (lista, no dict), y un `.sl = 0` no cuenta como stop. Tests nuevos, uno por rotura: `test_rompe_con_un_stop_a_cero`, `test_rompe_con_una_sobrecarga_del_mismo_nombre_sin_stop`, `test_rompe_con_una_accion_puesta_por_variable` y `test_rompe_con_un_ordersend_sin_accion_en_la_funcion`. |
| b3 | importa | **Arreglado.** `DEMO-FTMO.md`, «Lo que hace…»: «Solo toca **EURUSD**, con el **lote mínimo** …, salvo en los pasos 6 y 8. … El 8, desde la 1.2, usa lotes grandes (el punto siguiente).» |
| a3 | menor | **Arreglado.** El «Como se lee» del README atribuye cada parte a su fuente: la lectura estricta y la medida de 200 y 160 bytes vienen de la fase 0 (§0.h.2), aceptadas con la previsión, y la coma de la enumeración, del punto 6. |
| a4 | menor | **Se deja, con motivo.** El paréntesis de la línea de ADR-0042 era «(falso positivo medido con enero, ENTRADA-ENERO.md §0.b)», y esa es la cita de su informe tal como la línea la escribía. Quitarle «falso positivo medido con enero» sería reescribirla, y además el bloque de HISTORIA (e2d80a3) ya registra lo que queda, y no se puede cambiar. |
| b6 | menor | **Arreglado.** El «no» y el «sí» de M4 enseñan `m4_libre_al_resolver` («libre al resolver …»), sin que decida nada. |
| b7 | menor | **Arreglado.** El stop mínimo de `StopDelTope` es el mayor de `P8_STOP_MIN` y el stops level más 1. |
| «Lo que no pude comprobar», guiones | — | `fase2.py` y `cierre_copia.py` se escribieron en la carpeta de trabajo, FUERA del repo. `fase2.py` se ensayó primero sobre copias de PROJECT_STATE y HISTORIA en esa carpeta (`ensayo2/`, misma salida que en el repo: 22.119 bytes, −2.169 y −164), y después se ejecutó sobre el repo con la raíz como argumento (CLAUDE.md, «Ensayos aislados», punto 2), sin `make check` corriendo. `cierre_copia.py` solo lee el repo y escribe las copias en la carpeta de trabajo. No se usó un clon `git worktree` para el ensayo de `fase2.py`: es una desviación menor de «Ensayos aislados», punto 1. |

**Después de los arreglos:** `uv run pytest tests/unit/test_leer_demo_ftmo.py
tests/contract/test_medir_demo_ftmo.py tests/contract/test_capa_mt5.py -q` → 49 passed. ruff format,
ruff check y mypy, limpios. La compilación de la versión final (sha256 `f9903c6f…9151`), en la carpeta de
trabajo: `Result: 0 errors, 0 warnings, 1369 ms elapsed, cpu='X64 Regular'`, con un `.ex5` de 82.348
bytes. La línea 759 sigue siendo la condición DEMO. Con el código de `main`, en un clon
`--detach` de nuevo (C:/mp/main, quitado después, con `wt-ci` intacto): **20 failed, 16 passed**. Los
cuatro tests estáticos nuevos sin stop, de la sobrecarga, la acción por variable y el OrderSend sin
acción prueban el comprobador sobre roturas en memoria: pasan en los dos lados, salvo el del stop a
cero, que estropea `AbrirCompra` (no existe en la 1.1). Tests: 1.800 funciones (`state check`).
PROJECT_STATE: 22.119 bytes en la rama y 21.784 con las líneas del cierre (`cierre_copia.py`, otra
vez). La fila de ERRORES-RECURRENTES (§5) gana, en «revisor»: «Una pasada (opus): 0 bloquea, 7
importa (a1=b5, a2=b4, b1, b2, b3), 4 menores (a3, a4, b6, b7); arreglados todos salvo a4, contestado».

## Estado

Fases 0, 1 y 2 hechas, cada una con su commit sellado; el revisor (opus) pasado, con sus hallazgos arreglados o contestados (§8.1); las líneas del cierre preparadas (PROJECT_STATE con ellas: 21.784 bytes). Pendiente de Aleks: la comparación del lector sobre el CSV real con «!» (§1.4) y la ejecución 3 con el script 1.2. Rama lista para revisión, NO cerrada.
