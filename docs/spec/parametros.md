<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Parametros: la unica puerta de los valores

`spec_version 12.2.1` · hash `d3b9178415c4…`

75 en total: 66 con valor y 9 sin el. Ninguna regla contiene un numero: `spec check` exige que cada argumento de una forma ejecutable sea el NOMBRE de un parametro, de un token declarado o de una ligadura (ADR-0002, ADR-0019).

| Parametro | Valor | Estado | Categoria | De donde sale | Unidad |
|---|---|---|---|---|---|
| `anclaje_h4` | `17:00 America/New_York` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-479e68b9` | hora de reloj de pared en el huso declarado; parte la recta UTC en velas H4 |
| `base_calculo_objetivo` | `caja_completa` | CONFIRMED | estrategia | `ev-v2-003256-0197f4e1` | sobre que distancia se multiplica objetivo_rr |
| `base_calculo_perdida_diaria` | `saldo_inicial_dia` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-462134c7` | sobre que saldo se calcula |
| `base_calculo_perdida_semanal` | `saldo_actual` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a85b6bc7` | sobre que saldo se calcula |
| `base_calculo_riesgo` | `saldo_actual` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-2603c017` | sobre que saldo se calcula |
| `break_even_condicion` | `tocar` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-0ccafcba` | tocar/cierre |
| `break_even_criterio_ruptura` | `mecha` | DEFAULT_AMBIGUOUS · en revision por A-13 | estrategia | `fb-2026-09-09-sesion-01-0ccafcba` | que hace falta para dar por rota la zona que dispara el break even |
| `breaker_m1_criterio_ruptura` | `mecha` | CONFIRMED | estrategia | `ev-v4-005910-d24c0345` | que hace falta para dar por rota la estructura de M1 que forma el esquema de entrada |
| `cartucho_criterio` | `solo_perdida` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-aa2abe65` | que suma al contador |
| `cartuchos_max` | `3` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-1a3064b0` | intentos por zona de liquidez |
| `cartuchos_reinicio` | `siguiente_liquidez_m15` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-e3eedcaa` | cuando se pone a cero el contador |
| `cierre_forzoso_fin_ventana` | `si` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-ffb528d7` | si/no |
| `comportamiento_sin_regla` | `abstenerse` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-c698bc6a` | abstenerse/regla_mas_parecida |
| `cuenta_objetivo` | `fondeada` | CONFIRMED | prop_firm | `ADR-0012` | tipo de cuenta |
| `cuenta_pruebas` | `demo` | CONFIRMED | prop_firm | `ADR-0012` | tipo de cuenta |
| `dias_operables` | `lunes_a_viernes` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-140d655c` | que dias de la semana se opera |
| `filtro_noticias` | `no` | CONFIRMED | prop_firm | `ADR-0026` | regla de filtro, o no si no filtra |
| `filtro_spread` | `False` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-672262d5` | se aplica o no |
| `firma` | `ftmo` | CONFIRMED | prop_firm | `ADR-0026` | prop firm de destino |
| `firma_apalancamiento` | `30` | CONFIRMED | prop_firm | `ADR-0026` | apalancamiento maximo en forex (1:N) |
| `firma_base_perdida_diaria` | `saldo_corte_diario` | CONFIRMED | prop_firm | `ADR-0026` | sobre que saldo se fija el limite del dia |
| `firma_cierre_al_tope` | `si` | CONFIRMED | prop_firm | `ADR-0026` | si/no |
| `firma_magnitud_vigilada` | `equity` | CONFIRMED | prop_firm | `ADR-0026` | que magnitud no puede bajar del limite |
| `firma_margen_seguridad` | `0.5 %` | CONFIRMED | prop_firm | `ADR-0031` | porcentaje del capital simulado inicial (saldo_inicial_cuenta) |
| `firma_mensajes_dia_max` | `2000` | CONFIRMED | prop_firm | `ADR-0026` | peticiones al servidor por dia |
| `firma_noticias_restringe` | `False` | CONFIRMED | prop_firm | `ADR-0026` | si la cuenta restringe operar alrededor de noticias |
| `firma_perdida_diaria_max` | `5 %` | CONFIRMED | prop_firm | `ADR-0026` | porcentaje del capital simulado inicial (saldo_inicial_cuenta) |
| `firma_perdida_total_arrastra` | `False` | CONFIRMED | prop_firm | `ADR-0026` | si el limite total sigue al saldo maximo alcanzado |
| `firma_perdida_total_max` | `10 %` | CONFIRMED | prop_firm | `ADR-0026` | porcentaje del capital simulado inicial (saldo_inicial_cuenta) |
| `firma_programa` | `2-step` | CONFIRMED | prop_firm | `ADR-0026` | programa del reto |
| `firma_tipo_cuenta` | `swing` | CONFIRMED | prop_firm | `ADR-0026` | tipo de cuenta elegido en la compra |
| `huso_grafico` | `Europe/Madrid` | CONFIRMED | estrategia | `ev-v3-000136-6160fcea` | nombre IANA del huso configurado en el grafico del trader |
| `huso_operativa` | `Europe/Madrid` | CONFIRMED | ejecucion | `ADR-0017` | nombre IANA del huso en el que se expresan las horas de la operativa |
| `instrumento` | `EURUSD` | CONFIRMED | estrategia | `ev-v2-003320-a736fd37` | simbolo del instrumento |
| `instrumento_contrato` | `100000` | DEFAULT_AMBIGUOUS · en revision por A-27 | instrumento | `ADR-0026` | unidades de la divisa base por lote |
| `instrumento_digitos` | `5` | DEFAULT_AMBIGUOUS · en revision por A-27 | instrumento | `ADR-0026` | decimales de la cotizacion |
| `instrumento_lote_minimo` | `0.01` | DEFAULT_AMBIGUOUS · en revision por A-27 | instrumento | `ADR-0026` | lotes |
| `instrumento_lote_paso` | `0.01` | DEFAULT_AMBIGUOUS · en revision por A-27 | instrumento | `ADR-0026` | lotes |
| `instrumento_stops_level` | `0` | DEFAULT_AMBIGUOUS · en revision por A-27 | instrumento | `ADR-0026` | puntos de distancia minima a mercado |
| `latencia_ms` | `0` | CONFIRMED | ejecucion | `ADR-0012` | milisegundos de latencia supuesta entre senal y orden |
| `liquidez_m15_criterio_toma` | `cuerpo` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-6e15504f` | cuerpo/mecha |
| `lotaje_base` | `hasta_stop_fraccion` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-17ed6193` | distancia que absorbe riesgo_por_operacion |
| `mapeo_dos_velas` | `order_block_mayor` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-7ee9cabc` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `modelo_llenado` | `al_tocar` | CONFIRMED | ejecucion | `ADR-0012` | como se decide que una orden limite se ha llenado |
| `objetivo_extension_activa` | `False` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-9c259e06` | se aplica o no |
| `objetivo_rr` | `3` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-7fbbb2e7` | multiplo de la distancia que declara base_calculo_objetivo |
| `operaciones_simultaneas_max` | `1` | CONFIRMED | estrategia | `ev-v4-003710-c753f3d3` | operaciones abiertas a la vez |
| `orden_limite_nace` | `al_darse_el_esquema` | DEFAULT_AMBIGUOUS · en revision por A-29 | estrategia | `ev-v3-004201-bfeb3734` | cuando se coloca por primera vez la orden limite de una zona |
| `parciales` | `no` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-0905fd59` | si/no |
| `perdida_maxima_diaria` | `4.5 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-bff260ea` | porcentaje del saldo que declara base_calculo_perdida_diaria |
| `perdida_maxima_semanal` | `9 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a85b6bc7` | porcentaje del saldo que declara base_calculo_perdida_semanal |
| `reentrada_tras_equal` | `si` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-060cd801` | si/no |
| `reloj_dia_riesgo` | `civil_operativa` | CONFIRMED | prop_firm | `ADR-0027` | que reloj marca el corte del dia (y de la semana) de riesgo |
| `reubicacion_cadencia` | `al_romper` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-6b29059d` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `riesgo_por_operacion` | `0.5 %` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-648ec915` | porcentaje de la cuenta por operacion |
| `saldo_inicial_cuenta` | `100000` | CONFIRMED | prop_firm | `ADR-0026` | USD |
| `salida_sin_ruptura` | `proteger_y_dejar` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-9626d3dd` | cerrar_al_cierre/proteger_y_dejar |
| `sesgo_h4_criterio_ruptura` | `mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8eccf5c0` | que hace falta para dar por rota la vela H4 previa |
| `sesgo_h4_regla` | `vela_anterior_cierre_mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8eccf5c0` | opcion cerrada (las sostiene `opciones`, aqui debajo) |
| `sesgo_h4_tope_velas` | `60` | CONFIRMED | ejecucion | `ADR-0044` | velas H4 hacia atras en las que se busca la ultima ruptura que fija el sesgo |
| `stop_en_orden_pendiente` | `en_la_orden` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-76fd91ba` | en_la_orden/tras_el_llenado |
| `stop_fraccion_caja` | `0.8 (fraccion)` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-d34a0222` | fraccion de la distancia completa nivel 0 -> nivel 1 |
| `ventana_fin` | `15:00 Europe/Madrid` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-951b7a79` | hora de reloj de pared del trader (huso_operativa) |
| `ventana_inicio` | `07:00 Europe/Madrid` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-8741c388` | hora de reloj de pared del trader (huso_operativa) |
| `zona_control_criterio_completada` | `mecha` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-a456bc3f` | que hace falta para dar una zona de control por completada |
| `zonas_control_max_por_esquema` | `1` | CONFIRMED | estrategia | `fb-2026-09-09-sesion-01-1b2203b0` | zonas de control admitidas dentro de un mismo esquema |

## Sin valor, y leerlos FALLA a proposito

No es que falte rellenarlos: es el comportamiento. El motor que intente leer uno de estos revienta, y eso es lo correcto.

- **`broker_dst`** (broker) — con que calendario cambia la hora el servidor. El de FundedNext seguia el de Nueva York (valor `us` en su demo) y NO se hereda (ADR-0026): la ficha de FTMO dice "GMT+2 +DST" sin nombrar calendario, asi que se mide en su demo (A-28). Comprobarlo exige OBSERVAR UNA TRANSICION de hora, y por eso A-28 no se cierra antes del cambio de octubre. Desde ADR-0027 este reloj ya no mueve el dia de riesgo, que es civil; si decide si anclaje_h4 (17:00 Nueva York) cae de verdad en la medianoche del servidor. Este reloj y huso_grafico son DOS RELOJES DISTINTOS: este es el del servidor donde se ejecuta, aquel el de la pantalla donde el trader decide
- **`broker_offset_base`** (broker) — desfase base del reloj del servidor, medido en el terminal y no supuesto. En la demo de FundedNext valia 120 (GMT+2 en horario estandar) y NO se hereda (ADR-0026). FTMO declara "GMT+2 +DST" en su ficha de cuenta, que es una descripcion y no una medicion: se mide en su demo (A-28). Desde ADR-0027 no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor
- **`objetivo_extension`** (estrategia) — hasta donde se extiende el objetivo; solo si objetivo_extension_activa
- **`spread_maximo`** (estrategia) — spread por encima del cual no se abre la operacion; solo si filtro_spread
- **`stop_colchon_spread`** (estrategia) — si el 0,8 es fijo o es 0,75 mas un colchon variable. RESPONDIDO Y DESCARTADO en la sesion 1 (A-10): el 0,8 ya lleva el colchon dentro, asi que no hay parametro que fijar. Se queda UNKNOWN a proposito -leerlo falla- y la regla vive en strategy_spec
- **`stop_proteccion_capital`** (estrategia) — la fraccion de la caja que queda al otro lado del stop. DERIVADA de stop_fraccion_caja (1 - 0,8 = 0,2), asi que no se fija aqui: se queda UNKNOWN y el invariante vive en strategy_spec, para que no haya dos puertas para el mismo numero. OJO, dos cosas que esta descripcion decia hasta el 2026-09-11: el stop no "se mueve" -nace en la orden, A-11- y ese tramo no es presupuesto de riesgo que se "guarde", porque el lote ya no se dimensiona sobre la caja entera; RN-012 dice que no se arriesga nunca
- **`stop_reduccion_fraccion`** (estrategia) — nivel al que se reduce el stop cuando la vela avanza (A-12)
- **`stop_reduccion_umbral_vela`** (estrategia) — parte de la vela a partir de la cual se baja el stop (40 o 50; A-12)
- **`stop_segundo_esquema`** (estrategia) — UNKNOWN A PROPOSITO desde la auditoria del 2026-09-10 (A-7 sigue resuelta): no hay un stop del segundo esquema distinto del primero. El trader dijo que es el MISMO en los dos, asi que un parametro aparte con el mismo valor son dos puertas para el mismo numero -lo que RN-012 prohibe expresamente para stop_proteccion_capital y ADR-0002 para todo-. Hay un unico esquema de stop y vive en stop_fraccion_caja. Leerlo falla, que es lo que debe pasar

## Quien lee cada valor

Un valor que ninguna regla nombra declara quien lo consumira; si no, seria un valor que nadie usa y nadie vigila (F12).

- `anclaje_h4` → F15
- `cuenta_objetivo` → F33
- `cuenta_pruebas` → F17, F33
- `filtro_noticias` → F33
- `firma` → F33
- `firma_apalancamiento` → F21, F33
- `firma_mensajes_dia_max` → F23, F24, F31
- `firma_noticias_restringe` → F33
- `firma_programa` → F33
- `firma_tipo_cuenta` → F33
- `huso_grafico` → ADR-0017
- `instrumento` → F24, F28, F31, F33
- `latencia_ms` → F24, F27
- `modelo_llenado` → F24, F27
- `saldo_inicial_cuenta` → F24, F33
- `sesgo_h4_regla` → ADR-0019
- `sesgo_h4_tope_velas` → F18

## Que dice cada uno

### `anclaje_h4`

donde empieza la rejilla H4. Es la medianoche del servidor, que por convencion de los brokers se escribe 17:00 America/New_York (ADR-0005) y que sigue el calendario de Nueva York, como confirmo broker_dst en la demo de FundedNext. En FTMO esta SIN VERIFICAR: se contrasta con su rejilla H4 real al medir A-28, y si no coincide se abre ambiguedad y este valor no se toca por su cuenta (ADR-0027). El trader lo ve como las 23:00 en su pantalla, y es cierto 337 dias al año; los otros 28 -8 a 28 de marzo y 25 a 31 de octubre, cuando la UE y EE.UU. no cambian la hora el mismo dia- lo ve a las 22:00. Escrito como una hora de un huso FIJO, el ancla caia una hora antes todo el invierno y repartia mal todas las velas H4, que es de donde sale el sesgo (ADR-0017)

### `base_calculo_objetivo`

distancia sobre la que se mide el objetivo. `caja_completa` es la distancia nivel 0 -> nivel 1; `riesgo_real` seria la distancia hasta stop_fraccion_caja. Hasta el 2026-09-11 esta descripcion anadia que la caja completa es "la misma que dimensiona el lote": desde ADR-0020 ya NO lo es, el lote se dimensiona hasta stop_fraccion_caja y solo el objetivo se mide sobre la caja entera. El RR realizado no es 1:3 sino objetivo_rr / stop_fraccion_caja, y es a proposito (RN-012). OJO (2026-09-16): esta descripcion justificaba el valor con que "el objetivo se traza CON la orden, antes de que el stop se mueva, asi que la unica distancia que existe en ese instante es la caja completa". Esa premisa esta revocada -el stop no se mueve, viaja en la orden desde el principio (A-11)-, asi que el argumento ya no discrimina. El valor NO se cambia: la decision queda para el consultor (A-18, nota en ADR-0014 y en RN-015)

Opciones: `caja_completa`, `riesgo_real`.

### `base_calculo_perdida_diaria`

base del tope de perdida del dia; el trader dice que el saldo inicial. Coincide en forma con la del tope de la firma -el saldo al corte diario, firma_base_perdida_diaria- y la coincidencia se declara, no se da por obvia: el porcentaje y la base del porcentaje de la firma son otros (ADR-0026, RN-029)

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

### `breaker_m1_criterio_ruptura`

criterio de ruptura del breaker (BOS) de M1, el que forma los dos esquemas de entrada. Era el unico de su familia que vivia en prosa -dentro de la descripcion de `se_da_esquema`- mientras sus hermanos (sesgo_h4_criterio_ruptura, zona_control_criterio_completada, break_even_criterio_ruptura y liquidez_m15_criterio_toma) ya eran parametros. NO es la toma de liquidez de M15, que exige cuerpo (RN-004): son dos rupturas distintas, y confundirlas es lo que hacia parecer que el corpus se contradecia (docs/validation/BREAKER-M1.md)

Opciones: `mecha`, `cuerpo`.

### `broker_dst`

con que calendario cambia la hora el servidor. El de FundedNext seguia el de Nueva York (valor `us` en su demo) y NO se hereda (ADR-0026): la ficha de FTMO dice "GMT+2 +DST" sin nombrar calendario, asi que se mide en su demo (A-28). Comprobarlo exige OBSERVAR UNA TRANSICION de hora, y por eso A-28 no se cierra antes del cambio de octubre. Desde ADR-0027 este reloj ya no mueve el dia de riesgo, que es civil; si decide si anclaje_h4 (17:00 Nueva York) cae de verdad en la medianoche del servidor. Este reloj y huso_grafico son DOS RELOJES DISTINTOS: este es el del servidor donde se ejecuta, aquel el de la pantalla donde el trader decide

Opciones: `us`, `eu`, `ninguno`.

### `broker_offset_base`

desfase base del reloj del servidor, medido en el terminal y no supuesto. En la demo de FundedNext valia 120 (GMT+2 en horario estandar) y NO se hereda (ADR-0026). FTMO declara "GMT+2 +DST" en su ficha de cuenta, que es una descripcion y no una medicion: se mide en su demo (A-28). Desde ADR-0027 no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor

### `cartucho_criterio`

que cuenta como cartucho gastado. LO QUE DIJO EL TRADER: solo una perdida, y no cuentan un break even, una entrada invalidada ni la reentrada despues de un equal. LO QUE ES NUESTRO (RN-016, RN-019): que el break even se clasifica por mecanismo -el stop que RN-014 llevo a la entrada- y no por el P/L neto de costes; que "la reentrada despues de un equal" se lee como la salida en negativo SIN stop de una entrada que se activo sin ruptura, que no suma; y que un cierre en el que salto el stop de stop_fraccion_caja suma sea cual sea la activacion, que el trader no dijo y pregunta A-31

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

cuenta a la que apunta el bot cuando este validado: la FTMO Account que sale del reto 2-Step (ADR-0026). QUE firma, programa y tipo de cuenta lo dicen firma, firma_programa y firma_tipo_cuenta

Opciones: `fondeada`, `demo`, `propia`.

### `cuenta_pruebas`

cuenta en la que se prueba el funcionamiento antes de la fondeada: la prueba gratuita de FTMO (ADR-0026), donde se miden A-27 y A-28. La demo de FundedNext del 2026-09-05 ya no cuenta

Opciones: `fondeada`, `demo`, `propia`.

### `dias_operables`

dias en los que el bot busca entradas. Era `texto` con el valor "lunes a viernes" y RN-001 lo usa como condicion EJECUTABLE, asi que el motor habria tenido que parsear espanol

Opciones: `lunes_a_viernes`, `todos_los_dias`.

### `filtro_noticias`

si se deja de operar alrededor de noticias de alto impacto. `no` es lo que hace EL TRADER -"a mi me es indiferente si hay noticia o no", fb-2026-09-09-sesion-01-3565552d- y es tambien lo que hace el BOT desde el 2026-09-14: la cuenta elegida es FTMO 2-Step Swing, que no tiene restricciones de noticias (ADR-0026, firma_noticias_restringe). Del 2026-09-12 al 2026-09-14 corrio con `regla` por ADR-0022, que suponia una cuenta fondeada con prohibicion; ese supuesto es cierto en FTMO Standard y en FundedNext, y por eso NO se eligio ninguna de las dos. La opcion `regla` se conserva: si el bot corre algun dia en una cuenta con restriccion, se cambia este valor, se revive RN-028 y hace falta un calendario economico, que es precondicion del pre-vuelo de F33

Opciones: `no`, `regla`.

### `filtro_spread`

si el bot descarta una entrada por spread alto (el trader dice que no filtra)

### `firma`

la firma de la cuenta fondeada. FundedNext se descarta porque no admite bots en cuentas de 50.000 o mas, ni en el reto ni en la cuenta fondeada

Opciones: `ftmo`, `fundednext`.

### `firma_apalancamiento`

apalancamiento del tipo Swing en forex (el Standard admite mas). Limita el lote: el margen es lotes x instrumento_contrato x precio / este numero, y con riesgo_por_operacion sobre la cuenta un stop muy corto puede pedir mas margen del que hay (ADR-0026, impacto). F21 lo comprueba con la distribucion real de cajas

### `firma_base_perdida_diaria`

el limite del dia se fija con el saldo al corte diario (medianoche CE(S)T, reloj_dia_riesgo) y no con el capital inicial: "Account balance at midnight CE(S)T of the previous day - 5% of the Initial Simulated Capital"

Opciones: `saldo_inicial_cuenta`, `saldo_corte_diario`.

### `firma_cierre_al_tope`

si, al alcanzar un limite de la firma con una posicion viva, el bot la cierra a mercado (RN-030). Nace el 2026-09-14 para sustituir el literal `si: "si"` que RN-029 llevaba en su cierre, donde RN-002 usa cierre_forzoso_fin_ventana: una opcion de una accion es un valor de negocio y vive aqui (ADR-0002). `si` es lo que decide ADR-0026: con el limite ya alcanzado la cuenta esta en infraccion, y dejar correr la posicion solo puede agrandar la perdida

Opciones: `si`, `no`.

### `firma_magnitud_vigilada`

la firma vigila EQUITY: saldo mas P/L flotante, swaps y comisiones ("equity cannot drop at any time"). Por eso la fase de riesgo del motor va por tick (ADR-0028)

Opciones: `saldo`, `equity`.

### `firma_margen_seguridad`

cuanto antes de cada limite de la firma saltan sus frenos (RN-029, RN-030, RN-031) y deja de caber una operacion nueva (RN-032). Llegar al limite ya es la infraccion, asi que frenar en el limite no evita perder la cuenta. El margen es el colchon para lo que la lectura prospectiva no ve: deslizamiento, gap, costes y el equity flotante antes de que un cierre se ejecute. El valor lo VALIDO EL CONSULTOR el 2026-09-17 (ADR-0031): 0,5 % del capital inicial es aproximadamente un riesgo nominal, y como riesgo_por_operacion va sobre el saldo actual y encoge con el drawdown, el colchon solo crece. Con el, en un dia que empieza en el capital inicial o por encima, la decima perdida seguida del dia ya no se abre. No cubre un gap mayor que el propio margen

### `firma_mensajes_dia_max`

por encima de este numero de peticiones al servidor en un dia, la firma lo trata como practica prohibida ("an excessive number of more than 2,000 server requests per day"). Restriccion de diseño de primera clase: la fase de estrategia va al cierre de M1 para no acercarse (ADR-0028)

### `firma_noticias_restringe`

si la cuenta prohibe o penaliza operar alrededor de noticias. Con firma_tipo_cuenta = swing, no. Si algun dia vale true, filtro_noticias pasa a `regla`, RN-028 se revive y hace falta un calendario economico: el pre-vuelo de F33 lo comprueba

### `firma_perdida_diaria_max`

perdida maxima del dia de la firma. El limite del dia es el saldo al corte diario (firma_base_perdida_diaria, reloj_dia_riesgo) menos este porcentaje del capital INICIAL, y lo vigila sobre firma_magnitud_vigilada. No es perdida_maxima_diaria, que es el freno del trader: con saldo al empezar el dia por encima de 111.111,11 el del trader es el MENOS restrictivo (ADR-0026)

### `firma_perdida_total_arrastra`

si la perdida maxima total arrastra con el saldo mas alto alcanzado. En el programa 2-Step NO: es estatica, capital inicial menos firma_perdida_total_max

### `firma_perdida_total_max`

perdida maxima total de la firma: el limite es el capital inicial menos este porcentaje, fijo en las dos fases y en la cuenta fondeada (firma_perdida_total_arrastra). El semanal del trader no lo cubre: se reinicia cada semana y este no se reinicia nunca

### `firma_programa`

programa del reto: reto, verificacion y cuenta fondeada, con la perdida maxima ESTATICA. El programa de una fase se descarta porque su perdida maxima arrastra y lleva regla del mejor dia

### `firma_tipo_cuenta`

tipo de cuenta. Se elige EN LA COMPRA y no se puede cambiar despues ("Change from Standard to Swing: Not allowed"). `swing` no restringe las noticias; `standard` prohibe abrir o cerrar -incluida la ejecucion de un stop o un objetivo- de dos minutos antes a dos despues de noticias seleccionadas en la cuenta fondeada

Opciones: `standard`, `swing`.

### `huso_grafico`

como se ETIQUETAN las horas en la pantalla del trader. No hay configuracion deliberada de huso: su plataforma muestra su hora local, que es la misma de huso_operativa. Sirve para traducir lo que el dice -"la vela empieza a las 23"- a un instante: 23:00 Madrid son las 21:00 UTC en verano y las 22:00 en invierno. NINGUNA regla cuelga de este parametro; las horas de la operativa cuelgan de huso_operativa y la rejilla H4 de anclaje_h4. Y NO es el reloj del servidor, que va en broker_offset_base + broker_dst y se mide en la demo de FTMO (A-28)

### `huso_operativa`

reloj del TRADER como persona: la hora a la que se sienta y a la que cierra, y de la que cuelgan ventana_inicio y ventana_fin. Es su reloj civil y por tanto cambia con el horario de verano. ADR-0005 lo fijo en Europe/Madrid, ADR-0012 lo cambio a un offset fijo apoyandose en que "la sesion desmintio Madrid" -que no ocurrio, ver ADR-0015- y ADR-0017 lo revierte: el trader opera siempre a la misma hora SUYA, sea cual sea la fecha

### `instrumento`

instrumento sobre el que opera la primera version. Sale de la evidencia, no de una respuesta: es el unico instrumento de todo el corpus grabado y se lee en pantalla. Por donde ampliar -NASDAQ, oro, pares sin gaps, futuros- lo dijo el trader y vive en fb-2026-09-09-sesion-01-6eceb844

### `instrumento_contrato`

tamano del contrato; con el se convierte el riesgo en lotes. Medido en una demo de FundedNext el 2026-09-05; se conserva como default porque EURUSD tiene las mismas especificaciones en casi cualquier bróker, pero NO está verificado en FTMO (A-27).

### `instrumento_digitos`

digits del simbolo; con 5 un punto es 0,00001 y un pip son 10 puntos. Medido en una demo de FundedNext el 2026-09-05; se conserva como default porque EURUSD tiene las mismas especificaciones en casi cualquier bróker, pero NO está verificado en FTMO (A-27).

### `instrumento_lote_minimo`

lote minimo que admite el broker; por debajo, la operacion se rechaza. Medido en una demo de FundedNext el 2026-09-05; se conserva como default porque EURUSD tiene las mismas especificaciones en casi cualquier bróker, pero NO está verificado en FTMO (A-27).

### `instrumento_lote_paso`

escalon del lote; el lotaje calculado se redondea a un multiplo de este paso. Medido en una demo de FundedNext el 2026-09-05; se conserva como default porque EURUSD tiene las mismas especificaciones en casi cualquier bróker, pero NO está verificado en FTMO (A-27).

### `instrumento_stops_level`

distancia minima a la que el broker admite un stop o un limite. Si la spec pide uno mas cerca, la respuesta es ABSTENERSE, nunca aproximar (MASTER_PLAN H.2). Medido en una demo de FundedNext el 2026-09-05; se conserva como default porque EURUSD tiene las mismas especificaciones en casi cualquier bróker, pero NO está verificado en FTMO (A-27). Y aqui el aviso pesa mas que en los otros cuatro: el stops level SI cambia de un broker a otro, y con 0 RN-026 no se activa nunca

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

### `orden_limite_nace`

en que momento nace la orden limite (A-29). `al_darse_el_esquema`: cuando se da uno de los dos esquemas de entrada, y la orden se marca en su bloque de origen ("apenas el breaker, o sea, marco mi orden limit", ev-v3-004201). `al_tomarse_la_liquidez`: en cuanto la liquidez de M15 esta tomada, en la primera zona de control que se completa, y desde ahi RN-006 la va moviendo (ev-v1-001358, ev-v3-002511, y la sesion 1 en v6 1:22:14, donde la orden ya esta en la zona de "posible breaker" y se activa sin validar). El corpus sostiene las dos. DEFAULT NUESTRO en la primera, porque es la unica frase que nombra el momento y porque con la segunda RN-008 -que prohibe abrir sin esquema- frenaria la propia colocacion y habria que reescribirla

Opciones: `al_darse_el_esquema`, `al_tomarse_la_liquidez`.

### `parciales`

si se toman parciales

Opciones: `si`, `no`.

### `perdida_maxima_diaria`

perdida acumulada en el dia que detiene la operativa; la base la fija base_calculo_perdida_diaria y el corte, reloj_dia_riesgo. Tras corregir la aritmetica de los cartuchos (ver RN-020) este es el UNICO freno del dia que existe

### `perdida_maxima_semanal`

perdida acumulada en la semana que detiene la operativa; la base la fija base_calculo_perdida_semanal y el corte, reloj_dia_riesgo

### `reentrada_tras_equal`

si, tras cerrarse una operacion que se activo sin ruptura -lo que el trader llama cerrar un equal-, se vuelve a entrar sin gastar intento (RN-019). La reentrada va por la via normal de colocacion (RN-011 y RN-015). Hasta el 2026-09-16 decia "se reentra al romper de nuevo", que no es lo que dice el literal

Opciones: `si`, `no`.

### `reloj_dia_riesgo`

en que reloj cae la medianoche que reinicia el tope diario, y el corte que reinicia el semanal. Sin esto, "el saldo inicial del dia" no dice cuando empieza el dia. `civil_operativa` es la medianoche en huso_operativa, el reloj civil del trader. Es lo que dice el reglamento de FTMO -"Account balance at midnight CE(S)T of the previous day"- y CE(S)T tiene hoy las mismas reglas de horario de verano que Europe/Madrid (ADR-0027). Hasta el 2026-09-14 valia `servidor`, un DEFAULT NUESTRO sin verificar (A-19), y la opcion `grafico` se sustituye por esta: el grafico del trader esta en ese mismo huso y serian dos puertas para el mismo instante. COINCIDENCIA DECLARADA, no obvia: la base del trader (base_calculo_perdida_diaria = saldo_inicial_dia) y la de la firma (firma_base_perdida_diaria = saldo_corte_diario) coinciden en FORMA y en el corte; NO coinciden ni el porcentaje ni la base del porcentaje (ADR-0026). FTMO no tiene tope semanal: la semana es un freno del trader y corta con este mismo reloj. Se queda CONFIRMED por el reglamento, y ADEMAS se comprueba en el panel de la prueba gratuita de FTMO dentro de A-28: la medianoche del servidor y la CE(S)T se separan una hora y equivocarse cuesta la cuenta

Opciones: `servidor`, `civil_operativa`.

### `reubicacion_cadencia`

cada cuanto se reubica la orden limite mientras no se activa (A-5)

Opciones: `cada_vela`, `al_romper`, `otra`.

### `riesgo_por_operacion`

riesgo por operacion (1 en backtest; 0,4-0,5 en fondeo). Desde ADR-0020 es lo que cuesta el stop DE VERDAD, no un nominal: el lote se dimensiona sobre la distancia hasta stop_fraccion_caja (lotaje_base)

### `saldo_inicial_cuenta`

saldo con el que arranca la cuenta: el capital simulado inicial de la cuenta FTMO de 100.000 (ADR-0026). NO es base de ningun calculo DEL TRADER: el lotaje va sobre base_calculo_riesgo (saldo_actual), el tope diario sobre base_calculo_perdida_diaria (saldo_inicial_dia) y el semanal sobre base_calculo_perdida_semanal (saldo_actual). SI es la base de los dos topes DE LA FIRMA: firma_perdida_diaria_max y firma_perdida_total_max son porcentajes de este capital (RN-029)

### `salida_sin_ruptura`

que se hace si la orden se activa sin ruptura (A-3)

Opciones: `cerrar_al_cierre`, `proteger_y_dejar`.

### `sesgo_h4_criterio_ruptura`

criterio de ruptura del extremo de la H4 anterior, del que depende el sesgo. Vivia dentro del nombre del enum `sesgo_h4_regla` (`vela_anterior_cierre_mecha`), que mezclaba sujeto y criterio; la forma ejecutable de F12 lo separa porque el criterio es un ARGUMENTO del predicado `rompe`, y escribirlo a pelo seria un valor de negocio en un campo ejecutable

Opciones: `mecha`, `cuerpo`.

### `sesgo_h4_regla`

que vela H4 fija el sesgo y cuando cambia (A-1). Desde F12 ninguna forma lo lee: mezclaba sujeto y criterio, y la forma los separa en el predicado `rompe` (que: vela_h4_previa) y en sesgo_h4_criterio_ruptura. Se conserva porque es lo que el trader respondio; lo que ejecuta el motor es lo otro (ADR-0019)

Opciones: `vela_anterior_color`, `vela_anterior_cierre_mecha`, `otra`.

### `sesgo_h4_tope_velas`

tope de la busqueda hacia atras del estado inicial del sesgo H4 (ADR-0044): se busca la ultima H4 que rompio un extremo de su anterior, como mucho en estas velas; si no hay ninguna, el sesgo es INSUFICIENTE y no se opera. PROVISIONAL: es una decision del proyecto, no del trader, y no sale del corpus; por eso es de `ejecucion` y no de `estrategia`, cuyos valores solo los dice el trader

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
