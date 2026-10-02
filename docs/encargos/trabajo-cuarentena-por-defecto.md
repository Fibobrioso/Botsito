# Encargo · trabajo/cuarentena-por-defecto

Prompt de Aleks del 2026-10-01 que origina la rama, copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/cuarentena-por-defecto, desde main (c95ab8b, tag stable/F36k-dieta-y-skills). Usa la skill abrir-rama: guarda este encargo en docs/encargos/ y escribe el contrato.yaml antes de tocar código.
> Al abrir, apunta en docs/state/HISTORIA.md lo que quedó fuera del cierre de F36k: en main, make check da «1 skipped», que es el test del contrato saltándose porque contrato.yaml ya no existe.
>
> Objetivo: cerrar la Next Action «I». Los comandos que enseñan contenido del corpus respetan por defecto la cuarentena, los tramos no citables y el material reservado, y el contenido crudo solo sale con una opción explícita que la guardia bloquea para Claude. No cambia motor, spec, knowledge, datos ni ninguna cifra.
>
> Fase 0 · Inventario (sin tocar nada)
> Lista cada comando de botsito que imprime contenido (como mínimo kb find, kb at, transcript show y corpus frames show, y cualquier otro que encuentres). Para cada uno, indica si hoy filtra: (a) transcripciones en cuarentena, v7 en adelante; (b) tramos_no_citables de v6; (c) material de meses reservados o sin sortear y casos_reservados. Indica también de qué fichero o función sale cada lista. Entrega la tabla antes de escribir código.
>
> Fase 1 · Filtro por defecto
> - Cada comando oculta por defecto lo que cae en (a), (b) o (c), y al final dice cuántos elementos ocultó y por qué motivo. Nunca muestra su contenido, y nunca muestra fechas ni días de meses reservados.
> - Las listas se leen de donde ya están definidas. No se copian ni se escriben a mano dentro de los comandos: una sola fuente.
> - Opción explícita --crudo para ver todo. La usa Aleks en su propia terminal, nunca Claude.
> - Si algún script o pipeline interno (ingerir-sesion, make check, tests) necesita el contenido sin filtrar, que lo pida por la función de Python, no por la opción del CLI. Lista cuáles son.
>
> Fase 2 · Guardia
> - El hook .claude/hooks/guardia.py bloquea cualquier comando Bash que use --crudo, y su mensaje explica que esa opción es solo para Aleks en su terminal.
> - Como toca un hook, aplica la regla de RITUAL.md: empuja como fix/cuarentena-por-defecto y espera la CI de Linux antes de declarar la rama lista.
>
> Fase 3 · Tests
> - Para cada comando del inventario: por defecto oculta un tramo de cada tipo (a), (b) y (c), y con --crudo lo muestra.
> - El aviso de elementos ocultos no filtra fechas de meses reservados.
> - El hook bloquea --crudo en varias formas (al principio, al final, con = y con un valor) y deja pasar los mismos comandos sin esa opción.
> - Ningún test usa material reservado real: usa datos sintéticos.
>
> Informe en docs/validation/CUARENTENA-POR-DEFECTO.md, con la tabla de la fase 0 antes y después, y los runs de la CI de Linux.
> Ritual normal con make check sellado, sin --no-verify. Pasa el revisor y pega su informe al final.
> «Rama lista para revisión, NO cerrada.»

## Segunda orden: decisiones del consultor sobre §0.3 (2026-10-01)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisiones del consultor sobre §0.3:
>
> 1. Fuente de (a): sí a src/botsito/corpus/cuarentena.py, pero con una LISTA EXPLÍCITA de vídeos en cuarentena (v7 en adelante, y la excepción de v6 declarada ahí con su motivo), no con la deducción por drive_id: null. La deducción pasa a ser un test cruzado: falla si un vídeo con drive_id null no está en la lista, o si uno de la lista tiene drive_id, salvo las excepciones declaradas. Así un vídeo nuevo sin listar rompe make check en vez de quedar visible. El hook guarda su copia y un test comprueba que dice lo mismo que el módulo, como ya se hace con casos_reservados. La skill ingerir-sesion añade el paso «añadir el vídeo a la lista de cuarentena».
>
> 2. (c) dentro del texto: aprobado. Mueve en_cuarentena a src/ como única fuente para el script y la CLI, y aplícala a todos los vídeos. En el informe, por cada vídeo: total de segmentos, cuántos oculta (a), (b) y (c), y el porcentaje. Solo números, nunca contenido ni qué mes o día disparó la regla.
>
> 3. evidence propose: aprobado. Además, audita lo que ya existe en knowledge/_proposals/: cuántos ficheros y segmentos caen en (a), (b) o (c). Solo cuentas y nombres de fichero, sin imprimir contenido. No los borres ni los edites; si hay alguno, para y avísame.
>
> 4. Funciones de Python: el filtro va en las funciones, no solo en la CLI. buscar, en_instante, texto_entre y cargar_cruda filtran por defecto. El contenido sin filtrar se pide con un parámetro explícito crudo=True.
>    - Llamadores autorizados: la verificación de citas, transcribir_sesion.py y los tests.
>    - Un test recorre el código y falla si aparece un crudo=True fuera de esa lista.
>    - El hook bloquea los comandos Bash que contengan crudo=True o --crudo (python -c, heredocs, scripts nuevos), salvo make check y pytest sin argumentos extra.
>    - El resto del encargo sigue igual: fase 1, fase 2 y fase 3, CI de Linux como fix/cuarentena-por-defecto, revisor e informe.
>
> Sigue.

## Tercera orden: decisiones del consultor (2026-10-01)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisiones del consultor:
>
> 0. Desviación de glossary apply: no la acepto como está. Una función interna que lee la cruda sin crudo=True es una vía que el test de autorizados no ve. Haz que corpus glossary apply use crudo=True y añádelo a la lista de llamadores autorizados, con su motivo. Comprueba que no queda ninguna otra función que lea la cruda sin pasar por crudo=True, y que el test lo vigila.
>
> 1. Las 10 propuestas de knowledge/_proposals/: no se borran ni se editan.
>    - Añádelas a la guardia: una propuesta con segmentos ocultos no se puede leer. Que la lista salga de cuarentena.py, calculada, no escrita a mano.
>    - Auditoría, solo con cuentas e ids, sin contenido: ¿alguna evidencia o regla aceptada en knowledge/ cita un segmento que hoy cae en (b) o (c)? Para cada caso, da el id de la evidencia o regla, el vídeo y el motivo, (b) o (c). No toques nada de knowledge/. Si sale algún caso, para y avísame antes de declarar la rama lista.
>
> 2. Reglas viejas del hook:
>    - Quita el bloqueo de kb find sin --video: el filtro del código ya lo hace innecesario.
>    - Mantén como segunda capa los bloqueos de vídeos en cuarentena y de intervalos que pisan un tramo.
>    - Tests: kb find sin --video pasa la guardia; v7 y un intervalo que pisa un tramo de v6 siguen bloqueados.
>
> Después sigue: push como fix/cuarentena-por-defecto, CI de Linux, revisor e informe.
> «Rama lista para revisión, NO cerrada.»

## Cuarta orden: decisiones del consultor (2026-10-01)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisiones del consultor sobre trabajo/cuarentena-por-defecto:
>
> 1. Los 9 ítems de evidencia: knowledge/ no se toca.
>    a) Para cada ítem, comprueba por código si el segmento citado contiene una fecha que sea un día de casos_ocultos. Imprime solo el id del ítem y True o False, nunca el texto ni la fecha. Si alguno da True, para y avísame antes de seguir: sería una exposición real y hay que declararla.
>    b) kb find y kb at ocultan por defecto también la evidencia cuya cita cae en un segmento oculto, con el recuento y el motivo, igual que con los segmentos. --crudo la muestra. Test con un ítem sintético.
>
> 2. corpus transcript check: autorizado con crudo=True, con su motivo en la lista. Condición: solo imprime el resultado de la comprobación (OK o fallo, y el fichero), nunca contenido. Test que lo comprueba.
>
> 3. scripts/a18_buscar.py: se queda filtrado y sin autorizar.
>    - Sus cuatro salidas commiteadas contienen líneas que hoy se ocultan: añádelas a la lista calculada que bloquea la guardia, como las 10 propuestas.
>    - Explica en la cabecera del script que desde esta rama sus salidas salen filtradas y no reproducen las viejas.
>    - Si esas salidas viven en informes ya cerrados, pon un recuadro de corrección; no edites el cuerpo.
>
> 4. scripts/transcribir_sesion.py: si hoy no usa crudo=True, quítalo de la lista de autorizados. Negar por defecto: se autoriza cuando una función concreta lo necesite.
>
> 5. En CLAUDE.md, «Trampas medidas»: un texto que contenga literalmente la opción cruda o crudo=True (encargos, informes, mensajes de commit) se escribe con Write o Edit, no con un heredoc ni con -m, porque la guardia lo bloquea. Para el mensaje de commit, usa git commit -F con un fichero escrito con Write.
>
> 6. Apunta en el informe el run 36938253913, y el run nuevo cuando acabe la CI de Linux.
>
> Como vuelve a tocar la guardia: push como fix/cuarentena-por-defecto, CI de Linux, revisor solo sobre lo que cambie, y su informe pegado.
> «Rama lista para revisión, NO cerrada.»

## Quinta orden: respuestas del consultor a dos preguntas (2026-10-01)

Al hacer el punto 3 de la cuarta orden se midió
(`docs/validation/anexos/CUARENTENA-POR-DEFECTO/citas_de_salidas.py`, solo cuentas) qué ficheros
seguidos citan las líneas de las cuatro salidas que hoy se ocultan. Las preguntas y las respuestas,
copiadas tal cual del diálogo de la sesión:

> **Pregunta 1.** Dos informes cerrados citan líneas que hoy se ocultan, según la medición del anexo `citas_de_salidas.py`, que solo imprime cuentas: `A24-A21-A26-A34-CLASIFICACION.md` cita 3 y `A35-PIVOTE-FORMADO-CLASIFICACION.md` cita 4 (cuentan si coincide la mitad o más de sus ventanas de 30 caracteres). Hoy la guardia los deja leer. ¿Qué hago con ellos?
>
> **Respuesta:** «Bloquear y recuadro (Recommended)»: Se añaden a la lista calculada `ficheros_con_ocultos.txt`, que la guardia bloquea. El generador los calcula con el mismo método y el mismo umbral. Además llevan un recuadro de corrección arriba, sin tocar el cuerpo.
>
> **Pregunta 2.** Dos ítems de evidencia, `ev-v3-002130-8617c40b` (3 líneas) y `ev-v4-003451-d750e553` (5), copian texto de líneas que hoy se ocultan, pero su cita no cae en un segmento oculto. Por eso no estaban entre los 9 y el punto 1b no los oculta en kb find ni en kb at. No los he abierto; puede ser texto que el ASR repite en un segmento vecino. knowledge/ no se toca. ¿Qué hago?
>
> **Respuesta:** «Ocultar por contenido (Recommended)»: kb find y kb at ocultan también el ítem cuyo texto copia la mitad o más de una línea oculta, con su recuento y su motivo. Con la opción cruda se ven. Se añade un test sintético y se repite la comprobación 1a sobre estos dos (id y True/False).
