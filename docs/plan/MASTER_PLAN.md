# Master Development Plan · Botsito

Version Markdown del plan (la version completa con detalle de cada funcionalidad esta en
`MASTER_PLAN.html`, mismo contenido). Deriva del informe de investigacion
`docs/research/2026-09-03-del-corpus-al-bot.html` y no redefine el metodo: lo convierte en
funcionalidades, ramas, tests y criterios de aceptacion.

## 0 · Principios

- Una funcionalidad = una rama `feature/F##-nombre` = un `FUNCTIONALITY VALIDATION REPORT` = un
  merge `--no-ff` tras validacion del usuario. `main` siempre estable, etiquetado `stable/F##`.
- Tres regimenes de contenido: evidencia inmutable; feedback del trader solo-anadir; especificacion
  y casos versionados citando evidencia o feedback.
- `domain/` puro (sin IO, reloj ni MetaTrader), impuesto por import-linter y test AST.
- Causalidad en tipos y tests; parametros congelados por argumento, nunca optimizados.
- Validacion de fidelidad (F26) antes de cualquier MQL5.
- Sesion nueva de IA: `PROJECT_STATE.md` → brief de la funcionalidad actual → sus ficheros.
- Cambios de arquitectura solo via ARCHITECTURE CHANGE PROPOSAL y ADR.

## B · Estructura del repositorio

| Ruta | Responsabilidad |
|---|---|
| `PROJECT_STATE.md` | memoria operativa |
| `docs/plan/` | este plan y `features/F##-*.md` (briefs) |
| `docs/adr/` | decisiones con estado ACTIVE / SUPERSEDED |
| `docs/validation/` | informes de validacion por rama, informes de fidelidad |
| `docs/spec/` | especificacion legible GENERADA (F13) |
| `docs/runbooks/` | operacion demo/real (F33) |
| `knowledge/corpus` | manifiesto con hash y huecos (F03) |
| `knowledge/evidence` | `EvidenceItem` inmutables (F06) |
| `knowledge/feedback` | `FeedbackRecord` solo-anadir (F09) |
| `knowledge/spec` | `strategy_spec.yaml`, glosario (F11) |
| `knowledge/cases/{dev,holdout,fixtures}` | casos ejecutables; holdout ilegible para spec/domain (F14) |
| `src/botsito/{corpus,evidence,feedback,spec,cases,data,domain,engine,validation,viewer,mql5bridge}` | paquete Python; ver docstring de cada subpaquete |
| `mql5/` | EA, includes (Params.mqh generado), RunCases, tester (fase 6) |
| `tests/{unit,contract,integration,golden,regression,differential}` | por capa de validacion |
| `scripts/`, `config/` | operaciones puntuales; settings sin secretos |
| `corpus/`, `data/` | gitignored; solo manifiestos con hash entran en git |

## A · Fases y funcionalidades

| Id | Rama | Objetivo | Depende de | Pruebas clave | Aceptacion |
|---|---|---|---|---|---|
| **Fase 0 · Fundamentos** | | | | | |
| F01 | `feature/F01-project-scaffold` | Andamiaje y contratos | — | docs, import-linter | CI verde; PROJECT_STATE completo |
| F02 | `feature/F02-config-and-parameter-registry` | Parametros con procedencia | F01 | sin fuente = error | una sola puerta por parametro |
| **Fase 1 · Base de conocimiento** | | | | | |
| F03 | `feature/F03-corpus-inventory` | Manifiesto con hash y huecos | F01 | huecos sinteticos | manifiesto determinista |
| F04 | `feature/F04-transcription-pipeline` | Transcripcion alineada (large-v3) | F03 | desfases; clip fixture | 50 citas conservan sentido |
| F05 | `feature/F05-frame-extraction` | Fotogramas densos en tramos con decision | F03 | integridad del indice | sin huecos > 2 s |
| F06 | `feature/F06-evidence-model` | Evidencia inmutable | F03 | inmutabilidad; contradiccion | sin cita = rechazado |
| F07 | `feature/F07-evidence-extraction` | Poblar evidencia (humano; LLM propone) | F04, F05, F06 | esquema LLM; golden | 100 % citas verificadas |
| F08 | `feature/F08-evidence-retrieval` | Busqueda por texto y tiempo | F07 | indice; fuentes | toda respuesta con fuente |
| **Fase 2 · Feedback del experto** | | | | | |
| F09 | `feature/F09-expert-feedback-model` | Feedback solo-anadir con procedencia | F06 | solo-anadir; trazabilidad | cambio de spec sin id = error |
| F10 | `feature/F10-elicitation-kit` | Preguntas desde UNKNOWN; etiquetado ciego; kappa | F09 (F15) | kappa; determinismo | paquete reproducible |
| **Fase 3 · Formalizacion** | | | | | |
| F11 | `feature/F11-strategy-spec-schema` | StrategySpec (reglas, parametros, ambiguedades, tablas, statecharts) | F02, F07, F09 | referencias; estados | carga estricta |
| F12 | `feature/F12-spec-semantic-validator` | Validacion semantica | F11 | por comprobacion | falla nombrando el id |
| F13 | `feature/F13-spec-documents` | Docs y hoja del trader generados | F11 | anti-deriva | docs = generado |
| F14 | `feature/F14-case-library` | Casos ejecutables con holdout | F09, F11, F15 | guarda de holdout | runner independiente |
| **Fase 4 · Datos** | | | | | |
| F15 | `feature/F15-market-data-ohlc` | OHLC y agregacion con anclaje y huso | F02 | DST; anclaje; golden | H4 = las del trader |
| F16 | `feature/F16-market-data-ticks` | Ticks a Parquet con calidad | F15 | comprobaciones | M1 desde ticks coincide |
| F17 | `feature/F17-demo-tick-recorder` | Grabar ticks y spread de la demo | F16 | rotacion | perfil de spread |
| **Fase 5 · Motor y fidelidad** | | | | | |
| F18 | `feature/F18-domain-types-and-h4-bias` | Tipos y sesgo H4 | F11, F14 | golden; lint | casos de sesgo verdes |
| F19 | `feature/F19-domain-m15-zones` | Zonas M15 y mitigacion | F18 | causalidad | truncado = completo |
| F20 | `feature/F20-domain-m1-breaker-and-control-zones` | Mapeo M1, breaker, zonas de control | F19 | causalidad; negativos | casos de entrada verdes |
| F21 | `feature/F21-domain-risk-geometry` | Caja, stop 0,75, lotaje, 1:3, BE | F18 | golden 4,08 / 3,94 | stop = −0,75 R |
| F22 | `feature/F22-domain-state-machines` | Statecharts jornada y ciclo (Decider) | F20, F21 | property | invariantes probadas |
| F23 | `feature/F23-engine-event-loop` | Bucle, reloj determinista, journal | F22 | determinismo | mismo sha256 |
| F24 | `feature/F24-engine-tick-backtest` | Simulacion sobre ticks | F16, F23 | llenado; golden | llenado defendible |
| F25 | `feature/F25-viewer` | Visor de tres marcos | F24 | igualdad con journal | dibuja lo que hay en memoria |
| F26 | `feature/F26-fidelity-validator` | Fidelidad contra el trader (holdout) | F10, F14, F24 | comparador; holdout | informe reproducible |
| F27 | `feature/F27-sensitivity-and-edge-report` | Sensibilidad y ventaja (DSR, N declarado) | F24, F26 | DSR | N declarado |
| **Fase 6 · MQL5 y diferencial** | | | | | |
| F28 | `feature/F28-mql5-spec-export` | Params.mqh y fixtures generados | F11, F14 | roundtrip | regenerar sin diff |
| F29 | `feature/F29-mql5-domain` | Dominio en MQL5 | F28 | compilacion | RunCases produce CSV |
| F30 | `feature/F30-differential-testing` | Harness Python ↔ MQL5 | F29, F26 | harness | 100 % decisiones iguales |
| F31 | `feature/F31-mql5-expert-advisor` | EA, ordenes idempotentes, veto de riesgo, journal | F29, F30 | retcodes | nunca duplica |
| F32 | `feature/F32-strategy-tester-parity` | Paridad con Strategy Tester (ticks reales) | F24, F31 | comparacion | > 95 % operaciones |
| **Fase 7 · Demo y sombra** | | | | | |
| F33 | `feature/F33-demo-deployment` | Demo, pre-vuelo, runbooks | F17, F31 | pre-vuelo | aborta si no cuadra |
| F34 | `feature/F34-shadow-reconciliation` | Reconciliacion diaria demo ↔ backtest | F32, F33 | triage | 3 meses en umbral |
| F35 | `feature/F35-go-live-gate` | Memorando de decision | F27, F34 | reproducibilidad | decision humana |

## D · Grafo de dependencias

```
F01 ── F02 ── F15 ── F16 ── F17
 └── F03 ── F04 ─┐
      ├── F05 ───┼── F07 ── F08
      └── F06 ───┘   │
           └── F09 ──┴── F11 ── F12 / F13 / F14
                └── F10 (usa F15)
F11 + F14 ── F18 ── F19 ── F20 ─┐
               └── F21 ─────────┴── F22 ── F23 ── F24 ── F25
                                                    ├── F26 ── F27
F11 + F14 ── F28 ── F29 ── F30 (◄ F26) ── F31 ── F32 (◄ F24)
                                            F17 ── F33 ── F34 ── F35 (◄ F27)
```

## E · Orden de desarrollo

F01, F02 → F03, F06, F09 → F15 → F04, F05, F07, F08 → F10 + sesion 1 con el trader → F11–F14 →
F16, F17 → F18–F22 → F23–F25 → F26 + sesion 2 (punto de decision: reglas solas o respaldo) → F27 →
F28–F32 → F33–F35.

## F · Validacion (13 capas acumulativas)

Estructura de documentos → esquema de knowledge → regimenes de cambio → semantica de la spec →
causalidad → invariantes → casos dorados → determinismo → fidelidad en holdout → diferencial
Python/MQL5 → paridad con tester → paridad en vivo → validacion humana (usuario y trader).

Ritual de cierre de rama: `make regress` → informe en `docs/validation/F##.md` con estado
`WAITING_FOR_USER_VALIDATION` → parada → tras validacion: re-ejecucion, docs, commits, merge
`--no-ff`, tests desde `main`, etiqueta `stable/F##`, `PROJECT_STATE.md`.

## G · Bucle del experto

| Cuando | Que valida | Objeto que crea | Que modifica (via diff propuesto) |
|---|---|---|---|
| Sesion 1 (tras F10 + F15) | 3 preguntas bloqueantes sobre casos; ronda 1 de etiquetado; hoja de reglas | FeedbackRecord | spec (F11), casos dev/holdout |
| Sesion 2 (tras F26) | discrepancias en el visor; FP/FN; fronterizos; ronda 2 (kappa) | FeedbackRecord | reglas, tablas de decision, casos; posible ACP de respaldo |
| Sesion 3 (tras F32) | divergencias de ejecucion | FeedbackRecord | reglas de ejecucion |
| Mensual (F34) | discrepancias en vivo | FeedbackRecord | igual |

Invariantes: la evidencia nunca cambia; toda etiqueta tiene autor y fecha; decision del sistema y del
experto se guardan como hechos distintos; un UNKNOWN se cierra solo con registro del trader o
grabacion en vivo.
