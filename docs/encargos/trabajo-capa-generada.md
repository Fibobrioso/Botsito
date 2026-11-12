# Encargo · trabajo/capa-generada

Dado por Aleks (consultor) el 2026-11-12, en un solo mensaje. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/capa-generada (hoja de ruta R6a.2, tramo R6a; ADR-0082 D5). Encargo del consultor, 2026-11-12.
>
> 0. Apertura
> - Base: main en 893ce6f, el commit de estado de stable/F38y-laminas-motivos. Verifica con git main, origin/main y el tag, que no hay otra rama abierta (git branch --list solo da main) y, con gh, que la CI de main de ese commit está en verde (run 43217308040). Si el clasificador niega gh, PARADA y la consulto yo con «!».
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R6a.
> - Informe: docs/validation/CAPA-GENERADA.md. Anexos: docs/validation/anexos/CAPA-GENERADA/. En rutas_permitidas, además: mql5/, src/botsito/mql5bridge/, tests/ (con tests/golden/), docs/runbooks/DEMO-FTMO.md y docs/runbooks/RENOVAR-CIERRES.md.
> - No espero ningún ADR: las decisiones van al informe y a mql5/JOURNAL.md. Si al final hiciera falta uno, su id va en el bloque ids-inexistentes del encargo antes del primer make check (lección de F38o).
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0; entregar-rama al final.
> - Revisa /model antes de empezar: Opus en esfuerzo alto.
>
> 1. Objetivo, y por qué va ahora
> Que lo que la capa de MT5 recibe del repo le llegue generado, sin ninguna cifra a mano y con su propio hash en el journal (ADR-0082 D5; hoja de ruta R6a.2, «Hecho cuando: regenerar no da diff y el hash está en el journal»). No envía, no modifica y no cancela ninguna orden.
> Por qué ahora: va en el hueco hasta la sesión 7a (ADR-0082 D8: no le quita turno a F); RUMBO-2026-11.md §6 pide dos ramas de fidelidad por cada una de infraestructura, y las cinco últimas (F38u a F38y) han sido de fidelidad; y R6a.3, R6a.4, R6a.5 y R6a.6 dependen de ella.
> Tiene que estar cerrada antes de la ingesta de la 7a, porque solo cabe una rama abierta (abrir-rama). Si te digo que ya tengo la grabación de la 7a y la rama no está para cerrar, PARADA y decido yo.
>
> 2. Decisiones del consultor (2026-11-12; las tomo antes de medir. Si la fase 0 encuentra un hecho que las contradiga —un ADR, una regla, la documentación oficial de MQL5 o lo que mida en MT5—, PARADA)
> D1. Qué entra: la condición de ADR-0082 D3 (§3), que niega por defecto. Un parámetro entra en lo generado si no es de categoría estrategia ni es un hecho de la estrategia, y lo lee una pieza de R6a.3 a R6a.8 según su «Qué es» en la hoja de ruta (el pre-vuelo de R6a.7 compara el instrumento y el perfil con SymbolInfo y AccountInfo). Que una regla de la spec lea también el parámetro no lo saca: D3 nombra como entradas de la capa los parámetros de firma, bróker, instrumento y ejecución y el perfil, y por ejemplo reloj_dia_riesgo (RN-029 y RN-030, veto de la firma de R6a.4) o instrumento_lote_minimo, instrumento_lote_paso e instrumento_contrato (R6a.6) los necesita la capa. Quedan fuera, aunque sean de categoría ejecucion, los que son de la estrategia (huso_grafico, sesgo_h4_tope_velas, caja_se_fija, reloj_sesiones, sesiones_primera_vela_h4) y los del simulador (modelo_llenado, latencia_ms): verifícalo con sus consumido_por. Dudosos, que decido yo en la PARADA: huso_operativa (hora de la operativa del trader y reloj del día de riesgo) y cierre_pendientes (política del bróker simulado, DEFAULT_AMBIGUOUS bajo A-55). Un parámetro sin valor (UNKNOWN) no se genera; si una pieza lo necesitara, PARADA. El estado de cada parámetro viaja con su valor: un DEFAULT_AMBIGUOUS no puede leerse como CONFIRMED.
> D2. Una fuente por nombre. Un nombre que esté en knowledge/spec/parametros.yaml y en knowledge/cuentas/ftmo-2step-swing-100k.yaml sale una sola vez, y el generador falla si su tipo, valor, opciones o estado difieren: no elige. El test que hoy los cruza (verifica que es tests/unit/test_perfil_cuenta.py, hacia :106, y que no compara el estado) se amplía al estado. Los sinónimos con nombre distinto (verifica instrumento_stops_level frente a firma_stops_level_puntos, y huso_operativa frente a firma_huso_corte, que cruza otro test del mismo fichero) van en la tabla de la fase 0: de cada pareja sale un solo nombre, el que yo decida, y el generador falla si sus valores difieren.
> D3. El calendario de cierres, tal como está: knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml con su `cubre` (verifica que acaba el 2026-10-07). Esta rama no lo renueva (RENOVAR-CIERRES.md, «Quién, y en qué rama»: la renovación va en su rama propia) ni amplía `cubre`. Lo generado lleva `cubre`, para que R6a.5 niegue fuera de él como el predicado (cierre_sin_calendario). Propón en la fase 0 la forma (instantes o la pauta con sus extraordinarios), usando lo que ya existe en src/botsito/engine/calendario_cierres.py sin portar lógica que decida: portar cierres_desde_sesiones y unir_cierres (src/botsito/domain/cierres.py) es de R6a.5. La corrida de la fase 3 cae fuera de `cubre`: no importa para esta rama, que no opera, y el informe lo dice. Desde esta rama, quien cambie lo generado (renovar el calendario, una activación que toque los parámetros que entran, el perfil) tiene que regenerar: escribe en esta rama esa línea en docs/runbooks/RENOVAR-CIERRES.md (va en rutas_permitidas) y prepara una línea de Technical Debt para la skill activar-sesion, porque .claude/ no se toca aquí.
> D4. Dónde y cómo. Un solo fichero generado bajo mql5/Include/Botsito/Capa/, con una cabecera que diga que se genera y con qué orden. El nombre lo propones, y no es Params.mqh ni Risk.mqh: MASTER_PLAN.md §H.2 (hacia :270) los deja para F28, Params.mqh con estrategia, instrumento y ejecución y Risk.mqh con prop_firm, y su §H (hacia :238) pone en Params.mqh el hash de la spec; ADR-0082 §6 lo cita. El informe dice además que lo de la capa se genera también desde knowledge/cuentas/, no solo desde knowledge/spec/ como dicen mql5/README.md y ADR-0001 (no se corrigen aquí: línea para el cierre si hace falta). El generador va en src/botsito/mql5bridge/ (verifica en pyproject.toml que import-linter deja a mql5bridge leer config, spec y engine), se lanza por su ruta (python -m no lo ejecuta la guardia, EA-CONEXION.md §7) y se escribe en el informe exactamente como se ejecuta, con uv run y todos sus flags. El fichero generado se commitea; un test lo regenera en memoria y falla si difiere un byte, y otro rompe a propósito cambiando un valor del yaml sin regenerar. UTF-8 sin BOM y LF, como el resto de la capa (test_la_capa_es_utf8_sin_bom_y_lf).
> D5. El hash. Un solo capa_hash: SHA-256 en hexadecimal sobre el contenido canónico de lo generado, sin la línea que lleva el propio hash. La fórmula exacta la propones en la fase 0, y tiene que poder recalcularse desde el repo en un tag stable, porque R6a.7 la comparará. El generador lo escribe en el fichero; un test de Python lo recalcula por su cuenta; el EA lo escribe en el campo capa_hash del journal.
> D6. El journal, versión 2. capa_hash deja de ser null (mql5/JOURNAL.md lo tiene «reservada para R6a.2»): es la v2 del formato (EA-CONEXION.md §7, «R6a.2»), definida una vez en JOURNAL.md, con el validador de src/botsito/mql5bridge/journal.py y su golden. Los journals v1 congelados en docs/validation/anexos/EA-CONEXION/ tienen que seguir validando como v1, y hoy el lector rechaza cualquier versión que no sea la suya («este lector es de la v…»): el lector lee cada fichero por la versión que declara. No hay cadena mixta: UltimaLinea (Journal.mqh) exige la cabecera de su versión, así que un EA v2 sobre un journal v1 daría «rota»; el procedimiento de la fase 3 empieza con el journal v1 fuera de MQL5/Files (movido, no borrado) y la cadena v2 arranca con «ninguna». VERSION_EA sube. Las dos deudas de Technical Debt sobre estos ficheros (la comprobación redundante del LF en UltimaLinea y el reinicio de globales tras un cambio de símbolo) no se pagan aquí salvo que la rama toque esa lógica; si la toca, PARADA.
> D7. LATIDO_SEG y TOPE_SESIONES no se generan: son cifras del formato del journal, no de la cuenta (JOURNAL.md, «Las dos cifras del formato»; respuesta a la PARADA de R6a.1, punto 6). Cambiarlas sigue siendo una versión nueva del formato. La frase de R6a.2 en la hoja («Si se decide, también `LATIDO_SEG` y `TOPE_SESIONES`, las dos cifras del formato del journal (`mql5/JOURNAL.md`)») pasa a decir que no se generan, con este porqué (línea para el cierre).
> D8. Los tests de la capa.
>  - Lo generado son constantes const, ni #define ni variables: así no hay #define nuevos para DEFINES_PERMITIDOS (EA-CONEXION.md §7: «Los #define nuevos, a DEFINES_PERMITIDOS», y a6) y no son globales que test_el_ea_reinicia_sus_globales_en_oninit tenga que exigir (verifica que globales() no cuenta una línea que empieza por const). Si algo necesitara un #define, PARADA.
>  - El detector de cifras a mano (test_la_capa_no_lleva_cifras_ni_nombres_a_mano; hoy: decimales fuera de cadenas, los nombres de símbolos y firmas, y los #define fuera de la lista) admite decimales y esos nombres solo dentro del fichero generado y solo si ese fichero es idéntico byte a byte a lo que da el generador, comprobado por el propio detector. Es la herencia a6 de EA-CONEXION.md. Hoy el detector no prohíbe enteros (su caso bueno «int n = 32;»): esta rama no lo amplía a enteros, lo declara, y si la fase 0 ve un entero de firma, bróker o instrumento escrito a mano en la capa, PARADA.
>  - Ampliar la capa obliga a ampliar LA_CAPA, y test_la_capa_son_los_ficheros_de_r6a1 cambia de nombre porque dejará de decir la verdad; renombra igual cualquier otro test cuyo nombre deje de decir lo que comprueba.
>  - LECTURA_PERMITIDA sigue vacía: esta rama no llama a ninguna función de trading.
> D9. Compilar, probar y la demo, con la ruta de R6a.1 (EA-CONEXION.md §7, «Todas» y «El tester»): compilar.py compilar, con la puerta «Result: 0 errors» y el .ex5 (compila lo exportado del índice: el fichero generado tiene que estar estadiado antes); las pruebas con compilar.py pruebas y su script; el EA quitado de la demo y el terminal cerrado al compilar e instalar. Las pruebas gratuitas de FTMO anteriores ya terminaron (la última, el 11-nov): la corrida de cierre va en una prueba nueva que creo yo cuando me lo pidas. Avísame al llegar a la fase 3, no antes, para no gastar sus 14 días. Basta una corrida que conecte y escriba arranque, cuenta y unos latidos con capa_hash. Si el Strategy Tester con esa cuenta lo da, vale el tester, con su .ini a mano como en anexos/EA-CONEXION/tester-ea/ (compilar.py no tiene esa orden).
>
> 3. Lo que NO cambia
> - El motor, la spec, parametros.yaml, ambiguedades.yaml, el perfil, el calendario de cierres, knowledge/cases y el holdout. La rama no lee velas, ticks ni material del trader; si algo lo necesitara, PARADA.
> - tools/mql5/MedirDemoFTMO.mq5, scripts/leer_demo_ftmo.py y data/manifests/.
> - Las guardias, .claude/, .gitattributes y el Makefile. Si algo obliga a tocar el Makefile o .gitattributes, PARADA.
> - PROJECT_STATE, salvo lo que haga el ritual y «Tests Currently Passing», que actualizas con cada test nuevo (test_state_check_ok_on_real_repo lo exige; decláralo, como en ea-conexion). Está en 23.899 bytes (verifícalo; el tope del test es 25.000 bytes): si el cierre le añade algo, recorta antes con los criterios de docs/state/README.md, «Que sale de PROJECT_STATE, y con que criterio».
> - Si el clasificador o la guardia niegan un comando (los .exe incluidos), no cambies de vía ni lo reescribas: PARADA, y lo lanzo yo con «!».
>
> 4. Fase 0 (inventario y medida, sin escribir código de la capa) y PARADA
> a. La tabla de D1: cada parámetro de parametros.yaml que no sea de categoría estrategia y cada uno del perfil, con su estado, su valor, su consumido_por y las reglas que lo leen, si entra o no y por qué, y la pieza de R6a que lo lee (fichero:línea de la hoja). Lo dudoso queda fuera y marcado para mí.
> b. D2: qué nombres están en los dos ficheros, si algo difiere hoy (estado incluido), los sinónimos y el test que los cruza.
> c. D3: `cubre`, las pautas y los extraordinarios del calendario; qué ofrece engine/calendario_cierres.py sin decidir nada; la forma que propones.
> d. D4 y D5: el nombre del fichero, la orden exacta del generador, la fórmula del hash y cómo la recalcula el test.
> e. D6: cómo lee hoy journal.py la versión, qué cambia para leer v1 y v2, y qué goldens se tocan.
> f. D8: qué hacen hoy LA_CAPA, DEFINES_PERMITIDOS y el detector de cifras, con fichero:línea, y el cambio que propones, con cómo lo romperás a propósito en los dos sentidos.
> g. D9: si el Strategy Tester corre el EA sin una prueba viva. Mídelo si se puede sin crear la prueba; si no, dilo.
> h. Herencias: busca R6a.2, capa_hash, LATIDO_SEG y Params.mqh en PROJECT_STATE (Next Action y Technical Debt), HISTORIA, la hoja de ruta, EA-CONEXION.md, PLATAFORMA-ADELANTADA.md y ADR-0082. Lo que lo nombre entra o se dice por qué no.
> PARADA siempre al final de la fase 0: entrega a-h en el informe y espera mi respuesta. Si lo medido cuadra con D1-D9, mientras esperas puedes escribir los tests de la fase 1 (sin código de la capa ni del generador); con lo que no cuadre, espera.
>
> 5. Fases (tras mi respuesta)
> Fase 1 · Tests primero: regenerar sin diff, el hash recalculado, el cruce de D2, el validador v1 y v2 con sus goldens y el detector de D8, cada uno roto a propósito en los dos sentidos. make check sellado.
> Fase 2 · El generador, el fichero generado, el EA que escribe capa_hash, JOURNAL.md v2 y el procedimiento de la fase 3 en docs/runbooks/DEMO-FTMO.md, como la sección de R6a.1 y en mi lenguaje. Compilación con su log en los anexos (UTF-8, LF y el sha256 del original); el script de pruebas ejecutado, con sus roturas a propósito, y su salida comparada con el golden. make check sellado.
> Fase 3 · Mi corrida (D9): me avisas y creo la prueba. El journal copiado, validado como v2 con el lector, con capa_hash igual al del repo, y congelado en los anexos.
> En cada make check, copia al informe la línea PICO DE MEMORIA de make-check.log.
>
> 6. El informe
> - El encargo frente a lo hecho, punto por punto, y las desviaciones.
> - La fase 0, las medidas, los logs y la respuesta a la PARADA.
> - Lo que heredan R6a.3 a R6a.8, una línea por pieza: qué constantes generadas le tocan y cómo se amplía lo generado sin tocar el hash a mano.
> - «Líneas preparadas para el commit del contrato de la orden de cierre»: R6a.2 pasa a HECHA con su línea de Estado; la línea de D7; la de activar-sesion de D3; las deudas que salgan, como líneas para Technical Debt. Simula en memoria que test_hoja_de_ruta.py y test_project_state.py pasan con esas líneas y da el tamaño que quedaría de PROJECT_STATE.
>
> 7. Revisor
> El agente revisor (opus) sobre la rama, con los dos ejes de siempre: reglas y encargo. Que compruebe además: que ninguna cifra de firma, bróker, instrumento ni ejecución está escrita a mano fuera del fichero generado; que nada de lo generado es de la estrategia (D1; ADR-0082 D3); que regenerar no da diff y que un test independiente recalcula el hash; que los journals v1 siguen validando; que ningún .mq5 ni .mqh llama a una función de trading; y que cada comportamiento de MT5 que el informe afirma está medido o citado de la documentación oficial.
>
> 8. CI
> La rama toca mql5/ y src/: push como fix/capa-generada, con la forma de RITUAL.md (git push origin trabajo/capa-generada:refs/heads/fix/capa-generada), y CI de Linux con su run en el informe. El único fallo aceptado es el de state check por el nombre fix/.
>
> Rama lista para revisión, NO cerrada.

## Cambio del consultor (2026-11-12, respuesta a la PARADA de la fase 0)

Dado por Aleks (consultor) el 2026-11-12, en un solo mensaje. Copiado tal cual (el mensaje habla de «los puntos A a E»; trae A, B y C):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/capa-generada (2026-11-12). Cópiala tal cual al informe (CAPA-GENERADA.md, «Respuesta a la PARADA») y al final de docs/encargos/trabajo-capa-generada.md, bajo «Cambio del consultor» (los puntos A a E). Donde choque con el encargo, manda esto. Aplícala punto por punto.
>
> A. Cambio de calendario y de alcance (Aleks fija la sesión 7a para el domingo 15 de noviembre; su ingesta no puede abrirse con esta rama abierta).
> A1. Sin demo ni prueba nueva de FTMO: la fase 3 sale del encargo y no me pides crear ninguna prueba. «El hash está en el journal» se comprueba con el script de pruebas, que corre sin conexión (EA-CONEXION.md, hacia :100). Es una lectura mía del «Hecho cuando» de R6a.2: decláralo como desviación decidida por el consultor.
> A2. La corrida en la demo pasa a R6a.8, que ya necesita la demo una semana. Para el commit del contrato prepara: (i) la línea de R6a.8 en la hoja, que dice que su journal en la demo es v2 y comprueba que capa_hash coincide con el del repo en el tag vigente; (ii) la línea de Estado de R6a.2, que dice que el hash se comprobó con el script de pruebas y que la demo queda para R6a.8.
> A3. El procedimiento de docs/runbooks/DEMO-FTMO.md se escribe igual, para R6a.8, incluido mover el journal v1 fuera de MQL5/Files antes del primer arranque v2.
> A4. Calendario: fases 1 y 2 hoy y mañana viernes; revisor y «Rama lista para revisión, NO cerrada» el sábado 14. Si no cabe, PARADA con lo que recortarías.
> A5. Si el domingo, con la grabación hecha, la rama no está para cerrar, PARADA y decido yo; no abras nada más.
>
> B. Las nueve decisiones.
> 0. (a). Entra firma_huso_corte; huso_operativa queda fuera. El generador comprueba, como ADR-0053 §4, que los dos dan los mismos instantes en la medianoche de cada día de `cubre`, y falla si no. Por qué: es el reloj que ya usa el simulador, y reloj_dia_riesgo: civil_operativa es la medianoche en huso_operativa (ADR-0027, citado en ADR-0053 §4), así que la capa la resuelve con firma_huso_corte bajo esa misma comprobación. Línea para la hoja, en R6a.4: «reloj_dia_riesgo se resuelve con firma_huso_corte, comprobado contra huso_operativa al generar (ADR-0053 §4); cómo pasa MQL5 un nombre IANA a instantes lo decide esta rama». D2 queda corregida así: un error del consultor, para la fila de ERRORES-RECURRENTES.
> 1. (a). cierre_pendientes, fuera: qué hace la capa con una pendiente al abrir la ventana lo decide R6a.5 con A-55, y entrar entonces es regenerar.
> 2. (a). Fuera lo que no lee ninguna pieza, por la regla de D1.
> 3. (a). Sale instrumento_stops_level, y el generador falla si difiere de firma_stops_level_puntos.
> 4. (a). Los 228 instantes juntos de calendario(), en segundos UTC, con `cubre` y su fuente.
> 5. (a). Si el enum o los arrays const globales no compilan en MQL5, PARADA.
> 6. (a), con un añadido por A1. El golden v2 va con el hash fijo de prueba, como propones. Además, el script de pruebas escribe un fichero aparte, fuera de --golden (comparar_con_golden solo recorre los del golden, compilar.py:192-201), con una línea v2 escrita por JournalLinea con el CAPA_HASH real de Generado.mqh. compilar.py pruebas lo valida como v2 y comprueba que su capa_hash es igual al recalculado desde el Generado.mqh del repo; si no lo es, falla. Ese paso lleva su test en Python, roto a propósito en los dos sentidos (hash distinto y fichero ausente). La salida de la corrida va a los anexos, con su sha256.
> 7. No aplica: la demo sale de la rama (A1 y A2). No arranques el terminal con la cuenta vencida.
> 8. (a). Un solo capa_hash. Línea para el cierre: en F28, lo de prop_firm viajará también en risk_hash, y esa rama dice si capa_hash sigue.
>
> C. Lo demás de la fase 0.
> - La fila de HOLDOUT-EXPOSICIONES de la apertura y la ampliación del contrato, bien.
> - lote_si_no_cabe CONFIRMED frente a ADR-0082:53, que lo da por DEFAULT_AMBIGUOUS: déjalo en el informe como línea para el cierre; aquí no se toca el ADR.
> - El matiz de «4 de las 5 últimas ramas son de fidelidad», aceptado: la proporción de RUMBO §6 se cumple igual.
> - PROJECT_STATE:82, mql5/README.md:2 y ADR-0001:12, como líneas para el cierre, como dices.
>
> Sigue con la fase 1 (tests primero, cada uno roto a propósito en los dos sentidos, make check sellado) y la fase 2. PARADA solo si algo no cuadra con esto. Rama lista para revisión, NO cerrada.
