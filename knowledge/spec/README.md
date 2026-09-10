# knowledge/spec/ — StrategySpec (F11) y registro de parametros (F02).

- `parametros.yaml`: LA unica puerta de los valores de negocio (ADR-0002), con categoria por
  parametro y huso en las horas (ADR-0004, ADR-0012). Desde la sesion 1 (2026-09-09) tiene 52
  parametros: 46 con valor y 6 UNKNOWN **a proposito**, cada uno de estos con un registro `REJECT`
  que explica por que no existe ese numero. Un valor de `estrategia` cita SIEMPRE al trader
  (feedback o evidence); uno de entorno (instrumento, broker, prop_firm, ejecucion) cita un ADR.
- `ambiguedades.yaml` (F10, ADR-0011): A-1..A-17 con pregunta, evidencia, parametros y estado.
  A-1..A-12 quedaron RESUELTAS en la sesion 1; A-13..A-17 siguen abiertas. Es la fuente de la
  tabla de PROJECT_STATE y del cuestionario del kit, y el feedback la cita.
- `strategy_spec.yaml` (F11, ADR-0013): las reglas de la operativa. **No contienen numeros**:
  nombran parametros del registro, y un test lo comprueba. Cada regla lleva el `literal` del
  trader que la sostiene, verificado contra el registro o el item que cita.
- `glossary.yaml` (F11): los terminos del trader, definidos una vez. Cada definicion lleva su
  `literal` y se verifica igual que una regla: aqui se dice QUE es cada cosa, no que se hace con
  ella -eso son reglas- ni con que numero -eso es el registro-.
- `spec_manifest.yaml` (F11, ADR-0013): `spec_version` (semver) y hash canonico sobre los TRES
  ficheros anteriores. Lo genera `botsito spec manifest --escribir`; no se edita a mano. Si el
  hash cambia y la version no, `knowledge validate` falla.

Cada cambio de valor cita evidence-id o feedback-id, y el commit lleva su trailer `Fuente:`.

Comandos: `botsito feedback apply --sesion <s> [--check]` · `botsito spec status` ·
`botsito spec manifest [--escribir]`.
