# Encargo · trabajo/hoja-sesion-05

Dado por Aleks (consultor) el 2026-10-22. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/hoja-sesion-05 (NA:V, hoja de ruta R4.1, tramo R4), desde main en 7e6dec2 (el commit de estado sobre el merge e4563db, que es al que apunta el tag stable/F37y-previa-sesion-5). Verifica con git las tres cosas y que no hay otra rama abierta; si algo no cuadra, para y avísame. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con la fecha de hoy.
>
> POR QUÉ ESTA RAMA, Y POR QUÉ HOY
> La sesión 5 con el trader es mañana, viernes 2026-10-23, y su ingesta va después. La guardia solo da por revisado un guion idéntico al de main (.claude/hooks/guardia.py, _igual_que_en_main): si el alta de la sesión 05 en scripts/transcribir_sesion.py se hiciera en la rama de la ingesta, la guardia negaría ejecutarlo sobre la cruda, y con el guion de main la filtrada se agruparía con la hoja 04, donde S-25 no existe. Es lo que pasó en la sesión 4 (docs/validation/SESION-04-EXTRACCION.md §1.2). Esta rama deja la hoja 05 en main antes de grabar.
>
> OBJETIVO
> 1. Dar de alta la sesión 05 en scripts/transcribir_sesion.py.
> 2. Escribir en docs/runbooks/DECISIONES-DE-PROCESO.md la regla del consultor del 2026-10-21 para los encargos, que hoy solo vive en docs/encargos/trabajo-previa-sesion-5.md y en PREVIA-SESION-5.md.
>
> QUÉ NO CAMBIA
> El motor, la spec, las ambigüedades, el feedback, los casos, el corpus, fuentes.yaml y la cuarentena (v15 entra con la ingesta, no aquí). docs/sesion-5/PREGUNTAS.md no se toca. Esta rama no lee ningún material del punto 3 de CLAUDE.md, ni transcripciones, ni fotogramas; si por algo tuvieras que hacerlo, PARADA.
>
> REGLAS DE ESTA RAMA
> - Si la guardia o el clasificador niegan un comando: PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.
> - La CI no se consulta con un guion ni con un bucle: un gh run view suelto cada vez.
>
> FASE 0 (sin escribir código; entrega en el informe, sin PARADA salvo sorpresa)
> Mide y apunta, con fichero:línea:
> - cómo usan los códigos codigos_validos, HOJAS, CODIGOS_DE_SESION_TEXTO, orden_de_preguntas, registro_filtro y la opción --sesion (sus choices salen de HOJAS);
> - qué tests fijan la sesión en curso o la hoja 04 (verifica tests/unit/test_transcribir_sesion.py, que hoy afirma SESION_EN_CURSO == "04");
> - qué documentos nombran la sesión en curso o la opción --sesion por defecto (la skill ingerir-sesion, SESION-DE-PREGUNTAS.md, MIRAR-EL-MATERIAL.md) y si alguno queda falso con el cambio.
> Si algo de esto pide más que lo de abajo, PARADA con tu propuesta.
>
> FASE 1 · LA HOJA 05
> - ORDEN_SESION_05 = S-1 a S-25 en el orden de la hoja (verifica que en PREGUNTAS.md el orden de los bloques es el numérico). Comentario encima: los códigos son los de la sesión 5, no los de la 04; si en la sesión se salta alguno, la filtrada lo lista entre los «sin código detectado», y el orden real y lo que no se preguntó van a docs/sesion-5/HOJA-USADA.md con la ingesta.
> - CODIGOS_DE_SESION_TEXTO["05"]: el texto de cada código es el título de su pregunta en PREGUNTAS.md, sin el prefijo «S-n. » y sin lo que va detrás del cierre de la negrita (en S-7, «· en parte · A-48 y» y lo que sigue en la línea siguiente; en S-1, la negrita ocupa dos líneas y se toma entera), con la primera letra en minúscula como en la 04; salvo S-7 y S-12, que toman el «Título» de su RECUADRO DE CORRECCIÓN del 2026-10-21. S-13 y S-15 conservan su título.
> - HOJAS["05"] = ORDEN_SESION_05 y SESION_EN_CURSO = "05".
> - Las sesiones 03 y 04 siguen agrupando exactamente igual.
> - Con la hoja por defecto en 05, una re-filtrada de v9 o v10 sin --sesion se agruparía en silencio con la hoja 05. Corrige el ejemplo del docstring del guion (hoy «--video v10 --solo-filtrar» sin --sesion) y deja escrito, en el docstring y en el informe, que v9 se filtra con --sesion 03 y v10 con --sesion 04.
> - El test que hoy fija SESION_EN_CURSO == "04" se parte: el orden de la 04 se queda en su test y la sesión en curso pasa al test de la 05.
> - Tests, cada uno roto a propósito en los dos sentidos y con las dos salidas en el informe: que la hoja 05 tiene los 25 códigos con su texto; que S-25 es válido en la 05 y no en la 04; que la 03 y la 04 no cambian; y el de SESION_EN_CURSO actualizado.
> - Si un documento de la fase 0 queda falso, se corrige en esta rama; si es un informe cerrado, con un recuadro.
>
> FASE 2 · LA REGLA DEL 2026-10-21
> En docs/runbooks/DECISIONES-DE-PROCESO.md, sección «Decisions and Rationale», con el formato de sus entradas, una entrada con fecha 2026-10-21 que diga que nace aquí y no viene de la mudanza de PROJECT_STATE. Dos frases, cada una con su origen (verifica cada cita):
> - «Si la guardia o el clasificador niegan un comando, PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.» Origen: docs/encargos/trabajo-previa-sesion-5.md, PREVIA-SESION-5.md y el antecedente de EA-CONEXION.md.
> - «Ninguna consulta de la CI con un guion ni con un bucle.» Origen: EA-CONEXION.md §13 y su fila de hallazgos, la orden de cierre de SESGO-H4-COLOR.md («cambiar de vía tras una negativa es rodearla») y la línea de Technical Debt de PROJECT_STATE sobre el guion que espera a la CI, que sigue abierta para el carril de guardias.
> Si algún test exige que esto viva en otro sitio, PARADA.
>
> CIERRE DE LA RAMA
> Informe en docs/validation/HOJA-SESION-05.md. make check sellado; push a fix/hoja-sesion-05 (git push origin trabajo/hoja-sesion-05:refs/heads/fix/hoja-sesion-05) y CI de Linux con solo el fallo esperado de state check; dame el número de run. Después el revisor, lanzado con el informe YA TERMINADO, y su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
