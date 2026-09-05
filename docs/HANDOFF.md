# HANDOFF · continuar Bot v3 desde otra terminal (2026-09-05)

Este fichero resume la conversacion que construyo F04 y deja el estado exacto para retomar.
Lee primero `PROJECT_STATE.md`; esto es el contexto humano que ahi no cabe.

## Estado
- Rama: `feature/F04-transcription-pipeline` (pusheada; CI verde). Main: `1c8346b`; tag
  `stable/F15` en `11ee1ac` (el merge). Protegida en GitHub (sin force-push, sin checks requeridos).
- F04 esta en WAITING_FOR_USER_VALIDATION: `docs/validation/F04-transcription-pipeline.md`.
- Cerradas y en main: F01, F02, F03, F06, F09, F15. Ramas fusionadas ya borradas (local y origin).
- Siguiente orden (E): F04 -> F05 -> F07 -> F08 -> F10 + sesion 1 con el trader.

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

## Que debe decidir el usuario para cerrar F04 (detalle en el informe)
1. 40 % frente a 50 % de la vela (queda como pregunta al trader).
2. Entradas propuestas para el glosario (con ejemplo real; cambian la huella, no se aplican solas).
3. Constantes de corte como hechos tecnicos, no de negocio.
4. Lo heredado de Whisper tiny no se cita.

## Comandos utiles
```
make check
uv run botsito knowledge validate
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus transcribe --video v1        # reanudable; no llama al modelo si ya esta
```

## Lecciones operativas
- Heredocs bash con comillas triples o barras invertidas fallan en Git Bash: escribir el script a
  un fichero del scratchpad y ejecutarlo.
- Escribir ficheros con `newline="\n"`; git en UTF-8 con `core.quotepath=false`.
- Agentes: pueden caer por limite de sesion; si pasa, hacer la auditoria a mano y decirlo.
- Dukascopy da 503/cortes: la descarga tiene cache por dia y reintentos.
