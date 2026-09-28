---
status: ACTIVE
date: 2026-09-28
phase: post-F14 (rama `trabajo/selector-orden-stop`)
---

# 0058 · El selector de A-47 en la rama 2: la orden stop en el instante de la límite, para medirla

> **PROVISIONAL.** Escrito en la rama `trabajo/selector-orden-stop`, la rama 2 de código de
> ADR-0056 §8, con lo que ni ADR-0056 ni ADR-0057 fijaban o que el brief del consultor cambió. La
> decisión 2 ENMIENDA a ADR-0056 §1 y a su fila 2 de §8, que dejaban `stop_en_ruptura` en
> NO_IMPLEMENTADA hasta la rama 3: el consultor pidió medirla en esta rama. Todo se revisa en la
> rama 3, cuando exista el instante propio de la orden stop. A-47 sigue ABIERTA y
> `entrada_tipo_orden` UNKNOWN.

## Decision

### 1. Los nombres son los de ADR-0056

El brief pedía `tipo_orden_entrada` con `limite | stop`; ADR-0056 §1, aceptado, fija
`entrada_tipo_orden` con `stop_en_ruptura | limite_en_retroceso`, y el mismo brief pide aplicarlo
«tal como lo define ese ADR». Se usan los de ADR-0056. El parámetro vive en
`knowledge/spec/parametros.yaml`, `estrategia`, `enum`, UNKNOWN, y A-47 lo cita.

### 2. Con `stop_en_ruptura`, la orden stop va donde y cuando iría la límite

Al mismo precio, el 0 de la caja (`Zona.entrada`, el borde del bloque más cercano al precio), en
el mismo instante, el cierre del breaker, con el mismo stop, objetivo y lote de RN-011 y RN-015. Lo
único que cambia es el tipo con que llega al bróker (`colocar_stop`). El instante propio de una
orden stop, el POSIBLE punto de breaker antes de la ruptura (ADR-0056 §7, la tercera lectura de
A-29), es la rama 3 y no existe todavía. Consecuencia que ADR-0056 §1.3 ya anticipaba y la medida
confirma (`docs/validation/SELECTOR-ORDEN-STOP.md`): en el cierre del breaker el precio suele haber
roto ya, y la orden stop queda del lado equivocado y el bróker la rechaza (ADR-0057).

### 3. El selector solo se exige con el bróker simulado

El tipo de orden solo existe en el bróker. Con `--simular`, sin el valor fijado ni
`--diagnostico-a47`, el arnés y el visor se niegan nombrando A-47 y antes de leer una vela, como
ADR-0054. Sin `--simular` no cambia nada, y `--diagnostico-a47` sin `--simular` es un error. Un
motor cableado construido sin tipo (los tests con estrategia sintética) coloca límites, lo de
siempre.

### 4. El bloque y el momento son los de hoy

A-48 (el bloque) y A-49 (el momento) no tienen todavía selector: nacen en la rama 4 de ADR-0056.
No hay, pues, lectura diagnóstica vigente que usar; la caja es la que traza hoy el productor (la
última vela contraria, velas cerradas) y no se fija nada.

### 5. La etiqueta y el stops level de la medida

`DIAGNOSTICO-A47-<lectura>`, detrás de la de A-21 y delante de la de A-27. La medida de la rama
usa `--diagnostico-a27 0`, el valor medido en la otra firma que es el DEFAULT de
`instrumento_stops_level`: con él, el stops level no rechaza nada y lo que se mide es el tipo de
orden. No es un valor de FTMO.

## Problema que resuelve

ADR-0056 dejaba `stop_en_ruptura` sin comportamiento hasta la rama 3, y el consultor pidió medir
ya lo que pasa con órdenes stop en construcción. Sin estas decisiones, la rama 2 no podía darle
esa medida ni decir por qué sale como sale.

## Alternativas consideradas

1. Seguir ADR-0056 al pie: `stop_en_ruptura` NO_IMPLEMENTADA, y la tabla de la medida vacía.
2. Colocar la stop en el instante de la límite (la elegida), sabiendo que el precio ya rompió.
3. Adelantar aquí el instante propio de la stop, el posible punto de breaker: es la rama 3 entera.

## Por que elegimos esta opcion

Es la única que da una medida real en esta rama sin inventar una pieza que tiene su rama propia.
Y la medida dice algo útil aunque salga mal: cuantifica cuánto importa el instante.

## Por que descartamos las demas

- La 1 no mide nada, y el consultor pidió la medida.
- La 3 adelanta sin su revisión de diseño la pieza más delicada, la vida de la orden stop
  (ADR-0056 §7), con dos lecturas PROVISIONALES encima.

## Impacto

- `knowledge/spec/parametros.yaml` (el selector), `knowledge/spec/ambiguedades.yaml` (A-47 lo
  cita), `knowledge/cases/kit/mapa_parametros.yaml`, spec 13.4.0.
- `engine/entrada.py` (la lectura y la negativa), `engine/diagnostico.py` (A-47),
  `engine/primitivas_broker.py` (la acción que coloca elige el tipo), `engine/cableado.py` y la CLI.
- Con `limite_en_retroceso`, la corrida de construcción sale idéntica a la de `main`, salvo la
  cabecera y las etiquetas del diagnóstico.

## Fecha / fase

2026-09-28 · post-F14, rama `trabajo/selector-orden-stop`, rama 2 de código de ADR-0056.

## Estado

ACTIVE
