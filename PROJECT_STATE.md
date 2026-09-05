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
1. Leer este fichero. 2. Leer `docs/plan/features/<Current Feature>.md` y `docs/HANDOFF.md` (contexto humano de la ultima sesion). 3. `make check` (desde F01).
4. Si `Current Feature` está WAITING_FOR_USER_VALIDATION: no avanzar; preguntar.

## Change Regimes (must be respected)
- knowledge/evidence/  → INMUTABLE tras commit (hook). Corrección = nuevo item que supersede.
- knowledge/feedback/  → SOLO AÑADIR. Nunca editar un registro.
- knowledge/spec/, knowledge/cases/ → versionados; cada cambio de valor cita evidence-id o feedback-id.
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; prohibido leer desde src/botsito/spec y src/botsito/domain (guarda en tests); cada una se abre una sola vez.
- src/botsito/domain/ → sin IO, sin reloj, sin MetaTrader (import-linter).
- data/manifests/ y knowledge/corpus/transcripciones/ → INMUTABLES tras commit (hook + historial de git; ADR-0005 y ADR-0007). Corrección = manifiesto nuevo con `reemplaza_a`.

## Current Phase
FASE 1 · Base de conocimiento (F03-F08); F09 (fase 2) y F15 (fase 4) ya integradas por el orden E

## Current Feature
— (F04 integrada; F05 pendiente de abrir)

## Current Branch
main

## Stable Main State
a7f8b4b · merge de F04. make check verde: 359 casos (236 funciones), 4 contratos, mypy strict, state/config/knowledge validate (3 manifiestos de datos, 4 de transcripcion). CI Ubuntu verde en la rama (run 33986995223). Tag stable/F04. Rama main protegida en GitHub.

## Completed Phases
- FASE 0 · Fundamentos (F01, F02) · cerrada el 2026-09-04 en dc3384d · puerta: make check verde en main; registro de parametros con tipos y lectura estricta; .gitattributes y cero CRLF; hooks copiados por make sync; tags stable/F01 y stable/F02; CI Linux verde

## Completed Features
- F01 · project-scaffold · validada el 2026-09-04 · docs/validation/F01-project-scaffold.md · tag stable/F01
- F02 · config-and-parameter-registry · validada el 2026-09-04 · docs/validation/F02-config-and-parameter-registry.md · tag stable/F02
- F03 · corpus-inventory · validada el 2026-09-04 · docs/validation/F03-corpus-inventory.md · tag stable/F03
- F06 · evidence-model · validada el 2026-09-04 · docs/validation/F06-evidence-model.md · tag stable/F06
- F09 · expert-feedback-model · validada el 2026-09-04 · docs/validation/F09-expert-feedback-model.md · tag stable/F09
- F15 · market-data-ohlc · validada el 2026-09-04 · docs/validation/F15-market-data-ohlc.md · tag stable/F15
- F04 · transcription-pipeline · validada el 2026-09-05 · docs/validation/F04-transcription-pipeline.md · tag stable/F04

## Features Waiting for Validation
—

## Existing Components
- Paquete `botsito`: `domain/valores.py` (Fraccion, Porcentaje sobre Decimal, no intercambiables; HoraLocal con huso); `config/registro.py` (registro de parametros con categoria, procedencia y lectura estricta; vacio de valores); `config/ajustes.py` (entorno y rutas, sin claves de negocio).
- CLI: `state check` (rama, recuento de tests, tag estable, informes de validacion, main sin cambios tras el tag), `knowledge validate` (registro, manifiesto, evidencia, contradicciones, feedback, historial de git y trailers `Fuente:`), `config validate` (ajustes contra el registro), `corpus inventory` y `corpus check`.
- `corpus/inventario.py`: manifiesto del corpus con SHA-256, ffprobe, papel y huecos de fotogramas heredados. `knowledge/corpus/{fuentes,manifest}.yaml`.
- `evidence/{modelo,contradicciones}.py` + `comun/historial.py`: EvidenceItem inmutable (id con hash), contradicciones regeneradas, guardia de historial de git. CLI `evidence new` / `evidence contradictions`. Hook rechaza editar o borrar evidencia y feedback.
- `feedback/modelo.py`: FeedbackRecord solo-anadir (id por hash, coherencia accion/objetivo, trazabilidad, supersede del mismo objetivo sin ciclos); CLI `feedback new` (valida contexto antes de escribir), `trace`, `pending` (filtra parametros no `estrategia`); `commits_sin_fuente` exige trailer `Fuente:` con ids existentes (evidencia, feedback, ADR) en commits que tocan spec/cases desde el SHA de stable/F06; `historial_evaluable` marca clon superficial o repo anidado como no evaluable.
- Contratos de importacion (import-linter + test AST; `domain` no importa `config`). Test de literales de negocio con lista real. Tests de integridad del indice.
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- `domain/velas.py` (F15): `Vela` (MinutoUtc, Puntos, volumen entero, duracion, n_m1, completa), `SerieVelas`, `combinar`; sin datetime/float/Decimal. `data/velas.py` (CSV determinista), `data/agregacion.py` (particion UTC por reloj de pared, ADR-0005), `data/dukascopy.py` (bi5, red inyectada, planas descartadas), `data/dataset.py` (dataset congelado, manifiesto inmutable con id por hash, `cargar_serie` con ventana). CLI `data download/check/aggregate`. Hook y `knowledge validate` protegen `data/manifests/`.
- Paquete `comun/` (ADR-0006, por encima de `domain`): `yaml_estricto.py` (claves duplicadas y no hashables rechazadas, fechas como texto), `historial.py` (guardia de git para evidencia, feedback y manifiestos; trailers Fuente), `documentos.py` (normalizacion, vacios, hash corto, directorios, supersede, activos), `ids.py` (todos los formatos de id), `husos.py` (nombre IANA canonico, un criterio para registro y datos). `validation/knowledge.py`: orquestador de `knowledge validate` (F12 y F14 anaden capas ahi); la CLI solo imprime. Registro: accesores por tipo declarado; test de contrato que vigila `registro.<accesor>("nombre")` en src/. Contrato de capas: cli > validation > viewer/mql5bridge > engine > cases > spec > feedback > evidencia/corpus/data/config > comun > domain. `scripts/instalar_hooks.py` (make hooks portable; destino `git rev-parse --git-path hooks`; aborta con `core.hooksPath` global). `.python-version` = 3.12 (local y CI).
- `corpus/{audio,transcripcion,motor_whisper,glosario,pipeline_transcripcion,manifiestos_transcripcion}.py` (F04, ADR-0007): WAV por video y corte por muestras en silencios, segmentos en ms enteros con senales, faster-whisper solo en `motor_whisper`, glosario de dos alcances, pipeline reanudable con manifiesto INMUTABLE `tr-<video>-<motor>-<hash8>` en `knowledge/corpus/transcripciones/`, corregida = cruda + glosario verificada por recomputo. CLI `corpus transcribe | glossary apply | transcript check | transcript show`; capa en `knowledge validate`; hook protege el directorio.
- Plantillas: brief, ADR, informe de validacion. ADR-0001 a 0007. `.gitattributes` con LF (`*.bi5` binario).

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- knowledge/evidence/README.md (esquema de EvidenceItem) · src/botsito/evidence/modelo.py
- knowledge/feedback/README.md (esquema de FeedbackRecord y plantilla de sesion) · src/botsito/feedback/modelo.py · src/botsito/evidence/historial.py
- knowledge/corpus/fuentes.yaml (fuentes esperadas, ids de Drive) · knowledge/corpus/manifest.yaml (GENERADO) · src/botsito/corpus/inventario.py
- knowledge/spec/parametros.yaml (LA puerta de los parametros; solo `huso_operativa` CONFIRMED por ADR-0005 y `anclaje_h4` UNKNOWN hasta F11) · src/botsito/config/registro.py · src/botsito/domain/valores.py
- docs/adr/0005-datos-de-mercado-fuente-formato-y-relojes.md · data/manifests/README.md (esquema del manifiesto) · src/botsito/data/agregacion.py (regla de anclaje) · tests/fixtures/ohlc/README.md (fixtures reales con sha256)
- docs/adr/0007-transcripcion-en-dos-capas.md · knowledge/corpus/glosario_asr.yaml (manual, versionado) · knowledge/corpus/transcripciones/ (INMUTABLE) · src/botsito/corpus/pipeline_transcripcion.py · docs/validation/F04-transcription-pipeline.md
- docs/plan/features/F02-config-and-parameter-registry.md · docs/validation/F02-config-and-parameter-registry.md
- docs/adr/0002-registro-de-parametros-una-sola-puerta.md · docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
- docs/plan/AUDITORIA_FASES_2026-09-04.html · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
236 funciones de test (parametrizadas x3, x6, x7, x8, x9, x11, x13, x15, x18, x19 y x22) · unit: project_state, adr, tree, cli, cli_data, valores, velas, registro, ajustes, inventario, evidence, feedback, yaml_estricto, dukascopy, agregacion, agregacion_dst, dataset, golden_ohlc, comun, audio, transcripcion, pipeline_transcripcion · contract: import_contracts, no_business_literals, repository_integrity, registro_accessors, evidence_history, feedback_history, data_manifest_history, transcripcion_history · 4 contratos import-linter KEPT · mypy strict OK (src + tests)

## Architectural Decisions (index)
- ADR-0001 estructura del repositorio y regimenes de cambio — ACTIVE
- ADR-0002 registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta — ACTIVE
- ADR-0003 hooks copiados desde scripts/git-hooks; sin framework pre-commit — ACTIVE
- ADR-0004 categorias de parametro y horas con huso — ACTIVE
- ADR-0005 datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje — ACTIVE
- ADR-0006 capas revisadas, paquete `comun` y accesores del registro por tipo declarado — ACTIVE
- ADR-0007 transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario — ACTIVE

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
  - Hallazgo F04 (2026-09-05, large-v3): en V1 0:15:59 el trader dice "ya ha pasado mas del 50%
    de la vela" (la transcripcion heredada decia 40 %) y en V1 0:16:51 "de pasar de 0.75 es a
    0.50". La cifra 40 % frente a 50 % es la ambiguedad A-12 (sesion 1).
  - Preguntas abiertas para el trader (sesion 1): (a) ¿el 0,8 es fijo o "0,75 mas el spread del
    momento"? (b) ¿el stop se coloca en el 0,75 al enviar la orden limite o solo tras el llenado?
    Para el bot es equivalente y mas seguro adjuntar el SL al 0,75 en la propia orden pendiente
    (F22/F31); confirmar que el trader no ve inconveniente.
  - Consecuencia para F21: el TP nunca se recalcula al mover el SL (invariante a probar).

## Expert Validations
—

## Known Ambiguities
Todas ABIERTAS hasta un registro de feedback del trader (sesion 1, tras F10 + F15). El esquema de
feedback solo acepta ids `A-N`. Columna "resuelve en": la funcionalidad que convierte la respuesta
en regla o parametro; "pregunta": lo que se le plantea al trader.

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
| A-9 | anclaje de la vela H4 (hora y huso del grafico) | F07 (captura), F11 (valor y `huso` de `anclaje_h4`, creado UNKNOWN en F15) | ¿a que hora y en que huso del grafico abre su H4? (se resuelve viendo su grafico) |
| A-10 | stop a 0,8: fijo o 0,75 + spread | F21 | ¿el 0,8 es fijo o "0,75 mas el spread del momento"? |
| A-11 | SL en la orden o tras el llenado | F22, F31 | ¿el SL va en la orden pendiente o se pone tras el llenado? |
| A-12 | porcentaje de vela transcurrido para bajar la proteccion a 0,50: 40 % (transcripcion heredada) o 50 % (large-v3, V1 0:15:59) | F21 | ¿a partir de que parte de la vela bajas el stop a 0,50? |

Las 3 preguntas bloqueantes de la sesion 1 (MASTER_PLAN G) se eligen en el brief de F10 con los
casos delante; candidatas por impacto en el kit: A-9 (afecta a todos los casos), A-2 y A-4.

## Known Contradictions
Cartuchos 2 (ficha) vs 3 (V4 0:48:41) · parciales 30–40 % (ficha) vs "sin parciales" (respuesta) ·
BE al tocar vs al cierre (V4 0:44:56) · salida anticipada sí/no (V4 1:08:18 / 1:08:30)

## Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; `escribir_item` trata la colision como "mismo contenido" (revisar en F07).

## Technical Debt
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de `data/transcripciones/<v>/large-v3-int8-float16/cruda.jsonl` (y `audio.wav`) fuera de esta maquina (Drive) con su sha256 del manifiesto; dueno: usuario, antes de abrir F07. Sin ella, otra maquina solo valida esquema e historial (o retranscribe: ~1 h de GPU).
- Glosario ASR v2: sustituciones e ids propuestos en el informe F04 ("Que debe decidir el usuario", punto 2). Cambiar `vocabulario` cambia el `initial_prompt` y la huella: exige retranscribir los 4 videos con ids nuevos (`reemplaza_a`), decidirlo ANTES de que F07 cite ids de transcripcion; las `sustituciones` no obligan a retranscribir (solo `corpus glossary apply`).
- V3 0:28:56: las cifras del Excel (2,3/3,23 heredadas frente a 2.83/3.33 de large-v3) las decide el fotograma en F05; igual V2 0:33:21 (4,08/3,94) y V4 0:12:30 (1,19537): las tres marcas "no verificables por audio" del informe F04 son fotogramas obligatorios de F05.
- F04, pendientes tecnicos declarados en el informe: (i) la huella de reanudacion incluye GPU/driver (excluirlos al retranscribir para el glosario v2; cambiarla ahora invalidaria los parciales); (ii) faster-whisper trunca el `initial_prompt` a ~224 tokens sin aviso y, con `condition_on_previous_text=False`, solo condiciona la primera ventana de cada fragmento (medir y valorar `hotwords` antes del glosario v2; cambia la huella); (iii) `palabras` de la cruda quedan bajo un texto corregido sin marcar (F07 cita palabras solo desde la capa cruda). Dueno: (i) y (ii) la retranscripcion del glosario v2; (iii) F07.
- Hallazgo F04 sin registrar aun: V4 1:28:20-1:28:37 "entrar con 0.50... 0.40 creo yo... estatico o escalado en base a la cuenta" (riesgo por operacion). Entra como evidencia en F07 y como pregunta candidata en F10.
- Regla de cita para F07 (decidida en la auditoria del 2026-09-05, ver MASTER_PLAN H fila F07): `cita_literal` se verifica contra la capa CRUDA (la que forma el id `tr-*`); la corregida es ayuda de lectura. Secuencia obligatoria: glosario v2 aprobado -> retranscribir los 4 videos (`--reemplaza-a`) -> copia en Drive -> primera evidencia con `transcripcion:`.
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
F05 · frame-extraction (orden E: F04 -> F05, F07, F08 -> F10). F10 absorbe: parametros UNKNOWN
pre-poblados, ids de caso + particion + seed, papel `sesion_feedback` en el corpus, y dibujar los
casos con dos anclajes mientras A-9 siga abierta (ver MASTER_PLAN H.2).

## Next Action
Abrir feature/F05-frame-extraction con el metodo supervisado (brief desde MASTER_PLAN H.2 fila F05 y tabla A -> revision de diseno por agente -> construccion -> auditoria de cierre con dos agentes -> informe WAITING_FOR_USER_VALIDATION). Insumo: transcripcion activa `tr-*` de F04 mas huecos heredados de F03; fotogramas obligatorios V3 0:28:56, V2 0:33:21, V4 0:12:30 y configuracion del grafico (A-9). Antes de abrir F07: glosario v2 decidido y retranscripcion hecha, copia de `data/transcripciones/*/cruda.jsonl` y `audio.wav` en Drive.

## Last Stable Commit
a7f8b4b · merge: F04 transcription-pipeline validado por el usuario · tag stable/F04

## Change Log
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
- 2026-09-03 · repositorio inicializado en local · punto cero con documentacion · plan pendiente de validacion
- 2026-09-03 · plan aprobado por el usuario · rama feature/F01-project-scaffold abierta · paquete botsito
- 2026-09-03 · F01 construida; make check verde (21 tests, 3 contratos); WAITING_FOR_USER_VALIDATION
- 2026-09-04 · auditoria de fases (docs/plan/AUDITORIA_FASES_2026-09-04.html): 4 criticos, 19 huecos; plan ampliado (MASTER_PLAN.md seccion H)
- 2026-09-04 · F01 corregida: .gitattributes, tests de integridad del indice, hook anti-main, uv --locked; 26 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · push de la rama F01 autorizado; CI Ubuntu verde (run 33880866257). Linux verificado
- 2026-09-04 · pruebas cruzadas: clon limpio, autocrlf=true, HEAD separado, PowerShell 7, Python 3.13 verdes; Linux pendiente del primer push. HALLAZGO: core.hooksPath relativo omitia el hook en main (sin el fichero); make hooks ahora copia a .git/hooks. Reprobado OK
- 2026-09-04 · tercera auditoria: hook con modo 100755 en el indice, READMEs en todas las carpetas (sin exenciones), holdout/{1,2,3} fisico, mypy strict sobre tests
- 2026-09-04 · segunda auditoria: Last Stable Commit corregido (era 0b43244, main esta en 7baa27d), Next Feature = F02, brief de F01 y README actualizados
