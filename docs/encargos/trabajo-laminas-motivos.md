# Encargo · trabajo/laminas-motivos

Dado por Aleks (consultor) el 2026-11-11, en un solo mensaje. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Encargo del consultor (2026-11-11): rama trabajo/laminas-motivos, tramo R4 (corrige R4.5 antes de grabar la 7a; F de la Next Action, punto (1)). Ábrela con la skill abrir-rama, con riesgo medio (engine/laminas.py y sus tests; ni el motor ni la spec), y copia este encargo tal cual en docs/encargos/trabajo-laminas-motivos.md. Trabaja en la laptop (F2 necesita velas y ticks) y arranca Claude Code con CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1. Antes, /model: Opus 5.5, esfuerzo alto.
>
> BASE (compruébala con git al abrir): main y origin/main en b52a760, commit de estado sobre el merge 5260147 del tag stable/F38x-preparacion-sesion-7; CI de main sobre b52a760, run 43145636325, success (gh run view suelto); ninguna otra rama; PROJECT_STATE en 23.914 bytes. Si algo no cuadra, PARADA.
>
> OBJETIVO: que ninguna lámina dé al trader una causa falsa o dudosa como cierta de por qué el bot no coloca, y regenerar las láminas de la 7a con el arreglo.
>
> LO QUE ENCONTRÓ EL CONSULTOR al revisar C:\Users\USER\Desktop\laminas-sesion-7a (2026-11-11), con su auditor:
> - sesion-06, láminas 09 (corte 14:09) y 10 (corte 14:23), sesión de 11:00 a 15:00: «Iba a colocar la orden y no la coloca: está fuera de la ventana de la sesión.», junto a «ya ha gastado sus intentos en esta liquidez».
> - La causa: MOTIVO_GATE["RN-001"] = «está fuera de la ventana de la sesión» (src/botsito/engine/laminas.py:569), y la forma de RN-001 (strategy_spec.yaml:896-909) prohíbe con cualquiera_de cuatro ramas: fuera de la ventana, detenido_por_tope, detenido_por_tope_total y detenido_por_cartuchos. La frase nombra un caso, no la condición (patrón 3 de ERRORES-RECURRENTES).
> - El mismo defecto, según el auditor del consultor (verifícalo en 0.1): RN-020 (ramas perdida_dia, perdida_semana y el hecho detenido_por_tope; frase «pérdida máxima del día del trader») y RN-029 (ramas perdida_dia_firma y el hecho detenido_por_tope; frase «freno diario de la cuenta»). detenido_por_tope lo encienden RN-020 y RN-029, así que cada una puede salir con la frase de la otra. RN-008 es un todos_de cuya frase solo nombra la primera condición: parcial, no falsa.
> - _sin_orden (laminas.py:1022) pone la frase de _motivo (:1010-1019) a cada gate de f.bloqueos (:1055-1058) sin mirar la rama activa, e ignora el segundo campo del par (g, t), que puede ser «desconocido» (:440; interprete.py:136): un gate desconocido sale como causa cierta. La vía de f.prohibido y f.quizas (:1066-1074) usa el mismo _motivo.
> - Ningún test, ni el revisor de trabajo/laminas, ni la revisión de la v5 lo vieron.
>
> QUÉ NO CAMBIA: el motor (engine/ fuera de laminas.py y laminas_svg.py), la spec, los parámetros, el arnés y su salida, `motor decisiones`. Las láminas tienen que salir byte a byte iguales salvo las frases de causa que cambien por este arreglo. Lo que entra: laminas.py, sus tests, docs/runbooks/LAMINAS.md si describe las causas, docs/sesion-7/PREGUNTAS-7A.md (F3), el informe docs/validation/LAMINAS-MOTIVOS.md, HOLDOUT-EXPOSICIONES y lo de abrir-rama.
>
> FASE 0 (sin escribir salvo la apertura y la fila de exposiciones), con PARADA:
> 0.1 Por cada gate de MOTIVO_GATE: su forma en la spec, sus ramas (cualquiera_de, todos_de, hechos de detención y qué reglas encienden cada hecho), la frase de hoy y si cubre cada rama. Tabla: gate, ramas, quién enciende cada hecho, frase de hoy, cubre sí/no/parcial.
> 0.2 Mide qué rama de RN-001 está activa a las 14:08 y a las 14:22 en la sesión que corresponde a sesion-06 de la 7a, y qué hecho la produce. El día lo lees en C:\Users\USER\Desktop\laminas-sesion-7a\clave.txt y no se escribe ni en el repo ni en el informe: allí es «la sesión 6 de la 7a». Usa `motor decisiones` con las opciones que tiene (--carpeta en data/, --meses, --bitacora: verifícalas con --help; la bitácora registra los cambios de hechos, decisiones.py:467-475). Antes de correr, la fila de HOLDOUT-EXPOSICIONES.
> 0.3 Cuántas láminas de laminas-sesion-7a llevan una frase de gate que no cubre su rama activa, o un gate «desconocido» dicho como cierto (contado contra los HTML; la clave no hace falta).
> 0.4 Propón el arreglo, con estas decisiones del consultor que no cambian sin PARADA:
>    a) La frase sale de la rama activa. Si la rama es un hecho de detención, sale de f.origen (quién lo encendió), como ya hace FRASE_TOPE_POR_REGLA (laminas.py:504-510 y :795-803): nunca se deduce del nombre del hecho.
>    b) Negar por defecto: un gate de varias ramas sin frase para su rama activa, o un hecho sin origen conocido, es LaminaError.
>    c) Varias ramas activas a la vez: una frase por rama, sin repetir lo que ya dice otra causa de la lista (por ejemplo «ya ha gastado sus intentos»).
>    d) Un gate con t = «desconocido» en f.bloqueos se dice como dudoso, con la misma forma que FRASE_PROHIBE["desconocido"], nunca como causa cierta.
>    e) Lo mismo en la vía de f.prohibido y f.quizas.
>    f) RN-008 parcial: lo propones y decido en la PARADA.
> PARADA al terminar la fase 0.
>
> F1 · El arreglo en laminas.py, con tests:
>    - Que rompen en main (compruébalo con comparar-con-main): (1) una foto con detenido_por_cartuchos y RN-001 en f.bloqueos no dice «fuera de la ventana»; (2) detenido_por_tope encendido por RN-029 no da la frase de RN-020, y al revés; (3) un gate «desconocido» en f.bloqueos no sale como causa cierta.
>    - De la guardia nueva, que fallan a propósito con una tabla mutada: un gate de varias ramas al que se le quita la frase de una rama da LaminaError (en main no existe la tabla, así que este no se compara con main: se dice).
>    - Que no cambian: una foto fuera de la ventana sigue diciendo «está fuera de la ventana de la sesión».
>    - test_ninguna_frase_lleva_ids_dinero_ni_fechas (test_laminas.py:518-530) cubre también las frases nuevas, sea cual sea su forma (dict por rama u otra): que no quede ninguna sin revisar en silencio.
> F2 · Regenerar las láminas de la 7a. Fila de exposiciones antes. Ensayo en un clon desechable y después, con el MISMO orden de sesiones que clave.txt de laminas-sesion-7a (léelo de ahí; no lo escribas en el repo):
> uv run botsito motor laminas --sesiones <las seis de clave.txt, en su orden> --salida C:\Users\USER\Desktop\laminas-sesion-7a-v2
> Compara v1 con v2 fichero a fichero: cuántas láminas cambian y en qué carpeta y número, y que el resto sea idéntico byte a byte. Si cambia algo más que frases de causa, PARADA.
> F3 · Sin código. En docs/sesion-7/PREGUNTAS-7A.md, la carpeta pasa a ser laminas-sesion-7a-v2 en todas las líneas que la nombran (al menos la introducción de §1, hacia :49, y el paso 4, hacia :67-69). Y en el paso 4 entra: «Las láminas de una sesión se enseñan en su orden, y el trader corrige cada una antes de pasar a la siguiente: la siguiente dice cómo acabaron las anteriores («Antes, en esta sesión: …»). Si la pantalla mide menos de 1.624 píxeles de ancho, se aleja el zoom del navegador hasta que la lámina entre entera.»
>
> INFORME en docs/validation/LAMINAS-MOTIVOS.md (sin fechas ni la clave). Revisor (agente revisor) con cuatro alcances: la tabla de 0.1 contra la spec; que los tests de F1 rompan en main o fallen a propósito como se dice; que v2 solo cambie frases de causa; que ninguna frase nueva lleve ids, dinero ni fechas. Sin CI de Linux (no toca plataforma). Termina con la PARADA final: la ruta de v2 (Aleks me la subirá en ZIP, sin clave.txt) y las líneas de cierre. PROJECT_STATE no crece: F no nombra la carpeta.
>
> Para la fila de ERRORES-RECURRENTES del cierre: importa (hallazgo del consultor en la revisión visual de las láminas de la 7a, ampliado por su auditor): las frases de RN-001, RN-020 y RN-029 nombraban un caso de un gate de varias ramas, y los gates dudosos salían como ciertos; habría dado al trader causas falsas. No lo vieron ni el revisor de trabajo/laminas ni la revisión de la v5. Lección para el revisor: cada frase de una tabla cerrada se contrasta con la forma entera de su regla y con quién enciende cada hecho, no con su título. Y menor (consultor, de la orden de cierre de F38x): dijo que en el cierre de trabajo/laminas la F anterior se pasó a HISTORIA, y no fue así. Lección: un precedente que se cita en una orden se lee antes.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-12)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/laminas-motivos (2026-11-12). Cópiala tal cual al final del encargo y del informe, con su fecha, y aplícala punto por punto (skill fase-cero). Buena fase 0: las cuatro desviaciones de «Lo que cambia» quedan aceptadas (la rama se deduce de la foto, con LaminaError si no se identifica; el test F1 (2) con RN-020 y RN-029 juntas en la foto, que es el caso real; el arreglo del filtro del test de frases dentro de F1; y lo que esperas en v2). La fila de exposiciones del 2026-11-11 escrita pasada la medianoche queda aceptada como desviación declarada: lo que se leyó (clave.txt) son días de construcción.
>
> 0. RN-008: de acuerdo. La frase se queda, y el informe y la tabla de 0.1 declaran sus dos condiciones y que con el valor actual de orden_limite_nace no dispara.
> 1. De acuerdo: el contrato se amplía a tests/unit/test_laminas_svg.py.
> 2. Publícalos. Con ADR-0093 §2 el trader carga él mismo el día, así que la clave ya no protege ninguna fecha que él no vea. Es lo mismo que se decidió en el cierre de F38x (respuesta a su PARADA final, punto 3), y la fase 0 ya los nombra.
> 3. Que entre la frase, pero la regla se aclara en el ADR, que es la fuente, y no solo en la hoja: un recuadro fechado en ADR-0093 §2, con la forma de los recuadros de ADR-0084. Su texto: «"Ningún resultado se enseña" quiere decir ningún resultado posterior al corte. Lo que la lámina dice de cómo acabaron las órdenes anteriores de la misma sesión ("Antes, en esta sesión: …") es el estado del bot en el instante del corte (sus intentos, RN-016) y se enseña, porque explica la decisión. Por eso las láminas de una sesión se enseñan en su orden, y el trader corrige cada una antes de ver la siguiente.» El paso 4 de PREGUNTAS-7A.md dice «ningún resultado posterior al corte» y remite al recuadro. El contrato se amplía a docs/adr/0093-*.md, solo con ese recuadro.
> 4. De acuerdo: 1.648 píxeles, medido.
> 5. De acuerdo: recuadro de corrección en docs/runbooks/LAMINAS.md, en su tabla, y el contrato se amplía a ese fichero.
> 6. De acuerdo: en el cierre, una frase en R4.5 que remita a LAMINAS-MOTIVOS.md, comprobada con problemas_a a problemas_d.
>
> Sigue sin parar con F1, F2 y F3 y la PARADA condicional: solo paras si v2 cambia algo más que la línea de RN-001 de sesion-06/09 y sesion-06/10, si una foto de las seis sesiones da LaminaError con el arreglo, o si una guardia niega algo legítimo. Después, el revisor con sus cuatro alcances más uno: que el recuadro de ADR-0093 diga lo del punto 3 sin añadir ni quitar. Luego, la PARADA final con la ruta de C:\Users\USER\Desktop\laminas-sesion-7a-v2 y las líneas de cierre.
>
> Rama lista para revisión, NO cerrada.
