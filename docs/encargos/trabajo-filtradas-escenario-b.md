# Encargo · trabajo/filtradas-escenario-b

Dado por Aleks (consultor) el 2026-10-04. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/filtradas-escenario-b, desde main. Comprueba antes que main está en f712650 y que el tag stable/F36w-cuarentena-por-condicion apunta a 44f461d; si no, para y dímelo. Ábrela con la skill abrir-rama (encargo en docs/encargos/, contrato.yaml, archivo de PROJECT_STATE en HISTORIA). Copia este prompt tal cual al encargo.
>
> OBJETIVO
> Es el punto P de la Next Action: rehacer con el guion de main (scripts/transcribir_sesion.py, que desde el merge pasa meses_libres_del_repo()) las filtradas de sesión de v7–v10 en el escenario B. Hoy están en el escenario A (CUARENTENA-POR-CONDICION.md §2.1, §4.2, §4.6 y §5).
>
> QUÉ NO CAMBIA
> Ni el motor, ni la spec, ni la regla de cuarentena (botsito.corpus.cuarentena, cases.holdout), ni meses_reservados.yaml, ni el guion. Lo único de knowledge/ que puede cambiar es knowledge/corpus/tramos_no_citables.yaml, por su régimen (solo añadir), y únicamente si la fase 1 lo pide. Si la guardia bloquea algún paso, para y dímelo. No se rodea: ni con funciones internas ni con el guion reescrito.
>
> REGLA DE LECTURA DE TODA LA RAMA
> No se lee ni se imprime texto de ningún segmento, de ninguna cruda ni de ninguna filtrada. Solo valen recuentos, marcas de tiempo, límites en milisegundos, ids ev-* y sha256.
>
> FASE 0. Inventario y medida, sin escribir nada. Entrégamela antes de seguir.
> 1. Rutas fuera del repo de la cruda de cada vídeo y de sus filtradas actuales (A), y de las *.filtrada-ANTES-condicion.md de v9 y v10. Hoja de cada vídeo: verifica que es --sesion 02 para v7 y v8, 03 para v9 y 04 para v10. Recuerda que v7 y v8 no tienen filtrada ANTES: su «antes» son sus tramos no citables.
> 2. Para cada vídeo, con el Filtro real y meses_libres del repo (B), sin escribir la filtrada, tabla con:
>    - segmentos y bloques ocultos en ANTES (o en sus tramos), en A y en B;
>    - NUEVOS: ocultos en B que en ANTES (o en sus tramos) estaban visibles, con su marca de tiempo y los ev-* que caen en ellos;
>    - DESTAPADOS: visibles en B que estaban ocultos en ANTES o que caen dentro de un tramo no citable, con su marca de tiempo.
> 3. Antes de dar cifras, compara la medida con un caso negativo conocido (lección de la rama anterior). Vale v8, que en A daba 0 bloques.
>
> PARADAS de la fase 0 (si salta alguna, no sigas y avísame):
> - algún ev-* cae en un segmento NUEVO;
> - algún segmento DESTAPADO está dentro de un tramo no citable. Un tramo se queda tapado siempre;
> - algún DESTAPADO está fuera de un tramo pero oculto en ANTES. Dime cuántos son y de qué vídeo. No se escribe esa filtrada hasta que yo decida.
>
> FASE 1. Con mi visto bueno a la fase 0.
> 1. Las filtradas A actuales se apartan como *.filtrada-A-condicion.md, fuera del repo y sin borrar nada. Las ANTES se quedan donde están.
> 2. --solo-filtrar con la hoja de cada vídeo, usando el guion de main tal cual y escrito exactamente como se ejecuta (uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion NN, con el --audio que corresponda).
> 3. Las marcas [CUARENTENA …] de cada filtrada nueva tienen que coincidir con la tabla de B de la fase 0. Si no coinciden, para.
> 4. Apunta el sha256 de cada filtrada nueva. En v9, compáralo con f7529459…a027b (SESION-04-EXTRACCION.md §1.2). Si cambia, explica con recuentos qué cambió.
> 5. Tramos: cada bloque NUEVO de B se registra como tramo no citable, con sus límites en milisegundos sacados del Filtro y con el motivo «precaución: mes con días ocultos que la cuarentena mecánica no cubría», el mismo criterio que los tramos de v6 y de v10 1:55:29. Si no hay ninguno, el informe lo dice por vídeo. Después corre scripts/ficheros_con_ocultos.py, uv run botsito knowledge validate y test_guardia_claude.py::test_los_tramos_del_repo_real.
>
> TESTS
> Si hay tramos nuevos, el test de la lista de tramos del repo real los incluye. Prueba que lo vigila de verdad: quita a propósito un tramo nuevo de la lista y comprueba que el test cae. Luego devuélvelo.
>
> DOCUMENTOS
> - Informe nuevo en docs/validation/FILTRADAS-ESCENARIO-B.md: fase 0, las tablas por vídeo, los sha, los tramos, las desviaciones y el tamaño de PROJECT_STATE. Las cifras salen de un anexo reproducible y commiteado (guion y su salida, sin texto), no de registros fuera del repo.
> - Recuadro de corrección en CUARENTENA-POR-CONDICION.md §5 y en SESION-04-EXTRACCION.md §1.2 que remita al informe nuevo. Son informes cerrados: no se editan.
> - Exposición: debe ser ninguna. Si algo se llega a leer, se declara hoy mismo en HOLDOUT-EXPOSICIONES.md.
>
> CI Y REVISOR
> - make check sellado.
> - Si la rama toca los tramos o la lista de la guardia, push como fix/filtradas-escenario-b y CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
> - Revisor, con su informe pegado al final del informe de la rama.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la fase 0 (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la fase 0 de trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Cómo se mide B: adelantando la fase 1, en su sitio. Nada de ASR nuevo.
>    Por qué: escribir una filtrada que nadie lee no expone nada. Un ASR completo crea otra copia de material en cuarentena fuera del repo, cuesta hora y media de GPU y no garantiza los mismos segmentos en v9.
>    Cómo:
>    a) Antes de ejecutar nada, copia cada filtrada A a *.filtrada-A-condicion.md y apunta su sha256. Las ANTES no se tocan.
>    b) Ejecuta uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion NN, con el --audio de cada vídeo, guion de main tal cual.
>    c) De las filtradas B solo se miran las marcas [CUARENTENA …], los recuentos y los ids. Nadie las abre hasta que yo dé el visto bueno.
>    d) Si salta una parada, se restaura A desde la copia, se comprueba que el sha256 coincide con el apuntado y me avisas.
>
> 2. Límites de los tramos nuevos: mm:ss del bloque, con el inicio al segundo y un segundo de margen al final.
>    Por qué: es lo único que da la filtrada sin leer la cruda, y el segundo de margen corrige el truncado que tu control positivo detectó.
>    Antes de usarlo, verifica en tramos_no_citables.yaml y en sus informes que v9 y v10 se registraron así. Si no fue así, para y dime cómo se hizo.
>    Cada tramo nuevo tiene que pasar tu control positivo: el bloque de B cabe entero dentro del tramo.
>
> 3. Las paradas quedan así, y sustituyen a las del encargo:
>    - algún ev-* cae en un segmento oculto en B que estaba visible en ANTES (o en sus tramos, para v7 y v8);
>    - algún segmento oculto en A pasa a visible en B y cae, aunque sea en parte, dentro de un tramo no citable;
>    - algún segmento oculto en ANTES pasa a visible en B. Dame cuántos y de qué vídeo, y no se usa esa filtrada hasta que yo decida.
>    Por qué: la parada de tramos que escribí presuponía que las filtradas aplicaban los tramos, y no lo hacen. Lo que mide esta rama es lo que B cambia frente a A, no un hueco que ya estaba.
>
> 4. El hueco de los tramos no se arregla aquí; se documenta.
>    Por qué: arreglarlo exige cambiar el guion, y la guardia solo deja ejecutar el de main.
>    En el informe, una sección propia con:
>    - para cada tramo de v7–v10: su clase (precaución, conversación personal u otra), el commit y la fecha en que entró, y cuántas líneas de la filtrada A y de la B caen dentro. Todo sin texto;
>    - qué lecturas de esas filtradas constan en los informes (extracción de las sesiones 3 y 4 y otras) después de la fecha de cada tramo;
>    - si hay alguna lectura posterior de un tramo de precaución, no la declares tú: me la pasas, y yo decido si va a HOLDOUT-EXPOSICIONES.md.
>
> 5. Next Action, en el commit que cierre esta rama: añadir después de P un punto nuevo:
>    «Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con test sintético que rompa la guardia a propósito; tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10. Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera.»
>    Por qué: la activación de la sesión 4 lee la filtrada de v10, y hoy esa filtrada enseña tramos de precaución.
>
> 6. Hallazgo del consultor para ERRORES-RECURRENTES, que se apunta en la fila de esta rama al cerrarla:
>    importa · El consultor escribió una parada sobre los tramos dando por hecho, sin medirlo, que las filtradas los aplicaban. Lección: antes de escribir una parada sobre un mecanismo, medir que el mecanismo existe.
>
> Lo demás del encargo sigue igual: los sha, v9 frente a f7529459…, los tramos nuevos por su régimen, ficheros_con_ocultos, knowledge validate, el test de tramos con su rotura a propósito, los recuadros en los dos informes cerrados, make check sellado, fix/ con la CI de Linux y sus números de run, y el revisor.
>
> Rama lista para revisión, NO cerrada.

## Segunda respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Segunda respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. P2: B no se instala en esta rama. A se queda donde la has restaurado, y las B siguen apartadas como *.filtrada-B-condicion.md, sin abrir.
>    Por qué: una parada no se relaja después de ver el resultado. B no empeora nada frente a ANTES (P3 = 0), pero sí frente a A en 6 segmentos de tramos de precaución, y la rama Q rehará las filtradas en todo caso, ya con los tramos aplicados. Instalar B ahora no aporta nada.
>    El alcance de esta rama queda así: medir B (hecho), arreglar los tramos y documentar el hueco. Declara este cambio de alcance como desviación aceptada por el consultor.
>
> 2. Tramos, por su régimen (solo añadir, sin editar los que ya existen):
>    a) v10, bloque de 1:55:27: tramo nuevo con inicio al segundo y un segundo de margen al final, el criterio de los 12 de v10, y con el motivo de precaución de siempre. Tiene que pasar tu control positivo: el bloque de B cabe entero dentro del tramo.
>    b) v9: un tramo nuevo por cada uno de los 8 bloques. Cubre el bloque entero con un segundo de margen al final, y el motivo dice que completa el tramo original (nombra cuál), porque ese se registró sin margen. Control positivo igual.
>    Por qué: con el final sin margen, la cola del último segundo de cada bloque queda fuera de su tramo, y los tramos son los que respeta la guardia.
>    Parada: si algún ev-* cae en los segundos que cubren los tramos nuevos, para y dime cuál, sin tocar el ítem.
>    Después: scripts/ficheros_con_ocultos.py, uv run botsito knowledge validate y el test de tramos del repo real, con la rotura a propósito (quitar un tramo nuevo y ver que cae).
>
> 3. Termina la sección del hueco (punto 4 de mi respuesta anterior) con las 10 sesiones de tramos que haya en v7–v10: clase, commit y fecha de entrada, líneas visibles dentro en A y en B, y las lecturas de cada filtrada que constan en los informes después de esa fecha. Sin texto. Lo que encuentres sobre lecturas de tramos de precaución me lo pasas, y yo decido si va a HOLDOUT-EXPOSICIONES.md.
>
> 4. Recuadros en los dos informes cerrados:
>    - CUARENTENA-POR-CONDICION.md §5 decía que en v9 «ya NO sale f7529459…». Sí sale: B es idéntica a ANTES. El recuadro lo corrige y remite al informe nuevo.
>    - SESION-04-EXTRACCION.md §1.2: la comparación pendiente queda hecha (v9 da f7529459…a027b), con remisión al informe nuevo.
>
> 5. El punto Q de la Next Action se sustituye por este texto (va en el commit de la rama, para que entre con el merge):
>    «Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con un test sintético que rompa la guardia a propósito. Tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10 en B con los tramos, y comprobar que lo tapado es B más los tramos, y nada destapado frente a A dentro de un tramo (FILTRADAS-ESCENARIO-B.md). Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera.»
>    Y P se quita: pasa a HECHO con esta rama.
>
> 6. Para la fila de ERRORES-RECURRENTES, además del hallazgo de mi respuesta anterior:
>    importa · De Claude Code: la comparación por bloques marcaba destapados falsos porque las marcas truncan al segundo, y el criterio de los tramos de v9 (sin margen) era distinto del de v10. Lección: toda comparación de marcas con segundos truncados se valida contra un caso idéntico conocido (aquí, v9 B = ANTES), y los criterios de registro de tramos se fijan por escrito en un solo sitio.
>    Dime dónde está hoy escrito el criterio de registro de tramos. Si no lo está, añádelo al runbook que corresponda en esta rama.
>
> Lo demás del encargo sigue igual: make check sellado, push como fix/filtradas-escenario-b con la CI de Linux y sus números de run (único fallo aceptado: state check por el nombre fix/), revisor con su informe pegado al final, y el tamaño de PROJECT_STATE.
>
> Rama lista para revisión, NO cerrada.

## Tercera respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Tercera respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Antes de registrar nada, comprueba solo con marcas, sin texto, en la filtrada ANTES de v9 (o en la A):
>    a) que el bloque [CUARENTENA …] que completa este tramo termina en la marca 0:34:56;
>    b) que la línea siguiente es visible y lleva la marca 0:34:56;
>    c) que el ancla de ev-v9-003456-9ef48fb5 es esa línea visible y no un segmento de dentro del bloque.
>    Si alguna de las tres falla, para y dímelo sin tocar nada.
>    Por qué: si se cumplen, el segmento oculto termina antes de que empiece el del ítem, porque la transcripción no solapa segmentos, y el choque es solo del truncado al segundo.
>
> 2. Si se cumplen las tres: el tramo nuevo que completa el de 0:34:44 va de 2.084.000 a 2.096.000 ms, es decir, termina en el inicio del ítem. Su motivo nombra el tramo original y el ítem. El ítem no se toca.
>
> 3. El criterio de docs/runbooks/SESION-DE-PREGUNTAS.md («Los límites de un tramo: el criterio único») se completa con esta condición, escrita como regla general y no como caso de v9:
>    «Si el segundo de margen pisa el ancla de un ítem ev-*, el tramo termina en el inicio de ese ítem, siempre que las marcas demuestren que el ítem viene de una línea visible que sigue al bloque. Si no se puede demostrar, se para y decide el consultor.»
>    Añade un test que lo vigile: con un tramo y un ítem sintéticos, el tramo que pisa el ancla de un ítem tiene que fallar en knowledge validate, o en el control que ya tengas. Si hoy ningún control lo detecta, dilo en el informe y queda como requisito de Q, no de esta rama.
>
> 4. El texto de Q en la Next Action (el de mi segunda respuesta) se amplía con esta frase:
>    «La aplicación de un tramo a la filtrada tapa un segmento solo si se solapa con el tramo más de 0 ms: un segmento que empieza exactamente donde termina un tramo queda visible. Test sintético con ese caso de borde (v9, 0:34:56; FILTRADAS-ESCENARIO-B.md).»
>    Por qué: si no, la regla de Q taparía el segmento del ítem y lo dejaría sin ancla.
>
> 5. Sigue con los puntos 3 a 6 de mi segunda respuesta: la sección del hueco, los recuadros, la Next Action, la fila de ERRORES-RECURRENTES, make check sellado, push como fix/filtradas-escenario-b con la CI de Linux y sus números de run, revisor con su informe pegado al final y el tamaño de PROJECT_STATE.
>    Pregunta expresa para el revisor: que compruebe que ningún tramo nuevo pisa el ancla de ningún ítem ev-* y que todos pasan el control positivo.
>
> Rama lista para revisión, NO cerrada.

## Cuarta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Cuarta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Autorizo medir el ancla de ev-v9-003456-9ef48fb5 con la misma localización de citas que usa uv run botsito knowledge validate. Debe ser la misma función, llamada como la llama validate; nada de una vía paralela.
>    Condiciones:
>    - la salida es solo: índice y milisegundos de inicio y fin de cada segmento en que caen las palabras citadas, y el índice y los milisegundos de fin del último segmento del bloque [CUARENTENA 34:44-34:56];
>    - ni texto, ni palabras, ni longitudes de cita;
>    - el guion va como anexo (ancla_v9.py) con su salida commiteada, y el informe dice qué función llama y que es la de validate.
>    Por qué: es un control ya autorizado y no expone texto. Lo que decide es si el ítem cita la línea visible o el segmento oculto.
>
> 2. Según el resultado:
>    a) Todas las palabras citadas caen en la línea visible (la de 0:34:58 o posteriores): el ítem no pisa la cuarentena, y lo que está mal es solo su ventana declarada.
>       - Tramo nuevo de 2.084.000 a 2.096.000 ms, que completa el de 0:34:44. Pasa validate porque no solapa la ventana del ítem.
>       - Declara en el informe que la cola del segmento oculto, desde 2.096.000 ms hasta su fin real, queda fuera del tramo. La tapará Q, porque ese segmento solapa el tramo más de 0 ms.
>       - El ítem no se toca en esta rama. Su ventana se corrige por su régimen (evidence new --supersede, con t0 en el inicio real del ancla) en una rama aparte. Añade a la Next Action, tras Q:
>         «R. Rama corta: corregir por su régimen la ventana declarada de ev-v9-003456-9ef48fb5 (empieza 2 s antes de su ancla, sobre la cola de un segmento en cuarentena; FILTRADAS-ESCENARIO-B.md §3).»
>    b) Alguna palabra citada cae en el segmento oculto: para. No registres el tramo, no toques el ítem y no declares nada. Dame solo índices y milisegundos, y yo decido la exposición y qué se hace con el ítem.
>    c) La localización falla o es ambigua: para y dime por qué, también sin texto.
>
> 3. Lección para la fila de ERRORES-RECURRENTES (del consultor):
>    importa · El consultor dio por hecho, sin medirlo, que la línea visible empezaba en la marca del fin del bloque. La comprobación (b) lo desmintió. Lección: las hipótesis sobre marcas truncadas se escriben como comprobaciones con parada, nunca como premisa de una decisión.
>
> 4. El criterio de SESION-DE-PREGUNTAS.md: la condición de mi tercera respuesta («el tramo termina en el inicio del ítem…») se cambia por esta, porque la otra se apoyaba en la premisa que ha fallado:
>    «Si el segundo de margen solapa la ventana declarada de un ítem ev-*, se mide el ancla del ítem con la localización de validate, sin texto. Si el ancla está fuera del bloque, el tramo termina en el inicio de la ventana del ítem y la ventana se corrige por su régimen. Si el ancla cae dentro del bloque, se para y decide el consultor.»
>    Test sintético contra tramo_no_citable (verificacion.py:358): un tramo que termina justo en el inicio de la ventana de un ítem pasa, y uno que se mete 1 ms en ella falla.
>
> 5. Lo demás sigue como en mis respuestas segunda y tercera: los puntos 3 a 6, el texto de Q con el solapamiento de más de 0 ms, make check sellado, fix/ con la CI de Linux y sus números de run, y el revisor con la pregunta expresa sobre tramos e ítems.
>
> Rama lista para revisión, NO cerrada.

## Quinta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Quinta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Aleks ha hecho a mano el commit y el push a fix/. Cópiala tal cual al encargo y al informe, en un commit nuevo.
>
> 1. Comprueba que el commit que hizo Aleks es el que preparaste: el mensaje es el de msg-tramos.txt, el árbol coincide con el sello 5727c7de… y no se coló ningún fichero más. Comprueba también que fix/filtradas-escenario-b apunta a ese commit. Si algo no cuadra, para.
>
> 2. El tramo de 2.084.000 a 2.096.000 ms no se registra, y aceptamos la desviación.
>    Por qué: es idéntico al original, y duplicarlo no tapa nada. Basta con que el informe explique que ese tramo se queda sin margen por la condición del ancla, nombrando ev-v9-003456-9ef48fb5 y R.
>
> 3. El hallazgo para Q: se acepta que Q tape la línea visible que cae en el segundo de margen de esos 9 tramos.
>    Por qué: tapar de más no expone nada, y ningún ítem tiene su ventana ahí (tramo_no_citable lo garantiza). Aplicar los tramos por los milisegundos reales de los segmentos de cuarentena obligaría a leerlos de la cruda, y eso es otra vía que no hace falta.
>    Añade al texto de Q en la Next Action: «Se acepta que la regla de más de 0 ms tape el segmento visible que cae en el segundo de margen de un tramo (9 casos, FILTRADAS-ESCENARIO-B.md); el informe de Q da su recuento.»
>
> 4. Las tres lecturas de tramos de precaución de v10 durante trabajo/sesion-04 (0:40:20, 1:27:44 y 1:56:07) se declaran hoy en docs/validation/HOLDOUT-EXPOSICIONES.md, como exposición de precaución.
>    - Por cada una: fecha, quién (sesión o revisor), qué se vio por su clase (un grep, una descripción, una cifra en el cuerpo de c489685) y dónde queda (historia de git, inmutable). Sin copiar el contenido en ningún sitio nuevo.
>    - Sigue el procedimiento de knowledge/cases/holdout/README.md para una exposición. Con casos_ocultos y casos_reservados, sin abrir nada, dime si el mes al que apunta cada tramo tiene días en alguna partición reservada o en el universo de marzo. Si los tiene, para antes de marcar nada y dame los recuentos (no las fechas). Yo decido si algo queda quemado.
>    - No se reescribe la historia de git ni se toca c489685.
>    Por qué: un tramo de precaución existe porque su texto puede tocar un mes con días ocultos, y lo leído ya no se puede deshacer, pero sí declarar.
>
> 5. Sigue: CI de Linux sobre el commit de Aleks y sobre el nuevo, con sus números de run (único fallo aceptado: state check por el nombre fix/). Si el push del commit nuevo vuelve a bloquearse, para y dame los comandos con «!», como esta vez. Después, el revisor con su informe pegado al final, más dos preguntas expresas: (a) que ningún tramo nuevo pise la ventana de ningún ítem y que todos pasen el control positivo; (b) que la declaración del punto 4 no copie contenido de los tramos.
>    La fila de ERRORES-RECURRENTES lleva los hallazgos de mis respuestas segunda, tercera y cuarta.
>
> Rama lista para revisión, NO cerrada.

## Sexta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Sexta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Las tres lecturas de tramos de precaución de v10 ya estaban declaradas en la fila del 2026-10-04 de HOLDOUT-EXPOSICIONES.md: la de trabajo/sesion-04, con la corrección del consultor sobre junio y el commit c489685. El grep del revisor y la descripción de su A6 son el mismo contenido.
>    Mi punto 4 de la quinta respuesta pedía declararlas de nuevo porque escribí sin leer el fichero. Queda así: no hay exposición nueva.
>
> 2. En HOLDOUT-EXPOSICIONES.md, por su régimen (solo añadir; la fila del 2026-10-04 no se toca), una fila nueva con fecha de hoy y estas columnas:
>    - qué: «Complemento a la fila del 2026-10-04 (v10, sesión 4). Recuento por partición del alcance de sus tres tramos de precaución, sin abrir nada (anexo meses_de_los_tramos.py, FILTRADAS-ESCENARIO-B.md): 0:40:20, enero, sin días reservados; 1:56:07, junio, 11 días (holdout-1: 2, holdout-2: 4, holdout-3: 5); 1:27:44, periodo no identificado, que no se puede descartar en ningún mes reservado (fidelidad-1: 10, holdout-1: 8, holdout-2: 8, holdout-3: 8, y febrero y marzo de 2026 enteros). Las lecturas posteriores (grep y A6 del revisor de trabajo/sesion-04, cuerpo de c489685) son el mismo contenido ya declarado.»
>    - particiones: las que da el recuento.
>    - quién: la sesión autónoma de trabajo/filtradas-escenario-b; la decisión, del consultor.
>    - ¿quema?: «No. Decisión del consultor (2026-10-04): lo visto son agregados sin fecha, un máximo de operaciones en un día y tres valores de R, que no identifican ningún día reservado ni permiten ajustar decisiones a un día concreto. Las cifras siguen excluidas de todo uso, como dice la fila del 2026-10-04, y además: ninguna regla ni parámetro sobre el número de operaciones por día o sobre el R de salida puede tener esas cifras como fuente. F26 cita las dos filas.»
>    No copies las cifras de los tramos en la fila nueva ni en ningún otro fichero nuevo: «un máximo de operaciones en un día» y «tres valores de R» bastan.
>
> 3. Para la fila de ERRORES-RECURRENTES, además de mis hallazgos anteriores:
>    importa · Del consultor: pidió declarar unas lecturas que ya estaban declaradas, porque no leyó HOLDOUT-EXPOSICIONES.md antes de escribir la orden. Lección: antes de ordenar una declaración de exposición, leer la tabla y citar la fila que ya cubre el caso, si la hay.
>
> 4. Sigue: make check sellado, commit, y push a fix/filtradas-escenario-b con la CI de Linux y sus números de run (único fallo aceptado: state check por el nombre fix/). Si el commit o el push se bloquean, para y dame los comandos con «!».
>    Después, el revisor con su informe pegado al final y tres preguntas expresas:
>    (a) ningún tramo nuevo pisa la ventana de ningún ítem, y todos pasan el control positivo;
>    (b) la fila nueva de HOLDOUT-EXPOSICIONES no copia contenido ni cifras de los tramos y no modifica la del 2026-10-04;
>    (c) el texto de Q y de R en la Next Action coincide con mis respuestas.
>    Y la fila de ERRORES-RECURRENTES.
>
> Rama lista para revisión, NO cerrada.
