# DEMO-EJECUCION-1 · La ejecución 1 de MedirDemoFTMO en la prueba de FTMO

Rama `trabajo/demo-ejecucion-1`, abierta el 2026-10-09 desde `main` en e5a2261 (merge f6d3117, tag
`stable/F37h-adelgazar-estado`). Encargo: `docs/encargos/trabajo-demo-ejecucion-1.md`. Punto A de la
Next Action: con el primer CSV, fijar los valores de ADR-0057 y A-27.

Antes de abrir se comprobó con git: `main` = `origin/main` = e5a2261;
`git rev-parse "stable/F37h-adelgazar-estado^{commit}"` = f6d3117, que es el merge que nombra el
último registro de HISTORIA; ninguna otra rama, ni local ni en `origin` (`git ls-remote --heads`
solo da `main`).

**Lo que declara Aleks (2026-10-09), sin comprobar desde aquí salvo donde se dice:** ejecución 1 en
la prueba gratuita creada el 2026-10-08, lanzada a las 07:35 de Lima; terminó «completo» en unos 45
segundos, sin órdenes ni posiciones al final, con el balance en 99.999,75 USD; el CSV se copió tal
cual a `data/demo_ftmo/` sin abrirlo con Excel. El CSV CONFIRMA la hora (fila 30, `time_local`
07:35:52; fila 28, servidor 15:35:52), el «completo» (fila 59), que no quedó nada abierto (fila 58,
`quedan_abiertas_al_terminar` 0) y la duración: de la primera fila (15:35:52 del servidor) a la última
(15:36:36), **44 segundos**. El balance no está en el CSV (§0.b, fila 53).

## 0. Fase 0: inventario sin tocar knowledge ni código

### 0.a El CSV congelado

| campo | valor |
|---|---|
| fichero | `data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv` (fuera de git, `.gitignore`) |
| bytes | 9.907 |
| sha256 | `86f0df8b24f632102f0207b62a298a7776a164868e9a2d820ceb133c144b3c6e` |
| filas | 59 de datos más la cabecera; `version_script` 1.0 en todas |
| manifiesto | `data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml`, INMUTABLE tras commit |

**El procedimiento.** `docs/runbooks/DEMO-FTMO.md` («Dónde queda el fichero y a dónde va») pide
congelar el hash en un manifiesto de `data/manifests/` y no fija formato. No hay comando para esto
(`botsito data download` y `download-ticks` generan los suyos, y ninguno lee un CSV de MT5), así que el
manifiesto se escribe a mano, con el esquema nuevo que documenta `data/manifests/README.md`
(«Demo de FTMO»), en la subcarpeta `demo_ftmo/`, como `ticks/`:
- la guardia de inmutabilidad la cubre igual (`comun/historial.py`, `_es_protegido`: todo `.yaml`
  bajo `data/manifests/`, a cualquier profundidad), y el hook `pre-commit` también
  (`scripts/git-hooks/pre-commit`, línea 60);
- `knowledge validate` solo carga como dataset de velas los manifiestos de la raíz
  (`data/dataset.py`, `manifiestos`: `p.parent == carpeta`), así que una subcarpeta no le choca.

**Una cosa que el repositorio no puede comprobar:** el CSV tiene fin de línea LF (0 retornos de carro,
medido con `grep -c $'\r'`), y el script escribe `\r\n` en cada línea
(`tools/mql5/MedirDemoFTMO.mq5:118` y `:132`). O el modo texto de MetaTrader lo cambió al escribir, o
cambió en la copia. No toca ningún valor (el lector lee los dos), pero el hash congela ESTOS bytes:
si Aleks quiere comprobar que la copia es la de `MQL5\Files`, basta `certutil -hashfile
<fichero> SHA256` sobre el original y compararlo con el de arriba. Para las ejecuciones 2 y 3, lo
mismo antes de copiar.

> **Añadido en la fase 1 (2026-10-09, respuesta del consultor, punto 0).** **Los bytes congelados
> son los del original:** Aleks pasó `certutil -hashfile` sobre
> `MQL5\Files\MedirDemoFTMO_20261009_153552.csv` y da `86f0df8b…3c6e`, el mismo sha256 (lo declara
> Aleks, 2026-10-09). Así que el LF no cambió en la copia: **lo escribió MetaTrader**, y el LF frente
> al `\r\n` del código queda como hecho medido.
>
> **Por qué sale LF, leyendo el script: el script no lo explica.** Abre el fichero con
> `FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI)` (`MedirDemoFTMO.mq5:756`): texto, de un
> byte por carácter. Escribe cada línea con `FileWriteString(g_csv, linea + "\r\n")` (`:118`) y la
> cabecera igual (`:132`). Nada en el script quita el `\r`. La documentación de MQL5 tampoco lo
> explica: la de `FILE_TXT` y `FILE_ANSI` no dice nada de fines de línea, y la de `FileWriteString`
> dice lo contrario, que en un fichero CSV o TXT añade el `\r` que falte delante de un `\n`
> (consultada el 2026-10-09: <https://www.mql5.com/en/docs/files/filewritestring> y
> <https://www.mql5.com/en/docs/constants/io_constants/fileflags>). Lo que haga el terminal (build
> 6230, fila 26) con el `\r\n` en modo texto no se puede medir desde el repositorio. **No se cambia
> nada por ello**: el lector parte las líneas con `str.splitlines()` y lee las dos formas
> (`scripts/leer_demo_ftmo.py:89`).

**La tabla del lector** (`uv run python scripts/leer_demo_ftmo.py data/demo_ftmo`, con
`PYTHONUTF8=1` para que el «·» salga bien en la consola de Windows), tal cual:

```text
# Demo de FTMO: lo medido (1 fichero(s))

Solo lee: ningun valor pasa a los parametros ni cierra ninguna decision desde aqui.

- MedirDemoFTMO_20261009_153552.csv: completo

## Decision a decision

| decision | que se mide | MedirDemoFTMO_20261009_153552.csv |
|---|---|---|
| ADR-0057 d1 | llenado de una buy stop: precio - nivel | 1.0 puntos (nivel 1.11999, llenado 1.12000) |
| ADR-0057 d1 · DN-3 | compra a mercado | comision -0.03; deslizamiento 2.0 puntos |
| ADR-0057 d1 · DN-3 | cierre a mercado | comision -0.03; deslizamiento -2.0 puntos |
| ADR-0057 d2 | pendiente en el nivel exacto | sell_stop si (10009 DONE); buy_stop no (10015 INVALID_PRICE); sell_limit llenada (10009 DONE) a 1.11993; buy_limit no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | sell stop por encima del bid | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | buy stop por debajo del ask | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | sell limit por debajo del bid | no (10015 INVALID_PRICE) |
| ADR-0057 d2 · d3 | buy limit por encima del ask | no (10015 INVALID_PRICE) |
| ADR-0057 d3 | modificar una sell stop al lado equivocado | si_sin_cambios (10015 INVALID_PRICE) |
| ADR-0057 d3 | modificar una buy limit al lado equivocado | si_sin_cambios (10015 INVALID_PRICE) |
| ADR-0057 d4 | cotizacion al enviar (bid/ask en cada fila del CSV) | en el CSV, fila a fila |
| ADR-0057 d5 · A-27 | stops level (puntos) | 0 |
| ADR-0057 d5 · A-27 | a la distancia del stops level | sin medir |
| ADR-0057 d5 · A-27 | un punto dentro del stops level | sell_stop no (10015 INVALID_PRICE); buy_stop no (10015 INVALID_PRICE); sell_limit no (10015 INVALID_PRICE); buy_limit no (10015 INVALID_PRICE) |
| ADR-0057 d5 | freeze level (puntos) | 0 |
| A-27 | digits | 5 |
| A-27 | point | 0.00001000 |
| A-27 | contrato | 100000.00 |
| A-27 | volumen minimo | 0.01 |
| A-27 | paso de volumen | 0.01 |
| A-27 | modos de llenado | FOK IOC (bits 3) |
| A-27 | modo de ejecucion | SYMBOL_TRADE_EXECUTION_MARKET |
| FTMO-REGLAS R11 | volumen maximo | 50.00 |
| FTMO-REGLAS R12 | swap largo | -9.4100 |
| FTMO-REGLAS R12 | swap corto | 0.1000 |
| FTMO-REGLAS R12 | modo de swap | SYMBOL_SWAP_MODE_POINTS |
| FTMO-REGLAS R12 | dia del triple swap | WEDNESDAY |

## A-28: desfase del servidor frente a GMT, por fecha

| fecha (servidor) | desfase (min) | hora del servidor | hora GMT | fichero |
|---|---|---|---|---|
| 2026.10.09 | 180 | 2026.10.09 15:35:52 | 2026.10.09 12:35:52 | MedirDemoFTMO_20261009_153552.csv |

## Retcodes INESPERADOS: esas filas no miden lo que dicen

- ninguno

## Avisos de seguridad

- ninguno: el script no dejo nada abierto
```

### 0.b Medida → decisión, fila a fila

«Fila» es la columna `fila` del CSV. Columnas: a qué responde; qué dice hoy el repositorio; qué dice
la medida; y el veredicto: **COINCIDE**, **CONTRADICE**, **FIJA** (hoy UNKNOWN o DEFAULT sin
medir, y la medida le da valor) o **CONTEXTO** (no responde a ninguna decisión).

| fila | qué | responde a | el repositorio hoy | la medida | veredicto |
|---|---|---|---|---|---|
| 1-2 | versión 1.0, cuenta DEMO | contexto | — | el script corrió en una cuenta de prueba | CONTEXTO |
| 3, 38, 47, 52, 55, 58 | limpieza: órdenes o posiciones del script abiertas | seguridad | — | 0 en las seis | CONTEXTO (nada quedó abierto) |
| 4 | `stops_level_puntos` | A-27; ADR-0057 §5 | `instrumento_stops_level` 0, DEFAULT_AMBIGUOUS (FundedNext, ADR-0026); `firma_stops_level_puntos` UNKNOWN (perfil), y sin él el bróker simulado se NIEGA a colocar una orden stop | **0** | FIJA los dos (y coincide con el default del registro) |
| 5 | `freeze_level_puntos` | ADR-0057 §5 | «El freeze level no se modela» (ADR-0057 §5); R11 NO ENCONTRADA | **0** | FIJA: con 0, no modelarlo es exacto |
| 6 | `digits` | A-27; R11 | `instrumento_digitos` 5, DEFAULT_AMBIGUOUS; API de FTMO `digits: 5` | 5 | COINCIDE (y FIJA el estado) |
| 7 | `point` | A-27 | implícito: 5 decimales → 0,00001 (descripción de `instrumento_digitos`) | 0.00001000 | COINCIDE |
| 8 | `contrato` | A-27; R11 | `instrumento_contrato` 100000, DEFAULT_AMBIGUOUS; API `contractSize: 100000` | 100000.00 | COINCIDE (y FIJA el estado) |
| 9 | `volumen_min` | A-27 | `instrumento_lote_minimo` 0.01, DEFAULT_AMBIGUOUS; R11 NO ENCONTRADA | 0.01 | COINCIDE (y FIJA el estado) |
| 10 | `volumen_max` | R11 | `firma_volumen_max_lotes` **100**, CONFIRMED (perfil, API `maxTradeVolume: 100`) | **50.00** | **CONTRADICE** |
| 11 | `volumen_paso` | A-27 | `instrumento_lote_paso` 0.01, DEFAULT_AMBIGUOUS; R11 NO ENCONTRADA | 0.01 | COINCIDE (y FIJA el estado) |
| 12 | `volumen_limite` | R11 | nada (el perfil no tiene tope de volumen agregado) | 0.00 (sin tope agregado) | CONTEXTO: no falta ningún parámetro |
| 13 | `modos_llenado` | A-27 | nada: «el registro todavía no guarda» (pregunta de A-27); el simulador no modela llenados parciales | FOK e IOC (bits 3); RETURN no | FIJA un hecho para el conector (F33): una orden del EA tiene que ir con FOK o IOC. Ningún parámetro lo consume hoy |
| 14 | `modo_ejecucion` | A-27 | nada; el simulador llena al precio del tick, sin recotización (ADR-0051, ADR-0057 §1) | `SYMBOL_TRADE_EXECUTION_MARKET` | COINCIDE con lo que supone el simulador: ejecución a mercado, sin recotizaciones |
| 15 | `modos_caducidad_bits` | A-27 | nada: el bróker admite `expira_ms` opcional; cuánto vive una stop sin llenar es la candidata C7, sin abrir | 15: GTC, DAY, SPECIFIED y SPECIFIED_DAY | CONTEXTO: el servidor admite los cuatro modos; no limita ninguna decisión |
| 16 | `swap_largo` | R12 | `firma_swap_largo_puntos` **-9.49** (API, 2026-09-25) | **-9.41** (2026-10-09) | CONTRADICE en la cifra, pero el swap **cambia con la fecha** (§0.i, P6) |
| 17 | `swap_corto` | R12 | `firma_swap_corto_puntos` **0.36** (API, 2026-09-25) | **0.10** (2026-10-09) | ídem |
| 18 | `swap_modo` | R12 | puntos (`swapType: points`; el bróker los convierte con contrato y escala, `broker.py:808`) | `SYMBOL_SWAP_MODE_POINTS` | COINCIDE |
| 19 | `swap_triple_dia` | R12 | el simulador cobra UN swap por cada corte diario (`broker.py:797-811`), sin triple | WEDNESDAY | CONTRADICE (el simulador no cobra triple el miércoles); sin efecto mientras el bot cierre a las 15:00 (R7, `FTMO-REGLAS.md` §3) |
| 20 | `spread_actual_puntos` | contexto | DN-4: spread supuesto 5 puntos a las 14 de Madrid para minutos SIN ticks (percentil 90 de Dukascopy, `knowledge/simulador/llenado.yaml`) | 2 (y 1-2 en las filas 34-57) | CONTEXTO: un instante; DN-4 es un percentil 90 conservador y no se toca con una lectura |
| 21-23 | servidor, empresa, moneda | contexto | prueba de octubre: FTMO-Demo, USD (`DEMO-FTMO.md`) | FTMO-Demo; FTMO Global Markets Ltd; USD | COINCIDE |
| 24 | `apalancamiento` | R9 | `firma_apalancamiento` 30, CONFIRMED (perfil y registro) | 30 | COINCIDE |
| 25 | `modo_margen` | contexto | `DEMO-FTMO.md`: «Netting o hedging: SIN COMPROBAR» | `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING` | FIJA para la prueba (§0.c) |
| 26 | `build_terminal` | contexto | — | 6230 | CONTEXTO |
| 27-33 | el reloj | A-28 | `broker_offset_base` y `broker_dst` UNKNOWN; R10 «GMT+2 +DST» | servidor 15:35:52, GMT 12:35:52, Lima 07:35:52; desfase servidor-GMT **180** min; Lima −300, sin horario de verano | ANOTADA, NO CIERRA (§0.f) |
| 34 | sell stop 20 puntos por ENCIMA del bid | ADR-0057 §2, §3, §4 | se RECHAZA con `precio_invalido` (`llenado.lado_equivocado`, `Broker._precio_infringido`) | rechazada, 10015 INVALID_PRICE | COINCIDE |
| 35 | buy stop 20 por DEBAJO del ask | ídem | se rechaza | rechazada, 10015 | COINCIDE |
| 36 | sell limit 20 por DEBAJO del bid | ídem; la deuda «LLENA AL INSTANTE» | se rechaza (desde ADR-0057; antes se llenaba a su precio) | rechazada, 10015 | COINCIDE (§0.d) |
| 37 | buy limit 20 por ENCIMA del ask | ídem | se rechaza | rechazada, 10015 | COINCIDE (§0.d) |
| 39 | sell stop EN el bid exacto | ADR-0057 §2 | se acepta y espera («el nivel exacto no es lado equivocado») | colocada (10009), viva a 1.11981 | COINCIDE (una observación) |
| 40 | buy stop EN el ask exacto | ADR-0057 §2 | se acepta y espera | **rechazada, 10015** | **CONTRADICE** (una observación, §0.d) |
| 41 | sell limit EN el bid exacto | ADR-0057 §2; DN-1 | se acepta y ESPERA a que el bid pase ESTRICTAMENTE por encima; se llena a su precio, 1.11990 (`primer_llenado_limite`) | **se llenó al instante, a 1.11993** (3 puntos MEJOR que su precio) | **CONTRADICE** (una observación, §0.d) |
| 42 | buy limit EN el ask exacto | ADR-0057 §2 | se acepta y espera | **rechazada, 10015** | **CONTRADICE** (una observación) |
| 43-46 | las cuatro, UN punto del lado equivocado (con stops level 0, «un punto dentro» es un punto pasado) | A-27; ADR-0057 §2, §3, §5 | se rechazan con `precio_invalido` | las cuatro rechazadas, 10015 | COINCIDE |
| (a la distancia del stops level) | — | A-27 | — | no se mide: con stops level 0 coincide con el nivel exacto y el script lo salta (`MedirDemoFTMO.mq5:480-481`) | — |
| 48, 50 | sell stop y buy limit válidas, a 50 puntos | ADR-0057 §3 | se aceptan | colocadas (10009) | COINCIDE |
| 49, 51 | modificarlas 20 puntos al lado equivocado | ADR-0057 §3 | la modificación se rechaza y la orden sigue como estaba («así lo hace MT5 según el consultor; no medido») | 10015 y `si_sin_cambios`: la orden sigue a su precio | COINCIDE, y deja de ser «no medido» |
| 53 | compra a mercado: comisión | R12; perfil | `firma_comision_usd_por_lote` 5 con `firma_comision_por_lado` true: **5 USD por lote EN CADA LADO** (0,05 con 0,01 lotes), supuesto conservador | **−0,03** con 0,01 lotes en la apertura | **CONTRADICE** el importe; COINCIDE en que se cobra en la apertura (§0.i, P5) |
| 53 | compra a mercado: deslizamiento | ADR-0057 §1; DN-3 | `deslizamiento_fijo_puntos` 0 (PROVISIONAL «hasta la demo») | pedido 1.11996 (el ask), llenada 1.11998: **+2** puntos en contra | una muestra (§0.i, P7) |
| 54 | cierre a mercado: comisión | R12; perfil | se cobra otra vez en el cierre (`broker.py:880-882`) | **−0,03** en el cierre | COINCIDE en el lado; el importe, como en la 53 |
| 54 | cierre a mercado: deslizamiento | DN-3 | 0 | pedido 1.11993 (el bid), llenada 1.11995: **−2** (a favor) | una muestra |
| 56 | buy stop 2 puntos por encima del ask | ADR-0057 §1 | se acepta | colocada (10009) a 1.11999 | COINCIDE |
| 57 | el llenado de esa buy stop | ADR-0057 §1 | salta cuando el ASK toca el nivel y se llena al precio de ese tick, nunca mejor que el nivel | llenada a 1.12000 sobre un nivel de 1.11999: **+1 punto** en contra, en un segundo | COINCIDE (una observación; no dice qué tick la disparó) |
| 59 | terminado | contexto | — | completo | CONTEXTO |

**El balance que declara Aleks (99.999,75) no está en el CSV**, y el CSV no basta para reconstruirlo:
de las tres operaciones de ida y vuelta (la sell limit de la fila 41, la compra de las filas 53-54 y
la buy stop de la 57) solo trae la comisión y el precio de cierre de la segunda (−0,03 de resultado y
−0,06 de comisión). Con −0,03 de comisión en cada uno de los seis lados (0,18) quedan −0,07 de
resultado para las tres, que cabe en el spread de 1-2 puntos de esos segundos. Es compatible, no una
comprobación.

### 0.c Netting o hedging

**Lo medido:** fila 25, `modo_margen` = `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING`, y Aleks declara que la
barra de título de MT5 dice «Hedge». La línea de `DEMO-FTMO.md` («MetaTrader 5 muestra la cuenta de
prueba como "Netting"») no casa con lo medido: se corrige en esta rama (fase 0, solo el runbook).

**Lo que supone hoy el simulador, leído en el código:**
- El bróker guarda las posiciones en un diccionario por id (`engine/broker.py:290`), y cada orden
  llenada abre una posición NUEVA con su propio stop y objetivo (`broker.py:716-728`). Cada una se
  cierra sola (`_proximo_evento` las recorre una a una, `broker.py:660-670`). Nada suma ni compensa
  posiciones: **es la semántica de hedging**. Si se llenara una orden con otra posición abierta,
  habría dos posiciones independientes.
- **La estrategia nunca llega a tener dos**: RN-011 solo dimensiona y coloca con
  `ninguno_de: [orden_limite_pendiente, operacion_abierta]` (`knowledge/spec/strategy_spec.yaml:1353-1355`),
  y el hecho `operacion_abierta` lo da el bróker (`broker.py:609-616`). Una posición a la vez y, con
  ella viva, ninguna pendiente.

**Si netting o hedging lo cambiaría:** con una posición a la vez, no: en netting una orden que se
llena con una posición abierta del lado contrario la reduce o la cierra, y eso no puede pasar porque
no hay pendiente mientras hay posición. La diferencia está en el CONECTOR de F33, no en el
simulador: en hedging se cierra una posición por su ticket (`req.position`, como hace el propio script,
`MedirDemoFTMO.mq5:267`) y en netting con una operación contraria. **Nada que cambiar en el
simulador.**

**La cuenta Swing de verdad podría diferir de la prueba**: la prueba es una cuenta de prueba en
FTMO-Demo, y FTMO dice que la especificación de la cuenta es la que se ve en la plataforma (R11).
Pregunta para FTMO, por la vía de RESPUESTAS-FTMO (la escribe Aleks en el ticket; el repositorio
guarda la paráfrasis de la respuesta, no el correo), parafraseada:

> P-D1. La cuenta FTMO Challenge 2-Step Swing en MT5, ¿es de cobertura (hedging), como la prueba
> gratuita, o de compensación (netting)? Y en EURUSD, ¿el volumen máximo por orden es de 50 lotes,
> como en la prueba, o de 100, como dice la tabla de símbolos de la web?

### 0.d La sell limit en el nivel exacto (fila 41) frente a la deuda «LLENA AL INSTANTE»

La deuda (HISTORIA, Archivo 1, línea 538; viva en `PROJECT_STATE.md`, Technical Debt) es la de una
límite **colocada con el precio YA PASADO el nivel**: «3 de 8 (lectura a) y 4 de 8 (b) ordenes limite
del bot se colocaron con el precio al otro lado y `primer_llenado_limite` las lleno en el tick
siguiente». Se arregló en el simulador con ADR-0057 (se rechaza) y quedaba: «Sigue PENDIENTE medir en
la demo lo que hace MT5».

**Esta medida la paga ENTERA, y no con la fila 41:** el caso de la deuda son las filas **36 y 37** (una
límite 20 puntos pasada, de cada lado) y **45 y 46** (un punto pasada): MT5 las RECHAZA las cuatro con
10015 INVALID_PRICE y no llena ninguna. Es lo que dijo el consultor y lo que hace el simulador desde
ADR-0057. Cuatro observaciones, dos por lado, a 20 y a 1 punto.

**La fila 41 NO es el mismo caso**: una límite EN el nivel exacto no está pasada (ADR-0057 §2 lo
decide así a propósito). Lo que muestra es otra discrepancia, con ADR-0057 §2:
- **el simulador** la acepta y la deja esperando a que el bid pase estrictamente por encima de 1.11990
  (DN-1), y entonces la llena a 1.11990;
- **MT5** la llenó AL INSTANTE, a **1.11993**: 3 puntos MEJOR que su precio, es decir, a mercado.

Y las cuatro del nivel exacto (filas 39-42) no se portan igual: las dos de VENTA se aceptaron (la
stop quedó viva; la límite se llenó) y las dos de COMPRA se rechazaron (10015). **Una sola
ejecución no distingue entre dos explicaciones:** (1) que el servidor trate el nivel exacto de forma
distinta en compras y en ventas; o (2) que la cotización se moviera entre la lectura del tick
(`Cotizacion(t)`, justo antes de `OrderSend`) y la comprobación del servidor, que el CSV no registra.
La (2) es plausible: el bid se mueve de 3 a 6 puntos entre filas separadas por 1 a 4 segundos (filas
39-42: 1.11981, 1.11987, 1.11990, 1.11996), y
el llenado de la 41 a 1.11993 dice que el bid de la ejecución no era el de la lectura. Las ejecuciones
2 y 3 repiten el paso 4 con el mismo script; con tres observaciones por tipo se decide si §2 cambia.
**Para el bot el caso es raro** (una pendiente justo en el precio del momento), y la regla que importa,
el lado equivocado, queda medida.

### 0.e La fila 57: retcode 0 «SIN_RESPUESTA» con «llenada»

**Es lo esperado, no un defecto de la medida.** En `MedirLlenadoStop`
(`tools/mql5/MedirDemoFTMO.mq5:684-688`) la fila del llenado se escribe con el retcode **0 escrito a
mano**: no hay petición propia que dé un retcode, porque el llenado lo hace el servidor solo cuando el
ask toca el nivel; el script lo detecta porque la pendiente deja de estar viva (`PendienteViva`, cada
500 ms) y lee el precio del deal (`PrecioDelLlenado`). `Fila` escribe el número porque el tipo de
orden no está vacío (`:111`), y `TextoRetcode(0)` lo nombra «SIN_RESPUESTA» (`:66`). El lector lo sabe:
`buy_stop_llenado` está en `OBSERVACIONES` y su retcode no se juzga (`scripts/leer_demo_ftmo.py:53-54`,
`:128`); por eso el resumen dice «Retcodes INESPERADOS: ninguno».

Dos matices, sin cambiar el script en esta rama: la etiqueta engaña (sería más claro «OBSERVACION»
que «SIN_RESPUESTA»); y el bid/ask de la fila 57 son los de DESPUÉS del llenado (`Cotizacion(a)`,
`:682-683`), no los del tick que la disparó, así que la fila dice a qué precio se llenó (1.12000) pero
no qué ask la disparó.

### 0.f A-28: la primera de tres medidas

| medida | fecha (servidor) | servidor | GMT (reloj del ordenador) | local (Lima) | desfase servidor − GMT | Europa | Nueva York |
|---|---|---|---|---|---|---|---|
| 1 de 3 | 2026-10-09 | 15:35:52 | 12:35:52 | 07:35:52 | **180 min** | horario de verano | horario de verano |

**No cierra A-28.** 180 casa con «GMT+2 +DST» (R10) en verano, pero los DOS calendarios dan 180 el
2026-10-09; la ejecución 2 (26-30 de octubre: Europa ya en invierno, Nueva York todavía en verano) es
la que los separa: 120 diría europeo, 180 diría Nueva York. `broker_offset_base` (el desfase en
horario ESTÁNDAR) tampoco se fija: 180 en verano es 120 de base con cualquiera de los dos. La
«verificación explícita» de A-28 (a qué hora recalcula el panel el límite diario) no la mide el
script. El GMT sale del reloj del ordenador (nota de la fila 29); el local de Lima (−300 min, sin
horario de verano, filas 32-33) casa con él.

### 0.g El pendiente heredado A4: adelantar la negativa por A-27

A4 propone que el arnés se niegue por A-27 ANTES de leer velas (ADR-0057 §5, `MEMORIA-SUITE.md:97-99`),
porque hoy la negativa la da el bróker al colocar la primera orden stop. **Esa negativa existe solo
mientras `firma_stops_level_puntos` sea UNKNOWN** (`broker.py:399-405`). La fila 4 lo mide: 0.

**Propuesta: descartarla si la fase 1 fija `firma_stops_level_puntos` = 0** (P3): con el valor en el
único perfil que hay, la negativa no se da nunca, y adelantarla no tiene objeto; A4 sale de
`PROJECT_STATE.md` a HISTORIA por la condición (c), SUSTITUIDA, citando ADR-0071 y la fila 4. **Si el
consultor prefiere esperar a las ejecuciones 2 y 3 para fijar el stops level**, A4 se queda tal cual
hasta entonces: no hay razón para aplicarla, porque solo adelantaría una negativa que desaparecerá. En
ningún caso propongo aplicarla.

### 0.h La Next Action M (el break even de una venta que salta por el ASK)

**Esta ejecución no lo mide.** El script no abre ninguna venta, no pone un stop de protección en la
entrada ni lo modifica (`MedirDemoFTMO.mq5`: los pasos 6 y 7 son compras con stop de protección a 200
puntos, que nunca se mueve). Lo más cercano es la fila 57: una orden de compra que salta por el ASK se
llenó 1 punto peor que su nivel. Es un dato vecino (un stop de una venta también es una compra que
salta por el ASK), pero no mide lo que pide ADR-0065 §6: la latencia de la petición `modificar` ni si
el trader lo pone en la entrada exacta. **M se queda.**

### 0.i La propuesta para la PARADA

**Cómo citar.** El trailer `Fuente:` solo admite `ev-*`, `fb-*` o `ADR-NNNN` que existan
(`comun/historial.py`, `DIRECTORIOS_CON_FUENTE`), y el campo `fuente` del registro, `{tipo: decision,
id: ADR-NNNN}` para lo que no es estrategia (ADR-0004; cabecera de `parametros.yaml`). Un manifiesto
no cabe en ninguno. Propongo un ADR nuevo, **ADR-0071, «Lo que fija la ejecución 1 de la demo de
FTMO»**: cita el
manifiesto (id y sha256) y, por cada valor, la fila del CSV; dice qué partes de ADR-0057 pasan a
MEDIDAS y cuáles no; y es la `fuente` de cada parámetro y el `Fuente:` de cada commit. Se commitea
ANTES que los valores que lo citan (`docs/runbooks/AMBIGUEDADES.md`: «primero se commitea el
documento, despues la fuente que lo cita»; y la trampa de citar un ADR que todavía no existe). Una
evidencia documental (`ev-*`) no sirve: `knowledge/evidence/` es para items del corpus con su cita
(`DEMO-FTMO.md`).

**Los valores, uno a uno (cada uno con su fila):**

| | qué | de → a | fila | efecto | mi propuesta |
|---|---|---|---|---|---|
| P1 | ADR-0071 | nuevo | todas las de abajo | ninguno por sí solo | **aplicar** |
| P2 | `instrumento_digitos`, `_contrato`, `_lote_minimo`, `_lote_paso`, `_stops_level` (registro) | DEFAULT_AMBIGUOUS (FundedNext, ADR-0026) → **CONFIRMED** con el MISMO valor (5, 100000, 0.01, 0.01, 0), fuente ADR-0071, sin `ambiguedad_id` | 6, 8, 9, 11, 4 | ningún valor cambia: ni la estrategia ni las corridas. RN-026 sigue sin activarse nunca (con 0, su nota ya lo dice) | **aplicar** |
| P3 | `firma_stops_level_puntos` (perfil) | UNKNOWN → **CONFIRMED 0**, fuente ADR-0071 | 4 | el bróker simulado coloca órdenes stop SIN `--diagnostico-a27`, que con el valor fijado se rechaza (`broker.py:270-275`); las límites no cambian (`if minimo:` con 0 no juzga nada, `broker.py:449`). Desaparece uno de los diagnósticos que hoy impiden un «sí» de ADR-0070 (quedan A-21, A-35 y A-44). Tests que usan `--diagnostico-a27` o que esperan el UNKNOWN con el perfil real tendrán que cambiar (al menos `test_perfil_cuenta.py:85-88`, `test_cableado.py:638`, `test_renovar_cierres.py:189`; se miden en la fase 1). Ningún cambio en `src/` | **aplicar** |
| P4 | `firma_volumen_max_lotes` (perfil) | 100 (API de la web) → **50** | 10 | más rechazos por `volumen_max_lotes` en la línea base, donde ya los hay con 100 (pendiente heredado 37, `BROKER-ORDENES-STOP.md` §3). La plataforma manda sobre la web (R11: «The account specification can be seen directly in the trading platform») | **aplicar**, y P-D1 a FTMO por si la cuenta de verdad dice otra cosa |
| P5 | `firma_comision_usd_por_lote` (perfil) | 5 «por lado» (10 ida y vuelta, supuesto conservador) → ? | 53, 54 | la medida es 0,03 por lado CON 0,01 LOTES, y no fija la tarifa por lote: la comisión de un deal va en céntimos, y 0,03 sale de cualquier tarifa entre 2,50 y 3,49 por lado si redondea al más cercano, de 2,01 a 3,00 si redondea hacia arriba, o de 3,00 a 3,99 si trunca; el CSV no dice cuál. Excluye las dos del perfil y de `VIABILIDAD-COMISION.md` que no son 5 ida y vuelta: 5 por lado (daría 0,05) y 1,50 por lado (0,015 → 0,02). Casa con la tarifa publicada de 2,50 por lado (FTMO-REGLAS, recuadro del 2026-09-28) solo si redondea 0,025 hacia arriba | **no cambiar el importe en esta rama**: el 5 por lado es MÁS caro que cualquier tarifa compatible (a lo sumo 3,99), así que sigue siendo conservador; se anota en ADR-0071 que la medida lo excluye como hecho. **Y medir la comisión con 1,00 lote** en la ejecución 2: hace falta un cambio del script (una entrada de volumen para el paso 6), en una rama corta antes del 26 de octubre. `firma_comision_por_lado` = true: la medida lo CONFIRMA (se cobra en los dos lados, como dijo FTMO el 29-09); sin cambio de valor, solo la descripción |
| P6 | `firma_swap_largo_puntos`, `firma_swap_corto_puntos` | −9.49 / 0.36 (API, 2026-09-25) | 16, 17 | −9.41 / 0.10 el 2026-10-09: el swap **cambia con la fecha** (los tipos de interés), y el encargo no cierra nada que dependa de ella. Sin efecto mientras el bot cierre a las 15:00 | **no cambiar**; las tres ejecuciones dan tres lecturas; se anota en ADR-0071. Lo mismo el triple del miércoles (fila 19), que el simulador no cobra: deuda de una línea si el consultor quiere |
| P7 | `deslizamiento_fijo_puntos` (DN-3, `knowledge/simulador/llenado.yaml`) | 0, PROVISIONAL | 53, 54, 57 | tres muestras: +2, −2 y +1 (media +0,3). Ninguna cifra fija se sostiene con tres muestras de un minuto | **no cambiar**; se anota en ADR-0071 y suman las ejecuciones 2 y 3 |
| P8 | ADR-0057 §2 (el nivel exacto) | se acepta y espera | 39-42 | 3 de 4 discrepan, con una sola observación por tipo y una explicación por latencia que el CSV no puede descartar (§0.d) | **no cambiar**; esperar a las ejecuciones 2 y 3 |

**Ambigüedades.** **A-27 se cierra con esta ejecución**, como **DECIDIDA por ADR-0071** (ADR-0022,
la segunda forma: una `medicion` no la contesta el trader). Sus cinco parámetros no dependen de la
fecha (son la ficha del símbolo, que `SymbolInfo*` lee igual cualquier día), y las ejecuciones 2 y 3
los vuelven a leer con el mismo script: si alguno difiriera, se reabre con otro ADR. La cuenta de
verdad la sigue comprobando el pre-vuelo de F33 (`resuelve_en: [F17, F33]`). Cerrarla toca los cinco
sitios de `AMBIGUEDADES.md`: el YAML (`estado: DECIDIDA`, `decision: ADR-0071`, `decidida_el`), los
cinco parámetros (P2), la regla que la cita (RN-026: su nota dice «vale 0 en la demo medida [...] hay
que volver a medirlo en la cuenta fondeada»; propongo añadir que en FTMO también es 0, ADR-0071), la
fila de `PROJECT_STATE.md` («Known Ambiguities») que sale, y la hoja de preguntas, que no la lleva
(`scripts/hoja_preguntas.py`, sin A-27). Más `tests/unit/test_kit.py:353-355`, que congela A-27 en
ABIERTA, y `botsito spec docs --escribir` en el mismo commit. **A-28 no se cierra** (§0.f).

**Deudas.** Se paga «EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO
EL NIVEL»: sale de Technical Debt a HISTORIA por la condición (a), con las filas 36, 37, 45 y 46 y
ADR-0071 (§0.d). Si el consultor quiere, entra una línea por el swap triple que el simulador no
cobra (P6). La discrepancia del nivel exacto (P8) no es deuda todavía: es una medida que repetir, y va
en la entrada A.

**Entradas de la Next Action** (cambian en el commit del contrato, con la orden de cierre, RITUAL
punto 3; aquí solo la propuesta):
- **A** sigue en pie, reescrita: la ejecución 1 se hizo el 2026-10-09 (DEMO-EJECUCION-1.md, ADR-0071);
  las ejecuciones 2 y 3, en la segunda prueba desde el 26 de octubre, miden A-28 (desfase y
  calendario), repiten el nivel exacto (P8), los deslizamientos y los swaps, y, si se cambia el
  script, la comisión con 1,00 lote (P5).
- **M** se queda (§0.h).
- **S**: una de sus condiciones («después [...] de la primera ejecución de la demo de FTMO») se cumple
  con esta rama; el resto de la entrada no cambia.
- **Nueva, para Aleks con FTMO:** la pregunta P-D1 (§0.c).
- **Nueva, si el consultor lo decide:** la rama corta del script para la comisión a 1,00 lote (P5),
  antes del 26 de octubre.
- **A4** sale (§0.g) si se aplica P3. **El 37** (rechazos por volumen máximo) cambia su texto si se
  aplica P4: el máximo pasa de 100 a 50.

**El texto de `DEMO-FTMO.md` que se corrige — YA CORREGIDO en el commit de esta fase**, porque es un
runbook y no knowledge ni código (el encargo lo pide en c y lo propone en i; si el consultor quiere
otra redacción, se cambia en la fase 1):
- «Tarda unos cinco minutos» → «Tarda menos de un minuto si la orden del paso 7 salta enseguida (44
  segundos en la ejecución 1, el 2026-10-09) y como mucho unos tres si no salta: el paso 7 la espera
  hasta 120 segundos»;
- «**Esperar** unos cinco minutos» → «**Esperar** de uno a tres minutos»;
- «Netting o hedging: SIN COMPROBAR. MetaTrader 5 muestra la cuenta de prueba como "Netting" [...]»
  → «HEDGING en la prueba, medido», con la fila 25, el manifiesto, lo que declara Aleks y que la
  cuenta de verdad es una pregunta para FTMO (§0.c).
El «como mucho unos tres» sale de los 44 s más los 120 de espera del paso 7 (`InpEsperaStopSeg`,
`MedirDemoFTMO.mq5:30`), sin contar los pasos que fallen y reintenten la limpieza.

## 1. PARADA

> **Nota (fase 1, 2026-10-09).** Hasta la respuesta del consultor este informe llamaba «ADR-D1» al
> ADR nuevo: era su nombre provisional, porque citar un id que todavía no existe rompe `knowledge
> validate` (el primer `make check` de la fase 0 salió en rojo por eso, con 5 tests fallidos). Al
> crearlo tomó el número libre siguiente, **ADR-0071**, y desde la fase 1 el informe lo nombra así
> en todas partes salvo en la respuesta del consultor, que va tal cual.

Fase 0 entregada. **No se ha cambiado ningún valor**: ni `knowledge/`, ni `src/`, ni tests, ni el
script. En la rama solo hay: la apertura (encargo, contrato, Archivo 25), el manifiesto del CSV, la
sección «Demo de FTMO» de `data/manifests/README.md`, las tres correcciones de `DEMO-FTMO.md` y este
informe. Para seguir, el consultor decide P1-P8, el cierre de A-27, la deuda, A4 y si hay rama del
script para la comisión.

## 2. Respuesta del consultor a la PARADA

Dada el 2026-10-09. Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/demo-ejecucion-1 (2026-10-09). Cópiala tal cual en DEMO-EJECUCION-1.md, sección «Respuesta del consultor a la PARADA».
>
> 0. Hash del original: Aleks pasó certutil -hashfile sobre MQL5\Files\MedirDemoFTMO_20261009_153552.csv y coincide con 86f0df8b…3c6e (lo declara Aleks, 2026-10-09). Anótalo en §0.a: los bytes congelados son los del original. El LF frente al \r\n del código queda como hecho medido. Explica en el informe, leyendo el script (modo de FileOpen), por qué sale LF, sin cambiar nada por ello.
>
> 1. P1, ADR nuevo: APLICAR. Toma el número libre siguiente al crearlo y sustituye «ADR-D1» por el id real en todo lo commiteado desde ahora. En el informe, una nota dice que ADR-D1 era el nombre provisional. Se commitea antes que los valores que lo citan. Además de lo que propones, el ADR lleva, como consecuencia medida y calculada con los parámetros del registro (sin medir nada sobre trades): con riesgo_por_operacion sobre 100.000 y el valor del pip de EURUSD, el tope de 50 lotes corta todo stop por debajo de 1 pip. Es la cuenta que tiene que usar el pendiente heredado 37 (rechazos por volumen máximo, A-18).
>
> 2. P2, los cinco del registro a CONFIRMED con el mismo valor: APLICAR.
>
> 3. P3, firma_stops_level_puntos = 0: APLICAR. Condición: la negación por defecto del bróker con el stops level UNKNOWN sigue cubierta por tests con un perfil sintético UNKNOWN. Ningún test que hoy compruebe esa negativa se borra: se pasa al perfil sintético. Lista en el informe cada test cambiado, con su antes y después, y por qué sigue protegiendo lo mismo.
>    A4 sale de Pendientes heredados a HISTORIA por la condición (c), SUSTITUIDA, citando el ADR y la fila 4.
>
> 4. P4, firma_volumen_max_lotes = 50: APLICAR. La pregunta P-D1 a FTMO entra como pendiente para Aleks (la manda él; el repo guarda la paráfrasis de la respuesta). Cambia el texto del pendiente 37 con el máximo nuevo (50) y la cuenta del punto 1.
>
> 5. P5, la comisión: el importe NO cambia en esta rama; el ADR anota que la medida excluye 5 por lado como hecho y que sigue siendo conservador. firma_comision_por_lado = true, CONFIRMADO por la medida: solo cambia su descripción.
>    Además, EN ESTA RAMA, y lo autorizo pese a que el encargo decía no cambiar el script en el punto e: el script mide la comisión con 1,00 lote en la ejecución 2.
>    - Añade un input para el volumen del paso 6, por defecto 1.00, y súbelo a version_script 1.1.
>    - El paso 6 sigue abriendo y cerrando enseguida con su stop de protección. Comprueba el margen libre antes de abrir y, si no alcanza, que no abra y lo escriba.
>    - El lector reconoce las dos versiones, con un test del lector sobre un CSV sintético 1.1.
>    - DEMO-FTMO.md dice que antes de la ejecución 2 Aleks vuelve a copiar y compilar el script (F7, 0 errors) y comprueba que el CSV dice 1.1.
>    - Mientras haces esto, cambia la etiqueta «SIN_RESPUESTA» de las observaciones por «OBSERVACION» (0.e), en el script y en el lector, sin romper la lectura de los CSV 1.0.
>    - No toques nada más del script.
>
> 6. P6 (swaps), P7 (deslizamiento) y P8 (el nivel exacto): NO CAMBIAR. Esperan a las ejecuciones 2 y 3 y se anotan en el ADR. Sin deuda nueva por el triple del miércoles: el bot cierra a las 15:00.
>
> 7. A-27: se cierra como DECIDIDA por el ADR nuevo (ADR-0022), con los cinco sitios de AMBIGUEDADES.md, test_kit.py y botsito spec docs --escribir en el mismo commit. El ADR dice expresamente que las ejecuciones 2 y 3 y el pre-vuelo de F33 vuelven a leer la ficha, y que una diferencia la reabre con otro ADR. A-28 sigue ABIERTA.
>
> 8. La deuda «EL BROKER SIMULADO LLENA AL INSTANTE…»: sale PAGADA a HISTORIA, con las filas 36, 37, 45 y 46 y el ADR.
>
> 9. DEMO-FTMO.md: acepto las tres correcciones de la fase 0. Añade lo del punto 5.
>
> 10. Next Action: la propuesta va al informe, para la orden de cierre, y no se toca ahora. A queda reescrita como propones; S anota que la ejecución 1 está hecha; entra la pregunta P-D1 para Aleks.
>
> Cierre de la rama:
> - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO, antes de cada commit.
> - Si tocas algo de src/, empuja como fix/demo-ejecucion-1 y pasa la CI de Linux. Si solo cambian knowledge, tests, el script y el lector, dilo y no hace falta.
> - Pasa el revisor (subagente revisor), con este alcance: cada valor cambiado sale de una fila del CSV; nada que dependa de la fecha se cierra; la negativa con el stops level UNKNOWN sigue probada; el script 1.1 solo cambia lo autorizado; el lector lee 1.0 y 1.1. Pega su informe al final del tuyo.
>
> Rama lista para revisión, NO cerrada.

## 3. Fase 1

### 3.1 ADR-0071 (commit propio, antes que los valores)

`docs/adr/0071-lo-que-fija-la-ejecucion-1-de-la-demo-de-ftmo.md` y su fila en `docs/adr/README.md`.
Lleva lo propuesto en §0.i y, por el punto 1 de la respuesta, la cuenta del volumen máximo (su §2):
con `riesgo_por_operacion` 0,5 % sobre 100.000 (500 USD) y 10 USD por lote y pip de EURUSD, el lote
es 50 / stop en pips, y el tope de 50 corta todo stop de menos de 1 pip; con 1 pip exacto pasa
(`broker.py:857`, `lotes > volumen_max_lotes`). El contrato se amplía en este commit con lo que toca
la fase 1 (y `src/` entero pasa a protegido: nada de la fase 1 lo toca).

## Estado

EN CURSO: fase 1. Hecho: ADR-0071. Siguen los valores (registro, perfil, A-27), los tests, el script
1.1 y su lector, y el revisor.
