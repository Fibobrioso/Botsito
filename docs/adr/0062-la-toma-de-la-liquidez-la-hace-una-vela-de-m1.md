---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `trabajo/nocturno-01oct`, sesión nocturna)
---

# 0062 · La toma de la liquidez de M15 la hace una vela de M1, y lo que eso destapa en el productor (PROPUESTO: pendiente de aceptación del consultor)

> **PROPUESTO.** Escrito en la sesión autónoma de la noche del 30 de septiembre al 1 de octubre de
> 2026 (`docs/nocturno/PLAN-01oct.md`, F34, segunda parte). Va en su propio commit a propósito: es
> la única pieza de la noche que **baja** la cobertura en diagnóstico, y así se puede revisar y
> revertir sola. Lo acepta o corrige el consultor. El campo `status` dice ACTIVE solo porque la
> guardia de ADR (`tests/unit/test_adr.py`) no admite otro valor.

## Decision

### 1. `alcanza_nivel` y `cruza` miran la última M1 cerrada

El trader resolvió A-45 en la sesión 3: la vela que cierra con cuerpo pasado el nivel de M15 es una
vela de M1, no la de quince minutos (`fb-2026-09-29-sesion-03-b2e074e3`,
`fb-2026-09-29-sesion-03-43e0f90e`, `ev-v9-004037-ca58e486`, `ev-v9-004217-c014bfdc`). El motor
evaluaba la toma en la última M15 cerrada, una elección de implementación que ADR-0054 §4 dejó
**PROVISIONAL** hasta esa respuesta. **Este ADR cierra ese provisional**: las dos primitivas de
RN-004 leen la M1 que acaba de cerrar (`DatosMercado.ultima_m1_cerrada`).

- La forma de RN-004 no cambia: la granularidad no era un argumento. Cambian su `entonces`, sus
  notas y las descripciones de los dos predicados.
- El pivote tiene que existir antes de que esa M1 cierre, como antes: es lo que decide el selector
  de A-35, que no se toca.
- `liquidez_m15_criterio_toma` sigue en `cuerpo`: una M1 que solo perfora con la mecha toca el
  nivel y no lo toma.

### 2. A-43 no se activa

El trader dijo que la toma tiene que ocurrir dentro del horario aunque el nivel se formara antes de
las 7 (`ev-v9-004533-d075b080`). A-43 sigue ABIERTA y no se activa aquí. El rango de eventos empieza
en la apertura de la ventana, así que la única vela anterior al horario que todavía puede tomar el
nivel es la M1 que cierra en el instante mismo de la apertura; antes era una M15 entera.

### 3. HALLAZGO: con la toma en M1, el productor encuentra menos esquemas

No es una decisión: es lo que mide el arnés, y va aquí porque cambia cómo se lee esta pieza. Con la
toma antes —ya no espera al cierre de la vela de quince minutos—, la liquidez deja de ser el paso
en que el bot pierde a las operaciones del trader, y pasa a serlo el breaker (las cifras, en
«Impacto»). Lo MEDIDO es que suben los dos motivos de «sin esquema»: más zonas de control que el
tope, y ninguna M1 que pase la referencia. La explicación que sigue sale de leer el código, **no
está medida**:

- el productor guarda **un esquema por sesión**, el primero que encuentra tras la toma. Si esa
  primera ruptura deja más zonas de control que `zonas_control_max_por_esquema`, RN-009 lo invalida
  y la sesión se queda sin zona. Con la toma antes hay más recorrido entre la toma y la ruptura;
- la referencia del breaker es el último pivote de M1 formado hasta la toma
  (`referencia_del_breaker`). Con la toma antes, ese pivote es uno anterior.

**No se revierte.** La lectura la elige el trader, no el ajuste: es la frase con que el propio arnés
encabeza toda corrida en diagnóstico. Lo que el trader hace después de una toma que no da esquema
—otro escenario, otra caja, la orden que sigue viva hasta el siguiente posible punto de breaker
(A-46 y A-38, RESUELTAS)— es la caja por operación y la vida de la orden stop de ADR-0056 §4 y §7,
que no están hechas. Mientras no lo estén, esta pieza deja al productor peor que antes.

## Problema que resuelve

`ACTIVAR-SESION-03.md` §3, desalineación 4: la spec dice M1 y el motor evaluaba la M15. En
construcción, en 13 operaciones el trader entró antes del cierre de la M15 en la que una M1 ya había
tomado el nivel (ADR-0054 §4).

## Alternativas consideradas

1. No aplicar A-45 hasta que exista la caja por operación.
2. Aplicarla ahora, en un commit propio, y medir (la elegida).
3. Evaluar la toma al tick.

## Por que elegimos esta opcion

La 2 hace lo que el trader dijo y lo que el consultor pidió en la lista de ramas (`PROJECT_STATE.md`,
Next Action A3.c), deja el efecto medido por separado y se puede revertir sin tocar nada más.

## Por que descartamos las demas

- La 1 deja al motor haciendo lo que el trader desmintió, y esconde la dependencia en vez de
  medirla. Queda como opción del consultor: revertir este commit.
- La 3 rompe ADR-0028, y el trader habló de una vela que cierra.

## Impacto

- **Código:** `engine/motor.py` (`ultima_m1_cerrada`), `engine/primitivas.py` (`_liquidez`),
  `scripts/embudo_77.py` (el instante de la toma es el del hecho).
- **Spec:** el `entonces` y las notas de RN-004; las descripciones de `alcanza_nivel` y `cruza`.
  `spec_version` **14.2.0 → 14.3.0**.
- **Tests:** `tests/unit/test_preparar_a35.py` cambia de sentido a propósito en dos tests (la toma y
  el primer toque se miden en M1); `tests/unit/test_sesiones_independientes.py` fija la toma de cada
  sesión en su M1.
- **Medido sobre construcción** (abril y agosto de 2026, 42 días `dev`, 84 sesiones, 49 con
  operaciones del trader), antes y después de esta pieza, en DIAGNÓSTICO —A-35
  `cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control`, A-27 con 0 puntos—:
  **ninguna cifra cuenta como medida de fidelidad**.
  - `liquidez_tomada` se produce en 47 de las 49 sesiones, antes 44; RN-004 dispara en 79 sesiones
    de 84, antes 73;
  - `orden_dimensionada` baja de 26 a **14** de 49, y RN-011 de 46 a 26 sesiones de 84; RN-009 sube
    de 73 a 79;
  - en la simulación, las operaciones del bot puntuables bajan de 8 a **2**, y la cobertura **de 2
    de 77 a 0 de 77**; los eventos del bróker, de 16 a 4, y sus rechazos, de 26 a 9;
  - el embudo de las 77: `liquidez` baja de 11 a **1**; `breaker` sube de 24 a **46** (26 por más
    zonas de control que el tope, antes 16; 20 porque ninguna M1 pasa la referencia, antes 8);
    `caja`, de 22 a 12; `reglas`, de 0 a 3 (RN-005); `bróker`, de 2 a 0; `llenado`, de 1 a 0;
    `coincide`, de 2 a **0**; `sesgo` sigue en 15.

## Fecha / fase

2026-09-30 · sesión nocturna, rama `trabajo/nocturno-01oct`. `PROJECT_STATE.md`, Next Action A3.c.

## Estado

ACTIVE (PROPUESTO: pendiente de aceptación del consultor; el campo dice ACTIVE porque la guardia
de ADR no admite otro valor)
