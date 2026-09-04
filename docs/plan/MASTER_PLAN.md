# Master Development Plan · Botsito

Version Markdown del plan (la version completa con detalle de cada funcionalidad esta en
`MASTER_PLAN.html`, mismo contenido). Deriva del informe de investigacion
`docs/research/2026-09-03-del-corpus-al-bot.html` y no redefine el metodo: lo convierte en
funcionalidades, ramas, tests y criterios de aceptacion.

Las letras de las secciones (0, B, A, D, E, F, G, H) siguen la numeracion del HTML original para
que las citas cruzadas (`seccion H`, `orden E`) valgan en ambos; no hay seccion C.

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
| `knowledge/spec` | `parametros.yaml` (F02, ADR-0002/0004), `strategy_spec.yaml`, glosario (F11) |
| `knowledge/cases/{dev,holdout/1,holdout/2,holdout/3,fixtures}` | casos ejecutables; tres particiones reservadas ilegibles para spec/domain (F14) |
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
| F14 | `feature/F14-case-library` | Casos ejecutables con tres particiones reservadas (holdout-1/2/3) | F09, F11, F15 | guarda de holdout por audit hook | runner independiente |
| **Fase 4 · Datos** | | | | | |
| F15 | `feature/F15-market-data-ohlc` | OHLC y agregacion con anclaje y huso | F02 | DST; anclaje; golden | H4 reproducible para cualquier `anclaje_h4`; golden del trader en F07 |
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
| F26 | `feature/F26-fidelity-validator` | Fidelidad contra el trader (holdout-1; umbrales pre-registrados) | F10, F14, F24 | comparador; holdout; pre-registro | informe reproducible que cita PREREGISTRO.md |
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

Grafo simplificado: la tabla A es la fuente de las dependencias. No se dibujan, por legibilidad,
F15 → F14 (fixtures OHLC), F10 → F26 y F14 → F26 (validacion de fidelidad).

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

Ritual de cierre de rama: `make regress` → informe en `docs/validation/F##-nombre.md` con estado
`WAITING_FOR_USER_VALIDATION` → parada → tras validacion: re-ejecucion, docs, commits, merge
`--no-ff`, tests desde `main`, etiqueta `stable/F##`, `PROJECT_STATE.md`.

## G · Bucle del experto

| Cuando | Que valida | Objeto que crea | Que modifica (via diff propuesto) |
|---|---|---|---|
| Sesion 1 (tras F10 + F15) | 3 preguntas bloqueantes sobre casos (se eligen en el brief de F10 entre A-1..A-11 por impacto en el kit de casos; ver mapeo en `PROJECT_STATE.md`, Known Ambiguities); ronda 1 de etiquetado; hoja de reglas | FeedbackRecord | spec (F11), casos dev/holdout |
| Sesion 2 (tras F26) | discrepancias en el visor; FP/FN; fronterizos; ronda 2 (kappa) | FeedbackRecord | reglas, tablas de decision, casos; posible ACP de respaldo |
| Sesion 3 (tras F32) | divergencias de ejecucion | FeedbackRecord | reglas de ejecucion |
| Mensual (F34) | discrepancias en vivo | FeedbackRecord | igual |

Invariantes: la evidencia nunca cambia; toda etiqueta tiene autor y fecha; decision del sistema y del
experto se guardan como hechos distintos; un UNKNOWN se cierra solo con registro del trader o
grabacion en vivo.

## H · Salvaguardas anadidas por la auditoria de fases (2026-09-04)

Fuente: `docs/plan/AUDITORIA_FASES_2026-09-04.html` (instantanea). Aprobadas por el usuario. Cada
una se incorpora al brief de la funcionalidad indicada cuando se abra.

| Salvaguarda | Funcionalidades | Que impide |
|---|---|---|
| Tres particiones reservadas: `holdout-1` (se abre en F26, sesion 2), `holdout-2` (cifra final de fidelidad, una sola apertura), `holdout-3` (correcciones de fase 7). La asignacion se commitea con seed ANTES de la sesion de etiquetado; un test comprueba la fecha del commit | F10, F14, F26, F34, F35 | Medir la fidelidad final sobre casos ya vistos al corregir |
| Pre-registro: `docs/validation/PREREGISTRO.md` con umbrales de fidelidad, kappa, paridad y DSR, commiteado antes de abrir cualquier holdout; los informes citan su hash | F26, F27, F32, F35 | Ajustar el umbral a la cifra |
| Test en CI contra el historial de git: cada fichero de `knowledge/evidence/`, `knowledge/feedback/`, etiquetas de casos y manifiestos de datos es byte-identico a su primera version commiteada | F06, F09, F14, F15 | Editar evidencia o feedback saltando los hooks |
| Prohibicion de inferencias en `evidence/` (cita literal obligatoria; la afirmacion no anade condiciones); todo lo importado de Bot v2 se re-cita sobre la transcripcion large-v3 o entra como UNKNOWN; los defaults del ADR-0015 de Bot v2 (no existe en este repositorio) entran como ambiguedades abiertas | F06, F07 | Arrancar la base de conocimiento contaminada |
| Propuestas de LLM en `knowledge/_proposals/` con prompt, modelo, salida y decision humana; `extractor` y `reviewed_by` obligatorios en evidencia | F07 | Perder el rastro de que propuso la IA |
| Transcripciones en dos capas: cruda del ASR (inmutable) y corregida solo por sustituciones del glosario; test `cruda + glosario = corregida`; nombradas por modelo | F04 | Reescribir lo que dijo el trader |
| Modelo de llenado como parametro declarado; informe de ventaja con dos modelos (al tocar / cruce + latencia) | F24, F27 | Un modelo optimista que infla resultados |
| Contador automatico y versionado de N (ejecuciones de backtest) para el Deflated Sharpe | F24, F27 | N declarado incompleto |
| Regla: toda divergencia Python/MQL5 se resuelve citando la spec; si la spec no decide, es una ambiguedad nueva | F30 | Parches que alinean implementaciones sin fuente |
| `spec_version` y hash en journal, informes y `Params.mqh`; pre-vuelo de la demo compara el hash con el tag `stable/*` vigente | F11, F28, F33 | Operar con una spec distinta de la validada |
| Parametros con tipos `Porcentaje` y `Fraccion` no intercambiables, valores `Decimal`; leer un parametro `UNKNOWN` falla siempre; `settings.toml` no puede contener claves del registro | F02 | Error de factor 100 y dobles puertas |
| `state check` ampliado: recuento real de tests, tag estable, informe de validacion por funcionalidad completada | F02 | PROJECT_STATE que miente |
| Manifiestos de datos inmutables con `dataset_id`, proveedor, fecha, `schema_version`; escritura atomica en el grabador de demo; desfase servidor-UTC registrado | F15, F16, F17 | Re-descargas que cambian datos congelados; ficheros truncados |
| MQL5: enteros de puntos en el dominio; verificacion de `ACCOUNT_MARGIN_MODE` al arrancar; journal con flush y hash encadenado; veto de riesgo con parametros propios | F29, F31 | Discrepancias por redondeo; posicion duplicada; journal truncado |

### Puertas de fase

Cada fase termina con su lista de comprobacion (en la auditoria) verificada y registrada en
`PROJECT_STATE.md` bajo "Completed Phases" con fecha y commit. La puerta es por dependencia
(seccion D) y por el orden E, no por numero de fase: F06, F09 y F15 se abren con la fase 1 sin
cerrar porque no dependen de F04/F05/F07/F08, y F10 (sesion 1) exige la fase 1 cerrada. Ninguna
funcionalidad se abre con una dependencia de D sin validar. (Reescrito en la auditoria extrema del
2026-09-04: la redaccion anterior contradecia el orden E.)

### Trailer de commit

Todo commit que toque `knowledge/spec/` o `knowledge/cases/` lleva un trailer `Fuente: <ids>` con
ids de evidencia (`ev-…`), feedback (`fb-…`) o decision (`ADR-NNNN`), separados por comas.
`knowledge validate` lo comprueba desde `stable/F06` (SHA `b6b82f2` como ancla si el tag falta).
La auditoria de fases lo llamaba `Feedback:`/`Evidence:`; el nombre real es `Fuente:`.

### H.2 · Riesgos de ejecucion absorbidos por funcionalidad (auditoria extrema 2026-09-04)

Tres agentes auditaron codigo, plan y repositorio antes de F15. Lo corregible ahora se corrigio
(ver Change Log de PROJECT_STATE). Lo que pertenece a una funcionalidad futura queda aqui y entra
en su brief al abrirla. Ninguna fila se cierra sin cita en el informe de validacion.

| Riesgo | Funcionalidad | Que debe hacer |
|---|---|---|
| Tres relojes (trader Europe/Madrid, servidor GMT+2/+3, datos UTC) con desfase variable; el dia de riesgo de la prop firm es el del servidor | F15, F17, F28, F31, F33 | F15: `huso_datos` y `huso_operativa` como parametros (`hora` ya exige huso, ADR-0004). F17: desfase servidor-UTC en cada evento. F28: exportar tabla de transiciones DST del horizonte, no un offset fijo. F31: dia de riesgo = dia de servidor. F33: pre-vuelo compara offset real con la tabla y aborta |
| Anclaje de la vela H4 (00:00 Madrid, 00:00 servidor o 17:00 NY) cambia el sesgo la mitad de los dias; MQL5 `PERIOD_H4` nativo divergiria de Python | F07, F15, F29, F30, F33 | Parametro `anclaje_h4` en estado UNKNOWN/DEFAULT_AMBIGUOUS (A-9) hasta evidencia `modalidad: pantalla` de la configuracion del grafico (F07). F15 (antes que F07 por el orden E): agregacion parametrizada por `anclaje_h4`, reproducible para cualquier anclaje declarado; el golden contra la captura del trader se anade en F07 como test de regresion sobre F15. F29: H4 agregada desde M1 con el mismo anclaje; prohibido `iTime/iClose(PERIOD_H4)`. F33: comparar ultima H4 cerrada EA vs Python |
| Parametros de instrumento, broker, prop firm y ejecucion sin hogar | F11, F24, F28, F31, F33 | Categorias del ADR-0004 (hecho). F11 los puebla citando ADR. F24 simula `stops_level`, `freeze_level`, comision y modo de llenado desde `instrumento`/`broker`. F28: `Params.mqh` (estrategia+instrumento+ejecucion) y `Risk.mqh` (prop_firm) con dos hashes en el journal. F33: `[broker]` en settings, entorno `real`, pre-vuelo contra `SymbolInfo*`/`AccountInfo*` |
| Veto de riesgo solo en MQL5: el backtest Python del mismo dia ejecutaria lo que el EA veto y F34 lo contaria como divergencia | F21, F22, F24, F30 | El veto (5 % diario sobre equity a medianoche de servidor, 10 % total, lote maximo, presupuesto de mensajes) es regla pura del dominio con `equity`, `balance_inicio_dia_servidor`, `mensajes_enviados_hoy`; F24 la ejecuta; F28 la exporta; F30 la cubre; el journal registra cada veto como abstencion |
| Redondeo fraccion → puntos (0,75 × 137 = 102,75) y lotaje al paso: `Decimal` no lo resuelve frente a MQL5 | F18, F21, F28, F29 | F18: tipo `Puntos(int)`, regla escrita (stop al lado conservador; lote hacia abajo al paso), test AST que prohibe `float`/`Decimal` en `domain/` salvo `valores.py`. F21: golden con residuo ,5. F28: fracciones como racionales `num/den`; F29: aritmetica en `long` |
| Sesion 1 sin registro, sin reglas ni casos: `RESOLVE_UNKNOWN` sobre parametros inexistentes falla; `LABEL_CASE` sobre casos que F14 aun no creo; la particion holdout debe existir antes de la sesion | F10 | F10 pre-puebla `parametros.yaml` con todos los nombres en `UNKNOWN` (commit `Fuente: ADR-0004`), genera ids de caso, seed y asignacion dev/holdout-1/2/3 con el test de fecha (F14 conserva runner y fixtures). Papel `sesion_feedback` en `fuentes.yaml`, `drive_id` opcional para grabaciones locales, `t0/t1` del feedback contra la duracion de la grabacion |
| Dos ficheros de spec sin version ni hash comun | F11 | `spec_manifest.yaml` con `spec_version` semver y hash canonico sobre `parametros.yaml + strategy_spec.yaml + glossary.yaml`; `strategy_spec.yaml` referencia parametros por nombre, nunca por valor |
| Restricciones del broker (stops level, freeze level, expiracion, llenado) fuera de la spec | F11, F24, F31 | Seccion "restricciones de ejecucion" en la spec con decision explicita (rechazo por stops level = abstencion, nunca aproximacion); F24 las simula; F31 solo implementa lo que la spec dice |
| Estado de jornada no persistente en el EA: reinicio a media jornada = cartuchos a cero; contador de mensajes igual | F23, F31 | F23: esquema de journal versionado y compartido (UTC, offset servidor, evento, regla, condicion fallida, `spec_hash`, `risk_hash`, lecturas ambiguas). F31: al arrancar reconstruye la jornada desde el historial de MT5 (magic + comentario con `spec_hash` y numero de cartucho) y el journal; test "reinicio a media jornada" |
| Tipos que faltan: `enum` (interruptores de ambiguedad), `booleano`, `puntos`, `minutos`, `lotes` | F11, F28 | F11 anade los tipos con `opciones`; F28 los exporta como `enum`/`bool`/`long` |
| Modelo de llenado en la spec pero no en el registro | F11, F24, F27 | Parametro `categoria: ejecucion`, `tipo: enum` (`al_tocar` / `cruce_mas_latencia`) con `latencia_ms`; dos informes en F27 |
| Test de literales prohibe `0.5` y `2000` globalmente (chocara con punto medio de vela y timeouts) | F18 | Exenciones por linea `# no-negocio: motivo`, listadas en el informe de validacion |
| Detalle vivo de F15–F35 solo en `MASTER_PLAN.html` con nombres obsoletos (`botv3`) | F15 | Trasladar el detalle por funcionalidad al Markdown al abrir cada una (el HTML queda como instantanea) |

## Change Log del plan

- 2026-09-03 · version inicial (35 funcionalidades, 8 fases).
- 2026-09-04 · auditoria de fases: seccion H, tres particiones reservadas, pre-registro, tests contra
  historial; F01 amplia su alcance con `.gitattributes`, tests de integridad del indice, hook anti-main,
  `uv sync --locked`.
- 2026-09-04 · auditoria extrema previa a F15: puertas por dependencia, trailer `Fuente:`
  documentado, seccion H.2 con los riesgos de ejecucion absorbidos por funcionalidad, ADR-0004.
