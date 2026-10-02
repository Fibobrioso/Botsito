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

## Segunda orden: decisiones del consultor (2026-10-02)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Decisiones del consultor sobre trabajo/cerrar-a29-a36:
>
> 1. A-29: aceptada. En la nota del registro de la ambigüedad, cita docs/validation/SESION-03-EXTRACCION.md como fuente del contexto de la pregunta (v9 0:01:30), y di que hoy no se puede releer porque v9 está en cuarentena.
>
> 2. A-36: NO se cierra. La pregunta se hizo sobre una orden límite, y desde A-47 la entrada es con orden stop; además está C6 (v7, orden 2 puntos más allá del 0).
>    - Reábrela con un registro nuevo (el feedback solo admite añadir), con ese motivo.
>    - ambiguedades.yaml vuelve a ABIERTA, y se deshacen la tabla de PROJECT_STATE, test_kit.py, la hoja de preguntas y spec docs.
>    - Si algún parámetro cambió de estado por A-36, vuelve al de antes.
>    - Añade a docs/sesion-4/PREGUNTAS.md, junto a la pregunta 6 (sección A), una pregunta cerrada con «otra, ¿cuál?»: «Cuando pones la orden de entrada, ¿va exactamente en el 0 de la caja, contando la mecha, o unos puntos más allá? Si va más allá, ¿cuántos?». Cita A-36 y C6, sin fechas ni resultados.
>
> 3. docs/runbooks/AMBIGUEDADES.md: cerrar una ambigüedad toca cinco sitios, no cuatro (también scripts/hoja_preguntas.py y su test). Corrígelo, y también donde CLAUDE.md lo repita. Amplía el contrato a esos ficheros.
>
> PROJECT_STATE por debajo de 23.000 bytes. make check sellado; revisor solo sobre lo que cambie, con su informe pegado.
> «Rama lista para revisión, NO cerrada.»
