# Encargo · trabajo/filtradas-con-tramos

Dado por el consultor el 2026-10-05, como tarea autónoma (Aleks no está). Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> TAREA AUTÓNOMA (Aleks no está; el consultor revisa por la tarde). No cierres nada.
>
> PASO PREVIO, solo lectura y fuera de la rama: con gh, mide el consumo de minutos de GitHub Actions de Fibobrioso/Botsito en los últimos 30 días como si fuera privado (cada job redondeado al minuto superior; Linux por 1): número de runs, total de minutos, media por run, el más largo, jobs del workflow con su SO, y si hay branch protection o rulesets (gh api). Va en una tabla al final de tu respuesta, no en el repo.
>
> RAMA: trabajo/filtradas-con-tramos, desde main. Comprueba que main está en 0bf71a2 y que stable/F36x-filtradas-escenario-b apunta a 5e486dc; si no, para. Ábrela con la skill abrir-rama y copia este prompt tal cual al encargo.
>
> OBJETIVO: es el punto Q de la Next Action. Que las filtradas de sesión que escribe scripts/transcribir_sesion.py tapen también los tramos no citables (knowledge/corpus/tramos_no_citables.yaml) de su vídeo, además de la cuarentena por meses. Lee el texto de Q en PROJECT_STATE.md y cúmplelo entero.
>
> QUÉ NO CAMBIA: la regla de cuarentena por meses (botsito.corpus.cuarentena, cases.holdout), el motor, la spec, el knowledge y los tramos ya registrados. No se toca .claude/ ni los hooks. Si para hacerlo hiciera falta tocar la guardia, PARA y escríbelo en el informe.
>
> REGLA DE LECTURA: no se lee ninguna cruda ni ninguna filtrada real. Todo se prueba con texto y segmentos sintéticos. La guardia solo deja ejecutar sobre una cruda el guion de main, así que el guion nuevo no se ejecuta sobre material real en esta rama, ni se intenta.
>
> FASE 0 (va en el informe; si no salta ninguna parada, sigues sin esperar):
> - dónde aplica hoy el guion la cuarentena, cómo están los segmentos (inicio y fin en ms), cómo se identifica el vídeo de cada sesión y cómo se leen los tramos (formato, función que los carga y validación);
> - si ya existe una función de la librería que dé los tramos de un vídeo; si existe, se usa esa y no una paralela.
>
> LA REGLA, escrita como condición:
> - un segmento se tapa si se solapa más de 0 ms con algún tramo de SU vídeo. El que empieza exactamente donde termina un tramo queda visible (el caso de borde de v9, 0:34:56);
> - la marca en la filtrada es distinta de la de meses: [NO CITABLE mm:ss–mm:ss], sin la clase ni el motivo del tramo, y los bloques contiguos se funden igual que los de cuarentena;
> - falla cerrado: si el fichero de tramos falta, no se puede leer o no valida, el guion NO escribe la filtrada y sale con error. Nunca escribe una filtrada sin aplicar los tramos;
> - el registro del guion da, sin texto, los recuentos por separado: segmentos tapados por meses, por tramos y por ambos.
>
> TESTS (sintéticos), cada uno con el caso negativo que demuestra que puede fallar:
> - solapamiento de 1 ms: se tapa; empieza justo en el fin del tramo: visible; termina justo en el inicio del tramo: visible;
> - un tramo de otro vídeo no tapa nada;
> - un segmento tapado a la vez por meses y por tramo cuenta en «ambos» y sale en un solo bloque;
> - fichero de tramos ausente o corrupto: no se escribe nada y el código de salida es distinto de 0;
> - rotura a propósito: desactivar la aplicación de tramos tiene que hacer caer al menos un test. Documéntalo y restáuralo;
> - los tests de la cuarentena por meses que ya existen siguen pasando sin cambiarse.
>
> PARADAS (para, escribe el informe y no sigas):
> - la fase 0 muestra que los segmentos no tienen ms fiables o que el vídeo de una sesión no se puede identificar sin ambigüedad;
> - hace falta tocar .claude/, la guardia, la regla de meses o leer material real.
>
> DOCUMENTOS
> - Informe en docs/validation/FILTRADAS-CON-TRAMOS.md: fase 0, regla, tests con sus roturas, desviaciones y tamaño de PROJECT_STATE.
> - Lo que queda para después del merge, sin hacerlo: «En la fase 0 de la rama de activación de la sesión 4, rehacer con --solo-filtrar las filtradas de v7–v10 y comprobar contra FILTRADAS-ESCENARIO-B.md que lo tapado es B más los tramos, que nada se destapa frente a A dentro de un tramo y que los 12 casos del segundo de margen quedan tapados.»
>
> CIERRE DEL TRABAJO (no de la rama)
> - make check sellado, commit y push como fix/filtradas-con-tramos, con la CI de Linux y su número de run. El único fallo aceptado es state check por el nombre fix/.
> - Si el clasificador bloquea el commit o el push, NO busques otra vía: deja los comandos exactos en el informe y en tu respuesta final, y para.
> - Revisor, con su informe pegado al final. Preguntas expresas: (a) que la regla de más de 0 ms es la que dice Q; (b) que no hay ningún camino que escriba una filtrada sin aplicar los tramos; (c) que ningún test lee material real.
>
> Rama lista para revisión, NO cerrada.
