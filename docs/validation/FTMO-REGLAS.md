# Las reglas de FTMO 2-Step Swing de 100.000, con su fuente oficial

Rama `trabajo/ftmo-reglas`, 2026-09-25. Sin merge, sin tag y sin push. Solo investigación y
documentación: no se toca `src/`, ni `ambiguedades.yaml`, ni la spec. Lo decide el consultor con este
documento delante.

**Cómo se leyó.** Solo fuentes oficiales de FTMO: páginas de `ftmo.com`, sus FAQ y la API que alimenta
su tabla de símbolos (`ftmo.com/wp-json/ftmo/symbols`). Se descargó el HTML crudo con `curl` y se
extrajo el texto; **las citas son literales de ese texto**, no de un resumen. Consultado el
**2026-09-25 entre las 19:32 y las 19:36 UTC**. Las copias descargadas no se versionan. No se ha usado
ningún foro ni blog. Lo que no aparece en fuente oficial dice **NO ENCONTRADA**.

## 1. Lo que preguntan A-27 y A-28, y lo que el repositorio da por supuesto

**A-27 y A-28 no son reglas: son MEDICIONES** en la plataforma. Las dos están ABIERTAS y no son
bloqueantes.
- **A-27**: «MEDICION, no pregunta al trader. ¿que digits, tamaño de contrato, lote minimo, paso de
  lote y stops level tiene EURUSD en la cuenta de FTMO?». Parámetros: `instrumento_digitos`,
  `instrumento_contrato`, `instrumento_lote_minimo`, `instrumento_lote_paso` e
  `instrumento_stops_level`. Todos en DEFAULT_AMBIGUOUS, con los valores medidos en la demo de
  FundedNext: 5, 100000, 0.01, 0.01 y 0.
- **A-28**: «MEDICION, no pregunta al trader. ¿cuanto va el reloj del servidor de FTMO por delante de
  UTC en horario estandar, y con que calendario cambia de hora [...]?», más una «VERIFICACION
  EXPLICITA»: que el corte del día de riesgo cae a medianoche CE(S)T y NO a la del servidor.
  Parámetros: `broker_offset_base` y `broker_dst`, los dos UNKNOWN.

**Lo que el repositorio da por supuesto de FTMO.** Viene de ADR-0026 y ADR-0027 y de los parámetros
`firma_*`, leídos el 2026-09-14:
- firma FTMO, programa 2-Step, tipo Swing, 100.000;
- pérdida diaria 5 %, fijada con el saldo a medianoche CE(S)T (`firma_base_perdida_diaria =
  saldo_corte_diario`);
- pérdida máxima 10 %, estática (`firma_perdida_total_arrastra = false`);
- las dos del capital inicial y vigilando la equity (`firma_magnitud_vigilada = equity`);
- el tipo Swing sin restricción de noticias (`firma_noticias_restringe = false`);
- apalancamiento 1:30 (`firma_apalancamiento = 30`);
- 2.000 peticiones al servidor al día (`firma_mensajes_dia_max`);
- servidor «GMT+2 +DST»;
- sin tope semanal de la firma (ADR-0027 §6).

**Lo que el repositorio NO tiene:** objetivos de beneficio, días mínimos de trading, límite de
tiempo, reglas de fin de semana, comisiones, swaps, volumen máximo, gap trading ni reglas de gestión
del riesgo.

## 2. Las reglas, con su fuente

| # | regla | lo que dice FTMO (literal) | fuente |
|---|---|---|---|
| R1 | Objetivo de beneficio | «The Profit Target is calculated as a percentage of your Initial Simulated Capital: 10% for the FTMO Challenge 5% for the Verification [...]. There is no Profit Target on the subsequent FTMO Account (2-Step).» · «You will meet this objective once your account balance exceeds the Initial Simulated Capital by the required Profit Target with all positions closed.» · Ejemplo de 100.000: 110.000 y 105.000 | [Trading Objectives](https://ftmo.com/en/trading-objectives/), sección 2-Step |
| R2 | Pérdida máxima diaria | «The Maximum Daily Loss rule establishes a limit (the Maximum Daily Loss Limit) below which your account equity (i.e., Balance + Open Positions P/L ± Swaps – Commissions) cannot drop.» · «is recalculated daily at 00:00 CE(S)T as the difference between: the account balance recorded at 00:00 CE(S)T of the current day and the Maximum Daily Loss Amount, which is 5% of the Initial Simulated Capital.» · «On the first day of trading, the account balance used for this calculation is the Initial Simulated Capital.» · Vale para las dos fases y para la FTMO Account (2-Step) | ídem |
| R3 | Pérdida máxima total | «The Maximum Loss rule establishes a static limit (the Maximum Loss Limit) below which your account equity [...] cannot drop.» · «calculated as the difference between: the Initial Simulated Capital and the Maximum Loss Amount, which is 10% of the Initial Simulated Capital.» · Ejemplo: «Limit = $90,000» | ídem |
| R4 | Días mínimos de trading | «The Minimum Trading Days rule requires the trader to achieve at least 4 Trading Days. A Trading Day is defined as any day – measured from 00:00:00 to 23:59:59 CE(S)T – during which at least one position is opened.» · En las dos fases; «There is no Minimum Trading Days rule on the subsequent FTMO Account (2-Step).» | ídem; y [How long does it take](https://ftmo.com/en/faq/how-long-does-it-take-to-become-an-ftmo-trader/): «(they do not need to be consecutive)» |
| R5 | Límite de tiempo | «There is no maximum time limit to complete the FTMO Challenge: 2-Step, allowing you to progress at your own pace.» | [How long does it take](https://ftmo.com/en/faq/how-long-does-it-take-to-become-an-ftmo-trader/) |
| R6 | Swing: noticias | «Restrictions for trading during selected news releases apply only to the Standard account type. The Swing account type have no restrictions on trading during news releases.» Durante la evaluación, además, no aplican a ningún tipo | [Can I trade news?](https://ftmo.com/en/faq/can-i-trade-news/) |
| R7 | Swing: noche y fin de semana | «The FTMO Swing account type does not have any restrictions on trading during news releases or on holding positions overnight (longer than 2 hours after market close) or over the weekend.» · En la FTMO Account Standard: «you are required to close your positions shortly before the markets close for the weekend or if the rollover (market break) lasts longer than 2 hours. An exception applies only to Swing accounts.» | [Swing account type](https://ftmo.com/en/faq/ftmo-swing-account-type/); [Overnight or before the weekend](https://ftmo.com/en/faq/do-i-have-to-close-my-positions-overnight-or-before-the-weekend/) |
| R8 | Swing: disponibilidad y cambio | «The FTMO Swing account type is available exclusively within the FTMO Challenge: 2-Step.» · «if you purchase an FTMO Challenge as a Standard account type, it is not possible to change it to a Swing account type at a later stage.» · De Swing a Standard sí se puede, al empezar cada ciclo en la FTMO Account | [Swing account type](https://ftmo.com/en/faq/ftmo-swing-account-type/) |
| R9 | Apalancamiento | «The leverage we offer for Standard type account is up to 1:100 and cannot be increased. The Swing account type has leverage set to up to 1:30.» · API, EURUSD: `"leverageSwing": 30` | [Account specifications](https://ftmo.com/en/faq/what-are-the-account-specifications/); [API de símbolos](https://ftmo.com/wp-json/ftmo/symbols) |
| R10 | Reloj del servidor | «Platform server time: MetaTrader 4, MetaTrader 5 = GMT+2 +DST» · **El calendario del +DST: NO ENCONTRADA** | [Account specifications](https://ftmo.com/en/faq/what-are-the-account-specifications/) |
| R11 | Especificación de EURUSD | API: `"contractSize": 100000`, `"digits": 5`, `"maxTradeVolume": 100`, `"marginPercent": 1`. FTMO avisa: «The account specification can be seen directly in the trading platform.» · **Lote mínimo, paso de lote, stops level, freeze level y modos de llenado: NO ENCONTRADA** | [API de símbolos](https://ftmo.com/wp-json/ftmo/symbols); [Account specifications](https://ftmo.com/en/faq/what-are-the-account-specifications/) |
| R12 | Comisión y swaps de EURUSD | API: `"commission": 5`, `"commissionType": "flat_USD"` (la web lo muestra como «USD/LOT*»), `"swapLong": -9.49`, `"swapShort": 0.36`, `"swapType": "points"` · **Si la comisión es por lado o por operación completa, y qué aclara el asterisco: NO ENCONTRADA** · Spread: la web solo remite a «live spreads» | [API de símbolos](https://ftmo.com/wp-json/ftmo/symbols) |
| R13 | Límites del servidor | «perform simulated trades that are operated or managed by automated robots / EAs (Expert Advisors) which cause the trading account to become hyperactive in the sense of an excessive number of more than 2,000 server requests per day [...]» · Y otra FAQ: «platform servers have 200 orders at a time and 2000 max positions per day limitation, just as the limited acceptance of the server messages» | [Forbidden Trading Practices](https://ftmo.com/en/forbidden-trading-practices/); [Instruments and strategies](https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/) |
| R14 | Bots permitidos | «we have no reasons for limiting or restricting your trading strategy, whether it’s discretionary trading, algorithmic trading, EAs, etc.» · Con un EA de terceros, riesgo de «exceed the maximum capital allocation rule» (**esa regla: NO ENCONTRADA**) | [Instruments and strategies](https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/) |
| R15 | Gap trading | Prohibido «perform gap trading [...] by opening simulated trades: when major global news, macroeconomic events, or corporate reports or earnings are scheduled and they might affect the relevant financial market [...]; or two hours or less before a relevant financial market is closed for at least two hours» | [Forbidden Trading Practices](https://ftmo.com/en/forbidden-trading-practices/) |
| R16 | Otras prácticas prohibidas | Explotar errores del servicio o feeds lentos; operaciones manipuladoras, incluidas posiciones opuestas entre cuentas; «use any software, artificial intelligence, ultra-high-speed tools, or mass data entry that might manipulate, abuse, or give you an unfair advantage»; repartir beneficio entre días para esquivar la Best Day Rule; que un tercero opere la cuenta | ídem |
| R17 | Reglas de gestión del riesgo | Evitar «opening substantially larger position sizes compared to your other simulated trades», «opening a substantially smaller or larger number of positions compared to your other simulated trades» y «repeated simulated trading activity that results in higher Risk per Trade Idea» | ídem |
| R18 | Consecuencias | «Any breach or non-compliance with these rules may result in corrective actions, including, but not limited to, removal of simulated trades from your history, restricted access to a trading platform, disqualification from the Evaluation Process, forfeiture of any potential Rewards, or even termination of all agreements [...]» · R2 y R3: «If the equity drops below this limit, the rule is considered violated.» | ídem; [Trading Objectives](https://ftmo.com/en/trading-objectives/) |
| R19 | Consistencia | «Provided you maintain sustainable risk management practices, there are no additional consistency requirements for your trading.» La **Best Day Rule** aparece solo en la sección 1-Step; la sección 2-Step no la trae | [Consistency rules](https://ftmo.com/en/faq/do-you-have-any-consistency-rules/); [Trading Objectives](https://ftmo.com/en/trading-objectives/) |
| R20 | Tope semanal de la firma | No aparece en los objetivos del 2-Step: **NO ENCONTRADA** | [Trading Objectives](https://ftmo.com/en/trading-objectives/) |

## 3. Contraste con lo que daba por supuesto el repositorio

**Coinciden:**
- **R2**, la pérdida diaria: 5 % del capital inicial, fijada con el SALDO a las 00:00 CE(S)T,
  vigilando la EQUITY, y el primer día con el capital inicial. Coincide con ADR-0026 §2-3 y
  ADR-0027 §1. **La página oficial contesta por escrito la «VERIFICACION EXPLICITA» de A-28**: el
  recálculo es a las 00:00 CE(S)T. Lo que A-28 pedía era verlo además en el panel.
- **R3**, la pérdida total: 10 % estática.
- **R6** y **R7**, Swing sin restricción de noticias. **R8**, no se cambia de Standard a Swing.
- **R9**, apalancamiento 1:30.
- **R10**, «GMT+2 +DST».
- **R13**, las 2.000 peticiones al servidor, con la misma cita.
- **R11**, 5 decimales y contrato de 100.000, iguales a los defaults de A-27.
- **R20**, que FTMO no tiene tope semanal.

**Diferencias o matices:**
- **R13, dos límites más de los que el repo no habla:** «200 orders at a time» y «2000 max positions
  per day». `firma_mensajes_dia_max` solo recoge las peticiones al servidor.
- **R15, el gap trading es práctica prohibida para todos los tipos de cuenta**, y choca en apariencia
  con R6: Swing no restringe operar durante noticias, pero prohíbe «opening simulated trades when
  major global news [...] are scheduled» cuando se entiende como gap trading. ADR-0026 §7 dio por
  hecho que con Swing «la restricción de noticias desaparece». Hay que saber dónde está la línea.
- **R17, el tamaño de posición.** El bot dimensiona el lote hasta el stop con riesgo fijo (ADR-0020),
  así que su lote cambia con cada caja. FTMO pide evitar «substantially larger position sizes
  compared to your other simulated trades». El repositorio no lo contempla.
- **R12, costes.** El repositorio no modela ninguno: comisión de 5 USD por lote en EURUSD (sin saber
  si por lado) y swaps. Afecta al break even y a la equity que vigila la firma. Los swaps no le
  afectan mientras el bot cierre a las 15:00.
- **R11, volumen máximo de 100 lotes por operación**: no está en el registro.

**Huecos del repositorio que este documento llena con fuente:** R1 (10 % y 5 %), R4 (4 días de
trading por fase, contados en CE(S)T), R5 (sin límite de tiempo), R7 (noche y fin de semana libres en
Swing), R14 (bots permitidos) y R19 (sin reglas de consistencia adicionales, sin Best Day en el
2-Step).

## 4. Lo que queda abierto

**PARA DATOS** (se mide en la plataforma, cuenta de prueba de FTMO):
- lote mínimo, paso de lote, stops level, freeze level y modos de llenado de EURUSD (A-27): **no
  publicados**;
- `digits` y `contractSize`, que la web da (5 y 100.000) pero FTMO dice que manda la plataforma;
- el calendario del +DST del servidor y el desfase base (A-28), y la rejilla H4 real frente a
  `anclaje_h4`;
- la comisión efectiva de un lote de EURUSD: si 5 USD son por lado o por operación completa;
- el spread real de EURUSD, que FTMO solo publica en vivo.

**PARA EL CONSULTOR** (decisiones de modelado del simulador):
- si el simulador modela los objetivos de beneficio (R1) y los días mínimos (R4) para decir si una
  serie de días «pasa» cada fase, o solo los topes de pérdida;
- si se modelan comisión y swaps en la equity que vigila la firma (R12, R2), y cómo tratar un break
  even que cierra en negativo por comisión (ya contemplado en RN-016);
- si el volumen máximo (R11) y los límites de órdenes y posiciones (R13) entran en el registro como
  parámetros `firma_*`;
- si hace falta una guardia de coherencia del tamaño de posición (R17), dado que el lote es variable
  por diseño.

**PARA FTMO O ALEKS** (preguntar o leerlo en la cuenta):
- **R15 frente a R6**: si operar durante una noticia en Swing puede considerarse gap trading, y qué
  cuenta como «major global news» a esos efectos;
- **R17**: si un lote que varía con el stop, con riesgo constante en dinero, se considera
  «substantially larger position sizes»;
- **R14**: qué es la «maximum capital allocation rule», que no aparece en ninguna página leída;
- **R12**: el asterisco de «USD/LOT*».

## Estado

WAITING_FOR_USER_VALIDATION. No se ha tocado `ambiguedades.yaml` ni la spec.
