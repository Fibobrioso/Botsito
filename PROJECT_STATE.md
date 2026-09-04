# PROJECT STATE

> Memoria operativa. Una sesión nueva lee este fichero, luego `docs/plan/features/<Current Feature>.md`,
> luego los ficheros de esa funcionalidad. Nada más salvo razón técnica registrada aquí.

## Project Goal
Bot fiel a la estrategia de un trader concreto (EURUSD, H4→M15→M1), verificable caso a caso contra sus
decisiones, ejecutable en MetaTrader 5 (FundedNext), sin IA en ejecución. Fidelidad y rentabilidad se
miden por separado.

## Approved Architecture
Evidencia inmutable del corpus → elicitación con el trader (feedback solo-añadir) → StrategySpec ejecutable
+ biblioteca de casos → motor de referencia Python (núcleo puro, backtest sobre ticks, visor) → validación
de fidelidad → EA MQL5 (misma spec) → pruebas diferenciales → paridad con Strategy Tester → demo/sombra.
Referencia: `docs/plan/MASTER_PLAN.html` · `docs/research/2026-09-03-del-corpus-al-bot.html`.

## Development Strategy
Una funcionalidad = una rama `feature/F##-nombre` = un FUNCTIONALITY VALIDATION REPORT = un merge --no-ff
tras validación del usuario. `main` siempre estable y etiquetado `stable/F##`. Push autorizado por el usuario el 2026-09-04; `main` solo recibe merges validados.

## How to Start a Session
1. Leer este fichero. 2. Leer `docs/plan/features/<Current Feature>.md`. 3. `make check` (desde F01).
4. Si `Current Feature` está WAITING_FOR_USER_VALIDATION: no avanzar; preguntar.

## Change Regimes (must be respected)
- knowledge/evidence/  → INMUTABLE tras commit (hook). Corrección = nuevo item que supersede.
- knowledge/feedback/  → SOLO AÑADIR. Nunca editar un registro.
- knowledge/spec/, knowledge/cases/ → versionados; cada cambio de valor cita evidence-id o feedback-id.
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; prohibido leer desde src/botsito/spec y src/botsito/domain (guarda en tests); cada una se abre una sola vez.
- src/botsito/domain/ → sin IO, sin reloj, sin MetaTrader (import-linter).

## Current Phase
FASE 0 · Fundamentos

## Current Feature
F01 · project-scaffold

## Current Branch
feature/F01-project-scaffold

## Stable Main State
Punto cero: documentación (README, PROJECT_STATE, plan, investigación). Sin código.

## Completed Phases
—

## Completed Features
—

## Features Waiting for Validation
- F01 · project-scaffold · WAITING_FOR_USER_VALIDATION · informe: docs/validation/F01-project-scaffold.md

## Existing Components
- Paquete `botsito` con subpaquetes vacios documentados; CLI `state check` y `knowledge validate` (no-op).
- Contratos de importacion (import-linter + test AST). Tests de integridad del indice (tracked, CRLF, ignorados, gitignore anclado).
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- Plantillas: brief, ADR, informe de validacion. ADR-0001. `.gitattributes` con LF.

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- docs/plan/AUDITORIA_FASES_2026-09-04.html · docs/plan/features/F01-project-scaffold.md · docs/validation/F01-project-scaffold.md
- docs/adr/0001-repository-structure-and-change-regimes.md · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
26 (unit: project_state, adr, tree, cli · contract: import_contracts, no_business_literals, repository_integrity) · 3 contratos import-linter KEPT · mypy strict OK

## Architectural Decisions (index)
- ADR-0001 estructura del repositorio y regimenes de cambio — ACTIVE

## Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.

## Expert Entry Points
- Sesión 1 (tras F10+F15): 3 preguntas bloqueantes + ronda 1 de etiquetado · pendiente
- Sesión 2 (tras F26): discrepancias + ronda 2 (κ) · pendiente
- Sesión 3 (tras F32): divergencias de ejecución · pendiente
- Mensual (F34): discrepancias en vivo · pendiente

## Expert Validations
—

## Known Ambiguities
A-1 sesgo H4 · A-3 salida sin ruptura · A-4 BE al tocar/cierre · A-5 cadencia de reubicación ·
A-6 cierre 15:00 · tercer cartucho · stop del 2.º esquema · "dos velas como una" en mapeo
(todas: ABIERTA hasta registro de feedback del trader)

## Known Contradictions
Cartuchos 2 (ficha) vs 3 (V4 0:48:41) · parciales 30–40 % (ficha) vs "sin parciales" (respuesta) ·
BE al tocar vs al cierre (V4 0:44:56) · salida anticipada sí/no (V4 1:08:18 / 1:08:30)

## Known Issues
—

## Technical Debt
- Transcripciones previas con Whisper tiny: no usar para extracción hasta F04.
- MASTER_PLAN existe en HTML; la versión Markdown se genera en F01.

## Open Questions
- Nombre del paquete `botsito`: confirmar antes del merge de F01.
- Fuente de ticks historicos: decidir en F16.
- Ruta local de trabajo: C:/Users/USER/Desktop/Bot v3.

## Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado.
- Ficheros de texto siempre con LF y UTF-8 (escribir con newline="
").

## Next Feature
F02 · config-and-parameter-registry (`feature/F02-config-and-parameter-registry`)

## Next Action
Usuario valida F01 (con correcciones de la auditoria) -> re-ejecutar make check -> merge --no-ff a main con BOTSITO_ALLOW_MAIN=1 -> tests desde main -> tag stable/F01 -> abrir feature/F02-config-and-parameter-registry.

## Last Stable Commit
7baa27d · docs(state): registra el commit del punto cero (main)

## Change Log
- 2026-09-03 · repositorio inicializado en local · punto cero con documentacion · plan pendiente de validacion
- 2026-09-03 · plan aprobado por el usuario · rama feature/F01-project-scaffold abierta · paquete botsito
- 2026-09-03 · F01 construida; make check verde (21 tests, 3 contratos); WAITING_FOR_USER_VALIDATION
- 2026-09-04 · auditoria de fases (docs/plan/AUDITORIA_FASES_2026-09-04.html): 4 criticos, 19 huecos; plan ampliado (MASTER_PLAN.md seccion H)
- 2026-09-04 · F01 corregida: .gitattributes, tests de integridad del indice, hook anti-main, uv --locked; 26 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · push de la rama F01 autorizado; CI Ubuntu verde (run 33880866257). Linux verificado
- 2026-09-04 · pruebas cruzadas: clon limpio, autocrlf=true, HEAD separado, PowerShell 7, Python 3.13 verdes; Linux pendiente del primer push. HALLAZGO: core.hooksPath relativo omitia el hook en main (sin el fichero); make hooks ahora copia a .git/hooks. Reprobado OK
- 2026-09-04 · tercera auditoria: hook con modo 100755 en el indice, READMEs en todas las carpetas (sin exenciones), holdout/{1,2,3} fisico, mypy strict sobre tests
- 2026-09-04 · segunda auditoria: Last Stable Commit corregido (era 0b43244, main esta en 7baa27d), Next Feature = F02, brief de F01 y README actualizados
