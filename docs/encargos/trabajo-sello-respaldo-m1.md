# Encargo · trabajo/sello-respaldo-m1

Dado por Aleks (consultor) el 2026-11-07, en un solo mensaje. Copiado tal cual (el bloque
`ids-inexistentes` es el que trae el propio encargo; declara ADR-0091, que crea la fase 1 si la
regla D2 da «límite del respaldo», y sale en el mismo commit que lo crea):

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-07) · trabajo/sello-respaldo-m1 · tramo «R3 · Una corrida del arnés sobre toda la construcción» (R3.6 de la hoja de ruta; H de la Next Action). Rama de noche: corre sola, con las decisiones por adelantado y PARADA condicional. NUNCA cierra.
>
> ```ids-inexistentes
> ADR-0091 — lo crea la fase 1 de esta rama si la regla D2 da «límite del respaldo»; el bloque sale en el mismo commit que lo crea (si no se crea, el bloque se queda y el informe lo dice)
> ```
>
> Rama nueva: trabajo/sello-respaldo-m1, desde main tras el cierre de trabajo/demo-ejecuciones-2-3. Antes de nada, comprueba con git que main es el commit docs(state) de ese cierre, que el tag stable/F38p-demo-ejecuciones-2-3 apunta a su merge, que la CI de main de ese commit está en verde (un gh run view suelto, sin bucle) y que no queda otra rama. Si algo de eso falla, PARA sin tocar nada y dilo. Ábrela con abrir-rama: contrato con tramo "R3 · Una corrida del arnés sobre toda la construcción" (entre comillas), riesgo alto (toca el respaldo M1 del bróker simulado), artefacto docs/validation/SELLO-RESPALDO-M1.md. El recorrido lo mandan fase-cero, comparar-con-main y entregar-rama; si chocan con este encargo, ganan ellas y lo dices. Antes de usar el número 0091, grep de «0091» en docs/ y en Technical Debt.
>
> Objetivo: decidir y aplicar lo de la entrada H: (e2), que corrige la marca adelantada de _peor_del_minuto, y qué se hace con los 22 eventos del respaldo M1 que se sellan en el cierre de su vela, un milisegundo después de que el motor decida.
>
> NO cambia: la estrategia, strategy_spec.yaml, parametros.yaml, el perfil de FTMO, ADR-0053, nada de knowledge/ salvo lo que diga una decisión de abajo. No se toca corpus, holdout ni material del trader. Solo días del material de desarrollo (enero, abril, julio y agosto), comprobados antes con casos_reservados(repo) y declarados el mismo día en HOLDOUT-EXPOSICIONES.md como manda CLAUDE.md.
>
> REGLA DEL CONSULTOR PARA ESTA RAMA (2026-11-07): NINGUNA CORRIDA DEL ARNÉS sobre la construcción entera, ni la que cuenta (ADR-0070 §3) ni la diaria con --diagnostico-cuenta-diaria, y ninguna cifra agregada nueva (cobertura, precisión, veredicto, recuentos sobre el mes o sobre toda la construcción). Porqué: R3.7 pide que el consultor fije los umbrales de la rama de método (R) «antes de ver ninguna corrida nueva», y el orden es H → R → la re-corrida que cuenta. El comportamiento se comprueba con tests, con las sondas y con días concretos de construcción (uv run botsito motor visor --caso <id> --simular, con --hasta HH:MM si hace falta; verifica sus argumentos en cli.py; nunca --todos ni --meses). Leer las salidas ya commiteadas de docs/validation/anexos/RESPALDO-M1/ para localizar los 22 sí vale: ya se vieron y no son una corrida nueva. Las «dos corridas repetidas» del «Hecho cuando» de R3.6 pasan a la re-corrida que cuenta, después de R: línea preparada para el cierre.
>
> Herencias que entran (cada una se cumple o se dice por qué no):
> - La entrada H entera: lo que el auditor de RESPALDO-M1 encontró en «sellar en k fin − 1» (las marcas y m1_entre del break even empiezan a contar la vela del llenado; cambia la sesión de un llenado en la última vela de 07-11; cambian el fin de la ventana y el borde de ADR-0068; rompen tests de main por el milisegundo).
> - R3.6 de la hoja de ruta (RESPALDO-M1.md §0.a y §0.l).
> - RESPALDO-M1.md, punto 27 y hallazgo b2: _peor_del_minuto va a H con su sonda 5 (docs/validation/anexos/RESPALDO-M1/sonda_z.py) y con la sonda y el prototipo en memoria del auditor del consultor (RESPALDO-M1.md §0.l y :448), que no están en el repo (:1097).
> - censo_cierre.py, el guion que contó los 22 (RESPALDO-M1.md:351), tampoco está en el repo.
> - La lección de RESPALDO-M1 (:494): antes de mover un instante, grep de TODOS los lectores de abierta_ms y del minuto del evento. Las líneas de broker.py que cita esa respuesta (:888, :909-913) ya no cuadran con main: vuelve a localizarlas.
> - El diagnóstico de H hecho sin rama el 2026-10-31 (diagH\, en el scratchpad de una sesión anterior de Claude Code, bajo %LOCALAPPDATA%\Temp\claude\; busca INFORME-DIAG-H.md). Léelo en solo lectura donde esté; si la guardia lo niega o no aparece, sigue sin él (esta rama vuelve a medirlo todo) y dilo. Lo que el consultor tiene apuntado de él, para que lo VERIFIQUES y no lo copies: (e2) es una línea en _peor_del_minuto y no rompe nada; (c2) = sellar en k fin − 1 + (e2) + leer el minuto de apertura con «+1», rompe 10 tests de main, enmienda ADR-0051 §5 y ADR-0057 §1 y toca unos 6 lectores de abierta_ms; (d) rompe 17 y toca ADR-0053. Se midió sobre un main anterior y con la comisión a 5: nada de sus cifras entra como dato sin volver a medirlo sobre este main (comisión 2,50, ADR-0090).
> - Busca además «a H», «para H», «NA:H» y «R3.6» en RESPALDO-M1.md, en ACTIVAR-SESION-06*.md y en el final de HISTORIA, y añade lo que falte.
>
> FASE 0, inventario sin commitear cambios de código. Para medir (c2) y (e2) sin tocar src/: un prototipo en memoria, como el del auditor de RESPALDO-M1, en un guion de docs/validation/anexos/SELLO-RESPALDO-M1/ que parchea las funciones en tiempo de ejecución y llama al visor por caso; si la guardia lo niega, PARADA para eso con el comando exacto, sin rodearla. comparar-con-main se usa como manda su skill (con lo ya commiteado y los tests de la rama copiados al clon de main):
> a) diagH: qué dice, y cada afirmación suya contrastada con este main.
> b) Los 22: de dónde salen (RESPALDO-M1.md §0.l y :351: 22 de 1002 cancelaciones en el cierre de una M1 sin ticks, en la corrida 2, contados con censo_cierre.py, que no está en el repo), y la lista de eventos (día, caso, sesión, orden, qué hizo la vela k), sacada de nuevo de la salida diaria ya commiteada (docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt) con un guion nuevo en docs/validation/anexos/SELLO-RESPALDO-M1/ (o censo_respaldo.py, si sirve). Si no salen 22, gana tu recuento y lo dices. Todos tienen que ser días del material de desarrollo (CLAUDE.md: enero, abril, julio y agosto): compruébalo con casos_reservados(repo); si alguno no lo es, ese evento no se mira y lo dices.
> c) EL CENSO, evento por evento, con el código de main y con (c2) en el prototipo en memoria, por caso con el visor: ¿cambia una OPERACIÓN del bot (entra o no entra, el lado, la vela de entrada o el resultado en R) o solo el instante o el tipo de un evento que no cambia ninguna operación? Por día, nunca agregado sobre el mes.
> d) Lo de la entrada H medido con (c2): marcas y m1_entre del break even, la sesión del llenado en la última vela de 07-11, el fin de la ventana y el borde de ADR-0068, y los tests de main que rompe (cuántos y cuáles; H decía 5 y diagH 10).
> e) Los lectores de abierta_ms y de _peor_del_minuto, con fichero:línea.
> f) (e2) en el prototipo: el diff que se commiteará, los tests de main que rompe (si alguno) y la sonda 5 convertida en un test que rompe en main y pasa con (e2).
> g) Las líneas del cierre, preparadas sobre una copia, según el caso que salga de D2: H (sale HECHA o se queda reescrita), F, R3.6 (su «Hecho cuando» sin las dos corridas, que pasan a la re-corrida que cuenta), R3.7 si hace falta y Technical Debt; con test_hoja_de_ruta y test_project_state en verde y la previsión de PROJECT_STATE con wc -c, por debajo de 23.000.
>
> DECISIONES DEL CONSULTOR, POR ADELANTADO (2026-11-07):
> D1. (e2) se aplica en esta rama pase lo que pase con los 22: su línea en _peor_del_minuto y el test de la sonda 5, que rompe en main y pasa en la rama (salida contra main pegada). Si (e2) rompe algún test de main o cambia algo más que la marca de _peor_del_minuto, PARADA solo para (e2).
> D2. Los 22. Regla escrita antes del censo: si NINGUNO cambia una operación del bot en ningún día de construcción (entra o no, lado, vela de entrada, resultado en R), se declaran LÍMITE DEL RESPALDO: no se aplica (c2), y ADR-0091 enmienda ADR-0051 §5 y ADR-0057 §1 declarando el límite (qué pasa, por qué, el alcance medido: 22 eventos y 0 operaciones cambiadas, y que el bot en vivo opera con ticks, no con el respaldo), con recuadro en los dos ADR y fila en el índice, y un test que fija el comportamiento actual con un nombre que diga que es un límite declarado. Si AL MENOS UNO cambia una operación, o el censo no puede decidirlo para alguno (negar por defecto: cuenta como que cambia), el camino es (c2), pero NO se implementa en esta rama esta noche: PARADA con el plan (borrador de ADR-0091 en el informe, los tests que rompen, los lectores que toca y lo de d)), porque enmienda dos ADR y toca varios lectores.
> D3. (d) está descartada.
> D4. Nada de corridas agregadas (la regla de arriba). Si para decidir algo te faltara una, PARADA para eso, sin correrla.
> D5. La sonda y el prototipo del auditor del consultor no están en el repo: se reconstruyen desde su descripción en RESPALDO-M1.md (§0.l y la respuesta del consultor), y lo que no se pueda reconstruir se declara perdido; no se inventa.
>
> PARADA CONDICIONAL: entrega la fase 0 en el informe y commitéala (skill fase-cero). Luego, sin esperarme: si D2 da «límite del respaldo», sigue con la fase 1 entera; si da (c2), aplica solo D1 en la fase 1 y para con el plan de (c2). Lo que contradiga una decisión de arriba se para; lo demás sigue si no depende de ello. Nunca cierres.
>
> FASE 1, un commit por punto, cada uno con estadiar, uv run botsito state check, make check > make-check.log 2>&1 y leer el log (exit 0, ningún failed y la línea SELLO); antes, ruff format, ruff check y mypy sobre lo tocado:
> 1) (e2) y su test de la sonda 5.
> 2) Si D2 da límite: ADR-0091 con los recuadros de ADR-0051 §5 y ADR-0057 §1 y sus filas del índice (el bloque ids-inexistentes sale en este commit), y el test del límite declarado.
> 3) El informe con las líneas del cierre preparadas.
> Si la guardia o el clasificador niegan algo legítimo, PARADA para eso con el comando exacto (lo lanza Aleks con «!» por la mañana) y sigue con lo demás.
>
> TESTS QUE ROMPEN A PROPÓSITO: el de la sonda 5 (falla en main, pasa con (e2)), con su salida contra main pegada; el del límite declarado no rompe en main a propósito: fija el comportamiento, y el informe lo dice.
>
> CI: la rama toca src/ del motor pero no hooks, rutas, .claude/ ni plataforma: sin fix/. Si acabaras tocando alguno de esos, empuja fix/<rama> y pega el run.
>
> INFORME en docs/validation/SELLO-RESPALDO-M1.md: el encargo punto por punto, la fase 0, el censo evento por evento, lo que no pudiste medir, las líneas del cierre preparadas y la fila de ERRORES-RECURRENTES preparada con este error del consultor: «(importa, del consultor) el plan del 2026-11-01 mandaba a H "las dos corridas del arnés", y R3.7 pide fijar los umbrales de R antes de ver ninguna corrida nueva. Lección: antes de mandar una corrida, mirar si hay un umbral pendiente de pre-registrar.» Pasa el revisor (subagente revisor, opus) con estos alcances: reglas de la casa, encargo, que no haya ninguna corrida agregada ni cifra agregada nueva, que todos los días mirados sean de construcción y estén declarados, y que (c2) no esté aplicado. Pega su informe al final.
>
> Rama lista para revisión, NO cerrada.
