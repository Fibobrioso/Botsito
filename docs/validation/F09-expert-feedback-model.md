# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F09 · expert-feedback-model
**Rama:** `feature/F09-expert-feedback-model`
**Objetivo:** cada aportacion del trader como registro trazable y solo-anadir, con respuesta
literal, medio, objetivo tipado y accion; nunca modifica la evidencia (la supersede); cadena
evidencia → feedback reconstruible; todo cambio de spec o casos cita su fuente en el commit.

## Que se construyo
- `src/botsito/feedback/modelo.py`: `FeedbackRecord` (7 campos obligatorios, 6 opcionales), id
  `fb-<sesion>-<hash8>` por hash del contenido, carpeta = sesion, nombre = id; nueve acciones;
  seis tipos de objetivo con formato propio; tabla de coherencia accion/objetivo; acciones que
  exigen `valor_resultante`; medio distinto de `escrito` exige grabacion y minuto; `supersede`;
  `activos()`; `trazar()`; validacion contra contexto (evidencia existente, parametro del registro,
  contradiccion abierta, grabacion inventariada; regla/ambiguedad/caso por formato hasta F11/F14).
- `src/botsito/evidence/historial.py` generalizado: guardia por blobs para cualquier directorio
  (`knowledge/feedback/` incluido) y `commits_sin_fuente`: todo commit posterior a `stable/F06` que
  toque `knowledge/spec/` o `knowledge/cases/` debe llevar un trailer `Fuente:` con ids de
  evidencia, feedback o ADR existentes.
- Hook `pre-commit`: rechaza modificar, renombrar o borrar feedback (ademas de evidencia).
- CLI: `botsito feedback new`, `feedback trace <id>`, `feedback pending`; `knowledge validate`
  cubre feedback, su historial y los trailers `Fuente:`.
- `knowledge/feedback/README.md`: esquema, coherencia y plantilla de sesion.
- Contrato de capas refinado en `pyproject.toml`: `cases -> spec -> feedback -> evidencia/corpus/
  datos/config -> domain`. El contrato anterior tenia evidencia y feedback como hermanos
  independientes y se rompio (correctamente) al importar; la jerarquia nueva es la que el plan
  describe (seccion G y H).

## Archivos creados
```
src/botsito/feedback/modelo.py
tests/unit/test_feedback.py  tests/contract/test_feedback_history.py
docs/plan/features/F09-expert-feedback-model.md  docs/validation/F09-expert-feedback-model.md
```

## Archivos modificados
`src/botsito/evidence/historial.py` (generalizacion + trailers), `src/botsito/cli.py`,
`src/botsito/feedback/__init__.py`, `scripts/git-hooks/pre-commit`, `knowledge/feedback/README.md`,
`pyproject.toml` (capas), `tests/contract/test_evidence_history.py` (firma), `PROJECT_STATE.md`.

## Decisiones tomadas
- **`feedback apply` se difiere a F11** (con reason en el brief): sin esquema de `strategy_spec.yaml`
  no hay diff que proponer. `feedback pending` lista lo que F11 debera reflejar.
- **Trailer `Fuente:` desde `stable/F06`** y no desde el inicio: los commits anteriores crearon el
  esquema vacio del registro sin fuente de negocio. Los cambios de esquema futuros citan un ADR
  (`Fuente: ADR-NNNN`), los de valor citan evidencia o feedback.
- **Medio `escrito` sin grabacion**: la respuesta literal es el texto exacto del trader; los demas
  medios exigen grabacion inventariada y minuto, porque la sesion se graba (seccion H).
- **Coherencia accion/objetivo en el cargador**, no en la revision: un `RESOLVE_CONTRADICTION`
  sobre un tema sin contradiccion abierta no entra.

## Como ejecutarlo
```
make check
uv run botsito feedback new --sesion 2026-09-20-sesion-01 --fecha 2026-09-20 --medio escrito \
  --objetivo-tipo parametro --objetivo-id stop_fraccion --accion CONFIRM \
  --respuesta "si, el stop va al 0,75 siempre" --registrado-por aleks
uv run botsito feedback trace stop_fraccion
uv run botsito feedback pending
uv run botsito knowledge validate
```

## Como probarlo
- Crear un registro y editarlo a mano: `knowledge validate` falla por id; el hook rechaza el
  commit; con `--no-verify`, el test de historial falla.
- Tocar `knowledge/spec/parametros.yaml` y commitear sin `Fuente:`: `knowledge validate` nombra el
  commit.
- Un `LABEL_CASE` con objetivo `evidence`: rechazado por coherencia.

## Tests ejecutados
`make check` en `feature/F09-expert-feedback-model`, Windows 11. Hook probado en repositorio
temporal: acepta anadir feedback, rechaza editar y borrar.

## Resultados
- ruff, mypy strict (46 ficheros), 3 contratos KEPT con la jerarquia nueva.
- pytest: 131 passed (106 funciones; 14 rechazos parametrizados; property de estabilidad del id;
  historial con modificar/borrar; trailers validos, invalidos e inexistentes).
- `state`, `config`, `knowledge validate` (0 registros, historial intacto, commits con Fuente): OK.

## Que deberia observar el usuario
`knowledge/feedback/README.md` con esquema y plantilla de sesion; `feedback pending` vacio;
`knowledge validate` en verde; el hook rechazando una edicion de feedback.

## Que casos funcionan
Todo el alcance del brief salvo `feedback apply`, diferido a F11 por diseno.

## Que casos todavia no funcionan
- No hay registros reales: la sesion 1 con el trader va tras F10 y F15.
- Objetivos `regla`, `ambiguedad` y `caso` se validan solo por formato hasta F11/F14.
- CI de GitHub para esta rama: pendiente del push.

## Limitaciones
El trailer `Fuente:` se exige por commit, no por linea cambiada: un commit que mezcle un cambio
de esquema y uno de valor debe citar ambas fuentes.

## Riesgos
Sesiones sin grabacion: el modelo obliga a `escrito` con texto exacto; la paráfrasis del
intermediario queda excluida por construccion, no por disciplina.

## Impacto sobre funcionalidades anteriores
`historial.py` cambia de firma (directorio opcional, por defecto evidencia); los tests de F06
siguen en verde. `knowledge validate` es mas estricto.

## Estado
WAITING_FOR_USER_VALIDATION
