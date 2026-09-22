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

## R6. Lo que esta rama no hizo

No se reajustó el fractal. No se abrió el xlsx de enero. No se tocó febrero. No se tocó la
predicción congelada de mayo. **ADR-0038 no decide nada sobre qué se puede mirar**: sólo cómo se
llega a mirarlo.

## Estado
WAITING_FOR_USER_VALIDATION
