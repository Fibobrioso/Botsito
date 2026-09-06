# knowledge/evidence/ — evidencia INMUTABLE (F06)

Un fichero por item, en `<video_id>/<id>.yaml`. El `id` es `ev-<video>-<hhmmss>-<hash8>` y el hash
es del contenido: editar un item rompe su id, y el historial de git se vigila
(`tests/contract/test_evidence_history.py`, hook `pre-commit`). Una correccion es un item nuevo con
`supersede: <id anterior>`. Crear items con `botsito evidence new` para no calcular el id a mano.

## Esquema

| Campo | Obligatorio | Valores |
|---|---|---|
| `id` | si (calculado) | `ev-v4-001533-1a2b3c4d` |
| `video_id` | si | `v1..v5` segun `knowledge/corpus/fuentes.yaml` |
| `t0`, `t1` | si | `h:mm:ss[.d]`, `t0 < t1 <= duracion del video` |
| `modalidad` | si | `audio` · `pantalla` · `ambas` |
| `tipo` | si | `RULE_STATEMENT` · `PARAMETER` · `EXAMPLE_TRADE` · `NO_TRADE` · `MANAGEMENT` · `UNKNOWN` |
| `cita_literal` | si | lo que se dice o se ve, tal cual; nunca una parafrasis |
| `afirmacion` | si | normalizacion de la cita; no puede anadir condiciones que la cita no diga |
| `tema` | si | clave jerarquica, p. ej. `stop.nivel`, `mitigacion.m15.cierre` |
| `valor` | no | texto normalizado del valor (`"0.75"`, `"cuerpo"`); dos temas iguales con valor distinto = contradiccion |
| `confianza` | si | `alta` · `media` · `baja` |
| `extractor` | si | `humano` · `llm` (una propuesta de LLM aceptada por una persona) |
| `revisado_por` | si | quien verifico la cita contra el video |
| `provenance` | si | `botsito` (extraido en este proyecto) · `bot-v2` (importado; re-citado obligatoriamente) |
| `fotogramas` | no | rutas del manifiesto del corpus |
| `supersede` | no | id del item al que corrige |
| `notas` | no | texto libre |

Reglas adicionales que el cargador hace cumplir: `cita_literal` de al menos 5 caracteres;
`afirmacion` no mas larga que `2 x cita + 40`; tiempos e ids solo con digitos ASCII; un campo en
blanco cuenta como ausente y no entra en el id; `supersede` apunta a un item del MISMO `tema` y no
puede formar ciclos; en la carpeta solo hay `*.yaml` (cualquier otro fichero es error).
`botsito evidence new` comprueba contra el manifiesto ANTES de escribir (duracion del video,
fotogramas inventariados, supersede existente): si algo falla, no crea el fichero.

`_contradicciones.yaml` es GENERADO (`botsito evidence contradictions`) y `knowledge validate` falla
si no coincide con la regeneracion. Las inferencias del equipo NO son evidencia: van a la
especificacion como ambiguedad o regla `DEFAULT` (seccion H del plan).
