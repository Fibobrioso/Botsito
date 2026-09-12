# knowledge/spec/ — StrategySpec (F11) y registro de parametros (F02).

- `parametros.yaml`: LA unica puerta de los valores de negocio (ADR-0002), con categoria por
  ADR-0004 y lectura estricta por tipo. **El recuento no se copia aqui**: lo dan
  `botsito spec status` y `docs/spec/parametros.md`, que se genera desde este fichero (F13).
  Esta linea llevaba los numeros a mano y se quedo vieja dos veces.
- `ambiguedades.yaml` (F10, ADR-0011): las preguntas abiertas del modelo, con evidencia,
  parametros y estado. **El recuento no se copia aqui** -esta linea llego a llevar un rango de ids
  que se quedo cuatro ambiguedades por detras-: lo dan `botsito spec status` y
  `docs/spec/ambiguedades.md`, que se genera. Hay DOS formas de cerrar una, y el commit que la
  cierra cita su fuente: **RESUELTA**, solo con un registro de feedback del trader
  (`RESOLVE_UNKNOWN`), y **DECIDIDA**, cuando lo que decide no es el trader sino el consultor
  -alcance, metodo o herramienta-, con el ADR que la nombra (ADR-0022). `ABIERTA` es la unica que
  se sigue preguntando: entra en el cuestionario de la sesion siguiente.
- `strategy_spec.yaml` (F11, ADR-0013): las reglas de la operativa. **No contienen numeros**:
  nombran parametros del registro, y un test lo comprueba. Cada regla lleva el `literal` tal cual
  del registro o el item que cita, verificado contra el. Normalmente es del trader; cuando lo
  refiere el consultor -lo dice el `registrado_por` del registro- la regla declara ademas
  `decision`. Desde F12, cada regla vigente lleva ademas `forma`: la version ejecutable, escrita
  con el vocabulario de `predicados`, `acciones`, `efectos`, `hechos`, `acumuladores` y `tokens`
  (ADR-0019). Que no contengan numeros no es una promesa: `spec check` exige que cada argumento de
  una forma ejecutable sea el NOMBRE de un parametro, de un token declarado o de una ligadura.
- `glossary.yaml` (F11): los terminos del trader, definidos una vez. Cada definicion lleva su
  `literal` y se verifica igual que una regla: aqui se dice QUE es cada cosa, no que se hace con
  ella -eso son reglas- ni con que numero -eso es el registro-.
- `spec_manifest.yaml` (F11, ADR-0013): `spec_version` (semver) y hash canonico sobre los TRES
  ficheros anteriores. Lo genera `botsito spec manifest --escribir`; no se edita a mano. Si el
  hash cambia y la version no, `knowledge validate` falla.

Cada cambio de valor cita evidence-id o feedback-id, y el commit lleva su trailer `Fuente:`.

Comandos: `botsito feedback apply --sesion <s> [--check]` · `botsito spec status` ·
`botsito spec check` · `botsito spec docs [--escribir]` · `botsito spec manifest [--escribir]`.
