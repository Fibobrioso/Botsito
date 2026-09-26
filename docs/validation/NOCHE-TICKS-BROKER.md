# Registro vivo de la noche del 2026-09-26: ticks, llenado, bróker

Rama `trabajo/ticks-llenado`, desde `main` en `29e42b5`. Sesión autónoma (Aleks duerme). Sin
merge, sin tag y sin push: el cierre lo decide Aleks por la mañana. Cada fase cierra con sus
commits sellados antes de empezar la siguiente. Si la sesión se corta, aquí está dónde retomar.

Guardas verificadas al empezar: `PREREGISTRO.md` con blob `52649183…`, el declarado; cero
autorizaciones en `knowledge/cases/holdout/`. Solo abril y agosto de 2026 en todo lo que se
descarga o ejecuta; mayo, marzo, febrero y septiembre, ni se descargan ni se ejecutan. Antes de
descargar nada se guardó la salida de `kit check --sesion 2026-09-09-sesion-01` y de `fidelidad
check --artefacto eurusd-2026-09` para compararlas byte a byte después.

## Fase 0 · comisión conservadora — HECHA

`firma_comision_por_lado` pasa de UNKNOWN a CONFIRMED `true` en
`knowledge/cuentas/ftmo-2step-swing-100k.yaml`: se cobra en CADA lado (apertura y cierre), por
decisión del consultor del 2026-09-25 (PROJECT_STATE, Decisions and Rationale), pendiente de
confirmar con FTMO; la descripción sigue citando R12 NO ENCONTRADA. Fuente formal: ADR-0050, que
es el ADR de la capa de cuenta (los estados del registro son solo los de ADR-0012; la decisión no
tiene ADR propio y no se inventa uno). Test: el perfil ya no se niega a leerla; quedan tres sin
valor (objetivo y días de la fondeada, ratio de la guardia). Recuadro de corrección en
`SIMULADOR-CUENTA.md` §2.

## Fase 1 · ADR del modelo de llenado — HECHA

ADR-0051 «El modelo de llenado», PROPUESTO. Fija: el lado del spread por orden (compra al ASK,
vende al BID); las límites y los objetivos exigen pasar estrictamente el nivel y los stops saltan
al toque (DN-1); con ticks el orden real, y un tick que cruce stop y objetivo a la vez es stop
(DN-2); respaldo M1 pesimista, stop primero (ADR-0049 H4), marcado `respaldo_m1`; sin
deslizamiento fijo, solo el de hueco de los ticks (DN-3); spread de cada tick y, sin ticks, el
percentil 90 por hora medido en construcción (DN-4), en `knowledge/simulador/llenado.yaml`.

## Fase 2 · ticks de construcción — HECHA (con DN-5, selección de días y horas)

Código sellado (`data/ticks.py`, `domain/ticks.py`, CLI `data download-ticks` y `check-ticks`,
16+1 tests sin red, `scripts/ticks_integridad.py` y `scripts/ticks_spread.py`). Formato del
proveedor medido sobre una hora de abril: `>IIIff`, ms en la hora, ASK, BID, volúmenes float.

**Tolerancia de integridad, fijada ANTES de comparar:** una M1 cuadra si existe en las dos
fuentes y |ΔO|, |ΔH|, |ΔL|, |ΔC| ≤ 2 puntos; el volumen no se compara. No se toca después.

**Resultado (mañana del 2026-09-26):** el proceso desacoplado terminó solo tras el corte, y una
segunda pasada sobre la caché (pausa de 5 s, 5 intentos con esperas 4-16 s) recuperó casi todas
las horas perdidas. Datasets congelados, verificados con `check-ticks --hashes`:
`eurusd-ticks-2026-04-1d189bdd` (21 días dev, horas 05-13 UTC, 182 de 189 horas presentes, 7
perdidas, 687.585 ticks) y `eurusd-ticks-2026-08-75bd3a08` (21 días dev, 186 de 189, 3 perdidas,
484.035 ticks). Los dos datasets anteriores de la primera pasada se descartaron sin comitear: el
de abril había quedado incoherente (un `rm` mío borró dos CSV a mitad de descarga; el descargador
recrea ahora la carpeta antes de cada día) y el de agosto tenía 28 horas perdidas.

**Integridad, con la tolerancia fijada antes** (`docs/validation/TICKS-INTEGRIDAD-SALIDA.txt`):
de las M1 del repo cuyo minuto tiene ticks, cuadran el 100 % (22.075 de 22.075: abril 10.915,
agosto 11.160) y no discrepa ninguna; las 39.731 M1 restantes no tienen ticks porque quedan fuera
de la selección (días no dev u horas fuera de 05-13 UTC) o en las 10 horas perdidas. Ningún minuto
con ticks carece de M1 en el repo.

**Spread medido** (`docs/validation/TICKS-SPREAD-SALIDA.txt`, ASK − BID en puntos, ventana
07:00-15:00 del trader): media 2,8-3,4 según la hora, p50 3, p90 5 de 07 a 11 y a las 14, 4 a las
12 y 13; fuera de la ventana p90 4; máximo aislado 121 a las 14:00 de abril. Con eso,
`knowledge/simulador/llenado.yaml` lleva el p90 por hora (DN-4).

**`kit check --sesion 2026-09-09-sesion-01` y `fidelidad check --artefacto eurusd-2026-09`
salen IDÉNTICOS byte a byte** a los guardados antes de descargar nada (comparados con `cmp`).

**Lo que pasó con la descarga de noche (medido):** dos descargas en paralelo perdían horas (503 con
esperas de 5-20 s). Una sola secuencial con esperas 15-60 s fue de 2 s por hora al empezar a
6,5 minutos por hora al saturarse: un mes entero (720 horas) no cabe en la noche. Ver DN-5.

## Fase 3 · modelo de llenado en código — HECHA

`engine/llenado.py`: funciones puras sobre un `Mercado` (ticks por minuto, M1 de respaldo):
`primer_llenado_limite` y `primera_salida` con las reglas de ADR-0051 (lado del spread, paso
estricto para límites y objetivos, toque para stops, orden real con ticks, respaldo pesimista con
el stop primero y el evento en el cierre de la vela, hueco a la apertura, deslizamiento fijo
opcional). Tests: sin mirar al futuro, determinismo, stop y objetivo en la misma M1 (ticks frente
a respaldo), límite tocada justo en su precio a cada lado, tramo sin ticks marcado, hueco.
`engine/simulador_config.py` lee `knowledge/simulador/llenado.yaml` con lectura estricta; el
fichero se escribe cuando el spread esté medido (Fase 2).

## Fase 4 · bróker simulado — HECHA

ADR-0052 «El bróker simulado», PROPUESTO. `engine/broker.py`: ciclo de vida completo de la orden,
posición con stop y objetivo, cierre por stop, objetivo o a mercado, rechazos por límite del
perfil registrados, comisión por lado, swap por corte diario del huso del perfil (DN-6), marcas
del peor precio por minuto para la cuenta, hechos de origen broker derivados del estado; sin
cifras de negocio ni nada que asuma un instrumento o una firma. NO se cablea al motor: el
contrato del motor queda en ADR-0052 §5. Tests: ciclo de vida, cancelada/expirada/manual, stop
al precio del tick, rechazos por cada límite, equity de la cuenta = saldo + flotante en cada
marca, respaldo M1 marcado, swap y comisión, determinismo y sin mirar al futuro.

## Fase 5 · punta a punta con estrategia sintética — HECHA

`engine/simulacion.py`: `MercadoDia` (el mercado de un día dev de construcción por la compuerta
del arnés, con los datasets de ticks que existan y la M1 de respaldo), el contrato `Estrategia`
(decidir al cierre de cada M1 con las velas cerradas; recoger al cerrar la ventana), `simular_dia`
y `simular_fase` (la cuenta persiste entre días), `reglas_broker_de(perfil)`. La estrategia de
juguete vive en `tests/unit/test_simulacion.py`, marcada SINTÉTICA y fuera de `src`. Tests:
determinismo, sin mirar al futuro, una que pierde siempre acaba SUSPENDIDA en el instante exacto,
una que gana poco sin los días mínimos queda EN_CURSO, un día sin ticks va entero por el respaldo
marcado, y un día dev real por la compuerta si hay datos.

## Fase 6 · repetición descriptiva de las operaciones del trader — pendiente

## Fase 7 · medición del instante con ticks — pendiente

## Decisiones nocturnas (pendientes de validar)

- **DN-0 (proceso).** La guardia de ADR solo admite `status: ACTIVE|SUPERSEDED` y el primer token
  de `## Estado` en ese conjunto. Los ADR nocturnos llevan `ACTIVE` en el campo y PROPUESTO en el
  título, en el Estado y en los índices. Alternativa: cambiar la guardia para admitir PROPUESTO;
  no se hace de noche porque cambia una regla del repositorio.
- **DN-1..DN-4**: las del modelo de llenado, en ADR-0051 §1, §3, §4 y §6.
- **DN-7 (proceso, Fase 4): en ADR-0051 se quitó el bloque `ids-inexistentes` que declaraba a
  ADR-0052**, porque la guardia falla cuando un id declarado inexistente pasa a existir. Es el
  único cambio a un ADR PROPUESTO y no toca su contenido.
- **DN-6 (Fase 4): el corte del swap es la medianoche del huso del perfil** (CE(S)T para FTMO),
  porque el reloj del servidor no tiene calendario publicado (A-28); ADR-0052 §3.
- **DN-5 (Fase 2): los ticks se congelan solo para los DÍAS DEV de construcción y las HORAS 05-13
  UTC** (07:00-16:00 CEST: la ventana del trader 07:00-15:00 más una hora), con 2 s de pausa entre
  peticiones, y la selección queda escrita en el manifiesto (`seleccion`). Motivo: el ritmo del
  servidor, medido arriba. Alternativas: el mes entero (no cabe en la noche); solo los minutos de
  las operaciones (no serviría al bróker ni a la medida del spread). El mes entero se baja de día
  con el mismo comando sin `--solo-dias-dev`, y es otro dataset. Consecuencia: la integridad y el
  spread se miden sobre esas horas; fuera de ellas el modelo de llenado usa el respaldo M1 y lo
  marca.

## Paradas

- **La sesión se cortó a la 01:35 por el límite de uso**, con el árbol TODO ESTADIADO y SIN SELLAR
  (no dio tiempo a `make check`). Lo estadiado: Fase 3 (`engine/llenado.py` + 9 tests, verdes),
  su configuración (`engine/simulador_config.py`, `knowledge/simulador/README.md`, tests verdes;
  falta `llenado.yaml`, que espera al spread medido), Fase 4 (ADR-0052 PROPUESTO, `engine/broker.py`
  + 8 tests verdes, `engine/simulacion.py`), Fase 5 (`tests/unit/test_simulacion.py`, 6 verdes,
  estrategia sintética fuera de src), los scripts de las Fases 6 y 7 (escritos, SIN ejecutar: no hay
  manifiesto de ticks), el índice de ADR-0052 y la robustez del descargador. Para retomar:
  `make check > make-check.log 2>&1` y commits por pieza en el orden Fase 2 → 3 → 4 → 5.
- **Fase 2 no cerró: Dukascopy rechaza las conexiones.** Medido a la 01:33: con conexiones nuevas y 8 s
  de pausa, 1 de 4 horas responde 200 y el resto 503 o timeout; con una conexión persistente, 503 en
  las 6. Antes, entre las 00:50 y la 01:30, el ritmo fue de 2 s por hora al empezar a más de un minuto
  por hora, con horas perdidas. Lo bajado está en la caché cruda (`data/raw/EURUSD/ticks/`: abril 1 y 2
  completos, abril 3 parcial, algo de agosto 1 y 2); NO hay manifiesto ni dataset congelado, y `kit
  check` y `fidelidad check` no se han vuelto a comparar porque no se congeló nada. Para retomar:
  relanzar `scratchpad/descarga.cmd` (o `botsito data download-ticks ... --solo-dias-dev --horas 05-13
  --pausa 2`) cuando el servidor responda; la caché reanuda sola. Las Fases 6 y 7 dependen de esto.
- Las decisiones nocturnas DN-0 a DN-6 están arriba y en ADR-0051 y ADR-0052.
