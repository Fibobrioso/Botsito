# knowledge/spec/ — StrategySpec (F11) y registro de parametros (F02).

- `parametros.yaml`: LA unica puerta de los valores de negocio (ADR-0002), con categoria por
  parametro y huso en las horas (ADR-0004, ADR-0012). Desde la sesion 1 (2026-09-09) tiene 59
  parametros: 50 confirmados, 2 con un default nuestro y 7 UNKNOWN **a proposito**, cada uno de estos con un registro `REJECT`
  que explica por que no existe ese numero. Un valor de `estrategia` cita SIEMPRE al trader
  (feedback o evidence); uno de entorno (instrumento, broker, prop_firm, ejecucion) cita un ADR.
- `ambiguedades.yaml` (F10, ADR-0011): las preguntas abiertas del modelo, con evidencia,
  parametros y estado. El recuento vivo lo da `botsito spec status`: no se pega aqui, que es
  como esta linea se quedo diciendo "A-1..A-17" cuando ya iban por A-21. Se cierran SOLO con
  un registro de feedback del trader (RESOLVE_UNKNOWN) y el commit que las cierra lo cita.
- `strategy_spec.yaml` (F11, ADR-0013): las reglas de la operativa. **No contienen numeros**:
  nombran parametros del registro, y un test lo comprueba. Cada regla lleva el `literal` tal cual
  del registro o el item que cita, verificado contra el. Normalmente es del trader; cuando lo
  refiere el consultor -lo dice el `registrado_por` del registro- la regla declara ademas
  `decision`. Desde F12, cada regla vigente lleva ademas `forma`: la version ejecutable, escrita
  con el vocabulario de `predicados`, `acciones`, `hechos` y `acumuladores` (ADR-0019).
- `glossary.yaml` (F11): los terminos del trader, definidos una vez. Cada definicion lleva su
  `literal` y se verifica igual que una regla: aqui se dice QUE es cada cosa, no que se hace con
  ella -eso son reglas- ni con que numero -eso es el registro-.
- `spec_manifest.yaml` (F11, ADR-0013): `spec_version` (semver) y hash canonico sobre los TRES
  ficheros anteriores. Lo genera `botsito spec manifest --escribir`; no se edita a mano. Si el
  hash cambia y la version no, `knowledge validate` falla.

Cada cambio de valor cita evidence-id o feedback-id, y el commit lleva su trailer `Fuente:`.

Comandos: `botsito feedback apply --sesion <s> [--check]` · `botsito spec status` ·
`botsito spec manifest [--escribir]`.
