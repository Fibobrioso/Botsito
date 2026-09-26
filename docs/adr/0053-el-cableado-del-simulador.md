---
status: ACTIVE
date: 2026-09-26
phase: post-F14 (rama `trabajo/cableado-simulador`)
---

# 0053 · El cableado del simulador (PROPUESTO: pendiente de aceptación del consultor)

> **PROPUESTO.** Escrito en una sesión autónoma con la regla de elegir siempre la opción más
> conservadora y anotarla como DECISIÓN pendiente de validar. El campo `status` dice ACTIVE porque
> la guardia de ADR no admite otro valor (ADR-0051, DN-0). Lo acepta o corrige el consultor.

## Decision

El simulador queda completo de punta a punta: **día → motor de reglas → órdenes → bróker →
llenado con ticks → capa de cuenta → veredicto FTMO y operaciones del bot para el criterio de
fidelidad**. Este ADR fija el cableado entre las piezas que ya existen —el intérprete del árbol
(ADR-0030, ADR-0048), el bróker (ADR-0052) con el modelo de llenado (ADR-0051) y la capa de cuenta
(ADR-0050)— sin tocar la spec ni el intérprete. Vive en `engine/cableado.py` (el bucle y el
motor cableado), `engine/primitivas_broker.py` (las primitivas que leen el bróker y la cuenta) y
`cuenta.CuentaViva` (la capa de cuenta incremental). Lo que la spec no da queda como HUECO CON
NOMBRE y la primitiva sigue NO_IMPLEMENTADA (ADR-0048 §2): no se inventa nada.

### 1. Las acciones del motor se traducen en peticiones al bróker (ADR-0052 §5)

El contrato del bróker es `colocar_limite`, `modificar`, `cancelar`, `cerrar_a_mercado`,
`mover_stop` (nuevo, para RN-014) y `hechos()`. Las acciones de la spec se traducen así, sobre una
**orden en preparación** (`OrdenEnPreparacion`) que nace cuando una regla liga una zona `Z`:

| acción de la spec | traducción |
|---|---|
| `dimensionar_lote {base, riesgo, sobre}` (RN-011) | anota en la orden la base del lotaje, el riesgo y su base de cálculo; **el lote se resuelve al colocar**, con el stop ya escrito (§1.1) |
| `escribir_stop_en_la_orden {donde, nivel}` (RN-011) | stop = entrada ∓ `nivel` (fracción) × distancia completa de la caja `Z` |
| `fijar_objetivo {multiplo, sobre, extension, parciales}` (RN-015) | objetivo = entrada ± `multiplo` × (la caja completa o la distancia al stop, según `sobre`); `extension` y `parciales` solo si sus parámetros lo dicen (hoy no) |
| `colocar_orden_limite {en: Z}` (RN-015) | `Broker.colocar_limite` con la orden preparada: entrada de la zona, lote, stop, objetivo; efecto `abrir_operacion`, así que un `gate` que prohíba o esté DESCONOCIDO la frena (ADR-0032, ADR-0048 §2) |
| `redondear_lote {a_la_baja, paso, minimo, contrato}` (RN-027) | redondea el lote de la orden en preparación hacia abajo al paso, no por debajo del mínimo |
| `cerrar_a_mercado {de: OP, si}` (RN-002, RN-030) | si el parámetro `si` vale `si`, `Broker.cerrar_a_mercado` de la posición ligada a `OP` (§1.2) |
| `retirar_orden_limite {de}` | `Broker.cancelar` (declarada sin regla que la use) |
| `reubicar_orden_limite {a: Z, cadencia}` (RN-006) | `Broker.modificar` con la entrada de la zona nueva |
| `mover_stop {de: OP, a, cuando}` (RN-014) | `Broker.mover_stop` de la posición ligada |
| `fijar {hecho, a}` | como hasta hoy (ADR-0048) |

**1.1 DECISIÓN pendiente de validar (el lote se resuelve al colocar).** RN-011 ejecuta
`dimensionar_lote` ANTES de `escribir_stop_en_la_orden`, y con `lotaje_base: hasta_stop_fraccion`
(ADR-0020) el lote depende de la distancia al stop, que todavía no está escrito, y la acción no
nombra `stop_fraccion_caja`. Para no leer un parámetro que la forma no nombra (ADR-0019 §1), la
acción anota qué base, riesgo y sobre usar, y el lote se calcula en `colocar_orden_limite`, cuando
la orden ya lleva stop: lote = riesgo % × base ÷ (distancia × contrato), redondeado por RN-027 si
hace falta. Alternativa: cambiar el orden de las acciones en RN-011 (toca la spec).

**1.2 DECISIÓN pendiente de validar (la ligadura `OP`).** El intérprete liga `OP` al VALOR del
hecho `operacion_abierta`, que para un hecho de origen bróker es `si`: no identifica una posición.
Con `operaciones_simultaneas_max = 1`, `OP` se resuelve a la única posición viva; con más de una,
la acción falla con error nombrado (no se elige una al azar). `OP.precio_entrada` (RN-014) es el
precio de entrada de esa posición.

**1.3 La zona `Z` es una ligadura de texto** (`zona:<id>`) que apunta a una `Zona` del contexto del
día: entrada (nivel 0), extremo (nivel 1), lado y `por` (el esquema que la produjo). Hoy ninguna
primitiva de mercado produce zonas (`toca_colocar_orden_limite`, `se_completa_zona_de_control`
siguen NO_IMPLEMENTADA por A-29 y A-35); una estrategia sintética puede producirlas en los tests.

### 2. Los eventos del bróker vuelven al motor como hechos de origen `broker`

Antes de cada evento del intérprete, `EstadoDia.broker` se rellena con `Broker.hechos()`:
`operacion_abierta` y `orden_limite_pendiente` (ADR-0028 §5). Los eventos del bróker desde el
evento anterior —llenada, stop, objetivo, cierre manual, expirada, rechazo— quedan en el contexto
del minuto, y los leen las primitivas de fuente `broker`:

| predicado | lectura |
|---|---|
| `operaciones_abiertas_alcanzan {tope}` (RN-018) | posiciones vivas ≥ `tope` |
| `se_activa_entrada {por}` (RN-010) | hubo un llenado en el tramo y el `por` de su orden casa (`cualquier_esquema` casa con los dos esquemas) |
| `salta_stop {}` (RN-012) | hubo un cierre por stop en el tramo |
| `se_cierra_operacion {resultado, por}` (RN-016, RN-017, RN-019) | hubo un cierre cuyo mecanismo casa: `salto_el_stop` si lo cerró el stop en su nivel original; `break_even` si lo cerró un stop movido a la entrada; si no, `ganancia` o `perdida` por el signo del P/L bruto; `cualquier_activacion` casa con todo `por` |

**2.1 DECISIÓN pendiente de validar (los eventos llegan al cierre de M1).** ADR-0028 §3 dice
«por evento del bróker»; aquí los eventos del bróker se entregan agrupados en el siguiente cierre
de M1, porque el intérprete solo corre ahí (ADR-0028 §2). Un llenado a las 09:03:20 se ve en el
evento de las 09:04. Alternativa: un evento extra del intérprete en el instante de cada evento
del bróker; exige que las primitivas de mercado sepan evaluarse fuera de un cierre de M1.

### 3. La capa de cuenta alimenta los acumuladores de la firma

`CuentaViva` avanza con los eventos del bróker: abre una posición al llenarse, marca cada minuto
con el peor precio (ADR-0052 §3), carga comisiones y swaps, cierra, y corta el día. Antes de cada
evento del intérprete expone los acumuladores de la spec:

- `perdida_dia_firma` = max(0, saldo al corte − magnitud vigilada mínima del minuto);
- `perdida_total_firma` = max(0, base total − magnitud vigilada mínima del minuto), con la base
  estática o arrastrando el saldo máximo según el perfil.

**3.1 DECISIÓN (el signo del acumulador, lo que ADR-0050 §5 dejó pendiente): se recorta en cero.**
Un acumulador con la equity POR ENCIMA de su base vale 0, no un número negativo: es lo
conservador, porque con `no_cabe_la_operacion` (RN-032) un valor negativo daría holgura de
sobra. Alternativa: dejarlo negativo.

**3.2 Las tres lecturas de un acumulador** (`alcanza_tope`, `se_acerca_al_limite`,
`no_cabe_la_operacion`) las hace la primitiva del acumulador, que las distingue por los argumentos
que recibe (el intérprete no le pasa el nombre del predicado, ADR-0030 §1): con `riesgo` y `sobre`
es la prospectiva; con `margen`, el freno; sin ellos, el tope. El tope y el margen son porcentajes
del capital inicial (`saldo_inicial_cuenta`); el riesgo prospectivo, `riesgo_por_operacion` sobre
`base_calculo_riesgo` (`saldo_actual` = el saldo de la cuenta). Comparación: mayor o igual (los
frenos de la estrategia disparan ANTES del límite); la cuenta suspende por debajo (ADR-0050).

**3.3 Huecos con nombre (siguen NO_IMPLEMENTADA):** `perdida_dia` y `perdida_semana` (los del
trader, RN-020) no declaran `magnitud` en la spec —saldo o equity— y no se supone; `cartuchos`
(RN-016) depende de `cartucho_criterio` y de `se_cierra_operacion` con esquema, que es geometría.

### 4. Un solo reloj

**El reloj del simulador es el del perfil de cuenta (`firma_huso_corte`)**, y el cableado
COMPRUEBA al arrancar que coincide con `huso_operativa` (que es lo que `reloj_dia_riesgo:
civil_operativa` significa, ADR-0027) en las medianoches de cada día del tramo: si divergen, se
niega a correr y lo dice. Motor, bróker y cuenta ven el mismo instante: el evento del intérprete en
el minuto `t` se evalúa después de que el bróker haya procesado hasta el último milisegundo
anterior a `t` y la cuenta haya marcado ese minuto; nada del minuto `t` en adelante es visible.

### 5. Las tres fases de ADR-0028 en el bucle

Por cada minuto `t` de la ventana del día, en este orden:

1. **Riesgo por tick:** `Broker.avanzar(t − 1 ms)` procesa llenados, stops y objetivos tick a
   tick (o con el respaldo M1 en una hora perdida); `CuentaViva` recibe los eventos y la peor marca
   del minuto de cada posición viva.
2. **Órdenes por evento del bróker:** los eventos del tramo se ponen a disposición de las
   primitivas de fuente `broker` y `EstadoDia.broker` se actualiza (§2, §2.1).
3. **Estrategia al cierre de M1:** el intérprete corre el evento en `t` a punto fijo con
   refracción; las acciones llaman al bróker (§1). Un `gate` de la firma (RN-029, RN-030, RN-031,
   RN-032) lee los acumuladores del punto 1: por eso la lectura es con la PEOR marca del minuto,
   no con el cierre.

**5.1 DECISIÓN pendiente de validar (el cierre de RN-030 se ejecuta al cierre de M1).** ADR-0028
§1 permite a la fase de riesgo cerrar a mercado por su cuenta, tick a tick. Aquí RN-030 se evalúa
con la peor marca del minuto (dispara como mínimo igual de pronto) pero el cierre se ejecuta al
precio del cierre de M1, que puede ser mejor o peor que el del tick. Alternativa: un cierre
intravela en la primera marca que cruce; exige evaluar el gate dentro de `Broker.avanzar`.

### 6. Estado entre días

La cuenta PERSISTE en todo el tramo (ADR-0050, ADR-0049 H6): un `CuentaViva` por corrida, con sus
cortes diarios, su límite total y sus días de trading. El estado de estrategia empieza cada día de
cero (`EstadoDia` nuevo; PROVISIONAL, ADR-0049 H6), y el bróker también: una orden pendiente o una
posición viva al cerrar la ventana la cierra RN-002 (`cierre_forzoso_fin_ventana`), y lo que quede
—hoy nada— se cancela al terminar el día y se cuenta en la traza.

### 7. Los ticks son obligatorios; el respaldo M1 solo para depurar

Por ADR-0051 §8, una corrida que cuente exige un dataset de ticks para cada día: sin él, el
cableado SE NIEGA. Con `--depuracion` corre igual sobre el respaldo M1 y toda la salida —el informe,
la curva de equity, la traza— lleva la marca `DEPURACION: respaldo M1, no cuenta`. Una hora perdida
dentro de un dataset sigue cayendo al respaldo y queda marcada evento a evento
(`fuente: respaldo_m1`), y el informe cuenta cuántos eventos salieron de cada fuente.

### 8. Solo construcción

La simulación completa corre solo sobre los días `dev` de construcción, por la compuerta del arnés
(`dias_de_construccion`), y se niega a medición y a ocultos con el mismo mecanismo y los mismos
mensajes (ADR-0048 §7).

## Problema que resuelve

ADR-0048 y ADR-0049 dejaron el motor sin bróker: diez gates en DESCONOCIDO y cobertura 0 por
construcción. ADR-0050, ADR-0051 y ADR-0052 construyeron las piezas y dejaron escrito el contrato
que el motor tendría que cumplir. Sin este ADR, el cableado se escribiría inventando por el camino
el signo de los acumuladores, el reloj, el instante en que llegan los eventos y qué hace una
acción cuya ligadura no identifica nada.

## Alternativas consideradas

1. Cableado sobre el intérprete tal cual, con primitivas que leen el bróker y la cuenta, huecos
   con nombre y decisiones conservadoras (elegida).
2. Cambiar el intérprete para que pase el nombre del predicado a los acumuladores y ligue `OP` a
   un id de posición.
3. Un evento del intérprete por cada evento del bróker (§2.1) y cierre intravela (§5.1).
4. Reordenar RN-011 en la spec para que el stop se escriba antes que el lote (§1.1).

## Por que elegimos esta opcion

Porque cumple el brief sin tocar la spec ni el intérprete, deja cada lectura escrita y comprobable
con un test, y donde la spec no alcanza deja un hueco con nombre en vez de una suposición. Las
cuatro decisiones pendientes están marcadas y cada una tiene su alternativa a un cambio de spec o
de intérprete de distancia.

## Por que descartamos las demas

- **(2)** toca el intérprete, que esta rama no toca; queda como alternativa de §1.2 y §3.2.
- **(3)** exige que las primitivas de mercado se evalúen fuera de un cierre de M1, que la spec no
  contempla (ADR-0028 §2), y un gate dentro del bróker.
- **(4)** toca la spec.

## Impacto

- `src/botsito/engine/cableado.py`, `src/botsito/engine/primitivas_broker.py`,
  `cuenta.CuentaViva`, `Broker.mover_stop`.
- `botsito motor arnes --simular` (informe de fidelidad más veredicto FTMO, curva de equity y
  eventos del bróker) y el visor con las órdenes y los llenados del bot.
- La línea base del arnés se vuelve a escribir al lado de las anteriores: cobertura 0 (el motor
  sigue parado en RN-011 y RN-004 por A-35) y el embudo muestra qué reglas pasan de DESCONOCIDO a
  evaluadas. **Medido al construir (`CABLEADO-SIMULADOR.md` §4), y corrige lo que este ADR
  anunciaba al proponerse:** pasan a evaluadas RN-010, RN-012, RN-016, RN-017, RN-018, RN-019,
  RN-026, RN-027, RN-029, RN-031 y RN-032; de los diez gates de ADR-0049 H4 siguen en DESCONOCIDO
  RN-005, RN-008 y RN-009 (geometría) y RN-020 (hueco de `perdida_dia` y `perdida_semana`).
  RN-016 se evalúa porque `se_cierra_operacion` da NO mientras no hay cierres y el hueco de
  `cartuchos` no llega a pedirse; RN-030 es terminal y lee un hecho, no el acumulador, así que no
  cambia de estado con el cableado.
- Sin tocar: la spec, `ambiguedades.yaml`, `engine/interprete.py`, `engine/motor.py`.

## Fecha / fase

2026-09-26 · rama `trabajo/cableado-simulador`. Next Action 33.

## Estado

ACTIVE (PROPUESTO: pendiente de aceptación del consultor; el campo dice ACTIVE porque la guardia
de ADR no admite otro valor)
