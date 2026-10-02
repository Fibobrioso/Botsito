# FUNCTIONALITY VALIDATION REPORT · Escenarios por sesion

Rama `feature/escenarios-por-sesion`, abierta el 2026-10-01 desde `main` `a093ffb` (tag
`stable/F36m-ajustes-cierre`). Encargo, copiado tal cual:
`docs/encargos/feature-escenarios-por-sesion.md`. Es A3 b) de los pendientes de `PROJECT_STATE.md`.
Tarea autonoma: NO se cierra.

## 0. Fase 0 · Lo que hay hoy, medido en el codigo (antes de tocar nada)

### 0.1 Lo que ya esta hecho de A3 b)

`PROJECT_STATE.md` dice que b) no tiene evidencia de estar hecha. **Parte si la tiene**: la noche del
30 de septiembre (`stable/F36-nocturno-01oct`, `docs/validation/NOCTURNO-01OCT.md` §1) entro F33,
«cada sesion es un escenario propio: `liquidez_tomada` caduca al abrir la sesion» (`bf1dc0b`), con
`tests/unit/test_sesiones_independientes.py`. Y la caja por operacion de ADR-0056 §4 la hace ADR-0064
(F35): cada posible punto de breaker liga su propia zona, con su 0, su 1 y su instante
(`engine/zonas.zona_del_punto`). **Lo que no esta hecho es lo de DENTRO de la sesion**: varios
escenarios, sus intentos y que pasa con lo que queda vivo al cambiar de sesion.

### 0.2 Donde vive `liquidez_tomada`, y por que el bot opera una sola vez

- **El hecho** lo fija RN-004 (`alcanza_nivel` y `cruza` sobre `liquidez_m15`, la ultima M1
  cerrada; ADR-0062) y caduca al abrir cada sesion (`caduca: al_abrir_sesion`, F33). Lo consumen los
  predicados del productor (`se_da_esquema`, `toca_colocar_orden_limite`), no una regla.
- **La toma del productor** (`engine/zonas.py`, `_anotar_toma`) se guarda UNA vez por sesion: «la
  primera vez que el hecho aparece encendido en ella». Despues, el productor no mira si se toma otra
  liquidez: la referencia de la sesion es esa toma hasta que acaba.
- **La razon de una sola operacion por sesion** es otra, y esta en `engine/primitivas_broker.py`
  (`toca_colocar_orden_limite`): la DECISION 2 de ADR-0064, «una sola vida de orden por sesion que
  llega a llenarse. Tras un llenado, la sesion no coloca otra orden, como la zona de un solo uso que
  habia antes. Los cartuchos siguen sin geometria». Antes de F33 era una por DIA, porque la toma no
  caducaba (ADR-0055 §4).
- **Los cartuchos no existen en el motor.** El acumulador `cartuchos` es un hueco con nombre
  (`HUECOS` en `primitivas_broker.py`), asi que RN-016 nunca dispara; y si disparara,
  `detenido_por_cartuchos` no tiene quien lo apague: `cartuchos_reinicio` =
  `siguiente_liquidez_m15` no tiene mecanismo (lo dicen las notas de RN-004 desde el 2026-09-20).
- **Una toma de antes de abrir la sesion cuenta.** `cruza` (`domain/pivotes_m15.py`) mira donde
  CIERRA la ultima M1, no si cruza: da SI en cada M1 que cierre pasada la linea. Si el precio tomo el
  pivote a las 6:45 y sigue pasado a las 07:00, RN-004 dispara a las 07:00 (es la nota de A-43). Y lo
  mismo a las 11:00 con un pivote tomado en la sesion de la manana: **la toma de la manana vale en la
  tarde por la puerta de atras**, aunque F33 haga caducar el hecho, porque RN-004 lo vuelve a fijar
  en la apertura sobre el mismo pivote. Eso contradice A-46. **Medido** sobre un dia sintetico
  (`anexos/ESCENARIOS-POR-SESION/puerta_de_atras.py`): la toma de la manana cae trece minutos antes
  de las 11:00 y el precio sigue bajando sin vela contraria; RN-004 vuelve a fijar el hecho en el
  primer minuto de la tarde, sobre el MISMO pivote. Y lo fija en cada M1 que cierra pasada la linea
  (105 veces en esa tarde): «la toma» no es un instante sino un estado, y el productor se queda con
  el primero.
- **La orden pendiente de una sesion sigue viva en la siguiente** (DECISION 3 de ADR-0064): no se
  reubica con los puntos de la tarde (`_punto_nuevo` exige que la orden sea de la sesion) y, como
  RN-011 no coloca mientras haya una pendiente, **bloquea la tarde entera** hasta la ventana, el
  llenado o el final del dia.

### 0.3 Lo que dijo el trader (desde la evidencia y el feedback, no de memoria)

| Que | Cita | Fuente |
|---|---|---|
| Las dos sesiones son independientes | «tú básicamente distingues ambas sesiones. O sea, cada uno es un mundo diferente. Claro, exacto. [...] No, no importa cómo terminó la primera operación.» | `fb-2026-09-29-sesion-03-5021677e` (A-46 RESUELTA), `ev-v9-003253-2ac6060a`, `ev-v9-003303-818a0796` |
| Sin tope de escenarios | «Pues, eso no lo podemos definir. [...] en todas estas 4 se va a dar una operación» | `ev-v9-003318-c0503fe5` |
| Tres intentos por liquidez, no por dia | «Sí, serían tres intentos por liquidez. [...] ¿El máximo es por día? No, no, por liquidez.» | `ev-v9-013054-d49a544e` (A-41 RESUELTA) |
| El break even y la invalidada no gastan | «¿Cuentan los break-even y las entradas invalidadas? no cuentan» | `ev-v9-013117-c683f9b5` |
| Tras una ganadora, otra liquidez | «pues trazamos nuevamente liquidez, o sea, ya aquí está el trade ganador, aquí no buscamos nada, [...] pues tenemos que esperar nuevamente a que se desarrolle la liquidez» | `ev-v6-003227-c4efcf49` |
| Tras perder, quedan cartuchos en la misma liquidez | «nuevamente tiene todavía un gatillo, o sea, un cartucho [...] y luego esperar a que si no sea esta entrada que desarrolle otra zona de liquidez» | `ev-v3-002405-a202dbf6` |
| Una liquidez formada antes de las 7 vale si se toma dentro | «si la liquidez se formó antes de las 7, pero el precio la toma ya dentro. Es valio la entrada, sí.» | `ev-v9-004533-d075b080` (A-43) |

**Una precision sobre A-46.** El registro `fb-…-5021677e` sostiene que las sesiones son
independientes y que no importa como acabo la primera operacion. La frase de `ambiguedades.yaml`
«cada toma nueva de M15 abre un escenario, sin tope diario de escenarios» dice mas que el registro:
lo de «sin tope» sale de `ev-v9-003318`, y que una toma NUEVA abra escenario dentro de la misma
sesion, de la evidencia de antes (`ev-v6-003227`, `ev-v3-002405`). Aqui se cita cada parte con su
fuente.

### 0.4 Lo que depende de preguntas abiertas de la sesion 4

| Pregunta (docs/sesion-4/PREGUNTAS.md) | Ambiguedad | Que decide |
|---|---|---|
| 5. La orden sin llenar al acabar la sesion | A-30 y A-39 | que pasa con la orden pendiente al cambiar de sesion |
| 15. Una liquidez tomada antes de las 7 | A-43 | si una toma anterior a la primera sesion cuenta |
| 18. Los intentos: ¿por marca o por toma? | A-25 | si una toma nueva con el escenario vivo empieza con los intentos enteros |

## 1. El diseño

**Un escenario es una liquidez de M15 tomada dentro de una sesion, con sus intentos.** Vive en el
productor (`engine/zonas.py`), sesion a sesion, y guarda la toma (instante, nivel, lado y el pivote
tomado), sus intentos gastados y si ha terminado.

1. **Las sesiones siguen siendo independientes** (F33, A-46): una sesion empieza sin escenario.
2. **Una toma solo cuenta si ocurre dentro de la sesion.** RN-004 gana una condicion: el pivote no
   puede haberse tomado ya -una M1 cerrada pasada la linea con el criterio de la toma- entre su
   formacion y la apertura de la sesion.
   - Si esa toma previa fue en una sesion anterior del dia, **no cuenta**: es A-46 («cada uno es un
     mundo diferente»), no una pregunta abierta.
   - Si fue antes de la primera sesion (antes de `ventana_inicio`), lo decide el parametro
     `toma_antes_de_la_ventana` (pregunta 15, A-43): **PROVISIONAL `no_cuenta`**, por
     `ev-v9-004533` («la toma tiene que ser dentro»). La otra opcion, `cuenta`, es lo que hace hoy el
     motor.
3. **Nace un escenario** con la primera toma de la sesion, y con cada toma NUEVA -la de un pivote
   distinto del de la toma del escenario- cuando el anterior ha terminado. Lo abre la accion nueva
   `abrir_escenario`, que RN-004 hace junto con fijar el hecho; con el mismo pivote no hace nada.
4. **Termina un escenario**:
   - cuando una operacion suya se cierra en ganancia: «ya aquí está el trade ganador, aquí no
     buscamos nada, [...] esperar nuevamente a que se desarrolle la liquidez» (`ev-v6-003227`). Lo
     hace una regla nueva, RN-034, con la accion nueva `terminar_escenario`;
   - cuando gasta sus intentos: RN-016 con el acumulador `cartuchos`, que deja de ser un hueco y
     cuenta las perdidas del escenario con el mismo criterio que las dos ramas de RN-016
     («tres intentos por liquidez», `ev-v9-013054`);
   - cuando acaba la sesion (A-46).
   Tras una perdida, un break even o un equal el escenario SIGUE, con los intentos que le queden: la
   orden vuelve a nacer en el siguiente punto de breaker de la misma liquidez (`ev-v3-002405`; el
   break even y la invalidada no gastan, `ev-v9-013117`). **Esto sustituye la DECISION 2 de
   ADR-0064** (una sola vida de orden por sesion que llega a llenarse), que se escribio porque los
   cartuchos no existian.
5. **Una toma nueva con el escenario VIVO** (sin ganar ni agotar) la decide el parametro
   `intentos_tras_toma_nueva` (pregunta 18, A-25): **PROVISIONAL `vuelven_a_cartuchos_max`** -abre
   un escenario nuevo con los intentos enteros-, por «tres intentos por liquidez» (`ev-v9-013054`);
   la otra opcion, `siguen_los_que_quedan`, sigue el mismo escenario sobre la toma nueva con los
   intentos que le quedaban. En los dos casos la orden pendiente, si la hay, la reubica RN-006 en el
   primer punto de la toma nueva: es la frase del trader de que la orden «sigue vivo hasta que se
   desarrolle otra próxima, otro posible punto de breaker» (A-38, v9 1:32:07).
6. **Cuantos por sesion: sin tope** (`ev-v9-003318`). Lo acotan las tomas de la sesion y RN-018
   (una operacion a la vez).
7. **El reinicio de los cartuchos** (`cartuchos_reinicio` = `siguiente_liquidez_m15`, que ya decia
   el registro) es abrir un escenario: `abrir_escenario` apaga `detenido_por_cartuchos`. Las otras
   opciones del parametro no tienen contrato y el motor las rechaza con nombre.
8. **La orden pendiente al abrir la sesion siguiente** la decide el parametro
   `orden_pendiente_al_abrir_sesion` (pregunta 5, A-30 y A-39) con una regla nueva, RN-035:
   **PROVISIONAL `se_retira`**, por A-46 (la sesion siguiente es otro mundo). La otra opcion,
   `sigue_hasta_ventana_fin`, es lo que hace hoy el motor (DECISION 3 de ADR-0064). La opcion (b)
   de la pregunta 5, «la dejo y la sigo moviendo en la sesión siguiente», no se escribe: queda para
   despues de la sesion 4. Una posicion ABIERTA no entra aqui: la cierra RN-002 un minuto antes del
   fin de su vela H4, que en verano es el fin de la sesion.

**Lo que no cambia**: el criterio de los segmentos de la sesion, el sesgo (RN-003 al abrir), la caja
y el punto de la orden (ADR-0064), RN-006, y todo con `orden_limite_nace` = `al_darse_el_esquema`.

**Las piezas**: un ADR nuevo (el siguiente libre, tras ADR-0065), tres parametros DEFAULT_AMBIGUOUS con su `ambiguedad_id`, un
predicado nuevo (`la_toma_es_de_la_sesion`, con cita: entra en las tres guardias de
`spec/modelo.py`, que ya recorren los predicados), dos acciones nuevas (`abrir_escenario`,
`terminar_escenario`), dos reglas nuevas (RN-034, RN-035), RN-004 con una condicion y una accion mas,
y `Momento` con el inicio de la sesion y de la ventana.

## Estado

EN CURSO: Fase 0 escrita (diseño, antes de implementar); falta la Fase 1.
