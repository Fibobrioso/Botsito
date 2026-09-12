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

Un fichero escrito a mano se carga con el cargador estricto: claves duplicadas rechazadas,
`fecha` sin comillas sigue siendo texto, pero `t0: 1:05:00` sin comillas es un entero para YAML y
se rechaza ("debe ser texto entre comillas"). La `fecha` es la de la `sesion`.

Desde F10 (ADR-0011): `ambiguedad` debe existir en `knowledge/spec/ambiguedades.yaml`; `grabacion`
puede ser un video de `fuentes.yaml` y `t1` no supera su `duracion_s`; `LABEL_CASE` usa la gramatica
de `knowledge/cases/kit/README.md` (`07-11: venta@08:37 e=...; 11-15: no_trade`).

Coherencia exigida: `RESOLVE_CONTRADICTION` solo sobre un tema con contradiccion abierta;
`RESOLVE_UNKNOWN` sobre parametro, ambiguedad o evidencia; `LABEL_CASE`, `MARK_*` y `BORDERLINE`
solo sobre casos; `CONFIRM/CORRECT/REJECT` sobre evidencia, regla o parametro. Ademas:
`respuesta_literal` tiene al menos 5 caracteres (no es un placeholder); `t0 < t1`; la `fecha` es
una fecha real y la de la `sesion`; los ids y tiempos solo admiten digitos ASCII; un campo en
blanco (`"   "`) cuenta como ausente y no entra en el id; `supersede` apunta a un registro del
MISMO objetivo y no puede formar ciclos; en la carpeta solo hay `*.yaml` (un `.yml` o cualquier
otro fichero es error). `botsito feedback new` comprueba el contexto ANTES de escribir (evidencia,
parametro del registro, contradiccion abierta, grabacion inventariada): si algo falla, no crea el
fichero, porque un registro es inmutable y un error solo se arreglaria con otro registro.

Todo cambio en `knowledge/spec/` o `knowledge/cases/` cita en el commit un trailer
`Fuente: <ids>` de evidencia, feedback o ADR EXISTENTES (`knowledge validate` lo comprueba; el
asunto del commit no cuenta como trailer). `feedback pending` omite los parametros que no son de
categoria `estrategia` (ADR-0004: no se le preguntan al trader).

## Material que llega fuera de sesion

El trader manda cosas por escrito entre sesiones: respuestas, capturas, backtests. Entra asi, en
este orden, y el 2026-09-11 se hizo a ojo porque esto no estaba escrito:

1. **Al corpus, nunca a la raiz**: `corpus/Estrategia del trader/Material adicional de su
   operativa/<Mensajes del trader | Backtest <mes> <ano> | ...>/`. Un fichero suelto en la raiz no
   tiene `papel` y `corpus check` lo rechaza con "no inventariado".
2. **`knowledge/corpus/fuentes.yaml`** gana o amplia esa subcarpeta con su papel, la fecha de
   entrega y LAS CAUTELAS: que holdout toca, en que convencion vienen sus cifras, que falta.
3. **`botsito corpus inventory`**: el hash entra en git; el binario no (`/corpus/` esta ignorado).
4. **Si trae una respuesta**, registro de feedback con `medio: escrito` y la ruta de la captura en
   `notas`. Si son SUS palabras (una captura), el `respuesta_literal` es literal; si lo refiere el
   consultor, el `registrado_por` tiene que decirlo -"REFERIDO por el consultor, no es
   transcripcion"- y la regla que se apoye en el declara `decision`.
5. **Si cierra una ambiguedad**, hace falta ADEMAS un registro con `objetivo: {tipo: ambiguedad}` y
   `accion: RESOLVE_UNKNOWN`: el del parametro escribe el valor, pero no cierra la pregunta. Hay
   guardia desde el 2026-09-12.
6. **Si toca un holdout o cambia una convencion de negocio**, se anota en el ADR que corresponda
   ANTES de citarlo en ningun sitio.

## Plantilla de sesion
1. Grabar la sesion y anadir la grabacion al corpus (manifiesto). F10 anade el papel
   `sesion_feedback` en `fuentes.yaml` para que una grabacion local sin `drive_id` sea
   inventariable.
2. Por cada respuesta: `botsito feedback new --sesion 2026-09-20-sesion-01 --fecha 2026-09-20
   --medio replay --grabacion "Material adicional de su operativa/sesion-01.mp4" \
   --t0 0:12:10 --t1 0:12:40
   --objetivo-tipo evidence --objetivo-id ev-v4-001533-… --accion CONFIRM
   --respuesta "si, con cuerpo, siempre" --registrado-por aleks`
3. `botsito knowledge validate`; commit con `Fuente:` si toca spec o casos (F11+).

Desde F11 el registro esta poblado: `--objetivo-tipo parametro` es la via normal, y `botsito
feedback apply --sesion <s>` lleva los valores al registro sin interpretar nada.