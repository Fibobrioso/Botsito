# Sesión 02: la clasificación de los 47 pasajes de los candidatos C-xx

Rama `trabajo/sesion-02`, 2026-09-25. Sin merge, sin tag y sin push.

**Qué se clasifica:** los pasajes de la salida congelada (`SESION-02-BUSQUEDA-SALIDA.txt`), los 47
y ninguno fuera. La norma es la de `SESION-02-BUSQUEDA-CRITERIO.md` §2, candidato por candidato:
**RESPONDE** enuncia la regla en general; **DUDA** la muestra en un ejemplo o con deícticos, o
responde a medias como allí se define, y para la regla global no responde; **NO RESPONDE** habla de
otra cosa.

**De dónde sale cada frase:** está copiada de la salida, que es la cruda. Una frase que ocupa varios
segmentos se da con sus números y los segmentos separados por « / ». Todas se han comprobado por
script contra su pasaje (§ «Cómo se comprobó»).

**Fotogramas:** solo donde la respuesta depende del gráfico. Es el más cercano según
`botsito corpus frames show`, y se indica si ya estaba citado en el repositorio. **No se ha abierto
ninguno** (ADR-0038).

**Qué no se hace aquí:** no se aplica la regla global. La aplica el consultor.

## C-01 · El precio de la orden límite dentro de la zona

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v1 | 0:04:35-0:06:26 | **DUDA** | #66-#67 «bajista que se sigue generando mi orden límite estaría por aquí por debajo porque por allí por / debajo por el hecho de que esta mecha yo considero también como parte de la estructura de mercado» | Pone la orden «por debajo» porque una mecha cuenta como estructura, pero sobre el ejemplo y con deícticos | `fr-v1-5a2a42c3/335000` (0:05:35), no citado |
| 2 | v1 | 0:23:10-0:24:49 | NO RESPONDE | #313 «que ir con el orden límite o sea muy límite vale aquí hay una entrada como tal o sea aquí estaría» | Repasa una entrada; no dice en qué punto va la orden | — |
| 3 | v3 | 0:18:47-0:20:32 | **DUDA** | #229-#230 «que puedas tomarlo bueno en este caso aquí estaría la orden / limit y bueno ahí no lo ha roto ahí ya se» | La sitúa con deícticos. Lo general del tramo (#225-#228) es que la orden se va moviendo con el flujo, que es A-5 y A-29, no el precio | `fr-v3-982da728/1172000` (0:19:32), no citado |
| 4 | v3 | 0:24:26-0:26:03 | **DUDA** | #272-#273 «yo lo suelo marcar aquí porque si nosotros hacemos un mapa estructural rápido, o sea, así al ojo, / Vemos que este fue el último movimiento que generó el breaker, o sea, el rompimiento.»; #281 «entonces aquí estaría esperaría que me genera un voz aquí está mi orden link estaría ya predefinido» | Da un motivo con forma general, el último movimiento que generó el breaker, pero lo aplica al ejemplo y no dice el precio dentro de ese movimiento | `fr-v3-982da728/1474000` (0:24:34), no citado |
| 5 | v3 | 0:40:29-0:43:15 | **DUDA** | #503-#504 «entrada por orden límite / en el origen del quiebre, bloque» | Lee el enunciado del cuestionario: dice la zona, el bloque de origen del quiebre, y no el precio dentro de ella. Es el ancla que ya citaba la auditoría del 2026-09-13. El «marco mi orden limit» de #527-#528 es cuándo (A-29) | — |
| 6 | v3 | 0:51:02-0:52:40 | NO RESPONDE | #647 «esta sería mi orden límite que no llega a romperlo entonces no hay entrada aquí no hay entrada» | Si hay entrada o no | — |
| 7 | v3 | 1:06:50-1:08:26 | NO RESPONDE | #868 «de ICT, esto sería un order block. Esto de aquí sería tu order block. Esto sería tu bloque de» | El mapeo de order blocks en M5 y M1 (RN-007), no la orden | — |
| 8 | v3 | 1:11:38-1:13:13 | NO RESPONDE | #921 «¿Cómo se marca el bloque de origen por el orden? Como ya tenemos nosotros definido, el shot era el giro, claro,» | Cómo se define el bloque (BOS o breaker), no dónde va la orden dentro de él | — |
| 9 | v3 | 1:16:08-1:17:49 | NO RESPONDE | #999 «Boss breaker que define cómo se marca el bloque de origen es eso. No uso lo que sería el shot como» | Lo mismo que P8 | — |
| 10 | v4 | 0:07:28-0:09:00 | NO RESPONDE | #102-#103 «tiene es esto, si el punto de entrada, por ejemplo / ahí que tienes es en el nivel 1.19502» | El stop a 0,75 y su respiro de pips; la entrada es un dato del ejemplo | — |
| 11 | v4 | 0:40:26-0:42:35 | NO RESPONDE | #717 «Si el precio hubiera hecho esto, o sea, subía, aquí estaríamos con orden limit, se activa la orden limit, o sea, el buy limit, y entraríamos» | La toma de liquidez en M1, con mecha o con cuerpo, y la reentrada | — |
| 12 | v4 | 1:02:48-1:04:25 | NO RESPONDE | #1065 «activar tu entrada o sea bueno tu orden límite entonces se llega a activar entonces aquí pueden» | La entrada que se activa sin ruptura (RN-010, A-31) | — |
| 13 | v4 | 1:05:09-1:08:09 | **RESPONDE → en la mecha** | #1110-#1115 «¿qué vela y dónde va el límite? / la pregunta va así, la zona donde pones / la orden límite, ¿es sólo el rango / de esa vela o también toma en cuenta / las del lado? o sea, ¿la orden va en el borde de arriba / en el medio o el borde de abajo?»; #1116-#1118 «ah, vale, la orden límite / bueno, como hemos estado viendo / o sea, suele ir en la mecha»; #1122 «aquí vale por ejemplo aquí en la mecha sería mecha tal cual sabes siempre la mecha tomamos la mecha»; #1123 «Siempre se toma en la mecha el límite» | Le preguntan justo esto, borde de arriba, medio o borde de abajo, y contesta en general: siempre en la mecha. **No dice** qué punto de la mecha ni de qué vela; eso lo enseña con deícticos (#1120-#1122). Ítem `ev-v4-010605-a11249c0` (`entrada.orden_limite.en_la_mecha`), que **no cita ninguna regla ni ambigüedad**. Lo que sigue (#1127-#1146) es la vida de la orden pendiente: ver C-04 | `fr-v4-9ad0ebb8/3972000` (1:06:12), no citado |
| 14 | v4 | 1:30:21-1:32:54 | NO RESPONDE | #1590 «que sería se pondría el orden límite en este caso bajista y cuando se active» | El tercer esquema de entrada, que la v1 deja fuera | — |

**Recuento C-01:** 14 pasajes · RESPONDE 1 (P13) · DUDA 4 (P1, P3, P4, P5) · NO RESPONDE 9.

## C-02 · El extremo de la caja, del que sale el stop

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v1 | 0:04:05-0:05:39 | **DUDA** | #49-#53 «me olvidé mencionar también que tenemos que / trazar el cuadro de GAN / para poder, desde aquí / hasta aquí, para poder cubrir / hasta un 0.75, entonces» | La caja se traza «desde aquí hasta aquí»: deícticos | `fr-v1-5a2a42c3/292000` (0:04:52), no citado |
| 2 | v1 | 0:14:09-0:15:50 | **RESPONDE → el punto más bajo donde se genera la vela contraria** | #192-#194 «Desde el punto más abajo te genera la vela contraria / Se puede definir, pues, el stop loss y demás / Entonces, aquí sería mi stop loss, ¿vale?» | Dice qué punto en general: el más bajo, donde se genera la vela contraria. **No dice** de qué temporalidad ni qué vela contraria, la de la liquidez de M15 o una de M1, y lo aplica enseguida con un deíctico («aquí», #194). Es el control positivo. Ítem `ev-v1-001454-69cebe62` (`stop.origen_vela_contraria`), que **no cita ninguna regla**. Para A-35 este mismo pasaje era NO RESPONDE, porque allí se preguntaba otra cosa | `fr-v1-5a2a42c3/894000` (0:14:54), no citado |
| 3 | v1 | 0:15:58-0:17:36 | NO RESPONDE | #219-#220 «o sea se cambia y está pero yo según suelo reducir o sea mi stop loss digamos máximo que yo puedo / fijar o sea de pasar de 0.75 es a 0.50 entonces si yo estuviera gestionando el trade que es lo» | La fracción de la caja (A-10), no su extremo | — |
| 4 | v1 | 0:20:19-0:21:54 | NO RESPONDE | #270-#271 «o sea, teniendo desde aquí hasta aquí, ¿vale? No llegó al 1.3. / Claro, si entrábamos, digamos así, en 0.75, configurando el lotaje a esta zona de aquí,» | El lote y el objetivo (A-18) | — |
| 5 | v3 | 0:09:03-0:10:45 | NO RESPONDE | #99 «sea entrada aquí en el punto más alto entrada bueno entrada por por aquí aquí hay otra entrada» | Dónde entra en M1 en un ejemplo del sesgo, no la caja | — |
| 6 | v3 | 0:25:30-0:27:02 | NO RESPONDE | #290 «nosotros lo hemos tomado desde el punto más alto» | Por qué opera en M1 y no en M5 | — |
| 7 | v3 | 0:32:33-0:34:22 | NO RESPONDE | #391 «Es a través de eso, o sea, buscar, plantear, aquí tengo liquidez en M15 y este sería, pues, el punto más alto.» | El objetivo y cómo maximizarlo (A-18, RN-015). Ver el hallazgo lateral L-2 | — |
| 8 | v3 | 0:43:00-0:45:08 | **DUDA** | #557-#559 «yo protegería aquí o sea definiría aquí vale o sea definiría aquí lo que sería mi stop loss pero / claro yo mi lotaje el lotaje se calcula desde el inicio desde el punto más alto hasta el punto más / bajo ahora esto es algo que también le quería preguntar a lo mejor con la se podría ver con» | La caja del lote va «desde el punto más alto hasta el punto más bajo», pero no dice de qué, y lo señala en el gráfico. El stop «aquí» de #557 es el del segundo esquema (A-7). Ítems `ev-v3-004353-b7661782` (sin citar en la spec) y `ev-v3-004329-a16d379b` | `fr-v3-982da728/2633000` (0:43:53), no citado |
| 9 | v3 | 0:53:26-0:55:01 | NO RESPONDE | #687-#688 «es esto. Marcar, por ejemplo, si tengo esta zona de liquidez de aquí a aquí y veo que / el precio me va a este, puedo maximizarlo hasta 0.50. Suelo usar el 0.50 que lo suelo» | La fracción (0,50) | — |
| 10 | v3 | 1:03:04-1:05:55 | **DUDA** | #824-#826 «caja de GAN / nivel 0 con un bral de invalidación y optimización / del stock, sí» | Lee el cuestionario y confirma que el nivel 0 de la caja es el umbral de invalidación y de optimización del stop: dice **qué papel** tiene el nivel 0, no qué punto del mercado es. El «punto más bajo» de #849-#850 es un mapeo de M1. Ver el hallazgo lateral L-1 (#804-#816) | — |
| 11 | v4 | 0:02:48-0:04:27 | **DUDA** | #36-#37 «entrada aquí tampoco aquí se abrió una entrada y sería donde sólo los como tal ya que sería / nuestro blog por el hecho de que haber gestionando el trade o sea sería de aquí hasta aquí pero mira» | La caja «de aquí hasta aquí», con deícticos, y la cruda degradada («sólo los», «blog») | `fr-v4-9ad0ebb8/217000` (0:03:37), no citado |
| 12 | v4 | 0:06:37-0:08:08 | NO RESPONDE | #79 «Yo suelo proteger en 0.75 como te dije» | La fracción | — |
| 13 | v4 | 0:21:03-0:22:38 | **DUDA** | #371-#373 «entrada un poco más arriba así entonces tú tu stop loss o sea en vez de proteger a 0.75 en lugar de / eso pues lo protege es o sea por el punto más bajo en este caso como estamos de bajista alcista / protege es allí en ese nivel pues en este caso sería proteger a este nivel aquí sabes el segundo» | En el segundo esquema el stop va «por el punto más bajo», con deícticos y sin decir de qué. Es dónde va el stop, no de dónde sale la caja; y `stop_segundo_esquema` quedó en UNKNOWN por REJECT en la sesión 01 (P-08), con RN-013 «hay un unico esquema de stop» | `fr-v4-9ad0ebb8/1313000` (0:21:53), no citado |
| 14 | v4 | 0:28:28-0:30:00 | **DUDA** | #478-#481 «estaba aquí, de aquí a aquí / esta es la última / zona de liquidez o de control / en la cual busco el breaker» | Moviendo el stop en la calculadora, la caja «de aquí a aquí» parece llegar a «la última zona de liquidez o de control en la cual busco el breaker»; con deícticos | `fr-v4-9ad0ebb8/1755000` (0:29:15), no citado |
| 15 | v4 | 0:39:14-0:40:46 | NO RESPONDE | #685 «Cuando hay el breaker de liquidez, o sea, la mitigación de liquidez, sea con cuerpo.» | La toma de liquidez con cuerpo en M15 (RN-004) | — |
| 16 | v4 | 0:49:15-0:51:03 | NO RESPONDE | #836 «A ver, siguiente es, cuando marcas la zona de liquidez en M15, ¿tomas el último pico que ya se formó del todo o simplemente el punto más alto de las últimas velas aunque sigan en curso?» | Cuándo está formado el pivote de M15 (A-35) | — |
| 17 | v4 | 0:55:59-0:58:42 | NO RESPONDE | #930 «que hago es que en m15 pues mi punto más alto en este caso no sé cuál es la tendencia la verdad y» | El mapeo de la liquidez de M15 (A-24, A-35) | — |
| 18 | v4 | 1:30:55-1:32:31 | NO RESPONDE | #1596 «o sea se calcula el rotaje desde aquí hasta aquí y luego espera hasta que se desarrolle la otra» | El tercer esquema de entrada, fuera de la v1 | — |

**Recuento C-02:** 18 pasajes · RESPONDE 1 (P2) · DUDA 6 (P1, P8, P10, P11, P13, P14) · NO RESPONDE 11.

## C-04 · La orden pendiente que el precio deja sin llenar

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v2 | 0:59:08-1:00:40 | NO RESPONDE | #624 «No entro desde hace meses.» | Una conversación sobre inversiones en cripto | — |
| 2 | v4 | 1:08:16-1:09:48 | **RESPONDE → se mueve, no se cancela** | #1169-#1172 «entonces el límite se va actualizando / o sea, el mismo límite se va moviendo / a medida que no se activa / se va desarrollando el precio, sí» | Dice en general qué pasa con una orden que no se llena: se mueve mientras no se activa, según se desarrolla el precio. Contesta a la pregunta que abre el pasaje 13 de C-01 (#1130-#1132, «¿cuánto tiempo se tiene que esperar / Con esta orden para poder / Darla por anulada?»). **Reservas:** es el ítem `ev-v4-010857-5bc906c9`, ya evidencia de A-5 (RESUELTA), el mecanismo de RN-006; **no dice** qué pasa si el precio se aleja sin completar una zona nueva, por ejemplo hasta el objetivo, que es justo el hueco que describe C-04 | — |

**Recuento C-04:** 2 pasajes · RESPONDE 1 (P2) · DUDA 0 · NO RESPONDE 1.

## C-05 · Lo que viene de una sesión cuando empieza la otra con otro sesgo

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v1 | 0:00:00-0:02:07 | NO RESPONDE | #17 «entonces tenemos a las 7, primera sesión y la segunda sesión a las 11, vale, bien definimos nosotros el enfoque,» | El horario de las sesiones y el enfoque del día | — |
| 2 | v1 | 0:09:44-0:11:16 | NO RESPONDE | #130 «o bien nosotros en la primera sesión tenemos el trade y ahí paramos, vale, o sea apenas tenemos el trade ya no operamos la segunda» | Parar tras la ganadora, que la sesión 01 revocó (RN-017); nada de lo pendiente al cambiar de sesión | — |
| 3 | v1 | 0:11:17-0:13:00 | NO RESPONDE | #157 «es el que yo como tal a ver yo pero esta segunda sesión vale esto es algo que quiero destacar yo» | El sesgo al empezar la sesión (RN-003) | — |
| 4 | v4 | 0:49:01-0:50:33 | NO RESPONDE | #830-#831 «o sea, aunque después haya otros trades / con la otra sesión, se den 3 ganadores» | Parar tras la ganadora (RN-017) | — |
| 5 | v4 | 1:14:21-1:15:57 | **DUDA** | #1281-#1283 «A ver, yo lo separo por dos sesiones, si te das cuenta, porque suelo trabajar con H4, / entonces, obviamente, la otra vela de H4 me puede, o sea, tomando como vallas esto, que es lo que ha hecho esto, / el bayas puede cambiar entonces si juntamos las dos claro sería de 7 a 3 pm utc más 2 pero es eso» | Dice que con la otra vela H4 el sesgo puede cambiar, pero no qué pasa con lo pendiente o lo abierto. Lo que sigue (#1287-#1291) es el cierre de las 15:00 (RN-002) | — |

**Recuento C-05:** 5 pasajes · RESPONDE 0 · DUDA 1 (P5) · NO RESPONDE 4. Ver el hallazgo lateral L-1.

## C-06 · El stop después del break even

**Cero pasajes.** Sin control positivo conocido (criterio §5), así que el cero dice que ninguno de
los 15 términos aparece, no que el corpus calle. Ver el hallazgo lateral L-2.

## C-07 · El tope de entradas por día

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v2 | 0:15:30-0:17:17 | **DUDA** | #138-#139 «por ejemplo luego tienes esto aquí donde te genera el otro voz que máximo suele ser dos entradas o / sea después del rompimiento de liquidez en este caso de m15 tienes máximo dos entradas pero bueno» | El máximo es por liquidez de M15, no por día: son los cartuchos (A-2, RESUELTA con `cartuchos_max` 3). Ítem `ev-v2-001615-d96c699f` | — |
| 2 | v3 | 0:26:51-0:29:12 | **DUDA** | #306 «vale tenemos por lo general dos entradas vale porque nuestro ratio riesgo»; #309 «Por lo general, o sea, yo cortaría apenas se desarrolle, o sea, el 1 a 3 en una zona, o sea, de 7 a 11, si ya se ha dado el 1 a 3, ya no operaría de 7 a 3.»; #310 «Eso es mi opinión, ¿vale?»; #313 «O sea, en una sesión te puede generar, qué sé yo, tres entradas de 1 a 3,» | «Por lo general dos entradas», sin decir si es un tope ni de qué (día, sesión o zona), dicho como opinión y seguido de que una sesión puede dar tres. Ítems `ev-v3-002714-742f2589` y `ev-v3-002815-64fbe91b` | — |
| 3 | v4 | 0:29:06-0:30:38 | NO RESPONDE | #497-#498 «¿Quieres que sea sí o sí dos entradas? / ¿O tener permiso por una tres?» | Lo pregunta el interlocutor, y la respuesta (#503) se va a la gestión del capital sin fijar tope | — |
| 4 | v4 | 0:33:05-0:34:45 | **RESPONDE → como máximo dos por día** | #573-#576 «entonces en un día como máximo / dos entradas ¿no? por separado / es un buen punto / sí, dos entradas» | Un tope por día, explícito. **Reservas:** (1) la frase se propone en forma de pregunta y se asiente («es un buen punto / sí, dos entradas»); la cruda no separa hablantes, así que quién dice cada tramo es lectura; (2) su ítem, `ev-v4-003350-acb03ee7`, es evidencia de A-2 («¿2 o 3 intentos por zona?»), RESUELTA con `cartuchos_max` 3: allí se leyó como tope por zona; (3) las notas de RN-020 sostienen que nada acota el día salvo el tope porcentual | — |
| 5 | v4 | 0:36:15-0:37:51 | NO RESPONDE | #634-#640 «ya la respuesta es no / o sea, por el hecho de que / para que tú puedas entrar nuevamente / o bien te ha tocado stop loss / o bien pues has / tenido profit, pero con el profit / ya no operas más» | Las operaciones en paralelo (RN-018) y parar tras la ganadora, revocado en la sesión 01 (RN-017; lo dicen las notas de RN-018). No es un máximo de entradas | — |
| 6 | v4 | 0:39:16-0:41:13 | NO RESPONDE | #688 «no es posible, mejor dicho, que haya dos entradas en el mismo caso, en el mismo trade,» | Entradas en paralelo (RN-018) | — |
| 7 | v4 | 0:48:57-0:50:28 | NO RESPONDE | #827-#829 «yo no lo hago, o sea, yo cierro / la operación, apenas tengo el trade positivo / ya no opero más» | Parar tras la ganadora; es `ev-v4-004936-d7004417`, el ítem que RN-017 corrige | — |
| 8 | v4 | 1:13:11-1:14:43 | NO RESPONDE | #1275-#1276 «yo me suelo detener / en la primera operación ganadora.»; #1277-#1278 «Ok, una operación ganadora y se / acaba el día. Sí, se acaba el día.» | Lo mismo que P7. Ítem `ev-v4-011351-74b8bb39` | — |

**Recuento C-07:** 8 pasajes · RESPONDE 1 (P4) · DUDA 2 (P1, P2) · NO RESPONDE 5.

> **CORRECCIÓN del 2026-09-25 (misma rama, al abrir A-41).** P2 cita `ev-v3-002714-742f2589` sin
> decir que **está supersedido** por `ev-v6-000732-f9c41d5e` (sesión 1: «no estamos pausando cuando
> se dé el trade ganador»). No cambia la clase de P2, que es DUDA por lo que dice su frase, pero su
> ítem no vale como evidencia vigente, y A-41 no lo lleva en `evidencia`. La tabla no se toca.

## Recuento

| candidato | pasajes | RESPONDE | DUDA | NO RESPONDE |
|---|---|---|---|---|
| C-01 | 14 | 1 (P13) | 4 | 9 |
| C-02 | 18 | 1 (P2) | 6 | 11 |
| C-04 | 2 | 1 (P2) | 0 | 1 |
| C-05 | 5 | 0 | 1 | 4 |
| C-06 | 0 | 0 | 0 | 0 |
| C-07 | 8 | 1 (P4) | 2 | 5 |
| **total** | **47** | **4** | **13** | **30** |

## Hallazgos laterales: fuera del criterio, sin clasificar

Al leer la salida entera aparecen tres tramos que tocan un candidato **desde el pasaje de otro**. No
los recogió la búsqueda de su candidato, así que **no entran en su recuento** ni se clasifican: el
criterio está congelado y cambiarlo después de ver la salida es cambiarlo. Se anotan para que el
consultor sepa que existen. Sus frases también están comprobadas por script.

- **L-1 · C-05, la mitad de la posición viva.** En C-02 P10 (v3), #804-#806 «luego, en cierre
  agresivo opcional / el vencimiento exacto de la vela H4 operativa / este es un muy buen punto» y
  #809-#812 «cierra la vela de H4 / operativa, se cierra el trade / porque ya la siguiente / vela es
  otro movimiento». Ítem `ev-v3-010304-4468cc20` («confirma el cierre al vencer la vela H4
  operativa»), que **no cita ninguna regla ni ADR**; la spec solo cierra al fin de la ventana
  (RN-002). Ningún término de C-05 casa aquí porque no dice «sesión».
- **L-2 · C-06, el stop que sigue al precio.** En C-02 P7 (v3), #374-#375 «pero mi tp objetivo es
  aquí o sea 16 ese sería mi tema probable pero yo iría aquí si protegiendo / protegiendo diría poco
  a poco si veo que hay un flujo de velas alcistas o por ejemplo en» y #392-#393 «si tienes un 1 a 3
  pero consideras que puede llegar a más entonces en ese caso pues más / protegiendo en lo que yo
  haría sería proteger o sea y voy subiendo también mi visto los conforme». Que «mi visto los» sea
  «mi stop loss» es lectura nuestra del ASR, no cita. Ítems `ev-v3-003220-8805194d` y `ev-v3-003318-f1a2d27d`, sin
  citar en la spec. Habla de ir **más allá del 1:3**, y RN-015 dice que el objetivo es fijo y no se
  mueve: no es necesariamente lo que pregunta C-06, que es el stop después del break even con el
  objetivo fijo. Ningún término de C-06 casa porque el ASR no escribió «stop».
- **L-3 · C-04, la pregunta explícita.** En C-01 P13 (v4), #1130-#1132 «Y así mismo, ¿cuánto tiempo
  se tiene que esperar / Con esta orden para poder / Darla por anulada?» y #1140-#1142 «se... Ah,
  vale. No, es que la orden / si te das cuenta, o sea, se va actualizando como tal. / La vamos
  actualizando.». Es la misma respuesta que C-04 P2, con su pregunta; ítem `ev-v4-010731-bb8af97c`
  (A-5).

## Notas para el consultor

1. **Los cuatro RESPONDE ya eran ítems de evidencia.** Dos no los cita ninguna regla ni
   ambigüedad: `ev-v4-010605-a11249c0` (C-01, la orden en la mecha) y `ev-v1-001454-69cebe62` (C-02, el
   punto más bajo donde se genera la vela contraria). Los otros dos están citados en ambigüedades
   RESUELTAS: `ev-v4-010857-5bc906c9` en A-5 (C-04) y `ev-v4-003350-acb03ee7` en A-2 (C-07). Así que
   en C-01 y C-02 el hueco no es que el corpus calle: es que la spec no recoge lo que ya está
   registrado. Lo que sigue sin decir, en los dos, es **qué punto exacto** (qué punto de la mecha;
   qué vela contraria y de qué temporalidad).
2. **C-07, un RESPONDE ya leído de otra manera.** P4 dice «en un día como máximo dos entradas», y el
   repositorio lo usó para A-2, que es por zona; RN-020 sostiene que no hay cota diaria salvo el
   tope porcentual. P1 y P2 hablan de dos entradas por liquidez o «por lo general», y P2 añade que
   una sesión puede dar tres. Si el consultor lee el parar tras la ganadora (P5, P7, P8 y C-05 P2 y
   P4) como una cota diaria, son pasajes anteriores a la sesión 01, que la revocó (RN-017).
3. **C-04 responde con el mecanismo que ya existe.** «el mismo límite se va moviendo / a medida que
   no se activa» es RN-006; el caso del precio que se va sin completar zona sigue sin palabra del trader.
4. **C-05 y C-06 quedan sin RESPONDE**, pero con los laterales L-1 y L-2, que la búsqueda no podía
   ver con sus términos. **Un cero en C-06 no es ausencia.**
5. **Los dos fotogramas que deciden un RESPONDE son los «aquí» que `CLAUDE.md` ya da por no
   abiertos:** v4 1:06:12 (C-01 P13) y v1 0:14:54 (C-02 P2). Tampoco se han abierto aquí.

## Cómo se comprobó

Cada frase entre « » de este documento, partida por « / », se buscó por script en el texto de los
segmentos del pasaje que la tabla nombra dentro de `SESION-02-BUSQUEDA-SALIDA.txt` (el de C-02 P10,
C-02 P7 y C-01 P13 para los laterales): 125 trozos, 0 fallos. El script es de una sola vez y no se versiona: lee la tabla, parte cada frase por « / » y exige cada trozo en el texto de su pasaje. Los fotogramas salen de
`botsito corpus frames show --video <v> --t <instante>`, que da rutas y no abre ninguno; «citado»
quiere decir que su id aparece en algún fichero versionado.

## Estado

CLASIFICACIÓN CERRADA. La regla global no se ha aplicado: la aplica el consultor.
