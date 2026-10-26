---
status: ACTIVE
date: 2026-10-18
phase: post-F14 (rama `trabajo/punto-usado`, R3.4 de la hoja de ruta; Y de la Next Action)
---

# 0083 · Qué gasta un punto: el rechazo (al colocar o al llenar) y el no envío; el llenado no, y tras una pérdida o un break even el mismo punto se vuelve a colocar, con la misma caja o con otra (enmienda la decisión 1 de ADR-0064)

> Decisión del consultor del 2026-10-18 (encargo de `trabajo/punto-usado`, D1 a D5), tomada ANTES
> de ver las medidas. **Enmienda la DECISIÓN 1 de ADR-0064** (recuadro allí y fila del índice) y
> pone una nota en ADR-0074 §4. **PROVISIONAL en D1 hasta la pregunta 3 de la sesión 5** (V de la
> Next Action; R4.1): cuántas veces reentra el trader en el mismo punto tras un stop, y con qué
> caja. No es un parámetro ni cuelga de ninguna ambigüedad: lo ata esta nota, su fila del índice y
> la línea de V (PUNTO-USADO.md §6).

## Decision

### 1. D1 · Lo que gasta un punto, en su sesión

Un **punto** es el posible punto de breaker en el que nace la orden stop (ADR-0064 §1): la clave
`nivel@inicio` de su vela contraria. Una **caja** es un 1 de ese punto (ADR-0074: el 1 se recalcula
en cada cierre de M1 hasta el llenado), y cada caja es una zona del productor.

**Gasta el punto**, y en esa sesión ninguna caja de ese punto se vuelve a colocar:

- la orden que el bróker **RECHAZA al colocar** (precio inválido, stops level, volumen, margen;
  ADR-0052 §4, ADR-0057, ADR-0081 §4);
- la orden que el bróker **RECHAZA al llenar** (margen libre al precio del llenado, ADR-0081 §4);
- la orden que el bot **NO ENVÍA** (lote por debajo del mínimo, o `lote_si_no_cabe = no_operar` con
  un límite que muerde; ADR-0081 §2 y §3).

**No lo gastan:**

- la **reubicación** (RN-006): con un 1 nuevo del mismo punto (ADR-0074) o con un punto nuevo
  (ADR-0064 §4), la orden pendiente se cancela y se vuelve a colocar en el mismo cierre;
- el **llenado**: cerrada la operación con una **pérdida, un break even o un equal** (en el motor:
  todo cierre por `stop`, `objetivo` o `manual` cuyo resultado no sea `ganancia`; el equal es
  RN-019, que hoy no dispara, PUNTO-USADO.md §1.h), el punto se puede volver a colocar, **con la
  misma caja o con otra**, por la vía normal de colocación (D5) y con los cartuchos de siempre
  delante (RN-016).

Tras una **ganadora**, RN-034 termina el escenario y no se vuelve a colocar nada: esto no cambia
(ADR-0066; `toca_colocar_orden_limite` ya lo niega con el escenario terminado).

**Lo que no cambia**, y la fase 0 midió (PUNTO-USADO.md §1.b): una orden **cancelada** (RN-035 a
`ventana_fin` o al abrir otra sesión, RN-036 por la racha, el escenario nuevo con `se_retira`, la
ventana prohibida de ADR-0068 y la red de seguridad del fin del día, ADR-0053 §6) deja su caja
usada y su punto sin gastar, como hasta hoy: esa caja no vuelve, otra sí. EXPIRADA no ocurre
(ningún llamador del cableado pone `expira_ms`).

> **LO QUE DIJO EL TRADER EN LA SESIÓN 5 (2026-10-23, S-6, «pregunta 3»; recuadro del 2026-10-26,
> `trabajo/activar-sesion-05`, que no reescribe el cuerpo). D1 SIGUE PROVISIONAL.** Sobre su propio
> replay, sin que se le enseñara ningún día real, contestó en parte y sin una regla: de las
> reentradas en el mismo nivel, «me da unas ganas de replantearme para poder quitar esa condicional
> cuando hay break even porque siento yo que las veces que he hecho backtesting … son las que nos
> generan un gran cúmulo de pérdidas» (`ev-v15-002029-1ac081ae`: una duda, no una regla); en su
> ejemplo «solo vemos el punto … El punto 1 … Se actualiza del nivel 0 … sigue marcando el mismo
> nivel» (`ev-v15-002441-2e609b87`: el 1 sigue y el 0 se actualiza; si la caja es la del primer
> intento o una nueva no lo dice con esas palabras); y «un posible punto breaker tiene que haber
> roto por encima porque si no está roto por encima, nosotros no lo validamos»
> (`ev-v15-002729-30480ec5`: para volver a validar el punto, el precio tiene que haberlo roto).
> No dio un número de reentradas y no llegó a decir si tras un break even vuelve al mismo punto. Lo
> demás de ese tramo -que cada reentrada es una decisión aparte y su duda sobre los niveles
> iguales- está en `SESION-05-EXTRACCION.md` §3.2, S-6, y no se cita aquí. Ningún registro de
> feedback: una respuesta «en parte» no fija nada. **Lo que pasa a la sesión 6:** cuántas veces
> reentra en el mismo punto tras un stop, si la caja de la reentrada es la del primer intento o una
> nueva, y qué hace tras un break even; con esquemas, sin días reales.

### 2. D2 · Cómo lo hace el código

Hoy hay dos marcas en la memoria de la sesión (`engine/zonas.py`): `usadas`, por ZONA (una caja), que
se pone al colocar y nunca se borra; y `rechazados`, por PUNTO, que se pone al no enviar y al rechazo
al colocar. Por eso `main` hacía dos cosas que D1 no dice: tras un llenado y un stop, la MISMA caja
no volvía (la zona seguía en `usadas`) pero OTRA sí, y el rechazo al llenar no gastaba el punto (nadie
llamaba a `marcar_rechazada`). Era la E de VISOR-CONSTRUCCION.md §2.d.4 leída al revés: volver al
punto tras un stop no es el error; el error es no volver con la misma caja y no gastar el punto con el
rechazo al llenar.

Con este ADR (PUNTO-USADO.md §1.c, la vía):

- `zonas.liberar_usada(estado, sesion, zona_id)`: la orden de esa zona terminó sin ganar y su punto
  vuelve a estar disponible, con esa caja o con otra.
- `cableado.correr_dia`, en cada cierre de M1 y a partir de `ctx.eventos` (los hechos del bróker que
  `_a_la_cuenta` acaba de pasar): un evento `rechazada` gasta el punto de la orden
  (`marcar_rechazada`); un cierre (`stop`, `objetivo`, `manual`) con resultado distinto de `ganancia`
  libera la zona de su orden (`liberar_usada`). Con `ganancia` no se libera nada: RN-034 ya termina el
  escenario. La sesión de cada orden la apunta `colocar_orden_limite` (`ctx.sesion_de_orden`), que es
  la misma con la que marcó la zona.
- `_punto_nuevo` (RN-006) no cambia: la zona de una orden PENDIENTE sigue en `usadas` hasta que su
  posición se cierra, así que «la pendiente es de esta sesión» se lee igual. El sentido de `usadas`
  pasa a ser «zonas cuya orden está viva o terminó sin liberar el punto».
- Por qué en el cableado y no en las primitivas ni en `_a_la_cuenta`: los predicados son puros
  (ADR-0055 §1); una acción de la spec para llevar la memoria del productor sería mecánica, no
  estrategia; `_a_la_cuenta` es el puente bróker→cuenta y no sabe de la memoria de la estrategia; el
  bucle de `correr_dia` es el único sitio que ya tiene el bróker, el contexto y el estado, y donde
  los hechos del bróker llegan al intérprete (`estado.broker = broker.hechos()`).

### 3. D3 · Los dos tests que rompen en `main`, y los que pasan en los dos

`tests/unit/test_punto_usado.py`, por el cableado real con la spec real y el productor real de la
zona; lo único sintético de la geometría es `zona_del_punto`, que registra la zona como la real y
dice en cada test qué caja construye. En `main` fallan: (a) tras una pérdida, el mismo punto se
vuelve a colocar con la MISMA caja; (b) tras un rechazo al llenar, el punto no se vuelve a colocar
con ninguna caja (con un 1 nuevo, que es lo que `main` colocaba); y, por (a), el break even y
`_punto_nuevo` tras una pérdida. Pasan en los dos: el 1 nuevo tras la pérdida, la ganadora (RN-034),
los cartuchos (RN-016), el rechazo al colocar, el no envío, D4 y la reubicación con la orden sin
llenar. Los recuentos de FAILED, en PUNTO-USADO.md §3.

### 4. D4 · Con la posición abierta no se coloca otra orden

Lo impide ya RN-011 (`ninguno_de orden_limite_pendiente y operacion_abierta`) con RN-018 y
`operaciones_simultaneas_max = 1`. No cambia; un test lo fija por el cableado. En la traza de
2026-07-13 11-15 (PUNTO-USADO.md §1.d) cada orden se coloca en el cierre siguiente al stop de la
anterior, y con otra caja (tres 1 distintos).

### 5. D5 · La reentrada sale por la vía normal

RN-011 y RN-015, con los gates delante; la caja se calcula como siempre (`caja_bloque`,
`caja_se_fija`). Este ADR **no decide** si la caja de la reentrada es la del primer intento o una
nueva: es la pregunta 3 de V, que gana el ejemplo del 29 de abril.

### 6. Lo que dijo el trader, y lo que no

- **LA-CAJA-DEL-29-DE-ABRIL.md:236-243** (abril es construcción): dos ventas del xlsx con la misma
  entrada (1.17064) y el mismo stop (1.17079) a las 07:55 y 07:58 UTC; la primera pierde en el stop
  (`rPnL -15`) y el trader lo narra: «nos mitiga y nuevamente, pues, sería cuestión de poner otra
  reentrada aquí». El pasaje da las horas de entrada, no la de cierre de la primera.
- **`fb-2026-09-09-sesion-01-fe4a6a5c`** (sesión 1, CONFIRM sobre `ev-v4-003710-c753f3d3`): «SI (no
  hay entradas en paralelo; para reentrar debe haber tocado el stop)»; sigue vivo según
  `fb-2026-09-09-sesion-01-fae74396`. Apoya D1 (se reentra tras el stop) y D4.
- **RN-018** («para que tú puedas entrar nuevamente o bien te ha tocado stop loss»,
  `ev-v4-003710-c753f3d3`).
- **v6 1:23:45-1:24:07** (capa corregida y filtrada, `corpus transcript show`; fuera de los tramos
  no citables de v6; es el pasaje del equal que RN-019 ya cita unas líneas antes). Tal como lo da
  la capa: «[1:23:45] … después de un igual si [1:23:53] nos genera una pérdida nuevamente
  actualizamos a la siguiente o sea al siguiente nivel al mismo [1:23:59] mismo nivel como tal
  mantenemos o abrimos otro otra orden límite para poder reentrar si se da». **Lectura nuestra,
  declarada:** el trader habla de un equal que acaba en pérdida y da dos salidas, actualizar al
  siguiente nivel o mantener o abrir otra orden límite en el mismo nivel para reentrar; lo que D1
  toma de ahí es que la reentrada en el MISMO nivel tras una pérdida es una de las dos, no que
  sea la única. Sin item de evidencia propio (`knowledge/evidence/` no se toca en esta rama): V
  puede proponerlo. Y `ev-v5-000246-17eff9e1` («cuando hay un equal […] contarlo como pérdida
  pero reentrar nuevamente si es que el precio»).
- **ADR-0066:51 y RN-034** (tras una pérdida, un break even o un equal, el escenario sigue con los
  intentos que le queden; `ev-v3-002405-a202dbf6`, `ev-v4-004832-6543b551`) hablan del ESCENARIO,
  no del punto: VISOR-CONSTRUCCION.md:673-675 lo señaló. Por sí solos no bastan; con lo de arriba,
  sí: ADR-0066 no fija si el intento siguiente puede ir al mismo punto, y el material dice que sí.
- **CORRIDA-CONSTRUCCION.md §4.5**: P7 (entradas repetidas del trader en el mismo nivel que el bot
  toma una vez) y P5 (el bot se para y vuelve a entrar) tienen destino V, pregunta 3. Medido en la
  fase 4 (PUNTO-USADO.md §4.d): este ADR no mueve P7 (3 filas antes y después; en esas sesiones el
  bot no estaba en el punto cuando el trader repitió) y añade a P5 las reentradas con la misma
  caja; deja la pregunta 3 abierta con el ejemplo del 29 de abril.
- **En contra: nada** en `knowledge/feedback/` ni en el corpus filtrado («reentrada», «mismo nivel»,
  «equal»).

## Problema que resuelve

La decisión 1 de ADR-0064 (2026-09-30, «un punto ya usado no se vuelve a colocar. Usado es con la
orden enviada, aceptada o rechazada») se escribió como la lectura más conservadora, antes de
ADR-0066 (2026-10-01), y su única razón es el rechazo: no reintentarlo en cada M1 y no llenar el
contador de R13 (ADR-0064:79-81). El código la aplicó por zona y no por punto, así que hacía dos
cosas que ni la decisión ni el material dicen (§2). VISOR-CONSTRUCCION.md §2.d.4 lo clasificó como E
en el sentido contrario (que el bot NO debía volver al punto), y el consultor lo aceptó sin buscar
en el material del trader (encargo §1).

## Alternativas consideradas

1. Aplicar la decisión 1 al pie de la letra: marcar el PUNTO al colocar, y que tras un stop no
   vuelva con ninguna caja (lo que proponía VISOR-CONSTRUCCION.md §3.3).
2. D1: el rechazo y el no envío gastan el punto; el llenado no, y tras un cierre sin ganar vuelve
   con la misma caja o con otra.
3. Dejarlo como estaba (`main`): la misma caja no vuelve, otra sí.

## Por que elegimos esta opcion

Por el material (§6): el trader reentra en el mismo nivel tras el stop, y la razón de la decisión 1
(no reintentar un rechazo) no alcanza a un llenado. Y porque el motor ya tiene los cartuchos (RN-016)
y RN-034 delante: la reentrada está acotada por lo que el trader sí fijó.

## Por que descartamos las demas

La 1 contradice el 29 de abril y los registros de la sesión 1, y convertiría la reentrada del
trader (P7) en una diferencia permanente del bot. La 3 no es una decisión: es el efecto de una marca
por zona que la decisión 1 no pedía, y deja el rechazo al llenar sin gastar el punto.

## Impacto

- `src/botsito/engine/zonas.py` (`liberar_usada`; los docstrings del módulo, de `marcar_usada` y de
  `marcar_rechazada`), `cableado.py` (`correr_dia`) y `primitivas_broker.py`
  (`ctx.sesion_de_orden`; el comentario del no envío cita este ADR).
- `knowledge/spec/strategy_spec.yaml`: la descripción de `toca_colocar_orden_limite` dice qué gasta
  un punto; `spec_version` sube; `spec manifest --escribir` y `spec docs --escribir`.
- Recuadro en ADR-0064 (decisión 1) y nota en ADR-0074 §4; filas del índice de los tres.
- Recuadros de corrección en VISOR-CONSTRUCCION.md junto a todo lo que da la E por buena, y la línea
  del Estado de R3.2 en la hoja de ruta (en el cierre).
- La corrida de R3.1 repetida (PUNTO-USADO.md §4): cambian las reentradas que la pregunta 3 enseña al
  trader y las sesiones con los cartuchos agotados.
- Un límite que este ADR abre y no cierra: una zona reutilizada en un escenario nuevo sigue ligada
  al escenario en que nació, y sus cierres contarían en los cartuchos de aquel (PUNTO-USADO.md
  §1.c). La fase 4 no lo midió (hace falta la traza por cierre; las 14 reentradas con la misma caja
  van de 21 s a 4 min 27 s después del llenado anterior). Va a Technical Debt (PUNTO-USADO.md §6).

## Fecha / fase

2026-10-18; post-F14, rama `trabajo/punto-usado` (R3.4).

## Estado

ACTIVE (PROVISIONAL en D1: la sesión 5 respondió en parte y sin regla, recuadro del 2026-10-26 en
§1; va a la sesión 6; enmienda la decisión 1 de ADR-0064; nota en ADR-0074 §4)
