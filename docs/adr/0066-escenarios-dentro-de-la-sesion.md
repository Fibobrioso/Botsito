---
status: ACTIVE
date: 2026-10-01
phase: post-F14 (rama `feature/escenarios-por-sesion`, A3 b) de Next Action)
---

# 0066 · Escenarios dentro de la sesion: la toma tiene que ser de la sesion, y cada liquidez nueva abre un escenario con sus intentos

> **PROVISIONAL en cinco parametros.** Cinco decisiones dependen de preguntas abiertas de la sesion
> 4 con el trader (5, 15, 18, 20 y 21; las dos ultimas, de la orden del consultor del 2026-10-02):
> van como parametros DEFAULT_AMBIGUOUS con su `ambiguedad_id`, y su valor se revisa con la
> respuesta. Lo demas sale de lo que el trader ya dijo, con su cita. Es una
> tarea autonoma: el consultor no lo ha revisado todavia.

## Decision

### 1. Una toma solo cuenta si ocurre dentro de la sesion

RN-004 gana una condicion, el predicado `la_toma_es_de_la_sesion`: el pivote que es la liquidez no
puede estar tomado ya -una M1 cerrada pasada la linea con `liquidez_m15_criterio_toma`- entre su
formacion y la apertura de la sesion.
- **Tomado en una sesion anterior del dia: no cuenta.** Es A-46 RESUELTA («cada uno es un mundo
  diferente», `fb-2026-09-29-sesion-03-5021677e`). Sin esto, RN-004 volvia a fijar la toma de la
  manana en la apertura de la tarde sobre el mismo pivote si el precio seguia pasado: `cruza` mira
  donde cierra la ultima M1, no si cruza (medido, `docs/validation/ESCENARIOS-POR-SESION.md` §0.2).
- **Tomado antes de la primera sesion: lo decide `toma_antes_de_la_ventana`** (A-43, pregunta 15),
  PROVISIONAL `no_cuenta`: la liquidez formada antes de las 7 vale si el precio «la toma ya dentro»
  (`ev-v9-004533-d075b080`). `cuenta` es lo que hacia el motor.
- La M1 que cierra exactamente en la apertura es de antes: se formo antes de que la sesion abriera.

### 2. Un escenario es una liquidez tomada dentro de la sesion, con sus intentos

Vive en el productor (`engine/zonas.py`), sesion a sesion: la toma (con la identidad del pivote),
las zonas que se ligan en el, y si ha terminado.
- **Nace** con la primera toma de la sesion, y con cada toma de una liquidez NUEVA -otro pivote-
  cuando el vigente ha terminado. Lo abre la accion nueva `abrir_escenario`, que RN-004 hace tras
  fijar el hecho. RN-004 vuelve a fijar el hecho en cada M1 que cierra pasada la linea, asi que la
  misma liquidez no abre nada.
- **Termina** cuando una operacion suya se cierra en ganancia -RN-034, nueva: «ya aquí está el trade
  ganador, aquí no buscamos nada, [...] pues tenemos que esperar nuevamente a que se desarrolle la
  liquidez»
  (`ev-v6-003227-c4efcf49`)-, cuando gasta sus intentos (RN-016) y cuando acaba la sesion (A-46).
  **La version vigente es la de la sesion 1, no la de v4.** En v4 el trader dijo que el dia termina
  con la primera ganadora (`ev-v4-004936-d7004417`, v4 0:49:36, «apenas tengo el trade positivo ya
  no opero más»; y `ev-v4-011351-74b8bb39`, v4 1:13:51). La primera la rechazo en la sesion 1
  (`fb-2026-09-09-sesion-01-af02495f`: «NO. Que siga operando, pero que respete la regla de los 3
  cartuchos de perdida»); la segunda la sustituye `ev-v6-000732-f7189541`, y
  `ev-v6-000732-5945fd87` sustituye a `ev-v1-000959-b82650ad` («no estamos pausando cuando se dé el
  trade ganador»). Lo vigente es RN-017 (el dia sigue) mas RN-034 (en otra liquidez). Cadena
  confirmada por el consultor el 2026-10-02.
- **Tras una perdida, un break even o un equal, SIGUE** con los intentos que le queden: «nuevamente
  tiene todavía un gatillo [...] un cartucho» (`ev-v3-002405-a202dbf6`). Tras un break even lo
  dijo el trader en v4: «los breakeven no se cuenta [...] tienes un cartucho todavía para poder
  seguir operando» (`ev-v4-004832-6543b551`, v4 0:48:32-0:48:52); y en la sesion 3, a la pregunta
  «¿Cuentan los break-even y las entradas invalidadas?», «no cuentan» (`ev-v9-013117-c683f9b5`,
  confianza media: el hablante se atribuye por contexto).
- **El tope de escenarios** por sesion lo decide `max_escenarios_por_sesion` (A-52, pregunta 20),
  PROVISIONAL `sin_limite`: «eso no lo podemos definir [...] en todas estas 4 se va a dar una
  operación» (`ev-v9-003318-c0503fe5`), que no da un numero; antes habia dicho «como máximo dos
  entradas por día» (`ev-v4-003350-acb03ee7`). Con un tope, la toma que lo pasaria no abre
  escenario. Lo acotan ademas las tomas y RN-018.
- **Una toma nueva con el escenario vivo** la decide `intentos_tras_toma_nueva` (A-25, pregunta 18),
  PROVISIONAL `vuelven_a_cartuchos_max` -un escenario nuevo con los intentos enteros-, por «tres
  intentos por liquidez» (`ev-v9-013054-d49a544e`). Con `siguen_los_que_quedan`, el mismo escenario
  sigue sobre la toma nueva.

### 3. Los cartuchos son los intentos del escenario

El acumulador `cartuchos` deja de ser un hueco: cuenta los cierres de las ordenes de las zonas del
escenario vigente que nombran las dos ramas de RN-016 (`cartucho_criterio` = `solo_perdida`). Asi
RN-016 puede disparar por primera vez. El reinicio (`cartuchos_reinicio` = `siguiente_liquidez_m15`)
es abrir un escenario: `abrir_escenario` apaga `detenido_por_cartuchos`. Las otras opciones de
`cartuchos_reinicio` no tienen contrato y el motor las rechaza con nombre.

### 4. La orden pendiente al abrir otra sesion

RN-035, nueva: al abrir una sesion con una orden de la anterior sin llenar, `retirar_orden_limite`
segun `orden_pendiente_al_abrir_sesion` (A-30 y A-39, pregunta 5), PROVISIONAL `se_retira`, por la
independencia de las sesiones (A-46). `sigue_hasta_ventana_fin` es lo que hacia el motor. La opcion
«la dejo y la sigo moviendo en la sesión siguiente» de la pregunta 5 no se escribe hasta que el
trader la elija. Una posicion abierta no entra: la cierra RN-002.

### 4 bis. La orden pendiente al abrir otro escenario en la misma sesion

Si una toma de otra liquidez abre un escenario con una orden del anterior sin llenar,
`abrir_escenario` hace lo que diga `orden_pendiente_al_abrir_escenario` (A-53, pregunta 21),
PROVISIONAL `se_mueve`: la orden sigue viva -y se puede llenar- hasta el primer punto de breaker de
la liquidez nueva, donde RN-006 la reubica. Es lo que hacia el motor, medido con un test sintetico
(`test_la_orden_viva_cuando_otra_toma_abre_un_escenario`), y no sale de una regla del trader: lo
unico que dijo de la vida de la orden («sigue vivo hasta que se desarrolle otra próxima, otro posible
punto de breaker», A-38, `fb-2026-09-29-sesion-03-c7fa3068`) habla de la misma liquidez. Con
`se_retira` se cancela en la toma. En los dos casos nunca hay dos ordenes vivas a la vez: RN-011 no
coloca con una pendiente, y `retirar_orden_limite` y `reubicar_orden_limite` se niegan con nombre
si hubiera dos. Ninguna de las dos opciones multiplica las peticiones al servidor (R13): abrir un
escenario emite como mucho una cancelacion (`se_retira`) o ninguna (`se_mueve`); la reubicacion son
dos peticiones, igual que dentro de un mismo escenario
(`docs/validation/ESCENARIOS-POR-SESION.md`, §6.4: cinco escenarios en una sesion, 10
peticiones en el dia, medido con un test sintetico).

### 5. Que enmienda

- **ADR-0064, DECISION 2** («una sola vida de orden por sesion que llega a llenarse»): la sustituyen
  el escenario y RN-034. Se escribio porque los cartuchos no existian.
- **ADR-0064, DECISION 3** («la orden pendiente de una sesion [...] sigue viva hasta la ventana»):
  pasa a ser la opcion `sigue_hasta_ventana_fin` de RN-035, que no es la de por defecto.
- **ADR-0055 §4** queda cerrada en lo que dejaba abierto: la caducidad del hecho no bastaba sola.

## Problema que resuelve

El bot operaba como mucho una vez por sesion, aunque el trader dice que cada liquidez da hasta tres
intentos y que tras una ganadora busca otra liquidez; los cartuchos no existian; la liquidez de la
manana valia en la tarde por la puerta de atras; y una orden de la manana sin llenar dejaba la tarde
sin operar.

## Alternativas consideradas

- **Dejar la decision 2 de ADR-0064**: contradice «tres intentos por liquidez».
- **Hacer caducar `liquidez_tomada` al terminar el escenario**: el hecho se volveria a fijar en la
  M1 siguiente sobre la misma liquidez, porque `cruza` no mira si cruza; hace falta la identidad
  del pivote, que es lo que guarda el escenario.
- **Inventar las respuestas de las preguntas 5, 15, 18, 20 y 21**: el encargo lo prohibe; van como
  parametros PROVISIONAL.

## Por que elegimos esta opcion

Cada pieza sale de una cita del trader, salvo las cinco que dependen de la sesion 4, que quedan como
parametros con su pregunta. El mecanismo queda en la spec (RN-004, RN-034, RN-035 y el acumulador)
y no solo en el motor.

## Por que descartamos las demas

Ver «Alternativas consideradas».

## Impacto

- **Spec**: `la_toma_es_de_la_sesion`; `abrir_escenario` y `terminar_escenario`; `retirar_orden_limite`
  con `segun`; el token `ORDEN`; RN-004, RN-016 (notas), RN-034 y RN-035; el acumulador `cartuchos`
  y los hechos `liquidez_tomada`, `detenido_por_cartuchos` y `orden_limite_pendiente`. Cinco
  parametros nuevos, DEFAULT_AMBIGUOUS (`max_escenarios_por_sesion` y
  `orden_pendiente_al_abrir_escenario`, de la orden del 2026-10-02).
- **Codigo**: `engine/interprete.py` (el `Momento` lleva el inicio de la sesion y de la ventana),
  `engine/motor.py`, `engine/cableado.py`, `engine/primitivas.py`, `engine/zonas.py` y
  `engine/primitivas_broker.py`.
- **Tests**: `tests/unit/test_escenarios_por_sesion.py`.
- **Medido** en `docs/validation/ESCENARIOS-POR-SESION.md`, sin cifras agregadas sobre las 77
  operaciones de construccion (el consultor pre-registra antes el umbral de cobertura).

## Fecha / fase

2026-10-01 · rama `feature/escenarios-por-sesion`. `PROJECT_STATE.md`, Next Action A3 b).

## Estado

ACTIVE (PROVISIONAL en `toma_antes_de_la_ventana`, `intentos_tras_toma_nueva`,
`orden_pendiente_al_abrir_sesion`, `max_escenarios_por_sesion` y
`orden_pendiente_al_abrir_escenario`: se revisan con las preguntas 15, 18, 5, 20 y 21 de la sesion 4)
