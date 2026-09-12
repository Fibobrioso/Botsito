# knowledge/evidence/ — evidencia INMUTABLE (F06, F07)

Un fichero por item, en `<video_id>/<id>.yaml`. El `id` es `ev-<video>-<hhmmss>-<hash8>` y el hash
es del contenido: editar un item rompe su id, y el historial de git se vigila
(`tests/contract/test_evidence_history.py`, hook `pre-commit`). Una correccion es un item nuevo con
`supersede: <id anterior>`. Crear items con `botsito evidence new` (o `evidence accept` desde una
propuesta de `knowledge/_proposals/`) para no calcular el id a mano y para que la cita se verifique
ANTES de escribir (F07, ADR-0009): la de audio se localiza en la CRUDA de `transcripcion`; la de
pantalla exige un fotograma real `fr-<id>/<t_ms>` del tramo.

## Esquema

| Campo | Obligatorio | Valores |
|---|---|---|
| `id` | si (calculado) | `ev-v4-001533-1a2b3c4d` |
| `video_id` | si | `v1..v6` segun `knowledge/corpus/fuentes.yaml` |
| `t0`, `t1` | si | `h:mm:ss[.d]`, `t0 < t1 <= duracion del video` |
| `modalidad` | si | `audio` · `pantalla` · `ambas` |
| `tipo` | si | `RULE_STATEMENT` · `PARAMETER` · `EXAMPLE_TRADE` · `NO_TRADE` · `MANAGEMENT` · `UNKNOWN` |
| `cita_literal` | si | lo que se dice o se ve, tal cual; nunca una parafrasis |
| `afirmacion` | si | normalizacion de la cita; no puede anadir condiciones que la cita no diga |
| `tema` | si | clave jerarquica, p. ej. `stop.nivel`, `mitigacion.m15.cierre` |
| `valor` | no | texto del valor tal como aparece en la cita o cerrado en `_temas.yaml` (`"0.75"`, `"4,08"`, `"cuerpo"`); la coma se conserva si la cita la trae; `evidence contradictions` compara valores normalizados: dos temas iguales con valor distinto = contradiccion |
| `confianza` | si | `alta` · `media` · `baja` |
| `extractor` | si | `humano` · `llm` (una propuesta de LLM aceptada por una persona) |
| `revisado_por` | si | quien acepto el item y con que metodo (`"<persona> · hoja F07 <fecha> · cruda leida"` o `"... · fotograma visto"`); la cita de audio la verifica la maquina contra la cruda; la persona revisa que `afirmacion`, `tema` y `valor` no digan mas que la cita, y en pantalla que el fotograma muestre lo citado |
| `provenance` | si | `botsito` (extraido en este proyecto) · `bot-v2` (importado; re-citado obligatoriamente) |
| `fotogramas` | no (si en `pantalla`/`ambas`) | referencias `fr-<id>/<t_ms>` del mismo video dentro de `[t0 - 1 s, t1 + 1 s]` (ADR-0008 §6) o rutas `material_adicional` acompanadas de un `fr-*` del tramo; `audio` no las admite; lo heredado (`_procesado/`) no se cita |
| `transcripcion` | si en `audio`/`ambas`, no en `pantalla` | id `tr-*` de la cruda donde se localiza la cita (la activa del video al crear el item) |
| `supersede` | no | id del item al que corrige |
| `notas` | no | texto libre |

Regla de la cita de audio (F07): `cita_literal` se COPIA de la cruda tal cual, con sus errores
del ASR (`m 15`, `breakeven`, `1.3` cuando el trader dice "uno a tres"); `afirmacion` y `valor`
normalizan (`1:3`) y `notas` explica la lectura. Se localiza POR TOKENS (numeros con separador
interior como un token; acentos conservados; `0.75` y `0,75` son distintos) dentro de los
segmentos que tocan `[t0 - 2 s, t1 + 2 s]`, con el comodin `[...]` para omitir palabras (maximo 2;
cada trozo >= 3 tokens; cita >= 4 tokens), y su tiempo real por `palabras` debe caer en esa
ventana. `tema`: raiz en `_temas.yaml` (cerrada para F07; F11 la hara normativa).

Reglas adicionales que el cargador hace cumplir: `cita_literal` de al menos 5 caracteres;
`afirmacion` no mas larga que `2 x cita + 40`; tiempos e ids solo con digitos ASCII; un campo en
blanco cuenta como ausente y no entra en el id; `supersede` apunta a un item del MISMO `tema` y no
puede formar ciclos; en la carpeta solo hay `*.yaml` (cualquier otro fichero es error).
`botsito evidence new` comprueba contra el manifiesto y el contexto ANTES de escribir (duracion
del video, referencias de fotogramas conocidas, transcripcion activa, cita localizada en la
cruda, supersede existente): si algo falla, no crea el fichero. `knowledge validate` repite esas
comprobaciones sobre todos los items; sin la cruda en `data/`, avisa "no verificables aqui".

`_contradicciones.yaml` es GENERADO (`botsito evidence contradictions`) y `knowledge validate` falla
si no coincide con la regeneracion. Las inferencias del equipo NO son evidencia: van a la
especificacion como ambiguedad o regla `DEFAULT` (seccion H del plan).
