---
status: ACTIVE
date: 2026-10-26
phase: post-F14 (rama `trabajo/activar-sesion-05-motor`, R4.1 de la hoja de ruta)
---

# 0086 · RN-020 retira la orden pendiente al llegar al tope del trader, como RN-036 (enmienda ADR-0077 §3)

> **DECISIÓN DEL CONSULTOR** del 2026-10-26 (encargo de `trabajo/activar-sesion-05-motor`, punto
> 8, y su respuesta a la PARADA, punto 8). No sale de ningún ítem de evidencia: el trader no ha
> dicho qué hace con una orden sin llenar cuando llega a su tope del día. **Enmienda ADR-0077 §3**
> en «RN-020 no cambia (ni su prosa ni lo que hace con una orden pendiente, que es nada: heredado
> 35)», con recuadro allí y su fila del índice; cierra el heredado 35 de
> `docs/runbooks/ACTIVAR-A35-A44.md` §5.1 (NOTA allí).

## Decision

### 1. Lo que cambia

La forma de RN-020 gana la acción `retirar_ordenes_pendientes` (la misma de RN-036: sin
argumentos, idempotente, cancela lo que haya, cero o una). Cuando la pérdida acumulada del día
llega a `perdida_maxima_diaria`, o mientras `detenido_por_tope` esté encendido, RN-020 prohíbe
`abrir_operacion`, fija `detenido_por_tope` y retira la orden pendiente que quede. RN-020 no lee
nada más ni cambia lo que cuenta: el acumulador, el corte (`reloj_dia_riesgo`, ADR-0027), el
alcance y la unidad de A-44 son los que eran.

### 2. El modelo y el motivo son los de RN-036

ADR-0077 §3 lo decidió para la racha: se retira «porque el bróker la llenaría por ticks mientras
el trader ya ha dejado de operar». El tope del día es la otra detención del trader (RN-020, A-44;
sesión 5, S-4: «solo el del día y las 9 seguidas», `ev-v15-000856-ee8f7ba3`, el ítem que ya cita
RN-020), y una orden viva al llegar a él la llenaría
igual. Dentro de la spec, RN-011 no coloca con una orden pendiente ni con una posición viva, así
que en el cierre de M1 en que cae la pérdida que alcanza el tope no suele quedar ninguna
pendiente: la acción es la red de seguridad, como en RN-036, y vale para cualquier pendiente que
llegue viva a ese cierre (una colocada y sin llenar cuando el tope se alcanza por otra vía).

### 3. Lo que NO se decide aquí

- Nada de A-44: sigue ABIERTA con sus parámetros `perdida_trader_*` como los dejó
  `trabajo/activar-sesion-05`; la magnitud es la primera pregunta de la sesión 6.
- Nada de RN-036: lo que cuenta y cuándo detiene no cambia (su reinicio lo cambió la sesión 5,
  recuadro en ADR-0077 §5).

## Problema que resuelve

Con A-44 activada (sesión 5), RN-020 prohibía abrir y fijaba `detenido_por_tope`, pero dejaba
viva la orden pendiente, que el bróker podía llenar por ticks con el trader ya parado: el
heredado 35, anotado en `ACTIVAR-A35-A44.md` §5.1 y en las notas de RN-020 desde el commit de
A-44.

## Alternativas consideradas

1. La acción de RN-036 también en RN-020 (la elegida).
2. Dejar la pendiente viva hasta RN-035 (el último minuto o la sesión siguiente).
3. Preguntarlo al trader en la sesión 6.

## Por que elegimos esta opcion

Porque es el mismo caso que RN-036 con el mismo motivo, y el consultor ya lo decidió allí; una
regla que detiene al trader y deja una orden que se puede llenar es la peor de las dos lecturas.

## Por que descartamos las demas

- La 2 deja llenar una orden con el trader parado por su propio tope.
- La 3 deja el hueco abierto hasta la sesión 6 sin que el trader haya mostrado ninguna
  preferencia distinta a la de RN-036.

## Impacto

- **Spec:** RN-020, su `entonces` y su forma (`hace` gana `retirar_ordenes_pendientes`), sus
  notas; `spec_version` 18.4.0 → **18.5.0** (una regla hace algo nuevo).
- **Código:** ninguno nuevo: la acción existe desde ADR-0077 (`engine/primitivas_broker.py`).
- **Docs:** recuadro en ADR-0077 §3 y su fila del índice; NOTA en `ACTIVAR-A35-A44.md` §5.1.
- **Tests:** `tests/unit/test_rn020_retira_pendiente.py` (nuevo): por el cableado real, con un
  acumulador `perdida_dia` sintético que alcanza el tope con una orden colocada y sin llenar,
  RN-020 dispara y la orden queda CANCELADA en ese cierre; en `main` seguía viva hasta RN-035.
- **Sin arnés y sin material**: velas sintéticas.

## Fecha / fase

2026-10-26 · rama `trabajo/activar-sesion-05-motor` (R4.1). Informe:
`docs/validation/ACTIVAR-SESION-05-MOTOR.md`.

## Estado

ACTIVE
