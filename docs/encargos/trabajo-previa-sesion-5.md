# Encargo · trabajo/previa-sesion-5

Dado por Aleks (consultor) el 2026-10-21. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/previa-sesion-5 (NA:V, hoja de ruta R4.1 y A.3, tramo R4). Encargo del consultor, 2026-10-21.
>
> 0. Apertura
> - Base: main 24b7cba, el commit de estado sobre el merge e76f829 (stable/F37x-ea-conexion). Verifica con git main, origin/main y el tag, y que no hay otra rama abierta. La CI de main de 24b7cba la dio verde el cierre (run 39705799089): compruébala con gh, a mano y una vez, nunca con un guion ni con un bucle que espere.
> - Ábrela con la skill abrir-rama. Tramo R4. Informe: docs/validation/PREVIA-SESION-5.md. En rutas_permitidas, además: docs/sesion-5/PREGUNTAS.md, docs/runbooks/SESION-DE-PREGUNTAS.md, docs/plan/HOJA-DE-RUTA.md y los runbooks o documentos que reciban texto movido de PROJECT_STATE (punto 4).
> - Skills: fase-cero (con auditor-encargo) y entregar-rama. Revisa /model: Opus, esfuerzo medio.
> - Regla del consultor desde el 2026-10-21: si la guardia o el clasificador niegan un comando, PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.
>
> 1. Objetivo
> Dejar el repo listo para la sesión 5 con el trader, que es el viernes 23 de octubre: corregir dos preguntas de PREGUNTAS.md, un paso del runbook de la sesión, apuntar la fecha y adelgazar PROJECT_STATE, que está en 24.135 bytes (tope 25.000) y no deja sitio para la ingesta. Es una rama solo de documentos: no cambia el motor, la spec, las ambigüedades, el feedback, knowledge/cases ni el holdout. Tiene que cerrar el jueves 22, para que la ingesta pueda abrir su rama después de la sesión.
>
> 2. Las dos preguntas con los extremos de la caja cambiados (error del barrido, encontrado por el consultor el 2026-10-20)
> En una compra, el 0 de la caja es el punto (donde va la orden, arriba) y el 1 es el otro extremo, del lado del stop (abajo); en una venta, al revés. Lo dicen orden_stop_punto («un BAJO en una venta») y caja_bloque («el extremo opuesto, la máxima en una venta») en knowledge/spec/parametros.yaml: verifícalo.
> - S-7 preguntaba «desde dónde trazas el 0», con opciones que son las del 1 (A-48: r1, r4 y r6 de caja_bloque).
> - S-12 decía, de una compra, «el 1 queda por encima y el 0 por debajo», que es imposible. Su fuente (ACTIVAR-SESION-04.md §0.e.6) decía «el 0 de este lado y el 1 del otro», y su propia línea «Para Aleks» habla del 0 por encima.
> PREGUNTAS.md está cerrado en main: lleva un recuadro de corrección junto a cada una (fecha, rama y motivo) y su cuerpo queda intacto. El recuadro trae el texto corregido que va en la hoja del trader, tal cual:
> S-7. Título: «Los dos extremos de la caja: dónde pones el 0 y hasta dónde llevas el 1». Lo que todavía no sabemos: «Hasta qué vela llevas el 1 de la caja, el extremo del lado del stop, y si actualizar la caja con la vela abierta es lo que haces siempre o solo a veces.» Pregunta: «Para esta compra, el 0 va en el punto de breaker, arriba, y el 1 en el otro extremo, abajo, del lado del stop. ¿Hasta dónde llevas el 1? (a) hasta el mínimo de la última vela roja; (b) hasta el mínimo de todo el tramo de velas rojas seguidas; (c) hasta el mínimo de todas las velas desde la que marca el punto hasta que pones la orden; (d) otra, ¿cuál?» Para precisar: «¿Y el 0: lo pones siempre en el último alto de M1 que se formó, o en el punto que marcaste en la vela que tomó la liquidez?»; «Dijiste que la caja "la puedes actualizar" mientras el precio avanza: ¿lo haces siempre, o solo a veces? ¿Cuándo?»; «En una venta, ¿es lo mismo al revés, con el 0 abajo y el 1 arriba?». Para confirmar al final: «El 0 de mi caja va en ______, el 1 llega hasta ______, y la trazo cuando la vela ______.» Para Aleks: (a) = r1, (b) = r4, (c) = r6 (el valor de hoy de caja_bloque); la primera de «Para precisar» es orden_stop_punto (último alto de M1 = ultimo_pivote_m1, el valor de hoy; el punto de la vela de la toma = referencia_de_la_toma); la de la vela abierta es A-49.
> S-12. Pregunta: «Son dos compras, con la línea del bajo de M15 que se tomó. En la primera, la caja entera queda por encima de la línea; en la segunda, el 0 queda por encima y el 1 por debajo. ¿Operas las dos? (a) las dos; (b) solo la primera: la caja entera tiene que quedar por encima; (c) otra, ¿cuál?» Para Aleks: hoy el bot mira solo el 0 (RN-005) y opera las dos: eso es (a).
> Comprueba en el informe que ninguna otra pregunta de PREGUNTAS.md tiene la orientación de la caja al revés (S-13, S-16 y S-17 la nombran) y di qué encontraste en cada una.
>
> 3. El runbook y la fecha
> - docs/runbooks/SESION-DE-PREGUNTAS.md, paso 6 de «Antes» (hacia :76): «el día tiene que ser de abril o de agosto» pasa a remitir a la regla 2 del mismo runbook (abril, julio del 1 al 17, agosto y enero del 2 al 30). Es un runbook: se edita directamente.
> - La sesión 5 es el viernes 2026-10-23 (Aleks, 2026-10-21). Compruébalo antes con la línea del paso 1 de «Antes» del runbook (imprime solo True o False) y pon el resultado en el informe; si sale True, PARADA. Con False, en la hoja de ruta, A.3 lleva una línea de Estado con la fecha (la confirmación de marzo sigue pendiente, así que A.3 no pasa a HECHA). La fecha no va a PROJECT_STATE.
>
> 4. Adelgazar PROJECT_STATE (objetivo: 22.000 bytes o menos)
> Con el criterio de docs/state/README.md y como lo hicieron trabajo/dieta-y-skills y trabajo/plataforma-adelantada: solo se mueven entradas enteras, nunca se resumen ni se pierde texto. Cada entrada que sale va entera a su sitio (un runbook, ERRORES-RECURRENTES o el informe que la originó, si su texto ya está allí entero) y deja una línea con el puntero, o sale a HISTORIA bajo «# Next Action HECHA», si de verdad está hecha. Candidatas para mirar primero: las deudas de Technical Debt escritas en mayúsculas de septiembre, que son reglas o lecciones y no deudas abiertas (por ejemplo «BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD»), y los pendientes heredados. Las deudas abiertas de verdad se quedan.
> Fase 0: la lista de lo que propones mover, con su destino y el tamaño que quedaría. Si llegas a 22.000 bytes sin tocar nada que siga vivo, sigue sin parar. Si no se puede sin quitar algo vivo, PARADA con la lista.
> Los tests que vigilan PROJECT_STATE (test_project_state.py, test_kit.py con la tabla de las abiertas, test_hoja_de_ruta.py y state check) tienen que seguir pasando.
>
> 5. Lo que NO cambia
> El motor, la spec, parametros.yaml, ambiguedades.yaml, el feedback, knowledge/cases, el holdout, scripts/hoja_preguntas.py, las guardias, .claude/ y el Makefile. Los informes cerrados de docs/validation/ solo reciben recuadros, si alguno hace falta.
>
> 6. Informe, revisor y CI
> - El informe lleva el encargo frente a lo hecho, las desviaciones, lo que se movió y adónde, el tamaño final de PROJECT_STATE y las «Líneas preparadas para el commit del contrato de la orden de cierre». Simúlalas en memoria con test_hoja_de_ruta.py y test_project_state.py, como simular_cierre.py de VISOR-CONSTRUCCION.
> - En cada make check, copia al informe la línea PICO DE MEMORIA.
> - Revisor (opus), con los dos ejes. Que compruebe además que ningún texto movido se perdió ni se resumió, que cada puntero lleva al sitio donde está el texto entero, y que los recuadros de S-7 y S-12 tienen la caja bien orientada contra parametros.yaml.
> - CI: si la rama no toca hooks, rutas ni código, dilo con la lista de ficheros cambiados.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-10-21)

Dada por Aleks (consultor) el 2026-10-21. Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/previa-sesion-5 (2026-10-21). Cópiala tal cual en el informe y aplícala punto por punto (skill fase-cero).
>
> 0. (c), dentro de S-12 y sin cambiar la numeración. S-12 pasa a tener dos partes, en este orden: primero el lado («En una compra, después de que el precio toma la liquidez de M15, ¿tu caja tiene que quedar por encima o por debajo del nivel tomado? (a) por encima; (b) por debajo; (c) depende, ¿de qué?»), con un esquema neutro (el nivel tomado y una caja a cada lado, sin decir cuál vale); y después la de A-50, dicha sobre el lado que haya contestado («Y si la caja queda a caballo del nivel, con el 0 de tu lado y el 1 del otro, ¿la operas?»). En «Lo que nos has dicho» van las dos citas que se contradicen (la de RN-005, ev-v1-001306-f98e12e9, y ev-v9-004919-c6bfb3ee), sin decirle cuál sigue el bot. El «Para Aleks» corregido dice: hoy el bot sigue RN-005 (en una compra, la zona por encima del bajo tomado es ruido) y no opera ninguno de los dos dibujos del texto anterior; la respuesta a la primera parte decide si RN-005 sigue o se reabre. Por qué: el repo se contradice y solo el trader puede decidirlo; preguntar A-50 sobre un lado equivocado no cierra nada. El error del «Para Aleks» anterior («opera las dos: eso es (a)») es del consultor y va al informe y a la orden de cierre.
>    Lo mismo afecta a S-15: su «Para Aleks» dice que el lado del ruido ya está respondido con ev-v9-004919, y no lo está. Corrígelo en su recuadro: el lado se pregunta en S-12.
> 1. (a). El recuadro de S-7 sustituye también el esquema: el 0 arriba, en el último alto de M1 (el punto, donde va la orden de compra), y el 1 abajo, con los tres mínimos rotulados (la última roja, el tramo de rojas y todas las velas desde la que marca el punto).
> 2. (a). Recuadro en S-13: «sube mucho» pasa a «baja mucho (la caja se hace muy grande)».
> 3. (c). El conjunto A y las Reglas vivas, estas a un runbook nuevo, docs/runbooks/DECISIONES-DE-PROCESO.md, con el texto entero y en el mismo orden. En PROJECT_STATE se quedan los encabezados que exigen los tests, cada uno con una sola línea que apunta a su sección del runbook: un puntero, no un resumen. Cada entrada del conjunto A va entera a un destino que el informe nombra; ninguna se borra sin destino. «BUSCAR EN EL CORPUS» se queda en Technical Debt, como dice el auditor. Si al hacerlo algún test exige que un texto viva en PROJECT_STATE, PARADA. Por qué: la ingesta y las dos activaciones que vienen necesitan más de 2 KB libres.
> 4. Además: S-9 y S-10 nombran bajos de M15 para comprar, que es lo que dice RN-005. Comprueba en el informe que sus esquemas y su texto no dan por bueno ningún lado de la caja, y di lo que encuentres. No hace falta cambiarlas si no lo dan.
>
> Sigue sin parar hasta la entrega, con el revisor y su comprobación añadida: que en S-7, S-12, S-13 y S-15 la caja y el lado estén bien orientados contra RN-005, orden_stop_punto y caja_bloque.
