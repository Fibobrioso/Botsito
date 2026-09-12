---
status: ACTIVE
date: 2026-09-10
phase: F11
---

# 0014 · La base sobre la que se mide el objetivo: `base_calculo_objetivo`

> **Enmienda (2026-09-11, ADR-0020).** Este ADR dice que la caja completa es tambien la distancia sobre la que se dimensiona el lote (`lotaje_base: distancia_completa`). **Eso ya no es cierto**: el acuerdo final del lotaje lo mide hasta `stop_fraccion_caja`. Lo que sigue vigente de este ADR es lo que decide de verdad: el OBJETIVO se mide sobre la caja completa.

## Decision

1. **El 1:3 se mide sobre la CAJA COMPLETA** (la distancia nivel 0 -> nivel 1), no sobre el riesgo
   que queda tras mover el stop. El objetivo se traza **con la orden**, junto al lotaje.
2. **Esa base deja de ser prosa y pasa a ser parametro**: `base_calculo_objetivo`, enum
   `caja_completa | riesgo_real`, `CONFIRMED` en `caja_completa`. Es la tercera base del registro,
   junto a `base_calculo_riesgo` y `base_calculo_perdida_diaria` (ADR-0012, punto 6).
3. **`objetivo_rr` no se renombra.** Renombrar rompe referencias del kit y de las ambiguedades
   (ADR-0012), y el paquete de la sesion 1 es prueba historica. Lo que cambia es su `unidad`, que
   deja de decir "multiplo del riesgo" -ambiguo- y nombra la base.
4. **A-18 queda ABIERTA**, no bloqueante: el valor entra `CONFIRMED` y la revision se ve por cruce,
   como fija ADR-0012 punto 3.
5. **El RR realizado es `objetivo_rr / stop_fraccion_caja` = 3,75:1**, y queda escrito en RN-015.
   No es un fallo del bot ni una desviacion de lo que dijo el trader: es la mecanica.

## Problema que resuelve

Tres sitios del repositorio decian cosas distintas sobre la misma cifra:

| Donde | Que decia |
|---|---|
| `parametros.yaml`, `unidad` de `objetivo_rr` | `multiplo del riesgo (1 a N)` |
| `fb-2026-09-09-sesion-01-7fbbb2e7`, `notas` | "el 1:3 expresado como multiplo del riesgo" |
| `strategy_spec.yaml`, RN-015 | "sobre la caja completa" |

Y "riesgo" tiene dos significados dentro de este mismo registro: el **nominal** (la caja completa,
sobre la que se dimensiona el lote, `lotaje_base: distancia_completa`) y el **real** (`0,8` de la
caja, donde acaba el stop). RN-012 dice explicitamente que no son el mismo numero y que la
diferencia es deliberada.

La diferencia entre las dos lecturas es **un 25 % de distancia al objetivo** (3,00 cajas frente a
2,40) y casi 4 puntos de win-rate de equilibrio (21,1 % frente a 25,0 %). Con `objetivo_rr` sin
ningun consumidor todavia en `src/`, el motor de F18-F23 tenia un 50 % de probabilidad de
implementar la lectura equivocada, y F26 habria medido con precision un bot que hace otra cosa.

## Alternativas consideradas

- **A. Medir el 1:3 sobre el riesgo real** (2,40 cajas).
- **B. Dejar la base en la prosa de RN-015** y corregir solo la `unidad` de `objetivo_rr`.
- **C. Renombrar `objetivo_rr`** a algo que no sugiera un ratio realizado.
- **D. Dejar `base_calculo_objetivo` UNKNOWN** hasta preguntarselo al trader en la sesion 2.

## Por que elegimos esta opcion

Porque es lo que dice la evidencia y lo que exige la mecanica de colocacion de la orden.

- **`ev-v2-003256-0197f4e1`** (v2 0:32:56, `PARAMETER`, confianza alta): *"Y al final, igual tienes
  planteado tu objetivo a 1 a 3"*, extraido como *"el objetivo sigue planteado a 1 a 3 aunque el
  stop se mueva a 0,75"*. **Mover el stop no mueve el objetivo.** Si el 1:3 se midiera contra el
  stop de proteccion, moverlo lo recalcularia.
- **La mecanica**: el movimiento del stop a `stop_fraccion_caja` ocurre DESPUES de la apertura
  (`fb-...-d34a0222`: *"todo SL se marca completo para el lotaje pero se reduce al 0.8 para la
  operativa"*). En el instante en que se traza el TP, la unica distancia que existe es la caja
  completa, que es tambien la que dimensiona el lote.
- **El consultor lo confirma** el 2026-09-10 con las mismas palabras: se traza un 1:3 inicial para
  el calculo del lotaje y, tras aperturar, el SL se mueve al 0,8; el resultado ya no es un 1:3
  realizado, y esa es la mecanica.

Que la base sea un **parametro** y no una frase es lo unico coherente con ADR-0002: la spec dice
que las reglas nombran parametros y que el valor vive en el registro. Una base de calculo escondida
en un adverbio de RN-015 es negocio viviendo en la prosa, que es la deuda declarada en el §8 del
informe de F11. Ademas es el patron que ADR-0012 ya aplico dos veces por el mismo motivo.

## Por que descartamos las demas

- **A**: contradice `ev-v2-003256` y obligaria a superseder ese item con un registro de feedback del
  trader, que no existe. Habria cambiado el sentido de RN-015 (bump mayor). El unico apoyo es
  `ev-v4-011951-5fb49e03` -*"si tengo 2 o 3 consecutivos perdidas pues uno tercero me lo puedo
  permitir"*-, que cuadra aritmeticamente mejor con 2,40 cajas (RR realizado exactamente 3,0), pero
  es una estimacion redonda hablando de margenes, no una descripcion del calculo. Queda anotado en
  las `notas` de RN-015 y en A-18 para que no reaparezca dentro de tres meses como un hallazgo.
- **B**: mas barato y deja el problema donde estaba. La prosa no la lee el motor.
- **C**: ADR-0012 avisa de que renombrar rompe referencias del kit y de las ambiguedades, y el
  paquete de la sesion 1 tiene que reproducirse. El nombre se queda; la `unidad` deja de mentir.
- **D**: `UNKNOWN` significa "leerlo falla", y una regla VIGENTE que nombra un parametro `UNKNOWN`
  es un error de `knowledge validate` -con razon-. Habria bloqueado RN-015 por una duda que la
  evidencia ya responde.

## Que sustituye de otros ADR

Nada. **Completa ADR-0012 punto 6**: la sesion 1 obligo a crear `base_calculo_riesgo` y
`base_calculo_perdida_diaria` porque "la diferencia se perdia porque ambos declaraban la misma
unidad". Es el mismo fallo en un tercer sitio, que entonces no se vio.

## Impacto

- El registro pasa de 51 a **52 parametros**: 46 con valor y 6 UNKNOWN. `spec_version` 1.4.1 ->
  **1.5.0** (menor: se anade un parametro).
- `spec status` saca `base_calculo_objetivo` y `objetivo_rr` en "corriendo con un valor que sigue en
  revision" por A-18.
- La descripcion de `objetivo_rr` deja de decir "fijo **y minimo**": ese "minimo" venia del corpus
  previo (`ev-v1-000414`, `ev-v3-003142`, `ev-v5-000456`) y la sesion 1 lo revoco al fijar
  `objetivo_extension_activa: false`. Era un residuo pre-sesion vivo dentro del parametro.
- Un test nuevo impide que la base vuelva a la prosa: toda regla vigente que nombre `objetivo_rr`
  tiene que nombrar tambien su base, y ningun `base_calculo_*` puede quedar sin regla que lo use.
- **Para F26**: el RR realizado de una operacion ganadora es 3,75:1, no 3:1. Un informe de fidelidad
  que compare 3,75 contra el "1:3" declarado y lo marque como desviacion estara midiendo mal.

## Fecha / fase

2026-09-10, F11 (auditoria previa a la validacion).

## Estado

ACTIVE
