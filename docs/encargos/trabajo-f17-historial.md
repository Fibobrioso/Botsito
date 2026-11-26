# Encargo · trabajo/f17-historial

Dado por Aleks (consultor) el 2026-11-25, en un solo mensaje. Copiado tal cual.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> ENCARGO DEL CONSULTOR (2026-11-25) · rama `trabajo/f17-historial` · tag al cerrar: `stable/F39p-f17-historial` (verifica con `abrir-rama`, contra origin, que el último tag es F39o)
>
> Antes de nada, revisa /model (Opus 5.5, alto).
>
> ## 0. Base y apertura
>
> - Base: `main` en `2dc4f7dd` (commit de estado del cierre de F39o; el merge `96b250fd` lleva el tag `stable/F39o-contraste-trader`; CI de main 45747377112 en verde según ese cierre), sin ninguna otra rama. Verifícalo con la skill `abrir-rama`; si algo no cuadra, PARA y dilo.
> - Abre con `/abrir-rama trabajo/f17-historial`: encargo copiado tal cual en `docs/encargos/trabajo-f17-historial.md`, `contrato.yaml` y el Archivo en HISTORIA. Tramo del contrato: R4 (es R4.7; la A.5 de la hoja se cita en el informe). Ningún ADR nuevo: el bloque ids-inexistentes no declara ninguno. Lista blanca (y cada ruta, fuera de `rutas_protegidas` si lo estaba): este encargo, `contrato.yaml`, `tools/mql5/ExportarTicksFTMO.mq5` y `tools/mql5/README.md`, el lector nuevo en `scripts/` y `scripts/README.md`, `src/botsito/mql5bridge/compilar.py`, `src/botsito/cases/criterio_fidelidad.py`, los tests nuevos y los que D5 y D6 adaptan, `docs/plan/F17-HISTORIAL.yaml`, `data/manifests/README.md`, `docs/runbooks/F17-HISTORIAL.md`, el ADR-0090 (solo el recuadro de D7), `docs/validation/F17-HISTORIAL.md` y sus anexos, y `docs/validation/HOLDOUT-EXPOSICIONES.md`.
> - Lecciones que aplican: la fila de HOLDOUT-EXPOSICIONES del día va ANTES del primer `make check` del día (también si no lees nada protegido: lo dice la fila); toda frase «la herramienta X da Y» se mide o se cita antes de escribirla (y ADR-0082 D7: ningún comportamiento de MT5 entra como hecho sin medirlo o citarlo); para insertar texto en un documento, Edit; un guion que escribe se ensaya antes en un clon desechable; con un `make check` corriendo no se programa nada que escriba en `.claude/`; si la guardia niega compilar MQL5 o un guion nuevo, no la rodees: lo dices, el consultor revisa el diff y Aleks lo lanza con «!».
>
> ## 1. Objetivo
>
> F17 rediseñado (ADR-0099 §5) se parte en dos ramas, y esta es la primera, la que ADR-0099 §5 pone «antes que nada»: dejar listo, probado y compilado lo que mide **el historial de ticks que el servidor de la demo de FTMO ya guarda**, para que en una prueba gratuita (que Aleks activará después, en otra rama) solo haya que ejecutar, congelar y leer. Y, en la misma rama, lo que Technical Debt de PROJECT_STATE (:100) pide antes de usar F17: `curva_con_deslizamiento` y `veredicto_con_f17` por cuenta.
>
> El grabador de ticks y la medida de las órdenes stop van en la segunda rama, con su propio encargo, que se escribe con lo que deje esta (si el historial cubre los meses de construcción, el spread de FTMO sale de ahí sin esperar al grabador, ADR-0099 §5).
>
> ## 2. Qué NO cambia
>
> Motor, simulador y `knowledge/simulador/llenado.yaml` (`deslizamiento_fijo_puntos` sigue en 0), spec, casos, evidencia, feedback, corpus, `data/` (salvo temporales de los tests), la capa de MT5 en `mql5/` (ADR-0082; no envía órdenes, `tests/contract/test_capa_mt5.py`), `tools/mql5/MedirDemoFTMO.mq5` (se reutiliza su patrón, no se edita), `data/manifests/demo_ftmo/` y `tests/unit/test_manifiestos_demo_ftmo.py` (exige exactamente las ejecuciones 1, 2 y 3), la regla de ADR-0092 §4 (mediana y percentil 90) y las cifras de `criterio_fidelidad.yaml`, PREMISA-COSTES.yaml y PUENTE-TECHO.yaml. Nada se conecta a FTMO, no se activa ninguna prueba y no se envía ninguna orden. Ningún ADR cambia salvo el recuadro de D7.
>
> ## 3. Fase 0 (inventario, sin escribir código; PARADA al final)
>
> - 0.1 La fila de HOLDOUT del día, antes del primer `make check`. Declara también lo único que el proyecto ha visto ya del historial de FTMO: el recuento de ticks de un día de EA-CONEXION.md:141-145 (solo un recuento, ningún precio), para que conste antes de fijar D3.
> - 0.2 Lee y resume con fichero:línea: `tools/mql5/MedirDemoFTMO.mq5` (`Comprobaciones`, :757-791, con la negativa fuera de DEMO en :759; CSV en `MQL5/Files`), `tests/contract/test_medir_demo_ftmo.py`, `scripts/leer_demo_ftmo.py` y su test, `docs/runbooks/DEMO-FTMO.md`, `data/manifests/README.md` (el esquema `schema_demo_ftmo`), `scripts/ticks_spread.py` y `scripts/ticks_integridad.py` (la rejilla y la tolerancia de 2 puntos), `src/botsito/engine/arnes.py` (`dias_de_mercado`, :184), los parámetros del reloj del servidor (`broker_offset_base` y `broker_dst`, `knowledge/spec/parametros.yaml` hacia :140-180; A-28; ADR-0090 §1), `src/botsito/mql5bridge/compilar.py` y su test, ADR-0069 §1-§2 y su NOTA del 2026-10-13, ADR-0092 §4 y §8 (y su NOTA sobre la cuenta arrastrada de §5), ADR-0099 §5, `criterio_fidelidad.py` (`CuentaDelTramo`, `medir_por_cuentas`, `medir_rentabilidad`, `curva_con_deslizamiento`, `veredicto_con_f17`) y CUENTA-POR-MES.md (fase 0 e) 8).
> - 0.3 El auditor `auditor-encargo`, contra este encargo.
>
> ## 4. PARADA
>
> Entrega lo de 0.2; el diseño del exportador, del lector y del manifiesto (D1, D2, D4), con las columnas de cada CSV; el borrador del yaml de D3; el diseño del arreglo de D5 con su test; cómo queda la compilación (D6); y lo que proponga el auditor. Espera la respuesta del consultor. Lo que cuadre con D1 a D8 puedes empezarlo; lo que no, espera.
>
> ## 5. Decisiones dadas por adelantado
>
> - D1. **`tools/mql5/ExportarTicksFTMO.mq5`, script de solo lectura**, con su contrato en `tests/contract/` como el de `MedirDemoFTMO`: nunca envía una orden (el contrato lo comprueba en el texto, como `test_capa_mt5`); se niega fuera de una cuenta DEMO con la misma condición que `MedirDemoFTMO.mq5:759`; solo EURUSD. Exporta, por día, con `CopyTicksRange` sobre el terminal (no el tester), los ticks (instante en milisegundos, bid, ask y banderas) y la M1 del propio servidor (`CopyRates`), a CSV en `MQL5/Files`, más el primer tick disponible del símbolo (hasta dónde llegan hacia atrás, ADR-0099 §5). **Solo exporta días de los meses de construcción** (`construccion` de `criterio_fidelidad.yaml`): la lista va en el `.mq5` como constante y un test comprueba que es la del yaml; cualquier otro mes, se niega sin pedir nada (heredado 6: febrero no se toca ni se descarga). Al empezar escribe, como control, `TimeTradeServer()` y `TimeGMT()` del momento (MASTER_PLAN:258, «desfase servidor-UTC registrado»). Lo que el `.mq5` da por supuesto de MT5 (que `CopyTicksRange` devuelve los ticks guardados y no fabricados, cuántos devuelve por llamada, cómo se pide un día entero) se cita de la documentación de MQL5 o queda como «por medir en la corrida» (ADR-0082 D7); el lector lo comprueba con el punto (c) de D3.
> - D2. **El lector, en `scripts/`**, con tests sintéticos que rompen a propósito: pasa el instante del servidor a UTC con `broker_offset_base` y `broker_dst` del registro, sin ninguna cifra en el código (test a los dos lados del cambio de hora de Europa y de EE. UU.), y compara el control de D1 con lo que dice el registro; se niega a un mes que no sea de construcción; calcula, por mes, los tres puntos de D3 con la rejilla y las horas de la ventana de `ticks_spread.py` y la tolerancia de `ticks_integridad.py`, y da el veredicto «cubre» o «no cubre»; y, solo para los meses que cubren, el spread de FTMO por hora de la ventana (percentiles como `ticks_spread.py`) y la **diferencia mediana con el de Dukascopy** en las horas de la ventana, el número que ADR-0099 §5 usa para elegir la fila `spread_menos_1` o `spread_menos_2` del puente (lo da como diagnóstico, sin elegir). Imprime recuentos, puntos y percentiles; ningún precio de una operación.
> - D3. **El criterio del historial, escrito antes de ver un tick de FTMO**, en `docs/plan/F17-HISTORIAL.yaml`, fijado por su sha256 con un test que rompe a propósito, como `PREMISA-COSTES.yaml` (aquí sin ADR propio: ADR-0099 §5 ya decide que se escribe antes, y el yaml lo cita). Propuesta del consultor, que Aleks aprueba al pegar este encargo: un mes de construcción CUBRE si, en los minutos de la ventana (de `ventana_inicio` a `ventana_fin`, por la rejilla H4) de sus días de mercado (`arnes.dias_de_mercado`): (a) al menos el 99 % de esos minutos tienen al menos un tick; (b) como mucho hay 3 huecos sin ticks de más de 5 minutos en todo el mes, y ninguno de más de 30 minutos; y (c) al menos el 99 % de las M1 con ticks cuadran con la M1 BID del propio servidor con |ΔO|, |ΔH|, |ΔL| y |ΔC| ≤ 2 puntos (la tolerancia que `scripts/ticks_integridad.py` fijó para Dukascopy; contra la M1 del mismo servidor es holgada, y el yaml lo dice). Si no cubre, ese mes queda para el grabador. Que un mes cubra no autoriza a usar esos ticks como fuente de una medida: eso pide un ADR que enmiende ADR-0005 y ADR-0024 (punto 4 de su decisión), como dice ADR-0099 §5, y no es de esta rama.
> - D4. **El manifiesto**: el historial de FTMO no va en `data/manifests/demo_ftmo/`: va en una carpeta propia, `data/manifests/f17/`, con su esquema escrito en `data/manifests/README.md` (sha256 de cada CSV, días, primer tick disponible y el control de D1) y su test; esta rama solo lo define y lo prueba con un manifiesto sintético en un temporal. Y el runbook de la corrida, `docs/runbooks/F17-HISTORIAL.md`, con la forma de `DEMO-FTMO.md`: qué se compila, dónde se copia, qué días se piden, cómo se congela y cómo se lee.
> - D5. **El arreglo por cuenta** de `curva_con_deslizamiento` y `veredicto_con_f17`: las cuentas son las que dé la corrida (`CuentaDelTramo`), no «un mes»: en construcción, una por mes (ADR-0092 §8); en los meses no vistos de ADR-0092 §5, una sola arrastrada en todo el tramo. Cada cuenta recompone su curva sin arrastrar el ajuste de otra, y `veredicto_con_f17` evalúa por `medir_por_cuentas`, para que f) siga diciendo qué cuenta falla. Tests: dos cuentas (el ajuste de la primera no baja el saldo al corte de la segunda) y una cuenta arrastrada de varios meses (el ajuste sí se arrastra). Que el test nuevo rompa en `main` será por la firma de la función: dilo así, y añade uno de contenido que rompa en `main` con la firma de hoy si se puede (skill `comparar-con-main`). Los tests de hoy de `test_metodo_adr0092.py` se adaptan y el informe dice cómo. La regla de ADR-0092 §4 no cambia, y la línea :100 de Technical Debt sale en el cierre.
> - D6. **La compilación**: `compilar.py` hoy solo exporta `mql5/` e instala en Experts o Scripts. Se amplía con un camino aparte para una herramienta de `tools/mql5`, sin cambiar el de la capa (sus tests pasan igual), con tests en los dos sentidos; `ExportarTicksFTMO.mq5` y, como control, `MedirDemoFTMO.mq5` compilan sin errores ni avisos y sus logs van a `docs/validation/anexos/F17-HISTORIAL/`. El `.ex5` no se versiona.
> - D7. **Los textos**: `tools/mql5/README.md` y `scripts/README.md` (:85) nombran lo nuevo; un recuadro en ADR-0090 §7 (que dice que el spread «lo mide el grabador de spread y ticks de F17»), en su propio commit y con el cuerpo intacto, remite a ADR-0099 §5.
> - D8. **CI de Linux**: la rama toca `src/` y la ruta de compilación, así que antes de declararla lista se empuja como `fix/f17-historial` (RITUAL.md, «Una rama `trabajo/*` no dispara la CI») y pasa la CI, con el único fallo esperado de `state check`. Dame el número del run.
>
> ## 6. Para el cierre, en el informe
>
> Las líneas propuestas para la orden de cierre, con su efecto en bytes:
> - la F de la Next Action y la A.5 de la hoja: el historial de F17, con herramientas y sin correr;
> - los textos que hoy llaman «grabador» a todo F17 (el heredado 10 de PROJECT_STATE, la A.1 y el «Hecho cuando» de la A.5 de la hoja, y la fila F:F17 de su tabla), con la corrección. La fila de F17 de MASTER_PLAN NO se toca (su NOTA del 2026-11-24 lo dice);
> - PROJECT_STATE está en 24.854 bytes de 25.000: propón qué recortar con los criterios (a)-(e) de `docs/state/README.md`, que valen para los heredados, Technical Debt y las Reglas vivas, para que el cierre deje al menos 1.000 bytes de margen (la salida de la línea :100 por D5 cuenta).
>
> ## 7. Informe y entrega
>
> - `docs/validation/F17-HISTORIAL.md`: la fase 0, la PARADA y su respuesta tal cual, lo hecho por fase con su evidencia, el encargo punto por punto, las desviaciones, las líneas de §6 y la fila de ERRORES-RECURRENTES preparada.
> - El subagente `revisor`, con estos alcances: que el exportador no puede enviar órdenes ni pedir un mes fuera de construcción; el paso del reloj del servidor a UTC y su test a los dos lados de los cambios de hora; que D3 se escribió antes de cualquier dato de FTMO y está fijado por su sha256; que el lector se niega a meses que no son de construcción; el arreglo de D5 con la cuenta arrastrada; que el camino de compilación de la capa no cambia; y diff vacío en lo de §2. Su informe, pegado al final del de la rama.
> - Termina con: «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA (2026-11-26), copiada tal cual

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA de `trabajo/f17-historial` (2026-11-26, 00:15, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA. Lo que cuadre con lo medido, adelante sin esperar; si algo de lo medido contradice esta respuesta, PARA solo en eso.
>
> Veredicto: la fase 0 cumple y corrige al encargo en tres puntos que acepto. Errores del consultor, para la fila de ERRORES: (1) D3 (c) decía que detectaba ticks fabricados, y no puede, porque cuadran con la M1 por construcción; (2) D7 atribuía a ADR-0090 §7 el spread, y lo que atribuye al grabador es el deslizamiento; (3) D1 pedía «el primer tick disponible», que obliga a preguntar por meses fuera de construcción; (4) D3 tomó `arnes.dias_de_mercado` de una auditoría sin comprobar qué devuelve.
>
> D1, el exportador: no exige trading algorítmico ni mercado abierto (no opera), y aplicas el test más estricto de la capa (ninguna función de trading). De acuerdo.
>
> 0. Los días de D3: de acuerdo. Son los laborables (lunes a viernes) de cada mes de construcción menos los días con algún cierre del calendario de cierres de FTMO (ADR-0068) que toque la ventana. Si el calendario del repo no cubre algún día de enero, abril, julio o agosto de 2026, PARA y dilo; no lo completes de fuera. Nada lee la M1 de marzo ni de junio.
>
> 1. La profundidad: de acuerdo. El primer tick de cada mes pedido, buscado dentro de ese mismo mes, y la primera M1 del servidor por `SeriesInfoInteger`, como metadato. Ningún tick fuera de construcción. D1 se corrige así en el informe.
>
> 2. El discriminador (d), fijado ahora y antes de ver un tick de FTMO. Un mes CUBRE solo si además, en la ventana de sus días (punto 0): (d1) en al menos el 95 % de las horas día-hora, el spread (ASK − BID) toma al menos 3 valores distintos; y (d2) la mediana de ticks por minuto es al menos la mitad de la de los ticks de Dukascopy del mismo mes en la misma ventana. El yaml lo dice tal cual: es una heurística pre-registrada, no una prueba de que los ticks sean guardados (ADR-0082 D7). Control en esta rama: corres (d1) sobre los ticks de Dukascopy de los meses de construcción que ya están en `data/` (los que lee `ticks_spread.py`), y tienen que pasarlo todos (el (d2) de Dukascopy contra sí mismo es trivial y no se corre). Declara esa lectura en HOLDOUT el mismo día, solo con recuentos. Si algún mes de Dukascopy no pasa (d1), PARA: no cambies la cifra.
>
> 3. La diferencia de spreads: la del texto de ADR-0099 §5, «la diferencia mediana»: por cada par día-hora de la ventana con ticks de las dos fuentes, la mediana del spread de FTMO menos la mediana del de Dukascopy, y la mediana de esas diferencias. Es la que se compara con las filas `spread_menos_1` y `spread_menos_2` del puente. La diferencia de las dos medianas globales sale al lado, como dato y sin uso. Va al yaml.
>
> 4. El recuadro de D7: de acuerdo con tu texto. Por ADR-0099 §5, el deslizamiento lo mide la medida de las órdenes stop (segunda rama de F17), y el spread sale del historial, si cubre, o del grabador.
>
> 5. D5: de acuerdo con no tocar `CuentaDelTramo` ni `cableado.py`, con una condición: `curva_con_deslizamiento` y `veredicto_con_f17` agrupan por la etiqueta de cuenta que reciben y nunca la derivan de la fecha. Tests: dos cuentas con etiquetas distintas (el ajuste de una no baja el saldo al corte de la otra) y una sola etiqueta que abarca días de varios meses (el ajuste sí se arrastra dentro de ella), aunque la cuenta arrastrada de ADR-0092 §5 todavía no la construya el motor. Que rompe en `main` por la firma, dicho así. El informe dice que el constructor de la cuenta arrastrada falta y es de la rama que mida §5.
>
> 6. V02, las aperturas H4 del servidor: fuera de esta rama, de acuerdo. Una línea para R6a.8 en las propuestas del cierre.
>
> 7. El contrato gana `docs/runbooks/README.md`, `docs/adr/README.md` y `.gitignore`, este solo con una línea concreta para el `.ex5` de `tools/mql5` (nada más amplio), y comprueba que `test_no_unexpected_ignored_paths` sigue verde.
>
> D6, la compilación: cuando `compilar.py` y `ExportarTicksFTMO.mq5` estén escritos y sellados, pon en el informe su diff (el `--stat` y las funciones nuevas de `compilar.py` enteras) y PARA. El consultor lo revisa y entonces Aleks lanza la compilación con «!» con el comando exacto que le des. Los logs, a los anexos.
>
> Lo demás de D3 queda como en el encargo: (a) 99 % de los minutos con ticks; (b) como mucho 3 huecos de más de 5 minutos al mes y ninguno de más de 30; (c) 99 % de M1 cuadran a ≤ 2 puntos, ahora descrito como coherencia y no como detector. Escribe el yaml con 0 a 3 y fíjalo por su sha256 antes de cualquier otra cosa que lea ticks.

## Respuesta del consultor a la PARADA 2 (2026-11-26), copiada tal cual

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA 2 de `trabajo/f17-historial` (2026-11-26, 03:15, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA 2.
>
> 0. (d2) compara los minutos de las horas día-hora de la ventana que Dukascopy tiene descargadas en sus manifiestos de ticks de ese mes (opción a). Sobre ese mismo conjunto de minutos, un minuto sin ticks cuenta como 0 en cada fuente, y las dos medianas de ticks por minuto se calculan sobre él. Las horas que Dukascopy no tiene descargadas no entran en (d2): ni cuentan como 0 ni se comparan. El resto de D3 no cambia; (a), (b), (c) y (d1) siguen sobre todos los minutos de la ventana de los días del punto 0. La diferencia mediana de los spreads, como estaba.
>
> 1. El yaml cambia, a la vista: en un commit propio, una frase en el bloque `d2_ticks_por_minuto` con la definición del punto 0 y su sha256 nuevo en el test. El informe lo declara como desviación con su motivo: el cambio sale de los recuentos de horas de los manifiestos de Dukascopy y del control (d1), no de ningún dato de FTMO, que nadie ha visto, y la cifra (la mitad) no se mueve. Ensaya (d2) con la definición nueva sobre un caso sintético que rompa a propósito: unas horas con ticks densos en Dukascopy y escasos en FTMO, que tienen que dar «no cubre».
>
> 2. La compilación de D6 se lanzó antes de que el consultor revisara el diff, que era lo que pedía la respuesta a la PARADA 1. Declárala como desviación (solo compiló y el exportador es de solo lectura) y deja en el informe el diff de `compilar.py` (`--stat` y las funciones nuevas enteras) y el del `.mq5`, para la revisión final.
>
> Después, sigue con lo que tenías: el recuadro de ADR-0090 §7, las líneas del cierre, la CI por `fix/f17-historial` y el revisor, hasta «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA 3 (2026-11-26), copiada tal cual

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA 3 de `trabajo/f17-historial` (2026-11-26, 07:40, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA 3.
>
> Revisión de la compilación: el consultor leyó en `fix/f17-historial` (958ffec3) el diff de `compilar.py` (el camino `herramienta`: solo un `.mq5` directamente bajo `tools/mql5/` y en el índice, compilado en una copia temporal del índice, sin cambiar `exportar` ni `instalar`) y `ExportarTicksFTMO.mq5` 1.01 (ninguna función de trading; DEMO y rango de construcción comprobados antes de pedir nada; solo escribe en `MQL5/Files`; b1 normaliza las dos fechas al inicio del día). Aprobado: Aleks recompiló con «!» después de esta revisión. Commitea los logs nuevos de los anexos con su `make check`.
>
> 0. Las horas de otro mes en los días de los bordes (a1): de acuerdo con tu recomendación. El exportador sigue pidiendo días del servidor. El lector pasa cada tick y cada M1 a UTC y descarta, sin usarlo para nada, todo lo que cae fuera del mes UTC pedido; lo cuenta en su salida, por mes vecino y en número de filas, y la fila de HOLDOUT del día de la corrida lo declara por recuento. Son precios fuera de la ventana: ADR-0021 §1 no los trata como holdout, y ningún día de febrero queda nunca en el borde de un mes de construcción. Test sintético que rompe a propósito: un tick de la última hora UTC del mes anterior en el fichero del día 1 no entra en ninguna cuenta y sí en el recuento de descartes. Corrige en el informe la frase de la respuesta a la PARADA 1 «Nada lee la M1 de marzo ni de junio» con lo que pasa de verdad: el exportador las baja en esas horas de borde y el lector las descarta sin leerlas para nada.
>
> 1. La regla de elección de fila del yaml (b2): se queda. Es copia literal de ADR-0099 §5, el yaml lo dice con su cita y el lector no elige nada. Declárala en el informe. El yaml no cambia más.
>
> Para el cierre: de acuerdo con que el heredado 10 salga por (b) y con una F corta, con el margen en 833 bytes. Doy por bueno no llegar a 1.000 porque a2 exige conservar las citas; deja los textos a la letra en §12.
>
> Después: la CI de `fix/f17-historial` sobre el último commit (el número del run, con el único fallo esperado de `state check`), el revisor solo sobre lo que cambie desde 958ffec3, y termina con «Rama lista para revisión, NO cerrada.»
