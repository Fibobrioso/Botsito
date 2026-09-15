---
status: ACTIVE
date: 2026-09-14
phase: post-F13 (antes de F18-F24)
---

# 0028 · El reloj del motor: tres fases, y el riesgo va por tick

## Decision

El bucle del motor tiene **tres fases con cadencias distintas**. No es una preferencia: sale del
reglamento de la firma (ADR-0026) y de lo que la auditoría del 2026-09-13 midió ejecutando la spec.

1. **Fase de riesgo — por tick.** El veto mira **equity**, no saldo: FTMO define el límite diario
   como aquello por debajo de lo cual *«equity cannot drop at any time»*, y equity incluye posiciones
   abiertas, comisiones y swaps. Un veto evaluado solo al cierre de cada M1 podría dejar pasar una
   violación dentro de la vela. La fase de riesgo se evalúa en cada tick recibido, puede cerrar a
   mercado y prohibir abrir, y **es la única fase que puede hacer lo primero por su cuenta**.
2. **Fase de estrategia — al cierre de M1.** Las reglas de entrada, sesgo, zonas y gestión se
   evalúan sobre velas cerradas. Ya estaba implícito en la operativa (la orden límite se reubica al
   completarse una zona, RN-006) y es lo que mantiene el consumo de peticiones muy por debajo del
   límite de `firma_mensajes_dia_max`.
3. **Fase de órdenes — por evento del bróker.** Llenado, salto de stop, alcance de objetivo y
   rechazos se procesan cuando llegan, no en la vela siguiente.
4. **Dentro de un mismo evento, la evaluación es a punto fijo con refracción**: cada regla dispara
   como mucho una vez por evento y, tras cada disparo, se vuelve a empezar por los `gate`. Así se
   conserva la precedencia por clase de ADR-0018 y el estado que produce una acción está a la vista
   de los gates en el mismo evento.
5. **Los hechos `operacion_abierta` y `orden_limite_pendiente` se derivan del bróker**, no se fijan
   por regla. El motor los lee del estado de órdenes y posiciones que la fase 3 mantiene.

## Problema que resuelve

Es el ADR que la auditoría del 2026-09-13 señaló como el primero por coste de reescritura: *«Ningún
ADR (0001-0025) fija si el motor evalúa al cerrar cada M1, en cada tick o en eventos de orden»*
(`docs/validation/AUDITORIA-2026-09-13-ultracode.md` §9.3 (a)). Sin él, F23 elige la cadencia al
escribir el bucle y F24 la hereda, y cambiarla después es rehacer los dos.

Y dos defectos medidos en ejecución (intérprete de juguete de la auditoría, §4):

- **Sin punto fijo, una operación de más.** Con un stop y un esquema nuevo en el MISMO evento, se
  abre una 11.ª orden con 4,889 % ya perdido (máximo 5,365 %); con punto fijo se queda en 10 órdenes
  y 4,885 %. **Ojo a lo que el punto fijo NO arregla**: el tope del 4,5 % se sobrepasa igual, porque
  `alcanza_tope` se comprueba antes de abrir sin descontar el riesgo de la operación que se abre
  ([d1-interprete-04], el único hallazgo que el escéptico confirmó sin matizar). Eso es una lectura
  prospectiva del tope que ninguna regla declara todavía, y no lo decide este ADR.
- **Copias del bróker desincronizadas.** RN-010 enciende `operacion_abierta` sin apagar
  `orden_limite_pendiente`, y el par RN-006/RN-014 vuelve a coincidir en el mismo evento; RN-002
  llega a cerrar una posición ya cerrada. *«[...] derivar `operacion_abierta` y `orden_limite_pendiente`
  del bróker (en vez de fijarlos por regla) resuelve el par RN-006/RN-014 en todas las trazas
  probadas»* (§4.3).

## Alternativas consideradas

1. **Tres fases con cadencia propia, punto fijo y hechos del bróker derivados** (elegida).
2. **Todo al cierre de M1**, riesgo incluido.
3. **Todo por tick**, estrategia incluida.
4. **Hechos del bróker fijados por regla**, apagándolos con reglas nuevas.

## Por que elegimos esta opcion

Porque cada fase tiene la cadencia de lo que vigila. El riesgo vigila una magnitud que el
reglamento mide de forma continua; la estrategia, velas cerradas que el trader lee cerradas; las
órdenes, eventos que llegan cuando llegan. Y el punto fijo con refracción es la única semántica de
evaluación que la auditoría probó sin cambiar la conducta de ninguna traza salvo el redondeo, que
pasa de tardío a puntual (26 escenarios, 0 diferencias de conducta).

## Por que descartamos las demas

- **(2) Todo al cierre de M1**: el veto llegaría hasta un minuto tarde sobre una magnitud que la
  firma mide en todo instante. Un salto dentro de la vela rompe la cuenta antes de que el motor mire.
- **(3) Todo por tick**: evaluaría esquemas sobre velas abiertas, que no es lo que hace el trader, y
  multiplicaría las reubicaciones de la orden límite; con 2.000 peticiones al día como práctica
  prohibida, es diseñar hacia la infracción.
- **(4) Fijar y apagar por regla**: mantiene dos fuentes de verdad para el mismo hecho, y la
  auditoría midió que se desincronizan. Las copias del bróker son el caso en que derivar es
  estrictamente mejor, y lo dice el propio laboratorio de la alternativa B de la auditoría (§4):
  *«para las copias del bróker es menos robusta que derivarlas del bróker»*.

## Impacto

- **F14b §0 se deshace en su mitad**: RN-010 deja de fijar `operacion_abierta`. **La spec NO se toca
  en esta rama** (alcance cerrado): RN-010, RN-011 y RN-013 siguen fijando los dos hechos en su
  `forma`, y hasta que el brief siguiente las reescriba **la spec contradice este ADR**. Está
  declarado en el informe de la rama como pendiente, y F18 no puede empezar sin ese cambio.
- **Lo que queda para F14b** es solo la caducidad de `liquidez_tomada` y `zona_perdida`, que es
  donde de verdad falta el evento `se_marca_liquidez_m15` (y A-24..A-26).
- **F16 (ticks) pasa a ser precondición del backtest fiel**, porque la fase de riesgo necesita
  ticks. F23 y F24 se escriben contra este ADR.
- **La lectura prospectiva del tope** (descontar la operación que se abre) queda como decisión
  abierta, fuera de esta rama.

## Fecha / fase

2026-09-14, después de F13 (decisión del consultor, sobre la auditoría del 2026-09-13).

## Estado

ACTIVE
