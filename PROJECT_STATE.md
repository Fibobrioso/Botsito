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
FASE 2 · Retroalimentacion del experto (F09-F10)

## Current Feature
F09 · expert-feedback-model

## Current Branch
feature/F09-expert-feedback-model

## Stable Main State
b6b82f2 · merge de F06. make check verde: 104 casos (92 funciones), 3 contratos, mypy strict, state/config/knowledge validate. CI Ubuntu verde. Tag stable/F06.

## Completed Phases
- FASE 0 · Fundamentos (F01, F02) · cerrada el 2026-09-04 en dc3384d · puerta: make check verde en main; registro de parametros con tipos y lectura estricta; .gitattributes y cero CRLF; hooks copiados por make sync; tags stable/F01 y stable/F02; CI Linux verde

## Completed Features
- F01 · project-scaffold · validada el 2026-09-04 · docs/validation/F01-project-scaffold.md · tag stable/F01
- F02 · config-and-parameter-registry · validada el 2026-09-04 · docs/validation/F02-config-and-parameter-registry.md · tag stable/F02
- F03 · corpus-inventory · validada el 2026-09-04 · docs/validation/F03-corpus-inventory.md · tag stable/F03
- F06 · evidence-model · validada el 2026-09-04 · docs/validation/F06-evidence-model.md · tag stable/F06

## Features Waiting for Validation
- F09 · expert-feedback-model · WAITING_FOR_USER_VALIDATION · informe: docs/validation/F09-expert-feedback-model.md

## Existing Components
- Paquete `botsito`: `domain/valores.py` (Fraccion, Porcentaje sobre Decimal, no intercambiables); `config/registro.py` (registro de parametros con procedencia y lectura estricta; vacio de valores); `config/ajustes.py` (entorno y rutas, sin claves de negocio).
- CLI: `state check` (rama, recuento de tests, tag estable, informes de validacion), `knowledge validate` (registro + manifiesto del corpus), `config validate` (ajustes contra el registro), `corpus inventory` y `corpus check`.
- `corpus/inventario.py`: manifiesto del corpus con SHA-256, ffprobe, papel y huecos de fotogramas heredados. `knowledge/corpus/{fuentes,manifest}.yaml`.
- `evidence/{modelo,contradicciones,historial}.py`: EvidenceItem inmutable (id con hash), contradicciones regeneradas, guardia de historial de git. CLI `evidence new` / `evidence contradictions`. Hook rechaza editar o borrar evidencia y feedback.
- `feedback/modelo.py`: FeedbackRecord solo-anadir (id por hash, coherencia accion/objetivo, trazabilidad); CLI `feedback new/trace/pending`; `commits_sin_fuente` exige trailer `Fuente:` en commits que tocan spec/cases desde stable/F06.
- Contratos de importacion (import-linter + test AST; `domain` no importa `config`). Test de literales de negocio con lista real. Tests de integridad del indice.
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- Plantillas: brief, ADR, informe de validacion. ADR-0001, 0002, 0003. `.gitattributes` con LF.

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- knowledge/evidence/README.md (esquema de EvidenceItem) · src/botsito/evidence/modelo.py
- knowledge/feedback/README.md (esquema de FeedbackRecord y plantilla de sesion) · src/botsito/feedback/modelo.py · src/botsito/evidence/historial.py
- knowledge/corpus/fuentes.yaml (fuentes esperadas, ids de Drive) · knowledge/corpus/manifest.yaml (GENERADO) · src/botsito/corpus/inventario.py
- knowledge/spec/parametros.yaml (LA puerta de los parametros; vacio hasta F11) · src/botsito/config/registro.py · src/botsito/domain/valores.py
- docs/plan/features/F02-config-and-parameter-registry.md · docs/validation/F02-config-and-parameter-registry.md
- docs/adr/0002-registro-de-parametros-una-sola-puerta.md · docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
- docs/plan/AUDITORIA_FASES_2026-09-04.html · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
106 funciones de test (parametrizadas x3, x11 y x14) · unit: project_state, adr, tree, cli, valores, registro, ajustes, inventario, evidence, feedback · contract: import_contracts, no_business_literals, repository_integrity, evidence_history, feedback_history · 3 contratos import-linter KEPT · mypy strict OK (src + tests)

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

## Lineamientos recibidos del usuario (pendientes de formalizar como evidencia/feedback)
Lo que el usuario (consultor) aporta por escrito sobre la operativa. NO es evidencia (no es cita del
corpus) ni feedback del trader: se convierte en items de evidencia en F07 cuando se re-cite sobre la
transcripcion nueva, y en reglas en F11. Hasta entonces vive aqui con su fecha y su mapeo.

- **2026-09-04 · Geometria del riesgo y gestion del stop.** "Se traza un 1:3 inicialmente; con eso
  se calcula el lotaje y todo. Una vez se mete la operativa, se baja el SL hasta el 0,75 del trade
  o hasta el 0,8; el TP sigue donde estaba inicialmente."
  - Estado en el plan: CONTEMPLADO. MASTER_PLAN F21 (caja 0/0,25/0,5/0,75/1, lotaje sobre la
    distancia completa, stop en 0,75 con colchon de spread, objetivo 1:3 sobre la distancia completa)
    y la investigacion (tres confirmaciones aritmeticas: ratio 4,08/3,94 = 3/0,75; Excel con -0,75).
  - Citas del corpus a re-citar en F07: V2 0:31:59-0:33:53 ("calculo mi lotaje desde aqui... luego
    apenas se da inicio la entrada lo pongo en 0,75... el objetivo sigue en 1:3"), V1 0:06:19-0:06:34
    ("no olvidarse de poner el cuadro de Gann en 0,75, proteger el trade apenas se genera la entrada"),
    V4 0:08:39-0:08:50 ("dar un pequeno respiro: de 0,75 a 0,80" por el spread).
  - Lectura: el 0,8 es el colchon de spread sobre el 0,75, no un nivel alternativo libre.
  - Preguntas abiertas para el trader (sesion 1): (a) ¿el 0,8 es fijo o "0,75 mas el spread del
    momento"? (b) ¿el stop se coloca en el 0,75 al enviar la orden limite o solo tras el llenado?
    Para el bot es equivalente y mas seguro adjuntar el SL al 0,75 en la propia orden pendiente
    (F22/F31); confirmar que el trader no ve inconveniente.
  - Consecuencia para F21: el TP nunca se recalcula al mover el SL (invariante a probar).

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
F09 · expert-feedback-model (`feature/F09-expert-feedback-model`)

## Next Action
Usuario valida F09 -> merge --no-ff a main -> tag stable/F09 -> push -> abrir feature/F15-market-data-ohlc (orden E: F15 antes de F04/F05 porque F10 y F14 necesitan datos reales).

## Last Stable Commit
b6b82f2 · merge: F06 evidence-model validado por el usuario · tag stable/F06

## Change Log
- 2026-09-04 · push F09; CI Ubuntu verde (run 33894611220); hook de feedback probado
- 2026-09-04 · F09 construida: FeedbackRecord solo-anadir, guardia de historial generalizada, trailer Fuente en commits de spec/cases, capas refinadas; 106 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F09-expert-feedback-model abierta; brief escrito (feedback apply diferido a F11 por falta de esquema de spec)
- 2026-09-04 · F06 VALIDADA por el usuario; merge --no-ff a main (b6b82f2); tag stable/F06
- 2026-09-04 · lineamiento del usuario registrado: SL a 0,75/0,8 tras la entrada con TP fijo (contemplado en F21; dos preguntas abiertas para el trader)
- 2026-09-04 · push F06 tras auditoria global; CI Ubuntu verde (run 33893230602)
- 2026-09-04 · auditoria global: la guardia de historial no detectaba ediciones dentro de un merge (ahora compara blobs con el primer commit); make check ejecuta knowledge validate; coma decimal normalizada en contradicciones; 92 funciones de test
- 2026-09-04 · push F06; CI Ubuntu verde (run 33892467496); hook de evidencia probado en 5 escenarios
- 2026-09-04 · F06 construida: modelo de evidencia inmutable, contradicciones regeneradas, guardia de historial, hook; 89 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F06-evidence-model abierta; brief escrito
- 2026-09-04 · F03 VALIDADA por el usuario; merge --no-ff a main (77fdd44); tag stable/F03
- 2026-09-04 · push F03 tras auditoria; CI Ubuntu verde con ffmpeg (run 33891193380)
- 2026-09-04 · auditoria de F03: orden POSIX del manifiesto (Windows ordenaba sin mayusculas), corpus check detecta ficheros no inventariados, esquema de ficheros validado, ffmpeg en CI, xlsx/pdf binarios; 76 funciones de test
- 2026-09-04 · push de la rama F03; CI Ubuntu verde (run 33890615366)
- 2026-09-04 · F03 construida: fuentes.yaml, inventario.py, manifest.yaml real (4 videos con hash y duracion, 477 heredados, 17 adicionales), corpus inventory/check; 74 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · corpus recibido en local (4 videos identicos a Drive, _procesado heredado, material adicional: 2 xlsx FXReplay + 15 capturas); movido a corpus/ (gitignored); ffmpeg 9 instalado; rama feature/F03-corpus-inventory abierta
- 2026-09-04 · F02 VALIDADA por el usuario; merge --no-ff a main (dc3384d); tag stable/F02; FASE 0 CERRADA
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
