---
status: ACTIVE
date: 2026-09-26
phase: post-F14 (rama `trabajo/ticks-llenado`, sesión nocturna)
---

# 0052 · El bróker simulado

> **ACEPTADO el 2026-09-26** por el consultor, tras su revisión, sobre lo escrito en la sesión
> autónoma de la noche anterior (`docs/validation/TICKS-LLENADO.md`). La decisión nocturna de este
> ADR (DN-6, el corte del swap) queda PROVISIONAL hasta medir el corte real en la plataforma
> (A-28); las demás decisiones nocturnas, resueltas en ADR-0051 §7. Los ticks son obligatorios
> para toda simulación que cuente (ADR-0051 §8): este bróker cae al respaldo M1 solo en una hora
> perdida, y lo marca.

## Decision

El **bróker simulado** es la mitad del simulador que ADR-0050 dejó pendiente: convierte las órdenes
de una estrategia en operaciones con instantes, precios, lotes y costes, usando el modelo de
llenado de ADR-0051, y alimenta la capa de cuenta con cada llenado, comisión y swap. Vive en
`engine/broker.py` como estado puro sobre un `Mercado`; sin cifras de negocio y sin nada que asuma
un instrumento ni una firma: los límites y los costes vienen del perfil de cuenta
(`knowledge/cuentas/`), lo elegible del llenado de `knowledge/simulador/llenado.yaml`.

### 1. Ciclo de vida de una orden

Una orden límite está **colocada**, puede ser **modificada** (precio, stop, objetivo) mientras
esté pendiente, y termina **llenada**, **cancelada** o **expirada** (si se colocó con un instante
de expiración). Una orden que un límite del perfil no admite queda **rechazada** en el acto y el
rechazo se registra con su motivo; no se encola. Una orden llenada abre una **posición** con stop
y objetivo, que se cierra **por stop**, **por objetivo** o **a mercado** (cierre manual, al último
tick anterior o igual al instante, o al cierre de la M1 del minuto si no hay ticks). Cada orden
lleva su historial de estados con instante.

### 2. El modelo de llenado decide cada evento

El bróker no decide precios: pregunta a ADR-0051. `primer_llenado_limite` para las pendientes y
`primera_salida` para las vivas, desde el instante en que cada una quedó colocada, modificada o
abierta (ese instante es exclusivo: el tick en que se decidió no cuenta) y hasta el instante al
que se avanza. Los eventos se aplican en orden de instante; a igual instante, por tipo y por id. El
tick del último evento procesado sí puede llenar OTRA orden pendiente (dos límites al mismo precio
se llenan en el mismo tick).

### 3. Lo que la cuenta recibe

Por cada posición cerrada, una `cuenta.Operacion` (ADR-0050): apertura y cierre con su instante y
su precio en moneda, los **cargos** —la comisión por lote del perfil, en cada lado si
`firma_comision_por_lado` lo dice y una vez si no; un **swap** por cada corte diario del perfil
que la posición cruce viva, con el signo de los puntos del perfil (negativo = cuesta)— y las
**marcas**: el PEOR precio de cada minuto vivo para el lado de la posición (el BID más bajo de una
larga, el ASK más alto de una corta; con respaldo M1, la mínima o la máxima más el spread
supuesto). Es lo que la cuenta vigila para la pérdida diaria por equity flotante, y es pesimista a
propósito. **La equity de la cuenta en cada marca es el saldo más el flotante del bróker**, y un
test lo comprueba.

**DECISIÓN NOCTURNA 6 (conservadora): el corte del swap es la medianoche del huso del perfil**
(`firma_huso_corte`, CE(S)T para FTMO). Motivo: el reloj del servidor de FTMO es «GMT+2 +DST» sin
calendario publicado (A-28, R10), y CE(S)T es lo más cercano que hay con fuente; con el bot
cerrando a las 15:00 del trader (RN-002) ninguna posición cruza ese corte, así que hoy no cambia
nada. Alternativas: 00:00 UTC; no modelar swaps hasta medir A-28.

### 4. Los límites del perfil, como rechazos registrados

`firma_volumen_max_lotes` (una orden con más lotes se rechaza), `firma_ordenes_simultaneas_max`
(órdenes pendientes más posiciones vivas) y `firma_posiciones_dia_max` (posiciones abiertas en el
día del huso del perfil). Un rechazo no es un error: queda en la traza con su instante y su motivo,
y la estrategia lo ve.

### 5. El contrato que el motor tendrá que cumplir (NO se cablea aquí)

El motor de reglas sigue sin tocarse. Cuando se cablee, tendrá que:

- decidir **al cierre de cada M1** (`Estrategia.decidir(broker, minuto, cerradas)`,
  `engine/simulacion.py`), después de que el bróker haya procesado todo hasta ese instante y solo
  con las velas cerradas hasta él;
- emitir órdenes SOLO por el contrato del bróker: `colocar_limite`, `modificar`, `cancelar`,
  `cerrar_a_mercado`, cada una con su instante, en puntos y con lotes `Decimal`;
- leer los hechos de origen `broker` de la spec del propio bróker, no fijarlos por regla
  (ADR-0028 §5): **`operacion_abierta`** y **`orden_limite_pendiente`** salen de `Broker.hechos()`;
- alimentar los acumuladores de la firma (`perdida_dia_firma`, `perdida_total_firma`) desde la
  capa de cuenta con las marcas que este bróker produce (ADR-0050 §5), y aplicar ahí el margen de
  ADR-0031, que el bróker no conoce;
- y, cuando existan ticks para la fase de riesgo (ADR-0028), evaluar los gates de la firma sobre
  las marcas del bróker, no solo al cierre de M1.

Lo que el bróker NO decide: cuándo se coloca una orden, dónde va el stop, cuántos lotes (eso es
la spec: RN-011, RN-015, RN-027...), ni el cierre forzoso a fin de ventana (RN-002): la estrategia
lo pide con `cerrar_a_mercado`.

## Problema que resuelve

ADR-0048 H4 y ADR-0049 H4 dejaron escrito que sin bróker simulado el motor no puede producir
ninguna operación y que diez gates en DESCONOCIDO prohíben abrir. ADR-0050 construyó la capa de
cuenta y la dejó esperando operaciones con marcas y cargos. Este ADR pone la pieza que las
produce, con el modelo de llenado de ADR-0051 detrás, y deja el cableado al motor descrito y no
inventado.

## Alternativas consideradas

1. Bróker como estado puro sobre un `Mercado`, eventos en orden de instante, marcas por minuto
   pesimistas, rechazos registrados (elegida).
2. Cablear ya el intérprete de la spec al bróker en esta rama.
3. Marcas por tick (cada tick una marca) en vez del peor precio por minuto.
4. Swaps no modelados hasta medir el reloj del servidor.

## Por que elegimos esta opcion

Porque cada pieza es comprobable sola: el ciclo de vida con ticks sintéticos, la coherencia con la
cuenta marca a marca, los rechazos por cada límite, y la estrategia de juguete de la Fase 5 que
recorre todo el camino hasta el veredicto de la firma. Y porque el peor precio por minuto es
suficiente para lo que la cuenta vigila (¿cruzó el límite en algún instante?) y mantiene las
operaciones pequeñas.

## Por que descartamos las demas

- **(2)** el cableado exige resolver los huecos de ADR-0050 §5 (signo del acumulador, un solo
  reloj) y tocar el motor, prohibido esta noche.
- **(3)** multiplica el tamaño de cada operación por cientos sin cambiar ninguna decisión de la
  cuenta: el mínimo del minuto ya dice si el límite se cruzó.
- **(4)** dejaría sin cargo una posición que cruzara el corte; hoy no pasa (RN-002), pero el
  bróker de una estrategia sintética sí puede dejarla abierta, y es mejor que cueste.

## Impacto

- `src/botsito/engine/broker.py`: `Broker`, `Orden`, `Posicion`, `Rechazo`, `Traza`,
  `ReglasBroker`.
- `src/botsito/engine/simulacion.py`: `MercadoDia`, `mercado_de_construccion` (por la compuerta
  del arnés), `Estrategia`, `simular_dia`, `simular_fase`, `reglas_broker_de`.
- `src/botsito/engine/simulador_config.py` y `knowledge/simulador/llenado.yaml` (ADR-0051).
- Tests: `tests/unit/test_broker.py`, `tests/unit/test_simulacion.py` (la estrategia sintética,
  fuera de `src`).
- Sin tocar: la spec, `ambiguedades.yaml`, el motor de reglas, el arnés.

## Fecha / fase

2026-09-26 · escrito en la sesión nocturna y ACEPTADO por el consultor el mismo día, rama
`trabajo/ticks-llenado`. Next Action 33.

## Estado

ACTIVE
