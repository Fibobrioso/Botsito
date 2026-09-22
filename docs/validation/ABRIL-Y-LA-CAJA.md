# Abril y la caja · PRE-REGISTRO

Rama `trabajo/abril-y-la-caja`, desde `34414d5` (tag `stable/F14-cobertura`). Sin merge, sin tag,
sin push.

**Este documento se commitea ANTES de descargar abril y ANTES de abrir el xlsx.** Lo que se elige
después de ver los datos no vale, y esta rama vive de eso. Los criterios de abajo quedan
congelados; los resultados se escriben debajo, sin tocarlos.

## 0. Qué separa esta rama

Agosto midió el RR realizado con suelo en 3,00 y **no pudo elegir** entre dos lecturas que predicen
lo mismo, porque **la caja no está en el fichero**:

```
H(0,8)   base = riesgo_real     stop = 0,8 · caja   ->  RR realizado 3,00
H(1,0)   base = caja_completa   stop = 1,0 · caja   ->  RR realizado 3,00
```

En abril sí se puede poner la caja: el xlsx da entrada y stop exactos, y las velas M1 dan los altos
y bajos. Abril es material de **DESARROLLO** y se abre sin puerta, lo cual **se comprobó antes de
abrir nada**:

```
casos_reservados(repo) -> 34 casos reservados · de 2026-04: 0
   (2026-05: 13 · 2026-06: 11 · 2026-09: 10)
```

## 1. Lo que dijo el trader sobre el 0,8, traído ANTES de medir

A-10 —*«stop a 0,8: fijo o 0,75 + spread»*— está **RESUELTA**, y lo que la resuelve es un registro
del trader, no una decisión nuestra:

> **`fb-2026-09-09-sesion-01-6b07b172`** (objetivo: ambigüedad A-10)
> *«Por temas de Spread, todo SL se marca completo para el lotaje pero se reduce al 0.8 para la
> operativa como tal»*

Y el que fija el parámetro:

> **`fb-2026-09-09-sesion-01-d34a0222`** (`stop_fraccion_caja`)
> *«todo SL se marca completo para el lotaje pero se reduce al 0.8 para la operativa»*
>
> **`fb-2026-09-09-sesion-01-a9630011`**
> *«El SL siempre en 0.8 fijado con la regla de primero la caja completa»*

**Lectura, escrita antes de los recuentos: el 0,8 es FIJO.** El spread es el *motivo* de que exista
el 0,8, no un término variable que se le sume. Eso hace de **H(0,8) una predicción puntual limpia**
—`1,25 · d` = caja exacta— y no una banda.

**Pero el corpus anterior a la sesión dice otra cosa, y va escrito porque debilitaría la predicción
si mandara:**

| Item | Momento | Literal |
|---|---|---|
| `ev-v1-000448-346d6d90` | v1 0:04:48 | *«cubrir hasta un 0.75, entonces aquí perderíamos menos un 0.75»* |
| `ev-v2-003142-beb4ad3c` | v2 0:31:42 | *«al final lo suelo poner en 0.75 […] no estás arriesgando el 100% de la entrada»* |
| `ev-v5-000312-f5062062` | **v5 0:03:12** | *«si yo protejo a 0.80, que es el SL por defecto»* |
| `ev-v4-000835-782cf2cc` | v4 0:08:35 | *«darle un pequeño respiro […] de un par de pips […] de 0.75 a 0.80 o que sea fijo en 0.75»* |
| `ev-v4-001221-1e66b5fd` | v4 0:12:21 | *«que este 0.75 se desplace lo suficiente como para que esté de acuerdo al split del momento»* |

Los dos de **v4 (2026-08-30)** proponen un desplazamiento **variable con el spread**. Si eso
mandara, el multiplicador de H(0,8) no sería 1,25 sino una banda ≈1,25–1,33 —de 1,5 puntos de
ancho, comparable a la tolerancia estrecha— y la predicción dejaría de ser puntual. **Los dos son
anteriores a la sesión 1 (2026-09-09), que es la que resuelve A-10 con las palabras del trader.**
Se mide con 1,25 puntual y esta banda queda escrita: si los recuentos salen justos y los residuos
se agrupan entre 1,25 y 1,33, la banda es la explicación candidata y **no se decide con abril**
(ver §5).

**Y un hecho que conviene tener delante:** `ev-v5-000312-f5062062` es **v5 a 0:03:12**, el mismo
vídeo del que sale el fotograma que vamos a usar, a 0:04:52. La evidencia del 0,8 y la operación
que vamos a medir están **a menos de dos minutos una de otra**.

## 2. MEDIDA 1 — Réplica de la distribución del RR

No cierra A-18 por sí sola; **es réplica**.

Filas de abril con `maxTP` e `initialSL`. `RR = |maxTP − entryPrice| / |entryPrice − initialSL|`.
Región discriminante **[3,00 , 3,75)**, la misma que la predicción de mayo, **que no se toca**.

Se reporta: `n`, mínimo, máximo, moda, cuántas dentro de la región, cuántas ≥ 3,75, y **cuántas
ganadoras por debajo de 3R** —el 2,50 de agosto contradecía v6 0:17:07; se mira si abril tiene más
como ella, y **se nombra sin concluir**.

## 3. MEDIDA 2 — La caja, que es la que sí discrimina

Para cada operación con `initialSL`: **`d = |entryPrice − initialSL|`**.

En el sentido del stop (SELL → arriba, se busca un ALTO; BUY → abajo, se busca un BAJO):

```
nivel1 bajo H(1,0)  =  entrada ± 1,00 · d      (el stop mismo)
nivel1 bajo H(0,8)  =  entrada ± 1,25 · d
SEÑUELOS de control =  0,90 · d  ·  1,10 · d  ·  1,40 · d
CONTROL DEL ANCLA   =  entryPrice, contra los MISMOS fractales y las MISMAS tolerancias
```

- **ALTO/BAJO ESTRUCTURAL**, fijado ahora: vela M1 cuyo `high` (`low`) es **estrictamente** mayor
  (menor) que el de las **5** velas a cada lado.
- **VENTANA DE BÚSQUEDA**, fijada ahora: las **120** velas M1 anteriores al `dateStart` de la
  operación, incluida la suya. `dateStart` viene en **UTC** (`ingesta.py`).
- **TOLERANCIAS**, fijadas ahora, y se reportan las dos: **±0,00002** y **±0,00005**.

### El criterio, y no se toca después

Se **DECIDE** sólo si una de `{1,00 ; 1,25}` acierta en **la mitad o más** de las operaciones **a la
tolerancia estrecha** **Y** al menos el **doble** que el mejor de los tres señuelos. Si empatan, o
si ninguna supera a los señuelos, es **NO CONCLUYENTE y se escribe así**. No se busca un tercer
multiplicador para salvar la medida.

### ±0,00005 es DESCRIPTIVA

> **A esta tolerancia el test no discrimina: el azar da ~16 de 38 y el umbral quedaría en 38.
> Ningún recuento a ±0,00005 se puede citar como apoyo de ninguna de las dos hipótesis, ni aquí ni
> en ninguna rama posterior.**

Medido antes de escribirlo, sobre velas M1 ya descargadas de mayo (leer velas no es abrir,
ADR-0021 §1), 58 ventanas de 120:

```
altos estructurales por ventana:  min 2 · mediana 6 · max 9 · ventanas con CERO: 0
bajos estructurales por ventana:  min 3 · mediana 5 · max 9 · ventanas con CERO: 0
rango de precio de la ventana:    mediana 141 puntos

p(acierto por azar) ~ n_fractales · 2·tol / rango
   ±0,00002 -> p ~ 0,170 -> un señuelo ~6,5 de 38 · MEJOR DE TRES: mediana 8, p95 12
   ±0,00005 -> p ~ 0,426 -> un señuelo ~16,2 de 38 · MEJOR DE TRES: mediana 19, p95 23
```

Los señuelos **no salen cero por construcción**: el test tiene control. La cláusula del **doble del
mejor señuelo se queda**: a la mediana es casi redundante (2×8 = 16 < 19) pero **al p95 muerde**
(2×12 = 24 > 19), que es exactamente la racha afortunada para la que se escribió.

**El control que cuenta es el de ABRIL**, medido en sus propias ventanas: si abril tiene ventanas
más anchas o más estrechas, la `p` cambia. Se reportan las dos y se dice si difieren.

### El control del ancla

Los tres señuelos controlan el **blanco**; nadie controla el **ancla**. La premisa de toda la medida
2 es *«entrada = nivel 0»*, y se comprueba al mismo coste pasando `entryPrice` por los mismos
fractales y las mismas tolerancias.

- si la entrada acierta **muy por encima del azar**, el ancla está validada y los recuentos de 1,00
  y 1,25 se leen con confianza;
- si acierta **al nivel del azar**, **no refuta** la premisa —el nivel 0 de un breaker puede ser un
  borde de cuerpo y no un alto o bajo fractal— pero **sí acota cuánto fiarse** de los recuentos.

**No es un gate que aborte: es un número que se publica con los otros y limita la lectura.**

### El residuo con signo

Se reporta, por operación y por multiplicador, **`nivel − fractal`**: moda, mediana y dispersión. Un
desfase sistemático de lado —BID/ASK— aparece como **moda desplazada**; el ruido, como distribución
ancha centrada en cero. **No añade ningún parámetro libre y los recuentos siguen decidiendo.**

> **Cláusula, escrita ahora porque es donde esto se puede torcer:** si los residuos enseñan una moda
> desplazada limpia, **eso NO decide abril**. Se convierte en una **predicción pre-registrada** para
> el mes siguiente —enero, que ya tiene xlsx y dataset, o mayo— y se comprueba allí. Una hipótesis
> nacida de mirar los residuos de abril **no se valida con los residuos de abril**. Es exactamente
> como nació la predicción de mayo.

## 4. El orden: el paso del fotograma va PRIMERO

**Se comprueba y se escribe ANTES de calcular ni un recuento de la medida 2.** Si el fotograma
cuadra con las velas BID descargadas, FX Replay dibuja BID, el desfase de lado no existe y la
tolerancia estrecha es utilizable; si no cuadra, el residuo dice cuánto y hacia dónde. **Lo que no
puede pasar es que ese resultado se conozca después de los recuentos**, porque entonces sirve para
explicar lo que haya salido.

El fotograma: v5 `0:04:52` y `0:04:53` (`data/fotogramas/v5/png-1fps/000292000.png` y
`000293000.png`), herramienta de posición sobre un **SELL** de EURUSD M1 del **miércoles 29 de abril
de 2026**, hacia las **10:03-10:08**, con riesgo constante **0,00019** y el R/R pasando de 3,21 a 3.

- **Si NO cuadran**, la medida 2 **no se ejecuta** y se escribe por qué: las velas de FX Replay no
  serían las de Dukascopy y todo el recuento estaría sobre la serie equivocada.
- **Si cuadran, se dice también**: ADR-0029 §1 fija que toda la geometría se mide sobre BID y deja
  escrito que *«lo que NO está verificado»* es que sea el lado que dibuja FX Replay; su §Impacto lo
  deja *«pendiente de verificación con el trader o con FX Replay»*. **Esta comparación es la primera
  ocasión de contestarlo, y si lo contesta es un hallazgo con nombre propio**, independiente de lo
  que diga A-18.

## 5. Qué significa cada salida, escrito ahora

**Gana 1,25** → el stop vive a 0,8 de la caja, `stop_fraccion_caja` aguanta, y el RR realizado 3,00
significa objetivo sobre **riesgo real**: **A-18 se decide hacia `riesgo_real`**. ADR-0038 + cambio
de `base_calculo_objetivo` (CONFIRMED), con los cuatro sitios de `CLAUDE.md` y
`botsito spec docs --escribir` en el mismo commit.

**Gana 1,00** → el stop vive en el borde de la caja: lo que está mal es **`stop_fraccion_caja`**
(0,8 → 1,0), también CONFIRMED, y **A-18 NO se cierra por esta vía**, porque con stop = caja las dos
lecturas coinciden y el RR no puede discriminar nunca. Se escribe así, con ADR propio.

> **Y lo que cuesta esta salida, escrito antes de medir.** Ganar 1,00 no sería sólo corregir un
> parámetro: **contradiría A-10, que está RESUELTA por un registro del trader**, no decidida por
> nosotros. Es el mismo choque que el informe de F14a nombró en su §6c —**lo que el trader dice
> sobre su regla frente a lo que la herramienta hace mientras la usa**— y se escribe dentro de ese
> marco, sin inventar uno nuevo. No cambia el criterio: **lo encarece**.

**No concluyente** → A-18 sigue abierta, **mayo sigue siendo el discriminador y su predicción sigue
intacta**. Es un resultado, no un fracaso.

## 6. Lo que NO se hace en esta rama

- **Enero de 2026 tiene xlsx en el corpus Y dataset ya descargado** (`eurusd-m1-2026-01-e37291d4`),
  y es material de desarrollo igual que abril: **es un tercer mes a coste de descarga cero** para
  replicar esto. **No se abre aquí: se nombra, y lo decide el consultor.**
- No se escribe ni un `caso-*.yaml` de abril: abril es un mes de **medida**, como agosto. La
  biblioteca de casos se construye con mayo.
- **No se declara abril en `cobertura_material`**: esa declaración la hace el consultor antes del
  sorteo, y abril no hace falta ahí porque ya está en `vistos.yaml`.
- Nada del material de septiembre. `PREREGISTRO.md` vacío. Cero autorizaciones.

---

# RESULTADOS

Los criterios de arriba **no se han tocado**. Lo que sigue es lo que dio cada uno.

## R0. El titular: la puerta del paso 3 se abrió por dos pelos, y de paso contestó a A-16

**El reloj del gráfico de FX Replay no es UTC: es UTC+2.** Lo dice el propio FX Replay en el
fotograma de v4 (`001200000.png`), abajo a la derecha: **`14:29:59 UTC+2`**. Y es un **UTC+2 fijo**,
no un huso con horario de verano: ese fotograma muestra **enero** —`Thu 29 Jan '26`— y ya marca +2.

Con ese desfase aplicado, las dos velas que las leyendas de v5 dan exactas **sí** están en las velas
de Dukascopy recién descargadas:

| Fotograma | Eje (UTC+2) | UTC | Pantalla (OANDA) O/H/L/C | Dukascopy O/H/L/C | máx \|dif\| |
|---|---|---|---|---|---|
| `000293000.png` | 10:03 | **08:03** | 116996 · 116998 · 116986 · 116988 | 116996 · 116996 · 116986 · 116986 | **2 puntos** |
| `000292000.png` | 10:04 | **08:04** | 116987 · 116994 · 116980 · 116982 | 116988 · 116993 · 116979 · 116982 | **1 punto** |

**Las series cuadran a 1 y 2 puntos (0,1 y 0,2 pips).** Por eso la medida 2 **sí** se ejecutó.

> **CORRECCIÓN, y el error fue mío.** Durante esta misma rama concluí lo contrario —«no cuadran, la
> medida 2 no se ejecuta»— con dos fallos encadenados: **supuse que el eje del gráfico era UTC** sin
> comprobarlo, y **leí `10:08` donde pone `10:04`**. Comparando UTC con UTC+2 las diferencias salían
> de 15 a 26 puntos y la conclusión parecía sólida; incluso barrí las 31.549 velas del mes buscando
> la vela exacta y no apareció, lo cual era cierto y no significaba lo que le hice significar. **Lo
> que lo destapó no fue una relectura: fue mirar un fotograma de OTRO vídeo por un motivo distinto**
> —el punto (b) de la ampliación de A-16, «leer la leyenda de la fuente»— y encontrarse el reloj.

**Y esto es la primera medida de A-16** —*«cuánto se separan las velas de Oanda de las de
Dukascopy»*, ABIERTA, `clase: medicion`, `resuelve_en: [F26]`—, que es exactamente la **tercera
fuente** que su propio texto dice que la medición del 2026-09-09 no cubría: *«queda una tercera
fuente en juego, que es la del trader […] esta medicion no la cubre»*. Da **1 y 2 puntos**,
comparable a los **2 puntos de mediana** de la pareja MT5/FundedNext. **Con n = 2 no se cierra
nada**: `estado`, `decision` y `evidencia` de A-16 **no se tocan**.

La leyenda de v5 dice además de dónde salen esas velas: **`EUR/USD · 1 · OANDA on FXReplay`**.

## R1. Medida 1 — la réplica

```
38 filas leidas   (vistos.yaml decia 38 operaciones: cuadra exactamente)
buy 18 · sell 20 · sin initialSL 3 · con stop pero sin maxTP 20

RR realizado, n = 15:
2,57  2,94  3,00  3,00  3,00  3,12  3,31  3,33  3,50  4,15  4,18  4,19  4,60  4,69  5,05

minimo 2,57 · maximo 5,05 · MODA 3,00 (tres filas)
en [3,00 , 3,75): 7 de 15   ·   >= 3,75: 6 de 15   ·   < 3,00: 2 de 15
```

**Lo que abril refuta, y lo refuta solo:** `caja_completa` predice la región **[3,00 , 3,75) VACÍA**
con suelo en 3,75. Abril tiene **7 de 15 dentro** y **la moda clavada en 3,00**, con tres filas.
**Nueve de quince** están por debajo de 3,75. Es el **segundo mes independiente** que puebla una
región que esa lectura exige vacía.

**Lo que abril NO decide, y es lo mismo que ya estaba escrito:** la alternativa a `riesgo_real`
nunca fue sólo `caja_completa`; era **`caja_completa` CON `stop_fraccion_caja` = 1,0**, que predice
suelo en 3,00 igual. Lo único que separa esas dos es la medida 2. **A-18 sigue ABIERTA.**

**Dónde los dos meses no se parecen**, y se dice sin adornarlo: el suelo de agosto era **limpio**
—17 de 18 en 3,00 o más, una sola por debajo— y el de abril **no** —2 de 15 por debajo de 3,00—.
**Coinciden en lo que refutan y difieren en la limpieza del suelo.**

### Qué es `maxTP`, fijado ANTES de usar el hallazgo

El corpus **no lo dice**: se buscó al trader explicando su exportación (`exporta`, `excel`,
`analytics`, `estadistic`, `maxTP` en las seis transcripciones crudas) y **no aparece**. Se fijó por
**consistencia interna del libro**, con dos medidas sobre abril:

```
maxTP == avgClosePrice  en las 17 filas donde existen las dos.   DISTINTOS: 0
maxTP presente  <=>  rPnL > 0   (17 de 17; las 21 sin maxTP: 19 pierden, 2 a cero)
```

**`maxTP` es el PRECIO DE CIERRE de las operaciones ganadoras**, no la excursión favorable máxima.

> **Esto corrige algo que escribí en F14a**, donde dije que `maxTP` es *«lo más lejos que llegó a
> favor»*. Era una suposición, no una medida. **La conclusión de F14a no cambia** —`maxTP` sigue
> siendo un resultado y no el objetivo planeado, y sigue estando relleno si y sólo si se ganó— pero
> el motivo estaba mal dicho, y el argumento que colgaba de él ha tenido que reescribirse (§R4).

### El hallazgo que no es de A-18: tres ganadoras por debajo de 3R

Entre los dos meses hay **tres ganadoras que cierran por debajo de 3R**: **2,50** en agosto, **2,57**
y **2,94** en abril. El informe de F14a dijo *«una fila no tumba una cita, pero se nombra»*. **Tres
filas en dos meses independientes ya no son una fila.**

Y ahora que `maxTP` está fijado, el hallazgo es **más fuerte** de lo que parecía: no son operaciones
que *no llegaron* a 3R —eso sería la lectura de la excursión— sino operaciones que **cerraron en
ganancia por debajo de 3R**. Contradice el *«sin toma de parciales y que tiene que llegar al ratio
1.3 sí o sí»* de **v6 0:17:07**, y apunta a **parciales o salidas manuales**, que sería cosa de la
spec y no de un parámetro.

**La incertidumbre que queda, delante y no detrás:** la columna se llama `avgClosePrice` —un cierre
**promedio**—. Si hubiera cierres parciales, ese promedio los mezclaría, lo cual es *coherente* con
la hipótesis de los parciales pero **no la prueba**: «avg» puede ser sólo el nombre del campo. No se
decide aquí.

## R2. Medida 2 — NO CONCLUYENTE

Se ejecutó con los criterios pre-registrados, sin tocar un parámetro.

```
operaciones usadas: 35 de 38   ·   sin ventana suficiente: 0
fractales por ventana (ABRIL): mediana 11 · min 6 · max 14      (mayo daba 6 y 5)
rango de ventana (ABRIL): mediana 128 puntos                     (mayo daba 141)

multiplicador        ±2 pts    ±5 pts    residuo mediana / min / max
1,00  (H 1,0)         4/35      10/35        +4 / -54 / +54
1,25  (H 0,8)         3/35       8/35         0 / -57 / +57
0,90 (señuelo)        4/35      12/35        +3 / -52 / +52
1,10 (señuelo)        4/35       9/35         0 / -55 / +55
1,40 (señuelo)        5/35       9/35        +1 / -59 / +59
ANCLA (entrada)       7/35      17/35        -1 / -40 / +41

umbral del criterio: max(mitad = 17,5 · doble del mejor señuelo = 10) = 17,5
   1,00 -> 4 aciertos. NO CUMPLE
   1,25 -> 3 aciertos. NO CUMPLE
```

**NO CONCLUYENTE, y no por poco: por mucho.** Ninguno de los dos multiplicadores llega al umbral, y
lo que es más informativo, **ninguno se distingue de los señuelos** —4 y 3 frente a 4, 4 y 5—.

**Lo que esto dice, y no es «no salió»:** los niveles derivados de `d` **no caen sobre fractales más
que el azar**. O el nivel 1 de la caja del trader **no es un alto/bajo estructural de M1**, o no lo
es con *este* fractal (5 velas a cada lado) y *esta* ventana (120 velas). La premisa geométrica de
la medida, y no las hipótesis sobre A-18, es lo que este resultado pone en duda.

**El control del ancla lo refuerza:** `entryPrice` acierta **7/35 a ±2 y 17/35 a ±5**, por encima de
todos los demás niveles. La **entrada** sí tiende a caer en estructura; los niveles a `1,00·d` y
`1,25·d` **no**. Eso acota cuánto fiarse: el ancla no está roto, lo que falla es el blanco.

**Los residuos no enseñan moda desplazada**: medianas entre −1 y +4 puntos y rangos de ±50-59. **No
hay desfase sistemático de lado**, lo cual es coherente con que las series cuadren a 1-2 puntos
(§R0). Así que **no nace ninguna predicción pre-registrada** de aquí.

**El control es de abril y no de mayo, como estaba exigido**: abril tiene **11** fractales por
ventana frente a los 6+5 de mayo y ventanas algo más estrechas (128 frente a 141 puntos), así que la
probabilidad por azar en abril es **mayor** que la estimada. El test era, si acaso, más fácil de
pasar de lo previsto, y aun así no se pasó.

## R3. El universo en cero, y de quién es la culpa

```
CON cobertura (hoy, tras la rama de ayer):        UNIVERSO = 0 casos · 145 excluidos
SIN cobertura (main ANTES de ayer):               UNIVERSO = 22 casos, TODOS de 2026-06
```

**La guardia que escribí ayer es la que llevó el universo a cero**, y hay que mirarla de frente.

**Por qué se excluye junio, con las citas:** ADR-0025 §1 dice *«Los 21 de junio salen: el trader se
comprometió a dos meses y entregó uno, así que para junio **no hay ninguna decisión suya con la que
comparar**»*, y §4 añade que rescatar sus `dev` *«exigiría pedirle un backtest de junio que ya no va
a llegar»*. **Ese motivo es del camino de FIDELIDAD**: sin su backtest no hay con qué *comparar*.

**Pero un paquete CIEGO no compara: hace etiquetar.** El trader recibe gráficos de días que no ha
visto y los etiqueta en sesión; la etiqueta **es** el dato (`LABEL_CASE`). Junio **no está en
`vistos.yaml`** —y es correcto que no esté: no lo ha visto—, así que sus 22 días **son ciegos y
etiquetables**. El criterio que apliqué ayer, *«no hay material del trader»*, es el de la
comparación, y lo puse donde se decide **qué se puede etiquetar**.

**Es el patrón 2 de la lista de tres** —una regla más estricta de lo que el ADR sostiene— y en el
informe de ayer escribí que lo había comprobado y que no aplicaba. **Esa comprobación fue mía y fue
errónea.** No lo arreglo aquí: no toca a esta rama y la decisión de qué es un paquete ciego es del
consultor.

**Y el hecho, se decida como se decida:** con la guardia puesta, **hoy no hay ni un día ciego**. Un
`kit build` nuevo falla con `universo tiene 0` y **falla correctamente**. **La sesión 2 no se puede
construir hasta que entre material nuevo** —o hasta que junio vuelva.

## R4. Lo que se corrige en otros documentos

- **`F14A-INGESTA.md` y ADR-0037**: `maxTP` no es la excursión favorable máxima sino el precio de
  cierre de las ganadoras. El argumento *«una orden límite habría cerrado ahí y el recorrido máximo
  no podría superarlo»* colgaba de la lectura vieja y se reescribe.
- **`F14A-INGESTA.md`**: decía *«15 de 18 se pasan de 3,00»* donde ADR-0037 ya estaba corregido a
  **14**. Quedó descuadrado al corregir sólo uno de los dos.
- **`F14A-INGESTA.md`**: la predicción congelada de mayo gana un **recuadro de anotación** —no se
  reescribe— que dice qué decide de verdad la región poblada.

## R5. Deuda que esta rama deja

- **La serie del trader es OANDA y la nuestra es Dukascopy**, y toda medida geométrica contra su
  material depende de eso (**A-16**, `resuelve_en: [F26]`). Hoy tiene su primera medida —1 y 2
  puntos, n=2— y **el método para ampliarla ya no es el que estaba escrito**: hay que aplicar el
  **UTC+2** del gráfico antes de comparar nada. Barrer los 367 fotogramas de v5 exige OCR y este
  repositorio no tiene Pillow a propósito; la vía realista es **pedirle al trader una exportación de
  velas de FX Replay**, o leer a mano una muestra.
- **El reloj de FX Replay es UTC+2 FIJO**, también en enero. No es Europe/Madrid, que en enero es
  UTC+1. Toca A-9 (anclaje H4) y no se decide aquí.
- **El fractal 5/120 no captura lo que el trader llama estructura** (§R2): cualquier medida futura
  que quiera poner la caja sobre las velas necesita otra definición, y esta rama no la busca.

## R6. La peticion al trader: son DOS cosas, y Next Action 1 las mezclaba

| Necesidad | Que hace falta del trader | Cita |
|---|---|---|
| **Sesion 2 ciega** (kit) | solo una **CONFIRMACION por escrito** de que no ha operado ni backtesteado ese mes; las velas las bajamos nosotros | `vistos.yaml`: *«antes de cada sesion el trader confirma por escrito que no ha operado ni backtesteado los meses del paquete […] se registra en F09 como CONFIRM sobre el objetivo `paquete <sesion>`»* |
| **Llenar `fidelidad-2` y `fidelidad-3`** (F26) | un **BACKTEST suyo** de un mes que no haya visto, para tener decisiones con las que comparar | ADR-0036 es el camino para material **ya visto**; Next Action: *«un mes limpio es LO UNICO que puede llenarlas con una cifra defendible»* |

**Y son INCOMPATIBLES sobre el mismo mes:** si backtestea febrero, febrero deja de ser ciego y pasa
a ser material del camino de fidelidad. **Si se quieren las dos cosas, hacen falta DOS meses.**

### El texto literal, para que Aleks lo mande

> Hola. Dos cosas, y son distintas.
>
> **1) Confirmame por escrito, si puedes:** ¿has operado o backtesteado **febrero de 2026** o
> **marzo de 2026**? Me vale un si o un no por cada uno. No necesito que hagas nada con esos meses:
> solo saber si los has mirado.
>
> **2) Y esto si es trabajo, cuando puedas:** necesito **un mes entero backtesteado que no hayas
> visto antes** — el que me confirmes limpio en el punto 1. Exportado como los otros, con el Excel
> de FX Replay. Es lo unico que nos permite medir de verdad si el bot decide como tu, porque los
> meses que ya conoces no sirven para eso: ya sabes lo que paso.
>
> Lo primero me desbloquea la siguiente sesion contigo. Lo segundo no corre prisa esta semana, pero
> sin ello hay una parte de la validacion que no se puede cerrar nunca.

## R7. Que debe decidir el usuario

1. **Validar la rama** y, si procede, el ritual. No hay ADR: **no se decide nada**.
2. **Junio (§R3)**: si vuelve al universo ciego, o si la guardia de ayer se queda como esta. De eso
   depende si la sesion 2 se puede construir sin material nuevo.
3. **A-16**: si se amplia, y por que via —OCR sobre los fotogramas, que exige una dependencia que
   este repositorio no tiene a proposito, o pedirle al trader una exportacion de velas—.
4. **El hallazgo de los parciales (§R1)**: tres ganadoras por debajo de 3R en dos meses
   independientes. Si abre ambiguedad, si va a la sesion 2, o si espera a mayo para tener un tercer
   mes.
5. **Enero**: tercer mes de desarrollo a coste de descarga cero, con xlsx y dataset ya presentes.

## Estado
WAITING_FOR_USER_VALIDATION
