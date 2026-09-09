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
Referencia: `docs/plan/MASTER_PLAN.md` (plan vivo; el `.html` es la instantanea congelada) · `docs/research/2026-09-03-del-corpus-al-bot.html`.

## Development Strategy
Una funcionalidad = una rama `feature/F##-nombre` = un FUNCTIONALITY VALIDATION REPORT = un merge --no-ff
tras validación del usuario. `main` siempre estable y etiquetado `stable/F##`. Push autorizado por el usuario el 2026-09-04; `main` solo recibe merges validados.

## How to Start a Session
1. Leer este fichero. 2. Leer `docs/plan/features/<Current Feature>.md` y `docs/HANDOFF.md` (contexto humano de la ultima sesion; si contradice este fichero, manda este fichero). 3. `make check` (desde F01).
4. Si `Current Feature` está WAITING_FOR_USER_VALIDATION: no avanzar; preguntar.

## Change Regimes (must be respected)
- knowledge/evidence/  → INMUTABLE tras commit (hook). Corrección = nuevo item que supersede.
- knowledge/feedback/  → SOLO AÑADIR. Nunca editar un registro.
- knowledge/spec/, knowledge/cases/ → versionados; cada cambio de valor cita evidence-id o feedback-id.
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; prohibido leer desde src/botsito/spec y src/botsito/domain (guarda en tests); cada una se abre una sola vez.
- src/botsito/domain/ → sin IO, sin reloj, sin MetaTrader (import-linter).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

## Current Phase
FASE 2 · Retroalimentacion del experto. SESION 1 CELEBRADA el 2026-09-09 (2 h 27 min, video v6): las 27 preguntas del cuestionario, las 3 adicionales y las 14 confirmaciones respondidas, y las doce ambiguedades A-1..A-12 RESUELTAS con feedback del trader. Falta el etiquetado de casos, que el trader entrega como backtest completo de mayo y junio con Excel. Siguiente: F11 strategy-spec-schema

## Current Feature
F11 strategy-spec-schema (rama `feature/F11-strategy-spec-schema`, brief en `docs/plan/features/F11-strategy-spec-schema.md`): `feedback apply` (la puerta diferida desde F09), `strategy_spec.yaml` con reglas por nombre de parametro, `glossary.yaml`, `spec_manifest.yaml` con semver y hash canonico sobre los TRES ficheros, y los tipos que faltan en el registro. BRIEF REVISADO por agente el 2026-09-09 (13 bloqueantes, 10 importantes, 8 menores; 20 decisiones de diseno CERRADAS antes de programar). Tres decisiones del consultor: los valores bajo ambiguedad abierta entran CONFIRMED y la revision se ve por cruce; la normalizacion de los 14 valores que no convierten se hace con registros de feedback que superseden (campo `valor_canonico`), no con codigo; enero de 2026 ya estaba congelado, asi que A-14 es medible sin descargar nada.
## Current Branch
feature/F11-strategy-spec-schema

## Stable Main State
1475956 · merge de la sesion 1 con el trader (tras stable/F10). make check verde: 538 casos (373 funciones), 4 contratos, mypy strict, state/config/knowledge validate (33 parametros con 32 sin confirmar, 353 items de evidencia, 1 contradiccion abierta, 17 ambiguedades con A-1..A-12 RESUELTAS, 1 paquete de sesion valido, 5 manifiestos de datos, 11 de transcripcion con 6 activos, 6 de fotogramas). Tags stable/F05, stable/F05-auditoria-1, stable/F05-previos-F07, stable/F07, stable/F08, stable/F10 y stable/F10-sesion-01. Rama main protegida en GitHub.

## Completed Phases
- FASE 1 · Base de conocimiento (F03, F04, F05, F06, F07, F08) · cerrada el 2026-09-08 en 5d8cf3c · puerta: 5 videos inventariados, transcritos (large-v3, glosario v2) y con fotogramas a 1 fps; 341 items de evidencia verificables por maquina y trazables a su propuesta y decision; busqueda `kb find | at` con fuente en cada linea; make check verde en main
- FASE 0 · Fundamentos (F01, F02) · cerrada el 2026-09-04 en dc3384d · puerta: make check verde en main; registro de parametros con tipos y lectura estricta; .gitattributes y cero CRLF; hooks copiados por make sync; tags stable/F01 y stable/F02; CI Linux verde

## Completed Features
- F01 · project-scaffold · validada el 2026-09-04 · docs/validation/F01-project-scaffold.md · tag stable/F01
- F02 · config-and-parameter-registry · validada el 2026-09-04 · docs/validation/F02-config-and-parameter-registry.md · tag stable/F02
- F03 · corpus-inventory · validada el 2026-09-04 · docs/validation/F03-corpus-inventory.md · tag stable/F03
- F06 · evidence-model · validada el 2026-09-04 · docs/validation/F06-evidence-model.md · tag stable/F06
- F09 · expert-feedback-model · validada el 2026-09-04 · docs/validation/F09-expert-feedback-model.md · tag stable/F09
- F15 · market-data-ohlc · validada el 2026-09-04 · docs/validation/F15-market-data-ohlc.md · tag stable/F15
- F04 · transcription-pipeline · validada el 2026-09-05 · docs/validation/F04-transcription-pipeline.md · tag stable/F04
- F05 · frame-extraction · validada el 2026-09-05 · docs/validation/F05-frame-extraction.md · tag stable/F05
- Auditoria global de la estructura · validada el 2026-09-06 · docs/validation/AUDITORIA-2026-09-05-estructura.md · tag stable/F05-auditoria-1
- Previos de F07 · validados el 2026-09-06 · docs/validation/F07-previos.md · tag stable/F05-previos-F07
- F07 · evidence-extraction · validada el 2026-09-07 · docs/validation/F07-evidence-extraction.md · tag stable/F07
- F08 · evidence-retrieval · validada el 2026-09-08 · docs/validation/F08-evidence-retrieval.md · tag stable/F08
- F10 · elicitation-kit · validada el 2026-09-08 · docs/validation/F10-elicitation-kit.md · tag stable/F10

## Features Waiting for Validation
—

## Existing Components
- Paquete `botsito`: `domain/valores.py` (Fraccion, Porcentaje sobre Decimal, no intercambiables; HoraLocal con huso); `config/registro.py` (registro de parametros con categoria, procedencia y lectura estricta; vacio de valores); `config/ajustes.py` (entorno y rutas, sin claves de negocio).
- CLI: `state check` (rama, recuento de tests, tag estable, informes de validacion, main sin cambios tras el tag), `knowledge validate` (registro, manifiesto, evidencia, contradicciones, feedback, historial de git y trailers `Fuente:`), `config validate` (ajustes contra el registro), `corpus inventory` y `corpus check`.
- `corpus/inventario.py`: manifiesto del corpus con SHA-256, ffprobe, papel y huecos de fotogramas heredados. `knowledge/corpus/{fuentes,manifest}.yaml`.
- `evidence/{modelo,contradicciones,verificacion,propuestas}.py` + `comun/historial.py` + `validation/contexto_evidencia.py` (ADR-0009): EvidenceItem inmutable (id con hash) con `transcripcion` y referencias `fr-*`; cita de audio localizada por tokens en la cruda citada con tiempo por palabras (`[t0 - 2 s, t1 + 2 s]`, comodin `[...]`); cita de pantalla anclada a un fotograma real del tramo; contradicciones regeneradas; propuestas trazables en `knowledge/_proposals/` (esqueleto, `--check` con guardias, sello `salida_sha256`, `accept`/`reject`); taxonomia `knowledge/evidence/_temas.yaml`. CLI `evidence new|propose|accept|reject|list|contradictions`. Hook rechaza editar o borrar evidencia y feedback.
- `feedback/modelo.py`: FeedbackRecord solo-anadir (id por hash, coherencia accion/objetivo, trazabilidad, supersede del mismo objetivo sin ciclos); CLI `feedback new` (valida contexto antes de escribir), `trace`, `pending` (filtra parametros no `estrategia`); `commits_sin_fuente` exige trailer `Fuente:` con ids existentes (evidencia, feedback, ADR) en commits que tocan spec/cases desde el SHA de stable/F06; `historial_evaluable` marca clon superficial o repo anidado como no evaluable.
- Contratos de importacion (import-linter + test AST; `domain` no importa `config`). Test de literales de negocio con lista real. Tests de integridad del indice.
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- `domain/velas.py` (F15): `Vela` (MinutoUtc, Puntos, volumen entero, duracion, n_m1, completa), `SerieVelas`, `combinar`; sin datetime/float/Decimal. `data/velas.py` (CSV determinista), `data/agregacion.py` (particion UTC por reloj de pared, ADR-0005), `data/dukascopy.py` (bi5, red inyectada, planas descartadas), `data/dataset.py` (dataset congelado, manifiesto inmutable con id por hash, `cargar_serie` con ventana). CLI `data download/check/aggregate`. Hook y `knowledge validate` protegen `data/manifests/`.
- Paquete `comun/` (ADR-0006, por encima de `domain`): `yaml_estricto.py` (claves duplicadas y no hashables rechazadas, fechas como texto), `historial.py` (guardia de git para evidencia, feedback y manifiestos; trailers Fuente), `documentos.py` (normalizacion, vacios, hash corto, directorios, supersede, activos), `ids.py` (todos los formatos de id), `husos.py` (nombre IANA canonico, un criterio para registro y datos). `validation/knowledge.py`: orquestador de `knowledge validate` (F12 y F14 anaden capas ahi); la CLI solo imprime. Registro: accesores por tipo declarado; test de contrato que vigila `registro.<accesor>("nombre")` en src/. Contrato de capas: cli > validation > viewer/mql5bridge > engine > cases > spec > feedback > evidencia/corpus/data/config > comun > domain. `scripts/instalar_hooks.py` (make hooks portable; destino `git rev-parse --git-path hooks`; aborta con `core.hooksPath` global). `.python-version` = 3.12 (local y CI).
- `cases/{ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py` (F10, ADR-0011): ambiguedades legibles por maquina (`knowledge/spec/ambiguedades.yaml`), cuestionario con casos `ev-*` por origen fusionado, ventanas de replay sobre dias no vistos (hash de velas y limites H4 por anclaje), particiones por hash con seed, kappa de Cohen desde los `LABEL_CASE`, paquete determinista de cada sesion en `knowledge/cases/kit/<sesion>/` con `check` puro; guardia en `knowledge validate` (particiones antes del primer LABEL_CASE y sin cambios despues). CLI `kit build|check|kappa`. Datos de negocio del kit en `knowledge/cases/kit/config.yaml`.
- `retrieval/{indice,consultas,salida}.py` (F08, ADR-0010; capa entre `spec` y `feedback`): indice en memoria regenerado en cada ejecucion (341 items + segmentos de las crudas activas con su corregida y `dudas`; fotograma de referencia `referencia_en`), token de busqueda = tokens de F07 con acentos plegados y numeros normalizados, `kb find` (AND por documento, `--frase` con comodin via `buscar_secuencia`, `--prefijo`, filtros, `--top`, `--json`) y `kb at` (items, segmentos, fotograma y contradicciones de un instante). Toda linea con fuente; rutas relativas; sin escritura. `corpus.pipeline_transcripcion.{dudas_de,cargar_capas}` compartidos con `validation`.
- `corpus/{audio,transcripcion,motor_whisper,glosario,pipeline_transcripcion,manifiestos_transcripcion}.py` (F04, ADR-0007): WAV por video y corte por muestras en silencios, segmentos en ms enteros con senales, faster-whisper solo en `motor_whisper`, glosario de dos alcances, pipeline reanudable con manifiesto INMUTABLE `tr-<video>-<motor>-<hash8>` en `knowledge/corpus/transcripciones/`, corregida = cruda + glosario verificada por recomputo; guardia `comprobar_prompt` (223 tokens, antes de cargar la GPU) y huella de reanudacion sin `gpu` ni `initial_prompt_tokens` (`CLAVES_FUERA_DE_HUELLA`, 2026-09-06). CLI `corpus transcribe | glossary apply | transcript check | transcript show`; capa en `knowledge validate`; hook protege el directorio.
- Corpus: 5 videos (v5 = grabacion del trader del 2026-09-05 en FXReplay, 6 min, no esta en Drive) y material adicional de enero, abril y agosto 2026 (xlsx + capturas).
- `corpus/trabajo.py` (auditoria 2026-09-05): guardias comunes a transcripciones y fotogramas: carpeta de trabajo decidida por marcas locales Y por los manifiestos registrados (clon sin `data/`), exactamente una extraccion activa por video y tipo, inmutabilidad del contenido por carpeta, manifiesto existente idempotente sin `reemplaza_a`. `config/ajustes.carpeta_datos` unica para CLI y `knowledge validate`.
- `corpus/{fotogramas,manifiestos_fotogramas}.py` (F05, ADR-0008): cobertura completa de cada video a 1 fps sin perdida (PNG bitexact) con regla `select` "primer fotograma con t >= instante" y `pts` real de `showinfo`; `index.jsonl` en `data/fotogramas/<video>/png-1fps/`; manifiesto INMUTABLE `fr-<video>-<hash8 del indice>` en `knowledge/corpus/fotogramas/` (un activo por video, `reemplaza_a`, huecos sobre `pts`, extra); obligatorios en `knowledge/corpus/fotogramas_obligatorios.yaml` validados contra el indice activo; referencia citable `fr-<id>/<t_ms>` (`referencias_conocidas` excluye `heredado_v2`). CLI `corpus frames extract | check | show`; capa en `knowledge validate`; hook protege el directorio.
- Plantillas: brief, ADR, informe de validacion. ADR-0001 a 0011. `.gitattributes` con LF (`*.bi5` binario).

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- knowledge/evidence/README.md (esquema de EvidenceItem) · src/botsito/evidence/modelo.py
- knowledge/feedback/README.md (esquema de FeedbackRecord y plantilla de sesion) · src/botsito/feedback/modelo.py · src/botsito/comun/historial.py
- knowledge/corpus/fuentes.yaml (fuentes esperadas, ids de Drive) · knowledge/corpus/manifest.yaml (GENERADO) · src/botsito/corpus/inventario.py
- docs/adr/0011-kit-de-elicitacion.md · knowledge/spec/ambiguedades.yaml (manual; fuente de la tabla Known Ambiguities) · knowledge/cases/kit/README.md (gramatica de la etiqueta) · knowledge/cases/kit/config.yaml (datos de negocio del kit) · src/botsito/cases/paquete.py · docs/validation/F10-elicitation-kit.md
- knowledge/spec/parametros.yaml (LA puerta de los parametros; 33 parametros: `huso_operativa` CONFIRMED por ADR-0005 -desmentido por la sesion 1, se corrige en F11- y 32 en UNKNOWN hasta que F11 aplique el feedback) · src/botsito/config/registro.py · src/botsito/domain/valores.py
- docs/adr/0005-datos-de-mercado-fuente-formato-y-relojes.md · data/manifests/README.md (esquema del manifiesto) · src/botsito/data/agregacion.py (regla de anclaje) · tests/fixtures/ohlc/README.md (fixtures reales con sha256)
- docs/adr/0007-transcripcion-en-dos-capas.md · knowledge/corpus/glosario_asr.yaml (manual, versionado) · knowledge/corpus/transcripciones/ (INMUTABLE) · src/botsito/corpus/pipeline_transcripcion.py · docs/validation/F04-transcription-pipeline.md
- knowledge/corpus/tramos_no_citables.yaml (manual; tramos de video que NO son especificacion: `evidence propose --check` y `evidence new` rechazan una cita que caiga dentro) · src/botsito/validation/contexto_evidencia.py
- docs/adr/0008-fotogramas-cobertura-completa.md · knowledge/corpus/fotogramas_obligatorios.yaml (manual) · knowledge/corpus/fotogramas/ (INMUTABLE) · src/botsito/corpus/fotogramas.py · docs/validation/F05-frame-extraction.md
- docs/plan/features/F02-config-and-parameter-registry.md · docs/validation/F02-config-and-parameter-registry.md
- docs/adr/0002-registro-de-parametros-una-sola-puerta.md · docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
- docs/plan/AUDITORIA_FASES_2026-09-04.html · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
382 funciones de test (548 casos; parametrizadas x3, x5, x6, x7, x8, x9, x11, x13, x15, x18, x19 y x22) · unit: project_state, project_state_rutas, adr, tree, cli, cli_data, valores, velas, registro, ajustes, inventario, evidence, feedback, yaml_estricto, dukascopy, agregacion, agregacion_dst, dataset, golden_ohlc, comun, audio, transcripcion, pipeline_transcripcion, motor_prompt, verificacion, propuestas, fotogramas, retrieval, kit · integration: fotogramas_ffmpeg · contract: import_contracts, no_business_literals, repository_integrity, registro_accessors, evidence_history, feedback_history, data_manifest_history, transcripcion_history, fotogramas_history, golden_citas_f07 (40 referencias contra la evidencia real), golden_consultas_f08 (15 consultas; con y sin `data/`), kit_particiones (guardia de ancestro), hoja_sesion_docx (OOXML valido, citas del paquete, sin fuga de holdout) · 4 contratos import-linter KEPT · mypy strict OK (src + tests)

## Architectural Decisions (index)
- ADR-0001 estructura del repositorio y regimenes de cambio — ACTIVE
- ADR-0002 registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta — ACTIVE
- ADR-0003 hooks copiados desde scripts/git-hooks; sin framework pre-commit — ACTIVE
- ADR-0004 categorias de parametro y horas con huso — ACTIVE
- ADR-0005 datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje — ACTIVE
- ADR-0006 capas revisadas, paquete `comun` y accesores del registro por tipo declarado — ACTIVE
- ADR-0007 transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario — ACTIVE
- ADR-0008 fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable — ACTIVE
- ADR-0009 verificacion mecanica de citas contra la cruda y propuestas de evidencia trazables y selladas — ACTIVE
- ADR-0010 busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente — ACTIVE
- ADR-0011 kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback — ACTIVE

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

## Lineamientos recibidos del usuario y hechos del corpus (evidencia en F07)
Dos fuentes distintas, separadas a proposito: (a) lo que el usuario (consultor) aporta por escrito
sobre la operativa (lineamiento, NO es evidencia ni feedback del trader) y (b) hechos leidos en el
corpus (crudas y fotogramas). Desde F07 (2026-09-07) todo hecho del corpus tiene un item en
`knowledge/evidence/` (id `ev-*` anotado aqui; la cita se verifica contra la cruda o el fotograma);
las reglas se infieren en F11, no aqui.

### (a) Lineamientos del usuario

- **2026-09-04 · Geometria del riesgo y gestion del stop.** "Se traza un 1:3 inicialmente; con eso
  se calcula el lotaje y todo. Una vez se mete la operativa, se baja el SL hasta el 0,75 del trade
  o hasta el 0,8; el TP sigue donde estaba inicialmente."
  - Estado en el plan: CONTEMPLADO. MASTER_PLAN F21 (caja 0/0,25/0,5/0,75/1, lotaje sobre la
    distancia completa, stop en 0,75 con colchon de spread, objetivo 1:3 sobre la distancia completa)
    y la investigacion (tres confirmaciones aritmeticas: ratio 4,08/3,94 = 3/0,75; Excel con -0,75).
  - Citas del corpus re-citadas en F07 (evidencia): V2 0:31:42-0:33:53 `ev-v2-003142-beb4ad3c`
    (stop en 0,75), `ev-v2-003256-0197f4e1` (el objetivo sigue en 1:3), `ev-v2-003336-fc210a05`
    (lotaje sobre la distancia completa), `ev-v2-003350-dbd9e3ad` (una ganadora acaba en 3,25);
    V1 0:06:20 `ev-v1-000620-0f7dea14` (cuadro de Gann en 0,75 apenas se genera la entrada);
    V4 0:08:35-0:09:09 `ev-v4-000835-782cf2cc` (respiro de 0,75 a 0,80 por el spread),
    `ev-v4-000858-4e50f00c` (mas respiro con noticias), `ev-v4-001207-0c4ffd4b` y
    `ev-v4-001221-1e66b5fd` (0,75 desplazado segun el spread del momento).
  - Lectura: el 0,8 es el colchon de spread sobre el 0,75, no un nivel alternativo libre.
  - Hallazgo F04 (2026-09-05, large-v3): en V1 0:15:59 el trader dice "ya ha pasado mas del 50%
    de la vela" (la transcripcion heredada decia 40 %) y en V1 0:16:51 "de pasar de 0.75 es a
    0.50". La cifra 40 % frente a 50 % es la ambiguedad A-12 (sesion 1). Evidencia:
    `ev-v1-001557-1dd16e5c` (50 % de la vela) y `ev-v1-001643-47673889` (de 0,75 a 0,50).
  - Preguntas abiertas para el trader (sesion 1): (a) ¿el 0,8 es fijo o "0,75 mas el spread del
    momento"? (b) ¿el stop se coloca en el 0,75 al enviar la orden limite o solo tras el llenado?
    Para el bot es equivalente y mas seguro adjuntar el SL al 0,75 en la propia orden pendiente
    (F22/F31); confirmar que el trader no ve inconveniente.
  - Consecuencia para F21: el TP nunca se recalcula al mover el SL (invariante a probar).
  - Material del 2026-09-05 (v5, `tr-v5-large-v3-int8-float16-01a1ae03`, reemplazada el 2026-09-06 por `tr-v5-...-3c6fbb57`, donde la frase esta en 0:03:12-0:03:35): 0:03:21 "si yo protejo a
    0.80, que es el SL por defecto"; 0:04:44 "el calculo del RR en base al 1 %"; 0:04:56 "todo lo
    backtestee buscando el 1:3... posibilidad de amplificar a 1:4, lo veremos mas adelante"; la
    caja en pantalla (`fr-v5-718ecabb/240000`) tiene el nivel 0,8, no 0,75. Refuerza la pregunta (a)
    de A-10. Evidencia (F07): `ev-v5-000312-f5062062` (0,80 SL por defecto; contradiccion
    mecanica `stop.nivel` con `ev-v1-000448-346d6d90` y `ev-v2-003142-beb4ad3c`, 0,75),
    `ev-v5-000219-bc86af3d` (a veces no llega hasta el 0,80), `ev-v5-000442-b13610fa` (RR sobre
    el 1 %), `ev-v5-000456-dfb95b24` y `ev-v5-000515-02b5bc7a` (1:3 con 1:4 abierto). No se
    decide aqui.
### (b) Hechos del corpus, ya como evidencia (F07, 2026-09-07)
- **Obligatorios de F05 (pantalla):** Excel de abril V3 0:28:56 `ev-v3-002856-bff84636` (2,83 /
  -0,75 / 3,3; `fr-v3-982da728/1736000`); ratios 4,08 / 3,94 V2 0:33:21 `ev-v2-003320-a736fd37`
  (`fr-v2-c5a09508/2001000`); caja 0,75 = 1,19537 V4 0:12:30 (items de la caja en pantalla del
  tramo V4 0:05-0:15: `ev-v4-000813-c916eac6` nivel de entrada 1,19502 y `ev-v4-001221-1e66b5fd`,
  modalidad ambas, caja 0,75 = 1,19537).
- **Candidatos A-9 (reloj del grafico):** V3 0:01:36 `ev-v3-000136-6160fcea` ("configurado como
  UTC mas 2", Madrid). Ningun fotograma muestra la hora de apertura de una H4: el golden H4 sobre
  F15 pasa a F10 (decision del usuario 2026-09-07).
- **Ficha de reglas en Word (V3 0:01:38, `fr-v3-982da728/101000`):** `ev-v3-000138-567dc5d7`
  (ventana 07-15), `ev-v3-000138-8399c18a` (sesgo por la H4 previa cerrada),
  `ev-v3-000138-fc8f7905` (limite estricto de 2 cartuchos); lecturas confirmadas en
  `ev-v3-004817-f2dfb955` y `ev-v3-005735-f24a4bdf`.
- **V4 1:28:20 (riesgo por operacion):** `ev-v4-012815-2aa13700` (0,40 o 0,50 escalado sobre la
  cuenta) y `ev-v4-012733-0c8d7f1f` (racha de 7 perdidas: 0,5 -> 3,5 % de drawdown).
- **2026-09-05 · Reentrada tras un "igual" (equal) y descarte por flujo de ordenes** (v5; evidencia
  `ev-v5-000038-6570a65f`, `ev-v5-000246-17eff9e1`, `ev-v5-000527-c56ebe45`,
  `ev-v5-000427-f8d5d36d`; sin inferir regla): 0:00:39 "no hay entrada porque no me genera el esquema 2 de entrada,
  sino que genera un flujo de ordenes, esa entrada queda descartada"; 0:01:56-0:02:58 "el precio
  llega, activa la entrada y se regresa... cuando hay un equal que no lo vamos a poder anticipar...
  contarlo como perdida, pero reentrar nuevamente si el precio te llega a romper nuevamente esta
  zona"; 0:05:27 "como esto es un igual... esperariamos a que el precio rompa por arriba para la
  reentrada". Relacion: A-7 (stop del segundo esquema), A-2 (cartuchos: la reentrada consume uno?),
  A-4 (BE "cuando se cumplen las condiciones"). Preguntas candidatas para la sesion 1.
- **2026-09-05 · Backtest de abril 2026** (`Material adicional/backtesting-analytics ABRIL 2026.xlsx`
  y 6 capturas de Analytics): 38 operaciones, 17/19/2, PnL +872, win rate 47,22 %, RR medio 3,64,
  profit factor 4,01, expectancy $22,95; horas 05-12 UTC; por dia lun 50 %, mar 25 %, mie 71 %,
  jue 25 %, vie 56 %. Tres meses exportados (enero 58, abril 38, agosto 47): golden de F26.
  Evidencia del video v5: `ev-v5-000000-69774090` (sesion de backtest de abril de 2026); las
  cifras del xlsx entran como `material_adicional` cuando F26 las cite desde un tramo de video.

## Expert Validations
—

## Known Ambiguities
Fuente legible por maquina desde F10: `knowledge/spec/ambiguedades.yaml` (ids, pregunta, evidencia,
parametros, estado; un test exige que esta tabla coincida en id y titulo).
Las doce (A-1..A-12) quedaron RESUELTAS en la sesion 1 del 2026-09-09, cada una con su registro de
feedback, su minuto y su cita en v6; la tabla se conserva porque es la pregunta que se llevo a la
sesion y el test anti-deriva la compara con el YAML. El esquema de feedback solo acepta ids `A-N`.
Columna "resuelve en": la funcionalidad que convierte la respuesta en regla o parametro.

Lo que la sesion DEJA ABIERTO son A-13..A-17, registradas el 2026-09-09 con los doce items de
evidencia de v6 que el consultor acepto:
1. **A-13 break even**: responde "apenas toca" (0:57:01) y doce minutos despues se plantea exigir
   un rompimiento con cuerpo, porque protegerlo al toque le hace perder movimientos (1:09:27,
   1:09:47). No hace falta volver a preguntarselo: se mide sobre los mismos dias.
2. **A-14 anclaje H4**: dice que en el cambio de horario mantiene "la misma hora" y acto seguido
   que la apertura podria verse "a las 8, o [...] a las 6" (0:58:10). Con UTC+2 fijo el anclaje es
   21:00 UTC todo el año; con Madrid, en invierno se desplaza. Mayo y junio no se ven afectados;
   enero si.
3. **A-15 alcance** (DECIDIDA por el consultor el 2026-09-09: no se amplia en esta fase; se cierra por ADR en F11): deja abierto ampliar a Nueva York, "puedes buscar las operaciones donde sea"
   (1:46:23), cuando toda su operativa grabada va de 07:00 a 15:00. Decision del consultor.
4. **A-16 proveedor de datos** (DECIDIDA el 2026-09-09 con medicion, `docs/validation/anexos/A-16-proveedor-de-datos-2026-09-09.md`: el historico sigue siendo Dukascopy porque la demo de FundedNext solo sirve M1 desde el 2026-06-03 y no cubre el paquete; donde se pueden comparar coinciden a 2 puntos de mediana; MT5 queda para spread, ejecucion y paridad): el backtestea en FX Replay, que usa datos de Oanda (0:24:14), y el
   proyecto mide sobre Dukascopy (ADR-0005). Con reglas que dependen de romper "por una milesima",
   uno o dos puntos cambian un dia entero.
5. **A-17 noticias** (DECIDIDA por el consultor el 2026-09-09: se opera con noticias; si resulta un impedimento, el filtro se hara bloqueante y anclado a un calendario externo tipo Investing, que es funcionalidad nueva, no un parametro): avisa de que la cuenta puede prohibir operar dos minutos antes y despues de
   una noticia y cerrarla aunque acabes en profit (2:00:29, 2:01:14), y aun asi deciden operar con
   noticias (2:02:00). Verificar la regla real antes de F33.

| Id | Ambiguedad | Resuelve en | Pregunta de la sesion 1 |
|---|---|---|---|
| A-1 | sesgo H4 | F11 (regla), F18 (motor de sesgo) | ¿que vela H4 fija el sesgo y cuando cambia? |
| A-2 | tercer cartucho | F11, F21 | ¿2 o 3 intentos por zona? (contradiccion ficha vs V4 0:48:41) |
| A-3 | salida sin ruptura | F11, F23 | ¿se cierra si no rompe? ¿cuando? |
| A-4 | BE al tocar o al cierre | F11, F23 | ¿break-even al tocar el nivel o al cierre de vela? (V4 0:44:56) |
| A-5 | cadencia de reubicacion | F11, F22 | ¿cada cuanto se reubica la orden pendiente? |
| A-6 | cierre 15:00 | F11, F23 | ¿cierre forzoso a las 15:00 y en que huso? |
| A-7 | stop del 2.o esquema | F11, F21 | ¿donde va el stop en el segundo esquema de entrada? |
| A-8 | "dos velas como una" en mapeo | F11, F18 | ¿cuando dos velas cuentan como una estructura? |
| A-9 | anclaje de la vela H4 (hora y huso del grafico) | sesion 1 (captura, P-03 del kit), F11 (valor y `huso` de `anclaje_h4`, creado UNKNOWN en F15) | ¿a que hora y en que huso del grafico abre su H4? (se resuelve viendo su grafico) |
| A-10 | stop a 0,8: fijo o 0,75 + spread | F21 | ¿el 0,8 es fijo o "0,75 mas el spread del momento"? |
| A-11 | SL en la orden o tras el llenado | F22, F31 | ¿el SL va en la orden pendiente o se pone tras el llenado? |
| A-12 | porcentaje de vela transcurrido para bajar la proteccion a 0,50: 40 % (transcripcion heredada) o 50 % (large-v3, V1 0:15:59) | F21 | ¿a partir de que parte de la vela bajas el stop a 0,50? |
| A-13 | break even al toque o con cuerpo | F11, F23, F26 | ¿el rompimiento que dispara el BE vale al toque o hay que esperar cuerpo? (v6 0:57:01 vs 1:09:27) |
| A-14 | anclaje H4 fuera del horario de verano | F11, F15 | ¿UTC+2 fijo (21:00 UTC todo el año) o Madrid (en invierno se desplaza)? (v6 0:58:10) |
| A-15 | alcance de la ventana operativa | F11 | ¿solo 07-11 y 11-15, o tambien Nueva York? (v6 1:46:10) |
| A-16 | proveedor de datos para medir la fidelidad | F26 | ¿como se comparan decisiones sobre Oanda con un bot medido sobre Dukascopy? (v6 0:24:14) |
| A-17 | noticias frente a la regla de la cuenta de fondeo | F11, F33 | ¿la cuenta prohibe operar dos minutos antes y despues de una noticia? (v6 2:00:29) |

Las 3 preguntas bloqueantes de la sesion 1 (MASTER_PLAN G) se eligen en el brief de F10 con los
casos delante; candidatas por impacto en el kit: A-9 (afecta a todos los casos), A-2 y A-4.

Evidencia por ambiguedad (F07, 2026-09-07; ids en `knowledge/evidence/`, `evidence list --tema`):
- A-1 sesgo H4: `ev-v2-000836-6dbfcd6b`, `ev-v3-000531-4d6375b6`, `ev-v3-000824-c81f03eb`,
  `ev-v3-010948-331c69aa`, `ev-v3-011045-a185d2ba`, `ev-v3-011614-a5a05b0a` (simplificacion
  abierta), `ev-v4-004603-d0ffd4f2`.
- A-2 tercer cartucho: ficha 2 `ev-v3-000138-fc8f7905`, `ev-v3-004817-f2dfb955`,
  `ev-v4-003350-acb03ee7` frente a 3 `ev-v4-002333-8bf96363`, `ev-v4-004742-30c8d58a`,
  `ev-v4-004832-6543b551`, `ev-v4-005411-a486336d`; pregunta del consultor `ev-v4-002951-d3132b3f`.
- A-3 salida sin ruptura: `ev-v4-010759-514b5d7d` (cerrar al cierre de la vela sin rotura) frente
  a `ev-v4-010831-5f4a00ad` (prefiere proteger y dejarlo).
- A-4 BE al tocar o al cierre: `ev-v4-004447-bc2e74ee`, `ev-v2-003103-31d872da`,
  `ev-v5-000427-f8d5d36d`.
- A-5 cadencia de reubicacion: `ev-v1-001358-a2b8ec0d`, `ev-v4-010731-bb8af97c`,
  `ev-v4-010857-5bc906c9` (se actualiza con el precio; sin cadencia explicita).
- A-6 cierre 15:00: `ev-v4-011514-fe34ac7e` (se cierra en punto a las 3 PM); huso en A-9.
- A-7 stop del 2.o esquema: `ev-v3-004329-a16d379b`, `ev-v4-002056-5d25b29d`,
  `ev-v4-002139-23e44f38`, `ev-v4-003029-2ea7124e`, `ev-v4-003102-1ddeeaa8`,
  `ev-v4-003227-038864db`, `ev-v4-003252-ef8d3139` (opcion simple: 0,75 estatico en los dos).
- A-8 dos velas como una: `ev-v3-010648-0039e34d`, `ev-v3-011540-5425b533`.
- A-9 anclaje H4: `ev-v3-000136-6160fcea` (grafico en UTC+2), `ev-v3-000157-b26147c7` (velas H4
  de 7 a 11 y de 11 a 3 hora del grafico); la hora de apertura no aparece en ningun fotograma.
- A-10 0,8 fijo o 0,75 + spread: contradiccion mecanica `stop.nivel` (`ev-v1-000448-346d6d90`,
  `ev-v2-003142-beb4ad3c` = 0,75; `ev-v5-000312-f5062062` = 0,80); `ev-v4-000835-782cf2cc`,
  `ev-v4-001221-1e66b5fd`.
- A-11 SL en la orden o tras el llenado: `ev-v4-001207-0c4ffd4b` (el stop que se introduce en la
  operacion es el 0,75), `ev-v1-000620-0f7dea14`; nada dice si va en la orden pendiente.
- A-12 40 % o 50 % de la vela: `ev-v1-001557-1dd16e5c` (50 %), `ev-v1-001643-47673889`.

## Known Contradictions
Mecanica (`knowledge/evidence/_contradicciones.yaml`, mismo tema con `valor` distinto): 1 ABIERTA,
`stop.nivel` 0,75 (`ev-v1-000448-346d6d90`, `ev-v2-003142-beb4ad3c`) frente a 0,8
(`ev-v5-000312-f5062062`) = A-10; se cierra con un registro de feedback (F09) tras la sesion 1.
De lectura (temas distintos, sin `valor` comparable; abiertas como ambiguedades): cartuchos 2
(ficha, `ev-v3-000138-fc8f7905`) vs 3 (`ev-v4-004832-6543b551`) = A-2 · parciales 30-40 %
(`ev-v2-002419-4629d258`) vs sin parciales (`ev-v1-002313-6342a154`, `ev-v3-010244-2edecd2d`,
`ev-v4-011112-17178b38`; idea del 50 % en 1:2 `ev-v4-011116-b0e6f3f5`) · BE al tocar vs al cierre
(`ev-v4-004447-bc2e74ee`) = A-4 · salida anticipada si/no (`ev-v4-010759-514b5d7d` /
`ev-v4-010831-5f4a00ad`) = A-3.

## Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 341 items sin colision.

## Technical Debt
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA. Carpeta de Drive `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R` ("transcripciones (crudas, Bot v3)") con SHA256SUMS, LEEME, 5 manifiestos, 5 crudas (jsonl y txt), 5 WAV y v5 (el usuario subio los binarios el 2026-09-06; verificado por API). Una retranscripcion futura exige repetir la copia (nuevo SHA256SUMS via `docs/validation/anexos/F07-previos/staging.py`).
- Glosario ASR v2 APLICADO el 2026-09-06 (aprobado por el usuario): 29 terminos, 6 sustituciones globales y 6 de segmento; los 5 videos retranscritos con ids nuevos. Regla vigente: cambiar `vocabulario` cambia el `initial_prompt` y la huella y exige retranscribir; las `sustituciones` solo exigen `corpus glossary apply`. Las apariciones de `boss|voz|blog|blogs` y `split|sprint` fuera de los 6 segmentos verificados quedan como `dudas` en `correcciones.jsonl` (v2: 8, v3: 13, v4: 4) para que F07 las mire al citar. HECHO en F07: los items que caen en esos segmentos llevan `confianza: media` y la nota lo dice (94 items).
- Fotogramas obligatorios de F05 LEIDOS y REGISTRADOS como evidencia en F07 (`ev-v3-002856-bff84636`, `ev-v2-003320-a736fd37`, `ev-v4-001221-1e66b5fd`; ficha de Word `ev-v3-000138-*`; reloj `ev-v3-000136-6160fcea`): V3 0:28:56 el Excel muestra `2,83 / -0,75 / 3,3 / -0,75 / -0,5` (inferencia: la heredada `2,3 / 3,23` no coincide con la pantalla; large-v3 coincide en 2.83 y dice 3.33 donde hay 3,3); V2 0:33:21 herramienta de posicion `4,08` y `3,94` (golden F21 confirmado); V4 0:12:30 caja 0,75 = `1,19537`. Relojes de grafico en `UTC+2` en V2 (TradingView) y V4 (FXReplay); V3 0:01:41 "lo tengo configurado como utc mas 2": candidatos de A-9 para F07. Hallazgo: `fr-v3-982da728/101000` es la ficha de reglas en Word con las confirmaciones del trader (2 cartuchos "si" frente a "limito a tres" en V4 0:48:41: A-2; "probar sin parciales").
- RESUELTO en F07 (ADR-0009 §3): `validar_contra_manifiesto` y el `comprobar` de `evidence new` reciben las referencias conocidas (`ContextoEvidencia.referencias`, sin `heredado_v2`); `knowledge/evidence/README.md` fila `fotogramas` actualizada.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F04, pendientes tecnicos (i) y (ii) RESUELTOS el 2026-09-06 (previos de F07): huella sin GPU/driver (`CLAVES_FUERA_DE_HUELLA`), guardia de 223 tokens del prompt (`comprobar_prompt`), `hotwords` medido y descartado (ADR-0007 enmienda). (iii) `palabras` de la cruda bajo un texto corregido sin marcar: CERRADA por declaracion en F08 (`kb` muestra la corregida sin tiempos propios y la cabecera dice "tiempos de la cruda"; ADR-0010).
- Hallazgo F04 V4 1:28:20-1:28:37 (riesgo por operacion 0,40 o 0,50, escalado) REGISTRADO en F07: `ev-v4-012815-2aa13700`, `ev-v4-012733-0c8d7f1f`. Queda como pregunta candidata en F10.
- RESUELTA en F07 (ADR-0009; secuencia cumplida: glosario v2 -> retranscribir -> Drive -> evidencia). Regla de cita (decidida en la auditoria del 2026-09-05, ver MASTER_PLAN H fila F07): `cita_literal` se verifica contra la capa CRUDA (la que forma el id `tr-*`); la corregida es ayuda de lectura. Secuencia obligatoria: glosario v2 aprobado -> retranscribir los 5 videos (v1-v5) (`--reemplaza-a`) -> copia en Drive -> primera evidencia con `transcripcion:`.
- F10: la fecha de la sesion 1 (`2026-09-15`) es provisional (regenerar con `kit build --sesion <fecha>-sesion-01 --seed 20260915` y commitear ANTES de la sesion); el paquete exige la confirmacion escrita del trader de que no ha visto mayo ni junio de 2026 (si la niega, `vistos.yaml` y otro mes con `data download`); `mapa_parametros.yaml` es manual (F11 lo hara normativo); el primer dia laborable de cada mes solo entra si el mes anterior esta congelado y es contiguo.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave). El control independiente es el usuario (acepto los 341 sin cambios; recall humano de V4 0:05-0:15 sin faltas). Dueno: si llega una clave, otro proponente rellena una propuesta del mismo tramo y se compara; mientras tanto no bloquea.
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `test_fichero_real_sin_valores_de_estrategia` (registro) y `test_directorio_real_valida`
  (feedback) afirman que no hay valores de estrategia ni registros: se retiran en F11 y en la
  sesion 1.
- El reloj de servidor del broker es una aproximacion (`17:00 America/New_York`) hasta que F17
  lo mida contra el terminal de FundedNext; F11 debe declarar `dst_servidor` y `offset_base_servidor`.
  Verificado el 2026-09-05 (lectura de solo consulta al terminal MT5 build 6180 instalado en la
  maquina de desarrollo, cuenta demo MetaQuotes): EURUSD digits 5 / escala 100000; H4 de servidor
  en 12:00, 16:00, 20:00; ultimo tick del viernes 23:59:55 de servidor = 20:59 UTC = 17:00 Nueva
  York con GMT+3. VERIFICADO tambien en FundedNext (2026-09-05, cuenta demo 34891752, servidor
  `FundedNext-Server 3`, FundedNext Ltd, USD, apalancamiento 100, balance 100000, margen hedging=2):
  ultimo tick del viernes 23:59:45 de servidor = 20:59 UTC; H4 en 08/12/16/20 y D1 en 00:00 de
  servidor; la M1 del 2026-07-02 15:00 de servidor (= 12:00 UTC) vale o=1.14039 h=1.14042
  l=1.14030 c=1.14038 (tick_volume 83) frente a Dukascopy 114037/114043/114031/114036: diferencia
  de 1-2 puntos, misma alineacion horaria. Instrumento EURUSD en FundedNext (para F11 por ADR y
  F33 pre-vuelo): digits 5, point 1e-5, contrato 100000, lote 0.01/0.01/40, stops_level 0,
  freeze_level 0, filling 3 (FOK|IOC), expiration 15, ejecucion market, ruta Forex\EURUSD,
  spread 12 puntos con mercado cerrado. Queda por medir en invierno (GMT+2) en F17.
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.

## Open Questions
- Fuente de ticks historicos: decidir en F16.
- Ruta local de trabajo: C:/Users/USER/Desktop/Bot v3.

## Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado.
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

## Next Feature
F11 strategy-spec-schema. Entra con los 26 parametros que fija la sesion 1 (todos con registro de feedback, minuto y cita) y con `feedback apply`, diferido desde F09: el registro sigue en UNKNOWN hasta que F11 lo aplique. Golden H4 contra la pantalla del trader (regresion sobre F15): se escribe al fijar `anclaje_h4` con `ev-v6-005830-48b30e48`, teniendo en cuenta A-14 (fuera del horario de verano el anclaje puede no coincidir con las 17:00 de Nueva York).
## Next Action
1. Decidir las tres de A-13..A-17 que son del consultor y no del trader: A-15 (ampliar o no a Nueva York), A-16 (Oanda frente a Dukascopy para medir fidelidad) y A-17 (verificar la regla de noticias de FundedNext). A-13 y A-14 se MIDEN, no se preguntan.
2. Recibir del trader el backtest COMPLETO de mayo y junio de 2026 con el Excel (decision, hora, entrada, SL y TP por operacion). Se comprometio a enviarlo antes del sabado 2026-09-12 (v6 2:26:12). Eso sustituye al etiquetado a mano de los 16 dias `dev` de la hoja: son 40 casos sobre meses que NO ha visto (precondicion confirmada dos veces, 0:00:56 y 2:25:41). Ojo al matiz: los hara aplicando las reglas acordadas en la sesion, asi que sirven de patron oro para medir al bot, pero ya no miden si esas reglas capturan su juicio espontaneo.
3. Abrir F11 strategy-spec-schema con los 26 parametros que la sesion deja fijados y con `feedback apply` (diferido desde F09): el registro sigue en UNKNOWN hasta que F11 lo aplique.
4. Pendiente del usuario: borrar las ramas fusionadas `feature/F08-evidence-retrieval` y `feature/F10-elicitation-kit` con `!`.

## Last Stable Commit
1475956 · merge: sesion 1 con el trader procesada y validada por el usuario · tag stable/F10-sesion-01

## Change Log
- 2026-09-09 · SESION 1 VALIDADA por el usuario (acepto los 12 items de evidencia de v6). merge --no-ff a main (1475956); tag stable/F10-sesion-01. A-13..A-17 registradas. Siguiente: F11 strategy-spec-schema.
- 2026-09-09 · SESION 1 CON EL TRADER (2 h 27 min, video v6, paquete `2026-09-09-sesion-01`). El paquete se movio del 15 al 9 con `scripts/mover_sesion.py` (mismo seed, mismos 40 casos) y se commiteo ANTES de la sesion. Material: v6 inventariado, transcrito (tr-v6-...-7718b3f4, 2146 segmentos) y con fotogramas (fr-v6-22982c02, 8824), y la hoja de Word RELLENADA guardada en el corpus. 72 registros de feedback: 41 de la hoja, 5 aclaraciones del consultor y 26 con la voz del trader (minuto y cita). Las doce ambiguedades A-1..A-12 RESUELTAS, incluidas las tres bloqueantes: cartuchos 3 intentos (break even, entrada invalidada y reentrada no cuentan), break even al TOCAR, y anclaje H4 a las 23:00 de su grafico (UTC+2), verificado tambien en pantalla en fr-v6-22982c02/3585000. El stop queda en 0,8 FIJO de la caja con el lotaje sobre la caja completa (riesgo real 0,4 %), objetivo 1:3 sin extension, sin parciales, lunes a viernes, freno del dia por 3 perdidas y no por porcentaje. Correcciones del trader a lo que dabamos por sabido: NO deja de operar con el primer trade positivo, vuelve tras TRES perdidas, y no grabara su pantalla cada dia (pasara resumenes de backtest, lo que cambia la entrada de F26). Dos tramos de v6 declarados NO citables (0:41:00-0:50:11, acordado en voz que no va para la operativa; 1:53:30-1:57:31, video ajeno mientras el trader se ausenta) con guardia real en `evidence propose --check` y `evidence new`. Cinco propuestas de evidencia de v6 selladas (12 items) para las cinco dudas nuevas, pendientes de decision. Tests que afirmaban un estado ya superado, actualizados: feedback real vacio y corpus de cinco videos.
- 2026-09-08 · `scripts/mover_sesion.py`: mover la fecha de una sesion del kit en una sola orden. El id del paquete lleva la fecha dentro y el registro de feedback exige que la fecha de cada respuesta sea la de su sesion, asi que si la reunion se mueve el paquete hay que rehacerlo. Hacerlo a mano tiene una trampa: `kit build` pide el seed, y con otro seed salen dias distintos sin aviso. El script lo lee del paquete existente, comprueba despues que casos, reparto y preguntas son identicos, restaura el original si algo falla y se niega a mover una sesion que ya tenga registros de feedback. Tres tests (identidad al mover y al volver, negativa con LABEL_CASE, restauracion tras fallo).
- 2026-09-08 · Auditoria de codigo previa a la sesion 1, con dos agentes (generador de la hoja y kit; bugs latentes en todo el arbol). Bloqueantes de contenido en la hoja: la nota de una confirmacion rapida remitia a una pregunta `E-06` que ya no existia, y una linea del cierre imprimia `paquete <sesion>` sin sustituir. Bugs reales de codigo: (1) `kappa.etiquetas_de_registros` aplicaba `activos()` sobre los `LABEL_CASE` ya filtrados, asi que una etiqueta retirada con `BORDERLINE` o `MARK_FALSE_*` reaparecia viva y contaba en el kappa; (2) `validar_contra_contexto` no detectaba dos registros que superseden al MISMO registro, que deja dos activos contradictorios y solo asoma semanas despues al calcular el kappa. Endurecido ademas: `leer_yaml` centraliza la decodificacion (un .yaml guardado en cp1252 o UTF-16 sale como error de dominio, no como traceback; 16 cargadores migrados); `desktop.ini`, `Thumbs.db`, `.DS_Store` y `.gitkeep` dejan de invalidar knowledge/ (los crean solos Explorer y la sincronizacion de Drive); `_numero` acota los decimales del registro y explica `0,75` y `1%` en vez de ensenar las internals de `decimal`; `VelaInvalidaError` capturada en `kit build` y en la CLI; `cargar_manifiesto` del corpus ya no queda sombreado por el de datos en `knowledge validate`; el duplicado de feedback distingue mismo contenido de colision. Generador de la hoja: numeros de pregunta y bloqueantes derivados del paquete (los renumera `kit build`), la rejilla H4 se presenta como suposicion a confirmar, la ventana local se explica como grafico y no como horario de operativa, errores legibles en vez de traceback, saltos de linea que ya no pegan palabras, y un test de contrato nuevo (`test_hoja_sesion_docx`, 13 casos: OOXML valido, citas del paquete intactas, cada pregunta con caja, sin fuga de holdout).
- 2026-09-08 · Auditoria previa a la sesion 1 (rama `feature/F10-hoja-sesion-docx`): una simulacion del registro posterior a la sesion (18 respuestas representativas de la hoja contra `feedback new` sobre una copia del repo) descubrio que 7 de ellas NO se podian registrar porque no habia objeto al que apuntar. Arreglado: 6 parametros de negocio nuevos en el registro en UNKNOWN (`dias_operables`, `filtro_noticias`, `spread_maximo`, `perdida_maxima_diaria`, `perdida_maxima_semanal`, `comportamiento_sin_regla`) mas `instrumento` y `cuenta_objetivo`, con su fila en `mapa_parametros.yaml` y su contexto; tipo de objetivo `paquete` en F09 (CONFIRM/REJECT) para la precondicion de ceguera, que antes solo quedaba en el video, con la guardia de que el paquete confirmado sea el de la propia sesion; el test del registro exige la fuente por decision al VALOR y no al hueco UNKNOWN; el generador de la hoja comprueba antes de escribir que toda pregunta declarada tenga objetivo resoluble (`comprobar_objetivos`). Cuestionario del paquete regenerado: 21 -> 27 preguntas (mismo seed, mismas ventanas y particiones). Simulacion repetida: 21 de 21 registrables. ADR-0011 y `vistos.yaml` actualizados.
- 2026-09-08 · Hoja de respuestas de la sesion 1 en Word (rama `feature/F10-hoja-sesion-docx`): contexto humano de cada pregunta como dato versionado (`contexto_preguntas.yaml`, con acentos porque lo lee el trader) y generador `.docx` sin dependencias (OOXML a mano) con la confirmacion previa, las 21 preguntas con sus citas y caja de respuesta, y la tabla de etiquetado de los 16 casos dev; el binario queda fuera de git y declarado en la guardia de rutas ignoradas.
- 2026-09-08 · F10 VALIDADA por el usuario. merge --no-ff a main (4f8277e); tag stable/F10. Kit de la sesion 1 listo (paquete `2026-09-15-sesion-01`, fecha provisional). Siguiente: sesion 1 con el trader y despues F11.
- 2026-09-08 · F10 abierta y construida (rama `feature/F10-elicitation-kit`): brief con revision de diseno de agente (3 bloqueantes: julio y agosto ya vistos por el trader -> meses limpios 2026-05/06 descargados y confirmacion escrita previa; cifras de negocio del kit como datos en `knowledge/cases/kit/config.yaml`; etiqueta por sesion H4 con gramatica; 9 importantes y 6 menores aceptados); ADR-0011; `knowledge/spec/ambiguedades.yaml` (A-1..A-12 legibles por maquina, validadas contra evidencia y registro; test anti-deriva con esta tabla); registro pre-poblado con 23 parametros de estrategia mas en UNKNOWN (24 con `anclaje_h4`); paquete `cases` (ambiguedades, cuestionario con casos `ev-*`, ventanas de dias no vistos con hash y limites H4 por anclaje, particiones por hash con seed, kappa de Cohen desde los `LABEL_CASE`, paquete determinista); CLI `kit build|check|kappa`; `knowledge validate` capa kit (guardia de ancestro: particiones antes del primer LABEL_CASE); feedback valida `ambiguedad` contra el fichero y `t1` contra la duracion; grabaciones de sesion como videos sin `drive_id`. Paquete real `knowledge/cases/kit/2026-09-15-sesion-01/` (seed 20260915: 21 preguntas, 40 casos de un universo de 42 dias de mayo y junio de 2026 descargados hoy, 16 dev + 8 + 8 + 8); auditoria de cierre de codigo aplicada (asignacion inmutable tras el etiquetado, esquema estricto del paquete, huso validado, escritura atomica, build valida ambiguedades y usa items activos, mes anterior contiguo para el primer dia). Informe WAITING_FOR_USER_VALIDATION.
- 2026-09-08 · F08 VALIDADA por el usuario (confirmo el cierre tras la auditoria). merge --no-ff a main (5d8cf3c); tag stable/F08. FASE 1 CERRADA (F03-F08). Siguiente: abrir F10 elicitation-kit.
- 2026-09-08 · F08 abierta y construida (rama `feature/F08-evidence-retrieval`): brief con revision de diseno de agente (3 bloqueantes, 9 importantes, 9 menores aceptados: token de busqueda con acentos plegados y numeros normalizados, `buscar_secuencia` en vez de `localizar_cita` para la frase, `no_consta` fuera, capa `retrieval` entre `spec` y `feedback`, `dudas_de`/`cargar_capas` en `corpus`, `referencia_en` unica, rutas relativas, golden con y sin `data/`, fixture a mano, esquema JSON); ADR-0010 (+ enmiendas en ADR-0006 y ADR-0009); paquete `retrieval` y CLI `kb find | at`; golden de 15 consultas de referencia en verde (15/15 devuelven su item; `1:3` solo por la afirmacion: fallo lexico del ASR); `kb find` 1,04 s de pared. Auditoria de cierre aplicada (codigo: `--frase` acotada a 3 segmentos y buscando en cruda y corregida, `[corregida]` solo si difiere, `--margen-s inf` sin traceback, `dudas` no enteras ignoradas, `--frase`+`--prefijo` y `--tema`+`--solo cruda` son error, `--tema` contra `_temas.yaml`, `t0` real en contradicciones y fotograma, corregida ilegible = aviso, tests de supersede/carpeta fuera/determinismo de la CLI; docs: HANDOFF, MASTER_PLAN Change Log, deuda F04 iii cerrada, Next Feature F10). Informe WAITING_FOR_USER_VALIDATION.
- 2026-09-07 · F07 VALIDADA por el usuario (acepto los 341 items sin modificaciones, `fotograma visto` en los 7 de pantalla/ambas, recall humano de V4 0:05-0:15 sin faltas, tag `stable/F07`, golden H4 a F10; confirmo el cierre tras la auditoria). merge --no-ff a main (f0c280b); tag stable/F07. Siguiente: abrir F08 evidence-retrieval.
- 2026-09-07 · F07 ronda 2: el usuario acepto los 341 items sin modificaciones (7 de pantalla/ambas con `fotograma visto`; recall humano de V4 0:05-0:15: ninguna frase faltaba; tag `stable/F07`; golden H4 sobre F15 pasa a F10). `evidence accept` x341 (0 fallos; `revisado_por` "Aleks · hoja F07 2026-09-07 · cruda leida|fotograma visto"), evidencia commiteada (ff13e7a), 20 propuestas con decision (0 pendientes), `_contradicciones.yaml` regenerado (1 abierta: `stop.nivel` 0,75 vs 0,8 = A-10), golden `test_golden_citas_f07` 40/40 en verde, hechos y ambiguedades A-1..A-12 con ids de evidencia. Auditoria de cierre (2 agentes) aplicada: docs (HANDOFF, PROJECT_STATE, MASTER_PLAN filas H/H.2/tabla A y B, ADR-0009 en el indice, deuda de F07 cerrada o con dueno, hook local reinstalado con `make hooks`) y codigo/tests (1 bloqueante: `test_directorio_real_valida` sin contexto rompia con los 7 items de pantalla; localizacion que prueba todas las apariciones de la frase; `hueco_ms` con aviso a partir de 15 s (41 items aceptados lo superan, maximo 44 s); palabras parciales al final del segmento alineadas (1 item); sello ampliado a la cabecera y 20 propuestas re-selladas; `validate` cruza cada decision con la evidencia; `accept` atomico y sin manifiesto; cabecera invalida sin traceback; audio no admite `fotograma_visto`; 8 tests nuevos). 311 funciones / 456 casos. Informe WAITING_FOR_USER_VALIDATION (ronda 2: confirmacion de cierre).
- 2026-09-06 · F07 ronda 1 construida (rama `feature/F07-evidence-extraction`; brief con revision de diseno de agente: 6 bloqueantes aplicados, entre ellos `evidence` sin importar `corpus`, comodin `[...]` en vez de la elipsis del ASR, tiempo real por `palabras`, `material_adicional` solo desde un tramo de video, `revisado_por` con metodo, sello `salida_sha256`): verificacion mecanica de citas (tokens, TOL 2 s), campo `transcripcion`, referencias `fr-*` obligatorias en pantalla, contexto compuesto en `validation`, propuestas trazables con guardias de calidad, CLI `propose|--check|accept|reject|list`, `_temas.yaml`, `PROMPT.md`, ADR-0009, golden cerrado (40 referencias) y contrato; 20 propuestas para los 5 videos (341 items, 91 `no_consta`, 42 marcas heredadas re-citadas) con `--check` en verde; hoja de revision HTML por script. Medicion V4 0:05-0:15: 7 referencias cerradas, 7 cubiertas, 22 items, todos en verde; recall humano en la ronda 2. Ningun item escrito en `knowledge/evidence/`. Informe WAITING_FOR_USER_VALIDATION (ronda 1).
- 2026-09-06 · PREVIOS DE F07 VALIDADOS por el usuario (ratifico las 4 decisiones: hotwords descartado, 6 sustituciones de segmento, Drive completo con drive_id de v5, tag stable/F05-previos-F07 con §F ampliado). merge --no-ff a main (8cba5c5); tag stable/F05-previos-F07. Siguiente: abrir F07.
- 2026-09-06 · PREVIOS DE F07 construidos (rama `feature/F07-previos`, commits b9ffd0d, 13b4e40, 627d90d): glosario v2 aprobado por el usuario (29 terminos, 6 globales + 6 de segmento sobre los ids nuevos); huella de reanudacion sin GPU/driver; guardia de 223 tokens del prompt; `hotwords` MEDIDO y DESCARTADO (sobre v5 alargo los segmentos hasta 40 s, la pasada oficial perdio ~10 s con "protejo a 0.80, SL por defecto" y transcribio "sell" como "SL" en 2 de 2 pasadas; `initial_prompt` no mostro nada de eso; ADR-0007 enmienda); los 5 videos retranscritos (~1 h de GPU; ids `bbd8a931`, `28391c2c`, `270a4851`, `a8d1bccc`, `3c6fbb57`; contenido conservado: ratio de palabras 0,958-1,000, hechos clave presentes, senales comparables); Drive: carpeta `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R` con SHA256SUMS/LEEME/manifiestos por API; crudas, WAV y v5 en `data/drive_staging/` pendientes del usuario. Auditoria de cierre (2 agentes) aplicada: recuento del prompt como el motor (96, no 99; `add_special_tokens=False`), `initial_prompt_tokens` fuera de la huella, guardia antes de cargar la GPU, tests de `_carpeta_base_registrada_ajena`, anexos de la medicion en `docs/validation/anexos/F07-previos/`, tag `stable/F05-previos-F07` y §F ampliado. Informe WAITING_FOR_USER_VALIDATION. 2026-09-06: el usuario subio los 21 ficheros de `drive_staging/` a Drive (verificado por API) y valido las 4 decisiones; `drive_id` de v5 anotado.
- 2026-09-06 · AUDITORIA GLOBAL VALIDADA por el usuario (ratifico las tres: regla del HANDOFF en la rama y nunca en main tras el tag; cierre de la auditoria como rama con tag `stable/F05-auditoria-1`; orden de los previos de F07: glosario v2 -> retranscribir 5 videos -> copia de crudas y WAV en Drive -> v5 en Drive -> abrir F07). merge --no-ff a main (916d0d0); tag stable/F05-auditoria-1.
- 2026-09-05 · AUDITORIA GLOBAL de la estructura (rama `feature/F05-auditoria-estructura`, 2 agentes) aplicada: codigo (`corpus/trabajo.py` con las guardias de F05 tambien en `corpus transcribe`: sin ella retranscribir en un clon sin `data/` pisaba la cruda; una transcripcion activa por video; `parse_ms` estricto; glosario rechaza `.` sin escapar; WAV/YAML corruptos y `corpus check` sin `fichero` ya no dan traceback; `carpeta_datos` unica; `--margen-s` negativo; `TOLERANCIA_DURACION_S` unica; mensaje de `state check` con el ritual) y docs/proceso (regla del HANDOFF en la rama, incidente de CI registrado, fila H.2 "Previos y entradas de F07", 5 videos, fotogramas en §0/B/ADR-0001/READMEs, lineamientos separados de hechos, Change Logs ordenados, `ci.yml` sin cancelar en main, test de rutas de Important Files). 389 casos, make check verde. Informe `docs/validation/AUDITORIA-2026-09-05-estructura.md`.
- 2026-09-05 · Incidente de CI en main: el commit `docs(handoff)` f452e6f (tras `stable/F05`) puso `state check` y la CI en rojo (run 34000376588) porque en main solo puede cambiar PROJECT_STATE.md tras el tag; revertido en de42ec1 (run 34000499649 verde). El `docs(state)` c97273f quedo cancelado por `cancel-in-progress` (run 34000351246) y su `make check` es local. El `docs(handoff)` de F04 (3b754f1) tambien estaba en rojo (run 33988126976) sin registro: main estuvo en rojo del 2026-09-05 19:46Z al 2026-09-06 00:08Z. Regla escrita en MASTER_PLAN §F: el HANDOFF se actualiza en la rama. Rama `feature/F05-auditoria-estructura` abierta a peticion del usuario para una auditoria global antes de F07.
- 2026-09-05 · F05 VALIDADA por el usuario (acepto las cuatro decisiones: cobertura completa a 1 fps sin perdida, Excel y ficha de Word hacia F07 y F10, sin copia de fotogramas en Drive, candidatos A-9 hacia F07). merge --no-ff a main (dd8de55); tag stable/F05. Pregunta del usuario respondida: las decisiones y la lista de obligatorios son modificables; los manifiestos no se editan, se reemplazan.
- 2026-09-05 · Material adicional del usuario ("Info extra de backtesting") integrado en el corpus por su instruccion antes de validar F05: v5 (`2026-09-05 21-03-59.mkv`, 365 s, FXReplay abril; transcrito `tr-v5-...-01a1ae03`, 99 segmentos; fotogramas `fr-v5-718ecabb`, 366), xlsx abril 2026 (38 operaciones) y 6 capturas de Analytics como `material_adicional`; `fuentes.yaml` y `manifest.yaml` (5 videos); hechos en Lineamientos (0,8 "SL por defecto", reentrada tras equal, RR sobre 1 %, 1:3 con 1:4 futuro, backtest abril 47 %/PF 4,01). Deuda: subir v5 a Drive.
- 2026-09-05 · F05 construida (ADR-0008): brief con revision de diseno por agente (7 bloqueantes aplicados: `fps=1` elegia el fotograma en n+0,47 s y reescribia el `pts`; `huecos` vacuo; referencias heredadas citables; "cinco obligatorios"; salidas incompletas; test AST inviable) y decision del usuario (maxima fidelidad sin restriccion de recursos: cobertura completa a 1 fps en PNG sin perdida, cambio de la tabla A). Cuatro videos extraidos (16 182 fotogramas, 8,9 GiB, ~11 min, `huecos: []`), determinismo 80/80 por `-ss -copyts`, obligatorios legibles (Excel 2,83/3,3; 4,08/3,94; 1,19537), candidatos A-9 y ficha de reglas en Word (V3 0:01:41) como hechos para F07. Informe WAITING_FOR_USER_VALIDATION. Auditoria de cierre (2 agentes) aplicada: A1 carpeta de trabajo decidida tambien por los manifiestos (otra build/maquina ya no es callejon sin salida), A2 `segundos_ausentes_ms` (referencias solo a fotogramas que existen; sin el campo, cobertura densa obligatoria), A3 `start_time != 0` rechazado, YAML estricto en guardias, `show` acotado por duracion; docs: resolucion v4, 8,9 GiB, Change Regimes con corpus/fotogramas, brief anotado, READMEs. CI rama: run 33992054088 verde (pre-auditoria) y run 33992911952 verde sobre a118352 (cierre).
- 2026-09-05 · F04 VALIDADA por el usuario (decisiones: A-12 queda como pregunta al trader; glosario v2 como paso previo a F07 con retranscripcion de los 4 videos; constantes de corte tecnicas; lo heredado de Whisper tiny no se cita). Commit de docs de la auditoria final reescrito con trailer `Fuente: ADR-0005` (tocaba knowledge/spec/README.md; CI lo detecto: run 33985993346 rojo, 33986995223 verde). merge --no-ff a main (a7f8b4b); tag stable/F04
- 2026-09-05 · AUDITORIA FINAL previa a validar F04 (2 agentes: bugs de codigo y estructura del plan). Codigo: `sha256_video` entra en la huella de la carpeta de trabajo (un video cambiado ya no reescribe el WAV ni falla tras la GPU con "motor no determinista"), cita de un instante en el borde exacto de un segmento, comodines cuantificados (`\\w+`, `\\d+`) rechazados en el glosario, `glossary apply --video` con video inexistente es error, temporal del manifiesto con prefijo `_` (no rompe `check` si queda huerfano), borde de fragmento con 1 ms de redondeo no cuenta como recorte, `cargar_todos` detecta ids repetidos y ciclos, asercion vacia de un test corregida. Docs: regimenes de cambio completos (manifiestos de datos y transcripciones), deuda tecnica de F04 con dueno (huella GPU, initial_prompt, palabras bajo corregida, hallazgo V4 1:28:20, fotogramas obligatorios de F05), regla de cita de F07 contra la cruda y secuencia glosario v2 -> retranscribir -> Drive -> F07, F05 depende de F04, plantillas de brief e informe con revision de diseno, auditoria de cierre y decisiones del usuario, MASTER_PLAN §F con el metodo supervisado, A-1..A-12, 33 marcas, Change Log del plan al dia; HANDOFF y READMEs alineados
- 2026-09-05 · F04 construida y auditada: cuatro videos transcritos con large-v3 (403 + 854 + 1031 + 1645 segmentos, cero cortes forzados, cero recortes), manifiestos inmutables tr-v1-...-00fcaf53, tr-v2-...-ac6b337b, tr-v3-...-570a315f, tr-v4-...-3f8c826e; determinismo verificado retranscribiendo un fragmento; 33 marcas heredadas revisadas (28 coinciden, 3 eran fotogramas, 2 con cifra distinta: 40/50 % y 2,3/2.83); auditoria de cierre sin agentes (limite de sesion) con 5 correcciones; hook sin resync; informe WAITING_FOR_USER_VALIDATION. CI verde: 3f73813 (run 33946879078), d1f3947 (33948083299), 69ea773 (33966530552)
- 2026-09-05 · AUDITORIA GENERAL de F04 (2 agentes: codigo/tests y docs/proceso) aplicada en la misma rama. Codigo: solape de milisegundos entre segmentos de Whisper se recorta y cuenta (antes abortaba tras la GPU), palabra con fin < inicio se iguala, reemplazo del glosario LITERAL (no plantilla de re.sub), alternancias envueltas en limites de palabra, nombre de motor validado antes de trabajar, `--reemplaza-a` comprobado antes de la GPU y del mismo video, manifiesto escrito atomicamente y con `reemplaza_a` inmutable, esquema del manifiesto valida fragmentos contiguos, duraciones, senales, huecos y cortes forzados, `comprobar` recomputa ms_con_habla/senales/huecos desde la cruda, carpeta por huella (`<motor>-<huella8>`) para retranscribir sin pisar la cruda anterior, WAV reextraido si cambia el video, sha256 del video por bloques, errores de CLI sin traceback, tests que no probaban lo que decian corregidos, ffmpeg obligatorio en CI. Docs: PROJECT_STATE (waiting, componentes, ADR-0007, A-12, deuda), READMEs de knowledge/scripts/hooks, MASTER_PLAN (tabla B, H.2 F07), brief y informe coherentes (33 marcas, margen 75 s), notas en ADR-0003/0005.
- 2026-09-05 · F04 en construccion: brief revisado por agente (8 hallazgos de fondo aceptados: muestras enteras, corte con min/max y forzados, glosario Unicode de dos alcances, manifiesto inmutable por transcripcion, corregida por recomputo, data/ para lo pesado, VAD y senales, vocabulario como initial_prompt); ADR-0007; faster-whisper large-v3 en la GTX 1650 a 3,6x tiempo real (grupo de dependencias `asr`); pipeline reanudable con motor falso testeado de extremo a extremo
- 2026-09-05 · ramas feature/F01-F15 fusionadas borradas (local y origin); rama feature/F04-transcription-pipeline abierta
- 2026-09-05 · cuenta demo FundedNext conectada en el MT5 de esta maquina; lectura de solo consulta: reloj de servidor GMT+3 con cierre 17:00 NY (decision 2 de F15 verificada en el broker real), escala 100000, M1 del 2026-07-02 coincide con Dukascopy a 1-2 puntos, parametros de instrumento/broker anotados en Technical Debt para F11/F33
- 2026-09-05 · MT5 instalado en la maquina de desarrollo (terminal build 6180, demo MetaQuotes conectada); lectura de solo consulta confirma escala 100000 y reloj de servidor GMT+3 con cierre a las 17:00 NY (decision 2 de F15 verificada en MetaQuotes-Demo; FundedNext pendiente). El adaptador MT5 (F17/F33) puede desarrollarse aqui
- 2026-09-04 · F15 VALIDADA por el usuario (con auditoria de arquitectura y de proceso previas); merge --no-ff a main (11ee1ac); tag stable/F15
- 2026-09-04 · F15 auditoria de arquitectura (agente) antes de fusionar: ADR-0006 (contrato de capas revisado para F25/F26/F30/F32, paquete comun con yaml_estricto/historial/documentos/ids/husos, accesores del registro por tipo declarado, SerieVelas.origen + ventana por instante + agregar_serie, validador de knowledge fuera del CLI, test AST sin float/Decimal en domain, test de accesores del registro); auditoria de proceso (agente): ritual de cierre reescrito con el orden real, cifras del informe corregidas, seccion "que debe decidir el usuario". 324 casos, 210 funciones
- 2026-09-04 · F15: auditoria de cierre aplicada (2 agentes), tres datasets reales congelados (ene/jul/ago 2026: 30150/32774/30257 velas M1) con manifiestos inmutables; H4 real del 2026-07-02 = goldens; CI verde (runs 33917006801, 33918894784); WAITING_FOR_USER_VALIDATION
- 2026-09-04 · REVISION GLOBAL de alineacion con las 8 fases (tras F15): sin bloqueos hacia F04-F33. Verificado: contrato de capas admite engine->data/domain, spec->config, cases->data; domain/velas.py sin float/Decimal (F18); tipos del registro y papeles del corpus ampliables sin romper (F10/F11); commits_sin_fuente listo para F11; cargar_serie con ventana para F14; regla de anclaje escrita en ADR-0005 para exportar en F29; ritual de merge/tag coincide con git log; main cumple state check. Pendientes conocidos: retirar en F11/sesion 1 los tests que afirman registro sin valores y feedback vacio; borrar ramas feature/F01-F09 fusionadas (decision del usuario); reloj de servidor aproximado hasta F17
- 2026-09-04 · F15 construida con revision de diseno previa por agente (brief corregido: sin velas de 3/5 h en datos reales, Vela en domain sin Decimal, huso_datos fuera del registro, id de dataset por hash, velas de borde `completa`); domain/velas, data/{velas,agregacion,dukascopy,dataset}, CLI data, 16 fixtures reales bi5, goldens H4 del 2026-07-02, hook y validate sobre data/manifests; ADR-0005; parametros huso_operativa (CONFIRMED) y anclaje_h4 (UNKNOWN, A-9)
- 2026-09-04 · rama feature/F15-market-data-ohlc abierta; brief y ADR-0005 (fuente Dukascopy M1 publica, precios enteros en puntos, tres relojes, anclaje por reloj de pared)
- 2026-09-04 · F09 VALIDADA por el usuario; merge --no-ff a main (2ff6450); tag stable/F09; proteccion de rama main activada en GitHub (enforce_admins, sin force-push ni borrado)
- 2026-09-04 · push de la auditoria de cierre (e99afba, con trailer Fuente: ADR-0002, ADR-0004 por tocar el comentario de parametros.yaml); CI Ubuntu verde (run 33912550454); Python 3.12 en local y CI
- 2026-09-04 · AUDITORIA DE CIERRE de F09 (3 agentes: codigo, plan/docs, infraestructura), antes de la validacion del usuario. Corregido: campos en blanco rompian el id de feedback/evidencia; `Fuente: ADR-9999` pasaba; detector de literales de negocio eludible; KeyError con `--sesion ""`; `feedback new`/`evidence new` validan contexto antes de escribir; fechas imposibles y digitos Unicode; supersede cruzado y ciclos; ficheros no-yaml; tracebacks con manifiesto/TOML/YAML corruptos; ancla por SHA con tag vigilado; clon superficial y repo anidado no evaluables; registro estricto (texto vacio, claves ajenas, limites en hora); instalador de hooks (worktree, hooksPath global, .bak, git ausente); hook con `uv run --locked`; `.python-version` 3.12; CI con permisos, concurrencia, timeout y ffprobe obligatorio; tests de integridad no eludibles; `feedback pending` filtra por `estrategia` (ADR-0004); docs coherentes (ejemplo del informe, H.2 anclaje H4, mapa de ambiguedades, READMEs). Un agente ejecuto por error una prueba en el repo real (rama `prueba/soft`, creada y borrada; solo quedan entradas de reflog)
- 2026-09-04 · push de la auditoria extrema (8 commits); CI Ubuntu verde (run 33909186793, d217a11); clon sin tags OK por ancla SHA, clon superficial ERROR explicito
- 2026-09-04 · AUDITORIA EXTREMA (3 agentes: codigo, plan/ejecucion, repositorio). Corregido: git decodificado en UTF-8 con quotepath=false (un commit con mayuscula acentuada anulaba la guardia de trailers en Windows); adiciones en commits de merge protegidas (`git log -m`); video_id y formato de id validados, `evidence new` contra fuentes.yaml; hook con rutas sin entrecomillar y tabulador; cargador YAML estricto (claves duplicadas, fechas como texto, tipos texto exigidos); InvalidOperation/NaN/Infinity/25:99 rechazados; guardias no evaluables son ERROR y el ancla de trazabilidad tiene tag + SHA; `state check` vigila que main solo cambie PROJECT_STATE tras el tag; corpus check sin KeyError; `make hooks` portable (Python) desde PowerShell; CI sin doble disparo, tags forzados, actions al dia; ADR-0004 (categorias de parametro, horas con huso, tzdata); lecturas ambiguas sin crecer por tick; contradicciones con Decimal; feedback con fecha = sesion y t0/t1 siempre validados; MASTER_PLAN H.2 con los riesgos de ejecucion absorbidos por funcionalidad; ambiguedades numeradas A-1..A-11; docs incoherentes corregidos. 122 funciones / 167 casos
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
- 2026-09-04 · segunda auditoria: Last Stable Commit corregido (era 0b43244, main esta en 7baa27d), Next Feature = F02, brief de F01 y README actualizados
- 2026-09-04 · tercera auditoria: hook con modo 100755 en el indice, READMEs en todas las carpetas (sin exenciones), holdout/{1,2,3} fisico, mypy strict sobre tests
- 2026-09-04 · pruebas cruzadas: clon limpio, autocrlf=true, HEAD separado, PowerShell 7, Python 3.13 verdes; Linux pendiente del primer push. HALLAZGO: core.hooksPath relativo omitia el hook en main (sin el fichero); make hooks ahora copia a .git/hooks. Reprobado OK
- 2026-09-04 · push de la rama F01 autorizado; CI Ubuntu verde (run 33880866257). Linux verificado
- 2026-09-04 · F01 corregida: .gitattributes, tests de integridad del indice, hook anti-main, uv --locked; 26 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · auditoria de fases (docs/plan/AUDITORIA_FASES_2026-09-04.html): 4 criticos, 19 huecos; plan ampliado (MASTER_PLAN.md seccion H)
- 2026-09-03 · F01 construida; make check verde (21 tests, 3 contratos); WAITING_FOR_USER_VALIDATION
- 2026-09-03 · plan aprobado por el usuario · rama feature/F01-project-scaffold abierta · paquete botsito
- 2026-09-03 · repositorio inicializado en local · punto cero con documentacion · plan pendiente de validacion
