---
status: ACTIVE
date: 2026-09-25
phase: post-F14 (rama `trabajo/sesion-02`)
---

# 0047 · La unidad de comparación es la operación también en el holdout

## Decision

1. **Se adopta la opción (a) de C-08** (`docs/validation/SESION-02-INVENTARIO.md` §4.3, D-03).
   Cuando se rellene `docs/validation/PREREGISTRO.md`, la unidad con la que se compare al bot con
   el trader en el holdout será **la misma que ADR-0043 fija para el desarrollo**: «**Unidad:** la
   operación, dentro de su día y su sesión». Con ella se hereda el emparejamiento uno a uno de
   ADR-0043 como punto de partida; las tolerancias y el umbral del holdout se fijan en el
   PREREGISTRO, no aquí.
2. **El PREREGISTRO NO se toca ahora.** Sigue vacío y con su blob declarado; esta decisión dice qué
   unidad llevará cuando se rellene, no lo rellena.
3. **La gramática del kit queda como deuda.** ADR-0011 §6 y §7 y `kappa.py` usan la unidad
   `(caso, sesión)`, con una decisión por sesión, y la gramática de etiquetado rechaza dos entradas
   en la misma sesión (`parsear_etiqueta(...)` → «la sesion 07-11 aparece dos veces», reproducido en
   la auditoría del 2026-09-13, hallazgo [47]). No se cambia ahora: **no rompe nada, porque hay 0
   registros `LABEL_CASE`** en `knowledge/feedback/`. Se adapta antes del primer etiquetado por
   operación, o antes de medir un kappa entre sesiones.

## Problema que resuelve

El proyecto manejaba tres unidades sin que ninguna decisión las atara (auditoría del 2026-09-13,
hallazgo [47], `d7-metodo-07`):
- ADR-0011 y `kappa.py` fijan una decisión `{compra, venta, no_trade}` por `(caso, sesión H4)`;
- `PREREGISTRO.md` pide definir «que cuenta como "misma decision" entre el bot y el trader
  (direccion, ventana de tiempo, nivel de entrada, stop y objetivo con que tolerancia)», que es la
  operación, sin nombrar la unidad;
- ADR-0043 (2026-09-24) fijó la operación, pero solo para el desarrollo.

La spec permite varias operaciones por sesión (`cartuchos_max` por zona de liquidez), y **la
auditoría midió que medir por sesión deja sin comparar el segundo y el tercer cartucho, «donde se
concentran las pérdidas»**. Un bot con una gestión de reentradas distinta de la del trader podría
aprobar el holdout sin que la medida lo viera.

## Alternativas consideradas

- **(a)** La operación también en el holdout, y la gramática del kit como deuda.
- **(b)** Dos unidades: `(caso, sesión)` para el acuerdo entre etiquetadores y la operación para el
  bot frente al trader.
- **(c)** Medir el holdout por sesión, que es lo que hoy representa el kit.

## Por que elegimos esta opcion

- **Es la unidad que ya mide el desarrollo** (ADR-0043). Medir el holdout con otra haría que la
  cifra del holdout no fuera comparable con la del desarrollo.
- **Ve las reentradas**, que es donde la auditoría encontró el riesgo.
- **No cuesta nada hoy**: el PREREGISTRO está vacío y no hay ningún `LABEL_CASE` que migrar.

## Por que descartamos las demas

- **(b)** deja dos cifras que no se pueden cruzar y aplaza la misma adaptación del kit sin
  evitarla.
- **(c)** es justo la medida que no ve el segundo ni el tercer cartucho.

## Impacto

- Ninguno en `src/`, en el kit ni en el PREREGISTRO: solo documentación.
- **Deuda:** la gramática de `LABEL_CASE` y `kappa.py` siguen en `(caso, sesión)`. Hay que
  adaptarlas antes del primer etiquetado por operación.
- Quien rellene el PREREGISTRO tiene que escribir la unidad de ADR-0043 y citar este ADR.

## Fecha / fase

2026-09-25 · post-F14, rama `trabajo/sesion-02`. Decisión del consultor sobre C-08.

## Estado

ACTIVE
