# Encargo · trabajo/barrido-sesion-5

Dado por Aleks (consultor) el 2026-10-19. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/barrido-sesion-5 (NA:V, hoja de ruta R4.1, tramo R4). Encargo del consultor, 2026-10-19.
>
> 0. Apertura
> - Base: main e518707, el commit de estado sobre el merge a1bb8a5 (stable/F37v-punto-usado). Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de e518707 la dio verde el cierre (run 39275923817, que no está escrito en el repo): compruébala con gh; si el clasificador niega gh, PARADA y la consulto yo con «!». Por orden del consultor, nunca con curl ni con un guion, aunque RITUAL.md lo traiga.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R4.
> - Informe (el artefacto del contrato): docs/validation/BARRIDO-SESION-5.md. En rutas_permitidas, además: docs/sesion-5/PREGUNTAS.md y docs/validation/HOLDOUT-EXPOSICIONES.md.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0; entregar-rama al final.
> - Revisa /model antes de empezar: Opus en esfuerzo alto.
>
> 1. Objetivo
> El barrido de preguntas de la sesión 5 con el trader (primera semana de noviembre), como hizo feature/barrido-sesion-4 con docs/sesion-4/PREGUNTAS.md: reunir todo lo que V y R4.1 mandan preguntar, buscar cada cosa en lo ya registrado, juntar las repetidas, ordenarlas y escribir cada pregunta lista para la hoja. La sesión 5 es SOLO de preguntas: va por docs/runbooks/SESION-DE-PREGUNTAS.md, scripts/hoja_preguntas.py y el PDF que hace el consultor con este documento; no usa kit hoja, y por eso J no la bloquea (punto 6). Recuerda que ADR-0083 es PROVISIONAL hasta la pregunta 3, y ADR-0081 hasta A-57.
>
> 2. Decisiones del consultor (2026-10-19; las tomo antes del barrido, y el barrido no las cambia. Si la fase 0 encuentra un hecho que las contradiga, PARADA)
> D1. Las fuentes, todas, cada una con su fichero y su sección leídos ahora:
>  - las que lista V en PROJECT_STATE: ACTIVAR-SESION-04.md §0.e y §5; ACTIVAR-SESION-04-MOTOR.md §5 y §6; ENTRADA-JULIO.md §8 (si el xlsx de julio es la exportación de v11 a v13); CORRIDA-CONSTRUCCION.md §4.5, con su pregunta 1 sustituida por las dos de SESGO-H4-COLOR.md §4.4; MARGEN-LOTE.md §5 (A-57); VISOR-CONSTRUCCION.md §3.2; y PUNTO-USADO.md §5 (la pregunta 3);
>  - las que R4.1 nombra y V no: ADR-0076 §4, ADR-0077 §5 y la confirmación del caso bajista de S-13. RN-004 tras A-35 y RN-020 tras A-44 (ACTIVAR-A35-A44.md §5.1) son la medida de después de activar, no preguntas: van a «fuera de la hoja», con esa razón;
>  - como en la sesión 4, las ambigüedades ABIERTAS que no estén ya (al menos A-48, que CORRIDA pone con la pregunta 4; las de clase medicion, A-16, A-28, A-54, A-55 y A-56, van fuera de la hoja), las candidatas de Known Ambiguities de PROJECT_STATE y el feedback pending (uv run botsito feedback pending; ojo: el CORRECT de RN-003 de la sesión 3 sale pendiente por un falso positivo conocido, HOJA-DE-RUTA G.2). Cada una, o entra, o va a «fuera de la hoja» con su porqué.
>  Donde V y R4.1 no dicen lo mismo, gana PROJECT_STATE, y la línea que lleva a R4.1 lo que le falta va al punto 6.
> D2. El formato, como la sesión 4: preguntas cerradas, con opciones y «otra, ¿cuál?» donde las opciones puedan sugerir. Es una desviación de SESION-DE-PREGUNTAS.md («Durante», que pide abiertas) y el documento la declara, como hizo el de la sesión 4. Esquemas inventados, rotulados «Esquema inventado, no es un día real», donde la pregunta lo pida, y SIEMPRE en las dos del sesgo (SESGO-H4-COLOR.md §4.4: con un esquema dibujado, nunca con fotogramas de v6). La de la contradicción con la sesión 1 va sin el literal de la sesión 1 y sin ninguna referencia a ese caso: no lleva «Lo que nos has dicho» de v6. Ningún gráfico de un día real por defecto: lo que lo pida se marca en 4.e y lo decido en la PARADA. La pregunta 3 va con el texto de PUNTO-USADO.md §5, ejemplo del 29 de abril incluido.
> D3. Cada pregunta, con estas partes: título; «Lo que nos has dicho», con citas literales, su fuente y su minuto; «Lo que todavía no sabemos», en el lenguaje del trader; la pregunta, una sola y sin jerga del repo; «Para precisar», de dos a cuatro subpreguntas; y «Para confirmar al final», una frase con huecos. Una «en parte» lleva lo que el trader ya dijo y pregunta solo lo que falta: nunca se repite lo respondido.
>  Las citas: la CLI filtrada (uv run botsito kb find / kb at) oculta entero el texto de las sesiones en cuarentena (v7 a v10, src/botsito/corpus/cuarentena.py; verifícalo). De las sesiones 2 a 4 se cita lo que ya está registrado: los ítems de evidencia que da kb y los registros fb-* de knowledge/feedback/ (los usó el barrido de la sesión 4), por la vía que la guardia permita; si la guardia niega una, no la rodees: PARADA. Nunca la transcripción cruda, ni las filtradas a mano, ni los tramos no citables.
> D4. El orden, por impacto, en bloques:
>  1. lo que más separa al bot del trader y lo que bloquea: las dos del sesgo (SESGO-H4-COLOR.md §4.4), A-35 y A-44 (BLOQUEANTES);
>  2. el resto de la lista de CORRIDA-CONSTRUCCION.md §4.5 en su orden, del 2 al 9 (el lote que no cabe, A-57; las reentradas, la pregunta 3; las velas de la caja, con la A de VISOR §3.2 junto a ella; la zona; hasta cuándo mueve la orden; qué le hace no operar; el lado del ruido o las zonas de control; el precio pasado el 0), con las ampliaciones de VISOR §3.2, y la B de VISOR §3.2 donde encaje (si puede reabrir A-46, que está RESUELTA, dilo: se pregunta igual, y la respuesta entraría por REOPEN, docs/runbooks/AMBIGUEDADES.md);
>  3. las demás «en parte» y las preguntas de ACTIVAR-SESION-04-MOTOR.md §5;
>  4. al final, las confirmaciones cortas (el caso bajista de S-13, la casi plana de S-14, el xlsx de julio).
>  Mide cuánto duró la sesión 4 (fuentes.yaml, la duración de v10, sin abrir el vídeo) y estima la 5 con el mismo ritmo; si pasa de lo que duró la 4, el documento dice qué se puede dejar para un WhatsApp o para la sesión 6.
> D5. Códigos: S-1 a S-n en el orden final. Son de la sesión 5: el documento lo dice, como docs/sesion-4/HOJA-USADA.md §1, y repite cómo se dicen en voz (SESION-DE-PREGUNTAS.md, «pregunta …» y «fin de pregunta»). CODIGOS_DE_SESION_TEXTO["05"] (scripts/transcribir_sesion.py) entra en la ingesta, no aquí.
> D6. Al final del documento, un bloque «Para cerrar», sin código de voz, con lo que no es de la operativa y hay que pedirle al trader: si grabó diciembre con su voz (NA:I), la exportación del backtest de agosto (NA:Q) y la confirmación escrita sobre marzo que pide REGISTRO-MARZO.md §2 (verifica qué pide). Sin fechas de días.
> D7. S-14 (la casi plana, NA:H): el literal de v10 a 1:44:49 lo leo yo en mi terminal. Hasta que te diga qué dice, la pregunta se escribe con las dos lecturas («1 o 2» y «12»), sin elegir.
>
> 3. Lo que NO cambia
> - Es una rama de solo lectura más dos documentos: no cambia el motor, la spec, ambiguedades.yaml, el feedback, knowledge/cases ni el holdout. scripts/hoja_preguntas.py tampoco, hasta la PARADA (4.d).
> - Holdout: solo material de construcción (abril, julio del 1 al 17, agosto y enero del 2 al 30: SESION-DE-PREGUNTAS.md, regla 2; su paso 6 de «Antes» dice todavía «abril o agosto», y eso va como línea en el punto 6), cada día comprobado con casos_reservados. Ninguna fecha de un día reservado ni ningún resultado de holdout en nada de lo que escribas. Lo que se abra se declara el mismo día en HOLDOUT-EXPOSICIONES.md, y el documento lleva su «## 0. Qué se abrió», como el de la sesión 4.
> - Las guardias, .claude/ y el Makefile. PROJECT_STATE, salvo lo que haga el ritual (22.580 bytes; verifícalo).
> - Si el clasificador niega un comando, no cambies de vía ni lo reescribas: PARADA, y lo lanzo yo con «!».
>
> 4. Fase 0 (inventario sin tocar nada) y PARADA
> a. La lista completa de D1, una fila por cosa: de dónde sale (fichero:línea), qué ambigüedad, regla o patrón nombra, su estado, y si ya tiene respuesta registrada (con su id).
> b. Las repetidas que juntas, y las que van a «fuera de la hoja», con su porqué.
> c. El orden propuesto con D4, la duración de la sesión 4, la estimación de la 5 y lo que se puede dejar.
> d. scripts/hoja_preguntas.py: si corre hoy en main (con --salida fuera del repo) o falla, y por qué; qué le haría falta para la sesión 5 (el orden, que hoy es ORDEN_SESION_02; el encabezado; las preguntas que no son ambigüedades; la B si toca A-46) y qué tests lo fijan (tests/unit/test_hoja_preguntas.py; el de tests/unit/test_transcribir_sesion.py hacia :306 fija la copia de transcribir_sesion.py, no la del script: dilo). Propón; no lo toques.
> e. Las preguntas que pedirían un gráfico o un fotograma de un día real, con el día y por qué. Al menos: el fotograma de v4 a 0:53:10 para A-32, que «no se abre sin decisión del consultor en R4.1» (ACTIVAR-SESION-04.md, hacia :837; la sesión 4 dejó A-32 fuera porque solo se entiende con el gráfico); y los días de VISOR-CONSTRUCCION.md §3.2, que R3.2 manda volver a comprobar con contexto_h4.py si el visor o la spec cambian (ADR-0083 cambió el motor después), incluido el día de julio que se quedó sin página. Para lo que se vaya a enseñar de un gráfico en directo, mira antes, por la fecha de grabación, qué días enseña (SESGO-H4-COLOR.md §5.3). No abras nada: lista y propón.
> PARADA siempre al final de la fase 0: entrega a-e en el informe y espera mi respuesta.
>
> 5. Fase 1 (tras mi respuesta)
> docs/sesion-5/PREGUNTAS.md con D2-D7, y el informe. Si en la respuesta a la PARADA decido cambiar hoja_preguntas.py, va en su commit, con sus tests y make check sellado; si no, make check sellado sobre los documentos. En cada make check, copia al informe la línea PICO DE MEMORIA de make-check.log. Si test_nunca_bloquea_y_es_rapido falla por tiempo, no lo arregles ni lo repitas en bucle: córrelo suelto una vez, apunta los dos tiempos en el informe y prepara una línea para G (hoy no tiene entrada).
>
> 6. El informe
> Lleva el encargo frente a lo hecho, punto por punto, las desviaciones, la fase 0 y «Líneas preparadas para el commit del contrato de la orden de cierre». Entre ellas, la decisión del consultor del 2026-10-19 sobre J, copiada tal cual: «J (kit hoja) NO bloquea V. kit hoja es la hoja Word para sesiones que etiquetan días; la sesión 5 es solo de preguntas (SESION-DE-PREGUNTAS.md, scripts/hoja_preguntas.py y el PDF del consultor), como la 2, la 3 y la 4.» Y lo que cambia por ella y por esta rama:
> · en V, «de J (kit hoja)» sale de su «Depende de», y V gana «Hoja de preguntas: docs/sesion-5/PREGUNTAS.md (trabajo/barrido-sesion-5)»;
> · F pasa a «V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno a V.»;
> · en la hoja de ruta, R4.1 pierde la frase de :212-213 que empieza «La hoja Word necesita antes que `kit hoja` funcione…» y acaba en «(NA:J).» (está partida en dos líneas: el Edit tiene que cogerla entera) y NA:J sale de sus Refs; R4.1 gana lo que V tiene y ella no (§0.e, MOTOR §6, ENTRADA-JULIO §8, la pregunta 3); y en G.2, «(J, antes de R4)» y «(J, antes de R4.1)» pasan a «(J, antes de la próxima sesión que etiquete días)». J sigue viva en G.2, con NA:J en sus Refs;
> · el paso 6 de «Antes» de SESION-DE-PREGUNTAS.md («abril o agosto»), como línea para la rama que lo corrija.
> Comprueba en memoria que test_hoja_de_ruta.py y test_project_state.py pasan con esas líneas, como simular_cierre.py de VISOR-CONSTRUCCION, y da el tamaño que quedaría de PROJECT_STATE.
>
> 7. Revisor
> El agente revisor (opus) sobre la rama, con los dos ejes de siempre: reglas y encargo. Que compruebe además que cada cita sale de lo registrado y de material citable, que ninguna fecha reservada ni ningún resultado aparece en PREGUNTAS.md ni en el informe, que ninguna «en parte» repite lo ya respondido, que las dos del sesgo van solo con esquema y que ninguna consulta de CI se hizo con curl ni con un guion. Su informe va pegado al final del informe, con lo arreglado y lo declarado.
>
> 8. CI
> Si la rama no toca hooks, rutas ni el sistema de archivos, dilo con la lista de ficheros cambiados. Si toca hoja_preguntas.py, push como fix/barrido-sesion-5 y CI de Linux, con su run en el informe.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA (2026-10-19)

Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/barrido-sesion-5 (2026-10-19). Cópiala tal cual en el informe y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Las 25, en el orden de 1.c. S-25 y S-23 llevan la marca «si falta tiempo, por WhatsApp» y S-18 la de «si falta tiempo, a la sesión 6». Por qué: la estimación supera en unos 5 minutos a la sesión 4, y eso no basta para quitar nada de antemano.
> 1. (a). Las dos subpreguntas salen, y lo que ya está registrado pasa a «Lo que nos has dicho» con su id (fb-2026-09-09-sesion-01-bff260ea para el saldo inicial del día; lo FIRME de A-13, ambiguedades.yaml). Por qué: D3 prohíbe repetir lo respondido.
> 2. (a). S-1 es la contradicción: va sobre el esquema de dos velas y con «Lo que nos has dicho» vacío, con la frase «se pregunta sobre el esquema». S-2 es la ruptura simple sin cuerpo, y lleva el WhatsApp del 2026-10-14 como «Lo que nos has dicho». Las dos van con esquema inventado, como manda D2. Por qué: la contradicción solo se resuelve si el trader contesta sin tener delante la regla que la decide. Es una desviación del orden de SESGO-H4-COLOR.md §4.4, y el documento la declara.
> 3. (a). hoja_preguntas.py no se toca en esta rama. La hoja de la sesión 5 es el PDF del consultor hecho con docs/sesion-5/PREGUNTAS.md, como en la sesión 4. Una línea para G recoge lo que tiene desfasado: el encabezado y la regla 2 de la sesión 2, A-24 DECIDIDA dentro del orden, A-50, A-53 y A-57 fuera, y la B, que toca A-46 (RESUELTA). Por qué: la hoja de la 5 no sale del script, y esta rama es de documentos.
> 4. (a). Ningún gráfico de un día real: todo con esquemas inventados, y los días se quedan en el informe como clave de Aleks. Por qué: es lo que D2 pone por defecto, y así no hay que volver a pasar contexto_h4.py ni declarar exposiciones.
> 5. (a). A-32 en abstracto, con un esquema: «¿hay alguna línea en M1 que, si el precio la rompe solo con la mecha, te quite la entrada? ¿Cuál?». Por qué: S-23 de la sesión 4 ya dio la regla general, y lo que falta saber es si existe esa clase de línea.
> 6. (a). S-25 se pregunta. Su «Lo que nos has dicho» no es una cita: dice «nos lo comentaste de palabra el 13 de octubre, sin grabar», para que quede en la voz. Por qué: cuesta medio minuto y da la cita grabada que ENTRADA-JULIO.md no tiene.
> 7. (a). Van a «Líneas preparadas para el commit del contrato»: G.2 nombra los dos pendientes de RN-003 (31fb311f y ca0afae6), y entra la línea para G del punto 3. Por qué: hoy G.2 dice uno y son dos.
> 8. (b). Aviso en el encabezado de PREGUNTAS.md («antes de grabar, la copia de seguridad A.4»), y V conserva A.4 en su frase de dependencias. La línea del cierre sustituye «, de J (kit hoja) y» por « y», como propones en el matiz 57. Por qué: A.4 sigue siendo verdad, y solo sale J.
>
> Además:
> - Herencia 3: las opciones de S-3 (A-35) y S-4 (A-44) se escriben de modo que cada una caiga en una lectura documentada de ACTIVAR-A35-A44.md §1. Debajo de cada opción, en el documento y no en la hoja del trader, pon la lectura en la que cae.
> - Herencias 2, 4 y 6: se aplican como dices. Sin dinero, con las horas en Europe/Madrid, con cada premisa contrastada con la spec de hoy y sin juntar nunca un rango de fechas con un recuento de reservados.
> - Matiz 43: es correcto. El literal de 1:44:49 lo lee Aleks en su terminal; hasta que lo diga, S-24 va con las dos lecturas.
> - La corrección del punto 25 (dos falsos positivos, no uno) y la del matiz 31 (la guardia niega kb sobre v7-v10) van al informe como hallazgos del auditor sobre el encargo.
>
> Sigue con la fase 1 sin parar: PREGUNTAS.md, make check sellado (con la línea PICO DE MEMORIA), revisor, entregar-rama y «Rama lista para revisión, NO cerrada».
