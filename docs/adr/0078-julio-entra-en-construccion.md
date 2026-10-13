---
status: ACTIVE
date: 2026-10-13
phase: post-F14 (rama `trabajo/entrada-julio`, R2.1 de la hoja de ruta)
---

# 0078 · Julio de 2026 entra en construcción, del 1 al 17 (lo que cubre su libro)

> Decisión del consultor del 2026-10-12 (encargo de `trabajo/entrada-julio`, «DECISIÓN DEL
> CONSULTOR») y del 2026-10-13 (datos para la fase 3, «DECISIÓN DEL CONSULTOR SOBRE EL TRAMO»),
> copiadas tal cual en `docs/encargos/trabajo-entrada-julio.md`. Medido en
> `docs/validation/ENTRADA-JULIO.md` §0 y §3. Escrito ANTES de cualquier corrida del arnés que
> incluya julio.

## Decision

1. **2026-07 se añade a `construccion`** en `knowledge/cases/criterio_fidelidad.yaml`, que queda
   `["2026-04", "2026-07", "2026-08"]`. `medida` no cambia (`["2026-05"]`), y **ningún umbral
   cambia**: ni los de medida de ADR-0043 ni los de construcción de ADR-0070.
2. **Julio entra en construcción SOLO del 1 al 17**, que es el tramo de `cobertura_material` en
   `knowledge/cases/kit/config.yaml`: la fecha mínima y la máxima de la columna de fechas de su
   libro, leídas por Aleks una vez el 2026-10-13 (ADR-0072). Como en abril, es un LÍMITE INFERIOR
   de lo que cubre el libro: un laborable del borde sin operaciones no se distingue de uno no
   cubierto. Sus 13 laborables son `dev` por el reparto dev-visto (ADR-0042) y son los días que el
   arnés lee de julio (`dias_de_construccion`).
3. **Los días del 20 al 31 de julio NO entran** ni en el reparto ni en los casos: no hay libro que
   los cubra (ADR-0042 §2). Según el trader (de palabra a Aleks el 2026-10-13), el xlsx exporta los
   tres primeros vídeos (v11 a v13) y el cuarto (v14) termina el mes desde el 20 sin xlsx, que ya no
   puede exportar porque borró el backtest. Las capturas de resumen tampoco sirven para esos días:
   son un agregado del mes entero, y no se abren (ADR-0038). **Si se sacan casos del vídeo para
   ellos se decide DESPUÉS de la rama que transcriba v11 a v14**, que además comprueba lo que dice
   el trader sobre qué vídeo cubre qué días.
4. **La lectura de la columna de fechas ANTES de declarar el libro** -la excepción a ADR-0039 §1
   que la NOTA de ADR-0046 acotaba a marzo- **se extiende a julio**: la hizo Aleks, una vez y antes
   del reparto, y solo esa columna (ADR-0072: QUIÉN, CUÁNDO y QUÉ), declarada el mismo día en
   `HOLDOUT-EXPOSICIONES.md`. ADR-0039 §1 lleva una NOTA que apunta aquí.
5. **Por qué julio es construcción** (los seis puntos de la decisión del 2026-10-12, medidos de
   nuevo en ENTRADA-JULIO.md §0.a):
   - no está en `knowledge/cases/meses_reservados.yaml`;
   - ningún reparto de `knowledge/cases/{kit,fidelidad,visto}/` le asigna un caso reservado
     (`casos_reservados` y `casos_ocultos`: 0 para 2026-07, el 2026-10-12 y otra vez el 2026-10-13
     antes de leer el libro);
   - está en `knowledge/cases/kit/vistos.yaml` (visto el 2026-08-03: v2 y v3 dibujan y operan sobre
     julio), así que no sirve como mes ciego;
   - tampoco como mes de fidelidad al estilo de septiembre (ADR-0034): en v10 el trader enseñó en
     pantalla operaciones de julio comentadas en voz (`HOLDOUT-EXPOSICIONES.md`, 2026-10-04);
   - es un mes de verano: su ventana de ticks, 05:00-13:00 UTC, no depende de la rejilla de
     invierno (ADR-0069 §1 y §5; NA:X);
   - el trader da por bueno su backtest grabado en vídeo, «y lo mismo dijo de julio» (ADR-0073 §5).

## Problema que resuelve

ADR-0043 fijó construcción = abril y agosto, y ADR-0070 §2 hace del umbral para medir mayo un
umbral de «la construcción vigente». Julio llegó el 2026-10-04 sin decidir si era construcción o
reservado (NA:S, R2.1). Sin decisión escrita antes de la primera corrida que lo incluya, cualquier
cambio de la lista después de ver resultados sería ajustar el conjunto al resultado.

## Alternativas consideradas

- **(a) Julio en construcción, del 1 al 17** (esta).
- (b) Julio reservado, como mes de fidelidad (ADR-0034/0036).
- (c) Julio en construcción, el mes entero, sacando del vídeo los días 20 a 31.
- (d) Dejar julio fuera de todo hasta transcribir los vídeos.

## Por que elegimos esta opcion

Julio ya no es ciego (vistos.yaml) ni limpio para fidelidad (v10), y no tiene ningún día en ninguna
partición: lo único que puede ser es desarrollo. Entrar con lo que el libro cubre es lo que hicieron
abril y agosto (ADR-0042), con el mismo procedimiento y las mismas puertas, y amplía la construcción
de 42 a 55 días `dev` antes de la corrida de R3.1.

## Por que descartamos las demas

- (b): reservar días de un mes que el trader ya enseñó en pantalla no protege nada (ADR-0042, el
  mismo argumento que para abril y agosto).
- (c): un caso necesita su libro (ADR-0042 §2); sacar etiquetas de un vídeo sin transcribir es
  inventarlas. Se decide tras la transcripción (punto 3).
- (d): la parte del 1 al 17 tiene libro, y esperar no cambia nada de ella.

## Impacto

- `knowledge/cases/criterio_fidelidad.yaml`: `construccion` con julio. `tests/unit/test_criterio_fidelidad.py`
  lo afirma.
- Desde este commit, `make check` corre el sesgo H4 del motor sobre las velas M1 de los días `dev`
  de julio (`tests/unit/test_huecos_motor.py`), como ya hacía con abril y agosto: solo lee velas
  (ADR-0021 §1), ninguna etiqueta, y no mide nada (aceptado por el consultor el 2026-10-12).
- `data download-ticks` admite julio (sale con 2 para un mes fuera de construcción).
- La corrida de ADR-0070 (R3.1) cubre ya los tres meses: «la construcción vigente».
- **El spread supuesto del respaldo sin ticks** (ADR-0051 §6, `knowledge/simulador/llenado.yaml`)
  está medido sobre los ticks de abril y agosto y NO se rehace aquí: con ticks de julio, los días
  de julio no lo usan, salvo en las horas perdidas de su dataset (3 de 117 en
  `eurusd-ticks-2026-07-6e7dc7cd`), que van por el respaldo M1 con ese spread supuesto, como las
  de abril y agosto. Si una rama lo remide, julio es construcción y puede entrar.
- Notas, sin reescribir cuerpos: ADR-0043 («construcción = abril y agosto») y ADR-0039 §1 (la
  excepción de la lectura de fechas). Los runbooks `ARNES-MOTOR.md` y `SESION-DE-PREGUNTAS.md`,
  corregidos en el mismo commit.
- Los guiones de medidas ya cerradas que fijan `("2026-04", "2026-08")` (`scripts/caja_77.py`,
  `scripts/embudo_77.py`, `scripts/sesgo_h4_diagnostico.py`, `scripts/viabilidad_trader.py`) no
  cambian: reproducen su medida, no la construcción vigente.

## Fecha / fase

2026-10-13 · rama `trabajo/entrada-julio` (R2.1 de `docs/plan/HOJA-DE-RUTA.md`; NA:S). Informe
`docs/validation/ENTRADA-JULIO.md`.

## Estado

ACTIVE
