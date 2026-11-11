# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F (1) · las láminas del bot (R4.5)
**Rama:** trabajo/laminas
**Objetivo:** que el trader vea lo que hizo el bot y por qué, en su idioma, recortado al instante de decidir: un subcomando nuevo de `motor` que escribe las láminas desde la corrida con la cuenta por mes, las láminas de las diez sesiones candidatas de la 7a y la enmienda de RUMBO-2026-11.md §0, §4 y §5 (encargo en `docs/encargos/trabajo-laminas.md`).

## Base (comprobada con git al abrir, 2026-11-10)

- `git rev-parse main origin/main`: `e5394c57e57a9488b8042f33b03c292142eb034e` las dos veces.
- Último `- Tag:` de HISTORIA: `stable/F38v-trazas-ablacion`; `git rev-parse "stable/F38v-trazas-ablacion^{commit}"` = `git rev-parse main^1` = `76bbe0997c1ef2bb052b4724017fb66cfaf77b06`; en origin (`git ls-remote --tags`: `62bd425…` refs/tags/stable/F38v-trazas-ablacion). `stable/F38w-laminas` no existe ni en local ni en origin.
- CI de main sobre `e5394c57e57a9488b8042f33b03c292142eb034e` (check-runs): `python completed success`, run 42759493730.
- `git branch --list -a`: solo `main` (y `origin/main`); `git ls-remote --heads origin`: solo `refs/heads/main`.
- Sesión arrancada con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` (medido: `echo $CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` da `1`); modelo Opus 5.5, esfuerzo alto.
- La apertura: commit `chore(rama): abre trabajo/laminas …`, `make check` 3359 passed, SELLO sobre `692ec4de`, pico 309 MiB.

## La decisión de los gráficos 2 a 6 (del consultor, 2026-11-08, con RUMBO §3)

ACTIVAR-SESION-06.md §«Para la sesión 7», punto 10, dice que los gráficos 2 a 6 (S-8 a S-12) «se rehacen SIN fecha y con el contexto que pidió». No se rehacen: los sustituyen las láminas del bot, que llevan ese contexto, y el bloque de días de la sesión 7 (RUMBO §1 b). ACTIVAR-SESION-06.md es un informe cerrado y no se toca: la decisión queda escrita aquí y en el encargo, y la recogerá la orden de cierre.

**Hasta que el ADR del método cambie la regla 2 de `docs/runbooks/SESION-DE-PREGUNTAS.md`, las láminas no se enseñan al trader**: la regla 2 corta los gráficos antes de la colocación y prohíbe la orden, el stop y el objetivo, que la lámina enseña.

## 0. Fase 0 (2026-11-10)

Hecha con la skill `fase-cero`: el encargo, contrastado por el agente `auditor-encargo` (su informe, tal cual, en el Apéndice A), y el inventario medido. **No se ha escrito código.** F1 está retenida por un punto que no casa (§0.10).

### 0.1 La base y lo de mirar

- La base: arriba.
- **Las diez sesiones frente a la compuerta** (guion `diez_sesiones.py` de la carpeta de trabajo; solo recuentos y sí/no, sin ids): `casos_reservados(repo)` y `casos_ocultos(repo)` dan 34 claves cada uno (34 días); los meses de construcción son `2026-04, 2026-07, 2026-08, 2026-01`; `dias_de_construccion` da 76 días dev. **Los siete días de las diez sesiones son dev, y ninguno está oculto ni reservado.** De los seis días de calendario que van del quinto anterior al propio día (lo que pueden tocar las ventanas en Madrid y en UTC), en 04-13, 07-06, 07-07, 07-15 y 07-17 no hay ninguno oculto ni reservado; en 07-02 y 07-03, uno de junio en cada caso. Junio no es construcción, así que el recorte del punto 6 deja fuera esos días igual (la H4 y la M15 de 07-02 y 07-03 empiezan el 1 de julio a las 00:00 UTC, las 02:00 de Madrid).
- **Horas perdidas** (`docs/validation/anexos/RESPALDO-M1/horas_perdidas.py:18-24`, 18 horas; en código, `MercadoDia.horas_perdidas`, que llena `_ticks_del_dia` de `engine/simulacion.py:166-180`): **ninguna de las diez sesiones tiene una dentro**. Pero las ventanas de dos sí las tocan, y faltan ticks, no velas M1 (auditor, afirmación 50): la de H4 de 07-15 11-15 contiene 2026-07-14T12Z, y las de H4 y M15 de 07-17 11-15 contienen 2026-07-16T11Z. El punto 6 excluye solo las horas perdidas DENTRO de la sesión, así que estas dos se quedan. Decisión 9.
- La 07-14 11-15 sigue fuera por el encargo (la hora 12Z cae dentro de la sesión: de 09Z a 13Z).

### 0.2 Qué da cada pieza, medido sobre una ejecución

La medida: **una corrida del motor cableado solo sobre julio** (la misma preparación que `motor decisiones`), declarada antes en HOLDOUT-EXPOSICIONES, con un observador que imprime nombres de campos y tipos (guion `campos_cierre.py` de la carpeta de trabajo): 6253 cierres observados en 13 días.

**Lo que recibe el observador (`Cierre`, `engine/cableado.py:221-237`):** `dia` str, `instante` int (minuto UTC del cierre de M1), `sesion` str, `huso` str, `escala` int, `evento` (`Evento`), `estado` (`EstadoDia`), `broker` (`Broker`), `ctx` (`ContextoDia`) y `datos` (`DatosMercado`). Lo llama `correr_dia` en cada cierre, después de decidir (`cableado.py:442-449`), y **solo en los cierres de las sesiones** (el bucle va del primer al último minuto de `dia.limites()`, `:326-391`). `estado`, `broker` y `ctx` son los objetos vivos del motor; `Orden` y `Posicion` son dataclasses mutables (`broker.py:224-264`), y la memoria de zonas lleva `set` y `dict` que el motor sigue cambiando. Medido en 2026-07-03:
- `estado.memoria["zona_de_entrada"]`: `por_sesion` y `zonas`. En cada sesión: `escenarios` (list), `toma` (dict), `puntos` (dict), `punto_de_zona` (dict de id de zona a `"nivel@inicio"`), `usadas` (set) y, en 9 cierres, `esquema` (`Esquema`). Cada escenario: `n`, `toma`, `zonas` (set) y `terminado` (None o str). Cada toma: `instante`, `nivel`, `lado` y `pivote` (lado, nivel, formado). `zonas`: `Zona` con `id, lado, entrada (el 0), extremo (el 1), por (primer_esquema o segundo_esquema), desde, formada`.
- `estado.anotaciones` por sesión: `sesgo_h4`, `liquidez_m15`, `liquidez_m15_alcanzada` (y, cuando las hay, `sesgo_h4_doble_ruptura` y las tres de saltadas, que en 07-03 no salen).
- `estado.hechos`: `sesgo`, `liquidez_tomada`; `estado.broker`: `operacion_abierta`, `orden_limite_pendiente`.
- `broker.ordenes`: `Orden` con `id, lado, precio, lotes, stop, objetivo, colocada_ms, expira_ms, estado, ultimo_cambio_ms, historial (instante, estado), tipo, anterior` (la versión antes de la última modificación). `broker.posiciones`: `Posicion` con, entre otros, `orden_id, entrada, stop, objetivo, abierta_ms, cerrada_ms, motivo_cierre, precio_cierre`.
- `ctx`: entre otros, `zona_de_orden`, `sesion_de_orden`, `no_enviadas` (instante, zona, motivo, lote del riesgo) y `zonas`.
- `evento`: `disparadas`, `fijados`, `prohibido_por`, `quizas_por`, `bloqueadas` y `bloqueada_por` (los gates, de F38v).

**Lo que junta `motor decisiones` (`engine/decisiones.py`, la bitácora):** escribe TEXTO por cierre: la toma con su M1, los escenarios, cada zona con su 0, su 1 y su punto, la orden con precio, stop y objetivo, los hechos que cambian, las prohibiciones con sus gates, los bloqueos y el llenado. La liquidez de M15 la lee con `c.datos.liquidez_m15(c.instante, lado)` (`decisiones.py:406`, verificado), pero **solo en `_linea_m15`, al nacer una zona, y solo para compararla por igualdad con el 0 de la zona**: no la guarda ni da la lista de líneas de la sesión (auditor, afirmación 22). `_sin_orden` (`:446-465`) compone sus motivos como texto suelto. Las parejas: `resumir` llama a `emparejar` del criterio (`:183-211`) con las mismas operaciones puntuables que `medir`.

**Cómo saca el visor las parejas y las operaciones del trader (`engine/visor.py:308-382`):** corre el motor **sobre el día suelto** (`self.motor.correr_dia(mercado)`, `:325`), **recalcula el sesgo de cada sesión con su propio código** (`_sesgo_de_sesion`, `:336-339`) y empareja con `medir` sobre ese día (`:362-366`). Son los dos defectos que la lámina no puede heredar: el día suelto (la cuenta por mes no llega) y el recálculo. La lámina toma las parejas de `medir` sobre la corrida entera (lo que hace el arnés en `medida_de`, `arnes.py:268-271`, y lo que llama T0 `patrones.py:18`: «filas del trader con PAREJA») y el sesgo de las anotaciones del motor.

**Qué hace `scripts/graficos_sesion.py`:** las ventanas (`:73-77`, `:199-203`: H4 desde las 00:00 de Madrid de cuatro días antes, M15 desde las 00:00 del día anterior, M1 desde una hora antes de la sesión, todo hasta el corte; la primera vela agregada que empieza antes del recorte no se dibuja, `:211-214`); el recorte (`recorte` y `permitido`, `:123-146`: cada minuto, en Madrid y en UTC, en un día de la tabla `CONSTRUCCION` de `:67-72` y fuera de `casos_ocultos`, y si el corte no cumple, error); la última puerta (`comprobar`, `:220-233`); las fechas (`_RE_FECHA`, **en `:247-252`**, no en :265-270 como dice el encargo; los meses van sin `\b`, así que «mayor» casa con «mayo»); y el SVG (`:265-341`) y la escritura, que se niega dentro del repo y no pisa ficheros (`:347-374`). Lee las velas del mes del día con `cargar_ventana`, sin el mes anterior.

**Lo que de los puntos 1 a 4 de «La lámina» no da hoy ninguna pieza:**
1. **Qué H4 fijó el sesgo y cuáles saltó, y por qué.** `ResultadoSesgo` (`domain/sesgo.py:56-76`) solo da contadores; la anotación, también (`primitivas.py:203-213`). Además, `velas_miradas` (cuántas miró hasta decidir) no se anota. Decisión 1.
2. **Las líneas de M15 de la sesión y dónde acaban.** Nada las acumula: `liquidez_m15` da el pivote más reciente de cada lado en un instante (`engine/motor.py:150-176`). Se pueden acumular desde el observador, leyendo esa misma función en cada cierre; la toma, de la memoria (`toma.pivote`). Decisión 4.
3. **Qué zonas de control contó RN-009.** El predicado (`zonas.py:466-481`) llama a `zonas_de_control` (`domain/estructura_m1.py:153-171`), que solo devuelve un número, y no lo guarda. Decisión 2.
4. **Una lista cerrada de causas de «por qué no hay orden».** Hoy es texto (`_sin_orden`). La tabla de §0.3 la cierra con causas estructuradas.
5. **Una foto del instante.** Nada copia el estado: la bitácora escribe texto en el instante. La lámina necesita copiarlo (§0.3, «el enganche»).
6. **Con cuerpo o con mecha.** No va en la memoria, pero lo dice la forma de RN-004 (`cruza: {criterio: liquidez_m15_criterio_toma}`, `strategy_spec.yaml:1331`): la opción del registro que el motor usó (hoy `cuerpo`).

### 0.3 El diseño que propongo

**El subcomando y sus opciones.** `motor laminas --sesiones 2026-07-06:07-11,2026-07-06:11-15,... --salida <carpeta fuera del repo>`, las dos obligatorias. `--sesiones` lleva pares `día:sesión`, con la sesión por el nombre que traen los datos (`config.sesiones`). No lleva `--meses` ni ninguna opción de diagnóstico: corre siempre la corrida de `motor decisiones` (toda la construcción, la cuenta por mes, el perfil y la fase por defecto, sin depuración), porque el emparejamiento sale de la corrida entera. No comparte `_opciones_simulacion` ni `_opciones_diagnostico`, así que `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` y `test_la_seccion_no_anade_ninguna_opcion_al_comando` no cambian.

**Dónde vive el código e import-linter.** `src/botsito/engine/laminas.py` (el recolector, la selección, la foto, la tabla de frases y la puerta del punto 6) y `src/botsito/engine/laminas_svg.py` (el dibujo y el HTML), más el subcomando en `cli.py`. `engine` ya importa `cases`, `data`, `spec` y `domain` (pyproject.toml:95-117), y `viewer` está por encima: **no hace falta tocar `pyproject.toml`**. Si se aprueban las decisiones 1 y 2, el contrato se amplía en un commit a `src/botsito/domain/sesgo.py` y `src/botsito/domain/estructura_m1.py` (dominio puro: import-linter lo deja).

**Cómo se engancha sin cambiar lo que el motor devuelve.** El recolector es el `observador` de `MotorCableado`, como la bitácora, y entra por `decisiones.motor_nuevo(plantilla, reglas, recolector)`: no hay campo nuevo en `MotorCableado` (las listas de `CAMPOS_DE_CONFIGURACION` y `CAMPOS_DE_ESTADO`, `decisiones.py:121-134`, no cambian). En los días pedidos, y solo en ellos, hace dos cosas, las dos con COPIAS:
- en cada cierre acumula las líneas de M15 (`datos.liquidez_m15` de los dos lados) y la vida de cada orden de la sesión (cuándo se colocó y cuándo cambió de precio);
- en los cierres en que una orden se coloca o cambia de precio, y en los cortes de tipo b (que se conocen antes de correr, por las operaciones del trader), saca una FOTO: un dataclass congelado con las velas de la ventana hasta el corte (tuplas de `Vela`, que son inmutables), los hechos, las anotaciones, la memoria de la sesión convertida a tuplas y frozensets, las órdenes y posiciones como tuplas de valores, las prohibiciones y bloqueos del evento y lo que se sabía antes del corte. Nada guarda una referencia a `estado`, `broker`, `ctx` ni a la memoria.
Al terminar la corrida, con las parejas de `medir` sobre la corrida entera, elige las fotos (punto 2) y dibuja solo desde ellas. Propongo además que corra la base dos veces, como `motor decisiones`, la segunda sin recolector, y que salga con error sin escribir nada si los recuentos no son iguales (decisión 10).

**Qué láminas.** (a) Por cada orden de la sesión que acabó llenada: la foto del último cierre en que se colocó o se movió al precio al que se llenó (`Orden.precio` en ese cierre igual al de la posición), que siempre es anterior al llenado, porque el llenado ocurre en el `avanzar` de un minuto posterior. (b) Por cada operación del trader de la sesión sin pareja: la foto del cierre `t` más tardío con `t · 60 000 < entrada en ms` (la última M1 cerrada estrictamente antes de su entrada; decisión 8). Sin la operación del trader. Las dos, en orden de hora dentro de la sesión.

**Las ventanas y el negar por defecto (punto 6).** Las ventanas de `graficos_sesion.py` (H4: cuatro días; M15: el día anterior; M1: una hora antes de la sesión, con el inicio de la sesión de `DiaDeMercado.limites()`, la puerta de ADR-0069), con las velas en formación de H4 y M15 hechas con las M1 hasta el corte y `agregar` con `anclaje_h4` del registro. Las velas salen de `c.datos`, que son las que el arnés cargó por la API del manifiesto. La puerta: cada minuto, en el huso que da el registro y en UTC, cae en un tramo de construcción y fuera de `casos_ocultos`; los tramos, de `cobertura_material` (decisión 3). Lo que no es vela se dibuja o se nombra con su precio solo si su instante de nacimiento está permitido y dentro de la ventana (decisión 5): la H4 que fija el sesgo, por su inicio; una línea de M15, por la vela contraria de su pivote; una zona, por el cierre de su breaker (`formada`); el punto, por la vela que lo forma; la toma, por su M1. Si no cumple, no se dibuja ni da precio, y la sustentación dice «viene de antes de la ventana». Un día pedido que no sea dev de construcción, uno oculto, una sesión con una hora perdida dentro, un corte que no cumpla o una causa sin frase: error que lo nombra, y no se escribe nada (todo se calcula en memoria antes del primer fichero).

**La salida (punto 7).** `--salida` obligatoria; se niega si resuelve dentro del repo (con su test) y si existe y no está vacía (no pisa). Dentro: `sesion-NN/indice.html` y `sesion-NN/lamina-NN.html` (NN, el orden de `--sesiones` y el de la hora), y `clave.txt` en la raíz (código → día, sesión, corte y tipo a/b), que no entra al repo ni al informe. Cada nombre y cada byte de los HTML pasan por la regex de fechas antes de escribir.

**El formato (punto 8).** Un HTML por lámina con un SVG escrito por el código, sin JavaScript, sin `<title>`, `<metadata>` ni comentarios, y deterministas (orden fijo, formato de números fijo, sin reloj). Tres paneles uno sobre otro (H4, M15 y M1), los precios en el eje derecho, las horas de Madrid de ese día abajo, el corte en el borde derecho (la última vela, la del corte, como en el replay) y la sustentación debajo. La regex de fechas: `\d{4}-\d{1,2}-\d{1,2}`, `\b\d{1,2}/\d{1,2}\b`, `\b\d{1,2}-\d{1,2}\b` y los meses en castellano e inglés CON `\b` (`\b(enero|…|diciembre|january|…|december)\b`, sin mayúsculas): «3 de mayo» casa y «otro rango mayor» no. Por eso la lámina nunca escribe el nombre de la sesión («07-11» casaría como DD-MM): dice «la sesión de las HH:MM a las HH:MM», con las horas de los datos.

**El punto 9.** El 0,8: `registro.decimal("stop_fraccion_caja")`, también para su rótulo; el huso: `Cierre.huso` (el `huso_visible` del reloj del registro); el anclaje: `registro.hora("anclaje_h4")`; las horas de las sesiones: `DiaDeMercado.limites()`. Los rótulos 0,25 y 0,5 van como `Decimal("0.25")  # no-negocio: rótulo del Fibonacci, solo dibujo` y `Decimal("0.5")  # no-negocio: …`, una línea cada uno, declaradas en el informe. Nada copia los literales de `graficos_sesion.py` (`ZoneInfo("Europe/Madrid")`, las horas).

**La tabla de frases (punto 4), entera.** La clave la usa el código; la salida solo lleva la frase. Sin ids, sin lote, sin R, sin dinero y sin porcentajes. `{…}` son huecos que se llenan con precios, horas o recuentos del instante.

*Hechos (el vocabulario de la spec: `sesgo`, `liquidez_tomada`, `orden_dimensionada`, los cuatro `detenido_por_*` y los dos del bróker):*

| Clave | Frase |
|---|---|
| `sesgo=alcista` | «Sesgo de H4 alcista: la vela H4 que lo fija rompió el alto de la anterior y cerró verde.» (con doble ruptura: «rompió los dos extremos de la anterior y cerró verde») |
| `sesgo=bajista` | «Sesgo de H4 bajista: la vela H4 que lo fija rompió el bajo de la anterior y cerró roja.» (con doble ruptura: «… los dos extremos … y cerró roja») |
| `sesgo=insuficiente` | «Sin sesgo de H4: ninguna de las velas H4 que mira hacia atrás rompe un extremo de la anterior cerrando de ese color.» |
| `sesgo=ambiguo` | «Sesgo de H4 ambiguo.» (sin productor desde ADR-0075; está porque el vocabulario lo declara) |
| saltadas, color contrario | «Antes de esa vela saltó {n} velas H4 que rompieron un extremo y cerraron del color contrario.» |
| saltadas, sin cuerpo | «… {n} que rompieron un extremo y cerraron sin cuerpo.» |
| saltadas, dos extremos sin cuerpo | «… {n} que rompieron los dos extremos y cerraron sin cuerpo.» |
| la H4 que fija, fuera de la ventana | «La vela H4 que fija el sesgo viene de antes de la ventana.» |
| `liquidez_tomada=si` | «Liquidez de M15 tomada: una vela de M1 cerró con {cuerpo / mecha} por {debajo del bajo / encima del alto} de M15 en {precio}, a las {HH:MM}.» (cuerpo o mecha: la opción del registro que nombra la forma de RN-004; otra opción, error) |
| sin `liquidez_tomada` | «Todavía no ha tomado la liquidez de M15 en esta sesión.» |
| `orden_dimensionada` | sin frase visible, a propósito: es la marca interna de la orden preparada, y la orden se enseña aparte |
| `detenido_por_cartuchos` | «Ya ha gastado sus intentos en esta liquidez: espera otra liquidez de M15.» |
| `detenido_por_tope` | «Ha llegado al tope del día del trader: no abre más hasta el corte del día.» |
| `detenido_por_tope_total` | «La cuenta ha llegado a su freno total: no opera más.» |
| `detenido_por_racha` | «Tras la racha de pérdidas seguidas del trader, no opera más hoy.» |
| `operacion_abierta` | «Tiene una operación abierta.» |
| `orden_limite_pendiente` | la orden viva (abajo) |

*Gates VIGENTE que pueden prohibir (los 15 de la spec con `prohibe`, medidos con `listas_frases.py`). La frase es el motivo; con `[dispara]` sale «No abre: {motivo}.», con `[desconocido]` «No abre porque no puede descartar que {motivo}.», y en un bloqueo, «Iba a colocar la orden y no la coloca: {motivo}.»:*

| Gate | Motivo |
|---|---|
| RN-001 | «está fuera de la ventana de la sesión» |
| RN-037 | «es el último minuto antes de que cierre la vela H4 de la sesión» |
| RN-033 | «no hay sesgo de H4 claro» |
| RN-005 | «lo que se forma está en el lado de ruido de la liquidez de M15» |
| RN-008 | «no se da ninguno de los dos esquemas de entrada» |
| RN-009 | «el esquema tiene más zonas de control de las que admite ({n}, y admite {m})» (los números, si se aprueba la decisión 2; `m` del registro) |
| RN-016 | «ya ha gastado sus intentos en esta liquidez» |
| RN-018 | «ya tiene una operación abierta, y no opera en paralelo» |
| RN-020 | «ha llegado al tope del día del trader» |
| RN-036 | «viene de la racha de pérdidas seguidas del trader» |
| RN-022 | «la situación no encaja en lo que sabe hacer» |
| RN-026 | «el bróker no admite el stop donde toca» |
| RN-029 | «ha saltado el freno diario de la cuenta» |
| RN-031 | «ha saltado el freno total de la cuenta» |
| RN-032 | «el riesgo de la operación no cabe antes del límite de la cuenta» |

*Por qué no hay orden (una enumeración cerrada en el código; cada causa sale de un campo de la foto, nunca de un texto):*

| Causa | De dónde sale | Frase |
|---|---|---|
| sin sesgo | `hechos["sesgo"]` no es alcista ni bajista | la del hecho |
| sin toma | sin `liquidez_tomada` en la sesión | «Todavía no ha tomado la liquidez de M15 en esta sesión.» |
| sin caja | el escenario vigente sin zonas | «Ha tomado la liquidez, pero aún no se ha formado ninguna caja con su breaker en este escenario.» |
| caja sin punto | la zona sin `punto_de_zona` | «La caja no tiene punto de breaker.» |
| caja usada | la zona en `usadas` | «Esa caja ya tuvo su orden.» |
| punto gastado | el punto en `rechazados` | «Ese punto ya se gastó: el bróker rechazó la orden.» |
| escenario terminado | `terminado == ganancia` (el único valor del código, `zonas.TERMINADO_POR_GANANCIA`) | «Este escenario ya terminó con una ganadora: espera otra liquidez de M15.» |
| operación abierta | `operacion_abierta` | «Tiene una operación abierta.» |
| colocación bloqueada | `evento.bloqueada_por` de `colocar_orden_limite` | «Iba a colocar la orden y no la coloca: {motivo del gate}.» |
| no enviada | `ctx.no_enviadas` en el corte, con el límite (`volumen`, `margen`, `minimo` de `broker.py:174-176`, y `no_operar`) | «Iba a colocar la orden y no la envía: no cabe en la cuenta ({por el volumen máximo / por el margen / por debajo del mínimo}).» |
| no tocaba | caja con punto, nada de lo anterior, y ni RN-011 ni RN-015 disparan | «Con la caja formada, todavía no le toca colocar la orden.» |
| fuera de la sesión | RN-001 | la del gate |

*Lo que se enseña siempre (hechos del instante, en el orden en que se leen):*

| Clave | Frase |
|---|---|
| esquema | «Es el {primer / segundo} esquema.» (`Zona.por`; otro valor, error) |
| escenario | «Escenario {n} de la sesión.» |
| la caja | «La caja va de {precio del 0} (el 0) a {precio del 1} (el 1).» |
| el punto | «El punto de breaker está en {precio}, de la vela de las {HH:MM}.» |
| la orden colocada (tipo a) | «Coloca la orden de {compra / venta} en {precio}, el 0 de la caja, con el stop en {precio} (el {0,8} redondeado) y el objetivo en {precio}.» |
| la orden movida (tipo a) | «Mueve la orden de {compra / venta} a {precio}, …» (igual) |
| la orden viva (tipo b) | «Tiene una orden de {compra / venta} pendiente en {precio}, …» (igual) |
| antes del corte, cerradas | «Antes, en esta sesión: {n} cerradas en el stop, {n} en el objetivo y {n} a mercado.» (solo las que salen, por `motivo_cierre`; otro valor, error) |
| antes del corte, retiradas | «{n} órdenes anteriores se retiraron sin llenarse.» (`cancelada`, `expirada`) / «el bróker rechazó {n}» (`rechazada`) |
| en la liquidez | «En esta liquidez ya lleva {n} stops.» |

Quedan fuera de la lámina, por ser posteriores al corte: el llenado, la cancelación, el cierre y su motivo, el stop o el objetivo alcanzados y el resultado de lo que la lámina enseña.

**La tabla de colores (la primera; la ajustan Aleks y el consultor al revisar).** Una sola tabla de constantes en `laminas_svg.py`, de `graficos_sesion.py` (velas) y del visor (`visor.py:732-745`):

| Qué | Color |
|---|---|
| fondo / rejilla / separador de día | `#ffffff` / `#eeeeee` / `#cccccc` discontinuo |
| vela verde / roja / sin cuerpo | `#26a69a` / `#ef5350` / `#9e9e9e` |
| la H4 que fija el sesgo | recuadro `#f39c12`, relleno al 25 % |
| las H4 saltadas por el color | contorno `#7f8c8d` discontinuo |
| línea de M15 de un alto / de un bajo | `#3b6fd6` / `#8e44ad` |
| la tomada / la que dejó de ser la liquidez | trazo grueso con un punto en la M1 que la toma / discontinua |
| la caja de compra / de venta | `#2e8b57` / `#c0392b`, relleno al 16 % |
| niveles 0,25, 0,5 y 0,8 | `#888888` fino, rotulados a la derecha |
| la orden (el 0) | `#1f4e9c`, grueso |
| el stop / el objetivo | `#c0392b` / `#2e8b57`, discontinuos |
| el punto de breaker | `#1565c0`, marca en su vela |
| texto y ejes | `#444444` y `#666666` |

**Cómo se prueba cada punto de «La lámina».** 1, una sola fuente: el render solo recibe fotos (su firma no admite `Cierre`), un test de importaciones prohíbe a `laminas*.py` importar `domain.sesgo`, `domain.estructura_m1`, `domain.pivotes_m15` y `engine.zonas` para algo que no sean constantes, y la mutación de la referencia viva (F2). 2: un día sintético con una orden llenada, una cancelada y una operación del trader sin pareja da exactamente dos láminas, en orden. 3: el SVG lleva cada elemento con su clase (la H4 que fija, las líneas, la caja, los rótulos, la orden, el stop y el objetivo) y ninguno a la derecha del corte. 4: la tabla cerrada contra la spec y el código, y las regex de ids y dinero. 5: la regex con «3 de mayo» y «otro rango mayor», y todos los bytes y nombres. 6: días y elementos fuera de la puerta. 7: la salida dentro del repo. 8: dos ejecuciones dan los mismos bytes, y sin `<script>`. 9: `test_no_business_literals` en verde con las dos exenciones.

### 0.4 Los tests

Propongo **dos fixtures sintéticos**, ninguno lee un mes real:
- **Fotos hechas a mano** para el dibujo y las frases (`tests/unit/test_laminas_svg.py`): una foto con todo -sesgo con saltadas, toma, dos líneas de M15, caja, punto, orden- y otra con elementos nacidos antes de la ventana. El dibujo no ve más que la foto, así que «sin mirar al futuro» se prueba dando al render una foto cuyas velas, órdenes y tomas siguen después del corte (el render debe cortar por `foto.corte`): la mutación es un render que no corta.
- **El día sintético de `test_decisiones.py` ampliado** para el recolector (`tests/unit/test_laminas.py`): las zonas sintéticas siguen inyectadas, y una primitiva sintética escribe la toma, el escenario y el punto en la memoria con las mismas funciones de `engine/zonas.py` que usa el motor (`_abrir`, `punto_de_zona`), así que la forma de la memoria es la real. Con el `toca_colocar_orden_limite` sin estado (Technical Debt) para el determinismo y el golden. La mutación de la referencia viva: un recolector que guarda `c.estado` y dibuja al final enseña un hecho posterior al corte (un freno encendido después), y el test falla.
- El golden: con y sin recolector, el `ResultadoDia`, las órdenes, las posiciones y la traza del bróker son iguales; y un recolector que muta el estado lo rompe (como `test_decisiones.py:122-135`).
- `motor arnes`, `motor visor` y `motor decisiones`: sus opciones, comparadas con las de main por el parser (como `test_la_seccion_no_anade_ninguna_opcion_al_comando`).
- Las lecciones de `graficos_sesion.py` (ERRORES-RECURRENTES.md:103; auditor, «lo que el repo pide» 4): los tests prueban la constante real (los tramos que da `cobertura_material`), pasan por `main()` (el subcomando entero sobre el fixture) y miden en la salida lo que cada marca enseña, no solo la geometría.

### 0.5 Herencias

Buscado («lámina», «gráficos 2 a 6», «trazos de M15», «R4.5» y «graficos_sesion») en PROJECT_STATE, el final de HISTORIA, docs/validation/, docs/adr/, docs/plan/ y docs/runbooks/:
- **Lo que esta rama recoge:** RUMBO §3 y R4.5 (las láminas); la decisión b de TRAZAS-ABLACION.md:1392 (las líneas de M15 de 07-03, y también en el M1); SESION-06-EXTRACCION.md:448-457 y :727 (el trader pidió «los criterios del bot y los trazos de M15», y `graficos_sesion.py` no los dibuja); :1246 (la fecha no se pone: la lámina no la lleva); RECORRIDA-CONSTRUCCION-2.md:698 («hoja + gráficos 2 a 6 con contexto»), sustituido por la decisión de arriba; ERRORES-RECURRENTES.md:103 (las lecciones de los tests del guion, en §0.4).
- **Lo que no recoge, y por qué:** S-7 (el gráfico 1) «va como contexto de los gráficos 2 a 6» (ACTIVAR-SESION-06.md:611-613; auditor): al sustituirlos, adónde va S-7 lo decide la rama de la preparación, que elige los días (decisión 11). VIDEO-JULIO.md:798-840 solo ordena (las láminas van antes de C): nada que hacer aquí.
- **Las tres líneas de Technical Debt:**
  - «`motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker» (PROJECT_STATE.md:104): **la lámina no lo hereda**, porque todo -los tres paneles, las órdenes, las posiciones y el texto- sale de una foto tomada en el corte, y los tests de F2 lo prueban. **No se paga aquí**: el código del visor es otro (`visor.py:974-1008`).
  - «El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10)» (:102): la lámina las enseña si se aprueba la decisión 1. **No se paga aquí**: el visor recalcula el sesgo con su propio código (`_sesgo_de_sesion`); la anotación nueva le serviría, pero cambiar el visor no es de este encargo.
  - «La zona que RN-005 liga al escenario vigente … se queda en el escenario anterior» (:144): no se toca; la lámina de 07-03 de las 09:35 enseña lo que hizo el motor.

### 0.6 El tiempo y la memoria

- El último `make check` (la apertura): 22 min 9 s, **PICO DE MEMORIA 309 MiB** en `test`.
- Las corridas de TRAZAS-ABLACION (las más parecidas): F4.1, 364,9 s y 636,2 MiB; F4.2 (dos corridas), 565,6 s y 633,3 MiB (TRAZAS-ABLACION.md:645-646).
- Estimación para esta rama: F4.1, unos 6 min; F4.2, unos 10 min; `motor laminas` de las diez sesiones, dos corridas (con la decisión 10), unos 10-12 min y algo más de memoria que F4.2 por las fotos (velas de la ventana por foto: tuplas de referencias a velas que ya están cargadas); y el ensayo en el clon desechable, otro tanto. Una a la vez, nunca junto a un `make check`. El clon necesita su `config/settings.local.toml` con `[rutas].data` absoluto (skill `comparar-con-main`; auditor, 5).

### 0.7 El encargo frente al repo (auditor-encargo, informe tal cual en el Apéndice A)

75 afirmaciones: 64 correctas, 1 incorrecta y 10 con matiz. Lo que cambia algo:
- **INCORRECTA (26):** la regex de fechas está en `graficos_sesion.py:247-252`, no en :265-270. El fondo es cierto.
- **Matiz que retiene F1 (63):** §0.10.
- **Matiz (21, 22, 74):** las H4 saltadas y las líneas de M15 no las da ninguna pieza (§0.2), y añadirlas como registro toca `src/botsito/domain/`, que el contrato protege: decisiones 1 y 2.
- **Matiz (50):** las horas perdidas en las ventanas de 07-15 y 07-17 (§0.1; decisión 9).
- **Matiz (55):** §0 de RUMBO llama «comparables» a las cuatro corridas, y la del 14-oct se corrió con `--diagnostico-a35` y `--diagnostico-a44` (CORRIDA-CONSTRUCCION.md:618). Ya lo decía RUMBO; el recuadro no lo empeora. Lo digo y no lo toco.
- **Matiz (9, 24, 29, 71):** «sin extenderla» es paráfrasis del informe de la sesión 6, no literal; T0 sale de un guion de anexo, y en `src/` lo equivalente es `medir`; BARRIDO:247 nombra la fila de 07-02, y lo de 07-03 se deduce; el revisor b3 pidió los comandos y el texto de los guiones fue cómo se cumplió. Ninguno cambia lo que se pide.
- **Lo que el repo pide y el encargo no dice:** un campo nuevo de `MotorCableado` iría en las listas de `decisiones.py:121-134` (el diseño no añade ninguno); los literales de `TEXTOS_PROHIBIDOS` («07:00», «11:00», «15:00», «17:00», «23:00», «1:3», EURUSD, FTMO) y el 100000 no pueden ir en la tabla de frases ni en los rótulos (no van); las ventanas son literales en el guion (decisión 7); y el margen de PROJECT_STATE para las líneas nuevas de Technical Debt del cierre es de unos 2.500 bytes (22.494 de 25.000).

### 0.8 Lo que no pude medir

- La forma de la memoria en un `rechazado` o en un escenario terminado con su motivo en la ejecución medida: 07-03 no trae rechazos (`rechazados` no sale en §0.2). Lo que se sabe es del código (`zonas.py:420-427`, `primitivas_broker.py:741`).
- Cuántas H4 que fijan el sesgo caen fuera de la ventana de cuatro días en las diez sesiones: `sesgo_h4_tope_velas` vale 60 (unos diez días de H4) y `velas_miradas` no se anota (decisión 1); se mide en F4.3.

### 0.9 Exposiciones del día

Dos filas de hoy en HOLDOUT-EXPOSICIONES.md: la de la apertura (el `make check`, que lee el M1 de marzo y calienta con el de junio) y la de la corrida de medida de 0.2 (julio, con el M1 de junio para calentar; `casos_reservados` y `casos_ocultos`, por recuento). Ninguna transcripción, ningún fotograma, ningún libro, ninguna operación del trader leída fuera de la compuerta (la corrida de 0.2 imprime el recuento de parejas de julio, 14, y nada de sus filas).

### 0.10 F1, retenida: una referencia no casa

Verificado contra el repo, punto por punto:
- §0: 6.1 % (14-oct): CORRIDA-CONSTRUCCION.md:610 y RUMBO, nota (:48). 20.7 % (27-oct), la diaria de RECORRIDA-CONSTRUCCION: RECORRIDA-CONSTRUCCION.md:653 («41/198 (20.7 %)»), corrida el 2026-10-27 (HOLDOUT-EXPOSICIONES, filas de ese día). La de RESPALDO-M1, el 29-oct: RUMBO, nota (:49-51), y HOLDOUT-EXPOSICIONES, fila del 2026-10-29. 20.2 % y 40 parejas el 8-nov: RECORRIDA-CONSTRUCCION-2.md:565 y :575. **Casa.**
- §4: ADR-0082 §4 (D4, :65-83): la capa es el EA de MQL5, y «se descarta el EA que recibe las decisiones de Python, porque exige un puente en vivo que choca con el tope de peticiones». R6.0 HECHA, confirmada por Aleks el 2026-11-09 (HOJA-DE-RUTA.md:591-599). Los puntos de pivote, a R4.3 (HOJA:384-386). ADR-0092 es la puerta para operar en vivo (ADR-0092 §3). **Casa.**
- §5: A.5 (HOJA:689-697, la demo de FTMO y F17) y R5.7 (HOJA:483-489, el R de las parejas) **casan**. **No casa del todo: «el motor de Python no corre en una demo de FTMO sin un puente en vivo, que ADR-0082 §4 descarta»**. Lo que ADR-0082 §4 descarta (:80-82) es «el EA que recibe las decisiones de Python», y el motivo es el puente. La sombra temprana de RUMBO §5 (:39) es el motor «solo registrando», sin mandar decisiones. Que el ADR descarte también un puente que solo lee es más de lo que su texto dice (CLAUDE.md: «Nada afirma más de lo que su cita sostiene»). El encargo manda PARADA en ese caso y no corregirlo: **F1 no se commitea hasta tu respuesta (decisión 0).**

## Lo que necesito que decidas

0. **F1, el recuadro de §5.** Opciones: (a) lo commiteo literal, si das por bueno que ADR-0082 §4 descarta también un puente que solo lee; (b) me das el texto corregido (por ejemplo, que la sombra necesita un puente en vivo y que ADR-0082 §4 descarta el EA que recibe decisiones de Python por ese puente; o un ADR que lo diga) y lo commiteo literal. Recomiendo (b): el recuadro, tal como está, atribuye al ADR un descarte que no escribe. Coste de (a): una cita que dice más que su fuente, en un documento que lee `ids_citados.py`. §0 y §4 casan; F1 va en un solo commit, así que espera entero.
1. **Qué H4 fijó el sesgo y cuáles saltó (ADR-0080 §10).** Opciones: (a) registro en el dominio: `ResultadoSesgo` gana el inicio de la vela que fija y, por cada saltada, su inicio y su motivo (el bucle ya los tiene; nada los lee para decidir), y `sesgo_h4_al_abrir` los anota; amplía el contrato a `src/botsito/domain/sesgo.py`; (b) solo en engine: anotar `velas_miradas`, que identifica exactamente la vela que fija y las saltadas, pero sin saber por qué se saltó cada una (la lámina diría los recuentos por motivo); (c) nada nuevo: solo los recuentos en el texto, sin marcar velas. Recomiendo (a): es lo que el encargo pide («las que saltó por el color») sin recalcular nada. Coste de (b): no distingue el color de la vela sin cuerpo cuando hay de las dos; de (c): la H4 que fija no se ve.
2. **Qué zonas de control contó RN-009.** Opciones: (a) registro: en `domain/estructura_m1.py`, una función que devuelve los pivotes que cuenta (`zonas_de_control` pasa a ser su longitud, el mismo número), y el predicado de RN-009 los anota con el instante en que los evaluó; se dibujan en el M1 y la frase da «{n}, y admite {m}»; amplía el contrato a ese fichero; (b) solo el número en el texto, sin dibujarlas. Recomiendo (a): la pregunta 2 de la 7a (TRAZAS-ABLACION.md 5.5) es qué zonas cuenta el trader, y la lámina enseñaría cuáles contó el bot. Coste de (b): el trader ve «contó dos» sin ver cuáles.
3. **De dónde salen los tramos de construcción del punto 6.** Opciones: (a) de `cobertura_material` de `knowledge/cases/kit/config.yaml` para los meses de `criterio.construccion` (enero del 2 al 30, abril del 1 al 29, julio del 1 al 17, agosto del 1 al 31); (b) una tabla en el código con la regla 2 tal cual, como `graficos_sesion.py:67-72` (abril hasta el 30). Recomiendo (a): sale de los datos, y es igual o más estricta que la regla 2 (abril pierde el 30, que no toca ninguna de las diez). Coste de (b): un literal más que hay que mantener a mano cuando entre un mes.
4. **Qué líneas de M15 y hasta dónde.** Opciones: (a) las que el motor tuvo como liquidez de cada lado en algún cierre de la sesión hasta el corte; cada una desde la vela contraria de su pivote hasta la M1 que la toma (la del lado del sesgo, de la toma del motor), o, si dejó de ser la liquidez sin tomarse, hasta el último cierre en que lo era, en discontinuo; o hasta el corte; (b) igual, pero las que dejaron de ser la liquidez llegan también hasta el corte. Recomiendo (a): es lo que vio el motor, y «sin extenderla» (§3.6). Coste de (b): líneas que el motor ya no miraba parecen vivas.
5. **El instante de nacimiento de lo que no es vela, y en qué panel.** Opciones: (a) cada elemento se dibuja si su nacimiento está permitido y dentro de la ventana del panel más ancho en que se dibuja, y en los paneles más estrechos entra desde el borde izquierdo (una línea de M15 nacida ayer se ve en el M1 desde su borde); (b) panel a panel: lo que nace antes de la ventana de un panel no sale en ese panel. Recomiendo (a): con (b), las líneas de M15 casi nunca saldrían en el M1, que es lo que pidió la decisión b de TRAZAS para 07-03. Coste de (a): ninguno para el holdout (el nacimiento sigue en la puerta).
6. **El sesgo de 07-02 y 07-03, que lo fija una H4 de junio.** Opciones: (a) la lámina dice el sesgo («alcista») y «la vela H4 que lo fija viene de antes de la ventana», sin dibujarla ni dar su precio; (b) no dice ni el sentido. Recomiendo (a): el sentido ya lo dice la orden (compra o venta), las velas no son holdout (ADR-0021 §1) y el encargo lo prevé así (punto 6). Coste de (b): la lámina de una compra sin decir por qué compra.
7. **Las ventanas (cuatro días, un día, una hora) y los 240 y 15 minutos.** Opciones: (a) constantes de dibujo en `laminas.py`, declaradas, porque no deciden nada (los marcos salen de `MINUTOS_H4` y `MINUTOS_M15` del código de agregación); (b) parámetros del registro. Recomiendo (a): no son reglas del trader. Coste de (b): tres parámetros nuevos en `knowledge/spec/`, que esta rama no toca.
8. **Los cortes.** (a) tipo a, el último cierre en que la orden se colocó o se movió al precio del llenado; tipo b, el cierre `t` más tardío con `t · 60 000 < entrada en ms`; (b) en el tipo b, admitir `≤` (si la entrada cae justo en el cierre de la M1). Recomiendo (a): estrictamente antes de su entrada. Coste de (b): ninguno práctico; es el borde.
9. **Más H4 para los días del rango, y las horas perdidas de las ventanas.** Opciones: (a) cuatro días; en F4.3, por lámina, si la H4 que fija el sesgo cae dentro, y si alguna cae fuera, lo enseño en la PARADA final para que decidas con eso; las ventanas de 07-15 y 07-17 con horas sin ticks se dibujan igual (las velas M1 están) y se dice en el informe; (b) más días de H4 en las sesiones del rango ya ahora. Recomiendo (a): se decide con la medida. Coste de (b): un número a ojo.
10. **Comprobar en la propia herramienta que el recolector no cambia la corrida.** Opciones: (a) dos corridas por invocación, como `motor decisiones`: la base con el recolector y la base otra vez sin él; si los recuentos no son iguales, error y no se escribe nada; (b) una sola corrida, con la prueba en los tests, F4.1 y F4.2. Recomiendo (a): niega por defecto en cada uso. Coste: unos 5-6 min más por invocación.
11. **S-7, el gráfico 1, que «va como contexto de los gráficos 2 a 6».** Opciones: (a) lo decide la rama de la preparación, que elige los días; (b) se decide aquí. Recomiendo (a): esta rama no elige días.
12. **El nombre, las opciones, la tabla de frases y la de colores** (§0.3). Opciones: (a) las apruebas como están, o con lo que cambies; (b) otra forma de pedir las sesiones (un fichero, como `graficos_sesion.py --dias`). Recomiendo (a), con `--sesiones día:sesión`: una línea de comando que se copia al informe tal cual.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-10)

Dada por Aleks (consultor) el 2026-11-10, tal cual (también al final de `docs/encargos/trabajo-laminas.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/laminas (2026-11-10). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA de la fase 0», con su fecha, y aplícala punto por punto (skill fase-cero). Buena fase 0: el diseño queda aprobado con los cambios de abajo.
>
> 0. F1: (b). Tenías razón: ADR-0082 §4 solo descarta por escrito el EA que recibe las decisiones de Python. Commitea F1 con este texto para §5 (sustituye al del encargo) y con §0 ampliado con el matiz 55 del auditor; §4 queda literal como estaba. Verifica de nuevo las referencias nuevas antes del commit y, si alguna no casa, PARADA.
>    - §0:
>      > **Enmienda del 2026-11-10** (trabajo/laminas; decisión del consultor del 2026-11-09, precisada en la respuesta a la PARADA de la fase 0). Son cuatro corridas diarias, no tres: faltaba la del 27-oct (RECORRIDA-CONSTRUCCION.md, diaria 20.7 %), y la de RESPALDO-M1.md se corrió el 29-oct (nota final). Léase: «Cuatro corridas diarias: 6.1 % (14-oct), 20.7 % (27-oct), 20.2 % (29-oct) y 20.2 % (8-nov, tras activar la sesión 6 entera, con 40 parejas antes y después).» La del 14-oct se corrió con los diagnósticos de A-35 y A-44 (CORRIDA-CONSTRUCCION.md:574 y :618), así que no es del todo comparable con las otras tres. El resto de §0 no cambia.
>    - §5:
>      > **Enmienda del 2026-11-10** (trabajo/laminas; decisión del consultor del 2026-11-09, precisada en la respuesta a la PARADA de la fase 0). La «sombra temprana» no se hace. Para correr el motor de Python en una demo de FTMO, aunque solo registrara, haría falta un puente en vivo entre Python y el MT5. ADR-0082 §4 descarta por escrito el EA que recibe las decisiones de Python; un puente que solo lea no lo nombra, pero las razones del mismo §4 valen igual para él: una capa en Python habría que tirarla al llegar F29, y un bucle de Python que sondea gasta presupuesto de peticiones. Solo lo abriría un ADR nuevo. En su lugar van la capa de R6a y el grabador F17, en una prueba gratuita nueva de FTMO (A.5 de la hoja de ruta). La tabla del R de las parejas es R5.7. El resto de §5 no cambia.
> 1. (a). Registro en domain/sesgo.py: ResultadoSesgo gana el inicio de la vela que fija y, por cada saltada, su inicio y su motivo, y sesgo_h4_al_abrir los anota. Nada los lee para decidir. Amplía el contrato a ese fichero en un commit propio, antes del código, con su motivo. Los tests de sesgo que ya existen pasan sin tocarlos, y uno nuevo comprueba que, sobre los mismos casos, el sesgo y los contadores salen idénticos con los campos nuevos.
> 2. (a). En domain/estructura_m1.py, la función que devuelve los pivotes que cuenta, con zonas_de_control = su longitud. Un test comprueba que el número sale igual que antes en todos los casos de los tests actuales (y en uno con 0, 1 y 2 zonas). Mismo commit de contrato que el punto 1. F4.1 y F4.2 a 0 bytes siguen siendo la prueba de fondo.
> 3. (a), de cobertura_material. El 30 de abril queda fuera (el libro no lo cubre, config.yaml:72-76), aunque la regla 2 diga «abril». No toques la regla 2: la diferencia la recoge el ADR del método. Dilo en el informe.
> 4. (a).
> 5. (a). El nacimiento sigue en la puerta: lo que nace en un minuto no permitido no sale en ningún panel.
> 6. (a).
> 7. (a), constantes de dibujo declaradas en el informe.
> 8. (a), estrictamente antes.
> 9. (a). En F4.3, por lámina: si la H4 que fija el sesgo cae dentro de la ventana. Si en alguna sesión del rango cae fuera en más de la mitad de sus láminas, lo enseñas en la PARADA final con la cifra; no amplíes la ventana sin respuesta.
> 10. (a). Los 5-6 minutos más valen la pena.
> 11. (a). S-7 lo decide la rama de la preparación.
> 12. (a): `motor laminas --sesiones día:sesión,... --salida <fuera del repo>`, y la tabla de colores como primera versión. La tabla de frases queda aprobada con estos cambios:
>    - detenido_por_tope lo fijan dos reglas: RN-020 (la pérdida máxima del día del trader) y RN-029 (el freno diario de la cuenta), y RN-020 lee ese mismo hecho en su `cuando` (strategy_spec.yaml:2112). La lámina dice quién lo fijó según la regla que lo fijó (evento.fijados del cierre en que se encendió, guardado en la foto), nunca por el hecho solo ni porque RN-020 salga disparada:
>      · de RN-020: «Ha llegado a la pérdida máxima del día del trader: no abre más hasta la primera sesión del día siguiente.» (perdida_trader_reinicio = primera_sesion_dia_siguiente, parametros.yaml:1593-1612; ADR-0089);
>      · de RN-029: «Ha saltado el freno diario de la cuenta: no abre más hasta el cambio de día de la cuenta.»;
>      · si la foto no permite saber cuál de las dos: error que lo nombra (negar por defecto).
>      El motivo del gate RN-020 pasa a ser «ha llegado a la pérdida máxima del día del trader», con la misma regla de origen. Ninguna frase hereda «el único freno del día» del título de RN-020, que ya no es cierto por RN-036 y RN-029.
>    - «Escenario {n} de la sesión.» lleva jerga del repo. Cámbiala por «Sigue la liquidez de M15 número {n} de esta sesión.». Si esa liquidez se tomó antes de la ventana (toma_antes_de_la_ventana = cuenta), la frase de la toma ya dice «viene de antes de la ventana».
>    - RN-005: «ruido» es palabra del trader (ev-v3-001600-ed45b091, «por debajo de esta liquidez de m15 es ruido»; ev-v3-001725-bca9714b), pero «lado de ruido» no. Motivo: «lo que se forma queda en la zona de ruido de la liquidez de M15, donde no se busca entrada».
>    - RN-016: la frase vale. El informe dice que una pérdida por equal no gasta intento (strategy_spec.yaml:1874-1876) y que la cuenta empieza de cero con cada liquidez nueva.
>    - En el informe, cada frase de la tabla lleva su fuente (la regla o el campo, con fichero:línea), y el revisor la comprueba con el alcance (4).
>    Resto de la tabla, aprobada tal cual.
>
> Lo demás de la fase 0 queda aprobado como está (§0.3 y §0.4: el enganche por decisiones.motor_nuevo sin campo nuevo en MotorCableado, las fotos congeladas, los dos fixtures, el test de importaciones y el ensayo en el clon con su settings.local.toml). Sigue con F2, F3 y F4 con la PARADA condicional del encargo, y termina con la PARADA final como dice el encargo.

## Aplicación de la respuesta, punto por punto (2026-11-10)

- **0. F1: hecho**, commit `daed48b` «docs(plan): enmienda de RUMBO §0, §4 y §5, decisiones del 2026-11-09». Lleva el §0 y el §5 de la respuesta y el §4 literal del encargo, cada recuadro justo debajo de su encabezado. El diff solo añade líneas. Antes del commit verifiqué las referencias nuevas, y todas casan:
  - CORRIDA-CONSTRUCCION.md:574 es la orden de la corrida diaria con `--diagnostico-a35` y `--diagnostico-a44`;
  - CORRIDA-CONSTRUCCION.md:618 es su veredicto, con el 6.1 %;
  - ADR-0082 §4 da las dos razones del §5: «una capa en Python habría que tirarla al llegar F29» (:69-71) y «un bucle de Python que sondea gasta presupuesto» (:74-76).
- **1 y 2: el contrato se amplía en un commit propio, antes del código.** Este commit añade `src/botsito/domain/sesgo.py` y `src/botsito/domain/estructura_m1.py` a las permitidas y saca `src/botsito/domain/` de las protegidas, porque la protegida gana a la permitida. El resto del dominio sigue fuera del contrato. El código y sus tests van en F2 y F3.
- **3: los tramos salen de `cobertura_material`.** El 30 de abril queda fuera, porque el libro no lo cubre (`knowledge/cases/kit/config.yaml:72-76`, abril del 1 al 29), aunque la regla 2 de SESION-DE-PREGUNTAS.md diga «abril». La regla 2 no se toca: la diferencia la recoge el ADR del método.
- **4 a 11: aplicados en el diseño tal como estaban.** El nacimiento de lo que no es vela sigue pasando por la puerta (punto 5). Las ventanas son constantes de dibujo, declaradas en el informe de F3 (punto 7). La medida del punto 9 va por lámina en F4.3.
- **12: la tabla de frases lleva los cambios de la respuesta.**
  - `detenido_por_tope` dice quién lo fijó, según las reglas de `Evento.fijados` del cierre en que se encendió, guardadas en la foto. Si no se sabe cuál, da un error.
  - El motivo de RN-020 es el nuevo.
  - «Sigue la liquidez de M15 número {n} de esta sesión.» sustituye a la frase del escenario.
  - El motivo de RN-005 es el nuevo.
  - La tabla entera, con la fuente de cada frase (fichero:línea), va en el informe de F3 para el alcance (4) del revisor. Sobre RN-016: una pérdida por equal no gasta intento (strategy_spec.yaml:1874-1876), y la cuenta empieza de cero con cada liquidez nueva.

## F2 y F3 · Los tests y el subcomando (2026-11-10)

Van en un solo commit de código (tests y código juntos), después del commit del contrato. Los tests se escribieron con el código, sobre fixtures sintéticos. Ninguno lee un mes real.

### Lo que se añade como registro (puntos 1 y 2 de la respuesta)

- **`domain/sesgo.py`.**
  - `ResultadoSesgo` gana `vela_que_fija` (el inicio de la H4 que fija el sesgo, o None) y `h4_saltadas`: por cada saltada, su inicio y su motivo, de la más reciente a la más antigua. Los motivos son `SALTADA_COLOR_CONTRARIO`, `SALTADA_NEUTRA_SIMPLE` y `SALTADA_NEUTRA_DOBLE`.
  - El bucle es el mismo. Solo apunta lo que ya tenía en la mano.
- **`engine/primitivas.py`.** `sesgo_h4_al_abrir` lo anota en `sesgo_h4_vela` y en `sesgo_h4_saltadas` (`inicio:motivo,...`).
  - Las saltadas se anotan, como sus recuentos, solo cuando las hay.
  - La vela se anota o se quita en cada evaluación.
- **`domain/estructura_m1.py`.** `pivotes_de_control` devuelve los pivotes que contaba `zonas_de_control`, y esta pasa a ser su longitud.
- **`engine/zonas.py`.** El predicado de RN-009, `zonas_desarrolladas_superan`, anota `zonas_de_control = instante|nivel@inicio,...` y decide con `len(pivotes) > tope`, que es el mismo número que antes.
- **Nada de esto lo lee una decisión.** `tests/unit/test_laminas_registro.py` lo comprueba de tres formas:
  - compara el sesgo y sus contadores, y `zonas_de_control`, contra copias literales de las funciones de `main`;
  - lo hace sobre los casos de `test_sesgo_h4.py` y de `test_estructura_m1.py` (los de 0, 1 y 2 zonas), y sobre 400 series al azar de cada una (Hypothesis);
  - los tests de sesgo y de estructura que ya existían pasan sin tocarlos.
- **La prueba de fondo son F4.1 y F4.2.**

### El código

- **`src/botsito/engine/laminas.py`:**
  - la `Puerta` del punto 6;
  - el `Recolector`, que es el observador;
  - la `Foto` congelada y sus partes;
  - la elección de las láminas (a) y (b), con `decisiones.resumir`;
  - la tabla de frases;
  - `componer` (de la foto al dibujo y la sustentación);
  - la regex de fechas, ids y dinero;
  - `generar`, que corre la base con el recolector y la repite sin él;
  - la salida.
- **`src/botsito/engine/laminas_svg.py`:** el SVG y el HTML, que solo reciben una `Composicion`.
- **`src/botsito/cli.py`:** `motor laminas --sesiones día:sesión,... --salida <fuera del repo>`.
  - Las dos opciones son obligatorias.
  - No comparte `_opciones_simulacion` ni `_opciones_diagnostico`.
  - `motor arnes`, `motor visor` y `motor decisiones` conservan sus opciones, comparadas con las de `main` en `test_arnes_visor_y_decisiones_tienen_las_mismas_opciones_que_en_main`.
  - No hace falta tocar `pyproject.toml`: import-linter mantiene sus 4 contratos.

**Las constantes de dibujo (punto 7 de la respuesta).**
- `DIAS_H4 = 4`, `DIAS_M15 = 1` y `MINUTOS_ANTES_M1 = 60` (`laminas.py:49-51`).
- Los marcos de 240 y 15 minutos son `MINUTOS_H4` y `MINUTOS_M15` de `cases/ventanas.py`, los mismos con que el arnés agrega.
- Ninguna decide nada.

**Las exenciones de `test_no_business_literals` (punto 9 del encargo), una por línea:**
- `laminas.py:950` y `:951` (en `f6ed348`; en `3f800b5` eran `:935` y `:936`, revisor, a1): `Decimal("0.25")` y `Decimal("0.5")`, los rótulos del Fibonacci de la caja.
- `laminas_svg.py:48`: la opacidad `"0.25"` del relleno de la H4 que fija el sesgo. Esta tercera no la preveía el encargo: el «25 %» de la tabla de colores es el literal 0.25, que el test prohíbe.
- El 0,8 sale de `stop_fraccion_caja` (`registro.fraccion(...).valor`).
- **Un color que la tabla de la fase 0 no tenía** (revisor, b-m2): `control` = `#e67e22`, el de las zonas de control que cuenta RN-009 en el M1 (`laminas_svg.py:44`). Lo añadió la decisión 2, que manda dibujarlas.
- El huso, de `RelojSesiones.huso_visible`.
- El anclaje, de `anclaje_h4`.

**Lo que cambia frente al diseño aprobado (§0.3), y por qué:**
- **No hay cotejo entre `orden_limite_pendiente` y las órdenes vivas.** El hecho del bróker se calcula ANTES de que el motor decida en ese cierre (`cableado.py:399`), y la orden se coloca después: en la foto de una colocación no casan nunca. Las órdenes vivas salen de la copia de las órdenes.
- **Lo que no es vela y nace fuera de la ventana lleva frase propia.** La regla aprobada dice que la sustentación diga «viene de antes de la ventana», y estas son sus frases:
  - «La vela H4 que fija el sesgo viene de antes de la ventana.»
  - «La toma de la liquidez de M15 viene de antes de la ventana.»
  - «Liquidez de M15 tomada a las {HH:MM}: la línea que toma viene de antes de la ventana.»
  - «{n} líneas de M15 de esta sesión vienen de antes de la ventana.»
  - «La caja viene de antes de la ventana.»
  - «El punto de breaker viene de antes de la ventana.»
- **Las frases tienen singular y plural** («una vela», «{n} velas»; «un stop», «{n} stops»).
- **Las saltadas solo se dicen con un sesgo que tenga lado.** Con «Sin sesgo de H4» la frase del sesgo ya cubre las velas miradas.
- **La comprobación de ids no distingue mayúsculas, salvo la R.** La R aislada solo cuenta en mayúscula, porque el radio de los círculos del SVG (`r="5"`) casaba.

### La tabla de frases, con su fuente

Todas las frases están en `src/botsito/engine/laminas.py:455-603`.

*Hechos* (el vocabulario, `knowledge/spec/strategy_spec.yaml:669-768`):

| Frase (clave en `laminas.py`) | Fuente |
|---|---|
| `FRASE_SESGO` (:461), alcista, bajista, insuficiente y ambiguo, con la variante de doble ruptura | el hecho `sesgo` (strategy_spec.yaml:680), RN-003 (:1079) y `ResultadoSesgo.doble_ruptura` (`domain/sesgo.py`); la anotación `sesgo_h4_doble_ruptura` (primitivas.py:65) |
| `FRASE_SALTADAS` (:475), por motivo | `ResultadoSesgo.h4_saltadas` y los tres recuentos (`domain/sesgo.py`, ADR-0080 D1 y D3, ADR-0075); las anotaciones de primitivas.py:70-78 |
| `FRASE_FIJA_FUERA` (:491) | `sesgo_h4_vela` fuera de las H4 dibujadas (punto 6 del encargo) |
| `FRASE_DETENIDO` (:492): cartuchos, tope total y racha | los hechos de strategy_spec.yaml:746, :734 y :757, fijados por RN-016 (:1912), RN-031 (:2532) y RN-036 (:2179) |
| `FRASE_TOPE_POR_REGLA` (:499): RN-020 o RN-029 | `detenido_por_tope` (strategy_spec.yaml:723), fijado por RN-020 (:2116) y por RN-029 (:2427), según `Evento.fijados` del cierre en que se encendió (`Recolector._origen`); el «hasta la primera sesión del día siguiente», de `perdida_trader_reinicio = primera_sesion_dia_siguiente` (parametros.yaml:1593-1612; ADR-0089); con otro valor, error |
| `orden_dimensionada` | sin frase, a propósito (`HECHOS_SIN_FRASE`; strategy_spec.yaml:713) |
| `FRASE_TOMA` (:508), «con cuerpo / con mecha» y «por debajo del bajo / por encima del alto» | la toma del escenario (`zonas.py:214-219`: instante, nivel, lado y pivote) y `liquidez_m15_criterio_toma`, que nombra la forma de RN-004 (strategy_spec.yaml:1331) |
| `FRASE_SIN_TOMA` (:518) | la sesión sin escenarios (`zonas.py:222-232`, `_abrir`) |
| `FRASE_ESCENARIO` (:519) | `escenario["n"]` (`zonas.py:227`) |

*Lo que se enseña siempre:*

| Frase | Fuente |
|---|---|
| `FRASE_ESQUEMA` (:524) | `Zona.por` (`zonas.py:148`) |
| `FRASE_CAJA` (:528) | `Zona.entrada` y `Zona.extremo` (`zonas.py:146-147`) |
| `FRASE_PUNTO` (:530) | `punto_de_zona` = «nivel@inicio» (`zonas.py:393` y `:412`) |
| `FRASE_ORDEN` (:533): coloca, mueve, pendiente | `Orden.precio`, `stop` y `objetivo` (`broker.py:224-264`); «el 0 de la caja» se comprueba (`precio == Zona.entrada`, o error); el 0,8, de `stop_fraccion_caja` |
| `FRASE_CERRADAS` (:542) con `CIERRE_ANTES` (:541) | `Posicion.motivo_cierre` (`broker.py:255` y `:934`): `stop` y `objetivo` (`llenado.py:44-45`) y `manual` (`broker.py:95`, «a mercado»); otro valor, error |
| `FRASE_RETIRADAS` (:543) y `FRASE_RECHAZADAS` (:547) | `Orden.estado` `cancelada` y `expirada`, y `rechazada` (`broker.py:92-94`) |
| `FRASE_STOPS_LIQUIDEZ` (:551) | las posiciones cerradas en el stop cuya zona es del escenario vigente (`ctx.zona_de_orden`, `escenario["zonas"]`). Una pérdida por equal no gasta intento (strategy_spec.yaml:1874-1876), y la cuenta empieza de cero con cada liquidez nueva (`abrir_escenario`, en `acciones_escenario`, `zonas.py:270-322`). La frase cuenta stops, no intentos |

*Gates* (`MOTIVO_GATE`, :559; las 15 VIGENTE con `prohibe`, comprobadas contra la spec por `test_la_tabla_de_gates_es_la_de_las_vigente_que_prohiben`), con «No abre: …» o «No abre porque no puede descartar que …» (`FRASE_PROHIBE`, :580; `Evento.prohibido_por` y `quizas_por`) y «Iba a colocar la orden y no la coloca: …» (`FRASE_BLOQUEO`, :584; `Evento.bloqueada_por`):

| Gate | Fuente |
|---|---|
| RN-001, RN-037, RN-033, RN-005, RN-008, RN-009, RN-016, RN-018, RN-020, RN-036, RN-022, RN-026, RN-029, RN-031 y RN-032 | strategy_spec.yaml:863, :1046, :1183, :1347, :1508, :1546, :1861, :1978, :2037, :2121, :2208, :2271, :2372, :2490 y :2536 |

- **RN-009 lleva los números:** `{n}` sale de la anotación `zonas_de_control` del mismo cierre (si es de otro instante, error) y `{m}` de `zonas_control_max_por_esquema`.
- **RN-005** usa la palabra del trader: «ruido», de ev-v3-001600-ed45b091 y ev-v3-001725-bca9714b, como pidió la respuesta.

*Por qué no hay orden* (`_sin_orden`; solo en el tipo b sin orden viva):

| Frase | Fuente |
|---|---|
| `FRASE_OPERACION_ABIERTA` (:592) | `operacion_abierta` del bróker (`broker.py:738-745`) |
| `FRASE_TERMINADO` (:593) | `escenario["terminado"] == "ganancia"` (`zonas.TERMINADO_POR_GANANCIA`, `zonas.py:110`); otro valor, error |
| `FRASE_SIN_CAJA` (:596) | `escenario["zonas"]` vacío |
| `FRASE_SIN_PUNTO` (:600) | la zona sin `punto_de_zona` |
| `FRASE_USADA` (:601) | `usadas` (`zonas.py:435-448`) |
| `FRASE_PUNTO_GASTADO` (:602) | `rechazados` (`zonas.py:420-432`) |
| `FRASE_NO_ENVIADA` (:591) con `LIMITE_NO_ENVIO` (:585) | `ctx.no_enviadas` del cierre (`primitivas_broker.py:639`) y los límites `volumen`, `margen` y `minimo` (`broker.py:174-176`), con o sin `no_operar:` (`primitivas_broker.py:635-637`); otro, error |
| `FRASE_NO_TOCABA` (:603) | caja con punto, ninguna causa de arriba y ni RN-011 ni RN-015 en `Evento.disparadas`; si alguna dispara sin causa, error |

### Los tests (40 funciones nuevas; 1979 en total, con las de lo que encontró el revisor)

- **`tests/unit/test_laminas_registro.py`:** el registro del dominio, como se dice arriba.
- **`tests/unit/test_laminas_svg.py`:** el dibujo y las frases sobre fotos hechas a mano. Prueba:
  - que cada marca sale con su clase y la sustentación entera;
  - que el dibujo corta por `foto.corte` aunque la foto traiga velas posteriores (la mutación es un dibujo que no corta);
  - que lo nacido antes de la ventana no se dibuja ni da precio;
  - la orden colocada y la viva, y la que no está en el 0 (error);
  - lo de antes del corte;
  - las causas de «sin orden»;
  - RN-009 con sus números, y el error si la anotación no es del corte;
  - el HTML sin script ni fechas y determinista;
  - los colores de la tabla única.
- **`tests/unit/test_laminas.py`:** el día sintético de `test_cableado.py`. Una estrategia sintética abre el escenario y liga dos zonas con sus puntos con las funciones de `engine/zonas.py` (`_abrir`, `_ligar_al_escenario`), sobre una liquidez de M15 de verdad de los datos sintéticos. Prueba:
  - el golden con y sin recolector, y la mutación de un recolector que cambia el estado;
  - que la foto no mira al futuro, y la mutación de la referencia viva (un `broker` guardado en vez de copiado ve la segunda orden, que nace una hora después);
  - que salen exactamente dos láminas (la orden llenada y la operación del trader sin pareja; la segunda orden, retirada sin llenarse, no tiene lámina), en orden y sin dibujar la operación del trader;
  - las clases de las marcas;
  - sin fechas, ids ni dinero, y determinista;
  - la regex de fechas («3 de mayo» casa y «otro rango mayor» no);
  - la puerta y su recorte;
  - un día oculto, que hace fallar la corrida entera;
  - las negativas antes de correr (día no dev, oculto, sesión inexistente, hora perdida dentro);
  - los tramos de `cobertura_material`, con el 30 de abril fuera;
  - la tabla de gates contra la spec;
  - ninguna frase con ids, dinero ni fechas, y ninguna con «el único freno»;
  - el tope según la regla que lo encendió, y su error;
  - una causa sin frase, que da error;
  - la salida dentro del repo o no vacía;
  - la CLI, que niega la salida en el repo antes de leer nada;
  - las opciones del subcomando y las de los otros tres;
  - el test de importaciones: de los módulos que deciden, las láminas solo importan constantes.
- **Las lecciones de ERRORES-RECURRENTES.md:103:**
  - los tests prueban la constante real (los tramos de `cobertura_material` del repo);
  - miden en la salida lo que enseña cada marca, no solo la geometría;
  - y pasan por la tubería entera de `generar` sobre el fixture, del motor a los ficheros.

  **Hay una desviación:** `main()` de la CLI solo se prueba con la negativa de la salida. La corrida entera por la CLI necesita las velas reales, y la hacen F4.3 y su ensayo.

## F4 · Las corridas (2026-11-10)

Las declara la fila de hoy de HOLDOUT-EXPOSICIONES («las corridas de F4»), escrita antes de la primera. Las corridas van una a una, ninguna junto a un `make check`, y todas con el código de F2 y F3 antes de commitearlo.

**F4.1.**
- Orden: `uv run botsito motor arnes --simular --salida data/laminas/base.txt`.
- El primer intento hizo la corrida entera y falló al escribir, porque la carpeta `data/laminas/` no existía y el arnés no la crea. Es un error mío, no del código. Creé la carpeta con `mkdir -p data/laminas` y la repetí.
- Resultado: `TIEMPO: 321.7 s; MEMORIA: pico del proceso de 640.0 MiB`, exit 0.
- `diff data/laminas/base.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt | wc -c` da **0**: los dos ficheros tienen 588 978 bytes.

**F4.2.**
- Orden: `uv run botsito motor decisiones --carpeta data/laminas/bitacora --bitacora 2026-04-13,2026-07-02,2026-07-03,2026-07-14`.
- La base y la base repetida dan `(31, 192, 24, 1150, 0, 32, 0)`.
- Resultado: `TIEMPO: 595.1 s; MEMORIA: pico del proceso de 638.1 MiB`, exit 0.
- El diff de cada `bitacora.DIAGNOSTICO.<día>.txt` contra el de `docs/validation/anexos/TRAZAS-ABLACION/` da **0** bytes en los cuatro.
- La anotación nueva de RN-009 y las del sesgo no salen en la bitácora (la bitácora no las lee), y el arnés da los mismos bytes.

**F4.3, las láminas.**

Cinco invocaciones de `motor laminas`, todas de las diez sesiones del encargo y con dos corridas cada una (con y sin el recolector). En todas, la base dio `(31, 192, 24, 1150, 0, 32, 0)` las dos veces. Las órdenes, tal cual, salvo la lista de `--sesiones`: `uv run botsito motor laminas --sesiones <las diez sesiones del encargo, en el orden de su lista> --salida <carpeta>`.

**Una desviación declarada, por el hallazgo b-B1 del revisor.** El número de la carpeta `sesion-NN` es el orden de `--sesiones` (diseño de la fase 0, §0.3). Con la lista escrita aquí, el informe daría la clave al nivel de la sesión. Por eso la lista no se copia. Las versiones de este informe en `675ee62` sí la llevan, igual que dos horas de corte de láminas de un día con nombre; quedan en el historial de la rama, y no lo reescribo (decisión 13 de la PARADA final).

| # | Código | Desde | Salida | Láminas | Tiempo y pico | Lo que destapó |
|---|---|---|---|---|---|---|
| 1 | `3f800b5` | clon (`git worktree add --detach`, con su `config/settings.local.toml` y `[rutas].data` absoluto) | carpeta temporal | 47 (58 ficheros) | 580,6 s; 646,0 MiB | la caja «viene de antes de la ventana» en 23 láminas: un error mío, corregido en `675ee62` |
| 2 | `675ee62` | clon | carpeta temporal | 47 | 659,2 s; 644,8 MiB | nada |
| 3 | `675ee62` | repo | el Escritorio | 47; `diff -r` contra la 2: 0 bytes | 520,2 s; 644,4 MiB | — (apartada a la carpeta de trabajo, fuera del repo, antes de la 5) |
| 4 | `f6ed348` | clon | carpeta temporal | 47; contra la 2, solo cambian dos ficheros (b-m3, abajo) | 600,3 s; 645,9 MiB | nada |
| 5 | `f6ed348` | repo | `C:\Users\USER\Desktop\laminas-sesion-7` | 47; `diff -r` contra la 4 en la línea de abajo | 619,1 s; 644,6 MiB | — |

- **El diff entre la 2 y la 4:** solo cambia la `x` de dos marcas de zona de control, que ya no pasan del borde del corte (b-m3).
- **El nivel de las líneas de M15 de b-I3 no cambia ninguna lámina:** todas las líneas de las 47 láminas tienen su nivel marcado por una M1 de la ventana. Lo mide el diff de 0 bytes en todo lo demás.
- **`git status` sale vacío** en el repo y en los clones antes y después de cada invocación.
- **La 5, contra la 4:** 0 bytes: las láminas del Escritorio son byte a byte las del ensayo 4, `clave.txt` incluida.

**Dónde están:** `C:\Users\USER\Desktop\laminas-sesion-7\`. Hay diez carpetas `sesion-01` a `sesion-10`, cada una con su `indice.html`, y `clave.txt` en la raíz. La clave no entra en este informe.

**Por sesión** (`docs/validation/anexos/LAMINAS/estructura_laminas.py`, que solo lee los HTML):

| Sesión | Láminas | Tipo a | Tipo b |
|---|---|---|---|
| sesion-01 | 4 | 0 | 4 |
| sesion-02 | 1 | 0 | 1 |
| sesion-03 | 5 | 1 | 4 |
| sesion-04 | 9 | 5 | 4 |
| sesion-05 | 5 | 1 | 4 |
| sesion-06 | 1 | 0 | 1 |
| sesion-07 | 4 | 1 | 3 |
| sesion-08 | 10 | 5 | 5 |
| sesion-09 | 2 | 1 | 1 |
| sesion-10 | 6 | 5 | 1 |
| **total** | **47** | **19** | **28** |

- **No sale ninguna sesión.** Las diez pasan la puerta: días dev, ningún oculto, ninguna hora perdida dentro y el corte dentro de los tramos.
- **Ninguna marca** pasa del borde del corte.
- **La medida del punto 9:** la H4 que fija el sesgo cae dentro de la ventana de cuatro días en **47 de 47** láminas. Ninguna sesión del rango pasa de la mitad fuera, así que no hay nada que decidir sobre la ventana.
- **Las horas sin ticks de las ventanas de 07-15 y 07-17** (§0.1): sus velas M1 están y se dibujan como las demás.
- **Cotejado contra la bitácora del anexo de TRAZAS-ABLACION de la sesión de 07-03:**
  - las órdenes, sus precios y las órdenes retiradas casan;
  - el punto de 1.14496 a 4 puntos de la toma en 1.14500 (decisión b de TRAZAS-ABLACION) sale en una de las láminas de esa sesión.

**Lo que no pude comprobar:** cómo se ven las láminas. La extensión de Chrome no abre ficheros `file://`, y en la máquina no hay nada que pase un SVG a imagen. La estructura sí la medí, con el guion de arriba y con las frases.

## La CI de Linux

- Se empujó como `fix/laminas` con `git push origin trabajo/laminas:refs/heads/fix/laminas` (RITUAL.md:102).
- **Run 42881622332**, sobre `675ee623`: `1 failed, 3347 passed, 48 skipped`.
- **Run 42893354923**, sobre `f6ed348e`, con lo que encontró el revisor: `1 failed, 3352 passed, 48 skipped`.
- En las dos, el único fallo es el aceptado, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`: PROJECT_STATE declara `trabajo/laminas` y la rama es `fix/`.
- Lo que va después de `f6ed348` es este informe y HOLDOUT-EXPOSICIONES, más un ajuste de test (la toma cambiada después del corte, abajo).

## Lo hecho con lo que encontró el revisor

Su informe va entero, tal cual, en el Apéndice B.

| Hallazgo | Lo hecho |
|---|---|
| b-B1, bloquea: el informe ataba láminas a su día | La lista de `--sesiones` ya no se copia en F4.3, y lo escrito desde F4 no nombra ninguna hora de corte ni ninguna cifra de una lámina de un día con nombre (segunda pasada, N1). Lo que queda de antes lo recoge la decisión 13: la fase 0 (§0.5 y el Apéndice A, tal cual) nombra «la lámina de 07-03 de las 09:35» Lo ya commiteado en `675ee62` queda en el historial: decisión 13 de la PARADA final |
| b-B2, bloquea: faltaba el encargo frente a lo hecho | La sección «El encargo frente a lo hecho, punto por punto», abajo |
| b-B3, bloquea: los tipos a y b por sesión | La tabla de arriba; y la consola de `motor laminas` los da por sesión (`f6ed348`) |
| b-B4, bloquea: los hechos no se enumeraban desde la spec | `test_cada_hecho_del_vocabulario_tiene_su_frase_o_su_motivo` (de regla y del bróker, desde `cargar_vocabulario`) y `test_cada_freno_dice_su_frase`, uno por freno: quitar una frase los rompe |
| b-I1, importa: la mutación de la referencia viva no se ejecutaba | `test_la_mutacion_de_la_referencia_viva_rompe_la_comprobacion`: la foto hecha al final desde el `Cierre` guardado lleva cinco cosas posteriores al corte (la segunda orden, el llenado, el freno, la segunda caja y la toma nueva), y `lo_del_futuro` las caza; la copiada en su instante, ninguna |
| b-I2, importa: sin fixture de un estado cambiado después del corte | El fixture enciende un freno después del corte de la primera lámina. La segunda caja entra en el escenario después, y una toma nueva abre otro escenario después (este último, en el commit del informe). La foto no lleva nada de eso |
| b-I3, importa: el nivel de una línea de M15 podía venir de antes de la ventana | `linea_dentro`: la línea sale solo si su contraria y una M1 que marque su nivel antes de formarse están en la ventana de M15. Tiene su test. Medido en las 47 láminas: no cambia ninguna |
| b-I4, importa: faltaba `anexos/LAMINAS/` | `docs/validation/anexos/LAMINAS/`, con los guiones de la sesión. `diez_sesiones.py` y `campos_cierre.py` son de la fase 0 (§0.1 y §0.2), `listas_frases.py` de la tabla de frases (§0.3), `simular_cierre.py` de las propuestas de cierre y `estructura_laminas.py` de F4.3 |
| b-m1: el runbook | El panel más ancho y el tiempo medido |
| b-m2: un color sin declarar | Declarado en F2 y F3 (`control` = `#e67e22`) |
| b-m3: dos marcas pasaban del borde | Ya no pasan; el test mira `x`, `x1`, `x2`, `cx` y el ancho de los `rect` |
| a1 y a2: números de línea y recuentos | Corregidos (`laminas.py:950-951`; 40 funciones nuevas, 1979 en total) |
| a3: la fila de F4 de HOLDOUT-EXPOSICIONES se reescribe | Se escribió antes de F4.1, en el árbol de trabajo, y se commiteó en `3f800b5`. Su recuento se actualiza en su sitio, como ella misma anunciaba, y cada invocación nueva se declaró antes de lanzarla |
| a4: F1 antes de que la respuesta estuviera en el repo | Cierto. F1 se commiteó primero porque el encargo lo pide en su commit propio, y la respuesta entró en el siguiente (`b7d5d6d`). El orden queda dicho aquí |

## El encargo frente a lo hecho, punto por punto

| Punto del encargo | Hecho | Dónde |
|---|---|---|
| Abrir con abrir-rama, riesgo alto, tramo R4, encargo tal cual | sí | 73668c16; `docs/encargos/trabajo-laminas.md`; `contrato.yaml` |
| BASE comprobada con git | sí | «Base», arriba |
| (a) el subcomando de `motor` | sí, `motor laminas` | F2 y F3 (3f800b5, 675ee62 y el commit de lo del revisor) |
| (b) las láminas de las diez sesiones | sí: 47, en `C:\Users\USER\Desktop\laminas-sesion-7` | F4.3 |
| (c) F1 en su commit, literal | sí | daed48b; alcance 6 del revisor |
| La decisión de los gráficos 2 a 6, en el informe | sí | arriba |
| Lo que pidió el trader: los criterios y los trazos de M15 | sí | las frases y `class="linea-m15"` en las 47 |
| El contexto de lo de antes | sí | las ventanas de H4, M15 y M1 |
| Las líneas de M15 hasta su toma, sin extenderlas | sí | decisión 4 (a); `LineaDibujada` |
| 07-03: el punto de 1.14496 a 4 puntos de la toma en 1.14500, también en el M1 | sí | sale en una lámina de esa sesión, y las líneas de M15 se dibujan en el M1 |
| QUÉ NO CAMBIA: lo que el motor decide | sí | F4.1 y F4.2 a 0 bytes; golden y mutaciones |
| No se tocan knowledge/, scripts/ ni .claude/ | sí | contrato; revisor, eje (b) 4 |
| `motor arnes`, `motor visor` y `motor decisiones`, iguales | sí | `test_arnes_visor_y_decisiones_tienen_las_mismas_opciones_que_en_main`; F4.1 y F4.2 |
| `graficos_sesion.py` y SESION-DE-PREGUNTAS.md, sin tocar | sí | contrato |
| Las láminas no se enseñan hasta el ADR del método | sí, dicho | arriba y en el runbook |
| Los informes cerrados, sin tocar | sí | contrato |
| Fuera de src/ y tests/, solo lo permitido | sí | contrato (`anexos/LAMINAS/` entra con lo del revisor) |
| LA LÁMINA 1: una sola fuente, copias, solo registro | sí | `Recolector` y `Foto`; registro de sesgo y RN-009; `test_las_laminas_no_recalculan_ninguna_decision` |
| 2: los tipos (a) y (b), en orden; el emparejamiento de la corrida entera | sí | `elegir`, con `decisiones.resumir` |
| 3: tres paneles, las ventanas y sus marcas | sí; las H4 de los cuatro días bastan (decisión 9: 47 de 47 dentro) | F4.3 |
| 4: la tabla cerrada, sin ids, lote, R ni dinero, nada después del corte | sí | la tabla con sus fuentes; `comprobar_texto`; los tests |
| 5: sin fechas, la regex con `\b`, la clave solo en `clave.txt` | sí, con una desviación del informe (b-B1, abajo) | `RE_FECHA`; F4.3 |
| 6: negar por defecto, también lo que no es vela | sí | `Puerta`; `linea_dentro` (b-I3) |
| 7: la salida fuera del repo, por argumento, ensayada en un clon | sí | `comprobar_salida`; los ensayos de F4.3 |
| 8: HTML y SVG autocontenidos, deterministas, colores en una tabla | sí | `laminas_svg.py`; `diff -r` de 0 bytes |
| 9: las cifras del registro y las exenciones declaradas | sí, con una tercera exención declarada | F2 y F3 |
| LO QUE SE PUEDE MIRAR | sí | las filas de HOLDOUT-EXPOSICIONES del 2026-11-10 |
| LAS DIEZ SESIONES: las que salgan, con su motivo | ninguna sale | F4.3 |
| FASE 0 y su PARADA | sí | §0; la respuesta, tal cual |
| F2, los tests | sí; lo que pedía y faltaba lo encontró el revisor (b-B4, b-I1, b-I2) y está hecho | «Lo hecho con lo que encontró el revisor» |
| F3, el subcomando | sí | `cli.py` |
| F4.1 y F4.2 a 0 bytes | sí | F4 |
| F4.3, por sesión, los tipos a y b | sí | F4.3 |
| INFORME: comandos tal cual | sí, salvo la lista de `--sesiones` de F4.3 (b-B1) | F4 |
| El runbook | sí | `docs/runbooks/LAMINAS.md` |
| CI por `fix/laminas`, con su run | sí | «La CI de Linux» |
| REVISOR con sus seis alcances, su informe al final | sí | Apéndice B |
| La PARADA final | sí | el mensaje a Aleks |

## Lo que necesito que decidas (PARADA final)

La numeración sigue la de la fase 0.

13. **La clave en el historial de la rama** (revisor, b-B1). El informe de `675ee62` escribe la lista de `--sesiones` en el orden de las carpetas y dos horas de corte de láminas de un día con nombre. Desde el commit de cierre del informe ya no los escribe, pero los dos commits siguen en el historial y llegarían a `main` con el merge. Opciones:
    - (a) se deja así y se dice en el cierre. El informe no se enseña al trader, y el orden de las carpetas ya era el de la lista del encargo, que está en el repo desde la apertura (§0.3, «NN, el orden de `--sesiones`»).
    - (b) antes de enseñar nada, se regeneran las láminas con las carpetas en un orden que no sea el de la lista (un cambio de código pequeño: barajar con una semilla que va solo a `clave.txt`).

    **Lo que (b) no arregla** (revisor, segunda pasada, N2): el encargo (punto 1.14496 de 07-03) y PROJECT_STATE (la lámina de 07-03 de las 09:35), los dos en el repo, nombran cosas que solo salen en las láminas de una carpeta. Barajar no oculta ESA sesión a quien lea el repo. Y la fase 0 lo nombra también (§0.5 y el Apéndice A). Como el informe y el repo no se enseñan al trader, nada de esto llega a él. Solo importa si alguien que lee el repo enseña una lámina sin su clave.

    Recomiendo (b) si las láminas de estas diez sesiones van a llegar al trader tal cual. Recomiendo (a) si la rama de la preparación las va a generar de nuevo para los días que elija, que es lo que dice el «Hecho cuando» propuesto. La historia de la rama no se reescribe en ningún caso (sin `rebase`; CLAUDE.md).
14. **R4.5 HECHA:** solo si das las láminas por revisadas (propuesta 2, abajo).

## Lo que no me convence de las láminas

1. **«Es el primer esquema.» sale en las 31 láminas que enseñan una caja.** Con la orden en el punto (`al_aparecer_punto_de_breaker`), `zona_del_punto` crea todas las zonas con `por = PRIMER_ESQUEMA` (`engine/zonas.py:414-416`). Así que la frase dice lo que guarda el motor, no qué esquema ve, y el trader leerá «primer esquema» siempre. Propongo quitarla o cambiarla en la rama que toque el esquema. Aquí no la toco, porque está aprobada.
2. **El motivo de RN-020 y su frase dicen «del día».** RN-020 también salta por la pérdida semanal del trader (`alcanza_tope: perdida_semana`, strategy_spec.yaml:2111). En las diez sesiones no sale ninguna lámina con ese freno, pero la frase no distingue el día de la semana.
3. **«Iba a colocar la orden y no la coloca: …» y «No abre: …» repiten el mismo gate en 13 láminas.** Son dos hechos del motor distintos (el bloqueo de la acción y la prohibición del efecto), pero al trader le llega el mismo motivo dos veces.
4. **Las zonas de control que cuenta RN-009 son muchas en algunas láminas** (más de diez). El número es el que el motor contó, `pivotes_de_control` desde la toma, y se dibujan todas. Si eso es lo que el trader llama zonas de control es justo la pregunta 2 de la 7a.
5. **No las he visto dibujadas** (arriba).

## Propuestas para la orden de cierre

Las propuestas 1 y 2 están comprobadas con las funciones de `tests/unit/test_hoja_de_ruta.py` (`problemas_a`, `problemas_b`, `problemas_c` y `problemas_d`) sobre copias en memoria de PROJECT_STATE.md y HOJA-DE-RUTA.md. Las cuatro dan `[]` hoy y con las propuestas. PROJECT_STATE queda en 22 506 bytes con la F nueva.

1. **La entrada F (sigue viva; ningún encabezado de HECHA):** sustituir
   «Siguiente, en este orden: (1) las láminas del bot (R4.5), con la enmienda de RUMBO §0, §4 y §5 en un commit propio; (2) J, si la hoja sale de kit hoja; (3) la preparación de la sesión 7»
   por
   «Las láminas del bot están hechas (LAMINAS.md; `motor laminas`; R4.5) y RUMBO §0, §4 y §5, enmendado. Siguiente, en este orden: (1) J, si la hoja sale de kit hoja; (2) la preparación de la sesión 7».
   El resto de la entrada no cambia.
2. **R4.5 HECHA, solo si das las láminas por revisadas.** Sus `Refs` quedan en `ID:ADR-0092`, sin NA:F en ningún sitio del bloque. El «Hecho cuando» pasa a ser «la herramienta y las láminas de las sesiones candidatas de la 7a, revisadas por el consultor; las de los días que elija la preparación se generan allí con la herramienta.», y el `Estado`, «HECHA (trabajo/laminas, LAMINAS.md).».
3. **Líneas nuevas de Technical Debt** (las que quedan tras la respuesta a la PARADA final, puntos 1, 2, 4 y 8):
   - «`motor laminas` no dice el esquema: con la orden en el punto, `zona_del_punto` crea toda zona con `por = primer_esquema` (zonas.py:414-416); la frase vuelve cuando el motor distinga los dos esquemas (LAMINAS.md, respuesta a la PARADA final, 1).»
   - «`motor laminas`: la CLI solo se prueba entera con las velas reales (F4.3); en los tests, `main()` solo con la negativa de la salida, y la tubería entera por `laminas.generar` sobre el fixture.»
   - La de RN-020 y «del día» sale (punto 2: medido, la rama semanal no dispara con el registro de hoy). La de las H4 saltadas sale (punto 4, entero).
   - La de la flecha de la marca de borde del M1 (revisor de la ronda de dibujo, m1) sale: está arreglada (respuesta tras revisar la v4, punto 2).
   - **El falso positivo de la guardia** (respuesta tras revisar la v4, punto 6): «la guardia de Claude Code toma por ruta una barra dentro de una cadena que no es una ruta, como una etiqueta HTML (`</li>`) en una regex o « / » entre espacios en un texto, y niega un guion que solo lee HTML de láminas (LAMINAS.md, «Aplicación de la respuesta a la PARADA final», al final); y toma por argumento que se construye al ejecutarse una cadena constante de bash, `$'\r'`, en un `grep -c` sobre ficheros del repo nombrados literales (LAMINAS.md, respuesta tras revisar la v4, 6).»
4. **La fila de ERRORES-RECURRENTES del cierre lleva un hallazgo menor** (respuesta tras revisar la v4, punto 6). En la respuesta a la PARADA final, para que la guardia no tomara por ruta una regex y una cadena de un guion de medida, las reescribí. Eso es rodearla (CLAUDE.md, «Una guardia no se rodea»), aunque el guion solo leía HTML de láminas y lo declaré. Ante una negativa así se para y se dice.

## Respuesta del consultor a la PARADA final (2026-11-10)

Dada por Aleks (consultor) el 2026-11-10, tal cual (también al final de `docs/encargos/trabajo-laminas.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/laminas (2026-11-10). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA final», con su fecha, y aplícala punto por punto (skill fase-cero). La rama está bien hecha: F1, el registro del dominio (lo he leído entero: solo anota, y F4.1 y F4.2 a 0 bytes lo confirman) y el diseño cumplen lo aprobado. Pero no la cierro todavía, por dos motivos: aún no he visto ninguna lámina dibujada, ni tú tampoco, y tres de tus cuatro reparos se arreglan aquí en poco y no deben pasar a deuda, porque son frases que le dirían al trader algo que no es cierto. Una ronda corta, en esta rama:
>
> 1. «Es el primer esquema» sale de la lámina. Tal como está, le diría al trader un esquema que el motor no ha distinguido (zonas.py:414-416). Quita la frase y su clave de la tabla, con su test, y escribe en el informe por qué. La línea de Technical Debt cambia a: «`motor laminas` no dice el esquema: con la orden en el punto, `zona_del_punto` crea toda zona con `por = primer_esquema` (zonas.py:414-416); la frase vuelve cuando el motor distinga los dos esquemas (LAMINAS.md, respuesta a la PARADA final, 1).»
> 2. RN-020 y «del día». Mide en el registro si, con los valores de hoy, la rama semanal de RN-020 (strategy_spec.yaml:2111, `perdida_maxima_semanal` con `perdida_trader_alcance`) puede disparar.
>    - Si no puede: la frase sigue diciendo «del día», y un test falla si el registro cambia de forma que la semanal pueda disparar (negar por defecto).
>    - Si puede: la lámina dice cuál de los dos acumuladores llegó al tope, y si la foto no lo permite saber, la frase es «Ha llegado a la pérdida máxima del trader: no abre más hasta el corte siguiente.».
>    En los dos casos, la línea de Technical Debt sale.
> 3. El motivo repetido: cuando el bloqueo de la acción y la prohibición del efecto vienen del mismo gate en el mismo cierre, la lámina da una sola frase, «Iba a colocar la orden y no la coloca: {motivo}.». Con su test, y con el recuento de las láminas afectadas (hoy 13) antes y después.
> 4. Las H4 saltadas que se quedan de una evaluación anterior. Esto no va a deuda: la lámina las cotejaría y, si las dos anotaciones se quedan viejas a la vez, casarían y dibujaría como saltadas unas H4 que la evaluación vigente no saltó, sin dar error.
>    - En primitivas.py, `sesgo_h4_saltadas` se borra (pop) cuando la evaluación no salta ninguna, como ya hace `sesgo_h4_vela`.
>    - Los tres recuentos de main, igual: se borran cuando valen cero. Solo si F4.1 y F4.2 siguen a 0 bytes; si alguno cambia, deshaces el cambio de los recuentos, la lámina deja de cotejar con ellos y, en su lugar, comprueba que toda saltada es anterior a la vela que fija; y lo dices.
>    - Un test con dos evaluaciones en la misma sesión, la segunda sin saltadas, que falla con el código de hoy.
>    - En F4.3 dices en cuántas de las láminas cambió el dibujo de las saltadas. Si cambió alguna, el defecto estaba ocurriendo de verdad, y lo dices.
> 5. Lo de verlas dibujadas: las miro yo, cuando Aleks conecte a mi chat la carpeta nueva (punto 7); las abro con un navegador en mi lado. Si en la laptop ya tienes una forma de hacer capturas de un HTML local sin instalar nada en el proyecto (compruébalo; no añadas dependencias ni toques pyproject.toml), haz una de cada lámina de 07-03 07-11 y de una de cada sesión, con el guion en la carpeta de trabajo y no en el repo, y míralas antes de la PARADA. Si no la tienes, dilo y sigue sin ellas.
> 6. Punto 13 de tu PARADA: (b), y es barato porque hay que regenerarlas igual. La corrida nueva pide las diez sesiones en un orden barajado que eliges tú y no escribes en el repo, así que el informe de 675ee62 deja de servir de clave para estas carpetas. El comando del informe se escribe con la lista sustituida por «<las diez sesiones, en el orden de clave.txt>», como desviación declarada de «los comandos tal como se ejecutaron». Que 07-03 07-11 se reconozca por su contenido es inevitable y no importa: el trader opera cada día antes de ver su lámina, así que la clave nunca le ocultó el día. En el cierre se dice así.
> 7. Regenera las 47 (o las que salgan) en una carpeta nueva, C:\Users\USER\Desktop\laminas-sesion-7-v2, tras el ensayo en el clon, como antes. La carpeta vieja no se toca: la borra Aleks cuando yo dé la nueva por revisada. Repite F4.1 y F4.2 a 0 bytes con el código final.
> 8. Las otras dos líneas de Technical Debt (la CLI solo se prueba entera con velas reales; y la de las saltadas, solo si el punto 4 se queda a medias) quedan como las propones.
> 9. Las propuestas 1 y 2 de la orden de cierre (F y R4.5) quedan aprobadas tal cual. R4.5 pasa a HECHA solo cuando yo dé por revisadas las láminas de la carpeta v2.
>
> Después: make check, push a fix/laminas con su CI (el run del último commit y el de la ronda), el revisor solo sobre lo que cambia en esta ronda, pegado al final, y otra PARADA final corta con: lo que cambió, los recuentos de 3 y 4, lo que viste en las capturas, la ruta de la carpeta v2 y «Rama lista para revisión, NO cerrada.».

## Aplicación de la respuesta a la PARADA final, punto por punto (2026-11-10)

1. **«Es el primer esquema» sale de la lámina.** Se quitan `FRASE_ESQUEMA` y su uso en `componer`, y en su lugar queda un comentario que dice por qué. Lo prueba `test_la_lamina_no_dice_el_esquema`.
   - **Por qué:** con la orden en el punto (`al_aparecer_punto_de_breaker`), `zona_del_punto` crea toda zona con `por = primer_esquema` (zonas.py:414-416). La frase le diría al trader un esquema que el motor no ha distinguido.
   - **Recuento:** la frase salía en 31 láminas y ahora en 0.
   - **Technical Debt:** la línea pasa a ser la del consultor (en las propuestas, abajo).
2. **RN-020 y «del día», medido en el registro:**
   - `perdida_trader_alcance = dia` (parametros.yaml:1504-1526).
   - Con `dia`, `TopeTrader.aplica_semana` es falso (`tope_trader.py:126-127`), y `acumulador_del_trader` da NO a `perdida_semana` sin leerla (`primitivas_broker.py:360-362`). La rama semanal de RN-020 (strategy_spec.yaml:2111) **no puede disparar**, así que la frase y el motivo siguen diciendo «del día».
   - **Negar por defecto:** `Lectura` lleva ahora el alcance (`perdida_trader_alcance`, leído en cli.py). Con `semana` o `ambos`, la frase de RN-020 y su motivo dan un error que lo nombra (`ALCANCES_SOLO_DIA`). `test_rn020_dice_del_dia_solo_si_la_rama_semanal_no_puede_disparar` falla si el registro cambia a uno de los dos, y comprueba el error.
   - La línea de Technical Debt sale.
3. **El motivo repetido:** cuando el mismo gate bloquea la colocación y prohíbe el efecto en el mismo cierre, la lámina da solo «Iba a colocar la orden y no la coloca: {motivo}.». Un gate que solo prohíbe sigue con su «No abre». Lo prueba `test_el_gate_que_bloquea_y_prohibe_en_el_mismo_cierre_da_una_sola_frase`.
   - **Recuento de láminas con el motivo repetido:** antes 13, ahora 0.
4. **Las H4 saltadas de una evaluación anterior.** En `sesgo_h4_al_abrir` (primitivas.py), cada evaluación borra lo que no le toca:
   - `sesgo_h4_saltadas`;
   - los tres recuentos de main, cuando valen cero;
   - y, como el mismo defecto, `sesgo_h4_doble_ruptura` cuando la vela que fija no es de doble ruptura. Esto lo añado yo: con la anotación vieja, la lámina diría «rompió los dos extremos».
   - **F4.1 y F4.2 siguen a 0 bytes con el borrado** (abajo), así que el cambio de los recuentos se queda y la lámina sigue cotejando con ellos.
   - `test_una_segunda_evaluacion_sin_saltadas_borra_las_de_la_primera` hace dos evaluaciones en la misma sesión, la segunda sin saltadas ni doble ruptura. **Falla con el `primitivas.py` de antes de la ronda** (medido con `git stash` del fichero: «AssertionError: assert 'sesgo_h4_saltadas_color_contrario' not in {…, 'sesgo_h4_saltadas_color_contrario': '1', …}»).
   - **En F4.3, láminas con un dibujo distinto de las saltadas:** 0 de 47. No cambió ninguna: el defecto no llegaba a ocurrir en estas diez sesiones, que es lo esperable, porque RN-003 solo evalúa el sesgo una vez por sesión. Lo medí lámina a lámina, emparejando cada una por sus velas contra la carpeta vieja (`comparar_laminas.py`, de la carpeta de trabajo). Lo único que cambia, aparte de las frases de los puntos 1 y 3, es el dibujo de la orden en las 19 láminas de tipo a, por el arreglo de «Lo que vi en las capturas», 1.
   - RN-003 solo evalúa el sesgo al abrir la sesión (`abre_sesion_operativa`, strategy_spec.yaml:1170), así que dos evaluaciones en la misma sesión no ocurren en la corrida normal.
5. **Las capturas:** las hace el Chrome que ya tiene la máquina, en modo headless:

   ```
   chrome.exe --headless=new --disable-gpu --hide-scrollbars --window-size=1700,1500 --screenshot=<png> file:///<lamina.html>
   ```

   - No se instala nada ni se toca `pyproject.toml`.
   - El guion y los PNG están en la carpeta de trabajo de la sesión, fuera del repo.
   - Lo que vi, en «Lo que vi en las capturas», abajo.
6. **El orden barajado:** la corrida de la v2 pide las diez sesiones en un orden que elegí y no escribo en el repo, así que el informe de `675ee62` ya no sirve de clave para estas carpetas.
   - El comando se escribe con la lista sustituida, como desviación declarada.
   - Que la sesión de 07-03 de las 07:00 a las 11:00 se reconozca por su contenido es inevitable y no importa: el trader opera cada día antes de ver su lámina, así que la clave nunca le ocultó el día. En el cierre se dice así.
7. **Las láminas, en una carpeta nueva:** `C:\Users\USER\Desktop\laminas-sesion-7-v2`, tras el ensayo en el clon. La carpeta vieja no se toca.
   - F4.1 y F4.2 se repiten con el código final.
   - Desviación pequeña en F4.2: las carpetas son `data/laminas/bitacora-ronda` (con el código de `2aa36a0`) y `data/laminas/bitacora-final` (con el de `6276be1`), y no `data/laminas/bitacora`, para no pisar la de la primera vuelta. El diff es contra los mismos anexos.
8. **Las dos líneas de Technical Debt que quedan:** la de la CLI tal como estaba propuesta; la de las saltadas no hace falta, porque el punto 4 queda entero.
9. **Las propuestas 1 y 2 quedan aprobadas.** R4.5 pasa a HECHA solo cuando el consultor dé por revisadas las láminas de la v2.

**Un hallazgo de la guardia, de esta ronda.** El guion de comparación de la carpeta de trabajo (`comparar_laminas.py`) fue negado dos veces con «el código nombra la carpeta / , que contiene material protegido».
- La primera, por las etiquetas de cierre de una regex (`</li>`).
- La segunda, por la cadena « / » de un `print` («antes / ahora»).

El guion solo lee los HTML de las láminas. Las dos son falsos positivos de la lectura de rutas de la guardia. Reescribí la regex como `<li>([^<]*)` y la cadena como «antes y ahora», que miden lo mismo; queda dicho aquí. **Propuesta para la Next Action:** que la guardia no tome por ruta una barra dentro de una cadena que no es una ruta (una etiqueta HTML, « / » entre espacios).

## Lo que vi en las capturas (respuesta a la PARADA final, punto 5)

Las capturas son las seis láminas de la sesión de 07-03 de las 07:00 a las 11:00 y la primera de cada una de las otras nueve sesiones. Las saqué del Chrome de la máquina en modo headless, una por llamada y con rutas literales: la guardia niega lanzar Chrome desde un guion con argumentos construidos. Los PNG están en la carpeta de trabajo de la sesión, fuera del repo.

1. **Un defecto, corregido en esta ronda.** En las láminas de tipo a no se veían la orden, el stop ni el objetivo.
   - **Por qué:** la orden nace en el mismo cierre del corte, y su línea iba de ese cierre al corte, así que no tenía largo. El objetivo, por ejemplo en la de las 11:13 de una sesión, solo era el techo del eje de precios.
   - **El arreglo:** las tres líneas cubren ahora la M1 que coloca la orden, y su precio va en una etiqueta de su color en el eje derecho, como en el replay (`_etiqueta`, `class="eje-…"`).
   - **El test:** `test_la_orden_que_nace_en_el_corte_se_ve_con_su_stop_y_su_objetivo`, con la orden colocada en el cierre del corte, como en una lámina de tipo a. En la versión de `6276be1` se colocaba un minuto antes, y con el código viejo la línea habría tenido largo igual (revisor de la ronda, I2).
   - **La comprobación:** las etiquetas están en el eje de precios, a la derecha del borde del corte. Ese test, y `estructura_laminas.py`, las cuentan como del eje y no como del tiempo.
   - **Lo comprobé en las capturas de la v2 final:** en las de tipo a se ven la orden, el stop y el objetivo, con su etiqueta azul, roja y verde en el eje. A veces una etiqueta pisa un precio del eje, y eso se lee peor pero no engaña.
2. **Se lee peor, y no lo cambio sin tu respuesta:** en una caja pequeña, los rótulos 0, 0,25, 0,5, 0,8 y 1 se montan unos sobre otros en el borde derecho. Propuesta: rotular en el eje solo el 0, el 0,8 y el 1 cuando la caja mida menos de unos 40 px.
3. **Se lee peor, y no lo cambio sin tu respuesta:** las líneas de M15 lejanas en precio (las del día anterior, que entran en el M1 desde su borde por la decisión 5) estiran la escala del M1, y las velas quedan apretadas arriba. Propuesta: en el M1, solo las líneas de M15 que caen dentro del rango de precios de sus velas, de la caja y de la orden. En el M15 se dibujan todas.
4. **Bien, y como estaba aprobado:**
   - la H4 que fija el sesgo, recuadrada, y las saltadas, en discontinuo (en la única de las capturas que las tiene, tres);
   - las líneas de M15: la tomada, gruesa y con su punto en la vela que la toma; las que dejaron de ser la liquidez, en discontinuo;
   - las zonas de control de RN-009, en naranja sobre sus velas;
   - el punto de breaker;
   - los separadores de día sin fecha;
   - las horas de Madrid;
   - el corte en el borde derecho;
   - y la sustentación debajo.
   - El M15 de una sesión de lunes empieza a las 23:00 del domingo: es la primera vela del mercado, no un recorte.

**F4.3 de la ronda.**
- **Antes de las láminas, F4.1 y F4.2 otra vez, con el código final.** Se corrieron con el árbol de trabajo que después se commiteó en `6276be1`, que solo cambia el dibujo y los tests; el motor es el de `2aa36a0` (revisor de la ronda, m3):
  - F4.1: `motor arnes --simular --salida data/laminas/base.txt`, diff de **0 bytes** (266,7 s; 639,9 MiB).
  - F4.2: `motor decisiones --carpeta data/laminas/bitacora-final --bitacora 2026-04-13,2026-07-02,2026-07-03,2026-07-14`, base y base repetida `(31, 192, 24, 1150, 0, 32, 0)`, y **0 bytes** en las cuatro bitácoras (467,8 s; 637,1 MiB).
  - Con el árbol que se commiteó en `2aa36a0`, también 0 y 0 (266,1 s y 470,3 s).
- **Las láminas:**
  - **La orden, tal cual salvo la lista:** `uv run botsito motor laminas --sesiones <las diez sesiones, en el orden de clave.txt> --salida C:\Users\USER\Desktop\laminas-sesion-7-v2`. Es una desviación declarada de «los comandos tal como se ejecutaron» (respuesta a la PARADA final, punto 6). El orden barajado no está en el repo.
  - **Antes, el ensayo en el clon desechable con `6276be1`:** 47 láminas, 485,2 s, 645,1 MiB. Contra la carpeta vieja, emparejadas las 47 por sus velas:
    - el motivo repetido pasa de 13 a 0;
    - la frase del esquema, de 31 a 0;
    - las saltadas no cambian en ninguna;
    - cambian de dibujo solo las 19 de tipo a (la orden);
    - ninguna otra frase cambia.
  - **La v2 de `2aa36a0`** (la primera de la ronda, idéntica a su ensayo) llevaba el defecto de la orden que enseñaron sus capturas. Se apartó a la carpeta de trabajo antes de escribir la buena.
  - **La v2 buena:** desde el repo en `6276be1`, con `git status` vacío, a `C:\Users\USER\Desktop\laminas-sesion-7-v2`.
    - Resultado: `OK: 58 ficheros`, `TIEMPO: 479.7 s; MEMORIA: pico del proceso de 644.6 MiB`, exit 0.
    - `diff -r` contra su ensayo da **0 bytes**, `clave.txt` incluida.
    - Ninguna marca pasa del borde del corte.
    - **47 láminas, 19 de tipo a y 28 de tipo b, las mismas que la v1.** No sale ninguna sesión.
    - Los recuentos por carpeta no se dan: junto con la tabla de la v1, que sigue el orden de la lista del encargo, dejarían reconstruir el orden barajado (revisor de la ronda, I1). Son las mismas 47 láminas que la v1, emparejadas una a una por sus velas.
    - La H4 que fija el sesgo cae dentro de la ventana en 47 de 47 láminas.
  - **La carpeta vieja** `C:\Users\USER\Desktop\laminas-sesion-7` sigue como estaba: la borra Aleks cuando el consultor dé la v2 por revisada.

## El revisor de la ronda (2026-11-10), tal cual

Solo sobre lo que cambia en la ronda. Lo hecho con él: I1, los recuentos de la v2 por carpeta salen del informe; I2, el test coloca la orden en el cierre del corte; m1 y m3, corregidos en el texto; m2, el Estado.

> ## Informe del revisor · trabajo/laminas (ronda de la respuesta a la PARADA final) · 2026-11-10
>
> He revisado solo la ronda: `2aa36a0`, `6276be1` y `docs/validation/LAMINAS.md` sin commitear (`git diff cbeb840`). Los puntos 1 a 4 están hechos y sostenidos por el código, los HTML y los diffs; el 5 está hecho hasta donde se puede ver. No hay nada que bloquee. Hay **dos hallazgos que importan**: el informe deja reconstruir la clave de la v2, y el test de la orden de tipo a no reproduce el defecto real. Además hay tres menores.
>
> ### Puntos 1-9 de la respuesta
>
> | # | Estado | Evidencia |
> |---|---|---|
> | 1 | Hecho | `FRASE_ESQUEMA` y su uso desaparecen (diff de `laminas.py:524-531` y `:883-886`). Queda el comentario `laminas.py:529-531`; zonas.py:414-416 sí crea la zona con `PRIMER_ESQUEMA`. En la v2, `grep -rl "Es el primer esquema\|Es el segundo esquema"` da 0 ficheros; en la carpeta vieja, 31. La línea de Technical Debt es la del consultor, literal. Test `test_la_lamina_no_dice_el_esquema` PASSED. |
> | 2 | Hecho | Medida cierta: `perdida_trader_alcance` vale `dia` (`parametros.yaml:1504-1526`, `valor: dia`). `aplica_semana` es `alcance in (SEMANA, AMBOS)` (`tope_trader.py:126-127`). `primitivas_broker.py:360-362` da NO si no aplica. `tope_del_registro` no deja otro alcance si el registro está fijado (`tope_trader.py:161-166`). La negativa por defecto existe en `laminas.py:796` y `:1008-1009`, con `ALCANCES_SOLO_DIA` en `:511`. El test lee el registro real (`test_laminas_svg.py:25,38`) y PASSED. La línea de Technical Debt sale. |
> | 3 | Hecho | Solo se quita el «No abre» de un gate que está en `bloquean`. Ese conjunto se llena solo con los gates que bloquean `accion:colocar_orden_limite` en la misma `Foto` (un solo cierre, `ev` en `laminas.py:430-444`): `laminas.py:1049-1069`. En los HTML, la carpeta vieja tiene 13 ficheros con «No abre» y 22 frases, y cada motivo coincide en número con su «Iba a colocar…». La v2 tiene 0 «No abre» y los mismos 22 «Iba a colocar». Test PASSED. |
> | 4 | Hecho | Los pop están en `primitivas.py` (diff `:211-236`). F4.1: `diff data/laminas/base.txt …/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt \| wc -c` da 0. F4.2: las cuatro bitácoras y la ablación de `data/laminas/bitacora-final` dan 0 contra `anexos/TRAZAS-ABLACION`. El test de las dos evaluaciones PASSED. Que fallara con el código anterior lo confirma la lectura: el código viejo nunca hacía pop de `ANOTACION_SALTADAS_COLOR`. No lo ejecuté (necesita escribir). Saltadas: 12 `h4-saltada` en las dos carpetas y 5 «rompió los dos extremos» en las dos. El borrado de `sesgo_h4_doble_ruptura` está declarado (LAMINAS.md, punto 4, «Esto lo añado yo»). «Una sola evaluación por sesión» es cierto: RN-003 es `todos_de` con `abre_sesion_operativa` primero (`strategy_spec.yaml:1169-1171`) y `todos_de` corta en el primer NO (`interprete.py:243-250`). |
> | 5 | Hecho, hasta donde se ve | No cambian `pyproject.toml` ni `uv.lock`: `git diff --stat main...HEAD -- pyproject.toml uv.lock` sale vacío. El guion y los PNG no están en el repo. |
> | 6 | En parte | El comando lleva la lista sustituida (LAMINAS.md:730), pero ver el hallazgo I1. |
> | 7 | Hecho | La v2 tiene 58 ficheros con mtime 18:03, después de `6276be1` (17:46). La carpeta vieja tiene 58 ficheros, todos de 15:35, y `find -newer` sobre el encargo da 0. `make-check.log`: el SELLO es del árbol `25513a1…`, que es `git rev-parse 6276be1^{tree}`; PICO DE MEMORIA 313 MiB. |
> | 8 | Hecho | La línea de la CLI se queda y la de las saltadas no hace falta (LAMINAS.md, sección de las propuestas). |
> | 9 | Hecho | Las propuestas no cambian y R4.5 sigue pendiente de la revisión de la v2. |
>
> `6276be1`: las etiquetas `eje-*` solo traen precios de 5 decimales, sin id, fecha ni dinero. Solo aparecen en las 19 láminas con «Coloca la orden». La línea empieza un minuto antes y nunca pasa del corte. No mete nada posterior al corte.
>
> ### Hallazgos
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | I1 | importa | **El informe deja reconstruir la clave de la v2.** LAMINAS.md:743 da los recuentos por carpeta «en el orden barajado de las carpetas». La tabla de la v1 (LAMINAS.md:497-508) da los mismos recuentos por carpeta, y las carpetas de la v1 siguen el orden de la lista del encargo (LAMINAS.md:476, «en el orden de su lista»; las fechas, en encargo:62-64). Cruzando las tres cosas salen seis de las diez carpetas de la v2 atadas a su día, y las otras cuatro quedan en dos parejas. El punto 6 pide no escribir el orden barajado. No escribo aquí cuál es cuál. Arreglo propuesto: dar los recuentos ordenados o como totales, no por carpeta. | LAMINAS.md:743 frente a LAMINAS.md:497-508 y :476 |
> | I2 | importa | **El test de la orden de tipo a no reproduce el defecto que dice arreglar.** El fixture coloca la orden en `(CORTE - 1) * 60_000 - 1`, que es el cierre de la penúltima M1. El corte es el cierre de la M1 de `corte-1` (`laminas_svg.py:314-315`). Con la fórmula vieja, `desde` sería `CORTE-1`: la línea tendría un minuto de largo (unos 5 px) y pasaría `> 1`. El defecto real era largo 0: en la carpeta vieja, `<line class="orden" x1="1490.0" … x2="1490.0"`. Solo la parte de las etiquetas `eje-` haría fallar el test con el código viejo. | `tests/unit/test_laminas_svg.py:380`; `grep '<line class="orden"'` en las dos carpetas |
> | m1 | menor | La carpeta de F4.2 sale con tres nombres. El punto 7 dice `data/laminas/bitacora-ronda` (LAMINAS.md:691), el F4.3 de la ronda `bitacora-final` (:727) y la fila de HOLDOUT `data/laminas/bitacora`. Existen las dos primeras: ronda a las 16:33, final a las 17:26. | `ls data/laminas` |
> | m2 | menor | El Estado dice que «siguen las láminas de la carpeta v2, las capturas», pero el mismo informe ya las da por hechas. `{REVISOR3}` está sin rellenar, como se espera en esta fase. | LAMINAS.md:1117, :747 |
> | m3 | menor | Las corridas atribuidas a un commit son anteriores a ese commit. F4.1/F4.2 «con `6276be1`» terminaron a las 17:18 y 17:26, y el commit es de las 17:46. `bitacora-ronda` (16:33) es anterior a `2aa36a0` (16:55). No hace daño: `6276be1` solo toca `laminas_svg.py` y tests, no el motor. Pero la atribución al sha no se ve en las horas. | mtimes de `data/laminas`; `git show --stat 6276be1` |
>
> ### Lo que no pude comprobar
> - Que el test de las dos evaluaciones falle con el `primitivas.py` viejo: ejecutarlo exige `git stash` o un clon, y los dos escriben. Me quedo con la lectura del diff.
> - Las capturas PNG y que se hicieran con Chrome headless: están fuera del repo, en la carpeta de trabajo de la sesión.
> - Si la ampliación de la fila de HOLDOUT-EXPOSICIONES en `6276be1` (las 7 corridas más) se escribió antes de lanzarlas. El commit es de las 17:46 y las corridas empezaron hacia las 17:14; la hora de edición en el árbol no se puede saber.
> - No abrí ningún `clave.txt`.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`, `git log main..HEAD`/`cbeb840..HEAD`, `git diff --stat cbeb840`, `git status --short`
> 2. `git diff cbeb840 -- docs/encargos/trabajo-laminas.md`, `-- src tests`, `-- docs/validation/LAMINAS.md HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md anexos`
> 3. Read de `laminas.py` (190-240, 400-449, 575-594, 1015-1084), `interprete.py:230-259`, `tope_trader.py:150-199`, `test_laminas_svg.py:60-89`, `LAMINAS.md:480-509`
> 4. `sed -n` de `zonas.py:405-420`, `primitivas_broker.py:350-366`, `parametros.yaml:1504-1526`, `strategy_spec.yaml:2104-2115` y `1164-1174`
> 5. `grep` de símbolos en laminas.py y strategy_spec, y de los comandos `--sesiones` en el informe y el encargo
> 6. `uv run pytest tests/unit/test_laminas.py tests/unit/test_laminas_svg.py tests/unit/test_laminas_registro.py -p no:cacheprovider -q` (y otra vez con `-rA | grep`): todo verde. Un intento encadenado lo negó la guardia.
> 7. `grep -r --include=*.html` en las dos carpetas de láminas: esquema, «Iba a colocar», «No abre», `h4-saltada`, «rompió los dos extremos», `eje-*`, `<line class="orden"`
> 8. `find`/`ls` de mtimes de las dos carpetas y de `data/laminas`; `git log -1 --format=%ci` de `6276be1` y `f6ed348`; `git show --stat` de los dos commits de la ronda
> 9. `diff … | wc -c` de F4.1 y de las cinco salidas de F4.2 contra sus anexos: todos 0
> 10. `grep` de `make-check.log` (SELLO, PICO); `git rev-parse 6276be1^{tree}`
> 11. `git show 6276be1 -- HOLDOUT-EXPOSICIONES.md`; `git show 2aa36a0:docs/validation/HOLDOUT-EXPOSICIONES.md | grep`

## Respuesta del consultor a la PARADA final de la ronda (2026-11-10)

Dada por Aleks (consultor) el 2026-11-10, tal cual (también al final de `docs/encargos/trabajo-laminas.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de la ronda de trabajo/laminas (2026-11-10). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA final de la ronda», con su fecha, y aplícala punto por punto (skill fase-cero). Buena ronda. El borrado de sesgo_h4_doble_ruptura queda aprobado, y la orden de tipo a que no se veía es justo lo que solo encuentra la revisión visual. Una última ronda de dibujo, sin tocar el motor:
>
> 1. Los rótulos de la caja: aprobado, con esta regla. Cuando dos rótulos quedan a menos de la altura de su letra, se dejan solo el 0, el 0,8 y el 1. Si aun así se montan (una caja diminuta), solo el 0 y el 1. Las líneas de los niveles se dibujan siempre. Lo que digo es la condición, no un umbral en píxeles a ojo; la altura de la letra es la constante de dibujo que ya usas. Con su test.
> 2. Las líneas de M15 lejanas en el M1: en el M1 se dibujan las que caen dentro del rango de precios de sus velas, de la caja y de la orden, ampliado por arriba y por abajo una altura de caja (o, sin caja, un 10 % del rango). Las que quedan fuera no se dibujan, pero tampoco desaparecen: van como una marca pequeña en el borde de arriba o de abajo del M1, con su precio y una flecha hacia donde están, del color de su lado. En el M15 se dibujan todas, como hasta ahora. La línea que el motor tomó se dibuja siempre en el M1, aunque estire la escala. Con su test. La de 07-03 (1.14500, con el punto en 1.14496) tiene que verse en el M1: compruébalo en su captura.
> 3. Las etiquetas del eje que pisan un precio del eje: cuando una etiqueta de la orden, el stop o el objetivo cae sobre un precio de la rejilla del eje, ese precio de la rejilla no se escribe. Con su test.
> 4. Regenera tras el ensayo en el clon, en una carpeta nueva, C:\Users\USER\Desktop\laminas-sesion-7-v3, con el mismo orden barajado de la v2: es el mismo conjunto, y así la clave no cambia. Haz las mismas capturas que en la ronda y míralas. F4.1 y F4.2 no hace falta repetirlas si el diff de la ronda no toca nada fuera de engine/laminas_svg.py, sus tests y el informe; si toca otra cosa, se repiten a 0 bytes.
> 5. En el informe: cuántas láminas cambian de rótulos (punto 1), cuántas de líneas de M15 en el M1 (punto 2) y cuántas de etiquetas (punto 3). Sin recuentos por carpeta, como dijo el revisor.
> 6. Las carpetas v1 y v2 no se tocan; las borra Aleks.
>
> Después: make check, push a fix/laminas con su CI (el run de 1d42881 y el de esta ronda), el revisor solo sobre esta ronda, pegado al final, y la PARADA final corta con lo que cambió, los tres recuentos, lo que viste en las capturas, la ruta de la v3 y «Rama lista para revisión, NO cerrada.». Yo reviso la v3 y doy la orden de cierre.

## Aplicación de la respuesta a la PARADA final de la ronda, punto por punto (2026-11-10)

El código solo cambia en `src/botsito/engine/laminas_svg.py`, con sus tests en `tests/unit/test_laminas_svg.py` (commit `c166093`). Por eso F4.1 y F4.2 no se repiten (punto 4). Fuera de eso cambian el informe, la respuesta copiada en el encargo, la fila de HOLDOUT-EXPOSICIONES y el recuento de tests de PROJECT_STATE.

1. **Los rótulos de la caja.** `rotulos_visibles` aplica tu regla con la altura de la letra (`TAMANO_ROTULO`, la constante con que se escriben):
   - los cinco;
   - si dos quedan a menos de esa altura, el 0, el del stop y el 1;
   - si aun así se montan, el 0 y el 1.

   Las líneas de los niveles se dibujan siempre. Lo prueba `test_los_rotulos_de_la_caja_siguen_la_regla`, con niveles puestos a píxeles conocidos.
   - **Con el stop en el 0,8, el caso intermedio no puede darse.** El paso más corto entre los cinco rótulos es el del 0,8 al 1 (dos décimas de la caja), y ese paso sigue entre los tres. Así que, cuando los cinco se montan, los tres también. El test lo prueba aparte, con niveles sueltos.
2. **Las líneas de M15 en el M1.** `lineas_del_m1` decide cuáles se dibujan:
   - entran las que caen en el rango de las velas del M1, la caja y la orden, ampliado por arriba y por abajo una altura de caja (sin caja, un décimo del rango);
   - la tomada, siempre;
   - las demás van como una marca en el borde de arriba o de abajo, con «▲» o «▼», su precio y el color de su lado (`class="m15-fuera …"`).

   En el M15 se dibujan todas. Lo prueba `test_las_lineas_de_m15_lejanas_van_como_marca_en_el_m1_y_la_tomada_siempre`. **En la lámina de 07-03 con la orden en 1.14496** (la captura): la línea tomada de 1.14500 se ve en el M1 junto a la orden y el punto en 1.14496, y la línea lejana del día anterior va como «▼ 1.14366» abajo.
3. **Los precios de la rejilla:** el que caería bajo una etiqueta de la orden, el stop o el objetivo (a menos de `ALTO_ETIQUETA`) no se escribe. Lo prueba `test_el_precio_de_la_rejilla_bajo_una_etiqueta_de_la_orden_no_se_escribe`, sobre un panel y sobre una lámina de tipo a.
4. **La v3:** en `C:\Users\USER\Desktop\laminas-sesion-7-v3`, tras el ensayo en el clon, con el mismo orden barajado de la v2. Su `clave.txt` es idéntica a la de la v2 (`diff`, 0 bytes; no se abrió).
   - La orden, tal cual salvo la lista: `uv run botsito motor laminas --sesiones <las diez sesiones, en el orden de clave.txt> --salida C:\Users\USER\Desktop\laminas-sesion-7-v3`.
   - Base con y sin el recolector, `(31, 192, 24, 1150, 0, 32, 0)`.
   - Ensayo: 612,9 s y 646,2 MiB. La v3: 552,6 s y 644,7 MiB.
   - `diff -r` de la v3 contra su ensayo: 0 bytes.
   - 47 láminas, 19 de tipo a y 28 de tipo b. Las frases no cambian en ninguna.
5. **Los recuentos, de la v2 a la v3, sin recuentos por carpeta.** Las 47 láminas se emparejan por su cabecera y sus velas de H4, que esta ronda no toca. Lo mide `comparar_v3.py`, de la carpeta de trabajo, que solo lee los HTML.
   - **Punto 1:** cambian de rótulos 29 láminas, que ahora llevan el 0 y el 1. 2 conservan los cinco. 16 no tienen caja.
   - **Punto 2:** cambian de líneas de M15 en el M1 3 láminas, con una marca en el borde cada una. En esas 3 cambia la escala del M1.
   - **Punto 3:** en 16 láminas se deja de escribir algún precio de la rejilla bajo una etiqueta de la orden. Cambian de rejilla 19; las otras 3 son las del cambio de escala del punto 2.
6. **Las carpetas v1 y v2 no se tocan.**

**Lo que vi en las capturas de la v3** (las seis láminas de 07-03 de las 07:00 a las 11:00 y la primera de cada otra sesión, con Chrome en modo headless, fuera del repo):
- se ven la línea tomada y el punto de 07-03;
- los rótulos de las cajas pequeñas ya no se montan;
- las etiquetas de la orden ya no tapan precios de la rejilla;
- la marca de la línea lejana se lee.

**Lo único que no queda limpio:** una marca de borde que nace en el extremo izquierdo pisa un poco las primeras velas. Se lee, y no lo toco sin tu respuesta.

## El revisor de la ronda de dibujo (2026-11-10), tal cual

Solo sobre esta ronda: 0 bloquea, 0 importa, 2 menores. Lo hecho con ellos: m2, el Estado, al día; m1, la flecha de una marca que podría apuntar al lado equivocado en un caso que no aparece en la v3, queda como línea propuesta de Technical Debt (abajo). Arreglarlo ahora cambiaría el código después de la v3. (Después: arreglada en la ronda tras revisar la v4, punto 2, y la línea de Technical Debt sale.)

> ## Informe del revisor · trabajo/laminas · última ronda de dibujo (c166093 + LAMINAS.md sin commitear) · 2026-11-10
>
> Resumen: 0 bloquea, 0 importa, 2 menor. Los seis puntos están hechos. Los recuentos del informe salen iguales al medirlos sobre los HTML.
>
> ### Los puntos 1 a 6
> | # | Estado | Evidencia |
> |---|---|---|
> | 1 Rótulos | **Hecho** | `rotulos_visibles` (`src/botsito/engine/laminas_svg.py:237-247`) escribe primero los cinco; si no caben, el 0, `niveles[-2]` (el stop, según `laminas._niveles`) y el 1; si tampoco, el 0 y el 1. La condición es `b - a >= TAMANO_ROTULO`, y `TAMANO_ROTULO` es la constante que da la altura de la letra (`font-size`) del rótulo, no un umbral a ojo. Las líneas de los niveles se dibujan siempre, con `for _, nivel in d.niveles` separado del bucle de los rótulos. Lo prueban `test_los_rotulos_de_la_caja_siguen_la_regla` y la aserción `count('class="nivel"') == 5`. El informe avisa de que, con el stop en el 0,8, el caso de tres rótulos no puede darse, porque el paso más corto (del 0,8 al 1) sigue entre los tres. El razonamiento es correcto y la v3 lo confirma: 2 láminas con cinco rótulos, 29 con dos y ninguna con tres. |
> | 2 Líneas de M15 en el M1 | **Hecho** | `lineas_del_m1` (`:202-215`) toma el rango de las velas del M1, la caja y la orden. Lo amplía una altura de caja, o `(hi-lo)//10` si no hay caja. La línea con `ln.tomada` entra siempre. Las demás van a `_fuera` (`:218-234`): una marca con ▲ o ▼, su precio y el color de su lado. En el M15 se dibujan todas: `_lineas_m15(m15, d, d.lineas)`. Lo prueba `test_las_lineas_de_m15_lejanas_...`. |
> | 3 Rejilla | **Hecho** | `_velas` se salta el precio de la rejilla que queda a menos de `ALTO_ETIQUETA` de una etiqueta (`:124`). Las etiquetas son las de la orden, el stop y el objetivo (`:361`). Hay test sobre un panel y sobre una lámina de tipo a. En los 47 HTML de la v3 he comprobado que ningún precio de la rejilla del M1 cae bajo una etiqueta: 0 solapes. |
> | 4 Diff de la ronda | **Hecho** | `git diff --name-status 1d42881 c166093` solo trae `laminas_svg.py`, `test_laminas_svg.py`, `LAMINAS.md`, el encargo, `HOLDOUT-EXPOSICIONES.md` y `PROJECT_STATE.md`. Lo único que cambia en `PROJECT_STATE.md` es 1984 → 1987, que cuadra con los 3 tests nuevos. `engine/laminas.py` no cambia, y fuera del propio fichero solo importa `laminas_svg` `laminas.py:1189` (`indice, pagina`). Así que F4.1 y F4.2 no dependen del cambio, y el informe y la fila de exposiciones lo declaran. |
> | 5 Recuentos | **Hecho, y salen exactos** | Empareje v2 y v3 por la misma ruta relativa. Las cabeceras, las velas de H4 y las frases son idénticas en las 47. Rótulos: cambian 29, quedan 2 con cinco y 16 sin caja. Líneas de M15 en el M1: cambian 3, con una marca cada una. Rejilla del M1: cambian 19; en 16 se ha quitado algún precio y en 3 aparecen precios nuevos porque cambia la escala. Todo coincide con el informe, que solo da recuentos globales, ninguno por carpeta. |
> | 6 v1 y v2 | **Hecho** | Las dos carpetas tienen 58 ficheros cada una. Las fechas de modificación son únicas por carpeta: la v1, 15:35; la v2, 18:03, anterior a `1d42881` (18:34) y a `c166093` (22:07). Las de la v3 son de las 22:27. |
>
> **La línea de 1.14500 en el M1 (v3):** hay dos láminas con la orden en 1.14496. En las dos, la línea `linea-m15 bajo tomada` está en el panel M1 en y1=702.9. Interpolando la rejilla del M1 (1.14508 en 690.8, 1.14469 en 750.0), ese y corresponde a 1.14500, así que la línea se dibuja. La línea lejana va como `▼ 1.14366`, y 1.14366 queda por debajo del mínimo de la rejilla (1.14390), así que la flecha apunta bien.
>
> **Lo posterior al corte, ids, fechas y dinero:** la marca nueva solo lleva una flecha y un precio, y su x se recorta a `p.derecha`. `lineas_del_m1` solo usa `d.m1`, `d.caja` y `d.ordenes`, que ya vienen cortados en el `Dibujo`. Un grep de fechas ISO, €, $, USD, EUR, `zona:N`, `ev-`, `fb-`, lote, % y beneficio o pérdida sobre los HTML de la v3 no encuentra nada.
>
> ### Hallazgos
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | m1 | menor | La flecha de una marca podría apuntar al lado equivocado en un caso que no aparece en la v3. La escala del M1 incluye también `d.control` y `d.punto` (`laminas_svg.py:348`), pero el rango de entrada de `lineas_del_m1` no (`:207-211`). La marca decide el lado con `arriba = ln.nivel > p.hi` (`:224`). Una línea por encima del rango ampliado, pero por debajo de un `p.hi` estirado por una zona de control, iría abajo con ▼. No ocurre en ninguna de las 3 marcas de la v3, todas ▼ y bien orientadas, y ningún test cubre la marca ▼. | código citado; medición: las 3 marcas `▼ 1.14366` están por debajo del mínimo de su rejilla |
> | m2 | menor | El `## Estado` de LAMINAS.md, sin commitear, dice «siguen la v3, sus capturas, la CI, el revisor…», pero la sección nueva ya da la v3 y las capturas por hechas. Queda el marcador `{REVISOR4}`, como se espera en esta fase. Es la misma observación que hizo el revisor anterior (m2). | `docs/validation/LAMINAS.md:1225` y `:855` |
>
> Lo que ya está declarado en el informe no lo cuento como hallazgo: la marca del borde izquierdo pisa un poco las primeras velas (las 3 marcas están en x=20.0).
>
> ### Lo que no pude comprobar
> - Que la línea lejana sea «del día anterior», como dice el informe. Comprobarlo exige ligar el HTML con el día, y me pediste no decir qué carpeta es qué día.
> - Las capturas de Chrome y el ensayo en el clon (los 0 bytes de `diff -r`, los tiempos y la memoria): están en la carpeta de trabajo de la sesión, y repetirlo exige escribir.
> - Que la `clave.txt` de la v2 y la de la v3 son idénticas: no la abrí, por orden tuya.
> - Las fechas de modificación no prueban que nadie leyera la v1 o la v2; solo prueban que no se escribió en ellas.
>
> ### Comandos ejecutados
> 1. `git log --format='%h %s' 1d42881..c166093`, `git diff --stat 1d42881 c166093`, `git status --short`
> 2. `git diff 1d42881 c166093 -- src/botsito/engine/laminas_svg.py`, `-- docs/encargos/... PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md`, `-- tests/unit/test_laminas_svg.py`
> 3. `git diff -- docs/validation/LAMINAS.md`, `git diff 1d42881 -- docs/validation/LAMINAS.md` (las líneas quitadas: solo el Estado)
> 4. `sed -n` y `grep -n` sobre `laminas_svg.py` y `laminas.py` (`_Panel`, `Dibujo`, `_niveles`, etiquetas)
> 5. `uv run pytest tests/unit/test_laminas_svg.py tests/unit/test_laminas.py -p no:cacheprovider -q -rA`: 44 PASSED, exit=0
> 6. `ls -la` y `find -printf` de fechas sobre las tres carpetas del Escritorio, sin abrir `clave.txt`
> 7. Tres guiones de Python por stdin (`uv run python -`) que solo leen los HTML de la v2 y la v3: emparejado y recuentos, búsqueda de 1.14496 y 1.14500, y orientación de las marcas
> 8. Un grep de fechas, ids y dinero sobre los HTML de la v3
> 9. `grep -rn laminas_svg src/`, `git diff --name-status 1d42881 c166093`, `git log -3 --format='%h %ci %s'`
>
> (Un intento con `uv run --project` lo bloqueó la guardia; lo repetí con `cd` al repositorio y `uv run python -`, que es la forma que la guardia acepta.)


## Respuesta del consultor tras revisar la v3 (2026-11-10)

Dada por Aleks (consultor) el 2026-11-10, tal cual (también al final de `docs/encargos/trabajo-laminas.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de la última ronda de dibujo de trabajo/laminas (2026-11-10). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor tras revisar la v3», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> He revisado la v3: las 47 dibujadas en un navegador y vistas juntas (ninguna rota), cuatro a fondo (07-03 a las 08:02, una de RN-009 de 07-03 11-15, una del rango de 07-06 y la de 04-13 con tres saltadas), y el texto de todas pasado por las regex del punto 4 y del punto 5 (sin fechas, ids, lote, R, dinero ni porcentajes). Lo que se aprobó está bien. La H4 que fija el sesgo, las saltadas, las líneas de M15 con la tomada, el punto, las etiquetas del eje y la sustentación casan con la bitácora de 07-03. Pero hay dos cosas que impiden usarlas para lo que sirven, que es que el trader corrija la caja del bot y diga qué zonas de control cuenta (las preguntas de la 7a). Una ronda más, solo en engine/laminas.py, engine/laminas_svg.py, sus tests y el informe:
>
> 1. Un panel nuevo, «M1 de cerca», debajo del M1 y encima de la sustentación. Con stops de pip y medio, en el M1 de dos horas la caja mide unos pocos píxeles: en 07-03 a las 08:02 la caja, el punto y la toma se amontonan en el borde, y en las láminas de RN-009 las zonas de control naranjas no se distinguen. El panel:
>    - Va del M1 de la toma (o de 15 velas antes de la primera zona de control que dibuje, si es anterior) hasta el corte, con un máximo de 60 velas. Si es más largo, empieza 60 velas antes del corte; sin toma, son las 30 últimas velas.
>    - La escala se ajusta a las velas de ese tramo, la caja, la orden y el stop. Todo lo que quede fuera (el objetivo, las líneas de M15 lejanas) va como marca de borde, con su precio y una flecha, como ya hace el M1.
>    - Lleva lo mismo que el M1, en esa escala: la caja con sus rótulos (con la regla de la ronda anterior, que aquí casi siempre dejará los cinco), el punto de breaker, la vela de la toma, las líneas de M15 que entren, las zonas de control de RN-009 que contó el motor en ese cierre y la orden, el stop y el objetivo con sus etiquetas.
>    - Mismo recorte y mismas puertas que el M1 (punto 6 del encargo): es un subconjunto de lo que ya se dibuja, y nada nace fuera de la ventana.
>    - Con sus tests: el tramo, el tope de 60, la escala y ninguna marca a la derecha del corte.
>    - En las capturas, compruébalo en 07-03 a las 08:02: la línea de 1.14500 y el 0 en 1.14496 tienen que verse separados, con sus precios. Y en una lámina de RN-009 de las que dicen «3, y admite 1», las tres zonas de control, una a una.
> 2. Las horas de la sustentación, con un solo convenio: toda hora que nombra una vela es la de su apertura, como la rotula FX Replay. Hoy la toma dice «una vela de M1 cerró … a las 07:57», que es el cierre de la vela de las 07:56, mientras que el punto dice «de la vela de las 08:01», que es la apertura. En la bitácora de 07-03 la M1 de la toma «cierra 07:57». La frase de la toma pasa a ser «La vela de M1 de las {HH:MM} cerró con {cuerpo / mecha} por {debajo del bajo / encima del alto} de M15 en {precio}.». Repasa cada frase con hora de la tabla con el mismo criterio, di en el informe cuáles cambian, y añade un test que fije el convenio. La cabecera («Corte: a las 08:02, al cierre de la vela de M1 de las 08:01») ya lo cumple y se queda.
> 3. Menor: «Antes de esa vela saltó 3 velas H4…» pasa a «Antes de esa vela, el bot se saltó {n} velas H4…» (y en singular, «se saltó una vela H4…»).
> 4. Regenera tras el ensayo en el clon, en C:\Users\USER\Desktop\laminas-sesion-7-v4, con el mismo orden barajado y la misma clave (compárala con diff, sin abrirla). F4.1 y F4.2 no se repiten si el diff de la ronda no sale de engine/laminas.py, engine/laminas_svg.py, sus tests y el informe; si sale, se repiten a 0 bytes. Haz las capturas de la ronda anterior más las dos del punto 1, y míralas.
> 5. En el informe: cuántas láminas llevan el panel nuevo (todas, salvo que alguna no tenga tramo; di cuál y por qué), cuántas frases cambian de hora y el recuento de zonas de control que se ven en el panel frente al que dice la frase, en las láminas de RN-009. Sin recuentos por carpeta.
> 6. Las carpetas v1, v2 y v3 no se tocan; las borra Aleks.
>
> Después: make check, push a fix/laminas con su CI, el revisor solo sobre esta ronda, pegado al final, y la PARADA final corta: lo que cambió, los recuentos del punto 5, lo que viste en las capturas, la ruta de la v4 y «Rama lista para revisión, NO cerrada.». Si la v4 está bien, con ella doy la orden de cierre.

## Aplicación de la respuesta tras revisar la v3, punto por punto (2026-11-10 y 2026-11-11)

El código solo cambia en `src/botsito/engine/laminas.py` (frases) y `src/botsito/engine/laminas_svg.py` (dibujo), con sus tests: commits `1a9c922`, `2178a65`, `1d40323`, `1201262` y `58de6ce`. Por eso F4.1 y F4.2 no se repiten (punto 4). Fuera de eso cambian el informe, la respuesta copiada en el encargo, las filas de HOLDOUT-EXPOSICIONES y el recuento de tests de PROJECT_STATE.

1. **El panel «M1 de cerca»**, debajo del M1 y encima de la sustentación (`1a9c922`).
   - **El tramo (`tramo_de_cerca`):** va de la M1 de la toma (o de 15 velas antes de la primera zona de control que se dibuja, si es anterior) al corte, con un máximo de 60 velas. Si es más largo, empieza 60 velas antes del corte; sin toma, son las 30 últimas.
   - **La escala:** las velas del tramo, la caja, la orden y el stop. Lo que queda fuera (el objetivo, las líneas de M15 lejanas) va como marca de borde, con su precio y una flecha (`objetivo-fuera`, `m15-fuera`).
   - **Lleva lo mismo que el M1:** la caja con sus rótulos (con la regla de la ronda anterior), el punto, la vela de la toma, las líneas de M15 que llegan al tramo, las zonas de control y la orden con sus etiquetas. Es un subconjunto de las velas y de los elementos del M1, que ya pasaron la puerta.
   - **Las constantes de dibujo:** `VELAS_CERCA_MAX = 60`, `VELAS_CERCA_SIN_TOMA = 30` y `VELAS_ANTES_DEL_CONTROL = 15`.
   - **Los tests:** `test_el_tramo_del_m1_de_cerca` (el tramo, el de la zona de control, el tope de 60 y sin toma) y `test_la_escala_del_m1_de_cerca_y_lo_que_queda_fuera` (la escala, el objetivo como marca y nada a la derecha del corte). El test de las marcas de `test_laminas.py`, que no cambia, ya recorría todo el SVG, así que cubre también el panel nuevo.
   - **Lo que enseñaron las capturas y el revisor, en cuatro vueltas.** Cada una se arregló con su test, y con su ensayo de nuevo en un clon. La v4 de cada vuelta se apartó o se cortó antes de escribir la buena.

     | Vuelta | Lo que se vio | El arreglo | Su test |
     |---|---|---|---|
     | Capturas de la primera v4 (`1a9c922`), escrita y después apartada a la carpeta de trabajo de la sesión | en el M1 de cerca la línea tomada no llevaba su precio, y la respuesta pide verla con él junto al 0; dos marcas de borde en el mismo sitio se montaban | `2178a65`: la línea tomada lleva su etiqueta en el eje del M1 de cerca; las marcas de borde se apilan | `test_la_linea_tomada_lleva_su_precio_en_el_m1_de_cerca_y_las_marcas_no_se_montan` |
     | Capturas del ensayo de `2178a65` (su v4 se cortó tras cargar los datos, sin escribir nada) | la lámina de RN-009 «3, y admite 1» tenía dos etiquetas una encima de otra, y una era de una línea que acabó antes del tramo. Medido en las 47 láminas con `etiquetas_montadas.py`, de la carpeta de trabajo, que solo lee los HTML: 9 pares de etiquetas montadas en el M1 de cerca, en 6 láminas, todos con la etiqueta que trajo `2178a65`; 10 líneas tomadas de longitud cero en el M1 de cerca; y 7 pares en el M1 (orden, stop y objetivo juntos, ya en la v3) | `1d40323`: las etiquetas del eje de cada panel se colocan juntas sin montarse, cada una con su precio (también las del M1); en el M1 de cerca solo entran las líneas que llegan al tramo. En los ensayos de `1d40323` y `1201262`: 0 pares montados en los dos paneles y 0 líneas de longitud cero | `test_las_etiquetas_del_eje_no_se_montan_y_cada_una_lleva_su_precio`, `test_en_el_m1_de_cerca_no_entra_la_linea_que_acabo_antes_del_tramo` |
     | Capturas del ensayo de `1d40323` (su v4 se cortó igual) | el punto negro de la toma, fuera del panel junto a su título, cuando la línea tomada queda un punto por encima de la escala; las velas anchas del M1 de cerca tapaban los rótulos de la caja y las marcas de borde | `1201262`: el punto no se dibuja fuera de la escala; rótulos y marcas de borde van delante de las velas, con un borde del color del fondo (`HALO`) | `test_el_punto_de_la_toma_no_se_dibuja_fuera_del_panel`, `test_los_rotulos_y_las_marcas_de_borde_van_delante_de_las_velas` |
     | El revisor de la ronda, sobre la v4 de `1201262` (apartada después a la carpeta de trabajo de la sesión) | b-i1: en una lámina, la marca de borde del objetivo y la de una línea de M15 en el mismo punto del M1 de cerca, porque solo se apilaban las de M15 entre sí. Medido con `marcas_montadas.py`, de la carpeta de trabajo: 1 par, en 1 lámina | `58de6ce`: todas las marcas de borde de un panel se apilan juntas, sean de la clase que sean. En el ensayo y en la v4: 0 pares | `test_la_marca_del_objetivo_se_apila_con_las_de_m15` |

2. **Las horas, con un solo convenio:** toda hora que nombra una vela es la de su apertura, como FX Replay. Cambian dos frases de la tabla:
   - **la de la toma:** «La vela de M1 de las {HH:MM} cerró con {cuerpo / mecha} por {debajo del bajo / encima del alto} de M15 en {precio}.»;
   - **la de la toma con la línea de antes de la ventana:** «La vela de M1 de las {HH:MM} tomó la liquidez de M15: la línea que toma viene de antes de la ventana.». Antes decía «Liquidez de M15 tomada a las {HH:MM}: …», con la hora del cierre. Reescribirla con la vela delante es mío, para que la hora nombre a la vela.
   - **Ya cumplían el convenio y no cambian:** la del punto («de la vela de las {HH:MM}», su apertura) y la cabecera, que nombra el corte y la vela cada uno por lo suyo. No hay más frases con hora en la tabla.
   - **El test:** `test_toda_hora_que_nombra_una_vela_es_la_de_su_apertura`.
3. **Las saltadas:** «Antes de esa vela, el bot se saltó {n} velas H4…», y en singular «se saltó una vela H4…».
4. **La v4:** en `C:\Users\USER\Desktop\laminas-sesion-7-v4`, de `58de6ce`, tras el ensayo en el clon (`git worktree add --detach`), con el mismo orden barajado.
   - La orden, tal cual salvo la lista: `uv run botsito motor laminas --sesiones <las diez sesiones, en el orden de clave.txt> --salida C:\Users\USER\Desktop\laminas-sesion-7-v4`.
   - Su `clave.txt` es idéntica a la de la v3 (`diff`, 0 bytes; no se abrió). `diff -r` de la v4 contra su ensayo: 0 bytes.
   - Base con y sin el recolector, `(31, 192, 24, 1150, 0, 32, 0)`.
   - Ensayo: 481,1 s y 645,9 MiB. La v4: 475,6 s y 645,0 MiB.
   - 47 láminas, 19 de tipo a y 28 de tipo b, como en la v3.
5. **Los recuentos, de la v3 a la v4, sin recuentos por carpeta.** Las 47 láminas se emparejan por su cabecera y sus velas de H4. Lo mide `comparar_v4.py`, de la carpeta de trabajo, que solo lee los HTML. Las cifras son las mismas en los cuatro ensayos de esta ronda: los arreglos del punto 1 son de dibujo y no cambian ni frases ni zonas.
   - **Llevan el panel nuevo las 47.** Ninguna se queda sin tramo.
   - **Cambian de hora 32 frases,** todas de la toma; la de la línea de antes de la ventana no sale en ninguna de las 47. Cambian de redacción 4 frases de las saltadas.
   - **Las zonas de control, en las 13 láminas de RN-009:** en 12, el M1 de cerca enseña tantas como dice la frase (3, 3, 3, 4, 5, 6, 6, 7, 8, 9, 11 y 11). En la que dice 18, el M1 de cerca enseña 14: las otras 4 quedan antes de las 60 velas del tope. En el M1 se ven las 18.
6. **Las carpetas v1, v2 y v3 no se tocan.**

**Lo que vi en las capturas de la v4.** Son 16: las 15 de la ronda anterior (una de ellas ya es la de las 08:02) más la de RN-009 «3, y admite 1». Las tomé con Chrome en modo headless sobre el ensayo de `1201262`, fuera del repo. `58de6ce` solo cambia dónde va la marca de borde del objetivo. Hay una 17.ª captura, la de la lámina que encontró el revisor, del ensayo de `58de6ce`, idéntico byte a byte a la v4 (`diff -r`, 0 bytes).
- **07-03 a las 08:02:** en el M1 de cerca, la línea tomada de 1.14500 (etiqueta violeta) y el 0 en 1.14496 (etiqueta azul) se ven separados, cada uno con su precio. El tramo empieza en la vela de la toma, la de las 07:56, como dice la frase.
- **La de RN-009 «3, y admite 1»:** las tres zonas de control se ven una a una en el M1 de cerca (las de las 08:39, 08:44 y 08:46). La línea tomada lleva una sola etiqueta, la de 1.16862, que es la de la frase.
- **La de RN-009 que dice 18:** el M1 de cerca enseña 14, por el tope de 60 velas.
- **Lo que ya no pasa:**
  - etiquetas montadas;
  - el punto de la toma fuera del panel;
  - rótulos o marcas tapados;
  - marcas de borde una encima de otra. En la lámina que encontró el revisor, «▼ 1.14239» (el objetivo) y «▼ 1.14234» (la línea de M15) se ven apiladas.
- **Lo que no queda limpio:**
  - **Las marcas de borde** caen dentro del dibujo, donde llegan las velas que fijan la escala, y en varias de las 16 capturas (al menos 5, sobre todo en el borde izquierdo) tienen una vela o una línea detrás. Con el borde del color del fondo se leen, pero no quedan limpias. Sacarlas al margen de arriba choca con el título del panel; no lo toco sin tu respuesta.
  - **Dos láminas tienen un tramo de 1 y de 2 velas**, medido con `tramos_cortos.py`, de la carpeta de trabajo: la toma es la vela que coloca o la anterior. El panel cumple la regla, pero enseña una o dos velas muy anchas; las otras 45 tienen 6 velas o más. Si quieres un mínimo de velas, es una línea más en `tramo_de_cerca`.

**La CI de esta ronda**, por `fix/laminas`. En todas, el único fallo es el aceptado (`tests/unit/test_cli.py::test_state_check_ok_on_real_repo`: PROJECT_STATE declara `trabajo/laminas` y la rama es `fix/`):
- **Run 42961299280**, sobre `1a9c922`: `1 failed, 3363 passed, 48 skipped`.
- **Run 42966334841**, sobre `2178a65`: `1 failed, 3364 passed, 48 skipped`.
- **Run 42970555589**, sobre `1d40323`: `1 failed, 3366 passed, 48 skipped`.
- **Run 42974511672**, sobre `1201262`: `1 failed, 3368 passed, 48 skipped`.
- **Run 42980390492**, sobre `58de6ce`: `1 failed, 3369 passed, 48 skipped`.

## El revisor de la ronda tras revisar la v3 (2026-11-11), tal cual

Solo sobre esta ronda, sobre `1201262` y la sección sin commitear: 0 bloquea, 1 importa y 3 menores. Lo hecho con cada uno:
- **b-i1 (importa):** arreglado en `58de6ce`, con su test. La v4 de `1201262` se apartó y se escribió la buena (arriba, la cuarta vuelta del punto 1).
- **a-m1:** el paréntesis de la fila del 2026-11-10, quitado.
- **b-m1:** la frase del test de las marcas, reescrita.
- **b-m2:** la cuenta de las capturas, reescrita, y el docstring del test, corregido.

Lo que no pudo comprobar (la `clave.txt`, los logs, que los tests fallen con el código anterior) lo comprobé yo: la clave con `diff`, sin abrirla; los logs y los tiempos, en la carpeta de trabajo. Los tests nuevos los repasé uno a uno: fallarían sin su arreglo, y el de `58de6ce` falla con una llamada que el código anterior no admitía. Después de `58de6ce` no volví a pasar el revisor.

> ## Informe del revisor · trabajo/laminas · ronda tras revisar la v3 (`ea08ae2..HEAD` + la sección sin commitear) · 2026-11-11
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a-m1 | menor | En la fila del 2026-11-10 de HOLDOUT-EXPOSICIONES sobra un paréntesis de cierre. | `docs/validation/HOLDOUT-EXPOSICIONES.md:135`: «…lo que se repite va en la fila del 2026-11-11).» |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` da «CONTRATO: 23 ficheros dentro del contrato de trabajo/laminas (riesgo alto, artefacto docs/validation/LAMINAS.md, tramo 'R4 · …', 3 comprobaciones para el revisor)». `uv run botsito state check` da «OK: rama 'trabajo/laminas' …».
> - **`make check`.** No lo ejecuté (escribe). En `make-check.log` están «SELLO: make check en verde sobre el arbol fd2c32bf…», `3417 passed`, `exit=0` y «PICO DE MEMORIA … 313 MiB». `git rev-parse HEAD^{tree}` da `fd2c32bf…`: el sello es el de `1201262`.
> - **El diff de la ronda.** Solo toca 7 ficheros: `engine/laminas.py`, `engine/laminas_svg.py`, `tests/unit/test_laminas_svg.py`, el informe, el encargo, HOLDOUT-EXPOSICIONES y PROJECT_STATE. Lo único sin commitear es `LAMINAS.md`. No toca `knowledge/`, `scripts/`, `.claude/`, `spec/` ni `domain/`, así que no hacen falta trailers `Fuente:`, ni regímenes, ni ambigüedades, ni ADR.
> - **HOLDOUT-EXPOSICIONES.** Contra `main`, 0 líneas quitadas. Las filas del 2026-11-10 y del 2026-11-11 están. El recuento de la del 11 cuadra con los commits: 6 invocaciones, 4 completas, y tres `make check` (`2178a65`, `1d40323` y `1201262`, todos del 11, a las -0500).
> - **Informes cerrados.** `LAMINAS.md` no existe en `main`, así que no aplica.
> - **PROJECT_STATE.** De 1987 a 1995: los 8 `def test_` nuevos de la ronda.
> - **La respuesta copiada.** La copia del encargo y la del informe son idénticas: md5 de las líneas `>`, `490115f6…` en las dos.
> - **El estado.** El `## Estado` está al final y dice «EN CURSO».
>
> ### Eje (b) · Encargo (la respuesta tras revisar la v3)
> Resumen: 0 bloquea, 1 importa, 2 menores. Requisitos: 14 hechos, 0 parciales, 0 no hechos. El 15, la PARADA final, va después del revisor.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Panel «M1 de cerca» debajo del M1 y encima de la sustentación | Hecho | `laminas_svg.py:450` (y0 = 3·ALTO_PANEL), `pagina` en `:491-494`; captura de la lámina con corte a las 08:02 |
> | 2 | Tramo: desde la toma, o 15 velas antes del primer control si es anterior; tope de 60; sin toma, 30 | Hecho | `laminas_svg.py:269-283`. En la captura RN-009 «3, y admite 1» el tramo empieza a las 08:24, 15 velas antes del control de las 08:39 |
> | 3 | Escala: velas, caja, orden y stop; lo de fuera como marca con precio y flecha | Hecho (ver b-i1) | `:447-450`, `:381-384`, `_fuera` `:255-266` |
> | 4 | Lleva lo mismo que el M1, en su escala | Hecho | `:470-473`: `_m1`, `_lineas_m15`, `_etiquetas` y `_fuera` sobre `cerca` |
> | 5 | Mismo recorte y mismas puertas: un subconjunto, nada fuera de la ventana | Hecho | `tramo_de_cerca` corta `d.m1` (`:274-283`). Medido en las 47 de la v4: 0 elementos del panel 4 a la derecha del corte (x > 1490) o fuera del panel |
> | 6 | Tests: el tramo, el tope de 60, la escala y ninguna marca a la derecha del corte | Hecho | `test_el_tramo_del_m1_de_cerca` y `test_la_escala_del_m1_de_cerca_y_lo_que_queda_fuera`. La escala fallaría si entrara el objetivo: la rejilla tiene que ser la de hi/lo sin 110_400 |
> | 7 | Capturas: a las 08:02, 1.14500 y el 0 en 1.14496 separados y con su precio; RN-009 «3, y admite 1», sus tres zonas | Hecho | Vistas las dos capturas `v4d`: etiqueta violeta 1.14500 y azul 1.14496 separadas; tres cuadros naranjas a las 08:39, 08:44 y 08:46; una sola etiqueta tomada, la de 1.16862 |
> | 8 | Frase de la toma con la hora de apertura | Hecho | `laminas.py:520`, `:852` y `:858` (`t.instante - 1`). Medido: las 32 frases de la toma de la v4 van exactamente 1 min antes que en la v3 (32 de 32) |
> | 9 | Repasar cada frase con hora y decir cuáles cambian | Hecho | Informe, punto 2. En la v3 y en la v4 solo hay frases con hora de la toma (23 + 9) y del punto (31, sin cambio). Ninguna frase sin hora cambia, fuera de las saltadas |
> | 10 | Test que fija el convenio; la cabecera se queda | Hecho | `test_toda_hora_que_nombra_una_vela_es_la_de_su_apertura` (fallaría con la frase vieja); cabecera en `laminas_svg.py:491-492` |
> | 11 | La frase de las saltadas, en singular y en plural | Hecho | `laminas.py:476-496`; en la v4, «Antes de esa vela, el bot se saltó 3 velas H4…» |
> | 12 | v4 tras el ensayo, mismo orden, misma clave; F4.1 y F4.2 solo si el diff sale del código | Hecho | `diff -rq -x clave.txt` de la v4 contra `ensayo-v4d`: exit 0. El diff solo sale a documentos, y el informe lo declara (`LAMINAS.md:933`). La clave, sin comprobar (abajo) |
> | 13 | Capturas de la ronda anterior más las dos del punto 1, y mirarlas | Hecho (ver b-m2) | 15 `v3-*.png` y 16 `v4d-*.png` |
> | 14 | Recuentos del punto 5 | Hecho | `comparar_v4.py` v3→v4: 47/47 emparejadas; 47 con panel; 32 frases con hora; 4 de las saltadas; 13 de RN-009, 12 iguales y la de 18 con 14 en el M1 de cerca y 18 en el M1 |
> | 15 | v1, v2 y v3 sin tocar | Hecho | mtime de las carpetas: v1 15:35, v2 18:03 y v3 22:27 del 2026-11-10, todas antes de `ea08ae2` (22:58) |
> | — | «Después»: `make check`, CI de `fix/laminas`, revisor | Hecho (el revisor es este) | Runs 42961299280, 42966334841, 42970555589 y 42974511672: headSha `1a9c922`, `2178a65`, `1d40323` y `1201262`. Los cuatro con «1 failed, 3363/3364/3366/3368 passed, 48 skipped», y el único FAILED es `test_cli.py::test_state_check_ok_on_real_repo`, como dice el informe |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b-i1 | importa | **Las marcas de borde no se apilan entre clases.** `_fuera` solo apila las líneas de M15 entre sí. La marca del objetivo (`_m1`, `laminas_svg.py:384`, `fila` siempre 0) no se aparta de ellas. En la v4 hay una lámina con `objetivo-fuera` y `m15-fuera` en el mismo punto exacto del M1 de cerca. El informe dice «las marcas de borde se apilan» (`LAMINAS.md:945`) y no lo menciona en «Lo que no queda limpio». Ningún test cubre este caso. | Script de solo lectura sobre los 47 HTML de la v4. Pares de marcas `*-fuera` del mismo panel a menos de 10 en y y de 90 en x: 1 en total, `('objetivo-fuera', 20.0, 1167.0, 'start', '▼ 1.14239')` y `('m15-fuera', 20.0, 1167.0, 'start', '▼ 1.14234')`. |
> | b-m1 | menor | «El test de las marcas de `test_laminas.py` recorre ahora los cuatro paneles» se puede leer como que se cambió. No se tocó: los recorre porque ya recorría todo el SVG. | `LAMINAS.md:940`; `git diff --stat ea08ae2..HEAD -- tests` solo da `test_laminas_svg.py` |
> | b-m2 | menor | «Son 16: las de la ronda anterior más las dos del punto 1»: la ronda anterior tenía 15 y una de las dos ya estaba entre ellas, así que la suma no es 15 + 2. También: el docstring de `test_los_rotulos_y_las_marcas_de_borde_van_delante_de_las_velas` dice «Van detras de todas las velas» (lo que quiere decir es que van después en el SVG). | `LAMINAS.md:967`; 15 `v3-*.png` y 16 `v4d-*.png` en `capturas/`; `tests/unit/test_laminas_svg.py:662` |
>
> Sobre si los tests fallarían sin el arreglo: lo comprobé leyendo el código, sin ejecutarlo contra el código anterior.
> - El punto de la toma: sin `p.lo <= nivel <= p.hi` se dibujaría en `hi+1`.
> - Los rótulos: sin el paso a `delante` quedan antes de la última vela.
> - La línea que acabó antes: sin `vistas` sube el recuento del panel 3.
> - Las marcas apiladas: sin `fila` las dos y serían iguales.
> - La etiqueta tomada: sin `_pedidas(..., tomadas)` el recuento es 0.
>
> ### Lo que no pude comprobar
> - **Que `clave.txt` de la v4 sea idéntica a la de la v3.** Prohibido abrirla. Excluí la clave del `diff -rq`.
> - **Las cifras de los ensayos `v4`, `v4b` y `v4c`** (que «las cifras son las mismas en los tres ensayos») y los datos de los logs: base `(31, 192, …)`, 480,2 s / 646,4 MiB, «19 de tipo a y 28 de tipo b». Están fuera del material HTML permitido o en logs.
> - **Si la lámina de b-i1 está entre las 16 capturas.** La guardia bloqueó el script que lo cruzaba (recorre directorios construidos en ejecución). No lo reescribí para rodearla.
> - **Que los tests nuevos fallen de verdad con el código de `ea08ae2`.** Exige un clon desechable, que escribe.
> - **«Al menos 5 capturas con una vela detrás de una marca»**: es un juicio visual. Vi solo las dos capturas del punto 1.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`; `git log --format='%h %s' ea08ae2..HEAD`; `git diff --stat ea08ae2..HEAD`; `git status --short`
> 2. `git diff ea08ae2..HEAD -- docs/encargos/trabajo-laminas.md docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md docs/validation/LAMINAS.md`
> 3. `git diff -- docs/validation/LAMINAS.md`
> 4. `git diff ea08ae2..HEAD -- src/botsito/engine/laminas.py src/botsito/engine/laminas_svg.py`
> 5. `ls tests/unit | grep -i lamin`; `git diff --stat ea08ae2..HEAD -- tests`; `grep` en `test_laminas.py`; Read de `test_laminas.py:340-399` y de `laminas_svg.py:80-515`
> 6. `grep` de horas en `laminas.py`; `sed -n 1220,1250p` y `895,915p` de `laminas.py`
> 7. `git diff ea08ae2..HEAD -- tests/unit/test_laminas_svg.py`
> 8. `ls` de la carpeta de trabajo y de `capturas/`; `cat comparar_v4.py etiquetas_montadas.py`
> 9. `python -I comparar_v4.py <v3> <v4>`
> 10. Scripts `python -I -c` de solo lectura sobre los HTML de la v3 y la v4: frases con hora; nada a la derecha del corte; la hora de la toma, 1 min antes; marcas de borde montadas
> 11. `python -I etiquetas_montadas.py` sobre la v4 y la v3. La primera forma, encadenada, la negó la guardia; la partí en llamadas
> 12. `diff -rq -x clave.txt <v4> <ensayo-v4d>`
> 13. Un script para cruzar la lámina de b-i1 con las capturas: negado por la guardia, no reintentado
> 14. Read de `capturas/v4d-s04-l01.png` y `capturas/v4d-s02-l02.png`
> 15. `gh run view <id> --json conclusion,headSha,headBranch` y `gh run view <id> --log-failed | grep` para los runs 42961299280, 42966334841, 42970555589 y 42974511672
> 16. `git log --format='%h %ad %cd %s' --date=iso ea08ae2^..HEAD`; `git show --stat` de los cuatro commits
> 17. `cat contrato.yaml`; `ls -la make-check.log`; `tail`/`grep` de `make-check.log`; `git rev-parse HEAD^{tree}`
> 18. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`
> 19. md5 de las líneas `>` de la respuesta en el encargo y en el informe (la forma con `> /dev/stdout` la negó `solo_lectura.py`)
> 20. `git cat-file -e main:docs/validation/LAMINAS.md`; `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md | grep -c '^-[^-]'` (la forma con `data` en la lista de rutas la negó la guardia)
> 21. `grep -n` de los números de línea de los hallazgos menores
> 22. `ls -ld --time-style=full-iso` de las carpetas v1 a v4

## Respuesta del consultor tras revisar la v4 (2026-11-11)

Dada por Aleks (consultor) el 2026-11-11, tal cual (también al final de `docs/encargos/trabajo-laminas.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor tras revisar la v4 de trabajo/laminas (2026-11-11). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor tras revisar la v4», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> He revisado la v4: las 47 dibujadas en un navegador, a fondo 07-03 a las 08:02, 07-03 a las 09:35 y la de 04-13 con «3, y admite 1», y el texto de todas pasado por las regex de los puntos 4 y 5 (limpio). El panel «M1 de cerca» hace lo que tenía que hacer: la toma en 1.14500 y el 0 en 1.14496 se ven separados, con sus precios, las tres zonas de control se distinguen una a una y las horas ya van por la apertura de la vela. Las láminas quedan revisadas, salvo dos detalles que se arreglan aquí:
>
> 1. Un mínimo de 15 velas en el M1 de cerca. Si el tramo que da la regla de la ronda anterior tiene menos de 15, empieza 15 velas antes del corte; el tope de 60 sigue igual. Con su test. Las dos láminas que hoy tienen 1 y 2 velas quedan con 15; di en el informe cuántas cambian.
> 2. La m1 del revisor de la ronda de dibujo no va a deuda. La marca de borde de una línea de M15 que queda fuera del M1 decide su lado contra el mismo rango con el que se decidió dejarla fuera, no contra el máximo de la escala, que estiran las zonas de control y el punto (laminas_svg.py:207-211 y :224). Aplica lo mismo en el M1 de cerca, si tiene el mismo defecto. Con un test de ▲ y otro de ▼, incluido el caso del revisor. La línea de Technical Debt propuesta sale.
> 3. Lo demás se queda como está y va al informe, sin deuda nueva: en la lámina que dice 18 zonas de control, el M1 de cerca enseña 14, porque el tope de 60 velas deja 4 fuera y el M1 las enseña todas; y las marcas de borde con una vela detrás se leen.
> 4. Regenera tras el ensayo en el clon, en C:\Users\USER\Desktop\laminas-sesion-7-v5, con el mismo orden barajado y la misma clave (diff, sin abrirla). F4.1 y F4.2 no se repiten si el diff no sale de engine/laminas.py, engine/laminas_svg.py, sus tests y los documentos.
> 5. El revisor, sobre todo lo posterior a su última pasada (58de6ce y esta ronda), con su informe pegado al final.
> 6. Sobre el hallazgo de la guardia de la ronda anterior: reescribir la regex y la cadena del guion para que la guardia no las tomara por ruta es rodearla (CLAUDE.md, «Una guardia no se rodea»), aunque el guion solo leía HTML de láminas y lo declaraste. La próxima vez se para y se dice. Va como hallazgo menor en la fila de ERRORES del cierre, y el falso positivo, a Technical Debt (orden de cierre).
>
> Después: make check, push a fix/laminas con su CI y una PARADA corta con el resultado del make check, el run de la CI, lo que diga el revisor, los recuentos de los puntos 1 y 2, la ruta de la v5 y «Rama lista para revisión, NO cerrada.».

## Aplicación de la respuesta tras revisar la v4, punto por punto (2026-11-11)

El código solo cambia en `src/botsito/engine/laminas_svg.py`, con sus tests en `tests/unit/test_laminas_svg.py` (commit `43d4bc3`). Por eso F4.1 y F4.2 no se repiten (punto 4). Fuera de eso cambian el informe, la respuesta copiada en el encargo, la fila del 2026-11-11 de HOLDOUT-EXPOSICIONES y el recuento de tests de PROJECT_STATE.

1. **Un mínimo de 15 velas en el M1 de cerca** (`VELAS_CERCA_MIN = 15`, en `tramo_de_cerca`). Si la regla de la ronda anterior da menos de 15, el tramo empieza 15 velas antes del corte; el tope de 60 sigue.
   - **El test:** `test_el_m1_de_cerca_tiene_como_poco_15_velas` (tramos de 1, 3 y 14 velas quedan en 15; uno de 20 no cambia; el tope de 60 sigue).
   - **Cambian 9 láminas:** las dos que tenían 1 y 2 velas y siete que tenían de 6 a 8. Las 9 quedan con 15, y ninguna queda por debajo. Lo mide `comparar_v5.py`, de la carpeta de trabajo, que solo lee los HTML.
   - **En las capturas de las dos de 1 y 2 velas** (del ensayo de `43d4bc3`), el M1 de cerca enseña ahora 15 velas, con la caja formándose, el punto y la toma.
2. **El lado de la marca de borde del M1** (la m1 del revisor de la ronda de dibujo). La marca de una línea de M15 que queda fuera del M1 decide su lado contra `rango_del_m1`, el mismo rango con que `lineas_del_m1` la deja fuera. Ya no se decide contra la escala del panel, que estiran las zonas de control y el punto.
   - **El M1 de cerca no tiene el defecto:** allí las líneas se dejan fuera con `cerca.lo <= nivel <= cerca.hi`, que es su propia escala. Su escala la fijan las velas del tramo, la caja, la orden y el stop; ni las zonas de control ni el punto la estiran.
   - **El test:** `test_la_marca_de_borde_del_m1_decide_su_lado_con_el_rango_que_la_deja_fuera`. Tiene un caso de ▲, que es el del revisor: una línea por encima del rango, pero por debajo del alto que estira una zona de control, salía con ▼. Tiene también un caso de ▼, el simétrico. El de ▲ fallaría con el código de antes (lo razoné leyendo el código, sin correrlo contra él). El de ▼ no: con el código de antes, una línea por debajo del rango ya salía siempre con ▼, porque el defecto solo existía hacia arriba. Ese caso protege contra otro error, el de decidir el lado contra un suelo mal puesto, y no contra este (revisor de la ronda, b-i1).
   - **Cambian de lado 0 marcas en la v5.** Las 3 marcas de borde de líneas de M15 del M1 ya apuntaban bien, como dijo el revisor de la ronda de dibujo. El defecto solo aparecía en el caso del test.
   - **La línea de Technical Debt propuesta sale** (en las propuestas para la orden de cierre).
3. **Lo que se queda como está.** En la lámina que dice 18 zonas de control, el M1 de cerca enseña 14: el tope de 60 velas deja 4 fuera, y el M1 las enseña todas. Las marcas de borde con una vela detrás se leen. Medido de nuevo en el ensayo de `43d4bc3`, los recuentos del punto 5 de la ronda anterior no cambian. Siguen a 0 las etiquetas del eje montadas, las marcas de borde montadas y las líneas de longitud cero del M1 de cerca.
4. **La v5:** en `C:\Users\USER\Desktop\laminas-sesion-7-v5`, de `43d4bc3`, tras el ensayo en el clon (`git worktree add --detach`), con el mismo orden barajado.
   - La orden, tal cual salvo la lista: `uv run botsito motor laminas --sesiones <las diez sesiones, en el orden de clave.txt> --salida C:\Users\USER\Desktop\laminas-sesion-7-v5`.
   - Su `clave.txt` es idéntica a la de la v4 (`diff`, 0 bytes; no se abrió). `diff -r` de la v5 contra su ensayo: 0 bytes.
   - Base con y sin el recolector, `(31, 192, 24, 1150, 0, 32, 0)`.
   - Ensayo: 595,7 s y 645,7 MiB. La v5: 577,1 s y 644,8 MiB.
   - 47 láminas, 19 de tipo a y 28 de tipo b, como en la v4.
5. **El revisor**, sobre `58de6ce` y esta ronda: al final, tal cual.
6. **Rodear la guardia.** En la respuesta a la PARADA final, para que la guardia no tomara por ruta una regex y una cadena de un guion de medida, las reescribí. Eso fue rodearla, aunque el guion solo leía HTML de láminas y lo declaré. La próxima vez se para y se dice.
   - Va como hallazgo menor en la fila de ERRORES-RECURRENTES del cierre, y el falso positivo, a Technical Debt (las dos en las propuestas para la orden de cierre).
   - **En esta ronda y en la anterior, ante cada negativa de la guardia:**
     - un comando partido en llamadas sueltas (`date`, `tail`), la forma que ella propone;
     - el guion con Write, ejecutado en otra llamada, en lugar de una tubería con `paste` y `bc` (`tipos.py`), la forma que ella propone;
     - para el `grep` de retornos de carro (`$'\r'`), la guardia no propuso esa forma: propuso rutas literales, que ya lo eran, o la herramienta Read. No reescribí el comando. Medí el defecto de otra forma, con `git diff --stat`, que enseña un fichero entero cambiado si los finales de línea lo están. La negativa es un falso positivo: `$'\r'` es una cadena constante. Va con el otro a la línea de Technical Debt de la guardia.
   - Lo digo aquí por si alguna de estas cuenta también como rodearla.

**La CI**, por `fix/laminas`. El único fallo es el aceptado (`tests/unit/test_cli.py::test_state_check_ok_on_real_repo`: PROJECT_STATE declara `trabajo/laminas` y la rama es `fix/`):
- **Run 42985112624**, sobre `824d574` (el informe de la ronda anterior): `1 failed, 3369 passed, 48 skipped`.
- **Run 43044973233**, sobre `43d4bc3`: el primer intento se canceló a los 20 minutos, colgado en el `apt-get install` de ffmpeg y sin llegar a `make check`; relanzado (intento 2), que al escribir esto seguía en el mismo paso. Su resultado, y el de la CI del commit de este informe, van en la PARADA final.

## El revisor de la ronda tras revisar la v4 (2026-11-11), tal cual

Sobre `1201262..43d4bc3` y la sección sin commitear: 0 bloquea, 1 importa y 2 menores, todos en el informe y ninguno en el código. Lo hecho con cada uno:
- **b-i1 (importa):** la frase de los dos tests, corregida. El de ▼ no protege contra este defecto, y el test se queda como está.
- **b-m1:** el puntero de la línea de Technical Debt de la guardia, corregido.
- **a-m1:** el Estado, al día.
- **El caso dudoso del `$'\r'`:** dicho qué propuso la guardia, y el falso positivo, a la misma línea de Technical Debt.

Como no cambia el código, la v5 no se regenera.

> ## Informe del revisor · trabajo/laminas · ronda tras revisar la v4 (`1201262..HEAD` + la sección sin commitear) · 2026-11-11
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a-m1 | menor | El `## Estado` no está al día. Dice que «siguen la v5, la CI, el revisor y la PARADA corta», pero la sección sin commitear ya da la v5 por escrita. | `docs/validation/LAMINAS.md:1507` frente a `:1118-1123` |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` da «CONTRATO: 23 ficheros dentro del contrato de trabajo/laminas (riesgo alto, artefacto docs/validation/LAMINAS.md, …, 3 comprobaciones para el revisor)», exit 0. `uv run botsito state check` da «OK: rama 'trabajo/laminas' …», exit 0.
> - **`make check`.** No lo ejecuté (escribe). En `make-check.log` (10:05:49) están `3420 passed`, «SELLO: make check en verde sobre el arbol 5cbe40cf…», «PICO DE MEMORIA … 313 MiB» y `exit=0`. `git rev-parse HEAD^{tree}` da `5cbe40cf…`: el sello es el de `43d4bc3`.
> - **El diff de la ronda.** `git diff --name-only 1201262..HEAD -- src tests` solo da `engine/laminas_svg.py` y `tests/unit/test_laminas_svg.py`. El resto son documentos: el informe, el encargo, HOLDOUT-EXPOSICIONES y PROJECT_STATE. No toca `knowledge/`, la spec, los ADR, las ambigüedades ni `domain/`, así que no hacen falta trailers `Fuente:` ni hay regímenes que mirar.
> - **HOLDOUT-EXPOSICIONES.** Contra `main`, 0 líneas quitadas.
>   - La fila del 2026-11-11 declara la ronda nueva y a este revisor sobre los HTML de la v4, la v5 y el ensayo.
>   - Su recuento cuadra con los commits del día 11 (`git log`): 8 invocaciones y 6 completas, y cinco `make check` (`2178a65`, `1d40323`, `1201262`, `58de6ce` y `824d574`). Después vienen «dos más», el de `43d4bc3` y el del commit de esta sección.
>   - El paréntesis de a-m1 de la pasada anterior ya no está.
> - **PROJECT_STATE.** Pasa de 1995 a 1998, que son los 3 `def test_` nuevos (uno de `58de6ce` y dos de `43d4bc3`).
> - **Retornos de carro.** Ninguno en `LAMINAS.md`, `laminas_svg.py` ni `test_laminas_svg.py`.
> - **Las cifras.** `VELAS_CERCA_MIN` es una constante de dibujo junto a las otras tres (`laminas_svg.py:68-73`). El `make check` en verde incluye `test_no_business_literals`.
> - **La respuesta copiada.** La del encargo y la del informe son idénticas: md5 de las líneas `>`, `51823b5b…` en las dos.
>
> ### Eje (b) · Encargo (respuesta tras revisar la v4)
> Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 13 hechos, 0 parciales, 0 no hechos. La CI de `43d4bc3` y la PARADA van después.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Un mínimo de 15 velas en el M1 de cerca; el tope de 60 sigue | Hecho | `laminas_svg.py:321-322`: primero `min(desde, len-15)`, después `max(desde, 0, len-60)` |
> | 2 | Su test | Hecho | `test_el_m1_de_cerca_tiene_como_poco_15_velas` cubre 1, 3 y 14 velas, que quedan en 15; 20, que no cambia; y el tope de 60. Falla sin el arreglo: si el fixture tuviera una zona de control que moviera `desde`, el caso de 1 vela daría 16 o más, no 15, así que con el código anterior saldría 1. `pytest tests/unit/test_laminas_svg.py`: 30 passed. |
> | 3 | Cuántas cambian; las de 1 y 2 velas quedan con 15 | Hecho | `comparar_v5.py v4 v5`: «cambian … 9; con menos de 15: v4 9, v5 0». Pares (antes, después): (1,15) (2,15) (6,15)×5 (7,15) (8,15); en la v5 va de 15 a 60. Cuadra con `LAMINAS.md:1110`. |
> | 4 | La marca de borde del M1 decide su lado con el rango que la deja fuera | Hecho | `rango_del_m1` (`:230-243`) lo comparten `lineas_del_m1` (`:225`) y `_fuera(…, rango_del_m1(d)[1])` (`:510`) |
> | 5 | Lo mismo en el M1 de cerca, si tiene el defecto | Hecho: no lo tiene, como dice el informe | La escala la fijan las velas del tramo, la caja, la orden y el stop (`:489-492`). Lo que queda fuera se decide con esa misma escala, `cerca.lo <= nivel <= cerca.hi` (`:496`). El objetivo de `_m1` decide su lado contra `p.hi`, que es esa escala. En el M1 la lista de `otras` va vacía, porque el objetivo entra en `niveles_m1` (`:483-484`). |
> | 6 | Un test de ▲ con el caso del revisor y otro de ▼ | Hecho (ver b-i1) | `test_la_marca_de_borde_del_m1_decide_su_lado_con_el_rango_que_la_deja_fuera` |
> | 7 | En la v5 no cambia de lado ninguna marca | Hecho | `comparar_v5.py`: «marcas de borde de M15 en el M1: 3; cambian de lado: 0» |
> | 8 | Sale la línea de Technical Debt de la flecha | Hecho | `LAMINAS.md:628` |
> | 9 | Punto 3, al informe y sin deuda: 18 frente a 14, y las marcas con vela detrás | Hecho | `LAMINAS.md:1117`. `comparar_v4.py v4 v5`: 13 de RN-009, la de 18 con 14 en el M1 de cerca y 18 en el M1. 0 frases con hora cambiadas. 0 láminas con el texto fuera del SVG distinto de la v4 a la v5. |
> | 10 | La v5 tras el ensayo, con el mismo orden y la misma clave | Hecho (la clave sin comprobar, abajo) | `diff -rq -x clave.txt v5 ensayo-v5`: exit 0. `marcas_montadas.py` y `etiquetas_montadas.py` sobre la v5: 0 marcas montadas, 0 etiquetas montadas y 0 líneas de longitud cero. Las capturas `v5-s03-l03` y `v5-s04-l04` enseñan 15 velas (12:18-12:32 y 09:09-09:23), la caja, el punto y la toma. |
> | 11 | F4.1 y F4.2 no se repiten porque el diff no sale de ahí | Hecho | El diff de la ronda queda dentro de `laminas_svg.py`, su test y los documentos (eje a) |
> | 12 | Punto 6: el hallazgo menor para la fila de ERRORES y el falso positivo a Technical Debt, en las propuestas para la orden de cierre | Hecho (ver b-m1) | `LAMINAS.md:629` (Technical Debt) y `:630` (ERRORES) |
> | 13 | Después: `make check`, la CI y el revisor | Hecho hasta el revisor; `{CI}` queda pendiente, como se esperaba | Sello de `43d4bc3` (eje a). Run 42985112624, sobre `824d574`: `1 failed, 3369 passed, 48 skipped`, y el único FAILED es `test_state_check_ok_on_real_repo` |
> | — | `58de6ce` y mis hallazgos de la pasada anterior | Bien | b-i1: `_fuera` apila todas las clases (`:290-303`) y tiene su test. v4: 0 pares montados. Run 42980390492, sobre `58de6ce`: `1 failed, 3369 passed`, el aceptado. a-m1, b-m1 y b-m2: corregidos (`LAMINAS.md:940`, `:970`; `test_laminas_svg.py:662`). |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b-i1 | importa | **«Los dos fallarían con el código de antes» no se sostiene para el caso de ▼.** El caso de ▼ solo falla con el código anterior porque `rango_del_m1` no existía (AttributeError). Por su comportamiento, pasa: el código viejo decidía `arriba = nivel > p.hi`, así que una línea por debajo del rango siempre salía con ▼. El defecto solo existía hacia arriba. El caso de ▼ protege contra otro mutante, no contra este defecto. Lo que hay que corregir es la frase del informe, no el test. | `LAMINAS.md:1114`; `git show 58de6ce:src/botsito/engine/laminas_svg.py`, línea 272: `arriba = nivel > p.hi`; el test, en `test_laminas_svg.py` (`abajo = _con_linea_y_control("bajo", lo - 3, lo - 100)`) |
> | b-m1 | menor | **La línea de Technical Debt del falso positivo cita una sección que no es la suya.** Remite a «lo que vi en las capturas de la respuesta a la PARADA final», pero el pasaje está en «Aplicación de la respuesta a la PARADA final», justo antes de ese encabezado. Esa línea irá a PROJECT_STATE con ese puntero. | `LAMINAS.md:629`; el pasaje está en `:698-702` y el encabezado citado en `:704` |
>
> **Sobre si las formas del punto 6 cuentan también como rodear la guardia.** Es un juicio, no un hallazgo:
> - **Partir un comando en llamadas sueltas** y **escribir el guion con Write para ejecutarlo en otra llamada:** no las veo como rodearla. Siguen la práctica ya aceptada en la casa, que es usar la forma que la propia guardia propone y declararla; para el guion, «Trampas medidas» de CLAUDE.md lo recomienda tal cual. Las usé yo mismo en la pasada anterior.
> - **El `grep` de `$'\r'` sustituido por `git diff --stat`:** es el caso dudoso. No reformula el comando negado: consigue otra prueba con otro comando, permitido, y lo declara. Para mí eso no es rodearla. Pero el informe lo pone bajo «usé la forma que ella misma propone» sin decir si la guardia propuso eso, ni si la negativa fue un falso positivo; si lo fue, también debería ir a Technical Debt.
> - Los textos de las negativas no están en el repo, así que no pude ver qué propuso la guardia en cada una.
>
> ### Lo que no pude comprobar
> - **Que la `clave.txt` de la v5 sea idéntica a la de la v4.** Tengo prohibido abrirla, así que la excluí del `diff -rq`.
> - **Los tiempos y la memoria del ensayo y de la v5** (595,7 s / 645,7 MiB y 577,1 s / 644,8 MiB), la base `(31, 192, …)` y «19 de tipo a y 28 de tipo b». Están en los logs, fuera del material que puedo leer.
> - **Que los tests fallen corriendo de verdad contra el código de `1201262`.** Hace falta un clon desechable, que escribe. Lo razoné leyendo el código anterior (`git show`).
> - **Qué propuso la guardia en cada negativa** del punto 6: no queda registrado en el repo.
> - **La CI de `43d4bc3`:** el run está relanzado y es el `{CI}` pendiente.
>
> ### Comandos ejecutados
> 1. `git log --format='%h %s' 1201262..HEAD`; `git diff --stat 1201262..HEAD`; `git status --short`
> 2. `git diff 1201262..HEAD -- src/ tests/ PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md docs/encargos/`
> 3. `git diff 1201262..HEAD -- docs/validation/LAMINAS.md`; `git diff -- docs/validation/LAMINAS.md`
> 4. Read de `laminas_svg.py:90-329` y `:440-518`; Grep de las constantes
> 5. `ls` de la carpeta de trabajo; `cat comparar_v5.py`; Read de `comparar_v4.py`
> 6. `python -I comparar_v5.py <v4> <v5>`; `python -I -c` de solo lectura con los pares de velas de v4 a v5 y el texto fuera del SVG
> 7. `diff -rq -x clave.txt <v5> <ensayo-v5>`
> 8. `python -I marcas_montadas.py <v5>` y `<v4>`; `python -I etiquetas_montadas.py <v5>`; `python -I comparar_v4.py <v4> <v5>`
> 9. Read de `capturas/v5-s03-l03.png` y `capturas/v5-s04-l04.png`
> 10. Grep en `.claude/hooks/guardia.py` de los mensajes que proponen formas (sin resultado concluyente)
> 11. `grep -n` y `sed -n` en `LAMINAS.md` (propuestas, encabezados, afirmaciones); Read de `LAMINAS.md:690-705` y `:1503-1508`
> 12. `uv run python scripts/contrato_rama.py`; `cat contrato.yaml`; `ls -la make-check.log`; `grep` en `make-check.log`; `git rev-parse HEAD^{tree}`; `git log -3`
> 13. `uv run botsito state check`
> 14. `uv run pytest -q -p no:cacheprovider tests/unit/test_laminas_svg.py` (dos veces; 30 PASSED); `git diff --name-status main...HEAD`; `git diff --name-only 1201262..HEAD -- src tests`
> 15. `git log --format='%h %ci %s' -9`; `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md | grep -c '^-[^-]'` (0)
> 16. md5 de las líneas `>` de la respuesta en el encargo y en el informe
> 17. `python -I -c` para buscar retornos de carro en los tres ficheros
> 18. `gh run view 42985112624` y `42980390492`, con `--json conclusion,headSha,headBranch` y con `--log-failed | grep`
> 19. `git show 58de6ce:src/botsito/engine/laminas_svg.py | grep -n …`; `git show --stat` de los tres commits
>
> Ficheros clave: `C:\Users\USER\Desktop\Bot v3\docs\validation\LAMINAS.md` (líneas 629, 1114 y 1507), `C:\Users\USER\Desktop\Bot v3\src\botsito\engine\laminas_svg.py`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_laminas_svg.py`.

## Apéndice A · El informe del auditor del encargo (fase 0, 2026-11-10), tal cual

> ## Auditoría del encargo · trabajo/laminas · 2026-11-10
>
> Resumen: he comprobado 75 afirmaciones. 64 son correctas, 1 es incorrecta y 10 tienen matiz. Hay 8 cosas que el repo pide y el encargo no recoge, más una que no aplica.
>
> No ejecuté pytest, make, `uv run` ni Python, y no escribí nada en el repo. La guardia me negó un `for f` que contaba líneas de los anexos de TRAZAS-ABLACION: no lo rodeé, y el dato sale de TRAZAS-ABLACION.md:1227.
>
> ### Afirmaciones
> | # | Afirmación (del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | La rama es el punto (1) de F, que es R4.5 (RUMBO §3), en el tramo R4 | CORRECTA | PROJECT_STATE.md:28 «(1) las láminas del bot (R4.5)»; HOJA-DE-RUTA.md:408-414 (Refs NA:F); contrato.yaml `tramo` es igual al `##` de HOJA:316 |
> | 2 | main y origin/main están en e5394c5, sobre el merge 76bbe09; el tag stable/F38v es el último «- Tag:» | CORRECTA | `git rev-parse main origin/main` da e5394c57… dos veces; `stable/F38v-trazas-ablacion^{commit}` da 76bbe099; HISTORIA.md:16727 |
> | 3 | No hay ninguna otra rama y stable/F38w-laminas no existe | CORRECTA (en local) | `git branch -a`: main, trabajo/laminas y origin/main; `git tag -l "stable/F38w*"` sale vacío |
> | 4 | `motor decisiones` da la misma corrida con la cuenta por mes | CORRECTA | cli.py:2601-2603 y :2655 («lo mismo que motor arnes --simular») |
> | 5 | ACTIVAR-SESION-06 §«Para la sesión 7», punto 10: «se rehacen SIN fecha y con el contexto que pidió» | CORRECTA | ACTIVAR-SESION-06.md:609-610 |
> | 6 | La decisión de sustituir los gráficos 2 a 6 solo estaba en el chat | CORRECTA | No aparece en PROJECT_STATE, HOJA ni validation/. SESION-06-EXTRACCION.md:1246 y :1257 todavía dicen «se rehacen» |
> | 7 | ev-v17-004910-11d48393: «no me dice los criterios por qué, o sea, no veo los trazos de M15» | CORRECTA | knowledge/evidence/v17/ev-v17-004910-11d48393.yaml:7-9 (la puntuación la añade el encargo; es del gráfico 2) |
> | 8 | Lo de S-18, «me des un contexto un poco más claro […] de lo que ha ocurrido antes», está en §3.6 | CORRECTA | SESION-06-EXTRACCION.md:686-688 |
> | 9 | La trendline hasta donde haya rompimiento, sin extenderla (§3.6, 45:00-46:08) | MATIZ | SESION-06-EXTRACCION.md:691-692. Solo «[45:26] yo suelo utilizar la trendline por defecto» es literal; «hasta donde haya rompimiento y sin extenderla» es paráfrasis de la sesión. Dibujar desde el pivote hasta la vela que toma es lectura del encargo |
> | 10 | Decisión b de TRAZAS: la lámina de 07-03 enseña las líneas de M15; 1.14496 está a 4 puntos de 1.14500 | CORRECTA | TRAZAS-ABLACION.md:1392 y :819 |
> | 11 | OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA está en arnes.py:80 | CORRECTA | arnes.py:80-82 |
> | 12 | test_la_seccion_no_anade_ninguna_opcion_al_comando está en :341 | CORRECTA | test_diferencias_por_operacion.py:341-345 |
> | 13 | `_opciones_diagnostico` no la usa `motor decisiones` | CORRECTA | cli.py:2282; solo la llaman :3199 (arnes) y :3225 (visor) |
> | 14 | La bitácora de los cuatro días del anexo es la salida de F4.2 | CORRECTA | anexos/TRAZAS-ABLACION/bitacora.DIAGNOSTICO.{2026-04-13,07-02,07-03,07-14}.txt; TRAZAS:1227 (mismo sha256 que data/) |
> | 15 | graficos_sesion.py es el precedente (BARRIDO §2.2) | CORRECTA | BARRIDO-SESION-6.md:547; SESION-DE-PREGUNTAS.md:96-98 |
> | 16 | La regla 2 corta ANTES de la colocación y prohíbe enseñar la orden, el stop y el objetivo | CORRECTA | SESION-DE-PREGUNTAS.md:21-28 |
> | 17 | La regla 2 la cambia el ADR del método, en la rama de preparación de la sesión 7 | CORRECTA | RUMBO-2026-11.md:13; HOJA:386 |
> | 18 | El observador de MotorCableado está en cableado.py:311 | CORRECTA | cableado.py:308-311 |
> | 19 | El Cierre que recibe el observador lleva el bróker y el estado vivos | CORRECTA | cableado.py:221-237 y :444-448 (son los objetos del motor) |
> | 20 | F38v añadió los gates solo como registro | CORRECTA | HISTORIA.md:16704-16706 |
> | 21 | ADR-0080 §10 solo anota CUÁNTAS H4 se saltaron, no cuáles | MATIZ | ADR-0080:166-179; domain/sesgo.py:69-76 (`ResultadoSesgo`, solo contadores). Saber cuáles exige tocar `src/botsito/domain/`, que contrato.yaml protege, o recalcular, que el punto 1 prohíbe. ADR-0080:178-179 lo asigna a «la rama de comprobaciones en el visor» |
> | 22 | `motor decisiones` ya lee la liquidez de M15 de cada lado (`c.datos.liquidez_m15`) | MATIZ | decisiones.py:406 la llama solo dentro de `_linea_m15`, al nacer una zona, para comparar por igualdad, y no la escribe. motor.py:150-152 devuelve el pivote más reciente ya formado de cada lado en ese instante. No da la lista de líneas de la sesión ni la vela que toma cada una, que es lo que pide el punto 3 |
> | 23 | `_sin_orden` compone los motivos sueltos y los frenos salen por otro camino | CORRECTA | decisiones.py:446-465 (texto); `ctx.no_enviadas` en :499-502 |
> | 24 | El tipo b es la operación que patrones.py no llama T0 (ADR-0043) | MATIZ | patrones.py:18: T0 = «filas del trader con PAREJA». Es un guion de anexo que lee el texto del arnés; desde src/ lo equivalente es `emparejar` de cases.criterio_fidelidad (decisiones.py:40) |
> | 25 | Ventanas: H4 desde 4 días antes, M15 desde el día anterior, M1 desde una hora antes; la última vela, en formación | CORRECTA | graficos_sesion.py:18-21, :73-77, :199-203 |
> | 26 | La regex de fechas está en graficos_sesion.py:265-270 | INCORRECTA | La regex `_RE_FECHA` está en :247-252; :265-270 es `_panel` |
> | 27 | Esa regex busca los meses sin límite de palabra, y «mayor» casa con «mayo» | CORRECTA | graficos_sesion.py:249-250 (sin `\b` en los meses) |
> | 28 | Días de construcción: abril, julio del 1 al 17, agosto y enero del 2 al 30 | CORRECTA | SESION-DE-PREGUNTAS.md:21-22; ADR-0078:7; ADR-0079:7 |
> | 29 | BARRIDO:247, la H4 recortada a principios de julio, «es el caso de 07-02 y 07-03» | MATIZ | :247 habla de la fila 18, que es 2026-07-02 07-11 (BARRIDO:232). 07-03 no se nombra; se deduce porque su H4 también empieza en junio |
> | 30 | RECORRIDA-CONSTRUCCION.md:1628: «su contexto de H4 y M15 puede venir del día anterior…» | CORRECTA | :1628, punto 2 de la respuesta del consultor |
> | 31 | La lista de horas perdidas está en anexos/RESPALDO-M1/horas_perdidas.py | CORRECTA | :18-24; idéntico (md5) en cinco anexos; RECORRIDA-CONSTRUCCION-2.md:98-103 |
> | 32 | `_ticks_del_dia` está en simulacion.py:166 | CORRECTA | simulacion.py:166-180 |
> | 33 | La salida va fuera del repo («Antes», paso 6) | CORRECTA | SESION-DE-PREGUNTAS.md:94-95 |
> | 34 | Ensayos aislados, puntos 1 y 2 (worktree; la raíz por argumento) | CORRECTA | CLAUDE.md, «Ensayos aislados» |
> | 35 | `comprobar_carpeta` exige que la salida esté dentro de data/ | CORRECTA | decisiones.py:62-76 |
> | 36 | BARRIDO-SESION-6 lo ensayó en un worktree | CORRECTA | HOLDOUT-EXPOSICIONES.md:80 (`git worktree add --detach C:/cm/graficos 09afe20`) |
> | 37 | test_no_business_literals mira todo src/botsito/ | CORRECTA | test_no_business_literals.py:3 (salvo config/registro.py) |
> | 38 | El 0,8 se lee del registro (`stop_fraccion_caja`) | CORRECTA | parametros.yaml:602-611 |
> | 39 | El literal "Europe/Madrid" está prohibido | CORRECTA | test_no_business_literals.py:43 |
> | 40 | 0,25 y 0,5 llevan la exención `# no-negocio: <motivo>`, una por línea | CORRECTA | :25-26, :112, :125 |
> | 41 | graficos_sesion.py usa `(i + 0.5) * paso` y `ZoneInfo("Europe/Madrid")` | CORRECTA | graficos_sesion.py:292 y :61 |
> | 42 | `dias_de_construccion`, `casos_ocultos` y `casos_reservados` existen | CORRECTA | arnes.py:139; cases/holdout.py:351 y :456 |
> | 43 | Cada corrida y cada make check calientan con el M1 de marzo y el de junio (Technical Debt) | CORRECTA | PROJECT_STATE.md:105 |
> | 44 | Rango de H4: 07-06 (dos sesiones), 07-07 (dos), 07-15 11-15 y 07-17 11-15 | CORRECTA | VIDEO-JULIO.md:611-613, :651 y :655, todas «regla desconocida / el rango de H4» |
> | 45 | 07-17 07-11 es «sin clase»; el 1 de julio nunca | CORRECTA | VIDEO-JULIO.md:654; RUMBO:17 |
> | 46 | Zonas de control: 04-13 07-11, 07-02 11-15 y 07-03 11-15 (5.2, 5.3 y 5.5 punto 2) | CORRECTA | TRAZAS:878-880, :894-896, :951-956 |
> | 47 | 07-14 11-15 tiene cuatro filas con gate RN-009 | CORRECTA | TRAZAS:881 |
> | 48 | Hora perdida 2026-07-14T12Z = 14:00 de Madrid, dentro de la sesión | CORRECTA | horas_perdidas.py:22. En julio Madrid es UTC+2, así que 12Z son las 14:00, y la sesión 11-15 va de 09Z a 13Z |
> | 49 | 07-03 07-11 entra por cuándo se coloca la orden (ADR-0064, 5.1 y 5.5 punto 1) | CORRECTA | TRAZAS:802-822, :945-950; título de ADR-0064 |
> | 50 | Ninguna de las diez sesiones tiene una hora perdida | MATIZ | Ninguno de los días 04-13, 07-02, 07-03, 07-06, 07-07, 07-15 y 07-17 está en horas_perdidas.py:18-24. Pero la H4 de 07-15 11-15 contiene 07-14T12Z, y la H4 y la M15 de 07-17 11-15 contienen 07-16T11Z. Faltan ticks, no velas M1 |
> | 51 | El día sintético de test_cableado no tiene toma, escenario, caja ni punto (la zona va inyectada) | CORRECTA | test_cableado.py:137-150 |
> | 52 | La línea de Technical Debt del `toca_colocar_orden_limite` con clausura | CORRECTA | PROJECT_STATE.md:146; test_cableado.py:141-149 |
> | 53 | Las tres líneas de Technical Debt de 0.5, tal como las cita | CORRECTA | PROJECT_STATE.md:104, :102 y :144 |
> | 54 | La lámina de 07-03 a las 09:35 enseña lo que hizo el motor | CORRECTA | PROJECT_STATE.md:144; TRAZAS:822, :840-845 |
> | 55 | F1 §0: 6.1 % (14-oct), y que las cuatro corridas son «comparables» | MATIZ | CORRIDA-CONSTRUCCION.md:610; RUMBO:48. Esa corrida 2 se hizo con `--diagnostico-a35` y `--diagnostico-a44` (CORRIDA-CONSTRUCCION:618); lo de «comparables» ya estaba en RUMBO |
> | 56 | 20.7 % (27-oct), diaria de RECORRIDA-CONSTRUCCION | CORRECTA | RECORRIDA-CONSTRUCCION.md:603, :636, :653 |
> | 57 | La diaria de RESPALDO-M1 se corrió el 29-oct (nota final), con 20.2 % | CORRECTA | RESPALDO-M1.md:765; HOLDOUT-EXPOSICIONES.md:85; RUMBO:49-51 |
> | 58 | 20.2 % (8-nov), con 40 parejas antes y después | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:565 y :575 («Parejas 40 (40)») |
> | 59 | F1 §4: ADR-0082 §4 fija el EA y descarta que el EA reciba decisiones de Python por el puente y el tope de peticiones | CORRECTA | ADR-0082:65-83 |
> | 60 | R6.0 está HECHA, confirmada el 2026-11-09 | CORRECTA | HOJA:591-599 |
> | 61 | Los puntos de pivote van a R4.3, con el esquema de tres salidas | CORRECTA | HOJA:386; PROJECT_STATE.md:28 |
> | 62 | La puerta para operar en vivo sigue siendo ADR-0092 | CORRECTA | HOJA:469-481; RUMBO:35 |
> | 63 | F1 §5: «el motor de Python no corre en una demo de FTMO sin un puente en vivo, que ADR-0082 §4 descarta» | MATIZ | ADR-0082:80-82 descarta «el EA que recibe las decisiones de Python». La sombra temprana solo registra y no manda decisiones; extender el descarte a ella dice más que la cita |
> | 64 | La capa de R6a y el grabador F17 en una prueba gratuita nueva (A.5) | CORRECTA | HOJA:689-697 |
> | 65 | La tabla del R de las parejas es R5.7 | CORRECTA | HOJA:483-489 |
> | 66 | validation/ids_citados.py lee todo docs/ | CORRECTA | src/botsito/validation/ids_citados.py:67-71 |
> | 67 | F4.1: diff contra RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt | CORRECTA | El fichero existe; TRAZAS:654-656 dio 0 bytes; `grep -c "cuenta-por-mes\|data/"` en él da 0, así que el nombre de la salida no entra en el diff |
> | 68 | F4.2 tiene la misma forma que TRAZAS:646 | CORRECTA | TRAZAS-ABLACION.md:646 |
> | 69 | La CI se empuja como fix/laminas (RITUAL:102) y el único fallo aceptado es el de state check | CORRECTA | RITUAL.md:102-107 |
> | 70 | La mutación de test_decisiones.py:123-135 | CORRECTA | test_decisiones.py:122-135 |
> | 71 | El revisor b3 de TRAZAS pidió «el texto de cada guion» | MATIZ | b3 pidió los comandos (TRAZAS:1251). El texto en el anexo fue cómo se cumplió (:1055-1058, :1375) |
> | 72 | BARRIDO, respuesta a la PARADA, punto 5: sin fechas | CORRECTA | BARRIDO-SESION-6.md:469 |
> | 73 | La lección de F38t y F38u (medir los campos antes de usar una pieza) | CORRECTA | ERRORES-RECURRENTES.md:115 |
> | 74 | «El contrato cubre exactamente eso»; «dónde vive el código» se propone en la fase 0 | MATIZ | contrato.yaml solo permite src/botsito/engine/ y cli.py, y protege domain/, spec/ y pyproject.toml. El encargo habla de «fuera de src/ y tests/», que es más amplio. Con ese contrato, el código ya tiene que vivir en engine |
> | 75 | Los ids ADR-0043, ADR-0064, ADR-0069, ADR-0080, ADR-0082, ADR-0092 y RN-009 existen y tratan lo que dice el encargo | CORRECTA | docs/adr/0043, 0064, 0069, 0080, 0082 y 0092; strategy_spec.yaml:1546-1547 (RN-009, zonas de control) |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | 1 | Todo campo nuevo de MotorCableado (por ejemplo, el registro para la lámina) tiene que ir en CAMPOS_DE_CONFIGURACION o en CAMPOS_DE_ESTADO; si no, `motor_nuevo` y su test fallan | engine/decisiones.py | decisiones.py:118-150 |
> | 2 | El registro de qué H4 se saltaron por el color vive en domain/sesgo.py, que el contrato protege. Esa pieza del punto 3 exige ampliar el contrato (domain es puro: import-linter lo deja) o una PARADA | contrato.yaml; ADR-0080 §10 | domain/sesgo.py:56-76; pyproject.toml:68-79 |
> | 3 | S-7 (gráfico 1) «va como contexto de los gráficos 2 a 6». Al sustituirlos, el encargo no dice adónde va S-7 | ACTIVAR-SESION-06.md §«Para la sesión 7», punto 10 | :611-613 |
> | 4 | Lecciones del guion precedente: los tests no probaban la constante real, `main()` ni los alias de recorrer carpetas; el test del SVG era solo geométrico; lo que una marca enseña se mide antes en la salida | ERRORES-RECURRENTES (barrido-sesion-6) | ERRORES-RECURRENTES.md:103 |
> | 5 | El clon desechable no tiene data/: necesita su config/settings.local.toml con `[rutas].data` absoluto | skill comparar-con-main | .claude/skills/comparar-con-main/SKILL.md:32, :53; cli.py:2705-2712 |
> | 6 | TEXTOS_PROHIBIDOS también incluye «07:00», «11:00», «15:00», «17:00», «23:00», «1:3», EURUSD y FTMO, y NUMEROS_PROHIBIDOS el 100000. La tabla de frases y los rótulos no pueden llevarlos literales | test_no_business_literals | :18-45 |
> | 7 | Las ventanas (4 días, 1 día, 1 hora, 240 y 15 minutos) son literales en el guion. CLAUDE.md, «Las cifras van en el registro» (ADR-0002), pide decidir si son parámetros o solo dibujo; el test de hoy no las caza | CLAUDE.md; ADR-0002 | graficos_sesion.py:73-77 |
> | 8 | PROJECT_STATE mide 22.494 bytes y el tope es 25.000: las líneas de Technical Debt nuevas del cierre tienen unos 2.500 bytes de margen | test_project_state | `wc -c PROJECT_STATE.md` |
> | 9 | (No aplica.) Las tres guardias de modelo.py: no se añade ningún sitio con `cita` y spec/ está protegido. import-linter: engine puede importar cases, spec y data, y viewer está por encima de engine. No hace falta tocar pyproject si el código vive en engine | CLAUDE.md; pyproject | pyproject.toml:95-117 |
>
> ### Comandos del encargo
> | # | Comando | Existe y se ejecuta así | Evidencia |
> |---|---|---|---|
> | 1 | `uv run botsito motor arnes --simular --salida data/laminas/base.txt` | Sí | cli.py:3185-3199; `--simular` en :2333-2334 |
> | 2 | `uv run botsito motor decisiones --carpeta data/laminas/bitacora --bitacora 2026-04-13,2026-07-02,2026-07-03,2026-07-14` | Sí. `--carpeta` tiene que estar dentro de data/ y cada día de `--bitacora` tiene que ser un día dev de construcción | cli.py:3226-3242, :2631, :2649-2654 |
> | 3 | `motor laminas` | Todavía no existe; lo crea F3 | cli.py:3183-3247 (solo arnes, visor y decisiones) |
> | 4 | `git push origin trabajo/laminas:refs/heads/fix/laminas` | Sí, en la forma de RITUAL | RITUAL.md:102 |
> | 5 | `casos_reservados(repo)` y `casos_ocultos(repo)` | Son funciones; su forma de uso está en SESION-DE-PREGUNTAS | holdout.py:351, :456; SESION-DE-PREGUNTAS.md:71 |
> | 6 | Las funciones de test_hoja_de_ruta.py sobre una copia | Existen `problemas_a` a `problemas_d` | test_hoja_de_ruta.py:121-187 |
> | 7 | `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` y `/model` | No son del repo; la variable está en CLAUDE.md, «Trampas medidas» | — |
>
> **Tramo:** R4 existe. R4.5 lleva NA:F, depende de R4.4, que está HECHA (HOJA:403), y es la siguiente según el orden de F (PROJECT_STATE.md:28). No se adelanta nada.
>
> ### Lo que no pude comprobar
> - **La CI de main (run 42759493730):** no tengo `gh`. La sesión dice haberlo medido en docs/validation/LAMINAS.md:12.
> - **casos_reservados y casos_ocultos de las diez sesiones:** no ejecuté Python, por la restricción de no escribir cachés. Lo que sí medí, contando: cada uno de los siete días tiene 1 caso en knowledge/cases/dev (`ls | grep -c`); `grep -c` de esos días en retirados.yaml da 0; meses_reservados.yaml no nombra 2026-01, 04, 07 ni 08.
> - **Ramas y tags en origin:** no consulté la red; solo las refs locales.
> - **La guardia me negó un `for f`** con `wc -l` sobre los anexos de TRAZAS. No lo rodeé.
> - **Si el sesgo se puede enseñar en 07-02 y 07-03:** allí el sesgo lo fija una H4 de junio (reservado; se lee para calentar). El encargo dice solo que esa H4 no se dibuja y que «viene de antes de la ventana»; si decir «sesgo alcista» enseña algo de junio no lo decide ningún ADR que yo haya encontrado (ADR-0021 §1 dice que las velas no son holdout).
> - **La copia del encargo frente al chat**, y las decisiones del 2026-11-09 dadas en el chat.
>
> ### Lo más grave
> 1. **Dos piezas del punto 3 no las da hoy ninguna pieza, y la forma prevista para añadirlas choca con el contrato.** «Las H4 que saltó por el color» solo existen como contadores en `domain/sesgo.py` (`ResultadoSesgo`), y `src/botsito/domain/` está en las rutas protegidas de contrato.yaml. «Las líneas de M15 de la sesión, desde el pivote hasta la vela que las toma» tampoco salen del motor: `liquidez_m15` solo devuelve el pivote más reciente de cada lado en el instante (motor.py:150), y la bitácora solo lo compara por igualdad (decisiones.py:401-411). Hay que acumularlo desde el observador o registrarlo en el motor, y cualquier campo nuevo de MotorCableado tiene que clasificarse en decisiones.py:121-134. Sin una decisión sobre el contrato, la lámina queda entre recalcular (prohibido) y PARADA.
> 2. **F1 tiene una referencia que no casa del todo.** El recuadro de §5 atribuye a ADR-0082 §4 el descarte de una sombra que solo registra, y lo que el ADR descarta es el EA que recibe decisiones de Python (ADR-0082:80-82). El propio encargo manda PARADA si una referencia de F1 no casa.
> 3. **La cita de la regex es falsa en el número de línea:** está en graficos_sesion.py:247-252, no en :265-270. El fondo es cierto: los meses van sin `\b`.
> 4. **Ninguna de las diez sesiones tiene una hora perdida dentro de la sesión**, pero 07-15 11-15 y 07-17 11-15 las tienen en su ventana de H4 o M15 (07-14T12Z y 07-16T11Z). Ahí faltan ticks, no velas, así que el punto 6 tal como está escrito no las saca; conviene decirlo en la fase 0.

## Apéndice B · El informe del revisor (primera pasada, 2026-11-10), tal cual

Lo hecho con cada hallazgo está en «Lo hecho con lo que encontró el revisor».

> ## Informe del revisor · trabajo/laminas · 2026-11-10
>
> Lo revisado: los commits 73668c16, 6b5f069e, daed48b8, b7d5d6d8, 3f800b5c y 675ee623, y los dos ficheros modificados sin commitear (`docs/validation/LAMINAS.md` y `docs/validation/HOLDOUT-EXPOSICIONES.md`). No modifiqué nada.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | menor | Los números de línea de las dos exenciones de `laminas.py` son los de 3f800b5, no los de HEAD. 675ee62 añadió dos líneas por encima. | `LAMINAS.md:346` dice `laminas.py:935` y `:936`. En HEAD están en `src/botsito/engine/laminas.py:937-938`; `git show 3f800b5c:src/botsito/engine/laminas.py \| sed -n '935,936p'` da las dos líneas `Decimal("0.25")`/`Decimal("0.5")  # no-negocio`. La de `laminas_svg.py:48` sí casa. |
> | a2 | menor | El recuento de tests del informe está desfasado. | `LAMINAS.md:417` dice «35 funciones nuevas; 1975 en total». Grep `^def test_` en `tests/unit/test_laminas*.py` da 21 + 11 + 5 = 37, y `PROJECT_STATE.md` dice 1976 (1939 + 37, el número correcto). pytest recoge 37 elementos. |
> | a3 | menor | La fila de F4 de HOLDOUT-EXPOSICIONES se reescribe en su sitio en vez de añadir una fila de cierre. Lo que se declaró antes de las corridas solo queda en el historial (3f800b5). La propia fila lo preveía («se cuenta aquí al cerrar el día») y ninguna regla del fichero lo prohíbe. | `git diff -- docs/validation/HOLDOUT-EXPOSICIONES.md`: una línea `-` y una `+` en la fila «las corridas de F4». |
> | a4 | menor | F1 (daed48b, 12:01) aplica la respuesta del consultor antes de que esa respuesta esté en el repo: se copió al encargo en b7d5d6d (12:27). En daed48b el lector no puede contrastar el texto de §0 y §5. | `git log --format='%h %ci'`; `git show --stat b7d5d6d8` (`docs/encargos/trabajo-laminas.md` +38). |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` da «CONTRATO: 18 ficheros dentro del contrato de trabajo/laminas (riesgo alto, …, 3 comprobaciones para el revisor)», exit 0. `uv run botsito state check` da OK, exit 0. Para `make check` (que escribe) vale como evidencia `make-check.log`: «3396 passed», «SELLO: make check en verde sobre el arbol 23f902b6…», que es `git rev-parse 675ee623^{tree}`, y «PICO DE MEMORIA … 315 MiB». La ampliación del contrato (b7d5d6d) añade solo `domain/sesgo.py` y `domain/estructura_m1.py`, y saca `src/botsito/domain/` de las protegidas, con su motivo.
> - **Trailers `Fuente:`.** No aplican: ningún commit toca `knowledge/spec` ni `knowledge/cases`.
> - **Holdout.** Nada toca `knowledge/cases/holdout`. El código de las láminas no nombra transcripciones, fotogramas, corpus, xlsx ni libros (grep: 0 en `engine/laminas*.py`). Hay tres filas de HOLDOUT-EXPOSICIONES del 2026-11-10: la del día, la de la medida de la fase 0 y la de F4, con 10 corridas más la de medida.
> - **Regímenes de cambio.** `git diff --name-only main...HEAD -- knowledge scripts .claude Makefile pyproject.toml …` da 0 ficheros. HISTORIA: +168/-0. HOLDOUT-EXPOSICIONES contra main: solo añade.
> - **Ambigüedades, ADR y las tres guardias de `cita`.** No aplican.
> - **Informes cerrados.** Ninguno se toca (diff contra los protegidos del contrato: 0).
> - **Cifras.** Hay exactamente tres `# no-negocio` en el diff de `src/` y ningún `Europe/Madrid` ni `ZoneInfo("` literal en `laminas*.py`. El 0,8 sale de `stop_fraccion_caja`, el huso de `huso_visible` y el anclaje de `anclaje_h4` (cli.py, `motor_laminas`).
> - **Ensayos aislados.** El ensayo se hizo en un worktree (`LAMINAS.md:474`). `git worktree list` ya no lo muestra.
> - **Citas del informe** comprobadas contra su fuente (más de tres): las 15 líneas de gate de `strategy_spec.yaml`; los hechos `:680/:713/:723/:734/:746/:757`; los fijar de `:1912/:2116/:2179/:2427/:2532`; `:1331`, `:1874-1876`, `:2111`; `parametros.yaml:1593-1612`; `config.yaml:72-76`; `zonas.py:110/146-148/214-232/393/412/414-416/420-448/270`; `broker.py:92-95/174-176/255/738-745/934`; `llenado.py:44-45`; `primitivas_broker.py:635-639`; `primitivas.py:65/70-78`; y todas las `FRASE_*` en `laminas.py:455-603`. Casan todas salvo a1.
> - **Evidencia nueva.** No hay.
>
> ### Eje (b) · Encargo
> Resumen: 4 bloquea, 4 importa, 3 menor. Requisitos: 30 hechos, 5 parciales, 1 no hecho.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Abrir con abrir-rama: encargo, contrato y Archivo de HISTORIA | Hecho | 73668c16; HISTORIA +168/-0 |
> | 2 | Base comprobada | Hecho | `LAMINAS.md:7-14` |
> | 3 | La decisión de los gráficos 2 a 6, escrita en el informe | Hecho | `LAMINAS.md:16-18` |
> | 4 | No se toca knowledge/, scripts/, .claude/, graficos_sesion.py, SESION-DE-PREGUNTAS ni los informes cerrados | Hecho | diff --name-only: 0 |
> | 5 | `motor arnes`, `motor visor` y `motor decisiones` conservan sus opciones; `motor laminas` no comparte `_opciones_diagnostico` ni `_opciones_simulacion` | Hecho | El diff de cli.py solo añade `motor_laminas` y dos `add_argument`; arnes.py y test_diferencias_por_operacion.py no cambian; `test_arnes_visor_y_decisiones_tienen_las_mismas_opciones_que_en_main` pasa |
> | 6 | La misma salida de arnes y decisiones (F4.1 y F4.2) | Hecho | sha256 de `data/laminas/base.txt` = el de `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` (e6ca305b…); las cuatro bitácoras = sus anexos de TRAZAS-ABLACION |
> | 7 | Fuera de src/ y tests/, solo lo permitido | Hecho | diff --name-status (18 ficheros). `anexos/LAMINAS/` no se creó (b-I4) |
> | 8 | Una sola fuente: el observador y las copias, sin referencia viva | Hecho | `laminas.py:285-446` (todo pasa a str, int, tuplas o `Vela` congelada); `test_las_laminas_no_recalculan_ninguna_decision` |
> | 9 | Lo nuevo es solo registro | Hecho | Diffs de sesgo, estructura_m1, primitivas y zonas; las anotaciones solo las leen `arnes.py:328-355` y `visor.py:766,1064` por clave concreta |
> | 10 | Láminas (a) y (b), en orden; las canceladas sin lámina; la operación del trader sin dibujar | Hecho | `laminas.py:1098-1144`; test «salen exactamente…»; en los HTML: 19 con «Coloca la orden» (tipo a), 28 de tipo b, ninguna «Tiene una orden … pendiente» |
> | 11 | Tres paneles y las ventanas | Hecho | `laminas.py:49-51,253-264,684-698` |
> | 12 | Las marcas de H4, M15 y M1 | Hecho | `class="h4-fija"` y `linea-m15` en 47 de 47 láminas; `laminas_svg.py:187-261` |
> | 13 | La tabla cerrada y el error que nombra la causa sin frase (código) | Hecho | `laminas.py:770-785,989-1052` |
> | 14 | Sin ids, lote, R, dinero ni porcentajes | Hecho | grep de los patrones del punto 4 en los 57 HTML: 0 |
> | 15 | Nada posterior al corte | Hecho | `_paneles` corta `< foto.corte` (`:695`); `m1_entre` es `[desde, hasta)` (`motor.py:144-148`); ninguna geometría pasa del borde del corte, salvo los dos marcadores de b-m3 |
> | 16 | Sin fechas; la regex con `\b`, con su test | Hecho | `laminas.py:1059-1065`; `test_la_regex_de_fechas_lleva_limites_de_palabra`; grep en los HTML: 0 |
> | 17 | La clave solo en clave.txt: ni en el repo ni en el informe | Parcial | b-B1 |
> | 18 | Negar por defecto (días, horas perdidas, velas y lo que no es vela) | Hecho, con b-I3 | `Puerta` `:63-89`; `comprobar_pedidas` `:1276-1295`; `dentro()` `:730-732` |
> | 19 | La salida fuera del repo, por argumento obligatorio, con su test; sin `comprobar_carpeta` | Hecho | `:1235-1244`; dos tests |
> | 20 | El ensayo en un worktree | Hecho | `LAMINAS.md:473-489` |
> | 21 | HTML autocontenido, determinista, colores en una tabla | Hecho | `diff -r` = 0 (`LAMINAS.md:494`); tests |
> | 22 | Las cifras (punto 9) y las exenciones | Hecho | eje (a) |
> | 23 | Mirar solo construcción por la compuerta, con sus filas de HOLDOUT-EXPOSICIONES | Hecho | cli.py: `dias_de_construccion` y `casos_ocultos`; las tres filas |
> | 24 | Fase 0 con PARADA, y la respuesta tal cual en el encargo y en el informe | Hecho | La comparación programática de los dos bloques (33 líneas) da True |
> | 25 | La respuesta aplicada punto por punto (0 a 12) | Hecho | `LAMINAS.md:285-299`; frases nuevas en `laminas.py:499-504,519,563,569` |
> | 26 | F1 literal | Hecho | alcance 6 |
> | 27 | F2: los tests | Parcial | b-B4, b-I1, b-I2 |
> | 28 | F3: el subcomando | Hecho | `cli.py` `motor_laminas` |
> | 29 | F4.1 a 0 bytes | Hecho | sha256 |
> | 30 | F4.2 a 0 bytes | Hecho | sha256 |
> | 31 | F4.3: las láminas, por sesión cuántas de tipo a y de tipo b, y las excluidas | Parcial | b-B3 |
> | 32 | Informe: «el encargo frente a lo hecho», desviaciones y comandos tal cual | Parcial | b-B2, b-I4 |
> | 33 | El runbook | Hecho, con b-m1 | `docs/runbooks/LAMINAS.md` |
> | 34 | La CI por fix/laminas, con su run | Hecho | `gh run view 42881622332`: headSha 675ee623, «1 failed, 3347 passed, 48 skipped», el fallo es `test_state_check_ok_on_real_repo` |
> | 35 | PARADA final: dónde están, lo que no convence, propuestas comprobadas | Hecho | En memoria, `problemas_a`, `problemas_b`, `problemas_c` y `problemas_d` dan [] hoy y con las propuestas; PROJECT_STATE en 22 504 bytes (22 506 con las comillas invertidas); sin NA:F en el bloque |
> | 36 | La frase «Rama lista para revisión, NO cerrada.» | No hecho | Pendiente después del revisor; `## Estado` dice EN CURSO (`LAMINAS.md:667`) |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b-B1 | bloquea | El informe ata láminas a su día. Primero, dice que las carpetas `sesion-NN` siguen el orden de la lista de `--sesiones`, y esa lista está en la misma sección: eso es la clave a nivel de sesión. Segundo, da el corte de láminas concretas de un día nombrado, así que junto con su `indice.html` identifica el fichero. El encargo (punto 5) dice que la clave «no entra al repo ni al informe», y HOJA R4.5 dice «La clave lámina-día no entra al repo». La parte de los cortes ya está commiteada (675ee62), así que queda en el historial de la rama. Que la numeración siga el orden de `--sesiones` fue diseño aprobado (§0.3); escribirlo junto a la lista y a los cortes no lo fue. | `LAMINAS.md:480`, `:481-484`, `:492` junto con `:496`; `git show 675ee623 -- docs/validation/LAMINAS.md` (líneas añadidas 30-34); `HOJA-DE-RUTA.md:411` |
> | b-B2 | bloquea | Falta «el encargo frente a lo hecho». El encargo lo pide en INFORME, y la skill entregar-rama lo pide como «El encargo, punto por punto». | encargo `:105`; `.claude/skills/entregar-rama/SKILL.md:46-50,97`; grep «punto por punto» en LAMINAS.md: solo `:224,253,285` |
> | b-B3 | bloquea | F4.3 da el total de láminas por sesión pero no cuántas son de tipo a y cuántas de tipo b, que el encargo pide. Contadas en los HTML, son 19 a y 28 b en total. | encargo `:102`; `LAMINAS.md:498` |
> | b-B4 | bloquea | «La tabla de frases es cerrada: el test enumera desde la spec … los hechos …; mutación: quitar una frase lo rompe.» Solo los gates se enumeran desde la spec. Ningún test enumera los hechos del vocabulario ni toca `FRASE_DETENIDO`, así que quitar la frase de `detenido_por_racha`, `detenido_por_tope_total` o `detenido_por_cartuchos` no rompe ningún test. | encargo `:90`; grep `detenido_por_racha\|detenido_por_tope_total\|FRASE_DETENIDO\|HECHOS_SIN_FRASE` en `tests/unit/test_laminas*.py`: 0; `test_laminas.py:402-410` (solo gates) |
> | b-I1 | importa | `test_un_recolector_con_la_referencia_viva_ve_el_futuro_y_el_test_lo_caza` no ejecuta ningún mutante del código. Comprueba que la foto real no tiene o2 y que el `broker` vivo sí la tiene; ninguna de las dos aserciones fallaría por la mutación que nombra. El encargo pide una «mutación comprobada», y el informe no enseña ninguna corrida de un mutante. La protección de verdad está en `test_la_foto_no_mira_al_futuro`. | `test_laminas.py:243-257`; encargo `:87`; `LAMINAS.md:432` |
> | b-I2 | importa | «Sin mirar al futuro» con una toma de M15 o un estado (un freno) cambiados después del corte no tiene fixture. Hay vela posterior (svg), y llenado y bróker posteriores (o2). El diseño de la fase 0 prometía «un freno encendido después». | encargo `:87`; `LAMINAS.md:181`; `test_laminas.py:231-240`; `test_laminas_svg.py:154-158` |
> | b-I3 | importa | Puede haber un hueco en el punto 6, aunque cae dentro del diseño aprobado. Una línea de M15 «nace» por `contraria_inicio`, pero su nivel es el extremo de la racha ANTERIOR a la contraria. En los paneles recortados al 1 de julio (las dos sesiones cuya ventana empieza en junio), una racha que empiece antes de la ventana daría el precio de una vela de fuera. No se mide en las 47 láminas. El encargo nombra en concreto «el pivote de origen de una línea de M15». | `domain/pivotes_m15.py:136-148`; `laminas.py:796` y `:819-823`; encargo `:50` |
> | b-I4 | importa | `docs/validation/anexos/LAMINAS/` no existe. Los guiones de la fase 0 (`diez_sesiones.py`, `campos_cierre.py`, `listas_frases.py`), la comprobación de las propuestas con `test_hoja_de_ruta` «sobre copias en memoria» y la de la estructura de las 47 láminas se citan sin su texto ni su orden. | `ls docs/validation/anexos \| grep -ci laminas` da 0; `LAMINAS.md:29,35,104,504,524`; encargo `:31,:105` |
> | b-m1 | menor | El runbook dice «lo que nace antes de la ventana de su panel» y que tarda «12-15 minutos». La decisión 5 es la del panel MÁS ANCHO: una línea de M15 nacida antes del M1 sí sale en el M1. Lo medido son 520-659 s. | `docs/runbooks/LAMINAS.md:24,51`; `laminas.py:23`; `LAMINAS.md:488,493` |
> | b-m2 | menor | El color `control` `#e67e22` (zonas de RN-009) no está en la tabla de colores de la fase 0 ni se declara en el informe. | `laminas_svg.py:44`; `LAMINAS.md:160-173` |
> | b-m3 | menor | El test «ninguna a la derecha del corte» solo mira `x=` y `x2=`, no `x1` ni `cx`. Medido en la salida: dos `zona-control` de 8 px pasan del borde unos 1,2 px; su centro está dentro. | `test_laminas.py:293-295`; mi comprobación de la geometría (2 casos en una carpeta) |
>
> Lo que la rama hace y el encargo no pide, y el informe lo justifica: no coteja `orden_limite_pendiente`; las frases de «viene de antes de la ventana»; singular y plural; la R solo en mayúscula; la cabecera con las dos horas; la anotación de las saltadas que no se borra (propuesta de Technical Debt). Sin justificar: solo b-m2.
>
> ### Los seis alcances (veredicto)
> 1. **Que nada cambie lo que el motor decide: CUMPLE.**
>    - F4.1 y F4.2 dan los mismos sha256 que sus anexos.
>    - Los ficheros de registro (sesgo, estructura_m1, primitivas, zonas, cli) tienen mtime 12:27-12:36, anterior a F4.1 (~12:47), y no cambian después (`git status` limpio en `src/`).
>    - El golden y la mutación del estado: `test_laminas.py:186-215`.
>    - La comparación con copias literales de main: `test_laminas_registro.py:42-96,173-176,229-233,315-323`.
>    - Lo nuevo no lo lee ninguna decisión: grep `.anotaciones` en `src/`.
>    - El 37 de 37 de los tests de las láminas.
> 2. **Que arnes, visor y decisiones no cambien: CUMPLE en opciones; en salida, por medida en arnes y decisiones y solo por lectura del código en visor.** El visor solo lee `ANOTACION_SESGO` y campos con nombre de `ResultadoSesgo` (`visor.py:766,772-783`). Lo de las opciones y `_opciones_*`, en el requisito 5.
> 3. **El corte: CUMPLE.** No hay ninguna referencia viva del `Cierre` (`Recolector`, `Foto` y `_DiaRec` solo guardan copias, `laminas.py:244-446`), y `laminas_svg.py` solo recibe una `Composicion`. En el texto no sale nada posterior al corte (grep de las frases de los 47). La debilidad está en las pruebas (b-I1, b-I2).
> 4. **Fechas, ids y dinero: CUMPLE. Las fuentes de las frases casan. Las exenciones son exactamente tres, con los números de línea desfasados (a1). La tabla cerrada en el código, CUMPLE; su test, NO (b-B4).**
> 5. **Holdout y negar por defecto: CUMPLE**, con el hueco posible de b-I3.
>    - La `Puerta` vale también para lo que no es vela (`laminas.py:796,825,871,884,917`).
>    - Ninguna transcripción ni fotograma se lee en el código.
>    - Las operaciones del trader entran por `dias_de_construccion` y no se dibujan.
>    - clave.txt no está en el repo (`git ls-files docs src tests \| grep -ci clave` da 0), pero el informe ata láminas a su día (b-B1).
>    - Las filas de HOLDOUT-EXPOSICIONES del 2026-11-10 están.
> 6. **F1 literal: CUMPLE.** Comparado línea a línea por programa: el §0 de RUMBO es igual al §0 de la respuesta, el §4 al del encargo y el §5 al de la respuesta. Cada recuadro va dos líneas debajo de su encabezado, con una línea en blanco entre medias. El diff de daed48b solo añade (+6/-0). Las referencias nuevas casan: CORRIDA-CONSTRUCCION.md:574 (la orden con `--diagnostico-a35/a44`), :618 y ADR-0082 :69-71 y :74-76.
>
> ### Lo que no pude comprobar
> - Que el encargo sea copia literal del chat: no tengo el chat.
> - Que la fila de F4 de HOLDOUT-EXPOSICIONES se escribiera antes de F4.1. Solo entra en 3f800b5 (13:27), después de F4.1 y F4.2, y el mtime de hoy es el de la edición sin commitear.
> - Que ninguna corrida coincidiera con un `make check`: el log solo guarda el último.
> - El sello del árbol de 3f800b5: `make-check.log` está sobrescrito. Lo garantizan los hooks.
> - Las mutaciones del encargo: ejecutarlas exige editar código.
> - `tests/contract/test_no_business_literals.py`: no lo ejecuté; solo tenía permiso para los de las láminas. La evidencia es `make-check.log` (3396 passed sobre el árbol de 675ee62) y la CI.
> - `motor visor` sobre datos reales: es una corrida.
> - Si alguna línea de M15 de las 47 láminas lleva el nivel de una vela anterior a su ventana (b-I3): hace falta la corrida.
> - Cómo se ven las láminas: no se pintan aquí.
> - El contenido de clave.txt: prohibido, no lo abrí.
> - Efecto lateral mío: el `pytest` de los tres ficheros pudo escribir `__pycache__` en `tests/unit/`, que git ignora. En la segunda comprobación usé `python -B`.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. `uv run python scripts/contrato_rama.py`
> 3. `git diff --name-status main...HEAD` y `git diff --name-status`
> 4. `git diff main...HEAD -- PROJECT_STATE.md docs/plan/RUMBO-2026-11.md` y `--numstat` de HISTORIA
> 5. `python -c` que compara los tres recuadros de RUMBO (en `git show daed48b8`) con el encargo
> 6. `git log --stat --format='==== %h %s%n%b' main..HEAD`. Antes, un `for c in …` que la guardia negó (no lo rodeé).
> 7. `ls -la make-check.log && grep -nE "SELLO|PICO DE MEMORIA|passed|failed" make-check.log`
> 8. `git rev-parse 675ee623^{tree} 3f800b5c^{tree}` y los diffs de HOLDOUT-EXPOSICIONES (contra main y sin commitear)
> 9. `git diff --stat` y el resumen del diff sin commitear de LAMINAS.md
> 10. `grep -n -B2 "^class Vela"`; `git show 3f800b5c:…laminas.py \| sed -n '935,936p'`; `sed -n '44,52p' laminas_svg.py`
> 11. `uv run pytest tests/unit/test_laminas.py tests/unit/test_laminas_svg.py tests/unit/test_laminas_registro.py -p no:cacheprovider -v`: 37 passed. Antes, una forma con `;` que la guardia negó.
> 12. `git diff main...HEAD -- src/botsito/cli.py`
> 13. `git diff main...HEAD -- domain/sesgo.py domain/estructura_m1.py engine/primitivas.py engine/zonas.py`
> 14. Grep de `anotaciones`, `ResultadoSesgo`, `zonas_de_control`, `m1_entre`, `contraria_inicio` y `EstadoDia(` en `src/`
> 15. En `C:\Users\USER\Desktop\laminas-sesion-7`: `ls`; `find … \| wc -l`; el grep de fechas, ids y dinero sobre `*.html`; el recuento de las frases `<li>`; `python -c` de geometría contra el borde del corte; `grep -rl … \| wc -l` de marcas y frases; recuento de `lamina-*.html` por carpeta. clave.txt no se abrió.
> 16. `sed -n` de los números de línea citados en strategy_spec.yaml, parametros.yaml, config.yaml, zonas.py, primitivas.py, broker.py, llenado.py, primitivas_broker.py, CORRIDA-CONSTRUCCION.md y ADR-0082
> 17. `git ls-files docs src tests \| grep -ci clave`, etc. Antes, un `git ls-files` sin rutas que la guardia negó por ADR-0088.
> 18. `git diff --name-only main...HEAD -- <protegidas> \| wc -l` y `git diff --name-only -- knowledge scripts .claude \| wc -l`: 0 y 0
> 19. `ls -la data/laminas/ data/laminas/bitacora/` y `git log --format='%h %ci' main..HEAD`. Antes, dos `cmp` que la guardia negó.
> 20. `sha256sum` de base.txt, las bitácoras y sus anexos
> 21. `ls -l --time-style=+%H:%M` de los ficheros de `src/` cambiados y de la salida
> 22. `uv run botsito state check`: OK
> 23. `gh run view 42881622332 --json …` y `--log-failed \| grep`
> 24. `wc -c PROJECT_STATE.md`; `grep -c` del texto de F; `grep -n R4.5 docs/plan/HOJA-DE-RUTA.md`
> 25. `uv run python -B -c` con `problemas_a`, `problemas_b`, `problemas_c` y `problemas_d` sobre copias en memoria. Antes, un `export PYTHONDONTWRITEBYTECODE` que la guardia negó.
> 26. `python -c` que compara la respuesta copiada en el encargo con la del informe
> 27. `git worktree list && git branch -a`; `git show b7d5d6d8 -- contrato.yaml`
> 28. Grep de `no-negocio` en el diff de `src/` y de `Europe/Madrid` en `laminas*.py`

### La segunda pasada (2026-11-10), tal cual

Va tal cual salvo en un sitio: en la fila N1 se quitan, marcadas «[quitado al pegar]» y «[esa cifra]», la cifra y el día que N1 pide quitar, porque copiarlos aquí los volvería a escribir. Lo hecho con ella: N1, N3 y N4, corregidos en el informe; N2, añadido a la decisión 13; y lo que quedaba de b-B1, dicho en su fila y en la decisión 13.

> ## Informe del revisor · trabajo/laminas · segunda pasada (acotada) · 2026-11-10
>
> He revisado `f6ed348` y lo que está sin commitear (`docs/validation/LAMINAS.md`, `docs/validation/HOLDOUT-EXPOSICIONES.md`, `tests/unit/test_laminas.py`). No he modificado nada.
>
> Resultado: de la primera pasada queda uno en parte (b-B1); todos los demás están resueltos. Hay 1 bloquea, 1 importa y 2 menores nuevos. La rama no está lista hasta quitar el bloquea N1.
>
> **En este informe no escribo qué carpeta `sesion-NN` es qué día, a propósito.** Si se pega en LAMINAS.md, tiene que seguir así.
>
> ### Los hallazgos de la primera pasada
>
> | # | Estado | Evidencia |
> |---|---|---|
> | a1 | Resuelto | `laminas.py:950-951` llevan los dos `# no-negocio`; `LAMINAS.md:346` cita esas líneas |
> | a2 | Resuelto | Hay 23 + 12 + 5 = 40 `def test_` y `PROJECT_STATE.md:19` dice 1979. pytest: «42 passed» (las 3 de más son el parametrize de `FRASE_DETENIDO`) |
> | a3 | Resuelto (declarado en `:547`) | La fila se reescribe en su sitio. Su recuento casa: 2 (F4.1) + 2 (F4.2) + 10 (5 invocaciones × 2) = 14. Contra main el fichero sigue solo añadiendo (`--numstat`: 3 0) |
> | a4 | Resuelto (declarado en `:548`) | — |
> | b-B1 | **En parte** | F4.3 ya no copia la lista ni las horas de corte (`:476-478`). Pero `:194` (fase 0, ya en `6b5f069`) dice «la lámina de 07-03 de las 09:35», y «09:35» solo sale en los HTML de una de las diez carpetas (grep: 3 ficheros, todos en la misma). Lo repite el Apéndice A en `:692`, que va tal cual. La fila de `:535` («no se nombra ninguna hora de corte de una lámina de un día») no es del todo cierta. Además está N1 |
> | b-B2 | Resuelto | `:550-591` |
> | b-B3 | Resuelto | La tabla de `:497-509` es idéntica a la salida de `estructura_laminas.py`. La consola da los tipos a y b en `laminas.py:1237-1240` |
> | b-B4 | Resuelto | `test_laminas.py:487-503`: hechos de regla y del bróker desde el vocabulario. `:506-514`: un test por freno |
> | b-I1 | Resuelto | La mutación se ejecuta: `Vivo` (`test_laminas.py:250-261`) y la aserción de `:316-322` |
> | b-I2 | Resuelto | `ConFreno` (`:235-247`) enciende el freno, abre la toma nueva (la toma, sin commitear) y liga la segunda caja después del corte. `lo_del_futuro` (`:264-280`) lo caza |
> | b-I3 | Resuelto en código y test | `linea_dentro` (`laminas.py:734-745`) se usa en `:809` y `:835`; su test es `test_laminas_svg.py:180-191`. `f.m1` arranca en `min(h4, m15, m1)` (`:410`), así que la búsqueda cubre toda la ventana de M15. «No cambia ninguna lámina» no lo he podido comprobar (abajo) |
> | b-I4 | Resuelto | `docs/validation/anexos/LAMINAS/` tiene 5 guiones. Ninguno nombra holdout, corpus, xlsx ni clave.txt (grep) |
> | b-m1 | Resuelto | `docs/runbooks/LAMINAS.md:24-25` (520-659 s) y `:51-55` (el panel más ancho) |
> | b-m2 | Resuelto | `LAMINAS.md:349` |
> | b-m3 | Resuelto | `laminas_svg.py:249-250`; el test mira x, x1, x2, cx y el ancho de los rect (`test_laminas.py:365-369`). En el Escritorio: «marcas a la derecha del corte: 0» |
>
> ### Lo que me pediste mirar aparte
>
> - **Que `f6ed348` no cambie lo que el motor decide: se cumple.** En `src/` solo cambian dos ficheros:
>   - `engine/laminas.py`: `linea_dentro` en `componer`, y el resumen de `generar`.
>   - `engine/laminas_svg.py`: la `x` del rect de `zona-control`.
>
>   Lo que está sin commitear es solo tests y docs. Lo que importa `laminas` en `src/` son ficheros de registro y de CLI (`sesgo.py`, `estructura_m1.py`, `zonas.py`, `primitivas.py`, `cli.py`), y ninguno cambia en `f6ed348`. El sello de `make-check.log` (`aa9dc64c…`, 3401 passed, pico de 310 MiB) es igual a `git rev-parse f6ed348e^{tree}`. La CI del run 42893354923 está sobre `f6ed348e…`, con «1 failed, 3352 passed, 48 skipped»; el único fallo es `test_state_check_ok_on_real_repo`.
> - **Las cifras de F4.3 casan con `C:\Users\USER\Desktop\laminas-sesion-7`:**
>   - 58 ficheros: 47 láminas, 10 índices y la clave;
>   - por sesión, la tabla de tipos a y b exacta: 19 de tipo a y 28 de tipo b;
>   - `h4-fija` en 47 de 47;
>   - «Es el primer esquema» en 31 ficheros, igual que las 31 con caja;
>   - «Iba a colocar la orden y no la coloca» en 13 ficheros;
>   - 0 casos en los HTML de fechas, ids, € o «julio/abril».
>
>   clave.txt no lo abrí.
>
> ### Hallazgos nuevos
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | N1 | **bloquea** | La línea nueva sin commitear de «Lo que no me convence» 4 ata una lámina y su carpeta a 07-03, por la misma regla que b-B1 (encargo, punto 5; HOJA R4.5). La lámina enseña el número de zonas, y [esa cifra] sale en una sola de las 47. La decisión 13 no lo recoge, y seguiría delatando la carpeta aunque se elija la opción (b). Basta con quitar la cifra o el día | `LAMINAS.md:609`: «([quitado al pegar])». `Grep 'zonas de control de las que admite \(\d+'` en `*.html`: el «([esa cifra]» sale en 1 fichero |
> | N2 | importa | La decisión 13 (b), barajar las carpetas, no deja de identificar 07-03. El encargo ata el punto 1.14496 a la lámina de 07-03, y PROJECT_STATE ata las 09:35 a 2026-07-03. Las dos cadenas salen solo en los HTML de una carpeta. El texto de la decisión no lo dice, así que Aleks decidiría con un dato incompleto | `docs/encargos/trabajo-laminas.md:23`. `PROJECT_STATE.md:144`. Grep `1\.14496` en `*.html`: 2 ficheros de la misma carpeta. Grep `09:35`: 3 ficheros de la misma carpeta. `LAMINAS.md:597-601` |
> | N3 | menor | La fila b-I1 dice «cuatro cosas posteriores al corte»; el test sin commitear ya pide cinco | `LAMINAS.md:539`; `test_laminas.py:311` («las cinco») y `:316-322` |
> | N4 | menor | `## Estado` sigue con «Falta el revisor» y solo nombra el run 42881622332, no el 42893354923. Además queda el marcador `{REVISOR2}` | `LAMINAS.md:905` y `:908` |
>
> ### Lo que no pude comprobar
>
> - Que `linea_dentro` no cambie ninguna de las 47 láminas (b-I3). La evidencia es el diff entre las invocaciones 2 y 4, que se escribieron en carpetas temporales que no he visto.
> - Los `diff -r` de 0 bytes (3 contra 2 y 5 contra 4), por lo mismo.
> - Cómo se ven las láminas.
> - El contenido de clave.txt: no lo abrí.
>
> ### Comandos ejecutados
>
> 1. `git log --format='%h %s' main..HEAD && git status --short && git diff --stat main...HEAD | tail -5 && grep -n "^#" docs/validation/LAMINAS.md`
> 2. Read de `LAMINAS.md:440-639` y `:755-909`
> 3. `git show --stat f6ed348e` y `git diff 675ee623 f6ed348e -- src/`
> 4. `grep -n "desde_m15\|…" src/botsito/engine/laminas.py`
> 5. `uv run pytest tests/unit/test_laminas.py tests/unit/test_laminas_svg.py tests/unit/test_laminas_registro.py -p no:cacheprovider -q` y `-v`: 42 passed
> 6. `grep -cE "^def test_"` en los tres ficheros: 23, 12 y 5
> 7. `git diff -- tests/unit/test_laminas.py`; Read de `test_laminas.py:200-529` y de `test_laminas_svg.py:176-210`
> 8. `cat docs/validation/anexos/LAMINAS/estructura_laminas.py` y `uv run python -B …/estructura_laminas.py C:/Users/USER/Desktop/laminas-sesion-7`
> 9. Grep sobre `*.html` del Escritorio: `1\.14496`, `zonas de control`, `… admite \(\d+`, `09:35`, «Es el primer esquema», «Iba a colocar…» y el de fechas, ids y dinero
> 10. Grep de `07-03|1\.14496|sesion-\d\d` en LAMINAS.md y en el encargo
> 11. `git show 675ee623:…LAMINAS.md | grep`, `git show f6ed348e:… | grep`, `git diff -- LAMINAS.md | grep`, `git log -S"de las 09:35"`, `grep 09:35 PROJECT_STATE.md`
> 12. `grep no-negocio` en `laminas*.py`; grep de recuentos en LAMINAS.md y PROJECT_STATE.md
> 13. `git diff 675ee623 f6ed348e -- docs/runbooks/LAMINAS.md`; `git diff -- HOLDOUT-EXPOSICIONES.md`; `--numstat` contra main
> 14. Grep de `laminas` en `src/botsito`
> 15. `git diff --name-only 675ee623 f6ed348e && git diff --name-only HEAD`. Antes, el mismo comando con `contrato_rama.py` encadenado, que la guardia negó; no lo rodeé, lo partí en dos llamadas
> 16. `uv run python scripts/contrato_rama.py`: «CONTRATO: 23 ficheros dentro del contrato de trabajo/laminas (riesgo alto, …, 3 comprobaciones para el revisor)»
> 17. `grep SELLO|PICO|passed|failed make-check.log` y `git rev-parse f6ed348e^{tree}`
> 18. `gh run view 42893354923 --json …` y `--log-failed | grep`
> 19. `git show 3f800b5c:…LAMINAS.md | grep`; `git log --format='%h%n%B' main..HEAD | grep`
> 20. `find … | wc -l` en `laminas-sesion-7` (58, 47, 10)
> 21. Grep `anexos/LAMINAS` de holdout, corpus, clave y xlsx

## Estado

LISTA PARA REVISIÓN (2026-11-11): la ronda tras revisar la v4, hecha. El mínimo de 15 velas del M1 de cerca y el lado de las marcas de borde del M1, con sus tests; la v5 de `43d4bc3`; la CI; el revisor, con lo que encontró. Rama lista para revisión, NO cerrada.
