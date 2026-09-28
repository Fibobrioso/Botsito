---
status: ACTIVE
date: 2026-09-28
phase: post-F14 (rama `trabajo/broker-ordenes-stop`)
---

# 0057 · Órdenes stop y rechazo de pendientes en el bróker simulado: lo que ADR-0056 no fijaba

> **PROVISIONAL.** Escrito en la rama `trabajo/broker-ordenes-stop`, la rama 1 de código de
> ADR-0056 §8, con las decisiones que ADR-0056 dejaba abiertas: el precio de una orden stop con
> hueco, qué es exactamente «lado equivocado», contra qué precio se juzga, y el stops level. Todas
> son PROVISIONALES hasta medir en la demo de FTMO en MetaTrader lo que hace el servidor de verdad
> (A-27 y la deuda del bróker del 2026-09-28). Las revisa el consultor antes de cerrar la rama.
> Ninguna cambia la estrategia: el selector de A-47 no existe todavía y RN-011 sigue colocando
> órdenes límite.

## Decision

### 1. La orden stop de entrada se llena al precio del tick que la dispara

Una venta stop salta cuando el BID toca el nivel o baja de él; una compra stop, cuando el ASK lo
toca o lo sube (ADR-0056 §2, como el stop de una posición, DN-1). Se llena al precio de ESE tick
más el deslizamiento fijo de la configuración (DN-3, hoy 0). Si el tick llega ya pasado el nivel
(un hueco), se llena a ese precio, peor que el nivel, **nunca al nivel**. Con el respaldo M1, que
solo sirve para depurar (ADR-0051 §8), al nivel o a la apertura si la vela abre ya pasada, sellado
al cierre de la vela: la misma convención que el stop de una posición (ADR-0051 §4) y, para la
vela del llenado, la misma que la límite (la salida se mira desde la vela siguiente). La posición
guarda el deslizamiento de la entrada, en puntos en contra (`Posicion.deslizamiento_entrada`); en
una límite es siempre 0. Código: `engine/llenado.py`, `primer_llenado_stop`.

### 2. «Lado equivocado» es estricto; el nivel exacto no lo es

Con la cotización del momento de colocar: una LÍMITE de venta por debajo del BID o de compra por
encima del ASK (el precio ya la pasó), y una STOP de venta por encima del BID o de compra por
debajo del ASK. **Una pendiente en el nivel exacto no es lado equivocado**: la límite espera y la
stop salta en el tick siguiente que lo toque. Lo que hace MT5 con una pendiente en el nivel es una
de las cuatro cosas que ADR-0056 §3 manda medir en la demo. Código: `llenado.lado_equivocado`.

### 3. Una pendiente del lado equivocado se RECHAZA, también al modificarla

Se rechaza con el motivo `precio_invalido`, se registra como los rechazos del perfil (ADR-0052 §4)
y el motor la ve como un evento de rechazo. **Nunca se convierte en una orden a mercado ni se llena
a su propio precio.** Una modificación que deja una pendiente del lado equivocado se rechaza igual,
y la orden sigue como estaba (así lo hace MT5 según el consultor; no medido). Es ADR-0056 §3; lo
que añade este ADR es la modificación. Código: `Broker._precio_infringido`, `Broker.modificar`.

### 4. La cotización con la que se juzga

El último tick anterior o igual al instante de colocar, mirando hacia atrás minuto a minuto; donde
no hay ticks, la última M1 CERRADA: BID igual a su cierre y ASK igual al cierre más el spread
supuesto de esa hora (ADR-0051 §1). Si no hay ninguna de las dos antes del instante, la orden no se
juzga y pasa. Código: `Mercado.cotizacion`.

### 5. El stops level del bróker es un parámetro del perfil de la firma, UNKNOWN

`firma_stops_level_puntos`, en `knowledge/cuentas/ftmo-2step-swing-100k.yaml`, `prop_firm`,
`puntos`, **UNKNOWN**: FTMO-REGLAS R11 lo da por NO ENCONTRADA y se mide en la demo (A-27).
**No es** `instrumento_stops_level`, el de la estrategia, que RN-026 usa para abstenerse y que es
DEFAULT_AMBIGUOUS con 0, medido en otra firma: ponerlo en UNKNOWN habría cambiado la estrategia, y
esta rama no puede. Son la misma magnitud física, así que cuando se mida los dos tienen que llevar
el mismo valor; el cruce entre perfil y registro que ya existe no los compara porque se llaman
distinto, y eso queda como deuda.

- **Sin valor**, el bróker **se niega a colocar una orden stop**, nombrando A-27 y la salida en
  diagnóstico. **Una límite no se juzga por stops level** mientras no se conozca: es lo que hace
  hoy, con el 0 implícito de la otra firma, y así la línea base de las límites no cambia.
- **En diagnóstico**, `--diagnostico-a27 <puntos>` (solo con `--simular`) corre con un stops level
  hipotético, etiquetado `DIAGNOSTICO-A27-<puntos>` en cada línea, fichero y página, como ADR-0054.
  Con el valor ya fijado en el perfil, el diagnóstico se rechaza.
- **Con valor**, medido o en diagnóstico, se exige para límites y stops: el precio de la pendiente
  a no menos que el stops level del ASK (compras) o del BID (ventas), y su stop y su objetivo a no
  menos que el stops level del precio de la orden. Si no, se rechaza con el motivo `stops_level`.
  El freeze level no se modela.

### 6. Lo que no cambia

- El hecho de origen bróker `orden_limite_pendiente` cuenta también una orden stop pendiente: el
  contrato del motor es «hay una pendiente», y el nombre se queda para no tocar la spec.
- La estrategia coloca límites por la misma vía de siempre (`colocar_orden_limite`). La orden stop
  solo la usa, en esta rama, el test de punta a punta que desvía esa acción.

## Problema que resuelve

El bróker simulado solo tenía órdenes límite y llenaba en el tick siguiente, a su propio precio,
una límite colocada con el precio ya pasado el nivel (`DISENO-ENTRADA-RUPTURA.md` §1.2): peor que
el mercado y algo que un bróker real no haría. El trader entra con órdenes stop
(`ORDEN-STOP-O-LIMITE.md` §10) y la rama 2 de ADR-0056 necesita un bróker que las sepa llenar.

## Alternativas consideradas

1. Para el hueco: llenar al nivel (optimista), o al precio del tick (la elegida).
2. Para la pendiente del lado equivocado: seguir llenándola a su precio, convertirla en orden a
   mercado, o rechazarla (la elegida, que ADR-0056 §3 ya fijó).
3. Para el nivel exacto: rechazarlo, o aceptarlo (la elegida).
4. Para el stops level: poner `instrumento_stops_level` en UNKNOWN, o un parámetro nuevo del perfil
   (el elegido); y con él sin valor, negarse a todo, o solo a la orden stop (el elegido).

## Por que elegimos esta opcion

El precio del tick es lo único que no inventa un llenado mejor que el mercado. Aceptar el nivel
exacto evita rechazar órdenes que hoy esperan y se llenan bien. Un parámetro nuevo en el perfil es
donde ADR-0050 pone lo que es de la firma, y deja la estrategia intacta. Negarse solo a la orden
stop sigue el patrón de ADR-0054 donde el valor es imprescindible, sin mover la línea base de las
límites, que el consultor exige idéntica.

## Por que descartamos las demas

- Llenar el hueco al nivel regala puntos al bot en cada salto.
- Convertir la pendiente en mercado inventa una orden que nadie puso; llenarla a su precio es lo de
  hoy, y es falso.
- Rechazar el nivel exacto rechazaría la orden «en el nivel» de agosto, que hoy espera y se llena.
- Poner `instrumento_stops_level` en UNKNOWN deja RN-026 en DESCONOCIDO, y un gate DESCONOCIDO
  prohíbe abrir (ADR-0049 H4): cambiaría todas las corridas.
- Negarse también con las límites obligaría a una bandera nueva en cada corrida de hoy y rompería
  la comparación byte a byte.

## Impacto

- `engine/llenado.py` (`primer_llenado_stop`, `lado_equivocado`, `Mercado.cotizacion`),
  `engine/broker.py` (`colocar_stop`, rechazo por precio y por stops level, `modificar` que rechaza,
  tipo en la orden, deslizamiento en la posición), `engine/perfil_cuenta.py`, `engine/simulacion.py`,
  `engine/cableado.py`, `engine/diagnostico.py` y la CLI (`--diagnostico-a27`).
- `knowledge/cuentas/ftmo-2step-swing-100k.yaml`: `firma_stops_level_puntos` UNKNOWN.
- La línea base de construcción con órdenes límite cambia en las órdenes que se colocaban del lado
  equivocado, que ahora se rechazan, y EN CASCADA: sin sus pérdidas, RN-032 deja de prohibir
  abrir y aparecen órdenes en días que antes bloqueaba. Caso a caso en
  `docs/validation/BROKER-ORDENES-STOP.md` §3; lo revisa el consultor.
- Pendiente de la demo de FTMO: el comportamiento real en el nivel exacto y al modificar, el
  precio de referencia, el stops level y el freeze level.

## Fecha / fase

2026-09-28 · post-F14, rama `trabajo/broker-ordenes-stop`, rama 1 de código de ADR-0056.

## Estado

ACTIVE
