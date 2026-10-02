# Encargo · trabajo/ajustes-cierre

Dado por Aleks (consultor) el 2026-10-01, tras el cierre de `trabajo/cuarentena-por-defecto`.

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/ajustes-cierre, desde main (72d0d20, tag stable/F36l-cuarentena-por-defecto). Solo documentación y la skill cerrar-rama: no cambia código, spec, cifras ni datos.
>
> 1. knowledge/corpus/tramos_no_citables.yaml: el comentario que dice que un tramo «se puede leer y buscar con kb find» ya no es cierto desde F36l. Corrígelo para que diga lo que hace hoy el código (kb find y kb at los ocultan por defecto; la opción cruda es solo de Aleks en su terminal). Antes, comprueba qué régimen de cambio tiene ese fichero en CLAUDE.md y respétalo: si un cambio ahí exige trailer Fuente:, usa el id del ADR o del informe CUARENTENA-POR-DEFECTO que corresponda, y si ese fichero no admite edición, dímelo y para.
>
> 2. Skill cerrar-rama y RITUAL.md: que digan sin ambigüedad que todo cierre lleva, en la rama y en el mismo commit que saca el contrato:
>    - el registro del cierre en docs/state/HISTORIA.md, con stable/<tag>^{commit}, los commits y los runs de CI;
>    - la fila de la rama en la tabla de docs/runbooks/ERRORES-RECURRENTES.md, con los hallazgos del revisor y los del consultor (si la orden no los trae, la sesión los pregunta).
>    Y que en el commit de estado no se añade nada a Change Log ni a Completed Features. Es obligatorio aunque la orden de cierre no lo repita.
>
> 3. Busca en CLAUDE.md, docs/runbooks/ y las skills otras frases que digan que la CLI enseña la cruda sin filtrar o que kb find muestra tramos no citables, y corrígelas igual. Lista lo que cambiaste.
>
> Ritual normal con make check sellado. No toca hooks ni la plataforma, así que no hace falta la CI de Linux por fix/. Pasa el revisor y pega su informe.
> «Rama lista para revisión, NO cerrada.»
