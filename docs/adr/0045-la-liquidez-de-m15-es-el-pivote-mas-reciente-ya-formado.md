---
status: ACTIVE
date: 2026-09-24
phase: post-F14 (rama `trabajo/a24-a21-a26-a34`)
---

# 0045 · La liquidez de M15 es el pivote más reciente ya formado

## Decision

**A-24 queda DECIDIDA por el consultor:** de los pivotes de M15 candidatos, la liquidez que
cuenta es **el más reciente que ya esté formado**. Es la hipótesis (a) de
`docs/validation/A24-A21-A26-A34-CRITERIO.md` §1.

Es una decisión del consultor, no una respuesta del trader. A-24 queda **DECIDIDA**, no
RESUELTA (ADR-0022), y pasa a RESUELTA solo con un registro del trader que apunte a ella.

**Cuándo está formado un pivote de M15 no lo define la spec vigente**, y este ADR no lo inventa:
- se abre **A-35**, «cuándo un pivote de M15 está formado»;
- es bloqueante, y bloquea RN-004;
- no se sustituye por un parámetro provisional, porque es un mecanismo y no una cifra.

## Problema que resuelve

Nadie produce `liquidez_m15` en la spec, así que RN-004 no puede dispararse. El productor no se
podía escribir sin saber qué pivote de M15 marca el trader, y eso era A-24, abierta y
bloqueante. La búsqueda en transcripciones, con criterio congelado, da la respuesta que sigue.

## Por que elegimos esta opcion

Se aplica la regla global congelada (`A24-A21-A26-A34-CRITERIO.md` §2) a la clasificación de los
18 pasajes de A-24 (`docs/validation/A24-A21-A26-A34-CLASIFICACION.md`). Responde uno, y ninguno
responde en contra.

**Responde, (a).** v1, pasaje 3 (0:12:49-0:14:25), segmento #180:
> «la zona de liquidez tiene que ser la más reciente es una línea de liquidez que está aquí no aquí»

Enuncia la regla de forma general (`ev-v1-001334-96e8ca40`).

**Refuerzo.** v4, pasaje 16 (1:08:36-1:10:17), #1174-#1182:
> «Respecto a estructura / Siempre se respeta la estructura más reciente / Por ejemplo, imagina que
> hay / Un alto / O un máximo como zona de liquidez / De hace 2 o 3 días / Ese ahí no se toma en
> cuenta / Lo importante es los más próximos / Exacto»

Es una regla general, que por la forma enuncia el interlocutor y el trader confirma con «Exacto»
(`ev-v4-010921-31dd762d`). La cruda no separa hablantes. Por eso es refuerzo y no base.

**Acotación.** v4, pasaje 14 (0:49:15-0:51:03). La pregunta, #836:
> «cuando marcas la zona de liquidez en M15, ¿tomas el último pico que ya se formó del todo o
> simplemente el punto más alto de las últimas velas aunque sigan en curso?»

La respuesta, #846 y #849: «Uno ya formado» y «Por encima de este ya formado»
(`ev-v4-005053-885e2773`). El pivote tiene que estar formado, no en curso.

## Por qué no cuentan los demás pasajes

- **P5, v3, #142-#145.** Es el único que apunta a (b):
  > «como es un retroceso complejo, estaríamos marcando lo que sería / en este complex pullback
  > alcista, / que yo no suelo usar el término higher, bueno, higher hike, / hay pero el alto más
  > alto aquí alto más alto sería la liquidez esto es en m15 temporalidad de m15 ya»

  **No responde en sentido contrario porque en ese dibujo (a) y (b) señalan el mismo pivote.** Lo
  dice la nota de A-24 en `knowledge/spec/ambiguedades.yaml`, medida en pantalla antes de esta
  rama:
  > «El item de v3 0:12:42 (complex pullback, "el alto mas alto") se mide sobre un CROQUIS A MANO
  > en un grafico de 1h -fr-v3-982da728/781000-, y en ese dibujo el alto mas alto es ademas el
  > ultimo: no sostiene un criterio distinto, solo el mismo en otro ejemplo»

- **P6, v3, #162-#168.**
  > «tus zonas de liquidez, que sería / este alto, aunque yo invadiría / este alto, la verdad, o
  > sea, suelo usar / la zona, en este caso / la zona / de liquidez más baja, que me deja el precio
  > / que sería este de aquí»

  La frase aparta el alto más alto, así que va en contra de (b), pero **no separa (a) de (c)**:
  «suelo usar» sobre un ejemplo no es una regla. Además, la nota de A-24 dice que las dos veces
  que se midió en pantalla (este instante es el del fotograma `fr-v3-982da728/944000`) el pivote
  elegido era el mismo con las dos lecturas.

- **P9, v3, #480-#481.**
  > «Coge SM15 y marcas tu zona / de liquidez que tú consideres y ya. Esperar a que el precio
  > llegue.»

  **Su contexto es el objetivo, no la liquidez de entrada.** El segmento anterior, #479, dice:
  > «creo o más o menos para allí sale profe entonces es eso lo más objetivo es ponerlo a 13 y ver
  > qué»

  Es la frase de `ev-v3-003916-447dc8d7`, **el ítem que sostenía la hipótesis (c)**, la
  discrecional, y el riesgo de fidelidad que A-24 anotaba. Leído en su contexto, no la sostiene.

- **P1, v1, #33.**
  > «zona de liquidez en m15 entonces lo que yo voy a usar va a ser la zona de liquidez más reciente»

  Va a favor de (a), pero habla de ESTE caso («voy a usar»), no enuncia una regla. Por la regla
  común, una operación concreta no responde.

- **P15, v4, #930-#932.**
  > «Y me es indiferente, o sea, según el momento y la sesión, o sea, yo marco desde el punto
  > anterior, en este caso desde aquí, si lo cojo, marco desde aquí a aquí y hasta aquí.»

  Los «aquí» no tienen referente en el texto. «desde el punto anterior» cabe en (a) y «según el
  momento» en (c): vale para varias hipótesis y no responde.

Los demás pasajes de A-24 hablan de otra cosa: el TP, el lotaje, el stop o la cuenta de fondeo.

## Contraste con el trader

La decisión **se contrasta con la respuesta abierta del trader**, en el mensaje consolidado
pendiente.
- **Si la respuesta la confirma,** se registra como feedback que apunte a A-24, y A-24 pasa a
  RESUELTA.
- **Si la contradice,** un ADR nuevo sustituye a este.

## Alternativas consideradas

- Dejar A-24 abierta hasta que conteste el trader.
- (b), el más extremo.
- (c), discrecional.
- Definir aquí «formado».

## Por que descartamos las demas

- **Dejar A-24 abierta:** la regla global da respuesta por el corpus, y la pregunta sigue viva
  en el mensaje consolidado.
- **(b), el más extremo:** ningún pasaje responde a su favor. El único que apunta ahí (P5) es un
  dibujo en el que (a) y (b) coinciden.
- **(c), discrecional:** su único sostén (P9) resultó ser del TP.
- **Definir aquí «formado»,** por ejemplo con un número de velas a cada lado: sería una regla
  inventada que se haría pasar por el método del trader (la nota del token `liquidez_m15`). Se
  pregunta como A-35.

## Impacto

- **`ambiguedades.yaml`:**
  - A-24 pasa a DECIDIDA por este ADR y deja de ser bloqueante;
  - nace A-35, bloqueante;
  - A-21, A-26 y A-34 anotan que la búsqueda en transcripciones no respondió.
- **La spec (versión 12.2.1, parche de redacción):** las notas de RN-004 y del token
  `liquidez_m15` apuntan a este ADR y a A-35. **Ninguna regla ejecutable cambia:** RN-004 sigue
  sin poder dispararse, porque nadie produce `liquidez_m15`.
- **El siguiente paso no es el productor de RN-004,** que está bloqueado por A-35. Es buscar A-35
  en las transcripciones con el método congelado de A-24.

## Fecha / fase

2026-09-24, post-F14, rama `trabajo/a24-a21-a26-a34`.

## Estado

ACTIVE
