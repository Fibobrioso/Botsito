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

## Fase 2 · ticks de construcción — EN CURSO

Código sellado (`data/ticks.py`, `domain/ticks.py`, CLI `data download-ticks` y `check-ticks`,
16+1 tests sin red, `scripts/ticks_integridad.py` y `scripts/ticks_spread.py`). Formato del
proveedor medido sobre una hora de abril: `>IIIff`, ms en la hora, ASK, BID, volúmenes float.

**Tolerancia de integridad, fijada ANTES de comparar:** una M1 cuadra si existe en las dos
fuentes y |ΔO|, |ΔH|, |ΔL|, |ΔC| ≤ 2 puntos; el volumen no se compara. No se toca después.

**Lo que pasó con la descarga (medido):** dos descargas en paralelo perdían horas (503 con
esperas de 5-20 s). Una sola secuencial con esperas 15-60 s fue de 2 s por hora al empezar a
6,5 minutos por hora al saturarse: un mes entero (720 horas) no cabe en la noche. Ver DN-5.

## Fase 3 · modelo de llenado en código — pendiente

## Fase 4 · bróker simulado — pendiente

## Fase 5 · punta a punta con estrategia sintética — pendiente

## Fase 6 · repetición descriptiva de las operaciones del trader — pendiente

## Fase 7 · medición del instante con ticks — pendiente

## Decisiones nocturnas (pendientes de validar)

- **DN-0 (proceso).** La guardia de ADR solo admite `status: ACTIVE|SUPERSEDED` y el primer token
  de `## Estado` en ese conjunto. Los ADR nocturnos llevan `ACTIVE` en el campo y PROPUESTO en el
  título, en el Estado y en los índices. Alternativa: cambiar la guardia para admitir PROPUESTO;
  no se hace de noche porque cambia una regla del repositorio.
- **DN-1..DN-4**: las del modelo de llenado, en ADR-0051 §1, §3, §4 y §6.
- **DN-5 (Fase 2): los ticks se congelan solo para los DÍAS DEV de construcción y las HORAS 05-13
  UTC** (07:00-16:00 CEST: la ventana del trader 07:00-15:00 más una hora), con 2 s de pausa entre
  peticiones, y la selección queda escrita en el manifiesto (`seleccion`). Motivo: el ritmo del
  servidor, medido arriba. Alternativas: el mes entero (no cabe en la noche); solo los minutos de
  las operaciones (no serviría al bróker ni a la medida del spread). El mes entero se baja de día
  con el mismo comando sin `--solo-dias-dev`, y es otro dataset. Consecuencia: la integridad y el
  spread se miden sobre esas horas; fuera de ellas el modelo de llenado usa el respaldo M1 y lo
  marca.

## Paradas

- Ninguna todavía.
