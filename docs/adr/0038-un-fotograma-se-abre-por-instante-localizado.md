---
status: ACTIVE
date: 2026-09-22
phase: post-F14 (rama `trabajo/la-caja-del-29-de-abril`)
---

# 0038 · Un fotograma se abre por instante localizado, nunca por muestreo

## Decision

1. **Un fotograma se abre SOLO en un instante localizado de antemano**: por la **transcripción**,
   por un **item de evidencia** que ya lo cite, o por una **marca de tiempo ya registrada**. **Nunca
   por muestreo.**

   El **vecindario inmediato** de un instante ya citado cuenta como localizado: abrir
   `0:04:40-0:05:00` de v5, alrededor de un fotograma que la evidencia ya cita, está dentro de la
   regla. **Esta regla existe para hacer seguro el trabajo, no para impedirlo**, y los fotogramas
   llevan infrautilizados desde la auditoría del 2026-09-13: la vía de localización es la
   transcripción, que además es mucho más barata que barrer imágenes.

2. **Si un fotograma abierto así resulta contener un AGREGADO o una vista de Analytics, se declara
   el MISMO DÍA** en `docs/validation/HOLDOUT-EXPOSICIONES.md` (ADR-0021 §4), **se listan las cifras
   vistas**, y **ninguna se usa** —ni en esa rama ni en ninguna posterior—. La lista existe para que
   un lector futuro pueda **comprobar** que no se usaron.

3. **La prohibición de las capturas de Analytics de `CLAUDE.md` es EN BLOQUE A PROPÓSITO, y el
   motivo se escribe aquí: el rango que cubre una captura NO SE PUEDE CONOCER ANTES DE ABRIRLA.**
   Se prohíbe la **clase** porque la **instancia** no se puede comprobar a tiempo.

   **UNA REGLA QUE ES GENERAL PORQUE LA COMPROBACIÓN NO LLEGA A TIEMPO NO ES EL PATRÓN 2**, y este
   ADR lo dice para que una corrección futura no la relaje. El patrón 2 —*una prohibición escrita
   más estricta que el ADR*— es una prohibición más estricta **sin motivo mecánico**; ésta **lo
   tiene**, y hoy se ha medido:

   > El descuido del 2026-09-22 cayó sobre un fotograma de v4 con la pestaña Analytics de **agosto**
   > —**cero días repartidos**, así que el agregado no contenía ningún día reservado—. **El mismo
   > muestreo sobre v1 o v2, que hablan de mayo y de julio, habría caído sobre un mes con días
   > reservados**, donde un agregado **no lo abre ninguna autorización** (ADR-0037 §1 y §3).

   Es la misma familia que la trampa del «15 de 18» que cerró la rama de abril: **no todo lo que
   parece necesitar corrección la necesita, y hay que saber QUÉ HACE una regla antes de tocarla.**

## Problema que resuelve

`CLAUDE.md` ya prohibía abrir las capturas de Analytics. Lo que no existía en ninguna parte es
**cómo se abre un fotograma**, y sin eso la prohibición es incumplible por construcción: **no se
puede saber qué hay en un PNG antes de abrirlo**. El 2026-09-22, muestreando fotogramas de v4 en
busca de un gráfico con leyenda OHLC legible para el control del reloj, se abrió
`data/fotogramas/v4/png-1fps/004800000.png` y resultó ser
`app.fxreplay.com/en-US/auth/testing/analytics-backtesting`.

**No fue un descuido puntual: era un riesgo estructural del método.** Abrir imágenes a ciegas en un
repositorio donde una clase entera de imágenes está prohibida es incompatible con la prohibición.

## Alternativas consideradas

1. **Dejarlo como aviso en el informe y en Technical Debt**, sin ADR.
2. **Prohibir abrir fotogramas de los vídeos que hablan de meses con días reservados.**
3. **Relajar la prohibición de las capturas de Analytics** cuando el mes no tenga días repartidos.
4. Un filtro automático que clasifique el PNG antes de enseñarlo.

## Por que elegimos esta opcion

**Porque la regla que faltaba es de PROCEDIMIENTO, no de contenido.** El contenido ya estaba
decidido —qué se puede mirar y qué no, ADR-0021, ADR-0033, ADR-0037—; lo que faltaba es **cómo se
llega a mirarlo**. Escribirlo como procedimiento deja intacto todo lo decidido y cierra el hueco por
el que se colaba.

Y porque **la vía de localización ya existe y está infrautilizada**: `CLAUDE.md` lleva desde el
2026-09-17 diciendo que hay 25.372 PNG y que sólo 8 fotogramas distintos están citados. La
transcripción localiza en segundos lo que barrer imágenes no encuentra.

## Por que descartamos las demas

- **(1) Sólo aviso**: el aviso no habría impedido la repetición. La regla que falta es la que se
  escribe, no la que se recuerda.
- **(2) Prohibir por vídeo**: sería el patrón 2 de verdad —más estricto sin motivo mecánico— y
  además **no funciona**: v4 habla de enero y de agosto y aun así trae Analytics dentro.
- **(3) Relajar por mes**: es exactamente lo que la decisión 3 prohíbe, y por el motivo que la
  decisión 3 nombra. **Que esta vez cayera sobre agosto fue suerte, no diseño.**
- **(4) Filtro automático**: clasificar la imagen exige leerla, que es lo que se quiere evitar, y
  además metería una dependencia de visión en un repositorio que evita hasta Pillow a propósito.

## Impacto

- **`CLAUDE.md` gana el PROCEDIMIENTO** en la sección de qué se puede mirar, escrito como
  procedimiento y no como prohibición nueva de contenido, citando este ADR y ADR-0021 §2.
- **No cambia ni una palabra** de ADR-0021, ADR-0033 ni ADR-0037: no toca qué se puede mirar.
- **La exposición del 2026-09-22 queda declarada** con sus cifras listadas y la cláusula de que
  ninguna se usa.
- **No cierra** el problema de fondo: los fotogramas siguen infrautilizados, y esta regla los hace
  más seguros de abrir pero no más fáciles de encontrar. La transcripción sigue siendo la única vía
  de localización.

## Fecha / fase

2026-09-22, rama `trabajo/la-caja-del-29-de-abril`. Informe:
`docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md`.

## Estado

ACTIVE
