# Encargo · trabajo/activar-sesion-06-motor

Dado por Aleks (consultor) el 2026-11-05, en un solo mensaje. Copiado tal cual (el ADR que el
encargo manda escribir, ADR-0089, fue declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`, hasta el commit de la fase 1, que lo crea):

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-05) · trabajo/activar-sesion-06-motor · tramo R4 (R4.2, el motor de la activación de la sesión 6; F de la Next Action)
>
> Rama nueva: trabajo/activar-sesion-06-motor, desde main (04ec025, commit de estado sobre el merge df0e672 del tag stable/F38n-activar-sesion-06; CI de main en verde, run 42147004153: compruébalo con un gh run view suelto, sin guion). Ábrela con la skill abrir-rama: base comprobada con git (su paso 1), contrato con tramo R4, riesgo alto (motor), artefacto docs/validation/ACTIVAR-SESION-06-MOTOR.md. El recorrido lo mandan las skills activar-sesion, fase-cero, comparar-con-main y entregar-rama; si este encargo y ellas chocan, ganan ellas y lo dices. Es una rama de laptop: necesita data/ para las medidas de la fase 0.
>
> ESTA RAMA CORRE SOLA DE NOCHE
> Aleks no va a estar delante. Por eso la PARADA de la fase 0 es CONDICIONAL: la escribes entera en el informe, la commiteas, y después:
> - cada fase de abajo cuya medida de la fase 0 CUADRE con mi decisión (los criterios de cuadre están escritos en cada fase) se hace;
> - cada fase cuya medida NO cuadre se deja marcada en la PARADA con la alternativa que ves, sin tocar su código, y la rama sigue con las demás;
> - si no cuadra ninguna, o si algo de holdout o de guardia te frena, te quedas en la PARADA.
> Lo que sí haces en cualquier caso: terminar con el informe, el revisor y «Rama lista para revisión, NO cerrada». Nunca cierras: la orden de cierre la da Aleks por la mañana tras mi revisión. Si la laptop se queda sin memoria en un make check (PICO DE MEMORIA en la última línea del log), no relances a ciegas: espera a que acabe lo que corre y repite una sola vez.
>
> OBJETIVO
> Que el motor haga lo que el trader fijó en la sesión 6 y la rama trabajo/activar-sesion-06 dejó en ACTIVAR-SESION-06.md §«Para la rama de motor» (sus cuatro puntos, con fichero:línea): el reinicio del tope del trader al abrir la primera sesión del día siguiente (S-2), la vela sin cuerpo en M15 (S-4), la condición del punto de breaker (S-22) y el rechazo por precio inválido que no gasta el punto (S-19). Y que A-44 quede RESUELTA si con S-2 ya no le queda nada abierto.
>
> QUÉ NO CAMBIA
> - Ninguna otra regla del motor: ni RN-004 ni RN-009 ni el break even ni la caja ni los cartuchos. Solo lo que nombran las cuatro fases.
> - Nada fijado se pisa sin su régimen: lo CONFIRMED sigue; lo DEFAULT_AMBIGUOUS de A-35, A-48 y A-53 sigue como quedó en F38n.
> - Ninguna cifra dentro de una forma ejecutable (ADR-0002).
> - Sin corrida que cuente: ninguna corrida del arnés con la lista cerrada de ADR-0070 §3 (--simular sin --diagnostico-* ni --depuracion), que es la re-corrida que va después de H y R. Lo autorizado en esta rama, solo para medir en la fase 0: el arnés con --depuracion sobre el respaldo M1 (cli.py:2342-2343: NO cuenta) o con una opción --diagnostico-* (como la corrida diaria del respaldo, --simular --diagnostico-cuenta-diaria), solo sobre los meses de desarrollo (enero del 2 al 30, abril, julio del 1 al 17 y agosto, como en anexos/RESPALDO-M1/README.md; la compuerta del arnés usa casos_ocultos y se declara igual), con la salida en la carpeta de trabajo (no en docs/) y de ella solo RECUENTOS al informe: nunca cobertura, fidelidad, fechas ni resultados de operaciones.
> - Las citas salen SOLO de los ítems de evidencia que §«Para la rama de motor» nombra, con el texto del ítem. Las notas de un registro llevan solo lo de su ítem (ERRORES-RECURRENTES.md:37).
> - La Next Action y la hoja de ruta no se tocan en la rama; sus líneas se preparan en el informe. La tabla Known Ambiguities sí, en el commit que cierre A-44 (test_kit.py).
> - El Makefile, .claude/ y la guardia no se tocan.
>
> FECHAS DE LOS REGISTROS
> Id de sesión 2026-11-04-sesion-06; --fecha 2026-11-04 --recibido-el 2026-11-04 --procedencia trader_grabado --medio video; t0 y t1 los del ítem; la carpeta knowledge/feedback/2026-11-04-sesion-06/ ya existe.
>
> MIS DECISIONES (2026-11-05)
>
> FASE 1 · S-2, el reinicio del tope del trader (A-44)
> Lo que dijo: vuelve a contar al abrir la primera sesión del día siguiente (ev-v17-000250-a468bcec); del viernes, el lunes, «siempre es de sesión en sesión» (ev-v17-000351-331daa6d).
> 1. Parámetro NUEVO en knowledge/spec/parametros.yaml: perdida_trader_reinicio, categoría estrategia, tipo enum (como perdida_trader_alcance, parametros.yaml:1484-1488), opciones [medianoche_huso, primera_sesion_dia_siguiente], consumido_por ADR-0089, con la descripción de qué hace cada lectura. Nace UNKNOWN y pasa a CONFIRMED primera_sesion_dia_siguiente por registro RESOLVE_UNKNOWN sobre el parámetro con ev-v17-000250-a468bcec (notas solo con su ítem; el del viernes va a la descripción). perdida_trader_reinicio_huso se queda UNKNOWN y su descripción dice «SIN EFECTO con perdida_trader_reinicio = primera_sesion_dia_siguiente» (el precedente de perdida_maxima_semanal).
> 2. Motor: engine/tope_trader.py. TopeTrader gana el modo de reinicio. Con primera_sesion_dia_siguiente, SeguidorTope corta el día en el instante de apertura de la primera sesión del día siguiente con actividad (el `primero` que cableado.py calcula de dia.limites(), :245-247), con el saldo de ese instante; la semana se corta en la apertura de la primera sesión del primer día de la semana con actividad (el lunes, o el siguiente si el lunes no tiene sesiones): «de sesión en sesión». Un viernes no corta el sábado ni el domingo: corta el lunes al abrir. Con medianoche_huso todo sigue como hoy (avanzar, :230-240). El seguidor recibe la apertura desde cableado.py donde hoy se construye (:266-269) y en cada día nuevo con cuenta arrastrada; con cuenta_diaria no cambia nada (se reinicia con la cuenta). La traza dice qué modo corta y, con primera_sesion_dia_siguiente, no marca SUPUESTO ningún huso, porque no usa ninguno.
> 3. ADR-0089 nuevo (el 0087 no existe y no se rellena: PROJECT_STATE.md:101; se numera desde 0089): el reinicio del tope del trader de sesión en sesión; enmienda ADR-0053 §3.3 y §9 con recuadro fechado y su fila del índice.
> 4. Tests: uno que rompe en main (con el registro real, el seguidor corta en la apertura y no en la medianoche: comparar-con-main); uno sintético con dos días seguidos en los que el saldo cambia entre la medianoche y la apertura, donde los dos modos dan bases distintas, y otro donde no cambia y dan la misma; el caso viernes → lunes; y test_preparar_a44.py:145-162 cambia de sentido a propósito (ya no asierta huso_supuesto).
> 5. A-44: si en la fase 0 compruebas que después de esto no queda ninguna parte de su pregunta sin regla general (alcance y unidad, sesión 5; magnitud, S-1; reinicio, S-2), A-44 pasa a RESUELTA: registro RESOLVE_UNKNOWN sobre la ambigüedad con ev-v17-000250-a468bcec, cinco sitios, test_kit.py (bloqueantes ABIERTAS queda {A-35}; EN_PARTE_SESION_4 pierde A-44; RESUELTAS la gana), la hoja de preguntas si la lleva, y el test de control de la sesión 6 (tests/unit/test_en_parte_no_se_cierra.py, A.10 de F38n) se reescribe A PROPÓSITO: A-44 sale de las que exige ABIERTAS, con el motivo en su docstring (la «en parte» de S-2 era por falta de opción en el enum, no por la respuesta); SESION-06-EXTRACCION.md es un informe cerrado: recuadro fechado junto a su tabla final diciendo que S-2 resuelve con la opción nueva. Si algo de A-44 sigue sin regla general, se queda ABIERTA y lo dices.
> CUADRA si: el seguidor solo lo construye cableado.py (:266-269) y el arnés/visor por él; `primero` es la apertura de la primera sesión del día en UTC; y ningún otro lector de perdida_trader_reinicio_huso existe fuera de tope_trader.py.
>
> FASE 2 · S-4, la vela sin cuerpo en M15 (A-35, parte resuelta)
> Lo que dijo: la vela sin cuerpo no corta la racha de M15 y el alto puede ser su mecha, también con dos o tres seguidas, y en un bajo igual (ev-v17-002155-f2c95111, ev-v17-002250-d6ca3ef8, ev-v17-002217-af442f84).
> 1. domain/pivotes_m15.py: tercera lectura de sin_cuerpo, SIN_CUERPO_NO_CORTA_Y_CUENTA = "no_corta_y_cuenta": la vela de cuerpo cero ni corta la racha ni es contraria, y SÍ entra en la racha, así que su extremo cuenta en el nivel. Las de cuerpo cero que quedan por DELANTE del primer color de la racha (antes de la primera vela del color) no entran: la racha empieza en una vela con color. Es lectura del consultor, y el docstring lo dice. M1 sigue con no_cuenta (estructura_m1.py:136) y el valor por defecto sigue siendo corta_la_racha.
> 2. El llamador de M15 (engine/motor.py:156-164, pivote_mas_reciente) pide no_corta_y_cuenta; pivotes_formados y pivote_mas_reciente ya admiten sin_cuerpo. Los dos guiones que llaman a pivotes_formados sobre M1 sin pasar sin_cuerpo (scripts/bloque_de_la_caja.py:204 y scripts/caja_77_exploratoria.py:175, que leen con corta_la_racha y divergen de estructura_m1.py) no se tocan: se declaran en el informe como deuda de guiones.
> 3. ADR-0085: recuadro fechado en §2 («M15 no cambia» deja de valer: lo decidió el trader en S-4) con los tres ítems y su fila del índice; no hace falta ADR nuevo porque el selector existe y §2 dejaba M15 a la sesión 6.
> 4. Tests: test_pivotes_m15.py:149 (test_lo_fijo_y_visible_el_doji_corta_la_racha) cambia de sentido a propósito y pasa a probar M15 con la lectura nueva; uno nuevo con dos y tres velas sin cuerpo seguidas cuya mecha es el alto; uno con la de cuerpo cero por delante de la racha, que no entra; el test por marco de ADR-0085 sigue diciendo que M1 no se mueve; y uno por el camino real que rompe en main (comparar-con-main).
> 5. Medida en la fase 0 (el arnés con la autorización de «Qué no cambia», sobre desarrollo): cuántos pivotes de M15 cambian de nivel o de instante con la lectura nueva, por mes, solo recuentos.
> CUADRA si: el único llamador para M15 es el de motor.py y el del motor de M1 (estructura_m1.py:135-137) pasa no_cuenta explícitamente.
>
> FASE 3 · S-22, cuándo el máximo de la verde es punto de breaker (RN-007)
> Lo que dijo: para validar el punto, la roja de después tiene que haber roto el mínimo de la verde, con cuerpo o con mecha (ev-v17-015307-0870a8ca, ev-v17-015318-1256caf7); la frase de la mecha lleva el «m15» dudoso del ASR (ev-v17-015404-06ac0e9d) y se confirma en la sesión 7, pero la regla está dicha dos veces.
> 1. Lectura del consultor: «la verde» es la ÚLTIMA vela de la racha, la que precede a la contraria; la contraria la rompe si su mínimo (su máxima, en un bajo) pasa el extremo opuesto de esa verde, con mecha basta (compatible con A-32). Solo se aplica al punto de breaker: ultimo_punto_de_ruptura (estructura_m1.py:201-212), que es lo que forma el punto de la zona y de la orden en engine/zonas.py:382 con las dos lecturas de orden_stop_punto. NO se aplica a referencia_del_breaker (:124, el nivel que el breaker tiene que pasar) ni a zonas_de_control (:167): la fase 0 confirma esa lista de llamadores de _pivotes_m1 y dice si la condición se puede poner en ultimo_punto_de_ruptura sin tocar _pivotes_m1.
> 2. ADR-0085 §3, tercera viñeta: recuadro fechado: la condición de ev-v15-004037-a2ab3980 se aplica desde la sesión 6 porque el trader dijo «con cuerpo o con mecha»; con su fila del índice. RN-007 en strategy_spec.yaml gana la condición en su texto con Fuente: los ítems, y spec docs --escribir.
> 3. Medida en la fase 0 (el arnés con la autorización de «Qué no cambia», sobre desarrollo): cuántos puntos de breaker de la corrida dejan de formarse con (a) el mínimo de la última verde y (b) el mínimo de toda la racha, por mes, solo recuentos. Se implementa (a); (b) queda en el informe para la sesión 7.
> 4. Tests: los de test_estructura_m1.py que forman el punto con una roja que no pasa el mínimo de la última verde cambian de sentido a propósito (:219 seguro; :65 solo con la lectura (b), porque su roja sí pasa el mínimo de la verde inmediata: la fase 0 lo mide); uno nuevo con la roja que rompe solo con la mecha (vale) y otro que cierra dentro de la verde sin pasar su mínimo (no vale); uno por el camino real que rompe en main.
> CUADRA si: el punto de breaker se forma en un único sitio del dominio y los demás usos de _pivotes_m1 son separables sin tocarlos.
>
> FASE 4 · S-19, el rechazo por precio inválido no gasta el punto (ADR-0083 D1)
> Lo que dijo: cuando el precio ya está más allá del 0 al formarse la caja, la orden se pone igual, sigue siendo stop y el 0 se va actualizando con los altos nuevos (ev-v17-014103-8cf3e7fb, ev-v17-014235-f3375358, ev-v17-014350-ec133d13). En la corrida diaria del respaldo M1 son 37 de 1.329 órdenes (ACTIVAR-SESION-06.md §b.6).
> 1. Decisión: un rechazo AL COLOCAR por MOTIVO_PRECIO_INVALIDO (broker.py:543-555; el Rechazo lleva el motivo, broker.py:278-282) NO gasta el punto. El sitio es engine/primitivas_broker.py:655-659, donde el Rechazo al colocar llama a marcar_rechazada y tiene r.motivo a mano: con precio_invalido no marca, la zona sigue viva y la orden se vuelve a colocar en el siguiente cierre de M1 en el que el 0 vigente quede del lado bueno (RN-006 la mueve si el punto cambió). Lo demás no cambia: los otros motivos al colocar (stops level, volumen, margen), el no envío (primitivas_broker.py:639) y el rechazo AL LLENAR (cableado.py:140-166, cuyo EventoBroker no lleva motivo) siguen gastando (ADR-0083 D1). No se añade el motivo al EventoBroker: no hace falta. Lo de «el 0 se actualiza con los altos nuevos» con el precio por encima es otra cosa, el 0 como máximo corriente, y NO se implementa: va a la lista de la sesión 7 con un esquema (el precio ya por encima del 0 cuando se forma la caja: «¿dónde está tu orden en ese minuto?»).
> 2. ADR-0083: recuadro fechado en D1 con la excepción y los tres ítems; su fila del índice; D1 sigue PROVISIONAL para lo demás.
> 3. Tests: test_punto_usado.py:343 (test_el_rechazo_al_colocar_sigue_gastando_el_punto) cambia de sentido a propósito y pasa a probar que con precio_invalido el punto sigue vivo y la orden vuelve a colocarse cuando el precio baja; uno nuevo donde un rechazo por stops level o margen sí gasta; uno por el camino real que rompe en main. Que el informe de simulación (cableado.informe_simulacion) siga contando los rechazos como rechazos.
> CUADRA si: los únicos sitios que escriben «rechazados» son primitivas_broker.py:639 y :659 y cableado.py:165, y el Rechazo al colocar llega a :655 con su motivo.
>
> FASE 0 (skill fase-cero; auditor-encargo al empezar)
> a. Tabla: las cuatro fases, con lo que hace hoy el código (fichero:línea), los llamadores, el test que lo prueba y si CUADRA según el criterio de cada fase.
> b. Mide, sin escribir en el repo:
>    1. los llamadores de SeguidorTope, perdida_trader_reinicio_huso, pivotes_formados/pivote_mas_reciente (por marco), _pivotes_m1 y ultimo_punto_de_ruptura, y marcar_rechazada;
>    2. lo que queda de A-44 (fase 1.5): su pregunta de ambiguedades.yaml, parte por parte, con la regla general que la cierra o «sin regla»;
>    3. los recuentos de las fases 2 y 3 con el arnés en el modo autorizado en «Qué no cambia», sobre desarrollo (compuerta y casos_reservados antes; salida en la carpeta de trabajo; al informe solo los recuentos);
>    4. qué tests cambian de sentido con cada fase (comparar-con-main), con la salida de main;
>    5. el flaky del cierre de F38n: tests/unit/test_valores.py::test_ida_y_vuelta_por_yaml_sin_perdida (@given, :50-51, sin settings) saltó por el deadline de Hypothesis (352 ms frente a 200 ms, luego 15 ms). Si es solo el deadline, se le pone @settings(deadline=None) en un commit propio, declarado; si es otra cosa, al informe;
>    6. PROJECT_STATE.md está en 22.615 bytes; con la fila de A-44 fuera y la F nueva tiene que quedar por debajo de 23.000.
> c. Plan de commits: uno por fase (motor + ADR o recuadro + tests + registro), uno para el cierre de A-44 si procede, uno para el flaky si procede, y el informe.
> d. La PARADA, en el informe y commiteada: la tabla, lo medido, y por fase «CUADRA: se hace» o «NO CUADRA: se deja, por esto, con esta alternativa». Luego sigues con lo que cuadra.
>
> DESPUÉS DE LA PARADA
> Cada fase que cuadra, en su commit: el código, su ADR o recuadro con la fila del índice, los tests (los que rompen en main, los que cambian de sentido con el porqué en el commit), el registro si lo lleva, spec_version subida con uv run botsito spec manifest --escribir y uv run botsito spec docs --escribir cuando toque knowledge/spec, uv run botsito knowledge validate antes de make check, y Fuente: en el cuerpo con ids que existen. Cada make check con su salida a fichero y sellado. En el informe, el diff de sentido de cada test con la salida de main y la de la rama pegadas.
>
> HOLDOUT
> - Solo construcción, comprobada con casos_reservados antes de cada corrida; nunca listes carpetas de meses reservados con un filtro detrás: rutas literales en el propio comando. Dale esta regla también al revisor.
> - Toda exposición, aunque sea dudosa, el mismo día en docs/validation/HOLDOUT-EXPOSICIONES.md y en el informe.
> - Ninguna fecha de día reservado ni ningún resultado de operación en nada de lo que escribas; de las corridas, solo recuentos.
>
> ENTREGA (skill entregar-rama)
> - CI de Linux con git push origin trabajo/activar-sesion-06-motor:refs/heads/fix/activar-sesion-06-motor, y el número de run; solo se acepta el fallo de state check; se espera a que termine antes de lanzar el revisor (gh run view suelto, sin bucle).
> - Si el clasificador niega un push o la guardia un make, no lo rodees: escribe el comando exacto en el informe y en la PARADA y sigue con lo que no dependa de él; Aleks lo lanza por la mañana con «!».
> - Revisor (opus) con cinco alcances: (1) cada fase hecha tiene su ADR o recuadro con fila del índice, su test que rompe en main y, si cambia de sentido un test, el porqué en el commit; (2) ninguna regla fuera de las cuatro fases cambia (diff de src/ contra main, fichero a fichero); (3) las citas solo de los ítems nombrados, y las notas de cada registro solo con su ítem; (4) si A-44 se cierra, sus cinco sitios, test_kit y el test de control reescrito con su motivo; (5) ninguna corrida con --simular y ningún número de cobertura o fidelidad en el informe. Su informe, pegado al final.
> - Al final del informe, las líneas preparadas para el commit del contrato:
>   - Next Action F sustituida entera: «F. Sesión 6 ACTIVADA en spec (F38n) y motor (este tag): [lo hecho por fase, en una línea cada una; lo que no cuadró, con su alternativa]. A-44 [RESUELTA | sigue ABIERTA por …]. Siguiente: H (diagH\ como fase 0), R y la re-corrida que cuenta (ADR-0070 §3); después, la rama de preparación de la sesión 7 (hoja + gráficos 2 a 6 con contexto, lista en ACTIVAR-SESION-06.md §«Para la sesión 7», más el 0 como máximo corriente de S-19 y la lectura (b) de S-22). El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo. R6a en los huecos.»
>   - Hoja de ruta: R4.2 Estado «HECHA (spec F38n, motor este tag)» o lo que quede; R4.3 pierde la dependencia de la rama de motor; en «Fechas fijas» sale la línea de la ejecución 3 de la demo («del 2 al 6 de noviembre»: hecha el 5).
>   - ERRORES-RECURRENTES: la fila de la rama; en la columna del consultor, solo lo que sea mío.
>   - El tamaño final de PROJECT_STATE.
>
> Rama lista para revisión, NO cerrada.
