# Abril y agosto, casos `dev` por el reparto dev-visto

Rama `trabajo/casos-agosto-abril`, 2026-09-23. Es el punto 17 de Next Action. Sin merge, sin tag
y sin push. Ningún texto de esta rama lleva la fecha de un día reservado ni retirado.

## 0. El paso 0: por el camino de mayo, cero días

La ingesta (F14a, ADR-0037) solo pedía días de un reparto commiteado del kit. Medido antes de
tocar nada, sin leer una fila:

- **Abril y agosto** tenían su libro declarado en `libros.yaml`, pero ningún tramo en
  `cobertura_material` y ningún día en ningún reparto. Pedían **0** días, con 0 ocultos.
- **Los 4 `fidelidad-dev` de septiembre quedan FUERA.** Solo los cubre el libro de septiembre, cuyo
  tramo no lleva `material_sha256` y que no está en `libros.yaml`. No se abrió nada para
  averiguarlo.
- **Ninguna salida de la ingesta refleja el libro entero:** solo los días pedidos. Lo vigilan tres
  tests de `tests/contract/test_ingesta.py`. No hubo nada que arreglar antes.

## 1. ADR-0042 y el camino dev-visto (`a435cb1`)

Decisión del consultor: **el material ya visto entra por un reparto dev-visto, sin sorteo y sin
holdout.**

- **El reparto.** Vive en `knowledge/cases/visto/<AAAA-MM>/`, con todos sus días `dev`, sin
  semilla y con cupo de holdout 0.
- **Solo entra si se cumplen tres condiciones**, que se comprueban al construir, en
  `dias_ingeribles` y en `knowledge validate`:
  - el mes está en `vistos.yaml`;
  - su libro está en `libros.yaml` y su lectura completa está declarada en
    `HOLDOUT-EXPOSICIONES.md`;
  - su tramo en `cobertura_material` lleva el `material_sha256` de ese libro.
- **El mismo régimen de fichero que los otros repartos.** Se recompone desde la cobertura, sin
  `data/`, y va anclado por el blob. Lo construye y lo ancla `botsito casos visto --mes`.
- **La puerta lo recorre** (`repartos_commiteables`) y aplica «ocultos» (ADR-0041): un día oculto
  no se ingiere aunque esté aquí. Si un dev-visto es inválido, la ingesta falla cerrada.
- **No toca los repartos del kit ni de fidelidad** (ADR-0036).
- **Tests:** 5, en `tests/contract/test_visto.py`.

## 2. Los tramos (`764aab5`)

| mes | tramo | libro |
|---|---|---|
| abril | del 1 al 29 | `backtesting-analytics ABRIL 2026.xlsx`, `5e5d9b83…4c125b` |
| agosto | del 3 al 31 | `backtesting-analytics AGOSTO 2026.xlsx`, `33a01f1d…090f45` |

- **Qué se leyó.** Cada tramo es la fecha **mínima** y la **máxima** de la columna `dateStart`,
  con el formato y el huso de `libros.yaml`. El día sale igual en UTC y en Europe/Madrid. No se
  leyeron recuentos, ni precios, ni ninguna otra columna.
- **Quién lo hizo.** La lectura la ejecutó la sesión **por orden del consultor**, así que **el
  acto es suyo** (`CLAUDE.md`). Se hizo una sola vez, con un script fuera de `src/`, y se declaró
  el mismo día.
- **Es un LÍMITE INFERIOR de la cobertura real.** Un día del borde sin operaciones no se distingue
  de uno no cubierto. Se amplía si el trader declara el mes completo.
- **Un test actualizado.** `test_mes_del_material` congelaba que solo mayo llevaba sha en la
  cobertura. Ahora exige abril, mayo y agosto, y sigue exigiendo que septiembre no lo lleve.

## 3. Los recuentos (`b471e78` y `5dc3bc3`)

| | abril | agosto |
|---|---|---|
| tramo (fecha mínima y máxima de la columna de fechas) | del 1 al 29 | del 3 al 31 |
| días pedidos (laborables del tramo, todos `dev`) | 21 | 21 |
| ocultos excluidos | 0 | 0 |
| filas leídas (solo de los días pedidos) | 38 | 47 |
| filas sin `initialSL`, que no producen caso | 3 | 5 |
| **casos escritos** | **16** | **19** |
| **operaciones en esos casos** | **35** | **42** |
| **días del tramo sin ninguna operación** | **5** | **2** |
| sesiones sin operación dentro de días con caso | 9 | 12 |

- **Qué no se midió.** Ni RR ni nada más: A-18 está en espera de la respuesta del trader.
- **Dónde está el material.** Cada commit de casos lleva su trailer `Material:` con el sha del
  libro, y `Fuente: ADR-0037, ADR-0039, ADR-0042`.

## 4. La biblioteca `dev`

**41 casos:** 6 de mayo, 16 de abril y 19 de agosto, en `knowledge/cases/dev/`.

## 5. La decisión sobre las ausencias: se quedan como RECUENTOS

Los días del tramo sin operación y las sesiones sin operación **no se convierten en `no_trade`**.
Hay tres motivos:

- **ADR-0016 sigue vigente.** Leer una ausencia como decisión del trader es una inferencia nuestra,
  y exige el ADR que la tome.
- **El tramo es un límite inferior.** Un día del borde sin operaciones puede no estar cubierto.
- **Cuándo se decide.** Si las ausencias cuentan, y cómo, se decide en el commit del criterio de
  fidelidad, **antes de ver resultados del bot**. Decidirlo después sería elegir el criterio
  viendo los datos.

## 6. Las exposiciones (`b8a5591`)

Se añadió una entrada nueva en `HOLDOUT-EXPOSICIONES.md`, solo añadiendo:
- la fecha mínima y la máxima de los dos libros;
- después, las filas de los días `dev` ingeridos, con las columnas `dateStart`, `side`,
  `entryPrice` e `initialSL`, sin agregados.

No quema: abril y agosto no tienen ningún día en ninguna partición.

## 7. Cierre

- **`make check`** en verde en cada commit, con el log borrado. El commit solo se hacía si pasaba.
- **Un matiz sobre `b471e78`.** Se probó con los ficheros de agosto ya en la copia de trabajo, así
  que no con su árbol exacto. Anotado en Technical Debt.
- **Comprobaciones:**
  - guardia de ids OK;
  - `state check` OK;
  - `kit check` del paquete de la sesión 1 y `fidelidad check --artefacto eurusd-2026-09`
    idénticos a su línea base;
  - PREREGISTRO con blob `52649183…`;
  - cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
