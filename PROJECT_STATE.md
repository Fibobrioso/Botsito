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
F02 · config-and-parameter-registry

## Current Branch
feature/F02-config-and-parameter-registry

## Stable Main State
85cedc4 · merge de F01 (project-scaffold). make check verde: 26 tests, 3 contratos, mypy strict, state check. CI Ubuntu verde. Tag stable/F01.

## Completed Phases
—

## Completed Features
- F01 · project-scaffold · validada por el usuario el 2026-09-04 · docs/validation/F01-project-scaffold.md · tag stable/F01

## Features Waiting for Validation
- F02 · config-and-parameter-registry · WAITING_FOR_USER_VALIDATION · informe: docs/validation/F02-config-and-parameter-registry.md

## Existing Components
- Paquete `botsito`: `domain/valores.py` (Fraccion, Porcentaje sobre Decimal, no intercambiables); `config/registro.py` (registro de parametros con procedencia y lectura estricta; vacio de valores); `config/ajustes.py` (entorno y rutas, sin claves de negocio).
- CLI: `state check` (rama, recuento de tests, tag estable, informes de validacion), `knowledge validate` (registro) y `config validate` (ajustes contra el registro).
- Contratos de importacion (import-linter + test AST; `domain` no importa `config`). Test de literales de negocio con lista real. Tests de integridad del indice.
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- Plantillas: brief, ADR, informe de validacion. ADR-0001, 0002, 0003. `.gitattributes` con LF.

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- knowledge/spec/parametros.yaml (LA puerta de los parametros; vacio hasta F11) · src/botsito/config/registro.py · src/botsito/domain/valores.py
- docs/plan/features/F02-config-and-parameter-registry.md · docs/validation/F02-config-and-parameter-registry.md
- docs/adr/0002-registro-de-parametros-una-sola-puerta.md · docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
- docs/plan/AUDITORIA_FASES_2026-09-04.html · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
65 funciones de test (65 casos de pytest: una parametrizada x3) · unit: project_state, adr, tree, cli, valores, registro, ajustes · contract: import_contracts, no_business_literals, repository_integrity · 3 contratos import-linter KEPT · mypy strict OK (src + tests)

## Architectural Decisions (index)
- ADR-0001 estructura del repositorio y regimenes de cambio — ACTIVE
- ADR-0002 registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta — ACTIVE
- ADR-0003 hooks copiados desde scripts/git-hooks; sin framework pre-commit — ACTIVE

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
Usuario valida F02 -> make check -> merge --no-ff a main (BOTSITO_ALLOW_MAIN=1) -> tests desde main -> tag stable/F02 sobre el merge -> push -> cerrar FASE 0 (puerta) -> abrir feature/F03-corpus-inventory.

## Last Stable Commit
85cedc4 · merge: F01 project-scaffold validado por el usuario · tag stable/F01

## Change Log
- 2026-09-04 · segunda auditoria de F02: explicit-preview-rules; botsito config validate en make check; 65 funciones / 67 casos
- 2026-09-04 · auditoria de F02: prefijo duplicado en errores, limites con float, accesores tipados, property YAML; 63 funciones / 65 casos
- 2026-09-04 · push de la rama F02; CI Ubuntu verde (run 33883045053)
- 2026-09-04 · F02 construida: valores.py, registro.py, ajustes.py, parametros.yaml vacio, state check ampliado, test de literales real, ADR-0002/0003, sin .pre-commit-config; 59 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F02-config-and-parameter-registry abierta; brief escrito
- 2026-09-04 · F01 VALIDADA por el usuario; merge --no-ff a main (85cedc4); tag stable/F01; push de main
- 2026-09-03 · repositorio inicializado en local · punto cero con documentacion · plan pendiente de validacion
- 2026-09-03 · plan aprobado por el usuario · rama feature/F01-project-scaffold abierta · paquete botsito
- 2026-09-03 · F01 construida; make check verde (21 tests, 3 contratos); WAITING_FOR_USER_VALIDATION
- 2026-09-04 · auditoria de fases (docs/plan/AUDITORIA_FASES_2026-09-04.html): 4 criticos, 19 huecos; plan ampliado (MASTER_PLAN.md seccion H)
- 2026-09-04 · F01 corregida: .gitattributes, tests de integridad del indice, hook anti-main, uv --locked; 26 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · push de la rama F01 autorizado; CI Ubuntu verde (run 33880866257). Linux verificado
- 2026-09-04 · pruebas cruzadas: clon limpio, autocrlf=true, HEAD separado, PowerShell 7, Python 3.13 verdes; Linux pendiente del primer push. HALLAZGO: core.hooksPath relativo omitia el hook en main (sin el fichero); make hooks ahora copia a .git/hooks. Reprobado OK
- 2026-09-04 · tercera auditoria: hook con modo 100755 en el indice, READMEs en todas las carpetas (sin exenciones), holdout/{1,2,3} fisico, mypy strict sobre tests
- 2026-09-04 · segunda auditoria: Last Stable Commit corregido (era 0b43244, main esta en 7baa27d), Next Feature = F02, brief de F01 y README actualizados
