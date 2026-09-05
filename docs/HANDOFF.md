# HANDOFF · continuar Bot v3 desde otra terminal (2026-09-05, actualizado al cerrar F05)

## Estado F05 (2026-09-05, rama `feature/F05-frame-extraction`, WAITING_FOR_USER_VALIDATION)
- Fotogramas de TODO el corpus a 1 fps en PNG sin perdida (ADR-0008): decision del usuario
  ("maxima fidelidad, sin restriccion de recursos") tras medir que una regla de tramos marca el
  46-99 % de cada video. 16 182 fotogramas, 8,9 GiB en `data/fotogramas/` (solo en esta
  maquina; se regeneran en ~11 min con `corpus frames extract`). Manifiestos inmutables
  `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`, `fr-v4-9ad0ebb8` (un activo por video).
- Informe: `docs/validation/F05-frame-extraction.md` (obligatorios leidos, candidatos A-9, ficha
  de reglas en Word en `fr-v3-982da728/101000`, dos auditorias aplicadas).
- Inmutables ahora: evidence, feedback, data/manifests, corpus/transcripciones, corpus/fotogramas
  (`make hooks` para instalar el hook nuevo).
- Siguiente tras validar: ritual de merge (tag `stable/F05`) y abrir F07 con `referencias_conocidas`
  (`corpus/manifiestos_fotogramas.py`) conectada a `validar_contra_manifiesto` y a `evidence new`;
  antes de F07: glosario v2 -> retranscribir -> copia de crudas en Drive.
- Leccion: `fps=1` de ffmpeg NO da el fotograma del segundo exacto ni conserva el `pts`; `-ss`
  necesita `-copyts`; showinfo despues de `select`. Los comandos que el clasificador bloquea
  (merge a main, rebase) los ejecuta el usuario con `!`.

## Contexto previo (F04)

Este fichero resume la conversacion que construyo F04 y deja el estado exacto para retomar.
Lee primero `PROJECT_STATE.md`; esto es el contexto humano que ahi no cabe.

## Estado (actualizado al cerrar F04, 2026-09-05)
- Rama actual: `main` en `415f496` (docs(state)); merge de F04 `a7f8b4b` con tag `stable/F04`;
  CI verde en main (run 33987802513). Protegida en GitHub (sin force-push, sin checks requeridos).
- F04 VALIDADA por el usuario el 2026-09-05. Decisiones: A-12 (40/50 % de la vela) queda como
  pregunta al trader; glosario v2 se aplica como paso previo a F07 (retranscribir los 4 videos con
  `--reemplaza-a`, luego copia de cruda/WAV en Drive); constantes de corte son tecnicas; lo
  heredado de Whisper tiny no se cita.
- Cerradas y en main: F01, F02, F03, F04, F06, F09, F15. Ramas fusionadas borradas (local y origin).
- SIGUIENTE: abrir `feature/F05-frame-extraction`. Brief desde MASTER_PLAN tabla A (F05 depende
  de F03 y F04) y H.2 fila F05: tramos con decision derivados de la transcripcion activa `tr-*`
  mas huecos heredados de F03; fotogramas obligatorios V3 0:28:56 (Excel 2,3/3,23 vs 2.83/3.33),
  V2 0:33:21 (4,08/3,94), V4 0:12:30 (1,19537) y configuracion del grafico para A-9. Metodo:
  brief -> revision de diseno por agente -> construir -> auditoria de cierre (2 agentes) -> informe.
- Orden (E) restante: F05 -> F07 -> F08 -> F10 + sesion 1 con el trader.

## Metodo de trabajo acordado con el usuario
1. Brief en `docs/plan/features/F##-*.md` -> revision de diseno por un agente ANTES de programar.
2. Construir en la rama; commits pequenos; `make check` (o `uv run --no-sync ...` si la GPU tiene
   abierto `botsito.exe`).
3. Auditoria de cierre con dos agentes en paralelo (codigo/tests y docs/proceso) -> aplicar
   correcciones -> informe WAITING_FOR_USER_VALIDATION -> decirle al usuario explicitamente que
   pasos seguir.
4. El usuario valida -> ritual: `BOTSITO_ALLOW_MAIN=1 git merge --no-ff` -> `git tag -a stable/F##`
   sobre el merge -> commit `docs(state)` que solo toca PROJECT_STATE.md -> `make check` -> push
   main + tag. (`state check` falla a proposito entre el merge y el docs(state).)
5. Commits que toquen `knowledge/spec` o `knowledge/cases` necesitan trailer `Fuente: ADR-NNNN` o
   ids `ev-`/`fb-` existentes. `knowledge/evidence`, `knowledge/feedback`, `data/manifests` y
   `knowledge/corpus/transcripciones` son inmutables (hook + historial de git).
6. El usuario exige evidencia (hechos / hipotesis / inferencias separados), no quiere
   recomendaciones prematuras y quiere saber siempre "que debo hacer ahora".

## Lo hecho en esta conversacion (5 sep 2026)
- F09 y F15 validadas y fusionadas (tags `stable/F09`, `stable/F15`); ADR-0006 (capas).
- MT5 + FundedNext demo verificados con la API de solo lectura (ver PROJECT_STATE).
- F04 (ADR-0007): un WAV por video, corte por muestras en silencios (600/420/780 s, -35 dB,
  0,5 s), faster-whisper large-v3 `int8_float16` en la GTX 1650 (grupo `asr`), cruda inmutable
  con manifiesto `tr-<video>-<motor>-<hash8>`, corregida = cruda + glosario verificada por
  recomputo, CLI `corpus transcribe | glossary apply | transcript check | transcript show`,
  capa en `knowledge validate`, hook protege el directorio.
- Cuatro videos transcritos (ids 00fcaf53, ac6b337b, 570a315f, 3f8c826e); determinismo verificado
  (fragmento retranscrito identico); 33 marcas heredadas revisadas (tabla en el informe).
- Hallazgo: V1 0:15:59 dice "50 % de la vela" (la heredada decia 40 %). Ambiguedad A-12 (sesion 1).
- Hook: `uv lock --check` + `uv run --no-sync` (con `--locked` fallaba mientras la GPU usaba el
  ejecutable). Detector de literales admite `# no-negocio: <motivo>`.
- Datos pesados en `data/transcripciones/` (no en git): si se cambia de maquina, copiar esa
  carpeta o retranscribir (~1 h de GPU); sin ella, `knowledge validate` solo avisa.

## Auditoria final de F04 (2 agentes, 2026-09-05, antes de validar)
- Codigo (`b1a7107`): `video.sha256` por carpeta de trabajo (video cambiado -> otra carpeta antes
  de la GPU), cita de un instante en el borde de un segmento, glosario rechaza `\w+`/`\d+`/`[..]+`,
  `glossary apply --video` inexistente es error, temporal `_<id>.yaml.tmp`, 1 ms de redondeo no
  es recorte, `cargar_todos` detecta ids repetidos y ciclos.
- Plan (`75c9dda`): regla de cita de F07 contra la CRUDA (MASTER_PLAN H, ADR-0007 §7), secuencia
  glosario v2 -> retranscribir -> Drive -> F07, F05 depende de F04 (fila H.2 nueva), plantillas
  de brief e informe con revision de diseno / auditoria de cierre / decisiones del usuario,
  regimenes de cambio completos, A-1..A-12, 33 marcas.
- Incidente: el commit de docs toco `knowledge/spec/README.md` sin trailer `Fuente:`; la CI lo
  detecto (make check local corrio ANTES del commit). Se reescribio con `Fuente: ADR-0005`.

## Comandos utiles
```
make check
uv run botsito knowledge validate
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus transcribe --video v1        # reanudable; no llama al modelo si ya esta
```

## Lecciones operativas
- `knowledge validate` (guardia del trailer `Fuente:`) solo ve commits existentes: correrlo
  DESPUES de commitear cuando el commit toque `knowledge/spec` o `knowledge/cases` (README incluido).
- El clasificador del modo automatico de Claude Code bloquea `rebase`, `cherry-pick`, `branch -f`
  y el merge a `main` con `BOTSITO_ALLOW_MAIN=1`: el usuario ejecuta esos comandos con `!`.
- La CI se consulta sin `gh`: `curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`
  (los logs del job requieren el token de `git credential fill`).
- Heredocs bash con comillas triples o barras invertidas fallan en Git Bash: escribir el script a
  un fichero del scratchpad y ejecutarlo.
- Escribir ficheros con `newline="\n"`; git en UTF-8 con `core.quotepath=false`.
- Agentes: pueden caer por limite de sesion; si pasa, hacer la auditoria a mano y decirlo.
- Dukascopy da 503/cortes: la descarga tiene cache por dia y reintentos.
