# F04 · transcription-pipeline

**Rama:** `feature/F04-transcription-pipeline` · **Fase:** 1 · **Depende de:** F03

## Objetivo
Retranscribir los cuatro videos del corpus con Whisper large-v3 (local, GPU de la maquina de
desarrollo) por fragmentos cortados en silencios y con desfase absoluto, para que cada segmento
tenga `t0`/`t1` fiables (las transcripciones heredadas de Whisper tiny derivan hasta un minuto y
confunden la jerga). Dos capas: cruda del ASR (inmutable, con hash) y corregida solo por
sustituciones de un glosario versionado; nunca se reescribe lo que dijo el trader. Es la entrada de
F07 (evidencia con cita literal y minuto) y lo que sustituye al material heredado, que se conserva
como historia y no se cita.

## Alcance cerrado (que SI)
Diseno revisado por agente antes de programar (hallazgos aceptados: aritmetica por muestras en
lugar de `ffmpeg -ss` por fragmento, corte con minimo y maximo y cortes forzados contados, sin
solape, glosario Unicode con dos alcances, manifiesto inmutable por transcripcion en vez de un
registro solo-anadir, corregida verificada por recomputo, ficheros pesados bajo `data/`, VAD y
senales de alucinacion por segmento, vocabulario como `initial_prompt`). Detalle en ADR-0007.
- `src/botsito/corpus/audio.py`: un WAV por video (PCM 16 kHz mono, `+bitexact`, reproducible
  byte a byte), `silencedetect` en muestras, `puntos_de_corte(n, silencios, ParametrosCorte)`
  con `OBJETIVO_S=600`, `MIN_S=420`, `MAX_S=780`, `UMBRAL_SILENCIO_DB=-35`,
  `SILENCIO_MINIMO_S=0.5` (constantes tecnicas con nombre, copiadas al manifiesto), cortes
  forzados contados, `cortar_wav` por muestras con `wave`.
- `src/botsito/corpus/transcripcion.py`: `SegmentoRelativo` (lo que da el motor) y `Segmento`
  (`n`, `t0_ms`, `t1_ms` enteros, texto NFC, palabras con probabilidad, `no_speech_prob`,
  `compression_ratio`, `avg_logprob`, `senales`); `fusionar` con `t_ms = inicio_ms + round(r *
  1000)`, recorte al fin del fragmento, descarte de lo posterior, monotonia, `t1 <= fin del WAV`;
  `huecos` (>= 30 s, inicial y final incluidos); JSONL con `n` como id estable; reanudacion por
  fragmento con sha256 del WAV y huella de parametros; `parse_ms`/`formato_ms` (`h:mm:ss.mmm`);
  `texto_entre` con margen; `MotorFalso` para tests y CLI.
- `src/botsito/corpus/motor_whisper.py`: unico modulo que importa `faster_whisper` (contrato de
  importacion); DLLs de cuBLAS/cuDNN desde pip; `temperature=0`, `beam_size=5`,
  `condition_on_previous_text=False`, `vad_filter=True`, `initial_prompt` = vocabulario;
  `describir()` con modelo, sha256 de `model.bin`, versiones, GPU, Python.
- `src/botsito/corpus/glosario.py`: `vocabulario` + `sustituciones` con `alcance: global |
  segmento`, patrones Unicode con limites en ambos extremos y sin comodines, una global no puede
  casar con el vocabulario; `aplicar` -> (corregida, correcciones, dudas); version = hash del
  fichero.
- `src/botsito/corpus/pipeline_transcripcion.py`: orquestacion reanudable; escribe
  `data/transcripciones/<video>/audio.wav`, `<video>/<motor>/{fragmentos,parciales,cruda.jsonl,
  cruda.txt,corregida.jsonl,correcciones.jsonl}` y el manifiesto inmutable
  `knowledge/corpus/transcripciones/tr-<video>-<motor>-<hash8>.yaml` (con `reemplaza_a`).
- `src/botsito/corpus/manifiestos_transcripcion.py`: esquema, `activos`/`activa_de`,
  `comprobar` (cruda por hash; corregida y correcciones recomputadas contra el glosario actual).
- CLI: `corpus transcribe --video v1 [--motor faster-whisper|falso] [--modelo] [--dispositivo]
  [--compute-type] [--objetivo-s --min-s --max-s] [--reemplaza-a]`, `corpus glossary apply
  [--video]`, `corpus transcript check`, `corpus transcript show --video --t0 --t1 [--margen-s]
  [--capa cruda|corregida] [--transcripcion]`. `knowledge validate` valida manifiestos,
  historial de git, cruda por hash y corregida por recomputo. Hook protege el directorio.
- Revision de citas: las 29 marcas unicas de la investigacion mas las 3 del lineamiento (y
  V1 0:00:00, referencia al inicio de la prueba de fondeo: 33 en total) se leen con
  `transcript show` con margen (75 s bastaron: el desfase maximo fue 8 s) y el informe lleva la
  tabla `marca heredada -> marca nueva -> veredicto`. El plan decia "50 citas"; son 32 + 1.
- Glosario inicial: vocabulario del dominio; sustituciones solo con ejemplo real de large-v3.
## Fuera de alcance (que NO)
Fotogramas (F05). Extraccion de evidencia (F07). Diarizacion (quien habla): se anota como
riesgo; F07 lo resuelve leyendo el contexto. Traduccion. Reconocimiento de lo que se ve en
pantalla. Motores en la nube (no hacen falta: hay GPU local; queda como alternativa documentada).

## Entradas
Videos del corpus (manifiesto F03 con duracion y sha256), ffmpeg 9, faster-whisper 1.2 con
CUDA (GTX 1650, 4 GB: `int8_float16`), README heredado con la lista de errores de jerga,
investigacion 2026-09-03 (citas), PROJECT_STATE (lineamientos).

## Salidas (ficheros)
`src/botsito/corpus/{audio,transcripcion,motor_whisper,glosario,pipeline_transcripcion,
manifiestos_transcripcion}.py`, `src/botsito/cli.py`, `src/botsito/validation/knowledge.py`,
`src/botsito/comun/{ids,historial}.py`, `scripts/git-hooks/pre-commit`,
`knowledge/corpus/{glosario_asr.yaml,README.md}`, `knowledge/corpus/transcripciones/*.yaml`,
`pyproject.toml` (grupo `asr`, contrato), `tests/unit/test_{audio,transcripcion,
pipeline_transcripcion}.py`, `tests/contract/test_transcripcion_history.py`,
`tests/fixtures/audio/tono_silencio_tono_10s.wav`, `docs/adr/0007-transcripcion-en-dos-capas.md`.

## Tests
- Unit (puros): corte sin silencios (forzados contados), silencio mas cercano al objetivo con
  desempate por el mas temprano, silencio fuera de la ventana ignorado, silencio que cruza el
  objetivo, audio corto sin corte, parametros invalidos; propiedad (hypothesis): puntos
  crecientes, primero 0, ultimo n, fragmentos <= MAX y >= MIN salvo el ultimo. Fusion: aritmetica
  exacta (fragmento en 599.4 s -> `t0_ms = 599920`), recorte y descarte contados, monotonia,
  fin del WAV; senales por segmento; huecos inicial y final; JSONL ida y vuelta y rechazos;
  `h:mm:ss.mmm`; reanudacion por fragmento sensible al WAV y a los parametros; glosario con dos
  alcances, dudas, reproducibilidad, limites Unicode (`an` no toca "año"), rechazos.
- Integracion (ffmpeg, sin modelo): fixture `tono_silencio_tono_10s.wav` (silencio 3-5 s
  detectado, corte en su centro, fragmentos por muestras); WAV del clip bit a bit reproducible;
  pipeline completo con `MotorFalso` sobre el clip: manifiesto valido, id estable, segunda
  ejecucion sin reescribir, `comprobar` detecta corregida editada, glosario cambiado y cruda
  alterada; manifiestos corruptos rechazados; CLI `transcribe`, `transcript check`, `glossary
  apply`, `transcript show`, `knowledge validate` con la capa de transcripciones.
- Contrato: historial de git de `knowledge/corpus/transcripciones/` (modificar y borrar se
  detectan); `faster_whisper` solo importable desde `motor_whisper`.
- Con modelo (no en CI): los cuatro videos reales; determinismo verificado en el informe
  transcribiendo dos veces un fragmento.

## Criterio de aceptacion
`make check` verde; los cuatro videos transcritos con large-v3 en esta maquina, cada uno con su
manifiesto inmutable versionado; ningun segmento fuera del WAV; cortes forzados y huecos >= 30 s
listados y justificados en el informe; las 32 citas revisadas con veredicto por cita; glosario
con cada entrada justificada por un ejemplo real; material heredado intacto.

## Riesgos
- Velocidad: large-v3 `int8_float16` en una GTX 1650 va a unas 3-6 veces tiempo real: 4,5 h de
  audio son 1-2 h de GPU; se ejecuta en segundo plano por video y se reanuda por fragmento
  (cada fragmento transcrito se guarda antes de seguir).
- Memoria: 4 GB de VRAM bastan para `int8_float16`; si falla, `int8` en CPU (unas 10 h).
- Alucinaciones de Whisper en silencios largos (repite frases): el corte en silencios y el
  listado de huecos las hacen visibles; el informe revisa los tramos senalados.
- Dos voces en V2/V3/V4 (trader y consultor): sin diarizacion; F07 atribuye por contexto y
  la cita literal siempre lleva minuto para comprobarlo en el video.
- Jerga: el glosario corrige solo con ejemplo real; una correccion sin ejemplo no entra.

## Que habilita
F07 (evidencia con cita y minuto), F08 (contradicciones sobre citas fiables), F10 (preguntas al
trader con su propia formulacion), F05 (los tramos con decision se localizan por la transcripcion).
