---
status: ACTIVE
date: 2026-11-07
phase: post-F14 (rama `trabajo/sello-respaldo-m1`, R3.6 de la hoja de ruta; H de la Next Action)
---

# 0091 · El evento del respaldo M1 se sella en el último milisegundo de su vela, antes de que el motor decida en su cierre (enmienda ADR-0051 §5, ADR-0057 §1, ADR-0068 §2 y ADR-0083 D2)

> Decisión del consultor del 2026-11-07 (respuesta a la PARADA de `trabajo/sello-respaldo-m1`,
> puntos 0 a 7), sobre lo medido en `docs/validation/SELLO-RESPALDO-M1.md` §0. Recuadros en ADR-0051
> §5 (y su NOTA del 2026-10-29), ADR-0057 §1, ADR-0068 §2 y ADR-0083 D2, y fila del índice. **Solo
> cambia lo sellado por el respaldo M1, es decir, los minutos SIN ticks**: el bot en vivo opera con
> ticks (ADR-0051 §8), y el respaldo M1 solo cubre los minutos que no los tienen (en construcción,
> las horas perdidas de los manifiestos). **Con ticks no cambia nada**: el «+ 1» de
> `minuto_de_apertura` es solo para las posiciones con `fuente_apertura == RESPALDO_M1` (§2;
> respuesta del consultor a la entrega de la fase 2, punto 1).

## Decision

### 1. El sello: el último milisegundo de la vela

En las tres funciones del respaldo de `engine/llenado.py` (`primer_llenado_limite`,
`primer_llenado_stop`, `primera_salida`), el instante de un evento de la vela k es **k fin − 1 ms**
(`_sello_ms`), y una vela entra si ese instante cae en `(desde, hasta]`. Antes era k fin, un
milisegundo DESPUÉS de que el motor decidiera en el cierre de k (`engine/cableado.py:303`,
`hasta_ms = instante · 60000 − 1`): el `avanzar` de ese cierre no llegaba a la vela k, y lo que el
motor cancelaba o cerraba en ese cierre no se evaluaba nunca contra la vela en que aún vivía. Ahora
la vela k se evalúa en el `avanzar` del cierre de k, ANTES de que el motor decida. `Mercado.cotizacion`,
que también usa `_fin_ms`, no cambia (sigue en la deuda de las cotizaciones sin tick, ADR-0057 §4).
La condición de Z (ADR-0051 §5, NOTA del 2026-10-29: la vela solo evalúa lo decidido cuando
EMPEZÓ) no cambia. **La vela k que se vuelve a mirar**: con el sello en k fin − 1 ms = `ahora`, el
«ahora − 1» deja que el `avanzar` siguiente vuelva a mirar la vela k para lo que no cambió; partir
el avance no cambia nada (`test_partir_el_avance_en_cada_cierre_da_los_mismos_eventos_y_las_mismas_marcas`,
y `test_partir_el_avance_en_instantes_redondos_da_los_mismos_eventos_y_marcas`, que en `main`
rompía solo por la marca adelantada que corrige (e2)), y lo que sí cambia en el cierre de k lleva su
instante en `desde` y la deja fuera: la orden colocada (`test_respaldo_m1_decision.py`:
`test_una_stop_colocada_en_el_cierre_de_una_m1_sin_ticks_no_se_llena_con_esa_vela` y
`test_una_limite_colocada_…`), la modificada (`test_la_vela_de_una_modificacion_no_llena_la_version_nueva`),
el stop movido (`test_el_stop_movido_en_el_cierre_de_una_m1_sin_ticks_no_salta_con_esa_vela`) y
la posición abierta con la vela k
(`test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente`).

### 2. Los lectores del minuto de apertura: neutros

El ADR cambia QUÉ VELA SE EVALÚA, no a qué minuto ni a qué día pertenece un llenado. Un llenado del
respaldo sellado en k fin − 1 ms sigue siendo, para todo lo que viene después, de la vela siguiente,
como cuando se sellaba en k fin. Una sola definición, `minuto_de_apertura(p)` (`engine/broker.py`),
con su CONDICIÓN: si la posición la abrió un llenado del respaldo (`p.fuente_apertura ==
RESPALDO_M1`, la única fuente que las tres funciones del respaldo ponen a un llenado,
`engine/llenado.py:42`), `(p.abierta_ms + 1) // 60000`; con cualquier otra apertura (un tick, aunque
caiga en el milisegundo .999 de un minuto; `abrir_conocida`, con su fuente por defecto `conocida` o
`caso`, la que pasan sus tres llamadores), `p.abierta_ms // 60000`, como antes del ADR. La
condición mira la cadena de la fuente: un `abrir_conocida(..., fuente="respaldo_m1")` llevaría el
«+ 1»; hoy nadie lo hace (revisor, tercera pasada, b1), y quien lo haga declara que esa apertura la
selló el respaldo. Ninguna otra fuente se sella en k fin − 1 ms: los
ticks llevan su instante y `abrir_conocida` el que recibe. La leen:

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
tabla «### Ordenes». Lo fijan, en `tests/unit/test_sello_respaldo.py`, para el respaldo (empieza en
la vela siguiente): `test_la_marca_de_la_vela_del_llenado_no_se_toma`,
`test_un_llenado_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap_ni_cambia_de_dia` y
`test_un_llenado_del_respaldo_en_la_ultima_vela_de_una_sesion_es_de_la_siguiente`; y para lo que
no es del respaldo (como en `main`): `test_un_llenado_por_tick_en_el_ultimo_ms_de_un_minuto_conserva_su_minuto_y_su_sesion`,
`test_un_llenado_por_tick_en_el_ultimo_ms_antes_del_corte_paga_el_swap_y_es_de_ese_dia` y
`test_una_apertura_conocida_en_el_cierre_menos_1_ms_se_comporta_como_en_main`.

**Leen `abierta_ms` y no cambian, sin tocarlos** (revisor, segunda pasada, b1), con su porqué:

- `Broker._proximo_evento`, la salida (`desde = max(ahora − 1, abierta_ms, stop_movido_ms)` y
  `decidido = abierta_ms`): con la apertura en k fin − 1 ms, la vela del llenado sigue fuera de la
  salida (su sello no es posterior a `desde`), y la siguiente, k + 1, empieza después de
  `decidido`, así que `_nivel_de_la_vela` la evalúa con el stop de nacimiento, como antes;
- `Broker._mover` (`vigente_desde`, el instante desde el que vale el stop anterior): un instante, no
  un minuto; lo compara `_nivel_de_la_vela` con el inicio de una vela, y k fin − 1 ms sigue por
  debajo del inicio de k + 1;
- `Broker._marcar_hasta` → `_peor_del_minuto(lado, m, abierta_ms, hasta)`: el filtro de ticks
  `abierta_ms <= tick <= hasta`; sin ticks no se usa, y con ticks no cambia;
- el orden de las posiciones en `cableado._operaciones_del_bot` y en `detalle_para_visor`: solo
  ordena.

### 3. Los lectores de `cerrada_ms`: en el instante sellado

Una salida del respaldo (stop u objetivo) se sella también en k fin − 1 ms. Cada lector, con su
porqué:

- `Broker._cerrar` (`p.cerrada_ms = instante`): el instante sellado.
- La comisión del cierre (`Broker._operacion`): en el instante sellado, como la de la apertura.
- Los swaps hasta el cierre (`Broker._operacion`, `instante <= cerrada_ms`) y `_marcar_hasta(instante)`
  antes de cerrar: **no neutros**. Una posición que sale por la última vela antes de un corte sale
  ANTES del corte, y no paga su swap; con el sello en k fin lo pagaba, aunque la vela que la cerró
  acabara en el corte. Es lo correcto: la posición no vivió más allá de su vela. Lo fija un test
  (`test_una_salida_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap`), que rompe en `main`.
- Las marcas dentro de la operación (`abierta_ms <= ms <= cerrada_ms`): la marca de la vela k se toma
  en k fin − 1 ms y sigue dentro.
- El cierre de la `Operacion` y el visor (`cableado.py`, `detalle_para_visor`): el instante sellado.

### 4. Lo que el motor ve un cierre antes

El motor ve el evento del respaldo de la vela k en el cierre de k, no en el siguiente. Todo lo que
decide a partir de él llega un cierre antes:

- la orden siguiente se coloca un cierre antes (en la verificación de SELLO-RESPALDO-M1.md §7.3,
  2026-04-22, 04-23 y 08-20);
- **ADR-0083 D2** (`cableado.correr_dia`: `broker.avanzar(hasta_ms)` en `engine/cableado.py:305`,
  `_a_la_cuenta` en `:306` y `_el_punto_tras_el_evento` en `:308`, antes del intérprete): un
  rechazo al llenar gasta el punto, y un stop u objetivo sin ganancia libera la zona, en el cierre
  de k; la reentrada por D5 sale en ese mismo cierre;
- **D4** (RN-011, `operacion_abierta`): la posición abierta se ve en el cierre de k.

### 5. El fin del día y el borde de ADR-0068

Se aceptan. Las dos velas transcurren enteras antes de su borde:

- **el fin del día** (`cableado.correr_dia`, `fin_ms = ultimo · 60000 − 1`, `engine/cableado.py:356`): la última vela de la
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
  llenado (ADR-0051 §3, su NOTA), `Mercado.cotizacion`, el reloj del motor (ADR-0053). Con el sello en
  k fin − 1 ms = `ahora`, el «ahora − 1» deja que el `avanzar` siguiente vuelva a mirar la vela k
  para lo que no cambió en el cierre (una pendiente que no llenó, una posición cuyo stop no tocó):
  es la misma vela con el mismo nivel y el mismo `decidido`, y da lo mismo; lo que se decidió en
  el cierre (colocar, modificar, mover, llenar) lleva su instante en `desde` y la deja fuera. Lo
  fijan los tests de §1.
- Las líneas citadas de `engine/` son las del código con este ADR (`trabajo/sello-respaldo-m1`).
- **La repetición del trader sin ticks** (ADR-0051 §8) cambia otra vez: no se vuelve a correr.

## Fecha / fase

2026-11-07 · post-F14, `trabajo/sello-respaldo-m1` (R3.6).

## Estado
ACTIVE
