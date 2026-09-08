# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-08, fase 1 cerrada en main; F10 construida, espera validacion)
- `main`: merge de F08 `5d8cf3c` con tag `stable/F08` (fase 1 F03-F08 cerrada); `docs(state)`
  `645aac6`; CI verde. Protegida en GitHub.
- Cerradas y en main: F01-F09 (salvo las no iniciadas), F15, la auditoria global y los previos
  de F07. Ramas fusionadas borradas.
- Rama actual: `feature/F10-elicitation-kit` (informe `docs/validation/F10-elicitation-kit.md`,
  WAITING_FOR_USER_VALIDATION; cierre con tag `stable/F10`). HECHO: ADR-0011;
  `knowledge/spec/ambiguedades.yaml` (A-1..A-12 legibles por maquina); registro con 24
  parametros de estrategia en UNKNOWN; `knowledge/cases/kit/{config,mapa_parametros,vistos}.yaml`
  (cifras de negocio como datos; enero, julio y agosto VISTOS por el trader); paquete `cases`
  (cuestionario de 21 preguntas con casos `ev-*`, ventanas de dias no vistos de mayo y junio de
  2026 con hash y limites H4 por anclaje, particiones por hash con seed, kappa desde los
  `LABEL_CASE`); CLI `kit build|check|kappa`; `knowledge validate` capa kit con guardia de
  ancestro (particiones commiteadas antes del primer `LABEL_CASE`); paquete real
  `knowledge/cases/kit/2026-09-15-sesion-01/` (fecha provisional).
- SIGUIENTE: el usuario valida F10 -> ritual §F (`BOTSITO_ALLOW_MAIN=1 git merge --no-ff
  feature/F10-elicitation-kit`, `git tag -a stable/F10`, `docs(state)`, `make check`, push, CI)
  -> SESION 1 con el trader: (1) confirmacion escrita de que no ha visto mayo/junio (registro
  F09 `medio: escrito`), (2) las 3 preguntas bloqueantes (A-9 con captura del grafico, A-2, A-4)
  y el resto de `hoja_trader.md`, (3) etiquetado de los 16 casos `dev` por sesion H4 con la
  gramatica del kit; cada respuesta = `botsito feedback new` (`RESOLVE_UNKNOWN` sobre
  `ambiguedad`/`parametro`, `LABEL_CASE` sobre `caso`); despues F11 strategy-spec-schema. Si la
  fecha de la sesion no es 2026-09-15: `kit build --sesion <fecha>-sesion-01 --seed 20260915` y
  commit ANTES de la sesion. Todo commit bajo `knowledge/spec` o `knowledge/cases` lleva
  `Fuente:`.
- Lecciones tecnicas (F10): Dukascopy devuelve 503 y resets a mitad de mes: `data download`
  cachea por dia y se relanza hasta que el manifiesto existe; los literales de negocio no pueden
  ir en `src/` (`config.yaml` del kit); `random.shuffle` no es estable entre versiones (orden por
  hash); la guardia de fecha de commit se falsifica, la de ancestro no; el trader decide por
  sesion H4, no por dia.
- Lecciones tecnicas (F08): el token de CITA (F07, fiel a la cruda) y el token de BUSQUEDA (F08,
  acentos plegados y `0,75` = `0.75`) son distintos a proposito; `localizar_cita` no sirve para
  buscar frases (minimos de 4/3 tokens, una ventana, una localizacion): `buscar_secuencia` es la
  base comun; los segmentos de Whisper son de 5-15 s, asi que el AND va por segmento y la frase
  puede cruzar segmentos; `frames show` (mas cercano por pts) y `kb` (regular anterior
  existente, `referencia_en`) responden preguntas distintas.
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
uv run botsito kb find "break even" --top 10       # busqueda con fuente (F08)
uv run botsito kb at --video v4 --t 0:44:56 --contexto
uv run botsito kit build --sesion 2026-09-15-sesion-01 --seed 20260915   # paquete de sesion (F10)
uv run botsito kit check --sesion 2026-09-15-sesion-01
uv run botsito kit kappa --sesion-a 2026-09-15-sesion-01 --sesion-b 2026-09-22-sesion-02
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
