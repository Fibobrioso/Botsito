# Mayo `dev` ingerido · los primeros casos del proyecto, y el tercer mes contra A-18

Rama `trabajo/mayo-dev-ingerido`, 2026-09-22. Dos cosas que van juntas y no se mezclan:

- **A)** ingerir los 6 días `dev` de mayo: 6 `caso-*.yaml` con PRECIOS bajo
  `knowledge/cases/dev/`, los primeros del proyecto;
- **B)** repetir la medida del RR contra la predicción **congelada** en `F14A-INGESTA.md` §4, que no
  se ha tocado.

Antes de leer una sola fila de mayo, la rama tuvo que arreglar **seis cosas del mecanismo**, y eso
es la mayor parte de lo que hay aquí.

## 1. Línea base

`main` en `a1576d0`, limpio, igual a `origin/main`, `state check` OK. `kit check --sesion
2026-09-09-sesion-01` en OK, con 24 días reservados leídos por velas (8 / 8 / 8).
`docs/validation/PREREGISTRO.md` con blob `52649183…` y cero autorizaciones. `make check`: 774 verdes
y un rojo esperado (la rama todavía no estaba declarada en `PROJECT_STATE.md`).

## 2. La medida (B)

### El n, primero

- Filas de los 6 días `dev`: **19**.
- **Ganadoras: 5.** «Ganadora» = «tiene `maxTP`». `rPnL` **no se ha leído**. Es la misma definición
  que en agosto y abril, donde se midió que `maxTP` está si y solo si `rPnL > 0`.
- Las 5 tienen `initialSL`: **n = 5** para el RR. Ningún `maxTP` cae del lado de la pérdida.

### La distribución

RR implícito de `maxTP` sobre entrada-stop, a dos decimales:

```
2,90 · 3,05 · 3,30 · 3,46 · 3,57          mínimo 2,90 · máximo 3,57
```

**Es una sola distribución, y vale igual para los dos supervivientes de A-18**, `(riesgo_real, 0,8)`
y `(caja_completa, 1,0)`. El fichero no trae la caja, así que las dos bases dan el mismo número
**por construcción**.

| | mayo | agosto | abril |
|---|---|---|---|
| n (con `maxTP` e `initialSL`) | **5** | 18 | 15 |
| por debajo de 3,00 | **1** (2,90) | 1 (2,50) | 2 (2,57 y 2,94) |
| en la región [3,00 , 3,75) | **4** | 15 | 7 |
| ≥ 3,75 | **0** | 2 | 6 |
| exactamente en 3,00 | **0** | 3 | 3 |

Agosto viene de `F14A-INGESTA.md` §4 y abril de `ABRIL-Y-LA-CAJA.md` §2, los dos commiteados el
2026-09-21. **Esta rama no ha vuelto a leer esos libros para el RR.** El brief pedía medir abril
«con sus casos ya registrados». Abril no tiene casos ingeridos, y los casos no llevan `maxTP` por
diseño (ADR-0037 §7), así que desde los casos no se mide ningún RR. Lo medido de abril es su
informe, y se cita.

**La frase del consultor «tres ganadoras por debajo de 3R en agosto y abril» queda CONFIRMADA por
lo medido**: una en agosto más dos en abril. En la respuesta de esta sesión se escribió «2» para
abril sin enseñar la cuenta; aquí queda sustituido por lo medido.

### La lectura contra el criterio congelado

El criterio, literal, de `F14A-INGESTA.md` §4, escrito el 2026-09-21 antes de mirar mayo:

> ```
> REGIÓN DISCRIMINANTE: el RR implícito de maxTP sobre entrada-stop, en  [3,00 , 3,75)
>
>   base = riesgo_real    ->  la región está POBLADA, con suelo y moda en 3,00
>   base = caja_completa  ->  la región está VACÍA,   con suelo en 3,75
> ```
>
> | Lo que dé mayo | Qué se hace |
> |---|---|
> | Región **poblada** y suelo en 3,00 | Dos meses independientes diciendo lo mismo: **se decide A-18 hacia `riesgo_real`**, con su ADR y con el cambio del parámetro |
> | Región **vacía** y suelo en 3,75 | Los dos meses se contradicen: A-18 **se queda abierta y sube a `bloqueante: true`**, porque el material diciendo cosas distintas según el mes es peor que no saber |
> | Otra cosa | Se escribe lo que dé. **No se fuerza** |

Y su anotación, commiteada el mismo día y también antes de mirar mayo:

> Lo que la región poblada con suelo en 3,00 decide es que **la COMBINACIÓN CONFIRMED de hoy**
> —`caja_completa` con el stop a 0,8— **es falsa**. **NO elige entre los dos supervivientes:**
> `(riesgo_real, 0,8)` y `(caja_completa, 1,0)` predicen el mismo suelo.

Se aplica la primera fila leída con su anotación. La letra de la fila («se decide A-18 hacia
`riesgo_real` […] con el cambio del parámetro») y la anotación estaban en tensión desde que se
escribieron. Se sigue la anotación: se refuta la combinación y no se cambia ningún parámetro
(ADR-0040, decisión 4).

- **La región [3,00 , 3,75) está POBLADA: 4 de 5.** Aplica la primera rama. **(caja_completa,
  0,8) sigue refutada, ahora por un tercer mes independiente**, después de agosto y abril. **A-18
  no sube a bloqueante.**
- **Los dos supervivientes no se separan en mayo, y no podían separarse**: el fichero no trae la
  caja, así que las dos bases dan el mismo número por construcción. **Mayo no aporta evidencia
  sobre esa separación, ni a favor ni en contra.**
- **Por qué un n de 5 basta para esto, y para nada más.** La fuerza de la predicción no venía del
  tamaño: venía de que `caja_completa` con 0,8 predice la región **VACÍA**, y «vacía» es absoluto.
  Una sola fila dentro la refuta, y aquí hay cuatro. Lo contrario no sería cierto: con n = 5, una
  región «poblada» o una forma concreta de la distribución no se sostendrían como hecho.
- **El suelo.** «Suelo» es el límite inferior de la región (3,00 en una rama, 3,75 en la otra), no
  el mínimo de la distribución. El 2,90 queda fuera de la región y no cambia qué rama aplica.

**El ADR que la primera rama exige es ADR-0040** (`f88da0b`). Escribe lo refutado —la combinación
CONFIRMED `(caja_completa, 0,8)`, con el n y el recuento de cada mes— y el residuo abierto: los dos
supervivientes, y la condición que los separaría, que es un material que traiga la caja. No se
abre ni se pide nada. No cambia ningún parámetro, y el texto de A-18 no se ha tocado.

### La forma: observación descriptiva, no una hipótesis

- **Cero ganadoras exactamente en 3,00**, frente a 3 en agosto y 3 en abril. Con n = 5, **sin
  interpretación**. No estaba pre-registrada y **no se convierte en hipótesis**.
- **Nota para A-33** (*«tres ganadoras que cierran por debajo de 3R»*): mayo añade **una ganadora
  en 2,90**. **Sin atribuirle causa.** Con agosto y abril suman cuatro ganadoras por debajo de 3R
  en tres meses. Añadida al final de la `pregunta` de A-33, sin reescribir el texto que había
  (`0992c14`, con `docs/spec/ambiguedades.md` regenerado en el mismo commit).

## 3. Lo que se ingirió (A)

| día `dev` | casos | operaciones | forma |
|---|---|---|---|
| 2026-05-08 | 1 | 2 | 8/8 |
| 2026-05-12 | 1 | 1 | 8/8 |
| 2026-05-15 | 1 | 1 | 8/8 |
| 2026-05-18 | 1 | 3 | 8/8 |
| 2026-05-20 | 1 | 5 | 8/8 |
| 2026-05-28 | 1 | 5 | 8/8 |

- 19 filas leídas, todas de días pedidos. 17 operaciones. Las **2 filas sin `initialSL`** no
  producen caso y la ingesta las cuenta en su salida.
- `casos check` OK.
- Los ocho controles de forma: claves exactas en caso, en operación y en `fuente`; sin `objetivo`;
  sesión declarada; dirección válida; `fuente.sha256` = el del libro de mayo; ningún `maxTP` ni
  `idealTP`.
- Commit `1dfde42`, **solo** los 6 ficheros. Trailer `Fuente: ADR-0025, ADR-0037, ADR-0039`, y el
  sha del libro en una línea `Material:` del cuerpo.

**La puerta, sobre material real por primera vez.** `casos_reservados` da 34: 13 de mayo, 11 de
junio y 10 de septiembre. Con el libro de mayo se piden exactamente 2026-05-08, 12, 15, 18, 20 y
28: **6 pedidos, 0 reservados**. Esos días los deriva la puerta; nadie los elige.

## 4. Lo que hubo que arreglar antes de leer una fila

Cada punto, con su commit.

1. **`dias_ingeribles` devolvía 10 días, no 6** (`a3038d6`). Eran los 6 `dev` de mayo más los 4
   `fidelidad-dev` de septiembre, porque recorría los repartos de los dos caminos. Ahora:
   - el mes de un libro **se declara**: cada tramo de `cobertura_material` lleva el
     `material_sha256` de su libro, copiado del manifiesto del corpus;
   - `casos ingerir` pide solo los días de ese mes, y antes de leer una fila;
   - **solo toma días del camino del kit**: los de fidelidad se cuentan, no se nombran, y el mensaje
     cita Next Action.

   Paga la deuda «el mes del material se deduce de las filas». **La paga en parte**: la regla «mes
   pedido sin filas es error» sigue en pie, ya redundante, con su falso positivo, y queda en
   Technical Debt.

2. **Tests con dos repartos** (`61162cb`): un kit con dos meses y un reparto de fidelidad. Incluye
   el que convierte la obligación en mecanismo: el libro **correcto** de septiembre no mete ni un
   día de fidelidad.

3. **Ningún mensaje nombra una fila por su posición en el libro** (`37838c5`). Los contadores ya
   contaban solo filas pedidas, pero los errores decían «fila 12», y esa posición cuenta las filas
   de días no pedidos que van delante.

4. **El caso no lleva `objetivo`, y su forma es una lista cerrada en los tres niveles** (`9d5f94f`).
   Ver §5.

5. **La frontera de día UTC/Madrid** (`b657534`). Ver §5.

6. **Ningún libro se lee sin su formato y su huso declarados: ADR-0039** (`7e72d55`).
   - El libro de mayo viene **entero** en `AAAA-MM-DD HH:MM:SS`, no en el formato de agosto.
   - Se declara por libro, atado a su sha, en `knowledge/corpus/libros.yaml`. El registro es de
     solo añadir y se cruza con `cobertura_material`.
   - El huso se midió por velas: entrada dentro de la M1 ±2 puntos, contando cuántas filas caen
     dentro con cada huso. Solo sobre filas `dev` de mayo, y con dos controles de huso conocido:

     | libro | filas | UTC | Madrid |
     |---|---|---|---|
     | mayo | 19 (`dev`) | 19 | 0 |
     | agosto | 47 | 47 | 1 |
     | abril | 38 | 36 | 4 |

   - Las 2 filas de abril que caen fuera con UTC quedan como dato, sin interpretar.
   - Septiembre perdió su `material_sha256` (ver §5). Su tramo se queda y significa «hay material de
     este mes y este comando no lo lee».

7. **Un XML roto no publica su posición en la hoja** (`045664d`). El `ParseError` traía «column
   4913», una posición en la hoja entera.

Los cinco booleanos de estructura H1–H5, los seis H6–H11 y los siete del paso A (H12–H18) se
tomaron con los cuantificadores fijados antes de ejecutar, y solo salieron booleanos. Los detalles
están en la conversación de la rama. Lo que decidieron: el libro no usa `sharedStrings` y no tiene
celdas numéricas, y todas las fechas que no parseaban casan con un único formato, `AAAA-MM-DD`, con
el año delante.

## 5. Proceso: los hechos

- **El «falla cerrada» de la primera ingesta no lo produjo la puerta.** Fue la regla «mes pedido
  sin filas es error», protegiendo por coincidencia: el libro de mayo «no tenía filas de 2026-09».
  Arreglado en `a3038d6`.
- **Los tests de F14a enumeraban el caso que se pensó en vez de nombrar la condición**: montaban un
  solo reparto, y por eso no vieron que dos meses ingeribles dejaban el comando sin poder ingerir
  ninguno. **Patrón 3, en los tests.** Arreglado en `61162cb`.
- **La «mezcla de formatos» la dedujo el consultor de H3 y H10, que decían «alguna» y no «todas».**
  El libro de mayo viene entero en `AAAA-MM-DD`. Fue afirmar sobre la cadena habiendo mirado un
  eslabón, y **lo cazó el control del paso B al no encontrar ni una fila del formato viejo**. La
  sesión lo había repetido.
- **La fuga en la frontera de día UTC/Madrid del lector** (`b657534`). El lector comparaba la fecha
  UTC con días de Madrid, así que una fila de las 22–24 UTC de un día pedido, que en Madrid es el
  día siguiente, entraba como pedida, y su instante y sus precios podían salir en un error. **Es el
  huso otra vez, la tercera vez en dos días.** La regla de `CLAUDE.md` —fijar el huso de las dos
  fuentes antes de compararlas— no se aplicó porque el libro y el reparto parecían la misma cosa.
  **Abril y agosto no estaban afectados**: ninguna de sus filas cambia de día ni de mes entre UTC y
  Madrid, y todas caen entre las 05 y las 12 UTC.
- **`como_documento` escribía `objetivo`** (`9d5f94f`). ADR-0037 §7 y `F14A-INGESTA.md` decían que
  el caso no lleva ese campo, y el código escribía una clave `objetivo` con el texto «NO ES UN
  CAMPO». Se detectó midiendo la afirmación del brief antes de commitear los casos. Recuadro de
  corrección en los dos documentos. **Patrón 5, quinta instancia**, y la primera que no destapa un
  fallo.
- **El brief del consultor pedía el sha del libro en `Fuente:`, y el trailer solo admite `ev-*`,
  `fb-*` y `ADR-NNNN`** (`comun/ids.py`). Se resolvió con una línea `Material:` en el cuerpo del
  commit (`1dfde42`). **Otra instancia del patrón 5**: lo escrito y lo ejecutado se separan.
- **El sha de septiembre entró por un brief del consultor —«mayo, septiembre»— escrito sin
  anticipar ADR-0039.** La guardia del cruce lo cazó el mismo día que nació. Vuelve cuando
  septiembre tenga su brief **y** su medida en `libros.yaml`, las dos cosas a la vez.
- **Un fixture de F14a pasaba `fuente={"tipo": "prueba"}`**, que ya no cumple la lista cerrada. Se
  ajustó en `9d5f94f` y se dijo; no fijaba el defecto de `objetivo`. **Un test de esta misma
  rama** fijaba el formato «la fila pedida 1 (instante)», prohibido después; se ajustó en
  `b657534` y también se dijo.

## 6. La exposición

Declarada el mismo día en `HOLDOUT-EXPOSICIONES.md` (`708c7b1`). **Es la primera lectura de filas
de un libro que contiene días reservados**: agosto y abril tenían cero.

- **Lo leído:** los 6 días `dev`, cinco columnas (`dateStart`, `side`, `entryPrice`, `initialSL` y
  `maxTP`), ningún agregado.
- **Lo que se tocó de las filas reservadas:** su `dateStart` se parseó en memoria para saber de qué
  día era cada una, y de ahí solo salieron booleanos de estructura.
- **Qué garantiza que no salió nada de ellas:** la puerta, la frontera UTC/Madrid, los mensajes sin
  posición ni precios, los contadores de días pedidos y la guardia de la biblioteca.

## 7. Lo que NO se ha hecho, y dónde queda

- **Quitar la regla «mes pedido sin filas es error»**: queda en Technical Debt, pagada en parte.
- **Corregir `docs/runbooks/RITUAL.md`**, las ventanas de `state check`: **en su propia rama,
  después de mayo**. El «rama siguiente» de esa deuda se lee así. Mientras tanto sigue mandando la
  anulación de `PROJECT_STATE.md`.
- **El hook de pre-commit no cubre `libros.yaml`**: solo sabe de ficheros inmutables enteros. La
  garantía es `knowledge validate`.
- **El índice de ADRs de `PROJECT_STATE.md`** no tenía la entrada de ADR-0038 desde la rama
  anterior. Se añadió en esta rama, junto con ADR-0039 y ADR-0040. **Sigue teniendo ADR-0033 dos
  veces**, con dos redacciones distintas; no se ha tocado.
- Nada de septiembre se ha abierto, febrero no se ha tocado y marzo no existe para esta rama.

## 8. Cierre

`kit check --sesion 2026-09-09-sesion-01` idéntico a la línea base. PREREGISTRO con blob
`52649183…` y cero autorizaciones. `make check` en verde: 804 tests, 4 contratos de importación.

## Estado

WAITING_FOR_USER_VALIDATION
