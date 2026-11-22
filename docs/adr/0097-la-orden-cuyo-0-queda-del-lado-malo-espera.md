---
status: ACTIVE
date: 2026-11-22
phase: post-F14 (rama `trabajo/activar-sesion-08`, R4.3 de la hoja de ruta)
---

# 0097 · La orden cuyo 0 queda del lado malo espera (enmienda ADR-0083 D1 y la decisión 1 de ADR-0064)

> Decisión del consultor del 2026-11-21 (encargo de `trabajo/activar-sesion-08`, F2), escrita el
> 2026-11-22. Es **LECTURA DEL CONSULTOR**, bajo `orden_stop_lado_malo` = `espera`
> (DEFAULT_AMBIGUOUS) y **A-59, ABIERTA**: no cierra nada. **Enmienda ADR-0083 D1 y la decisión 1
> de ADR-0064** en un solo caso (recuadro en los dos y fila del índice).

## Decision

### 1. La regla

Cuando la orden stop no se puede colocar porque la cotización del cierre deja el 0 del lado malo
(una compra stop por debajo del ask, una venta stop por encima del bid; ADR-0057 §2), **no se
envía**: ninguna petición al bróker, **la caja no queda usada y el punto no se gasta**. Se envía en
el **primer cierre de M1 en que el 0 vigente quede del lado bueno**, y RN-006 la mueve si el punto
cambió.

**Todo lo demás que gasta un punto sigue como en ADR-0083 D1**: el rechazo al llenar, cualquier otro
motivo de rechazo al colocar (stops level, volumen, margen, y la negativa por un cierre de mercado o
por el freno, que el cableado trata como rechazo) y los «NO ENVÍA» que D1 ya tiene (el lote por
debajo del mínimo y `lote_si_no_cabe = no_operar` con un límite que muerde), que **sí** gastan el
punto. Este es un no envío distinto: la traza (`ContextoDia.esperas`), el informe del arnés (la
sección «### Esperas») y `motor decisiones` («orden NO enviada … el 0 queda del lado malo; espera»
y, al enviarse, «enviada tras esperar desde …») lo nombran aparte de los no envíos de ADR-0081.

**El orden con los otros motivos (decisión de implementación de esta rama, declarada; la regla del
consultor no lo dice):** la comprobación del lado malo va DESPUÉS del lote de ADR-0081 (si el lote no
cabe, no se envía y el punto se gasta, aunque el 0 esté del lado malo) y ANTES de enviar. Así que, si
a la vez el 0 queda del lado malo y la orden caería en otro motivo de rechazo al colocar, los que el
bróker mira antes que el precio (el cierre de mercado de ADR-0068, el corte o el bucle del freno de
ADR-0067, el volumen y las órdenes simultáneas) o después (stops level, margen), **manda el lado
malo**: no se envía, espera y no gasta el punto. Esos otros motivos gastan el punto cuando el 0 está
del lado bueno.

**Aceptado por el consultor tal como está** (respuesta del 2026-11-22 a la PARADA final de
`trabajo/activar-sesion-08`, punto 8a): mientras espera no se envía nada; cuando el 0 pasa al lado
bueno la orden se envía, y si en ese momento sigue vigente el cierre de mercado, el freno o el
margen, el bróker la rechaza y el punto se gasta; si ya no, entra, como entraría cualquier orden
colocada en ese momento. Cambia cuándo se gasta el punto, no si se gasta.

Solo vale para la orden STOP en la ruptura (A-47); la límite de las líneas base antiguas no cambia.
Con `orden_stop_lado_malo` = `se_gasta_el_punto` todo es como antes de este ADR.

### 2. Lo que dijo el trader y lo que es lectura del consultor

**Dicho:**
- Sesión 6 (2026-11-04, S-19): que la orden se pone igual, «ya a mí me habilita»
  (`ev-v17-014103-8cf3e7fb`), y que, con la stop order y el precio por encima, el nivel de la caja
  se va actualizando (`ev-v17-014235-f3375358`, `ev-v17-014350-ec133d13`).
- Sesión 7b (2026-11-20, S-6): la opción «otra» de la hoja, inclinándose por la (b): «inclinaría
  más que nada que espero que el cero quede al lado bueno y entonces la pongo»
  (`ev-v20-010243-21636d5f`); y, a «¿Y si el precio vuelve por debajo del 0 antes de que pongas la
  orden?», que la orden tiene que estar a nivel y, si sube o retrocede, «solo toca esperar»
  (`ev-v20-010354-ada60dca`). Lo dijo inclinándose, no como regla; la extracción lo da «en parte»,
  sin regla general clara y sin decir si vale en compra y en venta (`SESION-08-EXTRACCION.md`
  §3.6).

**Lectura del consultor** (encargo, F2, con estas palabras): «no cierro nada. Cambio un
comportamiento de ejecución que las dos sesiones contradicen y lo dejo como LECTURA DEL CONSULTOR,
bajo un parámetro DEFAULT_AMBIGUOUS y una ambigüedad nueva que queda ABIERTA, como se hizo con
ADR-0084 y ADR-0094». En lo único en que las dos sesiones coinciden es en que ese punto no se
pierde; esperar en vez de entrar es la inclinación de la 7b. Es la opción (b) de
`docs/sesion-7/PREGUNTAS-7B.md` (S-6) y los puntos 3 y 4, opción (a), de «Lo que necesito que
decidas» de `ACTIVAR-SESION-06-MOTOR.md` (que el consultor dejó escrita el 2026-11-06: «si el trader
dice "espero", 3.a y 4.a»). Desviación declarada por el consultor de «en parte no se cierra» y de
«solo se activan las reglas generales» (R4.6): no se cierra; se cambia la ejecución por defecto.

### 3. Por qué no se reenvía en cada cierre

La decisión 1 de ADR-0064 no reintentaba un rechazo «en cada M1, que llenaría el contador de
peticiones (R13)». Según la respuesta de FTMO del 2026-10-05 (recuadro de
`docs/validation/FTMO-REGLAS.md`, preguntas 1 a 3) todo tipo de orden cuenta para el límite de
2.000 peticiones al día, sin distinguir las rechazadas; la del 2026-11-20 (paráfrasis del consultor
en `docs/validation/ACTIVAR-SESION-08.md`) no dice nada de las rechazadas. Así que la orden no se
reenvía para que la rechace el bróker: **se comprueba antes de enviarla**, y mientras no vale no
hay petición.

### 4. Qué vela mira la comprobación

La del bróker, sin copiarla: `Broker.lado_equivocado_al_colocar` (`engine/broker.py`), que es la
misma `Mercado.cotizacion` y la misma `lado_equivocado` con las que `_precio_infringido` rechaza
(ADR-0057 §4). En el cierre de la M1 k el instante es `k·60000 − 1`: con ticks, el último tick
anterior o igual a ese instante; **sin ticks, la última M1 cerrada antes del instante, que es la
k−1**, no la k que acaba de cerrar. Es la deuda «Las cotizaciones sin tick del bróker no usan la
misma vela» (Technical Debt): este ADR no la resuelve, y la comprobación y el rechazo miran siempre
lo mismo.

### 5. Qué cambia de ADR-0083 D1 y de la decisión 1 de ADR-0064

- ADR-0083 D1, primer guion de «Gasta el punto» («la orden que el bróker RECHAZA al colocar (precio
  inválido, …)»): con `espera`, la stop del lado malo ya no llega al bróker, y por tanto el precio
  inválido al colocar deja de gastar el punto. Los demás motivos de rechazo al colocar, el rechazo
  al llenar y los no envíos de D1, sin cambios. D1 sigue PROVISIONAL.
- ADR-0064, decisión 1 («Si el precio ya pasó el punto al colocarla, se rechaza una vez y no se
  reintenta en cada M1»): con `espera`, no se envía; tampoco se reintenta en cada M1 (no hay
  petición), y se envía una vez, cuando vale.

### 6. Cómo lo hace el código, y los tests

- `engine/primitivas_broker.py`, `colocar_orden_limite`: después del lote (ADR-0081) y antes de
  enviar, si la orden es stop, `orden_stop_lado_malo` = `espera` y
  `Broker.lado_equivocado_al_colocar(...)`, no envía, no marca la zona usada ni el punto gastado y
  apunta la espera una vez por punto y sesión (`ContextoDia.esperas`, `espera_abierta`); al enviarse
  después la orden de ese punto, la espera lleva su id. RN-011 y RN-015 vuelven a preparar la orden
  en cada cierre, porque `toca_colocar_orden_limite` sigue viendo el punto sin gastar.
- `engine/zonas.py`, `punto_de_la_zona`; `engine/cableado.py`, la sección del informe;
  `engine/decisiones.py`, las líneas de la bitácora.
- Tests (`tests/unit/test_orden_lado_malo.py`): en compra y en venta, el precio vuelve y la orden se
  coloca en el primer cierre en que vale; no vuelve y no hay ni orden ni petición; con
  `se_gasta_el_punto`, lo de antes; la comprobación y el rechazo miran lo mismo; y el 2026-07-08 de
  11 a 15 por el camino real. Los que congelaban el rechazo que gasta el punto cambian de sentido a
  propósito (`test_punto_usado.py`, `test_cableado.py`; `test_vida_de_la_orden.py` pasa a la opción
  `se_gasta_el_punto`).

## Problema que resuelve

Las dos sesiones dicen que ese punto no se pierde, y el bot hacía lo contrario: la stop del lado
malo se enviaba, el bróker la rechazaba por precio inválido y el rechazo gastaba el punto (ADR-0083
D1). En la corrida de julio de la base, 5 órdenes rechazadas por precio inválido al colocar, en 3
sesiones (`ACTIVAR-SESION-08.md`, 0.5).

## Alternativas consideradas

1. **Dejarlo como estaba** (el rechazo gasta el punto): la opción `se_gasta_el_punto`.
2. **Reenviar en cada cierre** y dejar que el bróker la rechace, sin gastar caja ni punto (la (b)
   de la decisión 3 de ACTIVAR-SESION-06-MOTOR.md).
3. **No enviar mientras el 0 esté del lado malo**, sin gastar caja ni punto, y enviar en el primer
   cierre en que valga (la elegida).
4. **Mover el 0** a los nuevos altos y poner la orden ahí (la (d) de S-6, que sostienen las citas de
   la sesión 6).

## Por que elegimos esta opcion

Es la que se inclina a decir el trader en la 7b y la que el consultor dejó escrita para ese caso el
2026-11-06; no gasta peticiones; y deja intacto todo lo demás de ADR-0083.

## Por que descartamos las demas

- (1) Contradice lo único en que las dos sesiones coinciden: el punto no se pierde. Queda como
  opción del parámetro.
- (2) Una petición rechazada por minuto mientras dure. FTMO dijo el 2026-10-05 que todo tipo de
  orden cuenta para el límite, sin distinguir las rechazadas, y no ha dicho si una rechazada cuenta
  (A-54 sigue sin esa respuesta); el freno de ADR-0067 sí las cuenta.
- (4) El trader contestó «otra» inclinándose por esperar, no por mover el 0; y mover el 0 es otra
  regla de dónde va el 0, que es A-48 (F1 de la misma rama, en la PARADA).

## Impacto

- `knowledge/spec/parametros.yaml`: `orden_stop_lado_malo` (estrategia, enum, DEFAULT_AMBIGUOUS en
  `espera` bajo A-59); `knowledge/spec/ambiguedades.yaml`: A-59, pregunta, no bloqueante, ABIERTA;
  `knowledge/spec/strategy_spec.yaml`: la descripción de `toca_colocar_orden_limite`; `spec_version`
  19.1.0, `spec manifest --escribir` y `spec docs --escribir`.
- Recuadros en ADR-0083 (§1) y ADR-0064 (decisión 1), y las filas del índice.
- `PROJECT_STATE.md`: A-59 en Known Ambiguities.
- La corrida de julio tras F2, con su delta y las filas declaradas, en `ACTIVAR-SESION-08.md`.
- Las láminas (`engine/laminas.py`) no enseñan la espera: leen los no envíos de ADR-0081 y no esta
  lista. Lo dice el informe de la rama.

## Fecha / fase

2026-11-22; post-F14, rama `trabajo/activar-sesion-08` (R4.3).

## Estado

ACTIVE (LECTURA DEL CONSULTOR bajo A-59, ABIERTA; `orden_stop_lado_malo` DEFAULT_AMBIGUOUS en
`espera`; enmienda ADR-0083 D1 y la decisión 1 de ADR-0064, con recuadros)
