# Abrir, editar y cerrar una ambiguedad

Lo que hace falta SOLO cuando una tarea toca `knowledge/spec/ambiguedades.yaml`. Mudado TAL CUAL
desde `CLAUDE.md` el 2026-10-01, en `trabajo/dieta-y-skills`; alli queda una linea que apunta aqui.

> **CORRECCION (2026-10-01, `trabajo/dieta-y-skills`).** Desde hoy la tabla «Known Ambiguities» de
> `PROJECT_STATE.md` lleva solo las ABIERTAS, con su titulo, clase, bloqueante y «resuelve en», y
> `tests/unit/test_kit.py` (`test_project_state_refleja_las_ambiguedades_abiertas`) exige que sean
> exactamente las `ABIERTA` del YAML. ABRIR una sigue tocando la tabla (se anade su fila); CERRARLA
> la toca QUITANDO la fila, no cambiando su texto. Lo que dicen los dos apartados de abajo sobre «la
> tabla» se lee asi. Las filas de las cerradas hasta hoy estan en docs/state/HISTORIA.md.

## Abrir una ambiguedad toca dos sitios; cerrarla, cuatro

**Abrirla:** `knowledge/spec/ambiguedades.yaml` y la tabla "Known Ambiguities" de `PROJECT_STATE.md`,
donde un test exige que ids y titulos coincidan.

**Y TOCAR EL TEXTO DE UNA AMBIGUEDAD, AUNQUE NO SE ABRA NI SE CIERRE NINGUNA, OBLIGA A
`botsito spec docs --escribir`** (medido el 2026-09-21, rama F14a: anadir una nota medida al campo
`pregunta` de A-18 dejo `make check` en rojo con
`test_lo_commiteado_es_lo_que_sale_de_la_fuente`). `docs/spec/ambiguedades.md` es GENERADO y va
commiteado, asi que cualquier cambio en el YAML -no solo el `estado`- tiene que viajar con su
documento en el MISMO commit. Vale igual para `parametros.yaml`, `strategy_spec.yaml` y
`glossary.yaml`, que generan los otros tres de `docs/spec/`.

## Cerrar una ambiguedad toca cuatro sitios, y solo dos los vigila una guardia

El registro de parametros (via `feedback apply`), `knowledge/spec/ambiguedades.yaml`, la regla de la
spec que la citaba -que probablemente citaba la evidencia DEBIL que abrio la duda- y la tabla "Known
Ambiguities" de `PROJECT_STATE.md`. Mas el test de `tests/unit/test_kit.py` que congela cuales estan
RESUELTAS. Hay DOS formas de cerrarla (ADR-0022): `RESUELTA` con un registro del trader que apunte A LA
AMBIGUEDAD -no al parametro-, o `DECIDIDA` por el consultor con el ADR que la nombre.
