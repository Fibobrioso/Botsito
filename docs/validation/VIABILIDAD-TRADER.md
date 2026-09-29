# ¿Habrían pasado la fase 1 de FTMO las operaciones del propio trader?

> **NO SE ENSEÑA AL TRADER.** Ni este informe, ni sus cifras, ni nada que salga de él entra en
> material para él: saber cómo le iría en FTMO sesgaría sus respuestas en las sesiones. Solo para el
> consultor y para Aleks.

Rama `trabajo/viabilidad-trader`, 2026-09-28, desde `main` en `16e973d`. Es una **medición**: no
cambia la estrategia, el bot ni el bróker, y no se ha ajustado nada para mejorar la cifra. Solo
construcción: las 77 operaciones de los días `dev` de abril y agosto de 2026, material de desarrollo
sin ningún día en ninguna partición (comprobado con `casos_reservados` y `casos_ocultos` antes de
leer; declarado en `HOLDOUT-EXPOSICIONES.md`). Script: `scripts/viabilidad_trader.py`.

## 0. Fase 0 · Qué hay y qué falta

**Lo que trae cada operación.** El caso (`knowledge/cases/dev/`) trae el instante del llenado, la
dirección, la entrada y el stop inicial (`initialSL`). Del libro del trader se leyeron, solo para
las filas de los días `dev` y por el lector que no enumera nada (`corpus/libro.py`), `avgClosePrice`
(el precio de salida real), `dateEnd` (su instante), `rPnL` (el resultado) y `status`. El signo de la
salida real en R casa con el signo de `rPnL` en **77 de 77** (33 ganan, 39 pierden, 5 a cero): la
lectura es coherente.

**Lo que falta, y qué se hace sin ello:**

| falta | consecuencia |
|---|---|
| **8 filas sin `initialSL`** (3 de abril, 5 de agosto) | sin stop no hay riesgo ni R: quedan fuera; las 77 son las que lo tienen |
| **el objetivo planeado**: el libro no lo registra (`idealTP` sale del lado de la pérdida en 4 filas y `maxTP` es el cierre de las ganadoras, ADR-0037 §7) | la simulada usa la regla de la spec: `objetivo_rr` (3, CONFIRMED) por la distancia al stop inicial |
| **los movimientos del stop**: el libro solo da la salida | la simulada usa el stop inicial; el único movimiento documentado con instante y caso inequívoco se reproduce (§1) |
| **la caja (0 y 1)** de casi todas las operaciones | no se sabe si el stop inicial está en el 1 o en el 0,8 (BLOQUE-DE-LA-CAJA.md §5: las dos cosas pasan), así que el riesgo de la spec se da con sus dos extremos (abajo) |
| **el camino dentro de cada operación** en la serie anotada | la anotada solo abre y cierra: no ve la equity flotante, y para la regla diaria es optimista |
| **si la comisión de FTMO es por lado**: R12, NO ENCONTRADA | se usa el perfil: 5 USD por lote **en cada lado**, supuesto conservador del consultor (CONFIRMED en `ftmo-2step-swing-100k.yaml`) |

**El riesgo y el lote de la spec.** `riesgo_por_operacion` = **0,5 %**, **CONFIRMED**, sobre el
saldo actual (`base_calculo_riesgo: saldo_actual`, CONFIRMED), con el lote medido en el 0,8 de la
caja (`lotaje_base: hasta_stop_fraccion`, CONFIRMED, ADR-0020). Como aquí la distancia conocida es
la del stop inicial, el 0,5 % se aplica a esa distancia; si el stop inicial está en el 1 de la caja,
la spec arriesgaría 0,5 / 0,8 = **0,625 %** hasta él. Los dos son la spec. **1 % y 2 % son
sensibilidad, fuera de la spec.**

**Las reglas de FTMO**, de `docs/validation/FTMO-REGLAS.md` y del perfil que las recoge
(`ftmo-2step-swing-100k.yaml`, fase `reto`):
- **R1**, objetivo: «10% for the FTMO Challenge», cumplido «once your account balance exceeds the
  Initial Simulated Capital by the required Profit Target with all positions closed».
- **R2**, pérdida diaria: la equity no puede bajar de «the account balance recorded at 00:00 CE(S)T
  of the current day» menos el 5 % del capital inicial.
- **R3**, pérdida total: límite fijo en el capital inicial menos el 10 % («Limit = $90,000»).
- **R4**, al menos **4 días de trading**, «measured from 00:00:00 to 23:59:59 CE(S)T».
- **R11**, «maxTradeVolume: 100» lotes, y **R12**, comisión de 5 USD por lote.

## 1. Fase 1 · Cómo se reprodujo cada operación

- **Serie SIMULADA.** Cada operación se abre en su instante y a su entrada (el caso es el llenado,
  ADR-0043), desplazada **−2 puntos** a la escala de Dukascopy junto con su stop y su objetivo
  (OANDA va unos 2 puntos por encima: BLOQUE-DE-LA-CAJA.md §2.3). Después la repite el bróker
  simulado sobre los **ticks de Dukascopy**, con el spread de cada tick, el stop al toque y al precio
  del tick (ADR-0057 d1), la comisión del perfil y el cierre forzoso al final de la ventana (RN-002).
  Los 42 días tienen ticks; en las horas que Dukascopy no sirvió, el respaldo M1 (ADR-0051 §5).
- **El único movimiento de stop reproducido: v7-3**, la venta del 3 de agosto llenada a las
  06:07:40 UTC (orden 2 puntos bajo el 0 y stop en el 1, como el caso), cuyo stop se ve en el 0,8
  (1.15383) en el fotograma de las 06:11:59 UTC (BLOQUE-DE-LA-CAJA.md §5.1). Se mueve en ese
  instante. Los demás de §5.1 o no casan sin ambigüedad con una operación del caso o no tienen
  instante: se quedan con el stop inicial.
- **Serie ANOTADA.** Las mismas operaciones con la salida real del trader (`avgClosePrice` en
  `dateEnd`), el mismo lote y la misma comisión.
- **El lote**, en las dos: el riesgo sobre el saldo realizado al abrir, hasta el stop inicial,
  redondeado hacia abajo a 0,01. Una operación cuyo lote pasa de 100 no entra (R11), en las dos.
- **R** es lo ganado o perdido en unidades de la distancia al stop inicial. **R neta** le resta la
  comisión, que en R no depende del lote: con EURUSD y cuenta en USD un punto por lote vale un
  dólar, así que 5 USD por lado cuestan **10 / distancia en puntos** R.

**Lo que manda sobre todo lo demás: los stops son cortos, y la comisión se come la ventaja.** La
distancia al stop inicial tiene mediana de **15 puntos**; **19 de 77 están por debajo de 10**, y la
mínima es de 3. La comisión cuesta de media **0,86 R por operación** (mediana 0,67 R; máximo 3,33 R).
Y al 0,5 % hay 4 operaciones con stops de 3 a 5 puntos cuyo lote pasa de 100: no entran. Al 2 %, 57.

## 2. Fase 2 · Esperanza en R, con intervalo del 95 % por bootstrap

10.000 remuestreos con semilla fija. **Con 77 operaciones la muestra es pequeña: manda el
intervalo, no la cifra.**

| tramo | serie | n | aciertan | R medio ganadoras | R medio perdedoras | esperanza bruta [IC 95 %] | **esperanza neta [IC 95 %]** |
|---|---|---|---|---|---|---|---|
| abril | anotada | 35 | 43 % | +3,64 | −0,99 | +1,05 [+0,31; +1,83] | **+0,22 [−0,61; +1,09]** |
| abril | simulada | 32 | 44 % | +3,00 | −1,20 | +0,64 [−0,09; +1,37] | **−0,03 [−0,79; +0,75]** |
| agosto | anotada | 42 | 43 % | +3,33 | −1,00 | +0,93 [+0,31; +1,55] | **+0,05 [−0,63; +0,74]** |
| agosto | simulada | 41 | 44 % | +2,85 | −1,14 | +0,61 [−0,01; +1,24] | **−0,23 [−0,92; +0,47]** |
| **abril+agosto** | **anotada** | **77** | 43 % | +3,47 | −0,99 | **+0,98 [+0,50; +1,48]** | **+0,13 [−0,41; +0,67]** |
| **abril+agosto** | **simulada** | **73** | 44 % | +2,91 | −1,16 | **+0,62 [+0,15; +1,09]** | **−0,14 [−0,64; +0,36]** |

**Lo que dice.** Antes de la comisión, las operaciones del trader tienen ventaja en las dos series,
y el intervalo de abril+agosto no toca el cero. **Con la comisión del perfil, los intervalos de todos
los tramos cruzan el cero en las dos series**: la muestra no sostiene que haya ventaja después de
costes. Si la comisión fuera una sola vez por operación, costaría la mitad (0,43 R de media), y la
esperanza neta de abril+agosto quedaría hacia +0,55 R en la anotada y +0,19 R en la simulada: una
cuenta hecha aparte, sin intervalo. Qué cobra FTMO de verdad lo mide la demo (Next Action A2).

## 3. Fase 2 · Las reglas de FTMO, escenario a escenario

**El veredicto, con la regla escrita antes de correr:** **pasa** si la cuenta llega al objetivo con
los días mínimos y sin romper un límite; **no pasa** si rompe la pérdida diaria o la total; **no
concluyente** si no llega a ninguna de las dos cosas en la muestra. Y si la esperanza neta tiene un
intervalo que cruza el cero -en todos los casos-, la muestra no sostiene que se repita. «Peor día» es
lo máximo que la equity cayó en un día desde el saldo del corte, sobre el capital inicial (el límite
es 5 %); «peor total», lo máximo que cayó bajo el capital inicial (límite 10 %); «caída», la mayor de
pico a valle del saldo realizado.

### 3.1 El escenario de la spec: 0,5 %

| tramo | serie | veredicto | cuándo | días operados | peor día | peor total | caída | saldo final | n |
|---|---|---|---|---|---|---|---|---|---|
| abril | anotada | **pasa** | 13-abr 11:00 UTC, 6 días | 6 | 1,02 % | 0,08 % | 4,40 % | 109.498 | 32 |
| abril | simulada | **no concluyente** | - | 15 | 3,35 % | 2,85 % | 5,87 % | 99.384 | 32 |
| agosto | anotada | **no concluyente** | - | 17 | 1,89 % | 1,30 % | 3,06 % | 107.257 | 38 |
| agosto | simulada | **no pasa** | 7-ago 12:30 UTC, pérdida diaria | 4 | 5,38 % | 5,77 % | 8,22 % | 95.218 | 41 |
| abril+agosto | anotada | **pasa** | 13-abr 11:00 UTC, 6 días | 6 | 1,02 % | 0,08 % | 4,40 % | 117.444 | 70 |
| abril+agosto | simulada | **no pasa** | 7-ago 12:30 UTC, pérdida diaria | 19 | 5,35 % | 6,35 % | 11,77 % | 94.631 | 73 |

El «saldo final» y la «caída» siguen la serie entera aunque la cuenta hubiera quedado suspendida o
superada antes; el veredicto es el de la cuenta en su instante.

**La curva de saldo al cierre de cada día operado, 0,5 %, abril+agosto (en miles):**

- anotada: 04-01 101,9 · 04-03 104,3 · 04-06 106,4 · 04-09 106,3 · 04-10 107,0 · 04-13 109,3 ·
  04-14 109,3 · 04-16 107,7 · 04-17 106,8 · 04-22 109,4 · 04-23 106,9 · 04-24 107,0 · 04-27 107,7 ·
  04-28 106,8 · 04-29 109,5 · 08-03 109,3 · 08-04 108,2 · 08-06 109,8 · 08-07 110,8 · 08-10 111,0 ·
  08-11 110,0 · 08-12 111,1 · 08-13 109,0 · 08-14 110,7 · 08-17 112,1 · 08-19 115,3 · 08-20 114,5 ·
  08-21 115,0 · 08-25 114,2 · 08-26 117,1 · 08-27 117,1 · 08-31 117,4
- simulada: 04-01 101,3 · 04-03 103,5 · 04-06 102,6 · 04-09 99,9 · 04-10 100,4 · 04-13 100,8 ·
  04-14 103,1 · 04-16 101,6 · 04-17 100,7 · 04-22 100,9 · 04-23 97,6 · 04-24 99,0 · 04-27 99,6 ·
  04-28 98,7 · 04-29 99,4 · 08-03 98,8 · 08-04 97,7 · 08-06 99,0 · **08-07 93,6** · 08-10 93,5 ·
  08-11 92,6 · 08-12 93,4 · 08-13 91,7 · 08-14 92,8 · 08-17 93,8 · 08-19 96,3 · 08-20 95,4 ·
  08-21 97,6 · 08-24 96,2 · 08-25 94,0 · 08-26 94,2 · 08-27 94,3 · 08-31 94,6

(La anotada del 13 de abril toca 110.056 a las 11:00 y cierra el día en 109,3: el objetivo se cumple
en el primer cierre que lo alcanza.)

**El día que rompe la simulada, 7 de agosto.** Cuatro ventas; las dos primeras con stops de 6 y 5
puntos, que con el 0,5 % piden 82 y 98 lotes: la comisión de cada una cuesta cerca de 1 % de la
cuenta. Y la cuarta, con el stop a 38 puntos, salta a las **12:30:01 UTC en un tick de Dukascopy en
que el bid sube 126 puntos y el spread llega a 70** -la hora de un dato de EE. UU.-: el stop se llena
en ese tick, como manda ADR-0057 d1, a −3,58 R. El trader cerró esa operación a cero a las 12:30:00:
había subido el stop a la entrada, y eso el libro no lo documenta.

### 3.2 Sensibilidad

| riesgo | tramo | simulada | anotada |
|---|---|---|---|
| 0,625 % (spec) | abril | no concluyente | pasa (10-abr) |
| 0,625 % (spec) | agosto | no concluyente | no concluyente |
| 0,625 % (spec) | abril+agosto | no concluyente | pasa (10-abr) |
| 1 % (fuera de la spec) | abril | no concluyente | pasa (9-abr) |
| 1 % | agosto | no pasa (7-ago, diaria) | pasa (19-ago) |
| 1 % | abril+agosto | pasa (6-ago) | pasa (9-abr) |
| 2 % (fuera de la spec) | abril | no pasa (16-abr, pérdida total) | no pasa (13-abr, diaria) |
| 2 % | agosto | no pasa (7-ago, diaria) | pasa (19-ago) |
| 2 % | abril+agosto | no pasa (16-abr, total) | no pasa (13-abr, diaria) |

**Los veredictos no son monótonos con el riesgo, y hay que leerlos con eso delante.** Al subir el
riesgo, más operaciones de stop corto piden más de 100 lotes y no entran: al 2 % entran 20 de 77 en la
simulada y 15 en la anotada, así que ya no es la misma muestra. Y el lote se calcula sobre el saldo
realizado, así que el orden de ganancias y pérdidas cambia el tamaño de las siguientes.

## 4. Las diferencias entre lo simulado y lo anotado

Criterio escrito antes de mirar: una diferencia es **grande** si cambia la clase (gana, pierde o
«cero», con |R| < 0,1) o si difieren en 1 R o más. Hay **20 de 73**. Para las ocho en que una serie
gana y la otra pierde, se midió en los ticks de Dukascopy cuánto pasó el precio del stop (desplazado)
entre el llenado y el cierre anotado.

| categoría | n | operaciones (UTC) | qué dicen del bróker |
|---|---|---|---|
| **la anotada cierra a cero**: el trader subió el stop a la entrada, y eso no está documentado | 5 | 24-abr 11:30 · 29-abr 11:02 · 3-ago 12:10 · **7-ago 12:14** (el pico del dato) · 27-ago 12:13 | nada: es una regla que la simulada no tiene |
| **las dos ganan, la anotada más allá de 3 R** (4,2 a 5,1 R): el trader deja correr | 5 | 1-abr 12:30 · 13-abr 06:50 · 13-abr 10:26 · 29-abr 07:58 · 29-abr 09:36 | nada: el objetivo no es una orden fija en 3 R (ADR-0037 §7) |
| **la anotada gana y la simulada pierde, en la frontera**: Dukascopy pasa el stop por 1 a 3 puntos | 2 | 6-abr 06:34 (3 puntos) · 7-ago 05:14 (1 punto) | lo esperable con el desfase de ~2 puntos: lo **valida** |
| **la anotada gana antes del objetivo de la spec**: el trader cierra en 2,5 a 2,9 R y Dukascopy no toca el stop antes | 2 | 9-abr 07:12 · 3-ago 09:52 | la salida del trader, no el bróker; pero en 3-ago Dukascopy no llega al precio de cierre anotado por **16 puntos** |
| **una serie toca un nivel que la otra no**: OANDA llega a 3 R o al stop y Dukascopy se queda a **5 a 11 puntos** | 4 | 22-abr 08:02 (6) · 26-ago 05:49 (11) · 14-abr 12:06 (5) · 21-ago 11:56 (8) | **lo cuestiona**: no la lógica del bróker, sino **la fuente**. Los caminos de OANDA y Dukascopy se separan en minutos más que los 2 puntos del desfase medido: es A-16, abierta |
| **las dos pierden, la simulada mucho más** | 2 | 9-abr 09:15 (stop de 6 puntos, llenado 7 puntos más allá: −2,17 R) · 23-abr 05:53 (una hora sin ticks, **respaldo M1** pesimista: −3,14 R) | la primera es el llenado al tick de ADR-0057 d1; la segunda, el respaldo M1, que solo sirve para depurar (ADR-0051 §8) |

**Lo que dice en conjunto.** La lógica del bróker hace lo que sus ADR dicen: el stop al toque y al
precio del tick, el pico del dato incluido, y el respaldo pesimista donde no hay ticks. Lo que separa
las dos series son, por un lado, **reglas del trader que la simulada no tiene** -el stop a la entrada
en 5 y la salida más allá de 3 R en 5- y, por otro, **seis operaciones en que OANDA y Dukascopy
recorren caminos distintos por 5 a 16 puntos**. Esa segunda parte cuestiona que una simulación sobre
Dukascopy reproduzca operaciones de stop corto hechas sobre OANDA: con stops de 15 puntos, 5 a 16 de
diferencia deciden el desenlace.

## 5. Veredicto

| escenario | tramo | serie simulada | serie anotada |
|---|---|---|---|
| **0,5 % (spec)** | abril | no concluyente | **pasa** (13-abr) |
| **0,5 % (spec)** | agosto | **no pasa** (7-ago, pérdida diaria) | no concluyente |
| **0,5 % (spec)** | abril+agosto | **no pasa** (7-ago, pérdida diaria) | **pasa** (13-abr) |

**Con sus salidas reales**, las operaciones del trader pasan la fase 1 al riesgo de la spec: en abril
llegan al 10 % en seis días de trading, sin acercarse a ningún límite. En agosto no llegan (+7,3 %).
**Con la regla de salida de la spec sobre los ticks de Dukascopy**, no llegan nunca al objetivo, y
agosto rompe la pérdida diaria el día 7.

**Pero con la comisión que el perfil supone, la esperanza neta cruza el cero en todos los tramos de
las dos series.** Con la anterior, que abril alcanzara el objetivo es compatible con una racha buena
al principio de una muestra de 35 operaciones, y no sostiene que se repita. Lo que decide la
viabilidad no es el tamaño del riesgo sino **el coste por operación frente a la distancia del stop**:
con una mediana de 15 puntos, la comisión se lleva de media 0,86 R. Dos medidas lo aclararían: la
comisión real de FTMO (la demo, Next Action A2) y si las cajas de stop muy corto son las que el
trader operaría en una cuenta con comisión.

## 6. Error de código encontrado, y no corregido

**`evaluar_fase` (`src/botsito/engine/cuenta.py`) cuenta dos veces el resultado de cada operación
que viene del bróker.** El bróker deja en la operación cerrada una marca de precio en el **mismo
instante** que su cierre (la del tick que salta el stop o el objetivo): pasa en **73 de 73** de la
serie simulada. `_eventos` ordena, a igual instante, el cierre **antes** que la marca (`_ORDEN`:
cierre 0, marca 2), y la marca vuelve a meter la posición en `abiertas`, de donde ya no sale: la
equity vigilada lleva desde ese momento el resultado de la operación otra vez, como flotante.

**Lo que cambia.** Con el motor tal cual, la cuenta del 7 de agosto (abril+agosto, 0,5 %) cierra el
día con un saldo de 93.588 bajo un límite de 94.002 y **no marca la infracción**: la equity que
vigila no baja de 96.493, sostenida por las posiciones fantasma de días anteriores. Este informe da
las cifras **saneadas**: el script quita las marcas en o después del cierre antes de llamar a
`evaluar_fase` (`marcas_antes_del_cierre`), que no dicen nada que el cierre no diga. Con el motor tal
cual, **tres veredictos de §3 cambian de estado** -0,5 % abril+agosto simulada (en curso en vez de
no pasa), 1 % abril+agosto simulada (en curso en vez de pasa) y 2 % agosto simulada (en curso en vez
de no pasa)-, en otro cambia el día y la regla que rompe (2 % abril simulada: la diaria el 13 de
abril con el motor tal cual, la total el 16 saneado), y cambian el peor día y el peor total de casi
todas las simuladas. La serie anotada no lleva marcas y sale igual.

**A quién más toca.** A todo lo que evalúa operaciones del bróker con `evaluar_fase`: en particular
la repetición de la Fase 6 de `trabajo/ticks-llenado` (`scripts/repeticion_trader.py`,
`TICKS-LLENADO.md`), cuyos veredictos y pérdidas máximas se hicieron con el motor tal cual. La cuenta
viva del cableado (`CuentaViva`) no pasa por `_eventos`, y según su código solo marca las posiciones
abiertas (`cableado._a_la_cuenta`); no se ha comprobado con una corrida. **Se corrige en su propia rama**, con un test que falle hoy: una operación con una marca
en el instante del cierre no puede seguir abierta.

## 7. Estado

Script, test e informe en un solo commit sellado. Nada de esto se enseña al trader. **Rama lista para
revisión, NO cerrada.**
