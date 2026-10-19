# Encargo · trabajo/ea-conexion

Dado por Aleks (consultor) el 2026-10-19. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/ea-conexion (hoja de ruta R6a.1, tramo R6a; ADR-0082). Encargo del consultor, 2026-10-19.
>
> 0. Apertura
> - Base: main en el commit de estado del tag de trabajo/barrido-sesion-5 (stable/F37w-…), que se cierra antes. Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de ese commit, con gh; si el clasificador niega gh, PARADA y la consulto yo con «!». Por orden del consultor, nunca con curl ni con un guion, aunque RITUAL.md lo traiga.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R6a.
> - Informe: docs/validation/EA-CONEXION.md. Anexos: docs/validation/anexos/EA-CONEXION/. En rutas_permitidas, además: mql5/, src/botsito/mql5bridge/, tests/ (con tests/golden/) y docs/runbooks/.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0; entregar-rama al final.
> - Revisa /model antes de empezar: Opus en esfuerzo alto.
>
> 1. Objetivo, y por qué va ahora
> El primer EA de la capa de MT5 que nunca decide una operación (ADR-0082): se conecta, se niega fuera de una cuenta DEMO, lee el reloj del servidor, las sesiones del símbolo y ACCOUNT_MARGIN_MODE, y lo escribe todo en el journal, con un formato único y versionado. No envía, no modifica y no cancela ninguna orden. Y, antes de una línea de MQL5 de la capa, la fase 0 mide cómo se compila y cómo se prueba MQL5 en mi máquina (ADR-0082 D7).
> Va en el hueco que deja V mientras se espera al trader (ADR-0082 D8: no le quita turno a V). Por eso tiene que estar cerrada antes de la ingesta de la sesión 5 (primera semana de noviembre): sin cerrarla no se puede abrir la rama de la ingesta. Si el 30 de octubre no está para cerrar, PARADA y decido yo.
>
> 2. Decisiones del consultor (2026-10-19; las tomo antes de medir, y las medidas no las cambian. Si la fase 0 encuentra un hecho que las contradiga —un ADR, una regla, la documentación oficial de MQL5 o lo que mida en MT5—, PARADA)
> D1. Dónde vive. El EA en mql5/Experts/ (su README: «el EA (F31)»); lo común, en mql5/Include/Botsito/; el script de pruebas, en mql5/Scripts/. Los README de Include/Botsito («dominio espejo y Params.mqh generado») y de Scripts («RunCases.mq5… (F30)») se amplían para decir qué pone R6a ahí; propón los nombres. tools/mql5/MedirDemoFTMO.mq5 no se toca: es el script de medida del carril de Aleks.
> D2. Lo que hace el EA, y nada más:
>  a. Lo primero de OnInit es la negativa fuera de DEMO, con la misma condición que tools/mql5/MedirDemoFTMO.mq5 (hacia :759; verifica y cita), dentro de una función que recibe el modo de la cuenta como argumento. El código de retorno de OnInit al negarse sale de la documentación oficial (cítala).
>  b. Al arrancar lee y escribe en el journal ACCOUNT_TRADE_MODE, ACCOUNT_MARGIN_MODE, el servidor, el símbolo del gráfico y todo lo que lee el paso 2 de MedirDemoFTMO (MedirReloj, hacia :386-399: TimeTradeServer, TimeCurrent, TimeGMT, TimeLocal, el desfase servidor − GMT, el desfase local − GMT y TimeDaylightSavings; verifica la lista). TimeGMT sale del reloj del ordenador (DEMO-FTMO.md): el procedimiento de D5 lo recuerda.
>     ACCOUNT_MARGIN_MODE: la hoja de ruta y ADR-0082 §10 dicen que R6a.1 lo «comprueba» al arrancar. Decido que en R6a.1 se lee y se registra, sin abortar, porque el valor con el que compararlo llega con el perfil generado (R6a.2) y la comparación que aborta es del pre-vuelo (R6a.7, MASTER_PLAN §H). Es una lectura mía del texto: el informe la declara y lleva su línea para la hoja (punto 6).
>  c. Las sesiones del símbolo con SymbolInfoSessionTrade, para cada día de la semana y cada índice de sesión hasta que la función diga que no hay más (la firma y lo que devuelve, de la documentación oficial), al arrancar y cada vez que cambia el día del servidor. Es la condición 2 de N (docs/runbooks/RENOVAR-CIERRES.md: «Sin una de las dos, esa rama no se cierra»): R6a.1 la lee; R6a.5 la usa para el veto. Si la fase 0 ve que SymbolInfoSessionQuote se lee igual y sirve a R6a.5, propónlo; no lo añadas sin mi respuesta.
>  d. Un latido por minuto (OnTimer) con el desfase, y una línea en OnDeinit con el motivo.
>  e. NUNCA envía, modifica ni cancela una orden ni cierra una posición. Niega por defecto: un test de Python lee los .mq5 y .mqh de la capa y falla si aparece cualquier función del grupo de funciones de trading de la documentación oficial de MQL5 o la clase CTrade de la biblioteca estándar, salvo las de una lista de lectura permitida, que en esta rama está vacía. La lista del grupo sale de la documentación oficial y se cita.
>  f. Ni el login ni ningún dato personal en el journal, como MedirDemoFTMO (DEMO-FTMO.md: «El script no escribe el login»; el repo es público). Tampoco saldo ni dinero: R6a.1 no los necesita.
>  g. Ninguna cifra de firma, bróker, instrumento ni ejecución escrita a mano (ADR-0082 D5): llegan generadas en R6a.2. Si R6a.1 necesitara una, PARADA.
> D3. El journal: un solo formato, versionado y compartido (ADR-0082 D7; MASTER_PLAN §H.2, fila «Estado de jornada no persistente en el EA»: el esquema de F23 es «versionado y compartido» con el journal de Python). Se define UNA vez en el repo, con un documento del formato (propón dónde) y un lector-validador de Python en src/botsito/mql5bridge/ (su docstring dice «parsea resultados (F28, F30)»: se amplía), con tests que corren en la CI de Linux.
>  - Una línea por evento, legible sin Excel; cada línea con la versión del formato, un número de secuencia, la hora del servidor, la hora GMT, el desfase, el evento y sus datos.
>  - Flush por línea y hash encadenado (MASTER_PLAN §H, fila «MQL5: …»: «journal con flush y hash encadenado»). Verifica en la documentación oficial que MQL5 da SHA-256 (CryptEncode) y qué hace FileFlush; si no, PARADA.
>  - LOS BYTES DEL HASH, fijados por el formato: el repo exige UTF-8 y LF (.gitattributes con eol=lf; test_no_crlf_in_tracked_text_files en tests/unit/test_repository_integrity.py), y el fichero de la ejecución 1 de MedirDemoFTMO salió con LF aunque el código escribe CRLF, sin explicación (DEMO-EJECUCION-1.md, hacia :48-72). Mi criterio: UTF-8 sin BOM, LF, y el hash de cada línea sobre sus bytes sin el fin de línea, encadenado con el de la anterior (la fórmula exacta la propone la fase 0). La fase 0 mide cómo escribe MQL5 esos bytes (modo de apertura y codificación) y por qué salió LF; si MQL5 no puede escribirlos así, PARADA.
>  - Los campos de esa fila de §H.2 (UTC, offset servidor, evento, regla, condición fallida, spec_hash, risk_hash, lecturas ambiguas): los que la capa no puede llenar todavía quedan reservados y se dicen. El hash de lo que la capa reciba lo fija R6a.2 (ADR-0082 D5): aquí, su campo reservado. El informe dice cómo lo leerán F23 (el journal de Python) y F34 (la demo frente al backtest, línea a línea).
>  - Prueba cruzada: el script de pruebas escribe, con el mismo escritor que el EA, las líneas de unos casos fijos; el validador de Python las acepta y recalcula la cadena. Esas líneas se commitean como golden en tests/golden/ (su README: «cambia solo con una decisión documentada»; la CI no tiene data/: ERRORES-RECURRENTES), y cambiar un byte rompe la cadena.
>  - El journal queda en MQL5/Files del terminal; Aleks lo copia sin abrirlo ni renombrarlo a data/, fuera de git, como el CSV de DEMO-FTMO.md. El de la corrida de cierre se congela en los anexos de la rama: el fichero tal cual (si ya cumple UTF-8 y LF) y su sha256 del original. No va a data/manifests/: su esquema es el del CSV de MedirDemoFTMO (data/manifests/README.md) y no se cambia aquí.
> D4. Compilar y probar (ADR-0082 D7). La fase 0 lo mide (punto 4) y lo decido yo en la PARADA, con estos criterios:
>  - lo que pueda ejecutar Claude Code, mejor que lo que haga yo a mano; si se queda así, cambia el «Quién» de R6a.1 en la hoja («Aleks compila y ejecuta»), con su línea en el punto 6;
>  - cada compilación deja su log en los anexos convertido a UTF-8 y LF (MetaEditor puede escribirlo en UTF-16: mídelo), con el sha256 del original, 0 errores y los avisos listados;
>  - las pruebas son de dos niveles: (1) estáticas, en Python, en make check y en la CI: el test de D2e, el de que la condición de la negativa es la de MedirDemoFTMO y el de que OnInit la llama antes que nada; (2) dinámicas, en MQL5, en el script de pruebas que se ejecuta en mi máquina: la negativa con REAL y CONTEST, el escritor del journal contra el golden, el cambio de día con una fecha inyectada. Las de (2) no corren en make check ni en la CI; su salida va a los anexos y el informe lo declara. Cada test de los dos niveles se rompe a propósito en los dos sentidos;
>  - en esta rama no entra un job de Windows en la CI (.github/workflows/ci.yml lo deja para F29).
> D5. La demo. La prueba actual vence hacia el 22 de octubre (DEMO-FTMO.md). La corrida de cierre va en la prueba nueva que creo el 26, el mismo día que la ejecución 2 de MedirDemoFTMO o después, y siempre con la ejecución 2 ya terminada. El procedimiento para mí, escrito en mi lenguaje, como DEMO-FTMO.md (propón si es un runbook nuevo o una sección de ese): comprobar que la hora de Windows está sincronizada; copiar, compilar y poner el EA en un gráfico de EURUSD con el mercado abierto; dejarlo puesto hasta que cruce la medianoche del servidor (el journal dice cuándo es; en Lima cae por la tarde), para que el cambio de día se vea en la demo y no solo en la prueba con la fecha inyectada; quitarlo y volver a ponerlo (el journal sigue la cadena o empieza otro fichero: lo que fije el formato); y copiar el journal. La negativa fuera de DEMO no se puede ejecutar en una cuenta real: queda probada por los dos niveles de D4, y el informe lo declara así.
> D6. R6a.1 lee el desfase, no decide A-28 (ADR-0082 §10). El grabador de ticks y spread (F17) no entra. Y el CSV de la ejecución 2 de MedirDemoFTMO no entra en esta rama: se queda en data/demo_ftmo/, fuera de git, y lo congela, junto con el de la ejecución 3 (después del 1 de noviembre), una sola rama posterior, que es la que decide A-28 con los dos; la línea para A.1 va en el punto 6.
>
> 3. Lo que NO cambia
> - El motor, la spec, parametros.yaml, ambiguedades.yaml, knowledge/cases y el holdout. La rama no lee velas, ticks ni material del trader; si alguna prueba lo necesitara, PARADA.
> - tools/mql5/MedirDemoFTMO.mq5, scripts/leer_demo_ftmo.py y data/manifests/.
> - Las guardias, .claude/, .gitattributes y el Makefile. Si algo obliga a tocar el Makefile o .gitattributes, PARADA: con el Makefile cambiado la guardia niega todo make a la sesión, y esos make check los lanzo yo con «!».
> - PROJECT_STATE, salvo lo que haga el ritual (verifica su tamaño; el tope del test es 25 KB).
> - Si el clasificador o la guardia niegan un comando (el .exe de MetaEditor o del terminal incluidos), no cambies de vía ni lo reescribas: PARADA, y lo lanzo yo con «!».
>
> 4. Fase 0 (inventario y medida, sin escribir MQL5 de la capa) y PARADA
> a. Compilar. En mi máquina: dónde están el terminal de MT5 de FTMO y metaeditor64.exe; los parámetros de compilación por línea de órdenes, de la documentación oficial (cítala); si compila desde la carpeta del repo con su ruta de includes o hay que copiar a la carpeta de datos del terminal, y cómo, sin dejar copias que se desincronicen; dónde deja el .ex5 y el log, y en qué codificación; y qué código de salida y qué log da con 0 errores y con un error provocado a propósito. Mídelo con una copia de MedirDemoFTMO.mq5 fuera del repo, sin tocar el original.
> b. Probar. Qué se puede ejecutar y desde dónde: (1) un script de pruebas de MQL5 en el terminal, y si corre sin conexión; (2) el Strategy Tester por línea de órdenes (cítalo de la documentación): si un EA corre allí, qué devuelve ACCOUNT_TRADE_MODE en el tester (la negativa de D2a podría impedirlo: dilo, no lo cambies), si SymbolInfoSessionTrade responde, y si el servidor de la demo de FTMO da ticks reales de EURUSD al tester (ADR-0082 §4 deja a R6a.1 esa medida); (3) la demo. Si la prueba actual ya no deja conectar, dilo y deja (2) y (3) para la del 26.
> c. Los bytes: cómo abre MedirDemoFTMO su CSV (hacia :809, FILE_TXT|FILE_ANSI) y por qué el fichero salió con LF; con qué modo de apertura escribe MQL5 UTF-8 sin BOM y LF (documentación oficial y, si se puede, una prueba en el terminal con un fichero de prueba fuera del repo).
> d. El VPS sin puente (ADR-0082 §4: lo mide R6a.1): lo que digan el repo y las páginas oficiales de FTMO sobre correr un EA en un VPS, con la cita. No se decide nada; si hace falta preguntar a FTMO, va como línea para A.2 (la de las preguntas a FTMO, HER:27).
> e. Inventario, con fichero:línea: MedirDemoFTMO.mq5 (la negativa, MedirReloj, cómo escribe y si usa FileFlush); scripts/leer_demo_ftmo.py; mql5/ y sus README; src/botsito/mql5bridge/ y su sitio en import-linter (pyproject.toml); A-28 y los parámetros del reloj del servidor de knowledge/spec/parametros.yaml con su estado; ADR-0068 §4; la condición 2 de RENOVAR-CIERRES.md; las filas de MASTER_PLAN §H y §H.2 que cita D3; y si la guardia deja escribir .mq5 y .mqh en mql5/ (esta es la primera rama que lo hace).
> f. Las propuestas: la ruta de compilación y la de pruebas (con D4), el formato del journal campo a campo y la fórmula del hash (D3), los nombres de los ficheros (D1) y el procedimiento de D5.
> PARADA siempre al final de la fase 0: entrega a-f en el informe y espera mi respuesta.
>
> 5. Fases (tras mi respuesta)
> Fase 1 · Tests primero: los estáticos de D4 (1) y el validador del journal con su golden, cada uno roto a propósito en los dos sentidos. make check sellado.
> Fase 2 · El EA, el script de pruebas, el documento del formato y el procedimiento de D5. Compilación con su log en los anexos; el script de pruebas, ejecutado (las pruebas dinámicas de D4 (2), con sus roturas a propósito), y su salida comparada con el golden. make check sellado.
> Fase 3 · Mi corrida en la demo (D5). El journal copiado, validado con el lector y congelado en los anexos (D3). El informe dice lo que se leyó: el desfase, el modo de margen, las sesiones del símbolo, el cambio de día y si el journal sobrevivió al reinicio con la cadena entera.
> En cada make check, copia al informe la línea PICO DE MEMORIA de make-check.log. Si test_nunca_bloquea_y_es_rapido falla por tiempo, no lo arregles ni lo repitas en bucle: córrelo suelto una vez, apunta los dos tiempos en el informe y prepara una línea para G.
>
> 6. El informe
> Lleva:
> - el encargo frente a lo hecho, punto por punto, y las desviaciones;
> - la fase 0, las medidas, los logs y la respuesta a la PARADA;
> - lo que heredan R6a.2 a R6a.7, una línea por rama, para sus encargos (como mínimo: el campo reservado del hash para R6a.2; la ruta de compilación y de pruebas para todas; lo que el tester puede y no puede probar; las sesiones leídas para R6a.5);
> - «Líneas preparadas para el commit del contrato de la orden de cierre»:
>   · en la hoja de ruta, R6a.1 pasa a HECHA con su línea de Estado, y su «Qué es» dice que ACCOUNT_MARGIN_MODE se lee y se registra y que lo compara R6a.7; si la compilación la hace Claude Code, su «Quién» cambia; y su «Hecho cuando» dice que la negativa fuera de DEMO se prueba por los dos niveles de D4;
>   · en A.1, «la sesión congela cada CSV en su rama» pasa a decir que los dos CSV los congela una sola rama, tras la ejecución 3, con D6;
>   · en N, que la condición 2 de RENOVAR-CIERRES.md la cumple la lectura de SymbolInfoSessionTrade de R6a.1 (con el anexo del journal que lo muestra) y que R6a.5 la usa;
>   · las deudas que salgan, como líneas para Technical Debt, y la del VPS para A.2 si la hay.
>   Comprueba en memoria que test_hoja_de_ruta.py y test_project_state.py pasan con esas líneas, como simular_cierre.py de VISOR-CONSTRUCCION, y da el tamaño que quedaría de PROJECT_STATE.
>
> 7. Revisor
> El agente revisor (opus) sobre la rama, con los dos ejes de siempre: reglas y encargo. Que compruebe además que ningún .mq5 ni .mqh de la capa llama a una función de trading, que la negativa es lo primero de OnInit, que ninguna cifra de firma, bróker, instrumento ni ejecución está escrita a mano, que el journal no lleva login ni dinero, que el validador recalcula el hash sobre los bytes que fija el formato, que cada comportamiento de MT5 que el informe afirma está medido o citado de la documentación oficial, que ninguna consulta de CI se hizo con curl ni con un guion y que ningún guion nuevo escribe en el repo con rutas sacadas de __file__. Su informe va pegado al final del informe, con lo arreglado y lo declarado.
>
> 8. CI
> La rama toca rutas y plataforma (mql5/, src/): push como fix/ea-conexion y CI de Linux, con su run en el informe.
>
> Rama lista para revisión, NO cerrada.
