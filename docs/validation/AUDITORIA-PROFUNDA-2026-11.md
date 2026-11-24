# AUDITORIA-PROFUNDA-2026-11 · La auditoría profunda del 22 y 23 de noviembre de 2026, copiada tal cual

Encargada por el consultor y hecha por Claude Code como orquestador, sin rama, del 2026-11-22 (desde
las 23:30) al 2026-11-23, sobre `main` en 8a10590b; entregada por Aleks el 2026-11-23 y copiada tal
cual (rama `trabajo/puente-techo`, fase A). Debajo de la raya, el texto sin tocar una línea: 271910
bytes, sha256 `542ee81011e9d82402d6c274bea3ffdfdaa886685fce24811ff146eaead01263` del fichero del
Escritorio de Aleks. Su material de trabajo (el plan, el registro, las entregas de los ejes y las
pasadas adversarias) se queda fuera del repo, en el Escritorio de Aleks.

---

# AUDITORIA-PROFUNDA-2026-11 · La premisa del Bot v3, con la salida C de ADR-0098

- **Fecha:** empezada el 2026-11-22 a las 23:30 y entregada el 2026-11-23.
- **Base:** main en 8a10590b (commit de estado del cierre de F39l); `stable/F39l-recorrida-construccion-3`
  = `main^1` = 88f678f7.
- **Quién:** Claude Code (Opus 5.5, esfuerzo alto) como orquestador, con 85 subagentes, todos de solo
  lectura y del tipo `auditor-encargo` (su Bash pasa por `solo_lectura.py`):
  - 14 de eje: P1, P3, P4, P6, M y K con opus; P2, P5, P7, S, R, X, D e I con sonnet;
  - 69 adversarios por hallazgo, con sonnet, en tres Workflow (22, 29 y 18), uno por hallazgo de gravedad C
    y por cada PLAN que sostiene una opción de §7;
  - 1 adversario general de la respuesta central (opus) y 1 revisor final (opus).
- **Lo que no se hizo:** no se abrió el holdout, ni data/, ni transcripciones, ni fotogramas, ni libros,
  ni knowledge/cases/ salvo `criterio_fidelidad.yaml`, ni knowledge/feedback/; no se ejecutó pytest, el
  arnés, el techo ni ningún guion que cargue velas, ticks, libros o el corpus; no se escribió nada en el
  repo. Las únicas ejecuciones fueron dos guiones de aritmética con entradas sintéticas en la carpeta de
  trabajo (§13).
- **Fechas:** solo de enero, abril, julio y agosto de 2026, de commits, de sesiones y de ADR (regla 2.3).
- **Dónde está el trabajo:** C:\Users\USER\Desktop\auditoria-profunda-trabajo\ (plan, registro, las 14
  entregas tal cual en entregas/, los resultados de las dos pasadas adversarias en JSON y los guiones).

**Lo esencial, en tres líneas.** No hay en el repo ninguna fuente de que el trader gane en real. La
comisión no es lo que separa lo que se creía (+0,47 / +0,56 R) del techo (−0,239 R): la caída está en el
R bruto, al aplicar su regla tal como la dicta a unas operaciones cuyo registro no la sigue del todo. El
ADR de C puede decidir hoy el método, no que la estrategia no gane.

## §0 · El plan (fijado a las 23:35 del 2026-11-22, antes de leer las fuentes de los ejes)

Base: main 8a10590b; tag stable/F39l-recorrida-construccion-3 = main^1 = 88f678f7. Antes de fijarlo
solo se leyeron PROJECT_STATE.md, `.claude/hooks/ficheros_con_ocultos.txt` y la cabecera de
`.claude/agents/auditor-encargo.md` (para saber qué tipo de subagente usar).

Pregunta central: de dónde sale la diferencia entre el techo (−0,239 R), lo que se creía (+0,47 R de
V2, +0,56 R de la anotada) y lo que el trader dice ganar; qué parte es modelo, costes, serie, muestra
y premisa; qué habría que medir, preguntar o decidir para saberlo.

Decisiones de 0.2: a) ADR de C · b) preguntas al trader · c) F17 + la cancha · d) rama del puente ·
e) página de los ingenieros · f) hoja de ruta.

| Eje | Preguntas | Cuenta como hallazgo | Lo refutaría | Fuentes de partida | Alimenta |
|---|---|---|---|---|---|
| P1 Puente V2→techo | Q1: piezas que cambian entre `viabilidad_comision.py` y `techo_parejas.py`; dirección de cada una; cómo medirla; diseño de la rama | Pieza presente en un guion y no en el otro, o implementada distinto, con fichero:línea en los dos | Que la pieza esté en los dos con la misma semántica (leyendo el código), o que un informe posterior la haya igualado | Los dos guiones, viabilidad_trader.py, repeticion_trader.py, VIABILIDAD-*, TICKS-LLENADO, BROKER-ORDENES-STOP, BE-AL-TICK, MARGEN-LOTE, CUENTA-POR-MES, SIMULADOR-CUENTA, README del anexo, ADR 0050-0052, 0057, 0061, 0065, 0081, 0090, 0092, 0098, knowledge/simulador, la cuenta, parametros.yaml | a, d |
| P2 Gestión de salida | Q2: qué dice la spec de BE, objetivo, cierres, parciales, mover stop; qué dijo el trader (extracciones); por qué sus salidas serían mejores que cualquier regla fija | Forma de gestionar descrita por el trader y ausente en la spec (o al revés), con extracción citada | Que la spec la recoja con estado y fuente, o que la extracción diga otra cosa | strategy_spec, parametros, ambiguedades, glossary, SESION-0x-EXTRACCION, ACTIVAR-SESION-0x, kb filtrada, BE-AL-TICK, ADR 0014, 0040, 0061, 0065, 0073, 0093, 0094, VIABILIDAD-COMISION | a, b |
| P3 Serie, entrada y sesgo del material | Q3: A-16 medido / no medido; hipótesis de las 7 no colocables y cómo medirlas; tipo de orden (A-47); S-14 y julio como referencia; relojes | Diferencia de precio, reloj o material que pueda mover entrada, stop o muestra, con fuente | Que A-16 esté medido de verdad, o que el guion descarte esa causa por construcción | ADR-0092 §9-§11, 0096, 0069, A-16, A-47, RECORRIDA-CONSTRUCCION-3 §1 y §4, RELOJ-INVIERNO, HUSO-POR-VELAS-CONTROL-ABRIL, INSTANTE-*, VIDEO-JULIO, ENTRADA-JULIO, ORDEN-STOP-O-LIMITE, F35-ORDEN-STOP-PIVOTE, criterio_fidelidad.yaml | a, c, d |
| P4 Costes | Q4: comisión, spread, deslizamiento; qué es impuesto y qué elegido; la cuenta de 0,13 R por punto; qué y cuánto mide F17 | Coste mal modelado o sin medir; cuenta del consultor que no cuadra | Que el coste esté medido en una fuente commiteada; que la cuenta cuadre con el código ejecutado | ADR 0026, 0051, 0071, 0090, 0092 §4; FTMO-REGLAS, DEMO-EJECUCION-*, NOCHE-TICKS-BROKER, llenado.yaml, criterio_fidelidad.py (`punto_de_equilibrio`, `_fills_afectados`, ejecutables con entradas sintéticas), CONTADOR/FRENO-PETICIONES | a, c |
| P5 Lo que el trader dice ganar | Q5: fuentes commiteadas de resultados reales, retiros, cuenta real frente a backtest; lista de preguntas sin cifras nuestras | Afirmación sobre resultados reales con fuente, o ausencia probada (búsquedas literales y sus recuentos) | Una fuente commiteada que la búsqueda no vio | RUMBO-2026-11, extracciones, HOJA-DE-RUTA, HISTORIA, SESION-DE-PREGUNTAS, PREGUNTAS de docs/sesion-* | a, b |
| P6 La cancha | Q6: tres vías (sombra en diferido, Python en vivo, techo sobre ticks de FTMO); qué existe y qué falta; guardias que lo impiden; reglas para corregir sin ajustar; tamaño; encaje con R7.3 y calendario | Pieza que exista o falte para una vía, con fuente; riesgo de ajuste al resultado | Que la pieza exista (o no) en el código, o que un ADR ya lo resuelva | mql5/, mql5bridge, engine, CAPA-GENERADA, EA-CONEXION, PLATAFORMA-ADELANTADA, DEMO-FTMO*, FTMO-Y-ARQUITECTURA, RENOVAR-CIERRES, CIERRES-DE-MERCADO, ADR 0067, 0068, 0071, 0082, 0090, 0092 §5, HOJA-DE-RUTA R6/R7/A.5 | a, c, e |
| P7 Muestra y ruido | Q7: intervalos publicados y por qué no se comparan; N que separaría +0,47 y −0,239 (aritmética sobre cifras publicadas); muestra de la cancha y de la rentabilidad | Conclusión que dependa de una muestra demasiado pequeña | Que los intervalos publicados ya separen las dos cifras con el método correcto | VIABILIDAD-COMISION, VIABILIDAD-TRADER, meta.txt, ADR-0092 §3 y §5, criterio_fidelidad.yaml | a, d |
| S Supuestos | Q8: inventario de supuestos del techo y del bot (ADR-0098 §1 primero, simulador, bróker, relojes, datos), elegido o impuesto, y qué pasa si es falso | Supuesto sin fuente, o elegido presentado como impuesto | Que tenga fuente o que no mueva nada | ADR 0098 §1, 0050-0053, 0057, 0081, 0063, 0069, 0005, 0024 | a, e |
| R Ruta con salida C | Q9: qué espera al ADR de C y qué no; fechas de AUDITORIA-2026-11-21 §1; tramos que cambian por opción | Tramo bloqueado o libre que el estado no dice; fecha que ya no se sostiene | Que la hoja de ruta ya lo diga con su dependencia | PROJECT_STATE, HOJA-DE-RUTA, MASTER_PLAN, RUMBO-2026-11, AUDITORIA-2026-11-21 | f, e |
| M Método de fidelidad | Q10: alcanzabilidad de 0,70/0,60 con la trayectoria; cascada de ADR-0092 §2 en la corrida (3); las 29 parejas; sentido del método de ADR-0093 con C | Trayectoria que hace inalcanzable el umbral en un plazo razonable; un punto de la cascada que se lleve la mayor parte | Una medida publicada que muestre convergencia | ADR 0043, 0070, 0092, 0093; CRITERIO-FIDELIDAD, CAMINO-DE-FIDELIDAD, INVENTARIO-FIDELIDAD*, RECORRIDA-CONSTRUCCION, -2, -3 | a, f |
| X Proceso | Q11: peso de guardias, make check y rituales frente a fidelidad desde RUMBO-2026-11; ramas por tipo; errores por rama; qué se podría simplificar sin perder la protección | Proporción de ramas de proceso desmedida; regla que cuesta y no protege | Que el recuento diga otra cosa | HISTORIA, ERRORES-RECURRENTES, RITUAL, CLAUDE.md, .claude/, Makefile, MEMORIA-SUITE | e, f |
| K Código | Q12: deuda no recogida por AUDITORIA-2026-11-21; guiones sin test; estados de MT5 que el simulador no tiene | Defecto o hueco con fichero:línea no listado en la auditoría anterior ni en Technical Debt | Que ya esté listado, o que el código lo cubra | engine, cases, domain, tests, scripts, mql5, CAPA-GENERADA, HISTORIA (cierre F39l) | e, d |
| D Material | Q13: qué hay, qué falta, qué está en riesgo, qué gastaría cada opción | Material en riesgo o falta que bloquea una opción, con fuente | Que el documento diga que está a salvo o recibido | CLAUDE.md, HOLDOUT-EXPOSICIONES (solo recuentos), MESES-VISTOS, REGISTRO-MARZO, ADR 0021, 0033, 0037, 0092 §5, 0096, HOJA-DE-RUTA A.4 y R5 | a, f |
| I Ingenieros | Q14: qué tienen que saber el primer día; índice de la página de entrada | Regla o decisión abierta imprescindible que ningún documento de entrada recoge | Que ya exista un documento de entrada que la recoja | §1 de este informe, AUDITORIA-2026-11-21 Anexo B, CLAUDE.md, ADR 0082, HOJA-DE-RUTA R6 | e |

**Añadido a las 01:16 del 2026-11-23 (FASE E, eje propio):**

| Eje | Preguntas | Cuenta como hallazgo | Lo refutaría | Fuentes | Alimenta |
|---|---|---|---|---|---|
| E1 Robustez de la salida C pieza a pieza | ¿Qué piezas, solas o juntas, podrían sacar al techo de «no gana» (esperanza ≥ 0, percentil 95 ≥ +0,10, d) < 3 %, e) ≥ 94 %, f)), y cuáles no, con cotas sobre cifras publicadas? ¿Puede el ADR de C decidir hoy, o qué tiene que esperar? | Una pieza cuya cota publicada alcance la distancia, o la prueba de que ninguna la alcanza sola | Una cota publicada que contradiga la clasificación | meta.txt; las entregas P1, P3, P4, P7, S, K; ADR-0098 §2 | a, d |

Reglas del flujo que me fijo:
- Subagentes: tipo `auditor-encargo` (Bash con `solo_lectura.py`) para todos los ejes; Explore solo si
  hiciera falta un barrido muy ancho. Modelo: ver el registro (§10).
- Cada entrega se guarda tal cual en `entregas/<eje>.md` antes de contrastarla.
- Gravedad C y PLAN: los compruebo yo con fichero:línea antes de mandarlos a la pasada adversaria.

## §1 · El mapa del repo (main 8a10590b)

Sale de `git ls-files <zona> | wc -l`, `wc -c` y la primera línea `# ` o el docstring de cada fichero
(datos crudos en `mapa-*.txt` de la carpeta de trabajo). No se listó nada de `knowledge/cases/`, de
`data/` ni del corpus. Los cuatro `*-SALIDA.txt` de `.claude/hooks/ficheros_con_ocultos.txt` se
cuentan pero no se abren.

## Recuento por zona

| Zona | Ficheros en git | Nota |
|---|---|---|
| docs/adr | 98 | 0000-plantilla a 0098; no existen 0087 ni 0095 |
| docs/validation | 919 | 190 `.md` y 23 `.txt` en la raíz; 52 carpetas en `anexos/` |
| docs/plan | 26 | HOJA-DE-RUTA (71.943 B), MASTER_PLAN (49.857 B), RUMBO-2026-11 (8.284 B), features F01-F15 |
| docs/runbooks | 15 | ERRORES-RECURRENTES (199.352 B), RITUAL (26.303 B), DEMO-FTMO (25.234 B) |
| docs/state | 2 (+README) | HISTORIA.md 2.717.867 B (solo se amplía), README |
| knowledge/spec | 6 | strategy_spec 163.376 B, ambiguedades 129.856 B, parametros 122.351 B, glossary 6.463 B |
| knowledge/cuentas | 3 | ftmo-2step-swing-100k.yaml 21.629 B, cierres/ftmo-2step-swing-100k.yaml, README |
| knowledge/simulador | 2 | llenado.yaml 1.255 B, README |
| src/botsito | 107 | 15 paquetes + cli.py (166.161 B) |
| scripts | 38 | 36 `.py` + git-hooks |
| tests | 240 | unit 158; integration/contract/regression/differential/golden 57 |
| mql5 | 13 | EA Botsito.mq5, 5 `.mqh` de la capa, script de pruebas |
| .claude | 15 | guardia.py 289.378 B, solo_lectura.py, estado_sesion.py, 8 skills, 2 agentes, settings.json |

## docs/adr (98) · los que tocan esta auditoría

| ADR | Título (primera línea) | Ejes |
|---|---|---|
| 0002 | Registro de parámetros: una sola puerta | S, K |
| 0005, 0024 | Velas: datos de mercado, proveedor y huso | P3, S |
| 0014 | (gestión: break even / objetivo; ver P2) | P2 |
| 0021, 0033, 0037, 0039 | Holdout: qué es abrir, la puerta, granularidad, libros | D, I |
| 0026 | FTMO 2-Step Swing como cuenta | P4, S |
| 0040 | Objetivo / A-56 | P2 |
| 0043, 0070 | Criterio de fidelidad y umbral 0,70/0,60 | M |
| 0050-0053, 0057 | Simulador: cuenta, llenado, bróker, cableado, cotizaciones | P1, S, K |
| 0061, 0065 | Break even (RN-014) y ASK/BID | P1, P2 |
| 0063, 0069 | Relojes: rejilla H4 y Europe/Madrid con cambio de hora | P3, S |
| 0067, 0068 | Freno de peticiones; cierres de mercado | P6, K |
| 0071 | Stops 0, volumen máximo 50 (A-27) | P1, P4 |
| 0072 | Papeles: Aleks, consultor, sesión | P5, I |
| 0073 | Sesión 4 (S-16, agosto en vídeo) | P2, D |
| 0080, 0094 | Sesgo H4 (color; rango que rompe) | M |
| 0081 | Margen y lote a 1:30 | P1, P4 |
| 0082 | Capa MT5 en el EA antes de F26 (recuadro del 2026-11-22) | P6, I |
| 0088 | Nombres de holdout se cuentan | X |
| 0090 | Comisión 2,50 USD por lote y lado (A-28) | P4 |
| 0092 | Método fidelidad/rentabilidad (§2 cascada, §3 N, §4 F17, §5 meses, §6, §8 cuenta por mes, §9-§11) | P1, P3, P4, P6, P7, M, D |
| 0093 | Método de sesiones en dos días; pivote §6 | M, R |
| 0096 | PREREGISTRO | D, P7 |
| 0097 | La stop cuyo 0 queda del lado malo espera (A-59) | P1, P3 |
| 0098 | La meta se mide en la corrida (3): techo, parejas, salidas A/B/C | todos |

## docs/validation · informes por eje (tamaño en bytes)

| Informe | Para qué (primera línea) | Ejes |
|---|---|---|
| AUDITORIA-2026-11-21.md (31.275) | Auditoría del consultor copiada tal cual; tabla de fechas §1, Anexo B | R, K, I |
| RECORRIDA-CONSTRUCCION-3.md (97.500) | La corrida (3), el pivote y la meta de ADR-0098 | P1, P3, M, R |
| anexos/RECORRIDA-CONSTRUCCION-3/ | meta.txt (2.990), techo_parejas.py (45.007), test_techo_parejas.py, README.md (9.938), cuenta-por-mes.txt, resumen-*.txt, pivote-*.txt, frenos_julio.py, simular_cierre.py | P1, P3, M |
| RECORRIDA-CONSTRUCCION.md, -2.md | Corridas (1) y (2) | M |
| VIABILIDAD-COMISION.md (11.253) | V2 y anotada con 5 USD de ida y vuelta | P1, P4, P7 |
| VIABILIDAD-TRADER.md | ¿Habrían pasado la fase 1 las operaciones del trader? | P1, P7 |
| REPETICION-TRADER-SALIDA.txt | Repetición descriptiva anterior | P1 |
| TICKS-LLENADO.md, BROKER-ORDENES-STOP.md, CABLEADO-SIMULADOR.md, SIMULADOR-CUENTA.md | Simulador | P1, S, K |
| BE-AL-TICK.md | Break even al tick | P1, P2 |
| MARGEN-LOTE.md, MARGEN-PENDIENTE.md | Lote, margen, volumen | P1, P4 |
| CUENTA-POR-MES.md | Cuenta una por mes (ADR-0092 §8) | P1, K |
| DEMO-EJECUCION-1.md, DEMO-EJECUCIONES-2-3.md, DEMO-FTMO-SCRIPT.md, NOCHE-TICKS-BROKER.md | La demo de FTMO | P4, P6 |
| FTMO-REGLAS.md, FTMO-P-D1.md, FUENTES-FTMO.md, RESPUESTAS-FTMO.md, FTMO-Y-ARQUITECTURA.md | Reglas y respuestas de FTMO | P4, P6, S |
| CONTADOR-PETICIONES.md, FRENO-PETICIONES.md | Peticiones al servidor | P4, P6 |
| ORDEN-STOP-O-LIMITE.md, F35-ORDEN-STOP-PIVOTE.md, SELECTOR-ORDEN-STOP.md | Tipo de orden (A-47) | P3 |
| RELOJ-INVIERNO.md, HUSO-POR-VELAS-CONTROL-ABRIL.txt, INSTANTE-LLENADO-SALIDA.txt, INSTANTE-TICKS-SALIDA.txt | Relojes e instantes | P3 |
| VIDEO-JULIO.md, ENTRADA-JULIO.md, ENTRADA-ENERO.md | Material de construcción | P3, D |
| METODO-FIDELIDAD-RENTABILIDAD.md, CRITERIO-FIDELIDAD.md, CAMINO-DE-FIDELIDAD.md, INVENTARIO-FIDELIDAD*.md | Método | M |
| SESION-01-2026-09-09.md, SESION-02-DECISIONES.md, SESION-0[2-8]-EXTRACCION.md, ACTIVAR-SESION-0[3-8]*.md | Lo que dijo el trader y cómo entró | P2, P5 |
| HOLDOUT-EXPOSICIONES.md, MESES-VISTOS.md, REGISTRO-MARZO.md, PREREGISTRO.md, PREREGISTRO-INVENTARIO.md | Material y holdout (solo recuentos) | D |
| CAPA-GENERADA.md, EA-CONEXION.md, PLATAFORMA-ADELANTADA.md | Capa MT5 | P6, K |
| CIERRES-DE-MERCADO.md, RENOVAR-CIERRES.md | Cierres | P6 |
| MEMORIA-SUITE.md, BLINDAJE.md, BLINDAR-MAKE-CHECK.md, GUARDIA-*.md, GUARDIAS-*.md | Proceso y guardias | X |
| NO SE LEEN | A18-TRANSCRIPCIONES-SALIDA.txt, A24-A21-A26-A34-SALIDA.txt, A35-PIVOTE-FORMADO-SALIDA.txt, SESION-02-BUSQUEDA-SALIDA.txt | — |

## docs/plan, docs/runbooks, docs/state

| Fichero | Para qué | Ejes |
|---|---|---|
| plan/HOJA-DE-RUTA.md | «de hoy a operar en vivo»: tramos R*, carril A.*, Marcador | R, P6, M, D |
| plan/MASTER_PLAN.md | Plan F01-F36 | R, P6 |
| plan/RUMBO-2026-11.md | Rumbo desde la re-corrida del 2026-11-08 | R, P5, X |
| plan/META-TECHO-PAREJAS.yaml, PIVOTES-SESION-7.yaml | Lo fijado antes de la meta y del pivote | P1, M |
| runbooks/ERRORES-RECURRENTES.md | Errores del revisor y del consultor | X |
| runbooks/RITUAL.md, CONTRATO-DE-RAMA.md, DECISIONES-DE-PROCESO.md | Proceso | X |
| runbooks/DEMO-FTMO.md, RENOVAR-CIERRES.md | Demo y cierres | P4, P6 |
| runbooks/SESION-DE-PREGUNTAS.md | Estilo de las preguntas al trader | P5 |
| runbooks/MIRAR-EL-MATERIAL.md, AMBIGUEDADES.md, ENTRADA-MARZO.md | Material y ambigüedades | D, P2 |
| state/HISTORIA.md | Archivos de PROJECT_STATE, registros de cierre | R, X |
| docs/sesion-{4,5,6,7}/PREGUNTAS*.md | Preguntas de sesiones (se leen); HOJA-USADA*.md NO | P5 |

## knowledge (lo que se lee)

| Fichero | Para qué | Ejes |
|---|---|---|
| spec/strategy_spec.yaml | Reglas RN-* | P2, S, M |
| spec/parametros.yaml | Registro de parámetros (estado, fuente) | P1, P2, S |
| spec/ambiguedades.yaml | A-* con estado | P2, P3 |
| spec/glossary.yaml | Vocabulario del trader | P5 |
| cuentas/ftmo-2step-swing-100k.yaml | Perfil de cuenta (comisión, volumen máximo, margen) | P1, P4 |
| cuentas/cierres/ftmo-2step-swing-100k.yaml | Calendario de cierres (caducado) | P6 |
| simulador/llenado.yaml | Spread supuesto por hora, parámetros de llenado | P1, P4 |
| corpus/libros.yaml | Solo declaraciones de libros | D |
| cases/criterio_fidelidad.yaml | Lo ÚNICO de cases/ que se lee | M, P3, P7 |

## src/botsito (107) · paquetes

| Paquete | Ficheros clave (bytes) | Para qué | Ejes |
|---|---|---|---|
| engine | broker.py 57.482, cableado.py 76.088, cuenta.py 28.615, llenado.py 18.632, arnes.py 30.205, motor.py, zonas.py 30.780, interprete.py, primitivas*.py, freno.py, calendario_cierres.py, simulador_config.py, perfil_cuenta.py, tope_trader.py, racha.py, decisiones.py, laminas*.py, visor.py | Motor, simulador, bróker, cuenta | P1, P6, K, S |
| cases | criterio_fidelidad.py 38.502 (`punto_de_equilibrio`, `_fills_afectados`), holdout.py 35.586, paquete.py 67.627, fidelidad.py, ingesta.py, relojes.py, visto.py, particiones.py | Fidelidad, holdout, kit | M, P4, D |
| domain | sesgo.py, pivotes_m15.py, estructura_m1.py, cierres.py, velas.py, ticks.py, valores.py | Núcleo puro | K |
| data | dukascopy.py, ticks.py, dataset.py, agregacion.py | Datos Dukascopy | P3, S |
| mql5bridge | compilar.py, generar_capa.py, journal.py | Puente a la capa MT5 | P6, K |
| spec, config, comun, corpus, evidence, feedback, retrieval, validation, viewer | modelo de spec, registro, cuarentena, evidencia | Conocimiento | X, K |
| cli.py | 166.161 B | Todos los comandos | K |

## scripts (36 .py) · los de esta auditoría (NINGUNO se ejecuta)

| Guion | Para qué | Ejes |
|---|---|---|
| viabilidad_comision.py (16.496) | V1/V2/anotada con comisión | P1, P4 |
| viabilidad_trader.py (28.314) | ¿Habría pasado la fase 1? | P1 |
| repeticion_trader.py (10.978) | Repetición descriptiva | P1 |
| ticks_spread.py, ticks_integridad.py | Spread y calidad de ticks | P4, P3 |
| orden_stop_o_limite.py, instante_llenado.py, instante_ticks.py, huso_por_velas.py | Orden e instantes | P3 |
| leer_demo_ftmo.py (25.010) | Lector de la demo | P4, P6 |
| contrato_rama.py, sello_make_check.py, instalar_hooks.py, pico_memoria.py, ficheros_con_ocultos.py | Plataforma de proceso | X |

## mql5 (13)

| Fichero | Para qué | Ejes |
|---|---|---|
| Experts/Botsito.mq5 (4.305) | EA de la capa; no decide operaciones | P6, K |
| Include/Botsito/Capa/{Cuenta,Generado,Journal,Reloj,Sesiones}.mqh | Capa generada desde el repo | P6, K |
| Scripts/BotsitoPruebasCapa.mq5 (12.122) | Pruebas de la capa en el terminal | P6, K |

## .claude (15)

| Fichero | Para qué | Ejes |
|---|---|---|
| hooks/guardia.py (289.378) | PreToolUse: material protegido y operaciones prohibidas | X, I |
| hooks/solo_lectura.py | Bash de solo lectura para los agentes | X |
| hooks/estado_sesion.py | Hook de arranque | X |
| skills/* (8) | abrir-rama, fase-cero, activar-sesion, comparar-con-main, entregar-rama, cerrar-rama, ingerir-sesion, retomar-rama | X |
| agents/auditor-encargo.md, revisor.md | Agentes de solo lectura | X |
| settings.json | Permisos | X |

## Raíz

Makefile (3.781), pyproject.toml (3.932), CLAUDE.md, PROJECT_STATE.md (24.680; tope 25.000).

## §2 · La respuesta central

**La pregunta.** De dónde sale la diferencia entre el techo (−0,239 R en 191 operaciones,
meta.txt:12-13), lo que se creía (+0,47 R de V2 en 67 y +0,56 R de la serie anotada en 77, con 5 USD
de ida y vuelta; VIABILIDAD-COMISION.md:112, :115) y lo que el trader dice ganar.

**Lo que se sabe.**

1. **Lo que el trader dice ganar no está en el repo.** No hay ninguna fuente commiteada de que retire
   dinero, de que tenga cuentas con importe ni de que gane en real con esta estrategia; solo que opera
   cuentas propias (SESION-01-2026-09-09.md:68-73) y que en la sesión 7 no dio cifras de su cuenta
   (SESION-07-EXTRACCION.md:80). Todo lo medido es su backtest manual en FX Replay. La premisa es hoy
   una pregunta de Aleks al trader, no un dato (P5-01, SOBREVIVE).

2. **No es la comisión lo que separa lo que se creía del techo.** V2, la anotada y el techo pagan la
   misma tarifa: 5 USD de ida y vuelta son los 2,50 por lado medidos en la demo (ADR-0090 §3). V2 y la
   anotada, que usa la misma unidad de riesgo que el techo (el stop del libro), pagan casi lo mismo por
   R en abril y agosto: 0,42 y 0,43 (VIABILIDAD-COMISION.md:112, :115). En el techo, la comisión cuesta
   entre 0,34 y 0,67 R por operación, así que **antes de comisión el techo queda entre +0,10 y +0,43 R**
   (aritmética sobre meta.txt:13 y :18 con la fórmula de `punto_de_equilibrio`, criterio_fidelidad.py:
   869-882; comprobada con entradas sintéticas; P4-01, SOBREVIVE). La anotada tenía +0,98 bruto y V2
   +0,88. **La caída grande está en el R bruto.**

3. **Ese bruto cae porque aplicamos su regla tal como la dicta, y su registro no la sigue del todo.**
   El objetivo a 3 veces la caja con el stop en el 0,8 (3,75 veces la distancia del stop), el break
   even y la entrada con orden stop son reglas que el trader dictó (el stop y el objetivo, ADR-0073 §1;
   el break even, RN-014 desde la sesión 1, al cierre y con cuerpo desde la 7a, ADR-0061 y
   strategy_spec.yaml:1798-1858; la orden stop, A-47 RESUELTA). Su
   propio material las contradice en parte: 26 de 38 ganadoras salen entre 3,00 y 3,75 veces el stop
   (ADR-0040:22-35, enmendado por ADR-0073 como «regla dicha por el trader, contradicha por el
   material», A-56 abierta), cinco dejan correr más allá de 4 R, dos cierran antes del objetivo y solo
   5 de 77 cierran a cero (VIABILIDAD-TRADER.md:179-184). El techo movió el break even en 79 de 191
   (meta.txt:11), y cada break even que salta paga la comisión entera (unos −5/D R; P4-09). **Lo que es
   nuestro, y no del trader**, es más estrecho: la geometría de la zona que dispara el break even, que
   ninguna fuente dibuja vela a vela (ADR-0061 §4); no corregir su serie de OANDA frente a Dukascopy
   (A-16, no medida a esta escala: METODO-FIDELIDAD-RENTABILIDAD.md:888-893); y colocar la orden en
   el cierre de la M1 anterior y llenarla al tick. Ninguna de estas piezas está aislada: ADR-0098 §3 C
   no pide descomponer el techo (P2-02, MATIZ).

4. **Lo que no puede sacar al techo de «no gana».** El deslizamiento: el equilibrio pide 2,52 puntos
   A FAVOR por llenado (meta.txt:18) y en una stop no se gana precio, ni en el modelo (ADR-0057 §1) ni
   en la demo (DEMO-EJECUCIONES-2-3.md:41) (P4-02, SOBREVIVE). El sesgo S-14: las sesiones que se
   saltaba eran de break even, que con nuestros costes pierden; por dirección, añadirlas lo hundiría
   más (P3-07, MATIZ: no medido). Las 7 no colocables: ni todas ganadoras al máximo llevan la media a 0.
   La mezcla de meses: julio, el único con vídeo, da −0,245 (meta.txt:23). Y la cuenta falla además d)
   y e): 4,88 % y 92,05 % (meta.txt:15-16). Las piezas que sí podrían moverlo, sin signo conocido, son
   el objetivo, la geometría del break even y la serie con el llenado de FX Replay (E1-01); a favor
   solo empuja con seguridad un spread de FTMO menor que el de Dukascopy, sin medir.

5. **La muestra.** La diferencia de 0,71 R entre V2 y el techo queda a unos dos errores típicos con
   supuestos generosos, y los intervalos no son del mismo tipo (95 % por operación frente a 90 % por
   días; P7-01, P7-02). Pero la mayor parte de la pregunta no es estadística: V2 y el techo miden
   objetos distintos sobre universos distintos.

**Lo que no se sabe.** (a) Si el trader gana de verdad y cómo opera en real: si sale donde su regla dice
o donde su registro muestra, si se salta sesiones, con qué riesgo, en qué firma, con qué costes.
(b) Cuánto aporta cada pieza al salto de bruto: nadie ha medido el techo con el objetivo a 3,00, sin el
break even o con otra entrada. (c) El spread y la ejecución de FTMO. (d) Si los precios de FX Replay son
bid, ask o medio y si sus resultados llevan costes.

**Qué lo diría.** Tres cosas, ninguna exige abrir holdout: (1) las preguntas de §6, sobre todo A1-A4, B1,
C1 y D1; (2) el puente pieza a pieza sobre construcción (§8.1); (3) F17 rediseñado para medir spread y
deslizamiento de órdenes stop (§8.2).

**En una línea: con su regla tal como la dicta, aplicada por nuestro simulador con nuestros costes,
sus operaciones no ganan; lo que ganaba era su registro de FX Replay, cuyas salidas no siguen del todo
esa regla. Lo que no sabemos es cuál de los dos es su estrategia en real.**

### El argumento adversario y mi respuesta

**El argumento** (adversario general, `auditor-encargo` opus, sin ver mi trabajo; entregas/, registro
01:52). Que el techo peca de optimista y que mi borrador atribuía a la sesión reglas que son del trader:
el objetivo a 3,75 lo repitió tres veces (ADR-0073:15-30) y ADR-0040 está enmendado (:9-18); el break
even es suyo salvo la geometría; la entrada por stop la confirmó él (A-47); la diferencia entre una
regla fija y la anotada son salidas que contradicen su propia regla (VIABILIDAD-TRADER.md:181-184); y
todo lo que el techo deja fuera empuja hacia abajo: el deslizamiento (con un punto en contra, unos
−0,37 R, aritmética sobre meta.txt:13 y :18), S-14, agosto sale de un libro que el trader no avala
(ADR-0073:51-56) y julio da lo mismo que el total. Propone: «con su regla tal como la dicta y nuestros
costes, sin deslizamiento, sus operaciones no ganan; lo que ganaba era su registro». Lo tumbaría: A-56
resuelta con una caja que muestre que su objetivo real es 3 veces el stop; el backtest de agosto en
vídeo contado en break even y salidas; el puente mostrando que el techo con objetivo a 3,00 o sin RN-014
llega a +0,10; un spread de FTMO 1-2 puntos menor; A-16 con sesgo a su favor; o sus resultados reales.

**Mi respuesta.** Acepto la corrección de redacción, que ya está arriba: «refutado» era falso desde
ADR-0073 y la mayoría de las piezas son suyas. No acepto que la cuestión quede cerrada hacia abajo:
la geometría del break even sí es nuestra (ADR-0061 §4) y mueve 79 de 191 operaciones; el objetivo
dictado y el objetivo practicado difieren en el 25 % de la distancia, y eso no tiene signo conocido
(más cerca sube el acierto y baja el pago); y la serie no está medida a la escala que importa. Por eso
la conclusión se queda en dos partes: lo que se sabe (con su regla, no gana) y lo que no (si su regla o
su registro es lo que hace en real). El adversario y yo coincidimos en lo que lo resolvería.

## §3 · Los ejes de la premisa

### P1 · El puente de V2 al techo

**Conclusiones.** En estructura el techo es V2 (stop en el 0,8, lote al 0,8, objetivo a 3 cajas), pero
lee el stop del libro como el 0,8 y no como el 1, así que en puntos su stop y su unidad de R son los de
V1 (el stop del libro) y su objetivo queda un 25 % más lejos que el de V2 (P1-01, REFUTADO por la pasada
tal como decía «usa los de V1» y reformulado así; registro 02:20). La comisión no separa los
dos: V2 y la anotada, que usa la unidad del techo, pagan 0,42 y 0,43 R en abril y agosto (P1-07,
REFUTADO tal como estaba redactado y reformulado así en la pasada adversaria; registro 01:32). Las
piezas que sí cambian, sin signo conocido salvo dos (el hueco de la entrada y meter las operaciones de
stop cortísimo, que bajan), son la geometría del objetivo, el break even, la entrada por stop, la
corrección de serie y el cierre forzoso. V2 no corre sobre el main de hoy (P1-04, SOBREVIVE), así que el
puente empieza por reproducirla en un clon. El diseño de la rama está en §8.1. El redondeo de la caja
derivada no es la inversa de la regla del bot (P1-03 y K-01, comprobado con aritmética pura: 24 de 33
valores de d entre 8 y 40 dan un stop implícito un punto mayor); no mueve C.

#### (1) La tabla del puente

| # | Pieza | V2 | Techo | Dirección esperada (sin cifra nueva) | Cómo se mide |
|---|---|---|---|---|---|
| 1 | Muestra | 77 operaciones de abril y agosto, con la condición `construccion == {04,08}` (`viabilidad_trader.py:235-237`, `:331-332`); N=67 tras quitar 10 (`VIABILIDAD-COMISION.md:93,112`) | Días dev de 2026-04, -07, -08 y -01 (`criterio_fidelidad.yaml:47`; `techo_parejas.py:412-417`); 198 operaciones, 191 llenadas (`meta.txt:9-12`) | Sin signo a priori. Julio da −0,245 en 64 operaciones y el total −0,239 en 191 (meta.txt:13 y :23): casi coinciden, así que la mezcla de meses apenas mueve la cifra (la media del resto se retiró del informe por la regla 2.3). Abril, agosto y enero son libros sin vídeo con el sesgo S-14 (`criterio_fidelidad.yaml:55-64`) | Al final de la cadena: +enero y después +julio, imprimiendo la esperanza acumulada y N |
| 2 | Corrección de serie | −2 puntos a la entrada, al stop y al objetivo (`viabilidad_trader.py:50`; `viabilidad_comision.py:162-163`). Sale de 9 leyendas de agosto, 36 valores (`BLOQUE-DE-LA-CAJA.md:197-206`) | Ninguna (`techo_parejas.py:29`, `:804-805`; ADR-0098 §1:43-44) | Va en sentidos opuestos en compras y en ventas: en una compra, V2 aleja el stop y acerca el objetivo respecto al mercado; en una venta, al revés. El signo neto depende de la mezcla. Hay una medida posterior (METODO-FIDELIDAD-RENTABILIDAD.md:872-888): las entradas existen en el tick de Dukascopy del lado del llenado con mediana 0 y p90 1, y el propio informe dice que eso no contesta A-16 | Un paso con el desfase a 0 que imprime solo el total, nunca por dirección |
| 3 | Geometría del stop | Stop en round(0,8·D), objetivo a 3·D, lote y R sobre 0,8·D (`viabilidad_comision.py:68-79`, `:165-167`, `:279-282`) | Stop del caso = S (el del libro); caja = ceil(S/0,8); objetivo = floor(3·caja); lote y R sobre S (`techo_parejas.py:543-555`, `:806`, `:107-117`; `cableado.py:1352`) | La relación 3,75 es la misma y todo crece un 25 % en pips. La comisión por R de una misma operación pasa a 0,8 veces y sube la esperanza. El acierto de stop y de objetivo cambia sin signo conocido. El stop, el lote y la unidad del R del techo son los de **V1** | Un paso. Una ruta paralela desde V1, cambiando solo el objetivo de 3D a ≈3,75D, tiene que llegar al mismo nodo |
| 3b | Redondeo de la caja | No aplica | ROUND_UP (`techo_parejas.py:107-111`; `test_techo_parejas.py:168`). No es la inversa de la regla del bot, ceil(0,8·caja) (`primitivas_broker.py:493`): si S no es múltiplo de 4, la caja sale un punto mayor y el objetivo 3 puntos más lejos | Pocas operaciones llegan al objetivo, pero ganan más: signo sin conocer, efecto pequeño | Subpaso: con floor, la inversa coherente, y después con ROUND_UP |
| 4 | Break even | No hay. El movimiento de v7-3 lleva el stop al 0,8, solo en V1 y en una operación (`viabilidad_trader.py:56-60`; `viabilidad_comision.py:189-196`) | RN-014 al cierre de la M1, con cuerpo (`techo_parejas.py:523-530`; `parametros.yaml:520-541,1072-1101`); A-13 sigue abierta por el margen; se movió en 79 (`meta.txt:11`) | Ambigua. Aritmética sobre cifras publicadas: una salida en break even da bruto ≈0 y neto −5/S, unos **−0,43 R** de media en la unidad del techo sobre las 77 (0,86/2, `VIABILIDAD-TRADER.md:82,103`), o −0,42 en la de V2 (`VIABILIDAD-COMISION.md:112`). Frente a un stop (−1) ahorra 0,57; frente a un objetivo (+3,75) pierde 4,18. Ayuda si menos de ~12 % (0,57/4,75) de las que vuelven a la entrada habrían llegado al objetivo. Simplificación: sin RN-002 | Un paso, que imprime también **cuántas salidas en break even** hay, cifra que no está publicada |
| 5 | Tope del lote | Si pasa de 100 lotes, BrokerError y fuera (`viabilidad_comision.py:178-185`, `:299-301`): 10 operaciones con d08 ≲ 5 puntos (aritmética: 500 USD / 100 lotes) | `limitar_lote` con el volumen a 50 y el margen a 1:30·0,95 (`techo_parejas.py:549-553`, `:600-624`; `broker.py:188-220`), y la operación entra | Meterlas baja la esperanza: cada una paga ≥0,8 R de comisión (aritmética: 5 USD / ≤6,25 puntos). El tope en sí y el margen no mueven la esperanza, porque el R no depende del lote (`cableado.py:1349-1352`; `criterio_fidelidad.py:582-585`). El 50 nunca muerde solo: el margen corta antes (`MARGEN-LOTE.md:804-806`) | Dos pasos: de excluir a limitar (cambia N), y de 100 a 50 más el margen (paso nulo, es un control) |
| 6 | Entrada | `abrir_conocida` al precio del caso y en su segundo, sin mirar la cotización (`broker.py:658-689`; `viabilidad_comision.py:157-181`) | Orden stop colocada al cierre de la M1 anterior al minuto del llenado (`techo_parejas.py:19-24`, `:537-559`, `:807`). Salta por el ask en la compra y por el bid en la venta, al precio del tick, con hueco (`llenado.py:229-245`). 7 no colocables, fuera | El hueco solo puede empeorar la entrada: baja. Las no colocables seleccionan sin signo conocido. El bot, desde ADR-0097 §1, espera; el techo las tira | Un paso, que imprime cuántas no colocables y cuántas con deslizamiento de entrada distinto de 0 |
| 7 | Spread | Ticks de Dukascopy. Entrada sin spread, salida por el bid en la larga y por el ask en la corta (`llenado.py:321`). La columna de spread es informativa y no se resta (`viabilidad_comision.py:104-109`; `VIABILIDAD-COMISION.md:98-101`) | Los mismos ticks. Entrada por el lado del llenado y salida igual que en V2. Respaldo M1 con el p90 por hora (`knowledge/simulador/llenado.yaml`) | Si los precios del trader van referidos al bid, V2 se ahorra un spread en las compras y el techo baja. Supuesto, sin fuente | Va dentro del paso 6. Se separa si se resuelve la referencia de precios de FX Replay |
| 8 | Cierres forzosos | Solo al final de la ventana del kit (`viabilidad_comision.py:197-200`; `simulacion.py:197-199`) | RN-002, `vence_vela_h4` (a 1 minuto) o `alcanza_hora` 15:00, más el fin de día (`techo_parejas.py:518-522`, `:571-575`, `:752-768`): 7 y 0 | Ambigua y pequeña. El cierre H4 nació después de V2 (ADR-0060, 2026-09-30; `parametros.yaml:399-416`) | Un paso, con recuentos |
| 9 | Cuenta | Arrastrada de abril a agosto (`viabilidad_comision.py:151-152`) | `CuentaViva`, una por mes (`techo_parejas.py:481-485`; ADR-0092 §8) | 0 sobre la esperanza. En V2 solo cambia qué operaciones pasan de 100 lotes; en el techo, d/e/f | Paso nulo, es un control |
| 10 | Motor y spec | Sin intérprete: el Broker de septiembre y un objetivo literal 3 (`viabilidad_comision.py:77-83`) | Reglas posteriores: ADR-0060, 0061, 0065, 0068, 0069, 0081, 0090, 0091, 0092 §8, 0097. Cambios del bróker desde `stable/F29-viabilidad-comision` (git log): respaldo M1 (ADR-0091, Z), margen, cierres, freno, break even al tick | Los cambios del bróker solo tocan los minutos sin ticks: 2 entradas en abril y 0 en agosto (METODO…:875,877). Pequeño | Paso 1: V2 sobre el bróker de hoy sin margen |
| 11 | Intervalos | Bootstrap por operación, 10.000, semilla 20260928, percentiles 2,5/97,5 = **95 %** (`viabilidad_trader.py:54-55,89-98`) | Por días, incluidos los días sin operaciones, 10.000, semilla 20261107, p5/p95 = banda del **90 %** (`criterio_fidelidad.yaml:74-76`; `criterio_fidelidad.py:611-646`; `techo_parejas.py:671-678`) | No mueve la esperanza. [−0,13; +1,08] y [−0,450; −0,026] no son la misma clase de intervalo | Imprimir los dos en cada paso |
| 12 | Comisión y swaps | 5 USD de ida y vuelta, la mitad en cada lado (`viabilidad_comision.py:146-148`); sin swaps | 2,50 por lado según el perfil (`ftmo…yaml:382-400`; ADR-0090) más swaps (≈0: ninguna cruza la noche, `ftmo…yaml:419-422`) | 0: la misma tarifa | Control: el coste en R del paso 3 tiene que dar exactamente 0,8 veces |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P1-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P1.md).

### P2 · La gestión de la salida

**Conclusiones.** La spec recoge la gestión que el trader dicta hoy (break even al cierre y con cuerpo,
objetivo 1:3 sobre la caja, cierre forzoso, sin parciales), con dos puntos débiles: la geometría de la
zona que dispara el break even es una lectura nocturna aceptada (P2-03) y el criterio del break even
cambió en cada sesión (P2-04). Su material muestra formas de salir que la regla no recoge: dejar correr
(P2-05, MENOR tras la pasada), cerrar antes y el objetivo practicado entre 3,00 y 3,75 veces el stop
(P2-06, que comparte veredicto con S-01). La salida C no pide descomponer el techo por pieza (P2-02,
MATIZ: la salida B tampoco descompone el techo, sino la diferencia emparejada). Las preguntas que faltan
están en §6, bloque C.

#### 1. Inventario de la gestión (regla | parámetro | estado | fuente | lo que dijo el trader | lo que falta)

| Regla | Parámetro (valor) | Estado | Fuente | Lo que dijo | Lo que falta |
|---|---|---|---|---|---|
| RN-014 break even (`strategy_spec.yaml:1798-1858`) | `break_even_condicion` = `cierre` (`parametros.yaml:1072-1104`) | CONFIRMED | `fb-2026-11-16-sesion-07-828031df` (sesión 7a, S-2; supersede al de la sesión 1) | «nosotros esperamos a que cierre la vela y si cierra por debajo no vamos a poder» (`ev-v18-001327-70f1d014`). Antes, «apenas toca» (sesiones 1, 3 y 4); en la 5 las dos; en la 6 se corrige a «cierre» | Instante en M1 al cierre. A-13 sigue ABIERTA (`ambiguedades.yaml:215-265`) solo por el margen |
| RN-014 | `break_even_criterio_ruptura` = `cuerpo` | CONFIRMED | `fb-2026-11-16-sesion-07-a094ab28` | «tiene que cerrar con cuerpo por encima de su máximo». Sin excepción de imbalance (`ev-v18-001145-901d8aa0`) | Sesión 8: «depende del contexto»; si el precio está «demasiado extendido» basta poco cuerpo «o inclusive con mecha» (`ev-v20-002630-6271f57e`, `ev-v20-002700-955a2dc8`). No activado (`SESION-08-EXTRACCION.md:380-407`) |
| RN-014 | Zona de control posterior: no es un parámetro, es geometría de código | SUPUESTO de una sesión nocturna, aceptado por el consultor | ADR-0061 §4 (`0061-…md:61`): «Ninguna fuente dibuja la zona posterior vela a vela» | S-2 de la 7a: «una vela que mitiga el alto y otra que cierra con cuerpo por encima de su máximo» (`SESION-07-EXTRACCION.md:401`) | Si la zona del BE se forma antes o después de romper el punto: sin respuesta citable (`SESION-08-EXTRACCION.md:366-367`; duda de la 7a en `:402`) |
| RN-014 | «El stop no se mueve después» (A-40) | RESUELTA, pero respondida a una pregunta que el trader entendió como «parciales» | `ambiguedades.yaml:1232-1237`; `SESION-03-EXTRACCION.md:470-475` | «no definimos parciales, o sea lo dejamos ahí quieto» (`ev-v9-005850-8aae8764`) | Nunca se le preguntó directamente si protege el stop más allá de la entrada. Hay evidencia lateral contraria (P2-09) |
| RN-015 objetivo (`:1860-1921`) | `objetivo_rr` = 3 | CONFIRMED | `fb-2026-09-09-sesion-01-7fbbb2e7` | «Siempre se fija el 1:3»; «el objetivo es fijo… Ahora no lo gestionamos» (`fb-2026-09-29-sesion-03-3f69a5f7`) | Ver `base_calculo_objetivo` |
| RN-015 | `base_calculo_objetivo` = `caja_completa` (`parametros.yaml:1759-1785`) | CONFIRMED | `fb-2026-09-29-sesion-03-f572f1a0`; ratificado en la sesión 4 (ADR-0073 §1) | «desde el punto 0 al punto 1», «respecto al 1 de la caja… exacto» (`ev-v10-012902-257afe4b`) | El material lo contradice (A-56, abierta). Ver P2-06 |
| RN-015 | `objetivo_extension_activa` = false; `objetivo_extension` UNKNOWN (`parametros.yaml:1122-1139`) | CONFIRMED / UNKNOWN | `fb-2026-09-09-sesion-01-9c259e06` | «no vamos a dejar correr nada por ahora»; «lo de dejar correr lo dijo en los primeros vídeos; lo han dejado» (`ev-v10-012704-d3facd31`) | «Por ahora» y «primeros vídeos» no tienen fecha. Ver P2-05 |
| RN-015 | `parciales` = no (`parametros.yaml:1263-1273`) | CONFIRMED | `fb-2026-09-09-sesion-01-0905fd59` | «no hemos no definimos parciales» (sesión 3). Antes: parciales 30-40 % «discrecional» (`ev-v2-002419-4629d258`); «sacar parciales a un 50 %… pero por ahora vamos a dejarlo en 1:3, creo» (v6, 1:51:28) | Nada nuevo desde la sesión 3 |
| RN-002 cierre forzoso (`:931-987`) | `cierre_h4_antelacion` (1 min), `ventana_fin` = 15:00, `cierre_forzoso_fin_ventana` = sí (`parametros.yaml:372-411`) | CONFIRMED | `fb-2026-09-29-sesion-03-c38c4aef`; ADR-0060, ADR-0069 | «siempre menos un minuto, antes de que cierre»; «lo cierro enseguida, nunca se deja» (`ev-v16-002323-515b9da4`) | Nada que reclame el repo |
| RN-010 equal («activación sin ruptura») (`:1615-1642`) | `salida_sin_ruptura` = `proteger_y_dejar` | CONFIRMED | `fb-2026-09-09-sesion-01-9626d3dd` | «proteger a 0.80 […] o continúa ya nos saca con menos 0.80» | La acción `gestionar_salida` no aparece en `src/` ni en `tests/` (P2-10) |
| RN-024 baja de protección por % de vela | `stop_reduccion_*` UNKNOWN a propósito | DESCARTADA | `fb-2026-09-09-sesion-01-728b68da` | «Descartar esto, se mantiene el SL fijo de 0.8» | Nada |
| Mover el stop a 1:1 o a 0,50 | — | no existe en la spec | `ev-v4-000353-9ea3ce94` (idea abierta), `ev-v3-002026-fa5295fa` («no suelo trabajar con el 1-1») | Lo descarta: espera la zona de control | Nada |

Salida manual: el trader dice que no cierra a mano; se gana, se pierde o hay BE, y solo cierra al vencer la sesión (G-1, `SESION-03-EXTRACCION.md:478-490`, `ev-v9-005916-d6a15b43`). Los cierres `manual` del motor son de las guardias de la firma (RN-029 a RN-032, RN-030), no del trader. En el techo están apagados (ADR-0098 §1).

#### 3. Indicios commiteados de gestión manual (y que NO lo son)
- Cierre a mano antes del objetivo: dos operaciones (VIABILIDAD-TRADER:184) a 2,5-2,9 R; con las 4 de A-33, cierres en ganancia por debajo de 3R. El trader dijo «nunca» (S-12). A-56 lo dejó como medición.
- Más allá del objetivo: las siete de P2-05.
- BE a cero: 5 (P2-07).
- No es gestión manual: el cierre de la última vela H4 (RN-002, ADR-0060) y el cierre a mercado de RN-030.

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P2-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P2.md).

### P3 · La serie, la entrada y el sesgo del material

**Conclusiones.** A-16 no está medida a la escala que importa para el R: lo medido dice que la entrada
del trader existió dentro de la M1 de Dukascopy, no que las dos series marquen el mismo precio (P3-01,
MATIZ; P3-15). La escala de A-16 (1-2 puntos) es la misma que la distancia que separa el techo de 0
(P3-02). Las 7 no colocables no pueden cambiar C (P3-06) y tienen cinco hipótesis medibles sin R (§9).
S-14, por dirección razonada, sesga el techo hacia arriba (P3-07, MATIZ: no medido). Julio no es una
referencia limpia (P3-09, SOBREVIVE). No queda ningún desfase de horas; solo uno de segundos, candidato
a explicar las 7 (P3-14). El modelo de llenado de FX Replay no está medido, y VIABILIDAD-COMISION
afirma algo que METODO, posterior, deja abierto (P3-13).

#### Las 7 no colocables: hipótesis
Con lo publicado (ORDEN-STOP-O-LIMITE.md:115-117), 60 s antes del llenado hay 8 de 75 operaciones a ≤2 puntos del nivel, y el precio ronda el nivel una mediana de 261 s antes. H1 desfase de serie (predice sobre todo ventas, a ≤2-3 puntos); H2 instante (Dukascopy ya había cruzado en la M1 anterior); H3 colocación u orden (el trader coloca minutos antes; mueve órdenes; una límite cruzada es indistinguible de una stop); H4 sin ticks (M1 k−1); H5 huso (poco probable con 92,4 % dentro del rango M1).

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P3-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P3.md).

### P4 · Los costes

**Conclusiones.** La comisión es impuesta y medida (2,50 por lote y lado, dos veces con 1,00 lote en la
demo, ADR-0090 §3) y con stops de pips pesa entre 0,34 y 0,67 R por operación del techo (P4-01,
SOBREVIVE; aritmética comprobada con entradas sintéticas). La cuenta del consultor cuadra: 0,1345 R por
punto y llenado afectado, y −2,52 significa deslizamiento a favor (P4-02, SOBREVIVE; sintetico_equilibrio.py).
El spread de FTMO está sin medir y la relectura de ADR-0092 §4 no tiene vía para meterlo (P4-03, MATIZ:
ADR-0098 C ya pide F17 con spread). F17, tal como lo define MASTER_PLAN, es un grabador pasivo que no
mide el deslizamiento de una stop (P4-05, MATIZ); el encargo de F17 tiene que fijar la referencia del
deslizamiento (P4-04) y prever varias pruebas o un guion que coloque órdenes (P4-06). Que la prueba
gratuita ejecute como la cuenta real no está escrito (P4-08, MATIZ: solo se duda del margen).

#### Desglose del coste (EURUSD: 1 punto = 0,00001 = una décima de pip = 1 USD por lote; ADR-0090 §6, contrato 100000)

| Coste | Cómo entra en la simulación | Fuente | En R por operación del techo (aritmética sobre cifras publicadas) | Clase |
|---|---|---|---|---|
| Comisión | 2,50 × lotes al abrir y otra vez al cerrar. En R vale 5/D (D = distancia al stop en puntos) y no depende del lote | ADR-0090 §3 (:102-110); ftmo-2step-swing-100k.yaml:382-400; cableado.py:1349-1352 y :1366-1369 | Entre **0,336 y 0,673 R** (ver la cuenta abajo). Una medida previa, V2, abril+agosto, motor de septiembre: 0,42 R (VIABILIDAD-COMISION.md:112) | IMPUESTO POR EL MUNDO (FTMO, medido), una vez elegida FTMO (ADR-0026, elegido) |
| Spread | Va dentro de los precios: el de cada tick de Dukascopy (ADR-0051 §6). Sin ticks, el p90 por hora (llenado.yaml:13-28). Ninguna operación cayó en horas sin ticks (RECORRIDA-CONSTRUCCION-3.md:587) | TICKS-SPREAD-SALIDA.txt:5-32: media 2,70-3,49, p50 3, p90 4-5 | Del orden de 3·x, con x = media de 1/D entre 0,067 y 0,1345, es decir **0,20-0,40 R**. VIABILIDAD-COMISION.md:112 da 0,24 R (V2) | En vivo lo impone el bróker. En la simulación es ELEGIDO (Dukascopy). El de FTMO está sin medir |
| Deslizamiento | 0 fijo (llenado.yaml:9). Solo el de hueco de los ticks: la stop se llena al tick que la dispara, nunca mejor que el nivel (ADR-0057 §1; llenado.py:219-261, 320-328) | ADR-0051 §4 (DN-3 PROVISIONAL); ADR-0090 §7: siete muestras | **−0,1345 R por cada punto en contra en cada llenado afectado** | IMPUESTO (la ejecución de FTMO), sin medir. El modelo 0 es ELEGIDO |
| Swap | Lo carga el bróker simulado, pero ninguna posición pasa la noche (RN-002) | ADR-0090 §6 (:209-229); perfil :415-440 | 0 | Existe y lo impone FTMO. Lo anula una regla de la estrategia |
| Otros: tope de 50 lotes y margen 1:30 | Recortan el lote (`limitar_lote`, broker.py:188-220) | ADR-0071; FTMO-REGLAS.md:56 (R9: Swing 1:30, Standard 1:100) | No cambian el R. Bajan los USD de cada operación y retrasan el +10 % | 50 lotes: IMPUESTO (medido). 1:30: lo impone el tipo Swing, que fue ELEGIDO (ADR-0026) |

**Lo que falta para la comisión, la cuenta.** Todas las entradas del techo son órdenes stop (techo_parejas.py:20 y :539; `entrada_por_stop = o.tipo == TIPO_STOP`, cableado.py:1367). Por tanto f_i, los llenados afectados de cada operación, vale 1 o 2 (criterio_fidelidad.py:824-832). La pendiente de `punto_de_equilibrio` es la media de f_i·lotes·1/riesgo, y como riesgo = lotes·D_i (cableado.py:1352), queda en la media de f_i/D_i (criterio_fidelidad.py:876-879). Sale de meta.txt: (−0,239 − 0,10)/(−2,52) = 0,1345; con el redondeo de las dos cifras, entre 0,134 y 0,135. La comisión en R es 5·media(1/D), y la media de 1/D cae entre pendiente/2 y pendiente. Así que la comisión está entre 0,336 y 0,673 R por operación, y **el techo antes de comisión (con el spread de Dukascopy) estaría entre +0,097 y +0,434 R**. Todo es aritmética sobre las cifras publicadas de meta.txt:13 y :18 y se apoya solo en las fórmulas citadas. El coste total, comisión + spread, ronda 8 puntos por ida y vuelta, unos 8·x R: entre 0,54 y 1,08 R.

#### Qué tiene que medir F17
Para que la relectura diga algo, F17 tiene que medir tres cosas:
1. El deslizamiento de las stops de entrada, de los cierres por stop y de los cierres a mercado, por separado. Cada evento con el nivel, el tick que lo dispara (bid y ask, ms), el precio y el instante del llenado, y los lotes, con lotes del bot (unos 20-50) y en la franja del trader. Mediana y p90 (ADR-0092 §4; criterio_fidelidad.yaml:82-83). Serían 100-400 por clase, así que hace falta un guion que coloque órdenes, no un grabador pasivo.
2. El spread de FTMO por hora, para compararlo con TICKS-SPREAD-SALIDA.txt. Necesita una regla, que hoy no existe (P4-03).
3. Que la prueba gratuita valga por la cuenta real (P4-08).

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P4-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P4.md).

### P5 · Lo que el trader dice ganar

**Conclusiones.** No hay ninguna fuente commiteada de que el trader retire dinero ni gane en real con
esta estrategia (P5-01, SOBREVIVE). Hay tres clases de material: backtest con vídeo (julio, provisional,
y un día de abril), backtest sin vídeo (enero, abril, agosto) y cuenta real (nada) (P5-04, MATIZ). El
riesgo del trader en fondeo está escrito como 0,4-0,5 % (parametros.yaml:1279); no hay discrepancia viva
con el 0,5 % del bot (registro 00:02). Lo que ya se le preguntó sobre su real se limita al lote y a los
break even; la lista de preguntas que faltan está en §6.

#### Lo que se le preguntó ya (para no repetir)
- **Lote que no cabe, «¿te ha pasado en tu cuenta real?»:** `docs/sesion-5/PREGUNTAS.md:226`; contestada en `SESION-05-EXTRACCION.md:467`.
- **Cuartillas y rachas «¿en tus backtests o en tu cuenta?»:** `docs/sesion-5/PREGUNTAS.md:723`.
- **Por qué no entró (saltarse sesiones) en backtest:** `docs/sesion-6/PREGUNTAS.md:256-271` (S-7). Dijo «solo me he saltado a lo mejor para cuando en una sesión había break events» y «si un día no se opera es porque estaba enfermo». Es sobre backtest.
- **Stop y salida (cuándo pasa al 0,8):** A-18, RESUELTA el 2026-10-04 (`knowledge/spec/ambiguedades.yaml:371-383`; el stop va en el 0,8 al poner la orden). Pero la pregunta «¿cuándo pasa al 0,8?» quedó sin contestar en la sesión 3 (`docs/sesion-4/PREGUNTAS.md:99`). Esto es sobre backtest, no sobre su real.
- **Tipo de orden:** `docs/sesion-7/PREGUNTAS-7B.md:310` y `docs/sesion-5/PREGUNTAS.md:601` («entro a mercado»). Es sobre lo que hace el bot en el dibujo, no sobre su real.
- **Spread y comisión:** no aparece ninguna pregunta al trader. En SESION-0N solo hay menciones del consultor y `docs/sesion-5/PREGUNTAS.md:62` prohíbe poner cifras de VIABILIDAD-COMISION.
- **Retiros, tamaño de cuenta, cuántas cuentas, firma, resultados reales:** nunca se preguntó.

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P5-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P5.md).

### P6 · La cancha

**Conclusiones.** Hoy no se puede hacer ninguna de las tres vías de la cancha: el grabador de F17 no
existe (P6-01), el motor solo acepta datos de Dukascopy (P6-02), el día de mercado solo se construye
desde un caso dev (P6-03) y el calendario de cierres caducó (P6-11). R7.3 está bloqueada por su propia
condición de entrada mientras rija C, por el mínimo 2 del pivote (P6-06, MATIZ). La vía de Python en
vivo la cierran ADR-0082 §4 y R6.1; la prueba gratuita se lee como DEMO (P6-08, MATIZ). R6.0 y RUMBO
siguen citando una razón que el recuadro de ADR-0082 retiró (P6-07, MATIZ). El diseño está en §8.2.

#### Las tres vías

| Vía | Qué existe | Qué falta | Ramas | ADR | Riesgo | Guardias que lo impiden hoy | Lo que da |
|---|---|---|---|---|---|---|---|
| (i) Sombra en diferido sobre ticks de FTMO grabados | El EA que solo lee (R6a.1-2), `compilar.py`, el journal con cadena de hashes, el formato CSV de ticks, `MercadoDia` y `MotorCableado`. | (1) el grabador en MQL5; (2) un proveedor nuevo en los manifiestos de ticks y de M1, con la hora del servidor pasada a UTC por A-28; (3) un constructor del día de cancha sin `cases/`; (4) que el motor no mezcle proveedores; (5) un prefijo propio para el M1; (6) los cierres; (7) láminas para días de cancha; (8) R6a.8. | (a) F17, el grabador. (b) Datos: proveedor y prefijo. (c) El motor sobre días de cancha. (d) Cierres semanales o desde el journal. (e) Las láminas. | El de C, que cambie R7.3. Uno de la vía (R7.3 ya lo pide, HOJA:680). Uno del proveedor de datos (MASTER_PLAN:292). | Ajustar al resultado si se corrige mirando el R. Mezclar series. Perder ticks si la máquina duerme. Que la prueba gratuita no sea la cuenta de pago. | ticks.py:483 (`dukascopy`); cli.py:2884 (`construccion`); arnes.py:157 (dev-visto); cli.py:2742 (`motor laminas`); RENOVAR-CIERRES:4; heredado 9. | Las decisiones del bot con precios de FTMO, día a día. El spread por hora de FTMO. La pata «backtest» de F34. |
| (ii) Python decide en vivo en la prueba gratuita | La respuesta de FTMO (lecturas libres, Python permitido) y el freno de Python. | El puente, la dependencia MetaTrader5, la reconexión y la orden viva si el proceso cae (RUMBO §4:39), las órdenes idempotentes (R6a.3). | Un puente, nuevo. R6a.3. | Reabrir ADR-0082 §4 (D4); enmendar ADR-0082 D2 y ADR-0092 §3/§7, o definir «en vivo». | Construir lo que habría que tirar en F29. Decidir en vivo antes de la puerta de rentabilidad. El riesgo de ajuste. | ADR-0082 D4 y D2; ADR-0092 §3/§7; R6.1; `test_capa_mt5` (la capa no envía órdenes). | El deslizamiento real de las órdenes del bot y los rechazos reales. Las decisiones son las mismas que en (i). |
| (iii) El techo releído sobre ticks de FTMO con las operaciones reales del trader | El modelo del techo de ADR-0098 §1 (`techo_parejas.py`) y `con_operaciones_del_trader` (simulacion.py:217). | Todo lo de (i), la exportación del trader, su entrada en `libros.yaml`, la ingesta de un formato nuevo, y leer su resultado real. | Lo de (i), más la ingesta y la repetición sobre FTMO. | Uno que lea el resultado real y la categoría del mes nuevo. | Que el trader opere en otro bróker u otro servidor. Los resúmenes de su cuenta son agregados. | Las de (i), más la guardia (carpeta del mes como sin abrir, guardia.py:713-716) y el texto del mes 12 oculto. | El techo sin desfase de serie, A-16 medido y el error del simulador frente a sus llenados reales. |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P6-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P6.md).

### P7 · La muestra y el ruido

**Conclusiones.** Los dos intervalos no son comparables (95 % por operación frente a 90 % por días,
P7-01). Con supuestos generosos, la diferencia de 0,71 R queda a unos dos errores típicos (P7-02,
aritmética). La mayor parte de la pregunta no es estadística (P7-03). En la puerta de rentabilidad ata
el percentil 5, no la esperanza mínima: con N = 100 haría falta una media observada del orden de +0,29
R (P7-06, MATIZ, aritmética). La rentabilidad de 2025 tendría N suficiente solo si el bot llenara al
ritmo de construcción (P7-07).

#### 1. Cómo se calcula cada intervalo (hecho, con código)

| | V2 / anotada (VIABILIDAD-COMISION) | Techo y parejas (meta.txt, ADR-0098) |
|---|---|---|
| Función | `viabilidad_trader.bootstrap`, `viabilidad_trader.py:89-98`; la llama `estadisticas` (:118-132) desde `viabilidad_comision.py:251` | `remuestreo_por_dias`, `criterio_fidelidad.py:611-646` |
| Unidad que se sortea | la OPERACIÓN, con reemplazo, `k = len(rs)` | el DÍA de mercado, con reemplazo, tantos como días corridos (76, con o sin operaciones); la cifra de cada réplica es la media AGRUPADA de todas las operaciones de los días sorteados |
| Réplicas y semilla | 10.000; `SEMILLA = 20260928` (:54-55) | 10.000; 20261107 (`criterio_fidelidad.yaml:75-76`) |
| Cobertura | percentiles 2,5 y 97,5 → intervalo del 95 % bilateral (`medias[int(0.025*n)]`, `medias[int(0.975*n)-1]`) | percentiles 5 y 95 → intervalo del 90 % bilateral (`meta.txt` línea c; índice `(5*(n-1))//100`) |
| R que se promedia | R nominal (movido ÷ distancia del lote) menos comisión en R (`viabilidad_comision.py:279-284`) | PnL neto ÷ riesgo en USD de la cuenta (`r_neto`), con comisión, swaps y bróker simulado |
| Muestra | 67 (V2) o 77 (anotada), abril+agosto | 191, enero+abril+julio+agosto |

ADR-0098 §5 lo admite: «con intervalos por operación y no por días» (`docs/adr/0098-...md`, líneas 204-206).

#### 4. Qué parte de la pregunta es estadística y qué parte no

- Estadística (se puede responder con lo publicado, con las salvedades de P7-01 y P7-10): la diferencia de 0,709 R tiene un z ≈ 2,1 si todo fuera independiente y normal. El intervalo de V2 llega a −0,13, así que V2 por sí solo es compatible con 0 R y con −0,24. Separar de verdad V2 del techo pide del orden de 76 a 171 operaciones por brazo si la diferencia es la publicada, y 300 a 700 si fuera la mitad.
- No estadística (no se arregla con N): lo que midió cada uno. V2 = serie corregida por desfase de 2 puntos, tope de 100 lotes, R nominal, stop 0,8, abril y agosto. Techo = serie sin desfase, perfil de 50 lotes, PnL ÷ riesgo, cuatro meses, una cuenta por mes. Mientras no se mida el techo (o V2) sobre la misma muestra con la misma definición, la diferencia no se puede imputar ni al ruido ni a la medida.

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids P7-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/P7.md).

## §4 · Los ejes S, R, M, X, K, D e I

### S · Los supuestos

**Conclusiones.** De los 29 supuestos, los que deciden el signo del techo son de coste y de geometría:
el spread de Dukascopy usado como el del mundo (S-02, elegido presentado como impuesto), la comisión
medida en prueba gratuita (S-03, MATIZ) y el objetivo dictado frente al material (S-01, MATIZ: el techo
sigue la spec vigente por ADR-0073, y ADR-0098 no nombra A-56). La gestión del techo es la del bot
(S-05). Todo lo «impuesto por el mundo» sobre FTMO viene de una prueba gratuita (S-11). Que el trader
llenara al nivel sin spread ni comisión en FX Replay no tiene fuente (fila 28): es la premisa.

#### 1. Tabla de supuestos (rutas de ADR: `docs/adr/00NN-*.md`)

| # | Supuesto | Dónde vive | Clase | Fuente o pregunta pendiente (dueño) | Si fuera falso: dirección en el techo, razonada |
|---|---|---|---|---|---|
| 1 | Entrada por orden stop en la entrada del caso, colocada al cierre de la M1 anterior al llenado del trader | 0098:34-37; `techo_parejas.py:19-24` | IMPUESTO (el trader entra «siempre por stop»), con detalle ELEGIDO | A-47 RESUELTA, `fb-2026-09-29-sesion-03-92a38105` (`parametros.yaml:1032-1054`). Colocar justo un minuto antes es elección del guion | Por construcción no hay «no llenadas». Si el trader colocó antes, precio e instante serían otros. Indeterminada |
| 2 | El instante del xlsx está en Europe/Madrid con cambio de hora, exacto al minuto | 0069:68-87; `huso_grafico` | IMPUESTO, medido | 3 fotogramas de enero + 2 capturas de 2024 + frase del trader; A-16 halla la entrada dentro de la M1 BID en 183 de 198 (`ambiguedades.yaml:321-325`) | Un huso errado desplazaría una hora los llenados de invierno, y A-16 lo habría delatado. Riesgo bajo |
| 3 | El stop del caso es su 0,8 y el 1 se deriva | 0098:39-41; `techo_parejas.py:25-28` | IMPUESTO por el trader (A-18/ADR-0073), **contradicho por su material** | A-56 ABIERTA, para F26 (`ambiguedades.yaml:1927-1962`); 0040:22-55 | Ver S-01 |
| 4 | Objetivo = `objetivo_rr` 3 × la caja completa (3,75 sobre entrada-stop) | `parametros.yaml:1105-1121`, `:1759-1784` | IMPUESTO por el trader, **contradicho por el material** | 0040:22-35: 26 de 38 ganadoras en [3,00; 3,75); 0040:51-55 | Ver S-01 |
| 5 | Sin desfase de serie con Dukascopy | 0098:43-44 | ELEGIDO (ADR-0002/0024), declarado en 0098:173-177 | A-16 ABIERTA. OANDA +2 puntos por encima en mediana (0092:260-263). Vela de otro color: `ev-v19-012924-64367863` | 2 puntos son un 13-17 % del stop (aritmética). Signo neto indeterminado |
| 6 | Gestión: break even RN-014 por «zona posterior» de M1, al cierre y con cuerpo; objetivo, RN-002 y fin de día | 0098:46-50; `estructura_m1.py:263-275`; `parametros.yaml:520-541`, `:1072-1093` | ELEGIDO (la gestión es la del bot); «cierre» y «cuerpo» los dijo el trader en la 7a | A-13 ABIERTA por el margen (`parametros.yaml:1085-1086`). 79 de 191 movidos | No se puede sacar el signo razonando. Ver S-05 |
| 7 | Lote con `lote_si_no_cabe = limitar` | 0098:51-52; 0081:20-67 | ELEGIDO por el consultor, confirmado por el trader con reservas | 0081:42-51 | Casi no mueve la esperanza; mueve d) y e) a favor del techo |
| 8 | Margen 1:30 y volumen máximo 50 | `cuentas…yaml:270-302`; 0081; 0071:56-59 | IMPUESTO, medido en la **prueba gratuita** | R9, `FTMO-REGLAS.md:56`; P-D1 sin respuesta (`HOJA-DE-RUTA.md:725`) | Casi no mueve b) |
| 9 | Reserva de margen por pendiente stop viva | 0081:115-153; 0052:69-77 | ELEGIDO (conservador), **desmentido en la prueba** | 0090:130-165; PS:84 | Sin efecto medido: cero rechazos |
| 10 | Llenado de stop al precio del tick que lo dispara; stops al toque | 0057:19-29; 0051:34-39; `llenado.py:322` | ELEGIDO | Demo, filas 56-58 (0090:180-182) | Si FTMO llenara mejor, el techo subiría un poco. Poco probable |
| 11 | Objetivo y límites exigen pasar ESTRICTAMENTE el nivel | `llenado.yaml:6`; `llenado.py:331`, `:358`; 0051:34-39 | ELEGIDO (conservador), **no medido** | 0051:36-37: un tester de MT5 llena al toque | Si el TP se llenara al toque, el techo subiría. Ver S-07 |
| 12 | Nivel exacto no es lado equivocado; «lado equivocado» se rechaza con `precio_invalido` | 0057:37-60 | ELEGIDO, PROVISIONAL | 0090:167-182: tres patrones en tres ejecuciones | Mueve las 7 no colocables. Signo desconocido |
| 13 | Ticks de Dukascopy con su spread como el spread del mundo | 0098:53; 0005:21-24; 0024:17-25 | **ELEGIDO presentado como impuesto** | FTMO «solo publica en vivo» el spread (`FTMO-REGLAS.md:310`). F17 sin hacer. Mediana de Dukascopy: 4 puntos (`F35-ORDEN-STOP-PIVOTE.md:212`) | Ver S-02 |
| 14 | Spread supuesto sin ticks: p90 por hora local de Madrid | `llenado.yaml:16-28`; 0051:124-133 | ELEGIDO | 18 horas perdidas sobre 76 días (RECORRIDA-3:107-120); PS:116 | Poco efecto |
| 15 | Comisión 2,50 USD por lote y lado, en los dos lados | cuentas yaml:382-415; 0090:102-128 | IMPUESTO, medido en la prueba gratuita; **la lectura de ida y vuelta es del consultor** | El asterisco «USD/LOT*» sin responder (`FTMO-REGLAS.md:328`; `HOJA-DE-RUTA.md:709-711`; PS:58) | Ver S-03 |
| 16 | Deslizamiento fijo 0 | `llenado.yaml:9`; 0051:70-78; 0092:99-115 | ELEGIDO, PROVISIONAL | 7 muestras de un minuto, «no un modelo» (0090:231-237) | Cualquier deslizamiento ≥ 0 aleja el techo de ganar |
| 17 | Swaps a la medianoche del huso del perfil | 0052:56-60 | ELEGIDO, PROVISIONAL | 0090:209-229 | Sin efecto |
| 18 | Una cuenta por mes, en fase reto | 0092:214-224; 0098:55-57 | ELEGIDO por el consultor | «en vivo la cuenta nunca salta de enero a abril» | Favorece el techo. No cambia b) |
| 19 | Ninguna otra regla abre o cierra | 0098:58-60 | ELEGIDO | f) mide su cuenta sin protecciones | Ver S-06 |
| 20 | Umbrales 3 % de pérdida diaria y 94 % de equity | 0092:87-91; 0098:101-111 | ELEGIDO (márgenes sobre FTMO) | Límites de FTMO 5 % y 10 % | Ver S-06 |
| 21 | Equity vigilada con la peor marca por minuto | cuentas yaml:256-267; 0052:44-55 | IMPUESTO y ELEGIDO | `FTMO-REGLAS.md` R2/R3 | Solo d) y e) |
| 22 | Dukascopy BID como serie propia | 0005:5-52; 0024 | ELEGIDO | A-16 sin medirse velas con velas (`ambiguedades.yaml:325-328`) | Ver fila 5 |
| 23 | Rejilla H4 anclada a 17:00 America/New_York; servidor = Nueva York + 7 h | 0005:25-31; 0090:44-100 | ELEGIDO y DERIVADO, no medido | ADR-0090:90-100; R6a.8 | En el techo solo mueve RN-002 (7) |
| 24 | Las dos sesiones son velas H4 de la rejilla | 0069:15-37 | IMPUESTO | `ev-v10-010429-0c93f24a`; escrito del 2026-10-06 | Sin efecto en el techo |
| 25 | Stops_level 0 y freeze level 0 | cuentas yaml:444-458; 0071:44-55 | IMPUESTO, medido en prueba gratuita | Demo, filas 4 y 5 | Sin efecto con 0 |
| 26 | Eventos del bróker al siguiente cierre de M1 | 0053:89-93, :217-221 | ELEGIDO, PROVISIONAL | «Se revisa con la demo» | Retraso de hasta una M1 en la reacción |
| 27 | Cierre de RN-030 al cierre de M1 | 0053:173-177 | ELEGIDO, PROVISIONAL | — | Fuera del techo |
| 28 | El trader (FX Replay) llenaba al nivel, sin spread ni comisión | no está escrito en ningún ADR | **SIN FUENTE** | `ev-v3-010111-b7c16b19` («no he tomado en cuenta … el split y las comisiones»); bid/ask/mid nunca medido (`AUDITORIA-2026-09-13-ultracode.md:1636`) | Es la premisa de ADR-0098 §3 C. Ver S-02 |
| 29 | Sesiones con BE omitidas en libros sin vídeo (S-14) | 0098:173-176 | HECHO declarado | `ev-v15-011912-0ae32588`, `ev-v16-003421-b824b770` | Cada una costaría al menos comisión+spread: el techo real sería peor. Refuerza C |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids S-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/S.md).

### R · La ruta con la salida C

**Conclusiones.** La sesión siguiente se prepara y no se graba; ningún documento activo dice otra cosa
(R-01). Lo que puede avanzar sin el ADR de C: F17 y R6a.8 en la misma prueba gratuita, R6a.3, la letra
C (la voz del ASR, que decide F5 de julio), Q y las guardias (R-13, R-14). R6a.4-R6a.6 pierden sentido
si se reabre ADR-0082 §4 (R-08, MATIZ). La tabla de fechas de AUDITORIA-2026-11-21 §1 ya no se sostiene
en R4.6 ni en el umbral (R-05). Tres textos de estado no recogen ADR-0098 (R-02, R-03, R-04). R-16 queda
REFUTADO por mí (registro 01:00): A-16 no está medida velas contra velas.

#### 1. Tabla de tramos y letras

Leyenda de «¿espera al ADR de C?»: ESPERA (no debe arrancar o grabar), LIBRE (avanza), INÚTIL-SI (se vuelve inútil según qué decida el ADR), BLOQUEADA-POR-OTRA-COSA (la puerta 0,70/0,60, que C no toca).

| Tramo / letra | Depende de (hoja) | Hecho cuando (hoja) | ¿Espera al ADR de C? | Por qué (fichero:línea) | Qué aporta al ADR de C |
|---|---|---|---|---|---|
| R4.7 (salida C) | prueba gratuita de FTMO viva para F17 (HOJA:440) | un ADR de Aleks decide si se sigue y cómo (HOJA:442) | Es el propio trámite; ABIERTA (HOJA:443) | ADR-0098:144-148; HOJA:437-443 | Es el insumo del ADR |
| R4.6 (ciclo de afinado; sesión siguiente a la 7b) | R4.3; «para grabar, R4.7» (HOJA:432) | julio cumple mínimos, o el pivote o ADR-0098 cambian el objetivo (HOJA:434) | ESPERA para grabar; la preparación sigue permitida (HOJA:435; PS:28) | C manda sobre el pivote (ADR-0098:157-158; meta.txt, última línea) | Su preparación no necesita el ADR; grabar sí |
| R4.3 (sesión 7) | R4.4 y R4.5 | 7a/7b activadas y pivote leído | HECHA (HOJA:403) | pivote leído «una sesión más» (RECORRIDA-3 §1 (:455, :463), :665-667) | Dato del pivote |
| Letra F de la NA | — | — | Su paso siguiente (R4.6) espera | PS:28 | — |
| R6a.1, R6a.2, R6a.8 (lo hecho: EA, capa generada; R6a.8 pendiente) | R6a.1 y R6a.2 (HOJA:626 para R6a.8) | HOJA:545-547, 559-563, 628-629 | LIBRE | ADR-0082 D3: la capa no decide (HOJA:523-528). R6a.8 mide `anclaje_h4` real (HOJA:620-629) | R6a.8 cabe en la misma prueba gratuita que F17 |
| R6a.3 (órdenes idempotentes, reconstrucción) | R6a.1 y R6a.2 (HOJA:573) | HOJA:575 | LIBRE; Aleks ejecuta en demo (HOJA:572) | Es plataforma genérica, vale con EA o con Python | Comparte prueba gratuita con F17 |
| R6a.4, R6a.5, R6a.6 (portan freno, veto, cierres, tope a MQL5) | R6a.2/R6a.3 (HOJA:584, 593, 603) | «pasa los mismos casos que sus tests de Python» | INÚTIL-SI el ADR reabre ADR-0082 §4 (Python decide en vivo) | Portan código de Python al EA (HOJA:577-606). ADR-0082 recuadro: FTMO permite que decida un programa en Python y «quita la razón» del descarte (ADR-0082:101-114); ADR-0098:225-227 y :229-231 dejan la arquitectura para los ingenieros | Opción (3) de las del orquestador |
| R6a.7 (pre-vuelo) | R6a.1 a R6a.6 y R6a.8 (HOJA:617) | HOJA:618 | Hereda lo de R6a.4-6 | HOJA:617 | — |
| R6.0 (arquitectura en vivo) | nada | HECHA (HOJA:641) | Reabrible solo con un ADR nuevo | HOJA:637; RUMBO:37 y :43; ADR-0082:114 | — |
| R6.1 (porte F28-F32) | R5.6 (HOJA:648-650) | F32 con paridad medida | BLOQUEADA-POR-OTRA-COSA (puerta de R5.6) y, además, INÚTIL-SI Python decide | ADR-0098:223-228 | — |
| R5.2 (mayo) | R3.10 con un «sí» (HOJA:464) | HOJA:468 | BLOQUEADA-POR-OTRA-COSA: la corrida (3) dio «no» por tercera vez (HOJA:326-328) | ADR-0070 §3 (NOTA, :147) | El ADR de C es quien podría tocar la puerta (ADR-0098:133-138 lo prevé solo para A) |
| R5.1 / letra G (PREREGISTRO, F26 sobre febrero) | nada para lo que queda (HOJA:455); F26 depende además de febrero y de R5.2 (HOJA:455) | HOJA:458 | PARCIAL: la parte de código (comando de medida, arreglo de kappa) LIBRE; «Aleks pide febrero al trader» (PS:34) conviene alinearla con el ADR | Febrero con vídeo y voz es tiempo del trader; si C acaba en (3) o (4), no sirve | Febrero es mes ciego limpio; no sirve para el techo |
| R5.3 (marzo) | lectura de Aleks (HOJA:476) | HOJA:478 | LIBRE para su paso (a); su utilidad depende de que se siga | Sin letra en la NA (AUDITORIA:125, E19) | — |
| R5.4 / letra I (diciembre 2025) / N | R2.2, R2.1, R1.1 (HECHAS) (HOJA:486) | HOJA:488 | LIBRE; el consultor decide construcción o reservado | Cierres hacia atrás los pide también R5.6 (HOJA:501-502). ADR-0098:152-153: diciembre como construcción cambia el techo (salida D) | Es la única vía de material nuevo para releer el techo, pero sin vídeo (S-14) |
| R5.5 (F26 y F27) | R5.1, R5.2, R5.3 (HOJA:493) | HOJA:495 | BLOQUEADA-POR-OTRA-COSA (R5.2) | HOJA:493 | — |
| R5.6 (rentabilidad, la puerta) | R5.1 (G) y re-corrida «habilita medir: sí» (HOJA:507) | HOJA:509 | BLOQUEADA-POR-OTRA-COSA; solo un ADR que desate la puerta la libera | AUDITORIA:79-84 (opción 2 «desatar», nunca decidida); ADR-0098:133-138 | F17 es requisito (HOJA:505-506; ADR-0092 §4) |
| R5.7 | R3.10 | HECHA con salida C (HOJA:520-522) | No aplica | ADR-0098:94-95 la sustituyó | — |
| R7.1 (demo y sombra) | R6.1 y R6a (HOJA:662) | HOJA:664 | BLOQUEADA aguas abajo | HOJA:662 | — |
| R7.2 (otros activos) | R7.1 (HOJA:673) | HOJA:675 | BLOQUEADA aguas abajo | HOJA:673 | — |
| R7.3 (sombra en diferido) | julio cumple los dos mínimos del pivote; antes, R4.6 (HOJA:681) | HOJA:683 | ESPERA (depende de R4.6) | HOJA:681 | — |
| Letra A (noticias de FTMO) y M | nada / sin objeto (PS:40, :44) | — | LIBRE, irrelevante para C | PS:40-44 | No aportan |
| A.1 (ejecuciones 2 y 3) | — | HECHA (HOJA:701-703) | — | HOJA:701-703 | Las observaciones de deslizamiento (ADR-0090 §7: siete muestras de un minuto) |
| A.2 (preguntas a FTMO) | respuesta de FTMO (HOJA:722) | HOJA:723 | LIBRE; la respuesta del 2026-11-20 es insumo de C | HOJA:725; ADR-0082:101-114 | Python puede decidir en vivo según FTMO |
| A.4 (copia de seguridad v18-v21) | nada; «fecha límite: antes de grabar la próxima sesión» (HOJA:743) | v6 a v21 en Drive (HOJA:745) | LIBRE; no se mueve por C, pero el plazo de HOJA:743 ahora lo marca el ADR, no el calendario | HOJA:746 (vencida para la 7b) | — |
| A.5 (lo que queda de la demo; grabador F17) | prueba gratuita viva (HOJA:756) | HOJA:758 | LIBRE y pedido por C | HOJA:754-755; ADR-0098:144-145 | F17 = costes reales |
| Letra C (voz que el ASR se salta) | nada que la bloquee: HOJA:154-155 dice «no va antes de R4.4, láminas, preparación de la 7»; las tres están HECHAS | HOJA:153 | LIBRE | PS:32; HOJA:145-155 | Su salida decide F5 (`material_sin_video` de julio), que es el S-14 que C manda revisar |
| Letra D / G.1 (guardias) | nada (HOJA:771) | HOJA:773 | LIBRE; sin prisa (PS:25) | AUDITORIA:53-54 contó las ramas de guardias dentro del 29 % | Con la fidelidad pausada, es lo que más llena el hueco |
| Letra J (`kit hoja`) | «antes de la próxima sesión que etiquete días» (PS:38; G.2) | — | ESPERA: sin sesión, sin urgencia | PS:38 | — |
| Letra Q (R2.3, exportación de agosto) | exportación del trader (HOJA:122) | HOJA:124-125 | LIBRE y UTIL para C | ADR-0092 §11 (:274-285): si llega, el bloque `material_sin_video` cambia | Quita parte del sesgo S-14 al techo |

#### 2. Tabla de fechas de AUDITORIA-2026-11-21 §1 (líneas 62-72), fila a fila

| Fila | Con la salida C |
|---|---|
| R4.3 (7b ingerir, activar, corrida y pivote), «2–4 semanas, diciembre», cabe | Hecha: 7a y 7b activadas, corrida (3) y pivote leídos el 2026-11-22 (HOJA:403, :326). S-22 no se activó (RECORRIDA-3:669). La fila ya no es una estimación |
| R4.6 (2–5 vueltas, enero–febrero), «con riesgo» | No se sostiene: no se graba hasta el ADR de Aleks (HOJA:435). Sin fecha. Además C manda sobre el pivote que fijaba «una sesión más» (meta.txt, últimas líneas) |
| Umbral 0,70/0,60, «optimista, finales de abril» | No se sostiene como hipótesis: la AUDITORIA lo basó en +5 puntos por vuelta «que nunca se ha observado» (:55-56). Medido: de la corrida 2 (15,7 %/13,9 %) a la (3) (15,2 %/14,4 %), con la 7a y la 7b activadas entre las dos, cobertura −0,5 y precisión +0,5 (Marcador, HOJA:910-911; aritmética sobre cifras publicadas). Quedan unos 55 puntos de cobertura al 0,70 (aritmética: 70 − 15,2) |
| R5.2 (mayo), «No (lo hereda)» | Sigue «No»; sin cambio, y su «Depende» exige un «sí» que ya van tres «no» (HOJA:464; ADR-0070 §3) |
| F26 (3–5 semanas en paralelo), «No» | Sigue «No» mientras R5.5 dependa de R5.2 (HOJA:493). Pero el PS (:34) lo presenta como si solo faltaran febrero, el comando y kappa (ver R-11) |
| R5.6 (rentabilidad), «No» | Sigue «No»; ninguna decisión desató la puerta (ADR-0098 no la toca salvo en A, :133-138) |
| R6a.3–R6a.8, 6–9 semanas, «Cabe» | Cabe sin cambio, pero solo R6a.3 y R6a.8; R6a.4–R6a.6 quedan INÚTILES-SI el ADR reabre ADR-0082 §4 (ADR-0082:101-114; ADR-0098:229-231). La fecha de 6-9 semanas de las tres piezas portadas no se sostiene hasta la decisión de los ingenieros |
| F28 + F29–F32 (porte, 8–12 semanas), «No» | Sigue «No» por R5.6, y ahora condicional: si Python decide, no hay porte (ADR-0098:225-227) |
| F33 / F34 / F35, «No» | Sin cambio; ADR-0098 §6 lo dice sin vías para marzo de 2027 (:220-231) |
| «Aunque se quitara esa puerta, F35 a finales de mayo de 2027 como pronto» (:59-60) | Se sostiene como cota inferior, pero la cadena entera con la puerta es «hacia noviembre de 2027» (:57-58), posterior a agosto de 2027, el inicio de las prácticas de Aleks (HOJA:7). Esa cadena se apoyaba en la hipótesis de +5 puntos por vuelta, no observada |

#### 3. Tramos que mueve cada opción (de trabajo, sin elegir)

| Opción | Qué se mueve |
|---|---|
| (1) seguir tras F17 y el contraste | R4.7 HECHA; se abre R4.6 (grabar la sesión 8; antes A.4 para v18–v21, HOJA:743; J si etiqueta días, PS:38); R4.3 y su pivote «una sesión más» vuelven a leerse (ADR-0098:157-165); la puerta de R5.2/R5.6 sigue; las fechas de §1 de la AUDITORIA se desplazan lo que dure la espera, y el umbral no tiene trayectoria |
| (2) pausar y medir primero (puente, F17, cancha) | R4.7 se amplía con medidas; «puente» y «cancha» no están definidos en el repo (grep sin resultados); el puente en vivo lo descartó ADR-0082 §4 y solo lo abriría un ADR nuevo (RUMBO:43), así que tocaría R6.0 (HECHA→reabierta) y R6a.4–R6a.6/R7.3; A.5 y R6a.8 suben de prioridad; R4.6 sigue en pausa |
| (3) cambiar de objetivo (bot que solo opera lo que reproduce, o reabrir arquitectura) | ADR-0098 §3 A ya lo prevé solo con techo y parejas ganando (:130-138); el de C exigiría su propio ADR. Mueve R5.2/R5.6 (la puerta 0,70 «no la alcanza nunca» un subconjunto, :134-136), R4.6 (hecho cuando), R6a.4-R6a.7, R6.1, R7.x y MASTER_PLAN F29-F32 |
| (4) parar o rebajar la meta | Mueve HOJA:7 (metas), todo R5.5-R7, R6a (salvo lo hecho) y A.4/A.5; no hay entrada ni ADR para esto en el repo |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids R-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/R.md).

### M · El método de fidelidad

**Conclusiones.** El 0,70/0,60 no está a la vista: la corrida que cuenta pasó de 31 a 30 parejas con la
7a y la 7b (M-01, MATIZ: plano, no negativo; la diaria sí mejora), y con las órdenes de hoy la cobertura
no puede pasar del 27,8 % (M-04, MATIZ). El umbral está en el camino crítico al vivo (M-03, MATIZ) y no
tiene derivación escrita (M-14, SOBREVIVE). S-14 no explica la precisión (M-08, SOBREVIVE). Un bot fiel
heredaría aproximadamente el techo (M-15, MATIZ: inferencia; c) es el percentil 5). Las parejas no
concluyen (M-11). El pivote no tiene regla de parada, aunque C manda sobre él (M-12, MATIZ).

#### 1. La trayectoria

| Corrida (informe · tag) | Cuenta | Cobertura / precisión que cuenta | Parejas | Diaria (cob / prec · parejas) | Qué entró entre medias |
|---|---|---|---|---|---|
| RECORRIDA-CONSTRUCCION · stable/F38g, 2026-10-27 | arrastrada (solo opera enero) | 3.5 / 13.2 (7/198, 7/53) | 7 | 20.7 / 15.6 · 41 | activación de la sesión 5 (la del 2026-10-23; F38e y F38f) |
| RESPALDO-M1 · F38j, 2026-10-29 | arrastrada | 3.5 / 13.2 | 7 | 20.2 / 15.4 · 40 | arreglo del respaldo M1, sin sesión |
| RECORRIDA-CONSTRUCCION-2 · F38t, 2026-11-08 | una por mes | 15.7 / 13.9 (31/198, 31/223) | 31 | 20.2 / 14.6 · 40 | sesión 6 (2026-11-04; F38m a F38o), comisión, sello M1, **cuenta por mes** |
| RECORRIDA-CONSTRUCCION-3 · F39l, 2026-11-22 | una por mes | 15.2 / 14.4 (30/198, 30/208) | 30 | 22.7 / 16.3 · 45 | 7a (2026-11-16, F39e) y 7b (2026-11-20 y 21, F39k) |

Fuentes: Marcador, `docs/plan/HOJA-DE-RUTA.md:905-911`; `RECORRIDA-CONSTRUCCION.md:644-653`; `RECORRIDA-CONSTRUCCION-2.md:419-436` y `:565`; `RESPALDO-M1.md:745` y `:765`; `RECORRIDA-CONSTRUCCION-3.md:455-463` y `:626-627`. Las fechas de las sesiones salen de los ids `fb-2026-10-23-sesion-05`, `fb-2026-11-04-sesion-06` y `fb-2026-11-16-sesion-07`, y de `SESION-08-EXTRACCION.md:905`.

**Aritmética sobre cifras publicadas.** Hacen falta 0,70 × 198 = 138,6, es decir 139 parejas. Con 139 parejas, la precisión de 0,60 admite como mucho 231 operaciones puntuables del bot (139 / 0,6). Hoy son 208 en la que cuenta y 276 en la diaria. Mientras el bot no opere más, la condición que manda es la cobertura.

- **La que cuenta**, el único tramo con el mismo método (R2 → R3, dos días de sesión, 14 días): parejas −1, cobertura −0,5 puntos, precisión +0,5; a ese ritmo la cobertura no llega nunca; la precisión, en (60 − 14,4) / 0,25 ≈ 182 días de sesión.
- **La diaria, R1 → R3** (sesiones 6, 7a y 7b; 26 días): +4 parejas, +2,0 puntos de cobertura, +0,7 de precisión. Hacen falta unas 70 sesiones para la cobertura y unas 187 para la precisión. Por calendario: 94 / (4 / 26) ≈ 611 días.
- **La diaria, R2 → R3** (la más favorable: 7a y 7b; 14 días): +5 parejas, +2,5 puntos de cobertura, +1,7 de precisión. Unas 38 sesiones para la cobertura y unas 51 para la precisión. Por calendario, ≈ 263 días (unos 9 meses). Y es la diaria, no la que cuenta.

#### 2. La cascada de ADR-0092 §2 en la corrida (3), solo recuentos

| Escalón | Cuenta por mes (cuenta) | Diaria (diagnóstico) | R2 que cuenta | R2 diaria |
|---|---|---|---|---|
| sin orden del bot en su (día, sesión, dirección) | 70 (35,4 %) | 27 (13,6 %) | 67 | 48 |
| orden, entrada fuera de tolerancia | **73 (36,9 %)** | **88 (44,4 %)** | 67 | 72 |
| entrada, stop fuera de tolerancia | 37 (18,7 %) | 55 (27,8 %) | 44 | 54 |
| el caso no trae stop | 0 | 0 | 0 | 0 |
| en el nivel, no llenada | 3 | 6 | 6 | 6 |
| llenada fuera del instante | 1 | 1 | 0 | 0 |
| las cuatro piezas | 14 (7,1 %) | 21 (10,6 %) | 14 | 18 |
| órdenes del bot en un (día, sesión, dirección) sin trader | 321 | 362 | 425 | 526 |

Fuentes: `RECORRIDA-CONSTRUCCION-3.md:474-482`; `anexos/RECORRIDA-CONSTRUCCION-3/diaria.DIAGNOSTICO.cuenta=diaria.txt:3897-3903`; `RECORRIDA-CONSTRUCCION-2.md:438-446` y `:575-576`.

Con la 7a y la 7b, en la diaria, 21 operaciones pasaron de «sin orden» a tener orden, y la entrada fuera de tolerancia ganó 16. Ahora el bot está en la sesión y en el lado del trader, pero en otra entrada.

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids M-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/M.md).

### X · El proceso

**Conclusiones.** Por número de ramas, el proceso no es desmedido desde RUMBO (5 de 18; X-01); lo que
pesa es el coste unitario: un make check de unos 27 minutos por commit, del orden de 70 horas de reloj en
dos semanas como techo (X-03, MATIZ: unos 190 commits sin merge, no 169). Lo barato y sin tocar el
holdout: reordenar `check:` para que los pasos de segundos vayan antes de los 27 minutos (X-08),
remedir xdist (X-05) y separar los tests que leen data/ (X-06). La tabla de errores no baja (X-07).

#### Cuenta de ramas
Fuente: `git tag -l "stable/*"` (172 tags), `git log --merges --first-parent main` (177 merges, 1577 commits desde el 2026-09-03) y la tabla de ERRORES-RECURRENTES.md (líneas 115-132 = las 18 ramas). Clasificadas por el asunto del merge y la fila de la tabla (sin leer cada informe entero).

Desde RUMBO (2026-11-08) hasta `stable/F39l`: 18 ramas, tags F38u a F39l.

| Tipo | N | Ramas |
|---|---|---|
| Fidelidad, logística y herramienta de sesión | 7 | video-julio, laminas, preparacion-sesion-7, laminas-motivos, sesion-07, laminas-sesion-7b, sesion-08 |
| Fidelidad, medida o motor o método | 5 | trazas-ablacion, activar-sesion-07, activar-sesion-08, preregistro, recorrida-construccion-3 |
| Plataforma | 1 | capa-generada |
| Guardias y proceso | 5 | guardia-falsos-positivos, dieta-estado, skills-metodo, guardias-holdout, guardia-enlaces |

Hasta F39j reproduce lo publicado (10 de fidelidad y 6 de otras, AUDITORIA-2026-11-21.md:50-52); con F39k y F39l, 12 y 6. Total histórico: 78 ramas (76 en la auditoría anterior).

#### Protege el holdout o protege contra errores de proceso (no se recomienda quitar ninguna barrera del holdout)

| Pieza | Protege | Se puede tocar |
|---|---|---|
| Puerta de ADR-0033, `casos_reservados`, compuerta del arnés | HOLDOUT | No |
| Familia 1 de `guardia.py` (contenido protegido, ADR-0088, rutas canónicas y enlaces) | HOLDOUT | No |
| G2 (fila de HOLDOUT del día; ADR-0021 §4) | HOLDOUT | No; reducir cuántos `make check` leen reservados (X-06) |
| Familia 3 (~2190 líneas) | HOLDOUT de forma indirecta; sin ADR | Solo para evaluarla, con una separación del sistema operativo igual o más fuerte (pregunta para los ingenieros) |
| Espera a la CI (404), git/rm/make (653) | PROCESO | Separar en `permissions` o en otro hook pequeño |
| El sello del árbol | PROCESO | Se mantiene; cambiar cómo se calcula, no si existe |
| Revisor de 30 pasadas en 18 ramas | PROCESO | Etiquetar los hallazgos por patrón |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids X-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/X.md).

### K · El código

**Conclusiones.** Ningún defecto de techo_parejas.py puede cambiar C: «no gana» sale por cuatro vías
(K resumen). El control no ejerce las ramas que solo usa el trader (K-02, P1-17). La deuda de las
cotizaciones sin tick se ve en la línea base: 5 de 25 esperas en horas sin ticks (K-04, MATIZ). La letra
M de la Next Action dice «sin objeto», y 21 de los 50 break even del bot pierden en bruto (K-06, MATIZ).
Para el porte faltan estados de MT5 que el simulador no tiene (tabla).

#### Estados de MT5 (la capa MQL5 no opera; su columna dice qué lee o qué tiene planeado)

| Estado | Simulador | Capa MQL5 | Qué tendría que reproducir el porte |
|---|---|---|---|
| Dos stops a la vez (varias pendientes, o SL y TP en el mismo tick) | Varias órdenes con tope `ordenes_simultaneas_max` (broker.py:1114-1121); reserva margen por cada stop (PS:84); si un tick cruza SL y TP gana el stop (llenado.py:322-332, DN-2) | Nada | Cuándo mide MT5 el margen de una pendiente (ADR-0090 §4, M4) |
| Llenados parciales | No (broker.py:900-909) | Nada; FOK en MedirDemoFTMO | Modo de llenado y reparto de deals; K-13 |
| Recotizaciones / deslizamiento a mercado | Cierre al último tick, sin deslizamiento (broker.py:1011-1023); stop al tick más el fijo (0) | Nada | Desviación permitida y códigos; K-08 |
| Órdenes que sobreviven a un reinicio | No hay reinicio; todo se cierra o cancela al fin del día (cableado.py:349, :457-466) | OnInit no lee órdenes ni posiciones (Botsito.mq5:55-77) | R6a.3 (HOJA:565-575), MASTER_PLAN:286 |
| Expiración de pendientes | Admitida (broker.py:806-807, :862-868), sin uso | Nada | GTC frente a DAY en FTMO, sin medir |
| Gaps de fin de semana | Nada cruza el día; ventana de ADR-0068 (broker.py:841-854); hueco al precio del tick | Lee las sesiones; el veto es R6a.5 | El veto de R6a.5; calendario caducado |
| Spread en el rollover | Spread de Dukascopy por tick; p90 por hora sin ticks; las ventanas excluyen el rollover | No lee el spread | El spread de FTMO (F17); `spread_maximo` UNKNOWN |
| stops_level / freeze level en vivo | Stops level del perfil (0) solo para pendientes (broker.py:586-590), no al mover el SL; freeze sin modelo | Constante 0 (Generado.mqh:87) | Releer antes de cada petición; manejar 10016 |
| Modificar el SL del lado malo (break even) | Lo acepta y salta en el tick siguiente (K-05, K-06) | Nada | Rechazo 10016 y conservar el stop original |
| Latencia decisión → orden | 0 (K-09) | Nada | Detectar la vela nueva y la latencia real |
| Eventos del bróker al motor | Retraso de hasta una M1 (ADR-0053 §9 2.1, PROVISIONAL) | Nada | La cadencia real de OnTradeTransaction |
| Cancelar contra llenar | Atómico (K-14) | Nada | Carrera de RN-006 y su idempotencia |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids K-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/K.md).

### D · El material

**Conclusiones.** El techo ya está medido sobre los cuatro meses de construcción; releerlo pide material
nuevo o F17, y esa regla solo está escrita en la salida D (D-01, SOBREVIVE). Medir 2025 ya gasta junio a
noviembre sin vuelta si no pasa (D-02, MATIZ). Diciembre de 2025 como construcción pide ADR y código
(D-03, MATIZ). La copia de seguridad de v18 a v21 sigue sin hacer (D-05). Febrero, el único mes limpio,
nadie lo ha pedido (D-07).

#### Tabla de material

| Material | Estado | Fuente | Riesgo |
|---|---|---|---|
| Enero 2026 (libro, del 2 al 30; sin vídeo) | construcción | `criterio_fidelidad.yaml:44,47,62`; ADR-0079 | Sesgo S-14 (sin vídeo). Sus sesiones dependen de diciembre (PS NA:I; deuda PS:147). |
| Abril 2026 (sin vídeo, salvo un día) | construcción | `criterio_fidelidad.yaml:47,62-64` | Sesgo S-14. |
| Julio 2026 (libro; vídeo «provisional»; export solo del 1 al 17) | construcción | `criterio_fidelidad.yaml:42,47,59-60`; PS NA:Q | «Con vídeo» sin comprobar (T). Es el único mes que sostiene el pivote y el diagnóstico del techo. |
| Agosto 2026 (vídeo S-14; libro xlsx) | construcción | `criterio_fidelidad.yaml:47,62`; PS NA:Q | Falta la exportación del trader (Q); los casos salen del xlsx. |
| Mayo 2026 | medida (6 días dev; 13 reservados según HOLDOUT:3) | `criterio_fidelidad.yaml:48`; `HOLDOUT-EXPOSICIONES.md:196-198` | «No se toca» hasta que la construcción llegue al umbral (R5.2). |
| Particiones holdout-1/2/3 | reservado | PREREGISTRO.md §3 (8/8/8 días; 1 retirado en la 3; el día quemado de la 2 no está en retirados, PS:156) | Puerta cerrada: no existe el comando de medida (PS:154). |
| Septiembre 2026 (fidelidad-1: 10 días, 4 retirados, 6 medibles) | reservado | PREREGISTRO.md §3; PS NA:G | Su libro no está en `libros.yaml` (PS:155) y se declaró 4 veces como visto. |
| Marzo 2026 (xlsx + 7 imágenes) | recibido SIN ABRIR | REGISTRO-MARZO.md (Estado); HOJA R5.3; PREREGISTRO §3 (fidelidad-2 y -3 con 0 días) | Fuera de git, en una sola máquina. No está en `libros.yaml`. Las 7 imágenes no se abren nunca. |
| Febrero 2026 | reservado y NO recibido (hay que pedirlo con vídeo y voz) | ADR-0096:57; PS NA:G; HER:6; HOJA:873 | Es el único mes «limpio». F26 lo gasta de una vez. Hoy nadie lo ha pedido. |
| Diciembre 2025 (xlsx + capturas, sin vídeo) | recibido SIN ABRIR y reservado (`"2025-12"`) | PS NA:I; ADR-0092:125-126; HOJA R5.4 | El trader ya comentó operaciones de diciembre en v10 (PS NA:I): exposición parcial ya declarada. Sin salida de `meses_reservados` posible hoy (PS:81). |
| Junio-noviembre 2025 (rentabilidad) | reservado por ADR, sin material | ADR-0092:117-158; `criterio_fidelidad.yaml:84-86` | Sin velas ni ticks bajados (ADR-0092:126). Se gastan de una vez. |
| Enero-mayo 2025 (extensión) | reservado por ADR | `criterio_fidelidad.yaml:85` | Se añaden de uno en uno solo si N<100. |
| Octubre y noviembre 2026 | reservados | PS NA:F | — |
| Vídeo de mapeo (recibido el 2026-11-18) | recibido SIN ABRIR, fuera del repo | PS NA:F; ACTIVAR-SESION-08.md:768; RC3:816 | Solo existe fuera de git. No sé qué mes cubre. |
| Crudas y WAV de v18 a v21 | falta la copia | HOJA A.4 (746); PS:135; AUDITORIA E1 (107) | Fecha límite vencida; la próxima sesión no puede grabarse sin ella. |
| Libros declarados en `libros.yaml` | 5 (agosto, abril, mayo, enero, julio) | `libros.yaml:17-83` | Faltan septiembre, marzo y diciembre. |

#### Tabla de lo que gasta cada opción (no las elijo)

| Opción | Material que gasta | Reversible | Fuente |
|---|---|---|---|
| 1. Seguir con sesiones de fidelidad | Días `dev` de los 4 meses de construcción. Ningún mes reservado, salvo exposición accidental en vídeo (precedente: v20, declarado). Antes, la copia de v18-v21 (A.4) y que un ADR de Aleks levante R4.7. | Lo reservado no se toca. El tiempo del trader no se recupera. | HOJA R4.6 (429-435), R4.7 (437-443), A.4 (746); ADR-0098 §3 C |
| 2. Medir primero | F17 en prueba gratuita: ningún material del repo (una prueba de FTMO, repetible con una sola activa a la vez, A.5:754). La «rama del puente sobre construcción» NO es una rama escrita. El puente en vivo está descartado por ADR-0082 §4 y solo lo abre un ADR nuevo (RUMBO:43). La «cancha» no está definida en el repo (`git grep` vacío). | F17: sí. Puente: no aplicable hasta un ADR. Cancha: sin fuente. | HOJA A.5, R4.7; RUMBO-2026-11.md:37-43 |
| 3. Medir 2025 ya | 2025-06 a 2025-11 de una sola vez, más hasta 5 meses de extensión si N<100. Si no pasa, `vistos_rentabilidad` y no vuelven a medir. Antes: velas y ticks de 2025 bajados, cierres hacia atrás hasta enero de 2025, spec sellada, el comando que no existe, y un ADR que desate la línea «habilita medir». | NO: «una sola ejecución» y los meses medidos no vuelven a medir. La puerta no puede dar «pasa» antes de F17. | ADR-0092 §4 (113), §5 (117-158), §6 (176); `criterio_fidelidad.yaml:84-86`; HOJA R5.6 (497-509); AUDITORIA §1 opción 2 |
| 4. Diciembre 2025 como construcción | Diciembre 2025 sale de reservado a construcción: ADR + cambio de código (hoy un mes no sale de `meses_reservados`). Además, calendario de cierres hacia atrás (hoy empieza a principios de diciembre de 2025), velas y ticks de diciembre, entrada en `libros.yaml`, columna de fechas leída por Aleks. | NO: `meses_reservados` es solo añadir (`holdout.py:652-664`). Diciembre queda además como mes ya comentado por el trader en v10. | PS NA:I y PS:81; HOJA R5.4 (480-488); ADR-0092:145-146; ADR-0072; ADR-0039 |

Sus hallazgos, con su estado tras la pasada adversaria, están en §12 (ids D-NN); la entrega entera, tal cual, en la carpeta de trabajo (entregas/D.md).

### I · Los ingenieros

Su entrega es el borrador de índice de §11; sus hallazgos, en §12 (I-NN).

## §5 · El eje propio

### E1 · La robustez de la salida C, pieza a pieza

**Por qué se abrió** (registro, 01:16): decide si el ADR de C puede tomarse ya o tiene que esperar a
una medida. Preguntas fijadas antes en §0 (añadido de las 01:16). Lo hice yo, desde las entregas y las
fuentes que cito; sin subagente.

**Qué hace falta para salir de «no gana»** (ADR-0098 §2, :103-110). El techo deja de ser «no gana»
solo si a la vez: la esperanza es ≥ 0, el percentil 95 es ≥ +0,10, d) baja del 3 % y e) sube al 94 %
o más, y f) no hay cuenta suspendida. Hoy: −0,239, −0,026, 4,88 %, 92,05 % y no (meta.txt:13-17).

*Aritmética sobre cifras publicadas* (meta.txt:13-14): la distancia entre la media y el percentil 95
es 0,213 R; si el remuestreo conservara la anchura, el percentil 95 llegaría a +0,10 con una media de
−0,113. La condición que ata en la esperanza es, pues, la media ≥ 0: hacen falta +0,239 R por
operación, que a la pendiente de 0,1345 R por punto y llenado afectado (meta.txt:18 con
criterio_fidelidad.py:869-882) equivalen a unos 1,8 puntos por llenado afectado. Y d) y e) tienen que
cambiar también, y dependen de la secuencia de la cuenta, no solo de la media.

| Pieza | ¿Puede, sola, sacar al techo de «no gana»? | Por qué, con su fuente | Clase |
|---|---|---|---|
| Deslizamiento (F17) | **No.** Solo puede empeorarlo | El equilibrio pide 2,52 puntos a favor; una stop nunca se llena mejor que su nivel en el modelo (ADR-0057 §1) y la demo no lo vio (DEMO-EJECUCIONES-2-3.md:41). P4-02, SOBREVIVE | HECHO |
| El sesgo S-14 | **No, por dirección razonada** | Las sesiones omitidas eran de break even; con nuestros costes, un break even pierde la comisión (−5/D R). Añadirlas baja la media. No está medido (P3-07, MATIZ) | SUPUESTO ELEGIDO |
| Las 7 no colocables | **No** | Ni las 7 como ganadoras al máximo (objetivo de hasta 6 R) llevan la media de −0,239 a 0: queda en −0,018 (aritmética sobre meta.txt:9-13; P3-06) | HECHO |
| La mezcla de meses | **No** | Julio (−0,245, con vídeo) y el total (−0,239) casi coinciden (meta.txt:13, :23) | HECHO |
| El lote, el tope de 50, el margen, la cuenta por mes | **No mueven la esperanza** | El R no depende del lote: comisión 2,50×lotes×2 y riesgo lotes×D (cableado.py:1349-1352). Mueven d) y e), a favor del techo | HECHO |
| El spread de FTMO frente al de Dukascopy | **Quizá en la media; d) y e), sin saber** | Si el spread real fuera 1-2 puntos menor, del orden de +0,07 a +0,27 R (P4-03, aritmética; MATIZ en la pasada); la relectura de ADR-0092 §4 no tiene vía para meterlo | PREGUNTA PENDIENTE (F17) |
| El objetivo (A-56) | **Sin signo conocido** | El techo pone el objetivo a 3,75 veces el stop del trader; su material sale en [3,00; 3,75) en 26 de 38 ganadoras (ADR-0040:22-35). Más cerca sube el acierto y baja el pago (S-01, MATIZ) | Regla dicha por el trader (ADR-0073), contradicha por su material (A-56, ADR-0040 enmendado) |
| La geometría del break even (RN-014) | **Sin signo conocido** | 79 de 191 movidos (meta.txt:11); la zona posterior la leyó una sesión nocturna (ADR-0061 §4); cada break even cuesta la comisión (P4-09) | SUPUESTO ELEGIDO |
| La serie (A-16) y el modelo de llenado de FX Replay | **Sin signo conocido; escala suficiente** | 1-2 puntos es la escala de A-16 (BLOQUE-DE-LA-CAJA.md:197-206) y la de la distancia a cubrir; no medido velas contra velas (METODO-FIDELIDAD-RENTABILIDAD.md:888-893; P3-01, MATIZ) | PREGUNTA PENDIENTE |

**Conclusión de E1.** La salida C es robusta a todo lo que ADR-0098 §3 C manda revisar salvo a una
parte de F17 (el spread, no el deslizamiento), y no es robusta a tres piezas que C no manda revisar:
el objetivo, la geometría del break even y la serie y el llenado de FX Replay. Por eso el ADR de C
puede decidir hoy **el método** (qué se hace ahora y qué no), pero no puede concluir que **la
estrategia** no gana: solo que **su regla tal como la dicta, aplicada por nuestro simulador con
nuestros costes,** no gana (la redacción sale de la pasada del adversario general, §2).

| Id | Eje | Hallazgo | Clase | Gravedad | Evidencia | Alimenta | Lo refutaría | Estado |
|---|---|---|---|---|---|---|---|---|
| E1-01 | E1 | La salida C es robusta al deslizamiento, a S-14, a las 7 no colocables, a la mezcla de meses y al lote; no lo es (sin signo conocido) al objetivo, a la geometría del break even y a la serie y el llenado de FX Replay, que ADR-0098 §3 C no manda revisar | HECHO (cada fila con su fuente) + aritmética sobre cifras publicadas | CAMBIA LA DECISIÓN DE C | meta.txt:9-18; ADR-0098:103-110, :144-148; ADR-0057 §1; ADR-0040:22-35; ADR-0061 §4; METODO-FIDELIDAD-RENTABILIDAD.md:888-893 | a, d | Una medida del techo con una de esas tres piezas cambiada que dé el mismo «no gana» por las cuatro vías | Sus filas heredan el estado de P4-02 (SOBREVIVE), P3-07, S-01, P4-03 y P3-01 (MATIZ); las de las 7, los meses y el lote son aritmética comprobada por mí |

## §6 · Las preguntas para el trader

Para que el consultor las redacte en un mensaje de Aleks. **Ninguna lleva una cifra ni un resultado
nuestro** (ADR-0098 §3 C, :147; VIABILIDAD-COMISION.md:3-5, «NO SE ENSEÑA AL TRADER»). Van en su
lenguaje (la caja, el 0, el 0,8, el 1, el break even, la sesión, el objetivo 1:3), cortas, ordenadas
por la decisión a la que sirven. La columna «ya preguntado» dice qué no se repite: salen de P5, P2, P4,
P6 y S, comprobadas contra las PREGUNTAS de las sesiones 4 a 7 (nunca las HOJA-USADA).

**Bloque A · Sus resultados reales (la premisa).**

| # | Pregunta | Decisión a la que sirve | ¿Ya preguntado? |
|---|---|---|---|
| A1 | Con esta misma estrategia en EURUSD, ¿estás sacando dinero hoy de alguna cuenta? ¿Desde cuándo? (Basta sí o no y desde cuándo; no hace falta que digas cuánto.) | a (la premisa) | Nunca (P5-01) |
| A2 | ¿En qué firma o bróker tienes esas cuentas, y con qué tipo de cuenta? | a, c | Nunca; en el repo «cuenta fondeada» es la del bot (P5-01, pasada adversaria) |
| A3 | ¿Qué riesgo pones por operación en esas cuentas? ¿Lo has cambiado con el tiempo? | a, b | En parte: «1 en backtest; 0,4-0,5 en fondeo» (parametros.yaml:1279) |
| A4 | ¿Podrías pasarnos la exportación del historial de operaciones de unos días de tu cuenta real (el fichero que da la plataforma, no capturas de la pantalla de estadísticas)? Te diremos qué días, para no usar los que ya hemos mirado. | a, c (vía iii de la cancha) | Nunca |

**Bloque B · Si en real opera lo mismo que en el backtest.**

| # | Pregunta | Decisión | ¿Ya preguntado? |
|---|---|---|---|
| B1 | Cuando operas en real, ¿haces exactamente lo mismo que en tus backtests de FX Replay, o cambias algo (la caja, el 0, el 0,8, qué sesiones operas)? | a | Nunca directamente (P5-04) |
| B2 | En real, ¿te saltas alguna sesión? ¿Cuáles y por qué? ¿Alguna vez por ver que iba a acabar en break even? | a (S-14) | Solo sobre el backtest (docs/sesion-6/PREGUNTAS.md:256-271) |
| B3 | En real, ¿pones la orden pendiente o entras a mercado? ¿Siempre igual? | a, c | Solo sobre el dibujo del bot (docs/sesion-7/PREGUNTAS-7B.md:310) |

**Bloque C · La salida (dónde se separa más nuestro modelo de lo que él hace).**

| # | Pregunta | Decisión | ¿Ya preguntado? |
|---|---|---|---|
| C1 | Cuando arrastras el objetivo en la herramienta de FX Replay, ¿hasta dónde lo llevas: hasta que marca 3 sobre la distancia de la entrada al stop, o 3 veces la caja entera del 0 al 1? | a, d (A-56; el objetivo del techo) | A-56 no se le pregunta (ADR-0040 §2); la sesión 4 ratificó «del 0 al 1» (ADR-0073), pero no cómo lo coloca en la herramienta |
| C2 | En real, ¿esperas siempre al objetivo o a veces cierras antes, o lo dejas correr más? Si antes lo dejabas correr, ¿desde cuándo ya no? | a, b | En parte: «nunca… por ahora» (A-33, ADR-0073 §1) sin fecha |
| C3 | Una vez en break even, ¿el stop se queda quieto aunque el precio siga a favor con fuerza, o lo vas subiendo? (No hablamos de parciales.) | a | A-40 se cerró con una respuesta sobre parciales (SESION-03-EXTRACCION.md:470-475) |
| C4 | La zona que te hace mover el stop a break even, ¿se forma antes o después de que el precio rompa el punto? | d (RN-014) | Preguntado en la sesión 7b, sin respuesta citable (SESION-08-EXTRACCION.md:366-367) |

**Bloque D · Costes y precios.**

| # | Pregunta | Decisión | ¿Ya preguntado? |
|---|---|---|---|
| D1 | Los resultados de tus backtests en FX Replay, ¿llevan descontados el spread y la comisión, o no? | a (la premisa) | Dijo que no los tenía en cuenta (ev-v3-010111-b7c16b19), sin precisar si los resultados los llevan |
| D2 | En las horas en que operas, ¿qué spread y qué comisión ves en tu cuenta? | a, c | Lo mencionó sobre otra firma (ev-v4-000611-401b6978); nunca preguntado así |
| D3 | ¿Notas que te llenen las órdenes pendientes peor que el precio que pusiste? ¿Mucho? | c (F17) | Nunca |
| D4 | En FX Replay, ¿sabes si el precio que ves es el de compra, el de venta o el medio? | a, d (A-16) | Nunca (AUDITORIA-2026-09-13-ultracode.md:1920) |

**Bloque E · La cancha.**

| # | Pregunta | Decisión | ¿Ya preguntado? |
|---|---|---|---|
| E1 | ¿Operarías unos días en una cuenta de prueba de MetaTrader a la vez que corre el bot, para comparar día por día lo que hace cada uno? | c | Nunca |
| E2 | Si es así, ¿podrías apuntar también los días que miras y no operas? | c | Nunca |
| E3 | ¿Te parece bien que cada día que te enseñemos ya no lo podamos usar como prueba a ciegas? | c (R7.3) | Nunca |

**Lo que no se le pregunta**: ninguna cifra de VIABILIDAD-COMISION ni del techo ni de las parejas; ni
si «nuestro» resultado le parece bien. A1-A4, B1, C1 y D1 son las que más mueven el ADR de C.

## §7 · Las opciones para el ADR de C

El ADR lo escribe Aleks (ADR-0098 §3 C, :147-148; HOJA-DE-RUTA.md:437-443, R4.7). Aquí van cinco
opciones, sin elegir. Lo que **todas** comparten y puede empezar ya, sin esperar al ADR: las preguntas
del bloque A, B y D de §6 (no gastan material); abrir una prueba gratuita de FTMO, de la que hoy no consta ninguna viva
(DEMO-FTMO.md:162; R-09); la copia de seguridad de v18 a v21 (HOJA-DE-RUTA.md:743-746; PS:135); y
corregir tres textos de estado que ya no son verdad (R6.0 y RUMBO §4-§5 con la razón del tope de
peticiones, P6-07; la meta de marzo de 2027 en HOJA-DE-RUTA.md:7, R-02; la letra M, K-06).

| | O1 · Seguir el método | O2 · Medir primero | O3 · La cancha como objetivo | O4 · Medir 2025 ya | O5 · Pausar hasta tener la premisa |
|---|---|---|---|---|---|
| **Qué es** | Tras F17 y el contraste con el trader, volver a R4.6: sesiones de fidelidad con el método de ADR-0093 y el pivote tal como está | No grabar sesiones de fidelidad; hacer antes el puente pieza a pieza (§8), F17 rediseñado (§8) y las preguntas de §6; un segundo ADR decide con eso | Probar el bot sobre precios de FTMO grabados, días nuevos, corrigiendo solo por fidelidad (§8, vía i), como herramienta principal | Desatar R5.6 del 0,70/0,60 y medir la rentabilidad pre-registrada sobre junio a noviembre de 2025 (AUDITORIA-2026-11-21 §1, opción 2) | Parar las ramas de fidelidad y de medida hasta que el trader conteste A1-A4 de §6; seguir solo plataforma y deuda |
| **Qué necesita saber antes** | Que el trader opera en real lo mismo que en el backtest (B1) y que sus resultados ganan con costes (A1, D1); si no, se afina hacia un techo que no gana (M-15) | Nada más que el propio ADR: C pide F17 y la premisa, pero no pide el puente (D-01, P2-02); hay que escribirlo | Un ADR que reescriba la condición de entrada de R7.3 (P6-06) y otro de proveedor de datos (P6-02); qué meses (noviembre reservado; el 12 tapado por número, ADR-0092 §5, P6-10); las reglas para corregir sin ajustar, escritas antes (P6-24) | Un ADR que desate «habilita medir» (ADR-0092 §5, :154; M-03); datos de 2025, cierres hacia atrás y el comando, que no existen; F17, sin el cual la puerta no da «pasa» (ADR-0092 §4, :113; D-02) | Nada |
| **Coste en tiempo** | Una sesión con su extracción, activación y corrida por vuelta; sin regla de parada (M-12) y con trayectoria plana en la corrida que cuenta (M-01) | Puente: una o dos ramas sobre construcción (12 pasos, P1); F17: un guion que coloque órdenes y varias pruebas de 14 días (P4-05, P4-06) | De dos a seis pruebas gratuitas para N = 100 a ritmo de julio o de abril, unas ocho si se separan días de corregir y de medir (P6-13, aritmética); cuatro o cinco ramas de datos, motor, cierres y láminas (P6-01 a P6-04, P6-11, P6-18) | Las ramas de datos, cierres y comando; la medida, una semana (AUDITORIA-2026-11-21 §1) | Lo que tarde el trader |
| **Coste en material** | Días dev de construcción; ninguno reservado | Días dev de construcción (declarados en HOLDOUT-EXPOSICIONES por recuento); F17 no gasta material del repo | Días nuevos; cada día enseñado al trader queda gastado como material ciego (R7.3); octubre y noviembre de 2026 no sirven para comparar con él (P6-23) | **Irreversible**: junio a noviembre de 2025 de una vez, más extensión si N < 100 (ADR-0092 §5; D-02) | Ninguno |
| **Riesgo** | Gastar sesiones del trader acercando el bot a un techo que con nuestros costes no gana (M-15, MATIZ) | Que el R por pieza tiente a cambiar la spec por resultado (ADR-0092 §6 lo prohíbe; el diseño de §8 lo impide por escrito) | Ajuste al resultado si se corrige mirando el R del día (P6-24); mezclar series (P6-04); que la prueba gratuita no ejecute como la cuenta real (P4-08) | Quemar el holdout de rentabilidad para confirmar lo que el techo ya apunta; con el techo en «no gana» y la puerta atada por el percentil 5 (P7-06), «no pasa» es lo más probable | Perder el ritmo y la disponibilidad del trader; los ingenieros llegan hacia el 2026-12-03 sin una pregunta clara |
| **Qué aportaría la cancha** | Nada directo | F17 graba los precios que la cancha usaría después; el puente dice qué piezas del simulador habría que vigilar en ella | Es la cancha: decisiones del bot y del trader sobre los mismos precios, sin A-16 ni S-14 (P6, vías i y iii) | Nada | Nada |

### OPINIÓN DEL AUDITOR (separada; deciden el consultor y Aleks)

Si tuviera que recomendar, recomendaría **O2, con el bloque A de §6 enviado ya y F17 rediseñado como
primera rama en cuanto haya una prueba gratuita viva**, y no O4.

Por qué. La pregunta que decide el proyecto no es «¿afinamos más?» sino «¿es nuestro modelo su
estrategia?». La auditoría encuentra que la comisión no es lo que separa lo que se creía del techo
(P4-01, SOBREVIVE): el salto está en el R bruto, en tres piezas nuestras que nadie ha aislado (el
objetivo que ADR-0040 vio contradicho por el material, la geometría del break even y la entrada con
su serie), y E1 muestra que la salida C no es robusta justamente a esas tres. Medirlas cuesta días
dev de construcción, que no son holdout, y una o dos ramas. Preguntarle al trader si gana y si su
backtest lleva costes no cuesta nada. O1 gasta sesiones del trader sin saber si el destino paga; O3
es la mejor herramienta a medio plazo, pero hoy le faltan cuatro ramas y dos ADR, y lo que necesita
primero (el grabador de F17) es lo mismo que O2; O4 quema un material irrepetible para confirmar, con
toda probabilidad, un «no»; O5 deja sin usar dos cosas baratas y útiles.

Qué me haría cambiar de opinión. (1) Si el trader dice que saca dinero con esta estrategia y su
exportación real, con costes, va en positivo: el puente pasa a ser urgente y O3 se adelanta, porque
entonces el problema es nuestro modelo. (2) Si dice que en real no opera lo mismo, o que sus
backtests no llevan costes y no tiene historial real: O5, y el ADR de C debería decirlo así. (3) Si
el puente muestra que las tres piezas no mueven el bruto lo bastante (que con el objetivo a 3,00 y
sin el break even el techo sigue por debajo de 0): la salida C deja de depender de nuestro modelo y
gana peso O5.

## §8 · Los diseños de medida

### 8.1 · El puente de VIABILIDAD-COMISION al techo (P1, con P2, P3, P4 y S)

**Para qué.** Decir cuánto mueve la esperanza cada pieza que cambia entre la V2 publicada (+0,47 R, 67
operaciones de abril y agosto, VIABILIDAD-COMISION.md:112) y el techo (−0,239 R, 191 operaciones,
meta.txt:13), sin decidir nada con el R.

**Lo que hay que saber antes de abrir la rama** (preguntas para el consultor, de P1 y K):
- ¿El puente sale de V2 o de V1? En estructura el techo es V2 (stop en el 0,8, objetivo a 3 cajas),
  pero al leer el stop del libro como el 0,8 su stop y su unidad de R en puntos son los de V1 (P1-01,
  reformulado tras la pasada). Propuesta: las dos rutas, que tienen que llegar al mismo nodo en el paso 6.
- ¿El redondeo de la caja derivada (ROUND_UP) es intencionado? No es la inversa de la regla del bot
  cuando la distancia no es múltiplo de 4 (K-01/P1-03, comprobado con aritmética).
- V2 no corre sobre el main de hoy (P1-04, MATIZ): el paso 0 la reproduce en un clon desechable con
  el código de su fecha (la skill `comparar-con-main` hace esto).

**El orden, fijado antes en un yaml atado por su sha (como `META-TECHO-PAREJAS.yaml`), sobre las mismas
operaciones de abril y agosto, un interruptor por paso** (de P1, con dos pasos de diagnóstico añadidos
al final):

| Paso | Cambia | Imprime además de N y la esperanza | Control |
|---|---|---|---|
| 0 | V2 reproducida en un clon | — | 67, +0,47, [−0,13; +1,08], 10 fuera |
| 1 | V2 con el bróker de hoy, sin margen, tope 100 excluyendo | — | — |
| 2 | De excluir a limitar el lote | cuántas entran | — |
| 3 | De 100 a 50 lotes y el margen a 1:30 | — | Nulo en la esperanza (P1-05) |
| 4 | Cuenta por mes | — | Nulo en la esperanza |
| 5 | Desfase de −2 a 0 puntos | — | — |
| 6 | Geometría del techo (6a con la caja coherente, 6b con ROUND_UP) | — | Comisión por R a 0,8 veces |
| 7 | Entrada por orden stop por ticks | no colocables; llenados con hueco | — |
| 8 | RN-002 y fin de día | cierres por motivo | — |
| 9 | Break even RN-014 | **salidas en break even** (no publicadas hoy, P1-13) | — |
| 10-11 | +enero, +julio | — | Reproduce meta.txt: 191, −0,239, −0,450/−0,026, 79, 7, 7 |
| D1 | (diagnóstico) objetivo a 3,00 sobre entrada-stop | — | — |
| D2 | (diagnóstico) sin RN-014 | — | — |
| D3 | (diagnóstico) spread 1 y 2 puntos menor | — | — |

Y el orden inverso, registrado antes, para ver la interacción entre piezas sin elegir orden.

**Qué no imprime.** Ningún R por clase de setup, sesión o dirección: extender ADR-0098 §4 c (:182-186)
al puente es una decisión que el encargo debe decir. La esperanza acumulada por mes sí (el techo ya
imprime julio). Los recuentos de §9 de K (eventos del respaldo M1, si las 7 caen en horas sin ticks)
se añaden sin R.

**Material y declaración.** Velas y ticks de los días dev de los cuatro meses de construcción, por la
compuerta y con `casos_reservados`; el paso 0 lee las filas de los días dev de los libros de abril y
agosto. Fila en HOLDOUT-EXPOSICIONES el día de correr, con recuentos (ADR-0021 §4; ADR-0033).

**Lo que no puede decidir.** Ninguna rama de spec ni de motor se justifica con el R de un paso (ADR-0092
§6 y el recuadro de ADR-0098, :126-128): ni quitar el break even, ni cambiar el objetivo (A-56 sigue
siendo del trader), ni adoptar el −2 (A-16). Los pasos D1-D3 son diagnóstico y lo dicen. Si algún paso
fuera a sustituir al techo, eso pide un ADR que declare lo visto (ADR-0098:211-213).

**ADR.** Por la letra de ADR-0098 §5 el puente no necesita uno propio si no cambia el modelo, pero el
ADR de C tiene que autorizarlo (C no lo pide, D-01) y declararlo en «lo visto». Hace falta una entrada
`###` en R4 de la hoja de ruta (P1).

### 8.2 · La cancha (P6, vía i; con lo que necesitan las vías ii y iii)

**Para qué.** Ver al bot decidir día a día sobre precios de FTMO, sin la otra serie (A-16) ni el sesgo
del material (S-14), y comparar con lo que el trader hizo esos mismos días, sin ajustar al resultado.

**Las piezas, en el orden en que hacen falta** (P6-01 a P6-05, P6-11, P6-18, P6-21; P4-04 a P4-08):

| Rama | Qué hace | Bloqueo que quita | ADR |
|---|---|---|---|
| F17 rediseñado | Un grabador de ticks en MQL5 (hoy no existe: el EA solo llama a `AlConectar`, Botsito.mq5:93-96) y una parte en `tools/` que coloque órdenes stop con lotes del bot y registre nivel, tick que dispara, llenado y lotes; mediana y p90 por clase | No se puede medir deslizamiento con un grabador pasivo (P4-05); la referencia del deslizamiento (P4-04) | El encargo fija la referencia y que la prueba gratuita no es «en vivo» (P6-08, matiz: hoy se lee como DEMO por ADR-0082 D6) |
| Datos de un proveedor nuevo | Manifiesto de ticks y M1 con `proveedor` distinto de dukascopy, hora del servidor a UTC (A-28), prefijo propio | ticks.py:483-486 (P6-02); heredado 9 (P6-21) | Uno de proveedor de datos (MASTER_PLAN.md:292 lo preveía) |
| El día de cancha en el motor | Un constructor de `MercadoDia` que no pase por `cases/`; un filtro por proveedor en `_ticks_del_dia` | arnes.py:157 (P6-03); simulacion.py:166-180 (P6-04) | — |
| Los cierres | Leerlos del journal del EA (`SymbolInfoSessionTrade`) o renovar por semana | Calendario caducado (P6-11) | — |
| Las láminas | Admitir días de cancha | cli.py:2742-2755 (P6-18) | — |
| El ADR de la cancha | Reescribe la condición de entrada de R7.3; fija los meses; escribe las reglas de abajo | R7.3 depende de que julio cumpla el mínimo 2 (P6-06, MATIZ) | Sí |

**Las reglas para corregir sin ajustar** (P6-17, escritas antes de grabar el primer día): (1) dos
conjuntos de días, fijados por calendario y nunca por resultado: los de corregir (se enseñan, quedan
gastados y se declaran) y los de medir (nadie los mira de uno en uno; se leen una vez, agregados, con
la spec sellada por ADR-0096 §5); (2) cada corrección cita al trader (`ev-`, `fb-`) o un hecho de la
plataforma, nunca el R (ADR-0092 §6); (3) el R de los días de corregir es diagnóstico y las láminas van
sin resultados (RUMBO-2026-11.md:19); (4) solo reglas generales con un test que rompe (R4.6); (5) que
los días de medida hagan de puerta de rentabilidad pide enmendar ADR-0092 §5 (son días futuros: con la
spec congelada no se puede ajustar a ellos) y choca también con ADR-0098 §1, que limita sus medidas a días
dev de construcción; y el calendario de días se fija antes de ver ninguna cifra, como ADR-0078:56 y
ADR-0079:63 exigen para la lista de meses de construcción (matiz de la pasada adversaria sobre P6-17).

**El tamaño** (aritmética sobre recuentos publicados, P6-13): a 2,6 operaciones del trader por día dev
(198 en 76, RECORRIDA-CONSTRUCCION-3.md §0.3), N = 100 pide unos 39 días de mercado; con pruebas de 14
días naturales (unos 10 laborables) y una activa a la vez, unas cuatro pruebas seguidas, de dos (ritmo
de julio) a seis (ritmo de abril); unas ocho si se reserva la mitad de los días para medir.

**Lo que tiene que dar el trader** (P6-15; preguntas A4, E1-E3 de §6): exportaciones por día, sin el
resumen de la cuenta, con instante al segundo y huso, dirección, tipo y nivel de la orden, stop,
objetivo, lote, llenado, salida y motivo; los días que miró y no operó; y su acuerdo con que cada día
enseñado se gasta. La vía iii (releer el techo con sus operaciones reales) además lee su resultado
real: lectura nueva que pide un ADR con quién, qué y cuándo (ADR-0072; P6-16).

**El horario.** La ventana es de 07 a 15 en Madrid, de 06 a 14 las semanas de desajuste (ADR-0069);
en Lima, de 01:00 a 09:00 con Nueva York en invierno y de 00:00 a 08:00 en verano (aritmética de
husos, P6-19). El grabador y el motor sobre días cerrados corren solos; abrir cada prueba, poner el EA,
copiar los ficheros y las sesiones con el trader necesitan a Aleks.

**Lo que ya bloquea las próximas semanas.** Noviembre de 2026 está reservado (PROJECT_STATE.md:28): una
prueba abierta hoy graba días que sirven para el spread y el deslizamiento de F17, no para comparar con
el trader (P6-23). El mes 12 está tapado por número en cualquier año (ADR-0092 §5; en el código solo
actúa sobre la cuarentena del texto, P6-10). El calendario de cierres caducó a principios de octubre de 2026 (P6-11).

## §9 · Lo que no se pudo comprobar, lo refutado, lo que la guardia negó y las medidas que exigirían exponer material

### 9.1 · Refutado, con su motivo

| Qué | Motivo | Quién lo refutó |
|---|---|---|
| P1-07 tal como estaba («≈0,43 R en 77 operaciones» del techo) | Esa fila es la de la ANOTADA (VIABILIDAD-COMISION.md:115); el techo no publica su comisión. Entra reformulado (§3, P1) | Pasada adversaria, tanda 1 |
| P1-01 tal como estaba («el techo usa el stop, el lote y la unidad del R de V1») | En estructura el techo es V2: stop en el 0,8, lote al 0,8 (`lotaje_base` = `hasta_stop_fraccion`, parametros.yaml:1297-1303), objetivo a 3 cajas; solo en puntos coincide con V1, porque lee el stop del libro como el 0,8. Entra reformulado | Pasada adversaria, tanda 3 |
| R-16 («A-16 ya se midió: mediana 0, 92,4 %») | La medida dice que la entrada existió dentro de la M1, y el propio informe dice que no compara velas con velas (METODO-FIDELIDAD-RENTABILIDAD.md:888-893) | Yo, en el contraste (registro 01:00) |
| Mi borrador de §2: «combinación refutada por ADR-0040» | ADR-0040 está enmendado por ADR-0073 (:9-18): es la regla dicha por el trader, contradicha por el material (A-56) | Adversario general (D3) |
| Mi borrador de §2: «19 de 19 ventas en break even pierden en bruto» | 8 de 19 ventas y 13 de 31 compras pierden en bruto (cuenta-por-mes.txt:3129-3364) | Pasada adversaria sobre K-06 |
| P6 (en P6-06): «julio sigue en 10 parejas» | En el pivote vigente se lee la diaria: julio tiene 19 parejas; falla el mínimo 2 (40 > 33) | Pasada adversaria, tanda 1 |
| La pregunta C4 de §6 (break even en la entrada o con costes) | Ya contestada: A-40, sesión 3, exactamente en la entrada (strategy_spec.yaml:1832-1835) | Pasada adversaria sobre P4-09 |
| P5-03 («discrepancia 0,4 frente a 0,5 %») | SESION-01:39-40 dice que la tabla vieja ponía 0,4 y ADR-0020 lo invirtió | Yo (registro 00:02) |

### 9.2 · Pendiente de comprobar (no se pudo con lo permitido)

- Cuántos tests se saltan de verdad en la CI de Linux sin data/ (C4 de AUDITORIA-2026-11-21: «más de
  15»; I-07 cuenta 9 líneas): pide un `pytest -rs` sin data/, que 2.5 prohíbe.
- La cifra literal «0.1 o 0.2 a lo mucho» de ev-v4-000611-401b6978: la CLI la muestra truncada.
- «Sin orden en julio: 1 en la diaria» (M-06): no está en el informe; la pasada no lo pudo verificar.
- Que ninguna operación del techo caiga en horas sin ticks, y cuántas de las 7 no colocables caen en
  ellas (K-04, P3): no impreso por el guion (K-03).
- La distribución de la distancia al stop del techo, la mezcla de llenados afectados y cuántos break even
  cierran: no publicadas (P4, P1-13); sacarlas exige correr el techo.
- Si la prueba gratuita de FTMO ejecuta como la cuenta real (P4-08, S-11): pregunta a FTMO.
- Qué mes cubre el vídeo de mapeo (D-11): pregunta a Aleks.
- Si el historial real del trader, si lo comparte, se abre por la puerta de ADR-0033 (P5 lo propone): no
  es un libro de backtest; pregunta para el consultor antes de pedirlo.

### 9.3 · Lo que la guardia negó (ninguna negativa se rodeó; se usó la forma que la guardia indica)

| Quién | Comando negado | Regla | Qué se hizo |
|---|---|---|---|
| Orquestador | `for d in …; git ls-files "$d"` | ADR-0088 (nombres de holdout) y ruta no literal | Rutas literales |
| Orquestador | `join … <(…)` | Sustitución de proceso (guion-mismo-comando) | Leer los ficheros por separado |
| Orquestador | `PYTHONPATH=src python …` | Lista cerrada de nombres de entorno | Python del .venv sin la variable (el paquete está instalado; el encargo admite `uv run --no-sync`) |
| Subagentes (P1, P2, P3, P4, P5, M, S, X, I) | Bucles `for`, `while … sed`, `xargs sh`/`xargs cat`/`xargs wc`, `tac`, `$(…)`, `:` de relleno, una asignación `f=…`, un `subprocess` con `git ls-files` dinámico | Guion-mismo-comando y ADR-0088 | Llamadas sueltas con rutas literales |
| Subagentes (M, P3) | `kb at --video v15 --t 1:19:12` | Sesión en cuarentena | No reintentado; S-14 se citó por SESION-05-EXTRACCION y ACTIVAR-SESION-05 |
| Subagente (P2) | `kb find --video v10` | Sesión en cuarentena | Búsquedas sin `--video`, que la CLI filtra |
| Subagente (P1) | `git tag --contains` | Hook de solo lectura del agente | Sin sustituto |
| Subagente (P6) | Un comando que escribía y ejecutaba un guion de zoneinfo a la vez | Guion-mismo-comando | Aritmética a mano sobre desfases ya medidos |
| Subagente (I) | `uv run botsito --help` | La guardia no deja ejecutarlo como lectura | Se leyó cli.py |

### 9.4 · Medidas que exigirían exponer material (para una rama; nada de esto se hizo)

Todas leen solo días dev de los meses de construcción (enero, abril, julio y agosto de 2026), por la
compuerta y con `casos_reservados`, y se declaran en HOLDOUT-EXPOSICIONES el día de correr, por recuento
(ADR-0021 §4, ADR-0033). Ninguna decide una regla con el R (ADR-0092 §6).

| Medida | Qué leería | Qué imprimiría (sin R por clase) | Origen |
|---|---|---|---|
| El puente pieza a pieza (§8.1) | Velas y ticks de los días dev; en el paso 0, filas de días dev de los libros de abril y agosto | N, esperanza, recuentos y los dos intervalos por paso | P1, P2, S, P3 |
| El techo con el objetivo a 3,00, sin RN-014, con spread menor | Lo mismo | Lo mismo, marcado diagnóstico | P2 (M-P2-a), S (§3) |
| Las 7 no colocables, sin R | Casos dev, M1 y ticks | Mes, lado, distancia al colocar, si hubo tick, segundos desde el primer cruce, si caen en horas sin ticks; cuántas llenarían con la espera de ADR-0097 | P3, K |
| Eventos del respaldo M1 del techo (`por_fuente`) | Lo mismo | Recuentos por fuente | K-03 |
| Los 50 break even del bot: bid y ask frente a la entrada al mover el stop | Ticks de los días dev | Recuentos por lado | K-05, K-06 |
| Segunda pasada de descarga de las 18 horas sin ticks y línea base nueva | Ticks nuevos de construcción (datasets nuevos) | La línea base repetida | K-04 |
| El techo con los frenos de la firma (RN-032, RN-036) | Lo mismo | Si la cuenta del trader bloquearía en julio | M-06 |
| V2 con remuestreo por días y el techo solo sobre abril y agosto | Lo mismo | Los dos intervalos comparables | P7 |
| Modelo de llenado de FX Replay en fotogramas localizados de v7, v8, v11-v13 | Fotogramas de construcción, abiertos por instante localizado (ADR-0038) | Si llena al nivel y con qué lado | P3 (medida 2) |
| A-16 velas contra velas, con una exportación de velas de FX Replay de días de construcción | La exportación (vía Aleks) y la M1 de Dukascopy | Diferencias OHLC, velas de otro color, si los 79 break even caen del mismo lado | P3 (medida 3) |
| Recuento de filas a cero y de más de 3,75 en los libros de abril y agosto | Detalle por operación de días dev (permitido sin puerta, ADR-0021 §1) | Recuentos por mes | P2 (M-P2-b) |

## §10 · Registro de decisiones del flujo

| Hora | Decisión | Por qué |
|---|---|---|
| 23:30 | PARTE 1 pasada: status vacío, solo main, main = 8a10590b, tag^{commit} = main^1 = 88f678f7; foto `--ignored` en foto-ignored-inicio.txt (54 líneas) | Comprobaciones previas |
| 23:32 | Carpeta de trabajo creada en C:\Users\USER\Desktop\auditoria-profunda-trabajo\ (la guardia no la negó) | 1.2 |
| 23:35 | §0 fijado antes de leer las fuentes de los ejes | A1 |
| 23:35 | Tipo de subagente: `auditor-encargo` para todos (su Bash pasa por `solo_lectura.py`, más seguro que Explore, que tiene Bash sin ese hook). Se le dice que ignore los pasos 1-2 de su definición (buscar el encargo de rama) | 2.10 |
| 23:35 | Modelo: sonnet para los ejes de barrido documental (P2, P5, P7, S, R, X, D, I) y para las pasadas adversarias; opus (el de la definición) para los que exigen leer código y razonar (P1, P3, P4, P6, M, K) y para el revisor final (G1 lo pide opus) | Memoria del proyecto: el usuario pidió optimizar tokens (sonnet para verificar y redactar, opus para lo que decide) |
| 23:35 | Tandas de cuatro o cinco: T1 = P1, P4, P5, P7; T2 = P2, P3, P6, M; T3 = S, R, K, D, X; I al final, cuando exista §1 y parte de lo demás | B1; P1/P4/P5/P7 son el corazón de la pregunta central |
| 23:38 | La guardia negó dos comandos del mapa (`for d in ...; git ls-files "$d"`, por ruta no literal; `join ... <(...)`, por sustitución). No se rodeó: se repitieron con rutas literales, la forma que la propia guardia indica | 2.7 |
| 23:45 | T1 lanzada (P1 y P4 opus; P5 y P7 sonnet). T2 lanzada a la vez (P2 sonnet; P3, P6 y M opus), sin esperar a T1 | B1/B3: ganar tiempo; ocho a la vez no tocan el repo |
| 23:55 | Los ficheros de salida de los subagentes están vacíos (0 líneas): no se pueden extraer con guion; las entregas se copian a mano tal cual en entregas/<eje>.md. Los dos guiones auxiliares (extraer_entrega.py, estructura_jsonl.py) quedan en la carpeta de trabajo, sin uso | B2 |
| 23:56 | P7 recibida y DADA POR BUENA con dos reservas: (1) P7-04 calcula la media del techo fuera de julio (cifra retirada del informe): es aritmética sobre cifras publicadas, pero equivale a un R de un subconjunto nunca publicado; en el informe se dirá sin la cifra (julio y el total casi coinciden), y la cota de enero solo como contrafactual; (2) su «Días de junio a noviembre de 2025» es un recuento de días laborables, sin fechas: entra | 2.3 |
| 23:58 | P5 recibida y DADA POR BUENA con dos correcciones: «con el 5 % de deslizamiento» de P5-05 es un error de redacción (el equilibrio es −2,52 puntos, meta.txt:18); su «medida para una rama» dice que el historial real se abriría por la puerta de ADR-0033, lo que no está claro (el historial real no es un libro de backtest): pasa a pregunta para el consultor. Abre dos comprobaciones mías: 0,4 frente a 0,5 % (SESION-01:40 frente a parametros.yaml:1279) y que la cuenta fondeada del trader sea FundedNext (ADR-0022) | C2/C3 |
| 00:02 | Comprobado por mí: SESION-01-2026-09-09.md:39-40 dice que la tabla vieja ponía «riesgo real 0,4 %» y ADR-0020 lo invirtió: no hay discrepancia viva 0,4/0,5 (P5-03 → MATIZ). FundedNext es la firma que el proyecto eligió antes para el BOT (ADR-0026:12 «Se descarta FundedNext»), no consta como la del trader: la nota de P5 pasa a pregunta para el trader («¿en qué firma están tus cuentas de fondeo?») | C3 |
| 00:03 | T3 lanzada (S, R, D, X sonnet; K opus). Once subagentes vivos a la vez | B1 |
| 00:10 | P4 recibida y DADA POR BUENA. Comprobado por mí: cableado.py:1349-1352 (comisión 2,50×lotes×2; riesgo = lotes×|entrada−stop|), techo_parejas.py:538-541 (toda entrada es stop), ADR-0057 §1 (la stop nunca se llena mejor que el nivel), DEMO-EJECUCIONES-2-3.md:41 (buy stop +1, 0, 0). Ejecutada su llamada sintética (sintetico_equilibrio.py): las cinco salidas coinciden con lo esperado; la pendiente de meta.txt es 0,13452 | C3 |
| 00:11 | La guardia negó `PYTHONPATH=src` delante del python (lista cerrada de NOMBRES_DE_ENTORNO). Sin la variable, el paquete se importa desde el .venv (instalación editable): es la forma que la guardia indica y que el encargo admite («o uv run --no-sync»). Apuntado para §9 | 2.7 |
| 00:12 | P4-01 (comisión ≈ toda la distancia), P4-02 (F17 no puede dar la vuelta a C por el deslizamiento) y P4-14 (¿lleva comisión su cifra?) van a la pasada adversaria; P4-05 (F17 definido como grabador pasivo) también, porque sostiene una opción de §7 | D1 |
| 00:20-00:55 | Recibidas y guardadas D, R, M, P2, P6, P1, X, S, P3, I. Todas DADAS POR BUENAS salvo lo que sigue | B2 |
| 00:40 | El usuario pidió «mete workflow donde veas necesario»: lo uso en la fase D (muchas verificaciones pequeñas e independientes). La memoria del proyecto dice que en esta máquina el Workflow no llegó a terminar agentes (vigilante de 3 min): si falla, vuelvo a Agent | Mensaje del usuario |
| 00:58 | Tras T1-T3 e I: `git status --short` 0, `git diff --stat` 0, `--ignored` IDÉNTICO a la foto de partida (diff vacío) | 2.9 |
| 01:00 | C2 · Contradicción A-16: R-16 dice «ya se midió (mediana 0, 92,4 %)»; P3-01/P3-15 dicen que no a escala de R. Leído METODO-FIDELIDAD-RENTABILIDAD.md:881-893: la medida dice que la entrada EXISTIÓ dentro de la M1 y que «no compara velas con velas… estar dentro no quiere decir que las dos series marquen el mismo precio». R-16 REFUTADO; gana P3 | C2 |
| 01:00 | C2 · Spread de Dukascopy: S-02 dice «4 puntos de mediana» (F35:212), P4 «media 2,7-3,5, p50 3» (TICKS-SPREAD-SALIDA.txt). Leídos los dos: F35:212 es el spread en los instantes de llenado y cierre de 15 operaciones; TICKS-SPREAD es el de todos los ticks por hora. Los dos ciertos; poblaciones distintas. En el informe se dan los dos con su población | C2 |
| 01:02 | C3 comprobado por mí: RC3:474-480 (cascada 70/73/37/0/3/1/14 de 198), HOJA:903-911 (Marcador), ADR-0092:68 («condición NECESARIA de todo lo que decida operaciones en vivo») y :154 («la construcción en el umbral de ADR-0070»), MASTER_PLAN:127 (F17 = «Grabar ticks y spread de la demo» → «perfil de spread»), DEMO-FTMO.md:162 (prueba del 28/10 al 11/11), ADR-0040:22-35 (la combinación caja_completa+0,8 contradicha por el material, 26 de 38; a las 01:52 el adversario general recordó que ADR-0073 enmendó «refutada»), `grep -c A-56 ADR-0098` = 0, ADR-0098:144-155 (la relectura del techo solo está escrita en D) | C3 |
| 01:03 | P7-04 y P1 (fila 1) calculan la media del techo fuera de julio: en el informe va sin la cifra («julio −0,245 y el total −0,239 casi coinciden»), por 2.3 | 2.3 |
| 01:05 | K recibida y DADA POR BUENA. K-01/P1-03 comprobados por mí con aritmética pura (sintetico_caja.py, sin importar el anexo: 2.5 prohíbe ejecutar techo_parejas.py): con d no múltiplo de 4 la caja derivada da un stop implícito d+1 (24 de 33 valores entre 8 y 40). K-06 sube de MENOR a CAMBIA EL PLAN: contradice una letra viva de la Next Action (M) y es el mecanismo de P4-09 | C3 |
| 01:10 | Fase D lanzada como Workflow (wf_9dffc0bb-22c): 22 hallazgos C/PLAN, un adversario `auditor-encargo` sonnet por hallazgo, con la PARTE 2 literal y la plantilla adversaria | D1 |
| 01:15 | D3: borrador de §2 escrito y adversario general lanzado (auditor-encargo, opus por defecto) | D3 |
| 01:16 | FASE E: abro UN eje propio, E1 «La robustez de la salida C pieza a pieza»: qué piezas podrían, solas o juntas, mover el techo de «no gana», con los recuentos y cotas ya publicados; lo hago yo desde las entregas, sin subagente. Justificación: decide si el ADR de C se puede tomar hoy o debe esperar a una medida (alimenta a, d). No abro E2/E3: la calidad de Dukascopy frente a FTMO y el calendario ya los cubren P3-14, P4-03 y P6-11; un supuesto del simulador de cuenta que sesgue el techo lo cubren S y K | E1 |
| 01:30 | D1 terminada: el Workflow completó 22 de 22 agentes (sin errores), en contra de lo que decía la memoria. Resultado en entregas/D1-pasada-adversaria.json. SOBREVIVEN: P4-01, P4-02, P5-01, D-01. MATIZ: P3-07, S-01, P2-02, S-02b, M-01, M-04, M-03, P6-06, P6-08, P4-05, P3-01, P6-07, X-03, M-15, P2-05, K-06, K-04. REFUTADO: P1-07 | D1/D2 |
| 01:32 | D2 · P1-07 REFUTADO tal como estaba: «≈0,43 R en 77 operaciones» es la fila de la ANOTADA (VIABILIDAD-COMISION.md:115), no del techo, que no publica su comisión. Entra reformulado y como aritmética: V2 (0,42) y la anotada (0,43), que usa la misma unidad que el techo (el stop del libro), pagan casi lo mismo por R en abril y agosto; la cota del techo sale de P4-01 | D2 |
| 01:32 | D2 · K-06: 8 de las 19 ventas en BE pierden en bruto (11 a cero) y 13 de las 31 compras también; corrijo §2 («19 de 19» era falso) y K-06 queda en PLAN con el matiz: el BE no sale gratis en ningún lado, la asimetría por ASK no está demostrada | D2 |
| 01:32 | D2 · P6-06: el bloqueo de R7.3 se sostiene, pero viene del mínimo 2 (40 operaciones de más > 33 en la diaria), no del 1 (julio tiene 19 parejas en la diaria; las 10 eran de la corrida 1) | D2 |
| 01:33 | D2 · otros matices que entran: M-15 (c) es el percentil 5, no el 95; falla también e)); P6-08 (la prueba gratuita es DEMO por la lectura de ADR-0082 D6, así que la vía (ii) la cierran §4 y R6.1, no ADR-0092 §3); X-03 (unos 190 commits sin merge desde el 2026-11-09, no 169; 70-76 h es un techo); P3-07 (dirección razonada, no medida); S-01 (el techo sigue la spec vigente por ADR-0073; «refutada» es contradicción con el material; ADR-0098 no nombra A-56); P2-02 (B descompone la diferencia emparejada, no el techo); P2-05 baja a MENOR (con stop 0,8 son 3,32-4,27 cajas; VIABILIDAD-TRADER cuenta cinco); K-04 (684 horas y 2,63 % son derivación mía de 76×9, marcada) | D2 |
| 01:40 | La regla de D1 pide pasada adversaria para TODOS los de gravedad C: la primera tanda no los cubría. Segunda tanda lanzada con el mismo guion (wf_a7442c26-e9f): 14 de gravedad C que faltaban y 15 PLAN que sostienen opciones de §7. Los C duplicados de otro ya probado heredan su veredicto (R-06 y M-10 de P4-02; M-09 y R-07 de P3-07; S-04, P1-08 y P3-02 de P4-01; P2-06 de S-01; R-05 de M-01; R-20 de M-03). Regradúo: P5-05 a MENOR (repite cifras de meta.txt); D-06 y P6-17 a CAMBIA EL PLAN (vocabulario y propuesta, no hechos que cambien C) | D1/C4 |
| 01:50 | Segunda tanda: 29 de 29, sin errores. SOBREVIVEN M-08, M-14, P1-04, P3-09; MATIZ el resto; ningún REFUTADO. Matices que entran: P4-09 (A-40 RESUELTA: BE exactamente en la entrada, sin puntos para costes; quito la pregunta C4 de §6); P7-05 (la distancia del p95 al umbral es 0,126, no 0,026: baja a MENOR); P7-04 (la cota la doy con julio aparte, como P7); M-05 (el adversario dice que A-48 es el stop: lo descarto, PS:68 y ADR-0098:34-35 ponen la orden stop en el 0, que es la entrada; queda «no medido»); S-02 (F35 §5.4: con el precio medio saltan los mismos 33 stops); S-03 (comisión medida dos veces con 1,00 lote y el soporte dijo 50/50: «5 por lado» contradicho en la prueba gratuita); P6-11 (renovar los cierres es por condición, no cada semana); P4-06, P4-08, R-09, D-03 (citas o generalizaciones ajustadas) | D2 |
| 01:52 | D3 · Adversario general (dirección a): ADR-0040 está ENMENDADO por ADR-0073 (:9-18): «refutada» pasa a «la regla dicha por el trader, contradicha por el material» (A-56). El objetivo, el break even (salvo su geometría) y la entrada por stop son reglas dictadas por el trader. Comprobado por mí en ADR-0040:9-18 y ADR-0073:13-60. ACEPTO la corrección de redacción: lo nuestro es la geometría de la zona posterior, no corregir la serie y el modelo de colocación y llenado; la duda pasa a ser si su REGISTRO de FX Replay es su estrategia. Mantengo que la comisión no separa lo que se creía del techo y que tres piezas no están aisladas | D3 |
| 02:05 | Informe montado con montar_informe.py: 209 hallazgos (33 C, 96 PLAN, 80 MENOR); todos los C con estado. Tercera tanda adversaria (wf_799256c2-271) sobre los 18 PLAN que cito en §2, §7 y §8 y aún no tenían pasada; los demás PLAN (estado documental, proceso, ingenieros) no sostienen ninguna opción de §7 y quedan SIN PASADA, dicho en §12 | D1 |
| 02:06 | G1 lanzado: revisor final `auditor-encargo` (opus) sobre borrador.md, sin haber visto el trabajo: 15 hallazgos C/PLAN al azar, todas las cifras de §2 y §7, fechas reservadas y R nuevos | G1 |
| 02:20 | Tercera tanda: 18 de 18. SOBREVIVEN P6-01, P7-01, R-02, S-05; MATIZ 13; REFUTADO P1-01 («usa el stop, el lote y la unidad de R de V1»): en estructura el techo es V2 (stop en el 0,8, lote al 0,8, objetivo 3 cajas, parametros.yaml:1297-1303); en puntos coincide con V1 porque lee el stop del libro como el 0,8. Reformulado en §3 y §8. Matices que entran: P6-05 (el repo se contradice: ADR-0090 §7 dice que el grabador medirá el deslizamiento); P6-04 (hoy la mezcla es imposible porque el validador solo admite dukascopy; el filtro hace falta al añadir un proveedor); P6-17 (las reglas chocan también con ADR-0098 §1 y piden fijar el calendario antes, ADR-0078:56, ADR-0079:63); P1-13 (la ganadora media es +3,47 y el break even cierra entre −0,10 y −0,63 R) | D2 |

## §11 · Los insumos para la página de los ingenieros

Borrador de índice (del eje I, contrastado; la entrega completa está en la carpeta de trabajo,
entregas/I.md). Cada sección, con qué decir y dónde enlazar.

| # | Sección | Qué decir | Enlaces |
|---|---|---|---|
| 1 | Qué es y qué no es | Bot de EURUSD (H4 → M15 → M1) que replica a un trader, sin IA en ejecución. Hoy no opera: la capa de MT5 conecta, lee reloj y sesiones y escribe su journal, solo en demo. La meta de ADR-0098 dio salida C (el techo no gana con nuestros costes) y no se graba ninguna sesión de fidelidad hasta el ADR de Aleks | README.md; mql5/README.md; ADR-0082 §1 y D6; ADR-0098 §3 C; HOJA-DE-RUTA.md:437-443 |
| 2 | Los papeles | Aleks decide y cierra; el consultor es Claude en el chat; la sesión es Claude Code (ADR-0072). Los ingenieros revisan y Aleks decide; reabrir algo pide un ADR nuevo | ADR-0072 §1 |
| 3 | El mapa | §1 de esta auditoría. Cifras de hoy: 96 ADR (0001-0098 sin 0087 ni 0095), 2137 funciones de test (PROJECT_STATE.md:19), unas 40.800 líneas en src y 56.000 en tests (recuento del eje I) | §1; docs/adr/README.md |
| 4 | Lo que no se puede romper, cada cosa con su ADR | El holdout (ADR-0021 §1-§4, ADR-0033, ADR-0037 §1 y §3, ADR-0072 §2, ADR-0088); los regímenes de cambio (ADR-0001); el trailer `Fuente:`; el registro de parámetros (ADR-0002); las capas (ADR-0006); las guardias de .claude/ no se rodean; make check a un fichero, el sello y nunca `--no-verify`; main solo con orden de Aleks. CLAUDE.md comprime ADR-0037 §3 (lo visto por accidente es exposición que se declara; I-11) | ADR citados; CLAUDE.md; Makefile:82 |
| 5 | Las decisiones abiertas para ellos | (i) La arquitectura en vivo: ADR-0082 §4 y su recuadro del 2026-11-22 (cae la razón del tope de peticiones; quedan otras); R6.0 y RUMBO aún citan la razón retirada (P6-07). (ii) Los tres meses fijos de F34; marzo de 2027 no cabe (ADR-0098 §6). (iii) La paridad Python-MQL5 (R6.1). (iv) La cancha y F17 (§8.2), con lo que la prueba gratuita puede y no puede medir (P4-05, P4-08) | ADR-0082:71-114; ADR-0098:220-231; HOJA-DE-RUTA.md:635-652 |
| 6 | Qué podría acelerar | Reordenar `check:` para que los pasos de segundos vayan antes del de 27 minutos sin romper el sello (X-08); remedir xdist (1.084 → 410-504 s, pico 243 → 1.118-1.161 MiB, ENTORNO-CODE.md:150-180; X-05); separar los tests que leen data/ (X-06); sacar de guardia.py lo que no es del holdout (X-09). No quitar ninguna barrera del holdout. Librerías ICT/SMC solo para contrastar detectores; la tasa de descarte del trader por tipo de setup no tiene referencia en el repo y pide material declarado (I-09) | X; ENTORNO-CODE.md |
| 7 | Cómo arrancar | `make sync`; `make check > make-check.log 2>&1`; `make rapido`; `uv run botsito --help`; el arnés necesita data/ | Makefile:12-17, :45, :82 |
| 8 | Lo que la máquina de Aleks tiene y la suya no | data/, corpus/, la carpeta del trader, MetaEditor en Windows. Sin data/, varios tests se saltan y la CI de Linux no los corre; la CI no se dispara en ramas `trabajo/*` (I-07) | ci.yml; tests citados en I-07 |
| 9 | Lo que el porte a MQL5 tiene que reproducir | La tabla de estados de MT5 de K: modificar el SL del lado malo (10016), llenados parciales, expiración, cancelar contra llenar, latencia, stops level en vivo | §4, K |
| 10 | Qué leer después | PROJECT_STATE.md, CLAUDE.md, HOJA-DE-RUTA.md, runbooks, ERRORES-RECURRENTES.md | docs/runbooks/README.md |

Lo que hay que corregir antes de dárselo (eje I): el Anexo B de AUDITORIA-2026-11-21 tiene cifras viejas
y describe un ciclo hoy parado (I-01, I-02); «la cancha» no es todavía un término del repo (I-05); el
README de la raíz y mql5/README.md están desfasados (I-10).

## §12 · La tabla completa de hallazgos, ordenada por gravedad

208 hallazgos: 33 que cambian la decisión de C, 96 que cambian el plan y 79 menores. Las gravedades son las de cada eje salvo seis que regradué (registro 01:05 y 01:40). «SIN PASADA» en un PLAN quiere decir que no sostiene una opción de §7 (FASE D1); los PLAN que la sostienen pasaron por la segunda tanda.

| Id | Eje | Hallazgo | Clase | Gravedad | Evidencia | Alimenta | Lo refutaría | Estado tras la pasada adversaria |
|---|---|---|---|---|---|---|---|---|
| P2-01 | P2 | La diferencia +0,56 → −0,239 **no se explica por la regla de salida simulada**: la serie «V2» (stop 0,8, objetivo fijo 3 D, cierre forzoso, **sin BE**) da +0,47 en 67 operaciones frente a +0,56 de la anotada en 77, es decir 0,09 R. Lo que el techo añade es el BE (movido en 79 de 191), cuatro meses en vez de dos y el lote limitado. Esa diferencia sigue sin descomponerse. Aritmética sobre cifras publicadas | HECHO (cifras) + PREGUNTA PENDIENTE (los ingenieros / rama de diagnóstico) | CAMBIA LA DECISIÓN DE C | `VIABILIDAD-COMISION.md:112,115`; `meta.txt` (191 llenadas, BE movido 79, RN-002 en 7, esperanza −0,239); ADR-0098 §1 «Gestión» | a, b, f | Que el techo con RN-014 apagado sobre las mismas 191 siga en torno a −0,24, o que V2 sobre las 191 dé también negativo. Ninguna de las dos cuentas está hecha. Reservas: no es el mismo conjunto (Dukascopy, abril y agosto, 10 operaciones de V2 fuera por el tope de lote) | MATIZ (matiz en §3/§9) |
| P2-02 | P2 | ADR-0098 §3 salida C lista como revisión los costes (F17), el sesgo S-14, A-16 y contrastar con el trader. **No incluye** descomponer el techo por pieza (break even, cierre forzoso, objetivo); esa descomposición está solo en la salida B. Y la única ablación de RN-014 existente mide **fidelidad de decisiones** (parejas 31→28), no R | HECHO | CAMBIA LA DECISIÓN DE C | `0098-…md:139-148`; `anexos/TRAZAS-ABLACION/ablacion.DIAGNOSTICO.vigentes.txt:1486` («sin RN-014: parejas 31 -> 28…») | a, d | Que otro informe o anexo mida el R sin RN-014 | MATIZ (matiz en §3/§9) |
| P2-06 | P2 | La base del objetivo: la pantalla de v5 (0:04:52) enseña al trader arrastrando el TP hasta que la herramienta marca R/R 3 sobre entrada-stop (3,00 R); su frase dice 0 a 1, que con stop en 0,8 da 3,75 R. 26 de 38 ganadoras están en [3,00; 3,75). El techo usa `caja_completa` (3,75 R). **No hay sensibilidad con 3,00 R**: A-56 se dejó como medición para F26 y ADR-0096 la quitó de la puntuación | SUPUESTO ELEGIDO (ADR-0073: gana el testimonio) | CAMBIA LA DECISIÓN DE C | `ADR-0037` corrección; `ADR-0040:22-35`; `ADR-0098 §1`; `parametros.yaml:1759-1785` | a, b | Un material que traiga la caja, o la respuesta del trader sobre cómo coloca el TP en la herramienta | MATIZ (hereda de S-01, que dice lo mismo) |
| P4-01 | P4 | La comisión, impuesta y medida, cuesta entre 0,336 y 0,673 R por operación del techo. Sin ella, el techo estaría entre +0,097 y +0,434 R: la comisión sola es más o menos toda la distancia entre −0,239 y +0,10 | HECHO (la cota es aritmética sobre cifras publicadas) | CAMBIA LA DECISIÓN DE C | meta.txt:13,18; criterio_fidelidad.py:824-839,869-882; cableado.py:1349-1352,1366-1369; techo_parejas.py:20,539; ADR-0090:102-110 | a, e | Una posición del techo con entrada que no sea stop, o una comisión que no se cargue dos veces (`comision_por_lado` false) | SOBREVIVE |
| P4-14 | P4 | Si los resultados que el trader dice ganar (FX Replay) llevan comisión y con qué spread, no está en el repo. Con la comisión sola en 0,34-0,67 R, es parte de la premisa | PREGUNTA PENDIENTE (Aleks con el trader) | CAMBIA LA DECISIÓN DE C | ADR-0098:144-148, :174-177 (§4 a: «backtest manual en FX Replay», A-16); no aparece en ningún informe (git grep de «fx replay» con «comisi», vacío) | b, a | Que el trader confirme que sus cifras ya llevan una comisión equivalente | MATIZ (matiz en §3/§9) |
| P5-01 | P5 | Ninguna fuente commiteada dice que el trader retire dinero, tenga cuentas fondeadas con importe, o gane en real. «La premisa» no tiene fuente en el repo. | PREGUNTA PENDIENTE (dueño: Aleks, con el trader) | CAMBIA LA DECISIÓN DE C | Grep sin coincidencias de retiro/payout/«dice que gana»/«vive del» en HISTORIA (`grep -c` = 0). En `docs/plan/RUMBO-2026-11.md`, `docs/validation/AUDITORIA-2026-11-21.md` y `docs/validation/SESION-0[1-8]-EXTRACCION.md`, «retira» solo aparece como retirar una orden o una cita. `kb find "retiro"`, `"fondeada"` y `"payout"`: «0 resultados». `kb find "cuenta real"`: dos ítems de v18 sobre liquidez, no sobre cuentas. Límite: `kb` ocultó 12.337 segmentos (12.104 por cuarentena) y 6 ítems; ahí puede haber algo que no veo. | a, b | Una cita de Aleks o del trader en una fuente leída por el consultor, o en lo oculto por cuarentena, y registrada | SOBREVIVE |
| P5-04 | P5 | Tres tipos de material, con distinto valor como prueba. (1) Backtest en FX Replay con vídeo: solo julio de 2026 (provisional). (2) Backtest sin vídeo: libros de enero, abril y agosto de 2026; el trader «se saltaba las sesiones que acababan en break even» y su serie de precios no es la nuestra. (3) Cuenta real: sin material ninguno. | HECHO | CAMBIA LA DECISIÓN DE C | `docs/adr/0098-la-meta-se-mide-en-la-corrida-3.md:173-177`. `docs/validation/RECORRIDA-CONSTRUCCION-3.md:504` («libros sin video: 2026-01, 2026-04, 2026-08, salvo 2026-04-29; cuentan como CON video, provisionales: 2026-07») y `:695` («el único mes con video, provisional»). Las citas de S-14 son `ev-v15-011912-0ae32588` y `ev-v16-003421-b824b770`. | a, c | — | MATIZ (matiz en §3/§9) |
| P6-06 | P6 | La cancha está bloqueada sin fecha. R7.3 depende de que julio cumpla los dos mínimos del pivote. La salida C manda sobre el pivote y no deja grabar sesiones hasta su ADR. Sin sesiones, julio sigue en 10 parejas (< 19). F17 no queda bloqueado: C lo pide. | HECHO | CAMBIA LA DECISIÓN DE C | HOJA:681, :435, :439-440; ADR-0098:144-148, :160-161, :192-195 | a, f | Que el ADR de C reescriba la condición de entrada de R7.3 | MATIZ (matiz en §3/§9) |
| P6-08 | P6 | A la vía (ii) no la frena solo ADR-0082 §4. También ADR-0082 D2 (sustituido por ADR-0092 §3: «la rentabilidad es condición NECESARIA de todo lo que decida operaciones en vivo») y R6.1. ADR-0082 D6 deja la capa en DEMO hasta F35. Ningún ADR define si «en vivo» incluye la prueba gratuita. | HECHO; la lectura de «en vivo» es PREGUNTA PENDIENTE (Aleks) | CAMBIA LA DECISIÓN DE C | ADR-0082:28-33, :136-138; ADR-0092:68; HOJA:648-650; MASTER_PLAN.md:20-25 | a, e | Un ADR que defina «en vivo» como dinero real | MATIZ (matiz en §3/§9) |
| P6-15 | P6 | Lo que tiene que dar el trader (sección aparte). Cada exportación nueva necesita su entrada en `libros.yaml`, con el huso medido por velas; medirlo contra el M1 de FTMO ya es una medida de A-16. | PREGUNTA PENDIENTE (el trader) | CAMBIA LA DECISIÓN DE C | RUMBO:19; ADR-0098:173-177; ADR-0069:17-21, :41; libros.yaml:1-13; CLAUDE.md punto 3 | b | — | MATIZ (matiz en §3/§9) |
| P6-24 | P6 | Riesgo de ajuste al resultado. «Ver día a día y corregir» es justo lo que ADR-0092 §6 prohíbe si el R del día está a la vista. Las láminas ya van «sin resultados». En vivo el trader no puede saltarse días, así que el sesgo S-14 desaparece y el ritmo puede subir (supuesto). | SUPUESTO ELEGIDO / riesgo | CAMBIA LA DECISIÓN DE C | RUMBO:19; ADR-0092:174-179; ADR-0098:173-177 | a, b | — | MATIZ (matiz en §3/§9) |
| P7-04 | P7 | Consistencia interna del techo: julio (−0,245) y el total (−0,239) casi coinciden (la media del resto se retiró por la regla 2.3). Para que abril+agosto del techo valiera +0,47 haría falta enero ≈ −1,2 R/operación. Eso apoya que el techo ya es la medida y que +0,47 no es una estimación del mismo objeto. | HECHO (aritmética sobre cifras publicadas) | CAMBIA LA DECISIÓN DE C | `meta.txt` líneas a-c y julio; `RECORRIDA-CONSTRUCCION-3.md:130-136` (35+42+54 de abril, agosto y enero) | a) | El techo de abril+agosto por separado, que no está publicado | MATIZ (matiz en §3/§9) |
| E1-01 | E1 | La salida C es robusta al deslizamiento, a S-14, a las 7 no colocables, a la mezcla de meses y al lote; no lo es (sin signo conocido) al objetivo, a la geometría del break even y a la serie y el llenado de FX Replay, que ADR-0098 §3 C no manda revisar | HECHO (cada fila con su fuente) + aritmética sobre cifras publicadas | CAMBIA LA DECISIÓN DE C | meta.txt:9-18; ADR-0098:103-110, :144-148; ADR-0057 §1; ADR-0040:22-35; ADR-0061 §4; METODO-FIDELIDAD-RENTABILIDAD.md:888-893 | a, d | Una medida del techo con una de esas tres piezas cambiada que dé el mismo «no gana» por las cuatro vías | Hereda: P4-02 SOBREVIVE; P3-07, S-01, P4-03 y P3-01 MATIZ |
| S-01 | S | **El techo y el bot fijan un objetivo (3×(0→1) con el stop en 0,8 = 3,75 sobre entrada-stop) que el material del trader no sostiene, y ADR-0098 no lo declara entre los supuestos del techo.** §4a enumera S-14, A-16 y F17, pero no A-56. La salida C tampoco. Bajo los dos supervivientes de ADR-0040, el objetivo real sería 3,00 sobre entrada-stop, un 25 % más cerca | SUPUESTO ELEGIDO presentado como el del trader; A-56 PENDIENTE sin dueño de rama | CAMBIA LA DECISIÓN DE C | `ambiguedades.yaml:1927-1962`; `0040:22-55`; `parametros.yaml:1782` y `:662-676`; `RECORRIDA-CONSTRUCCION-3.md:228`; `grep -n "A-56\|3,75" 0098` sin resultados | a, b, c, f | Un diagnóstico que repita las 191 con objetivo a 3,00, o que el trader diga dónde pone el stop en su caja. Sin signo: el objetivo más cerca sube el acierto y baja el pago | MATIZ (matiz en §3/§9) |
| S-02 | S | **El spread del techo es el de Dukascopy y se presenta como el del mundo.** El repo no tiene el spread de FTMO. El trader dijo que en FundedNext es «0.1 o 0.2 a lo mucho» y que «no influye mucho», y que no tomó en cuenta spread y comisiones. Dukascopy da 4 puntos de mediana frente a stops de 12-15 puntos | SUPUESTO ELEGIDO presentado como impuesto; PREGUNTA PENDIENTE (F17; Aleks) | CAMBIA LA DECISIÓN DE C | `ev-v4-000611-401b6978`, `ev-v4-000757-bdb9579b`, `ev-v3-010111-b7c16b19`; `F35-ORDEN-STOP-PIVOTE.md:212`; `VIABILIDAD-COMISION.md:135`. Aritmética: con spread real de 1-2 puntos y coste lineal, el techo subiría unos 0,10-0,15 R | a, b, c | La medida de F17 en FTMO | MATIZ (matiz en §3/§9) |
| S-03 | S | **La comisión de 2,50 por lado es la pieza que más pesa y su lectura «5 = ida y vuelta» no está confirmada por FTMO.** Medida en la prueba gratuita con 1,00 lote. 5 USD de ida y vuelta equivalen a 0,33-0,42 R por operación | SUPUESTO IMPUESTO con fuente parcial; lectura PENDIENTE (Aleks con FTMO) | CAMBIA LA DECISIÓN DE C | `cuentas yaml:382-400`; `0090:122-128`; `FTMO-REGLAS.md:59`, `:328`; `VIABILIDAD-COMISION.md:111-115`, `:136`. Aritmética: de 5 a 3 USD, +0,14 a +0,17 R; sin comisión, +0,35 a +0,43 | a, b, c | Respuesta de FTMO al asterisco; medir en cuenta real | MATIZ (matiz en §3/§9) |
| S-04 | S | **El signo del techo lo decide el coste.** Con los costes publicados (0,55-0,67 R/op), el techo antes de costes sería de +0,3 a +0,4 R | HECHO (aritmética sobre cifras publicadas) + premisa | CAMBIA LA DECISIÓN DE C | `meta.txt:13`; `VIABILIDAD-COMISION.md:111-115`, `:134-137`. Mezcla muestras: orden de magnitud | a, b | Un diagnóstico del techo con costes cero, declarado | SOBREVIVE (hereda de P4-01, que dice lo mismo) |
| R-05 | R | La trayectoria optimista de la AUDITORIA («+5 puntos por vuelta», :55-56) no se observó: de la corrida 2 a la (3), con la 7a y la 7b activadas, 15,7→15,2 y 13,9→14,4 | HECHO (cifras publicadas) | CAMBIA LA DECISIÓN DE C | HOJA:910-911; RECORRIDA-3 §1 (:455, :463) | a | Una medida de la trayectoria con otra base | MATIZ (hereda de M-01, que dice lo mismo) |
| R-06 | R | El techo no gana ni con deslizamiento: la meta dice que haría falta −2,52 puntos por llenado afectado (mejora de precio) para llegar a +0,10 R. F17 solo mide el coste real; solo cambiaría C si midiera una mejora ≥ 2,52 puntos | HECHO (cifra publicada); la inferencia sobre F17 es SUPUESTO ELEGIDO | CAMBIA LA DECISIÓN DE C | meta.txt (línea «deslizamiento por llenado afectado»); ADR-0098:75-77 (el modelo de M1 lo dejó en 0) | a, c | Muestras de F17 con mejora de precio ≥ 2,52 puntos (las siete de ADR-0090 §7 son 0 a +2) | SOBREVIVE (hereda de P4-02, que dice lo mismo) |
| R-07 | R | El sesgo S-14 (se saltaba sesiones que acaban en break even) hace al trader más favorable de lo real en los libros sin vídeo; si es así, el techo es una cota optimista y revisarlo no puede darle la vuelta a C | SUPUESTO ELEGIDO | CAMBIA LA DECISIÓN DE C | ADR-0098:173-177 (§4a: «necesario, no suficiente»); ADR-0092 §11 | a, b | Que S-14 funcione al revés | MATIZ (hereda de P3-07, que dice lo mismo) |
| R-20 | R | La puerta 0,70/0,60 no ha cambiado y es lo que bloquea R5.2, R5.5, R5.6, R6.1, R7.x. AUDITORIA:79-84 (opción 2, «desatar R5.6») no se decidió: ADR-0098 dice que su «opción 2» es otra cosa (:9-11). El ADR de C es el sitio natural para decirlo y hoy no lo pide | HECHO | CAMBIA LA DECISIÓN DE C | AUDITORIA:79-84; ADR-0098:9-11, :133-138; HOJA:507 | a, f | — | MATIZ (hereda de M-03, que dice lo mismo) |
| M-01 | M | La corrida que cuenta no tiene pendiente positiva. Con el mismo método (R2 → R3, tras la 7a y la 7b) pasó de 31 a 30 parejas. Por extrapolación lineal (aritmética sobre cifras publicadas, que no es una predicción), la cobertura no llega nunca; en la diaria, de 38 a 70 sesiones o de 9 a 20 meses, según el tramo. | HECHO (cifras) + aritmética | CAMBIA LA DECISIÓN DE C | `HOJA-DE-RUTA.md:910-911`; `RECORRIDA-CONSTRUCCION-2.md:436`; `RECORRIDA-CONSTRUCCION-3.md:463`; `RECORRIDA-CONSTRUCCION.md:653` | a, f | La corrida tras la próxima activación sube 10 parejas o más en la que cuenta | MATIZ (matiz en §3/§9) |
| M-03 | M | El umbral de ADR-0070 está en el camino crítico al vivo. ADR-0092 §5 exige «la construcción en el umbral de ADR-0070» antes de medir la rentabilidad, y R5.6 depende de «habilita medir: sí». Con M-01, el vivo queda bloqueado mientras ningún ADR lo cambie. | HECHO | CAMBIA LA DECISIÓN DE C | `docs/adr/0092-…md:154`; `HOJA-DE-RUTA.md:505-507`; `docs/adr/0098-…md:133-138` | a, f | Un ADR que quite esa condición previa | MATIZ (matiz en §3/§9) |
| M-04 | M | Dónde se pierde el bot: la entrada es el escalón mayor (36,9 % en la que cuenta, 44,4 % en la diaria). Con las órdenes de hoy hay una cota (aritmética sobre cifras publicadas): la cobertura no puede pasar de (198 − 70 − 73) / 198 = 27,8 % en la que cuenta, ni de 83/198 = 41,9 % en la diaria, aunque se arreglen el stop, el llenado y el instante. Una pareja de ADR-0043 exige la misma clave y Δentrada (en valor absoluto) ≤ 3, y la cascada toma la orden más cercana en entrada. | HECHO + aritmética | CAMBIA LA DECISIÓN DE C | `RECORRIDA-CONSTRUCCION-3.md:474-480`; `diaria…txt:3902`; `criterio_fidelidad.py:115-119` y `:529-538` | a, b, f | Que haya llenados a otro precio que el de la orden; no lo medí | MATIZ (matiz en §3/§9) |
| M-05 | M | El escalón de la entrada tiene una ambigüedad abierta con valor por defecto (A-48), aplazada a la sesión que C no deja grabar. Que A-48 sea la causa no está medido: la fila P3 («otra zona», 57) también da entradas distintas. | HECHO / PREGUNTA PENDIENTE (el trader y el consultor) | CAMBIA LA DECISIÓN DE C | `RECORRIDA-CONSTRUCCION-3.md:601`, `:739`; `PROJECT_STATE.md:28`; `HOJA-DE-RUTA.md:435` | a, b | Una ablación de `orden_stop_punto` que no mueva el escalón | MATIZ (matiz en §3/§9) |
| M-08 | M | S-14 no explica la precisión. El diagnóstico del arnés da la cascada y la esperanza sin las 42 operaciones de break even, pero no la cobertura ni la precisión. Cotas (aritmética sobre cifras publicadas): 30/166 = 18,1 % si ninguna era pareja y todas puntuaban; techo absoluto 72/208 = 34,6 % si las 42 fueran parejas verdaderas. En julio, con vídeo y con el trader diciendo que ahí sí apunta las de break even, la precisión es 33,3 % (diaria 32,2 %). Además el filtro no distingue: quitarlas baja las cuatro piezas de 14 a 11. | HECHO + aritmética | CAMBIA LA DECISIÓN DE C | `cableado.py:1436-1477`; `RECORRIDA-CONSTRUCCION-3.md:503-507`, `:468`, `:627`; `SESION-07-EXTRACCION.md:469-476`; `ACTIVAR-SESION-07.md:712-714`; `criterio_fidelidad.yaml:61-65` | a, b | Que T diga que julio no está grabado entero (julio es provisional) | SOBREVIVE |
| M-09 | M | S-14 tampoco puede dar la vuelta al techo, con una condición: que las sesiones omitidas salgan en break even también en nuestro simulador (≈0 R o algo menos, por los costes). Sumar k operaciones de ≈0 a una media de −0,239 sobre 191 la acerca a 0 sin pasarla; no llega a +0,10 ni arregla d) 4,88 %. Solo cambiaría si esas operaciones fueran ganadoras en el simulador. | SUPUESTO ELEGIDO (la condición) + aritmética | CAMBIA LA DECISIÓN DE C | `meta.txt:13-20`; `docs/adr/0098-…md:103-110`, `:173-176` | a, b | Que las operaciones omitidas salieran ganadoras en el simulador; no se puede medir | MATIZ (hereda de P3-07, que dice lo mismo) |
| M-10 | M | Para que la esperanza del techo llegue a +0,10, la ejecución real tendría que ser 2,52 puntos mejor por llenado afectado que el modelo actual (deslizamiento 0 y spread de Dukascopy). Y aun así quedarían el percentil 95 y d). F17 solo lo mueve a favor si el spread de FTMO es menor que el de Dukascopy. | HECHO | CAMBIA LA DECISIÓN DE C | `meta.txt:20`; `criterio_fidelidad.py:869-882` | a, c | F17 midiendo una ejecución mejor que el modelo en esa magnitud | SOBREVIVE (hereda de P4-02, que dice lo mismo) |
| M-14 | M | El 0,70 / 0,60 no tiene derivación: es «texto literal del consultor». ADR-0043 justifica las tolerancias, no los umbrales. ADR-0070 los mantiene porque cualquier otro se elegiría viendo las corridas. | SUPUESTO ELEGIDO | CAMBIA LA DECISIÓN DE C | `docs/adr/0043-…md:11-12`, `:55`, `:100-103`; `docs/adr/0070-…md:223-225`; `CRITERIO-FIDELIDAD.md:71` | a, e | Un documento commiteado que derive el 0,70 / 0,60 | SOBREVIVE |
| M-15 | M | Con nuestros costes, un bot fiel hereda aproximadamente el techo: −0,239 R, percentil 95 −0,026 y d) 4,88 %, que incumplen b), c) y d) de ADR-0092 §3. Llegar al 0,70 lleva a un bot que no pasaría la puerta de rentabilidad. Con las reservas de ADR-0098 §4 a): backtest manual, S-14, A-16 y F17. | HECHO + razonamiento | CAMBIA LA DECISIÓN DE C | `meta.txt:13-20`; `docs/adr/0092-…md:76-92`; `docs/adr/0098-…md:160-161`, `:173-177` | a, c | Que F17 o A-16 cambien el techo | MATIZ (matiz en §3/§9) |
| D-01 | D | La regla «el techo solo cambia con material nuevo (diciembre si el consultor lo declara construcción; un backtest nuevo con vídeo) o con F17, y se relee» está escrita solo en la salida D. La salida C no dice cómo se relee el techo ni con qué material. Cualquier relectura necesita un ADR nuevo que declare lo visto. | HECHO | CAMBIA LA DECISIÓN DE C | ADR-0098:149-155 (D) frente a 144-148 (C); ADR-0098:212-213 | a, f | Un párrafo de ADR-0098 que aplique la relectura de D a C | SOBREVIVE |
| D-02 | D | Opción 3: gasta de una vez 2025-06 a 2025-11 (y 5 meses más si N<100), sin deshacer. La puerta no puede dar «pasa» antes de F17, así que la medida ahora solo puede dar «no pasa», «insuficiente» o «pendiente de F17». Además el comando no existe, no hay velas de 2025 y la línea «habilita medir» exige 0,70, que hoy está en 15,2 % (RC3). | HECHO | CAMBIA LA DECISIÓN DE C | ADR-0092:113, 117-158, 176; `criterio_fidelidad.yaml:84-86`; HOJA:507, 920 (Marcador, 2026-11-22: 15.2/14.4) | a | Un ADR que fije que la medida corre antes de F17 y declare los meses quemados | MATIZ (matiz en §3/§9) |
| D-03 | D | Opción 4: diciembre 2025 está reservado por número de mes y «un mes no sale» de `meses_reservados` (holdout.py lo niega sin excepción). Entrar como construcción exige código, ADR y la reforma del régimen «solo añadir». Sin vídeo (sesgo S-14) y ya comentado por el trader en v10. | HECHO | CAMBIA LA DECISIÓN DE C | PS:81; PS NA:I; ADR-0092:125-126; HOJA R5.4 (484-485); `holdout.py:652-664` | a, d, f | El ADR de salida de `meses_reservados` ya escrito (HOJA dice: «hoy no existe») | MATIZ (matiz en §3/§9) |
| P1-01 | P1 | El techo usa el stop, el lote y la unidad del R de **V1** (el stop del libro); de V2 solo comparte la relación 3,75. Comparar R entre V2 y el techo mezcla unidades (0,8D frente a D) | HECHO | CAMBIA EL PLAN | `techo_parejas.py:543-555,806`; `viabilidad_comision.py:76-79`; `VIABILIDAD-COMISION.md:76-77`; `viabilidad_trader.py:312-314` (stop del caso = initialSL) | a, d | Que `op.stop` del techo no fuera el initialSL | REFUTADO tal como estaba («usa los de V1»); entra reformulado: en estructura es V2, en puntos coincide con V1 (§3, P1) |
| P1-04 | P1 | V2 no se ejecuta sobre el main de hoy, por tres motivos: la condición de construcción, el Broker que exige saldo cuando el perfil declara apalancamiento, y `abrir_conocida`, que ahora rechaza por margen. Los guiones no han cambiado desde f59d5697 | HECHO | CAMBIA EL PLAN | `viabilidad_trader.py:235-237`; `criterio_fidelidad.yaml:47`; `broker.py:382-386,678-683`; `viabilidad_comision.py:154`; `git log` de los guiones | d | Que se ejecutara (no se ejecuta, por 2.5) | SOBREVIVE |
| P1-05 | P1 | El R del techo no depende del lote: limitar no mueve la esperanza y el 50 nunca muerde solo. Lo único que mueve es meter las operaciones que V2 excluía | HECHO | CAMBIA EL PLAN | `cableado.py:1349-1352`; `criterio_fidelidad.py:582-585`; `MARGEN-LOTE.md:804-806` | d, e | Swaps o redondeos no proporcionales al lote | SIN PASADA |
| P1-07 | P1 | Aritmética sobre cifras publicadas: en abril y agosto la comisión por R queda casi igual, 0,42 en V2 (67 operaciones, sobre 0,8D) y 0,43 en la unidad del techo (77, sobre D). Las 7 que excluye V1 pagan unos 1,2 R cada una: (0,43·77 − 0,35·70)/7. La comisión no separa V2 del techo | HECHO | CAMBIA EL PLAN | `VIABILIDAD-TRADER.md:82,103`; `VIABILIDAD-COMISION.md:111-112` | a, d | La distribución de stops de enero y julio | REFUTADO tal como estaba; entra reformulado (§3, P1) |
| P1-08 | P1 | Cota, por aritmética sobre cifras publicadas: la comisión media del techo está entre 0,336 y 0,673 R (pendiente 0,339/2,52 = 0,1345 por punto, con 1 o 2 llenados afectados). La esperanza bruta del techo, con swaps ≈0, está entre +0,10 y +0,43 | HECHO | CAMBIA EL PLAN | `meta.txt:13,18`; `criterio_fidelidad.py:824-827,869-882`; `cableado.py:1349-1352` | a, c | Swaps distintos de 0 | SOBREVIVE (hereda de P4-01, que dice lo mismo) |
| P1-09 | P1 | Spread: V2 no paga spread a la entrada; el techo dispara por el lado del llenado. Si V2 se ahorra un spread depende de a qué precio van referidos los precios del trader en FX Replay | PREGUNTA PENDIENTE (dueño: Aleks o el trader; los ingenieros) | CAMBIA EL PLAN | `broker.py:658-689`; `llenado.py:237-245,321`; `VIABILIDAD-COMISION.md:98-101` | b, c, d | Saber cómo llena FX Replay | SIN PASADA |
| P1-10 | P1 | El −2 de V2 sale de 9 leyendas de agosto. La medida posterior encuentra las entradas en el tick del lado del llenado con mediana 0, y no contesta A-16 | HECHO | CAMBIA EL PLAN | `BLOQUE-DE-LA-CAJA.md:197-206`; `METODO-FIDELIDAD-RENTABILIDAD.md:872-893`; `ambiguedades.yaml:313-336` | a, d | — | SIN PASADA |
| P1-13 | P1 | Las salidas en break even no están publicadas: `meta.txt` da «movido 79». Umbral, por aritmética: el break even ayuda si menos de ~12 % de las que vuelven a la entrada habrían llegado al objetivo | HECHO | CAMBIA EL PLAN | `meta.txt:11`; `techo_parejas.py:523-530`; `VIABILIDAD-TRADER.md:103` | b, d | — | MATIZ (matiz en §3/§9) |
| P1-14 | P1 | Casi toda la muestra de V2 es material sin vídeo (S-14; salvo un día de abril con vídeo, criterio_fidelidad.yaml:63). En el techo, julio ≈ el resto, por aritmética | HECHO | CAMBIA EL PLAN | `criterio_fidelidad.yaml:55-64`; `meta.txt:13,23` | a | — | SIN PASADA |
| P1-17 | P1 | El control del techo no ejercita la caja derivada, el instante de colocación ni la regla de no colocable: usa la caja y el instante reales. Solo el test de humo los toca, y fija el ROUND_UP | HECHO | CAMBIA EL PLAN | `techo_parejas.py:59-66,702-725`; ADR-0098 §1:64-71; `test_techo_parejas.py:167-171` | d | — | MATIZ (matiz en §3/§9) |
| P2-03 | P2 | La zona de control «posterior» que dispara el BE es lectura de la sesión nocturna del 2026-09-30, no del trader. ADR-0061 §4 lo dice («Ninguna fuente dibuja la zona posterior vela a vela») y la geometría es «vela contraria tras racha a favor». La 7a dio otra definición. La sesión 8 dejó sin respuesta si la zona se forma antes o después de romper el punto. Es la pieza que mueve el stop en 79 de 191 | SUPUESTO ELEGIDO (ADR-0061 §4, aceptado por el consultor) | CAMBIA EL PLAN | `0061-…md:61-80`; `SESION-07-EXTRACCION.md:401,436-441`; `SESION-08-EXTRACCION.md:366-367,402-403`; `RECORRIDA-CONSTRUCCION-3.md:206-207` | b, d | Un dibujo del trader vela a vela de una zona posterior que coincida con `zona_posterior_completada` | MATIZ (matiz en §3/§9) |
| P2-04 | P2 | El criterio del BE cambió en cada sesión (sesión 1 «apenas toca»; 3 toque; 5 las dos; 6 cierre y cuerpo con excepción de imbalance; 7a cierre y cuerpo sin imbalance; 8 «depende del contexto»). La spec lleva `cierre` + `cuerpo` fijos, sin contexto y sin margen. A-13 sigue ABIERTA | PREGUNTA PENDIENTE (el trader) | CAMBIA EL PLAN | `ambiguedades.yaml:215-245`; `parametros.yaml:1072-1101`; `SESION-08-EXTRACCION.md:392-395,404-407`; `ACTIVAR-SESION-08.md:598` | b | Que el trader fije un criterio estable | SIN PASADA |
| P2-07 | P2 | Los libros sin vídeo omiten sesiones que él sabía que iban a acabar en BE (S-14). En la serie anotada (abril y agosto) solo **5 de 77** cierran a cero (6,5 %). El propio trader dijo en v4 que había **13 break-evens** en un backtest de enero (`ev-v4-000133-01d2ca0a`; sin año ni denominador; 13/54 = 24 %, aritmética). Por tanto la anotada (+0,56) está sesgada al alza frente a cualquier regla con BE, y el techo repite esas mismas operaciones. ADR-0098 §4a lo reconoce pero no lo cuantifica | HECHO (S-14) + SUPUESTO (que «enero» sea el mismo enero) | CAMBIA EL PLAN | `VIABILIDAD-TRADER.md:28`; `SESION-05-EXTRACCION.md:785-787,1133-1136`; `ev-v15-011912-0ae32588`; `RECORRIDA-CONSTRUCCION-2.md:118-124` y `:459-461`; `0098-…md:173-177` | a, b | Que el trader cuente el recuento real de BE de cada libro | SIN PASADA |
| P2-11 | P2 | La frase de VIABILIDAD-COMISION («salidas reales mejores que cualquier regla fija») **no tiene en lo commiteado una explicación por gestión manual**. Hay cuatro candidatas, sin aislar: (a) 5 operaciones a cero; (b) 5 que superan 3 R; (c) 2 que cierra antes del objetivo (2,5 a 2,9 R); (d) caminos de OANDA y Dukascopy (A-16) y contabilidad de la pérdida: la anotada pierde −1,34 pips (≈ el stop medio de V2, 1,33) y V2 pierde −1,83, medio pip más por el llenado al tick con spread. Aritmética sobre cifras publicadas | HECHO + SUPUESTO sobre la causa | CAMBIA EL PLAN | `VIABILIDAD-COMISION.md:45-47`, `:107,110,112`; `VIABILIDAD-TRADER.md:179-194` | a, c | Medir con el mismo bróker las 77 con la gestión de la anotada reproducida | SIN PASADA |
| P3-01 | P3 | **A-16: medido frente a no medido.** Medido: (1) la entrada del trader respecto a la M1 BID de Dukascopy del minuto del llenado: 183/198 dentro, 15 a 1-4 puntos, mediana al tick del lado 0 y p90 1; (2) velas sueltas con leyenda: abril n=3 (1-2 puntos) y agosto 9 velas o 36 valores (mediana +2, máximo 4, OANDA por encima); (3) enero por píxeles, mediana 2-4 puntos con el error de píxel; (4) MT5/FundedNext contra Dukascopy, otra pareja y un día de un mes que no es de construcción. No medido: velas contra velas en una muestra; si FX Replay pinta bid, ask o mid; si sus llenados llevan spread; el efecto en decisiones; la vela de otro color que dijo el trader. | HECHO | CAMBIA EL PLAN | `ambiguedades.yaml:321-329`; `METODO-FIDELIDAD-RENTABILIDAD.md:872-893`; `BLOQUE-DE-LA-CAJA.md:194-210`; `LA-CAJA-DEL-29-DE-ABRIL.md:275-276`; `ABRIL-Y-LA-CAJA.md:439-441`; `RELOJ-INVIERNO.md:309-311`; `anexos/A-16-proveedor-de-datos-2026-09-09.md:26-33, :52-53`; `AUDITORIA-2026-09-13-ultracode.md:1920`; `ev-v19-012924-64367863` sin medir | a, c | Un informe que compare velas de OANDA y Dukascopy en una muestra amplia, o que mida el lado y el spread de FX Replay | MATIZ (matiz en §3/§9) |
| P3-02 | P3 | **Sensibilidad (aritmética sobre cifras publicadas):** pendiente 0,339/2,52 ≈ 0,1345 R por punto y llenado afectado. Llevar el techo a 0 pide ≈1,78 puntos a favor por llenado, la escala de A-16. Un desfase constante de nivel no actúa así (desplaza entrada, stop y objetivo a la vez). Sí actuarían por llenado: el spread de FX Replay en sus llenados y el llenado al nivel frente al tick que hace el techo. Y aun con esperanza ≥ 0 el techo seguiría en «no gana» por d) y e). | HECHO | CAMBIA EL PLAN | `meta.txt:13, :18`; `criterio_fidelidad.py:824-827, :869-882`; `meta.txt:15-16` frente a ADR-0098:103-107 y `criterio_fidelidad.yaml:78-80` | a, c | Que la pendiente por llenado se mida y salga muy distinta; o que el modelo de llenado de FX Replay coincida con el del techo | SOBREVIVE (hereda de P4-01, que dice lo mismo) |
| P3-03 | P3 | **El −2 de V1-V4.** Sale de `DESFASE_PUNTOS = 2`, con la mediana de BLOQUE-DE-LA-CAJA §2.3: 9 velas de agosto (36 valores) más abril n=3. Se aplica igual a entrada, stop y movimiento del stop, con llenado forzado en el instante (`abrir_conocida`). Tensión: en el instante del llenado, el precio de Dukascopy del lado del llenado menos L tiene mediana 0 en 75 operaciones; un +2 constante predeciría ≈ −2. Ni el −2 ni el 0 están establecidos. | HECHO | CAMBIA EL PLAN | `viabilidad_trader.py:50, :380-381, :397-399, :412`; `VIABILIDAD-TRADER.md:61-66`; `BLOQUE-DE-LA-CAJA.md:200-209`; `ORDEN-STOP-O-LIMITE.md:109-110` | a | Una medida en el llenado, con muestra, que dé ≈ −2 del lado del llenado | SIN PASADA |
| P3-04 | P3 | **La diferencia V2 frente al techo no se puede atribuir a A-16.** Difieren en al menos ocho piezas (−2 frente a 0; llenado forzado frente a stop; sin BE frente a 79 movidos; geometría; tope de 100 frente a limitar; meses; cuenta por mes; intervalos). Nadie las ha aislado. | HECHO | CAMBIA EL PLAN | `VIABILIDAD-COMISION.md:11-13, :74-79, :87-94, :112`; ADR-0098:34-63, :202-206; `meta.txt:11` | a | Una descomposición pieza a pieza publicada | SIN PASADA |
| P3-07 | P3 | **S-14, dirección.** Las sesiones saltadas son las que el trader sabía que acababan en break even. En el techo se repetirían casi siempre como break even, que cuesta ≈ −5/d R de comisión: 0,35 R de media con la geometría del techo y 0,33 con la mediana d=15. Eso está por debajo de −0,239, así que **S-14 sesga el techo hacia arriba**: corregirlo lo hunde más. En la serie anotada pasa lo mismo (aritmética: con c=0,43 harían falta ≈67 break even omitidos para llevar +0,56 a +0,10, y ≈100 para llevarla a 0). | SUPUESTO ELEGIDO (dirección razonada con fuentes) | CAMBIA EL PLAN | `SESION-05-EXTRACCION.md:767-779`; `ACTIVAR-SESION-05.md:300-312`; `VIABILIDAD-COMISION.md:111, :115, :34`; `VIABILIDAD-TRADER.md:28`, `:81`; `METODO-FIDELIDAD-RENTABILIDAD.md:233-235` | a, b | Que los break even del trader, repetidos con RN-014, acaben al objetivo | MATIZ (matiz en §3/§9) |
| P3-08 | P3 | **Operaciones por día (aritmética sobre cifras publicadas):** julio 67/13 = 5,2; enero 54/21 = 2,6; abril 35/21 = 1,7; agosto 42/21 = 2,0. Compatible con sesiones saltadas en los libros sin vídeo, pero también con el régimen, la evolución del trader o las reentradas: no mide S-14. El techo de julio no se separa del total. | HECHO (aritmética) | CAMBIA EL PLAN | `RECORRIDA-CONSTRUCCION-3.md:467-470`; `meta.txt:13, :22-24` | a, b | Una medida de sesiones con operación por mes | SIN PASADA |
| P3-09 | P3 | **Julio no es la referencia limpia.** Es provisional y F5 no se aplicó. 3 NO APARECE y 24 de 67 sin comprobar. El trader deja entradas válidas «para no afectar al mostreo». En el backtest no siempre pone el break even. El libro cubre solo del 1 al 17, y los días 20-31 que narra son «casi todas break even». | HECHO | CAMBIA EL PLAN | `criterio_fidelidad.yaml:61-65`; `VIDEO-JULIO.md:546, :552, :569-581, :682, :702, :704, :938-940`; `ev-v14-004404-ab0281c6`; `ENTRADA-JULIO.md:336`; PROJECT_STATE.md:32 | a, b | La rama del VAD convierte las no comprobadas y F5 pasa | SOBREVIVE |
| P3-12 | P3 | **A-16 actúa también en la gestión.** El break even del techo decide sobre cierres «con cuerpo» de la M1 BID de Dukascopy; el trader decidió sobre las velas de OANDA, y dijo que una vela sale de otro color en las dos fuentes. Sin medir. | PREGUNTA PENDIENTE (el consultor y los ingenieros) | CAMBIA EL PLAN | `techo_parejas.py:30-33, :523-530`; `meta.txt:11`; `ambiguedades.yaml:326-328` | a, c | Velas de FX Replay en las que el lado del cierre coincide en los 79 | SIN PASADA |
| P3-13 | P3 | **El modelo de llenado de FX Replay no está medido.** La etiqueta coincide con la entrada del libro (Δ0); el techo llena al precio del tick. VIABILIDAD-COMISION afirma que el spread va dentro de los llenados de OANDA; METODO (posterior) dice que sigue sin resolverse qué es `entryPrice`. Gana METODO: la afirmación de VIABILIDAD-COMISION queda con MATIZ. | PREGUNTA PENDIENTE (Aleks/trader, o medida en vídeo) | CAMBIA EL PLAN | `VIDEO-JULIO.md:558-560`; `ORDEN-STOP-O-LIMITE.md:171`; `llenado.py:215-220`; `VIABILIDAD-COMISION.md:99-101` frente a `METODO-FIDELIDAD-RENTABILIDAD.md:323-325`; `AUDITORIA-2026-09-13-ultracode.md:1920` | a, b, c | Fotogramas que enseñen que FX Replay llena con spread o con hueco | MATIZ (matiz en §3/§9) |
| P3-15 | P3 | **«La regla de ADR-0092 §9 no se dispara» no dice que A-16 no pese en el techo.** La regla mide si la entrada cae dentro del rango de una M1. El propio informe lo dice: «estar dentro no quiere decir que las dos series marquen el mismo precio». | HECHO | CAMBIA EL PLAN | ADR-0092:246-250; `METODO-FIDELIDAD-RENTABILIDAD.md:881-893` | a | — | SIN PASADA |
| P4-02 | P4 | El equilibrio −2,52 pide deslizamiento a favor en las stops, que el modelo excluye y la demo no vio. F17 no puede convertir C en «gana» por el deslizamiento, solo empeorarlo; C no tiene por qué esperar a F17 para la dirección, solo para la cuantía | HECHO | CAMBIA EL PLAN | ADR-0057 §1 (:19-29); DEMO-EJECUCIONES-2-3.md:41-44; ADR-0090 §7 (:231-237); meta.txt:18 | a, c, f | Que F17 midiera de forma sistemática llenados de stops mejores que el tick que las dispara, de 2,5 puntos o más | SOBREVIVE |
| P4-03 | P4 | Coste mal modelado: la relectura de ADR-0092 §4 (`veredicto_con_f17`) solo resta deslizamiento. El spread de FTMO no tiene vía y el techo usa el de Dukascopy. Es el canal que más mueve: el spread de la demo leyó 2 puntos (y 1-2) en un instante, frente a una media de Dukascopy de 2,7-3,5. Del orden de Δs·x, entre +0,07 y +0,27 R si Δs es 1-2 puntos; no da la vuelta a C solo | HECHO (la magnitud es aritmética sobre cifras publicadas y aproximada, porque el spread también cambia qué órdenes se llenan) | CAMBIA EL PLAN | ADR-0092:99-115; criterio_fidelidad.py:885-921; DEMO-EJECUCION-1.md:165; TICKS-SPREAD-SALIDA.txt:23-31; FTMO-REGLAS.md:310 | a, c | Un perfil de spread de FTMO por hora igual al de Dukascopy, o una regla escrita que meta el spread en la relectura | MATIZ (matiz en §3/§9) |
| P4-04 | P4 | Nadie ha fijado contra qué precio se mide el deslizamiento. El simulador ya cobra el hueco de los ticks de Dukascopy, así que «llenado − nivel» lo contaría dos veces: 1 punto son 0,13 R. MedirDemoFTMO no registra el tick que dispara la orden | PREGUNTA PENDIENTE (el consultor; F17) | CAMBIA EL PLAN | ADR-0051 §4 (:70-79); llenado.py:219-261,320-328; DEMO-EJECUCION-1.md:185 («no dice qué tick la disparó») | c | Un encargo de F17 que fije la referencia (llenado − tick que dispara en FTMO, y aparte FTMO frente a Dukascopy) | MATIZ (matiz en §3/§9) |
| P4-05 | P4 | F17, tal como lo define el MASTER_PLAN, es un grabador de ticks y spread que entrega un «perfil de spread». No coloca órdenes, así que no puede medir el deslizamiento de las stops que le piden ADR-0092 §4, ADR-0098 C y A.5 | HECHO | CAMBIA EL PLAN | MASTER_PLAN.md:127; HOJA-DE-RUTA.md:750-758 (A.5 «que también mide el deslizamiento»); ADR-0090:236-237 | c, f | Un F17 redefinido que coloque y registre órdenes stop | MATIZ (matiz en §3/§9) |
| P4-06 | P4 | Cuántas órdenes harían falta, sin varianza medida. Mediana a ±0,37 puntos (±0,05 R): unas 44σ² (normal); con masa en 0, 30-50. p90: cota superior sin supuestos con n ≥ 29 (0,9^29 = 0,047); un intervalo útil, 100-400 por clase (entrada stop, cierre por stop, cierre a mercado). Un bot como el de la corrida 1 da unos 5,6-6,2 llenados afectados al día (235/76 = 3,09 operaciones al día por 1,81-2) y una prueba dura 14 días naturales: unos 56-62 llenados. No basta una prueba: hace falta un guion que genere órdenes o varias pruebas | HECHO (aritmética sobre cifras publicadas; las σ son supuestas) | CAMBIA EL PLAN | RECORRIDA-CONSTRUCCION-3.md:510-513; resumen-cuenta-por-mes.txt:74-77; ADR-0090:80-82 (los 14 días de la prueba); criterio_fidelidad.yaml:82-83 (p90) | c | Una varianza medida mucho menor, o la decisión de no separar las clases | MATIZ (matiz en §3/§9) |
| P4-08 | P4 | Que la prueba gratuita ejecute (spread, deslizamiento, comisión) igual que el Challenge y la FTMO Account no está en el repo. ADR-0090 ya lo duda para la tasa de margen | PREGUNTA PENDIENTE (FTMO; Aleks) | CAMBIA EL PLAN | ADR-0090:157-159 §4(d); sin fuente en FTMO-REGLAS.md ni en DEMO-FTMO.md (grep de «free trial» y «prueba gratuita») | c, a | Una respuesta de FTMO o una medida en la cuenta real | MATIZ (matiz en §3/§9) |
| P4-09 | P4 | El break even va a «la entrada exacta» y cada BE que salta cierra en unos −5/D R (la comisión, más el hueco), entre 0,34 y 0,67 R. El techo movió el BE en 79 de 191; la corrida 1 del bot dio 50 de 235 cerrados en BE. Es la interacción de una regla del trader con un coste impuesto | HECHO (el mecanismo); cuántos BE cierran en el techo, sin publicar | CAMBIA EL PLAN | strategy_spec.yaml:1800-1827 (RN-014); meta.txt:11; resumen-cuenta-por-mes.txt:74-77; cableado.py:1349-1351 | b, a | Que el trader, en una cuenta con comisión, ponga el BE en entrada + costes (es la pregunta) | MATIZ (matiz en §3/§9) |
| P5-02 | P5 | El trader dice operar en «cuentas propias» y en «cuenta de fondeo». Sin número, sin importes y sin resultados. | HECHO (sobre lo que dijo) | CAMBIA EL PLAN | `docs/validation/SESION-01-2026-09-09.md:68-73` («Noticias y cuenta de fondeo»; la operativa del trader «corre en cuentas propias»). `docs/adr/0022-el-bot-no-opera-noticias-en-la-cuenta-fondeada.md:39-40`: «opera cuentas propias que no lo prohíben y su estrategia funciona dentro de esos eventos». `SESION-04-EXTRACCION.md:549,564,916`: «la condicional que nos da la cuenta de fondeo», con 0,5 %. «Funciona dentro de esos eventos» es una afirmación del trader sobre su estrategia, sin medida. | a, b | Respuesta del trader sobre cuántas cuentas, de qué firma y con qué retiros | SIN PASADA |
| P5-03 | P5 | El riesgo real del trader en fondeo es 0,4-0,5 %, y en backtest 1 %. El bot usa 0,5 %. | HECHO (parte documental) / SUPUESTO ELEGIDO (el 0,5 % del bot) | CAMBIA EL PLAN | `knowledge/spec/parametros.yaml:1279` («1 en backtest; 0,4-0,5 en fondeo»), `:1283` (valor 0.5), `:1481-1483` (las 9 pérdidas «vienen de una cuenta con un 0,5 %»; con menos riesgo «podríamos extender»). La fuente es `fb-2026-09-09-sesion-01-648ec915`, que no se lee. `SESION-01-2026-09-09.md:40` dice «0,4 %», y `parametros.yaml` dice 0,4-0,5: [corrección del orquestador: no hay discrepancia viva; SESION-01:39-40 dice que la tabla vieja ponía 0,4 y ADR-0020 lo invirtió]. | b, f | Ver el historial de una cuenta de fondeo real | MATIZ (corregido por el orquestador: SESION-01:39-40 y ADR-0020; registro 00:02) |
| P5-06 | P5 | VIABILIDAD-COMISION lleva el aviso literal «NO SE ENSEÑA AL TRADER», con la razón: sesgaría sus respuestas, en particular A-18. ADR-0098 §3 C pide contrastar «con sus resultados reales, sin enseñarle ninguna cifra de esta medida». Hay que decidir cómo se pregunta sin dar la cifra. | HECHO | CAMBIA EL PLAN | `docs/validation/VIABILIDAD-COMISION.md:3-5`; `docs/adr/0098-...md:144-148`; `docs/plan/HOJA-DE-RUTA.md` R4.7 (línea 437-439). | b | — | SIN PASADA |
| P6-01 | P6 | El grabador de F17 no existe. El EA no lee ticks: `OnTick` solo llama a `AlConectar`. MedirDemoFTMO solo toma cotizaciones sueltas con `SymbolInfoTick`, y nadie llama a `CopyTicks`. | HECHO | CAMBIA EL PLAN | mql5/Experts/Botsito.mq5:93-96; tools/mql5/MedirDemoFTMO.mq5:146-148; HOJA-DE-RUTA.md:892; :758; PROJECT_STATE.md:57 (heredado 10) | c, f | Un fichero en git que grabe ticks a disco | SOBREVIVE |
| P6-02 | P6 | El motor solo acepta datos de Dukascopy. El validador de ticks exige `proveedor="dukascopy"`, huso UTC y `escala_volumen`; el de M1 exige además BID y periodo 1. MASTER_PLAN preveía un esquema v2 con proveedores «al abrir F16», y no se hizo. El formato CSV sí se puede reutilizar; basta convertir la hora del servidor a UTC con A-28 (ADR-0090). | HECHO | CAMBIA EL PLAN | src/botsito/data/ticks.py:483-486, :59, :229-264; data/dukascopy.py:33-37; data/dataset.py:299-308; domain/ticks.py:26-43; MASTER_PLAN.md:292 | c, d | Un proveedor distinto aceptado en `validar_manifiesto_ticks` | MATIZ (matiz en §3/§9) |
| P6-03 | P6 | El mercado de un día solo se construye desde un caso `dev` de construcción con reparto dev-visto (`mercado_de_construccion` → `caso_de_construccion` → `dias_de_construccion`, que falla «no hay reparto dev-visto»). Reutilizable: `MercadoDia` y `MotorCableado.correr_dia(DiaDeMercado)`. Falta un constructor del «día de cancha» que no pase por `cases/`. El calentamiento lee el M1 del mes y del anterior. | HECHO | CAMBIA EL PLAN | engine/simulacion.py:56-68, :183-218; engine/visor.py:207-238; engine/arnes.py:139-173, :193-212; engine/cableado.py:320-328 | c, d | Un camino del motor que corra un día sin caso | MATIZ (matiz en §3/§9) |
| P6-04 | P6 | `_ticks_del_dia` junta los ticks de TODOS los manifiestos que cubren la ventana: si conviven Dukascopy y FTMO del mismo día, la serie queda mezclada sin aviso. | HECHO | CAMBIA EL PLAN | engine/simulacion.py:166-180 | d | Un filtro por proveedor en ese bucle | MATIZ (matiz en §3/§9) |
| P6-05 | P6 | Un grabador pasivo no mide el deslizamiento de las órdenes stop que pide ADR-0092 §4. Los ticks dan el spread y el «hueco», no el deslizamiento de ejecución. Para medirlo, F17 necesita: (1) una parte que ponga órdenes, en `tools/`; (2) las operaciones reales del trader en FTMO; o (3) las del bot. A.5 dice «que también mide el deslizamiento» sin decir cómo. | HECHO | CAMBIA EL PLAN | ADR-0092:105-107; DEMO-FTMO.md:177-178; ADR-0090:233-237; llenado.yaml:7-12; Botsito.mq5:9-11; tests/contract/test_capa_mt5.py:42-47; HOJA:754 | c, a | Un ADR o encargo que defina una medida pasiva del deslizamiento | MATIZ (matiz en §3/§9) |
| P6-07 | P6 | R6.0 sigue diciendo que Python en vivo se descartó «por el tope de peticiones», y RUMBO §4 y §5 repiten esa razón. El recuadro de ADR-0082 del 2026-11-22 la quita. Gana el ADR. | HECHO | CAMBIA EL PLAN | HOJA:635-637; RUMBO-2026-11.md:37, :43; ADR-0082:101-114; ACTIVAR-SESION-08.md:859 | e, f | Una R6.0 ya corregida en main | MATIZ (matiz en §3/§9) |
| P6-09 | P6 | La vía (i) no necesita un puente en vivo. R7.3 corre el motor «sobre días ya cerrados». Grabar ticks es leer y registrar (ADR-0082 D3), y FTMO contestó que las lecturas no cuentan para las 2.000 peticiones. | HECHO | CAMBIA EL PLAN | HOJA:680; RUMBO:43; ADR-0082:37-41; ACTIVAR-SESION-08.md:639 | c, d, e | — | SIN PASADA |
| P6-10 | P6 | Matiz sobre diciembre. Al motor y a la descarga los limita `construccion`, no `meses_reservados`. Que el mes 12 quede tapado por número sí es verdad, pero en el código solo actúa en la cuarentena del texto. Con la cancha en diciembre, se ocultaría el texto de las sesiones sobre esos días. La guardia lee una carpeta «Backtest» de un mes fuera de enero, abril, julio y agosto como material sin abrir. | HECHO | CAMBIA EL PLAN | criterio_fidelidad.yaml:47; cli.py:2884-2897, :2929-2936; arnes.py:3-5; cases/holdout.py:620-640; cli.py:435, :587, :1134, :1318-1325; corpus/cuarentena.py:220-228; ADR-0092:136-139; guardia.py:353, :436-438, :713-716 | a, c, f | `meses_reservados` leído por el motor o por `download-ticks` | MATIZ (matiz en §3/§9) |
| P6-11 | P6 | El calendario de cierres cubre de principios de diciembre de 2025 a principios de octubre de 2026, y el simulador niega cualquier día de fuera. Cada renovación es una rama con el ritual entero y un tag, y solo llega hasta la víspera del jueves siguiente. Para un diferido «cada pocos días», una rama por semana. Alternativa: los cierres desde `SymbolInfoSessionTrade`, que el journal del EA ya registra. | HECHO | CAMBIA EL PLAN | knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:21-22; RENOVAR-CIERRES.md:4-5, :19-27, :34-37, :46, :57-62; Botsito.mq5:52, :86 | c, d, f | — | MATIZ (matiz en §3/§9) |
| P6-13 | P6 | Tamaño (aritmética sobre cifras publicadas, sin R): trader 2,61 operaciones por día dev (191 llenadas: 2,51); bot 3,09. Para N = 100: unos 39-40 días de mercado (trader) y 33 (bot); con el ritmo de julio, 20; con el de abril, 60. A unos 10 días laborables por prueba, unas 4 pruebas (2 a 6). Si se reserva la mitad de los días para medir, unas 8 pruebas, unos 4 meses de mercado. | HECHO (cifras de partida) | CAMBIA EL PLAN | RECORRIDA-CONSTRUCCION-3.md:130-138, :983, :510; ADR-0092:76 | a, c | Un ritmo en vivo distinto (P6-24) | MATIZ (matiz en §3/§9) |
| P6-14 | P6 | ¿Los precios de la prueba gratuita (FTMO-Demo) son los de la cuenta Swing de pago? P-D1 sigue sin respuesta. | PREGUNTA PENDIENTE (FTMO) | CAMBIA EL PLAN | DEMO-EJECUCION-1.md:222-223; HOJA:725; ADR-0071:22 | c, e | La respuesta de FTMO | SIN PASADA |
| P6-16 | P6 | ADR-0098 sacó el R del trader del simulador para no abrir la columna de resultado de su libro. La vía (iii) lee su resultado real: lectura nueva que pide un ADR (quién lee, ADR-0072; qué; cuándo; y que nunca elige un parámetro). | HECHO | CAMBIA EL PLAN | ADR-0098:93-95; ADR-0072 | a, b | — | MATIZ (matiz en §3/§9) |
| P6-17 | P6 | Las reglas para corregir sin ajustar están en su sección. | SUPUESTO ELEGIDO | CAMBIA EL PLAN | ADR-0092:174-179, :189, :160-167, :121-158; HOJA:431, :680; RUMBO:19 | a, f | — | MATIZ (matiz en §3/§9) |
| P6-19 | P6 | Horario. Ventana 07-15 Madrid, 06-14 en semanas de desajuste; en Lima (aritmética de husos) de 01:00 a 09:00 con Nueva York en invierno, de 00:00 a 08:00 en verano. En 2027 hay 15 días laborables de desajuste. | HECHO + aritmética | CAMBIA EL PLAN | ADR-0069:17-21, :34, :36-37; DEMO-FTMO.md:154-155, :193 | c | — | MATIZ (matiz en §3/§9) |
| P6-20 | P6 | Encaje: F33 depende de F17, y F34 (reconciliación diaria demo ↔ backtest) de F32 y F33. El motor de Python sobre ticks de FTMO es la pata «backtest» de F34 (supuesto). La cancha no sustituye a F34. R6a.8 no está hecha y cabe en la misma prueba que el grabador. | HECHO | CAMBIA EL PLAN | MASTER_PLAN.md:146-147; HOJA:680, :620-629; arnes.py:196; ADR-0098:222-223 | c, f, e | — | SIN PASADA |
| P6-23 | P6 | Octubre y noviembre de 2026 están reservados. Una prueba abierta hoy graba días de noviembre. Grabar velas y ticks no es abrir (ADR-0021 §1) y vale para el spread y el deslizamiento de F17. Esos días no pueden servir para comparar con el trader. El repo no dice qué material ata esos dos meses. | HECHO + PREGUNTA PENDIENTE (el consultor) | CAMBIA EL PLAN | PROJECT_STATE.md:28; CLAUDE.md punto 2 (ADR-0021 §1) | a, c | — | MATIZ (matiz en §3/§9) |
| P7-01 | P7 | Los dos intervalos no son comparables: V2 sortea operaciones y da el 95 %; el techo sortea días y da el 90 % (p5-p95). Semillas distintas. Un solo par de intervalos no se puede pegar al otro sin conversión. | HECHO | CAMBIA EL PLAN | `viabilidad_trader.py:89-98`, `criterio_fidelidad.py:611-646`, `meta.txt` línea c, ADR-0098 líneas 204-206 | a), f) | Que alguien publique el techo con remuestreo por operación, o V2 por días, sobre la misma muestra | SOBREVIVE |
| P7-02 | P7 | Con lo publicado y suponiendo independencia, la diferencia 0,709 R es ≈ 2,1 errores típicos (ET combinado 0,335). Rozaría el 5 %, no lo descarta con holgura, y la independencia es falsa (las 77 operaciones de abril y agosto están dentro de las 191). Para 2 ET harían falta unas 76 operaciones por brazo y para 3 ET unas 171, tomando 0,709 como verdad. | HECHO (aritmética sobre cifras publicadas) | CAMBIA EL PLAN | Cálculo de §2; `VIABILIDAD-COMISION.md:112`, `meta.txt` línea c | a) | Las ET reales de V2 por días, o la covarianza entre V2 y el techo sobre la misma muestra, ninguna publicada | MATIZ (matiz en §3/§9) |
| P7-03 | P7 | La diferencia NO es solo ruido. V2 y el techo difieren en: (i) V2 aplica `DESFASE_PUNTOS = 2` a entradas y stops (`viabilidad_trader.py:50`) y el techo «sin desfase» (ADR-0098 §1); (ii) V2 usa un tope de 100 lotes y excluye 10 operaciones (`VIABILIDAD-COMISION.md:93`, 112), y el perfil de ADR-0071 es 50, con lo que en el techo el lote se limita por `lote_si_no_cabe` y solo sale lo bajo el mínimo; (iii) V2 recorre 67 operaciones de abril y agosto, el techo 191 de cuatro meses; (iv) R nominal contra PnL neto ÷ riesgo con swaps; (v) cuenta y gestión: V2 la `cuenta` de la viabilidad, el techo una cuenta por mes con el motor; (vi) V1 lleva un movimiento documentado a mano, V2 no. Que 0,709 R sea ruido de muestreo no es lo que dice el repo: parte es estadística (el 95 % de V2 llega a −0,13) y parte es de medida (los puntos i a vi). `VIABILIDAD-COMISION.md:11-13` ya avisa de que parte de la ventaja de V2 viene del tope. | HECHO | CAMBIA EL PLAN | `viabilidad_trader.py:50,443`; `docs/adr/0071*:44-71`; ADR-0098 §1, líneas 34-72; `VIABILIDAD-COMISION.md:11-13` | a) | Una medición del techo sobre abril+agosto con la misma definición de R | SIN PASADA |
| P7-06 | P7 | ADR-0092 §3: a) N ≥ 100 y b) +0,10 R no atan; ata c), percentil 5 > 0. Con N entre 100 y 400 y la desviación del techo, c) exige una media verdadera de ≈ +0,29 (N=100) a ≈ +0,16 (N=340). Un bot que valga justo +0,10 necesita unas 860 operaciones para que su p5 salga positivo. La puerta es más estricta que lo que dice su cifra de 0,10. | HECHO (aritmética sobre cifras publicadas) | CAMBIA EL PLAN | `docs/adr/0092-...md:76-79`; `criterio_fidelidad.yaml:70-76`; desviación del techo de §2 | a), c) | Una desviación por operación menor en el bot que en el trader | MATIZ (matiz en §3/§9) |
| P7-07 | P7 | Muestra de la rentabilidad de ADR-0092 §5 (junio a noviembre de 2025): unos 130 días y, solo si el bot llenara al ritmo de construcción (2,6 a 3,1 por día), 339 a 402 operaciones, que cumplen N ≥ 100 en 32-38 días. Pero el ritmo en 2025 no está medido (no hay datos de 2025 bajados, ADR-0092 §5 línea 127), y un bot con esperanza negativa llegaría al límite total antes de la operación 100 (≈ 84). La «extensión» solo se activa por N, no por pérdida. | SUPUESTO ELEGIDO | CAMBIA EL PLAN | `docs/adr/0092-...md:125-134`; `PREREGISTRO.md:63`; `meta.txt` línea del control | c), f) | El ritmo real de llenadas del bot en 2025 | SIN PASADA |
| S-05 | S | **La gestión del techo es la del bot, no la del trader**; `zona_posterior_completada` decide el BE (79 de 191, 41 %) | SUPUESTO ELEGIDO | CAMBIA EL PLAN | `estructura_m1.py:263-275`; `meta.txt:11`; `parametros.yaml:1085-1086`; `techo_parejas.py:30-35` | b, c | Diagnóstico con BE apagado (nuevo ADR si el modelo cambia, 0098:211-213) | SOBREVIVE |
| S-06 | S | **«No gana» por d) y e) mide una cuenta sin frenos con umbrales propios** (3 %, 94 %), no contra 5 %/10 %. Aquí b) y el p95 también disparan «no gana» | SUPUESTO ELEGIDO | CAMBIA EL PLAN | `0092:87-91`; `0098:58-60`, `:101-111`; `meta.txt:15-17` | f | Una lectura en que b) sea positiva y d) o e) fallen | SIN PASADA |
| S-08 | S | **El deslizamiento 0 es provisional y solo hay siete muestras** | PREGUNTA PENDIENTE (F17) | CAMBIA EL PLAN | `llenado.yaml:9`; `0051:140-141`; `0090:231-237`; `meta.txt:18` | c, f | F17 | SIN PASADA |
| S-11 | S | **Todo «impuesto por el mundo» sobre FTMO viene de una prueba gratuita, no de la cuenta real**, y P-D1 sigue sin respuesta | SUPUESTO IMPUESTO sin confirmar; PREGUNTA PENDIENTE (Aleks con FTMO) | CAMBIA EL PLAN | `cuentas yaml:293-296`; `HOJA-DE-RUTA.md:725`; `0071:56-59` | c, d, e | Respuesta de FTMO / pre-vuelo R6a.7 | SIN PASADA |
| S-12 | S | **Rejilla H4 del servidor derivada, no medida** (R6a.8) | SUPUESTO ELEGIDO (derivado) | CAMBIA EL PLAN | `0090:90-100`; `parametros.yaml:317-339` | d, f | R6a.8 | SIN PASADA |
| S-15 | S | **Diez parámetros DEFAULT_AMBIGUOUS del bot y la tensión de `toma_antes_de_la_ventana`** (CONFIRMED `cuenta` frente al «no es válido» de la 7a). Son del bot, no del techo | SUPUESTO ELEGIDO | CAMBIA EL PLAN | `RECORRIDA-CONSTRUCCION-3.md:592-613`; `parametros.yaml:912-936` | d, f | — | SIN PASADA |
| R-02 | R | Hoja de ruta:7 («Metas») sigue diciendo marzo de 2027 como meta firme, sin la nota de que ADR-0098 §6 dice que marzo no cabe con ninguna vía | HECHO | CAMBIA EL PLAN | HOJA:7; ADR-0098:220-231 | a, e, f | Que la hoja lleve en otro sitio el recuadro | SOBREVIVE |
| R-03 | R | RUMBO-2026-11.md no cita ADR-0098: sigue mandando «sobre el orden de F» con §6 («dos ramas de fidelidad por cada una de infraestructura hasta fin de año», :48-49), §4 (pivote de «precisión y R de las parejas», :39) y §5 (la tabla del R de las parejas es R5.7, :43, ya HECHA y sustituida por ADR-0098). `git grep -c 0098` sobre RUMBO, MASTER_PLAN y AUDITORIA no da ninguna línea | HECHO | CAMBIA EL PLAN | RUMBO:1, :37-49; HOJA:511-522 | f | Que un recuadro de otra rama lo cubra | SIN PASADA |
| R-08 | R | R6a.4–R6a.6 portan código de Python al EA: pierden sentido si el ADR de C o los ingenieros (hacia 2026-12-03) reabren ADR-0082 §4. La fecha del 2026-12-03 solo está en ADR-0098:230, no en la hoja ni en el PS | HECHO | CAMBIA EL PLAN | HOJA:577-606; ADR-0082:101-114; ADR-0098:229-231 | e, f, d | Que el ADR mantenga el EA como bot final | MATIZ (matiz en §3/§9) |
| R-09 | R | No hay prueba gratuita viva con evidencia: la del 2026-10-29 duraba 14 días como la anterior (28/10 a 11/11, DEMO-FTMO.md:162) y su propia hoja dice «vence hacia el 12-nov; sin comprobar» (DEMO-EJECUCIONES-2-3.md:447). R4.7 depende de una (HOJA:440) | PREGUNTA PENDIENTE (Aleks) | CAMBIA EL PLAN | DEMO-FTMO.md:162; HOJA:440, :756, :920 | c, d | Que Aleks tenga otra viva | MATIZ (matiz en §3/§9) |
| R-10 | R | El grabador de F17 no existe: F17 es PARCIAL («el script de medición, no el grabador», HOJA:892) y no hay letra ni rama para él en la NA. Además `curva_con_deslizamiento` y `veredicto_con_f17` toman una sola curva y arrastran `previo` entre cuentas (PS:100; criterio_fidelidad.py:842-865), que hay que arreglar para la cuenta por mes antes de usar F17 sobre el techo | HECHO | CAMBIA EL PLAN | HOJA:892; PS:100 | c, f | — | SIN PASADA |
| R-11 | R | R5.1 dice que F26 depende de febrero y de R5.2 (HOJA:455), y R5.5 de R5.1, R5.2, R5.3 (:493), pero la letra G del PS (:34) lista como faltante solo febrero, el comando, kappa y el hash, sin R5.2. R5.2 espera un «sí» que ya no llega (HOJA:464) | HECHO | CAMBIA EL PLAN | HOJA:455, :493; PS:34 | a, f | Una decisión que F26 no necesita mayo | SIN PASADA |
| R-13 | R | Letra C (voz del ASR) está libre (sus tres condiciones están HECHAS: HOJA:154-155) y su salida decide F5 `material_sin_video` de julio, que es el S-14 que C manda revisar | HECHO | CAMBIA EL PLAN | PS:32; HOJA:145-155; ADR-0092 §11 | a, b, f | — | SIN PASADA |
| R-14 | R | Q (exportación de agosto con vídeo) acorta el sesgo S-14 que revisa C; el contraste con el trader es la ocasión de pedírsela otra vez (PS:42; HOJA:122-125) | HECHO | CAMBIA EL PLAN | PS:42; HOJA:122-125; ADR-0092 §11 | b, f | — | SIN PASADA |
| R-18 | R | «Puente» y «cancha» (las del orquestador) no aparecen en ningún documento de estado, hoja, ADR ni runbook consultado (git grep sin resultados); lo más cercano es el puente en vivo descartado por RUMBO:43 y ADR-0082 §4 | PREGUNTA PENDIENTE (consultor: definirlos) | CAMBIA EL PLAN | git grep -i «cancha» sin salida; RUMBO:43 | c, d | — | SIN PASADA |
| M-06 | M | La fidelidad que cuenta depende del PnL del bot, por los frenos de su propia cuenta. En julio, 30 de las 67 operaciones del trader (44,8 %) caen en 11 sesiones con RN-032 y el bot sin operar. «Sin orden» en julio: 32 en la que cuenta y 1 en la diaria; en total, 70 y 27. Indicio, no prueba: la equity mínima del trader en julio (92,05 %) queda por debajo del saldo con que el bot empezó a bloquear (92.374,52 al corte del 2026-07-10), así que un bot fiel también podría frenarse. | HECHO + indicio | CAMBIA EL PLAN | `RECORRIDA-CONSTRUCCION-3.md:546-557`, `:572-573`, `:476-479`; `diaria…txt:3900`; `meta.txt:17`; `ACTIVAR-SESION-07.md:593-596` | a, e, f | Repetir M1 con RN-032 activo y que la cuenta del trader no bloquee en julio (pide una rama) | MATIZ (matiz en §3/§9) |
| M-12 | M | El pivote no tiene regla de parada. Con «se cumple uno», toca una sesión más y releer con los mismos números, sin límite. Solo la salida D de ADR-0098 tiene tope (dos relecturas). Las operaciones de más de julio no bajan: 39 en la base y 40 en la diaria leída. | HECHO | CAMBIA EL PLAN | `docs/adr/0093-…md:154-155`; `PIVOTES-SESION-7.yaml:34-36`; `docs/adr/0098-…md:154-155`; `RECORRIDA-CONSTRUCCION-3.md:657-665` | a, f | Un ADR que fije un número máximo de vueltas | MATIZ (matiz en §3/§9) |
| M-13 | M | Aunque se cumpla el pivote, se está muy lejos de ADR-0070. «Se sigue» pide 19 parejas de julio, un 28,4 % de 67; el 0,70 pide unas 47 (ilustración sobre julio: el 0,70 de ADR-0070 se mide sobre toda la construcción, y «se sigue» pide además el mínimo 2). | HECHO + aritmética | CAMBIA EL PLAN | `PIVOTES-SESION-7.yaml:30-31`; `RECORRIDA-CONSTRUCCION-3.md:468` | a, f | — | SIN PASADA |
| X-01 | X | Desde RUMBO hay 18 ramas: 12 de fidelidad y 6 de otras. Cumple el 2:1 de RUMBO §6, pero 7 de las 12 «de fidelidad» son logística de sesión y solo 5 mueven medida o motor. El proceso puro no es desmedido por número (28 %). | HECHO (la clasificación es mía) | CAMBIA EL PLAN | merges de `git log --merges --first-parent --since=2026-11-06`; ERRORES-RECURRENTES.md:115-132; RUMBO §6; AUDITORIA-2026-11-21.md:50-52 | f, a | Que un informe reclasifique alguna rama | SIN PASADA |
| X-03 | X | `make check` dura unos 27 min (1625,67 s y 1612,29 s solo del paso `test`, pico 318-319 MiB, 3612 passed). Crece casi lineal con los tests, unos 0,45 s por test. Cada commit exige su sello: ~un `make check` por commit. Aritmética: 169 commits × 25-27 min ≈ 70-76 h de reloj en 14 días; unos 10,4 `make check` por rama, unas 4,5 h por rama. Sin contar rojos, repeticiones ni la CI. | HECHO (cifras publicadas) + aritmética | CAMBIA EL PLAN | RECORRIDA-CONSTRUCCION-3.md:312; RECORRIDA-CONSTRUCCION-2.md:277; MEMORIA-SUITE.md:79-80; ENTORNO-CODE.md:152-157; CLAUDE.md; PREREGISTRO-INVENTARIO.md:801-802; METODO-FIDELIDAD-RENTABILIDAD.md:744 | e, f | Commits sellados con un único `make check` sobre árboles idénticos | MATIZ (matiz en §3/§9) |
| X-04 | X | 99 de los 169 commits (59 %) no tocan código ni knowledge; pagan igual la suite entera. No puedo afirmar que sea evitable: `test_project_state`, `test_hoja_de_ruta` y `knowledge validate` leen docs. | HECHO (99/169); la evitabilidad es SUPUESTO ELEGIDO | CAMBIA EL PLAN | `git log --no-merges --since=2026-11-09 --format=%h -- src tests scripts knowledge .claude Makefile pyproject.toml mql5 \| wc -l` = 70; RITUAL.md:179-181, :272 | e | Que los tests que leen docs sean tantos que la partición no gane nada | SIN PASADA |
| X-05 | X | xdist ya se midió y se rechazó solo por memoria: en serie 1084,2 s; con `-n auto`, 409,8 a 504,1 s, mismo resultado por nombre, la guarda del holdout sigue saltando; pico de 243 a 1118-1161 MiB. Aritmética: hoy ≈ 10,5 min. La nueva medida está pendiente. | HECHO + PREGUNTA PENDIENTE (Aleks) | CAMBIA EL PLAN | ENTORNO-CODE.md:150-176, :222-228, :261; HOJA-DE-RUTA.md:783-784, :830 (G.4) | e, f | Que a 16 GB el pico o el reaper lo hagan inviable | SIN PASADA |
| X-06 | X | `make check` lee en cada ejecución el M1 entero de marzo y de junio (días reservados) para calentar el arnés. Por eso G2 exige la fila de HOLDOUT del día. Separar en otro objetivo, local y declarado, los tests que leen `data/` reduciría los `make check` que tocan reservados sin tocar ninguna barrera. | HECHO (PS:106); la propuesta es SUPUESTO ELEGIDO | CAMBIA EL PLAN | PROJECT_STATE.md:106; HOLDOUT-EXPOSICIONES.md (filas 2026-10-14, 2026-10-18, 2026-10-27); RITUAL.md:113-140; `scripts/contrato_rama.py:16-19`; AUDITORIA-2026-11-21.md:167 | e, f | Que el sello deba cubrir esos tests por decisión del consultor | SIN PASADA |
| X-07 | X | La tabla de errores no baja: primera pasada del revisor en 16 de 18 ramas, 9 bloquea, 86 importa, 75 menor = 170, unos 10,6 por rama (las 7 primeras 9,7; las 9 últimas 11,3). 30 pasadas de revisor en 18 ramas. Errores del consultor en las 6 últimas filas: 2, 4, 2, 2, 4 y 6. La tabla no etiqueta por patrón 1 a 5. Tipos recurrentes: premisa del encargo contradicha por el ADR o el repo, e ids inexistentes (5 de 18). | HECHO (recuento manual) | CAMBIA EL PLAN | ERRORES-RECURRENTES.md:7, :115-132 (ejemplos :127, :129, :131, :132) | e, f | Que otra lectura cambie las sumas | SIN PASADA |
| X-08 | X | Un fallo barato se descubre tarde: `check:` corre `test` (27 min) antes de `state`, `config` y `knowledge` (82,8 s). La fila `dieta-estado` cuenta que un id inexistente «tumbó el make check (25 min)». Reordenar los pasos baratos antes de `test` no rompe el test del sello (que solo exige `desellar` el primero y `sellar` el último). No medido: que `state check` no dependa de pytest. | HECHO + SUPUESTO ELEGIDO (la ganancia) | CAMBIA EL PLAN | Makefile (`check: desellar contrato lint types contracts test state config knowledge sellar`); `tests/unit/test_sello_make_check.py:184-190`; ENTORNO-CODE.md:147; ERRORES-RECURRENTES.md:122 | e | Que `state check` o `knowledge validate` necesiten el resultado de `test` | SIN PASADA |
| X-09 | X | `guardia.py` pesa 289.378 B, 6018 líneas, 165 funciones. Doce merges la tocaron; 46 commits desde el 2026-10-01; 7 desde el 2026-11-09. Sus tests (7 ficheros) pesan 290.707 B. La familia 3 («lo que se ejecuta es lo que se leyó») ocupa unas 2190 líneas (36 %); la espera a la CI, 404 (6,7 %, proceso puro); git, rm y make, 653 (10,8 %); el tokenizador, 611. La cabecera dice «defensa en profundidad» (`guardia.py:3-6`). `settings.json` solo deniega git, rm y herramientas (`:9-58`). No encontré ADR de la familia 3. | HECHO; la reestructuración es PREGUNTA PENDIENTE (ingenieros) | CAMBIA EL PLAN | `git log --first-parent -- .claude/hooks/guardia.py`; `wc -c`; marcas `# ----` de guardia.py; `grep -l guion-mismo-comando docs/adr/*.md` vacío; informes GUARDIA-*, GUION-MISMO-COMANDO y GUARDIAS-HOLDOUT suman 1,08 MB | d, e, f | Un ADR de la familia 3 que no encontré | SIN PASADA |
| X-11 | X | El cierre exige como mínimo 3 `make check` sellados más una CI de Linux, unos 81 min solo en el ritual. RITUAL.md 26.303 B y 18 «Puerta»; `cerrar-rama` 8.633 B; HISTORIA.md 2.717.867 B con 80 `# Archivo` y 80 `# Registro de cierre`; PROJECT_STATE.md 24.680 B de 25.000. | HECHO + aritmética | CAMBIA EL PLAN | RITUAL.md:113-140, :185-195, :309-322; `wc -c`; `grep -c` sobre HISTORIA | e, f | Que el `docs(state)` de `main` pueda sellarse sin `make check` completo | SIN PASADA |
| K-04 | K | **La deuda de las cotizaciones sin tick (PS:138) se ve en la línea base vigente.** 5 de las 25 esperas caen en una de las 18 horas perdidas (2,63 % de 684; se esperarían 0,66, aritmética sobre cifras publicadas). En esas horas el lado malo se juzga con el cierre de la M1 anterior más el spread p90. Lo mismo decide los 7 «no colocables» del techo; no se midió cuántos caen en horas perdidas. Remedio barato: en enero, la segunda pasada de descarga bajó de 31 a 5 horas perdidas; pero los manifiestos son inmutables: dataset nuevo y línea base nueva. | HECHO + aritmética | CAMBIA EL PLAN | HISTORIA.md:20733-20737; RECORRIDA-CONSTRUCCION-3.md:108-115; ENTRADA-ENERO.md:172-173, :529, :533-535; llenado.py:99-119; ACTIVAR-SESION-08.md:491-493; PS:138, :159 | c, d, f | Que las esperas se concentren por hora de sesión, o que con tick real el 0 siguiera del lado malo | MATIZ (matiz en §3/§9) |
| K-06 | K | **La M de la Next Action («sin objeto mientras `break_even_condicion` sea cierre») la contradice la corrida (3).** Los 19 cierres a BE de ventas pierden en bruto. De los 31 de compras, 18 cierran exactamente a 0,00. ADR-0065 §6 daba por supuesto que el BE al cierre de la M1 daba 0. Al menos una venta salta 2,5 s después de mover el stop (12:17:59.999 → 12:18:02.481, 2026-04-02) y otra a los 20 s. | HECHO (recuentos de un fichero publicado) | CAMBIA EL PLAN | PROJECT_STATE.md:44; ACTIVAR-SESION-07.md:238; ADR-0065:80-93; cuenta-por-mes.txt:3129-3364, :1623 con :3209, :1863 con :3311 | c, d, f | Ticks que den el ASK por debajo de la entrada al mover el stop en los 19 | MATIZ (matiz en §3/§9) |
| D-04 | D | Un «mes nuevo con vídeo» choca con la reserva por número de mes y con los meses de 2025 ya reservados. El repo lista como reservados (por ADR o por documento) los números 2, 3, 5, 6, 9, 10, 11 y 12. Libres: enero, abril, julio y agosto, que ya son construcción. Y 2025-01 a 2025-11 están todos en `meses` o `extension` de rentabilidad. Un mes nuevo de otro año con número libre es posible; uno de número reservado no entra como construcción sin ADR y código. | SUPUESTO ELEGIDO (inferencia mía; no leí `meses_reservados.yaml`, no me lo permite 2.1) | CAMBIA EL PLAN | `holdout.py:620-640` (tapados = número de mes); ADR-0092:137-139; `criterio_fidelidad.yaml:84-85`; ADR-0096:57; REGISTRO-MARZO.md | a, f | Contraste de los números del fichero que yo no puedo leer | SIN PASADA |
| D-05 | D | La copia de seguridad (A.4) lleva vencida desde antes de la 7b; falta v18 a v21. Marzo, diciembre, el vídeo de mapeo y las 7 imágenes de marzo viven en `corpus/` y `data/`, fuera de git y en una sola máquina. | HECHO | CAMBIA EL PLAN | HOJA A.4 (743-746); PS:135; AUDITORIA-2026-11-21.md:107; ADR-0098:211-212 («viven en `data/`, en la laptop de Aleks») | e, f | Que Aleks suba v18-v21 con su SHA256SUMS | SIN PASADA |
| D-06 | D | La «rama del puente sobre construcción» y «la cancha» de la pregunta no existen en el repo. El puente en vivo de Python a MT5 está descartado por ADR-0082 §4 y por la enmienda del 2026-11-10 de RUMBO (solo lo abre un ADR nuevo). | HECHO | CAMBIA EL PLAN | `git grep -i cancha` vacío; RUMBO-2026-11.md:37-43; HOJA R7.3 (680) | a, c, d | Una rama o ADR que defina «puente sobre construcción» o «cancha» fuera del repo | SIN PASADA |
| D-07 | D | Febrero, el único mes limpio, nadie lo ha pedido todavía y F26 lo gasta de una vez. holdout-1 queda cerrada mientras tanto. La opción 1 no lo gasta; la 3 no lo gasta por diseño (ADR-0092:129-130). | HECHO | CAMBIA EL PLAN | ADR-0096:57; PS NA:G; PREREGISTRO.md:135-137 | b, f | — | SIN PASADA |
| D-08 | D | La sombra en diferido (R7.3) gasta cada día enseñado como material ciego y hoy está bloqueada: `motor laminas` niega todo día que no sea dev, los ticks solo se descargan de construcción y un manifiesto nuevo con el prefijo del kit cambia el universo (HER:9). | HECHO | CAMBIA EL PLAN | HOJA R7.3 (680) | c, d, f | — | SIN PASADA |
| D-11 | D | El vídeo de mapeo se cita solo por referencias («SIN ABRIR y fuera del repo»), y PREPARACION-SESION-7 dice que no había llegado al revisarla. No sé qué mes cubre ni si trae material de un mes nuevo. | PREGUNTA PENDIENTE (dueño: Aleks) | CAMBIA EL PLAN | PS NA:F; PREPARACION-SESION-7.md:650, 1022 | b, f | Que Aleks diga el mes y si trae backtest | SIN PASADA |
| I-02 | I | El Anexo B no recoge la meta de ADR-0098 ni su salida C: describe el ciclo «corrida en julio → láminas → sesión», hoy parado. | HECHO | CAMBIA EL PLAN | AUDITORIA-2026-11-21.md:362-364 frente a HOJA-DE-RUTA.md:438-442 y ADR-0098 §3 C | d, e, f | Que el Anexo B se actualice | SIN PASADA |
| I-03 | I | R6.0 sigue diciendo que Python en vivo se descarta «por el tope de peticiones»; la razón cayó con la respuesta de FTMO del 2026-11-20 (recuadro de ADR-0082). R6.0 y RUMBO §4 no llevan el recuadro. | HECHO | CAMBIA EL PLAN | HOJA-DE-RUTA.md:635-637, :641 frente a :719-725 y ADR-0082:101-114; RUMBO §4 | d, e, f | Otra parte de R6.0 que ya lo recoja | SIN PASADA |
| I-04 | I | El recuadro de ADR-0082 mantiene tres razones para el EA y descarta una; ningún documento de entrada lo resume. Las condiciones de FTMO son paráfrasis del consultor. | PREGUNTA PENDIENTE (los ingenieros; decide Aleks) | CAMBIA EL PLAN | ADR-0082:101-114; HOJA-DE-RUTA.md:725 | d, e | Un ADR de Aleks antes del 2026-12-03 | SIN PASADA |
| I-05 | I | «La cancha» no es un término del repo (grep vacío en hoja, ADR-0098, PROJECT_STATE, RUMBO). Lo que existe es F17 en una prueba gratuita (R5.7, A.5); el grabador está PARCIAL. | HECHO | CAMBIA EL PLAN | `grep -n cancha` vacío; HOJA-DE-RUTA.md:438-441, :892 | c, e | El término en otro documento | SIN PASADA |
| I-06 | I | Los tres meses fijos de F34: no hay documento que diga qué se les pregunta exactamente. | PREGUNTA PENDIENTE (ingenieros y Aleks) | CAMBIA EL PLAN | MASTER_PLAN.md:147; ADR-0098:222-231 | c, e, f | Una nota que fije el planteamiento | SIN PASADA |
| I-07 | I | C4 sin resolver ni cuantificar: la CI corre `make check` en Ubuntu sin `data/`; skips verificables, al menos 9 líneas; «más de 15» no confirmado. La CI no se dispara en `trabajo/*` (solo main, feature/** y fix/**). | HECHO (9) / SIN COMPROBAR (15) | CAMBIA EL PLAN | AUDITORIA-2026-11-21.md:167; ci.yml; `git grep -n "skip" -- tests` filtrado por data, corpus o material = 9 | e, f | Un `pytest -rs` en Linux sin `data/` | SIN PASADA |
| P1-02 | P1 | La afirmación del consultor sobre la pieza 3 es cierta, con matiz: el objetivo queda a ≥3,75·S (hasta +3 puntos por ROUND_UP; con S=10 sale a 3,9); el stop también es un 25 % más ancho, así que la relación es la misma; la comisión por R de una misma operación es 0,8 veces | HECHO | MENOR | `techo_parejas.py:107-117`; `test_techo_parejas.py:168-170`; `viabilidad_comision.py:72-79` | d | Que el objetivo se fijara sobre la distancia del stop | SIN PASADA |
| P1-03 | P1 | `caja_derivada` con ROUND_UP no invierte la regla del bot, stop = ceil(0,8·caja): si S no es múltiplo de 4 la caja sale un punto mayor y el objetivo +3 puntos. El guion cumple ADR-0098 §1 al pie de la letra; quien no es coherente con «la misma regla del 0,8 que usa el bot» es el ADR | HECHO | MENOR | `primitivas_broker.py:493`; `techo_parejas.py:107-111`; `test_techo_parejas.py:168`. Llamada que pido al orquestador: `caja_derivada(S, Decimal("0.8"), ROUND_UP)` y después `int((Decimal(c)*Decimal("0.8")).to_integral_value(ROUND_UP))` para S de 8 a 20. Espero que devuelva S solo si S%4==0, y S+1 en el resto | a, d | Esa salida | SIN PASADA |
| P1-06 | P1 | El +0,56 de la anotada promedia las 77, porque el bucle del R no filtra. El filtro de :217 solo alimenta la cuenta (veredictos y peor día) | HECHO | MENOR | `viabilidad_comision.py:208-218,310-326` | a | — | SIN PASADA |
| P1-11 | P1 | El techo tira las no colocables (7). El bot, desde ADR-0097, espera. V2 abre todas | HECHO | MENOR | `techo_parejas.py:537-542`; ADR-0097 §1:18-22 | a, d | — | SIN PASADA |
| P1-12 | P1 | El cierre al fin de la H4 de RN-002 entró después de V2. En V2 solo se cierra al final de la ventana | HECHO | MENOR | ADR-0060 (fecha 2026-09-30); `parametros.yaml:399-416`; `viabilidad_comision.py:197-200` | d | — | SIN PASADA |
| P1-15 | P1 | Los intervalos de V2 son del 95 % por operación; los del techo, una banda del 90 % por días. No son comparables | HECHO | MENOR | `viabilidad_trader.py:54-55,89-98`; `criterio_fidelidad.yaml:74-76` | a | — | SIN PASADA |
| P1-16 | P1 | ADR-0098 §5:202 dice «con el motor de septiembre». VIABILIDAD no usa el motor, solo `Broker` y `evaluar_fase`, con un 3 literal | HECHO | MENOR | `viabilidad_comision.py:77-83,122-206` | a | — | SIN PASADA |
| P1-18 | P1 | Arrastrada frente a una por mes: no mueve el R en ninguno de los dos | HECHO | MENOR | `viabilidad_comision.py:151-167`; `techo_parejas.py:481-485` | d | — | SIN PASADA |
| P1-19 | P1 | En abril y agosto, el «UTC+2 fijo» coincide con la hora de verano de Madrid. El reloj solo cambia enero | SUPUESTO IMPUESTO POR EL MUNDO (fuente: la tz Europe/Madrid; ADR-0069) | MENOR | CLAUDE.md, «Que se puede mirar»; ADR-0069 | d | — | SIN PASADA |
| P1-20 | P1 | Lo que cambió en el bróker desde V2 solo toca los minutos sin ticks | HECHO | MENOR | `git log stable/F29-viabilidad-comision..HEAD` sobre broker y llenado; METODO…:875,877 | d | — | SIN PASADA |
| P2-05 | P2 | **Deja correr: indicio fuerte en el material.** Siete ganadoras de abril y agosto salen entre 4,15 y 5,33 veces el stop del libro. Aun con el stop en el 0,8, cuatro quedan claramente más allá de 3 cajas. VIABILIDAD-TRADER las llama «el trader deja correr» (5 de 73). El trader dijo en los primeros vídeos que maximiza en M15 y que protege «poco a poco» (`ev-v3-003742-d38f9694`, `ev-v3-003220-8805194d`, `ev-v3-003318-f1a2d27d`, `ev-v1-002608-7daa95ae`). En la sesión 4 dijo que «lo han dejado… por ahora». A-33 y A-56 solo cubren las ganadoras que cierran **por debajo** de 3R | HECHO (las siete) + PREGUNTA PENDIENTE (el trader) | MENOR | `ACTIVAR-SESION-03.md:154-185`; `VIABILIDAD-TRADER.md:182`; `ambiguedades.yaml:937-947` y `1927-1942`; `docs/sesion-4/PREGUNTAS.md:220-235`; `ADR-0073:26-30` | a, b, c | Que el trader diga que sus libros son posteriores a que dejó de extender. Aritmética sobre cifras publicadas: exceso de las siete sobre 3,75 = 5,94 R y sobre 3,00 = 11,19 R; entre 77 operaciones son 0,08 a 0,15 R por operación, sobre la esperanza bruta anotada de +0,98 (`VIABILIDAD-TRADER.md:96`) | MATIZ (matiz en §3/§9) |
| P2-08 | P2 | La pregunta 16 de la sesión 4 dice que «el último en fecha (el vídeo) es el que se saltó operaciones de break even». Lo contrario dicen S-14 (sesión 5), Aleks en v16 y el propio trader en S-16. La pregunta se redactó con la premisa al revés | HECHO | MENOR | `docs/sesion-4/PREGUNTAS.md:269-272`; `SESION-05-EXTRACCION.md:785-787,1107-1110`; `ev-v10-014823-64248489` | b | Que la hoja realmente leída dijera otra cosa | SIN PASADA |
| P2-09 | P2 | A-40 («stop quieto tras el BE») se cerró con una respuesta a «¿parciales?». Hay dos ítems laterales que dicen que protege «poco a poco si veo un flujo de velas alcistas» (`ev-v3-003220`, `ev-v3-003318`). La spec dice «no se mueve» y no hay pregunta directa | PREGUNTA PENDIENTE (el trader) | MENOR | `SESION-03-EXTRACCION.md:466-475`; `ambiguedades.yaml:1232-1262` | b | Que el trader diga «una vez en BE, el stop no se vuelve a tocar» | SIN PASADA |
| P2-10 | P2 | `gestionar_salida` (RN-010, «proteger a 0.80») no aparece en `src/` ni en `tests/` (solo `strategy_spec.yaml:492,1640`); la tabla de acciones del cableado no la incluye | PREGUNTA PENDIENTE (los ingenieros) | MENOR | `primitivas_broker.py:842-857`; `git grep -n "gestionar_salida" -- src tests` sin resultados | e, f | Que la acción venga de otro fichero o el intérprete la trate como hueco declarado | SIN PASADA |
| P2-12 | P2 | `VIABILIDAD-TRADER.md:181` dice del BE-a-cero «el trader subió el stop a la entrada, y eso no está documentado». Ya está documentado: RN-014 desde la sesión 1. El informe está cerrado y no se toca | MATIZ | MENOR | `VIABILIDAD-TRADER.md:181`; `strategy_spec.yaml:1798-1858` | f | — | SIN PASADA |
| P3-05 | P3 | **Las 7 no colocables, cómo se deciden.** El pedido entra en el minuto del llenado truncado y se juzga en `instante*60000−1` con `lado_equivocado_al_colocar`. Sin ticks, se usa la M1 k−1. La espera de ADR-0097 se aplica al bot y no al trader. El control no prueba las piezas solo del trader. | SUPUESTO ELEGIDO | MENOR | `techo_parejas.py:504-505, :537-542, :807`; `broker.py:558-571`; `llenado.py:274-283`; `RECORRIDA-CONSTRUCCION-3.md:185-187, :1085`; ADR-0097 §1 | a | Que la salida por no colocable las explique todas por una causa ajena a serie e instante | SIN PASADA |
| P3-06 | P3 | **Cota de las 7 (aritmética sobre cifras publicadas).** 191 × (−0,239) = −45,65. Las 7 ganadoras a +3,75 R dan −0,098. Con el redondeo de la caja (objetivo hasta 6 R con d=1), 7 × 6 R da −0,018. Las 7 perdedoras a −1 R dan −0,266. Ningún caso llega a 0, y d) y e) no cambian. | HECHO | MENOR | `meta.txt:9-13`; `techo_parejas.py:107-117, :554-555`; `parametros.yaml` | a | Un error en N o en la media publicados | SIN PASADA |
| P3-10 | P3 | **Trampa confirmada:** `lista-s14.txt` y `lista_s14.py` son las sesiones P6 de la corrida 2, material para preguntar. No miden el sesgo. | HECHO | MENOR | `anexos/RECORRIDA-CONSTRUCCION/lista_s14.py:1-5` | b | — | SIN PASADA |
| P3-11 | P3 | **Filas sin `initialSL`.** 17 de 215 filas de los libros de construcción (enero 4, abril 3, julio 5, agosto 5) se caen en la ingesta. «sin stop: 0» del techo cuenta casos, no filas. | HECHO; PREGUNTA PENDIENTE (el trader) | MENOR | `ENTRADA-ENERO.md:502, :509`; `VIABILIDAD-TRADER.md:35`; `ENTRADA-JULIO.md:569, :577-578`; `meta.txt:9`; `RELOJ-INVIERNO.md:152, :159, :167`; `libros.yaml:77` | b | El trader dice que son filas de otro tipo | SIN PASADA |
| P3-14 | P3 | **Relojes: no queda desfase de horas.** Libros en UTC (enero, abril, agosto) y Europe/Madrid (julio), medidos por velas; sesiones por la rejilla H4; «fuera de la ventana: 0». Residuo de segundos: el techo trunca al minuto y coloca en el cierre de la M1 anterior, mientras Dukascopy toca la entrada antes de t (mediana −2,4 s, mínimo −51,4 s). Sin ticks, la cotización es la M1 k−1; 8 operaciones no tienen ticks en su minuto. | HECHO | MENOR | `libros.yaml:20-21, :32-33, :56-57, :71-79`; `RELOJ-INVIERNO.md:153-171, :309-312`; ADR-0069 §1-§3; `meta.txt:9`; `INSTANTE-LLENADO-SALIDA.txt:5`; `INSTANTE-TICKS-SALIDA.txt:9-10`; `ORDEN-STOP-O-LIMITE.md:111-117`; `broker.py:562-564`; `METODO-FIDELIDAD-RENTABILIDAD.md:878`; PROJECT_STATE.md:116 | a, f | Un libro cuyo huso medido no casa con el declarado | SIN PASADA |
| P4-07 | P4 | Las muestras de la demo son con 0,01 y 1,00 lotes. El bot lleva unos 22 lotes de media (26.213,00 USD de comisión / 235 / 5) y hasta el tope de 50: F17 tiene que medir con esos lotes | PREGUNTA PENDIENTE (F17; FTMO) | MENOR | ADR-0090:104-106; resumen-cuenta-por-mes.txt:74-77 (aritmética sobre cifras publicadas); perfil :286-302 | c | Que el deslizamiento no dependa del volumen en FTMO, medido | SIN PASADA |
| P4-10 | P4 | El techo recorta el lote de los stops cortísimos, no los excluye (ADR-0081 §2). Esas operaciones pagan 5/D en R: con 3-5 puntos, 1-1,67 R. VIABILIDAD-COMISION excluía las de más de 100 lotes (10 en V2 con 5 USD). Su +0,47 y el −0,239 del techo no tienen la misma población de costes | HECHO | MENOR | broker.py:188-220; meta.txt:9 («fuera por el lote minimo: 0»); VIABILIDAD-COMISION.md:11-13,87-94; VIABILIDAD-TRADER.md:80-83 | a, e | Una distribución de D del techo sin stops por debajo de 10 puntos | SIN PASADA |
| P4-11 | P4 | El swap no cuesta nada: ninguna posición cruza la medianoche. El simulador lo cobra en `huso_corte`, no en el rollover del servidor, y no tiene efecto | HECHO | MENOR | ADR-0090:209-229 | e | Que una regla deje posiciones abiertas de noche | SIN PASADA |
| P4-12 | P4 | `cerrar_a_mercado` no aplica `deslizamiento_fijo_puntos`, y las stops sí. ADR-0092 §4 cuenta los cierres a mercado como afectados. Si la cifra de F17 entrara por llenado.yaml y no por la relectura, se saltarían | HECHO | MENOR | broker.py:644-656; llenado.py:242,261,327,354,391-393; criterio_fidelidad.py:830-832 | c | Que la cifra de F17 entre solo por `veredicto_con_f17` | SIN PASADA |
| P4-13 | P4 | `curva_con_deslizamiento` y `veredicto_con_f17` toman una sola curva y arrastran `previo` de una cuenta a otra. Hay que arreglarlo antes de releer d) y e) por cuenta. Es deuda ya anotada | HECHO | MENOR | PROJECT_STATE.md:100; criterio_fidelidad.py:842-866 | c | — | SIN PASADA |
| P4-15 | P4 | Si la comisión cambia con el tipo de cuenta (Swing frente a Standard) y qué aclara el asterisco de «USD/LOT*», no está en el repo | PREGUNTA PENDIENTE (FTMO; Aleks, HER:27) | MENOR | PROJECT_STATE.md:58 (heredado 27); FTMO-REGLAS.md:59 | a | Una respuesta de FTMO | SIN PASADA |
| P5-05 | P5 | Los números publicados del techo del trader en construcción son negativos. Aritmética no hecha: son cifras ya publicadas. N = 191; esperanza −0,239 R; percentiles 5 y 95 = −0,450 y −0,026; en julio, N = 64 y −0,245 (percentil 95 = +0,085). Lectura «no_gana», salida C. Con el 5 % de deslizamiento por llenado la cifra no se arregla: haría falta −2,52 puntos. | HECHO (backtest, no real) | MENOR | `RECORRIDA-CONSTRUCCION-3.md:683-693, 695-698, 712-713` (el informe más reciente que las publica, el de la rama `recorrida-construccion-3`, con tag stable/F39l). Hay 79 break even movidos en 198 operaciones. | a | Que con costes reales de FTMO la cifra cambie (F17) o que el libro del trader tenga una serie de precios distinta | SIN PASADA |
| P5-07 | P5 | Lo que sí contestó sobre su real: sobre el lote que no cabe, «no ha vivido el caso en su cuenta»; «en real simplemente no puedes obviar [los break even]» (en el backtest los excluye del muestreo de stats). | HECHO (cita de su voz) | MENOR | `docs/validation/SESION-05-EXTRACCION.md:467-478` (S-5, ADR-0081; la respuesta viene tras la del consultor, que se atribuye por contexto). `SESION-07-EXTRACCION.md:471` (S-6, v18, `ev-v18-003808-c08babd3`). | b | — | SIN PASADA |
| P5-08 | P5 | Aviso de procedencia: «el trader SÍ opera noticias en cuentas propias» y «su estrategia funciona dentro del evento» está en el MASTER_PLAN como hecho; sale de la voz del trader (v6, 2:00:29), no de resultados. Nadie lo midió. | SUPUESTO IMPUESTO POR EL MUNDO (sin fuente de medida) | MENOR | `docs/plan/MASTER_PLAN.md:302` (entrada del 2026-09-12 sobre ADR-0022). | b | — | SIN PASADA |
| P5-09 | P5 | La sesión 7 declara que el trader «no dio cifras de resultados de su cuenta» en pantalla. Confirma que no se le preguntó por resultados reales. | HECHO | MENOR | `SESION-07-EXTRACCION.md:80`. | b | — | SIN PASADA |
| P6-12 | P6 | Una prueba gratuita dura 14 días naturales; una activa a la vez; se puede repetir. Hoy no hay ninguna viva. R4.7 depende de que la haya. | HECHO | MENOR | DEMO-FTMO.md:189-190, :162; HOJA:756, :920, :440 | c | Una prueba viva declarada | SIN PASADA |
| P6-18 | P6 | `motor laminas` niega todo día que no sea dev de construcción. RUMBO §3 da por hecho que el caso «nunca ocurre»; con la cancha ocurre. | HECHO | MENOR | cli.py:2742-2755; RUMBO:33 | c, d | — | SIN PASADA |
| P6-21 | P6 | Heredado 9. El M1 de FTMO necesita un prefijo propio: un manifiesto nuevo con el prefijo del kit cambia `universo()`. | HECHO | MENOR | HISTORIA.md:701; ADR-0092:149-151; arnes.py:208; simulacion.py:200 | d | — | SIN PASADA |
| P6-22 | P6 | Lo que falta para la vía (ii): no hay puente; MetaTrader5 no es dependencia. El tope de peticiones no aprieta: la corrida (3) da un máximo de 68 al día frente a 2.000. De ADR-0082 sigue en pie una razón: una capa en Python habría que tirarla en F29. | HECHO | MENOR | mql5bridge/journal.py:1-30; pyproject.toml:7-27; RECORRIDA-CONSTRUCCION-3.md:495-496; ACTIVAR-SESION-08.md:638-639; ADR-0082:111-113 | e | — | SIN PASADA |
| P7-05 | P7 | El techo ya excluye el cero en su lado: p95 = −0,026 < 0. Con N=191 (≥ 100) la salida C no depende de falta de muestra; la depende de la esperanza < 0 y del p95 < +0,10 (ADR-0098 §2). Pero el p95 queda a 0,026 R del cero: con el ET de 0,129, un +0,05 R de error de modelo (p. ej. el desfase) lo cruza. | HECHO | MENOR | `meta.txt` línea c, ADR-0098 §2 (líneas 105-108) | a) | Un recálculo con desfase y límite de 100 lotes que cambie el signo | MATIZ (matiz en §3/§9) |
| P7-08 | P7 | La diferencia emparejada de las parejas (+0,198 R bot−trader, p5-p95 −0,132 a +0,592) con 29 parejas es compatible con 0: ET ≈ 0,22, desviación por pareja ≈ 1,19. Y la lectura «ni una cosa ni otra» de ADR-0098 §2 refleja exactamente eso. | HECHO (aritmética sobre cifras publicadas) | MENOR | `meta.txt` bloque M2; ADR-0098 §2 | a) | N de parejas muy mayor | SIN PASADA |
| P7-09 | P7 | El techo de julio (64 operaciones) tiene p5-p95 de −0,546 a +0,085: incluye el cero. Su «no gana» en julio no se sostiene solo; lo hace el conjunto de 191. Es diagnóstico sin umbral (`meta.txt`). | HECHO | MENOR | `meta.txt` bloque julio | a) | — | SIN PASADA |
| P7-10 | P7 | El remuestreo por operación de V2 probablemente subestima la varianza frente al remuestreo por días, porque las operaciones de un mismo día no son independientes. El tamaño del efecto no está publicado. Un V2 «por días» tendría un intervalo más ancho que [−0,13; +1,08]. | SUPUESTO IMPUESTO POR EL MUNDO (sin fuente) | MENOR | `viabilidad_trader.py:95-98` (sortea `rs` sin agrupar) | a) | Calcular el V2 por días (ejecuta el guion, que carga velas: fuera de esta auditoría; ver §9) | SIN PASADA |
| P7-11 | P7 | Dónde mirar para saberlo: `VIABILIDAD-COMISION.md` no es el último informe de V2 ni de la serie del trader; ADR-0098 §5 declara «Ningún informe posterior rehace la construcción entera» y que el R de las parejas del bot no estaba publicado. No encontré otro informe commiteado con un R del trader distinto de +0,47/+0,56 (grep de «0,47» solo da VIABILIDAD-COMISION, VIABILIDAD-TRADER, ABRIL-Y-LA-CAJA y ADR-0098; el de ABRIL-Y-LA-CAJA es un +0,47 de desviaciones típicas, otra cosa). | HECHO | MENOR | `grep -ln "+0,47\|0,47 R"` en docs; `ABRIL-Y-LA-CAJA.md:353` | f) | — | SIN PASADA |
| S-07 | S | **El objetivo exige superar el nivel (DN-1), el stop salta al toque; no medido en FTMO** | SUPUESTO ELEGIDO, conservador | MENOR | `0051:34-39`; `llenado.yaml:6`; `llenado.py:331` frente a `:322` | b, c | Contar cuántas ganadoras tocaron el objetivo exacto sin pasarlo (declarar) | SIN PASADA |
| S-09 | S | **Las 7 no colocables y las 0 no llenadas son consecuencia de colocar un minuto antes del llenado** | HECHO + SUPUESTO ELEGIDO | MENOR | `meta.txt:9`; `techo_parejas.py:19-24`; `ambiguedades.yaml:321-325` | b | Ver las 7 por causa, sin R | SIN PASADA |
| S-10 | S | **El bróker simulado sigue con supuestos PROVISIONALES que la demo no ha cerrado** | SUPUESTO ELEGIDO, PROVISIONAL | MENOR | `0057:37-46`; `0090:130-182`; `0053:89-93`, `:173-177`; PS:84 | d, f | R6a (journal) | SIN PASADA |
| S-13 | S | **La Technical Debt señala dos supuestos con efecto bajo** (spread sin ticks por hora de pared; cotizaciones sin tick) | SUPUESTO ELEGIDO, deuda declarada | MENOR | PS:116, PS:138; `RECORRIDA-CONSTRUCCION-3.md:107-120` | f | — | SIN PASADA |
| S-14 | S | **Texto viejo**: ADR-0057 §5 dice «UNKNOWN» para `firma_stops_level_puntos`, CONFIRMED 0 desde ADR-0071 | HECHO | MENOR | `0057:7-15`, `:69-72` frente a `cuentas yaml:444-458` | f | — | SIN PASADA |
| R-01 | R | La sesión siguiente se «prepara» pero no se «graba»; en el repo la frase aparece en HOJA:432, :435, ADR-0098:147-148, PS:28 y RECORRIDA-3 PARADA 2 (:1127-1128). Ningún documento activo dice lo contrario | HECHO | MENOR | PS:28; HOJA:432-435 | a, f | Un documento posterior que ordene grabar | SIN PASADA |
| R-04 | R | MASTER_PLAN.md no tiene ninguna NOTA que cite ADR-0098; sus NOTAs llegan a ADR-0096 (:28-36) | HECHO | MENOR | MASTER_PLAN:3-36 | f | — | SIN PASADA |
| R-12 | R | Las tareas de Aleks de R4.7 (probar F17 en una cuenta, contrastar la premisa con el trader) no tienen entrada en el «Carril: lo de Aleks»; A.5 está bajo «guardias y deuda» (HOJA:750-758). El contraste con el trader no tiene entrada | HECHO | MENOR | HOJA:437-443, :686-758 | b, c, f | — | SIN PASADA |
| R-15 | R | A-43 estaba en la F vieja («por WhatsApp: si no contesta antes, (3) corre con el valor de hoy», HISTORIA:20740) y la F nueva no la recoge; sigue abierta (PS:67). A-35 (bloqueante) va por WhatsApp (PS:136). La salida C pide que Aleks contraste con el trader: no hay ninguna instrucción de si esos mensajes van antes, a la vez o después | PREGUNTA PENDIENTE (Aleks, consultor) | MENOR | HISTORIA:20740; PS:28, :67, :136 | b | — | SIN PASADA |
| R-16 | R | A-16 se pide «revisar» en C, pero ya se midió (mediana 0 puntos, 92,4 % dentro de la M1; HOJA:281-282) y sigue ABIERTA con regla (ADR-0092 §9-§10); el PS (:65) la deja en F26. R4.7 no dice qué queda por revisar | HECHO | MENOR | HOJA:281-282; PS:65; ADR-0092:244-264 | a, b | — | REFUTADO (por el orquestador en el contraste: METODO-FIDELIDAD-RENTABILIDAD.md:888-893) |
| R-17 | R | El techo y las parejas dieron: 7 operaciones del trader no colocables sobre 198 (191 llenadas y cerradas) y 29 parejas con 1 sin pata del trader (meta.txt). El techo es un diagnóstico de construcción (cuatro meses, 76 días), no un hecho de 2025 | HECHO | MENOR | meta.txt | a | — | SIN PASADA |
| R-19 | R | A.4 tiene un plazo («antes de grabar la próxima sesión») que C difiere; no se cumple ni se actualiza, y sigue ABIERTA con v18-v21 sin copiar (PS:135; HOJA:743-746) | HECHO | MENOR | HOJA:743-746; PS:135 | f | — | SIN PASADA |
| M-02 | M | El salto de 3,5 a 15,7 % del Marcador viene del método (cuenta por mes), no del bot: la diaria pasó de 20,7 a 20,2 y a 20,2. La columna «que cuenta» se lee como progreso y no lo es. | HECHO | MENOR | `HOJA-DE-RUTA.md:908-910`; `RECORRIDA-CONSTRUCCION.md:644-648`; `AUDITORIA-2026-11-21.md:45-46` | f | Una diaria que también saltara entre R1 y R2 | SIN PASADA |
| M-07 | M | La cobertura de ADR-0043 cuenta como pareja una operación con otro stop: 30 parejas T0 frente a 14 «cuatro piezas» (14/198 = 7,1 %). La diferencia no está descompuesta. | HECHO | MENOR | `criterio_fidelidad.py:53-55`, `:115-119`; `RECORRIDA-CONSTRUCCION-3.md:463`, `:480`; `docs/adr/0043-…md:34-40` | a, e | Descomponer las 30 en la cascada | SIN PASADA |
| M-11 | M | Las parejas no concluyen: N = 29, intervalos que cruzan el 0, selección por coincidencia, la pata del bot con su propio stop, y las dos negativas. No prueban que el bot gane al trader. | HECHO | MENOR | `meta.txt:30-36`; `techo_parejas.py:936-954`; `docs/adr/0098-…md:113-122` | a, f | Más parejas con el percentil 5 de la diferencia por encima de 0 | SIN PASADA |
| M-16 | M | La columna «Operaciones de más» del Marcador (321) cuenta órdenes sin operación del trader, no las operaciones de más del pivote. Está documentado, pero el encabezado engaña. | HECHO | MENOR | `HOJA-DE-RUTA.md:905`; `PIVOTES-SESION-7.yaml:25-28`; `docs/adr/0093-…md:151-152` | f | — | SIN PASADA |
| M-17 | M | El embudo no nombra RN-032. Las 12 sesiones de julio bloqueadas salen como «todos los hechos del camino producidos», y 2 sesiones de RN-032 sin operaciones del trader no se pueden localizar. | HECHO | MENOR | `anexos/.../cuenta-por-mes.txt:887-889`; `RECORRIDA-CONSTRUCCION-3.md:578-581` | e, f | — | SIN PASADA |
| X-02 | X | 153 commits en 16 ramas (media 9,6). Guardias y proceso: 35 en 5 (7). Fidelidad: 111 en 10 (11,1; `laminas` 24). Por commits, las guardias son el 23 %. Desde 2026-11-09 hay 169 commits sin merges: 90 `docs`, 35 `chore` (16 `chore(cierre)`), 22 `fix`, 16 `feat`, 5 `data` y 1 `spec`. | HECHO | MENOR | `git rev-list --count <merge>^1..<merge>^2` en 16 merges | e | Contar con otra fecha de corte | SIN PASADA |
| X-10 | X | Las negativas de la guardia no tienen registro central (75 menciones en docs/validation; 42 informes). En esta auditoría me negó 3 comandos (`tac`, un `$(...)`, un `:` de relleno), errores míos de forma; ninguno tocaba material protegido. | HECHO (menciones, no negativas únicas) | MENOR | `grep -rhoi` = 75; `grep -rli` = 42 | e | Un contador real en el hook | SIN PASADA |
| K-01 | K | **La caja derivada del trader no es inversa de la regla del bot.** El guion deriva caja = ⌈d/0,8⌉; el bot pone el stop en ⌈0,8·caja⌉. Si d no es múltiplo de 4, la caja derivada lleva el stop a d+1 y el objetivo hasta 3 puntos más lejos que con la única caja coherente (d=10: caja 13, objetivo 39; la coherente 12, objetivo 36). El test consagra el caso. Cumple la letra de ADR-0098 §1 («redondeado alejándose»), no su «misma regla del 0,8 que usa el bot». El control no lo ejerce. | HECHO | MENOR | techo_parejas.py:107-111, :806, :554; primitivas_broker.py:493; test_techo_parejas.py:168; ADR-0098:39-41, :67; parametros.yaml:677-695, :1759-1782 | a, e | Que el consultor diga que la caja se redondea hacia arriba a propósito | SIN PASADA |
| K-02 | K | **Ramas de `repetir()` que no ejerce el control ni ningún test.** Sin ejercer: «fuera de ventana» (:495-500), la cancelación al fin de sesión (:531-536), el lote mínimo (:551-553), los rechazos al colocar y al llenar (:564-566, :584-589), dos posiciones vivas con BE en cada una (:512-513, :523-530) y el manual fuera de control (:514-517). La rama `< primero` mueve la orden y la cuenta como «fuera», aunque puede entrar en el R. Solo las usa el trader: no colocable (7), la colocación en el minuto del llenado menos uno (:807-812) y `fin_minuto` con valor. Sí las ejerce el control: el BE en los dos lados (50 cierres a BE: 31 compras, 19 ventas), el lote limitado (176 de 235), RN-002 (6 manuales) y el respaldo. El test solo prueba piezas puras y `make check` no lo recoge. | HECHO | MENOR | meta.txt:9-11; cuenta-por-mes.txt:3129-3364 y :1990-3000; test_techo_parejas.py:64-192; README:78-80; pyproject.toml:38 | a, e | Un test de `repetir` con mercado sintético | SIN PASADA |
| K-03 | K | **meta.txt no dice cuántos eventos del techo salen del respaldo M1**, ni cuántos llenados del trader caen en un minuto distinto del suyo. `Traza.por_fuente` se rellena pero no se imprime; ADR-0053 §7 lo pide a una corrida que cuenta. | HECHO | MENOR | techo_parejas.py:360, :507-509, :836-859; cableado.py:522; ADR-0053:200-202; RECORRIDA-CONSTRUCCION-3.md:772-773 | a, c | Que el informe dé esos recuentos en otro sitio | SIN PASADA |
| K-05 | K | **`Broker.mover_stop` acepta un SL nuevo sin mirar de qué lado del precio queda, ni el stops level.** MT5 rechaza un SL del lado malo (10016, INVALID_STOPS); en el simulador, el stop salta en el tick siguiente. Ningún ADR trata la modificación del SL de una posición (ADR-0057 §3 solo trata pendientes). | HECHO (código); la conducta de MT5 es SUPUESTO IMPUESTO sin fuente en el repo | MENOR | broker.py:691-715, :573-591, :615; ADR-0057:54-60 | c, d, e | Una NOTA o ADR que lo decida, o la demo con un 10016 provocado | SIN PASADA |
| K-07 | K | **Dos parámetros muertos que contradicen al simulador.** `modelo_llenado` = `al_tocar` (CONFIRMED) y `latencia_ms` = 0: ningún código los lee. El simulador llena con `limite_llena_al_toque: false` (llenado.yaml). Dos registros para lo mismo, contra ADR-0002. Gana ADR-0051 DN-1. MASTER_PLAN:280 dice que F24 simula `freeze_level` y el modo de llenado, y no lo hace. | HECHO | MENOR | parametros.yaml:184-211; `git grep` (solo test_capa_generada.py:247-248); llenado.yaml:4-6; ADR-0051:34-39, :137; MASTER_PLAN.md:280 | c, e, f | Un lector de esos parámetros que no vi | SIN PASADA |
| K-08 | K | **El deslizamiento tiene dos rutas con distinta cobertura.** `deslizamiento_fijo_puntos` se aplica a entradas stop y stops de salida, no a los cierres a mercado; ADR-0092 §4 sí cobra los manuales. Según por dónde entre F17, los cierres manuales pagarán o no. | HECHO | MENOR | llenado.yaml:9-13; llenado.py:268-271, :391-393; broker.py:644-656, :1011-1023; criterio_fidelidad.py:824-832 | c | Un ADR que fije la ruta de F17 | SIN PASADA |
| K-09 | K | **Latencia cero al colocar.** El motor decide en el fin de la M1 menos 1 ms y la orden puede llenarse con el primer tick del minuto siguiente; un EA solo sabe que la M1 cerró con ese tick o con un temporizador. Ningún ADR fija la latencia de colocación. | SUPUESTO ELEGIDO implícito, sin ADR | MENOR | cableado.py:396-399; broker.py:789-797; llenado.py:233-236; ADR-0053:217-221; ADR-0065:106 | d, e | Un ADR que la fije o un journal de la demo | SIN PASADA |
| K-10 | K | **El guion del techo depende de APIs privadas sin guardia** (`MotorCableado._a_la_cuenta` con un `SimpleNamespace`, argumentos posicionales de `construir_motor_cableado`). Nada en tests/ lo protege; ADR-0098 §3 prevé releer el techo. | HECHO | MENOR | techo_parejas.py:419-422, :492, :507-509, :581-583, :1033-1038; cableado.py:506-560; ADR-0098:144-155 | a, f | Un test en tests/ que importe el guion | SIN PASADA |
| K-11 | K | **Docstrings viejos**: broker.py dice «ADR-0052, PROPUESTO» y que no se cablea; también simulacion.py:1, simulador_config.py:1, llenado.yaml:1 y knowledge/simulador/README.md:3-4. ADR-0051 y 0052 son ACTIVE y ADR-0053 cablea. | HECHO | MENOR | broker.py:1, :46; ADR-0052:149-151; ADR-0051:221-223 | e | — | SIN PASADA |
| K-12 | K | **La capa MQL5 no lee en vivo el estado del símbolo** (stops level constante generada; sin freeze level ni spread). R6a.7 compara una vez antes de operar. | HECHO; que MT5 los cambie en vivo es SUPUESTO sin fuente | MENOR | Generado.mqh:87-88; `grep -rn` en mql5/; HOJA-DE-RUTA.md:607-618 | d, e | Una lectura en vivo que no vi | SIN PASADA |
| K-13 | K | **Llenados parciales, modo de llenado y expiración no tienen modelo ni parámetro.** ADR-0004 los nombra como categoría broker, sin parámetro; `expira_ms` existe y nadie lo pasa; MedirDemoFTMO elige FOK→IOC→RETURN sin parámetro. | PREGUNTA PENDIENTE (F17 / demo; ingenieros) | MENOR | broker.py:900-909, :788, :806-807; primitivas_broker.py:694; ADR-0004:12; tools/mql5/MedirDemoFTMO.mq5:153-160 | c, d, e | Un parámetro que no vi | SIN PASADA |
| K-14 | K | **Cancelar y volver a colocar es atómico en el simulador.** 775 cancelaciones en la corrida (3), casi todas de RN-006 (ADR-0056 §7), en el mismo milisegundo. En MT5 la cancelación puede llegar con la orden ya llena. R6a.3 habla de idempotencia, no de esta carrera. | HECHO | MENOR | cuenta-por-mes.txt:1990-3000; primitivas_broker.py:801-807; broker.py:633-642; HOJA-DE-RUTA.md:565-575 | d | Que R6a.3 o F31 la nombren | SIN PASADA |
| D-09 | D | `libros.yaml` lleva una cabecera vieja: dice «NO ESTAN enero ni septiembre», y enero está en la línea 54. Septiembre, marzo y diciembre siguen sin entrada; sin ella ningún libro se lee (ADR-0039). | HECHO | MENOR | `libros.yaml:15` frente a 54; PS:155 | f | — | SIN PASADA |
| D-10 | D | El «Hecho cuando» de A.4 y su Estado son coherentes (v6 a v21, faltan v18-v21), pero su Refs sigue citando «hecha hasta v17». | HECHO | MENOR | HOJA:741, 745-746 | f | — | SIN PASADA |
| I-01 | I | El Anexo B da cifras viejas: «94 ADR» (hoy 96), «2.122 funciones» de test (hoy 2.137), «tests unas 55.000» líneas (hoy 56.050). Correctas: guardia 6.000 (6.018), MQL5 unas 1.700 (1.741; más `tools/mql5/MedirDemoFTMO.mq5`, 1.560), src unas 40.000 (40.809). | HECHO | MENOR | AUDITORIA-2026-11-21.md:334-335; `ls docs/adr` contado con `grep -c` = 97 con la plantilla, sin 0087 ni 0095; PROJECT_STATE.md:19; recuento con python | e | Otra forma de contar | SIN PASADA |
| I-08 | I | «Reordenar make check» no tiene medida publicada; el orden tiene una razón escrita (`desellar` primero, `sellar` último, `.NOTPARALLEL`). | HECHO | MENOR | Makefile:5-10, :82; ENTORNO-CODE.md:140-150 | e | Otra medida | SIN PASADA |
| I-09 | I | Librerías ICT/SMC y tasa de descarte por tipo de setup: sin referencia en el repo; la tasa exigiría material que se declara: §9. | SUPUESTO ELEGIDO | MENOR | grep en los ficheros citados | e | Un documento que lo pida | SIN PASADA |
| I-10 | I | El README de la raíz está desfasado («35 funcionalidades en 8 fases», CLI incompleta, sin CLAUDE.md ni hoja de ruta). mql5/README.md cita `Params.mqh` y `Scripts/RunCases.mq5`, que `git ls-files` no lista. | HECHO | MENOR | README.md:8-9, :27-32; mql5/README.md:2-4; `git ls-files mql5 tools` | e | Que se generen y no estén versionados | SIN PASADA |
| I-11 | I | CLAUDE.md comprime ADR-0037 §3 («no lo abre ninguna autorización»): vale para lo que se lee a propósito; lo visto por accidente es exposición que se declara (ADR-0021 §2). Gana el ADR. | MATIZ | MENOR | CLAUDE.md punto 3; ADR-0021:20-23; ADR-0037:17-24 | e | Un ADR posterior | SIN PASADA |
| I-12 | I | «Febrero no se descarga» sale de ADR-0092 (:129, :372, :393), no de CLAUDE.md: enlazar al ADR. | MATIZ | MENOR | ADR-0092:129, :372, :393 | e | — | SIN PASADA |
| I-13 | I | La guardia está pensada para sesiones de Claude Code; hay que decir que no es para humanos ni para su IDE. | SUPUESTO ELEGIDO | MENOR | Makefile:12-22; CLAUDE.md | e | Un runbook para humanos | SIN PASADA |

## §13 · Los comandos ejecutados y los prompts de los subagentes

### 13.1 · Comandos del orquestador (todos desde la raíz del repo salvo los de la carpeta de trabajo)

Comprobaciones de la PARTE 1:
```
git status --short
git branch --list
git rev-parse main
git rev-parse "stable/F39l-recorrida-construccion-3^{commit}"
git rev-parse "main^1"
git status --short --ignored > C:/Users/USER/Desktop/auditoria-profunda-trabajo/foto-ignored-inicio.txt
```
Mapa (§1): `git ls-files <zona> | wc -l` con rutas literales (docs/adr, docs/validation, docs/plan,
docs/runbooks, knowledge/spec, knowledge/cuentas, knowledge/simulador, scripts, tests, mql5, .claude,
src/botsito); `ls src/botsito`; `ls docs`; `wc -c docs/adr/*.md`; `grep -m1 "^# " docs/adr/*.md`;
`wc -c docs/validation/*.md`; `grep -m1 "^# " docs/validation/*.md`; `wc -c` y `grep -m1` sobre docs/plan,
docs/runbooks, docs/state, knowledge/spec, knowledge/cuentas, knowledge/simulador; `wc -c` sobre
src/botsito/*.py, src/botsito/*/*.py, scripts/*.py, mql5, .claude, Makefile y pyproject.toml; un `awk` que
imprime la primera línea de docstring de cada .py; `ls` de anexos/RECORRIDA-CONSTRUCCION-3 y de
docs/sesion-{4,5,6,7}. Negados por la guardia: un bucle `for` sobre `git ls-files "$d"` y un `join` con
`<(…)` (§9.3).

Lecturas con Read: PROJECT_STATE.md, .claude/hooks/ficheros_con_ocultos.txt, la cabecera de
.claude/agents/auditor-encargo.md, meta.txt, ADR-0098, VIABILIDAD-COMISION.md, AUDITORIA-2026-11-21.md.

Contraste (fase C), con `sed -n` sobre líneas concretas: SESION-01-2026-09-09.md:36-42,
parametros.yaml:1275-1285, ADR-0022 y ADR-0026 (grep FundedNext), criterio_fidelidad.py (imports,
`PosicionCerrada`, :815-885), cableado.py:1343-1372, techo_parejas.py:15-30, :105-118, :532-545,
ADR-0057:17-30, DEMO-EJECUCIONES-2-3.md:38-46, METODO-FIDELIDAD-RENTABILIDAD.md:872-893,
F35-ORDEN-STOP-PIVOTE.md:205-215, TICKS-SPREAD-SALIDA.txt:1-35, RECORRIDA-CONSTRUCCION-3.md:474-482,
HOJA-DE-RUTA.md:903-912, ADR-0092:66-70 y :150-156, MASTER_PLAN.md:127, DEMO-FTMO.md:160-163 y :188-190,
`grep -c A-56` sobre ADR-0098, ADR-0040:1-35, ADR-0073:13-60, VIABILIDAD-TRADER.md:179-186,
primitivas_broker.py:488-496.

Ejecuciones de Python (solo aritmética, sin leer nada del repo salvo importar la función pura):
```
.venv/Scripts/python.exe -B C:/Users/USER/Desktop/auditoria-profunda-trabajo/sintetico_equilibrio.py
.venv/Scripts/python.exe -B C:/Users/USER/Desktop/auditoria-profunda-trabajo/sintetico_caja.py
```
(El primer intento con `PYTHONPATH=src` delante lo negó la guardia: §9.3.) Salida del primero:
`fills [2, 1, 2, 0]`, `esperanza 0.3125`, `equilibrio a 0.10 2.125`, `esperanza tras deslizar 0.1000`,
`equilibrio a 0.50 -1.875`, `pendiente de meta.txt 0.13452…`. Salida del segundo: con d entre 8 y 40,
la caja derivada da un stop implícito d+1 en los 24 valores que no son múltiplo de 4.

Auxiliares en la carpeta de trabajo (no tocan el repo): `extraer_entrega.py` y `estructura_jsonl.py`
(sin uso: los ficheros de salida de los subagentes estaban vacíos), `resumen_d1.py` (lee los JSON de
las pasadas adversarias) y `montar_informe.py` (monta este informe). Comprobaciones de 2.9: `git status
--short | wc -l`, `git diff --stat | wc -l` y `diff` de `git status --short --ignored` contra la foto de
partida, tras las tandas y al final (§15).

### 13.2 · Los prompts

- **El marco y las reglas que recibieron TODOS los subagentes de eje**, literal, están en la carpeta de
  trabajo: `13-prefijo-subagentes.md` (las instrucciones de marco, la PARTE 2 entera y el formato de la
  PARTE 8). Cada prompt de eje fue: ese marco + la PARTE 2 literal + el bloque de su eje de la PARTE 6
  del encargo (pregunta, subpreguntas, fuentes, entrega, criterio y trampas) + el formato de la PARTE 8,
  con estas adiciones del orquestador, que fueron las únicas:
  - a todos: no buscar `docs/encargos/` (no hay rama), no escribir ficheros, no lanzar subagentes,
    pedir al orquestador la ejecución de funciones sintéticas, el mapa en `01-mapa.md`;
  - P1: «Comprueba esta afirmación del consultor leyendo el código: puede ser falsa» (pieza 3) y la
    pieza 12 con la comisión; P4: «Lee cómo calcula techo_parejas.py el equilibrio, qué llenados cuenta
    como afectados y con qué signo»; P5: los términos de búsqueda y `kb find`; P7: la aritmética por
    anchura de intervalo; P2: buscar en los yaml por id; P3: «razónalo» sobre la dirección de S-14;
    S, R, K, D, X, I: el CONTEXTO de la PARTE 3 que les tocaba y, a K, «NO la repitas» (la auditoría
    del 2026-11-21); a D, contar filas de HOLDOUT-EXPOSICIONES y no copiar fechas; a X, usar `git log`.
- **Los adversarios por hallazgo** recibieron, literal, la PLANTILLA ADVERSARIA de la PARTE 7 con la
  PARTE 2 entera y el texto del hallazgo; el guion y los argumentos de cada tanda quedan guardados por
  el Workflow en `C:\Users\USER\.claude\projects\C--Users-USER-Desktop-Bot-v3\cd5a60c3-e5f7-4564-9a32-adebee619f25\workflows\scripts\pasada-adversaria-auditoria-wf_9dffc0bb-22c.js`
  y en los diarios de las ejecuciones `wf_9dffc0bb-22c`, `wf_a7442c26-e9f` y `wf_799256c2-271`; los resultados, en
  `entregas/D1-pasada-adversaria.json`, `D1b-…` y `D1c-…`.
- **El adversario general** recibió la PLANTILLA DEL ADVERSARIO GENERAL con la PARTE 2 entera, el
  borrador de §2 (`02-respuesta-central-borrador.md`) y la petición de atacar en las dos direcciones.
- **El revisor final** recibió la plantilla de la FASE G con la PARTE 2 entera (§14).

Nota de honestidad: los prompts de eje no se guardaron como ficheros en el momento; lo de arriba los
describe por sus piezas, que sí son literales (el prefijo guardado y la PARTE 6 del encargo).

## §14 · El informe del revisor final, tal cual, y lo que hice con él

Revisor: `auditor-encargo` con opus, que no vio el trabajo, sobre `borrador.md` (registro 02:06). Su
informe, copiado tal cual:

> ## Revisión final G1 · borrador.md (AUDITORIA-PROFUNDA-2026-11) · 2026-11-23
>
> Base: main en 8a10590b. Solo he leído: no he escrito nada ni en el repo ni en la carpeta de trabajo, y no he ejecutado ningún guion. Al terminar, `git status --short` y `git diff --stat` salen vacíos. Los `__pycache__` ignorados de `docs/validation/anexos/*` ya estaban antes de la auditoría: los de RECORRIDA-CONSTRUCCION-3 tienen fecha del 2026-11-22 a las 17:03 y a las 19:32 (-0500). No tengo la foto de partida de `--ignored`, así que esa comparación no la puedo hacer.
>
> ### Cómo elegí los 15 hallazgos
> La tabla de §12 tiene 129 filas de gravedad C o PLAN (33 C y 96 PLAN), en las líneas 1149-1277 del borrador. Cogí una de cada ocho, empezando por la segunda (línea 1150): líneas 1150, 1158, 1166, 1174, 1182, 1190, 1198, 1206, 1214, 1222, 1230, 1238, 1246, 1254 y 1262.
>
> ### Parte 1 · Quince hallazgos contra el repo
> | Hallazgo | Dónde (borrador) | Fuente leída | Veredicto |
> |---|---|---|---|
> | P2-02: C no pide descomponer el techo; eso solo está en B; la ablación de RN-014 mide parejas 31→28 | :1150 | `docs/adr/0098-*.md:139-148`; `anexos/TRAZAS-ABLACION/ablacion.DIAGNOSTICO.vigentes.txt:1486` | CORRECTO. Que esa sea «la única» ablación no lo he podido comprobar. |
> | P6-15: cada exportación nueva necesita su entrada en libros.yaml, con el huso medido por velas | :1158 | `libros.yaml:10-13`, `ADR-0069:17-21,:41`, `RUMBO-2026-11.md:19` | MATIZ. libros.yaml y ADR-0069 lo sostienen. RUMBO:19 habla del bloque de días, no de las exportaciones. La gravedad C es discutible. |
> | R-05: 15,7→15,2 y 13,9→14,4 | :1166 | `HOJA-DE-RUTA.md:910-911`; `RECORRIDA-CONSTRUCCION-3.md:455,:463` | MATIZ. Las cifras son correctas, pero el borrador cita «RECORRIDA-3 §1 (:455, :463)», que es el pivote: las cifras están en §1 (:455, :463). |
> | M-08: 30/166 = 18,1 %, 72/208 = 34,6 %, julio 33,3 % (diaria 32,2 %), las cuatro piezas bajan de 14 a 11 | :1174 | `RC3:463-468, :475-480, :503-507, :627`; `cableado.py:1436-1477`; `criterio_fidelidad.yaml:55-65`; `SESION-07-EXTRACCION.md:469-476`; `ACTIVAR-SESION-07.md:712-714` | CORRECTO. Recalculé toda la aritmética (208−42 = 166; 30+42 = 72; 19/59 = 32,2 %). |
> | P1-01: el techo usa el stop y la unidad del R de V1; de V2 solo comparte el 3,75 | :1182 | `anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py:107-117, :543-555, :804-806`; `viabilidad_comision.py:66-79`; `viabilidad_trader.py:312-314` | CORRECTO. En el techo la caja es el stop del libro dividido por 0,8 y el objetivo es 3 cajas = 3,75 veces el stop del libro. V2 pone el stop en 0,8 D. Nota: el borrador cita `techo_parejas.py` como si estuviera en `scripts/`, pero está en `docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/`. |
> | P1-14: toda la muestra de V2 es material sin vídeo; en el techo julio ≈ el resto | :1190 | `criterio_fidelidad.yaml:61-64`; `VIABILIDAD-TRADER.md:179-182`; `meta.txt:13,23` | MATIZ. El 29-abr es un día CON vídeo (`dias_con_video`), y V2/la anotada tienen operaciones de ese día. «Toda» es falso por un día. |
> | P3-03: `DESFASE_PUNTOS = 2`, 36 valores, mediana 0 en 75 | :1198 | `viabilidad_trader.py:50, :380-381, :397-399, :412`; `VIABILIDAD-TRADER.md:61-66`; `BLOQUE-DE-LA-CAJA.md:200-209`; `ORDEN-STOP-O-LIMITE.md:96, :109` | CORRECTO. No he comprobado lo de «abril n=3». |
> | P4-02: el equilibrio −2,52 pide deslizamiento a favor y en una stop no se gana precio | :1206 | `ADR-0057:19-29`; `DEMO-EJECUCIONES-2-3.md:41-44`; `ADR-0090:231-237`; `meta.txt:18` | CORRECTO. Matiz: en la demo hubo un cierre a mercado con −2,0 (ADR-0090 §7, «−2 al cerrar»), y `_fills_afectados` cuenta también los cierres manuales. Las stops nunca llenaron mejor. |
> | P5-03: riesgo 0,4-0,5 % en fondeo, 1 % en backtest; el bot 0,5 %; «discrepancia 0,4/0,5 sin resolver» | :1214 | `parametros.yaml:1279, :1283, :1481`; `SESION-01-2026-09-09.md:39-40`; `ADR-0020:28-38, :103` | ERROR en parte. La «discrepancia sin resolver» no existe: SESION-01:40 dice que la tabla vieja ponía 0,4 y que ADR-0020 lo invirtió. El propio borrador lo refuta en §9.1 (:1030) y en el registro de las 00:02 (:1096, «P5-03 → MATIZ»), pero la fila de §12 sigue diciéndolo y su estado es «SIN PASADA». |
> | P6-09: la vía (i) no necesita puente; las lecturas no cuentan para las 2.000 peticiones | :1222 | `HOJA:680`; `ADR-0082:37-41`; `ACTIVAR-SESION-08.md:639`; `RUMBO:43` | CORRECTO |
> | P6-20: F33 depende de F17; F34 de F32 y F33; R6a.8 no está hecha | :1230 | `MASTER_PLAN.md:146-147`; `HOJA:620-629` (R6a.8 no tiene «Estado: HECHA»); `ADR-0098:220-224` | CORRECTO con matiz. F33 depende de F17 y también de F31. `arnes.py:196` no enseña nada de lo que se afirma (es un supuesto). |
> | S-06: d) y e) se miden con umbrales propios (3 %, 94 %), no con los 5 %/10 % de la firma | :1238 | `ADR-0092:87-91`; `ADR-0098:101-107`; `meta.txt:13-16` | CORRECTO |
> | R-09: no hay prueba gratuita viva con evidencia | :1246 | `docs/runbooks/DEMO-FTMO.md:162` (28/10/26 a 11/11/26); `DEMO-EJECUCIONES-2-3.md:447`; `HOJA:440` | CORRECTO. La redacción confunde: «como la anterior (28/10 a 11/11)» son las fechas de la propia prueba del 2026-10-29. |
> | M-13: «se sigue» pide 19 parejas = 28,4 % de 67; el 0,70 pide unas 47 | :1254 | `docs/plan/PIVOTES-SESION-7.yaml:30-31`; `RC3:468` | MATIZ. Las cuentas están bien (19/67 = 28,4 %; 0,70·67 = 46,9). Pero «se sigue» pide los DOS mínimos (también 33 o menos de más), y el 0,70 de ADR-0070 se mide sobre toda la construcción (198), no sobre julio. |
> | X-09: guardia.py 289.378 B, 6018 líneas, 165 funciones, 12 / 46 / 7 commits, tests de 290.707 B, ningún ADR | :1262 | `wc -c -l`, `grep -c "^def "`, `git log` (los tres recuentos), `cat tests/unit/test_guardia*.py \| wc -c`, `grep -l guion-mismo-comando docs/adr/*.md \| wc -l` = 0 | CORRECTO en todo lo que medí. No he comprobado el reparto por familias (2190, 404, 653, 611 líneas). |
>
> ### Parte 2a · Las cifras de §2
> | Cifra | Dónde | Fuente | Veredicto |
> |---|---|---|---|
> | −0,239 en 191 | :230 | `meta.txt:12-13` | CORRECTO |
> | +0,47 en 67; +0,56 en 77; 5 USD | :231-232 | `VIABILIDAD-COMISION.md:112, :115, :7, :56` | CORRECTO |
> | Opera cuentas propias; en la 7 no dio cifras de su cuenta | :238-239 | `SESION-01-2026-09-09.md:72`; `SESION-07-EXTRACCION.md:80` | CORRECTO |
> | 5 USD = 2,50 por lado | :243 | `ADR-0090:102-105` | CORRECTO |
> | Comisión por R de V2 y de la anotada: 0,42 y 0,43 | :245 | `VC:112, :115` | CORRECTO |
> | Comisión del techo 0,34-0,67 R; antes de comisión, de +0,10 a +0,43 | :246-248 | `meta.txt:13, :18`; `criterio_fidelidad.py:824-839, :869-882`; `cableado.py:1349-1352, :1366-1369`; `techo_parejas.py:541` (todas las entradas son `colocar_stop`) | CORRECTO. Aritmética sobre cifras publicadas: pendiente = 0,339/2,52 = 0,1345. Cada operación tiene 1 o 2 llenados afectados, así que la media de lotes/riesgo está entre 0,067 y 0,1345 y la comisión (×5) entre 0,336 y 0,673. |
> | Bruto: anotada +0,98, V2 +0,88 | :248-249 | `VC:112, :115` | CORRECTO |
> | Objetivo 3,75 veces el stop; A-47 RESUELTA; A-56 abierta | :252-256 | `techo_parejas.py:107-117, :555`; `ambiguedades.yaml` (A-47: `estado: RESUELTA`); `PROJECT_STATE.md:72` | CORRECTO. «El break even lo dictó el trader (ADR-0073 §1)»: ADR-0073 §1 resuelve el stop y el objetivo, no el break even. Es un matiz menor. |
> | 26 de 38 en [3,00; 3,75) | :254 | `ADR-0040:22-35`, enmienda en `:9-18` | CORRECTO. Las 38 incluyen mayo (5 ganadoras, de sus días dev), no solo meses de construcción. |
> | 5 más allá de 4 R; 2 antes del objetivo; 5 de 77 a cero | :256-257 | `VIABILIDAD-TRADER.md:179-183` | CORRECTO |
> | Break even movido en 79 de 191 | :258 | `meta.txt:11` | CORRECTO |
> | A-16 sin medir a esta escala | :260-261 | `METODO-FIDELIDAD-RENTABILIDAD.md:889-893`; `ADR-0061:61-63` | CORRECTO |
> | 2,52 puntos a favor; ni el modelo ni la demo | :265-267 | `meta.txt:18`; `ADR-0057:19-29`; `DEMO-EJECUCIONES-2-3.md:41` | CORRECTO (con el matiz del cierre a mercado de P4-02) |
> | 7 no colocables: ni todas al máximo llegan a 0 | :269 | aritmética sobre `meta.txt:9-13` | CORRECTO: −0,098 con 3,75 R y −0,018 con 6 R |
> | Julio −0,245 | :270 | `meta.txt:23` | CORRECTO |
> | d) 4,88 % y e) 92,05 %, que fallan | :271 | `meta.txt:15-16`; `ADR-0098:101-107` | CORRECTO |
> | 0,71 R a unos dos errores típicos | :275 | `VC:112` (IC [−0,13; +1,08]); `meta.txt:14` | MATIZ. La aritmética da 2,1 errores típicos (errores 0,309 y 0,129). Pero mezcla unidades, justo lo que dice P1-01: el R de V2 es 0,8 D. En la unidad del techo, V2 neto ≈ 0,47·0,8 = 0,38 y la diferencia ≈ 0,62 (aritmética sobre cifras publicadas). §2 debería decirlo o citar P1-01. |
> | Intervalos al 95 % por operación frente al 90 % por días | :276 | `VC:24` (bootstrap); `meta.txt:14` | CORRECTO |
> | Adversario: −0,37 R; ADR-0073:15-30 y :51-56; ADR-0040:9-18 | :298-303 | esas líneas | CORRECTO |
>
> ### Parte 2b · Las cifras de §7
> | Cifra o afirmación | Dónde | Fuente | Veredicto |
> |---|---|---|---|
> | El ADR de C lo escribe Aleks | :874 | `ADR-0098:147-148`; `HOJA:437-443` | CORRECTO |
> | Hoy no hay prueba gratuita viva | :876 | `DEMO-FTMO.md:162` | MATIZ. La fuente dice que la última acabó el 11/11; que no haya ninguna viva es una inferencia. Mejor «ninguna viva con evidencia», como R-09. |
> | Copia de v18 a v21 | :877 | `HOJA:746`; `PS:135` | CORRECTO |
> | R6.0 sigue con la razón del tope de peticiones | :878 | `HOJA:635-637`; recuadro `ADR-0082:101-114` | CORRECTO |
> | Meta de marzo de 2027 | :879 | `HOJA:7`; `ADR-0098:220` | CORRECTO |
> | Letra M | :879 | `PS:44` | CORRECTO |
> | R7.3 depende de los dos mínimos | :884 | `HOJA:681` | CORRECTO |
> | Noviembre reservado; el mes 12 tapado por número | :884 | `PS:28` («octubre y noviembre de 2026, reservados»); `ADR-0092:125-126, :136-139` | CORRECTO |
> | «Habilita medir» :154; sin F17 no hay «pasa» :113 | :884 | `ADR-0092:154, :113` | CORRECTO |
> | De 2 a 6 pruebas para N = 100, unas 8 si se reparten | :885 | `RC3:463-468` (julio 67 en 13 días; abril 35 en 21); 198/76 y 235/76 | CORRECTO (aritmética: 20 y 60 días) |
> | Opción 2 de la auditoría; la medida, una semana | :883, :885 | `AUDITORIA-2026-11-21.md:79-84, :69` | CORRECTO |
> | Junio a noviembre de 2025, más la extensión | :886 | `ADR-0092:117-133` | CORRECTO |
> | Octubre y noviembre de 2026 no sirven para comparar | :886 | `PS:28` | CORRECTO |
> | La puerta la ata el percentil 5 (P7-06) | :887 | aritmética sobre `meta.txt:14` | MATIZ menor. Con desviación 1,78 por operación salen +0,29 con N=100 y unas 857 operaciones para +0,10, como dice el borrador. Con N=340 sale +0,16, no «≈ +0,15» (:1235). |
> | Ingenieros hacia el 2026-12-03 | :887 | `ADR-0098:230` | CORRECTO |
> | Puente de 12 pasos | :885 | tabla P1 del borrador, 12 filas | CORRECTO (es interno) |
>
> ### Parte 3 · Fechas y R nuevos
> Patrones que pasé por grep: ISO de meses no permitidos, `dd-mes`, `dd/mm`, `aaaammdd`, y día + nombre de mes completo.
>
> | Coincidencia | Línea | Veredicto |
> |---|---|---|
> | 2026-09-09, 09-29, 10-23, 11-04, 11-16, 11-20/21 (ids `fb-*` y sesiones); 2026-09-12, 09-13, 09-30, 10-01, 10-04, 10-06, 11-08, 11-09, 11-10, 11-18, 11-22, 11-23 (ADR, documentos, decisiones, commits) | muchas | LEGÍTIMAS |
> | 2026-09-03, 2026-10-01, 2026-11-06, 2026-11-09 dentro de `git log --since` | :678, :1255, :1257, :1262, :1335 | LEGÍTIMAS (commits) |
> | HOLDOUT-EXPOSICIONES «filas 2026-10-14, 2026-10-18, 2026-10-27» | :1259 | LEGÍTIMAS: son fechas de declaración, no días expuestos. PS:106 escribe la misma. |
> | 28/10 a 11/11 y «12-nov» | :1106, :1246 | LEGÍTIMAS (prueba gratuita de FTMO) |
> | 2026-12-03 | :887, :1245, :1274 | LEGÍTIMA (fecha dada por Aleks, ADR-0098:230) |
> | Semillas 20260928 y 20261107 | :347, :492 | LEGÍTIMAS (no son fechas) |
> | **principios de diciembre de 2025** («el calendario empieza el...») | :768, :1224 | DUDOSA. Es el límite publicado del calendario de cierres (ADR-0092:147), pero es un día de mercado de diciembre de 2025, un mes con material del trader. Reescribir como «principios de diciembre de 2025». |
> | **principios de octubre de 2026** («caducó el», «hasta el») | :1016, :1224 | DUDOSA por la misma razón: día de mercado de octubre de 2026, mes reservado (PS:28). Reescribir como «principios de octubre de 2026». |
> | Días de construcción (abr, jul, ago, ene de 2026) | varias | LEGÍTIMAS |
>
> **R nuevos.** No hay ningún R de operaciones reales sin publicar que no esté marcado. Los valores hipotéticos (−0,098, −0,018, −0,266, −0,37, +0,07 a +0,27, «enero ≈ −1,2») van marcados como aritmética sobre cifras publicadas.
>
> **Una incoherencia con la regla 2.3.** La media del techo fuera de julio aparece en §3 P1, tabla del puente, fila 1 (:336) y en §12 P7-04 (:1160). El registro dice lo contrario: a las 23:56 (:1094) y a las 01:03 (:1107) se decidió que «equivale a un R de un subconjunto nunca publicado; en el informe va sin la cifra». También la citan las propias filas del registro.
>
> ### Lo que no pude comprobar
> - Que la ablación de TRAZAS-ABLACION sea la única de RN-014.
> - «Abril n=3» de P3-03.
> - El reparto por familias de guardia.py (X-09).
> - Las referencias internas de §7 a M-01, M-12, M-15, D-01, P4-05, P4-06 y P6-24 (cada una tiene su fila; no son de mi muestra).
> - La comparación de `git status --short --ignored` con la foto de partida, porque no la tengo.
>
> ### Lo que el orquestador debe arreglar, de más a menos grave
> 1. La media del techo fuera de julio en §3 P1 y §12 P7-04 (y su cita en el registro): quitar la cifra.
> 2. La fila P5-03 sigue con la «discrepancia 0,4/0,5» y «SIN PASADA»: corregir el texto y poner MATIZ.
> 3. §2 punto 5: los 0,71 R mezclan la unidad de V2 (0,8 D) con la del techo (D): decirlo o dar ≈ 0,62.
> 4. Fechas principios de diciembre de 2025 y principios de octubre de 2026: pasarlas a mes.
> 5. P1-14: no «toda» la muestra de V2 es sin vídeo (un día de abril con vídeo).
> 6. M-13: «se sigue» pide los dos mínimos y el 0,70 es sobre toda la construcción.
> 7. Citas desplazadas: R-05 (§1, no §3); `techo_parejas.py` está en el anexo, no en `scripts/`; P6-15 cita RUMBO:19, que no trata de exportaciones; P6-20 (F33 depende también de F31; `arnes.py:196` no sostiene nada).
> 8. §7: «hoy no hay viva» → «ninguna viva con evidencia».
> 9. P7-06: con N = 340 sale ≈ +0,16.
> 10. Formato: la fila M-04 lleva un «|» sin escapar y la tabla de §12 se desordena desde ahí.
>
> [Comandos: lecturas con `sed -n`, `grep -n`, `awk -F'|'` y `grep -oE` sobre el borrador y sobre los ADR, informes, anexos, spec y código citados; `wc`, `git log` y `git grep` sobre guardia.py y docs. Negativas de la guardia: `git ls-files | grep techo_parejas` sin ruta (ADR-0088; repetido con rutas literales) y una asignación sobrante (`NOMBRES_DE_ENTORNO`; error suyo). Ninguna se rodeó.]

(Una sola alteración: en su Parte 3 y en el punto 1 de la lista, la cifra de la media del techo fuera
de julio que el revisor citaba se ha quitado, porque es justo lo que pide retirar; y su lista de
comandos va resumida entre corchetes.)

**Lo que hice con cada punto:**

| # | Qué pedía | Qué hice |
|---|---|---|
| 1 | Quitar la media del techo fuera de julio | Hecho: sustituido en el montaje (tabla del puente y P7-04) por «julio −0,245 y el total −0,239 casi coinciden», y quitado del registro. El guion de montaje comprueba que la cifra no queda en el informe. Las entregas de la carpeta de trabajo quedan tal cual (no son el informe) |
| 2 | P5-03 | Hecho: texto corregido y estado «MATIZ (corregido por el orquestador)» |
| 3 | Los 0,71 R mezclan unidades | **No lo aplico.** En V2 y en el techo el R es el PnL entre el riesgo en dinero al colocar, que en los dos es el 0,5 % del saldo (techo: cableado.py:1352 y criterio_fidelidad.py:582-585; V2: viabilidad_comision.py:279-284, R sobre la distancia del lote, que se calcula para ese 0,5 %). Lo que cambia es la distancia en puntos, no la unidad del R; por eso P1-01 se reformuló («en estructura es V2»). Multiplicar V2 por 0,8 sería un error |
| 4 | Fechas | Hecho: «principios de diciembre de 2025» y «principios de octubre de 2026»; el montaje comprueba que no quedan |
| 5 | P1-14 | Hecho |
| 6 | M-13 | Hecho: marcado como ilustración sobre julio |
| 7 | Citas desplazadas | R-05: hecho. `techo_parejas.py`: en el informe se cita por su nombre o por el anexo; donde un subagente puso otra ruta, queda en la entrega y lo dice este punto. P6-15 y P6-20: anotado aquí; sus filas ya tienen estado MATIZ de la pasada adversaria por lo mismo |
| 8 | «hoy no hay viva» | Hecho: «de la que hoy no consta ninguna viva» |
| 9 | P7-06 | Hecho: +0,16 |
| 10 | Formato de §12 | Hecho: la fila que descuadraba era una pieza de la tabla de E1 llamada «S-14» que el patrón tomaba por un id (renombrada), y tres celdas con «|» dentro (P2-02, I-01, I-07), reescritas; el montaje comprueba que todas las filas tienen nueve celdas. Su matiz sobre «el break even lo dictó el trader» lo aplico en §2: lo dictó en las sesiones 3 y 7a (ADR-0061 §1; fb de la sesión 7), no en ADR-0073 §1 |
| 11 | (De su Parte 1) P1-01 CORRECTO | La tercera tanda adversaria la dio por REFUTADA. Las dos lecturas son ciertas en su eje: en puntos, el stop y la unidad del R del techo coinciden con los de V1; en estructura (stop en el 0,8, lote al 0,8, objetivo a 3 cajas) es V2. Queda reformulada con las dos cosas (§3, P1; §9.1) |

## §15 · La lista de control de la PARTE 10, marcada

- [x] **Las comprobaciones de la PARTE 1 pasaron; al final, git status y git diff vacíos y el status con
  --ignored igual que la foto de partida.** Al empezar: status vacío, solo main, main = 8a10590b,
  `stable/F39l…^{commit}` = `main^1` = 88f678f7. Al final (2026-11-23): `git status --short` 0 líneas,
  `git diff --stat` 0 líneas, `diff` de `git status --short --ignored` contra la foto de partida vacío
  (las dos en la carpeta de trabajo: foto-ignored-inicio.txt y foto-ignored-final.txt), main sigue en
  8a10590b y solo existe main. También se comprobó tras las tres primeras tandas (registro 00:58). No
  hubo nada que borrar: los Python se ejecutaron con `-B`.
- [x] **Todos los subagentes fueron de solo lectura y nada se escribió fuera de la carpeta de trabajo.**
  Los 85 fueron `auditor-encargo` (Read, Grep, Glob y Bash con `solo_lectura.py`). Todo lo escrito está
  en C:\Users\USER\Desktop\auditoria-profunda-trabajo\, más este informe en el Escritorio, donde lo
  pide la PARTE 9.
- [x] **§0 se escribió antes de leer; cada cambio posterior lleva su hora y su motivo.** §0 a las 23:35
  del 2026-11-22, tras leer solo PROJECT_STATE.md, la lista de ficheros con ocultos y la cabecera del
  agente; el único añadido, E1, a las 01:16 del 2026-11-23, con su motivo en el registro.
- [x] **Cada eje de la PARTE 6 tiene su entrega.** Los catorce (P1-P7, S, R, M, X, K, D, I), guardados
  tal cual en entregas/, más E1 (§5).
- [~] **Cada hallazgo de gravedad C o PLAN está comprobado por ti con fichero:línea y pasó la pasada
  adversaria.** Los 33 de gravedad C pasaron la pasada adversaria (los diez duplicados heredan el
  veredicto del hallazgo que dice lo mismo; §12). Los PLAN que sostienen una opción de §7 o un diseño
  de §8 también (segunda y tercera tanda). Quedan **51 PLAN sin pasada** que no sostienen ninguna
  opción (incoherencias de documentos de estado, proceso, ingenieros): la FASE D1 no los exige, pero
  esta casilla, leída al pie de la letra, sí; por eso va a medias. Comprobados por mí con fichero:línea
  (registro 00:02, 00:10, 01:00, 01:02, 01:05, 01:52): los que sostienen §2 y §7 (P4-01, P4-02, P5-01,
  S-01 y su enmienda, M-04, M-03, D-01, P4-05, R-09, K-01, la contradicción A-16 y la del spread); los
  demás de gravedad C los comprobaron los adversarios y el revisor final, no yo línea a línea.
- [x] **Cada cifra lleva su fichero:línea y es la del informe más reciente que la publica.** Las cifras
  del techo salen del anexo de la última rama cerrada (meta.txt, RECORRIDA-CONSTRUCCION-3); las de lo
  que se creía, de VIABILIDAD-COMISION, que ningún informe posterior rehace (ADR-0098 §5, :199-201;
  P7-11). El revisor comprobó todas las de §2 y §7.
- [x] **Ninguna cifra es un R nuevo de operaciones; la aritmética está marcada como tal.** La única
  media de un subconjunto que se había colado (la del techo fuera de julio) se quitó tras el revisor;
  el montaje comprueba que no queda.
- [x] **Ninguna fecha de un día de mercado, operación o caso fuera de los meses de construcción; ningún
  resultado que no esté ya publicado.** Los dos límites del calendario de cierres que el revisor marcó
  pasaron a «principios de diciembre de 2025» y «principios de octubre de 2026»; el montaje comprueba
  que no quedan. Las demás fechas son de commits, sesiones, ADR, la prueba gratuita o días de enero,
  abril, julio y agosto de 2026.
- [x] **No se leyó nada de la lista de la PARTE 2.2 ni se ejecutó nada de la 2.5.** Las negativas de la
  guardia (§9.3) fueron por forma de comando, no por material; dos subagentes intentaron `kb at` sobre
  una sesión en cuarentena y la guardia lo negó sin que se leyera nada. Solo se ejecutaron dos guiones
  de aritmética con entradas sintéticas y los de la carpeta de trabajo.
- [x] **Las preguntas para el trader no llevan cifras ni resultados nuestros.** §6.
- [x] **§7 da opciones sin elegir; la opinión del auditor va aparte y marcada.**
- [x] **El revisor final está pegado y sus hallazgos, tratados.** §14: nueve aplicados, uno rechazado con
  su motivo (las unidades del R) y la discrepancia sobre P1-01 explicada.
- [x] **Lo que no se pudo comprobar está en §9.**

Auditoría lista para revisión. No hay rama que cerrar.
