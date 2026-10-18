# Encargo · trabajo/plataforma-adelantada

Dado por Aleks (consultor) el 2026-10-18. Copiado tal cual (hasta que exista, el ADR que el
encargo manda escribir va declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; sale del bloque en el commit que lo crea):

```ids-inexistentes
ADR-0082 — el ADR que este encargo manda escribir en su fase 1; aún no existe
```

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/plataforma-adelantada, desde main en 8642b8c (commit de estado sobre el merge 7d3783d, tag stable/F37t-visor-construccion). Antes de abrirla, verifica con git que main está en 8642b8c, que su padre es el merge 7d3783d y que stable/F37t-visor-construccion^{commit} es 7d3783d; si no, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-plataforma-adelantada.md, su contrato.yaml y el archivo en HISTORIA del PROJECT_STATE.md de main. En el contrato: tramo «R0 · Lo que ordena el trabajo» (la rama reordena la hoja de ruta, y el tramo nuevo aún no existe al abrirla); rutas_permitidas, las de siempre más docs/adr/, docs/plan/MASTER_PLAN.md, docs/plan/HOJA-DE-RUTA.md y docs/validation/PLATAFORMA-ADELANTADA.md; rutas_protegidas: src/, tests/, mql5/, tools/, knowledge/, scripts/, .claude/ y Makefile.
>
> Objetivo, en dos partes, solo documentos: (1) escribir el ADR que adelanta antes de F26 la capa de MT5 que no depende de la estrategia, enmendar la regla «la validación de fidelidad (F26) precede a cualquier MQL5» y abrir su tramo en la hoja de ruta; (2) dejar PROJECT_STATE.md en 20.500 bytes o menos (hoy 24.391; tope del test 25.000), contando lo que entra en esta rama.
> NO cambia: motor, spec, knowledge, parámetros, guardias, hooks, Makefile, src/, tests/, mql5/ ni tools/. No se escribe ni una línea de MQL5 ni de Python. Nadie ejecuta uv run botsito motor arnes ni el visor. No se lee material del trader.
>
> DECISIONES. Las de Aleks son del 2026-10-18; las del consultor, del mismo día. Van al ADR con su autor y su fecha:
>  D1 (Aleks). SÍ se adelanta, antes de F26, la capa de MT5 que no depende de la estrategia: conexión; órdenes stop idempotentes; freno de peticiones (ADR-0067); veto antes de los cierres de mercado (ADR-0068 y SymbolInfoSessionTrade); margen (ADR-0081); reloj del servidor (A-28); journal y reconciliación; y el pre-vuelo de F33.
>  D2 (Aleks). El dominio de la estrategia en MQL5 (F29) y el harness Python-MQL5 (F30) siguen esperando a F26.
>  D3 (consultor). La frontera es una condición, y la lista de D1 son sus casos: la capa ejecuta, frena, veta, mide y registra, pero nunca decide una operación. Su prueba es que ninguna de sus entradas es un hecho de la estrategia (sesgo, liquidez, caja, zona, escenario, distancia del stop) ni un parámetro de categoría estrategia; lee solo cuenta, símbolo, sesiones del símbolo, reloj, órdenes, posiciones y los parámetros de firma, bróker y ejecución. Lo que no cumpla la condición, o deje duda, espera a F26 (niega por defecto). Tres consecuencias que el ADR escribe:
>    - La capa sabe mover un stop; cuándo se pone el break even (ADR-0065) es de la estrategia.
>    - De ADR-0081 entran el tope por margen libre y por volumen y el rechazo por margen; el lote del riesgo (RN-011, que usa riesgo_por_operacion, de categoría estrategia, y la distancia del stop) es de la estrategia. La capa recibe un lote y lo limita; no lo calcula.
>    - El veto de la firma (RN-029 a RN-032) cumple la condición, porque solo lee cuenta y registro. Entra en la capa aunque D1 no lo nombre (verifica en knowledge/spec/ qué lee cada una; si alguna lee algo de la estrategia, esa se queda fuera y se dice).
>  D4 (consultor). Dónde vive la capa NO se supone. En el repo conviven dos lecturas: el EA de MQL5 de MASTER_PLAN §A (F29-F31; F31 «EA, ordenes idempotentes, veto de riesgo, journal») y un adaptador en vivo en Python que reutiliza las mismas clases (ADR-0067 §1: «el adaptador real de MetaTrader usará la misma clase», engine/freno.py; ADR-0068 §4: el adaptador llama a cierres_desde_sesiones y unir_cierres de domain/cierres.py; ADR-0006, la capa mql5bridge; MASTER_PLAN §H.2 sobre el módulo MetaTrader5 de Python). Lo decido yo en la PARADA de la fase 0 con el inventario de b). Elija lo que elija, lo que hoy deciden ADR-0067, ADR-0068 y ADR-0081 sigue siendo la referencia, y el ADR enmienda de forma explícita los ADR cuya letra contradiga la decisión, con un recuadro en cada uno, como hizo ADR-0081 §5.
>  D5 (consultor). Ninguna cifra escrita a mano en la capa: los parámetros de firma, bróker y ejecución y el calendario de cierres (knowledge/cuentas/cierres/<perfil>.yaml) le llegan generados desde el repo, con sus hashes en el journal (MASTER_PLAN §H.2 habla de dos hashes; dilo como esté). La parte de estrategia de F28 espera a F26.
>  D6 (consultor). Hasta F35, la capa se niega a funcionar fuera de una cuenta DEMO, como tools/mql5/MedirDemoFTMO.mq5 (ACCOUNT_TRADE_MODE, hacia la línea 759; verifica y cita). Y la condición 2 de la entrada N (RENOVAR-CIERRES.md, «Antes de que el bot corra en tiempo real») se cumple al pie de la letra: la primera rama que conecta, R6a.1, trae la lectura de las sesiones del símbolo con SymbolInfoSessionTrade, y R6a.5 la usa para el veto.
>  D7 (consultor). Cómo se compila y se prueba lo que haga falta en MT5 (MetaEditor por línea de órdenes en la máquina de Aleks, el Strategy Tester o la demo) no se supone: lo mide la fase 0 de R6a.1, con PARADA. Ningún comportamiento de MT5 entra en un encargo como hecho sin medirlo en la demo o citarlo de la documentación oficial de MQL5. El formato del journal se fija en R6a.1 pensando en F34, que compara la demo con el backtest línea a línea: un solo formato, versionado.
>  D8 (Aleks). Las ramas de la capa van en los huecos de espera (del trader, de FTMO, de la demo) y no le quitan turno al camino crítico de F (hoy Y → V). La ganancia realista es de 1 a 2 meses, porque los 3 meses en sombra de F34 no se acortan: el ADR lo dice en su Impacto.
>  D9 (consultor). El orden, una rama por entrada salvo que su encargo diga otra cosa:
>    - R6a.1: conexión, reloj del servidor, sesiones del símbolo y journal.
>    - R6a.2: parámetros y calendario generados (D5).
>    - R6a.3: órdenes stop idempotentes y reconciliación.
>    - R6a.4: freno de peticiones (ADR-0067, A-54) y veto de la firma (RN-029 a RN-032).
>    - R6a.5: veto antes de los cierres de mercado (ADR-0068, A-55).
>    - R6a.6: tope por margen y volumen (ADR-0081), con la ejecución 3 de la demo, que mide cuándo comprueba MT5 el margen de una pendiente stop.
>    - R6a.7: pre-vuelo (MASTER_PLAN §H y §H.2: el hash de la spec contra el tag stable vigente, el desfase del reloj contra la tabla, ACCOUNT_MARGIN_MODE, SymbolInfo/AccountInfo contra el perfil; aborta si no cuadra).
>    Las ejecuciones 2 y 3 de la demo y A-28 siguen en el carril de Aleks (A.1): R6a.1 lee el desfase del reloj, no lo decide.
>
> FASE 0, inventario sin tocar nada. Entrégalo en el informe antes de escribir:
>  a) Cada sitio que diga que F26 va antes de cualquier MQL5, con fichero:línea. Ya sé de PROJECT_STATE.md:167, docs/plan/MASTER_PLAN.md:27 (§0), docs/plan/HOJA-DE-RUTA.md R6.1 (que lo atribuye a «§A»), docs/plan/MASTER_PLAN.html (hacia :115 y :783) y docs/research/2026-09-03-del-corpus-al-bot.html (hacia :635). Busca más con grep en CLAUDE.md, docs/runbooks/, .claude/, docs/plan/ y docs/adr/. Las instantáneas congeladas (los dos HTML), los informes cerrados y HISTORIA solo se listan, no se tocan. Si aparece uno en CLAUDE.md, docs/runbooks/ o .claude/, PARADA: está fuera del contrato.
>  b) Para D4, las dos lecturas con su cita: cada ADR, fila de MASTER_PLAN, capa de import-linter (pyproject.toml) y módulo de src/ que suponga el adaptador en Python o el EA de MQL5; qué haría falta enmendar en cada caso; y qué partes del código de hoy (engine/freno.py, domain/cierres.py, el límite del lote) se reutilizarían tal cual o habría que reescribir. Sin opinión: hechos con cita. PARADA aquí siempre: decido D4.
>  c) Las filas de MASTER_PLAN §A que toca la rama (F28, F31, F33). El cuerpo de MASTER_PLAN no se toca (su NOTA del 2026-10-10, líneas 3-8). Comprueba que una NOTA nueva arriba no rompe tests/unit/test_hoja_de_ruta.py (_funcionalidades) ni ningún otro test. No se crean números F nuevos.
>  d) PROJECT_STATE: para cada línea de «Pendientes heredados», «Technical Debt» y «Reglas vivas», su condición de salida (a/b/c/d de docs/state/README.md, «Que sale de PROJECT_STATE, y con que criterio») o «se queda», con su evidencia. Niega por defecto. La hoja de ruta no cuenta como sitio para (b): (b) admite solo la Next Action, CLAUDE.md o un runbook. Las «Candidatas a ambiguedad sin abrir» no están en el criterio y se quedan. Comprueba en particular, sin darlo por hecho: los heredados 10, 25, 30, 34 y 35 frente a las entradas A y V; las deudas en mayúsculas del 2026-09-17 al 2026-09-25, una por una; y la decisión del 2026-09-25 de «Decisions and Rationale» frente a ADR-0050. Por cada heredado que salga, su HER:n sale de la hoja de ruta en el mismo commit (test_hoja_de_ruta da «no es un heredado vivo» si se queda en una entrada no HECHA); y si sale la deuda de la copia de seguridad, A.4 deja de citarla por su texto.
>  e) La Next Action NO se edita en esta rama. Si ves texto suyo repetido entero en la hoja de ruta o en un runbook, ponlo en una tabla aparte como propuesta (entrada, texto, dónde vive, bytes); yo decido en la orden de cierre.
>  f) Bytes de cada sección de PROJECT_STATE antes y la previsión después, contando la regla nueva y el cambio de Current Branch y Current Feature. Si la previsión no baja de 21.500, dímelo en la misma PARADA con lo que más haría falta; si queda entre 20.500 y 21.500, explícalo.
>  Para en b) y espera mi respuesta.
>
> FASE 1, el ADR. docs/adr/0082-<título>.md (verifica que 0082 es el siguiente número libre), con el formato de 0000-template.md y su fila en docs/adr/README.md, con las enmiendas entre paréntesis en la columna Estado, como 0080 y 0081. Lleva D1 a D9 con su autor y fecha y la decisión de D4 de mi respuesta. El título nombra la condición de D3. Enmienda la regla de MASTER_PLAN §0 y la de PROJECT_STATE, y los ADR que diga mi respuesta a D4, cada uno con su recuadro.
>
> FASE 2, los sitios de la regla y del plan.
>  - PROJECT_STATE, «Things That Must Not Be Changed»: la línea se sustituye por «La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.» La línea vieja va a HISTORIA, literal, en un bloque «# Regla viva SUSTITUIDA · sale de PROJECT_STATE.md en trabajo/plataforma-adelantada (<fecha>)», con ADR-0082 como evidencia.
>  - MASTER_PLAN: su cuerpo no se toca. Debajo de la NOTA del 2026-10-10, una NOTA nueva con fecha y rama: el principio de §0 «Validacion de fidelidad (F26) antes de cualquier MQL5» queda enmendado por ADR-0082, con la frase de arriba; la parte de F28, F31 y F33 que adelanta, y que su orden vive en el tramo R6a de la hoja de ruta.
>  - Cualquier otro sitio vivo de la fase 0 a), alineado en el mismo commit. Lista cada uno, con su antes y después.
>
> FASE 3, la hoja de ruta (docs/plan/HOJA-DE-RUTA.md). Es una desviación pedida del paso 4 de entregar-rama (las entradas de la hoja no se tocan en la rama): decláralo en el informe.
>  - Un tramo nuevo, «## R6a · La capa de MT5 que no decide operaciones (ADR-0082)», entre R5 y R6, con una línea de cabecera: va en paralelo a R2-R5, en los huecos de espera, sin quitarle turno a F. Dentro, una entrada por rama de D9 (R6a.1 a R6a.7), con los cuatro campos de siempre y sus Refs. Cada Ref tiene que existir (test_hoja_de_ruta, regla b): F:F28, F:F31, F:F33, F:F17, ID:ADR-0082 y los ids de cada pieza (ADR-0057, ADR-0067, ADR-0068, ADR-0081, A-28, A-54, A-55, RN-029 a RN-032; NA:N en R6a.1 y R6a.5). Ninguna entrada nueva va HECHA.
>  - R6.1: «Depende de» pasa a decir que F29, F30 y lo de F31-F32 que decide operaciones dependen de R5.5 (ADR-0082, que enmienda MASTER_PLAN §0), y que lo demás de F31 vive en R6a.
>  - R7.1: su «Qué es» deja de decir que el pre-vuelo va aquí (pasa a R6a.7), y su «Depende de» pasa a R6.1 y R6a.
>  - Comprueba que el contrato de una rama futura puede nombrar «R6a» como tramo (contrato_rama.py acepta el título o el id antes de « · ») y escríbelo en el informe.
>
> FASE 4, adelgazar PROJECT_STATE con la tabla de la fase 0 d): lo que sale va al final de docs/state/HISTORIA.md (solo se amplía), literal, con su condición y su evidencia, en un bloque por clase con el formato de docs/state/README.md y el id en la cabecera, como «# Pendiente heredado SALE · 37 · …». Lo que se queda no se resume ni se reescribe. En PROJECT_STATE no queda ni un resumen de lo que sale.
>
> Cierre de la rama:
>  - make check > make-check.log 2>&1, con exit 0, ningún failed y la línea SELLO. En el informe, el tamaño final exacto de PROJECT_STATE.md y que pasan test_project_state.py, test_historia.py, test_hoja_de_ruta.py, test_adr.py y test_kit.py.
>  - La rama no toca hooks, rutas, código ni plataforma: no hace falta CI de Linux.
>  - Informe en docs/validation/PLATAFORMA-ADELANTADA.md: la fase 0 entera, mi respuesta a la PARADA, el ADR, cada sitio alineado con su antes y después, el tramo nuevo, lo que salió de PROJECT_STATE y adónde, la tabla de propuestas sobre la Next Action, y el tamaño final.
>  - Pasa el revisor (subagente revisor), con este alcance:
>    - que el ADR diga D1 a D9 y mi respuesta a D4, sin añadir ni quitar, y que la frontera de D3 sea una condición y no una lista;
>    - que ningún sitio vivo siga diciendo «antes de cualquier MQL5», salvo la cita literal de la enmienda y las instantáneas congeladas;
>    - que cada ADR cuya letra contradiga D4 lleve su recuadro;
>    - que nada salga de PROJECT_STATE sin evidencia, que todo lo que sale esté literal en HISTORIA y que lo que se queda no cambie de texto;
>    - y que el tramo R6a pase test_hoja_de_ruta sin entradas HECHAS.
>    Pega su informe al final del tuyo.
>  - Lo que cambie la Next Action (F, N y las ramas de R6a en los huecos) va en el commit del contrato cuando yo dé la orden de cierre. No toques la Next Action antes.
>
> Rama lista para revisión, NO cerrada.
