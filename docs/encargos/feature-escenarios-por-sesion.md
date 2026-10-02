# Encargo · feature/escenarios-por-sesion

Dado por Aleks (consultor) el 2026-10-01, tras el cierre de `trabajo/ajustes-cierre`.

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: feature/escenarios-por-sesion, desde main (a093ffb, tag stable/F36m-ajustes-cierre). Es A3 b) de los pendientes heredados de PROJECT_STATE: «sesiones independientes y varios escenarios por sesión: liquidez_tomada caduca al abrir la sesión…». Tarea autónoma: NO se cierra; deja la rama sellada y espera.
>
> Lo que ya dijo el trader (sesión 3, activado en feature/reflejar-feedback-s3; cítalo desde la evidencia y el feedback, no de memoria):
> - las sesiones de 07 a 11 y de 11 a 15 son independientes;
> - tras una operación, una toma nueva de liquidez de M15 abre un escenario nuevo (A-46).
>
> Fase 0 · Diseño, antes de escribir código (CLAUDE.md: «se contesta midiendo»):
> - Dónde vive hoy liquidez_tomada y por qué el bot traza una sola zona por día. Qué RN, ADR y parámetros tocan esto (RN-006, ADR-0056, A-46, A-35, A-43, A-25).
> - Propón el diseño: cuándo caduca un escenario, cuándo nace otro, cuántos puede haber por sesión, y qué pasa con una orden viva al cambiar de sesión.
> - Lo que dependa de preguntas aún abiertas de la sesión 4 (en particular la 15, la liquidez tomada antes de las 7, y la 18, los intentos por marca o por toma) va como PARÁMETRO del registro, con un valor provisional marcado PROVISIONAL y su pregunta citada. No inventes la regla.
> - Escribe el diseño en el informe antes de implementar.
>
> Fase 1 · Implementación:
> - Motor y spec con su régimen: trailer Fuente: con ids que existen, parámetros en el registro (ADR-0002) y sin literales de negocio.
> - Las tres guardias de cita si añades un sitio con cita propia.
>
> Fase 2 · Comprobación, SIN cobertura agregada:
> - NO calcules la cobertura ni ninguna cifra agregada sobre las 77 operaciones de construcción, ni sobre ningún subconjunto que la deje deducir. El consultor tiene pendiente pre-registrar el umbral de cobertura (Next Action J) antes de ver esa medida. Si algún test o informe existente la imprime sola, dilo y no la pegues en el informe.
> - Tests sintéticos: dos sesiones independientes; una segunda toma tras una operación cerrada abre un escenario nuevo; la liquidez de la mañana no vale para la tarde; una orden viva al cambiar de sesión según el diseño.
> - Con el visor, de 2 a 4 días de agosto (construcción, comprobados con casos_reservados) en los que el trader volvió a operar por la tarde: describe qué hace el bot ahora frente a antes, día a día, sin cifras agregadas.
>
> Informe en docs/validation/ESCENARIOS-POR-SESION.md, con el diseño, los parámetros provisionales y sus preguntas, y lo que queda para después de la sesión 4.
> Ritual normal con make check sellado, sin --no-verify. Si tocas algo dependiente de la plataforma, CI de Linux por fix/. Pasa el revisor y pega su informe.
> «Rama lista para revisión, NO cerrada.»
