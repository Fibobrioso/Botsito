---
status: ACTIVE
date: 2026-09-24
phase: post-F14 (rama `trabajo/criterio-fidelidad`)
---

# 0043 · Criterio de fidelidad en desarrollo

## Decision

El criterio con el que se comparará lo que haría el bot con lo que hizo el trader, en desarrollo,
se fija AQUÍ, antes de escribir una línea del motor. Texto literal del consultor:

- **Unidad:** la operación, dentro de su día y su sesión.
- **Emparejamiento uno a uno:**
  - una operación del bot empareja con una del trader si coinciden el día, la sesión y la
    dirección, |Δentrada| ≤ 3 puntos y |Δinstante de llenado| ≤ 15 min;
  - si hay varias candidatas, gana la de menor |Δinstante|, luego la de menor |Δentrada|, y luego
    la más temprana (determinista).
- **Métricas:**
  - cobertura = operaciones del trader emparejadas / operaciones del trader;
  - precisión = operaciones del bot emparejadas / operaciones del bot, contando solo los días con
    al menos una operación del trader;
  - las operaciones del bot en días sin ninguna del trader se informan aparte y no puntúan
    (ADR-0016);
  - se informa también la distribución de Δinstante (cuántas en el mismo minuto) y de Δentrada.
- **Fuera del criterio hasta que se resuelva su ambigüedad:** stop (A-18, A-31), TP y resultado
  (ADR-0037 §7), gestión (A-13, A-33).
- **Conjuntos:**
  - construcción = abril y agosto;
  - medida = mayo (y marzo cuando entre);
    > **NOTA del 2026-09-24 (ADR-0046, no reescribe el cuerpo).** «Marzo cuando entre» significa
    > SOLO su parte `fidelidad-dev`: marzo entra por el camino de fidelidad (ADR-0036), y lo que caiga
    > en `fidelidad-2` y `fidelidad-3` queda oculto y no es medición de desarrollo.
  - mayo se mide una vez por versión de la spec; si la spec cambia después de ver el resultado de
    mayo, mayo pasa a construcción y queda escrito.
- **Umbral de desarrollo:** cobertura ≥ 70 % y precisión ≥ 60 % sobre el conjunto de medida. Esto
  NO es el PREREGISTRO del holdout.
- **Calentamiento:** el bot puede leer velas de días anteriores para su sesgo; solo puntúan los días
  evaluados. Leer velas no es abrir casos (ADR-0021 §1).
- **Cambios:** este criterio no se modifica una vez que el motor produzca su primera salida sobre el
  conjunto de medida, salvo con un ADR nuevo que diga por qué y declare quemado lo que se haya
  visto.

**Cómo se implementa.**
- **Las cifras** viven en `knowledge/cases/criterio_fidelidad.yaml` (ADR-0002).
- **El emparejamiento y las métricas** están en `src/botsito/cases/criterio_fidelidad.py`, una
  función pura fuera del motor.
- **Unidades:**
  - un punto es 0,00001 en EURUSD (`domain/velas.py`: 100000 puntos por unidad);
  - el instante del trader es el LLENADO, medido en `docs/validation/INSTANTE-LLENADO-SALIDA.txt`.
- **El desempate es voraz y global:** entre todas las parejas compatibles de la medida, en el orden
  dicho, y ninguna operación se usa dos veces.
- **Sin denominador, la métrica queda sin definir y se informa así.** El módulo no divide por cero.

## Problema que resuelve

Sin un criterio fijado antes, cualquier cifra de fidelidad se podría leer a favor después de verla.
Y el inventario (`INVENTARIO-FIDELIDAD.md`) midió que el motor no existe: es el momento en que
fijarlo no cuesta nada, porque todavía no hay nada que ver.

## Alternativas consideradas

- Comparar por sesión (hubo o no operación, y su dirección) en vez de por operación.
- Comparar también el stop y el TP.
- Fijar el criterio después de ver una primera salida del motor.

## Por que elegimos esta opcion

- **Es la unidad que traen los casos:** cada operación con su instante de llenado, su dirección
  y su entrada.
- **Deja fuera lo que no es comparable hoy.** El stop está atado a A-18 y A-31, y el TP y el
  resultado no están en el caso.
- **Las tolerancias salen de lo medido:**
  - las series difieren 1-2 puntos (A-16);
  - el instante es el llenado;
  - los datos son M1 y el xlsx trae segundos.

## Por que descartamos las demas

- **Por sesión** pierde la mitad de la información: 27 de los 41 casos tienen más de una
  operación el mismo día.
- **Stop y TP** no se pueden comparar mientras sus ambigüedades sigan abiertas.
- **Fijarlo después** es exactamente lo que un criterio pre-escrito impide.

## Impacto

- **Nuevos ficheros:**
  - `src/botsito/cases/criterio_fidelidad.py`;
  - `knowledge/cases/criterio_fidelidad.yaml`;
  - los tests de `tests/unit/test_criterio_fidelidad.py`, todos sintéticos.
- **Ninguna línea del motor.**
- **El siguiente paso es el motor**, primera regla: el sesgo H4 (RN-003), con test contra velas
  y sin tocar mayo.

## Fecha / fase

2026-09-24, post-F14, rama `trabajo/criterio-fidelidad`. Next Action 18.

## Estado

ACTIVE
