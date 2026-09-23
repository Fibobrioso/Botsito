<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Ambiguedades: lo que todavia no se sabe

`spec_version 12.1.1` · **sin sello**: el hash cubre knowledge/spec/parametros.yaml, knowledge/spec/strategy_spec.yaml, knowledge/spec/glossary.yaml y este documento no sale de ninguno de ellos

Como se cierra cada una: **RESUELTA** solo con un registro de feedback del trader; **DECIDIDA** por el consultor, con su ADR (ADR-0022); **ABIERTA** es la unica que se sigue abierta: si es una `pregunta` entra en el cuestionario de la sesion siguiente, y si es una `medicion` la cierra un dato y no se le pregunta al trader.

## ABIERTA (14)

### A-13 · break even al toque o con cuerpo · pregunta

¿el rompimiento de la zona de control que dispara el break even vale al toque (por un pip) o hay que esperar a que la vela cierre con cuerpo? El parametro que responde a esto es `break_even_criterio_ruptura`, no `break_even_condicion`: aquel dice CON QUE se da por rota la zona y este si el stop se mueve al TOCAR el nivel o al cierre, que es otra pregunta y la cerro A-4. Hasta el 2026-09-11 esta ambiguedad nombraba el segundo, asi que `spec status` ensenaba como "en revision" un valor CONFIRMED y ESCONDIA el default que de verdad corre

Afecta a: `break_even_criterio_ruptura`.

### A-16 · cuanto se separan las velas de Oanda de las de Dukascopy · medicion

¿como se comparan decisiones tomadas sobre velas de Oanda (FX Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milesima? Partida el 2026-09-12 (ADR-0024): aqui queda solo la MEDICION, que no la puede cerrar ninguna decision. El anexo del 2026-09-09 midio OTRA pareja -MT5/FundedNext contra Dukascopy, 2 puntos de mediana- y el lo dice: "queda una tercera fuente en juego, que es la del trader [...] esta medicion no la cubre". La decision de metodo que estaba mezclada aqui es A-23

### A-18 · base sobre la que se mide el objetivo 1:3 · pregunta

¿el 1:3 se mide sobre la caja completa o sobre la distancia hasta el stop, que es la que dimensiona el lote? Hasta el 2026-09-11 las dos eran la MISMA distancia y la pregunta sonaba academica; desde ADR-0020 el lote se dimensiona hasta stop_fraccion_caja y el objetivo sigue midiendose sobre la caja entera, asi que la respuesta cambia el RR realizado de verdad. PRIMERA MEDIDA, y no sale de la sesion sino del material (2026-09-21, agosto, ADR-0037): las dos lecturas predicen RR distintos sobre la distancia entrada-stop -`caja_completa` da objetivo_rr/stop_fraccion_caja = 3,75; `riesgo_real` da 3,00- y las 18 filas de agosto con `maxTP` e `initialSL` tienen SUELO EN 3,00 (minimo 2,50, tres clavadas en 3,00, 16 de 18 por debajo de 3,75). La combinacion CONFIRMED de hoy -caja_completa con stop a 0,8- no cuadra con el material: o la base es `riesgo_real`, o el stop del trader en su backtest no esta a 0,8 de la caja. NO DECIDE NADA: es un mes, son 18 filas, y LA CAJA NO ESTA EN EL FICHERO -el RR medido es riesgo real por construccion, asi que si el stop viviera en el borde de la caja las dos lecturas coincidirian y la medida no discriminaria-. Se repite sobre mayo al ingerirlo

Afecta a: `base_calculo_objetivo`, `objetivo_rr`.

### A-21 · que es una zona de control limpia, sin ruido · **BLOQUEANTE** · pregunta

el trader condiciona la entrada a que la zona de control "no haga mucho ruido, o sea, sea una zona limpia". Los dos esquemas SI estan definidos en el corpus -rompe directo sin retroceso, o pequeno retroceso con zona de control y luego rompe- pero "limpia" no: es lo unico de la geometria de entrada que sigue siendo cualitativo y que el motor no puede evaluar. ¿cuantas velas? ¿cuanto retroceso de mas la invalida? ¿o se mide por otra cosa? ESTA AMBIGUEDAD NACIO MAL el 2026-09-10, preguntando que es un breaker; la definicion ya estaba en el corpus y lo que faltaba era recogerla en el glosario. Reformulada el mismo dia

### A-24 · que hace que marques un pivote de M15 y no otro · **BLOQUEANTE** · pregunta

cuando en M15 tienes varios pivotes candidatos, ¿que hace que marques uno y no otro? En v3 0:15:31 (fotograma fr-v3-982da728/944000) descartas expresamente el alto mas alto -"aunque yo invadiria este alto"- y marcas el de abajo, el que te deja el precio. No te preguntamos si es "el mas reciente" o "el mas extremo": las dos veces que lo hemos medido, el que eliges es el mismo. La pregunta es por el CRITERIO, y lo necesitamos dicho de forma que se pueda reproducir sin ti: que dos personas mirando el mismo grafico marquen el mismo nivel. Si la respuesta es "el que yo considere" (v3 0:39:16), dinos QUE MIRAS para considerarlo: cuantas velas atras, que tamano de movimiento, que lo descalifica

### A-25 · la vida de la marca de liquidez de M15 · pregunta

ya has marcado la liquidez de M15 y el precio todavia no la ha tomado, o la ha tomado y sigues con cartuchos: si M15 desarrolla entretanto otro pivote del mismo lado y mas reciente, ¿mueves la liquidez a ese pivote -y con ella el lado de ruido de RN-005 y el reinicio de los cartuchos, que es `siguiente_liquidez_m15`- o la marca se queda fija hasta que la retire uno de los eventos que si nombras: trade ganador (v6 0:32:27), invalidacion (v3 0:51:10) o cambio de dia (v4 1:09:21)?

Afecta a: `cartuchos_reinicio`.

### A-26 · el flujo de M15 cuando va contra el sesgo de H4 · pregunta

la vela que marca la liquidez es "contraria al flujo", y ese flujo es el de M15: eso ya lo dijiste cuatro veces y desde el 2026-09-20 esta escrito en la spec. Lo que no has dicho: en v3 0:12:42 el sesgo de H4 es bajista y el flujo de M15 que describes es un "complex pullback ALCISTA". Cuando el flujo de M15 va contra el sesgo de H4, ¿marcas igual la liquidez con la vela contraria a ese flujo alcista -y entonces el lado de ruido hay que leerlo del flujo de M15 y no del sesgo de H4, como esta hoy en RN-005- o solo cuentan las velas contrarias al flujo que va en el sentido del sesgo?

### A-27 · las especificaciones de EURUSD en FTMO · medicion

MEDICION, no pregunta al trader. ¿que digits, tamaño de contrato, lote minimo, paso de lote y stops level tiene EURUSD en la cuenta de FTMO? Los cinco se midieron el 2026-09-05 en una demo de FundedNext, la firma que ADR-0026 descarta, y se conservan como DEFAULT declarado porque EURUSD tiene las mismas especificaciones en casi cualquier broker: no se heredan como medicion. El que mas puede diferir es el stops level, que en FundedNext valia 0 y dejaba RN-026 sin activarse nunca. Se mide en la prueba gratuita de FTMO con SymbolInfo* (junto con el lote maximo, el freeze level y los modos de llenado, que el registro todavia no guarda) y el pre-vuelo de F33 aborta si la cuenta real dice otra cosa

Afecta a: `instrumento_digitos`, `instrumento_contrato`, `instrumento_lote_minimo`, `instrumento_lote_paso`, `instrumento_stops_level`.

### A-28 · el reloj del servidor de FTMO y su regla de horario de verano · medicion

MEDICION, no pregunta al trader. ¿cuanto va el reloj del servidor de FTMO por delante de UTC en horario estandar, y con que calendario cambia de hora: el de Nueva York, el europeo o ninguno? La ficha de FTMO dice "GMT+2 +DST" sin nombrar el calendario, y lo que midio la demo de FundedNext (120 minutos, calendario de Nueva York) no se hereda (ADR-0026). Desde ADR-0027 este reloj ya no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor y si anclaje_h4 (17:00 Nueva York) cae de verdad en su medianoche. COMPROBAR EL CALENDARIO EXIGE OBSERVAR UNA TRANSICION de hora en el terminal, asi que esta ambiguedad NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE: el desfase base se puede medir cualquier dia, la regla de horario de verano no. VERIFICACION EXPLICITA (añadida el 2026-09-14 al validar la rama): confirmar EN EL PANEL de la prueba gratuita de FTMO que el corte del dia de riesgo -cuando se recalcula el limite diario- cae a medianoche CE(S)T y NO a la medianoche del servidor. Las dos se separan una hora (el servidor va a GMT+2/+3 y CE(S)T a GMT+1/+2) y equivocarse cuesta la cuenta. reloj_dia_riesgo se queda CONFIRMED en `civil_operativa` por el reglamento (ADR-0027); si el panel dijera otra cosa, se reabre A-19 y el parametro vuelve a DEFAULT_AMBIGUOUS

Afecta a: `broker_offset_base`, `broker_dst`.

### A-29 · cuando nace la orden limite · pregunta

¿cuando colocas la orden limite por primera vez en una zona: cuando ya se ha dado el esquema de entrada ("apenas el breaker, o sea, marco mi orden limit"), o en cuanto tomas la liquidez de M15, en la primera zona de control que se completa, y desde ahi la vas moviendo? El corpus dice las dos: v3 0:42:01 marca la orden con el breaker; v1 0:13:58 la va "bajando" en cuanto rompe la liquidez; v3 0:25:11 la tiene "predefinida" esperando el breaker; y en la sesion 1 (v6 1:22:14) la orden ya esta en la zona de "posible breaker" y se activa sin validar, que es el caso de RN-010. La spec corre con la primera como default (orden_limite_nace). Con la segunda hay que reescribir RN-008, que hoy prohibe abrir sin esquema y frenaria la propia colocacion. PRIORIDAD DE LA SESION 2 (consultor, 2026-09-17): el default se queda hasta que el trader responda

Afecta a: `orden_limite_nace`.

### A-30 · la orden limite pendiente al llegar el fin de la ventana · pregunta

¿que haces con una orden limite que sigue pendiente, sin llenar, cuando llegan las 15:00: la cancelas, o la dejas puesta y, si se llena despues, la gestionas? A las 15:00 cierras lo que tengas abierto (RN-002), pero de una orden todavia sin llenar no hablaste, y ninguna ambiguedad lo preguntaba: la auditoria del 2026-09-13 midio que, sin respuesta, una limite viva sobrevive al cierre y se llena fuera de la ventana. La accion `retirar_orden_limite` esta declarada y ninguna regla la usa hasta que respondas

### A-31 · el stop entero de una entrada que se activo sin ruptura · pregunta

una entrada que se activo sin ruptura y se fue al stop entero, ¿gasta intento? Dijiste que no cuentan como intento "un break even [...] una entrada invalidada [...] reentrada despues de equal" (RN-016, v6 0:52:19), y el equal que describes en v6 1:22:25-1:23:19 es una salida que no llega al stop: se activa sin validar, un equal "te saque la entrada, te genera una perdida" y actualizas el limit para reentrar. Del stop entero de esa misma entrada no hablaste. La spec corre con que SI gasta, porque cuesta el riesgo entero y ninguno de tus tres casos lo exime; y con que la salida en negativo sin stop NO gasta. Las dos cosas son lectura nuestra (cartucho_criterio, RN-016, RN-019). Se lleva a la sesion 2

### A-32 · el nivel que al romperse con mecha invalida la entrada · pregunta

en v4 0:53:23 (fotograma fr-v4-9ad0ebb8/3203000) descartas la entrada porque el precio rompe con mecha el nivel horizontal que tienes dibujado, al que apunta tu flecha: ¿ese nivel es la liquidez de M15 -y entonces lo que exige cuerpo es RN-004, ya escrito- o es un nivel de M1, y entonces hay rupturas de M1 que tampoco valen con mecha, contra breaker_m1_criterio_ruptura?

Afecta a: `breaker_m1_criterio_ruptura`.

### A-33 · tres ganadoras que cierran por debajo de 3R · pregunta

en la sesion 1 dijiste "sin toma de parciales y que tiene que llegar al ratio 1.3 si o si" (v6 0:17:07). Pero en tu material hay TRES operaciones GANADORAS que CIERRAN por debajo de 3R: una en agosto (2,50) y dos en abril (2,57 y 2,94), en dos meses independientes. ¿cerraste esas a mano? ¿tomaste parciales en ellas? ¿o hubo otro motivo -un break even que salto, una noticia, cerrar antes de una sesion-? No te preguntamos si tomas parciales EN GENERAL, que ya lo contestaste: te preguntamos que paso en esas. MEDIDO ANTES DE PREGUNTAR, y es lo que hace que la pregunta exista: `maxTP` es el PRECIO DE CIERRE de las ganadoras y no la excursion maxima -`== avgClosePrice` en 17 de 17 filas de abril donde existen las dos, y presente si y solo si `rPnL > 0`-, asi que esas tres no son operaciones que NO LLEGARON a 3R: son operaciones que CERRARON en ganancia por debajo de 3R. En F14a esa columna se habia SUPUESTO al reves (ADR-0037 y su correccion del 2026-09-22). OBSERVACION DESCRIPTIVA del 2026-09-22 (MAYO-DEV, ADR-0040), sin atribuir causa: ganadoras por debajo de 3R = agosto 1 (2,50), abril 2 (2,57; 2,94), mayo 1 (2,90), esta ultima sobre los 6 dias `dev` de mayo

Afecta a: `parciales`, `objetivo_rr`.

## DECIDIDA (5)

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
