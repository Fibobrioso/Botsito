# F17-HISTORIAL · El historial de ticks del servidor de la demo de FTMO, con sus herramientas y sin correr, y el ajuste por cuenta de F17 (R4.7, entrada F)

> Informe de la rama. La fase 0 y su PARADA (§0 a §5 de la fase 0), lo hecho tras las respuestas
> (§3 y §4), las líneas del cierre (§5), la fila de ERRORES (§6), el encargo punto por punto (§7),
> la CI (§8), el revisor y lo hecho con sus hallazgos (§9), las desviaciones (§10), la PARADA 3
> (§11) y lo que decide la orden de cierre (§12).

Rama `trabajo/f17-historial`, abierta el 2026-11-25 desde `main` en 2dc4f7dd (commit de estado
sobre el merge 96b250fd del tag `stable/F39o-contraste-trader`). Encargo:
`docs/encargos/trabajo-f17-historial.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la A.5 se
cita en el informe; la F de la Next Action). Tag previsto: `stable/F39p-f17-historial` (no existe ni
en local ni en origin: `git tag -l "stable/F39p*"` y `git ls-remote --tags origin "stable/F39p*"`,
0 líneas).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main` (tras `git fetch origin`):
  `2dc4f7dd55b9c8bcffe7902486851c73ef81ea19` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39o-contraste-trader^{commit}"` = `git rev-parse main^1` =
  `96b250fd15297b443ec3d5e51771b84669ced7b0`; en origin, `98d6df47…` (el objeto del tag anotado) y
  `96b250fd…` (`^{}`). Es el último `- Tag: ` de HISTORIA y el último `stable/*` de origin.
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal da el check `python`
  (139666601005) en `completed` / `success`; es el run 45747377112 del cierre de F39o.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`, y
  `git ls-remote --heads origin "fix/*"` sale vacío.
- Sesión en Opus 5.5, esfuerzo alto (`/model` y `/effort`).

## 0. Fase 0

Sin escribir código. Lo leído, en las dos filas de HOLDOUT del 2026-11-25 de esta rama (y la del
2026-11-26 para lo que pase de la medianoche).

### 0.1 La fila de HOLDOUT del día

Escrita y estadiada antes del primer `make check` (commit `fdc18717`), con lo único que el
proyecto ha visto del historial de ticks de FTMO: el recuento de un día de un mes hoy reservado que
contó el EA **en el Strategy Tester** (`EA-CONEXION.md`:141-145), sin ningún precio. El auditor
señala (afirmación 8) que esas líneas traen también la hora del primer y del último tick y que «el
historial de velas M1 empieza» a principios de 2025 según el log del tester (:144): lo segundo es
justo la profundidad que mide D1. Va declarado en la fila 2 del día, antes de fijar D3.

### 0.2 Lo leído, con fichero:línea

**El modelo del exportador, `tools/mql5/MedirDemoFTMO.mq5`.**
- `Comprobaciones` (:757-791): la condición DEMO literal en :759,
  `if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)`;
  después exige el símbolo (:764), el trading algorítmico activado (:769), `SYMBOL_TRADE_MODE_FULL`
  (:774) y una cotización de menos de 2 minutos (:785). Un exportador de solo lectura no necesita
  las tres últimas, y con ellas se negaría en fin de semana (auditor, 9).
- El CSV: `FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI)` (:1522) en `MQL5/Files` con nombre
  `MedirDemoFTMO_<hora del servidor>.csv` (:1521); filas con `\r\n` y `FileFlush` (:126-127).
- El reloj, `MedirReloj` (:386-399): `TimeCurrent`, `TimeTradeServer`, `TimeGMT` (que «sale del
  reloj del ordenador», :393), `TimeLocal`, el desfase servidor−GMT en minutos, el desfase local y
  el horario de verano local. ADR-0090 §1 valida `TimeGMT` con esas filas (:59-65).
- `tests/contract/test_medir_demo_ftmo.py`: niega por defecto toda función que llama a `OrderSend`
  con una acción que no sea de una lista cerrada (:5, :36-38, :69-88) y fija la condición DEMO en la
  759 (:30-32, :139). `tests/contract/test_capa_mt5.py` es más estricto: la capa no llama a ninguna
  de las 33 funciones de `FUNCIONES_DE_TRADING` (:42-76; `llamadas_de_trading`, sobre el código sin
  comentarios ni textos, :259-262; test :576). **Para el exportador vale el de la capa**: ninguna
  función de trading.

**El lector modelo, `scripts/leer_demo_ftmo.py`** (617 líneas; test, 563): `COLUMNAS` cerradas
(:33-52), `LecturaError` (:80), lee por patrón de nombre (`PATRON`, :53) y marca, nunca oculta, lo
inesperado (:5-8). Uso: `uv run python scripts/leer_demo_ftmo.py <csv o carpeta>... [--salida]`.

**`docs/runbooks/DEMO-FTMO.md`**: «Lo que hace, y lo que no hace nunca» (:15), «Una vez: la cuenta
y MetaTrader» (:47), «Cada vez: ejecutarlo» (:65), «Dónde queda el fichero y a dónde va» (:86),
«Cuándo» (:105). Es la forma del runbook de D4.

**`data/manifests/README.md`**: el esquema `schema_demo_ftmo: 1` (:56-75): `dataset_id`
`demo-ftmo-<fecha>-<8 hex>`, `ejecucion`, `fichero` (ruta, bytes, sha256, filas, `fin_de_linea`),
`script` (ruta, versión, sha256, commit), `cuenta`, horas, y quién y cuándo lo congeló; «se escribe
a mano con `sha256sum` y el lector delante» (:61-62). Todo `.yaml` bajo `data/manifests/` es
INMUTABLE por el hook (:59-60). Los ticks de Dukascopy de construcción tienen sus manifiestos en
`data/manifests/ticks/` para los cuatro meses (enero, abril, julio y agosto de 2026).

**`scripts/ticks_spread.py`**: la hora de cada tick sale de `reloj_de_las_sesiones` (la rejilla H4;
:11-16, :111), la ventana de `ventana_inicio` a `ventana_fin` (:112-113, horas nominales 07-15 del
registro), percentil por rango más cercano (`percentil`, `resumen`, :42-59), `clave_de_hora` por
minuto (:69-83). Recorre solo `construccion` y exige sus ticks (:102-110).
**`scripts/ticks_integridad.py`**: `TOLERANCIA_PUNTOS = 2` «fijada antes de comparar» (:27, :3-9),
`reconstruir_m1` (primer, máximo, mínimo y último BID del minuto, :38-47) y `comparar` (cuadra si
los cuatro |Δ| ≤ 2; cuenta también `solo_repo` y `solo_ticks`, :50-75).

**`engine/arnes.py`, `dias_de_mercado`** (:184-226): **no enumera los días de mercado de un mes.**
Recibe `dias: Sequence[DiaTrader]` (los días del trader, :189) y les carga la M1 de Dukascopy del mes
y del ANTERIOR (:206-211) para calentar el sesgo, agregada a H4, M15 y M1. Ver §5, decisión 0.

**El reloj del servidor** (`parametros.yaml`): `broker_offset_base` = 120, CONFIRMED, ADR-0090
(:140-159), y `broker_dst` = `us`, CONFIRMED (:160-183); los dos con `consumido_por: [F17, F24,
F33]`. A-28 DECIDIDA (ADR-0090 §1, :44-58: solo «120, `us`» casa con las tres ejecuciones).
**Ningún código de `src/` ni de `scripts/` pasa hoy un instante del servidor a UTC**: los dos
parámetros solo los lee `mql5bridge/generar_capa.py` (:67-68) para la capa. ADR-0069 §2 (:39-67)
manda «instantes UTC desde la rejilla, con zoneinfo, nunca un desfase fijo». La NOTA del 2026-10-13
está en ADR-0069 **§5** (:128-132), no en §1-§2 (auditor, 14): `ticks_spread.py` lee la ventana por
la puerta de `engine/relojes.py`.

**`mql5bridge/compilar.py`** (363 líneas; test, 206): `exportar` copia del ÍNDICE de git solo
`mql5/` (:95-111) a un temporal; `compilar_uno` llama a MetaEditor con `/compile`, `/include` y
`/log` (:124-155); la puerta es `Result: 0 errors` y el `.ex5`, no el código de salida (:76-79);
`instalar` copia el `.ex5` a `MQL5/Experts/Botsito/` o `MQL5/Scripts/Botsito/` según
`Path(fuente).parts[1]` (:174-184), que para `tools/mql5/X.mq5` daría `mql5`. `.gitignore` no
ignora `*.ex5`: hoy no hace falta porque se compila en un temporal (auditor, 41).

**ADR-0092** §4 (:99-115): la mediana a cada llenado afectado, b)-e) sobre la curva recompuesta, y
el percentil 90 con esperanza > 0; §8 (:218-228): una cuenta por mes en construcción, arrastrada en
los meses no vistos; su NOTA (:230-246): la medida sobre los meses no vistos, arrastrada, «no existe
todavía: su rama dirá, con su ADR, cómo se arrastra allí».

**ADR-0099 §5** (:152-179): el historial «antes que nada», medido con un criterio escrito antes
«(huecos dentro de la ventana, minutos sin ticks y coherencia con su propio M1; un recuento por día
no basta, porque el tester genera ticks donde faltan)»; si cubre, el spread de FTMO sale de ahí;
usarlo como fuente pide un ADR que enmiende ADR-0005 y ADR-0024 §4; y la fila `spread_menos_1` o
`spread_menos_2` del puente se elige por «la diferencia mediana medida entre los dos spreads en las
horas de la ventana». Lo medido el 2026-10-19 fue **en el Strategy Tester**; D1 elige el terminal
(auditor, 16).

**`criterio_fidelidad.py`**:
- `CuentaDelTramo` (:678-684): «una cuenta mensual», `mes: str`, `curva`, `suspendida`;
- `medir_por_cuentas` (:696-721): d) y e) de cada cuenta contra el capital inicial, la peor con su
  mes, y f) los meses suspendidos; la llama `engine/cableado.py`:1561 (protegido);
- `medir_rentabilidad` (:745-769): una sola curva y un solo `suspendida`;
- `curva_con_deslizamiento` (:842-866): suma el ajuste al día de cada cierre y **arrastra `previo`
  por toda la curva que recibe**;
- `veredicto_con_f17` (:885-921): una curva, un `suspendida`, `medir_rentabilidad`; nunca
  `medir_por_cuentas`;
- las dos últimas no tienen llamadores fuera de los tests (`test_metodo_adr0092.py`:295-304 y
  :315-342). Es la deuda de `CUENTA-POR-MES.md`:118-120 y de `PROJECT_STATE.md`:100.

**MASTER_PLAN.md:258**: la fila «… escritura atómica en el grabador de demo; desfase servidor-UTC
registrado» de F15, F16 y F17.

**La documentación de MQL5** (subagente `web-fetch`, cuatro páginas oficiales):
- `CopyTicksRange(simbolo, ticks[], flags=COPY_TICKS_ALL, from_msc, to_msc)`, con los dos límites
  incluidos («Ticks with the time >= from_msc are sent», «<= to_msc»); `COPY_TICKS_INFO` da los
  ticks «with Bid and/or Ask changes» (`docs/series/copyticksrange`);
- `time_msc`, «Time of a price last update in milliseconds»; **ninguna de las páginas dice en qué
  reloj** (`constants/structures/mqltick`);
- la primera llamada «initiates synchronization of the symbol's tick database stored on the hard
  disk. If the local database does not provide all the requested ticks, then missing ticks will be
  automatically downloaded from the trade server», y en scripts «can wait for the result for 45
  seconds»; `ERR_HISTORY_TIMEOUT`, «the function has sent all it had» (`docs/series/copyticks`);
- **ninguna dice si los ticks son los guardados o generados, ni hasta dónde llega la base**;
- `CopyRates` por rango de fechas devuelve «only data from this interval», descarga del servidor
  si falta y no dice en qué reloj van las barras ni si son BID (`docs/series/copyrates`).

Lo que no está en la documentación queda **por medir en la corrida** (ADR-0082 D7): el reloj de
`time_msc` y de las barras (se compara con el control de D1), si la M1 es BID (se ve en el
punto (c)), si los ticks son guardados, y cuántos devuelve `CopyTicksRange` en una llamada (la
documentación no da un tope; un día a medias queda en `dia_*_ticks` y `dia_*_error` del control, y
el lector lo dice: añadido tras el revisor, b5).

### 0.3 El auditor (subagente `auditor-encargo`)

50 afirmaciones: 31 correctas, 2 incorrectas y 17 con matiz; 11 herencias. Lo que cambia algo,
abajo y en §5. El informe entero va al final («Informe del auditor»).

- **Incorrecta, D3:** `arnes.dias_de_mercado` no da los días de mercado de un mes (lo de arriba), y
  además lee la M1 de marzo y de junio para calentar (H1). Si se cambia por «todos los laborables»,
  el servidor de FTMO cierra el 1 de enero de 2026 (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`:44-48)
  y enero fallaría (b) con los datos bien (H2).
- **Incorrecta, D7:** ADR-0090 §7 se titula «El deslizamiento: observaciones, no un modelo»
  (:231-237): lo que «mide el grabador de spread y ticks de F17» es el deslizamiento, no el spread.
  ADR-0099 §5 se lo da a la medida de las órdenes stop (:168-172), que es de la segunda rama.
- **Matiz grave, D3 (c):** unos ticks fabricados a partir de la M1 cuadran con ella por
  construcción y llenan todos sus minutos: ni (a) ni (c) distinguen ticks guardados de generados,
  que es la cautela de ADR-0099 §5 (:161-163).
- **Matiz, D1:** «el primer tick disponible del símbolo» choca con «cualquier otro mes, se niega sin
  pedir nada»: saber hasta dónde llegan obliga a preguntar por fechas de otros meses, y la primera
  llamada puede descargar ticks del servidor a la base del terminal (documentación de arriba), que
  con febrero toca el heredado 6.
- **Matiz, D5:** `CuentaDelTramo` es mensual (`mes: str`) y la arrastrada de los meses no vistos no
  existe en el motor (NOTA de ADR-0092 §8); cambiar la clase rompe
  `tests/unit/test_cuenta_por_mes_metodo.py` y `engine/cableado.py`, protegido (H11).
- **Matiz, D2/D3:** la tolerancia de 2 puntos quedaría en dos sitios (afirmación 30); y «la diferencia
  mediana» no dice si es la diferencia de las medianas o la mediana de las diferencias por hora (31).
- **H5, D6:** el `compilar.py` cambiado lo negará la guardia (solo un guion idéntico al de `main`
  está exento): la compilación la lanza Aleks con «!».
- **Otras herencias:** H3 (`docs/runbooks/README.md` lista cada runbook, y no está en el contrato),
  H4 (el índice de ADR anota los recuadros, y `docs/adr/README.md` está protegido), H6 (V02 de la
  auditoría «cazador»: las aperturas H4 del servidor, R6a.8), H7 (`cuenta_pruebas`, «F17 mide el
  reloj del servidor contra este terminal», `parametros.yaml`:1817-1832), H8 (MASTER_PLAN:299 prevé
  un esquema v2 `mt5_demo`), H9 (el ADR de ADR-0099 §7, hacia el 2026-12-03), H10 (CRLF y ANSI en los
  CSV de MQL5; la CI no tiene `data/`).

## 1. El diseño (D1, D2, D4, D5 y D6), para la PARADA

### 1.1 El exportador, `tools/mql5/ExportarTicksFTMO.mq5` (D1)

Un `#property script_show_inputs`, versión `1.0`, sin ninguna función de `FUNCIONES_DE_TRADING`
ni `CTrade` ni `#include <Trade\...>`.
- **Entradas:** `InpDesde` e `InpHasta` (fechas del servidor, `AAAA.MM.DD`). Antes de pedir nada,
  recorre los días del rango y, si UNO solo cae fuera de `MESES_CONSTRUCCION`
  (`{"2026-01","2026-04","2026-07","2026-08"}`, la lista de `criterio_fidelidad.yaml`:47, fijada
  por un test), sale con un `Alert` sin llamar a ninguna función de series.
- **La negativa:** la condición DEMO de `MedirDemoFTMO.mq5`:759, literal, y `SymbolSelect("EURUSD")`;
  sin exigir trading algorítmico ni mercado abierto.
- **Por día** (de las 00:00 a las 23:59:59.999 del servidor): `CopyTicksRange` con
  `COPY_TICKS_ALL` en un array dinámico, hasta 3 intentos con `Sleep` si `GetLastError()` no es 0
  (el patrón del ejemplo de `CopyTicks`), y `CopyRates` de M1 del mismo día. Escribe en
  `MQL5/Files/F17/`:
  - `F17_<AAAA-MM-DD>_ticks.csv`: `time_msc,bid,ask,flags` (bid y ask con `SYMBOL_DIGITS`);
  - `F17_<AAAA-MM-DD>_m1.csv`: `time,open,high,low,close,tick_volume,spread,real_volume`;
- **El control**, `F17_control_<hora del servidor>.csv`, `clave,valor,nota`: versión, cuenta DEMO,
  servidor, empresa, build; `time_trade_server`, `time_current`, `time_gmt`, `time_local`, el
  desfase servidor−GMT en minutos, el desfase y el horario de verano locales (los de
  `MedirReloj`, para validar `TimeGMT` como ADR-0090 §1); y por día: ticks, M1, último error,
  intentos, primer y último `time_msc`. Y la profundidad, según la decisión 1 de §5.
- **Lo que da por supuesto de MT5**, citado o por medir: los límites del rango y el flag, citados;
  el reloj de `time_msc` y de las barras, la M1 BID y si los ticks son guardados, por medir.

### 1.2 El lector, `scripts/leer_historial_f17.py` (D2)

`uv run python scripts/leer_historial_f17.py <carpeta> --salida <fichero>`.
- **Se niega** a un mes que no sea de `construccion`: decide por el NOMBRE de cada CSV antes de
  abrirlo, y sale con 2 nombrando el fichero.
- **Del servidor a UTC:** `servidor = UTC + broker_offset_base + horario de verano`, donde el horario
  de verano es el `dst()` de zoneinfo del huso del calendario de `broker_dst` (una tabla de nombres:
  `us` → `America/New_York`, `eu` → `Europe/London`, `ninguno` → sin horario de verano), sin ninguna
  cifra en el código. La inversa prueba los dos candidatos y, si el instante cae en la hora ambigua
  o inexistente de un cambio (domingos, con el mercado cerrado), falla nombrándolo. Tests: a los dos
  lados del cambio de EE. UU. (marzo y noviembre) y del de Europa (marzo y octubre), con `us` y con
  `eu`, y el instante ambiguo que falla.
- **El control:** compara el desfase servidor−GMT del CSV con el que da el registro en ese instante,
  y dice si cuadra.
- **Por mes, los puntos de D3**, con los minutos de la ventana por `reloj_de_las_sesiones` (como
  `ticks_spread.py`), los días de la decisión 0 y las cifras del yaml de D3; y el veredicto «cubre»
  o «no cubre».
- **Solo para los meses que cubren:** el spread de FTMO por hora de la ventana (`resumen` de
  `ticks_spread.py`) y el de Dukascopy de los mismos minutos (sus ticks de construcción), y la
  diferencia mediana de la decisión 3. Recuentos, puntos y percentiles; ningún precio.
- Acepta CRLF y ANSI (H10).

### 1.3 El manifiesto, `data/manifests/f17/` (D4)

`schema_f17_historial: 1`, uno por mes exportado, escrito a mano como el de la demo:
`dataset_id` `f17-historial-<AAAA-MM>-<8 hex>` (sha256 de los sha256 de sus ficheros), `mes`,
`ficheros[]` (`ruta` relativa a `data/`, `tipo` ticks, m1 o control, `bytes`, `sha256`, `filas`,
`fin_de_linea`), `dias` (pedidos, con ticks, sin ticks), `primer_tick` (lo que dé la decisión 1),
`control` (las horas y el desfase del CSV de control y si cuadra con el registro), `script` (ruta,
versión, sha256 y commit), `cuenta`, y `declarado_por`, `congelado_el`, `rama`, `informe`. Un
validador en el lector y su test con un manifiesto sintético en un temporal. Va aparte de
`demo_ftmo/` porque `test_manifiestos_demo_ftmo.py` exige exactamente las ejecuciones 1, 2 y 3, y del
esquema v2 `mt5_demo` de MASTER_PLAN:299, que no existe en `src/` (H8). El runbook,
`docs/runbooks/F17-HISTORIAL.md`, con la forma de `DEMO-FTMO.md`.

### 1.4 El arreglo por cuenta (D5)

- `veredicto_con_f17(posiciones, dias, cuentas, capital, base, criterio, *, mediana,
  percentil_f17)`: recibe las `CuentaDelTramo` de la corrida en lugar de una curva y un
  `suspendida`.
- Cada cuenta recompone su curva con `curva_con_deslizamiento` solo con las posiciones de sus días,
  que no cambia: sigue siendo la recomposición dentro de UNA cuenta, y por eso dentro de una cuenta
  arrastrada de varios meses el ajuste sí se arrastra.
- b) y c) salen de todas las posiciones con la mediana; d), e) y f), de `medir_por_cuentas` sobre
  las cuentas recompuestas, como hace hoy `cableado.py` con la medida sin F17.
- **`CuentaDelTramo` no cambia:** su `mes` es una etiqueta (para la arrastrada, el tramo, p. ej.
  `2025-06..2025-11`), y así ni `cableado.py` ni `test_cuenta_por_mes_metodo.py` se tocan (H11).
- **Tests:** dos cuentas, donde el ajuste de la primera no baja el saldo al corte de la segunda; una
  cuenta de varios meses, donde sí se arrastra; f) nombra la cuenta suspendida; una posición de un
  día que no está en ninguna cuenta falla con nombre.
- Los dos tests de hoy se adaptan: el de `curva_con_deslizamiento` no cambia, y el de
  `veredicto_con_f17` pasa su curva como una sola cuenta, con las mismas cuatro aserciones.
- **Que rompa en `main`:** el test nuevo rompe por la firma. Uno de contenido con la firma de hoy no
  es posible: con una sola curva no hay cuentas que separar, y `curva_con_deslizamiento` no cambia.
  Se dice así y se prueba la firma en un clon de `main`.

### 1.5 La compilación (D6)

- Un camino aparte en `compilar.py`, `--herramienta tools/mql5/<X>.mq5`: exporta del índice SOLO ese
  fichero (rechaza otra ruta), compila con `/include` a la `mql5/` exportada e instala en
  `MQL5/Scripts/Botsito/`.
- El camino de la capa no cambia: sus tests siguen igual, y uno nuevo comprueba que `exportar` sigue
  copiando solo `mql5/`.
- Tests en los dos sentidos: una ruta fuera de `tools/mql5/` se rechaza, y un Experts o un Scripts
  de la capa sigue instalándose donde iba.
- **Lo lanza Aleks con «!»** (H5): la sesión da el comando exacto; los dos logs, el de
  `ExportarTicksFTMO` y el de control de `MedirDemoFTMO`, van a `docs/validation/anexos/F17-HISTORIAL/`.
- `*.ex5` entra en `.gitignore`. Esa ruta no está en el contrato; se pide en la decisión 7.

## 2. El borrador del yaml de D3

Se escribe tras la respuesta, porque tres de sus campos dependen de las decisiones 0, 2 y 3. Su forma:

```yaml
version: 1
fuente: ADR-0099 §5   # el criterio se escribe antes de ver un tick de FTMO
meses: construccion de knowledge/cases/criterio_fidelidad.yaml   # un test compara la lista
ventana: ventana_inicio a ventana_fin por reloj_de_las_sesiones (rejilla H4)
dias: <decisión 0>
cubre_si:
  a_minutos_con_tick_min: "0.99"
  b_huecos: {umbral_min: 5, max_huecos_mes: 3, hueco_max_min: 30}
  c_m1_propia: {tolerancia_puntos: 2, fraccion_min: "0.99", denominador: M1 del servidor con ticks}
  d_no_fabricados: <decisión 2>
diferencia_spread: <decisión 3>
no_autoriza: usar los ticks como fuente de una medida pide un ADR que enmiende ADR-0005 y ADR-0024 §4
```

La tolerancia de 2 vive en el yaml para este criterio, y un test comprueba que coincide con
`TOLERANCIA_PUNTOS` de `ticks_integridad.py` (auditor, 30). El test del sha256, como
`test_premisa_costes.py`:151-153 y :182-189.

## 5 de la fase 0. PARADA

## Lo que necesito que decidas

0. **Los días de D3** (`arnes.dias_de_mercado` no los da). Opciones: (a) los laborables de cada mes
   de construcción menos los cierres del calendario de FTMO (`knowledge/cuentas/cierres/`, que cubre
   los cuatro meses), contando solo los minutos de la ventana en que el servidor está abierto; (b) los
   días con M1 de Dukascopy en la ventana; (c) los días `dev` del trader. Recomiendo (a): es lo que el
   servidor de FTMO debería tener, sin leer la M1 de marzo ni de junio (H1) y sin hundir enero por el 1
   de enero (H2). Coste de (b): ata FTMO a los huecos de Dukascopy. Coste de (c): lee casos, y julio y
   enero quedarían a medias.
1. **La profundidad, sin pedir otros meses** (D1 se contradice). Opciones: (a) el primer tick de cada
   mes de construcción, pedido dentro del mes, y la fecha de la primera M1 del servidor por
   `SeriesInfoInteger` (`SERIES_SERVER_FIRSTDATE`), que es un dato de la serie y no pide ticks (se cita
   de la documentación antes de escribirlo); (b) `CopyTicks` desde el principio con un solo tick, que
   puede sincronizar y descargar la base del terminal desde el principio, febrero incluido. Recomiendo
   (a): respeta el heredado 6. Coste de (a): no sabremos si hay ticks antes de enero de 2026.
2. **Un discriminador de ticks fabricados, fijado antes** (auditor, 34). Opciones: (a) añadir a D3 un
   punto (d): al menos el 90 % de los minutos de la ventana con ticks tienen más de cuatro ticks o más
   de cuatro precios BID distintos, y la mediana de ticks por minuto de FTMO es al menos la mitad de la
   de Dukascopy en los mismos minutos; (b) sin punto (d), y que el informe de la corrida diga que (a) y
   (c) no lo distinguen; (c) otro que diga el consultor. Recomiendo (a): unos ticks hechos de la M1 son
   como mucho cuatro por minuto. Coste de (a): las dos cifras son un juicio, fijado antes de ver datos y
   sin medida que lo respalde.
3. **La diferencia mediana de los spreads** (ADR-0099 §5). Opciones: (a) la mediana del spread de
   Dukascopy menos la de FTMO, sobre todos los ticks de la ventana de los meses que cubren (positiva si
   FTMO es más barato); (b) la mediana de las ocho diferencias por hora. Recomiendo (a): es la lectura
   literal de «la diferencia mediana medida entre los dos spreads en las horas de la ventana», y no
   pesa igual una hora con pocos ticks. Coste de (b): más sensible a una hora rara.
4. **El recuadro de D7.** ADR-0090 §7 atribuye al grabador el DESLIZAMIENTO, no el spread. Opciones:
   (a) el recuadro dice que ese deslizamiento lo mide la medida de las órdenes stop de ADR-0099 §5 (la
   segunda rama), y que el spread de FTMO saldrá del historial si cubre o, si no, del grabador; (b) sin
   recuadro en esta rama. Recomiendo (a). Coste de (b): ADR-0090 §7 sigue diciendo algo que ADR-0099 §5
   descartó.
5. **D5 sin cambiar `CuentaDelTramo`** (§1.4). Opciones: (a) la clase no cambia y `mes` es una
   etiqueta; (b) un campo nuevo para el tramo, que obliga a tocar `cableado.py` (protegido) y
   `test_cuenta_por_mes_metodo.py`. Recomiendo (a). Coste de (a): `mes` dice «2025-06..2025-11» en una
   cuenta arrastrada, y la docstring «una cuenta mensual» se precisa.
6. **V02, las aperturas H4 del servidor** (auditor, H6). Opciones: (a) fuera de esta rama, porque la M1
   del servidor que exporta D1 ya permite derivar la rejilla y eso es de R6a.8; (b) que el lector las
   saque ya. Recomiendo (a). Coste de (a): nada, la M1 queda exportada y congelada.
7. **Rutas que el contrato no tiene:** `.gitignore` (`*.ex5`, D6), `docs/runbooks/README.md` (el
   índice, H3) y `docs/adr/README.md` (el recuadro en el índice, H4, hoy protegido). Opciones: (a)
   entran las tres en un commit del contrato que lo declara; (b) solo las dos primeras. Recomiendo (a),
   si D7 sigue.

Lo que cuadra con D1-D8 y no depende de estas respuestas lo empiezo mientras espero (encargo, §4): el
paso del reloj a UTC del lector con sus tests, el contrato del exportador sobre un `.mq5` sin días, el
validador del manifiesto y D5 con la decisión 5 en (a).

**Espero tu respuesta a la PARADA.**

## Respuesta del consultor a la PARADA (2026-11-26), tal cual

Copiada también al final del encargo. Llegó con el reloj de la máquina en las 23:50 del
2026-11-25; la respuesta lleva las 00:15 del 26.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA de `trabajo/f17-historial` (2026-11-26, 00:15, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA. Lo que cuadre con lo medido, adelante sin esperar; si algo de lo medido contradice esta respuesta, PARA solo en eso.
>
> Veredicto: la fase 0 cumple y corrige al encargo en tres puntos que acepto. Errores del consultor, para la fila de ERRORES: (1) D3 (c) decía que detectaba ticks fabricados, y no puede, porque cuadran con la M1 por construcción; (2) D7 atribuía a ADR-0090 §7 el spread, y lo que atribuye al grabador es el deslizamiento; (3) D1 pedía «el primer tick disponible», que obliga a preguntar por meses fuera de construcción; (4) D3 tomó `arnes.dias_de_mercado` de una auditoría sin comprobar qué devuelve.
>
> D1, el exportador: no exige trading algorítmico ni mercado abierto (no opera), y aplicas el test más estricto de la capa (ninguna función de trading). De acuerdo.
>
> 0. Los días de D3: de acuerdo. Son los laborables (lunes a viernes) de cada mes de construcción menos los días con algún cierre del calendario de cierres de FTMO (ADR-0068) que toque la ventana. Si el calendario del repo no cubre algún día de enero, abril, julio o agosto de 2026, PARA y dilo; no lo completes de fuera. Nada lee la M1 de marzo ni de junio.
>
> 1. La profundidad: de acuerdo. El primer tick de cada mes pedido, buscado dentro de ese mismo mes, y la primera M1 del servidor por `SeriesInfoInteger`, como metadato. Ningún tick fuera de construcción. D1 se corrige así en el informe.
>
> 2. El discriminador (d), fijado ahora y antes de ver un tick de FTMO. Un mes CUBRE solo si además, en la ventana de sus días (punto 0): (d1) en al menos el 95 % de las horas día-hora, el spread (ASK − BID) toma al menos 3 valores distintos; y (d2) la mediana de ticks por minuto es al menos la mitad de la de los ticks de Dukascopy del mismo mes en la misma ventana. El yaml lo dice tal cual: es una heurística pre-registrada, no una prueba de que los ticks sean guardados (ADR-0082 D7). Control en esta rama: corres (d1) sobre los ticks de Dukascopy de los meses de construcción que ya están en `data/` (los que lee `ticks_spread.py`), y tienen que pasarlo todos (el (d2) de Dukascopy contra sí mismo es trivial y no se corre). Declara esa lectura en HOLDOUT el mismo día, solo con recuentos. Si algún mes de Dukascopy no pasa (d1), PARA: no cambies la cifra.
>
> 3. La diferencia de spreads: la del texto de ADR-0099 §5, «la diferencia mediana»: por cada par día-hora de la ventana con ticks de las dos fuentes, la mediana del spread de FTMO menos la mediana del de Dukascopy, y la mediana de esas diferencias. Es la que se compara con las filas `spread_menos_1` y `spread_menos_2` del puente. La diferencia de las dos medianas globales sale al lado, como dato y sin uso. Va al yaml.
>
> 4. El recuadro de D7: de acuerdo con tu texto. Por ADR-0099 §5, el deslizamiento lo mide la medida de las órdenes stop (segunda rama de F17), y el spread sale del historial, si cubre, o del grabador.
>
> 5. D5: de acuerdo con no tocar `CuentaDelTramo` ni `cableado.py`, con una condición: `curva_con_deslizamiento` y `veredicto_con_f17` agrupan por la etiqueta de cuenta que reciben y nunca la derivan de la fecha. Tests: dos cuentas con etiquetas distintas (el ajuste de una no baja el saldo al corte de la otra) y una sola etiqueta que abarca días de varios meses (el ajuste sí se arrastra dentro de ella), aunque la cuenta arrastrada de ADR-0092 §5 todavía no la construya el motor. Que rompe en `main` por la firma, dicho así. El informe dice que el constructor de la cuenta arrastrada falta y es de la rama que mida §5.
>
> 6. V02, las aperturas H4 del servidor: fuera de esta rama, de acuerdo. Una línea para R6a.8 en las propuestas del cierre.
>
> 7. El contrato gana `docs/runbooks/README.md`, `docs/adr/README.md` y `.gitignore`, este solo con una línea concreta para el `.ex5` de `tools/mql5` (nada más amplio), y comprueba que `test_no_unexpected_ignored_paths` sigue verde.
>
> D6, la compilación: cuando `compilar.py` y `ExportarTicksFTMO.mq5` estén escritos y sellados, pon en el informe su diff (el `--stat` y las funciones nuevas de `compilar.py` enteras) y PARA. El consultor lo revisa y entonces Aleks lanza la compilación con «!» con el comando exacto que le des. Los logs, a los anexos.
>
> Lo demás de D3 queda como en el encargo: (a) 99 % de los minutos con ticks; (b) como mucho 3 huecos de más de 5 minutos al mes y ninguno de más de 30; (c) 99 % de M1 cuadran a ≤ 2 puntos, ahora descrito como coherencia y no como detector. Escribe el yaml con 0 a 3 y fíjalo por su sha256 antes de cualquier otra cosa que lea ticks.

**Lo medido frente a la respuesta, antes de aplicarla:** el calendario de cierres del repo
(`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`) cubre del 2025-12-04 al 2026-10-07
(`cubre`, :21-22): los cuatro meses enteros. Sus cierres que tocan una ventana de un laborable de
esos meses: el del 1 de enero de 2026 (:44-48); el diario (16:55-17:05 de Nueva York, :31-33) cae
fuera de la ventana, y el del 8 de marzo es domingo. Punto 0, sin PARADA.

## 3. Lo hecho tras la respuesta

### 3.1 El criterio de D3, lo primero (`3ce320e6`)

`docs/plan/F17-HISTORIAL.yaml`, con los puntos 0 a 3 de la respuesta y (a), (b) y (c) del encargo,
fijado por su sha256 (`51a8ada2…`) en `tests/unit/test_f17_historial_criterio.py` (7 tests): el sha,
LF, las cifras, que la tolerancia de (c) es `TOLERANCIA_PUNTOS` de `ticks_integridad.py`, que el
calendario de cierres cubre los cuatro meses de construcción, que las filas `spread_menos_1` y
`spread_menos_2` existen en las piezas de `PUENTE-TECHO.yaml`, y uno que rompe a propósito (d1 a
0,90). Commiteado antes de leer ningún tick, de FTMO o de Dukascopy.

### 3.2 El lector, `scripts/leer_historial_f17.py` (D2), con el manifiesto (D4)

Como el diseño de §1.2, con dos cambios. (1) **Los días** son los del punto 0, por
`dias_del_mes`: los laborables menos los que tienen un cierre del calendario de FTMO que toca su
ventana; un día fuera del calendario para. (2) **El reloj, inverso**: la primera versión solo
probaba dos horarios de verano y no veía la hora repetida del 1-nov (los dos sondeos daban 0); ahora
sondea el de la víspera, el del día y el del siguiente, y el test lo comprueba. Valida además el
manifiesto (`validar_manifiesto`, esquema en `data/manifests/README.md`).
`tests/unit/test_leer_historial_f17.py`, 20 tests sintéticos:
- el reloj a los dos lados de cada cambio, con `us`, `eu` y `ninguno`;
- la hora repetida y la que no existe, que fallan con nombre;
- un calendario desconocido;
- que el guion no lleva 120 ni 180;
- el control;
- la negativa por nombre, con un fichero de febrero ilegible: sale con 2 sin escribir salida;
- los días, y un día fuera del calendario;
- un mes lleno que cubre y cada punto que rompe por separado;
- la diferencia mediana;
- los precios en puntos exactos y CRLF.

`tests/unit/test_manifiestos_f17.py`, 3 tests (9 mutaciones del esquema que rompen a propósito).

**El control (d1) sobre Dukascopy (punto 2 de la respuesta) no se ha corrido**: la guardia lo negó
a la sesión («el codigo nombra la carpeta /, que contiene material protegido, y no se puede decidir
que abrira dentro»; un guion nuevo de la rama). No se rodeó. Va en §4, para Aleks con «!».

### 3.3 D5, F17 por cuenta (`criterio_fidelidad.py`)

`cuentas_con_deslizamiento(cuentas, posiciones, puntos)` nueva: cada cuenta recompone su curva
con `curva_con_deslizamiento` (que no cambia, y su docstring dice ahora que una curva es UNA cuenta)
solo con las posiciones de sus días; agrupa por la etiqueta recibida (`mes`) y nunca la deriva de
la fecha; falla con nombre si dos cuentas comparten etiqueta o día, o si una posición no está en
ninguna. `veredicto_con_f17` recibe `cuentas` en lugar de `curva` y `suspendida`, y saca d), e) y f)
de `medir_por_cuentas`, como `cableado.py`. `CuentaDelTramo` y `cableado.py` no cambian. **El
constructor de la cuenta arrastrada de ADR-0092 §5 falta en el motor**: es de la rama que mida §5.
Tests en `test_metodo_adr0092.py`:
- **adaptado:** el de F17 de hoy pasa su curva como una sola cuenta, con sus cuatro aserciones
  iguales;
- **nuevos:** dos cuentas, donde el ajuste de una no baja el corte de la otra (con, al lado, la curva
  seguida, que sí lo arrastra); dos cuentas del mismo mes, donde no se arrastra, y una etiqueta de
  dos meses, donde sí; las cuentas mal formadas; y f), que nombra la cuenta suspendida.

**Rompe en `main` por la firma**: con el código de `main`, en un clon desechable, el fichero no
importa («cannot import name 'cuentas_con_deslizamiento'»).

### 3.4 El exportador y su contrato (D1)

`tools/mql5/ExportarTicksFTMO.mq5` (1.0, sha256 `5359f686…`), como §1.1 con las correcciones de la
respuesta:
- no exige trading algorítmico ni mercado abierto;
- la profundidad: el primer tick de cada mes, buscado dentro del mes (fila
  `mes_<AAAA-MM>_primer_msc`), y la primera M1 del servidor y del terminal por `SeriesInfoInteger`
  (`SERIES_SERVER_FIRSTDATE`, `SERIES_TERMINAL_FIRSTDATE`). **Si `SeriesInfoInteger` descarga
  historial o no, no está citado: queda por medir en la corrida**, como su valor;
- escribe en `MQL5/Files` con el prefijo `F17_`, sin carpeta propia: así no da por supuesto que
  `FileOpen` cree subcarpetas.

`tests/contract/test_exportar_ticks_ftmo.py`, 10 tests: ninguna función de trading (la lista de
`test_capa_mt5.py`), la condición DEMO literal de la 759, `MESES_CONSTRUCCION` igual a `construccion`,
la negativa y el rango antes de cualquier petición de series en `OnStart`, solo EURUSD, UTF-8 y LF; y
siete mutaciones que rompen a propósito (una `OrderSend`, un `#include <Trade\...>`, febrero en la
lista, la negativa quitada, el rango sin comprobar, una petición antes de la negativa y otro símbolo).

### 3.5 La compilación (D6), el runbook y los textos (D4, D7)

`compilar.py` gana el camino `herramienta` (sha256 `dbf63514…`), con `exportar_herramienta`,
`instalar_herramienta` y `_herramienta`. `exportar` e `instalar` de la capa no cambian, y sus tests
pasan igual. Cuatro tests nuevos en `test_compilar_mql5.py`, en los dos sentidos:
- la herramienta y `mql5/` se exportan, y `exportar` sigue copiando solo `mql5/`;
- se rechaza lo que no es una herramienta;
- se exige que esté en el índice;
- cada camino instala donde va y rechaza el del otro.

Además: `docs/runbooks/F17-HISTORIAL.md` con su entrada en el índice, el esquema `f17/` en
`data/manifests/README.md`, `tools/mql5/README.md` y `scripts/README.md`, y `/tools/mql5/*.ex5` en
`.gitignore` (`test_no_unexpected_ignored_paths` sigue en verde). El recuadro de ADR-0090 §7 va en
su propio commit, después.

## 4. PARADA de D6 (respuesta, «D6, la compilación»)

`compilar.py` y `ExportarTicksFTMO.mq5` están escritos y, con este commit, sellados. El diff de
este commit (sin este informe), `git diff --cached --stat`:

```
 .gitignore                                 |   2 +
 data/manifests/README.md                   |  29 ++
 docs/runbooks/F17-HISTORIAL.md             |  72 +++
 docs/runbooks/README.md                    |   4 +
 docs/validation/HOLDOUT-EXPOSICIONES.md    |   1 +
 scripts/README.md                          |  12 +-
 scripts/leer_historial_f17.py              | 693 +++++++++++++++++++++++++++++
 src/botsito/cases/criterio_fidelidad.py    |  59 ++-
 src/botsito/mql5bridge/compilar.py         |  74 ++-
 tests/contract/test_exportar_ticks_ftmo.py | 140 ++++++
 tests/unit/test_compilar_mql5.py           |  62 +++
 tests/unit/test_leer_historial_f17.py      | 295 ++++++++++++
 tests/unit/test_manifiestos_f17.py         | 128 ++++++
 tests/unit/test_metodo_adr0092.py          |  74 ++-
 tools/mql5/ExportarTicksFTMO.mq5           | 266 +++++++++++
 tools/mql5/README.md                       |   8 +
 16 files changed, 1908 insertions(+), 11 deletions(-)
```

Más `PROJECT_STATE.md` (el recuento de tests, 2156 → 2184) y este informe.

**Las funciones nuevas de `compilar.py`, enteras:**

```python
# Las herramientas de solo lectura o de medida de `tools/mql5/` (MedirDemoFTMO, ExportarTicksFTMO):
# un camino APARTE del de la capa (rama trabajo/f17-historial, D6), que no cambia `exportar` ni
# `instalar`. Una herramienta es un `.mq5` directamente bajo `tools/mql5/` y se instala como script.
CARPETA_HERRAMIENTAS = "tools/mql5"
_HERRAMIENTA = re.compile(r"^tools/mql5/[A-Za-z][A-Za-z0-9_]*\.mq5$")


def exportar_herramienta(repo: Path, destino: Path, fuente: str) -> list[str]:
    """Copia a `destino` la herramienta `fuente` tal como esta en el INDICE de git, y `mql5/` para
    `/include` (con `exportar`). Rechaza cualquier ruta que no sea un `.mq5` directamente bajo
    `tools/mql5/`, y una herramienta que no este en el indice."""
    if not _HERRAMIENTA.match(fuente):
        raise CompilarError(f"{fuente}: no es una herramienta de {CARPETA_HERRAMIENTAS}/ (un .mq5)")
    listado = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", fuente],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    if [f for f in listado.split("\0") if f] != [fuente]:
        raise CompilarError(f"{fuente}: no esta en el indice de git")
    copiados = exportar(repo, destino)
    prefijo = destino.resolve().as_posix().rstrip("/") + "/"
    subprocess.run(
        ["git", "-C", str(repo), "checkout-index", "-f", f"--prefix={prefijo}", "--", fuente],
        check=True,
        capture_output=True,
    )
    return [*copiados, fuente]


def instalar_herramienta(c: Compilacion, datos: Path) -> Path:
    """Copia el `.ex5` de una herramienta a `MQL5/Scripts/Botsito/` del terminal."""
    if c.ex5 is None:
        raise CompilarError(f"{c.fuente}: no hay .ex5 que instalar")
    if not _HERRAMIENTA.match(c.fuente):
        raise CompilarError(f"{c.fuente}: no es una herramienta de {CARPETA_HERRAMIENTAS}/")
    destino = datos / "MQL5" / "Scripts" / "Botsito" / c.ex5.name
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(c.ex5, destino)
    return destino


def _herramienta(a: argparse.Namespace) -> int:
    """Compila herramientas de `tools/mql5/`, cada una en su copia del indice (D6)."""
    a.salida.mkdir(parents=True, exist_ok=True)
    todas = True
    for fuente in a.fuentes:
        with tempfile.TemporaryDirectory(prefix="botsito-herramienta-") as tmp:
            raiz = Path(tmp)
            exportar_herramienta(a.repo, raiz, fuente)
            c = compilar_uno(a.metaeditor, raiz, fuente)
            (a.salida / (Path(fuente).stem + ".log")).write_text(
                log_para_anexo(c), encoding="utf-8", newline="\n"
            )
            puerta = "PASA" if c.pasa else "NO PASA"
            print(f"{fuente}: {puerta} ({c.errores} errores, {len(c.avisos)} avisos)")
            todas = todas and c.pasa and not c.avisos
            if c.pasa and a.instalar is not None:
                print(f"  instalado en {instalar_herramienta(c, a.instalar)}")
    return 0 if todas else 1
```

Y en `main`, el subcomando `herramienta` (`--repo`, `--metaeditor`, `--salida`, `--instalar` y las
fuentes) y un diccionario de órdenes en lugar del `if`; `compilar` y `pruebas`, sin cambios. El
docstring del módulo nombra el uso nuevo. `_herramienta` devuelve 1 también con avisos: D6 pide «sin
errores ni avisos».

**Los dos comandos para Aleks, con «!» desde la raíz del repositorio, tras la revisión del
consultor:**

1. La compilación de D6. `ExportarTicksFTMO.mq5` y, como control, `MedirDemoFTMO.mq5`, cada uno en
   su copia del índice; sin `--instalar`, porque se instala en la rama de la corrida. Los dos logs
   van a los anexos. Tiene que imprimir «PASA (0 errores, 0 avisos)» dos veces:

       ! uv run python src/botsito/mql5bridge/compilar.py herramienta --repo . --metaeditor "C:/Program Files/MetaTrader 5/MetaEditor64.exe" --salida docs/validation/anexos/F17-HISTORIAL tools/mql5/ExportarTicksFTMO.mq5 tools/mql5/MedirDemoFTMO.mq5

2. El control (d1) del punto 2, que la guardia le negó a la sesión. Lee los ticks de Dukascopy de
   construcción (su fila de HOLDOUT del día ya está escrita) e imprime solo recuentos:

       ! uv run python scripts/leer_historial_f17.py --control-dukascopy --salida docs/validation/anexos/F17-HISTORIAL/control-d1.txt

Si algún mes no pasa (d1), PARA: la cifra no se cambia (punto 2).

### 4.1 Lo que dieron los dos comandos (Aleks, con «!», el 2026-11-26)

1. **La compilación de D6**: «tools/mql5/ExportarTicksFTMO.mq5: PASA (0 errores, 0 avisos)» y
   «tools/mql5/MedirDemoFTMO.mq5: PASA (0 errores, 0 avisos)». Los logs, en los anexos:
   `ExportarTicksFTMO.log` (copia del índice con sha256 `5359f686…`, el del fuente; log original
   `e9f2b5ae…`) y `MedirDemoFTMO.log` (`f9903c6f…`; log `1f6d350e…`), los dos «puerta: PASA (0
   errores, 0 avisos, .ex5 si)», con el código de salida 1 de MetaEditor, que no es la puerta.
2. **El control (d1) sobre Dukascopy** (`anexos/F17-HISTORIAL/control-d1.txt`): los cuatro PASAN.

   | Mes | Días (punto 0) | Horas día-hora con tick | Con 3 spreads distintos o más |
   |---|---|---|---|
   | 2026-04 | 22 | 162 | 162 (100 %) |
   | 2026-07 | 23 | 101 | 101 (100 %) |
   | 2026-08 | 21 | 165 | 165 (100 %) |
   | 2026-01 | 21 | 163 | 163 (100 %) |

### 4.2 PARADA 2: lo medido contradice el (d2) implementado

Las horas día-hora de la ventana de esos días son 8 por día: 168 en enero y agosto, 176 en abril y
184 en julio. **Dukascopy no tiene ticks en todas**: el control solo encuentra 163, 162, 101 y 165. La
causa está en sus manifiestos: los datasets de ticks de construcción no son meses enteros, sino las
horas que se descargaron. Sus `horas.presentes` son 184 (enero), 182 (abril), 114 (julio) y 186
(agosto), con 0 ausentes y 0 vacías. Julio, por ejemplo, cubre poco más de la mitad de sus horas de
ventana.

(d1) no se ve afectado, porque su denominador son las horas con tick. **(d2) sí**: el yaml compara la
mediana de ticks por minuto de FTMO «sobre todos los minutos de la ventana de los días del mes (un
minuto sin ticks cuenta 0)» con la de Dukascopy «en los mismos minutos». El lector cuenta hoy como 0
los minutos en que Dukascopy no tiene NADA descargado, y eso baja su mediana y hace (d2) más fácil.
En julio solo 101 de las 184 horas de ventana tienen ticks de Dukascopy (el 55 %), así que la
mediana cae en el extremo bajo de las descargadas; con un poco menos de cobertura sería 0, y (d2)
pasaría siempre. No se ha medido el valor: el lector no lo imprime en el control. La diferencia mediana del spread no se ve afectada, porque solo usa pares día-hora
con ticks de las dos fuentes.

## Lo que necesito que decidas (PARADA 2)

0. **Qué minutos compara (d2).** Opciones:
   - (a) los minutos de las horas que Dukascopy tiene descargadas (`horas.presentes` de su
     manifiesto), las dos medianas sobre ese mismo conjunto. Es la lectura de «en los mismos
     minutos», y el texto de FTMO («sobre todos los minutos de la ventana») queda acotado por ahí.
   - (b) dejarlo como está (0 donde Dukascopy no tiene descarga).
   - (c) bajar antes los ticks de Dukascopy de todas las horas de la ventana de los cuatro meses, en
     su propia rama.

   Recomiendo (a). Coste de (a): si el consultor la lee como un cambio de criterio y no como su
   lectura, el yaml (fijado por sha256) se reescribe con su texto en un commit propio a la vista,
   antes de ver un tick de FTMO, que es lo único que lo autoriza. Coste de (b): (d2) deja de
   discriminar en julio. Coste de (c): otra rama y otra descarga.
1. **Si el yaml cambia o no.** Opciones: (a) no cambia, porque «en los mismos minutos» ya lo dice, y
   el lector y su test lo implementan; (b) se añade una frase al bloque `d2_ticks_por_minuto`, con el
   sha nuevo en su test. Recomiendo (b): un criterio pre-registrado no se deja a una lectura.

Sigo mientras tanto con lo que no depende de esto: el recuadro de ADR-0090 §7, las líneas del
cierre y el informe; el revisor y la CI van después de la respuesta.

## Respuesta del consultor a la PARADA 2 (2026-11-26), tal cual

Copiada también al final del encargo.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA 2 de `trabajo/f17-historial` (2026-11-26, 03:15, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA 2.
>
> 0. (d2) compara los minutos de las horas día-hora de la ventana que Dukascopy tiene descargadas en sus manifiestos de ticks de ese mes (opción a). Sobre ese mismo conjunto de minutos, un minuto sin ticks cuenta como 0 en cada fuente, y las dos medianas de ticks por minuto se calculan sobre él. Las horas que Dukascopy no tiene descargadas no entran en (d2): ni cuentan como 0 ni se comparan. El resto de D3 no cambia; (a), (b), (c) y (d1) siguen sobre todos los minutos de la ventana de los días del punto 0. La diferencia mediana de los spreads, como estaba.
>
> 1. El yaml cambia, a la vista: en un commit propio, una frase en el bloque `d2_ticks_por_minuto` con la definición del punto 0 y su sha256 nuevo en el test. El informe lo declara como desviación con su motivo: el cambio sale de los recuentos de horas de los manifiestos de Dukascopy y del control (d1), no de ningún dato de FTMO, que nadie ha visto, y la cifra (la mitad) no se mueve. Ensaya (d2) con la definición nueva sobre un caso sintético que rompa a propósito: unas horas con ticks densos en Dukascopy y escasos en FTMO, que tienen que dar «no cubre».
>
> 2. La compilación de D6 se lanzó antes de que el consultor revisara el diff, que era lo que pedía la respuesta a la PARADA 1. Declárala como desviación (solo compiló y el exportador es de solo lectura) y deja en el informe el diff de `compilar.py` (`--stat` y las funciones nuevas enteras) y el del `.mq5`, para la revisión final.
>
> Después, sigue con lo que tenías: el recuadro de ADR-0090 §7, las líneas del cierre, la CI por `fix/f17-historial` y el revisor, hasta «Rama lista para revisión, NO cerrada.»

### Cómo se aplica

- **Punto 1, el yaml, a la vista y en su propio commit:** la frase `minutos` en el bloque
  `d2_ticks_por_minuto` de `docs/plan/F17-HISTORIAL.yaml`, con la definición del punto 0. Las horas
  «descargadas» son las del propio manifiesto de ticks de Dukascopy de ese mes: `seleccion.dias` por
  `seleccion.horas_utc`, menos `horas.perdidas` (lo que escribe `congelar_ticks`,
  `data/ticks.py`:436-440, y lo que expone `cargar_ticks` como `dias_seleccion`, `horas_seleccion` y
  `horas_perdidas`). El sha256 pasa de `51a8ada2…` a `46af1341…`, y el test comprueba además la frase.
  **Desviación declarada:** el criterio pre-registrado se cambia una vez después de fijarlo. El
  motivo son los recuentos de horas de los manifiestos de Dukascopy y el control (d1); no hay ningún
  dato de FTMO detrás, porque nadie lo ha visto, y la cifra (la mitad) no se mueve.
- **Punto 0, el lector:** en el commit siguiente, con el caso sintético que rompe a propósito.
- **Punto 2, la compilación antes de la revisión. Desviación declarada:** la respuesta a la PARADA 1
  pedía que el consultor revisara el diff y que Aleks lanzara la compilación después. Se lanzó antes
  (la sesión dio el comando en el mismo mensaje que la PARADA). Solo compiló, en un temporal desde el
  índice, y el exportador es de solo lectura. El diff de `compilar.py` está en §4 (el `--stat` y las
  tres funciones nuevas enteras); el del `.mq5`, que es un fichero nuevo, es el fichero entero, en
  §4.3.

### 4.3 El `.mq5` entero, para la revisión final

> **Después del revisor (b1), la 1.01** (`958ffec3`, sha256 `eb9ccdb9…`, la que revisó el consultor
> en la PARADA 3 y la que compilan los logs de los anexos): sobre la copia de abajo, que es la 1.0,
> cambian la versión (`#property version` y `VERSION_SCRIPT`, «1.01»), la cabecera (añade «cuántos
> devuelve CopyTicksRange en una llamada» a lo que queda por medir, y que el lector lo contrasta
> «con el control (dia_*_ticks y dia_*_error)») y el rango, que lleva las dos entradas a las 00:00
> del día del servidor con una función nueva, con su comentario:
>
>     // Las 00:00 del dia del servidor de `t`: el rango se cuenta siempre por dias enteros, aunque la
>     // entrada traiga una hora (revisor de trabajo/f17-historial, b1: con «2026.08.31 06:00» el dia
>     // pedido llegaba al 1-sep).
>     datetime InicioDelDia(const datetime t)
>       {
>        return t - t % 86400;
>       }
>     ...
>        datetime desde = InicioDelDia(StringToTime(InpDesde));
>        datetime hasta = InicioDelDia(StringToTime(InpHasta));
>
> El diff entero: `git diff 531e4318 958ffec3 -- tools/mql5/ExportarTicksFTMO.mq5`.

`tools/mql5/ExportarTicksFTMO.mq5` 1.0, 266 líneas, sha256 `5359f686…`, el compilado en §4.1 y el del
commit `81c89ea0`, que no ha cambiado desde entonces. Es un fichero nuevo: su diff es el fichero
entero, que va al final de este apartado. Lo que hace, función a función:
- `Comprobaciones`: la condición DEMO de la 759 y `SymbolSelect`;
- `RangoDeConstruccion`: cada día del rango con `EsDeConstruccion` sobre `MESES_CONSTRUCCION`;
- `ExportarTicks`: `CopyTicksRange(SIMBOLO, ticks, COPY_TICKS_ALL, desde_ms, hasta_ms)` con hasta 3
  intentos y `Sleep` si `GetLastError` no es 0, a `F17_<día>_ticks.csv`;
- `ExportarM1`: `CopyRates(SIMBOLO, PERIOD_M1, día, día + 86399, velas)` a `F17_<día>_m1.csv`;
- `OnStart`: la negativa, el rango, y después el control (los relojes, `digits`, la cuenta,
  `SeriesInfoInteger` con `SERIES_SERVER_FIRSTDATE` y `SERIES_TERMINAL_FIRSTDATE`), y día a día los
  dos ficheros y sus filas de control, con el primer tick de cada mes.

```mql5
//+------------------------------------------------------------------+
//| ExportarTicksFTMO.mq5                                            |
//| Bot v3 - rama trabajo/f17-historial (2026-11-26)                 |
//|                                                                  |
//| Exporta el HISTORIAL de ticks de EURUSD que el servidor de la    |
//| demo de FTMO ya guarda (F17, ADR-0099 §5), un dia por CSV, con   |
//| la M1 del propio servidor, y un CSV de control con los relojes.  |
//| Escribe en MQL5/Files con el prefijo F17_. Lo lee                |
//| scripts/leer_historial_f17.py con el criterio pre-registrado de  |
//| docs/plan/F17-HISTORIAL.yaml. Instrucciones:                     |
//| docs/runbooks/F17-HISTORIAL.md.                                  |
//|                                                                  |
//| SOLO LEE (tests/contract/test_exportar_ticks_ftmo.py):           |
//| - no llama a ninguna funcion de trading ni de ordenes;           |
//| - se niega a correr si la cuenta no es DEMO, con la condicion    |
//|   de MedirDemoFTMO.mq5:759;                                      |
//| - solo EURUSD, y solo dias de los meses de construccion          |
//|   (MESES_CONSTRUCCION, la lista de criterio_fidelidad.yaml): si  |
//|   un dia del rango pedido es de otro mes, sale sin pedir nada.   |
//|                                                                  |
//| Lo que da por supuesto de MT5 (ADR-0082 D7): los limites del     |
//| rango de CopyTicksRange (>= from_msc, <= to_msc) y COPY_TICKS_ALL|
//| salen de la documentacion de MQL5 (docs/series/copyticksrange);  |
//| en que reloj van time_msc y las barras, si la M1 es BID y si los |
//| ticks son los guardados queda POR MEDIR en la corrida: el lector |
//| lo contrasta con el control y con los puntos (c) y (d).          |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Exporta el historial de ticks y la M1 de EURUSD del servidor de una cuenta DEMO, solo de los meses de construccion. No opera."
#property script_show_inputs

#define VERSION_SCRIPT "1.0"
#define SIMBOLO        "EURUSD"
#define INTENTOS       3
#define PAUSA_MS       1000

// la lista de construccion de knowledge/cases/criterio_fidelidad.yaml; un test exige que sea esa
string MESES_CONSTRUCCION[] = {"2026-01", "2026-04", "2026-07", "2026-08"};

input string InpDesde = "2026.04.01"; // primer dia, en la fecha del servidor (AAAA.MM.DD)
input string InpHasta = "2026.04.30"; // ultimo dia, incluido

int g_control = INVALID_HANDLE;
int g_digits  = 5;

//+------------------------------------------------------------------+
//| Utilidades                                                       |
//+------------------------------------------------------------------+
string Campo(const string texto)
  {
   string t = texto;
   StringReplace(t, "\"", "\"\"");
   return "\"" + t + "\"";
  }

void Control(const string clave, const string valor, const string nota = "")
  {
   FileWriteString(g_control, Campo(clave) + "," + Campo(valor) + "," + Campo(nota) + "\r\n");
   FileFlush(g_control);
  }

string Mes(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d", s.year, s.mon);
  }

string Dia(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d-%02d", s.year, s.mon, s.day);
  }

bool EsDeConstruccion(const datetime t)
  {
   string mes = Mes(t);
   for(int i = 0; i < ArraySize(MESES_CONSTRUCCION); i++)
      if(MESES_CONSTRUCCION[i] == mes)
         return true;
   return false;
  }

//+------------------------------------------------------------------+
//| La negativa                                                      |
//+------------------------------------------------------------------+
bool Comprobaciones(string &motivo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)
     {
      motivo = "la cuenta NO es DEMO: el script no hace nada";
      return false;
     }
   if(!SymbolSelect(SIMBOLO, true))
     {
      motivo = "no existe el simbolo EURUSD en esta cuenta";
      return false;
     }
   return true;
  }

// Todos los dias de [desde, hasta] tienen que ser de construccion: se comprueba ANTES de pedir
// nada al servidor (heredado 6: febrero no se toca ni se descarga).
bool RangoDeConstruccion(const datetime desde, const datetime hasta, string &motivo)
  {
   if(desde <= 0 || hasta < desde)
     {
      motivo = "el rango de fechas no se entiende: " + InpDesde + " a " + InpHasta;
      return false;
     }
   for(datetime d = desde; d <= hasta; d += 86400)
      if(!EsDeConstruccion(d))
        {
         motivo = "el dia " + Dia(d) + " no es de un mes de construccion: no se pide nada";
         return false;
        }
   return true;
  }

//+------------------------------------------------------------------+
//| Un dia: ticks y M1 del servidor                                  |
//+------------------------------------------------------------------+
int ExportarTicks(const datetime dia, int &intentos, int &error, long &primero, long &ultimo)
  {
   MqlTick ticks[];
   ulong desde_ms = (ulong)dia * 1000;
   ulong hasta_ms = ((ulong)dia + 86400) * 1000 - 1;
   int n = -1;
   for(intentos = 1; intentos <= INTENTOS; intentos++)
     {
      ResetLastError();
      n = CopyTicksRange(SIMBOLO, ticks, COPY_TICKS_ALL, desde_ms, hasta_ms);
      error = GetLastError();
      if(n >= 0 && error == 0)
         break;
      Sleep(PAUSA_MS);
     }
   if(intentos > INTENTOS)
      intentos = INTENTOS;
   primero = 0;
   ultimo = 0;
   if(n <= 0)
      return n;
   string nombre = "F17_" + Dia(dia) + "_ticks.csv";
   int f = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(f == INVALID_HANDLE)
      return -1;
   FileWriteString(f, "time_msc,bid,ask,flags\r\n");
   for(int i = 0; i < n; i++)
      FileWriteString(f, IntegerToString(ticks[i].time_msc) + "," + DoubleToString(ticks[i].bid, g_digits) +
                      "," + DoubleToString(ticks[i].ask, g_digits) + "," + IntegerToString(ticks[i].flags) + "\r\n");
   FileClose(f);
   primero = ticks[0].time_msc;
   ultimo = ticks[n - 1].time_msc;
   return n;
  }

int ExportarM1(const datetime dia)
  {
   MqlRates velas[];
   ResetLastError();
   int n = CopyRates(SIMBOLO, PERIOD_M1, dia, dia + 86399, velas);
   if(n <= 0)
      return n;
   string nombre = "F17_" + Dia(dia) + "_m1.csv";
   int f = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(f == INVALID_HANDLE)
      return -1;
   FileWriteString(f, "time,open,high,low,close,tick_volume,spread,real_volume\r\n");
   for(int i = 0; i < n; i++)
      FileWriteString(f, IntegerToString((long)velas[i].time) + "," + DoubleToString(velas[i].open, g_digits) + "," +
                      DoubleToString(velas[i].high, g_digits) + "," + DoubleToString(velas[i].low, g_digits) + "," +
                      DoubleToString(velas[i].close, g_digits) + "," + IntegerToString(velas[i].tick_volume) + "," +
                      IntegerToString(velas[i].spread) + "," + IntegerToString(velas[i].real_volume) + "\r\n");
   FileClose(f);
   return n;
  }

//+------------------------------------------------------------------+
//| OnStart                                                          |
//+------------------------------------------------------------------+
void OnStart()
  {
   string motivo = "";
   if(!Comprobaciones(motivo))
     {
      Alert("ExportarTicksFTMO: ", motivo);
      return;
     }
   datetime desde = StringToTime(InpDesde);
   datetime hasta = StringToTime(InpHasta);
   if(!RangoDeConstruccion(desde, hasta, motivo))
     {
      Alert("ExportarTicksFTMO: ", motivo);
      return;
     }
   g_digits = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS);

   MqlDateTime s;
   TimeToStruct(TimeTradeServer(), s);
   string nombre = StringFormat("F17_control_%04d%02d%02d_%02d%02d%02d.csv", s.year, s.mon, s.day, s.hour, s.min, s.sec);
   g_control = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_control == INVALID_HANDLE)
     {
      Alert("ExportarTicksFTMO: no se pudo crear ", nombre, " (error ", GetLastError(), ")");
      return;
     }
   FileWriteString(g_control, "clave,valor,nota\r\n");
   // los relojes, como MedirReloj de MedirDemoFTMO.mq5 (ADR-0090 §1: TimeGMT sale del ordenador)
   datetime servidor = TimeTradeServer();
   datetime gmt = TimeGMT();
   Control("version_script", VERSION_SCRIPT);
   Control("cuenta_demo", "si");
   Control("servidor", AccountInfoString(ACCOUNT_SERVER));
   Control("empresa", AccountInfoString(ACCOUNT_COMPANY));
   Control("build", IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   Control("digits", IntegerToString(g_digits));
   Control("time_trade_server_s", IntegerToString((long)servidor));
   Control("time_current_s", IntegerToString((long)TimeCurrent()), "hora del ultimo tick recibido");
   Control("time_gmt_s", IntegerToString((long)gmt), "sale del reloj del ordenador: tiene que estar en hora");
   Control("time_local_s", IntegerToString((long)TimeLocal()));
   Control("desfase_servidor_gmt_min", IntegerToString((int)((servidor - gmt) / 60)));
   Control("desfase_local_gmt_min", IntegerToString(-TimeGMTOffset() / 60));
   Control("horario_verano_local_seg", IntegerToString(TimeDaylightSavings()));
   // la profundidad del historial de M1, como metadato de la serie (respuesta a la PARADA, punto 1)
   Control("primera_m1_servidor_s", IntegerToString(SeriesInfoInteger(SIMBOLO, PERIOD_M1, SERIES_SERVER_FIRSTDATE)));
   Control("primera_m1_terminal_s", IntegerToString(SeriesInfoInteger(SIMBOLO, PERIOD_M1, SERIES_TERMINAL_FIRSTDATE)));
   Control("desde", InpDesde);
   Control("hasta", InpHasta);

   string mes_actual = "";
   long primero_del_mes = 0;
   for(datetime d = desde; d <= hasta; d += 86400)
     {
      int intentos = 0, error = 0;
      long primero = 0, ultimo = 0;
      int n = ExportarTicks(d, intentos, error, primero, ultimo);
      int m1 = ExportarM1(d);
      string dia = Dia(d);
      Control("dia_" + dia + "_ticks", IntegerToString(n));
      Control("dia_" + dia + "_m1", IntegerToString(m1));
      Control("dia_" + dia + "_error", IntegerToString(error));
      Control("dia_" + dia + "_intentos", IntegerToString(intentos));
      Control("dia_" + dia + "_primer_msc", IntegerToString(primero));
      Control("dia_" + dia + "_ultimo_msc", IntegerToString(ultimo));
      // el primer tick de cada mes pedido, buscado dentro de ese mismo mes (punto 1)
      if(Mes(d) != mes_actual)
        {
         if(mes_actual != "")
            Control("mes_" + mes_actual + "_primer_msc", IntegerToString(primero_del_mes));
         mes_actual = Mes(d);
         primero_del_mes = 0;
        }
      if(primero_del_mes == 0 && primero > 0)
         primero_del_mes = primero;
     }
   if(mes_actual != "")
      Control("mes_" + mes_actual + "_primer_msc", IntegerToString(primero_del_mes));
   Control("terminado", "si");
   FileClose(g_control);
   g_control = INVALID_HANDLE;
   Alert("ExportarTicksFTMO: terminado. Ficheros F17_* en MQL5\\Files (control: ", nombre, ")");
  }
//+------------------------------------------------------------------+
```

La copia de arriba se comprueba contra el fichero con `uv run python` antes de este commit
(§4.3, comprobación): idéntica línea a línea.

### 4.4 El punto 0 de la PARADA 2, en el lector

`scripts/leer_historial_f17.py`:
- `horas_descargadas(dias, horas_utc, perdidas)` saca del manifiesto de Dukascopy las horas que
  tiene descargadas, que `_dukascopy_del_mes` devuelve junto a sus ticks;
- `puntos_del_mes` recibe esas horas y calcula (d2) solo sobre los minutos de la ventana cuya hora
  UTC está en ellas, con 0 en cada fuente para un minuto sin ticks y las dos medianas sobre ese
  conjunto. Sin ninguna hora descargada, (d2) no se puede evaluar y no cubre;
- (a), (b), (c) y (d1) siguen sobre todos los minutos de la ventana, y la diferencia mediana del
  spread no cambia.

La salida dice sobre cuántos minutos se mide (d2). Tests nuevos en `test_leer_historial_f17.py`:
- `test_d2_compara_solo_las_horas_que_dukascopy_tiene_descargadas`, que rompe a propósito como
  pide el punto 1. Con Dukascopy descargado solo en las cuatro primeras horas y denso (8 ticks por
  minuto) frente a FTMO escaso (2), da 240 minutos y medianas 2 y 8: **no cubre** por (d2). Con FTMO
  denso en esas horas y vacío en las otras cuatro, (d2) cubre, aunque (a) falle, porque las horas
  sin descarga no cuentan como 0. Sin horas descargadas, no cubre;
- `test_las_horas_descargadas_salen_del_manifiesto`.

Los tests de hoy pasan a dar las horas de la ventana como descargadas. Son 22 tests en el fichero.

## 5. Las líneas propuestas para el cierre (encargo, §6)

Medidas con un guion de la carpeta de trabajo sobre `git show main:PROJECT_STATE.md` (24.854 bytes),
aplicando cada cambio a la letra.

**La F de la Next Action** (`PROJECT_STATE.md`:28), +63 bytes: «F17 (ADR-0099 §5) y el backtest del
trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa y el contraste con el
trader, hechos.» pasa a «F17 (ADR-0099 §5; el historial, con herramientas y sin correr:
F17-HISTORIAL.md) y el backtest del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico
de la premisa y el contraste con el trader, hechos.»

**Los textos que llaman «grabador» a todo F17:**
- **El heredado 10** (`PROJECT_STATE.md`:57), dos opciones (§11.1, decisión 0; decidido en §12):
  - (a) corregirlo, +31 bytes: «- 10. De la demo de FTMO queda F17 (ADR-0099 §5): el historial, el
    grabador y las órdenes stop.»;
  - (b) que salga por (b) REPETIDA, −67 bytes: su contenido, lo que queda de F17, vive entero en la
    F nueva (`docs/state/README.md`:65-66); va literal a HISTORIA bajo `# Pendiente heredado SALE`.
- **La hoja de ruta, A.1** (HECHA):
  - :716, «A-28 y el grabador de spread y ticks (F17, PARCIAL)» pasa a «A-28 y F17 (PARCIAL; desde
    ADR-0099 §5, el historial, el grabador y la medida de las órdenes stop)»;
  - :727, «(el panel, el BE por el ASK y el grabador) pasa a A.5» pasa a «(el panel, el BE por el ASK
    y F17) pasa a A.5».
- **La A.5**:
  - en su «Qué es», tras «y la medida de las órdenes stop.», se añade «El historial: herramientas
    hechas y sin correr (trabajo/f17-historial, F17-HISTORIAL.md); la corrida, en una prueba
    gratuita, en su rama.»;
  - su «Hecho cuando», «el panel declarado (HECHO el 2026-11-07) y el grabador hecho», pasa a «el
    panel declarado (HECHO el 2026-11-07) y las tres partes de F17 de ADR-0099 §5 hechas (el
    historial, corrido y leído; el grabador, para lo que no cubra; y la medida de las órdenes
    stop)».
- **La fila F:F17** (:923) pasa a «PARCIAL: el script de medición (tres ejecuciones, ADR-0071 y
  ADR-0090) y las herramientas del historial, sin correr; no el grabador ni la medida de las
  órdenes stop», con `F17-HISTORIAL.md` añadido en su columna de prueba.
- **La fila de F17 de MASTER_PLAN no se toca** (su NOTA del 2026-11-24).

**R6a.8** (respuesta a la PARADA, punto 6): en su «Qué es» se añade «Las aperturas H4 del servidor
(V02 de la auditoría «cazador») se pueden derivar de la M1 del servidor que exporta F17 (el
historial, F17-HISTORIAL.md).»

**Technical Debt:**
- **sale la línea :100** (`curva_con_deslizamiento` y `veredicto_con_f17`), −196 bytes, por (a)
  PAGADA: `cuentas_con_deslizamiento` y la firma nueva de `veredicto_con_f17` (`81c89ea0`, §3.3) y
  sus tests, que rompen en `main`;
- **(e) ACORTADA**, las TRES líneas de más de 200 bytes que ahorran 60 o más con su arranque
  literal cortado al final de una frase o inciso (160 bytes como mucho) y **su cita de informe con
  su sección conservada delante de la cola** (`docs/state/README.md`:81-86). Su texto entero, a
  HISTORIA. Corregido tras el revisor (a2): la primera medida quitaba la cita a dos líneas («Sin git
  callan…» y «RN-029…»); con su cita ahorran 27 y 46 bytes y no valen. El texto de cada una, a la
  letra:

  | Antes (bytes con salto) | Después, a la letra | Ahorra |
  |---|---|---|
  | `- RN-019 no dispara nunca en el motor…` (280) | `- RN-019 no dispara nunca en el motor: su forma pide \`por: activacion_sin_ruptura\` y la orden stop lleva \`por = primer_esquema\` (zonas.py) … (PUNTO-USADO.md §1.h; entera en HISTORIA, Technical Debt ACORTADA)` (211) | 69 |
  | `- El visor no conecta \`--diagnostico-cuenta-diaria\`…` (347) | `- El visor no conecta \`--diagnostico-cuenta-diaria\` (cli.py: la valida \`_diagnostico_de\`, :2250-2261; el arnés la aplica, :2438; \`motor_visor\`, :2479, no) … (VISOR-CONSTRUCCION.md §4.3; entera en HISTORIA, Technical Debt ACORTADA)` (235) | 112 |
  | `- Sin guardia contra fechas de días ocultos…` (362) | `- Sin guardia contra fechas de días ocultos en lo que añade una rama. … (GUARDIAS-HOLDOUT.md §4.3 y §9; entera en HISTORIA, Technical Debt ACORTADA)` (155) | 207 |

  Las demás de más de 200 bytes, con su cita, ahorran menos de 60:
  - la del validador del journal, 58;
  - «Sin git callan», 27;
  - «RN-029», 46;
  - y otras.

  La de la zona de RN-005 (368 bytes) no tiene un corte de frase dentro de los 160. Ninguna línea
  de Technical Debt ni de Reglas vivas está pagada, repetida ni sustituida con evidencia:
  - el ADR 0087 de S-15 no existe;
  - la nota de RN-019 y el docstring de `test_kit.py` siguen;
  - y el heredado 27 solo está repetido a medias en la A.2.

**El tamaño**, con el heredado 10 fuera por (b), las tres acortadas y la salida de la :100:
- con la F propuesta (+63), **24.266 bytes** (margen 734);
- con la F corta de §11.1, decisión 1 (−36), **24.167** (margen 833);
- con el heredado 10 corregido en lugar de sacarlo, 98 bytes más.

**No llega a los 1.000 de margen que pide el encargo con los criterios (a)-(e)**: faltan 167 bytes
en el mejor caso. Cómo llegar lo decide la orden de cierre (§11.1, decisión 1; decidido en §12), porque la F es de la
Next Action y no está bajo esos criterios.

## 6. La fila de ERRORES-RECURRENTES, preparada para el cierre

| Rama | Hallazgos del revisor | Hallazgos del consultor despues | Que se le escapo |
|---|---|---|---|
| `trabajo/f17-historial` | Una pasada, opus, con los siete alcances del encargo (F17-HISTORIAL.md, «Informe del revisor»; lo hecho, en §9): eje (a) 0 bloquea, 3 importa, 1 menor; eje (b) 1 bloquea, 5 importa, 2 menor. b1 (**bloquea**: una entrada con hora pasaba la comprobación del mes y pedía el día siguiente, que podía ser de otro mes), a1 (el mes por la fecha del servidor, a la PARADA 3), a2 (las acortadas sin su cita), a3 (los guiones que escriben, sin clon), b2 (una regla de elección en el yaml, a la PARADA 3), b3 a b6, arreglados o declarados. Segunda pasada, acotada a lo de la PARADA 3: 0 bloquea, 3 importa (fechas de borde de meses reservados en claro en el informe, la pregunta de cierre borrada, §12 sin los textos a la letra), 3 menor; arreglados todos | (1) D3 (c) decía que detectaba ticks fabricados, y no puede, porque cuadran con la M1 por construcción; (2) D7 atribuía a ADR-0090 §7 el spread, y lo que atribuye al grabador es el deslizamiento; (3) D1 pedía «el primer tick disponible», que obliga a preguntar por meses fuera de construcción; (4) D3 tomó `arnes.dias_de_mercado` de una auditoría sin comprobar qué devuelve (respuesta a la PARADA 1, «errores del consultor»); y lo que la sesión dejó a la revisión: la compilación de D6 lanzada antes de que el consultor revisara el diff (PARADA 2, punto 2). | (1) **La sesión**: el (d2) implementado contaba como 0 los minutos que Dukascopy no tiene descargados; lo cazó el control (d1) al contar horas, y cambió el yaml una vez, a la vista y sin dato de FTMO (PARADA 2). Lección: antes de comparar con una fuente de construcción, se mide qué cubre (`horas.presentes`, `seleccion`), no se supone que es el mes entero. (2) **La sesión**: la primera inversa del reloj del servidor no veía la hora repetida del 1-nov, porque los dos sondeos daban 0; su test la cazó en el borrador. (3) **La sesión**: dio en el mismo mensaje de la PARADA el comando de compilar que el consultor tenía que revisar antes; Aleks lo lanzó. Lección: un comando para «!» que espera una revisión va en un mensaje aparte, después de la respuesta. (4) La guardia negó lanzar a la sesión el lector y `compilar.py` cambiados en la rama, que lanzó Aleks: lo esperado (H5 del auditor). |

## 7. El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | §0 Base, apertura, contrato (tramo R4), sin ADR nuevo | Hecho | «Base comprobada»; `fdc18717`; contrato con las tres rutas de la respuesta, punto 7 (`3ce320e6`) |
| 2 | §0 La fila de HOLDOUT antes del primer `make check` de cada día | Hecho | filas del 2026-11-25 (2) y del 2026-11-26 (2) |
| 3 | §0 «La herramienta X da Y», medido o citado; ADR-0082 D7 | Hecho | §0.2 (documentación de MQL5 citada; lo no citado, «por medir») |
| 4 | §0 Insertar texto con Edit; guiones que escriben, en un clon | Parcial: desviación declarada (§10) | los documentos, con Edit; `compilar.py herramienta` y el lector con `--salida` los lanzó Aleks directamente en el repo, sin ensayo en un clon (revisor, a3) |
| 5 | §0 Sin programar nada que escriba en `.claude/` con un `make check` en marcha | Hecho | ningún `ScheduleWakeup` en la rama |
| 6 | §0 La guardia negó compilar y el lector: dicho, sin rodearla, lo lanzó Aleks con «!» | Hecho | §3.2, §4 y §4.1 |
| 7 | §2 Qué NO cambia (motor, simulador, `llenado.yaml`, spec, casos, evidencia, feedback, corpus, `data/`, `mql5/`, `MedirDemoFTMO.mq5`, `demo_ftmo/`, ADR-0092 §4, cifras de los yaml, ningún ADR salvo D7) | Hecho | `git diff --stat main...HEAD` sobre esas rutas, vacío (lo comprueba el revisor); el contrato las protege |
| 8 | 0.1 La fila con el recuento de EA-CONEXION | Hecho | fila 1 del 2026-11-25; el inicio de la M1 del log, en la fila 2 |
| 9 | 0.2 Lo leído, con fichero:línea | Hecho | §0.2 |
| 10 | 0.3 El auditor | Hecho | §0.3 e «Informe del auditor» |
| 11 | §4 La PARADA con el diseño, el yaml en borrador, D5, D6 y el auditor | Hecho | §1, §2 y §5 (fase 0); `4661575d` |
| 12 | D1 El exportador de solo lectura, con su contrato | Hecho de otra forma (respuesta, D1 y punto 1) | `ExportarTicksFTMO.mq5` y `test_exportar_ticks_ftmo.py` (§3.4); sin trading algorítmico; la profundidad por mes y `SeriesInfoInteger` |
| 13 | D2 El lector, con el reloj a UTC sin cifras, la negativa, los puntos, el veredicto, el spread y la diferencia mediana | Hecho | §3.2 y §4.4; 22 tests |
| 14 | D3 El criterio, antes de ver un tick, fijado por su sha256 | Hecho, con un cambio a la vista (PARADA 2) | `3ce320e6` y `802c159f`; ningún tick de FTMO visto |
| 15 | D3 El control (d1) sobre Dukascopy (respuesta, punto 2) | Hecho | §4.1: los cuatro pasan |
| 16 | D4 El manifiesto `f17/` y el runbook | Hecho | `data/manifests/README.md`, `test_manifiestos_f17.py`, `F17-HISTORIAL.md` |
| 17 | D5 F17 por cuenta, sin tocar `CuentaDelTramo` ni `cableado.py`; rompe en `main` por la firma | Hecho | §3.3; el clon de `main` no importa |
| 18 | D6 La compilación aparte, con sus tests; los dos compilan sin errores ni avisos; logs en los anexos | Hecho; lanzada antes de la revisión (desviación, PARADA 2, punto 2) | §3.5 y §4.1 |
| 19 | D7 Los README y el recuadro de ADR-0090 §7, en su propio commit | Hecho (los README); el recuadro, en su commit | §3.5; el commit del recuadro |
| 20 | D8 La CI de Linux por `fix/f17-historial` | Hecho sobre `531e4318`; se repite sobre el último commit | §8 |
| 21 | §6 Las líneas del cierre con sus bytes | Parcial: el margen queda en 734 u 833 bytes, no en 1.000 | §5 |
| 22 | §7 El informe, el revisor con sus alcances, la frase final | Hecho el revisor; la frase, tras la PARADA 3 | «Informe del revisor»; «Estado» |

## 8. La CI de Linux (D8)

`git push origin trabajo/f17-historial:refs/heads/fix/f17-historial` sobre `531e4318`: run
**45797145889**, `completed` / `failure` con **un solo fallo, el esperado**:
`tests/unit/test_cli.py::test_state_check_ok_on_real_repo` («assert 1 == 0»: `state check` ve
`fix/` y PROJECT_STATE declara `trabajo/`), «1 failed, 3588 passed, 102 skipped»
(`gh run view 45797145889 --log-failed`). Lo de después del revisor se volvió a empujar, con el
mismo único fallo esperado en cada run:
- `958ffec3`: run **45805382618**, «1 failed, 3592 passed, 102 skipped»;
- `ed2a15de`: run **45833012704**, «1 failed, 3593 passed, 102 skipped».

El run del último commit, el de la segunda pasada, va en «Estado».

## 9. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| b1 | **bloquea** | **Arreglado.** `InicioDelDia` lleva las dos entradas a las 00:00 del día del servidor antes de comprobar el rango (`.mq5` 1.01). El contrato exige `InicioDelDia(StringToTime(Inp…))` para las dos y que corte a las 00:00, con dos mutaciones que rompen a propósito. El `.mq5` cambia, así que **hay que volver a compilarlo** (§11). |
| a1 | importa | **A la PARADA 3** (§11, decisión 0): choca con «Nada lee la M1 de marzo ni de junio» del punto 0 de la respuesta a la PARADA 1. |
| a2 | importa | **Corregido** en §5: tres acortadas, con su cita, y su texto a la letra; el margen, 734 u 833 bytes. |
| a3 | importa | **Declarado** como desviación (§10); no se puede deshacer. |
| a4 | menor | **Arreglado** en los tests del reloj y de D5: fechas de 2027. Quedan a propósito los nombres de febrero y marzo del test de la negativa (es lo que prueba) y el `cubre` sintético del test de los días, que no son datos. |
| b2 | importa | **A la PARADA 3** (§11, decisión 1): el yaml está fijado por su sha256. |
| b3 | importa | **Arreglado**: el run, en §8; la fila 4 de §7, parcial; el «Estado», al día. |
| b4 | importa | **Arreglado**: `control_cuadra_con_registro`, y un test que la discrimina con `us` y `eu` el 3-nov-2027 (120 cuadra con `eu` y no con `us`, 180 al revés). |
| b5 | importa | **Arreglado** en el lector (`dias_incompletos`: los días sin ticks o con error al pedirlos salen nombrados, con su test). «Cuántos devuelve `CopyTicksRange` por llamada» pasa a la lista de lo que queda por medir, en la cabecera del `.mq5` y en §0.2. |
| b6 | importa | **Arreglado**: §10, las desviaciones. |
| b7 | menor | **Arreglado**: la hora repetida y la que no existe, también con `eu` (31-oct y 28-mar de 2027). |
| b8 | menor | **Arreglado**: fuera la línea de PLANTILLA; las líneas del cierre siguen en §5 y la PARADA de la fase 0 queda como «§5 de la fase 0»; el README de manifiestos dice que el esquema lo valida `validar_manifiesto` en su test, y que la CLI todavía no lo llama. |

## 10. Las desviaciones

1. **El criterio de D3 cambió una vez después de fijarlo** (`802c159f`): (d2) compara solo las
   horas que Dukascopy tiene descargadas. Motivo: los recuentos de horas de sus manifiestos y el
   control (d1); ningún dato de FTMO, y la cifra no cambió (PARADA 2).
2. **La compilación de D6 se lanzó antes de que el consultor revisara el diff** (PARADA 2, punto
   2). Solo compiló, en un temporal desde el índice, y el exportador es de solo lectura.
3. **Ningún guion que escribe se ensayó antes en un clon** (CLAUDE.md, «Ensayos aislados» 1; revisor,
   a3): `compilar.py herramienta` (escribe los dos logs en los anexos) y el lector con `--salida`
   (escribe `control-d1.txt`) los lanzó Aleks en el repo. Los dos sacan su ruta de un argumento
   (regla 2) y no escriben fuera de ella.
4. **El margen del cierre queda corto** (§5): 734 u 833 bytes, no 1.000.
5. **D5 no tiene test de contenido que rompa en `main` con la firma de hoy**: rompe por la firma,
   como el encargo previó.
6. **El yaml lleva la regla de elección de fila de ADR-0099 §5** (revisor, b2), copiada con su
   cita; el lector no elige. Se queda por la respuesta a la PARADA 3, punto 1.
7. **El día del servidor no es el día UTC** (revisor, a1): el fichero del día 1 trae horas del mes
   anterior, que el lector descarta sin leerlas y cuenta (respuesta a la PARADA 3, punto 0). Corrige
   lo que decía la respuesta a la PARADA 1 («Nada lee la M1 de marzo ni de junio»): ver «Cómo se
   aplica» de la PARADA 3.

## 11. PARADA 3: dos hallazgos del revisor que chocan con lo fijado

0. **El mes se decide por la fecha del servidor** (revisor, a1). El exportador pide cada día de
   las 00:00 a las 24:00 del servidor, que va dos o tres horas por delante de UTC. Así, el fichero
   del 1 de abril trae las últimas horas UTC del último día de marzo, y el del 1 de julio las del
   último día de junio. Son horas fuera de la ventana, de noche, pero son ticks y M1 de marzo y de junio, y la
   respuesta a la PARADA 1 dice «Nada lee la M1 de marzo ni de junio». Enero no se ve afectado: el
   1 de enero el servidor está cerrado. Opciones:
   - (a) el lector descarta, sin usarlas, las filas cuya fecha UTC no sea de construcción, y las
     cuenta en su salida. El yaml y el runbook dicen que el día del servidor empieza antes que el
     UTC, y la lectura se declara en HOLDOUT, por recuento, el día que corra (ADR-0021 §1: son velas).
   - (b) el exportador no pide nada antes de las 00:00 UTC del primer día del mes. Para eso
     necesita el desfase del servidor en ese instante, que hoy no conoce sin el registro.
   - (c) dejarlo como está y declararlo.

   Recomiendo (a). Coste de (a): los ficheros del primer día siguen trayendo esas horas desde el
   servidor; no se leen para nada, pero están en el CSV. Coste de (b): meter en el exportador una
   cifra o un cálculo de huso que el registro ya tiene.
1. **El yaml lleva una regla de elección de fila que nadie dio** (revisor, b2).
   `solo_si_cubre.diferencia_mediana.lectura` dice qué fila del puente «vale»: «cuyo número sea el
   mayor que no pase de su valor absoluto». La regla está copiada de ADR-0099 §5. Pero D2 decía
   «sin elegir», y la respuesta, punto 3, solo dice que es la que «se compara». Opciones:
   - (a) se queda: es el texto de ADR-0099 §5, y el lector no elige (imprime la diferencia y nada
     más);
   - (b) el yaml cambia a la vista, con su sha256 nuevo, y esa frase pasa a decir «se compara con
     las filas `spread_menos_1` y `spread_menos_2` del puente (ADR-0099 §5)».

   Recomiendo (a), y que el informe lo declare. Coste de (b): un segundo cambio del criterio
   pre-registrado, aunque sin datos detrás.

**Y la compilación otra vez** (b1 cambió el `.mq5`): tras la revisión del consultor de este diff,
desde la raíz del repo, el mismo comando de D6. Tiene que salir «PASA (0 errores, 0 avisos)» dos
veces, y los logs sustituyen a los de `0dabbeab` en los anexos:

    ! uv run python src/botsito/mql5bridge/compilar.py herramienta --repo . --metaeditor "C:/Program Files/MetaTrader 5/MetaEditor64.exe" --salida docs/validation/anexos/F17-HISTORIAL tools/mql5/ExportarTicksFTMO.mq5 tools/mql5/MedirDemoFTMO.mq5

### 11.1 Para la orden de cierre, tal como se preguntó en la PARADA 3

Era el «§12. Lo que necesito que decidas en la orden de cierre» de `958ffec3`. Se repone tras la
segunda pasada del revisor (b1): lo contestó la respuesta de abajo («Para el cierre»), y §12 lleva
ahora las líneas que decide.

0. **El heredado 10.** Opciones: (a) corregirlo (+31 bytes); (b) que salga por (b) REPETIDA (−67).
   Recomiendo (b): la F nueva dice entero lo que queda de F17. Coste de (b): ninguno.
1. **Los bytes que faltan para el margen de 1.000.** Opciones: (a) la F corta, «F17 (ADR-0099 §5;
   el historial: F17-HISTORIAL.md) y el backtest del trader con costes (ADR-0100, R4.10),
   pendientes.», que saca de la Next Action lo hecho (el diagnóstico de la premisa y el contraste,
   ya en HISTORIA; RITUAL.md, punto 3): margen de 833; (b) aceptar el margen de 734 con la F
   propuesta. Ninguna llega a 1.000 con los criterios (a)-(e); faltan 167 bytes en el mejor caso, y
   no hay en Technical Debt, en los heredados ni en las Reglas vivas otra línea que salga con
   evidencia. Recomiendo (a). Coste de (b): un margen más corto.

## Respuesta del consultor a la PARADA 3 (2026-11-26), tal cual

Copiada también al final del encargo.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA 3 de `trabajo/f17-historial` (2026-11-26, 07:40, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA 3.
>
> Revisión de la compilación: el consultor leyó en `fix/f17-historial` (958ffec3) el diff de `compilar.py` (el camino `herramienta`: solo un `.mq5` directamente bajo `tools/mql5/` y en el índice, compilado en una copia temporal del índice, sin cambiar `exportar` ni `instalar`) y `ExportarTicksFTMO.mq5` 1.01 (ninguna función de trading; DEMO y rango de construcción comprobados antes de pedir nada; solo escribe en `MQL5/Files`; b1 normaliza las dos fechas al inicio del día). Aprobado: Aleks recompiló con «!» después de esta revisión. Commitea los logs nuevos de los anexos con su `make check`.
>
> 0. Las horas de otro mes en los días de los bordes (a1): de acuerdo con tu recomendación. El exportador sigue pidiendo días del servidor. El lector pasa cada tick y cada M1 a UTC y descarta, sin usarlo para nada, todo lo que cae fuera del mes UTC pedido; lo cuenta en su salida, por mes vecino y en número de filas, y la fila de HOLDOUT del día de la corrida lo declara por recuento. Son precios fuera de la ventana: ADR-0021 §1 no los trata como holdout, y ningún día de febrero queda nunca en el borde de un mes de construcción. Test sintético que rompe a propósito: un tick de la última hora UTC del mes anterior en el fichero del día 1 no entra en ninguna cuenta y sí en el recuento de descartes. Corrige en el informe la frase de la respuesta a la PARADA 1 «Nada lee la M1 de marzo ni de junio» con lo que pasa de verdad: el exportador las baja en esas horas de borde y el lector las descarta sin leerlas para nada.
>
> 1. La regla de elección de fila del yaml (b2): se queda. Es copia literal de ADR-0099 §5, el yaml lo dice con su cita y el lector no elige nada. Declárala en el informe. El yaml no cambia más.
>
> Para el cierre: de acuerdo con que el heredado 10 salga por (b) y con una F corta, con el margen en 833 bytes. Doy por bueno no llegar a 1.000 porque a2 exige conservar las citas; deja los textos a la letra en §12.
>
> Después: la CI de `fix/f17-historial` sobre el último commit (el número del run, con el único fallo esperado de `state check`), el revisor solo sobre lo que cambie desde 958ffec3, y termina con «Rama lista para revisión, NO cerrada.»

### Cómo se aplica

- **La compilación revisada y los logs nuevos**: los dos «PASA (0 errores, 0 avisos, .ex5 si)», ya
  con el `.mq5` 1.01 (copia del índice con sha256 `eb9ccdb9…`, la del fuente; log original
  `9de3797e…`), sustituyen en los anexos a los de la 1.0. Entran con este commit.
- **Punto 0, el lector**: `leer_ticks` y `leer_m1` reciben el mes pedido, pasan cada fila a UTC y,
  si cae fuera de ese mes, la descartan ANTES de leer su precio y la cuentan por su mes
  («ticks del AAAA-MM», «M1 del AAAA-MM»). La salida da por mes «DESCARTADAS sin usar (fuera del mes
  UTC pedido; para HOLDOUT, por recuento)». El test
  `test_las_filas_de_otro_mes_utc_se_descartan_sin_leer_su_precio` rompe a propósito: un tick y una
  M1 de la última hora UTC del mes anterior en el fichero del día 1, con su precio ilegible, no
  entran en ninguna cuenta y sí en los descartes; sin el mes, el mismo fichero falla al leer ese
  precio. Lo dicen también el runbook y el docstring de `leer_ticks`.
- **La corrección de «Nada lee la M1 de marzo ni de junio»** (respuesta a la PARADA 1, punto 0;
  la copia de arriba es literal y no se toca): lo que pasa de verdad es que el exportador, al pedir
  el día 1 de abril y el 1 de julio por el reloj del servidor, baja también las últimas dos o tres
  horas UTC del último día del mes anterior (de marzo y de junio), fuera de la ventana; el lector las descarta sin
  leerlas para nada y las cuenta; y la M1 de Dukascopy de marzo y de junio no la lee nada
  (`dias_del_mes` no usa `arnes.dias_de_mercado`).
- **Punto 1, la regla de elección del yaml, declarada**: `solo_si_cubre.diferencia_mediana.lectura`
  lleva la regla de ADR-0099 §5 (qué fila del puente «vale»), copiada con su cita. El lector no
  elige nada: imprime la diferencia. El yaml no cambia más (§10, desviación 6).

## 12. Las líneas del cierre que decide la respuesta, a la letra

Con el heredado 10 fuera por (b) y la F corta, PROJECT_STATE queda en **24.167 bytes (margen 833)**,
medidos sobre el de `main` (24.854). Lo que no llega a 1.000 lo da por bueno la respuesta, porque
a2 exige conservar las citas.

- **La F** (`PROJECT_STATE.md`:28): se sustituye «F17 (ADR-0099 §5) y el backtest del trader con
  costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa y el contraste con el trader,
  hechos.» por «F17 (ADR-0099 §5; el historial: F17-HISTORIAL.md) y el backtest del trader con
  costes (ADR-0100, R4.10), pendientes.» (−36 bytes). El diagnóstico de la premisa y el contraste
  están ya en HISTORIA (sus registros de cierre).
- **Sale el heredado 10** (`PROJECT_STATE.md`:57), por (b) REPETIDA: lo que queda de F17 vive
  entero en la F. Va literal a HISTORIA, bajo `# Pendiente heredado SALE · sale de PROJECT_STATE.md
  en trabajo/f17-historial (<fecha>)`, con la condición (b) y la F como evidencia:

      - 10. De la demo de FTMO queda el grabador de spread y ticks, F17.

- **Sale de Technical Debt la línea :100**, por (a) PAGADA (`cuentas_con_deslizamiento` y
  `veredicto_con_f17` por cuenta, `81c89ea0`, y sus tests), literal a HISTORIA bajo `# Technical Debt
  PAGADA · …`:

      - `curva_con_deslizamiento` y `veredicto_con_f17` (criterio_fidelidad.py) toman una sola curva y arrastran `previo` entre cuentas: cuando F17 los use, por cuenta (CUENTA-POR-MES.md, fase 0 e) 8).

- **Tres líneas de Technical Debt, (e) ACORTADA**: su texto entero va a HISTORIA bajo
  `# Technical Debt ACORTADA · …`, y en PROJECT_STATE quedan así (las mismas de la tabla de §5):

      - RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden stop lleva `por = primer_esquema` (zonas.py) … (PUNTO-USADO.md §1.h; entera en HISTORIA, Technical Debt ACORTADA)
      - El visor no conecta `--diagnostico-cuenta-diaria` (cli.py: la valida `_diagnostico_de`, :2250-2261; el arnés la aplica, :2438; `motor_visor`, :2479, no) … (VISOR-CONSTRUCCION.md §4.3; entera en HISTORIA, Technical Debt ACORTADA)
      - Sin guardia contra fechas de días ocultos en lo que añade una rama. … (GUARDIAS-HOLDOUT.md §4.3 y §9; entera en HISTORIA, Technical Debt ACORTADA)

- **La hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`; no cuenta en los bytes de PROJECT_STATE):
  - A.1, :716: «A-28 y el grabador de spread y ticks (F17, PARCIAL)» pasa a «A-28 y F17
    (PARCIAL; desde ADR-0099 §5, el historial, el grabador y la medida de las órdenes stop)»;
  - A.1, :727: «(el panel, el BE por el ASK y el grabador) pasa a A.5» pasa a «(el panel, el BE
    por el ASK y F17) pasa a A.5»;
  - A.5, «Qué es»: tras «y la medida de las órdenes stop.» se añade «El historial: herramientas
    hechas y sin correr (trabajo/f17-historial, F17-HISTORIAL.md); la corrida, en una prueba
    gratuita, en su rama.»;
  - A.5, «Hecho cuando»: «el panel declarado (HECHO el 2026-11-07) y el grabador hecho» pasa a «el
    panel declarado (HECHO el 2026-11-07) y las tres partes de F17 de ADR-0099 §5 hechas (el
    historial, corrido y leído; el grabador, para lo que no cubra; y la medida de las órdenes
    stop)»;
  - R6a.8, «Qué es»: se añade «Las aperturas H4 del servidor (V02 de la auditoría «cazador») se
    pueden derivar de la M1 del servidor que exporta F17 (el historial, F17-HISTORIAL.md).»;
  - la fila F:F17, :923, entera, pasa a:

        | F:F17 | PARCIAL: el script de medición (tres ejecuciones, ADR-0071 y ADR-0090) y las herramientas del historial, sin correr; no el grabador ni la medida de las órdenes stop | `DEMO-EJECUCION-1.md`, `DEMO-EJECUCIONES-2-3.md`, `F17-HISTORIAL.md` |

  La fila de F17 de MASTER_PLAN no se toca (su NOTA del 2026-11-24).

## Informe del auditor (subagente `auditor-encargo`, 2026-11-25), tal cual

Copiado tal cual, con sus títulos bajados dos niveles. No cita ninguna fecha de un mes reservado
(lo dice él mismo).

#### Auditoría del encargo · trabajo/f17-historial · 2026-11-25

No escribí nada en el repo: solo Read, Grep y Bash de lectura, sin `make`, sin tests y sin `--help`. No imprimo ninguna fecha de mes reservado: el día que contó el tester en EA-CONEXION es de un mes que hoy está reservado, y lo nombro así.

**Resumen:** 50 afirmaciones; 31 correctas, 2 incorrectas, 17 con matiz. 11 herencias no recogidas.

##### Afirmaciones

| # | Afirmación (literal o resumida) | Veredicto | Evidencia |
|---|---|---|---|
| 1 | Base `main` en `2dc4f7dd`; el merge `96b250fd` lleva `stable/F39o-contraste-trader`; el último tag es F39o | CORRECTA | `git rev-parse main` y `origin/main` dan 2dc4f7dd…; el tag apunta a 96b250fd; `git tag -l stable/F39*` por fecha: F39o, F39n, F39m |
| 2 | «CI de main 45747377112 en verde según ese cierre» | MATIZ | El número no aparece en ningún sitio de `main`. El registro de cierre de contraste-trader (final de HISTORIA) dice solo «La que cuenta es la de main sobre el commit de estado», sin número. Hay que comprobarlo con `gh` (lo hace `abrir-rama`) |
| 3 | Sin ninguna otra rama | CORRECTA | `git for-each-ref refs/heads refs/remotes`: main, trabajo/f17-historial, origin/main |
| 4 | Tramo R4 (es R4.7); la A.5 se cita | CORRECTA | HOJA-DE-RUTA.md:330 (`## R4`) y :437-443 (R4.7, Refs NA:F · F:F17). `scripts/contrato_rama.py:129-152` acepta el id del tramo |
| 5 | Ningún ADR nuevo; el bloque ids-inexistentes no declara ninguno | CORRECTA | Todos los ids citados existen: ADR-0005, 0024, 0069, 0082, 0090, 0092 y 0099, y A-28 |
| 6 | La lista blanca, y cada ruta fuera de `rutas_protegidas` | MATIZ | contrato.yaml:5-68 cuadra con el encargo. Pero faltan tres cosas: `docs/runbooks/README.md` (H3), `docs/adr/README.md`, que está PROTEGIDO (H4), y `tests/unit/test_cuenta_por_mes_metodo.py` (H11) |
| 7 | La fila de HOLDOUT va antes del primer `make check` | CORRECTA | CLAUDE.md (G2). La fila ya existe: HOLDOUT-EXPOSICIONES.md:195 |
| 8 | 0.1: «el recuento de ticks de un día de EA-CONEXION.md:141-145 (solo un recuento, ningún precio)» | MATIZ | Esas líneas traen más que un recuento: la hora del primer y del último tick, y que «el historial de velas M1 empieza el [inicio de 2025] según el log» (:144). Eso último es justo la profundidad que miden D1 y D3. Además se midió en el **Strategy Tester**, no en el terminal, y el día es de un mes hoy reservado. La fila :195 declara el recuento y las horas, pero no el inicio de la M1 |
| 9 | `MedirDemoFTMO.mq5` `Comprobaciones` :757-791, la negativa fuera de DEMO en :759, CSV en `MQL5/Files` | CORRECTA, con matiz | :757-791 y :759 son literales; CSV en :7 y :1522. Matiz: la función también exige Algo Trading activado (:769-773), mercado abierto (:774-778) y una cotización de menos de 2 min (:785-789). Un exportador de solo lectura que copie el patrón se negaría en fin de semana y pediría Algo Trading sin necesitarlo |
| 10 | `arnes.py` `dias_de_mercado`, :184 | CORRECTA (la línea) | arnes.py:184. Su uso en D3 es la n.º 33 |
| 11 | `broker_offset_base` y `broker_dst` en parametros.yaml hacia :140-180 | CORRECTA | :140-159 (120, CONFIRMED, ADR-0090) y :160-183 (`us`). `consumido_por` incluye F17 (:156, :180) |
| 12 | A-28; ADR-0090 §1 | CORRECTA | ambiguedades.yaml: A-28 `estado: DECIDIDA`, `decision: ADR-0090`; ADR-0090:44-65 |
| 13 | «`compilar.py` hoy solo exporta `mql5/` e instala en Experts o Scripts» | CORRECTA | compilar.py:95-111 (`git ls-files -- mql5`) y :174-184. `Path(fuente).parts[1]` daría «mql5» para `tools/mql5/X.mq5`: hace falta otro camino |
| 14 | «ADR-0069 §1-§2 y su NOTA del 2026-10-13» | MATIZ | La NOTA está en **§5** («Lo que NO cambia», 0069:128-132), no en §1-§2 |
| 15 | ADR-0092 §4, §8 y su NOTA sobre la cuenta arrastrada de §5 | CORRECTA, con matiz | §4: 0092:99-115; §8: :218-228; NOTA: :230-246. La NOTA dice que la arrastrada de §5 «no existe todavía: su rama dirá, con su ADR, cómo se arrastra allí» (:244-246). D5 no puede decidir cómo se arrastra en el motor, solo el ajuste dentro de una cuenta que le den |
| 16 | ADR-0099 §5: «antes que nada» | CORRECTA, con matiz | 0099:159. Matiz: §5 habla de los ticks que el servidor sirve «al Strategy Tester» (:159-163); D1 elige el terminal. Es una elección legítima, pero la profundidad del terminal no está medida y el informe debe decir que se aparta de lo medido |
| 17 | Las funciones de criterio_fidelidad.py y lo que hacen hoy | CORRECTA, con matiz | `curva_con_deslizamiento` arrastra `previo` (:842-866). `veredicto_con_f17` llama a `medir_rentabilidad` con una sola curva y nunca a `medir_por_cuentas` (:885-921). Solo las llaman los tests. **Matiz:** `CuentaDelTramo` es «una cuenta mensual…: su mes» con `mes: str` (:679-684), así que una cuenta arrastrada de varios meses no cabe sin cambiar la clase. Y en `engine/cableado.py:1537-1543` la cuenta arrastrada (sin `cuentas_cerradas`) no es una `CuentaDelTramo`: sale de `curva_de_equity`. Ese fichero está protegido |
| 18 | CUENTA-POR-MES.md, fase 0 e) 8 | CORRECTA | CUENTA-POR-MES.md:118-120 |
| 19 | Technical Debt :100 | CORRECTA | PROJECT_STATE.md:100, igual en main; 196 bytes |
| 20 | Si el historial cubre, el spread de FTMO sale de ahí sin esperar al grabador | CORRECTA | 0099:163-164 |
| 21 | `deslizamiento_fijo_puntos` sigue en 0 | CORRECTA | knowledge/simulador/llenado.yaml:9 |
| 22 | La capa no envía órdenes: `test_capa_mt5.py` | CORRECTA | test_capa_mt5.py:576; `FUNCIONES_DE_TRADING` en :42 (33 funciones, :343-344) |
| 23 | `test_manifiestos_demo_ftmo.py` exige exactamente las ejecuciones 1, 2 y 3 | CORRECTA | :47-49, `assert ejecuciones == [1, 2, 3]` |
| 24 | ADR-0092 §4: mediana y percentil 90 | CORRECTA | 0092:105-112 |
| 25 | D1: contrato en `tests/contract/` como el de MedirDemoFTMO, comprobado en el texto como `test_capa_mt5` | CORRECTA | Existe `tests/contract/test_medir_demo_ftmo.py` (`LINEA_DEMO = 759`, :30-32) |
| 26 | D1: solo los meses de `construccion` de `criterio_fidelidad.yaml`; heredado 6 | CORRECTA, con matiz | criterio_fidelidad.yaml:47 da `["2026-04", "2026-07", "2026-08", "2026-01"]`; heredado 6 en PROJECT_STATE:53 y HISTORIA:696. Son solo esos cuatro de 2026: los de 2024 de ADR-0100 «no son construccion de criterio_fidelidad.yaml» (PREMISA-COSTES.yaml, `regimen`). Matiz: julio entra «del 1 al 17» y enero «del 2 al 30» por lo que cubren los libros (:42-44), pero la lista son meses enteros. El yaml de D3 debe decir qué días de esos meses cuentan |
| 27 | D1: «más el primer tick disponible del símbolo» frente a «cualquier otro mes, se niega sin pedir nada» | MATIZ (el encargo se contradice) | Saber hasta dónde llegan los ticks obliga a preguntar por fechas anteriores: febrero de 2026 (heredado 6), 2025 (los meses de rentabilidad de ADR-0092 §5) o marzo. Cómo se obtiene sin pedir ticks de esos meses es un comportamiento de MT5 que hay que citar (ADR-0082 D7, 0082:143-149). Ver «Lo que no pude comprobar» |
| 28 | D1: `TimeTradeServer()` y `TimeGMT()` como control; MASTER_PLAN:258 | CORRECTA, con matiz | MASTER_PLAN.md:258 dice literalmente «desfase servidor-UTC registrado». Matiz: ADR-0090 §1 (:59-65) advierte que `TimeGMT()` sale del reloj del ordenador y lo valida con `time_current` y el desfase y horario de verano locales (filas 27, 32 y 33; MedirDemoFTMO.mq5:389-396). El control de D1 debería llevar esos mismos datos |
| 29 | D2: la rejilla y las horas de la ventana de `ticks_spread.py`; sus percentiles | CORRECTA | ticks_spread.py:100-117 (`reloj_de_las_sesiones`, `ventana_inicio` y `ventana_fin`) y :42-59 (rango más cercano) |
| 30 | D2 y D3: la tolerancia de 2 puntos de `ticks_integridad.py`, «fijada para Dukascopy» | CORRECTA, con matiz | ticks_integridad.py:27 (`TOLERANCIA_PUNTOS = 2`) y :3-9. Matiz: el número quedaría en dos sitios, la constante y el yaml de D3 (ADR-0002, una sola puerta). Hay que decir cuál manda y que un test compare los dos |
| 31 | D2: la «diferencia mediana» con Dukascopy en las horas de la ventana decide `spread_menos_1` o `spread_menos_2` | CORRECTA, con matiz | 0099:177-179; PUENTE-TECHO.yaml:14, :23-24 y :36-37. Matiz: no dice si es la mediana de las diferencias por hora, la diferencia de las medianas o se calcula sobre ticks. Se fija en el yaml antes de ver datos |
| 32 | D3: fijado por su sha256, como `PREMISA-COSTES.yaml` | CORRECTA | test_premisa_costes.py:151-153 (el sha) y :182-189 (rompe a propósito) |
| 33 | D3: «los minutos de la ventana… de sus días de mercado (`arnes.dias_de_mercado`)» | **INCORRECTA** | `dias_de_mercado` no enumera los días de mercado de un mes. Recibe `dias: Sequence[DiaTrader]` (arnes.py:189), que son los días `dev` del trader por la compuerta (`dias_de_construccion`, :139-147), y devuelve sus velas. Además lee la M1 de Dukascopy del mes y del anterior (:206-211), es decir marzo y junio, con días reservados (Technical Debt, PROJECT_STATE:106; HOJA G.2 :817-819). Y FTMO cierra el 1 de enero de 2026 (knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:44-48): con «todos los laborables», enero no cubriría por (b) aunque los datos estén bien |
| 34 | D3 (c): «la M1 BID del propio servidor», y en D1 «el lector lo comprueba con el punto (c)» | MATIZ | Que la M1 de MT5 sea BID es un hecho de MT5 sin cita (D7). El denominador de `comparar` incluye `solo_repo` (ticks_integridad.py:55-59 y :78), distinto del «de las M1 con ticks» de (c). Y sobre todo: unos ticks fabricados a partir de la M1 cuadran con su OHLC por construcción (la reconstrucción es primero, máximo, mínimo y último BID, :38-47), y llenan todos los minutos que tienen vela. Ni (a) ni (c) distinguen ticks reales de generados, que es lo que ADR-0099 §5 (:161-163) pide cuidar |
| 35 | Usar los ticks como fuente pide un ADR que enmiende ADR-0005 y ADR-0024 (punto 4) | CORRECTA | 0099:164-165; ADR-0024:22-25. Nota: ADR-0024 §4 ya admite MT5 para «spread real» |
| 36 | D4: el esquema `schema_demo_ftmo` de `data/manifests/README.md` | CORRECTA | README:56-75. La guardia inmutable cubre todo `.yaml` bajo `data/manifests/` (pre-commit:60), y `knowledge validate` solo lee la raíz (:62-64) |
| 37 | D4: el runbook con la forma de `DEMO-FTMO.md` | CORRECTA | Existe docs/runbooks/DEMO-FTMO.md |
| 38 | D5: que f) siga diciendo qué cuenta falla | CORRECTA | `veredicto_rentabilidad`, :805-810 (usa `meses_suspendidos`). El matiz de la clase, en la n.º 17 |
| 39 | D5: los tests de hoy de `test_metodo_adr0092.py` se adaptan | CORRECTA | :295-304 y :315-342 |
| 40 | D5: la línea :100 sale en el cierre | CORRECTA | docs/state/README.md:64, condición (a) |
| 41 | D6: `compilar.py` y su test; «el `.ex5` no se versiona» | CORRECTA, con matiz | Existe `tests/unit/test_compilar_mql5.py`. Matiz: `.gitignore` no ignora `*.ex5` (el grep da vacío; EA-CONEXION:74). Hoy se cumple solo porque se compila en una carpeta temporal (compilar.py:264). Un `.ex5` dentro del repo deja `make check` sin sello |
| 42 | D6: `MedirDemoFTMO` compila sin errores ni avisos | CORRECTA (precedente) | MARGEN-PENDIENTE.md:686-692 (la 1.2: 0 errores, 0 avisos); EA-CONEXION:61 (la 1.1) |
| 43 | D7: `scripts/README.md` (:85) y `tools/mql5/README.md` | CORRECTA | scripts/README.md:85 dice «Futuro: grabacion de ticks de la demo (F17)» |
| 44 | D7: ADR-0090 §7 «dice que el spread "lo mide el grabador de spread y ticks de F17"» | **INCORRECTA** | ADR-0090 §7 se titula «El deslizamiento: observaciones, no un modelo» (:231-237), y el «lo» es el deslizamiento, no el spread. ADR-0099 §5 dice que un grabador no puede medirlo (:154-155) y se lo da a la medida de las órdenes stop (:168-172), que es la segunda rama |
| 45 | D8: se empuja como `fix/f17-historial`, con el único fallo esperado de `state check` | CORRECTA | RITUAL.md:101-107; ci.yml:3-4 |
| 46 | §6: lo que llama «grabador» a todo F17: heredado 10, A.1, el «Hecho cuando» de A.5 y la fila F:F17 | CORRECTA | PROJECT_STATE:57; HOJA:716, :727, :782 y :923. Lo mismo lista PUENTE-TECHO.md:568-570. Hay dos sitios más con el mismo texto: ADR-0090 §7 (:236) y scripts/README:85 |
| 47 | La fila de F17 de MASTER_PLAN no se toca (su NOTA lo dice) | CORRECTA | MASTER_PLAN.md:38-43, «La fila de F17 no se toca» |
| 48 | «PROJECT_STATE está en 24.854 bytes de 25.000» | CORRECTA | `git show main:PROJECT_STATE.md \| wc -c` da 24854; `TOPE_BYTES = 25_000` en test_project_state.py:21. Con la apertura, la rama ya está en 24.944 (lo que mide el test, `stat`, :51) |
| 49 | Los criterios (a)-(e) «valen para los heredados, Technical Debt y las Reglas vivas» | MATIZ | (a)-(d) valen para las tres (docs/state/README.md:60-69). (e) ACORTADA es solo para líneas de Technical Debt de más de 200 bytes (:81-86) |
| 50 | ADR-0082 D7: ningún comportamiento de MT5 entra como hecho sin medirlo o citarlo | CORRECTA | ADR-0082:143-149 (el §8 lleva el título D7) |

##### Lo que el repo pide y el encargo no recoge

| # | Qué | Dónde lo pide | Evidencia |
|---|---|---|---|
| H1 | Si el lector usa `arnes.dias_de_mercado`, lee la M1 de marzo y de junio sin declararlo: va a HOLDOUT el día que corra, y G.2 pide una línea `LECTURA:` por recuento | Technical Debt; hoja G.2 | PROJECT_STATE:106; HOJA:817-819 |
| H2 | El calendario de cierres de FTMO es la fuente de qué días abre el servidor y cubre los cuatro meses (`cubre` va de 2025-12-04 a 2026-10-07). Cierra el 1 de enero de 2026 | ADR-0068 | knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:18-48 |
| H3 | `docs/runbooks/README.md` lista cada runbook. `F17-HISTORIAL.md` debería entrar, y el fichero no está en `rutas_permitidas` | práctica del índice | docs/runbooks/README.md:4-37 (DEMO-FTMO en :23-25) |
| H4 | Los recuadros se anotan en la columna Estado del índice de ADR. El recuadro de D7 lo pediría, y `docs/adr/README.md` está protegido | práctica | docs/adr/README.md:34, :60 y :66; contrato.yaml:68 |
| H5 | **La guardia negará el `compilar.py` cambiado.** Solo el guion idéntico al de `main` está exento (guardia.py:4337). El código cambiado se analiza, y un `subprocess.run` cuyo programa sale de un argumento (`str(metaeditor)`, compilar.py:131-140) se niega con «el programa que lanza no se calcula» (guardia.py:5073-5075). Los logs de D6 y el control saldrán del «!» de Aleks: es seguro, no posible. EA-CONEXION:79-82 lo dejó como herencia 7 | ERRORES; EA-CONEXION | citas de la columna Qué |
| H6 | V02 de la auditoría «cazador»: «En la misma prueba, sacar las aperturas H4 del servidor». Toca R6a.8 y ADR-0027 §4, y ADR-0005:28-29 dice que «solo F17 puede verificar» el ancla. El encargo ni lo recoge ni lo descarta | auditoría; ADR-0005 | AUDITORIA-CAZADOR-2026-11-23.md:137; HOJA:644-653 |
| H7 | `cuenta_pruebas` tiene `consumido_por: [F17, F33]`, con la nota «F17 mide el reloj del servidor contra este terminal» | registro; MASTER_PLAN | parametros.yaml:1817-1832; MASTER_PLAN:287 |
| H8 | MASTER_PLAN prevé un esquema v2 con el proveedor `mt5_demo` para F16 y F17. D4 crea uno aparte en `f17/` y debería decir por qué | MASTER_PLAN §H | MASTER_PLAN:299; no hay `mt5_demo` en `src/` |
| H9 | ADR-0099 §7: el ADR de Aleks llega como tarde hacia el 2026-12-03, con lo que haya. Es el calendario de la segunda rama y de la prueba | ADR-0099 | 0099:194-199 |
| H10 | La CI no tiene `data/`. Y el CSV de MQL5 sale con `FILE_ANSI` y CRLF (EA-CONEXION:153-156), donde `grep` sin `-U` da LF por error (ADR-0090:35-40): el lector acepta CRLF y el `fin_de_linea` del manifiesto se mide con Python o `grep -U` | ERRORES-RECURRENTES | ERRORES-RECURRENTES.md:31; ADR-0090:35-40 |
| H11 | Si D5 cambia `CuentaDelTramo`, se rompen `tests/unit/test_cuenta_por_mes_metodo.py:32-34`, que no está en `rutas_permitidas`, y `engine/cableado.py:1562`, que está protegido y es parte del motor de §2 | contrato | contrato.yaml:28-36 |

##### Comandos del encargo

| # | Comando | Existe y se ejecuta así | Evidencia |
|---|---|---|---|
| C1 | `/abrir-rama trabajo/f17-historial` | Sí (skill) | .claude/skills/abrir-rama |
| C2 | `make check > make-check.log 2>&1` | Sí, con la salida a un fichero | CLAUDE.md; Makefile |
| C3 | `uv run botsito state check` (contrato) | Sí | cli.py:3140-3142; `state_check` en :105 |
| C4 | `uv run botsito knowledge validate`, con el log fuera del repo | Sí | cli.py:3143-3146; :179 |
| C5 | `uv run python scripts/contrato_rama.py` | Sí | scripts/contrato_rama.py |
| C6 | `uv run python src/botsito/mql5bridge/compilar.py compilar --repo … --metaeditor … --salida … [--instalar …] [--etiqueta …] [--sustituir R V N] <fuente>…` (lo que implica D6) | Existe, pero hoy solo exporta `mql5/` (:95-111). Una vez cambiado, la sesión no puede lanzarlo (H5) | compilar.py:336-346 |
| C7 | `git push origin trabajo/f17-historial:refs/heads/fix/f17-historial` (D8) | Sí, en texto | RITUAL.md:103 |
| C8 | Skill `comparar-con-main` (D5) | Sí | .claude/skills/comparar-con-main |

El encargo no trae ningún otro comando `uv run botsito …`.

##### Lo que no pude comprobar

- Que la CI 45747377112 esté en verde: no está en el repo y no consulté `gh`.
- Que el encargo esté copiado tal cual: no tengo el original.
- Varios comportamientos de MT5 que no están en el repo y que ADR-0082 D7 pide citar o medir:
  - si `CopyTicksRange` en el terminal devuelve ticks guardados o generados;
  - si descarga a la caché del terminal el historial del rango pedido (lo que tocaría el heredado 6);
  - cómo se sabe el primer tick disponible sin pedir ticks de otros meses (por ejemplo, alguna propiedad de serie del servidor);
  - si la M1 de `CopyRates` es BID;
  - si la profundidad del terminal es la del tester.
- Que la guardia niega `compilar.py` una vez cambiado: lo infiero del código (H5), no lo ejecuté.
- Si el servidor tiene ticks de los cuatro meses: es justo lo que mide la corrida.

##### Lo más grave

D3 se va a fijar por su sha256 antes de ver un tick, así que lo que esté mal se queda escrito. Y su definición de los días se apoya en algo falso. `arnes.dias_de_mercado` no da los días de mercado de un mes: recibe los días `dev` del trader y les carga la M1 de Dukascopy, incluida la de marzo y junio, que tienen días reservados (n.º 33, H1). Si se cambia por «todos los laborables», el cierre de FTMO del 1 de enero hace que enero no cubra aunque los datos estén bien (H2). El yaml tiene que definir los días con el calendario de cierres, o con la cobertura de la M1, antes del sha.

Segundo, D1 confía en el punto (c) para cazar ticks fabricados, y (c) no puede: unos ticks hechos a partir de la M1 cuadran con ella por construcción, y (a) tampoco los distingue (n.º 34). Es la cautela central de ADR-0099 §5, y le falta al criterio un discriminador fijado antes.

Tercero, el recuadro de D7 escribiría en un ADR una atribución falsa: ADR-0090 §7 habla del deslizamiento, no del spread, y ADR-0099 §5 se lo da a la medida de las órdenes stop de la segunda rama, no a esta (n.º 44).

Además:
- D1 se contradice: «el primer tick disponible» frente a «se niega a cualquier otro mes sin pedir nada» (n.º 27).
- La compilación de D6 la lanzará Aleks con «!» sí o sí (H5).
- El arreglo de D5 choca con una `CuentaDelTramo` que hoy es mensual, y con que la cuenta arrastrada de §5 todavía no existe en el motor (n.º 15 y 17; H11).

Propongo que la PARADA lleve las tres primeras como preguntas al consultor antes de escribir `docs/plan/F17-HISTORIAL.yaml`.

## Informe del revisor (subagente `revisor`, 2026-11-26), tal cual

Copiado tal cual, con sus títulos bajados dos niveles y con una clase de retiradas, por holdout: las
fechas de días de meses con días reservados (marzo, mayo y junio de 2026) que citaba de los tests y
del borde del mes: nueve retiradas, siete como «[fecha retirada]» y dos, de una lista de fechas,
como «[fechas retiradas]». Sus números de línea son los
del árbol que revisó (`531e4318`).

#### Informe del revisor · trabajo/f17-historial · 2026-11-26

Revisado sobre `531e4318`, con el árbol limpio. El último `make check` (`make-check.log`) sella el árbol `d42533cd0d402b456d65a436568aed6bcc024475`, que es `git rev-parse HEAD^{tree}`. El log dice «3685 passed, 6 xfailed in 1351.93s», y su línea `PICO DE MEMORIA` da 321 MiB en `test`.

**Lo más importante:** la rama no está lista. Hay un **bloquea** en el eje (b): el exportador puede pedir ticks de un mes que no es de construcción si `InpDesde` lleva una hora. Además, el run de la CI no está en el informe y la tabla de §7 lo da por hecho.

##### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El mes se decide por la fecha del servidor, y eso no está declarado.** El fichero del primer día de abril y el de julio trae ticks y M1 de las últimas 3 h UTC del [fecha retirada] y del [fecha retirada]. El lector lee esas filas y nadie las cuenta. Ni el informe ni el yaml dicen en qué reloj se define el mes. Por ADR-0021 §1 son velas y se pueden leer, pero se declaran por recuento. Además, la respuesta a la PARADA 1, punto 0, dice «Nada lee la M1 de marzo ni de junio». | `tools/mql5/ExportarTicksFTMO.mq5`:128-129 y :164: el día va de las 00:00 a las 24:00 del servidor. El registro da servidor = UTC + 120 + verano `us`, así que el 1-abr y el 1-jul van a UTC+180: las 00:00 del servidor son las 21:00 UTC del día anterior. `scripts/leer_historial_f17.py`:703-706 lee todas las filas del CSV. El yaml (`docs/plan/F17-HISTORIAL.yaml`:9) solo dice «meses: los de construccion». El encargo, :71. Enero no se ve afectado: está cerrado del 31-dic 16:55 NY al 1-ene 17:05 NY (`ftmo-2step-swing-100k.yaml`:44-48). |
| a2 | importa | **Las líneas (e) ACORTADA de §5 incumplen la regla de la cita.** Dos de las cinco solo dan sus bytes «Después» si se quita la cita de su informe. `docs/state/README.md` exige conservarla («Si la línea citaba su informe con su sección, el paréntesis conserva esa cita delante»). Con las dos citas, el margen baja en 88 bytes: 820 en el mejor caso, no 908. El informe tampoco da el texto de ninguna línea acortada, así que nada se puede comprobar a la letra. | Medido sobre `git show main:PROJECT_STATE.md`. La línea :113 («Sin git callan…») cita `docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1`; su único corte válido, con la cita y la cola, da 207 bytes. Sin la cita da 157, que es lo que dice el informe (`F17-HISTORIAL.md`:1041). La línea :114 («RN-029…») cita `REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4`; con la cita da 158, sin ella 120, que es lo del informe (:1042). Regla: `docs/state/README.md`:81-86. |
| a3 | importa | **Ningún guion que escribe se ensayó en un clon desechable.** Aleks lanzó `compilar.py herramienta` y el lector con `--salida` directamente en el repo. El primero escribe `.log` en `docs/validation/anexos/` (`compilar.py`, `_herramienta`); el segundo escribe `control-d1.txt`. CLAUDE.md, «Ensayos aislados» 1, y la lección del encargo (:15) lo piden. El informe no lo declara como desviación. Los dos sacan la ruta de un argumento, así que la regla 2 sí se cumple. | `F17-HISTORIAL.md`:583 y :588 son los comandos sobre `.`. `grep -n -i "clon\|worktree\|ensay"` en el informe solo encuentra el clon de `main` de D5 (:261, :443). |
| a4 | menor | **Tests con fechas de marzo y mayo de 2026.** Son instantes sintéticos para los cambios de hora, sin etiqueta ni precio. Marzo es un mes reservado entero, y había años sin reserva para el mismo cambio de hora. | `tests/unit/test_leer_historial_f17.py`:68, :71, :73, :75 y :99-101: [fechas retiradas]. `tests/unit/test_metodo_adr0092.py`:388: [fecha retirada]. |

Comprobado sin hallazgos:
- **El contrato.** `scripts/contrato_rama.py` da «CONTRATO: 28 ficheros dentro del contrato de trabajo/f17-historial (riesgo medio, …, tramo 'R4', 4 comprobaciones para el revisor)» y «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-26 para trabajo/f17-historial, estadiada». `botsito state check` da OK. `knowledge validate` (salida fuera del repo) sale con 0, con todos los OK («1255 documentos: todo id citado existe…»; manifiestos, feedback y evidencia con su historial intacto). `make check` está sellado sobre HEAD, como arriba.
- **Los trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`.
- **El holdout.** Nada bajo `knowledge/`, `data/` (salvo `data/manifests/README.md`) ni `corpus/`. Hay cuatro filas de HOLDOUT, dos del 25 y dos del 26, cada una con su rama y su contenido. Ninguna nombra un día reservado: la de EA-CONEXION dice «un mes que hoy es reservado». No se ha leído ningún dato de FTMO. Los anexos solo traen rutas temporales y recuentos (`control-d1.txt`).
- **Los regímenes de cambio.** No hay `A` ni `M` en evidence, feedback, transcripciones, fotogramas ni `libros.yaml`. Bajo `data/manifests/` solo cambia el README, que el encargo permite y que no es un `.yaml`. HISTORIA solo se amplía.
- **Ambigüedades y spec.** Sin cambios. No hay ningún sitio nuevo con `cita`.
- **El ADR.** El de ADR-0090 es un recuadro junto a §7, con fecha y rama, y el cuerpo está intacto: el diff solo añade líneas. Su `## Estado` no se toca. No hay ningún ADR nuevo.
- **Diff vacío en lo protegido.** `git diff --stat main...HEAD` sale vacío para `engine/`, `domain/`, `spec/`, `knowledge/{spec,evidence,feedback,simulador,corpus,cuentas}`, `mql5/`, `MedirDemoFTMO.mq5` (sha `f9903c6f…`, el mismo que en `main`), `data/manifests/{demo_ftmo,ticks}`, `test_manifiestos_demo_ftmo.py`, `test_capa_mt5.py`, `test_medir_demo_ftmo.py`, `PREMISA-COSTES.yaml`, `PUENTE-TECHO.yaml`, `HOJA-DE-RUTA.md`, `MASTER_PLAN.md`, `cableado.py` y `test_cuenta_por_mes_metodo.py`.
- **Las citas del informe.** Comprobé estas contra su fuente:
  - `criterio_fidelidad.yaml`:47, que es la lista `construccion`;
  - el calendario de cierres, :21-22 (`cubre`), :31-33 (el cierre diario) y :44-48 (el 1 de enero);
  - `data/ticks.py`:436-440, que es la `seleccion`;
  - PROJECT_STATE :100, de 196 bytes;
  - las `horas.presentes` de los manifiestos de Dukascopy: 184, 182, 114 y 186.
- **Los bytes del cierre.** El PROJECT_STATE de `main` tiene 24.854 bytes. Medí: la F +63, el heredado 10 +31 o −67, y el «Antes» de las cinco líneas (e) (280, 347, 362, 234 y 220).
- **Las dos respuestas del consultor.** El encargo y el informe las copian igual (`diff` vacío).

##### Eje (b) · Encargo
Resumen: 1 bloquea, 5 importa, 2 menor. Requisitos: 43 hechos (y 3 de otra forma, declarados), 5 parciales, 2 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | §0 Base comprobada (main, origin, tag, CI, ninguna otra rama) | Hecho | informe :12-23 |
| 2 | §0 Apertura: encargo, contrato (tramo R4) y Archivo | Hecho | `fdc18717`; `contrato.yaml`:4; `state check` OK |
| 3 | §0 Ningún ADR nuevo | Hecho | no hay `A` en `docs/adr/` |
| 4 | §0 Lista blanca; nada fuera de lo protegido | Hecho | contrato_rama: 28 ficheros dentro |
| 5 | §0 Fila de HOLDOUT antes del primer make check | Hecho | filas del 25 y del 26; G2 OK |
| 6 | §0 «La herramienta X da Y», citado o por medir (ADR-0082 D7) | Parcial | b5 |
| 7 | §0 El guion que escribe, ensayado antes en un clon | No hecho | hallazgo a3 del eje (a) |
| 8 | §0 La guardia negó compilar y el lector: lo lanzó Aleks con «!» | Hecho | §3.2, §4, §4.1 |
| 9 | 0.1 La fila con el recuento de EA-CONEXION | Hecho | la primera fila del 25 |
| 10 | 0.2 Lo leído, con fichero:línea | Hecho | §0.2 |
| 11 | 0.3 El auditor | Hecho | §0.3 y su anexo |
| 12 | §4 La PARADA | Hecho | `4661575d` |
| 13 | D1 Ninguna función de trading, comprobado por el contrato | Hecho | `test_exportar_ticks_ftmo.py`:62-64 y mutaciones :106-117 |
| 14 | D1 Se niega fuera de DEMO con la condición de la :759 | Hecho | test :88-89 |
| 15 | D1 Solo EURUSD | Hecho | test :82-84 |
| 16 | D1 Ticks y M1 por día, a `MQL5/Files` | Hecho | `.mq5`:125-180 |
| 17 | D1 La profundidad (corregida por el punto 1) | De otra forma, declarado | §3.4 |
| 18 | D1 Ningún otro mes: «se niega sin pedir nada» | **Parcial** | b1 |
| 19 | D1 Control con TimeTradeServer y TimeGMT | Hecho | `.mq5`:212-226 |
| 20 | D2 Del servidor a UTC sin cifras; tests a los dos lados, EE. UU. y Europa | Hecho | test :64-114; en pytest, 110 passed |
| 21 | D2 Compara el control con el registro | Hecho (test débil) | b4 |
| 22 | D2 Se niega a un mes que no es de construcción, por el nombre, antes de abrir | Hecho | lector :598-605; test :151-163 |
| 23 | D2 Los puntos de D3 y el veredicto | Hecho | lector :290-385 y :564-578 |
| 24 | D2 Spread por hora y diferencia mediana, como diagnóstico, «sin elegir» | Hecho (el yaml añade una regla de elección) | b2 |
| 25 | D2 Ningún precio en la salida | Hecho | lector :564-578 y :712-725 |
| 26 | D3 El yaml antes de cualquier tick, fijado por su sha256, con un test que rompe | Hecho | `3ce320e6` (00:41) es anterior a `81c89ea0` y a la fila del control (d1); `sha256sum` da `46af1341…`, el del test; test :119-127 |
| 27 | D3 El control (d1) sobre Dukascopy | Hecho | `control-d1.txt`: los cuatro PASAN |
| 28 | PARADA 2: el yaml en su commit, a la vista; el (d2) nuevo con un sintético que rompe | Hecho | `802c159f` (1 línea del yaml y el sha); `test_d2_compara_solo…` |
| 29 | D4 El esquema `f17/` en el README y su test sintético | Hecho | `data/manifests/README.md`:80-107; `test_manifiestos_f17.py` |
| 30 | D4 El runbook | Hecho | `docs/runbooks/F17-HISTORIAL.md` |
| 31 | D5 `cuentas_con_deslizamiento` y `veredicto_con_f17` por cuenta, por la etiqueta | Hecho | `criterio_fidelidad.py`:870-898 y :917-956; agrupan por la pertenencia del día a la curva recibida, nunca por el mes |
| 32 | D5 Tests de dos cuentas y de una arrastrada | Hecho | `test_metodo_adr0092.py`:359-384 |
| 33 | D5 Rompe en `main` por la firma; uno de contenido si se puede | De otra forma, declarado | §1.4 :259-261; §3.3 :443 |
| 34 | D5 Los tests de hoy, adaptados y explicados | Hecho | §3.3 :437-438 |
| 35 | D5 Sin tocar `CuentaDelTramo` ni `cableado.py`; el constructor de la arrastrada falta | Hecho | diff vacío; §3.3 :434 |
| 36 | D6 Camino aparte; `exportar` e `instalar` sin cambios; tests en los dos sentidos | Hecho | el único `-` de `compilar.py` es la línea del despacho |
| 37 | D6 Los dos compilan sin errores ni avisos; logs en los anexos | Hecho | «Result: 0 errors, 0 warnings»; el sha del log es el del fuente |
| 38 | D6 El `.ex5` no se versiona | Hecho | `.gitignore` `/tools/mql5/*.ex5` |
| 39 | D6 El diff revisado antes de compilar | De otra forma, desviación declarada | «Cómo se aplica» :675-680 |
| 40 | D7 Los dos README | Hecho | diff |
| 41 | D7 El recuadro de ADR-0090 §7, en su commit y con el cuerpo intacto | Hecho | `531e4318` |
| 42 | D8 La CI por `fix/f17-historial`, con el número del run | **Parcial** | b3 |
| 43 | §6 La F y la A.5, con sus bytes | Hecho | §5 |
| 44 | §6 Los textos «grabador»; la fila de MASTER_PLAN no se toca | Hecho | §5 |
| 45 | §6 El recorte para dejar ≥1.000 bytes | Parcial, declarado (y el margen es menor: a2) | §5 :1050-1054 |
| 46 | Punto 6: la línea para R6a.8 | Hecho | §5 :1024-1026 |
| 47 | Punto 7: las tres rutas del contrato; `test_no_unexpected_ignored_paths` en verde | Hecho | `contrato.yaml`:25-27; make check en verde |
| 48 | §7 La PARADA y su respuesta, tal cual | Hecho | `diff` vacío |
| 49 | §7 «Las desviaciones» | Parcial | b6 |
| 50 | §7 La fila de ERRORES, preparada | Hecho | §6, con 4 columnas |
| 51 | §7 El revisor pegado y la frase final | No hecho (es lo que falta) | — |
| 52 | PARADA 2, punto 2: el diff de `compilar.py` y del `.mq5`, en el informe | Hecho | §4 y §4.3; copia igual al fichero (sha `5359f686…`) |
| 53 | PARADA 1, punto 0: parar si el calendario no cubre | Hecho (medido) | informe :384-388 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | **bloquea** | **El exportador puede pedir un mes que no es de construcción.** `RangoDeConstruccion` solo mira el instante `desde`, `desde+86400`… a la hora del día que traiga `InpDesde`. En cambio, `ExportarTicks` y `ExportarM1` piden de `d` a `d+24 h`. Con `InpDesde = InpHasta = "2026.08.31 06:00"` el rango pasa, porque es agosto, y la petición llega al 1-sep 05:59 del servidor. Pasa lo mismo con el 31-ene y febrero (heredado 6). `StringToTime` acepta la hora; la capa del repo la usa así. El contrato no lo caza: solo exige que `EsDeConstruccion` aparezca en el cuerpo y que las llamadas directas vayan después. Hasta ahora lo evita solo el runbook, que da fechas sin hora. | `tools/mql5/ExportarTicksFTMO.mq5`:41-42 (entradas `string` libres), :113-114, :128-129, :164, :192-193 y :235 (ninguna normalización a las 00:00). `mql5/Scripts/BotsitoPruebasCapa.mq5`:95 (`T("2026.10.26 23:51:58")` → `StringToTime`). `tests/contract/test_exportar_ticks_ftmo.py`:72-73 y :75-81. Encargo :39 («cualquier otro mes, se niega sin pedir nada»). |
| b2 | importa | **El yaml pre-registrado lleva una regla de elección que nadie dio.** `diferencia_mediana.lectura` dice qué fila del puente «vale» («cuyo número sea el mayor que no pase de su valor absoluto»). D2 decía «sin elegir», y el punto 3 de la respuesta solo dice que es la que «se compara». Ahora queda fijada por el sha256, y el informe no la declara. | `docs/plan/F17-HISTORIAL.yaml`:48. Encargo :40 y :77. `grep "mayor que no pase"` solo la encuentra en el yaml. |
| b3 | importa | **La CI de D8 y el Estado del informe.** D8 pide el número del run, y el informe no lo trae. La fila 20 de §7 dice «Hecho» y remite a §8, que es «Lo que necesito que decidas en la orden de cierre», sin CI. La fila 4 dice «Hecho» al ensayo en un clon, que no se hizo (a3). El `## Estado` dice que falta el recuadro de ADR-0090 §7, ya commiteado en `531e4318`. | `F17-HISTORIAL.md`:1069, :1085, :1089-1097 y :1226-1227. `git ls-remote --heads origin` da `531e4318… refs/heads/fix/f17-historial`. `gh run list --branch fix/f17-historial` da el run `45797145889`, `in_progress`. |
| b4 | importa | **El test del control no prueba el caso «no cuadra».** Su segunda aserción comprueba que `int("120") != 180`, que es cierto por la entrada misma. La comparación `csv_d == reg_d` del lector (:696) no la ejerce ningún test. | `tests/unit/test_leer_historial_f17.py`:124-126. `scripts/leer_historial_f17.py`:479-483 y :695-697. |
| b5 | importa | **«Cuántos devuelve por llamada» no está ni citado ni por medir.** D1 lo nombra entre lo que se cita o se mide, y no aparece en ninguna de las dos listas. El informe cita `ERR_HISTORY_TIMEOUT` («the function has sent all it had»): un día parcial queda en el control (`dia_*_error`), pero el lector no lee esas filas. Un mes corto daría «NO CUBRE» sin decir por qué. | Encargo :39. `.mq5`:21-26 y :238-243. Informe :138-139 y :204-205. Lector :689-691 (solo `digits`, `time_gmt_s` y el desfase). |
| b6 | importa | **No hay sección de «las desviaciones».** §7 del encargo la pide. Las dos de la PARADA 2 están declaradas sueltas («Cómo se aplica»), pero no las reúne nada. Faltan a1 (el mes por la fecha del servidor) y b2 (la regla de elección). | Encargo :57. Los títulos del informe (`grep "^## "`): ninguno de desviaciones. |
| b7 | menor | **La hora repetida y la que no existe solo se prueban con `us`.** Con `eu` solo se prueban los dos lados. | `tests/unit/test_leer_historial_f17.py`:91-101. |
| b8 | menor | **Restos de forma en el informe.** Queda la línea de PLANTILLA de la apertura y hay dos `## 5.`, el de la PARADA y el de las líneas del cierre. Además, `data/manifests/README.md`:90-92 dice que el lector «lo valida», pero su CLI no llama a `validar_manifiesto`: lo valida el test. | `F17-HISTORIAL.md`:3, :299 y :989. `scripts/leer_historial_f17.py`:581-625. `test_manifiestos_f17.py`:126-128. |

##### Lo que no pude comprobar
- **Si la CI de `fix/f17-historial` acaba verde con el único fallo de `state check`.** El run 45797145889 estaba `in_progress` a las 09:59 UTC.
- **Si el [fecha retirada], el [fecha retirada], el [fechas retiradas] o el [fecha retirada] son días de una partición** (a1, a4). No abrí `casos_reservados` ni nada protegido; marzo es un mes reservado entero según CLAUDE.md.
- **Si `CopyTicksRange` tiene un tope por llamada, y el comportamiento real de `StringToTime`** más allá de su uso con hora en la capa. No consulté la documentación de MQL5.
- **Si la fila de HOLDOUT del 25 se estadió antes del primer `make check`.** Solo veo los commits, no el orden real de las ejecuciones.
- **Que el encargo esté copiado tal cual del mensaje original.** No tengo el original.
- **El texto «Después» de las cinco líneas (e).** El informe no lo trae; a2 sale de la aritmética de bytes sobre los únicos cortes válidos.
- **La compilación.** No ejecuté `make check`, `compilar.py` ni el lector sobre datos (son comprobaciones que escriben): lo sustituyen `make-check.log` (SELLO y PICO), los anexos de la compilación y `control-d1.txt`.

##### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff --name-status main...HEAD`
3. `uv run python scripts/contrato_rama.py`
4. `gh run list --branch fix/f17-historial --limit 3`; `git ls-remote --heads origin`
5. `grep -n "SELLO\|PICO DE MEMORIA\|passed\|failed\|error" make-check.log`; `git rev-parse HEAD^{tree}`
6. `uv run botsito state check`
7. `uv run botsito knowledge validate` (salida a un temporal fuera del repo)
8. `uv run pytest -p no:cacheprovider tests/contract/test_exportar_ticks_ftmo.py tests/unit/test_leer_historial_f17.py tests/unit/test_f17_historial_criterio.py tests/unit/test_manifiestos_f17.py tests/unit/test_compilar_mql5.py tests/unit/test_metodo_adr0092.py -rA` → 110 passed
9. `git log --reverse --format='%h %ad %s' --date=iso main..HEAD`; `git show --stat` de los ocho commits
10. `git show 802c159f -- docs/plan/F17-HISTORIAL.yaml tests/unit/test_f17_historial_criterio.py`; `sha256sum docs/plan/F17-HISTORIAL.yaml`
11. `git diff main...HEAD --` sobre `criterio_fidelidad.py`, `compilar.py`, `test_metodo_adr0092.py`, `HOLDOUT-EXPOSICIONES.md`, `PROJECT_STATE.md`, `docs/adr/`, `.gitignore`, los tres README y `data/manifests/README.md`; `git show 0dabbeab -- HOLDOUT-EXPOSICIONES.md`
12. `git diff --stat main...HEAD --` sobre las rutas protegidas de §2 (vacío; la guardia negó la primera forma, que llevaba `corpus/`, y la repetí sin él)
13. `git diff --name-only main...HEAD | grep -E '^(knowledge|data|corpus)/'`
14. `git diff main...HEAD | grep '^+' | grep -oE` fechas de meses que no son de construcción; `git grep` de sus contextos
15. `git show main:PROJECT_STATE.md | wc -c` y `sed -n Np | wc -c` de las líneas 28, 57, 96, 99, 100, 101, 113 y 114; `printf … | wc -c` de las líneas propuestas
16. `grep presentes data/manifests/ticks/*.yaml`; `sed` del calendario de cierres, de `criterio_fidelidad.yaml`:47 y de `data/ticks.py`:430-442
17. `diff <(sed …encargo) <(sed …informe)` de las dos respuestas del consultor
18. `head`/`tail` de los anexos; `sha256sum` de los dos `.mq5`
19. Read de: encargo, contrato, informe entero, `ExportarTicksFTMO.mq5`, `leer_historial_f17.py`, `test_exportar_ticks_ftmo.py`, `test_leer_historial_f17.py` (parcial), `test_f17_historial_criterio.py` (parcial), `test_manifiestos_f17.py` (parcial), `F17-HISTORIAL.yaml`, el runbook, `docs/state/README.md`:55-95 y `BotsitoPruebasCapa.mq5`:50-69

## Informe del revisor, segunda pasada (subagente `revisor`, 2026-11-26), tal cual

Acotada a `git diff 958ffec3 ed2a15de`, como pidió la respuesta a la PARADA 3. Va copiada tal cual,
con sus títulos bajados dos niveles y sin su última línea, la lista de ficheros revisados con su
ruta absoluta de la máquina, que son los de sus comandos. Sus números de línea son los de
`ed2a15de`. Las «[fecha retirada]» son suyas.

#### Lo que se hizo con sus hallazgos

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado**: las fechas de borde de marzo y junio se escriben como «el último día de marzo» y «el último día del mes anterior (de marzo y de junio)», también en §11, que venía de `958ffec3`. |
| a2 | menor | **Arreglado**: dice «el docstring de `leer_ticks`», no «la cabecera del lector». |
| a3 | menor | **Arreglado**: el recuadro de §4.3 recoge el añadido «(dia_*_ticks y dia_*_error)» y el comentario de `InicioDelDia`. |
| b1 | importa | **Arreglado**: la pregunta de cierre de la PARADA 3 vuelve como §11.1, tal como se hizo. Los punteros de §5 van a «§11.1, decisión 0/1; decidido en §12». |
| b2 | importa | **Arreglado**: §12 trae a la letra las tres acortadas, los seis cambios de la hoja de ruta y la fila F:F17 entera, con su columna de prueba. |
| b3 | menor | **Arreglado**: la lectura del mes sale a `leer_mes_ftmo` y la línea a `linea_descartes`, que `leer_historial` llama. El test los recorre sobre la carpeta y comprueba la línea; espera `InvalidOperation`, no cualquier excepción. |

#### Informe del revisor · trabajo/f17-historial · 2026-11-26 (segunda pasada, acotada a `git diff 958ffec3 ed2a15de`)

**Lo principal:** ningún hallazgo bloquea. Hay 3 importa: uno en el eje (a), sobre fechas de meses reservados escritas en el informe, y dos en el eje (b), sobre lo que se hizo con la decisión de cierre de la PARADA 3. Los pasos que dan la rama por terminada todavía no se pueden hacer: la CI de `ed2a15de` (run **45833012704**) sigue **en curso**.

Datos de partida:
- Revisado el commit `ed2a15de`, con el árbol limpio.
- `make-check.log` sella `e82b9182c1ed53c04e40314cc2ac048e51dc359a`, que es `git rev-parse ed2a15de^{tree}`. El log dice «3690 passed, 6 xfailed», sin ningún `failed`. `PICO DE MEMORIA`: 322 MiB en `test`.

##### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El texto nuevo escribe en claro las fechas de borde de marzo y de junio de 2026 que la propia rama retiró por holdout.** La cabecera del informe del revisor pegado dice que retiró «las fechas de días de meses con días reservados (marzo, mayo y junio de 2026) … del borde del mes». Esas fechas son justo las mismas. Se puede decir lo mismo sin la fecha, por ejemplo «las últimas horas UTC del mes anterior». La misma forma ya estaba en §11:1171-1172, que viene de `958ffec3` y por tanto queda fuera de esta pasada. | En `git show ed2a15de:docs/validation/F17-HISTORIAL.md`, :1236-1237 dice «baja también las últimas dos o tres horas UTC del [fecha retirada] y del [fecha retirada]». Frente a eso, :1398-1400 da el criterio de retirada, y :1415 las retira en el hallazgo a1 de la primera pasada. |
| a2 | menor | **«Lo dicen también el runbook y la cabecera del lector» no es verdad para la cabecera.** El docstring de módulo de `scripts/leer_historial_f17.py` (:1-27) no se tocó y no habla del descarte. Lo explica el docstring de `leer_ticks` (:467-469). | `F17-HISTORIAL.md`:1233. `grep -n -i "mes utc\|borde\|descart"` sobre el script solo da :465-495 y :754-764. |
| a3 | menor | **El recuadro de §4.3 no recoge todo el cambio de la 1.01.** Dice que la cabecera «añade «cuántos devuelve CopyTicksRange en una llamada»». No dice que también añade «(dia_*_ticks y dia_*_error)», ni el comentario que va sobre `InicioDelDia`. El puntero al diff entero sí está, así que no se pierde nada. | `git diff 531e4318 958ffec3 -- tools/mql5/ExportarTicksFTMO.mq5`: la línea `+//\| con el control (dia_*_ticks y dia_*_error) y con (c) y (d).` y las tres líneas `+// Las 00:00 del dia del servidor…`. El recuadro está en `F17-HISTORIAL.md`:689-703. |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da «CONTRATO: 28 ficheros dentro del contrato … 4 comprobaciones para el revisor» y «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-26 para trabajo/f17-historial, estadiada», con exit 0.
- **Las demás comprobaciones del contrato.**
  - `uv run botsito state check` da «OK: rama 'trabajo/f17-historial' …», exit 0.
  - `make check`: su evidencia es el log de arriba.
  - `knowledge validate` no lo ejecuté (ver «Lo que no pude comprobar»).
- **Trailers `Fuente:`.** No aplican: el commit no toca `knowledge/spec` ni `knowledge/cases`. `git diff --name-status 958ffec3 ed2a15de` da 8 ficheros, todos `M`, ninguno en esas carpetas.
- **Holdout y material.** El commit no toca `knowledge/cases/holdout/`, ni evidencia, ni feedback, ni manifiestos, ni transcripciones, ni fotogramas. No declara ninguna lectura nueva de material. La fila del día existe (G2).
- **Regímenes, ambigüedades, ADR y tres guardias de una `cita`.** No aplican: el diff no toca nada de eso.
- **Informes cerrados.** `F17-HISTORIAL.md` y los anexos son de la rama (`A` contra `main`).
- **Los sha de los logs nuevos.**
  - `ExportarTicksFTMO.mq5`: `git show ed2a15de:…`, `git show 958ffec3:…` y `git show :…` dan los tres `eb9ccdb99043932c82362cd0fba8a880daf1f9f721348d8ec563a7151ad79b6c`. Es el que trae `ExportarTicksFTMO.log`:1, y el fichero lleva `#property version "1.01"` y `VERSION_SCRIPT "1.01"`.
  - `MedirDemoFTMO.mq5`: da `f9903c6f…59151`, igual que su log:1.
  - Los dos logs dicen «PASA (0 errores, 0 avisos, .ex5 si)».
- **Cifras.** El lector nuevo no mete ningún literal de negocio: `mes_utc` solo formatea con `%Y-%m`.
- **PROJECT_STATE.** El recuento pasa de 2187 a 2188, que es +1 por el test nuevo.
- **Bytes de §12, medidos con `printf | wc -c`.**
  - La F vieja tiene 153 bytes y la corta 117: −36.
  - El heredado 10 tiene 67 bytes y la línea :100 tiene 196, los dos con salto.
  - 24.854 − 36 − 67 − 196 − (69 + 112 + 207) = **24.167**, es decir, un margen de **833**.
  - Los tres textos citados son literales de `git show main:PROJECT_STATE.md` en :28, :57 y :100.

##### Eje (b) · Encargo (respuesta del consultor a la PARADA 3)
Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 11 hechos, 2 parciales (uno de ellos «hecho de otra forma» sin declarar), 1 no hecho todavía (pendiente por orden del encargo).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Commitear los logs nuevos de la compilación revisada, con su `make check` | Hecho | Los dos `.log` cambian en `ed2a15de`, con sha y rutas temporales nuevas. El sello es el de arriba. Los sha casan con el `.mq5` 1.01 del índice (eje a). |
| 2 | El exportador sigue pidiendo días del servidor | Hecho | `git diff 958ffec3 ed2a15de -- tools/` sale vacío. |
| 3 | El lector pasa cada tick y cada M1 a UTC y descarta lo que cae fuera del mes UTC pedido, sin usarlo | Hecho | `leer_historial_f17.py`:472-477 y :492-496: calcula `reloj.a_utc` y, si `mes_utc(utc) != mes`, cuenta la fila y hace `continue` antes de llamar a `a_puntos`. :756 y :758 pasan `mes`. El precio solo llega a memoria como texto, en el `DictReader` de `_filas`, :433-439, y nunca se convierte ni se usa. |
| 4 | Lo cuenta en su salida, por mes vecino y en número de filas | Hecho | :762-765 escriben la línea «DESCARTADAS sin usar (fuera del mes UTC pedido; para HOLDOUT, por recuento): N filas de ticks del AAAA-MM, …», o «ninguna». Las claves de :475 y :495 ya llevan el mes. |
| 5 | La fila de HOLDOUT del día de la corrida lo declara por recuento | Hecho, como instrucción (la corrida no se ha hecho) | `docs/runbooks/F17-HISTORIAL.md`:70-73. El texto de la línea DESCARTADAS lo recuerda. |
| 6 | Test sintético que rompe a propósito: un tick de la última hora UTC del mes anterior en el fichero del día 1 no entra en ninguna cuenta y sí en los descartes | Hecho | `test_las_filas_de_otro_mes_utc_se_descartan_sin_leer_su_precio`, `tests/unit/test_leer_historial_f17.py`:164-197. El precio del tick y de la M1 del borde es ilegible, y sin `mes` el lector falla (:196-197). Es de 2027, sin meses reservados. `uv run pytest tests/unit/test_leer_historial_f17.py -q` pasa, exit 0. |
| 7 | Corregir en el informe la frase «Nada lee la M1 de marzo ni de junio» con lo que pasa de verdad | Hecho | La corrección está en `F17-HISTORIAL.md`:1162-1165 (§10.7) y :1234-1239. La copia literal de la PARADA 1 no cambia: la sección de «Respuesta del consultor a la PARADA (2026-11-26)» hasta «## 3.» tiene el mismo sha256 en `958ffec3` y en `ed2a15de` (`8e2e20cc…`). Lo que se dice de `dias_del_mes` es cierto (:148-176, sin `arnes`). La forma de las fechas es el hallazgo a1 del eje (a). |
| 8 | Punto 1: declarar en el informe la regla de elección del yaml | Hecho | Desviación 6 de §10 (:1160-1161) y :1240-1242. |
| 9 | El yaml no cambia más | Hecho | `git diff 958ffec3 ed2a15de -- docs/plan/` sale vacío. |
| 10 | Cierre: el heredado 10 por (b), la F corta, margen 833 | Hecho | §12, :1246-1259. Los bytes están medidos en el eje (a). |
| 11 | «deja los textos a la letra en §12» | Parcial (hecho de otra forma, sin declarar por qué) | §12 da a la letra la F, el heredado 10 y la :100. Para las tres «(e) ACORTADA» dice «quedan como en la tabla de §5, a la letra», y para la hoja de ruta «como en §5» (:1266-1269). Además, la fila F:F17 de §5 no es literal en su columna de prueba: «con `F17-HISTORIAL.md` añadido en su columna de prueba», :1040-1042. |
| 12 | Copia tal cual en el informe, en su sección de la PARADA 3 | Hecho | Las líneas `>` de `F17-HISTORIAL.md`:1203-1219 y las del final del encargo dan el mismo sha256 (`55c852dc…`), 13 líneas. |
| 13 | Copia al final del encargo | Hecho | `docs/encargos/trabajo-f17-historial.md`:105-119. El diff solo añade líneas. |
| 14 | La CI de `fix/f17-historial` sobre el último commit, con su número y el único fallo esperado | Parcial (en curso) | `gh run view 45833012704 --json headSha,status` da `headSha` `ed2a15de7c87…` y `status` `in_progress`. El «Estado» del informe dice que falta, y es coherente. El run anterior, **45805382618**, se comprobó: «FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo» y «1 failed, 3592 passed, 102 skipped», como dice el Estado. |
| 15 | Terminar con «Rama lista para revisión, NO cerrada.» | No hecho (pendiente, va después de la CI y de esta pasada) | El Estado (:1539-1542) dice «EN CURSO». |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Se borró la pregunta de cierre de la PARADA 3 que el consultor contestó.** El antiguo «## 12. Lo que necesito que decidas en la orden de cierre» tenía las decisiones 0 y 1, con sus opciones, su coste y la recomendación. Se quitó entera y no se declara, aunque las PARADAs 1 y 2 conservan su «Lo que necesito que decidas» (:306 y :631). La respuesta («que el heredado 10 salga por (b) y con una F corta») ya no tiene sus opciones en el informe, salvo en parte en §5. Y un puntero queda colgando: §5:1022 dice «dos opciones (decisión 0, abajo)», y abajo ya no hay ninguna decisión 0 del cierre. Aparte, y desde antes de esta pasada: §5:1084 dice «(§11, decisión 1)», pero la decisión 1 de §11 es la del yaml. | Las líneas `-` del hunk `@@ -1178,17 +1200,73 @@` de `git diff 958ffec3 ed2a15de -- docs/validation/F17-HISTORIAL.md`. `grep -n "decisión 0\|decisión 1"` sobre `ed2a15de` da :1022 y :1084. |
| b2 | importa | **El requisito 11 está hecho de otra forma sin declararlo.** La respuesta pide los textos a la letra «en §12». §12 manda a §5 las tres acortadas y la hoja de ruta, y §5 no es literal en la fila F:F17. | `F17-HISTORIAL.md`:1266-1269 y :1040-1042. |
| b3 | menor | **El test del punto 0 solo prueba las funciones, no el recorrido entero.** Nada comprueba que `leer_historial` pase `mes` a `leer_ticks` y a `leer_m1` (:756, :758), ni la línea DESCARTADAS (:762-765). Si alguien quitara `mes, descartes` de esas dos llamadas, ningún test fallaría. Además, `pytest.raises(Exception)` (:196) acepta cualquier excepción. Era más preciso esperar `decimal.InvalidOperation`. | `grep -n "leer_historial(\|DESCARTADAS"` en `tests/unit/test_leer_historial_f17.py` no da ninguna línea. |

Lo que la rama hace y esta respuesta no pide, todo justificado:
- el recuadro de la 1.01 en §4.3, por la PARADA 2, punto 2 («el del `.mq5`»);
- el runbook, con la versión 1.01 y el párrafo del descarte, que «Cómo se aplica» nombra;
- el +1 de PROJECT_STATE, por el test nuevo.

La única cosa sin justificar es el borrado del antiguo §12 (b1).

**El informe de la primera pasada no se ha tocado.** «## Informe del revisor (subagente `revisor`, 2026-11-26), tal cual», hasta «## Estado», da el mismo sha256 (`6d29201c…`) en `958ffec3` y en `ed2a15de`. Lo mismo pasa con el informe del auditor (`d717f77b…`).

##### Lo que no pude comprobar
- **La CI de `ed2a15de`**: el run 45833012704 sigue en curso.
- **`uv run botsito knowledge validate`**: escribe su log, así que no lo ejecuté. Su evidencia es el `make check` sellado, que lo incluye.
- **Que la copia del encargo y la del informe sean literalmente el mensaje original del consultor**: solo pude comprobar que son iguales entre sí. El original no está en el repo.
- **Que la recompilación la lanzara Aleks después de la revisión del consultor**: solo lo dice la respuesta. Las rutas temporales nuevas de los logs muestran que es otra compilación, no cuándo se hizo.
- **El material protegido**: no abrí ni listé nada. No abrí `casos_reservados` ni ningún CSV de FTMO. La corrida del lector no existe todavía.

##### Comandos ejecutados
1. `git branch --show-current && git log --format='%h %s' 958ffec3..ed2a15de && git diff --stat 958ffec3 ed2a15de && git status --short`
2. `git diff 958ffec3 ed2a15de -- scripts/ tests/ PROJECT_STATE.md docs/runbooks/ docs/validation/anexos/`
3. `git diff 958ffec3 ed2a15de -- docs/encargos/`
4. `git diff 958ffec3 ed2a15de -- docs/validation/F17-HISTORIAL.md`
5. Grep `fecha retirada|fechas reservadas|…` en `docs/runbooks/`, y `sed -n` de las líneas 86, 102, 114, 118 y 135 de `ERRORES-RECURRENTES.md`
6. `git show ed2a15de:scripts/leer_historial_f17.py`, con `sed`/`grep` (cabecera, funciones, :130-180, :433-450, :670-770)
7. `grep` de la ventana en `docs/plan/F17-HISTORIAL.yaml`, `git diff --name-status 958ffec3 ed2a15de` y `git diff --name-status main...ed2a15de -- docs/plan/F17-HISTORIAL.yaml`
8. `git show <ref>:tools/mql5/ExportarTicksFTMO.mq5 | sha256sum`, con `ed2a15de`, `958ffec3` y el índice (el primer intento, con `for`, lo negó la guardia)
9. `git show ed2a15de:tools/mql5/MedirDemoFTMO.mq5 | sha256sum` y `grep` de la versión del exportador
10. `git diff 531e4318 958ffec3 -- tools/mql5/ExportarTicksFTMO.mq5`
11. `sha256sum` de las líneas `>` de la respuesta a la PARADA 3, en el encargo y en el informe
12. `grep` de «M1 de marzo», «borde», etc. en el informe, el encargo, el runbook y el yaml
13. Read de `F17-HISTORIAL.md`, :1-14, :1010-1089, :1120-1203 y :1396-1420
14. `git show main:PROJECT_STATE.md | sed -n '28p;57p;100p'`, `wc -c`, y `printf | wc -c` de las cuatro cadenas
15. `sha256sum` de la sección del revisor, de la copia de la PARADA 1 y del auditor, en `958ffec3` y en `ed2a15de`
16. `grep` de «decisión 0/1» y «§12» en el informe
17. Grep `ventana_inicio|ventana_fin` en `knowledge/spec/parametros.yaml`
18. `uv run python scripts/contrato_rama.py`
19. `grep SELLO/PICO/passed/failed make-check.log` y `git rev-parse ed2a15de^{tree} HEAD`
20. `grep comprobaciones contrato.yaml` y `git diff --name-status main...ed2a15de -- docs/validation/ knowledge/ data/manifests/`
21. `uv run botsito state check`
22. `uv run pytest tests/unit/test_leer_historial_f17.py -q -p no:cacheprovider`
23. `gh run list --branch fix/f17-historial --limit 4`, `gh run view 45833012704 --json headSha,status,conclusion` y `gh run view 45805382618 --log-failed | grep …`

## Estado

Hechas las tres PARADAs con su respuesta aplicada:
- el lector descarta y cuenta las filas de otro mes UTC;
- la regla del yaml, declarada;
- los logs de la 1.01, en los anexos;
- §12, a la letra.

Las dos pasadas del revisor, con sus hallazgos arreglados o declarados (§9 y «segunda pasada»). La
CI de `fix/f17-historial`, con el único fallo esperado de `state check` en cada run (§8). La del
commit que trae este «Estado», el de los arreglos de la segunda pasada, se da al entregar: este
fichero no puede llevar el número de un run que se lanza al empujarlo.

Rama lista para revisión, NO cerrada.
