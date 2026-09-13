<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Ambiguedades: lo que todavia no se sabe

`spec_version 10.2.0` · **sin sello**: el hash cubre knowledge/spec/parametros.yaml, knowledge/spec/strategy_spec.yaml, knowledge/spec/glossary.yaml y este documento no sale de ninguno de ellos

Como se cierra cada una: **RESUELTA** solo con un registro de feedback del trader; **DECIDIDA** por el consultor, con su ADR (ADR-0022); **ABIERTA** es la unica que se sigue preguntando, y entra en el cuestionario de la sesion siguiente.

## ABIERTA (6)

### A-13 · break even al toque o con cuerpo

¿el rompimiento de la zona de control que dispara el break even vale al toque (por un pip) o hay que esperar a que la vela cierre con cuerpo? El parametro que responde a esto es `break_even_criterio_ruptura`, no `break_even_condicion`: aquel dice CON QUE se da por rota la zona y este si el stop se mueve al TOCAR el nivel o al cierre, que es otra pregunta y la cerro A-4. Hasta el 2026-09-11 esta ambiguedad nombraba el segundo, asi que `spec status` ensenaba como "en revision" un valor CONFIRMED y ESCONDIA el default que de verdad corre

Afecta a: `break_even_criterio_ruptura`.

### A-16 · cuanto se separan las velas de Oanda de las de Dukascopy

¿como se comparan decisiones tomadas sobre velas de Oanda (FX Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milesima? Partida el 2026-09-12 (ADR-0024): aqui queda solo la MEDICION, que no la puede cerrar ninguna decision. El anexo del 2026-09-09 midio OTRA pareja -MT5/FundedNext contra Dukascopy, 2 puntos de mediana- y el lo dice: "queda una tercera fuente en juego, que es la del trader [...] esta medicion no la cubre". La decision de metodo que estaba mezclada aqui es A-23

### A-17 · noticias frente a la regla de la cuenta de fondeo

DESCARTADA una via el 2026-09-12: se penso que la pestaña `Prop firm` de FX Replay -que el trader tiene con el plan Pro- podria llevar dentro la ventana de noticias y el corte del dia de riesgo, y cerrar esta y A-19 de golpe. El trader responde que NO la tiene configurada con FundedNext. Sigue haciendo falta el reglamento. ¿QUE prohibe exactamente el reglamento de FundedNext sobre operar en noticias: que eventos, cuantos minutos antes y despues, y que sancion? Es un HECHO que se verifica en su reglamento, no una decision. Partida en dos el 2026-09-12 (ADR-0022): la decision de alcance -el bot no opera noticias en la v1 aunque la estrategia del trader si funcione dentro de ellas- se fue a A-22 y esta DECIDIDA; aqui se queda lo que hay que leer y medir. Sin esta respuesta, RN-028 sabe QUE bloquea y no CON QUE VENTANA

Afecta a: `filtro_noticias`.

### A-18 · base sobre la que se mide el objetivo 1:3

¿el 1:3 se mide sobre la caja completa o sobre la distancia hasta el stop, que es la que dimensiona el lote? Hasta el 2026-09-11 las dos eran la MISMA distancia y la pregunta sonaba academica; desde ADR-0020 el lote se dimensiona hasta stop_fraccion_caja y el objetivo sigue midiendose sobre la caja entera, asi que la respuesta cambia el RR realizado de verdad

Afecta a: `base_calculo_objetivo`, `objetivo_rr`.

### A-19 · cuando empieza el dia y la semana de riesgo

DESCARTADA una via el 2026-09-12: la pestaña `Prop firm` de FX Replay no la tiene el trader configurada con FundedNext, asi que no hay atajo. Sigue siendo el panel de la cuenta (F17). ¿en que reloj cae la medianoche que reinicia el tope diario del 4,5 % y el domingo que reinicia el semanal: el del servidor del broker, que cambia con el calendario de Nueva York, o el del grafico? Hay que verificarlo en el panel de la cuenta, no suponerlo

Afecta a: `reloj_dia_riesgo`.

### A-21 · que es una zona de control limpia, sin ruido · **BLOQUEANTE**

el trader condiciona la entrada a que la zona de control "no haga mucho ruido, o sea, sea una zona limpia". Los dos esquemas SI estan definidos en el corpus -rompe directo sin retroceso, o pequeno retroceso con zona de control y luego rompe- pero "limpia" no: es lo unico de la geometria de entrada que sigue siendo cualitativo y que el motor no puede evaluar. ¿cuantas velas? ¿cuanto retroceso de mas la invalida? ¿o se mide por otra cosa? ESTA AMBIGUEDAD NACIO MAL el 2026-09-10, preguntando que es un breaker; la definicion ya estaba en el corpus y lo que faltaba era recogerla en el glosario. Reformulada el mismo dia

## DECIDIDA (3)

### A-15 · alcance de la ventana operativa · cerrada por `ADR-0024` el 2026-09-12

¿el bot busca solo en las dos sesiones de 07-11 y 11-15, o tambien en la de Nueva York? DECIDIDO por el consultor el 2026-09-12: NO se amplia en esta fase. No es una pregunta que el trader se reservara, es una que DEVOLVIO -"puedes buscar las operaciones donde sea, o sea, no hay problema"-, y toda su operativa GRABADA va de 07:00 a 15:00. Ampliar sin una sola sesion grabada en Nueva York meteria en el universo de etiquetado dias que nadie ha visto operar y cambiaria el sesgo H4 de la mitad. La capacidad se conserva: ampliar es cambiar ventana_inicio y ventana_fin, nada mas

Afecta a: `ventana_inicio`, `ventana_fin`.

### A-22 · si el bot opera noticias, y que pasa con la capacidad para otras cuentas · cerrada por `ADR-0022` el 2026-09-12

el trader opera noticias en sus cuentas propias -que no lo prohiben- y su estrategia funciona dentro de esos eventos. ¿el bot hace lo mismo? DECIDIDO por el consultor el 2026-09-12: NO en la primera version, porque va a una cuenta fondeada que puede prohibirlo como norma y la sancion es perder la cuenta aunque la operacion acabe en profit. La CAPACIDAD se conserva: `filtro_noticias` mantiene la opcion `no`, asi que el dia que el bot corra en una cuenta que lo permita se cambia el valor y nada mas. Lo que falta por saber -que ventana exacta- es A-17

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
