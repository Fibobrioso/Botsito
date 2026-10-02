---
status: ACTIVE
date: 2026-10-02
phase: post-F14 (rama `feature/freno-peticiones`, la K de Next Action)
---

# 0067 · El freno de peticiones vive en el puerto del broker: aviso, corte y bucle, y lo que protege la cuenta pasa siempre

> **PROVISIONAL en sus cuatro umbrales**, DEFAULT_AMBIGUOUS bajo A-54: son un margen del proyecto,
> no una cifra de FTMO, y se revisan cuando la demo diga qué cuenta como «server request». Es una
> tarea autónoma: el consultor no lo ha revisado todavía.

## Decision

### 1. Dónde vive

En el puerto. Las peticiones salen solo por cinco métodos del broker: `_colocar`, `modificar`,
`cancelar`, `cerrar_a_mercado` y `_mover`. Cada uno pregunta al freno (`engine/freno.py`) antes de
apuntar la petición. Las reglas de la estrategia (RN-002, RN-004, RN-006, RN-014, RN-015, RN-030 y
RN-035) llaman a acciones, que llaman al broker: ninguna puede saltarse el freno. El freno no tiene
IO ni reloj propio, y el adaptador real de MetaTrader usará la misma clase.

### 2. Tres umbrales, en el registro

Los cuatro parámetros son de categoría `ejecucion`, DEFAULT_AMBIGUOUS bajo A-54:
- `freno_peticiones_aviso` = 1000: se apunta y no frena;
- `freno_peticiones_corte` = 1500: desde ahí, ese día solo sale lo que protege la cuenta;
- `freno_bucle_repeticiones` = 5 dentro de `freno_bucle_minutos` = 1: tantas peticiones IGUALES
  (el mismo contenido, sin el id) cortan el envío el resto del día.

El corte va por debajo de `firma_mensajes_dia_max` (2.000), y el broker se niega a armarse si no.
El margen hasta el límite es para lo que protege la cuenta.

### 3. Lo que protege la cuenta pasa siempre, y cuenta

Pasan siempre:
- cancelar una pendiente;
- cerrar a mercado;
- mover el stop de una posición viva hacia el lado que reduce el riesgo (el break even, RN-014 y
  ADR-0065).

Cuentan para el límite, porque FTMO no dice que no sean «server requests». Una petición NEGADA no
llega al servidor y no se cuenta. Colocar y modificar una pendiente negadas devuelven un `Rechazo`
con motivo `freno_corte` o `freno_bucle`. Un stop hacia fuera negado deja la posición como estaba.

### 4. Nunca deja una posición sin stop

El stop viaja en la orden (A-11). El freno niega crear o mover, nunca quita: lo único que puede
negar sobre una posición es alejar su stop, y entonces conserva el que tenía.

### 5. El día es el de la firma

Cambia a medianoche en `firma_huso_corte`, el mismo reloj del día de riesgo (ADR-0027), no el de
las sesiones (ADR-0063). Con el día nuevo todo vuelve a cero, también un corte por bucle.

### 6. Todo queda escrito

Cada aviso y cada petición negada, con su motivo:
- en `Traza.cortes`;
- en el log (`logging`, WARNING);
- en el informe del arnés, «El freno de peticiones».

### 7. Sin umbrales, el límite de la firma

Si quien arma el broker no trae los umbrales del registro, el broker frena igual en
`mensajes_dia_max` (el límite de la firma), sin margen ni aviso. `reglas_broker_de(perfil,
registro)` los lee cuando se le pasa el registro, y el cableado siempre se lo pasa.

## Problema que resuelve

R13 de `docs/validation/FTMO-REGLAS.md` prohíbe «more than 2,000 server requests per day». El bot
las contaba y nada frenaba: `feature/escenarios-por-sesion` midió que siete reglas envían
peticiones y que el código, por sí solo, no garantiza el tope (Next Action K).

## Alternativas consideradas

- **Frenar en las reglas** (un gate de la spec): una regla nueva o una acción olvidada se lo
  saltaría. El encargo lo pide en el puerto.
- **Frenar también lo que protege**: dejaría la cuenta peor que pasarse del límite.
- **No contar lo que protege**: FTMO no lo dice, y la lectura estricta corta antes.
- **Bucle como peticiones consecutivas**: la reubicación alterna cancelar y colocar, y un bucle de
  reubicación no se vería nunca.

## Por que elegimos esta opcion

Es la única que cumple «pase lo que pase en el código que lo llama». Además no cambia nada de un
día normal: el más cargado medido son 13 peticiones, y el aviso está en 1000.

## Por que descartamos las demas

Ver «Alternativas consideradas».

## Impacto

- **Código**:
  - `engine/freno.py` (nuevo);
  - `engine/broker.py` (`ReglasBroker.freno`, el freno en los cinco métodos, `Traza.cortes`);
  - `engine/simulacion.py` (`limites_freno_de`, `reglas_broker_de(perfil, registro)`);
  - `engine/cableado.py` (lo pasa y lo informa).
- **Spec**: cuatro parámetros `ejecucion`, DEFAULT_AMBIGUOUS bajo A-54.
- **Tests**:
  - `tests/unit/test_freno_peticiones.py`;
  - `tests/unit/test_peticiones.py` cambia el test que fijaba que nada frenaba.
- Medido en `docs/validation/FRENO-PETICIONES.md`.

## Fecha / fase

2026-10-02 · rama `feature/freno-peticiones`. `PROJECT_STATE.md`, Next Action K.

## Estado

ACTIVE (PROVISIONAL en `freno_peticiones_aviso`, `freno_peticiones_corte`,
`freno_bucle_repeticiones` y `freno_bucle_minutos`: se revisan con A-54, en la demo de FTMO)
