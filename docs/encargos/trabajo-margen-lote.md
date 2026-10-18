# Encargo · trabajo/margen-lote

Dado por Aleks (consultor) el 2026-10-17; el encargo va fechado el 2026-10-18. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: trabajo/margen-lote (NA:E, hoja de ruta R3.3, heredado 37). Encargo del consultor, 2026-10-18.
>
> 0. Apertura
> - Base: main 9cf711e, el commit de estado sobre el merge 5296a31 (stable/F37r-sesgo-h4-color). Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de 9cf711e la dio verde el cierre (run 39083113877, que no está escrito en el repo): compruébala con gh; si el clasificador niega gh, PARADA y la consulto yo con «!». Nunca con curl ni con un guion.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R3.
> - Informe: docs/validation/MARGEN-LOTE.md. Anexos: docs/validation/anexos/MARGEN-LOTE/.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0 y su PARADA; entregar-rama al final. Antes de abrir A-57, lee docs/runbooks/AMBIGUEDADES.md, como manda CLAUDE.md.
> - Revisa /model antes de empezar: Fable 5.1 en esfuerzo alto.
>
> 1. Objetivo
> Decidir por ADR qué hace el bot cuando el lote del 0,5 % no cabe en el margen libre a 1:30 o en los 50 lotes de la firma; hacer que el bróker simulado rechace lo que FTMO rechazaría por margen; y medir lo que pide la entrada E: (1) qué parte de las operaciones del trader en construcción tiene un stop de menos de unos 2 pips, y cuántas caen a ±2 minutos de una noticia; (2) cuántas órdenes de la corrida diaria rechaza el volumen y cuántas rechazaría el margen.
>
> La medida 2 se hace sobre el código de main de hoy, no sobre la salida de R3.1 que cita E (CORRIDA-CONSTRUCCION.md §3.12, 100 rechazos por volumen): desde ADR-0080 el sesgo es otro y la salida commiteada de main da otra cifra. El informe da las dos y dice que sustituye la base por eso.
>
> Lo que ya está medido y no se repite (verifícalo): FTMO-P-D1.md §2. Con todo el saldo como margen caben 27,27 lotes a 1,10 y 25,00 a 1,20. El 0,5 % deja de cumplirse con un stop de menos de 1,83 y 2,00 pips, y el tope de 50 lotes corta en 1 pip. Partir en varias órdenes no lo arregla. El apalancamiento 30 se midió en la prueba gratuita (DEMO-EJECUCION-1.md, fila 24). VIABILIDAD-COMISION.md da, para abril y agosto, un stop del trader de 1,5 pips de mediana, y de 1,2 con el 0,8: el margen corta en buena parte de las operaciones, y esta rama lo cuenta en los cuatro meses de construcción.
>
> 2. Decisiones del consultor (van al ADR con esta fecha. Las tomo ANTES de ver las medidas, y las medidas no las cambian. Si la fase 0 encuentra un hecho que las contradiga —una regla de MT5 o de FTMO, un ADR o algo que el trader ya dijera—, PARADA)
> D1. Cuando el lote no cabe, el bot LIMITA el lote y opera; no deja de operar. De las tres salidas que ADR-0071 §2 dejó abiertas (recortar, partir en varias órdenes, no operar), partir queda descartada por FTMO-P-D1.md §2. Por qué limitar: el objetivo de fidelidad son las mismas decisiones (misma operación, lado, vela y resultado en R), y limitar el lote conserva la decisión y el resultado en R; solo cambia el riesgo en dinero. No operar quitaría justo las operaciones de stop corto, y VIABILIDAD-COMISION.md enseña que sacarlas del juego mueve la esperanza: elegir por eso sería ajustar contra resultados. La decisión es PROVISIONAL hasta que el trader diga qué hace él. La pregunta ya está en la lista «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5 (la del lote que no cabe; cítala por su texto, no por su número) y se amplía al margen.
> D2. El lote final es el menor de tres: el del riesgo (RN-011), firma_volumen_max_lotes, y el que cabe en el margen libre multiplicado por un parámetro nuevo de fracción del margen libre, de valor 0,95. Después se redondea hacia abajo al paso (RN-027). El 5 % de colchón cubre el deslizamiento del llenado y el precio con que se convierte el margen (ask en compras, bid en ventas, FTMO-P-D1.md §2). Es una decisión nuestra, no del trader. El lote mínimo: RN-027 dice en su prosa que por debajo del mínimo «no se opera», pero redondear_lote sube al mínimo (primitivas_broker.py:492, y ADR-0053, tabla de la línea 39). Lee la cita de RN-027 (fb-2026-09-09-sesion-01-17ed6193). Si la cita sostiene «no se opera», el código se alinea con la regla y el ADR enmienda ADR-0053 con su recuadro. Si no la sostiene, PARADA. En la práctica casi nunca muerde: solo con el margen libre casi a cero.
> D3. El margen se calcula con la fórmula de FTMO-P-D1.md §2 (lotes × instrumento_contrato × precio / firma_apalancamiento, en USD), sobre el margen libre: la equidad menos el margen de las posiciones abiertas. El bróker simulado comprueba el margen al LLENAR la orden stop. Al colocar una pendiente también, si la documentación de MT5 (la misma página que leyó FTMO-P-D1.md §2) dice que MT5 lo hace. El informe cita su frase. Si no lo dice, se comprueba en los dos instantes como supuesto conservador. El rechazo al llenar es un camino nuevo: ADR-0052 §4 solo prevé rechazos al colocar, así que el ADR lo enmienda con su recuadro. Hoy el bróker no conoce el saldo: la fase 0 propone cómo le llega la equidad desde la capa de cuenta. El script 1.1 no se toca. Medir en la demo cuándo comprueba MT5 el margen de una pendiente queda como una línea para la entrada A, con la ejecución 3, y el informe lo dice.
> D4. Parámetros nuevos. Los nombres son propuestos: ajústalos al estilo de la spec y no los confundas con firma_margen_seguridad (ADR-0031), que es otra cosa.
> - lote_si_no_cabe: enum limitar | no_operar; valor limitar; DEFAULT_AMBIGUOUS bajo A-57.
> - lote_margen_libre_fraccion: decimal; valor 0,95; CONFIRMED, con fuente {tipo: decision, id: <el ADR nuevo>}.
> La fase 0 propone dónde va cada uno y cómo lee la spec el tope de volumen. Hoy firma_volumen_max_lotes vive solo en el perfil; el test que cruza los firma_* de los dos sitios es test_perfil_cuenta.py:110. Ten en cuenta también la guardia comprobar_decisiones (spec/modelo.py:425-455): RN-011 y RN-027 ya tienen ocupado su campo decision. Propón una regla nueva o el límite fuera de la spec, con su porqué.
> D5. Ambigüedad nueva: verifica que la siguiente libre es A-57. Clase pregunta, no bloqueante: qué hace el trader cuando el lote de su riesgo no cabe en el margen o en el volumen máximo de la cuenta. Antes de redactarla, busca en el corpus que se puede citar (evidence, feedback y transcripciones activas fuera de cuarentena, por la CLI que filtra) lo que el trader dijo de lotes, margen o apalancamiento. El informe dice qué se buscó (Technical Debt: «BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD»). Va también a la tabla Known Ambiguities de PROJECT_STATE en la misma rama, porque test_kit lo exige.
> D6. ADR nuevo: verifica que el siguiente libre es 0081. Cita ADR-0026 (Impacto, el margen), ADR-0050 (el perfil), ADR-0052 §4, ADR-0053, ADR-0056 §8 (rama 5, «lote por el bróker») y ADR-0071 §2. Si alguno lo contradice más allá de lo que D2 y D3 enmiendan, PARADA. En el perfil corrige lo que hoy no es verdad:
> - firma_apalancamiento, en el perfil (:276, «Lo consume el broker simulado (margen)») y en parametros.yaml (:1831-1832, «F21 lo comprueba con la distribucion real de cajas»). Que digan quién lo consume de verdad, y que sus consumido_por, que hoy discrepan ([F24] frente a [F21, F33]), digan la verdad.
> - Como esta rama toca el perfil, le cae G.3 de la hoja de ruta: la descripción de firma_tamano_posicion_ratio_aviso pasa a decir lo que respondió FTMO (FTMO-REGLAS.md, respuesta 10).
> D7. La cuenta sigue siendo FTMO 2-Step Swing (ADR-0026). Aleks decidió el 2026-10-13 quedarse en Swing; eso no está escrito en el repo y entra en el ADR con esa fecha. La medida de noticias es información para más adelante, no una propuesta de cambiar de tipo de cuenta: el informe da la cifra y no recomienda nada.
>
> 3. Lo que NO cambia
> - La geometría (caja, stop en el 0,8, objetivo, break even), el sesgo, la ventana y ninguna otra regla ni cifra. riesgo_por_operacion sigue en 0,5 %.
> - El script 1.1 de la demo y los runbooks de la demo.
> - Los informes y anexos cerrados (CORRIDA-CONSTRUCCION, SESGO-H4-COLOR, VIABILIDAD-COMISION, FTMO-P-D1): no se editan. Los guiones cerrados se usan tal cual o se copian a los anexos de esta rama.
> - Las guardias, .claude/ y el Makefile. Si algo obliga a tocar el Makefile, PARADA: con el Makefile cambiado la guardia niega todo make a la sesión, y esos make check los lanzo yo con «!».
> - PROJECT_STATE, salvo la fila de A-57 y lo que haga el ritual. Está en 23.396 bytes y el tope es 25.000: la rama no lo engorda más que esa fila.
> - Si el clasificador niega un comando, no cambies de vía ni reescribas el comando: PARADA, y lo lanzo yo con «!».
>
> 4. Fase 0 (inventario sin tocar nada; entrega y PARADA antes de escribir código)
> a. Dónde se calcula y se comprueba el lote hoy, con fichero:línea:
> - _lote_resuelto y redondear_lote (engine/primitivas_broker.py);
> - _limite_infringido (engine/broker.py, el rechazo por volumen_max_lotes) y _aplicar (el llenado, sin camino de rechazo hoy);
> - abrir_conocida (engine/broker.py), la vía de las operaciones conocidas, que también tiene que comprobar el margen;
> - cómo llegan los firma_* (engine/simulacion.py, engine/cableado.py), dónde viven el saldo (ctx.cuenta) y el flotante;
> - qué predicados y reglas de strategy_spec.yaml cambian con D1 y D2 (dimensionar_lote, redondear_lote, RN-011, RN-027).
> Propón dónde va el límite (en la preparación de la orden, en el bróker o en los dos) y por qué. El bróker simulado tiene que rechazar por margen aunque el bot calcule bien, porque es el que hace de FTMO.
> b. Lo que dice la documentación de MT5 sobre cuándo se comprueba el margen de una orden pendiente (D3), con su frase y su URL. Si el clasificador niega leerla, PARADA.
> c. La medida 1, sobre las operaciones del trader de los días dev de construcción (enero, abril, julio del 1 al 17 y agosto), leídas por la misma vía que usa el arnés. Antes de leer, comprueba con casos_reservados(repo) que ningún día está en una partición, y declara la lectura en HOLDOUT-EXPOSICIONES el mismo día. Cuenta cuántas operaciones, y qué parte, tienen una distancia del 0 al 0,8 (la del lote) de menos de 1,00, 1,83 y 2,00 pips, y lo mismo del 0 al 1, por mes y en total. Propón el guion: en anexos, que lea el registro y no lleve cifras dentro, como margen_p_d1.py, y los ±2 minutos como argumento, porque no son un parámetro del registro. No lo corras hasta mi respuesta. Agosto sale del xlsx que el trader ya no da por bueno (NA:Q): el informe lo dice junto a su cifra.
> d. Las noticias: de dónde sale un calendario de noticias de alto impacto de USD y EUR que cubra las fechas de construcción (lo pertinente es la lista de noticias restringidas de FTMO para la cuenta Standard), si hace falta descargar algo y quién lo hace. No descargues nada: propón la fuente y el procedimiento. Si no hay fuente razonable, dilo; la medida de noticias no bloquea el ADR.
> e. La medida 2. La salida de «### Ordenes» no lleva el lote ni la distancia. Propón el campo que hay que añadir (lote pedido, distancia en puntos y margen requerido), con el mismo régimen que el campo bloqueadas de R3.1: solo salida, ninguna decisión cambia, test sintético en los dos sentidos. Con él se cuenta, sobre la corrida 2 y ANTES del cambio, cuántos rechazos son por volumen y cuántas órdenes rechazaría el margen. Verifica la cifra de partida en la salida commiteada de main (anexos/SESGO-H4-COLOR/diaria…txt, «### Rechazos por motivo»). Yo cuento 96 por volumen_max_lotes (enero 18, abril 24, julio 20, agosto 34) y 11 por precio_invalido, frente a los 100 de R3.1.
> f. Los parámetros de D4, la ambigüedad de D5 (con lo que encontró la búsqueda en el corpus) y los tests que cambian de resultado con el límite. Mira al menos tests/regression/test_cuenta_7_de_agosto.py (espera un BrokerError por volumen en abrir_conocida), test_broker.py, test_broker_ordenes_stop.py, test_be_al_tick.py y test_peticiones.py. Para cada uno, di cómo se rehace sin rebajar lo que comprobaba.
> g. Lectura de material de las corridas: como declaró R3.1 (HOLDOUT-EXPOSICIONES.md, fila del 2026-10-14), el calentamiento lee el M1 entero de marzo y de junio. Se declara con su fila el mismo día de cada corrida y ANTES de correrla. Ninguna salida ni el informe imprime fechas fuera de los días dev de construcción, salvo la línea de cobertura del calendario de cierres, como en R3.1.
> PARADA con a-g y todo lo que la fase 0 contradiga de este encargo.
>
> 5. Fases tras mi respuesta
> Fase 1 · Medidas antes del cambio. El campo de 4.e con su test y make check sellado. Después, la corrida 2 (la diaria), con su fila de exposiciones antes. El arnés añade al nombre el sufijo DIAGNOSTICO…:
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/antes-diaria.txt
>    Con ella, la medida 2: rechazos por volumen y órdenes que rechazaría el margen, por mes, contados por orden y también por sesión, porque una misma caja se recoloca varias veces. También la medida 1 con el guion aprobado, y la de noticias si hay fuente.
> Fase 2 · Tests primero, en rojo sobre el código de main, con el recuento de FAILED en el informe:
> - el bróker rechaza por margen al llenar (y al colocar, si D3 lo pide), con el margen libre justo por encima y justo por debajo;
> - el margen tiene en cuenta una posición ya abierta;
> - la compra usa el ask y la venta el bid;
> - el lote se limita por margen, por volumen y por los dos;
> - el lote por debajo del mínimo, según lo que decida D2;
> - con lote_si_no_cabe = no_operar, no se coloca;
> - el lote que cabe no cambia;
> - el resultado en R de una operación limitada es el mismo que sin límite;
> - y los tests de 4.f, rehechos.
> Fase 3 · Código, spec y ADR: el límite y el rechazo por margen; los dos parámetros; A-57; el ADR de D6, con sus recuadros sobre ADR-0052 §4 y, si toca, ADR-0053; las descripciones corregidas del perfil y de parametros.yaml, y G.3. En el mismo commit, spec_version subida, spec manifest --escribir y spec docs --escribir; trailer Fuente: con los ids nuevos. Tests en verde y make check sellado.
> Fase 4 · Re-corrida: hace falta porque el límite cambia lo que simula (los rechazos por volumen pasan a ser órdenes colocadas). Antes, su fila de exposiciones. Van los tres comandos de R3.1 tal cual, salvo la carpeta de --salida:
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/MARGEN-LOTE/arrastrada.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/diaria.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/a35-inicio.txt
>    Es una corrida con --diagnostico-*: no cuenta ni habilita mayo (ADR-0070 §3), no decide ningún parámetro y no se mide cobertura contra ningún umbral. En el informe van:
> - los rechazos por motivo, antes y después;
> - cuántas órdenes se colocan con el lote limitado, y por qué límite;
> - el riesgo efectivo de las operaciones del bot: cuántas con el 0,5 % entero, la mediana y el mínimo, en % del saldo;
> - la tabla T0 y P1-P7 con patrones.py, frente a la de SESGO-H4-COLOR.md §4.3.
>    Si cambian las parejas o la precisión, se dice y se explica por sesión; no se ajusta nada.
>
> 6. El informe
> Lleva:
> - el encargo frente a lo hecho, punto por punto, y las desviaciones;
> - las medidas 1 y 2 con sus guiones, y la frase de la documentación de MT5;
> - lo que va a la sesión 5: A-57, con lo que encontró la búsqueda;
> - «Líneas preparadas para el commit del contrato de la orden de cierre»:
>   · E sale de la Next Action a HISTORIA;
>   · el heredado 37 sale con el criterio (a) de docs/state/README.md: su texto literal y su evidencia, bajo «# Pendiente heredado SALE»;
>   · en la hoja de ruta, R3.3 pasa a HECHA; A.2 queda con «el heredado 37 decidido» cumplido; G.3 pasa a HECHA; A-57 entra en los Refs de R4.1;
>   · F queda en «O → V», y V gana A-57 entre lo que lleva a la sesión 5;
>   · una línea para A: medir en la ejecución 3 cuándo comprueba MT5 el margen de una pendiente;
>   · si la medida de noticias quedó sin fuente, una línea para A con quién la consigue.
>
> 7. Revisor
> El agente revisor (opus) sobre la rama, con los dos ejes de siempre: reglas y encargo. Que compruebe además que ninguna consulta de CI se hizo con curl ni con un guion. Su informe va pegado al final del informe, con lo arreglado y lo declarado.
>
> 8. CI
> Si la rama toca hooks, rutas o el sistema de archivos, push como fix/margen-lote y CI de Linux, con su run en el informe. Si no los toca, dilo con la lista de ficheros cambiados.
>
> Rama lista para revisión, NO cerrada.
