# Inventario para la fidelidad: las decisiones del consultor

Rama `trabajo/inventario-fidelidad`, 2026-09-23. Sin merge, sin tag y sin push.

Registra las respuestas del consultor a las tres preguntas de `INVENTARIO-FIDELIDAD.md` (§5), y
una corrección suya. Ese informe ya estaba commiteado y no se toca: estas decisiones van aparte.

## D1 · La verdad de un caso es el xlsx

- **La fuente primaria de lo que hizo el trader es su libro de backtest.**
- **«No operó» solo se afirma en los días que el libro cubre de verdad.** Son los tramos que
  declara `cobertura_material`. Un día fuera de esos tramos no es un `no_trade`: es un día sin
  material.
- **Las etiquetas del kit ciego (`LABEL_CASE`) siguen en su propio ADR.** Esta decisión no las
  toca.

Es la decisión D1 de `docs/plan/features/F14-case-library.md`, que el inventario marcaba como el
punto 1 de lo mínimo.

## Ampliar los casos `dev`

Agosto, abril y los 4 días `fidelidad-dev` de septiembre se ingieren **por el camino de mayo**,
como **SIGUIENTE rama**. Hoy solo hay 6 casos `dev`, todos de mayo (`INVENTARIO-FIDELIDAD.md` §2).

## El instante que se compara

- **Se compara el instante que registra el xlsx.**
- **La colocación de la orden límite no puntúa** hasta que haya una fuente que la registre.

## Corrección del consultor

La estimación de calendario que manejaba el consultor suponía que el motor ya existía en parte.
**No existe**: F18 a F24 y F26 no se han empezado, y ninguna regla de la spec está implementada
(`INVENTARIO-FIDELIDAD.md` §0 y §1). La corrige él.

## Estado

WAITING_FOR_USER_VALIDATION
