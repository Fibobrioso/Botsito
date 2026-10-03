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

- **del 4-12-2025 al 13-08-2026, las 35 de cada jueves**, más la del 10-09-2026 y la del 11-12-2025.
  **Solo nombran el Forex las de Navidad** (11-dic, 18-dic y 1-ene, la misma tabla). Semana Santa
  (2-abr-2026) cierra índices, metales y acciones, no el Forex;
- **del 20-08-2026 al 1-10-2026, las 7 que faltaban** (el primer barrido chocó con el límite de
  ritmo de FTMO, HTTP 429, y se repitieron con 45 s de pausa entre una y otra): **ninguna nombra el
  Forex.** La del 1-10 trae el festivo de Hong Kong (HK50.cash) y el cambio de hora de Australia;
- **la del 25-12-2025 no existe** (HTTP 404). Esa semana la cubren las tablas de Navidad.

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
  su huso. El servidor de FTMO es Nueva York + 7 todo el año (§0.2), así que «23:55 del servidor» se
  declara como «16:55 `America/New_York`», y `zoneinfo` pone el cambio de hora en su sitio.

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
  the window starts?»
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
| `src/botsito/engine/broker.py` | `ReglasBroker.cierres`. `_colocar` y `modificar` preguntan al predicado ANTES que al freno; lo negado es un `Rechazo` con su motivo, no se envía ni se cuenta. La cancelación al empezar la ventana es un evento más de `_proximo_evento`, que en el mismo instante va antes que cualquier llenado. `Traza.cierres` y el log (INFO) |
| `src/botsito/engine/simulacion.py` | `reglas_cierres_de(perfil, registro, calendario)`, y `reglas_broker_de(perfil, registro, calendario)` lo arma cuando llegan las dos cosas |
| `src/botsito/engine/perfil_cuenta.py` | El accesor `minutos`, que faltaba: la lectura es estricta por tipo (ADR-0002), y `entero` no lee unos `minutos` |
| `src/botsito/engine/cableado.py` | Carga el calendario del perfil (sin él, no corre) y se niega a correr un día fuera de `cubre`. `TrazaBroker.cierres`, y la sección «Los cierres de mercado (ADR-0068)» del informe del arnés |
| `knowledge/spec/parametros.yaml` y el perfil | `firma_gap_margen_minutos` = 120 y `firma_gap_cierre_minimo_minutos` = 120 (CONFIRMED, R15), en los dos con el mismo valor; `cierre_pendientes` = `cancelar` (DEFAULT_AMBIGUOUS, A-55), en el registro. La descripción de `firma_noticias_restringe` en el perfil decía que R15 «no se modela»: ahora dice que la mitad de los cierres sí |
| `knowledge/spec/ambiguedades.yaml`, `PROJECT_STATE.md` | **A-55**, abierta, clase `medicion`, no bloqueante, con su fila en «Known Ambiguities» |
| `docs/spec/` | Regenerado con `botsito spec docs --escribir` |
| `docs/adr/0068-…md` y `docs/adr/README.md` | ADR-0068 y su fila en el índice |

**Lo que NO se ha tocado:** `mql5/` (el EA y `SymbolInfoSessionTrade`). El adaptador real de
MetaTrader todavía no existe en Python, y su unión con el calendario está escrita en ADR-0068 §4 y
probada con sesiones sintéticas. Como no se toca nada que dependa de la plataforma, no hace falta la
CI de Linux por `fix/`. `abrir_conocida` tampoco pasa por el predicado, porque no la emite el bot.

## 2. Fase 2 · Tests, rompiendo la guardia a propósito

`tests/unit/test_cierres_de_mercado.py`: 22 funciones, 25 casos. Los cinco que pide el encargo:

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

**La guardia rota, medido.** Con `return None` en la primera línea útil de
`ventana_prohibida_por_cierre`, restaurado justo después (el fichero no lleva la marca):

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
```

Fallan 11 de 25. Pasan los que esperan que NO se prohíba nada (día normal, corte diario, la
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

## Estado

EN CURSO: Fases 0, 1 y 2 hechas; falta el arnés, el sello y el revisor.
