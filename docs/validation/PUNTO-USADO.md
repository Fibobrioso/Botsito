# PUNTO-USADO · Qué gasta un punto: la reentrada tras un stop y el rechazo al llenar (R3.4)

Rama `trabajo/punto-usado`, abierta el 2026-10-18 desde `main` en f96b581 (commit de estado sobre
el merge 3ae2933, tag `stable/F37u-plataforma-adelantada`). Encargo:
`docs/encargos/trabajo-punto-usado.md`. Tramo: R3 (R3.4 de `docs/plan/HOJA-DE-RUTA.md`; Y de la
Next Action). Modelo de la sesión: `claude-fable-5-1` según el entorno de la sesión; `/model` en el
terminal de Aleks dio «Fable 5.1 … `high` effort» al empezar.

(Hasta que exista, ADR-0083 va declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; el bloque sale en el commit que lo cree.)

```ids-inexistentes
ADR-0083 — el ADR que el encargo manda escribir (D2); no existe hasta la fase 3 de la rama
```

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
  «equal»; oculta 4.631 segmentos y 2 items, como siempre): v6 1:23:53-1:24:07, capa corregida y
  filtrada (`corpus transcript show`, fuera de los dos tramos no citables de v6): «después de un
  igual si nos genera una pérdida nuevamente actualizamos a la siguiente, o sea al siguiente nivel;
  al mismo nivel como tal mantenemos o abrimos otra orden límite para poder reentrar si se da». Es
  el pasaje del equal que RN-019 ya cita (v6 1:22:25-1:23:19) unas líneas después, y dice lo que D1
  dice: tras la pérdida, la reentrada en el MISMO nivel. No tiene item de evidencia propio
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

## Estado

EN CURSO. Abierta el 2026-10-18; fase 0 entregada (§1) sin PARADA; sigue la fase 1 (el campo y la
corrida «antes»).
