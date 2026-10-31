# Encargo · trabajo/margen-pendiente

Dado por Aleks (consultor) el 2026-10-30. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Encargo de rama: trabajo/margen-pendiente (el script 1.2 de MedirDemoFTMO para la ejecución 3, entrada A de la Next Action y A.1 de la hoja de ruta; y PROJECT_STATE adelgazado para que quepa la ingesta de la sesión 6). Consultor, 2026-10-30.
>
> 0. APERTURA
> - Base: main en 6948375 (commit de estado del cierre de trabajo/respaldo-m1), sobre el merge 4b12a92 con tag stable/F38j-respaldo-m1. Verifica con gh que la CI de main 40943847054 está en verde (no está escrita en el repo). La skill abrir-rama comprueba main, origin, el tag, la CI y que no hay otra rama. El worktree wt-ci, si sigue, no se toca.
> - Abre la rama con la skill abrir-rama: este prompt, tal cual, en docs/encargos/trabajo-margen-pendiente.md; contrato.yaml con tramo: "Carril: lo de Aleks" (entre comillas) y riesgo alto, con el motivo en el comentario (un script que envía órdenes a la cuenta de prueba de FTMO); y el Archivo de PROJECT_STATE en HISTORIA.
> - Rutas del contrato: docs/encargos/; tools/mql5/MedirDemoFTMO.mq5; tools/mql5/README.md y scripts/README.md, solo si nombran la versión o lo que hace el script; scripts/leer_demo_ftmo.py; tests/unit/test_leer_demo_ftmo.py; un test estático nuevo del script en tests/contract/; docs/runbooks/DEMO-FTMO.md; docs/validation/MARGEN-PENDIENTE.md y sus anexos; PROJECT_STATE.md; docs/state/HISTORIA.md (solo se amplía); docs/state/README.md (solo la condición (e) de abajo); y docs/plan/HOJA-DE-RUTA.md, solo para quitar las referencias HER:n de los heredados que salgan (test_hoja_de_ruta lo exige). HOLDOUT-EXPOSICIONES.md solo si hay exposición. Nada más sin ampliar el contrato en un commit a la vista.
> - Calendario: la sesión 6 con el trader es el martes 3 de noviembre y su ingesta necesita la rama libre; la ejecución 3 es entre el 2 y el 6 de noviembre, salvo el martes. Esta rama tiene que quedar lista para revisión cuanto antes, y en cualquier caso antes del martes 3. Si no llega, Aleks hace la 3 con el script 1.1 y la medida del margen pasa a la siguiente prueba (lo que ya dice la entrada A).
>
> 1. OBJETIVO
> Dos cosas, en este orden:
> a) El script 1.2 de MedirDemoFTMO: los pasos 1 a 7 de la 1.1 sin cambios y un paso 8 que mide cuándo comprueba MT5 el margen de una orden pendiente stop (ADR-0081 §4: el bróker simulado lo comprueba al colocar y al llenar, y «cuándo lo comprueba MT5 de verdad se mide en la demo»). El lector lo lee y da la respuesta con una regla escrita ANTES de ejecutarlo.
> b) PROJECT_STATE (24.393 bytes en main, tope 25.000) adelgazado hasta que la copia con todas las líneas del cierre de esta rama mida 21.800 bytes o menos (wc -c). Hace falta margen: la ingesta de la sesión 5 lo subió 997 bytes (23.733 en main antes de abrirla; 24.730 en su commit del contrato, b678ad4), el cierre de respaldo-m1 lo subió 1.459 (de 22.956 a 24.415 en 884301d), y después vienen la activación de la sesión 6 y R.
>
> QUÉ NO CAMBIA: src/ entero; mql5/ entero; knowledge/ entero (spec, casos, parámetros, cuentas, simulador); ningún ADR (lo que mida la ejecución 3 entra con la rama que congele los CSV de las ejecuciones 2 y 3, A.1); los pasos 1 a 7 del script, salvo la versión; lo que el lector dice de un CSV 1.0 o 1.1, byte a byte; el CSV de la ejecución 2 en data/demo_ftmo/ (no se congela aquí); el texto de las entradas de la Next Action (lo que cambie va en las líneas del cierre); y ninguna cifra. Si algo de esto tiene que cambiar, PARADA.
>
> Esta rama NO ejecuta el script en ninguna cuenta: lo ejecuta Aleks en la ejecución 3.
>
> 2. FASE 0 · INVENTARIO SIN TOCAR NADA (entrega antes de escribir código; PARADA al final)
> Mide, no razones: cada afirmación con fichero:línea, la salida de un comando o la URL consultada con su fecha.
>
> a) El script 1.1. Lo que el auditor del consultor ya ha visto, y verificas:
>    - VERSION_SCRIPT "1.1" (:31), #property version "1.10" (:27), MAGICO (:33); las funciones Cotizacion, PonerCaducidad, PendienteViva, BorrarPendiente, PrecioDelLlenado, CerrarPosicion, Limpiar y MargenAlcanza (con OrderCalcMargin);
>    - OnStart limpia al empezar, tras los pasos 3, 4, 5 y 6 y al terminar; el paso 7 depende de InpMedirLlenadoStop; si un paso falla, los siguientes se saltan;
>    - Fila escribe el fin de línea a mano («\r\n», :126): el paso 8 escribe con Fila y Dato, como los demás;
>    - las peticiones: EnviarPendiente (pasos 3, 4 y 5) va sin stop a propósito («SIN stop ni objetivo»); CerrarPosicion es un cierre con req.position, sin stop; MedirComision y MedirLlenadoStop llevan magic, stop y, la pendiente, caducidad.
>    - Las líneas que citan otros ficheros: la condición DEMO de Comprobaciones está en :759 y la citan ADR-0082 (:116), mql5/Include/Botsito/Capa/Cuenta.mqh (:8) y tests/contract/test_capa_mt5.py (:10 y :278); y condicion_de_medir (test_capa_mt5.py:143-151) toma la PRIMERA línea del fichero con ACCOUNT_TRADE_MODE_DEMO. Ni el ADR ni mql5/ se tocan, así que la 1.2 no puede mover esa línea: nada de lo que añada va antes de :759 cambiando el número de líneas, y el paso 8 no repite esa comprobación antes de ella. Mi lectura es que el paso 8 va después de Comprobaciones (entre ella y OnStart, o tras OnStart con su prototipo antes de OnStart); verifica en la documentación de MQL5 que admite prototipos o llamadas a funciones definidas más abajo, y la compilación lo prueba. Si no cabe sin mover :759, PARADA.
>
> b) La documentación, buscada y no recordada. En la documentación oficial de MetaTrader 5 / MQL5, con URL y fecha de consulta:
>    - cómo se calcula y se carga el margen de una pendiente stop (la página que cita ADR-0081 §4 y la que haga falta);
>    - el margen en una cuenta de hedging (ACCOUNT_MARGIN_MODE, SYMBOL_MARGIN_HEDGED);
>    - el código de retorno que da el servidor cuando falta margen, con el nombre de la constante;
>    - qué son ACCOUNT_MARGIN y ACCOUNT_MARGIN_FREE, y si cuentan las pendientes.
>    Si la documentación no dice algo, se escribe que no lo dice: es lo que mide el paso 8. El modo de margen de la prueba nueva (la del 2026-10-29) no está escrito en el repo: el RETAIL_HEDGING se midió en la prueba vieja (DEMO-FTMO.md). Lo dice la fila modo_margen del paso 1 de cada CSV, y el paso 8 lo vuelve a escribir junto a SYMBOL_MARGIN_HEDGED.
>
> c) El diseño del paso 8. Tiene que responder estas cuatro preguntas, cada una con su fila o filas en el CSV:
>    - M1 · ¿Rechaza MT5 al COLOCAR una pendiente stop cuyo margen no cabe en el margen libre? Una pendiente lejos del precio, que no salte, con el menor volumen admitido (mínimo, máximo por orden y paso, leídos en el momento) cuyo margen (OrderCalcMargin) pase del margen libre. Retcode y texto. Si la acepta, se borra en cuanto se lee.
>    - M2 · ¿Una pendiente stop viva carga margen, y a qué precio? ACCOUNT_MARGIN y ACCOUNT_MARGIN_FREE antes y después de colocar una que cabe, lejos del precio, comparados con OrderCalcMargin al precio de la orden y al ask o el bid del momento. La distancia tiene que bastar para que las dos cifras se distingan (ADR-0081 §4 carga la stop viva «a su precio» y comprueba al colocar con el ask o el bid).
>    - M3 · ¿Suma MT5 el margen de las pendientes al colocar otra? Dos pendientes del mismo lado que caben solas y no juntas.
>    - M4 · ¿Comprueba al LLENAR? Una stop que cabe al colocarla y cuyo margen ya no cabe cuando salta. Si M2 dice que la pendiente carga su margen, el margen se ocupa con pendientes lejanas, que no tienen riesgo de mercado, y no con posiciones; si dice que no, se ocupa con una posición del MISMO lado (en hedging, los lados opuestos se calculan aparte: lo dirá b). Si con el tope de e) no se puede medir, el CSV dice «no medible» y su motivo.
>    Para cada una: los volúmenes, calculados por el script con OrderCalcMargin y el margen libre del momento (nunca un lote fijo); las distancias; el orden de las operaciones; las filas exactas (medicion, clave, valor, retcode, nota); y un input propio que active el paso 8 (por defecto, activado), tras el paso 7 y con su Limpiar.
>    Ojo con los volúmenes: con unos 100.000 de margen libre y unos 3.720 USD de margen por lote (la ejecución 2), M1 pide unos 27 lotes y M3 y M4 posiciones o pendientes de 13 a 27 lotes. El máximo de 50 por orden se midió en la prueba vieja: el script lo lee.
>
> d) La regla de lectura, escrita ANTES de que nadie ejecute el script: para cada una de M1 a M4, qué filas dan «sí», cuáles «no» y cuáles «no concluyente», y qué imprime el lector.
>
> e) La seguridad, que manda sobre el diseño:
>    - el script sigue negándose fuera de una cuenta DEMO, y el paso 8 solo corre después de Comprobaciones;
>    - toda petición del paso 8 que abre o coloca lleva MAGICO y stop de protección, y toda pendiente, la caducidad de PonerCaducidad; toda salida del paso 8, también la de error, pasa por Limpiar;
>    - tope de pérdida: 1.000 USD en el peor caso para todo lo que el paso 8 pueda tener a la vez, que es la quinta parte de la pérdida diaria máxima de FTMO (5 % del capital inicial, FTMO-REGLAS.md R2; R2 vigila la equidad con las comisiones dentro). El peor caso cuenta las posiciones abiertas Y las pendientes que puedan llenarse, cada una hasta su stop de protección, más la comisión de ida y vuelta (2,50 USD por lote y lado) y un margen de deslizamiento que propones con su fuente. Se calcula con OrderCalcProfit ANTES de colocar o abrir; si pasa de 1.000, no se coloca ni se abre y se escribe en el CSV. Con 27 lotes eso deja stops de protección de unos 2 a 4 pips: dilo con la cifra. Perder la prueba de FTMO costaría la ejecución 3 y lo que quede de A-28;
>    - las peticiones al servidor del script entero, 1.1 frente a 1.2, contadas (el límite de 2.000 al día es FTMO-REGLAS.md R13; el freno del bot, ADR-0067);
>    - el tiempo del paso 8 en el peor caso.
>
> f) La compilación. Por la línea de órdenes de EA-CONEXION.md §0.a, sobre una copia fuera del repo: el log se crea junto al fuente, en UTF-16LE con BOM, y el código de salida va al revés (1 es éxito), así que la puerta es la línea «Result: 0 errors, 0 warnings» más el .ex5. compilar.py solo exporta mql5/, no tools/mql5/. Verifica que la ruta del terminal sigue valiendo en esta máquina.
>
> g) El lector y la guardia. Con el lector cambiado, la guardia niega ejecutarlo por la línea crudo = ruta.read_bytes() (falso positivo de CRUDO_PYTHON, DEMO-EJECUCION-1.md §3.3; entrada K). No se rodea: la variable no se renombra y el patrón no se toca en esta rama. pytest sobre los tests del lector no lo niega (lo probó el auditor del consultor; verifícalo tú). La comprobación sobre el CSV real de la ejecución 2 (1.1) la lanza Aleks con «!»: tiene que dar lo mismo que en el cierre de respaldo-m1 (desfase 180; comisión -2.50 por lado con 1,00 lote; margen 3720.77 en la nota de volumen_comision; registro de cierre en HISTORIA). Y el lector no rechaza una carpeta con un 1.1 y un 1.2 (solo la mezcla dentro de un fichero): así seguirá, porque en data/demo_ftmo/ van a convivir.
>
> h) PROJECT_STATE. Bytes por sección y por línea (con su salto de línea). Después:
>    1. Cada línea de «Pendientes heredados», «Technical Debt» y «Reglas vivas», clasificada con las condiciones (a) a (d) de docs/state/README.md («Que sale de PROJECT_STATE, y con que criterio»), con su evidencia. Niega por defecto: con duda, se queda. Si sale un heredado, la entrada de la hoja de ruta que lo cita en Refs (HER:n) pierde esa referencia en esta rama.
>    2. Mi decisión de método, que esta rama escribe en ese README como condición (e), con fecha y rama, y como excepción declarada a la frase «lo que se queda no se resume ni se reescribe»: «(e) ACORTADA: una línea de Technical Debt de más de 200 bytes se queda en PROJECT_STATE con su arranque literal, sin reescribir, cortado al final de una frase o de un inciso, en 160 bytes como mucho y nunca dentro de una ruta ni de un id, seguido de " … (entera en HISTORIA, Technical Debt ACORTADA)". Si la línea citaba su informe con su sección, el paréntesis conserva esa cita delante. El texto entero va literal a HISTORIA, bajo "# Technical Debt ACORTADA · sale de PROJECT_STATE.md en <rama> (<fecha>)". No se aplica a una línea si ahorra menos de 60 bytes.» Para cada línea candidata, el texto exacto que quedaría y los bytes que ahorra.
>    3. Los tests que leen PROJECT_STATE (verifica la lista con grep; el auditor encontró trece, y miran el contenido de estas secciones test_hoja_de_ruta, por los heredados vivos, test_project_state_rutas, por las rutas, y test_ids_citados, por los ids): una línea acortada que pierda una ruta, un id o una referencia que alguno exija se queda entera, y lo dices.
>    4. La previsión: bytes de la copia con (a) a (d), con (e) y con las líneas del cierre de §5. El auditor calcula que (e) ahorra unos 2.400 a 2.650 bytes: puede no bastar. Si no baja de 21.800, PARADA con los candidatos que faltarían y sus bytes (por ejemplo, entradas largas de la Next Action del carril de guardias o las candidatas a ambigüedad sin abrir); ningún recorte fuera de (a) a (e) sin mi respuesta.
>
> i) Herencias. Busca en la Next Action, los pendientes heredados, el final de HISTORIA y los informes de octubre todo lo que nombre el script 1.2, MargenAlcanza, el margen de una pendiente, ADR-0081 §4 o adelgazar PROJECT_STATE, y di qué entra y qué no. Dos que NO entran: la deuda del CRLF del CSV es de la rama que congele los CSV de las ejecuciones 2 y 3; y el falso positivo de la guardia es de la entrada K.
>
> j) La ejecución 3, para el runbook. Las horas de Lima de la franja de 9:00 a 18:00 de España para el lunes 2, el miércoles 4, el jueves 5 y el viernes 6 de noviembre, medidas con zoneinfo (el auditor da 03:00 a 12:00; verifícalo). El martes 3 no.
>
> k) Exposiciones. Esta rama no lee material del trader, ni velas, ni ticks. Si algo lo lee, fila en HOLDOUT-EXPOSICIONES el mismo día; si no, dilo.
>
> PARADA con «Lo que necesito que decidas», numerado y con una recomendación por punto. Al menos: dónde va el paso 8 sin mover :759 (a), el diseño de M1 a M4 (c), la regla de lectura (d), la seguridad con el peor caso en dólares y los stops que salen (e), las líneas que salen por (a) a (d) y las que se acortan por (e) con la previsión (h), y lo que encuentres en b) e i).
>
> 3. FASE 1 · EL SCRIPT 1.2, EL LECTOR Y SUS TESTS (tras mi respuesta)
> - MedirDemoFTMO.mq5: VERSION_SCRIPT "1.2", #property version "1.20" y el paso 8 como lo decida la PARADA. La cabecera dice qué añade la 1.2 y deja de decir algo falso (hoy, en SEGURIDAD, «solo el volumen mínimo, salvo el paso 6»), sin cambiar el número de líneas antes de :759. El diff de los pasos 1 a 7 contra main va en el informe: solo puede cambiar la versión, y la condición DEMO sigue en :759.
> - Compilado sobre una copia fuera del repo, con la línea «Result:» del log pegada.
> - El lector: VERSIONES gana "1.2"; las respuestas de M1 a M4 (con la regla de la PARADA), el modo de margen y SYMBOL_MARGIN_HEDGED van en una sección APARTE que solo sale cuando hay un fichero 1.2, y no en la tabla de cada fichero; con solo ficheros 1.0 o 1.1, la salida es byte a byte la de main.
> - Tests del lector con CSV sintéticos: cada respuesta de M1 a M4 en sus dos sentidos y el «no concluyente»; un 1.2 con el paso 8 desactivado; un 1.1 que da la misma salida que en main; y una carpeta con un 1.1 y un 1.2.
> - Test estático del script, en tests/contract/: toda función que envía una petición TRADE_ACTION_DEAL o TRADE_ACTION_PENDING lleva req.magic; y lleva req.sl y, si es pendiente, PonerCaducidad, salvo las exentas por nombre en una lista cerrada con su motivo: EnviarPendiente (los pasos 3, 4 y 5 miden pendientes sin stop a propósito) y CerrarPosicion (es un cierre con req.position). Niega por defecto: una función nueva fuera de la lista tiene que cumplir. Rómpelo a propósito sobre una copia en la carpeta de trabajo (quitando un req.sl del paso 8 y, aparte, un PonerCaducidad, y añadiendo una función nueva que envía sin stop) y pega la salida en rojo; luego, en verde sobre el fichero de la rama. Esto se suma a lo que pida entregar-rama con comparar-con-main.
> - DEMO-FTMO.md: «Antes de la ejecución 3: el script 1.2» (copiarlo encima del que hay, F7 con «0 errors», y comprobar que el CSV y el lector dicen 1.2); el paso 8 en «Lo que mide cada paso»; las horas de Lima de j); qué hacer si sale «ATENCIÓN: quedan…»; y lo que el paso 8 deja falso en «Lo que hace, y lo que no hace nunca» (los volúmenes y los stops) y en el tiempo de la cabecera. Lo de la ejecución 2 se queda como está.
>
> 4. FASE 2 · PROJECT_STATE (tras mi respuesta, en commits propios)
> - La condición (e) en docs/state/README.md, con fecha y rama, como excepción declarada, sin reescribir lo demás.
> - Las líneas que salen, a HISTORIA, literales, con su condición y su evidencia, en sus bloques (# Pendiente heredado SALE, # Technical Debt PAGADA, # Technical Debt RECLASIFICADA, # Regla viva SUSTITUIDA, # Technical Debt ACORTADA), y en PROJECT_STATE ni un resumen de las que salen. Las referencias HER:n que sobren, fuera de la hoja de ruta en el mismo commit.
> - wc -c antes y después, por sección.
>
> 5. INFORME, REVISOR Y ENTREGA
> - docs/validation/MARGEN-PENDIENTE.md, con:
>   - la fase 0, la PARADA y mi respuesta tal cual;
>   - el script: el diff de los pasos 1 a 7, el paso 8, el log de compilación, la cuenta de peticiones y el peor caso en dólares;
>   - el lector y los tests, con la salida en rojo y en verde del estático;
>   - PROJECT_STATE: qué salió, qué se acortó, bytes por sección antes y después;
>   - el encargo frente a lo hecho y las desviaciones.
> - Las líneas del cierre, preparadas y medidas sobre una copia, sin aplicar en la rama:
>   - en la entrada A, la frase «Cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4) pide un script 1.2, que aún no existe: una rama corta antes de la 3; si no llega, esa medida pasa a la siguiente prueba.» pasa a «La 3 va con el script 1.2 (trabajo/margen-pendiente), que además mide cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4; paso 8, DEMO-FTMO.md).»;
>   - en la hoja de ruta, A.1: la frase partida en :479-480, «Falta un script 1.2 para el instante en que MT5 comprueba el margen de una pendiente stop (ADR-0081 §4).», pasa a «El script 1.2 (trabajo/margen-pendiente) mide en la 3 el instante en que MT5 comprueba el margen de una pendiente stop (ADR-0081 §4).», con las líneas reajustadas; y en R6a.6 (:432), «el script 1.2 de MedirDemoFTMO» pasa a «el script 1.2 de MedirDemoFTMO (HECHO, trabajo/margen-pendiente)»;
>   - PROJECT_STATE de la copia, con todas las líneas, medido con wc -c: 21.800 bytes o menos. Comprueba la copia contra tests/unit/test_hoja_de_ruta.py y test_project_state.py.
> - La fila de ERRORES-RECURRENTES de la rama, preparada en el informe (la escribe el cierre).
> - El revisor (opus), antes de declarar la rama lista, con estos alcances:
>   1. que los pasos 1 a 7 son los de main salvo la versión, que la condición DEMO sigue en :759 y que un CSV 1.0 o 1.1 da la misma salida del lector;
>   2. la seguridad del paso 8: solo tras Comprobaciones, toda petición con MAGICO, stop y (si es pendiente) caducidad, Limpiar en toda salida, el peor caso calculado antes de colocar o abrir, con pendientes, comisión y deslizamiento, por debajo de 1.000 USD, y el mismo lado en M4;
>   3. que la regla de lectura del lector es la de la PARADA, con tests en los dos sentidos, y que el test estático rompe de verdad y niega por defecto;
>   4. PROJECT_STATE: cada línea que sale tiene su condición, su evidencia y su texto literal en HISTORIA; (e) solo se aplica a líneas de más de 200 bytes que ahorran 60 o más, sin reescribir el arranque y sin cortar una ruta o un id; los tests que leen PROJECT_STATE y la hoja de ruta pasan;
>   5. que no se lee material, ni velas, ni ticks.
>   Su informe va pegado al final. Arregla lo que bloquee o importe, o di por qué no.
> - No toca hooks ni rutas: el fix/ en la CI de Linux no es obligatorio. Si la skill entregar-rama lo empuja igual, pega el número de run.
>
> Reglas de siempre:
> - make check > make-check.log 2>&1 antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado, y leer el log (exit 0, ningún failed y la línea SELLO). Nunca --no-verify.
> - Mensajes de commit con Write y git commit -F.
> - Si la guardia o el clasificador niegan algo legítimo, PARADA con el comando exacto, y lo lanza Aleks con «!». No se rodea; seguir la forma que propone la propia guardia vale, declarándolo (DECISIONES-DE-PROCESO.md).
> - Una sola rama abierta: la ingesta de la sesión 6 espera a que esta se cierre.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA (2026-10-31)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/margen-pendiente (2026-10-31). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Todo lo nuevo del paso 8 (constantes, InpMedirMargen, InpEsperaMargenSeg y funciones) va entre Comprobaciones y OnStart, sin prototipos. En las líneas 1 a 758 solo cambian :27, :31 y la cabecera en su sitio, con las mismas 25 líneas. La compilación de la fase 1 lo vuelve a probar, y el informe pega la línea 759 de la 1.2.
>
> 1. (a). Se corrigen las dos frases falsas de la cabecera y la de DEMO-FTMO.md:22, y #property description gana el margen de las pendientes. La frase nueva dice la verdad entera: las pendientes de los pasos 3, 4 y 5 van sin stop a propósito y, si una se llena al instante, el script la cierra en cuanto la lee; las demás posiciones llevan stop de protección.
>
> 2. (a), con cinco cambios en M2 y M4. Un «sí» o un «no» falsos de M4 acabarían en un ADR, porque la 3 es la única ejecución prevista; así que todo lo que no pruebe la causa sale «no concluyente».
>    a) La ocupación caída. Si V o P dejan de estar vivas antes de que S se resuelva, S puede llenarse con margen libre de sobra y el lector daría un «no» falso. Con V es físico: su stop común queda a unos 1,5 pips por debajo, S a 1 pip por encima, y en 120 s el precio puede bajar, cerrar V y volver a subir hasta S. Con P, la vía no es la caducidad (15 minutos) sino que el bróker la borre con el nivel de margen tan bajo (stop out o gestor de riesgo de FTMO; el repo no tiene esa cifra). Al resolverse S, el script escribe si la ocupación seguía viva (fila m4_ocupacion_viva, «si» o «no», con su ticket) y el margen libre justo antes de esa lectura. Ocupación caída → «no concluyente: la ocupación cayó antes de que se resolviera S».
>    b) El «sí» solo con la causa. Al saltar en el servidor, S no devuelve retcode, así que un rechazo o un borrado por otra causa no se distingue a ciegas (tope agregado de volumen, stops inválidos tras un hueco, stop out, una cancelación del cliente). Regla: «sí» solo si S queda sin deal, en estado REJECTED, con un comentario o un motivo del historial que nombre el margen, y con p8_volumen_limite = 0 o el volumen de S más el de la ocupación dentro de ese tope. CANCELED nunca da «sí». Cualquier otro caso de S sin deal → «no concluyente», con el estado y el comentario literales. Verifica en la documentación de MQL5 qué guarda el historial de una orden rechazada al saltar (ORDER_STATE, ORDER_COMMENT, ORDER_REASON u otro) y escribe en el informe qué campo usa la regla. Si ninguno puede nombrar el margen, M4 no da nunca «sí»: lo dices y el lector da «no concluyente» con lo que haya.
>    c) El llenado parcial. Si el volumen del deal de S es menor que el de S, «no concluyente».
>    d) M2 por las tres cifras. La documentación solo atribuye las pendientes a ACCOUNT_MARGIN_INITIAL. M2 escribe antes y después ACCOUNT_MARGIN, ACCOUNT_MARGIN_FREE y ACCOUNT_MARGIN_INITIAL, y la regla juzga «carga» por la bajada del margen libre (lo que importa para M4): carga si el libre baja al menos un 10 % del margen calculado. El precio se decide con esa misma bajada, por la mitad de D como en tu propuesta. El informe dice también qué hicieron ACCOUNT_MARGIN e INITIAL.
>    e) La comprobación antes de esperar, con lo que midió M2. M4 escribe el libre antes y después de colocar S. Si la pendiente reserva su margen, la condición es «libre + lo que reservó S < margen de S al llenar», no «libre < margen de S». Si no se cumple, «no medible».
>    Tests del lector con cada caso, en los dos sentidos: ocupación viva y caída; S rechazada con el motivo del margen, rechazada con otro motivo, y cancelada; llenado entero y parcial; y M2 con el libre que baja y con el libre que no baja aunque ACCOUNT_MARGIN suba.
>
> 3. (a), con el cambio de 2.d: el 10 % se mide en la bajada del margen libre; el precio, por la mitad de la diferencia D, con D ≥ 10 USD.
>
> 4. (a): 5,00 USD por lote y lado en el tope, el supuesto conservador del registro (ADR-0071), mientras el CSV de la ejecución 2 no esté congelado. Stops de 13 a 17 puntos. Es un cambio del encargo, que daba 2,50: el informe lo declara así.
>
> 5. (a). M (el break even de una venta que salta por el ASK) queda fuera de esta rama y sigue esperando a una prueba posterior. El informe lo dice en «el encargo frente a lo hecho».
>
> 6. Ninguna de las cuatro opciones: (d), pero escrita desde ya. «Al final de una frase o de un inciso» no incluye la coma de una enumeración: «Artifact…» se queda entera, y (e) se aplica en lectura estricta, sin el corte más corto de (b). Lo que falta lo pongo yo con las cabeceras del cierre, que escribo yo y que van a ser estas (con el sha y la fecha reales):
>    - Current Feature: «Ninguna rama abierta. trabajo/margen-pendiente cerrada en main el <fecha> (stable/F38k-margen-pendiente): MedirDemoFTMO 1.2, con el paso 8 (el margen de una pendiente stop), y PROJECT_STATE adelgazado (MARGEN-PENDIENTE.md).»
>    - Stable Main State: «<sha> · merge de `trabajo/margen-pendiente` (tag `stable/F38k-margen-pendiente`): MedirDemoFTMO 1.2 y PROJECT_STATE adelgazado. Sobre `stable/F38j-respaldo-m1` (4b12a92). Informe docs/validation/MARGEN-PENDIENTE.md; el registro del cierre, al final de HISTORIA.»
>    - Last Stable Commit: «<sha> · merge: trabajo/margen-pendiente, MedirDemoFTMO 1.2 y PROJECT_STATE adelgazado · tag stable/F38k-margen-pendiente»
>    Rehaz la previsión con estos tres textos y con la decisión 7, y pega la cifra. Mi auditor la estima en unos 21.755 bytes; mídela tú. Si no baja de 21.800, PARADA.
>
> 7. Sale el heredado 2; la deuda de cherry-pick se queda.
>    - Heredado 2, por (b), con la evidencia corregida: la versión entera del Archivo 1 vive en docs/runbooks/ENTRADA-MARZO.md (verifica que en :45-49), y CLAUDE.md:178-181 lleva lo esencial. Al salir, quedan falsas las frases que remiten a él: ENTRADA-MARZO.md:32 («Lo que falta sigue en PROJECT_STATE.md, pendiente heredado 2») y la prosa «heredado 2» de HOJA-DE-RUTA.md (verifica que en :338 y :499-500), además de HER:2 en las Refs de R5.3. Se amplía el contrato a docs/runbooks/ENTRADA-MARZO.md, en un commit a la vista, solo para esa frase, y las tres pasan a remitir a ENTRADA-MARZO.md, en el mismo commit que saca el heredado. Comprueba la copia contra test_hoja_de_ruta.
>    - La deuda de cherry-pick se queda: su texto entero (HISTORIA, Archivo 1) dice «la garantia de fondo sigue siendo la CI», que no está en CLAUDE.md ni en ningún runbook, y (b) exige el contenido vivo entero (ERRORES-RECURRENTES, fila de plataforma-adelantada). La opción (a) que recomendabas era contraria al README.
>
> 8. (a): fase 1 y fase 2 seguidas, sin otra PARADA salvo que algo medido contradiga una decisión de esta respuesta.
>
> Sobre §0.m. Quitar del guion la parte negada no es rodear la guardia si las medidas que quedaron (975 bytes de K y 554 de las candidatas) ya estaban hechas antes de la negativa, porque entonces no se ejecutó lo negado de otra forma. Si se hicieron después, con grep y wc -c, eso es cambiar de vía tras una negativa (DECISIONES-DE-PROCESO.md). El informe escribe el orden real y, en ese caso, lo declara como desviación. El falso positivo, en cualquier caso, es otra aparición de K: va en la fila de ERRORES-RECURRENTES preparada, no en la entrada K.
>
> La comprobación de Aleks con «!» sobre el CSV de la ejecución 2 no puede pedir el 3720.77, porque el lector no lo imprime (lo dijo tu fase 0). El criterio es que la salida del lector de main y la de la rama sean idénticas byte a byte. El informe da los dos comandos exactos, con las dos salidas fuera del repo.
>
> Para la fila de ERRORES-RECURRENTES del cierre, los errores del consultor que cazaron la fase 0 y el auditor:
> - (importa) El encargo dio como dato lo que decía el auditor del consultor sin medirlo: que (e) ahorraba de 2.400 a 2.650 bytes (son 2.169); que los stops saldrían de 2 a 4 pips (salen de 1,3 a 2,2); que trece tests leen PROJECT_STATE (lo leen seis y lo nombran trece) y que test_ids_citados lo lee (lo hace knowledge validate); que la comprobación de Aleks diera el margen 3720.77, que el lector no imprime; y citas de línea de test_capa_mt5.py (:143-151 son :142-149; :278 es una cadena de ejemplo). Es la lección del cierre de visor-construccion, repetida: lo que diga el auditor del consultor sobre una cifra, un recuento o un mecanismo va en el encargo como «verifica que…», nunca como dato.
> - (importa) En el primer borrador de esta respuesta acepté sacar por (b) la deuda de cherry-pick sin comprobar que su texto entero vive en otro sitio, que es lo que exige el README; lo cazó mi auditor antes de entregarla. Lección: antes de aceptar una salida por (b), leer el texto entero en HISTORIA y buscar cada frase.
> - (menor) El encargo nombró una frase falsa de la cabecera y no vio la segunda («toda posición lleva stop de protección»), falsa ya en la 1.1. Lección: antes de pedir que se corrija un texto, leerlo entero.
> - (menor) El encargo fijó 2,50 USD de comisión para el tope sin mirar que el registro mantiene 5 como supuesto conservador mientras el CSV no está congelado.
>
> Lo que sigue: el commit con esta respuesta y la ampliación del contrato a ENTRADA-MARZO.md; la fase 1 (script, compilación con la línea 759 pegada, lector, tests y runbook); la fase 2 (PROJECT_STATE, con la previsión rehecha); y el informe con las líneas del cierre preparadas sobre una copia, el revisor y la entrega. make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA 2 (2026-10-31)

Copiada tal cual:

> Respuesta del consultor a la PARADA 2 de trabajo/margen-pendiente (2026-10-31). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha.
>
> Opción 3, con la evidencia escrita en el bloque de HISTORIA, para que la salida no sea juicio sino hecho del repo. El heredado 2 sale por dos condiciones, frase a frase:
> - «MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE»: (c) SUSTITUIDA. Marzo llegó el 2026-09-30 y no interrumpió nada: entra por el camino de fidelidad, en su turno de la hoja de ruta (REGISTRO-MARZO.md, decisión del consultor del 2026-09-30, §«Marzo entra por el camino de fidelidad» y su aceptación; CLAUDE.md, párrafo «Marzo de 2026 esta RECIBIDO y SIN ABRIR»; R5.3). Verifica esas líneas y cítalas.
> - «El trader confirmo el 2026-09-21 que no habia visto febrero NI marzo, y backtestea MARZO»: (c) SUSTITUIDA por hechos posteriores: el backtest de marzo está recibido (REGISTRO-MARZO.md) y la confirmación escrita llegó el 2026-10-25 (SESION-05-EXTRACCION.md §3.5); lo de febrero sigue vivo en el heredado 6, que se queda.
> - El resto (vistos.yaml con visto_el y cobertura_material, fidelidad-2/3, CONFIRM «sin sus palabras, no vale»): (b) REPETIDA, entero en ENTRADA-MARZO.md:45-49.
> El bloque de HISTORIA va como «# Pendiente heredado SALE», con el texto literal entero y las tres condiciones con su evidencia. Lo demás del punto 7 sigue igual: ENTRADA-MARZO.md:32 y la prosa de la hoja de ruta pasan a remitir a ENTRADA-MARZO.md, HER:2 sale de R5.3, y el contrato se amplía a ENTRADA-MARZO.md solo para esa frase. Esto es distinto de lo que bloqueó el revisor en plataforma-adelantada: entonces se pedía (b) para la línea entera, y (b) no cubría las dos frases; ahora esas dos salen por (c) con su evidencia. Dilo así en el informe.
>
> Previsión aceptada: 21.784 bytes. Sigue con la fase 1 y la fase 2 como dice la respuesta a la PARADA.
