---
status: ACTIVE
date: 2026-11-06
phase: post-F14 (rama `trabajo/demo-ejecuciones-2-3`, A.1 de la hoja de ruta)
---

# 0090 · Lo que fijan las ejecuciones 2 y 3 de la demo de FTMO: A-28 DECIDIDA (120 y `us`), la comisión a 2,50 por lote y lado, y el paso 8 (enmienda ADR-0081 §4)

> Decisiones del consultor del 2026-11-06 (encargo de `trabajo/demo-ejecuciones-2-3`, D1-D12),
> tomadas antes de que la sesión midiera, y aplicadas sobre lo medido en
> `docs/validation/DEMO-EJECUCIONES-2-3.md` §0. Como ADR-0071, es la fuente citable de lo que entra
> en `knowledge/` desde unos CSV congelados: el trailer `Fuente:` no admite un manifiesto. **Enmienda
> ADR-0081 §4** (lo que da por hecho del margen de una pendiente stop), con recuadro allí y fila en el
> índice; y deja recuadro en ADR-0071 §3 y §4, ADR-0057 §2, ADR-0027 §4, ADR-0068 y ADR-0082.

## La medida

«Fila» es la columna `fila` del CSV. Los tres CSV viven en `data/demo_ftmo/` (fuera de git); sus
originales siguen en `MQL5\Files` del terminal, y la sesión midió el 2026-11-06 que coinciden con
las copias byte a byte (informe §0.b).

| ejecución | CSV (sha256) | manifiesto | script | cuándo (servidor) |
|---|---|---|---|---|
| 1 | `MedirDemoFTMO_20261009_153552.csv` (`86f0df8b…3c6e`, 9.907 bytes) | `data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml` | 1.0 | 2026-10-09 15:35:52-15:36:36 |
| 2 | `MedirDemoFTMO_20261029_194056.csv` (`1b82f61b…823d`, 10.167 bytes, 60 filas) | `data/manifests/demo_ftmo/demo-ftmo-2026-10-29-1b82f61b.yaml` | 1.1 (d48150e) | 2026-10-29 19:40:56-19:42:01 |
| 3 | `MedirDemoFTMO_20261105_203519.csv` (`59565621…4924`, 18.991 bytes, 115 filas) | `data/manifests/demo_ftmo/demo-ftmo-2026-11-05-59565621.yaml` | 1.2 (a90cd45) | 2026-11-05 20:35:19-20:38:44 |

La 2 y la 3 corrieron en la prueba gratuita creada el 2026-10-29 (2-Step, Swing, USD, 100.000, MT5),
servidor FTMO-Demo, FTMO Global Markets Ltd, build 6230; las dos «completo» y sin nada abierto al
terminar. **La 3 corrió fuera de la franja del runbook** (de 9 a 18 de España): 20:35 del servidor,
18:35 UTC, 19:35 de España y 13:35 de Lima, con Nueva York abierto (13:35 EST) y Londres ya cerrado
(18:35 GMT), comprobado con `zoneinfo`. La hora puede afectar al spread, al deslizamiento y al
llenado de los pasos 6 y 7; no afecta al desfase del reloj, a la comisión ni a la ficha.

**Una corrección a la ejecución 1.** Su manifiesto (inmutable) declara `fin_de_linea: LF`, y el CSV
es CRLF en sus 60 líneas: siempre lo fue (el sha256 es el congelado el 2026-10-09). La medida que
dio LF (DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c, `grep -c $'\r'` en Git Bash) es un artefacto: el
`grep` de Git para Windows quita el CR del final de línea salvo con `-U` (`grep -U -c -P '\r'` da
60; sin `-U`, 0). El manifiesto no se toca; los dos informes reciben un recuadro, y la deuda del CRLF
sale de Technical Debt por (a) de `docs/state/README.md`. Ningún código ni test lee `fin_de_linea`.

## Decision

### 1. A-28 DECIDIDA: `broker_offset_base` = 120 y `broker_dst` = `us`

| ejecución | fecha del servidor | fila 31 (`desfase_servidor_gmt_min`) | con `eu` | con `us` | con `ninguno` |
|---|---|---|---|---|---|
| 1 | 2026-10-09 | 180 | 180 | 180 | 120 |
| 2 | 2026-10-29 | 180 | **120** | 180 | 120 |
| 3 | 2026-11-05 | 120 | 120 | 120 | 120 |

La regla de lectura se escribió antes de mirar (encargo, D3): el 29-oct discrimina, porque Europa
cambió de hora el 25 y EE. UU. el 1-nov. Con base 120, solo `us` casa con las tres; probadas las
bases 60, 120 y 180 con los tres calendarios, **solo «120, `us`» casa**. En `parametros.yaml` los
dos pasan de UNKNOWN a CONFIRMED con fuente este ADR. Ningún código los lee hoy (informe §0.d): no
cambia ninguna corrida. A-28 se cierra como DECIDIDA (ADR-0022, la segunda forma: una `medicion` no
la contesta el trader).

**Cuánto depende del reloj del ordenador.** El script mide `TimeTradeServer() − TimeGMT()`
(`MedirDemoFTMO.mq5:389-395`), y `TimeGMT()` sale del reloj y del huso del ordenador. La fila 32
(`desfase_local_gmt_min`, −300 en las tres) y la 33 (horario de verano 0) dicen que el ordenador
estuvo en el huso de Lima, sin cambio de hora, las tres veces: un huso mal puesto movería el desfase
en horas enteras y se vería ahí. Que el reloj estuviera en hora lo acota otra fila: la 27
(`time_current`, la hora del último tick, que manda el servidor) frente a la 29 (`time_gmt`) da 180,
180 y 120 minutos menos 0 o 1 segundo. Confundir 120 con 180 pediría un error de 30 minutos.

**Observación concordante, que no discrimina:** el journal del EA del 2026-10-21
(`docs/validation/anexos/EA-CONEXION/demo-20261021-cierre/journal_20261021.jsonl`) da `desfase_s`
10800 (180 min); ese día los dos calendarios dan 180.

**La verificación del panel que A-28 llevaba dentro** (a qué hora se recalcula el límite diario:
medianoche de España o del servidor) no la hace ninguna ejecución, y Aleks no la ha declarado. Sale
de A-28 con su texto entero a una línea propia de la Next Action para Aleks. Si el panel dijera
medianoche del servidor, se reabre A-19 y `reloj_dia_riesgo` vuelve a DEFAULT_AMBIGUOUS, como decía
A-28; hasta entonces `reloj_dia_riesgo` sigue CONFIRMED en `civil_operativa` por el reglamento
(ADR-0027).

**El calendario de cierres** (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`, ADR-0068)
declara sus horas en `America/New_York` porque una Trading Update decía que el servidor cambia de
hora con EE. UU.: A-28 lo confirma con la medida, ningún cierre cambia y la cabecera deja de ser
PROVISIONAL en eso (recuadro en ADR-0068).

### 2. `anclaje_h4`: una DERIVACIÓN, no la medida de ADR-0027 §4

Con 120 y `us`, del 2026-01-01 al 2027-12-31 (730 días, `zoneinfo`), la medianoche del servidor cae
a las 17:00 de Nueva York **todos los días**. Es una derivación del modelo: con base 120 y el
calendario de EE. UU., el servidor es Nueva York + 7 h siempre, así que no podía salir otra cosa. No
es la medida que pide ADR-0027 §4 -«se verifica contra la rejilla H4 real del servidor de FTMO»-,
porque ninguna ejecución lee una vela. `anclaje_h4` no cambia de valor ni de estado. **La rejilla
real la mide la capa de R6a con el EA escribiendo en el journal de la demo la hora de apertura de
las velas H4 (`iTime`), antes de R6a.7 y de F33** (recuadro en ADR-0027 §4, que enmienda «en la
misma medición»).

### 3. La comisión: 2,50 USD por lote y lado

- **Medido** (filas 54 y 55 de la 2 y de la 3, con 1,00 lote, fila 53): −2,50 en la apertura y
  −2,50 en el cierre, las dos veces. La 1 (0,01 lotes) cobró −0,03 y −0,03, que es 0,025 redondeado
  al céntimo: cuadra con una tarifa proporcional al volumen y sin mínimo, que ADR-0071 §3 suponía
  y no podía distinguir.
- **Lo que fija:** `firma_comision_usd_por_lote` pasa de 5 a **2.50**, CONFIRMED con fuente este ADR;
  `firma_comision_por_lado` sigue en true. El bróker simulado carga la mitad que antes en cada lado
  (informe §0.d: baja menos el saldo, y por él el margen libre, el lote siguiente y los frenos).
- **Una consecuencia medida antes de cambiarlo** (informe §0.e): la cuenta del 7 de agosto de 2026
  (construcción, cuatro operaciones del trader repetidas con el tope de volumen subido a 100 y sin
  margen) se suspendía por pérdida diaria con 5 (peor equidad 94.485,53, 514,47 bajo el límite de
  95.000) y con 2,50 no (95.515,78, 515,78 por encima). La regresión que fija ese corte
  (`tests/regression/test_cuenta_7_de_agosto.py`) no fija un importe ni un saldo, así que el cambio
  del perfil y sus tests espera a la respuesta del consultor (informe, decisión 3).
- **Cómo se lee el «commission: 5» de la API** (R12, FTMO-REGLAS.md): 5 USD por lote **de ida y
  vuelta**, la mitad en cada lado, que es lo que FTMO dijo el 2026-09-29 («50 % al abrir, 50 % al
  cerrar»). Es una lectura compatible con la medida, no una respuesta de FTMO: el asterisco de
  «USD/LOT*» (heredado 27) sigue en A.2, que es de Aleks con FTMO.
- **El tope del paso 8 de la 3** se calculó con 5,00 por lado (fila 73, la constante del script,
  MARGEN-PENDIENTE.md punto 4): más caro que lo medido, así que sus peores casos (988,27, 118,80,
  998,92 y 981,40 USD) quedan del lado seguro del tope de 1.000.

### 4. El paso 8 (MARGEN-PENDIENTE.md §0.d): enmienda de ADR-0081 §4

Con la regla de lectura escrita antes de ejecutar, la 3 da:

| medida | resultado | filas |
|---|---|---|
| M1 · rechaza al colocar una pendiente sin margen libre | **no**: la acepta (10009) con margen al ask 100.010,25 y libre 99.989,55 | 74-76 |
| M2 · una stop viva carga margen | **no**: margen, libre e inicial no cambian (Δ 0,00 < 0,10 × 2.021,94) | 78-90 |
| M3 · suma las pendientes al colocar otra | **no**: las dos de 14,69 lotes se colocan | 92-97 |
| M4 · comprueba el margen al llenar | **no concluyente**: `no_salto` en 120 s | 99-111 |

Y la tasa de margen de la buy stop en el símbolo es **0;0** (inicial;mantenimiento, fila 65; la de
una compra, 1;1, fila 66). **Eso desmiente lo que ADR-0081 §4 da por hecho** -que una pendiente stop
RESERVA margen mientras vive y que se comprueba al colocarla- en esta prueba. Por eso este ADR
**enmienda ADR-0081 §4**:

- **(a) El límite del lote del bot (ADR-0081 D1-D2) no cambia.** El tope por margen lo pone el bot;
  con M4 sin medir sigue abierto que MT5 compruebe el margen al llenar.
- **(b) El bróker simulado no cambia en esta rama.** Su reserva de margen por pendiente stop
  (`broker.py`, `margen_usado`) y su comprobación al colocar quedan como **SUPUESTO CONSERVADOR
  declarado**: en las corridas del arnés sobre construcción no han tenido efecto medido (cero
  rechazos por `margen_libre` y ninguna orden colocada con otra viva; informe §0.f). Con una sola
  orden viva a la vez la reserva no cambia ningún lote: al colocar no hay otra que reservar, y al
  llenar el bróker devuelve la reserva propia (`libre_extra`).
- **(c)** Línea nueva de Technical Debt: el bróker simulado reserva margen por pendiente stop y
  comprueba al colocar, la prueba de FTMO no (tasa 0), sin efecto medido; se decide antes de R6a.6,
  que no la porta al EA sin esa decisión.
- **(d) Para R6a.7:** la tasa de margen de las pendientes stop es configuración del símbolo en la
  prueba, y la cuenta Swing real no la garantiza; el pre-vuelo la lee (`SymbolInfoMarginRate`) y la
  compara con lo esperado.

M4 queda declarado sin medir y no abre ambigüedad.

**La fórmula del margen** (ADR-0081 §4; FTMO-P-D1.md §3) casa con las dos notas del paso 6: 1,00 ×
100.000 × 1,11623 / 30 = 3.720,77 (la 2) y 1,12329 → 3.744,30 (la 3); y la de M1, 26,71 lotes al
ask 1,12329, da 100.010,24, el 100.010,25 del CSV con el redondeo de MT5.

### 5. El nivel exacto (ADR-0057 §2): sigue PROVISIONAL

| ejecución | sell stop | buy stop | sell limit | buy limit |
|---|---|---|---|---|
| 1 (filas 39-42) | viva | rechazada (10015) | llenada al instante, 3 puntos mejor | rechazada (10015) |
| 2 (filas 39-42) | viva | viva al leerla; su borrado devolvió 10013 | viva | llenada al instante, a su precio |
| 3 (filas 39-42) | llenada al instante | llenada al instante | viva | viva |

Tres ejecuciones, tres patrones distintos. Este script no puede decidirlo: no registra la cotización
del servidor en el instante de la comprobación, así que no distingue una regla del servidor de que
el precio se moviera. No hay más ejecuciones previstas. El simulador no cambia; lo observa el
journal de R6a cuando el EA coloque órdenes en la demo. Recuadros en ADR-0057 §2 y ADR-0071 §4.

ADR-0057 §1 (la stop se llena al precio del tick, nunca mejor que el nivel) y §3 (el lado
equivocado se rechaza, también al modificar) se repiten en la 2 y la 3 (filas 57-58: 0,0 puntos;
filas 34-37, 43-46, 49 y 51: 10015).

### 6. La ficha y los swaps (paso 1)

| dato (fila) | registro / perfil | la 1 | la 2 | la 3 |
|---|---|---|---|---|
| dígitos (6), point (7) | 5; 0,00001 | 5; 0.00001 | 5; 0.00001 | 5; 0.00001 |
| contrato (8) | 100000 | 100000.00 | 100000.00 | 100000.00 |
| lote mínimo (9), paso (11) | 0.01; 0.01 | 0.01; 0.01 | 0.01; 0.01 | 0.01; 0.01 |
| stops level (4), freeze level (5) | 0; 0 (ADR-0071) | 0; 0 | 0; 0 | 0; 0 |
| volumen máximo (10), límite (12) | 50; 0 | 50.00; 0.00 | 50.00; 0.00 | 50.00; 0.00 |
| llenado, ejecución, caducidad (13-15) | FOK IOC, mercado, 15 | igual | igual | igual |
| apalancamiento (24), modo de margen (25) | 30; hedging | 30; HEDGING | 30; HEDGING | 30; HEDGING |
| modo de swap, triple (18-19) | puntos, miércoles | igual | igual | igual |
| swap largo (16) | −9,49 | −9,41 | −9,74 | −10,06 |
| swap corto (17) | 0,36 | 0,10 | 0,42 | 0,40 |

**Todo coincide salvo los swaps. A-27 no se reabre:** sus cinco parámetros (`instrumento_digitos` 5,
`instrumento_contrato` 100000, `instrumento_lote_minimo` 0.01, `instrumento_lote_paso` 0.01 e
`instrumento_stops_level` 0) se repiten en la 2 y la 3, y ADR-0071 §6 ata la reapertura a ellos.

**Los swaps: el valor del perfil no cambia** (respuesta del consultor a la PARADA, punto 1). Las
tres lecturas, con su fecha: largo −9,41 (2026-10-09), −9,74 (2026-10-29) y −10,06 (2026-11-05);
corto 0,10, 0,42 y 0,40 los mismos días; el perfil dice −9,49 y 0,36, la API leída el 2026-09-25
(fuente ADR-0050). Un swap cambia cada día y no se fija con una lectura (ADR-0071 §5); no se
renueva porque no decide nada, y su descripción lo dice.

**Por qué no decide nada: ninguna operación del bot puede seguir abierta a la medianoche del
servidor** (verificado en el repo):
- RN-002 (`knowledge/spec/strategy_spec.yaml:910-966`) cierra a mercado toda operación abierta
  cuando a su vela H4 le queda `cierre_h4_antelacion` (1 minuto) o menos, y también al alcanzar
  `ventana_fin`; su forma, `:954-964`, con `cierre_forzoso_fin_ventana` = `si`
  (`parametros.yaml:387-397`) y `cierre_h4_antelacion` = 1 (`:398-415`). El predicado es `vence_vela_h4` (`engine/primitivas.py:142-151`),
  que da SÍ también en el propio límite, para que nada llenado en el último minuto cruce a la vela
  siguiente.
- La rejilla H4 empieza en `anclaje_h4` = 17:00 de Nueva York, que con 120 y `us` es la medianoche
  del servidor (§2): **la medianoche del servidor es una frontera de la rejilla H4**, así que ninguna
  operación puede cruzarla viva. Y la ventana de la operativa son las dos velas H4 que empiezan en
  ancla + 8 h y ancla + 12 h (`sesiones_primera_vela_h4` = 3, `parametros.yaml:262-276`;
  `ventana_inicio` y `ventana_fin`, `:354-386`; ADR-0069): lo último que puede estar abierto se cierra un minuto antes de las 16:00 del servidor,
  ocho horas antes de su medianoche.
- RN-035 (`strategy_spec.yaml:968-1041`) retira además la orden sin llenar en el mismo minuto, y
  RN-037 (`:1043-1074`) no deja colocar ninguna en él.

Una diferencia de modelo, sin efecto: el bróker simulado cobra el swap a la medianoche de
`huso_corte` del perfil (`engine/broker.py:960-973`), no a la del servidor, que es donde MT5 hace el
rollover. Con ninguna operación viva en ninguna de las dos medianoches, no cambia nada; queda dicho
por si un día el bot pasara la noche.

### 7. El deslizamiento: observaciones, no un modelo

`deslizamiento_fijo_puntos` (`knowledge/simulador/llenado.yaml`) sigue en 0. Lo observado a mercado:
la 1, +2 al abrir y −2 al cerrar, y +1 en la buy stop (ADR-0071 §5, con 0,01 lotes); la 2, +2,0 al
abrir y 0,0 al cerrar (filas 54-55) y 0,0 en la buy stop (fila 58); la 3, 0,0, 0,0 y 0,0, fuera de
la franja. Siete muestras de un minuto no son un modelo: lo mide el grabador de spread y ticks de
F17 (heredado 10).

## Problema que resuelve

A-28 seguía ABIERTA con sus dos parámetros en UNKNOWN; la comisión del perfil era un supuesto
conservador a la espera de la 2; ADR-0081 §4 daba por hecho cómo trata MT5 el margen de una
pendiente stop sin haberlo medido; y el nivel exacto, la ficha y el deslizamiento esperaban a la 2 y
la 3 (ADR-0071 §3-§6). Faltaba una fuente citable para lo medido.

## Alternativas consideradas

1. Una NOTA en ADR-0081 §4 en vez de enmienda (el plan primero del consultor).
2. Dejar la comisión en 5 como supuesto conservador.
3. Esperar a medir la rejilla H4 real para decidir A-28.
4. Un ADR que cite los manifiestos y cada fila, decida A-28 por su pregunta (desfase y calendario),
   fije la comisión y enmiende ADR-0081 §4 (la elegida).

## Por que elegimos esta opcion

Es la puerta de ADR-0071 para lo que no es estrategia. A-28 pregunta el desfase y el calendario, y las
tres medidas dejan una sola opción. La comisión es un importe medido dos veces con 1,00 lote y una con
0,01, que casan. Y la medida del paso 8 contradice lo que ADR-0081 §4 da por hecho.

## Por que descartamos las demas

- La 1: la medida desmiente lo que §4 da por hecho y lo que modela el bróker simulado; una nota lo
  dejaría escrito como verdad.
- La 2: un valor conservador sin medir tenía sentido sin medida; con ella, duplica el coste.
- La 3: la rejilla no es la pregunta de A-28, y medirla es trabajo del EA (R6a).

## Impacto

- `data/manifests/demo_ftmo/`: los manifiestos de la 2 y la 3 (el de la 1 no se toca).
- `knowledge/spec/parametros.yaml`: `broker_offset_base` 120 y `broker_dst` `us`, CONFIRMED; las
  frases que A-28 dejaba en futuro; `anclaje_h4` y `reloj_dia_riesgo` sin cambio de valor ni de
  estado, con su descripción reescrita. `ambiguedades.yaml`: A-28 DECIDIDA. `spec_version` y
  `docs/spec/` regenerados.
- `knowledge/cuentas/ftmo-2step-swing-100k.yaml`: `firma_comision_usd_por_lote` 2.50 (tras la
  decisión 3 del informe); el yaml de cierres, su cabecera.
- Tests: la comisión, `test_kit` y uno nuevo para el `dataset_id` de los manifiestos de la demo.
- Recuadros: ADR-0081 §4 (enmienda), ADR-0071 §3 y §4, ADR-0057 §2, ADR-0027 §4, ADR-0068 (el
  huso del calendario) y ADR-0082 (A.1); y DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c (el LF).
- Ningún cambio en `src/`, en `tools/mql5/` ni en `scripts/leer_demo_ftmo.py`.
- `docs/runbooks/DEMO-FTMO.md`: las tres ejecuciones.

## Fecha / fase

2026-11-06 · post-F14, rama `trabajo/demo-ejecuciones-2-3`.

## Estado

ACTIVE
