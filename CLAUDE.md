# Reglas de la casa

Lo que toda sesion tiene que saber antes de tocar nada. Cada regla de aqui esta comprobada contra el
repositorio el 2026-09-17 (rama `trabajo/reglas-de-la-casa`); si alguna deja de ser cierta, se corrige
aqui en el mismo commit que la rompe.

## Por donde se empieza

1. `PROJECT_STATE.md` (memoria operativa: manda sobre cualquier otro documento).
2. `docs/plan/features/<Current Feature>.md`, si hay funcionalidad abierta.
3. `docs/HANDOFF.md` (contexto humano de la ultima sesion; si contradice a `PROJECT_STATE.md`, manda
   `PROJECT_STATE.md`).
4. `make check` con la salida a un fichero.

Si `Current Feature` esta en WAITING_FOR_USER_VALIDATION: no se avanza, se pregunta.

## main no se toca

Se trabaja en una rama (`feature/F##-nombre` o `trabajo/<nombre>`). **La sesion no hace merge, ni tag,
ni push: el ritual de cierre lo ejecuta el usuario** (`docs/runbooks/RITUAL.md`). El hook `pre-commit`
rechaza un commit directo en `main` salvo con `BOTSITO_ALLOW_MAIN=1`, que solo usa el ritual.

## Regimenes de cambio

- `knowledge/evidence/` → INMUTABLE tras commit (hook). Correccion = item nuevo que supersede.
- `knowledge/feedback/` → SOLO ANADIR. Nunca se edita un registro.
- `knowledge/spec/`, `knowledge/cases/` → versionados; cada cambio de valor cita su fuente.
- `data/manifests/`, `knowledge/corpus/transcripciones/`, `knowledge/corpus/fotogramas/` → INMUTABLES
  tras commit.
- `src/botsito/domain/` → sin IO, sin reloj, sin MetaTrader (import-linter).

## El trailer `Fuente:`

Todo commit que toque `knowledge/spec/` o `knowledge/cases/` lleva un trailer `Fuente:` con ids que
EXISTAN: `ev-*`, `fb-*` o `ADR-NNNN` (`comun/historial.py`, `DIRECTORIOS_CON_FUENTE`). Un sha de commit
no es un id valido. Va en el CUERPO del mensaje: en el asunto no cuenta.

## Al anadir un sitio con `cita` propia, las TRES guardias

Un sitio nuevo que lleve `cita` obliga a ampliar, EN EL MISMO COMMIT, las tres de
`src/botsito/spec/modelo.py`: `comprobar_contra`, `comprobar_literales` y `comprobar_citas_revocadas`.
Ha nacido corta cuatro veces.

## Las cifras no van en la forma ejecutable

Si un valor puede cambiar, es un parametro del registro (ADR-0002: una sola puerta, tipos no
intercambiables, lectura estricta). La forma nombra el parametro; no lleva el numero dentro.

## Holdout

La puerta `botsito.cases.holdout` es el UNICO sitio por el que se abre, y exige `PREREGISTRO.md`
relleno y autorizacion commiteada por particion, atada por `preregistro_blob` (ADR-0033). **Leer velas
no es abrir:** `kit build` y `kit check` se pueden ejecutar con `data/` presente y declaran en su
salida, por RECUENTO y no por fechas, los dias reservados cuyas velas leen. Toda exposicion se declara
en `docs/validation/HOLDOUT-EXPOSICIONES.md`.

## Cerrar una ambiguedad toca cuatro sitios, y solo dos los vigila una guardia

El registro de parametros (via `feedback apply`), `knowledge/spec/ambiguedades.yaml`, la regla de la
spec que la citaba -que probablemente citaba la evidencia DEBIL que abrio la duda- y la tabla "Known
Ambiguities" de `PROJECT_STATE.md`. Mas el test de `tests/unit/test_kit.py` que congela cuales estan
RESUELTAS. Hay DOS formas de cerrarla (ADR-0022): `RESUELTA` con un registro del trader que apunte A LA
AMBIGUEDAD -no al parametro-, o `DECIDIDA` por el consultor con el ADR que la nombre.

## Trampas medidas

- **Los regex se escriben con Write, nunca dentro de un heredoc con delimitador sin comillas.** En Git
  Bash, `cat > f <<EOF` convierte `\b` en BACKSPACE (0x08) antes de que Python lo vea: el patron queda
  `'\x08(hola)\x08'` y casa con otra cosa. Con `<<'EOF'` se conserva, pero lo seguro es Write. Lo mismo
  vale para Python con comillas y sangrado complicado: script a la carpeta de trabajo y ejecutarlo.
- **El `## Estado` de un ADR se lee con `split()[0]`** (`tests/unit/test_adr.py`): escribir `ACTIVE.`
  con punto hace fallar el test.
- **`make check` con la salida a un FICHERO, nunca a `/dev/null`:** `lint-imports` falla al escribir
  ahi y `make` sale con 2 aunque todo este verde. Medido hoy: a `/dev/null` sale 1; al fichero, 0 y
  "Contracts: 4 kept, 0 broken".

## Donde esta el texto de las transcripciones

Es lo que mas tiempo hace perder. `knowledge/corpus/transcripciones/` solo tiene los MANIFIESTOS YAML
(`tr-<video>-<modelo>-<hash>.yaml`), no el texto.

- **El texto bueno:** `data/transcripciones/<video>/<modelo>/` -por ejemplo
  `data/transcripciones/v1/large-v3-int8-float16/`- con `cruda.jsonl`, `cruda.txt`, `corregida.jsonl`,
  `correcciones.jsonl`, `fragmentos/` y `parciales/`. La CRUDA es de la que se copia una cita literal.
- **Version legible para buscar:** `corpus/Estrategia del trader/_procesado/transcripciones/*.txt`
  (7 ficheros). Es el ASR pequeno heredado, con deriva de hasta un minuto (ADR-0007): sirve para
  LOCALIZAR, no para citar literal.
- **Los segmentos CRUDOS estan copiados dentro de `knowledge/_proposals/*.yaml`**, en
  `contexto.segmentos` (con `n`, `t0_ms`, `t1_ms`, `texto`, `senales`): suele ser la via mas rapida
  para ver el tramo que rodea a una evidencia.

## Como se trabaja

- Antes de escribir codigo, revision de diseno; se contesta MIDIENDO, no razonando.
- Un informe por rama en `docs/validation/`, con su estado al final.
- Nada afirma mas de lo que su cita sostiene.
