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
Los cinco videos con `corpus transcribe --reemplaza-a <id anterior>` (glosario v2 como
`initial_prompt`, 99 tokens; misma GPU, versiones y corte que F04; ~1 h 5 min de GPU en total).
Cada uno en carpeta nueva `large-v3-int8-float16-<huella8>` (la huella cambio por el prompt);
las carpetas y crudas anteriores siguen en `data/` sin tocar. Comparacion cruda nueva frente a
cruda reemplazada (palabras normalizadas, `difflib`; script `comparar.py` en el scratchpad):

| Video | Id activo (reemplaza a) | Segmentos | Palabras | Ratio | Habla (s) | `no_habla` | Hechos clave comprobados |
|---|---|---|---|---|---|---|---|
| v1 | `tr-v1-...-bbd8a931` (00fcaf53) | 403 -> 405 | 4552 -> 4552 | 1,000 | 1631 -> 1631 | 0 -> 0 | 0,75; 50 % (V1 0:15:59) |
| v2 | `tr-v2-...-28391c2c` (ac6b337b) | 854 -> 806 | 8671 -> 8693 | 0,958 | 3382 -> 3419 | 339 -> 342 | stop loss; order flow |
| v3 | `tr-v3-...-270a4851` (570a315f) | 1031 -> 1020 | 10668 -> 10727 | 0,987 | 3999 -> 3993 | 54 -> 36 | 2.83; 3.3; "utc" |
| v4 | `tr-v4-...-a8d1bccc` (3f8c826e) | 1645 -> 1625 | 14257 -> 14256 | 0,978 | 4945 -> 4923 | 441 -> 457 | 0.50 / 0.40; spread; lotaje; "tres" |
| v5 | `tr-v5-...-3c6fbb57` (01a1ae03) | 99 -> 80 | 814 -> 805 | 0,968 | 318 -> 336 | 0 -> 0 | 0.80; "SL por defecto"; "sell"; 1.3; 1.4 |

Huecos (> 30 s sin habla) identicos a los anteriores (v2: 7, v3: 3, resto 0); `repeticion`
baja (v2 2 -> 1, v3 1 -> 0, v4 3 -> 0). Bloques de mas de 6 palabras distintos: 0 en v1 y v5,
2 en v2 y v4, 4 en v3, todos en tramos de charla cruzada o musica (por ejemplo v2 "eres mi
amigo desde que somos ninos", v3 "la mayoria de veces no hace eso"): son lecturas distintas de
audio ambiguo, no perdida de un tramo con decision. Segmento mas largo: 30,4 / 55,0 / 42,0 /
47,5 / 39,6 s (v1..v5). `transcript check` y `knowledge validate` en verde con 10 manifiestos
(5 activos, 5 reemplazados).

Sustituciones aplicadas por `glossary apply` sobre las activas (glosario `e55d5a2c`): v1 2,
v2 5, v3 4, v4 6, v5 0. Las 6 de alcance segmento: `boss` -> BOS (v3 seg 126, 0:11:29),
`voz` -> BOS (v2 seg 275, 0:31:20), `blogs` -> BOS (v4 seg 789, 0:46:59), `split` -> spread
(v4 seg 57, 0:06:06 y seg 131, 0:09:09), `sprint` -> spread (v4 seg 109, 0:08:27). Las demas
apariciones de esos patrones quedan como `dudas` en `correcciones.jsonl` (v2: 8, v3: 13,
v4: 4): F07 decide segmento a segmento ("un orden blog" en v2 0:08:05 es order block, no BOS).

## Copia fuera de esta maquina
- Drive: subcarpeta "transcripciones (crudas, Bot v3)" (id `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R`)
  dentro de "Estrategia del trader", creada por API con `SHA256SUMS.txt`, `LEEME.txt` y los 5
  manifiestos activos (texto, subidos por API en esta sesion).
- PENDIENTE del usuario (las herramientas de la sesion no suben binarios de ese tamano: el API
  del conector solo admite texto o base64 en el propio mensaje, y el navegador exige un dialogo
  nativo): arrastrar a esa carpeta el contenido de `data/drive_staging/` (21 ficheros, 625 MiB:
  5 `cruda.jsonl` + 5 `cruda.txt` + 5 manifiestos + 5 WAV + `2026-09-05 21-03-59.mkv`), cuyos
  sha256 estan en `SHA256SUMS.txt` y coinciden con `sha256_cruda`/`sha256_wav` de los
  manifiestos (comprobado por el script `staging.py` al copiar). Luego anotar el `drive_id` de
  v5 en `knowledge/corpus/fuentes.yaml` (hoy es una nota).

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

## Que deberia observar el usuario
`knowledge validate` en verde con 10 manifiestos de transcripcion; `transcript show --video v5
--t0 0:03:22 --t1 0:03:34` con la frase del 0,80 y el SL por defecto; el glosario con 12
sustituciones; la carpeta de Drive con SHA256SUMS y los 5 manifiestos.

## Que casos funcionan
Todo el alcance de la fila H.2 salvo la subida de binarios a Drive (queda en `drive_staging/`).

## Que casos todavia no funcionan / limitaciones
- `initial_prompt` solo condiciona la primera ventana de cada fragmento: la jerga del resto
  la corrige el glosario (sustituciones con ejemplo real), no el motor. Alternativa medida y
  descartada (`hotwords`). Otra alternativa no medida: `condition_on_previous_text=True` (fue
  descartada en F04 por bucles de repeticion).
- Segmentos de hasta 55 s (v2) tambien con `initial_prompt`: la cita fina usa `palabras` (F07).
- Las `dudas` del glosario (25 segmentos) no se resuelven aqui: F07 las mira al citar.
- `drive_id` de v5 y la copia de crudas/WAV dependen del usuario.

## Riesgos
Si el usuario no sube `drive_staging/`, otra maquina no puede verificar `sha256_cruda` (solo
esquema e historial) ni regenerar sin ~1 h de GPU. Si F07 cita un segmento con `duda`, debe
mirar el audio.

## Impacto sobre funcionalidades anteriores
Los ids `tr-*` de F04 quedan reemplazados (nadie los citaba aun: F07 no ha empezado). El
esquema del manifiesto no cambia (campos nuevos dentro de `motor`, que es libre salvo
`modelo`). `huella_de` cambia para TODAS las carpetas: las de F04 pasan a ser "ajenas" por
manifiesto (`_carpeta_base_registrada_ajena`), lo que ya se comprobo al abrir carpetas nuevas.

## Que debe decidir el usuario
1. Ratificar que `hotwords` queda descartado y el motor sigue con `initial_prompt` (ADR-0007
   enmienda), con las sustituciones del glosario como via para la jerga.
2. Ratificar las 6 sustituciones de alcance segmento (BOS x3, spread x3) con
   `verificado_por: usuario (aprobacion del 2026-09-06 ...)`; si prefiere verificarlas oyendo
   el audio, los minutos estan en el glosario.
3. Subir `data/drive_staging/` a la carpeta de Drive y anotar el `drive_id` de v5 (dueno:
   usuario). Puede hacerse despues del merge (solo cambia `fuentes.yaml`, regimen manual).
4. Cierre como rama con tag `stable/F07-previos` (misma regla que la auditoria global).

## Estado
WAITING_FOR_USER_VALIDATION
