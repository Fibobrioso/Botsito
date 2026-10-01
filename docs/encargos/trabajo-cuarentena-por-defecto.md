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
