# El bróker simulado: órdenes stop y rechazo de pendientes mal colocadas

Rama `trabajo/broker-ordenes-stop`, 2026-09-28, desde `main` en `stable/F21-blindar-make-check`
(`08769c3`). Es la rama 1 de código de ADR-0056 §8. **Solo toca el bróker simulado**: la estrategia
no cambia, el selector de A-47 no existe todavía y RN-011 sigue colocando órdenes límite. Las
decisiones que ADR-0056 no cubría están en ADR-0057, todas PROVISIONALES hasta la demo de FTMO.
Solo construcción: abril y agosto de 2026, por la compuerta del arnés.

## 0. Lo que deja la rama, en cinco líneas

- **El bróker sabe colocar y llenar una orden STOP de entrada**: salta al tocar el nivel y se llena
  al precio del tick que la dispara; con hueco, peor que el nivel, y el deslizamiento queda en la
  posición.
- **Una pendiente del lado equivocado del precio se rechaza** (`precio_invalido`), también al
  modificarla. Ya no se llena a su propio precio.
- **El stops level del bróker es `firma_stops_level_puntos`, UNKNOWN en el perfil de FTMO** (A-27).
  Sin él, una orden stop no se coloca; con `--diagnostico-a27`, corre etiquetada.
- **La línea base de las límites NO sale byte a byte idéntica**, y no se tapa (§3): cambia en las
  órdenes que se colocaban del lado equivocado y, en cascada, en los días que RN-032 bloqueaba.
- **Dieciséis tests nuevos**, uno de ellos de punta a punta por el arnés real con una orden stop.

## 1. Fase 0 · Cómo estaba el bróker, leído y medido sobre `main`

- **Resolución de precios.** Ticks de Dukascopy donde los hay, con su BID y su ASK reales; donde
  falta una hora de ticks, la vela M1 BID de respaldo, que solo sirve para depurar y la salida
  marca (ADR-0051 §8). `engine/llenado.py`, `Mercado`.
- **Spread.** Con ticks, el de cada tick: una compra mira el ASK y una venta el BID (ADR-0051 §1).
  Con respaldo M1, un spread supuesto por hora local, el percentil 90 medido
  (`knowledge/simulador/llenado.yaml`, DN-4): el ASK es el BID de la vela más ese spread.
- **Misma vela.** Con ticks manda el orden real: gana el primer tick que cumple, y si el mismo tick
  cumple stop y objetivo, el stop (DN-2). Con respaldo M1, pesimista: el stop antes que el
  objetivo, todo sellado al cierre de la vela, y la salida de una posición no se mira en la vela en
  la que se llenó, sino desde la siguiente.
- **Límites del lado equivocado, medido.** Misma corrida que la línea base (`motor arnes
  --simular` en diagnóstico, A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21 cada lectura),
  con la cotización del último tick anterior a colocar:

| lectura de A-21 | órdenes del bot | del lado equivocado | en el nivel | sin ticks al colocar |
|---|---|---|---|---|
| `solo_una_zona_de_control` | 15 | 3 | 1 | 1 |
| `sin_mecha_mas_alla_del_extremo` | 12 | 4 | 0 | 1 |
| distintas entre las dos | 16 | 4 | 1 | 1 |

  Las cuatro del lado equivocado se llenaron a su propio precio y las cuatro cerraron por stop:
  −8, −18, −30 y −23 puntos. Es la misma medida que `ORDEN-STOP-O-LIMITE.md` §8 («cruzadas»).

## 2. Fases 1 y 2 · Lo que se hizo

**La orden stop** (`llenado.primer_llenado_stop`, `Broker.colocar_stop`). Una venta stop salta
cuando el BID toca o baja del nivel; una compra stop, cuando el ASK lo toca o lo sube. Se llena al
precio de ese tick más el deslizamiento fijo de la configuración (DN-3, hoy 0). Si el tick llega ya
pasado el nivel, a ese precio, nunca al nivel, y `Posicion.deslizamiento_entrada` guarda los puntos
en contra (en una límite, siempre 0). Con respaldo M1, al nivel o a la apertura si la vela abre
pasada, sellado al cierre: la misma convención que el stop de una posición y, para la vela del
llenado, que la límite.

**El rechazo** (`llenado.lado_equivocado`, `Mercado.cotizacion`, `Broker._precio_infringido`).
Con la cotización del momento, el último tick o, sin ticks, la última M1 cerrada: una límite de
venta por debajo del BID, una de compra por encima del ASK, una stop de venta por encima del BID y
una de compra por debajo del ASK se rechazan con `precio_invalido`. El nivel exacto pasa. Una
modificación que cruza se rechaza y la orden sigue como estaba.

**El stops level** (`firma_stops_level_puntos` en `knowledge/cuentas/ftmo-2step-swing-100k.yaml`,
UNKNOWN, R11, A-27). No es `instrumento_stops_level`, el de la estrategia (RN-026, DEFAULT 0 de
otra firma): ponerlo en UNKNOWN habría cambiado la estrategia. Sin valor, el bróker se niega a
colocar una stop y lo dice nombrando A-27; una límite no se juzga por stops level, como hoy. Con
`--diagnostico-a27 <puntos>` (solo con `--simular`) corre etiquetado `DIAGNOSTICO-A27-<puntos>`;
con el valor fijado en el perfil, el diagnóstico se rechaza. Con valor, la pendiente, su stop y su
objetivo tienen que estar a esa distancia como mínimo, o se rechaza con `stops_level`.

## 3. La línea base de las límites: lo que cambia, caso a caso

Misma corrida en `main` y en la rama, sobre la misma máquina y los mismos datos, las dos lecturas
de A-21. **No sale idéntica.** Cambian dos clases de casos.

**a) Directos: órdenes que en `main` se colocaban del lado equivocado y se llenaban a su precio;
ahora se rechazan con `precio_invalido`.**

| día | orden | contra el precio al colocar | en `main` | lecturas |
|---|---|---|---|---|
| 2026-04-23 | venta límite 1.16994 | 6 puntos (sin ticks: última M1 cerrada, 04:59Z, cierre 1.17000) | llenada por respaldo M1, stop, −10 | las dos |
| 2026-04-27 | compra límite 1.17268 | 5 puntos | llenada, stop, −8 | las dos |
| 2026-08-03 | venta límite 1.15363 | 14 puntos | llenada, stop, −18 | las dos |
| 2026-08-04 | venta límite 1.15085 | 28 puntos | llenada, stop, −30 | las dos |
| 2026-08-20 | compra límite 1.16981 | 16 puntos | llenada, stop, −23 | solo `sin_mecha…` |

El del 23 de abril no estaba en la cuenta de la Fase 0, que solo miraba ticks: se juzga con la
última M1 cerrada (ADR-0057 §4), y se señala por eso.

**b) En cascada: días en que en `main` RN-032 prohibía abrir y ahora no.** RN-032 es la lectura
prospectiva de la firma, «no abrir lo que no cabe» antes del límite de pérdida (ADR-0026, ADR-0031).
En `main` disparaba en 29 de 84 sesiones con la primera lectura y en 15 de 84 con la segunda; en
la rama, en ninguna. Hasta el primer día en cascada, la única diferencia entre las dos corridas son
los casos directos, así que lo que la apaga es que faltan sus pérdidas: con ellas, el saldo de
`main` acaba en unos 90 760, cerca del límite total de la firma. Sin RN-032, RN-011 y RN-015
colocan órdenes que antes no llegaban a colocarse:

| día | orden | qué le pasa ahora | lecturas |
|---|---|---|---|
| 2026-08-18 | venta límite 1.15782 | rechazada por el perfil: `volumen_max_lotes` | solo `solo_una…` |
| 2026-08-20 | compra límite 1.16981 | rechazada: `precio_invalido` | solo `solo_una…` |
| 2026-08-24 | venta límite 1.16673 | llenada con ticks, stop, −5 | las dos |
| 2026-08-26 | venta límite 1.16656 | rechazada: `precio_invalido`, 4 puntos | las dos |
| 2026-08-27 | compra límite 1.16535 | rechazada por el perfil: `volumen_max_lotes` | las dos |

**El efecto agregado:**

| | `solo_una…`, `main` | `solo_una…`, rama | `sin_mecha…`, `main` | `sin_mecha…`, rama |
|---|---|---|---|---|
| operaciones del bot | 9 | 6 | 9 | 5 |
| puntuables contra el trader | 7 | 4 | 7 | 3 |
| precisión | 1/7 | 1/4 | 1/7 | 1/3 |
| rechazos del bróker | 2 | 10 | 0 | 7 |
| saldo final | 90 759,08 | 94 269,02 | 90 776,36 | 95 269,22 |
| días de trading | 9 | 6 | 9 | 5 |
| sesiones con RN-032 | 29 de 84 | 0 | 15 de 84 | 0 |

El resto del informe del arnés (embudo, reglas por sesión, avisos H3, eventos) cambia solo en las
líneas de esos días, y la precisión sube porque desaparecen operaciones que no casaban con el
trader. **Ninguna operación del bot ganó**: todas las que quedan siguen cerrando por stop, como en
`main`. Es un cambio correcto del bróker, no de la estrategia, y lo revisa el consultor.

## 4. Fase 3 · Tests

`tests/unit/test_broker_ordenes_stop.py`, catorce tests sobre ticks y velas sintéticos de 2030:
venta y compra stop al toque; hueco al precio del tick con el deslizamiento guardado, y con el
deslizamiento fijo; la límite no desliza; respaldo M1 al nivel y a la apertura; misma vela, igual
para límite y stop, y con ticks el orden real; los cuatro mal colocados rechazados y nunca
llenados; los bien colocados y el nivel exacto aceptados; la cotización sin ticks; la modificación
que cruza; el stops level sin valor, en diagnóstico y ya fijado; y la etiqueta de A-27 y la CLI.

`tests/unit/test_cableado.py`, dos nuevos. **De punta a punta por `arnes.correr` con la spec real**:
RN-011 y RN-015 dimensionan y colocan, la acción de colocar se desvía en el test a la orden stop del
bróker, el ASK toca la entrada y la compra se llena al nivel, y cierra por objetivo con ganancia. Y
sin stops level, la misma corrida se niega nombrando A-27. Además se actualizó el test que congela
los parámetros sin valor del perfil de FTMO.

**Un test existente dependía del llenado falso, y se dice.** En `tests/unit/test_simulacion.py`,
la estrategia sintética que pierde siempre colocaba su venta límite al último cierre más 3 puntos,
POR DEBAJO del BID de ese instante: una límite cruzada, que el bróker llenaba al instante a su
propio precio. Con el rechazo, esa orden no entra y el test (la cuenta acaba suspendida) fallaba.
Se corrige la estrategia del test, no el bróker: la venta va 15 puntos por encima del cierre, por
encima del BID, espera a que la tendencia alcista la llene y el stop salta igual que antes.

## 5. Estado

Código, tests, ADR-0057 y este informe en un solo commit sellado. Queda para el consultor la
revisión del cambio de la línea base (§3) y las decisiones provisionales de ADR-0057. Sigue
pendiente medir en la demo de FTMO lo que hace MT5 de verdad. **Rama lista para revisión, NO
cerrada.**
