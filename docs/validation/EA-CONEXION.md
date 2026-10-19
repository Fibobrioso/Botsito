# EA-CONEXION · el primer EA de la capa de MT5 que no decide operaciones (R6a.1)

Rama `trabajo/ea-conexion`, tramo R6a de `docs/plan/HOJA-DE-RUTA.md` (R6a.1; ADR-0082). Encargo del
consultor del 2026-10-19, copiado tal cual en `docs/encargos/trabajo-ea-conexion.md`.

## Apertura

Base comprobada el 2026-10-19 (skill `abrir-rama`, paso 1), con git y con `gh`:

- `git rev-parse main origin/main` → `9c456292e9eb656ef523a89e9f5d5893482b4979` las dos veces.
- `git rev-parse "stable/F37w-barrido-sesion-5^{commit}"` → `ff55b3d3e313aae4fd0069ca0fee2431faf7b4a0`
  = `main^1` (el merge); el tag esta en origin (`git ls-remote --tags origin`).
- CI de `main` sobre su HEAD, con `gh run list --branch main --commit 9c456292e9eb656ef523a89e9f5d5893482b4979`:
  run 39314463754, `completed` / `success` (ni curl ni guion, por orden del consultor).
- `git branch --list` → solo `main`; `git ls-remote --heads origin` de `fix/*`, `trabajo/*` y
  `feature/*` → vacio.

`make check` del commit de apertura (`8ac24ed`): exit 0, 2690 passed, SELLO sobre el arbol
`6c46d41a`; `PICO DE MEMORIA de make check: 296 MiB en `test``.

## 0. Fase 0 (2026-10-19): inventario y medida, sin MQL5 de la capa

Todo lo de MT5 se midió en la máquina de Aleks el 2026-10-19, entre las 15:19 y las 15:30 de Lima
(UTC−5), con el MetaTrader 5 instalado y la cuenta de prueba de FTMO de octubre, con copias y guiones
de medida **fuera del repositorio** (en el scratchpad de la sesión). `tools/mql5/MedirDemoFTMO.mq5`
no se tocó. Los guiones de medida, sus salidas y los logs de compilación (convertidos a UTF-8 y LF, con
el sha256 del original) están en `docs/validation/anexos/EA-CONEXION/fase0/`. Ningún guion de medida
llama a una función de trading. Lo que dejaron en la carpeta de datos del terminal (los `.ex5` de
medida, sus ficheros y el informe del tester) se borró al terminar; quedan el caché de ticks y los logs
propios del terminal, fuera del repo.

Los logs del terminal (`logs/AAAAMMDD.log`) llevan el login y la IP de la conexión: **no se copian al
repo**; lo que se cita de ellos se cita con las cifras largas tapadas.

### 0.a Compilar

**Dónde está.** Un solo MetaTrader 5, genérico (no una instalación con la marca de FTMO): `C:\Program
Files\MetaTrader 5\` con `terminal64.exe`, `MetaEditor64.exe` y `metatester64.exe` (fechados el
2026-10-08, build 6230: `terminal_build|6230` en `fase0/medida.txt`). Una sola carpeta de datos,
`%APPDATA%\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\` (su `origin.txt` apunta a esa
instalación), con `MQL5\Scripts\MedirDemoFTMO.mq5` y `.ex5` y el CSV de la ejecución 1 en `MQL5\Files`.

**Hallazgo de paso:** el `MedirDemoFTMO.mq5` de la carpeta del terminal es de 31.200 bytes y del
2026-09-28 (sha256 `28d58110…7540`), y el `.ex5` se compiló el 2026-10-08 a partir de él; el del repo
(1.1) tiene 33.720 bytes. Es decir, **en el terminal sigue la 1.0**, que es lo que DEMO-FTMO.md ya
manda sustituir antes de la ejecución 2 («vuelve a copiar…»). No se toca: es del carril de Aleks (A.1);
lo anoto porque es justo la copia desincronizada que la ruta de compilación de abajo evita.

**La línea de órdenes, de la documentación oficial** (MetaEditor, «Integración con IDE»,
<https://www.metatrader5.com/en/metaeditor/help/beginning/integration_ide>, consultada el 2026-10-19):
`metaeditor64.exe /compile:"<ruta al fuente>"`; `/include:"<carpeta>"` — «Include files are searched
at: [specified directory]\include\[path from #include<...>]»; `/log` — «<source file name>.log
compilation log file is created in the folder containing the source file»; `/s` solo comprueba la
sintaxis. **La página no dice nada del código de salida, de la codificación del log ni de dónde deja el
`.ex5`**: eso lo medí.

**Medido** (con una copia de `tools/mql5/MedirDemoFTMO.mq5` en el scratchpad; el original, intacto):

| prueba | código de salida | `.ex5` | última línea del log |
|---|---|---|---|
| la copia de MedirDemoFTMO 1.1, `/compile:… /log:compilar-ok.log` | **1** | sí, junto al fuente (48.872 bytes) | `Result: 0 errors, 0 warnings, 1054 ms elapsed, cpu='X64 Regular'` |
| la misma con un error provocado (`int x = ;` en la línea 793) | **0** | no | `Roto.mq5(793,26) : error 157: expression expected` · `Result: 1 errors, 0 warnings` |
| un EA mínimo con `#include <Botsito/Prueba.mqh>`, sin `/include` | 0 | no | `error 106: file 'Include\Botsito\Prueba.mqh' not found` |
| el mismo, con `/include:"<…>\inc\mql5"` | 1 | sí | `information: including <…>\inc\mql5\Include\Botsito\Prueba.mqh` · `Result: 0 errors, 0 warnings` |

- **El código de salida va al revés de lo habitual**: 1 con éxito y 0 con error (en las cuatro
  pruebas). No sirve como puerta: la puerta tiene que leer la línea `Result: N errors, M warnings`
  del log y comprobar que existe el `.ex5`.
- **El log es UTF-16LE con BOM (`ff fe`) y CRLF**; el de `/log:<nombre>` se escribe con el nombre
  dado (no solo «<fuente>.log» como dice la página). El log general de MetaEditor
  (`logs/metaeditor.log`) y los del terminal, igual.
- **Compila desde cualquier carpeta** con `/include` apuntando a una carpeta que tenga `Include\`
  dentro: el `mql5/` del repo vale tal cual (`mql5/Include/Botsito/…`). Pero **deja el `.ex5` y el
  log junto al fuente**: compilar dentro del repo deja ficheros sin seguir (`.gitignore` no ignora
  `*.ex5`, y no está en las rutas de la rama) y `make check` no sella. Ver la propuesta de §0.f.
- Una compilación anterior por línea de órdenes ya está en el log general de MetaEditor (2026-09-28,
  tres veces, desde un scratchpad de otra sesión: `DEMO-FTMO-SCRIPT.md` §1 lo cuenta como
  «Compilado en esta máquina… fuera del repositorio»).
- **La guardia dejó ejecutar `MetaEditor64.exe` y `terminal64.exe`** con rutas del scratchpad. Con un
  `.mq5` de la rama como argumento no está medido (el auditor apunta que la guardia niega un fichero
  de la rama distinto del de `main` como argumento de un programa desconocido; herencia 7). La ruta
  de §0.f no pasa nunca un fichero de la rama a MetaEditor: le pasa la copia exportada.
- **Codificación del fuente: MetaEditor lee UTF-8 sin BOM.** `fase0/MedirFase0.mq5` está escrito en
  UTF-8 sin BOM y lleva el literal `"año|línea"`; el SHA-256 que calcula MQL5 sobre sus bytes UTF-8
  (`sha256_utf8|32:78ecdd95…b4d6`) es el que da Python sobre `"año|línea".encode()`. El precedente
  (MedirDemoFTMO) es ASCII puro (herencia 14 del auditor).

### 0.b Probar

**(1) Un script de pruebas en el terminal, lanzado por línea de órdenes: SÍ, y Claude Code puede
hacerlo.** De la documentación oficial («Platform start», <https://www.metatrader5.com/en/terminal/help/start_advanced/start>):
`terminal64.exe /config:<fichero.ini>` con una sección `[StartUp]` (`Script`, `Symbol`, `Period`,
`ShutdownTerminal` — «enable/disable trading platform shutdown upon completion of script operation»).
Medido: con `Script=Botsito_fase0\MedirFase0`, `Symbol=EURUSD`, `Period=M1`, `ShutdownTerminal=1`, el
terminal arrancó, cargó el script, el script escribió sus ficheros en `MQL5\Files` y el terminal se
cerró solo con código 0 (log del terminal: «script MedirFase0 (EURUSD,M1) loaded successfully» ·
«closes terminal with code 0» · «shutdown with 0»). El script tiene que estar en `MQL5\Scripts` de la
carpeta de datos (la ruta de `Script=` es relativa a ella).

**¿Corre sin conexión? Sí, y eso es un hallazgo de cuidado.** La primera vez el script corrió a las
15:23:48.9 y el terminal se autorizó en FTMO-Demo a las 15:23:49.7: **el script corrió antes de
conectar** y leyó `terminal_connected|0`, `account_margin_mode|ACCOUNT_MARGIN_MODE_RETAIL_NETTING`,
`desfase_servidor_gmt_seg|0` y un `time_current` del 2026-10-09 (el último tick guardado). El mismo
log, un segundo después: «trading has been enabled, demo account - **hedging mode**». Con una espera
hasta `TERMINAL_CONNECTED` (4,3 s) y 3 s más (`fase0/medida.txt`, la versión 2 del guion): HEDGING,
desfase **+10.800 s (+3 h)**, `time_current` de ese mismo minuto.

Y lo que lo hace delicado para D2a (`fase0/medida_b.txt`):

```
enum|DEMO=0|CONTEST=1|REAL=2
enum_margen|NETTING=0|EXCHANGE=1|HEDGING=2
init|SUCCEEDED=0|FAILED=1
antes_de_conectar|connected=0|trade_mode=0|error_trade_mode=0|login_distinto_de_cero=si|error_login=0|servidor_vacio=no|margin_mode=0
conectado|connected=1|trade_mode=0|error_trade_mode=0|login_distinto_de_cero=si|error_login=0|servidor_vacio=no|margin_mode=2
```

`ACCOUNT_TRADE_MODE_DEMO` **vale 0**, y antes de conectar `AccountInfoInteger` devuelve 0 en el modo de
margen **sin error** (`GetLastError` = 0), cuando el valor real es 2. Si con el modo de la cuenta pasa
lo mismo, la condición de `MedirDemoFTMO.mq5:759` (`!= ACCOUNT_TRADE_MODE_DEMO`) **deja pasar** a una
cuenta real leída antes de conectar: el 0 por defecto es DEMO. En esta cuenta no se puede distinguir
(es demo: 0 antes y después). No lo puedo medir con una cuenta real; lo que está medido es que una
propiedad entera de la cuenta vale 0 sin error antes de conectar. En MedirDemoFTMO no importa (corre a
mano, conectado, y comprueba además la cotización de los dos últimos minutos, `:785`); en un EA que
arranca con el terminal, sí. Va a la PARADA (decisión 1).

**(2) El Strategy Tester por línea de órdenes: SÍ.** De la misma página oficial: sección `[Tester]`
con `Expert`, `Symbol`, `Period`, `Model` («4 "Every tick based on real ticks"»), `FromDate`, `ToDate`,
`Report`, `ReplaceReport`, `ShutdownTerminal`. Medido con un EA de medida que no opera
(`fase0/TesterFase0.mq5`), EURUSD M1, `Model=4`, del 2026-10-13 al 2026-10-14 (`fase0/tester.txt` y el
log del agente del tester):

- **El EA corre en el tester** y **`ACCOUNT_TRADE_MODE` = `ACCOUNT_TRADE_MODE_DEMO`** allí (con la
  cuenta de prueba conectada; `mql_tester|1`). La negativa de D2a, por tanto, no impide correr en el
  tester con esta cuenta. Con otra cuenta no está medido (la doc de `[Tester]` habla de un `Login`
  emulado que «communicates to the Expert Advisor the value of an account»).
- **`SymbolInfoSessionTrade` responde en el tester**: lunes a viernes 00:05-23:55, sábado y domingo
  sin sesión, igual que en vivo.
- **El reloj no se puede probar en el tester:** `TimeTradeServer`, `TimeCurrent` y `TimeGMT` dan la
  misma hora simulada (`2026.10.13 00:00:00` las tres): el desfase sale 0.
- **El servidor de la demo de FTMO da ticks reales al tester:** «EURUSD,M1 (FTMO-Demo): generating
  based on real ticks» · «EURUSD : real ticks begin from 2026.10.13 00:00:00»; el EA contó 83.305
  ticks del 13 de octubre, del 00:05:04 al 23:54:59. Cuánto hacia atrás llegan los ticks reales no lo
  medí (solo pedí un día; el historial de velas M1 empieza el 2025-01-02 según el log). Se contaron
  ticks; no se leyó ni se guardó ningún precio.

**(3) La demo.** La prueba de octubre **todavía conecta** (2026-10-19: «authorized on FTMO-Demo»,
«demo account - hedging mode»). Vence hacia el 22 (DEMO-FTMO.md); la corrida de cierre va en la del 26
(D5).

### 0.c Los bytes

**MedirDemoFTMO** abre su CSV con `FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI)`
(`tools/mql5/MedirDemoFTMO.mq5:809`), escribe cada fila con `FileWriteString(g_csv, linea + "\r\n")` y
`FileFlush(g_csv)` justo detrás (`:126-127`), y la cabecera con `"\r\n"` (`:138-140`). La copia del
terminal (la 1.0) hace lo mismo (`:118`, `:130`, `:756`).

**Medido hoy** (`fase0/MedirFase0.mq5`, función `Bytes`; los ficheros de bytes no se commitean porque
uno lleva CRLF y otro es UTF-16, y `.gitattributes` los normalizaría; van sus volcados):

| modo de apertura | lo escrito | bytes en disco |
|---|---|---|
| `FILE_WRITE\|FILE_TXT\|FILE_ANSI` | `"uno\r\n"`, `"dos\n"`, `"tres"` | `uno\r\ndos\r\ntres` (14 bytes): **CRLF**, y el `\n` suelto recibe su `\r` |
| `FILE_WRITE\|FILE_TXT\|FILE_UNICODE` | `"uno\r\n"`, `"dos\n"` | `ff fe` + UTF-16LE con `\r\n` las dos (22 bytes) |
| `FILE_WRITE\|FILE_BIN`, bytes de `StringToCharArray(…, CP_UTF8)` sin el 0 final | `"año\|línea\n"` | `61 c3 b1 6f 7c 6c c3 ad 6e 65 61 0a`: **UTF-8 sin BOM, LF, exacto** |
| reabrir con `FILE_READ\|FILE_WRITE\|FILE_BIN` + `FileSeek(SEEK_END)` | `"segunda\n"` | se conservan los 12 bytes y se añaden 8: **así se continúa un fichero** |
| reabrir con `FILE_WRITE\|FILE_BIN` (sin `FILE_READ`) | — | **tamaño 0: lo trunca** |

Lo que dice la documentación oficial, que casa con lo medido: `FILE_BIN` es «Binary read/write mode
(without string to string conversion)»; sin `FILE_ANSI` ni `FILE_UNICODE` se supone `FILE_UNICODE`
(<https://www.mql5.com/en/docs/constants/io_constants/fileflags>); en TXT y CSV `FileWriteString`
añade el `\r` que falte delante de un `\n` (<https://www.mql5.com/en/docs/files/filewritestring>);
`StringToCharArray` con `count=-1` copia también el 0 final, que hay que quitar
(<https://www.mql5.com/en/docs/convert/stringtochararray>; medido: 13 elementos para 12 bytes).

**Por qué el CSV de la ejecución 1 salió con LF sigue sin explicarse, y ahora contradice una medida.**
El fichero que sigue en `MQL5\Files` (`MedirDemoFTMO_20261009_153552.csv`) tiene 0 retornos de carro
(`grep -c $'\r'`) y el sha256 congelado (`86f0df8b…3c6e`); pero el mismo modo de apertura, en el mismo
terminal (build 6230), escribe hoy CRLF. DEMO-EJECUCION-1.md (recuadro de la fase 1) concluyó «lo
escribió MetaTrader»; lo medido hoy dice que MetaTrader, en modo texto ANSI, escribe CRLF. No lo puedo
explicar (no sé qué pasó con ese fichero entre que se escribió y el 2026-10-09); **no toca al journal**,
que no usa el modo texto (§0.f), y lo dejo como línea de deuda para la rama que congele los CSV 2 y 3.

**SHA-256: sí** (<https://www.mql5.com/en/docs/common/cryptencode>: `int CryptEncode(ENUM_CRYPT_METHOD
method, const uchar& data[], const uchar& key[], uchar& result[])`, devuelve el número de bytes del
resultado o 0 si falla; `CRYPT_HASH_SHA256`, «SHA256 HASH calculation», en la tabla de
<https://www.mql5.com/en/docs/constants/namedconstants/otherconstants>). Medido: `"abc"` da 32 bytes,
`ba7816bf…f20015ad`, el mismo que `sha256sum`. **Y con un array vacío devuelve 0 (falla)**:
`sha256_vacio|0:`. El formato no puede hashear nunca una cadena vacía (no lo hace: cada línea lleva al
menos la versión y el `prev`).

**FileFlush** (<https://www.mql5.com/en/docs/files/fileflush>): «Writes to a disk all data remaining in
the input/output file buffer»; sin él, lo pendiente se escribe «only when the file is closed using
FileClose()»; la página avisa de que llamarlo a menudo puede ralentizar. Una línea por evento y como
mucho un latido por minuto: el coste es nulo.

### 0.d El VPS sin puente

- **En el repo:** solo la instantánea de la investigación lo da como razón
  (`docs/research/2026-09-03-del-corpus-al-bot.html:341`, «el EA nativo corre en el Strategy Tester con
  ticks reales y en VPS sin puente»; `:483`) y ADR-0082 §4 dice que «no tienen cita de FTMO en el
  repo» y lo deja a R6a.1. `MASTER_PLAN.html:516` (F33) nombra «Configuración de terminal/VPS».
  `docs/validation/FTMO-REGLAS.md` R14: «we have no reasons for limiting or restricting your trading
  strategy, whether it's discretionary trading, algorithmic trading, EAs, etc.»
- **FTMO, página oficial** «Can I travel or use VPN/VPS?»
  (<https://ftmo.com/en/faq/can-i-travel-or-use-vpn-vps/>, consultada el 2026-10-19; sus datos dicen
  publicada el 2026-04-27 y modificada el 2026-08-24): «The use of VPN/VPS is also generally
  allowed.» La única excepción: no iniciar sesión en MetaTrader desde Estados Unidos ni poner la
  geolocalización del VPN/VPS en Estados Unidos.
- **Lo que no dice ninguna página de FTMO que haya encontrado:** nada específico de un EA en un VPS ni
  del VPS integrado de MetaQuotes. «Sin puente» es una propiedad de la arquitectura (el EA no necesita
  un proceso de Python al lado; ADR-0082 D4), no una regla de FTMO.
- **No se decide nada.** Línea propuesta para A.2 (opcional, §Líneas preparadas): preguntar a FTMO si
  admite el EA en el VPS integrado de MetaQuotes y si hay alguna región de VPS que no admita, además de
  Estados Unidos.

### 0.e Inventario, con fichero:línea

- **MedirDemoFTMO.mq5.** La negativa: `:759`, dentro de `bool Comprobaciones(string &motivo)` (`:757`),
  sin argumento de modo, llamada desde `OnStart` (`:796`) porque es un script; en un fallo, `Alert` y
  `return` (`:797-800`). `MedirReloj`: `:386-399`; lee `TimeCurrent` (`:391`), `TimeTradeServer`
  (`:389`, `:392`), `TimeGMT` (`:390`, `:393`, con la nota «TimeGMT sale del reloj del ordenador»),
  `TimeLocal` (`:394`), el desfase servidor − GMT en minutos (`:395`), **el desfase local − GMT como
  `-TimeGMTOffset()/60`** (`:396`: la lista de D2b no nombra `TimeGMTOffset`, y es de ahí de donde sale)
  y `TimeDaylightSavings` (`:397`). Escribe con `FileWriteString(… "\r\n")` y `FileFlush` (`:126-127`).
  No escribe el login: el paso 1 escribe el servidor, la empresa, la moneda, el apalancamiento, el modo
  de margen y el build (DEMO-FTMO-SCRIPT.md §1), y sí cifras de dinero (margen necesario y libre,
  `:603-604`; comisión).
- **scripts/leer_demo_ftmo.py.** Lee el CSV con `csv.reader(texto.splitlines())` (`:102`), así que
  acepta LF y CRLF (DEMO-EJECUCION-1.md lo dice en `:89`; hoy está en `:102`). No se toca.
- **mql5/.** Solo README: `mql5/README.md` (Params.mqh generado en F28, RunCases en F30, tester en
  F32), `Experts/README.md` («el EA (F31)»), `Include/Botsito/README.md` («dominio espejo y Params.mqh
  generado (F28, F29)»), `Scripts/README.md` («RunCases.mq5 para pruebas diferenciales (F30)»),
  `tester/README.md` (F32). Ningún `.mq5` ni `.mqh`.
- **src/botsito/mql5bridge/.** Solo `__init__.py`, con el docstring «Exporta spec y casos a MQL5; lanza
  compilacion y tester; parsea resultados (F28, F30).» En import-linter (`pyproject.toml:96-117`) está
  en la capa `botsito.viewer | botsito.mql5bridge`, **por encima de `engine`**: `engine` (F23) no puede
  importarlo, y `viewer` (su hermano, «independiente») tampoco. Ver decisión 4.
- **A-28** ABIERTA (`knowledge/spec/ambiguedades.yaml:692`), medición, no bloqueante; no se cierra
  antes del cambio de hora de octubre. Sus dos parámetros: `broker_offset_base` (`parametros.yaml:138`,
  `estado: UNKNOWN`) y `broker_dst` (`:151`, `estado: UNKNOWN`). R6a.1 no los toca (D6).
- **ADR-0068 §4** (`docs/adr/0068-*.md:61-74`): en vivo, las sesiones de `SymbolInfoSessionTrade` se
  convierten en cierres con `cierres_desde_sesiones` y se unen con `unir_cierres`; el recuadro de
  ADR-0082 dice que el EA los porta y que la lectura llega en R6a.1 y el veto en R6a.5.
  `cierres_desde_sesiones` (`src/botsito/domain/cierres.py:121`) recibe **instantes** `(inicio, fin)`;
  `SymbolInfoSessionTrade` da **segundos desde las 00:00 de un día de la semana** («in the returned
  value date should be ignored», doc oficial), sin huso declarado: pasar de uno a otro necesita una
  semana concreta y el reloj del servidor, y eso es de R6a.5 (y de A-28).
- **RENOVAR-CIERRES.md, condición 2** (`:19-27`): antes de que el bot corra en tiempo real, la rama
  que lo conecte trae la lectura de `SymbolInfoSessionTrade` o un procedimiento de renovación; «Sin una
  de las dos, esa rama no se cierra.»
- **MASTER_PLAN §H** (`docs/plan/MASTER_PLAN.md:234`): «MQL5: … verificacion de `ACCOUNT_MARGIN_MODE`
  al arrancar; journal con flush y hash encadenado …», en F29 y F31. **§H.2** (`:268`), fila «Estado de
  jornada no persistente en el EA»: «F23: esquema de journal versionado y compartido (UTC, offset
  servidor, evento, regla, condicion fallida, `spec_hash`, `risk_hash`, lecturas ambiguas)».
- **La guardia y los `.mq5`/`.mqh` en `mql5/`:** la guardia no mira Write ni Edit (el matcher de
  `.claude/settings.json:69` es `Read|Grep|Glob|Bash|PowerShell`, lo midió el auditor), así que escribir
  `.mq5` y `.mqh` en `mql5/` no la toca; `guardia.py` no nombra `mql5`, `.mq5` ni `.mqh` (grep vacío).
  Escribir allí se mide de verdad con el primer fichero de la fase 1.
- **Las sesiones de EURUSD en la demo de FTMO**, leídas (`fase0/medida.txt`): lunes a viernes, una
  sesión de 00:05 a 23:55 (`from_seg=300`, `to_seg=86100`); sábado y domingo, ninguna. La segunda
  llamada (índice 1, y el índice 0 del sábado y del domingo) devuelve `false` con `GetLastError()` =
  **4307**, `ERR_MARKET_SESSION_INDEX`, «Wrong session ID when calling the SymbolInfoSessionQuote/
  SymbolInfoSessionTrade function» (<https://www.mql5.com/en/docs/constants/errorswarnings/errorcodes>).
  `SymbolInfoSessionQuote` (misma firma, «quoting sessions»,
  <https://www.mql5.com/en/docs/marketinformation/symbolinfosessionquote>) dio exactamente lo mismo.
  Leídas igual antes y después de conectar.

### 0.f Las propuestas

**Ruta de compilación (decisión 2).** Un módulo nuevo, `src/botsito/mql5bridge/compilar.py`, que se
ejecuta con `uv run python -m botsito.mql5bridge.compilar --repo <raíz> --metaeditor <exe> --salida
<carpeta de anexos> <fuente>…` (la raíz, el ejecutable y la salida, por argumento; nada sacado de
`__file__`):

1. exporta `mql5/` **del índice de git** (lo estadiado, que es lo que se sella) a una carpeta
   temporal nueva (`git checkout-index --prefix=`), nunca a la del terminal;
2. compila cada fuente con `/compile:"<tmp>\mql5\…" /include:"<tmp>\mql5" /log:"<tmp>\….log"`;
3. lee el log UTF-16, escribe en `--salida` su versión UTF-8 y LF con una cabecera (sha256 del log
   original, sha256 del fuente compilado, build, fecha) y lista los avisos;
4. sale con 0 **solo si** la línea `Result:` dice `0 errors` y existe el `.ex5` (el código de salida de
   MetaEditor no sirve: 1 con éxito); el `.ex5` se queda en la carpeta temporal o se instala con
   `--instalar <carpeta de datos>` en `MQL5\Experts\Botsito\` / `MQL5\Scripts\Botsito\` (lo único que se
   copia al terminal es el compilado, que se rehace cada vez: no hay fuentes desincronizadas en el
   terminal).

Con tests en Python (que corren en la CI de Linux sin MetaEditor): el lector del log contra logs de
muestra (los de `fase0/`), la puerta con `0 errors` y con un error, y la exportación. Si la guardia
niega el módulo nuevo o el `.exe` con un fichero de la rama, PARADA (punto 3 del encargo).

**Ruta de pruebas (D4).** (1) Estáticas, en Python, en `make check` y la CI: `tests/contract/test_capa_mt5.py`
con las tres de D4 más la de D2e. (2) Dinámicas: el script de pruebas compilado por la ruta de arriba,
instalado en `MQL5\Scripts\Botsito\` y lanzado con `terminal64.exe /config:<ini>` (`[StartUp]`,
`ShutdownTerminal=1`), que escribe su salida en `MQL5\Files\Botsito\pruebas\`; el módulo
(`compilar.py --pruebas`, o un segundo módulo `pruebas.py`) la copia a los anexos y la compara con el
golden. Todo lo ejecuta Claude Code: medido hoy que puede (§0.a, §0.b). **El «Quién» de R6a.1 cambia**:
la sesión compila y ejecuta las pruebas en la máquina de Aleks; Aleks pone el EA en la demo (D5). La
negativa con REAL y CONTEST se prueba llamando a la función con el modo como argumento (D2a): no hace
falta una cuenta real.

**Nombres (D1).**
- `mql5/Experts/Botsito.mq5`: el EA. Uno solo, que las ramas de R6a irán ampliando (R6a.3 órdenes,
  R6a.4 freno...), con `#property version` y una `VERSION_EA` que va al journal.
- `mql5/Include/Botsito/Capa/`: `Cuenta.mqh` (la negativa `NegarFueraDeDemo(const long modo)` y las
  lecturas de la cuenta), `Reloj.mqh` (las lecturas de MedirReloj y `CambioDeDia(anterior, ahora)`,
  pura, para inyectar fechas), `Sesiones.mqh` (la lectura de `SymbolInfoSessionTrade`), `Journal.mqh`
  (el escritor: formato de línea, JSON, SHA-256, apertura y continuación del fichero). La subcarpeta
  `Capa/` separa lo de R6a del «dominio espejo» de F29.
- `mql5/Scripts/BotsitoPruebasCapa.mq5`: el script de pruebas dinámicas.
- `mql5/JOURNAL.md`: el documento del formato, junto al código que lo escribe y enlazado desde
  `mql5/README.md` (en `mql5/`, dentro de las rutas de la rama). Alternativa: `docs/runbooks/`, pero un
  formato no es un procedimiento.
- `src/botsito/mql5bridge/journal.py` (lector-validador; `python -m botsito.mql5bridge.journal
  <fichero>…` para Aleks), `compilar.py` (§ arriba); el docstring de `__init__.py` se amplía.
- `tests/golden/journal/casos_v1.jsonl` (las líneas que escribe el script de pruebas) y
  `tests/unit/test_journal_mql5.py`.
- Los README de `mql5/`, `Experts/`, `Include/Botsito/`, `Scripts/` y `tests/golden/` se amplían
  (el auditor recuerda que `mql5/README.md` y el de `tests/golden/` también describen su árbol).

**El formato del journal, versión 1 (D3; decisión 3).** JSON Lines: un objeto JSON por línea, UTF-8
sin BOM, LF, legible con cualquier editor. Claves **siempre presentes y en este orden**:

| clave | qué | v1 |
|---|---|---|
| `v` | versión del formato | `1` |
| `seq` | número de secuencia, desde 1, sin huecos, continuo entre ficheros y reinicios | entero |
| `srv` | hora del servidor (`TimeTradeServer`), ISO 8601 sin huso | `"2026-10-26T23:59:00"` |
| `gmt` | hora GMT (`TimeGMT`, **del reloj del ordenador**), ISO 8601 | ídem |
| `desfase_s` | `srv − gmt` en segundos (el «offset servidor» de §H.2) | entero |
| `ev` | el evento | `arranque`, `cuenta`, `reloj`, `sesiones`, `latido`, `cambio_de_dia`, `fin` |
| `datos` | objeto con los datos del evento | ver abajo |
| `regla` | regla que actuó (§H.2) | `null`, reservado (F23, R6a.4+) |
| `condicion` | condición fallida (§H.2) | `null`, reservado |
| `capa_hash` | hash de lo que la capa recibe (ADR-0082 D5) | `null`, reservado para R6a.2 |
| `spec_hash`, `risk_hash` | los dos hashes de F28 (§H.2) | `null`, reservados (desde F29) |
| `ambiguas` | lecturas ambiguas (§H.2) | `null`, reservado |
| `prev` | SHA-256 de la línea anterior, 64 hex en minúsculas | 64 ceros en la primera línea de la cadena |

Eventos de R6a.1: `arranque` (versión del EA, build, símbolo del gráfico, `conectado`); `cuenta`
(`ACCOUNT_TRADE_MODE`, `ACCOUNT_MARGIN_MODE` como texto del enum, el servidor, `conectado`) — **se
escribe solo cuando `TERMINAL_CONNECTED`**, por lo medido en §0.b; `reloj` (las siete lecturas de
MedirReloj más `TimeGMTOffset`, con la nota de que `gmt` sale del reloj del ordenador); `sesiones`
(`{"trade": {"MONDAY": [[300, 86100]], …}}`, segundos desde las 00:00 del servidor, la semana entera;
al arrancar y en cada cambio de día); `latido` (cada 60 s: `conectado`, `time_current`); `cambio_de_dia`
(`dia_anterior`, `dia_nuevo`, fechas del servidor); `fin` (el `reason` de `OnDeinit` y su nombre). Ni
login, ni dinero, ni el nombre del titular (D2f): el servidor sí (como MedirDemoFTMO).

**La fórmula del hash.** `h(n) = SHA-256(b(n))`, donde `b(n)` son los bytes UTF-8 de la línea `n` **sin
el LF final**; la línea `n+1` lleva `"prev": hex(h(n))`. Así el hash es sobre los bytes que fija el
formato, cada línea encadena con la anterior (cambiar un byte de la línea `n` cambia `h(n)` y rompe el
`prev` de la `n+1`), y la línea nunca está vacía (CryptEncode falla con un array vacío, §0.c). El
validador exige, además, que cada línea sea **la forma canónica** de su objeto
(`json.dumps(obj, ensure_ascii=False, separators=(",", ":"))` con las claves en el orden de la tabla):
una sola forma de escribir cada línea, y el escritor de MQL5 la produce. Límite conocido (como toda
cadena sin sello): borrar las últimas líneas no se detecta; una última línea sin LF sí (la marca como
truncada).

**Los ficheros.** `MQL5\Files\Botsito\journal_AAAAMMDD.jsonl`, uno por día del servidor, abiertos con
`FILE_READ|FILE_WRITE|FILE_BIN|FILE_SHARE_READ` y `FileSeek(SEEK_END)` (medido en §0.c: así se
continúa sin truncar; `FILE_SHARE_READ` para que Aleks pueda copiarlo con el EA puesto), escrito con
`FileWriteArray` de los bytes de `StringToCharArray(…, CP_UTF8)` sin el 0 final, y `FileFlush` tras cada
línea. **La cadena sigue entre días y entre reinicios**: al arrancar, el EA lee la última línea del
journal más reciente y sigue con su `seq + 1` y su hash; el cambio de día abre el fichero del día nuevo,
cuya primera línea (`cambio_de_dia`) lleva el `prev` de la última del día anterior. Si al arrancar la
última línea no valida (truncada), el EA empieza una cadena nueva con `prev` de ceros y lo dice en el
`arranque` (`cadena_anterior: "rota"`). El validador de Python valida uno o varios ficheros en orden
como una sola cadena. (Alternativa en la decisión 3.)

**Cómo lo leerán F23 y F34.** F23 (el journal de Python del simulador) escribe la misma v1 (los campos
de §H.2 son los de la tabla) con el mismo validador —por eso la decisión 4—; F34 compara la demo con el
backtest línea a línea por `(día, ev, regla, condicion)`, sin mirar `seq` ni `prev` (que solo prueban
la integridad de cada lado).

**El procedimiento de D5 (decisión 5).** Recomiendo una sección nueva en `docs/runbooks/DEMO-FTMO.md`
(«El EA de conexión (R6a.1)»), escrita como el resto del runbook: comprobar la hora de Windows
(Configuración → Hora e idioma → «Sincronizar ahora»: `gmt` sale de ahí); la sesión deja el EA
compilado en `MQL5\Experts\Botsito\` (no hay que copiar ni compilar a mano); ponerlo en un gráfico de
EURUSD con el mercado abierto y Algo Trading da igual (no opera); dejarlo puesto hasta pasada la
medianoche del servidor (el journal dice la hora del servidor en cada latido; hoy, con +3 h, son las
16:00 de Lima; tras el 25 de octubre, las 16:00 o las 17:00 según A-28); quitarlo y volver a ponerlo
(la cadena sigue en el mismo fichero); y copiar `MQL5\Files\Botsito\` entero, sin abrir ni renombrar,
a `data/ea_conexion/` (fuera de git). Un runbook aparte (`docs/runbooks/EA-CONEXION.md`) sería la
alternativa si se prefiere no alargar DEMO-FTMO.md.

## 1. El encargo frente al repo

El informe del auditor (subagente `auditor-encargo`, 2026-10-19): 60 afirmaciones, 51 correctas, 2
incorrectas y 7 con matiz; 15 herencias no recogidas. Lo que cambia algo, con su evidencia:

- **INCORRECTA (17): «el valor con el que compararlo llega con el perfil generado (R6a.2)».** Ni el
  perfil (`knowledge/cuentas/`) ni el registro tienen modo de margen (grep `hedg|netting|margin_mode|modo_margen`
  vacío), R6a.2 no lo nombra (HOJA-DE-RUTA.md:292-294), y si la cuenta Swing es hedging es una pregunta
  abierta a FTMO (DEMO-FTMO.md:139-140; A.2, P-D1). Y ADR-0082 §10 da a R6a.1 «la comprobación de
  `ACCOUNT_MARGIN_MODE`» al arrancar, que el consultor aceptó el 2026-10-18
  (PLATAFORMA-ADELANTADA.md:461, :480). **D2b contradice un ADR: es PARADA por la regla del propio
  encargo** (decisión 0).
- **MATIZ (18):** MASTER_PLAN §H:234 pone la verificación al arrancar en F29/F31, no en el pre-vuelo;
  R6a.7 la lleva por ADR-0082 §10.
- **INCORRECTA (29):** `test_no_crlf_in_tracked_text_files` está en
  `tests/contract/test_repository_integrity.py:98`, no en `tests/unit/`.
- **MATIZ (30):** «el repo exige UTF-8 y LF»: `.gitattributes` solo fija LF; el test busca `\r\n`
  (`:113`) en los sufijos de `TEXT_SUFFIXES` (`:15-30`), **sin `.log` ni `.jsonl`**; nada mira el BOM.
  El validador del journal sí lo hará para el journal y el golden, y los logs de compilación de los
  anexos se comprueban en sus tests (herencia 13).
- **MATIZ (14):** la lista de MedirReloj no nombra `TimeGMTOffset`, de donde sale el desfase local −
  GMT (`:396`). El EA lo lee igual.
- **MATIZ (22):** MedirDemoFTMO no escribe el login, pero sí cifras de dinero (margen, comisión); D2f
  se aparta de ese precedente, y está bien: R6a.1 no las necesita.
- **MATIZ (25):** «con el journal de Python» es lectura del consultor; F23 aún no tiene journal
  (HOJA-DE-RUTA.md:510).
- **MATIZ (54):** «una línea para G»: NA:G es PREREGISTRO; se quiere decir el carril de guardias y
  deuda de la hoja (como dijo el encargo de punto-usado).
- **MATIZ (7):** «la ingesta de la sesión 5 (primera semana de noviembre)» solo lo dice el encargo de
  barrido-sesion-5; A.3 (fecha de la sesión 5) no está HECHA.

Herencias que cambian algo:

- **(2) Import-linter**: con el validador en `mql5bridge`, `engine` (F23) no puede importarlo
  (`pyproject.toml:96-117`), y `pyproject.toml` está fuera de las rutas (decisión 4).
- **(3) Rutas**: `cli.py` y `pyproject.toml` fuera; por eso propongo `python -m` y no un subcomando de
  `botsito`.
- **(4) `.ex5` sin seguir** si se compila dentro del repo: la ruta de §0.f compila en una carpeta
  temporal.
- **(5) `Tests Currently Passing`** cambia con cada test nuevo (`state check`): la rama toca
  `PROJECT_STATE.md` en esa línea, que es lo que hacen todas; no es «el ritual», y lo declaro.
- **(6) D2g no tiene guardia en MQL5**: `test_no_business_literals` solo mira `src/botsito/`. Y el
  latido de 60 s es una cifra escrita a mano (decisión 6).
- **(7) La guardia**: un `.mq5` de la rama como argumento de un programa desconocido se niega; la ruta
  de §0.f no lo hace.
- **(8) Mayúsculas**: los tests leerán `mql5/Experts` y `mql5/Include/Botsito` con la grafía exacta (la
  CI es Linux).
- **(9) Festivos**: `SymbolInfoSessionTrade` es una plantilla semanal y no puede expresar un festivo;
  leerla en cada cambio de día deja constancia de si la plantilla cambia (eso sí lo hace el EA), pero
  un cierre de un día concreto sigue viniendo del calendario (ADR-0068 §4, R6a.5).
- **(10) `crudo`**: medido hoy, otra vez: la guardia negó un guion de medida mío del scratchpad por una
  variable llamada `crudo` (el falso positivo de K). La renombré (`original`), que es lo que la deuda K
  ya pide para el código nuevo; lo declaro aquí y no toca la rama.
- **(11)** La comprobación del contrato con `pytest -k "mql5 or journal or ea_conexion"` no selecciona
  nada hasta la fase 1 (los nombres propuestos sí casan).
- **(15)** Las líneas de la hoja sin recuentos; y el «Quién» nombra a la sesión, al consultor y a Aleks
  por separado (ADR-0072).

## 2. Lo que no pude medir

- **El modo de la cuenta antes de conectar en una cuenta REAL o de CONCURSO.** Solo hay una cuenta, de
  demo. Lo medido: el modo de margen vale 0 sin error antes de conectar (§0.b).
- **El código de retorno de un EA que se niega, en el terminal.** Está citado de la documentación
  oficial (<https://www.mql5.com/en/docs/basis/function/events>): `INIT_FAILED` (= 1, medido) —
  «Initialization failed»—, y un código distinto de cero en `OnInit` genera `Deinit` con
  `REASON_INITFAILED` y el EA «is forcibly unloaded from the chart». Lo medirá el script de pruebas de
  la fase 2 si el consultor quiere (con el EA real en el tester o en el terminal).
- **Por qué el CSV de la ejecución 1 tiene LF** (§0.c).
- **Cuánto hacia atrás llegan los ticks reales del servidor de FTMO en el tester** (§0.b).
- **El cambio de día en vivo** (llega con D5).

## 3. Exposiciones

Ninguna. No se leyeron velas, ticks (se contaron, sin leer un precio), libros ni material del trader;
el CSV de la ejecución 1 se midió por sha256 y por recuento de `\r`, sin abrirlo.

## Lo que necesito que decidas

0. **ACCOUNT_MARGIN_MODE en R6a.1 (D2b contradice ADR-0082 §10, y su motivo no se sostiene).** El valor
   con el que comparar no está en el perfil ni lo trae R6a.2; FTMO no ha confirmado que Swing sea
   hedging (A.2, P-D1). Opciones: (a) R6a.1 lo lee y lo registra sin abortar, como decidiste, **con un
   recuadro en ADR-0082 §10** (la rama tendría que tocar `docs/adr/`, hoy protegida; o el recuadro va en
   el commit del contrato de la orden de cierre) y una línea para R6a.7 que diga que antes de comparar
   hay que crear el parámetro del modo de margen con su fuente; (b) R6a.1 lo comprueba y aborta si no es
   HEDGING, con un valor que hoy no tiene fuente (lo medido en la demo no es la cuenta Swing de verdad).
   Recomiendo (a): comparar contra un valor sin fuente es una cifra a mano (D2g); el motivo correcto no
   es «llega con R6a.2» sino «no hay valor con fuente hasta que FTMO conteste». Coste de (b): un
   parámetro nuevo en `parametros.yaml` (protegido en esta rama) con fuente `ev-*` que no existe.
1. **La negativa antes de conectar.** `ACCOUNT_TRADE_MODE_DEMO` vale 0 y una propiedad entera de la
   cuenta vale 0 sin error antes de conectar (§0.b). Opciones: (a) la condición de MedirDemoFTMO:759 tal
   cual, lo primero de `OnInit`, dentro de `NegarFueraDeDemo(modo)` (D2a), **y además** el EA no escribe
   `cuenta` ni hace nada más que `arranque` y latidos hasta `TERMINAL_CONNECTED`, y entonces vuelve a
   llamar a la misma función con el modo leído conectado y, si no es DEMO, se quita (`ExpertRemove()`) y
   lo escribe; (b) solo la condición de D2a. Recomiendo (a): mismo texto de condición, mismo test
   estático, y cierra el hueco medido; hoy no envía órdenes, pero lo heredan R6a.3 y siguientes. Coste
   de (b): una negativa que con el terminal recién abierto puede leer el 0 por defecto.
2. **La ruta de compilación y de pruebas.** (a) La de §0.f: la sesión compila desde una exportación del
   índice a una carpeta temporal con `/include`, la puerta lee `Result: 0 errors` (no el código de
   salida), los logs van a los anexos en UTF-8 y LF con el sha256 del original, y la sesión lanza el
   script de pruebas con `terminal64.exe /config`; el «Quién» de R6a.1 cambia («la sesión compila y
   ejecuta las pruebas en la máquina de Aleks; Aleks pone el EA en la demo»). (b) Compilar en la carpeta
   de datos del terminal copiando los fuentes (como DEMO-FTMO.md), a mano por Aleks con F7. Recomiendo
   (a): medido que funciona y deja log; (b) deja copias que se desincronizan (ya pasa hoy: el terminal
   tiene MedirDemoFTMO 1.0). Coste de (a): un módulo y sus tests más, en `mql5bridge`. Si la guardia
   niega el módulo o el `.exe`, PARADA.
3. **El formato y los ficheros del journal.** (a) El de §0.f: JSON Lines con las claves siempre
   presentes (las reservadas a `null`), `h(n) = SHA-256(línea n sin LF)` y `prev` en la siguiente, forma
   canónica obligatoria, un fichero por día del servidor y la cadena continua entre días y reinicios.
   (b) Lo mismo, pero un fichero por arranque, cada uno con su cadena desde ceros y el `arranque`
   apuntando al hash final del anterior. Recomiendo (a): el día es la unidad de F34 y del «reinicio a
   media jornada» de R6a.3, y el reinicio de D5 prueba de verdad que la cadena sobrevive. Coste de (a):
   el EA tiene que leer la última línea al arrancar (más código y una prueba más en el script).
4. **Dónde vive el validador, con import-linter.** (a) En `src/botsito/mql5bridge/journal.py`, como
   dice D3, con una línea de deuda: cuando F23 lo necesite, el esquema se baja a `botsito.comun` (o a
   una capa que `engine` vea) en su rama, tocando `pyproject.toml`. (b) Ya ahora en `botsito.comun`, lo
   que pide ampliar las rutas del contrato a `src/botsito/comun/` (y quizá `pyproject.toml`). Recomiendo
   (a): cumple D3 tal cual, `mql5bridge` puede importar todo lo de abajo, y el movimiento lo decide quien
   tenga el primer consumidor. Coste de (b): tocar una capa que usa medio repo para un consumidor que no
   existe aún.
5. **El procedimiento de D5.** (a) Una sección nueva de `docs/runbooks/DEMO-FTMO.md`; (b) un runbook
   nuevo, `docs/runbooks/EA-CONEXION.md`. Recomiendo (a): es la misma demo, el mismo terminal y el
   mismo `data/`, y Aleks ya sigue ese runbook el 26.
6. **El latido «por minuto» es una cifra en el EA.** D2g prohíbe cifras de firma, bróker, instrumento
   y ejecución; el periodo del latido no es ninguna de las cuatro (es del propio journal), pero CLAUDE.md
   dice que «si un valor puede cambiar, es un parámetro del registro» y R6a.2 aún no genera nada.
   Opciones: (a) una constante `#define LATIDO_SEG 60` en el EA, nombrada y documentada en `JOURNAL.md`
   como parte del formato v1 (cambiarla es una versión nueva), con línea para R6a.2 por si se quiere
   generar; (b) PARADA hasta R6a.2. Recomiendo (a): es una propiedad del formato, no de la cuenta. Y lo
   mismo para el tope de seguridad del bucle de sesiones (el índice sube hasta que la función devuelve
   `false`; un tope de 32 solo evita un bucle infinito).
7. **`SymbolInfoSessionQuote`** se lee igual (medido: misma firma, mismas horas en EURUSD hoy). (a)
   Leerlo también y escribirlo en `sesiones` (`"quote": …`), sin usarlo; R6a.5 decide si sirve (un hueco
   de cotización que no sea de negociación). (b) No leerlo. Recomiendo (a): cuesta una llamada por día y
   deja el dato para R6a.5. Coste de (b): ninguno hoy; si R6a.5 lo quiere, otra rama de MQL5.
8. **El CSV de la ejecución 1 y el LF (§0.c).** Solo una línea de deuda para la rama que congele los CSV
   de las ejecuciones 2 y 3: «el modo texto ANSI de MT5 build 6230 escribe CRLF (medido el 2026-10-19,
   EA-CONEXION.md §0.c) y el CSV de la ejecución 1 tiene LF: comprobar el CRLF del CSV 2 en `MQL5\Files`
   antes de copiarlo». ¿De acuerdo? Recomiendo que sí; no cambia nada de esta rama.
9. **La línea para A.2 sobre el VPS (§0.d).** (a) Añadirla («si FTMO admite el EA en el VPS integrado
   de MetaQuotes y alguna región, además de EE. UU., que no admita»); (b) no, porque la página oficial
   ya dice «generally allowed». Recomiendo (b) salvo que vayas a usar el VPS de MetaQuotes: entonces (a).

## Estado

EN CURSO: fase 0 entregada, **PARADA**. Espero la respuesta del consultor a «Lo que necesito que decidas».
