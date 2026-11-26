# F17-HISTORIAL · El historial de ticks del servidor de la demo de FTMO, con sus herramientas y sin correr, y el ajuste por cuenta de F17 (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

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
punto (c)), y si los ticks son guardados.

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

## 5. PARADA

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

## Estado

EN CURSO: fase 0, PARADA.
