# v5, los seis instantes: la medida no está en v5

Rama `trabajo/v5-instantes`, 2026-09-23. Sin merge, sin tag y sin push. Son los puntos 3 y 4 de
Next Action: los instantes de v5 sin abrir y el decodificador de PNG en `scripts/`.

## 1. El criterio y la salida, citados por commit

- **Criterio congelado antes de mirar:** `bd9405f`, que es el documento
  `docs/validation/V5-INSTANTES-CRITERIO.md` más su implementación `scripts/v5_criterio.py`. Lo
  completa `306ce1b`: los fotogramas mixtos por instante, la lista cerrada de los 36 y la
  integridad contra la extracción de F05. `79f4390` solo añade la impresión de esa integridad.
- **Decodificador:** `3f40481`, con `scripts/decodificar_png.py` y un test que fabrica sus propios
  PNG con los cinco filtros.
- **Salida congelada:** `d279a3b`, `docs/validation/V5-INSTANTES-SALIDA.txt`. Es la salida exacta
  de una sola ejecución de `uv run python scripts/v5_criterio.py --medir`. La integridad salió
  completa: los dos eslabones y los 36 hashes coinciden con los de F05.

## 2. El resultado

**0 de 36 fotogramas sirven.**

| instante | fotogramas | qué falla |
|---|---|---|
| 1 (`0:01:46`) | `000106000`…`000111000` | a) y b), en los seis |
| 2 (`0:02:33`) | `000153000`…`000158000` | a) y b), en los seis |
| 3 (`0:03:21`) | `000201000`…`000206000` | a) y b) en los cinco primeros; solo b) en `000206000` (niveles 0 y 1 en y=424 y 237) |
| 4 (`0:03:29`) | `000209000`…`000214000` | solo b), en los seis (niveles 0 y 1 en y=424 y 237) |
| 6 (`0:04:44`) | `000284000`…`000289000` | solo a), en los seis |
| 7 (`0:04:58`) | `000298000`…`000303000` | solo a), en los seis: el nivel 1 se ve y el nivel 0 no |

## 3. La regla, aplicada

La regla congelada (§e del criterio) dice: *«Si ningún fotograma de los 36 cumple a) y b), se escribe
"la medida NO ESTÁ en v5" y se cierra esa vía.»* Y la salida global es
`== GLOBAL: la medida NO ESTA en v5`.

- **La medida NO ESTÁ en v5. La vía se cierra.**
- **A-18 sin cambios:** `(riesgo_real, 0,8)` y `(caja_completa, 1,0)` siguen sin separarse
  (ADR-0040). **No sube a bloqueante**, porque el resultado no es «contradictorio».

## 4. Una observación descriptiva, sin inferencia

En `000298000`…`000303000` (instante 7), el **stop** medido está en **y=160**, a **1 px** del
**nivel 1**, que está en **y=161**. Y `|TP − entrada| / |entrada − stop| = (447 − 232) / (232 − 160) =
2,99`. **Falta el nivel 0**, así que la caja no se puede anclar a la entrada, y por la regla
**estos fotogramas no cuentan**. **No es evidencia a favor de ninguna combinación.** Se anota para
quien pregunte al trader.

## 5. Las correcciones que deja la rama

- **Los pendientes eran seis, no cinco:** el 1, 2, 3, 4, 6 y 7. El 5 contaba como abierto
  (`000216000` a +2 s, `000225000` a +11 s), y `000292000`–`000293000` no se asignaron ni al 6 ni
  al 7. Next Action decía «cinco»; corregido.
- **Los cuatro fotogramas ya abiertos** (`000216000`, `000225000`, `000292000` y `000293000`) son
  los únicos con los que se calibró. **Dos de ellos, `000216000` y `000225000`, se volvieron a leer
  durante esta rama** para explicar las etiquetas (§6). **Ninguno de los cuatro está entre los 36**,
  y hay un test que lo comprueba (`test_la_lista_cerrada_son_36_de_la_ventana_y_ninguno_ya_abierto`).
- **§R10 de `LA-CAJA-DEL-29-DE-ABRIL.md`, a medias:** en `000292000` el nivel 1 **sí** tiene línea
  propia (y=83–84); el que falta es el 0. La conclusión de §R10 no cambia (criterio, §c).
- **`PROJECT_STATE.md:415`** decía que hacía falta «caja ≥ 100 px». Eso quedó sin efecto desde
  §R10; corregido en `bd9405f`.

## 6. Las etiquetas de los niveles 0 y 1

**Se preguntó** si la calibración había dado `nivel_0=237` y `nivel_1=424` en `000216000`, al revés
que la medición en 206–214. **Medido, releyendo solo `000216000` y `000225000`: no.** Los dos dan
`nivel_0 424 nivel_1 237`, igual que 206–214, y el criterio (§c, línea 80) ya decía «nivel 1 en
y=237, nivel 0 en y=424». Lo ambiguo era un resumen del chat, «(y=237 y 424)», que no decía cuál
era cuál.

**Cómo decide el detector cuál es el 0 y cuál el 1.** Por la geometría de los colores de la
caja, no por arriba o abajo:
- el nivel 1 queda al otro lado del 0,8 (`y1 = y08 − 0,2·Δ`, `scripts/v5_criterio.py:140`);
- el nivel 0 queda al otro lado del 0,5 (`y0 = y05 + 0,5·Δ`, `:144`).

**b) no depende de esa etiqueta.** `detector_b(img)` no recibe la caja (`b, h = detector_b(img)`),
y `:325` (`if not (a and b)`) invalida todo fotograma que falle b). Los veredictos de 206–214 no
cambian con ninguna etiqueta.

**Un defecto que sí hay, y no es de etiquetado: la orientación.** La caja solo se reconoce si el
0,5 queda **por debajo** del 0,8 en la imagen: `5 <= yv - ya <= 400` (`:155`). Esa es la
orientación de una **venta**. Una caja de **compra**, con el 0,8 debajo del 0,5, no se detecta.
**No habría cambiado ningún veredicto de `d279a3b`**, y se demuestra con el código, sin ejecutar
nada:
- en los instantes 1 a 4 todos los fotogramas fallan b), y b) no depende de la caja (`:325`);
- en los instantes 6 y 7 b) pasa con una herramienta de **venta** (stop 208 < entrada 279,5, y
  stop 160 < entrada 232). Una caja de compra tendría `y1 > y0`, y entonces
  `(y1 − y0)·(y_stop − y_entrada) < 0`, que por `:332` («el nivel 1 y el stop no están del mismo
  lado») invalida el fotograma. Una caja de venta ya se detecta.

**No se corrige.** Corregir el detector después de medir sería cambiar el criterio sobre una salida
ya vista, y la vía está cerrada. Si alguien reutiliza `scripts/v5_criterio.py` con otro vídeo, esta
limitación va primero.

## Pregunta al trader (RESERVA)

**Solo se usa si la búsqueda en las transcripciones del corpus no resuelve A-18** (Next Action 14,
en su propia rama, con la regla fijada antes de buscar). Hasta entonces no se envía.

> Cuando colocas la orden con la herramienta de posición, ¿cómo decides dónde va el stop y cómo
> calculas dónde va el TP? Cuéntamelo paso a paso con un ejemplo, usando los niveles de la caja si
> los usas.

Su respuesta entra como feedback (`fb-*`), por su régimen.

## 7. Cierre

`state check` OK. `make check` en verde, con el log borrado.

**Un tropiezo del cierre, dicho.** El commit `40759cb` se hizo con `make check` en **rojo**: el
commit no estaba condicionado al resultado. El fallo era
`test_no_crlf_in_tracked_text_files`, porque la **copia de trabajo** de
`V5-INSTANTES-SALIDA.txt` conservaba los CRLF que imprimió la consola de Windows. El contenido
commiteado en `d279a3b` siempre fue LF (git lo normaliza por `.gitattributes`), y el texto es el
mismo. Se corrigió restaurando la copia de trabajo desde el blob, sin tocar el contenido, y desde
ahí cada commit va condicionado a `make check`. Guardia de ids OK. `kit check --sesion
2026-09-09-sesion-01` idéntico a la línea base. PREREGISTRO con blob `52649183…` y cero
autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
