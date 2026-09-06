# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** Previos de F07 (evidence-extraction), fila H.2 "Previos y entradas de F07"
**Rama:** `feature/F07-previos`
**Objetivo:** dejar el corpus en el estado que F07 necesita para citar: glosario v2 aprobado,
los 5 videos retranscritos con el vocabulario nuevo (ids `tr-*` nuevos con `reemplaza_a`),
copia de las crudas fuera de esta maquina y v5 en Drive. Orden ratificado por el usuario el
2026-09-06: glosario v2 -> tareas tecnicas -> retranscribir -> Drive -> abrir F07.

## Que se construyo
- **`hotwords` medido y descartado; el vocabulario sigue como `initial_prompt`**
  (`motor_whisper.py`; ADR-0007, enmienda 2026-09-06). Leido en el codigo de faster-whisper
  1.2.1: con `condition_on_previous_text=False`, `prompt_reset_since = len(all_tokens)` tras
  cada ventana de 30 s, asi que el `initial_prompt` solo condiciona la PRIMERA ventana de cada
  fragmento de ~600 s. `hotwords` se antepone a TODAS las ventanas, pero la medicion (abajo)
  mostro perdida de habla y sesgo hacia el vocabulario: fidelidad manda.
- **Guardia del prompt**: faster-whisper trunca el prompt a `max_length // 2 - 1 = 223` tokens
  sin avisar. `comprobar_prompt` (error de dominio si el motor truncaria; el v2 ocupa 99 tokens)
  y campos nuevos del manifiesto: `initial_prompt_tokens`, `hotwords: null`.
- **Huella de reanudacion sin GPU/driver** (`pipeline_transcripcion.CLAVES_FUERA_DE_HUELLA =
  ("gpu",)`): la carpeta de trabajo y los parciales ya no se invalidan por un cambio de driver;
  ctranslate2, cuBLAS, cuDNN, pesos del modelo, parametros de corte e `initial_prompt_sha256`
  siguen en la huella. El manifiesto sigue anotando la GPU. `_carpeta_base_registrada_ajena`
  recomputa la huella de los manifiestos previos con la misma regla.
- **Glosario v2** (`knowledge/corpus/glosario_asr.yaml`, version `47ae19d7`): 29 terminos
  (v1 + `mitigación`, `orden límite` con acento, `BOS`, `order flow`, `order block`, `complex
  pullback`, `backtesting`, `Gann`, `TP`, `SL`, `RR`) y 6 sustituciones globales con ejemplo
  real (`store loss`, `orden flow`, `cuadro de GAN|gam`, `rotaje`, `bacteseando`, `tepes`).
  Las de alcance segmento (`boss|voz|blog|blogs -> BOS`, `split|sprint -> spread`) exigen
  `transcripcion_id` + `segmento` + `verificado_por`: se anaden sobre las transcripciones
  nuevas (seccion "Sustituciones de segmento").

## Medicion: initial_prompt frente a hotwords (v5, 365 s, GPU local)
Paso 1, tres pasadas de large-v3 sobre `data/transcripciones/v5/audio.wav` con los parametros
del pipeline (beam 5, temperatura 0, VAD, sin condicionar) y el vocabulario v2 (102 tokens en
esa lista, 99 en el glosario final): sin prompt, `initial_prompt`, `hotwords`. Script y salidas
en el scratchpad de la sesion:

| Variante | s | Diferencias de palabras frente a la anterior | Hechos |
|---|---|---|---|
| sin prompt | 81,0 | — | `bacteseando`; "se va a cumplir 13"; "espera, sell" |
| `initial_prompt` | 79,3 | 86 (casi todas puntuacion/mayusculas) | `backtesteando` (primera ventana); "13"; "sell"; repite "no hay entrada No hay entrada" en un borde |
| `hotwords` | 82,8 | 95 (casi todas puntuacion) | `backtesteando`; "cumple el 1, 3"; **"espera, SL"** donde el trader dice "sell" |

Paso 2, pasada OFICIAL con `corpus transcribe` y `hotwords` (id provisional `tr-v5-...-e9a31700`,
borrada sin commitear; cruda guardada en el scratchpad): 22 segmentos frente a 99 (media 15,8 s
frente a 3,2 s; maximo 40,45 s, mas que la ventana de 30 s), `no_habla: 3`, y PERDIDA del tramo
0:03:22-0:03:34 "Y si yo protejo a 0.80, que es el SL por defecto, que no me permite dejarlo"
(hecho A-10) aunque el paso 1 con `hotwords` si lo contenia (99 frente a 102 tokens de prompt
bastan para otro camino de decodificacion). "sell" -> "SL" repetido (2 de 2). Conclusion:
`hotwords` alarga los segmentos mas alla de la ventana (mecanismo conocido de salto de audio en
Whisper), sesga hacia el vocabulario y no es estable; `initial_prompt` no mostro nada de eso.
Decision: `initial_prompt` (ADR-0007 sin cambio de motor) + sustituciones del glosario.

## Retranscripcion (v1-v5)
PENDIENTE DE COMPLETAR

## Copia fuera de esta maquina
PENDIENTE DE COMPLETAR

## Archivos creados
`tests/unit/test_motor_prompt.py`, `docs/validation/F07-previos.md`, manifiestos
`knowledge/corpus/transcripciones/tr-v*-large-v3-int8-float16-<hash8>.yaml` nuevos.

## Archivos modificados
`src/botsito/corpus/{motor_whisper,pipeline_transcripcion,glosario}.py`, `src/botsito/cli.py`,
`tests/unit/test_transcripcion.py`, `knowledge/corpus/glosario_asr.yaml`,
`docs/adr/0007-transcripcion-en-dos-capas.md` (enmienda), `docs/plan/features/F04-transcription-pipeline.md`
(nota), `PROJECT_STATE.md`, `docs/HANDOFF.md`, `docs/plan/MASTER_PLAN.md` (fila H.2).

## Decisiones tomadas
1. `initial_prompt` se mantiene; `hotwords` descartado por fidelidad (medicion). 2. `gpu` fuera de la huella.
3. Las sustituciones de alcance segmento se registran sobre los ids nuevos, no sobre los
   reemplazados. 4. Las transcripciones anteriores no se borran: quedan reemplazadas
   (`reemplaza_a`) y su carpeta `large-v3-int8-float16` intacta en `data/`.

## Como ejecutarlo
```
uv run botsito corpus transcribe --video v5 --reemplaza-a tr-v5-large-v3-int8-float16-01a1ae03
uv run botsito corpus glossary apply
uv run botsito corpus transcript check
uv run botsito knowledge validate
```

## Tests ejecutados
`make check`: 272 funciones de test (395 casos), 4 contratos, mypy strict, state/config/knowledge
validate. Nuevos: huella sin GPU (igual con otra GPU, distinta con otro ctranslate2/prompt/
corte), guardia del prompt (vacio, dentro del limite, truncado = error de dominio),
configuracion sin `hotwords`.

## Estado
WAITING_FOR_USER_VALIDATION
