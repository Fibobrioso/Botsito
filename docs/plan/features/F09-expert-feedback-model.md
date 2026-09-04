# F09 · expert-feedback-model

**Rama:** `feature/F09-expert-feedback-model` · **Fase:** 2 · **Depende de:** F06

## Objetivo
Definir `FeedbackRecord`: cada aportacion del trader como un registro trazable, solo-anadir, con
respuesta literal, medio, objetivo (que item, regla, parametro, ambiguedad o caso corrige) y
accion. Nunca modifica la evidencia: la supersede. La cadena evidencia → feedback → regla debe
poder reconstruirse (`botsito feedback trace`).

## Alcance cerrado (que SI)
- `src/botsito/feedback/modelo.py`: esquema, id `fb-<sesion>-<hash8>` (hash del contenido),
  carga, validacion; acciones `CONFIRM · CORRECT · REJECT · RESOLVE_UNKNOWN ·
  RESOLVE_CONTRADICTION · LABEL_CASE · MARK_FALSE_POSITIVE · MARK_FALSE_NEGATIVE · BORDERLINE`;
  objetivo tipado (`evidence | regla | parametro | ambiguedad | caso | contradiccion`); medio
  (`replay | audio | video | escrito`); cita de la grabacion de la sesion (`grabacion`, `t0`, `t1`)
  obligatoria salvo medio `escrito`, que exige el texto exacto del trader; `respuesta_literal`
  obligatoria; `registrado_por` obligatorio; `supersede` a otro registro.
- Coherencia accion/objetivo: `RESOLVE_CONTRADICTION` exige objetivo `contradiccion` (tema) y
  `valor_resultante`; `RESOLVE_UNKNOWN` exige `valor_resultante`; `LABEL_CASE`, `MARK_*` y
  `BORDERLINE` exigen objetivo `caso`; `CONFIRM/CORRECT/REJECT` exigen `evidence`, `regla` o
  `parametro`.
- Validacion contra lo que existe: objetivo `evidence` debe ser un id de evidencia real;
  `parametro` un nombre del registro; `contradiccion` un tema con contradiccion abierta;
  `regla`, `ambiguedad` y `caso` solo por formato hasta F11/F14 (anotado).
- Guardia de historial generalizada (`evidence/historial.py` acepta directorio) aplicada a
  `knowledge/feedback/`; hook extendido.
- Trazabilidad de cambios en la especificacion: todo commit posterior a `stable/F06` que toque
  `knowledge/spec/` o `knowledge/cases/` debe llevar un trailer `Fuente: <ids>` con ids de evidencia
  o de feedback existentes (`historial.commits_sin_fuente`); `knowledge validate` lo comprueba.
- CLI: `botsito feedback new` (valida contra el contexto antes de escribir), `botsito feedback
  trace <id>` (el item de evidencia si `<id>` lo es, y los registros de feedback sobre ese id con
  sus supersedes), `botsito feedback pending` (registros activos; hasta F11 todos salvo los de
  parametros que no son de `estrategia`); `knowledge validate` cubre feedback, historial y
  trailers.
- `knowledge/feedback/README.md` con el esquema y la plantilla de sesion.

## Fuera de alcance (que NO)
`feedback apply` (diff propuesto sobre `strategy_spec.yaml`): la spec no existe hasta F11; se
implementa alli con el esquema real. Kit de elicitacion (F10). Reglas con valor.

## Entradas
`knowledge/evidence/` (ids), `knowledge/spec/parametros.yaml` (nombres), `_contradicciones.yaml`.

## Salidas (ficheros)
`src/botsito/feedback/modelo.py`, `src/botsito/evidence/historial.py` (generalizado),
`knowledge/feedback/README.md`, tests, hook, informe.

## Tests
- Unit: esquema; id por hash; coherencia accion/objetivo (tabla); objetivo evidence inexistente;
  parametro inexistente; contradiccion no abierta; medio escrito sin texto; supersede; trace.
- Contract: historial de feedback (modificar/borrar/merge); commits sin trailer detectados en
  repo temporal y ninguno en el real desde `stable/F06`.
- Property: id estable ante espacios; cambia con contenido.

## Criterio de aceptacion
`make check` verde; un registro sin respuesta literal, sin cita o con accion incoherente es
rechazado; editar un registro commiteado rompe id, hook y test de historial; un commit que toque
`knowledge/spec/` sin `Fuente:` falla `knowledge validate`; informe WAITING_FOR_USER_VALIDATION.

## Riesgos
Trailer olvidado en commits legitimos de esquema (F11): el brief de F11 debe usar `Fuente: ADR-xxxx`
para cambios de esquema sin valor; se admite `ADR-\d{4}` como fuente.

## Que habilita
F10 (kit de elicitacion genera plantillas de registro), F11 (estados de regla derivados de
evidencia + feedback), F14 (etiquetas de casos como registros LABEL_CASE).
