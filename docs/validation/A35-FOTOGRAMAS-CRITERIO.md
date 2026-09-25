# A-35, los fotogramas: el criterio, congelado antes de abrir ninguno

Rama `trabajo/a35-pivote-formado`, 2026-09-24. Sin merge, sin tag y sin push.

Este documento y `scripts/a35_fotogramas.py`, con su test (`tests/unit/test_a35_fotogramas.py`), se
commitean juntos y **antes** de abrir ningún fotograma. El script es la implementación exacta de la
lista cerrada y de la verificación: cambiarlo después de mirar es cambiar el criterio.

## 0. De dónde sale y qué se pregunta

- **La decisión del consultor**, sobre `A35-PIVOTE-FORMADO-CLASIFICACION.md`: A-35 no se decide
  todavía; primero se miden los fotogramas.
- **Lo firme**, por P4, P5, P6 y P9: el pivote lo marca **la vela contraria al flujo**, no un
  recuento de velas a cada lado.
- **Lo que no es firme:** **en qué momento de esa vela contraria** el pivote cuenta como formado.
  P9 dice «apenas se inicia», y P8 dice «ya formado».

He contrastado la lectura del consultor antes de escribir esto y no la refuto:
- el color de una vela en curso cambia hasta que cierra, porque es el signo del cierre menos la
  apertura;
- «voy marcando» (P9, #942) admite leerse como una marca provisional;
- P8 (#846) dice «Uno ya formado».

## 1. Medido contra el brief: ADR-0038 no tiene «registro de extracciones»

El brief pide abrir los fotogramas «con el procedimiento y el registro de extracciones que exige
ADR-0038, de forma que make check siga validando el registro». **ADR-0038 no define ningún
registro.** Su decisión 1 es de procedimiento: un fotograma se abre en un instante localizado de
antemano, nunca por muestreo. Su decisión 2 manda declarar el mismo día un agregado que aparezca.

Lo que sí existe, y es lo que se usa aquí, es la **cadena de F05**, con los tres mismos eslabones que
comprobó `scripts/v5_criterio.py` en V5-INSTANTES:
- el manifiesto commiteado de la extracción (`knowledge/corpus/fotogramas/fr-v3-982da728.yaml` y
  `fr-v4-9ad0ebb8.yaml`), inmutable, fija el `sha256_index`;
- el índice fija el sha de cada PNG;
- cada PNG se comprueba contra el índice antes de decodificarlo.

`make check` sigue validando los manifiestos (el contrato del historial de fotogramas), y el test del
script valida la lista cerrada y la verificación. El registro de lo abierto es la salida del script,
que se commitea tal cual con la medición.

## 2. Qué fotogramas: la lista cerrada

| pasaje | vídeo | segmentos | ventana | fotograma citado | localizado por |
|---|---|---|---|---|---|
| P4 | v3 | #976 | 1:15:40-1:15:59 | `fr-v3-982da728/4540000` | la transcripción, `ev-v3-011540-5425b533` y el cuestionario de la sesión 1, que ya cita ese fotograma |
| P5 | v4 | #461-#462 | 0:28:01-0:28:14 | `fr-v4-9ad0ebb8/1681000` | la transcripción y `ev-v4-002807-dd5f3718` (0:28:07) |
| P6 | v4 | #597-#601 | 0:35:07-0:35:24 | `fr-v4-9ad0ebb8/2116000` | la transcripción |
| P8 | v4 | #844-#849 | 0:50:44-0:50:56 | `fr-v4-9ad0ebb8/3048000` | la transcripción y `ev-v4-005053-885e2773` |
| P9 | v4 | #942 | 0:58:06-0:58:29 | `fr-v4-9ad0ebb8/3486000` | la transcripción y `ev-v4-005749-1e9325cb` |

**P4 y P5 entran**, porque ADR-0038 §1 lo permite:
> «**Un fotograma se abre SOLO en un instante localizado de antemano**: por la **transcripción**,
> por un **item de evidencia** que ya lo cite, o por una **marca de tiempo ya registrada**»

y
> «El **vecindario inmediato** de un instante ya citado cuenta como localizado»

Los dos están localizados por la transcripción y por un ítem de evidencia, y P4 además por un
fotograma ya citado.

**La ventana** de cada pasaje es la de sus segmentos en la cruda: un fotograma por segundo, de `t0`
a `t1`, los dos incluidos. Son 89 en total, y cualquier otro nombre se rechaza antes de leer un byte.

**Cuáles se abren:** el primero de cada ventana, y todos los que tengan algún píxel distinto del
anterior (la columna de la salida del script). Un fotograma sin ningún píxel distinto tiene el mismo
contenido que el anterior y se da por leído.

**Si alguno trae un agregado o una vista de Analytics,** se declara el mismo día en
`HOLDOUT-EXPOSICIONES.md` con sus cifras listadas, y ninguna se usa (ADR-0038 §2).

## 3. Qué se registra

Para cada pasaje se busca **el PRIMER fotograma de la ventana en el que aparece la marca o línea del
pivote**, es decir, la línea horizontal de la liquidez de M15 o la marca de la que habla el segmento.
En ese fotograma se registra:

- **(a)** la temporalidad visible;
- **(b)** si la vela que hace el extremo del flujo está cerrada;
- **(c)** si la vela contraria está en curso o cerrada;
- **(d)** si en ese momento la mecha de la vela contraria supera el extremo marcado;
- **(e)** a qué precio del extremo va la línea: mecha o cuerpo;
- **(f)** si más adelante, dentro de la ventana, la marca se mueve o se borra.

Y dos campos más, **añadidos antes de abrir nada** (§5):

- **(g)** si el gráfico avanza dentro de la ventana, es decir, si la vela de más a la derecha cambia
  de un fotograma a otro, o si es un gráfico histórico parado;
- **(h)** si la marca ya está presente en el primer fotograma de la ventana.

**Sin interpretar:** lo que no se lea con claridad se escribe «no legible». Cada campo cita su
fotograma y su marca de tiempo.

## 4. Qué contaría como respuesta (decisión del consultor)

- **«Formado al iniciarse la primera vela contraria»:** en todos los medidos, la marca aparece con
  la vela contraria en curso, en el extremo, y no se mueve después.
- **«Formado al cerrar la primera vela contraria»:** en todos, la marca aparece con la vela
  contraria ya cerrada.
- **No responde, y se pregunta al trader:** si los casos se contradicen, si alguno no se puede leer
  o si la marca se mueve.

## 5. Dos alternativas que la lista del consultor no tenía, añadidas ANTES de abrir nada

1. **El gráfico histórico parado, en (g).** Si el replay no avanza, todas las velas visibles están
   cerradas desde antes de dibujar. Entonces una vela contraria «cerrada» **no demuestra** que el
   trader esperase a su cierre, porque no había vela en curso que esperar.
   - Con el gráfico parado, (c) se registra como «cerrada (gráfico parado)».
   - **Ese caso no cuenta para la rama «al cerrar»**: cuenta como «no se puede leer el cuándo».
2. **La marca ya presente al empezar la ventana, en (h).** El momento en que se trazó no se ve.
   - (b)-(e) se registran igual en el primer fotograma.
   - **El caso cuenta como «no se puede leer el cuándo».**

**Y un caso de (a):** si la marca está en una temporalidad que no es M15, el caso no habla de A-35 y
**no se puede leer para M15**.

## 6. Qué no se hace

- No se abre ningún fotograma fuera de la lista.
- No se abre nada del material de septiembre; mayo y febrero no se tocan.
- No se decide A-35: la tabla del tercer commit pone cada caso frente al §4, y la decisión la toma
  el consultor.

## Estado

CRITERIO CONGELADO. No se ha abierto ningún fotograma.
