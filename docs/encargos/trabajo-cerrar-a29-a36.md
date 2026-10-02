# Encargo · trabajo/cerrar-a29-a36

Dado por Aleks (consultor) el 2026-10-02. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/cerrar-a29-a36, desde main (487c64f, tag stable/F36n-escenarios-por-sesion). Tarea autónoma: NO se cierra.
>
> Objetivo: cerrar dos ambigüedades que ya tienen respuesta grabada del trader y siguen ABIERTAS (docs/sesion-4/PREGUNTAS.md §4):
> - A-29: v9 0:01:43, a la pregunta que ofrecía las tres lecturas → al_aparecer_punto_de_breaker;
> - A-36: v9 1:17:18, «Mecha incluida, siempre».
>
> 1. Antes de tocar nada, comprueba con la vía autorizada que los dos tramos están fuera de los tramos no citables y de la cuarentena de v9, y que la cita literal sale de la verificación de citas, no de memoria ni de PREGUNTAS.md. Si alguno cae en un tramo protegido, para y avísame.
> 2. Cierra cada una por docs/runbooks/AMBIGUEDADES.md, con los cuatro sitios: un FeedbackRecord RESOLVE_UNKNOWN por respuesta con su cita y tramo, feedback apply al registro, ambiguedades.yaml en RESUELTA, la regla de la spec que la cita y la tabla Known Ambiguities de PROJECT_STATE; más tests/unit/test_kit.py y spec docs --escribir, todo con Fuente: y los ids fb-* nuevos.
> 3. Si cerrar A-29 cambia el comportamiento del motor (cuándo se coloca la orden), dilo con un test sintético antes y después. Sin cobertura agregada sobre las 77.
> 4. Quita las dos de docs/sesion-4/PREGUNTAS.md si aparecían como pendientes, y pásalas a «ya respondidas».
> 5. De paso, como tocas tests/: corrige el comentario de SECCIONES_EXENTAS en tests/contract/test_documentos_vivos.py (pendiente de ajustes-cierre) y quítalo de la fila de ERRORES-RECURRENTES.
> 6. PROJECT_STATE por debajo de 23.000 bytes.
>
> Informe en docs/validation/CERRAR-A29-A36.md. make check sellado, revisor con su informe pegado.
> «Rama lista para revisión, NO cerrada.»
