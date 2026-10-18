# Encargo · trabajo/sesgo-h4-color

Dado por Aleks (consultor) el 2026-10-17. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: trabajo/sesgo-h4-color (NA:W, hoja de ruta R1.2). Encargo del consultor, 2026-10-17.
>
> 0. Apertura
> - Base: main 59c8ae7, el commit de estado sobre el merge fa15a84 (stable/F37q-corrida-construccion). Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de 59c8ae7 la dio verde el cierre (run 38656985715, que no está escrito en el repo): compruébala con gh; si el clasificador niega gh, PARADA y la consulto yo con «!». Nunca con curl ni con un guion.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R1.
> - Informe: docs/validation/SESGO-H4-COLOR.md. Anexos: docs/validation/anexos/SESGO-H4-COLOR/.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0 y su PARADA; activar-sesion para registrar y activar la respuesta (cubre las llegadas por escrito fuera de sesión); entregar-rama al final.
>
> 1. Objetivo
> Activar en la spec y en el motor la regla del sesgo de H4 que el trader respondió por WhatsApp el 2026-10-14 (literales en la entrada W de PROJECT_STATE), con su ADR, sus registros de feedback y su evidencia, y volver a correr el arnés con los tres comandos de R3.1.
>
> La regla confirmada (gráfico de cuatro casos, «Si, esta bien bro», 15:18 hora de Lima): una H4 cambia el sesgo solo si rompe el extremo de la anterior (con mecha o con cuerpo) Y cierra del color de esa ruptura. Rompe el bajo y cierra roja: bajista. Rompe el máximo y cierra verde: alcista. Rompe un extremo y cierra del color contrario: no cambia, sigue el sesgo que había.
>
> 2. Decisiones del consultor (van al ADR con esta fecha; si la fase 0 mide algo que las contradiga, PARADA)
> D1. Ruptura simple con el color contrario: la vela NO decide y la búsqueda hacia atrás de ADR-0044 §2 sigue, igual que hoy con la neutra de doble ruptura (ADR-0075). Es lo que dice el gráfico: «sigue el sesgo que había».
> D2. Doble ruptura: el resultado no cambia. ADR-0060 §1 (decide el color) y la neutra de ADR-0075 ya son casos de la regla nueva.
> D3. Ruptura simple con una vela SIN CUERPO (cierre igual a apertura): el trader no la describió. Decisión del consultor: no decide y la búsqueda sigue, porque la regla pide cerrar del color de la ruptura y una neutra no tiene color; es la lectura de S-13 (ADR-0075), con su reserva: el trader la dijo solo con un sesgo previo alcista. El ADR la marca como decisión del consultor y va como pregunta de confirmación a la sesión 5 (V), en la lista «Para el cuestionario de la sesión 5» del informe.
> D4. El extremo de la anterior es su máximo o su mínimo (la línea discontinua del gráfico está en la mecha), y romperlo con mecha o con cuerpo equivale a superarlo con la mecha. sesgo_h4_criterio_ruptura se queda en mecha y en CONFIRMED (resuelve lo que CORRIDA-CONSTRUCCION.md:1316 dejó a esta rama). El ADR lo justifica con el WhatsApp y con lo que el trader ya había dicho de la mecha (fb-…-41f46b21, que cierra A-1, y ev-v9-001312-19e45e4a; verifica los dos), no con la idea de que «mecha» fuera solo una re-expresión del consultor, que es inexacta. Y dice por qué no aplica aquí la lección de ERRORES-RECURRENTES.md:84 (una re-expresión que añade un criterio va como DEFAULT_AMBIGUOUS): el criterio lo dijo el trader.
> D5. La exigencia del color NO es un parámetro ni un interruptor de diagnóstico: es la definición del trader, como el color de la doble ruptura en ADR-0060. La comparación con lo de antes se hace contra las salidas commiteadas de R3.1.
> D6. ADR nuevo (verifica que el siguiente libre es 0080). Enmienda, cada una con su recuadro como hizo ADR-0075: ADR-0060 §1 («Con un solo extremo roto, el color sigue sin decidir nada»), ADR-0044 §2 («la última H4 que rompió un extremo») y su alternativa descartada «el color de la vela NO decide», y ADR-0075 §3 («con un solo extremo roto el color no decide»). Si la fase 0 encuentra otro ADR que lo contradiga, PARADA.
> D7. Feedback, dos registros nuevos y ninguno supersede a fb-2026-09-09-sesion-01-8eccf5c0 (supersederlo rompería knowledge validate en las cinco citas que lo usan): un CORRECT sobre RN-003 (precedente: fb-2026-10-04-sesion-04-ca0afae6, que es lo que RN-003 cita hoy) y un CONFIRM sobre sesgo_h4_criterio_ruptura con valor mecha, que pasa a ser su fuente, aplicado con feedback apply --check. Los dos con procedencia trader_escrito, medio escrito, recibido_el 2026-10-14. A qué carpeta de sesión van (la P1 de R3.1 no se hizo en ninguna sesión; A-42 usó la de su pregunta): propuesta en la PARADA. sesgo_h4_regla (que ninguna forma lee desde F12) no se borra: solo se actualiza su descripción para decir que la regla vigente es la de este ADR.
>
> 3. Lo que NO cambia
> - Ningún otro parámetro, ninguna cifra (sesgo_h4_tope_velas sigue en 60), ninguna otra regla ni la geometría de M15 y M1.
> - El simulador, la cuenta, el bróker y el arnés salvo la anotación de 4.f.
> - Los anexos y los informes cerrados (CORRIDA-CONSTRUCCION, MOTOR-SESGO-H4, SESGO-H4-DIAGNOSTICO.txt y anteriores): no se editan ni se reescriben sus salidas; si un guion cerrado (scripts/sesgo_h4_diagnostico.py, los de anexos) da otra cosa con el motor nuevo, el informe lo dice y no se toca.
> - Las guardias, .claude/ y el Makefile. Si algo obliga a tocar el Makefile, PARADA: con el Makefile cambiado la guardia niega todo make a la sesión y esos make check los lanzo yo con «!».
> - PROJECT_STATE, salvo lo que haga el ritual. Está en 24.359 bytes y el tope es 25.000: la rama no lo engorda.
>
> 4. Fase 0 (inventario sin tocar nada; entrega y PARADA antes de escribir código)
> a. Todo lo que lee, nombra o contradice la regla, con fichero:línea y qué cambia: domain/sesgo.py; engine/primitivas.py (escribe sesgo_h4_doble_ruptura) y lo que cuenta arnes.py; engine/visor.py; los guiones de scripts/ que llaman a sesgo_h4; en strategy_spec.yaml, los predicados rompe y sesgo_h4_al_abrir, RN-003 (entonces, que dice «según sesgo_h4_regla», notas, que hoy dicen lo contrario, y cita) y RN-033; el término «equal» de glossary.yaml, que cita 8eccf5c0; los dos parámetros; y docs/spec, que se regenera.
> b. Los tests que la regla cambia de resultado. Medido por el auditor del consultor con el parche aplicado: fallan siete de test_sesgo_h4.py (rompe_arriba…el_color_no_decide, rompe_abajo_es_bajista, un_equal_no_rompe, una_neutra_mantiene_el_sesgo_anterior, los dos casos de semana_de_desfase y semana_normal), porque el ayudante h4() cierra verde por defecto y las velas del cambio de hora rompen abajo cerrando verdes. Verifícalo y di cómo se rehace cada uno conservando lo que comprobaba (el color explícito), sin rebajar ninguno.
> c. Lo que el trader dijo antes sobre el cambio de sesgo y puede chocar con la regla: las evidencias de A-1 ev-v3-010948 («cambio_exige_cierre_bajo_mecha»), ev-v3-011045 («cambio_exige_cierre_encima») y ev-v4-004603, más 41f46b21 y ev-v9-001312 de D4. Léelas como evidencia (no hay cuarentena en v3, v4 ni v9; si alguna cita cae en un tramo no citable, dilo y no la abras) y di si alguna contradice la regla de WhatsApp. Si alguna la contradice, PARADA: eso va al detector de contradicciones y a la sesión 5, no se decide aquí.
> d. El registro (D7): carpeta de sesión, objetivo, acción y valor de cada registro, y qué pasan a citar RN-003, el predicado sesgo_h4_al_abrir, el término «equal» y sesgo_h4_criterio_ruptura (rompe se queda como está si ninguna regla lo invoca; dilo). Por el precedente de trabajo/activacion-a42 (ACTIVACION-A42.md §1.1 y la respuesta D1 a su PARADA, :476 y :494).
> e. La evidencia. En corpus/whatsapp-sesgo-h4-2026-10-14/ (fuera de git) hay seis ficheros que entran; el LEEME.md y la subcarpeta ws/ NO entran (ws/ es una copia que borro yo, con el zip de corpus/). Lista sin abrir nada (la guardia no deja abrir imágenes, ADR-0038) nombre, tamaño y sha256 de los seis, y prepara los mv, que lanzo yo con «!», a «corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/» (la subcarpeta que fuentes.yaml describe dentro de «Material adicional de su operativa») con estos nombres:
>    2-whatsapp-1445-primera-respuesta.png → mensaje-whatsapp-2026-10-14-1445-primera-respuesta.png
>    3-whatsapp-1448-pide-grafico.png → mensaje-whatsapp-2026-10-14-1448-pide-grafico.png
>    4-whatsapp-1455-regla.png → mensaje-whatsapp-2026-10-14-1455-regla.png
>    6-whatsapp-1518-confirma.png → mensaje-whatsapp-2026-10-14-1518-confirma.png
>    1-grafico-pregunta-dos-casos.png → grafico-consultor-2026-10-14-pregunta-dos-casos.png
>    5-grafico-regla-entendida-cuatro-casos.png → grafico-consultor-2026-10-14-regla-cuatro-casos.png
>    Los dos gráficos son esquemas dibujados por el consultor, no días reales, y fuentes.yaml lo dice. Los literales los transcribió el consultor y los volvió a leer contra las capturas el 2026-10-17; registrado_por lo dice con la ruta y el sha256 de cada captura, con la fórmula de A-42. Ningún nombre ni número del trader entra al repo. La captura de las 14:55 deja ver además una nota de voz de 0:21 a las 14:56 que no se ha transcrito: no se registra ni se interpreta, y el informe lo dice.
> f. El arnés: qué hace falta (campo nuevo en ResultadoSesgo y su anotación en primitivas.py) para contar por sesión las H4 saltadas por color contrario (D1) y por neutra simple (D3), como hoy sesgo_h4_doble_ruptura.
> g. Lectura de material de la re-corrida: la misma que declaró R3.1 el 2026-10-14 (HOLDOUT-EXPOSICIONES.md:52-53: el calentamiento de arnes.dias_de_mercado lee el M1 entero de marzo y de junio). Se declara con su fila el mismo día de la corrida y ANTES de correrla.
> PARADA con a-g, las propuestas de D7 y e, y todo lo que la fase 0 contradiga de este encargo.
>
> 5. Fases tras mi respuesta
> Fase 1 · Evidencia y feedback. Tras mis mv: corpus inventory, fuentes.yaml y manifest.yaml (solo se añaden líneas; los seis sha256 casan con la fase 0); los dos registros con feedback new, feedback apply --check y knowledge validate en verde.
> Fase 2 · Tests primero, en rojo sobre el código de main, con el recuento de FAILED en el informe: los cuatro casos del gráfico (1 y 2 bajista; 3 y 4 «sigue el sesgo que había», con una H4 detrás que fije el contrario para que se vea que sigue y no que da INSUFICIENTE); los mismos al revés para el alcista; la ruptura simple neutra de D3; color contrario sin nada detrás dentro del tope, INSUFICIENTE; varias seguidas de color contrario; doble ruptura sin cambios; con criterio cuerpo la regla también vale; y sin mirar el futuro. Los siete tests de 4.b, rehechos.
> Fase 3 · Motor y spec, como manda activar-sesion: domain/sesgo.py, primitivas.py y la anotación de 4.f; RN-003, el predicado sesgo_h4_al_abrir, el término «equal» y la descripción de sesgo_h4_regla; el ADR de D6 con sus tres recuadros; spec_version subida, spec manifest --escribir y spec docs --escribir en el mismo commit; las tres guardias de spec/modelo.py si un sitio nuevo gana cita; trailer Fuente: con los ids nuevos. Tests en verde y make check sellado.
> Fase 4 · Re-corrida. Antes, la fila de HOLDOUT-EXPOSICIONES de 4.g. Los tres comandos de R3.1 (CORRIDA-CONSTRUCCION.md:571-577), tal cual salvo la carpeta de --salida (el arnés añade al nombre el sufijo DIAGNOSTICO…):
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/SESGO-H4-COLOR/arrastrada.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/SESGO-H4-COLOR/diaria.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/SESGO-H4-COLOR/a35-inicio.txt
>    En el informe, frente a R3.1: en cuántas sesiones de construcción cambió el sesgo y por qué regla (D1, D3), cuántas pasan a INSUFICIENTE, y la tabla T0 y P1-P7 contada con patrones.py de CORRIDA-CONSTRUCCION (lee la ruta por argumento; no se copia ni se toca). Ni la fecha ni el precio de la H4 que fija el sesgo: puede ser una vela de calentamiento de un día reservado (lección de ERRORES-RECURRENTES.md:84, incidente a1). Es diagnóstico (ADR-0070 §3), como R3.1: no decide ningún parámetro, no habilita mayo y no se mide cobertura contra ningún umbral. Si el clasificador o la guardia niegan un comando, PARADA y lo lanzo yo con «!»; no se rodea con curl, otro guion ni una función interna.
>
> 6. Informe y entrega
> - SESGO-H4-COLOR.md: el encargo punto por punto con su evidencia, las desviaciones declaradas, las salidas de la fase 4 y la lista «Para el cuestionario de la sesión 5» con la pregunta de D3 (sin fechas de días reservados ni resultados de holdout).
> - Líneas preparadas para el commit del contrato de la orden de cierre, medidas en bytes:
>   · W sale entera de la Next Action a HISTORIA con su texto literal, bajo un título que no se confunda con el «# Next Action HECHA · W» del 2026-10-10 (HISTORIA:7638); comprueba qué acepta el test.
>   · F queda: «E → O → V. La re-corrida de R3.1 tras el sesgo la hizo W (SESGO-H4-COLOR.md); si E cambia lo que simula, su encargo decide si hace falta otra.»
>   · V deja de nombrar W, y la pregunta 1 de CORRIDA-CONSTRUCCION.md §4.5 (respondida) se sustituye por la de D3.
>   · En la hoja de ruta, R1.2 pasa a HECHA, y R4.1 (HOJA-DE-RUTA.md:167, :176 y :178) deja de esperar a NA:W y a R1.2.
>   · El tamaño de PROJECT_STATE que resulta, que tiene que bajar del de hoy.
> - CI de Linux por la rama remota fix/sesgo-h4-color (trabajo/sesgo-h4-color:refs/heads/fix/sesgo-h4-color) si la rama toca hooks, rutas, el sistema de archivos o guiones que dependan de la plataforma (RITUAL.md:92-104); si no los toca, dilo con el diff de nombres.
> - Revisor (opus) con dos alcances: reglas del repo y este encargo punto por punto; su informe pegado al final. Que mire también que ninguna consulta de CI se haya hecho con curl o con un guion cuando el clasificador negó gh.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-10-17)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/sesgo-h4-color (2026-10-17). Cópiala tal cual en el informe, como manda fase-cero, y aplícala punto por punto.
>
> 0. La contradicción con v6 1:04:30-1:05:35: (a), con dos cambios.
>    - Se activa la regla del WhatsApp. Porqué: es la respuesta escrita a la pregunta exacta, cinco semanas posterior a la sesión 1, y el trader confirmó el caso 3 a propósito («sobre todo el 3 y el 4»). La contradicción queda ABIERTA y a la vista; el ADR, las notas de RN-003 y las de R1 lo cuentan.
>    - Los ítems de evidencia, con el tema de ev-v3-011045-a185d2ba en los dos, porque la guardia exige que el que supersede conserve el tema y el detector solo compara ítems del mismo tema con valor: uno que supersede a ev-v3-011045 con la misma cita y la misma afirmación, que solo añade valor (exige_color_de_la_ruptura), y uno nuevo de v6 1:04:30-1:05:35 con valor color_indiferente. Ninguno nombra el día ni el gráfico del que habla el trader. ev-v3-011045 está citado en la lista de A-1 de ambiguedades.yaml: mide antes si supersederlo rompe knowledge validate o pide tocar A-1. Si lo rompe, si evidence contradictions no abre la contradicción con eso, o si hace falta forzar algo más, se queda en (b) y se dice.
>    - La pregunta para la sesión 5 se hace con un esquema dibujado (como el caso 3), NUNCA con los fotogramas de v6 ni con los instantes de ese gráfico. Porqué: lo que el trader enseña ahí es su sesgo sobre velas en directo de días de fidelidad-1; enseñárselo y que lo explique sería pedirle una etiqueta de esos días.
>
> 0bis. La exposición de §1.j (decisión del consultor, para la fila de hoy de HOLDOUT-EXPOSICIONES). No quema: lo visto son velas y unas líneas del trader, no una operación ni una cifra del bot, y no se sabe qué vela señala. Pero ese pasaje de v6 trae el sesgo que el trader dio en directo sobre un gráfico con cuatro días de fidelidad-1, y eso se acerca a una etiqueta. Por eso:
>    - No se abren más fotogramas de ese tramo ni se cruzan las velas para averiguar qué vela señalaba. Si alguna guardia, guion o test lo hiciera, PARADA.
>    - Amplía la fila del 2026-10-17 con una línea que lo diga, y añade al informe una sección «Para F26»: el pasaje v6 1:03:48-1:05:35 (ya citado por 41f46b21 desde la sesión 1) da el sesgo del trader sobre velas en directo de cuatro días de fidelidad-1; la vela no está identificada y esta rama prohíbe identificarla. Lo decide F26 al rellenar el PREREGISTRO.
>    - Hallazgo para el cierre, no para la rama: antes de abrir un fotograma de un gráfico en directo, se mira qué días enseña por la fecha de grabación del vídeo y se comprueba con casos_reservados si alguno es reservado.
>
> 1. Carpeta de sesión de R1 y R2: (a), 2026-10-04-sesion-04, fecha 2026-10-04, recibido_el 2026-10-14. Porqué: es el precedente de A-42 y no inventa una sesión 5.
>
> 2. La cita del término equal: (a). Conserva 8eccf5c0, y la definición gana «y cerrar del color de esa ruptura (el ADR de esta rama)». Porqué: nada cita más de lo que su literal sostiene.
>
> 3. RN-033 e insuficiente: (a). Una línea en las notas de RN-033 y en la descripción del token; la forma, la cita y el cuándo no cambian. Porqué: es lo medido en §1.b, y la spec no puede decir algo que ya no es verdad.
>
> 4. El arnés: (b). También la neutra de doble ruptura de ADR-0075, en su propio campo y su propia anotación. Porqué: cuesta una línea y la fase 4 cuenta todos los saltos.
>
> 5. El literal de R1: (a), las dos burbujas de las 14:55 unidas. Los cuatro literales de la entrada W son exactos: el consultor los releyó hoy contra las capturas. Tres correcciones a mi encargo:
>    - La nota de voz de 0:21 de las 14:56 no está en la captura de las 14:55: se ve arriba de la de las 15:18 (6-whatsapp-1518-confirma.png). Corrígelo donde lo copiaste.
>    - La captura de las 14:55 trae dos mensajes más del trader que no se registran ni se interpretan: una risa a las 14:55 y, a las 14:56, una petición de que le manden el planteamiento con un gráfico. Se mencionan en las notas de R1 como contexto, sin copiarlos.
>    - Nota de voz: Aleks la escuchó el 2026-10-17 y no añade nada a la regla. No se registra.
>
> 6. A-1: (a), no se reabre. Porqué: es el precedente de ADR-0060 y ADR-0075, y reabrirla quitaría a 41f46b21, que sostiene mecha. El ADR dice que las notas de 41f46b21 («el criterio es la ruptura del extremo, no el color ni el cierre») quedan contradichas por el WhatsApp y que eso es la contradicción abierta del punto 0.
>
> 7. El recuadro de ADR-0044: (a), uno solo que cubre §2, su alternativa descartada y la nota de §1 (deuda G.2). Porqué: es el mismo fichero y la misma fila del índice.
>
> Además:
> - Se aceptan los hallazgos de §1.k: el contrato con docs/adr/README.md; la fase 1 con spec_version, spec manifest --escribir, spec docs --escribir y Fuente:; --check y después apply; el README de los anexos; ADR-0080 sin citar hasta que exista; el texto alternativo de F; R4.1 en :167, :176 y :178; feedback pending con G.2; y no volver a correr guiones cerrados.
> - D4: el ADR cita también ev-v9-000902-25db5bf5 («con mecha o con cuerpo»). ERRORES-RECURRENTES.md:84 y CORRIDA-CONSTRUCCION.md:1315 no se tocan, como dices.
> - Sigue con la fase 1. Los mv de §1.e los lanzo yo con «!» cuando me los pidas, cada uno en su línea.
>
> Rama lista para revisión, NO cerrada, al terminar la fase 4 y el revisor.

## Orden de cierre del consultor (2026-10-17)

Copiada tal cual:

> Modelo: Fable 5.1 (la sesión de la rama) · Esfuerzo: alto
>
> Orden de cierre de trabajo/sesgo-h4-color (2026-10-17), tras la revisión del consultor. Cópiala tal cual al final de docs/encargos/trabajo-sesgo-h4-color.md y a SESGO-H4-COLOR.md, §10, bajo «Orden de cierre del consultor». Después lanzo yo /cerrar-rama trabajo/sesgo-h4-color, sola en una línea.
>
> Veredicto: rama aceptada. La regla del color está en la spec y en el motor con ADR-0080, dos registros y su evidencia en el corpus; la re-corrida es diagnóstico y no cambia las parejas (12). Las dos decisiones que me dejas:
>
> 1. Paso 0, ANTES del commit del contrato: el hallazgo a1 se resuelve con una retirada (ADR-0041 §1); limpiar el texto vivo no basta.
>    Porqué: los commits 1030a4d a 37ae53f escriben el rango de días del gráfico en directo de v6 junto con cuántos de ellos tienen caso en fidelidad-1, la historia no se reescribe y el push lo publica. Con el día de grabación de v6 ya público (cdcf58e), eso deja deducible qué días de septiembre son reservados. Es el precedente de v6 (2026-09-23) y del día de holdout-3 (7f8322a, 2026-10-14). Corrijo mi 0bis en lo que toca: lo que se VIO en los fotogramas no quemaba; lo que quedó ESCRITO en git obliga a retirar.
>    a) Retira de su partición TODOS los días con caso reservado entre los días laborables que enseñaban los tres fotogramas de v6 (los que contó la fila del 2026-10-17 en 1030a4d), salvo el que ya esté retirado. Cuántos son, con un guion de la carpeta de trabajo sobre casos_reservados y casos_retirados que NO imprima ids ni fechas, solo recuentos por partición. Lo esperado: hasta cuatro, de los que el día de grabación de v6 quizá ya está retirado.
>    b) Un commit propio en esta rama (feat(holdout): retirar los dias de fidelidad-1 expuestos en la rama, ADR-0041), como 7f8322a. Toca exactamente estos ficheros:
>       - contrato.yaml: ampliado a knowledge/cases/retirados.yaml y tests/unit/test_retirados.py; si hace falta partir la protección de knowledge/ carpeta a carpeta, como en 7f8322a, se parte.
>       - knowledge/cases/retirados.yaml: una entrada nueva por día, solo añadida, por la HUELLA, con motivo («identidad deducible de textos commiteados en trabajo/sesgo-h4-color, fases 0 a 4: el rango de días del gráfico en directo de v6 junto al recuento de sus días reservados; el trader da su sesgo sobre ese gráfico en v6 1:03:48-1:05:35, sin vela identificada»), exposicion (las filas del 2026-10-17 de HOLDOUT-EXPOSICIONES), adr: ADR-0041 y retirado_el: 2026-10-17. Y la cabecera de comentario, que dice que fidelidad-1 se mide sobre 9, pasa al recuento nuevo (ADR-0041 §5: la diferencia se documenta en el propio fichero); las entradas anteriores no se tocan.
>       - tests/unit/test_retirados.py: test_el_repo_real_retira_uno_y_ninguna_salida_lo_nombra pasa a los totales nuevos (recuento esperado; puedes corregir su nombre y su docstring, desfasados desde el segundo retirado) y sigue comprobando que todos los retirados están en casos_ocultos y que ninguna salida los nombra.
>       - docs/validation/HOLDOUT-EXPOSICIONES.md: la primera fila del 2026-10-17 gana al final, sin fechas: «Consecuencia: los días reservados del gráfico salen del holdout por ADR-0041 (retirados.yaml, este commit); fidelidad-1 pasa de <n> a <m> días medidos.» Y en las filas del 2026-10-17, «cuatro días de fidelidad-1» pasa a «días de fidelidad-1».
>       - SESGO-H4-COLOR.md: «cuatro días de fidelidad-1» pasa a «días de fidelidad-1» en «Para F26» y en §5.3, y un §10.1 nuevo con la tabla de recuentos antes y después por partición (reservados, medidos, retirados, ocultos), sin ids ni fechas, y una línea: retirar todos los reservados del rango deja saber qué días del rango no lo son; ADR-0041 ya acepta que la huella no es secreta, y F26 lo tiene en cuenta.
>       - docs/encargos/trabajo-sesgo-h4-color.md: esta orden copiada.
>       Trailer Fuente: ADR-0041. knowledge validate y make check en verde. Si hace falta tocar cualquier otro fichero, o los recuentos no casan con lo esperado, PARADA.
>
> 2. La pregunta 2 de la sesión 5 (§4.4) va SOLO con el esquema de dos velas, sin el literal de la sesión 1 ni ninguna referencia a ese caso. Porqué: el literal le recordaría un gráfico en directo de días que acaban de salir del holdout por estar expuestos; la pregunta del esquema basta para resolver la contradicción.
>
> 3. Commit del contrato (chore(cierre): sale el contrato y entra el registro en HISTORIA), con todo lo de RITUAL y además:
>    a) PROJECT_STATE: las líneas de §5.1 tal cual (W sale entera a HISTORIA con el título de §5.1; F y V como en §5.1). En HISTORIA, después del texto literal de W, una línea: «Corrección del consultor (2026-10-17): sesgo_h4_criterio_ruptura = mecha no era solo una re-expresión suya; el trader ya lo había dicho (fb-2026-09-09-sesion-01-41f46b21, ev-v9-001312-19e45e4a, ev-v9-000902-25db5bf5; ADR-0080).»
>    b) G gana una frase: «fidelidad-1 tiene <k> días medidos menos desde el 2026-10-17 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta.» Con <k> el recuento del paso 0.
>    c) La hoja de ruta, como §5.2, con el tag stable/F37r-sesgo-h4-color.
>    d) La fila de la rama en ERRORES-RECURRENTES, con lo del revisor y estos hallazgos del consultor:
>       - (importa, consultor) Mi respuesta a la PARADA leyó la fila de exposiciones de la fase 0, con el rango de días y el recuento de reservados, y no lo vio; lo cazó el revisor (a1). Lección para el consultor y el revisor: en todo texto que hable de días de un mes con reservados, buscar juntos un rango de fechas y un recuento de reservados: juntos identifican días aunque ninguno lo haga solo.
>       - (importa, consultor) El encargo traía cuatro errores del consultor que cazó su auditor antes de la fase 0: que «mecha» era solo re-expresión del consultor (el trader lo había dicho), que la regla solo enmendaba ADR-0060 (también ADR-0044 §2 y ADR-0075 §3), que un registro sobre RN-003 podía ser fuente del parámetro, y una línea F que rompía test_hoja_de_ruta (c). Y uno que llegó a la rama: la nota de voz situada en la captura equivocada (§1.m). Lección: el auditor del encargo funciona; lo que cita una captura se comprueba captura a captura.
>       - (menor) Antes de abrir un fotograma de un gráfico EN DIRECTO, se mira qué días enseña por la fecha de grabación del vídeo y se comprueba con casos_reservados si alguno es reservado (§5.3).
>       - (menor, de la orden de cierre de corrida-construccion, que no la escribió) Allí el clasificador negó gh api y la sesión consultó la CI por otra vía (curl y un guion Python): cambiar de vía tras una negativa es rodearla. Lo que niega el clasificador lo lanza Aleks con «!».
> 4. Después, el ritual tal cual lo mandan RITUAL.md y la skill cerrar-rama, en su orden (merge --no-ff, tag stable/F37r-sesgo-h4-color, las cuatro líneas de cabecera, state check, make check sellado, commit de estado, push atómico de main y el tag con mi «1. Yes», ls-remote, CI de main en verde y borrar la rama local). En main..trabajo/sesgo-h4-color tienen que quedar nueve commits: los siete de la rama, el de la retirada y el del contrato. La CI se consulta por la vía que escribe RITUAL; si el clasificador la niega, PARADA y la consulto yo con «!»: no se cambia de vía. Esta rama no se empujó como fix/, así que no hay rama remota que borrar.
> 5. Informe final: sha de main, tag, run y estado de la CI de main, sha del commit de la retirada, recuentos por partición antes y después, ramas que quedan y tamaño de PROJECT_STATE.
>
> Si un paso del ritual falla o el clasificador niega algo, PARADA; nada de --no-verify, force, rebase ni rodeos.
