# F11 · strategy-spec-schema

**Rama:** `feature/F11-strategy-spec-schema` · **Fase:** 2 (retroalimentación del experto) ·
**Depende de:** F02 (registro), F07 (evidencia), F09 (feedback), F10 + sesión 1 (`stable/F10-sesion-01`)

## Objetivo

Convertir lo que el trader dijo en la sesión 1 en una **especificación ejecutable y citable**:

1. `feedback apply` — la puerta que faltaba desde F09: los `RESOLVE_UNKNOWN` de la sesión pasan al
   registro de parámetros, cada valor con su `fuente: {tipo: feedback, id: fb-…}`. Ningún valor
   entra a mano.
2. `knowledge/spec/strategy_spec.yaml` — las reglas de la operativa, que referencian parámetros
   **por nombre, nunca por valor**, y citan la evidencia o el feedback que las sostiene.
3. `knowledge/spec/glossary.yaml` — los términos del trader (breaker, zona de control, estructura,
   equal, cartucho, caja) definidos una vez y usados por la spec.
4. `knowledge/spec/spec_manifest.yaml` — `spec_version` semver y hash canónico sobre los tres
   ficheros, para que un backtest, un informe y un `Params.mqh` puedan decir contra qué spec
   corrieron.

Sin motor y sin backtest: F11 describe, no ejecuta. El motor es F18–F23.

## Hechos de partida

- **Registro** (`knowledge/spec/parametros.yaml`, ADR-0002/0004): 33 parámetros — 32 de
  `estrategia`, 1 de `instrumento`, 2 de `ejecucion`; 2 CONFIRMED (`huso_operativa` por ADR-0005) y
  **31 UNKNOWN**. `Registro.obtener` se niega a leer un UNKNOWN, así que hoy nada puede usarlos.
- **Sesión 1** (2026-09-09, `stable/F10-sesion-01`): 72 registros de feedback, todos con medio,
  minuto y cita. 26 parámetros tienen ya respuesta del trader. A-1..A-12 RESUELTAS; A-13..A-17
  abiertas con sus 12 items de evidencia de v6.
- **Riesgos que el plan asigna a F11** (MASTER_PLAN H.2): `spec_manifest` con versión y hash
  (fila 215); restricciones de ejecución dentro de la spec, con la abstención como respuesta al
  rechazo por `stops_level` (216); tipos que faltan — `enum`, `booleano`, `puntos`, `minutos`,
  `lotes` (218); modelo de llenado como parámetro de `ejecucion` (219); `dst_servidor` y
  `offset_base_servidor` en `broker`, por ADR (209); poblar instrumento/broker/prop_firm citando
  ADR (211).
- **Guardias vigentes**: `test_no_business_literals` prohíbe en `src/botsito/` los literales de
  negocio; todo commit bajo `knowledge/spec` necesita `Fuente:`; el registro no admite claves
  extra ni valores fuera de tipo.

## Lo que la sesión deja resuelto y lo que aún no encaja en el registro

Esto es el trabajo real de F11, y conviene mirarlo antes de escribir una línea. Seis valores del
trader **no entran tal cual** en el esquema de F02:

1. **`anclaje_h4` y las horas: el huso no tiene nombre IANA.** El trader trabaja con el gráfico en
   **UTC+2** y dice que **no se ajusta** en el cambio de horario (A-14). El registro exige, para
   tipo `hora`, un huso IANA (`Europe/Madrid`, `UTC`). Un desplazamiento fijo de +2 no es
   `Europe/Madrid` — coinciden en verano y divergen en invierno. Hay que decidir si se admite
   `Etc/GMT-2` (IANA válido, signo invertido, fácil de leer mal), si se añade un tipo `hora` con
   `offset_fijo`, o si se modela el reloj del trader como un parámetro aparte del que cuelgan
   todas las horas. **Afecta a `anclaje_h4`, `ventana_inicio`, `ventana_fin` y al día de riesgo.**
2. **`cartuchos_max` cuenta pérdidas, no intentos.** El trader: "se opera hasta el tercer trade" y
   "un intento no es considerado un break even […] una entrada invalidada tampoco […] reentrada
   después de equal, tampoco". Es decir: el contador sube **solo con una pérdida**. El nombre del
   parámetro dice otra cosa y el bot lo leería como "3 entradas". Renombrar a `perdidas_max_dia`
   (o añadir el criterio como parámetro propio) es más honesto que documentarlo en una frase.
3. **`spread_maximo` = "no existe un límite"**, y el tipo declarado es `decimal`. Un decimal no
   expresa "sin tope". O el parámetro pasa a opcional con semántica explícita de ausencia, o entra
   un `filtro_spread: booleano` con el máximo solo cuando está activo. Lo mismo con
   `objetivo_extension` ("no se extiende") y `stop_reduccion_*` ("no aplica").
4. **`riesgo_por_operacion` no es lo que arriesga.** Es 0,5 % del saldo, pero el lote se dimensiona
   sobre la caja completa y el stop salta en 0,8 → la pérdida real es **0,4 %**. Si la spec guarda
   solo 0,5 %, cualquiera que la lea sacará la cifra equivocada. Hace falta que la relación entre
   `riesgo_por_operacion`, `lotaje_base` y `stop_fraccion_caja` sea explícita en la spec, no un
   cálculo que cada implementación repita a su manera.
5. **`instrumento` es una lista con prioridad**, no un valor: EURUSD primero; el NASDAQ es el que
   mejor calca; después FX sin gaps y oro. El tipo `texto` lo aplana. La primera versión opera
   EURUSD: ¿se guarda solo eso y el resto queda en la evidencia, o el registro admite una lista
   ordenada?
6. **Los interruptores de ambigüedad.** A-13..A-17 siguen abiertas y el bot tiene que poder correr
   igualmente. Para eso existe `DEFAULT_AMBIGUOUS` con `ambiguedad_id`: `break_even_condicion` vale
   `tocar` porque el trader lo dijo, pero A-13 pregunta si debería ser cuerpo. **Decisión de
   diseño**: un valor respondido por el trader y a la vez bajo una ambigüedad abierta, ¿es
   CONFIRMED (lo dijo) o DEFAULT_AMBIGUOUS (está en revisión)? La respuesta cambia qué mide F26.

## Alcance

**Dentro:**
- `feedback apply`: lee los registros de una sesión y propone el cambio en el registro; escribe
  solo tras `--check` en verde; rechaza aplicar un feedback superseded o uno cuyo objetivo no
  exista; deja el registro con `fuente` apuntando al `fb-…` exacto.
- Tipos nuevos del registro: `enum` (con `opciones`), `booleano`, `puntos`, `minutos`, `lotes`.
- `strategy_spec.yaml`: reglas por nombre de parámetro, con su cita; validación estricta de carga.
- `glossary.yaml` y `spec_manifest.yaml` (semver + hash canónico).
- Parámetros de entorno que el plan pide con ADR: `dst_servidor`, `offset_base_servidor`,
  modelo de llenado y latencia, restricciones de ejecución.
- ADR-0012 con las decisiones de forma (huso del trader, interruptores, ausencia de valor).

**Fuera:** motor, backtest, validación semántica (F12), documentos generados (F13), biblioteca de
casos (F14), export MQL5 (F28).

## Criterios de aceptación

1. `botsito feedback apply --sesion 2026-09-09-sesion-01 --check` lista los 26 cambios sin escribir
   nada; sin `--check`, los escribe y cada parámetro queda con `fuente: {tipo: feedback, id: fb-…}`.
2. Ningún valor de negocio aparece en `src/`; `test_no_business_literals` sigue en verde.
3. `strategy_spec.yaml` carga con esquema estricto y **no contiene ni un número de negocio**: solo
   nombres de parámetro. Un test lo comprueba.
4. `spec_manifest.yaml` da el mismo hash al regenerarlo y uno distinto si cambia cualquiera de los
   tres ficheros.
5. Cada regla de la spec cita al menos un `ev-…` o `fb-…` existente, y `knowledge validate` lo
   verifica.
6. Los parámetros bajo ambigüedad abierta llevan `ambiguedad_id` y el valor con el que corre el
   bot, de modo que se pueda listar "con qué está corriendo y qué está en revisión".

## Lo que hay que decidir antes de programar

Los seis puntos de arriba. Ninguno es técnico de verdad: los seis cambian lo que la spec **dice**,
y por tanto lo que el bot hará y lo que F26 medirá. Van a revisión de diseño antes de escribir
código, y las que sean del usuario se le preguntan.
