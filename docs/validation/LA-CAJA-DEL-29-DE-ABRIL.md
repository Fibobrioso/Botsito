# La caja del 29 de abril

Rama `trabajo/la-caja-del-29-de-abril`, desde `569ce2c` (tag `stable/F14-abril`). Sin merge, sin
tag, sin push.

Anoche la medida 2 salió **nula** y se sabe por qué: con fractal 5 y ventana 120 ningún nivel
derivado de la operación cae sobre un fractal por encima del azar, la entrada incluida. Eso **no
dice que la caja no esté**: dice que **nuestra definición de estructura no es la del trader**. Esta
rama **no reajusta el fractal** —eso sería elegir el instrumento después de ver los datos—: le
pregunta al material **qué son sus niveles**.

## 1. La revisión de diseño, y las tres midiendo

### (a) La operación del fotograma NO está en el xlsx

> **CORREGIDO DENTRO DE ESTA MISMA RAMA, ver §R3.** Esto es cierto del instante `0:04:52`
> —riesgo 0,00019— pero **falso del instante que la transcripción localiza**, `0:03:36`, que
> está parado en una operación **sí registrada**. Se deja el apartado como se escribió, con el
> puntero: es lo que se creía al empezar, y la corrección tiene más valor con el error delante.

```
operaciones del 2026-04-29 en el libro de abril: 4, todas SELL
  07:55 UTC (eje 09:55)  entrada 1.17064  stop 1.17079  d = 0.00015
  07:58 UTC (eje 09:58)  entrada 1.17064  stop 1.17079  d = 0.00015
  09:36 UTC (eje 11:36)  entrada 1.17031  stop 1.17042  d = 0.00011
  11:02 UTC (eje 13:02)  entrada 1.17066  stop 1.17091  d = 0.00025

SELL con d = 0,00019 (el riesgo que se lee en pantalla): NINGUNA
```

Y el nivel tampoco: el fotograma está en **~1.1699**, unos **70 puntos por debajo** de la entrada
de las dos operaciones más cercanas en el tiempo.

**El fotograma es una DEMOSTRACIÓN, no una operación registrada.** Coherente con lo que dice el
audio en `0:03:34`: *«es que le he dado buy creo, espera, sell»*.

**Y eso corta en los dos sentidos, que es lo que hay que decir entero:**

- **Para (a), resta**: no se puede atar el fotograma a precios exactos del xlsx, y la forma que el
  brief había diseñado para (ii) —comparar la caja de pantalla contra `d` del libro— **no tiene
  suelo**.
- **Para (ii), SUMA**: en una demostración **está enseñando la regla a propósito**. Para la pregunta
  *«cuál es su regla»*, una demostración deliberada es **mejor material** que una operación suelta.

### (b) y (6) El control del reloj: la vía de las velas de enero NO sirve, medido

El fotograma de v4 que se abrió (`004800000.png` es otro; el del gráfico es `001200000.png`,
v4 `0:20:00`) **no tiene leyenda OHLC legible** —la tapa la barra del replay— y la lectura del eje
de precios desde la imagen es demasiado gruesa:

```
ventana de 255 velas del 2026-01-29 que mejor encaja con el rango leido (~1.19520 .. ~1.19840):
   00:00-04:14 UTC  rango 1.19532..1.19906   error 78 puntos
```

Un error de **78 puntos** y una ventana que empezaría a las 00:00 UTC —es decir, un desfase de
+6:15, que no es ningún huso—. **Eso es ruido, no señal: esta vía no sirve.**

**La evidencia primaria del UTC+2 no es el ajuste de velas: es LA ETIQUETA que el propio gráfico
muestra**, en un vídeo de **enero**, y un gráfico que dice UTC+2 en enero **no es Europe/Madrid**,
porque Madrid en invierno es UTC+1. El reloj queda sostenido por **la etiqueta** más **el ajuste de
abril a 1-2 puntos** (rama anterior). El ajuste en enero pasa a ser **confirmación opcional**, y sólo
se hace si la transcripción de v4 pone delante un gráfico limpio.

### (c) La transcripción SÍ localiza los momentos, y es la vía única

Barrida la cruda de v5 (99 segmentos) con los términos `nivel`, `caja`, `cuadro`, `gan`, `protejo`,
`stop`, `SL`, `0.8`, `0.80`, `0.75`, `objetivo`, `RR`, `ratio`, `1.3`, `marco`, `trazo`, `trazar`,
`mido`, `medir`, `mapeo`:

| Instante | Lo que dice |
|---|---|
| `0:01:46` | *«al hacer mapeo estructural […] cuando hago mapeo la estructura pues me quedaría algo así»* |
| `0:02:33` | *«no llega a romper ese nivel aquí»* |
| **`0:03:21`** | ***«Y si yo protejo a 0.80»*** |
| `0:03:29` | *«SL por defecto»* |
| **`0:03:34`** | ***«protejo aquí»*** —el gesto de colocar el stop, y lo narra |
| `0:04:44` | *«el cálculo del RR en base al 1%»* |
| `0:04:58` | *«estaba buscando el 1.3»* |

**`0:03:21`-`0:03:40` es el tramo que decide**: dice el número **y** hace el gesto. Más el vecindario
`0:04:40`-`0:05:00`, que la evidencia ya cita.

## 2. PRE-REGISTRO de la medida (ii), escrito ANTES de abrir ningún fotograma

La forma es nueva y **mejor que la que el brief diseñó**: se lee **dentro de la misma imagen** dónde
cae la línea de stop respecto de las etiquetas `0 / 0,25 / 0,5 / 0,8 / 1` **que dibuja el trader**.
No necesita el xlsx, no necesita calibrar píxeles, **y los números son suyos y no nuestros**.

**Qué se va a leer exactamente:**

1. **Sobre qué etiqueta cae la línea de stop** de la herramienta de posición.
2. **En qué extremo de la caja está la entrada**: el `0` o el `1`. **No se supone: se lee.**

**Qué significa cada salida, escrito ahora:**

- **Stop sobre `0,8`** → `stop_fraccion_caja` = 0,8 **confirmado por su propia plantilla**, y
  entonces el RR realizado de **3,00 medido en dos meses** significa objetivo sobre **riesgo real**:
  **A-18 se inclina a `riesgo_real`**. **No se cierra con esto solo** —n = 1 y es una demostración—
  pero **se dice que el peso cambia**.
- **Stop sobre `1`** → `stop_fraccion_caja` = 1,0, y eso **contradice A-10**, que está **RESUELTA por
  un registro del trader**, no decidida por nosotros. Es el choque de `F14A-INGESTA.md` §6c y se
  escribe **ahí dentro**.
- **Stop en ningún sitio claro, o etiquetas ilegibles** → **NO CONCLUYENTE**, y se escribe así.

**Y una cosa que la imagen ya dice y que no habíamos tenido nunca:** su herramienta está configurada
con **`0,8` como nivel marcado**. Que ese número exista en su plantilla es evidencia **por sí sola**
de que **la caja y el 0,8 se dibujan juntos**.

**n será 1 o 2. NO DECIDE A-18, y se escribe así de claro.** Lo que produce es la **primera
descripción medida de cómo el trader elige sus niveles**.

## 3. SEGUNDO PRE-REGISTRO: el rodeo del cociente, escrito ANTES de reabrir los fotogramas

La medida 2 se quedó en NO CONCLUYENTE (§R2) **por una vía muerta, no por el material**: la escala
de precios de la imagen no se puede fijar. **Hay rodeo, y no cambia el criterio pre-registrado**
—sigue siendo *«sobre qué etiqueta cae el stop»*— **sino sólo el instrumento**:

```
fraccion_del_stop  =  (pixeles de entrada a stop)  /  (pixeles del 0 al 1 de la caja)
```

**La escala de precios NO interviene: aparece en los dos términos y se cancela.** Con las medidas ya
tomadas —`0` en `y=424`, `1` en `y=237`, alto **187 px**— el `0,8` está en `y=274`, a **37 px** del
`1`, y **un píxel vale 0,005 de caja**.

**TOLERANCIA, fijada ahora:** la fracción medida tiene que caer **a menos de 0,03** de una de las
**cinco** etiquetas de su plantilla (`0 · 0,25 · 0,5 · 0,8 · 1`). Si cae a menos de 0,03 de **dos**,
o de **ninguna**, es **NO CONCLUYENTE y se escribe así. No se ensancha después.**

### La comprobación que puede tumbar la lectura, y va ANTES de concluir

En `000292000.png` la herramienta imprime **«Risk/Reward Ratio: 3.21»** y **«Target: 0.00061
(0.052%) 6.1»**. Entonces:

```
alto de la zona de BENEFICIO (px)  /  alto de la zona de RIESGO (px)  =  3,21
```

Se miden las dos alturas y se comprueba. **Si no da 3,21, lo identificado como stop no es el stop y
se para ahí.** Es la misma disciplina que el señuelo: una comprobación que puede tumbar la lectura
antes de que la lectura signifique algo.

### Y la comprobación de ANCLA COMÚN, sin la cual el cociente no significa nada

La **arista de ENTRADA de la herramienta de posición** —la frontera entre la zona roja y la verde—
tiene que **coincidir en `y`** con el **nivel 0 de la caja**. Lo medido en §R2 fue que la *línea de
precio actual* está a dos píxeles del nivel 0, y **eso es la línea de precio, no la entrada de la
herramienta**: son cosas distintas y hay que medir la segunda. **Si no coinciden, la comparación es
inválida, y ésa es la respuesta honesta.**

Además, en los dos fotogramas hay **DOS grupos de etiquetas** `1/0,8/0,5/0,25/0`, uno sobre las
velas y otro desplazado a la derecha. **Se dirá cuál se midió y si son el mismo objeto o dos
dibujos.** Si son dos, el que vale es **el que comparte ancla con la herramienta**.

## 4. TERCER PRE-REGISTRO: el error de lectura baja a ±1 px

Escrito y commiteado **antes de medir nada**. **El criterio NO se toca** —sigue siendo *«sobre qué
etiqueta cae el stop»*, tolerancia **0,03**, las cinco etiquetas de su plantilla—. Lo único que
cambia es **el error de lectura**, y eso es **mejorar el instrumento, no elegir el resultado**: el
mismo caso que el rodeo del cociente, y se justifica igual.

- La lectura pasa de **estimación a ojo (±3 px)** a **detección programática (±1 px)**. El ±1 px se
  justifica porque **una línea dibujada ocupa una o dos filas exactas de píxeles** y la ambigüedad
  es **cuál de las dos**.
- Con ±1 px: caja de **80 px → ±0,0125**, **DENTRO** de 0,03. **La condición «caja ≥ 100 px» queda
  SIN EFECTO**, y se dice por qué: **era una consecuencia del ±3 px, no del material**.
- **CRITERIO DE ANCLA, numérico y fijado ahora:**
  `|y(nivel 0 de la caja) − y(arista de entrada de la herramienta)| ≤ 2 px`.
  Si lo supera, **no comparten ancla**, la comparación es **inválida** y se escribe así. **Diez
  píxeles no se explican como error de lectura cuando el error es uno.**
- **COMPROBACIÓN DEL 3,21, ahora afilada:** `alto(zona teal) / alto(zona roja) = 3,21`. Con ±1 px en
  cada borde el margen baja de ~±10 % a **~±3 %**. **Si no da 3,21 dentro de ese margen, lo
  identificado como stop no es el stop y se para ahí.**

**El instrumento**: un decodificador PNG de biblioteca estándar —firma, chunks, IHDR, IDAT +
`zlib`, y deshacer los filtros por línea incluido Paeth—. **`pyproject.toml` no se toca**: no es una
dependencia del paquete, es una **herramienta de medida** de la rama.

---

# RESULTADOS

Los criterios de arriba no se han tocado.

## R1. La caja del trader, vista: su plantilla LLEVA el 0,8

Fotogramas abiertos, **los dos por instante localizado** (ADR-0038): `000216000.png` (v5 `0:03:36`,
*«protejo aquí»*) y `000225000.png` (v5 `0:03:45`, el mismo tramo, con las velas ocultas y la caja
limpia).

**La caja está dibujada y sus cinco niveles son legibles.** En `000225000.png`, de arriba abajo:
`1` · `0.8` · `0.5` · `0.25` · `0`, cada uno con su color —el `0,8` en **azul**, el `0,5` en verde,
el `0,25` en naranja— y repetidos en los dos bordes del rectángulo. Las proporciones cuadran con las
etiquetas dentro de un píxel:

```
0 en y=424 · 1 en y=237  ->  alto 187 px
   0,25 esperado y=377,3   ·  leido 377
   0,50 esperado y=330,5   ·  leido 331
   0,80 esperado y=274,4   ·  leido 274
```

**Eso es el hallazgo, y es nuevo: el `0,8` no es una inferencia nuestra. Está en su plantilla de
dibujo, con línea propia, y lo dibuja a la vez que la caja.** Hasta hoy el 0,8 venía sólo de lo que
él **dice** —A-10, resuelta por un registro suyo— y de lo que la spec escribe. Ahora se ve.

## R2. Lo pre-registrado: media respuesta, y la otra media NO CONCLUYENTE

**«En qué extremo de la caja está la entrada»: en el `0`.** En `000216000.png` la línea discontinua
del precio actual cae en `y≈422` y el nivel `0` de la caja en `y≈424` —dos píxeles, con una escala
del orden de 10 px por punto—. **El nivel 0 es la entrada**, y la caja se dibuja **desde** ella.

**«Sobre qué etiqueta cae la línea de stop»: NO CONCLUYENTE, y el motivo es honesto.** No consigo
fijar la escala de precios de la imagen con precisión suficiente: distintos pares de referencias que
creo leer dan escalas incompatibles —de 1,5 a 16 px por punto— y con esa dispersión **cualquier
lectura del stop sería inventada**. Las etiquetas son legibles; la **escala** no. Sin ella no se
puede decir si el stop cae en `0,8` o en `1`, que es justo lo que decide.

**Así que A-18 no se mueve por esta vía**, tal como el pre-registro contemplaba.

**Y lo que sí queda atado, que no es poco:** la operación es **real y está en el xlsx**. El replay
está parado en la vela de **07:55 UTC**, y esa es la primera de las cuatro del día:

```
07:55 UTC  sell  entrada 1.17064  stop 1.17079  d = 15 pt  ->  PERDIO (cierre 1.17079, rPnL -15)
07:58 UTC  sell  entrada 1.17064  stop 1.17079  d = 15 pt  ->  GANO   (cierre 1.16995, RR 4,60)
```

Las dos son **la misma entrada y el mismo stop**: es la **reentrada** que él narra en ese momento
—*«nos mitiga y nuevamente, pues, sería cuestión de poner otra reentrada aquí»*—. **La demostración
del fotograma es la operación del xlsx**, no un dibujo suelto.

Y lo que implicaría cada lectura, escrito aunque no se pueda elegir entre ellas:

```
stop en 0,8 de la caja  ->  caja = 15/0,8 = 18,75 pt  ·  nivel 1 = 1,170828
stop en 1,0 de la caja  ->  caja = 15 pt              ·  nivel 1 = 1,17079
```

## R3. Corrección a (a): el fotograma SÍ está en el xlsx, y me equivoqué al decir que no

En §1(a) escribí que la operación del fotograma **no** está en el libro, porque el riesgo que se lee
en `0:04:52` es **0,00019** y ninguna de las cuatro del día lo tiene. Eso sigue siendo cierto **para
ese instante**. Pero el instante que la transcripción localiza —`0:03:36`, *«protejo aquí»*— está
parado en **07:55 UTC**, que **sí** es una operación registrada, con `d = 15`.

**Son dos momentos distintos del mismo vídeo y los confundí en uno.** El de `0:04:52` es él
arrastrando el objetivo con la herramienta —un gesto de enseñanza, riesgo 19— y el de `0:03:36` es
la operación real. **La lección se repite: localizar el instante antes de interpretarlo**, que es lo
que ADR-0038 acaba de hacer obligatorio por otro motivo.

## R4. El reloj: TERCERA confirmación, y a 1 punto

La leyenda de `000216000.png` da otra vela exacta: `O 1.17071 H 1.17072 L 1.17064 C 1.17072`, con el
eje en `Wed 29 Apr '26`. El minuto más parecido de todo el día en Dukascopy:

```
07:55 UTC  ->  1 punto de diferencia   (eje UTC+2: 09:55)
07:35 UTC  ->  3 puntos
04:35 UTC  ->  4 puntos
```

**UTC+2 otra vez, y a 1 punto.** A-16 pasa de n=2 a **n=3**, las tres entre 1 y 2 puntos. **Sigue
ABIERTA**: `estado`, `decision` y `evidencia` sin tocar.

## R5. A-33, abierta

`clase: pregunta`, `resuelve_en: [F20, F24, F26]`, `parametros: [parciales, objetivo_rr]`, en
`ambiguedades.yaml` y en la tabla Known Ambiguities, con `botsito spec docs --escribir` en el mismo
commit. **33 ambigüedades registradas.**

Lleva las tres ganadoras que **cierran** por debajo de 3R —2,50 en agosto; 2,57 y 2,94 en abril, en
dos meses independientes—, la corrección de que `maxTP` es el precio de cierre y no la excursión
máxima, y la cita de v6 `0:17:07` copiada de la cruda.

> **No hay item de evidencia de v6 `0:17:07`.** La cita vive en el texto de la `pregunta`, y la
> `evidencia` cita los items **reales** que hay sobre parciales. Estuve a punto de escribir un id
> inventado —`ev-v6-001707-9f2b6e31`— y la comprobación lo paró. Es exactamente lo que la guardia
> existe para impedir, y queda dicho porque el error llegó a estar escrito.

## R7. El rodeo del cociente: NO CONCLUYENTE, y ahora con motivo exacto

**El cociente cancela la escala de precios, como estaba previsto. Lo que NO cancela es la precisión
de lectura**, y ése es el muro.

**Todas mis coordenadas son estimaciones a ojo sobre la imagen renderizada.** No hay extracción
programática de píxeles: este repositorio no tiene Pillow, a propósito. Con un error realista de
**±3 px**:

```
caja de 187 px (fotogramas 216/225):  1 px = 0,0053 de caja · ±3 px = ±0,016  ->  DENTRO de 0,03
caja de  80 px (fotograma 292):       1 px = 0,0125 de caja · ±3 px = ±0,038  ->  FUERA de 0,03

altura minima de caja para que ±3 px quepa en la tolerancia: 100 px
```

### Y el problema es que las dos condiciones nunca coinciden en los fotogramas abiertos

| Fotograma | Caja | Herramienta de posición | ¿Sirve? |
|---|---|---|---|
| `000216000.png`, `000225000.png` | **187 px** ✓ | en **ERROR** —*«Order Error: Stop Loss price must be lower than current price»*—, sin zonas roja/verde válidas | **no**: no hay stop que localizar |
| `000292000.png`, `000293000.png` | **~80 px** ✗ | válida, con sus tooltips | **no**: la caja no da resolución |

**Hace falta un fotograma con la caja ≥ 100 px Y la herramienta en estado válido. Ninguno de los
cuatro abiertos lo cumple.**

### La comprobación de ancla común: tampoco se sostiene

En `000292000.png`, leído a ojo: el **nivel 0** de la caja está en `y≈165` y la **arista de entrada**
de la herramienta —frontera roja/verde, con sus manijas— en `y≈155`. **Diez píxeles**, que sobre una
caja de 80 px son **0,125 de caja**: muy por encima de la tolerancia.

**O no comparten ancla, o mi lectura no da para distinguirlo. En los dos casos la comparación es
inválida**, que es exactamente la respuesta honesta que el pre-registro anticipaba.

### La comprobación que podía tumbar la lectura: consistente, pero con error inútil

Zona verde ≈ 215 px, zona roja ≈ 70 px → cociente **≈ 3,07** frente al **3,21** que la herramienta
imprime. **Consistente dentro de mi error**, pero ese error es de ~±10 %, y con él no se valida nada
a 0,03. **No tumba la lectura; tampoco la sostiene.**

### Los dos grupos de etiquetas: son el mismo objeto

En `000292000.png` las etiquetas aparecen a `x≈885` y a `x≈1043`, y en `000225000.png` a `x≈690` y
`x≈1040`. **Son los dos bordes del mismo rectángulo**, no dos dibujos: en `000225000.png` los dos
grupos están a la misma altura `y` exacta para cada nivel. **No hay ambigüedad de qué objeto se
midió.**

### Conclusión, con el criterio sin tocar

**NO CONCLUYENTE.** La fracción del stop no se puede medir a ±0,03 con los fotogramas abiertos.
**No se ensancha la tolerancia** y **no se cambia el criterio**: lo que se escribe es **qué haría
falta**, que es lo que esta medida deja de herencia.

> **Lo que el rodeo SÍ consiguió**, y no es poco: convertir *«no se puede fijar la escala»* —un muro
> sin salida— en *«hace falta un fotograma con la caja ≥ 100 px y la herramienta válida»*, que es
> una **condición comprobable** sobre un conjunto finito. La transcripción de v5 localiza siete
> instantes (§1c) y sólo se han abierto cuatro fotogramas de dos de ellos.

## R8. El id inventado: la guardia, medida

`ev-v6-001707-9f2b6e31` llegó a estar escrito en `ambiguedades.yaml` y lo paró una comprobación.
**Cuál, y con qué cobertura:**

- La guardia es `cases/ambiguedades.py:170` —*«cada evidencia citada existe»*— más su gemela de
  `cases/paquete.py:1150`, y corre dentro de `knowledge validate`.
- **Corre sobre `knowledge/**`. NO corre sobre `docs/**`.** Ningún test recorre los documentos
  buscando ids citados: `test_documentos_vivos.py` sólo vigila **recuentos** en `PROJECT_STATE` y
  en los README.

**Medido sobre el repositorio, no supuesto:**

```
ids ev-* citados en docs/**:  104
de esos, INEXISTENTES:          3
   ev-v4-003710-f32c06e4  ·  AUDITORIA-2026-09-13-ultracode.md
   ev-v4-003710-f610cc8f  ·  AUDITORIA-2026-09-13-ultracode.md
   ev-v6-001707-9f2b6e31  ·  LA-CAJA-DEL-29-DE-ABRIL.md  (este informe, nombrándolo como el id que
                             estuve a punto de inventar)
```

**Ninguno de los tres es una fabricación haciéndose pasar por evidencia:** los dos de la auditoría
son **salida pegada de un `botsito evidence new` ejecutado sobre una copia**, y el tercero es este
informe citando el error. **Pero eso es suerte, no diseño: nada habría parado una fabricación de
verdad en un documento.**

Es el mismo agujero, con el mismo nombre, que el punto ciego de `comprobar_citas_revocadas` que ya
está en Technical Debt: **una guardia que enumera los sitios que vigila en vez de nombrar la
condición** —el patrón 3—. **No se arregla aquí**, y queda anotado con su disparador.

## R10. La medida con ±1 px: el 3,21 PASA, el ancla NO, y sigue NO CONCLUYENTE

**El instrumento**: decodificador PNG de biblioteca estándar —firma, chunks, IHDR, `IDAT` + `zlib`,
y deshacer los filtros por línea incluido Paeth—, en la carpeta de trabajo de la rama.
**`pyproject.toml` no se tocó.** Devuelve `1280x720, 3 canales`.

> **Dónde vive, y por qué no en el repositorio.** Se queda como **script de la rama**, en la
> carpeta de trabajo. Meterlo dentro abriría un **directorio nuevo de primer nivel**, y eso lo
> vigila `tests/unit/test_tree.py`: sería un cambio de estructura del repositorio, que es una
> decisión de otro tamaño que la de medir unos píxeles. **Si vuelve a hacer falta, entra con su
> sitio y su test, no de rebote.** Lo que no vale —y no se ha hecho— es volver a medir a ojo.

### Mi medida, independiente, y dónde difiere de la tuya

Localizada por color sobre el fotograma **entero**, no sobre una banda elegida a mano:

| | medida del consultor | mi medida |
|---|---|---|
| zona roja | `y≈79..153` | `y 82..152` en `x=1050`, interrumpida por superposiciones |
| arista de entrada | `y=154-155` | `y≈153..155` |
| teal empieza | `y≈156` | `y≈155-157`, y acaba en **`y=384`** |
| línea azul A | `y=98-99` | `y=98-99`, **`x 880..1057`** |
| línea azul B | `y=108-109` | `y=108-109`, **`x 475..941`** |
| línea verde | `y=118-119` | `y=118-119`, **`x 880..991`** |
| barra flotante | `y≈121-145` | `y≈120..145` |

**Coincidimos en todos los bordes dentro de 1-3 px.** Lo que añado es **la extensión en `x`**, y es
lo que resuelve tu pregunta.

### Las dos azules: son TRES, y ninguna es una línea de la herramienta

```
y= 98-99   x  880..1057   RGB (58,102,220)/(6,50,168)
y=108-109  x  475.. 941   RGB (58,102,220)/(6,50,168)   <- MISMO color exacto
y=236-237  x   80.. 662   RGB (57,101,219)/(6,50,168)   <- y hay una TERCERA
```

**Las tres tienen el mismo RGB y rangos de `x` que no se solapan: teselan el gráfico de izquierda a
derecha a tres alturas distintas.** Eso es la firma de **tres rayas horizontales dibujadas a mano**,
cada una terminada donde él soltó el ratón —no de niveles de una caja, que compartirían `x`—.

**La que pertenece a la caja es la de `y=98-99`**, y se sabe por el ancla: **arranca en `x=880`,
igual que la verde de `y=118-119`**. Las otras dos arrancan en `x=475` y `x=80`. **Un solo nivel
azul en la caja, como su plantilla dice.**

### La comprobación del 3,21: PASA

```
riesgo    = entrada 154,5 - stop 81,5  =  73,0 px
beneficio = teal 384,5 - 155,5         = 229,0 px
cociente  = 3,137      declarado 3,21      desvio 2,3 %   (margen +-3 %)
```

**Dentro del margen.** Lo identificado como stop **es** el stop: el borde superior de la zona roja.
La comprobación podía tumbar la lectura y no la tumba.

### La comprobación del ANCLA: NO PASA

Con la azul de la caja en `0,8` y la verde en `0,5`, separadas **20 px** para **0,3** de caja:

```
caja = 66,7 px   ·   nivel 0 en y=151,8   ·   nivel 1 en y=85,2
ANCLA: |151,8 - 154,5| = 2,7 px      criterio <= 2 px   ->   NO COMPARTEN
```

**2,7 px con un error de ±1 px no se explica como lectura.** Y la propagación tampoco salva:
con ±1 px en cada una de las cuatro medidas, la separación va de **0,3 a 5,1 px**, así que **ni
siquiera se puede afirmar que la superen o no**. Por el criterio pre-registrado, **la comparación
es inválida**.

### Y aun así, la fracción, para que conste

```
fraccion_del_stop = 73,0 / 66,7 = 1,095
etiqueta mas cercana: 1   ·   a 0,095   ·   tolerancia 0,03   ->   FUERA
```

**NO CONCLUYENTE**, y por partida doble: el ancla no se sostiene **y** la fracción no cae cerca de
ninguna etiqueta. **No se ensancha la tolerancia y no se cambia el criterio.**

### La obstrucción, sin adornarla

**La barra de herramientas flotante tapa `y≈120..145`.** El nivel **`0,25`** de la caja caería en
`y=135,2`: **debajo de la barra**. Y los niveles **`0` y `1`** no tienen línea propia visible —sólo
`0,8` y `0,5` la tienen—, así que **los dos extremos de la caja se deducen, no se ven**.

**Ésa sí es una limitación del material y no del instrumento**, y es la que de verdad impide la
medida en este fotograma: aunque la precisión alcance, **faltan los dos extremos**.

## R11. Lo que la semana enseña, y la pregunta que abre

Cuatro de las reglas buenas de esta semana —ADR-0038, la regla del huso, la del «15 de 18» y la
condición de precisión de esta rama— **no salieron de un diseño previo. Salieron de fallos.**

**Pero decirlo así se lee como consuelo, y es menos que eso: es un sesgo de selección.** No
salieron de «procedimientos que fallaron»: salieron de **fallos que una comprobación sacó a la
luz**. Los fallos que ninguna comprobación mira **no producen reglas: producen silencio**, y por
construcción no aparecen en esta lista.

**La pregunta que eso abre —y no es retórica, porque hoy tiene un ejemplo medido— es: qué está
fallando donde no mira ninguna comprobación.** El ejemplo es §R8: **tres ids `ev-*` inexistentes
en `docs/**` que no caza nadie**, y que no son fabricaciones **por suerte**, no por diseño. Nadie
los había visto en nueve días. Aparecieron porque esta rama fue a buscar *otra cosa*.

## R9. Lo que esta rama no hizo

No se reajustó el fractal. No se abrió el xlsx de enero. No se tocó febrero. No se tocó la
predicción congelada de mayo. **ADR-0038 no decide nada sobre qué se puede mirar**: sólo cómo se
llega a mirarlo.

## Estado
WAITING_FOR_USER_VALIDATION
