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

## Estado

Fase 1 (el criterio) escrita y commiteada, con la nota §1.8 del consultor añadida antes de medir.
La medida todavía no se ha hecho: no se ha leído ninguna fila ni cruzado ninguna vela.
