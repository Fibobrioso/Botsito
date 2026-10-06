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

> **Recuadro (2026-09-28, rama `trabajo/viabilidad-comision`): la comisión de forex, más fuentes.
> TODAS NO CONFIRMADAS EN DEMO.** El parámetro del perfil (`firma_comision_usd_por_lote`,
> `firma_comision_por_lado`) solo se fija con el CSV de la demo (`docs/runbooks/DEMO-FTMO.md`).
> Consultadas el 2026-09-29 hacia las 04:17 UTC.
>
> - **FTMO, «Trading Update | 27 Mar 2025»**
>   (`https://ftmo.com/en/blog/trading-updates/trading-update-27-mar-2025/`, descargada con `curl`):
>   «Both symbols have a contract size of 100,000, with a commission of 3 USD per lot (round-trip).»
>   Habla de dos símbolos nuevos de forex, USDSGD y USDCNH, **no de EURUSD**.
> - **FTMO, «Trading Update | 25 Sep 2025»**
>   (`https://ftmo.com/en/blog/trading-updates/trading-update-25-sep-2025/`): **fija la comisión de
>   forex en 2,50 USD por lote y por lado (5 USD ida y vuelta) desde la apertura del 29 de
>   septiembre de 2025, para todas las cuentas; antes era 1,50 por lado (3 USD ida y vuelta).** Lo
>   DECLARA el consultor en su orden de cierre del 2026-09-28: la sesión no pudo leer la página (el
>   servidor cortó la conexión en los cuatro intentos), así que no hay cita literal. Casa con la API
>   leída el 2026-09-25 (5 USD por lote en EURUSD) y con los 3 USD de marzo de 2025 como la tarifa
>   anterior. **No confirmado en demo.**
> - **propvator.com, «FTMO Commissions, Spreads and Swaps»** (`https://propvator.com/blog/ftmo-trading-conditions/`,
>   tercero, fechada el 5 de julio de 2026): «FTMO charges roughly $3 per round lot on forex»,
>   «charged on the full round turn».
> - **La API de FTMO leída el 2026-09-25** (R12, arriba): EURUSD `"commission": 5`, `flat_USD`, sin
>   decir si por lado o por operación.
>
> Con eso, `docs/validation/VIABILIDAD-COMISION.md` mide tres escenarios de ida y vuelta por lote:
> 3 USD (la tarifa anterior al 29 de septiembre de 2025), **5 USD (la publicada desde entonces: el
> escenario de referencia)** y 10 USD (5 por lado, el supuesto conservador del perfil). **El parámetro
> del perfil no se toca**: se fija con el CSV de la demo. El cuerpo de este documento no cambia.

> **Respuesta de soporte de FTMO (ticket VDW-DPMWR-965, 29-09-2026; recuadro añadido en la rama
> `trabajo/sesion-03`).** La respuesta la recibió Aleks por correo y la traslada en su brief de ese
> día; no hay cita literal en el repositorio. Lo que dice, punto por punto:
>
> - **FTMO Account Swing: se permite operar durante noticias y mantener posiciones por la noche y el
>   fin de semana.** Coincide con R6 y R7.
> - **No se permite el gap trading** cuando hay programadas noticias globales importantes, eventos
>   macroeconómicos o resultados que puedan afectar al mercado, **ni dentro de las dos horas previas
>   al cierre de un mercado que va a estar cerrado al menos dos horas.** Confirma R15, que ya lo
>   decía en la fuente oficial leída el 2026-09-25 («two hours or less before a relevant financial
>   market is closed for at least two hours»).
> - **Comisiones: en MT4 se descuentan al instante; en MT5, cTrader y TradingView, el 50 % al abrir
>   y el 50 % al cerrar.** Es decir, en MT5 la comisión se cobra por lado, en dos mitades. **El
>   importe no lo dice el correo**: sigue siendo el de la actualización del 25-09-2025, 2,50 USD por
>   lote y por lado (recuadro de arriba), **no confirmado en demo**. El parámetro del perfil no se
>   toca en esta rama.
> - **La pregunta sobre si se puede variar el tamaño de posición quedó sin respuesta** (R17 sigue
>   abierta en §4).
>
> **Lo que eso pide al bot**, comprobado en la spec el 2026-09-29: el bot solo busca entradas de 07:00
> a 15:00 de Madrid, de lunes a viernes, y cierra a las 15:00 lo que tenga abierto (RN-001, RN-002).
> En una semana normal no puede abrir en las dos horas previas al cierre del viernes, a las 22:00 UTC.
> **Pero no tiene calendario de festivos ni de horario de mercado**: si FTMO cierra EURUSD antes de
> las 17:00 de Madrid en un día seguido de un cierre de dos horas o más -Nochebuena, Nochevieja,
> festivos con cierre anticipado-, el bot podría abrir dentro de esas dos horas. Queda como pendiente
> en `PROJECT_STATE.md`; no se corrige en esta rama.

> **Respuesta LITERAL de soporte de FTMO al ticket VDW-DPMWR-965 (recuadro añadido el 2026-10-03 en
> la rama `trabajo/fuentes-ftmo`).** CORRIGE el recuadro de arriba donde dice «no hay cita literal en
> el repositorio»: desde hoy la hay, aquí. Fuente escrita: correo de `support@ftmo.com` recibido el
> **2026-09-29 a las 14:00:47 UTC**, en respuesta al correo de Aleks del 2026-09-28. El texto lo
> copia Aleks en el encargo de la rama (`docs/encargos/trabajo-fuentes-ftmo.md`), sin la firma ni las
> imágenes, y aquí va tal cual, con sus negritas:
>
> > Dear Client,
> >
> > Thank you for reaching out to us.
> >
> > I would like to inform you that FTMO Account Swing allows trading during news releases and
> > holding positions overnight or over the weekend. However, **gap trading is not permitted** when
> > major global news, macroeconomic events, or corporate reports or earnings are scheduled and may
> > affect the relevant market, or within two hours before a relevant market closes for at least
> > two hours.
> >
> > **Commissions are charged differently depending on the platform: on MT4, they are deducted
> > instantly, while on MT5, cTrader, and TradingView, 50% is charged at order opening and the
> > remaining 50% at closing.**
> >
> > For more information, please visit this page: <https://ftmo.com/en/symbols/>
> >
> > If you have any other concerns, feel free to contact us again.
>
> **Contra el traslado de arriba**, punto por punto: coincide en Swing (noticias, noche y fin de
> semana), en el gap trading (las dos mitades de R15: noticias programadas y «within two hours before
> a relevant market closes for at least two hours») y en la comisión de MT5 (50 % al abrir, 50 % al
> cerrar). Tampoco da importe de la comisión: remite a la página de símbolos.
>
> **Lo que NO contesta.** El correo de Aleks preguntaba tres cosas: noticias y gap trading, tamaño de
> posición y comisión. **La del tamaño de posición NO se contestó**: si un lote que varía con el stop,
> con riesgo constante, cuenta como «substantially larger position sizes» (R17, §4 de abajo).
>
> **Repreguntado el 2026-10-03.** Aleks contestó en el mismo ticket con diez preguntas numeradas: la 1
> a la 4, los mensajes al servidor (A-54); la 5 a la 9, el gap trading (A-55); y la 10, el tamaño de
> posición (R17). **Respuesta pendiente.** El correo, literal, en el recuadro siguiente.

> **Correo LITERAL de Aleks a soporte de FTMO, ticket VDW-DPMWR-965 (recuadro añadido el 2026-10-03
> en la rama `trabajo/fuentes-ftmo`).** Fuente escrita: correo de `abriosotapia@gmail.com` a
> `support@ftmo.com`, enviado el **2026-10-03** como respuesta en el ticket, con el asunto «Re:
> Clarification on Swing account rules for an automated EURUSD strategy - [VDW-DPMWR-965]». El texto
> lo copia Aleks en la segunda orden de la rama (`docs/encargos/trabajo-fuentes-ftmo.md`), y aquí va
> tal cual:
>
> > Hello Guilherme,
> >
> > Thank you for your previous answer. I am preparing an FTMO Swing account on MT5 with an Expert
> > Advisor, and I would like to follow the rules exactly, so I have a few follow-up questions.
> >
> > Server messages (2,000 per day)
> > 1. Do rejected orders or rejected modification requests count towards the limit?
> > 2. Does each modification of a pending order (price, stop loss or take profit) count as one
> >    message?
> > 3. Do cancellations of pending orders and closing of positions count?
> > 4. At what time, and in which time zone, is the daily count reset?
> >
> > Gap trading ("within two hours before a relevant market closes for at least two hours")
> > 5. Does this also apply to placing pending orders (limit or stop) within those two hours, even if
> >    they are not filled?
> > 6. If a pending order was placed before the two-hour window and gets filled within it, is that
> >    considered opening a trade within the window? Should such orders be cancelled before the window
> >    starts?
> > 7. Is modifying the price of an existing pending order within the window treated as placing a new
> >    one?
> > 8. For EURUSD, is the "relevant market" only the EURUSD trading session on your servers (as shown
> >    on the Symbols page and in the Trading Updates), or does the closure of other markets (for
> >    example, stock exchanges on Good Friday) also count?
> > 9. Can you confirm that the daily EURUSD break (23:55 to 00:05 server time) does not count as a
> >    market closure for this rule?
> >
> > Position size (question 2 of my previous email, which was not answered)
> > 10. The EA risks the same fixed percentage on every trade, so the lot size varies with the stop
> >     distance, and one trade can be up to about 5 times larger in lots than another with the same
> >     monetary risk. Does this count as "substantially larger position sizes"?
> >
> > Thank you in advance.
> >
> > Best regards,
> > Alex
>
> **A quién responde cada pregunta:**
>
> | Pregunta | Qué | Dónde se usa |
> |---|---|---|
> | 1-4 | mensajes al servidor | A-54 |
> | 5 | colocar una pendiente en la ventana | A-55; P1 (a) de `docs/validation/CIERRES-DE-MERCADO.md` §0.6 |
> | 6 | la pendiente puesta antes que se llena dentro, y si cancelarla | A-55; P1 (b) y (c) |
> | 7 | modificar una pendiente en la ventana | A-55; P1 (d) |
> | 8 | qué mercado es el «relevant market» | A-55; P2 |
> | 9 | el corte diario de EURUSD | A-55; P3 |
> | 10 | el tamaño de posición | R17 (§4 de abajo) |

> **Respuesta de soporte de FTMO a las preguntas 1 a 10 (ticket VDW-DPMWR-965; recuadro añadido el
> 2026-10-05 en la rama `trabajo/respuestas-ftmo`).** Fuente escrita: correo de `support@ftmo.com`
> recibido el **2026-10-05 a las 10:29:36 UTC**, en respuesta al correo de Aleks del 2026-10-03 (el
> de las diez preguntas, literal en el recuadro anterior). **El correo NO se copia**: su pie prohíbe
> compartirlo sin el consentimiento de FTMO, y el repositorio es público. Lo de abajo es la paráfrasis
> del consultor del 2026-10-05 (`docs/encargos/trabajo-respuestas-ftmo.md`), por número de pregunta.
> Las páginas públicas de FTMO que nombra la respuesta son Symbols y Forbidden Trading Practices.
>
> | Pregunta | Lo que responde | Estado | Qué cambia en el bot |
> |---|---|---|---|
> | 1 | Contesta en bloque a la 1, la 2 y la 3: todo tipo de orden cuenta para el límite de 2.000 órdenes al día. No distingue rechazadas, modificaciones, cancelaciones ni cierres, ni excluye ninguna. | respondida en parte | Nada: el freno (ADR-0067) ya cuenta todo lo que llega al servidor, también lo que el servidor rechaza. Lo que el propio bot niega no sale y no cuenta. |
> | 2 | La misma respuesta en bloque que la 1. | respondida en parte | Nada: como en la 1. |
> | 3 | La misma respuesta en bloque que la 1. | respondida en parte | Nada: como en la 1; cancelar y cerrar ya cuentan (ADR-0067 §3). |
> | 4 | El límite se reinicia a las 00:00 hora de Europa central (CET/CEST) cada día, igual que los objetivos y límites de trading. | respondida | Nada: coincide con `firma_huso_corte` = `Europe/Prague`, medido en las 730 medianoches de 2026 y 2027 (`docs/validation/RESPUESTAS-FTMO.md` §0.b). |
> | 5 | Colocar pendientes dentro de las dos horas se desaconseja si refleja intención de hacer gap trading y no trading genuino; recuerda que el gap trading está prohibido (Forbidden Trading Practices). No hay prohibición expresa de colocar. | respondida en parte | Nada: el bot sigue negando colocar dentro de la ventana (ADR-0068). Es una restricción ELEGIDA, más estricta que FTMO. |
> | 6 | Sin respuesta. | sin respuesta | Nada: `cierre_pendientes` sigue en `cancelar` (A-55). |
> | 7 | Modificar el precio de una pendiente dentro de la ventana se considera en general gestionar una orden existente, no abrir una operación nueva. | respondida | Nada: el bot sigue negando modificar dentro de la ventana (ADR-0068). Es una restricción ELEGIDA, más estricta que FTMO. |
> | 8 | Cada instrumento tiene su propio horario de cierre, y remite a la página Symbols, instrumento por instrumento. No menciona bolsas ni otros mercados. | respondida en parte (cuenta el horario del propio instrumento) | Nada: el calendario de EURUSD (`knowledge/cuentas/cierres/`) ya es el mercado relevante. |
> | 9 | El rollover de lunes a viernes no se considera gap trading. | respondida | Nada: la pausa diaria no es cierre. |
> | 10 | FTMO no valida estrategias, métodos de tamaño ni patrones de ejecución concretos, y no fija límites numéricos de exposición o de tamaño ni multiplicadores. «Sustancialmente mayor» depende del comportamiento histórico del propio trader. Recomienda evitar aumentos bruscos o desproporcionados del tamaño o del número de operaciones y mantener un tamaño consistente y consciente del riesgo, dentro de las reglas de gestión de riesgo de sus Términos. | respondida sin cifra; no se repregunta | Nada: el riesgo fijo del 0,5 % desde el primer día (ADR-0020) es el patrón histórico de la cuenta, y no hay nada que cambiar. |
>
> **Además**, una nota sobre el tipo de cuenta Normal, que no aplica a Swing (ADR-0026): se anota sin
> efecto.
>
> **Lo que eso deja:** A-54 y A-55 siguen ABIERTAS, respondidas en parte (la pregunta 6 sigue sin
> respuesta); R17 queda contestada sin cifra, y su línea de Technical Debt sale de `PROJECT_STATE.md`
> a `docs/state/HISTORIA.md`. Los recuadros anteriores no se editan.

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
