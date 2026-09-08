# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-07, F07 ronda 2 hecha; parada corta antes del cierre)
- `main`: merge de los previos de F07 `8cba5c5` con tag `stable/F05-previos-F07` (validados por
  el usuario el 2026-09-06); CI verde. Protegida en GitHub (sin force-push, sin checks requeridos).
- Cerradas y en main: F01, F02, F03, F04, F05, F06, F09, F15, la auditoria global
  (`stable/F05-auditoria-1`) y los previos de F07. Ramas fusionadas ya borradas (local y origin).
- Rama actual: `feature/F07-evidence-extraction` (informe
  `docs/validation/F07-evidence-extraction.md`, estado WAITING_FOR_USER_VALIDATION, ronda 2;
  cierre con tag `stable/F07`). HECHO: ADR-0009 (cita de audio localizada por tokens en la cruda
  con tiempo por `palabras`, comodin `[...]`, tolerancia 2 s; cita de pantalla anclada a un
  `fr-*` real; `evidence` no importa `corpus`); propuestas trazables en `knowledge/_proposals/`
  (20, selladas, con decision anotada, 0 pendientes; 91 `no_consta`); 341 items en
  `knowledge/evidence/` (commit `ff13e7a`; 334 audio, 4 pantalla, 3 ambas; 42 `provenance:
  bot-v2` por marca heredada; `revisado_por` "Aleks · hoja F07 2026-09-07 · cruda leida" o
  "· fotograma visto"); `_contradicciones.yaml` con 1 abierta (`stop.nivel` 0,75 vs 0,8 =
  A-10, se cierra con feedback tras la sesion 1); golden `tests/golden/f07_citas_referencia.yaml`
  (40 referencias) en verde; PROJECT_STATE con hechos y ambiguedades A-1..A-12 enlazados a ids.
- Decisiones del usuario (2026-09-07): acepto los 341 items sin modificaciones; `fotograma visto`
  en los 7 de pantalla/ambas; recall humano de V4 0:05-0:15 sin frases que faltaran; tag
  `stable/F07`; golden H4 sobre F15 pasa a F10 (ningun fotograma muestra la apertura de una H4).
- Copia fuera de la maquina COMPLETA (2026-09-06): carpeta de Drive "transcripciones (crudas,
  Bot v3)" (id `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R`) con SHA256SUMS, LEEME, 5 manifiestos, 5
  crudas, 5 WAV y el video v5 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`). Los binarios los
  sube el usuario a mano desde `data/drive_staging/`; una retranscripcion futura repite
  `staging.py` y la subida.
- SIGUIENTE: el usuario confirma el cierre -> ritual §F (`BOTSITO_ALLOW_MAIN=1 git merge --no-ff
  feature/F07-evidence-extraction`, `git tag -a stable/F07` sobre el merge, commit `docs(state)`
  que solo toca PROJECT_STATE.md, `make check`, push main + tag, CI verde) -> abrir F08
  evidence-retrieval (busqueda por texto y tiempo sobre los 341 items y las crudas; toda
  respuesta con fuente). Para anadir evidencia nueva: `evidence propose --video --t0 --t1
  --modelo <quien> --tema-buscado <raiz>...` -> rellenar `items`/`no_consta` (la cita se COPIA de
  la cruda, con sus repeticiones de borde) -> `--check` -> el usuario decide -> `evidence accept`
  o `reject`. Tras cambiar `scripts/git-hooks/`, ejecutar `make hooks`.
- Lecciones tecnicas (F07): el ASR repite palabras en los bordes de segmento ("tiene tiene",
  "no no"): la cita literal las incluye; los segmentos con `boss/voz/blog/split` fuera de las 6
  sustituciones quedan como `dudas` y obligan `confianza: media`; la ventana `t0/t1` debe cubrir
  las palabras localizadas (+-2 s), el `--check` dice donde estan; una cita de <4 tokens o con
  `0,75` donde la cruda dice `0.75` no se localiza a proposito.
- Lecciones tecnicas (previos de F07): con `condition_on_previous_text=False` el
  `initial_prompt` solo condiciona la primera ventana de 30 s de cada fragmento; `hotwords`
  entra en todas pero alarga los segmentos mas alla de la ventana (hasta 40 s) y Whisper salta
  audio (~10 s perdidos en v5, "sell" -> "SL"); faster-whisper trunca el prompt a 223 tokens
  sin avisar (guardia `comprobar_prompt`, contar con `add_special_tokens=False`); medir SIEMPRE
  con la pasada oficial (`corpus transcribe`), no solo con un script suelto (el paso 1 no
  mostro la perdida, el paso 2 si); el YAML estricto rechaza un valor que empieza por comillas
  y sigue texto (`motivo: "x" ...`): sin comillas o todo entrecomillado; `write_text` sin
  `newline="\n"` mete CRLF en Windows y rompe `test_repository_integrity`; las herramientas de
  la sesion no suben binarios grandes a Drive (API: texto/base64 en el mensaje; navegador:
  dialogo nativo; `file_upload`: 10 MB).

## F05 (validada el 2026-09-05)
- Fotogramas de TODO el corpus a 1 fps en PNG sin perdida (ADR-0008), decision del usuario
  ("maxima fidelidad, sin restriccion de recursos") tras medir que una regla de "tramos con
  decision" marca el 46-99 % de cada video. 5 videos: 16 548 fotogramas (8,9 GiB los cuatro de
  F05 + v5) en `data/fotogramas/` (solo en esta maquina; se regeneran en ~11 min con `corpus
  frames extract`). Manifiestos inmutables `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`,
  `fr-v4-9ad0ebb8`, `fr-v5-718ecabb` (uno activo por video).
- Informe `docs/validation/F05-frame-extraction.md`: obligatorios leidos, candidatos A-9, ficha
  de reglas en Word (`fr-v3-982da728/101000`), material del 2026-09-05 (v5, xlsx abril, capturas),
  dos auditorias de cierre aplicadas.
- Material del 2026-09-05 ("Info extra de backtesting"): v5 `2026-09-05 21-03-59.mkv` (6 min,
  FXReplay abril; `tr-v5-large-v3-int8-float16-01a1ae03`, 99 segmentos, reemplazada el 2026-09-06
  por `tr-v5-...-3c6fbb57`, 80; en Drive desde el 2026-09-06), xlsx
  abril 2026 (38 operaciones) y 6 capturas de Analytics en `Material adicional de su operativa`.
  Hechos en PROJECT_STATE (seccion "Lineamientos recibidos del usuario y hechos del corpus", ya con ids de evidencia desde F07).
- Lecciones tecnicas: `fps=1` de ffmpeg NO da el fotograma del segundo exacto ni conserva el
  `pts` (regla `select` + `-fps_mode passthrough`); `-ss` necesita `-copyts`; `showinfo` despues
  de `select`; `start_time` debe ser 0. Otra build de ffmpeg = otra carpeta y otro manifiesto con
  `--reemplaza-a`.

## Metodo de trabajo acordado con el usuario
1. Brief en `docs/plan/features/F##-*.md` -> revision de diseno por un agente ANTES de programar.
2. Construir en la rama; commits pequenos; `make check` (o `uv run --no-sync ...` si la GPU tiene
   abierto `botsito.exe`).
3. Auditoria de cierre con dos agentes en paralelo (codigo/tests y docs/proceso) -> aplicar
   correcciones -> informe WAITING_FOR_USER_VALIDATION -> decirle al usuario explicitamente que
   pasos seguir y que debe decidir.
4. El usuario valida -> ritual: `BOTSITO_ALLOW_MAIN=1 git merge --no-ff` -> `git tag -a stable/F##`
   sobre el merge -> commit `docs(state)` que solo toca PROJECT_STATE.md -> `make check` -> push
   main + tag. (`state check` falla a proposito entre el merge y el docs(state).) El HANDOFF ya
   vino actualizado en la rama.
5. Commits que toquen `knowledge/spec` o `knowledge/cases` necesitan trailer `Fuente: ADR-NNNN` o
   ids `ev-`/`fb-` existentes. `knowledge/evidence`, `knowledge/feedback`, `data/manifests`,
   `knowledge/corpus/transcripciones` y `knowledge/corpus/fotogramas` son inmutables (hook +
   historial de git).
6. El usuario exige evidencia (hechos / hipotesis / inferencias separados), no quiere
   recomendaciones prematuras y quiere saber siempre "que debo hacer ahora".

## Comandos utiles
```
make check
uv run botsito knowledge validate
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus transcribe --video v1        # reanudable; no llama al modelo si ya esta
uv run botsito corpus frames check
uv run botsito corpus frames show --video v3 --t 0:28:56 --n 3
uv run botsito corpus frames extract --video v5    # idempotente
```

## Lecciones operativas
- `knowledge validate` (guardia del trailer `Fuente:`) solo ve commits existentes: correrlo
  DESPUES de commitear cuando el commit toque `knowledge/spec` o `knowledge/cases` (README incluido).
- El clasificador del modo automatico de Claude Code bloquea `rebase`, `cherry-pick`, `branch -f`
  y a veces el merge a `main` con `BOTSITO_ALLOW_MAIN=1`: el usuario ejecuta esos comandos con `!`.
- La CI se consulta sin `gh`: `curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`
  (los logs del job requieren el token de `git credential fill`). El merge no tiene run propio: el
  que cuenta es el del `docs(state)`. Mirar SIEMPRE la CI de main tras el ritual.
- Heredocs bash con comillas simples anidadas o barras invertidas fallan en Git Bash: escribir el
  script a un fichero del scratchpad y ejecutarlo.
- Escribir ficheros con `newline="\n"`; git en UTF-8 con `core.quotepath=false`.
- Agentes: pueden caer por limite de sesion; si pasa, hacer la auditoria a mano y decirlo.
- Dukascopy da 503/cortes: la descarga tiene cache por dia y reintentos.
- Datos pesados (`data/transcripciones/`, `data/fotogramas/`) no estan en git: si se cambia de
  maquina, copiarlos o regenerarlos (transcribir ~1 h de GPU; fotogramas ~11 min).
