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
| Las dos sesiones son independientes (lo resume el consultor y el trader lo confirma: «Claro, exacto»; la segunda frase es suya) | «tú básicamente distingues ambas sesiones. O sea, cada uno es un mundo diferente. Claro, exacto. [...] No, no importa cómo terminó la primera operación.» | `fb-2026-09-29-sesion-03-5021677e` (A-46 RESUELTA), `ev-v9-003253-2ac6060a`, `ev-v9-003303-818a0796` |
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
     buscamos nada, [...] pues tenemos que esperar nuevamente a que se desarrolle la liquidez»
     (`ev-v6-003227`). Lo
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

> **CORRECCION (2026-10-02, misma rama, revisor a2).** Lo ultimo no es verdad, y no se habia
> medido: el escenario es de la sesion y no del productor de la orden, asi que con
> `al_darse_el_esquema` tambien actua -una ganadora termina la liquidez, y cada toma nueva borra el
> esquema y la zona de la sesion y deja ligar otra-. Es la misma regla para las dos lecturas de A-29;
> lo que no cambia en esa lectura es como nace la zona (el esquema). Los tests de esa lectura
> (`test_sesiones_independientes.py`) siguen en verde, y uno nuevo lo fija:
> `test_con_la_orden_en_el_esquema_el_escenario_tambien_manda`. Hoy el valor de
> `orden_limite_nace` es `al_aparecer_punto_de_breaker`.

**Las piezas**: un ADR nuevo (el siguiente libre, tras ADR-0065), tres parametros DEFAULT_AMBIGUOUS con su `ambiguedad_id`, un
predicado nuevo (`la_toma_es_de_la_sesion`, con cita: entra en las tres guardias de
`spec/modelo.py`, que ya recorren los predicados), dos acciones nuevas (`abrir_escenario`,
`terminar_escenario`), dos reglas nuevas (RN-034, RN-035), RN-004 con una condicion y una accion mas,
y `Momento` con el inicio de la sesion y de la ventana.

## 2. Fase 1 · Lo implementado (`066246b`)

El diseño de §1, tal cual, con ADR-0066 (nuevo, ACTIVE y PROVISIONAL en tres parámetros) y
`spec_version` 15.2.1 → **15.3.0** (se añaden dos reglas y tres parámetros; ninguna regla cambia de
sentido). El commit lleva `Fuente:` con ADR-0066, `fb-2026-09-29-sesion-03-5021677e`,
`ev-v9-004533-d075b080`, `ev-v9-013054-d49a544e` y `ev-v6-003227-c4efcf49`.

**Spec** (`knowledge/spec/`, y `docs/spec/` regenerado):
- **RN-004**: la condición `la_toma_es_de_la_sesion` y la acción `abrir_escenario`; declara
  `decision: ADR-0066`.
- **RN-034** (nueva, disparador): una ganadora termina su escenario (`terminar_escenario`).
  `complementa: [RN-017]`, porque las dos disparan con el mismo cierre y valen en cualquier orden.
- **RN-035** (nueva, disparador): la orden pendiente al abrir otra sesión, `retirar_orden_limite`
  según `orden_pendiente_al_abrir_sesion`. La acción gana el argumento `segun`, y la ligadura
  `ORDEN` entra en los tokens.
- **RN-016**: sin cambio de forma; sus notas dicen que desde hoy puede disparar.
- **Hechos y acumulador**: `liquidez_tomada`, `detenido_por_cartuchos`, `orden_limite_pendiente`
  (consume RN-035) y el acumulador `cartuchos`, con su descripción al día.
- **Parámetros** (DEFAULT_AMBIGUOUS, `categoria: estrategia`, citados por lo que sostiene el valor):

| Parámetro | Valor PROVISIONAL | Otra opción | Ambigüedad | Pregunta de la sesión 4 | Fuente |
|---|---|---|---|---|---|
| `toma_antes_de_la_ventana` | `no_cuenta` | `cuenta` (lo de antes) | A-43 | 15 | `ev-v9-004533-d075b080` |
| `intentos_tras_toma_nueva` | `vuelven_a_cartuchos_max` | `siguen_los_que_quedan` | A-25 | 18 | `ev-v9-013054-d49a544e` |
| `orden_pendiente_al_abrir_sesion` | `se_retira` | `sigue_hasta_ventana_fin` (lo de antes) | A-30 (y A-39) | 5 | `fb-2026-09-29-sesion-03-5021677e` |

- **Las tres guardias de cita.** El sitio nuevo con `cita` propia es un predicado más, y la de
  `predicados` ya la recorren `comprobar_contra`, `comprobar_literales` y
  `comprobar_citas_revocadas` (`botsito spec check`: OK, 35 reglas). Las dos reglas nuevas citan
  como cualquier regla. Las acciones nuevas no llevan cita, como las demás menos
  `colocar_orden_limite`.

**Motor** (`src/botsito/engine/`):
- `interprete.Momento` lleva `desde_sesion` y `desde_ventana`, que ponen `motor.py` y `cableado.py`.
- `primitivas.py`: el predicado, y la acción `abrir_escenario`, que va con las primitivas escritas
  haya geometría o no.
- `zonas.py`: la lista de escenarios por sesión. Un escenario terminado no coloca.
- `primitivas_broker.py`: el acumulador `cartuchos` (sale de `HUECOS`), `terminar_escenario`,
  `retirar_orden_limite` con `segun`, y fuera el envoltorio de la DECISION 2 de ADR-0064.
- `cableado.py`: guarda los cierres del día para contar los intentos de cada escenario.
- ADR-0064 lleva un recuadro en sus decisiones 2 y 3 que apunta a ADR-0066.

**Dos tests existentes cambian a propósito:**
- `test_spec_fidelidad.py::test_la_pendiente_a_las_15_esta_declarada_como_ambiguedad_y_no_supuesta`
  exigía que ninguna regla usara `retirar_orden_limite` hasta que el trader respondiera A-30. Ahora
  exige que la única que la usa, RN-035, lo haga según un parámetro DEFAULT_AMBIGUOUS de A-30: sigue
  sin suponerse la respuesta.
- `test_arnes_motor.py::test_no_implementada_detiene_la_sesion_y_queda_registrada`: sin lectura de
  «formado», la traza de RN-004 nombra también el predicado nuevo.

## 3. Fase 2 · Comprobación, sin cobertura agregada

### 3.1 Tests sintéticos (`tests/unit/test_escenarios_por_sesion.py`, 13 casos)

Todos sobre días y velas de 2030, con la spec real:

| Lo que pide el encargo | Test |
|---|---|
| Dos sesiones independientes | `test_dos_sesiones_independientes_cada_una_con_sus_escenarios`; y los de F33 (`test_sesiones_independientes.py`) siguen en verde |
| Una toma nueva tras una operación cerrada abre un escenario nuevo | `test_una_toma_nueva_tras_una_ganadora_abre_un_escenario_nuevo` (la misma liquidez no abre nada); por el cableado, `test_por_el_cableado_la_ganadora_termina_su_escenario` |
| La liquidez de la mañana no vale para la tarde | `test_la_liquidez_de_la_manana_no_vale_para_la_tarde`: el día de §0.2, en el que hasta hoy RN-004 volvía a fijar la toma en la tarde |
| Una orden viva al cambiar de sesión, según el diseño | `test_la_orden_viva_al_cambiar_de_sesion_segun_el_parametro`: con `se_retira`, cancelada en la apertura de la tarde; con `sigue_hasta_ventana_fin`, al final del día |

Y las piezas:
- **La toma antes de la ventana.** Con los dos valores, y la M1 que cierra justo en la apertura:
  `test_la_toma_antes_de_la_ventana_la_decide_el_parametro`. Una toma de la sesión anterior no
  cuenta con ninguno: `test_una_toma_de_la_sesion_anterior_no_cuenta_nunca`.
- **La pregunta 18**, con las dos opciones:
  `test_una_toma_nueva_con_el_escenario_vivo_la_decide_el_parametro`.
- **El reinicio de los cartuchos**: `test_abrir_un_escenario_es_el_reinicio_de_los_cartuchos`.
- **Un escenario terminado no coloca**: `test_un_escenario_terminado_no_coloca_mas`.
- **Por el cableado, tras una pérdida el escenario sigue y gasta un intento.** Con
  `cartuchos_max` = 1, RN-016 dispara por primera vez y deja `detenido_por_cartuchos`:
  `test_por_el_cableado_tras_una_perdida_el_escenario_sigue_y_cuenta_el_intento`.

`make check` del commit: 1806 pasados.

### 3.2 Con el visor: tres días de agosto, antes y ahora

**Los días.** El 3, el 7 y el 20 de agosto de 2026: construcción, con operaciones del trader en
la mañana y en la tarde. Comprobados por la compuerta del visor: `visor.caso_de_construccion` cruza
cada caso con `casos_ocultos` antes de leerlo, y `casos_ocultos` es `casos_reservados`
(`cases/holdout.py`). Ningún día se negó.

**Cómo se corrió.**
- **Ahora**: la rama.
- **Antes**: `main` (`a093ffb`) en un worktree desechable fuera del repositorio, con
  `config/settings.local.toml` apuntando a la misma `data/`.
- Las dos con `botsito motor visor --caso <c> --simular` y las lecturas de diagnóstico de la
  medida de F35 (A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control`,
  A-27 a 0). **Es DIAGNÓSTICO: nada de esto cuenta como medida.**
- El detalle por sesión lo saca `anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`, que monta el mismo
  motor cableado. Horas de Madrid.

> **CORRECCION (2026-10-02, misma rama, revisor b1).** Este apartado ponia las horas de las
> operaciones del trader junto a las del bot y comparaba una direccion, y eso deja emparejar a mano.
> Ya no las lleva: de cada dia se dice solo que el trader opero en las dos sesiones, y lo que hace
> el bot.

**3 de agosto.** El trader opera en las dos sesiones.
- Mañana: el bot no coloca ninguna orden, ni antes ni ahora. Ahora la mañana tiene dos escenarios
  (tomas a las 07:47 y 09:32), sin ninguna colocación.
- Tarde, **antes**: una sola vida de orden. Colocada a las 11:48, reubicada a las 11:51, llenada a
  las 11:51:57 y cerrada a la entrada a las 11:55 (break even). Nada más: la DECISION 2 de ADR-0064
  cerraba la sesión tras el llenado.
- Tarde, **ahora**: el mismo comienzo, y la sesión sigue.
  - Una toma nueva a las 13:02 abre el escenario 2: orden a las 13:04, reubicada a las 13:06,
    llenada a las 13:06:13 y al stop a las 13:09.
  - La toma de las 13:49 abre el escenario 3: orden a las 13:56, reubicada a las 14:03, llenada a
    las 14:03:38 y al stop a las 14:04.
  - La toma de las 14:17 abre el escenario 4, sin orden.

**7 de agosto.** El trader opera en las dos sesiones.
- Mañana, **antes**: una toma (07:22) y una orden rechazada a las 07:35 (el precio ya había pasado
  el punto, ADR-0064 decisión 1); nada más.
- Mañana, **ahora**:
  - el mismo rechazo, en el escenario 1;
  - otra orden rechazada a las 08:44 en el escenario 3 (toma de las 08:42);
  - en el escenario 4 (toma de las 10:12), una compra llenada a las 10:15 y cerrada a la entrada a
    las 10:26.
- Tarde, **antes**: una toma a las 11:01 y ninguna orden.
- Tarde, **ahora**: cinco escenarios (tomas a las 11:01, 11:47, 13:02, 13:39 y 14:31) y tres
  órdenes que no se llenan:
  - colocada a las 13:43 y cancelada a las 13:49;
  - colocada a las 14:34 y reubicada a las 14:38;
  - esa reubicada, cancelada a las 14:43 sin otra detrás.

**20 de agosto.** El trader opera en las dos sesiones.
- Mañana, **antes**: una venta llenada a las 08:02 y al stop a las 08:10; después nada, por la
  DECISION 2.
- Mañana, **ahora**:
  - la misma venta al stop, que gasta un intento del escenario 1;
  - en el escenario 2 (toma de las 08:46), una venta llenada a las 09:02 que **llega al objetivo a
    las 09:28**, y RN-034 termina ese escenario;
  - en el escenario 3 (toma de las 09:42), una venta llenada a las 09:45 y al stop a las 09:59;
  - en el escenario 4 (toma de las 10:42), una venta llenada a las 10:47 y al stop a las 10:51.
- Tarde, **antes**: una compra llenada a las 12:50:01 y al stop a las 12:50:32.
- Tarde, **ahora**:
  - la misma compra al stop;
  - en el mismo escenario 1, una orden nueva a las 12:51, cancelada a las 12:57 (el reintento tras
    la pérdida);
  - en el escenario 2 (toma de las 13:43), una compra llenada a las 13:49:09 y al stop a las
    13:50:37, y otra orden a las 13:51 cancelada a las 13:56.

**Lo que se ve en los tres días.**
- El bot ya no se para tras el primer llenado de la sesión.
- Cada toma de una liquidez nueva abre un escenario, y en sesiones con mucho movimiento son
  muchos: cinco en la tarde del 7.
- Tras una pérdida reintenta en la misma liquidez, y tras la ganadora del 20 espera otra.
- Ninguna orden quedó pendiente al cambiar de sesión, así que RN-035 no actuó en estos días.
- Ningún escenario llegó a gastar sus tres intentos.

### 3.3 La cobertura: ni se calculó ni se pega

- **Lo que no se ejecutó**: el arnés sobre construcción, `scripts/embudo_77.py` y cualquier
  recuento de parejas.
- **Lo que ya imprime una cifra de cobertura sin pedirlo:**
  - `docs/validation/NOCTURNO-01OCT.md` §2, un informe ya cerrado, con la cobertura sobre las 77
    operaciones;
  - la cabecera de cada página del visor, «parejas del criterio N», por día.

Ninguna de las dos cifras se copia aquí. §3.2 no da las horas ni las direcciones de las operaciones
del trader, así que no deja emparejar las del bot con las suyas (corregido tras el revisor, b1).

## 4. Lo que queda para después de la sesión 4

- **Pregunta 5** (A-30, A-39): fijar `orden_pendiente_al_abrir_sesion`. Si el trader elige «la dejo
  y la sigo moviendo en la sesión siguiente», hay que escribir esa opción: hoy no existe.
- **Pregunta 15** (A-43): fijar `toma_antes_de_la_ventana`.
- **Pregunta 18** (A-25): fijar `intentos_tras_toma_nueva`. Y lo que A-25 deja aparte, la marca
  más reciente frente a la anterior («alto nuevo más bajo [...] si no se da entrada, pues seguimos
  al más alto», `ev-v9-013736-463282d5`): el motor sigue el pivote más reciente (ADR-0045) y no
  vuelve al anterior.
- **Para el consultor, no para el trader:**
  - ~~**Que el escenario siga tras un break even** es lectura nuestra (RN-034, notas).~~ **Ya no
    (2026-10-02, §6.1):** lo dijo el trader dos veces, `ev-v4-004832-6543b551` y
    `ev-v9-013117-c683f9b5`, y RN-034 y ADR-0066 lo citan.
  - **Cuántos escenarios abre una sesión movida.** Cada pivote nuevo tomado abre uno, y en la tarde
    del 7 son cinco. Es lo que dicen la spec y A-46 («sin tope de escenarios»); si se ve demasiado,
    la pregunta es qué es para el trader una liquidez NUEVA. **Desde el 2026-10-02 (§6.2) es un
    parámetro**, `max_escenarios_por_sesion`, PROVISIONAL `sin_limite`, con la pregunta 20.
  - **Una liquidez tomada antes de abrir la sesión queda muerta en ella, aunque el precio vuelva
    dentro y la tome otra vez** (revisor, a3). `la_toma_es_de_la_sesion` mira si ALGUNA M1 cerró
    pasada la línea entre la formación del pivote y la apertura, porque `cruza` es un estado y no
    un cruce. Es una decisión de este diseño, no del trader. Con `no_cuenta`, una liquidez tomada a
    las 6:45 que el precio recupera y vuelve a tomar a las 7:20 no vale, y la frase del trader
    («si el precio la toma ya dentro») admite leerlo al revés. Va con la pregunta 15. En la tarde,
    con una toma de la mañana, es lo mismo, y lo sostiene A-46. **Desde el 2026-10-02 (§6.3) la
    pregunta 15 lleva una segunda parte con este caso.**
  - **Una orden pendiente cuando una toma nueva abre otro escenario** (revisor, b2). §1.5 dice que
    la reubica RN-006 en el primer punto de la toma nueva. Es lectura del código (`_punto_nuevo`
    mira las zonas usadas de la SESIÓN, no del escenario), **no está medido ni tiene test**, y en
    los tres días de §3.2 no pasó. **Desde el 2026-10-02 (§6.4) está medido con un test, es un
    parámetro** (`orden_pendiente_al_abrir_escenario`, PROVISIONAL `se_mueve`) **y va en la
    pregunta 21.**

## 5. Informe del revisor

Subagente `revisor`, sobre `main..HEAD` (`fad197e`, `ae6c7b3`, `066246b`) más el informe estadiado.
Los hallazgos, tal cual; lo comprobado sin hallazgos, resumido.

> ## Informe del revisor · feature/escenarios-por-sesion · 2026-10-02
>
> Alcance: `main..HEAD` (`fad197e`, `ae6c7b3`, `066246b`) más lo estadiado (informe con Fases 1-2 y `dia_del_bot.py`). Las restricciones del encargo se cumplieron. Una salvedad: al contrastar la cita de `NOCTURNO-01OCT.md` (un `grep` de «cobertura|77») salió impresa una línea con la cobertura de ese informe cerrado, que no calculé ni uso.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 1 bloquea, 3 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | **bloquea** (por la letra de CLAUDE.md; hay precedente reciente sin fila, decide el consultor) | No hay fila en `HOLDOUT-EXPOSICIONES.md` por la lectura de los días de agosto. El informe (§3.2) cuenta que el visor leyó los días 3, 7 y 20 de agosto y da las horas de las operaciones del trader de cada día (salen del detalle por operación del xlsx de agosto). CLAUDE.md: material de desarrollo «se declara igual el mismo día»; «toda exposición se declara… siempre». | `git diff main...HEAD --stat` no toca `docs/validation/HOLDOUT-EXPOSICIONES.md`; la última fila es del 2026-09-30. Hay filas análogas de lecturas ya vistas el 2026-09-23 y 2026-09-28. Los tres casos NO están en `casos_reservados` (comprobado: los tres `False`). |
> | a2 | importa | El diseño dice «Lo que no cambia: … todo con `orden_limite_nace` = `al_darse_el_esquema`». El código sí lo cambia para esa opción: `toca_colocar_orden_limite` llama a `_anotar_toma` y devuelve NO si el escenario está terminado antes de ramificar por `momento_orden`; `_abrir` borra `esquema` y `zona_id`, y `_ligar_al_escenario` se llama también en la rama de `al_darse`. Ningún test nuevo lo cubre. La afirmación del informe es falsa o no está medida. | `src/botsito/engine/zonas.py`; informe §1. |
> | a3 | importa | Decisión de diseño no declarada: `la_toma_es_de_la_sesion` usa «alguna M1 anterior cerró pasada la línea» (`cruza` es un estado, no un cruce). Un pivote que cerró fuera una vez entre su formación y la apertura queda muerto en esa sesión, aunque el precio vuelva dentro y lo tome de nuevo. Mismo efecto con `no_cuenta` antes de las 7 (el trader dice que vale «si el precio la toma ya dentro») y en la tarde. No se declara ni se deja para después de la sesión 4. | `primitivas.py` (diff); el test `_Datos` solo prueba tomas que siguen debajo. |
> | a4 | importa | `test_un_escenario_terminado_no_coloca_mas` dice «no liga zona en un escenario terminado, y sí en el siguiente» y solo comprueba la primera mitad. No hay test de «intentos agotados» de punta a punta, y la rama de intentos agotados no marca `terminado`: se apoya en el gate de RN-016 y en `HECHO_DETENIDO`. Correcto por lectura del código, pero el docstring de `zonas.py` y el informe dicen «termina … sin intentos». | `tests/unit/test_escenarios_por_sesion.py`; `zonas.py`. |
> | a5 | menor | La cita de dos sitios nuevos sostiene menos de lo que declaran: el predicado `la_toma_es_de_la_sesion` cita `ev-v9-004533` (solo A-43) y su descripción añade la parte de A-46; RN-035 cita la independencia de sesiones, que no dice «se retira» (las notas lo admiten, PROVISIONAL). | `strategy_spec.yaml` (diff). |
> | a6 | menor | Las citas del informe y del ADR para RN-034 quitan «pues tenemos que» sin marcarlo; y la tabla §0.3 pone como cita del trader «tú básicamente distingues ambas sesiones…», que es del consultor y el trader confirma («Claro, exacto»). | informe; `ev-v9-003253-2ac6060a.yaml`; ADR-0066 §2. |
> | a7 | menor | A-30, A-39 y A-43 siguen con `parametros: []` y A-25 solo con `cartuchos_reinicio`, aunque los tres parámetros nuevos llevan su `ambiguedad_id` (patrón de A-29). Nada lo exige hoy. RN-035 está colocada antes de RN-003 en el fichero. | `ambiguedades.yaml`; `strategy_spec.yaml`. |
>
> Comprobado sin hallazgos: el contrato (ninguna ruta protegida tocada); `botsito spec check` y `botsito state check`; el `Fuente:` de `066246b` (todos los ids existen); las citas y literales de §0.3, RN-034 y el predicado; las preguntas 5, 15 y 18; el diseño (`ae6c7b3`) commiteado antes que la implementación (`066246b`) y sin cambios entre los dos; los regímenes de cambio (evidence, feedback, manifests, corpus, holdout intactos); los tres parámetros DEFAULT_AMBIGUOUS; `test_no_business_literals`; las tres guardias de cita recorren `predicados`; `spec_version` y `docs/spec/`; ADR-0066 y su índice; la lógica del motor (la identidad del pivote, el acumulador `cartuchos` frente a las ramas de RN-016, `terminar_escenario`, `retirar_orden_limite`, la M1 de la apertura); los dos tests que cambian lo hacen con motivo y sin rebajar.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 12 hechos, 2 parciales (Fase 0 sin A-35 analizada; citas que dicen algo más), 0 no hechos.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | La Fase 2 empareja de hecho: las horas de las operaciones del trader van justo antes de las del bot, y el 20 de agosto compara dirección. No hay una cifra pegada, pero la afirmación de §3.3 es más fuerte que lo que §3.2 hace. | informe §3.2 y §3.3 |
> | b2 | importa | «En los dos casos la orden pendiente la reubica RN-006 en el primer punto de la toma nueva» (§1.5) no está medida ni probada por ningún test. | informe §1.5 |
> | b3 | menor | Fase 0 no analiza A-35 ni RN-006 como piezas que «tocan esto» (el encargo los nombra). | informe §0 |
> | b4 | menor | Que RN-002 cierra la posición «un minuto antes del fin de su vela H4, que en verano es el fin de la sesión» no se midió en esta rama. | informe §1.8; ADR-0066 §4 |
>
> ### Lo que no pude comprobar
> `make check` y el «1806 pasados» (no hay log en el árbol); `puerta_de_atras.py`; las horas, órdenes y escenarios por día de §3.2 (piden correr el motor sobre `data/`); si el consultor da por cubierta con filas anteriores la lectura de hoy; el efecto de a2 con el valor vigente; lo de RN-002 en verano.

**Respuesta de la sesion, hallazgo a hallazgo:**
- **a1, arreglado**: fila del 2026-10-02 en `HOLDOUT-EXPOSICIONES.md` (los tres días, qué se leyó,
  la compuerta, y que las «parejas del criterio» del visor no se copian). El contrato se amplía a
  ese fichero, con su motivo.
- **a2, arreglado**: recuadro de corrección en §1 y un test nuevo,
  `test_con_la_orden_en_el_esquema_el_escenario_tambien_manda`. Es la misma regla para las dos
  lecturas de A-29, a propósito.
- **a3, declarado**: en §4, como decisión de este diseño que va con la pregunta 15.
- **a4, arreglado**: el test comprueba ya las dos mitades -el escenario terminado no liga zona y
  el siguiente sí-, sobre las M1 de `test_orden_stop_pivote`. El docstring de `zonas.py` dice cómo
  acaba un escenario sin intentos: no se marca terminado; lo para `detenido_por_cartuchos` hasta la
  toma siguiente. El RN-016 de punta a punta está en
  `test_por_el_cableado_tras_una_perdida_el_escenario_sigue_y_cuenta_el_intento` (con
  `cartuchos_max` = 1).
- **a5, declarado sin tocar la spec**: la parte de A-46 del predicado la sostiene
  `fb-2026-09-29-sesion-03-5021677e`, que cita RN-004 en sus notas; RN-035 ya se declara
  PROVISIONAL con su pregunta. Cambiar la descripción obligaba a otra versión de la spec por una
  redacción.
- **a6, arreglado**: la cita de RN-034 en el informe y en ADR-0066 lleva «pues tenemos que», y la
  tabla de §0.3 dice que la primera frase la resume el consultor y el trader la confirma.
- **a7, declarado**: que A-25, A-30, A-39 y A-43 apunten a su parámetro nuevo es una edición de
  `ambiguedades.yaml` que queda para la rama que fije sus valores tras la sesión 4.
- **b1, arreglado**: §3.2 ya no da las horas ni las direcciones de las operaciones del trader, con
  un recuadro de corrección; §3.3 dice lo que hace ahora.
- **b2, declarado**: en §4, como lectura del código sin medir.
- **b3**: A-35 no cambia aquí; es la lectura de «formado» de `liquidez_m15`, y la Fase 2 corre con
  ella en diagnóstico. RN-006 tampoco: su mecanismo (`_punto_nuevo`, ADR-0064) sigue igual y solo
  cambia que la orden pendiente de otra sesión ya no llega (RN-035).
- **b4**: no se midió en esta rama. Lo de verano sale de las notas de RN-001 («la ventana coincide
  con dos velas H4 completas 337 días al año»), y el cierre al minuto lo prueba
  `test_rn002_cierra_la_posicion_viva_antes_del_fin_de_su_vela_h4` (`test_cableado.py`).

## 6. Órdenes 2 y 3 del consultor (2026-10-02)

Las dos están copiadas tal cual en el encargo (`docs/encargos/feature-escenarios-por-sesion.md`,
«Segunda orden» y «Tercera orden»). Sigue sin cobertura agregada: nada de esta sección cuenta
parejas ni compara con las operaciones del trader.

### 6.1 Punto 0: dos búsquedas en el registro, y la versión vigente

Con `kb find` y `kb at`, filtrados (nada en cuarentena ni en tramos no citables):

- **a) «los break even no gastan un intento»: está en el registro, dos veces.**
  - `ev-v4-004832-6543b551` (v4 0:48:32-0:48:52), del trader: «los breakeven no se cuenta o sea, si
    te saca un breakeven es un trade que [...] tienes un cartucho todavía para poder seguir
    operando»;
  - `ev-v9-013117-c683f9b5` (sesión 3), pregunta y respuesta juntas: «¿Cuentan los break-even y las
    entradas invalidadas?» «no cuentan». El ítem tiene confianza media: la cruda no separa voces y
    el hablante se atribuye por contexto (revisor, a5).

  RN-034 (notas) y ADR-0066 §2 los citan, y ya no lo marcan como lectura nuestra.
- **b) «el día termina con la primera ganadora»: está en el registro, en v4, y NO es lo vigente.**
  La sesión se paró aquí y lo llevó al consultor, que confirmó la cadena (tercera orden):
  - `ev-v4-004936-d7004417` (v4 0:49:36, «apenas tengo el trade positivo ya no opero más») lo
    rechazó el trader en la sesión 1: `fb-2026-09-09-sesion-01-af02495f`, «NO. Que siga operando,
    pero que respete la regla de los 3 cartuchos de perdida»;
  - `ev-v4-011351-74b8bb39` (v4 1:13:51) lo sustituye `ev-v6-000732-f7189541`;
  - `ev-v1-000959-b82650ad` lo sustituye `ev-v6-000732-5945fd87` («no estamos pausando cuando se
    dé el trade ganador»).

  Lo vigente es la sesión 1: RN-017 (el día sigue) más RN-034 (en otra liquidez). La cadena está
  escrita en las notas de RN-034 y en ADR-0066 §2.

### 6.2 Punto 1: `max_escenarios_por_sesion`

- Parámetro nuevo, `enum` (`sin_limite`, `"1"` a `"5"`), DEFAULT_AMBIGUOUS, valor `sin_limite`,
  `ambiguedad_id` A-46, fuente `ev-v9-003318-c0503fe5`.
- **La subpregunta de la sesión 3 no se contestó con un número**: «eso no lo podemos definir [...]
  en todas estas 4 se va a dar una operación» (v9 0:33:18-0:33:40). Va como pregunta 20 de
  `docs/sesion-4/PREGUNTAS.md`, sección D, con la frase anterior de v4 («como máximo dos entradas
  por día», `ev-v4-003350-acb03ee7`) al lado.
- `abrir_escenario` lo recibe como `maximo` (RN-004): con el tope alcanzado, una toma de otra
  liquidez no abre escenario. Test: `test_el_tope_de_escenarios_por_sesion` (con `"2"`, tres tomas
  abren dos; con `sin_limite`, tres).

### 6.3 Punto 3: la pregunta 15, con la toma que vuelve

La pregunta 15 lleva una segunda parte para el caso de §4 (revisor, a3): la liquidez tomada a las
6:45, que el precio recupera y vuelve a tomar a las 7:20. Hoy el motor no la vuelve a contar
(`toma_antes_de_la_ventana` = `no_cuenta`, PROVISIONAL).

### 6.4 Punto 4: la orden viva cuando otra toma abre un escenario

**Lo que hacía el motor, medido.** Test sintético
`test_la_orden_viva_cuando_otra_toma_abre_un_escenario`, sobre el motor cableado con la spec real:
una toma a T1 coloca la orden de `zona:1`; una toma de OTRA liquidez a T2 abre el escenario 2 con
esa orden sin llenar; la liquidez nueva da su primer punto en T2 + 3.
- **`se_mueve`** (lo que hacía el motor antes de esta orden): la orden sigue viva -y se podía
  llenar- de T2 a T2 + 3, y en T2 + 3 RN-006 la cancela y RN-015 coloca la nueva en el punto de la
  liquidez nueva, en el mismo cierre de M1.
- **`se_retira`**: `abrir_escenario` la cancela en T2, y la liquidez nueva coloca la suya en T2 + 3.
- **En los dos, nunca hay dos órdenes vivas a la vez** (el test lo comprueba petición a petición),
  y las peticiones son las mismas cuatro: colocar `o1`, cancelar `o1`, colocar `o2` y cancelar `o2`
  al abrir la tarde (RN-035). Lo garantiza la spec, no el azar: RN-011 no prepara orden con una
  pendiente o una posición viva (`ninguno_de`), y `retirar_orden_limite` y
  `reubicar_orden_limite` se niegan con nombre (`CableadoError`) si hubiera dos.

**No sale de una regla del trader**: lo único que dijo de la vida de la orden («sigue vivo hasta que
se desarrolle otra próxima, otro posible punto de breaker», A-38, `fb-2026-09-29-sesion-03-c7fa3068`)
habla de la misma liquidez. Por eso es un parámetro, `orden_pendiente_al_abrir_escenario`
(`se_mueve` / `se_retira`), DEFAULT_AMBIGUOUS, valor `se_mueve` -lo que hacía el motor, no una
decisión-, A-25, y la pregunta 21 de la sección D.

**Las peticiones al servidor (R13: 2.000 al día en FTMO).**
- **El caso peor que se pidió, medido con un test sintético**
  (`test_cinco_escenarios_en_una_sesion_cuestan_dos_peticiones_cada_uno`, añadido tras el revisor,
  b1): cinco liquidez distintas tomadas en la misma sesión, cada una con la orden de la anterior
  todavía viva, sobre el mismo motor cableado. Con `se_mueve` y con `se_retira`, la secuencia es la
  misma: colocar `o1`, y por cada escenario nuevo cancelar la vieja y colocar la suya, y la retirada
  de RN-035 al abrir la otra sesión. **10 peticiones en el día: dos por escenario**, y nunca dos
  órdenes vivas. Frente a 2.000, cinco escenarios son el 0,5 %; para llegar al tope por esta vía
  harían falta unos mil escenarios en un día.
- **Medido, un día de desarrollo** (`caso-eurusd-2026-08-07`, el de la tarde de cinco escenarios;
  `anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`, que ahora imprime las peticiones del día: es el
  recuento de lo que emite el bot ese día, no una cifra de cobertura):
  - el día entero, con nueve escenarios: **10 peticiones** (6 colocar, 1 modificar, 3 cancelar) y
    como mucho **una orden pendiente a la vez**;
  - la tarde de cinco escenarios: **6 peticiones**, entre las 13 y las 15 h;
  - ese día ninguna toma abrió escenario con una orden viva: el caso del test no se dio.
  - Los otros dos días de §3.2: 10 (el 3) y 13 (el 20), también con una orden pendiente como mucho.
- **Lo que dice el código, sin medir un día peor:**
  - una evaluación por minuto, de la apertura de la primera sesión al cierre de la última, ambos
    incluidos: de 07:00 a 15:00, 481 cierres de M1 (el bucle `while instante <= ultimo` de
    `MotorSpec.correr_dia`, `engine/motor.py`); y cada regla dispara como mucho una vez por
    evaluación (punto fijo con refracción, `Interprete.evento`, `engine/interprete.py`);
  - abrir un escenario emite como mucho UNA petición (la cancelación con `se_retira`) o ninguna
    (`se_mueve`); llevar la orden al punto de la liquidez nueva son dos (cancelar y colocar), las
    mismas que una reubicación dentro de un escenario. **El número de escenarios no multiplica las
    peticiones; las multiplican las reubicaciones.**
  - **El código no garantiza el tope por sí solo**: siete reglas vigentes emiten peticiones
    (RN-002, RN-004, RN-006, RN-014, RN-015, RN-030 y RN-035); a una por minuto cada una, la cota
    trivial pasa de 2.000. El broker solo mide R13 y nada frena por peticiones (`engine/broker.py`,
    cabecera). No es nuevo de esta rama, y queda anotado aquí.

### 6.5 Lo que cambia en el código y la spec

- `knowledge/spec/parametros.yaml`: los dos parámetros nuevos.
- `knowledge/spec/strategy_spec.yaml` (15.3.0 → 15.4.0, y 15.4.1 tras el revisor por la redacción
  de RN-034): RN-004 pasa `maximo` y `orden_pendiente` a `abrir_escenario`; las notas de RN-034
  citan la cadena y los dos items del break even.
- `engine/zonas.py`: el tope en `abrir_escenario`; `engine/primitivas_broker.py`: el
  `abrir_escenario` del cableado, que retira la orden con `se_retira`.
- `docs/adr/0066-...`: §2 (la cadena, el break even y el tope) y §4 bis (la orden pendiente y las
  peticiones), y cinco parámetros PROVISIONAL en vez de tres.
- `docs/sesion-4/PREGUNTAS.md`: la segunda parte de la 15, y la 20 y la 21 (el contrato se amplía a
  ese fichero, con su motivo).
- Tests: los tres nuevos de §6.2 y §6.4 (el tercero, el caso peor, tras el revisor).

### 6.6 Informe del revisor (solo `7ab42d6..a43641b`)

Subagente `revisor`, sobre el commit `a43641b`. Los hallazgos, tal cual; lo comprobado sin
hallazgos, resumido.

> ## Informe del revisor · feature/escenarios-por-sesion (solo a43641b, desde 7ab42d6) · 2026-10-02
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | La pregunta 20 y la 21 cuelgan de A-46 y A-38 como `ambiguedad_id`, pero las dos están RESUELTAS. Los parámetros `max_escenarios_por_sesion` (A-46) y `orden_pendiente_al_abrir_escenario` (A-25 en el yaml, y la fuente es el registro de A-38) son DEFAULT_AMBIGUOUS. La pregunta 20 se rotula «A-46 (la subpregunta que quedó sin número)», pero ninguna ambigüedad abierta recoge esa subpregunta. A-46 dice «sin tope diario de escenarios» y cita `fb-2026-09-29-sesion-03-5021677e`, cuya `respuesta_literal` no habla de tope, y esto ya estaba antes. El informe no declara esta tensión. | `knowledge/spec/ambiguedades.yaml:1226-1235` (A-46 RESUELTA). Registro: `knowledge/feedback/2026-09-29-sesion-03/fb-2026-09-29-sesion-03-5021677e.yaml`. A-38 RESUELTA: `knowledge/spec/ambiguedades.yaml:971-977`. Parámetros: `knowledge/spec/parametros.yaml` (diff de a43641b). |
> | a2 | importa | El pie «Estado» de `PREGUNTAS.md` quedó desactualizado. Dice «Por preguntar: 19 [...] las 17 del barrido y 2 que añadió el consultor» y «No cambia nada del motor, de la spec, de las ambigüedades ni del feedback». El encabezado sí se actualizó a (21). Con la 20 y la 21 son 21 por preguntar, y la rama sí cambia motor y spec. | `docs/sesion-4/PREGUNTAS.md:45` («(21)») frente al párrafo bajo «## Estado» (~línea 366). |
> | a3 | menor | `dia_del_bot.py`: la rama `b is None` es código muerto. `ultimo_cambio_ms` vale 0 por defecto, no `None`. Una orden que quede pendiente al final del día sin modificarse cuenta con un tramo vacío, y una modificada sin cerrar cuenta solo hasta la modificación. La cifra «una orden pendiente a la vez» puede quedar corta en ese caso. El día 7 no sufre el defecto, porque sus 6 colocadas acaban en 3 cancelaciones y, por tanto, 3 llenadas. | `src/botsito/engine/broker.py:126` (`ultimo_cambio_ms: int = 0`), `:402`, `:411`, `:585`, `:597`. `docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py` (diff): `(t + 1 if b is None else b)`. |
> | a4 | menor | RN-034 (notas) y ADR-0066 conservan la frase «Hasta el 2026-10-02 esto se marcaba como lectura nuestra». La orden decía que deje de marcarse como lectura. Es historia dentro de la spec y de un ADR. | `knowledge/spec/strategy_spec.yaml` (diff, RN-034). `docs/adr/0066-...md` (diff, §2). |
> | a5 | menor | Se atribuye «lo dijo el trader, dos veces» a `ev-v9-013117-c683f9b5`. El propio ítem dice «revisión sin humana; la cruda no separa voces y el hablante se atribuye por contexto», con `confianza: media`. La cita es pregunta y respuesta juntas. El de v4 sí es del trader. | `knowledge/evidence/v9/ev-v9-013117-c683f9b5.yaml` (`revisado_por`, `confianza`). `docs/validation/ESCENARIOS-POR-SESION.md` §6.1. |
>
> Comprobado sin hallazgos: el contrato (28 ficheros, `PREGUNTAS.md` añadido con su motivo); `state check`, `spec check` y `spec docs`; los tests de `test_escenarios_por_sesion.py`, `test_kit`, `test_adr`, `test_project_state` y `tests/contract`; `spec_version` 15.3.0 → 15.4.0 y los docs generados; 1163 funciones de test; el trailer `Fuente:` (los 9 ids existen); que los ids citados dicen lo que se les atribuye (leídos los yaml, con la salvedad de a5) y la cadena v4 → sesión 1 en RN-034, ADR-0066 §2 y el informe §6.1; holdout y regímenes de cambio intactos, y la fila nueva de `HOLDOUT-EXPOSICIONES.md`; el `## Estado` de ADR-0066; ningún sitio nuevo con `cita`; ninguna cifra en la forma ejecutable; que el test de la orden viva mide lo que dicen el informe y el parámetro («se podía llenar» no lo prueba, porque el precio no baja a ella: menor, no contado aparte); que §6.4 separa lo medido de lo deducido del código.
>
> ### Eje (b) · Encargo (Segunda y Tercera orden)
> Resumen: 0 bloquea, 1 importa, 0 menor. Requisitos: 10 hechos, 1 parcial, 0 no hechos.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | El requisito 10 está parcial: «el caso peor» queda como medida de días reales y cota por lectura del código. El informe lo dice, pero sin una medición de un caso peor (cinco escenarios con cada toma reubicando) no se puede afirmar con evidencia que el número de escenarios no mueve el tope de 2.000. Lo sostiene el razonamiento del código, no una medida. | Informe §6.4 («Lo que dice el código, sin medir un día peor», «El código no garantiza el tope por sí solo»). |
>
> ### Lo que no pude comprobar
> `make check`, `knowledge validate` y el sello (escriben); las cifras de peticiones por día (10, 6, 10, 13), que exigían correr `dia_del_bot.py` sobre días dev; «481 instantes por día», que no encontró escrito en `engine/`; que `se_mueve` coincide con `7ab42d6` ejecutando el test allí (exige `git worktree add`); la suite completa.

**Respuesta de la sesión, hallazgo a hallazgo:**
- **a1, declarado; lo decide el consultor.** Es verdad: A-46 y A-38 están RESUELTAS, y los dos
  parámetros nuevos son DEFAULT_AMBIGUOUS. `orden_pendiente_al_abrir_escenario` cuelga de A-25,
  que está abierta (pregunta 18), y su fuente es el registro de A-38 porque es lo único que dijo el
  trader de la vida de la orden. `max_escenarios_por_sesion` cuelga de A-46, RESUELTA, sin que
  ninguna ambigüedad abierta recoja la subpregunta del número. Hay dos salidas: abrir una
  ambigüedad nueva para el tope (toca `ambiguedades.yaml`, la tabla de `PROJECT_STATE.md` y los
  docs generados, `docs/runbooks/AMBIGUEDADES.md`) o colgar el parámetro de A-25. No se hace aquí
  sin la decisión, porque la orden pedía parámetro y pregunta, no una ambigüedad. Que A-46 diga
  «sin tope diario de escenarios» con una cita que no habla de tope venía de antes, y queda anotado
  aquí.
- **a2, arreglado**: el pie de `PREGUNTAS.md` dice 21 por preguntar, de dónde salen la 20 y la 21,
  y qué parámetros PROVISIONAL dependen de ellas.
- **a3, arreglado**: el tramo de una orden acaba al llenarse o cancelarse; si sigue pendiente, al
  final del día, y una modificación ya no lo corta. Vuelto a correr sobre los tres días: las mismas
  cifras (10, 10 y 13 peticiones, una orden pendiente como mucho).
- **a4, arreglado**: RN-034 y ADR-0066 ya no cuentan que antes era lectura nuestra; solo citan. La
  spec pasa a 15.4.1.
- **a5, arreglado**: la cita de la sesión 3 va como pregunta y respuesta, con su confianza media,
  en RN-034, en ADR-0066 y en §6.1.
- **b1, arreglado con una medida**: `test_cinco_escenarios_en_una_sesion_cuestan_dos_peticiones_cada_uno`
  (§6.4): cinco escenarios con la orden viva en cada toma cuestan 10 peticiones en el día, con las
  dos opciones. Lo que el código no garantiza -un tope de peticiones por reubicaciones dentro de un
  escenario- sigue anotado en §6.4, y no es de esta rama.
- **Lo que no pudo comprobar**: `make check` sella este commit (abajo); los «481» están ahora
  nombrados con su bucle en §6.4.

## Estado

**Rama lista para revisión, NO cerrada.** Tarea autónoma: no se cierra. Fases 0, 1 y 2 hechas y
selladas, con el revisor pasado y sus hallazgos atendidos o declarados. Las órdenes 2 y 3 del
consultor (2026-10-02), hechas en §6, con su revisor (§6.6). Lo que espera a la sesión 4 y lo que
decide el consultor está en §4 y en la respuesta a a1 de §6.6.
