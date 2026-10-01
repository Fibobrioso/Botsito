# Encargo · trabajo/guardias-claude

Copiado tal cual, al crear la rama el 2026-10-01, del prompt de Aleks que la origina. Es la vara
con la que el revisor (`.claude/agents/revisor.md`, eje b) mide lo hecho.

---

Modelo: Opus · Esfuerzo: alto

Rama nueva: trabajo/guardias-claude, desde main (41c9ed9).
Objetivo: que las reglas de CLAUDE.md que hoy son solo texto tengan un mecanismo que las haga cumplir. Hoy el repo no tiene carpeta .claude/: ni hooks de Claude Code, ni subagentes, ni permisos. No cambia motor, spec, knowledge ni ninguna cifra.

Fase 0 · Inventario (sin tocar nada)
Lista cada regla de CLAUDE.md, RITUAL.md y docs/runbooks que prohíba algo («nunca», «no se», «prohibido», «solo») y di qué la hace cumplir hoy: un test, un git hook, make check, la CI o nada. Las que tienen «nada» son el alcance de esta rama. Entrega la tabla antes de escribir código.

Fase 1 · .claude/settings.json: hooks y permisos
- Hook PreToolUse en Python (Windows, PYTHONUTF8, sin dependencias nuevas) para Read, Grep, Glob y Bash:
  - bloquea leer el CONTENIDO de material de meses reservados o sin sortear: libros xlsx, imágenes, transcripciones y casos que marquen casos_reservados, casos_ocultos o los registros de entrada sin abrir (marzo);
  - permite solo stat, tamaño, sha256 y `botsito corpus inventory`;
  - si no puede decidir con seguridad sobre un comando Bash (por ejemplo, rutas construidas en tiempo de ejecución), lo BLOQUEA y explica cómo reescribirlo;
  - el mensaje de bloqueo cita la regla de CLAUDE.md.
- Denegaciones en permisos: git commit o push con --no-verify, push --force, borrar tags, `git push origin main` sin BOTSITO_ALLOW_MAIN y `rm -rf` sobre data/, corpus/ o knowledge/.
- .claude/settings.local.json va en .gitignore; settings.json se versiona.
- Si algo de esto bloquearía lo que hoy hacen make check, la CI o el ritual, dilo y no lo actives.
- Es defensa en profundidad: las comprobaciones en código (casos_reservados, la compuerta del arnés) siguen siendo la barrera principal y no se tocan.

Fase 2 · Contrato por rama
- Formato: contrato.yaml en la raíz de cada rama de trabajo, con rutas_permitidas, rutas_protegidas, comprobaciones (comandos obligatorios), riesgo (bajo, medio o alto) y artefacto (el informe esperado en docs/validation/).
- make check: si existe contrato.yaml, compara el diff contra el merge-base con main; falla nombrando cada fichero fuera de rutas_permitidas o dentro de rutas_protegidas, y si falta el artefacto. En main el contrato se borra en el merge y no se exige.
- Plantilla en docs/runbooks/CONTRATO-DE-RAMA.md con tres ejemplos: rama de solo knowledge, rama de motor y rama de medición.
- Escribe el contrato de esta propia rama como primer ejemplo.

Fase 3 · Subagente revisor
- .claude/agents/revisor.md, con herramientas de solo lectura (Read, Grep, Glob y Bash sin escritura). Revisa una rama antes del «Rama lista para revisión», en dos ejes independientes, cada uno con su propio informe y sin mezclarlos:
  (a) reglas de la casa: CLAUDE.md, trailers Fuente: con ids que existen, holdout, régimen de cambio (CORRECT frente a RESOLVE), ADR con Estado válido, contrato de la rama y recuadros de corrección en informes cerrados;
  (b) encargo: lo hecho frente al prompt que originó la rama, guardado en docs/encargos/<rama>.md (Claude Code copia ahí el prompt al crear la rama).
- Cada hallazgo lleva su evidencia (fichero y línea, o comando y salida) y una gravedad: bloquea, importa o menor. No arregla nada.
- Línea nueva en CLAUDE.md: «Antes de declarar una rama lista para revisión: guarda el encargo en docs/encargos/, pasa el revisor y pega su informe al final del informe de la rama».
- Métrica en docs/runbooks/ERRORES-RECURRENTES.md: por rama, cuántos hallazgos encontró el revisor y cuántos encontró después el consultor. El segundo número debe tender a cero.

Fase 4 · Tests
- El hook bloquea una lectura de material reservado, deja pasar un sha256 y bloquea un comando Bash indecidible.
- El contrato falla con un diff fuera de las rutas permitidas y pasa con uno dentro.
- El revisor existe, su frontmatter es válido y no tiene herramientas de escritura.

Guarda este mismo prompt como docs/encargos/trabajo-guardias-claude.md al empezar.
Ritual normal con make check sellado, sin --no-verify. Al terminar, pasa el revisor sobre esta misma rama y pega su informe.
«Rama lista para revisión, NO cerrada.»
