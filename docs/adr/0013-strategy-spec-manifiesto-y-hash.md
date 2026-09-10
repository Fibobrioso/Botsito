---
status: ACTIVE
date: 2026-09-09
phase: F11
---

# 0013 · StrategySpec: reglas que nombran parametros y nunca los contienen, y un hash que cubre lo que el bot hace

## Decision

1. **Una regla nombra parametros; nunca los contiene.** Los campos ejecutables (`cuando`,
   `entonces`, `parametros`) rechazan cualquier cifra que empiece palabra. `M15`, `H4` y
   `liquidez_m15_criterio_toma` pasan: son nombres. El campo `literal` **si** admite cifras, porque
   son las palabras del trader.
2. **Cada regla cita** un item de evidencia o un registro de feedback existente, y `knowledge
   validate` lo comprueba.
3. **Una regla descartada conserva su cita y su motivo** (`estado: DESCARTADA`).
4. **Una regla vigente no puede nombrar un parametro UNKNOWN**: se detecta en `knowledge validate`.
5. **El hash del `spec_manifest.yaml` cubre los TRES ficheros**: `parametros.yaml`,
   `strategy_spec.yaml` y `glossary.yaml`. Por parametro entran nombre, categoria, tipo, unidad,
   **estado**, valor, **fuente**, `ambiguedad_id`, `opciones` y limites.
6. **Se hashea la estructura re-serializada canonicamente, no los bytes.**
7. **Semver**: mayor si una regla cambia de sentido o desaparece; menor si se anade una regla o un
   parametro; parche si solo cambia un valor o una redaccion.

## Problema que resuelve

Con los valores ya en el registro faltaba el otro lado -las reglas- y faltaba poder decir, desde un
backtest, un informe o un `Params.mqh`, **contra que spec** se corrio. Sin eso, un resultado de
fidelidad no significa nada: no se sabe que estrategia se midio.

## Alternativas consideradas

- **A. Reglas con los valores dentro**, legibles de un vistazo sin saltar al registro.
- **B. Hash solo sobre las reglas y el glosario**, dejando fuera el registro.
- **C. Hash sobre los bytes de los tres ficheros.**
- **D. Sin manifiesto**: usar el SHA del commit de git como version de la spec.

## Por que elegimos esta opcion

Porque **una sola puerta por valor** es lo que impide que la spec y el motor dejen de decir lo
mismo. Cambiar el stop se hace en el registro, y la spec no se toca.

Y porque el hash tiene que cubrir **lo que el bot hace**, no una parte. Que entren el estado y la
fuente ademas del valor responde a una pregunta que F26 se hara: ¿este resultado se midio con un
valor que dijo el trader, o con un default nuestro? Si solo entrara el valor, las dos situaciones
darian el mismo hash.

Hashear la estructura y no los bytes mantiene los comentarios como lo que son: documentacion.

## Por que descartamos las demas

- **A**: dos puertas para el mismo numero. Es la forma mas rapida de que un backtest corra con 0,8 y
  la spec siga diciendo 0,75.
- **B**: el fallo exacto que MASTER_PLAN H.2 (fila 215) pide impedir: mover el stop de 0,8 a 0,75 no
  cambiaria el hash y el pre-vuelo de la demo daria verde con una estrategia distinta de la
  validada. Hay un test que lo comprueba.
- **C**: convertiria la cabecera de `parametros.yaml` -que es documentacion del esquema- en contrato
  criptografico, y reordenar un comentario cambiaria la version de la spec sin cambiar la spec.
- **D**: el SHA de git cambia con cualquier cosa del repositorio -un README, un test- y no cambia
  cuando la spec se edita sin commitear. No dice nada sobre la estrategia.

## Impacto

- `botsito spec manifest` comprueba el hash y `--escribir` lo regenera; `knowledge validate` falla si
  esta desfasado. Ya salto una vez, al alinear `huso_operativa`, y obligo a subir la version.
- `botsito spec status` responde "con que corre el bot y que sigue en revision".
- De la sesion 1 salen 25 reglas: 22 vigentes y 3 descartadas con su cita.
- F12, F13, F14 y F28 tienen ya un esquema estricto y un identificador de version sobre el que
  apoyarse.

## Fecha / fase

2026-09-09, F11.

## Estado

ACTIVE
