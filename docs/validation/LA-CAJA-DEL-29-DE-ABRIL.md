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

## Estado
PRE-REGISTRO COMMITEADO · sin fotogramas abiertos en esta rama
