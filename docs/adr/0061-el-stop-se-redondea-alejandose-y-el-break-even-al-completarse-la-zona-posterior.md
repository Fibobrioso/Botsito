---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `trabajo/nocturno-01oct`, sesión nocturna)
---

# 0061 · El stop se redondea alejándose de la entrada, y el break even se pone al completarse la zona de control posterior

## Decision

### 1. La forma de RN-011 nombra `stop_fraccion_redondeo`, y el motor lo lee

El trader quiere que, cuando el 0,8 de la caja no cae en un punto exacto, el stop vaya hacia fuera
(`fb-2026-09-29-sesion-03-11910e0a`, `ev-v9-010541-0c80d5cf`). `trabajo/activar-sesion-03` creó el
parámetro `stop_fraccion_redondeo` = `alejandose_de_la_entrada`, pero el motor seguía redondeando
hacia la entrada con una línea de código (`ACTIVAR-SESION-03.md` §3, desalineación 5).

- La acción `escribir_stop_en_la_orden` gana el argumento `redondeo`, y la forma de RN-011 lo
  nombra (ADR-0019 §1: todo argumento de valor es un nombre del registro).
- Se redondea la **distancia** de la entrada al stop: con `alejandose_de_la_entrada`, hacia arriba
  al punto entero siguiente; con `hacia_la_entrada`, hacia abajo, que es lo que hacía el código.
- El lote sale de esa distancia (`lotaje_base` = `hasta_stop_fraccion`, ADR-0020), así que con el
  stop un punto más lejos el lote es un poco menor. El objetivo no cambia: sale de la caja completa.
- **Enmienda ADR-0029 §3 para el redondeo del stop.** El stop ya no se redondea al punto entero
  más cercano con el empate en contra del bot: su distancia a la entrada se redondea siempre
  alejándose de ella, como dice `stop_fraccion_redondeo`. ADR-0029 §3 sigue valiendo para el
  objetivo, y su §4 para el lote.

### 2. DECISIÓN NOCTURNA: «lo mínimo posible» es un punto, no un pip entero

El trader dijo «lo mínimo posible [...] si es un pip, un pip y ya está». Se lee como el mínimo
incremento del precio: un punto, la última cifra de la cotización. La otra lectura —redondear al pip
entero, diez puntos— alejaría el stop hasta nueve puntos más, con stops que miden 15 puntos de
mediana (`docs/validation/VIABILIDAD-TRADER.md` §2). Si el trader quiso decir pip entero, cambia la
regla de redondeo, no el parámetro. **Aceptada por el consultor el 2026-09-30, y queda además
como pregunta para la sesión 4 con el trader.**

### 3. El break even de RN-014 deja de ser un hueco

RN-014 pone el stop en la entrada cuando, tras la entrada, se desarrolla otra zona de control y el
precio la rompe; en la sesión 3 el trader lo confirmó «al tocar», mirado en M1 y con el stop
exactamente en la entrada (`fb-2026-09-29-sesion-03-9f506366`,
`fb-2026-09-29-sesion-03-2cff5008`). La forma ya lo decía; faltaba la primitiva de
`se_completa_zona_de_control`, que valía DESCONOCIDO.

- La primitiva se escribe **solo para el caso de RN-014**, el que lleva `posterior_a` la entrada de
  la posición viva. Vive en `engine/primitivas_broker.py`, porque necesita la posición del bróker.
- **Sin `posterior_a`** —la reubicación de la orden pendiente de RN-006— sigue NO_IMPLEMENTADA: es
  la vida de la orden stop, rama 3 de ADR-0056.
- La acción `mover_stop` ya existía en el cableado (ADR-0053 §1) y lleva el stop a la entrada.
  Después el stop no se vuelve a mover (A-40 RESUELTA): la primitiva da SÍ una sola vez, en el
  cierre de la M1 que completa la primera zona.

### 4. DECISIÓN NOCTURNA: qué es «la zona de control posterior» en M1

Ninguna fuente dibuja la zona posterior vela a vela. Se lee con la misma geometría de M1 que ya usa
el breaker (`domain/estructura_m1.py`, `domain/pivotes_m15.py`):

- tras la entrada, una vela **contraria** que sigue a una racha a favor deja el **punto extremo**
  —el punto alto en una compra— y abre el retroceso, que es la zona de control;
- la zona **se completa** cuando una M1 posterior **pasa** ese punto con
  `break_even_criterio_ruptura` (`mecha`): «rompe el punto alto anterior con mecha»
  (`fb-2026-09-09-sesion-01-a456bc3f`);
- manda el **último** punto formado; la mecha de la propia vela contraria no cuenta, porque el
  punto existe desde su cierre; igualar el punto no lo rompe;
- solo cuentan las M1 desde la que contiene el llenado: la zona es posterior a la entrada.

Código: `zona_posterior_completada`, pura, en `domain/estructura_m1.py`.

### 5. Lo que todavía no es «al tocar»

La estrategia se evalúa al cierre de M1 (ADR-0028), así que el stop se mueve en el cierre de la M1
que toca el punto, no en el tick. Es la misma limitación que ADR-0053 §2.1 deja para revisar con la
demo de MetaTrader. `break_even_condicion` (`tocar`) se lee y no cambia nada todavía.

### 6. Lo que NO se decide aquí

- **A-13 sigue ABIERTA** por el corte de audio de v9 0:57:00–0:58:06.
- **El redondeo del objetivo.** ADR-0029 dice que un nivel se redondea «al punto entero más
  cercano y, en empate, en contra del bot». El código del stop no hacía eso, sino redondear
  siempre hacia la entrada; ahora hace lo que dijo el trader, y para el stop ADR-0029 §3 queda
  enmendado (§1). El redondeo del objetivo no se toca.

## Problema que resuelve

`ACTIVAR-SESION-03.md` §3, desalineación 5: `stop_fraccion_redondeo` no lo leía nadie. Y §4: de las
20 diferencias grandes entre las operaciones anotadas y las simuladas, 5 se explican por el break
even al tocar, que el bróker simulado no podía reproducir porque la regla valía DESCONOCIDO.

## Alternativas consideradas

1. Leer `stop_fraccion_redondeo` dentro de la acción sin nombrarlo en la forma.
2. Nombrarlo en la forma de RN-011 como argumento de la acción (la elegida).
3. Redondear al pip entero.
4. Escribir `se_completa_zona_de_control` entero, también para RN-006.
5. Escribirlo solo para RN-014, con `posterior_a` (la elegida).
6. Mover el stop en el tick del toque, fuera del cierre de M1.

## Por que elegimos esta opcion

- La 2 es ADR-0019 §1: un valor que una acción lee se nombra en la forma, o las guardias que leen la
  lista de parámetros de la regla no lo ven.
- La 5 cierra lo que tiene fuente —el break even de la sesión 3— sin adelantar la vida de la orden
  stop, que tiene sus propias ambigüedades abiertas (A-29, A-48).

## Por que descartamos las demas

- La 1 deja una segunda puerta: la acción leería un parámetro que la regla no declara.
- La 3 no sale de la frase del trader, que pide lo mínimo.
- La 4 exige decidir qué es el posible punto de breaker y qué hace la orden con una caja nueva.
- La 6 rompe ADR-0028, que no se toca sin un ADR propio.

## Impacto

- **Código:** `engine/primitivas_broker.py` (`escribir_stop_en_la_orden` lee el redondeo;
  `se_completa_zona_de_control` para RN-014) y `domain/estructura_m1.py`
  (`zona_posterior_completada`).
- **Spec:** la acción `escribir_stop_en_la_orden` gana `redondeo`; la forma, el `entonces`, los
  parámetros y las notas de RN-011; la descripción de `stop_fraccion_redondeo`; las notas de RN-014 y
  del predicado `se_completa_zona_de_control`. `spec_version` **14.1.0 → 14.2.0**.
- **Tests:** en `tests/unit/test_cableado.py`, el redondeo con una caja de 21 puntos (el stop a 17 y
  el lote de esa distancia; con el otro valor del parámetro, a 16) y el break even de punta a punta;
  en `tests/unit/test_estructura_m1.py`, la zona posterior; y `tests/unit/test_preparar_a21.py`
  cambia a propósito: su caja de 16 puntos deja el stop a 13, no a 12.
- **Medido sobre construcción** (abril y agosto de 2026, 42 días `dev`), con `motor arnes --simular`
  y `scripts/embudo_77.py` antes y después, en DIAGNÓSTICO —A-35 `cierre_vela_contraria`, A-44
  `sin_tope`, A-21 `solo_una_zona_de_control`, A-27 con 0 puntos—, así que **ninguna cifra cuenta
  como medida de fidelidad**:
  - las operaciones del bot, la cobertura y la precisión no cambian: 8 puntuables, 2 de 77 y 2 de 8;
  - **RN-014 dispara en 3 sesiones de 84**, 2 de ellas con operaciones del trader;
  - los 16 eventos del bróker son los mismos; tres stops saltan un poco después, y el saldo final
    del tramo pasa de 95.605,67 a 96.253,00;
  - el embudo de las 77 da los mismos pasos (sesgo 15, liquidez 11, breaker 24, caja 22, bróker 2,
    llenado 1, coincide 2). Una orden cambia de motivo de rechazo: con el stop un punto más lejos el
    lote baja del máximo de la firma, y pasa de `volumen_max_lotes` a `precio_invalido`.
  - El arnés sin bróker no cambia: el redondeo y el break even son acciones del cableado.

## Fecha / fase

2026-09-30 · sesión nocturna, rama `trabajo/nocturno-01oct`. `PROJECT_STATE.md`, Next Action A3.c.

## Estado

ACTIVE (ACEPTADO por el consultor el 2026-09-30, con sus DECISIONES NOCTURNAS; revisión de
`feature/nocturno-01oct`, docs/validation/NOCTURNO-01OCT.md)
