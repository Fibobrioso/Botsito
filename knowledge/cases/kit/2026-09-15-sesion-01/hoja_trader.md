# Sesion 2026-09-15-sesion-01 · hoja del trader

Condicion previa: el trader confirma por escrito que NO ha operado ni backtesteado los meses del paquete (2026-01, 2026-07, 2026-08). Toda respuesta se anota literal (registro F09).

## Preguntas

### P-01 · tercer cartucho (BLOQUEANTE)
Pregunta: ¿2 o 3 intentos por zona? (contradiccion ficha vs V4 0:48:41)
Casos:
- v3 0:01:38: "Ficha, fila con el cursor: Límite estricto de 2 cartuchos | Si" · fotograma fr-v3-982da728/98000
- v3 0:48:17: "límite estricto de dos cartuchos por robar el barrio de liquidez exactamente si ambos pierden escenario y escenario invaliado" · fotograma fr-v3-982da728/2897000
- v4 0:33:50: "entonces en un día como máximo dos entradas ¿no? por separado es un buen punto sí, dos entradas" · fotograma fr-v4-9ad0ebb8/2030000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-02 · BE al tocar o al cierre (BLOQUEANTE)
Pregunta: ¿break-even al tocar el nivel o al cierre de vela? (V4 0:44:56)
Opciones: tocar / cierre (u otra, literal)
Casos:
- v4 0:44:47: "en el segundo esquema De entrada, si se da Lo respetas allí y te genera la otra zona de control Y luego pones en break even Y te termina sacando en break even" · fotograma fr-v4-9ad0ebb8/2687000
- v2 0:31:03: "el break even yo creo que es fundamental o sea que apenas el precio suele generar ese movimiento [...] te genera este bloque de orden alcista entonces ahí o sea apenas genera aquí ya la entrada se pone automáticamente en solos" · fotograma fr-v2-c5a09508/1863000
- v5 0:04:27: "se cumplen las condiciones para poner break even, bueno, en ese caso el precio sigue así por caída ya lo podemos poner en B" · fotograma fr-v5-718ecabb/267000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-03 · anclaje de la vela H4 (hora y huso del grafico) (BLOQUEANTE)
Pregunta: ¿a que hora y en que huso del grafico abre su H4? (se resuelve viendo su grafico: captura de la configuracion; y que ocurre en las semanas en que Europa y EE. UU. no coinciden en el cambio de hora)
Casos:
- v3 0:01:36: "una posible regla que sería venta en operativa de 7 a 15 por españa que está muy bien aquí pues yo lo tengo configurado como utc más 2 que son ahora ya madrid" · fotograma fr-v3-982da728/96000
- v3 0:01:57: "Aquí empieza a las 7, termina a las 11 y luego tenemos, sí, hasta las 3 de la tarde [...] la siguiente vela de H4 se desarrolla a las 7 de la mañana, finaliza a las 11, luego la otra vela se desarrolla a las 11 y finaliza a las 3 [...] diría que es un sí a la ventana operativa" · fotograma fr-v3-982da728/117000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-04 · sesgo H4
Pregunta: ¿que vela H4 fija el sesgo y cuando cambia?
Opciones: vela_anterior_color / vela_anterior_cierre_mecha / otra (u otra, literal)
Casos:
- v2 0:08:36: "tú tomas como referencia la vela anterior [...] Que tome de referencia la vela anterior a cuatro horas [...] si es bajista, pues la siguiente operativa va a tener un enfoque principal, o sea, tendencial bajista" · fotograma fr-v2-c5a09508/516000
- v3 0:05:31: "sería h4 ahora dice lo fija la vela de 4 previa cerrada en el menos uno es verdad o sea alcistas sólo compras bajistas sólo ventas" · fotograma fr-v3-982da728/331000
- v3 0:08:24: "para que yo tome alcista esta vela verde debió de haber pues finalizado al menos con una mecha por encima de esto haberme pues generado como que este breaker aquí y para poder validar la siguiente operativa como alcista" · fotograma fr-v3-982da728/504000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-05 · salida sin ruptura
Pregunta: ¿se cierra si no rompe? ¿cuando?
Opciones: cerrar_al_cierre / proteger_y_dejar (u otra, literal)
Casos:
- v4 1:07:59: "aquí hay un igual aquí se activaría la entrada [...] lo ideal sería proteger a 0.75 pero bueno te come aquí [...] cerrar apenas la operación lo más rápido posible se cierra la vela y si no termina por debajo con un rompimiento cerrar la operación" · fotograma fr-v4-9ad0ebb8/4079000
- v4 1:08:31: "pero va a haber momentos claros que si no protege si demás te lo va a quitar, pero también existe la posibilidad de que se dé el trade [...] no llega a tocar al 0.75 y se dé el trade, yo prefiero eso, entonces protejo" · fotograma fr-v4-9ad0ebb8/4111000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-06 · cadencia de reubicacion
Pregunta: ¿cada cuanto se reubica la orden pendiente?
Opciones: cada_vela / al_romper / otra (u otra, literal)
Casos:
- v1 0:13:58: "apenas se genera el rompimiento de la zona de liquidez pues nosotros vamos abarcando con nuestro límite [...] vamos ahí bajando el límite bajando el límite" · fotograma fr-v1-5a2a42c3/838000
- v4 1:07:31: "la orden, tú, o sea, order limit, tú lo puedes ir moviendo conforme se va desarrollando el flujo [...] seguimos usar nosotros la orden de orden límite lo seguimos moviendo para aquí abajo hasta que se rompa" · fotograma fr-v4-9ad0ebb8/4051000
- v4 1:08:57: "el límite se va actualizando o sea, el mismo límite se va moviendo a medida que no se activa se va desarrollando el precio, sí" · fotograma fr-v4-9ad0ebb8/4137000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-07 · cierre 15:00
Pregunta: ¿cierre forzoso a las 15:00 y en que huso?
Opciones: si / no (u otra, literal)
Casos:
- v4 1:15:14: "Y si hay un trade que queda abierto Por ejemplo a las 3 PM se cierra automáticamente O se deja correr hasta que llegue a su destino No, se cierra Ya, a las 3 PM en punto se cierra el trade Sí" · fotograma fr-v4-9ad0ebb8/4514000
- v3 1:03:04: "cierre agresivo opcional el vencimiento exacto de la vela H4 operativa este es un muy buen punto y puse que sí o sea, lo ideal sería que cierra la vela de H4 operativa, se cierra el trade porque ya la siguiente vela es otro movimiento" · fotograma fr-v3-982da728/3784000
- v1 0:00:49: "la primera sesión empieza a partir de las 7 hora España [...] tenemos a las 7, primera sesión y la segunda sesión a las 11" · fotograma fr-v1-5a2a42c3/49000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-08 · stop del 2.o esquema
Pregunta: ¿donde va el stop en el segundo esquema de entrada?
Casos:
- v3 0:43:29: "usualmente yo lo tengo en 0.75 o sea, 0.75 en la entrada [...] si se desarrolla más abajo entonces yo protegería aquí o sea definiría aquí vale o sea definiría aquí lo que sería mi stop loss" · fotograma fr-v3-982da728/2609000
- v4 0:20:56: "si sé que me va a generar este segundo esquema de entrada yo protejo por debajo de este, o sea, hay algunos momentos donde inclusive esta protección te puede llegar no a 0.75 sino protege ya inmediatamente entre un 0.50 y así" · fotograma fr-v4-9ad0ebb8/1256000
- v4 0:21:39: "en vez de proteger a 0.75 en lugar de eso pues lo protege es o sea por el punto más bajo en este caso como estamos de bajista alcista protege es allí en ese nivel" · fotograma fr-v4-9ad0ebb8/1299000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-09 · "dos velas como una" en mapeo
Pregunta: ¿cuando dos velas cuentan como una estructura?
Opciones: order_block_mayor / otra (u otra, literal)
Casos:
- v3 1:06:48: "Si tú lo mapeas de esta manera, es lo más probable que en una temporalidad mayor esto sea una vela [...] esto de aquí sería tu order block [...] es por eso que se considera una vela y lo demás sería ruido" · fotograma fr-v3-982da728/4008000
- v3 1:15:40: "si hay un flujo alcista, una vela contraria, pues marca un mínimo si es roja y eso, y al revés, si el flujo es bajista, una vela verde, pues una vela alcista marca un retroceso" · fotograma fr-v3-982da728/4540000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-10 · stop a 0,8: fijo o 0,75 + spread
Pregunta: ¿el 0,8 es fijo o "0,75 mas el spread del momento"?
Opciones: fijo / spread (u otra, literal)
Casos:
- v1 0:04:48: "trazar el cuadro de GAN para poder, desde aquí hasta aquí, para poder cubrir hasta un 0.75, entonces aquí perderíamos menos un 0.75" · fotograma fr-v1-5a2a42c3/288000
- v2 0:31:42: "yo cuando suelo medir lo que sería sería la entrada, lo suelo medir normalmente así, o sea, desde el punto anterior [...] al final lo suelo poner en 0.75, o sea, 0.75, entonces no estás arriesgando el 100% de la entrada" · fotograma fr-v2-c5a09508/1902000
- v5 0:03:12: "me activa la entrada y si yo protejo a 0.80, que es el SL por defecto" · fotograma fr-v5-718ecabb/192000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-11 · SL en la orden o tras el llenado
Pregunta: ¿el SL va en la orden pendiente o se pone tras el llenado?
Opciones: en_la_orden / tras_el_llenado (u otra, literal)
Casos:
- v4 0:12:07: "se arma un trade y el stop loss se pone hasta el final como del rango, ¿no? Al final del rango. Pero el stop loss como tal que se va a introducir en la operación es hasta el 0.75" · fotograma fr-v4-9ad0ebb8/727000
- v1 0:06:20: "no olvidarse de poner el cuadro, bueno el cuadro de GAN [...] en 0.75 proteger el trade, a inicio apenas se genere la entrada" · fotograma fr-v1-5a2a42c3/380000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-12 · porcentaje de vela transcurrido para bajar la proteccion a 0,50: 40 % (transcripcion heredada) o 50 % (large-v3, V1 0:15:59)
Pregunta: ¿a partir de que parte de la vela bajas el stop a 0,50?
Casos:
- v1 0:15:57: "sé que cuando ya he entrado demasiado y ya ha pasado más del 50% de la vela [...] yo prefiero reducir mi riesgo" · fotograma fr-v1-5a2a42c3/957000
- v1 0:16:43: "mi stop loss digamos máximo que yo puedo fijar o sea de pasar de 0.75 es a 0.50" · fotograma fr-v1-5a2a42c3/1003000
- v1 0:18:39: "ya estoy protegiendo a 0.50 el trade y mira me saca [...] yo ya protejo 0.50 no pierdo el 1% en total sino el 0.50" · fotograma fr-v1-5a2a42c3/1119000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-13 · ventana_inicio
Pregunta: ¿inicio de la ventana operativa (primera sesion H4)? (hora de reloj del trader)
Casos:
- v1 0:00:49: "la primera sesión empieza a partir de las 7 hora España [...] tenemos a las 7, primera sesión y la segunda sesión a las 11" · fotograma fr-v1-5a2a42c3/49000
- v1 0:25:30: "yo las de 7 a 11 lo que trabajo y de 11 a 3 de la tarde" · fotograma fr-v1-5a2a42c3/1530000
- v2 0:03:10: "hay 22 sesiones que serían la de nueva york y londres entonces usualmente comienza entre las 7 y finalizaría a las 3 de la tarde esto es sobre españa" · fotograma fr-v2-c5a09508/190000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-14 · liquidez_m15_criterio_toma
Pregunta: ¿si la liquidez de M15 se toma con cierre de cuerpo o basta la mecha? (cuerpo/mecha)
Opciones: cuerpo / mecha (u otra, literal)
Casos:
- v3 1:12:00: "¿Sol, barrio, cuánto debe penetrar el nivel? Vale. Esto pasa con mecha. O sea, pasa con la mecha nomás" · fotograma fr-v3-982da728/4320000
- v4 0:15:33: "es muy Importante que lo rompa con cuerpo Y cierre con cuerpo por encima de la zona de liquidez" · fotograma fr-v4-9ad0ebb8/933000
- v4 0:18:35: "la condicional es número uno, que el precio por encima de liquidez me tiene que cerrar con cuerpo" · fotograma fr-v4-9ad0ebb8/1115000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-15 · stop_proteccion_capital
Pregunta: ¿parte del riesgo que se guarda al proteger el trade al entrar (0,25)? (fraccion de la distancia completa)
Casos:
- v1 0:19:58: "voy reduciendo un poquito más, no lo dejo por encima del 0.25" · fotograma fr-v1-5a2a42c3/1198000
- v2 0:32:26: "en 0.75 lo que tú haces estás ya protegiendo un 0.25 del capital cuida también lo que sería tu curva de drawdown [...] ya no es lo mismo perder un 1% a perder solo 0.75" · fotograma fr-v2-c5a09508/1946000
- v3 0:45:27: "si tú ya proteges inmediatamente, que es lo que yo también haría en esta entrada, ya tienes 0.25 explícitamente, pues estás guardando" · fotograma fr-v3-982da728/2727000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-16 · objetivo_rr
Pregunta: ¿objetivo riesgo/beneficio fijo y minimo (1 a 3)? (multiplo del riesgo (1 a N))
Casos:
- v1 0:04:14: "planteas el 1.3, 1.3 como objetivo fijo, como objetivo fijo y mínimo" · fotograma fr-v1-5a2a42c3/254000
- v5 0:04:56: "yo todos los backtesting como tal, o sea estaba buscando el 1.3 [...] amplificar a 1.4" · fotograma fr-v5-718ecabb/296000
- v2 0:16:58: "Suelo buscar yo como mínimo, o sea, el ratio de riesgo-beneficio de 1 a 3" · fotograma fr-v2-c5a09508/1018000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-17 · objetivo_extension
Pregunta: ¿hasta donde se extiende el objetivo cuando se maximiza (0,50 de la liquidez)? (fraccion de la distancia hasta la liquidez de M15)
Casos:
- v1 0:28:12: "pero aquí entra la subjetividad [...] extenderías hasta un 3,50 bueno, un 3,63" · fotograma fr-v1-5a2a42c3/1692000
- v3 0:54:05: "Marcar, por ejemplo, si tengo esta zona de liquidez de aquí a aquí y veo que el precio me va a este, puedo maximizarlo hasta 0.50. Suelo usar el 0.50" · fotograma fr-v3-982da728/3245000
- v3 0:31:12: "yo el profil máximo que suelo buscar es en la liquidez de m15" · fotograma fr-v3-982da728/1872000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-18 · reentrada_tras_equal
Pregunta: ¿si tras un equal (activacion sin rotura) se reentra al romper de nuevo? (si/no)
Opciones: si / no (u otra, literal)
Casos:
- v4 0:38:20: "en 0.75 se corta la entrada ahí se corta la entrada ya no habría entrada aquí hasta que te termine de cerrar este flujo de aquí o sea tenemos una entrada en pérdida pero no puedes volver a entrar hasta que nuevamente pues o sea se cierre esta zona de control y te genere otra [...] tiene que ser nuevamente afuera" · fotograma fr-v4-9ad0ebb8/2300000
- v4 1:03:26: "llega a activar tu entrada o sea bueno tu orden límite [...] o bien se revierte o sea te genera como un igual único el high [...] pongo en 0 75 solo proteger en 0.50 y ya" · fotograma fr-v4-9ad0ebb8/3806000
- v5 0:02:46: "cuando hay un equal que no lo vamos a poder anticipar [...] contarlo como pérdida pero reentrar nuevamente si es que el precio" · fotograma fr-v5-718ecabb/166000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-19 · parciales
Pregunta: ¿si se toman parciales? (si/no)
Opciones: si / no (u otra, literal)
Casos:
- v1 0:23:13: "yo no suelo tomar parciales por ahora no lo he intentado" · fotograma fr-v1-5a2a42c3/1393000
- v2 0:18:19: "yo honestamente no lo he probado tomando parciales" · fotograma fr-v2-c5a09508/1099000
- v4 1:11:12: "Sí, sí, pero creo que he descartado eso, ¿verdad? [...] yo no lo haría, o sea, por ahora no Hasta tener un número de muestras [...] Break even y sin parciales" · fotograma fr-v4-9ad0ebb8/4272000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-20 · riesgo_por_operacion
Pregunta: ¿riesgo por operacion (1 en backtest; 0,4-0,5 en fondeo)? (porcentaje de la cuenta por operacion)
Casos:
- v2 0:27:53: "lo más óptimo sería si uno quiere escalar la cuenta rápido rápido que sea un crecimiento geométrico [...] porcentaje un 1% de la cuenta" · fotograma fr-v2-c5a09508/1673000
- v2 0:28:45: "el porcentaje que puedes manejar es un 1% aunque para la prueba de fondeo que yo lo tengo planteado sería manejarlo con un 0.50 0.50 o un 0.75 para que tengas mayores tiros" · fotograma fr-v2-c5a09508/1725000
- v4 1:27:33: "tomando en cuenta el mes más malo que hemos tenido, bueno, se ha tenido siete pérdidas consecutivas, un negativo así tal cual daría un drawdown de 3,5, o sea, arriesgando un 0,5. Obviamente si inviertes un 1% sería un 7%, entonces ahí sí te quema la cuenta" · fotograma fr-v4-9ad0ebb8/5253000
Respuesta del trader: ______________________  ¿confirma? [ ]

### P-21 · lotaje_base
Pregunta: ¿sobre que distancia se calcula el lotaje? (distancia_completa/desde_075)
Opciones: distancia_completa / desde_075 (u otra, literal)
Casos:
- v4 0:29:01: "el tamaño también de la posición de tu cuenta 1%, ponías 1% y ahí lo moviendo el SL pues se calculaba" · fotograma fr-v4-9ad0ebb8/1741000
- v1 0:21:10: "si entrábamos, digamos así, en 0.75, configurando el lotaje a esta zona de aquí [...] el lotaje calcularlo ya no en base a esto sino en base a esta zona de aquí o sea a 0 75" · fotograma fr-v1-5a2a42c3/1270000
- v2 0:33:00: "No suelo poner yo aquí, por así decirlo, calcular el OTAG y demás desde aquí [...] No lo veo viable porque en algunos casos [...] no me fue muy bien por el hecho del drawdown" · fotograma fr-v2-c5a09508/1980000
Respuesta del trader: ______________________  ¿confirma? [ ]

## Ventanas de etiquetado (solo `dev`)

Dia operativo 00:00-15:00 (Europe/Madrid). Sesiones: 07-11 (07:00-11:00), 11-15 (11:00-15:00). Decision por sesion: compra / venta / no_trade. Gramatica: `07-11: venta@08:37 e=... sl=... tp=...; 11-15: no_trade`.

| Caso | Dia | Ventana UTC | H4 madrid-00 | H4 servidor-ny-17 (sesiones) |
|---|---|---|---|---|
| caso-eurusd-2026-05-08 | 2026-05-08 | 2026-05-07T22:00Z-2026-05-08T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-05-12 | 2026-05-12 | 2026-05-11T22:00Z-2026-05-12T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-05-15 | 2026-05-15 | 2026-05-14T22:00Z-2026-05-15T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-05-18 | 2026-05-18 | 2026-05-17T22:00Z-2026-05-18T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-05-20 | 2026-05-20 | 2026-05-19T22:00Z-2026-05-20T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-05-28 | 2026-05-28 | 2026-05-27T22:00Z-2026-05-28T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-03 | 2026-06-03 | 2026-06-02T22:00Z-2026-06-03T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-05 | 2026-06-05 | 2026-06-04T22:00Z-2026-06-05T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-08 | 2026-06-08 | 2026-06-07T22:00Z-2026-06-08T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-10 | 2026-06-10 | 2026-06-09T22:00Z-2026-06-10T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-12 | 2026-06-12 | 2026-06-11T22:00Z-2026-06-12T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-17 | 2026-06-17 | 2026-06-16T22:00Z-2026-06-17T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-19 | 2026-06-19 | 2026-06-18T22:00Z-2026-06-19T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-24 | 2026-06-24 | 2026-06-23T22:00Z-2026-06-24T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-25 | 2026-06-25 | 2026-06-24T22:00Z-2026-06-25T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |
| caso-eurusd-2026-06-26 | 2026-06-26 | 2026-06-25T22:00Z-2026-06-26T13:00Z | 00:00 04:00 08:00 12:00 16:00 | 23:00 03:00 07:00 11:00 15:00 |

16 casos dev de 40 del paquete (los holdout no se muestran).
