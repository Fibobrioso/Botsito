<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Ambiguedades: lo que todavia no se sabe

`spec_version 12.2.2` · **sin sello**: el hash cubre knowledge/spec/parametros.yaml, knowledge/spec/strategy_spec.yaml, knowledge/spec/glossary.yaml y este documento no sale de ninguno de ellos

Como se cierra cada una: **RESUELTA** solo con un registro de feedback del trader; **DECIDIDA** por el consultor, con su ADR (ADR-0022); **ABIERTA** es la unica que se sigue abierta: si es una `pregunta` entra en el cuestionario de la sesion siguiente, y si es una `medicion` la cierra un dato y no se le pregunta al trader.

## ABIERTA (21)

### A-13 · break even al toque o con cuerpo · pregunta

Para poner el break even esperas a que se rompa la zona de control. ¿Qué tiene que pasar para que la des por rota?

Afecta a: `break_even_criterio_ruptura`.

### A-16 · cuanto se separan las velas de Oanda de las de Dukascopy · medicion

¿como se comparan decisiones tomadas sobre velas de Oanda (FX Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milesima? Partida el 2026-09-12 (ADR-0024): aqui queda solo la MEDICION, que no la puede cerrar ninguna decision. El anexo del 2026-09-09 midio OTRA pareja -MT5/FundedNext contra Dukascopy, 2 puntos de mediana- y el lo dice: "queda una tercera fuente en juego, que es la del trader [...] esta medicion no la cubre". La decision de metodo que estaba mezclada aqui es A-23

### A-18 · base sobre la que se mide el objetivo 1:3 · pregunta

Cuando trazas el objetivo de una operación, ¿qué distancia tomas como referencia para calcularlo?

Afecta a: `base_calculo_objetivo`, `objetivo_rr`.

### A-21 · que es una zona de control limpia, sin ruido · **BLOQUEANTE** · pregunta

Antes de entrar dices que la zona de control tiene que ser limpia, sin mucho ruido. ¿Qué miras para decidir que una zona está limpia?

### A-25 · la vida de la marca de liquidez de M15 · pregunta

Una vez que tienes marcada la liquidez en M15, a veces el precio forma después otro alto o bajo por ese mismo lado. ¿Qué haces entonces con la marca que ya tenías?

Afecta a: `cartuchos_reinicio`.

### A-26 · el flujo de M15 cuando va contra el sesgo de H4 · pregunta

A veces el sesgo de H4 va en un sentido y el flujo que ves en M15 va en el contrario. Cuando pasa eso, ¿cómo marcas la liquidez en M15?

### A-27 · las especificaciones de EURUSD en FTMO · medicion

MEDICION, no pregunta al trader. ¿que digits, tamaño de contrato, lote minimo, paso de lote y stops level tiene EURUSD en la cuenta de FTMO? Los cinco se midieron el 2026-09-05 en una demo de FundedNext, la firma que ADR-0026 descarta, y se conservan como DEFAULT declarado porque EURUSD tiene las mismas especificaciones en casi cualquier broker: no se heredan como medicion. El que mas puede diferir es el stops level, que en FundedNext valia 0 y dejaba RN-026 sin activarse nunca. Se mide en la prueba gratuita de FTMO con SymbolInfo* (junto con el lote maximo, el freeze level y los modos de llenado, que el registro todavia no guarda) y el pre-vuelo de F33 aborta si la cuenta real dice otra cosa

Afecta a: `instrumento_digitos`, `instrumento_contrato`, `instrumento_lote_minimo`, `instrumento_lote_paso`, `instrumento_stops_level`.

### A-28 · el reloj del servidor de FTMO y su regla de horario de verano · medicion

MEDICION, no pregunta al trader. ¿cuanto va el reloj del servidor de FTMO por delante de UTC en horario estandar, y con que calendario cambia de hora: el de Nueva York, el europeo o ninguno? La ficha de FTMO dice "GMT+2 +DST" sin nombrar el calendario, y lo que midio la demo de FundedNext (120 minutos, calendario de Nueva York) no se hereda (ADR-0026). Desde ADR-0027 este reloj ya no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor y si anclaje_h4 (17:00 Nueva York) cae de verdad en su medianoche. COMPROBAR EL CALENDARIO EXIGE OBSERVAR UNA TRANSICION de hora en el terminal, asi que esta ambiguedad NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE: el desfase base se puede medir cualquier dia, la regla de horario de verano no. VERIFICACION EXPLICITA (añadida el 2026-09-14 al validar la rama): confirmar EN EL PANEL de la prueba gratuita de FTMO que el corte del dia de riesgo -cuando se recalcula el limite diario- cae a medianoche CE(S)T y NO a la medianoche del servidor. Las dos se separan una hora (el servidor va a GMT+2/+3 y CE(S)T a GMT+1/+2) y equivocarse cuesta la cuenta. reloj_dia_riesgo se queda CONFIRMED en `civil_operativa` por el reglamento (ADR-0027); si el panel dijera otra cosa, se reabre A-19 y el parametro vuelve a DEFAULT_AMBIGUOUS

Afecta a: `broker_offset_base`, `broker_dst`.

### A-29 · cuando nace la orden limite · pregunta

¿En qué momento pones por primera vez la orden límite en una zona?

Afecta a: `orden_limite_nace`.

### A-30 · la orden limite pendiente al llegar el fin de la ventana · pregunta

Si se acaba tu horario de operar y tienes una orden límite puesta que todavía no se ha llenado, ¿qué haces con ella?

### A-31 · el stop entero de una entrada que se activo sin ruptura · pregunta

Si una entrada se activa sin que se haya dado la ruptura y acaba tocando el stop, ¿cómo la cuentas en tus intentos?

### A-32 · el nivel que al romperse con mecha invalida la entrada · pregunta

En uno de tus vídeos descartas una entrada porque el precio rompe con mecha una línea horizontal que tenías dibujada. ¿Qué nivel marcaba esa línea?

Afecta a: `breaker_m1_criterio_ruptura`.

### A-33 · tres ganadoras que cierran por debajo de 3R · pregunta

En tu material hay algunas operaciones ganadoras que se cerraron antes de llegar al objetivo. ¿Qué pasó en esas operaciones?

Afecta a: `parciales`, `objetivo_rr`.

### A-34 · vela H4 previa que rompe ambos extremos · pregunta

Si la vela de H4 anterior rompe los dos extremos de la vela que tenía antes, ¿qué sesgo tomas para la sesión?

### A-35 · cuándo un pivote de M15 está formado · **BLOQUEANTE** · pregunta

Cuando marcas un alto o un bajo en M15 como liquidez, ¿en qué momento lo das por bueno? ¿Y qué haces si después el precio lo supera un poco?

### A-36 · en qué punto de la mecha va la orden límite · pregunta

Dijiste que la orden límite siempre va en la mecha. ¿En qué punto de la mecha la colocas?

### A-37 · en qué temporalidad se busca la vela contraria de la que sale el stop · pregunta

Dijiste que el stop sale del punto donde se genera la vela contraria. ¿En qué temporalidad buscas esa vela?

### A-38 · cuándo se da por anulada una orden límite que el precio deja sin llenar · pregunta

Si pones una orden límite y el precio se aleja sin llenarla, ¿cuándo la das por anulada?

### A-39 · qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo · pregunta

Cuando empieza la segunda sesión y el sesgo de H4 ha cambiado, ¿qué haces con lo que traes de la primera, ya sea una orden puesta o una operación abierta?

### A-40 · qué se hace con el stop después del break even · pregunta

Una vez que la operación está en break even, ¿qué haces con el stop a partir de ahí?

### A-41 · si hay un tope de entradas por día, aparte de los cartuchos · pregunta

Aparte de lo que ya dijiste sobre los intentos por zona, ¿hay algo que limite cuántas entradas haces en un día?

## DECIDIDA (6)

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

## RESUELTA (14)

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

### A-20 · cuantas zonas de control invalidan un esquema

RN-009 afirma que con mas de una zona de control no hay trade, pero el literal que la sostiene dice "por lo general solo buscamos uno", que no es una prohibicion dura. ¿es regla o es tendencia? ¿dos zonas invalidan SIEMPRE el esquema, o hay casos en que opera igual? El valor 1 es un default nuestro hasta que lo diga. RESPONDIDA por escrito el 2026-09-11: es REGLA -"solo 1 zona control bro. si hay 2 se descarta"- y ratifica tambien el descarte, no solo el numero (fb-2026-09-09-sesion-01-1b2203b0)

Afecta a: `zonas_control_max_por_esquema`.
