---
status: ACTIVE
date: 2026-09-05
phase: F04
---

# 0007 · Transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario

## Decision
1. **Un WAV por video** (PCM 16 bit, 16 kHz, mono, `-fflags +bitexact`) y toda la aritmetica de
   tiempos en **muestras enteras** sobre ese WAV. Los fragmentos se cortan por muestras (con
   `wave`, no con `ffmpeg -ss` sobre el MP4) y los tiempos absolutos de cada segmento son
   milisegundos enteros: `t_ms = muestra_inicio * 1000 // 16000 + round(r_s * 1000)`.
2. **Corte determinista en silencios**: `cur = 0`; mientras queden mas de `MAX_S` (780 s), se
   elige el centro del silencio (ffmpeg `silencedetect`, -35 dB, >= 0,5 s) mas cercano a
   `cur + OBJETIVO_S` (600 s) dentro de `[cur + MIN_S (420 s), cur + MAX_S]`, empate al mas
   temprano; sin silencio, corte forzado en `cur + OBJETIVO_S`, contado en el manifiesto. Sin
   solape entre fragmentos (deduplicar texto de un ASR no es reproducible). Un segmento que
   cruza el corte se recorta; uno que empieza despues se descarta; ambos se cuentan.
3. **Motor**: faster-whisper large-v3 en la GPU local (`int8_float16`), `temperature=0`,
   `beam_size=5`, `condition_on_previous_text=False`, `vad_filter=True`, `initial_prompt` =
   vocabulario del glosario. Determinismo prometido: misma maquina y mismas versiones -> misma
   cruda. El manifiesto anota modelo y sha256 de sus pesos, versiones de faster-whisper,
   ctranslate2, cuBLAS y cuDNN, GPU, Python, ffmpeg y parametros de corte.
4. **Dos capas**. `cruda.jsonl` (una linea por segmento con `n`, `t0_ms`, `t1_ms`, texto,
   palabras con probabilidad, `no_speech_prob`, `compression_ratio`, `avg_logprob` y `senales`
   derivadas: `repeticion`, `baja_prob`, `compresion`, `no_habla`) es INMUTABLE: su sha256 forma
   el `transcripcion_id = tr-<video>-<motor>-<hash8>`. `corregida.jsonl` = `cruda + glosario`,
   regenerable; `knowledge validate` la recomputa y compara bytes (no guarda su hash, porque el
   glosario cambia). `correcciones.jsonl` registra cada sustitucion y las `dudas`.
5. **Glosario** (`knowledge/corpus/glosario_asr.yaml`, versionado): `vocabulario` para el motor
   y `sustituciones` con dos alcances. `global` solo para un "antes" que no es palabra del
   dominio (el validador rechaza una global que case con el vocabulario); `segmento` (con
   `transcripcion_id`, `segmento`, `verificado_por`) para ambiguedades reales como M5/M15.
   Patrones Unicode con limites de palabra en ambos extremos, sin comodines sin limite, texto
   normalizado a NFC. Nunca se reescribe lo que dijo el trader fuera de este mecanismo.
6. **Manifiesto inmutable por transcripcion** en `knowledge/corpus/transcripciones/<id>.yaml`
   (patron de F15: hook, guardia de historial, `reemplaza_a`, `activos`). Los ficheros pesados
   viven en `data/transcripciones/<video>/<motor>/` (ignorados por git); `knowledge/corpus/`
   declara sus tres regimenes en su README.
7. **Cita desde la evidencia** (F07): `video_id + t0 + t1` sigue siendo la referencia (el video
   es la verdad y sobrevive a retranscribir); `transcript show` entrega la cita literal de la
   transcripcion activa con marcas `h:mm:ss.mmm` y senales. La verificacion de `cita_literal`
   se hace contra la capa cruda (la corregida cambia con el glosario bajo el mismo id); la
   corregida es ayuda de lectura (decidido en la auditoria del 2026-09-05; F07 lo implementa).

## Problema que resuelve
Las transcripciones heredadas (Whisper tiny) derivan hasta un minuto y confunden la jerga; F07
necesita citas literales con minuto fiable, y la seccion H del plan exige no reescribir lo que
dijo el trader. Sin una aritmetica de tiempos exacta, una regla de corte escrita y una
separacion cruda/corregida verificable, cada cita seria discutible.

## Alternativas consideradas
1. Whisper en la nube (API) sobre el video entero.
2. Corte con solape y deduplicacion de texto.
3. Correcciones a mano sobre la transcripcion.
4. Un registro solo-anadir en un unico YAML en vez de un manifiesto por transcripcion.

## Por que elegimos esta opcion
Hay GPU local y el proveedor local es reproducible por hash (3,6x tiempo real medido); el corte
por muestras sin solape es exacto y determinista; el glosario con ejemplo real y dos alcances
corrige lo que el ASR rompe sin tocar lo ambiguo; el manifiesto por fichero reutiliza las guardias
que ya existen (hook, historial, `activos`).

## Por que descartamos las demas
(1) Coste y tiempos poco fiables en ficheros largos; sin control del modelo. (2) Deduplicar
texto de un ASR no es reproducible. (3) Prohibido por la seccion H. (4) No hay guardia de
"solo anadir dentro de un fichero" y contradice el regimen regenerable de `knowledge/corpus`.

## Impacto
`src/botsito/corpus/{audio,transcripcion,glosario,motor_whisper,pipeline_transcripcion,
manifiestos_transcripcion}.py`, `src/botsito/cli.py` (`corpus transcribe|glossary|transcript`),
`src/botsito/validation/knowledge.py`, `src/botsito/comun/{ids,historial}.py`, hook,
`knowledge/corpus/{glosario_asr.yaml,README.md,transcripciones/}`, `pyproject.toml` (grupo `asr`
y contrato: `faster_whisper` solo en `motor_whisper`), fixtures de audio. F07 anade a la evidencia
el campo opcional `transcripcion` (id) sin alterar ids existentes.

## Fecha / fase
2026-09-05 · F04

## Estado
ACTIVE
