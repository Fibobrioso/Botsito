# Abrir, editar y cerrar una ambiguedad

Lo que hace falta SOLO cuando una tarea toca `knowledge/spec/ambiguedades.yaml`. Mudado TAL CUAL
desde `CLAUDE.md` el 2026-10-01, en `trabajo/dieta-y-skills`; alli queda una linea que apunta aqui.

> **CORRECCION (2026-10-01, `trabajo/dieta-y-skills`).** Desde hoy la tabla «Known Ambiguities» de
> `PROJECT_STATE.md` lleva solo las ABIERTAS, con su titulo, clase, bloqueante y «resuelve en», y
> `tests/unit/test_kit.py` (`test_project_state_refleja_las_ambiguedades_abiertas`) exige que sean
> exactamente las `ABIERTA` del YAML. ABRIR una sigue tocando la tabla (se anade su fila); CERRARLA
> la toca QUITANDO la fila, no cambiando su texto. Lo que dicen los dos apartados de abajo sobre «la
> tabla» se lee asi. Las filas de las cerradas hasta hoy estan en docs/state/HISTORIA.md.

## Abrir una ambiguedad toca dos sitios; cerrarla, cinco

**Abrirla:** `knowledge/spec/ambiguedades.yaml` y la tabla "Known Ambiguities" de `PROJECT_STATE.md`,
donde un test exige que ids y titulos coincidan.

**Y TOCAR EL TEXTO DE UNA AMBIGUEDAD, AUNQUE NO SE ABRA NI SE CIERRE NINGUNA, OBLIGA A
`botsito spec docs --escribir`** (medido el 2026-09-21, rama F14a: anadir una nota medida al campo
`pregunta` de A-18 dejo `make check` en rojo con
`test_lo_commiteado_es_lo_que_sale_de_la_fuente`). `docs/spec/ambiguedades.md` es GENERADO y va
commiteado, asi que cualquier cambio en el YAML -no solo el `estado`- tiene que viajar con su
documento en el MISMO commit. Vale igual para `parametros.yaml`, `strategy_spec.yaml` y
`glossary.yaml`, que generan los otros tres de `docs/spec/`.

## Cerrar una ambiguedad toca cinco sitios, y solo tres los vigila una guardia

El registro de parametros (via `feedback apply`), `knowledge/spec/ambiguedades.yaml`, la regla de la
spec que la citaba -que probablemente citaba la evidencia DEBIL que abrio la duda-, la tabla "Known
Ambiguities" de `PROJECT_STATE.md` y **la hoja de preguntas, `scripts/hoja_preguntas.py`
(`ORDEN_SESION_02`), con su test, `tests/unit/test_hoja_preguntas.py`, que copia el orden**: la hoja
se niega a llevar al trader una ambiguedad que ya no esta ABIERTA ni DECIDIDA, y su test falla en
`make check`. Medido el 2026-10-02 en `trabajo/cerrar-a29-a36`: el primer `make check` tras cerrar
A-29 y A-36 salio en rojo por eso. REABRIR una toca los mismos cinco al reves, y la hoja vuelve a
llevarla; el registro que la reabre es un `REOPEN` (abajo, «Reabrir una ambiguedad»). Mas el test de `tests/unit/test_kit.py` que congela cuales estan
RESUELTAS. Hay DOS formas de cerrarla (ADR-0022): `RESUELTA` con un registro del trader que apunte A LA
AMBIGUEDAD -no al parametro-, o `DECIDIDA` por el consultor con el ADR que la nombre.

## Reabrir una ambiguedad: un registro `REOPEN`

Desde el 2026-10-03 (`trabajo/reabrir-y-fuente-documental`, decision 1 del consultor). Hasta
entonces se reabria con otro `RESOLVE_UNKNOWN` de valor «sin resolver» (A-36, `fb-…-a0b61bc9`), y
`feedback pending` lo contaba como una respuesta pendiente.

- **Solo sobre una ambiguedad**, y sin `valor_resultante` ni `valor_canonico`: reabrir no fija nada.
- **`supersede` obligatorio, al ULTIMO registro de la cadena** de esa ambiguedad, no al que la
  cerro: un registro solo se supersede una vez (`feedback/modelo.py`). En esa cadena, hacia atras,
  tiene que haber un `RESOLVE_UNKNOWN` sobre ella, y es lo primero que se encuentra: si antes
  aparece otro `REOPEN`, ya esta reabierta. En los dos casos no hay nada que reabrir y
  `knowledge validate` falla.
- **El YAML pasa a `ABIERTA`** en el mismo commit (con su `clase`), y la tabla de `PROJECT_STATE.md`
  recupera su fila: un `REOPEN` activo exige `ABIERTA`. Y una `RESUELTA` exige un `RESOLVE_UNKNOWN`
  ACTIVO: el que un `REOPEN` supersede ya no la cierra.
- **Una `DECIDIDA` no se reabre con feedback**: la cierra un ADR y solo la reabre otro ADR.
- **Volver a cerrarla** es un `RESOLVE_UNKNOWN` nuevo que supersede al `REOPEN`.
- `feedback pending`: un `REOPEN` activo esta reflejado si la ambiguedad esta `ABIERTA`.

Ejemplo: A-36, `fb-2026-09-29-sesion-03-f3caeb2d` (`reexpresion_consultor`, misma `fecha` que el
registro que reexpresa y `recibido_el` del dia de la decision).

## Una fuente documental en vez de evidencia (solo en `medicion`)

Desde el 2026-10-03 (decision 3 del consultor). Cuando la fuente de una ambiguedad es un documento
del repositorio (una regla de FTMO en `docs/validation/FTMO-REGLAS.md`, por ejemplo) y no lo que
dijo el trader, se cita en `fuentes_documentales` en vez de rellenar `evidencia` con el item del
corpus mas cercano:

```yaml
    evidencia: []
    fuentes_documentales:
      - documento: docs/validation/FTMO-REGLAS.md
        ancla: "2. Las reglas, con su fuente"
        literal: "an excessive number of more than 2,000 server requests per day"
```

- **Solo en `clase: medicion`.** En una `pregunta` se niega: su evidencia es lo que dijo el trader,
  y el cuestionario de la sesion busca en ella sus casos.
- **`evidencia` vacia solo si hay al menos una fuente documental.**
- **`documento`:** ruta relativa, con `/`, normalizada y DENTRO de `docs/`. Se niegan `..`, las rutas
  absolutas y los enlaces que salgan de `docs/`. Y tiene que estar COMMITEADO: primero se commitea
  el documento, despues la fuente que lo cita.
- **`ancla`:** el texto de un ENCABEZADO del documento, sin las almohadillas.
- **`fila`** (opcional, desde la tercera orden del consultor del 2026-10-03): el id de UNA fila de
  tabla de esa seccion, su primera celda (`R13` en `FTMO-REGLAS.md`). Entonces el literal tiene que
  estar DENTRO DE ESA FILA, no en cualquier parte de la seccion. Un id que no esta en ninguna fila,
  o que esta en mas de una, se niega. Si la fuente es una tabla, se ancla a su fila; sin `fila`
  queda lo que no es una fila (la respuesta del ticket de A-55, un recuadro).
- **`literal`:** tal cual, DENTRO de la seccion de ese encabezado (hasta el siguiente de su nivel).
  Se comparan sin las marcas de cita `>` y con los espacios y los saltos de linea de seguido.
- Lo comprueba `knowledge validate`, y `docs/spec/ambiguedades.md` la pinta debajo de la pregunta.
  Sin git (una copia del repositorio sin `.git`), «commiteado» no se comprueba y `knowledge
  validate` lo DICE con un `AVISO: ambiguedades: sin git, NO se comprobo...`.
