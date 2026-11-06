---
status: ACTIVE
date: 2026-11-05
phase: post-F14 (rama `trabajo/activar-sesion-06-motor`, R4.2 de la hoja de ruta)
---

# 0089 · El tope del trader se reinicia de sesión en sesión: en la apertura de la primera sesión del día siguiente (enmienda ADR-0053 §3.3 y §9)

> Decisión del consultor del 2026-11-05 (encargo de `trabajo/activar-sesion-06-motor`, fase 1),
> sobre lo que el trader dijo en la sesión 6 (S-2). **Enmienda ADR-0053 §3.3 y §9** (el reloj del
> reinicio del tope propio del trader, que allí era la medianoche del huso de reinicio y, sin él,
> el corte del perfil marcado SUPUESTO), con recuadros fechados allí y su fila del índice. El
> número 0087 sigue reservado (`PROJECT_STATE.md`, Technical Debt): este se numera 0089.

## Decision

### 1. Lo que dijo el trader

- `ev-v17-000250-a468bcec` (v17 0:02:50-0:03:15): «La respuesta es la C, la primera sesión del día
  siguiente, ya que de esa manera pues nosotros, o sea, cada día por lo general estamos trabajando
  dos sesiones que están planteadas, entonces si en esas dos sesiones se llega al 4.5 obviamente se
  detiene, pero al día siguiente a la primera sesión nuevamente después seguimos operando.»
- `ev-v17-000351-331daa6d` (v17 0:03:51-0:04:00): «Si paro un viernes, pues se vuelve a contar desde
  cero el día lunes. Exactamente, o sea, siempre es de sesión en sesión».

No es una medianoche, y no cabe en `perdida_trader_reinicio_huso` (un huso IANA cuya medianoche
corta): por eso la sesión 6 la dejó «en parte» por falta de opción, no por la respuesta
(`SESION-06-EXTRACCION.md`, tabla final, S-2, regla general «sí»).

### 2. El parámetro nuevo

`perdida_trader_reinicio` (estrategia, enum), con dos opciones:

- `medianoche_huso`: lo de antes. El conteo del día vuelve a empezar en cada medianoche de
  `perdida_trader_reinicio_huso` (y, sin él, del huso de corte del perfil, marcado SUPUESTO), y el
  de la semana en la del lunes.
- `primera_sesion_dia_siguiente`: el conteo del día vuelve a empezar en la apertura de la primera
  sesión del día siguiente CON ACTIVIDAD, con el saldo de ese instante; el de la semana, en la
  apertura de la primera sesión del primer día de la semana con actividad (el lunes, o el siguiente
  si el lunes no tiene sesiones). Un viernes no corta el sábado ni el domingo: corta el lunes al
  abrir. No usa ningún huso.

Nace UNKNOWN y pasa a CONFIRMED `primera_sesion_dia_siguiente` por un registro `RESOLVE_UNKNOWN` de
la sesión 6 sobre el parámetro, con `ev-v17-000250-a468bcec`. `perdida_trader_reinicio_huso` se
queda UNKNOWN y su descripción dice que no tiene efecto con este valor (el precedente de
`perdida_maxima_semanal`, SIN EFECTO con `perdida_trader_alcance = dia`). Si el parámetro faltara o
fuera UNKNOWN, el motor hace lo de antes (`medianoche_huso`): no se adivina un reloj nuevo.

### 3. Dónde

- `engine/tope_trader.py`: `TopeTrader` gana `reinicio`; `tope_del_registro` lo lee y, con
  `primera_sesion_dia_siguiente`, no lee el huso ni marca SUPUESTO; `SeguidorTope.abrir_dia` corta el
  día (y la semana, si cambia la semana ISO respecto al último día con actividad) en la apertura que
  le da el cableado; `avanzar` no corta nada con ese valor. La descripción de la traza dice qué
  modo corta.
- `engine/cableado.py`: al empezar cada día que corre, con el seguidor ya construido o recién
  nacido, `abrir_dia(dia, apertura, saldo)`, con la apertura de la primera sesión del día (`primero`,
  de `dia.limites()`, en UTC por la puerta de ADR-0069) y el saldo arrastrado. Con
  `--diagnostico-cuenta-diaria` el seguidor nace cada día con la cuenta y no cambia nada.

Con `perdida_trader_alcance = dia` el corte de la semana no tiene efecto hoy (no se lee
`perdida_semana`); se escribe igual, porque es la regla del trader, y se prueba con un tope
sintético `ambos`.

## Problema que resuelve

A-44 seguía ABIERTA y bloqueante solo por el reinicio: el motor cortaba el tope del trader en la
medianoche del huso de corte del perfil, marcada SUPUESTO, y el trader dijo otra cosa. En la
simulación de hoy el día corre de la apertura de su primera sesión al fin de la última y ahí cierra
lo que quede (`engine/cableado.py`, el bucle y el fin del día; ADR-0053 §6), así que el saldo no
cambia entre la medianoche y la apertura y los dos relojes dan la misma base: lo que cambia es el
instante del corte y que la traza deje de marcar un huso SUPUESTO. Si algún día el saldo cambia
entre los dos instantes, las bases se separan (el test sintético lo dice).

## Alternativas consideradas

1. Un parámetro nuevo con las dos lecturas y el corte en la apertura (la elegida).
2. Meter «primera sesión» como un valor especial de `perdida_trader_reinicio_huso`.
3. Fijar el huso del reinicio en el de la primera sesión y seguir cortando a medianoche.

## Por que elegimos esta opcion

Porque lo que dijo el trader es un reloj de sesiones y no de husos: cada opción de A-44 vive en su
parámetro (ADR-0002), y la medianoche queda como la otra lectura, explícita.

## Por que descartamos las demas

- La 2 mezclaría un tipo `texto` (un nombre IANA) con un modo, y la guardia de husos lo rechazaría.
- La 3 seguiría cortando en un instante en que el trader no corta.

## Impacto

- **Registro y spec:** `perdida_trader_reinicio` nuevo (UNKNOWN → CONFIRMED por su registro de la
  sesión 6); las descripciones de `perdida_trader_reinicio_huso` («SIN EFECTO con
  perdida_trader_reinicio = primera_sesion_dia_siguiente»); `spec_version` 18.5.10 → **18.6.0**. El
  cierre de A-44, que esto deja sin parte abierta, va en su propio commit.
- **Código:** `engine/tope_trader.py` y `engine/cableado.py`.
- **Docs:** recuadros en ADR-0053 §3.3 y §9 y su fila del índice.
- **Tests:** `tests/unit/test_reinicio_tope_trader.py` (nuevo): los dos modos con el saldo que
  cambia y que no cambia entre la medianoche y la apertura, el viernes al lunes, el lunes sin
  sesiones, y dos que fallan con el código de `main` (el registro real y el cableado real).
  `tests/unit/test_preparar_a44.py::test_con_el_registro_real_el_tope_es_el_del_dia_en_porcentaje_sobre_el_saldo`
  cambia de sentido A PROPÓSITO: ya no asierta `huso_supuesto`.
- **Sin corrida que cuente** (ADR-0070 §3): la re-corrida va después de H y R.

## Fecha / fase

2026-11-05 · rama `trabajo/activar-sesion-06-motor` (R4.2). Informe:
`docs/validation/ACTIVAR-SESION-06-MOTOR.md`.

## Estado

ACTIVE
