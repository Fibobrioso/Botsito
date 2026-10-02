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

## Segunda orden: decisiones del consultor sobre §4 (2026-10-02)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Decisiones del consultor sobre feature/escenarios-por-sesion (§4):
>
> 0. Antes de decidir, busca en la evidencia y el feedback (kb find y kb at, filtrados) dos cosas que el consultor recuerda de la entrevista del 30 de agosto (v4) y que NO se dan por buenas sin cita:
>    a) que los break even no consumen intento;
>    b) que el día (o la sesión) termina en la primera operación ganadora.
>    Para cada una: el id del ítem o del registro con su tramo, o «no consta». Si consta b) y contradice que una ganadora solo cierre el escenario (RN-034), para y avísame antes de seguir.
>
> 1. Escenarios en una sesión movida: se mantiene A-46 (cada liquidez nueva tomada abre uno), pero el número máximo por sesión pasa a ser un parámetro max_escenarios_por_sesion, PROVISIONAL, con valor «sin_limite» y la pregunta citada. Busca si quedó respondida la subpregunta de la sesión 3 «¿cuántos escenarios nuevos puede haber en un mismo día como máximo?» (A-46). Si no, añádela a docs/sesion-4/PREGUNTAS.md, sección D, con el formato de las demás.
>
> 2. Seguir tras un break even: si 0a) consta, cítalo en RN-034 y en ADR-0066 y deja de marcarlo como lectura de la sesión. Si no consta, se queda PROVISIONAL y va a la sesión 4 como pregunta en la sección D.
>
> 3. Liquidez tomada antes de abrir la sesión: de acuerdo. Queda dentro de toma_antes_de_la_ventana (PROVISIONAL, pregunta 15); que el texto de la pregunta 15 en PREGUNTAS.md cubra también el caso de que el precio vuelva y la tome otra vez dentro de la sesión.
>
> 4. La orden pendiente cuando se abre otro escenario: no se acepta sin medida.
>    - Test sintético que fije el comportamiento actual (qué pasa con la orden viva del escenario anterior: se retira, se mueve o convive).
>    - Comprueba que no pueden quedar dos órdenes vivas a la vez.
>    - Cuenta los mensajes al servidor que genera el caso peor de una tarde de cinco escenarios, frente al tope de 2.000 al día de FTMO.
>    - Si el comportamiento no sale de una regla del trader, parámetro PROVISIONAL y pregunta en la sección D.
>
> Sigue sin cobertura agregada. make check sellado; revisor solo sobre lo que cambie, con su informe pegado.
> «Rama lista para revisión, NO cerrada.»

## Tercera orden: respuesta del consultor al aviso del punto 0 (2026-10-02)

La sesión paró en el punto 0 porque b) constaba en v4 y contradecía RN-034. La respuesta, copiada tal
cual:

> Sí: la versión vigente es la de la sesión 1 (fb-2026-09-09-sesion-01-af02495f y ev-v6-000732-f7189541 / ev-v6-000732-5945fd87): tras la ganadora el día sigue y se espera otra liquidez, que es RN-017 + RN-034. No hay contradicción con el diseño. Cita esa cadena (v4 sustituido o rechazado → sesión 1) en ADR-0066 y en el informe, para que nadie vuelva a leer la versión de v4 como vigente.
>
> 0a) consta: cita ev-v4-004832-6543b551 y ev-v9-013117-c683f9b5 en RN-034 y ADR-0066, y lo de seguir tras un break even deja de marcarse como lectura tuya.
>
> Sigue con los puntos 1, 3 y 4 de la orden tal cual. El 2 ya está resuelto por 0a).

## Cuarta orden: decisión del consultor sobre a1 (2026-10-02)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Decisión del consultor sobre a1:
>
> 1. Regla general (nombra la condición, no el caso): todo parámetro PROVISIONAL cuelga de una ambigüedad ABIERTA. Test nuevo que recorre el registro y falla si un parámetro PROVISIONAL no apunta a una ambigüedad ABIERTA de knowledge/spec/ambiguedades.yaml. Rómpelo a propósito para ver que falla.
>
> 2. Abre las ambigüedades que hagan falta para cumplirla, con docs/runbooks/AMBIGUEDADES.md (abrir toca dos sitios, y spec docs --escribir en el mismo commit):
>    - una para max_escenarios_por_sesion (pregunta 20 de docs/sesion-4/PREGUNTAS.md);
>    - una para orden_pendiente_al_abrir_escenario (pregunta 21), si tampoco tiene ambigüedad abierta;
>    - y cualquier otro parámetro PROVISIONAL que el test destape.
>    Usa los siguientes ids libres y cita cada pregunta en su ambigüedad. No cuelgues nada de A-25 ni de A-46.
>
> 3. Next Action: añade una línea nueva: «Freno duro de peticiones al servidor: hoy el código solo cuenta las peticiones y nada impide pasar de las 2.000 al día de FTMO (medido en feature/escenarios-por-sesion). Rama propia antes de operar en una cuenta real». No lo implementes en esta rama. Comprueba que PROJECT_STATE sigue por debajo de 25 KB.
>
> make check sellado; revisor solo sobre lo que cambie, con su informe pegado.
> «Rama lista para revisión, NO cerrada.»

## Quinta orden: decisiones del consultor sobre a1 y b1 de §7.4 (2026-10-02)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Decisiones del consultor:
>
> 1. intentos_tras_toma_nueva se queda en A-25: A-25 es la pregunta de los intentos (pregunta 18) y el parámetro le pertenece. Mi «nada en A-25» era no colgar de A-25 parámetros ajenos, como los de las preguntas 20 y 21.
>
> 2. sesgo_h4_tope_velas: corrige su descripción para que diga lo que es (CONFIRMED por ADR-0044, decisión del proyecto), sin la palabra PROVISIONAL. Régimen de parametros.yaml: spec docs --escribir en el mismo commit y trailer Fuente: ADR-0044. El test no cambia: sigue mirando solo el estado.
>
> 3. PROJECT_STATE está en 24.106 bytes y el cierre puede pasar del tope.
>    - Regla nueva en RITUAL.md y en docs/state/README.md: una entrada de Next Action que pasa a HECHA se mueve a docs/state/HISTORIA.md en la misma rama que la cierra, y en PROJECT_STATE no queda ni el resumen.
>    - Aplícala ya: la I (HECHA en F36l y F36m) sale de PROJECT_STATE a HISTORIA, con su texto literal.
>    - Si con eso no baja de 23.000 bytes, dime qué más ocupa sitio y no recortes nada por tu cuenta.
>
> make check sellado; revisor solo sobre lo que cambie, con su informe pegado.
> «Rama lista para revisión, NO cerrada.»
