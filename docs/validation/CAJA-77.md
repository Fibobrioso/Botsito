# La caja de las 77: qué regla da la caja del trader, con el stop en el 0,8 o en el 1

Rama `feature/caja-77`, 2026-09-30, desde `main` en `5731f71` (`stable/F36-nocturno-01oct`). Es la
C del Next Action: la medición PRE-REGISTRADA de R1 a R6 de `BLOQUE-DE-LA-CAJA.md` §1.4 sobre las
77 operaciones de construcción. **Descriptiva**: no cambia el motor, el productor, RN-011 ni ningún
parámetro, regla, ambigüedad, evidencia o registro de feedback. Nada se resuelve aquí; su resultado
es la entrada de la D (F35, el bloque por selector).

## 1. El criterio, escrito y commiteado ANTES de medir (2026-09-30)

Este apartado se commitea antes de leer ninguna fila de ningún caso y antes de cruzar ninguna vela.
**No se cambia después.** Si hay que corregirlo, se añade una nota con fecha debajo, el cuerpo queda
intacto y las dos versiones se presentan juntas, como en `BLOQUE-DE-LA-CAJA.md` §1.5.

**Por qué esta medida y no la de la pantalla.** `BLOQUE-DE-LA-CAJA.md` leyó 12 cajas en los
fotogramas: todas ventas y de cuatro días. Con el criterio escrito antes (su v1), ninguna regla
explicó más de una caja, y el consultor concluyó que «el 0 de la caja no sale de los fotogramas con
esta muestra». Aquí la caja no se lee en la pantalla: se **reconstruye desde el libro**, con la
entrada como el 0 y el stop como el 0,8 o como el 1. Así entran las 77 operaciones, compras
incluidas.

### 1.1 Qué operaciones entran

- **El universo**: las operaciones de los días `dev` de abril y agosto de 2026, los dos meses de
  construcción, tal como las devuelve `arnes.dias_de_construccion` (la compuerta del arnés). Se
  esperan **77**. Si salen otras, se para antes de medir y se dice cuántas.
- **Antes de leer ninguna fila**: `casos_reservados(repo)` y `casos_ocultos(repo)` sobre esos días.
  Se espera 0; si no es 0, se para. Los dos meses son de desarrollo (CLAUDE.md, «Material de
  DESARROLLO»).
- **De cada operación se leen cuatro campos del caso ya ingerido**
  (`knowledge/cases/.../caso-*.yaml`, F14a): `instante_utc`, `direccion`, `entrada` (el
  `entryPrice` del libro) y `stop` (su `initialSL`). **No se abre ningún xlsx, ningún fotograma ni
  ninguna transcripción.** Son los mismos casos que ya leen el arnés, `ORDEN-STOP-O-LIMITE.md` y
  `EMBUDO-77.md`, así que no hay exposición nueva que declarar.
- **Queda fuera**, con su motivo y una a una:
  - el stop del lado equivocado: por debajo de la entrada en una venta, por encima en una compra;
  - el stop a menos de 1 punto de la entrada;
  - ninguna vela M1 en la ventana de §1.3.

### 1.2 La caja del trader, reconstruida desde el libro

Precios en puntos: escala 100 000, 5 decimales. Una VENTA; una COMPRA es la simétrica (§1.5).

- **El 0** = la entrada del libro. `BLOQUE-DE-LA-CAJA.md` §5.3 midió la orden en el 0 en 11 de 12
  cajas, y `ORDEN-STOP-O-LIMITE.md` que las 77 se llenaron desde el lado de la ruptura (orden stop).
  **Se supone que el precio de llenado del libro es el de la orden**, sin deslizamiento.
- **El 1**, en dos lecturas que se miden siempre las dos:
  - **L0,8, el stop en el 0,8**: 1 = 0 + (stop − 0) / 0,8. El 1 puede no caer en un punto entero, y
    se compara sin redondear.
  - **L1, el stop en el 1**: 1 = stop.
- **Lo que no se puede separar.** El trader redondea el stop hacia fuera (ADR-0061). En L0,8 eso
  mueve el 1 reconstruido hasta 1,25 puntos, y se hereda. Tampoco se sabe si `initialSL` es el stop
  al colocar la orden o al llenarse. `BLOQUE-DE-LA-CAJA.md` §5 vio las dos secuencias: del 1 al 0,8,
  y quedarse en el 1. Por eso se miden las dos lecturas y ninguna se da por buena de antemano.

### 1.3 Las velas y el instante de referencia

- **Velas**: las M1 de Dukascopy del repositorio, `eurusd-m1-2026-04-990211bd` y
  `eurusd-m1-2026-08-0d42230e` (precio BID, `ts_utc` en UTC), por su manifiesto. **Husos fijados antes de comparar**: `instante_utc` es UTC (el huso del libro
  se midió por velas, ADR-0039) y las velas son UTC. No hay conversión.
- **El instante de referencia T** = `instante_utc`, que es el **LLENADO**
  (`INSTANTE-LLENADO-SALIDA.txt`: 93 de 94 al minuto), no la colocación. El libro no da la hora de
  colocación.
- **Qué vela cuenta como cerrada**: una M1 cuyo minuto termina a la hora de inicio del minuto que
  contiene T, o antes. **La vela en curso en T, la del minuto del llenado, NO entra**: es la que
  rompe el 0, y su extremo del lado de la ruptura queda por construcción al otro lado del 0.
- **La ventana**: las M1 cerradas en [T − 90 min, minuto de T), la misma de
  `BLOQUE-DE-LA-CAJA.md` §1.3.
- **Límite que se declara ya**: la caja se dibuja antes de colocar la orden, y la orden se coloca
  antes de llenarse. Las velas que cierran entre la colocación y el llenado **entran** en la
  ventana y pueden mover la «última vela contraria». Cuántos minutos son no se sabe: en las cajas
  de v7 y v8 iban de 1 a 6 (`BLOQUE-DE-LA-CAJA.md` §2.4). Pesa en contra de todas las reglas por
  igual, y no se corrige.

### 1.4 Las reglas: las de BLOQUE-DE-LA-CAJA §1.4, con su código

R1 a R6 son **exactamente las funciones `r1` a `r6` de `scripts/bloque_de_la_caja.py`**, tal como
están en `main` en `5731f71`. Se importan, no se reescriben:

- R1, la última vela contraria;
- R2, R1 y la siguiente si la cubre con la mecha;
- R3, la última envolvente del color de la entrada;
- R4, la racha de contrarias consecutivas que termina en R1;
- R5, el último pivote de M1 contrario a la entrada, con `cierre_vela_contraria`, y las velas desde
  la que marca el nivel hasta la contraria que lo forma;
- R6, del nivel de R5 al extremo de las velas entre ese pivote y T.

Cada una recibe la ventana de §1.3 y el lado, y devuelve (0, 1) o nada: «no da caja». El productor
no se mide aquí.

### 1.5 Las compras, simétricas de las ventas

En una compra se cambian mínimas por máximas y los colores. La contraria es la bajista, y el 0 de
la caja es su máximo. El código de §1.4 ya lo hace por el lado (`cero_uno`, `contraria`). **Todas
las cifras se dan además por separado para compras y para ventas.** Las velas son BID y la entrada
de una compra se llena en el ask, y no se corrige el spread. Si las compras salen sistemáticamente
peor, esa es la primera sospecha, y se dirá.

### 1.6 La tolerancia, el desfase entre proveedores y qué es un acierto

- **La tolerancia τ = 2 puntos**, el `margen_puntos` de `knowledge/corpus/criterio_huso.yaml`
  (A-16). **Sensibilidad: τ = 1 y τ = 3.**
- **El desfase OANDA − Dukascopy.** El libro son precios de OANDA (FX Replay) y las velas son de
  Dukascopy.
  - **Principal: sin corrección.** El desfase queda dentro de τ, como en la v1 de
    `BLOQUE-DE-LA-CAJA.md`.
  - **Sensibilidad: el 0 y el 1 del trader desplazados −2 puntos**, la mediana +2 medida en agosto
    en `BLOQUE-DE-LA-CAJA.md` §2.3 (9 velas, OANDA por encima).
  - Abril no tiene un desfase con signo medido: `ABRIL-Y-LA-CAJA.md` da 1 y 2 puntos con n = 2. Por
    eso la corrección no va en la principal, y la sensibilidad se da también por mes.
- **Un acierto**: una regla acierta una operación en una lectura si su 0 y su 1 están **los dos** a
  ≤ τ del 0 y del 1 del trader. Se cuentan también «solo el 0», «solo el 1» y «no da caja».
- **La celda principal**, la única que se lee como resultado: **τ = 2, sin corrección, las 77 (menos
  las de fuera), por regla y por lectura (L0,8 y L1).** Todo lo demás es sensibilidad.
  - Por regla: aciertos, solo el 0, solo el 1, no da caja.
  - Por lectura: cuántas operaciones explica alguna regla y cuántas ninguna.
  - Por dirección y por mes.
- **No se elige ganadora en este informe.** Qué regla y qué lectura pasan al selector de la D lo
  decide el consultor con la tabla.

### 1.7 Salida

`scripts/caja_77.py` escribe `docs/validation/CAJA-77-SALIDA.txt`. Lleva, operación a operación, el
día, la dirección, T, el 0 y el 1 en las dos lecturas, y la diferencia «regla − trader» en el 0 y en
el 1 de cada regla. Todas son de días `dev`: su detalle se lee sin puerta (ADR-0037). Solo lee el
repositorio y escribe solo esa salida. Se ensaya antes en un clon desechable con `git worktree add`
(CLAUDE.md, «Ensayos aislados»).

### 1.8 Nota del 2026-09-30, del consultor, añadida ANTES de medir

Tras revisar §1.1–§1.7, que no se tocan, el consultor añade cuatro puntos. Se commitean y se suben
al remoto antes de leer ninguna fila ni cruzar ninguna vela.

**1. El umbral, pre-registrado.**
- **Evaluable** es una operación que no queda fuera por §1.1. Una regla que «no da caja» en una
  operación evaluable cuenta como fallo, no la saca del denominador.
- **Una regla queda SOSTENIDA** si, en la celda principal (τ = 2, sin corrección) y en al menos una
  de las dos lecturas del stop, acierta en el **40 % o más de las operaciones evaluables**.
- **Entre R1 y R4 deciden solo las operaciones en que dan cajas distintas** (distinto 0 o distinto
  1; si una de las dos no da caja, también cuenta como distinta). En ese subconjunto, y en cada
  lectura, **gana la que acierte al menos el doble que la otra**, con al menos un acierto. Si
  ninguna llega al doble, R1 frente a R4 queda sin decidir en esa lectura.
- **Si ninguna regla queda sostenida, el resultado es «no decide»** y la pregunta va a la sesión 4.
- **Se informa aparte** en cuántas operaciones R1 y R4 dan la misma caja y en cuántas difieren, y
  los aciertos de cada una en cada grupo.

**2. El control de la reconstrucción, que se informa ANTES que el resultado principal.**
- **Qué cajas.** Las de `BLOQUE-DE-LA-CAJA.md` con pareja en el libro según ADR-0043, tal como la
  fijaron `SESION-02-VIDEO.md` §4 y `SESION-02-VIDEO-V8.md` §4: v7 n.º 2, 3, 5, 11 y 15. v8 n.º 1 no
  tiene pareja.
- **Qué niveles y horas.** Solo lo que `BLOQUE-DE-LA-CAJA.md` ya leyó: el 0, el 1 y la hora de
  colocación de su §2.2. Para v7 n.º 2 se usa la caja que el trader dejó, la de §5.3
  (0 = 1.15364, 1 = 1.15380), y se da también la primera. **No se abre ningún fotograma.**
- **(a) La caja reconstruida frente a la leída.** Con la entrada y el stop del libro, la caja en L0,8
  y en L1, y su diferencia con la caja leída en pantalla en el 0 y en el 1.
- **(b) Las reglas ancladas en el llenado frente a la colocación real.** Cada regla, con la ventana
  de §1.3 anclada en el llenado del libro y anclada en la hora de colocación leída (M1 cerradas
  antes del minuto de colocación, la v1 de `BLOQUE-DE-LA-CAJA.md`). Se da la diferencia entre las
  dos cajas, y la de cada una con la caja leída.
- **Lo que se sabe ya y se dice aquí.** El libro es el backtest original y el vídeo es otra
  ejecución de los mismos días: en las cinco parejas el stop del libro difiere del stop del vídeo
  entre 3 y 17 puntos (`SESION-02-VIDEO.md` §4). El control mide cuánto pesa eso en la
  reconstrucción, y no se corrige.

**3. El spread.**
- **En la principal no se corrige**: la orden se coloca en el nivel dibujado sobre el gráfico BID, y
  el libro da ese precio.
- **Como sensibilidad, se repiten las compras restando al 0 y al 1 del trader el spread de los
  ticks de Dukascopy en T**: ask − bid del último tick en [T − 60 s, T], de los datasets
  `eurusd-ticks-2026-04-1d189bdd` y `eurusd-ticks-2026-08-75bd3a08`. Una compra sin tick en ese
  minuto se informa como «sin spread» y queda fuera de esa sensibilidad.

**4. Lo demás del criterio queda como está.**

## 2. La medida (2026-09-30, después de subir el criterio y su nota)

Script: `scripts/caja_77.py`. Salida completa, operación a operación: `CAJA-77-SALIDA.txt`. Se ensayó
en un clon desechable (`git worktree add` en la carpeta de trabajo, leyendo los datos del
repositorio y escribiendo fuera), y la salida del repositorio es idéntica byte a byte a la del
ensayo.

**El universo, tal como lo fijó §1.1**: 77 operaciones en 42 días `dev` de abril y agosto; 0 días
reservados u ocultos; **77 evaluables y 0 fuera**. Son 45 ventas y 32 compras, 35 de abril y 42 de
agosto. Las 32 compras tienen tick en T para la sensibilidad del spread.

### 2.1 El control de la reconstrucción (§1.8.2), antes del resultado

**(a) La caja reconstruida desde el libro frente a la leída en pantalla**, «reconstruida − leída»
en puntos, en el 0 / en el 1:

| caja | libro: entrada / stop | pantalla: 0 / 1 | L0,8 | L1 |
|---|---|---|---|---|
| v7-2 (la que dejó, §5.3) | 1.15364 / 1.15380 | 1.15364 / 1.15380 | 0 / +4 | **0 / 0** |
| v7-2 (la primera, §2.2) | 1.15364 / 1.15380 | 1.15352 / 1.15376 | +12 / +8 | +12 / +4 |
| v7-3 | 1.15362 / 1.15388 | 1.15364 / 1.15389 | −2 / +5,5 | **−2 / −1** |
| v7-5 | 1.15274 / 1.15284 | 1.15274 / 1.15290 | 0 / −3,5 | 0 / −6 |
| v7-11 | 1.15184 / 1.15193 | 1.15184 / 1.15210 | 0 / −14,75 | 0 / −17 |
| v7-15 | 1.15488 / 1.15516 | 1.15491 / 1.15516 | −3 / +7 | −3 / 0 |

- **El 0 se reconstruye bien**: a ≤ 2 puntos en 4 de 5 (v7-15 a −3).
- **El 1 sale mejor con el stop del libro en el 1 que en el 0,8**: a ≤ 2 puntos en 3 de 5 con L1
  (v7-2, v7-3 y v7-15) y en 0 de 5 con L0,8. Lo que eso dice: **el `initialSL` del libro coincide
  con el 1 de la caja de la pantalla más a menudo que con su 0,8**. Encaja con «primer cálculo desde
  el punto 1» (A-18), pero con cinco cajas no lo decide.
- **La caja entera** (0 y 1 a ≤ 2) se reconstruye en 2 de 5 con L1 y en 0 de 5 con L0,8.
- **v7-11 no se reconstruye con ninguna lectura**: el stop del libro está 17 puntos por debajo del de
  la pantalla. Es lo que ya se sabía (§1.8.2): el libro y el vídeo son dos ejecuciones distintas de
  los mismos días.

**(b) Las reglas ancladas en el llenado frente a la colocación leída.** En v7-3 y v7-5 las seis
reglas dan la misma caja con los dos anclajes. En v7-2, v7-11 y v7-15, **R1 y R4 cambian entre 7 y
15 puntos** en el 0 o en el 1 según el anclaje. También cambian R3 y R5 en v7-2, R5 en v7-15 y R6
en las tres. Anclar en el
llenado, como obliga el libro, mueve la «última vela contraria» en 3 de 5 cajas. Es el límite que
§1.3 declaró, y aquí está medido. Contra la caja leída, a ≤ 2 en el 0 y en el 1:
- **ancladas en el llenado**: R4 en v7-2 (−1 / +1) y en v7-11 (0 / −1), y R6 en v7-11 (+1 / −1);
- **ancladas en la colocación**: R5 y R6 en v7-15 (0 / −1), y R1 y R4 en v7-15 (−2 / −1).

**Lo que el control deja dicho antes de leer el resultado.** La reconstrucción acierta el 0 casi
siempre y el 1 solo a veces, mejor con L1. El anclaje en el llenado mueve la caja de R1 y R4 en la
mitad de los casos. Las dos cosas restan aciertos a todas las reglas, así que **el resultado de §2.2
es probablemente una cota inferior** de lo que cada regla explicaría con la hora de colocación y el
stop de pantalla.

### 2.2 La celda principal (τ = 2, sin corrección, 77 evaluables) y el veredicto

| regla | L0,8: acierta | solo el 0 | solo el 1 | no da caja | L1: acierta | solo el 0 | solo el 1 | no da caja |
|---|---|---|---|---|---|---|---|---|
| R1 | 12 (16 %) | 11 | 13 | 0 | 7 (9 %) | 16 | 15 | 0 |
| R2 | 0 (0 %) | 5 | 4 | 56 | 3 (4 %) | 2 | 2 | 56 |
| R3 | 0 (0 %) | 6 | 3 | 0 | 1 (1 %) | 5 | 5 | 0 |
| R4 | 11 (14 %) | 20 | 13 | 0 | 11 (14 %) | 20 | 11 | 0 |
| R5 | 12 (16 %) | 24 | 5 | 0 | 8 (10 %) | 28 | 7 | 0 |
| R6 | 11 (14 %) | 25 | 12 | 0 | 12 (16 %) | 24 | 11 | 0 |

**Veredicto, con el umbral de §1.8.1: NO DECIDE.** Ninguna regla llega al 40 % en ninguna lectura;
la que más acierta se queda en el 16 %. **La pregunta va a la sesión 4.**

**R1 frente a R4.** Dan la misma caja en 46 operaciones y distinta en 31.

| | L0,8: R1 / R4 | L1: R1 / R4 |
|---|---|---|
| misma caja (46) | 8 / 8 | 5 / 5 |
| caja distinta (31) | 4 / 3 → sin decidir | 2 / **6 → gana R4** |

R4 gana a R1 en las distintas solo con L1 (6 frente a 2). Como ninguna de las dos queda sostenida,
eso no decide nada: dice por dónde preguntar.

**Lo que sí se lee.** El 0 lo dan R4, R5 y R6 mucho más que el 1: entre 31 y 36 de 77 operaciones
tienen el 0 a ≤ 2 puntos, contando los aciertos. **El 1 es donde fallan todas.** Y el 1 es
justamente lo que depende de cómo se lea el stop y de la hora de colocación, que el control ya
señaló como el punto débil de la reconstrucción.

### 2.3 Las sensibilidades (no deciden)

Aciertos, L0,8 / L1, de 77 salvo donde se dice:

| | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|
| τ = 1 | 5 / 4 | 0 / 2 | 0 / 1 | 4 / 6 | 4 / 3 | 4 / 4 |
| τ = 3 | 14 / 17 | 3 / 5 | 2 / 6 | 15 / **21** | 20 / **21** | 20 / **21** |
| desfase −2, τ = 2 | 9 / 11 | 0 / 1 | 0 / 2 | 13 / 16 | 11 / 12 | 8 / 11 |
| desfase −2, τ = 3 | 14 / 14 | 1 / 4 | 1 / 6 | 19 / **21** | 16 / 16 | 12 / 16 |
| solo ventas (45) | 9 / 6 | 0 / 3 | 0 / 1 | 8 / 8 | 6 / 6 | 6 / 7 |
| solo compras (32) | 3 / 1 | 0 / 0 | 0 / 0 | 3 / 3 | 6 / 2 | 5 / 5 |
| compras restando el spread en T (32) | 2 / 7 | 0 / 0 | 0 / 0 | 5 / 8 | 2 / 7 | 4 / 4 |
| solo abril (35) | 4 / 3 | 0 / 2 | 0 / 1 | 4 / 5 | 7 / 5 | 7 / 6 |
| solo agosto (42) | 8 / 4 | 0 / 1 | 0 / 0 | 7 / 6 | 5 / 3 | 4 / 6 |

- **Ninguna sensibilidad lleva a ninguna regla al 40 %.** El máximo es 21 de 77 (27 %) con τ = 3.
- **El spread** de las compras en T tiene mediana 3 puntos (de 1 a 7). Restarlo mejora L1: R1 pasa
  de 1 a 7 de 32 y R4 de 3 a 8. En L0,8 el efecto es mixto: R4 sube de 3 a 5 y R5 baja de 6 a 2. Las compras salen peor que las ventas sin restarlo,
  como §1.5 pedía vigilar.
- **El desfase −2** favorece a R4 en L1 (de 11 a 16) y perjudica a R1 y R6 en L0,8.
- **R2 y R3 no describen al trader** en ninguna variante, como ya dijo `BLOQUE-DE-LA-CAJA.md`.

### 2.4 Lo que la medida sostiene y lo que no

- **Sostiene**:
  - que ninguna de las seis reglas, aplicada a la caja reconstruida desde el libro, explica la caja
    del trader en el 40 % de las operaciones;
  - que R2 y R3 quedan descartadas;
  - que el `initialSL` del libro casa más con el 1 de la caja de pantalla que con su 0,8 (3 de 5
    frente a 0 de 5).
- **No sostiene** que ninguna regla sea la del trader, ni que alguna de R1, R4, R5 y R6 quede
  descartada. El control dice que la reconstrucción y el anclaje en el llenado restan aciertos a
  todas. La medida que cerraría esto necesita la hora de colocación y el stop de pantalla, que el
  libro no trae.
- **Para la sesión 4**, lo que la medida afila:
  1. «¿El bloque es solo la última vela contraria o todo el tramo de contrarias?» (R1 o R4). R4 va
     por delante solo con el stop en el 1.
  2. «¿El stop que pones al colocar va en el 1 o en el 0,8?». El libro apunta al 1.
- **El control indica que el stop del libro es el inicial y está en el 1 de la caja.** Línea
  añadida en la revisión del consultor del 2026-09-30.

## 3. EXPLORATORIA: posterior a ver el resultado, y no cambia el veredicto (2026-09-30)

> **Esta sección se pidió en la revisión del consultor, DESPUÉS de ver §2.** No está en el criterio
> de §1 y no cambia el veredicto: NO DECIDE. Sirve para orientar la pregunta de la sesión 4, no para
> sostener ninguna regla.

Script: `scripts/caja_77_exploratoria.py`, que importa las piezas de `caja_77.py` sin tocarlo.
Salida: `CAJA-77-EXPLORATORIA.txt`. Se ensayó en un clon desechable y la salida del repositorio es
idéntica byte a byte.

### 3.1 «Solo el 0» (τ = 2, sin corrección)

Celda: «solo el 0» (el 0 a ≤ 2 puntos y el 1 no) / el 0 a ≤ 2 en total (aciertos más «solo el 0»):

| regla | ventas L0,8 | ventas L1 | compras L0,8 | compras L1 | todas L0,8 | todas L1 |
|---|---|---|---|---|---|---|
| R1 | 9 / 18 | 12 / 18 | 2 / 5 | 4 / 5 | 11 / 23 | 16 / 23 |
| R2 | 5 / 5 | 2 / 5 | 0 / 0 | 0 / 0 | 5 / 5 | 2 / 5 |
| R3 | 3 / 3 | 2 / 3 | 3 / 3 | 3 / 3 | 6 / 6 | 5 / 6 |
| R4 | 15 / 23 | 15 / 23 | 5 / 8 | 5 / 8 | 20 / 31 | 20 / 31 |
| R5 | 15 / 21 | 15 / 21 | 9 / 15 | 13 / 15 | 24 / 36 | 28 / 36 |
| R6 | 15 / 21 | 14 / 21 | 10 / 15 | 10 / 15 | 25 / 36 | 24 / 36 |

n: 45 ventas y 32 compras. **R5 y R6 dan el 0 en 36 de 77** (21 de 45 ventas y 15 de 32 compras),
y en la mayoría falla el 1: R5 da «solo el 0» en 24 (L0,8) o 28 (L1). **R1 da el 0 en 5 de 32
compras**, frente a 18 de 45 ventas.

### 3.2 Placebo del 0

Mismo T y mismas velas; el 0 del trader, la entrada, desplazado. «+» es hacia el stop y «−» hacia
la ruptura. Aciertos del 0 a ≤ 2 puntos, de 77:

| regla | −10 | −5 | **0 (la entrada real)** | +5 | +10 |
|---|---|---|---|---|---|
| R1 | 1 | 1 | **23** | 24 | 17 |
| R2 | 0 | 0 | **5** | 10 | 3 |
| R3 | 3 | 6 | **6** | 14 | 6 |
| R4 | 1 | 5 | **31** | 24 | 10 |
| R5 | 1 | 5 | **36** | 18 | 4 |
| R6 | 1 | 5 | **36** | 18 | 4 |

- **Hacia la ruptura, cualquier regla falla**: 0 a 6 aciertos. No dice nada de las reglas: su 0 sale
  de velas cerradas antes de la ruptura, y queda del lado del stop por construcción.
- **La comparación que vale es con +5 y +10.** Con el mismo sesgo de lado, R5 y R6 aciertan el doble
  en la entrada real que a 5 puntos (36 frente a 18) y nueve veces más que a 10 (36 frente a 4).
  **Su 0 localiza la entrada**, no solo «un nivel por encima».
- **R1 no la localiza**: acierta lo mismo en la entrada que a 5 puntos hacia el stop (23 frente a
  24). R4 está entre las dos (31 frente a 24). R2 y R3 aciertan más con el placebo que con la
  entrada.

### 3.3 R5: su pivote frente a la referencia del breaker del productor

Para cada operación:
- **la toma** es la de su sesión en el productor (en diagnóstico, como `scripts/embudo_77.py`: A-35
  `cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control`);
- **la referencia** es el último pivote contrario formado hasta la vela de la toma, incluida. Es
  `referencia_del_breaker`, el mismo que `Esquema.referencia` cuando hay esquema.
- «Mismo pivote» quiere decir mismo nivel y misma vela contraria.

| el pivote que da el 0 de R5 | operaciones | de ellas, con el 0 de R5 a ≤ 2 |
|---|---|---|
| **formado DESPUÉS de la toma** | **56** | 29 |
| el MISMO que la referencia | 5 | 2 |
| la toma es del lado contrario a la operación | 7 | |
| la toma de su sesión llega después de T | 6 | |
| sin toma del productor en su sesión | 3 | |
| **total** | 77 | 36 (5 de ellas sin toma útil) |

- Los minutos entre la vela contraria del pivote de R5 y la toma tienen **mediana +61**, de −7 a
  +199.
- En las 5 del mismo pivote, el pivote es de 1 a 7 minutos anterior a la toma.
- De las 56 «después», 13 tenían ya un esquema del productor antes de T y 43 no.

**Lo que dice, sin sostener nada:**
- el pivote cuya ruptura coincide con la entrada del trader casi nunca es la referencia que el
  productor fija en la toma;
- casi siempre es un pivote de M1 formado después, una hora de mediana;
- y es ahí donde R5 acierta el 0 (29 de 36).

Encaja con que la orden vaya en el último mínimo (en una venta) o máximo (en una compra) formado en
M1, y se mueva cuando se forma otro. Por eso esa pregunta pasa a la F de Next Action, para la
sesión 4.

## Estado

Criterio (§1) y nota del consultor (§1.8) commiteados y subidos antes de medir; medida hecha (§2);
parte exploratoria (§3) añadida tras la revisión del consultor. **Veredicto: NO DECIDE**, aceptado
por el consultor el 2026-09-30 tal cual; la pregunta del bloque, la del stop y la de la orden en
el último mínimo o máximo de M1 van a la sesión 4. Cerrada en `main` como
`stable/F36c-caja-77`.
