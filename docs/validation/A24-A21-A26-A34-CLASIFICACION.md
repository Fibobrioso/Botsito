# A-24, A-21, A-26 y A-34 en las transcripciones: la clasificación de los 44 pasajes

Rama `trabajo/a24-a21-a26-a34`, 2026-09-24. Sin merge, sin tag y sin push.

- **Qué se clasifica:** los pasajes de la salida congelada (`A24-A21-A26-A34-SALIDA.txt`), los 44
  y ninguno fuera.
- **Con qué norma:** la de `A24-A21-A26-A34-CRITERIO.md` §1 y §2.
- **Clases posibles:**
  - **responde → hipótesis X**, si el pasaje enuncia la regla de forma general, o si es
    incompatible con todas las hipótesis menos una;
  - **no responde**, en otro caso, y también ante la duda, con la duda anotada.
- **De dónde sale cada frase:** está copiada de la salida, que es la cruda. Una frase que ocupa
  varios segmentos se da con sus números y con los segmentos separados por « / ».
- **Qué no se hace aquí:** no se aplica la regla global. La aplica el consultor.

**Las hipótesis, en corto** (`A24-A21-A26-A34-CRITERIO.md` §1):
- **A-24:** (a) el pivote más reciente; (b) el más extremo; (c) otro, o discrecional.
- **A-26:** (a) se marca igual la liquidez con la vela contraria al flujo de M15, y el lado de
  ruido se lee de ese flujo; (b) solo cuentan las velas contrarias al flujo que va en el sentido
  del sesgo.
- **A-21 y A-34:** abiertas; un pasaje responde si enuncia una regla general.

## A-24 · qué hace que marques un pivote de M15 y no otro (18 pasajes)

| pasaje | tr | intervalo | clase | frase literal | por qué |
|---|---|---|---|---|---|
| 1 | v1 | 0:02:13-0:03:49 | no responde · **DUDA** | #33 «zona de liquidez en m15 entonces lo que yo voy a usar va a ser la zona de liquidez más reciente» | Apunta a (a), pero lo dice de ESTE caso («voy a usar»), cuando se forma una zona nueva; no lo enuncia como regla |
| 2 | v1 | 0:04:56-0:06:30 | no responde | #67 «debajo por el hecho de que esta mecha yo considero también como parte de la estructura de mercado» | Habla de que la mecha cuenta como estructura; no dice qué pivote elige |
| 3 | v1 | 0:12:49-0:14:25 | **responde → (a)** | #180 «la zona de liquidez tiene que ser la más reciente es una línea de liquidez que está aquí no aquí» | Enuncia la regla en general («tiene que ser la más reciente»). Es el control positivo |
| 4 | v3 | 0:09:03-0:10:45 | no responde | #99 «sea entrada aquí en el punto más alto entrada bueno entrada por por aquí aquí hay otra entrada» | Una entrada concreta |
| 5 | v3 | 0:11:19-0:14:19 | no responde · **DUDA** | #142-#145 «como es un retroceso complejo, estaríamos marcando lo que sería / en este complex pullback alcista, / que yo no suelo usar el término higher, bueno, higher hike, / hay pero el alto más alto aquí alto más alto sería la liquidez esto es en m15 temporalidad de m15 ya» | Apunta a (b), pero está dicho sobre un croquis y en contexto de retroceso complejo. Este fotograma no se ha abierto. La nota de A-24 en `ambiguedades.yaml` dice que, las dos veces que se midió, el pivote elegido era el mismo con las dos lecturas |
| 6 | v3 | 0:14:19-0:16:19 | no responde · **DUDA** | #162-#168 «tus zonas de liquidez, que sería / este alto, aunque yo invadiría / este alto, la verdad, o sea, suelo usar / la zona, en este caso / la zona / de liquidez más baja, que me deja el precio / que sería este de aquí» | La frase aparta el alto más alto y dice que «suele usar» la más baja que le deja el precio: **en contra de (b)**. No separa (a) de (c), y está dicho sobre un ejemplo. Es el instante del fotograma `fr-v3-982da728/944000` que cita la nota de A-24, y esa nota dice que el pivote elegido era el mismo con las dos lecturas. Si lo es, el ejemplo no discrimina |
| 7 | v3 | 0:25:30-0:27:10 | no responde | #290 «nosotros lo hemos tomado desde el punto más alto» | Desde dónde tomó una entrada concreta |
| 8 | v3 | 0:32:33-0:34:22 | no responde | #391 «Es a través de eso, o sea, buscar, plantear, aquí tengo liquidez en M15 y este sería, pues, el punto más alto.» | Es el objetivo (maximizar el TP), no la liquidez de entrada |
| 9 | v3 | 0:38:39-0:40:48 | no responde · **DUDA** | #480-#481 «que onda. Ahora, sí, y ya normalmente si quieres hacerlo, pues es eso. Coge SM15 y marcas tu zona / de liquidez que tú consideres y ya. Esperar a que el precio llegue. ¿Y qué más? Bueno, ¿cuál era la» | Parecería apuntar a (c), pero **el contexto es maximizar el TP** («lo más objetivo es ponerlo a 13», #479), no marcar la liquidez de entrada. Es la frase del ítem `ev-v3-003916-447dc8d7`, que sostiene el riesgo de fidelidad de A-24 |
| 10 | v3 | 0:43:08-0:44:51 | no responde | #558 «claro yo mi lotaje el lotaje se calcula desde el inicio desde el punto más alto hasta el punto más» | Lotaje (A-18) |
| 11 | v3 | 1:04:17-1:05:55 | no responde | #849 «o sea, si parto desde aquí, sería, este es el punto más bajo,» | Mapeo en M1 de un ejemplo |
| 12 | v3 | 1:07:24-1:09:03 | no responde | #873 «sería como tal entonces si yo yo considero esto aquí porque a veces si consideraría si lo haría» | Order blocks en M5 y M1 |
| 13 | v4 | 0:21:03-0:22:38 | no responde | #372 «eso pues lo protege es o sea por el punto más bajo en este caso como estamos de bajista alcista» | Dónde se protege en el segundo esquema |
| 14 | v4 | 0:49:15-0:51:03 | no responde · **DUDA** | #836 «A ver, siguiente es, cuando marcas la zona de liquidez en M15, ¿tomas el último pico que ya se formó del todo o simplemente el punto más alto de las últimas velas aunque sigan en curso?»; #846 «Uno ya formado» | Contesta OTRA dimensión: el pivote tiene que estar **ya formado**, no en curso. No separa reciente de extremo. Se anota porque es un dato para la regla que falte |
| 15 | v4 | 0:55:59-0:57:36 | no responde · **DUDA** | #930-#932 «que hago es que en m15 pues mi punto más alto en este caso no sé cuál es la tendencia la verdad y / Y me es indiferente, o sea, según el momento y la sesión, o sea, yo marco desde el punto anterior, en este caso desde aquí, si lo cojo, marco desde aquí a aquí y hasta aquí. / O sea, todo lo que hay es liquidez, o sea, yo lo considero liquidez y me es indiferente, o sea, la zona de control se desarrolla tal cual así.» | «Marco desde el punto anterior» y «según el momento y la sesión» podrían ser (a) o (c); con deícticos, no se puede fijar |
| 16 | v4 | 1:08:36-1:10:17 | no responde · **DUDA** | #1174-#1182 «Respecto a estructura / Siempre se respeta la estructura más reciente / Por ejemplo, imagina que hay / Un alto / O un máximo como zona de liquidez / De hace 2 o 3 días / Ese ahí no se toma en cuenta / Lo importante es los más próximos / Exacto» | Enuncia una regla general a favor de (a). **La duda es quién habla:** la cruda no separa hablantes, y por la forma lo enuncia el interlocutor y el trader lo confirma con «Exacto». Si se acepta la confirmación, responde → (a) |
| 17 | v4 | 1:24:26-1:26:08 | no responde | #1487 «O sea, yo puedo pagar, o sea, la prueba en la que es más factible, o sea, la que tú consideres viable, si es FTMO u otra, pues lo pago, no pasa nada.» | La cuenta de fondeo |
| 18 | v4 | 1:30:37-1:32:13 | no responde | #1593 «yo considero muy clave el break even cuando se desarrolle otra zona de» | Break even |

## A-21 · qué es una zona de control limpia (14 pasajes)

| pasaje | tr | intervalo | clase | frase literal | por qué |
|---|---|---|---|---|---|
| 1 | v1 | 0:13:28-0:16:28 | no responde | #189 «Y cuando se desarrolle esta zona de control que no haga mucho ruido, o sea, sea una zona limpia, por así decirlo, sin mucho ruido.» | Es el control positivo: nombra «limpia» sin definirla |
| 2 | v2 | 0:12:30-0:14:08 | no responde | #117 «sea el precio toma una dirección como un retroceso complejo entonces pero si te das cuenta en m 15» | Describe el flujo de un ejemplo |
| 3 | v2 | 0:34:10-0:35:42 | no responde | #320-#321 «ese flujo de órdenes natural / digámoslo también así, no muy ruidoso» | Un flujo «no muy ruidoso», cualitativo |
| 4 | v3 | 0:06:25-0:08:01 | no responde | #65 «volatilidad y un poco más ruidoso está el mercado entonces qué hacemos en este caso pues yo lo que» | El mercado en M15, no la zona de control |
| 5 | v3 | 0:11:57-0:13:34 | no responde | #142 «como es un retroceso complejo, estaríamos marcando lo que sería» | Marcar liquidez (es de A-24) |
| 6 | v3 | 0:41:18-0:42:49 | no responde | #514-#516 «es esto aquí. Yo no espero / ningún retroceso, si se han dado cuenta. / Con el breaker ya me basta,» | Define el primer esquema (sin retroceso), no qué es «limpia» |
| 7 | v3 | 0:48:57-0:50:33 | no responde · **DUDA** | #624-#627 «una dos tres desarrolló un retroceso complejo más desarrollados hay / demasiadas zonas de control y invalida porque la única manera de poder tomar / la entrada es que el precio llegue al menos me genere uno de estos y luego me / rompa o inmediatamente pues rompa si hacen más de esto o sea más de esta zona» | Es una regla general, pero de otra cosa: **más de una zona de control invalida** la entrada, que es lo que ya dice RN-009 (`zonas_control_max_por_esquema`). No define «limpia». Si A-21 fuera en realidad esto, estaría contestada por RN-009 |
| 8 | v3 | 0:58:49-1:00:52 | no responde | #756 «Cuando el precio desarrolla de esta manera, te genera este esquema aquí suponiendo y luego el precio si llega a hacer un retroceso con complex pullback y todavía no te desarrolla la zona de control, entonces lo más probable es que de 0.75 se pase a 0.50 para proteger mucho más porque existe una alta probabilidad, pero muy alta probabilidad.» | Gestión del stop |
| 9 | v3 | 1:02:57-1:05:19 | no responde | #830-#831 «¿cuántas velas a cada lado / valían un máximo o mínimo estructural? ¿a qué te» | Una pregunta sobre pivotes; su respuesta es mapear con las mechas, no la zona limpia |
| 10 | v3 | 1:14:26-1:16:25 | no responde | #976 «O bueno, podría responder a esto, si hay un flujo alcista, una vela contraria, pues marca un mínimo si es roja y eso, y al revés, si el flujo es bajista, una vela verde, pues una vela alcista marca un retroceso y eso.» | Cómo se marca un máximo o un mínimo, no la zona limpia |
| 11 | v4 | 0:35:44-0:37:25 | no responde | #617-#618 «porque se desarrolla o sea no se desarrolla el esquema como tal si no te suelta otra zona de / control entonces no hay entrada ok me nace una duda aquí justamente creo que es parte de las» | Un caso concreto, en la línea de RN-009 |
| 12 | v4 | 0:44:05-0:45:38 | no responde | #768 «Lo respetas allí y te genera la otra zona de control» | Break even |
| 13 | v4 | 1:03:40-1:06:00 | no responde · **DUDA** | #1077-#1078 «Está allí, el número de velas / Creo que es indiferente el número de velas»; #1089 «El número de velas que hay al costado» | Una regla general en negativo: **el número de velas es indiferente**. Pero el contexto es una orden límite que se activa y se devuelve y las velas «al costado», no la zona de control. Descarta el recuento de velas como criterio, sin decir cuál es |
| 14 | v4 | 1:30:37-1:32:39 | no responde | #1593-#1594 «yo considero muy clave el break even cuando se desarrolle otra zona de / control o sea ya se habría dentro 2 entonces pero ya cuando se desarrolle» | Break even y un tercer esquema |

## A-26 · el flujo de M15 cuando va contra el sesgo de H4 (9 pasajes)

| pasaje | tr | intervalo | clase | frase literal | por qué |
|---|---|---|---|---|---|
| 1 | v1 | 0:14:09-0:15:42 | no responde | #192 «Desde el punto más abajo te genera la vela contraria» | Dónde va el stop |
| 2 | v3 | 0:08:25-0:09:59 | no responde · **DUDA** | #91-#95 «m 15 hay entradas o sea está esto que sería una entrada si nosotros marcamos liquidez esto que / que sería otra entrada, o sea, estaríamos operando contra tendencia, / pero ese es el, aquí otra entrada, y o sea, aquí tenemos desarrollo del precio. / O sea, tenemos desarrollo del precio aquí, desarrollo del precio aquí, / desarrollo del precio aquí, a pesar de que el flujo sea alcista.» | Opera en el sentido del sesgo aunque las velas vayan al revés, pero no dice con qué vela marca la liquidez. No separa (a) de (b) |
| 3 | v3 | 0:14:26-0:16:04 | no responde · **DUDA** | #157-#159 «Nosotros sabemos que, número uno, se cumplen los criterios. / Vela bajista envuelve a la vela anterior, por lo tanto, valida que este tipo de órdenes de H4, / existe una alta probabilidad de que continúen, ¿vale?» | Es el control positivo. Es del sesgo H4, no de A-26. **Cruza con A-34**: una vela que envuelve a la anterior valida la continuidad en su sentido. Pero «envuelve» no dice que la mecha rompa los dos extremos |
| 4 | v3 | 1:07:40-1:09:17 | no responde | #875 «ver la contra si hay un flujo bajista hay una vela contraria marcarlo acá y eso es ahora» | Order blocks en M5 y M1 |
| 5 | v3 | 1:14:55-1:17:18 | no responde · **DUDA** | #976 «O bueno, podría responder a esto, si hay un flujo alcista, una vela contraria, pues marca un mínimo si es roja y eso, y al revés, si el flujo es bajista, una vela verde, pues una vela alcista marca un retroceso y eso.» | La regla de marcar es simétrica para cualquier flujo y no nombra el sesgo: **apunta a (a)**. Pero contesta a qué es un máximo o un mínimo estructural, no a qué pasa cuando M15 va contra H4 |
| 6 | v4 | 0:27:16-0:28:52 | no responde | #461 «está bajista trata entonces ya sabes que aquí la vela contraria pues ya te está diciendo que» | Un ejemplo, con el flujo a favor del sesgo |
| 7 | v4 | 0:34:22-0:36:01 | no responde | #597-#599 «cual y ya apenas una manera de identificarlos es la vela contraria o sea estas son un flujo / bajista, se desarrolla una vela / alcista, entonces ya» | Un ejemplo con sesgo alcista y flujo de M15 bajista, en el que marca con la vela alcista contraria. **Apunta a (a)**, pero es una operación concreta |
| 8 | v4 | 0:56:32-0:59:14 | no responde · **DUDA** | #930-#931 «que hago es que en m15 pues mi punto más alto en este caso no sé cuál es la tendencia la verdad y / Y me es indiferente, o sea, según el momento y la sesión, o sea, yo marco desde el punto anterior, en este caso desde aquí, si lo cojo, marco desde aquí a aquí y hasta aquí.»; #942 «Entonces, la vela contraria para mí, apenas se inicia una vela contraria en un flujo de órdenes, yo ya lo tomo como un punto en el cual yo ya voy marcando, por ejemplo, en ese caso, si sé que la vela MX se me ha desarrollado, yo ya, o sea, no tenemos nada aquí, sé que aquí, entonces yo ya marco y sé que esperaría un breaker en M1 para seguir operando.» | Es lo más cerca de una regla: **marca con la vela contraria de cualquier flujo, y la tendencia le es indiferente al marcar**. Apunta a (a). Pero «la tendencia» no dice de qué marco, ni habla del lado de ruido |
| 9 | v4 | 1:01:14-1:02:50 | no responde | #1032-#1033 «esquemas, pero es eso, o sea, es correlacionar las temporales, o sea, nosotros buscamos un flujo / que se rompa el flujo en M15, pero tratamos de tomarlo, o sea, desde casi que desde que se» | Correlacionar temporalidades, en general |

## A-34 · vela H4 previa que rompe ambos extremos (3 pasajes)

| pasaje | tr | intervalo | clase | frase literal | por qué |
|---|---|---|---|---|---|
| 1 | v3 | 0:04:54-0:06:30 | no responde | #56 «lo fija la vela de 4 previa cerrada en el menos uno es verdad o sea alcistas sólo compras bajistas» | Es el control positivo: la regla general del sesgo, sin el caso de los dos extremos |
| 2 | v3 | 1:08:53-1:10:26 | no responde | #894-#895 «¿Qué hace la vela previa alcista o bajista exactamente? / ¿Y si es un doji indecisa?»; #901 «cualquiera de estas velas o las siguientes no sabemos si me va a cubrir aquí o sea tendría que terminar por debajo al menos su mecha por debajo para poder considerar nosotros pues ese cambio de escenario si no operaríamos alcistas independientemente si aquí es rojo rojo rojo verde rojo rojo rojo» | Le preguntan por el doji y contesta «ya lo hemos respondido», con la ruptura de un solo lado |
| 3 | v3 | 1:15:15-1:16:48 | no responde · **DUDA** | #982-#992 «pero si quieren hacerlo / más factible, o sea / también podría, se podría / intentar, o sea, no considerar / que a veces se envuelva y indirecto / o sea, simplemente / si la vela anterior es bajista / que la otra sea, exista una probabilidad que sea bajista / y así, o sea, plantearlo de esa manera / y ya, no / No tratar de buscar, claro, a ver si envuelve y todo eso para no liarse.» | Ofrece una SIMPLIFICACIÓN opcional («si quieren hacerlo más factible»): no mirar si envuelve y tomar el sentido de la vela anterior. **Choca con RN-003**, cuyas notas dicen que el color no decide. No es su regla, así que no responde. Se anota porque toca A-1 y A-34 |

## Recuento

| ambigüedad | pasajes | responde | no responde (con duda) |
|---|---|---|---|
| A-24 | 18 | **1 → (a)** | 17 (7) |
| A-21 | 14 | 0 | 14 (2) |
| A-26 | 9 | 0 | 9 (3) |
| A-34 | 3 | 0 | 3 (1) |

## Las dudas, para el consultor

- **A-24.**
  - Lo que responde, y las dudas 1 y 16, van en el mismo sentido: **(a), el más reciente**.
  - En la frase del pasaje 6, el trader aparta el alto más alto, **en contra de (b)**. Pero, según la nota de A-24, ese mismo instante, medido en el fotograma, no separa (a) de (b).
  - El 5 apunta a (b), en un croquis de retroceso complejo cuyo fotograma no se ha abierto.
  - **El 9, que sostenía la hipótesis discrecional, es de maximizar el TP y no de la liquidez de
    entrada.**
  - El 14 añade que el pivote tiene que estar ya formado.
  - Ningún pasaje responde en contra de (a).
- **A-21.** Nada define «limpia».
  - Lo más cercano es una regla que ya está en RN-009: más de una zona de control invalida
    (pasaje 7).
  - Hay también una negativa: el número de velas es indiferente (pasaje 13).
  - **Pregunta de fondo:** ¿A-21 pide algo distinto de RN-009?
- **A-26.** Tres pasajes (5, 7 y 8) **apuntan a (a)**: se marca con la vela contraria de cualquier
  flujo, y la tendencia le es indiferente al marcar. Ninguno lo dice como regla para el caso en que
  M15 va contra H4, ni habla del lado de ruido.
- **A-34.**
  - Nada responde.
  - Un pasaje de A-26 (el 3) dice que una vela que **envuelve** a la anterior valida la continuidad
    en su sentido.
  - El pasaje 3 de A-34 ofrece, como simplificación opcional, tomar el color de la vela anterior,
    lo que choca con RN-003.
  - «Envuelve» no dice que la mecha rompa los dos extremos.

## Estado

CLASIFICADO. La regla global no se ha aplicado: la aplica el consultor.
