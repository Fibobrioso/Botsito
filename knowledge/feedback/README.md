# knowledge/feedback/ — registros del trader, SOLO ANADIR (F09)

Un fichero por registro, en `<sesion>/<id>.yaml`, con `id = fb-<sesion>-<hash8>` (hash del
contenido). Editar un registro rompe su id; el hook y `tests/contract/test_feedback_history.py`
rechazan modificarlo o borrarlo. Una correccion es un registro nuevo con `supersede`. Crear con
`botsito feedback new`. Ver la cadena con `botsito feedback trace <id>`.

## Esquema

| Campo | Obligatorio | Valores |
|---|---|---|
| `sesion` | si | `AAAA-MM-DD-sesion-NN` (carpeta) |
| `fecha` | si | `AAAA-MM-DD` |
| `medio` | si | `replay` · `audio` · `video` · `escrito` |
| `grabacion`, `t0`, `t1` | si, salvo `escrito` | ruta de la grabacion de la sesion en el corpus y minuto exacto de la respuesta |
| `objetivo` | si | `{tipo, id}` con tipo en `evidence` (`ev-…`) · `regla` (`RN-NNN`) · `parametro` (nombre del registro) · `ambiguedad` (`A-N`) · `caso` (`caso-…`) · `contradiccion` (tema) |
| `accion` | si | `CONFIRM` · `CORRECT` · `REJECT` · `RESOLVE_UNKNOWN` · `RESOLVE_CONTRADICTION` · `LABEL_CASE` · `MARK_FALSE_POSITIVE` · `MARK_FALSE_NEGATIVE` · `BORDERLINE` |
| `respuesta_literal` | si | lo que dijo o escribio el trader, tal cual |
| `valor_resultante` | si para `CORRECT`, `RESOLVE_*`, `LABEL_CASE` | valor normalizado que queda |
| `registrado_por` | si | quien transcribio la respuesta |
| `supersede` | no | id del registro que corrige |
| `notas` | no | texto libre |

Coherencia exigida: `RESOLVE_CONTRADICTION` solo sobre un tema con contradiccion abierta;
`LABEL_CASE`, `MARK_*` y `BORDERLINE` solo sobre casos; `CONFIRM/CORRECT/REJECT` sobre evidencia,
regla o parametro. Todo cambio en `knowledge/spec/` o `knowledge/cases/` cita en el commit un
trailer `Fuente: <ids>` de evidencia, feedback o ADR (`knowledge validate` lo comprueba).

## Plantilla de sesion
1. Grabar la sesion y anadir la grabacion al corpus (manifiesto).
2. Por cada respuesta: `botsito feedback new --sesion 2026-09-20-sesion-01 --fecha 2026-09-20
   --medio replay --grabacion "Material adicional/sesion-01.mp4" --t0 0:12:10 --t1 0:12:40
   --objetivo-tipo evidence --objetivo-id ev-v4-001533-… --accion CONFIRM
   --respuesta "si, con cuerpo, siempre" --registrado-por aleks`
3. `botsito knowledge validate`; commit con `Fuente:` si toca spec o casos (F11+).
