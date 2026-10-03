# Encargo · trabajo/reabrir-y-fuente-documental

Dado por Aleks (consultor) el 2026-10-03. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva trabajo/reabrir-y-fuente-documental, desde main. Antes de abrirla, verifica que main está en d942aff y que stable/F36s-renovar-cierres es el último stable/*; si no coincide, para y dímelo. Ábrela con la skill abrir-rama: este prompt, tal cual, en docs/encargos/, más contrato.yaml y el archivo en HISTORIA.
>
> OBJETIVO: pagar dos deudas de Technical Debt de PROJECT_STATE antes de procesar la sesión 4: (1) una acción de feedback para REABRIR una ambigüedad; (2) que una ambigüedad pueda citar una fuente documental (una regla de FTMO) en vez de una cita de evidencia de relleno.
> NO CAMBIA: el motor, la estrategia, los parámetros, ninguna cifra, ni el material del corpus. No se abre nada de v7 en adelante (cuarentena): para A-36 basta con su registro de feedback y ambiguedades.yaml, sin tocar la transcripción.
>
> FASE 0, inventario sin tocar nada. Entrégamela antes de escribir código:
> 1. Cómo está hoy el modelo de feedback (src/botsito/feedback/modelo.py, aplicar.py, validation/knowledge.py, botsito feedback pending): las acciones, qué objetivo admite cada una, qué exige y cómo se cierra o se abre una ambigüedad. Cita fichero y línea.
> 2. El caso de A-36 tal como está: los registros fb-…-626c4dc7 (el cierre) y fb-2026-09-29-sesion-03-a0b61bc9 (la reapertura con RESOLVE_UNKNOWN y valor «sin resolver»), y por qué feedback pending la cuenta como pendiente. Mídelo con el comando, escrito tal como lo ejecutas (uv run botsito feedback pending …), con su salida.
> 3. Cómo exige hoy el esquema de ambigüedades la cita de evidencia, y qué ambigüedades llevan una de relleno: A-27, A-54 y las que encuentres. Busca la condición, no te quedes en esas dos.
> 4. Propuesta para cada deuda, con alternativas y su coste:
>    a) REOPEN: qué objetivo admite (¿solo ambigüedad?), qué exige (motivo literal, supersede del registro que la cerró, procedencia), cómo la ven feedback pending, knowledge validate y los documentos generados, y cómo se migra A-36 sin editar ningún registro existente (feedback solo añade).
>    b) Fuente documental: cómo se declara (¿un tipo de fuente nuevo que apunte a un documento commiteado del repo, como docs/validation/FTMO-REGLAS.md, con su sección o su literal?), qué guardia comprueba que el documento y la cita existen, y para qué clases de ambigüedad se admite. Nombra la condición y niega por defecto: una fuente documental no puede sustituir a la evidencia del trader en una ambigüedad de clase «pregunta».
> 5. Qué documentos, runbooks y sitios de CLAUDE.md repiten las reglas que cambian («cinco sitios» al abrir o cerrar una ambigüedad, AMBIGUEDADES.md, el revisor), para que la Fase 1 los toque todos.
>
> FASE 1, tras mi visto bueno:
> - Las dos piezas, con sus tests. Cada guardia nueva se rompe a propósito y se comprueba que falla: un REOPEN sin motivo o sin supersede, un REOPEN sobre algo que no es una ambigüedad cerrada, una fuente documental que apunta a un fichero o a una sección que no existe, y una fuente documental en una ambigüedad de clase «pregunta».
> - A-36 migrada al REOPEN con un registro nuevo, y feedback pending ya sin contarla como pendiente por el apaño.
> - A-27 y A-54 (y las que salgan en la Fase 0) con su fuente documental en lugar del relleno, con trailer Fuente: válido.

**SUSTITUIDO (2026-10-03, decisión 4 del consultor, «Segunda orden», abajo).** Las que se migran
son cuatro: A-54 (R13), A-55 (R15 y el ticket), A-27 (R11) y A-28 (R10); en A-27 y A-28 solo
sale el ítem de FundedNext, y A-44 queda fuera. Recuadro de la sesión, no del consultor: lo
citado arriba y abajo sigue tal cual.

> - Los documentos generados regenerados, y los runbooks y CLAUDE.md actualizados donde repitan la regla.
> - Si alguna de las dos deudas se cierra, su línea sale de Technical Debt en la rama, con el texto entero movido a HISTORIA.
> Si tocas rutas o el sistema de archivos, push como fix/trabajo-reabrir-y-fuente-documental y CI de Linux en verde antes del merge; dame los números de run.

**SUSTITUIDO EN PARTE (2026-10-03, medido; informe §1.7).** Con ese nombre la CI sale roja en
`contrato` antes de correr un solo test (run 195): `scripts/contrato_rama.py` quita solo el
primer prefijo, y `trabajo-reabrir-…` no es `reabrir-…`. La rama se empuja con el nombre de
`docs/runbooks/RITUAL.md` («Antes del merge: la CI de Linux»), `fix/reabrir-y-fuente-documental`.
Recuadro de la sesión, no del consultor.

> Informe en docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md, con el revisor al final y su informe pegado.
>
> Rama lista para revisión, NO cerrada.

## Segunda orden: decisiones del consultor sobre la Fase 0 (2026-10-03)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisiones del consultor sobre la Fase 0 de trabajo/reabrir-y-fuente-documental (2026-10-03). Cópialas con su fecha al informe y al final del encargo, y pon un recuadro SUSTITUIDO en lo que reemplacen:
>
> 1. REOPEN, aprobado tal como lo propones: solo sobre ambigüedades, supersede obligatorio al último registro de la cadena y sin valor. Un REOPEN activo exige ABIERTA, una RESUELTA exige un cierre activo, y una DECIDIDA solo se reabre con un ADR. Tests añadidos a los que pedía el encargo, cada uno roto a propósito: el ciclo completo cerrar → reabrir → volver a cerrar tiene que funcionar; un REOPEN sobre una ambigüedad que nunca se cerró, o sobre una DECIDIDA, tiene que fallar; y la guardia nueva de RESUELTA tiene que cazar una RESUELTA cuyo único cierre está superseded.
> 2. Migración de A-36: un registro nuevo con procedencia reexpresion_consultor (modelo.py:113, «sin respuesta nueva: lo mismo, en el tipo que espera el registro»), que supersede a a0b61bc9. Lleva la misma fecha que a0b61bc9 y recibido_el 2026-10-02. Motivo: según knowledge/feedback/README.md, recibido_el es el día en que llegó la respuesta, y aquí no llega nada nuevo: se reescribe la decisión del 2026-10-02. El literal cita a0b61bc9 y su motivo. No se edita ningún registro existente. Antes de escribirlo, comprueba si algún registro reexpresion_consultor anterior sigue otra convención para las fechas; si la hay, para y dímelo.
> 3. fuentes_documentales, aprobado: solo en ambigüedades de clase medicion, la evidencia solo puede quedar vacía si hay al menos una fuente documental, y por defecto se niega. Además, por ser una lectura de rutas:
>    - la ruta se normaliza y tiene que quedar dentro de docs/; cualquier «..», ruta absoluta o enlace que salga de docs/ se niega (es el agujero de leer_fichero, patrón 3 de ERRORES-RECURRENTES);
>    - el ancla tiene que ser un encabezado que exista en el documento, y el literal tiene que aparecer tal cual dentro de la sección de ese ancla, no en cualquier parte del fichero;
>    - test roto a propósito para cada condición: «..», ruta fuera de docs/, documento sin commitear, ancla que no existe, literal fuera de su sección y fuente documental en una pregunta.
>    Como lee rutas, push como fix/trabajo-reabrir-y-fuente-documental y CI de Linux en verde antes del merge; dame los números de run.
> 4. Las cuatro migraciones aprobadas: A-54 (R13), A-55 (R15 y el ticket), A-27 (R11) y A-28 (R10). En A-27 y A-28 solo se cambia el ítem de FundedNext. A-44 queda fuera: su evidencia es del trader (las citas de v4 y v9 que ya tiene), no relleno. Si tras las cuatro el ítem de FundedNext sigue citado en alguna ambigüedad, dime cuál y por qué.
> 5. PROJECT_STATE: el único tope es el de 25 KB de tests/unit/test_project_state.py. No hay ningún «margen de 23.000» en CLAUDE.md, los runbooks, .claude/ ni el test (lo he buscado). No lo vuelvas a citar; si lo sacaste de algún sitio del repo, dime de cuál.
>
> Lo demás, como en el encargo: los documentos generados regenerados; CLAUDE.md, los tres runbooks, los dos README de knowledge/ y el revisor actualizados donde repitan la regla; y las dos líneas de Technical Debt fuera de PROJECT_STATE y movidas a HISTORIA, si se pagan enteras.
> Informe en docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md, con el revisor al final y su informe pegado.
>
> Rama lista para revisión, NO cerrada.
