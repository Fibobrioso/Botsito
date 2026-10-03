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
> - Los documentos generados regenerados, y los runbooks y CLAUDE.md actualizados donde repitan la regla.
> - Si alguna de las dos deudas se cierra, su línea sale de Technical Debt en la rama, con el texto entero movido a HISTORIA.
> Si tocas rutas o el sistema de archivos, push como fix/trabajo-reabrir-y-fuente-documental y CI de Linux en verde antes del merge; dame los números de run.
> Informe en docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md, con el revisor al final y su informe pegado.
>
> Rama lista para revisión, NO cerrada.
