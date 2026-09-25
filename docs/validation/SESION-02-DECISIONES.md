# Sesión 02: las decisiones del consultor sobre el inventario, aplicadas

Rama `trabajo/sesion-02`, 2026-09-25. Sin merge, sin tag y sin push. Aplica las decisiones del
consultor sobre `SESION-02-INVENTARIO.md` y `SESION-02-BUSQUEDA-CLASIFICACION.md`, una pieza por
commit.

## 1. K-04: a qué regla afecta A-21

**El origen.** A-21 nace en ADR-0019 (commit `d264912`, 2026-09-10) preguntando qué es un breaker,
y se reformula el mismo día. ADR-0019: «Lo que sí queda abierto, y por eso A-21 se reformula en vez
de borrarse: **qué es una zona de control "limpia, sin ruido"**. Es lo único de la geometría de
entrada que sigue siendo cualitativo.» La nota de `PROJECT_STATE.md`, entrada (10) del 2026-09-10,
dice lo mismo: «A-21 se REFORMULA a lo unico que sigue siendo cualitativo: que es una zona de
control "limpia, sin ruido"», con RN-008 como la regla que dejaba de estar pendiente.

**Los pasajes que la sostienen** son los tres de su `evidencia`, y los tres hablan del esquema de
entrada en M1:
- `ev-v1-001435-f0586d02` (v1 0:14:35): «cuando se desarrolle esta zona de control que no haga
  mucho ruido, o sea, sea una zona limpia», y a continuación el breaker activa la orden límite;
- `ev-v4-000243-5f8875ce`: los dos esquemas de entrada;
- `ev-v3-004201-bfeb3734`: el primero no espera retroceso.

**La spec.** Ninguna regla cita A-21. RN-004 (`strategy_spec.yaml`, la liquidez de M15) cita A-24,
DECIDIDA por ADR-0045, y A-35, bloqueante. La geometría de la entrada es RN-008 («sin ninguno de
los esquemas de entrada no hay entrada»), cuyo segundo esquema es el que deja una zona de control.

**De dónde salía el error.** La frase «RN-004 sigue BLOQUEADA por A-21 y A-35» entra en
`PROJECT_STATE.md` en `0901d2c` (2026-09-24, `docs(state)` del cierre de `trabajo/a35-pivote-formado`)
y en el cuerpo de `A35-FOTOGRAMAS-RESULTADO.md`, sin fuente en ninguno de los dos.

**Qué se corrige.** El lado equivocado es `PROJECT_STATE.md`: sus dos apariciones (la funcionalidad
actual y Next Action 22) dicen ahora que RN-004 está bloqueada solo por A-35 y que A-21 toca RN-008.
`A35-FOTOGRAMAS-RESULTADO.md` está cerrado en `main`, así que lleva un recuadro de corrección junto
al pasaje y su cuerpo no cambia. La spec no se toca: no dice nada falso.

**Resultado: A-21 afecta a RN-008, no a RN-004. RN-004 queda bloqueada solo por A-35.** A-21 sigue
siendo bloqueante, ahora de la regla que le corresponde. Que ninguna regla la cite es un hueco de
enlace, no un error: no se abre aquí.

## Estado

EN CURSO. Cada sección entra con su commit.
