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

> **Nota (fase 1, revisor a2).** Las referencias `MedirDemoFTMO.mq5:NNN` de esta fase 0 (y de la
> nota del §0.a) son del script **1.0**, el de `main` en e5a2261 y el que corrió en la ejecución 1.
> La 1.1 de esta rama mueve las líneas: por ejemplo, `FileOpen` pasa de la 756 a la 809 y
> `InpEsperaStopSeg` de la 30 a la 36. Para leerlas: `git show main:tools/mql5/MedirDemoFTMO.mq5`.

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

### 3.2 Los valores, A-27 y los tests (commit propio, `Fuente: ADR-0071`)

**Cada valor, con su fila del CSV** (puntos 2, 3, 4, 5 y 7 de la respuesta):

| fichero | parámetro | antes | después | fila |
|---|---|---|---|---|
| `knowledge/spec/parametros.yaml` | `instrumento_digitos` | 5, DEFAULT_AMBIGUOUS, ADR-0026, A-27 | 5, CONFIRMED, ADR-0071 | 6 |
| ídem | `instrumento_contrato` | 100000, ídem | 100000, CONFIRMED, ADR-0071 | 8 |
| ídem | `instrumento_lote_minimo` | 0.01, ídem | 0.01, CONFIRMED, ADR-0071 | 9 |
| ídem | `instrumento_lote_paso` | 0.01, ídem | 0.01, CONFIRMED, ADR-0071 | 11 |
| ídem | `instrumento_stops_level` | 0, ídem | 0, CONFIRMED, ADR-0071 | 4 |
| `knowledge/cuentas/ftmo-2step-swing-100k.yaml` | `firma_stops_level_puntos` | UNKNOWN | **0**, CONFIRMED, ADR-0071 | 4 |
| ídem | `firma_volumen_max_lotes` | **100**, ADR-0050 (la web) | **50**, ADR-0071 | 10 |
| ídem | `firma_comision_por_lado` | true, supuesto conservador, ADR-0050 | true, MEDIDO, ADR-0071 (solo la descripción) | 53, 54 |
| ídem | `firma_comision_usd_por_lote` | 5, ADR-0050 | **sin cambio** (5, ADR-0050); la descripción dice que la medida excluye 5 por lado y que queda como supuesto conservador | 53, 54 |

`spec_version` 15.9.0 → **15.9.1** (parche: solo cambian estado y fuente, `knowledge validate` lo
exige al cambiar el hash) y `spec manifest --escribir`; `spec docs --escribir` regenera
`docs/spec/ambiguedades.md` y `docs/spec/parametros.md`. El contrato añade
`knowledge/spec/spec_manifest.yaml` en este commit.

**A-27 DECIDIDA por ADR-0071**, en los cinco sitios de `AMBIGUEDADES.md`:
1. el registro: los cinco de arriba;
2. `knowledge/spec/ambiguedades.yaml`: `estado: DECIDIDA`, `decision: ADR-0071`, `decidida_el:
   '2026-10-09'`, y la pregunta dice con qué filas y que las ejecuciones 2 y 3 y el pre-vuelo de F33
   vuelven a leer la ficha (una diferencia la reabre con otro ADR); sigue `clase: medicion` y su fuente
   documental (R11);
3. la regla de la spec que la cita: **ninguna** (medido: `grep A-27 knowledge/spec/strategy_spec.yaml`
   no da nada). RN-026 usa `instrumento_stops_level`, pero no cita A-27, y su nota («hay que volver
   a medirlo en la cuenta fondeada») sigue siendo verdad (F33); no se toca la spec de reglas;
4. `PROJECT_STATE.md`, «Known Ambiguities»: sale la fila de A-27;
5. la hoja de preguntas: no la llevaba (`scripts/hoja_preguntas.py`, sin A-27; es una medición).
Más `tests/unit/test_kit.py`: A-27 entra en el conjunto de DECIDIDAS, y el test de A-27 y A-28 dice
DECIDIDA (con `decision` ADR-0071 y `clase` medicion) y ABIERTA. **A-28 sigue ABIERTA.**

**`PROJECT_STATE.md` y HISTORIA** (puntos 3, 4 y 8): sale de Technical Debt la deuda «EL BROKER
SIMULADO LLENA AL INSTANTE...» (PAGADA, condición (a), filas 36, 37, 45 y 46); sale A4 de
Pendientes heredados (condición (c), SUSTITUIDA, ADR-0071 y fila 4); las dos, literales, al final de
HISTORIA con su evidencia. El pendiente 37 añade, tras su arranque literal, el máximo nuevo y la
cuenta: «· Desde ADR-0071 (2026-10-09) el maximo es 50 lotes, no 100: con riesgo_por_operacion (0,5 %)
sobre 100.000 y 10 USD por lote y pip, corta todo stop de menos de 1 pip (ADR-0071 §2)». `Tests
Currently Passing`: 1418 → 1420. La Next Action no se toca (punto 10).

**Los tests cambiados por P3** (punto 3 de la respuesta). Con `firma_stops_level_puntos` = 0 en el
perfil real, un `stops_level_diagnostico` sobre ese perfil lo rechaza el bróker («ya esta fijado»), y
la negativa por defecto ya no salta con él. Ningún test de la negativa se borra:

| test | antes | después | por qué sigue protegiendo lo mismo |
|---|---|---|---|
| `test_cableado.py::test_sin_stops_level_la_orden_stop_no_se_coloca_y_lo_dice` | perfil real (stops level UNKNOWN): la stop no se coloca y el error nombra A-27 | **perfil sintético** con el stops level en UNKNOWN (`tests/unit/perfil_stops_level_unknown.py`): la misma aserción, `BrokerError` con «A-27» | la negativa es del código (`Broker._colocar`), no del perfil: se prueba con un perfil que no tiene el valor, por el mismo camino (`_motor` → `reglas_broker_de` → `Broker`) |
| `test_selector_orden_stop.py::test_la_cli_con_a47_fijada_pasa_a_pedir_a27` | CLI real con el perfil real: exit 2 y «A-27» al colocar la primera stop | la CLI carga el **perfil sintético** en lugar del real (`monkeypatch` de `cableado.cargar_perfil`, como `_registro_con_a47_unknown` con el registro): la misma aserción. La salida se pide en una subcarpeta para comprobar que no escribe nada | sigue probando que, con A-47 fijada, la puerta siguiente es la del stops level, por la CLI de verdad y con las velas reales; solo el perfil es otro. Con el perfil real la corrida ya no se pararía ahí: correría el mes entero |
| `test_perfil_cuenta.py::test_lo_que_no_esta_en_la_fuente_no_tiene_valor` | `sin_valor()` incluía `firma_stops_level_puntos` y `puntos_o_nada` daba None | sin él en `sin_valor()`, y `puntos_o_nada` da 0 | dice lo que el perfil tiene hoy |
| `test_perfil_cuenta.py::test_con_el_stops_level_unknown_puntos_o_nada_da_none` | — (nuevo) | con el perfil sintético, `puntos_o_nada` da None y el parámetro está en `sin_valor()` | la mitad del perfil de la negativa: el UNKNOWN llega al bróker como None, no como error |
| `test_perfil_cuenta.py::test_la_comision_por_lado_...` | `..._toma_el_supuesto_conservador`: la descripción decía NO ENCONTRADA y CONSERVADOR | `..._esta_medida_y_su_importe_sigue_conservador`: true, fuente ADR-0071, «MEDIDO» y las filas 53 y 54; el importe sigue en 5 y su descripción dice CONSERVADOR | lo mismo que antes (el valor es true y el importe es el conservador), con la fuente nueva |
| `test_cableado.py::test_con_el_stops_level_del_perfil_el_diagnostico_de_a27_se_rechaza` | — (nuevo) | con el perfil real y un diagnóstico de 2, `BrokerError` «ya esta fijado en 0» | la otra mitad de ADR-0057 §5: con valor fijado, no hay diagnóstico |
| `test_cableado.py::test_una_orden_stop_por_el_arnes_real_salta_al_romper_y_cierra_por_objetivo` | perfil real y `stops_level_diagnostico = 2` | perfil real, sin diagnóstico (0 del perfil) | no prueba la negativa: prueba una operación stop de punta a punta, y ahora por la vía real. Mismas aserciones, en verde |
| `test_cableado.py::test_rn011_con_el_selector_en_stop_de_punta_a_punta_por_el_arnes` | ídem, diagnóstico 2 | ídem, sin diagnóstico | ídem |
| `test_cableado.py::test_con_el_selector_en_stop_y_el_precio_ya_roto_la_orden_se_rechaza` | diagnóstico 0 | sin diagnóstico (el 0 del perfil) | el mismo 0, ahora medido; mismo rechazo por `precio_invalido` |
| `test_orden_stop_pivote.py::_cadena` y `test_la_cadena_colocada_cancelada_recolocada_y_llenada_por_el_cableado` | diagnóstico 2 en los dos motores | sin diagnóstico | no prueban la negativa (la cadena de la orden stop, ADR-0064); mismas aserciones, en verde |
| `test_renovar_cierres.py::test_simular_un_dia_posterior_a_hasta_sale_con_2_y_lo_nombra` | `--diagnostico-a27 0` en la CLI | sin esa opción | con el perfil real la opción se rechaza; el test prueba el calendario de cierres, que se niega antes |

**Dos tests más, que el primer `make check` de este commit dio en rojo** (2 fallidos de 2456):

| test | antes | después | por qué |
|---|---|---|---|
| `test_spec_fidelidad.py::test_las_mediciones_no_entran_en_el_cuestionario` | leía la clase de A-16, A-27 y A-28 solo entre las ABIERTAS (`KeyError: 'A-27'`) | la lee de todas | A-27 está DECIDIDA y sigue siendo una medición; lo que el test protege (que las mediciones no lleguen al cuestionario) no cambia, y la aserción de que ninguna de las tres entra en él sigue igual |
| `tests/regression/test_cuenta_7_de_agosto.py` | el bróker con las reglas del perfil real | el bróker con las reglas del perfil real **salvo** `volumen_max_lotes`, que se fija en 100, el tope del perfil hasta hoy, declarado en el test (`VOLUMEN_MAX_DE_LA_REGRESION`) | ver el hallazgo de abajo: la regresión es del corte de la cuenta en el tick del pico (`trabajo/corregir-evaluar-fase`), no del volumen; con el tope de antes vuelve a probar exactamente lo mismo, con las mismas aserciones |

> **HALLAZGO para el consultor: el volumen máximo de 50 rechaza una operación real del trader.**
> Esa regresión repite por el bróker, con `abrir_conocida`, las cuatro operaciones del trader del
> 2026-08-07 (agosto es material de DESARROLLO, `CLAUDE.md`), dimensionadas al 0,5 % de 100.000
> hasta el stop inicial. Con el perfil nuevo, el bróker rechazó la primera: `BrokerError: t1: el
> perfil no admite esta posicion (volumen_max_lotes)`. Por la cuenta de ADR-0071 §2, su stop queda
> por debajo de 1 pip. Es justo el caso que el pendiente 37 tiene que resolver (qué hace el bot
> cuando el lote pasa del máximo: A-18), y ya no es hipotético. No se ha medido nada más de esa
> operación (ni su stop ni su lote); el dato es el mensaje del test.

Los tests del bróker que usan reglas sintéticas (`test_broker_ordenes_stop.py`: sin stops level la
stop no se coloca; con uno en diagnóstico se exige la distancia; con uno fijado no se admite
diagnóstico) no cambian: construyen `ReglasBroker` a mano y no leen el perfil.

### 3.3 El script 1.1, su lector y `DEMO-FTMO.md` (punto 5 y 9; commit propio)

**`tools/mql5/MedirDemoFTMO.mq5`, 1.0 → 1.1. Solo lo autorizado** (`git diff main --
tools/mql5/MedirDemoFTMO.mq5`):
- `VERSION_SCRIPT` "1.1" y `#property version` "1.10";
- un input nuevo, `InpVolumenComision = 1.00`, y el paso 6 abre con él (`req.volume = volumen`; antes
  `g_volumen`, el mínimo). El cierre ya cerraba el volumen de la posición (`CerrarPosicion` usa
  `POSITION_VOLUME`) y no cambia. El stop de protección (200 puntos) y la apertura y el cierre
  enseguida (3 s) siguen igual;
- **antes de abrir**: que el volumen sea admisible (mínimo, máximo y paso del símbolo,
  `VolumenAdmitido`) y que el margen alcance (`OrderCalcMargin` frente a `ACCOUNT_MARGIN_FREE`,
  `MargenAlcanza`). Una fila nueva, `volumen_comision`, escribe el volumen y, en su nota, el margen
  necesario y el libre (o por qué no se admite). **Si no alcanza, no abre**: la fila
  `apertura_compra_mercado` lleva `no_abre` y el motivo, y el paso termina sin error;
- las dos filas de observación (`buy_stop_llenado`, llenada o «no_salto») escriben «OBSERVACION» en
  `retcode_texto` en vez de «SIN_RESPUESTA», con un parámetro nuevo de `Fila` (`observacion`, falso
  por defecto). `TextoRetcode(0)` sigue diciendo SIN_RESPUESTA para una petición sin respuesta de
  verdad;
- los comentarios de la cabecera: qué trae la 1.1 y la línea de SEGURIDAD («solo el volumen mínimo»
  ya no era exacta).
**Lo que va más allá de la letra del punto 5, y por qué** (revisor, a3): la comprobación de que el
volumen sea admisible (`VolumenAdmitido`) y la fila `volumen_comision`. La respuesta pide el input y
la comprobación del margen; sin la primera, un volumen mal escrito en la ventana de Aceptar llegaría
al servidor y volvería con un retcode de volumen en vez de un «no abre» explicado; sin la segunda, el
lector no sabría con cuántos lotes se midió la comisión (la 1.0 no lo escribía). Las dos sirven a lo
autorizado y no tocan ningún otro paso; si el consultor no las quiere, se quitan en una línea cada una.

Nada más: los pasos 1-5 y 7, la limpieza y las comprobaciones de arranque no cambian. **El script no
se compila en el repositorio** (MetaEditor solo está en la máquina de Aleks): la comprobación es el
F7 con «0 errors» que pide `DEMO-FTMO.md`.

**`scripts/leer_demo_ftmo.py`**: lee la 1.0 y la 1.1 y rechaza cualquier otra versión, o un
fichero que mezcle dos; dice la versión junto a cada fichero; una fila nueva de la tabla, «lotes de
la compra a mercado» (el de `volumen_comision` en la 1.1; en la 1.0, el volumen mínimo, que es lo que
usaba); la compra que no abre sale como «no abrio: <motivo>»; y la etiqueta de las observaciones de
la 1.0 (SIN_RESPUESTA) se lee como OBSERVACION. La tabla de la 1.0 no cambia salvo esas dos cosas
(la versión y la fila de los lotes).

**`tests/unit/test_leer_demo_ftmo.py`**: los cinco tests de antes, sin tocar sus aserciones (el
generador de filas gana un parámetro `version`, por defecto "1.0"), y cuatro nuevos sobre CSV
sintéticos: la 1.1 con 1,00 lote y la observación; la 1.1 sin margen (no abre y lo dice, sin
retcode inesperado); la 1.0 con la etiqueta nueva y el volumen mínimo; y otra versión o una mezcla,
rechazadas. 1424 funciones de test.

**`docs/runbooks/DEMO-FTMO.md`** (punto 9): las tres correcciones de la fase 0 se quedan; se añade
que el paso 6 va con 1,00 lote desde la 1.1 (en «Lo que hace» y en la tabla de pasos) y, en «Cuándo»,
lo que Aleks hace antes de la ejecución 2: copiar otra vez el script, compilarlo con F7 hasta «0
errors» y comprobar que el CSV dice 1.1.

**La guardia de Claude Code bloquea ejecutar el lector nuevo, y es un falso positivo.** Al lanzar
`uv run python scripts/leer_demo_ftmo.py data/demo_ftmo` con el lector cambiado, la guardia lo niega:
«el codigo que se ejecuta pide el corpus SIN FILTRAR». Su patrón (`CRUDO_PYTHON`,
`.claude/hooks/guardia.py:162`, `\bcrudo\s*=\s*(?!False\b)\S`) casa con la línea
`crudo = ruta.read_bytes()` del lector, que está en `main` desde `trabajo/demo-ftmo-script`: una
variable local con los bytes del CSV, no la opción de la CLI que enseña el corpus. Mientras el lector
era idéntico al de `main` la guardia lo daba por revisado; al cambiar en esta rama, lo lee y salta.
**No se rodea** (`CLAUDE.md`, «Una guardia no se rodea»): ni se renombra la variable para que no la
vea ni se ejecuta el lector por otro camino. El lector nuevo lo prueban los nueve tests del lector
con CSV sintéticos; la tabla de la ejecución 1 del §0.a es la del lector 1.0. Para el consultor: o
se renombra esa variable en una rama (y así el lector deja de parecer lo que no es), o se afina el
patrón de la guardia en la suya. Aleks puede ejecutarlo en su terminal con `!`.

## 4. La Next Action, propuesta para la orden de cierre (punto 10: no se toca ahora)

Literal, para el commit del contrato (RITUAL punto 3), si la orden de cierre lo manda:

- **A, reescrita:** «A. **Demo de FTMO: las ejecuciones 2 y 3 de MedirDemoFTMO** (las hace Aleks;
  docs/runbooks/DEMO-FTMO.md). La ejecución 1 se hizo el 2026-10-09 en la prueba gratuita del
  2026-10-08 y fijó lo que no depende de la fecha (ADR-0071, docs/validation/DEMO-EJECUCION-1.md;
  A-27 DECIDIDA). Las 2 y 3, en una segunda prueba creada el 26 de octubre desde el mismo registro,
  con el script 1.1 (copiarlo, compilarlo con F7 y comprobar que el CSV dice 1.1): la 2 entre el 26 y
  el 30 de octubre, la 3 después del 1 de noviembre. Miden A-28 (el desfase en invierno y el
  calendario del servidor: 180 min el 2026-10-09), repiten el nivel exacto de ADR-0057 §2 (filas
  39-42), los deslizamientos (DN-3) y los swaps, y la 2 mide la comisión con 1,00 lote (ADR-0071 §3).
  Con cada CSV, rama para congelarlo y fijar lo que mida; si la ficha de EURUSD difiere, A-27 se
  reabre con otro ADR.»
- **S, una frase añadida al final:** «La ejecución 1 de la demo de FTMO está hecha (2026-10-09,
  ADR-0071).»
- **Nueva, para Aleks con FTMO (la letra la elige el consultor):** «**Pregunta P-D1 a FTMO, la manda
  Aleks** (el repositorio guarda la paráfrasis de la respuesta, como RESPUESTAS-FTMO): la cuenta FTMO
  Challenge 2-Step Swing en MT5, ¿es de cobertura (hedging), como la prueba gratuita, o de
  compensación (netting)? Y en EURUSD, ¿el volumen máximo por orden es de 50 lotes, como en la
  prueba, o de 100, como dice la tabla de símbolos de la web? (docs/validation/DEMO-EJECUCION-1.md
  §0.c, ADR-0071 §2 y §7).»
- **M** se queda como está (§0.h). A4 y la deuda de la límite ya salieron en esta rama (§3.2).
- **Para decidir (no es propuesta de texto):** la guardia que niega ejecutar el lector cambiado
  (§3.3), y el rechazo por volumen máximo de la operación del 7 de agosto (§3.2, HALLAZGO), que
  concreta el pendiente 37.

## 5. Comprobaciones

- **Commits de la rama** (`git log --format=%h main..HEAD`): a59408b (apertura), e99ad4b (fase 0),
  d5a31d1 (ADR-0071), e5c549d (valores, A-27 y tests), d48150e (script 1.1 y lector), y el de este
  informe con el del revisor. Cada uno con `make check` en verde y su línea SELLO antes del commit:
  2454, 2454, 2454, 2456 y 2460 tests pasados.
- **Los `make check` en rojo, y por qué** (ninguno se commiteó): el primero de la fase 0, por citar
  `ADR-0071` antes de que existiera (5 tests, §1); en el commit de los valores, uno por `ruff` (una
  línea larga y el formato de dos líneas de `test_cableado.py`) y otro con 2 tests (los del §3.2,
  «Dos tests más»); y uno que se paró a mano porque la guardia había bloqueado el `git add` que iba
  delante en el mismo comando y corría sin los ficheros estadiados.
- **El CSV:** `sha256sum data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv` da
  `86f0df8b24f632102f0207b62a298a7776a164868e9a2d820ceb133c144b3c6e`, el del manifiesto.
- **`src/` no cambia** (`git diff --stat main -- src/` vacío): solo knowledge, docs, tests, el
  script y el lector. **Por eso no se empuja como `fix/demo-ejecucion-1` ni hace falta la CI de
  Linux** (respuesta del consultor, «Cierre de la rama»).
- **Nadie ejecutó `botsito motor arnes`** en esta rama, ni para medir. Los tests que ya lo hacían
  (`test_selector_orden_stop.py`, `test_preparar_a35.py`) corren dentro de `make check`, como
  siempre; el de la CLI con A-47 fijada sigue parándose en la primera orden stop porque lleva el
  perfil sintético.
- **`knowledge validate`** sin errores y **`state check`** en verde (1424 funciones de test).

### 5.1 Lo hecho con cada hallazgo del revisor

| # | gravedad | lo hecho |
|---|---|---|
| a1 | importa | Sin arreglo en esta rama: corregir la guardia o renombrar la variable del lector es una decisión del consultor (§3.3, y §4 «Para decidir»). La comprobación del contrato que la guardia niega se queda listada tal cual, para que quede a la vista; su evidencia sustituta son los nueve tests del lector. |
| a2 | menor | Nota al principio del §0: las líneas del script que cita la fase 0 son de la 1.0, y cómo leerlas. |
| a3 | menor | El §3.3 dice qué va más allá de la letra del punto 5 (`VolumenAdmitido` y la fila `volumen_comision`) y por qué. |
| a4 | menor | ADR-0071 §3 dice que las dos exclusiones suponen una comisión proporcional y sin mínimo, que lo comprueba la ejecución 2, y que la conclusión práctica no depende de ello. |
| a5 | menor | La fila de ADR-0057 en `docs/adr/README.md` anota qué partes quedan medidas por ADR-0071 y cuál sigue PROVISIONAL. El ADR no se edita. |
| a6 | menor | El pendiente 37 separa con «·» su arranque truncado del texto nuevo. |
| b1 | menor | Sin cambio: P-D1 entra en la Next Action con la orden de cierre (punto 10), y el texto está en el §4. Hasta entonces vive en el informe y en la descripción de `firma_volumen_max_lotes`. |

## 6. Informe del revisor

Pegado tal cual (subagente `revisor`, sobre HEAD d48150e más este informe estadiado):

## Informe del revisor · trabajo/demo-ejecucion-1 · 2026-10-09

Base: merge-base con main = e5a2261. HEAD = d48150e. Sobre el árbol de HEAD (95eeb8c) hay un `make-check.log` con SELLO, `2460 passed` y `exit=0`. Estadiado y sin commitear solo está `docs/validation/DEMO-EJECUCION-1.md`, que no está en ese sello.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 5 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El contrato lista una comprobación que la guardia niega ejecutar.** `contrato.yaml` incluye `uv run python scripts/leer_demo_ftmo.py data/demo_ftmo`, pero con el lector cambiado la guardia la bloquea. No la rodeé. El informe §3.3 lo explica y lo deja al consultor. Hasta que se renombre `crudo = ruta.read_bytes()` o se afine `CRUDO_PYTHON`, ninguna sesión puede ejecutar esa comprobación del contrato. | `contrato.yaml:57`. Mi ejecución: «GUARDIA … bloquea: el codigo que se ejecuta pide el corpus SIN FILTRAR». `scripts/leer_demo_ftmo.py:97`: `crudo = ruta.read_bytes()`. `.claude/hooks/guardia.py:162`: `CRUDO_PYTHON`. En main la línea es la 84 y es idéntica. |
| a2 | menor | **Las referencias `MedirDemoFTMO.mq5:NNN` del informe son del script 1.0 y no lo dicen.** Con la 1.1 ya no apuntan a lo citado. El informe cita `:756`, `:118`, `:132`, `:30`, `:66`, `:267`, `:111` y `:684-688`. En la 1.1 son `:809` (FileOpen), `:36` (`InpEsperaStopSeg`), `:73` (`TextoRetcode(0)`) y `:275` (`req.position`). | `grep -n` sobre el fichero de la rama frente a `git show main:…`. |
| a3 | menor | **El script 1.1 añade algo que la respuesta no lista.** Es la comprobación `VolumenAdmitido` (mínimo, máximo y paso) y la fila nueva `volumen_comision`. La respuesta pedía margen libre y «no toques nada más». El informe §3.3 lo describe pero no lo señala como añadido ni dice por qué. Es coherente con lo autorizado: el lector necesita la fila, y sin la comprobación un input mal puesto daría un retcode. | `git diff main -- tools/mql5/MedirDemoFTMO.mq5`, hunks `VolumenAdmitido` y `MedirComision`. Informe §3.3. |
| a4 | menor | **ADR-0071 §3 «excluye como hecho los 5 USD por lado» supone, sin decirlo, que la comisión es lineal en el volumen y sin mínimo por deal.** Con 0,01 lotes y 0,03 USD no se puede distinguir. La ejecución 2 (1,00 lote) lo comprueba. La conclusión práctica (el 5 sigue siendo conservador) no se ve afectada. | ADR-0071 §3. Filas 53 y 54 del CSV: `-0.03` con volumen mínimo. |
| a5 | menor | **El índice de ADR no recoge que ADR-0057 pasa en parte a medido.** ADR-0071 §4 declara §3 MEDIDO. La fila de ADR-0057 sigue diciendo «PROVISIONAL hasta la demo de FTMO», y su cabecera igual. Es coherente con que un ADR no se edita, pero el índice sí admite anotaciones, como la de 0037. | `docs/adr/README.md:63`. ADR-0071 §4. |
| a6 | menor | **La línea del pendiente 37 en `PROJECT_STATE.md` queda con el texto nuevo pegado tras el «…» de truncado**, lo que se lee como una línea cortada. | `PROJECT_STATE.md:67`. |

**Comprobado sin hallazgos:**
- **Contrato.** `uv run python scripts/contrato_rama.py`: «CONTRATO: 30 ficheros dentro del contrato de trabajo/demo-ejecucion-1 (riesgo alto, artefacto docs/validation/DEMO-EJECUCION-1.md, 8 comprobaciones para el revisor)».
- **Comprobaciones del contrato.** `sha256sum` del CSV da `86f0df8b…3c6e`, igual al manifiesto (9.907 bytes, 59 filas). `pytest` de los seis ficheros de tests: todo en verde, sin saltos. `knowledge validate` sin errores; los AVISO son los de siempre y ninguno es de esta rama. `state check`: OK. `git log` y `git diff main -- tools/mql5/MedirDemoFTMO.mq5` ejecutados.
- **`make check`.** `make-check.log`: línea 96 `SELLO … árbol 95eeb8c…`, que es `HEAD^{tree}`; línea 72 `2460 passed`; línea 97 `PICO DE MEMORIA 294 MiB`; `exit=0`.
- **Trailer `Fuente:`.** El único commit que toca `knowledge/spec/` (e5c549d) lleva `Fuente: ADR-0071` en el cuerpo. El ADR existe y se commiteó antes (d5a31d1).
- **Material protegido.** Ni holdout, ni libros, ni fotogramas, ni transcripciones en la rama. No hay filas nuevas en `HOLDOUT-EXPOSICIONES`, porque no se abrió nada.
- **Regímenes de cambio.** `data/manifests/`: solo `A` para el `.yaml` y `M` para `README.md`, que no es protegido. `knowledge/evidence`, `feedback`, `cases`, `corpus` y `simulador` sin tocar. `HISTORIA.md`: 212 líneas añadidas y 0 borradas. `libros.yaml` no se toca.
- **Ambigüedades (cinco sitios).**
  - El YAML pasa A-27 a DECIDIDA, con `decision: ADR-0071` y `decidida_el`.
  - El registro lleva los cinco parámetros.
  - Ninguna regla cita A-27 (`grep` en `strategy_spec.yaml` sin resultados).
  - `PROJECT_STATE` sin la fila de A-27.
  - La hoja de preguntas no lleva A-27.
  - `docs/spec/ambiguedades.md` va en el mismo commit (ABIERTA 22, DECIDIDA 7).
  - `test_kit` actualizado. A-28 intacta: `estado: ABIERTA`.
- **ADR.** `## Estado` = `ACTIVE`.
- **Informes cerrados.** Ninguno cambia; `DEMO-EJECUCION-1.md` es nuevo.
- **Guardias de `cita`.** Sin sitios nuevos con `cita`.
- **Cifras.** El perfil es el sitio de las cifras de la firma. No hay literales de negocio nuevos.
- **Evidencia nueva.** No hay ítems nuevos en `knowledge/evidence/`; el punto 10 no aplica.
- **Informe.** Existe y acaba en `## Estado` (EN CURSO).
- **Tres citas del informe contra su fuente.** `broker.py:857`, `:449` y `:270-275` coinciden. HISTORIA línea 538 coincide con el texto de la deuda. `strategy_spec.yaml:1353-1355` coincide con `ninguno_de`.
- **Cifras del CSV citadas en el ADR.** Todas casan con su fila: 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 21-23, 25, 31, 34-37, 39-46, 49, 51, 53, 54, 56-59.

### Eje (b) · Encargo
Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 16 hechos, 0 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde el `main` actual, con `abrir-rama`: encargo, contrato y archivo en HISTORIA | Hecho | `a59408b`. El encargo existe. El contrato pasa. HISTORIA tiene el Archivo 25. |
| 2 | 0.a Congelar el CSV en un manifiesto con el procedimiento del repo, y pegar la tabla del lector | Hecho | Manifiesto `data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml`. Sha, bytes y filas verificados. El sha del `.mq5` (`28d58110…`) coincide con el de main. Tabla pegada en el informe §0.a. Esquema documentado en `data/manifests/README.md`. |
| 3 | 0.b Tabla medida → decisión, fila a fila, con los mínimos pedidos | Hecho | Informe §0.b. Contrasté contra el CSV las filas 4-19, 24, 25 y 34-57. |
| 4 | 0.c Corregir «Netting o hedging» y medir qué supone el simulador | Hecho | `DEMO-FTMO.md` ahora dice «HEDGING … medido». Informe §0.c: posiciones independientes, `ninguno_de` en RN-011, y la pregunta P-D1 a FTMO. |
| 5 | 0.d Comparar la fila 41 con la deuda «LLENA AL INSTANTE» | Hecho | Informe §0.d: la paga entera con las filas 36, 37, 45 y 46, y la 41 se trata como otro caso. Verificado en el CSV. |
| 6 | 0.e Explicar la fila 57 (retcode 0 «SIN_RESPUESTA») | Hecho | Informe §0.e: es lo esperado. |
| 7 | 0.f Anotar el desfase de 180 min como primera de tres medidas, sin cerrar A-28 | Hecho | Informe §0.f. A-28 sigue ABIERTA. |
| 8 | 0.g Decidir sobre el pendiente heredado A4 | Hecho | Informe §0.g. A4 sale por la condición (c) con ADR-0071 y la fila 4 (punto 3 de la respuesta). |
| 9 | 0.h Decir si se mide la Next Action M | Hecho | Informe §0.h: no se mide, M se queda. |
| 10 | 0.i Propuesta de valores, ambigüedades, deudas, Next Action y texto de `DEMO-FTMO.md`, y PARADA | Hecho | Informe §0.i y §1. |
| 11 | Fase 1, puntos 0, 1 y 2 de la respuesta: nota del hash del original, ADR nuevo con la cuenta de 1 pip, y los cinco del registro a CONFIRMED | Hecho | Informe §0.a (nota añadida) y §1 (nota «ADR-D1»). ADR-0071 §2 con la cuenta 50/stop. Diff de `parametros.yaml`. |
| 12 | Puntos 3 y 4: stops level a 0, volumen máximo a 50, negativa probada con un perfil sintético, A4 a HISTORIA, pendiente 37 y P-D1 | Hecho | Perfil: `firma_stops_level_puntos` pasa a CONFIRMED 0 y `firma_volumen_max_lotes` a 50. Existe `tests/unit/perfil_stops_level_unknown.py`. A4 va a HISTORIA. El pendiente 37 en `PROJECT_STATE` lleva el 50 y la cuenta. P-D1 queda en el informe §4 para la orden de cierre. |
| 13 | Punto 5: el importe de la comisión no cambia y solo cambia la descripción de `firma_comision_por_lado` | Hecho | `firma_comision_usd_por_lote` sigue en 5 con fuente ADR-0050. Solo cambia su descripción, que dice «excluye 5 por lado». |
| 14 | Punto 5, script 1.1: input por defecto 1.00, versión 1.1, margen libre y no abrir, etiqueta OBSERVACION; lector que lee 1.0 y 1.1 con test sintético; `DEMO-FTMO.md` | Hecho | Diff del script y del lector. `test_leer_demo_ftmo.py` tiene 4 tests nuevos (1.1 con 1,00 lote, 1.1 sin margen, 1.0 con etiqueta nueva, versión ajena o mezcla). `DEMO-FTMO.md` «Antes de la ejecución 2». |
| 15 | Puntos 6, 7, 8 y 9: P6, P7 y P8 sin cambio; A-27 DECIDIDA en los cinco sitios con `spec docs --escribir`; deuda PAGADA; correcciones de `DEMO-FTMO.md` | Hecho | Swaps, `llenado.yaml` y ADR-0057 sin tocar. El ADR los anota. Cinco sitios y docs regenerados en el mismo commit. Deuda en HISTORIA. |
| 16 | Punto 10: la Next Action no se toca y la propuesta va al informe | Hecho | `git diff -U0 -- PROJECT_STATE.md`: ningún hunk entre las líneas 23 y 50. El informe §4 tiene la propuesta literal. |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | menor | **P-D1 no queda en ningún sitio durable de la rama.** La respuesta (punto 4) dice que la pregunta «entra como pendiente para Aleks», y el punto 10 la manda a la Next Action en la orden de cierre. Entre tanto solo vive en el informe §0.c y §4, y en la descripción del perfil. Sigue lo ordenado; conviene tenerlo presente al cerrar. | Informe §4; `ftmo-2step-swing-100k.yaml` (descripción de `firma_volumen_max_lotes`). |

**Nada fuera del encargo sin justificar.** Lo extra está declarado en el informe: `test_spec_fidelidad.py` y la regresión del 7 de agosto (§3.2, «Dos tests más», con el contrato ampliado), el parche de `spec_version` 15.9.1, y las correcciones de `DEMO-FTMO.md`. `src/` entero sin cambios (`git diff --stat main -- src/` vacío). La rama no toca `strategy_spec.yaml`, `knowledge/simulador/`, corpus, holdout, evidencia ni feedback.

### Los seis puntos de alcance

**1. Cada valor cambiado sale de una fila del CSV.** Sin hallazgos.

| Parámetro | Valor nuevo | Fila del CSV |
|---|---|---|
| `instrumento_digitos` | 5 | 6 (`digits` 5) |
| `instrumento_contrato` | 100000 | 8 (100000.00) |
| `instrumento_lote_minimo` | 0.01 | 9 |
| `instrumento_lote_paso` | 0.01 | 11 |
| `instrumento_stops_level` | 0 | 4 |
| `firma_stops_level_puntos` | 0 | 4 |
| `firma_volumen_max_lotes` | 50 | 10 (50.00) |
| `firma_comision_por_lado` | true (solo la descripción) | 53 y 54 (−0.03 y −0.03) |

Las filas que citan las descripciones del perfil y del registro, y las de ADR-0071, casan con el CSV. `firma_comision_usd_por_lote` queda en 5; solo cambia su descripción.

**2. Nada que dependa de la fecha se cierra.** Sin hallazgos.
- A-28 sigue `ABIERTA` en `ambiguedades.yaml:699`.
- `firma_swap_largo_puntos` y `firma_swap_corto_puntos` no cambian.
- `knowledge/simulador/llenado.yaml` (DN-3) no se toca.
- ADR-0057 no se toca, y el nivel exacto (§2) queda «SIGUE PROVISIONAL» en ADR-0071 §4.
- El desfase de 180 min se anota como primera de tres medidas.

**3. La negativa del bróker con el stops level UNKNOWN sigue probada.** Sin hallazgos.
- `git diff main -- tests/` no borra ninguna función de test. La única que desaparece es `test_la_comision_por_lado_toma_el_supuesto_conservador`, renombrada y con aserciones nuevas; el informe lo declara en su tabla.
- `test_sin_stops_level_la_orden_stop_no_se_coloca_y_lo_dice` conserva su nombre y su aserción (`BrokerError` con «A-27») sobre el perfil sintético.
- `test_la_cli_con_a47_fijada_pasa_a_pedir_a27` conserva `exit 2` y «A-27» con el perfil sintético inyectado. Esa inyección funciona porque `cableado.py:429` llama a `cargar_perfil` por el global del módulo.
- `test_con_el_stops_level_unknown_puntos_o_nada_da_none` es nuevo.
- `test_broker_ordenes_stop.py` (reglas sintéticas) no cambia.
- Los demás cambios están en la tabla del informe §3.2 y coinciden con el diff. Los antes y después son fieles.
- Los tests que usaban un diagnóstico de 2 sobre el perfil real ya no ejercitan el rechazo por distancia al stops level de punta a punta. Ese camino sigue en `test_broker_ordenes_stop.py`.

**4. El script 1.1 solo cambia lo autorizado.** Cambia lo siguiente.
- `VERSION_SCRIPT` a 1.1 y `#property version` a 1.10.
- El input `InpVolumenComision = 1.00`; el paso 6 abre con él.
- `VolumenAdmitido` y `MargenAlcanza`; si no alcanza, la fila `apertura_compra_mercado` lleva `no_abre` y el paso termina sin error.
- La etiqueta OBSERVACION en las dos filas de `buy_stop_llenado`.
- Los comentarios de cabecera.

No cambian el paso 7 (`g_volumen`, línea 694), `CerrarPosicion` (usa `POSITION_VOLUME`), la limpieza ni las comprobaciones de arranque. Lo no listado en la respuesta es lo de a3. El script no se compila en el repositorio, así que el F7 con «0 errors» lo hace Aleks.

**5. El lector lee 1.0 y 1.1.** Sin hallazgos. Los cuatro tests nuevos pasan: 1.1 con 1,00 lote y OBSERVACION, 1.1 sin margen, 1.0 con la etiqueta nueva y el volumen mínimo, y versión ajena o mezcla rechazadas. Los cinco antiguos conservan sus aserciones. No pude ejecutar el lector sobre el CSV real por la guardia (a1). La tabla pegada en §0.a la hizo el lector 1.0, y el código de lectura 1.0 está cubierto por los tests sintéticos.

**6. La entrada A sigue en pie para las ejecuciones 2 y 3.** Sin hallazgos.
- `PROJECT_STATE.md:39` conserva A tal cual, con «Las ejecuciones 2 y 3, en una segunda prueba creada el 26 de octubre».
- La propuesta de reescritura está en el informe §4.
- La Next Action no se tocó: ningún hunk entre las líneas 23 y 50.
- Cambian Current Branch y Current Feature, el recuento de tests (1424), el pendiente 37 y la fila de A-27, que sale.

### Lo que no pude comprobar
- **El lector 1.1 sobre el CSV real**, por la guardia (a1). Evidencia sustituta: los nueve tests del lector, todos en verde.
- **Que el `.mq5` compile.** MetaEditor solo está en la máquina de Aleks.
- **Lo que declara Aleks:** el sha `certutil` del original, la hora, los 45 s, el balance de 99.999,75 USD y el título «Hedge». El CSV confirma la hora, el «completo», los 44 s y el cero de abiertas; el balance no está en el CSV.
- **Por qué el CSV sale con LF si el script escribe `\r\n`.** El informe lo deja como hecho medido, y yo no tengo acceso a la documentación de MQL5 que cita.
- **Los `make check` de los commits anteriores a d48150e.** Solo existe el log del último.
- **Si el árbol del sello coincide con el estadiado en su momento.** El árbol del sello es el de HEAD, pero el informe estadiado es posterior.
- **Si la regresión del 7 de agosto rechaza por una operación con stop de menos de 1 pip.** El código del test (`lotes = 500/(distancia/escala*contrato)`) respalda la inferencia del informe, pero no ejecuté ni medí esa operación, y el informe tampoco.
- **No ejecuté `make check` ni `botsito motor arnes`.** Una nota: el test de la CLI `test_la_cli_con_a47_fijada_pasa_a_pedir_a27` invoca `cli.main(... motor arnes --simular ...)` internamente. Salió en verde al ejecutar los seis ficheros del contrato; con el perfil sintético se para en la primera orden stop.

### Comandos ejecutados
1. `git branch --show-current`, `git merge-base main HEAD`, `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `sha256sum` del CSV; `wc -c` del CSV; `git show 6460dee:…/MedirDemoFTMO.mq5 | sha256sum`, y lo mismo sobre main
4. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases knowledge/cuentas`
5. `git diff main...HEAD` sobre knowledge, tests, script, lector, `PROJECT_STATE.md`, `docs/spec/*.md`, `docs/adr/README.md`, `HISTORIA.md`, `DEMO-FTMO.md` y `data/manifests/README.md`
6. `git diff main -- tools/mql5/MedirDemoFTMO.mq5`; `git diff main -- scripts/leer_demo_ftmo.py`; `git diff main -- tests/ | grep …`
7. `uv run pytest tests/unit/test_leer_demo_ftmo.py tests/unit/test_cableado.py tests/unit/test_selector_orden_stop.py tests/unit/test_perfil_cuenta.py tests/unit/test_orden_stop_pivote.py tests/unit/test_renovar_cierres.py -q -rs -p no:cacheprovider`
8. `uv run botsito knowledge validate`; `uv run botsito state check`
9. `uv run python scripts/leer_demo_ftmo.py data/demo_ftmo`: **bloqueado por la guardia**, no rodeado
10. `grep` y `sed` sobre `make-check.log`, `broker.py`, `guardia.py`, `HISTORIA.md`, `strategy_spec.yaml` y `mq5`; `git rev-parse HEAD^{tree}`
11. `git diff --cached` y `git status --short`, que sigue siendo solo el informe estadiado
12. Dos comandos compuestos que la guardia bloqueó por la forma (`sha256sum` con `python <<EOF` detrás, y un `grep -rn` sobre una carpeta protegida); los rehice en llamadas separadas.

Fichero revisado: `C:\Users\USER\Desktop\Bot v3\docs\validation\DEMO-EJECUCION-1.md`.

## 7. Segunda respuesta del consultor y orden de cierre (2026-10-09)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Respuesta del consultor a trabajo/demo-ejecucion-1 (2026-10-09). Primero los puntos 1 a 4, con commit sellado; después, la orden de cierre de abajo, que ejecutas cuando Aleks escriba /cerrar-rama.
>
> 1. Aleks acaba de ejecutar con «!» el lector cambiado sobre el CSV real (salida arriba). Compárala con la tabla de §0.a, que se sacó con el lector de main. Solo pueden cambiar la etiqueta OBSERVACION y lo que diga la versión 1.0; cualquier otra diferencia, para y dímelo. Pega la salida y la comparación en el informe.
> 2. Regresión del 7 de agosto: se queda con el tope 100 declarado en el propio test, porque prueba el corte de la cuenta. Añade un test hermano con el perfil real (50) que compruebe que esa operación se rechaza por volumen máximo, nombrando el pendiente 37 y ADR-0071, sin fechas reservadas (agosto es construcción).
> 3. En ADR-0071 (aún no está en main, se puede completar en la rama), en sus consecuencias: volumen_limite = 0 (fila 12) dice que no hay tope sumado entre órdenes, así que la rama del pendiente 37 decide entre recortar el lote a 50 (riesgo menor que el del parámetro), partir la operación en varias órdenes o no operar. No se decide aquí.
> 4. La guardia (exigir_sin_crudo) da un falso positivo con la asignación «crudo = ruta.read_bytes()» del lector, que ya estaba en main. No se renombra la variable: eso sería rodear la guardia. Va a la Next Action (abajo). Déjalo dicho en el informe.
>
> Orden de cierre de trabajo/demo-ejecucion-1 (consultor, 2026-10-09). Tag: stable/F37i-demo-ejecucion-1 (verifica en HISTORIA que el último es F37h y que F37i no existe ni en local ni en origin).
>
> No toca src/: no hay CI de Linux, como declara el informe.
>
> Hallazgos para la fila de la rama en ERRORES-RECURRENTES, con su lección:
> 1. (importa, consultor) El perfil mantenía la comisión en 5 USD por lote y lado, «supuesto conservador hasta que FTMO confirme», y FTMO-REGLAS ya traía desde el 2026-09-28 la tarifa publicada de 2,50 por lado. Nadie revisó el supuesto, y duplicaba el coste de cada operación en las simulaciones. Lección: un supuesto con condición de caducidad («hasta que…») se revisa en la rama que trae esa condición; el revisor busca en knowledge/ los supuestos cuya condición ya se cumplió.
> 2. (importa, sesión; lo vio la sesión) El volumen máximo medido (50) rechaza una operación real del trader en una regresión. Lección: cuando un valor medido cambia un límite, se pasan las regresiones con el perfil real y lo que rompe se declara como consecuencia, no se esconde con el valor viejo.
> 3. (menor, consultor) El consultor repitió a Aleks los «unos cinco minutos» y el «Netting» sin medirlos; el CSV dio 44 segundos y HEDGING. Lección: lo que el consultor le dice a Aleks sobre un mecanismo también se mide o se cita.
> 4. (menor, sesión) La guardia exigir_sin_crudo confunde una variable llamada «crudo» con la opción prohibida. Lección: una guardia de texto sobre código nombra la forma de la opción, no la palabra suelta.
>
> Next Action, en el commit del contrato (punto 3 de RITUAL):
> - CAMBIA A, con la propuesta de §4 del informe. Debe decir, además, que antes de la ejecución 2 Aleks copia y compila el script 1.1 (F7, 0 errors) y que el CSV de la ejecución 2 tiene que decir 1.1.
> - CAMBIA S: su condición de la primera ejecución de la demo está cumplida (DEMO-EJECUCION-1.md).
> - ENTRA, con una letra libre (compruébalo antes): «Para Aleks, con FTMO: la pregunta P-D1 (DEMO-EJECUCION-1.md §0.c): si la cuenta 2-Step Swing real es hedging como la prueba y si su volumen máximo en EURUSD es 50 o 100. La respuesta se registra parafraseada (RESPUESTAS-FTMO).»
> - ENTRA, con otra letra libre: «La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos.»
> Comprueba que PROJECT_STATE sigue por debajo de 25.000 bytes; si no, para antes del commit.
> En el commit de estado no se toca la Next Action.
>
> El resto, según RITUAL: merge, tag, commit de estado, make check sellado y push atómico de main y el tag. Si el clasificador te niega el push, dame el comando exacto para lanzarlo yo con «!»; no lo rodees. La CI de main tiene que estar en verde antes de borrar nada: consúltala con el sha de 40 caracteres escrito tal cual. Con la CI de main en completed/success, borra trabajo/demo-ejecucion-1 (git branch -d).
>
> Informe final: sha de main, tag, número de run y conclusión de la CI de main, ramas que quedan (local y origin) y tamaño de PROJECT_STATE.

### 7.1 El lector cambiado sobre el CSV real (punto 1)

Aleks lo ejecutó en su terminal el 2026-10-09 con `! PYTHONUTF8=1 uv run python
scripts/leer_demo_ftmo.py data/demo_ftmo` (desde esta sesión la guardia lo niega, §3.3). La salida,
tal cual:

```text
# Demo de FTMO: lo medido (1 fichero(s))

Solo lee: ningun valor pasa a los parametros ni cierra ninguna decision desde aqui.

- MedirDemoFTMO_20261009_153552.csv: completo (script 1.0)

## Decision a decision

| decision | que se mide | MedirDemoFTMO_20261009_153552.csv |
|---|---|---|
| ADR-0057 d1 | llenado de una buy stop: precio - nivel | 1.0 puntos (nivel 1.11999, llenado 1.12000) |
| FTMO-REGLAS R12 | lotes de la compra a mercado | 0.01 (la 1.0 usa el volumen minimo) |
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

**La comparación, con `diff --strip-trailing-cr`** entre la salida del lector de `main` (la del
§0.a) y esta: dos diferencias, y nada más.

```text
5c5
< - MedirDemoFTMO_20261009_153552.csv: completo
---
> - MedirDemoFTMO_20261009_153552.csv: completo (script 1.0)
11a12
> | FTMO-REGLAS R12 | lotes de la compra a mercado | 0.01 (la 1.0 usa el volumen minimo) |
```

Las dos son de lo que el punto 1 admite, «lo que diga la versión 1.0»: la versión junto al fichero,
y la fila de los lotes, que dice el volumen con que midió la 1.0 (la fila es nueva, pero su
contenido es exactamente eso; §3.3 la anunciaba). Las 28 celdas de valores de la tabla de
decisiones, la de A-28, los retcodes inesperados y los avisos son idénticas byte a byte. La etiqueta
OBSERVACION no aparece en la tabla: el lector no imprime el retcode de una observación (la fila 57
sale como «1.0 puntos …»), así que en la salida no cambia nada por ella. Sin el fin de línea: la
salida del §0.a se guardó en un fichero de Windows con CRLF y la de Aleks se copió con LF, por eso
el `diff` sin `--strip-trailing-cr` marca todas las líneas.

### 7.2 El test hermano de la regresión del 7 de agosto (punto 2)

`tests/regression/test_cuenta_7_de_agosto.py::test_con_el_perfil_real_la_primera_operacion_se_rechaza_por_volumen_maximo`:
con las reglas del bróker del perfil REAL (50), la primera operación del trader del 2026-08-07 (día
de construcción) tiene un lote mayor que el máximo, y `abrir_conocida` la rechaza con
`BrokerError` por `volumen_max_lotes`. Su docstring nombra ADR-0071 §2 y el pendiente 37 (A-18).
La conversión de una operación del trader en orden pasa a una función, `_orden`, que usan los dos
tests; la regresión original se queda con el tope de 100 declarado y sus aserciones intactas. Los
dos pasan en esta máquina (con `data/`); en la CI se saltan, como el original. 1425 funciones de
test.

### 7.3 ADR-0071 (punto 3)

ADR-0071 §2 añade, como consecuencia y sin decidir nada: `volumen_limite` = 0 (fila 12) dice que
no hay tope sumado entre órdenes, así que la rama del pendiente 37 elige entre recortar el lote a 50
(con riesgo menor que el del parámetro), partir la operación en varias órdenes o no operar; y cita
el caso real (la regresión del 7 de agosto).

### 7.4 La guardia (punto 4)

La guardia (`exigir_sin_crudo`, patrón `CRUDO_PYTHON`) da un falso positivo con la asignación a la
variable local del lector, que ya estaba en `main` (§3.3). **No se renombra la variable**: sería
rodear la guardia. Va a la Next Action con la orden de cierre, como entrada nueva: que la guardia
nombre la forma de la opción, con un test que rompa a propósito los dos sentidos.

## Estado

LISTA PARA REVISIÓN, NO CERRADA. Fase 0 y fase 1 hechas (§0-§3); revisor pasado (§5.1, §6); los
puntos 1 a 4 de la segunda respuesta del consultor, hechos (§7): la salida del lector cambiado
sobre el CSV real solo difiere en lo que dice la versión 1.0; el test hermano con el perfil real
(50) prueba el rechazo; ADR-0071 dice qué decide la rama del pendiente 37; la guardia va a la Next
Action. `make check` en verde antes de cada commit; sin cambios en `src/`. La orden de cierre (§7)
se ejecuta cuando Aleks escriba /cerrar-rama.
