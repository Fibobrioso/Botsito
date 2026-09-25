---
status: ACTIVE
date: 2026-09-25
phase: post-F14 (rama `trabajo/arnes-motor`)
---

# 0048 · El arnés del motor

## Decision

Este ADR **complementa a ADR-0030** y no sustituye ni enmienda nada: ADR-0030, ADR-0018, ADR-0019,
ADR-0028 y ADR-0032 siguen tal cual. ADR-0030 fija que «el motor recorre el árbol genérico de
`forma` [...] y despacha por nombre a primitivas escritas a mano: una por predicado, una por acción
y una por acumulador». Aquí se fija el **arnés** que envuelve a ese intérprete para medir cada regla
en cuanto se escriba.

1. **El arnés envuelve al intérprete del árbol genérico.** El intérprete recorre la `forma` de las
   reglas VIGENTES de `strategy_spec.yaml`:
   - en cada evento, a punto fijo con refracción y con la precedencia por clase de ADR-0018
     (`gate` > `terminal` > `disparador` > `fallback`), volviendo a empezar por los `gate` tras cada
     disparo (ADR-0028 §4);
   - una acción con `efecto` solo se ejecuta si, en ese instante, ningún `gate` prohíbe ese efecto
     (ADR-0032 §3).
2. **`NO_IMPLEMENTADA` se marca por PRIMITIVA**, con su nombre: predicado, acción o acumulador.
   Nunca por regla, y nunca con un valor por defecto.
   - Un predicado no implementado vale **DESCONOCIDO**, no falso ni verdadero. Los nodos
     `todos_de`, `cualquiera_de` y `ninguno_de` lo propagan con la lógica de Kleene: `todos_de` es
     falso si algún hijo es falso; `cualquiera_de` es verdadero si alguno es verdadero; en otro
     caso, DESCONOCIDO.
   - Una regla cuyo `cuando` es DESCONOCIDO **no ejecuta su `entonces`**: ni fija hechos, ni
     permite, ni prohíbe.
   - Una acción con `efecto` que un `gate` DESCONOCIDO podría prohibir **no se ejecuta**.
   - Una acción no implementada no hace nada.

   Así, el camino que pasa por una primitiva no implementada no produce hechos ni operaciones, y
   **queda registrado**: qué primitiva, en qué regla, en qué (día, sesión).
3. **La unidad de ejecución es el DÍA.** El estado del día cruza sus dos sesiones, como dice la
   spec: los hechos de origen `regla` que fija una sesión siguen vivos en la siguiente
   (`detenido_por_tope`, `detenido_por_cartuchos`...). **Lo que A-39 deja abierto** —qué pasa con
   lo pendiente o lo abierto cuando la segunda sesión cambia el sesgo— **se marca PROVISIONAL y no
   se inventa**: el arnés no añade ningún cierre ni ninguna retirada al cambiar de sesión.
4. **La unidad del informe** sigue siendo (día, sesión), y la operación dentro de ellos, según
   ADR-0043 y ADR-0047. Las operaciones del bot salen en el formato exacto de
   `cases/criterio_fidelidad.Operacion`, y se miden con `medir`, sin tocarlo.
5. **El embudo va sobre el grafo de hechos, no sobre una fila de reglas.** Para cada (día, sesión)
   con operaciones del trader, el informe dice:
   - qué hechos de origen `regla` llegaron a producirse, en el orden en que la spec los declara:
     `sesgo`, `liquidez_tomada`, `orden_dimensionada`…;
   - si hubo operación;
   - en qué primitivas `NO_IMPLEMENTADA` se paró el camino hacia cada hecho que faltó, que son las
     de las reglas que lo producen (`produce`).

   En conjunto: cuántas sesiones producen cada hecho, y cuántas se paran en cada primitiva.
6. **Instrumento y perfil de cuenta entran como configuración.** El símbolo y el prefijo de los
   datasets salen de `knowledge/cases/kit/config.yaml`; las cifras, de `parametros.yaml`; y las del
   criterio, de `criterio_fidelidad.yaml`. Nada en `src/` asume un instrumento ni una firma
   (ADR-0002).
7. **El comando solo corre sobre CONSTRUCCIÓN**, los meses `construccion` de
   `criterio_fidelidad.yaml`.
   - Se niega a cualquier mes de `medida` y a cualquier otro mes.
   - Pasa siempre por la compuerta: cada caso se cruza con `casos_ocultos` ANTES de leerlo, y un
     oculto detiene el comando.
   - La medida tendrá su propia rama y su propio ADR.
8. **RN-003 entra como la primitiva que produce el hecho `sesgo`**, con `domain/sesgo.py` tal cual
   (ADR-0044), evaluada al abrir cada sesión.

## Problema que resuelve

Hoy solo existe una regla escrita en código, RN-003, y ninguna forma de ver qué hace el conjunto
cuando se añade la siguiente. Sin arnés, cada regla nueva se mide a mano o no se mide. Con él, la
cobertura, la precisión y el embudo salen de un comando, y dicen dónde se pierden las operaciones
del trader.

El brief de esta rama suponía una cadena lineal de reglas, y el proyecto ya la había descartado:
- ADR-0030 descarta por escrito el «código a mano por regla»;
- ADR-0018 §2 dice que «el orden del fichero deja de tener semántica»;
- ADR-0028 §4 fija el punto fijo con refracción;
- la spec es un grafo de hechos con ciclos: `detenido_por_tope` lo producen y lo consumen RN-020 y
  RN-029, y `orden_dimensionada` lo producen RN-011 y RN-015.

El consultor eligió mantener esa arquitectura (`docs/validation/ARNES-MOTOR.md`).

## Alternativas consideradas

1. Envolver al intérprete del árbol, con `NO_IMPLEMENTADA` por primitiva y el día como unidad
   (elegida).
2. Una cadena lineal de reglas, cada una función pura del estado de la anterior.
3. Tratar una primitiva no implementada como falsa.

## Por que elegimos esta opcion

- **Es la arquitectura que ya rige** (ADR-0030, ADR-0018, ADR-0028): el arnés no la cambia, la
  ejercita.
- **DESCONOCIDO no decide por la regla que falta.** Una primitiva no implementada tratada como
  falsa haría que un `gate` no escrito dejara pasar todo; tratada como verdadera, que prohibiera
  todo. En los dos casos el arnés inventaría un comportamiento.
- **El día como unidad** respeta el estado que la spec hace cruzar de una sesión a la otra.

## Por que descartamos las demas

- **(2)** Contradice ADR-0030, ADR-0018 §2 y ADR-0028 §4, y no puede representar los ciclos del
  grafo.
- **(3)** Una primitiva falsa en un `gate` equivale a no tenerlo: el arnés daría operaciones que la
  spec prohíbe en cuanto se escribiera.

## Impacto

**Huecos de interpretación, registrados y no inventados.** Cada uno se resuelve con su ADR o su
ambigüedad, no en el código.

- **H1. RN-003, la forma frente a ADR-0044.** La `forma` es `rompe` sobre la vela H4 previa y fija
  `sesgo` al sentido de la ruptura. ADR-0044 añade la búsqueda hacia atrás hasta
  `sesgo_h4_tope_velas`, y los estados AMBIGUO e INSUFICIENTE, «con cualquiera de los dos no se
  opera». Ninguna forma expresa ese «no se opera». Por orden del consultor, la primitiva usa
  `domain/sesgo.py` tal cual. Con AMBIGUO o INSUFICIENTE, el hecho `sesgo` queda sin valor en esa
  sesión y el embudo lo dice.
- **H2. Qué es una sesión.** `abre_sesion_operativa` es «empieza una de las sesiones de la
  ventana», y la spec no declara sus límites como parámetro. El arnés usa las sesiones de
  `knowledge/cases/kit/config.yaml`, las mismas que etiquetan los casos del trader, para que bot y
  trader se midan con la misma unidad.
- **H3. El orden dentro de una clase.** ADR-0028 §4 no lo fija, y ADR-0032 §4 encadena por hechos
  lo que lo necesita. Para ser determinista, el arnés recorre las reglas de una misma clase por su
  id. La spec no debe depender de ese orden.
- **H4. Las fases de ADR-0028.**
  - Riesgo por tick: no hay ticks, solo M1, así que en el arnés se evalúa al cierre de M1. Sus
    acumuladores, además, no están implementados.
  - Órdenes por evento del bróker: no hay bróker simulado (F24). Los predicados de fuente `broker`
    y la acción `colocar_orden_limite` son `NO_IMPLEMENTADA`, y los hechos de origen `broker`
    (`operacion_abierta`, `orden_limite_pendiente`) son falsos mientras no se haya colocado nada,
    que es lo que diría un bróker sin órdenes.
- **H5. `permite`.** Por la precedencia de ADR-0018 una prohibición gana siempre, así que en el
  arnés `permite` se registra y no cambia nada.
- **H6. Estado entre días.** El contador de cartuchos se reinicia «con la siguiente liquidez de
  M15», no con el día (RN-016). En el arnés cada día empieza de cero: **PROVISIONAL**, como lo que
  deja abierto A-39.

**Lo demás:**
- `src/botsito/engine/` recibe el intérprete y el arnés. El comando es `botsito motor arnes`, con
  su runbook en `docs/runbooks/ARNES-MOTOR.md`.
- **Hasta que exista el bróker simulado, el motor real no puede producir ninguna operación**: la
  cobertura del motor de hoy es 0 por construcción, y el embudo dice dónde se para.

## Fecha / fase

2026-09-25 · post-F14, rama `trabajo/arnes-motor`. Decisión del consultor: opción (a).

## Estado

ACTIVE
