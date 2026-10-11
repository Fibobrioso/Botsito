---
status: ACTIVE
date: 2026-10-11
phase: post-F14 (rama `trabajo/activar-sesion-04`, R1.1 de la hoja de ruta)
---

# 0074 · El 1 de la caja de la orden stop se recalcula en cada cierre de M1 hasta el llenado: `caja_se_fija` = `en_cada_cierre_m1` (enmienda la decisión 5 de ADR-0064)

> Decisión del consultor del 2026-10-11 (respuesta a la PARADA de `trabajo/activar-sesion-04`,
> punto 2). **Enmienda la DECISIÓN 5 de ADR-0064** (recuadro allí y fila del índice). Lo dijo el
> trader en la sesión 4, S-4.

## Decision

### 1. El valor

`caja_se_fija` pasa de `al_verse_el_punto` a `en_cada_cierre_m1`: con la orden sin llenar, el 1 de
la caja se recalcula en cada cierre de M1 con las velas desde el pivote hasta la última cerrada
(`caja_bloque`, hoy R6), y cada 1 nuevo es una zona nueva del mismo punto que RN-006 reubica con su
stop y su lote. El 0 y el punto no se mueven; la distancia al máximo nuevo no importa; un punto cuya
orden se rechazó no se vuelve a colocar con otra caja (decisión 1 de ADR-0064). Es lo que el trader
describió en S-4 (v10 0:49:45–0:51:28, sobre un esquema inventado): «Ahora, si ocurre una vela
verde, otra vela verde Pues simplemente lo vamos actualizando la caja Mientras no se desarrolle otro
punto breaker» (`ev-v10-004945-59ebac47`); la distancia da igual (`ev-v10-005056-1a55d5b4`); en una
compra, lo mismo con un mínimo nuevo (`ev-v10-005116-2a9ff066`). Que el stop y el lote se recalculan
con el 1 lo dijo en S-3 (0:37:27, «si uno mueve el stop pues va a cambiar el lote»). El mecanismo ya
existía como sensibilidad de la decisión 5 (ADR-0064 §5; `engine/zonas.py`, `zona_del_punto`) y está
medido en `docs/validation/F35-ORDEN-STOP-PIVOTE.md` §4.3.

### 2. Cómo entra en el registro, y con qué estado

El cambio se hace a mano con fuente `decision: ADR-0074`: `caja_se_fija` es de categoría `ejecucion`
y `feedback apply` no escribe un parámetro de esa categoría (ADR-0004; `feedback/aplicar.py`). El
estado se queda en **DEFAULT_AMBIGUOUS bajo A-49**: es el único que el registro admite con
`ambiguedad_id` (`config/registro.py`: `ambiguedad_id` solo con DEFAULT_AMBIGUOUS), y
`tests/contract/test_provisional_cuelga_de_abierta.py` exige que esa ambigüedad esté ABIERTA, que
es el caso: A-49 (la caja con la vela cerrada o en formación) sigue ABIERTA, porque S-1 y S-2 la
dejan «en parte» y van a la sesión 5. Si A-49 se cierra, el estado pasa a CONFIRMED con esta misma
fuente, como `reloj_sesiones` con ADR-0069. El testimonio de S-4 se registra sobre A-49 sin
cerrarla; la forma de ese registro es la PARADA 2 del informe.

### 3. La cota de peticiones, con un test sintético

Con el 1 expandiéndose, cada cierre de M1 que sube el 1 cuesta dos peticiones (cancelar y colocar,
ADR-0056 §7): la cota es 2 × (M1 que mueven el 1 mientras la orden sigue sin llenar) por vida de
orden, menos una (la primera colocación no cancela nada). El freno de bucles de ADR-0067 no se
dispara, porque cada colocación lleva otro precio, otro stop y otro lote, y «igual» es la misma
firma sin el id (`engine/freno.py`); el corte del día cuenta el total como cualquier otra petición.
Lo fija `tests/unit/test_caja_hasta_el_llenado.py`: con velas que suben el máximo, una zona distinta
del mismo punto por cada máximo nuevo, y todas las peticiones admitidas sin ningún corte, frente al
mismo número de colocaciones iguales, que sí lo dispara. ADR-0067 midió sus umbrales con la lectura
de antes; en `F35-ORDEN-STOP-PIVOTE.md` §4.3, en DIAGNÓSTICO, esta lectura dio hasta 14 peticiones
al día y 59 en 42 días (frente a 7 y 35), lejos del límite. La medida real es la corrida de R3.1;
aquí no corre el arnés.

### 4. Lo que no cambia

`caja_bloque` (R6, DEFAULT_AMBIGUOUS bajo A-48), `orden_stop_punto`, la decisión 1 de ADR-0064 y la
vida de la orden (ADR-0066). A-49 sigue ABIERTA.

## Problema que resuelve

La decisión 5 de ADR-0064 era «la lectura más conservadora» de algo que el trader no había dicho, y
su sensibilidad se midió sin cambiar el valor (§5). El trader lo dijo en la sesión 4.

## Alternativas consideradas

1. Activar `en_cada_cierre_m1` por decisión, con A-49 abierta (la elegida).
2. Nada hasta la sesión 5.

## Por que elegimos esta opcion

El mecanismo existe, está medido y el trader lo describió sin dudar.

## Por que descartamos las demas

La 2 deja al bot fijando la caja al verse el punto, que no es lo suyo.

## Impacto

- `knowledge/spec/parametros.yaml`: `caja_se_fija` = `en_cada_cierre_m1`, fuente ADR-0074.
- `docs/adr/0064-*.md`: recuadro en la decisión 5; `docs/adr/README.md`: «ACTIVE (con enmienda de
  ADR-0074)».
- `tests/unit/test_caja_hasta_el_llenado.py`: el valor del registro (falla en `main`) y la cota;
  `tests/unit/test_orden_stop_pivote.py` cambia de sentido a propósito en lo que daba por fija la
  caja.
- `spec_version` sube un parche: cambia un valor.

## Fecha / fase

2026-10-11 · rama `trabajo/activar-sesion-04` (R1.1). Informe: `docs/validation/ACTIVAR-SESION-04.md`.

## Estado

ACTIVE
