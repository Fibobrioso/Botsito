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

## Estado
PRE-REGISTRO COMMITEADO · sin datos leídos
