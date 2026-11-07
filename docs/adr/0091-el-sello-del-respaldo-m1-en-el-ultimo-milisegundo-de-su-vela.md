---
status: ACTIVE
date: 2026-11-07
phase: post-F14 (rama `trabajo/sello-respaldo-m1`, R3.6 de la hoja de ruta; H de la Next Action)
---

# 0091 · El evento del respaldo M1 se sella en el último milisegundo de su vela, antes de que el motor decida en su cierre (enmienda ADR-0051 §5, ADR-0057 §1, ADR-0068 §2 y ADR-0083 D2)

> Decisión del consultor del 2026-11-07 (respuesta a la PARADA de `trabajo/sello-respaldo-m1`,
> puntos 0 a 7), sobre lo medido en `docs/validation/SELLO-RESPALDO-M1.md` §0. Recuadros en ADR-0051
> §5 (y su NOTA del 2026-10-29), ADR-0057 §1, ADR-0068 §2 y ADR-0083 D2, y fila del índice. **Solo
> cambia los minutos SIN ticks**: el bot en vivo opera con ticks (ADR-0051 §8), y el respaldo M1 solo
> cubre los minutos que no los tienen (en construcción, las horas perdidas de los manifiestos).

## Decision

### 1. El sello: el último milisegundo de la vela

En las tres funciones del respaldo de `engine/llenado.py` (`primer_llenado_limite`,
`primer_llenado_stop`, `primera_salida`), el instante de un evento de la vela k es **k fin − 1 ms**
(`_sello_ms`), y una vela entra si ese instante cae en `(desde, hasta]`. Antes era k fin, un
milisegundo DESPUÉS de que el motor decidiera en el cierre de k (`cableado.py:302`,
`hasta_ms = instante · 60000 − 1`): el `avanzar` de ese cierre no llegaba a la vela k, y lo que el
motor cancelaba o cerraba en ese cierre no se evaluaba nunca contra la vela en que aún vivía. Ahora
la vela k se evalúa en el `avanzar` del cierre de k, ANTES de que el motor decida. `Mercado.cotizacion`,
que también usa `_fin_ms`, no cambia (sigue en la deuda de las cotizaciones sin tick, ADR-0057 §4).
La condición de Z (ADR-0051 §5, NOTA del 2026-10-29: la vela solo evalúa lo decidido cuando
EMPEZÓ) no cambia.

### 2. Los lectores del minuto de apertura: neutros

El ADR cambia QUÉ VELA SE EVALÚA, no a qué minuto ni a qué día pertenece un llenado. Un llenado del
respaldo sellado en k fin − 1 ms sigue siendo, para todo lo que viene después, de la vela siguiente,
como cuando se sellaba en k fin. Una sola definición, `minuto_de_apertura(p)` =
`(p.abierta_ms + 1) // 60000` (`engine/broker.py`), la leen:

- `Broker._marcar_hasta`: el primer minuto que se marca (la vela del llenado no se marca: sus precios
  pueden ser anteriores al llenado);
- `Broker._swaps`: el corte desde el que se cuentan los swaps (un llenado en la última vela antes del
  corte no paga el swap de ese corte, como antes);
- `Broker._limite_infringido`: el día local de la posición para `posiciones_dia_max`;
- `MotorCableado._operaciones_del_bot` (`cableado.py`): la sesión de la posición;
- el break even por velas (RN-014, `primitivas_broker.py`, `m1_entre`): las M1 desde la siguiente a
  la del llenado.

**Se quedan en el instante sellado**, porque son un instante y no un minuto: las comisiones de la
apertura (`Broker._operacion`), el instante de la operación para el criterio de fidelidad
(`cableado.py`, `_operaciones_del_bot`), la apertura de la `Operacion`, el detalle del visor y la
tabla «### Ordenes». El «+ 1» mueve también un llenado por TICK en el milisegundo .999 de un minuto
al minuto siguiente: es la misma convención que `_sesion_de` aplica a `colocada_ms`
(`cableado.py`), y un tick en .999 cae en el último milisegundo de su minuto.

### 3. Los lectores de `cerrada_ms`: en el instante sellado

Una salida del respaldo (stop u objetivo) se sella también en k fin − 1 ms. Cada lector, con su
porqué:

- `Broker._cerrar` (`p.cerrada_ms = instante`): el instante sellado.
- La comisión del cierre (`Broker._operacion`): en el instante sellado, como la de la apertura.
- Los swaps hasta el cierre (`Broker._operacion`, `instante <= cerrada_ms`) y `_marcar_hasta(instante)`
  antes de cerrar: **no neutros**. Una posición que sale por la última vela antes de un corte sale
  ANTES del corte, y no paga su swap; con el sello en k fin lo pagaba, aunque la vela que la cerró
  acabara en el corte. Es lo correcto: la posición no vivió más allá de su vela.
- Las marcas dentro de la operación (`abierta_ms <= ms <= cerrada_ms`): la marca de la vela k se toma
  en k fin − 1 ms y sigue dentro.
- El cierre de la `Operacion` y el visor (`cableado.py`, `detalle_para_visor`): el instante sellado.

### 4. Lo que el motor ve un cierre antes

El motor ve el evento del respaldo de la vela k en el cierre de k, no en el siguiente. Todo lo que
decide a partir de él llega un cierre antes:

- la orden siguiente se coloca un cierre antes (en la verificación de §7, 2026-04-22, 04-23 y 08-20);
- **ADR-0083 D2** (`cableado.correr_dia`: `broker.avanzar(hasta_ms)` en `engine/cableado.py:304`,
  `_a_la_cuenta` en `:305` y `_el_punto_tras_el_evento` en `:307`, antes del intérprete): un
  rechazo al llenar gasta el punto, y un stop u objetivo sin ganancia libera la zona, en el cierre
  de k; la reentrada por D5 sale en ese mismo cierre;
- **D4** (RN-011, `operacion_abierta`): la posición abierta se ve en el cierre de k.

### 5. El fin del día y el borde de ADR-0068

Se aceptan. Las dos velas transcurren enteras antes de su borde:

- **el fin del día** (`cableado.correr_dia`, `fin_ms = ultimo · 60000 − 1`, `engine/cableado.py:355`): la última vela de la
  ventana se evalúa en el `avanzar(fin_ms)`, antes de cerrar lo vivo y cancelar lo pendiente; una
  pendiente que esa vela cruza se llena, y una posición cuyo stop toca sale por él;
- **el borde de ADR-0068**: un llenado en la vela que acaba en W (el inicio de la ventana prohibida)
  se sella en W − 1 ms, fuera de la ventana; la pendiente que siga viva se cancela al empezar la
  ventana, como hasta hoy (recuadro en ADR-0068 §2).

### 6. La versión anterior se queda

`Orden.anterior` y `Posicion.stop_anterior` (ADR-0051 §5, NOTA; ADR-0065 §4): el motor mueve el stop
o modifica la orden en el cierre de k menos 1 ms, un instante que cae dentro de la vela k; con este
sello la vela k ya se evaluó en el `avanzar` de ese cierre, ANTES del cambio y con la versión
vigente, y no se vuelve a evaluar (su sello no es posterior al cambio). Desde el motor la versión
anterior ya no se alcanza. Se queda para quien decida a media vela (la
repetición del trader, `abrir_conocida`, y los tests), y retirarla es otra rama.

### 7. Alcance medido

En `SELLO-RESPALDO-M1.md` §0.c, con el visor por caso sobre once días de desarrollo (enero, abril,
julio y agosto de 2026; ningún día reservado): **27 cancelaciones del bot en el cierre de una M1 sin
ticks**, de las que la vela k habría llenado **2** (2026-01-23 o29 y 2026-07-10 o3); con este sello
son **2 operaciones nuevas del bot**, y las demás operaciones de esos días no cambian. Ninguna cifra
agregada sobre un mes ni sobre la construcción: lo demás lo ve la re-corrida que cuenta
(ADR-0070 §3).

## Problema que resuelve

El respaldo sellaba el evento de una vela en su cierre, un milisegundo después de que el motor
decidiera (ADR-0051 §5, ADR-0057 §1). La vela k no se evaluaba para la orden que el motor cancelaba
en su cierre (las «22 de 1002» de RESPALDO-M1.md §0.l, que en main son 27 en once días), y el motor
veía un llenado del respaldo un cierre tarde.

## Alternativas consideradas

1. **(c) sellar en k fin − 1 sin más**: metía la vela del llenado en las marcas, en el break even por
   velas y en la sesión (SELLO-RESPALDO-M1.md §0.d, S1-S3; diagH).
2. **(d) evaluar antes de decidir**: el bróker avanza hasta `t` y el motor decide en `t`. Enmienda
   ADR-0053 §4 y §5, empeora las cotizaciones sin tick y rompe 17 tests; descartada (D3 del encargo).
3. **Declararlo límite del respaldo**: la regla D2 del encargo lo admitía solo si ninguna de las
   cancelaciones cambiaba una operación; cambian 2.

## Por que elegimos esta opcion

(c) con los lectores del minuto de apertura neutros (la forma (c2)) evalúa la vela k para lo que vivía
en ella sin cambiar a qué vela, minuto o día pertenece lo que viene después, y deja el reloj del
motor como está (ADR-0053 intacto).

## Por que descartamos las demas

(c) sola cambiaba más de lo que pretende; (d) cambia el reloj del motor y obliga a decidir la deuda de
las cotizaciones; el límite declarado contradice lo medido.

## Impacto

- **Código**: `engine/llenado.py` (`_sello_ms` y las tres funciones), `engine/broker.py`
  (`minuto_de_apertura` y sus tres lectores), `engine/cableado.py` (la sesión),
  `engine/primitivas_broker.py` (el break even por velas).
- **Tests**: `tests/unit/test_sello_respaldo.py` (nuevo) y los diez de `main` que fijaban el sello en
  k fin, reescritos (SELLO-RESPALDO-M1.md §7).
- **Lo que no cambia**: los ticks, el `desde` exclusivo, el «ahora − 1», la vela de la salida tras un
  llenado (ADR-0051 §3, su NOTA), `Mercado.cotizacion`, el reloj del motor (ADR-0053).
- **La repetición del trader sin ticks** (ADR-0051 §8) cambia otra vez: no se vuelve a correr.

## Fecha / fase

2026-11-07 · post-F14, `trabajo/sello-respaldo-m1` (R3.6).

## Estado
ACTIVE
