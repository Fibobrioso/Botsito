# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-06, previos de F07 construidos)
- `main`: merge de la auditoria global `916d0d0` con tag `stable/F05-auditoria-1` (las tres
  ratificaciones del usuario el 2026-09-06); `docs(state)` `76060c9`; CI verde (run
  34044627478). Protegida en GitHub (sin force-push, sin checks requeridos).
- Cerradas y en main: F01, F02, F03, F04, F05, F06, F09, F15 y la auditoria global. Rama
  `feature/F05-auditoria-estructura` fusionada (pendiente de borrar por el usuario).
- Rama actual: `feature/F07-previos` (informe `docs/validation/F07-previos.md`, estado
  WAITING_FOR_USER_VALIDATION; cierre con tag `stable/F07-previos`). Hecho: glosario v2
  (29 terminos, 6 sustituciones globales + 6 de segmento), `hotwords` medido y DESCARTADO
  (perdida de habla y sesgo "sell" -> "SL"; ADR-0007 enmienda), guardia de 223 tokens del
  prompt, huella de reanudacion sin GPU, los 5 videos retranscritos (ids activos:
  `tr-v1-...-bbd8a931`, `tr-v2-...-28391c2c`, `tr-v3-...-270a4851`, `tr-v4-...-a8d1bccc`,
  `tr-v5-...-3c6fbb57`; los anteriores quedan reemplazados, sus carpetas siguen en `data/`).
- Copia fuera de la maquina: carpeta de Drive "transcripciones (crudas, Bot v3)" (id
  `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R`, dentro de "Estrategia del trader") con SHA256SUMS,
  LEEME y los manifiestos subidos por API; crudas, WAV y el video v5 (625 MiB en total)
  estan preparados en `data/drive_staging/` para que el usuario los arrastre (las
  herramientas de la sesion no suben binarios de ese tamano). Al subir v5, anotar su
  `drive_id` en `knowledge/corpus/fuentes.yaml`.
- SIGUIENTE: abrir F07 evidence-extraction (entradas en MASTER_PLAN H.2, fila "Previos y
  entradas de F07"; la cita se verifica contra la CRUDA de la transcripcion activa).

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
  FXReplay abril; `tr-v5-large-v3-int8-float16-01a1ae03`, 99 segmentos; NO esta en Drive), xlsx
  abril 2026 (38 operaciones) y 6 capturas de Analytics en `Material adicional de su operativa`.
  Hechos en PROJECT_STATE (seccion "Hechos del corpus pendientes de evidencia").
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
