# PUNTO-USADO · Qué gasta un punto: la reentrada tras un stop y el rechazo al llenar (R3.4)

Rama `trabajo/punto-usado`, abierta el 2026-10-18 desde `main` en f96b581 (commit de estado sobre
el merge 3ae2933, tag `stable/F37u-plataforma-adelantada`). Encargo:
`docs/encargos/trabajo-punto-usado.md`. Tramo: R3 (R3.4 de `docs/plan/HOJA-DE-RUTA.md`; Y de la
Next Action). Modelo de la sesión: `claude-fable-5-1` según el entorno de la sesión; `/model` en el
terminal de Aleks dio «Fable 5.1 … `high` effort» al empezar.

(Hasta que existió, ADR-0083 iba declarado aquí en un bloque `ids-inexistentes`; salió en el commit
que lo creó.)

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones de la skill `abrir-rama`, con su salida:

| Comprobación | Comando | Salida |
|---|---|---|
| `main` es el sha del encargo y es `origin/main` | `git rev-parse --short main`; `git rev-parse main origin/main` | `f96b581`; dos veces `f96b581bfbf93fa3fb6478f3fbc0261dcc0aa37b` |
| El último tag de HISTORIA apunta al merge bajo `main` | `git rev-parse "stable/F37u-plataforma-adelantada^{commit}"`; `git rev-parse main^1` | dos veces `3ae2933817c968de2eea27651416d5fdce6721a8`; `git ls-remote --tags origin stable/F37u-plataforma-adelantada` → `9546e31… refs/tags/stable/F37u-plataforma-adelantada` |
| La CI de `main` sobre su HEAD | `gh run view 39186492700 --json status,conclusion,headSha,headBranch,name` (con `gh`, como pide el encargo; ni curl ni guion) | `{"conclusion":"success","headBranch":"main","headSha":"f96b581bfbf93fa3fb6478f3fbc0261dcc0aa37b","name":"ci","status":"completed"}` |
| Ninguna otra rama | `git branch --list`; `git ls-remote --heads origin "fix/*"` | `* main`; vacío |

`PROJECT_STATE.md` en `main`: 21.911 bytes (`wc -c`), como dice el encargo. `git status --short`
vacío antes de abrir.

**El primer `make check` de la rama salió en rojo** (5 fallos, todos «id citado que no existe:
ADR-0083», en PROJECT_STATE:10 y en el encargo :31, :38 y :67), como le pasó a
`trabajo/plataforma-adelantada` con ADR-0082 (PLATAFORMA-ADELANTADA.md, «Lo que el repo pide y el
encargo no dice»). El auditor del encargo lo había avisado (H1). Arreglado igual: un bloque
`ids-inexistentes` en el encargo y otro aquí, y el id fuera de PROJECT_STATE («un ADR nuevo»). Los
bloques salen en el commit que cree el ADR.

## 1 · Fase 0 · Inventario (sin tocar nada)

### 1.a El encargo frente al repo (el auditor `auditor-encargo`, 2026-10-18)

57 afirmaciones: 47 correctas, 0 incorrectas, 10 con matiz; 7 herencias que el repo pide y el
encargo no dice. El auditor solo leyó el repo (ni holdout, ni libros, ni imágenes, ni corpus; de la
diaria de MARGEN-LOTE, días dev, solo recuentos con `grep -c`). Los matices y las herencias, con lo
que hace la rama con cada uno:

| # | Hallazgo | Evidencia | Qué hace la rama |
|---|---|---|---|
| M7 | LA-CAJA-DEL-29-DE-ABRIL.md:237-242 da las dos ventas (07:55 y 07:58 UTC, misma entrada 1.17064 y mismo stop 1.17079) pero solo la hora de ENTRADA, no la de cierre de la primera: el «después» del stop no se demuestra ahí; abril es construcción | LA-CAJA:236-243 | ADR-0083 cita el pasaje como lo que es: dos entradas en el mismo nivel con tres minutos entre ellas y la primera perdida en el stop (`rPnL -15`), y la narración «sería cuestión de poner otra reentrada aquí». No afirma más (la hora de cierre no está leída) |
| M8 | ADR-0066:51 habla del ESCENARIO (la liquidez sigue dando intentos), no del punto; VISOR-CONSTRUCCION.md:673-675 ya descartó esa lectura por escrito | 0066:51; VISOR:673-675 | ADR-0083 contesta a ese pasaje: ADR-0066 no fija si el intento siguiente puede ir al mismo punto; lo que lo apoya es el material del punto 1 (abril) y `fb-2026-09-09-sesion-01-fe4a6a5c` (H6) |
| M17 | Con la MISMA caja `main` ya niega (la zona queda en `usadas` al colocar, primitivas_broker.py:650): el test D3b solo falla en `main` si construye OTRO 1 | zonas.py:471-476 | El test D3b construye un 1 nuevo tras el rechazo al llenar (dicho en su docstring) |
| M18 | El camino «no se coloca» es ADR-0081 §2 y §3, no solo §3 | primitivas_broker.py:624-626; 0081:72-75 | Se cita «§2 y §3» |
| M21 | `escenario_terminado` está en zonas.py:467-468 (:466 es `_anotar_toma`) | zonas.py:466-468 | Nada |
| M22 | El motor solo tiene cuatro resultados de cierre: `salto_el_stop`, `break_even`, `perdida` y `ganancia` (primitivas_broker.py:180-184); el «equal» no tiene clase (es RN-019, que no dispara: §1.h). Y el cierre MANUAL (`cerrar_a_mercado`, RN-002, y el fin de día) no está en 4.a | primitivas_broker.py:180-184 | D1 se aplica por RESULTADO: libera el punto todo cierre (`stop`, `objetivo` o `manual`) cuyo resultado no sea `ganancia`. El manual entra en la tabla de 1.b |
| M23 | ADR-0083 estaba libre en `main`, pero la rama ya lo citaba (PROJECT_STATE estadiado, encargo, contrato) sin bloque `ids-inexistentes` | ids_citados.py:39 y :67 | Arreglado antes del primer commit (§0) |
| M31 | La fila de los cartuchos agotados de §3.1 está en VISOR:904 (:906 es el párrafo «Correcto…»); y hay más pasajes que dan la E por buena (H2) | VISOR:898, :904 | Recuadros en todos (H2) |
| M41 | test_margen_lote.py:185 es un test del bróker sin `usadas`; :333 pasa por `no_enviadas`; test_cableado.py no nombra `marcar_usada`, `usadas` ni `rechazados` | grep | 1.e lo recoge |
| M55 | HISTORIA ya tiene una «# Next Action HECHA · Y ·» (HISTORIA.md:7130): el título de la de esta rama lleva nombre, como el de O | HISTORIA:7130, :10131 | Las líneas preparadas (§6) lo llevan |
| H1 | El bloque `ids-inexistentes` para ADR-0083 | ids_citados.py | Hecho (§0) |
| H2 | Más pasajes de VISOR-CONSTRUCCION.md dan la E por buena: :582-586 y :596 (2026-01-29 11-15), :861 (§2.g), **:932-934 (§3.2, pregunta 3: «se arregla en Y», que V lee directamente)**, :1022 y :1026-1031 (líneas preparadas de R3.2 y R3.4), :1203 (desviación) y :1432 (Estado); y en la hoja de ruta, el Estado de R3.2 (HOJA-DE-RUTA.md:160, «Una E (la reentrada en un punto ya llenado: R3.4)») | VISOR, HOJA | Recuadros también en :596, :861, :932-934, :1022-1031, :1203 y :1432 (el cuerpo intacto); :582-586 es el mismo pasaje que :596. La línea de la hoja de ruta va en las líneas preparadas para el cierre (§6), porque `docs/plan/` está protegido en el contrato |
| H3 | Las filas del índice de ADR: la nueva de 0083, la de 0064 (README.md:70) y la de 0074 (:80) con su nota; y que el Impacto de ADR-0083 nombre sus notas | test_adr.py:38-42; a519d06 | Fase 3 |
| H4 | R3.4 pasa a HECHA sin ganar `ID:ADR-0083` en sus Refs | HOJA:7-10, :179 | Las líneas preparadas añaden `ID:ADR-0083` a los Refs de R3.4 |
| H5 | D1 es PROVISIONAL hasta la pregunta 3 de V, pero no es un parámetro ni cuelga de ninguna A-nn: nada mecánico lo ata | test_provisional_cuelga_de_abierta.py:1-7; README.md:87 | Se apunta en el Estado de ADR-0083 y en su fila del índice («PROVISIONAL en D1 hasta la pregunta 3 de V»), como ADR-0081 con A-57; y en la línea de V de las líneas preparadas |
| H6 | `fb-2026-09-09-sesion-01-fe4a6a5c` (CONFIRM sobre `ev-v4-003710-c753f3d3`): «SI (no hay entradas en paralelo; para reentrar debe haber tocado el stop)»; sigue vivo según `fb-…-fae74396` («'para reentrar debe haber tocado el stop' siguen siendo ciertas») | los dos registros | ADR-0083 lo cita: apoya D1 (se reentra tras el stop) y D4 (no en paralelo) |
| H7 | El docstring de `marcar_rechazada` (zonas.py:405-406) y el comentario de primitivas_broker.py:624-626 también citan la decisión 1 de ADR-0064 | zonas.py:405; primitivas_broker.py:624-626 | Pasan a citar ADR-0083 en la fase 3 |

Lo que el auditor no pudo comprobar y la rama mide después: que la corrida «antes» salga igual a
la diaria de MARGEN-LOTE (fase 1); que los tests «pasan en los dos» (fase 2); la hora de cierre de
la primera venta del 29 de abril (no se lee: no hace falta para D1); si el trader dijo algo contra
D1 fuera de `knowledge/feedback` (la sesión buscó en `knowledge/evidence` por `grep` de texto
citable, «reentr» y «mismo nivel»: nada contrario; §1.i).

### 1.b (4.a) Por dónde termina una orden, y si gasta su punto hoy y con D1

Hoy hay DOS marcas, y las dos viven en la memoria de la sesión (`zonas.py`, `_de_la_sesion`):

- **`usadas`**, por ZONA (`marcar_usada`, zonas.py:418-420): el id de la zona (`zona:N`), que con
  `caja_se_fija = en_cada_cierre_m1` es una por `nivel@inicio#extremo` (zonas.py:377-395), así que
  cada 1 nuevo del mismo punto es otra zona. Se marca al colocar (primitivas_broker.py:650) y al no
  enviar (:635). **Nunca se borra.**
- **`rechazados`**, por PUNTO (`marcar_rechazada`, :404-410): la clave `nivel@inicio` de
  `punto_de_zona`. Se marca al no enviar (:636) y al rechazo al colocar (:653).

`toca_colocar_orden_limite` niega si la zona está en `usadas` o su punto en `rechazados`
(zonas.py:471-476), y antes si el escenario terminó (:467-468). «Gasta el punto» = ninguna caja de
ese punto se vuelve a colocar en la sesión; «usa la zona» = esa caja no, otra sí.

| Camino | Dónde | La orden y la zona | ¿Gasta el punto HOY? | ¿Con D1? | ¿Cambia? |
|---|---|---|---|---|---|
| Rechazada al COLOCAR (precio_invalido, stops_level, volumen, margen) | `colocar_orden_limite`, primitivas_broker.py:647-653; el bróker, broker.py:506-519 | zona usada (:650) y punto rechazado (:653) | sí | sí (D1: gasta) | no |
| No enviada (lote bajo el mínimo, o `lote_si_no_cabe = no_operar` con un límite que muerde; ADR-0081 §2 y §3) | primitivas_broker.py:628-638 | zona usada y punto rechazado (:635-636) | sí | sí (D1: gasta) | no |
| Rechazada al LLENAR (margen libre, ADR-0081 §4) | broker.py:813-834: la orden pasa a `rechazada`, evento `(instante, "rechazada", id, fuente)` a `Traza.eventos` (:833); llega a `ctx.eventos` por el `else` de `_a_la_cuenta` (cableado.py:395-396) como `EventoBroker(ms, "rechazada", id)`, sin `por` ni `resultado` | zona usada (al colocar); el punto NO se marca: nadie llama a `marcar_rechazada` | **no**: un 1 nuevo vuelve a colocar el punto (misma caja no) | sí (D1: gasta) | **sí: D3b** |
| Llenada y cerrada por STOP (`salto_el_stop`), por BREAK EVEN (`stop` con `stop_original`) o por OBJETIVO (`ganancia`); y por MANUAL (`cerrar_a_mercado` de RN-002 al vencer la H4, primitivas_broker.py:657-667, o el fin del día, cableado.py:302-304), que `clasificar_cierre` (:180-184) da como `ganancia` o `perdida` por el bruto | broker.py:835-845 (el llenado) y `_cerrar` (:870); cableado.py:366-391 (a la cuenta, a `ctx.eventos` con `resultado` clasificado, :389, y a `ctx.cierres` para los cartuchos, :391) | zona usada (al colocar); el punto no | **no** por punto, **sí** por caja: la misma caja no vuelve (zona en `usadas`), otra sí. Es la E de VISOR §2.d.4 leída al revés: el error no es volver al punto, es no volver con la misma caja | **no gasta** si cierra sin ganar (D1: misma caja o con otra; los cartuchos delante, RN-016); tras una ganadora RN-034 termina el escenario y nada se coloca (ya hoy, zonas.py:467-468) | **sí: D3a** (la misma caja vuelve tras un cierre sin ganancia) |
| Cancelada por RN-035 (`retirar_orden_limite`, a `ventana_fin` o al abrir otra sesión, `se_retira`) | primitivas_broker.py:681 | zona usada; punto no | no (misma caja no; es el fin de la sesión o de la ventana: no se coloca nada después en esa sesión) | igual | no |
| Cancelada por RN-036 (`retirar_ordenes_pendientes`, la racha) | :694 | zona usada; punto no | no (RN-036 prohíbe operar después) | igual | no |
| Cancelada al abrir un escenario nuevo con `se_retira` (`abrir_escenario`) | :714 | zona usada; punto no | no: el escenario nuevo coloca su punto cuando lo da | igual | no |
| Cancelada por la reubicación (RN-006, `reubicar_orden_limite`): un 1 nuevo del mismo punto (ADR-0074) o un punto nuevo (ADR-0064 §4) | :753 | la zona vieja usada; la nueva se coloca en el mismo cierre (RN-011 y RN-015) | no (es la vida de la orden) | no gasta (D1) | no |
| Cancelada por la red de seguridad del fin del día (ADR-0053 §6) | cableado.py:302-309 | zona usada; punto no | no (el día terminó) | igual | no |
| Cancelada al empezar una ventana prohibida (`_cancelar_por_cierre`, ADR-0068) | broker.py:849-868; es una petición del bot (`protege=True`), no un evento del servidor | zona usada; punto no | no (misma caja no; otra sí, pasada la ventana) | igual | no |
| EXPIRADA | broker.py:801-807 | — | **no ocurre**: ningún llamador del cableado pasa `expira_ms` (`grep expira` en primitivas_broker.py y cableado.py: nada; `colocar_stop`/`colocar_limite` lo dejan en None, broker.py:440-462) | — | no |

**La PARADA de 4.a no se da:** D1 solo cambia los dos caminos de D3. Lo que D1 no nombra (las
cancelaciones) se queda como hoy: la zona cancelada sigue en `usadas` (esa caja no vuelve) y el
punto no se gasta (otra caja sí). Lo dice la fase 3 en ADR-0083 («lo que no cambia»). La decisión
1 de ADR-0064 se escribió para el rechazo («se rechaza una vez y no se reintenta en cada M1», :80-81)
y el código la aplicó también al llenado por el mecanismo de `usadas`, que no distingue.

### 1.c (4.b) La vía

**Lo que hay.** `_a_la_cuenta` (cableado.py:349-357) recibe `broker, ctx, tb, nuevos, vistos,
hasta_ms`: ni el `EstadoDia` ni la sesión. Pero deja en `ctx.eventos` TODO lo que hace falta: el
llenado (`LLENADA`, con `por`, :375), cada cierre (`stop`, `objetivo`, `manual`, con `resultado`
clasificado, :389) y el rechazo al llenar (`"rechazada"`, por el `else` de :395-396). Y `correr_dia`
tiene a la vez `ctx` y `estado` (:234-243), que es donde `estado.broker = broker.hechos()` ya
refresca los hechos cada minuto (:265). La zona de cada orden está en `ctx.zona_de_orden`
(primitivas_broker.py:649);
la sesión de la orden, no: el cableado la reconstruye después para el informe (`_sesion_de`,
:770-779, «la sesión de una orden, por el CIERRE de M1 en que se colocó»).

**Propuesta: en el cableado, a partir de `ctx.eventos`, sin cambiar la firma de `_a_la_cuenta`.**

1. `primitivas_broker.py`, `colocar_orden_limite`: junto a `ctx.zona_de_orden[id] = z.id`, apuntar
   `ctx.sesion_de_orden[id] = momento.sesion` (campo nuevo de `ContextoDia`, `dict[str, str | None]`).
   Es el mismo dato con el que el productor marcó la zona (`marcar_usada(estado, momento.sesion, …)`),
   sin reconstruirlo.
2. `zonas.py`: `liberar_usada(estado, sesion, zona_id)` (`usadas.discard`) con su docstring: la
   orden de esa zona terminó sin ganar y el punto vuelve a estar disponible, con esa caja o con
   otra; `marcar_rechazada` queda como está (gasta el punto) y pasa a citar ADR-0083.
3. `cableado.py`, `correr_dia`: justo después de `vistos = self._a_la_cuenta(...)` del paso 1 (:262),
   una función nueva `_el_punto_tras_el_evento(ctx, estado)` recorre `ctx.eventos` de ese minuto:
   - `tipo == "rechazada"` → `marcar_rechazada(estado, ctx.sesion_de_orden[id], ctx.zona_de_orden[id])`
     (D3b; la zona ya estaba usada desde que se colocó);
   - `tipo in (stop, objetivo, manual)` y `resultado != ganancia` → `liberar_usada(...)` con la zona de
     `p.orden_id` (D3a). Con `ganancia` no se libera: RN-034 termina el escenario y `toca_colocar`
     ya niega (zonas.py:467-468); dejar la zona usada es defensa en profundidad y no cambia nada.
   Las órdenes que no son del productor (zonas sintéticas de los tests, sin `punto_de_zona`) no
   rompen nada: `marcar_rechazada` no hace nada sin punto y `liberar_usada` descarta el id.

**Por qué ahí.** Los predicados son puros y no pueden escribir (ADR-0055 §1); una acción de la spec
necesitaría una regla que disparara en cada cierre y en cada rechazo solo para llevar la memoria
del productor, que es mecánica y no estrategia. `_a_la_cuenta` es el puente bróker→cuenta y no sabe
de la memoria de la estrategia; cambiarle la firma para pasarle el `EstadoDia` mezclaría las dos
cosas en la misma función. El bucle de `correr_dia` es el único sitio que ya tiene el bróker, el
contexto y el estado, y es donde los hechos del bróker llegan al intérprete: el punto se gasta o se
libera en el mismo minuto en que el cableado ve el evento, antes de evaluar las reglas de ese
cierre, igual que `operacion_abierta`.

**`_punto_nuevo` (primitivas_broker.py:235-253) no cambia.** Su `de_la_orden not in usadas → None`
(:241-243) sigue valiendo: una orden PENDIENTE tiene su zona en `usadas` desde que se coloca y solo
se libera al cerrarse su posición, cuando ya no está pendiente; así que «la pendiente es de esta
sesión» se sigue leyendo igual. Lo que cambia es el sentido de `usadas`: de «zonas cuya orden se
envió alguna vez» a «zonas cuya orden está viva (pendiente o abierta) o terminó sin liberar el
punto». Su test (fase 2): tras una pérdida, la misma zona se vuelve a colocar (o2) y un 1 nuevo la
reubica como hoy (RN-006: cancelar y colocar en el mismo cierre), y con una orden de OTRA sesión
pendiente sigue devolviendo None.

**Un límite medido, fuera de D1-D3:** `zona_del_punto` liga cada zona al escenario vigente cuando
la crea (zonas.py:397) y la clave `puntos` es de la sesión. Si tras una toma nueva (escenario
nuevo) el último pivote contrario siguiera siendo el mismo punto con la misma caja, la zona
reutilizada seguiría ligada al escenario viejo y sus cierres contarían en los cartuchos de aquel
(`cartuchos`, primitivas_broker.py:380-396, cuenta por `escenario["zonas"]`). Hoy no es
alcanzable (la zona no se vuelve a colocar); con D1 lo es en teoría. No se toca en esta rama: se
mide en la fase 4 (si alguna sesión reentra en un escenario nuevo con una zona del anterior, se
dice) y, si aparece, va a Technical Debt.

### 1.d (4.c) D4 y la traza de 2026-07-13 11-15 (día dev de construcción)

De `anexos/VISOR-CONSTRUCCION/dias/2026-07-13.traza.txt:414-416` (órdenes de la sesión) y de los
«Eventos del broker» y «### Ordenes» de la diaria de `main` (`anexos/MARGEN-LOTE/diaria…txt`,
líneas de 2026-07-13):

| Orden | Colocada (cierre de M1) | Llenada | Cierre de su posición | Zona | 1 de la caja | Stop |
|---|---|---|---|---|---|---|
| o11 | 09:36:59.999Z | 09:37:00.370Z | stop 09:37:09.912Z | zona:123, punto `114301@29732256` | 1.14297 | 1.14297 |
| o12 | 09:37:59.999Z | 09:38:31.016Z | stop 09:38:40.213Z | zona:124, el MISMO punto | 1.14292 | 1.14293 |
| o13 | 09:38:59.999Z | 09:39:00.191Z | stop 09:39:24.216Z | zona:125, el MISMO punto | 1.14291 | 1.14293 |

**Sí: cada una se coloca en el cierre de M1 siguiente al stop de la anterior, y ninguna con la
posición anterior abierta** (o11 cierra a las 09:37:09Z y o12 se coloca a las 09:37:59Z; o12
cierra a las 09:38:40Z y o13 se coloca a las 09:38:59Z). Lo garantiza RN-011 por el cableado:
`ninguno_de operacion_abierta` (strategy_spec.yaml:1490-1495) se evalúa con `estado.broker =
broker.hechos()` del cierre, y RN-018 con `operaciones_simultaneas_max = 1` (parametros.yaml:944-955)
prohíbe `abrir_operacion` mientras haya una viva. **Y cada una con OTRA caja:** tres 1 distintos
(1.14297, 1.14292, 1.14291: el mínimo del bloque bajó con cada vela), tres zonas del mismo punto. Por
eso `main` las colocó: ninguna caja repetida. o12 y o13 llevan el mismo stop (1.14293) porque el
redondeo de `stop_fraccion_redondeo` iguala dos 1 que difieren en un punto: la caja NO se
distingue por el stop ni por la distancia, solo por el 1 (lo que fija qué campo añade la fase 1).
La cuarta de la sesión, o14 (12:14:59Z, punto `114223@29732414`), es el rechazo por
`precio_invalido` de §2.g de VISOR; su punto queda en `rechazados` (traza :418). Las tres pérdidas
agotan los cartuchos a las 09:40Z (`detenido_por_cartuchos`, traza :254).

**Lo que pasa el 29 de abril en el bot** se mide en la fase 4 sobre la corrida 2 (la sesión 07-11
de ese día dev), con la traza de órdenes y puntos; en la fase 0 no se corre nada.

### 1.e (4.d) Los tests que dependen de `marcar_usada`, `usadas` y `rechazados`

| Test | Qué comprueba | ¿Cambia con D1 por la vía de 1.c? | Qué se hace |
|---|---|---|---|
| test_orden_stop_pivote.py:178-197 (`test_el_productor_liga_una_zona_por_punto_y_no_repite_un_punto_usado`) | marca `usada` a mano (sin cierre) y la zona no vuelve en el cierre siguiente; un punto nuevo liga otra zona | **No**: sin cierre nada libera; una orden pendiente sigue sin repetirse | Su docstring pasa a decir «mientras su orden esté viva» |
| :210-237 (`test_con_la_caja_recalculada_un_1_nuevo_liga_otra_zona_del_mismo_punto`) | con `usada` + `rechazada`, el punto no vuelve con otra caja | **No**: el rechazo sigue gastando el punto | Cita ADR-0083 en vez de «decisión 1» |
| :312 (`test_la_cadena_colocada_cancelada_recolocada_y_llenada_por_el_cableado`, con `_cadena` :255-310) | la cadena colocada→cancelada→recolocada→llenada→OBJETIVO; su `toca` sintético consulta `zonas_usadas` | **No**: el cierre es `ganancia` (objetivo), no se libera nada | Nada |
| test_escenarios_por_sesion.py:506 (`_motor_dos_tomas`, `toca` sintético con `zonas_usadas`) | la orden viva al abrir otro escenario; `puntos` da una zona por instante de toma | **No**: `puntos.get(t)` solo devuelve una zona en instantes fijos, y la orden de zona:1 no se llena (el precio no baja) | Nada; se corre en la fase 2 para confirmarlo |
| test_margen_lote.py:185 (`test_rechaza_al_llenar_si_el_margen_libre_bajo_desde_que_se_coloco`) | el bróker, sin cableado: la orden pasa a RECHAZADA y el evento llega a la traza | **No**: el bróker no cambia | Nada; D3b se prueba por el cableado en un test nuevo |
| test_margen_lote.py:333 (`test_con_no_operar_la_orden_que_no_cabe_no_se_envia_y_queda_anotada`) | el no envío queda en `no_enviadas` | **No**: el no envío sigue marcando usada y rechazada | Nada |
| test_cableado.py | no nombra ninguna de las tres cosas (grep); su `toca` sintético (`_sinteticas`, :139-176) liga zona:1 UNA vez por `zona_puesta` | **No** | Nada |
| test_caja_hasta_el_llenado.py:48 y :57 | zonas del productor con `zona_del_punto` y la cota de peticiones | **No** (no cierra nada) | Nada |

Ninguno cambia de resultado con la vía de 1.c: lo que comprobaban sigue siendo verdad con D1. Los
tests nuevos de la fase 2 van en `tests/unit/test_punto_usado.py`, por el cableado real
(`MotorCableado.correr_dia` con la spec real, como `_cadena` y `test_escenarios_por_sesion`) y con el
productor REAL de la zona en lo que decide (`toca_colocar_orden_limite` de `primitivas_zona`, con
`motor.limpia`), sustituyendo solo `zona_del_punto` por una geometría sintética que registra la zona
exactamente como la real (`puntos`, `punto_de_zona`, `_ligar_al_escenario`, `zonas`) y que dice en
cada test qué caja construye: la misma (mismo `nivel@inicio#extremo`, misma zona) u otra (otro
extremo, otra zona del mismo punto). Así el test falla en `main` por la razón que dice: la zona
sigue en `usadas` tras el stop, y el punto no está en `rechazados` tras el rechazo al llenar.

### 1.f (4.e) Lectura de material, declarada

Ninguna corrida en la fase 0. Lo que la sesión leyó hoy, declarado en `HOLDOUT-EXPOSICIONES.md`
(fila del 2026-10-18, fase 0): la traza commiteada del día dev 2026-07-13
(`anexos/VISOR-CONSTRUCCION/dias/2026-07-13.traza.txt`, sesión 11-15: órdenes, puntos, eventos),
las filas de 2026-07-13 de «### Ordenes» y «Eventos del broker» de la diaria de `main`
(`anexos/MARGEN-LOTE/`, sin las columnas en USD) y sus recuentos («ordenes: cancelada 299, llenada
179, rechazada 26»; «### Rechazos por motivo»; 4 sesiones con `detenido_por_cartuchos:si`); los
repartos solo por RECUENTO, con un guion de la carpeta de trabajo que no imprime claves y recibe la
raíz por argumento: `casos_reservados` 34 y `casos_ocultos` 34 (13 en 2026-05, 11 en 2026-06, 10 en
2026-09; **0 en los cuatro meses de construcción**, 2026-01, 04, 07 y 08); dos registros de
`knowledge/feedback/` de la sesión 1 (H6); `knowledge/evidence/` por `grep`. Ningún libro, ninguna
imagen, ningún fotograma, ninguna transcripción; nada de marzo, mayo, junio, septiembre ni febrero.
El auditor: solo el repo. Las corridas de las fases 1 y 4 leen el M1 entero de marzo y de junio para
calentar (como R3.1 y MARGEN-LOTE): cada una llevará su fila el día que corra y ANTES de correrla.
Ninguna salida ni este informe imprime fechas fuera de los días dev de construcción, salvo la
línea de cobertura del calendario de cierres.

### 1.g Lo que no pude medir

- La hora de cierre de la primera venta del 29 de abril (el xlsx no se lee para esto; LA-CAJA solo
  da las entradas). D1 no la necesita: la decisión es del consultor, provisional hasta V.
- Si alguna sesión de la corrida 2 reentra en un escenario nuevo con una zona del anterior (el
  límite de 1.c): se mide en la fase 4.
- El esfuerzo de `/model` desde dentro: lo dio el terminal de Aleks al empezar (cabecera).

### 1.h Las dos deudas del auditor del consultor (RN-019), verificadas

- **RN-019 no dispara nunca en el motor.** Su forma pide
  `se_cierra_operacion: {resultado: perdida, por: activacion_sin_ruptura}` (strategy_spec.yaml:1845);
  `_casa_por` compara por igualdad salvo `cualquier_*` (primitivas_broker.py:168-173); el `por` de
  cada cierre es el de su orden (`ctx.por_de_orden`, cableado.py:388), que es `z.por`
  (primitivas_broker.py:648) y en la vida de la orden stop es `PRIMER_ESQUEMA` siempre
  (zonas.py:399; ADR-0064:66-67). `grep activacion_sin_ruptura src/botsito/engine/*.py`: nada lo
  produce. En la corrida 2 de `main`, RN-019 no aparece en ninguna línea «Por sesion» (`grep -c
  RN-019` da 0; RN-016 19, RN-034 48). Y aunque disparara, la acción `reentrar` no está escrita en
  `src/` (grep vacío): sería `no_implementada`.
- **Su nota dice que A-31 lo pregunta** («Si el stop entero de una activacion sin ruptura gasta
  intento lo pregunta A-31», strategy_spec.yaml:1838-1839) **y A-31 está RESUELTA** desde el
  2026-09-29 (ambiguedades.yaml:817-819: «gastaría un intento», `fb-2026-09-29-sesion-03-d36ba0d2`);
  la nota de RN-016 ya lo recoge (:1705-1706). Las dos van a Technical Debt en las líneas preparadas
  (§6); esta rama no las arregla.

### 1.i Para ADR-0083: lo que el trader dijo, buscado antes de escribirlo

- A favor de D1: LA-CAJA-DEL-29-DE-ABRIL.md:236-243 (dos ventas en 1.17064 con stop 1.17079 a las
  07:55 y 07:58 UTC; la primera `rPnL -15`; «sería cuestión de poner otra reentrada aquí»);
  `fb-2026-09-09-sesion-01-fe4a6a5c` («para reentrar debe haber tocado el stop», vivo según
  `fb-2026-09-09-sesion-01-fae74396`); RN-018 («para que tú puedas entrar nuevamente o bien te ha
  tocado stop loss», `ev-v4-003710-c753f3d3`); ADR-0066:51 y RN-034 (tras una pérdida, un break even
  o un equal el escenario sigue con sus intentos: `ev-v3-002405-a202dbf6`, `ev-v4-004832-6543b551`),
  que hablan del escenario y no del punto (M8) y por eso no bastan solos.
- **Lo que la búsqueda en el corpus filtrado trajo** (`kb find` por «reentrada», «mismo nivel» y
  «equal»; oculta 4.631 segmentos y 2 items, como siempre): v6 1:23:45-1:24:07, capa corregida y
  filtrada (`corpus transcript show`, fuera de los dos tramos no citables de v6), tal como la da la
  capa: «[1:23:45] … después de un igual si [1:23:53] nos genera una pérdida nuevamente
  actualizamos a la siguiente o sea al siguiente nivel al mismo [1:23:59] mismo nivel como tal
  mantenemos o abrimos otro otra orden límite para poder reentrar si se da». Es el pasaje del
  equal que RN-019 ya cita (v6 1:22:25-1:23:19) unas líneas después. **Lectura nuestra, declarada**
  (a3 del revisor: la primera redacción lo daba por literal y por lo que D1 dice): el trader habla
  de un equal que acaba en pérdida y da dos salidas, actualizar al siguiente nivel o mantener o
  abrir otra orden límite en el mismo nivel para reentrar; D1 toma de ahí que la reentrada en el
  MISMO nivel tras una pérdida es una de las dos, no la única. No tiene item de evidencia propio
  (`knowledge/evidence/` está protegido en esta rama): ADR-0083 lo cita por instante, como RN-019,
  y V puede proponer el item. Y `ev-v5-000246-17eff9e1` («cuando hay un equal […] contarlo como
  pérdida pero reentrar nuevamente si es que el precio…», tema `reentrada.equal`).
- En contra: nada encontrado en `knowledge/feedback/` (el auditor) ni en el corpus filtrado (la
  sesión). La pregunta 3 de V sigue abierta: cuántas veces y con qué caja.
- Lo que P5 y P7 de CORRIDA-CONSTRUCCION.md §4.5 (:1216, :1225) dicen: P7 son entradas repetidas del
  trader en el mismo nivel que el bot toma UNA vez (3 filas); P5 «de más, mismo lado» (47) es el
  bot parándose y volviendo a entrar (93 stops frente a 12 objetivos en la corrida 2). D1 mueve
  parte de P7 hacia T0 o P5 y parte de P5 sigue: la fase 4 lo mide.

**La fase 0 no para**: a-e no contradicen el encargo y la PARADA de 4.a no se da. Lo que la fase 0
fija dentro de D1-D5, declarado: (1) «gastar el punto» es la marca por punto (`rechazados`); «usar
la zona» sigue siendo la marca por caja (`usadas`), que D1 no toca para las cancelaciones; (2) D1 se
aplica por RESULTADO del cierre (`salto_el_stop`, `break_even`, `perdida`, también en un cierre
MANUAL), nunca con `ganancia`; el «equal» del encargo es RN-019, que no dispara (1.h); (3) la vía es
la de 1.c; (4) el campo de la fase 1 lleva el punto Y el 1 de la caja (1.d: el stop no distingue dos
cajas).

## 2 · Fase 1 · El campo y la medida antes del cambio (2026-10-18)

### 2.a El campo, solo salida

«### Ordenes» lleva al final de cada línea DOS columnas nuevas, `punto` y `caja 1`
(`engine/cableado.py`, `CABECERA_ORDENES`, `FilaOrden`, `_punto_y_caja`): el punto de la orden (la
clave `nivel@inicio` de la vela contraria, la que el productor guarda en `punto_de_zona`) y el 1 de
su caja en precio; `-` en una zona sin productor. El encargo pedía solo el punto; **el 1 va también,
y es una desviación declarada**: el recuento que el mismo encargo pide («separando las de la misma
caja y las de otra») no se puede hacer con lo que ya traía la fila, porque el stop no distingue dos
cajas (§1.d: o12 y o13 de 2026-07-13 llevan el mismo stop con dos 1 distintos, por el redondeo de
`stop_fraccion_redondeo`). `TrazaBroker` guarda la zona de cada orden (`zona_de_orden`, el mismo
diccionario del contexto) y `vida_de_las_ordenes` lee la memoria del productor del día
(`MotorCableado.estados`). Régimen del campo `bloqueadas` de R3.1: ninguna decisión lo lee; test
sintético en los dos sentidos (`tests/unit/test_punto_usado.py`: con el productor real de la zona
y `zona_del_punto` sintético, la fila termina en `punto | caja 1`; con una zona sintética del
contexto, en `- | -`); `test_vida_de_la_orden.py` ajusta sus tres filas esperadas. Los guiones
cerrados que leen las filas lo hacen por índice desde el principio (`reentradas.py`,
`comun_visor.py:169`, `ticks_del_rechazo.py:49`, `traza_por_cierre.py:336`): no se desplazan.
`make check` sellado sobre ese árbol (commit e55d00a): 2679 passed, `SELLO`, `PICO DE MEMORIA de
make check: 295 MiB en test (…; el mayor proceso, 285 MiB)`. `state check`: 1592 funciones de test.

### 2.b La corrida «antes», con su fila de exposiciones antes

Fila de HOLDOUT-EXPOSICIONES del 2026-10-18 («Fase 1 de la rama `trabajo/punto-usado`»), escrita
antes del comando (el reloj de la máquina va en UTC-5: 22:00-23:00 del 18; `generado_el` del
manifiesto de la spec sale en UTC, ya el 19). Comando:

    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/antes-diaria.txt

→ `antes-diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (2.144
líneas; `TIEMPO: 356.3 s; MEMORIA: pico del proceso de 634.5 MiB`, por pantalla). sha256
`db5a3f886ecba830ebab09a0f25716e2746a1a2b7d1ff31f123955d7d37ad557`.

**Igual que la diaria de MARGEN-LOTE quitando el campo nuevo, medido:** un guion de la carpeta de
trabajo (`comparar_sin_campo.py`, no se commitea) quita a las filas de «### Ordenes» las dos
últimas columnas y a su cabecera sus dos nombres, y compara línea a línea con
`anexos/MARGEN-LOTE/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
(sha256 `e584077bf767818b97b3e7878024925bcbf017269e3112ab0d00aba89cef55e3`, el del encargo,
comprobado con `sha256sum`): **2.144 líneas en las dos y 0 líneas distintas**. Nada que parar.

**Determinismo:** la misma corrida repetida con `--salida` en la carpeta de trabajo (fuera del
repositorio; la misma lectura, declarada en la fila): `sha256sum` idéntico (`db5a3f88…`);
`TIEMPO: 300.3 s; MEMORIA: pico del proceso de 634.7 MiB`. La copia no se commitea.

### 2.c El recuento por punto exacto (`anexos/PUNTO-USADO/reentradas_por_punto.py`)

Recibe la salida por argumento, lee solo «### Ordenes», no escribe nada y no imprime las columnas
en USD. Por sesión: las órdenes colocadas en el punto EXACTO de una orden ya llenada de su sesión
(después del llenado), separadas por el 1 de la caja (la misma / otra), y las colocadas en el
punto de una ya rechazada. Salida con `--filas` en `anexos/PUNTO-USADO/reentradas_antes.txt`:

    ordenes colocadas en el punto exacto de una orden ya llenada de su sesion: 41, en 18 sesiones; con la misma caja: 0 (llenadas 0); con otra caja: 41 (llenadas 13)
    ordenes colocadas en el punto exacto de una orden ya rechazada de su sesion: 0, en 0 sesiones
    filas sin punto (zona sin productor): 0

Lo que dice de `main`: **ninguna reentrada con la misma caja y ninguna tras un rechazo**, que es
exactamente lo que la fase 0 midió en el código (la zona queda en `usadas`; el rechazo al llenar no
ocurre en esta corrida: «### Rechazos por motivo» solo trae `precio_invalido` al colocar, 26). Las
41 con otra caja (13 llenadas) son la E de VISOR §2.d.4 contada por el punto y no por el precio:
VISOR daba 47 en 22 sesiones por el 0 (cota superior); 6 órdenes en 4 sesiones eran un pivote
nuevo al mismo nivel. 2026-07-13 11-15 trae sus dos (o12 y o13 en el punto de o11, §1.d);
2026-04-29 07-11 no trae ninguna (el bot no reentra ahí: §4 lo mira).

## 3 · Fases 2 y 3 · Los tests en rojo sobre `main`, y el código, el ADR, la spec y los recuadros (2026-10-18)

### 3.a Los tests, primero en rojo (comparar-con-main)

`tests/unit/test_punto_usado.py` (13 tests; los dos del campo son de la fase 1), por el cableado
real: `MotorCableado.correr_dia` con la spec real y el productor real de la zona
(`toca_colocar_orden_limite` de `primitivas_zona`, con `motor.limpia`, y `_punto_nuevo` real),
RN-004 disparada en la toma por la geometría de toma sintética de `test_escenarios_por_sesion`,
los gates de geometría que no se prueban (RN-005, RN-009, el esquema) sintéticos como en
`test_cableado`, el acumulador `cartuchos` REAL y la orden STOP en la ruptura. Lo único sintético
de la geometría es `zona_del_punto` (`_geometria`, sustituido con `monkeypatch` en `zonas` y en
`primitivas_broker`): un plan «desde este cierre se ve el punto con este 1» que registra la zona
exactamente como la real (`puntos`, `punto_de_zona`, `_ligar_al_escenario`, `zonas` del día), de
modo que la misma caja es la misma zona y otro 1 es otra zona del mismo punto. Cada test dice en su
docstring qué caja construye.

Sobre el código de `main` (clon desechable `git worktree add --detach C:/cm/main main`, f96b581,
con su `config/settings.local.toml`; el fichero copiado dentro y `uv run pytest
tests/unit/test_punto_usado.py -q -p no:cacheprovider`; estado del repo real anotado antes y
después: un worktree ajeno de otra sesión, `…/2ea2c3d2…/scratchpad/wt-ci` en e7df30b, que ya
estaba y no se toca): **6 FAILED, 7 pasan**.

| Test | La caja que construye | En `main` | Por qué falla en `main` (la aserción) |
|---|---|---|---|
| `test_tras_una_perdida_el_mismo_punto_se_vuelve_a_colocar_con_la_misma_caja` (D3a) | la misma todo el día | **FAILED** | `assert ['o1'] == ['o1', 'o2']`: tras el stop no hay o2 (la zona sigue en `usadas`) |
| `test_tras_una_perdida_un_1_nuevo_coloca_otra_zona_del_mismo_punto` | otra desde el cierre siguiente al stop | pasa | — |
| `test_tras_un_break_even_el_mismo_punto_se_vuelve_a_colocar_igual_que_tras_la_perdida` | la misma | **FAILED** | `assert ['o1'] == ['o1', 'o2']` |
| `test_tras_una_ganadora_nada_se_vuelve_a_colocar` (RN-034) | otra desde Z+10 | pasa | — |
| `test_los_cartuchos_cortan_la_reentrada_al_agotarse` (RN-016) | un 1 nuevo en cada reentrada | pasa | — |
| `test_tras_un_rechazo_al_llenar_el_punto_no_se_vuelve_a_colocar_con_ninguna_caja` (D3b) | otra desde Z+6 | **FAILED** | `assert False` en `zonas.punto_rechazado(estado, "07-11", "zona:1")`: el rechazo al llenar no gastó el punto (y `main` coloca o2) |
| `test_el_rechazo_al_colocar_sigue_gastando_el_punto` | otra desde Z+4 | pasa | — |
| `test_el_no_envio_sigue_gastando_el_punto` | otra desde Z+4 | pasa | — |
| `test_con_la_posicion_abierta_no_se_coloca_otra_orden` (D4) | otra con la posición abierta | pasa | — |
| `test_con_la_orden_sin_llenar_el_1_nuevo_la_reubica_como_hoy` (RN-006) | otra en Z+2, sin llenar | pasa | — |
| `test_punto_nuevo_sigue_reconociendo_la_orden_de_la_sesion_tras_una_perdida` | la misma tras la pérdida, otra en Z+9 | **FAILED** | las peticiones: en `main` no existe la o2 de Z+7 (la misma caja); su o2 es la otra caja en Z+9, sin reubicación: `colocar o1, colocar o2, cancelar o2` (RN-035) frente a los cinco esperados (b3 del revisor: la primera redacción decía «falta colocar o2») |
| `test_la_fila_de_ordenes_lleva_al_final_el_punto_y_el_1_de_la_caja` (fase 1) | la misma | **FAILED** | la cabecera de `main` no lleva las columnas (es el campo de la fase 1, no D1) |
| `test_sin_productor_el_punto_y_la_caja_dicen_sin_medida` (fase 1) | zona sintética | **FAILED** | la fila de `main` no termina en `- \| -` (ídem) |

Dos rutas de precio salieron mal en el primer borrador y se corrigieron ANTES de fijar el rojo (el
objetivo de la otra caja está en +75, no en +60; el stop de la tercera caja de los cartuchos está
en -24): los dos tests que decían «pasa en los dos» fallaban en `main` por mi ruta, no por D1. Lo
digo porque el revisor tiene que comprobar que cada rojo lo es por la razón que dice.

Los tests de 4.d (§1.e), sin tocar, siguen pasando con el código nuevo: `test_orden_stop_pivote.py`,
`test_escenarios_por_sesion.py`, `test_margen_lote.py`, `test_cableado.py`,
`test_vida_de_la_orden.py`, `test_caja_hasta_el_llenado.py`, `test_arnes_motor.py` y
`test_be_al_tick.py`: 101 passed. Solo cambian dos comentarios de `test_orden_stop_pivote.py`
(«usada -su orden viva-, no se vuelve a colocar mientras nadie la libere» y la cita de ADR-0083).
En la rama, `test_punto_usado.py`: 13 passed.

### 3.b El código (D3), por la vía de §1.c

- `engine/zonas.py`: `liberar_usada` (nueva; `usadas.discard`), los docstrings del módulo
  (:41-49), de `marcar_usada` y de `marcar_rechazada` dicen qué gasta un punto; `__all__`.
- `engine/primitivas_broker.py`: `ContextoDia.sesion_de_orden` (orden → sesión en que se colocó),
  escrito en `colocar_orden_limite` junto a `zona_de_orden`; el comentario del no envío cita
  ADR-0083.
- `engine/cableado.py`: `_el_punto_tras_el_evento(ctx, estado)`, llamada en `correr_dia` justo
  después de `_a_la_cuenta` y antes de `estado.broker = broker.hechos()`: un evento `rechazada`
  (el rechazo al llenar) → `marcar_rechazada`; un cierre `stop`/`objetivo`/`manual` con resultado
  distinto de `ganancia` → `liberar_usada` de la zona de la orden de esa posición. Las órdenes sin
  sesión ni zona apuntadas (zonas sintéticas) no tocan nada. `_a_la_cuenta` no cambia de firma.
- `_punto_nuevo` no cambia (§1.c), y su test lo fija.

### 3.c ADR-0083, los recuadros, la spec y los docstrings (D2)

- `docs/adr/0083-que-gasta-un-punto.md` (D1 a D5, el material del trader en §6 -con lo que la
  fase 0 encontró: `fb-2026-09-09-sesion-01-fe4a6a5c`, v6 1:23:53-1:24:07,
  `ev-v5-000246-17eff9e1`-, y la respuesta a VISOR:673-675 sobre ADR-0066:51); recuadro en la
  decisión 1 de ADR-0064; nota en ADR-0074 §4; las tres filas del índice (0064, 0074 y la nueva
  0083, con «PROVISIONAL en D1 hasta la pregunta 3 de la sesión 5», H5). Los bloques
  `ids-inexistentes` del encargo y de este informe salen en este mismo commit.
- VISOR-CONSTRUCCION.md: diez recuadros de corrección, con fecha y rama, junto a todo lo que da la
  E por buena (los seis sitios del encargo, con uno solo antes de la tabla de §3.1 para sus dos
  filas, y los que el auditor añadió, H2): §2.d.4, :596 (2026-01-29 11-15), :861 (§2.g), §2.h
  (:887), antes de la tabla de §3.1, §3.2 pregunta 3, §3.3, la línea Y de §4.1 (que cubre las
  líneas preparadas de R3.2 y R3.4), :1203 y el Estado. El cuerpo queda intacto. (El mensaje del
  commit 56bbf91 dice «once»: a4 del revisor; son diez.) Tras el revisor (b1), los de §2.h, §3.3 y
  la línea Y dicen también las tres cosas que pide el encargo §3. La línea del Estado de R3.2 en la hoja de ruta va en las líneas del
  cierre (§6), porque `docs/plan/` está protegido en el contrato.
- `knowledge/spec/strategy_spec.yaml`: la descripción de `toca_colocar_orden_limite` pasa de «que
  la sesion no haya usado» a decir qué gasta un punto (ADR-0083). `spec_version` 18.1.1 → **18.1.2**
  (parche: cambia la redacción de un predicado, ninguna regla cambia de forma ni se añade un
  parámetro; lo que cambia el bot lo fija el ADR y el código, no la forma de la spec);
  `spec manifest --escribir` (hash `857d0b91…`) y `spec docs --escribir` (`docs/spec/`) en el mismo
  commit; trailer `Fuente: ADR-0083`. Tras el revisor (a1), la descripción dice también que una
  caja CANCELADA no vuelve (otra caja del mismo punto sí), igual que el docstring del módulo y el
  de `marcar_usada`: hash `94d004a7…`, manifest y docs regenerados, `spec_version` 18.1.2 → 18.1.3
  (`knowledge validate` exige subirla con cada cambio del hash, también dentro de la rama), trailer
  `Fuente: ADR-0083` en ese commit.

`make check` sellado sobre ese árbol (commit 56bbf91, que lleva también los resultados de la fase 1):
2690 passed, `SELLO`, `PICO DE MEMORIA de make check: 295 MiB en test (…; el mayor proceso,
285 MiB)`. `knowledge validate`: 0 errores (el trailer `Fuente: ADR-0083` en el commit; ADR-0083 ya
existe y los bloques `ids-inexistentes` salieron).

## 4 · Fase 4 · La re-corrida con ADR-0083 (2026-10-18)

Fila de HOLDOUT-EXPOSICIONES («Fase 4 de la rama `trabajo/punto-usado`») escrita antes de los
comandos. Los tres de R3.1 tal cual, salvo la carpeta de `--salida` (sobre el commit 56bbf91):

    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/PUNTO-USADO/arrastrada.txt
    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/diaria.txt
    uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/a35-inicio.txt

| corrida | TIEMPO | MEMORIA (pico) | líneas |
|---|---|---|---|
| 1 arrastrada | 504,3 s | 631,8 MiB | — |
| 2 diaria | 467,0 s | 634,2 MiB | 2.177 (antes 2.144) |
| 3 a35-inicio | 363,9 s | 634,1 MiB | — |

Es una corrida con `--diagnostico-*`: no cuenta ni habilita mayo (ADR-0070 §3; la salida lo dice:
«habilita medir el conjunto de medida (2026-05): no»), no decide ningún parámetro y no se mide
cobertura contra ningún umbral. Las corridas 1 y 2 corrieron en paralelo; la 3 y la repetición de
la 2, después.

### 4.a El recuento de la fase 1, antes y después (`reentradas_por_punto.py` sobre la corrida 2)

| | antes (§2.c) | después |
|---|---|---|
| órdenes en el punto exacto de una ya llenada de su sesión | 41, en 18 sesiones | **55, en 25 sesiones** |
| con la MISMA caja (llenadas) | 0 (0) | **14 (7)** |
| con otra caja (llenadas) | 41 (13) | 41 (13) |
| en el punto de una ya rechazada | 0 | 0 |

Salida con `--filas` en `anexos/PUNTO-USADO/reentradas_despues.txt`. Las 14 con la misma caja son
exactamente D3a: una por sesión, colocada en el cierre siguiente al stop de la llenada anterior
(2026-01-07 07-11, 01-14 07-11, 01-16 11-15, 01-20 11-15, 01-21 11-15, 04-03 07-11, 04-06 11-15,
04-07 07-11, 04-24 11-15, 07-02 11-15, 07-15 07-11, 08-11 11-15, 08-21 07-11 y 08-26 07-11); 7 se
llenan, 5 se cancelan (RN-006 las reubica con un 1 nuevo, o RN-035 a `ventana_fin`) y 2 se rechazan
por `precio_invalido` (el precio ya había pasado el punto al colocarla: el rechazo gasta el punto,
como antes). Las 41 con otra caja son las mismas 41 de antes. Nada tras un rechazo: el rechazo al
llenar no ocurre en estas corridas (`margen_libre` 0, como en MARGEN-LOTE §4.a), así que D3b solo lo
ejercita su test.

### 4.b Las órdenes, las peticiones por día y los rechazos por motivo, antes y después

| corrida 2 (diaria) | antes (`main` + campo, §2) | después (ADR-0083) |
|---|---|---|
| órdenes | 504: cancelada 299, llenada 179, rechazada 26 | **514**: cancelada 303, llenada **184**, rechazada 27 |
| no enviadas | 0 | 0 |
| rechazos por motivo | `precio_invalido` 26 (6, 8, 4, 8), todos al colocar | `precio_invalido` **27** (6, 8, 4, 9), todos al colocar; `margen_libre` 0 |
| peticiones al servidor (total; colocar / modificar / cancelar / rechazadas) | 858; 504 / 55 / 299 / 26 (enero 257, abril 251, julio 142, agosto 208) | **875**; 514 / 58 / 303 / 27 (enero 262, abril 257, julio 145, agosto 211) |
| día con más peticiones | 39 | 41 |
| sesiones con `detenido_por_cartuchos:si` | 4 | **6** |
| corrida 1 (arrastrada): órdenes | 124: cancelada 76, llenada 46, rechazada 2 (MARGEN-LOTE §4.a) | **120**: cancelada 74, llenada **44**, rechazada 2 (`precio_invalido`, enero) |
| corrida 3 (a35-inicio): órdenes | 494: cancelada 289, llenada 179, rechazada 26 | **504**: cancelada 293, llenada **184**, rechazada 27 |

(`anexos/PUNTO-USADO/peticiones_por_mes.py` y `sesiones_que_cambian.py`, que reciben las salidas por
argumento.) El rechazo nuevo por `precio_invalido` es o2 de 2026-08-21 07-11: la reentrada con la
misma caja, colocada cuando el precio ya había pasado el punto. +17 peticiones (+10 colocar, +3
modificar, +4 cancelar) y el día más cargado pasa de 39 a 41: lejos del tope de R13.

**Las 12 sesiones de la diaria cuyas órdenes cambian de recuento** (y las 2 en que cambia la caja
de una orden sin cambiar el recuento: 2026-01-07 07-11 y 2026-01-16 11-15, donde la reentrada con la
misma caja sustituye a la que antes iba con otra):

| sesión | antes | después | qué pasa |
|---|---|---|---|
| 2026-01-14 07-11 | 4 llenadas, 1 cancelada, 1 rechazada | 5 llenadas | o3 vuelve al punto de o2 con la misma caja y se llena; la tercera pérdida agota los cartuchos (`detenido_por_cartuchos`, nueva) |
| 2026-01-20 11-15 | 2 llenadas, 5 canceladas | 3 llenadas | o4 vuelve al punto de o3 (misma caja) y se llena |
| 2026-01-21 11-15 | 3 llenadas, 8 canceladas | 3 llenadas, 9 canceladas | o8 vuelve al punto de o7 (misma caja) y RN-006 la reubica |
| 2026-04-03 07-11 | 2 llenadas, 3 canceladas | + 1 rechazada | o4 vuelve al punto de o3 y el bróker la rechaza (`precio_invalido`): el punto queda gastado |
| 2026-04-06 11-15 | 1 llenada, 1 rechazada | 2 llenadas | o3 vuelve al punto de o2 (misma caja) y se llena; el rechazo de antes (otra caja, con el precio pasado) ya no ocurre |
| 2026-04-07 07-11 | 3 llenadas, 1 rechazada, 16 canceladas | + 1 cancelada | o6 vuelve al punto de o5 y RN-006 la reubica |
| 2026-04-24 11-15 | 2 llenadas | + 1 cancelada | o11 vuelve al punto de o10 y se cancela sin llenar |
| 2026-07-02 11-15 | 2 llenadas, 9 canceladas | 3 llenadas | o12 vuelve al punto de o11 (misma caja) y se llena; agota los cartuchos (nueva) |
| 2026-07-15 07-11 | 3 llenadas, 12 canceladas | + 1 cancelada | o4 vuelve al punto de o3 y RN-006 la reubica |
| 2026-08-11 11-15 | 3 llenadas, 1 cancelada | 4 llenadas | o4 vuelve al punto de o3 (misma caja) y se llena |
| 2026-08-21 07-11 | 2 llenadas | + 1 rechazada | o2 vuelve al punto de o1 y el bróker la rechaza (`precio_invalido`) |
| 2026-08-26 07-11 | 4 llenadas, 4 canceladas | + 1 cancelada | o2 vuelve al punto de o1 y RN-006 la reubica |

### 4.c Las sesiones con `detenido_por_cartuchos`, antes y después

Antes, las cuatro de VISOR-CONSTRUCCION.md §2.h: 2026-07-01 07-11, 2026-07-01 11-15, 2026-07-13
11-15 y 2026-08-26 07-11. Después, **las mismas cuatro más dos**: 2026-01-14 07-11 y 2026-07-02
11-15, las dos sesiones en que la reentrada con la misma caja se llena y pierde como tercer intento
(tabla de 4.b). Las cuatro de §2.h no cambian de resultado: 2026-07-13 11-15 sigue con o11, o12 y
o13 (tres 1 distintos: ninguna misma caja que añadir) y su rechazo o14; 2026-08-26 07-11 gana una
reentrada con la misma caja (o2 en el punto de o1) que RN-006 reubica antes de llenarse, y se agota
igual con sus cuatro llenadas. VISOR §2.h decía que «si Y se arregla, esas dos sesiones cambian»: no
cambian, porque Y se hizo al revés (recuadro allí).

### 4.d La tabla T0 y P1-P7 (`patrones.py` de R3.1 sobre la corrida 2), frente a MARGEN-LOTE.md §4.d

Salida completa en `anexos/PUNTO-USADO/patrones.txt` (364 filas, 104 sesiones con rn003;
MARGEN-LOTE: 359 filas, las mismas 104 sesiones).

| mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de más | P6 trader no operó | P7 repetidas | T0 pareja |
|---|---|---|---|---|---|---|---|---|
| enero | 7 (7) | 13 (13) | 26 (26) | 6 (6) | **43** (41) | 8 (8) | 0 (0) | 2 (2) |
| abril | 9 (9) | 4 (4) | 11 (11) | 6 (6) | 22 (22) | **21** (20) | 0 (0) | 5 (5) |
| julio (1-17) | 20 (20) | 9 (9) | 14 (14) | 14 (14) | **25** (24) | 2 (2) | 3 (3) | 7 (7) |
| agosto | 8 (8) | 7 (7) | 9 (9) | 14 (14) | 25 (25) | **20** (19) | 0 (0) | 4 (4) |
| **total** | **44 (44)** | **33 (33)** | **60 (60)** | **40 (40)** | **115 (112)** | **51 (49)** | **3 (3)** | **18 (18)** |

(entre paréntesis, MARGEN-LOTE.md §4.d.) **Las parejas no cambian (18) ni la cobertura (18/198,
9,1 %); la precisión BAJA de 18/162 (11,1 %) a 18/167 (10,8 %)**: cinco operaciones puntuables más
del bot y ninguna pareja nueva. Como pide el encargo, se dice y se explica por sesión, y no se
ajusta nada: las cinco son las reentradas con la misma caja que se llenan en una sesión que ya
tenía operaciones del bot (tabla de 4.b): 2026-01-14 07-11 y 2026-01-20 11-15 (P5, enero 41 → 43),
2026-07-02 11-15 (P5, julio 24 → 25), 2026-04-06 11-15 (P6, abril 20 → 21) y 2026-08-11 11-15 (P6,
agosto 19 → 20). Las otras dos llenadas con la misma caja (2026-01-07 07-11 y 2026-01-16 11-15)
sustituyen a una que antes iba con otra caja y no mueven la tabla. P7 sigue en 3, P5 «mismo lado»
pasa de 90 a 93.

**P5 y P7, aparte (la pregunta 3 de V).** P7 son las 3 entradas repetidas del trader en el mismo
nivel que el bot toma una vez (las tres de julio, CORRIDA-CONSTRUCCION.md §4.5); ADR-0083 no las
mueve: en esas tres sesiones el bot no reentra, porque su primera orden ahí no pierde en el stop
antes de la repetición del trader (o emparejó y ganó: RN-034). P5 «de más, mismo lado» (93) es el
bot parándose y volviendo a entrar, y ahora incluye las reentradas con la misma caja: lo que la
pregunta 3 tiene que preguntar es cuántas veces reentra el trader en el mismo punto tras un stop y
con qué caja (§5). **La corrida 1 (arrastrada)** cambia también, y se explica igual: antes 2 parejas,
cobertura 2/198 (1,0 %), precisión 2/44 (4,5 %); después las mismas 2 parejas, 2/198 y **2/44**; por
mes, P2 13 → 12, P3 24 → 22, P4 115 → 118, P6 7 → 5 (`anexos/PUNTO-USADO/patrones-arrastrada.txt`).
Con la cuenta arrastrada las reentradas de enero (2026-01-14, 01-20 y 01-23 ganan una llenada; 01-21
una cancelada) adelantan las pérdidas, la cuenta se suspende antes y **cuatro sesiones que antes
tenían órdenes se quedan sin ninguna** (2026-01-30 11-15, 04-01 11-15, 04-02 11-15 y 04-03 07-11):
46 → 44 llenadas. Es lo que R3.1 y MARGEN-LOTE ya decían de la arrastrada (corta en enero); nada de
eso cambia aquí.

### 4.e Lo que pasa el 29 de abril en el bot (corrida 2, sesión 07-11, día dev)

Igual antes y después. El trader vende dos veces en 1.17064, a las 07:55:40Z y 07:58:35Z (la
reentrada de LA-CAJA-DEL-29-DE-ABRIL.md:236-243). El bot: o1 en 1.17048 (07:11:59Z, punto
`117048@29624111`, 1 en 1.17071), que RN-006 reubica a o2 (07:12:59Z, el mismo punto con el 1 en
1.17072) y después a **o3 en 1.1706, OTRO punto (`117060@29624113`, 1 en 1.17072), llenada a las
07:14:06Z y cerrada por el stop (RN-012 dispara en la sesión)**, y ninguna orden más en la sesión: las dos ventas del trader quedan SIN PAREJA («bot
más cercano en la sesión: venta 07:14:06Z 1.1706, Δentrada -4 puntos, Δinstante -41/-44 min»; P3).
Tras el stop de o3 el bot NO reentra en su punto, ni antes ni después de ADR-0083, y tampoco en el
nivel del trader 41 minutos más tarde: el punto de o3 queda liberado, pero `toca_colocar` no vuelve a
dar SI en la sesión (la liquidez tomada y el último pivote contrario cambian con las velas que
siguen; la traza por cierre es la vía para decirlo, `anexos/VISOR-CONSTRUCCION/traza_por_cierre.py`,
y no se corre en esta rama). Así que **el ejemplo del 29 de abril no se ve en el bot como reentrada**:
va a V con la pregunta 3 tal cual (§5), con lo que el bot hace ahora cuando sí reentra (4.a y 4.b).

### 4.f La corrida 3 (a35-inicio) y el determinismo

La otra lectura de A-35 con la cuenta diaria da, como en R3.1, R1.2 y MARGEN-LOTE, **las mismas
parejas, cobertura y precisión que la corrida 2** (18/198, 9,1 %; 18/167, 10,8 %; antes 18/162), los
mismos rechazos (`precio_invalido` 27: 6, 8, 4, 9; antes 26), las mismas 6 sesiones con
`detenido_por_cartuchos:si`, el mismo recuento por punto (55 en 25 sesiones; 14 con la misma caja,
7 llenadas; 41 con otra) y la misma tabla T0 y P1-P7 (`anexos/PUNTO-USADO/patrones-a35-inicio.txt`);
184 llenadas (antes 179) y 293 canceladas (antes 289; la diaria, 303: `inicio_vela_contraria`
recoloca distinto, como ya decía MARGEN-LOTE §4.e).

**Determinismo:** la corrida 2 repetida con `--salida` fuera del repositorio (la misma lectura,
declarada en la fila de la fase 4): `sha256sum` idéntico
(`140e147947cdb99c7f880fb2e956320e6d98221a71fcd3824438d386194b01bf`); `TIEMPO: 370.1 s; MEMORIA:
pico del proceso de 633.9 MiB`. La copia no se commitea.

**El límite de §1.c** (una zona reutilizada en un escenario nuevo): no se mide en esta corrida
(haría falta la traza por cierre, que no se corre en esta rama). Lo que sí dice la salida: las 14
reentradas con la misma caja se colocan entre 21 s y 4 min 27 s después del llenado de la orden
anterior (`reentradas_despues.txt`, «colocada» frente al instante del llenado anterior), un tramo
corto para una toma nueva, pero no se afirma. Queda dicho en ADR-0083, Impacto, y **va a Technical
Debt** como tercera línea de §6 (a2 del revisor: es un riesgo que D1 abre y nadie mide).

## 5 · Lo que cambia para V (la sesión 5)

**La pregunta 3** («cuántas veces reentra el trader en la misma zona tras un stop», CORRIDA-CONSTRUCCION.md
§4.5) gana dos cosas: el **ejemplo del 29 de abril** (dos ventas en 1.17064 con el stop en 1.17079 a
las 09:55 y 09:58 de su reloj, la primera perdida en el stop; «sería cuestión de poner otra reentrada
aquí», LA-CAJA-DEL-29-DE-ABRIL.md:236-243), y **la caja de la reentrada: ¿la del primer intento o
una nueva?** (D5: esta rama no lo decide). Y la pregunta sigue necesitando el número: ¿una vez, dos,
hasta agotar los tres cartuchos?

**Lo que hace el bot tras esta rama**, para que el cuestionario lo enseñe tal cual: tras una pérdida o
un break even, en el cierre de M1 siguiente vuelve a colocar la orden stop en el MISMO punto, con la
caja que diga el productor en ese cierre (la misma si el 1 no cambió, otra si cambió: ADR-0074), con
RN-011 y RN-015 delante (sesgo, ruido de RN-005, RN-009, el margen) y con los cartuchos de RN-016; y
así hasta tres pérdidas por liquidez. Tras una ganadora no vuelve (RN-034). Un rechazo del bróker,
al colocar o al llenar, gasta el punto. En la construcción (corrida 2) eso son 14 reentradas con la
misma caja en 14 sesiones (7 llenadas) además de las 41 con otra caja que ya había; dos sesiones más
agotan los cartuchos (§4.c). El 29 de abril el bot no llega a reentrar: entra 41 minutos antes que el
trader, en otro punto, y tras su stop no vuelve a ver un punto en la sesión (§4.e).

Para la hoja de preguntas, en el reloj del trader (Europe/Madrid) y sin cifras en dinero:

> Pregunta 3 (reentradas). El 29 de abril, a las 09:55 vendiste en 1.17064 con el stop en 1.17079,
> perdiste en el stop y a las 09:58 volviste a vender exactamente en el mismo nivel con el mismo
> stop («sería cuestión de poner otra reentrada aquí»). ¿Cuántas veces reentras en el mismo punto
> tras un stop: una, dos, hasta agotar los tres cartuchos? ¿Y la caja de la reentrada es la del
> primer intento (el mismo stop) o la vuelves a trazar con lo que el precio hizo desde entonces?

## 6 · Líneas preparadas para el commit del contrato de la orden de cierre

Simuladas con `anexos/PUNTO-USADO/simular_cierre.py <raíz>` contra `test_hoja_de_ruta.py` (a, b y c)
y `test_project_state.py`, como VISOR-CONSTRUCCION: **a, b y c vacíos; las cuatro pruebas de
PROJECT_STATE pasan; 22.546 bytes simulados** con las tres deudas (22.182 con las dos del encargo;
hoy 22.026; tope 25.000). En el repo no escribe nada.

**Next Action** (`PROJECT_STATE.md`):

- **Y sale** a `docs/state/HISTORIA.md`, con su texto literal, bajo (el título lleva nombre porque ya
  hay una «# Next Action HECHA · Y ·» de `trabajo/adelgazar-estado`, HISTORIA.md:7130):

      # Next Action HECHA · Y · qué gasta un punto · sale de PROJECT_STATE.md en trabajo/punto-usado (2026-10-18)

      Y. Que el punto de una orden ya llenada no se vuelva a colocar con otra caja (ADR-0064, decisión 1): hoy se marca la zona y no el punto; en la corrida 2, hasta 47 órdenes en 22 sesiones van al 0 de una ya llenada (VISOR-CONSTRUCCION.md §2.d.4). Rama de código, con su test y la corrida 2 repetida.

      La hace `trabajo/punto-usado` (docs/validation/PUNTO-USADO.md; ADR-0083, que la rehizo en el sentido contrario al de esta línea: el llenado no gasta el punto).

- **F queda en:**

      F. J → V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno ni a J ni a V.

- **V cambia:** «y las preguntas de VISOR-CONSTRUCCION.md §3.2. Depende de R1.1, de R3.1, de Y, de J
  (kit hoja) y de la copia de seguridad (A.4).» pasa a «las preguntas de VISOR-CONSTRUCCION.md §3.2;
  y la pregunta 3 con el ejemplo del 29 de abril y la caja de la reentrada (PUNTO-USADO.md). Depende
  de R1.1, de R3.1, de J (kit hoja) y de la copia de seguridad (A.4).»

**Technical Debt** (`PROJECT_STATE.md`), dos líneas nuevas al principio de la lista:

    - RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden stop lleva `por = primer_esquema` (zonas.py); nada produce ese `por`, y la acción `reentrar` no está escrita (PUNTO-USADO.md §1.h).
    - La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta, y A-31 está RESUELTA desde el 2026-09-29 (PUNTO-USADO.md §1.h).
    - Una zona del productor reutilizada en un escenario nuevo (misma caja del mismo punto tras una toma nueva) sigue ligada al escenario en que nació y sus cierres cuentan en los cartuchos de aquel (zonas.py, `zona_del_punto` liga solo al crearla); ADR-0083 lo hace alcanzable y la fase 4 no lo midió: hace falta la traza por cierre (PUNTO-USADO.md §1.c y §4.f).

(La tercera no la pedía el encargo: la trae a2 del revisor, y las tres caben: la simulación da
22.546 bytes.)

**Hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`; `docs/plan/` está protegido en el contrato, por eso
van aquí):

- **R3.4** cambia de título y de «Qué es», gana `ID:ADR-0083` en sus Refs (H4) y pasa a HECHA:

      ### R3.4 · Qué gasta un punto: el rechazo y el no envío, no el llenado
      - **Refs:** NA:Y · ID:ADR-0083 · ID:ADR-0064 · ID:ADR-0074
      - **Qué es:** fijar por ADR qué gasta un punto (ADR-0083, que enmienda la decisión 1 de
        ADR-0064): el rechazo del bróker -al colocar o al llenar- y el no envío lo gastan; el
        llenado no, y tras una pérdida o un break even el mismo punto se vuelve a colocar, con la
        misma caja o con otra; el código lo cumple, con tests que rompen en `main`, y la corrida 2
        repetida.
      - **Depende de:** R3.2 (HECHA).
      - **Quién:** la sesión, con el encargo del consultor.
      - **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está repetida
        con los tres comandos de R3.1.
      - **Estado:** HECHA (`trabajo/punto-usado`; PUNTO-USADO.md): ADR-0083; `liberar_usada` y el
        rechazo al llenar gasta el punto, por el cableado; 13 tests por el cableado real (4 rompen
        en `main` por D1); la corrida 2 repetida con los tres comandos de R3.1 (§4). PROVISIONAL en
        D1 hasta la pregunta 3 de la sesión 5 (R4.1).

- **R4.1:** `NA:Y` sale de los Refs («NA:V · NA:Y · ID:RN-004» → «NA:V · ID:RN-004») y «R3.4 (NA:Y)»
  pasa a «R3.4 (HECHA)» en «Depende de».
- **R3.2, Estado** (H2 del auditor): «Una E (la reentrada en un punto ya llenado: R3.4)» pasa a «Una
  E (la reentrada en un punto ya llenado: R3.4, que ADR-0083 rehízo en el sentido contrario: el
  llenado no gasta el punto)».

## 7 · El encargo, punto por punto

Requisitos numerados (cada fase, cada viñeta, cada «test que rompe», cada «NO cambia»), con
Hecho / Parcial / No hecho / Hecho de otra forma y su evidencia (b2 del revisor: la primera versión
iba agrupada por punto del encargo).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base main f96b581, origin/main, el tag, ninguna otra rama | Hecho | §0 |
| 2 | La CI de main con `gh`, nunca curl ni guion | Hecho | §0; el revisor lo repitió |
| 3 | abrir-rama: encargo tal cual, contrato, Archivo en HISTORIA; tramo R3 | Hecho | 09fe2cc; Archivo 38 |
| 4 | Informe y anexos en su ruta | Hecho | contrato.yaml |
| 5 | Skills fase-cero (con el auditor), comparar-con-main, entregar-rama | Hecho | §1.a; §3.a; §9 |
| 6 | /model: Fable 5.1, esfuerzo alto | Hecho | cabecera |
| 7 | Verificar en la fase 0 las dos cosas del punto 1 | Hecho | §1.b |
| 8 | 4.a: todos los caminos de fin de orden, con fichero:línea; PARADA si D1 cambia más que los dos de D3 | Hecho | §1.b (tabla); la PARADA no se da |
| 9 | 4.b: la vía, y `_punto_nuevo` con su test | Hecho | §1.c; `test_punto_nuevo_sigue_reconociendo…` |
| 10 | 4.c: la traza de 2026-07-13 11-15 | Hecho | §1.d |
| 11 | 4.d: los tests que dependen, cuáles cambian y cómo se rehacen | Hecho | §1.e: ninguno cambia de resultado; dos comentarios |
| 12 | 4.e: la lectura declarada el mismo día y antes de cada corrida | Hecho | filas del 2026-10-18 en HOLDOUT-EXPOSICIONES (fase 0, fase 1, fase 4) |
| 13 | D1 en el código (gasta: rechazo al colocar o al llenar, no envío; no gastan: reubicación ni llenado; RN-034 no cambia) | Hecho | §3.b; cableado.py `_el_punto_tras_el_evento`; zonas.py `liberar_usada` |
| 14 | D2: ADR-0083 con sus cinco citas, recuadro en ADR-0064, nota en ADR-0074 §4 | Hecho | ADR-0083 §6; diff de 0064 y 0074; índice |
| 15 | D2: docstrings de zonas.py (:41-45 y `marcar_usada`) | Hecho | zonas.py; tras a1, también lo de las cajas canceladas |
| 16 | D2: la descripción de `toca_colocar_orden_limite`, spec_version, manifest, docs, `Fuente: ADR-0083` | Hecho | 18.1.1 → 18.1.2 (56bbf91) → 18.1.3 (el commit del revisor, a1) |
| 17 | D3a: test que rompe en main (misma caja tras una pérdida) | Hecho | §3.a (FAILED en main: `['o1'] == ['o1','o2']`); pasa en la rama |
| 18 | D3b: test que rompe en main (el rechazo al llenar gasta) | Hecho | §3.a (FAILED en main en `punto_rechazado`); pasa en la rama |
| 19 | D4: un test por el cableado | Hecho | `test_con_la_posicion_abierta_no_se_coloca_otra_orden` |
| 20 | D5: la reentrada por la vía normal, sin decidir la caja | Hecho | sin cambios en `caja_bloque` ni `caja_se_fija` |
| 21 | NO cambia: reubicación, geometría, sesgo, ventana, lote y límite, RN-034, cartuchos, ninguna cifra | Hecho | `git diff --name-status`: en `src/` solo cableado, primitivas_broker y zonas; ninguna cifra |
| 22 | Recuadros en VISOR junto a todo lo que da la E por buena, diciendo las tres cosas | Hecho (de otra forma: diez sitios en vez de seis, H2; tras b1, los tres que no decían lo del consultor lo dicen) | §3.c |
| 23 | NO tocar cases, holdout, guardias, .claude, Makefile | Hecho | diff |
| 24 | PROJECT_STATE solo con lo del ritual (21.911 bytes en main) | Hecho | 22.026 bytes: rama, feature, recuento de tests y Archivo 38 |
| 25 | Si el clasificador niega un comando, PARADA | Hecho (no se dio) | la guardia negó `kb at` y comandos compuestos; se partieron, no se rodearon (§1.f) |
| 26 | Fase 1: el campo al final de «### Ordenes», solo salida, test en los dos sentidos | Hecho de otra forma (declarado) | dos columnas, `punto` y `caja 1` (§2.a) |
| 27 | Fase 1: make check sellado | Hecho | e55d00a (§8) |
| 28 | Fase 1: la corrida «antes» igual a la diaria de MARGEN-LOTE quitando el campo (sha256 del encargo) | Hecho | §2.b: 0 líneas distintas; sha256 de MARGEN-LOTE = e584077b…; el revisor lo repitió por su cuenta |
| 29 | Fase 1: la repetición fuera del repo (determinismo) | Hecho | §2.b: sha idéntico db5a3f88… (la copia está en la carpeta de trabajo, no en el repo: el revisor no pudo verla) |
| 30 | Fase 1: guion en los anexos por argumento, por punto exacto y por sesión, misma caja / otra, tras un rechazo | Hecho | `reentradas_por_punto.py`; §2.c |
| 31 | Fase 2: tests primero, en rojo sobre main con comparar-con-main, recuento de FAILED, por el cableado real, cada test dice su caja | Hecho | §3.a: 6 FAILED de 13; clon `--detach` retirado |
| 32 | Fase 2: las diez viñetas de tests (D3a, 1 nuevo, break even, ganadora, cartuchos, D3b, rechazo al colocar y no envío, D4, reubicación, 4.d) | Hecho | 13 tests (§3.a) |
| 33 | Fase 3: código, ADR, recuadros, docstrings, spec; tests en verde; make check sellado | Hecho | 56bbf91 |
| 34 | Fase 4: la fila de exposiciones antes de correr | Hecho | el revisor lo contrastó por horas de modificación (eje a) |
| 35 | Fase 4: los tres comandos tal cual, y la repetición de la 2 fuera del repo | Hecho | §4; sha idéntico 140e1479… |
| 36 | Fase 4: recuento de la fase 1 antes y después; órdenes, peticiones por día y rechazos; sesiones con cartuchos (las cuatro de §2.h); T0 y P1-P7 frente a MARGEN-LOTE §4.d con P5 y P7 aparte; el 29 de abril; si cambian parejas o precisión, explicar por sesión | Hecho | §4.a-4.e; la precisión baja de 11,1 % a 10,8 %, explicada por sesión; nada se ajusta |
| 37 | PICO DE MEMORIA de cada make check; test_nunca_bloquea | Hecho | §8; no falló |
| 38 | §6: encargo frente a lo hecho; fase 0 y medidas; lo que cambia para V; las dos deudas; líneas del cierre simuladas | Hecho (de otra forma: una tercera deuda, a2) | §1, §5, §6, §7 |
| 39 | §7: el revisor (opus) con los dos ejes y las tres comprobaciones extra; su informe pegado con lo arreglado y lo declarado | Hecho | §9 |
| 40 | §8: CI si toca la plataforma; si no, decirlo con la lista de ficheros | Hecho | §8: no la toca |
| 41 | «Rama lista para revisión, NO cerrada» | Hecho | Estado |

Desviaciones declaradas, en una línea cada una: (26) dos columnas en vez de una; (22) diez
recuadros en vez de seis, y la línea de la hoja de ruta al cierre; (38) una tercera deuda; (33) los
resultados de la fase 1 van en el commit de las fases 2 y 3, porque el sello cubre el árbol
estadiado entero; el bloque `ids-inexistentes` desde el primer commit; las dos rutas de precio
corregidas antes de fijar el rojo; D1 aplicada por resultado, también al cierre manual.

## 8 · make check, memoria y CI

| make check | árbol | resultado | PICO DE MEMORIA |
|---|---|---|---|
| apertura, 1.º | encargo con ADR-0083 sin bloque | ROJO: 5 failed (ids), 2672 passed | — |
| apertura, 2.º (09fe2cc) | 1f69292… | 2677 passed, SELLO | 295 MiB en `test` (el mayor proceso, 284 MiB) |
| fase 0 (71c8d46) | 641b8a5… | 2677 passed, SELLO | 296 MiB (286 MiB) |
| fase 1 (e55d00a) | ade5be5… | 2679 passed, SELLO | 295 MiB (285 MiB) |
| fases 1-3 (56bbf91) | d5f7e74… | 2690 passed, SELLO | 295 MiB (285 MiB) |
| fase 4 y el informe (cf994a7) | c7310ad… | 2690 passed, SELLO | 295 MiB (285 MiB) |
| el revisor y sus arreglos (el último commit) | el árbol estadiado de ese commit | su `SELLO` y su `PICO DE MEMORIA` quedan en `make-check.log` y en el mensaje final a Aleks: el informe que sella no puede llevar la cifra de su propio sello | — |

`test_nunca_bloquea_y_es_rapido` no falló por tiempo en ninguno. `state check`: 1603 funciones de
test (1590 en `main`; +2 de la fase 1, +11 de la fase 2).

**CI de Linux: no hace falta.** La rama no toca hooks, rutas ni el sistema de archivos. Ficheros que
cambia frente a `main` (`git diff --stat main...HEAD`): `PROJECT_STATE.md`, `contrato.yaml`,
`docs/adr/0064-…`, `docs/adr/0074-…`, `docs/adr/0083-que-gasta-un-punto.md`, `docs/adr/README.md`,
`docs/encargos/trabajo-punto-usado.md`, `docs/spec/{ambiguedades,glosario,parametros,reglas}.md`,
`docs/state/HISTORIA.md`, `docs/validation/{HOLDOUT-EXPOSICIONES,PUNTO-USADO,VISOR-CONSTRUCCION}.md`,
`docs/validation/anexos/PUNTO-USADO/*` (salidas, guiones y recuentos),
`knowledge/spec/{spec_manifest,strategy_spec}.yaml`, `src/botsito/engine/{cableado,primitivas_broker,zonas}.py`,
`tests/unit/{test_orden_stop_pivote,test_punto_usado,test_vida_de_la_orden}.py`. Ni `.claude/`, ni
`Makefile`, ni `scripts/`, ni `config/`.

**El clon de `main`** (`C:/cm/main`, `git worktree --detach`) se retiró con `git worktree remove
--force` (tenía el test copiado y su `settings.local.toml`) antes de sellar la fase 4; el worktree
ajeno de otra sesión (`…/2ea2c3d2…/scratchpad/wt-ci`, e7df30b)
estaba antes y no se toca. Estado del repo real antes y después: `main` y `trabajo/punto-usado`,
129 tags, nada nuevo en origin.


## 9 · El revisor

Lanzado sobre la rama con el informe terminado (commit cf994a7 más la fila de §8 sin commitear), con
los dos ejes de siempre y las tres comprobaciones del encargo §7. Su informe, pegado tal cual (no
cita ningún tramo no citable: ninguna retirada). Debajo, lo que se hizo con cada hallazgo.

### 9.1 Informe del revisor (opus), tal cual

## Informe del revisor · trabajo/punto-usado · 2026-10-19

Base `main` f96b581 (merge-base). Revisé los commits 09fe2cc, 71c8d46, e55d00a, 56bbf91 y cf994a7, y también la edición sin commitear de `docs/validation/PUNTO-USADO.md` (§8: cambia `[MC5] [MC5R] [MC5P]` por la fila real de cf994a7).

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 4 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | La spec y los docstrings dicen menos de lo que hace el código. La spec dice que una caja se bloquea solo si está «gastado ni con orden viva». El docstring dice «la zona queda usada mientras la orden vive», y el comentario del test, «usada -su orden viva-». Pero una zona CANCELADA (RN-035, RN-036, `se_retira`, ventana de ADR-0068, fin de día) se queda en `usadas` para siempre: esa caja no vuelve aunque no tenga orden viva ni punto gastado. El propio ADR y el informe lo dicen bien. | `knowledge/spec/strategy_spec.yaml:275-276` («que la sesion no tenga gastado ni con orden viva»); `src/botsito/engine/zonas.py:44` y `:425-428`; `tests/unit/test_orden_stop_pivote.py:190`; en contra: `docs/adr/0083-que-gasta-un-punto.md:45-48` («deja su caja usada y su punto sin gastar […] esa caja no vuelve») y PUNTO-USADO.md:146-147 («o terminó sin liberar el punto»). `_el_punto_tras_el_evento` (`cableado.py:140-167`) solo libera la zona en un cierre sin ganancia. |
| a2 | importa | ADR-0083 (fichero nuevo de la rama, todavía editable) afirma dos cosas que la medida de la fase 4 contradice o no hizo, y no se corrigió después de medir. (1) «Este ADR mueve parte de P7»: P7 sigue en 3 y el informe dice «ADR-0083 no las mueve». (2) «se mide en la fase 4» (el límite de una zona reutilizada en un escenario nuevo): el informe dice que no se midió, y no lo lleva a Technical Debt («no es una deuda abierta mientras no se mida»). Es un riesgo que abre el propio cambio de D1 (PUNTO-USADO.md:157: «con D1 lo es en teoría»). | `docs/adr/0083-que-gasta-un-punto.md:126-127` y `:173-174`; PUNTO-USADO.md:554-557, `:599-604`; `anexos/PUNTO-USADO/patrones.txt` «total \| … \| 3 \| 18» frente a `anexos/MARGEN-LOTE/patrones.txt:7» «… \| 3 \| 18» |
| a3 | importa | La cita de v6 «1:23:53-1:24:07» no sostiene del todo lo que se le hace decir. (1) «después de un igual si» está en el segmento de 1:23:45.730, fuera del rango citado. (2) No es literal: la capa dice «al mismo / mismo nivel» y «otro otra orden límite». (3) El informe la resume como «dice lo que D1 dice: tras la pérdida, la reentrada en el MISMO nivel». Pero el pasaje habla de un equal y dice además «actualizamos a la siguiente, o sea al siguiente nivel». Es una LECTURA del pasaje y no se declara como tal. | `uv run botsito corpus transcript show --video v6 --t0 1:23:50 --t1 1:24:10` → `[1:23:45.730] … después de un igual si` / `[1:23:53.250] nos genera una pérdida nuevamente actualizamos a la siguiente o sea al siguiente nivel al mismo` / `[1:23:59.550] mismo nivel como tal mantenemos o abrimos otro otra orden límite para poder reentrar si se da`; PUNTO-USADO.md:265-272; ADR-0083:115-118 |
| a4 | importa | Se dice «once recuadros» en VISOR-CONSTRUCCION y hay diez. La lista del propio informe también enumera diez. | `Grep "RECUADRO DE CORRECCIÓN \(2026-10-18"` en VISOR-CONSTRUCCION.md → líneas 598, 666, 875, 907, 916, 965, 995, 1049, 1255 y 1486 (10); PUNTO-USADO.md:426 y `:698`; cuerpo del commit 56bbf91 («once recuadros de correccion») |
| a5 | menor | §4.e dice «o1 y o2 en 1.17048 […] reubicadas por RN-006 con un 1 nuevo». o2 no se reubica con un 1 nuevo: o3 está en OTRO punto. | diaria de la fase 4, :1858-1859: o2 `117048@29624111`, o3 `117060@29624113`; PUNTO-USADO.md:572-573 |
| a6 | menor | Dos recuadros van dentro de una lista y la línea siguiente empieza por «- » sin línea en blanco: en el renderizado quedan pegados a la viñeta siguiente. El cuerpo sigue intacto. | VISOR-CONSTRUCCION.md:875-878 → :879 «- **Uno de los ocho…»; :1255-1258 → :1259 «- **Las páginas…» |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` → «CONTRATO: 36 ficheros dentro del contrato de trabajo/punto-usado (riesgo alto, artefacto docs/validation/PUNTO-USADO.md, tramo 'R3', 5 comprobaciones para el revisor)», exit 0.
- **pytest de las comprobaciones del contrato.** `uv run pytest tests/unit/test_punto_usado.py tests/unit/test_orden_stop_pivote.py tests/unit/test_escenarios_por_sesion.py tests/unit/test_margen_lote.py tests/unit/test_cableado.py -p no:cacheprovider` → «84 passed». También `test_adr.py` y `test_vida_de_la_orden.py` → «13 passed», y `test_historia.py test_project_state.py test_hoja_de_ruta.py test_contrato_rama.py` → «47 passed».
- **`make check`.** No lo lancé (escribe). `make-check.log`: «2690 passed», «SELLO: make check en verde sobre el arbol c7310ada3a8e…» y «PICO DE MEMORIA de make check: 295 MiB en `test` (…; el mayor proceso, 285 MiB)». `git rev-parse HEAD^{tree}` da c7310ada…: el sello es el de cf994a7.
- **`knowledge validate` y `spec docs --escribir`.** No los lancé (escriben). El paso `knowledge` del mismo log trae todo OK: «657 documentos: todo id citado existe…», «hash del manifiesto al dia».
- **Trailer `Fuente:`.** El único commit que toca `knowledge/spec` es 56bbf91: lleva `Fuente: ADR-0083` en el cuerpo y ADR-0083 existe.
- **Regímenes.** La rama no toca evidence, feedback, manifests, transcripciones, fotogramas, libros.yaml, ambiguedades.yaml ni `knowledge/cases`. HOLDOUT-EXPOSICIONES y HISTORIA solo añaden líneas (numstat 3/0 y 184/0).
- **ADR.** ADR-0083: `## Estado` empieza por `ACTIVE`; sus secciones y su fila del índice están; test_adr en verde. El recuadro de ADR-0064 va junto a la decisión 1. La nota de ADR-0074 va en §4, que ya nombraba «la decisión 1 de ADR-0064» entre lo que no cambia.
- **VISOR-CONSTRUCCION.md.** `git diff -U0 main...HEAD` solo trae líneas `+>` o en blanco: el cuerpo está intacto y cada recuadro lleva fecha y rama.
- **Holdout y material.** Hay filas de las fases 0, 1 y 4. La de la fase 4 es anterior a las corridas: HOLDOUT-EXPOSICIONES.md modificado a las 23:19:05; diaria y arrastrada terminan a las 23:27:05 y 23:27:42 tras 467,0 s y 504,3 s, es decir, empiezan hacia las 23:19:18.
- **Fechas reservadas.** Ni el informe, ni el ADR, ni los anexos traen fechas de días reservados. Grep `2026-(02|03|05|06|09)-dd` y `2026-07-(18..31)`: solo ids de sesión y de feedback. Las únicas fechas de 2025 o posteriores a 2026-10 son la línea de cobertura del calendario.
- **Cifras.** Ninguna cifra nueva en código.
- **Ninguna `cita` nueva en la spec**, así que no aplican las tres guardias.
- **Citas contrastadas contra su fuente:** LA-CAJA-DEL-29-DE-ABRIL.md:236-243, `fb-2026-09-09-sesion-01-fe4a6a5c`, `fb-…-fae74396`, `ev-v5-000246-17eff9e1`, ADR-0064:79-81, A-31 en ambiguedades.yaml:812-819, la nota de RN-019 y `operaciones_simultaneas_max`. Todas correctas.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 2 menor. Requisitos: 35 hechos, 1 parcial, 1 no hecho (el revisor, pendiente por diseño), 1 hecho de otra forma (declarado) y 2 que no pude comprobar.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main, origin/main, tag, ninguna otra rama | Hecho | PUNTO-USADO.md:18-21; `git branch --list` → main y trabajo/punto-usado |
| 2 | CI de main con gh, nunca curl ni guion | Hecho | Repetí `gh run view 39186492700 --json …` → `"conclusion":"success","headSha":"f96b581…"`. En `git diff main...HEAD` solo aparece «curl» en el encargo y en las dos menciones «ni curl ni guion». Los guiones de los anexos no traen curl, subprocess, urllib ni requests |
| 3 | abrir-rama: encargo, contrato y Archivo | Hecho | `A contrato.yaml`, `A docs/encargos/trabajo-punto-usado.md`, HISTORIA «# Archivo 38 · PROJECT_STATE.md de main en f96b581» |
| 4 | Tramo R3; informe y anexos en su ruta | Hecho | contrato.yaml:3-4 |
| 5 | Skills: fase-cero con el auditor, comparar-con-main | Hecho | §1.a y §3.a. El clon C:/cm/main ya no está: en `.git/worktrees` solo queda `wt-ci` |
| 6 | /model | Hecho | PUNTO-USADO.md:6-7 |
| 7 | Verificar en la fase 0 las dos cosas del punto 1 | Hecho | §1.b |
| 8 | 4.a todos los caminos de fin de orden; sin PARADA | Hecho | §1.b, tabla :83-95 |
| 9 | 4.b la vía y `_punto_nuevo` con su test | Hecho | §1.c; test_punto_usado.py:423-447 |
| 10 | 4.c la traza del 2026-07-13 | Hecho | §1.d |
| 11 | 4.d los tests que dependen, rehechos | Hecho | §1.e: ninguno cambia de resultado y solo se tocan comentarios. Declarado |
| 12 | 4.e la lectura declarada | Hecho | Filas de HOLDOUT-EXPOSICIONES |
| 13 | D1 en el código | Hecho | cableado.py:140-167, :296; primitivas_broker.py:147-149, :653; zonas.py `liberar_usada` |
| 14 | D2: ADR-0083, recuadro en ADR-0064, nota en ADR-0074 §4, las cinco citas | Hecho | ADR-0083 §1 y §6; diff de 0064 y 0074 |
| 15 | D2: docstrings de zonas.py | Hecho | Con la imprecisión de a1 |
| 16 | D2: spec, spec_version, manifest, docs, Fuente | Hecho | 18.1.1 → 18.1.2; hash 857d0b91…; docs/spec/* |
| 17 | D3a: test que rompe en main | Hecho (razonado) | En main, `toca_colocar_orden_limite` niega con `z.id in zonas_usadas(...)` (`git show main:src/botsito/engine/zonas.py` :473) y nada libera la zona. La aserción del test es `list(ordenes) == ["o1","o2"]` (:203) |
| 18 | D3b: test que rompe en main | Hecho (razonado) | En main nadie llama a `marcar_rechazada` con el rechazo al llenar. La primera aserción que falla es `zonas.punto_rechazado(...)` (:333), como dice §3.a |
| 19 | D4: un test por el cableado | Hecho | test_punto_usado.py:383-397 |
| 20 | D5 | Hecho | Sin cambios en caja_bloque ni caja_se_fija |
| 21 | No tocar broker.py, arnes.py, geometría, sesgo, lote ni cifras | Hecho | `git diff --name-status`: solo cableado, primitivas_broker y zonas en `src/` |
| 22 | Recuadros en VISOR con lo que el encargo dice que «dicen» | Parcial | Ver b1 |
| 23 | No tocar cases, holdout, .claude ni el Makefile | Hecho | diff |
| 24 | PROJECT_STATE solo con el ritual (21.911 bytes en main) | Hecho | `git show main:PROJECT_STATE.md \| wc -c` → 21911; el diff solo cambia rama, feature, recuento y Archivo 38 |
| 25 | Fase 1: el campo al final, solo salida, test en los dos sentidos | Hecho de otra forma (declarado) | Dos columnas en vez de una (§2.a, con su motivo); tests en :453-481 |
| 26 | Fase 1: make check sellado | Hecho | §2.a y §8 (e55d00a) |
| 27 | Fase 1: la corrida «antes» igual a MARGEN-LOTE quitando el campo | Hecho (lo verifiqué) | sha256 de MARGEN-LOTE = e584077b… (el del encargo); `diff` → un solo bloque «1540,2044c1540,2044» (la sección «### Ordenes»); cortando las 15 primeras columnas, las 504 filas dan el mismo sha256 (d3acc1d9…) en los dos ficheros |
| 28 | Fase 1: la repetición fuera del repo | No comprobable | Ver abajo |
| 29 | Fase 1: guion por argumento, por punto exacto y por sesión, misma caja y otra, tras un rechazo | Hecho | reentradas_por_punto.py; salidas «41, en 18 sesiones; misma caja 0» y «55, en 25; misma caja 14 (llenadas 7)» |
| 30 | Fase 2: en rojo sobre main con comparar-con-main, recuento en el informe | Hecho | §3.a: 6 FAILED de 13 |
| 31 | Fase 2: las diez viñetas de tests | Hecho | Los 13 tests cubren todas |
| 32 | Fase 3: tests en verde y make check sellado | Hecho | 56bbf91 |
| 33 | Fase 4: la fila antes de correr | Hecho | Horas de modificación (ver eje a) |
| 34 | Fase 4: los tres comandos tal cual | Hecho | §4:449-451 |
| 35 | Fase 4: la repetición de la 2 fuera del repo | No comprobable | Ver abajo |
| 36 | Fase 4: contenido del informe (recuento, órdenes, peticiones, rechazos, cartuchos, T0/P1-P7, P5 y P7 aparte, 29 de abril) | Hecho | §4.a-4.e. Cifras contrastadas con los anexos: 55/14/41, 6 `detenido_por_cartuchos:si` (antes 4), P5 115 y «mismo lado» 93 (MARGEN-LOTE 112 y 90), T0 18 |
| 37 | PICO DE MEMORIA de cada make check | Hecho | §8 |
| 38 | §6: lo que cambia para V, las dos deudas verificadas, las líneas del cierre simuladas | Hecho | §5, §1.h, §6. Las sustituciones de simular_cierre.py casan una vez cada una en PROJECT_STATE y en la hoja de ruta (grep -c → 1) |
| 39 | §7: el informe del revisor pegado | No hecho (pendiente) | §9 no existe todavía; el Estado lo dice |
| 40 | §8: CI, con la lista de ficheros | Hecho | §8:723-731. No toca hooks, rutas ni el sistema de archivos |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | El encargo §3 pide que los recuadros «Dicen que la E se rehace en ADR-0083: volver al punto tras un stop no es el error; el error es no volver con la misma caja y no gastar el punto con el rechazo al llenar; y que lo aceptó el consultor sin buscar en el material del trader». Tres de los seis sitios que nombra el encargo no dicen lo del consultor: §2.h, §3.3 y la línea Y de §4.1. El de §3.3 tampoco dice «volver al punto tras un stop no es el error» (dice «se hizo al revés»). El informe no lo declara. Si «dicen» se lee como «cada uno», sería bloquea. | VISOR-CONSTRUCCION.md:907-910, :995-999, :1049-1054; en cambio :666-671 (§2.d.4), :916-921 (§3.1) y :1486-1489 (Estado) sí lo dicen; encargo:40 |
| b2 | menor | La tabla «El encargo frente a lo hecho» va agrupada por punto del encargo, con columnas «Hecho / Desviaciones». No es la tabla de requisitos numerados con Hecho / Parcial / No hecho / Hecho de otra forma que pide la skill entregar-rama. | PUNTO-USADO.md:691-707; `.claude/skills/entregar-rama/SKILL.md:46-50` |
| b3 | menor | Por qué falla en main `test_punto_nuevo_sigue_reconociendo_…`: el informe dice «falta `colocar o2`» y el docstring dice «En main falla: o2 no existe». Por el código de main, o2 SÍ existe: la otra caja en Z+9, porque zona:2 no está en `usadas`. Lo que falta es la o2 de Z+7 con la misma caja y la reubicación a o3. La lista de main sería `[colocar o1, colocar o2, cancelar o2]`. La causa (D1) es la correcta; la descripción no lo es. Lo saco por razonamiento: el test no lo ejecuté sobre main. | PUNTO-USADO.md:388; test_punto_usado.py:430-440; main zonas.py:470-474 |

Las comprobaciones (1), (2) y (3) del encargo §7:
- **(1) Los tests de la fase 2 van por el cableado real.** `_correr` usa `tc._motor` (MotorCableado) y `motor.correr_dia` con `tc.SPEC` (la spec real). Quita del juego sintético `toca_colocar_orden_limite`, `se_completa_zona_de_control` y `cartuchos`, que pasan a ser los reales. Solo sustituye `zona_del_punto`, en zonas y en primitivas_broker (:141-142), y deja sintéticos RN-004 (la toma) y los gates de geometría, como declara. Todos los símbolos privados que usa el test existen en main (`git show main:…zonas.py`: `_memoria` :160, `_de_la_sesion` :164, `_anotar_toma` :233, `_ligar_al_escenario` :248, `PREFIJO_ZONA` :89). La causa de los 4 rojos de D1 coincide con el código de main (ver b3 para la descripción de uno). Los 2 del campo fallan porque `CABECERA_ORDENES` de main no lleva `punto | caja 1`.
- **(2) Ninguna consulta de la CI se hizo con curl ni con un guion.** Nada en el diff ni en los anexos. La consulta con gh la reproduje yo.
- **(3) Ningún guion nuevo escribe en el repo con rutas sacadas de `__file__`.** Grep de `__file__|write|open(|mkdir|unlink` en `anexos/PUNTO-USADO/*.py`: ninguno usa `__file__`. Tres solo leen rutas recibidas por `sys.argv`. `simular_cierre.py` recibe la raíz por argumento y solo escribe en un `tempfile.TemporaryDirectory()`, fuera del repo (:137-139).

### Lo que no pude comprobar
- **Los 6 FAILED en el clon de main.** El clon está retirado y cambiar de rama o crear un worktree escribe (`git worktree` lo bloquea solo_lectura). Lo sustituye el razonamiento sobre `git show main:…` de la tabla.
- **Las dos repeticiones fuera del repo** (sha idéntico, db5a3f88… y 140e1479…). Están en la carpeta de trabajo. Sí comprobé que los sha256 de las salidas commiteadas son esos.
- **Que la fila de la fase 1 se escribiera antes de su corrida.** HOLDOUT-EXPOSICIONES.md se modificó otra vez después (23:19:05). La corrida «antes» terminó a las 22:45:26 tras 356,3 s, así que empezó hacia las 22:39:30, y e55d00a se commiteó a las 22:39:01. La fila tuvo que escribirse en esos ~30 s: es posible, pero no lo puedo mostrar.
- **Guiones que no están en el repo:** `comparar_sin_campo.py` (lo sustituí con mi propia comparación, fila 27) y el del reparto de `casos_reservados`.
- **`knowledge validate > knowledge-validate.log`, `spec docs --escribir`, `make check` y `simular_cierre.py`.** Los cuatro escriben (el último, en un temporal); no los ejecuté. Para los tres primeros, la evidencia es `make-check.log`. Para el último, que sus anclas existen una vez cada una (grep -c).
- **La traza de VISOR del 2026-07-13 (§1.d) y las horas de cierre del 29 de abril:** no las contrasté línea a línea.
- **Nota para la entrega:** la edición de §8 está sin commitear. El commit que la lleve (con este informe pegado) necesita su propio `make check` sellado.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read de `docs/encargos/trabajo-punto-usado.md`, `contrato.yaml` y `docs/validation/PUNTO-USADO.md`
3. `git diff --name-status main...HEAD && git diff --name-status`
4. `uv run python scripts/contrato_rama.py`
5. `git diff -- docs/validation/PUNTO-USADO.md`
6. `ls -la make-check.log knowledge-validate.log; grep -nE "SELLO|PICO DE MEMORIA|passed|failed" make-check.log; git rev-parse HEAD^{tree}`; Read de `make-check.log`
7. `uv run pytest <los 5 del contrato> -p no:cacheprovider | grep …` (un primer intento con `cat -A` lo negó la guardia)
8. `uv run pytest tests/unit/test_adr.py tests/unit/test_vida_de_la_orden.py -p no:cacheprovider`
9. `git log --format='%h%n%B%n-----' main..HEAD -- knowledge/spec knowledge/cases`
10. Read de ADR-0083 y ADR-0064; `git diff main...HEAD -- docs/adr/0064-… docs/adr/0074-… docs/adr/README.md`; `grep -n "^#\|no cambia"` en ADR-0074
11. `git diff --numstat main...HEAD -- VISOR-CONSTRUCCION.md HOLDOUT-EXPOSICIONES.md HISTORIA.md` y `git diff -U0 … VISOR | grep` (añadidos que no son `>`); `git diff -U2 main...HEAD -- docs/validation/VISOR-CONSTRUCCION.md`
12. `git diff -U0 main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`
13. `ls docs/validation/anexos/CORRIDA-CONSTRUCCION/; grep -nE "open\(|read_text|argv|…" …/patrones.py`
14. `ls -la --time-style=full-iso …/CORRIDA-CONSTRUCCION/__pycache__/; git check-ignore -v …; ls -la docs/validation/anexos/PUNTO-USADO/`
15. `git log --format='%h %ad %cd %s' --date=iso main..HEAD`
16. `git log --format='%h' main..HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md; git show --stat cf994a7`
17. `grep -nE "__file__|write|open\(|argv|…" docs/validation/anexos/PUNTO-USADO/*.py`; Read de los cuatro guiones
18. `git diff main...HEAD -- src/`
19. Grep de `ctx.eventos` en `src/botsito/engine`; Read de `cableado.py:286-435`
20. Read de `tests/unit/test_punto_usado.py`; grep de `_sinteticas` y `_motor` en `test_cableado.py`
21. `git show main:src/botsito/engine/zonas.py | grep …` (dos veces) y `git show main:src/botsito/engine/primitivas_broker.py | grep …`
22. `git diff main...HEAD -- knowledge/spec/ docs/spec/`
23. Read de `LA-CAJA-DEL-29-DE-ABRIL.md:228-247`; `sed -n` de strategy_spec, ambiguedades y parametros; `grep -n "ninguno_de" …` (rama y main) y `grep -n "activacion_sin_ruptura"`
24. `grep -rl` de los dos registros de feedback y del item de evidencia; Read de los tres
25. `uv run botsito corpus transcript show --video v6 --t0 1:23:50 --t1 1:24:10`
26. Grep de fechas reservadas en el informe, el ADR y los anexos (un primer intento con `for` lo negó la guardia), y de 2025, 2026-10 a 12 y julio 18-31
27. `tail` de reentradas_antes/despues, `cat patrones.txt`, `grep -c detenido_por_cartuchos:si`, `wc -l` de los anexos
28. `sha256sum` de antes-diaria, de la diaria de MARGEN-LOTE y de la diaria de la fase 4
29. `wc -l` y `diff … | grep -c "^>"`; `diff … | grep -E "^[0-9]"`; `grep -n "### Ordenes"`; `sed -n '1541,2044p' … | cut -d'|' -f1-15 | sha256sum` frente al de MARGEN-LOTE
30. `git diff main...HEAD | grep -nE "curl|api.github|…"`; `grep -rnE "curl|subprocess|urllib|requests"` en los anexos
31. `gh run view 39186492700 --json status,conclusion,headSha,headBranch,name`
32. `git diff main...HEAD -- PROJECT_STATE.md; wc -c PROJECT_STATE.md; git show main:PROJECT_STATE.md | wc -c`
33. `git diff main...HEAD -- docs/state/HISTORIA.md | grep "^+" | head`
34. `uv run pytest tests/unit/test_historia.py tests/unit/test_project_state.py tests/unit/test_hoja_de_ruta.py tests/unit/test_contrato_rama.py -p no:cacheprovider`
35. Grep de «punto por punto» en `.claude/skills`
36. Grep de «RECUADRO DE CORRECCIÓN (2026-10-18» en VISOR-CONSTRUCCION.md
37. `grep -c` de las anclas de simular_cierre.py en PROJECT_STATE.md y HOJA-DE-RUTA.md (dos llamadas)
38. `grep -n "2026-04-29 | 07-11 | o"` en la diaria de la fase 4
39. `git diff main...HEAD -- tests/unit/test_orden_stop_pivote.py tests/unit/test_vida_de_la_orden.py`
40. `ls docs/validation/anexos/MARGEN-LOTE/; grep -rn "mismo lado\|^total" …/MARGEN-LOTE/*.txt`
41. `git branch --list && ls .git/worktrees` (antes, `git worktree list` lo bloqueó solo_lectura)
42. `ls -l --time-style=full-iso` de los anexos, de HOLDOUT-EXPOSICIONES.md y de make-check.log
43. Grep de «ni con orden viva», «mientras la» y de las líneas del ADR para a1 y a2; grep de `broker:` y `RECHAZADA` en primitivas_broker, cableado y broker

### 9.2 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado.** La descripción de `toca_colocar_orden_limite` dice ahora «que la sesion no tenga gastado, ni con orden viva, ni con esa misma caja ya cancelada (una caja cancelada no vuelve; otra caja del mismo punto si)»; el docstring del módulo de `zonas.py` y el de `marcar_usada` dicen lo mismo; el comentario de `test_orden_stop_pivote.py:190` dice «su orden viva, o cancelada». `spec manifest --escribir` (hash `94d004a7…`) y `spec docs --escribir` en este commit, con `Fuente: ADR-0083`; `spec_version` 18.1.2 → 18.1.3 (`knowledge validate` lo exige con cada cambio del hash). ADR-0083 §1 («lo que no cambia») y §1.b del informe ya lo decían bien |
| a2 | importa | **Arreglado.** ADR-0083 §6 dice que no mueve P7 (3 antes y después, medido en §4.d) y añade a P5 las reentradas con la misma caja; su Impacto dice que el límite de la zona reutilizada en un escenario nuevo NO se midió y va a Technical Debt. §4.f y §6 lo llevan como tercera línea de deuda (`simular_cierre.py` la lleva: a, b y c vacíos, 22.546 bytes) |
| a3 | importa | **Arreglado.** ADR-0083 §6 y §1.i citan v6 1:23:45-1:24:07 tal como lo da la capa corregida (con las marcas y sin recomponer «al mismo / mismo nivel» ni «otro otra»), y declaran la lectura: dos salidas tras un equal perdido, el siguiente nivel o el mismo; D1 toma que la reentrada en el mismo nivel es una de las dos, no la única |
| a4 | importa | **Arreglado.** «diez recuadros» en §3.c y §7; el mensaje del commit 56bbf91 dice «once» y no se reescribe (se declara) |
| a5 | menor | **Arreglado.** §4.e: o1 reubicada a o2 con el 1 nuevo (el mismo punto); o3 en OTRO punto |
| a6 | menor | **Arreglado.** Línea en blanco tras los dos recuadros que van dentro de una lista (el cuerpo sigue intacto: solo se añade una línea vacía) |
| b1 | importa | **Arreglado.** Los recuadros de §2.h, §3.3 y la línea Y de §4.1 dicen las tres cosas del encargo §3 (la E se rehace en ADR-0083; volver al punto tras un stop no es el error, el error es no volver con la misma caja y no gastar el punto con el rechazo al llenar; y lo aceptó el consultor sin buscar en el material del trader). Declarado en §3.c |
| b2 | menor | **Arreglado.** §7 es ahora la tabla de 41 requisitos numerados con Hecho / Parcial / No hecho / Hecho de otra forma |
| b3 | menor | **Arreglado.** El docstring del test y la fila de §3.a dicen que en `main` o2 sí existe (la otra caja en Z+9, sin reubicación: colocar o1, colocar o2, cancelar o2 por RN-035) y que lo que falta es la o2 de Z+7 con la misma caja y la reubicación a o3 |

Lo que no pudo comprobar, contestado: (1) los 6 FAILED en el clon de `main`: el log de pytest está en
la carpeta de trabajo de la sesión y el clon se retiró como pide `comparar-con-main`; la causa de
cada rojo la razonó él sobre `git show main:…` y coincide con §3.a (b3 corrige la descripción de
uno). (2) Las dos repeticiones fuera del repo: las copias no se commitean por regla; los sha256 de
las salidas commiteadas son los que dice el informe, y los de las copias coinciden (§2.b y §4.f).
(3) La fila de la fase 1: se escribió con un Edit en la misma respuesta de la sesión que lanzó la
corrida, justo antes del comando; la hora de modificación del fichero es la de la fila de la fase
4, posterior. (4) Los dos guiones de la carpeta de trabajo (`comparar_sin_campo.py` y el recuento de
`casos_reservados`) no se commitean: el primero lo reprodujo él con otro método (fila 27) y el
segundo solo imprime recuentos por mes. (5) `knowledge validate`, `spec docs` y `make check` quedan
en `make-check.log` de este último commit; `simular_cierre.py` escribe en un temporal.

## Estado

LISTA PARA REVISIÓN, NO CERRADA (2026-10-18, por el reloj de la máquina; 2026-10-19 en UTC). Fases 0
a 4 hechas (§1 a §4): ADR-0083 enmienda la decisión 1 de ADR-0064, el código lo cumple con 13 tests
por el cableado real (6 rompen en `main`: 4 por D1 y 2 del campo), la corrida de R3.1 repetida con
sus tres comandos (§4); lo que cambia para V (§5) y las líneas del cierre, simuladas (§6); el
revisor, con 0 «bloquea», 5 «importa» y 4 «menor», todos arreglados (§9); sin CI de Linux porque la
rama no toca la plataforma (§8). El cierre en `main` solo con la orden de Aleks.

Rama lista para revisión, NO cerrada.
