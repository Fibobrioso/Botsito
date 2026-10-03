# FUNCTIONALITY VALIDATION REPORT · Cierres de mercado

Rama `feature/cierres-de-mercado`, abierta el 2026-10-02 desde `main` `5947e55` (tag
`stable/F36p-freno-peticiones`, que apunta al merge `b64e675`). Encargo, copiado tal cual:
`docs/encargos/feature-cierres-de-mercado.md`. Es A3 e) de «Pendientes heredados». Tarea autónoma:
NO se cierra.

Objetivo: que el bot no abra ni coloque operaciones en la ventana prohibida por FTMO antes de un
cierre de mercado largo, según lo que FTMO dijo por escrito. Sin cobertura agregada: nada de esta
rama cuenta parejas ni compara con las operaciones del trader.

## 0. Fase 0 · Inventario y diseño, antes de escribir código

### 0.1 La regla, copiada tal cual

**R15, la página oficial** (`https://ftmo.com/en/forbidden-trading-practices/`). Está en
`docs/validation/FTMO-REGLAS.md` R15, leída el 2026-09-25. Se ha vuelto a descargar con `curl` el
**2026-10-03 hacia las 00:32 UTC** y dice lo mismo, con el paréntesis que R15 había recortado:

> perform gap trading (a high-risk practice that carries potentially unfavourable outcomes if
> performed in real market conditions due to increased volatility) by opening simulated trades: when
> major global news, macroeconomic events, or corporate reports or earnings are scheduled and they
> might affect the relevant financial market (i.e., a market that allows trading of financial
> instruments potentially impacted by the events); or two hours or less before a relevant financial
> market is closed for at least two hours;

**El ticket de soporte VDW-DPMWR-965 (29-09-2026) NO está literal en el repositorio.** Lo único que
hay es lo que Aleks trasladó en su brief de ese día, en el recuadro de `FTMO-REGLAS.md` (líneas
97-122): «**No se permite el gap trading** cuando hay programadas noticias globales importantes,
eventos macroeconómicos o resultados que puedan afectar al mercado, **ni dentro de las dos horas
previas al cierre de un mercado que va a estar cerrado al menos dos horas.**» El recuadro lo dice
así: «no hay cita literal en el repositorio». Para Aleks queda guardar el texto del correo (§0.6, P0).

**R7, lo que se puede mantener** (`FTMO-REGLAS.md` R7): «The FTMO Swing account type does not have
any restrictions on trading during news releases or on holding positions overnight (longer than 2
hours after market close) or over the weekend.»

**Qué prohíbe, punto por punto:**

| Pregunta del encargo | Lo que consta por escrito | Fuente |
|---|---|---|
| ¿Abrir? | **SÍ, prohibido**: «by opening simulated trades [...] two hours or less before» | R15 |
| ¿Colocar una pendiente dentro de la ventana? | **NO CONSTA.** R15 dice «opening simulated trades», no «placing orders» | — → A-55, P1 |
| ¿Una pendiente puesta ANTES que se llena DENTRO? | **NO CONSTA.** Si el llenado es «opening», cae dentro | — → A-55, P1 |
| ¿Mantener posiciones? | **SÍ, permitido** en Swing: «no restrictions on [...] holding positions [...] over the weekend» | R7 |
| ¿Cuántas horas antes? | **Dos, con el borde dentro**: «two hours or less before» | R15 |
| ¿Qué cierre cuenta como «largo»? | **Dos horas o más, con el borde dentro**: «closed for at least two hours» | R15 |
| ¿Qué mercado es el «relevant financial market» de EURUSD? | **NO CONSTA para los cierres.** La definición entre paréntesis («a market that allows trading of financial instruments potentially impacted by the events») va en la cláusula de las noticias | — → A-55, P2 |

**Fuera del encargo:** la primera mitad de R15, operar con noticias programadas. Sigue abierta en
`FTMO-REGLAS.md` §4 («R15 frente a R6») y esta rama no la toca.

### 0.2 Qué cierres tocan a EURUSD, y de dónde sale cada uno

**El horario de EURUSD en FTMO, medido.** Sale de la API que alimenta la página de símbolos
(`https://ftmo.com/wp-json/ftmo/symbols`, la misma de R9-R12). Leída el 2026-10-03 hacia las 00:33
UTC, con sha256 `6a8b1b36…709690617`, y no se versiona. Trae un campo `tradingHours` con las sesiones
de la semana en UTC, y `platformTimeOffset: {"UTC": 3, "Europe/Prague": 1}`. Para `EUR/USD`:

| inicio (UTC) | fin (UTC) |
|---|---|
| 2026-09-27 21:05 | 2026-09-28 20:55 |
| 2026-09-28 21:05 | 2026-09-29 20:55 |
| 2026-09-29 21:05 | 2026-09-30 20:55 |
| 2026-09-30 21:05 | 2026-10-01 20:55 |
| 2026-10-01 21:05 | 2026-10-02 20:55 |

Es decir, con el servidor en UTC+3: abre a las 00:05 y cierra a las 23:55 del servidor, y el corte
diario dura **10 minutos**, así que **no es un cierre largo**. El fin de semana va del viernes 20:55
UTC al domingo 21:05 UTC, **48 h 10 min**.

**El servidor sigue el horario de verano de EE. UU., por escrito.** La Trading Update del 5 de marzo
de 2026 (`trading-update-5-mar-2026`) dice: «On Sunday, 8 Mar 2026, the USA will transition to
Daylight Saving Time (DST). Therefore, trading on all platforms (MT4, MT5, cTrader, and DXtrade)
will be unavailable between 07:00 GMT+2 and 11:00 GMT+3.» Y la del 19 de marzo, sobre el 29 de marzo
en Europa: «Trading will not be interrupted». El servidor pasa de GMT+2 a GMT+3 con EE. UU. Con eso,
el cierre de las 23:55 del servidor es **las 16:55 de Nueva York todo el año**, y la apertura las
17:05. Esto es lo que A-28 pregunta (`broker_dst`), y la fuente escrita apunta a `us`. A-28 es una
MEDICION y no se cierra aquí: se cierra observando una transición (su texto).

**Cuándo toca un cierre la ventana del trader.** El bot solo busca entradas de 07:00 a 15:00 de
Madrid y cierra a las 15:00 (RN-001, RN-002). La ventana prohibida de un cierre que empieza en `C` es
`[C − 2 h, C)`, así que **solo toca la operativa si `C` cae antes de las 17:00 de Madrid** de un día
de lunes a viernes. Cada cierre conocido:

| Cierre | Desde | Hasta | ¿Largo? | Ventana prohibida en Madrid | ¿Toca 07-15? | Fuente |
|---|---|---|---|---|---|---|
| Corte diario | 16:55 NY | 17:05 NY | no (10 min) | — | no | API, `tradingHours` |
| Fin de semana | viernes 16:55 NY | domingo 17:05 NY | sí (48 h 10 min) | viernes 20:55-22:55 (19:55-21:55 cuando EE. UU. y Europa no coinciden: 8 a 29 de marzo y 25 de octubre a 1 de noviembre) | no | API; Trading Update 5-mar-2026 |
| Navidad 2025 | 24-12-2025 16:55 NY (el cierre de siempre) | 25-12-2025 17:05 NY | sí | 24-12, 20:55-22:55 | no | Trading Update 18-dic-2025: «Forex: 25th December Closed»; el 24, en blanco |
| Año Nuevo 2026 | 31-12-2025 16:55 NY | 01-01-2026 17:05 NY | sí | 31-12, 20:55-22:55 | no | ídem: «1st January Closed»; el 31, en blanco |
| Cambio de hora de EE. UU. | domingo 08-03-2026 05:00 UTC | 08:00 UTC | sí (3 h) | cae DENTRO del fin de semana | no | Trading Update 5-mar-2026 |

Las fechas de Navidad y Año Nuevo («25th December», «1st January») se leen como días del servidor:
cerrado de las 00:00 a las 24:00 del servidor, o sea de las 16:55 a las 17:05 de Nueva York. Es una
lectura, pero no cambia la ventana, porque el cierre empieza a la hora de cierre de siempre.

**El barrido de las Trading Updates.** Para saber si algún festivo cerró el Forex fuera de Navidad,
se descargaron las actualizaciones semanales de FTMO (cada jueves, `ftmo.com/en/blog/trading-updates/`)
y se buscó `Forex`, `EUR/USD`, `EURUSD`, `FX`, `currenc`, `Exotics`, `all symbols` y
`all instruments`. Leídas el 2026-10-03 entre las 00:35 y las 01:00 UTC:

- del 4-12-2025 al 1-10-2026 hay **44 jueves, y se leyeron 43** (recuento corregido tras el
  revisor, a4). La del 25-12-2025 no existe (HTTP 404), y esa semana la cubren las tablas de
  Navidad. Las 43 son:
  - **35** en el primer barrido, por nombre (`trading-update-<día>-<mes>-<año>`, del 4-12-2025 al
    13-08-2026). Se cortó ahí porque FTMO limita el ritmo (HTTP 429);
  - **la del 11-12-2025**, que tiene otro nombre (`11-december-2025`), y **la del 10-09-2026**,
    descargadas aparte;
  - **las 6 restantes** (20-08, 27-08, 3-09, 17-09, 24-09 y 1-10-2026), repetidas con 45 s de pausa
    entre una y otra.
- **Solo nombran el Forex las de Navidad** (11-dic, 18-dic y 1-ene, la misma tabla). Semana Santa
  (2-abr-2026) cierra índices, metales y acciones, no el Forex. La del 1-10 trae el festivo de Hong
  Kong (HK50.cash) y el cambio de hora de Australia, nada del Forex.

Con eso, el calendario cubre del **4-12-2025 al 7-10-2026**: del primer jueves revisado al día antes
del jueves siguiente a la última actualización. Los días de construcción (`knowledge/cases/dev`, del
1-4-2026 al 31-8-2026) caen todos dentro, también el Viernes Santo, 3-4-2026, en el que FTMO no
cerró el Forex.

**Conclusión: en todo el material (diciembre de 2025 a septiembre de 2026), ningún cierre largo de
EURUSD en FTMO cae antes de las 17:00 de Madrid.** La guardia no cambia ningún día medido. Es una red
para el día en que FTMO publique un cierre anticipado del Forex, como el «Close Early at 14:50» que
este diciembre puso a UK100.cash.

### 0.3 La fuente del calendario, y cómo se cruzan las dos

**1. La versionada en el repositorio:** `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`, un
calendario POR PERFIL, porque el horario es el de los servidores de la firma. Va en una subcarpeta
porque `perfil_del_repo` toma cada `*.yaml` de `knowledge/cuentas/` como un perfil. Lleva:
- `cubre`: desde y hasta qué día se han revisado las Trading Updates;
- `semanal`: el cierre y la apertura del fin de semana, con día, hora y **huso declarado**
  (`America/New_York`);
- `diario`: el corte diario, que no es largo pero se declara (un test comprueba que no bloquea);
- `extraordinarios`: cada cierre con fecha, inicio, fin, huso y fuente (la URL de la Trading Update
  y el día de lectura).

Cada hora declara su huso, como los libros (ADR-0039), y nada se pasa a UTC a mano.

**2. La de la plataforma, en vivo.** Hay dos, y ninguna se lee en esta rama:
- `SymbolInfoSessionTrade(símbolo, día de la semana, índice)` de MT5 da las sesiones POR DÍA DE LA
  SEMANA en el reloj del servidor. **Por su firma no puede expresar una fecha**: un festivo solo
  aparece si el broker cambia la plantilla esa semana, y eso no está medido;
- la API de FTMO (`tradingHours`) da sesiones FECHADAS en UTC, solo de la semana en curso (medido
  arriba).

**Cómo se cruzan: gana la más restrictiva, por unión.** Un cierre que aparezca en CUALQUIER fuente
cuenta. Las sesiones de la plataforma se convierten en cierres (los huecos entre sesiones), y
`domain/cierres.py` las une con las del calendario. Cuando una fuente trae un cierre largo que la
otra no tiene, la unión lo toma y el log lo apunta como DISCREPANCIA (WARNING), con el cierre y la
fuente que lo trae. Si la plataforma no responde, queda el calendario versionado, con un WARNING.

**Fuera de lo que cubre el calendario, se niega abrir y colocar** (motivo `cierre_sin_calendario`):
ante la duda, abstenerse y no aproximar (MASTER_PLAN H.2). En el simulador, el cableado se niega a
correr un día fuera de `cubre`, igual que con un parámetro UNKNOWN: así un calendario vencido no
cambia una medida en silencio.

En esta rama se implementan el predicado, el calendario versionado, la unión con sesiones (con
sesiones sintéticas en los tests) y su uso en el broker simulado. **Leer `SymbolInfoSessionTrade` en
el EA no entra**: es código de plataforma (`mql5/`) y el adaptador real de MetaTrader todavía no
existe en Python. Queda escrito como lo que tiene que hacer ese adaptador (§0.5).

### 0.4 En qué reloj se calcula, y el cambio de hora

**El encargo dice «el del servidor de FTMO; ADR-0063», y la medida lo matiza.** En el registro, el
reloj del servidor es UNKNOWN (`broker_offset_base`, `broker_dst`, A-28). Y ADR-0063 separa otros dos
relojes, el de las sesiones del trader y el del día de riesgo, que no son el del mercado. La ventana
prohibida no necesita ninguno de los tres:

- es **una duración antes de un instante**: `[C − margen, C)`, calculada en instantes absolutos
  (milisegundos UTC), como todo el broker;
- el reloj solo entra al **convertir la hora declarada de un cierre en un instante**, cada una con
  su huso. Según la Trading Update del 5-mar-2026, el servidor de FTMO es Nueva York + 7 todo el año
  (§0.2), así que «23:55 del servidor» se declara como «16:55 `America/New_York`», y `zoneinfo` pone
  el cambio de hora en su sitio. **Es PROVISIONAL bajo A-28** (revisor, a1): lo dice una fuente
  escrita, no una medida. Pero no cambia la operativa con ninguna lectura de `broker_dst`. Con `us`,
  el cierre del viernes son las 22:55 de Madrid (21:55 en las semanas desalineadas). Con `eu`, el
  servidor sería Praga + 1 y cerraría a las 22:55 de Madrid. Con `ninguno` (GMT+2 fijo), a las 22:55
  o a las 23:55. La ventana empezaría, como pronto, a las 19:55 de Madrid.

**El cambio de hora.** Las dos horas son dos horas de reloj absoluto, nunca de pared. El 25-10-2026
(último domingo de octubre) Europa pasa a invierno y Nueva York no hasta el 1-11. Esa semana el cierre
del viernes 30-10 son las 20:55 UTC, las 21:55 de Madrid, y la ventana va de las 19:55 a las 21:55 de
Madrid: una hora antes que la semana anterior en el reloj de Madrid, y la misma en el de Nueva York.
Un cierre sintético justo después del cambio, el domingo 25-10, abre una ventana de exactamente
7.200.000 ms, ni una hora más ni una menos de pared. Los tests de la Fase 2 lo fijan.

### 0.5 El diseño

**Dónde vive: en el puerto del broker, como el freno (ADR-0067 §1).**
- `src/botsito/domain/cierres.py` (puro, sin IO ni reloj): `Cierre`, `CalendarioCierres`,
  `cierres_desde_sesiones`, `unir_cierres` y el predicado único
  **`ventana_prohibida_por_cierre(instante_ms, calendario, margen_ms, minimo_ms)`**, que devuelve
  `None` o la prohibición con su motivo y su cierre.
- `src/botsito/engine/calendario_cierres.py`: lee y valida el YAML y expande la pauta semanal en
  instantes.
- `engine/broker.py`: `ReglasBroker.cierres` (calendario, margen, mínimo y política de pendientes).
  `_colocar` y `modificar` preguntan al predicado ANTES que al freno: lo que se niega por un cierre
  no llega al servidor y no se cuenta. Las siete reglas que envían peticiones (ADR-0067 §1) pasan
  por esos métodos, así que ninguna se lo salta.

**Lo que bloquea el predicado:** de `C − 2 h` hasta que el cierre ACABA, con los dos bordes de R15
dentro. Además de las dos horas previas entra el propio cierre: con el mercado cerrado tampoco se
coloca (el servidor lo rechazaría). Solo cuentan los cierres de dos horas o más: el corte diario de
10 minutos no bloquea nada. Y fuera de lo que cubre el calendario, `cierre_sin_calendario`.

**Lo que hace dentro de la ventana:**
- **colocar** (limite o stop): se niega con un `Rechazo` de motivo `cierre_mercado`;
- **modificar una pendiente** (reubicar, RN-006): se niega igual y la orden sigue como estaba. Una
  pendiente que se mueve es una orden nueva en otro precio;
- **modificar una pendiente**, se niega. Se toma como colocarla en otro precio, que es lo más
  restrictivo, y va como pregunta en A-55 (P1 d). Con `cancelar` no llega a pasar, porque la
  pendiente ya se canceló al empezar la ventana (revisor, b2);
- **una pendiente ya puesta**: lo dice `cierre_pendientes`, que es PROVISIONAL bajo A-55 porque la
  regla escrita no lo dice:
  - `cancelar`, el valor de partida y el más restrictivo: al EMPEZAR la ventana el broker la cancela,
    lo que protege la cuenta y cuenta como petición (ADR-0067 §3), antes que cualquier llenado de ese
    mismo instante;
  - `mantener`: sigue, y puede llenarse dentro;
- **una posición abierta**: nada. R7 lo permite por escrito. Mover su stop y cerrarla siguen igual;
- `abrir_conocida` (una operación del trader que se repite) no pasa por el predicado: no la emite el
  bot.

**Los parámetros (ADR-0002):**
- `firma_gap_margen_minutos` = 120 («two hours or less before») y `firma_gap_cierre_minimo_minutos`
  = 120 («closed for at least two hours»). Son `prop_firm`, CONFIRMED, citan R15 y van en el perfil
  de FTMO y en `parametros.yaml` con el mismo valor, como `firma_mensajes_dia_max`;
- `cierre_pendientes` (`cancelar` | `mantener`) = `cancelar`, de categoría `ejecucion`,
  DEFAULT_AMBIGUOUS bajo **A-55**, nueva.

**A-55**, de clase `medicion` como A-54: es una pregunta a soporte de FTMO, no al trader, y la clase
`pregunta` la llevaría al cuestionario del trader (`cases/cuestionario.py`). Lleva P1 y P2, y cita
la evidencia de relleno de A-54, porque el esquema exige una (deuda ya anotada en `PROJECT_STATE.md`).

**Todo bloqueo, en el log y en la traza.** Cada colocación o modificación negada y cada pendiente
cancelada al empezar la ventana van al log (INFO) y a `Traza.cierres` con su motivo. El informe del
arnés lleva una sección «Los cierres de mercado» que dice el calendario, su cobertura y cada bloqueo
por día.

**El adaptador real de MetaTrader** (cuando exista) arma el mismo `ReglasBroker`: lee las sesiones
con `SymbolInfoSessionTrade`, las pasa por `cierres_desde_sesiones` y las une al calendario
versionado con `unir_cierres`. Lo apunta el ADR nuevo de esta rama.

**Rutas.** El contrato se amplía en un commit a `knowledge/cuentas/` (el perfil y el calendario).

### 0.6 Preguntas para soporte de FTMO (en inglés)

- **P0 (para Aleks, no para FTMO):** guardar en el repositorio el texto literal de la respuesta del
  ticket VDW-DPMWR-965, como cualquier otra fuente escrita.
- **P1 (A-55):** «Regarding the forbidden practice of gap trading "two hours or less before a
  relevant financial market is closed for at least two hours": (a) does it also apply to *placing*
  pending orders (limit or stop) within those two hours, even if they are not filled? (b) If a
  pending order was placed *before* the two-hour window and it gets filled *within* it, is that
  considered opening a trade within the window? (c) Should such pending orders be cancelled before
  the window starts? (d) Is *modifying* the price of an existing pending order within the window
  treated as placing a new one?»
- **P2 (A-55):** «For EURUSD on MT5, is the "relevant financial market" only the EURUSD trading
  session on your servers (as published on the Symbols page and in the Trading Updates), or does
  the closure of other markets (for example, US or European stock exchanges on Good Friday) also
  count for this rule?»
- **P3 (A-55):** «Can you confirm that the daily EURUSD break (23:55-00:05 server time, about ten
  minutes) does not count as a market closure for this rule, and that the closure times we should
  use are the ones in your platform's symbol sessions and Trading Updates (server time, GMT+2/GMT+3
  following US daylight saving time)?»

## 1. Fase 1 · Implementación

Lo escrito en §0.5, con un ajuste que el diseño ya decía: el predicado bloquea también mientras el
cierre dura.

| Fichero | Qué |
|---|---|
| `src/botsito/domain/cierres.py` (nuevo) | `Cierre`, `CalendarioCierres`, `ReglasCierres`, `Prohibicion`; el predicado único **`ventana_prohibida_por_cierre`**; `proxima_prohibicion` (cuándo empieza la próxima ventana, para cancelar pendientes); `cierres_desde_sesiones`, `juntar_cierres` y `unir_cierres` con `FuenteCierres` y `Discrepancia` (gana la más restrictiva). Sin IO, sin reloj y sin cifras |
| `src/botsito/engine/calendario_cierres.py` (nuevo) | Lee y valida `knowledge/cuentas/cierres/<perfil>.yaml`: claves exactas, `perfil` igual al nombre del fichero, huso IANA en cada hora, fuente en cada extraordinario. Expande la pauta semanal y la diaria día a día en su huso, con una semana de margen a cada lado, y lo une todo |
| `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml` (nuevo) | El calendario de FTMO, con lo de §0.2: cubre del 4-12-2025 al 7-10-2026; viernes 16:55 a domingo 17:05 de Nueva York; corte diario 16:55-17:05; Navidad, Año Nuevo y el cambio de hora de EE. UU. del 8-3-2026, cada uno con su Trading Update |
| `src/botsito/engine/broker.py` | `ReglasBroker.cierres`. `_colocar` y `modificar` preguntan al predicado ANTES que al freno; lo negado es un `Rechazo` con su motivo, no se envía ni se cuenta. La cancelación al empezar la ventana es un candidato más de `_proximo_evento`, que en el mismo instante va antes que cualquier llenado; como `cancelar`, es una petición del bot y no un evento del servidor (no va a `Traza.eventos`). `Traza.cierres` y el log (INFO) |
| `src/botsito/engine/simulacion.py` | `reglas_cierres_de(perfil, registro, calendario)`, y `reglas_broker_de(perfil, registro, calendario)` lo arma cuando llegan las dos cosas |
| `src/botsito/engine/perfil_cuenta.py` | El accesor `minutos`, que faltaba: la lectura es estricta por tipo (ADR-0002), y `entero` no lee unos `minutos` |
| `src/botsito/engine/cableado.py` | `calendario_del_perfil` carga el calendario (sin él, no corre) y `comprobar_que_cubre` se niega a correr un día fuera de `cubre`. `TrazaBroker.cierres`, y la sección «Los cierres de mercado (ADR-0068)» del informe del arnés |
| `knowledge/spec/parametros.yaml` y el perfil | `firma_gap_margen_minutos` = 120 y `firma_gap_cierre_minimo_minutos` = 120 (CONFIRMED, R15), en los dos con el mismo valor; `cierre_pendientes` = `cancelar` (DEFAULT_AMBIGUOUS, A-55), en el registro. La descripción de `firma_noticias_restringe` en el perfil decía que R15 «no se modela»: ahora dice que la mitad de los cierres sí |
| `knowledge/spec/ambiguedades.yaml`, `PROJECT_STATE.md` | **A-55**, abierta, clase `medicion`, no bloqueante, con su fila en «Known Ambiguities» |
| `docs/spec/` | Regenerado con `botsito spec docs --escribir` |
| `docs/adr/0068-…md` y `docs/adr/README.md` | ADR-0068 y su fila en el índice |

**Lo que NO se ha tocado:** `mql5/` (el EA y `SymbolInfoSessionTrade`). El adaptador real de
MetaTrader todavía no existe en Python, y su unión con el calendario está escrita en ADR-0068 §4 y
probada con sesiones sintéticas. Como no se toca nada que dependa de la plataforma, no hace falta la
CI de Linux por `fix/`. `abrir_conocida` tampoco pasa por el predicado, porque no la emite el bot.

**Sin calendario, el predicado queda apagado** (revisor, a5). `reglas_broker_de(perfil, registro)`
sin calendario arma el broker con `cierres=None`, como sin registro lo arma sin los umbrales del
freno. Pasa en los tests que construyen el broker a mano y en `scripts/repeticion_trader.py` y
`scripts/viabilidad_trader.py`, que repiten operaciones del trader con `abrir_conocida` y no colocan
nada. El cableado, que es el camino del bot, siempre lo pasa, y sin calendario no corre. Un test lo
fija.

## 2. Fase 2 · Tests, rompiendo la guardia a propósito

`tests/unit/test_cierres_de_mercado.py`: 25 funciones, 28 casos. Los cinco que pide el encargo:

| Encargo | Test | Qué fija |
|---|---|---|
| Un viernes: no dentro, sí justo antes | `test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_justo_antes` | Con el calendario REAL de FTMO, viernes 25-9-2026: a las 18:54:59.999 UTC la compra sale; a las 18:55:00.000 y a las 20:54:59.999, `Rechazo` `cierre_mercado`; lo negado no existe, no es petición y queda en `Traza.cierres` |
| Festivo con cierre anticipado sintético | `test_un_cierre_anticipado_mete_la_ventana_en_la_operativa` | Un cierre inventado a las 14:00 de Madrid (2030): la ventana empieza a las 12:00 de Madrid, DENTRO de la operativa; a las 11:59:59.999 sale, a las 12:00 no |
| El cambio de hora del último domingo de octubre | `test_el_cambio_de_hora_de_octubre_no_mueve_la_ventana_de_mas` y `test_un_cierre_justo_despues_del_cambio_tiene_dos_horas_absolutas` | Con `cubre` alargado (sintético): la ventana del viernes empieza a las 18:55 UTC el 23-10 y el 30-10, y a las 19:55 UTC el 6-11; en Madrid, 20:55, 19:55 y 20:55. Siempre dos horas absolutas. Y un cierre a las 03:30 de Madrid del 25-10 abre su ventana a las 00:30 UTC (02:30 de verano), no a la 01:30 de la pared, que estaría una hora antes |
| Un día normal no bloquea nada | `test_un_dia_normal_no_bloquea_nada` | Miércoles 23-9-2026, minuto a minuto las 24 horas: nada prohibido; ocho compras de 05:00 a 12:00 UTC, todas salen |
| Con el predicado desactivado, fallan | `test_sin_el_predicado_el_viernes_se_coloca_dentro` y la medida de abajo | Con el predicado parcheado a «nada prohibido», la compra del viernes dentro de la ventana SALE, y el test del viernes y el del festivo fallan |

Los demás: los bordes de R15 (un cierre de exactamente 2 h cuenta; uno de 2 h menos 1 ms, no), el
corte diario que no bloquea, el mercado cerrado, la pendiente cancelada al empezar la ventana antes
que un llenado del mismo instante, `mantener` (se llena dentro), modificar negado, la posición que
sigue y mueve su stop, el log, fuera del calendario, Navidad y Año Nuevo en el calendario real (y
que ningún cierre largo empieza antes de las 17:00 de Madrid un día laborable), la unión con
sesiones y su discrepancia, cuatro calendarios mal escritos, cierres sin unir y las reglas que salen
del perfil, del registro y del calendario.

**Por el cableado, de punta a punta** (añadidos tras el revisor, b1 y a3):
- `test_el_cableado_no_corre_sin_calendario_ni_fuera_de_lo_que_cubre`: `calendario_del_perfil` sin
  fichero y `comprobar_que_cubre` con un día fuera, los dos con `CableadoError`;
- `test_por_el_motor_la_colocacion_en_la_ventana_se_niega_y_sale_en_el_informe`: el día sintético
  de `test_cableado` por `MotorCableado`, con la ventana abierta antes de colocar. La colocación se
  niega, nada se llena, y el informe del arnés trae la línea con su instante y su motivo;
- `test_por_el_motor_la_pendiente_se_cancela_al_empezar_la_ventana`: la ventana empieza entre la
  colocación y el llenado. Los instantes salen de una corrida sin cierres, no se escriben a mano. La
  pendiente se cancela en ese instante, nada se llena, la cancelación es una petición y el motor
  sigue.

**La guardia rota, medido** (repetido tras los tests nuevos). Con `return None` en la primera
línea útil de `ventana_prohibida_por_cierre`, restaurado justo después (`git diff` del fichero,
vacío):

```
FAILED test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_justo_antes
FAILED test_con_el_mercado_cerrado_tampoco_se_coloca_y_al_abrir_si
FAILED test_la_pendiente_puesta_antes_se_cancela_al_empezar_la_ventana
FAILED test_modificar_una_pendiente_dentro_se_niega_y_la_deja_como_estaba
FAILED test_cada_bloqueo_va_al_log_con_su_motivo
FAILED test_un_cierre_anticipado_mete_la_ventana_en_la_operativa
FAILED test_los_bordes_de_r15_van_dentro
FAILED test_el_cambio_de_hora_de_octubre_no_mueve_la_ventana_de_mas
FAILED test_un_cierre_justo_despues_del_cambio_tiene_dos_horas_absolutas
FAILED test_fuera_de_lo_que_cubre_el_calendario_no_se_coloca
FAILED test_gana_la_mas_restrictiva_y_la_discrepancia_se_dice
FAILED test_por_el_motor_la_colocacion_en_la_ventana_se_niega_y_sale_en_el_informe
FAILED test_por_el_motor_la_pendiente_se_cancela_al_empezar_la_ventana
```

Fallan 13 de 28. Pasan los que esperan que NO se prohíba nada (día normal, corte diario, la
ventana del viernes lejos de la operativa), los que no pasan por el predicado (el calendario y sus
errores, las reglas, `mantener`, la posición) y el del monkeypatch, que espera justo eso.

**Dos errores míos en los tests, cazados al correrlos.** (1) El tick del llenado no cruzaba el
precio de la límite. (2) Puse el ejemplo del cambio de hora en la 01:00 UTC del 25-10, que es
exactamente el salto: ahí la pared y el reloj absoluto dan lo mismo, y el test no probaba nada. Se
movió a las 03:30 de Madrid, donde la resta en la pared se equivoca en una hora.

## 3. Lo que cambia en el arnés

El arnés simulado se corrió en DIAGNÓSTICO, con las lecturas de `CONTADOR-PETICIONES.md` §4: A-35
`cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control` y A-27 a 0. Sin A-35, el
motor se niega a correr (medido). Se corrió dos veces, sobre los mismos días de construcción:
- con el código de esta rama;
- con el de `main` (`5947e55`), en un clon desechable (`git worktree add` en la carpeta de trabajo,
  con `data` apuntado al del repositorio por `config/settings.local.toml`, sin copiar ni enlazar
  nada). La guardia de Claude bloqueó un primer intento con `cmd /c mklink` y no se rodeó.

**Sin cobertura agregada:** las salidas no se leyeron. Un guion las comparó línea a línea y solo
sacó números de línea, hashes y la sección nueva:

| | líneas | sha256 (16) |
|---|---|---|
| `main` | 842 | `e9854b6457cbe227` |
| rama, sin la sección nueva | 842 | `e9854b6457cbe227` |

**Idénticas byte a byte.** La rama solo añade, al final:

```
### Los cierres de mercado (ADR-0068)
calendario: cubre 2025-12-04 05:00 a 2026-10-08 04:00 UTC, 228 cierres; margen 120 min, minimo 120 min; pendientes: se cancelan
ninguna peticion negada ni ninguna pendiente cancelada
```

(Cada línea lleva delante las etiquetas `[DIAGNOSTICO-…]`, quitadas aquí.) Es lo que decía §0.2:
ningún cierre largo cae en la operativa de ningún día de construcción, y la guardia no cambia nada
medido. `cubre` empieza a las 05:00 UTC porque el día se cuenta en el huso del calendario, Nueva
York.

**Repetido con el código final**, tras los cambios por el revisor (a3 y la extracción de b1): la
rama, sin la sección nueva, vuelve a dar 842 líneas y `e9854b6457cbe227`, idéntica a `main`, y la
misma sección.

## 4. Lo que encontró el revisor, y qué se hizo

El informe del revisor, entero, va al final. Ningún hallazgo bloqueaba.

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Declarado PROVISIONAL bajo A-28.** El huso `America/New_York` del calendario supone que el servidor cambia de hora con EE. UU., y eso lo dice una Trading Update, no una medida. Va así en el encabezado y en §3 de ADR-0068, en la cabecera del calendario y en §0.4. Se mide que no cambia la operativa con ninguna lectura de `broker_dst` (§0.4). A-28 no se toca: es una medición |
| a2 | importa | El `## Estado` dice el estado real (abajo) |
| a3 | importa | **Cambiado.** La cancelación por cierre ya no añade un evento a `Traza.eventos`. Como `cancelar()`, es una petición del bot, no algo que hace el servidor, y no llega al motor como `EventoBroker` ni cuenta en `por_fuente`. Queda en las peticiones, en `Traza.cierres` y en el log. Probado por el motor (b1) |
| a4 | menor | **Corregido** el recuento del barrido (§0.2): 44 jueves, 43 leídas, desglosadas |
| a5 | menor | **Dicho** en §1: sin calendario el predicado queda apagado, y dónde pasa |
| b1 | importa | **Hecho.** El código nuevo del cableado sale a dos funciones, `calendario_del_perfil` y `comprobar_que_cubre`, y tres tests nuevos lo prueban, dos de ellos de punta a punta por `MotorCableado` (§2). Con la guardia rota fallan también los dos de punta a punta: 13 de 28 |
| b2 | importa | **Declarado bajo A-55**, sin parámetro nuevo. Con `cancelar`, el valor de partida, no hay pendiente que modificar dentro de la ventana, porque ya se canceló al empezar, así que el caso solo existe con `mantener`. Negar la modificación es lo más restrictivo. A-55 y la pregunta P1 (d) lo preguntan, y si FTMO dice que modificar no es colocar, se deja de negar. **Para el consultor:** si prefiere un parámetro propio, es una línea en el broker y otra en el registro |
| b3 | menor | **Declarado** en ADR-0068 §2 como más allá de la letra de R15: el mercado cerrado y fuera del calendario |

**Dos rojos de `make check` en la rama, los dos míos:**
- citar «ADR-0068» en el informe de la Fase 0, antes de que el ADR existiera, rompió
  `knowledge validate`;
- dos ficheros redactados en la carpeta de trabajo llegaron con CRLF y rompieron
  `test_no_crlf_in_tracked_text_files`.

Los dos se corrigieron antes de commitear, y ningún commit lleva un rojo. Propuesta de fila para
`docs/runbooks/ERRORES-RECURRENTES.md`, que queda fuera del contrato de esta rama: «un id futuro
citado en un informe de Fase 0» y «CRLF desde la carpeta de trabajo», con su señal (los dos tests
de arriba) y qué hacer (correr `knowledge validate` y buscar CR en lo estadiado antes de lanzar
`make check`).

**Para el cierre** (no lo hace esta rama): la línea «e) calendario de cierres de mercado» de
«Pendientes heredados» en `PROJECT_STATE.md` tiene evidencia con esta rama. La quita el cierre, si
el consultor lo decide.

## 5. Informe del revisor

Pegado tal cual, sobre `227bc5e`; lo que se hizo con cada hallazgo, en §4.

> ## Informe del revisor · feature/cierres-de-mercado · 2026-10-02
>
> Base: `git merge-base main HEAD` = 5947e554. Commits: 369d9f8, 94b28ad, 227bc5e. `git status --short` limpio. HEAD^{tree} = 894e9dd666042a46bcd40f2634bcae4189d00129.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 3 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | **El calendario y el ADR dan por hecho el reloj del servidor, y A-28 sigue abierta.** El informe afirma como hecho «El servidor de FTMO es Nueva York + 7 todo el año (§0.2)». ADR-0068 §3 dice «ese reloj cambia de hora con EE. UU.». El YAML del calendario declara todo en `America/New_York`. Pero A-28 (`broker_dst`: `us`/`eu`/`ninguno`) es una MEDICION abierta que «NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE». La base es una Trading Update web, que no se versiona. El encabezado PROVISIONAL del ADR cubre solo `cierre_pendientes`, no esta hipótesis. No cambia ningún día medido: ningún cierre cae antes de las 17:00 de Madrid. Pero es una decisión no declarada como provisional. | `docs/validation/CIERRES-DE-MERCADO.md` §0.4; `docs/adr/0068-*.md` líneas 8-11 (encabezado) y §3; `knowledge/spec/ambiguedades.yaml:651-662` (A-28); `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml` (cabecera y `semanal`) |
> | a2 | importa | **El «Estado» del informe está desfasado.** Acaba en «EN CURSO: Fases 0, 1 y 2 hechas; falta el arnés, el sello y el revisor». Pero §3 ya cuenta el arnés corrido y comparado, y `make-check.log` ya trae el sello. El informe de la rama tiene que acabar en su estado real al declararla lista. | Última línea de `docs/validation/CIERRES-DE-MERCADO.md` frente a §3 y a `make-check.log` |
> | a3 | importa | **La cancelación por cierre hace algo que `cancelar()` no hace, y nada lo prueba a través del cableado.** `_cancelar_por_cierre` añade `(instante, CANCELADA, id, TICKS)` a `_eventos`. El `cancelar()` manual no añade nada. En `_a_la_cuenta` ese evento cae en el `else`: sube a `ctx.eventos` como `EventoBroker(CANCELADA)`, que las reglas pueden ver, y suma al recuento `por_fuente[TICKS]`. En el arnés de §3 no hubo ni una cancelación («ninguna peticion negada ni ninguna pendiente cancelada»). Ningún test pasa por `construir_motor_cableado` ni por `MotorCableado`. Es un camino nuevo, sin ejercitar de extremo a extremo. | `broker.py` (`_cancelar_por_cierre`, que escribe en `self._eventos`) frente a `broker.py:494-503` (`cancelar`); `cableado.py` `_a_la_cuenta`, rama `else`; `grep -n "construir_motor_cableado\|cableado" tests/unit/test_cierres_de_mercado.py` sin salida |
> | a4 | menor | **El recuento de las Trading Updates se solapa.** «las 35 de cada jueves [4-12-2025 a 13-08-2026], más la del 10-09-2026 y la del 11-12-2025». Del 4-12-2025 al 13-08-2026 hay 37 jueves, 36 sin el 25-12 (404). El 11-12 ya es uno de ellos. El 10-09 aparece luego otra vez entre «las 7 que faltaban» (20-08 a 1-10). Las cifras no cuadran limpias. Las fuentes web no se pueden verificar. | `docs/validation/CIERRES-DE-MERCADO.md` §0.2, «El barrido de las Trading Updates» |
> | a5 | menor | `reglas_broker_de(perfil, registro)` sin calendario devuelve `cierres=None`: el predicado queda apagado en silencio. Hoy solo ocurre en tests y en `scripts/repeticion_trader.py` y `scripts/viabilidad_trader.py`, que repiten operaciones del trader con `abrir_conocida`. Un test lo fija (`... .cierres is None`). Conviene que el informe lo diga. | `simulacion.py:121-150`; `tests/unit/test_cierres_de_mercado.py:415`; `scripts/repeticion_trader.py:80` |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` dio: `CONTRATO: 23 ficheros dentro del contrato de feature/cierres-de-mercado (riesgo alto, artefacto docs/validation/CIERRES-DE-MERCADO.md, 4 comprobaciones para el revisor)`. Ningún fichero en `rutas_protegidas`.
> - **`uv run botsito state check`:** OK (rama y funcionalidad actual).
> - **`uv run botsito spec check`:** OK, 35 reglas, hash del manifiesto al día.
> - **`uv run botsito knowledge validate`:** lo ejecuté a stdout, sin el `> knowledge-validate.log` que escribiría. OK: «296 documentos: todo id citado existe», «149 registros de feedback... commits con Fuente», «55 ambiguedades registradas», «437 items de evidencia». Los AVISO son preexistentes.
> - **`make check`: no lo ejecuté.** Escribe, y mi función es solo lectura. La evidencia es `make-check.log` (21:21; el commit es de 21:22):
>   - `All checks passed!`
>   - `1857 passed in 665.11s`
>   - `SELLO: make check en verde sobre el arbol 894e9dd666042a46bcd40f2634bcae4189d00129`, igual al `HEAD^{tree}`
>   - `PICO DE MEMORIA ... 286 MiB`
> - `pytest tests/unit/test_cierres_de_mercado.py -q -p no:cacheprovider`: 25 pasan. Son 22 funciones, y la parametrización de 4 casos da 25, como dice el informe.
> - **Trailer `Fuente:`.** El único commit que toca `knowledge/spec/` es 227bc5e. Lleva `Fuente: ADR-0068, ADR-0067, ADR-0050` en el cuerpo, y los tres existen.
> - **Regímenes de cambio.** `git diff --name-status` solo muestra A y M. Nada en `knowledge/evidence`, `feedback`, `cases`, `corpus` ni `data/manifests`. HISTORIA solo con líneas añadidas.
> - **Ambigüedades.** A-55 abierta: el mismo commit toca `docs/spec/ambiguedades.md` y la fila de «Known Ambiguities» de `PROJECT_STATE.md`. La evidencia de relleno `ev-v4-012524-0ef85a89` existe y el propio texto de A-55 la declara de relleno.
> - **ADR-0068.** `## Estado` empieza por `ACTIVE`; fila añadida al README.
> - **Informes cerrados.** Ningún `docs/validation/*.md` previo cambia.
> - **Tres guardias de `cita`.** No aplica: la rama no añade sitios con `cita` a la spec.
> - **ADR-0002.** Margen y mínimo van al registro y al perfil con el mismo valor (120), citando R15. `cierre_pendientes` es DEFAULT_AMBIGUOUS con `ambiguedad_id: A-55`. `broker.py` y `domain/cierres.py` no llevan cifras de negocio, y `test_no_business_literals` pasó en `make check`.
> - **`PROJECT_STATE.md`:** 22.825 bytes, por debajo de 23.000 y de 25.000. El recuento «1205 funciones» es 1183 + 22.
> - **Holdout y material.** Sin exposiciones: no se abre ningún libro, imagen ni fotograma. El arnés se corrió sobre días de construcción y sus salidas se compararon por hash y por líneas.
> - **Tres citas del informe contra su fuente en el repo:**
>   - R7 y R15: coinciden con `docs/validation/FTMO-REGLAS.md` líneas 54 y 62.
>   - El recuadro del ticket VDW-DPMWR-965: coincide con las líneas 97-122 y con lo que el informe dice de él, «no hay cita literal».
>   - El «or less» y el «at least» están reflejados en `ventana_prohibida_por_cierre`: `c.inicio - margen > instante` rompe, así que el borde queda dentro, y `duracion >= minimo` también.
> - **Fechas del calendario:** 4-12-2025 y 1-10-2026 son jueves, y 7-10-2026 es el día antes del jueves siguiente.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 22 hechos (1 de ellos «de otra forma» y declarado), 1 parcial, 0 no hechos; 1 pendiente (pegar este informe, lo hace el caller).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Fase 0: copia literal de la regla (R15 y el ticket) | Hecho | §0.1. R15 literal con el paréntesis recortado antes. El ticket no está literal en el repo, y el informe lo dice con P0 para Aleks |
> | 2 | Qué prohíbe: abrir, colocar, mantener; horas; cierre «largo»; lo que no consta, como pregunta | Hecho | Tabla de §0.1. Lo que no consta va a A-55 P1 y P2 |
> | 3 | Preguntas a soporte en inglés | Hecho | §0.6, P1-P3 |
> | 4 | Cierres que afectan a EURUSD en 07-15 de España, con su origen | Hecho | Tabla de §0.2: API `tradingHours`, Trading Updates. Las fuentes web no son verificables |
> | 5 | Fuente del calendario: YAML o servidor, cómo se cruzan, gana la más restrictiva | Hecho | §0.3 y `domain/cierres.py::unir_cierres`. La lectura de `SymbolInfoSessionTrade` no entra, y se declara (código de plataforma) |
> | 6 | Reloj de la ventana y cambio de hora | Hecho de otra forma, declarado | §0.4: instantes absolutos, y el encargo se matiza respecto a ADR-0063. Ver hallazgo b1 |
> | 7 | Diseño escrito antes de implementar | Hecho | 94b28ad (informe, 245 líneas) es anterior a 227bc5e (código) |
> | 8 | Predicado único donde ninguna regla pueda saltárselo | Hecho | `broker.py` `_colocar` y `modificar` llaman a `_prohibido_por_cierre` antes que a `_admitir`. Las únicas vías de colocación son `colocar_limite` y `colocar_stop`, que van por `_colocar`. `abrir_conocida` queda fuera y no la emite el bot (declarado, solo la usan scripts de repetición) |
> | 9 | Dentro de la ventana no abre ni coloca | Hecho | `ventana_prohibida_por_cierre`; tests del viernes, del cierre y del festivo sintético |
> | 10 | Pendientes y posiciones: solo lo que diga FTMO; si no lo dice, parámetro PROVISIONAL colgado de una ambigüedad nueva | Parcial | Posición: R7, sin cambio. Pendiente puesta: `cierre_pendientes` PROVISIONAL bajo A-55. Pero modificar una pendiente se niega fijo, sin parámetro (b2) |
> | 11 | Horas de margen como parámetro del registro, con la cita de la regla | Hecho | `parametros.yaml`: `firma_gap_margen_minutos` y `firma_gap_cierre_minimo_minutos`, ambos con R15 en la descripción |
> | 12 | Todo bloqueo en el log con su motivo | Hecho | `LOG.info` en `_prohibido_por_cierre` y en `_cancelar_por_cierre`; `test_cada_bloqueo_va_al_log_con_su_motivo` |
> | 13 | Test: viernes, no dentro y sí justo antes | Hecho | `test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_justo_antes`: 18:54:59.999 sale, 18:55:00.000 no |
> | 14 | Test: festivo con cierre anticipado sintético | Hecho | `test_un_cierre_anticipado_mete_la_ventana_en_la_operativa` |
> | 15 | Test: cambio de hora de octubre | Hecho | Dos tests, con `cubre` sintético alargado. Cuadra con la aritmética UTC y de Madrid: viernes 23-10 y 30-10 a las 18:55 UTC, y 6-11 a las 19:55 UTC |
> | 16 | Test: día normal sin bloqueos | Hecho | `test_un_dia_normal_no_bloquea_nada` |
> | 17 | Con el predicado desactivado, los tests fallan | Hecho, no reproducido por mí | Informe §2: 11 de 25 fallan con `return None` puesto. Reproducirlo exige editar el fichero y no lo hice. Existe además `test_sin_el_predicado_el_viernes_se_coloca_dentro`, que parchea el predicado a «nada prohibido» y espera exactamente ese resultado |
> | 18 | Sin cobertura agregada sobre las 77 | Hecho | §3: salidas comparadas por hash y línea, no leídas; el calendario solo cubre fechas |
> | 19 | Informe con preguntas en inglés | Hecho | §0.6 |
> | 20 | CI de Linux por `fix/` solo si se toca algo dependiente de la plataforma | Hecho | No se toca `mql5/` ni nada de plataforma; el informe lo declara. Sin guardia de Claude tocada |
> | 21 | `make check` sellado | Hecho | Sello = árbol de HEAD (ver eje a) |
> | 22 | `PROJECT_STATE` por debajo de 23.000 bytes | Hecho | 22.825 |
> | 23 | La rama no se cierra | Hecho | Sin merge ni tag; `PROJECT_STATE` dice «NO se cierra» |
> | 24 | Revisor con su informe pegado | Pendiente | Este informe se devuelve; lo pega quien la prepara |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **El código nuevo de `construir_motor_cableado` no tiene ningún test.** Es el calendario que se carga siempre, el `CableadoError` por perfil sin calendario, la negativa a correr fuera de `cubre` y la sección `_informe_cierres`. El informe y el ADR §7 lo presentan como garantía («se niega a correr»), y no hay prueba de que lo haga. La Fase 2 del encargo pide «tests, rompiendo la guardia a propósito». Lo único que lo ejercita es el arnés, por la rama «dentro» y a mano. | `grep -rln construir_motor_cableado tests` sin salida; `grep -rn "fuera del calendario\|sin calendario de cierres\|Los cierres de mercado" tests` sin salida; `cableado.py` (diff, `fuera = sorted(...)`) |
> | b2 | importa | **Modificar una pendiente dentro de la ventana se niega con un comportamiento fijo, y el encargo pide parámetro PROVISIONAL para lo que la regla no diga.** R15 solo dice «opening». El informe lo justifica («una pendiente que se mueve es una orden nueva»), pero P1(a) de §0.6 pregunta por colocar y no por modificar. `cierre_pendientes` solo gobierna la cancelación al empezar la ventana. | `broker.py` `modificar` (llamada a `_prohibido_por_cierre`, sin consulta a `cancelar_pendientes`); informe §0.5; `docs/validation/CIERRES-DE-MERCADO.md` §0.6 P1 |
> | b3 | menor | El predicado también niega mientras el cierre dura y fuera de `cubre` (`cierre_sin_calendario`). Son decisiones declaradas y razonadas, pero van más allá de R15 y no tienen parámetro. | informe §0.5 y §1; ADR-0068 §1 |
>
> ### Lo que no pude comprobar
> - Las fuentes web (Trading Updates, `ftmo.com/wp-json/ftmo/symbols`, la página de R15 releída, el «Close Early at 14:50» de UK100, el Viernes Santo sin cierre del Forex, el recuento de actualizaciones). No se versionan y no las descargué.
> - El texto literal del ticket VDW-DPMWR-965. No está en el repo, como el informe ya declara.
> - `make check`, que escribe: solo leí el log y su sello.
> - El comando `knowledge validate > knowledge-validate.log`, por escribir: lo ejecuté a stdout.
> - La medida de «con el predicado desactivado fallan 11 de 25». Exige editar el fuente; la tomo del informe.
> - Una cancelación por cierre a través de `MotorCableado` (hallazgos a3 y b1): sin test ni caso en el arnés.
> - Que la clasificación de los 41 días de construcción (abril a agosto de 2026) caiga dentro de `cubre`: la comparé por fechas del directorio, no con el cableado.
>
> ### Comandos ejecutados
> 1. `git branch --show-current; git merge-base main HEAD; git log --format='%h %s' main..HEAD; git diff --stat main...HEAD; git status --short; cat contrato.yaml; ls make-check.log docs/encargos/feature-cierres-de-mercado.md`
> 2. `uv run python scripts/contrato_rama.py`
> 3. `cat docs/encargos/feature-cierres-de-mercado.md; ls -la make-check.log knowledge-validate.log; grep -E "SELLO|PICO|passed|failed" make-check.log; git log -1 --format=%cd; git check-ignore make-check.log`
> 4. `uv run botsito state check; uv run botsito spec check`
> 5. `git rev-parse HEAD^{tree}; uv run botsito knowledge validate; cat docs/validation/CIERRES-DE-MERCADO.md`
> 6. `git log --format='%h%n%B----' main..HEAD -- knowledge/spec knowledge/cases; git diff --name-status main...HEAD | grep -vE "^M|^A"; git diff main...HEAD -- knowledge/spec/ambiguedades.yaml knowledge/spec/parametros.yaml knowledge/cuentas/ftmo-2step-swing-100k.yaml PROJECT_STATE.md`
> 7. `wc -c PROJECT_STATE.md; git diff main...HEAD -- docs/state/HISTORIA.md | grep '^-[^-]'; git diff main...HEAD -- docs/adr/README.md; head/grep de docs/adr/0068-*.md; cat knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`
> 8. `grep` de R7 y R15 en `FTMO-REGLAS.md`; `sed -n 90,125p`; `ls knowledge/evidence`; búsqueda del id `ev-v4-012524-0ef85a89`
> 9. `cat src/botsito/domain/cierres.py; git diff main...HEAD -- engine/broker.py engine/simulacion.py engine/perfil_cuenta.py`
> 10. `git diff main...HEAD -- engine/cableado.py; cat engine/calendario_cierres.py`
> 11. `grep` de `def`/`Posicion(` en `broker.py` y de `reglas_broker_de` / `ReglasBroker(` en src, scripts y tests
> 12. `sed` de `broker.py` 494-520 y 305-322; `grep` de `construir_motor_cableado`, `abrir_conocida` y `CANCELADA` en el motor; `ls knowledge/cuentas`
> 13. `sed -n 185,245p` y `262,330p` de `cableado.py`
> 14. `uv run pytest tests/unit/test_cierres_de_mercado.py -q -p no:cacheprovider`
> 15. `grep` de las pruebas y los `def test_` de `test_cierres_de_mercado.py`; lectura de sus primeras 125 líneas
> 16. `grep` de A-28 y `broker_dst` en la spec; lectura de ADR-0068 líneas 30-122
> 17. `ls knowledge/cases/dev` y recuento por mes; `git log -- contrato.yaml`; `git show 94b28ad`
> 18. `grep` de tests de `construir_motor_cableado`, `CableadoError`, «fuera del calendario»
> 19. `grep` de la `fuente` de `firma_mensajes_dia_max` y del perfil de cuenta

## Estado

**Rama lista para revisión, NO cerrada.** Fases 0, 1 y 2 hechas. `make check` sellado sobre el
árbol del último commit y revisor pasado, con su informe pegado y sus hallazgos atendidos (§4).
Quedan para el consultor:
- las tres preguntas a soporte de FTMO (§0.6, A-55), y P0, el texto literal del ticket;
- si la modificación de una pendiente lleva parámetro propio (b2);
- la orden de cierre.
