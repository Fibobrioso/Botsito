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
  fragmento de ~600 s. `hotwords` se antepone a TODAS las ventanas, pero la medicion (Resultados)
  mostro perdida de habla y sesgo hacia el vocabulario: fidelidad manda.
- **Guardia del prompt**: faster-whisper trunca el prompt a `max_length // 2 - 1 = 223` tokens
  sin avisar. `comprobar_prompt` cuenta como el motor (`" " + texto.strip()`,
  `add_special_tokens=False`) y es error de dominio si el motor truncaria; corre ANTES de cargar
  los pesos en la GPU (tokenizador desde `tokenizer.json`). El vocabulario v2 ocupa 96 tokens.
  Campos nuevos del manifiesto: `initial_prompt_tokens` (fuera de la huella) y `hotwords: null`
  (constancia de la configuracion, no campo funcional).
- **Huella de reanudacion sin GPU/driver ni recuento de tokens**
  (`pipeline_transcripcion.CLAVES_FUERA_DE_HUELLA = ("gpu", "initial_prompt_tokens")`): la
  carpeta de trabajo y los parciales ya no se invalidan por un cambio de driver ni por como se
  cuentan los tokens; ctranslate2, cuBLAS, cuDNN, pesos del modelo, parametros de corte e
  `initial_prompt_sha256` siguen en la huella. El manifiesto sigue anotando la GPU.
  `_carpeta_base_registrada_ajena` recomputa la huella de los manifiestos previos con la misma
  regla (tests nuevos).
- **Glosario v2** (`knowledge/corpus/glosario_asr.yaml`, version `e55d5a2c`; `47ae19d7` fue la
  version con solo las 6 globales, con la que se retranscribio: el `vocabulario`, y por tanto
  el `initial_prompt`, es el mismo en ambas): 29 terminos (v1 + `mitigación`, `orden límite`
  con acento, `BOS`, `order flow`, `order block`, `complex pullback`, `backtesting`, `Gann`,
  `TP`, `SL`, `RR`), 6 sustituciones globales con ejemplo real (`store loss`, `orden flow`,
  `cuadro de GAN|gam`, `rotaje`, `bacteseando`, `tepes`) y 6 de alcance segmento
  (`boss|voz|blogs -> BOS`, `split|sprint -> spread`) sobre los ids nuevos.

## Archivos creados
`tests/unit/test_motor_prompt.py`, `docs/validation/F07-previos.md`,
`docs/validation/anexos/F07-previos/` (evidencia de la medicion: script, las tres salidas del
paso 1, la cruda y el manifiesto descartados del paso 2, `comparar.py`, `staging.py`),
manifiestos `knowledge/corpus/transcripciones/tr-v{1..5}-large-v3-int8-float16-<hash8>.yaml`.

## Archivos modificados
`src/botsito/corpus/{motor_whisper,pipeline_transcripcion,glosario}.py`,
`knowledge/corpus/glosario_asr.yaml`, `docs/adr/0007-transcripcion-en-dos-capas.md` (enmienda),
`docs/plan/features/F04-transcription-pipeline.md` (nota), `PROJECT_STATE.md`,
`docs/HANDOFF.md`, `docs/plan/MASTER_PLAN.md` (fila H.2, §F, Change Log).

## Decisiones tomadas
1. `initial_prompt` se mantiene; `hotwords` descartado por fidelidad (medicion).
2. `gpu` e `initial_prompt_tokens` fuera de la huella de reanudacion.
3. Las sustituciones de alcance segmento se registran sobre los ids nuevos, no sobre los
   reemplazados; el resto de apariciones quedan como `dudas` para F07.
4. Las transcripciones anteriores no se borran: quedan reemplazadas (`reemplaza_a`) y su
   carpeta `large-v3-int8-float16` intacta en `data/`.
5. Los binarios (WAV, v5) no se suben por API: quedan preparados en `data/drive_staging/`.

## Como ejecutarlo
```
uv run botsito corpus transcribe --video v5 --reemplaza-a tr-v5-large-v3-int8-float16-01a1ae03
uv run botsito corpus glossary apply
uv run botsito corpus transcript check
uv run botsito knowledge validate
```

## Como probarlo
`make regress` (= `make check`: lint, mypy strict, tests, contratos, state/config/knowledge
validate). Sin GPU: `uv run --no-sync pytest -q tests/unit/test_motor_prompt.py` (huella sin
GPU, guardia del prompt con tokenizador falso y, si large-v3 esta en la cache local, con el
real), `uv run --no-sync botsito corpus transcript check`, `knowledge validate`.

## Tests ejecutados
`make check` (`make regress`): 278 funciones de test (405 casos), 4 contratos, mypy strict,
state/config/knowledge validate. Nuevos: huella sin GPU (igual con otra GPU o con otro recuento
de tokens; distinta con otro ctranslate2/cuDNN/modelo/prompt/corte), guardia del prompt (vacio,
dentro del limite, limite exacto 223, truncado = error de dominio, tokenizador real si esta en
cache), configuracion sin `hotwords`, `_carpeta_base_registrada_ajena` (otra GPU no es ajena;
otro ctranslate2/modelo/prompt/corte/video si; manifiesto sin `corte`; otra carpeta no cuenta).
La GPU estuvo ocupada parte de la sesion: los tests se corrieron con `uv run --no-sync`, como
preve el HANDOFF.

## Resultados

### Medicion: initial_prompt frente a hotwords (v5, 365 s, GPU local)
Paso 1, tres pasadas de large-v3 sobre `data/transcripciones/v5/audio.wav` con los parametros
del pipeline (beam 5, temperatura 0, VAD, sin condicionar) y el vocabulario v2 (31 terminos en
esa lista, 29 en el glosario final): sin prompt, `initial_prompt`, `hotwords`. Script
`anexos/F07-previos/medir_prompt.py`, salidas `medir_*.txt` y `medir_resultado.json`:

| Variante | s | Diferencias de palabras frente a la anterior | Hechos |
|---|---|---|---|
| sin prompt | 81,0 | — | `bacteseando`; "se va a cumplir 13"; "espera, sell" |
| `initial_prompt` | 79,3 | 86 (casi todas puntuacion/mayusculas) | `backtesteando` (primera ventana); "13"; "sell"; repite "no hay entrada No hay entrada" en un borde |
| `hotwords` | 82,8 | 95 (casi todas puntuacion) | `backtesteando`; "cumple el 1, 3"; **"espera, SL"** donde el trader dice "sell" |

Paso 2, pasada OFICIAL con `corpus transcribe` y `hotwords` (id provisional
`tr-v5-...-e9a31700`, borrada sin commitear; cruda y manifiesto en
`anexos/F07-previos/v5_hotwords_*`): 22 segmentos frente a 99 (media 15,8 s frente a 3,2 s;
maximo 40,45 s, mas que la ventana de 30 s), `no_habla: 3`, y PERDIDA del tramo 0:03:12-0:03:35
"Y si yo protejo a 0.80, que es el SL por defecto, que no me permite dejarlo" (hecho A-10)
aunque el paso 1 con `hotwords` si lo contenia (29 frente a 31 terminos de prompt bastan para
otro camino de decodificacion). "sell" -> "SL" repetido (2 de 2). Conclusion: `hotwords`
alarga los segmentos mas alla de la ventana (mecanismo conocido de salto de audio en Whisper),
sesga hacia el vocabulario y no es estable; `initial_prompt` no mostro nada de eso.
Decision: `initial_prompt` (ADR-0007 sin cambio de motor) + sustituciones del glosario.
Leccion de metodo: medir SIEMPRE con la pasada oficial, no solo con el script suelto.

### Retranscripcion (v1-v5)
Los cinco videos con `corpus transcribe --reemplaza-a <id anterior>` (glosario v2 como
`initial_prompt`; 96 tokens reales, anotados como 99 en los 5 manifiestos porque la primera
version de la guardia contaba los 3 tokens especiales, corregido en la auditoria de cierre I-1;
misma GPU, versiones y corte que F04; ~1 h 5 min de GPU en total). Cada uno en carpeta nueva
`large-v3-int8-float16-<huella8>` (la huella cambio por el prompt); las carpetas y crudas
anteriores siguen en `data/` sin tocar. Comparacion cruda nueva frente a cruda reemplazada
(palabras normalizadas, `difflib`; `anexos/F07-previos/comparar.py`):

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
`voz` -> BOS (v2 seg 275, 0:31:20), `blogs` -> BOS (v4 seg 789, 0:46:58), `split` -> spread
(v4 seg 57, 0:06:06 y seg 131, 0:09:09), `sprint` -> spread (v4 seg 109, 0:08:27). Las demas
apariciones de esos patrones quedan como `dudas` en `correcciones.jsonl` (v2: 8, v3: 13,
v4: 4): F07 decide segmento a segmento ("un orden blog" en v2 0:08:05 es order block, no BOS).

### Copia fuera de esta maquina
- Drive: subcarpeta "transcripciones (crudas, Bot v3)" (id `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R`)
  dentro de "Estrategia del trader", creada por API con `SHA256SUMS.txt`, `LEEME.txt` y los 5
  manifiestos activos (texto, subidos por API en esta sesion).
- PENDIENTE del usuario (las herramientas de la sesion no suben binarios de ese tamano: el API
  del conector solo admite texto o base64 en el propio mensaje, y el navegador exige un dialogo
  nativo): arrastrar a esa carpeta el contenido de `data/drive_staging/` (21 ficheros, 625 MiB:
  5 `cruda.jsonl` + 5 `cruda.txt` + 5 manifiestos + 5 WAV + `2026-09-05 21-03-59.mkv`), cuyos
  sha256 estan en `SHA256SUMS.txt` y coinciden con `sha256_cruda`/`sha256_wav` de los
  manifiestos (comprobado por `anexos/F07-previos/staging.py` al copiar). Luego anotar el
  `drive_id` de v5 en `knowledge/corpus/fuentes.yaml` (hoy es una nota).

## Que deberia observar el usuario
`knowledge validate` en verde con 10 manifiestos de transcripcion; `transcript show --video v5
--t0 0:03:12 --t1 0:03:35 --capa cruda` con "y si yo protejo" y "a 0.80, que es el SL por
defecto"; el glosario con 12 sustituciones; la carpeta de Drive con SHA256SUMS y los 5
manifiestos.

## Que casos funcionan
Todo el alcance de la fila H.2 salvo la subida de binarios a Drive (queda en `drive_staging/`).

## Que casos todavia no funcionan
- `initial_prompt` solo condiciona la primera ventana de cada fragmento: la jerga del resto
  la corrige el glosario (sustituciones con ejemplo real), no el motor. Alternativa medida y
  descartada (`hotwords`). Otra alternativa no medida: `condition_on_previous_text=True` (fue
  descartada en F04 por bucles de repeticion).
- Las `dudas` del glosario (25 segmentos) no se resuelven aqui: F07 las mira al citar.
- `drive_id` de v5 y la copia de crudas/WAV dependen del usuario.

## Limitaciones
- Segmentos de hasta 55 s (v2) tambien con `initial_prompt`: la cita fina usa `palabras` (F07).
- Las marcas locales `huella.txt` de las carpetas de F04 (`large-v3-int8-float16/`) y de las
  cinco carpetas nuevas se escribieron con reglas de huella anteriores (con `gpu`; con
  `initial_prompt_tokens`): repetir exactamente esa configuracion en esta maquina abriria otra
  carpeta con sufijo y `comprobar_activa` pediria `--reemplaza-a`. No afecta a manifiestos ni a
  `knowledge validate` (verifican por `carpeta` y `sha256_cruda`); una retranscripcion futura
  (glosario v3) abre carpeta nueva de todos modos.
- Los 5 manifiestos anotan `initial_prompt_tokens: 99` (recuento con especiales) y son
  inmutables: el valor real es 96, documentado aqui y en el ADR.

## Riesgos
Si el usuario no sube `drive_staging/`, otra maquina no puede verificar `sha256_cruda` (solo
esquema e historial) ni regenerar sin ~1 h de GPU. Si F07 cita un segmento con `duda`, debe
mirar el audio.

## Impacto sobre funcionalidades anteriores
Los ids `tr-*` de F04 quedan reemplazados (nadie los citaba aun: F07 no ha empezado). El
esquema del manifiesto no cambia (campos nuevos dentro de `motor`, que es libre salvo
`modelo`). `huella_de` cambia para TODAS las carpetas: las de F04 pasan a ser "ajenas" por
manifiesto (`_carpeta_base_registrada_ajena`), lo que ya se comprobo al abrir carpetas nuevas.
La convencion de tags de MASTER_PLAN §F se amplia con las ramas de trabajo sin numero propio.

## Auditoria de cierre (dos agentes: codigo/tests y docs/proceso)
Codigo (sin bloqueantes; aplicado): I-1 `comprobar_prompt` contaba con `add_special_tokens`
por defecto (99 en vez de los 96 que ve el motor) -> `add_special_tokens=False`; I-2
`initial_prompt_tokens` entraba en la huella sin aportar informacion -> fuera de la huella;
M-1 la guardia corria despues de cargar los pesos en la GPU -> tokenizador desde
`tokenizer.json` antes de `WhisperModel`; M-2 marcas locales con la regla antigua (documentado
en Limitaciones); M-3 `ejemplo_t0` de `blogs` era 0:46:59 y el segmento empieza en 0:46:58
-> corregido; M-4 citas de "99 tokens" -> 96 con nota; T-1 tokenizador falso que no distinguia
los especiales -> distingue, mas limite exacto y tokenizador real si esta en cache; T-2 sin
cobertura de `_carpeta_base_registrada_ajena` -> 8 casos nuevos.
Docs/proceso (sin bloqueantes; aplicado): version del glosario `47ae19d7` -> `e55d5a2c` con la
aclaracion; ficheros modificados que la rama no tocaba (`cli.py`, `test_transcripcion.py`)
retirados; secciones de la plantilla (Como probarlo, Resultados, Limitaciones, Auditoria de
cierre, Que puede comprobar); evidencia de la medicion movida del scratchpad a
`docs/validation/anexos/F07-previos/`; nombre del tag ajustado a §F (decision 4); ids de v5 en
PROJECT_STATE/HANDOFF con la nota de reemplazo y el tramo 0:03:12-0:03:35; `verificado_por`
aclarado (decision 2); "Tests Currently Passing" con el detalle anterior; H.2 "hechos salvo
(3) y (4)"; Next Action alineado (Drive antes o despues del merge); componentes y lecciones
tecnicas en PROJECT_STATE/HANDOFF; `hotwords: null` explicado en el ADR; "~1 h 5 min" unificado.

## Que debe decidir el usuario
1. Ratificar que `hotwords` queda descartado y el motor sigue con `initial_prompt` (ADR-0007
   enmienda), con las sustituciones del glosario como via para la jerga.
2. Ratificar las 6 sustituciones de alcance segmento (BOS x3, spread x3). Hoy `verificado_por`
   registra la aprobacion de la propuesta del informe F04, no una escucha del audio; si
   prefiere oirlos, los minutos estan en el glosario, y cambiar el texto de `verificado_por`
   es una edicion manual del glosario (version nueva, `glossary apply`, sin retranscribir).
3. Subir `data/drive_staging/` a la carpeta de Drive y anotar el `drive_id` de v5 (dueno:
   usuario). Puede hacerse antes o despues del merge (solo cambia `fuentes.yaml`, regimen
   manual).
4. Cierre como rama con tag `stable/F05-previos-F07`: §F solo contemplaba `stable/F##` y
   `stable/F##-auditoria-N` (F## = ultima funcionalidad cerrada), asi que esta rama amplia §F
   con "rama de trabajo sin numero propio: `stable/F##-<tema>`". Alternativa: `stable/F07-previos`,
   que sugeriria que F07 esta cerrada cuando no se ha abierto (descartada por eso).

## Que puede comprobar sin recursos especiales
Sin GPU: `make check`; `uv run botsito knowledge validate` (10 manifiestos, corregida
recomputada); `uv run botsito corpus transcript show --video v5 --t0 0:03:12 --t1 0:03:35
--capa cruda`; `git diff stable/F05-auditoria-1..HEAD -- knowledge/corpus/glosario_asr.yaml`;
`sha256sum -c data/drive_staging/SHA256SUMS.txt` desde `data/drive_staging/`; en Drive, la
carpeta `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R` con SHA256SUMS, LEEME y 5 manifiestos; los anexos
de la medicion en `docs/validation/anexos/F07-previos/`.

## Estado
WAITING_FOR_USER_VALIDATION
