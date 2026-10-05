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
