# El selector del tipo de orden de entrada (A-47) y RN-011 con órdenes stop

Rama `trabajo/selector-orden-stop`, 2026-09-28, desde `main` en `stable/F22-broker-ordenes-stop`
(`ced3afc`). Es la rama 2 de código de ADR-0056 §8. Las decisiones que ni ADR-0056 ni ADR-0057
fijaban están en ADR-0058, todas PROVISIONALES. A-47 sigue ABIERTA y el selector, UNKNOWN. Solo
construcción: abril y agosto de 2026, por la compuerta del arnés.

## 0. Fase 0 · Qué cambia en la estrategia con el selector en stop

1. **La entrada va al bróker como orden STOP** del lado de la ruptura (venta stop por debajo del
   bid, compra stop por encima del ask) en el 0 de la caja, en vez de una límite que espera el
   retroceso: se entra cuando el precio rompe, no cuando vuelve.
2. **El stop, el objetivo y el lote no cambian**: RN-011 y RN-015 los calculan igual (el 0,8 de la
   caja, el 1:3 sobre la caja, el lote hasta el stop).
3. **El instante es el de hoy, el cierre del breaker** (ADR-0058 §2). El instante propio de la
   stop, el posible punto de breaker antes de la ruptura, es la rama 3; por eso muchas stops nacen
   con el precio ya roto y el bróker las rechaza.
4. **Depende de A-48**, qué velas forman el bloque, porque eso fija el 0 de la caja, que es el
   precio de la orden. Hoy, la última vela contraria.
5. **Depende de A-49**, vela cerrada o en formación, porque eso fija desde cuándo puede existir la
   orden. Hoy, velas cerradas. Ninguna de las dos tiene selector todavía (rama 4).

**Dos choques del brief con ADR-0056, resueltos en ADR-0058:** los nombres son los de ADR-0056
(`entrada_tipo_orden`, `stop_en_ruptura` y `limite_en_retroceso`), y la stop no queda
NO_IMPLEMENTADA como decía ADR-0056 §1, sino colocada en el instante de la límite, para poder medir.

## 1. Fase 1 · Lo que se hizo

- **El selector** `entrada_tipo_orden` en `knowledge/spec/parametros.yaml`, `enum`, UNKNOWN, con
  las dos lecturas; A-47 lo cita; entrada en `mapa_parametros.yaml`; spec 13.4.0.
- **`engine/entrada.py`**: la lectura del registro o del diagnóstico y la negativa que nombra A-47.
  Con el valor fijado, el diagnóstico se rechaza.
- **`--diagnostico-a47 <lectura>`**, solo con `--simular`, etiquetado `DIAGNOSTICO-A47-<lectura>`.
  Con `--simular` y sin él, el arnés y el visor se niegan antes de leer una vela.
- **La acción que coloca** (`primitivas_broker.colocar_orden_limite`) llama a `colocar_stop` con
  `stop_en_ruptura` y a `colocar_limite` con `limite_en_retroceso` o sin selector.

## 2. La línea base de las límites: idéntica

Misma corrida de construcción que en `main` (diagnóstico A-35 `cierre_vela_contraria`, A-44
`sin_tope`), con `--diagnostico-a47 limite_en_retroceso`: **sale idéntica byte a byte a la de
`main`**, con las dos lecturas de A-21, una vez quitadas la cabecera y las etiquetas del
diagnóstico, que son lo único que la bandera añade.

## 3. Fase 2 · La medición

Construcción en diagnóstico, con `--diagnostico-a27 0` (el stops level medido en la otra firma, que
es el DEFAULT de `instrumento_stops_level`; no es un valor de FTMO). Una coincidencia es una
operación del bot a no más de 3 puntos y 15 minutos de una del trader (ADR-0043,
`tolerancia_entrada_puntos: 3`, `tolerancia_instante_min: 15`). No se ajustó nada.

| | límite, `solo_una…` (`main`) | límite, `sin_mecha…` (`main`) | stop, `solo_una…` | stop, `sin_mecha…` |
|---|---|---|---|---|
| órdenes colocadas | 20 | 15 | 20 | 15 |
| operaciones del bot | 6 | 5 | 6 | 5 |
| en días con operaciones del trader | 4 | 3 | 6 | 5 |
| coincidencias con las 77 del trader | 1 | 1 | 2 | 2 |
| cobertura | 1/77 | 1/77 | 2/77 | 2/77 |
| precisión | 1/4 | 1/3 | 2/6 | 2/5 |
| en el mismo minuto que el trader | 0 | 0 | 1 | 1 |
| cierran por stop | 6 | 5 | 4 | 4 |
| cierran por objetivo | 0 | 0 | 2 | 1 |
| rechazos: lado equivocado | 6 | 6 | 9 | 8 |
| rechazos: volumen máximo | 4 | 1 | 4 | 1 |
| sesiones con RN-032 | 0 | 0 | 0 | 0 |
| saldo final | 94 269,02 | 95 269,22 | 97 611,09 | 96 216,02 |
| deslizamiento de entrada | ninguno | ninguno | 1 punto en una | 1 punto en una |

**Lo que dice, sin afirmar más.**
- **Con stop se llenan casi exactamente las órdenes que, como límites, nacían cruzadas.** En el
  cierre del breaker el precio ya había pasado el nivel: una límite ahí estaba del lado
  equivocado y ahora se rechaza, y una stop ahí está bien colocada y se llena en los ticks
  siguientes. Las límites que esperaban el retroceso son, como stops, del lado equivocado, y casi
  todas se rechazan. **El tipo de orden invierte qué órdenes sobreviven.**
- **Dos cierres por objetivo, con la primera lectura, y uno con la segunda**, frente a ninguno con
  límites. Las cifras son pequeñas: seis y cinco operaciones.
- **Una de las stops se llenó por el respaldo M1**, en una hora sin ticks del 23 de abril, igual
  que su límite en `main`. El respaldo solo sirve para depurar (ADR-0051 §8) y la corrida no lo
  excluye; se señala.
- **Nada de esto es la entrada del trader**: el instante sigue siendo el de la límite (ADR-0058 §2).
  La medida que importa llega con la rama 3.

## 4. Fase 3 · Tests

- `tests/unit/test_selector_orden_stop.py`, seis: el selector en el registro, sin valor y con sus
  dos lecturas; la negativa sin fijar ni diagnóstico, que nombra A-47; el rechazo del diagnóstico
  con el valor fijado; la etiqueta y su orden; la CLI que exige `--simular`; y la CLI con
  `--simular` y sin A-47, que se niega antes de escribir nada.
- `tests/unit/test_cableado.py`, tres: **RN-011 con el selector en stop, de punta a punta por
  `arnes.correr`**, sin desviar nada, con una operación completa llenada al romper y cerrada por
  objetivo; con el selector en límite, el informe sale idéntico al de sin selector; y con stop y el
  precio ya roto en el cierre del breaker, la orden se rechaza por lado equivocado.

## 5. Una aclaración sobre ADR-0057 §4, pedida por el consultor

Cuando una pendiente se coloca sin ninguna cotización anterior, ni tick ni M1 cerrada, **no se
juzga y se acepta**. **En construcción no pasa ninguna vez**: medido sobre `main` en las dos
lecturas de A-21, las 20 órdenes distintas tienen cotización. Por eso la salida no lleva etiqueta
para ese caso; si alguna vez pasara, habría que añadirla.

## 6. Estado

Código, spec, tests, ADR-0058 y este informe en un solo commit sellado. **Rama lista para revisión,
NO cerrada.**
