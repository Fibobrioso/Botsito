<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Parametros: la unica puerta de los valores

`spec_version 10.2.0` · hash `9c4bf66f4707…`

59 en total: 52 con valor y 7 sin el. Ninguna regla contiene un numero: `spec check` exige que cada argumento de una forma ejecutable sea el NOMBRE de un parametro, de un token declarado o de una ligadura (ADR-0002, ADR-0019).

| Parametro | Valor | Estado | Categoria | De donde sale | Unidad |
|---|---|---|---|---|---|
| `anclaje_h4` | `17:00 America/New_York` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-479e68b9` | hora de reloj de pared en el huso declarado; parte la recta UTC en velas H4 |
| `base_calculo_objetivo` | `caja_completa` | CONFIRMED | estrategia | `ev-v2-003256-0197f4e1` | sobre que distancia se multiplica objetivo_rr |
| `base_calculo_perdida_diaria` | `saldo_inicial_dia` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-462134c7` | sobre que saldo se calcula |
| `base_calculo_perdida_semanal` | `saldo_actual` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a85b6bc7` | sobre que saldo se calcula |
| `base_calculo_riesgo` | `saldo_actual` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-2603c017` | sobre que saldo se calcula |
| `break_even_condicion` | `tocar` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-0ccafcba` | tocar/cierre |
| `break_even_criterio_ruptura` | `mecha` | DEFAULT_AMBIGUOUS · en revision por A-13 | estrategia | `fb-2026-09-09-sesion-01-0ccafcba` | que hace falta para dar por rota la zona que dispara el break even |
| `broker_dst` | `us` | CONFIRMED | broker | `ADR-0012` | que calendario de cambio de hora sigue el servidor |
| `broker_offset_base` | `120` | CONFIRMED | broker | `ADR-0012` | minutos que el reloj del servidor va por delante de UTC en horario estandar |
| `cartucho_criterio` | `solo_perdida` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-aa2abe65` | que suma al contador |
| `cartuchos_max` | `3` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-1a3064b0` | intentos por zona de liquidez |
| `cartuchos_reinicio` | `siguiente_liquidez_m15` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-e3eedcaa` | cuando se pone a cero el contador |
| `cierre_forzoso_fin_ventana` | `si` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-ffb528d7` | si/no |
| `comportamiento_sin_regla` | `abstenerse` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-c698bc6a` | abstenerse/regla_mas_parecida |
| `cuenta_objetivo` | `fondeada` | CONFIRMED | prop_firm | `ADR-0012` | tipo de cuenta |
| `cuenta_pruebas` | `demo` | CONFIRMED | prop_firm | `ADR-0012` | tipo de cuenta |
| `dias_operables` | `lunes_a_viernes` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-140d655c` | que dias de la semana se opera |
| `filtro_noticias` | `regla` | CONFIRMED | prop_firm | `ADR-0022` | regla de filtro, o no si no filtra |
| `filtro_spread` | `False` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-672262d5` | se aplica o no |
| `huso_grafico` | `Europe/Madrid` | CONFIRMED | estrategia | `ev-v3-000136-6160fcea` | nombre IANA del huso configurado en el grafico del trader |
| `huso_operativa` | `Europe/Madrid` | CONFIRMED | ejecucion | `ADR-0017` | nombre IANA del huso en el que se expresan las horas de la operativa |
| `instrumento` | `EURUSD` | CONFIRMED | estrategia | `ev-v2-003320-a736fd37` | simbolo del instrumento |
| `instrumento_contrato` | `100000` | CONFIRMED | instrumento | `ADR-0012` | unidades de la divisa base por lote |
| `instrumento_digitos` | `5` | CONFIRMED | instrumento | `ADR-0012` | decimales de la cotizacion |
| `instrumento_lote_minimo` | `0.01` | CONFIRMED | instrumento | `ADR-0012` | lotes |
| `instrumento_lote_paso` | `0.01` | CONFIRMED | instrumento | `ADR-0012` | lotes |
| `instrumento_stops_level` | `0` | CONFIRMED | instrumento | `ADR-0012` | puntos de distancia minima a mercado |
| `latencia_ms` | `0` | CONFIRMED | ejecucion | `ADR-0012` | milisegundos de latencia supuesta entre senal y orden |
| `liquidez_m15_criterio_toma` | `cuerpo` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-6e15504f` | cuerpo/mecha |
| `lotaje_base` | `hasta_stop_fraccion` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-17ed6193` | distancia que absorbe riesgo_por_operacion |
| `mapeo_dos_velas` | `order_block_mayor` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-7ee9cabc` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `modelo_llenado` | `al_tocar` | CONFIRMED | ejecucion | `ADR-0012` | como se decide que una orden limite se ha llenado |
| `objetivo_extension_activa` | `False` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-9c259e06` | se aplica o no |
| `objetivo_rr` | `3` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-7fbbb2e7` | multiplo de la distancia que declara base_calculo_objetivo |
| `operaciones_simultaneas_max` | `1` | CONFIRMED | estrategia | `ev-v4-003710-c753f3d3` | operaciones abiertas a la vez |
| `parciales` | `no` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-0905fd59` | si/no |
| `perdida_maxima_diaria` | `4.5 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-bff260ea` | porcentaje del saldo que declara base_calculo_perdida_diaria |
| `perdida_maxima_semanal` | `9 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a85b6bc7` | porcentaje del saldo que declara base_calculo_perdida_semanal |
| `reentrada_tras_equal` | `si` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-060cd801` | si/no |
| `reloj_dia_riesgo` | `servidor` | DEFAULT_AMBIGUOUS · en revision por A-19 | prop_firm | `ADR-0015` | que reloj marca el corte del dia (y de la semana) de riesgo |
| `reubicacion_cadencia` | `al_romper` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-6b29059d` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `riesgo_por_operacion` | `0.5 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-648ec915` | porcentaje de la cuenta por operacion |
| `saldo_inicial_cuenta` | `100000` | CONFIRMED | prop_firm | `ADR-0012` | USD |
| `salida_sin_ruptura` | `proteger_y_dejar` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-9626d3dd` | cerrar_al_cierre/proteger_y_dejar |
| `sesgo_h4_criterio_ruptura` | `mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8eccf5c0` | que hace falta para dar por rota la vela H4 previa |
| `sesgo_h4_regla` | `vela_anterior_cierre_mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8eccf5c0` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `stop_en_orden_pendiente` | `en_la_orden` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-76fd91ba` | en_la_orden/tras_el_llenado |
| `stop_fraccion_caja` | `0.8 (fraccion)` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-d34a0222` | fraccion de la distancia completa nivel 0 -> nivel 1 |
| `ventana_fin` | `15:00 Europe/Madrid` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-951b7a79` | hora de reloj de pared del trader (huso_operativa) |
| `ventana_inicio` | `07:00 Europe/Madrid` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8741c388` | hora de reloj de pared del trader (huso_operativa) |
| `zona_control_criterio_completada` | `mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a456bc3f` | que hace falta para dar una zona de control por completada |
| `zonas_control_max_por_esquema` | `1` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-1b2203b0` | zonas de control admitidas dentro de un mismo esquema |

## Sin valor, y leerlos FALLA a proposito

No es que falte rellenarlos: es el comportamiento. El motor que intente leer uno de estos revienta, y eso es lo correcto.

- **`objetivo_extension`** (estrategia) — hasta donde se extiende el objetivo; solo si objetivo_extension_activa
- **`spread_maximo`** (estrategia) — spread por encima del cual no se abre la operacion; solo si filtro_spread
- **`stop_colchon_spread`** (estrategia) — si el 0,8 es fijo o es 0,75 mas un colchon variable. RESPONDIDO Y DESCARTADO en la sesion 1 (A-10): el 0,8 ya lleva el colchon dentro, asi que no hay parametro que fijar. Se queda UNKNOWN a proposito -leerlo falla- y la regla vive en strategy_spec
- **`stop_proteccion_capital`** (estrategia) — la fraccion de la caja que queda al otro lado del stop. DERIVADA de stop_fraccion_caja (1 - 0,8 = 0,2), asi que no se fija aqui: se queda UNKNOWN y el invariante vive en strategy_spec, para que no haya dos puertas para el mismo numero. OJO, dos cosas que esta descripcion decia hasta el 2026-09-11: el stop no "se mueve" -nace en la orden, A-11- y ese tramo no es presupuesto de riesgo que se "guarde", porque el lote ya no se dimensiona sobre la caja entera; RN-012 dice que no se arriesga nunca
- **`stop_reduccion_fraccion`** (estrategia) — nivel al que se reduce el stop cuando la vela avanza (A-12)
- **`stop_reduccion_umbral_vela`** (estrategia) — parte de la vela a partir de la cual se baja el stop (40 o 50; A-12)
- **`stop_segundo_esquema`** (estrategia) — UNKNOWN A PROPOSITO desde la auditoria del 2026-09-10 (A-7 sigue resuelta): no hay un stop del segundo esquema distinto del primero. El trader dijo que es el MISMO en los dos, asi que un parametro aparte con el mismo valor son dos puertas para el mismo numero -lo que RN-012 prohibe expresamente para stop_proteccion_capital y ADR-0002 para todo-. Hay un unico esquema de stop y vive en stop_fraccion_caja. Leerlo falla, que es lo que debe pasar

## Quien lee cada valor

Un valor que ninguna regla nombra declara quien lo consumira; si no, seria un valor que nadie usa y nadie vigila (F12).

- `cuenta_objetivo` → F33
- `cuenta_pruebas` → F17, F33
- `huso_grafico` → ADR-0017
- `instrumento` → F24, F28, F31, F33
- `latencia_ms` → F24, F27
- `modelo_llenado` → F24, F27
- `saldo_inicial_cuenta` → F24, F33

## Que dice cada uno

### `anclaje_h4`

donde empieza la rejilla H4. Es la medianoche del servidor, que por convencion de los brokers se escribe 17:00 America/New_York (ADR-0005) y que sigue el calendario de Nueva York, como confirma broker_dst medido contra la demo. El trader lo ve como las 23:00 en su pantalla, y es cierto 337 dias al año; los otros 28 -8 a 28 de marzo y 25 a 31 de octubre, cuando la UE y EE.UU. no cambian la hora el mismo dia- lo ve a las 22:00. Escrito como una hora de un huso FIJO, el ancla caia una hora antes todo el invierno y repartia mal todas las velas H4, que es de donde sale el sesgo (ADR-0017)

### `base_calculo_objetivo`

distancia sobre la que se mide el objetivo. `caja_completa` es la distancia nivel 0 -> nivel 1; `riesgo_real` seria la distancia hasta stop_fraccion_caja. Hasta el 2026-09-11 esta descripcion anadia que la caja completa es "la misma que dimensiona el lote": desde ADR-0020 ya NO lo es, el lote se dimensiona hasta stop_fraccion_caja y solo el objetivo se mide sobre la caja entera. El objetivo se traza CON la orden, antes de que el stop se mueva, asi que la unica distancia que existe en ese instante es la caja completa. El RR realizado no es 1:3 sino objetivo_rr / stop_fraccion_caja, y es a proposito (RN-012)

Opciones: `caja_completa`, `riesgo_real`.

### `base_calculo_perdida_diaria`

base del tope de perdida del dia; el trader dice que el saldo inicial

Opciones: `saldo_actual`, `saldo_inicial_dia`.

### `base_calculo_perdida_semanal`

base del tope de perdida de la semana. NO es la misma que la diaria: el trader dijo "9% de la cuenta actual" para la semana y "el saldo inicial del dia" para el dia. Estaba en el literal desde la sesion y no habia parametro donde guardarlo, asi que perdida_maxima_semanal declaraba "porcentaje de la cuenta" sin decir de cual

Opciones: `saldo_actual`, `saldo_inicial_semana`, `saldo_inicial_dia`.

### `base_calculo_riesgo`

base del riesgo por operacion; el trader dice que el saldo actual

Opciones: `saldo_actual`, `saldo_inicial_dia`.

### `break_even_condicion`

si el break even se pone al tocar el nivel o al cierre de la vela (A-4)

Opciones: `tocar`, `cierre`.

### `break_even_criterio_ruptura`

criterio de ruptura de la zona de control POSTERIOR a la entrada, que es la que dispara el break even. Es exactamente lo que pregunta A-13, y sigue ABIERTA: el trader se desdice a los doce minutos. Entra `mecha` por coherencia con los otros dos criterios, pero es un DEFAULT NUESTRO. No confundir con break_even_condicion, que dice si el stop se mueve al TOCAR el nivel o al cierre de la vela: son dos preguntas distintas que la prosa mantenia juntas

Opciones: `mecha`, `cuerpo`.

### `broker_dst`

con que calendario cambia la hora el servidor. FundedNext sigue el de Nueva York, asi que en verano el reloj va a GMT+3 y el dia de riesgo se desplaza. Este reloj y huso_grafico son DOS RELOJES DISTINTOS: este es el del servidor donde se ejecuta, aquel el de la pantalla donde el trader decide. Coinciden en invierno y divergen una hora en verano, asi que las horas de la operativa se interpretan SIEMPRE en huso_grafico y se convierten al ejecutar

Opciones: `us`, `eu`, `ninguno`.

### `broker_offset_base`

desfase base del reloj del servidor (GMT+2 en invierno, GMT+3 en verano de Nueva York); medido en el terminal, no supuesto

### `cartucho_criterio`

que cuenta como cartucho gastado; el trader dice que solo una perdida

Opciones: `solo_perdida`, `todo_intento`.

### `cartuchos_max`

numero maximo de intentos por barrido de liquidez (2 o 3; A-2)

### `cartuchos_reinicio`

cuando vuelve a operar tras agotar los cartuchos (no es por fin de dia)

Opciones: `siguiente_liquidez_m15`, `fin_de_dia`, `nunca`.

### `cierre_forzoso_fin_ventana`

si un trade abierto se cierra en punto al terminar la ventana (A-6)

Opciones: `si`, `no`.

### `comportamiento_sin_regla`

que hace el bot cuando la situacion no encaja con ninguna regla

Opciones: `abstenerse`, `regla_mas_parecida`.

### `cuenta_objetivo`

cuenta a la que apunta el bot cuando este validado

Opciones: `fondeada`, `demo`, `propia`.

### `cuenta_pruebas`

cuenta en la que se prueba el funcionamiento antes de la fondeada

Opciones: `fondeada`, `demo`, `propia`.

### `dias_operables`

dias en los que el bot busca entradas. Era `texto` con el valor "lunes a viernes" y RN-001 lo usa como condicion EJECUTABLE, asi que el motor habria tenido que parsear espanol

Opciones: `lunes_a_viernes`, `todos_los_dias`.

### `filtro_noticias`

si se deja de operar alrededor de noticias de alto impacto y con que margen. `no` es lo que hace EL TRADER en sus cuentas propias, que no lo prohiben, y su estrategia funciona dentro de esos eventos -"a mi me es indiferente si hay noticia o no", fb-2026-09-09-sesion-01-3565552d-. El BOT corre con `regla` desde ADR-0022 porque va a una cuenta fondeada que puede prohibirlo como norma, y la sancion es perder la cuenta aunque la operacion acabe en profit. La opcion `no` se conserva a proposito: el dia que el bot corra donde se permita, se cambia el valor y nada mas. CON QUE VENTANA se bloquea es A-17, que sigue abierta

Opciones: `no`, `regla`.

### `filtro_spread`

si el bot descarta una entrada por spread alto (el trader dice que no filtra)

### `huso_grafico`

como se ETIQUETAN las horas en la pantalla del trader. No hay configuracion deliberada de huso: su plataforma muestra su hora local, que es la misma de huso_operativa. Sirve para traducir lo que el dice -"la vela empieza a las 23"- a un instante: 23:00 Madrid son las 21:00 UTC en verano y las 22:00 en invierno. NINGUNA regla cuelga de este parametro; las horas de la operativa cuelgan de huso_operativa y la rejilla H4 de anclaje_h4. Y NO es el reloj del servidor, que va en broker_offset_base + broker_dst y sigue a Nueva York

### `huso_operativa`

reloj del TRADER como persona: la hora a la que se sienta y a la que cierra, y de la que cuelgan ventana_inicio y ventana_fin. Es su reloj civil y por tanto cambia con el horario de verano. ADR-0005 lo fijo en Europe/Madrid, ADR-0012 lo cambio a un offset fijo apoyandose en que "la sesion desmintio Madrid" -que no ocurrio, ver ADR-0015- y ADR-0017 lo revierte: el trader opera siempre a la misma hora SUYA, sea cual sea la fecha

### `instrumento`

instrumento sobre el que opera la primera version. Sale de la evidencia, no de una respuesta: es el unico instrumento de todo el corpus grabado y se lee en pantalla. Por donde ampliar -NASDAQ, oro, pares sin gaps, futuros- lo dijo el trader y vive en fb-2026-09-09-sesion-01-6eceb844

### `instrumento_contrato`

tamano del contrato; con el se convierte el riesgo en lotes

### `instrumento_digitos`

digits del simbolo; con 5 un punto es 0,00001 y un pip son 10 puntos

### `instrumento_lote_minimo`

lote minimo que admite el broker; por debajo, la operacion se rechaza

### `instrumento_lote_paso`

escalon del lote; el lotaje calculado se redondea a un multiplo de este paso

### `instrumento_stops_level`

distancia minima a la que el broker admite un stop o un limite. Si la spec pide uno mas cerca, la respuesta es ABSTENERSE, nunca aproximar (MASTER_PLAN H.2)

### `latencia_ms`

latencia que asume `cruce_mas_latencia`; con `al_tocar` no se usa

### `liquidez_m15_criterio_toma`

si la liquidez de M15 se toma con cierre de cuerpo o basta la mecha

Opciones: `cuerpo`, `mecha`.

### `lotaje_base`

sobre que distancia se dimensiona el lote. `distancia_completa` es la caja entera, del nivel 0 al nivel 1, y deja la perdida del stop POR DEBAJO del riesgo nominal; `hasta_stop_fraccion` es la distancia del nivel 0 a stop_fraccion_caja, asi que el stop cuesta el riesgo ENTERO y el resto de la caja deja de ser presupuesto de riesgo. La segunda opcion se llamaba `desde_075` hasta el 2026-09-11: nombraba un 0,75 que A-10 habia cerrado en 0,8, y un numero de negocio en el nombre de una opcion es la clase de doble puerta que ADR-0002 prohibe. Ahora el nivel lo pone stop_fraccion_caja y solo el

Opciones: `distancia_completa`, `hasta_stop_fraccion`.

### `mapeo_dos_velas`

cuando dos velas de M1 cuentan como una estructura al mapear (A-8)

Opciones: `order_block_mayor`, `otra`.

### `modelo_llenado`

criterio de llenado en el motor de referencia. `al_tocar` es optimista y `cruce_mas_latencia` exige que el precio cruce y pase `latencia_ms`; F27 mide las dos y la diferencia entre ellas es una cota de cuanto depende el resultado del modelo, no de la estrategia

Opciones: `al_tocar`, `cruce_mas_latencia`.

### `objetivo_extension`

hasta donde se extiende el objetivo; solo si objetivo_extension_activa

### `objetivo_extension_activa`

si el objetivo se extiende mas alla del 1:3 (el trader dice que no se extiende)

### `objetivo_rr`

objetivo fijo, en multiplos de la distancia que fija base_calculo_objetivo. "Riesgo" a secas seria ambiguo: hay dos distancias y no son la misma (ADR-0014). Desde ADR-0020 la diferencia es mayor, porque el lote ya no se dimensiona sobre la caja entera sino hasta stop_fraccion_caja, que es donde acaba el stop. El objetivo es FIJO, no minimo: la sesion 1 cerro la extension en objetivo_extension_activa: false

### `operaciones_simultaneas_max`

cuantas operaciones puede tener abiertas el bot a la vez. Vivia en la prosa de RN-018 -"hay una operacion abierta", "no se abre otra"- y por tanto fuera del registro

### `parciales`

si se toman parciales

Opciones: `si`, `no`.

### `perdida_maxima_diaria`

perdida acumulada en el dia que detiene la operativa; la base la fija base_calculo_perdida_diaria y el corte, reloj_dia_riesgo. Tras corregir la aritmetica de los cartuchos (ver RN-020) este es el UNICO freno del dia que existe

### `perdida_maxima_semanal`

perdida acumulada en la semana que detiene la operativa; la base la fija base_calculo_perdida_semanal y el corte, reloj_dia_riesgo

### `reentrada_tras_equal`

si tras un equal (activacion sin rotura) se reentra al romper de nuevo

Opciones: `si`, `no`.

### `reloj_dia_riesgo`

en que reloj cae la medianoche que reinicia el tope diario, y el domingo que reinicia el semanal. Sin esto, "el saldo inicial del dia" no dice cuando empieza el dia. Importa porque los dos relojes NO coinciden: el del servidor cambia con el calendario de Nueva York (broker_offset_base + broker_dst) y el del grafico esta en discusion (A-14), asi que se separan una hora buena parte del año. `servidor` es un DEFAULT NUESTRO: es como lo calculan las cuentas de fondeo, pero no esta verificado contra el panel de FundedNext (A-19), y en una cuenta fondeada equivocarse aqui es perder la cuenta, no perder un trade

Opciones: `servidor`, `grafico`.

### `reubicacion_cadencia`

cada cuanto se reubica la orden limite mientras no se activa (A-5)

Opciones: `cada_vela`, `al_romper`, `otra`.

### `riesgo_por_operacion`

riesgo por operacion (1 en backtest; 0,4-0,5 en fondeo). Desde ADR-0020 es lo que cuesta el stop DE VERDAD, no un nominal: el lote se dimensiona sobre la distancia hasta stop_fraccion_caja (lotaje_base)

### `saldo_inicial_cuenta`

saldo con el que arranca la cuenta. NO es la base de ningun calculo: el lotaje va sobre base_calculo_riesgo (saldo_actual), el tope diario sobre base_calculo_perdida_diaria (saldo_inicial_dia) y el semanal sobre base_calculo_perdida_semanal (saldo_actual). Lo decia y era falso; corregido en la auditoria del 2026-09-10

### `salida_sin_ruptura`

que se hace si la orden se activa sin ruptura (A-3)

Opciones: `cerrar_al_cierre`, `proteger_y_dejar`.

### `sesgo_h4_criterio_ruptura`

criterio de ruptura del extremo de la H4 anterior, del que depende el sesgo. Vivia dentro del nombre del enum `sesgo_h4_regla` (`vela_anterior_cierre_mecha`), que mezclaba sujeto y criterio; la forma ejecutable de F12 lo separa porque el criterio es un ARGUMENTO del predicado `rompe`, y escribirlo a pelo seria un valor de negocio en un campo ejecutable

Opciones: `mecha`, `cuerpo`.

### `sesgo_h4_regla`

que vela H4 fija el sesgo y cuando cambia (A-1)

Opciones: `vela_anterior_color`, `vela_anterior_cierre_mecha`, `otra`.

### `spread_maximo`

spread por encima del cual no se abre la operacion; solo si filtro_spread

### `stop_colchon_spread`

si el 0,8 es fijo o es 0,75 mas un colchon variable. RESPONDIDO Y DESCARTADO en la sesion 1 (A-10): el 0,8 ya lleva el colchon dentro, asi que no hay parametro que fijar. Se queda UNKNOWN a proposito -leerlo falla- y la regla vive en strategy_spec

Opciones: `fijo`, `spread`.

### `stop_en_orden_pendiente`

si el SL viaja en la orden pendiente o se pone tras el llenado (A-11). RESPONDIDO por el trader el 2026-09-10: "el SL se pone junto a la orden limite, no cuando se apertura recien". Deja de ser la inferencia que el barrido de fidelidad habia marcado. Consecuencia para el motor: la orden pendiente NACE con su stop, asi que no hay evento "mover el stop tras el llenado" que implementar, y RN-026 tiene que comprobar instrumento_stops_level en el momento de COLOCAR, no despues

Opciones: `en_la_orden`, `tras_el_llenado`.

### `stop_fraccion_caja`

nivel de la caja donde vive el stop. Se escribe EN la orden limite y no se mueve despues (A-10 lo fijo en 0,8; A-11 cerro que viaja en la orden). Ademas es la distancia que dimensiona el lote desde ADR-0020

### `stop_proteccion_capital`

la fraccion de la caja que queda al otro lado del stop. DERIVADA de stop_fraccion_caja (1 - 0,8 = 0,2), asi que no se fija aqui: se queda UNKNOWN y el invariante vive en strategy_spec, para que no haya dos puertas para el mismo numero. OJO, dos cosas que esta descripcion decia hasta el 2026-09-11: el stop no "se mueve" -nace en la orden, A-11- y ese tramo no es presupuesto de riesgo que se "guarde", porque el lote ya no se dimensiona sobre la caja entera; RN-012 dice que no se arriesga nunca

### `stop_reduccion_fraccion`

nivel al que se reduce el stop cuando la vela avanza (A-12)

### `stop_reduccion_umbral_vela`

parte de la vela a partir de la cual se baja el stop (40 o 50; A-12)

### `stop_segundo_esquema`

UNKNOWN A PROPOSITO desde la auditoria del 2026-09-10 (A-7 sigue resuelta): no hay un stop del segundo esquema distinto del primero. El trader dijo que es el MISMO en los dos, asi que un parametro aparte con el mismo valor son dos puertas para el mismo numero -lo que RN-012 prohibe expresamente para stop_proteccion_capital y ADR-0002 para todo-. Hay un unico esquema de stop y vive en stop_fraccion_caja. Leerlo falla, que es lo que debe pasar

### `ventana_fin`

hora a la que el trader deja de operar y cierra lo que quede abierto. Es SU horario como persona, igual que ventana_inicio (A-6, ADR-0017)

### `ventana_inicio`

hora a la que el trader empieza a buscar entradas. Es SU horario como persona y no se mueve con la fecha, asi que en UTC si se mueve con el cambio de hora (ADR-0017)

### `zona_control_criterio_completada`

criterio de ruptura del punto extremo anterior que completa una zona de control. El trader lo dice con todas las letras -"con mecha no importa"- y hasta ahora vivia solo en la definicion del glosario

Opciones: `mecha`, `cuerpo`.

### `zonas_control_max_por_esquema`

cuantas zonas de control puede desarrollar un esquema sin invalidarlo. Vivia en la prosa de RN-009 -"se desarrolla mas de una zona de control"- y por tanto fuera de la unica puerta (ADR-0002). Fue un default nuestro mientras la unica cita disponible decia "por lo general solo buscamos uno", que no es una prohibicion dura. El 2026-09-11 el trader lo cierra por escrito -"solo 1 zona control bro. si hay 2 se descarta"- y ratifica las dos cosas: el numero y el descarte. A-20 RESUELTA
