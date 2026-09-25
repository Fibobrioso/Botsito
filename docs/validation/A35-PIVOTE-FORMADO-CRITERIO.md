# A-35 en las transcripciones: el criterio, congelado antes de buscar

Rama `trabajo/a35-pivote-formado`, 2026-09-24. Sin merge, sin tag y sin push.

Este documento y la lista `TERMINOS_A35` de `scripts/buscar_ambiguedades.py` se commitean juntos y
**antes** de ejecutar la búsqueda. El script es la implementación exacta de este documento: cambiarlo
después de ver la salida es cambiar el criterio.

Es el **mismo método que A-24** (`A24-A21-A26-A34-CRITERIO.md`), con la misma normalización, la
misma ventana y el mismo corte. A-35 va en un conjunto aparte (`--conjunto a35`) para que la salida
de A-24, A-21, A-26 y A-34 se siga reproduciendo. Regeneradas fuera del repositorio, esa salida y la
de A-18 salen **idénticas byte a byte** a las commiteadas. Sus tests siguen en verde, y A-35 lleva
test propio (`tests/unit/test_buscar_a35.py`).

## 0. El alcance

Las mismas cinco transcripciones vigentes de v1 a v5. Solo se lee la cruda, verificada contra el
`sha256_cruda` de su manifiesto.

Quedan fuera:
- **v6**, porque su día está retirado (ADR-0041);
- **las heredadas y las sustituidas.**

No se abre nada más del corpus.

## 1. La pregunta

A-35, tal como está en `knowledge/spec/ambiguedades.yaml`: **cuándo un pivote de M15 está formado.**

ADR-0045 decide que la liquidez de M15 es el pivote más reciente **ya formado**. Se apoya en v4 #846,
«Uno ya formado», y #849, «Por encima de este ya formado» (`ev-v4-005053-885e2773`), pero no dice
cuándo un pivote lo está.

**Hipótesis: ABIERTA**, como A-21 y A-34 en la búsqueda de A-24. Las opciones que nombra la pregunta
del yaml no son una lista cerrada, sino ejemplos de lo que sería una regla:
- cuando cierra la vela que hace el alto o el bajo;
- cuando cierra la vela contraria que lo deja atrás;
- otra cosa.

## 2. Las clases de cada pasaje

- **RESPONDE:** el pasaje enuncia **de forma general** cuándo un pivote está formado, o cuándo un
  alto o un bajo cuenta como marcado. La frase literal tiene que decirlo; no basta con inferirlo.
- **DUDA:** el pasaje apunta a una regla, pero no la enuncia en general. Puede ser una operación
  concreta, una frase que valga para varias reglas, un deíctico («aquí», «este») que solo se
  resuelve con el gráfico, o una regla que puede ser de otra cosa (la marca del pivote frente a su
  formación). Se anota la duda. **Para la regla global, una DUDA no responde.**
- **NO RESPONDE:** el pasaje habla de otra cosa (la operación en curso, el cierre de un trade, el
  stop, el TP...).

**Si la respuesta depende de un gráfico**, se anota el fotograma más cercano (`botsito corpus
frames show`) y si ya estaba medido, es decir, citado en un ítem de evidencia o en la spec. **Aquí no
se abre ningún fotograma:** la clasificación se hace con el texto (ADR-0038).

## 3. La regla global

**Si hay pasajes que RESPONDEN en sentidos opuestos, o ninguno responde, se pregunta al trader.** La
aplica el consultor, no esta rama.

## 4. Los términos, lista cerrada

Solo frases o combinaciones de dos o más palabras. Queda prohibida cualquier palabra suelta de uso
constante: liquidez, zona, M15, H4, sesgo, vela y pivote. Un test lo comprueba.

La búsqueda no distingue mayúsculas ni tildes, y casa por palabra o por frase.

- **La formación:** ya formado · ya formada · ya formados · ya se formó · ya se ha formado · se ha
  formado · se formó · se forme · está formado · esté formado · formado del todo · se termine de
  formar · termina de formarse
- **Lo que aún no está formado:** en curso
- **El cierre de la vela:** vela cerrada · velas cerradas · cierre de la vela · cierra la vela · la
  vela cierra · esperar el cierre · espero el cierre · ya cerró
- **Cómo se marca el alto o el bajo:** vela contraria · velas contrarias · marca un mínimo · marca
  un máximo · marca un alto · marca un bajo · máximo estructural · mínimo estructural · a cada
  lado · cuántas velas

**No se añade ni se quita ningún término después de ver resultados.**

## 5. La ventana y el corte

Los mismos que en A-24:
- **ventana** de ±45 s alrededor de cada coincidencia, uniendo las que se solapan;
- **corte**: un pasaje mide como mucho **180 s**, y una unión más larga se corta en pasajes
  consecutivos contados desde su inicio;
- **cada trozo** lista sus propias coincidencias, y un trozo sin coincidencias propias no se emite.

## 6. El control positivo

Tienen que aparecer en la salida las dos frases que sostienen la acotación de ADR-0045:
- v4 #846, «Uno ya formado»;
- v4 #849, «Por encima de este ya formado» (`ev-v4-005053-885e2773`).

**Si falta alguna, se para.** Un test comprueba que casan con la lista, y también la pregunta de
v4 #836 («¿tomas el último pico que ya se formó del todo … aunque sigan en curso?»).

## 7. La salida y la clasificación

- **Una sola ejecución**, con la salida tal cual en `A35-PIVOTE-FORMADO-SALIDA.txt`, en su propio
  commit.
- **Después, la clasificación**, en su propio commit. Cada pasaje lleva:
  - su clase;
  - la frase literal, comprobada por script contra su pasaje;
  - la referencia de vídeo y de segmento;
  - el fotograma, cuando dependa de un gráfico.

## Estado

CRITERIO CONGELADO. La búsqueda no se ha ejecutado.
