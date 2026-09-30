---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `trabajo/nocturno-01oct`, sesión nocturna)
---

# 0063 · El reloj de las sesiones se separa del reloj del día de riesgo: el selector `reloj_sesiones` (PROPUESTO: pendiente de aceptación del consultor)

> **PROPUESTO.** Escrito en la sesión autónoma de la noche del 30 de septiembre al 1 de octubre de
> 2026 (`docs/nocturno/PLAN-01oct.md`, F36). Es el mecanismo que ADR-0059 pedía como «rama de
> código», y **no cambia ningún comportamiento**: el selector nace apuntando al reloj que el motor
> ya usaba. A-42 sigue ABIERTA y bloqueante, y la lectura PROVISIONAL de ADR-0059 sigue sin
> aplicarse. Lo acepta o corrige el consultor. El campo `status` dice ACTIVE solo porque la guardia
> de ADR (`tests/unit/test_adr.py`) no admite otro valor.

## Decision

### 1. Un selector dice con qué reloj se cuentan la ventana y sus sesiones

`reloj_sesiones`, `ejecucion`, `enum`, con dos opciones: `civil_operativa` —el reloj civil del
trader— y `grafico` —el de su gráfico—. **El huso de cada reloj no se escribe en el selector: vive
en el parámetro que ya lo tenía**, `huso_operativa` y `huso_grafico`, una sola vez (ADR-0002). La
correspondencia entre la opción y su parámetro está en `src/botsito/engine/relojes.py`.

Es el mismo patrón que `reloj_dia_riesgo` (ADR-0027), que elige entre relojes con las mismas
palabras, y por eso no nace un tercer parámetro con un huso dentro: con la lectura provisional de
A-42 las sesiones van «en el reloj del gráfico», y ese huso ya tiene su puerta.

### 2. Nace en `civil_operativa`, DEFAULT_AMBIGUOUS bajo A-42

- **Valor:** `civil_operativa`, que es lo que el motor hacía leyendo `huso_operativa`. Nada cambia:
  el informe del arnés sale idéntico byte a byte antes y después (medido, «Impacto»).
- **Estado:** `DEFAULT_AMBIGUOUS` con `ambiguedad_id: A-42`, porque con qué reloj cuenta el trader
  su horario es exactamente lo que A-42 pregunta y sigue abierta. Cada lectura del parámetro queda
  anotada como lectura ambigua, como las de la ficha del instrumento bajo A-27.
- **A-42** pasa a citar `reloj_sesiones` en vez de `huso_operativa`.

### 3. Quién lee cada reloj

| Reloj | Dónde vive | Quién lo lee |
|---|---|---|
| de las sesiones | el que diga `reloj_sesiones` | `en_ventana` (RN-001) y `alcanza_hora` (RN-002), que ahora reciben `reloj` en vez de `huso`; los límites de sesión del motor (`motor arnes`, `motor visor`); la ventana de mercado del día en la simulación |
| del día de riesgo | `huso_operativa` | el cableado, que lo compara con el reloj del perfil de la firma (ADR-0053 §4); es lo que `reloj_dia_riesgo: civil_operativa` declara (ADR-0027) |
| de la rejilla H4 | `anclaje_h4` | la agregación de velas, el sesgo y, desde ADR-0060, el cierre de RN-002 |

`huso_operativa` deja de leerlo ninguna forma, y declara `consumido_por` con los ADR que lo leen.

### 4. Las dos horas de la ventana declaran el huso del reloj de las sesiones

`ventana_inicio` y `ventana_fin` son de tipo `hora` y llevan su propio `huso`. Un test exige que sea
el del reloj que diga `reloj_sesiones`. El día que el selector pase a `grafico`, las dos horas
tienen que pasar a declarar `huso_grafico`, o el test falla.

### 5. Lo que NO se decide ni se toca aquí

- **El valor.** Pasar `reloj_sesiones` a `grafico` es aplicar la lectura de A-42, y eso lo decide el
  consultor cuando el trader la confirme sin «creo» (ADR-0059 §3).
- **La biblioteca de casos y el kit** (`cases/ingesta.py`, `cases/ventanas.py`, `cases/paquete.py`,
  `cases/fidelidad.py`) siguen leyendo `huso_operativa` para el día del caso y para asignar la
  sesión de cada operación del trader, y lo congelan en sus artefactos. No se tocan: ningún mes de
  invierno ha entrado, y la entrada de marzo sigue parada en la PARADA B0. **Antes de ingerir un
  mes de invierno con el selector en `grafico` hay que decidir con qué reloj se asigna la sesión de
  las operaciones del trader**; si no, el motor abriría las sesiones a una hora y los casos las
  tendrían etiquetadas a otra.
- **Los ticks de invierno.** Qué ventana de ticks hay que bajar para un mes de invierno depende de
  A-42: 05:00–13:00 UTC con las sesiones en el gráfico —la misma que en verano—, o 06:00–14:00 UTC
  con el reloj civil (ADR-0051 §7). No se baja nada aquí.
- **Los scripts de medición de ramas cerradas** siguen pasando `huso_operativa` al arnés. Solo
  `scripts/embudo_77.py` pasa a leer el reloj de las sesiones.

## Problema que resuelve

`docs/validation/ACTIVAR-SESION-03.md` §3, desalineación 9, y ADR-0059 §2: `huso_operativa` era a
la vez el reloj de las sesiones y el del día de riesgo. Probado el 2026-09-29: al pasarlo a
`Etc/GMT-2`, el cableado se negaba a correr en invierno («no hay un solo reloj») y fallaban 8 tests.
Sin separar los dos relojes, la lectura de A-42 no se puede aplicar, y ninguna corrida de invierno
—tampoco `fidelidad-dev`— puede contar.

## Alternativas consideradas

1. Un parámetro nuevo de tipo texto con el huso de las sesiones dentro.
2. Un selector que elige entre los relojes que el registro ya tiene (la elegida).
3. Que las formas de RN-001 y RN-002 nombren `huso_grafico` directamente cuando A-42 se confirme,
   sin parámetro nuevo.
4. Cambiar el reloj del día de riesgo y dejar `huso_operativa` para las sesiones.

## Por que elegimos esta opcion

- La 2 no duplica ningún huso: cada reloj sigue teniendo una sola puerta, y aplicar la lectura de
  A-42 es cambiar un valor, no escribir código ni editar formas.
- Deja a la vista, con su ambigüedad, que el valor de hoy es un default.

## Por que descartamos las demas

- La 1 crea un parámetro que el día de la confirmación valdría lo mismo que `huso_grafico`: dos
  puertas para el mismo reloj (ADR-0002), justo lo que ADR-0027 evitó al quitar la opción `grafico`
  de `reloj_dia_riesgo`.
- La 3 deja sin nombre en el registro el reloj con que el motor corta las sesiones, que no lo lee
  solo una forma: lo leen el arnés, el visor y la simulación.
- La 4 mueve el corte del día de la firma, que es el que cuesta la cuenta si se equivoca
  (ADR-0027).

## Impacto

- **Código:** `engine/relojes.py` (nuevo: `huso_del_reloj`, `huso_de_las_sesiones`);
  `engine/primitivas.py` (`en_ventana` y `alcanza_hora` reciben `reloj`); `cli.py` (`motor arnes`),
  `engine/visor.py` y `engine/simulacion.py` (los límites de sesión salen del reloj de las
  sesiones); `engine/cableado.py` y `engine/motor.py` (solo comentarios: el reloj único sigue
  comprobándose contra `huso_operativa`); `scripts/embudo_77.py`.
- **Spec:** los predicados `en_ventana` y `alcanza_hora` cambian el argumento `huso` por `reloj`;
  las formas de RN-001 y RN-002 nombran `reloj_sesiones`; parámetro nuevo `reloj_sesiones`;
  `huso_operativa` y `huso_grafico` declaran `consumido_por`; A-42 cita `reloj_sesiones`.
  `spec_version` **14.3.0 → 14.4.0**.
- **Tests:** `tests/unit/test_dos_relojes.py` (nuevo): el selector nace en el reloj civil y bajo
  A-42; las horas de la ventana declaran el huso del reloj de las sesiones; con el selector en
  `grafico`, en un día de invierno de 2030 la ventana y las sesiones abren una hora antes en UTC y
  en verano nada cambia; y el cableado no se niega, mientras que mover `huso_operativa` —lo que se
  probó el 2026-09-29— sí lo para. `test_cierre_vela_h4.py`, `test_huecos_motor.py` y
  `test_registro.py` se ajustan al argumento nuevo.
- **Medido sobre construcción** (abril y agosto de 2026), antes y después de esta pieza, con los
  mismos diagnósticos de ADR-0062: el informe del arnés sin simular y el simulado salen **idénticos
  byte a byte** (mismo sha256 de los dos ficheros antes y después). El mecanismo no cambia ningún
  comportamiento mientras el selector valga `civil_operativa`.
- **Lo que NO se ha medido:** ninguna corrida real con el selector en `grafico`. Construcción es
  abril y agosto, meses de verano en los que los dos relojes dan la misma hora, así que ahí el
  cambio de valor tampoco se vería; el comportamiento de invierno solo está probado sobre días
  sintéticos.

## Fecha / fase

2026-09-30 · sesión nocturna, rama `trabajo/nocturno-01oct`. `PROJECT_STATE.md`, Next Action A3.0.

## Estado

ACTIVE (PROPUESTO: pendiente de aceptación del consultor; el campo dice ACTIVE porque la guardia
de ADR no admite otro valor)
