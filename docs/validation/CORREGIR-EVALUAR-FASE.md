# La corrección de `evaluar_fase`: el orden a igual instante

Rama `trabajo/corregir-evaluar-fase`, 2026-09-28, desde `main` en `stable/F27-viabilidad-trader`
(`2e2f10e`). Corrige el error que encontró `VIABILIDAD-TRADER.md` §6. Solo construcción, abril y
agosto de 2026; ninguna fecha reservada.

## 1. La causa raíz

**Está en la capa de cuenta, `evaluar_fase` (`src/botsito/engine/cuenta.py`), y no en el bróker.**

- **El bróker hace lo que su contrato dice.** Deja en cada operación cerrada una marca en el
  instante mismo de su cierre: el peor precio visto con la posición viva hasta el tick que la
  cierra (`Broker._operacion`, marcas con `abierta_ms <= ms <= cerrada_ms`). Pasa en **73 de 73**
  operaciones medidas, y `comprobar_operacion` admite expresamente las marcas en todo el intervalo
  `[apertura, cierre]`, extremos incluidos.
- **La capa de cuenta las procesaba mal.** `_eventos` ordena a igual instante por un convenio
  declarado en ADR-0050: el cierre (0) antes que el cargo (1), la marca (2) y la apertura (3). Ese
  convenio tiene sentido **entre** operaciones -realizar la que cierra antes de abrir otra-, pero
  se aplicaba también **dentro** de una misma. Así, la marca del instante del cierre llegaba
  después del cierre, y el manejador de la marca volvía a meter la operación en `abiertas` **sin
  mirar si seguía abierta**. Desde ahí la equity vigilada llevaba el resultado de esa operación
  otra vez, como flotante, hasta el final.
- **Y un segundo síntoma de la misma causa**: una operación que abre y cierra en el mismo instante
  reventaba con `KeyError`, porque su cierre llegaba antes que su apertura. No se había dado en
  construcción, pero el contrato lo permite.

**La corrección** (`cuenta.py`, con la enmienda en ADR-0050): la vida de una misma operación manda
sobre el convenio entre operaciones. A igual instante, **su apertura va antes que sus marcas y sus
marcas antes que su cierre**. Por eso la marca del instante del cierre se procesa antes de él (es el
último precio con la posición viva), la marca del instante de la apertura después de ella, y la
apertura de una operación que cierra en el acto antes que cualquier cierre. Y **una marca nunca abre
ni reabre una posición**: si llegara para una que no está abierta, es un `OperacionError` con
nombre, como ya hacía `CuentaViva.marcar`. El convenio entre operaciones distintas no cambia.

## 2. Los tests

- `tests/unit/test_cuenta.py`, cuatro nuevos, **tres de ellos fallaban antes de la corrección**,
  por lo que dicen:
  - una ganadora de +3.000 con la marca en su cierre, y el mismo día una perdedora de −8.500: la
    cuenta tiene que suspender por pérdida diaria (94.500 bajo 95.000). **Antes: EN_CURSO**;
  - una operación sola con la marca en su cierre: la equity final igual al saldo final. **Antes:
    equity 101.400 con saldo 101.000**, la posición fantasma; y la marca del cierre sí cuenta,
    antes del cierre, para el mínimo de equity;
  - una operación que abre y cierra en el mismo instante. **Antes: `KeyError`**;
  - una marca en el instante de la apertura, procesada después de abrir (pasaba antes y pasa
    después: fija el orden nuevo).
- `tests/regression/test_cuenta_7_de_agosto.py`, el primero de esa carpeta: las cuatro operaciones
  del trader del 7 de agosto por el bróker sobre los ticks, al 0,5 % de 100.000, y `evaluar_fase`.
  **Tiene que suspender por pérdida diaria a las 12:30:01.312 UTC**, en el tick del pico. **Antes
  suspendía a las 12:10:26**: la marca fantasma de la tercera operación doblaba su pérdida cuando el
  saldo real seguía en 96.340, por encima del límite. El error no solo escondía suspensiones:
  también las adelantaba, según el signo de las operaciones fantasma. Necesita los ticks de `data/`:
  en la CI se salta.

## 3. Quién estaba afectado

| consumidor | usa | ¿afectado? |
|---|---|---|
| `scripts/repeticion_trader.py` (TICKS-LLENADO, Fase 6) | `evaluar_fase` sobre operaciones del bróker | **sí**: cambian las pérdidas máximas de todos los escenarios y dos veredictos (§4) |
| `scripts/viabilidad_trader.py` (VIABILIDAD-TRADER) | `evaluar_fase`, con las marcas del cierre quitadas antes | **sus cifras saneadas no**: salen idénticas; las del «motor tal cual» sí, y ahora coinciden con las saneadas |
| `engine/simulacion.simular_fase` (TICKS-LLENADO, Fase 5) | `evaluar_fase` | **en principio sí**; sus 6 tests (`test_simulacion.py`) pasan igual antes y después: la estrategia de juguete no cae en el caso, o no en lo que comprueban |
| el cableado del simulador: `motor arnes --simular`, `motor visor --simular`, el selector de A-47 y el embudo | `CuentaViva`, que no pasa por `_eventos` y solo marca posiciones abiertas | **no**: salidas byte a byte idénticas (§5) |
| `scripts/embudo_77.py` | el cableado | **no**: idéntico (§5) |
| `tests/unit/test_broker.py`, `test_cuenta.py` | `evaluar_fase` | sus tests previos pasan igual |

## 4. Los veredictos, antes → después

**La repetición de TICKS-LLENADO** (`repeticion_trader.py`, riesgo sobre el capital inicial, salida
por la regla de la spec). Entre paréntesis, pérdida diaria máxima / pérdida total máxima. La
repetición de antes reproduce byte a byte la salida commiteada, `REPETICION-TRADER-SALIDA.txt`.

| riesgo | abril: antes → después | agosto: antes → después |
|---|---|---|
| 0,25 % | EN_CURSO (3,89 / 6,29) → EN_CURSO (2,72 / 5,13) | EN_CURSO (1,29 / 3,46) → EN_CURSO (1,73 / 3,22) |
| 0,5 % | EN_CURSO (2,77 / 5,42) → EN_CURSO (3,20 / 5,85) | EN_CURSO (2,59 / 6,92) → EN_CURSO (3,45 / 6,20) |
| 1 % | EN_CURSO (0,58 / 1,52) → EN_CURSO (3,39 / 3,36) | **EN_CURSO (3,85 / 3,05) → SUSPENDIDA el 7 de agosto a las 12:30:01 UTC por pérdida diaria (5,11 %)** |
| 2 % | SUSPENDIDA el 13 de abril a las 12:03:59 (5,06 %) → SUSPENDIDA el 13 de abril a las **12:06:23** (5,07 %) | **EN_CURSO (1,70 / 0,85) → SUSPENDIDA el 7 de agosto a las 12:30:01 UTC por pérdida diaria (10,22 %)** |

Los saldos finales cambian donde la cuenta suspende, porque desde ese instante no evalúa más
operaciones: 2 % abril 97.066 → 94.862; 1 % agosto 113.260 → 103.847; 2 % agosto 123.198 → 118.120.

**La viabilidad** (VIABILIDAD-TRADER): sus cifras saneadas, que eran las válidas, salen idénticas
con la corrección, y el «motor tal cual» ahora da lo mismo que ellas. Los veredictos que el error
cambiaba -el motor tal cual frente a lo saneado- eran estos, y la corrección confirma los saneados:

| escenario | motor tal cual (inválido) | corregido = saneado |
|---|---|---|
| 0,5 % abril+agosto, simulada | EN_CURSO | **SUSPENDIDA** el 7 de agosto a las 12:30:01 UTC (pérdida diaria) |
| 1 % abril+agosto, simulada | EN_CURSO | **SUPERADA** el 6 de agosto a las 08:01 UTC |
| 2 % agosto, simulada | EN_CURSO | **SUSPENDIDA** el 7 de agosto a las 12:30:01 UTC (pérdida diaria) |
| 2 % abril, simulada | SUSPENDIDA el 13 de abril (pérdida diaria) | SUSPENDIDA el **16 de abril** (pérdida total) |

## 5. Las corridas de estrategia: byte a byte

Con el código de `main` (un worktree en `2e2f10e`) y con la corrección, las mismas corridas de
construcción, leyendo los datos del repositorio y escribiendo fuera:

| corrida | resultado |
|---|---|
| arnés `--simular`, A-47 `limite_en_retroceso`, A-21 `solo_una_zona_de_control` (informe y cifras) | **idéntica** |
| arnés, límite, A-21 `sin_mecha_mas_alla_del_extremo` | **idéntica** |
| arnés, A-47 `stop_en_ruptura`, A-21 `solo_una_zona_de_control` | **idéntica** |
| arnés, stop, A-21 `sin_mecha_mas_alla_del_extremo` | **idéntica** |
| embudo de las 77, las dos lecturas (informe y JSON) | **idéntico** |
| repetición de TICKS-LLENADO | cambia (§4) |
| viabilidad | cambia solo el bloque «motor tal cual» (§4) |

Las corridas de estrategia van por la cuenta viva del cableado, que no pasa por `_eventos`: la
corrección no las toca, y la medida lo confirma.

## 6. Recuadros en los informes cerrados

Sin reescribir nada: recuadro de corrección con los veredictos que cambian, remitiendo aquí, en
`TICKS-LLENADO.md` (Fase 6), `NOCHE-TICKS-BROKER.md` (su tabla de la Fase 6) y
`VIABILIDAD-TRADER.md` (§6). `REPETICION-TRADER-SALIDA.txt`, salida commiteada, no se toca: la
corregida está en §4.

## 7. Estado

Corrección, tests, enmienda de ADR-0050, recuadros e informe. **Rama lista para revisión, NO
cerrada.**
