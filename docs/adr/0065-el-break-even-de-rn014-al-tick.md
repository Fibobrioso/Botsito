---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `feature/be-al-tick`, Next Action G: RN-014, break even al tick)
---

# 0065 · El break even de RN-014 se pone al tick que pasa el nivel, no al cierre de la M1

> **PROVISIONAL.** Las decisiones marcadas **DECISIÓN** son las que el encargo y ningún ADR
> anterior cubrían. Se escriben con la lectura más conservadora y se revisan con la demo de
> MetaTrader (ADR-0053 §2.1), que es la que dirá cómo tarda una petición `modificar` de verdad.

## Decision

### 1. El instante: el primer tick cuyo BID pasa el nivel

- RN-014 cita la corrección de la sesión 3 (`fb-2026-09-29-sesion-03-9f506366`, «apenas toca,
  pues se pone en B la entrada»), y la sesión 1 ya lo había dicho a la pregunta del instante
  (`ev-v6-005701-7ae2b8d3`: «apenas toca»). `break_even_condicion` vale `tocar` (CONFIRMED).
- Hasta esta rama el motor evaluaba la estrategia al cierre de M1 (ADR-0028) y movía el stop en el
  cierre de la M1 que pasa el punto (ADR-0053 §2.1, ADR-0061 §5). **Ahora el stop pasa a la entrada
  en el primer tick cuyo BID pasa el nivel de activación.**
- **El nivel no cambia**: es el mismo punto extremo que mira `zona_posterior_completada`, sacado
  del mismo recorrido (`nivel_de_activacion_posterior`, `domain/estructura_m1.py`). Con el criterio
  `mecha` (`break_even_criterio_ruptura`, CONFIRMED), pasar el nivel es que el BID quede
  estrictamente por encima en una compra y por debajo en una venta: la mecha de una M1 BID vista
  tick a tick. **El precio tampoco cambia**: el stop va a la entrada exacta, como hoy.

### 2. Cómo llega el nivel al bróker

- En cada cierre de M1, con la posición abierta, el predicado de RN-014 calcula el nivel vigente y
  lo deja en el contexto, sin tocar el bróker ni el estado (ADR-0055 §1).
- El cableado, después de evaluar las reglas, lo arma en el bróker (`vigilar_break_even`) si
  `break_even_condicion` es `tocar`. Así el instante lo sigue diciendo el parámetro que la forma
  de RN-014 nombra en `mover_stop` (`cuando: break_even_condicion`).
- El bróker mira los ticks posteriores. **DECISIÓN: vigilar no es una petición al servidor.** El
  bot mira el precio en local; la petición es mover el stop, una `modificar` de R13 que el contador
  suma en el instante del tick.

### 3. Lo que manda en el mismo tick

**DECISIÓN:**
- Si un mismo tick llena, salta el stop vigente o el objetivo y además pasa el nivel, primero va lo
  que el servidor hace con lo que ya hay, y después se mueve el stop.
- El stop nuevo cuenta **desde el tick siguiente**, nunca en el tick que lo movió. Es la misma
  regla de todo el modelo de llenado: un evento no se evalúa contra el tick en el que se decidió
  (ADR-0051).
- Así, un tick que pasa el objetivo y el nivel cierra por objetivo. Y si el nivel quedó por debajo
  de la entrada en una compra (la racha a favor no llegó a ella), el stop movido salta en el tick
  siguiente, al precio de ese tick.

### 4. El break even y el stop original en el mismo tick

**DECISIÓN:**
- **Con ticks no puede pasar.** El nivel queda del lado del objetivo y el stop original del otro, y
  un mismo BID no puede pasar los dos.
- **Con el respaldo M1 sí puede pasar**: una M1 que pasa el nivel y toca el stop original. Ahí manda
  lo de siempre (ADR-0051 §3): **el stop primero**, pesimista, y no hay break even.

### 5. Lo que se queda al cierre de la M1, y queda marcado

- **Sin ticks** (modo `--depuracion`, o un minuto sin ticks) no hay instante al tick. El break even
  se pone al cierre de la M1, como antes, y la traza lo marca: evento `stop_movido` con fuente
  `respaldo_m1`.
- **Con `break_even_condicion` = `cierre`, o con el criterio `cuerpo`** (un cuerpo no se ve en un
  tick), también al cierre de la M1. Ahí la fuente es `cierre_m1` si el minuto tiene ticks.
- **DECISIÓN: el cierre de la M1 no repite la petición.** Si el stop ya se movió al tick, RN-014 lo
  vuelve a pedir al cierre de esa M1 y el bróker no hace nada: ni petición ni evento.

## Problema que resuelve

El trader pone el break even «apenas toca», y el motor lo ponía al cierre de la M1. Una M1 que pasa
el punto y vuelve al stop original antes de cerrar salía por el stop entero, y él habría salido a la
entrada.

## Alternativas consideradas

- **Dejarlo al cierre de la M1**: es lo que cambia el encargo.
- **Mirar el ASK en una venta**: el nivel sale de velas BID. Comparar el ASK cambiaría el nivel en
  el spread, y el encargo dice que el nivel no cambia.
- **Aplicar el stop nuevo en el mismo tick**: supondría una petición sin latencia y contradiría la
  convención del modelo de llenado.

## Por que elegimos esta opcion

Cambia solo el instante, que es lo que dijo el trader, y deja el nivel, el precio y el modelo de
llenado como estaban.

## Por que descartamos las demas

Ver «Alternativas consideradas».

## Impacto

- **Código:**
  - `domain/estructura_m1.py`: `nivel_de_activacion_posterior`;
  - `engine/llenado.py`: `primer_toque_al_tick`;
  - `engine/broker.py`: `vigilar_break_even`, el evento `stop_movido`, el desempate y `mover_stop`
    idempotente;
  - `engine/primitivas_broker.py` y `engine/cableado.py`.
- **Tests:**
  - `tests/unit/test_be_al_tick.py` (nuevo);
  - `test_rn014_pone_el_stop_en_la_entrada_al_completarse_la_zona_posterior` cambia a propósito:
    la traza lleva `stop_movido` al tick.
- **No cambia ningún valor de la spec ni de su forma.**
- **Medido en diagnóstico** en `docs/validation/BE-AL-TICK.md`.

## Fecha / fase

2026-09-30 · rama `feature/be-al-tick`. `PROJECT_STATE.md`, Next Action G.

## Estado

ACTIVE (PROVISIONAL: se revisa con la demo de MetaTrader, ADR-0053 §2.1)
