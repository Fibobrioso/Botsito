# A-18 en las transcripciones: la clasificación de los 42 pasajes

Rama `trabajo/a18-transcripciones`, 2026-09-23. Sin merge, sin tag y sin push.

- **Qué se clasifica:** los pasajes de la salida congelada `019ed47`
  (`A18-TRANSCRIPCIONES-SALIDA.txt`), los 42 y ninguno fuera.
- **Con qué norma:** la del criterio `cdcf58e` (`A18-TRANSCRIPCIONES-CRITERIO.md` §1 y §6).
- **De dónde sale cada frase:** está copiada de esa salida, que es la cruda. Una frase que ocupa
  varios segmentos se da con sus números y los segmentos separados por « / ».
- **Qué no se hace aquí:** no se aplica la regla global. Eso lo decide el consultor.

## 0. El control positivo, antes de clasificar

- **Duración de los pasajes:** mínima 92 s, mediana 162 s, máxima 813 s (el 10, de v2).
- **El único pasaje de v5** es el 42, de `0:02:27` a `0:06:06` (219 s).
- **Las tres frases ya conocidas de v5** (`LA-CAJA-DEL-29-DE-ABRIL.md` §1c) aparecen en la
  salida:
  - «SL por defecto»: segmento #47;
  - «protejo a 0.80», en la cruda partida entre #46 («… y si yo protejo») y #47 («a 0.80, que es
    el SL por defecto …»). La tabla §1c se hizo sobre la cruda anterior, de 99 segmentos;
  - «el cálculo del RR en base al 1%»: segmento #59.

  La búsqueda no falla en el control, así que se clasifica sobre ella.

## 1. Las dos hipótesis, y la duda que atraviesa casi todos los pasajes

Los dos supervivientes (ADR-0040):

- **R = `(riesgo_real, 0,8)`**: el stop está a 0,8 de la caja y el TP se mide sobre la distancia
  entrada-stop. Eso da un TP a 2,4 cajas.
- **C = `(caja_completa, 1,0)`**: el stop está en el borde de la caja y el TP se mide sobre la caja
  entera. Eso da un TP a 3 cajas.

**D-0, la duda estructural.** En v1, v2, v3 y v4 (agosto) el trader describe un stop en DOS
tiempos:
- el lote se calcula sobre la caja entera («el lotaje se calcula desde el inicio desde el punto
  más alto hasta el punto más bajo», pasaje 18);
- al activarse la entrada, el stop se protege a 0,75 («Proteger el trade, a inicio apenas / Se
  genere la entrada, en 0.75», pasaje 2).

Ninguno de los dos supervivientes distingue el stop inicial del protegido. Leído con el stop
inicial, lo que describe es C. Leído con el protegido, es la combinación que ADR-0040 refutó
(caja completa con el stop dentro de la caja), con 0,75 en lugar de 0,8. Además, **0,75 no es
ni 0,8 ni 1,0**. Por la norma («si dudas, no responde»), **ningún pasaje con esta forma se marca
«responde»**: queda como duda, para que la resuelva el consultor.

## 2. La tabla

| pasaje | transcripción | intervalo | clase | frase exacta que decide | por qué |
|---|---|---|---|---|---|
| 1 | v1 | 0:03:29-0:05:11 | no responde · **DUDA** | #44 «pues, como corresponde, y planteas el 1.3, 1.3 como objetivo fijo, como objetivo fijo»; #50-#54 «trazar el cuadro de GAN / para poder, desde aquí / hasta aquí, para poder cubrir / hasta un 0.75, entonces / aquí perderíamos menos un 0.75» | Stop a 0,75 de la caja, que no es 0,8 ni 1,0. Si «perderíamos menos un 0.75» está en la misma unidad que el «1.3» (1:3), la unidad es la caja entera y el TP se mide sobre ella: eso apuntaría a C. Pero es inferencia entre dos frases, con deícticos («desde aquí hasta aquí»). D-0 |
| 2 | v1 | 0:05:43-0:09:46 | no responde · **DUDA** | #77-#81 «En 0.75 / Proteger el trade, a inicio apenas / Se genere la entrada, en 0.75 / Proteger el trade / Y pues plantar hasta 1.3» | Es el stop en dos tiempos (se protege a 0,75 al generarse la entrada) y un TP a 1:3 sin decir sobre qué distancia. D-0 |
| 3 | v1 | 0:14:12-0:17:36 | no responde · **DUDA** | #194 «Entonces, aquí sería mi stop loss, ¿vale?»; #218 «que es más factible qué sé yo o sea no usar en 0.75 y mejor dejarlo en 1 pues ya es otra historia» | Dice que el stop que usa es 0,75 y que 1 es la alternativa. Leído como stop de reposo, sería incompatible con C, pero 0,75 tampoco es 0,8. No habla del TP. D-0 |
| 4 | v1 | 0:18:00-0:20:36 | no responde | #245 «mira luego se me termina sacando del todo entonces yo ya protejo 0.50 no pierdo el 1% en total sino» | Gestión del stop después de la entrada. De paso fija que el 1 % corresponde a la distancia del lote, pero no dice nada del TP |
| 5 | v1 | 0:21:53-0:23:42 | no responde | #311 «aquí no menos 0 75 aquí menos 0 50 vale y aquí pues menos 0 50 vamos 0 1 menos 1 con 75 menos» | Resultados sueltos de operaciones: números sin regla |
| 6 | v2 | 0:01:00-0:02:50 | no responde | #15 «a lo mejor la subjetividad entra en lo que sería la gestión de riesgo pero en cuanto a la toma de» | Habla de la gestión de riesgo en general |
| 7 | v2 | 0:04:46-0:06:18 | no responde | #51 «Pero la subjetividad entra más que nada en lo que sería la gestión del store loss.» | No dice dónde va el stop |
| 8 | v2 | 0:15:01-0:19:45 | no responde | #144 «Suelo buscar yo como mínimo, o sea, el ratio de riesgo-beneficio de 1 a 3.» | 1:3 sin decir sobre qué distancia; vale para las dos |
| 9 | v2 | 0:20:23-0:23:57 | no responde | #201 «operativa que sería un stop loss fijo que no buscamos reducir los stop loss o sea para eso» | Stop fijo, sin decir dónde respecto a la caja |
| 10 | v2 | 0:25:04-0:38:37 | no responde · **DUDA** | #281 «Pero, por ejemplo, pongo unos aquí, ¿vale? Pero al final lo suelo poner en 0.75, o sea, 0.75, entonces no estás arriesgando el 100% de la entrada, ¿vale?»; #287 «Y al final, igual tienes planteado tu objetivo a 1 a 3.»; #300-#307 «es eso, yo calculo mi lotaje / desde aquí, o sea, como si fuera lo básico / un bot normal, pero luego / automáticamente, se de inicio / la entrada, lo pongo en 0.75 / y estoy / guardándome 0.25 / 25 que si lo agrega también a la operativa sería finalizando con un 3 con 25 no sólo un 3 un radio» | Es la descripción más completa. El lote se calcula antes de proteger («desde aquí», deíctico), luego se protege a 0,75, el objetivo sigue a 1:3 («igual») y el 0,25 guardado se suma al 3. Con eso el TP no se mide sobre la distancia hasta el stop protegido, y apuntaría a C. Pero el stop que queda es 0,75, no 1,0, y «desde aquí» no se puede fijar sin el fotograma. D-0 |
| 11 | v2 | 0:45:41-0:47:13 | no responde | #425 «ponga el stop loss, ponga el take profit» | Habla de lo que haría el bot, sin regla |
| 12 | v2 | 0:58:42-1:00:17 | no responde | #614 «Tampoco tenía, digamos, un plan de gestión de riesgo muy óptimo.» | Conversación personal |
| 13 | v2 | 1:06:08-1:07:49 | no responde | #773 «ratio riesgo-beneficio, o sea» | Habla de los fondos de inversión |
| 14 | v3 | 0:20:09-0:23:42 | no responde | #258 «Entonces, ¿qué pasa? Si no se desarrolla la zona de control, pues fácilmente yo podría poner en break-even o, como está en 0.75 la entrada, llevarlo a 0.50 o a 0.25, ¿vale? O sea, proteger.» | Gestión posterior del stop (de 0,75 a 0,50 o 0,25) |
| 15 | v3 | 0:25:42-0:30:21 | no responde · **DUDA** | #306-#308 «vale tenemos por lo general dos entradas vale porque nuestro ratio riesgo / beneficio es de 1 a 3 si nosotros perdemos 2 pero la siguiente es ganadora / ahora todavía tendríamos, restando estas dos, o sea, 3 menos 2, nos quedaría todavía un 1%, digamos, positivo, así continuamente, ¿vale?»; #321 «Que en la primera sesión, o sea, bueno, sí, la primera sesión me dio un 2.83.»; #323-#324 «Perdí / Menos 0.75» | Las ganadas valen cerca de 3 (2,83; 3,33) y las perdidas 0,75, en la misma unidad. Si es así, el TP se mide sobre la distancia con la que se pierde 1, no sobre la del stop a 0,75: apuntaría a C. Pero son números de operaciones, y un número suelto no basta. D-0 |
| 16 | v3 | 0:30:57-0:34:37 | no responde | #391 «Te la arriesgas, o sea, pero el objetivo sería un 1 a 3.» | 1:3 sin decir la base |
| 17 | v3 | 0:36:35-0:41:13 | no responde | #472 «O sea, como te digo, yo defino lo principal es mi 1 a 3.» | 1:3 sin decir la base |
| 18 | v3 | 0:43:00-0:47:38 | no responde · **DUDA** | #552-#553 «usualmente yo lo tengo en 0.75 / o sea, 0.75 en la entrada»; #557-#558 «yo protegería aquí o sea definiría aquí vale o sea definiría aquí lo que sería mi stop loss pero / claro yo mi lotaje el lotaje se calcula desde el inicio desde el punto más alto hasta el punto más»; #560-#562 «con los datos porque si yo más si yo pusiera mira bueno si yo pongo aquí dibujo el 1 a 3 / objetivamente desde allí hasta allí vale pero qué pasaría si yo pongo desde aquí hasta aquí / y hasta el mismo nivel de un 3 un 3.5 o sea un 0.5 por ciento más entiendes entonces qué pasa»; #589-#590 «ya recuerdo, es por eso que también calculo el lotaje desde aquí / pero luego protejo desde allí, o sea, si» | Dice sin deícticos que el lote se calcula sobre la caja entera. El 1:3 se dibuja «desde allí hasta allí», y medirlo desde el stop protegido hasta EL MISMO NIVEL daría «un 3.5». O sea, el nivel del TP no se mueve con el stop protegido, lo que apuntaría a C. Pero el 1:3 va con deícticos y el stop es 0,75. D-0 |
| 19 | v3 | 0:52:15-0:54:50 | no responde · **DUDA** | #683-#685 «aquí también entra de ese dilema de o sea de break even porque si yo no hubiera puesto break / even y lo hubiera dejado en 0.75 existe la posibilidad de que pues hubiera obtenido el / el RR pues el 1 a 3, o sea bueno, el RR objetivo. Vale. Ah, aquí quiero que también les pudiera» | «Dejado en 0.75» es el stop de reposo, con el objetivo a 1:3, pero no dice sobre qué distancia se mide. D-0 |
| 20 | v3 | 0:57:05-0:58:44 | no responde | #750 «de liquidez para poder seguir operando durante un beneficio objetivo mínimo 1 a 3 un rey esperado» | Lee una lista de preguntas; 1:3 sin base |
| 21 | v3 | 0:58:49-1:01:56 | no responde | #756 «entonces lo más probable es que de 0.75 se pase a 0.50 para proteger mucho más porque existe una alta probabilidad, pero muy alta probabilidad.»; #763 «Stop loss va a estar predefinido aquí, ¿vale?» | Gestión posterior del stop; «predefinido aquí» es deíctico |
| 22 | v3 | 1:02:13-1:04:34 | no responde | #796 «claro, si no, se deja en 0.75»; #824-#826 «caja de GAN / nivel 0 con un bral de invalidación y optimización / del stock, sí» | Lee una lista. Nombra la caja y el nivel 0, pero no dice dónde va el stop respecto a la caja ni cómo se calcula el TP |
| 23 | v4 | 0:00:07-0:02:28 | no responde | #9 «he calculado el lotaje ni nada pero estás haciendo cálculos simples sería 12 por 3 que es el rr» | Cuenta de resultados de enero |
| 24 | v4 | 0:04:13-0:06:21 | no responde | #50 «claro como manejamos un digamos un rr bueno pero un solo de tres cuartos o sea 0 75 pros entonces» | Pérdida de 0,75 (número suelto); no habla del TP |
| 25 | v4 | 0:06:40-0:09:41 | no responde · **DUDA** | #79 «Yo suelo proteger en 0.75 como te dije»; #121-#124 «allí. Entonces, ¿prefieres que sea / rankeado, por ejemplo, de 0.75 / a 0.80 o que sea / fijo en 0.75? Porque» | Stop protegido a 0,75. Aquí el «0.80» es un margen por el spread sobre el 0,75, preguntado por el interlocutor. No habla del TP. Se anota porque puede tocar el origen del 0,8. D-0 |
| 26 | v4 | 0:09:42-0:14:06 | no responde · **DUDA** | #200-#205 «se arma un trade y el stop loss se pone / hasta el final como del rango, ¿no? / Al final del rango. Pero / el stop loss / como tal que se va a introducir / en la operación es hasta el 0.75.»; #215-#218 «con ese porcentaje que igual va a ser / el 0.75, ya ahí se / calcule el lotaje para arriesgar el porcentaje / de la cuenta que vamos a ver»; #220 «Sí, perfecto. Ya, cerramos el tema entonces.» | La cruda no dice quién habla en cada segmento. El acuerdo es que el rango llega hasta el final, pero el stop que se introduce es 0,75 y el lote se calcula a ese 0,75. Eso choca con el pasaje 18 (lote a la caja entera). No habla del TP. D-0 |
| 27 | v4 | 0:20:20-0:23:26 | no responde | #371-#372 «entrada un poco más arriba así entonces tú tu stop loss o sea en vez de proteger a 0.75 en lugar de / eso pues lo protege es o sea por el punto más bajo en este caso como estamos de bajista alcista» | Protección en el segundo esquema de entrada; no dice nada del TP |
| 28 | v4 | 0:28:13-0:33:47 | no responde | #508 «claramente es en 075 y bueno que se acomode y ya entonces la primera forma que mostraste es»; #548 «y proteger en 0.75» | Stop protegido a 0,75; no habla del TP |
| 29 | v4 | 0:35:01-0:39:11 | no responde | #662 «bueno ya sé que me va a quitar entonces protejo al 0.75 no voy a calcular ahora pero es como que» | Stop protegido a 0,75 en un ejemplo |
| 30 | v4 | 0:39:48-0:41:21 | no responde | #691 «O bien te saca en stop loss» | Habla de si puede haber dos entradas a la vez |
| 31 | v4 | 0:43:34-0:45:29 | no responde | #752 «inclusive pues podrías proteger a 0.75»; #756 «a ver, expandes hasta el 1.3» | 0,75 y 1:3 en un ejemplo, sin decir la base |
| 32 | v4 | 0:46:13-0:48:04 | no responde | #788 «estos los por qué porque si yo marco de aquí aquí mira protegiendo 0.75 pues no llevo o sea no se» | Un ejemplo, con deícticos |
| 33 | v4 | 0:48:05-0:49:37 | no responde | #814 «entonces, porque mi RR es de 1 a 3» | 1:3 sin base |
| 34 | v4 | 0:51:35-0:54:30 | no responde | #890 «inclusivos a dibujas el 137 al 13 o inclusive un poco más pero teniendo como fijo el 13 ahí se te» | 1:3 fijo, sin base |
| 35 | v4 | 0:59:13-1:01:09 | no responde | #987 «la correlación no 100% perfecta pero más perfecta para estas 3 temporalidades» | Habla de temporalidades |
| 36 | v4 | 1:03:18-1:04:56 | no responde | #1069 «0 76 a ver pongo en 0 75 y lo que se entiende es lo que se ve pongo en 0 75 solo proteger en» | Stop a 0,75 y su gestión; no habla del TP |
| 37 | v4 | 1:07:22-1:09:34 | no responde | #1155 «la entrada pero qué pasa 1 lo ideal sería proteger a 0.75 pero»; #1165 «protejo, pues aquí tengo un stop loss» | Un ejemplo de protección |
| 38 | v4 | 1:10:25-1:13:53 | no responde | #1239 «O sea, el stop ya quedó que es en 0.75»; #1246 «el rr a ver yo lo tengo en un 13 entonces influye mucho porque como te digo yo lo si tuviera que» | Stop a 0,75 (lo dice el interlocutor) y RR 1:3, sin decir sobre qué distancia se mide |
| 39 | v4 | 1:18:32-1:21:20 | no responde · **DUDA** | #1379-#1380 «si nos vamos por números arriesgando un 1% 12 x 3 son 39 ahora el 9 no es un 9 como tal que / que perdemos si no promediando un 0.75 por 0.75 sería 6.75 o sea 36 menos 6.75 es casi más de un» | Las ganadas cuentan 3 por cada 1 % y las perdidas 0,75. Es la misma cuenta que el pasaje 15, y apuntaría a C. Pero es un cálculo de resultados, no la regla. D-0 |
| 40 | v4 | 1:25:05-1:28:45 | no responde | #1518-#1519 «¿Nos quedamos con un riesgo estático de 0.75 / O 0.75 de la cuenta» | Riesgo sobre la cuenta, no sobre la caja |
| 41 | v4 | 1:31:53-1:33:27 | no responde | #1600 «que protege la entrada y nada tienes si se da pues bien porque pasa que se suele dar eso es» | Break-even |
| 42 | v5 | 0:02:27-0:06:06 | no responde · **DUDA** | #46-#47 «vamos aquí, vale, yo activo la entrada aquí, mira, me activa la entrada y si yo protejo / a 0.80, que es el SL por defecto, que no me permite dejarlo, vale, la cosa es esa, si»; #59 «el cálculo del RR en base al 1%» | Stop a 0,80 «por defecto». Si es el stop inicial, es incompatible con C; si «protejo» es el movimiento al activarse la entrada, como en el pasaje 2, vale para las dos. «RR en base al 1%» no dice sobre qué distancia se mide ese 1 %. D-0 |

## 3. El recuento

| clase | pasajes |
|---|---|
| responde → riesgo_real | **0** |
| responde → caja_completa | **0** |
| no responde | **42** (con **DUDA** anotada: 11, que son 1, 2, 3, 10, 15, 18, 19, 25, 26, 39 y 42) |

## 4. Las dudas, para el consultor

- **Hacia dónde apuntan.** En cinco de ellas (1, 10, 15, 18 y 39) lo dicho por el trader apunta,
  si se resuelve D-0, a **C (caja completa)** para la base del TP. En todas, el lote se mide sobre
  la caja entera y el nivel del TP no se mueve al proteger. **Ninguna apunta a R.**
- **Por qué quedan como duda.**
  - (a) El stop de reposo que describen es **0,75**, que no es ni 0,8 ni 1,0.
  - (b) Los supervivientes no dicen si «el stop» es el inicial o el protegido (D-0).
  - (c) Las frases del TP usan deícticos («desde aquí», «desde allí hasta allí») que solo el
    fotograma fija.
  - (d) Dos de ellas (15 y 39) son cuentas de resultados, no la regla.
- **Dos dudas van en sentido distinto.**
  - El pasaje 26 (v4, 30 de agosto) acuerda calcular el lote al 0,75, y eso choca con el 18.
  - El 42 (v5) llama al 0,80 «el SL por defecto».
- **Todo esto es de agosto**, anterior al lineamiento del 9 de septiembre (stop 0,8). La
  clasificación no lo corrige: lo anota.

## Estado

CLASIFICADO. No se ha aplicado la regla global. WAITING_FOR_USER_VALIDATION de las dudas.
