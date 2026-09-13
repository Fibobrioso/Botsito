---
status: ACTIVE
date: 2026-09-12
phase: post-F13
---

# 0024 · La ventana no se amplía a Nueva York, y la referencia para medir es Dukascopy

## Decision

1. **A-15 queda DECIDIDA: la ventana operativa del bot es 07-11 y 11-15, y no se amplía a Nueva
   York en esta fase.** `ventana_inicio` = 07:00 y `ventana_fin` = 15:00 (Europe/Madrid) se quedan
   como están.
2. **La capacidad se conserva**: ampliar es cambiar dos parámetros del registro, no reescribir
   nada. El día que haya material grabado de Nueva York, se reabre con evidencia y se cambia.
3. **A-16 se parte en dos**, porque hoy mezcla una decisión con una medición y solo una de las dos
   la puede cerrar el consultor:
   - **A-16** se queda con la **MEDICIÓN** —cuánto se separan las velas de Oanda (FX Replay, donde
     el trader decide) de las de Dukascopy (donde el bot se mide)— y sigue **ABIERTA**, con
     `resuelve_en: F26`.
   - **A-23** nace con la **DECISIÓN de método** y queda **DECIDIDA** por este ADR.
4. **A-23: la referencia para medir fidelidad es Dukascopy** (ADR-0005). MT5/FundedNext se usa
   para lo que sí aporta —spread real, condiciones de ejecución, reloj de servidor y paridad con
   Strategy Tester— y **la divergencia entre proveedores entra en F26 como margen declarado**, no
   como ruido ignorado.

## Problema que resuelve

Son dos preguntas que llevaban **abiertas y decididas a la vez desde el 2026-09-09**. Las dos las
decide el consultor y no el trader, y hasta ADR-0022 no existía forma de cerrarlas: el fichero de
ambigüedades solo admitía cerrarlas con un registro del trader. Con el estado `DECIDIDA` ya
existiendo, dejarlas abiertas tiene un coste inmediato y mecánico: **`cuestionario.py` mete toda
`ABIERTA` en el cuestionario de la sesión siguiente**, así que el próximo `kit build` le volvería a
preguntar al trader lo que ya está decidido.

**A-15.** El trader no se reservó esta decisión: la delegó, y con esas palabras. Preguntado por
ampliar a Nueva York respondió *"Por ahora vamos a trabajarlo en esas dos sesiones. Aunque si
quieres incluir Nueva York como te digo, pues lo puedes hacer. O sea, por mí no hay problema"*
(`ev-v6-014610-597e442a`) y *"como te digo, bro, puedes buscar las operaciones donde sea, o sea, no
hay problema"* (`ev-v6-014623-f23c5f63`). Una pregunta que el trader devuelve no se cierra
esperando su respuesta.

**A-16.** Su pregunta literal es *"¿cómo se comparan decisiones tomadas sobre velas de Oanda (FX
Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milésima?"*. El
anexo del 2026-09-09 (`docs/validation/anexos/A-16-proveedor-de-datos-2026-09-09.md`) midió una
pareja **distinta**: MT5/FundedNext contra Dukascopy, 2 puntos de mediana una vez corregido el
reloj de servidor. El propio anexo lo dice sin ambigüedad: *"Queda una tercera fuente en juego, que
es la del trader: él backtestea en FX Replay, que usa datos de Oanda. Esta medición no la cubre."*

Cerrar A-16 con ese anexo sería afirmar más de lo que la evidencia sostiene, que es justo lo que
este proyecto no hace.

## Impacto

- **El cuestionario de la sesión 2 pierde dos preguntas** que no son del trader. A-16 sigue dentro
  porque la medición sigue pendiente, pero ya no arrastra la decisión.
- **`spec status` deja de enseñar `ventana_inicio` y `ventana_fin` como "corriendo con un valor en
  revisión"**: los dos están CONFIRMED con el registro de la sesión 1, y lo que los ponía ahí era
  A-15.
- **F26 hereda una obligación explícita y legible por máquina**, no una frase en un ADR: A-16
  sigue ABIERTA con `resuelve_en: F26`, así que la medición de la divergencia Oanda/Dukascopy no
  se puede olvidar sin que se note.
- **El universo de casos de F14 no cambia**: se sigue construyendo sobre las dos sesiones, que es
  sobre lo que están calculados los días de mayo.

## Alternativas consideradas

1. **Cerrar A-15 y partir A-16** (elegida).
2. **Cerrar las dos enteras** con el anexo del 2026-09-09.
3. **Dejar las dos abiertas** hasta la sesión 2 y preguntárselas al trader.
4. **Cerrar A-15 y dejar A-16 entera abierta.**

## Por que elegimos esta opcion

Porque separa lo que se decide de lo que se mide, que es la única forma de cerrar A-16 sin mentir.
La decisión de método —qué proveedor es la referencia— está tomada y sostenida por una medición
real; la comparación con la fuente del trader **no está medida** y no la puede cerrar una decisión.
Es el mismo corte que ADR-0022 hizo con A-17 tres días antes, y por el mismo motivo.

Y A-15 es más simple de lo que parecía: no hay nada que preguntar, porque ya se preguntó y el
trader devolvió la pelota. Toda su operativa **grabada** va de 07:00 a 15:00; ampliar a Nueva York
sin una sola sesión grabada allí metería en el universo de etiquetado días cuyo comportamiento
nadie ha visto, y cambiaría el sesgo H4 de la mitad de ellos.

## Por que descartamos las demas

- **(2) Cerrar las dos enteras**: el anexo no mide lo que A-16 pregunta. Cerrarla con él dejaría la
  obligación de medir la divergencia Oanda/Dukascopy dentro de la prosa de este ADR, que es
  exactamente donde el aviso de RN-021 sobre las noticias vivió tres días sin que ninguna guardia
  lo mirara (ADR-0022).
- **(3) Dejarlas abiertas hasta la sesión 2**: gasta dos preguntas de una sesión cara en cosas que
  el trader ya ha dicho que no decide él. El tiempo con el trader es el recurso más escaso del
  proyecto.
- **(4) Dejar A-16 entera abierta**: conserva el problema —la decisión de método seguiría sin
  registrarse en ninguna parte— y sigue llevándola al cuestionario.

## Fecha / fase

2026-09-12, después de cerrar F13 (que construyó el mecanismo `DECIDIDA` y dejó explícitamente
fuera de su alcance usarlo sobre A-15 y A-16: brief de F13 §4).

## Estado

ACTIVE
