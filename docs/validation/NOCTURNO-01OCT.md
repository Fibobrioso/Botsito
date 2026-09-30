# La noche del 30 de septiembre al 1 de octubre: F32, F33, F34 y F36

Rama `trabajo/nocturno-01oct` (sesión autónoma, desde `14e01bc`), revisada como
`feature/nocturno-01oct`: la misma rama con `main` (`df5edf9`, `stable/F31d-ci-linux-memoria`)
traído en `8d73cae`, con la CI de Linux en verde (run 36738817150). La base de este informe es
`docs/nocturno/INFORME-01oct.md`, que queda como estaba y tiene el detalle de la noche; su §0 (la CI
de `main` en rojo) ya no vale: la arregló `stable/F31d-ci-linux-memoria`.

## 1. Qué entra

| Funcionalidad | Commit | `spec_version` | ADR |
|---|---|---|---|
| F32 · el sesgo con doble ruptura lo decide el color; RN-002 cierra antes del fin de la vela H4 | `6698426` | 14.0.0 | ADR-0060 |
| F33 · cada sesión es un escenario propio: `liquidez_tomada` caduca al abrir la sesión | `bf1dc0b` | 14.1.0 | — (A-46 RESUELTA; ADR-0055 §4) |
| F34 (1 de 2) · el stop se redondea alejándose de la entrada; el break even de RN-014 | `2cca34d` | 14.2.0 | ADR-0061 |
| F34 (2 de 2) · la toma de RN-004 la hace una vela de M1 | `2763ceb` | 14.3.0 | ADR-0062 |
| F36 · el reloj de las sesiones se separa del reloj del día de riesgo | `fad0305` | 14.4.0 | ADR-0063 |
| Decisiones del consultor (este informe) | commit de la revisión | 14.4.1 | — |

De paso, dos errores que ya estaban, arreglados con su test en `bf1dc0b`: una orden preparada y no
enviada se arrastraba a la zona siguiente, y `scripts/embudo_77.py` no corría desde que A-47 se fijó.

## 2. Lo medido (en DIAGNÓSTICO, sobre construcción)

Abril y agosto de 2026: 42 días `dev`, 84 sesiones, 77 operaciones del trader, por la compuerta y
con A-35, A-44, A-21 y A-27 en diagnóstico. **Ninguna cifra cuenta como medida de fidelidad**, y
ninguna corrida tocó mayo, marzo, febrero ni septiembre. No se abrió nada nuevo, así que no hay
exposición que declarar (INFORME-01oct §2).

| | antes | tras F32 | tras F33 | tras F34 (1 de 2) | tras F34 (2 de 2) | tras F36 |
|---|---|---|---|---|---|---|
| Sesiones que RN-033 prohíbe por sesgo ambiguo (de 84) | 15 | 0 | 0 | 0 | 0 | 0 |
| Operaciones puntuables del bot | 6 | 5 | 8 | 8 | 2 | 2 |
| Cobertura: operaciones del trader que el bot iguala (de 77) | 2 | 2 | 2 | 2 | **0** | 0 |

**F34 (2 de 2) es la única pieza que empeora las cifras**: con la toma en M1 el productor encuentra
menos esquemas y la cobertura baja de 2 a 0 de 77 (ADR-0062 §3, razonado leyendo el código, no
medido). **Entra igualmente, por decisión del consultor**: la lectura la eligió el trader (A-45
RESUELTA), y lo que falta es la vida de la orden stop y la caja por operación.

## 3. Decisiones del consultor (2026-09-30)

1. **ADR-0060, ADR-0061, ADR-0062 y ADR-0063: ACEPTADOS.** Sin recuadro ni marca PROPUESTO en el
   título; su `## Estado` lo dice. **ADR-0061 enmienda ADR-0029 §3** para el redondeo del stop:
   la distancia a la entrada se redondea siempre alejándose de ella; el objetivo y el lote siguen
   con ADR-0029.
2. **`2763ceb` (la toma en M1) entra**, tal cual.
3. **Las 14 decisiones de interpretación de INFORME-01oct §4 quedan aceptadas.** La 8 —«lo mínimo
   posible» es un punto y no un pip entero (ADR-0061 §2)— queda además como pregunta para la sesión 4.
4. **Citas.** RN-002 cita `fb-2026-09-29-sesion-03-c38c4aef` y RN-003
   `fb-2026-09-29-sesion-03-31fb311f`, con el literal exacto de cada registro; la cita anterior de
   cada una pasa a sus notas, porque sigue sosteniendo una parte de la regla (el cierre en
   `ventana_fin` y la ruptura de un solo extremo). Los dos dejan de salir en `botsito feedback
   pending`. **RN-033 no cambia de forma ni de cita**: sus notas dicen que es una guardia del
   proyecto para los dos casos que el trader no describió —la doble ruptura sin cuerpo y la falta de
   ruptura dentro de `sesgo_h4_tope_velas`—, con ADR-0044 y ADR-0060. Por eso su CORRECT de la
   sesión 3 (`fb-2026-09-29-sesion-03-1168f036`, «siempre va a haber un sesgo») **sigue saliendo en
   `feedback pending`**, y es lo esperado: la regla no hace lo que ese registro dice.
   Las guardias de la spec (`comprobar_contra`, `comprobar_literales`, `comprobar_citas_revocadas`)
   lo admiten: `botsito spec check` da OK.
5. `spec_version` 14.4.0 → **14.4.1**, PARCHE: solo cambian citas y redacción, ninguna forma.
   `docs/spec/` regenerado.

## 4. Lo que sigue bloqueado

- **F35, la vida de la orden stop**: en qué precio nace la orden y con qué caja (A-48, A-49). Pasa a
  depender de la medición pre-registrada de R1 a R6 (`PROJECT_STATE.md`, Next Action C y D).
- **La caja por operación** (ADR-0056 §4): detrás de F35.
- **RN-007**: falta el umbral de «casi plana», para la sesión 4.
- **F37, el calendario de cierres de mercado**: sin fuente en el repositorio, y R15 frente a R6 sin
  respuesta de FTMO.

## Estado

VALIDADA por el consultor el 2026-09-30, con orden de cierre en `main` como
`stable/F36-nocturno-01oct`.
