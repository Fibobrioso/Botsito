# Encargo · trabajo/dieta-estado

Dado por Aleks (consultor) el 2026-11-13, en un solo mensaje. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/dieta-estado (tramo «Carril: guardias y deuda» de la hoja de ruta; precedentes: trabajo/adelgazar-estado y trabajo/margen-pendiente). Encargo del consultor, 2026-11-13.
>
> 0. Apertura
> - Base: main en c473d4c9, el commit de estado sobre el merge e9314598, al que apunta stable/F39a-guardia-falsos-positivos (CI de main run 43459199788, según el informe final del cierre). Antes, git fetch --prune. Verifica con git main, origin/main y el tag, y que no hay otra rama abierta ni en local ni en origin; si algo no cuadra, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-dieta-estado.md (con Write), su contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tag de cierre: stable/F39b-dieta-estado (comprueba que no existe ni en local ni en origin).
> - Contrato: tramo "Carril: guardias y deuda", entre comillas y exactamente como el título de su sección en docs/plan/HOJA-DE-RUTA.md (verifícalo); riesgo bajo; en rutas_permitidas, además de lo que pone abrir-rama, docs/validation/HOLDOUT-EXPOSICIONES.md y docs/plan/HOJA-DE-RUTA.md (esta última SOLO para quitar la referencia HER:n de un pendiente heredado que salga, en el mismo commit, como hizo trabajo/margen-pendiente).
> - Informe: docs/validation/DIETA-ESTADO.md, que nace con su línea de PLANTILLA en sus primeros 600 caracteres.
> - La fila de HOLDOUT-EXPOSICIONES.md de los make check de la rama (leen el M1 de marzo y calientan con el de junio, Technical Debt) va ANTES del primero, con la forma de la de trabajo/guardia-falsos-positivos, así que entra en el commit de apertura: es una desviación de la verificación de abrir-rama, decláralo. Una fila por día.
> - Revisa /model antes de empezar: Opus en esfuerzo medio.
>
> 1. Objetivo, y por qué va ahora
> Bajar PROJECT_STATE.md (hoy 24.652 bytes; el tope del test es estricto, menos de 25.000) sacando a HISTORIA, o acortando, lo que ya no es presente, con los criterios de docs/state/README.md, «Que sale de PROJECT_STATE, y con que criterio», sin cambiarlos.
> Por qué ahora: los registros de cierre de F38z y F39a (HISTORIA, hacia :17702 y :17949) dejan dicho que la rama de activación de la 7a recorta antes de añadir. Esta rama lo hace antes, sin material, y quita ese paso del camino crítico: la ingesta y las activaciones de la 7a y la 7b añadirán texto a la Next Action. Va en el hueco hasta la grabación de la 7a y tiene que estar cerrada antes de su ingesta, porque solo cabe una rama abierta: hoy viernes 13, como mucho el sábado 14. Si el domingo, con la grabación hecha, no está para cerrar, PARADA y decido yo; no abras nada más.
>
> 2. Lo que NO cambia
> - Las entradas con letra de la Next Action, Known Ambiguities (test_kit.py), lo que solo toca el ritual (Current Branch y las demás) y las secciones y su orden (test_project_state.py). De la Next Action solo pueden salir líneas de su subsección «Pendientes heredados», por los criterios.
> - Los criterios de README, el tope de 25.000, el motor, la spec, knowledge/, las guardias, .claude/, el Makefile, los tests y cualquier fichero fuera de PROJECT_STATE.md, docs/state/HISTORIA.md, el informe, el encargo, el contrato, HOLDOUT-EXPOSICIONES.md y la excepción de la hoja de ruta de arriba. Si algo obliga a tocar otro fichero, PARADA.
> - La rama no lee ningún material del trader, ni velas, ni ticks, ni el holdout, y no ejecuta el arnés.
>
> 3. El criterio (README, sin cambiarlo; con tres precisiones mías)
> - Una línea de «Pendientes heredados», «Technical Debt» o «Reglas vivas» sale SOLO si cumple (a) HECHA o PAGADA, (b) REPETIDA, (c) SUSTITUIDA o (d) NO ES DE SU SECCIÓN, con su evidencia citada como dice README (fichero:línea, commit, tag o ADR), y con la sección del fichero, no solo el fichero (lección de trabajo/adelgazar-estado, ERRORES-RECURRENTES.md).
> - (e) ACORTADA es SOLO para líneas de Technical Debt (README), con sus reglas exactas: más de 200 bytes, arranque literal cortado al final de una frase o de un inciso en 160 bytes como mucho, nunca dentro de una ruta ni de un id, el sufijo literal de README, la cita del informe conservada delante si la línea la traía, y no se aplica si ahorra menos de 60 bytes (cómo se lee, en README y en MARGEN-PENDIENTE.md). Las líneas de Reglas vivas no se acortan.
> - Precisión 1: en (b), «otro sitio» es lo que dice README (otra entrada de la Next Action, CLAUDE.md o un runbook). Precisión 2: en (d), el sitio donde vive literal tampoco puede ser la hoja de ruta, un informe ni HISTORIA. Precisión 3: una línea ya ACORTADA no se vuelve a acortar. Las tres son decisión del consultor: decláralas así en el informe.
> - Antes de sacar un pendiente heredado, se lee su texto entero en HISTORIA (el Archivo donde está completo, no el arranque truncado de PROJECT_STATE) y se busca cada una de sus frases donde la condición dice que vive; si una rama anterior lo dejó (trabajo/adelgazar-estado, trabajo/margen-pendiente, trabajo/plataforma-adelantada), se lee por qué. Si sale, su HER:n sale de las Refs de la hoja de ruta en el mismo commit, y test_hoja_de_ruta.py tiene que pasar (lección de trabajo/margen-pendiente, ERRORES-RECURRENTES.md).
> - Niega por defecto: si hay duda, la línea se queda, y lo que se queda no se resume ni se reescribe. Una línea que se queda distinta de lo que manda el criterio es una desviación y se declara.
> - Lo que sale va al final de HISTORIA, literal, con su condición y su evidencia, en un bloque por clase (# Pendiente heredado SALE, # Technical Debt PAGADA, # Technical Debt RECLASIFICADA, # Technical Debt ACORTADA, # Regla viva SUSTITUIDA, seguido de «· sale de PROJECT_STATE.md en trabajo/dieta-estado (<fecha>)»), con la forma de los bloques que ya hay.
>
> 4. Fase 0 (inventario, sin tocar PROJECT_STATE)
> Una tabla con cada línea de las tres secciones: su arranque, sus bytes, la condición propuesta (a-e o «se queda») y la evidencia. Comprueba en particular, sin darlo por hecho, lo que hayan pagado las ramas desde el último recorte (registros de cierre de F38u a F39a en HISTORIA), por ejemplo lo que nombre cmp o G.6 (F39a), capa_hash, R6a.2 o LATIDO_SEG (F38z), las láminas o motor laminas (F38w y F38y) y la preparación de la sesión 7 (F38x). Da los bytes de cada sección antes y la previsión después.
> No pares: sigue a la fase 1, salvo que la previsión no baje de 24.000 bytes; entonces PARADA con lo que harías. Las dudosas se quedan y van a una lista aparte para mí.
>
> 5. Fase 1 · Aplicar
> Los bloques al final de HISTORIA y las líneas fuera de PROJECT_STATE, o acortadas, en commits sellados (estadiar → make check > make-check.log 2>&1 → leer exit 0, ningún failed y SELLO → commit). En cada make check, la línea PICO DE MEMORIA al informe. Además de test_historia.py, test_project_state.py, test_kit.py y test_hoja_de_ruta.py, leen PROJECT_STATE test_project_state_rutas.py, tests/contract/test_ids_citados.py y test_documentos_vivos.py: una acortada no puede dejar una ruta o un id a medias. Da el tamaño final exacto de PROJECT_STATE.md con wc -c.
>
> 6. El informe
> La tabla de la fase 0, lo que salió y adónde, lo acortado con sus bytes antes y después, la lista de dudosas, los bytes por sección antes y después, las desviaciones y el estado al final. Prepara también, para la orden de cierre, la fila de ERRORES-RECURRENTES.md de la rama.
>
> 7. Revisor y CI
> El agente revisor, con este alcance además de sus dos ejes: que nada salga sin evidencia que lo sostenga; que todo lo que sale o se acorta esté literal en HISTORIA; que lo que se queda no cambie ni un byte; que cada acortada sea de Technical Debt y cumpla las reglas de (e); que ninguna salga por (b) o (d) con un sitio que el criterio no admite; y que cada HER:n quitado de la hoja de ruta corresponda a un heredado que salió. Pega su informe al final del tuyo.
> La rama no toca hooks, rutas, el sistema de archivos ni código: no hace falta CI de Linux (RITUAL.md, hacia :94-96; precedente: trabajo/adelgazar-estado). Si el revisor o tú veis que algo la exige, PARADA.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-13)

Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/dieta-estado (2026-11-13). Cópiala tal cual en el informe, en su sección, y aplícala.
>
> 1. Opción 1: se acortan por (e) las cuatro líneas que lo admiten, tal cual las propones, con sus bloques literales en HISTORIA. El umbral de 24.000 bytes del encargo era un freno por si la rama no merecía la pena, no un objetivo: 609 bytes liberados dejan unos 957 de margen hasta el tope (hoy 348), y eso basta para la ingesta y la activación de la 7a. Decláralo en el informe como respuesta a la PARADA.
> 2. Opción 2, no: dejar en :152 solo la primera cita reescribe la línea, y (e) manda conservar la cita del informe. La :152 se acorta como en la opción 1.
> 3. Opción 3, no: la :120 (cherry-pick y rebase) se quedó por decisión del consultor en trabajo/margen-pendiente, y reabrir esa decisión por unos 130 bytes no compensa. Se queda.
> 4. Las tres dudosas se quedan, sin tocar un byte, como manda la negación por defecto:
>    - :96 (ADR 0087): que el número quede abandonado es una decisión aparte, ligada a S-15 de la sesión 5, y no se toma aquí.
>    - :100 (cli.py:2558 y :2438): los números de línea viejos no son ninguna de las condiciones de README. En la lista de dudosas del informe, una línea que diga que los corrige la próxima rama que toque esa línea o cli.py.
>    - :113 (la línea en blanco): README no la cubre y no es una línea con contenido. Se queda, y va a la lista de dudosas.
> 5. Lo demás, como dice el encargo: el pico de memoria del make check de la fase 0 entra en el informe en el próximo commit; el tamaño final exacto con wc -c; las pruebas de §5; y el revisor con su alcance. Después, «Rama lista para revisión, NO cerrada».
