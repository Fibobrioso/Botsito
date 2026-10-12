---
status: ACTIVE
date: 2026-10-12
phase: post-F14 (rama `trabajo/activar-sesion-04-motor`, R1.1 de la hoja de ruta)
---

# 0076 · «Limpia» es «sin alternancia de colores», y eso ya lo filtra RN-009: A-21 RESUELTA con `solo_una_zona_de_control`, sin opción nueva (enmienda ADR-0055 §2 y §5)

> Decisión del consultor del 2026-10-12 (respuesta a la PARADA de `trabajo/activar-sesion-04-motor`,
> punto 0), sobre la respuesta del trader en la sesión 4 (S-10). **Enmienda ADR-0055 §2** (el
> selector deja de ser PROVISIONAL: tiene valor) **y §5** (el rótulo `.a21=` y `--diagnostico-a21`
> se retiran; recuadro allí y fila del índice). El consultor **retira** la opción
> `sin_alternancia_de_colores` y la regla de la vela sin cuerpo que había decidido el 2026-10-11
> (encargo de la rama, decisión 3): se midió antes de añadir nada, y no hacía falta.

## Decision

### 1. Lo que dijo el trader

Una zona de control está limpia si no hay velas verdes y rojas alternándose antes de la ruptura
del posible punto de breaker, «y es solo eso»; el número de velas del retroceso no importa (sesión
4, S-10, v10 1:17:25–1:20:27): «¿una zona se limpia si hay velas verdes y rojas o terrenos rojos?
¿Es solo eso? Claro, exacto.» (`ev-v10-011725-3741e266`); «¿cuántas velas puede tener como máximo
el retroceso? … Eso es indiferente, no importa» (`ev-v10-011734-fedd3f8e`); «se alterna de una vela
verde a una vela roja, entonces ya allí ya quedaría invalidado … porque lo está haciendo antes de
la ruptura del posible punto de breaker» (`ev-v10-011957-7ebb3453`). Lo mismo había dicho en la
sesión 3 (v9 1:19:57, la lectura candidata escrita en la `pregunta` de A-21). Registro:
`fb-2026-10-04-sesion-04-22d08cbf` (RESOLVE_UNKNOWN sobre A-21) y
`fb-2026-10-04-sesion-04-48fb5817` (sobre `zona_control_limpia`).

### 2. Eso es lo que RN-009 ya filtra: medido, no razonado

En `domain/estructura_m1.py` cada paso de una vela contraria a una vela del color de la entrada,
después del primer impulso que sigue a la toma, forma un pivote de M1 en el sentido de la entrada
(`pivotes_formados` con `CIERRE_VELA_CONTRARIA`, `domain/pivotes_m15.py`), y `zonas_de_control` lo
cuenta como zona de control; el breaker de color de la entrada que sigue a una contraria forma
otra. Así, verde-roja-verde-roja antes de la ruptura son dos zonas o más, y
`zonas_control_max_por_esquema` = 1 (RN-009, «solo 1 zona control bro. si hay 2 se descarta»,
`fb-2026-09-09-sesion-01-1b2203b0`) las rechaza. **La tabla**, en compra y en venta (la venta es
la compra en espejo), con `detectar_esquema(…, MECHA, tope 1, solo_una_zona_de_control)` frente a
una comprobación literal de «ningún cambio de color en el retroceso» (desde la primera vela
contraria posterior al primer impulso hasta el bloque de origen incluido, saltando las de cuerpo
cero; solo como medida):

| serie (tras la toma) | lado | `detectar_esquema`, `solo_una_zona_de_control`, tope 1 | literal «sin alternancia» | |
|---|---|---|---|---|
| S-10: V, R, V, R y breaker V | compra / venta | None (2 zonas) | NO limpia (RVR / VRV) | igual |
| retroceso limpio de un solo bloque (R, R) y breaker V | compra / venta | segundo esquema (1 zona) | limpia (RR / VV) | igual |
| una zona de control y el último tramo limpio (V, R, V, breaker V) | compra / venta | segundo esquema (1 zona) | limpia (R / V) | igual |
| doble alternancia (V, R, V, R, V, R) y breaker V | compra / venta | None (3 zonas) | NO limpia (RVRVR / VRVRV) | igual |
| breaker contrario (R) que rompe con mecha, retroceso limpio (R, R) | compra / venta | primer esquema (0 zonas) | limpia (RRR / VVV) | igual |
| alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V | compra / venta | segundo esquema (1 zona) | NO limpia (RVR / VRV) | **DISTINTO** |
| breaker contrario (R) que rompe con mecha tras alternancia (R, V) | compra / venta | segundo esquema (1 zona) | NO limpia (RVR / VRV) | **DISTINTO** |

Las únicas diferencias salen de las series con una vela de cuerpo cero en medio (un doji no es de
ningún color, no es contraria y corta la racha: no forma pivote, `pivotes_m15.py`) y del breaker
contrario que rompe con la mecha (el bloque de origen es el propio breaker y la zona que forma la
alternancia anterior queda dentro del tope). Es el caso (b) de la respuesta del consultor: A-21 se
cierra con la opción que ya existe. Las series viven como tests
(`tests/unit/test_a21_series.py`), con la medida literal al lado.

### 3. Lo que se fija y lo que se retira

- `zona_control_limpia` = `solo_una_zona_de_control`, CONFIRMED vía `feedback apply` con el
  registro de S-10. El enum no gana ninguna opción; `LECTURAS_LIMPIA` sigue con sus dos lecturas.
- **Se retira `--diagnostico-a21`** (ADR-0055 §5 y su Impacto): la opción de la CLI, el campo
  `a21` de `Diagnostico` (`engine/diagnostico.py`), la rama hipotética de `lectura_limpia`
  (`engine/zonas.py`, que ahora lee solo el registro y sin valor se niega nombrando el parámetro,
  sin ofrecer diagnóstico), `ETIQUETA_A21`, `DiagnosticoDeZonaRechazadoError` y el rótulo `.a21=`.
  Los tres guiones que construían `Diagnostico` con `a21` por posición pasan a argumentos con
  nombre (`scripts/embudo_77.py`, cuyo `--a21` pasa a opcional y tiene que coincidir con el
  registro; `scripts/caja_77_exploratoria.py`, que se niega si el registro no trae la lectura con
  que midió; `scripts/orden_stop_o_limite.py`). Los cuatro guiones que recorren `LECTURAS_LIMPIA`
  no se tocan: recorren las mismas dos lecturas de siempre.
- **ADR-0055 §2** queda enmendado en lo que decía del selector PROVISIONAL («si la respuesta no
  calza en ninguna de las dos, se para»): la respuesta calza en la primera. **§5**, en el rótulo
  `.a21=`.
- A-21 RESUELTA por sus cinco sitios: el registro, `ambiguedades.yaml`, la hoja de preguntas (sale
  de `ORDEN_SESION_02` y de `ORDEN` de su test), `test_kit.py` (RESUELTAS y bloqueantes ABIERTAS,
  que quedan A-35 y A-44) y la tabla de Known Ambiguities; ninguna regla ni término del glosario la
  citaba, y se dice.

### 4. Lo que va a la sesión 5

Las dos series en que la lectura literal y el motor no coinciden, en el lenguaje del trader:

1. «En el retroceso antes de romper el punto de breaker, si en medio hay una vela sin cuerpo
   (abre y cierra en el mismo precio) entre una verde y una roja, ¿eso cuenta como alternancia y
   te invalida la entrada, o la vela sin cuerpo no cuenta y sigues? (a) cuenta como alternancia e
   invalida; (b) no cuenta, sigo como si no estuviera; (c) otra, ¿cuál?».
2. «Si la vela que rompe el punto de breaker es una vela contraria que lo pasa solo con la mecha,
   y antes hubo una verde y una roja alternadas, ¿la entrada vale o queda invalidada? (a) vale, la
   mecha rompe; (b) queda invalidada por la alternancia; (c) otra, ¿cuál?».

## Problema que resuelve

A-21 era bloqueante de RN-008/RN-011 desde el 2026-09-10 y el corpus no definía «limpia». El
trader la definió en la sesión 4; el encargo del 2026-10-11 iba a sumar una opción al enum con un
tramo que, medido, no filtraba nada, y la lectura alternativa de la sesión habría rechazado todo
esquema con dos zonas y dejado vacío el tramo en el caso típico (respuesta del consultor, punto
0).

## Alternativas consideradas

1. Cerrar A-21 con `solo_una_zona_de_control`, sin opción nueva, medido con series (la elegida).
2. Sumar `sin_alternancia_de_colores` al enum con el tramo del encargo (del bloque al breaker).
3. Sumar `sin_alternancia_de_colores` con el tramo del retroceso (la (a) de la PARADA).
4. Llevar A-21 entera a la sesión 5.

## Por que elegimos esta opcion

Porque lo que dijo el trader es lo que el motor ya hace, demostrado serie a serie, y lo que no
coincide son dos casos que él no describió y que se le preguntan.

## Por que descartamos las demas

- La 2 no filtra nunca (`bloque_de_origen` deja entre el bloque y el breaker solo velas del color
  de la entrada o sin cuerpo).
- La 3 rechazaría todo esquema con dos zonas o más -que RN-009 ya rechaza- y en el caso típico
  acota el tramo a la última zona, vacío; y decide por el trader en el doji y en el breaker por
  mecha.
- La 4 deja A-21 bloqueante con la respuesta ya dada.

## Impacto

- **Registro:** `zona_control_limpia` CONFIRMED (`fb-2026-10-04-sesion-04-48fb5817`), descripción
  nueva; A-21 RESUELTA con sus tres ítems de v10 y el párrafo de la respuesta. `spec_version`
  17.0.1 → **17.0.2** (cambia un valor).
- **Código:** `engine/diagnostico.py`, `engine/zonas.py`, `cli.py` (sin `--diagnostico-a21`),
  los tres guiones. Ningún cambio en `domain/estructura_m1.py`.
- **Docs:** recuadro en ADR-0055 y sus filas del índice; nota al principio de
  `docs/runbooks/ACTIVAR-A35-A44.md` §6.
- **Tests:** `tests/unit/test_a21_series.py` (nuevo, la tabla); los que congelaban «sin fijar» y
  el diagnóstico cambian de sentido a propósito (`test_preparar_a21.py`); los que pasaban
  `--diagnostico-a21` o esperaban `.a21=` en un nombre lo pierden (`test_preparar_a35.py`,
  `test_visor.py`, `test_renovar_cierres.py`, `test_rutas_windows.py`,
  `test_selector_orden_stop.py`, `test_cableado.py`); `test_hoja_preguntas.py`, `test_kit.py`.
  Con el código de `main`, `lectura_limpia(registro)` levanta `SinLecturaDeZonaError`.
- **Sin arnés y sin material**: series sintéticas.

## Fecha / fase

2026-10-12 · rama `trabajo/activar-sesion-04-motor` (R1.1). Informe:
`docs/validation/ACTIVAR-SESION-04-MOTOR.md`.

## Estado

ACTIVE
