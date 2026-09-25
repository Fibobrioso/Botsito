# A-35, los fotogramas: el resultado frente al criterio

Rama `trabajo/a35-pivote-formado`, 2026-09-24. Sin merge, sin tag y sin push.

Se pone la medición de `A35-FOTOGRAMAS-MEDICION.md` (commit `6702a82`) frente al §4 y al §5 de
`A35-FOTOGRAMAS-CRITERIO.md` (commit `14ed54e`), sin cambiar ninguno de los dos.

## La tabla

| pasaje | temporalidad | ¿se lee el cuándo? | por qué | «al iniciarse» | «al cerrar» |
|---|---|---|---|---|---|
| P4 (v3 1:15:40-1:15:59) | — | **no** | no hay gráfico: los 20 fotogramas son el cuestionario en Word | no | no |
| P5 (v4 0:28:01-0:28:14) | 1m | **no** | la temporalidad no es M15 (§5), y **la marca se mueve** (f): 1.19715 → 1.19720 → 1.19739 | no | no |
| P6 (v4 0:35:07-0:35:24) | 15m | **no** | la marca ya está al empezar la ventana (h), y el replay está parado (g): la contraria sale «cerrada (gráfico parado)», que no cuenta para «al cerrar» (§5.1) | no | no |
| P8 (v4 0:50:44-0:50:56) | 15m | **no** | lo mismo que P6: (h) y (g) | no | no |
| P9 (v4 0:58:06-0:58:29) | 15m | **no** | lo mismo que P6: (h) y (g) | no | no |

**Frente al §4:**
- **«Formado al iniciarse la primera vela contraria»:** ningún caso muestra la marca con la vela
  contraria en curso. **No se cumple.**
- **«Formado al cerrar la primera vela contraria»:** en ningún caso se ve la marca aparecer con la
  contraria recién cerrada. Donde la contraria sale cerrada es porque el gráfico está parado.
  **No se cumple.**
- **Tercera rama:** alguno no se puede leer (todos) y la marca se mueve (P5). **Se cumple.**

## Decisión del consultor

**Se cumple la tercera rama: A-35 no responde, se pregunta al trader y sigue bloqueante.**

**Los motivos, por pasaje:**
- **P4:** no hay gráfico.
- **P5:** está en M1, y la marca se mueve.
- **P6, P8 y P9:** la marca es anterior a la ventana y el replay está parado.

**Lo que sí consta como evidencia, sin decidirse:**
- P4, P5, P6 y P9 coinciden en que el pivote lo marca **la vela contraria al flujo**. En P4 y P5 lo
  dice la transcripción, porque sus fotogramas no enseñan un M15. En P6 y P9 lo dicen la
  transcripción y la pantalla.
- P4 rechaza expresamente el recuento de velas a cada lado (v3 #975, «yo puedo poner cuántas velas
  a cada lado y invalidar un máximo y decir, pues, yo lo que hago es mapear de tal manera la
  estructura»).

**Una observación descriptiva, sin interpretarla:** en P5 (M1), la marca pasa de 1.19715 a 1.19720
y luego a 1.19739, es decir, **del cuerpo a las mechas**.

**La pregunta para el trader**, abierta y sin sugerir respuestas:

> «Cuando marcas un alto o un bajo en M15 como liquidez, ¿en qué momento lo das por bueno? ¿Y qué
> haces si después el precio lo supera un poco?»

**Lo que esta rama no cambia:** RN-004 sigue bloqueada, con A-21 y A-35 bloqueantes a la espera del
trader.

> **CORRECCIÓN del 2026-09-25 (rama `trabajo/sesion-02`).** A-21 no bloquea RN-004. Nació en
> ADR-0019 (commit `d264912`, 2026-09-10) y se reformuló el mismo día a «qué es una zona de control
> "limpia, sin ruido". Es lo único de la geometría de entrada que sigue siendo cualitativo»: la zona
> de control del esquema de entrada en M1, que es RN-008. Su evidencia es de ese esquema
> (`ev-v1-001435-f0586d02`, «cuando se desarrolle esta zona de control que no haga mucho ruido»;
> `ev-v4-000243-5f8875ce`; `ev-v3-004201-bfeb3734`), y RN-004 solo cita A-24, DECIDIDA, y A-35. La
> frase de arriba copió la de `PROJECT_STATE.md`, que entró sin fuente en `0901d2c`. **RN-004 queda
> bloqueada solo por A-35.** El cuerpo no se toca.

## Estado

CERRADA PARA EL RITUAL. A-35 sin respuesta en transcripciones ni en fotogramas, y a la reunión con el
trader.
