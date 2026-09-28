---
status: ACTIVE
date: 2026-09-28
phase: post-F14 (rama `trabajo/preparar-a47`)
---

# 0056 · La entrada con la ruptura: RN-011 con orden stop, preparada con selectores UNKNOWN

> **ACEPTADO** por el consultor el 2026-09-28: las nueve decisiones sobre
> `docs/validation/DISENO-ENTRADA-RUPTURA.md` §3 y la pieza nueva (la vida de la orden stop), en la
> orden de cierre de `trabajo/preparar-a47`. Lo que este ADR añade a esas decisiones para que la
> pieza nueva se pueda construir va marcado **PROVISIONAL**, como en ADR-0053, y se revisa en la
> rama de código que lo toque. **Nada se resuelve ni se fija aquí**: A-47, A-18, A-21, A-29, A-46,
> A-48 y A-49 siguen ABIERTAS y ningún parámetro cambia de valor.

## Decision

El punto de partida está medido en `DISENO-ENTRADA-RUPTURA.md` §1: el bróker simulado solo conoce
la orden LÍMITE y llena una límite colocada al lado equivocado del precio en el tick siguiente, a su
propio precio; RN-011 dimensiona y RN-015 coloca una límite en el cierre del breaker, cuando el
precio ya ha roto; el productor traza una zona por día desde la primera toma de M15 y no la
recalcula. Sobre eso, en pantalla el trader coloca órdenes STOP (38 frente a 1, `SESION-02-VIDEO-V8.md`
§4), ninguna de sus 77 entradas de construcción es una límite esperando el retroceso
(`ORDEN-STOP-O-LIMITE.md` §10) y su caja no la reproduce ninguna regla escrita de antemano
(`BLOQUE-DE-LA-CAJA.md` §3). Todas las piezas siguen el patrón de ADR-0054: **un selector por
decisión del trader, `enum`, UNKNOWN, con solo las lecturas documentadas como opciones; sin él, el
arnés y el visor se niegan nombrando la ambigüedad; el modo diagnóstico es la única excepción, con
su bandera y su etiqueta en cada línea, fichero y página, y nunca alimenta una medida de fidelidad.**

### 1. El tipo de orden de entrada es un selector ligado a A-47, y se construye ya

`entrada_tipo_orden`, `estrategia`, `enum`, **UNKNOWN**, con dos lecturas: `stop_en_ruptura` (lo
que el trader hace en pantalla: la orden se dispara cuando el precio rompe el punto) y
`limite_en_retroceso` (lo que programa RN-011 hoy: la orden espera el retroceso al bloque).
Diagnóstico `--diagnostico-a47 <lectura>`, etiqueta `DIAGNOSTICO-A47-<lectura>`, forma compacta
`a47=` en el nombre de fichero. **Con `limite_en_retroceso` todo sale como hoy, byte a byte.** Con
`stop_en_ruptura`, mientras las piezas 4 a 7 no existan, la acción es NO_IMPLEMENTADA con nombre y
vale DESCONOCIDO (ADR-0048). A-47 pasa a citar el parámetro. **La activación espera a la
confirmación grabada del trader**: el recuerdo de Aleks («cuando rompe») no es cita.

### 2. La orden stop en el bróker simulado salta al toque y se llena al precio del tick

Una venta stop salta cuando el BID toca el nivel o baja de él; una compra stop, cuando el ASK lo toca
o lo sube. Es **al toque**, como el stop de una posición (ADR-0051 §1, DN-1). Se llena **al precio
de ese tick más el deslizamiento** de la configuración (DN-3, hoy 0 y provisional hasta la demo). El
tick en que se decide no cuenta. El respaldo M1 es pesimista y marcado, como el stop de una posición,
y solo sirve para depurar (ADR-0051 §8). La orden lleva su tipo en `Orden` y en su historial, y el
evento de llenado registra el precio de la orden y el del llenado. **PENDIENTE DE MEDIR EN LA DEMO
de FTMO en MetaTrader: si el disparo al toque y el precio del tick son lo que hace MT5.**

### 3. Una pendiente colocada al lado equivocado se RECHAZA, y es PROVISIONAL

Al colocar o modificar una pendiente, el bróker la compara con el último tick anterior al instante.
Una límite de venta con el BID ya por encima de su precio, o de compra con el ASK ya por debajo, y una
stop de venta con el BID ya por debajo, o de compra con el ASK ya por encima, se rechazan con motivo
`precio_invalido`, como un `Rechazo` más de los del perfil (ADR-0052 §4), y el motor lo ve como un
evento de rechazo. **Nunca se convierte en una orden a mercado.** Lo de hoy, llenar al precio de la
orden, queda como la otra opción de un selector de modelo, `pendiente_mal_colocada`, para
reproducir las líneas base antiguas. **Qué hace MT5 de verdad lo mide Aleks en la demo de FTMO con
un script que se prepara en otra rama**: contra qué precio compara, si aplica la distancia mínima del
instrumento (que RN-026 ya tiene que comprobar al colocar) y qué hace con una pendiente en el nivel.
Cierra la deuda anotada el 2026-09-28 (`PROJECT_STATE.md`, Technical Debt).

### 4. La caja se traza por operación, y solo con la orden stop

El productor traza **una caja nueva en cada punto de ruptura candidato**, con su id, su 0, su 1 y
su instante, y no una por día. La memoria de un solo uso de hoy (`mem["toma"]`, `mem["esquema"]`,
`mem["zona_id"]` en `engine/zonas.py`) deja de valer. **Solo actúa con `stop_en_ruptura`**: con
`limite_en_retroceso` el productor hace lo que hace hoy, y la línea base no cambia. Qué es cada caja
frente a la toma de M15, y si una toma de una sesión anterior sigue valiendo, es A-46; qué hace con
la orden pendiente cuando aparece una caja nueva es una candidata (§8 del diseño, C1) y no se decide.

### 5. El bloque y el momento son dos ambigüedades nuevas, y A-21 no se amplía

- **A-48, qué velas forman el bloque de la caja**, con dos lecturas documentadas y ninguna fijada:
  `ultima_contraria` (lo que hace hoy `bloque_de_origen`; `ev-v3-010818-010bd2b3`,
  `ev-v3-011540-5425b533`) y `tramo_de_contrarias` (RN-007 y `ev-v3-010648-0039e34d`; v7 0:24:03,
  `ev-v7-002403-8344331d`, «pueden ser velas consecutivas del mismo color», que lo condiciona a que
  la vela siguiente cubra con la mecha a la anterior y **no dice** que el bloque sea todo el tramo).
  El selector `caja_bloque` nace con su rama de código.
- **A-49, si la caja se traza con la vela del bloque cerrada o en formación**: `cerrada` es lo de
  hoy y `en_formacion` **choca con ADR-0028** (la estrategia se evalúa al cierre de M1). Queda
  documentada y **NO_IMPLEMENTADA (DESCONOCIDO) hasta un ADR que lo decida. ADR-0028 no se toca.**
  El selector `caja_vela` nace con su rama.
- Las dos son `pregunta`, ABIERTAS y **no bloqueantes**: con la orden límite de hoy RN-011 corre con
  `ultima_contraria` y velas cerradas.

### 6. Stop y lote: tres selectores UNKNOWN, y las respuestas entran como CORRECT

`stop_inicial` (`nivel_1`, `nivel_0_8`), `stop_paso_a_0_8` (`al_llenarse`, `nunca`) y
`lotaje_distancia` (`hasta_1`, `hasta_0_8`), los tres `estrategia`, `enum`, **UNKNOWN**. Lo medido
que los sostiene está en `BLOQUE-DE-LA-CAJA.md` §5: con la orden colocada el stop está en el 1 en 6
cajas y en el 0,8 en 2; el paso del 1 al 0,8 sobre la misma caja se ve en v7 n.º 3 y no en n.º 11 ni
n.º 15. Las lecturas «stop inicial en el 1», «baja al 0,8» y «lote hasta el 1» contradicen
parámetros CONFIRMED de hoy: `stop_fraccion_caja` («no se mueve despues»), `lotaje_base`
(`hasta_stop_fraccion`) y, por v8 n.º 1, `stop_en_orden_pendiente`. **Cuando el trader conteste
grabado, cada respuesta entra como `CORRECT` sobre el parámetro CONFIRMED afectado, con la
grabación como fuente** (`feedback apply`, ADR-0012 §7): `RESOLVE_CONTRADICTION` solo actúa sobre
una contradicción de evidencia y no fija valores (`feedback/modelo.py`, `feedback/aplicar.py`).
**Aquí no se resuelve nada.** `base_calculo_objetivo` sigue cuestionado por A-18, sin cambio.

### 7. La vida de la orden stop: nace en el posible punto de breaker y se mueve con él

Es la pieza que el diseño no tenía. En v7 el trader marca **un posible punto de breaker antes de la
ruptura, lo activa como orden stop en ese punto** («un punto de breaker [...] que si lo rompe el
precio, pues se opera. Vale, lo activo», v7 0:14:57, `ev-v7-001457-1fe7fdfe`, con la Sell stop ya
puesta por debajo del precio en pantalla) **y lo va actualizando conforme se desarrolla el precio
hasta fijarlo** («actualizamos nuestro posible breaker y pues lo fijamos», v7 0:22:01,
`ev-v7-002201-2b2f20aa`; la Sell stop se mueve con el punto en el mismo minuto). Con velas del mismo
color el punto también se actualiza si la vela siguiente cubre con la mecha a la anterior (v7
0:24:03, `ev-v7-002403-8344331d`).

- **Comportamiento.** Con `stop_en_ruptura`, la orden nace **en cuanto existe un posible punto de
  breaker**, no en el cierre del breaker: se coloca como stop en ese punto, con el precio todavía
  al otro lado (si no, la pieza 3 la rechaza). Cada vez que el punto se actualiza, la orden se
  cancela y se vuelve a colocar en el punto nuevo, con el stop y el lote recalculados sobre la caja
  nueva (pieza 4). Cuando el precio rompe el punto, la orden se llena (pieza 2): eso es la entrada
  del esquema 1, sin retroceso. Cuando la orden sigue sin llenar al cerrar la ventana, se cancela.
- **Qué la gobierna.** El momento es la **tercera lectura de A-29**, `al_aparecer_punto_de_breaker`,
  opción nueva de `orden_limite_nace` (DEFAULT_AMBIGUOUS, valor sin cambiar; con esta lectura el
  motor queda NO_IMPLEMENTADA con nombre, como con la segunda). El movimiento es **el mecanismo de
  RN-006**: la orden pendiente se reubica cuando se completa una zona de control, con
  `reubicacion_cadencia` (`al_romper`, CONFIRMED) y `zona_control_criterio_completada` (`mecha`,
  CONFIRMED); hoy su predicado `se_completa_zona_de_control` sigue NO_IMPLEMENTADA (`engine/zonas.py`).
  **Qué es «el posible punto de breaker» es hoy `referencia_del_breaker`** (`domain/estructura_m1.py`:
  el último pivote de M1 contrario a la entrada formado con `CIERRE_VELA_CONTRARIA`), y **que el
  trader lo valide «apenas con una mecha» y con velas del mismo color es un criterio distinto**:
  entra en A-48 como lectura del punto, no se decide aquí.
- **Lo PROVISIONAL, para revisar en la rama 3:**
  - RN-008 («sin ninguno de los esquemas de entrada no hay entrada») **no frena la colocación** de
    la orden stop: prohíbe ABRIR sin esquema, y la orden stop solo se llena cuando el precio rompe
    el punto, que es el esquema 1. La descripción de `orden_limite_nace` ya avisa de que con una
    orden anterior al esquema RN-008 «frenaria la propia colocacion y habria que reescribirla». La
    rama 3 escribe esa lectura con `Fuente:` y un test que la fije, o se para.
  - Para correr la tercera lectura sin fijarla, la rama 3 extiende el diagnóstico de ADR-0054 a un
    parámetro DEFAULT_AMBIGUOUS: `--diagnostico-a29 <lectura>`, con su etiqueta, que se rechaza si
    el parámetro pasa a CONFIRMED.
- **Ambigüedad.** A-29 (el momento), A-47 (el tipo), A-48 (el punto y el bloque) y las candidatas
  C1 (la orden pendiente ante una caja nueva) y C7 (cuánto vive una stop sin llenar).
- **ADR.** Enmienda ADR-0055 (RN-011 coloca en el cierre del breaker) y ADR-0053 (la tabla de
  acciones gana la orden stop, su reubicación y su cancelación).
- **Tests.** La orden nace en el punto tras la toma y con el precio al otro lado; se mueve cuando el
  punto se actualiza y nunca cruza el precio; se llena al romper; se cancela al cerrar la ventana;
  y, por el arnés real sobre un día sintético, con `a47=stop_en_ruptura` y `a29=al_aparecer_punto_de_breaker`
  la traza enseña la cadena colocada, reubicada, llenada.

### 8. Cinco ramas de código, en este orden, y cada una con su prueba de punta a punta

| rama | qué | prueba de punta a punta por el arnés real |
|---|---|---|
| 1 | bróker: órdenes stop (pieza 2) y rechazo de pendientes mal colocadas (pieza 3) | una estrategia de prueba coloca una stop por el cableado, salta y se llena al precio del tick; las 4 órdenes cruzadas de `ORDEN-STOP-O-LIMITE.md` §8 salen rechazadas |
| 2 | selector de A-47 y RN-011 con stop (pieza 1) | con `limite_en_retroceso` la línea base sale idéntica; con `stop_en_ruptura`, NO_IMPLEMENTADA con nombre |
| 3 | vida de la orden stop y RN-006 (pieza 7) | colocada, reubicada, llenada en un día sintético |
| 4 | caja por operación y selectores del bloque y del momento (piezas 4 y 5) | dos cajas y dos órdenes stop en un día; las dos lecturas del bloque dejan trazas distintas |
| 5 | stop y lote (pieza 6) | stop inicial, paso al 0,8 y lote por el bróker |

**En cada rama, la línea base con la orden límite tiene que salir IDÉNTICA byte a byte** (salvo la
etiqueta del diagnóstico), con `diff`, antes de sellar. Se empieza por el bróker, que no depende
del trader.

### 9. Qué enmienda y qué supersede en parte

- **ADR-0020**: la distancia que dimensiona el lote pasa a un selector (`lotaje_distancia`);
  `lotaje_base` no cambia de valor hasta un `CORRECT`.
- **ADR-0028**: **no se toca.** `en_formacion` queda NO_IMPLEMENTADA hasta un ADR propio.
- **ADR-0051**: gana el llenado de una entrada stop (§1 a §3); DN-1 y DN-3 valen igual para ella.
- **ADR-0052**: §1 gana el ciclo de vida de una orden stop; §4 gana el rechazo `precio_invalido`,
  PROVISIONAL.
- **ADR-0053**: la tabla de acciones gana la orden stop, su reubicación y su cancelación; el contrato
  de `mover_stop`, que hoy solo va a la entrada, gana el paso al 0,8.
- **ADR-0055**: queda superseded en parte: RN-011 deja de colocar solo una límite en el cierre del
  breaker, y la zona deja de ser una por día con memoria de un solo uso. Su §1 (predicados puros) y
  su §2 (el selector de «limpia», PROVISIONAL) siguen en pie.

## Problema que resuelve

La spec programa una entrada que el trader no hace. RN-011 y RN-015 colocan una límite en el bloque
esperando el retroceso, y las 77 entradas de construcción llegan desde el lado de la ruptura
(`ORDEN-STOP-O-LIMITE.md`). El bróker simulado, además, llena al instante una límite colocada al
lado equivocado, así que ni siquiera mide lo que RN-011 dice: 4 de las 9 órdenes del bot en el
control de §8 eran de esas. Y el productor traza una zona por día, mientras el trader traza una caja
por operación (`BLOQUE-DE-LA-CAJA.md` §3.4). Sin selectores, la respuesta del trader a A-47 no
tendría dónde entrar, y cada pieza se escribiría con un valor inventado.

## Alternativas consideradas

1. **Fijar ya `stop_en_ruptura`** con lo que se ve en pantalla y el recuerdo de Aleks, y reescribir
   RN-011.
2. **Seguir con la límite** hasta la respuesta grabada, sin tocar el bróker ni el productor.
3. **Selectores UNKNOWN con diagnóstico**, construidos ya, y la activación con la respuesta grabada
   (la elegida).
4. Para la pendiente mal colocada: **llenarla al precio de la orden** (lo de hoy), **convertirla en
   orden a mercado**, o **rechazarla** (la elegida, PROVISIONAL).

## Por que elegimos esta opcion

Porque es el patrón que ya funcionó con A-35, A-44 (ADR-0054) y A-21 (ADR-0055): el motor se niega
sin la respuesta, el diagnóstico permite medir cada lectura rotulada, y la activación es escribir un
valor, no escribir código. Porque las dos primeras ramas no dependen del trader y cierran una deuda
medida del bróker. Y porque exigir la línea base idéntica en cada rama es la única forma de que
cinco ramas sobre la entrada no muevan lo que hoy se mide.

## Por que descartamos las demas

- **Fijar ya la stop**: el «cuando rompe» no es cita y CLAUDE.md no admite un valor sin fuente
  grabada; además contradice parámetros CONFIRMED (`stop_fraccion_caja`, `lotaje_base`) que solo un
  `CORRECT` con fuente puede cambiar.
- **Seguir con la límite**: deja el bróker llenando órdenes cruzadas y el productor con una zona por
  día, que son fallos medidos con independencia de A-47.
- **Llenar la pendiente cruzada al precio de la orden**: es lo de hoy, y es peor que el mercado en
  toda la distancia cruzada (`DISENO-ENTRADA-RUPTURA.md` §1.2). **Convertirla en mercado**: inventa
  una orden que el trader no puso. Rechazar es lo que el consultor entiende que hace MT5, y por eso
  es provisional hasta la demo.

## Impacto

- `knowledge/spec/`: A-48 y A-49 abiertas; A-29 con su tercera lectura y la opción nueva de
  `orden_limite_nace`; A-47 citará `entrada_tipo_orden` cuando la rama 2 lo cree. Los seis
  selectores nuevos y el de modelo nacen en sus ramas, todos UNKNOWN. RN-011, RN-015, RN-006 y la
  lectura de RN-008 cambian en las ramas 2 y 3, con `Fuente:`.
- `src/botsito/engine/`: la orden stop y el rechazo en `broker.py` y `llenado.py` (rama 1); el
  selector y la acción de entrada con tipo (rama 2); la reubicación y la cancelación (rama 3); la
  caja por operación en `zonas.py` y `domain/estructura_m1.py` (rama 4); stop y lote (rama 5).
- Tests: uno de punta a punta por rama, sobre el día sintético de 2030 y la spec real, más la línea
  base con `diff`.
- `PROJECT_STATE.md`: la deuda del bróker del 2026-09-28 pasa a la rama 1; las candidatas C1 a C7
  del diseño quedan en Open Questions hasta que alguna se abra.
- Fuera del repositorio: el script de la demo de MT5, en otra rama.

## Fecha / fase

2026-09-28 · post-F14, rama `trabajo/preparar-a47`, tras `DISENO-ENTRADA-RUPTURA.md`.

## Estado

ACTIVE
