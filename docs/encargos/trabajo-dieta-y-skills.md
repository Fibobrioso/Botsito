# Encargo · trabajo/dieta-y-skills

Prompt de Aleks del 2026-10-01 que origina la rama, copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/dieta-y-skills, desde main (df6aa2c, tag stable/F36j-guardia-linux).
> Objetivo: que cada sesión cargue menos contexto y que los rituales repetidos sean una sola orden. No cambia motor, spec, knowledge ni ninguna cifra. Primero guarda este encargo en docs/encargos/ y escribe su contrato.yaml.
>
> 0. Ajuste de la guardia de borrado remoto.
>    - Hoy bloquea borrar cualquier referencia remota, y eso choca con la regla nueva de RITUAL.md: cada fix/<rama> que se empuja para la CI de Linux hay que borrarla después.
>    - Permite `git push origin --delete <rama>` y `git push origin :<rama>` solo si la rama empieza por trabajo/, feature/ o fix/.
>    - Sigue bloqueando main, cualquier tag (stable/* incluido), refs/tags/, comodines y cualquier comando que no pueda decidir con seguridad.
>    - Tests: deja borrar fix/x y bloquea main, stable/F36j-guardia-linux, refs/tags/x y un borrado de varias referencias en el que una esté prohibida.
>    - Como toca un hook, aplica la regla de RITUAL.md: empuja como fix/dieta-y-skills y espera la CI de Linux antes de declarar la rama lista.
>
> 1. Dieta de PROJECT_STATE.md (407 KB el 2026-10-01).
>    - La historia de merges y los bloques «LO QUE DECÍA…» pasan a docs/state/HISTORIA.md, que solo se amplía y nunca se reescribe.
>    - PROJECT_STATE.md queda con: main y último tag; Next Action vigente; tabla de ambigüedades abiertas; deuda técnica; y las reglas vivas que hoy solo estén ahí (copiadas tal cual, no reinventadas). Objetivo: menos de 25 KB.
>    - Ajusta state check, el ritual y cualquier test o script que lea las secciones movidas.
>    - Comprueba que ningún texto se pierde: todo lo anterior está en HISTORIA.md o en PROJECT_STATE.md.
>    - Mide el tamaño antes y después, y lo que tarda en arrancar una sesión que lee los dos ficheros obligatorios.
>
> 2. Revisión de CLAUDE.md con los criterios de writing-for-agents (mattpocock/skills):
>    - quita lo que ya hace cumplir un test, un hook o el contrato y deja una línea que apunte a él;
>    - lo que solo se usa en algunos casos pasa a docs/runbooks/ con una línea de puntero clara;
>    - las prohibiciones se escriben primero en positivo (qué hacer) y después la guarda.
>    Entrega el antes y el después en KB y la lista de lo movido.
>
> 3. Skills del proyecto en .claude/skills/:
>    - cerrar-rama: el ritual completo de RITUAL.md (merge, tag, PROJECT_STATE, make check sellado, commit de estado, push atómico, CI en verde, y borrado de la rama local y de su fix/<rama> remota si existe); solo se ejecuta si el usuario lo ordena;
>    - ingerir-sesion: el pipeline de una grabación del trader (comprobación de audio, cuarentena, transcripción, extracción por pregunta y evidencia);
>    - abrir-rama: crea la rama, guarda el encargo en docs/encargos/ y escribe el contrato.yaml.
>    Cada skill indica entradas, límites, herramientas, artefacto y verificación. No duplican RITUAL.md: lo citan.
>
> 4. Registro de errores recurrentes: completa docs/runbooks/ERRORES-RECURRENTES.md (patrón, señal y qué hacer) con lo documentado en el repo: CI roja en main tras el merge porque la CI no tiene data/; la regla 5 de state check y el tag; el recorte de procesos por memoria de Claude Code; tests cuyo nombre promete algo que no comprueban; conversaciones del consultor sin traspaso.
>
> 5. Next Action: añade la línea «Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir». El umbral no lo escribes tú.
>
> Ritual normal con make check sellado, sin --no-verify. Pasa el revisor al terminar.
> «Rama lista para revisión, NO cerrada.»
