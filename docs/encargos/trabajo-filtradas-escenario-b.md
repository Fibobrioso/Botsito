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
