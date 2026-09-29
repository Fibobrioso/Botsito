# El embudo de las 77: dónde deja el bot de acompañar al trader en construcción

Rama `trabajo/embudo-77`, 2026-09-28, desde `main` en `stable/F23-selector-orden-stop` (`ea8153f`).
Es una **medición**: no cambia la estrategia, el productor ni el bróker, y no corrige nada de lo que
encuentra. Solo construcción, abril y agosto de 2026, por la compuerta del arnés; las velas del mes
anterior de cada uno las lee el arnés para el calentamiento del sesgo H4, como siempre, y de ellas
no sale aquí ni una fecha ni un precio.

## 1. Cómo se midió

`scripts/embudo_77.py` corre el motor cableado igual que `motor arnes --simular`, en diagnóstico:
A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-47 `stop_en_ruptura`, A-27 `0` (el mismo
diagnóstico de `SELECTOR-ORDEN-STOP.md` §3), una vez por cada lectura de A-21. Para cada una de las
77 operaciones del trader anota el **primer paso** en el que el bot deja de acompañarla, midiendo lo
que el motor hizo ese día: la traza de la sesión, la memoria del productor, el bróker y las parejas
del criterio de fidelidad (ADR-0043, 3 puntos y 15 minutos). La clasificación es una función pura,
`clasificar`, y el test la fija sobre casos sintéticos.

**El orden es el del pipeline real, y difiere del de la guía en dos cosas:**

1. **Las reglas van antes que el bróker.** En el motor, las gates (RN-005, RN-008, RN-009, RN-032 y
   las demás) actúan en el mismo minuto en que RN-011 y RN-015 van a colocar la orden, y el bróker
   solo ve las órdenes que pasan. Por eso aquí «reglas» es el paso 7 y «bróker» el 8.
2. **«La orden nace con el precio ya roto» no es un paso aparte: es el rechazo `precio_invalido`
   del bróker.** Con la orden stop colocada en el cierre del breaker (ADR-0058 §2), una stop cuyo
   precio ya se ha pasado está del lado equivocado y el bróker la rechaza (ADR-0057). Se cuenta una
   vez, en el paso 8. El paso 6, «momento», queda para un breaker que cierra más de 15 minutos
   después de la entrada del trader.

Los pasos, en ese orden: **1 sesión** (el instante del trader fuera de su ventana); **2 sesgo**
(RN-003 sin sesgo, o con el contrario a la operación); **3 liquidez** (el productor no tiene toma
de M15 a tiempo, o la que tiene es de una sesión anterior y su zona no casa con la del trader);
**4 breaker** (tras la toma no hay esquema); **5 caja** (el 0 del bot a más de 3 puntos de la
entrada del trader); **6 momento** (el breaker cierra más de 15 minutos después del trader);
**7 reglas** (con la zona formada no sale orden); **8 bróker** (la orden se rechaza); **9 llenado**
(no se llena, se llena fuera de tolerancia, o su operación ya casa con otra del trader); y
**coincide**.

Dos detalles de la medida:
> **Corregido el 2026-09-28** (rama `trabajo/registrar-embudo`): una toma es un pivote tomado, no
> una M15; ver el recuadro de §4, punto 3.

- **Una toma de RN-004 es el cierre de la M15 que toma, no cada minuto en que el hecho se vuelve a
  fijar.** RN-004 fija `liquidez_tomada` en cada M1 mientras esa M15 sea la última cerrada, así que
  la traza trae la misma toma hasta quince veces. El script cuenta tomas distintas.
- **Las gates que bloquean se leen del minuto exacto del cierre del breaker**, envolviendo el
  intérprete solo para grabar su evento; la traza de la sesión lo junta todo y pierde el minuto. Y
  solo cuentan las gates que **prohíben** el efecto bloqueado: RN-027 dispara en ese minuto porque
  redondea el lote, pero no prohíbe nada.

## 2. La tabla del embudo

Operaciones del trader que mueren en cada paso, por lectura de A-21:

| paso | `solo_una_zona_de_control` | `sin_mecha_mas_alla_del_extremo` |
|---|---|---|
| 1. sesión | 0 | 0 |
| 2. sesgo | 19 | 19 |
| 3. liquidez | 26 | 26 |
| 4. breaker | 13 | 14 |
| 5. caja | 15 | 14 |
| 6. momento | 0 | 0 |
| 7. reglas | 0 | 0 |
| 8. bróker | 1 | 1 |
| 9. llenado | 1 | 1 |
| **coincide** | **2** | **2** |
| total | 77 | 77 |

Por motivo (las dos lecturas solo difieren en una operación, la del 17 de agosto a las 05:17Z, que
la segunda lectura rechaza en el breaker por la mecha y la primera deja llegar a la caja):

| paso | motivo | 1.ª | 2.ª |
|---|---|---|---|
| sesgo | contrario a la operación | 12 | 12 |
| sesgo | sin sesgo (`ambiguo`) | 7 | 7 |
| liquidez | la toma del productor es de una sesión anterior, y en la sesión hubo tomas nuevas que no usa | 15 | 15 |
| liquidez | la toma del productor es de una sesión anterior, y en la sesión no hubo otra | 4 | 4 |
| liquidez | ninguna toma de M15 antes del trader + 15 min | 7 | 7 |
| breaker | la primera ruptura deja más zonas de control que el tope (RN-009) | 9 | 9 |
| breaker | ninguna M1 pasa la referencia antes del trader + 15 min | 4 | 4 |
| breaker | la lectura de A-21 rechaza la primera ruptura | 0 | 1 |
| caja | el 0 a más de 3 puntos; la zona del bot se formó más de 15 min antes que la entrada | 13 | 12 |
| caja | el 0 a más de 3 puntos; zona reciente | 2 | 2 |
| bróker | `precio_invalido` | 1 | 1 |
| llenado | su operación ya casa con otra del trader | 1 | 1 |

**Lo que no se ve en la tabla y pesa igual.** Los pasos 6 y 7 salen a cero porque las operaciones
mueren antes, no porque no actúen. Por días (42): el productor toma liquidez en 40, forma zona en 28
(1.ª) y 21 (2.ª), y de esas zonas **RN-005 prohíbe colocar la orden en 8 y 6 días**; de las órdenes
que salen, el bróker rechaza 9 y 8 por lado equivocado y 4 y 1 por volumen máximo; se llenan 6 y 5.

**Una anotación, que no clasifica.** Para las 39 operaciones muertas en liquidez, breaker o caja con
el sesgo a favor y alguna toma anterior, el script repite la detección del productor, minuto a
minuto y con las mismas funciones, desde la **última** toma de RN-004 anterior al trader. El
esquema que sale casa con el del trader en **3 (1.ª) y 2 (2.ª)**; en 22 y 25 no hay esquema antes del
trader + 15 min, y en 14 y 12 lo hay a más de 3 puntos. Mirar la toma más cercana no basta: la
geometría del breaker y de la caja también se separa.

## 3. Los tres pasos que más matan

### 3.1 Liquidez (26 y 26)

**Lo que la gobierna.** 19 de las 26 las decide la **zona única por día con memoria de un solo uso**
del productor (`mem["toma"]`, `mem["esquema"]`, `mem["zona_id"]` en `engine/zonas.py`): es
ADR-0055, superseded en parte por **ADR-0056 §4** («la caja se traza por operación»), que todavía no
está implementado. Si una toma de la sesión anterior sigue valiendo es **A-46**, ABIERTA. Las otras
7 no tienen toma de M15 a tiempo: **RN-004**, con **A-35** (qué es un pivote formado, aquí en
diagnóstico) y **A-45** (el cuerpo se mira en la M15, PROVISIONAL por ADR-0054 §4).

**Casos** (los de las tres secciones, con la primera lectura; con la segunda cada uno muere en
el mismo paso, y solo cambia un detalle del bot: el 10 de agosto no forma zona).
- **3 de agosto, sesión 11-15.** El trader vende cuatro veces, a las 09:46Z, 09:52Z, 12:03Z y 12:10Z,
  entre 115274 y 115322. El bot tiene una sola zona ese día, la venta con 0 en 115363 que nace de la
  toma de las 06:00Z; se llenó por la mañana, coincidió con la primera venta del trader y saltó su
  stop. En la sesión de la tarde RN-004 fija tomas nuevas (una antes de las dos primeras ventas, tres
  antes de las dos últimas) y el productor no las usa.
- **10 de agosto, sesión 11-15.** El trader compra a las 11:57Z y a las 12:38Z. En esa sesión el
  sesgo del bot ya es alcista, pero su única zona es una venta de la sesión anterior (0 en 115544,
  06:01Z, rechazada por volumen máximo), y las seis y ocho tomas nuevas de la sesión no cuentan. Aquí
  se juntan A-46 y A-39 (qué pasa con lo de la primera sesión cuando la segunda cambia el sesgo).
- **19 de agosto, sesión 11-15.** El trader compra a las 09:03Z y a las 11:46Z con el sesgo del bot
  alcista, y RN-004 no fija ninguna toma en la sesión ni el productor registra ninguna en todo el
  día: no hay liquidez de M15 tomada con cuerpo según la lectura de A-35 del diagnóstico.

### 3.2 Sesgo (19 y 19)

**Lo que lo gobierna.** **RN-003** (ADR-0044: la H4 previa cerrada, al abrir la sesión) y **RN-033**,
que prohíbe operar con `ambiguo` o `insuficiente`. Las 7 sin sesgo son `ambiguo`, **A-34** (la H4
rompe los dos extremos). Las 12 contrarias son operaciones del trader contra el sesgo H4 del bot:
**A-26** (el flujo de M15 va contra H4) y, en la segunda sesión, **A-39**. El motor no las opera
porque RN-005 y el productor solo miran el lado del sesgo.

**Casos.**
- **9 de abril.** El trader vende a las 07:12Z y a las 09:15Z (116659 y 116748); el bot tiene sesgo
  alcista en las dos sesiones y su única zona es una compra (0 en 116677, 05:02Z).
- **27 de agosto, sesión 07-11.** Dos ventas, a las 08:04Z y 08:12Z, con el sesgo del bot alcista; su
  zona es una compra de caja 5 que el bróker rechaza por volumen máximo.
- **13 de abril, sesión 11-15.** Dos compras, a las 10:26Z y 12:02Z, con el sesgo `ambiguo`: RN-033
  prohíbe abrir toda la sesión.

### 3.3 Caja (15 y 14)

**Lo que la gobierna.** 13 y 12 de estas muertes son **otra vez la zona única por día**: el trader
entra más de 15 minutos después de que se formara la única zona del bot, con otra estructura, y la
caja del bot se queda a entre 6 y 151 puntos (ADR-0055; ADR-0056 §4). Las 2 recientes
son **geometría del bloque**: qué velas forman la caja, **A-48**; con la vela cerrada o en
formación, **A-49**; en qué punto de la mecha va la orden, **A-36**; y la lectura de «limpia»,
**A-21**. Bajo todas está **RN-011**, que traza la caja del bot.

**Casos.**
- **23 de abril, sesión 07-11.** La zona del bot es una venta con 0 en 116994, formada a las 05:01Z;
  su orden stop se llenó por el respaldo M1 (una hora sin ticks, ya señalada en
  `SELECTOR-ORDEN-STOP.md` §3) y la posición cerró por stop. El trader vende a las 05:30Z, 05:53Z y 06:49Z, a 24, 44 y 78 puntos de ese 0.
- **26 de agosto, sesión 07-11.** El bot coincide con la venta de las 05:49Z en 116652: su stop con
  0 en 116656 se llena a las 05:48Z en 116655 y cierra por objetivo. Las dos ventas siguientes del trader, a las 07:03Z y 08:31Z, quedan a 24 y 96 puntos de
  esa misma zona, porque el bot no traza otra.
- **6 de agosto, 06:07Z.** El trader vende en 115488; el bot forma un segundo esquema con 0 en 115501
  a las 06:10Z, tres minutos después: 13 puntos. Es la caja del bloque, no la zona única.

**El cuarto, cerca:** el breaker (13 y 14). 9 son la primera ruptura con más zonas de control que el
tope de **RN-009** (A-20, RESUELTA) y, como el productor no busca otro breaker para la misma toma
(`PREPARACION-A21.md`), el día se queda sin zona; 4 no llegan a pasar la referencia a tiempo.

## 4. Errores de código: ninguno medido, y tres decisiones sin fuente

**Ningún paso en el que el bot deja al trader lo decide un error de código.** En cada uno se
comprobó que el código hace lo que dice un documento escrito:

| lo que decide | dónde está escrito |
|---|---|
| una zona por día, memoria de un solo uso | ADR-0055; su sustituta, ADR-0056 §4, sin implementar |
| la primera ruptura decide para la toma | `PREPARACION-A21.md` |
| el cuerpo de la toma se mira en la M15 | ADR-0054 §4, PROVISIONAL (A-45) |
| la stop se coloca en el cierre del breaker | ADR-0058 §2, PROVISIONAL |
| la pendiente del lado equivocado se rechaza | ADR-0057, PROVISIONAL |
| un llenado por el respaldo M1 en una hora sin ticks | ADR-0051 §5 y §8, marcado en la traza |
| el lote que supera el volumen máximo se rechaza | el perfil de cuenta; pendiente 37 (A-18) |

**Lo que sí sale son tres decisiones del código que ningún documento fija.** No son errores
demostrados, porque nada dice lo contrario, pero cada una decide resultados y ninguna tiene fuente.
Se reportan aquí y no se tocan.

1. **RN-005 compara con el nivel tomado solo el 0 de la zona.** `se_desarrolla_en_el_lado_de_ruido`
   (`engine/zonas.py`) llama ruido a una compra cuyo 0 queda por encima del nivel, y a una venta cuyo
   0 queda por debajo. La spec dice dónde está la operativa del trader («por debajo» en alcista, «por
   encima» en bajista) y no qué punto de la zona se mira. **Medido:** RN-005 deja sin orden 8 días
   con la primera lectura y 6 con la segunda, y en los 8 **la caja cruza el nivel por 1 a 5 puntos
   con el 1 en el lado donde opera el trader**; por ejemplo, el 17 de abril una venta con nivel en 117837, 0 en
   117836 y 1 en 117844. Es el orden de magnitud de A-16 (Oanda frente a Dukascopy). Ninguna de esas
   8 zonas habría coincidido con el trader, porque sus operaciones mueren antes; lo que cambia es
   cuántas operaciones hace el bot.
2. **La M15 que cierra justo en la apertura de la sesión cuenta como toma dentro de la sesión.**
   RN-004 se evalúa desde el primer minuto de la sesión con la última M15 cerrada, así que la que
   cierra a las 07:00 locales (y que tomó entre las 06:45 y las 07:00) cuenta, y las anteriores no.
   En 7 de los 40 días con toma, la del productor es esa. Contesta en la práctica **A-43**
   (ABIERTA), y solo para una vela.
3. **RN-004 vuelve a fijar `liquidez_tomada` en cada M1** mientras la misma M15 sea la última
   cerrada. El productor solo registra la primera y el motor no cambia por ello, pero todo recuento
   que se haga sobre `fijados` cuenta la misma toma hasta quince veces. Este informe lo sufrió en su
   primer ensayo.

> **Advertencia y corrección (2026-09-28, rama `trabajo/registrar-embudo`).** **Todo recuento sobre
> la traza tiene que deduplicar por toma, y una toma es un PIVOTE tomado, no un minuto ni una M15.**
> RN-004 vuelve a fijar `liquidez_tomada` en cada M1 mientras la misma M15 sea la última cerrada, y
> una M15 posterior que vuelve a cruzar el mismo pivote también lo fija. Medido en construcción, con
> la primera lectura: 2992 minutos con RN-004, 206 M15 distintas y **118 pivotes distintos** (lado,
> nivel y vela contraria). Este informe deduplicó por M15, no por pivote, y eso toca a tres cifras
> suyas, que no se reescriben:
> - **La clasificación no cambia.** Las 15 operaciones de «la del productor es de una sesión
>   anterior y no usa las nuevas» tienen en su sesión, antes del trader + 15 min, al menos un pivote
>   distinto del que usa el productor (15 de 15).
> - **Los recuentos de «toma(s) nueva(s)» del detalle son de M15, no de pivotes.** En §3.1, el 10 de
>   agosto son **2 y 3 pivotes**, no «seis y ocho tomas»; el 3 de agosto, 1 y 3, como decía.
> - **La anotación de §2 baja de 3 a 1 de 39** con la primera lectura si se parte de la primera toma
>   del último pivote anterior al trader, y no de su última M15: el 22 de abril a las 08:02Z y el 17
>   de agosto a las 05:17Z casaban porque su última M15 volvía a tomar un pivote ya tomado. Lo que la
>   anotación decía -que mirar la toma más cercana no basta- sale más fuerte.
>
> No hay una utilidad común de lectura de trazas donde poner la deduplicación: cada script lee
> `TrazaSesion.fijados` por su cuenta, y `TrazaSesion.hechos_producidos` es un conjunto y no cuenta.
> Revisados los que la leen hoy: `scripts/verificacion_a21.py` cuenta minutos y los llama minutos;
> `bloque_de_la_caja.py`, `orden_stop_o_limite.py` y `verificacion_a21_entradas.py` solo usan la
> primera toma del día; el visor lista los hechos uno por minuto, sin contarlos. Ninguno más publica
> un recuento de tomas.

## 5. Fase 3 · Test

`tests/unit/test_embudo_77.py`, tres tests sobre hechos sintéticos, sin leer ni una vela:
- cada paso del embudo, en el orden del pipeline, con su motivo y su detalle;
- que una toma de una sesión anterior cuya zona sí casa con el trader no mata en liquidez y deja
  seguir el embudo;
- y la tabla por lectura, fijada entera.

## 6. Estado

Script, test e informe en un solo commit sellado. No se corrige nada: RN-005, la M15 de la
apertura y el recuento de RN-004 quedan para su propia rama. **Rama lista para revisión, NO
cerrada.**
