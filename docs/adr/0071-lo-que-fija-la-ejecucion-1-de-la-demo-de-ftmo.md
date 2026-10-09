---
status: ACTIVE
date: 2026-10-09
phase: post-F14 (rama `trabajo/demo-ejecucion-1`)
---

# 0071 · Lo que fija la ejecución 1 de la demo de FTMO: la ficha de EURUSD, el stops level y el volumen máximo; A-27 DECIDIDA

> La fuente de cada valor que entra en `knowledge/` desde la primera medida de
> `tools/mql5/MedirDemoFTMO.mq5` en la prueba gratuita de FTMO. El trailer `Fuente:` y el campo
> `fuente` del registro no admiten un manifiesto; este ADR lo cita y cita la fila de cada valor.
> Informe con el inventario fila a fila y la respuesta del consultor:
> `docs/validation/DEMO-EJECUCION-1.md` (allí se le llama «ADR-D1», su nombre provisional).

## La medida

- **CSV:** `data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv` (fuera de git), 9.907 bytes, sha256
  `86f0df8b24f632102f0207b62a298a7776a164868e9a2d820ceb133c144b3c6e`, 59 filas, `version_script`
  1.0. Congelado en `data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml`. Aleks declara
  (2026-10-09) que `certutil -hashfile` sobre el original de `MQL5\Files` da el mismo sha256.
- **Cuenta:** prueba gratuita de FTMO creada el 2026-10-08 (2-Step, Swing, USD, 100.000, MT5),
  servidor FTMO-Demo, FTMO Global Markets Ltd (filas 21-23); ejecución el 2026-10-09 de 15:35:52 a
  15:36:36 del servidor, «completo» y sin nada abierto al terminar (filas 58-59).
- «Fila» es la columna `fila` del CSV.

## Decision

### 1. Los cinco parámetros de A-27 pasan a CONFIRMED con el valor que ya tenían

En `knowledge/spec/parametros.yaml`, de DEFAULT_AMBIGUOUS (FundedNext, ADR-0026) a CONFIRMED con
fuente este ADR, sin `ambiguedad_id`:

| parámetro | valor | fila del CSV |
|---|---|---|
| `instrumento_digitos` | 5 | 6 (`digits` 5; `point` 0.00001000, fila 7) |
| `instrumento_contrato` | 100000 | 8 (`contrato` 100000.00) |
| `instrumento_lote_minimo` | 0.01 | 9 (`volumen_min` 0.01) |
| `instrumento_lote_paso` | 0.01 | 11 (`volumen_paso` 0.01) |
| `instrumento_stops_level` | 0 | 4 (`stops_level_puntos` 0) |

Ningún valor cambia, así que ni la estrategia ni las corridas cambian. RN-026 sigue sin activarse
con 0, como ya decía su nota.

### 2. El perfil de FTMO: stops level 0 y volumen máximo 50

En `knowledge/cuentas/ftmo-2step-swing-100k.yaml`:

- **`firma_stops_level_puntos`: UNKNOWN → CONFIRMED 0** (fila 4). El bróker simulado coloca órdenes
  stop sin `--diagnostico-a27`, y ese diagnóstico se rechaza con el perfil de FTMO, que ya fija el
  valor (`engine/broker.py`, `Broker.__init__`; ADR-0057 §5, «Con el valor ya fijado en el perfil,
  el diagnóstico se rechaza»). Con 0 el bróker no juzga ninguna distancia mínima (`if minimo:`), así
  que las límites siguen como hasta hoy. La negativa por defecto de ADR-0057 §5 (sin valor, el
  bróker se niega a colocar una stop) NO desaparece: es del código, y la siguen probando los tests
  con un perfil sintético en UNKNOWN. El freeze level también es 0 (fila 5): que el simulador no lo
  modele es exacto para esta cuenta.
- **`firma_volumen_max_lotes`: 100 → 50** (fila 10, `volumen_max` 50.00). El 100 venía de la tabla
  de símbolos de la web (R11), y FTMO dice en la misma fuente que la especificación de la cuenta es
  la que se ve en la plataforma. Si la cuenta Swing de verdad dijera otra cosa, es la pregunta P-D1
  a FTMO (la manda Aleks).

**La consecuencia del volumen máximo, calculada con el registro y sin medir nada sobre
operaciones.** El lote se dimensiona con `riesgo_por_operacion` (0,5 %) sobre `base_calculo_riesgo`
(`saldo_actual`, 100.000 al empezar) y sobre la distancia hasta el stop (`lotaje_base` =
`hasta_stop_fraccion`, ADR-0020). El valor del pip de EURUSD en una cuenta en USD es
`instrumento_contrato` × 10 puntos × 0,00001 = **10 USD por lote y pip**. Entonces:

    riesgo = 0,005 × 100.000 = 500 USD
    lote   = 500 / (stop_en_pips × 10) = 50 / stop_en_pips
    lote > 50  ⇔  stop_en_pips < 1

**El tope de 50 lotes corta todo stop de menos de 1 pip (10 puntos)**; con 1 pip exacto el lote es
50,00 y pasa, porque el bróker solo rechaza `lotes > volumen_max_lotes`. El umbral se mueve con el
saldo: 1 pip × saldo / 100.000 (0,9 pips con 90.000, 1,1 con 110.000). Es la cuenta que usa el
pendiente heredado 37 (los rechazos por volumen máximo, A-18).

**Y lo que deja abierto para esa rama** (añadido por el consultor el 2026-10-09, antes del merge):
`volumen_limite` = 0 (fila 12, `SYMBOL_VOLUME_LIMIT`) dice que el servidor no pone tope a la suma
de órdenes y posiciones del símbolo, solo a cada orden. Así que la rama del pendiente 37 decide entre
tres salidas cuando el lote pasa de 50: **recortar el lote a 50** (con un riesgo menor que el de
`riesgo_por_operacion`), **partir la operación en varias órdenes** de 50 como mucho, o **no
operar**. No se decide aquí. Ya hay un caso real: la primera operación del trader del 2026-08-07
(construcción) pasa de 50 lotes, y el bróker la rechaza
(`tests/regression/test_cuenta_7_de_agosto.py`).

### 3. La comisión: el importe no cambia; cobrarla en cada lado queda CONFIRMADO

- **Medido** (filas 53 y 54): −0,03 USD en la apertura y −0,03 en el cierre de una compra de 0,01
  lotes.
- **Lo que fija:** `firma_comision_por_lado` = true queda CONFIRMADO como hecho medido: se cobra en
  los dos lados, como dijo FTMO el 2026-09-29 (50 % al abrir, 50 % al cerrar). Solo cambia su
  descripción.
- **Lo que no fija:** la tarifa por lote. La comisión de un deal va en céntimos, y 0,03 con 0,01
  lotes sale de cualquier tarifa de 2,01 a 3,99 USD por lote y lado, según redondee MT5. **Excluye
  como hecho los 5 USD por lado** del perfil (darían 0,05) y los 1,50 por lado (0,02). Las dos
  exclusiones suponen que la comisión es proporcional al volumen y sin mínimo por operación; con
  0,01 lotes no se puede distinguir, y la ejecución 2, con 1,00 lote, lo comprueba (revisor, a4). La
  conclusión práctica no depende de ello: el 5 por lado del perfil no es más barato que la medida. El valor del
  perfil, `firma_comision_usd_por_lote` = 5 con cobro en cada lado, **no cambia en esta rama**:
  queda como supuesto CONSERVADOR, más caro que cualquier tarifa compatible con la medida.
- **La tarifa se mide en la ejecución 2**, con 1,00 lote en el paso 6 (script 1.1, rama
  `trabajo/demo-ejecucion-1`).

### 4. Lo medido de ADR-0057, y lo que sigue PROVISIONAL

- **§1, la stop de entrada se llena al precio del tick y nunca mejor que el nivel:** coincide (filas
  56-57: una buy stop a 1.11999 se llenó a 1.12000, un punto en contra). Una observación; no dice qué
  tick la disparó.
- **§2, el nivel exacto no es lado equivocado: SIGUE PROVISIONAL.** En las filas 39-42, de las
  cuatro pendientes en el nivel exacto solo la sell stop hizo lo que supone el simulador (quedó
  viva); la sell limit se llenó al instante a 1.11993, 3 puntos mejor que su precio, y la buy stop y
  la buy limit se rechazaron (10015). Una observación por tipo, y el CSV no registra la cotización
  del servidor en el instante de la comprobación: no se distingue entre una regla del servidor y
  que el precio se moviera. Esperan a las ejecuciones 2 y 3.
- **§3, una pendiente del lado equivocado se RECHAZA, también al modificarla: MEDIDO.** Las ocho
  de las filas 34-37 (20 puntos pasadas) y 43-46 (1 punto pasadas) se rechazan con 10015
  INVALID_PRICE, y ninguna se llena; las dos modificaciones al lado equivocado (filas 49 y 51) se
  rechazan con 10015 y la orden sigue a su precio. Paga la deuda «EL BROKER SIMULADO LLENA AL
  INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL» con las filas 36, 37, 45 y 46.
- **§4, la cotización con que se juzga:** sin cambio; la medida no la resuelve en el nivel exacto.
- **§5:** stops level 0 y freeze level 0 (punto 2).

### 5. Lo que NO cambia, y por qué

- **Los swaps** (filas 16-17: −9,41 y 0,10 el 2026-10-09, frente a −9,49 y 0,36 de la web el
  2026-09-25): cambian con la fecha, y nada que dependa de ella se fija con una ejecución. Las tres
  ejecuciones dan tres lecturas. El triple del miércoles (fila 19) que el simulador no cobra no
  entra como deuda: el bot cierra a las 15:00.
- **El deslizamiento fijo** (DN-3, `deslizamiento_fijo_puntos` 0): tres muestras, +2, −2 y +1
  puntos (filas 53, 54 y 57). Ninguna cifra fija se sostiene con tres muestras de un minuto.
- **El nivel exacto** (§4 de arriba).
- **El reloj (A-28):** desfase servidor − GMT **180 min** el 2026-10-09 (fila 31), la primera de
  tres medidas. Los dos calendarios dan 180 ese día; A-28 sigue ABIERTA hasta la ejecución 2.

### 6. A-27 DECIDIDA por este ADR

A-27 (la ficha de EURUSD en FTMO) se cierra como DECIDIDA (ADR-0022, la segunda forma: una
`medicion` no la contesta el trader). Sus cinco valores no dependen de la fecha. **Las ejecuciones 2
y 3 vuelven a leer la ficha con el mismo script, y el pre-vuelo de F33 la lee en la cuenta de
verdad; una diferencia en cualquiera de ellas reabre A-27 con otro ADR.**

### 7. Hechos para el conector (F33), sin parámetro hoy

- **Hedging** en la prueba (fila 25, `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING`). El simulador ya modela
  posiciones independientes y la estrategia nunca tiene dos a la vez (RN-011, `ninguno_de`), así
  que no cambia nada; el conector cerrará por ticket. Si la cuenta de verdad es de hedging, P-D1.
- **Modos de llenado FOK e IOC** (fila 13): una orden del EA va con uno de los dos.
- **Ejecución a mercado** (fila 14) y los cuatro modos de caducidad (fila 15).

## Problema que resuelve

Hasta hoy los cinco parámetros del instrumento eran la medida de otra firma (FundedNext) conservada
como default, y el stops level de FTMO era UNKNOWN: el bróker simulado se negaba a colocar cualquier
orden stop, que es como entra el trader desde la sesión 3 (A-47), y sin `--diagnostico-a27` ninguna
corrida simulada pasaba de la primera orden. El volumen máximo era el de la web, que FTMO dice que
manda la plataforma. Faltaba una fuente citable para lo medido.

## Alternativas consideradas

1. Citar el manifiesto directamente en el trailer `Fuente:`: no lo admite (`comun/historial.py`).
2. Una evidencia `ev-*`: `knowledge/evidence/` es para items del corpus con su cita.
3. Esperar a las tres ejecuciones para fijar nada.
4. Un ADR que cite el manifiesto y cada fila, y que fije solo lo que no depende de la fecha (la
   elegida).

## Por que elegimos esta opcion

Es la puerta que el registro ya tiene para lo que no es estrategia (ADR-0004): una decisión con su
ADR. Cada valor sale de una fila de un fichero congelado por su hash. La ficha del símbolo no
cambia con el día, y fijarla quita el diagnóstico de A-27 de toda corrida simulada; lo que sí
depende de la fecha espera.

## Por que descartamos las demas

- La 1 y la 2 no las admite el repositorio.
- La 3 dejaría a A-27 bloqueando las corridas tres semanas por valores que una segunda lectura solo
  puede repetir; si no los repite, se reabre.

## Impacto

- `knowledge/spec/parametros.yaml`: los cinco de A-27, a CONFIRMED (y `docs/spec/` regenerado).
- `knowledge/spec/ambiguedades.yaml`: A-27 DECIDIDA; sale su fila de «Known Ambiguities».
- `knowledge/cuentas/ftmo-2step-swing-100k.yaml`: `firma_stops_level_puntos` 0,
  `firma_volumen_max_lotes` 50 y la descripción de `firma_comision_por_lado`.
- Tests: la negativa con el stops level UNKNOWN pasa a un perfil sintético; ningún test que la
  compruebe se borra (lista en el informe).
- Ningún cambio en `src/`.
- `tools/mql5/MedirDemoFTMO.mq5` 1.1 y su lector, para la comisión con 1,00 lote (rama
  `trabajo/demo-ejecucion-1`, autorizado por el consultor).

## Fecha / fase

2026-10-09 · post-F14, rama `trabajo/demo-ejecucion-1`.

## Estado

ACTIVE
