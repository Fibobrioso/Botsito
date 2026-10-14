---
status: ACTIVE
date: 2026-10-13
phase: post-F14 (rama `trabajo/entrada-enero`, R2.2 de la hoja de ruta)
---

# 0079 · Enero de 2026 entra en construcción, del 2 al 30 (lo que cubre su libro)

> Decisiones del consultor del 2026-10-13: las tres del encargo de `trabajo/entrada-enero`
> («DECISIONES DEL CONSULTOR») y su respuesta a la PARADA, copiadas tal cual en
> `docs/encargos/trabajo-entrada-enero.md`. Medido en `docs/validation/ENTRADA-ENERO.md` §0, §1 y
> §2. Escrito ANTES de cualquier corrida del arnés que incluya enero.

## Decision

1. **2026-01 se añade a `construccion`** en `knowledge/cases/criterio_fidelidad.yaml`, que queda
   `["2026-04", "2026-07", "2026-08", "2026-01"]`. `medida` no cambia (`["2026-05"]`), y **ningún
   umbral cambia**: ni los de medida de ADR-0043 ni los de construcción de ADR-0070.
2. **El orden de la lista importa, y enero va AL FINAL.** `cargar_criterio` conserva el orden del
   fichero, y siete ficheros de tests toman `construccion[0]` del repo real como «el mes de
   construcción» sobre el que trabajar (`test_preparar_a21.py`, `test_preparar_a35.py`,
   `test_preparar_a44.py`, `test_rutas_windows.py`, `test_selector_orden_stop.py`,
   `test_simulacion.py` y `test_visor.py`); cinco de ellos llaman a `motor arnes`. Con enero
   primero, el `make check` de este mismo commit correría el arnés sobre enero, que todavía no
   tiene casos ni ticks, y la decisión dejaría de ser anterior a cualquier corrida con enero. Con
   enero al final, `construccion[0]` sigue siendo abril y ninguno cambia. Quien reordene la lista
   mueve a la vez esos siete tests (ENTRADA-ENERO.md, auditor, H1).
3. **Enero entra en construcción SOLO del 2 al 30**, que es el tramo de `cobertura_material` en
   `knowledge/cases/kit/config.yaml`: la fecha mínima y la máxima de la columna de fechas de su
   libro, leídas por Aleks una vez el 2026-10-13 (ADR-0072). Como en abril y julio, es un LÍMITE
   INFERIOR de lo que cubre el libro. Sus 21 laborables son `dev` por el reparto dev-visto
   (ADR-0042) y son los días que el arnés lee de enero. El 1 de enero no entra.
4. **La columna de fechas la leyó antes la sesión.** El 2026-10-06, cuatro días antes de ADR-0072,
   la rama `trabajo/reloj-invierno` leyó `dateStart` (y `entryPrice`) de todas las filas del libro
   para medir su huso, y con esa medida se declaró el libro en `libros.yaml` (ADR-0039). La lectura
   de Aleks del 2026-10-13 es la que fija el tramo según ADR-0072. No es una exposición nueva: enero
   no tiene ningún día en ninguna partición. Y como el libro ya estaba declarado, enero no necesita
   la excepción a ADR-0039 §1 que ADR-0078 extendió a julio.
5. **Diciembre de 2025 NO se baja** (decisión 2 del consultor): es material del trader sin decidir
   (NA:I) y no está en `vistos.yaml`, así que un `kit build` posterior lo sortearía como ciego. Sin
   las velas de diciembre, el sesgo H4 de los primeros días de enero calienta solo con velas de
   enero (`engine/arnes.py`: el mes anterior, si hay dataset). **Medido** (ENTRADA-ENERO.md §0.f,
   con el motor de hoy, que ya incluye ADR-0075): en los 21 laborables por sus dos sesiones, **0
   INSUFICIENTE** (19 alcista, 23 bajista), ninguna búsqueda mira más de 2 velas, y todas se
   deciden con pares de velas de enero, así que con diciembre ningún sesgo cambiaría. Lo único
   recortado es el horizonte: hasta el 15 de enero hay menos H4 cerradas (como mucho 57) que las 60
   del tope. Si un día se baja el M1 de diciembre, enero calentará con él sin cambiar una línea.
6. **Por qué enero es construcción** (decisión 1 del consultor, medida otra vez en ENTRADA-ENERO.md
   §0.a y §2.a):
   - no está en `knowledge/cases/meses_reservados.yaml`;
   - ningún reparto le asigna un caso reservado (`casos_reservados` y `casos_ocultos`: 0 para
     2026-01, en 6fb483b y otra vez en 7bc7fa3, antes de leer el libro);
   - está en `knowledge/cases/kit/vistos.yaml` (visto el 2026-08-30: el trader recorrió el backtest
     de enero en v4), así que no sirve como mes ciego;
   - su libro ya estaba declarado en `libros.yaml` (UTC, 2026-10-06).

## Problema que resuelve

ADR-0043 fijó construcción = abril y agosto; ADR-0078 añadió julio. Enero era el único mes de
desarrollo con libro que no contaba, porque su ventana de ticks es la de invierno y
`scripts/ticks_spread.py` la contaba en `huso_operativa` y no por la rejilla (ADR-0069 §5, NA:X).
Sin decisión escrita antes de la primera corrida que lo incluya, cualquier cambio de la lista
después de ver resultados sería ajustar el conjunto al resultado.

## Alternativas consideradas

- **(a) Enero en construcción, del 2 al 30, al final de la lista** (esta).
- (b) Enero en construcción, en orden cronológico (primero), cambiando los siete tests de
  `construccion[0]`.
- (c) Enero en construcción con diciembre de 2025 bajado antes, para calentar el sesgo.
- (d) Enero reservado.

## Por que elegimos esta opcion

Enero no es ciego (vistos.yaml) ni tiene ningún día en ninguna partición: lo único que puede ser es
desarrollo, y entra con lo que su libro cubre, como abril, julio y agosto (ADR-0042). Al final de
la lista, ningún test cambia de mes y este commit no corre el arnés sobre enero. Amplía la
construcción de 55 a 76 días `dev` antes de la corrida de R3.1.

## Por que descartamos las demas

- (b): siete ficheros de tests fuera del encargo, y el arnés sobre enero en el `make check` de este
  commit, antes de tener casos (punto 2).
- (c): diciembre está sin decidir y sin ver; bajarlo lo haría sortearse como ciego en un `kit
  build` posterior. Y no cambia ningún sesgo de enero (punto 5).
- (d): reservar días de un mes que el trader ya recorrió en pantalla no protege nada (el mismo
  argumento que para abril, julio y agosto).

## Impacto

- `knowledge/cases/criterio_fidelidad.yaml`: `construccion` con enero al final.
  `tests/unit/test_criterio_fidelidad.py` lo afirma.
- **La ventana de ticks sale de la rejilla** (ADR-0069 §5; NA:X, hecha en la fase 1 de la rama):
  `scripts/ticks_spread.py` lee cada tick con `reloj_de_las_sesiones` y no en la hora de pared de
  `huso_operativa`, y exige los ticks de cada mes de `construccion`;
  `tests/unit/test_ticks_spread.py` lo rompe a propósito con un día de desfase (2026-10-27). Sobre
  abril, julio y agosto, que no tienen días de desfase, da las mismas cifras que antes (regresión
  contra `main`, ENTRADA-ENERO.md §1). Los ticks de enero se bajan con `--horas 06-14`: la ventana
  de la rejilla (06:00-14:00 UTC) más una hora, el criterio de abril, julio y agosto (DN-5 de
  ADR-0051).
- Desde este commit, `make check` corre el sesgo H4 del motor sobre las velas M1 de los 21 días
  `dev` de enero (`tests/unit/test_huecos_motor.py`; los días salen del reparto dev-visto, ya
  commiteado, y no de los casos), como con abril, julio y agosto: solo lee velas (ADR-0021 §1),
  ninguna etiqueta, y no mide nada (aceptado por el consultor el 2026-10-13, punto 4).
- `data download-ticks` admite enero (sale con 2 para un mes fuera de construcción).
- La corrida de ADR-0070 (R3.1) cubre ya los cuatro meses: «la construcción vigente».
- **El spread supuesto del respaldo sin ticks** (ADR-0051 §6, `knowledge/simulador/llenado.yaml`)
  sigue medido sobre los ticks de abril y agosto, como dejó ADR-0078, y NO se rehace aquí. Las horas
  perdidas del dataset de enero irán por el respaldo M1 con ese spread supuesto. La corrida de
  `ticks_spread.py` con los cuatro meses se deja en un anexo de la rama, sin tocar `llenado.yaml`.
- **Deuda declarada, no arreglada aquí** (ENTRADA-ENERO.md §8): `engine/simulador_config.py` busca
  ese spread por la hora de PARED de `Europe/Madrid`, y no por la rejilla: los días de desfase
  (2026: del 9 al 27 de marzo y del 26 al 30 de octubre) la hora sale corrida; medido el 2026-10-27,
  4 de 11 horas con 1 punto distinto. Ningún mes de construcción tiene días de desfase.
- Notas, sin reescribir cuerpos: ADR-0043 («construcción = abril y agosto»), ADR-0069 §5 (la
  ventana de ticks de invierno, pendiente) y ADR-0051 DN-5 (la ventana de invierno, PENDIENTE). Los
  runbooks `ARNES-MOTOR.md`, `SESION-DE-PREGUNTAS.md` y `VISOR-DIAS.md`, corregidos en el mismo
  commit.
- Los guiones de medidas ya cerradas que fijan sus meses (`scripts/caja_77.py`,
  `scripts/embudo_77.py`, `scripts/sesgo_h4_diagnostico.py`, `scripts/viabilidad_trader.py`) no
  cambian: reproducen su medida, no la construcción vigente.

## Fecha / fase

2026-10-13 · rama `trabajo/entrada-enero` (R2.2 de `docs/plan/HOJA-DE-RUTA.md`; NA:X). Informe
`docs/validation/ENTRADA-ENERO.md`.

## Estado

ACTIVE
