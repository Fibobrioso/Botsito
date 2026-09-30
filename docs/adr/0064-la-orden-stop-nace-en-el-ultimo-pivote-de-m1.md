---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `feature/F35-orden-stop-pivote`, F35: la rama 3 de ADR-0056 con la caja por operación de la rama 4)
---

# 0064 · La orden stop nace en el último pivote de M1 y se reubica con cada pivote nuevo, con la caja de R6

> **ACEPTADO en su dirección** por el consultor el 2026-09-30, en el encargo de la rama. Los valores
> de los dos selectores nuevos quedan DEFAULT_AMBIGUOUS bajo A-48, y el de `orden_limite_nace` sigue
> DEFAULT_AMBIGUOUS bajo A-29: **nada se resuelve aquí**. Lo que el encargo y ADR-0056 §7 no deciden
> va marcado **DECISIÓN**, con la lectura más conservadora.

## Decision

### 1. El punto de nacimiento es un selector: `orden_stop_punto`

- **`ultimo_pivote_m1`** (el valor): el último pivote de M1 contrario al sentido de la entrada (un
  BAJO en una venta, un ALTO en una compra) formado con las M1 cerradas, con
  `pivotes_formados` y `CIERRE_VELA_CONTRARIA`. Es la función de R5 de
  `scripts/bloque_de_la_caja.py`, ahora `ultimo_punto_de_ruptura` en `domain/estructura_m1.py`.
  - Por qué: en `CAJA-77.md` §3.2 su 0 localiza la entrada del trader (36 de 77, frente a 18 con la
    entrada desplazada 5 puntos). En §3.3, en 56 de 77 ese pivote es uno de M1 formado DESPUÉS de la
    toma, y solo en 5 es la referencia del breaker del productor.
- **`referencia_de_la_toma`**: el pivote de `referencia_del_breaker` en la vela de la toma. Es lo que
  ADR-0056 §7 llamaba «hoy» el posible punto de breaker, y queda para poder comparar. **No se mueve**:
  la referencia de la toma no cambia después de la toma.
- DEFAULT_AMBIGUOUS bajo **A-48**, que pregunta por el punto y por el bloque (ADR-0056 §5 y §7).

### 2. La caja de cada orden: `caja_bloque`

- **El 0 es siempre el punto**, donde va la orden.
- **El 1 depende del bloque**, con las reglas de CAJA-77:
  - **`r6`** (el valor): la máxima (en una venta; la mínima en una compra) de las velas desde la que
    marca el nivel del pivote hasta la última M1 cerrada en el instante de colocar o reubicar;
  - **`r4`**: la del tramo de velas contrarias consecutivas que acaba en la última contraria;
  - **`r1`**: la de esa última contraria.
- `extremo_de_la_caja` en `domain/estructura_m1.py`.
- **Cada reubicación recalcula la caja, el stop y el lote**: la orden de un punto nuevo es una zona
  nueva, dimensionada de cero por RN-011.
- DEFAULT_AMBIGUOUS bajo **A-48**.
- **A-49** (la vela del bloque cerrada o en formación) no cambia: solo cuentan las M1 cerradas, que
  es su lectura `cerrada` y lo que exige ADR-0028.

### 3. El stop sigue su parámetro

`stop_fraccion_caja`, con su redondeo (ADR-0061), sobre la caja de §2. **A-18 sigue abierta y no se
toca.**

### 4. La vida de la orden, desde ADR-0056 §7

Corre con `orden_limite_nace` = **`al_aparecer_punto_de_breaker`**, la tercera lectura de A-29. Es
el valor nuevo del parámetro, que sigue DEFAULT_AMBIGUOUS. Con `al_darse_el_esquema` todo sale como
antes, byte a byte.

- **Nace tras la toma de la liquidez de su sesión** (ADR-0056 §7: «la orden nace en el punto tras la
  toma»), en el lado del sesgo, en cuanto hay punto y caja con altura. Se coloca como STOP (A-47)
  con el precio todavía al otro lado; si ya lo ha pasado, el bróker la rechaza (ADR-0057).
- **Se reubica cuando se forma un punto nuevo**. Es el mecanismo de RN-006 (ADR-0056 §7): en esta
  lectura, «se completa una zona de control» es «se forma un posible punto de breaker nuevo».
  - La orden se **cancela**, y RN-011 y RN-015 la vuelven a colocar en el mismo cierre de M1, en el
    punto nuevo.
  - Son dos peticiones al servidor, cancelar y colocar, como dice ADR-0056 §7 («se cancela y se
    vuelve a colocar»).
  - Con `referencia_de_la_toma` no hay reubicación.
- **Se llena al romper el punto**: es la entrada del esquema 1, sin retroceso (ADR-0056 §7). La zona
  lleva `por` = `primer_esquema`.
- **Se cancela al cerrar la ventana** si sigue sin llenar. Ya lo hacía el cableado (ADR-0053 §6).
- **RN-008 no frena la colocación** (ADR-0056 §7, que la dejaba PROVISIONAL para esta rama).
  - Su forma gana una condición, un predicado nuevo `la_orden_nace_antes_del_esquema` sobre
    `orden_limite_nace`, de fuente `motor`: con la orden en el punto, RN-008 no prohíbe.
  - La razón es la de ADR-0056 §7: RN-008 prohíbe ABRIR sin esquema, y la orden stop solo abre
    cuando el precio rompe el punto, que es el esquema 1.
  - Un test lo fija.

**DECISIONES** (lo que ni el encargo ni ADR-0056 §7 deciden; en cada una, la lectura más
conservadora):

1. **Un punto ya usado no se vuelve a colocar.** Usado es con la orden enviada, aceptada o
   rechazada. Si el precio ya pasó el punto al colocarla, se rechaza una vez y no se reintenta en
   cada M1, que llenaría el contador de peticiones (R13).
2. **Una sola vida de orden por sesión que llega a llenarse.** Tras un llenado, la sesión no coloca
   otra orden, como la zona de un solo uso que había antes. Los cartuchos siguen sin geometría.
3. **La orden pendiente de una sesión no se reubica con los puntos de la siguiente** (A-46: cada
   sesión es un escenario propio). Sigue viva hasta la ventana, el llenado o su propia reubicación.
   La siguiente sesión no coloca otra mientras esa esté pendiente, porque RN-011 lo exige. A-39 y
   A-30 siguen abiertas.
4. **RN-005 (el lado de ruido) se aplica a la zona del punto**, y RN-009 (más zonas de control que
   el tope) sigue en pie. Los dos pueden prohibir, y prohibir es lo conservador.
5. **La caja se fija la primera vez que se ve el punto.** Si un gate retrasa la colocación, la caja
   no se recalcula hasta el punto siguiente.
6. **La ventana de M1 es la del productor**: desde 240 minutos antes de la toma
   (`LOOKBACK_M1`). En CAJA-77 era de 90 antes de T. El último pivote es el mismo mientras esté
   dentro de las dos.

## Problema que resuelve

F35 estaba BLOQUEADA (`docs/nocturno/INFORME-01oct.md` §3) por dos cosas que ADR-0056 no decidía:
en qué precio nace la orden y con qué caja. `CAJA-77.md` las midió sobre las 77 operaciones de
construcción: el veredicto pre-registrado fue NO DECIDE, y la parte exploratoria apuntó al último
pivote de M1 y a R6. El consultor decidió la dirección con esa medida, sabiendo que es de
construcción.

## Alternativas consideradas

1. Esperar a la sesión 4 (A-48 y A-49).
2. Construir la vida con la referencia de la toma, que es lo que ADR-0056 llamaba el punto.
3. Construirla con el último pivote de M1 y la caja de R6, dejando las otras lecturas como opciones
   de dos selectores (la elegida).

## Por que elegimos esta opcion

Desbloquea F35 sin fijar A-48. Deja las lecturas que CAJA-77 midió como opciones comparables. Y
mantiene la línea base antigua intacta con `al_darse_el_esquema`.

## Por que descartamos las demas

- La 1 deja el bot sin igualar ninguna operación del trader hasta la sesión 4 (`NOCTURNO-01OCT.md`
  §2: cobertura 0 de 77).
- La 2 construye sobre un punto que la medida desmiente (`ORDEN-STOP-O-LIMITE.md` §4 y `CAJA-77.md`
  §3.3). Queda como opción para comparar.

## Impacto

- **Código:**
  - `domain/estructura_m1.py`: `ultimo_punto_de_ruptura`, `extremo_de_la_caja`, `PuntoDeRuptura`;
  - `engine/zonas.py`: `zona_del_punto`, `toca_colocar_orden_limite` con la tercera lectura,
    `la_orden_nace_antes_del_esquema` y RN-005 sobre la zona del punto;
  - `engine/primitivas_broker.py`: RN-006 con `se_completa_zona_de_control` sin `posterior_a`, la
    reubicación como cancelación y la sesión con llenado.
- **Spec:**
  - la forma de RN-008;
  - el predicado `la_orden_nace_antes_del_esquema`;
  - `orden_limite_nace` pasa a `al_aparecer_punto_de_breaker`, y nacen `orden_stop_punto` y
    `caja_bloque`, bajo A-48;
  - las notas de RN-006, RN-008 y RN-011 y las descripciones de los predicados;
  - `spec_version` sube a MAYOR, porque RN-008 cambia de sentido con la orden en el punto.
- **Enmienda ADR-0056 §7**:
  - «el posible punto de breaker es `referencia_del_breaker`» pasa a ser un selector con el último
    pivote de M1 como valor;
  - lo PROVISIONAL de RN-008 queda escrito.
- **Enmienda ADR-0055**: RN-011 coloca también fuera del cierre del breaker.
- **Medido** en `docs/validation/F35-ORDEN-STOP-PIVOTE.md`, en DIAGNÓSTICO: **no es fidelidad**,
  porque el criterio se eligió mirando construcción.

## Fecha / fase

2026-09-30 · rama `feature/F35-orden-stop-pivote` (F35). `PROJECT_STATE.md`, Next Action D.

## Estado

ACTIVE (ACEPTADO en su dirección por el consultor el 2026-09-30; valores DEFAULT_AMBIGUOUS bajo A-48 y A-29)
