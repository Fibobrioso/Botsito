---
status: SUPERSEDED
date: 2026-09-29
phase: post-F14 (rama `trabajo/activar-sesion-03`)
---

# 0059 · A-42, PROVISIONAL: la ventana va en el reloj del gráfico, UTC+2 fijo, todo el año

> **CORRECCIÓN (2026-10-06, rama `trabajo/activacion-a42`, ADR-0069).** **SUPERSEDED por ADR-0069.** La lectura provisional de este ADR era la hipótesis H1 de
> `docs/validation/RELOJ-INVIERNO.md`: sesiones fijas en un reloj UTC+2 todo el año (en invierno,
> 05:00–13:00 UTC). La medida de enero la descarta (M2: el trader opera de 06:00 a 14:00 UTC; M3:
> el eje de su gráfico va en UTC+1 en enero), y el trader, en S-7 y por escrito el 2026-10-06,
> describió lo que solo predice H2b: las dos sesiones son las velas H4 de la rejilla de
> `anclaje_h4` que empiezan en ancla + 8 h y ancla + 12 h, y en su gráfico (Europe/Madrid) solo
> cambian las semanas en que Europa y EE. UU. no coinciden en el horario de verano. A-42 queda
> RESUELTA. Lo que este ADR tenía de mecanismo —separar el reloj de las sesiones del reloj del
> día de riesgo— lo hizo ADR-0063 y sigue en pie; `huso_operativa` no se ha movido.
>
> **PROVISIONAL, y SIN CAMBIAR NINGÚN VALOR TODAVÍA.** Decisión del consultor del 2026-09-29, tras
> revisar la sesión 3. El trader dijo «creo»: se confirma en la próxima sesión. A-42 sigue ABIERTA,
> y bloqueante, hasta entonces. `huso_operativa` NO cambia: en el motor ese parámetro es a la vez
> el reloj de las sesiones y el del día de riesgo, y cambiarlo rompe el segundo (§2). La
> separación de los dos relojes es rama de código, requisito previo de toda corrida de invierno.

## Decision

1. **La lectura PROVISIONAL de A-42: las sesiones de 07:00 a 11:00 y de 11:00 a 15:00 van fijas en
   el reloj del gráfico** (UTC+2 fijo, el de FX Replay; ADR-0039) todo el año. En verano coinciden
   con Madrid; **en invierno equivalen a 06:00–14:00 de Madrid**.
2. **`huso_operativa` no cambia en esta rama.** Se probó a pasarlo a `Etc/GMT-2` y el motor lo usa
   también como reloj del DÍA DE RIESGO, que tiene que dar la misma medianoche que el de FTMO
   (Europe/Prague, ADR-0053 §4): en invierno no la da, el cableado se niega a correr («no hay un solo
   reloj») y el corte del día del trader se movería a las 23:00. Aplicar la lectura exige
   **separar el reloj de las sesiones (gráfico, UTC+2 fijo) del reloj del día de riesgo (FTMO,
   Europe/Prague)**, que es código (`engine/motor.py`, `engine/simulacion.py`, la comprobación de
   `engine/cableado.py`): desalineación 9 de `docs/validation/ACTIVAR-SESION-03.md` §3, **requisito
   previo de cualquier corrida sobre meses de invierno, incluida fidelidad-dev**. Además, un cambio
   de un parámetro de `ejecucion` lo hace una decisión, no un registro de feedback (ADR-0004). La
   fuente de la lectura es la voz del trader en la sesión 3, **citada solo en su versión filtrada**:
   - `ev-v9-010753-063c8cb7`: «Entonces en invierno no empiezas a las 7 o a las 6 sería tu reloj,
     ¿no? Sí.»;
   - `ev-v9-010809-68e4ea44`: «lo adapto. O sea, automáticamente se adapta. La plataforma la
     adapta.»;
   - el tramo 1:06:38–1:07:51, que está en cuarentena y **solo se cita con máscara**
     (`docs/validation/SESION-03-EXTRACCION.md`, apartado de A-42), donde dice que en invierno «en
     lugar de 7 sería 6, y creo que eso sería invierno».
3. **A-42 sigue ABIERTA y bloqueante**, con la nota «el trader dijo "creo"; confirmar en la próxima
   sesión». Mientras siga abierta, la entrada de un mes de invierno desde el sorteo sigue parada
   (PARADA B0 de `ENTRADA-MARZO.md`): lo provisional no se congela en un sorteo.

## Problema que resuelve

A-42 pregunta con qué reloj cuenta el trader su horario de 07:00 a 15:00. ADR-0017 respondió que con
su reloj civil, que cambia con el horario de verano; pero su gráfico es UTC+2 fijo (ADR-0039), y las
dos lecturas solo se distinguen en invierno. En la sesión 3 el trader dice que en invierno empieza a
las 6 de su reloj y que la plataforma se adapta sola. Eso es lo que da la ventana fija en el reloj
del gráfico.

## Alternativas consideradas

1. Dejar la lectura fuera hasta que el trader la confirme sin «creo».
2. Pasar `huso_operativa` a `Etc/GMT-2` ya, y actualizar los tests que fijan el reloj civil.
3. Tomar la lectura como decisión PROVISIONAL, con A-42 abierta, sin cambiar `huso_operativa`
   hasta que una rama de código separe los dos relojes.

## Por que elegimos esta opcion

La 3 es la que el consultor eligió («opción (a)») tras ver lo que rompía la 2. Deja escrita la
lectura y su fuente, no toca el motor y mantiene A-42 en la hoja de la próxima sesión.

## Por que descartamos las demas

- La 1 pierde una respuesta del trader que desmiente ADR-0017 para el invierno.
- La 2, medida en la rama: 8 tests en rojo, y seis de ellos no por fijar la decisión anterior, sino
  porque el motor se niega a correr en invierno (`test_preparar_a44.py`, `test_perfil_cuenta.py`).

## Impacto

- `knowledge/spec/ambiguedades.yaml` (nota de A-42) y recuadro en ADR-0017. Ningún parámetro cambia.
- El motor sigue con la ventana en `Europe/Madrid`: en construcción (verano) coincide con la lectura
  nueva; en invierno no, y por eso ninguna corrida de invierno cuenta hasta la separación de relojes.
- Toda regla que cuelgue de la vela H4 sigue en la rejilla de `anclaje_h4`, que no se toca.

## Fecha / fase

2026-09-29 · post-F14, rama `trabajo/activar-sesion-03`.

## Estado

SUPERSEDED por ADR-0069 (2026-10-06)
