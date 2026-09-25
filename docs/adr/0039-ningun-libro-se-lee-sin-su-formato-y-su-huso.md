---
status: ACTIVE
date: 2026-09-22
phase: post-F14 (rama `trabajo/mayo-dev-ingerido`)
---

# 0039 · Ningún libro se lee sin su formato y su huso declarados

## Decision

1. **Ningún libro de backtest del trader se lee sin su formato y su huso declarados, atados a su
   sha y a la medida que los sostiene.** Las declaraciones viven en `knowledge/corpus/libros.yaml`,
   con el sha256 de los bytes del libro como clave. Cada entrada lleva una lista **cerrada** de
   lecturas `{formato, huso}`, la medida que las sostiene, la fecha y la fuente. El lector único
   (`corpus.libro`, ADR-0037) comprueba que los bytes dan el sha declarado y parsea cada fecha
   **solo** con las lecturas declaradas. Si una fecha no casa con ninguna, falla sin dar su valor
   ni su posición. **Nunca se prueban formatos hasta que uno parsee**: eso es aceptar un formato
   sin su huso.

   > **NOTA del 2026-09-24 (ADR-0046, no reescribe el cuerpo). Excepción acotada a este §1 para
   > el libro de marzo:** Aleks lee SOLO la columna de fechas, UNA vez, antes del sorteo y antes de
   > declarar el libro, y lo declara el mismo día en `HOLDOUT-EXPOSICIONES.md`. Nada más del fichero.
   > Resuelve la circularidad entre el §5 -el huso se mide con filas `dev`- y el sorteo, que necesita
   > el tramo de cobertura antes de que exista ningún `dev`.

2. **Los formatos salen de un vocabulario cerrado** (`corpus.libros.FORMATOS`), hoy de dos:
   `AAAA/MM/DD HH:MM:SS` y `AAAA-MM-DD HH:MM:SS`. No hay DD/MM ni MM/DD: el orden de un formato con
   día y mes intercambiables no se ha demostrado en ningún libro. Un formato nuevo entra en el
   vocabulario solo con su medida.

3. **El registro es SOLO AÑADIR**, como `knowledge/feedback/`. El sha fija los bytes, así que el
   formato y el huso de un libro no pueden cambiar nunca: una entrada commiteada no se edita ni se
   borra. `knowledge validate` lo comprueba versión a versión del fichero contra el historial y
   contra el árbol de trabajo. Si una declaración resulta estar mal, el libro deja de leerse hasta
   que otro ADR decida qué hacer.

4. **Los dos registros con la misma llave se cruzan.** Todo `material_sha256` de
   `cobertura_material`, que dice de QUÉ MES es un libro, tiene que existir en `libros.yaml`, que
   dice CÓMO SE LEE. Guardia en `knowledge validate`.

5. **EL PROCEDIMIENTO PARA DECLARAR UN LIBRO NUEVO**, validado el 2026-09-22:
   - el huso se mide **por velas**: la entrada de cada fila, dentro de
     `[mínima - 2, máxima + 2]` puntos de la vela M1 de Dukascopy de ese minuto, leyendo el
     instante con UTC y con el huso alternativo (hoy Europe/Madrid). Los 2 puntos son A-16: tres
     medidas OANDA frente a Dukascopy, entre 1 y 2 puntos;
   - solo sobre filas que se puedan leer; en un libro con días reservados, solo las de días `dev`
     **cuyo día sale igual con los dos husos**. De las demás sale como mucho un booleano;
   - **decide** si un huso da **>= 90 %** dentro **y** el otro **<= 50 %**. El 50 % importa tanto
     como el 90 %: si los dos salen altos, la prueba no distingue husos. Cualquier otra cosa es
     **NO CONCLUYENTE** y el libro no se declara;
   - con **CONTROL** sobre un libro cuyo huso ya se conoce, con el mismo método y el mismo umbral.
     Si el control no sale, el método no sirve.

## Problema que resuelve

El lector de F14a fijaba el formato (`AAAA/MM/DD HH:MM:SS`) y el huso (UTC) medidos sobre agosto, y
los aplicaba a **todos** los libros. Su propia docstring decía que «nada de eso se da por hecho
para el mes siguiente», y el mes siguiente lo rompió: el libro de mayo viene **entero** en
`AAAA-MM-DD HH:MM:SS`. Se detectó porque el lector falló cerrado («fecha ilegible»), no porque
nada lo comparara.

La salida fácil era añadir el segundo formato y probar los dos. Eso es aceptar un formato **sin
fijar antes su huso**, y el huso es justo lo que ha salido mal tres veces en dos días: el eje de
FX Replay supuesto UTC (es UTC+2 fijo), el `dateStart` de agosto, y la frontera de día UTC/Madrid
del propio lector, cerrada en la misma rama que este ADR.

## Alternativas consideradas

1. Añadir el formato de mayo al lector y probar los formatos en orden.
2. Declarar formato y huso en el tramo de `cobertura_material`, junto al `material_sha256`.
3. **Un registro propio, `knowledge/corpus/libros.yaml`, indexado por sha, solo añadir, cruzado
   con `cobertura_material`.**

## Por que elegimos esta opcion

- La llave es el **sha de los bytes**, que es lo único que identifica un libro sin leerlo. Un
  formato y un huso medidos sobre unos bytes valen para esos bytes y para ningunos otros.
- Cubre a **todos** los libros que se leen, estén o no en `cobertura_material`. Agosto y abril no
  están ahí a propósito: no se reparten en ningún universo. Pero se leen con el lector, y su
  lectura también tiene que estar declarada.
- Solo añadir es la consecuencia directa de que la llave sea el sha, no una disciplina aparte.

## Por que descartamos las demas

- **(1)** Es exactamente el error: un formato aceptado porque parsea, no porque se haya medido su
  huso. Además el orden de prueba se convierte en una decisión silenciosa.
- **(2)** Deja fuera a agosto y abril, que se leen y no están en `cobertura_material`, y reparte
  la regla en dos sitios. `cobertura_material` responde a otra pregunta (¿hay material de este
  mes?) y ya tiene su régimen.

## Impacto

- **Hoy deja fuera a ENERO y a SEPTIEMBRE, y es lo correcto**: nadie ha medido cómo se leen. El día
  que haga falta leer uno, se mide con el procedimiento de la decisión 5 y se declara.
- **Y con eso septiembre choca con la decisión 4**: su `material_sha256` ya está en
  `cobertura_material` (se puso en esta misma rama, antes de que existiera el registro) y no está
  en `libros.yaml`. Cómo se resuelve lo decide el consultor; queda escrito en
  `docs/validation/MAYO-DEV.md`.
- Declaraciones iniciales, todas en UTC: **agosto** `AAAA/MM/DD` (sesiones, F14A §4; velas 47/47
  frente a 1/47), **abril** `AAAA/MM/DD` (velas 36/38 frente a 4/38) y **mayo** `AAAA-MM-DD` (velas
  19/19 frente a 0/19, solo sobre filas `dev`, con agosto y abril como controles).
- El pre-commit no cubre `libros.yaml`: el hook solo sabe de inmutabilidad fichero a fichero. La
  garantía es `knowledge validate`, como dice ADR-0003 para todas las guardias de historial.

## Fecha / fase

2026-09-22, rama `trabajo/mayo-dev-ingerido`. Informe: `docs/validation/MAYO-DEV.md`.

## Estado

ACTIVE
