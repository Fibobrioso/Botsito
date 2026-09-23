# v5, los seis instantes: el criterio de lectura, congelado antes de mirar

Rama `trabajo/v5-instantes`, 2026-09-23. **Este documento se commitea ANTES de abrir ningún fotograma
nuevo.** Todo lo que dice se calibró **solo** con los cuatro fotogramas ya abiertos
(`000216000`, `000225000`, `000292000` y `000293000`) y con fotogramas sintéticos. Su
implementación exacta es `scripts/v5_criterio.py`: cambiarla después de mirar es cambiar el
criterio.

## 0. Los instantes: seis, no cinco

La transcripción de v5 localiza siete (`LA-CAJA-DEL-29-DE-ABRIL.md` §1c). El consultor decidió el
2026-09-23 que el **5** (`0:03:34`, «protejo aquí») cuenta como abierto, porque `000216000` está a
+2 s y `000225000` a +11 s. `000292000` y `000293000` **no se asignan ni al 6 ni al 7**. Así que
quedan **seis pendientes**: el 1, 2, 3, 4, 6 y 7. El «cinco» de Next Action estaba mal contado y se
corrige en `PROJECT_STATE.md`.

**Ventana fija, sin elegir mirando:** por cada instante, exactamente los fotogramas de `t`, `t+1`,
`t+2`, `t+3`, `t+4` y `t+5` s. Son 36 en total, y ninguno más.

| instante | t | ficheros (`data/fotogramas/v5/png-1fps/`) |
|---|---|---|
| 1 | `0:01:46` | `000106000` … `000111000` |
| 2 | `0:02:33` | `000153000` … `000158000` |
| 3 | `0:03:21` | `000201000` … `000206000` |
| 4 | `0:03:29` | `000209000` … `000214000` |
| 6 | `0:04:44` | `000284000` … `000289000` |
| 7 | `0:04:58` | `000298000` … `000303000` |

Los 36 días son el **29 de abril de 2026**, la sesión de backtest de v5 según `fuentes.yaml`. **No
están reservados y no son de septiembre**: `caso-eurusd-2026-04-29` no está en `casos_reservados`
ni en ningún reparto.

## a) Detector «líneas propias de los niveles 0 y 1»

Todo en píxeles del fotograma, que mide 1280×720. Región del gráfico: `x` de 75 a 1249, `y` de 80
a 639.

1. **Clases de color, por tono.** Se clasifica por tono y no por RGB exacto porque, dentro de las
   zonas de la herramienta, las líneas salen teñidas: en `000292000` el azul es `(95,92,193)`, no
   `(58,102,220)`.
   - **azul** (nivel 0,8): `B ≥ R + 60` y `B ≥ G + 60`.
   - **verde** (nivel 0,5): `G ≥ R + 20` y `G ≥ B + 40`.
   - **gris** (bordes de la caja, niveles 0 y 1): `max(RGB) − min(RGB) ≤ 16` y `95 ≤ R ≤ 175`.
2. **La caja:** una fila con un tramo azul y otra con un tramo verde, de **≥ 40 px seguidos** cada
   uno, que **acaban en la misma `x` (±3)**. El borde derecho es el de la caja; el izquierdo lo
   cortan etiquetas y trazos. La verde queda de 5 a 400 px por debajo. Si hay varias parejas, gana
   la de tramos más largos. Con ellas: `Δ = (y₀,₅ − y₀,₈) / 0,3` px por unidad de caja,
   `y₁ = y₀,₈ − 0,2·Δ` e `y₀ = y₀,₅ + 0,5·Δ`.
3. **Línea propia:** en alguna fila a **±3 px** de `y₁` (y otra de `y₀`) hay un tramo **gris
   continuo** que cubre **≥ 50 % del ancho** de la caja, dentro de su rango en `x`. Una línea
   discontinua, como la cruz del ratón o la línea de precio, no llega al 50 % seguido.
4. **SÍ** solo si están **los dos**, el nivel 0 y el nivel 1.

## b) Detector «herramienta de posición válida», sin OCR

En estado de error («Order Error») la herramienta **no pinta sus zonas**; válida, pinta una zona
roja (el stop) y una teal (el objetivo), pegadas en la arista de entrada.

1. **Relleno de las zonas**, por canal: **rojo** `|RGB − (59,22,26)| ≤ 8`; **teal**
   `|RGB − (12,41,38)| ≤ 8`.
2. **Una columna tiene herramienta** si, en la región del gráfico:
   - el relleno rojo y el teal **abarcan** cada uno **≥ 20 px**, del primer al último píxel;
   - de cada uno se ven **≥ 6 px**, porque las barras flotantes tapan;
   - **no se solapan** y quedan a **≤ 6 px** entre sí.

   Venta: rojo arriba y teal abajo. Compra: al revés.
3. **VÁLIDA** si hay **≥ 30 columnas seguidas** con herramienta.
4. **Medida**, mediana sobre esas columnas:
   - **stop** = borde exterior de la zona roja, incluidas las filas rojizas pegadas a ella
     (`R ≥ G + 25` y `R ≥ B + 20`): son bordes de la caja teñidos por la zona;
   - **entrada** = punto medio entre las dos zonas;
   - **TP** = borde exterior de la teal.

## c) Calibración: los dos detectores tienen positivo y negativo reales

Resultado de `uv run python scripts/v5_criterio.py --calibrar` sobre los cuatro fotogramas abiertos:

| fotograma | a) niveles 0 y 1 | b) herramienta válida | medida de la herramienta | RR medido / impreso |
|---|---|---|---|---|
| `000216000` | **SÍ**: nivel 1 en y=237, nivel 0 en y=424 (previstos 236,7 y 423,3) | **NO**: estado «Order Error», sin zonas | — | — |
| `000225000` | **SÍ**: 237 y 424 | **NO** | — | — |
| `000292000` | **NO**: nivel 1 en y=83; **nivel 0 ausente** | **SÍ** | stop 82 · entrada 154 · TP 384 | **3,194 / 3.21** |
| `000293000` | **NO**: la barra del objeto tapa el 0,8 y no hay caja | **SÍ** | stop 82 · entrada 154 · TP 369 | **2,986 / 3** |

- **a) dice NO en `000292000`**, el negativo conocido de §R10. Sus positivos reales son
  `000216000` y `000225000`.
- **b)** tiene dos positivos reales (`000292000` y `000293000`) y dos negativos reales (`000216000`
  y `000225000`). La medida de las zonas **reproduce el RR que la propia herramienta imprime** con
  un 0,5 % de diferencia, y en `000292000` da los mismos bordes que midió §R10 (82, 154, 384).
- **Ningún fotograma abierto cumple a) y b) a la vez.** Por eso la medida quedó NO CONCLUYENTE.
  El positivo de la cadena completa (válido, y separa) es **sintético**:
  `tests/unit/test_v5_criterio.py` pinta una caja y una herramienta con los colores calibrados. Con
  el stop en 0,8 y el TP a 2,4 cajas sale «separa: riesgo_real»; con el stop en 1,0 y el TP a 3
  cajas, «separa: caja_completa»; con la entrada a 10 px del nivel 0, «no válido: ancla».

**Una corrección a §R10, medida.** §R10 dice que en `000292000` «los niveles `0` y `1` no tienen
línea propia visible». **El nivel 1 sí la tiene**: un gris `(114,114,114)` en y=83–84, a 1–2 px de
donde lo ponen el 0,8 y el 0,5. Lo que falta es solo el nivel 0. La conclusión de §R10 no cambia
(sin los dos extremos no hay medida), pero la frase era la mitad falsa.

## d) Las dos lecturas supervivientes de A-18, y su predicción en píxeles

Citadas literalmente:

- `knowledge/spec/parametros.yaml`, `base_calculo_objetivo`: *«`caja_completa` es la distancia
  nivel 0 -> nivel 1; `riesgo_real` seria la distancia hasta stop_fraccion_caja.»*
- `knowledge/spec/parametros.yaml`, `stop_fraccion_caja`: *«nivel de la caja donde vive el stop.
  Se escribe EN la orden limite y no se mueve despues»*.
- `knowledge/spec/parametros.yaml`, `objetivo_rr`: *«objetivo fijo, en multiplos de la distancia
  que fija base_calculo_objetivo.»*
- ADR-0040, decisión 2: *«`(riesgo_real, 0,8)`: el objetivo se mide sobre la distancia hasta el
  stop, y el stop está a 0,8 de la caja»*; *«`(caja_completa, 1,0)`: el objetivo se mide sobre la
  caja entera, y el stop está en su borde.»*

**Predicción en píxeles**, con `objetivo_rr` = 3, la entrada en el nivel 0 (§R1) y
`d = y₁ − y₀` con signo, hacia el lado del stop:

| superviviente | stop previsto | TP previsto |
|---|---|---|
| `(riesgo_real, 0,8)` | `y₀ + 0,8·d` (nivel 0,8) | `y₀ − 3·0,8·d = y₀ − 2,4·d` |
| `(caja_completa, 1,0)` | `y₀ + d` (nivel 1) | `y₀ − 3·d` |

Las dos predicen el mismo RR sobre entrada-stop, 3,00, así que **el RR no las separa**. Lo que las
separa es **dónde caen el stop y el TP respecto a la caja**: el stop difiere en `0,2·|d|` y el TP en
`0,6·|d|`. En una caja de 67 px, como la de `000292000`, son 13 y 40 px.

**Un fotograma SIRVE** si cumple a) y b), además de dos condiciones ya escritas:
- **ancla**: `|y(nivel 0) − y(entrada de la herramienta)| ≤ 2 px`, criterio de
  `LA-CAJA-DEL-29-DE-ABRIL.md:180`;
- **coherencia**: el nivel 1 y el stop están del mismo lado de la entrada.

Los `y₀` e `y₁` que se usan son **los bordes grises medidos por a)**, no los previstos.

## e) La regla de decisión

**Fijada por el consultor, literal:**

> Tolerancia ±2 px. Un instante SEPARA si uno de los dos supervivientes cae dentro de ±2 px y el
> otro queda fuera por más de 4 px. Si ambos caen dentro, o ambos fuera, o la diferencia es de 2 a
> 4 px, NO SEPARA. Resultado global: se declara separación si al menos un instante válido separa y
> ningún instante válido separa en sentido contrario. Si hay instantes en ambos sentidos, el
> resultado es «contradictorio», A-18 sube a bloqueante y no se elige superviviente. Si ningún
> fotograma de los 36 cumple a) y b), se escribe «la medida NO ESTÁ en v5» y se cierra esa vía.

**Cómo lo implemento, y son decisiones mías que conviene revisar:**
1. **Error de un superviviente** en un fotograma = `max(|stop medido − stop previsto|, |TP medido −
   TP previsto|)`. Tiene que cumplir los dos, stop y TP, no solo uno.
2. **Veredicto de un fotograma que sirve:**
   - «separa: X» si el error de X es ≤ 2 px y el del otro > 4 px;
   - si no, «no separa».
3. **Un instante** es válido si al menos uno de sus 6 fotogramas sirve. **Fotogramas mixtos**
   (fijado por el consultor el 2026-09-23, antes de medir):
   - **separa hacia X si al menos uno de sus fotogramas válidos separa hacia X y ninguno separa en
     sentido contrario. Los fotogramas «no separa» no vetan;**
   - si dentro del instante hay fotogramas en los dos sentidos, el instante es
     **«contradictorio»**, y eso cuenta como contradicción global;
   - si ninguno separa, «no separa».

   **El informe muestra siempre los 36 resultados por fotograma, sirvan o no.**
4. **Global:**
   - ningún instante válido: **«la medida NO ESTÁ en v5»**;
   - instantes en los dos sentidos, o alguno contradictorio: **«contradictorio»** (A-18 sube a
     bloqueante);
   - al menos uno hacia X y ninguno hacia el otro: **«separación hacia X»**;
   - si no, **«no separa»**.

## f) La extracción: no hace falta; los 36 fotogramas ya existen

v5 está extraída entera a 1 fps desde F05. El manifiesto commiteado es
`knowledge/corpus/fotogramas/fr-v5-718ecabb.yaml`: `ffmpeg 9.0.1-full_build-www.gyan.dev`,
`bitexact: true`, PNG, 1 fps y selección
`isnan(prev_selected_t)+gte(floor(t),floor(prev_selected_t)+1)`. Son 366 fotogramas y ningún
hueco, y el nombre de cada fichero es su instante en milisegundos. Así se obtuvieron los cuatro
abiertos. **Los 36 de la ventana existen**: se comprobó solo por nombre, con `ls`, sin abrir
ninguno. `ffmpeg` está instalado, pero **no se re-extrae nada**: volver a extraer crearía otro
manifiesto sin ninguna necesidad.

**El comando que lee los 36**, que NO se ha ejecutado:

```
uv run python scripts/v5_criterio.py --medir
```

**Integridad**, añadida el 2026-09-23 en un commit posterior a `bd9405f` y anterior a medir:
- **Lista cerrada:** los 36 nombres están escritos en el código (`MEDIR`), y se comprueba al
  cargar que son exactamente la ventana t…t+5 s de los seis instantes. Cualquier otro nombre se
  rechaza **antes de leer un solo byte del fichero**; hay un test que lo comprueba con el
  decodificador prohibido.
- **Contra F05, fichero a fichero, antes de decodificar ninguno.** El manifiesto commiteado
  `fr-v5-718ecabb.yaml`, inmutable por hook, fija `sha256_index`. Ese es el sha del
  `index.jsonl` de la extracción, y el índice trae **el sha256 de cada PNG**. `--medir` comprueba
  primero que el índice es el del manifiesto y después que los 36 ficheros tienen su sha. Si
  falla algo, se para sin decodificar nada.

**Salida**, una línea por fotograma, sirva o no:
- si sirve, o qué condición falla;
- la posición en px del stop, la entrada, el TP, el nivel 0 y el nivel 1;
- el error de cada superviviente;
- el veredicto del fotograma.

Después, el veredicto de cada instante y el global.

## Estado

CRITERIO CONGELADO. Pendiente de la luz verde del consultor para ejecutar `--medir`.
