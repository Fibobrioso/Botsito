---
status: ACTIVE
date: 2026-09-22
phase: post-F14 (rama `trabajo/mayo-dev-ingerido`)
---

# 0040 · La combinación CONFIRMED del objetivo es falsa, y los dos supervivientes siguen abiertos

## Decision

1. **La combinación `(base_calculo_objetivo = caja_completa, stop_fraccion_caja = 0,8)` queda
   REFUTADA** por tres meses independientes. Esa combinación predice que el RR implícito de `maxTP`
   sobre entrada-stop cae **fuera** de la región `[3,00 , 3,75)`, con suelo en 3,75
   (`objetivo_rr / stop_fraccion_caja = 3 / 0,8`). Los tres meses tienen la región **poblada**:

   | mes | n (ganadoras con `maxTP` e `initialSL`) | en `[3,00 , 3,75)` | medido en |
   |---|---|---|---|
   | agosto | 18 | 15 | `F14A-INGESTA.md` §4 (2026-09-21) |
   | abril | 15 | 7 | `ABRIL-Y-LA-CAJA.md` §2 (2026-09-21) |
   | mayo | 5 | 4 | `MAYO-DEV.md` §2 (2026-09-22), solo los 6 días `dev` |

   «Ganadora» es «tiene `maxTP`», con la misma definición en los tres meses. La fuerza no viene del
   tamaño: la combinación refutada predice la región **VACÍA**, y «vacía» es absoluto. Una fila
   dentro basta, y hay 26 en 38.

2. **Siguen ABIERTOS los dos supervivientes**, que predicen la misma región poblada con suelo en
   3,00:
   - `(riesgo_real, 0,8)`: el objetivo se mide sobre la distancia hasta el stop, y el stop está a
     0,8 de la caja;
   - `(caja_completa, 1,0)`: el objetivo se mide sobre la caja entera, y el stop está en su borde.

   **Mayo no puede separarlos, por construcción**: el fichero no trae la caja, así que las dos
   bases dan el mismo número. Mayo no aporta evidencia sobre esa separación, ni a favor ni en
   contra. **Lo que los separaría es un material que traiga la caja.** Este ADR solo nombra esa
   condición: no abre ni pide nada.

3. **A-18 sigue ABIERTA y NO sube a `bloqueante: true`.** Esa subida era la segunda rama del
   criterio (región vacía), y no es la que ha salido.

4. **No se cambia ningún parámetro.** Refutada la combinación, al menos uno de los dos valores
   CONFIRMED es falso: `base_calculo_objetivo` (si rige `riesgo_real`) o `stop_fraccion_caja` (si
   rige `1,0`). Cambiar uno de los dos sería elegir superviviente, y eso es justo lo que el material
   no permite. Los dos siguen en el registro con su valor y su fuente, **y desde hoy se sabe que no
   pueden ser ciertos los dos a la vez**.

## El criterio congelado, literal

Escrito en `docs/validation/F14A-INGESTA.md` §4 el 2026-09-21, antes de mirar mayo:

> ```
> REGIÓN DISCRIMINANTE: el RR implícito de maxTP sobre entrada-stop, en  [3,00 , 3,75)
>
>   base = riesgo_real    ->  la región está POBLADA, con suelo y moda en 3,00
>   base = caja_completa  ->  la región está VACÍA,   con suelo en 3,75
> ```
>
> **EL CRITERIO, y no se toca después de mirar:**
>
> | Lo que dé mayo | Qué se hace |
> |---|---|
> | Región **poblada** y suelo en 3,00 | Dos meses independientes diciendo lo mismo: **se decide A-18 hacia `riesgo_real`**, con su ADR y con el cambio del parámetro |
> | Región **vacía** y suelo en 3,75 | Los dos meses se contradicen: A-18 **se queda abierta y sube a `bloqueante: true`**, porque el material diciendo cosas distintas según el mes es peor que no saber |
> | Otra cosa | Se escribe lo que dé. **No se fuerza** |

Y su anotación, commiteada el mismo 2026-09-21 en `trabajo/abril-y-la-caja`, también antes de mirar
mayo:

> Lo que la región poblada con suelo en 3,00 decide es que **la COMBINACIÓN CONFIRMED de hoy**
> —`caja_completa` con el stop a 0,8— **es falsa**. **NO elige entre los dos supervivientes:**
> `(riesgo_real, 0,8)` y `(caja_completa, 1,0)` predicen el mismo suelo. Elegir entre ellos exige
> la medida de la caja, y la medida de la caja exige la serie de precios del trader, que no es la
> nuestra (**A-16**, medida por primera vez el 2026-09-21).

**Este ADR aplica la primera fila leída con su anotación.** La letra de la fila —«se decide A-18
hacia `riesgo_real` […] con el cambio del parámetro»— y la anotación estaban en tensión desde que
se escribieron, y la anotación lo dice. Se sigue la anotación, que es la lectura que el consultor
fijó antes de mirar: se refuta la combinación y **no** se cambia el parámetro (decisión 4).

**«Suelo» es el límite inferior de la región**: 3,00 en una rama y 3,75 en la otra. **No es el
mínimo de la distribución.** El 2,90 de mayo queda fuera de la región y no cambia qué rama aplica.

## Problema que resuelve

Desde F11 la spec lleva como CONFIRMED dos parámetros cuya combinación predice un RR realizado de
3,75 sobre entrada-stop. `knowledge/spec/strategy_spec.yaml` ya lo avisaba sin haberlo contrastado:
*«El RR REALIZADO sigue siendo `objetivo_rr / stop_fraccion_caja`»*. Tres meses de material del
trader dicen que no: el RR se concentra entre 3,00 y 3,75. Sin un ADR, ese hallazgo quedaba repartido
en tres informes y ningún documento que mande decía que la combinación es falsa.

## Alternativas consideradas

1. Decidir A-18 hacia `riesgo_real` y cambiar `base_calculo_objetivo`, como dice la letra de la
   primera fila del criterio.
2. Cambiar `stop_fraccion_caja` a 1,0.
3. **Declarar refutada la combinación, dejar abiertos los dos supervivientes y no tocar ningún
   parámetro.**

## Por que elegimos esta opcion

Es lo único que el material sostiene. La refutación es sólida porque se apoya en una región que
tenía que estar vacía. La elección entre supervivientes no tiene ninguna medida detrás: la medida
de la caja sobre abril salió NO CONCLUYENTE (`ABRIL-Y-LA-CAJA.md` §R2; `LA-CAJA-DEL-29-DE-ABRIL.md`),
y ningún backtest trae la caja.

## Por que descartamos las demas

- **(1)** Elige la lectura cómoda. `(caja_completa, 1,0)` predice exactamente lo mismo, y la propia
  anotación del criterio lo dejó escrito antes de mirar.
- **(2)** El mismo error en el otro sentido. Además `stop_fraccion_caja` = 0,8 tiene apoyo propio:
  la plantilla de dibujo del trader lleva el 0,8 en línea propia (`LA-CAJA-DEL-29-DE-ABRIL.md`),
  aunque eso no demuestra dónde pone el stop en cada operación.

## Impacto

- **La spec tiene dos parámetros CONFIRMED que no pueden ser ciertos los dos a la vez.** Un bot
  construido hoy con ellos apuntaría a un RR realizado de 3,75, y el material dice 3,00. Quien mida
  fidelidad en F26 tiene que leer esta diferencia como **conocida**, no como un fallo del bot. Y no
  puede darla por resuelta.
- A-18 conserva su `pregunta` y su estado. Este ADR no la cierra: `DECIDIDA` exigiría decidir
  (ADR-0022), y aquí no se decide la base.
- La condición para separar a los supervivientes queda nombrada: **un material que traiga la
  caja**. No se abre ni se pide nada por este ADR.

## Fecha / fase

2026-09-22, rama `trabajo/mayo-dev-ingerido`. Informe: `docs/validation/MAYO-DEV.md`.

## Estado

ACTIVE
