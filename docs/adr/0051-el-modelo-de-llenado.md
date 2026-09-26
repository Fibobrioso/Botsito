---
status: ACTIVE
date: 2026-09-26
phase: post-F14 (rama `trabajo/ticks-llenado`, sesión nocturna)
---

# 0051 · El modelo de llenado

> **ACEPTADO el 2026-09-26** por el consultor, tras su revisión, sobre lo escrito en la sesión
> autónoma de la noche anterior (`docs/validation/TICKS-LLENADO.md`). Lo que el consultor decidió
> sobre cada DECISIÓN NOCTURNA está en la sección «Las decisiones nocturnas, resueltas», más abajo.

## Decision

El **modelo de llenado** es la regla con la que el simulador decide, para cada orden y cada
posición, en qué instante y a qué precio ocurre cada evento —llenado de una límite, salto del
stop, alcance del objetivo— a partir de los precios de mercado. Vive en `engine/llenado.py` como
funciones puras (Fase 3), sin cifras de negocio: lo que puede cambiar es configuración en
`knowledge/simulador/llenado.yaml`.

### 1. A qué lado del spread se compara cada orden

Una cuenta compra al ASK y vende al BID. Por eso:

| orden | lado que se mira | condición |
|---|---|---|
| límite de COMPRA (entrada larga) | ASK | el ASK pasa POR DEBAJO del precio de la límite |
| límite de VENTA (entrada corta) | BID | el BID pasa POR ENCIMA del precio de la límite |
| STOP de una larga (vende) | BID | el BID TOCA o pasa por debajo del stop |
| STOP de una corta (compra) | ASK | el ASK TOCA o pasa por encima del stop |
| OBJETIVO de una larga (vende) | BID | el BID pasa POR ENCIMA del objetivo |
| OBJETIVO de una corta (compra) | ASK | el ASK pasa POR DEBAJO del objetivo |

**DECISIÓN NOCTURNA 1 (conservadora): las límites y los objetivos exigen que el precio pase
ESTRICTAMENTE más allá de su nivel; los stops se disparan al TOCARLO.** Un toque exacto no llena
una entrada ni un objetivo (el bot entra menos y cobra menos), y sí salta un stop (pierde más).
Alternativa descartada por ahora: llenar al toque en los tres casos, que es lo que hace un tester
de MT5 y probablemente FX Replay; es más favorable al bot y sesgaría la fidelidad a su favor. Si
el consultor prefiere el toque, es un booleano de la configuración (`limite_llena_al_toque`).

### 2. Cuándo una límite se da por llenada con ticks

En el PRIMER tick, posterior o igual al instante en que la orden queda colocada, cuyo lado
relevante cumple la condición de §1. El precio de llenado es el de la orden (una límite se llena
a su precio o mejor; aquí, a su precio: no se regala la mejora), y el instante es el del tick, con
milisegundos. Una orden colocada en un tick no se evalúa contra ese mismo tick: contra el
siguiente (sin mirar al futuro: el motor decide con lo que ya cerró).

### 3. Qué toca antes, el stop o el objetivo

**Con ticks, el orden real:** se recorre la secuencia y gana el primer tick que cumpla cualquiera
de las dos condiciones. Si el mismo tick cumple las dos (un salto que cruza stop y objetivo a la
vez), **gana el stop** (DECISIÓN NOCTURNA 2, conservadora; con ticks es rarísimo y solo ocurre en
un hueco de precio).

**Respaldo con solo M1: pesimista, el stop primero**, como decidió ADR-0049 H4. Dentro de una
vela M1 cuyo rango cubre el stop y el objetivo no se sabe el orden: se toma el stop. Y dentro de
una M1 que cubre la límite de entrada y luego el stop, se toma que la entrada se llenó y el stop
saltó en la misma vela (la peor lectura).

### 4. El deslizamiento

**No se modela un deslizamiento fijo** (DECISIÓN NOCTURNA 3). Motivo: no hay ninguna medida del
deslizamiento de FTMO, y ADR-0002 prohíbe una cifra inventada; un `deslizamiento_fijo_puntos`
existe en la configuración con valor 0 y su motivo escrito, para que el día que se mida entre por
ahí y no por código. Lo que SÍ queda modelado sin inventar nada es el deslizamiento de hueco: con
ticks, un stop se llena al precio del TICK que lo dispara, no al nivel del stop, así que un salto
que pase de largo el stop pierde lo que salte. Con el respaldo M1 el stop se llena a su nivel (no
hay tick que diga otra cosa) salvo que la vela ABRA más allá del stop: entonces a la apertura.

### 5. El tramo sin ticks: respaldo M1, marcado en la traza

Cada evento lleva su `fuente`: `ticks` o `respaldo_m1`. Un minuto sin ticks —una hora que Dukascopy
no sirve, un tramo perdido tras los reintentos, o un dataset de ticks que no existe— se evalúa
con la vela M1 BID del repositorio y el spread supuesto de §6, con la regla pesimista de §3, y el
evento queda marcado. El informe de una corrida dice cuántos eventos salieron de cada fuente.
El instante de un evento del respaldo es el CIERRE de la vela (la lectura que menos sabe: nada
dentro del minuto).

### 6. El spread

**Con ticks, el spread es el de cada tick** (ASK − BID), y no hace falta suponer nada. **Sin
ticks, el spread supuesto por hora** sale de la medida de la Fase 2 sobre los ticks de
construcción (abril y agosto de 2026, ventana 07:00–15:00 del trader): se toma el **percentil 90**
de cada hora (DECISIÓN NOCTURNA 4, conservadora: un spread alto llena peor las compras y salta
antes los stops de las cortas), y fuera de la ventana el percentil 90 de toda la muestra. Vive en
`knowledge/simulador/llenado.yaml` con su fuente (el dataset de ticks del que se midió) y el
respaldo se niega a correr sin él. Las M1 del repositorio son BID (ADR-0005): el ASK del respaldo
es BID más el spread supuesto.

### 7. Las decisiones nocturnas, resueltas por el consultor (2026-09-26)

- **DN-1** (límites y objetivos pasan estrictamente el nivel; stops al toque, §1): **ACEPTADA**.
- **DN-2** (un tick que cruza stop y objetivo a la vez es stop, §3): **ACEPTADA**.
- **DN-3** (sin deslizamiento fijo, §4): **PROVISIONAL hasta la demo en MetaTrader**, donde se
  medirá; hasta entonces `deslizamiento_fijo_puntos: 0` con su motivo en `llenado.yaml`.
- **DN-4** (spread supuesto = percentil 90 por hora medido, §6): **ACEPTADA**.
- **DN-5** (ticks solo de los días dev de construcción y las horas 05-13 UTC, Fase 2 de la rama):
  **ACEPTADA PARA VERANO**. La ventana de ticks de invierno (06:00-14:00 UTC, cuando el trader
  está en CET) queda PENDIENTE y ligada a A-42, que decide con qué reloj cuenta la sesión.
- **DN-6** (el swap se cobra en cada medianoche del huso del perfil, ADR-0052 §3): **PROVISIONAL
  hasta medir el corte real en la plataforma** (A-28).
- **DN-7** (quitar de este ADR la declaración de ADR-0052 como id inexistente): **ACEPTADA**.
- **DN-8** (la salida de cada operación del trader se repite con la regla de la spec, Fase 6):
  **ACEPTADA** como lectura descriptiva; no es la salida real del trader y así se dice.
- **DN-0** (PROPUESTO con `status: ACTIVE` por la guardia): **SUPERADA por esta aceptación**.

### 8. El hallazgo que cambia el proyecto: los ticks son obligatorios

La Fase 6 de la rama repitió las operaciones reales del trader de construcción por el bróker de
dos formas: con ticks y con el respaldo M1 pesimista. **El desenlace —el motivo o el precio de
cierre— difiere entre las dos en una fracción grande de las operaciones** (las cifras, por mes y
por escenario, en `docs/validation/TICKS-LLENADO.md` y `REPETICION-TRADER-SALIDA.txt`). Por eso,
por decisión del consultor del 2026-09-26: **los TICKS SON OBLIGATORIOS para toda simulación que
cuente —construcción, medición y holdout—, y el respaldo M1 solo sirve para depurar.** Una corrida
que valga tiene que declarar su dataset de ticks y su selección; una hora perdida sigue cayendo al
respaldo y queda marcada, pero un día sin ticks no cuenta. Lo que sigue de aquí: descargar los
ticks de cada mes que se vaya a medir con el mismo procedimiento, y la ventana de invierno (DN-5).

## Problema que resuelve

ADR-0028 fija que la fase de riesgo va por tick y que las órdenes se procesan por evento del
bróker; ADR-0049 H4 deja escrito que sin ticks el camino intravela será pesimista por OHLC de M1;
ADR-0050 construye la capa de cuenta y la deja esperando a un bróker que le entregue operaciones
con marcas y cargos. Nadie había escrito todavía CÓMO se decide un llenado: a qué lado del spread
se mira, qué pasa cuando stop y objetivo caben en la misma vela, ni de dónde sale el spread cuando
no hay ticks. Sin eso, el bróker simulado (ADR-0052) inventaría esas reglas al escribirse.

## Alternativas consideradas

1. Toque a los dos lados del spread, con ticks y con respaldo pesimista (elegida, con las cuatro
   decisiones nocturnas marcadas).
2. Llenar todo al toque, incluidas las límites y los objetivos (lo que hace un tester estándar).
3. Un deslizamiento fijo en puntos, inventado, además del de hueco.
4. Spread medio (no percentil 90) como supuesto sin ticks.
5. Sin respaldo: negarse a correr en cuanto falte una hora de ticks.

## Por que elegimos esta opcion

Porque cada regla queda escrita, medida donde se puede medir (el spread) y conservadora donde hay
que elegir, y todo lo elegible vive en configuración: aceptar la alternativa 2 o 4 mañana es
cambiar un valor, no código. Y porque el respaldo M1 marcado en la traza permite medir, en la
Fase 6, cuántas veces el resultado cambia entre ticks y respaldo, que es la única forma de saber
cuánto pesa la pérdida de ticks.

## Por que descartamos las demas

- **(2)** es más favorable al bot y sin medida que lo respalde: sesgaría la fidelidad a favor.
- **(3)** es una cifra inventada (ADR-0002).
- **(4)** el spread medio deja pasar la mitad de los minutos con un spread mayor: no es
  conservador.
- **(5)** perdería días enteros de construcción por una hora perdida, y la regla pesimista ya
  existe (ADR-0049 H4).

## Impacto

- `knowledge/simulador/llenado.yaml` (carpeta nueva con README): `limite_llena_al_toque: false`,
  `deslizamiento_fijo_puntos: 0` con motivo, y `spread_supuesto_puntos` por hora con su fuente.
- `src/botsito/engine/llenado.py` (Fase 3): funciones puras con tests de no mirar al futuro,
  determinismo, stop y objetivo en la misma M1 (ticks frente a respaldo), límite tocada justo en su
  precio a cada lado, y tramo sin ticks marcado.
- `src/botsito/data/ticks.py` (Fase 2): los ticks de construcción, congelados con manifiesto y
  hashes como las M1.
- El bróker simulado (ADR-0052) consume este modelo y no decide nada de esto por su cuenta.
- Lo que el consultor decidió al aceptar está en §7; el hallazgo de los ticks, en §8.

## Fecha / fase

2026-09-26 · escrito en la sesión nocturna y ACEPTADO por el consultor el mismo día, rama
`trabajo/ticks-llenado`. Next Action 32.

## Estado

ACTIVE
