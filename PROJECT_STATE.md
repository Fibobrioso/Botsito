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
tras validación del usuario. `main` siempre estable y etiquetado `stable/F##`. Trabajo local; push solo
cuando el usuario lo pide.

## How to Start a Session
1. Leer este fichero. 2. Leer `docs/plan/features/<Current Feature>.md`. 3. `make check` (desde F01).
4. Si `Current Feature` está WAITING_FOR_USER_VALIDATION: no avanzar; preguntar.

## Change Regimes (must be respected)
- knowledge/evidence/  → INMUTABLE tras commit (hook). Corrección = nuevo item que supersede.
- knowledge/feedback/  → SOLO AÑADIR. Nunca editar un registro.
- knowledge/spec/, knowledge/cases/ → versionados; cada cambio de valor cita evidence-id o feedback-id.
- knowledge/cases/holdout/ → prohibido leer desde src/<paquete>/spec y src/<paquete>/domain (guarda en tests).
- src/<paquete>/domain/ → sin IO, sin reloj, sin MetaTrader (import-linter).

## Current Phase
FASE 0 · Fundamentos

## Current Feature
— (plan publicado, pendiente de validación del usuario; F01 no abierta)

## Current Branch
main

## Stable Main State
Punto cero: documentación (README, PROJECT_STATE, plan, investigación). Sin código.

## Completed Phases
—

## Completed Features
—

## Features Waiting for Validation
- Master Development Plan (docs/plan/MASTER_PLAN.html) · WAITING_FOR_USER_VALIDATION

## Existing Components
—

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.html · docs/research/2026-09-03-del-corpus-al-bot.html

## Tests Currently Passing
—

## Architectural Decisions (index)
- (ADR-0001 estructura del repositorio y regímenes de cambio se redacta en F01)

## Decisions and Rationale
Formato obligatorio por decisión:
Decisión: · Problema que resuelve: · Alternativas consideradas: · Por qué elegimos esta opción: ·
Por qué descartamos las demás: · Impacto: · Fecha / fase: · Estado: ACTIVE / SUPERSEDED

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
- Nombre del paquete Python (`botsito` propuesto) — decidir antes del merge de F01.
- Fuente de ticks históricos — decidir en F16.
- Ruta local de trabajo — actual: C:\Users\USER\Desktop\Bot v3.

## Things That Must Not Be Changed
- Regímenes de cambio de knowledge/. · Pureza de domain/. · Parámetros no se optimizan contra resultados.
- La validación de fidelidad (F26) precede a cualquier MQL5.

## Next Feature
F01 · project-scaffold (`feature/F01-project-scaffold`)

## Next Action
Usuario valida el Master Development Plan → abrir rama F01 → implementar según docs/plan/features/F01 → VALIDATION REPORT → parar.

## Last Stable Commit
(se rellena tras el primer commit)

## Change Log
- 2026-09-03 · repositorio inicializado en local · punto cero con documentación · plan pendiente de validación
