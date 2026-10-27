# Decisiones de arquitectura (ADR)

Una decision por fichero, `NNNN-titulo.md`, con el formato de `0000-template.md`. Estado `ACTIVE` o
`SUPERSEDED` (con enlace a la que la sustituye). Un ADR nunca se borra.

| ADR | Titulo | Estado |
|---|---|---|
| 0001 | Estructura del repositorio y regimenes de cambio | ACTIVE |
| 0002 | Registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta | ACTIVE |
| 0003 | Hooks copiados desde scripts/git-hooks; sin framework pre-commit | ACTIVE |
| 0004 | Categorias de parametro y horas con huso | ACTIVE |
| 0005 | Datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje | ACTIVE (con enmienda REVOCADA por ADR-0017) |
| 0006 | Capas revisadas, paquete `comun` y accesores del registro por tipo declarado | ACTIVE |
| 0007 | Transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario | ACTIVE |
| 0008 | Fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable | ACTIVE |
| 0009 | Verificacion mecanica de citas y propuestas de evidencia trazables | ACTIVE |
| 0010 | Busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente | ACTIVE |
| 0011 | Kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback | ACTIVE (el esquema de ambiguedades gana el estado DECIDIDA en ADR-0022) |
| 0012 | El registro despues de la sesion 1: tipos nuevos, ausencia de valor, categorias y el reloj del trader | ACTIVE (punto 5 revertido por ADR-0017) |
| 0013 | StrategySpec: reglas que nombran parametros y nunca los contienen, y un hash que cubre lo que el bot hace | ACTIVE |
| 0014 | La base sobre la que se mide el objetivo: `base_calculo_objetivo` | ACTIVE (enmendado por ADR-0020; con nota del 2026-09-16: sus dos premisas estan revocadas y la base queda para el consultor) |
| 0015 | Los relojes tras la auditoria: el del grafico es un default, y el dia de riesgo necesita el suyo | ACTIVE (enmendado por ADR-0017, ADR-0020 y ADR-0027) |
| 0016 | De donde sale cada regla: el campo `decision`, y un hash que cubre lo que un humano lee | ACTIVE (con nota del 2026-09-11) |
| 0017 | El reloj del trader es su reloj civil: se revierte ADR-0012 y se confirma ADR-0005 | ACTIVE |
| 0018 | La precedencia va por clase, no por orden del fichero; y los siete defectos que eso destapo | ACTIVE (con nota del 2026-09-11: A-20 cerrada) |
| 0019 | La forma ejecutable de una regla: predicados con argumentos, ligadura, y cuatro cosas con nombre (cinco desde F12: nace `efectos`) | ACTIVE |
| 0020 | La base del lotaje es la distancia hasta el stop, no la caja completa | ACTIVE |
| 0021 | Que cuenta como abrir un holdout, y que se hace con la exposicion de mayo | ACTIVE (con nota del 2026-09-17: su §3 tiene mecanismo en ADR-0033); y del 2026-09-21: su §1 ya era granular por dia, y ADR-0037 le anade la regla del fichero mixto) |
| 0022 | El bot no opera noticias en la cuenta fondeada, y una ambiguedad puede cerrarse por decision | ACTIVE (con enmienda del 2026-09-14: con FTMO Swing el bot si opera noticias) |
| 0023 | El registro de feedback sabe cuando llego cada respuesta y por donde (`recibido_el`, `procedencia`) | ACTIVE |
| 0024 | La ventana no se amplia a Nueva York (A-15), y la referencia para medir es Dukascopy (A-23; A-16 se parte y conserva la medicion) | ACTIVE |
| 0025 | El reparto de mayo no se toca: 6 dias dev y 13 de holdout (6/4/3), y junio sale del universo de F14 | ACTIVE |
| 0026 | La prop firm es FTMO, reto 2-Step, tipo de cuenta Swing | ACTIVE |
| 0027 | Los relojes con FTMO: el dia de riesgo es el dia civil del trader | ACTIVE |
| 0028 | El reloj del motor: tres fases, y el riesgo va por tick | ACTIVE (con nota del 2026-09-16: el punto 5 aplicado y el 4 precisado por ADR-0032) |
| 0029 | Lado del precio y redondeo de niveles | ACTIVE |
| 0030 | El motor interpreta la `forma`; las primitivas se escriben a mano | ACTIVE |
| 0031 | El freno de la firma dispara antes del limite: margen declarado y lectura prospectiva | ACTIVE |
| 0032 | De donde sale cada hecho y cada evento, y como nace la orden limite | ACTIVE |
| 0033 | La guarda y la puerta del holdout: que vigilan, por donde se abre y como se autoriza | ACTIVE (con enmienda del 2026-09-21: la autorizacion cita la PREGUNTA que abre, gastarla cierra, y el lector decide sobre la ruta resuelta) |
| 0034 | Septiembre es material ETIQUETADO de un mes que el trader ya ha visto | ACTIVE |
| 0035 | El universo de un paquete se congela en el paquete: comprobar va por la lista, construir por el disco | ACTIVE (con enmienda del 2026-09-21: tambien los cupos, y `anclas.yaml` ata lo congelado por el sha de su blob) |
| 0036 | El material ya visto se reparte por su propio camino, con nombres propios y con puerta | ACTIVE |
| 0038 | Un fotograma se abre por instante localizado, nunca por muestreo | ACTIVE |
| 0039 | Ningun libro se lee sin su formato y su huso declarados | ACTIVE |
| 0040 | La combinacion CONFIRMED del objetivo es falsa, y los dos supervivientes siguen abiertos | ACTIVE (con enmienda de ADR-0073) |
| 0041 | Un dia reservado expuesto sale del holdout y no se sustituye | ACTIVE |
| 0042 | Material ya visto entra por un reparto dev-visto, sin sorteo y sin holdout | ACTIVE |
| 0043 | Criterio de fidelidad en desarrollo | ACTIVE |
| 0044 | El sesgo H4: ambiguo, insuficiente, y fijado al abrir la sesion | ACTIVE (con enmiendas: ADR-0060 §1 y ADR-0075 en su §1, la doble ruptura; ADR-0080 en su §2 y su alternativa descartada, el color de la ruptura) |
| 0045 | La liquidez de M15 es el pivote mas reciente ya formado | ACTIVE (enmendado por ADR-0084 en «no se sustituye por un parámetro provisional»: `liquidez_m15_mecha_que_vuelve`, DEFAULT_AMBIGUOUS bajo A-35) |
| 0046 | Marzo entra por el camino de fidelidad, con su reserva y sin repetir el sorteo | ACTIVE |
| 0047 | La unidad de comparacion es la operacion tambien en el holdout | ACTIVE |
| 0048 | El arnes del motor | ACTIVE |
| 0049 | Los huecos del arnes: H1-H6 de ADR-0048 cerrados con las decisiones del consultor | ACTIVE |
| 0050 | El simulador: la capa de cuenta | ACTIVE (con la ratificación del consultor del 2026-09-25, registrada el 2026-10-18 en §4; nota de ADR-0082) |
| 0051 | El modelo de llenado (con las decisiones nocturnas resueltas y los ticks obligatorios para simular) | ACTIVE |
| 0052 | El broker simulado | ACTIVE |
| 0053 | El cableado del simulador (con las decisiones resueltas por el consultor, 2.1 y 5.1 para revisar, y A-44 como siguiente bloqueo tras A-35) | ACTIVE (nota de ADR-0082; notas del 2026-10-26 en §3.3 y §9: A-44 con valor por la sesión 5, la magnitud como DEFAULT_AMBIGUOUS, sigue ABIERTA) |
| 0054 | RN-004 y RN-020, listas para activarse con la respuesta del trader | ACTIVE (nota del 2026-10-26 en §1 e Impacto: A-35 fijada en `cierre_vela_contraria` y A-44 en `dia`/`porcentaje` por la sesión 5, la magnitud `saldo` como DEFAULT_AMBIGUOUS; las dos siguen ABIERTAS; nota de ADR-0084 en «Por qué descartamos las demás», (2): la mecha que vuelve como DEFAULT_AMBIGUOUS bajo A-35) |
| 0055 | RN-011 y la zona de entrada: preparada para A-21, con el selector de «limpia» PROVISIONAL | ACTIVE (con enmienda de ADR-0076: A-21 RESUELTA, `--diagnostico-a21` retirado) |
| 0056 | La entrada con la ruptura: RN-011 con orden stop, preparada con selectores UNKNOWN | ACTIVE |
| 0057 | Órdenes stop y rechazo de pendientes en el bróker simulado (PROVISIONAL hasta la demo de FTMO) | ACTIVE (desde el 2026-10-09, ADR-0071: §3 y §5 MEDIDOS en la ejecución 1 de la demo; §1 coincide con una observación; §2 sigue PROVISIONAL) |
| 0058 | El selector de A-47 en la rama 2: la orden stop en el instante de la límite, para medirla (PROVISIONAL) | ACTIVE |
| 0059 | A-42, PROVISIONAL: la ventana va en el reloj del gráfico, UTC+2 fijo, todo el año | SUPERSEDED por ADR-0069 |
| 0060 | El sesgo con doble ruptura lo decide el color, y toda operación se cierra antes del fin de su vela H4 | ACTIVE (con enmiendas de ADR-0075: la H4 neutra no fija el sesgo; y de ADR-0080 en §1: con un solo extremo roto el color sí decide) |
| 0061 | El stop se redondea alejándose de la entrada, y el break even se pone al completarse la zona de control posterior | ACTIVE (enmienda ADR-0029 §3 para el redondeo del stop; nota de ADR-0085 en §4: la zona posterior salta la vela sin cuerpo) |
| 0062 | La toma de la liquidez de M15 la hace una vela de M1, y lo que eso destapa en el productor | ACTIVE |
| 0063 | El reloj de las sesiones se separa del reloj del día de riesgo: el selector `reloj_sesiones` | ACTIVE |
| 0064 | La orden stop nace en el último pivote de M1 y se reubica con cada pivote nuevo, con la caja de R6 | ACTIVE (aceptado en su dirección; valores DEFAULT_AMBIGUOUS bajo A-48 y A-29; decisión 5 enmendada por ADR-0074; decisión 1 enmendada por ADR-0083) |
| 0065 | El break even de RN-014 se pone al tick que pasa el nivel, no al cierre de la M1 | ACTIVE (PROVISIONAL hasta la demo de MetaTrader) |
| 0066 | Escenarios dentro de la sesión: la toma tiene que ser de la sesión, y cada liquidez nueva abre un escenario con sus intentos | ACTIVE (sus parámetros PROVISIONAL de las preguntas 5, 15, 18 y 20 de la sesión 4 son CONFIRMED desde `trabajo/activar-sesion-04`; queda el de la 21, `orden_pendiente_al_abrir_escenario`, bajo A-53) |
| 0067 | El freno de peticiones vive en el puerto del broker: aviso, corte y bucle, y lo que protege la cuenta pasa siempre | ACTIVE (PROVISIONAL en sus cuatro umbrales, hasta A-54 en la demo de FTMO; enmendado por ADR-0082 en §1) |
| 0068 | La ventana prohibida antes de un cierre de mercado largo vive en el puerto del broker, con un calendario versionado por perfil | ACTIVE (PROVISIONAL en `cierre_pendientes`, hasta A-55 con el soporte de FTMO; enmendado por ADR-0082 en §4) |
| 0069 | A-42 RESUELTA: las dos sesiones son las velas H4 de la rejilla de `anclaje_h4` (H2b); deja superado ADR-0059 | ACTIVE |
| 0070 | Mayo solo se mide cuando una corrida del arnés sobre construcción, solo con las opciones de una lista cerrada, llega al umbral de ADR-0043 | ACTIVE (notas en §3: A-21 fijada el 2026-10-14; A-35 y A-44 fijadas el 2026-10-26, el motor ya no necesita ningún diagnóstico) |
| 0071 | Lo que fija la ejecución 1 de la demo de FTMO: la ficha de EURUSD, el stops level 0 y el volumen máximo 50; A-27 DECIDIDA | ACTIVE |
| 0072 | Quién lee la columna de fechas de un backtest (Aleks, para todo backtest) y los tres papeles: Aleks, el consultor y la sesión | ACTIVE |
| 0073 | La base del objetivo y el stop los fija el testimonio del trader; lo que el material contradice es una medición abierta (A-56), y ADR-0040 queda enmendado | ACTIVE (enmienda ADR-0040) |
| 0074 | El 1 de la caja de la orden stop se recalcula en cada cierre de M1 hasta el llenado: `caja_se_fija` = `en_cada_cierre_m1` | ACTIVE (enmienda la decisión 5 de ADR-0064; DEFAULT_AMBIGUOUS bajo A-49; nota en §4 por ADR-0083) |
| 0075 | Una H4 neutra con doble ruptura no decide el sesgo: se mantiene el anterior | ACTIVE (enmienda ADR-0060 §1 y §2; su §3 enmendado por ADR-0080; nota del 2026-10-26 en §1: el caso bajista confirmado en la sesión 5) |
| 0076 | «Limpia» es «sin alternancia de colores», y eso ya lo filtra RN-009: A-21 RESUELTA con `solo_una_zona_de_control`, sin opción nueva | ACTIVE (enmienda ADR-0055 §2 y §5; enmendado por ADR-0085 en la cabecera y en la fila del doji de §2, con nota del 2026-10-26 sobre S-10 por el camino real) |
| 0077 | La racha de pérdidas seguidas del trader: RN-036, aparte de RN-020, con cuatro parámetros; A-51 RESUELTA | ACTIVE (la lectura de la sesión sobre la racha tras la novena, §5) |
| 0078 | Julio de 2026 entra en construcción, del 1 al 17 (lo que cubre su libro) | ACTIVE (notas en ADR-0043 y ADR-0039 §1) |
| 0079 | Enero de 2026 entra en construcción, del 2 al 30 (lo que cubre su libro), al final de la lista | ACTIVE (notas en ADR-0043, ADR-0051 DN-5 y ADR-0069 §5) |
| 0080 | El sesgo de H4 cambia solo si la vela rompe el extremo de la anterior y cierra del color de esa ruptura | ACTIVE (enmienda ADR-0044 §2, ADR-0060 §1 y ADR-0075 §3; recuadros del 2026-10-26 en §4 y §9: D3 confirmada por el trader y la contradicción con la sesión 1 cerrada en la sesión 5) |
| 0081 | El lote que no cabe en el margen o en el volumen se limita, y el bróker simulado rechaza por margen libre al colocar y al llenar | ACTIVE (D1 confirmada por el trader en la sesión 5, 2026-10-23: A-57 RESUELTA, activada el 2026-10-26, con reservas en el recuadro de §1; enmienda ADR-0052 §4, ADR-0053 §1 y ADR-0026, Impacto) |
| 0082 | La capa de MT5 que nunca decide una operación va antes de F26: ejecuta, frena, veta, mide y registra, y ninguna de sus entradas es un hecho ni un parámetro de la estrategia | ACTIVE (enmienda MASTER_PLAN §0, la regla de PROJECT_STATE, ADR-0067 §1 y ADR-0068 §4; nota en ADR-0050 §4 y ADR-0053 §3.2) |
| 0083 | Qué gasta un punto: el rechazo (al colocar o al llenar) y el no envío; el llenado no, y tras una pérdida o un break even el mismo punto se vuelve a colocar, con la misma caja o con otra | ACTIVE (PROVISIONAL en D1: la sesión 5 respondió en parte, recuadro del 2026-10-26 en §1, y va a la sesión 6; enmienda la decisión 1 de ADR-0064; nota en ADR-0074 §4) |
| 0084 | La mecha que pasa el nivel de M15 y vuelve lo mueve a esa mecha: `liquidez_m15_mecha_que_vuelve` bajo A-35 | ACTIVE (DEFAULT_AMBIGUOUS en `cualquier_mecha`, lectura del consultor; A-35 sigue ABIERTA y la sesión 6 pregunta cuál mecha; enmienda ADR-0045; nota en ADR-0054) |
| 0085 | La vela sin cuerpo en M1 no corta la racha, no es contraria, no forma pivote, no entra en el extremo del punto y no cuenta como alternancia: «casi plana» es cuerpo cero | ACTIVE (enmienda ADR-0076 §2 y su cabecera; nota en ADR-0061 §4; la condición de `ev-v15-004037`, las mechas de la vela sin cuerpo y las velas de 1 o 2 puntos, a la sesión 6) |
| 0037 | La granularidad del dato decide que se abre, no el tipo de fichero | ACTIVE (con correccion del 2026-09-21 en su decision 7: el objetivo no es `idealTP` ni `maxTP`, es la regla `objetivo_rr`) |
