# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F04 · transcription-pipeline
**Rama:** `feature/F04-transcription-pipeline`
**Objetivo:** retranscribir los cuatro videos del corpus con Whisper large-v3 en la GPU local, por
fragmentos cortados en silencios y con tiempos absolutos exactos, en dos capas (cruda inmutable
con hash; corregida = cruda + glosario versionado), con un manifiesto inmutable por transcripcion
y una CLI que entrega la cita literal con minuto. Es la entrada de F07 (evidencia con cita) y
sustituye al material heredado de Whisper tiny, que se conserva y no se cita.

## Que se construyo
- `src/botsito/corpus/audio.py`: un WAV por video (PCM 16 bit, 16 kHz, mono, `-fflags +bitexact`,
  byte a byte reproducible), `silencedetect` convertido a muestras, `puntos_de_corte` (objetivo
  600 s, minimo 420 s, maximo 780 s, silencio >= 0,5 s bajo -35 dB; sin silencio, corte forzado
  contado), `cortar_wav` por muestras exactas con `wave`. Sin solape entre fragmentos.
- `src/botsito/corpus/transcripcion.py`: `Segmento` con `n`, `t0_ms`, `t1_ms` enteros, texto NFC,
  palabras con probabilidad, `no_speech_prob`, `compression_ratio`, `avg_logprob` y `senales`
  derivadas (`repeticion`, `baja_prob`, `compresion`, `no_habla`); `fusionar` con `t_ms =
  inicio_ms_del_fragmento + round(r_s * 1000)`, recorte al fin del fragmento y descarte de lo
  posterior (ambos contados), monotonia y `t1 <= fin del WAV`; `huecos` >= 30 s (inicial y
  final incluidos); JSONL con claves ordenadas; reanudacion por fragmento (`parciales/*.json`
  con sha256 del WAV del fragmento y huella de motor + corte; un parcial corrupto o de otros
  parametros se retranscribe); `parse_ms`/`formato_ms` (`h:mm:ss[.mmm]`); `texto_entre`.
- `src/botsito/corpus/motor_whisper.py`: unico modulo que importa `faster_whisper` (contrato de
  importacion y test AST); DLLs de cuBLAS/cuDNN desde pip; `temperature=0`, `beam_size=5`,
  `condition_on_previous_text=False`, `vad_filter=True`, `word_timestamps=True`,
  `initial_prompt` = vocabulario del glosario; `describir()` con modelo, sha256 de `model.bin`,
  versiones de faster-whisper, ctranslate2, cuBLAS, cuDNN, GPU, Python.
- `src/botsito/corpus/glosario.py`: `knowledge/corpus/glosario_asr.yaml` con `vocabulario` y
  `sustituciones` de dos alcances (`global` para un "antes" que no es palabra del dominio;
  `segmento` con `transcripcion_id`, `segmento`, `verificado_por`); patrones Unicode con limites
  de palabra en ambos extremos y sin comodines sin limite; una global no puede casar con el
  vocabulario; `aplicar` -> (corregida, correcciones, dudas); version = hash del fichero.
- `src/botsito/corpus/pipeline_transcripcion.py`: orquestacion reanudable; escribe
  `data/transcripciones/<video>/audio.wav` y `<video>/<motor>/{fragmentos,parciales,cruda.jsonl,
  cruda.txt,corregida.jsonl,correcciones.jsonl}`; manifiesto INMUTABLE
  `knowledge/corpus/transcripciones/tr-<video>-<motor>-<hash8 de cruda>.yaml` (con
  `reemplaza_a`); una cruda existente con otro contenido detiene el proceso (inmutabilidad).
- `src/botsito/corpus/manifiestos_transcripcion.py`: esquema (campos obligatorios, id con prefijo
  `tr-<video>-` y sufijo = hash de cruda, carpeta exacta `transcripciones/<video>/<motor>`),
  `activos`/`activa_de` (rechaza `--transcripcion` de otro video), `comprobar` (cruda por hash;
  corregida y correcciones recomputadas contra el glosario actual y comparadas byte a byte).
- CLI: `corpus transcribe --video v1 [--motor faster-whisper|falso] [--modelo] [--dispositivo]
  [--compute-type] [--objetivo-s --min-s --max-s] [--reemplaza-a]`, `corpus glossary apply
  [--video]`, `corpus transcript check`, `corpus transcript show --video --t0 --t1 [--margen-s]
  [--capa cruda|corregida] [--transcripcion]` (un instante `--t0 == --t1` es una cita valida).
  `knowledge validate` suma la capa de transcripciones (esquema, historial de git, cruda por hash,
  corregida por recomputo). Hook `pre-commit` protege `knowledge/corpus/transcripciones/` y ya no
  resincroniza el entorno dentro de un commit (`uv lock --check` + `uv run --no-sync`).
- ADR-0007; `knowledge/corpus/README.md` con los tres regimenes; grupo de dependencias `asr`
  (faster-whisper 1.2.1, ctranslate2 4.8.2, nvidia-cublas-cu12, nvidia-cudnn-cu12); fixture
  `tests/fixtures/audio/tono_silencio_tono_10s.wav`.

## Archivos creados
```
src/botsito/corpus/{audio,transcripcion,motor_whisper,glosario,pipeline_transcripcion,manifiestos_transcripcion}.py
docs/adr/0007-transcripcion-en-dos-capas.md  docs/plan/features/F04-transcription-pipeline.md
docs/validation/F04-transcription-pipeline.md
knowledge/corpus/glosario_asr.yaml  knowledge/corpus/README.md
knowledge/corpus/transcripciones/tr-v{1,2,3,4}-large-v3-int8-float16-<hash8>.yaml
tests/unit/test_{audio,transcripcion,pipeline_transcripcion}.py
tests/contract/test_transcripcion_history.py  tests/fixtures/audio/tono_silencio_tono_10s.wav
```

## Archivos modificados
`src/botsito/cli.py`, `src/botsito/validation/knowledge.py`, `src/botsito/comun/{ids,historial}.py`,
`scripts/git-hooks/pre-commit`, `pyproject.toml` (grupo `asr`; cuarto contrato de importacion),
`uv.lock`, `tests/contract/test_{import_contracts,no_business_literals}.py` (exencion explicita
`# no-negocio: <motivo>` para hechos tecnicos que coinciden con un numero de negocio),
`docs/adr/README.md`, `docs/plan/MASTER_PLAN.md` (H.2 "dos capas" hecho; F04: 32 citas, no 50),
`README.md`, `tests/README.md`, `PROJECT_STATE.md`.

## Decisiones tomadas
- **Revision de diseno antes de programar** (agente revisor sobre el brief; 8 hallazgos de fondo
  aceptados): aritmetica por muestras enteras en lugar de `ffmpeg -ss` por fragmento (el priming
  del AAC desplaza el audio); corte con minimo y maximo y cortes forzados contados; sin solape
  (deduplicar texto de un ASR no es reproducible); glosario Unicode con dos alcances; manifiesto
  inmutable por transcripcion en vez de un registro solo-anadir; corregida verificada por
  recomputo (no por hash, porque el glosario cambia); ficheros pesados bajo `data/`; VAD y
  senales de alucinacion por segmento; vocabulario como `initial_prompt`.
- **Motor local (GPU) y no nube**: reproducible por hash en esta maquina, 3,6x tiempo real medido;
  la version y el sha256 de los pesos quedan en el manifiesto.
- **Vocabulario sin acentos en esta tanda**: el `initial_prompt` entra en la huella de
  reanudacion; cambiarlo a mitad de tanda habria obligado a retranscribir. Se corrige en la
  siguiente edicion del glosario (ver "Que debe decidir el usuario").
- **Literal 0,5 s en `audio.py`**: es la duracion minima de un silencio, no la proteccion a
  0,50; el detector de literales de negocio gana una exencion explicita con motivo obligatorio.
- **Auditoria de cierre hecha sin agentes**: los dos auditores lanzados cayeron por el limite de
  sesion; la revise yo linea a linea (hallazgos y correcciones en "Resultados").

## Como ejecutarlo
```
make check
uv sync --group asr                               # faster-whisper + CUDA por pip (una vez)
uv run botsito corpus transcribe --video v1        # ~7 min en la GTX 1650; reanudable
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus glossary apply               # tras editar knowledge/corpus/glosario_asr.yaml
uv run botsito knowledge validate
```

## Como probarlo
- `uv run botsito corpus transcribe --video v1` otra vez: no llama al modelo (parciales validos),
  recomputa la cruda, comprueba que su hash coincide con la existente y no reescribe el
  manifiesto. Borrar `data/transcripciones/v1/large-v3-int8-float16/parciales/fragmento_000.json`
  y repetir: retranscribe solo ese fragmento y la cruda debe salir identica (determinismo; ver
  "Resultados").
- Editar un byte de `cruda.jsonl`: `transcript check` y `knowledge validate` lo detectan
  ("alterada"). Editar `corregida.jsonl`: "no es cruda + glosario". Editar el glosario sin
  `glossary apply`: "no coincide con el glosario actual".
- Editar a mano un manifiesto de `knowledge/corpus/transcripciones/` e intentar commitear: el
  hook lo rechaza; con `--no-verify`, `knowledge validate` y
  `tests/contract/test_transcripcion_history.py` fallan.
- `uv run pytest -q tests/unit/test_audio.py tests/unit/test_pipeline_transcripcion.py`: el
  fixture de 10 s (tono, silencio 3-5 s, tono) se corta en el centro del silencio, el pipeline
  completo corre con `MotorFalso` (sin modelo) y el manifiesto valida.

## Tests ejecutados
`make check` equivalente (`ruff`, `mypy strict` src + tests, `lint-imports` 4 contratos, `pytest`
235 funciones, `state check`) en `feature/F04-transcription-pipeline`, Windows 11, Python 3.12,
con `uv run --no-sync` mientras la GPU transcribia. CI verde en `3f73813`
(https://github.com/Fibobrioso/Botsito/actions/runs/33946879078); CI de `d1f3947` y del
commit final: ver la rama.

## Resultados
### Transcripciones reales (large-v3, int8_float16, GTX 1650, CUDA)
| Video | Duracion | Fragmentos | Forzados | Segmentos | Recortados/descartados | Huecos >= 30 s | Senales | GPU |
|---|---|---|---|---|---|---|---|---|
| v1 | 29:12 | 3 | 0 | 403 | 0 / 0 | 0 | ninguna | 7 min 12 s |
| v2 | 1:08:54 | 7 | 0 | 854 | 0 / 0 | 7 (todos entre 0:38:28 y 0:56:04) | no_habla 339, repeticion 2 | 14 min 58 s |
| v3 | 1:17:56 | 8 | 0 | 1031 | 0 / 0 | 3 (0:35:06, 0:58:05, 1:05:50) | no_habla 54, repeticion 1 | 17 min 9 s |
| v4 | 1:33:37 | 10 | 0 | 1645 | 0 / 0 | 0 | no_habla 441, repeticion 3 | no medible (la maquina estuvo en pausa: 6 h 37 min de reloj; estimado 22 min a 3,6x) |

Ningun corte forzado: todos los cortes cayeron en silencios reales. Los huecos y las 339 senales
`no_habla` de v2 coinciden con el tramo que la investigacion ya marcaba como inutilizable por
musica y solapamiento (0:38:48 a 0:53:14): el modelo no inventa texto ahi, marca lo poco que
transcribe y deja huecos. Ids: `tr-v1-large-v3-int8-float16-00fcaf53`,
`tr-v2-large-v3-int8-float16-ac6b337b`, `tr-v3-large-v3-int8-float16-570a315f`, `tr-v4-large-v3-int8-float16-3f8c826e`.

### Determinismo
Tras terminar los cuatro videos se borro `parciales/fragmento_000.json` de v1 y se repitio
`corpus transcribe --video v1`: solo ese fragmento volvio a la GPU (2 min 38 s), el parcial nuevo
es identico al anterior (128 segmentos, mismo JSON), la cruda tuvo el mismo sha256 y el manifiesto
`tr-v1-large-v3-int8-float16-00fcaf53` no se reescribio. Determinismo verificado en esta
maquina y estas versiones (faster-whisper 1.2.1, ctranslate2 4.8.2, cuBLAS 12.9.2.10, cuDNN
9.25.1.1, driver 610.62).

### Revision de las 33 marcas heredadas (29 de la investigacion + 3 del lineamiento + V1 0:00:00)
Leidas con `transcript show --margen-s 75` sobre la cruda. "Coincide" = la frase citada esta
en la transcripcion nueva a menos de 15 s de la marca heredada.

| Marca heredada | Que se citaba | Marca nueva | Veredicto |
|---|---|---|---|
| V1 0:00:00 | inicio de la prueba de fondeo | 0:00:00.210 "acabo de iniciar con lo de la prueba de fondeo" | coincide |
| V1 0:06:19 | proteger a 0,75 al entrar (lineamiento) | 0:06:27-0:06:32 "En 0.75 proteger el trade, a inicio apenas se genere la entrada" | coincide (+8 s) |
| V1 0:07:52 | extender el objetivo mas alla de 1:3 "por lectura de mercado" | 0:07:51 "me hubiera salido en 13 no por lectura de mercado" | coincide |
| V1 0:15:58 | proteger a 0,50 "cuando ha pasado mas del 40 % de la vela" | 0:15:59 "ya ha pasado mas del 50% de la vela"; 0:16:51 "de pasar de 0.75 es a 0.50" | marca coincide; **la cifra NO: large-v3 dice 50 %, la heredada decia 40 %** (pregunta para el trader, F10) |
| V2 0:05:22 | "cuando se pase a codigo, sea lo mas objetivo posible" | 0:05:21-0:05:31 "lo mas simple posible... para que cuando se ponga el codigo... sea objetivo" | coincide (parafrasis heredada) |
| V2 0:31:59 | 0,75 protege 0,25 del capital (lineamiento) | 0:32:01-0:32:34 | coincide (+2 s) |
| V2 0:33:21 | herramienta de posicion 4,08 / 3,94 (fotograma) y "se acaba el dia" | audio 0:33:14-0:33:50 habla de drawdown y "3 con 25" | no verificable por audio (era fotograma); el audio no contradice |
| V2 0:37:08 | "validar el sistema" como objetivo | 0:37:10 "aumentar mi numero de muestras... y validar el sistema" | coincide |
| V2 0:38:48-0:53:14 | tramo inutilizable [MUSICA] | huecos 0:38:28-0:56:04 y senales no_habla | coincide |
| V2 0:59:01 | tramo con audio malo | hueco 0:58:41-0:59:09 y no_habla hasta 0:59:37 | coincide |
| V3 0:12:26 | huecos de fotogramas al dibujar sobre el mismo grafico | (era fotograma) audio 0:12:04-0:12:29 sobre el flujo de M15 | no verificable por audio; el audio no contradice |
| V3 0:14:00 | recuento de deicticos ("aqui", "esto") en 10 min | 0:14:04-0:14:48 "aqui... este... esto... vamos a definirlo asi, mira" | coincide |
| V3 0:16:05 | "todo lo que se desarrolla por debajo de la liquidez de M15 es ruido" | 0:16:06-0:16:14 "todo lo que se desarrolle... por debajo de esta liquidez de m15 es ruido" | coincide (literal) |
| V3 0:28:56 | Excel "2,3 / -0,75 / 3,23 / -0,5" | 0:28:56-0:29:28 "2.83... menos 0.75... 3.33... menos 0.5" | marca coincide; **cifras 2,3/3,23 (heredada) frente a 2.83/3.33 (large-v3)**: decide el fotograma del Excel (F05) |
| V3 0:31:28 | objetivo mas alla de 1:3 por lectura de mercado | 0:31:25-0:31:42 "el profit maximo que suelo buscar es en la liquidez de m15... 1 a 3 es lo minimo" | coincide |
| V3 0:51:46 | "aqui no hay entrada, mucho ruido, no mapeo asi" | 0:51:47-0:52:09 "no hay entrada aqui... si lo mapeas de esta manera se rompe el esquema... simplemente no hay entrada" | coincide |
| V3 0:59:56 | retroceso complejo y gestion del stop | 0:59:34-1:00:07 "complex pullback... gestiono el stop loss de esa manera" | coincide |
| V3 1:06:48 | que se considera una vela al mapear | 1:06:48.962 "si tu lo mapeas de esta manera, es lo mas probable que en una temporalidad mayor esto sea una vela" | coincide (literal) |
| V4 0:05:42 | "mas de 250" operaciones backtesteadas a mano | 0:05:43-0:05:49 "mas de 250 en trades... mi muestra es de esa cantidad" | coincide |
| V4 0:08:39 | "dar un pequeno respiro: de 0,75 a 0,80" por el spread (lineamiento) | 0:08:39-0:08:56 "darle un pequeno respiro... uno o dos pips... de 0.75 a 0.80 o fijo en 0.75" | coincide (literal) |
| V4 0:12:30 | caja: nivel 0,75 = 1,19537 (fotograma) | audio 0:12:13-0:12:41 "el stop loss... es hasta el 0.75... que se desplace de acuerdo al spread del momento" | nivel no verificable por audio; el audio coincide con la regla |
| V4 0:19:21 | "aqui no hay entrada porque genera dos zonas de control" | 0:19:09-0:19:22 "aqui no habria un trade... por el hecho de que te genera dos zonas de control" | coincide |
| V4 0:21:41 | stop del segundo esquema en el minimo estructural en vez de 0,75 | 0:21:39-0:21:54 "en vez de proteger a 0.75... lo protege por el punto mas bajo" | coincide |
| V4 0:22:27 | "soy humano, no puedo procesar muchos datos" | 0:22:25 "mira soy humano o sea no puedo procesar muchos datos" | coincide (literal) |
| V4 0:44:56 | break even al tocar o al cierre | 0:44:49-0:45:00 "pones en break even... apenas rompe esto o cierra la vela, pues ya proteges" | coincide |
| V4 0:47:47 | "aqui entra un poco lo discrecional" | 0:47:43 "aqui entra un poco discrecional, o sea, la discrecionalidad de decir" | coincide |
| V4 0:48:41 | 2 frente a 3 cartuchos | 0:48:36-0:48:49 "tienes un cartucho todavia... yo sinceramente limito a tres" | coincide |
| V4 0:58:05 | "apenas inicia una vela contraria en un flujo de ordenes ya marco" | 0:58:06 "apenas se inicia una vela contraria en un flujo de ordenes, yo ya lo tomo como un punto en el cual yo ya voy marcando" | coincide (literal) |
| V4 1:07:33 | la orden limite se mueve con el flujo | 1:07:31-1:07:53 "order limit, tu lo puedes ir moviendo conforme se va desarrollando el flujo" | coincide |
| V4 1:08:18 | salida anticipada si la limite se activa sin ruptura | 1:08:17-1:08:31 "cerrar apenas la operacion... se cierra la vela y si no termina por debajo con un rompimiento, cerrar" | coincide |
| V4 1:28:41 | grabaciones operando en vivo, ofrecidas | 1:28:44-1:28:52 "cualquier dia que opere simplemente graba tu pantalla... tu operativa en vivo" | coincide (+3 s) |
| V4 1:30:09 | una sola estrategia; tercer esquema propuesto | 1:30:08-1:30:43 "quiero agregar algo... el tercer esquema de entrada seria que el precio llegue aqui" | coincide |
| V4 1:31:16 | variantes de entrada con gestion identica | 1:31:12-1:31:40 "muy clave el break even cuando se desarrolle otra zona de control... se calcula el lotaje desde aqui hasta aqui" | coincide |

Balance: 33 marcas; 28 coinciden (12 literales o casi), 3 eran fotogramas (el audio no las
contradice), 2 coinciden en la marca pero con cifra distinta en la transcripcion nueva (V1
0:15:58: 50 % frente a 40 %; V3 0:28:56: 2.83/3.33 frente a 2,3/3,23). Desfase maximo observado
entre marca heredada y nueva: 8 s (V1 0:06:19). Ninguna cita cambia de sentido. Hallazgo extra
no citado antes: V4 1:28:20-1:28:37 "entrar con 0.50... 0.40 creo yo... estatico o escalado en
base a la cuenta" (riesgo por operacion; para el registro en F07/F10).


### Auditoria de cierre (codigo y proceso)
Hallazgos corregidos en `d1f3947`: un parcial JSON corrupto abortaba la transcripcion (ahora se
retranscribe ese fragmento); el esquema del manifiesto no exigia que el id empezara por
`tr-<video>-` ni que la carpeta fuera exactamente `transcripciones/<video>/<motor>` (un
manifiesto podia apuntar fuera de `data/`); `transcript show --video v1 --transcripcion <id de
v2>` mostraba el texto de v2 rotulado como v1; `knowledge validate` se caia con una cruda no
parseable en vez de listar el error; una cita de un instante (`--t0 == --t1`) se rechazaba.
Sin hallazgos: aritmetica de tiempos (probada con fragmento en 599,4 s), atomicidad de escrituras,
contratos de capas, mypy strict, literales de negocio.

## Que debe decidir el usuario
1. El **50 % frente al 40 %** de la vela para bajar la proteccion a 0,50 (V1 0:15:58): la
   transcripcion nueva contradice la cifra del lineamiento. Propuesta: queda como pregunta al
   trader en F10 y el lineamiento en PROJECT_STATE se anota con ambas cifras y la fuente.
2. Glosario: entradas con ejemplo real de large-v3 para la siguiente version (no aplicadas aun,
   porque cambian la huella): `store loss -> stop loss` (V2 0:05:41), `orden flow -> order
   flow` (V2 0:32:26), `cuadro de GAN|gam -> cuadro de Gann` (V1 0:06:22, V2 0:31:42) y
   vocabulario con acentos (`mitigación`, `orden límite`) ; ademas `boss|voz|blog|blogs -> BOS` (V3 0:11:29, V2 0:31:20, V4 0:46:59; `blog` con alcance segmento porque es palabra corriente), `split|sprint -> spread` (V4 0:06:06, 0:08:27, 0:09:09; alcance segmento), `rotaje -> lotaje` (V4 1:31:40), `bacteseando -> backtesteando` (V3 0:14:18), `tepes -> TPs` (V3 0:32:20), y vocabulario nuevo: `BOS`, `order flow`, `order block`, `complex pullback`, `backtesting`, `Gann`, `TP`, `SL`, `RR`.
3. El corte 600/420/780 s y el umbral -35 dB / 0,5 s como constantes tecnicas (no de negocio).
4. Que las transcripciones heredadas de Whisper tiny no se citan (se conservan como historia).

## Que puede comprobar sin GPU
`make check`, `uv run botsito knowledge validate` (los cuatro manifiestos validan por esquema e
historial; sin `data/` avisa que la cruda no esta en esta maquina), `uv run botsito corpus
transcript check`, y `git log -- knowledge/corpus/transcripciones/` (un commit por manifiesto,
nunca editados). Con la carpeta `data/transcripciones/` de esta maquina: `transcript show` sobre
cualquier marca de la tabla.

## Que deberia observar el usuario
Los cuatro manifiestos con recuentos coherentes con la tabla; `transcript show --video v1 --t0
0:06:19 --t1 0:06:19 --margen-s 30` con la frase del 0,75; `knowledge validate` en verde.

## Que casos funcionan
Todo el alcance del brief: cuatro videos transcritos, manifiestos inmutables, dos capas
verificadas por recomputo, CLI de cita, reanudacion, guardias de historial.

## Impacto sobre funcionalidades anteriores
`knowledge validate` suma una capa; el hook protege un directorio mas; el detector de literales
admite `# no-negocio: <motivo>`; `comun/ids.py` gana el patron `transcripcion`. Nada del corpus
heredado (F03) cambia.

## Que casos todavia no funcionan
- Sin diarizacion (quien habla) en V2-V4: F07 atribuye por contexto y cita con minuto.
- El glosario no tiene sustituciones todavia (solo vocabulario): la corregida es igual a la
  cruda hasta que el usuario apruebe las entradas propuestas.
- El campo `transcripcion` en la evidencia llega con F07; schema v2 del manifiesto con F16.

## Limitaciones
Los ficheros pesados (WAV, cruda, corregida) no viajan en git: otra maquina valida esquema e
historial pero no el hash de la cruda salvo que copie `data/transcripciones/`. Whisper marca
`no_habla` con frecuencia en tramos con dos voces o musica: es senal, no veredicto. El
determinismo esta verificado en esta maquina y estas versiones; otra GPU o version puede dar
otra cruda (seria otro manifiesto con `reemplaza_a`).

## Riesgos
Un cambio de version de faster-whisper/ctranslate2 o del vocabulario obliga a retranscribir
para mantener la promesa de reproducibilidad (el manifiesto lo delata). La cifra 40 % / 50 %
afecta a la regla de gestion del stop (F21).

## Estado
WAITING_FOR_USER_VALIDATION
