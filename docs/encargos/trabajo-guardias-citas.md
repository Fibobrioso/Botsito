# Encargo · trabajo/guardias-citas

Dado por el consultor el 2026-10-05. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Encargo de rama: trabajo/guardias-citas (consultor, 2026-10-05). Paga dos líneas de Technical Debt de PROJECT_STATE.md.
>
> BASE
> main en 442a948 (commit de estado de stable/F37a-respuestas-ftmo), CI de main run 37411332514 en verde. Compruébalo antes de abrir; si no cuadra, para. Abre con la skill abrir-rama (encargo en docs/encargos/, contrato.yaml, archivo de PROJECT_STATE en HISTORIA). Copia este prompt tal cual al encargo.
>
> OBJETIVO
> Dos guardias nuevas, con tests que las rompen a propósito:
> G1. Un ítem de evidencia supersedido no se cita desde la spec ni desde las ambigüedades.
> G2. Todo commit que toque tramos_no_citables.yaml lleva trailer Fuente:.
> NO cambia: motor, broker, freno, strategy_spec, parámetros, contenido de knowledge/evidence ni de tramos_no_citables.yaml, cifras. No se abre ni se cierra ninguna ambigüedad. No se lee el contenido de material en cuarentena: las guardias trabajan con ids, estados y metadatos de git, no con citas ni transcripciones.
>
> FASE 0 · INVENTARIO SIN TOCAR NADA (entrégala antes de escribir código)
> a) G1:
>    - Cómo se sabe hoy que un ítem ev-* está supersedido: campo, fichero y función que ya lo lean (por ejemplo, la de knowledge validate o la de evidence).
>    - Qué ficheros versionados citan ids ev-*. Como mínimo: knowledge/spec/strategy_spec.yaml, parametros.yaml, ambiguedades.yaml, y docs/spec/ generado.
>    - El recuento ACTUAL de citas a ítems supersedidos en cada uno, con el id, el fichero y la línea, medido con un comando.
>    Si el recuento no es cero, PARA: cada cita necesita decisión del consultor (sustituir o mantener) y no se arregla en esta rama sin ella.
> b) G1: qué ficheros quedan FUERA de la guardia y por qué. Los informes cerrados de docs/validation/, HISTORIA, los encargos y los campos de supersede de los propios ítems citan ids viejos legítimamente. Propón la condición en positivo (qué ficheros se vigilan) y niega por defecto todo fichero de knowledge/spec/ nuevo: un fichero nuevo bajo knowledge/spec/ entra en la guardia salvo que se excluya a la vista.
> c) G2:
>    - Cómo exige hoy el repo el trailer Fuente: (test, hook, función) y sobre qué rutas.
>    - Cuántos commits de la historia tocan tramos_no_citables.yaml y cuántos de ellos NO llevan Fuente:, con sha y fecha.
>    - Propón el ancla para no tocar los viejos: un sha fijado en el test a partir del cual se exige, nunca una fecha, y que el test falle si el ancla no existe en la historia.
> d) Si G2 lee la historia de git, di si hay algo dependiente de la plataforma (codificación, core.quotepath, finales de línea, clon superficial en la CI).
>
> DECISIONES (aplícalas salvo que la fase 0 las contradiga; si las contradice, para)
> 1. G1 va en knowledge validate (y por tanto en make check), junto a las comprobaciones de citas que ya existen. Mensaje de error: el id, su sustituto si lo tiene, fichero y línea.
> 2. G2 va como test en CI contra la historia de git, como las guardias de inmutabilidad (Decisions and Rationale, 2026-09-04: la garantía es el test de CI, el hook es comodidad). Exige Fuente: en todo commit posterior al ancla que toque tramos_no_citables.yaml. Los commits anteriores al ancla no se tocan y se listan en el informe.
> 3. Tests que rompen las guardias a propósito, en un repo o fixture temporal y nunca sobre el repo real:
>    - G1: una cita a un supersedido en ambiguedades.yaml y otra en un fichero nuevo bajo knowledge/spec/ hacen fallar la guardia; una cita al sustituto pasa.
>    - G2: un commit posterior al ancla sin Fuente: falla; con Fuente: pasa; un ancla inexistente falla.
> 4. Las dos líneas de Technical Debt («Nada avisa cuando la spec o las ambiguedades citan un item ev-* supersedido…» y «Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml…») salen de PROJECT_STATE.md y pasan literales a HISTORIA, en esta rama. El saldo de bytes de PROJECT_STATE en esta rama tiene que ser menor o igual que cero.
> 5. Una guardia no se rodea: si para que pase hay que tocar una guardia existente, para y dímelo.
>
> COMPROBACIONES
> - make check y uv run botsito state check en verde, con su salida en el informe.
> - Como G2 lee la historia de git, empuja fix/guardias-citas y pasa la CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Da el número de run.
> - Trailer Fuente: en los commits que lo pidan.
>
> INFORME
> docs/validation/GUARDIAS-CITAS.md: fase 0 con su evidencia, tabla encargo frente a lo hecho, desviaciones, tests nuevos y qué rompen, run de la CI de Linux y bytes de PROJECT_STATE.
>
> REVISOR
> Pasa el revisor y pega su informe al final. Que compruebe aparte que G1 niega por defecto los ficheros nuevos de knowledge/spec/, que el ancla de G2 es un sha y no una fecha, y que ningún test escribe en el repo real.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la fase 0 (2026-10-05)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la fase 0 de trabajo/guardias-citas (2026-10-05). Cópiala tal cual al encargo y al informe.
>
> 1. Las 4 citas de A-10 (dos), A-11 y A-18: SE SUSTITUYEN por su sustituto, como A-46 en VENTANA-EV-V9.md. Antes de sustituir, compara para cada par (viejo → sustituto) la cita y la afirmación tal como están en los ítems, con la CLI filtrada o leyendo los campos del ítem, nunca transcripciones. Si en algún par el sustituto ya no sostiene lo que la ambigüedad cita (por ejemplo, porque recortó esa parte), para con ese par y dímelo; los demás siguen. Las ambigüedades no cambian de estado. Commit con Fuente:, spec docs --escribir en el mismo commit y el procedimiento de AMBIGUEDADES.md. El contrato se amplía con ambiguedades.yaml y docs/spec/, declarado.
>    Porqué: la spec cita el ítem vigente; un supersedido solo se nombra para contar la sustitución.
>
> 2. Condición de G1, ni A ni B: «En todo fichero versionado bajo knowledge/spec/, un id ev-* supersedido solo puede aparecer dentro del mismo valor escalar de YAML, o de la misma línea de comentario, que nombra su sustituto. Cualquier otra aparición falla.» Se escanea el texto entero, comentarios incluidos, sin lista de campos. Lista de excluidos visible en el código y vacía. docs/spec/ fuera por ser generado, como propones.
>    Comprueba con la medida que, tras el punto 1, el recuento da 0 y que las 5 menciones en prosa (RN-034 y el comentario de A-41) pasan. Si alguna no nombra a su sustituto en el mismo valor o comentario, para: no se toca strategy_spec.yaml sin decisión.
>    Tests que rompen la guardia: un supersedido en el campo evidencia: (falla); el mismo id en una nota sin su sustituto (falla); con su sustituto en la misma nota (pasa); en un fichero nuevo bajo knowledge/spec/ (falla).
>    Porqué: nombrar la condición y negar por defecto; enumerar campos deja escapar el que nadie pensó.
>
> 3. commits_sin_fuente: SÍ al parámetro opcional que solo cambia el texto del mensaje. Con el valor por defecto, el mensaje tiene que ser byte a byte el actual: añade un test que lo compruebe, y los tests existentes no se tocan. Nada de un bucle propio en el test.
>    Porqué: un bucle paralelo que repite la guardia es una segunda vía que puede divergir.
>
> 4. Ancla de G2: aceptado c489685, fijado como sha en el test y que el test falle si no existe en la historia. Los tres commits que deja fuera (cfec50b, c489685 y f443eee) se listan en el informe.
>
> 5. Las dos líneas de Technical Debt salen de PROJECT_STATE.md cuando las guardias existan, en esta rama, y pasan literales a HISTORIA. El saldo final de bytes tiene que ser menor o igual que cero.
>
> Sigue con el encargo: make check y uv run botsito state check en verde, fix/guardias-citas con la CI de Linux y su número de run, y el revisor con su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
