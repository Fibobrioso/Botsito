---
status: ACTIVE
date: 2026-10-12
phase: post-F14 (rama `trabajo/activar-sesion-04-motor`, R1.1 de la hoja de ruta)
---

# 0077 · La racha de pérdidas seguidas del trader: RN-036, aparte de RN-020, con cuatro parámetros (A-51 RESUELTA)

> Decisión del consultor del 2026-10-11 (respuesta a la PARADA de `trabajo/activar-sesion-04`,
> punto 6, y encargo de `trabajo/activar-sesion-04-motor`, decisión 4). Lo dijo el trader en la
> sesión 4, S-8; los cuatro parámetros son del trader, CONFIRMED vía `feedback apply`, y A-51
> queda RESUELTA con su RESOLVE_UNKNOWN. Lo que el trader no dijo va marcado como **lectura de la
> sesión** o **decisión del consultor**.

## Decision

### 1. Cuatro parámetros del trader, en el registro

| Parámetro | Valor | Lo que dijo (v10) |
|---|---|---|
| `racha_perdidas_max` | 9 | «como máximo una racha de pérdidas, una racha de nueve pérdidas, como máximo. Esto es por la condicional que nos da la cuenta de fondeo» (1:06:53, `ev-v10-010653-81316808`; ya en v9 1:11:28, `ev-v9-011128-a267338b`) |
| `racha_perdidas_corte` | `ganadora` (enum `[ganadora, ganadora_o_break_even]`) | «un break even no se cuenta como cartucho … no corta la racha como tal» (1:07:15, `ev-v10-010715-fae17215`) |
| `racha_perdidas_reinicio` | `nunca` (enum `[nunca, fin_de_dia, fin_de_semana]`) | «la racha sigue de un día a otro y una semana otra» (1:08:04, `ev-v10-010804-5b6ad1a3`) |
| `racha_perdidas_reanudacion` | `dia_siguiente` (enum `[dia_siguiente, semana_siguiente, sin_fecha]`) | «sería el día siguiente operaría» (el mismo ítem) |

Las 9 pérdidas vienen de una cuenta con un 0,5 % de riesgo por operación (SESION-04-EXTRACCION.md
§4.8: 9 × 0,5 % = 4,5 %, el tope del día de S-9), y el bot también arriesga un 0,5 %
(`riesgo_por_operacion`): la nota va en la descripción de `racha_perdidas_max`. Son del trader y de
categoría `estrategia`: cualquier cifra o enum distintos entran por un registro suyo. Las opciones
que no eligió están declaradas y SIN contrato en el motor (`engine/racha.py` se niega con ellas,
como `abrir_escenario` con una lectura sin contrato): nadie las inventa.

### 2. Lo que cuenta como pérdida: lo mismo que gasta un cartucho

Una pérdida de la racha es exactamente lo que las dos ramas de RN-016 cuentan como intento
gastado: un cierre en que saltó el stop, se activara como se activara, o una `perdida` de una
operación que vino de un esquema (`cartucho_criterio` = `solo_perdida`). La función es una sola,
`cuenta_como_perdida` (`engine/racha.py`), y `cartuchos` (`engine/primitivas_broker.py`) la usa
desde hoy: no hay dos definiciones. Un break even no cuenta ni corta; una ganadora pone la racha a
cero (`racha_perdidas_corte`).

### 3. RN-036, aparte de RN-020, con su acumulador y su hecho

- **`racha_perdidas`** (acumulador, `base: cartucho_criterio`, `reinicia_con:
  racha_perdidas_reinicio`): las pérdidas seguidas desde la última ganadora. Lo lleva
  `SeguidorRacha` (`engine/racha.py`), que PERSISTE entre días como la cuenta y el `SeguidorTope`
  (ADR-0053 §6: `EstadoDia` nace de cero cada día y no puede llevarlo), como atributo propio de
  `MotorCableado` -no dentro del `SeguidorTope`, que solo existe con A-44 fijada o en diagnóstico-
  y con la misma regla de `cuenta_diaria` (en diagnóstico, se reinicia cada día). RN-036 no lee
  ningún parámetro de A-44 y corre sin `--diagnostico-a44` (medido: `tests/unit/test_racha_perdidas.py`
  corre el cableado con `tope=None`).
- **RN-036** (gate): cuando `racha_perdidas` alcanza `racha_perdidas_max`, o mientras
  `detenido_por_racha` esté encendido, prohíbe `abrir_operacion`, fija `detenido_por_racha` a
  `hasta_el_dia_siguiente` y **retira la orden pendiente que quede** (`retirar_ordenes_pendientes`,
  acción nueva sin argumentos, idempotente: cancela lo que haya, cero o una). **Decisión del
  consultor:** se retira porque el broker la llenaría por ticks mientras el trader ya ha dejado de
  operar. Medido: dentro de la spec RN-011 solo coloca sin orden pendiente ni posición viva (el
  `ninguno_de` de su `cuando`, `strategy_spec.yaml`), así que una pendiente no convive con una
  posición y en el cierre de M1 en que cae la novena no queda ninguna; la acción es la red de
  seguridad que el consultor pidió, y `tests/unit/test_racha_perdidas.py` la ejercita directamente
  sobre un broker con una pendiente.
- **`detenido_por_racha`** (hecho de origen regla, valores `[hasta_el_dia_siguiente]`, producido y
  consumido por RN-036) dura lo que queda del día: `EstadoDia` muere con el día, y el acumulador
  vuelve a decir lo mismo mientras dure la detención.
- **RN-020 no cambia** (ni su prosa ni lo que hace con una orden pendiente, que es nada: heredado
  35, para cuando se active A-44).
  > **Enmendada por ADR-0086 (2026-10-26, `trabajo/activar-sesion-05-motor`).** Con A-44 activada
  > (sesión 5), RN-020 también retira la orden pendiente que quede al llegar al tope, con la misma
  > acción y el mismo motivo que RN-036: decisión del consultor; el heredado 35 queda hecho.

### 4. «Día siguiente» es el día operativo del reloj de las sesiones

El día se cuenta con `reloj_sesiones` (ADR-0063; `rejilla_h4` desde ADR-0069), no con el día civil
de `huso_operativa` ni con el corte de la firma: tras la novena no se opera más en ese día
operativo y se vuelve en la primera sesión del día operativo siguiente. Por qué: la ventana entera
(las dos velas H4) cae dentro de un día civil, así que «el día siguiente» del trader es el
siguiente día con ventana, y el único reloj que sabe qué instante pertenece a qué día operativo es
el de las sesiones (`RelojSesiones.lectura`). Un fin de semana no corta nada: la racha «sigue de
un día a otro y una semana otra».

### 5. LECTURA DE LA SESIÓN: qué vale la racha después de la novena

El trader dijo tres cosas que juntas no se escriben con un acumulador «≥ tope» y un reinicio
`nunca`: tras la novena no se opera más ese día, se vuelve al día siguiente, y la racha sigue de un
día a otro. Si la racha siguiera en 9 y el tope fuera «≥», RN-036 prohibiría para siempre hasta
una ganadora. La lectura que las hace valer a la vez, y que escribe `SeguidorRacha`:

- la **detención es del día operativo en que cayó la pérdida** que dejó la racha en el tope o por
  encima (`detenido_desde`), y `racha_perdidas` da SÍ contra `racha_perdidas_max` solo ese día;
- al día siguiente la racha **sigue en 9** (`reinicio` = `nunca`), la detención ha caducado
  (`reanudacion` = `dia_siguiente`) y se opera;
- la **siguiente pérdida -la décima- vuelve a detener** el día en que caiga, y así hasta que una
  ganadora ponga la racha a cero.

No es lo que el trader dijo palabra por palabra: es una lectura PROVISIONAL de la sesión, la que
hace caber a la vez las tres cosas que dijo. Hay otras (que la décima no detenga, o que la racha
se ponga a cero al reanudar): cada una es un parámetro más o un valor distinto de
`racha_perdidas_reinicio`, con su registro. La pregunta va a la lista de la sesión 5 (decisión
del consultor del 2026-10-12): «Después de parar por 9 pérdidas seguidas, cuando vuelves al día
siguiente: (a) empiezas a contar de cero; (b) sigues en 9 y una pérdida más te vuelve a parar ese
día; (c) otra, ¿cuál?».

> **Sustituida el 2026-10-26 (`trabajo/activar-sesion-05-motor`; sesión 5, S-21).** El trader
> contestó (a): «Pues al día siguiente Nuevamente en cero, o sea, se sigue continuando»
> (`ev-v16-002126-d2376f71`). `racha_perdidas_reinicio` pasa a `tras_la_detencion` por
> `fb-2026-10-23-sesion-05-978be13f` (CORRECT sobre el parámetro, que supersede al `nunca` de la
> sesión 4): tras parar, el día siguiente empieza en cero; mientras no se pare, la racha sigue de
> un día a otro (la sesión 4, con su reserva). `SeguidorRacha` lo hace: anota el día de la
> detención y pone la racha a cero en el primer instante del día operativo siguiente. A-51 sigue
> RESUELTA.

### 6. Lo que no cambia

RN-016 y `cartuchos` (solo comparten la definición de pérdida), RN-020, A-44 (ABIERTA, bloqueante),
`--diagnostico-a44` y `--diagnostico-a35`, el `SeguidorTope`, `engine/cuenta.py`.

## Problema que resuelve

A-51 nació de la respuesta de A-44 en la sesión 3 (el tope del trader son 9 pérdidas seguidas, no
un porcentaje) con dos huecos: qué corta la racha y cuándo se vuelve. El trader los cerró en la
sesión 4 (S-8) y RN-020 no podía escribirlos sin inventar.

## Alternativas consideradas

1. RN-036 aparte de RN-020, con cuatro parámetros y su acumulador (la elegida).
2. Una tercera rama en RN-020 (el acumulador `racha_perdidas` junto a `perdida_dia` y
   `perdida_semana`).
3. Contar la racha en `EstadoDia`, como los cartuchos.
4. Que la décima pérdida no detenga (la racha se «consume» al reanudar).

## Por que elegimos esta opcion

RN-020 es el tope porcentual (A-44, abierta) y lo lee el `SeguidorTope`; la racha es otra cosa del
trader, con otro reloj y sin A-44 detrás: mezclarlas ataría la racha a A-44. El acumulador persiste
porque la racha persiste.

## Por que descartamos las demas

- La 2 deja RN-036 bloqueada por A-44 (RN-020 sigue en `--diagnostico-a44`), contra el encargo.
- La 3 pone a cero la racha cada día (ADR-0053 §6), contra «la racha sigue de un día a otro».
- La 4 inventa un reinicio que el trader negó; queda como lectura alternativa en §5.

## Impacto

- **Registro:** `racha_perdidas_max`, `racha_perdidas_corte`, `racha_perdidas_reinicio`,
  `racha_perdidas_reanudacion` (CONFIRMED, fuente los registros de S-8); A-51 RESUELTA
  (`ambiguedades.yaml`, su fila sale de Known Ambiguities, `test_kit.py`: bloqueantes ABIERTAS
  quedan A-21, A-35 y A-44).
- **Spec:** RN-036; el acumulador `racha_perdidas`; el hecho `detenido_por_racha`; el token
  `hasta_el_dia_siguiente`; la acción `retirar_ordenes_pendientes`. `spec_version` 16.0.0 →
  **16.1.0**: una regla y cuatro parámetros nuevos.
- **Código:** `engine/racha.py` (nuevo); `engine/cableado.py` (el seguidor, su alimentación en
  cada cierre y la línea del informe de simulación); `engine/primitivas_broker.py` (el
  acumulador, la acción y `cartuchos` sobre `cuenta_como_perdida`); `engine/primitivas.py` (en el
  motor de la spec, sin broker, la racha es cero).
- **Tests:** `tests/unit/test_racha_perdidas.py` (nuevo): nueve pérdidas con un break even en
  medio detienen hasta el día siguiente; una ganadora a la octava la pone a cero; la racha cruza un
  fin de semana; la orden pendiente se retira; las opciones sin contrato se niegan; el cableado
  nueve días seguidos con el décimo operando otra vez.
- **Sin arnés ni medida sobre material.**

## Fecha / fase

2026-10-12 · rama `trabajo/activar-sesion-04-motor` (R1.1). Informe:
`docs/validation/ACTIVAR-SESION-04-MOTOR.md`.

## Estado

ACTIVE
