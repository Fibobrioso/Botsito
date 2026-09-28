# Diseño de la entrada con la ruptura: el nuevo RN-011

Rama `trabajo/preparar-a47`, 2026-09-28, desde `main` en `stable/F20-bloque-de-la-caja`. **Revisión
de diseño, sin código**: no cambia el motor, ni el productor, ni el bróker, ni las reglas, ni ningún
parámetro, ambigüedad, evidencia o registro de feedback. No hay ADR: se escribe tras la revisión.

**De dónde se parte.** A-47 está ABIERTA y es BLOQUEANTE de RN-011: la spec coloca una orden LÍMITE
y en pantalla, en v7 y v8, las órdenes legibles son 38 stop frente a 1 límite
(`SESION-02-VIDEO-V8.md` §4). `ORDEN-STOP-O-LIMITE.md` §10 midió que **ninguna de las 77 entradas de
construcción es una límite puesta de antemano esperando el retroceso**: todas llegan desde el lado de
la ruptura. Aleks recuerda que el trader contestó «cuando rompe»; **no es cita** y se confirma
grabado. `BLOQUE-DE-LA-CAJA.md`: la orden va en el 0 de la caja en 11 de 12, el 1 es la máxima de la
vela en curso o de la anterior en 10 de 12, el 0 no lo explica ninguna regla con el criterio escrito
antes de medir, el productor no reproduce ninguna caja, y el stop se ve en el 1 al colocar y en el
0,8 ya lleno en varios casos (§5).

**Lo que la medición corrige del brief, antes de empezar.**
- **ADR-0011 no es A-11.** ADR-0011 es el kit de elicitación. La decisión «el stop va en la orden»
  es la respuesta del trader a A-11 (RESUELTA el 2026-09-10), registrada en `fb-2026-09-09-sesion-01-76fd91ba`
  y en el parámetro `stop_en_orden_pendiente` (`knowledge/spec/parametros.yaml:497-513`).
- **RN-011 no coloca la orden: la dimensiona.** RN-011 fija el lote y escribe el stop, y deja el
  hecho `orden_dimensionada`; **quien coloca es RN-015**, con `fijar_objetivo` y
  `colocar_orden_limite` (`knowledge/spec/strategy_spec.yaml:1009-1070` y `:1157-1205`). En este
  documento «RN-011» nombra las dos, porque el cambio las toca a las dos.
- **La límite al lado equivocado no se llena «a mercado»: se llena a su propio precio**, que es PEOR
  que el mercado en toda la distancia cruzada (§1.2). La deuda de `PROJECT_STATE.md` es cierta y es
  además una pérdida de fidelidad del precio, no solo del instante.
- **`RESOLVE_CONTRADICTION` no cambia un parámetro.** Solo actúa sobre una contradicción y no fija
  valores; lo que cambia un CONFIRMED es un `CORRECT` (§2.6).

## 1. Cómo está hoy, medido

Cada punto lleva la cita del código y una medida. Las medidas son de tres clases: los tests del
repositorio (34 de `test_llenado.py`, `test_broker.py`, `test_estructura_m1.py` y
`test_preparar_a21.py`, que pasan en esta rama), un script de lectura sobre ticks SINTÉTICOS de 2030
que no abre material (Anexo A, con su salida), y las mediciones sobre construcción ya commiteadas
(`ORDEN-STOP-O-LIMITE.md` §8 y `BLOQUE-DE-LA-CAJA.md` §3.4, abril y agosto).

### 1.1 (a) Qué órdenes admite el bróker y cómo las llena

**Una sola orden pendiente: la LÍMITE.** No hay tipo stop ni tipo mercado para entrar. `Orden`
(`src/botsito/engine/broker.py:75-87`) no lleva campo de tipo; la única vía de entrada es
`colocar_limite` (`broker.py:178`). `cerrar_a_mercado` (`:241`) solo cierra una posición y
`abrir_conocida` (`:252`) abre un llenado ya conocido (la repetición del trader). **Medido** (Anexo
A): los métodos del `Broker` que colocan o abren son `abrir_conocida`, `cerrar_a_mercado`,
`colocar_limite` y `mover_stop`, y los estados de una orden, `colocada`, `modificada`, `llenada`,
`cancelada`, `expirada` y `rechazada` (`broker.py:45-51`).

| qué | cómo llena con ticks (ADR-0051) | precio del llenado | respaldo M1 |
|---|---|---|---|
| entrada LÍMITE | la venta mira el BID y la compra el ASK (`llenado.py:125`); tiene que PASAR el precio, estrictamente, salvo `limite_llena_al_toque` (`llenado.py:90-94`, `:126`; DN-1); el tick en que se decide no cuenta (`:121`) | el de la orden, sin deslizamiento (`:127`) | venta con la máxima, compra con la mínima más el spread supuesto; al precio de la orden y sellado al cierre de la vela (`:129-136`) |
| stop de la posición | una larga mira el BID y una corta el ASK (`:170`), **al toque** (`:171`; DN-1) | el del tick, más el deslizamiento de la configuración (`:176`, `:209-211`; DN-3 = 0, provisional) | el stop primero; si la vela abre pasado el stop, a la apertura (`:192-196`) |
| objetivo de la posición | estricto (`:180`) | el del objetivo (`:181`) | detrás del stop (DN-2) |

**Medido** (Anexo A): una venta límite en 1000 con el bid en 995 al colocarla no se llena cuando el
bid toca 1000 y se llena cuando pasa a 1001, a 1000. El stop de una venta en 1010 salta con el ASK
del tick en 1012 y se llena a 1012 con deslizamiento 0 y a 1014 con deslizamiento 2. Lo mismo fijan
`test_una_limite_de_venta_mira_el_bid_y_exige_pasarlo` (`tests/unit/test_llenado.py:68`) y
`test_cierre_por_stop_al_precio_del_tick_y_una_venta` (`tests/unit/test_broker.py:132`).

**El stop de una posición solo se mueve a la entrada.** `Broker.mover_stop` (`broker.py:282-296`)
existe, pero la única acción del motor que lo llama lo mueve a `precio_entrada` y cualquier otro
destino es «sin contrato» (`src/botsito/engine/primitivas_broker.py:428-438`). Ningún test llama a
`mover_stop` directamente.

### 1.2 (b) Una pendiente colocada al lado equivocado del precio

**Ni se rechaza ni espera: se llena en el tick siguiente, al precio de la orden.**
`colocar_limite` solo comprueba la geometría stop < precio < objetivo (`broker.py:195-198`) y los
tres límites del perfil (`:199`, `_limite_infringido` en `:491-505`); nunca compara el precio con el
bid o el ask del momento. `primer_llenado_limite` llena en cuanto `_pasa` se cumple, sin saber dónde
estaba el precio al colocar (`llenado.py:117-127`). ADR-0052 §4 solo prevé los rechazos del perfil.
Ningún test fija este caso.

**Medido** (Anexo A):

| orden | precio al colocarla | qué pasa | precio de entrada | frente al mercado |
|---|---|---|---|---|
| venta límite en 1000 | bid 1012 | llenada en el tick siguiente, 2 s después; sin rechazo | 1000 | **12 puntos peor** que el bid del tick que llena |
| compra límite en 1000 | ask 991 | llenada en el tick siguiente, 1 s después | 1000 | **9 puntos peor** que el ask |

Sobre construcción, `ORDEN-STOP-O-LIMITE.md` §8 midió que **4 de las 9 órdenes distintas del bot se
colocaron ya cruzadas** (el precio había pasado el nivel entre 5 y 28 puntos) y el bróker las llenó en
1–5 s. **Qué hace MT5 con una límite así no está medido**: según el consultor la rechaza por precio
inválido, y se comprueba con la demo (§2.3).

### 1.3 (c) Cómo coloca RN-011 la orden hoy

| qué | hoy | dónde |
|---|---|---|
| **tipo** | LÍMITE, siempre | `primitivas_broker.py:378-380`: `ctx.broker.colocar_limite(id, z.lado, z.entrada, lote, o.stop, o.objetivo, ctx.instante_ms)` |
| **precio** | `z.entrada`: el borde del bloque más cercano al precio, con mechas (en una venta, la mínima del bloque) | `zonas.py:222-224`; `estructura_m1.py:205-207` |
| **lado** | compra con sesgo alcista, venta con sesgo bajista, congelado con la toma | `zonas.py:51`, `:137` |
| **momento** | exactamente en el cierre de la M1 del breaker (`toca_colocar_orden_limite` da SI solo si `instante == e.breaker_fin`); cualquier `orden_limite_nace` distinto de `al_darse_el_esquema` es NO_IMPLEMENTADA | `zonas.py:205-215`; el bróker recibe `breaker_fin` menos 1 ms (`cableado.py:161,175`) |
| **stop** | `entrada ± floor(distancia_completa × stop_fraccion_caja)`, 0,8 (CONFIRMED), escrito en la orden (A-11) y sin moverlo después | `primitivas_broker.py:292-304`; `parametros.yaml:433-447` |
| **lote** | `saldo × riesgo_por_operacion / distancia`, con la distancia hasta el stop (`lotaje_base: hasta_stop_fraccion`, ADR-0020); se resuelve al colocar (ADR-0053 §1.1, PROVISIONAL) | `primitivas_broker.py:342-358`; `parametros.yaml:698-715` |
| **objetivo** | `entrada ± floor(base × objetivo_rr)`, con la base `caja_completa` (CONFIRMED, cuestionada por A-18) | `primitivas_broker.py:306-328` |
| **caducidad** | ninguna: `colocar_limite` se llama sin `expira_ms` | `broker.py:187` |

**Medido**: `test_por_el_cableado_la_zona_llega_al_broker_como_una_orden_limite`
(`tests/unit/test_preparar_a21.py:277`) coloca por el cableado real una compra límite al precio de la
entrada, con el stop a 0,8 de la caja, el objetivo a 3 cajas y `colocada_ms = breaker_fin × 60 000 −
1`. Sobre construcción (`ORDEN-STOP-O-LIMITE.md` §8), las órdenes del bot se colocan en ese cierre y
**4 de 9 ya cruzadas**: la entrada de hoy no mira dónde está el precio.

**Una consecuencia que el diseño tiene que resolver.** En una venta, el bloque es la última vela
alcista antes del impulso y el breaker es la ruptura del último BAJO de M1. Cuando la orden se coloca,
en el cierre del breaker, el precio ya ha roto hacia abajo: una **límite** de venta en la mínima del
bloque queda, en general, por ENCIMA del precio y espera el retroceso, y por eso es lo que programa
RN-011. Una **stop** de venta en ese mismo nivel y en ese mismo instante quedaría del lado equivocado.
**Con una orden stop, el momento de hoy no sirve**: la orden tiene que estar puesta antes de que el
precio rompa (§2.1 y §2.4).

### 1.4 (d) Cómo decide hoy el productor la zona

**Una zona por día, desde la primera toma de M15, y ninguna después.**
- **La toma**: `_anotar_toma` registra la toma la primera vez que ve `liquidez_tomada == "si"` y
  después la devuelve sin mirar más (`zonas.py:119-139`, retorno temprano en `:122-124`). **Las tomas
  siguientes del día no cuentan.** `liquidez_tomada` no caduca al abrir la sesión (ADR-0055 §4,
  deuda ligada a A-46).
- **El esquema**: se busca en M1 CERRADAS (`m1_entre`, inicio en `[desde, instante)`,
  `motor.py:114-118`) desde la toma menos `LOOKBACK_M1 = 240` (`zonas.py:47-49,159`); una vez
  encontrado se guarda y **no se recalcula** (`zonas.py:155-165`).
- **La zona**: su id es `mem.setdefault("zona_id", "zona:<n>")`, así que **siempre es `zona:1`**
  (`zonas.py:217-225`). La memoria nace y muere con el día (`interprete.py:84-86`); no hay `caduca`.
- **El bloque**: una sola vela, la última del color contrario antes del impulso
  (`estructura_m1.py:122-132`). Agruparlas no tiene criterio escrito (`agrupar_estructura`
  NO_IMPLEMENTADA, RN-007, `estructura_m1.py:15-18`).
- **Si el esquema falla** en la primera M1 que pasa la referencia (tope de zonas, sin bloque o no
  «limpia»), la referencia y la toma están fijas y el día termina sin zona. Esto se lee del código y
  **no lo cubre ningún test** (`estructura_m1.py:198-211`).

**Medido**: `BLOQUE-DE-LA-CAJA.md` §3.4 cruzó la zona del productor en el instante de cada una de las
12 cajas del trader de agosto: **la zona no se mueve en todo el día** (el 3 de agosto, 1.15363 /
1.15377 para cinco cajas; el 4, 1.15085 / 1.15114 para tres), mientras que **el trader traza una caja
nueva en cada operación**, hasta siete el 3 de agosto. `test_el_primer_esquema_forma_la_zona_y_rn011_la_liga_en_el_cierre_del_breaker`
(`test_preparar_a21.py:169`) fija `zona:1`. **Ningún test cubre dos tomas en un día, una segunda
zona, ni la zona que cruza de sesión.**

## 2. Diseño propuesto

Todas las piezas siguen el patrón de ADR-0054: **un selector por decisión del trader, tipo enum,
en estado UNKNOWN, con solo las lecturas documentadas como opciones**. Sin él, el arnés y el visor se
niegan tras la compuerta de construcción, nombrando la ambigüedad y sin leer una vela. La única
excepción es el modo diagnóstico, con su bandera `--diagnostico-a<NN> <lectura>` y la etiqueta
`DIAGNOSTICO-A<NN>-<lectura>` en cada línea, fichero y página, que nunca alimenta una medida de
fidelidad y se rechaza si el valor ya está fijado (ADR-0054, `engine/diagnostico.py`).

### 2.1 Pieza 1 · El tipo de orden de entrada

- **Comportamiento.** Un selector decide si la entrada es una **orden stop en el nivel de ruptura**,
  que espera al otro lado y se dispara cuando el precio rompe, o una **orden límite en el retroceso**,
  que es lo de hoy. Con `limite_en_retroceso` todo queda como está, byte a byte. Con
  `stop_en_ruptura`, la orden se coloca **antes** de la ruptura, con el precio todavía al otro lado del
  nivel; el momento y el nivel los dan las piezas 4 y 5. Mientras esas piezas no existan,
  `stop_en_ruptura` es NO_IMPLEMENTADA y vale DESCONOCIDO (ADR-0048).
- **Selector.** `entrada_tipo_orden`, enum `[stop_en_ruptura, limite_en_retroceso]`, **UNKNOWN**.
  Diagnóstico: `--diagnostico-a47 <lectura>`, etiqueta `DIAGNOSTICO-A47-<lectura>`, forma compacta
  `a47=` en el nombre de fichero.
- **Ambigüedad.** A-47. Hoy no tiene parámetro: «Sin parametro: el registro no tiene todavia uno de
  tipo de orden» (`ambiguedades.yaml:1169`). Pasaría a `parametros: [entrada_tipo_orden]`.
- **ADR.** Supersede en parte a ADR-0055 (RN-011 coloca una límite). Enmienda ADR-0052 §1 y ADR-0053
  (la tabla de acciones: `colocar_orden_limite` pasa a una acción de entrada con tipo). La spec cambia
  el texto de RN-011 y RN-015 y el nombre de la acción, con `Fuente:`.
- **Tests.**
  - Sin el selector, el arnés se niega nombrando A-47, antes de leer una vela.
  - Con el valor fijado, el diagnóstico se rechaza.
  - **Con `--diagnostico-a47 limite_en_retroceso`, la línea base de hoy sale idéntica byte a byte**
    (salvo la etiqueta).
  - Con `stop_en_ruptura`, la traza dice NO_IMPLEMENTADA y ninguna orden sale.

### 2.2 Pieza 2 · La orden stop en el bróker simulado

- **Comportamiento.**
  - **Cuándo salta.** Una venta stop, cuando el BID llega al nivel o baja de él; una compra stop,
    cuando el ASK llega o lo sube. Es **al toque**, igual que los stops de las posiciones (DN-1). El
    tick en que se decide no cuenta, como en la límite (`llenado.py:121`).
  - **A qué precio.** Al del tick que la dispara, más el deslizamiento de la configuración (DN-3,
    hoy 0 y PROVISIONAL hasta la demo), igual que el stop de una posición (`llenado.py:176`). Si hay
    hueco, el precio es el del tick, que ya lleva el hueco dentro.
  - **Respaldo M1.** Pesimista y marcado, como el stop de la posición: al nivel, o a la apertura si
    la vela abre pasada; sellado al cierre de la vela (`llenado.py:192-196`). Solo para depurar
    (ADR-0051 §8).
  - **Traza.** La orden lleva su tipo (`limite` o `stop`) en `Orden` y en su historial. El evento de
    llenado registra el precio de la orden y el del llenado, para que el deslizamiento se lea en la
    traza sin recalcularlo.
- **Selector.** Ninguno de la estrategia: es modelo de llenado. El deslizamiento es DN-3 y ya existe.
  **Si el disparo al toque replica a MT5 es PENDIENTE DE MEDIR EN LA DEMO.**
- **Ambigüedad.** Ninguna del trader. A-47 decide si se usa.
- **ADR.** Enmienda ADR-0051 (el llenado de una entrada stop, §1-§3) y ADR-0052 §1 (el ciclo de vida
  de una orden stop).
- **Tests, sobre ticks sintéticos.**
  - No salta mientras el precio no llega.
  - Salta al toque, con el BID en una venta y el ASK en una compra.
  - Se llena al precio del tick, con deslizamiento 0 y con deslizamiento 2.
  - Con hueco, se llena al precio del tick.
  - Respaldo M1 marcado.
  - La orden llena y su stop en el mismo tick: el orden de los dos eventos, fijado por test.
  - Determinismo.

### 2.3 Pieza 3 · El rechazo de una pendiente mal colocada

- **Comportamiento propuesto.** Al colocar o modificar una pendiente, el bróker la compara con el
  último tick anterior al instante. Una **límite** de venta con el BID ya por encima de su precio, o
  una de compra con el ASK ya por debajo, se **rechaza**. Lo mismo una **stop** de venta con el BID ya
  por debajo, o una de compra con el ASK ya por encima. El rechazo queda como `Rechazo` con motivo
  `precio_invalido`, igual que los del perfil (ADR-0052 §4), y el motor lo ve como
  `EventoBroker(..., "rechazo", ...)` (`primitivas_broker.py:383`). **Nunca se convierte en una orden
  a mercado.**
- **PENDIENTE DE MEDIR EN LA DEMO, sin afirmarlo aquí:**
  - si MT5 rechaza de verdad una pendiente al lado equivocado, y con qué código;
  - contra qué precio compara (bid, ask o el último);
  - si aplica una distancia mínima (`stops level` o `freeze level` del instrumento, que RN-026 ya
    tiene que comprobar al colocar según `stop_en_orden_pendiente`);
  - qué hace con una pendiente justo en el nivel.
- **Selector.** De modelo, no de estrategia: `pendiente_mal_colocada`, `[rechazar, llenar_al_precio_de_la_orden]`,
  con `rechazar` como decisión PROVISIONAL del consultor hasta la demo, como DN-3 y DN-6.
  `llenar_al_precio_de_la_orden` es lo de hoy, y queda para reproducir las líneas base antiguas.
- **Ambigüedad.** Ninguna del trader. Es fidelidad del bróker y cierra la deuda del 2026-09-28.
- **ADR.** Enmienda ADR-0052 §4.
- **Tests.**
  - Las cuatro combinaciones, límite o stop y compra o venta, bien y mal colocadas.
  - Una modificación que la cruza.
  - **Por el arnés real sobre construcción, las 4 órdenes cruzadas de `ORDEN-STOP-O-LIMITE.md` §8
    salen como rechazos.**

### 2.4 Pieza 4 · Una caja por operación, no por día

- **Comportamiento.** El productor traza **una caja nueva en cada punto de ruptura candidato**, no
  una por día. Cada caja tiene su id (`zona:1`, `zona:2`...), su 0 y su 1, y su instante de
  nacimiento. Con `stop_en_ruptura`, la orden se pone en cuanto la caja existe y el precio está al
  otro lado de su 0. Si antes del llenado aparece una caja nueva, la orden se cancela o se mueve
  según la candidata C1 de §2.8; hoy no hay lectura documentada, así que es UNKNOWN. **La memoria de
  un solo uso de hoy (`mem["toma"]`, `mem["esquema"]`, `mem["zona_id"]`) deja de valer.**
- **Selector.** El 0 y el 1 los dan los selectores de la pieza 5. La relación de cada caja con la
  toma de M15 se deja como hoy, pero sin quedarse en la primera. **Medido** en `BLOQUE-DE-LA-CAJA.md`
  §2.4: una caja anterior a la toma del productor, dos en el mismo minuto y nueve después. Si la toma
  vale para todo el día o por sesión es A-46, ABIERTA.
- **Ambigüedad.** A-21 (la zona) y A-46 (la toma entre sesiones); más las candidatas C1 y C5.
- **ADR.** Supersede la parte de ADR-0055 que fija una zona por día y la memoria de un solo uso.
- **Tests.**
  - Dos puntos de ruptura en un día dan dos cajas y dos órdenes, en su instante y sin mirar al
    futuro.
  - Una caja nueva antes del llenado hace lo que diga el selector de C1.
  - Una toma de una sesión anterior se trata según A-46.
  - **La línea base con `limite_en_retroceso` no cambia**: la caja por operación solo actúa con
    `stop_en_ruptura`.

### 2.5 Pieza 5 · Qué velas forman el bloque, y cuándo

- **Selector del bloque.** `caja_bloque`, enum, **UNKNOWN**, con dos lecturas.
  - `ultima_contraria` (R1): la última vela contraria. Es la regla de hoy (`estructura_m1.py:122-132`),
    con base en el corpus (`ev-v3-010818-010bd2b3`, `ev-v3-011540-5425b533`).
  - `tramo_de_contrarias` (R4): el tramo de velas contrarias seguidas que acaba en esa última.
  - **R4 necesita su cita antes de ser opción.** Hoy solo la sostiene RN-007, «varias velas forman un
    order block mayor», sin criterio escrito (`mapeo_dos_velas = order_block_mayor`,
    `ev-v3-010648-0039e34d`; `estructura_m1.py:15-18`). Por ADR-0054 un selector solo lleva lecturas
    documentadas, así que o se cita o se queda fuera.
  - Las demás reglas de `BLOQUE-DE-LA-CAJA.md` (R2, R3, R5 y R6) no entran: no las sostiene el
    material. **Ninguna regla se elige**: con el criterio escrito antes de medir, ninguna pasa de una
    caja de 12 (`BLOQUE-DE-LA-CAJA.md` §3.1, v1). La pregunta 1 de la sesión 03 es exactamente esta.
- **Selector del momento.** `caja_vela`, enum `[cerrada, en_formacion]`, **UNKNOWN**. Una cosa medida
  cambia su alcance. Los fotogramas del trader caen en el segundo :59 (`BLOQUE-DE-LA-CAJA.md` §1.5),
  así que la vela «en formación» del trader es, en el reloj del motor, la M1 que cierra un segundo
  después: el motor la tiene ya cerrada en ese cierre (ADR-0028, estrategia al cierre de M1). Por eso
  la diferencia entre las dos lecturas no es de un segundo: es **si la caja incluye la vela del minuto
  de la colocación o espera a la siguiente**. `en_formacion` en sentido estricto, dentro de la vela,
  exigiría evaluar la estrategia por tick, y eso rompe ADR-0028. Si el trader dice eso, se para.
  Es la pregunta 2 de la sesión 03.
- **Ambigüedad.** El brief liga el bloque a A-21. **A-21 pregunta otra cosa**: qué hace «limpia» a una
  zona (`ambiguedades.yaml:402-435`, parámetro `zona_control_limpia`). El bloque y el momento
  necesitan su propia ambigüedad o una ampliación de A-21 (candidatas C2 y C3).
- **ADR.** Enmienda ADR-0055 (el bloque) y, si la respuesta lo exige, ADR-0028.
- **Tests.**
  - Por cada lectura, el 0 y el 1 sobre velas sintéticas con un tramo de tres contrarias.
  - `cerrada` frente a `en_formacion` sobre la vela del minuto de la colocación.
  - Sin mirar al futuro.
  - Por el arnés real en diagnóstico: las dos lecturas dejan trazas distintas, como
    `test_las_dos_lecturas_de_a21_dejan_trazas_distintas_por_el_arnes_real`.

### 2.6 Pieza 6 · Stop inicial, cuándo baja al 0,8, y el lote

- **Selectores**, los tres **UNKNOWN**:
  - `stop_inicial_fraccion`: `[1, 0,8]`. **Medido** en `BLOQUE-DE-LA-CAJA.md` §5.2: con la orden
    colocada, el stop está en el 1 en 6 cajas y en el 0,8 en 2.
  - `stop_baja_a_08`: `[al_llenarse, al_cierre_de_la_vela_del_llenado, nunca]`. **Medido**: el paso
    del 1 al 0,8 sobre la misma caja se ve en v7 n.º 3, tras el llenado; en v7 n.º 11 y n.º 15 el stop
    sigue en el 1 con la posición abierta. Con doce cajas, el material no decide.
  - `lote_distancia`: `[hasta_stop_inicial, hasta_0_8, caja_completa]`.
- **Contradicciones con parámetros CONFIRMED de hoy.**
  - `stop_fraccion_caja` = 0,8, que «se escribe EN la orden limite y no se mueve despues»
    (`parametros.yaml:437-440`, `fb-2026-09-09-sesion-01-d34a0222`). Las lecturas «stop inicial en el
    1» y «baja al 0,8» contradicen el «no se mueve».
  - `stop_en_orden_pendiente` = `en_la_orden` (A-11, RESUELTA): no se contradice con un stop en el 1
    escrito en la orden. **Sí se contradice con v8 n.º 1, colocada sin stop propio**
    (`BLOQUE-DE-LA-CAJA.md` §5.1).
  - `lotaje_base` = `hasta_stop_fraccion` (ADR-0020): si el stop inicial es el 1, «hasta el stop» ya
    no dice qué stop. `PROJECT_STATE.md` punto 15 recoge del corpus «lote sobre la caja entera, stop
    protegido tras la entrada», que es otra lectura.
  - `base_calculo_objetivo` = `caja_completa`, cuestionada por A-18 (suelo del RR realizado en 3,00
    frente al 3,75 que predice).
- **Cómo se tratarían, y lo que la medición corrige del brief.** El brief dice «RESOLVE_CONTRADICTION».
  Medido en el código, **esa acción solo admite como objetivo una `contradiccion`**
  (`src/botsito/feedback/modelo.py:65`) **y no fija ningún valor**: las acciones que fijan son
  `RESOLVE_UNKNOWN`, `CORRECT` y `CONFIRM` (`src/botsito/feedback/aplicar.py:34-36`). Además, las
  contradicciones abiertas se DERIVAN de los items de evidencia vivos, y un `RESOLVE_CONTRADICTION` no
  cierra nada por sí mismo (`src/botsito/cli.py:1978-1980`). Así que una respuesta grabada que
  contradiga un CONFIRMED entraría por dos vías:
  - un item de evidencia nuevo con la cita. Si choca en el mismo tema con el que sostiene el valor,
    la contradicción aparece y se resuelve con `RESOLVE_CONTRADICTION` sobre ella;
  - un `CORRECT` sobre el parámetro, que es lo único que cambia su valor por `feedback apply`
    (ADR-0012 §7).
  **Aquí no se resuelve nada.**
- **Ambigüedad.** A-18 (la base y el stop), A-11 (RESUELTA, se reabre solo si la respuesta la
  contradice) y la candidata C4.
- **ADR.** Enmienda ADR-0020 (la distancia del lote) y ADR-0053 (el contrato de `mover_stop`, que hoy
  solo va a la entrada, `primitivas_broker.py:428-438`).
- **Tests.**
  - Cada combinación de los tres selectores da el stop, el lote y el objetivo esperados.
  - El stop baja al 0,8 en el instante que diga el selector, y el bróker lo registra.
  - `mover_stop` a una fracción de la caja.
  - El lote no cambia al mover el stop.

### 2.7 Pieza 7 · Orden de implementación

Ramas pequeñas. **Cada una termina con un test de punta a punta por el arnés real**, como se hizo con
A-35: el cableado con la spec real, no una estrategia sintética.

| orden | rama | qué | depende de | test de punta a punta |
|---|---|---|---|---|
| 1 | bróker: rechazo de pendientes | pieza 3 | la decisión provisional del consultor | las 4 cruzadas de `ORDEN-STOP-O-LIMITE.md` §8 salen rechazadas |
| 2 | bróker: orden stop | pieza 2 | 1 | una estrategia de prueba coloca una stop por el cableado, salta y se llena al precio del tick |
| 3 | selector A-47 y diagnóstico | pieza 1 | 2 | con `limite_en_retroceso` la línea base sale idéntica; con `stop_en_ruptura`, NO_IMPLEMENTADA |
| 4 | caja por operación | pieza 4 | 3 y pieza 5 | dos cajas y dos órdenes stop en un día sintético |
| 5 | selectores del bloque y del momento | pieza 5 | la respuesta o el diagnóstico | las dos lecturas del bloque dan trazas distintas |
| 6 | stop y lote | pieza 6 | 3; las respuestas de A-18 | stop inicial, bajada al 0,8 y lote por el bróker |

Las ramas 1 y 2 no dependen del trader. Las 3 a 6 se pueden construir con los selectores en UNKNOWN y
correr en diagnóstico, como A-35 y A-44.

### 2.8 Pieza 8 · Candidatas a ambigüedad nuevas

Ninguna se abre aquí.

- **C1 · qué hace con la orden pendiente cuando aparece una caja nueva.** En v7 n.º 2 el trader
  redibujó la caja con la orden ya puesta, y la orden pasó del 0,5 de la primera al 0 de la segunda
  (`BLOQUE-DE-LA-CAJA.md` §5.3).
- **C2 · qué velas forman el bloque.** R1 frente a R4, y la cita de R4 (§2.5). Pregunta 1 de la
  sesión 03.
- **C3 · con la vela cerrada o en formación.** Pregunta 2 de la sesión 03.
- **C4 · el stop en dos tiempos.** El inicial en el 1 y el paso al 0,8, y cuándo; y la orden sin stop
  de v8 n.º 1. Toca A-18 y A-11.
- **C5 · la caja frente a la toma de M15.** Hay una caja anterior a la toma del productor
  (`BLOQUE-DE-LA-CAJA.md` §2.4). ¿La toma es condición previa de la caja, o la caja puede venir
  antes? Toca RN-004, RN-008 y A-29. Con `al_tomarse_la_liquidez`, RN-008 «frenaria la propia
  colocacion» (`parametros.yaml:477-496`).
- **C6 · la orden un poco más allá del 0.** En v7 n.º 3 la orden va 2 puntos por debajo del 0. Toca
  A-36, en qué punto de la mecha va la orden.
- **C7 · cuánto vive una orden stop sin llenar.** ¿Hasta el cierre de la sesión, hasta una caja nueva,
  o hasta que el precio invalide la caja? Hoy la límite no caduca (`broker.py:187`).

## 3. Decisiones que el consultor tiene que tomar antes del primer commit de código

1. **El selector de A-47**: nombre (`entrada_tipo_orden`), lecturas (`stop_en_ruptura`,
   `limite_en_retroceso`), y que A-47 pase a citarlo. ¿Se construye antes de que el trader confirme
   grabado el «cuando rompe»?
2. **El rechazo de pendientes mal colocadas**: ¿`rechazar` como decisión PROVISIONAL hasta la demo?
   ¿Quién mide en la demo de MT5 las cuatro cosas de §2.3, y cuándo?
3. **La orden stop en el bróker**: disparo al toque (como DN-1) y llenado al precio del tick más
   DN-3. ¿Se acepta con la etiqueta PENDIENTE DE MEDIR EN LA DEMO?
4. **La caja por operación**: supersede la zona por día y la memoria de un solo uso de ADR-0055. ¿Se
   acepta que solo actúe con `stop_en_ruptura`, para que la línea base de hoy no cambie?
5. **El bloque y el momento**: ¿se amplía A-21 o se abren ambigüedades nuevas? ¿R4 entra como opción
   sin cita, o espera a la respuesta de la sesión 03?
6. **`en_formacion` estricto**: si el trader dice que traza la caja dentro de la vela, ¿se para (rompe
   ADR-0028) o se acepta la lectura equivalente en el cierre de M1?
7. **Stop y lote**: los tres selectores de §2.6, y cómo entra una respuesta que contradiga
   `stop_fraccion_caja` o `lotaje_base`: un item de evidencia nuevo, `RESOLVE_CONTRADICTION` sobre la
   contradicción si aparece, y `CORRECT` sobre el parámetro, que es lo único que cambia su valor.
8. **El orden de las ramas** de §2.7: ¿se empieza por el bróker, que no depende del trader?
9. **La línea base**: ¿se exige que con `limite_en_retroceso` salga idéntica byte a byte, salvo la
   etiqueta del diagnóstico?

## 4. Estado

Revisión de diseño escrita. No hay código, ni ADR, ni cambios en la spec. A-47, A-18, A-21 y A-46
siguen ABIERTAS. **Rama lista para revisión, NO cerrada.**

## Anexo A · El script de lectura del bróker y su salida

Se ejecutó desde la raíz del repositorio con `uv run python <script>`. Vive fuera del repositorio,
porque esta rama no lleva código, y se copia aquí entero, tal como se ejecutó (solo cambia la ruta
de `RAIZ`), para que se pueda repetir. Usa ticks
SINTÉTICOS de 2030, como `tests/unit/test_broker.py`, y no abre ningún material.

```python
"""Medida de lectura del broker simulado para DISENO-ENTRADA-RUPTURA §1 (a) y (b). Ticks SINTETICOS
de 2030, como tests/unit/test_broker.py; no abre material. Escala 1: los precios son puntos."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(".").resolve()  # se ejecuta desde la raiz del repositorio
sys.path.insert(0, str(RAIZ / "src"))

from botsito.data.velas import a_minuto  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick  # noqa: E402
from botsito.domain.valores import Puntos  # noqa: E402
from botsito.engine import broker as B  # noqa: E402
from botsito.engine.llenado import Configuracion, Mercado  # noqa: E402

SPREAD = 3
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def ms(m: int, s: int = 0) -> int:
    return (M0 + m) * MS_POR_MINUTO + s * 1000


def tick(m: int, s: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(ms(m, s)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def broker(ticks: list[Tick], al_toque: bool = False, deslizamiento: int = 0) -> B.Broker:
    reglas = B.ReglasBroker(
        volumen_max_lotes=Decimal(10), ordenes_simultaneas_max=3, posiciones_dia_max=2,
        huso_corte=ZoneInfo("UTC"), comision_por_lote=Decimal(0), comision_por_lado=True,
        swap_largo_puntos=Decimal(0), swap_corto_puntos=Decimal(0),
    )
    cfg = Configuracion(al_toque, deslizamiento, lambda _m: SPREAD)
    return B.Broker(reglas, cfg, Mercado(ticks, []), Decimal(1), 1)


print("(a) metodos publicos del Broker que colocan o abren:",
      sorted(n for n in dir(B.Broker) if n.startswith(("colocar", "abrir", "cerrar", "mover"))))
print("    constantes de estado:", [B.COLOCADA, B.MODIFICADA, B.LLENADA, B.CANCELADA, B.EXPIRADA,
                                    B.RECHAZADA])

# (a) venta limite en 1000 bien colocada (bid por debajo): toca 1000 y no llena; pasa a 1001 y llena
b = broker([tick(0, 5, 995), tick(1, 0, 1000), tick(1, 30, 1001), tick(2, 0, 998)])
b.colocar_limite("v", "venta", 1000, Decimal(1), 1010, 970, ms(0))
ev = b.avanzar(ms(3))
print("(a) venta limite 1000, bid 995 al colocar; bid toca 1000 y luego 1001 ->", ev,
      "entrada", b.posiciones["pos-v"].entrada)

# (b) venta limite en 1000 colocada con el bid YA en 1012 (lado equivocado: el precio ha pasado)
b = broker([tick(0, 0, 1012), tick(0, 3, 1012), tick(0, 40, 1011)])
b.colocar_limite("x", "venta", 1000, Decimal(1), 1030, 970, ms(0, 1))
ev = b.avanzar(ms(1))
print("(b) venta limite 1000 colocada con el bid en 1012 ->", ev, "rechazos", b.traza().rechazos,
      "entrada", b.posiciones["pos-x"].entrada, "(el bid del tick que llena era 1012)")

# (b) compra limite en 1000 colocada con el ask YA en 991 (bid 988): lado equivocado
b = broker([tick(0, 0, 988), tick(0, 2, 988)])
b.colocar_limite("y", "compra", 1000, Decimal(1), 980, 1040, ms(0, 1))
ev = b.avanzar(ms(1))
print("(b) compra limite 1000 colocada con el ask en 991 ->", ev, "entrada",
      b.posiciones["pos-y"].entrada, "(el ask del tick que llena era 991)")

# stop de una posicion: al toque y al precio del tick, con el deslizamiento de la configuracion
for desl in (0, 2):
    b = broker([tick(0, 5, 1001), tick(1, 0, 1004), tick(1, 30, 1009)], deslizamiento=desl)
    b.colocar_limite("s", "venta", 1000, Decimal(1), 1010, 970, ms(0))
    b.avanzar(ms(2))
    p = b.posiciones["pos-s"]
    print(f"stop de una venta (stop 1010, ask del tick 1012), deslizamiento {desl}:",
          p.motivo_cierre, p.precio_cierre)
```

Salida (2026-09-28):

```
(a) metodos publicos del Broker que colocan o abren: ['abrir_conocida', 'cerrar_a_mercado', 'colocar_limite', 'mover_stop']
    constantes de estado: ['colocada', 'modificada', 'llenada', 'cancelada', 'expirada', 'rechazada']
(a) venta limite 1000, bid 995 al colocar; bid toca 1000 y luego 1001 -> [(1894694490000, 'llenada', 'v', 'ticks')] entrada 1000
(b) venta limite 1000 colocada con el bid en 1012 -> [(1894694403000, 'llenada', 'x', 'ticks')] rechazos () entrada 1000 (el bid del tick que llena era 1012)
(b) compra limite 1000 colocada con el ask en 991 -> [(1894694402000, 'llenada', 'y', 'ticks')] entrada 1000 (el ask del tick que llena era 991)
stop de una venta (stop 1010, ask del tick 1012), deslizamiento 0: stop 1012
stop de una venta (stop 1010, ask del tick 1012), deslizamiento 2: stop 1014
```

Los instantes: `1894694490000` es el minuto 1 y 30 s tras `M0` (el bid pasa a 1001), `1894694403000`
es 2 s después de colocar la venta cruzada, y `1894694402000` 1 s después de colocar la compra.
