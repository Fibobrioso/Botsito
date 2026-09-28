# Orden STOP o LÍMITE: cómo se llenó cada entrada del trader en construcción

Rama `trabajo/orden-stop-o-limite`, 2026-09-27, tarea autónoma sobre `main` en
`stable/F19-sesion-02-videos`. Sin merge, sin tag, sin push. **Mide una hipótesis y no la adopta**:
A-47 sigue ABIERTA, y ni el motor, ni el productor de `engine/zonas.py`, ni RN-011, ni ningún
parámetro, regla, ambigüedad, evidencia o registro cambian. Salida completa, operación por operación:
`ORDEN-STOP-O-LIMITE-SALIDA.txt`, generada por `scripts/orden_stop_o_limite.py`.

**La hipótesis.** En v7 y v8 casi todas las órdenes del trader aparecen en FX Replay como `Sell stop`
o `Buy stop` (38 stop frente a 1 limit legibles, `SESION-02-VIDEO-V8.md` §4), y A-47 pregunta si
entra al romper el punto de breaker o al volver a él. Todo el motor asume una orden límite que espera
el retroceso a la zona (RN-011), y en `VERIFICACION-A21.md` la entrada del trader cae dentro de la
zona del motor en 6 de 77 operaciones (7 con la tolerancia de ADR-0043), casi siempre «fuera por el
lado del precio». Si entrara con una orden stop en el punto del breaker, eso lo explicaría.

## 0. Lo que la medida dice, en cuatro líneas

1. **Las 77 entradas de construcción se llenaron con el precio llegando desde el lado de la
   ruptura**: 77 STOP, 0 LÍMITE, 0 ambiguas (§2). El resultado no depende de las elecciones del
   criterio: con otro precio, otra tolerancia y otra ventana sale lo mismo en 25 de 27 variantes,
   y en las otras dos hay 1 y 2 LÍMITE (§2.3).
2. **El método no contradice ninguna etiqueta de FX Replay**: en las 10 parejas de v7 y v8 con el
   libro, las 7 etiquetas legibles son stop y las 7 se clasifican STOP (§3). Pero **no puede
   discriminar**, porque no hay ninguna pareja con etiqueta limit contra la que probarlo.
3. **La entrada NO está en el nivel de referencia del breaker que calcula hoy el productor**:
   en 2 de 39 operaciones con zona viva queda a ≤ 3 puntos de `Esquema.referencia`, y la distancia
   va de −305 a +153 puntos, con mediana −15 (§4). Es tan lejos como la zona.
4. **Lo que sostiene y lo que no** (§5): sostiene que el trader entra a favor del movimiento,
   nunca en el retroceso; **no** sostiene que entre en el punto que el productor llama breaker.
5. **Añadido en la revisión del consultor (§7)**: el control positivo sobre la única orden límite
   real salió **AMBIGUO**, así que, por la regla fijada, el 77 de 77 NO queda sostenido por él y la
   rama no se cierra. Los controles sintéticos sí pasan.
6. **Añadido en la segunda revisión del consultor (§8 y §9)**: ese control quedó como no informativo
   (la orden se colocó con el precio en el nivel). El que lo sustituye, con llenados límite reales
   del simulador, da **STOP en 3 de 8 (lectura a) y 4 de 8 (b)**: el método no distingue una límite
   colocada con el precio ya al otro lado de una stop. **No queda validado.** Ninguna límite en espera
   sale STOP.

## 1. El criterio de la Fase 2, escrito antes de medir

Copiado tal cual de `scratchpad/criterio_fase2.md`, redactado y guardado antes de correr nada. **No se
ha cambiado después**; lo que se añadió después de ver el resultado está marcado como tal en §2.2 y
§2.3 y no toca el criterio.

- **Nivel L** = `entrada` del caso (`entryPrice` del libro, F14a), en puntos (escala 100 000).
- **Instante t** = `instante_utc` del caso, que es el LLENADO (`INSTANTE-LLENADO-SALIDA.txt`:
  93 de 94 al minuto).
- **Fuente primaria**: los ticks de Dukascopy del día (`eurusd-ticks-2026-04-1d189bdd` y
  `eurusd-ticks-2026-08-75bd3a08`, 05:00–14:00 UTC), obligatorios si existen (ADR-0051). Precio del
  tick que llena: **bid para una venta, ask para una compra**, el lado con el que un broker ejecuta
  cada una.
- **Tolerancia τ** = 2 puntos, el `margen_puntos` de `knowledge/corpus/criterio_huso.yaml` (A-16:
  OANDA y Dukascopy difieren 1–2 puntos). Un tick «está en el nivel» si |p − L| ≤ τ; «por encima» si
  p > L + τ; «por debajo» si p < L − τ.
- **Husos, fijados antes de comparar**: el caso está en UTC (`instante_utc`, con el huso del libro
  medido por velas, ADR-0039); los ticks están en UTC (`ts_utc`, Dukascopy). No hay conversión. El
  gráfico de FX Replay (UTC+2 fijo) no entra en esta fase; entra en la Fase 3, donde la hora de
  pantalla se convierte restando dos horas.
- **Regla con ticks.** (1) Ventana W1 = [t − 60 s, t]; el último tick de W1 que NO está en el nivel
  fija el lado de llegada: por encima → «llega de ARRIBA»; por debajo → «llega de ABAJO». (2) Si en
  W1 hay ticks por encima Y por debajo → **ambiguo**. (3) Si ningún tick de W1 está fuera del nivel,
  se amplía a W2 = [t − 300 s, t]; si tampoco → «sin datos». (4) Sin ticks en [t − 300 s, t + 60 s] →
  M1. (5) Venta que llega de ARRIBA → STOP; de ABAJO → LÍMITE. Compra que llega de ABAJO → STOP; de
  ARRIBA → LÍMITE.
- **Regla con M1** (solo sin ticks): la vela anterior a la que contiene t; lado = el de su `cierre`
  respecto a L con la misma τ; si el cierre está en el nivel, su `abierta`; si también, ambiguo. Va en
  tabla aparte.
- **Lo que el criterio NO decide**: no dice qué tipo de orden había en la plataforma; dice desde qué
  lado llegó el precio. Por eso la Fase 3 lo contrasta con las etiquetas de FX Replay.

Por qué el lado de llegada distingue los dos tipos: una **sell limit** solo puede estar por encima del
mercado y se llena cuando el precio SUBE hasta ella; una **sell stop** solo puede estar por debajo y se
llena cuando el precio BAJA hasta ella. Con una compra, al revés. Si el precio llega a L desde arriba
en una venta, esa venta no pudo llenarse como límite, salvo que la orden se colocara con el precio ya
en L.

## 2. Fase 2 · Cómo se llenó cada entrada

Conjunto: los 42 días de construcción (abril y agosto de 2026, `knowledge/cases/dev`), comprobados
contra `casos_ocultos(repo)` antes de leer nada (34 ocultos, ninguno de esos meses). 77 operaciones:
35 de abril y 42 de agosto; 32 compras y 45 ventas. Ticks presentes en 75; en 2 no (las dos ventas
del 23 de abril, a las 05:30 y 05:53 UTC: la hora `2026-04-23T05Z` está en `horas.perdidas` del
manifiesto de ticks) y se clasificaron con M1.

### 2.1 Resultado

| mes | fuente | STOP | LÍMITE | ambiguo | sin datos | total |
|---|---|---|---|---|---|---|
| 2026-04 | ticks | 33 | 0 | 0 | 0 | 33 |
| 2026-04 | M1 | 2 | 0 | 0 | 0 | 2 |
| 2026-08 | ticks | 42 | 0 | 0 | 0 | 42 |
| **total** | ticks | **75** | 0 | 0 | 0 | 75 |
| **total** | M1 | **2** | 0 | 0 | 0 | 2 |
| compra | todas | 32 | 0 | 0 | 0 | 32 |
| venta | todas | 45 | 0 | 0 | 0 | 45 |

Las 75 con ticks se decidieron con la ventana de 60 s; ninguna necesitó la de 300 s. La tabla por
operación (día, sesión, hora UTC, dirección, entrada, tipo, lado, fuente, ventana, ticks en 60 s) está
en la salida.

### 2.2 Diagnóstico, añadido después de ver el 77 de 77 (no cambia el criterio)

Un resultado unánime obliga a mirar si el instante del libro lo fuerza. Sobre las 75 con ticks:

- **El precio en t está en el nivel**: p(t) − L va de −16 a +11 puntos, mediana 0; |p(t) − L| ≤ 2 en
  39 y ≤ 5 en 67. El instante del caso es el llenado, como decía `INSTANTE-LLENADO-SALIDA.txt`.
- **El nivel se toca mucho antes de t**: el primer tick en el nivel dentro de [t − 300 s, t + 60 s]
  está de mediana 261 s antes de t (mínimo −299, máximo +5); solo en 9 de 75 el primer toque cae a
  ≤ 5 s de t. El precio ronda el nivel varios minutos antes del llenado, y el criterio decide por el
  ÚLTIMO tick fuera del nivel, no por el primero.
- **A qué lado está el precio 60 s antes, por dirección**: ventas, encima 38 · en 5 · debajo 0;
  compras, encima 0 · en 3 · debajo 29. Ni una venta con el precio por debajo ni una compra con el
  precio por encima un minuto antes del llenado.

### 2.3 Robustez, añadida después (el criterio es la fila «bid/ask · 2 · 60 s»)

| precio | tol | ventana | STOP | LÍMITE | ambiguo | sin dato |
|---|---|---|---|---|---|---|
| bid/ask | 0 | 10 s | 63 | 0 | 6 | 6 |
| bid/ask | 0 | 60 s | 59 | 0 | 16 | 0 |
| bid/ask | 0 | 300 s | 23 | 0 | 52 | 0 |
| bid/ask | 2 | 10 s | 58 | 0 | 0 | 17 |
| **bid/ask** | **2** | **60 s** | **73** | **0** | **0** | **2** |
| bid/ask | 2 | 300 s | 46 | 0 | 29 | 0 |
| bid/ask | 5 | 10 s | 27 | 0 | 0 | 48 |
| bid/ask | 5 | 60 s | 65 | 0 | 0 | 10 |
| bid/ask | 5 | 300 s | 51 | 2 | 22 | 0 |
| mid | 0 | 10 s | 68 | 0 | 1 | 6 |
| mid | 0 | 60 s | 74 | 0 | 1 | 0 |
| mid | 0 | 300 s | 43 | 0 | 32 | 0 |
| mid | 2 | 10 s | 69 | 0 | 0 | 6 |
| mid | 2 | 60 s | 75 | 0 | 0 | 0 |
| mid | 2 | 300 s | 49 | 0 | 26 | 0 |
| mid | 5 | 10 s | 40 | 0 | 0 | 35 |
| mid | 5 | 60 s | 70 | 0 | 0 | 5 |
| mid | 5 | 300 s | 53 | 1 | 21 | 0 |
| ask/bid (al revés) | 0 | 10 s | 69 | 0 | 0 | 6 |
| ask/bid (al revés) | 0 | 60 s | 75 | 0 | 0 | 0 |
| ask/bid (al revés) | 0 | 300 s | 48 | 0 | 27 | 0 |
| ask/bid (al revés) | 2 | 10 s | 69 | 0 | 0 | 6 |
| ask/bid (al revés) | 2 | 60 s | 75 | 0 | 0 | 0 |
| ask/bid (al revés) | 2 | 300 s | 51 | 0 | 24 | 0 |
| ask/bid (al revés) | 5 | 10 s | 56 | 0 | 0 | 19 |
| ask/bid (al revés) | 5 | 60 s | 74 | 0 | 0 | 1 |
| ask/bid (al revés) | 5 | 300 s | 57 | 0 | 18 | 0 |

(La fila del criterio da 73 y no 75 porque esta tabla no amplía a 300 s cuando la de 60 s no tiene
ningún tick fuera del nivel: esas 2 quedan «sin dato» aquí y STOP en §2.1.) **Ninguna combinación
produce más de 2 LÍMITE**, y las dos que los producen usan tolerancia 5 con ventana de 300 s. Lo que sí
mueve la ventana larga es el número de ambiguas: con 300 s el precio cruza el nivel por los dos lados
en 22–52 operaciones, que es la misma consolidación previa que el diagnóstico mide. El lado de la
ÚLTIMA aproximación es siempre el de la ruptura.

Dos trazas para leerlas a mano (segundos respecto a t, bid/ask menos L en puntos), en la salida: la
venta del 2026-08-03 a las 06:03:05 UTC baja de +14 a 0 en 90 s y cruza; la compra del 2026-08-10 a
las 11:57:15 UTC sube de −5 a 0 y sigue hasta +11.

## 3. Fase 3 · El método frente a las etiquetas de FX Replay

Las 10 parejas de v7 y v8 con el libro (ADR-0043), sin las DUDOSAS: 8 de v7 (`SESION-02-VIDEO.md`
§4) y 2 de v8 (`SESION-02-VIDEO-V8.md` §4). Para cada una, la etiqueta leída en los fotogramas que
esos informes ya citan (reabiertos por instante localizado; ninguno nuevo) y la clasificación de la
Fase 2 de la fila del libro. Hora de pantalla en UTC+2; la del caso, en UTC.

| pareja | caso (UTC, dir., entrada) | vídeo | fotograma | etiqueta leída | Fase 2 | ¿coincide? |
|---|---|---|---|---|---|---|
| v7-2 | 08-03 06:03:05 venta 1.15364 | v7 n.º 2 | 000404000 | `Sell stop` (TP·SL·-244->Sell stop en 1.15364) | STOP | sí |
| v7-3 | 08-03 06:07:40 venta 1.15362 | v7 n.º 3 | 000499000 | no legible (posición ya abierta, caja 0 = 1.15361) | STOP | — |
| v7-5 | 08-03 09:46:15 venta 1.15274 | v7 n.º 5 | 000955000 | no legible (posición ya abierta; etiquetas 297 en 1.15287 y 1.15274) | STOP | — |
| v7-8 | 08-03 12:03:25 venta 1.15320 | v7 n.º 8 | 001365000 | `Sell stop` (156->Sell stop en 1.15320) | STOP | sí |
| v7-11 | 08-04 11:34:50 venta 1.15184 | v7 n.º 11 | 002070000 | `Sell stop` (191->Sell stop en 1.15184) | STOP | sí |
| v7-15 | 08-06 06:07:25 venta 1.15488 | v7 n.º 15 | 002654000 | aviso «Stop order executed … Sell 100000 at 1.15491» | STOP | sí |
| v7-21 | 08-07 12:14:55 venta 1.15345 | v7 n.º 21 | 003610000 | `Sell stop` (773->Sell stop en 1.15346) | STOP | sí |
| v7-22 | 08-10 11:57:15 compra 1.15503 | v7 n.º 22 | 003900000 | `Buy stop` (TP·SL·-885->Buy stop en 1.15544, por encima del precio 1.15535) | STOP | sí |
| v8-12 | 08-17 05:17:15 compra 1.15842 | v8 n.º 12 | 001478000 | `Buy stop` (541->Buy stop en 1.15842, precio 1.15834 por debajo) | STOP | sí |
| v8-18 | 08-19 09:03:00 compra 1.15984 | v8 n.º 18 | 002390000 | no legible (posición abierta desde 1.15983; el menú previo, 002375000, ofrecía «Buy … stop» sin selección) | STOP | — |

**7 legibles, 7 coinciden, 0 discrepan, 3 no legibles; 0 etiquetas limit.** El método no contradice
ninguna etiqueta. **Pero esto no lo valida tal cual**: una validación exige que el método separe los
dos tipos, y en las parejas no hay ninguna orden limit con la que probar que las clasificaría LÍMITE.
La única `Sell limit` de los dos vídeos (v7 n.º 6, 13:08 del día 3) no tiene pareja en el libro. Lo
que la Fase 3 dice es más débil y va dicho así: **las siete veces que se pudo comprobar, la etiqueta
stop y el lado de llegada coincidieron**.

## 4. Fase 4 · Dónde está la entrada respecto a la estructura de M1

Para las operaciones con zona viva en el llenado (los mismos supuestos que
`scripts/verificacion_a21_entradas.py`: zona detectada desde la primera toma del día, lado del sesgo
de la sesión de la toma, A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21 en cada lectura, en
DIAGNÓSTICO), la distancia firmada entre la entrada del trader y **`Esquema.referencia`**, el pivote
de M1 contrario cuya ruptura forma el esquema y que el productor usa como nivel del breaker:

- d_ref = entrada − referencia (compra) o referencia − entrada (venta): d_ref > 0, la entrada está
  más allá del nivel en la dirección de la ruptura; d_ref < 0, del lado de antes de romper.
- d_zona = la distancia firmada al borde cercano de la zona, la misma de `VERIFICACION-A21.md`.

Como las 77 son STOP, «las operaciones STOP» son todas; la distribución por tipo coincide con la total.

| lectura de A-21 | con zona viva | d_ref: mín · p25 · mediana · p75 · máx | \|d_ref\| ≤ 3 | \|d_ref\| ≤ 10 | d_zona: mín · p25 · mediana · p75 · máx | \|d_zona\| ≤ 3 |
|---|---|---|---|---|---|---|
| (a) `solo_una_zona_de_control` | 39 de 77 | −305 · −86 · −15 · +14 · +153 | **2** | 6 | −151 · −24 · +20 · +83 · +312 | 2 |
| (b) `sin_mecha_mas_alla_del_extremo` | 34 de 77 | −149 · −76 · −9 · +29 · +153 | **2** | 6 | −151 · −24 · +2,5 · +71 · +168 | 2 |

Frente a `VERIFICACION-A21.md` (entrada dentro de la zona en 6 de 77, 7 con la tolerancia): **el nivel
de referencia del breaker no está más cerca de la entrada que la zona**. La mediana de d_ref es
negativa: en más de la mitad de las operaciones con zona el trader vende POR ENCIMA del bajo que el
productor espera ver roto (o compra por debajo del alto), es decir, antes de que el precio llegue al
nivel que el motor llama breaker. Y la dispersión (p25 −86, p75 +14) dice que no es un desfase fijo.
Dicho como medida y nada más: el trader entra a favor de la ruptura (§2), pero **el punto que rompe no
es el `referencia` del productor**. Las 38 (a) y 43 (b) sin zona viva quedan fuera de esta fase, con el
motivo de siempre (sin toma antes del llenado, o toma sin esquema válido).

## 5. Lo que la medición sostiene, lo que no, y A-47

**Sostiene:**
- En construcción, **todas** las entradas del trader se llenan con el precio viniendo del lado de la
  ruptura, y el hecho es robusto al precio, la tolerancia y la ventana (§2.3). Una orden límite en el
  retroceso, tal como la modela RN-011, se llenaría con el precio viniendo del lado contrario, y eso
  no pasa ni una vez.
- Las etiquetas de FX Replay que se pudieron leer en las parejas (7) son todas stop y coinciden con el
  lado de llegada (§3).
- El «fuera por el lado del precio» de `VERIFICACION-A21.md` es compatible con esto: si la entrada
  está a favor de la ruptura y la zona del motor espera un retroceso, la entrada queda del lado del
  precio por construcción.

**No sostiene:**
- Que el trader entre en el **punto de breaker que calcula el productor**: en 2 de 39 la entrada está
  a ≤ 3 puntos de `Esquema.referencia` (§4). Si entra con stop, lo hace en un nivel que el productor
  no calcula, o que calcula con otra referencia (su propio zigzag, el «equal», el bloque envolvente
  de M1 de `SESION-02-VIDEO.md` §5). Esta rama no lo busca.
- Que el tipo de orden en la plataforma sea stop en las 77: el lado de llegada lo hace muy probable,
  pero solo hay 7 comprobaciones directas y ninguna limit contra la que discriminar (§3).
- Nada sobre el precio de colocación de la orden ni sobre el instante en que se coloca (A-29), ni
  sobre por qué once ventas de v8 no tienen pareja en el libro.

**Para la pregunta de A-47 el martes** («cuando pones la orden en el punto de breaker, ¿quieres entrar
cuando el precio rompe ese punto o cuando el precio vuelve a él?»), sin resolverla: la medida dice que
en sus dos backtests de construcción el precio SIEMPRE rompe hacia la entrada, nunca vuelve a ella.
Si el trader responde «cuando vuelve», habrá que preguntarle por qué en 77 de 77 no fue así; si
responde «cuando rompe», la siguiente pregunta es **qué punto** rompe, porque no es el que el
productor calcula (§4). Lo decide el consultor.

## 6. Riesgos y dudas para el consultor

1. **El instante del libro y el nivel son la misma marca**: p(t) ≈ L por construcción (§2.2). El
   criterio no depende de eso (decide por el último tick FUERA del nivel), pero un libro con el
   instante de la ORDEN en vez del llenado daría otra cosa; `INSTANTE-LLENADO-SALIDA.txt` mide que es
   el llenado.
2. **Consolidación previa**: el precio ronda el nivel de mediana 4 minutos antes del llenado. Con
   ventanas largas eso se ve como ambiguo (hasta 52 de 75 con 300 s y tolerancia 0). El criterio fijó
   60 s antes de medir y ahí no hay ambiguas; se dice para que nadie lea el 77/77 como si el precio
   viniera limpio de lejos.
3. **Ticks de Dukascopy frente a OANDA de FX Replay**: 1–2 puntos de diferencia (A-16), cubiertos por
   τ = 2; la robustez con τ = 0 y τ = 5 no cambia el signo.
4. **Fase 3 con n = 7** y sin una sola limit: el método queda sin refutar, no validado.
5. **Fase 4 hereda todos los supuestos de `VERIFICACION-A21.md`** (zona desde la primera toma del
   día, diagnóstico de A-35 y A-44, lecturas de A-21) y la mitad de las operaciones no tienen zona
   viva. Dice dónde no está la entrada; no dice dónde está.
6. **Dos operaciones con M1** (23 de abril): mismo resultado, fuente distinta, en tabla aparte.

## 7. Control positivo del método (2026-09-27, revisión del consultor)

El método de §2 solo se había contrastado con etiquetas stop (§3). El consultor pidió aplicarlo, con
el MISMO criterio de §1 y sin cambiar nada, a la única orden que FX Replay etiquetó como `Sell limit`
—v7, operación n.º 6: lunes 3 de agosto, orden colocada a las 13:04:59 UTC+2 en 1.15253, llenado
entre 13:05 y 13:12 UTC+2 según `SESION-02-VIDEO.md` §3.2—, y añadir un control sintético en los
tests. El 3 de agosto es día de desarrollo, comprobado con `casos_reservados` y `casos_ocultos` antes
de leer nada. Salida en `ORDEN-STOP-O-LIMITE-SALIDA.txt` («CONTROL POSITIVO»), producida por
`control_sell_limit` del script.

### 7.1 El control real: AMBIGUO

Con los ticks del 3 de agosto (bid, porque es una venta), tolerancia 2 y la ventana entera del
informe de v7 porque el instante es incierto (regla 2 del criterio):

| | |
|---|---|
| ticks en 11:04:59–11:12:59 UTC | 214 |
| bid al colocar la orden (último tick ≤ 11:04:59 UTC), respecto a L | −2 puntos |
| bid mínimo / máximo en la ventana, respecto a L | −4 / +13 |
| ventana entera (criterio con instante incierto) | lado **ambiguo** → **ambiguo** |
| primer tick en el nivel | 11:05:02 UTC, 3 s después de colocarla |
| W1 = [ese tick − 60 s, ese tick] | lado **ambiguo** → **ambiguo** |

La traza de los 90 s anteriores al primer toque (bid − L, en puntos): +3 +3 +5 +4 … +5 +0 +0 +2 +3 +5
… +5 +4 +1 +1 +3 +3 +3 −1 −2 +1 −3 +0 −1 +0, y después +5 +6 +5 +9 +11 +9 +12. El precio estaba EN el
nivel cuando se colocó la orden (−2 puntos, dentro de la tolerancia) y oscila a los dos lados de L
durante toda la ventana. El fotograma `001080000` lo confirma: la etiqueta «Sell limit» aparece a las
13:04:59 UTC+2 con la última vela cerrando en 1.15252, un punto por debajo de la orden.

**Resultado del control real: AMBIGUO.** No es LÍMITE. El método no ha distinguido esta orden. Es
exactamente el caso que el propio criterio de §1 dejaba fuera de su lógica —«salvo que la orden se
colocara con el precio ya en L»—, pero esa salvedad no convierte el ambiguo en un LÍMITE: el control
pedido era que saliera LÍMITE, y no sale.

### 7.2 El control sintético: pasa

`tests/unit/test_orden_stop_o_limite.py`, con ticks inventados (día 2030-01-07, nivel 1.00000, que no
es de ningún día ni precio real): una serie que SUBE hasta un nivel de venta sale LÍMITE; una que
BAJA, STOP; una compra a la que el precio baja, LÍMITE, y a la que sube, STOP; una que cruza el nivel
por los dos lados, ambiguo; y sin ticks en la ventana el método cae a M1 y lo dice. Las funciones puras
y la Fase 2 de punta a punta pasan los seis casos.

### 7.3 Decisión, según la regla que fijó el consultor

La regla era: si el control real sale LÍMITE, el método queda validado; **si sale STOP o ambiguo, el
77/77 NO se sostiene, no se cierra la rama y se para.** Salió ambiguo. Por tanto:

- **El 77 de 77 de §2 NO queda sostenido por este control.** Lo que el método ha demostrado
  distinguir son series sintéticas; sobre la única orden límite real disponible, no distingue.
- **Lo que sí sigue en pie, dicho como medida**: las 77 entradas de construcción llegan al nivel desde
  el lado de la ruptura (§2), y ninguna de las 75 con ticks es ambigua con la ventana de 60 s. La
  orden límite real, en cambio, ES ambigua con esa misma ventana. Es decir, el método separa las 77
  de este caso; lo que no ha podido enseñar es que un LÍMITE real le salga LÍMITE.
- **Qué haría falta para validarlo**: una orden límite real colocada con el precio LEJOS del nivel y
  llenada por un retroceso. En v7 y v8 no hay ninguna: la única limit del trader se colocó con el
  precio a 1 punto de ella. Con el trader el martes se puede pedir, o buscar en un backtest suyo con
  el tipo de orden anotado.

**La rama no se cierra y aquí se para**, como manda la regla. A-47 sigue ABIERTA.

> **NOTA de la revisión del consultor (2026-09-28). El control de v7 n.º 6 queda como NO
> INFORMATIVO.** La orden se colocó con el bid a 2 puntos del nivel, dentro de la tolerancia: no hubo
> retroceso que medir, así que el método no tenía un lado de llegada que leer. Y el fallo relevante
> habría sido clasificarla STOP, que no ocurrió. La regla «ambiguo → el 77/77 no se sostiene» de
> §7.3 era, en palabras del consultor, demasiado gruesa, y el error es suyo. El control se sustituye
> por el de §8. El cuerpo de §7 no se reescribe.

## 8. Control con llenados LÍMITE reales del simulador (2026-09-28)

**Qué se hizo.** La corrida que en `PREPARACION-A21.md` §3 dio las 9 operaciones del bot —`botsito
motor arnes --simular` sobre construcción, con ticks (ADR-0051), en DIAGNÓSTICO: A-35
`cierre_vela_contraria`, A-44 `sin_tope`, A-21 en cada lectura—, reproducida por
`control_simulador` del script con las mismas piezas que la CLI (`construir_motor_cableado`,
`arnes.correr`). De cada posición del bot se comprueba en el bróker, antes de clasificar nada, que
nace de una orden LÍMITE: su orden existe, la posición es `pos-<orden>`, el historial es `colocada >
llenada`, el precio de la orden es la entrada de la posición y el llenado es con ticks. El bróker
simulado solo coloca órdenes límite (`primitivas_broker.colocar_limite` es la única vía del bot), y
las llena cuando el bid (venta) o el ask (compra) pasa **estrictamente** más allá del precio
(`engine/llenado.py`, `limite_llena_al_toque: false`). A cada entrada se le aplica la Fase 2 con el
MISMO criterio de §1, sin tocar nada; el instante es el del tick que llena.

**Resultado.** Las dos lecturas dan 9 posiciones, como en `PREPARACION-A21.md`; 8 son comunes y
cada lectura tiene una propia. **Una se excluye en las dos**: la venta del 23 de abril a las 05:01
UTC se llenó con el respaldo M1, porque la hora `2026-04-23T05Z` no tiene ticks (es la misma hora
perdida de §2). Las otras 8 de cada lectura son llenados de orden límite con ticks, comprobados en
la traza.

| día | llenado UTC | dir. | entrada | orden: colocada (UTC) | precio al colocar − L (puntos) | clase de la orden al colocarla | Fase 2 | lecturas |
|---|---|---|---|---|---|---|---|---|
| 2026-04-02 | 12:18:06 | venta | 1.15242 | 12:17:59 | −11 | en espera (el bid por debajo) | **LÍMITE** | a y b |
| 2026-04-08 | 08:27:46 | compra | 1.16823 | 07:17:59 | +41 | en espera (el ask por encima) | **LÍMITE** | a y b |
| 2026-04-10 | 09:33:15 | venta | 1.16974 | 09:32:59 | −11 | en espera | ambiguo | a y b |
| 2026-04-23 | 05:01:00 | venta | 1.16994 | — | — | excluida: llenado con respaldo M1 | — | a y b |
| 2026-04-27 | 05:01:00 | compra | 1.17268 | 05:00:59 | −5 | **cruzada**: el ask ya estaba por debajo de la compra límite | ambiguo | a y b |
| 2026-04-29 | 07:16:02 | venta | 1.17056 | 07:15:59 | −2 | en el nivel (dentro de la tolerancia) | **STOP** | a y b |
| 2026-08-03 | 06:01:00 | venta | 1.15363 | 06:00:59 | +14 | **cruzada**: el bid ya estaba por encima de la venta límite | **STOP** | a y b |
| 2026-08-04 | 07:16:00 | venta | 1.15085 | 07:15:59 | +28 | **cruzada** | **STOP** | a y b |
| 2026-08-11 | 12:32:35 | venta | 1.15405 | 11:16:59 | 0 | en el nivel | **LÍMITE** | solo a |
| 2026-08-20 | 11:01:04 | compra | 1.16981 | 11:00:59 | −16 | **cruzada** | **STOP** | solo b |

| lectura | llenados límite con ticks | LÍMITE | ambiguo | STOP |
|---|---|---|---|---|
| (a) `solo_una_zona_de_control` | 8 | 3 | 2 | **3** |
| (b) `sin_mecha_mas_alla_del_extremo` | 8 | 2 | 2 | **4** |
| las 9 distintas de las dos lecturas | 9 | 3 | 2 | **4** |

La columna «precio al colocar − L» se calculó en la misma corrida, antes de mirar la clasificación,
y da la clave del resultado. Con la misma tolerancia de 2 puntos, las 9 órdenes distintas con ticks
son de tres clases:

| clase de la orden al colocarla | órdenes | LÍMITE | ambiguo | STOP |
|---|---|---|---|---|
| **en espera**: el precio al otro lado del nivel, la orden espera a que llegue | 3 | 2 | 1 | **0** |
| **en el nivel**: el precio a ≤ 2 puntos | 2 | 1 | 0 | 1 |
| **cruzada**: el precio ya había pasado el nivel; el bróker la llena en el siguiente tick, 1–5 s después | 4 | 0 | 1 | **3** |

**Lo que eso dice, descriptivo.** El método lee DESDE QUÉ LADO LLEGA EL PRECIO, y con eso distingue
una límite que espera (ninguna sale STOP, 2 de 3 salen LÍMITE) de una stop. Pero una límite
colocada con el precio ya al otro lado se llena como una orden a mercado en cuanto se coloca, con el
precio llegando del lado de la ruptura, y el método la lee STOP: **por el lado de llegada, una límite
cruzada y una stop son indistinguibles**. Las 4 STOP distintas son 3 cruzadas y 1 colocada en el
nivel (la otra colocada en el nivel salió LÍMITE); **ninguna es una límite en espera**.

## 9. Decisión, según la regla que fijó el consultor

La regla era: si todas salen LÍMITE (con algún ambiguo explicado), el método queda validado; **si
alguna sale STOP, el método no distingue, no se cierra y se para.** Salen STOP: 3 de 8 en (a), 4 de 8
en (b). Por tanto:

- **El método NO queda validado.** Tal como está escrito en §1, no distingue una orden límite de una
  stop cuando la límite se coloca con el precio en el nivel o ya al otro lado.
- **El 77 de 77 de §2 se lee, con esto, más estrecho**: las 77 entradas del trader llegan desde el
  lado de la ruptura, y eso es compatible con órdenes stop Y con órdenes límite colocadas en el nivel
  o cruzadas. Lo que sí sigue excluido, porque ninguna límite en espera ha salido STOP, es que el
  trader entre con límites colocadas de antemano esperando un retroceso (la forma de RN-011). Eso
  es una lectura del consultor, no una conclusión del método: el método no ha quedado validado.
- **No se añade al §0** que el 77/77 se sostenga, ni la coincidencia con lo que el trader dijo en la
  llamada: esa parte del brief solo aplicaba si el método quedaba validado.
- **La rama no se cierra y aquí se para.** A-47 sigue ABIERTA.

**Qué haría falta para separar las dos lecturas**: el instante y el precio de COLOCACIÓN de cada
orden del trader, no solo el llenado. Con él, una stop y una límite cruzada se distinguen, porque la
stop espera al otro lado del precio y la límite cruzada no espera nada. El libro de FX Replay no trae
el instante de colocación; los vídeos v7 y v8 sí lo enseñan (la etiqueta de la orden aparece antes
del llenado), y es lo que A-47 le pregunta al trader el martes.

## 10. Estado

Rama lista para revisión, NO cerrada. El control de §7 quedó como no informativo (nota del
consultor); el que lo sustituye, con llenados límite del simulador (§8), da STOP en 3 de 8 y 4 de 8:
el método no queda validado y la rama no se cierra (§9).
