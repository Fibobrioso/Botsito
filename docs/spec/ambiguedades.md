<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Ambiguedades: lo que todavia no se sabe

`spec_version 18.0.0` · **sin sello**: el hash cubre knowledge/spec/parametros.yaml, knowledge/spec/strategy_spec.yaml, knowledge/spec/glossary.yaml y este documento no sale de ninguno de ellos

Como se cierra cada una: **RESUELTA** solo con un registro de feedback del trader (`RESOLVE_UNKNOWN`, activo); **DECIDIDA** por el consultor, con su ADR (ADR-0022); **ABIERTA** es la unica que se sigue abierta: si es una `pregunta` entra en el cuestionario de la sesion siguiente, y si es una `medicion` la cierra un dato y no se le pregunta al trader. Una RESUELTA se reabre con un registro `REOPEN`; una DECIDIDA, solo con otro ADR. Una `medicion` puede citar una fuente documental en vez de evidencia.

## ABIERTA (14)

### A-13 · break even al toque o con cuerpo · pregunta

Para poner el break even esperas a que se rompa la zona de control. ¿Qué tiene que pasar para que la des por rota? LO FIRME, ACTIVADO el 2026-09-29 (sesion 3, v9 0:55:48-0:56:39): al tocar («apenas toca, pues se pone en B la entrada»), mirado en M1, con el stop exactamente en la entrada, y despues el stop no se mueve (break_even_criterio_ruptura = mecha, fb-2026-09-29-sesion-03-2cff5008; RN-014, fb-2026-09-29-sesion-03-9f506366). SIGUE ABIERTA por orden del consultor: el corte de audio de v9 de 0:57:00 a 0:58:06 cae al final de su respuesta, y lo que pudo tapar se cierra con el audio de respaldo (docs/validation/SESION-03-EXTRACCION.md §2).

Afecta a: `break_even_criterio_ruptura`.

### A-16 · cuanto se separan las velas de Oanda de las de Dukascopy · medicion

¿como se comparan decisiones tomadas sobre velas de Oanda (FX Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milesima? Partida el 2026-09-12 (ADR-0024): aqui queda solo la MEDICION, que no la puede cerrar ninguna decision. El anexo del 2026-09-09 midio OTRA pareja -MT5/FundedNext contra Dukascopy, 2 puntos de mediana- y el lo dice: "queda una tercera fuente en juego, que es la del trader [...] esta medicion no la cubre". La decision de metodo que estaba mezclada aqui es A-23

### A-28 · el reloj del servidor de FTMO y su regla de horario de verano · medicion

MEDICION, no pregunta al trader. ¿cuanto va el reloj del servidor de FTMO por delante de UTC en horario estandar, y con que calendario cambia de hora: el de Nueva York, el europeo o ninguno? La ficha de FTMO dice "GMT+2 +DST" sin nombrar el calendario, y lo que midio la demo de FundedNext (120 minutos, calendario de Nueva York) no se hereda (ADR-0026). Desde ADR-0027 este reloj ya no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor y si anclaje_h4 (17:00 Nueva York) cae de verdad en su medianoche. COMPROBAR EL CALENDARIO EXIGE OBSERVAR UNA TRANSICION de hora en el terminal, asi que esta ambiguedad NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE: el desfase base se puede medir cualquier dia, la regla de horario de verano no. VERIFICACION EXPLICITA (añadida el 2026-09-14 al validar la rama): confirmar EN EL PANEL de la prueba gratuita de FTMO que el corte del dia de riesgo -cuando se recalcula el limite diario- cae a medianoche CE(S)T y NO a la medianoche del servidor. Las dos se separan una hora (el servidor va a GMT+2/+3 y CE(S)T a GMT+1/+2) y equivocarse cuesta la cuenta. reloj_dia_riesgo se queda CONFIRMED en `civil_operativa` por el reglamento (ADR-0027); si el panel dijera otra cosa, se reabre A-19 y el parametro vuelve a DEFAULT_AMBIGUOUS

Afecta a: `broker_offset_base`, `broker_dst`.

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente», fila R10: «Platform server time: MetaTrader 4, MetaTrader 5 = GMT+2 +DST».

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente», fila R10: «El calendario del +DST: NO ENCONTRADA».

### A-32 · el nivel que al romperse con mecha invalida la entrada · pregunta

En uno de tus vídeos descartas una entrada porque el precio rompe con mecha una línea horizontal que tenías dibujada. ¿Qué nivel marcaba esa línea? Si no lo recuerdas, no pasa nada.

Afecta a: `breaker_m1_criterio_ruptura`.

### A-35 · cuándo un pivote de M15 está formado · **BLOQUEANTE** · pregunta

Cuando marcas un alto o un bajo en M15 como liquidez, ¿en qué momento lo das por bueno? ¿Y qué haces si después el precio lo supera un poco?

Afecta a: `liquidez_m15_pivote_formado`.

### A-43 · si una liquidez de M15 tomada antes de las 7 cuenta para operar después · pregunta

Si el precio toma una liquidez antes de las 7, cuando todavía no ha empezado tu horario, ¿la tienes en cuenta para operar después? Nota medida: hoy el motor ya responde de hecho, y solo para una vela: la M15 que cierra a las 07:00 cuenta como toma dentro de la sesión; en construcción, la toma del bot es esa en 7 de los 40 días con toma. LO FIRME, ACTIVADO el 2026-10-11 (sesion 4, S-15, v10 1:46:13-1:47:16) como DESVIACION declarada de la regla «las en parte van a la sesion 5» (decision del consultor, punto 9): una liquidez tomada antes de las 7 SI la usa, siempre que la operacion se de desde las 7 («si el precio toma ese liquidez antes de tu horario, ¿lo usas para operar a partir de las 7? Sí.», ev-v10-014613-6cf002b2): toma_antes_de_la_ventana pasa de no_cuenta (PROVISIONAL, que decia lo contrario) a cuenta, CONFIRMED (fb-2026-10-04-sesion-04-c3d0c855). SIGUE ABIERTA por la segunda parte: si a las 6:45 la toma, el precio vuelve por encima y a las 7:20 la vuelve a tomar, no eligio entre «la de las 7:20 vale» y «esa liquidez ya esta gastada»; contesto que la liquidez se va actualizando y se toma «la más reciente». Va a la sesion 5.

Afecta a: `toma_antes_de_la_ventana`.

### A-44 · magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) · **BLOQUEANTE** · pregunta

¿Hay alguna pérdida a partir de la cual dejas de operar? ¿Cuándo vuelves a empezar a contar? RESPONDIDA en la sesion 3 (2026-09-29, v9 1:11:30-1:11:54) con una lectura que el registro no tiene: el tope no es un porcentaje sino 9 perdidas SEGUIDAS, sin importar el dia ni la semana («9 pérdidas seguidas» / «O en un día» / «Seguidas»; «el último cartucho es el noveno»). No encaja en perdida_trader_alcance ni en perdida_trader_unidad, asi que PARA (docs/runbooks/ACTIVAR-A35-A44.md §4) y sigue ABIERTA; lo que falta para escribir el tope es A-51.

Afecta a: `perdida_maxima_diaria`, `base_calculo_perdida_diaria`, `perdida_maxima_semanal`, `base_calculo_perdida_semanal`, `perdida_trader_alcance`, `perdida_trader_magnitud`, `perdida_trader_unidad`, `perdida_trader_dia_usd`, `perdida_trader_semana_usd`, `perdida_trader_reinicio_huso`.

### A-48 · qué velas forman el bloque de la caja · pregunta

Cuando trazas la caja de la entrada en M1, ¿qué vela o velas tomas como bloque para poner el 0 y el 1?

Afecta a: `orden_stop_punto`, `caja_bloque`.

### A-49 · si la caja se traza con la vela del bloque cerrada o en formación · pregunta

¿Trazas la caja cuando la vela del bloque ya ha cerrado, o mientras se está formando?

Afecta a: `caja_se_fija`.

### A-50 · para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera · pregunta

Para descartar una zona frente al nivel de la liquidez que se tomó, ¿cuenta solo el 0 de la caja o la caja entera? LECTURA CANDIDATA de la sesion 3 (2026-09-29, v9 0:51:23), NO activada: el trader no usa la posicion de la caja frente al nivel tomado como filtro («¿El 0 o el 0? No, no importa», y remite a sus ejemplos). Su respuesta general es que la caja va del punto de breaker al punto mas alto y que todo tiene que desarrollarse mas alla del nivel.

### A-53 · la orden sin llenar cuando el precio toma otra liquidez de M15 · pregunta

Tienes una orden stop puesta, sin llenar, y el precio toma otra liquidez de M15. ¿Qué haces con la orden? (a) la quito en ese momento y espero el punto de la liquidez nueva; (b) la dejo, y la muevo cuando aparezca el punto de la liquidez nueva; (c) otra, ¿cuál? Es la pregunta 21 de docs/sesion-4/PREGUNTAS.md.

Afecta a: `orden_pendiente_al_abrir_escenario`.

### A-54 · qué cuenta FTMO como petición al servidor y con qué margen frena el bot · medicion

Para el límite de 2.000 peticiones al servidor al día de FTMO (R13 de docs/validation/FTMO-REGLAS.md): ¿cuenta una petición rechazada, una modificación del stop, una cancelación y un cierre?; ¿con qué reloj corta FTMO ese día?; ¿qué hace el servidor al pasarse? Se mide en la demo (MedirDemoFTMO) o se pregunta al soporte; con la respuesta se fijan los umbrales del freno. Qué cuenta FTMO como mensaje (las rechazadas, las modificaciones, las cancelaciones) está preguntado al soporte de FTMO: enviado por Aleks el 2026-10-03 en el ticket VDW-DPMWR-965, preguntas 1 a 4 de su correo (literal en docs/validation/FTMO-REGLAS.md; docs/validation/FUENTES-FTMO.md), respondida en parte el 2026-10-05 (FTMO-REGLAS.md, recuadro de esa fecha). Si cuenta más de lo que cuenta el freno, los umbrales se revisan. Ningún ítem del corpus habla del límite: su fuente es documental, R13 de docs/validation/FTMO-REGLAS.md.

Afecta a: `freno_peticiones_aviso`, `freno_peticiones_corte`, `freno_bucle_repeticiones`, `freno_bucle_minutos`.

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente», fila R13: «an excessive number of more than 2,000 server requests per day».

### A-55 · qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta · medicion

R15 de docs/validation/FTMO-REGLAS.md prohíbe «perform gap trading [...] by opening simulated trades: [...] two hours or less before a relevant financial market is closed for at least two hours». No dice si colocar una orden pendiente en esas dos horas cuenta, ni si mover el precio de una ya puesta es colocarla, ni si una pendiente puesta antes que se llena dentro es «opening», ni qué mercado es el «relevant financial market» de EURUSD (el horario de EURUSD en los servidores de FTMO, o también el cierre de otras bolsas). Preguntado a soporte de FTMO, en inglés (docs/validation/CIERRES-DE-MERCADO.md §0.6, P1, P2 y P3): enviado por Aleks el 2026-10-03 en el ticket VDW-DPMWR-965, preguntas 5 a 9 de su correo: la 5 a la 7 son P1 (a-d), la 8 es P2 y la 9 es P3 (literal en docs/validation/FTMO-REGLAS.md; docs/validation/FUENTES-FTMO.md), respondida en parte el 2026-10-05 (FTMO-REGLAS.md, recuadro de esa fecha), y la pregunta 6 sigue sin respuesta; y con la respuesta se fija cierre_pendientes (y, si modificar no es colocar, se deja de negar en el broker). Ningún ítem del corpus habla de cierres de mercado: su fuente es documental, R15 y la respuesta literal del ticket en docs/validation/FTMO-REGLAS.md.

Afecta a: `cierre_pendientes`.

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente», fila R15: «two hours or less before a relevant financial market is closed for at least two hours».

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente»: «within two hours before a relevant market closes for at least two hours».

### A-56 · la regla del objetivo dicha por el trader frente a lo que mide su material · medicion

El trader dice, tres veces, que el stop va en el 0,8 y que el objetivo es 3 veces la distancia del 0 al 1 (A-18 y A-33, RESUELTAS por ADR-0073). Con esa combinacion el RR implicito de sus ganadoras sobre entrada-stop tendria que caer fuera de [3,00, 3,75), y en tres meses de sus libros cae dentro en 26 filas de 38 (ADR-0040). ¿Que explica la diferencia: donde queda el stop en sus backtests, como redondea FX Replay, otra cosa? Y las ganadoras de esos libros que cierran por debajo de 3R (una en agosto, dos en abril, una en mayo), que «nunca cierro antes del objetivo» no explica. NO SE LE PREGUNTA AL TRADER: ya contesto; se MIDE. La fila de agosto de ADR-0040 sale del xlsx del backtest de agosto, y en S-16 (sesion 4, v10 1:48:23-1:48:53) el trader da por bueno «el último» de sus dos backtests de agosto, el grabado en video, «porque incluye los break even» (que el xlsx sea el otro es lectura de la sesion, no su frase); sin agosto la region sigue poblada con abril y mayo. Lo que la resolveria lo dice ADR-0040 §2: un material que traiga la caja; y un libro de agosto que sea el que el trader da por bueno. F26 lee la diferencia como conocida.

Afecta a: `base_calculo_objetivo`, `objetivo_rr`, `stop_fraccion_caja`.

Fuente documental: `docs/adr/0040-la-combinacion-confirmed-del-objetivo-es-falsa.md`, «Decision»: «Una fila dentro basta, y hay 26 en 38.».

Fuente documental: `docs/adr/0040-la-combinacion-confirmed-del-objetivo-es-falsa.md`, «Impacto»: «Un bot construido hoy con ellos apuntaría a un RR realizado de 3,75, y el material dice 3,00.».

## DECIDIDA (7)

### A-15 · alcance de la ventana operativa · cerrada por `ADR-0024` el 2026-09-12

¿el bot busca solo en las dos sesiones de 07-11 y 11-15, o tambien en la de Nueva York? DECIDIDO por el consultor el 2026-09-12: NO se amplia en esta fase. No es una pregunta que el trader se reservara, es una que DEVOLVIO -"puedes buscar las operaciones donde sea, o sea, no hay problema"-, y toda su operativa GRABADA va de 07:00 a 15:00. Ampliar sin una sola sesion grabada en Nueva York meteria en el universo de etiquetado dias que nadie ha visto operar y cambiaria el sesgo H4 de la mitad. La capacidad se conserva: ampliar es cambiar ventana_inicio y ventana_fin, nada mas

Afecta a: `ventana_inicio`, `ventana_fin`.

### A-17 · noticias frente a la regla de la cuenta de fondeo · cerrada por `ADR-0026` el 2026-09-14

DESCARTADA una via el 2026-09-12: se penso que la pestaña `Prop firm` de FX Replay -que el trader tiene con el plan Pro- podria llevar dentro la ventana de noticias y el corte del dia de riesgo, y cerrar esta y A-19 de golpe. El trader responde que NO la tiene configurada con FundedNext. Sigue haciendo falta el reglamento. ¿QUE prohibe exactamente el reglamento de FundedNext sobre operar en noticias: que eventos, cuantos minutos antes y despues, y que sancion? Es un HECHO que se verifica en su reglamento, no una decision. Partida en dos el 2026-09-12 (ADR-0022): la decision de alcance -el bot no opera noticias en la v1 aunque la estrategia del trader si funcione dentro de ellas- se fue a A-22 y esta DECIDIDA; aqui se queda lo que hay que leer y medir. Sin esta respuesta, RN-028 sabe QUE bloquea y no CON QUE VENTANA. DECIDIDA el 2026-09-14 por ADR-0026, que cambia de firma. El reglamento se leyo ese dia y el supuesto era cierto donde se miro: FTMO Standard prohibe abrir o cerrar -incluida la ejecucion de un stop o un objetivo- de dos minutos antes a dos despues de noticias seleccionadas, con la cuenta como sancion, y FundedNext recorta el 40 % del beneficio operado cinco minutos antes y despues. Pero la cuenta elegida es FTMO 2-Step SWING, que no tiene restricciones de noticias, asi que la ventana deja de importar: filtro_noticias vuelve a `no` y RN-028 se descarta

Afecta a: `filtro_noticias`.

### A-19 · cuando empieza el dia y la semana de riesgo · cerrada por `ADR-0027` el 2026-09-14

DESCARTADA una via el 2026-09-12: la pestaña `Prop firm` de FX Replay no la tiene el trader configurada con FundedNext, asi que no hay atajo. Sigue siendo el panel de la cuenta (F17). ¿en que reloj cae la medianoche que reinicia el tope diario del 4,5 % y el domingo que reinicia el semanal: el del servidor del broker, que cambia con el calendario de Nueva York, o el del grafico? Hay que verificarlo en el panel de la cuenta, no suponerlo. DECIDIDA el 2026-09-14 por ADR-0027: con la firma elegida (ADR-0026) la contesta el reglamento, no el panel -"Account balance at midnight CE(S)T of the previous day"-. El corte es la medianoche CIVIL centroeuropea, que es el reloj del trader (huso_operativa), y no la del servidor, que era nuestro default. reloj_dia_riesgo pasa a `civil_operativa`, CONFIRMED. Lo que SI queda por medir -el reloj del servidor, que ya no decide el corte- es A-28

Afecta a: `reloj_dia_riesgo`.

### A-22 · si el bot opera noticias, y que pasa con la capacidad para otras cuentas · cerrada por `ADR-0022` el 2026-09-12

el trader opera noticias en sus cuentas propias -que no lo prohiben- y su estrategia funciona dentro de esos eventos. ¿el bot hace lo mismo? DECIDIDO por el consultor el 2026-09-12: NO en la primera version, porque va a una cuenta fondeada que puede prohibirlo como norma y la sancion es perder la cuenta aunque la operacion acabe en profit. La CAPACIDAD se conserva: `filtro_noticias` mantiene la opcion `no`, asi que el dia que el bot corra en una cuenta que lo permita se cambia el valor y nada mas. Lo que falta por saber -que ventana exacta- es A-17. SENTIDO INVERTIDO el 2026-09-14 por la enmienda de ADR-0022 (que la nombra, y por eso sigue siendo su decision): la cuenta elegida es FTMO 2-Step Swing, sin restriccion de noticias (ADR-0026), asi que el bot SI opera noticias, como el trader. La mitad que conserva la capacidad sigue en pie: si algun dia corre en una cuenta con restriccion, filtro_noticias pasa a `regla`, se revive RN-028 y hace falta un calendario economico (pre-vuelo de F33)

Afecta a: `filtro_noticias`.

### A-23 · que proveedor es la referencia para medir la fidelidad · cerrada por `ADR-0024` el 2026-09-12

el trader decide sobre velas de Oanda (FX Replay) y el bot se mide sobre otras. ¿cual es la referencia? DECIDIDO por el consultor el 2026-09-12: DUKASCOPY (ADR-0005), porque cubre 2026 entero, es publico y reproducible, y donde se puede comparar esta a 2 puntos del feed del broker. MT5/FundedNext no puede sustituirlo -no sirve los meses del paquete: cero velas M1 de mayo- y se usa para lo que si aporta: spread real, condiciones de ejecucion, reloj de servidor y paridad con Strategy Tester. La divergencia entre proveedores entra en F26 como MARGEN DECLARADO y no como ruido ignorado: una regla que depende de romper por una milesima puede cambiar de decision dentro de ese margen. Cuanto vale ese margen frente a Oanda es A-16, que sigue abierta

### A-24 · que hace que marques un pivote de M15 y no otro · cerrada por `ADR-0045` el 2026-09-24

Cuando en M15 ves varias zonas de liquidez posibles, ¿cuál eliges y por qué? ¿Hay algo que te haga descartar una?

### A-27 · las especificaciones de EURUSD en FTMO · medicion · cerrada por `ADR-0071` el 2026-10-09

MEDICION, no pregunta al trader. ¿que digits, tamaño de contrato, lote minimo, paso de lote y stops level tiene EURUSD en la cuenta de FTMO? Los cinco se midieron el 2026-09-05 en una demo de FundedNext, la firma que ADR-0026 descarta, y se conservan como DEFAULT declarado porque EURUSD tiene las mismas especificaciones en casi cualquier broker: no se heredan como medicion. El que mas puede diferir es el stops level, que en FundedNext valia 0 y dejaba RN-026 sin activarse nunca. Se mide en la prueba gratuita de FTMO con SymbolInfo* (junto con el lote maximo, el freeze level y los modos de llenado, que el registro todavia no guarda) y el pre-vuelo de F33 aborta si la cuenta real dice otra cosa. DECIDIDA el 2026-10-09 por ADR-0071 con la ejecucion 1 de MedirDemoFTMO en la prueba gratuita de FTMO (CSV congelado en data/manifests/demo_ftmo/, sha256 86f0df8b): digits 5, contrato 100000, lote minimo 0.01, paso 0.01 y stops level 0 (filas 6, 8, 9, 11 y 4), los mismos valores que se conservaban de FundedNext. El freeze level es 0, el lote maximo 50 y los modos de llenado FOK e IOC. Las ejecuciones 2 y 3 y el pre-vuelo de F33 vuelven a leer la ficha; una diferencia la reabre con otro ADR

Afecta a: `instrumento_digitos`, `instrumento_contrato`, `instrumento_lote_minimo`, `instrumento_lote_paso`, `instrumento_stops_level`.

Fuente documental: `docs/validation/FTMO-REGLAS.md`, «2. Las reglas, con su fuente», fila R11: «Lote mínimo, paso de lote, stops level, freeze level y modos de llenado: NO ENCONTRADA».

## RESUELTA (35)

### A-1 · sesgo H4

¿que vela H4 fija el sesgo y cuando cambia?

Afecta a: `sesgo_h4_regla`.

### A-2 · tercer cartucho · **BLOQUEANTE**

¿2 o 3 intentos por zona? (contradiccion ficha vs V4 0:48:41)

Afecta a: `cartuchos_max`.

### A-3 · salida sin ruptura

¿se cierra si no rompe? ¿cuando?

Afecta a: `salida_sin_ruptura`.

### A-4 · BE al tocar o al cierre · **BLOQUEANTE**

¿break-even al tocar el nivel o al cierre de vela? (V4 0:44:56)

Afecta a: `break_even_condicion`, `break_even_criterio_ruptura`.

### A-5 · cadencia de reubicacion

¿cada cuanto se reubica la orden pendiente?

Afecta a: `reubicacion_cadencia`.

### A-6 · cierre 15:00

¿cierre forzoso a las 15:00 y en que huso?

Afecta a: `ventana_fin`, `cierre_forzoso_fin_ventana`.

### A-7 · stop del 2.o esquema

¿donde va el stop en el segundo esquema de entrada?

Afecta a: `stop_fraccion_caja`, `stop_segundo_esquema`.

### A-8 · "dos velas como una" en mapeo

¿cuando dos velas cuentan como una estructura?

Afecta a: `mapeo_dos_velas`.

### A-9 · anclaje de la vela H4 (hora y huso del grafico) · **BLOQUEANTE**

¿a que hora y en que huso del grafico abre su H4? (se resuelve viendo su grafico: captura de la configuracion; y que ocurre en las semanas en que Europa y EE. UU. no coinciden en el cambio de hora)

Afecta a: `anclaje_h4`.

### A-10 · stop a 0,8: fijo o 0,75 + spread

¿el 0,8 es fijo o "0,75 mas el spread del momento"?

Afecta a: `stop_fraccion_caja`, `stop_colchon_spread`.

### A-11 · SL en la orden o tras el llenado

¿el SL va en la orden pendiente o se pone tras el llenado? RESPONDIDA por el trader el 2026-09-10: "el SL se pone junto a la orden limite, no cuando se apertura recien". Hasta entonces figuraba RESUELTA pero su valor era una INFERENCIA nuestra, que el barrido de fidelidad dejo anotada en la descripcion del parametro

Afecta a: `stop_en_orden_pendiente`.

### A-12 · porcentaje de vela transcurrido para bajar la proteccion a 0,50: 40 % (transcripcion heredada) o 50 % (large-v3, V1 0:15:59)

¿a partir de que parte de la vela bajas el stop a 0,50?

Afecta a: `stop_reduccion_umbral_vela`, `stop_reduccion_fraccion`.

### A-14 · los 28 dias al año en que su horario y la rejilla H4 no cuadran

del 8 al 28 de marzo y del 25 al 31 de octubre, la UE y EE.UU. no cambian la hora el mismo dia, asi que la primera H4 se ve a las 22:00 y no a las 23:00: sus dos sesiones dejan de empezar en la apertura de una vela. RESPONDIDA de hecho el 2026-09-10: el consultor informa de que el trader ES CONSCIENTE de ese cambio en la estructura de las velas, usa las velas tal cual -no reancla la rejilla- y mantiene el mismo rango de horarios. CERRADA el 2026-09-12 con la frase que le faltaba: el consultor la confirma por escrito y queda registrada como REFERIDA, igual que se cerro A-11

Afecta a: `ventana_inicio`, `ventana_fin`.

### A-18 · base sobre la que se mide el objetivo 1:3 · pregunta

¿Cómo decides dónde va el stop y dónde va el objetivo? En algún vídeo hablas de poner el stop en dos tiempos: ¿cómo funciona eso? RESUELTA el 2026-10-04 en la sesion 4 (S-3, v10 0:35:59-0:39:48; ADR-0073): el stop va ya en el 0,8 al poner la orden («Sería directamente a 0.8»); el 1 «se usa al comienzo pero no de ejecución, sino como planteamiento»; el objetivo se mide del 0 al 1 y el lote del 0 al 0,8 («se usa de 0 a 1 para el cálculo de 1 a 3 [...] para la toma de la operativa se usa de 0 a 0,8»). No hay stop en dos tiempos en la ejecucion. Ningun valor cambia: base_calculo_objetivo, objetivo_rr, stop_fraccion_caja y lotaje_base ya estaban CONFIRMED con lo mismo desde la sesion 3. Lo que el material contradice (ADR-0040, enmendado por ADR-0073) es una medicion y va en A-56 (fb-2026-10-04-sesion-04-87ccb0ee).

Afecta a: `base_calculo_objetivo`, `objetivo_rr`.

### A-20 · cuantas zonas de control invalidan un esquema

RN-009 afirma que con mas de una zona de control no hay trade, pero el literal que la sostiene dice "por lo general solo buscamos uno", que no es una prohibicion dura. ¿es regla o es tendencia? ¿dos zonas invalidan SIEMPRE el esquema, o hay casos en que opera igual? El valor 1 es un default nuestro hasta que lo diga. RESPONDIDA por escrito el 2026-09-11: es REGLA -"solo 1 zona control bro. si hay 2 se descarta"- y ratifica tambien el descarte, no solo el numero (fb-2026-09-09-sesion-01-1b2203b0)

Afecta a: `zonas_control_max_por_esquema`.

### A-21 · que es una zona de control limpia, sin ruido · **BLOQUEANTE** · pregunta

Antes de entrar dices que la zona de control tiene que ser limpia, sin mucho ruido. ¿Qué miras para decidir que una zona está limpia? LECTURA CANDIDATA de la sesion 3 (2026-09-29, v9 1:19:57), NO activada: zona limpia = sin alternancia de colores («que no haya una vela verde, una vela bajista, una vela verde, una bajista»). No es ninguna de las dos opciones de zona_control_limpia; anadirla al enum obliga a tocar LECTURAS_LIMPIA del motor, que es rama de codigo. RESUELTA el 2026-10-04 en la sesion 4 (S-10, v10 1:17:25–1:17:31, 1:17:34–1:17:46 y 1:19:57–1:20:27): «¿una zona se limpia si hay velas verdes y rojas o terrenos rojos? ¿Es solo eso? Claro, exacto.»; el numero de velas del retroceso «es indiferente, no importa»; y si se alternan antes de la ruptura del posible punto de breaker «quedaría invalidado» (fb-2026-10-04-sesion-04-22d08cbf). Activada el 2026-10-12 en trabajo/activar-sesion-04-motor (ADR-0076): «sin alternancia de colores» es lo que RN-009 ya filtra, porque cada paso de vela contraria a vela del color de la entrada forma una zona de control que zonas_control_max_por_esquema = 1 rechaza (medido con series sinteticas en compra y en venta), asi que zona_control_limpia = solo_una_zona_de_control, la opcion que ya existia, sin sumar ninguna al enum. Dos casos en que la lectura literal y el motor no coinciden van a la sesion 5: una vela sin cuerpo en medio del retroceso y el breaker contrario que rompe con mecha.

Afecta a: `zona_control_limpia`.

### A-25 · la vida de la marca de liquidez de M15 · pregunta

Una vez que tienes marcada la liquidez en M15, a veces el precio forma después otro alto o bajo por ese mismo lado. ¿Qué haces entonces con la marca que ya tenías? RESUELTA el 2026-10-04 en la sesion 4 (S-18, v10 1:51:52-1:54:34): la marca del alto viejo se descarta y pasa al nuevo («el más reciente es lo que importa [...] Paso al nuevo»), que es lo que ADR-0045 ya decidio (A-24: el pivote mas reciente ya formado); y la toma de otra liquidez reinicia los tres intentos («para nuevamente pues reiniciar los tres intentos»): intentos_tras_toma_nueva queda CONFIRMED en vuelven_a_cartuchos_max, el mismo valor, y cartuchos_reinicio ratificado (fb-2026-10-04-sesion-04-b3c218ce). El trader dice que el «se iria por una cuarta» pero lo deja en 3: cartuchos_max no se toca.

Afecta a: `cartuchos_reinicio`, `intentos_tras_toma_nueva`.

### A-26 · el flujo de M15 cuando va contra el sesgo de H4 · pregunta

A veces el sesgo de H4 va en un sentido y el flujo que ves en M15 va en el contrario. Cuando pasa eso, ¿qué haces? RESUELTA el 2026-09-29 en la sesion 3 (v9 0:19:17): «nosotros el sesgo ya nos define qué vamos a buscar, luego nos enfocamos solo en M15, tratar de buscar a favor»: manda el sesgo y en M15 solo se busca a favor (fb-2026-09-29-sesion-03-fc2c5c1f).

### A-29 · cuando nace la orden limite · pregunta

¿En qué momento pones por primera vez la orden límite en una zona? RESUELTA el 2026-10-02 con la respuesta grabada de la sesion 3 (v9 0:01:43): «Lo primero es que primero se desarrolla una toma de liquidez Para recién nosotros poder trazar los posibles puntos de breaker»; es `al_aparecer_punto_de_breaker` (fb-2026-09-29-sesion-03-d3063920; el contexto de la pregunta, en docs/validation/SESION-03-EXTRACCION.md §3.4).

Afecta a: `orden_limite_nace`.

### A-30 · la orden limite pendiente al llegar el fin de la ventana · pregunta

Si se acaba tu horario de operar y tienes una orden límite puesta que todavía no se ha llenado, ¿qué haces con ella? RESUELTA el 2026-10-04 en la sesion 4 (S-5, v10 0:54:27-0:54:51): se quita, a las 11 y a las 3, «porque siempre se va a ir actualizando la orden [...] no va a haber órdenes que a lo mejor se pueden tomar a las 3 o fuera de horario» (fb-2026-10-04-sesion-04-766c8d2e). orden_pendiente_al_abrir_sesion queda CONFIRMED en se_retira, el mismo valor (RN-035 deja de ser PROVISIONAL). RESERVA: la pregunta fue dirigida (SESION-04-EXTRACCION.md §3.6); lo que sostiene el cierre es la razon del trader. «Un minuto antes» es frase del consultor y no se fija. A ventana_fin la retirada la hace hoy el cableado al terminar el dia (ADR-0053 §6) sin regla de la spec: la rama ventana_fin de RN-035 va a trabajo/activar-sesion-04-motor.

Afecta a: `orden_pendiente_al_abrir_sesion`.

### A-31 · el stop entero de una entrada que se activo sin ruptura · pregunta

Si una entrada se activa sin que se haya dado la ruptura y acaba tocando el stop, ¿cómo la cuentas en tus intentos? RESUELTA el 2026-09-29 en la sesion 3 (v9 1:26:12): «si llega a tocar el stop se considera como un loss … gastaría un intento»: la lectura de RN-016 era la del trader (fb-2026-09-29-sesion-03-d36ba0d2).

### A-33 · tres ganadoras que cierran por debajo de 3R · pregunta

¿Alguna vez cierras una operación ganadora antes de que llegue al objetivo? ¿En qué casos? RESUELTA el 2026-10-04 en la sesion 4 (S-12, v10 1:27:04-1:27:36 y 1:29:02-1:29:21; ADR-0073): nunca; «todo es 13 o sea fijo es 13 la regla es esa [...] respecto al 1 de la caja», sin parciales y sin dejar correr. RESERVA LITERAL del trader: «no vamos a dejar correr nada por ahora» (ev-v10-012704-d3facd31): lo de los primeros videos queda de lado, no negado. Las ganadoras del material que cierran por debajo de 3R, que esta respuesta no explica, pasan a A-56 (medicion). Ningun valor cambia: parciales, objetivo_rr y base_calculo_objetivo ya estaban CONFIRMED (fb-2026-10-04-sesion-04-df162e6e).

Afecta a: `parciales`, `objetivo_rr`.

### A-34 · vela H4 previa que rompe ambos extremos · pregunta

Si la vela de H4 anterior rompe los dos extremos de la vela que tenía antes, ¿qué sesgo tomas para la sesión? RESUELTA el 2026-09-29 en la sesion 3 (v9 0:16:19): «si rompe por los dos, como te digo, importa el color de la vela»: con la doble ruptura el sesgo lo decide el color con que cierra la vela (fb-2026-09-29-sesion-03-617f496a).

### A-36 · en qué punto de la mecha va la orden límite · pregunta

Dijiste que la orden límite siempre va en la mecha. ¿En qué punto de la mecha la colocas? RESUELTA el 2026-10-04 en la sesion 4 (S-22, v10 1:02:14-1:02:37): «exactamente en el 0 contando la mecha [...] No depende de nada, siempre es la mecha», y sin tener en cuenta el spread («No, no tengo en cuenta el split al ponerla»). La pregunta hablaba de orden LIMITE; desde A-47 la entrada es con orden STOP, y la respuesta vale para esa orden, que es la que el trader pone hoy. El motor ya lo hace: el 0 de la caja es el extremo con mecha del ultimo pivote de M1 (ADR-0064 §2) y la stop se coloca en ese precio sin sumar el spread (tests/unit/test_orden_en_el_0_con_mecha.py lo congela). Registro fb-2026-10-04-sesion-04-bbfb5c98, que supersede al REOPEN fb-2026-09-29-sesion-03-f3caeb2d. C6 (v7 n.o 3, la orden 2 puntos mas alla del 0) sigue sin explicar, anotada en las candidatas sin abrir.

### A-37 · en qué temporalidad se busca la vela contraria de la que sale el stop · pregunta

Dijiste que el stop se define desde el punto más bajo donde se genera la vela contraria. ¿En qué temporalidad miras esa vela? RESUELTA el 2026-09-29 en la sesion 3 (v9 1:39:18): «M1», a «para precisar, M1, M15 u otra» (fb-2026-09-29-sesion-03-91eeee94).

### A-38 · cuándo se da por anulada una orden límite que el precio deja sin llenar · pregunta

Si pones una orden límite y el precio se aleja sin llenarla, ¿cuándo la das por anulada? RESUELTA el 2026-09-29 en la sesion 3 (v9 1:32:07): «sigue vivo hasta que se desarrolle otro posible punto de breaker», y entonces la orden se actualiza; que el precio se aleje no la anula (fb-2026-09-29-sesion-03-c7fa3068).

### A-39 · qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo · pregunta

Cuando empieza la segunda sesión y el sesgo de H4 ha cambiado, ¿qué haces con lo que traes de la primera, ya sea una orden puesta o una operación abierta? RESUELTA el 2026-10-04 en la sesion 4 (S-5, v10 0:56:03-0:56:15): la orden puesta se quita al abrir la segunda sesion, cambie o no el sesgo («Sí, se quita»; fb-2026-10-04-sesion-04-dd888b55; orden_pendiente_al_abrir_sesion = se_retira, CONFIRMED, RN-035); la operacion ABIERTA ya la cerraba RN-002 un minuto antes del fin de su vela H4 (sesion 3, S-1, ADR-0060). RESERVA: pregunta dirigida («Se quita, ¿verdad?»); coincide con la regla general de 54:38 y con la independencia de las sesiones (A-46). Lo que el corte de audio de v9 0:28:49-0:29:53 dejo sin oir queda contestado aqui.

Afecta a: `orden_pendiente_al_abrir_sesion`.

### A-40 · qué se hace con el stop después del break even · pregunta

Una vez que la operación está en break even, ¿qué haces con el stop a partir de ahí? RESUELTA el 2026-09-29 en la sesion 3 (v9 0:58:56): «no definimos parciales, o sea lo dejamos ahí quieto»: despues del break even el stop no se mueve (el trader entendio la pregunta como de parciales) (fb-2026-09-29-sesion-03-7a79dcd7).

### A-41 · si hay un tope de entradas por día, aparte de los cartuchos · pregunta

¿Hay algo que limite cuántas entradas haces? ¿Cómo lo cuentas? RESUELTA el 2026-09-29 en la sesion 3 (v9 1:31:00): «Sí, serían tres intentos por liquidez» y «¿El máximo es por día? No, no, por liquidez»: no hay tope por dia, aparte de los tres cartuchos por liquidez (la cifra la propuso el consultor tras un «no sé, dime tú») (fb-2026-09-29-sesion-03-7b87c3ee).

### A-42 · con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 · **BLOQUEANTE** · pregunta

Tu horario de operar, de 7 a 15, ¿con qué reloj lo cuentas? ¿Cambia algo en invierno? RESUELTA el 2026-10-06 (ADR-0069): con la REJILLA H4 de anclaje_h4. Sus dos sesiones son las velas H4 que empiezan en ancla + 8 h y ancla + 12 h; en su grafico, que va en Europe/Madrid, son 07-11 y 11-15 casi todo el año y 06-10 y 10-14 las semanas en que Europa y EE. UU. no coinciden en el horario de verano (H2b de RELOJ-INVIERNO.md). Lo dijo en la sesion 4, S-7 («sería de 6 a 10 [...] después del día 25», ev-v10-010429-0c93f24a), y por escrito el 2026-10-06, con las capturas en el corpus: «1-B)», a las 7 desde el lunes 2 de noviembre (fb-2026-10-04-sesion-04-fb7831cc), y «si es por cuestion horaria se oepra a las 6» (fb-2026-10-04-sesion-04-af490a3a). En UTC, con zoneinfo: 05:00-13:00 con Nueva York en horario de verano y 06:00-14:00 si no. La lectura provisional de abajo (ADR-0059) era H1, que la medida de enero descarto. LECTURA PROVISIONAL el 2026-09-29 (ADR-0059, decision del consultor): las sesiones 07-11 y 11-15 van fijas en el reloj del grafico (UTC+2) todo el ano; en invierno equivalen a 06:00-14:00 de Madrid. huso_operativa NO cambia: en el motor es tambien el reloj del dia de riesgo, y separar los dos relojes es rama de codigo, requisito previo de toda corrida de invierno. Fuente: la sesion 3, v9 1:07:53 y 1:08:09, y el tramo 1:06:38-1:07:51 solo en su version con mascara (docs/validation/SESION-03-EXTRACCION.md). El trader dijo «creo»: confirmar en la proxima sesion; hasta entonces sigue ABIERTA. DESDE EL 2026-09-30 (ADR-0063, ACEPTADO) los dos relojes estan separados: la ventana se cuenta con el reloj que dice reloj_sesiones -hoy `civil_operativa`, sin cambio-, y aplicar esta lectura sera pasarlo a `grafico`; huso_operativa queda como reloj del dia de riesgo.

Afecta a: `reloj_sesiones`.

### A-45 · en qué granularidad se evalúa «cierra con cuerpo» en la toma de liquidez de RN-004 · pregunta

Cuando dices que en M15 tiene que cerrar con cuerpo, ¿esperas a que cierre la vela de 15 minutos, o te basta con que una vela de 1 minuto cierre con cuerpo pasando el nivel? RESUELTA el 2026-09-29 en la sesion 3 (v9 0:40:38): «esta es la vela de M1 que rompe la zona de M15 y lo hace con cuerpo», confirmado a las 0:42:28: la toma la hace una vela de M1 que cierra con cuerpo pasado el nivel; la mecha solo vale para el punto de breaker en M1 (fb-2026-09-29-sesion-03-b2e074e3).

Afecta a: `liquidez_m15_criterio_toma`.

### A-46 · si una toma de liquidez de una sesion anterior del mismo dia sigue valiendo en la siguiente · pregunta

Si la liquidez se tomó en una sesión anterior del mismo día (por ejemplo en la de 07 a 11, la que tú llamas Londres), ¿sigue valiendo para operar en la siguiente (la de 11 a 15, la que llamas Nueva York), o en esa sesión esperas una toma nueva? Repregunta anotada: hoy el motor la da por válida, porque `liquidez_tomada` no caduca al abrir la sesión (solo `sesgo` caduca). RESUELTA el 2026-09-29 en la sesion 3 (v9 0:32:53): cada sesion es «un mundo diferente» («Claro, exacto») y «no importa cómo terminó la primera operación»: cada toma nueva de M15 abre un escenario, sin tope diario de escenarios (fb-2026-09-29-sesion-03-5021677e).

### A-47 · el tipo de orden de entrada, stop o límite · **BLOQUEANTE** · pregunta

Cuando pones la orden en el punto de breaker, ¿quieres entrar cuando el precio rompe ese punto o cuando el precio vuelve a él? RESUELTA el 2026-09-29 en la sesion 3 (v9 0:01:24): «aquí queda confirmado que se entra siempre por stop» / «Sí, exacto»: la orden de entrada es una STOP en la ruptura (entrada_tipo_orden = stop_en_ruptura) (fb-2026-09-29-sesion-03-92a38105).

Afecta a: `entrada_tipo_orden`.

### A-51 · qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar · **BLOQUEANTE** · pregunta

Dijiste que paras tras 9 pérdidas seguidas, sin importar el día ni la semana. ¿Qué corta la racha: una ganadora, un break even? Y después de la novena, ¿cuándo vuelves a operar? RESUELTA el 2026-10-04 en la sesion 4 (S-8, v10 1:06:53–1:07:08, 1:07:15–1:07:41 y 1:08:04–1:08:28): un break even no corta la racha -«no corta la racha como tal»-, solo una ganadora; tras la novena vuelve «al día siguiente», y «la racha sigue de un día a otro y una semana otra» (fb-2026-10-04-sesion-04-8e2d728a; racha_perdidas_max = 9, racha_perdidas_corte = ganadora, racha_perdidas_reinicio = nunca, racha_perdidas_reanudacion = dia_siguiente; RN-036, ADR-0077). Activada el 2026-10-12 en trabajo/activar-sesion-04-motor.

Afecta a: `racha_perdidas_max`, `racha_perdidas_corte`, `racha_perdidas_reinicio`, `racha_perdidas_reanudacion`.

### A-52 · cuántos escenarios puede abrir una misma sesión como máximo · pregunta

En una misma sesión, cada vez que el precio toma una liquidez nueva de M15, ¿vuelves a buscar entrada? (a) sí, todas las veces, no hay máximo; (b) hasta un número de liquidez por sesión, ¿cuántas?; (c) otra, ¿cuál? Es la pregunta 20 de docs/sesion-4/PREGUNTAS.md. RESUELTA el 2026-10-04 en la sesion 4 (S-20, v10 1:54:49-1:55:04 y 1:56:40-1:56:55): opcion (a), sin maximo; «tomamos todas las entradas ganadoras o perdidas que se puedan dar en una sesión», hasta que salta el tope de perdida (fb-2026-10-04-sesion-04-f0e58d1f; max_escenarios_por_sesion queda CONFIRMED en sin_limite, el mismo valor). Las «dos entradas por dia» de v4 quedan descartadas.

Afecta a: `max_escenarios_por_sesion`.
