# Historia del estado del proyecto

> Lo que `PROJECT_STATE.md` ya no lleva porque dejo de ser el presente: la historia de merges, las
> funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas pagadas y las
> secciones que se quedaron sin uso. Nacio el 2026-10-01 en `trabajo/dieta-y-skills`
> (docs/validation/DIETA-Y-SKILLS.md), cuando `PROJECT_STATE.md` pesaba 418.819 bytes.
>
> **SOLO SE AMPLIA. Nunca se reescribe ni se borra una linea**: cada version commiteada empieza por
> la anterior, byte a byte, y lo vigila `tests/unit/test_historia.py` contra el historial de git.
> Un archivo nuevo se anade AL FINAL con su encabezado `# Archivo N · …` (docs/state/README.md).
>
> Cada archivo copia TAL CUAL lo que se saco de `PROJECT_STATE.md`, con sus encabezados `##` de
> entonces. Para buscar: el titulo de la seccion (`## Change Log`, `## Technical Debt`…) o la frase
> que `PROJECT_STATE.md` conserva como arranque de una entrada.

# Archivo 1 · PROJECT_STATE.md entero en df6aa2c (2026-10-01, `stable/F36j-guardia-linux`)

# PROJECT STATE

> Memoria operativa. Una sesión nueva lee este fichero, luego `docs/plan/features/<Current Feature>.md`,
> luego los ficheros de esa funcionalidad. Nada más salvo razón técnica registrada aquí.

## Project Goal
Bot fiel a la estrategia de un trader concreto (EURUSD, H4→M15→M1), verificable caso a caso contra sus
decisiones, ejecutable en MetaTrader 5 (cuenta FTMO 2-Step Swing de 100.000, ADR-0026; FundedNext se descarto el 2026-09-14 porque no admite bots desde 50.000), sin IA en ejecución. Fidelidad y rentabilidad se
miden por separado.

## Approved Architecture
Evidencia inmutable del corpus → elicitación con el trader (feedback solo-añadir) → StrategySpec ejecutable
+ biblioteca de casos → motor de referencia Python (núcleo puro, backtest sobre ticks, visor) → validación
de fidelidad → EA MQL5 (misma spec) → pruebas diferenciales → paridad con Strategy Tester → demo/sombra.
Referencia: `docs/plan/MASTER_PLAN.md` (plan vivo; el `.html` es la instantanea congelada) · `docs/research/2026-09-03-del-corpus-al-bot.html`.

## Development Strategy
Una funcionalidad = una rama `feature/F##-nombre` = un FUNCTIONALITY VALIDATION REPORT = un merge --no-ff
tras validación del usuario. `main` siempre estable y etiquetado `stable/F##`. Push autorizado por el usuario el 2026-09-04; `main` solo recibe merges validados.

## How to Start a Session
1. Leer este fichero. 2. Leer `docs/plan/features/<Current Feature>.md` y `docs/HANDOFF.md` (contexto humano de la ultima sesion; si contradice este fichero, manda este fichero). 3. `make check` (desde F01).
4. Si `Current Feature` está WAITING_FOR_USER_VALIDATION: no avanzar; preguntar.

## Change Regimes (must be respected)
- knowledge/evidence/  → INMUTABLE tras commit (hook). Corrección = nuevo item que supersede.
- knowledge/feedback/  → SOLO AÑADIR. Nunca editar un registro.
- docs/validation/ → un informe CERRADO en main no se reescribe: se corrige con un recuadro de correccion al principio y el cuerpo queda intacto (practica de F14A-INGESTA y ADR-0037, escrita en `CLAUDE.md` el 2026-09-22). Sin detector mecanico (Technical Debt).
- knowledge/corpus/libros.yaml → SOLO AÑADIR (ADR-0039): el sha fija los bytes, asi que el formato y el huso de un libro no cambian nunca; una entrada commiteada no se edita ni se borra (`knowledge validate`, version a version contra el historial).
- knowledge/spec/, knowledge/cases/ → versionados; cada cambio de valor cita evidence-id o feedback-id.
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- src/botsito/domain/ → sin IO, sin reloj, sin MetaTrader (import-linter).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

## Current Phase
FASE 2 · Retroalimentacion del experto. SESION 1 CELEBRADA el 2026-09-09 (2 h 27 min, video v6): el cuestionario entero respondido -preguntas, adicionales y confirmaciones-, y las doce ambiguedades A-1..A-12 RESUELTAS con feedback del trader. El etiquetado de casos lo entrega el trader como backtest: MAYO llego el 2026-09-11 (68 operaciones, en el corpus) y JUNIO queda DESCARTADO por decision del consultor el 2026-09-12, asi que la biblioteca de casos se construye solo con mayo: 19 dias, de los que 6 son `dev` y 13 holdout. F12 cerrada en main el 2026-09-12 (stable/F12). Siguiente: F13, y F14 en cuanto el consultor decida el reparto de mayo y que hacer con la exposicion del holdout

## Current Feature
NINGUNA ABIERTA. `trabajo/guardia-linux` quedo VALIDADA y cerrada en `main` el 2026-10-01 por orden de cierre explicita de Aleks tras la revision del consultor: tag `stable/F36j-guardia-linux`, recuadro de correccion en docs/validation/GUARDIAS-CLAUDE.md. Arregla la guardia de Claude Code en Linux (la CI de `stable/F36i-guardias-claude` salio roja) y anade a RITUAL.md la CI de Linux antes del merge para toda rama que toque la plataforma. LO SIGUIENTE: el I del Next Action. Lo anterior: NINGUNA ABIERTA. `trabajo/guardias-claude` quedo VALIDADA y cerrada en `main` el 2026-10-01 por orden de cierre explicita de Aleks tras la revision del consultor: tag `stable/F36i-guardias-claude`, informe docs/validation/GUARDIAS-CLAUDE.md, sin ADR. Lo que hay: un hook PreToolUse de Claude Code (`.claude/hooks/guardia.py`) que bloquea leer el material protegido y las operaciones prohibidas, el push a main con confirmacion (regla ask), el contrato de rama en make check y el subagente revisor. LO SIGUIENTE: el I del Next Action (la CLI respeta la cuarentena y los tramos no citables). Lo anterior: NINGUNA ABIERTA. `trabajo/cableado-simulador` quedo VALIDADA y cerrada en `main` el 2026-09-26 por orden de cierre explicita de Aleks tras la revision del consultor: tag `stable/F24-cableado-simulador`, informe docs/validation/CABLEADO-SIMULADOR.md, ADR-0053 ACEPTADO con todas sus decisiones PROVISIONALES y dos para revisar (2.1, los eventos del broker llegan al motor en el siguiente cierre de M1, con la cuenta vigilando por tick, se revisa con la demo en MetaTrader; 5.1, el cierre de RN-030 al precio de cierre de M1, se revisa al implementar RN-030). Lo que hay: el simulador completo de punta a punta -dia, motor de reglas, ordenes, broker, llenado con ticks, cuenta viva, veredicto de la firma y operaciones del bot para el criterio-, `motor arnes --simular` y `motor visor --simular` sobre construccion, la linea base nueva al lado de las anteriores con cobertura 0 y el embudo con menos paradas. EL HALLAZGO: aunque la geometria (A-35 y demas) quede resuelta, RN-020 seguira prohibiendo abrir mientras `perdida_dia` y `perdida_semana` no tengan magnitud ni corte en la spec; por eso nace A-44, BLOQUEANTE de RN-020 y el siguiente bloqueo del bot despues de A-35, en la hoja de la sesion 02 justo despues de A-43. LO SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como prioridad, y registrar sus respuestas (punto 22); RN-004 tras A-35 (punto 30); RN-020 tras A-44 (punto 35); y marzo con PARADA antes del sorteo mientras A-42 no este RESUELTA (punto 23). Lo anterior: NINGUNA ABIERTA. `trabajo/ticks-llenado` quedo VALIDADA y cerrada en `main` el 2026-09-26 por orden de cierre explicita de Aleks tras la revision del consultor: tag `stable/F24-ticks-llenado`, informe docs/validation/TICKS-LLENADO.md (registro de la sesion nocturna en NOCHE-TICKS-BROKER.md), ADR-0051 (el modelo de llenado) y ADR-0052 (el broker simulado), los dos ACEPTADOS. Lo que hay: ticks de Dukascopy de los dias dev de abril y agosto congelados con manifiesto (data/manifests/ticks/), integridad del cien por cien de las M1 con ticks, spread medido en knowledge/simulador/llenado.yaml, el modelo de llenado y el broker como funciones puras, la simulacion de punta a punta con una estrategia sintetica, la repeticion descriptiva de las operaciones del trader y la medida del instante con ticks. EL HALLAZGO QUE CAMBIA EL PROYECTO (ADR-0051 §8): el desenlace difiere entre ticks y respaldo M1 en una fraccion grande de las operaciones, asi que LOS TICKS SON OBLIGATORIOS para toda simulacion que cuente -construccion, medicion y holdout- y el respaldo M1 solo sirve para depurar. PENDIENTES con dueno: la ventana de ticks de invierno 06-14 UTC (ligada a A-42), el deslizamiento con la demo en MetaTrader (DN-3) y el swap medido en la plataforma (A-28, DN-6). LO SIGUIENTE: la sesion 02 con el trader y registrar sus respuestas (punto 22); cablear el motor de reglas al broker (punto 33); RN-004 tras A-35 (punto 30); y marzo con PARADA antes del sorteo mientras A-42 no este RESUELTA (punto 23). Lo anterior: NINGUNA ABIERTA. `trabajo/visor-dias` quedo VALIDADA y cerrada en `main` el 2026-09-25: tag `stable/F25-visor-dias`, runbook docs/runbooks/VISOR-DIAS.md, sin ADR ni informe (el brief limito lo comiteable a codigo, tests y runbook). `botsito motor visor --caso <id>` genera una pagina HTML autocontenida por dia de CONSTRUCCION -velas M1/M15, H4 de contexto con la que rompio el sesgo, operaciones del trader y del bot, hechos fijados en su instante, embudo y donde se para, avisos H3 y parejas del criterio-, `--todos` todos los dias con indice, `--hasta HH:MM` la vista sin mirar al futuro; misma compuerta y mismos mensajes que el arnes; la salida va a data/visor/, ignorada. LO SIGUIENTE no cambia: la sesion 02 con el trader (punto 22); los ticks y el modelo de llenado como SIGUIENTE RAMA (punto 32); el broker simulado y el cableado de la capa de cuenta (punto 33); RN-004 tras A-35 (punto 30). Marzo (punto 23) se DETIENE ANTES DEL SORTEO mientras A-42 no este RESUELTA (PARADA B0). Lo anterior: NINGUNA ABIERTA. `trabajo/simulador-cuenta` quedo VALIDADA y cerrada en `main` el 2026-09-25: tag `stable/F24-simulador-cuenta`, informe docs/validation/SIMULADOR-CUENTA.md, ADR-0050. La capa de cuenta del simulador -la mitad que dice si una cuenta pasa o se suspende- son funciones puras en `engine/cuenta.py`, y el perfil de cuenta es un fichero con el formato del registro en `knowledge/cuentas/` (FTMO 2-Step Swing 100k, cada cifra con su regla de FTMO-REGLAS; lo NO ENCONTRADO queda UNKNOWN y el simulador se niega a correr si lo necesita para decidir). NO esta cableada al motor: el contrato con `perdida_dia_firma` y `perdida_total_firma` queda descrito en ADR-0050 §5 y espera al broker. De paso, los hooks exportan `PYTHONUTF8=1` y el commit ya no depende de la consola (RITUAL.md, correccion 9). Las tres cosas del informe §5 las decidio el consultor al validar (Decisions and Rationale, 2026-09-25): `firma_huso_corte` se queda en el perfil vigilado por el test de medianoches, la guardia de tamano sin cifra no impide correr, y la duplicacion con `parametros.yaml` se acepta mientras el test la vigile. Decision nueva, pendiente de implementar en la proxima rama: `firma_comision_por_lado` toma el supuesto conservador de cobrarse en cada lado hasta que FTMO lo confirme. LO SIGUIENTE, en este orden: la sesion 02 con el trader (punto 22, con A-43 tras A-35); los ticks y el modelo de llenado, que es la SIGUIENTE RAMA (punto 32); el broker simulado y el cableado de la capa de cuenta al motor (punto 33); RN-004 tras A-35 (punto 30). Marzo (punto 23) se DETIENE ANTES DEL SORTEO mientras A-42 no este RESUELTA (PARADA B0).

## Current Branch
main

## Stable Main State
1f597cb · merge de `trabajo/guardia-linux` (tag `stable/F36j-guardia-linux`), sobre `stable/F36i-guardias-claude` (00ce911, cuyo commit de estado ebb836b dejo la CI de main en rojo, run 36889215829). La guardia de Claude Code en Linux: `_normcase` da minusculas y `/` en cualquier sistema y las zonas se recorren con la grafia real de sus carpetas (`Politica._ruta_real`); probado en la CI de Linux empujando la rama como `fix/guardia-linux` (run 36900517031: un solo fallo, el esperado de `state check` por el nombre de rama). RITUAL.md: toda rama que toque hooks, rutas, el sistema de archivos o scripts dependientes de la plataforma espera la CI de Linux en verde ANTES del merge; y un arreglo de codigo tras una CI roja va por rama y tag, no encima de main. ERRORES-RECURRENTES.md: el patron «pasa en Windows y falla en Linux».
00ce911 · merge de `trabajo/guardias-claude` (tag `stable/F36i-guardias-claude`), sobre `stable/F36h-be-al-tick` (16771c5). Las guardias de Claude Code (docs/validation/GUARDIAS-CLAUDE.md, sin ADR): `.claude/settings.json` con un hook PreToolUse para Read, Grep, Glob, Bash y PowerShell que bloquea leer el contenido del material protegido de CLAUDE.md punto 3 (holdout, libros de meses con dias reservados o sin sortear, imagenes del material adicional, hojas de sesion, crudas de v7 en adelante, los tramos no citables de v6 y lo que nombre un caso reservado), `--no-verify` y `core.hooksPath`, `push --force`, borrar tags, `rm -rf` sobre data/corpus/knowledge y lo indecidible; 24 reglas deny y el push a main como regla ask; `contrato.yaml` por rama, comprobado por make check (scripts/contrato_rama.py, docs/runbooks/CONTRATO-DE-RAMA.md); el subagente revisor (`.claude/agents/revisor.md`) y su metrica (docs/runbooks/ERRORES-RECURRENTES.md). No cambia motor, spec, knowledge ni ninguna cifra.
16771c5 · merge de `feature/be-al-tick` (tag `stable/F36h-be-al-tick`), sobre `stable/F36g-reflejar-feedback-s3` (0ba8dad). El break even de RN-014 al tick (docs/validation/BE-AL-TICK.md, ADR-0065 ACTIVE y PROVISIONAL, el G del Next Action): el stop pasa a la entrada exacta en el primer tick cuyo BID pasa el nivel de activacion -el mismo punto de zona_posterior_completada-, no al cierre de la M1; mover el stop es una peticion `modificar` y el cierre de la M1 no la repite; sin ticks, con `cierre` o con el criterio `cuerpo`, al cierre de la M1 y marcado en la traza (`stop_movido`). En diagnostico sobre construccion, cobertura, operaciones del bot y maximo diario de peticiones no cambian; los mismos 5 (cuenta arrastrada) y 12 (diaria) break even, todos al tick y de 19 a 60 s antes. Pendiente para la demo de FTMO (ADR-0065 §6): en una venta el break even salta por el ASK y pierde el spread (04-07 pos-o3, -4 puntos). S-1 resuelto con la opcion (b): una correccion del consultor sobre RN-033 y una confirmacion sin valor sobre RN-003; `feedback pending` en 0.
0ba8dad · merge de `feature/reflejar-feedback-s3` (tag `stable/F36g-reflejar-feedback-s3`), sobre `stable/F36f-registro-marzo` (e12a6dd). El feedback pendiente de la sesion 3, reflejado en la spec (docs/validation/REFLEJAR-FEEDBACK-S3.md), sin cambiar ningun valor ni el motor; spec 15.2.0. Citan ya su registro de la sesion 3: base_calculo_objetivo (del 0 al 1), RN-014 (break even al tocar), RN-015 (objetivo fijo, G-2) y RN-007 (la vela casi plana no cuenta, E-3). Opcion (b) del consultor: `feedback pending` lista aparte, como «confirmaciones de valores ya fijados», el CONFIRM que coincide con el valor vigente (4: liquidez_m15_criterio_toma, cartuchos_max, lotaje_base y G-1 sobre RN-015); S-1 sobre RN-033 sigue pendiente porque es un CORRECT. Hoja de la sesion 4: la 16 (b) sin coletilla y la 19 con la nota para Aleks. G-2: ninguna de las siete ganadoras de mas de 3 R se puede medir en pantalla (ACTIVAR-SESION-03.md §4.1.1). Next Action G (RN-014 al tick) y H (RN-007 espera la pregunta 14).
e12a6dd · merge de `feature/registro-marzo` (tag `stable/F36f-registro-marzo`), sobre `stable/F36e-barrido-sesion-4` (97feeb6). La recepcion del backtest de marzo de 2026, SIN ABRIR (docs/validation/REGISTRO-MARZO.md): un xlsx y 7 jpeg movidos a `corpus/Estrategia del trader/Material adicional de su operativa/Backtest marzo 2026/`, fuera de git, con su sha256 en knowledge/corpus/manifest.yaml y la recepcion en HOLDOUT-EXPOSICIONES.md (no quema). La propuesta del §4, ACEPTADA por el consultor: marzo por el camino de fidelidad (`eurusd-2026-03`). A-42 se cerrara como RESUELTA con el trader en la sesion 4, no por ADR: marzo no se sortea ni se ingiere hasta entonces y la PARADA B0 no cambia. Las 7 imagenes se quedan sin abrir y fuera del protocolo. En la hoja de la sesion 4, dos preguntas nuevas: la primera, cuando pone la orden tras formarse el minimo (o maximo) de M1; la ultima, que son las 7 capturas de marzo.
97feeb6 · merge de `feature/barrido-sesion-4` (tag `stable/F36e-barrido-sesion-4`), sobre `stable/F36d-orden-stop-pivote` (cf6b1bf). La hoja de preguntas para la sesion 4 con el trader (docs/sesion-4/PREGUNTAS.md, la F del Next Action), aceptada tal cual: todas las preguntas abiertas -la F y la A5, las ambiguedades ABIERTAS, el feedback pendiente y las de los informes- buscadas en el corpus ya ingerido (sesiones 1 a 3 y videos) antes de preguntar. 17 por preguntar, cerradas y sin graficos; 15 ya respondidas que no se repiten; 6 fuera de la hoja. Para el consultor: A-29, la caja de R6, A-36 y el break even al tocar ya tienen respuesta grabada. Solo lectura: no cambia motor, spec, ambiguedades ni feedback.
cf6b1bf · merge de `feature/F35-orden-stop-pivote` (tag `stable/F36d-orden-stop-pivote`), sobre `stable/F36c-caja-77` (2a71827). La D del Next Action (docs/validation/F35-ORDEN-STOP-PIVOTE.md, ADR-0064 ACEPTADO en su direccion con los valores DEFAULT_AMBIGUOUS bajo A-48 y A-29): la vida de la orden stop de ADR-0056 §7. La orden nace tras la toma en el posible punto de breaker que dice `orden_stop_punto` (`ultimo_pivote_m1` por defecto) y se reubica con cada pivote nuevo de M1, con la caja por operacion de `caja_bloque` (`r6`, del punto de breaker al punto mas alto) fijada segun `caja_se_fija`. En diagnostico sobre construccion: la cobertura pasa de 0 a 2 de 77 con la cuenta continua (que se frena el 22 de abril) y a 7 de 77 con la cuenta reiniciada cada dia; el stop del bot mide lo mismo que el del trader; el bot entra a 0,9 minutos de mediana del pivote y el trader a 2,5, y gana el 8 % frente al 43 %; el precio medio no salva ningun stop. Ningun valor por defecto cambio en la revision. El tag no lleva F35 en el nombre: en MASTER_PLAN, F35 es la puerta del go-live.
2a71827 · merge de `feature/caja-77` (tag `stable/F36c-caja-77`), sobre `stable/F36b-contador-peticiones` (f2300c0). La C del Next Action (docs/validation/CAJA-77.md): R1 a R6 de BLOQUE-DE-LA-CAJA §1.4 frente a la caja del trader reconstruida desde el libro en las 77 operaciones de construccion, con el stop en el 0,8 y en el 1, con criterio y umbral PRE-REGISTRADOS y subidos antes de medir. VEREDICTO NO DECIDE, aceptado por el consultor: ninguna regla llega al 40 % (maximo 16 % en la celda principal). Control: el stop del libro es el inicial y esta en el 1 de la caja (3 de 5 frente a 0 de 5 en el 0,8). Exploratorio (§3, posterior): el 0 de R5 y R6 localiza la entrada (36 de 77 frente a 18 con el placebo a 5 puntos) y su pivote es uno de M1 formado despues de la toma del productor (56 de 77). Solo medicion: ni motor, ni spec, ni productor cambian.
f2300c0 · merge de `feature/contador-peticiones` (tag `stable/F36b-contador-peticiones`), sobre `stable/F36-nocturno-01oct` (4507617). El contador de peticiones al servidor (docs/validation/CONTADOR-PETICIONES.md, la B del Next Action): el broker simulado apunta cada peticion que el bot emite -colocar, modificar (una pendiente o el stop de una posicion), cancelar y cerrar a mercado-, aceptada o rechazada, la lectura mas estricta de R13; lo que el servidor hace solo y `abrir_conocida` no cuentan. El dia se corta a medianoche CE(S)T (`firma_huso_corte`, ADR-0027). `motor arnes --simular` da por dia corrido el total, cada tipo y las rechazadas, y el maximo diario junto a `firma_mensajes_dia_max`. Solo mide, nada frena. Sobre construccion, en diagnostico: 11 peticiones en 42 dias, maximo diario 1 frente a 2000; se repite cuando entre F35.
4507617 · merge de `feature/nocturno-01oct` (tag `stable/F36-nocturno-01oct`), sobre `stable/F31d-ci-linux-memoria` (99ea2f5). La noche del 30 de septiembre (docs/validation/NOCTURNO-01OCT.md, sobre docs/nocturno/INFORME-01oct.md), revisada por el consultor: F32, con doble ruptura el sesgo lo decide el color y RN-002 cierra `cierre_h4_antelacion` antes del fin de la vela H4 (ADR-0060); F33, cada sesion es un escenario propio y `liquidez_tomada` caduca al abrirla; F34, el stop se redondea alejandose de la entrada (ADR-0061, que enmienda ADR-0029 §3 para el stop), el break even de RN-014 deja de ser un hueco y la toma de RN-004 la hace una vela de M1 (ADR-0062, `2763ceb`, que baja la cobertura en diagnostico de 2 a 0 de 77 y entra por decision del consultor); F36, el selector `reloj_sesiones` separa el reloj de las sesiones del del dia de riesgo sin cambiar ningun comportamiento (ADR-0063). Los cuatro ADR ACEPTADOS con sus 14 decisiones nocturnas; la 8 (un punto, no un pip) queda tambien para la sesion 4. RN-002 y RN-003 citan sus CORRECT de la sesion 3; RN-033 sigue igual y sus notas dicen que es una guardia del proyecto (ADR-0044, ADR-0060). spec 13.5.0 -> 14.4.1. F35 (vida de la orden stop) sigue BLOQUEADA.
99ea2f5 · merge de `fix/ci-linux-memoria` (tag `stable/F31d-ci-linux-memoria`), sobre `stable/F31c-memoria-suite` (1cca80e). Arreglo de la CI roja de 67ab298 (run 36675429816: 1 failed, 1367 passed), por orden de cierre de Aleks: `test_el_pico_del_proceso_sube_con_una_reserva_y_no_baja_al_soltarla` daba `antes`, `despues` y final iguales (141414400) porque en Linux `exec` conserva en `ru_maxrss` la RSS del proceso que hizo el fork, y el hijo lanzado directamente por pytest arrancaba con la de pytest (135 MiB), por encima de la reserva de 64 MiB. El test lanza ahora el hijo medido desde un intermediario pequeno; la reserva y las aserciones no cambian y no se salta en ninguna plataforma. Nota en `comun/memoria.py` y recuadro de correccion en docs/validation/MEMORIA-SUITE.md. CI de la rama en verde (run 36707223055: 1368 passed, 8 skipped).
1cca80e · merge de `trabajo/memoria-suite` (tag `stable/F31c-memoria-suite`), sobre `stable/F31b-ci-a27` (7ff9a9c). La memoria de la suite (docs/validation/MEMORIA-SUITE.md), sin cambios de estrategia, spec ni knowledge: `motor arnes` solo arranca `tracemalloc` con `--tracemalloc` y por defecto da el pico del PROCESO (`comun/memoria.py`), con los informes identicos byte a byte (el no simulado, de 275,6 s a 54,5 s); `make check` mide cada paso con `scripts/pico_memoria.py` y acaba con una linea `PICO DE MEMORIA` en el log, sin cambiar la linea `check:`. Pico de `make check` medido igual antes y despues: 844 -> 330 MiB, 15 min 31 s -> 10 min 31 s. Nota en CLAUDE.md sobre el recorte de procesos en segundo plano de Claude Code (`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`). La propuesta de adelantar la negativa de A-27 (ADR-0057 §5) sigue PENDIENTE y sin aplicar (Next Action, A4). 1376 passed.
7ff9a9c · arreglo de la CI roja de e7df30b, directo en `main` por orden del consultor (tag `stable/F31b-ci-a27`), sobre `stable/F31-activar-sesion-03` (269102c). El test que afirmaba que la CLI se niega por A-27 antes de leer velas se renombra a `test_la_cli_con_a47_fijada_pasa_a_pedir_a27` y se salta sin las velas en la maquina: A-27 la comprueba el broker al colocar la primera orden stop (ADR-0057 §5), tras leer velas y ticks, y en la CI, sin `data/`, la CLI se paraba antes por «falta en disco». Recuadro de correccion en docs/validation/ACTIVAR-SESION-03.md. El tag hace falta porque `state check` (regla 5) no admite en `main` cambios tras el ultimo tag salvo `PROJECT_STATE.md`: sin el, la CI de 7ff9a9c salio roja por eso (1 failed, `test_state_check_ok_on_real_repo`; 1360 passed, 8 skipped).
269102c · merge de `trabajo/activar-sesion-03` (tag `stable/F31-activar-sesion-03`), sobre `stable/F30-sesion-03` (00fcced). La sesion 3 activada en knowledge (docs/validation/ACTIVAR-SESION-03.md), solo knowledge, spec y documentacion regenerada: ninguna linea del motor cambia y ninguna `forma` se toca. 24 registros de feedback (sesion `2026-09-29-sesion-03`, trader_grabado, v9) y `feedback apply`: RESUELTAS A-26, A-31, A-34, A-37, A-38, A-40, A-41, A-45, A-46 y A-47 (`entrada_tipo_orden` = `stop_en_ruptura`); A-13 y A-18 siguen abiertas con lo firme confirmado; nace `stop_fraccion_redondeo` = `alejandose_de_la_entrada`; ningun parametro CONFIRMED cambia de valor. A-42 con decision PROVISIONAL en ADR-0059 (recuadro en ADR-0017), sin cambiar `huso_operativa`, y sigue ABIERTA y bloqueante; nace A-51, bloqueante de RN-020. Lo que la spec dice y el motor todavia no hace queda en el §3 del informe.
00fcced · merge de `trabajo/sesion-03` (tag `stable/F30-sesion-03`), sobre `stable/F29-viabilidad-comision` (5ed948f). La sesion 3 con el trader, ingerida como v9 (1:44:34, dos cortes de audio de cero digital, 28:49-29:53 y 57:00-58:06, no citables) y extraida pregunta por pregunta desde la version FILTRADA (docs/validation/SESION-03-EXTRACCION.md): las 29 preguntas de la hoja hechas, 62 items ev-v9-*, 11 tramos no citables por holdout (8 de cuarentena y 3 por precaucion) y el tramo de A-42 leido con mascara por orden del consultor. Los codigos se dijeron sin «pregunta» y la deteccion estricta encontro 0: localizacion a mano. Nada activado: solo propuestas. La respuesta del soporte de FTMO (ticket VDW-DPMWR-965) en FTMO-REGLAS.md, y la deuda del calendario de cierres anticipados en Technical Debt. Anterior:
5ed948f · merge de `trabajo/viabilidad-comision` (tag `stable/F29-viabilidad-comision`), sobre `stable/F28-corregir-evaluar-fase` (06b936c). Una MEDICION que NO se ensena al trader (docs/validation/VIABILIDAD-COMISION.md): la viabilidad de las 77 operaciones de construccion con tres comisiones de ida y vuelta (3, 5 y 10 USD por lote) y cuatro variantes del stop de A-18, mas la serie anotada. ESCENARIO DE REFERENCIA: 5 USD, la comision de forex que FTMO publica desde el 29-09-2025 (declarado por el consultor, no confirmado en demo; 3 USD es la tarifa anterior). Con 5 USD, V2 es la mejor simulada (+0,47 R neta, intervalo que cruza el cero; parte de su ventaja viene de las operaciones de stop cortisimo que excluye el tope de 100 lotes) y la serie anotada queda en +0,56 R con el intervalo sobre cero. Stops de 1,5 pips de mediana. El parametro del perfil no se toca. Anterior:
06b936c · merge de `trabajo/corregir-evaluar-fase` (tag `stable/F28-corregir-evaluar-fase`), sobre `stable/F27-viabilidad-trader` (a3adb77). La correccion de `evaluar_fase` (docs/validation/CORREGIR-EVALUAR-FASE.md, enmienda en ADR-0050): a igual instante, la apertura de una operacion va antes que sus marcas y sus marcas antes que su cierre, y una marca de una operacion que no esta abierta es un error con nombre. La causa raiz estaba en la capa de cuenta, no en el broker. Afectados: la repeticion de TICKS-LLENADO (1 % y 2 % de agosto pasan a SUSPENDIDA el 7 de agosto) y el bloque tal cual de la viabilidad; no afectados, byte a byte, el arnes con limite y stop y el embudo. Primera regresion en tests/regression (la cuenta del 7 de agosto). Recuadros de correccion en TICKS-LLENADO, NOCHE-TICKS-BROKER y VIABILIDAD-TRADER, este con la nota del consultor sobre el 1 % y el stop minimo. Anterior:
a3adb77 · merge de `trabajo/viabilidad-trader` (tag `stable/F27-viabilidad-trader`), sobre `stable/F26-demo-ftmo-script` (f1f2ccb). Una MEDICION que NO se ensena al trader (docs/validation/VIABILIDAD-TRADER.md): las 77 operaciones del trader en construccion frente a la fase 1 de FTMO 2-Step Swing 100k, simuladas por el broker sobre ticks y con su salida anotada. Al 0,5 % de la spec, con sus salidas reales pasa en abril y en abril+agosto; con la regla de salida de la spec, agosto rompe la perdida diaria el dia 7. La esperanza en R es positiva en bruto, pero con la comision del perfil (5 USD por lote en cada lado, 10/distancia R) los intervalos cruzan el cero en todos los tramos. ERROR DE CODIGO encontrado y no corregido: `evaluar_fase` reabre la posicion con la marca del instante del cierre; los veredictos validos son los saneados, y se corrige en `trabajo/corregir-evaluar-fase`. Anterior:
f1f2ccb · merge de `trabajo/demo-ftmo-script` (tag `stable/F26-demo-ftmo-script`), sobre `stable/F25-registrar-embudo` (5cb4477). El instrumento para medir la demo de FTMO, sin tocar estrategia ni parametros: tools/mql5/MedirDemoFTMO.mq5 (se niega fuera de una cuenta DEMO; solo EURUSD, lote minimo y numero magico propio; caducidad, stop de proteccion y limpieza al empezar, tras cada paso y al terminar; compilado con MetaEditor, 0 errores y 0 avisos, sin ejecutar) mide la ficha de EURUSD, el reloj, las pendientes del lado equivocado, el nivel exacto y el stops level, la modificacion que cruza, la comision por lado y el llenado de una stop; scripts/leer_demo_ftmo.py lo lee y marca los retcodes inesperados; docs/runbooks/DEMO-FTMO.md, para Aleks, con el CSV a data/demo_ftmo/ y tres ejecuciones alrededor del cambio de hora. Anterior:
5cb4477 · merge de `trabajo/registrar-embudo` (tag `stable/F25-registrar-embudo`), sobre `stable/F24-embudo-77` (e32a9d9). Registra las tres decisiones del codigo sin fuente que encontro EMBUDO-77, sin cambiar el motor: A-50 ABIERTA (RN-005 compara solo el 0 de la zona con el nivel tomado; lectura vigente marcada como decision de codigo sin fuente; 8 y 6 dias sin orden); la medida en A-43 (la M15 que cierra a las 07:00 cuenta como toma, 7 de 40 dias); y en EMBUDO-77 el recuadro de advertencia y correccion: una toma es un PIVOTE tomado (2992 minutos, 206 M15, 118 pivotes), la clasificacion no cambia y la anotacion de §2 baja de 3 a 1 de 39. Anterior:
e32a9d9 · merge de `trabajo/embudo-77` (tag `stable/F24-embudo-77`), sobre `stable/F23-selector-orden-stop` (87d166e). Una MEDICION, sin cambiar estrategia ni broker: scripts/embudo_77.py corre el motor cableado en diagnostico con la orden stop y anota para cada una de las 77 operaciones de construccion el primer paso del pipeline en que el bot deja al trader (docs/validation/EMBUDO-77.md). Con las dos lecturas de A-21: sesgo 19, liquidez 26, breaker 13 y 14, caja 15 y 14, broker 1, llenado 1, coinciden 2; la zona unica por dia de ADR-0055 explica 19 de las 26 de liquidez y 13 de las 15 de caja. Ningun paso lo decide un error de codigo; tres decisiones del codigo sin fuente (RN-005 solo con el 0 de la zona, la M15 que cierra a las 07:00 como toma, RN-004 refijando la misma toma en cada M1) quedan para su propia rama. Anterior:
87d166e · merge de `trabajo/selector-orden-stop` (tag `stable/F23-selector-orden-stop`), sobre `stable/F22-broker-ordenes-stop` (3a3dad7). La rama 2 de codigo de ADR-0056: el selector de A-47, `entrada_tipo_orden` (stop_en_ruptura | limite_en_retroceso), UNKNOWN, con --diagnostico-a47 exigido solo con --simular y antes de leer velas; con stop_en_ruptura la entrada va al broker como orden STOP en el 0 de la caja, en el mismo instante y al mismo precio que la limite (ADR-0058, PROVISIONAL, que enmienda ADR-0056 §1 con recuadro); con limite_en_retroceso la corrida sale como main byte a byte. Medida en construccion (docs/validation/SELECTOR-ORDEN-STOP.md): con stop se llenan casi exactamente las ordenes que como limites nacian cruzadas; 2 de 77 coincidencias frente a 1. Spec 13.4.0. Anterior:
3a3dad7 · merge de `trabajo/broker-ordenes-stop` (tag `stable/F22-broker-ordenes-stop`), sobre `stable/F21-blindar-make-check` (807f986). La rama 1 de codigo de ADR-0056: el broker simulado coloca y llena ordenes STOP de entrada (al toque, al precio del tick que la dispara; con hueco, peor que el nivel, y el deslizamiento guardado en la posicion) y RECHAZA una pendiente del lado equivocado del precio (precio_invalido), tambien al modificarla; el stops level del broker es firma_stops_level_puntos, UNKNOWN en el perfil de FTMO (A-27), con --diagnostico-a27. ADR-0057 PROVISIONAL hasta la demo. La estrategia no cambia. La linea base de construccion con limites cambia, revisado por el consultor: 5 ordenes que se llenaban cruzadas se rechazan y, en cascada, RN-032 deja de prohibir abrir (docs/validation/BROKER-ORDENES-STOP.md §3). Anterior:
807f986 · merge de `trabajo/blindar-make-check` (tag `stable/F21-blindar-make-check`), sobre `stable/F20-preparar-a47` (0a2914a). La guardia de la huella en `make check` (scripts/sello_make_check.py): `borrar` toma una huella del arbol de trabajo -HEAD; por fichero seguido, su entrada del indice y el mtime y el tamano; por fichero sin seguir fuera de .gitignore, ademas el hash- y `sellar` toma otra; si difieren, make check sale en rojo, nombra los ficheros y no sella. Cubre lo que el sello de antes dejaba pasar: un fichero estadiado a mitad, un cambio deshecho antes del final y un commit a mitad. La exclusion es .gitignore, sin lista aparte: lo que make check escribe dentro del arbol esta todo ignorado, medido con una foto del arbol en dos corridas (docs/validation/BLINDAR-MAKE-CHECK.md). Coste de la huella: 0,28 s y 1,5 MB; make check, 716,8 s y 281 MB antes, 727,9 s y 284 MB despues. Regla nueva en CLAUDE.md: ensayos en un clon desechable con git worktree, la raiz de un script que escribe por argumento o variable de entorno, y nada escribe mientras corre make check. Anterior:
0a2914a · merge de `trabajo/preparar-a47` (tag `stable/F20-preparar-a47`), sobre `stable/F20-bloque-de-la-caja` (de2e100). La entrada con la ruptura, preparada sin codigo: docs/validation/DISENO-ENTRADA-RUPTURA.md (Fase 1 medida: el broker solo tiene orden limite y llena al instante una limite cruzada a su propio precio; RN-011 dimensiona y RN-015 coloca en el cierre del breaker; el productor hace una zona por dia) y ADR-0056 ACEPTADO con las nueve decisiones del consultor del 2026-09-28 y la pieza nueva, la vida de la orden stop. Tres items de evidencia de v7 (el punto de breaker que se activa si el precio lo rompe, su actualizacion, y las velas consecutivas del mismo color). A-48 (que velas forman el bloque) y A-49 (vela cerrada o en formacion) ABIERTAS, no bloqueantes; A-29 con su tercera lectura al_aparecer_punto_de_breaker. Nada se resuelve ni se fija; las cinco ramas de codigo de ADR-0056 §8 empiezan por el broker. Anterior:
de2e100 · merge de `trabajo/bloque-de-la-caja` (tag `stable/F20-bloque-de-la-caja`), sobre `stable/F20-orden-stop-o-limite` (f792cd4). Descriptivo: que velas de M1 elige el trader como bloque de su caja en v7 y v8, medido sobre 12 cajas legibles (todas ventas) con seis reglas candidatas escritas antes de medir y la zona del productor. Con el criterio escrito, ninguna regla pasa de una caja; las versiones v2 y v3 quedan EXPLORATORIAS por decision del consultor, y la conclusion es que el 0 de la caja no sale de los fotogramas con esta muestra y se pregunta (docs/validation/BLOQUE-DE-LA-CAJA.md §3-§5). El stop segun el momento de la operacion: el paso del 1 al 0,8 de A-18 se ve en una caja y no en otras dos; A-18 sigue abierta. La regla 2 de docs/runbooks/SESION-DE-PREGUNTAS.md, que no salia de ningun ADR, cambia por decision del consultor: solo graficos de dias de construccion, cortados antes de la orden y sin fecha. Anterior:
f792cd4 · merge de `trabajo/orden-stop-o-limite` (tag `stable/F20-orden-stop-o-limite`), sobre `stable/F19-sesion-02-videos` (408b609). Mide, sin adoptarla, la hipotesis de que el trader entra con ordenes STOP: las 77 entradas de construccion llegan al nivel desde el lado de la ruptura (ticks), y el metodo queda ACOTADO por el consultor -distingue una limite colocada de antemano esperando el retroceso (lo que programa RN-011, y ninguna de las 77 lo es) pero no una stop de una limite ya pasada- (docs/validation/ORDEN-STOP-O-LIMITE.md §10). A-47 sigue ABIERTA. Dos recuadros de correccion en los informes de la sesion 02 y una deuda nueva del broker simulado. Anterior:
408b609 · merge de `trabajo/sesion-02` (tag `stable/F19-sesion-02-videos`), sobre `stable/F25-preparar-a21` (0d48c0c). Las dos grabaciones de la sesion 02 en el corpus (v7 y v8, esta rescatada con audio solo hasta 0:40:00), leidas por su version filtrada tras la cuarentena mecanica; lo que el trader hace en pantalla del 3 al 19 de agosto, comparado con su backtest original (docs/validation/SESION-02-VIDEO.md y SESION-02-VIDEO-V8.md, con las decisiones del consultor en §11); y A-47 abierta, el tipo de orden de entrada, BLOQUEANTE de RN-011. Anterior:
5a417b9 · merge de `trabajo/cableado-simulador` (tag `stable/F24-cableado-simulador`), sobre `stable/F24-ticks-llenado` (8c9beea). ADR-0053, el cableado del simulador, ACEPTADO por el consultor el 2026-09-26 con sus decisiones PROVISIONALES (1.1 el lote se resuelve al colocar; 1.2 `OP` es la unica posicion viva; 1.3 la zona `Z` es una ligadura de texto; 2.1 los eventos del broker llegan al cierre de M1, PARA REVISAR con la demo; 3.1 los acumuladores de la firma recortados en cero; 3.2 la primitiva del acumulador distingue por argumentos; 5.1 el cierre de RN-030 al cierre de M1, PARA REVISAR al implementarla; y las nuevas de la rama). engine/cableado.py: `MotorCableado` cumple el protocolo del arnes y por cada minuto de la ventana el broker avanza tick a tick hasta el ultimo milisegundo anterior al cierre de M1, la cuenta viva recibe sus eventos y marcas, los hechos de origen broker quedan a la vista y el interprete corre el cierre de M1; un solo reloj comprobado contra huso_operativa; la cuenta persiste y la estrategia y el broker empiezan cada dia de cero; ticks obligatorios salvo `--depuracion` marcado. engine/primitivas_broker.py: las primitivas de fuente broker y bot, los acumuladores de la firma leidos de la cuenta viva y las acciones que hablan con el broker sobre una orden en preparacion; ninguna cifra en el codigo. cuenta.CuentaViva y Broker.mover_stop. `motor arnes --simular` anade al informe la seccion de simulacion (veredicto, curva de equity por dia corrido, eventos del broker, huecos con nombre) y `motor visor --simular` ensena las ordenes, las posiciones y los eventos del bot; solo construccion, por la compuerta. Linea base docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt: cobertura 0 como toca sin geometria; las reglas RN-010, 012, 016, 017, 018, 019, 026, 027, 029, 031 y 032 pasan de DESCONOCIDO a evaluadas; siguen RN-005, 008 y 009 por geometria y RN-020 por hueco. EL HALLAZGO: RN-020 seguira prohibiendo abrir aunque la geometria quede resuelta, mientras perdida_dia y perdida_semana no tengan magnitud ni corte en la spec: nace A-44, bloqueante de RN-020. Huecos con nombre: perdida_dia, perdida_semana, cartuchos, la geometria y cinco acciones sin contrato. Antes, 8c9beea · merge de `trabajo/ticks-llenado` (tag `stable/F24-ticks-llenado`), sobre `stable/F25-visor-dias` (8d8a42c). ADR-0051, el modelo de llenado, y ADR-0052, el broker simulado, ACEPTADOS por el consultor el 2026-09-26 tras la sesion nocturna. Ticks de Dukascopy congelados por horas en streaming con manifiesto inmutable y hashes, solo de los dias dev de construccion y las horas 05-13 UTC (DN-5, aceptada para verano; la ventana de invierno 06-14 UTC queda ligada a A-42), y una CLI que se niega a cualquier mes que no sea de construccion; integridad con tolerancia fijada antes de comparar: todas las M1 con ticks cuadran; spread medido por hora local con el percentil 90 en knowledge/simulador/llenado.yaml (DN-4). engine/llenado.py: compra al ASK y vende al BID, las limites y los objetivos exigen pasar estrictamente el nivel y los stops saltan al toque (DN-1), con ticks el orden real (DN-2), respaldo M1 pesimista con el stop primero marcado en la traza, sin deslizamiento fijo (DN-3, provisional hasta la demo). engine/broker.py: ciclo de vida completo de la orden, rechazos por limite del perfil registrados, cierre por stop, objetivo o a mercado, comision por lado, swap por corte diario del huso del perfil (DN-6, provisional hasta medirlo, A-28), marcas del peor precio por minuto para la cuenta, hechos de origen broker derivados del estado; el contrato del motor, que sigue sin cablear, en ADR-0052 §5. engine/simulacion.py: mercado de un dia por la compuerta, estrategia al cierre de cada M1, la cuenta persistiendo entre dias. La repeticion descriptiva de las operaciones del trader (salida por la regla de la spec, DN-8) y la medida del instante con ticks estan en TICKS-LLENADO.md. EL HALLAZGO: los ticks son obligatorios para toda simulacion que cuente (ADR-0051 §8). Fase 0: firma_comision_por_lado toma el supuesto conservador por lado. Los hooks exportan PYTHONUTF8=1. El ritual de cierre lo ejecuta Claude Code solo ante una orden explicita de Aleks tras la revision del consultor (CLAUDE.md, RITUAL.md). Antes, 8d8a42c · merge de `trabajo/visor-dias` (tag `stable/F25-visor-dias`), sobre `stable/F24-simulador-cuenta` (11132d6). El visor de dias de construccion (`engine/visor.py`, `botsito motor visor`): para un dia dev de construccion, una pagina HTML autocontenida con SVG generado por codigo y sin JavaScript -M1 de la ventana con M15 conmutable por CSS, H4 de contexto con la que rompio el sesgo resaltada por sesion, operaciones del trader con entrada y stop en su llenado (el objetivo DERIVADO por objetivo_rr y marcado, porque el caso no lo trae, ADR-0043), operaciones del bot si el arnes las produce, y por sesion el sesgo, los hechos fijados en su instante, el embudo con la lectura del arnes, donde se para, avisos H3 y parejas del criterio-; `--todos` genera todos los dias con un indice; `--hasta` recorta la vista a un instante. Solo construccion y por la compuerta del arnes (`dias_de_construccion`), con sus mismos mensajes y codigos. La salida va a data/visor/, ignorada por git; el render es puro y determinista. Tests sobre un dia sintetico de 2030: compuerta, centinela, determinismo, coordenadas exactas, sin mirar al futuro, indice, salida ignorada. Runbook docs/runbooks/VISOR-DIAS.md. Antes, 11132d6 · merge de `trabajo/simulador-cuenta` (tag `stable/F24-simulador-cuenta`), sobre `stable/F18-huecos-motor` (a65dba5). ADR-0050, el simulador: la capa de cuenta. Las cuatro decisiones del consultor del 2026-09-25 escritas (objetivos y dias minimos por fase; comision y swaps dentro de la equity vigilada; volumen y limites de ordenes como `firma_*` en un perfil de cuenta; guardia de AVISO de tamano de posicion); H4 y H6 de ADR-0049 cumplidos (la cuenta persiste entre dias, el gate DESCONOCIDO sigue estricto). Estrategia, instrumento y perfil de cuenta son capas separadas: el perfil es UN fichero en `knowledge/cuentas/` con el formato del registro, leido por `cargar_registro` -misma puerta, mismos tipos, los tres estados de ADR-0012-, y una firma nueva es un fichero nuevo, nunca codigo (un perfil INVENTADO en tests/fixtures lo demuestra). Perfil FTMO 2-Step Swing 100k con cada cifra citando su regla R1..R20 de FTMO-REGLAS y cuatro parametros sin valor (`firma_comision_por_lado`, `firma_tamano_posicion_ratio_aviso`, y el objetivo y los dias de la fondeada, que por R1 y R4 no existen); lo que coincide con `parametros.yaml` lleva el mismo valor, cruzado por test, y `firma_huso_corte` (Europe/Prague) da los mismos instantes que `huso_operativa` en las 365 medianoches de un ano. La capa de cuenta (`engine/cuenta.py`): saldo y equity con los cargos en su instante, corte a cada medianoche local antes de cualquier evento, diaria sobre el saldo del corte vigilando la equity e infringida estrictamente POR DEBAJO (R18), total estatica o arrastrando, objetivo al LLEGAR sin posiciones vivas y con los dias minimos, estado EN_CURSO/SUPERADA/SUSPENDIDA con motivo e instante exactos y terminal, guardia de tamano solo aviso (NO EVALUABLE sin cifra). El margen de ADR-0031 no esta en la cuenta: es de la estrategia. Sin cablear: el contrato con los acumuladores de la firma queda descrito en ADR-0050 §5 (forma incremental, signo del acumulador, las dos comparaciones, un solo reloj) y espera al broker. Los hooks exportan `PYTHONUTF8=1`: el commit ya no depende de la consola, con test de consola cp1252 simulada y mutante. Antes, a65dba5 · merge de `trabajo/huecos-motor` (tag `stable/F18-huecos-motor`), sobre `stable/F18-arnes-motor` (8a5806e). ADR-0049 complementa a ADR-0048 y cierra sus seis huecos: H1 opcion (c) -`ambiguo` e `insuficiente` como valores del hecho `sesgo`, RN-003 con el predicado propio `sesgo_h4_al_abrir` que nombra `sesgo_h4_tope_velas` y cubre la busqueda hacia atras, RN-033 (gate) prohibe buscar_entradas y abrir_operacion con `vale: ambiguo` o `vale: insuficiente`, el nodo `hecho` admite `vale` (amplia ADR-0019), y el hecho declara `caduca: al_abrir_sesion` porque, medido, sin la caducidad la primera pasada del evento de apertura evaluaba los gates con el sesgo de la sesion anterior-; H2 opcion (a), test de que las sesiones de `kit/config.yaml` cubren exactamente [ventana_inicio, ventana_fin) y A-43 no bloqueante; H3 opciones (b) y (c), test de invariancia al orden dentro de cada clase y aviso de empate en la traza y el informe; H4 gate DESCONOCIDO estricto e intravela pesimista por OHLC hasta tener ticks; H5 `permite` nunca levanta un `prohibe`; H6 (c) PROVISIONAL. `sesgo_h4_tope_velas` sigue CONFIRMED con fuente ADR-0044 y la palabra provisional en su descripcion: el registro no tiene ese estado y el consultor lo acepta asi. spec 13.0.0. Linea base nueva al lado de la anterior: cobertura 0, `sesgo` con valor en todas las sesiones, RN-033 solo en las ambiguas, diagnostico por operacion intacto, y seis avisos de H3 (RN-001 y RN-033 prohiben lo mismo a las 15:00 de una segunda sesion ambigua), inofensivos y pendiente menor. Antes, 8a5806e · merge de `trabajo/arnes-motor` (tag `stable/F18-arnes-motor`), sobre `stable/F14-ftmo-reglas` (82fab11). ADR-0048 complementa a ADR-0030: el interprete del arbol generico (logica de Kleene, punto fijo con refraccion, precedencia por clase) en `src/botsito/engine/`, con NO_IMPLEMENTADA por primitiva que vale DESCONOCIDO y no decide; el dia como unidad de ejecucion, con el estado cruzando sus sesiones; RN-003 con `domain/sesgo.py`; el arnes con la compuerta (solo construccion, `casos_ocultos` antes de leer) y el embudo sobre el grafo de hechos; `botsito motor arnes`. Linea base sobre construccion: cobertura 0 de las operaciones del trader, precision sin definir, `sesgo` en la mayoria de las sesiones y todo lo demas parado en su primera primitiva sin escribir; por operacion reproduce el diagnostico de RN-003 exactamente. Seis huecos de interpretacion registrados en el ADR (H1-H6).

## Completed Phases
- FASE 1 · Base de conocimiento (F03, F04, F05, F06, F07, F08) · cerrada el 2026-09-08 en 5d8cf3c · puerta: 5 videos inventariados, transcritos (large-v3, glosario v2) y con fotogramas a 1 fps; 341 items de evidencia verificables por maquina y trazables a su propuesta y decision; busqueda `kb find | at` con fuente en cada linea; make check verde en main
- FASE 0 · Fundamentos (F01, F02) · cerrada el 2026-09-04 en dc3384d · puerta: make check verde en main; registro de parametros con tipos y lectura estricta; .gitattributes y cero CRLF; hooks copiados por make sync; tags stable/F01 y stable/F02; CI Linux verde

## Completed Features
- F01 · project-scaffold · validada el 2026-09-04 · docs/validation/F01-project-scaffold.md · tag stable/F01
- F02 · config-and-parameter-registry · validada el 2026-09-04 · docs/validation/F02-config-and-parameter-registry.md · tag stable/F02
- F03 · corpus-inventory · validada el 2026-09-04 · docs/validation/F03-corpus-inventory.md · tag stable/F03
- F06 · evidence-model · validada el 2026-09-04 · docs/validation/F06-evidence-model.md · tag stable/F06
- F09 · expert-feedback-model · validada el 2026-09-04 · docs/validation/F09-expert-feedback-model.md · tag stable/F09
- F15 · market-data-ohlc · validada el 2026-09-04 · docs/validation/F15-market-data-ohlc.md · tag stable/F15
- F04 · transcription-pipeline · validada el 2026-09-05 · docs/validation/F04-transcription-pipeline.md · tag stable/F04
- F05 · frame-extraction · validada el 2026-09-05 · docs/validation/F05-frame-extraction.md · tag stable/F05
- Auditoria global de la estructura · validada el 2026-09-06 · docs/validation/AUDITORIA-2026-09-05-estructura.md · tag stable/F05-auditoria-1
- Previos de F07 · validados el 2026-09-06 · docs/validation/F07-previos.md · tag stable/F05-previos-F07
- F07 · evidence-extraction · validada el 2026-09-07 · docs/validation/F07-evidence-extraction.md · tag stable/F07
- F08 · evidence-retrieval · validada el 2026-09-08 · docs/validation/F08-evidence-retrieval.md · tag stable/F08
- F10 · elicitation-kit · validada el 2026-09-08 · docs/validation/F10-elicitation-kit.md · tag stable/F10
- F11 · strategy-spec-schema · validada el 2026-09-10 · docs/validation/F11-strategy-spec-schema.md · tag stable/F11
- F12 · spec-semantic-validator · validada el 2026-09-12 · docs/validation/F12-spec-semantic-validator.md · tag stable/F12
- Holdout: que cuenta como abrirlo · validada el 2026-09-12 · docs/validation/HOLDOUT-2026-09-12.md · tag stable/F12-holdout
- F13 · spec-documents · validada el 2026-09-12 · docs/validation/F13-spec-documents.md · tag stable/F13
- Decisiones del consultor (A-15, A-16/A-23 y el reparto de mayo) · validada el 2026-09-12 · docs/validation/DECISIONES-2026-09-12.md · tag stable/F13-decisiones
- Auditoria del material recogido · validada el 2026-09-13 · docs/validation/AUDITORIA-2026-09-12-material.md · tag stable/F13-auditoria
- FTMO y arquitectura · validada el 2026-09-14 · docs/validation/FTMO-Y-ARQUITECTURA.md · tag stable/F13-ftmo
- Fidelidad de la spec · validada el 2026-09-17 · docs/validation/FIDELIDAD-DE-LA-SPEC.md · tag stable/F13-fidelidad
- Guarda del holdout · validada el 2026-09-17 · docs/validation/GUARDA-DE-HOLDOUT.md · tag stable/F13-guarda
- Meses vistos · validada el 2026-09-17 · docs/validation/MESES-VISTOS.md · tag stable/F13-vistos
- Reglas de la casa (CLAUDE.md y el runbook del ritual) · validada el 2026-09-17 · `CLAUDE.md`, `docs/runbooks/RITUAL.md` · tag stable/F13-reglas
- El breaker de M1 · validada el 2026-09-17 · docs/validation/BREAKER-M1.md · tag stable/F13-breaker
- La liquidez de M15 · validada el 2026-09-20 · docs/validation/LIQUIDEZ-M15.md · tag stable/F13-liquidez
- La entrada de septiembre · validada el 2026-09-20 · docs/validation/SEPTIEMBRE-ENTRA.md · tag stable/F13-septiembre
- El universo congelado (ADR-0035) · validada el 2026-09-21 · docs/validation/UNIVERSO-CONGELADO.md · tag stable/F13-universo
- Los cupos congelados y el ancla (enmienda ADR-0035) · validada el 2026-09-21 · docs/validation/CUPOS-CONGELADOS.md · tag stable/F13-cupos
- El camino de fidelidad (ADR-0036) · validada el 2026-09-21 · docs/validation/CAMINO-DE-FIDELIDAD.md · tag stable/F13-camino-de-fidelidad
- El sorteo de septiembre · validada el 2026-09-21 · docs/validation/SEPTIEMBRE-SORTEO.md · tag stable/F13-septiembre-sorteo
- La puerta por pregunta · validada el 2026-09-21 · docs/validation/PUERTA-POR-PREGUNTA.md · enmienda ADR-0033 · tag stable/F13-puerta
- La ingesta del detalle por operacion (F14a) · validada el 2026-09-21 · docs/validation/F14A-INGESTA.md · ADR-0037 · tag stable/F14a-ingesta
- La cobertura del material en el kit · validada el 2026-09-21 · docs/validation/COBERTURA-DEL-KIT.md · enmienda ADR-0036 · tag stable/F14-cobertura
- Abril y la caja · validada el 2026-09-21 · docs/validation/ABRIL-Y-LA-CAJA.md · sin ADR (no decide nada) · tag stable/F14-abril
- La caja del 29 de abril · validada el 2026-09-22 · docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md · ADR-0038 · tag stable/F14-caja
- Lo que no cabia en main · validada el 2026-09-22 · docs/validation/LO-QUE-NO-CABIA-EN-MAIN.md · sin ADR · tag stable/F14-runbook
- Mayo `dev` ingerido · validada el 2026-09-22 · docs/validation/MAYO-DEV.md · ADR-0039 y ADR-0040 · tag stable/F14-mayo-dev
- El ritual y sus ventanas · validada el 2026-09-22 · docs/validation/RITUAL-VENTANAS.md · sin ADR · tag stable/F14-ritual
- La guardia de ids citados en los documentos · validada el 2026-09-23 · docs/validation/GUARDIA-IDS-DOCS.md · sin ADR · tag stable/F14-guardia-ids
- La regla del mes sin filas · validada el 2026-09-23 · docs/validation/REGLA-MES-SIN-FILAS.md · sin ADR · tag stable/F14-regla-mes
- v5, los seis instantes · validada el 2026-09-23 · docs/validation/V5-INSTANTES.md · sin ADR · tag stable/F14-v5-instantes
- A-18 en las transcripciones · validada el 2026-09-23 · docs/validation/A18-TRANSCRIPCIONES.md · sin ADR · tag stable/F14-a18-transcripciones
- El dia reservado de v6 fuera del holdout · validada el 2026-09-23 · docs/validation/V6-FUERA-DEL-HOLDOUT.md · ADR-0041 · tag stable/F14-v6-fuera-del-holdout
- Inventario para la fidelidad · validada el 2026-09-23 · docs/validation/INVENTARIO-FIDELIDAD.md y docs/validation/INVENTARIO-FIDELIDAD-DECISIONES.md · sin ADR · tag stable/F14-inventario-fidelidad
- Abril y agosto, casos `dev` por el reparto dev-visto · validada el 2026-09-23 · docs/validation/CASOS-AGOSTO-ABRIL.md · ADR-0042 · tag stable/F14-casos-agosto-abril
- El criterio de fidelidad en desarrollo · validada el 2026-09-24 · docs/validation/CRITERIO-FIDELIDAD.md · ADR-0043 · tag stable/F14-criterio-fidelidad
- El motor, primera regla: el sesgo H4 · validada el 2026-09-24 · docs/validation/MOTOR-SESGO-H4.md · ADR-0044 · tag stable/F18-sesgo-h4
- A-24, A-21, A-26 y A-34 en las transcripciones · validada el 2026-09-24 · docs/validation/A24-A21-A26-A34-CRITERIO.md · ADR-0045 · tag stable/F19-a24-decidida
- A-35 en transcripciones y fotogramas · validada el 2026-09-24 · docs/validation/A35-PIVOTE-FORMADO-CLASIFICACION.md y docs/validation/A35-FOTOGRAMAS-RESULTADO.md · sin ADR · tag stable/F19-a35-al-trader
- La entrada de marzo, preparada antes de que llegue · validada el 2026-09-24 · docs/validation/ENTRADA-MARZO.md · ADR-0046 · tag stable/F14-entrada-marzo
- La sesion 02, preparada: inventario, candidatos C-xx y decisiones del consultor · validada el 2026-09-25 · docs/validation/SESION-02-DECISIONES.md · ADR-0047 · tag stable/F19-sesion-02-preparada
- Blindaje: la puerta del commit y el indice de ADR · validada el 2026-09-25 · docs/validation/BLINDAJE.md · sin ADR · tag stable/F14-blindaje
- Arreglo de la CI: main y el tag en un solo push atomico · validada el 2026-09-25 · docs/validation/ARREGLO-CI.md · sin ADR · tag stable/F14-arreglo-ci
- Reglas de FTMO 2-Step Swing con fuente oficial · validada el 2026-09-25 · docs/validation/FTMO-REGLAS.md · sin ADR · tag stable/F14-ftmo-reglas
- El arnes del motor · validada el 2026-09-25 · docs/validation/ARNES-MOTOR.md · ADR-0048 · tag stable/F18-arnes-motor
- La sesion 02 en video: v7 y v8, la tuberia con cuarentena y A-47 · validada el 2026-09-27 · docs/validation/SESION-02-VIDEO.md y SESION-02-VIDEO-V8.md · sin ADR · tag stable/F19-sesion-02-videos
- Orden STOP o LIMITE, medida sobre construccion · validada el 2026-09-28 · docs/validation/ORDEN-STOP-O-LIMITE.md · sin ADR · tag stable/F20-orden-stop-o-limite
- El bloque de la caja del trader en v7 y v8 · validada el 2026-09-28 · docs/validation/BLOQUE-DE-LA-CAJA.md · sin ADR · tag stable/F20-bloque-de-la-caja
- La entrada con la ruptura, preparada con selectores UNKNOWN · validada el 2026-09-28 · docs/validation/DISENO-ENTRADA-RUPTURA.md · ADR-0056 · tag stable/F20-preparar-a47
- La guardia de la huella en make check · validada el 2026-09-28 · docs/validation/BLINDAR-MAKE-CHECK.md · sin ADR · tag stable/F21-blindar-make-check
- El broker simulado: ordenes stop y rechazo de pendientes mal colocadas · validada el 2026-09-28 · docs/validation/BROKER-ORDENES-STOP.md · ADR-0057 · tag stable/F22-broker-ordenes-stop
- El selector de A-47 y RN-011 con orden stop · validada el 2026-09-28 · docs/validation/SELECTOR-ORDEN-STOP.md · ADR-0058 · tag stable/F23-selector-orden-stop
- El embudo de las 77 en construccion · validada el 2026-09-28 · docs/validation/EMBUDO-77.md · sin ADR · tag stable/F24-embudo-77
- Las decisiones sin fuente del embudo, registradas (A-50, A-43, EMBUDO-77) · validada el 2026-09-28 · docs/validation/EMBUDO-77.md (recuadro) · sin ADR · tag stable/F25-registrar-embudo
- El script de la demo de FTMO, su lector y el runbook · validada el 2026-09-28 · docs/validation/DEMO-FTMO-SCRIPT.md · sin ADR · tag stable/F26-demo-ftmo-script
- La viabilidad del trader en FTMO (NO se ensena al trader) · validada el 2026-09-28 · docs/validation/VIABILIDAD-TRADER.md · sin ADR · tag stable/F27-viabilidad-trader
- La correccion de evaluar_fase: el orden a igual instante · validada el 2026-09-28 · docs/validation/CORREGIR-EVALUAR-FASE.md · ADR-0050 (enmienda) · tag stable/F28-corregir-evaluar-fase
- La viabilidad con la comision y las variantes del stop (NO se ensena al trader) · validada el 2026-09-28 · docs/validation/VIABILIDAD-COMISION.md · sin ADR · tag stable/F29-viabilidad-comision
- La sesion 3 con el trader (v9): ingesta, extraccion revisada y respuesta del soporte de FTMO · validada el 2026-09-29 · docs/validation/SESION-03-EXTRACCION.md · sin ADR · tag stable/F30-sesion-03
- La sesion 3 activada en knowledge (24 registros, diez ambiguedades resueltas, A-42 provisional) · validada el 2026-09-29 · docs/validation/ACTIVAR-SESION-03.md · ADR-0059 (PROVISIONAL) · tag stable/F31-activar-sesion-03
- La noche del 30 de septiembre: F32, F33, F34 y F36 (sesgo con doble ruptura y cierre antes del fin de la H4, sesiones como escenarios, stop hacia fuera, break even y toma en M1, reloj de las sesiones) · validada el 2026-09-30 · docs/validation/NOCTURNO-01OCT.md · ADR-0060, ADR-0061, ADR-0062 y ADR-0063 · tag stable/F36-nocturno-01oct
- El contador de peticiones al servidor (R13), por dia de la firma en el arnes · validada el 2026-09-30 · docs/validation/CONTADOR-PETICIONES.md · sin ADR · tag stable/F36b-contador-peticiones
- La caja de las 77: R1 a R6 frente a la caja reconstruida desde el libro, pre-registrada (NO DECIDE) · validada el 2026-09-30 · docs/validation/CAJA-77.md · sin ADR · tag stable/F36c-caja-77
- La vida de la orden stop: nace en el ultimo pivote de M1 tras la toma y se reubica con cada pivote nuevo, con la caja de R6 (diagnostico: 7 de 77 con la cuenta diaria; el bot entra antes que el trader) · validada el 2026-09-30 · docs/validation/F35-ORDEN-STOP-PIVOTE.md · ADR-0064 (ACEPTADO en su direccion; valores DEFAULT_AMBIGUOUS) · tag stable/F36d-orden-stop-pivote
- El barrido de preguntas para la sesion 4: 17 por preguntar, 15 ya respondidas, 6 fuera de la hoja · validada el 2026-09-30 · docs/sesion-4/PREGUNTAS.md · sin ADR · tag stable/F36e-barrido-sesion-4
- La recepcion del backtest de marzo, sin abrir: 8 ficheros en el corpus con su huella; propuesta de protocolo aceptada; A-42 por el trader en la sesion 4 · validada el 2026-09-30 · docs/validation/REGISTRO-MARZO.md · sin ADR · tag stable/F36f-registro-marzo
- El feedback de la sesion 3 en la spec (4 citas nuevas, 4 confirmaciones aparte, S-1 pendiente) y G-2 en fotogramas (0 de 7 medibles) · validada el 2026-09-30 · docs/validation/REFLEJAR-FEEDBACK-S3.md · sin ADR · tag stable/F36g-reflejar-feedback-s3
- El break even de RN-014 al tick, y S-1 llevado a RN-003 (feedback pending en 0) · validada el 2026-10-01 · docs/validation/BE-AL-TICK.md · ADR-0065 (PROVISIONAL) · tag stable/F36h-be-al-tick
- Las guardias de Claude Code: hook PreToolUse, permisos (deny y ask), contrato de rama y subagente revisor · validada el 2026-10-01 · docs/validation/GUARDIAS-CLAUDE.md · sin ADR · tag stable/F36i-guardias-claude
- La guardia de Claude Code en Linux, y la CI de Linux antes del merge · validada el 2026-10-01 · docs/validation/GUARDIAS-CLAUDE.md (recuadro de correccion) · sin ADR · tag stable/F36j-guardia-linux

## Features Waiting for Validation
— ninguna.

## Existing Components
- Paquete `botsito`: `domain/valores.py` (Fraccion, Porcentaje sobre Decimal, no intercambiables; HoraLocal con huso); `config/registro.py` (registro de parametros con categoria, procedencia y lectura estricta; vacio de valores); `config/ajustes.py` (entorno y rutas, sin claves de negocio).
- CLI: `state check` (rama, recuento de tests, tag estable, informes de validacion, main sin cambios tras el tag), `knowledge validate` (registro, manifiesto, evidencia, contradicciones, feedback, historial de git y trailers `Fuente:`), `config validate` (ajustes contra el registro), `corpus inventory` y `corpus check`.
- `corpus/inventario.py`: manifiesto del corpus con SHA-256, ffprobe, papel y huecos de fotogramas heredados. `knowledge/corpus/{fuentes,manifest}.yaml`.
- `evidence/{modelo,contradicciones,verificacion,propuestas}.py` + `comun/historial.py` + `validation/contexto_evidencia.py` (ADR-0009): EvidenceItem inmutable (id con hash) con `transcripcion` y referencias `fr-*`; cita de audio localizada por tokens en la cruda citada con tiempo por palabras (`[t0 - 2 s, t1 + 2 s]`, comodin `[...]`); cita de pantalla anclada a un fotograma real del tramo; contradicciones regeneradas; propuestas trazables en `knowledge/_proposals/` (esqueleto, `--check` con guardias, sello `salida_sha256`, `accept`/`reject`); taxonomia `knowledge/evidence/_temas.yaml`. CLI `evidence new|propose|accept|reject|list|contradictions`. Hook rechaza editar o borrar evidencia y feedback.
- `feedback/modelo.py`: FeedbackRecord solo-anadir (id por hash, coherencia accion/objetivo, trazabilidad, supersede del mismo objetivo sin ciclos); CLI `feedback new` (valida contexto antes de escribir), `trace`, `pending` (filtra parametros no `estrategia`); `commits_sin_fuente` exige trailer `Fuente:` con ids existentes (evidencia, feedback, ADR) en commits que tocan spec/cases desde el SHA de stable/F06; `historial_evaluable` marca clon superficial o repo anidado como no evaluable.
- Contratos de importacion (import-linter + test AST; `domain` no importa `config`). Test de literales de negocio con lista real. Tests de integridad del indice.
- Makefile (`sync` copia hooks a .git/hooks; `check`; `regress`), CI Linux con `uv sync --locked`, hook pre-commit anti-main.
- `domain/velas.py` (F15): `Vela` (MinutoUtc, Puntos, volumen entero, duracion, n_m1, completa), `SerieVelas`, `combinar`; sin datetime/float/Decimal. `data/velas.py` (CSV determinista), `data/agregacion.py` (particion UTC por reloj de pared, ADR-0005), `data/dukascopy.py` (bi5, red inyectada, planas descartadas), `data/dataset.py` (dataset congelado, manifiesto inmutable con id por hash, `cargar_serie` con ventana). CLI `data download/check/aggregate`. Hook y `knowledge validate` protegen `data/manifests/`.
- Paquete `comun/` (ADR-0006, por encima de `domain`): `yaml_estricto.py` (claves duplicadas y no hashables rechazadas, fechas como texto), `historial.py` (guardia de git para evidencia, feedback y manifiestos; trailers Fuente), `documentos.py` (normalizacion, vacios, hash corto, directorios, supersede, activos), `ids.py` (todos los formatos de id), `husos.py` (nombre IANA canonico, un criterio para registro y datos). `validation/knowledge.py`: orquestador de `knowledge validate` (F12 y F14 anaden capas ahi); la CLI solo imprime. Registro: accesores por tipo declarado; test de contrato que vigila `registro.<accesor>("nombre")` en src/. Contrato de capas: cli > validation > viewer/mql5bridge > engine > cases > spec > feedback > evidencia/corpus/data/config > comun > domain. `scripts/instalar_hooks.py` (make hooks portable; destino `git rev-parse --git-path hooks`; aborta con `core.hooksPath` global). `.python-version` = 3.12 (local y CI).
- `cases/{ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py` (F10, ADR-0011): ambiguedades legibles por maquina (`knowledge/spec/ambiguedades.yaml`), cuestionario con casos `ev-*` por origen fusionado, ventanas de replay sobre dias no vistos (hash de velas y limites H4 por anclaje), particiones por hash con seed, kappa de Cohen desde los `LABEL_CASE`, paquete determinista de cada sesion en `knowledge/cases/kit/<sesion>/` con `check` puro; guardia en `knowledge validate` (particiones antes del primer LABEL_CASE y sin cambios despues). CLI `kit build|check|kappa`. Datos de negocio del kit en `knowledge/cases/kit/config.yaml`.
- `retrieval/{indice,consultas,salida}.py` (F08, ADR-0010; capa entre `spec` y `feedback`): indice en memoria regenerado en cada ejecucion (353 items + segmentos de las crudas activas con su corregida y `dudas`; fotograma de referencia `referencia_en`), token de busqueda = tokens de F07 con acentos plegados y numeros normalizados, `kb find` (AND por documento, `--frase` con comodin via `buscar_secuencia`, `--prefijo`, filtros, `--top`, `--json`) y `kb at` (items, segmentos, fotograma y contradicciones de un instante). Toda linea con fuente; rutas relativas; sin escritura. `corpus.pipeline_transcripcion.{dudas_de,cargar_capas}` compartidos con `validation`.
- `corpus/{audio,transcripcion,motor_whisper,glosario,pipeline_transcripcion,manifiestos_transcripcion}.py` (F04, ADR-0007): WAV por video y corte por muestras en silencios, segmentos en ms enteros con senales, faster-whisper solo en `motor_whisper`, glosario de dos alcances, pipeline reanudable con manifiesto INMUTABLE `tr-<video>-<motor>-<hash8>` en `knowledge/corpus/transcripciones/`, corregida = cruda + glosario verificada por recomputo; guardia `comprobar_prompt` (223 tokens, antes de cargar la GPU) y huella de reanudacion sin `gpu` ni `initial_prompt_tokens` (`CLAVES_FUERA_DE_HUELLA`, 2026-09-06). CLI `corpus transcribe | glossary apply | transcript check | transcript show`; capa en `knowledge validate`; hook protege el directorio.
- Corpus: 6 videos (v5 = grabacion del trader del 2026-09-05 en FXReplay, 6 min; v6 = la sesion 1 del 2026-09-09, 2 h 27 min) y material adicional de enero, abril, agosto y MAYO 2026 (xlsx + capturas; mayo entro el 2026-09-11).
- `corpus/trabajo.py` (auditoria 2026-09-05): guardias comunes a transcripciones y fotogramas: carpeta de trabajo decidida por marcas locales Y por los manifiestos registrados (clon sin `data/`), exactamente una extraccion activa por video y tipo, inmutabilidad del contenido por carpeta, manifiesto existente idempotente sin `reemplaza_a`. `config/ajustes.carpeta_datos` unica para CLI y `knowledge validate`.
- `corpus/{fotogramas,manifiestos_fotogramas}.py` (F05, ADR-0008): cobertura completa de cada video a 1 fps sin perdida (PNG bitexact) con regla `select` "primer fotograma con t >= instante" y `pts` real de `showinfo`; `index.jsonl` en `data/fotogramas/<video>/png-1fps/`; manifiesto INMUTABLE `fr-<video>-<hash8 del indice>` en `knowledge/corpus/fotogramas/` (un activo por video, `reemplaza_a`, huecos sobre `pts`, extra); obligatorios en `knowledge/corpus/fotogramas_obligatorios.yaml` validados contra el indice activo; referencia citable `fr-<id>/<t_ms>` (`referencias_conocidas` excluye `heredado_v2`). CLI `corpus frames extract | check | show`; capa en `knowledge validate`; hook protege el directorio.
- Plantillas: brief, ADR, informe de validacion. ADR-0001 a 0011. `.gitattributes` con LF (`*.bi5` binario).
- `botsito.spec` (F11, ADR-0013): `modelo.py` (carga estricta de reglas y glosario, guardia de cifras y verificacion de literales contra lo que citan) y `manifiesto.py` (hash canonico sobre los tres ficheros de la spec y guardia de `spec_version`).
- `botsito.feedback.aplicar` (F11): lleva los valores de una sesion al registro sin interpretarlos; reescribe `parametros.yaml` preservando comentarios y falla si el formato no es el que sabe editar.
- CLI nueva de F11: `feedback apply --sesion <s> [--check]`, `spec status`, `spec manifest [--escribir]`.
- CLI y guardias de F12: `spec check` (la capa semantica sola, misma puerta que `knowledge validate`); las reglas con `forma` ejecutable y su vocabulario (`predicados`, `acciones`, `efectos`, `hechos`, `acumuladores`); campo `consumido_por` en el registro; y cuatro guardias nuevas: `comprobar_forma`, `comprobar_consumo`, `comprobar_citas_revocadas` y la que exige que una ambiguedad RESUELTA tenga su registro.- `botsito.cases.spec_docs` (F13): genera `docs/spec/` -reglas, parametros, glosario, ambiguedades- desde `knowledge/spec/`; `spec docs [--escribir]` y un test de contrato que regenera y compara el texto entero. La forma ejecutable se imprime VERBATIM como JSON.
- `botsito.cases.hoja_docx` (F13, antes `scripts/hoja_sesion_docx.py`): la hoja de respuestas de la sesion en Word; `kit hoja [--sesion] [--salida]`. Al entrar en `src/` quedo bajo `mypy --strict`, los contratos de importacion y el contrato de literales de negocio.
- Estado `DECIDIDA` de las ambiguedades (F13, ADR-0022): la cierra el consultor con un ADR que la nombre, y `spec status` le da su propia seccion. `RESUELTA` sigue siendo solo del trader.
- `recibido_el` y `procedencia` en el feedback (F13, ADR-0023): opcionales en el esquema y obligatorios por guardia desde la sesion del 2026-09-13; la validacion corre AL CARGAR.
- Seccion `tokens` del vocabulario de la spec (F13): los sujetos de geometria y los estados del bot, declarados. Con ella, `comprobar_forma` niega por defecto y ningun argumento de una regla puede llevar un valor de negocio crudo.
- `feedback pending` con tres estados (F13): pendiente, reflejado y SIN MECANISMO, que es el que impide afirmar lo que no se puede comprobar.

## Important Files
- PROJECT_STATE.md · README.md · docs/plan/MASTER_PLAN.md (fuente viva; seccion H = salvaguardas de la auditoria)
- knowledge/evidence/README.md (esquema de EvidenceItem) · src/botsito/evidence/modelo.py
- knowledge/feedback/README.md (esquema de FeedbackRecord y plantilla de sesion) · src/botsito/feedback/modelo.py · src/botsito/comun/historial.py
- knowledge/corpus/fuentes.yaml (fuentes esperadas, ids de Drive) · knowledge/corpus/manifest.yaml (GENERADO) · src/botsito/corpus/inventario.py
- docs/adr/0011-kit-de-elicitacion.md · knowledge/spec/ambiguedades.yaml (manual; fuente de la tabla Known Ambiguities) · knowledge/cases/kit/README.md (gramatica de la etiqueta) · knowledge/cases/kit/config.yaml (datos de negocio del kit) · src/botsito/cases/paquete.py · docs/validation/F10-elicitation-kit.md
- knowledge/spec/parametros.yaml (LA puerta de los parametros; el recuento y el desglose por estado los da `botsito spec status`, y `docs/spec/parametros.md` los publica generados: `huso_operativa` = Europe/Madrid por ADR-0017, que REVIERTE ADR-0012 y restituye ADR-0005 (esta linea dijo Etc/GMT-2 hasta el 2026-09-12, y ese offset fijo es justo el fallo que ADR-0017 llama el mas caro y el unico sin sintomas: dejaba el ancla H4 una hora antes que la vela real todo el invierno); los de estrategia citan al trader y los de entorno un ADR) · `knowledge/spec/strategy_spec.yaml` (el recuento lo da `spec check`) · `knowledge/spec/glossary.yaml` · `knowledge/spec/spec_manifest.yaml` (semver + hash sobre los tres) · src/botsito/config/registro.py · src/botsito/domain/valores.py
- docs/adr/0005-datos-de-mercado-fuente-formato-y-relojes.md · data/manifests/README.md (esquema del manifiesto) · src/botsito/data/agregacion.py (regla de anclaje) · tests/fixtures/ohlc/README.md (fixtures reales con sha256)
- docs/adr/0007-transcripcion-en-dos-capas.md · knowledge/corpus/glosario_asr.yaml (manual, versionado) · knowledge/corpus/transcripciones/ (INMUTABLE) · src/botsito/corpus/pipeline_transcripcion.py · docs/validation/F04-transcription-pipeline.md
- knowledge/corpus/tramos_no_citables.yaml (manual; tramos de video que NO son especificacion: `evidence propose --check` y `evidence new` rechazan una cita que caiga dentro) · src/botsito/validation/contexto_evidencia.py
- docs/adr/0008-fotogramas-cobertura-completa.md · knowledge/corpus/fotogramas_obligatorios.yaml (manual) · knowledge/corpus/fotogramas/ (INMUTABLE) · src/botsito/corpus/fotogramas.py · docs/validation/F05-frame-extraction.md
- docs/plan/features/F02-config-and-parameter-registry.md · docs/validation/F02-config-and-parameter-registry.md
- docs/adr/0002-registro-de-parametros-una-sola-puerta.md · docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
- docs/plan/AUDITORIA_FASES_2026-09-04.html · pyproject.toml · Makefile · src/botsito/cli.py · scripts/git-hooks/pre-commit
- docs/research/2026-09-03-del-corpus-al-bot.html (investigacion) · docs/plan/MASTER_PLAN.html (instantanea congelada del plan)

## Tests Currently Passing
1110 funciones de test (1686 casos; parametrizadas x3, x4, x5, x6, x7, x8, x9, x10, x11, x13, x14, x15, x18, x19, x22, x26 y x30) · unit: guardias de Claude Code (rama trabajo/guardias-claude: `test_guardia_claude` -el hook bloquea leer material reservado, deja pasar stat, tamano y sha256, bloquea el bash indecidible, las operaciones prohibidas, y el ritual y los runbooks pasan-, `test_contrato_rama` -el contrato falla fuera de las rutas permitidas, dentro de las protegidas y sin artefacto, y pasa dentro- y `test_revisor` -frontmatter valido, sin herramientas de escritura, Bash de solo lectura-); cableado (ADR-0053 sobre un dia SINTETICO de 2030 con la spec REAL y una estrategia sintetica que vive en el test: la geometria NO_IMPLEMENTADA resuelta a mano liga Z a una zona, RN-011 y RN-015 dimensionan y colocan la limite por el motor, el broker la llena con ticks, salta el stop al precio del tick que lo cruza, RN-012 dispara y la cuenta viva da el veredicto con la comision por lado; un hueco de 2.000 puntos deja la cuenta SUSPENDIDA en el instante del tick y RN-029 y RN-031 -antes DESCONOCIDO- prohiben en el cierre de M1 siguiente, nunca antes; el reloj unico se comprueba al arrancar; sin mirar al futuro de punta a punta -recortar los ticks tras el stop no cambia nada de lo fijado hasta el corte-; el informe identico byte a byte; los ticks obligatorios y la depuracion marcada; la cuenta persiste dos dias y la estrategia y el broker empiezan de cero -el lote del dia 2 sale del saldo mermado-; el detalle para el visor con ordenes, posiciones y eventos; y la CLI `--simular` del arnes y del visor que se niega a medida y a lo que no es construccion sin escribir nada); · unit: huecos_motor (ADR-0049 sobre H4 SINTETICAS y la spec real. H1: una sesion ambigua fija `sesgo` a ambiguo y RN-033 prohibe, una segunda sesion ambigua no hereda el sesgo de la primera ni una no ambigua la prohibicion de una ambigua -el hecho caduca al abrir-, insuficiente prohibe, el hecho solo caduca en la apertura, `vale` en el nodo hecho, la forma y la primitiva coinciden en todas las sesiones de construccion cuando `data/` esta, y las guardias nuevas: `vale` fuera de los valores o sobre un hecho sin valores, un valor de hecho que no es token, `sentido` como token en un predicado con lado_de_ruido, y `caduca` sin token de caducidad o en un hecho del broker. H2: las sesiones de kit/config.yaml cubren exactamente [ventana_inicio, ventana_fin) en huso_operativa. H3: la misma traza con el orden de cada clase invertido en cuatro escenarios, el aviso cuando dos reglas de la misma clase dan SI en la misma pasada -y ninguno cuando la spec las encadena por un hecho-, y el informe que lista los avisos y, con el motor real, ninguno); · unit: arnes_motor (ADR-0048 sobre velas y dias SINTETICOS: la logica de Kleene -una primitiva que falta vale DESCONOCIDO y no decide-, una regla desconocida no fija y un gate desconocido bloquea su efecto, sin mirar al futuro -anadir velas despues de T no cambia nada de lo decidido hasta T-, una NO_IMPLEMENTADA detiene la sesion y queda en el embudo, la negativa a medida y a lo que no es construccion, el centinela de un dia oculto que no se lee -y que si se leeria sin la compuerta-, un motor que copia al trader da 100 % y embudo completo, uno que no opera da cobertura 0 y precision sin definir, el informe identico byte a byte, y la CLI `motor arnes` que se niega a medida y a lo que no es construccion sin escribir nada); · unit: push_atomico (el run 36174003223 reproducido en un repo temporal: `state check` sobre un merge sin su tag falla con «main tiene cambios sin tag estable» y el mismo arbol pasa al crear el tag; el ritual empuja main y el tag en UN solo `git push --atomic` y ningun runbook empuja main o un tag suelto, con su prueba sobre el ritual viejo); · unit: adr, indice de PROJECT_STATE (lista EXACTAMENTE los ADR de docs/adr/, sin que falte, sobre ni se repita ninguno, con su prueba sobre un indice sintetico); · unit: sello_make_check (la puerta del commit sobre repos TEMPORALES con los hooks versionados: sello correcto y el commit entra; arbol cambiado despues del sello, sin sello, `commit -a` y `--amend` sin el sello de su arbol se rechazan diciendo que hacer; `make` con la linea `check:` real en rojo no sella y borra el sello viejo, en verde sella; cambios sin estadiar o un fichero sin seguir no sellan y uno ignorado si; `merge --no-ff` pasa con el sello del arbol fusionado, y sin el queda a medias y se sale abortando, sellando en la rama y repitiendo el merge; main sigue exigiendo BOTSITO_ALLOW_MAIN; el bloque del sello identico en los dos hooks y ninguna via de escape nueva); · unit: hoja_preguntas (el orden de la sesion 02 que fijo el consultor, cada pregunta tal cual del yaml y en su orden, las tres reglas arriba, y que una pregunta cerrada, repetida o inexistente para la hoja); · unit: buscar_sesion02 (la lista cerrada de los candidatos C-01, C-02, C-04, C-05, C-06 y C-07 sin palabras sueltas, sus tres controles positivos, una cifra que no casa dentro de otra, los conjuntos de A-24 y A-35 intactos y la CLI que rechaza un conjunto que no existe); · contract: ensayo_marzo (ADR-0046 §6 de punta a punta sobre un repo SINTETICO y con la CLI real: tramo sin sha, sorteo con la regla de cupos REAL de 2026-03 y solo dias de marzo aunque mayo este cubierto, anclado, el sorteo que no se repite ni con otra semilla ni borrando la carpeta, el huso por velas con la herramienta -velas que cambian cada minuto para que la prueba distinga-, la declaracion con el sha atado al tramo y la herramienta como control, `casos ingerir --artefacto` con la CENTINELA en las filas reservadas, y el artefacto que se sigue reproduciendo); unit: huso_por_velas (ADR-0039 §5 hecho herramienta, sobre datos SINTETICOS y en verde ANTES del control real: las cifras y los husos de §5 salen de `criterio_huso.yaml` y el script no lleva ninguno escrito -AST-, criterio estricto sin cifra por defecto, margen inclusivo y minuto hacia abajo, vela ausente en el total, los dos umbrales inclusivos y NO CONCLUYENTE si los dos husos salen altos, la fila de frontera descartada con solo un booleano, el libro sintetico con centinela que da el huso de sus velas, el control que coincide o para, y sin formato o sin dias `dev` no se mide); contract: ingesta_fidelidad (ADR-0046 §7, `casos ingerir --artefacto`: abre los `fidelidad-dev` de un artefacto sorteado, anclado y commiteado con una CENTINELA en las filas reservadas que no sale ni por stdout, ni por stderr, ni en los ficheros escritos, y la centinela viva -pedido a proposito, el dia reservado rompe la ingesta sin reproducirla-; sin `--artefacto` lo de antes; sin sorteo, sin ancla, sin commit, con el reparto mutado despues del ancla, con el libro de otro mes, con un id sin mes y sin ningun `dev`, se niega sin escribir); unit: fidelidad_marzo (ADR-0046 sobre repos sinteticos: la regla de cupos desde N -N = 0 se niega, N = 1, 2, 3 y 20 explicitos, la regla real de 2026-03 igual a la del consultor de 1 a 40, una regla mal formada o que no reparte los N no carga-, el kit no admite `cupos_por_mes`, un id sin mes no se sortea, el artefacto de un mes no contiene ningun dia de otro, la regla decide los cupos y queda en particiones, el sorteo no se repite nunca -ni con otra semilla, ni borrando la carpeta commiteada, ni con ancla-, y septiembre se recompone igual con el filtro por mes); a35_fotogramas (los fotogramas de A-35 sin abrir ninguno real: la lista cerrada son las ventanas de los segmentos con el fotograma citado dentro, fuera de ella no se lee nada, un PNG que no es el de F05 se rechaza y el recuento de pixeles distintos); buscar_a35 (la lista cerrada de A-35 sin palabras sueltas de uso constante, sus controles positivos -v4 #846, #849 y #836-, el conjunto de A-24 intacto y la CLI que rechaza un conjunto que no existe); buscar_ambiguedades (la busqueda de A-24, A-21, A-26 y A-34 sin leer ninguna transcripcion: el corte a 180 s con cada trozo listando lo suyo, el trozo sin coincidencias que no se emite, A-18 sin cambios, la lista cerrada sin palabras sueltas de uso constante y los cuatro controles positivos); sesgo_h4 (RN-003 y ADR-0044 sobre velas sinteticas: rompe arriba y el color no decide, rompe abajo, no rompe y se arrastra, equal que no rompe, romper por un punto, rompe ambos y es ambiguo, sin ruptura dentro del tope es insuficiente, cuerpo frente a mecha, sin mirar el futuro, y los cambios de hora de EE. UU. con la H4 de mitad de sesion contando en la siguiente); criterio_fidelidad (el emparejamiento y las metricas de ADR-0043 con operaciones sinteticas: exacto, fuera de tolerancia de entrada y de tiempo, direccion contraria, otra sesion u otro dia, desempate, uno a uno, bot en dia sin trader aparte, cero del bot y cero del trader sin dividir por cero, y el fichero del criterio); instante_llenado (la medida del instante del xlsx sobre velas sinteticas: margen y minuto hacia abajo, sin vela aparte, la regla fijada con el control mandando, y una salida sin precios ni instantes); contract: visto (el reparto dev-visto, ADR-0042: un dia de dev-visto es ingerible, uno oculto no aunque este en el, un mes que no esta en vistos.yaml no entra, sin la lectura completa declarada no entra, y el reparto se recompone y esta anclado); unit: retirados (los dias retirados del holdout, ADR-0041: un retirado no se mide, se oculta y la puerta lo rechaza con autorizacion; sin fichero, medidos = reservados; solo anadir contra el historial; una huella que no es de un reservado falla; una entrada mal formada cierra la puerta; en el repo real 1 retirado y ninguna salida de los comandos que recorren casos imprime su id); a18_buscar (la busqueda de A-18 sobre una transcripcion SINTETICA: las listas cerradas de terminos y de transcripciones, sin mayusculas ni tildes, por palabra y sin casar una cifra dentro de otra, la frase partida entre segmentos, la ventana de 45 s y su union, el formato sin recortar y la integridad contra el manifiesto); v5_criterio (el criterio de lectura de v5 sobre fotogramas SINTETICOS: stop en 0,8 separa hacia riesgo_real, stop en 1,0 hacia caja_completa, sin ancla comun no es valido; y la agregacion por instante y global; la lista cerrada de 36, un nombre fuera de ella falla sin decodificar, y un fotograma o un indice que no son los de F05 se rechazan), viabilidad_comision (las funciones puras de las variantes de A-18 sobre casos SINTETICOS: los niveles de V1 a V4 en compra y en venta con el 0,8 al punto mas cercano, el R nominal, los pips, el coste en R y la celda de la tabla), regression/cuenta_7_de_agosto (la primera regresion: la cuenta del 7 de agosto de construccion suspende por perdida diaria en el tick del pico, 12:30:01.312 UTC, y no antes; necesita los ticks de data/, y sin ellos se salta), cuenta: el orden a igual instante (una marca en el instante del cierre no reabre la operacion, no deja fantasma y cuenta antes del cierre; una operacion que abre y cierra en el mismo instante; una marca en el instante de la apertura va despues de abrir), viabilidad_trader (las funciones puras de la viabilidad del trader sobre casos SINTETICOS: el R de una operacion y su clase, la diferencia grande, el bootstrap con semilla y las estadisticas fijadas, la comision en R y el lote, el veredicto, y que las marcas en el instante del cierre se quitan antes de la cuenta), leer_demo_ftmo (el lector de la demo de FTMO sobre CSV SINTETICOS: la tabla por decision de ADR-0057, el desfase por fecha, un retcode inesperado marcado en la celda y en la lista sin ocultarse, lo que queda abierto y un corte avisados, y un CSV ajeno rechazado), embudo_77 (el embudo de las 77 sobre hechos SINTETICOS: cada paso en el orden del pipeline con su motivo y su detalle, la toma de una sesion anterior cuya zona casa no mata, y la tabla por lectura fijada entera), decodificar_png (el decodificador de `scripts/`: cada uno de los cinco filtros devuelve los pixeles exactos en gris, RGB y RGBA, con un codificador de test escrito por separado; CRC roto, entrelazado y firma ajena se rechazan; solo `zlib` y `struct`), project_state, project_state_rutas, adr, tree, cli, cli_data, valores, velas, registro, ajustes, inventario, evidence, feedback, yaml_estricto, dukascopy, agregacion, agregacion_dst, dataset, golden_ohlc, comun, audio, transcripcion, pipeline_transcripcion, motor_prompt, verificacion, propuestas, fotogramas, retrieval, kit, spec · integration: fotogramas_ffmpeg · contract: import_contracts, no_business_literals, repository_integrity, registro_accessors, evidence_history, feedback_history, data_manifest_history, transcripcion_history, fotogramas_history, golden_citas_f07 (40 referencias contra la evidencia real), golden_consultas_f08 (15 consultas; con y sin `data/`), kit_particiones (guardia de ancestro y ancla de blob del paquete), anterioridad (la prueba POR CASO, con el mutante de la etiqueta anterior a su reparto), hoja_sesion_docx (OOXML valido, citas del paquete, sin fuga de holdout), spec_docs_generados (los cuatro documentos de docs/spec/ salen de knowledge/spec/), documentos_vivos (ningun documento que describa el presente pega un recuento que el CLI ya da), cobertura (el mes sin material se niega POR MES y nunca por dia; los DOS CEROS distinguidos -dia sin operaciones frente a mes sin filas-; cero tramos admitido y la lista de dias aun prohibida), ingesta (F14a: el dia reservado no se ingiere NI SE NOMBRA, el agregado no se lee aunque viva en el mismo fichero, el invariante geometrico aborta nombrando la fila, y el lector no publica el conjunto de fechas ni de columnas; ningun numero de la salida cuenta el libro entero, tampoco la posicion de una fila en un error; el dia de una fila se calcula en el huso de los dias PEDIDOS -la frontera UTC/Madrid en verano y en invierno, en los dos sentidos- y los errores nombran el caso y la comprobacion, nunca el instante ni los precios; y la forma del caso es lista CERRADA en caso, operacion y `fuente`: caza `objetivo`, `maxTP` y cualquier clave que nadie penso), mes_del_material (SIEMPRE DOS repartos -kit con dos meses y fidelidad-: el libro de un mes ingiere solo ese mes; un sha sin tramo o fuera del manifiesto del corpus es error sin escribir; el libro CORRECTO de septiembre no mete ni un dia de fidelidad, y se dice; un tramo SIN sha es material que este comando no lee), libros (ADR-0039: cada formato se lee con su declaracion y con ninguna otra; sin declaracion o con una ajena no se lee; el registro es SOLO ANADIR contra el historial y se cruza con `cobertura_material`; un XML roto no publica su posicion en la hoja), ids_citados (todo id citado en `docs/**`, `CLAUDE.md` y `PROJECT_STATE.md` existe o esta declarado en su documento con motivo; el declarado que existe, el no citado fuera de su bloque, el que solo aparece en su bloque y el sin motivo fallan; lo que no es id para FUENTE se ignora, y una valla sangrada 4 espacios es codigo y no abre bloque; cada tipo de fallo con su prefijo, comprobado por mensaje exacto), regla_mes_sin_filas (por la CLI: el libro atado al tramo de otro mes lo para la regla; los dias pedidos sin filas en el libro correcto dan el mismo error, coste aceptado; todos reservados no llega a leer ni nombra dias; un huso que saca todas las filas del mes lo caza la regla) · 4 contratos import-linter KEPT · mypy strict OK (src + tests)

## Architectural Decisions (index)
- ADR-0001 estructura del repositorio y regimenes de cambio — ACTIVE
- ADR-0002 registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta — ACTIVE
- ADR-0003 hooks copiados desde scripts/git-hooks; sin framework pre-commit — ACTIVE
- ADR-0004 categorias de parametro y horas con huso — ACTIVE
- ADR-0005 datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje — ACTIVE
- ADR-0006 capas revisadas, paquete `comun` y accesores del registro por tipo declarado — ACTIVE
- ADR-0007 transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario — ACTIVE
- ADR-0008 fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable — ACTIVE
- ADR-0009 verificacion mecanica de citas contra la cruda y propuestas de evidencia trazables y selladas — ACTIVE
- ADR-0010 busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente — ACTIVE
- ADR-0012 el registro despues de la sesion 1: tipos nuevos, ausencia de valor, categorias y el reloj del trader — ACTIVE
- ADR-0013 StrategySpec: reglas que nombran parametros y nunca los contienen, y un hash que cubre lo que el bot hace — ACTIVE
- ADR-0011 kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback — ACTIVE (el esquema de ambiguedades gana DECIDIDA en ADR-0022)
- ADR-0014 la base sobre la que se mide el objetivo: `base_calculo_objetivo` — ACTIVE (enmendado por ADR-0020)
- ADR-0015 los relojes tras la auditoria: el del grafico es un default, y el dia de riesgo necesita el suyo — ACTIVE (enmendado por ADR-0020 y por ADR-0027: con FTMO el dia de riesgo es el civil del trader)
- ADR-0016 de donde sale cada regla: el campo `decision`, y un hash que cubre lo que un humano lee — ACTIVE
- ADR-0017 el reloj del trader es su reloj civil: se revierte ADR-0012 y se confirma ADR-0005 — ACTIVE
- ADR-0018 la precedencia va por clase, no por orden del fichero; y los siete defectos que eso destapo — ACTIVE
- ADR-0019 la forma ejecutable de una regla: predicados con argumentos, ligadura, y cuatro cosas con nombre (cinco desde que la auditoria de cierre de F12 anadio `efectos`) — ACTIVE
- ADR-0020 la base del lotaje es la distancia hasta el stop, no la caja completa — ACTIVE
- ADR-0021 que cuenta como abrir un holdout, y que se hace con la exposicion de mayo — ACTIVE
- ADR-0022 el bot no opera noticias en la cuenta fondeada, y una ambiguedad puede cerrarse por decision — ACTIVE (con enmienda del 2026-09-14: con FTMO Swing el bot SI opera noticias; `filtro_noticias` vuelve a `no`, RN-028 DESCARTADA; el estado DECIDIDA sigue en pie)
- ADR-0023 el registro de feedback sabe cuando llego cada respuesta y por donde (`recibido_el`, `procedencia`) — ACTIVE
- ADR-0024 la ventana no se amplia a Nueva York (A-15 DECIDIDA), y la referencia para medir la fidelidad es Dukascopy (A-23 nace DECIDIDA; A-16 se parte y conserva la medicion, que sigue ABIERTA) — ACTIVE
- ADR-0025 el reparto de mayo no se toca: 6 dias `dev` y 13 de holdout (6/4/3), junio sale del universo de F14 y los cupos de `config.yaml` se quedan quietos — ACTIVE (su DECISION sigue; su ARGUMENTO -que tocar los cupos rompia la comprobacion entera- caduco con la enmienda de ADR-0035 del 2026-09-21, y lleva nota)
- ADR-0026 la prop firm es FTMO, reto 2-Step, tipo de cuenta Swing: topes de la firma como parametros `firma_*`, RN-029 (prohibe y detiene) y RN-030 (cierra solo con posicion viva), el mas restrictivo manda, A-17 DECIDIDA, los parametros del instrumento a default bajo A-27 y el reloj del servidor a UNKNOWN bajo A-28 — ACTIVE
- ADR-0027 los relojes con FTMO: el dia de riesgo es el civil del trader (medianoche CE(S)T), desaparece el tercer reloj y A-19 queda DECIDIDA — ACTIVE
- ADR-0028 el reloj del motor: fase de riesgo por tick sobre equity, estrategia al cierre de M1, ordenes por evento, punto fijo con refraccion y hechos del broker derivados — ACTIVE (con nota del 2026-09-16: el punto 5 ya esta aplicado a la spec y el 4 lo precisa ADR-0032)
- ADR-0029 lado del precio y redondeo: geometria en BID (sin verificar que FX Replay dibuje BID), llenado por direccion, al mas cercano con empate en contra del bot, lote a la baja — ACTIVE
- ADR-0030 el motor interpreta la `forma` y despacha por nombre a primitivas escritas a mano; F18-F22 son primitivas, no modulos sueltos — ACTIVE
- ADR-0031 el freno de la firma dispara antes del limite: `firma_margen_seguridad` (0,5, validado por el consultor el 2026-09-17) y lectura prospectiva en RN-032; el tope del trader no cambia de lectura — ACTIVE
- ADR-0032 de donde sale cada hecho y cada evento (`origen: broker`, `fuente`, `lo_provoca`, `efecto`, `valores`, claves cerradas) y como nace la orden limite (RN-011 prepara, RN-015 coloca); precisa ADR-0028 §4 — ACTIVE
- ADR-0033 la guarda y la puerta del holdout: que vigilan, por donde se abre y como se autoriza -hook de auditoria para cualquier llamante en los tests, puerta `botsito.cases.holdout` para lo que abre (ficheros y valor de etiquetas de casos reservados) con autorizacion commiteada y PREREGISTRO relleno, y las velas declaradas y no bloqueadas- — ACTIVE (con enmienda del 2026-09-21: la autorizacion CITA la pregunta que abre, gastarla cierra todas las autorizaciones vivas, `abrir` sigue pura y el id de pregunta se compara; `casos_reservados` grita ante un reparto ilegible y el lector decide sobre la ruta resuelta)
- ADR-0040 la combinacion CONFIRMED del objetivo -`caja_completa` con `stop_fraccion_caja` 0,8- es FALSA: la region [3,00 , 3,75) que predice vacia esta poblada en agosto (15 de 18), abril (7 de 15) y mayo (4 de 5); siguen abiertos los dos supervivientes, (riesgo_real, 0,8) y (caja_completa, 1,0), que solo separaria un material que traiga la caja; A-18 ABIERTA y no bloqueante; ningun parametro cambia — ACTIVE
- ADR-0041 un dia reservado expuesto sale del holdout y no se sustituye: deja de MEDIRSE y sigue OCULTO (la puerta lo rechaza siempre); vive en `knowledge/cases/retirados.yaml`, solo anadir y por la huella del id; `casos_medidos` y `casos_ocultos` separan lo que mide de lo que oculta; el reparto no se toca — ACTIVE
- ADR-0042 material ya visto entra por un reparto dev-visto, sin sorteo y sin holdout: solo si el mes esta en `vistos.yaml`, su lectura completa esta declarada y `cobertura_material` le da un tramo con su libro; todo `dev`, recompuesto desde la cobertura y anclado; la puerta aplica «ocultos» tambien aqui — ACTIVE
- ADR-0043 criterio de fidelidad en desarrollo: la operacion como unidad; empareja dia, sesion y direccion con |Δentrada| <= 3 puntos y |Δinstante de llenado| <= 15 min, uno a uno; cobertura y precision, lo del bot en dias sin trader aparte; stop, TP, resultado y gestion fuera; construccion abril y agosto, medida mayo; umbral de desarrollo 70 % y 60 %; no se cambia tras la primera salida sobre la medida sin un ADR nuevo — ACTIVE
- ADR-0044 el sesgo H4: si la vela rompe los dos extremos es AMBIGUO (A-34); sin ruptura en `sesgo_h4_tope_velas` es INSUFICIENTE; con los dos no se opera; se fija al abrir la sesion con las H4 cerradas por su hora de fin; romper es superar por poco que sea — ACTIVE
- ADR-0045 la liquidez de M15 es el pivote MAS RECIENTE YA FORMADO (decide A-24, no la resuelve: falta el registro del trader); cuando esta formado es A-35, abierta y bloqueante de RN-004 — ACTIVE
- ADR-0046 marzo entra por el camino de fidelidad, con sorteo y la misma puerta: lo que caiga en `fidelidad-2` y `fidelidad-3` queda oculto y su `fidelidad-dev` es medicion de desarrollo con mayo; cupos por regla desde N fijada antes de ver el mes; el artefacto se limita al mes de su id; el sorteo no se repite nunca; orden de entrada a-e con la excepcion acotada a ADR-0039 §1 (solo la columna de fechas, una vez, por Aleks); enmienda ADR-0025 §5 y aclara ADR-0043 — ACTIVE
- ADR-0047 la unidad de comparacion es la operacion tambien en el holdout: cuando se rellene el PREREGISTRO sera la de ADR-0043; el PREREGISTRO no se toca ahora; la gramatica del kit en (caso, sesion) queda como deuda, con 0 LABEL_CASE; motivo, la auditoria del 2026-09-13 ([47]): por sesion no se comparan el segundo y el tercer cartucho — ACTIVE
- ADR-0048 el arnes del motor: COMPLEMENTA a ADR-0030 (no sustituye ni enmienda nada); envuelve al interprete del arbol generico; NO_IMPLEMENTADA por PRIMITIVA, que vale DESCONOCIDO (logica de Kleene) y no produce hechos ni operaciones; la unidad de ejecucion es el DIA, con el estado cruzando sus dos sesiones y lo de A-39 PROVISIONAL; el informe por (dia, sesion) y operacion; embudo sobre el grafo de hechos; solo sobre construccion y por la compuerta; seis huecos de interpretacion registrados (H1-H6) — ACTIVE
- ADR-0049 los huecos del arnes: COMPLEMENTA a ADR-0048; H1 opcion (c): `ambiguo` e `insuficiente` son valores del hecho `sesgo`, RN-003 usa `sesgo_h4_al_abrir` (nombra `sesgo_h4_tope_velas`, cubre la busqueda hacia atras) y RN-033 prohibe con ellos; cada sesion produce su propio sesgo y no hereda; el nodo `hecho` admite `vale` (amplia ADR-0019); `sesgo_h4_tope_velas` sigue CONFIRMED porque el registro no tiene estado PROVISIONAL; H2 (a): test de que las sesiones de `config.yaml` cubren [ventana_inicio, ventana_fin) y A-43; H3 (b)+(c): invariancia al orden y aviso de empates; H4: gate DESCONOCIDO estricto, intravela pesimista por OHLC hasta tener ticks, broker y cuenta en el simulador; H5 (a): `permite` nunca levanta un `prohibe`; H6 (c) PROVISIONAL: estrategia de cero cada dia, cuenta persistente en el simulador, lo demas pendiente de A-25, A-30 y A-38 — ACTIVE
- ADR-0050 el simulador, la capa de cuenta: las cuatro decisiones del consultor del 2026-09-25 (objetivos y dias minimos; comision y swaps dentro de la equity vigilada; volumen y limites de ordenes como `firma_*`; guardia de AVISO de tamano de posicion); H4 y H6 de ADR-0049 (la cuenta persiste entre dias, el gate DESCONOCIDO sigue estricto); estrategia, instrumento y perfil de cuenta son capas separadas y una firma nueva es un perfil nuevo en `knowledge/cuentas/` con el formato del registro, nunca codigo; lo NO ENCONTRADO queda UNKNOWN y el simulador se niega a correr si lo necesita; la capa de cuenta son funciones puras (`engine/cuenta.py`) y NO se cablea al motor: el contrato con `perdida_dia_firma` y `perdida_total_firma` queda descrito y pendiente del broker — ACTIVE
- ADR-0051 el modelo de llenado, ACEPTADO por el consultor el 2026-09-26 tras la sesion nocturna: a que lado del spread se compara cada orden (compra al ASK, vende al BID); limites y objetivos exigen pasar ESTRICTAMENTE el nivel y los stops saltan al toque (DN-1); con ticks el orden real y, si un tick cruza stop y objetivo a la vez, el stop (DN-2); respaldo con solo M1 pesimista, el stop primero (ADR-0049 H4), marcado `respaldo_m1`; sin deslizamiento fijo (DN-3, PROVISIONAL hasta la demo en MetaTrader); spread de cada tick con ticks y, sin ellos, el percentil 90 por hora medido en construccion (DN-4) en knowledge/simulador/llenado.yaml; DN-5 (ticks solo de dias dev y horas 05-13 UTC) aceptada para verano, la ventana de invierno 06-14 UTC pendiente y ligada a A-42; y §8, EL HALLAZGO: el desenlace difiere entre ticks y respaldo M1 en una fraccion grande de las operaciones, asi que los TICKS SON OBLIGATORIOS para toda simulacion que cuente (construccion, medicion y holdout) y el respaldo solo sirve para depurar — ACTIVE
- ADR-0052 el broker simulado, ACEPTADO por el consultor el 2026-09-26 tras la sesion nocturna: ciclo de vida colocada/modificada/llenada/cancelada/expirada y rechazada por limite del perfil (volumen, ordenes simultaneas, posiciones por dia) con el rechazo registrado; posicion con stop y objetivo cerrada por stop, por objetivo o a mercado; cada evento lo decide el modelo de llenado de ADR-0051; la cuenta recibe cada cierre con comision por lado, swap por corte diario del huso del perfil (DN-6, PROVISIONAL hasta medir el corte en la plataforma, A-28) y las MARCAS del peor precio por minuto, y su equity es el saldo mas el flotante del broker en cada marca; los hechos `operacion_abierta` y `orden_limite_pendiente` salen del broker; NO se cablea al motor y el contrato que el motor tendra que cumplir queda escrito en §5 — ACTIVE
- ADR-0054 RN-004 y RN-020 listas para activarse con la respuesta del trader, ACEPTADO: los selectores de A-35 y A-44 son parametros UNKNOWN y sin fijar el motor se niega, salvo en modo diagnostico rotulado; el tope del trader con tres estados (sin fijar, sin_tope, valor) e independiente de la firma; la correccion del cableado del selector; la granularidad de la toma de RN-004 PROVISIONAL ligada a A-45; y el silenciado de los empates entre gates que solo prohiben — ACTIVE
- ADR-0055 RN-011 y la zona de entrada, ACEPTADO: los predicados del motor son puros; el selector de «limpia» (A-21) PROVISIONAL; el veredicto de VERIFICACION-A21 (6/77 dentro, 7/77 con tolerancia, 38/77 sin zona viva); la incoherencia RN-008/RN-009 frente a RN-011 con una toma de otra sesion, como deuda ligada a A-46; y la guarda de 259 caracteres con las etiquetas cortas del diagnostico — ACTIVE
- ADR-0056 la entrada con la ruptura, ACEPTADO por el consultor el 2026-09-28 sobre DISENO-ENTRADA-RUPTURA.md: RN-011 con orden stop preparada con selectores UNKNOWN al patron de ADR-0054 (entrada_tipo_orden ligado a A-47, con --diagnostico-a47; stop_inicial, stop_paso_a_0_8 y lotaje_distancia; caja_bloque y caja_vela para A-48 y A-49); la orden stop del broker salta al toque y se llena al precio del tick mas DN-3, PENDIENTE DE MEDIR EN LA DEMO; la pendiente mal colocada se RECHAZA (precio_invalido), PROVISIONAL hasta la demo de FTMO; la caja por operacion solo con la orden stop y la linea base de la limite identica byte a byte en cada rama; la vida de la orden stop -nace en el posible punto de breaker antes de la ruptura (tercera lectura de A-29, al_aparecer_punto_de_breaker) y se mueve con el por el mecanismo de RN-006-, con la lectura de RN-008 y el diagnostico de A-29 PROVISIONALES; en_formacion NO_IMPLEMENTADA y ADR-0028 sin tocar; cinco ramas de codigo en orden (broker; selector de A-47; vida de la orden stop; caja por operacion; stop y lote). Enmienda 0020, 0051, 0052 y 0053 y supersede en parte 0055. Nada se resuelve ni se fija.
- ADR-0057 ordenes stop y rechazo de pendientes en el broker simulado, PROVISIONAL hasta la demo de FTMO (rama trabajo/broker-ordenes-stop, rama 1 de codigo de ADR-0056): la stop de entrada salta al toque y se llena al precio del tick que la dispara mas DN-3, con hueco peor que el nivel y el deslizamiento guardado en la posicion; lado equivocado estricto (el nivel exacto pasa); la pendiente del lado equivocado se RECHAZA (precio_invalido), tambien al modificarla, juzgada con el ultimo tick o la ultima M1 cerrada; stops level del broker = firma_stops_level_puntos, UNKNOWN en el perfil (R11, A-27), distinto de instrumento_stops_level de la estrategia: sin valor la stop no se coloca y la limite no se juzga por el; --diagnostico-a27 etiquetado. La estrategia no cambia.
- ADR-0058 el selector de A-47 en la rama 2, PROVISIONAL (rama trabajo/selector-orden-stop): entrada_tipo_orden (stop_en_ruptura | limite_en_retroceso) UNKNOWN con --diagnostico-a47, exigido solo con --simular y antes de leer velas; con stop_en_ruptura la orden stop va al 0 de la caja en el cierre del breaker, el mismo instante que la limite, porque el instante propio de la stop es la rama 3 (enmienda ADR-0056 §1 y su fila 2 de §8); el bloque y el momento, los de hoy (A-48 y A-49 sin selector hasta la rama 4); con limite_en_retroceso la corrida sale como main.
- ADR-0059 A-42, PROVISIONAL (rama trabajo/activar-sesion-03, decision del consultor tras la sesion 3, opcion (a)): la lectura es que las sesiones 07-11 y 11-15 van fijas en el reloj del grafico, UTC+2 todo el ano (06:00-14:00 de Madrid en invierno); huso_operativa NO cambia, porque en el motor es tambien el reloj del dia de riesgo (ADR-0053 §4) y cambiarlo rompe el invierno; separar los dos relojes es rama de codigo y requisito previo de toda corrida de invierno; recuadro en ADR-0017; A-42 sigue ABIERTA y bloqueante.
- ADR-0060 ACEPTADO por el consultor el 2026-09-30, con sus decisiones nocturnas (sesion nocturna, rama trabajo/nocturno-01oct, F32): con la doble ruptura el sesgo es el del color con que cierra la vela H4 (A-34 RESUELTA; enmienda ADR-0044 §1) y solo sin cuerpo sigue `ambiguo` (DECISION NOCTURNA); `insuficiente` se conserva; RN-002 cierra cuando a la vela H4 en curso le queda `cierre_h4_antelacion` o menos -parametro nuevo, con la cifra del trader-, por el predicado `vence_vela_h4` sobre la rejilla de `anclaje_h4`, tambien en el propio limite (DECISION NOCTURNA), con `ventana_fin` sin tocar; no retira la orden pendiente (A-39, A-30) — ACTIVE
- ADR-0061 ACEPTADO por el consultor el 2026-09-30, con sus decisiones nocturnas; enmienda ADR-0029 §3 para el redondeo del stop, y la decision 8 (un punto, no un pip) queda tambien como pregunta para la sesion 4 (sesion nocturna, rama trabajo/nocturno-01oct, F34): la forma de RN-011 nombra `stop_fraccion_redondeo` y el motor redondea la distancia al stop alejandose de la entrada, al punto siguiente (DECISION NOCTURNA: «lo minimo posible» es un punto, no un pip entero); y el break even de RN-014 deja de ser un hueco: `se_completa_zona_de_control` con `posterior_a` es el retroceso de M1 posterior a la entrada, completado cuando una M1 pasa el punto extremo que dejo (DECISION NOCTURNA sobre la geometria), evaluado al cierre de M1 y no al tick; RN-006 sigue sin escribirse — ACTIVE
- ADR-0062 ACEPTADO por el consultor el 2026-09-30, con sus decisiones nocturnas (sesion nocturna, rama trabajo/nocturno-01oct, F34, en commit propio para poder revertirlo solo): la toma de RN-004 la hace una vela de M1 que cierra con cuerpo (A-45 RESUELTA), y cierra lo PROVISIONAL de ADR-0054 §4; A-43 no se activa. HALLAZGO MEDIDO en diagnostico sobre construccion: con la toma antes, el productor -un esquema por sesion- encuentra menos esquemas y la cobertura baja de 2 a 0 de 77; no se revierte porque la lectura la elige el trader, y lo que falta es la caja por operacion y la vida de la orden stop (ADR-0056 §4 y §7) — ACTIVE
- ADR-0063 ACEPTADO por el consultor el 2026-09-30, con sus decisiones nocturnas (sesion nocturna, rama trabajo/nocturno-01oct, F36): el reloj de las sesiones se separa del reloj del dia de riesgo con el selector `reloj_sesiones` (`civil_operativa` o `grafico`; el huso de cada reloj sigue en `huso_operativa` y `huso_grafico`), que nace en `civil_operativa`, DEFAULT_AMBIGUOUS bajo A-42: es el mecanismo que ADR-0059 pedia y NO cambia ningun comportamiento -el arnes, simulado y sin simular, sale identico byte a byte-; A-42 sigue ABIERTA, y antes de ingerir un mes de invierno con el selector en `grafico` hay que decidir con que reloj asigna el kit la sesion de las operaciones del trader — ACTIVE
- ADR-0064 ACEPTADO en su direccion por el consultor (rama feature/F35-orden-stop-pivote, la vida de la orden stop de ADR-0056 §7 con la caja por operacion): la orden stop nace tras la toma en el posible punto de breaker que dice `orden_stop_punto` (`ultimo_pivote_m1`, el de R5, por defecto; `referencia_de_la_toma`, para comparar), con la caja de `caja_bloque` (`r6` por defecto; `r4`, `r1`), y RN-006 la cancela y RN-011 y RN-015 la recolocan en cada punto nuevo con caja, stop y lote recalculados; RN-008 no frena la colocacion (lo PROVISIONAL de ADR-0056 §7, escrito); `orden_limite_nace` pasa a `al_aparecer_punto_de_breaker`; los tres DEFAULT_AMBIGUOUS (A-29, A-48); seis DECISIONES conservadoras en §4 — ACTIVE
- ADR-0065 el break even de RN-014 al tick (rama feature/be-al-tick, PROVISIONAL hasta la demo de MetaTrader): el stop pasa a la entrada en el primer tick cuyo BID pasa el nivel de activacion -el mismo punto de `zona_posterior_completada`-, no al cierre de la M1; vigilar no es peticion y mover el stop si; en el mismo tick manda lo que ya hay y el stop nuevo cuenta desde el tick siguiente; sin ticks, con `cierre` o con el criterio `cuerpo`, al cierre de la M1 y marcado en la traza — ACTIVE
- ADR-0053 el cableado del simulador, ACEPTADO por el consultor el 2026-09-26 con todas sus decisiones PROVISIONALES y dos para revisar (2.1, los eventos del broker llegan al cierre de M1, se revisa con la demo de MetaTrader; 5.1, el cierre de RN-030 al precio de cierre de M1, se revisa al implementar RN-030); abre A-44, el siguiente bloqueo del bot despues de A-35: las acciones de la spec se traducen en peticiones al broker sobre una orden en preparacion (el lote se resuelve al colocar, con el stop ya escrito; la ligadura OP es la unica posicion viva; la zona Z es una ligadura de texto a una Zona del contexto); los eventos del broker vuelven como hechos de origen broker y como predicados de fuente broker, entregados en el siguiente cierre de M1; la capa de cuenta viva alimenta perdida_dia_firma y perdida_total_firma recortados en cero (lo que ADR-0050 §5 dejo pendiente) y la primitiva del acumulador distingue alcanza_tope, se_acerca_al_limite y no_cabe_la_operacion por sus argumentos; UN solo reloj, el del perfil, comprobado contra huso_operativa; las tres fases de ADR-0028 por minuto (riesgo por tick en el broker, eventos, estrategia al cierre de M1); ticks obligatorios y respaldo M1 solo con --depuracion marcado; solo construccion por la compuerta; huecos con nombre: perdida_dia y perdida_semana sin magnitud ni corte (A-44), cartuchos, y la geometria de A-29 y A-35 — ACTIVE
- ADR-0039 ningun libro de backtest se lee sin su formato y su huso declarados en `knowledge/corpus/libros.yaml`, atados a su sha y a la medida que los sostiene; registro SOLO ANADIR y cruzado con `cobertura_material`; la medida por velas con control (>= 90 % / <= 50 %) es EL procedimiento para declarar un libro nuevo — ACTIVE
- ADR-0038 un fotograma se abre por instante localizado -transcripcion, item de evidencia o marca de tiempo- y nunca por muestreo; un agregado visto asi se declara el mismo dia con sus cifras y ninguna se usa — ACTIVE
- ADR-0037 la granularidad del dato decide que se abre, no el tipo de fichero: lo atribuible a un dia se abre para ese dia si no esta reservado; lo que AGREGA sobre un rango con dias reservados no se abre NUNCA y ninguna autorizacion lo abre; la estructura se VERIFICA contra una lista escrita antes y no se lee; y el conjunto de FECHAS del fichero no se publica. Distingue lo que se VE (ADR-0021 §2, vigente) de lo que se LEE A PROPOSITO, y NO reclasifica ninguna exposicion ya declarada — ACTIVE (con correccion del 2026-09-21 sobre su decision 7: el objetivo no es `idealTP` ni `maxTP`, es la regla `objetivo_rr`)
- ADR-0036 el material ya visto se reparte por su propio camino, con nombres propios y con puerta: `knowledge/cases/fidelidad/` no es el kit -sin cuestionario, sin hoja, sin sesion y con el filtro de `vistos.yaml` saltado A PROPOSITO-, `cobertura_material` acota con motivo propio y SOLO por tramos -declarar dias cubiertos publicaria etiquetas-, las particiones `fidelidad-*` pasan por la MISMA puerta (ADR-0033) y la anterioridad se prueba POR CASO. Lo que promete es anterioridad demostrable, NO una cifra con potencia — ACTIVE
- ADR-0035 el universo de un paquete se congela en el paquete: comprobar va por la lista, construir por el disco — ACTIVE (con enmienda del 2026-09-21: los CUPOS tambien salen del bloque `config:` congelado, la guardia que comparaba contra `config.yaml` pasa a AVISO de deriva en `validar_paquetes`, y `anclas.yaml` ata `ventanas.yaml` y `particiones.yaml` por el sha de su BLOB -patron de `preregistro_blob`, ADR-0033-, sin depender de que existan etiquetas)
- ADR-0034 septiembre es material ETIQUETADO de un mes que el trader ya ha visto — ACTIVE

## Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

## Expert Entry Points
- Sesión 1 (tras F10+F15): 3 preguntas bloqueantes + ronda 1 de etiquetado <!-- cifra-congelada: la sesion 1 ya se celebro y su paquete esta commiteado --> · CELEBRADA el 2026-09-09 (v6, 2 h 27 min) y procesada; informe `docs/validation/SESION-01-2026-09-09.md`
- Sesión 2 (tras F26): discrepancias + ronda 2 (κ) · pendiente
- Sesión 3 (tras F32): divergencias de ejecución · pendiente
- Mensual (F34): discrepancias en vivo · pendiente

## Lineamientos recibidos del usuario y hechos del corpus (evidencia en F07)
Dos fuentes distintas, separadas a proposito: (a) lo que el usuario (consultor) aporta por escrito
sobre la operativa (lineamiento, NO es evidencia ni feedback del trader) y (b) hechos leidos en el
corpus (crudas y fotogramas). Desde F07 (2026-09-07) todo hecho del corpus tiene un item en
`knowledge/evidence/` (id `ev-*` anotado aqui; la cita se verifica contra la cruda o el fotograma);
las reglas se infieren en F11, no aqui.

### (a) Lineamientos del usuario

- **2026-09-04 · Geometria del riesgo y gestion del stop.** "Se traza un 1:3 inicialmente; con eso
  se calcula el lotaje y todo. Una vez se mete la operativa, se baja el SL hasta el 0,75 del trade
  o hasta el 0,8; el TP sigue donde estaba inicialmente."
  - Estado en el plan: CONTEMPLADO. MASTER_PLAN F21, que desde ADR-0020 (2026-09-11) dice: el
    stop lo fija `stop_fraccion_caja`, el objetivo `objetivo_rr` sobre `base_calculo_objetivo` y
    el LOTE la distancia HASTA EL STOP (`lotaje_base: hasta_stop_fraccion`). Esta linea le
    atribuia "lotaje sobre la distancia completa" y "stop en 0,75", que es lo que el plan decia
    ANTES de esa decision -o sea, citaba una fuente viva por un contenido que ya no tiene-.
    Y la investigacion (tres confirmaciones aritmeticas: ratio 4,08/3,94 = 3/0,75; Excel con -0,75).
  - Citas del corpus re-citadas en F07 (evidencia): V2 0:31:42-0:33:53 `ev-v2-003142-beb4ad3c`
    (stop en 0,75), `ev-v2-003256-0197f4e1` (el objetivo sigue en 1:3), `ev-v2-003336-fc210a05`
    (lotaje sobre la distancia completa), `ev-v2-003350-dbd9e3ad` (una ganadora acaba en 3,25);
    V1 0:06:20 `ev-v1-000620-0f7dea14` (cuadro de Gann en 0,75 apenas se genera la entrada);
    V4 0:08:35-0:09:09 `ev-v4-000835-782cf2cc` (respiro de 0,75 a 0,80 por el spread),
    `ev-v4-000858-4e50f00c` (mas respiro con noticias), `ev-v4-001207-0c4ffd4b` y
    `ev-v4-001221-1e66b5fd` (0,75 desplazado segun el spread del momento).
  - Lectura: el 0,8 es el colchon de spread sobre el 0,75, no un nivel alternativo libre.
  - Hallazgo F04 (2026-09-05, large-v3): en V1 0:15:59 el trader dice "ya ha pasado mas del 50%
    de la vela" (la transcripcion heredada decia 40 %) y en V1 0:16:51 "de pasar de 0.75 es a
    0.50". La cifra 40 % frente a 50 % es la ambiguedad A-12 (sesion 1). Evidencia:
    `ev-v1-001557-1dd16e5c` (50 % de la vela) y `ev-v1-001643-47673889` (de 0,75 a 0,50).
  - Preguntas abiertas para el trader (sesion 1): (a) ¿el 0,8 es fijo o "0,75 mas el spread del
    momento"? (b) ¿el stop se coloca en el 0,75 al enviar la orden limite o solo tras el llenado?
    Para el bot es equivalente y mas seguro adjuntar el SL al 0,75 en la propia orden pendiente
    (F22/F31); confirmar que el trader no ve inconveniente.
  - Consecuencia para F21: el TP nunca se recalcula al mover el SL (invariante a probar).
  - Material del 2026-09-05 (v5, `tr-v5-large-v3-int8-float16-01a1ae03`, reemplazada el 2026-09-06 por `tr-v5-...-3c6fbb57`, donde la frase esta en 0:03:12-0:03:35): 0:03:21 "si yo protejo a
    0.80, que es el SL por defecto"; 0:04:44 "el calculo del RR en base al 1 %"; 0:04:56 "todo lo
    backtestee buscando el 1:3... posibilidad de amplificar a 1:4, lo veremos mas adelante"; la
    caja en pantalla (`fr-v5-718ecabb/240000`) tiene el nivel 0,8, no 0,75. Refuerza la pregunta (a)
    de A-10. Evidencia (F07): `ev-v5-000312-f5062062` (0,80 SL por defecto; contradiccion
    mecanica `stop.nivel` con `ev-v1-000448-346d6d90` y `ev-v2-003142-beb4ad3c`, 0,75),
    `ev-v5-000219-bc86af3d` (a veces no llega hasta el 0,80), `ev-v5-000442-b13610fa` (RR sobre
    el 1 %), `ev-v5-000456-dfb95b24` y `ev-v5-000515-02b5bc7a` (1:3 con 1:4 abierto). No se
    decide aqui.
### (b) Hechos del corpus, ya como evidencia (F07, 2026-09-07)
- **Obligatorios de F05 (pantalla):** Excel de abril V3 0:28:56 `ev-v3-002856-bff84636` (2,83 /
  -0,75 / 3,3; `fr-v3-982da728/1736000`); ratios 4,08 / 3,94 V2 0:33:21 `ev-v2-003320-a736fd37`
  (`fr-v2-c5a09508/2001000`); caja 0,75 = 1,19537 V4 0:12:30 (items de la caja en pantalla del
  tramo V4 0:05-0:15: `ev-v4-000813-c916eac6` nivel de entrada 1,19502 y `ev-v4-001221-1e66b5fd`,
  modalidad ambas, caja 0,75 = 1,19537).
- **Candidatos A-9 (reloj del grafico):** V3 0:01:36 `ev-v3-000136-6160fcea` ("configurado como
  UTC mas 2", Madrid). Ningun fotograma muestra la hora de apertura de una H4: el golden H4 sobre
  F15 pasa a F10 (decision del usuario 2026-09-07).
- **Ficha de reglas en Word (V3 0:01:38, `fr-v3-982da728/101000`):** `ev-v3-000138-567dc5d7`
  (ventana 07-15), `ev-v3-000138-8399c18a` (sesgo por la H4 previa cerrada),
  `ev-v3-000138-fc8f7905` (limite estricto de 2 cartuchos); lecturas confirmadas en
  `ev-v3-004817-f2dfb955` y `ev-v3-005735-f24a4bdf`.
- **V4 1:28:20 (riesgo por operacion):** `ev-v4-012815-2aa13700` (0,40 o 0,50 escalado sobre la
  cuenta) y `ev-v4-012733-0c8d7f1f` (racha de 7 perdidas: 0,5 -> 3,5 % de drawdown).
- **2026-09-05 · Reentrada tras un "igual" (equal) y descarte por flujo de ordenes** (v5; evidencia
  `ev-v5-000038-6570a65f`, `ev-v5-000246-17eff9e1`, `ev-v5-000527-c56ebe45`,
  `ev-v5-000427-f8d5d36d`; sin inferir regla): 0:00:39 "no hay entrada porque no me genera el esquema 2 de entrada,
  sino que genera un flujo de ordenes, esa entrada queda descartada"; 0:01:56-0:02:58 "el precio
  llega, activa la entrada y se regresa... cuando hay un equal que no lo vamos a poder anticipar...
  contarlo como perdida, pero reentrar nuevamente si el precio te llega a romper nuevamente esta
  zona"; 0:05:27 "como esto es un igual... esperariamos a que el precio rompa por arriba para la
  reentrada". Relacion: A-7 (stop del segundo esquema), A-2 (cartuchos: la reentrada consume uno?),
  A-4 (BE "cuando se cumplen las condiciones"). Preguntas candidatas para la sesion 1.
- **2026-09-05 · Backtest de abril 2026** (`Material adicional/backtesting-analytics ABRIL 2026.xlsx`
  y 6 capturas de Analytics): 38 operaciones, 17/19/2, PnL +872, win rate 47,22 %, RR medio 3,64,
  profit factor 4,01, expectancy $22,95; horas 05-12 UTC; por dia lun 50 %, mar 25 %, mie 71 %,
  jue 25 %, vie 56 %. Tres meses exportados (enero 58, abril 38, agosto 47): golden de F26.
  Evidencia del video v5: `ev-v5-000000-69774090` (sesion de backtest de abril de 2026); las
  cifras del xlsx entran como `material_adicional` cuando F26 las cite desde un tramo de video.

## Expert Validations
—

## Known Ambiguities
Fuente legible por maquina desde F10: `knowledge/spec/ambiguedades.yaml` (ids, pregunta, evidencia,
parametros, estado; un test exige que esta tabla coincida en id y titulo).
Las doce (A-1..A-12) quedaron RESUELTAS en la sesion 1 del 2026-09-09, cada una con su registro de
feedback, su minuto y su cita en v6; la tabla se conserva porque es la pregunta que se llevo a la
sesion y el test anti-deriva la compara con el YAML. El esquema de feedback solo acepta ids `A-N`.
Columna "resuelve en": la funcionalidad que convierte la respuesta en regla o parametro.

Lo que la sesion DEJA ABIERTO son A-13..A-17, registradas el 2026-09-09 con los doce items de
evidencia de v6 que el consultor acepto:
1. **A-13 break even**: responde "apenas toca" (0:57:01) y doce minutos despues se plantea exigir
   un rompimiento con cuerpo, porque protegerlo al toque le hace perder movimientos (1:09:27,
   1:09:47). No hace falta volver a preguntarselo: se mide sobre los mismos dias.
2. **A-14 anclaje H4**: dice que en el cambio de horario mantiene "la misma hora" y acto seguido
   que la apertura podria verse "a las 8, o [...] a las 6" (0:58:10). Con UTC+2 fijo el anclaje es
   21:00 UTC todo el año; con Madrid, en invierno se desplaza. Mayo y junio no se ven afectados;
   enero si.
3. **A-15 alcance** (CERRADA como DECIDIDA el 2026-09-12 por ADR-0024: no se amplia a Nueva York en esta fase. No era una pregunta del trader: el la DEVOLVIO -"puedes buscar las operaciones donde sea, o sea, no hay problema"-, y toda su operativa grabada va de 07:00 a 15:00. La capacidad se conserva: ampliar es cambiar `ventana_inicio` y `ventana_fin`): deja abierto ampliar a Nueva York, "puedes buscar las operaciones donde sea"
   (1:46:23), cuando toda su operativa grabada va de 07:00 a 15:00. Decision del consultor.
4. **A-16 proveedor de datos**, PARTIDA EN DOS el 2026-09-12 por ADR-0024 porque mezclaba una decision con una medicion. La DECISION es **A-23** y esta DECIDIDA: la referencia es Dukascopy (ADR-0005), MT5/FundedNext se usa para spread, ejecucion, reloj de servidor y paridad, y la divergencia entre proveedores entra en F26 como MARGEN DECLARADO. La MEDICION se queda en **A-16** y sigue ABIERTA, con `resuelve_en: F26`: el anexo del 2026-09-09 (`docs/validation/anexos/A-16-proveedor-de-datos-2026-09-09.md`) midio MT5 contra Dukascopy -2 puntos de mediana una vez corregido el reloj de servidor, y la demo de FundedNext no sirve NI UNA vela M1 de mayo- pero el propio anexo dice que la fuente del trader, Oanda via FX Replay, "esta medicion no la cubre": el trader backtestea en FX Replay,
   que usa datos de Oanda (0:24:14), y con reglas que dependen de romper "por una milesima", uno o
   dos puntos cambian un dia entero. Eso es lo que F26 tiene que medir y declarar.
5. **A-17 noticias**, partida en dos por ADR-0022 (2026-09-12). **EL BOT NO OPERA NOTICIAS** en
   su primera version: `filtro_noticias = regla` y RN-028 (clase `gate`) prohibe abrir. Lo que el
   trader hace -y que este parrafo daba antes por decidido tambien para el bot- sigue siendo cierto
   sobre SU operativa: el opera cuentas propias que no lo prohiben y su estrategia funciona dentro
   del evento (2:02:00). Pero el propio trader aviso de que la cuenta fondeada puede prohibirlo dos
   minutos antes y despues y cerrarla aunque acabes en profit (2:00:29, 2:01:14), y ahi va el bot.
   **A-17** se queda con la VERIFICACION del reglamento y sigue ABIERTA (que ventana, que sancion;
   se lee antes de F33). **A-22** nace con la decision de alcance y esta DECIDIDA.
   ENMIENDA DEL 2026-09-14 (ADR-0026 y enmienda de ADR-0022): la firma pasa a ser FTMO 2-Step
   **Swing**, que no restringe las noticias. **EL BOT SI OPERA NOTICIAS**, como el trader:
   `filtro_noticias = no` y RN-028 DESCARTADA. A-17 queda DECIDIDA por ADR-0026 -el reglamento se
   leyo y el supuesto era cierto en FTMO Standard y en FundedNext, justo las cuentas que no se
   eligieron- y A-22 sigue DECIDIDA con el sentido invertido.
6. **A-27 y A-28**, abiertas el 2026-09-14 (ADR-0026), son MEDICIONES del entorno de FTMO, no
   preguntas al trader: la ficha de EURUSD (default declarado, heredado de la demo de FundedNext) y
   el reloj del servidor con su horario de verano (sin valor; no se cierra antes de observar el
   cambio de hora de octubre). A-19 queda DECIDIDA por ADR-0027: el corte del dia de riesgo es la
   medianoche CE(S)T que escribe el reglamento. A-24, A-25 y A-26 -la liquidez de M15- estuvieron
   RESERVADAS por F14b §3 hasta el 2026-09-20, y ese dia se abrieron REESCRITAS contra los
   fotogramas: las tres cambiaron de enunciado (docs/validation/LIQUIDEZ-M15.md).

| Id | Ambiguedad | Resuelve en | Pregunta de la sesion 1 |
|---|---|---|---|
| A-1 | sesgo H4 | F11 (regla), F18 (motor de sesgo) | ¿que vela H4 fija el sesgo y cuando cambia? |
| A-2 | tercer cartucho | F11, F21 | ¿2 o 3 intentos por zona? (contradiccion ficha vs V4 0:48:41) |
| A-3 | salida sin ruptura | F11, F23 | ¿se cierra si no rompe? ¿cuando? |
| A-4 | BE al tocar o al cierre | F11, F23 | ¿break-even al tocar el nivel o al cierre de vela? (V4 0:44:56) |
| A-5 | cadencia de reubicacion | F11, F22 | ¿cada cuanto se reubica la orden pendiente? |
| A-6 | cierre 15:00 | F11, F23 | ¿cierre forzoso a las 15:00 y en que huso? |
| A-7 | stop del 2.o esquema | F11, F21 | ¿donde va el stop en el segundo esquema de entrada? |
| A-8 | "dos velas como una" en mapeo | F11, F18 | ¿cuando dos velas cuentan como una estructura? |
| A-9 | anclaje de la vela H4 (hora y huso del grafico) | sesion 1 (captura, P-03 del kit), F11 (valor y `huso` de `anclaje_h4`, creado UNKNOWN en F15) | ¿a que hora y en que huso del grafico abre su H4? (se resuelve viendo su grafico) |
| A-10 | stop a 0,8: fijo o 0,75 + spread | F21 | ¿el 0,8 es fijo o "0,75 mas el spread del momento"? |
| A-11 | SL en la orden o tras el llenado | F22, F31 | ¿el SL va en la orden pendiente o se pone tras el llenado? |
| A-12 | porcentaje de vela transcurrido para bajar la proteccion a 0,50: 40 % (transcripcion heredada) o 50 % (large-v3, V1 0:15:59) | F21 | ¿a partir de que parte de la vela bajas el stop a 0,50? |
| A-13 | break even al toque o con cuerpo | F11, F23, F26 | ABIERTA por el corte de audio de v9 0:57:00-0:58:06; LO FIRME ACTIVADO el 2026-09-29 (al tocar, en M1, a la entrada exacta; break_even_criterio_ruptura = mecha, fb-2026-09-29-sesion-03-2cff5008). Antes: ¿el rompimiento que dispara el BE vale al toque o hay que esperar cuerpo? (v6 0:57:01 vs 1:09:27) |
| A-14 | los 28 dias al año en que su horario y la rejilla H4 no cuadran | F11, F15, F26 | del 8 al 28 de marzo y del 25 al 31 de octubre la primera H4 se ve a las 22:00: ¿opera de 7 a 15 igual o se ajusta a la vela? |
| A-15 | alcance de la ventana operativa | F11 | DECIDIDA (ADR-0024): no se amplia a Nueva York en esta fase; el trader devolvio la pregunta (v6 1:46:10, 1:46:23) |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | F26 | ABIERTA, y es una MEDICION: el anexo del 2026-09-09 midio MT5 contra Dukascopy, no Oanda (v6 0:24:14) |
| A-17 | noticias frente a la regla de la cuenta de fondeo | F11, F33 | DECIDIDA (ADR-0026, 2026-09-14): la cuenta elegida es FTMO 2-Step Swing, sin restriccion de noticias; el reglamento se leyo y la ventana de 2 minutos existe en FTMO Standard, que no se eligio |
| A-18 | base sobre la que se mide el objetivo 1:3 | F11, F26 | ¿el 1:3 se mide sobre la caja completa o sobre el riesgo real tras mover el stop? (v2 0:32:56). **PRIMERA MEDIDA, del material y no de la sesion (2026-09-21, agosto, ADR-0037): las dos lecturas predicen 3,75 y 3,00 de RR sobre entrada-stop, y las 18 filas con `maxTP` e `initialSL` tienen SUELO EN 3,00 -minimo 2,50, tres clavadas en 3,00, 16 de 18 por debajo de 3,75-. La combinacion CONFIRMED de hoy (caja_completa con stop a 0,8) NO cuadra con el material. NO decide: un mes, 18 filas, y la caja no esta en el fichero. Se repite sobre mayo** |
| A-19 | cuando empieza el dia y la semana de riesgo | F11, F33 | DECIDIDA (ADR-0027, 2026-09-14): la medianoche CE(S)T del reglamento de FTMO, que es el reloj civil del trader; `reloj_dia_riesgo = civil_operativa` |
| A-20 | cuantas zonas de control invalidan un esquema | F12, F20, F26 | RN-009 dice "mas de una zona" pero el literal dice "por lo general solo buscamos uno": ¿regla o tendencia? · RESUELTA el 2026-09-11 por escrito: es REGLA, y el trader ratifica el descarte |
| A-21 | que es una zona de control limpia, sin ruido | F12, F20, F26 | ABIERTA: lectura candidata de la sesion 3, sin activar -zona limpia = sin alternancia de colores-, que no esta en el enum del motor. Antes: los dos esquemas SI estan definidos en el corpus; lo que sigue siendo cualitativo es "que no haga mucho ruido, o sea, sea una zona limpia" |
| A-22 | si el bot opera noticias, y que pasa con la capacidad para otras cuentas | F13, F22, F26, F33 | DECIDIDA por el consultor (ADR-0022). El 2026-09-12: NO en la v1. Desde la enmienda del 2026-09-14 (ADR-0026): SI, porque la cuenta FTMO Swing no lo restringe; la capacidad de filtrar se conserva |
| A-23 | que proveedor es la referencia para medir la fidelidad | F26, F17, F24 | DECIDIDA (ADR-0024): Dukascopy; MT5 para spread, ejecucion y paridad; la divergencia entra en F26 como margen declarado |
| A-24 | que hace que marques un pivote de M15 y no otro | F19, F20 | DECIDIDA (2026-09-24, ADR-0045): el pivote MAS RECIENTE YA FORMADO, por la regla global sobre la busqueda en transcripciones (v1 #180 responde; ninguno en contra). Pasa a RESUELTA solo con un registro del trader que apunte a ella; cuando esta formado un pivote es A-35 |
| A-25 | la vida de la marca de liquidez de M15 | F19, F20 | ABIERTA, PREGUNTA (2026-09-20), sesion 2: si la marca se mueve a un pivote mas reciente mientras vive, o solo la retiran el trade ganador, la invalidacion o el cambio de dia. La version anterior -"¿un pivote mas reciente invalida una liquidez YA TOMADA?"- no la sostenia ni el corpus ni la pantalla |
| A-26 | el flujo de M15 cuando va contra el sesgo de H4 | F18, F19 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-fc2c5c1f): manda el sesgo, en M15 solo a favor. Antes: ABIERTA, PREGUNTA (2026-09-20), sesion 2: la mitad disyuntiva ("¿H4 o M15?") esta CERRADA -es M15, dicho cuatro veces- y escrita en la spec; lo abierto es que hacer cuando el flujo de M15 va contra el sesgo de H4, como en v3 0:12:42, porque RN-005 lee hoy el lado de ruido del sesgo |
| A-27 | las especificaciones de EURUSD en FTMO | F17, F33 | ABIERTA, MEDICION en la demo de FTMO: digits, contrato, lote minimo y paso, stops level; corren con el default de FundedNext, sin verificar en FTMO |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | F17 | ABIERTA, MEDICION: desfase y calendario de cambio de hora; sin valor, y no se cierra antes de observar la transicion de octubre |
| A-29 | cuando nace la orden limite | F20, F22 | ABIERTA, PREGUNTA (2026-09-16): al darse el esquema, o en cuanto se toma la liquidez y se va moviendo; el corpus dice las dos. Corre con la primera como default (`orden_limite_nace`); con la segunda hay que reescribir RN-008. TERCERA LECTURA (2026-09-28, trabajo/preparar-a47): `al_aparecer_punto_de_breaker`, la orden stop nace en el posible punto de breaker antes de la ruptura y se mueve con el (ev-v7-001457-1fe7fdfe, ev-v7-002201-2b2f20aa); solo con A-47 en `stop_en_ruptura` |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | F22, F23 | ABIERTA, PREGUNTA (2026-09-16): cancelarla o dejarla; ni el corpus ni ninguna ambiguedad lo decian. `retirar_orden_limite` esta declarada y ninguna regla la usa |
| A-31 | el stop entero de una entrada que se activo sin ruptura | F21, F22 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-d36ba0d2): gasta un intento. Antes: ABIERTA, PREGUNTA (2026-09-17), sesion 2: si gasta intento. La spec corre con que si -cuesta el riesgo entero y el trader no lo eximio- y con que la salida en rojo sin stop no; las dos son lectura nuestra |
| A-33 | tres ganadoras que cierran por debajo de 3R | F20, F24, F26 | en la sesion 1 dijo «sin toma de parciales y que tiene que llegar al ratio 1.3 si o si» (v6 0:17:07), pero hay TRES ganadoras que CIERRAN por debajo de 3R en DOS meses independientes: 2,50 en agosto, 2,57 y 2,94 en abril. `maxTP` es el precio de CIERRE -medido: `== avgClosePrice` 17 de 17-, asi que no es que no llegaran: es que cerraron ahi |
| A-32 | el nivel que al romperse con mecha invalida la entrada | F19, F20 | ABIERTA, PREGUNTA (2026-09-17), sesion 2: si el nivel que el trader ve romperse con mecha en v4 0:53:23 es la liquidez de M15 (RN-004, cuerpo) o un nivel de M1. La pantalla no lo dice: la linea no lleva etiqueta |
| A-34 | vela H4 previa que rompe ambos extremos | F18 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-617f496a): con la doble ruptura decide el color de la vela; el motor sigue dando `ambiguo` (desalineado). Antes: ABIERTA, PREGUNTA (2026-09-24, ADR-0044): RN-003 no dice que sentido toma el sesgo si la vela previa rompe los dos extremos de la anterior; mientras no lo diga el trader, el sesgo es AMBIGUO en esa sesion y no se opera |
| A-35 | cuándo un pivote de M15 está formado | F19, F20 | ABIERTA, PREGUNTA (2026-09-24, ADR-0045), BLOQUEANTE: la spec no define cuando un pivote esta formado; bloquea RN-004 y no se sustituye por un parametro provisional, porque es un mecanismo y no una cifra |
| A-36 | en qué punto de la mecha va la orden límite | F20, F22 | ABIERTA, PREGUNTA (2026-09-25, trabajo/sesion-02, candidato C-01): consta que la orden va siempre en la mecha (ev-v4-010605-a11249c0); falta en que punto. No bloqueante |
| A-37 | en qué temporalidad se busca la vela contraria de la que sale el stop | F21 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-91eeee94): M1. Antes: ABIERTA, PREGUNTA (2026-09-25, candidato C-02): consta que el stop sale del punto donde se genera la vela contraria (ev-v1-001454-69cebe62); falta la temporalidad. No bloqueante |
| A-38 | cuándo se da por anulada una orden límite que el precio deja sin llenar | F22 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-c7fa3068): la orden sigue viva hasta el siguiente posible punto de breaker. Antes: ABIERTA, PREGUNTA (2026-09-25, candidato C-04): RN-006 cubre la orden que se mueve; falta cuando se anula. No bloqueante |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | F22, F23 | ABIERTA, PREGUNTA (2026-09-25, candidato C-05): anotado el cierre al vencer la vela H4 operativa (ev-v3-010304-4468cc20), que ninguna regla cita. No bloqueante |
| A-40 | qué se hace con el stop después del break even | F23 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-7a79dcd7): tras el break even el stop no se mueve. Antes: ABIERTA, PREGUNTA (2026-09-25, candidato C-06): cero pasajes; anotada la proteccion progresiva mas alla del 1 a 3 (ev-v3-003220, ev-v3-003318), contra RN-015. No bloqueante |
| A-41 | si hay un tope de entradas por día, aparte de los cartuchos | F21 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-7b87c3ee): tres intentos por liquidez, sin tope por dia. Antes: ABIERTA, PREGUNTA (2026-09-25, candidato C-07): ev-v4-003350-acb03ee7 se lee por dia aqui y por zona en A-2. No bloqueante |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | F14, F26 | ABIERTA, lectura PROVISIONAL el 2026-09-29 (ADR-0059): sesiones fijas en el reloj del grafico todo el ano (06:00-14:00 de Madrid en invierno); huso_operativa NO cambia hasta separar el reloj de las sesiones del del dia de riesgo (rama de codigo); el trader dijo «creo», se confirma en la proxima sesion. Antes: ABIERTA, PREGUNTA, BLOQUEANTE de la entrada de meses de invierno desde el sorteo (2026-09-25, trabajo/sesion-02): el grafico es UTC+2 fijo y el corpus dice "de 7 a 15 por españa" y "De UTC más 2, de 7, claro"; en invierno se separan una hora. huso_operativa sigue en Europe/Madrid; ENTRADA-MARZO para antes del paso b, el sorteo (PARADA B0), porque congela huso_operativa y no se repite |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | F19, F20 | ABIERTA, PREGUNTA (2026-09-25, trabajo/huecos-motor, ADR-0049 H2): el motor solo tiene eventos de 07:00 a 15:00 y RN-004 no puede ver una toma anterior, mientras el contexto de mapeo del kit empieza a medianoche. El rango de eventos se queda en las 07:00 hasta que responda. Afecta a RN-004. No bloqueante; va en la hoja justo despues de A-35. MEDIDO el 2026-09-28 (EMBUDO-77.md §4, rama trabajo/registrar-embudo): el codigo ya responde de hecho, y solo para una vela: la M15 que cierra a las 07:00 cuenta como toma dentro de la sesion; la toma del productor es esa en 7 de los 40 dias de construccion con toma |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | F11, F18 | ABIERTA: respondida el 2026-09-29 con lectura NUEVA (9 perdidas SEGUIDAS, no un porcentaje; PARA, ACTIVAR-A35-A44.md §4); lo que falta es A-51. Antes: ABIERTA, PREGUNTA, BLOQUEANTE de RN-020 (2026-09-26, trabajo/cableado-simulador, ADR-0053 §9): RN-020 lee perdida_dia y perdida_semana y la spec no declara su magnitud (saldo o equity) ni su corte; medido con el broker y la cuenta cableados, siguen NO_IMPLEMENTADA y RN-020 prohibe abrir en todas las sesiones de construccion, y seguira prohibiendo aunque la geometria (A-35) quede resuelta: es el siguiente bloqueo del bot despues de A-35. Va en la hoja de la sesion 02 justo despues de A-43 |
| A-45 | en qué granularidad se evalúa «cierra con cuerpo» en la toma de liquidez de RN-004 | F19, F20 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-b2e074e3): la toma la hace una vela de M1 con cuerpo; el motor mira la M15 cerrada (desalineado). Antes: ABIERTA, PREGUNTA (ADR-0054 §4): ninguna fuente fija que vela cierra con cuerpo; la convencion actual, al cierre de M15, es PROVISIONAL. Lecturas: cierre de M15, cierre de M1 o tick. Va en la hoja de la sesion 02 justo despues de A-35 |
| A-46 | si una toma de liquidez de una sesion anterior del mismo dia sigue valiendo en la siguiente | F19, F20 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-5021677e): cada sesion es un escenario propio, sin tope diario de escenarios; `liquidez_tomada` no caduca todavia (desalineado). Antes: ABIERTA, PREGUNTA (ADR-0055 §4): `liquidez_tomada` no caduca al abrir la sesion; con una toma de la sesion anterior RN-008 y RN-009 disparan (31/31) y RN-011 no (0/31). Deuda conocida hasta la respuesta; no bloqueante |
| A-47 | el tipo de orden de entrada, stop o límite | F20, F22 | RESUELTA el 2026-09-29 en la sesion 3 (fb-2026-09-29-sesion-03-92a38105): STOP en la ruptura, entrada_tipo_orden = stop_en_ruptura. Antes: ABIERTA, PREGUNTA, BLOQUEANTE de RN-011 (2026-09-27, trabajo/sesion-02, decision del consultor): la spec asume orden limite y el trader lo dice asi, pero en pantalla en v7+v8 las ordenes legibles son 38 stop frente a 1 limite (SESION-02-VIDEO-V8.md §4; ev-v8-003620-12670f0e, ev-v8-003935-0a0b3f8e, ev-v7-000423-01b2c18a). Decide el precio y el instante de entrada: al romper el punto de breaker o al volver a el |
| A-48 | qué velas forman el bloque de la caja | F20, F21 | ABIERTA, PREGUNTA, no bloqueante (2026-09-28, trabajo/preparar-a47, decision del consultor sobre DISENO-ENTRADA-RUPTURA.md §2.5): con el criterio escrito antes de medir ninguna regla explica mas de 1 de las 12 cajas de v7 y v8 (BLOQUE-DE-LA-CAJA.md §3); lecturas `ultima_contraria` (lo de hoy; ev-v3-010818-010bd2b3, ev-v3-011540-5425b533) y `tramo_de_contrarias` (ev-v3-010648-0039e34d; v7 0:24:03 ev-v7-002403-8344331d, condicionado a la mecha que cubre). Solo actua con la orden stop (A-47) |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | F20, F21 | ABIERTA, PREGUNTA, no bloqueante (2026-09-28, trabajo/preparar-a47): en 10 de 12 cajas el 1 es la maxima de la vela en curso en el :59 o de la anterior (BLOQUE-DE-LA-CAJA.md §1.5, §2.4); lecturas `cerrada` (lo de hoy) y `en_formacion`, que choca con ADR-0028 y queda NO_IMPLEMENTADA hasta un ADR que lo decida; ADR-0028 no se toca |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | F19, F20 | ABIERTA: lectura candidata de la sesion 3, sin activar -el trader no usa la posicion de la caja frente al nivel como filtro («no importa»)-. Antes: ABIERTA, PREGUNTA, no bloqueante (2026-09-28, trabajo/registrar-embudo, orden del consultor tras EMBUDO-77.md §4): RN-005 no dice que punto de la zona se compara con el nivel tomado. Lectura vigente, DECISION DE CODIGO SIN FUENTE: solo el 0 (`se_desarrolla_en_el_lado_de_ruido`, engine/zonas.py). Medido: RN-005 deja sin orden 8 y 6 dias de construccion (las dos lecturas de A-21), con la caja cruzando el nivel por 1 a 5 puntos y el 1 del lado del trader. Afecta a RN-005. El motor no cambia hasta la respuesta |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | F11, F18 | ABIERTA, PREGUNTA, BLOQUEANTE de RN-020 (2026-09-29, trabajo/activar-sesion-03, orden del consultor): nace de la respuesta de A-44 en la sesion 3 -el tope son 9 perdidas seguidas, sin importar dia ni semana-; falta que corta la racha (una ganadora, un break even) y cuando vuelve a operar tras la novena |

Las 3 preguntas bloqueantes de la sesion 1 (MASTER_PLAN G) se eligen en el brief de F10 con los <!-- cifra-congelada: la sesion 1 ya se celebro -->
casos delante; candidatas por impacto en el kit: A-9 (afecta a todos los casos), A-2 y A-4.

Evidencia por ambiguedad (F07, 2026-09-07; ids en `knowledge/evidence/`, `evidence list --tema`):
- A-1 sesgo H4: `ev-v2-000836-6dbfcd6b`, `ev-v3-000531-4d6375b6`, `ev-v3-000824-c81f03eb`,
  `ev-v3-010948-331c69aa`, `ev-v3-011045-a185d2ba`, `ev-v3-011614-a5a05b0a` (simplificacion
  abierta), `ev-v4-004603-d0ffd4f2`.
- A-2 tercer cartucho: ficha 2 `ev-v3-000138-fc8f7905`, `ev-v3-004817-f2dfb955`,
  `ev-v4-003350-acb03ee7` frente a 3 `ev-v4-002333-8bf96363`, `ev-v4-004742-30c8d58a`,
  `ev-v4-004832-6543b551`, `ev-v4-005411-a486336d`; pregunta del consultor `ev-v4-002951-d3132b3f`.
- A-3 salida sin ruptura: `ev-v4-010759-514b5d7d` (cerrar al cierre de la vela sin rotura) frente
  a `ev-v4-010831-5f4a00ad` (prefiere proteger y dejarlo).
- A-4 BE al tocar o al cierre: `ev-v4-004447-bc2e74ee`, `ev-v2-003103-31d872da`,
  `ev-v5-000427-f8d5d36d`.
- A-5 cadencia de reubicacion: `ev-v1-001358-a2b8ec0d`, `ev-v4-010731-bb8af97c`,
  `ev-v4-010857-5bc906c9` (se actualiza con el precio; sin cadencia explicita).
- A-6 cierre 15:00: `ev-v4-011514-fe34ac7e` (se cierra en punto a las 3 PM); huso en A-9.
- A-7 stop del 2.o esquema: `ev-v3-004329-a16d379b`, `ev-v4-002056-5d25b29d`,
  `ev-v4-002139-23e44f38`, `ev-v4-003029-2ea7124e`, `ev-v4-003102-1ddeeaa8`,
  `ev-v4-003227-038864db`, `ev-v4-003252-ef8d3139` (opcion simple: 0,75 estatico en los dos).
- A-8 dos velas como una: `ev-v3-010648-0039e34d`, `ev-v3-011540-5425b533`.
- A-9 anclaje H4: `ev-v3-000136-6160fcea` (grafico en UTC+2), `ev-v3-000157-b26147c7` (velas H4
  de 7 a 11 y de 11 a 3 hora del grafico); la hora de apertura no aparece en ningun fotograma.
- A-10 0,8 fijo o 0,75 + spread: contradiccion mecanica `stop.nivel` (`ev-v1-000448-346d6d90`,
  `ev-v2-003142-beb4ad3c` = 0,75; `ev-v5-000312-f5062062` = 0,80); `ev-v4-000835-782cf2cc`,
  `ev-v4-001221-1e66b5fd`.
- A-11 SL en la orden o tras el llenado: `ev-v4-001207-0c4ffd4b` (el stop que se introduce en la
  operacion es el 0,75), `ev-v1-000620-0f7dea14`; nada dice si va en la orden pendiente.
- A-12 40 % o 50 % de la vela: `ev-v1-001557-1dd16e5c` (50 %), `ev-v1-001643-47673889`.

## Known Contradictions
Mecanica (`knowledge/evidence/_contradicciones.yaml`, mismo tema con `valor` distinto): 1 ABIERTA,
`stop.nivel` 0,75 (`ev-v1-000448-346d6d90`, `ev-v2-003142-beb4ad3c`) frente a 0,8
(`ev-v5-000312-f5062062`) = A-10. DECIDIDA: A-10 esta RESUELTA en 0,8 fijo y hay registro
(`fb-2026-09-09-sesion-01-e9708750`, RESOLVE_CONTRADICTION). Sigue contando como ABIERTA y es
CORRECTO: `contradicciones.detectar` la deduce de la EVIDENCIA, que es inmutable y de verdad dice
dos cosas distintas. Lo que se cerro es que valor usa la spec, no lo que el trader dijo en 2026.
De lectura (temas distintos, sin `valor` comparable; abiertas como ambiguedades): cartuchos 2
(ficha, `ev-v3-000138-fc8f7905`) vs 3 (`ev-v4-004832-6543b551`) = A-2 · parciales 30-40 %
(`ev-v2-002419-4629d258`) vs sin parciales (`ev-v1-002313-6342a154`, `ev-v3-010244-2edecd2d`,
`ev-v4-011112-17178b38`; idea del 50 % en 1:2 `ev-v4-011116-b0e6f3f5`) · BE al tocar vs al cierre
(`ev-v4-004447-bc2e74ee`) = A-4 · salida anticipada si/no (`ev-v4-010759-514b5d7d` /
`ev-v4-010831-5f4a00ad`) = A-3.

## Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Technical Debt
- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965). FTMO prohibe operar el gap -abrir cuando hay noticias o eventos macro programados y en las dos horas previas al cierre de un mercado que va a estar cerrado al menos dos horas-, y R15 ya lo decia en la fuente oficial leida el 2026-09-25. En una semana normal el bot no puede incumplirlo: opera de 07:00 a 15:00 Europe/Madrid, de lunes a viernes, y cierra lo que quede a las 15:00 (RN-002), lejos del cierre del viernes a las 22:00 UTC. Pero no tiene calendario de festivos ni de horario de mercado, asi que un dia en que el mercado cierra antes (Nochebuena, Nochevieja, un festivo con cierre anticipado) podria abrir dentro de esas dos horas. No se corrige en esta rama (brief del 2026-09-29): hace falta un calendario de cierres del broker y una regla que lo lea.
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c). En el control con el simulador, 3 de 8 (lectura a) y 4 de 8 (b) ordenes limite del bot se colocaron con el precio al otro lado y `primer_llenado_limite` las lleno en el tick siguiente (1-5 s); ADR-0052 solo preve rechazos por los limites del perfil. Segun el consultor, en MT5 una limite en el lado equivocado se RECHAZA por precio invalido: no medido aqui, se comprueba con la demo en MetaTrader. Si se confirma, es un fallo de fidelidad del broker (ADR-0052) y un sintoma de RN-011, que coloca la limite en la zona sin mirar donde esta el precio. No se toca en esta rama. ADR-0056 §3 (2026-09-28) decide RECHAZAR la pendiente mal colocada, PROVISIONAL hasta la demo de FTMO en MetaTrader, y lo asigna a la rama 1 de codigo de ADR-0056 §8; el script de la demo se prepara en otra rama. RESUELTA en el simulador por trabajo/broker-ordenes-stop (ADR-0057): la pendiente del lado equivocado se rechaza con precio_invalido y ya no se llena a su precio; el efecto sobre la linea base de construccion, en docs/validation/BROKER-ORDENES-STOP.md. Sigue PENDIENTE medir en la demo lo que hace MT5.
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047). ADR-0011 §6 y §7 y `src/botsito/cases/kappa.py` miden en `(caso, sesion)`, una decision por sesion, y la gramatica de `LABEL_CASE` rechaza dos entradas en la misma sesion («la sesion 07-11 aparece dos veces», auditoria del 2026-09-13, [47]). ADR-0047 fija que la unidad del holdout sera la operacion, la de ADR-0043. Hoy no rompe nada, porque hay 0 registros `LABEL_CASE`; hay que adaptar la gramatica y `kappa.py` antes del primer etiquetado por operacion o de medir un kappa entre sesiones.
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`). v6 se grabo en un dia de una particion reservada (medido con `casos_reservados`, solo el booleano), y su transcripcion la citan 23 items de evidencia y el informe de su sesion. Si trae detalle por operacion de ese dia solo se sabe leyendola. **Declarada como exposicion posible; decidir en rama propia, ANTES de usar el holdout, si ese dia se retira del holdout.**
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2): los dos crean o reescriben commits sin `pre-commit`, asi que no exigen el sello de `make check`. No se usan para meter trabajo (CLAUDE.md), y la garantia de fondo sigue siendo la CI. Es lo que queda de la deuda del commit sin puerta, que la puerta de `trabajo/blindaje` cerro: `40759cb` y `2753ac1`, los dos con `make check` en rojo, ya no podrian entrar.
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23): la caja se reconoce solo si el 0,5 queda por debajo del 0,8 en la imagen (`5 <= yv - ya <= 400`). Para reutilizarlo con compras hace falta un caso sintetico de compra y, si falla, arreglarlo ANTES de medir. No cambia ningun veredicto de v5 (docs/validation/V5-INSTANTES.md, §6).
- **RESUELTA el 2026-09-23 en `trabajo/v5-instantes`**: `docs/runbooks/RITUAL.md` ya dice que la sesion lee el sha del repositorio y se para si no esta en `main` o el tag no apunta a `HEAD`; el mensaje no lleva hueco. Historia: EL MENSAJE DE EDICION DE `PROJECT_STATE.md` DEL RITUAL TENIA UN HUECO <SHA> QUE SE RELLENABA A MANO (2026-09-23). Se pego sin rellenar CUATRO veces -cierres de mayo, guardia de ids dos veces y regla del mes-, dos de ellas ANTES del merge, con la sesion todavia en la rama y sin tag (patron 5). Corregido en la practica: la sesion lee el sha del repo y se para si no esta en `main` o el tag no apunta a `HEAD`. Falta reflejarlo en `docs/runbooks/RITUAL.md`.
- CON EL HUSO MAL DECLARADO, LAS FILAS QUE SE DESPLAZAN A UN DIA NO PEDIDO DESAPARECEN SIN AVISO (2026-09-23, `trabajo/regla-mes-sin-filas`). El lector solo devuelve las filas cuyo dia -en el huso de los dias pedidos- esta pedido; si el huso declarado en `libros.yaml` esta mal, una fila puede caer en otro dia DENTRO del mes, no pedido, y se descarta sin contarse. NINGUN CODIGO LO DETECTA: la regla del mes sin filas solo caza el extremo en que TODAS las filas de los dias pedidos salen del mes, y la comprobacion de sesion H4 solo las que caen fuera de sesion. Hoy solo lo evita el PROCEDIMIENTO de velas con control de ADR-0039 al declarar el libro. PATRON 5, sin detector. **DECIDIDO (2026-09-23): no se abre rama; un detector tendria que mirar dias no pedidos, incluidos reservados (ADR-0037); la proteccion es el procedimiento de velas con control de ADR-0039.**
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`). `CLAUDE.md` declara ya el regimen de `docs/validation/` -un informe cerrado en `main` se corrige con un recuadro al principio y el cuerpo queda intacto-, pero es una regla ESCRITA sin detector: un commit podria reescribir el cuerpo de un informe cerrado y ni `knowledge validate` ni ningun test lo verian. Es el PATRON 5 -lo escrito y lo ejecutado se separan y nada los compara-, y queda ANOTADO, no se arregla aqui. DISPARADOR: la primera vez que un diff de un informe cerrado traiga lineas BORRADAS o cambiadas fuera de un recuadro.
- **RESUELTA el 2026-09-22 en `trabajo/guardia-ids-docs`** (informe docs/validation/GUARDIA-IDS-DOCS.md). LA GUARDIA DE IDS CITADOS NO MIRABA `docs/**`: la que comprueba que un id citado existe (`cases/ambiguedades.py:170`, `cases/paquete.py:1150`) corria solo sobre `knowledge/**`, y ningun test recorria los documentos. Estaba anotada DOS VECES con redacciones distintas -la rama de la caja y el dia siguiente-, y las dos decian mal que ids faltaban: contaban como inexistente el item REAL que la copia de la auditoria supersedia, y omitian el segundo id inventado de esa auditoria. Medido con la gramatica de `comun.ids.FUENTE`: 13 citas de 4 ids que no existen en `docs/**` y en este fichero, ninguna una fabricacion. AHORA es una capa de `knowledge validate` sobre `docs/**`, `CLAUDE.md` y `PROJECT_STATE.md`, contra el MISMO conjunto que los trailers `Fuente:`; un id citado a proposito como inexistente se declara en SU documento, en un bloque `ids-inexistentes` con motivo.
  Ids que ESTE fichero cita a proposito aunque no existen (la guardia los exime solo aqui):

  ```ids-inexistentes
  ADR-9999 — ejemplo, en el Change Log de F09, del ADR inexistente que el trailer `Fuente:` dejaba pasar
  ```
- **CORREGIDA el 2026-09-23 en `trabajo/v5-instantes`: la condicion «caja >= 100 px» esta SIN EFECTO desde §R10 del mismo informe** -*«La condición «caja ≥ 100 px» queda SIN EFECTO, y se dice por qué: era una consecuencia del ±3 px, no del material»* (`LA-CAJA-DEL-29-DE-ABRIL.md:177-178`)-: con la lectura programatica a +/-1 px una caja de 80 px basta. Lo que sigue haciendo falta es un fotograma con los niveles 0 y 1 con linea propia Y la herramienta valida; el criterio mecanico esta en `docs/validation/V5-INSTANTES-CRITERIO.md`. Texto original: LA MEDIDA DE LA CAJA NECESITA UN FOTOGRAMA CON LA CAJA >= 100 px Y LA HERRAMIENTA VALIDA (2026-09-22, informe §R7). El cociente `px(entrada->stop) / px(0->1)` cancela la escala de precios pero NO la precision de lectura: a ojo el error es +/-3 px, que sobre una caja de 187 px es +/-0,016 -dentro de la tolerancia 0,03- y sobre una de 80 px es +/-0,038 -fuera-. Y las dos condiciones NO COINCIDEN en los cuatro fotogramas abiertos: donde la caja mide 187 px la herramienta esta en ERROR, y donde la herramienta es valida la caja mide 80. La transcripcion de v5 localiza SIETE instantes y solo se han abierto cuatro fotogramas de DOS de ellos.
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril). Medido: con el desfase aplicado, las dos velas que las leyendas de v5 dan exactas cuadran con Dukascopy a 1 y 2 PUNTOS. Es la PRIMERA MEDIDA DE A-16 -la TERCERA fuente, la que su propio texto dice que la medicion del 2026-09-09 no cubria- y con n=2 NO se cierra: `estado`, `decision` y `evidencia` de A-16 no se tocan. El UTC+2 es FIJO, no Europe/Madrid: el fotograma de v4 muestra ENERO y ya marca +2; toca A-9 y no se decide aqui. AMPLIARLA exige OCR sobre los 367 fotogramas -no hay Pillow, a proposito- o pedirle al trader una exportacion de velas de FX Replay.
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2). Los niveles a 1,00 y 1,25 de la distancia entrada-stop NO caen sobre fractales mas que el azar -4 y 3 de 35 frente a senuelos de 4, 4 y 5-, mientras que la ENTRADA si acierta mas que todos ellos (7 de 35 a +/-2 y 17 a +/-5). El ancla no esta rota: lo que falla es el blanco. Cualquier medida futura que quiera poner la caja sobre las velas necesita OTRA definicion de nivel estructural, y esta rama no la busca.
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21). Medido por consistencia interna sobre abril: `maxTP` == `avgClosePrice` en las 17 filas donde existen las dos, sin excepcion, y presente si y solo si `rPnL > 0`. F14a lo habia SUPUESTO al reves y queda corregido alli y en ADR-0037. CONSECUENCIA: las TRES ganadoras por debajo de 3R -2,50 en agosto, 2,57 y 2,94 en abril- no son operaciones que NO LLEGARON a 3R, son operaciones que CERRARON en ganancia por debajo de 3R, y eso contradice el 'sin toma de parciales y que tiene que llegar al ratio 1.3 si o si' de v6 0:17:07 mas fuerte de lo que parecia. Apunta a PARCIALES o SALIDAS MANUALES, que es cosa de la spec y no de un parametro. La incertidumbre que queda: la columna se llama `avgClosePrice` -un cierre PROMEDIO- y eso es coherente con los parciales pero no los prueba.
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior). Medido: CON la guardia el universo es 0 casos; SIN ella, 22, todos de junio. ADR-0025 §1 saca junio porque 'no hay ninguna decision suya con la que COMPARAR', que es el motivo del camino de FIDELIDAD; pero un paquete CIEGO no compara, hace ETIQUETAR, y junio NO esta en `vistos.yaml` -correcto: el trader no lo vio-, asi que sus 22 dias son ciegos y etiquetables. Es el PATRON 2 y el informe de esa rama afirma haberlo comprobado y descartado: esa comprobacion fue erronea. NO se arregla aqui: que es un paquete ciego lo decide el consultor.
- **DECIDIDA el 2026-09-23 en `trabajo/regla-mes-sin-filas`: la regla SE MANTIENE**, con el mensaje reescrito para decir solo lo que sabe (docs/validation/REGLA-MES-SIN-FILAS.md); su coste -no distingue un libro atado a otro mes de unos dias pedidos sin filas- queda aceptado y testeado. Historia: **PAGADA EN SU PARTE PRINCIPAL el 2026-09-22 en `trabajo/mayo-dev-ingerido`** (la disparo la segunda condicion: dos meses ingeribles a la vez y el comando sin poder ingerir ninguno). Cada tramo de `cobertura_material` declara el `material_sha256` de su libro, copiado del manifiesto del corpus, y `casos ingerir` pide SOLO los dias de ese mes ANTES de leer una fila. **LO QUE QUEDA, y se dice:** la regla por mes de `ingerir` sigue en pie, ahora REDUNDANTE para cazar el libro equivocado, y conserva su falso error si un mes llegara con cero operaciones en todos sus dias ingeribles; quitarla es decision aparte. Texto original: EL MES DEL MATERIAL SE DEDUCE DE LAS FILAS, Y DEBERIA DECLARARSE (2026-09-21, rama `trabajo/cobertura-material-del-kit`, informe §10). La regla por mes de `ingerir` usa los DIAS PEDIDOS: si el trader no hubiera operado en NINGUNO de los dias ingeribles de un mes, el libro CORRECTO daria cero filas y el comando lo llamaria error. Se deja asi porque FALLA HACIA EL LADO SEGURO -un falso error PARA el comando, no fabrica un dato, y esta rama existe para que nadie fabrique ausencias-. EL ARREGLO, nombrado para que no se redescubra: DECLARAR EL MES DEL MATERIAL y compararlo con lo pedido en vez de deducirlo de las filas; el fichero ya trae el mes en el nombre y el inventario ya lo hashea, asi que pasar el libro de mayo y pedir dias de septiembre se negaria ANTES de leer una fila, sin tocar ADR-0037 §6 -el lector sigue sin acumular nada del libro-. CONDICION: el dia que un mes llegue con cero operaciones en todos sus dias ingeribles, o el dia que el mes del material sea metadato declarado, lo que pase antes. Necesita una medida propia que NO es de esta rama: si el inventario del corpus ya registra el mes o hay que anadirlo.
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21). Un dia ingerible sin filas NO produce caso hoy. Es una decision sobre QUE ES UN CASO y no sobre como se ingiere, asi que va a la rama de la FORMA DEL CASO con su ADR, donde toca mirar 'un dia sin ninguna operacion ES su etiqueta' -lo que quemo algo el 2026-09-12-. Esperar sale BARATO justo por lo que esta rama compra: la salida de mayo ya dira que dias no produjeron caso y POR QUE, asi que la decision se tomara sobre un conjunto limpio y SIN volver a ingerir. Mayo escribe CERO casos `no_trade`.
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor). Medido: los ids NO son cronologicos -el orden real es v2 08-03, v3 08-06, v1 08-20, v4 08-30, v5 09-05, v6 09-09- y leerlos como secuencia es un error que hemos cometido los dos. De 368 items, los dos videos MAS VIEJOS aportan el 42 % (v2 53 + v3 102) y el material de SEPTIEMBRE menos del 10 % (v5 12 + v6 23), cuando la operativa se fue aclarando video a video y la version buena es la del ultimo. `fecha_grabacion` existe en `fuentes.yaml` y NINGUN mecanismo la usa; hay 11 `supersede` y 8 salen de v6, a mano. NO SE DECLARA AQUI ninguna regla de recencia: la decide el consultor con ADR, y lleva matiz -v6 es un cuestionario y manda SOBRE LO QUE SE LE PREGUNTO; v5 es una demostracion y manda sobre la GEOMETRIA que ensena; 'el ultimo gana' a secas dejaria que un comentario de pasada tumbe una explicacion cuidada-.
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21). `comprobar_citas_revocadas` vigila reglas, glosario y vocabulario contra registros de FEEDBACK revocados; NO mira `ambiguedades.yaml` y NO mira los `supersede` de EVIDENCIA. Medido: **tres ambiguedades citan evidencia superseded** -A-10 y A-11, ya RESUELTAS, y A-18, que sigue ABIERTA- y `make check` pasa verde. En A-18 no es cosmetico: cita `ev-v4-011951-5fb49e03`, al que `ev-v6-014702-2d7096db` supersede, y ese item de v6 concluye en sus `notas` lo CONTRARIO -que el 1:3 se mide sobre la caja completa- de lo que apuntan agosto y la geometria de v5. Es el mismo patron 3 de la lista: la guardia ENUMERA los sitios que vigila en vez de nombrar la condicion. TIENE RAMA PROPIA y no se arregla en F14a.
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). (1) UN INPUT GLOBAL Y MUTABLE DEL QUE DEPENDE LA REPRODUCCION -ADR-0035, el paquete recomponia con los cupos de hoy y no con los suyos-. (2) UNA PROHIBICION ESCRITA MAS ESTRICTA QUE EL ADR sin que ningun ADR lo diga -tres apariciones; la tercera es `CLAUDE.md` §3 y esta rama-. (3) **UNA REGLA QUE ENUMERA LOS CASOS EN VEZ DE NOMBRAR LA CONDICION DEJA FUERA EL CASO QUE NADIE PENSO**, tres apariciones esta semana: `CLAUDE.md` decia que sitios toca ABRIR y CERRAR una ambiguedad y no contemplaba EDITARLA -y por eso `docs/spec/ambiguedades.md` quedo desincronizado hoy-; `leer_fichero` enumeraba `1|2|3` en vez de negar por defecto y el `..` se colaba; y `CARPETAS_RESERVADAS`, explicita a proposito, convive con un fallback a `holdout-1` que es una enumeracion con agujero. EL ARREGLO ES SIEMPRE EL MISMO: nombrar la condicion y negar por defecto. **(4) UNA RESTRICCION ELEGIDA SE DISFRAZA DE RESTRICCION DEL MUNDO -Y AL REVES-, Y DESDE DENTRO LAS DOS SE VEN IGUAL.** Tiene DOS CARAS y separadas no sirven. **LA CARA DEL FALLO**: una restriccion ELEGIDA por nosotros pasa por restriccion DEL MUNDO y deja de revisarse. Medido el 2026-09-22: "este repositorio no tiene Pillow" -CIERTO, y es una decision de dependencias- se convirtio en "no hay extraccion programatica de pixeles" -FALSO: un PNG se decodifica con `zlib` y `struct` de la biblioteca estandar-, y con esa premisa se derivo una CONDICION DE MATERIAL que no existia ("hace falta una caja >= 100 px"). **LA CARA CONTRARIA**, ya escrita en **ADR-0038 decision 3** y hasta hoy sin conectar con esta: una regla general que PARECE elegida de mas y en realidad LA FUERZA EL MUNDO, porque la comprobacion no llega a tiempo -el rango que cubre una captura de Analytics no se puede conocer ANTES de abrirla, asi que se prohibe la clase porque la instancia no se puede comprobar-. **LA REGLA QUE SALE DE LAS DOS: antes de ACEPTAR o de RELAJAR una restriccion hay que establecer DE CUAL DE LAS DOS CLASES ES**, porque desde dentro se ven iguales. Las dos veces que esta semana se confundieron costaron algo: una, un "no concluyente" con el motivo equivocado; la otra, estuvo a punto de relajar una regla que protege de una quema IRREVERSIBLE. **(5) LO ESCRITO Y LO EJECUTADO SE SEPARAN, Y NADA LOS COMPARA.** **NO es el patron 3** -ese va sobre el CONTENIDO de una regla, enumerar en vez de nombrar la condicion, y aqui el contenido era CORRECTO: `git add PROJECT_STATE.md` mas mirar `--name-only` nombra la condicion exactamente-. **NO es el 4** -ese va sobre el ESTATUS de una restriccion-. Este va sobre **si lo que corre es lo que esta escrito**. TRES INSTANCIAS MEDIDAS, y van las tres porque el defecto corre EN LOS DOS SENTIDOS: (1) el 2026-09-22 el paso se ejecuto con `git add -A` en vez de nombrar el fichero -la puerta existia desde el 2026-09-17 y el commit paso igual-; (2) el `curl` del runbook estaba MAL desde el 2026-09-17 -le faltaba `--ssl-no-revoke`- y nunca se noto PORQUE QUIEN LO EJECUTABA LO ANADIA DE MEMORIA, o sea documento incorrecto y ejecucion corrigiendolo en silencio; (3) los briefs del consultor escribian `botsito ...` donde la maquina necesita `uv run botsito ...`, mismo eje y esta del consultor. **LA CONSECUENCIA, que es lo que lo hace regla y no anecdota: EL ARREGLO NUNCA ES OTRA PUERTA.** Es hacer que la forma escrita y la ejecutada sean EL MISMO OBJETO -nombrar el fichero elimina el "acuerdate de mirar"; el comando con sus flags elimina el "anadelo de memoria"-. Una puerta mas sobre un paso que se ejecuta de otra forma NO VE NADA, porque desde fuera las dos formas parecen la misma. **CUARTA INSTANCIA, del 2026-09-22 y otra vez del consultor**: dijo -y la sesion lo repitio sin contrastarlo, y el documento lo recogio- que `state check` falla entre el merge y el `docs(state)`. Medido: falla entre el merge y el TAG, y entre el TAG y la EDICION del fichero; con el fichero ya editado da OK. **DOS DIAS SEGUIDOS LA MISMA FORMA**: una instruccion del consultor que la sesion no contrasto con lo escrito ni con lo medido. **Y LA LINEA QUE FALTA, que se escribe para que nadie suponga que alguna guardia lo cubre: HOY ESTE PATRON NO TIENE DETECCION MECANICA.** La unica via es comparar el texto escrito con el que se ejecuto de verdad, y eso lo hace ALGUIEN LEYENDO, no un test. Las cuatro veces se detecto porque un fallo obligo a mirar. **QUINTA INSTANCIA, 2026-09-22, rama `trabajo/mayo-dev-ingerido`, y esta vez DENTRO DE DOCUMENTOS YA CERRADOS**: ADR-0037 §7 y `F14A-INGESTA.md` afirmaban que el caso NO lleva campo `objetivo` -«quitar el campo es el mecanismo; un comentario no lo es»- y `biblioteca.como_documento` escribia una clave `objetivo` con el texto «NO ES UN CAMPO», sin que la guardia cerrara las claves del caso: el comentario descartado, hecho campo. **Es la primera que NO la destapa un fallo**: la destapo medir la afirmacion del brief -«sin campo `objetivo`»- antes de commitear los seis primeros casos, que es la mitigacion del sub-caso aplicada. Arreglo: la clave desaparece -forma escrita y ejecutada, el mismo objeto- y la guardia pasa a lista CERRADA en caso, operacion y `fuente`, que caza tambien lo que nadie penso. Recuadro de correccion en los dos documentos, sin reescribir el cuerpo. **SEXTA INSTANCIA, del consultor y repetida por la sesion**: el runbook llevaba desde `4880079` (2026-09-22, rama `trabajo/lo-que-no-cabia-en-main`) una «puerta 2» `git diff --stat stable/<tag>..HEAD` justo despues del tag, y el bloque del ritual del cierre de mayo -que redacto la sesion- la repitio sin medirla. Tras el tag `HEAD` ES el commit del tag, asi que compara un commit consigo mismo: **SALE VACIA SIEMPRE**, y un diff entre commits ni siquiera ve lo estadiado. Una comprobacion que no puede fallar, escrita como si parara algo. Quitada en `trabajo/ritual-ventanas`, y el runbook gana la regla «ninguna comprobacion que pase siempre». **SEPTIMA INSTANCIA, de orden y sin dano**: en el cierre de mayo, `git diff --cached --name-only` y `git status --short` se corrieron ANTES del `git add`; salio vacio y ` M` en la segunda columna, y **la propia comprobacion lo delato** -con el fichero sin estadiar no puede dar la linea esperada-, asi que se repitio en orden. Es la forma sana del patron: la comprobacion bien escrita caza la ejecucion desordenada.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4). El RR realizado de agosto tiene suelo en 3,00 y la combinacion CONFIRMED de hoy -`base_calculo_objetivo: caja_completa` con `stop_fraccion_caja: 0.8`- predice 3,75: no cuadra. O la base es `riesgo_real`, o el stop del trader en su backtest no esta a 0,8 de la caja, y las dos tocan un parametro CONFIRMED. NO se decide con un mes y 18 filas, y sobre todo porque LA CAJA NO ESTA EN EL FICHERO: el RR medido es riesgo real por construccion, asi que un stop en el borde de la caja haria coincidir las dos lecturas. LA REPETICION ES PARTE DEL ALCANCE de `trabajo/mayo-dev-ingerido`; dos meses que coincidan mueven esto de una medida a un hecho, y entonces toca decidir.
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21). La regla `entrada +/- objetivo_rr x base_calculo_objetivo` tiene hoy DOS lecturas que difieren en un 25 % del recorrido. Puntuar contra 'la regla' sin decir cual de las dos es puntuar contra un numero que todavia no existe. Es la TERCERA redaccion de esta frase en el mismo dia. LAS DOS PRIMERAS LAS ESCRIBIO EL CONSULTOR EN EL BRIEF y se transcribieron a ADR-0037 y al informe, que hasta hoy se las atribuian a quien las redacto: EL FALLO FUE EN LA DECISION, NO EN LA REDACCION, y por eso la regla vigila EL BRIEF y no la transcripcion. La tercera no es error de nadie: la cadena era mas larga de lo que estaba escrito. La regla se amplia: una consecuencia para F26 no se escribe sin medir la cadena entera hasta ella, Y LA CADENA INCLUYE LAS AMBIGUEDADES ABIERTAS que cuelgan de los parametros que nombra.
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7). Esta en 47 de 47 filas de agosto, su RR implicito no tiene estructura (0,2 · 0,1 · -0,2 · 2,1 · 1,1 · 56,6) y en 4 de 47 cae DEL LADO DE LA PERDIDA -entre la entrada y el stop, las cuatro `sell` perdedoras-. NO se guarda en el caso y NO se le gasta al trader una pregunta por ella: no la miramos. Si algun dia hiciera falta, se pregunta con lo medido delante.
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a). DOS VECES EN UN DIA el corpus contesto una pregunta que estaba a punto de irse al trader: el objetivo -`ev-v2-001658-d02fb71a`, 'el ratio de riesgo-beneficio de 1 a 3'- y los parciales -`ev-v1-002313-6342a154`, `ev-v2-001819-60a1b0f1`-. Una pregunta al trader cuesta un hueco de sesion; una busqueda en el corpus no cuesta nada. LA FORMA MECANICA seria un campo en `ambiguedades.yaml` que obligue a declarar los terminos buscados, y NO se mete aqui porque es cambio de esquema en `knowledge/spec/` -con su trailer `Fuente:` y con el test que congela cuales estan RESUELTAS- y no se atornilla a una rama que cierra. CONDICION, escrita por el consultor el 2026-09-21 para que no sea 'alguna vez': **LA PROXIMA AMBIGUEDAD QUE SE ABRA lleva el campo, y el commit que la abra trae el cambio de esquema**. Hoy no se abre ninguna -A-33 no existe: la cerro el corpus sin abrirla, v6 0:17:07- asi que esperar no cuesta nada.
- JUNIO SIGUE SIENDO `dev` EN EL REPARTO DE LA SESION 1, Y ADR-0025 LO DESCARTO (2026-09-21, rama F14a). `dias_ingeribles` devuelve hoy 20 dias: 6 `dev` de mayo, 10 de JUNIO y 4 de septiembre. Hoy es inocuo -no hay xlsx de junio en el corpus, asi que no se ingiere nada- pero el dia que llegue uno, la ingesta escribiria 10 casos de un mes que el consultor descarto, sin que nada chille. El `config.yaml` del kit no tiene `cobertura_material`; el de fidelidad si. DECIDIDO POR EL CONSULTOR EL 2026-09-21, y el como importa: **NO se toca el reparto de la sesion 1** -es un artefacto commiteado y ANCLADO por blob, es la linea base contra la que se compara toda la semana, y sostiene la prueba de anterioridad por caso; reparticionar es legitimo (cero LABEL_CASE) pero el radio de explosion no se justifica para un defecto hoy inocuo-. **La guardia va donde se LEE**: `cobertura_material` al `config.yaml` del kit, mecanismo que ya existe (ADR-0036), ya tiene tests y declara SOLO POR TRAMOS, asi que no publica dias. Y **LA EXCLUSION TIENE QUE GRITAR**: un dia que este en un reparto y fuera de `cobertura_material` no se cae en silencio -se cuenta, se nombra el mes y se dice el motivo en la salida-, que es el mismo defecto que se acaba de arreglar en `casos_reservados` y el que a la sesion 1 le costo dos dias. **CERRADA** el 2026-09-21 en `stable/F14-cobertura`: una guardia aterriza sola. Y descargar ABRIL para la medida de A-18 anadiria 22 dias laborables mas al mismo agujero -un `kit build` NUEVO llama a `manifiestos_del_prefijo` SIN `datasets` y coge todo lo del prefijo-, asi que esta guardia va ANTES que la descarga. El paquete de la sesion 1 es INMUNE y esta medido: congela sus cinco datasets y se recompone con esos (ADR-0035, `cases/paquete.py:523-546`).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5). CONDICION FECHADA, no alguna vez: hoy NO hace falta y esta medido -`knowledge/cases/holdout/{1,2,3}/` tiene cuatro README y nada mas, y `knowledge/cases/fidelidad/` solo lleva ASIGNACION, que ADR-0036 declara que no es abrir; el material reservado vive en `knowledge/feedback/`, que cubren `casos_reservados` y `trazar(ocultar=)`, y en `corpus/`, que ningun codigo lee-. EL DISPARADOR: un fichero con una etiqueta, un precio o el detalle por operacion de un dia asignado a una particion reservada. Ese dia hay que anadir el camino a `CARPETAS_RESERVADAS` y nombrarlo en el contrato de importacion, en el MISMO commit.
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7). Es el ultimo hilo del patron: todo lo demas de `comprobar()` va ya por lo congelado del paquete. Con la lista de datasets congelada que se le pasa no cambia lo que declara -el prefijo solo filtra antes de seleccionar por id-, asi que hoy no miente; pero si alguien cambiara `dataset_prefijo` en el global, la declaracion de lectura de un paquete viejo se calcularia con un dato que no es suyo, y esa salida es el unico fichero que existe para ser creible (ADR-0033). Arreglo local: pasarle el config congelado como ya se le pasan los datasets.
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b). El universo son 42 dias y el paquete 40 porque los cupos suman 40: sobran `2026-05-25` y `2026-06-29`, que NO estan en `particiones.yaml`, ni en `casos:`, ni en `excluidos:` -lo unico que deja constancia de que existen es el contador `universo: 42`-. Los descarta el SORTEO por cupos y de forma REPRODUCIBLE: `asignar()` ordena por `sha256(seed:caso)` y reparte los cupos en orden, y con el seed commiteado quedan en los puestos 41 y 42 de 42. CONSECUENCIA: un kappa "sobre el universo" y uno "sobre el paquete" no son el mismo conjunto, y "las particiones se fijaron antes de etiquetar" cubre el PAQUETE y no el universo, porque esos dos dias no aparecen en el fichero que lo prueba. No son holdout: nunca estuvieron repartidos.
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6). `kappa_entre_sesiones` llama a `abrir` en un bucle sobre las particiones que TIENEN etiqueta en las dos rondas, y a `gastar_pregunta` UNA vez: para contestar una pregunta sobre `holdout-2` hay que firmar TODA particion reservada con etiqueta en esas rondas, o el comando falla entero. Quien llama no puede nombrar la particion que su pregunta abre. OJO AL HISTORIAL: hasta el 2026-09-21 por la tarde esto estaba anotado como una FUGA -'una autorizacion lee las etiquetas de los tres cubos'- y era FALSO. Medido: con etiqueta en holdout-1 y holdout-2 y firmada solo la de holdout-2, el comando FALLA nombrando `AUTORIZACION-holdout-1.md`, y ademas NO gasta la pregunta porque `abrir` lanza antes que `gastar_pregunta`. Fijado en `test_una_pregunta_abre_todas_las_particiones_con_etiqueta`. El arreglo -que el llamante nombre la particion y el resto siga en `excluir`- es RAMA PROPIA.
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta). `CARPETAS_RESERVADAS.get(resto[0], RESERVADAS[0])`: con `holdout-1` abierto para la pregunta en curso, `knowledge/cases/holdout/4/x.yaml` se leeria; y un `resto` vacio sale por `IndexError` en vez de `HoldoutCerradoError`. Su docstring dice 'niega por defecto' y eso es MAS de lo que el mecanismo sostiene. NO se arregla en la rama que endurece la puerta y el motivo esta medido: `leer_fichero` NO TIENE NINGUN LLAMANTE DE PRODUCCION -solo tests-, asi que HOY LA PUERTA PROTEGE UN SOLO COMANDO (`kit kappa --incluir-holdout`). El dia que tenga un llamante, esto entra con el.
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4). Medido: `CLAVES_VOCABULARIO["tokens"]` es `{descripcion, clase}`, asi que escribir `produce:` bajo un token lo rechaza `comprobar_vocabulario`; y `_problemas_lo_provoca` solo se invoca para predicados con `fuente` en (broker, bot) y para hechos de `origen: broker`, mientras que a los de `mercado` se les PROHIBE declarar `lo_provoca`. Por eso `liquidez_m15` -un objeto que dibuja una persona, no algo que el mercado produzca solo- lleva desde F11 sin productor y la spec sale verde. Arreglarlo es trabajo de F12/F14b con su ADR: hoy queda anotado y NO tapado.
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8). Se comprueba que los ids de `evidencia:` existan, nunca que las marcas de tiempo de la prosa tengan item. Se vio al validar: A-24 citaba "v3 0:39:16" -el item que sostiene su riesgo de fidelidad entero- sin tenerlo en su lista, y desde la ambiguedad no se llegaba a el; corregido a mano, y A-25 y A-26 revisadas igual y completas. La guardia no se hizo en esa rama: queda pendiente y es barata -cruzar cada marca `vN h:mm:ss` de la `pregunta` con el intervalo t0-t1 de los items de ese video-.
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20). `evidence/contradicciones.py` agrupa por tema IDENTICO y compara `valor`. (1) 2026-09-12, commit 2003e61: dos items que afirmaban 0,75 en temas hermanos, encontrados A MANO agrupando por parametro con el mapa del kit; (2) 2026-09-17, rama del breaker de M1: `entrada.breaker_m1_mecha_m15_cuerpo` frente a `no_trade.rompe_con_mecha_no_valida`, invisible tambien porque un item no tenia `valor`; (3) 2026-09-20: los ~10 items que describen que nivel es la liquidez de M15 viven en temas hermanos (`liquidez.m15.mas_reciente`, `.zona_mas_baja`, `.alto_mas_alto_en_pullback`, `.estructura_mas_reciente`, `.rango_completo_es_liquidez`...) y NINGUNO tiene `valor`. A la tercera deja de ser deuda: la proxima planificacion abre RAMA CON NOMBRE para ello -que agrupa, que hacer con los items sin `valor`, y si el mapa del kit es la vista buena-, y no se mete de matute en otra rama.
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5). `evidence/contradicciones.py` agrupa por tema IDENTICO y compara `valor`: un choque entre `entrada.breaker_m1_mecha_m15_cuerpo` y `no_trade.rompe_con_mecha_no_valida` le es invisible, y ademas el segundo item no tenia `valor`, asi que no entraba en la comparacion. Es la SEGUNDA vez: el 2026-09-12 (commit 2003e61) dos items que afirmaban 0,75 en temas hermanos se encontraron a mano, agrupando POR PARAMETRO con el mapa del kit. Arreglarlo es trabajo de F06 con su propio criterio de aceptacion -que agrupa, y que hacer con los items sin `valor`, que son la mayoria-: no se metio en esta rama para no mezclar una correccion de conocimiento con un cambio de mecanismo.
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3). El esquema de `knowledge/_proposals/` (`CAMPOS_ITEM_OPCIONALES`: valor, fotogramas, notas, marca_heredada) no lo lleva, y `evidence accept` tampoco, asi que TODA correccion de evidencia se sale del mecanismo de propuestas -sus guardias, el sello `salida_sha256` y la trazabilidad de que modelo la propuso- y va por `evidence new --supersede`, que verifica la cita igual pero no deja ese rastro. Los nueve supersede del proyecto se han hecho asi (2003e61 los ocho primeros, d588e21 el noveno). Hay que elegir: o el esquema de la propuesta admite `supersede`, o se declara por escrito que las correcciones van por otra via a proposito.
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2). `feedback pending` devuelve REFLEJADO sin mirar si el item objetivo sigue vivo, y el motivo que imprime -"un CONFIRM confirma un item que ya vive"- ya no es cierto desde el supersede de `ev-v4-005319-dee95093` (`cli.py`, `_estado_de_registro`). Ademas `kb find` filtra por activos (`retrieval/indice.py`), asi que el objetivo de `fb-2026-09-09-sesion-01-9deda56d` no aparece en ninguna busqueda: el registro sigue siendo cierto y su objetivo es inencontrable. Ninguna guardia se queja, medido; lo que falta es que el motivo diga la verdad y que la busqueda sepa llegar al item supersedido.
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09. Falta v6 -la sesion 1 entera, 2 h 27 min, fuente de los registros de feedback y 12 items de evidencia-: su cruda y su WAV no estan en Drive. Carpeta de Drive `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R` ("transcripciones (crudas, Bot v3)") con SHA256SUMS, LEEME, 5 manifiestos, 5 crudas (jsonl y txt), 5 WAV y v5 (el usuario subio los binarios el 2026-09-06; verificado por API). Una retranscripcion futura exige repetir la copia (nuevo SHA256SUMS via `docs/validation/anexos/F07-previos/staging.py`).
- Glosario ASR v2 APLICADO el 2026-09-06 (aprobado por el usuario): 29 terminos, 6 sustituciones globales y 6 de segmento; los 5 videos retranscritos con ids nuevos. Regla vigente: cambiar `vocabulario` cambia el `initial_prompt` y la huella y exige retranscribir; las `sustituciones` solo exigen `corpus glossary apply`. Las apariciones de `boss|voz|blog|blogs` y `split|sprint` fuera de los 6 segmentos verificados quedan como `dudas` en `correcciones.jsonl` (v2: 8, v3: 13, v4: 4) para que F07 las mire al citar. HECHO en F07: los items que caen en esos segmentos llevan `confianza: media` y la nota lo dice (94 items).
- Fotogramas obligatorios de F05 LEIDOS y REGISTRADOS como evidencia en F07 (`ev-v3-002856-bff84636`, `ev-v2-003320-a736fd37`, `ev-v4-001221-1e66b5fd`; ficha de Word `ev-v3-000138-*`; reloj `ev-v3-000136-6160fcea`): V3 0:28:56 el Excel muestra `2,83 / -0,75 / 3,3 / -0,75 / -0,5` (inferencia: la heredada `2,3 / 3,23` no coincide con la pantalla; large-v3 coincide en 2.83 y dice 3.33 donde hay 3,3); V2 0:33:21 herramienta de posicion `4,08` y `3,94` (golden F21 confirmado); V4 0:12:30 caja 0,75 = `1,19537`. Relojes de grafico en `UTC+2` en V2 (TradingView) y V4 (FXReplay); V3 0:01:41 "lo tengo configurado como utc mas 2": candidatos de A-9 para F07. Hallazgo: `fr-v3-982da728/101000` es la ficha de reglas en Word con las confirmaciones del trader (2 cartuchos "si" frente a "limito a tres" en V4 0:48:41: A-2; "probar sin parciales").
- RESUELTO en F07 (ADR-0009 §3): `validar_contra_manifiesto` y el `comprobar` de `evidence new` reciben las referencias conocidas (`ContextoEvidencia.referencias`, sin `heredado_v2`); `knowledge/evidence/README.md` fila `fotogramas` actualizada.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F04, pendientes tecnicos (i) y (ii) RESUELTOS el 2026-09-06 (previos de F07): huella sin GPU/driver (`CLAVES_FUERA_DE_HUELLA`), guardia de 223 tokens del prompt (`comprobar_prompt`), `hotwords` medido y descartado (ADR-0007 enmienda). (iii) `palabras` de la cruda bajo un texto corregido sin marcar: CERRADA por declaracion en F08 (`kb` muestra la corregida sin tiempos propios y la cabecera dice "tiempos de la cruda"; ADR-0010).
- Hallazgo F04 V4 1:28:20-1:28:37 (riesgo por operacion 0,40 o 0,50, escalado) REGISTRADO en F07: `ev-v4-012815-2aa13700`, `ev-v4-012733-0c8d7f1f`. Queda como pregunta candidata en F10.
- RESUELTA en F07 (ADR-0009; secuencia cumplida: glosario v2 -> retranscribir -> Drive -> evidencia). Regla de cita (decidida en la auditoria del 2026-09-05, ver MASTER_PLAN H fila F07): `cita_literal` se verifica contra la capa CRUDA (la que forma el id `tr-*`); la corregida es ayuda de lectura. Secuencia obligatoria: glosario v2 aprobado -> retranscribir los 5 videos (v1-v5) (`--reemplaza-a`) -> copia en Drive -> primera evidencia con `transcripcion:`.
- `mapa_parametros.yaml` CERRADA en F13: las `opciones` las sostiene el registro y la `ambiguedad`, `ambiguedades.yaml`. La premisa de esta deuda -que unificar rompia la reproducibilidad del paquete- resulto FALSA, medida al reves.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave). El control independiente es el usuario (acepto los 341 sin cambios; recall humano de V4 0:05-0:15 sin faltas). Dueno: si llega una clave, otro proponente rellena una propuesta del mismo tramo y se compara; mientras tanto no bloquea.
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- (CERRADA en F11: los dos tests se INVIRTIERON en vez de retirarse; ahora afirman que todo valor de estrategia cita al trader y que el feedback carga con ids unicos y supersede valido) ~~`test_fichero_real_sin_valores_de_estrategia`~~ (registro) y `test_directorio_real_valida`
  (feedback) afirman que no hay valores de estrategia ni registros: se retiran en F11 y en la
  sesion 1.
- El reloj de servidor del broker es una aproximacion (`17:00 America/New_York`) hasta que F17
  lo mida contra el terminal de FundedNext; HECHO en F11 como `broker_dst` y `broker_offset_base`, medidos contra la demo real; la tabla de transiciones DST para exportar sigue siendo de F28.
  Verificado el 2026-09-05 (lectura de solo consulta al terminal MT5 build 6180 instalado en la
  maquina de desarrollo, cuenta demo MetaQuotes): EURUSD digits 5 / escala 100000; H4 de servidor
  en 12:00, 16:00, 20:00; ultimo tick del viernes 23:59:55 de servidor = 20:59 UTC = 17:00 Nueva
  York con GMT+3. VERIFICADO tambien en FundedNext (2026-09-05, cuenta demo 34891752, servidor
  `FundedNext-Server 3`, FundedNext Ltd, USD, apalancamiento 100, balance 100000, margen hedging=2):
  ultimo tick del viernes 23:59:45 de servidor = 20:59 UTC; H4 en 08/12/16/20 y D1 en 00:00 de
  servidor; la M1 del 2026-07-02 15:00 de servidor (= 12:00 UTC) vale o=1.14039 h=1.14042
  l=1.14030 c=1.14038 (tick_volume 83) frente a Dukascopy 114037/114043/114031/114036: diferencia
  de 1-2 puntos, misma alineacion horaria. Instrumento EURUSD en FundedNext (para F11 por ADR y
  F33 pre-vuelo): digits 5, point 1e-5, contrato 100000, lote 0.01/0.01/40, stops_level 0,
  freeze_level 0, filling 3 (FOK|IOC), expiration 15, ejecucion market, ruta Forex\EURUSD,
  spread 12 puntos con mercado cerrado. Queda por medir en invierno (GMT+2) en F17.
  DESDE EL 2026-09-14 ESTA MEDICION NO VALE COMO MEDICION (ADR-0026): la firma es FTMO. Los cinco
  del instrumento corren como default declarado bajo A-27 y el reloj del servidor esta sin valor
  bajo A-28; todo se vuelve a medir en la prueba gratuita de FTMO.
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.

- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica). `feedback apply` reescribe la unica puerta de los valores editando por lineas: funciona y se niega si el formato no es el suyo, pero es la pieza que mas vigilancia merece cuando el fichero crezca. Las cadenas de supersede y `feedback pending` quedaron CERRADAS en F13, y con una correccion de enunciado: la cadena si se recorria entera -comparar con el predecesor inmediato ya es transitivo- y lo que faltaba era que una correccion no pudiera llegar antes que lo que corrige. Y `kit check` avisa -no falla- cuando el paquete de una sesion celebrada ya no se reproduce, que es lo esperado desde que el registro tiene las respuestas.
## Open Questions
- Fuente de ticks historicos: decidir en F16.
- Ruta local de trabajo: C:/Users/USER/Desktop/Bot v3.
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

## Next Feature
F14 (biblioteca de casos), que se abre con F11 igual que F12 y F13 (MASTER_PLAN §D). Se construye con MAYO, que ya esta en el corpus; junio quedo descartado por decision del consultor el 2026-09-12. Hereda de F13 `feedback pending` fiable y el esquema del feedback con `recibido_el`, y de ADR-0033 la guarda del holdout y la puerta `botsito.cases.holdout`, ya hechas: su ingesta del xlsx tiene que pasar por la puerta.

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`; el I, 2026-10-01, al cerrar `trabajo/guardias-claude`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

B. **HECHA** (2026-09-30, `stable/F36b-contador-peticiones`). **Un contador de peticiones al servidor en el broker simulado**, informado por dia en el arnes. Estuvo EN REVISION en `feature/contador-peticiones` (docs/validation/CONTADOR-PETICIONES.md): cuenta colocar, modificar, cancelar y cerrar, aceptadas o rechazadas, por dia CE(S)T; sobre construccion, maximo diario 1 frente a 2000; solo mide.

C. **Medicion PRE-REGISTRADA de R1 a R6** (docs/validation/BLOQUE-DE-LA-CAJA.md §1.4) sobre las 77 operaciones de construccion, contra la entrada y el stop de los libros, con el stop en el 0,8 y en el 1. El criterio se escribe y se commitea ANTES de medir. HECHA (2026-09-30, `stable/F36c-caja-77`, docs/validation/CAJA-77.md): criterio y nota del consultor commiteados y subidos antes de medir; VEREDICTO NO DECIDE -ninguna regla llega al 40 % (maximo 16 % en la celda principal)-; R4 gana a R1 solo con el stop en el 1; el stop del libro casa mas con el 1 de la caja de pantalla (3 de 5) que con su 0,8 (0 de 5). Las dos preguntas van a la sesion 4 (F). Exploratorio (§3, posterior al resultado): el 0 de R5 y R6 localiza la entrada (36 de 77, frente a 18 con el placebo a 5 puntos) y el pivote de R5 casi siempre es uno de M1 formado DESPUES de la toma del productor (56 de 77), no Esquema.referencia (5).

D. **F35: la orden stop nace en el 0 de la caja**; el bloque, por selector, segun el resultado de C (A-48, A-49). HECHA (2026-09-30, `stable/F36d-orden-stop-pivote`): ADR-0064 ACEPTADO en su direccion, con los valores DEFAULT_AMBIGUOUS bajo A-48 y A-29. Estuvo EN REVISION en `feature/F35-orden-stop-pivote` (ADR-0064, docs/validation/F35-ORDEN-STOP-PIVOTE.md): la orden nace en el ultimo pivote de M1 con la caja de R6; en diagnostico sobre construccion la cobertura pasa de 0 a 2 de 77 y el maximo diario de peticiones a 7 frente a 2000; `r6` y `r4` no se distinguen; `referencia_de_la_toma` da 0 de 77. El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor. OJO: en MASTER_PLAN, F35 es el go-live gate.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 19 por preguntar -las 17 del barrido y 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

G. **Rama de codigo: RN-014, break even al tick («apenas toca»); hoy al cierre de la M1** HECHA (2026-10-01, `stable/F36h-be-al-tick`, ADR-0065 PROVISIONAL, docs/validation/BE-AL-TICK.md): el stop pasa a la entrada en el primer tick que pasa el nivel; pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6). (orden del consultor del 2026-09-30, revision de `feature/reflejar-feedback-s3`). RN-014 cita ya la correccion de la sesion 3 (fb-2026-09-29-sesion-03-9f506366), pero el motor evalua la estrategia al cierre de M1 (ADR-0028) y mueve el stop en el cierre de la M1 que toca, no en el tick (ADR-0053 §2.1). docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

I. **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

LO QUE DECIA NEXT ACTION HASTA EL 2026-09-30, sustituido por la lista de arriba. De A3, las ramas a, b, c y 0 quedaron HECHAS en `stable/F36-nocturno-01oct` y d es la D de arriba; A4 quedo HECHA en `stable/F31c-memoria-suite` y `stable/F31d-ci-linux-memoria`; lo de A5 que no esta en F sigue pendiente para la sesion 4:

**URGENTE · la comision real de FTMO (por lado o por operacion) decide la viabilidad: ejecutar MedirDemoFTMO en cuanto exista la cuenta de prueba (paso 6).** (2026-09-28, orden de cierre de `trabajo/viabilidad-trader`: con stops de mediana 15 puntos, 5 USD por lado cuestan 0,86 R de media, y la esperanza neta cruza el cero; docs/validation/VIABILIDAD-TRADER.md §2.)

**LO QUE ERA AHORA HASTA EL 2026-09-30** (2026-09-28, orden de cierre de `trabajo/demo-ftmo-script`):

A1. **Sesion 03 con el trader: HECHA y ACTIVADA** (2026-09-29: extraccion en `stable/F30-sesion-03`, docs/validation/SESION-03-EXTRACCION.md; activacion en knowledge cerrada en `main` en `stable/F31-activar-sesion-03`, docs/validation/ACTIVAR-SESION-03.md, con A-42 PROVISIONAL por ADR-0059). Lo que dice la spec y el motor todavia no hace esta en ACTIVAR-SESION-03.md §3: es la lista de A3.

A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes del 25 de octubre, entre el 26 y el 30, y despues del 1 de noviembre. Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
   a) **sesgo**: RN-003 y RN-033 (siempre hay sesgo; la doble ruptura la decide el color) y RN-002 (cierre un minuto antes del fin de la vela H4, sobre la rejilla de anclaje_h4);
   b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion (A-46), y la caja por operacion (ADR-0056 §4, rama 4);
   c) **gestion**: `stop_fraccion_redondeo` hacia fuera (hoy ROUND_DOWN hacia la entrada), RN-004 en la vela de M1 (hoy la M15 cerrada, PROVISIONAL por ADR-0054 §4) y el break even al tocar;
   d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
   0) **REQUISITO PREVIO de cualquier corrida sobre meses de invierno, incluida fidelidad-dev: separar el reloj de las sesiones (grafico, UTC+2 fijo segun A-42 provisional) del reloj del dia de riesgo (FTMO, Europe/Prague)** (desalineacion 9 de ACTIVAR-SESION-03.md §3; ADR-0059). Hoy los dos son huso_operativa.
   e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).

A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El 2026-09-29 una corrida de `pytest` en segundo plano la corto el recorte de procesos en segundo plano de Claude Code por memoria libre del SISTEMA al 69 % (se evita con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`, CLAUDE.md, Trampas medidas). `motor arnes` ya no usa `tracemalloc` salvo con `--tracemalloc`, y `make check` escribe su pico en la ultima linea del log. **PENDIENTE, NO APLICADO (orden del consultor del 2026-09-29): la propuesta de cambiar ADR-0057 §5 para que la negativa por A-27 llegue ANTES de leer velas, como la de A-47.** Hoy la da el broker al colocar la primera orden stop, tras leer velas y ticks (ACTIVAR-SESION-03.md, recuadro de correccion); no se adelanta hasta que el consultor decida.

A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de 3 R frente a «objetivo fijo» (G-2; ACTIVAR-SESION-03.md §4.1, antes medir su caja en el fotograma); A-51 (que corta la racha de 9 perdidas y cuando vuelve a operar); A-50 y A-21 con sus lecturas candidatas; E-1 (cual de las dos versiones del backtest vale); y lo que taparon los cortes de audio en A-39 y A-13, si no llega antes el audio de respaldo.

Lo anterior, numerado como estaba (historial y pendientes con dueno):

0. HECHAS: abril (tag `stable/F14-abril`), la caja (tag `stable/F14-caja`), mayo `dev` ingerido (tag `stable/F14-mayo-dev`, 2026-09-22) y el ritual con sus ventanas (tag `stable/F14-ritual`, 2026-09-22).

1. HECHA: `trabajo/ritual-ventanas` (tag `stable/F14-ritual`, 2026-09-22): el runbook dice lo que se ejecuta, ADR-0033 aparece una sola vez en el indice y la regla de los briefs esta en `CLAUDE.md`. Ver punto 5.

2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto febrero NI marzo, y backtestea MARZO (lo declara el consultor; no hay captura en el corpus). Al entregarlo: el xlsx al corpus, marzo a `vistos.yaml` con `visto_el` = la fecha en que lo backtesteo citando el commit de entrega, y su `cobertura_material` declarada. Es material del CAMINO DE FIDELIDAD (ADR-0036), para `fidelidad-2` y `fidelidad-3`. La confirmacion por escrito se registra en F09 como CONFIRM sobre el objetivo `paquete <sesion>`: **sin sus palabras, no vale**.

3. **HECHO en `trabajo/v5-instantes`: 0 de 36 fotogramas sirven; la medida NO ESTA en v5 y la via se cierra; A-18 sin cambios (docs/validation/V5-INSTANTES.md).** CORREGIDO el 2026-09-23: son SEIS, no cinco -el 1, 2, 3, 4, 6 y 7; el 5 cuenta como abierto (`000216000` a +2 s, `000225000` a +11 s) y `000292000`-`000293000` no se asignan ni al 6 ni al 7 (decision del consultor)-; ventana fija t..t+5 s, 36 fotogramas; criterio en `docs/validation/V5-INSTANTES-CRITERIO.md`. Texto original: LOS CINCO INSTANTES SIN ABRIR, en rama corta y CON CONDICION ESCRITA: la transcripcion de v5 localiza SIETE instantes y solo se han abierto fotogramas de DOS. **Sirve el fotograma en el que los niveles 0 Y 1 de la caja tengan LINEA PROPIA visible y la herramienta de posicion este valida.** Si ninguno de los cinco la cumple, se escribe que la medida NO ESTA EN v5 y se cierra esa via. Va con el punto 4, no antes.

4. **HECHO en `trabajo/v5-instantes`: `scripts/decodificar_png.py` con su test de los cinco filtros sobre PNG autogenerados (`3f40481`).** Texto original: EL DECODIFICADOR DE PNG ENTRA AL REPOSITORIO, decidido por el consultor el 2026-09-22, con TRES condiciones. (a) En `scripts/`, que YA EXISTE -comprobado contra `tests/unit/test_tree.py:32`, que lo lista, en vez de supuesto: no hace falta directorio nuevo-. (b) **CON TEST, y el test FABRICA SU PROPIO PNG** con los cinco filtros (None, Sub, Up, Average, Paeth) y comprueba los pixeles, porque `data/fotogramas/**` esta fuera de git y porque **un filtro mal implementado no revienta: da una medida ligeramente falsa con cara de exacta**. (c) Cero dependencias nuevas, `pyproject.toml` sin tocar: sale entero de `zlib` y `struct`. Entra en la rama del punto 3, que es su primer consumidor.

5. **HECHA en `trabajo/ritual-ventanas`** (`0f45986` el runbook, `4747d25` la regla en `CLAUDE.md`). Historia: CERRADA el 2026-09-22 `trabajo/lo-que-no-cabia-en-main` (tag `stable/F14-runbook`, 2026-09-22). Las tres deudas del cierre -la nota de ADR-0038, el ritual y los comandos- estan aplicadas. **PERO DEJA UNA SUYA, medida el mismo dia y DESPUES del tag, asi que no cabe en `main`:**

   **Su deuda -`RITUAL.md` decia en las lineas 67 y 78 que `state check` fallaba «entre el merge y el `docs(state)`», y asi ensenaba a ignorar el unico caso que tiene que parar- queda APLICADA en `trabajo/ritual-ventanas`**: las ventanas A/B/C viven ahora en `docs/runbooks/RITUAL.md`, medidas, y la anulacion que esta entrada imponia sobre esas lineas deja de hacer falta.

   **Y LA EXTENSION DE REGLA QUE ESTA ENTRADA DEJABA SIN COLOCAR, HECHA** en `trabajo/ritual-ventanas` (`4747d25`): «toda afirmacion del consultor sobre como se comporta un mecanismo se mide antes de escribirla en ningun documento; si la medida la contradice, gana la medida y se dice con su nombre» vive ahora en `CLAUDE.md`, «Como se trabaja», junto a «se contesta MIDIENDO, no razonando». La segunda mitad la anadio el consultor al colocarla el 2026-09-22. **Sigue siendo la mitigacion BARATA DEL SUB-CASO: el patron 5 entero continua SIN DETECCION MECANICA.**

6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es el acto que devuelve el universo ciego a un numero distinto de cero: **rama propia y declaracion**, no una descarga suelta.

7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un paquete CIEGO, y ADR-0025 solo lo saca del de F14 por no haber decision suya con la que COMPARAR; un paquete ciego no compara, HACE ETIQUETAR. Es el PATRON 2, validado por el consultor. **NO se arregla sin contestar antes**: el reparto de la sesion 1 tiene ONCE dias de junio RESERVADOS y nada medido impide que un `kit build` nuevo coloque uno de esos once en `dev`.

8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se abre sin el. ANOTADO Y MEDIDO, porque cambia como se leen: los cuatro son `2026-09-01`, `2026-09-04`, `2026-09-17` y `2026-09-18`, o sea los puestos 1, 4, 13 y 14 de los 14 laborables. LA MUESTRA ESTA EN LOS EXTREMOS y no reparte el mes: la semana central (7-11) no tiene ni uno. Sirven para comprobar la INGESTA y el FORMATO contra un mes distinto, que es para lo que se sortearon, y NO se leen como representativos de septiembre. El sorteo es reproducible con el seed y no se toca por esto: es una propiedad de la muestra que hay que declarar al usarla, no un defecto que arreglar.
9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build` EN SILENCIO. Dos manifiestos con el prefijo del kit que cubran el mismo dia hacen fallar `universo()` con `dos datasets cubren el mismo dia: ids de caso repetidos`, y `reemplaza_a` NO salva: se ESCRIBE para datasets y nadie lo LEE -`manifiestos_del_prefijo` coge todo lo del prefijo sin mirarlo; para fotogramas si existe la nocion de extraccion activa, para datasets no-. LA DESCARGA DEL 2026-09-21 NOS ATA AL RANGO 2026-09-01..20, que era el maximo legal (`congelar` rechaza `hasta >= hoy`). SI EL TRADER ENTREGA DEL 19 AL 30, o si alguien quiere el mes completo en octubre, se choca con esto: hay que resolverlo ANTES de volver a descargar 2026-09. Es la misma clase de defecto que ADR-0035 arreglo, un escalon mas abajo.
10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para 100.000 y su region, con su apalancamiento-; abrir la prueba gratuita de FTMO y medir A-27 y A-28 (digits, contrato, lote minimo, paso y maximo, stops y freeze level, modos de llenado, desfase del servidor, rejilla H4 real); grabar spread y ticks de esa demo desde el primer dia.
11. **HECHA: `trabajo/guardia-ids-docs`** (tag `stable/F14-guardia-ids`, 2026-09-23). Texto original: **SIGUIENTE: LA GUARDIA DE IDS SOBRE `docs/**`.** La guardia que comprueba que un id `ev-*` citado EXISTE (`cases/ambiguedades.py:170` y `cases/paquete.py:1150`, dentro de `knowledge validate`) solo corre sobre `knowledge/**`; ningun test recorre `docs/**`, y medido el 2026-09-22 hay 104 ids `ev-*` citados ahi y TRES que no existen. La deuda esta en Technical Debt, anotada DOS VECES con redacciones distintas: la rama que la pague deja una sola entrada.
12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato y huso medidos por el metodo de velas con control (ADR-0039). Aleks no abre el fichero antes. Febrero no se toca ni se descarga. Complementa el punto 2 -la entrega: corpus, `vistos.yaml`, `cobertura_material` y la confirmacion del trader-, que no cubre la declaracion de lectura del libro.
13. **HECHA: `trabajo/regla-mes-sin-filas`** (2026-09-23): la regla se mantiene, con el mensaje reescrito y los tests por la CLI que faltaban. Texto original: **SIGUIENTE: DECIDIR LA REGLA «MES PEDIDO SIN FILAS» ANTES DE QUE LLEGUE MARZO.** `ingerir` sigue tratando como ERROR un mes pedido sin ninguna fila en el libro. Desde ADR-0039 el mes lo declara el sha del libro, asi que esa regla ya no hace falta para cazar un libro equivocado y solo le queda su falso positivo: si un mes llega con cero operaciones en todos sus dias ingeribles, el libro CORRECTO se rechaza. Esta en Technical Debt («EL MES DEL MATERIAL SE DEDUCE DE LAS FILAS», pagada en parte en `trabajo/mayo-dev-ingerido`). Se decide ANTES de marzo porque marzo es el primer libro nuevo que pasara por `casos ingerir` (punto 12): quitarla, mantenerla o convertirla en aviso, con su test.
14. **HECHO en `trabajo/a18-transcripciones`: 0 de 42 pasajes responden con la regla congelada; se pregunta al trader (docs/validation/A18-TRANSCRIPCIONES.md).** Texto original: A-18: buscar en TODAS las transcripciones del corpus (no solo v5) los pasajes donde el trader explica donde pone el stop respecto a la caja y como calcula el TP. Rama propia.** Regla fijada antes de buscar: un pasaje RESPONDE si dice ambas cosas, o si dice una sola de forma incompatible con uno de los dos supervivientes. Si hay pasajes en sentidos opuestos, o ninguno responde, se pregunta al trader con la pregunta abierta de `docs/validation/V5-INSTANTES.md` (seccion «Pregunta al trader», de reserva hasta entonces); su respuesta entra como feedback (`fb-*`) por su regimen.
15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la de `docs/validation/V5-INSTANTES.md`). Su respuesta entra como `fb-*` por su regimen, y con ella se decide si A-18 se replantea: en v1-v4 el stop se describe en DOS tiempos (lote sobre la caja entera, stop protegido a 0,75 tras la entrada) y las dos hipotesis vigentes suponen uno solo.
16. **HECHO en `trabajo/v6-fuera-del-holdout`: el dia reservado de v6 sale del holdout y no se sustituye (ADR-0041, `knowledge/cases/retirados.yaml`); medidos 33, `fidelidad-1` se mide sobre 9 (docs/validation/V6-FUERA-DEL-HOLDOUT.md).** Texto original: decidir, en rama propia y antes de usar el holdout, si el dia reservado de v6 se retira del holdout (exposicion posible + identidad revelada en `cdcf58e`; las dos declaradas en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
17. **HECHO en `trabajo/casos-agosto-abril`: 41 casos `dev` (6 mayo, 16 abril, 19 agosto), abril y agosto por el reparto dev-visto (ADR-0042); los 4 `fidelidad-dev` quedan fuera porque solo los cubre el libro de septiembre, sin sha (docs/validation/CASOS-AGOSTO-ABRIL.md).** Texto original: ingerir agosto, abril y los 4 `fidelidad-dev` por el camino de mayo, en rama propia (decision del consultor, docs/validation/INVENTARIO-FIDELIDAD-DECISIONES.md). D1 ya decidida: la verdad es el xlsx, y «no opero» solo en los dias que el libro cubre de verdad (`cobertura_material`); el instante que se compara es el que registra el xlsx.
18. **HECHO en `trabajo/criterio-fidelidad`: el criterio de fidelidad en desarrollo (ADR-0043), con su funcion pura de emparejamiento y metricas sin motor, y la medida de que el instante del xlsx es el LLENADO (docs/validation/CRITERIO-FIDELIDAD.md).** Texto original: criterio de fidelidad, commiteado antes de construir el motor: que se compara (D1: el xlsx), que instante (el que registra el xlsx), que tolerancias, como se tratan las ausencias (ADR-0016) y que cuenta como acierto. Los dias del tramo y las sesiones sin operacion son hoy RECUENTOS, no `no_trade`: si cuentan se decide aqui, antes de ver resultados del bot.
19. **HECHO en `trabajo/motor-sesgo-h4`: el sesgo H4 en el dominio (RN-003, ADR-0044), con A-34 abierta y un diagnostico sobre construccion -58 a favor, 12 en contra, 7 ambiguos de 77- sin tocar mayo (docs/validation/MOTOR-SESGO-H4.md).** Texto original: motor, primera regla: sesgo H4 (RN-003), con test contra velas; sin tocar mayo. Mayo es el conjunto de MEDIDA de ADR-0043: se mide una vez por version de la spec.
20. **HECHO en `trabajo/a24-a21-a26-a34`: A-24 DECIDIDA por ADR-0045 -el pivote de M15 mas reciente ya formado-, y abre A-35, que hereda el bloqueo de RN-004 (docs/validation/A24-A21-A26-A34-CRITERIO.md).** Texto original: **la siguiente regla en orden causal es RN-004 (la liquidez de M15 se toma con cuerpo), y esta BLOQUEADA**: lee el token `liquidez_m15` y ningun `fijar` de la spec lo produce (el hueco del productor), y la regla que marcaria ese nivel es A-24, bloqueante. Antes de codificarla hay que decidir A-24: respuesta del trader o decision del consultor.
21. **HECHO en `trabajo/a35-pivote-formado`: A-35 no responde ni en las transcripciones (10 pasajes, docs/validation/A35-PIVOTE-FORMADO-CLASIFICACION.md) ni en 89 fotogramas (docs/validation/A35-FOTOGRAMAS-RESULTADO.md); va al trader con una pregunta abierta y sigue bloqueante.** Texto original: **buscar A-35 («cuándo un pivote de M15 está formado») en las transcripciones con el metodo congelado de A-24**: criterio y lista cerrada de terminos commiteados antes de buscar, una sola ejecucion con control positivo, clasificacion con la frase literal y la regla global aplicada por el consultor. RN-004 queda BLOQUEADA por A-35: no se sustituye por un parametro provisional, porque es un mecanismo y no una cifra.
22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la hoja justo despues de A-35, y desde ADR-0053 §9 A-44 justo despues de A-43) -la respuesta a A-35 desbloquea RN-004, que es donde se paran TODAS las sesiones del embudo del arnes (docs/validation/ARNES-MOTOR-LINEA-BASE.txt), y la de A-44 desbloquea RN-020, el siguiente bloqueo del bot despues de A-35 (docs/validation/CABLEADO-SIMULADOR.md §4)-, siguiendo docs/runbooks/SESION-DE-PREGUNTAS.md: antes, comprobar que el dia no es reservado y generar la hoja (`uv run python scripts/hoja_preguntas.py`, en la raiz y no versionada); durante, grabar con permiso, sin ensenar ningun grafico y reconduciendo si sale septiembre. Lleva las preguntas abiertas en el orden de la hoja (`ORDEN_SESION_02`): A-35, A-43, A-44, A-21, A-24 (confirmacion de la DECIDIDA), A-42; A-26, A-25, A-32; A-36, A-37, A-29, A-30, A-38; A-18, A-13, A-31, A-40, A-33; A-34, A-41, A-39. **Despues, registrar**: la grabacion al corpus (fuentes.yaml con el siguiente video_id, inventario, transcripcion y fotogramas) y cada respuesta como `FeedbackRecord` `RESOLVE_UNKNOWN` sobre su ambiguedad, `procedencia: trader_grabado`, con la cita de la cruda y `Fuente:`. Cerrar una ambiguedad toca los cuatro sitios de `CLAUDE.md`. Preparada en `trabajo/sesion-02` (tag `stable/F19-sesion-02-preparada`).
23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`, docs/validation/REGISTRO-MARZO.md: libro y 7 jpeg en el corpus con su huella; las imagenes, sin abrir y fuera del protocolo). Siguiente: el paso a (Aleks lee la columna de fechas), y el sorteo solo con A-42 RESUELTA por el trader en la sesion 4. Lo que decia: **EN PARALELO: MARZO cuando llegue el libro**, siguiendo docs/runbooks/ENTRADA-MARZO.md paso a paso (ADR-0046 §6). **La sesion para en cada PARADA**, y **en la PARADA B0, ANTES DEL SORTEO, mientras A-42 no este RESUELTA**: marzo se detiene tras el paso a, porque el sorteo congela `huso_operativa` en `ventanas.yaml` y no se repite (ADR-0046 §5), y en invierno el reloj civil del trader y el de su grafico, UTC+2 fijo, se separan una hora. Complementa los puntos 2 y 12, que siguen siendo la entrega.
24. **HECHO en `trabajo/blindaje`** (tag `stable/F14-blindaje`, docs/validation/BLINDAJE.md): la puerta automatica del commit -el sello de `make check` y los hooks que lo exigen- y el test del indice de ADR. Texto original: **RAMA DE BLINDAJE.** Dos guardias que hoy dependen de que alguien se acuerde: (a) **una puerta automatica del commit**: que un commit solo entre si el hash de su arbol tiene un `make check` en verde registrado, porque el 2026-09-25 volvio a entrar un commit con un test en rojo en `trabajo/sesion-02` (corregido con --amend antes de seguir), igual que `40759cb` en Technical Debt; (b) **un test del indice de ADR**: que `PROJECT_STATE.md` liste todos los ADR de `docs/adr/`, porque ADR-0045 falto del indice sin que nada lo viera (K-01, corregido en este cierre).
25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona de control limpia de la geometria de la entrada y toca RN-008, no RN-004. Cuando el trader responda A-35, se escribe el productor de `liquidez_m15` y RN-004 deja de estar bloqueada.
26. **HECHO en `trabajo/simulador-cuenta`** (tag `stable/F24-simulador-cuenta`, ADR-0050 §1): las cuatro decisiones estan escritas en el ADR y en el perfil `knowledge/cuentas/ftmo-2step-swing-100k.yaml`; la (d) queda NO EVALUABLE hasta que FTMO de cifra (punto 27). Texto original: **DECIDIDO POR EL CONSULTOR (2026-09-25), PENDIENTE DEL ADR DEL SIMULADOR** (docs/validation/FTMO-REGLAS.md §4): el simulador (a) modela los objetivos de beneficio y los dias minimos de cada fase; (b) mete la comision y los swaps dentro de la equity que vigila la firma; (c) lleva el volumen maximo y los limites de ordenes y posiciones como `firma_*` dentro de un perfil de cuenta; y (d) tiene una guardia de AVISO por incoherencia del tamano de posicion. Ninguna esta escrita todavia en un ADR, en el registro ni en la spec.
27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap trading prohibido; si un lote que varia con riesgo constante cuenta como «posiciones mucho mayores»; que es la «maximum capital allocation rule»; que significa el asterisco de «USD/LOT*»; y, si hay cuenta de prueba, medir A-27 y A-28 en la plataforma. Desde ADR-0050 (2026-09-25), dos mas que hoy son parametros SIN VALOR del perfil `knowledge/cuentas/ftmo-2step-swing-100k.yaml`: **si la comision de EURUSD se cobra por lado o por operacion completa** (`firma_comision_por_lado`; mientras tanto, supuesto conservador por lado, Decisions and Rationale) y **la cifra de la guardia de tamano de posicion**, que «substantially larger» no da (`firma_tamano_posicion_ratio_aviso`; mientras tanto la guardia queda NO EVALUABLE y lo dice).
28. **HECHO en `trabajo/arnes-motor`** (tag `stable/F18-arnes-motor`, docs/validation/ARNES-MOTOR.md, ADR-0048): el interprete del arbol de ADR-0030 y su arnes. Cada primitiva que se escriba se mide con `uv run botsito motor arnes --salida <fichero>` y se compara con la linea base (docs/validation/ARNES-MOTOR-LINEA-BASE.txt) con `diff`. Texto original: **SIGUIENTE: el arnes del motor**, en su propia rama.
29. **HECHO en `trabajo/huecos-motor`** (tag `stable/F18-huecos-motor`, docs/validation/HUECOS-MOTOR.md, ADR-0049): los seis huecos cerrados con las decisiones del consultor. Quedan de ahi, con dueno: A-34 (si el trader da el sentido de la doble ruptura, `ambiguo` desaparece y RN-033 queda para `insuficiente`); A-42 y A-43 (el reloj y el rango de la sesion); un estado PROVISIONAL del registro si el consultor lo quiere (ADR-0002 y ADR-0012); y, pendiente menor, `complementa` entre RN-033 y RN-001 y que el aviso de H3 lo respete, a revisar cuando la spec se toque por otro motivo. Texto original: **PENDIENTE DEL CONSULTOR: revisar los huecos de interpretacion H1 a H6 de ADR-0048**: H1, la forma de RN-003 no expresa AMBIGUO ni INSUFICIENTE; H2, las sesiones del motor salen de `knowledge/cases/kit/config.yaml` y la spec no las declara; H3, el orden por id dentro de una clase; H4, sin ticks ni broker simulado; H5, `permite` no cambia nada; H6, cada dia empieza de cero (PROVISIONAL, como lo que deja abierto A-39). Cada uno se resuelve con su ADR o su ambiguedad, no en el codigo.
30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor visor`, docs/runbooks/VISOR-DIAS.md, desde `stable/F25-visor-dias`). Con A-35 respondida, se escribe el productor de `liquidez_m15` y las primitivas de RN-004 (`alcanza_nivel`, `cruza`), y se mide con `uv run botsito motor arnes --simular --salida <fichero>` contra la linea base vigente (docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt), con `diff`. A-43 dice si una toma anterior a las 07:00 cuenta; mientras no responda, el rango de eventos empieza en la ventana.
31. **HECHO en `trabajo/simulador-cuenta`** (tag `stable/F24-simulador-cuenta`, docs/validation/SIMULADOR-CUENTA.md, ADR-0050): la capa de cuenta como funciones puras y el perfil FTMO en configuracion, SIN cablear al motor; el cableado va con el broker (punto 32) y sus huecos estan en ADR-0050 §5. Quedan para el consultor `firma_huso_corte` frente a ADR-0027 §alt. 3, la guardia de tamano sin cifra y la duplicacion vigilada con `parametros.yaml` (informe §5). Texto original: **SIGUIENTE RAMA: LA CAPA DE CUENTA DEL SIMULADOR.** Sin broker simulado el motor no puede producir ninguna operacion (ADR-0048, H4), y escribir el broker no basta: diez gates en DESCONOCIDO prohiben abrir hasta que se puedan evaluar (ADR-0049, H4). Lleva al ADR del simulador lo que decidio el consultor en el punto 26 y lo que ADR-0049 deja escrito: el gate DESCONOCIDO sigue estricto, y la cuenta persiste entre dias mientras la estrategia empieza cada dia de cero (H6, PROVISIONAL; el estado de estrategia entre dias espera a A-25, A-30 y A-38).
32. **HECHO en `trabajo/ticks-llenado`** (tag `stable/F24-ticks-llenado`, ADR-0051 ACEPTADO, docs/validation/TICKS-LLENADO.md): ticks de construccion congelados, modelo de llenado en engine/llenado.py y LOS TICKS SON OBLIGATORIOS para toda simulacion que cuente (ADR-0051 §8). Texto original: **SIGUIENTE RAMA: LOS TICKS Y EL MODELO DE LLENADO.** Sin ticks, el camino intravela sera PESIMISTA a partir del OHLC de M1; con ticks, el orden real (ADR-0049, H4). F16 (ticks) es precondicion del backtest fiel (ADR-0028) y el modelo de llenado depende de A-11, A-29, A-30 y A-38.
33. **HECHO en `trabajo/cableado-simulador`** (tag `stable/F24-cableado-simulador`, docs/validation/CABLEADO-SIMULADOR.md, ADR-0053 ACEPTADO): el motor de reglas cableado al broker y a la cuenta viva, `motor arnes --simular` y `motor visor --simular`; quedan PARA REVISAR 2.1 (con la demo en MetaTrader) y 5.1 (al implementar RN-030), y el hallazgo abre A-44 (punto 35). Texto anterior: **EL BROKER SIMULADO ESTA HECHO** (`trabajo/ticks-llenado`, ADR-0052 ACEPTADO, engine/broker.py y engine/simulacion.py); **QUEDA EL CABLEADO DEL MOTOR DE REGLAS AL BROKER**, con el contrato de ADR-0052 §5 y los huecos de ADR-0050 §5, en su propia rama. Texto original: **DESPUES: EL BROKER SIMULADO Y EL CABLEADO DE LA CAPA DE CUENTA AL MOTOR.** La capa de cuenta (ADR-0050, `engine/cuenta.py`) esta escrita y probada pero no enchufada: el broker produce las operaciones con sus marcas y sus cargos, y el cableado resuelve lo que ADR-0050 §5 deja descrito sin inventar: la forma incremental (`avanzar(estado, evento)`), el signo y el recorte de `perdida_dia_firma` y `perdida_total_firma` cuando la equity esta por encima de su base (importa en RN-032), las dos comparaciones (mayor o igual para los frenos de la estrategia, estrictamente por debajo para la firma), un solo reloj declarado, y el margen de ADR-0031 aplicado en la estrategia y no en la cuenta. En esa misma rama se implementa la decision del consultor sobre `firma_comision_por_lado` (supuesto conservador por lado, fuente decision, hasta que FTMO confirme).
34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE INVIERNO, 06:00-14:00 UTC cuando el trader esta en CET, ligada a A-42 (con que reloj cuenta la sesion): los ticks de construccion de hoy cubren solo 05-13 UTC, la ventana de verano; (b) el DESLIZAMIENTO, sin cifra hasta medirlo en la demo de MetaTrader (DN-3; entra por knowledge/simulador/llenado.yaml); (c) el SWAP, que hoy se cobra al corte de medianoche del huso del perfil hasta medir el corte real en la plataforma (DN-6, A-28). Y de ADR-0051 §8: cada mes que se vaya a medir necesita sus ticks descargados con el mismo procedimiento ANTES de medir; sin ticks no cuenta.
35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje de operar y cuando vuelve a contar-, la spec declara la magnitud (saldo o equity) y el corte de `perdida_dia` y `perdida_semana`, el cableado deja de tener ese hueco con nombre (ADR-0053 §3.3 y §9) y RN-020 pasa de DESCONOCIDO a evaluado: es el siguiente bloqueo del bot despues de A-35, medido en docs/validation/CABLEADO-SIMULADOR.md §4, y sin el la geometria sola no abre ninguna operacion. Se mide con `uv run botsito motor arnes --simular --salida <fichero>` contra la linea base vigente, con `diff`.
36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN LA DEMO DE FTMO LAS CUATRO DECISIONES DE ADR-0057** (2026-09-28, orden de cierre de trabajo/broker-ordenes-stop). Con un script que se prepara en su propia rama, en la demo de FTMO en MetaTrader: (1) a que precio se llena una orden stop que salta con hueco; (2) que hace el servidor con una pendiente en el nivel exacto y con una modificacion que la cruza; (3) contra que precio juzga una pendiente (bid, ask o el ultimo); y, SOBRE TODO, (4) el stops level de EURUSD, `firma_stops_level_puntos` en knowledge/cuentas/ftmo-2step-swing-100k.yaml, UNKNOWN (A-27): sin el, las ordenes stop solo corren en diagnostico (--diagnostico-a27). Cuando se mida, `instrumento_stops_level` de la estrategia tiene que llevar el mismo valor.
37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de cierre de trabajo/broker-ordenes-stop). En la linea base de construccion con limites aparecen rechazos del perfil por `volumen_max_lotes`: el lote que sale de un stop muy corto pasa del maximo de la firma (docs/validation/BROKER-ORDENES-STOP.md §3, los dos nuevos de la cascada ademas de los que ya habia). Se revisan en la rama 5 de ADR-0056 §8, con A-18.

## Last Stable Commit
1f597cb · merge: la guardia de Claude Code en Linux, y la CI de Linux antes del merge · tag stable/F36j-guardia-linux

## Change Log
- 2026-10-01 (65) · LA GUARDIA DE CLAUDE CODE EN LINUX, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 1f597cb, tag stable/F36j-guardia-linux; rama `trabajo/guardia-linux`, 4 commits). La CI del cierre anterior (ebb836b) salio roja: la guardia no reconocia rutas en Linux. Arreglo probado en la CI de Linux antes del merge, regla nueva en RITUAL.md y patron en ERRORES-RECURRENTES.md.
- 2026-10-01 (64) · LAS GUARDIAS DE CLAUDE CODE, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 00ce911, tag stable/F36i-guardias-claude; rama `trabajo/guardias-claude`, 4 commits, informe docs/validation/GUARDIAS-CLAUDE.md). El revisor encontro 0 bloquea, 3 importa y 3 menor; el consultor, 2 que el revisor no vio (los tramos de v6 y los guiones de la rama), arreglados antes del cierre junto con sus otras tres decisiones: el push a main como regla ask, la exencion de v6 solo con sus tramos bloqueados, y la rama siguiente, el I del Next Action. Primer cierre con el contrato fuera de la rama antes del merge (RITUAL.md).
- 2026-10-01 (63) · EL BREAK EVEN DE RN-014 AL TICK, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 16771c5, tag stable/F36h-be-al-tick; rama `feature/be-al-tick`, 3 commits, informe docs/validation/BE-AL-TICK.md, ADR-0065 ACTIVE y PROVISIONAL; spec 15.2.1, sin cambio de valor ni de forma). El stop pasa a la entrada exacta en el primer tick cuyo BID pasa el nivel; en el mismo tick manda lo que ya hay y el stop nuevo cuenta desde el siguiente; sin ticks, al cierre de la M1 y marcado. Medido en diagnostico con un control (la rama con `cierre` reproduce main linea a linea): cobertura 2 y 7 de 77, operaciones y maximo diario de peticiones (7) iguales; los mismos break even, de 19 a 60 s antes; posicion a posicion solo cambian dos (04-07 pos-o3 de 0 a -4 puntos, por el ASK, pendiente para la demo en ADR-0065 §6; 04-29 pos-o2 de -3 a -1). S-1: fb-2026-09-29-sesion-03-86dc2801 (correccion del consultor, CONFIRM sin valor sobre RN-033, sustituye a 1168f036) y fb-2026-09-29-sesion-03-39af36ee (CONFIRM sin valor sobre RN-003 con la misma cita); `feedback pending` en 0.
- 2026-09-30 (62) · EL FEEDBACK DE LA SESION 3 EN LA SPEC, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 0ba8dad, tag stable/F36g-reflejar-feedback-s3; rama `feature/reflejar-feedback-s3`, 2 commits, informe docs/validation/REFLEJAR-FEEDBACK-S3.md, sin ADR, spec 15.2.0). De los 9 registros que `feedback pending` daba por pendientes, 4 se citan (base_calculo_objetivo, RN-014, RN-015 con G-2, RN-007 con E-3), 4 pasan a «confirmaciones de valores ya fijados» por la opcion (b) del consultor -un CONFIRM que coincide con el valor vigente, o sin valor propio, no ocupa la cita, que es del registro que fijo el valor- y S-1 sobre RN-033 sigue pendiente por ser un CORRECT. Desalineaciones con el motor, sin tocarlo: RN-014 al cierre de la M1 (Next Action G) y RN-007 sin umbral (H). G-2 en fotogramas por instante localizado: 0 de 7 medibles (cuatro dias de abril sin video, el 29 sin eje de precios y el 7 de agosto fuera del backtest grabado); fotogramas y saldos vistos declarados en HOLDOUT-EXPOSICIONES.md.
- 2026-09-30 (61) · LA RECEPCION DEL BACKTEST DE MARZO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge e12a6dd, tag stable/F36f-registro-marzo; rama `feature/registro-marzo`, informe docs/validation/REGISTRO-MARZO.md, sin ADR). Ocho ficheros (el libro y 7 jpeg) movidos al corpus fuera de git, comprobado con check-ignore antes de mover, con su sha256 en el manifiesto y la recepcion en HOLDOUT-EXPOSICIONES.md; ninguno abierto. La propuesta del §4 queda ACEPTADA: marzo por el camino de fidelidad; A-42 se cierra como RESUELTA con el trader en la sesion 4, no por ADR, asi que marzo no se sortea ni se ingiere hasta entonces y la PARADA B0 no cambia; las 7 imagenes, sin abrir y fuera del protocolo. En docs/sesion-4/PREGUNTAS.md, dos preguntas nuevas: la primera (cuando pone la orden tras formarse el minimo o maximo de M1; el barrido la dejo PARCIAL) y la ultima (que son las 7 capturas de marzo).
- 2026-09-30 (60) · EL BARRIDO DE PREGUNTAS PARA LA SESION 4, VALIDADA tal cual y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 97feeb6, tag stable/F36e-barrido-sesion-4; rama `feature/barrido-sesion-4`, 1 commit mas el merge de main, documento docs/sesion-4/PREGUNTAS.md, sin ADR). Cada pregunta abierta se busco en el corpus ya ingerido antes de llevarla al trader: 17 por preguntar, cerradas y sin graficos por orden del consultor; 15 ya respondidas; 6 fuera de la hoja; ninguna solo de memoria. A-29, la caja de R6, A-36 y el break even al tocar ya tienen respuesta grabada, y cerrarlas es rama propia.
- 2026-09-30 (59) · LA VIDA DE LA ORDEN STOP, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge cf6b1bf, tag stable/F36d-orden-stop-pivote; rama `feature/F35-orden-stop-pivote`, 7 commits, informe docs/validation/F35-ORDEN-STOP-PIVOTE.md, ADR-0064 ACEPTADO en su direccion con los valores en DEFAULT_AMBIGUOUS bajo A-48 y A-29). La orden stop nace tras la toma en el ultimo pivote de M1 (`orden_stop_punto`), se reubica con cada pivote nuevo y lleva la caja de R6 (`caja_bloque`, `caja_se_fija`); el item ev-v7-001550-82e5cffc (la caja de R6 dicha por el trader en v7 0:15:50) entra con la rama. Tres rondas de diagnostico sobre construccion (§2, §4 y §5): cobertura de 0 a 2 de 77, 7 de 77 con la cuenta diaria; el stop no es mas corto que el del trader; el bot entra antes (0,9 frente a 2,5 minutos del pivote) y gana el 8 % frente al 43 %; el mid no salva ningun stop; ffmpeg se queda en la CI porque cuatro tests lo necesitan. Ningun valor por defecto cambio. El tag evita F35 en el nombre por el choque con el go-live gate de MASTER_PLAN.
- 2026-09-30 (58) · LA CAJA DE LAS 77, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 2a71827, tag stable/F36c-caja-77; rama `feature/caja-77`, 5 commits mas el merge de main, informe docs/validation/CAJA-77.md, sin ADR). Criterio (§1) y nota del consultor con el umbral, el control y el spread (§1.8), commiteados y subidos ANTES de medir; medida con scripts/caja_77.py: NO DECIDE (ninguna regla al 40 %), aceptado tal cual; parte exploratoria posterior (§3) con scripts/caja_77_exploratoria.py. Nace en F la pregunta de la orden en el ultimo minimo o maximo de M1.
- 2026-09-30 (57) · EL CONTADOR DE PETICIONES AL SERVIDOR, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge f2300c0, tag stable/F36b-contador-peticiones; rama `feature/contador-peticiones`, 1 commit, informe docs/validation/CONTADOR-PETICIONES.md, sin ADR). La B del Next Action: el broker simulado cuenta colocar, modificar, cancelar y cerrar, aceptadas o rechazadas, por dia CE(S)T, y el arnes simulado lo informa junto a `firma_mensajes_dia_max`; solo mide. Seis tests nuevos. CI de la rama en verde (run 36747536392).
- 2026-09-30 (56) · LA NOCHE DEL 30 DE SEPTIEMBRE, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 4507617, tag stable/F36-nocturno-01oct; rama `trabajo/nocturno-01oct`, revisada como `feature/nocturno-01oct` con `main` traido en 8d73cae, 10 commits, informe docs/validation/NOCTURNO-01OCT.md). F32, F33, F34 (en dos commits, la toma en M1 aparte) y F36; ADR-0060, ADR-0061, ADR-0062 y ADR-0063 ACEPTADOS con sus 14 decisiones nocturnas, ADR-0061 enmienda ADR-0029 §3 para el stop; RN-002 y RN-003 citan sus CORRECT de la sesion 3 y RN-033 queda como guardia del proyecto. spec 14.4.1. En diagnostico sobre construccion la cobertura queda en 0 de 77 hasta F35 y la caja por operacion. CI de la rama en verde (run 36741509804). Antes, el mismo dia: la CI roja de 67ab298 arreglada en `fix/ci-linux-memoria` (stable/F31d-ci-linux-memoria, CI de main en verde, run 36735891599).
- 2026-09-29 (55) · LA SESION 3 ACTIVADA EN KNOWLEDGE, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 269102c, tag stable/F31-activar-sesion-03; rama `trabajo/activar-sesion-03`, 1 commit, informe docs/validation/ACTIVAR-SESION-03.md, ADR-0059 PROVISIONAL). 24 registros de feedback de la sesion 3 y `feedback apply`; diez ambiguedades RESUELTAS (A-26, A-31, A-34, A-37, A-38, A-40, A-41, A-45, A-46, A-47); A-13 y A-18 abiertas con lo firme confirmado; `stop_fraccion_redondeo` nace; A-42 PROVISIONAL y abierta; A-51 nace bloqueante de RN-020. Ninguna forma ni linea del motor cambia. El make check sellado de la rama paso en verde (1369 tests, 14:21) con un pico de 769 MB en el proceso de pytest; la rama siguiente, `trabajo/memoria-suite`, mide y baja ese pico.
- 2026-09-29 (54) · LA SESION 3 CON EL TRADER, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 00fcced, tag stable/F30-sesion-03; rama `trabajo/sesion-03`, 2 commits, informe docs/validation/SESION-03-EXTRACCION.md, sin ADR). v9 entra al corpus con dos cortes sin audio; 62 items ev-v9-*; la hoja entera preguntada; detectadas 0 por codigo (dichos sin «pregunta») y localizadas a mano. Revision del consultor: el tramo de A-42 con mascara (sin operaciones, precios ni resultados; cinco nombres de un mes reservado al hablar de su backtest y del cambio de hora), los tres tramos de precaucion declarados como agregados vistos, E-1..E-3 definidos con el texto de la hoja y la nota en SESION-DE-PREGUNTAS.md. FTMO: el gap de dos horas ya lo decia R15; comisiones 50/50 en MT5 y 2,50 por lado sin confirmar en demo; el tamano variable, sin respuesta.
- 2026-09-28 (53) · LA VIABILIDAD CON LA COMISION Y LAS VARIANTES DEL STOP, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 5ed948f, tag stable/F29-viabilidad-comision; rama `trabajo/viabilidad-comision`, 2 commits, informe docs/validation/VIABILIDAD-COMISION.md, que NO se ensena al trader, sin ADR). Escenario de referencia, 5 USD de ida y vuelta, la comision de forex de FTMO desde el 29-09-2025 segun su actualizacion del 25-09-2025 (declarada por el consultor; la sesion no pudo leer la pagina; no confirmado en demo). La comision decide; V2 sale la mejor simulada, en parte por las operaciones que excluye el tope de 100 lotes. Las variantes V2-V4 son hipotesis de A-18. El parametro del perfil no cambia hasta el CSV de la demo.
- 2026-09-28 (52) · LA CORRECCION DE EVALUAR_FASE, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 06b936c, tag stable/F28-corregir-evaluar-fase; rama `trabajo/corregir-evaluar-fase`, 2 commits, informe docs/validation/CORREGIR-EVALUAR-FASE.md, enmienda en ADR-0050). La marca que el broker deja en el instante del cierre se procesaba despues del cierre y reabria la posicion en la equity; corregido el orden dentro de una operacion. Cuatro tests en test_cuenta y la primera regresion. Nota del consultor en VIABILIDAD-TRADER: el SUPERADA al 1 % es una pista a favor de un stop minimo, no una regla.
- 2026-09-28 (51) · LA VIABILIDAD DEL TRADER EN FTMO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge a3adb77, tag stable/F27-viabilidad-trader; rama `trabajo/viabilidad-trader`, 2 commits, informe docs/validation/VIABILIDAD-TRADER.md, que NO se ensena al trader, sin ADR). Veredictos al 0,5 %: la serie anotada pasa en abril y abril+agosto; la simulada no llega al objetivo y rompe la perdida diaria el 7 de agosto. Esperanza neta con intervalos que cruzan el cero. El recuadro del informe fija que los veredictos validos son los saneados; el error de `evaluar_fase` se corrige en `trabajo/corregir-evaluar-fase`. Next Action gana arriba la URGENCIA de medir la comision real de FTMO.
- 2026-09-28 (50) · EL SCRIPT DE LA DEMO DE FTMO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge f1f2ccb, tag stable/F26-demo-ftmo-script; rama `trabajo/demo-ftmo-script`, 1 commit, informe docs/validation/DEMO-FTMO-SCRIPT.md, sin ADR). tools/mql5/MedirDemoFTMO.mq5 compilado y sin ejecutar; el lector con cinco tests sobre CSV sinteticos; el runbook para Aleks. Ningun valor en parametros ni decision cerrada. Next Action rehecha: sesion 03, la demo de FTMO y las ramas de estrategia en pausa hasta la sesion 03.
- 2026-09-28 (49) · LAS DECISIONES SIN FUENTE DEL EMBUDO, REGISTRADAS, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 5cb4477, tag stable/F25-registrar-embudo; rama `trabajo/registrar-embudo`, 1 commit, sin ADR). A-50 abierta, no bloqueante y sin parametro; A-43 con su medida, sin tocar ningun parametro; EMBUDO-77 con recuadro (una toma es un pivote). No hay utilidad comun de lectura de trazas: solo la nota. El motor no cambia.
- 2026-09-28 (48) · EL EMBUDO DE LAS 77, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge e32a9d9, tag stable/F24-embudo-77; rama `trabajo/embudo-77`, 1 commit, informe docs/validation/EMBUDO-77.md, sin ADR). Medicion en diagnostico (A-35 cierre_vela_contraria, A-44 sin_tope, A-47 stop_en_ruptura, A-27 0) del primer paso en que el bot deja a cada operacion del trader, en el orden del pipeline real (las reglas antes que el broker; la stop con el precio ya roto es el rechazo precio_invalido). Los que mas matan: liquidez, sesgo y caja; la zona unica por dia (ADR-0055, sin la caja por operacion de ADR-0056 §4) esta detras de la mayoria. Ningun error de codigo; tres decisiones sin fuente, reportadas y no corregidas. Tres tests nuevos sobre hechos sinteticos.
- 2026-09-28 (47) · EL SELECTOR DE A-47 Y RN-011 CON ORDEN STOP, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 87d166e, tag stable/F23-selector-orden-stop; rama `trabajo/selector-orden-stop`, 2 commits, informe docs/validation/SELECTOR-ORDEN-STOP.md, ADR-0058 PROVISIONAL). entrada_tipo_orden UNKNOWN en el registro (spec 13.4.0) y A-47 lo cita; la CLI se niega con --simular y sin A-47 antes de leer velas; con stop_en_ruptura la stop va en el instante y al precio de la limite, y el recuadro de enmienda de ADR-0056 remite a ADR-0058 decision 2. Con limite_en_retroceso la corrida de construccion sale identica a main. Medida en diagnostico con --diagnostico-a27 0: con stop, 6 y 5 operaciones, 2 de 77 coincidencias, dos y un cierre por objetivo; el tipo de orden invierte que ordenes sobreviven. Nueve tests nuevos, uno de punta a punta por el arnes con el selector en stop. Aclaracion de ADR-0057 §4: una orden sin cotizacion se acepta sin juzgar, y en construccion no pasa ninguna vez.
- 2026-09-28 (46) · EL BROKER SIMULADO CON ORDENES STOP Y RECHAZO DE PENDIENTES, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 3a3dad7, tag stable/F22-broker-ordenes-stop; rama `trabajo/broker-ordenes-stop`, 1 commit, informe docs/validation/BROKER-ORDENES-STOP.md, ADR-0057 PROVISIONAL). La rama 1 de codigo de ADR-0056: la orden stop de entrada y el rechazo por precio invalido y por stops level; firma_stops_level_puntos UNKNOWN (A-27) con --diagnostico-a27. Fase 0 medida sobre main: 4 limites distintas del bot se colocaban del lado equivocado y se llenaban a su precio, todas por stop. La linea base con limites NO sale identica: 5 rechazos directos (el del 23 de abril, juzgado con la ultima M1 cerrada) y la cascada de RN-032, que deja de prohibir; operaciones del bot 9 a 6 y 9 a 5, saldo final de unos 90 760 a 94 269 y 95 269. Un test sintetico dependia del llenado falso y se corrigio el test. 16 tests nuevos, uno de punta a punta por el arnes con orden stop. Pendientes 36 (la demo) y 37 (volumen maximo, A-18) en Next Action.
- 2026-09-28 (45) · LA GUARDIA DE LA HUELLA EN MAKE CHECK, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 807f986, tag stable/F21-blindar-make-check; rama `trabajo/blindar-make-check`, 2 commits, informe docs/validation/BLINDAR-MAKE-CHECK.md). Sale del incidente del instalador sobre copias de trabajo/preparar-a47. Medido: aquel incidente no habria sellado -el sello ya se negaba con cambios sin estadiar-, pero el sello dejaba pasar un fichero estadiado a mitad, un cambio deshecho y un commit a mitad, y avisaba con codigo 0. La guardia compara una huella del arbol al empezar y al sellar, y con cualquier diferencia make check sale con codigo 1 y no sella. Lo que no ve: un fichero sin seguir creado y borrado entre las dos huellas. Siete tests nuevos y tres ajustados a la semantica nueva. Regla nueva en CLAUDE.md (ensayos en git worktree, raiz por argumento o variable de entorno, nada escribe durante make check). Sin ADR.
- 2026-09-28 (44) · LA ENTRADA CON LA RUPTURA, PREPARADA SIN CODIGO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 0a2914a, tag stable/F20-preparar-a47; rama `trabajo/preparar-a47`, 4 commits). Revision de diseno medida (docs/validation/DISENO-ENTRADA-RUPTURA.md): el broker simulado solo tiene orden LIMITE y una limite colocada al lado equivocado se llena en el tick siguiente a su propio precio, peor que el mercado (script de lectura en el anexo); RN-011 dimensiona y RN-015 coloca una limite en el cierre del breaker, cuando el precio ya ha roto; el productor traza una zona por dia desde la primera toma y no la recalcula. Dos correcciones del brief: ADR-0011 no es A-11, y RESOLVE_CONTRADICTION no cambia un parametro (CORRECT si). Decisiones del consultor (ADR-0056): selector entrada_tipo_orden (A-47) UNKNOWN con --diagnostico-a47, construido ya y activado solo con la confirmacion grabada; la orden stop del broker salta al toque y se llena al precio del tick mas DN-3 (PENDIENTE DE MEDIR EN LA DEMO); la pendiente mal colocada se RECHAZA, PROVISIONAL, y MT5 lo mide Aleks en la demo de FTMO; la caja por operacion solo con orden stop; A-21 no se amplia y nacen A-48 (bloque) y A-49 (momento), esta con en_formacion NO_IMPLEMENTADA y ADR-0028 sin tocar; tres selectores de stop y lote UNKNOWN, y las respuestas entraran como CORRECT de los CONFIRMED afectados; la vida de la orden stop -nace en el posible punto de breaker y se mueve con el (tercera lectura de A-29, mecanismo de RN-006)- con la lectura de RN-008 y el diagnostico de A-29 PROVISIONALES; cinco ramas de codigo empezando por el broker, cada una con su test de punta a punta por el arnes real y la linea base de la limite identica byte a byte. Tres items de evidencia de v7 (0:14:57, 0:22:01 y 0:24:03), ninguno en tramo no citable; el de 0:24:03 condiciona el tramo de velas del mismo color a que la siguiente cubra con la mecha a la anterior y NO dice que el bloque sea todo el tramo.
- 2026-09-28 (43) · EL BLOQUE DE LA CAJA, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge de2e100, tag stable/F20-bloque-de-la-caja; rama `trabajo/bloque-de-la-caja`, 5 commits, informe docs/validation/BLOQUE-DE-LA-CAJA.md con su salida y scripts/bloque_de_la_caja.py). Descriptivo, sin tocar motor, productor, RN-011, parametros, reglas, ambiguedades, evidencia ni feedback. Criterio y seis reglas candidatas escritos antes de medir; de 39 operaciones de agosto de v7 y v8 entran 12 cajas legibles, todas ventas (desde v7 n.o 16 el trader deja de dibujar la caja). Con el criterio escrito ninguna regla pasa de una caja a 2 puntos; con la vela en curso y el desfase OANDA-Dukascopy medido (+2, mediana) R1 y R4 llegan a 6; el consultor deja esas versiones como EXPLORATORIAS y concluye que el 0 de la caja no sale de los fotogramas y se pregunta. El productor no reproduce ninguna caja. Tras la revision, §5: el stop segun el momento (paso del 1 al 0,8 visto en v7 n.o 3, no en n.o 11 ni n.o 15; A-18 sigue abierta) y un recuadro de correccion: la caja de v7 n.o 2 medida era la primera y el trader la sustituyo. La regla 2 de SESION-DE-PREGUNTAS.md no salia de ningun ADR y cambia por decision del consultor: solo graficos de dias de construccion, cortados antes de la orden, sin operacion, sin resultado y sin fecha, y primero la pregunta en abstracto. El material de la sesion 03 (graficos, clave y preguntas) esta fuera del repositorio. Sin ADR.
- 2026-09-28 (42) · ORDEN STOP O LIMITE, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge f792cd4, tag stable/F20-orden-stop-o-limite; rama `trabajo/orden-stop-o-limite`, 5 commits, informe docs/validation/ORDEN-STOP-O-LIMITE.md con su salida y scripts/orden_stop_o_limite.py). Criterio escrito antes de medir: con ticks, las 77 entradas de construccion llegan al nivel desde el lado de la ruptura (77 STOP, 0 LIMITE); las 7 etiquetas legibles de las parejas de v7 y v8 son stop. Dos controles: la unica Sell limit real (v7 n.o 6) salio ambigua y el consultor la dejo como no informativa; con llenados limite del simulador, las limites en espera no salen STOP (0 de 3) y las colocadas con el precio ya pasado si. Decision del consultor: el metodo queda ACOTADO -descarta la limite de antemano de RN-011, no separa una stop de una limite ya pasada-. Control sintetico en tests. Recuadros de correccion en SESION-02-VIDEO-V8.md §0.4 y SESION-02-VIDEO.md (n.o 23 DUDOSA). Deuda nueva: el broker simulado llena al instante una limite colocada al otro lado del precio. Sin ADR; A-47 sigue ABIERTA.
- 2026-09-27 (41) · LA SESION 02 EN VIDEO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 408b609, tag stable/F19-sesion-02-videos; rama `trabajo/sesion-02`, 12 commits, informes SESION-02-TUBERIA, SESION-02-VIDEO y SESION-02-VIDEO-V8). La tuberia de transcripcion con cuarentena mecanica (scripts/transcribir_sesion.py); v7 (3-11 ago) y v8 (12-19 ago, rescatada, audio solo hasta 0:40:00) en el corpus con sus manifiestos; 43 operaciones leidas en pantalla y comparadas con ADR-0043 (10 parejas); las decisiones del consultor sobre las dudosas, el rebobinado y las ventas sin pareja (riesgo de fidelidad del libro); tres items de evidencia de pantalla (entrada.tipo_orden) y A-47 abierta, BLOQUEANTE de RN-011, en la hoja detras de A-38. Agosto es desarrollo; las exposiciones estan declaradas. El cuestionario de la hoja se repite entero en la proxima sesion: el punto 22 sigue pendiente.
- 2026-09-26 (40) · EL CABLEADO DEL SIMULADOR, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 5a417b9, tag stable/F24-cableado-simulador; rama `trabajo/cableado-simulador`, informe docs/validation/CABLEADO-SIMULADOR.md, ADR-0053 ACEPTADO). Una sesion autonoma con un commit sellado por pieza: el ADR PROPUESTO; el bucle y el cableado (engine/cableado.py, engine/primitivas_broker.py, cuenta.CuentaViva, Broker.mover_stop) sin tocar la spec, ambiguedades.yaml, el interprete ni el motor; `motor arnes --simular` y `motor visor --simular`; los tests sobre un dia sintetico de 2030 con la spec real y una estrategia sintetica que vive en el test (punta a punta con llenado por ticks y cierre por stop, gate de la firma que prohibe con la cuenta cruzada en el cierre de M1 siguiente y nunca antes, reloj unico, sin mirar al futuro, determinismo, ticks obligatorios, cuenta persistente con estrategia de cero, negativas de la CLI); y la linea base con el informe. MEDIDO Y CORREGIDO SOBRE EL ADR: RN-016 si se evalua mientras no hay cierres y RN-030 no cambia de estado, contra lo que el ADR anunciaba al proponerse. INCIDENCIA: la primera linea base listaba todos los dias de calendario que la cuenta corta entre abril y agosto, con el saldo intacto, y la guarda del brief no admite fechas de meses reservados en ningun fichero; corregido en codigo, exigido por test, y el commit rehecho antes de salir de la maquina. En el cierre, el ultimo commit de la rama: ADR-0053 ACEPTADO con todas las decisiones PROVISIONALES y 2.1 y 5.1 para revisar; el hallazgo escrito en el ADR -RN-020 seguira prohibiendo abrir aunque la geometria quede resuelta mientras perdida_dia y perdida_semana no tengan magnitud ni corte-; nace A-44, BLOQUEANTE de RN-020, en la hoja de la sesion 02 justo despues de A-43.
- 2026-09-26 (39) · TICKS, MODELO DE LLENADO Y BROKER SIMULADO, VALIDADA y cerrada en main por orden de cierre explicita de Aleks tras la revision del consultor (merge 8c9beea, tag stable/F24-ticks-llenado; rama `trabajo/ticks-llenado`, informe docs/validation/TICKS-LLENADO.md, registro de la noche en NOCHE-TICKS-BROKER.md, ADR-0051 y ADR-0052 ACEPTADOS). Una sesion nocturna autonoma cortada por el limite de uso y retomada por la manana; once commits sellados, uno por pieza. Fase 0: firma_comision_por_lado conservador por lado. Fase 1: ADR-0051. Fase 2: ticks de Dukascopy de los dias dev de abril y agosto, horas 05-13 UTC (DN-5), en streaming, con manifiesto inmutable, hashes, horas perdidas listadas y una CLI que se niega fuera de construccion; el servidor devolvia 503 y resets a rafagas, asi que se baja con pausa y una segunda pasada sobre la cache; integridad con tolerancia fijada antes: todas las M1 con ticks cuadran; spread p90 de 4 a 5 puntos por hora en knowledge/simulador/llenado.yaml; kit y fidelidad check identicos byte a byte. Fase 3: engine/llenado.py. Fase 4: ADR-0052 y engine/broker.py. Fase 5: engine/simulacion.py con estrategia sintetica fuera de src. Fase 6: repeticion descriptiva de las operaciones del trader por el broker y la cuenta FTMO con una rejilla hipotetica de riesgo (la salida se reconstruye por la regla de la spec, DN-8): EL HALLAZGO es que el desenlace difiere entre ticks y respaldo M1 en una fraccion grande de las operaciones, y el consultor decidio que los TICKS SON OBLIGATORIOS para toda simulacion que cuente (ADR-0051 §8). Fase 7: la entrada se toca dentro del minuto del xlsx en todas las operaciones con ticks, el control a mas menos treinta minutos cae, y los ticks dicen el orden de los toques donde la M1 no puede. Decisiones nocturnas DN-0 a DN-8 resueltas por el consultor en ADR-0051 §7 (DN-3 y DN-6 provisionales; DN-5 aceptada para verano con la ventana de invierno ligada a A-42). Desde esta rama el ritual de cierre lo ejecuta Claude Code solo ante una orden explicita (CLAUDE.md, RITUAL.md).
- 2026-09-25 (38) · EL VISOR DE DIAS DE CONSTRUCCION, VALIDADO y cerrado en main (merge 8d8a42c, tag stable/F25-visor-dias; rama `trabajo/visor-dias`, runbook docs/runbooks/VISOR-DIAS.md; sin ADR ni informe por decision del brief). Cuatro commits, uno por pieza y con su sello: CLI de un dia y render (8643b10), modo lote e indice (1b8ad1f), tests (50045c8), runbook (41ee608). Para un dia dev de construccion, `botsito motor visor --caso <id>` genera un HTML autocontenido (SVG por codigo, sin JavaScript, M1/M15 por CSS) con lo que hizo el trader, lo que hizo el bot y por que: velas, H4 de contexto con la que rompio el sesgo, operaciones con entrada y stop en su llenado, hechos fijados en su instante, embudo y donde se para, avisos H3 y parejas del criterio; `--todos` con indice, `--hasta HH:MM` sin mirar al futuro. Misma compuerta y mensajes que el arnes; salida en data/visor/, ignorada. Medido: un dia en un segundo, los 42 de construccion en menos de diez. La pagina se miro en el navegador, no solo por texto. Sin tocar la spec, ambiguedades.yaml ni el motor.
- 2026-09-25 (37) · LA CAPA DE CUENTA DEL SIMULADOR, VALIDADA y cerrada en main (merge 11132d6, tag stable/F24-simulador-cuenta; rama `trabajo/simulador-cuenta`, informe docs/validation/SIMULADOR-CUENTA.md, ADR-0050). Cinco commits, uno por pieza y cada uno con su sello: los hooks exportan PYTHONUTF8=1 (0d85ca8; medido antes: con PYTHONUTF8=0 el emoji de lint-imports revienta por tuberia en esta maquina, con 1 pasa; test con consola cp1252 simulada, `uv` falso, control y mutante; RITUAL.md correccion 9; el propio commit entro sin anteponer nada), ADR-0050 (704278b), el perfil FTMO 2-Step Swing 100k con el formato del registro y su cargador (3370e48), la capa de cuenta y sus tests (617acd7) y el informe (481343a). El perfil: UN fichero en knowledge/cuentas/ leido por cargar_registro, cada cifra con su regla R1..R20 de FTMO-REGLAS, cuatro UNKNOWN por NO ENCONTRADA o por no existir (fondeada), cruce por test con parametros.yaml y con huso_operativa; un perfil INVENTADO en tests/fixtures demuestra que cambiar de firma es cambiar de fichero. La capa de cuenta: funciones puras sobre una linea de tiempo de aperturas, marcas, cargos y cierres; los nueve tests del brief (suspension en el instante exacto y no antes; los dos cambios de hora de 2030 con las medianoches afirmadas en UTC; equity flotante; objetivo sin dias minimos; comision y swaps; persistencia entre dias; negativa sin valor; perfil sintetico; determinismo). Convenios declarados en el ADR: por debajo estricto para la firma, al llegar para el objetivo, cierre antes que apertura a igual instante, primera suspension o superacion terminal. AL VALIDAR, el consultor decidio las tres cosas del informe §5: `firma_huso_corte` se queda en el perfil vigilado por el test de medianoches, la guardia de tamano sin cifra no impide correr porque es solo aviso, y la duplicacion con parametros.yaml se acepta mientras el test la vigile; y una decision nueva pendiente de implementar: `firma_comision_por_lado` toma el supuesto conservador de cobrarse en cada lado, con fuente decision, hasta que FTMO lo confirme. Sin tocar knowledge/spec ni ambiguedades.yaml; sin cablear al motor. Lo siguiente: la sesion 02 (punto 22), los ticks y el modelo de llenado como siguiente rama (punto 32), y despues el broker simulado y el cableado (punto 33).
- 2026-09-25 (36) · LOS HUECOS DEL ARNES, VALIDADA y cerrada en main (merge a65dba5, tag stable/F18-huecos-motor; rama `trabajo/huecos-motor`, informe docs/validation/HUECOS-MOTOR.md, ADR-0049; spec 12.2.2 -> 13.0.0). Sobre el informe de solo lectura del mismo dia, el consultor decidio los seis huecos de ADR-0048 y la rama los cerro en cuatro commits: ADR-0049 (`4404143`); la spec y el motor de H1 con sus tests (`edb34fb`); H2 y H3 con A-43 y la hoja de la sesion 02 (`c05faa6`); la linea base y el informe (`7c7fcd3`). H1: `ambiguo` e `insuficiente` valores del hecho `sesgo`, RN-003 con `sesgo_h4_al_abrir` (nombra el tope, ADR-0019 §1), RN-033 prohibe con `vale`, y el hecho caduca al abrir; MEDIDO ANTES DE CERRAR, contra la primera redaccion del ADR: sin la caducidad los gates leian en la primera pasada de la apertura el sesgo de la sesion anterior y RN-033 disparaba tambien en la sesion siguiente a una ambigua; el consultor eligio la caducidad entre tres opciones. Dos desviaciones del brief aceptadas por el consultor: `sesgo_h4_tope_velas` se queda CONFIRMED con fuente ADR-0044 y la palabra provisional en su descripcion, porque el registro no tiene estado PROVISIONAL (crearlo es cambio de ADR-0002/ADR-0012); y los seis avisos de H3 de la linea base -RN-001 y RN-033 prohiben lo mismo a las 15:00 de una segunda sesion ambigua- son inofensivos y quedan como pendiente menor, a revisar cuando la spec se toque por otro motivo. `lado_de_ruido` con ambiguo no se define: RN-033 ya prohibe, `sentido` tiene que ser ligadura y una primitiva futura ha de fallar, no valer. Guardias nuevas en `spec/modelo.py` (`vale`, `caduca`, valores de hecho como tokens, consumo por conjunto). La linea base nueva vive al lado de la anterior sin tocarla.
- 2026-09-25 (35) · EL ARNES DEL MOTOR, VALIDADA y cerrada en main (merge 8a5806e, tag stable/F18-arnes-motor; rama `trabajo/arnes-motor`, informe docs/validation/ARNES-MOTOR.md, ADR-0048). El brief pedia una cadena lineal de reglas y la sesion paro en la lectura previa: contradecia ADR-0030 §1-2, ADR-0018 §2 y ADR-0028 §4, y las sesiones independientes contradecian los hechos que la spec hace cruzar; el consultor eligio mantener esa arquitectura (opcion (a)). ADR-0048 (`fd7aeb2`); el interprete, las primitivas, el motor del dia y el arnes, con sus tests sobre datos sinteticos (`98fd8ef`); la CLI y el runbook (`e8ce5c8`); la linea base y el informe (`82f3ae2`). La linea base reproduce por operacion el diagnostico de RN-003 exactamente, y por sesion distingue las sesiones con varias operaciones; dos ejecuciones identicas byte a byte. Error medido y corregido en la rama: la traza solo registraba un hecho si cambiaba de valor, y una segunda sesion que volvia a fijar el mismo sesgo no lo contaba.
- 2026-09-25 (34) · REGLAS DE FTMO CON FUENTE OFICIAL, VALIDADA y cerrada en main (merge 82fab11, tag stable/F14-ftmo-reglas; rama `trabajo/ftmo-reglas`, informe docs/validation/FTMO-REGLAS.md, sin ADR). Solo investigacion y documentacion (`1df9af3`). Fuentes: ftmo.com, sus FAQ y la API `ftmo.com/wp-json/ftmo/symbols`, leidas por HTML crudo el 2026-09-25 entre las 19:32 y las 19:36 UTC; ningun foro ni blog; cada cita comprobada por script contra el texto descargado, y NO ENCONTRADA donde la fuente oficial calla (calendario del +DST del servidor, lote minimo, paso, stops level, si la comision es por lado, la `maximum capital allocation rule`). A-27 y A-28 resultan ser MEDICIONES y la web solo las contesta en parte; la pagina oficial SI confirma por escrito el recalculo del limite diario a las 00:00 CE(S)T. Lo que el repositorio no sabia: el GAP TRADING prohibido tambien en Swing, la coherencia del tamano de posicion frente a un lote variable, los limites de 200 ordenes y 2000 posiciones al dia, la comision de EURUSD y el volumen maximo. Decisiones del consultor para el ADR del simulador y preguntas de Aleks a FTMO en Next Action 26 y 27; lo siguiente, el arnes del motor (Next Action 28).
- 2026-09-25 (33) · ARREGLO DE LA CI, VALIDADA y cerrada en main (merge eb45c94, tag stable/F14-arreglo-ci; rama `trabajo/arreglo-ci`, informe docs/validation/ARREGLO-CI.md, sin ADR). El run 36174003223 sobre `ac4e3a0` salio rojo y verde al relanzarlo sin tocar el arbol: CARRERA entre los dos pushes, que `trabajo/blindaje` habia separado en dos lineas -el push de `main` creo el run a las 18:31:45 y la CI hizo `git fetch --tags` a las 18:31:50, antes de que llegara el tag-, reproducida en un clon sin el tag; descartadas midiendo las hipotesis del bit de ejecucion y de la identidad de git. El log literal no se leyo: pide autenticacion y la extension de Chrome no estaba conectada. El ritual empuja con un solo `git push --atomic origin main stable/<tag>` (`d8d0a89`, con el test que reproduce la carrera y el que prohibe pushes sueltos) y el informe (`75305dd`). Primer cierre cuyos commits y cuyo merge pasaron por la puerta del sello instalada.
- 2026-09-25 (32) · BLINDAJE, VALIDADA y cerrada en main (merge 8c6354e, tag stable/F14-blindaje; rama `trabajo/blindaje`, informe docs/validation/BLINDAJE.md, sin ADR). La puerta automatica del commit (`ac86865`): `make check` borra el sello al empezar y, solo en verde y sin cambios sin estadiar ni ficheros sin seguir, escribe el hash de `git write-tree`; `pre-commit` y el nuevo `pre-merge-commit` -que el README de los hooks daba por inexistente y existe desde git 2.24- lo exigen. El test del indice de ADR en PROJECT_STATE (`2067dfd`). El ritual con el orden nuevo y la salida de un merge rechazado -abortar, sellar en la rama y repetir, porque en `main` a mitad de merge `state check` falla por diseno- (`252224c`); el informe (`10dddec`). El primer `make check` salio en rojo (`make-check.log` fuera de la lista de ignorados) y la puerta no sello; uno lo corto el sistema por memoria y se paro sin reintentar. Los hooks nuevos se instalaron con `make hooks` en `main` justo despues del merge (reflog: no hubo checkout de vuelta a la rama), asi que el merge paso aun por el hook viejo; su arbol, `287a681`, era el del sello. LA DEUDA DEL COMMIT SIN PUERTA QUEDA CERRADA -`40759cb` el 2026-09-23 y `2753ac1` esta semana-; en Technical Debt queda solo lo que la puerta no cubre, `cherry-pick` y `rebase`. LA CI DEL `docs(state)` (`ac4e3a0`, run 36174003223) SALIO ROJA en el primer intento por la carrera entre el push de `main` y el del tag, que se empujaron en dos lineas, y VERDE en el segundo intento sin cambiar el arbol; la rama se borro con la CI en verde. El arreglo es la entrada (33).
- 2026-09-25 (31) · LA SESION 02, PREPARADA, VALIDADA y cerrada en main (merge bd56fb4, tag stable/F19-sesion-02-preparada; rama `trabajo/sesion-02`, 13 commits, informes docs/validation/SESION-02-INVENTARIO.md, SESION-02-BUSQUEDA-CRITERIO.md, SESION-02-BUSQUEDA-SALIDA.txt, SESION-02-BUSQUEDA-CLASIFICACION.md y SESION-02-DECISIONES.md, ADR-0047). Inventario y auditoria (`45bb3a9`): la sesion 01, 21 ambiguedades no RESUELTAS, siete contradicciones K-01..K-07 y ocho candidatos C-01..C-08. Busqueda de seis candidatos con criterio congelado (`4dc3dd5`, `8458284`, `52f5094`): 47 pasajes, 4 RESPONDE, todos ya items de evidencia. Decisiones del consultor: K-04 (`e59117b`), A-21 toca RN-008 y no RN-004, la frase contraria entro sin fuente en 0901d2c; K-07 (`d76f8c9`), `huso_grafico` a Etc/GMT-2 por la medida de enero, `huso_operativa` sin tocar; K-02, K-05 y K-06 (`fc1df40`); A-36..A-41 y preguntas en forma abierta (`76fd797`); runbook de sesion (`3a65c0e`); hoja (`b688b88`); A-42 bloqueante y preguntas revisadas (`4be7ed2`); ADR-0047 (`e75cd0c`); la parada de marzo antes del sorteo (`d470c9c`). K-01 y K-03, aplicadas en este docs(state). Error medido y corregido en la rama: un commit con 1 test en rojo por leer el aviso de la tarea y no el log; se rehizo con --amend antes de seguir.
- 2026-09-24 (30) · LA ENTRADA DE MARZO, VALIDADA y cerrada en main (merge e2931d9, tag stable/F14-entrada-marzo; rama `trabajo/entrada-marzo`, informe docs/validation/ENTRADA-MARZO.md, ADR-0046). Paso 0: tres documentos decian tres cosas sobre marzo; decide el consultor (`e9ef8b0`, ADR-0046): camino de fidelidad con sorteo y puerta, `fidelidad-dev` como medicion junto con mayo, cupos por REGLA desde N fijada antes de ver el mes (N = 18: 6/6/6/0; 20: 6/7/7/0; 22: 7/7/8/0), artefacto limitado al mes de su id, sorteo irrepetible y orden a-e con la excepcion acotada a ADR-0039 §1. Velas M1 de marzo (`04f1ed9`), con `kit check`, `fidelidad check` y `knowledge validate` identicos antes y despues. `c9b6a55` el mes del id, la regla y la negativa a repetir el sorteo; `425b3be` `casos ingerir --artefacto`, con CENTINELA en las filas reservadas -aprobada por el consultor-; `b4139ae` la medida del huso por velas hecha herramienta, cifras en `criterio_huso.yaml`, tests sinteticos en verde ANTES del control y control sobre ABRIL -no mayo-: UTC 36/38 frente a Madrid 4/38, coincide, con los blobs de la herramienta sin tocar; `2054b58` el ensayo de punta a punta sobre repo sintetico con la CLI real; `ae90410` el runbook; `aece668` el informe y, por decision del consultor, las PARADAS por fechas con otro formato: paran la medida entera, no se toca el lector sobre la marcha y la sesion describe el caso sin mostrar fechas. Un `make check` se corto por falta de memoria del sistema; relanzado solo y en primer plano, paso las seis veces siguientes.
- 2026-09-24 (29) · A-35 EN TRANSCRIPCIONES Y FOTOGRAMAS, VALIDADA y cerrada en main (merge 75f60d9, tag stable/F19-a35-al-trader; rama `trabajo/a35-pivote-formado`, informes docs/validation/A35-PIVOTE-FORMADO-CLASIFICACION.md y docs/validation/A35-FOTOGRAMAS-RESULTADO.md, sin ADR). Busqueda con el metodo congelado de A-24 (`a8a8e88` criterio con lista propia `--conjunto a35`, salida de A-24 y A-18 reproducida byte a byte; `3ad40da` salida, 10 pasajes con el control positivo entero; `ddf6eea` clasificacion: 1 RESPONDE -v4 #942-, 5 DUDA, 4 NO RESPONDE). Regla global del consultor: no se decide, se miden los fotogramas. Criterio congelado antes de abrir (`14ed54e`: lista cerrada por ventana de segmento, P4 y P5 localizados por ADR-0038 §1, verificacion contra F05, campos (a)-(f) y dos anadidos antes de abrir, (g) grafico parado y (h) marca ya presente); medicion de los 89 (`6702a82`); resultado (`838bed0`): tercera rama, A-35 no responde, al trader y bloqueante; y la pregunta del campo cambia a la abierta del informe (`126b446`). MEDIDO CONTRA EL BRIEF: ADR-0038 no define un «registro de extracciones»; se uso la cadena de F05, como en V5-INSTANTES. Un `make check` se corto por falta de memoria del sistema y se relanzo en primer plano por indicacion del consultor.
- 2026-09-24 (28) · A-24, A-21, A-26 Y A-34 EN LAS TRANSCRIPCIONES, VALIDADA y cerrada en main (merge 8451cff, tag stable/F19-a24-decidida; rama `trabajo/a24-a21-a26-a34`, informe docs/validation/A24-A21-A26-A34-CRITERIO.md, ADR-0045). Criterio congelado antes de buscar (`a821411`: hipotesis por ambiguedad, regla comun, lista cerrada de frases sin palabras sueltas de uso constante, ventana de +-45 s con corte a 180 s; `scripts/a18_buscar.py` generalizado sin cambiar A-18), una sola ejecucion con los cuatro controles positivos (`3698152`) y clasificacion con la frase literal comprobada contra su pasaje (`b435f3b`). Regla global aplicada por el consultor (`87ce977`, `8da90d6`): A-24 DECIDIDA -no RESUELTA: no hay registro del trader- por ADR-0045, el pivote mas reciente ya formado: responde v1 #180, refuerza v4 #1174-#1182 y acota v4 #846; P5 no responde en contra porque en ese croquis (a) y (b) coinciden, y el item que sostenia la hipotesis discrecional es del TP. A-21, A-26 y A-34: ningun pasaje responde, se preguntan al trader. Nace A-35, cuando esta formado un pivote, bloqueante: la spec no lo define y no se inventa. Spec 12.2.1. MEDIDO CONTRA EL BRIEF, DOS VECES: la tabla Known Ambiguities se toco en la rama porque `test_project_state_refleja_las_ambiguedades` lo exige al abrir A-35; y la regla del `<SHA>` NO se reescribio en el ritual porque ya estaba en `docs/runbooks/RITUAL.md` desde `dd150be`, con su recuento propio (cuatro veces, dos antes del merge).
- 2026-09-24 (27) · EL MOTOR, PRIMERA REGLA: EL SESGO H4, VALIDADA y cerrada en main (merge 28ecd0c, tag stable/F18-sesgo-h4; rama `trabajo/motor-sesgo-h4`, informe docs/validation/MOTOR-SESGO-H4.md, ADR-0044). EL PASO 0 SE PARO: RN-003 no definia que pasa si la vela rompe los dos extremos, ni el estado inicial, y fijaba el sesgo al abrir la sesion y no en cualquier instante. Decidido por el consultor (ADR-0044): rompe ambos -> AMBIGUO (A-34 abierta, pregunta al trader); sin ruptura en `sesgo_h4_tope_velas` (60, provisional, categoria `ejecucion` porque un valor de `estrategia` solo lo dice el trader) -> INSUFICIENTE; con los dos no se opera; se fija al abrir la sesion con las H4 cerradas por su hora de fin y no por la marca `completa`; romper es superar por al menos un punto. RN-003 declara `decision: ADR-0044`; spec 12.1.1 -> 12.2.0. El sesgo vive en el dominio, puro, con tests sinteticos de cada rama, sin mirar el futuro y con los cambios de hora de EE. UU. DIAGNOSTICO sobre construccion (abril y agosto; mayo no se lee), sin umbral y sin tocar la regla: de 77 operaciones del trader, 58 a favor del sesgo del bot al abrir su sesion, 12 en contra -anotadas en A-26- y 7 con sesgo ambiguo; ninguna ruptura en la zona de 1-2 puntos de A-16. La siguiente regla en orden causal, RN-004, queda BLOQUEADA: lee `liquidez_m15`, que nada produce, y la regla que marcaria el nivel es A-24, bloqueante.
- 2026-09-24 (26) · EL CRITERIO DE FIDELIDAD EN DESARROLLO, VALIDADA y cerrada en main (merge a7bf86b, tag stable/F14-criterio-fidelidad; rama `trabajo/criterio-fidelidad`, informe docs/validation/CRITERIO-FIDELIDAD.md, ADR-0043). FIJADO ANTES DEL MOTOR, sin una linea de el. Primero la medida del instante, con la regla fijada antes por el consultor y un control nuevo: la entrada dentro de [minima - 2, maxima + 2] puntos de la M1 de su instante en 93 de 94 operaciones `dev` (98,9 %), y en el 5,3 % y el 12,8 % a -30 y +30 min: el instante del xlsx es el LLENADO. No es del todo independiente -el mismo test fijo el huso (ADR-0039)-; lo nuevo es el control. Despues, el criterio literal del consultor: la operacion como unidad; empareja dia, sesion y direccion con |Δentrada| <= 3 puntos -un punto es 0,00001- y |Δinstante de llenado| <= 15 min, uno a uno y determinista; cobertura y precision, con lo del bot en dias sin trader aparte (ADR-0016); stop, TP, resultado y gestion fuera; construccion abril y agosto, medida mayo; umbral de desarrollo 70 % y 60 %, que no es el PREREGISTRO. Las cifras en un YAML (ADR-0002) y una funcion pura de emparejamiento y metricas probada solo con operaciones sinteticas.
- 2026-09-23 (25) · ABRIL Y AGOSTO, CASOS `dev` POR EL REPARTO DEV-VISTO, VALIDADA y cerrada en main (merge 4463019, tag stable/F14-casos-agosto-abril; rama `trabajo/casos-agosto-abril`, informe docs/validation/CASOS-AGOSTO-ABRIL.md, ADR-0042). EL PASO 0 MIDIO CERO: por el camino de mayo, abril y agosto pedian 0 dias, porque la ingesta solo toma dias de un reparto del kit y ninguno de los dos meses tenia un dia en ningun reparto ni tramo en `cobertura_material`; los 4 `fidelidad-dev` quedan fuera, porque solo los cubre el libro de septiembre, sin sha. Decidido por el consultor: ADR-0042, un reparto dev-visto -todo `dev`, sin sorteo ni holdout, recompuesto desde la cobertura y anclado- solo para meses vistos cuya lectura completa ya este declarada, con la puerta aplicando «ocultos»; y los tramos, fecha minima y maxima de la columna de fechas, leidas por orden suya como limite inferior de la cobertura. Resultado: abril 16 casos (35 operaciones), agosto 19 (42); la biblioteca `dev` pasa a 41 casos. Las ausencias -5 y 2 dias del tramo sin operacion, 9 y 12 sesiones- se quedan como RECUENTOS: si cuentan se decide en el criterio de fidelidad, antes de ver resultados del bot. Un test que congelaba que solo mayo llevaba sha en la cobertura pasa a abril, mayo y agosto; y `b471e78` se probo con ficheros de otro commit en la copia de trabajo, anotado en Technical Debt.
- 2026-09-23 (24) · INVENTARIO PARA LA FIDELIDAD, VALIDADA y cerrada en main (merge a8a9682, tag stable/F14-inventario-fidelidad; rama `trabajo/inventario-fidelidad`, informes docs/validation/INVENTARIO-FIDELIDAD.md y docs/validation/INVENTARIO-FIDELIDAD-DECISIONES.md, sin ADR y sin codigo). EL BOT NO EXISTE COMO ALGO EJECUTABLE: medido leyendo codigo, spec y tests, sin ejecutar nada contra ningun caso ni libro. F18 a F24 y F26 estan sin empezar; las reglas vigentes tienen forma validada estaticamente y ninguna implementada, con tres parciales por la agregacion de F15; solo hay 6 casos `dev`, todos de mayo. Lo minimo para una primera medida, ordenado, con A-24 y A-21 bloqueantes por delante, y los riesgos de look-ahead, huso y series. Decidido por el consultor: D1 -la verdad es el xlsx, «no opero» solo donde el libro cubre-, el instante que registra el xlsx, ampliar los casos `dev` como siguiente rama, y su correccion: la estimacion de calendario suponia un motor que no existe. La rama salio del `main` anterior y se reaplico con rebase sobre el cierre de v6, resolviendo PROJECT_STATE.
- 2026-09-23 (23) · EL DIA RESERVADO DE v6 FUERA DEL HOLDOUT, VALIDADA y cerrada en main (merge 286c113, tag stable/F14-v6-fuera-del-holdout; rama `trabajo/v6-fuera-del-holdout`, informe docs/validation/V6-FUERA-DEL-HOLDOUT.md, ADR-0041). La rama se paro primero en el paso 0 con cuatro preguntas, porque escribir la retirada en el `particiones.yaml` de fidelidad rompia su reproduccion byte a byte y su ancla (ADR-0036), y porque `casos_reservados` era a la vez lo que se MIDE y lo que se OCULTA: sacar el dia de el lo habria pasado a desarrollo. Decidido por el consultor: un fichero aparte, `knowledge/cases/retirados.yaml`, solo anadir y por la huella (sha256) del id, con su motivo, su exposicion y su ADR; dos conjuntos derivados, `casos_medidos` (33) y `casos_ocultos`; la puerta rechaza un retirado siempre; `fidelidad-1` declara 10 y se mide sobre 9, sin sustituto. Seis tests, incluido que ninguna salida de los comandos que recorren casos imprime el id. Y una medida que el brief no preveia: el reparto de septiembre ya nombra el dia en claro desde su sorteo, asi que la huella evita escribirlo en un sitio mas pero no que se deduzca. Las exposiciones de ese dia, resueltas por retirada en HOLDOUT-EXPOSICIONES.
- 2026-09-23 (22) · A-18 EN LAS TRANSCRIPCIONES, VALIDADA y cerrada en main (merge 6dbce8b, tag stable/F14-a18-transcripciones; rama `trabajo/a18-transcripciones`, informe docs/validation/A18-TRANSCRIPCIONES.md, sin ADR). NINGUN PASAJE RESPONDE: criterio congelado antes de buscar (`cdcf58e`: la regla literal del punto 14, 36 terminos en lista cerrada, ventana de +-45 s, solo la cruda verificada contra su manifiesto), una sola ejecucion (`019ed47`, 42 pasajes de v1-v5), control positivo con las frases conocidas de v5 y clasificacion (`468ec59`): 0 responden, 11 con duda anotada -cinco apuntarian a caja_completa si se resolviera, y son inferencias, no frases del trader-. Aplicada la regla por el consultor: se pregunta al trader con la pregunta de reserva de V5-INSTANTES y la busqueda queda cerrada. OBSERVACION, sin decidir: en v1-v4 el stop se describe en DOS tiempos (lote sobre la caja entera, protegido a 0,75 tras la entrada), anterior al lineamiento del 9 de septiembre, y las dos hipotesis de A-18 suponen un solo stop. Alcance: v6 fuera por grabarse en un dia reservado; su lectura previa y el desliz de `cdcf58e`, que dejo la identidad de ese dia en el historial, declarados en HOLDOUT-EXPOSICIONES. El brief del paso 0 uso «material de septiembre» como fecha de grabacion: error del consultor, dicho en el informe.
- 2026-09-23 (21) · V5, LOS SEIS INSTANTES, VALIDADA y cerrada en main (merge 7689ae8, tag stable/F14-v5-instantes; rama `trabajo/v5-instantes`, informe docs/validation/V5-INSTANTES.md, sin ADR). LA MEDIDA NO ESTA EN V5: 0 de 36 fotogramas -ventana fija de seis por instante- cumplen la condicion congelada ANTES de mirar (niveles 0 y 1 con linea propia, herramienta valida y ancla comun), asi que la via se cierra y A-18 sigue con (riesgo_real, 0,8) y (caja_completa, 1,0) sin separar, no bloqueante. Los pendientes eran SEIS, no cinco. El decodificador de PNG entra a `scripts/` con su test; el criterio verifica cada fotograma contra la extraccion de F05 antes de decodificarlo, y su salida quedo congelada en un commit propio. Dos defectos anotados en Technical Debt: un commit de la rama entro con `make check` en rojo, y el criterio solo reconoce cajas de venta. Lo siguiente, buscar A-18 en todas las transcripciones; la pregunta al trader queda de reserva.
- 2026-09-23 (20) · LA REGLA DEL MES SIN FILAS, VALIDADA y cerrada en main (merge f30128f, tag stable/F14-regla-mes; rama `trabajo/regla-mes-sin-filas`, informe docs/validation/REGLA-MES-SIN-FILAS.md, sin ADR). SE MANTIENE, aplicando el criterio fijado ANTES de medir: medido leyendo el codigo, cuenta SOLO sobre los dias pedidos -no sobre el mes completo- y es lo unico que detecta un libro cuyo sha esta atado en `cobertura_material` al tramo de otro mes; su coste, no distinguir eso de unos dias pedidos sin filas, queda aceptado y testeado. EL MENSAJE AFIRMABA MAS DE LO QUE LA REGLA COMPRUEBA -«el material no tiene ni una fila de <mes>»- (patron 5): ahora dice solo lo que sabe, SIN sujeto humano como su aviso hermano, desviandose del texto del brief por esa regla ya escrita. Cuatro tests por la CLI que faltaban. Y el caso normal de un huso mal declarado -filas que se van a un dia no pedido- queda en Technical Debt: sin detector y, decidido, sin rama, porque detectarlo exigiria mirar dias no pedidos, reservados incluidos.
- 2026-09-23 (19) · LA GUARDIA DE IDS CITADOS EN LOS DOCUMENTOS, VALIDADA y cerrada en main (merge cb6b33e, tag stable/F14-guardia-ids; rama `trabajo/guardia-ids-docs`, informe docs/validation/GUARDIA-IDS-DOCS.md, sin ADR). TODO ID CITADO EN `docs/**`, `CLAUDE.md` Y `PROJECT_STATE.md` EXISTE O ESTA DECLARADO EN SU DOCUMENTO CON MOTIVO. Una sola gramatica -`comun.ids.FUENTE`- y un solo conjunto de existencia -`ids_de_fuente`, el de los trailers-. Medido antes de escribir: 13 citas de 4 ids que no existen, ninguna una fabricacion, y la guardia salio en ROJO con exactamente esas antes de declarar nada. LA EXCEPCION NOMBRA LA CONDICION Y VIVE EN EL DOCUMENTO -un bloque `ids-inexistentes` con motivo, patron 3-, y falla si el id declarado existe, si no se cita fuera del bloque o si no tiene motivo. Dos ajustes cazados en la propia rama: la valla sangrada 4 espacios es codigo y no abre bloque, y los cuatro tipos de fallo compartian un prefijo que decia otra cosa (patron 5 en pequeno). La deuda duplicada queda en una entrada resuelta -las dos redacciones contaban mal que ids faltaban-, y `CLAUDE.md` gana el regimen de `docs/validation/`, sin detector.
- 2026-09-22 (18) · EL RITUAL Y SUS VENTANAS, VALIDADA y cerrada en main (merge 24dc81f, tag stable/F14-ritual; rama `trabajo/ritual-ventanas`, informe docs/validation/RITUAL-VENTANAS.md, sin ADR, solo documentacion). `RITUAL.md` DICE LO QUE SE EJECUTA, y `PROJECT_STATE.md` deja de corregirlo: las ventanas A/B/C de `state check`, MEDIDAS en un clon desechable -antes A y B estaban solo deducidas de `cli.py`-, el bloque en el orden del cierre de mayo, la cadena `&&` que de verdad se ejecuto en vez del `if` que se describia, y FUERA LA «PUERTA 2» `tag..HEAD`, que comparaba un commit consigo mismo y salia vacia siempre (correccion 6: ninguna comprobacion que pase siempre). Patron 5, sexta instancia -esa puerta, compartida por consultor y sesion- y septima -comprobaciones corridas antes del `add`, de orden y cazadas por la propia comprobacion-. La regla de los briefs entra en `CLAUDE.md`. ADR-0033 una sola vez en el indice. Y una inconsistencia anotada sin corregirla hacia atras: «Reglas de la casa» cerro sin informe, y `state check` no lo vigila.
- 2026-09-22 (17) · MAYO `dev` INGERIDO, VALIDADA y cerrada en main (merge 48075f6, tag stable/F14-mayo-dev; rama `trabajo/mayo-dev-ingerido`, informe docs/validation/MAYO-DEV.md, ADR-0039 y ADR-0040). LOS PRIMEROS CASOS DEL PROYECTO -6 `caso-*.yaml` de los dias `dev` de mayo- y EL TERCER MES CONTRA A-18: n = 5 ganadoras (2,90 · 3,05 · 3,30 · 3,46 · 3,57), region [3,00 , 3,75) POBLADA 4 de 5 -> (caja_completa, 0,8) refutada por tercer mes (ADR-0040), los dos supervivientes siguen abiertos porque el fichero no trae la caja, A-18 no sube a bloqueante. ANTES DE LEER UNA FILA HUBO QUE ARREGLAR SEIS COSAS DEL MECANISMO, y la revision de diseno refuto el punto de partida: `dias_ingeribles` daba 10 dias y no 6, y el «falla cerrada» no era la puerta sino la regla de cobertura por coincidencia (patron 3 en los tests de F14a). El mes del libro se declara por su sha; solo el camino del kit; ningun mensaje publica la posicion de una fila ni de un XML roto; el caso pierde `objetivo` y su forma es lista cerrada (patron 5, quinta instancia, en documentos ya cerrados); LA FRONTERA DE DIA UTC/MADRID DEL LECTOR -el huso otra vez, tercera vez en dos dias-; y ADR-0039, porque mayo viene ENTERO en AAAA-MM-DD y no en el formato de agosto (la «mezcla de formatos» la dedujo el consultor de booleanos «alguna»). Es LA PRIMERA LECTURA DE FILAS DE UN LIBRO CON DIAS RESERVADOS, declarada el mismo dia en HOLDOUT-EXPOSICIONES.
- 2026-09-22 (16) · LO QUE NO CABIA EN MAIN, VALIDADA y cerrada en main (merge 28e85ce, tag stable/F14-runbook; rama `trabajo/lo-que-no-cabia-en-main`, informe docs/validation/LO-QUE-NO-CABIA-EN-MAIN.md, sin ADR). LA RAMA NO MIDE NADA: CORRIGE EL CIERRE ANTERIOR. Y NACE DE UN FALLO DEL CONSULTOR -un brief que decia que lo que no es `PROJECT_STATE.md` iba igual en el commit de main, lo que contradice MASTER_PLAN §F- QUE LA SESION OBEDECIO SIN CONTRASTARLO CON LO ESCRITO, conociendo la regla. Lo paro `state check`, pero TARDE: el commit ya estaba en origin y la CI en rojo.
  EL HUECO ESTABA EN TRES SITIOS, NO EN UNO. `state check` CORRIA DESPUES DEL COMMIT, dentro de `make check` -medido: el error disparaba sobre el ARBOL DE TRABAJO, con el fichero sin commitear, asi que corriendolo antes el cambio no habria entrado nunca-; `make check` NO CONDICIONABA EL PUSH -imprimia el exit, borraba el log y empujaba igual-; y UNA TERCERA PUERTA QUE YA EXISTIA DESDE EL 2026-09-17 SE SALTO, porque se estadio con `git add -A` en vez de nombrar el fichero. Ahora: se estadia nombrando, `state check` es puerta ANTES del commit, y el push es una rama del `if` con el log quedandose cuando falla.
  Y LOS COMANDOS, COMO SE INVOCAN DE VERDAD, que no es cosmetico: DENTRO DE UN BLOQUE PEGADO UN `command not found` ES INDISTINGUIBLE DE UNA COMPROBACION QUE PASA. Revisado el runbook entero: el `curl` llevaba sin `--ssl-no-revoke` desde que se escribio, y NUNCA SE NOTO PORQUE QUIEN LO EJECUTABA LO ANADIA DE MEMORIA.
  DE AHI SALE EL PATRON 5: **LO ESCRITO Y LO EJECUTADO SE SEPARAN, Y NADA LOS COMPARA**, con sus tres instancias medidas y con la consecuencia que lo hace regla: **EL ARREGLO NUNCA ES OTRA PUERTA**, sino hacer que la forma escrita y la ejecutada sean el MISMO OBJETO. Una puerta mas sobre un paso que se ejecuta de otra forma no ve nada.
  Y EL RITUAL SE ESTRENA SOBRE SI MISMO: el primer cierre que usa el runbook corregido es el que lo fusiona.
- 2026-09-22 (15) · LA CAJA DEL 29 DE ABRIL, VALIDADA y cerrada en main (merge 7bef6ee, tag stable/F14-caja; rama `trabajo/la-caja-del-29-de-abril`, informe docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md, ADR-0038). EL 0,8 SE VE: la plantilla de dibujo del trader lleva los CINCO niveles 1 / 0,8 / 0,5 / 0,25 / 0, con el 0,8 en linea propia y las proporciones cuadrando dentro de un pixel. Hasta ahora ese numero venia solo de lo que el DICE -A-10, resuelta por un registro suyo-. Y la ENTRADA esta en el nivel 0, medido. QUEDA UN CRITERIO REUTILIZABLE: las rayas que dibuja a mano se distinguen de los niveles de la caja POR EL ANCLA EN x -tres rayas azules con el MISMO RGB y rangos de x que no se solapan; solo la de y=98-99 comparte el x=880 de la verde, asi que solo esa es de la caja-.
  LA FRACCION DEL STOP SIGUE NO CONCLUYENTE, Y EL MOTIVO CAMBIO TRES VECES, que es lo que hace la historia util: primero EL EJE DE PRECIOS -no se podia fijar la escala-; luego, con el rodeo del cociente que la cancela, LA LECTURA A OJO -+/-3 px, que no cabe en la tolerancia 0,03-; y al final, con el decodificador a +/-1 px, lo que queda es EL MATERIAL: los niveles 0 y 1 NO tienen linea propia visible y el 0,25 cae bajo la barra de herramientas flotante. Sin los extremos no hay denominador, por mucha precision que haya. Los dos pre-registros fueron ANTES de cada medida y se ve en el orden de los commits. A-18 NO SE MUEVE.
  ADR-0038 NACIO DE UN FALLO DE DENTRO DE LA RAMA: muestreando fotogramas de v4 se abrio sin querer una captura de Analytics de AGOSTO -declarada el mismo dia, con sus cinco cifras listadas, ninguna usada, y agosto sin dias repartidos-. No era un descuido: NO SE PUEDE SABER QUE HAY EN UN PNG ANTES DE ABRIRLO, asi que muestrear a ciegas era incompatible con que una clase entera de imagenes estuviera prohibida. La regla que faltaba era de PROCEDIMIENTO y no de contenido: un fotograma se abre por INSTANTE LOCALIZADO -transcripcion, item de evidencia, marca de tiempo- y nunca por muestreo. Y su decision 3 deja escrito, para que nadie la relaje despues, que UNA REGLA QUE ES GENERAL PORQUE LA COMPROBACION NO LLEGA A TIEMPO NO ES EL PATRON 2.
  A-33 ABIERTA (los parciales): tres ganadoras que CIERRAN por debajo de 3R en dos meses independientes. Y A-16 en n=3.
  UNA CORRECCION DEL CONSULTOR QUE VALE POR SI SOLA: la sesion escribio que "no hay extraccion programatica de pixeles: este repositorio no tiene Pillow, a proposito". Eso MEZCLABA dos cosas distintas -que el repositorio no LLEVA Pillow, que es cierto, y que no se pueden LEER pixeles, que es falso- y convertia una decision de dependencias en una limitacion fisica. Un decodificador PNG de biblioteca estandar -chunks, IDAT mas zlib, y deshacer los cinco filtros- lo refuto en una tarde. La leccion no es sobre PNG: es que una restriccion ELEGIDA se disfraza facilmente de restriccion del mundo, y entonces deja de revisarse.
  Y LO DEL METODO, CON SU MATIZ: las cuatro reglas buenas de la semana -ADR-0038, la del huso, la del «15 de 18» y la condicion de precision- no salieron de "procedimientos que fallaron" sino de FALLOS QUE UNA COMPROBACION SACO A LA LUZ. ES UN SESGO DE SELECCION: los fallos que ninguna comprobacion mira no producen reglas, producen silencio, y por construccion no aparecen en esta lista. LA PREGUNTA QUE ABRE, y no es retorica porque ya tiene ejemplo medido, es QUE ESTA FALLANDO DONDE NO MIRA NINGUNA COMPROBACION: los tres ids `ev-*` inexistentes de `docs/**`, que nadie caza, que no son fabricaciones por SUERTE, y que llevaban nueve dias ahi.
- 2026-09-21 (14) · ABRIL Y LA CAJA, VALIDADA y cerrada en main (merge e7f7638, tag stable/F14-abril; rama `trabajo/abril-y-la-caja`, informe docs/validation/ABRIL-Y-LA-CAJA.md). SIN ADR: no decide nada. EL TITULAR ES EL INSTRUMENTO Y NO EL RESULTADO: el reloj de los graficos de FX Replay es UTC+2 FIJO -medido en el propio grafico de v4 sobre un fotograma de ENERO, asi que no es Europe/Madrid- y con ese desfase las velas de OANDA y las de Dukascopy CASAN A 1 Y 2 PUNTOS. Primera medida de A-16, que queda ABIERTA con n=2, y DESBLOQUEA LA MEDIDA DE LA CAJA: no tenia instrumento no porque nadie lo intentara, sino porque nadie habia comprobado el huso. A-18 SIGUE ABIERTA y ahora se sabe POR QUE: con la definicion de estructura usada -fractal 5, ventana 120- ningun nivel derivado de la operacion cae sobre un fractal por encima del azar, LA ENTRADA INCLUIDA (4 y 3 de 35 frente a senuelos de 4, 4 y 5; el ancla, 7, a +0,47 sd del azar teorico y +1,37 del empirico), asi que NO refuta H(0,8) ni H(1,0): un test sin poder no es evidencia contra nada. La medida 1 REPLICO: abril puebla con 7 de 15 la region que `caja_completa` exige vacia, moda clavada en 3,00, segundo mes independiente.
  LO QUE MAS VALE DE LA NOCHE SON TRES CORRECCIONES QUE SON UNA SOLA FAMILIA: `maxTP` SUPUESTO en F14a -es el PRECIO DE CIERRE, `== avgClosePrice` 17 de 17, no la excursion maxima-; el «ancla no rota» AFIRMADO SIN ARITMETICA; y la guardia de junio MAS ESTRICTA QUE SU ADR con un informe que afirmaba haberlo comprobado. Las tres eran AFIRMACIONES SIN MEDIDA DENTRO DE DOCUMENTOS YA CERRADOS, y cerrarlos es justamente lo que impide que alguien vuelva a leerlos.
  Y SU REVERSO, LA TRAMPA DEL «15 DE 18»: TRES sitios con el mismo texto, dos MAL -ADR-0037 §7 y F14A §4, «se pasan de 3,00», que son 14- y uno BIEN -«15 de 18 dentro de la region», DENTRO de la prediccion congelada, que mide otra cosa-. Un barrido mecanico habria roto el bueno. LA REGLA QUE SALE: una correccion tiene que saber QUE MIDE cada sitio, no QUE DICE; y SI UNO DE LOS SITIOS ES LA PREDICCION CONGELADA, NO SE EDITA -la correccion va en el recuadro de anotacion-.
  Y LO QUE EL PRE-REGISTRO NO PROTEGIO: los criterios estaban congelados y se respetaron, pero el fallo estuvo ANTES, al INSTRUMENTAR -suponer que el eje del grafico era UTC-, y dio una conclusion falsa que estuvo a punto de cerrar la rama. Lo cazo mirar un fotograma de OTRO video por un motivo distinto. De ahi la regla nueva de `CLAUDE.md`: ANTES DE COMPARAR DOS FUENTES SE FIJA EL HUSO DE LAS DOS, MEDIDO Y NO SUPUESTO, igual que las cabeceras se escriben antes de abrir el libro.
- 2026-09-21 (13) · LA COBERTURA DEL MATERIAL EN EL KIT, VALIDADA y cerrada en main (merge 4b63344, tag stable/F14-cobertura; rama `trabajo/cobertura-material-del-kit`, informe docs/validation/COBERTURA-DEL-KIT.md, enmienda ADR-0036). La rama se abrio como "un mes descartado sigue siendo ingerible" y NO VA DE JUNIO: va de que un dia sin filas podia ser DOS cosas incompatibles -«el trader miro y no opero», que es UN DATO SUYO, y «este mes no tiene material», que es AUSENCIA DE CONOCIMIENTO- con EXACTAMENTE EL MISMO SILENCIO. LA REVISION DE DISENO REFUTO EL BRIEF TRES VECES antes de escribir codigo, y dos de esas refutaciones corrigieron una medida de la propia sesion: abril NO entraba en ningun universo -esta en `vistos.yaml` desde el 2026-09-12- y el campo en el config no habria hecho nada, porque la llamada del kit ni lo pasaba. ERAN TRES AGUJEROS Y NO UNO: junio ingerible HOY (`dias_ingeribles` no leia el config), junio entrando en el universo de un `kit build` NUEVO, y el cero significando dos cosas -mas `--material` pudiendo ser el libro equivocado sin que nada lo dijera-. LAS DOS PREGUNTAS SON ORTOGONALES Y HACEN FALTA LAS DOS: `vistos.yaml` responde ¿es ciego? -abril NO, junio SI- y `cobertura_material` responde ¿hay material? -abril SI, junio NO-; junio es el unico mes con dataset que es ciego y esta vacio. EL ENTREGABLE SON LAS FRASES, no el codigo, y van literales: (a) «dias ingeribles sin ninguna operacion en el material: lo cubre y no hay ninguna fila. NO producen caso. Leer esa ausencia como `no_trade` seria una inferencia NUESTRA sobre lo que hizo el trader, y ADR-0016 exige que una decision asi declare el ADR que la toma; hoy no hay ninguno» -SIN SUJETO HUMANO, reescrita antes del merge porque decia "el trader no opero" y eso atribuye una decision a una persona a partir de una ausencia-; (b) «N dias de 2026-06 NO son ingeribles: declarado con CERO tramos: no hay material del trader. No se han leido ni escrito, y no se nombran uno a uno: un dia laborable que no aparece es su etiqueta»; (c) «el material que se ha pasado no tiene ni una fila de 2026-09: o es el libro de otro mes, o falta. No se escribe nada, porque un cero de aqui no se puede distinguir de un dia sin operaciones». Y LA PRUEBA DE QUE NO SE CERRO DE MAS es el tercer caso del agujero 2: con tramos de verdad el universo sigue en 9 casos y son LOS MISMOS DIAS -acotar a todo el mes no quita ninguno-. SE RESISTIO `solo_con_cobertura=True`, que habria cerrado el agujero al precio de que todo mes no declarado dejara de aportar casos: eso es ENUMERAR, y CERO TRAMOS NOMBRA LA CONDICION, que es el tercer patron de la lista y la cuarta vez que aparece esta semana. `dias_ingeribles`: 20 dias -6 mayo + 10 JUNIO + 4 septiembre- pasan a 10. LA LIMITACION QUE LA RAMA CREA, dicha y no escondida: la regla por mes usa los DIAS PEDIDOS, asi que un mes en el que el trader no hubiera operado NINGUN dia ingerible daria un falso error sobre el libro correcto; se queda porque FALLA HACIA EL LADO SEGURO -un falso error PARA el comando, no fabrica un dato- y su arreglo queda NOMBRADO en Technical Debt: declarar el mes del material en vez de deducirlo de las filas. Y `documentos_vivos` cazo el contador de tests desajustado -decia 548 funciones y hay 555-, que es la enesima vez esta semana que una guardia mecanica pilla un documento separado de la realidad antes que un humano.
- 2026-09-21 (12) · F14a, LA INGESTA DEL DETALLE POR OPERACION, VALIDADA y cerrada en main (merge 15a33ff, tag stable/F14a-ingesta; informe docs/validation/F14A-INGESTA.md, ADR-0037). El contenido de la rama esta en (10) y la primera medida de A-18 en (11); esto es lo que salio DESPUES, al validarla, y es lo que mas cambia. LA PASADA POR EL MATERIAL DE SEPTIEMBRE -v5 y v6, que la rama no buscaba-: A-18 TIENE EVIDENCIA EN LOS DOS LADOS Y SON DE CLASE DISTINTA. De un lado `ev-v6-014702-2d7096db` -el mas reciente DE LOS QUE PESAN SOBRE A-18, posterior a los tres que ella cita, no el item mas nuevo del repositorio- donde el trader RAZONA EN VOZ ALTA sobre su regla y su aritmetica concluye caja completa. Del otro LA PANTALLA: en v5 0:04:52-53 la herramienta de FX Replay calcula el R/R SOBRE ENTRADA-STOP mientras el arrastra el objetivo hasta que marca 3, con riesgo constante en 0,00019 (0,00061/3,21 = 0,00057/3), mas la distribucion de agosto de (11). Es LO QUE DICE SOBRE SU REGLA frente a LO QUE LA HERRAMIENTA HACE MIENTRAS LA USA. POR ESO LA RECENCIA ENTRA COMO SENAL Y NUNCA COMO ARBITRO: la recencia sola elegiria `caja_completa` -v6 es el mas nuevo- y la pantalla y los backtests dicen lo contrario; un trader razonando sobre su regla puede equivocarse sobre su propia regla, la herramienta que usa no. Este caso es el contraejemplo que IMPIDIO declarar "lo mas reciente manda", que era lo que se iba a escribir esa manana. EL LIMITE, sin adornos: no se sabe a que nivel de la caja cae la pata roja del fotograma, las dos lecturas se separan justo ahi, y el .mkv de v5 es NATIVAMENTE 1280x720 -cabecera Matroska y manifiesto `fr-v5-718ecabb`-, asi que por esa via no se cierra. A-18 SIN DECIDIR, `evidence/` sin tocar y la prediccion de mayo congelada. DOS ERRORES DEL CONSULTOR EN EL MISMO BLOQUE, los dos de identificador: cito `ev-v4-011951` como apoyo sin comprobar que estaba SUPERSEDED por `ev-v6-014702`, cuyo sucesor empuja al contrario; y situo la frase falsa en ADR-0037 cuando vivia en el informe. NO SE ESCRIBIO EL ITEM DE v5, y es lo correcto: lo que contradiria son las `notas` de `ev-v6-014702` -interpretacion, no su `afirmacion`, que es aritmetica correcta- y el tema no coincide (`objetivo.rr_13_margen_tres_perdidas` frente a `objetivo.rr`); la guardia exige el mismo tema y no se fuerza. CUARTA APARICION DEL PUNTO CIEGO, con dimension nueva -LA RECENCIA-: `comprobar_citas_revocadas` mira reglas, glosario y vocabulario contra feedback REVOCADO, y NO mira `ambiguedades.yaml` ni los `supersede` de EVIDENCIA; TRES ambiguedades citan evidencia superseded -A-10, A-11 y A-18- con `make check` en verde. Es el patron 3 otra vez, tiene rama propia y no se arreglo aqui. A-21 y A-24, buscadas contra v6 con los terminos escritos y NO APARECEN: siguen abiertas y siguen siendo el motivo de la sesion 2, que es un resultado y no un fracaso. Y DE TODO ESTO SALIO EL ORDEN DE LAS TRES RAMAS, decidido antes del ritual y escrito en Next Action §0, que es donde vive y se mantiene.
- 2026-09-21 (11) · F14a · LA PRIMERA MEDIDA DE A-18, que no estaba en el brief y salio de mirar lo mismo otra vez. El suelo del RR que se habia escrito como 'huella mecanica de la regla' no mide el objetivo planeado: mide el RR REALIZADO sobre entrada-stop, que es exactamente lo que A-18 lleva abierta desde F11. Las dos lecturas PREDICEN cosas distintas -`caja_completa` da objetivo_rr/stop_fraccion_caja = 3,75; `riesgo_real` da 3,00- y agosto da SUELO EN 3,00 (18 filas: minimo 2,50, tres clavadas en 3,00, 16 por debajo de 3,75). LA COMBINACION CONFIRMED DE HOY NO CUADRA CON EL MATERIAL, y las dos salidas tocan un parametro CONFIRMED. No se decide: un mes, 18 filas, y la caja no esta en el fichero -el RR medido es riesgo real por construccion-. A-18 gana la nota; su estado, su `decision` y su `evidencia` no se tocan. Y la frase de F26 va por su TERCERA redaccion en el mismo dia: las dos primeras LAS ESCRIBIO EL CONSULTOR EN EL BRIEF y la sesion las transcribio -el fallo fue en la DECISION y no en la redaccion, asi que la regla vigila EL BRIEF-; la tercera no es error de nadie: F26 no puede puntuar el objetivo hasta que A-18 cierre, porque la regla tiene dos lecturas que difieren un 25 %.
- 2026-09-21 (10) · F14a · LA INGESTA DEL DETALLE POR OPERACION, esperando validacion (rama `feature/F14a-ingesta-del-detalle`, informe docs/validation/F14A-INGESTA.md, ADR-0037). Lo que parecia 'abrir cuatro dias' era escribir F14a entera: no habia ingesta -cero xlsx/openpyxl/pandas en `src/`- ni forma de caso -`find knowledge -name 'caso-*'` vacio-. ADR-0037 nombra el criterio que ya estaba a medias en ADR-0021 §1 y lo extiende a lo que faltaba: LA GRANULARIDAD DEL DATO. Lo atribuible a un dia se abre para ese dia si no esta reservado; un AGREGADO sobre un rango con dias reservados no se abre NUNCA y ninguna autorizacion lo abre; la ESTRUCTURA se verifica contra una lista escrita antes en vez de leerse; y el conjunto de FECHAS del fichero no se publica, porque un dia laborable sin operaciones ES su etiqueta. `CLAUDE.md` §3, que lo prohibia EN BLOQUE, queda corregido: TERCERA vez que es mas estricto que el ADR. Y LO QUE MAS VALE DE LA RAMA ES LO QUE SE MIDIO EN VEZ DE SUPONERSE: se abrio AGOSTO -material de desarrollo, cero dias reservados, comprobado ANTES de abrir- y resulto que NINGUNA columna es el objetivo. `maxTP` esta relleno si y solo si la operacion gano (20/20 y 27/0) e `idealTP` cae del lado de la perdida en 4 de 47. EL OBJETIVO ES UNA REGLA, `objetivo_rr`, con cita literal del trader (`ev-v2-001658-d02fb71a`), y el xlsx no lo registra. Por eso el caso NO lleva campo `objetivo`: un campo opcional vacio es una invitacion a rellenarlo con `maxTP`. Lo cazo el INVARIANTE GEOMETRICO, que estaba puesto como higiene y acabo siendo el discriminador que tres cruces disenados no vieron. Y el corpus contesto DOS veces lo que iba a irse al trader: el objetivo y los parciales.
- 2026-09-21 (9) · LA PUERTA POR PREGUNTA, VALIDADA y cerrada en main (merge 3ae8d1f, tag stable/F13-puerta; rama `trabajo/puerta-por-pregunta`, informe docs/validation/PUERTA-POR-PREGUNTA.md, ENMIENDA de ADR-0033). Lo construido va en la entrada (8). LO QUE HAY QUE ANOTAR AQUI ES LA RETRACTACION, porque vivia en DOS ADR y en Technical Debt y nadie la habia medido: hasta esta tarde estaba escrito que `kappa_entre_sesiones` tenia una FUGA -que tras pasar la puerta `excluir` quedaba vacio y UNA autorizacion leia las etiquetas de TODOS los cubos-. ERA FALSO. Medido en repositorio sintetico: con etiqueta en holdout-1 y en holdout-2 y firmada SOLO la de holdout-2, el comando FALLA nombrando `AUTORIZACION-holdout-1.md` y no lee nada, porque el conjunto que se lee y el que pasa por la puerta se derivan de lo MISMO -mismo `activos`, misma accion, mismas sesiones, mismo `objetivo.id`-. Y falla del lado seguro: `abrir` lanza ANTES que `gastar_pregunta`, asi que a una firma que falta no le cuesta una pregunta. LO QUE SI HAY ES EL ESPEJO, y sigue siendo bloqueante antes de la primera autorizacion: UNA pregunta se gasta UNA vez y abre N particiones, y N LO DECIDE EL DATO, NO EL HUMANO -hay que firmar toda particion reservada con etiqueta en esas dos rondas o el comando falla entero-. Fijado en `test_una_pregunta_abre_todas_las_particiones_con_etiqueta`, que es el que avisara si algun dia si hubiera fuga. TERCERA VEZ QUE UNA PROHIBICION ESCRITA POR EL CONSULTOR RESULTA SER MAS ESTRICTA -o directamente otra cosa- QUE EL MECANISMO: desde esta rama, todo criterio de aceptacion que afirme un defecto lleva el EXPERIMENTO que lo distingue de su contrario, no solo el razonamiento.
- 2026-09-21 (8) · LA PUERTA POR PREGUNTA, esperando validacion (rama `trabajo/puerta-por-pregunta`, informe docs/validation/PUERTA-POR-PREGUNTA.md, ENMIENDA de ADR-0033). LA AUTORIZACION DE UN HOLDOUT NO SE GASTABA, y esta medido: con una autorizacion valida y el pre-registro intacto, `abrir` pasa CINCUENTA veces dejando el repositorio identico -`git status` vacio, UNA sola version del fichero de autorizacion-. La hipotesis de que el historial de git sirviera de registro de aperturas quedo TUMBADA por aritmetica: no distingue 'usada una vez' de 'usada cincuenta' porque son el mismo arbol y el mismo commit, y `abrir` es pura. Por eso el criterio de aceptacion original era insatisfacible y se reescribio. AHORA: la autorizacion CITA la pregunta que abre, esa pregunta vive en `PREREGISTRO.md` con estado ABIERTA/GASTADA, el COMANDO la gasta ANTES de leer -los dos modos de fallo no son simetricos: 'gastada y no leida' cuesta re-pre-registrar, 'leida y no gastada' es el defecto- y `abrir` SIGUE PURA. `para_que`, que era una frase que solo salia en el mensaje de error -o sea que cuando la puerta ABRIA no dejaba rastro-, pasa a ser el id de la pregunta y SE COMPARA. Gastar invalida todas las autorizaciones vivas: es la caducidad automatica de ADR-0033 usada como lo que es, y firmar no invalida nada. DOS HUECOS MAS DE LA MISMA FAMILIA: `casos_reservados` GRITA ante un reparto ilegible -devolvia un mapa incompleto indistinguible de uno completo; medido, un yaml roto bajaba los reservados del repo real de 34 a 24 y `feedback trace` seguia con exit 0-, y el comentario que delegaba en `knowledge validate` se BORRA porque era falso para toda carpeta que el glob ve y el validador de su camino no reconoce. Y `leer_fichero` decide sobre la ruta RESUELTA: `knowledge/cases/holdout/../holdout/2/<fichero>` leia material reservado SIN llamar a `abrir`, medido. Y UNA CORRECCION DE LO ESCRITO AYER: el test de la puerta decia cazar 'un camino nuevo fuera del glob' y era FALSO -los dos lados de la igualdad usaban `repartos_commiteables`, asi que un tercer camino es invisible para ambos-; el docstring se retira, el par pegado a mano se va, entra una enumeracion que NO pasa por el glob, y ADR-0036 §Impacto lleva la correccion. `test_con_todo_en_orden_se_abre` sigue verde: hay un camino que abre de verdad.
- 2026-09-21 (7) · EL SORTEO DE SEPTIEMBRE, VALIDADA y cerrada en main (merge 15a49b0, tag stable/F13-septiembre-sorteo; rama `trabajo/septiembre-sorteo`, informe docs/validation/SEPTIEMBRE-SORTEO.md). Septiembre queda REPARTIDO Y ANCLADO antes de que exista ninguna etiqueta, que era la condicion innegociable de ADR-0034, y por el camino de fidelidad y no por el kit. Artefacto `eurusd-2026-09`, seed 20260921, universo de 14 dias exactos del 1 al 18 y cupos que suman JUSTO 14: no sobra ninguno, asi que no se cae nadie en silencio -la sesion 1 perdio dos dias asi-. LOS TRES MOTIVOS DEL REPARTO, escritos porque es lo que hay que poder reproducir y no el numero: (a) CONCENTRAR, y no por la potencia sino por la TENTACION -ningun reparto llega a las 36 unidades efectivas, asi que ninguna cifra sera defendible; tres cubos de ~3 dias no dan tres medidas, dan TRES CIFRAS QUE SE CONTRADICEN, y eso invita a escoger la que convenga, mientras que un cubo da una cifra honesta con su intervalo ancho a la vista-; (b) `fidelidad-2` y `fidelidad-3` SE QUEDAN VACIAS, reservadas para material que pueda cargar una cifra de verdad -febrero o marzo-, porque llenarlas hoy seria quemar dos aperturas para no medir nada; (c) SOLO 4 `dev` porque MAYO YA TIENE SEIS SIN ABRIR, y los de septiembre estan para comprobar la ingesta y el formato contra un mes DISTINTO -que el motor no acabe afinado solo sobre mayo-, no para afinar. EL HALLAZGO DEL CICLO, y es de los que solo aparecen al estrenar: el test de la puerta afirmaba la union exacta de los repartos de ambos caminos y era cierto POR VACUIDAD para el de fidelidad -no tenia ni un reservado-, asi que borrarle el glob no lo habria roto; ahora exige ademas que NINGUNO de los dos caminos aporte cero. Y en su propio commit, la fecha del backtest: `visto_el` pasa de 2026-09-20 -la ENTREGA- a 2026-09-19, con la fuente dicha tal cual -declaracion del consultor del 2026-09-21, SIN captura porque no la hay- y con el sabado explicado, que es el dato que dentro de seis meses alguien lee como errata.
- 2026-09-21 (6) · EL REPARTO DE SEPTIEMBRE, esperando validacion (rama `trabajo/septiembre-sorteo`, informe docs/validation/SEPTIEMBRE-SORTEO.md). Artefacto `eurusd-2026-09`: 14 dias laborables del 1 al 18 -lo que declara `cobertura_material`-, seed 20260921, cupos 4 `fidelidad-dev` y 10 `fidelidad-1`, `build` Y `anclar` en el mismo commit. EL UNIVERSO SON 14 Y LOS CUPOS SUMAN 14 EXACTOS: no sobra ninguno, asi que nadie se cae en silencio como le paso a `2026-05-25` y `2026-06-29` en la sesion 1. EL ARGUMENTO, que es lo que hay que poder reproducir y no el numero: (a) CONCENTRAR, y el motivo no es la potencia sino la TENTACION -ningun reparto llega a las 36 unidades efectivas, asi que ninguna cifra sera defendible; tres cubos de ~3 dias no dan tres medidas, dan tres cifras que se contradiran entre si, y eso invita a escoger la que convenga-; (b) `fidelidad-2` y `fidelidad-3` VACIAS a proposito, reservadas para material que pueda cargar una cifra de verdad -febrero o marzo-, porque llenarlas hoy seria quemar dos aperturas para no medir nada; (c) solo 4 `dev` porque MAYO YA TIENE SEIS SIN ABRIR, y los de septiembre estan para comprobar la ingesta contra un mes DISTINTO, no para afinar. ANTES DE SORTEAR se comprobo lo que el reparto estrenaba: `asignar` admite cupo 0 en un nombre reservado y una particion vacia simplemente no aparece -la decision no dependia de una limitacion del codigo-, y el test de la puerta sigue cierto con cubos vacios. ESE TEST SE REFUERZA OTRA VEZ: afirmaba la union exacta de los repartos de ambos caminos, pero hasta hoy el de fidelidad no tenia ni un reservado y la igualdad se cumplia POR VACUIDAD por ese lado; ahora exige ademas que ninguno de los dos aporte cero. Y en su propio commit, LA FECHA DEL BACKTEST: `visto_el` pasa de 2026-09-20 -la ENTREGA- a 2026-09-19, que es lo que el trader ha dicho; la fuente es la declaracion del consultor del 2026-09-21 y se escribe tal cual porque NO hay captura en el corpus, y queda anotado que el 19 es SABADO y que cuadra -el material llega al viernes 18-, porque es justo el dato que dentro de seis meses alguien lee como errata. No mueve nada, medido: la sesion 1 es del 2026-09-09 y `kit check` da la salida IDENTICA.
- 2026-09-21 (5) · EL CAMINO DE FIDELIDAD, VALIDADA y cerrada en main (merge 06330e2, tag stable/F13-camino-de-fidelidad; rama `trabajo/septiembre-particiones`, cuyo nombre se quedo viejo: no sorteo nada; informe docs/validation/CAMINO-DE-FIDELIDAD.md, ADR-0036). La rama se abrio para sortear septiembre y LA REVISION DE DISENO LO PARO: `kit build` no puede construirlo -`vistos.yaml` declara `2026-09` visto el 20, `universo()` excluye sus 14 dias y `construir()` aborta- y forzarlo exigia falsear la fecha de la sesion o desactivar el filtro. ADR-0034 §6 ya lo decia. LO MEDIDO QUE MAS IMPORTA, y va escrito en el ADR, en el README del directorio y en la cabecera del modulo para que nadie lo pierda: NO HAY TAMANO MINIMO ALCANZABLE. Hacen falta 36 unidades efectivas independientes (AUDITORIA-2026-09-13-ultracode.md §6.1, recomputado con binomial exacta en la revision); la unidad ejecutable es la SESION H4 y no el dia, asi que los 14 dias laborables de septiembre dan 28 unidades brutas y ~23 efectivas -potencia 0,50-0,68-, y ninguna combinacion de mayo llega tampoco. Mayo MAS septiembre si pasaria de 36, y es exactamente la mezcla de ciego con no ciego que ADR-0034 prohibe interpretar como una cifra. CONCLUSION: lo que este camino aporta es ANTERIORIDAD DEMOSTRABLE -comprobada por maquina- mas una cifra DESCRIPTIVA con su intervalo, NUNCA una cifra con potencia; quien la cite como fidelidad medida estara afirmando lo que no se probo. Y el segundo hallazgo medido: los nombres de particion del kit son GLOBALES -un `AUTORIZACION-<nombre>.md` por nombre y un mapa plano que tira el paquete-, y no esta escrito en ninguna parte que no se compartan, asi que meter dias no ciegos en `holdout-N` daria un cubo cuya cifra no se puede interpretar: de ahi los nombres propios, y con puerta. SE CONSTRUYO: `cases/fidelidad.py` y `knowledge/cases/fidelidad/`; `cobertura_material` con motivo propio y solo tramos; las particiones `fidelidad-1..3` reservadas y autorizables; y `cases/anterioridad.py`, que cierra la deuda de la guardia de ancestro en su cuarta aparicion. Y EL TEST DE LA PUERTA SE HIZO MAS FUERTE, no mas debil: donde afirmaba una cifra pegada (`== 8` por particion, que se habria roto con el primer reparto nuevo) ahora afirma LA UNION EXACTA de los repartos de AMBOS caminos, que no se rompe al anadir uno y ademas caza lo que la otra no veia -un camino que quede fuera del glob de la puerta, que es material reservado invisible-. Entraron tambien las velas de 2026-09 hasta el dia 20, con `kit check` de la sesion 1 IDENTICO a su linea base: lo que costaron las dos ramas anteriores, cobrado.
- 2026-09-21 (4) · EL CAMINO DE FIDELIDAD, esperando validacion (rama `trabajo/septiembre-particiones`, informe docs/validation/CAMINO-DE-FIDELIDAD.md, ADR-0036). LA RAMA SE ABRIO PARA SORTEAR SEPTIEMBRE Y LA REVISION DE DISENO LO PARO: `kit build` no puede construir un paquete de septiembre, medido -`vistos.yaml` lo declara visto el 2026-09-20, `universo()` excluye sus 14 dias con motivo 'mes visto por el trader' y `construir()` aborta-, y forzarlo exigia falsear la fecha de la sesion o desactivar el filtro de vistos. ADR-0034 §6 ya lo decia -'el camino del kit es el del etiquetado ciego y, por construccion, no sirve aqui'- y dejaba abierta la decision de COMO se sortean esas particiones. Esta rama la toma y entrega SOLO EL MECANISMO; el sorteo va en la siguiente, porque un ADR decidido y estrenado en el mismo aliento acaba con la forma de la conveniencia de un mes. LO MEDIDO QUE DECIDE EL RESTO: (1) los nombres de particion son GLOBALES -`casos_reservados` devuelve un mapa plano que tira el paquete y hay UN `AUTORIZACION-<nombre>` por nombre-, asi que meter dias no ciegos en `holdout-N` daria un cubo mezclado con los dias ciegos de mayo y una cifra que no se puede interpretar; y no esta escrito en ninguna parte que no se compartan. (2) NO HAY TAMANO MINIMO QUE ALCANZAR: hacen falta 36 unidades efectivas y septiembre entero da ~23 -potencia 0,50-0,68- y mayo tampoco llega, asi que lo que este camino aporta es ANTERIORIDAD DEMOSTRABLE mas una cifra DESCRIPTIVA con su intervalo, y eso va escrito en el ADR, en el README del directorio y en el modulo para que nadie la cite dentro de seis meses como si midiera algo. (3) El 1-18 es inocuo ESTE mes -19 y 20 son sabado y domingo y `dias_laborables` no los genera- pero el mecanismo hace falta igual, porque este camino se salta el filtro de vistos y entonces la cobertura es el unico filtro que queda. SE CONSTRUYO: `cases/fidelidad.py` y `knowledge/cases/fidelidad/` -artefacto = universo + reparto + ancla, sin cuestionario ni hoja ni sesion, id sin fecha, y NINGUN fichero se exime nunca-; `cobertura_material` en el bloque `config:` con motivo propio y SOLO tramos, porque declarar los dias cubiertos publicaria etiquetas -un laborable del rango que no apareciera seria un dia sin operaciones, y eso ES su etiqueta-; nombres `fidelidad-*` que pasan por la MISMA puerta con su `AUTORIZACION-fidelidad-N.md`; y la guardia de ANTERIORIDAD POR CASO, que cierra la deuda de la guardia de ancestro en su cuarta aparicion. El test de la puerta pasa a afirmar LA UNION EXACTA de los repartos de los dos caminos, que es mas fuerte que la cifra pegada que tenia. Y entraron las velas de 2026-09 hasta el dia 20 -el maximo legal- con `kit check` de la sesion 1 IDENTICO a su linea base, que es lo que costaron las dos ramas anteriores.
- 2026-09-21 (3) · LOS CUPOS CONGELADOS Y EL ANCLA, VALIDADA y cerrada en main (merge 93e17a2, tag stable/F13-cupos; rama `trabajo/cupos-congelados`, informe docs/validation/CUPOS-CONGELADOS.md, ENMIENDA de ADR-0035 y no ADR nuevo, porque el propio ADR-0035 dejo escrito en su Impacto que no cerraba los cupos). LO QUE CIERRA ES UN PATRON, Y ESA ES LA LECTURA QUE VALE MAS QUE EL PARCHE: `datasets` y `cupos` eran EL MISMO DEFECTO -un input GLOBAL Y MUTABLE del que depende la reproduccion de un paquete, y que el paquete tenia que guardar-, solo que uno vivia en `data/manifests` y el otro en `knowledge/cases/kit/config.yaml`. La rama del 20 arreglo el primero; esta arregla el segundo con la MISMA forma: `construir(..., config=)` con el contrato de `datasets=` -None lee el disco, que es lo que un paquete NUEVO tiene que hacer- y `mover_sesion` arrastra los dos. Con eso, editar `config.yaml` para los 14 dias de septiembre ya no rompe la sesion 1: medido con el global a 6/3/3/2, `kit check` IDENTICO a su linea base y `knowledge validate` en exit 0. Y RESUELVE LA PREGUNTA QUE ADR-0035 DEJABA ABIERTA, que no era como congelar sino COMO SE VERIFICA LO CONGELADO: el 20 se dio por bueno que alterar lo congelado se veia porque `particiones.yaml` dejaba de reproducirse, y al medirlo resulto FALSO PARA LA MITAD DE LAS CLAVES. Editar `particiones` dentro del bloque congelado si se ve; editar `anclajes_candidatos`, `sesiones` o `etiquetas` NO -solo alimentan `ventanas.yaml` y `hoja_trader.md`, que una sesion celebrada exime-, y el mutante daba EXIT 0 con "sin diferencias que no explique la sesion celebrada". La respuesta es el ANCLA: `anclas.yaml` declara el sha del BLOB de `ventanas.yaml` y `particiones.yaml`, vive FUERA del fichero que ata, es blob y no commit -`ventanas.yaml` ya tiene dos commits y un ancla de commit lo habria dado por alterado sin estarlo-, y re-anclar es un acto EXPLICITO con `--reanclar`. No hereda el `if not etiquetas: continue` de `validar_paquetes`, a proposito: hoy no existe ni un LABEL_CASE y ese es justo el periodo en el que hace falta. Tres tests nuevos y DOS QUE CAMBIAN DE SIGNIFICADO a proposito: donde afirmaban que sin etiquetas el paquete se podia regenerar libremente, ahora exigen que tocarlo se vea. ADR-0025 y el comentario de `config.yaml` justificaban no tocar los cupos citando el mecanismo sustituido: su DECISION sigue en pie y su ARGUMENTO queda corregido en el mismo commit.
- 2026-09-21 (2) · LOS CUPOS CONGELADOS Y EL ANCLA DEL PAQUETE, esperando validacion (rama `trabajo/cupos-congelados`, informe docs/validation/CUPOS-CONGELADOS.md, ENMIENDA de ADR-0035 y no ADR nuevo: el propio ADR-0035 dejo escrito que no cerraba los cupos). El universo se congelo ayer, pero los CUPOS seguian saliendo del `config.yaml` de HOY: `comprobar()` solo COMPARABA el bloque `config:` del paquete, asi que `config.yaml` era inmodificable mientras existiera un paquete, y septiembre no se podia sortear (`asignar` con 14 casos y 40 cupos: ParticionError). Ahora el bloque congelado se USA -`construir(..., config=)`, mismo contrato que `datasets=`- y `mover_sesion` lo arrastra. AL MEDIR LA FALSABILIDAD APARECIO EL HALLAZGO DE LA RAMA: no es uniforme. Editar `particiones` dentro del bloque congelado se ve -`particiones.yaml` no se exime nunca-, pero editar `anclajes_candidatos`, `sesiones` o `etiquetas` NO: solo alimentan ficheros que una sesion celebrada exime, y el mutante daba EXIT 0 con 'sin diferencias que no explique la sesion celebrada'. Dicho de frente: la linea que esta rama cambia de sujeto era LO UNICO que impedia editar a mano el bloque congelado de un paquete celebrado, y la guardia de ancestro no lo tapa porque se desentiende con `if not etiquetas: continue` y no existe ni un LABEL_CASE. Por eso lo congelado se ata FUERA: `anclas.yaml` declara el sha del BLOB de `ventanas.yaml` y `particiones.yaml` -patron `preregistro_blob` de ADR-0033: fuera del fichero que ata, blob y no commit porque `ventanas.yaml` ya tiene dos commits, y re-anclar es un acto EXPLICITO con `--reanclar`-, y NO depende de que existan etiquetas. El aviso de deriva del config global se muda a `validar_paquetes` como AVISO con exit 0, estrenando un canal que existia desde F10 y no se habia usado nunca. MEDIDO: `config.yaml` editado a 6/3/3/2 deja la sesion 1 IDENTICA a su linea base y `knowledge validate` en 0 con el aviso; el mutante de los cupos sigue viendose fallar; y el de `anclajes_candidatos`, que daba exit 0, pasa a exit 1. Tres tests nuevos y dos que CAMBIAN DE SIGNIFICADO a proposito: donde afirmaban que sin etiquetas todo valia, ahora exigen que tocar lo congelado se vea. De paso, ADR-0025 y el comentario de `config.yaml` justificaban no tocar los cupos citando el mecanismo que esta rama sustituye: su DECISION sigue en pie y su ARGUMENTO queda corregido en el mismo commit.
- 2026-09-21 · EL UNIVERSO CONGELADO, VALIDADA y cerrada en main (merge dfc7e20, tag stable/F13-universo; rama `trabajo/universo-congelado`, informe docs/validation/UNIVERSO-CONGELADO.md, ADR-0035). El universo de un paquete se calculaba del disco de HOY y no de como se construyo, asi que descargar un mes nuevo reparticionaba en silencio un paquete ya cerrado y `particiones.yaml` -la unica prueba mecanica de que las particiones se fijaron antes de etiquetar- dejaba de reproducirse. EL DEFECTO SE MIDIO, NO SE SUPUSO: el universo de la sesion 1 son 42 dias, `asignar` reproduce `particiones.yaml` exacto, y con septiembre descargado CAMBIAN 23 DE ESOS 42 -10 se caen, 13 cambian de particion, entran 10 de septiembre- y `holdout-3` se queda SIN NINGUNO de sus 8 dias. El arreglo: cada paquete declara sus `datasets:` en `ventanas.yaml` y `comprobar()` se recompone con esa lista congelada, igual que ya se hacia con `config.yaml`; `mover_sesion` tambien va por ella y `construir()` de un paquete NUEVO sigue leyendo el disco a proposito. La sesion 1 se relleno de forma ADITIVA (6 lineas, ninguna quitada) y `kit check` da la SALIDA IDENTICA a la linea base comparada con `diff`, que era el criterio, no el exit 0. De paso se cierra un exit 0 que no comprobaba nada -`hay_datos_del_kit` era un AND global y un manifiesto sin ficheros apagaba `kit check` entero sin declarar ninguna lectura; ahora se NOMBRA a quien le falta- y `lectura_de_velas` deja de declarar seis datasets leyendo cinco. Cuatro tests nuevos, con el mutante comprobado. AL MEDIR EL UNIVERSO APARECIO ADEMAS UN AGUJERO QUE NADIE HABIA VISTO: DOS DIAS DEL UNIVERSO NO ESTAN EN NINGUNA PARTICION -`2026-05-25` y `2026-06-29`-, porque los cupos suman 40 y el universo son 42; el sorteo por cupos los deja en los puestos 41 y 42 de forma REPRODUCIBLE con el seed commiteado, y no aparecen ni en `particiones.yaml`, ni en `casos:`, ni en `excluidos:`. No son holdout -nunca estuvieron repartidos-, pero un kappa "sobre el universo" y uno "sobre el paquete" no son el mismo conjunto, y F26 tiene que saberlo: queda en Technical Debt. AVISO para quien descargue el siguiente mes: esta rama tenia que estar dentro ANTES de congelar abril tambien, no solo septiembre.
- 2026-09-20 (3) · EL UNIVERSO CONGELADO, esperando validacion (rama `trabajo/universo-congelado`, informe docs/validation/UNIVERSO-CONGELADO.md, ADR-0035). El universo de un paquete se calculaba del disco de HOY: descargar un mes nuevo reparticionaba un paquete anterior y `particiones.yaml` -la unica prueba de que las particiones se fijaron antes de etiquetar- dejaba de reproducirse, en silencio. MEDIDO sobre el paquete real: el universo son 42 dias, `asignar` reproduce `particiones.yaml` exacto, y metiendo los 14 dias de septiembre CAMBIAN 23 DE ESOS 42 -10 se caen, 13 cambian de particion, entran 10 de septiembre- y `holdout-3` se queda sin ninguno de sus 8 dias. Ahora cada paquete declara sus `datasets:` y `comprobar()` se recompone con esa lista; `construir()` de un paquete NUEVO sigue leyendo el disco A PROPOSITO, porque congelarlo tambien seria el tercer caso del mes de una prohibicion que bloquea un paso que el proceso exige. DERIVAR la lista de `casos[].dataset_id` se midio y NO vale: enero, julio y agosto aportan 66 de las 67 exclusiones de la sesion 1 sin dejar un solo caso, y el donante por contiguidad es invisible en `casos[]` -medido en sintetico: pierde un caso y reasigna uno reservado-. La sesion 1 se relleno de forma ADITIVA (6 lineas, ninguna quitada) y `kit check` da la SALIDA IDENTICA a la linea base comparada con diff. `datasets:` no se exime nunca: se comprueba aparte y sin el es PROBLEMA, no aviso. De paso se cierra un exit 0 que no comprobaba nada: `hay_datos_del_kit` era un AND global sobre todos los datasets del prefijo y un manifiesto sin sus ficheros apagaba `kit check` entero sin declarar ninguna lectura; ahora se NOMBRAN. Y `lectura_de_velas` declaraba seis datasets leyendo cinco. Cuatro tests nuevos, con el mutante comprobado. AVISO para quien descargue el siguiente mes: esta rama tiene que estar dentro ANTES de congelar abril tambien, porque `2026-05-01` esta excluido por falta de abril y abril es mes visto.
- 2026-09-20 (2) · ENTRA EL BACKTEST DE SEPTIEMBRE, VALIDADA y cerrada en main (merge ad2693d, tag stable/F13-septiembre; rama `trabajo/septiembre-entra`, informe docs/validation/SEPTIEMBRE-ENTRA.md, ADR-0034). El trader entrego seis capturas y un xlsx el 2026-09-20. LO PRIMERO, LA EXPOSICION: el consultor abrio el xlsx y leyo la columna de fechas -del 1 al 18-; NO QUEMA (ADR-0021 §1, precedente del 09-13), porque saber que dias cubre un fichero no es leer una etiqueta ni medir una cifra del bot, y porque septiembre no tenia particiones, ni dataset, ni un solo LABEL_CASE. Se declara ademas lo que no se puede probar -Excel pinta la hoja activa entera-, la reserva del 09-12 -un dia sin operaciones ES su etiqueta, y como no se pueden nombrar, F26 los excluye en bloque- y que la lectura cruzo CLAUDE.md, mas ancho que ADR-0021. LOS SIETE FICHEROS entran al inventario tras medir que `corpus inventory` solo guarda ruta, papel, bytes y sha256, y que el proyecto no tiene openpyxl, pandas ni Pillow instalados; el fichero de bloqueo de Excel se borro antes, porque un libro abierto cambia de bytes. SEPTIEMBRE queda declarado visto con `visto_el: 2026-09-20`, la fecha de la ENTREGA: la del backtest del trader NO SE SABE y esta pedida, mismo criterio que abril. ADR-0034 dice QUE ES septiembre: material ETIQUETADO de un mes ya visto, no ciego para una sesion en vivo y si util para medir fidelidad con las particiones fijadas antes de leer una etiqueta; y NO cierra la peticion del mes limpio. LAS VELAS Y LAS PARTICIONES NO ENTRAN: los cupos de config.yaml suman 40 y septiembre tiene 14 dias, y -no previsto por el brief- descargar sus velas rompe la reproduccion de la sesion 1 por si solo. Decidido: se congela el universo en el propio paquete, en rama propia.
- 2026-09-20 · LA LIQUIDEZ DE M15, VALIDADA y cerrada en main (merge b60c44b, tag stable/F13-liquidez; rama `trabajo/liquidez-m15`, informe docs/validation/LIQUIDEZ-M15.md; spec 12.1.0 -> 12.1.1, parche: dos notas, ningun valor nuevo). SE MIDIO LA PANTALLA ANTES DE ESCRIBIR, con dos agentes que discreparon en lo principal y a los que resolvio el fotograma. EL EJE DE A-24 EN F14b §3 NO EXISTIA: `ev-v3-001531` no era el polo "mas extremo" -en fr-v3-982da728/944000 el trader DESCARTA el alto mas alto y marca el de abajo, pegado al precio, que con sesgo bajista es a la vez el menos extremo, el mas proximo y el mas reciente-, y `ev-v3-001242` ("el alto mas alto" en un complex pullback) esta dicho sobre un CROQUIS A MANO en un grafico de 1h donde el alto mas alto es ademas el ultimo: no discrimina. La hipotesis de los DOS CASOS segun el tipo de estructura tambien se cae: "estructura simple" no aparece ni una vez en el corpus. A-24, A-25 y A-26 se ABREN con sus ids reservados y las tres cambian de enunciado: A-24 es una REGLA DE SELECCION abierta que pide criterio reproducible; A-25 pasa a la vida de la marca -su premisa anterior no la sostenia nadie-; A-26 conserva solo el choque flujo de M15 contra sesgo de H4, porque la mitad disyuntiva la cierra el corpus y se ESCRIBE en la spec con sus cuatro citas. A-33 NO se abre: se midio v4 0:57:06 y lo marcado es una LINEA etiquetada "15 lq", no una banda, asi que entra como nota. EL HUECO DEL PRODUCTOR queda anotado y NO tapado (ninguna regla de marcado nueva): `liquidez_m15` tiene cero producciones, RN-008 es un `ninguno_de` que por eso prohibe abrir SIEMPRE, y ninguna guardia lo ve porque un token no puede declarar productor y los predicados de `fuente: mercado` no pasan por alcanzabilidad. Dos supersede con cita de pantalla (ev-v3-001528-87eef4f0, ev-v4-005644-e06ef304) y un item que faltaba (ev-v1-001403-eea19530, que MIDIENDO no sirve de apoyo: es M1 y habla del limite). Con los tres del 17-09 y hoy, TRES items con el mismo vicio de extraccion -la afirmacion quita el deictico o el matiz de la cita-: patron escrito en el informe §7. El punto ciego del detector va como TERCERA aparicion y pasa a rama con nombre en la proxima planificacion. RIESGO DE FIDELIDAD, dicho como en el informe §3: el trader marca la liquidez "la que tu consideres" (ev-v3-003916-447dc8d7), y si A-24 no sale de la sesion 2 con un criterio reproducible -que dos personas mirando el mismo grafico marquen el mismo nivel- la pregunta DEJA DE SER DE LA SPEC y pasa a ser del proyecto: habra que decidir si el bot marca peor que el trader y cuanto cuesta eso en fidelidad. Todo lo que hay aguas abajo -los dos esquemas de entrada, la orden limite, el reinicio de cartuchos y el unico filtro direccional- cuelga de ese nivel.
- 2026-09-17 (6) · EL BREAKER DE M1, VALIDADA y cerrada en main (merge 53e9d17, tag stable/F13-breaker; rama `trabajo/breaker-m1`, informe docs/validation/BREAKER-M1.md; spec 12.0.0 -> 12.1.0, MENOR porque se anade un parametro y ninguna regla cambia de sentido). Habia una contradiccion viva entre dos items de confianza alta del mismo video, con un CONFIRM del trader encima de uno: se resolvio MIRANDO LOS FOTOGRAMAS. A 0:53:12-0:53:17 la pantalla esta en M15 -con zonas etiquetadas a mano `m1 lq` y `15 lq`- y desde 0:53:18 en M1; lo que rompe con mecha es un NIVEL DIBUJADO al que apunta una flecha, con la mecha perforandolo y el cuerpo cerrando por debajo. Los dos items eran ciertos: lo que estaba mal era la `afirmacion` incondicional de ev-v4-005319, que decia mas que su cita y que su pantalla. La supersede `ev-v4-005310-ce69f8c6`, con cita de audio Y cita de pantalla (fr-v4-9ad0ebb8/3203000 y /3209000), creada con `evidence new --supersede` porque el esquema de una propuesta no admite `supersede` -asi se crearon los ocho primeros supersede del proyecto, commit 2003e61-. Medido ANTES de aceptar: ninguna guardia se queja del CONFIRM cuyo objetivo queda supersedido, porque 653efdc ya alineo la comprobacion de EXISTENCIA con todos los items; si alguien pasara solo los vivos, saltaria. El criterio de M1 deja de ser prosa: nace `breaker_m1_criterio_ruptura` (enum mecha|cuerpo, `mecha`, CONFIRMED citando ev-v4-005910, con ev-v3-000606 diciendo lo mismo), `se_da_esquema` lo toma como argumento y RN-008 lo pasa en su forma, que es lo que le da lector desde que `comprobar_consumo` solo cuenta formas. Nace A-32 para la sesion 2: la linea rota NO lleva etiqueta, asi que no consta si es la liquidez de M15 (RN-004, cuerpo) o un nivel de M1. `_contradicciones.yaml` sigue vacio y el hueco del detector queda como deuda. El paquete de la sesion 1 no se toca y `kit check` sigue OK.
- 2026-09-17 (5) · LAS REGLAS DE LA CASA, VALIDADA y cerrada en main (merge 52f579d, tag stable/F13-reglas; rama `trabajo/reglas-de-la-casa`, docs only). `CLAUDE.md` en la raiz recoge lo que hoy llega pegado en cada brief, con cada regla verificada contra el repositorio antes de escribirla: por donde se empieza, main no se toca, los regimenes de cambio, el trailer `Fuente:` (`DIRECTORIOS_CON_FUENTE`), las TRES guardias al anadir un sitio con `cita`, las cifras al registro (ADR-0002), el holdout de ADR-0033 -leer velas no es abrir-, los cuatro sitios de una ambiguedad mas el test que congela las RESUELTAS, las trampas medidas (un heredoc sin comillas convierte `` en BACKSPACE; `## Estado` se lee con `split()[0]`; `make check` a `/dev/null` sale 2 y a un fichero 0) y DONDE ESTA EL TEXTO DE LAS TRANSCRIPCIONES, que es lo que mas tiempo hace perder: los manifiestos en `knowledge/corpus/transcripciones/`, el texto en `data/transcripciones/<video>/<modelo>/`, la version legible con deriva en `corpus/Estrategia del trader/_procesado/transcripciones/` y los segmentos crudos dentro de `knowledge/_proposals/*.yaml` en `contexto.segmentos`. `docs/runbooks/RITUAL.md` escribe el ritual con sus puertas y las tres correcciones de la semana: `BOTSITO_ALLOW_MAIN=1` pegada al `git commit` porque cada linea `!` abre una shell nueva; `make check` pasa de 120 s y se va a segundo plano, asi que el push no se encadena detras -el 2026-09-17 se pusheo antes de saber si pasaba-; y de una linea en una, mirando la salida. knowledge/, src/ y tests/ sin tocar.
- 2026-09-17 (4) · LOS MESES VISTOS, VALIDADA y cerrada en main (merge 1c2561e, tag stable/F13-vistos; informe docs/validation/MESES-VISTOS.md). Al validar, el consultor decide: manda la fecha de la sesion porque la ceguera tiene que valer al ETIQUETAR -un paquete construido antes y etiquetado despues de que el trader vea el mes esta contaminado igual-; (a) aceptada con sus tres condiciones, y la tercera es un DEFECTO de la guardia de ancestro a comprobar por caso; abril, el 2026-09-05, la unica fecha con fuente. `mover_sesion` a una fecha posterior a un `visto_el` falla y restaura (test). Cierra el hueco que `vistos.yaml` declaraba desde el 2026-09-12. Cada mes o dia visto lleva `visto_el`, y cuenta para un paquete solo si es igual o anterior a la fecha de su SESION -la del nombre: el commit da la del ultimo `mover_sesion`, y una fecha dentro del paquete romperia la reproduccion-. MAYO queda declarado visto el 2026-09-11 y `kit check --sesion 2026-09-09-sesion-01` da la MISMA salida que antes, medida con `diff`. Guardia en `construir()` -falla, no avisa- y en `knowledge validate`, sin datos. `kit kappa` avisa de etiquetado no ciego. La sesion 2 etiqueta sobre el paquete de la sesion 1 (sus 10 `dev` de junio), con tres condiciones: confirmacion escrita de que el trader no backtesteo junio -su CONFIRM del 09-09 decia que lo haria-, material sin los `dev` de mayo, y resolver que la guardia de ancestro no ve etiquetas de otra sesion. Un paquete nuevo solo de junio esta bloqueado: `config.yaml` es global y cambiar los cupos rompe la sesion 1. knowledge/spec sin tocar.
- 2026-09-17 (3) · LA GUARDA DEL HOLDOUT, VALIDADA y cerrada en main (merge 44a9fc1, tag stable/F13-guarda; informe docs/validation/GUARDA-DE-HOLDOUT.md). Antes del merge, REVISADA POR EL CONSULTOR y corregida en la misma rama (informe §8 y §11). Decide: la salida `LECTURA:` da RECUENTO por particion y no fechas -puede acabar delante del trader, a quien la hoja le oculta esos dias-; el kappa EXCLUYE los reservados por defecto y dice sobre cuantas unidades y casos se calculo; el formato de la autorizacion vale con un campo nuevo. HALLAZGO POSTERIOR: la autorizacion no ataba QUE pre-registro se aprobo, asi que se podia autorizar, abrir y despues cambiar los umbrales. Nace `preregistro_blob` (el sha del blob, no del commit: se aprueba un contenido, y el blob no se mueve con otros commits ni con un rebase); la puerta cierra si no coincide con el PREREGISTRO commiteado. knowledge/spec sin tocar.
- 2026-09-17 (2) · LA GUARDA DEL HOLDOUT, en la rama (cerrada en main, ver la entrada de arriba; rama `trabajo/guarda-de-holdout`, informe docs/validation/GUARDA-DE-HOLDOUT.md, ADR-0033). Extrae de F14 su D4 y su criterio 3. La guarda de `tests/conftest.py`, stub desde F10, es un hook de auditoria `autouse` para cualquier llamante -restringida a `spec` y `domain`, como prometia, no habria visto nada: la revision midio que ninguna lectura de la suite los tiene en la pila- y se ve saltar por cada via de lectura. Nace la puerta `botsito.cases.holdout`: abrir exige PREREGISTRO relleno y autorizacion commiteada por particion, y cubre los ficheros del holdout y el VALOR de las etiquetas de casos reservados -`kit kappa` los excluye y `feedback trace`, que los imprimia, los oculta-. Las velas NO pasan por ella: construir un paquete exige leer las de todos los dias, y eso no es abrir. `kit build` y `kit check` declaran en su salida los dias reservados cuyas velas leen, y la obligacion 6 de HOLDOUT-EXPOSICIONES, que prohibia ejecutarlos con datos y bloqueaba la sesion 2, queda reescrita. knowledge/spec sin tocar (spec 12.0.0).
- 2026-09-17 · FIDELIDAD DE LA SPEC, VALIDADA y cerrada en main (merge e4f761c, tag stable/F13-fidelidad; informe docs/validation/FIDELIDAD-DE-LA-SPEC.md). Antes del merge, REVISADA POR EL CONSULTOR y corregida en la misma rama (informe §7 y §10). Decide: margen de la firma 0,5 CONFIRMADO, A-29 con su default y prioridad de la sesion 2, RN-013 descartada por absorbida y ADR-0032 punto 3, aceptados; RN-019 aceptada con una correccion. HALLAZGO POSTERIOR AL INFORME: la exencion de cartucho era ancha de mas -una entrada activada sin ruptura que se iba al stop entero no gastaba intento y habilitaba reentrar, y el trader nunca eximio ese caso-. El resultado del cierre gana `salto_el_stop`: el stop entero gasta sea cual sea la activacion y solo la salida en rojo sin stop (el equal del trader) no gasta. `cartucho_criterio` separa lo que dijo el trader de lo que es nuestro, y nace A-31 (sesion 2). spec_version se queda en 12.0.0 por decision del consultor: la rama no se ha fusionado. En esta rama se declara ademas, con cuatro dias de retraso, la EXPOSICION DE HOLDOUT DEL 2026-09-13 (docs/validation/HOLDOUT-EXPOSICIONES.md): dos ejecuciones de `kit check` con `data/` presente durante la auditoria ultracode, que leyeron las velas M1 de los 24 dias reservados de mayo y junio para recalcular hashes, sin ver etiquetas, precios ni cifras del bot; NO quema (ADR-0021 §1 y §4). Y la obligacion nueva: `kit check` y `kit build` no se ejecutan con `data/` presente hasta que una guarda lo impida, porque la prevista (`holdout_guard`, `tests/conftest.py`) es un stub y tal como esta descrita no cubriria la CLI.
- 2026-09-16 · LAS CORRECCIONES DE FIDELIDAD DE LA SPEC, en la rama (cerrada en main el 2026-09-17, ver la entrada de arriba; rama `trabajo/fidelidad-de-la-spec`, informe docs/validation/FIDELIDAD-DE-LA-SPEC.md; spec 11.1.0 -> 12.0.0 en un solo bump). La forma que F18-F22 van a implementar no colocaba ninguna orden, vetaba las dos direcciones en las que el trader opera y dejaba posiciones sin objetivo. RN-005 ESTABA AL REVES y ahora nombra el lado de ruido (`lado_de_ruido`), con una cita por sentido. NADA COLOCABA LA ORDEN: nace `colocar_orden_limite` y la orden se prepara en RN-011 y se coloca en RN-015, con stop y objetivo escritos antes de enviar y los gates entre medias (ADR-0032); RN-013 queda DESCARTADA por absorbida. `operacion_abierta` y `orden_limite_pendiente` declaran `origen: broker` (ADR-0028 §5) y ninguna forma puede fijarlos. `equal` deja de ser token: `activacion_sin_ruptura`, `break_even` y `por` en el cierre; RN-016 no gasta cartucho al cerrar un equal y RN-019, que no podia disparar nunca, dispara. La firma frena en el limite menos `firma_margen_seguridad` y no abre lo que no cabe (ADR-0031: RN-029 diario, RN-031 total y permanente, RN-032 prospectiva; RN-030 pasa a `terminal`). Guardias: ligadura, vocabulario con claves cerradas, `fuente`/`lo_provoca`/`efecto`/`valores`, `comprobar_consumo` solo cuenta formas (destapo cuatro parametros sin lector, uno de ellos `firma_magnitud_vigilada`), `reinicia_con` nunca booleano, `complementa` contra algo que existe, y los cuatro mutantes de `comprobar_precedencia` muertos. Ambiguedades con `clase` (medicion | pregunta): el cuestionario ya no pregunta mediciones; nacen A-29 (cuando nace la orden, el corpus dice dos cosas) y A-30 (la pendiente a las 15:00). La revision de diseno reescribio cinco puntos del brief antes de programar (2.2, 2.3, 3, 8 y 9); todo va en el informe. Sin motor, sin tocar evidencia ni feedback, sin abrir holdout.
- 2026-09-14 · FTMO Y ARQUITECTURA, VALIDADA y cerrada en main (merge 00ad174, tag stable/F13-ftmo; informe docs/validation/FTMO-Y-ARQUITECTURA.md). El consultor la aprobo con RN-030 tal como esta -identica en forma a RN-002- y con dos anotaciones: F14b avisa de que su numeracion provisional de reglas quedo obsoleta, y la clase de RN-030 y la guardia de ligadura pasan al brief siguiente. FUNDEDNEXT NO ADMITE BOTS desde 50.000 -ni en el reto ni en la fondeada-, asi que el objetivo del proyecto era imposible ahi: LA FIRMA PASA A SER FTMO 2-Step SWING de 100.000 (ADR-0026), leido su reglamento ese dia con cita por afirmacion. El tipo Swing no restringe noticias y BORRA DEL CAMINO CRITICO EL CALENDARIO ECONOMICO: `filtro_noticias` vuelve a `no`, RN-028 DESCARTADA, A-17 DECIDIDA y A-22 con el sentido invertido (enmienda de ADR-0022, que partio de un supuesto cierto en FTMO Standard y en FundedNext, justo las cuentas que no se eligieron). Los topes de la firma entran por fin en el registro -ADR-0004 lo prometio y ninguno de sus parametros lo era- y en la spec como RN-029: el MAS RESTRICTIVO NO ES SIEMPRE EL DEL TRADER, porque por encima de 111.111,11 de saldo al empezar el dia su 4,5 % supera el 5 % del capital inicial, y su semanal no cubre el total estatico. EL DIA DE RIESGO ES CIVIL (ADR-0027): el reglamento corta a medianoche CE(S)T, A-19 DECIDIDA y desaparece el tercer reloj; MASTER_PLAN decia "medianoche de servidor" sin fuente. Y los cuatro ADR de arquitectura que la auditoria del 09-13 echo en falta: riesgo por tick, estrategia al cierre de M1 y ordenes por evento con punto fijo (ADR-0028, cuyo punto 5 NO esta aplicado a la spec), BID y redondeo con empate en contra del bot (ADR-0029, sin verificar que FX Replay dibuje BID), arbol generico + primitivas a mano (ADR-0030). LO QUE EL BRIEF PEDIA Y EL ESQUEMA NO ADMITIA: "UNKNOWN con ambiguedad_id" no existe, y una regla vigente no puede nombrar un UNKNOWN; el consultor partio la pregunta en A-27 (cinco del instrumento, DEFAULT_AMBIGUOUS, con el valor de FundedNext declarado como default no verificado) y A-28 (reloj del servidor, UNKNOWN, que no se cierra antes del cambio de hora de octubre), y dejo que las guardias decidieran lo segundo. A-24..A-26 quedan RESERVADAS en `test_kit` con una exencion que se autoliquida. Una guardia corrigio el diseño de RN-029 -quien fija un freno tiene que leerlo- y su efecto va declarado. La auditoria de cierre (dos agentes Sonnet) encontro evidencia sin relacion tematica en A-27 y A-28 y un literal cortado antes de que el trader dijera su cifra; corregidos. AL VALIDAR, el consultor pidio tres correcciones mas: RN-029 cerraba a mercado con OP SIN LIGAR -la unica de la spec- y un `si` literal, y leyendo `detenido_por_tope` habria emitido un cierre en cada evento mientras el bot estaba parado; como la forma no puede condicionar una accion a una ligadura atada en una rama de `cualquiera_de`, el cierre se parte a RN-030 (liga OP en `todos_de`, `si: firma_cierre_al_tope`); y A-28 gana la verificacion en el panel de que el corte es medianoche CE(S)T y no la del servidor. Al brief siguiente: lector ejecutable de `firma_magnitud_vigilada`, valor permanente de `detenido_por_tope` para el tope total y token de "nunca" en `perdida_total_firma.reinicia_con`. spec_version 10.2.0 -> 11.1.0. make check verde: 663 casos, 473 funciones. QUEDA del dueño: no comprar sin confirmar Swing en el panel, medir A-27 y A-28 en la prueba gratuita grabando spread y ticks, pedir el mes limpio y declarar la exposicion de la auditoria del 09-13.
- 2026-09-13 · AUDITORIA DEL MATERIAL RECOGIDO, cerrada en main (merge 0a9612d, tag stable/F13-auditoria; informe docs/validation/AUDITORIA-2026-09-12-material.md). Nace de una pregunta del consultor: si tres exportaciones de backtest del trader -enero, abril y agosto, 143 operaciones- llevaban nueve dias en el corpus sin usar mientras se planificaba F14 sobre SEIS dias, ¿habria mas? Tres barridos en paralelo dicen que si. DOS DEFECTOS DE NEGOCIO EN LA SPEC: `liquidez_tomada` se enciende y NO SE APAGA NUNCA -el motor reentraria sobre la misma liquidez indefinidamente-, y RN-010 no declaraba posicion viva, asi que una entrada activada por un EQUAL era INVISIBLE para el cierre forzoso de las 15:00 y para el break even; el segundo va arreglado, el primero esta diseñado y BLOQUEADO por un defecto del propio diseño (F14b). LA OBSERVACION DE INVIERNO QUE ADR-0015 DABA POR INEXISTENTE estaba en el corpus desde el 3 de septiembre: las operaciones de enero van de 06 a 13 UTC y las de abril y agosto de 05 a 12, o sea hora de pared identica y horas UTC que se mueven con el cambio de hora; confirma empiricamente el reloj civil (ADR-0017) y la ventana 07:00-15:00, que se sostenian en una decision sobre algo NO MEDIDO. Y el numero que faltaba para dimensionar el riesgo: enero encadeno 9 perdidas consecutivas -la evidencia decia 7, tomada a mitad del backtest- y SEIS el mismo dia, que con ADR-0020 son 3,0 % de la cuenta en una sesion. LA CONTRADICCION `stop.nivel` QUEDA CERRADA, la unica del proyecto y abierta desde F06, con los OCHO PRIMEROS `supersede` sobre evidencia de la historia del repositorio; dos de los cuatro items a 0,75 los encontro agrupar la evidencia POR PARAMETRO en vez de por tema, que es como el detector mira y por eso lleva 0 detectadas de al menos 6 reales. Y estrenar ese mecanismo destapo TRES GUARDIAS que nunca se habian enfrentado a un item supersedido: la de contradicciones SE MORDIA LA COLA -exigia que siguiera ABIERTA, asi que cerrar una invalidaba el registro que la cierra-, el golden de F07 miraba solo los vivos cuando mide la EXTRACCION, y `kit check` decia que tres ambiguedades citaban evidencia "que no existe" porque miraba solo los vivos mientras `knowledge validate` miraba todos: dos llamadas a la misma comprobacion diciendo cosas distintas. LECCION: un mecanismo que existe y no se usa no esta probado, esta sin estrenar. El trader cierra ademas la unica pregunta que la auditoria le dejaba -el trade se deja correr hasta las 3pm: gana RN-002 y la spec no cambia; lo que queda viejo es su propia ficha de reglas- y el registro que lo recoge es el PRIMERO que usa `recibido_el` para lo que ADR-0023 lo creo. Descartada la via de la pestaña `Prop firm` de FX Replay: no la tiene configurada con FundedNext, asi que A-17 y A-19 siguen necesitando el reglamento y el panel. spec_version 10.1.1 -> 10.2.0. make check verde: 663 casos, 473 funciones. PENDIENTE: pedirle JUNIO al trader -el mes que ya debe, y el unico material que no ha visto, no sale en ningun video y tiene su particion YA SELLADA-, y decidir lo de los hechos durativos.
- 2026-09-12 (10) · LAS TRES DECISIONES DEL CONSULTOR QUE QUEDABAN, cerradas en main (merge b332639, tag stable/F13-decisiones; informe docs/validation/DECISIONES-2026-09-12.md). F13 construyo el estado DECIDIDA y dejo su uso fuera de alcance a proposito; esta rama lo usa. A-15 queda DECIDIDA -la ventana se queda en 07-11 y 11-15- y resulto mas simple de lo que parecia: no era una pregunta que el trader se reservara, es una que DEVOLVIO ("puedes buscar las operaciones donde sea, o sea, no hay problema"). A-16 NO SE PODIA CERRAR ENTERA: pregunta como se comparan decisiones tomadas sobre velas de OANDA con un bot medido sobre Dukascopy, y el anexo del 2026-09-09 midio otra pareja -MT5 contra Dukascopy- y lo dice el mismo, "esta medicion no la cubre"; se parte con el mismo corte que ADR-0022 le hizo a A-17, la MEDICION se queda en A-16 (ABIERTA, resuelve_en F26) y la DECISION de metodo nace como A-23 (DECIDIDA: la referencia es Dukascopy, MT5 para spread, ejecucion y paridad, y la divergencia entra en F26 como MARGEN DECLARADO). Cerrarla entera habria metido la obligacion de medir en la prosa de un ADR, que es donde el aviso de RN-021 sobre las noticias vivio tres dias sin que ninguna guardia lo mirara. Y ADR-0025: EL REPARTO DE MAYO NO SE TOCA -6 dias `dev` (05-08, 05-12, 05-15, 05-18, 05-20 y 05-28) y 13 de holdout 6/4/3, junio fuera del universo de F14-. Reparticionar todavia era legitimo -no existe NI UN SOLO LABEL_CASE, comprobado- y se dice a cambio de que se renuncia: `particiones.yaml` se reproduce byte a byte SIN exencion y es la unica prueba mecanica de que las particiones se fijaron ANTES de etiquetar; cuatro dias mas de un mes YA EXPUESTO no valen eso. Ademas hay un cierre mecanico: `cases/paquete.py` compara el config que el paquete guardo contra el `config.yaml` de hoy, asi que tocar los cupos rompe la comprobacion de la sesion 1 entera. Efecto visible: `ventana_inicio` y `ventana_fin` dejan de figurar como "corriendo con un valor en revision" en `spec status`, donde no pintaban nada. make check verde: 662 casos. F14 DESBLOQUEADA; queda pedirle al trader el mes limpio, que tras ADR-0025 ya no es conveniente sino la unica via para que la biblioteca crezca.
- 2026-09-12 (9) · F13 VALIDADA por el usuario y cerrada en main: merge --no-ff ce3b185, tag stable/F13. Entra `docs/spec/` GENERADO desde `knowledge/spec/` con guardia que compara el TEXTO ENTERO -no un hash: el hash cubre tres ficheros y no `ambiguedades.yaml`-, mueren dos copias vivas (el §2 del acta de la sesion 1 y el recuento del README de la spec), se cierran las cuatro deudas heredadas -TRES estaban mal enunciadas en el brief- y la hoja que se lleva a la sesion entra en la biblioteca (`botsito kit hoja`). Con ella, ADR-0022 (el bot no opera noticias en la cuenta fondeada; nace el estado DECIDIDA) y ADR-0023 (`recibido_el` y `procedencia` en el feedback). LA AUDITORIA DE CIERRE (dos agentes) encontro SEIS formas de colar un valor de negocio en la forma ejecutable: la peor, `tope: 9.5` en vez de `tope: perdida_maxima_diaria`, subia el tope de perdida diaria de 4,5 a 9,5 SIN TOCAR EL REGISTRO y sin una queja; de ahi nace la seccion `tokens`. Encontro tambien que RN-013 tenia DOS TIPOS en la misma casilla (`a: si` cadena, `a: no` booleano de YAML 1.1), que `feedback pending` daba por reflejado un RESOLVE_CONTRADICTION con la contradiccion todavia ABIERTA -ahora tiene TRES estados, y el tercero es "sin mecanismo": no afirmar lo que no se puede comprobar-, que `spec status` decia "0 en prosa" con RN-028 (`gate`) sin condicion definida, y una guardia MUERTA escrita en la propia rama, con BACKSPACE literales donde iban `\b`. Del lado de documentacion, dos afirmaciones de negocio FALSAS en PROJECT_STATE, que es el primer fichero que lee toda sesion. Y la mitad B del objetivo del brief, que se habia dado por hecha sin serlo: `test_documentos_vivos.py` prohibe pegar recuentos en los documentos que describen el presente, con exenciones nombradas por seccion y una por linea con motivo. spec_version 10.0.0 -> 10.1.1. make check verde: 662 casos, 472 funciones. QUEDA ABIERTO y es del consultor: el ADR que cierre A-15 y A-16 antes del `kit build` de la sesion 2, el reparto de mayo para F14, pedirle al trader un mes limpio (febrero o marzo) y la contradiccion `stop.nivel`, que se deja ABIERTA a proposito. Siguiente: F14.
- 2026-09-12 (8) · LA SPEC LEGIBLE SE GENERA, Y LAS CUATRO DEUDAS HEREDADAS CERRADAS. `docs/spec/` sale de `knowledge/spec/` con `botsito spec docs` -cuatro documentos, uno por fichero fuente- y un test de contrato REGENERA Y COMPARA EL TEXTO ENTERO, no un hash: el hash de la spec cubre tres ficheros y no `ambiguedades.yaml`, asi que sellar con el mentiria sobre una cuarta parte. Lo que MUERE, que es la mitad que justifica la funcionalidad: el §2 del acta de la sesion 1 -"la estrategia tal como queda especificada", que ya habia estado vieja dos veces en dos dias, las dos en hechos de negocio- y el recuento pegado a mano de `knowledge/spec/README.md`. LAS CUATRO DEUDAS, y TRES ESTABAN MAL ENUNCIADAS. (a) El mapa del kit tenia tres columnas y dos sobraban: `opciones` las sostiene el registro -donde coincidian eran identicas, pero `dias_operables` tenia enum en el registro y NADA en el mapa, asi que el cuestionario preguntaba ABIERTO por algo que el registro solo admite CERRADO- y `ambiguedad` la sostiene `ambiguedades.yaml`, columna que llevaba PARADA DESDE F10 (de las diez A-N nacidas despues, ninguna figuraba en ella; en A-7 ademas decia otra cosa) y que no se notaba porque el cuestionario hacia la UNION de las dos fuentes: la union tapaba la deriva. Su unica arista viva se mudo a `ambiguedades.yaml` antes de borrarla. Al unificar moria el test que las cruzaba, y se repone contra el PAQUETE COMMITEADO -mejor guardia: mira la prueba de lo que se le pregunto al trader, no el fichero del que salio- que en su primera ejecucion encontro el renombre `desde_075` -> `hasta_stop_fraccion` que la anterior no podia ver. (b) `feedback pending` listaba los 70 activos sin mirar si el valor ya habia llegado: ahora dice 0 pendientes de 72, con el criterio por tipo de objetivo y un REJECT reflejado cuando el parametro DEJA de citarlo. (c) el brief pedia recorrer la cadena de `supersede` mas alla del predecesor inmediato y NO HACIA FALTA -comparar con el predecesor ya es transitivo-; el hueco real era el TIEMPO, que nada impedia corregir a un registro POSTERIOR, y no se podia cerrar hasta que existio `recibido_el`. (d) `_ARGS_DE_VALOR` era una lista blanca AL REVES: solo se comprobaban los argumentos que figuraran en ella, asi que inventar un nombre bastaba para colar un valor crudo -medido: `sentido: alcista` pasaba sin una queja-. Ahora se niega por defecto. Y la hoja que se lleva a la sesion entra en la biblioteca (`src/botsito/cases/hoja_docx.py`, `botsito kit hoja`): era el unico codigo que se ejecuta DELANTE DEL TRADER y el unico sin red, y el traslado destapo un `EURUSD` horneado y catorce `SystemExit` en un modulo de libreria. make check verde: 648 casos, 463 funciones.
- 2026-09-12 (7) · EL FEEDBACK YA SABE CUANDO LLEGO CADA RESPUESTA (D5 de F13). Dos campos nuevos, `recibido_el` y `procedencia`, OPCIONALES en el esquema y OBLIGATORIOS POR GUARDIA desde la sesion del 2026-09-13. El numero que decidio el diseno: los 117 registros conservan su id EXACTO -cambian 0, medido y con test- porque `contenido_canonico` salta el campo ausente, que es el mismo mecanismo con el que F11 anadio `valor_canonico`. Hacerlos obligatorios no les habria "cambiado el id": habria dejado los 117 SIN CARGAR, porque `_validar` revienta antes de calcularlo, y rellenarlos si movería el id, o sea renombrar 117 ficheros que el hook y `test_feedback_history` declaran inmutables. POR QUE IMPORTA: `fecha` es la de la sesion -y esta bien asi, fecha la PREGUNTA- pero tres registros de la sesion 1 llegaron despues (A-11 el 10, el acuerdo del lotaje y el WhatsApp de A-20 el 11) y se leen como del 9. Para F26 es la unica forma mecanica de decir que valores se fijaron ANTES de la exposicion de holdout del 2026-09-11 y cuales despues (ADR-0021). `procedencia` es un enum de SEIS valores sacados de los 117 reales, no imaginados: incluye `correccion_consultor`, que la propuesta original no tenia y que cubre cinco registros que se quedaban sin casilla. Y no es decorativo: `trader_grabado` exige medio grabado, `trader_escrito` y `referido_por_consultor` exigen `medio: escrito`, y `correccion_consultor` exige `supersede` porque no trae respuesta nueva sino que retira lo que otro afirmaba. La guardia se comprueba AL CARGAR y no solo en `feedback new`, o un fichero escrito a mano se la salta: es la leccion que `knowledge validate` ya habia aprendido con `feedback apply`. make check verde: 636 casos.
- 2026-09-12 (6) · EL BOT NO OPERA NOTICIAS (ADR-0022), y nace el estado DECIDIDA. Decision del consultor con el matiz que el mismo aporto: el trader SI las opera y su estrategia funciona dentro de esos eventos, pero lo hace en cuentas PROPIAS que no lo prohiben; el bot va a una cuenta fondeada que puede prohibirlo como norma, y la sancion es perder la cuenta aunque la operacion acabe en profit. No es un cambio de estrategia: es una RESTRICCION DE LA CUENTA, de la misma familia que RN-026 (stops level) y RN-027 (redondeo). RN-021 se parte -se queda con el spread, que el trader dijo que no filtra- y las noticias van a RN-028, `gate`, con `decision: ADR-0022` porque su cita dice lo CONTRARIO de lo que la regla hace. RN-028 nace con `pendiente_definicion: A-17`: se sabe QUE bloquea y no CON QUE VENTANA, porque nadie ha leido el reglamento. `filtro_noticias` pasa a `regla` y -esto lo forzo una guardia, no yo- CAMBIA DE CATEGORIA a `prop_firm`: `test_fichero_real_cada_valor_de_estrategia_cita_al_trader` rechazo que un valor de estrategia viniera de una decision nuestra, y tenia razon. La capacidad se conserva: la opcion `no` sigue ahi para el dia que el bot corra donde se permita. A-17 se parte en dos como pidio el consultor: se queda con la VERIFICACION del reglamento (ABIERTA) y nace A-22 con la decision de alcance (DECIDIDA). Ademas A-14 CERRADA: estaba respondida de hecho desde el 2026-09-10 y le faltaba la frase, que el consultor confirmo por escrito; se cierra con un registro REFERIDO, igual que A-11. ESTADO NUEVO `DECIDIDA` con tres guardias -el ADR existe, el ADR NOMBRA la ambiguedad, y no vale sobre una bloqueante ni sobre una que sostenga el default de un parametro- y su linea propia en `spec status`, porque si no seria invisible. Tiene que ser un ESTADO y no un campo: `cuestionario.py` mete toda ABIERTA en el cuestionario de la sesion siguiente, asi que con un campo se le volveria a preguntar al trader lo que el consultor ya decidio. spec_version 9.1.0 -> 10.0.0. make check verde: 632 casos.
- 2026-09-12 (5) · F13 ABIERTA y su revision de diseno CERRADA el mismo dia (dos agentes), con el brief reescrito porque la revision DEMOLIO SU MOTIVACION: las cinco copias viejas que lo justificaban son ciertas -y son seis en tres dias, no cinco en nueve- pero NINGUNA era una copia de `knowledge/spec/` a `docs/spec/`; todas eran prosa narrativa, asi que el documento generado no habria evitado ninguna. El objetivo pasa a ser doble: SUSTITUIR lo que hoy se mantiene a mano y EXTENDER la guardia anti-copia, que ya existe desde el 2026-09-10 y es estrecha, no inexistente. D1..D6 cerradas con evidencia medida: cuatro documentos y no uno (el hash cubre tres ficheros y no `ambiguedades.yaml`); byte a byte con exenciones nombradas, como `kit check`; la hoja del trader se puede mover por UNA linea y cero errores de mypy, pero a `cases/` y no a `spec/`, que las capas lo prohiben; `DECIDIDA` es un ESTADO y no un campo -las dos revisiones discreparon y decidio el codigo: `cuestionario.py:123` mete toda ABIERTA en el cuestionario siguiente, asi que un campo haria que se le volviera a preguntar al trader lo que el consultor ya decidio-; `recibido_el` y `procedencia` opcionales con guardia desde el 2026-09-13, porque medido sobre los 116 registros reales NINGUN id cambia si son opcionales y los 116 DEJAN DE CARGAR si son obligatorios; y unificar las `opciones` del mapa es seguro, la premisa contraria era falsa y `kit check` ya da exit 0 con los dos ficheros exentos. Anotado para hacer ANTES: A-14 se cierra hoy con un registro referido, como se cerro A-11, y deja el problema en tres ambiguedades del consultor y no cuatro.
- 2026-09-12 (4) · QUE CUENTA COMO ABRIR UN HOLDOUT, decidido por el consultor (ADR-0021). El proyecto llevaba desde F01 diciendo "un holdout abierto queda quemado" sin definir que es abrir, sin decir quien autoriza y sin procedimiento para una exposicion accidental; la auditoria de proceso lo encontro y la exposicion YA HABIA OCURRIDO. Decidido: abrir es leer las etiquetas de esos dias o medir cualquier cifra del bot sobre ellos; ver el RESULTADO AGREGADO no abre -un PnL diario no contiene ninguna decision y no se puede invertir para deducirlas- pero SI se declara. La exposicion del 2026-09-11 -el calendario de PnL dia a dia de todo mayo, trece dias reservados- NO quema, queda registrada en `docs/validation/HOLDOUT-EXPOSICIONES.md` (nuevo) y F26 tendra que citarla en su informe: sin esa frase su cifra no es defendible. `holdout-1` se reserva intacto para la nota. Nace tambien `docs/validation/PREREGISTRO.md`, que `docs/validation/README.md` y MASTER_PLAN §G exigian en presente desde hace meses y no existia: va VACIO a proposito, y mientras lo este no se abre ningun holdout. Y queda pedido un mes nuevo al trader, que es la unica forma de tener una particion limpia de verdad. F14 hereda implementar la guarda de `tests/conftest.py`, que hoy es un stub pese a que PROJECT_STATE la daba por viva.
- 2026-09-12 (3) · F12 VALIDADA por el usuario y cerrada en main: merge --no-ff 77c7501, tag stable/F12. Entra la forma ejecutable de las 24 reglas vigentes (ADR-0019), la precedencia por clase (ADR-0018), siete guardias semanticas, `botsito spec check` y el campo `consumido_por`; y con ella una decision de negocio, ADR-0020, que sube el lote un 25 %. Queda ABIERTO y anotado: las tres decisiones que la auditoria de proceso dejo sin cerrar -que cuenta como abrir un holdout y que se hace con la exposicion del P&L de mayo, como se cierra una ambiguedad que decide el consultor (A-15/A-16/A-17 llevan decididas y abiertas desde el 2026-09-09), y si el registro de feedback necesita `recibido_el`- mas el reparto de mayo para F14. Siguiente: F13.
- 2026-09-12 (2) · AUDITORIA DE ORDEN (dos agentes: proceso/metodo y consistencia del repositorio). Lo aplicado, por gravedad. FALSEDADES QUE PODIAN COSTAR DINERO: (1) LA PRECEDENCIA ESTABA ESCRITA AL REVES en dos documentos -`gate > disparador > terminal` cuando ADR-0018 y `CLASES_REGLA` dicen `gate > TERMINAL > disparador`-, o sea que a las 15:00 activar una entrada habria ganado al cierre forzoso, y F22 lo va a implementar leyendo esos textos; (2) el acta de la sesion 1 -que el HANDOFF presenta como "el esquema completo de la estrategia"- seguia diciendo que el lotaje va sobre la caja completa, que el riesgo real es 0,4 % y que el stop se mueve tras el llenado: las tres invertidas por ADR-0020 y A-11; (3) PROJECT_STATE afirmaba `huso_operativa = Etc/GMT-2 por ADR-0012`, que es exactamente el fallo que ADR-0017 llama "el mas caro y el unico sin sintomas" -vale Europe/Madrid- y de paso llevaba 52 parametros cuando son 59. HUECOS DE PROCESO CERRADOS: el ritual documentaba `BOTSITO_ALLOW_MAIN=1` en el paso equivocado (la exige el commit `docs(state)`, no el merge: `git merge --no-ff` no dispara `pre-commit` y no hay `pre-merge-commit`); no habia regla para un hallazgo posterior al informe -ha pasado dos veces- y ahora la rama vuelve a WAITING_FOR_USER_VALIDATION en vez de cerrarse; el material que llega fuera de sesion tenia su procedimiento escrito UNA vez, dentro de una lista de lecciones tecnicas, y ahora vive en el README del feedback; `vistos.yaml` dice quien lo actualiza y cuando, y declara ABRIL -v5 ES el trader backtesteando abril y faltaba desde siempre-; y el MASTER_PLAN gana una tabla de QUIEN DECIDE QUE, porque la palabra "consultor" no aparecia ni una vez en el plan pese a ser quien mas decide. GUARDIA NUEVA: una ambiguedad RESUELTA tiene que tener un registro que la cierre apuntando A ELLA; A-20 no lo tenia -el suyo apuntaba al parametro, que basta para escribir el valor y no para cerrar la pregunta- y ninguna capa lo miraba. Ademas: PROJECT_STATE pierde las 318 lineas duplicadas que arrastraba desde a6fdcf1, ADR-0012 y ADR-0015 declaran en cabecera lo que ADR-0017 les revirtio, el indice de ADR marca las enmiendas, y el plan deja de prometer la TABLA DE DECISION que F12 descarto. SIN CERRAR, y son del consultor: que cuenta como ABRIR un holdout (y que se hace con la fuga del P&L de mayo), como se cierra una ambiguedad que decide el consultor y no el trader, y si el registro de feedback necesita `recibido_el` -hoy los registros se fechan el dia de la sesion aunque tres son del 10 y del 11-.
- 2026-09-12 · AUDITORIA DE CIERRE DE F12 (dos agentes, 57 hallazgos) APLICADA. Cuatro de severidad 1, y el primero es de negocio: `liquidez_tomada` (RN-004) y `estructura_m1` (RN-007) se FIJABAN SIN ESTAR DECLARADOS en `hechos:`, asi que la guardia -que iteraba los declarados- no los veia; la precondicion de los dos esquemas de entrada vivia solo en la prosa de `se_da_esquema`, o sea que UN MOTOR QUE LEYERA `forma` HABRIA ENTRADO SIN ESPERAR A QUE SE TOMARA LA LIQUIDEZ DE M15. Arreglado: el hecho se declara, `se_da_esquema` lo exige con `depende_de` -campo nuevo-, RN-007 pasa a la accion `agrupar_estructura` y la guardia denuncia los hechos usados y no declarados. Los otros tres: el `literal` de un predicado no se comparaba con NADA -se podia poner cualquier frase en boca del trader dentro del vocabulario, y el comentario de `comprobar_literales` habia predicho ese caso con esas palabras-; su `cita` podia no existir; y la `descripcion` de un parametro estaba fuera del hash siendo el unico sitio que define que significan las dos opciones de `lotaje_base` (reescribirla cambiaba el lote un 25 % sin mover `spec_version`). Severidad 2: `permite`/`prohibe` no se validaba contra nada en 11 de las 24 vigentes -seccion `efectos` nueva-; el cruce hecho-declarado casaba por SUBCADENA y BENDECIA UNA MENTIRA (`hechos.sesgo` decia que RN-003 lo consume, cuando lo produce, y corregirlo hacia fallar la guardia); `comprobar_precedencia` no miraba `forma` y RN-013 y RN-015 tenian el disparador ejecutable identico sin declarar `complementa`; `pendiente_definicion` admitia un `A-999` inexistente; y las dos comprobaciones que F12 estreno -`comprobar_consumo` y la de `forma` contra `parametros`- tenian agujeros propios. Del lado de documentacion, el mas caro: A-13 APUNTABA AL PARAMETRO EQUIVOCADO, asi que `spec status` ensenaba como "en revision" un valor CONFIRMED y ESCONDIA `break_even_criterio_ruptura`, uno de los dos unicos defaults vivos; y el glosario seguia diciendo, DENTRO DEL HASH, que el lote se calcula sobre la caja entera y que el stop se mueve despues. ADR-0014, 0015, 0016 y 0018 enmendados en cabecera sin reescribir lo que deciden. El brief afirmaba dos veces que la revision de diseno estaba PENDIENTE cuando se celebro el 2026-09-10. spec_version 8.2.0 -> 9.1.0. make check verde: 630 casos, 448 funciones.
- 2026-09-11 (4) · F12 COMPLETA, a la espera de validacion (informe `docs/validation/F12-spec-semantic-validator.md`). Cierra los tres puntos que faltaban del brief y encuentra dos defectos mas al hacerlo. (1) PARAMETROS SIN LECTOR: campo `consumido_por` en el registro -dentro del hash- y guardia `comprobar_consumo`: todo parametro CON VALOR lo nombra una regla vigente o declara quien lo leera (una funcionalidad con su fila en MASTER_PLAN H.2, o un ADR si es documental). Al encenderla saltaron DOCE y no nueve: los tres de mas eran el hallazgo, CUATRO REGLAS EJECUTABAN UN PARAMETRO QUE NO DECLARABAN -vivia en `forma` y no en `parametros`, que es la lista que leen las otras guardias, asi que RN-014 ejecutaba `break_even_criterio_ruptura` (DEFAULT_AMBIGUOUS bajo A-13) sin que la comprobacion de UNKNOWN lo viera-. Guardia nueva dentro de `comprobar_forma`. `broker_dst` y `broker_offset_base` pasan a RN-020 y `instrumento_digitos` a RN-026, porque esas reglas los consumen de verdad; los otros siete declaran dueno. DISCREPANCIA DELIBERADA CON EL BRIEF: proponia meter `modelo_llenado` en RN-011 y no se hizo -el modelo de llenado es del simulador, no de la estrategia, y meterlo en una regla habria hecho pasar por operativa del trader una decision del motor (ADR-0016)-; su hogar es F24/F27 por H.2:219. (2) `botsito spec check`: la capa semantica sola, sin las otras nueve delante, que es donde `knowledge validate` devolvia antes de llegar; comparten `problemas_de_spec` para que no puedan divergir. (3) Los `R-NN` dejan de ser posicionales: id explicito en `contexto_preguntas.yaml`, validado por el generador y atado al anexo del informe de la sesion 1 por un test de contrato. Ademas, `spec status` deja de llamar "a proposito" a todo parametro sin valor: lo comprueba contra los registros REJECT y separa lo rechazado de lo que falta preguntar. spec_version 8.1.0 -> 8.2.0.
- 2026-09-11 (3) · A-20 CERRADA POR EL TRADER, y la primera que se cierra FUERA de una sesion. Respuesta suya por escrito: "solo 1 zona control bro. si hay 2 se descarta". `zonas_control_max_por_esquema` deja de ser un default nuestro y pasa a CONFIRMED; el valor no cambia -era 1- pero ahora lo dice el trader y ratifica tambien el DESCARTE, no solo el numero. RN-009 deja de citar `ev-v4-001909-54ac2edd` -"por lo general solo buscamos uno", que es una TENDENCIA y era justo lo que A-20 preguntaba- y cita sus palabras, que si son una prohibicion. DEFECTO QUE ESTO DESTAPO en `feedback apply`, y es el caso mas comun de preguntar: `fuente_anterior` solo se rellenaba cuando la fuente previa era de tipo `feedback`, asi que un parametro DEFAULT_AMBIGUOUS -que por definicion cita evidencia- pasaba por no-op en cuanto el valor coincidia. Es decir: el trader ratifica lo que habiamos supuesto y el registro se queda diciendo que es un default nuestro, con la ambiguedad abierta. Arreglado y con test. La captura del mensaje entra al corpus (`Material adicional de su operativa/Mensajes del trader/`) para que el literal tenga fuente y no sea una sintesis del consultor. spec_version 8.0.0 -> 8.1.0; 50 parametros confirmados y 2 con default nuestro.
- 2026-09-11 (2) · EL LOTAJE SE DIMENSIONA HASTA EL STOP, NO SOBRE LA CAJA COMPLETA (ADR-0020). El consultor cierra el acuerdo final: el 0,5 % de riesgo se mide EN el nivel 0,8. `lotaje_base` pasa de `distancia_completa` a `hasta_stop_fraccion` por un registro de feedback que supersede al de la sesion 1 -cuyo literal decia justo lo contrario, "El lotaje se pone sobre la caja completa de SL"-, y la opcion deja de llamarse `desde_075`, que nombraba un 0,75 que A-10 habia cerrado en 0,8. Consecuencias reales: el lote SUBE UN 25 %, la perdida por operacion pasa de 0,4 % a 0,5 % del saldo y el tope diario del 4,5 % aguanta nueve perdidas en vez de once; el RR realizado NO cambia (3,75), porque las dos distancias se escalan igual. RN-012 se INVIERTE -decia "la perdida real es menor que el riesgo nominal, y es a proposito"- y `realizar_perdida` pierde el argumento `fraccion`, que ya no multiplica nada. El arrastre lo destaparon las guardias, no la lectura: RN-027 y el predicado `no_es_multiplo_de` se quedaron citando el registro que el acuerdo acababa de revocar, y la nota de RN-015 y la descripcion de `base_calculo_objetivo` afirmaban que el objetivo y el lote comparten distancia. LECCION: la guardia de citas revocadas ha nacido corta TRES veces -parametros (P13), reglas y glosario (RN-013), y ahora el vocabulario de F12, que tiene `cita` propia desde ADR-0019 y seguia fuera-; ahora es `comprobar_citas_revocadas`, con nombre y con un test que la dispara y otro que no. spec_version 7.0.0 -> 8.0.0.
- 2026-09-11 (1) · MATERIAL NUEVO: el trader entrega el BACKTEST DE MAYO 2026, el primero de los dos meses que se comprometio a mandar. Vive en `corpus/Estrategia del trader/Material adicional de su operativa/Backtest mayo 2026/` (fuera de git, inventariado con hash): exportacion xlsx de FXReplay, 7 capturas de Analytics y 2 de los mensajes de WhatsApp con los que lo entrego. Cifras de FX Replay: 68 operaciones, 18 ganadoras / 33 perdedoras / 17 en break even, win rate 35,29 %, RR medio 3,45 (maximo 4,47), profit factor 2,14 y +650 $ sobre 100 000 con lote fijo. DOS CAUTELAS: junio NO ha llegado, y 13 de los 19 dias de mayo son holdout-1/2/3, asi que este material NO puede elegir ningun parametro -es entrada de F14 y F26-. Y sus cifras de WhatsApp (21 %, 27,6 %, 28,2 %) salen EXACTAS de contar en cajas completas -18x3-33x1, 18x3-33x0,8 y 18x3,4-33x1-, que es la convencion VIEJA del lotaje: queda anotado en ADR-0020 como la pregunta que hay que ratificarle al trader, no como prueba de nada.
- 2026-09-10 (11) · VALIDACION DE LOS VIDEOS CONTRA LA SPEC (dos agentes, con el peso sobre v6 como pidio el consultor). Encontro TRES FALLOS EJECUTABLES en la forma que se escribio hoy, y los tres los dejaba pasar la guardia porque comprobaba la DECLARACION de los hechos y no lo que las formas hacen. (1) `operativa_detenida` declaraba `consume: [RN-001]` y RN-001 no lo leia: el tope diario del 4,5 %, el semanal y el corte por cartuchos prohibian abrir EN EL TICK DEL EVENTO y nada impedia abrir en el siguiente. (2) `operacion_abierta` declaraba producirse en RN-011 -que solo COLOCA la orden- asi que NADIE lo producia y RN-002 (cierre forzoso de las 15:00) y RN-014 (break even) eran INALCANZABLES. (3) `operaciones_abiertas` se invocaba como acumulador sin estar declarado. Arreglado: el freno unico se parte en `detenido_por_tope` y `detenido_por_cartuchos` -porque sus reinicios son distintos: el corte del dia y la siguiente liquidez de M15- los dos DURAN (quien los fija tambien los lee) y RN-001 es el gate maestro que los consulta; RN-013 produce `operacion_abierta` y apaga `orden_limite_pendiente` al llenarse la orden; y RN-018 usa un predicado en vez de un acumulador inventado. La guardia compara ahora declaracion contra realidad. spec_version 6.1.0 -> 7.0.0.
- 2026-09-10 (10) · CORRECCION: A-21 nacio mal. ADR-0019 afirmo que "el corpus nunca define que es un breaker" y marco RN-008 como pendiente_definicion; lo senala el consultor el mismo dia y tiene razon. Lo que se comprobo fue el GLOSARIO -circular- y UNA cita; lo que no se comprobo fue el corpus, y ahi esta la definicion repartida en una docena de items: ev-v4-000243 (los dos esquemas), ev-v3-004201 (el primero no espera retroceso, con el breaker basta), ev-v3-004230 (el segundo deja zona de control y luego rompe), ev-v3-011653 (el breaker marca el bloque de origen y NO se usa el CHoCH), ev-v4-005910 (en M1 vale mecha o cuerpo, en M15 cuerpo). Recogida en el glosario, que es donde faltaba: `breaker` deja de definirse a si mismo y nacen `primer esquema de entrada` y `segundo esquema de entrada`. RN-008 deja de estar pendiente y las 24 reglas son ejecutables sin asterisco. A-21 se REFORMULA a lo unico que sigue siendo cualitativo: que es una zona de control "limpia, sin ruido". LECCION: afirmar una AUSENCIA es una afirmacion como cualquier otra y exige buscarla en la FUENTE -las transcripciones, con `kb find`- y no en el indice. spec_version 6.0.0 -> 6.1.0.
- 2026-09-10 (9) · LAS 24 REGLAS VIGENTES YA TIENEN FORMA EJECUTABLE. Cierra la deuda del §8 del informe de F11 -'las reglas son prosa, nada garantiza que el motor implemente lo que dicen'-. Al escribir las veinte restantes, la guardia destapo un hueco de ADR-0019: las ACCIONES no son predicados y no tenian vocabulario propio; `cerrar_a_mercado`, `dimensionar_lote` o `abstenerse` no son condiciones que se evaluen. Seccion `acciones` nueva, y `comprobar_forma` valida cada rama contra su catalogo. Vocabulario final: 21 predicados, 12 acciones, 4 hechos con quien los produce y quien los consume, 3 acumuladores con base y reinicio. RN-008 queda VIGENTE -la prohibicion sigue en pie- pero con `pendiente_definicion: A-21`: el corpus NUNCA define que es un breaker, el glosario es circular y la cita dice 'el esquema de entrada QUE YA SABEMOS CUAL ES'. A-21 nueva y BLOQUEANTE para la sesion 2. Guardia nueva: una regla VIGENTE sin forma es un error. El hash cubre `forma` y las cuatro secciones. spec_version 5.0.0 -> 6.0.0.
- 2026-09-10 (8) · PILOTO DE LA FORMA EJECUTABLE (F12, ADR-0019): las cuatro reglas mas dificiles escritas en predicados con argumentos, y AGUANTAN. RN-003 (sujeto, referencia y criterio distintos sobre la misma primitiva `rompe`), RN-006 (ligadura: la zona recien completada es la misma a la que va el limite), RN-014 (ligadura + cuantificador: `distinta_de: OP.zona_de_entrada`, `posterior_a: OP.instante_entrada`) y RN-020 (dos acumuladores con base y reinicio propios). Tres secciones nuevas en strategy_spec.yaml -`predicados`, `hechos` y `acumuladores`- y NO un cuarto fichero, que habria roto el contrato del hash. Tres parametros nuevos que la forma obliga a crear porque un criterio a pelo seria un valor de negocio en un campo ejecutable: `sesgo_h4_criterio_ruptura` y `zona_control_criterio_completada` CONFIRMED, y `break_even_criterio_ruptura` DEFAULT_AMBIGUOUS bajo A-13 -que es justo lo que A-13 pregunta, y ademas destapa que `break_even_condicion` responde a OTRA pregunta: al tocar el nivel o al cierre, no con que se rompe la zona-. `comprobar_forma` valida vocabulario existente, argumentos declarados, argumentos de valor que llevan el NOMBRE y no el valor -el fallo que hundio la primera version de D1-, y hechos que alguien produce y alguien consume. El hash cubre `forma` y las tres secciones: sin eso, cambiar un predicado no moveria la version, que es el mismo fallo que P5 encontro con `notas` pero en el campo mas ejecutable de todos. spec_version 4.2.0 -> 5.0.0. 20 reglas vigentes siguen en prosa y `spec status` lo dice.
- 2026-09-10 (7) · A-11 RESPONDIDA por el trader: "el SL se pone junto a la orden limite, no cuando se apertura recien". Deja de ser la INFERENCIA que el barrido de fidelidad habia marcado en la descripcion del parametro -su literal anterior decia que hay dos stops y para que sirve cada uno, no cual viaja en la orden-. RN-011 cambia de sentido: la orden limite NACE con su stop, ya en stop_fraccion_caja, en vez de moverlo tras el llenado. Consecuencias para el motor: desaparece el evento 'mover el stop tras el llenado' que F22/F31 tendrian que implementar, y RN-026 debe comprobar instrumento_stops_level en el momento de COLOCAR la orden, no despues. Y un caso concreto deja de existir: un hueco de precio que atraviese la entrada NO puede saltar al stop de rango completo, porque ese nunca llega a estar vivo en el mercado. El corpus describe lo mismo desde el lado del resultado -'me activa la entrada y si yo protejo a 0.80', ev-v5-000312- y por eso parecia un movimiento posterior; queda escrito en las notas de RN-011 para que nadie lo lea como contradiccion. OJO: la frase es la del consultor REFIRIENDO la respuesta, no una transcripcion, y el registro de feedback lo dice asi en vez de hacerla pasar por cita textual. spec_version 4.1.0 -> 4.2.0.
- 2026-09-10 (6) · BARRIDO DE CABOS SUELTOS antes del piloto de F12. Lo hecho a mano se detecto primero con un script, no leyendo: las cifras de la spec pegadas a mano se habian quedado viejas TRES veces en dos dias (P8, P11, y una tercera que nacio desfasada porque spec_version subio dos veces mas antes del merge). Arreglo estructural y no cosmetico: el HANDOFF y el §6 del informe de F11 DEJAN DE PEGAR la salida de `spec status` y apuntan al comando; `knowledge/spec/README.md` sigue llevandola porque es el unico documento que describe el presente sin mezcla, y un test nuevo la vigila. El HANDOFF no entra en ese test a proposito: es una narracion con fechas -su seccion de F10 dice '24 parametros de estrategia en UNKNOWN', cierto entonces- y una guardia con falsos positivos se desactiva sola, que es la leccion de `comprobar_precedencia`. Ademas: la descripcion de `saldo_inicial_cuenta` era FALSA (decia 'base del lotaje y de los topes' y ninguna de las tres bases apunta a el); `spec status` cortaba el nombre mas largo del registro (29 caracteres en una columna de 28); `comprobar_decisiones` se saltaba las reglas DESCARTADAS, que tambien llevan `decision` en el hash; y el salto silencioso de `comprobar_literales` queda anotado como la trampa que sera cuando F12 meta predicados con cita propia.
- 2026-09-10 (5) · REVISION DE DISENO DE F12 (tres agentes) y los SIETE DEFECTOS VIVOS que encontro en la spec recien validada, arreglados en ADR-0018. Dos costaban dinero: (1) RN-006 no exigia que la orden siguiera pendiente y se disparaba sobre EL MISMO evento que RN-014, asi que con el orden del fichero ganaba a RN-014 y a RN-018 -reubicaba una limite en paralelo y NO ponia el break even-; (2) RN-019 (id 019) ganaba a RN-020 (020), o sea se reentraba despues de tocar el tope diario. Mas: la ventana no declaraba si a las 15:00 se abre (ahora es medio abierta, decision del consultor); `stop_fraccion_caja` y `stop_segundo_esquema` valian ambos 0.8 -dos puertas para el mismo numero, lo que RN-012 prohibe- y el segundo pasa a UNKNOWN a proposito (un unico esquema de stop, decision del consultor); RN-009 y RN-018 llevaban cardinalidades en prosa CON LA GUARDIA ESCRITA PARA NO VERLAS -su comentario declaraba que 'se abre una operacion' y 'los dos esquemas' eran espanol- y ahora son `zonas_control_max_por_esquema` (A-20, default nuestro: el literal dice 'por lo general solo buscamos uno') y `operaciones_simultaneas_max`; `dias_operables` era texto con 'lunes a viernes' usado como condicion ejecutable y pasa a enum; y RN-002 nombraba 'la hora del grafico' con parametros `huso_operativa` (resto de ADR-0017). DECISION D4: la precedencia va por CLASE -gate > terminal > disparador > fallback, tal como lo fija ADR-0018 y lo implementa CLASES_REGLA; esta entrada lo escribio al reves hasta el 2026-09-12- y no por orden del fichero, que es editorial (RN-026 y RN-027 son VIGENTES y viven bajo la cabecera 'reglas descartadas'); dos reglas de la misma clase con los mismos parametros son ERROR nombrando los dos ids. spec_version 3.0.1 -> 4.0.0. La revision tambien encontro tres errores de hecho en el brief de F12 y que 'un predicado hereda gratis las ocho guardias' es FALSO: pendiente reescribir el brief antes del piloto.
- 2026-09-10 (4) · F11 VALIDADA por el usuario y cerrada en main: merge --no-ff b62f4aa, tag stable/F11. Catorce puntos de auditoria cerrados (P1..P14; tabla viva en el §0 ter del informe), seis de ellos encontrados por las guardias nuevas en su primera ejecucion. Queda ABIERTO y anotado: A-13 y A-18 se miden, A-14 y A-11 se preguntan al trader, A-19 y instrumento_stops_level se verifican en la cuenta, y A-15/A-16/A-17 siguen ABIERTAS porque solo se cierran con feedback del trader -decidir si se permite cerrarlas por ADR sigue pendiente-. Siguiente: F12 spec-semantic-validator.
- 2026-09-10 (3) · BARRIDO DE FIDELIDAD de los 54 parametros contra el literal de su cita, pedido por el consultor antes de validar ("fiel a todo lo que tenemos en los videos siempre"). Es lo que la guardia de P4 hace con las reglas y el glosario y nadie hacia con el registro. P13: `cartuchos_reinicio` citaba `fb-...-dec10786`, REVOCADO por `fb-...-e3eedcaa` justamente por llevar una parafrasis del consultor en el campo del literal y decir 'dos perdidas' donde el trader remata 'seria 3 perdidas'. Y no era corregible: `apply` decidia si un parametro habia cambiado comparando VALORES, asi que una fuente muerta se quedaba para siempre -y el hash cubre la fuente justo para que quien mida fidelidad la distinga-. `es_no_op` compara ahora tambien la fuente y `knowledge validate` rechaza citar un registro revocado. P14, encontrado al arreglarlo: `apply` reescribia el `valor:` de los 30 parametros de la sesion para cambiar uno (42 lineas de diff para 2 de cambio real), que es el diff ilegible que `escribir_cambios` existe para evitar; ahora solo escribe lo que cambia. ANOTADO sin cerrar: `stop_en_orden_pendiente = en_la_orden` es una inferencia nuestra -su literal dice que hay dos stops y para que sirve cada uno, no cual viaja en la orden-; queda escrito en la descripcion del parametro y reabrir A-11 es decision del consultor. spec_version 3.0.0 -> 3.0.1.
- 2026-09-10 (2) · P12, el ultimo de la auditoria y el mas caro: **el reloj era civil, no un offset fijo**. El consultor lo cierra: el trader opera siempre a la misma hora SUYA, sea cual sea la fecha, y no hay configuracion deliberada de huso. `huso_operativa` vuelve a `Europe/Madrid` -ADR-0005 tenia razon y su enmienda del 2026-09-09 queda REVOCADA-, `ventana_inicio` y `ventana_fin` cuelgan de el, y `anclaje_h4` pasa a `17:00 America/New_York` = 00:00 de servidor, que es la convencion que ADR-0005 ya habia escrito. Con `Etc/GMT-2` el ancla caia a las 21:00 UTC TODO el invierno, una hora antes que la vela real, repartiendo mal todas las H4 -que es de donde sale el sesgo- sin dar ningun sintoma. Aparece ademas un efecto que nadie habia calculado: 28 dias al año (8-28 marzo, 25-31 octubre) la UE y EE.UU. no cambian la hora el mismo dia, la primera H4 se ve a las 22:00 y las sesiones del trader dejan de empezar en la apertura de una vela. DECIDIDO: manda su horario; RN-001 cambia de titulo, porque afirmaba una alineacion con H4 que no es cierta siempre. A-14 se reescribe con esa pregunta para ratificarla con el trader. spec_version 2.0.0 -> 3.0.0. ADR-0017.
- 2026-09-10 · F11 AUDITADA por el consultor antes de validar (once puntos, P1..P11; tabla viva en el informe). Cinco eran de negocio o de dato y ninguno lo veia ninguna guardia. (1) La base del 1:3 se contradecia entre la `unidad` de `objetivo_rr` y RN-015: un 25 % de distancia al TP dependia de cual leyera F18. Se decide la caja completa (ADR-0014) y la base sube a parametro, `base_calculo_objetivo`. (2) `huso_grafico` se afirmaba CONFIRMED con una cita que habla de la vela de las 23, no del reloj; TODAS las lecturas del repositorio son de verano y el trader ata el UTC+2 a Madrid (`ev-v3-000136`). Baja a DEFAULT_AMBIGUOUS bajo A-14, que se reescribe con la tercera opcion -el reloj del servidor- y con los cuatro parametros que dependen de ella. **CORRIGE la afirmacion de ADR-0012 y de la entrada del 2026-09-09 de que 'la sesion desmintio Europe/Madrid': no la desmintio** (ADR-0015). (3) El unico freno del dia no decia que es un dia: `reloj_dia_riesgo` nuevo (A-19) y `base_calculo_perdida_semanal` CONFIRMED en `saldo_actual`, que el trader habia dicho -"9% de la cuenta actual"- y no tenia donde guardarse. (4) La verificacion comprobaba `literal ⊆ cita` y nunca `regla ⊆ literal`: campo `decision` y guardia para las reglas construidas sobre parametros de entorno; RN-026 y RN-027 eran decisiones del consultor presentadas como palabra del trader (ADR-0016). (5) El hash no cubria `titulo`, `literal` ni `notas`, asi que la correccion de riesgo de RN-020 se podia borrar sin mover la version; y el titulo de RN-020 decia lo contrario que sus notas. Ademas: `feedback apply` desplazaba comentarios de bloque (dos cabeceras acabaron dentro de `anclaje_h4` y `lotaje_base`), `kit check` degradaba a AVISO hasta `particiones.yaml`, `spec manifest --escribir` nunca actualizaba `generado_el`, `spec status` dejo de cuadrar al aparecer los primeros DEFAULT_AMBIGUOUS, y MASTER_PLAN daba a F21 el criterio pre-sesion `stop = -0,75 R`. spec_version 1.4.1 -> 2.0.0. ADR-0014, ADR-0015, ADR-0016. A-18 y A-19 nuevas.
- 2026-09-09 · F11 CONSTRUIDA (rama `feature/F11-strategy-spec-schema`): brief revisado por agente (13 bloqueantes, 10 importantes, 8 menores; 24 decisiones cerradas antes de programar, cuatro de ellas del consultor). `feedback apply` que NO interpreta: en su primer uso real fallo nueve veces y cada fallo era un problema (tres horas sin huso, dos categorias que prohiben escribir por feedback, dos 'no aplica' y un 'sin limite' que no son numeros, dos registros vigentes sobre el mismo parametro). Campo `valor_canonico` en el feedback (opcional: los 72 registros previos conservan su id) y 35 registros del consultor que superseden, con el literal del trader intacto con el literal intacto. Registro: cinco tipos nuevos (enum con opciones, booleano, puntos, minutos, lotes), 42 parametros con 36 CONFIRMED y 6 UNKNOWN a proposito, categorias corregidas, `huso_grafico` = Etc/GMT-2 y `huso_operativa` alineado por ADR-0012 (la sesion desmintio Europe/Madrid). strategy_spec.yaml con 25 reglas (22 vigentes, 3 descartadas con su cita) que nombran parametros y no pueden llevar cifras; glosario de 9 terminos; spec_manifest 1.0.1 con hash sobre los TRES ficheros, estructura y no bytes. `spec status` y `spec manifest`. ADR-0012, ADR-0013. Tests: el que afirmaba 'ningun valor de estrategia' se invierte a 'todo valor de estrategia cita al trader'; literales prohibidos actualizados a los valores reales de la sesion. Informe WAITING_FOR_USER_VALIDATION.
- 2026-09-09 · SESION 1 VALIDADA por el usuario (acepto los 12 items de evidencia de v6). merge --no-ff a main (1475956); tag stable/F10-sesion-01. A-13..A-17 registradas. Siguiente: F11 strategy-spec-schema.
- 2026-09-09 · SESION 1 CON EL TRADER (2 h 27 min, video v6, paquete `2026-09-09-sesion-01`). El paquete se movio del 15 al 9 con `scripts/mover_sesion.py` (mismo seed, mismos 40 casos) y se commiteo ANTES de la sesion. Material: v6 inventariado, transcrito (tr-v6-...-7718b3f4, 2146 segmentos) y con fotogramas (fr-v6-22982c02, 8824), y la hoja de Word RELLENADA guardada en el corpus. 72 registros de feedback: 41 de la hoja, 5 aclaraciones del consultor y 26 con la voz del trader (minuto y cita). Las doce ambiguedades A-1..A-12 RESUELTAS, incluidas las tres bloqueantes: cartuchos 3 intentos (break even, entrada invalidada y reentrada no cuentan), break even al TOCAR, y anclaje H4 a las 23:00 de su grafico (UTC+2), verificado tambien en pantalla en fr-v6-22982c02/3585000. El stop queda en 0,8 FIJO de la caja con el lotaje sobre la caja completa (riesgo real 0,4 %), objetivo 1:3 sin extension, sin parciales, lunes a viernes, freno del dia por 3 perdidas y no por porcentaje. Correcciones del trader a lo que dabamos por sabido: NO deja de operar con el primer trade positivo, vuelve tras TRES perdidas, y no grabara su pantalla cada dia (pasara resumenes de backtest, lo que cambia la entrada de F26). Dos tramos de v6 declarados NO citables (0:41:00-0:50:11, acordado en voz que no va para la operativa; 1:53:30-1:57:31, video ajeno mientras el trader se ausenta) con guardia real en `evidence propose --check` y `evidence new`. Cinco propuestas de evidencia de v6 selladas (12 items) para las cinco dudas nuevas, pendientes de decision. Tests que afirmaban un estado ya superado, actualizados: feedback real vacio y corpus de cinco videos.
- 2026-09-08 · `scripts/mover_sesion.py`: mover la fecha de una sesion del kit en una sola orden. El id del paquete lleva la fecha dentro y el registro de feedback exige que la fecha de cada respuesta sea la de su sesion, asi que si la reunion se mueve el paquete hay que rehacerlo. Hacerlo a mano tiene una trampa: `kit build` pide el seed, y con otro seed salen dias distintos sin aviso. El script lo lee del paquete existente, comprueba despues que casos, reparto y preguntas son identicos, restaura el original si algo falla y se niega a mover una sesion que ya tenga registros de feedback. Tres tests (identidad al mover y al volver, negativa con LABEL_CASE, restauracion tras fallo).
- 2026-09-08 · Auditoria de codigo previa a la sesion 1, con dos agentes (generador de la hoja y kit; bugs latentes en todo el arbol). Bloqueantes de contenido en la hoja: la nota de una confirmacion rapida remitia a una pregunta `E-06` que ya no existia, y una linea del cierre imprimia `paquete <sesion>` sin sustituir. Bugs reales de codigo: (1) `kappa.etiquetas_de_registros` aplicaba `activos()` sobre los `LABEL_CASE` ya filtrados, asi que una etiqueta retirada con `BORDERLINE` o `MARK_FALSE_*` reaparecia viva y contaba en el kappa; (2) `validar_contra_contexto` no detectaba dos registros que superseden al MISMO registro, que deja dos activos contradictorios y solo asoma semanas despues al calcular el kappa. Endurecido ademas: `leer_yaml` centraliza la decodificacion (un .yaml guardado en cp1252 o UTF-16 sale como error de dominio, no como traceback; 16 cargadores migrados); `desktop.ini`, `Thumbs.db`, `.DS_Store` y `.gitkeep` dejan de invalidar knowledge/ (los crean solos Explorer y la sincronizacion de Drive); `_numero` acota los decimales del registro y explica `0,75` y `1%` en vez de ensenar las internals de `decimal`; `VelaInvalidaError` capturada en `kit build` y en la CLI; `cargar_manifiesto` del corpus ya no queda sombreado por el de datos en `knowledge validate`; el duplicado de feedback distingue mismo contenido de colision. Generador de la hoja: numeros de pregunta y bloqueantes derivados del paquete (los renumera `kit build`), la rejilla H4 se presenta como suposicion a confirmar, la ventana local se explica como grafico y no como horario de operativa, errores legibles en vez de traceback, saltos de linea que ya no pegan palabras, y un test de contrato nuevo (`test_hoja_sesion_docx`, 13 casos: OOXML valido, citas del paquete intactas, cada pregunta con caja, sin fuga de holdout).
- 2026-09-08 · Auditoria previa a la sesion 1 (rama `feature/F10-hoja-sesion-docx`): una simulacion del registro posterior a la sesion (18 respuestas representativas de la hoja contra `feedback new` sobre una copia del repo) descubrio que 7 de ellas NO se podian registrar porque no habia objeto al que apuntar. Arreglado: 6 parametros de negocio nuevos en el registro en UNKNOWN (`dias_operables`, `filtro_noticias`, `spread_maximo`, `perdida_maxima_diaria`, `perdida_maxima_semanal`, `comportamiento_sin_regla`) mas `instrumento` y `cuenta_objetivo`, con su fila en `mapa_parametros.yaml` y su contexto; tipo de objetivo `paquete` en F09 (CONFIRM/REJECT) para la precondicion de ceguera, que antes solo quedaba en el video, con la guardia de que el paquete confirmado sea el de la propia sesion; el test del registro exige la fuente por decision al VALOR y no al hueco UNKNOWN; el generador de la hoja comprueba antes de escribir que toda pregunta declarada tenga objetivo resoluble (`comprobar_objetivos`). Cuestionario del paquete regenerado: 21 -> 27 preguntas (mismo seed, mismas ventanas y particiones). Simulacion repetida: 21 de 21 registrables. ADR-0011 y `vistos.yaml` actualizados.
- 2026-09-08 · Hoja de respuestas de la sesion 1 en Word (rama `feature/F10-hoja-sesion-docx`): contexto humano de cada pregunta como dato versionado (`contexto_preguntas.yaml`, con acentos porque lo lee el trader) y generador `.docx` sin dependencias (OOXML a mano) con la confirmacion previa, las 21 preguntas con sus citas y caja de respuesta, y la tabla de etiquetado de los 16 casos dev; el binario queda fuera de git y declarado en la guardia de rutas ignoradas.
- 2026-09-08 · F10 VALIDADA por el usuario. merge --no-ff a main (4f8277e); tag stable/F10. Kit de la sesion 1 listo (paquete `2026-09-15-sesion-01`, fecha provisional). Siguiente: sesion 1 con el trader y despues F11.
- 2026-09-08 · F10 abierta y construida (rama `feature/F10-elicitation-kit`): brief con revision de diseno de agente (3 bloqueantes: julio y agosto ya vistos por el trader -> meses limpios 2026-05/06 descargados y confirmacion escrita previa; cifras de negocio del kit como datos en `knowledge/cases/kit/config.yaml`; etiqueta por sesion H4 con gramatica; 9 importantes y 6 menores aceptados); ADR-0011; `knowledge/spec/ambiguedades.yaml` (A-1..A-12 legibles por maquina, validadas contra evidencia y registro; test anti-deriva con esta tabla); registro pre-poblado con 23 parametros de estrategia mas en UNKNOWN (24 con `anclaje_h4`); paquete `cases` (ambiguedades, cuestionario con casos `ev-*`, ventanas de dias no vistos con hash y limites H4 por anclaje, particiones por hash con seed, kappa de Cohen desde los `LABEL_CASE`, paquete determinista); CLI `kit build|check|kappa`; `knowledge validate` capa kit (guardia de ancestro: particiones antes del primer LABEL_CASE); feedback valida `ambiguedad` contra el fichero y `t1` contra la duracion; grabaciones de sesion como videos sin `drive_id`. Paquete real `knowledge/cases/kit/2026-09-15-sesion-01/` (seed 20260915: 21 preguntas, 40 casos de un universo de 42 dias de mayo y junio de 2026 descargados hoy, 16 dev + 8 + 8 + 8); auditoria de cierre de codigo aplicada (asignacion inmutable tras el etiquetado, esquema estricto del paquete, huso validado, escritura atomica, build valida ambiguedades y usa items activos, mes anterior contiguo para el primer dia). Informe WAITING_FOR_USER_VALIDATION.
- 2026-09-08 · F08 VALIDADA por el usuario (confirmo el cierre tras la auditoria). merge --no-ff a main (5d8cf3c); tag stable/F08. FASE 1 CERRADA (F03-F08). Siguiente: abrir F10 elicitation-kit.
- 2026-09-08 · F08 abierta y construida (rama `feature/F08-evidence-retrieval`): brief con revision de diseno de agente (3 bloqueantes, 9 importantes, 9 menores aceptados: token de busqueda con acentos plegados y numeros normalizados, `buscar_secuencia` en vez de `localizar_cita` para la frase, `no_consta` fuera, capa `retrieval` entre `spec` y `feedback`, `dudas_de`/`cargar_capas` en `corpus`, `referencia_en` unica, rutas relativas, golden con y sin `data/`, fixture a mano, esquema JSON); ADR-0010 (+ enmiendas en ADR-0006 y ADR-0009); paquete `retrieval` y CLI `kb find | at`; golden de 15 consultas de referencia en verde (15/15 devuelven su item; `1:3` solo por la afirmacion: fallo lexico del ASR); `kb find` 1,04 s de pared. Auditoria de cierre aplicada (codigo: `--frase` acotada a 3 segmentos y buscando en cruda y corregida, `[corregida]` solo si difiere, `--margen-s inf` sin traceback, `dudas` no enteras ignoradas, `--frase`+`--prefijo` y `--tema`+`--solo cruda` son error, `--tema` contra `_temas.yaml`, `t0` real en contradicciones y fotograma, corregida ilegible = aviso, tests de supersede/carpeta fuera/determinismo de la CLI; docs: HANDOFF, MASTER_PLAN Change Log, deuda F04 iii cerrada, Next Feature F10). Informe WAITING_FOR_USER_VALIDATION.
- 2026-09-07 · F07 VALIDADA por el usuario (acepto los 341 items sin modificaciones, `fotograma visto` en los 7 de pantalla/ambas, recall humano de V4 0:05-0:15 sin faltas, tag `stable/F07`, golden H4 a F10; confirmo el cierre tras la auditoria). merge --no-ff a main (f0c280b); tag stable/F07. Siguiente: abrir F08 evidence-retrieval.
- 2026-09-07 · F07 ronda 2: el usuario acepto los 341 items sin modificaciones (7 de pantalla/ambas con `fotograma visto`; recall humano de V4 0:05-0:15: ninguna frase faltaba; tag `stable/F07`; golden H4 sobre F15 pasa a F10). `evidence accept` x341 (0 fallos; `revisado_por` "Aleks · hoja F07 2026-09-07 · cruda leida|fotograma visto"), evidencia commiteada (ff13e7a), 20 propuestas con decision (0 pendientes), `_contradicciones.yaml` regenerado (1 abierta: `stop.nivel` 0,75 vs 0,8 = A-10), golden `test_golden_citas_f07` 40/40 en verde, hechos y ambiguedades A-1..A-12 con ids de evidencia. Auditoria de cierre (2 agentes) aplicada: docs (HANDOFF, PROJECT_STATE, MASTER_PLAN filas H/H.2/tabla A y B, ADR-0009 en el indice, deuda de F07 cerrada o con dueno, hook local reinstalado con `make hooks`) y codigo/tests (1 bloqueante: `test_directorio_real_valida` sin contexto rompia con los 7 items de pantalla; localizacion que prueba todas las apariciones de la frase; `hueco_ms` con aviso a partir de 15 s (41 items aceptados lo superan, maximo 44 s); palabras parciales al final del segmento alineadas (1 item); sello ampliado a la cabecera y 20 propuestas re-selladas; `validate` cruza cada decision con la evidencia; `accept` atomico y sin manifiesto; cabecera invalida sin traceback; audio no admite `fotograma_visto`; 8 tests nuevos). 311 funciones / 456 casos. Informe WAITING_FOR_USER_VALIDATION (ronda 2: confirmacion de cierre).
- 2026-09-06 · F07 ronda 1 construida (rama `feature/F07-evidence-extraction`; brief con revision de diseno de agente: 6 bloqueantes aplicados, entre ellos `evidence` sin importar `corpus`, comodin `[...]` en vez de la elipsis del ASR, tiempo real por `palabras`, `material_adicional` solo desde un tramo de video, `revisado_por` con metodo, sello `salida_sha256`): verificacion mecanica de citas (tokens, TOL 2 s), campo `transcripcion`, referencias `fr-*` obligatorias en pantalla, contexto compuesto en `validation`, propuestas trazables con guardias de calidad, CLI `propose|--check|accept|reject|list`, `_temas.yaml`, `PROMPT.md`, ADR-0009, golden cerrado (40 referencias) y contrato; 20 propuestas para los 5 videos (341 items, 91 `no_consta`, 42 marcas heredadas re-citadas) con `--check` en verde; hoja de revision HTML por script. Medicion V4 0:05-0:15: 7 referencias cerradas, 7 cubiertas, 22 items, todos en verde; recall humano en la ronda 2. Ningun item escrito en `knowledge/evidence/`. Informe WAITING_FOR_USER_VALIDATION (ronda 1).
- 2026-09-06 · PREVIOS DE F07 VALIDADOS por el usuario (ratifico las 4 decisiones: hotwords descartado, 6 sustituciones de segmento, Drive completo con drive_id de v5, tag stable/F05-previos-F07 con §F ampliado). merge --no-ff a main (8cba5c5); tag stable/F05-previos-F07. Siguiente: abrir F07.
- 2026-09-06 · PREVIOS DE F07 construidos (rama `feature/F07-previos`, commits b9ffd0d, 13b4e40, 627d90d): glosario v2 aprobado por el usuario (29 terminos, 6 globales + 6 de segmento sobre los ids nuevos); huella de reanudacion sin GPU/driver; guardia de 223 tokens del prompt; `hotwords` MEDIDO y DESCARTADO (sobre v5 alargo los segmentos hasta 40 s, la pasada oficial perdio ~10 s con "protejo a 0.80, SL por defecto" y transcribio "sell" como "SL" en 2 de 2 pasadas; `initial_prompt` no mostro nada de eso; ADR-0007 enmienda); los 5 videos retranscritos (~1 h de GPU; ids `bbd8a931`, `28391c2c`, `270a4851`, `a8d1bccc`, `3c6fbb57`; contenido conservado: ratio de palabras 0,958-1,000, hechos clave presentes, senales comparables); Drive: carpeta `1zYZjUAYMoine0RILKg2ZJyzcLz5-1p-R` con SHA256SUMS/LEEME/manifiestos por API; crudas, WAV y v5 en `data/drive_staging/` pendientes del usuario. Auditoria de cierre (2 agentes) aplicada: recuento del prompt como el motor (96, no 99; `add_special_tokens=False`), `initial_prompt_tokens` fuera de la huella, guardia antes de cargar la GPU, tests de `_carpeta_base_registrada_ajena`, anexos de la medicion en `docs/validation/anexos/F07-previos/`, tag `stable/F05-previos-F07` y §F ampliado. Informe WAITING_FOR_USER_VALIDATION. 2026-09-06: el usuario subio los 21 ficheros de `drive_staging/` a Drive (verificado por API) y valido las 4 decisiones; `drive_id` de v5 anotado.
- 2026-09-06 · AUDITORIA GLOBAL VALIDADA por el usuario (ratifico las tres: regla del HANDOFF en la rama y nunca en main tras el tag; cierre de la auditoria como rama con tag `stable/F05-auditoria-1`; orden de los previos de F07: glosario v2 -> retranscribir 5 videos -> copia de crudas y WAV en Drive -> v5 en Drive -> abrir F07). merge --no-ff a main (916d0d0); tag stable/F05-auditoria-1.
- 2026-09-05 · AUDITORIA GLOBAL de la estructura (rama `feature/F05-auditoria-estructura`, 2 agentes) aplicada: codigo (`corpus/trabajo.py` con las guardias de F05 tambien en `corpus transcribe`: sin ella retranscribir en un clon sin `data/` pisaba la cruda; una transcripcion activa por video; `parse_ms` estricto; glosario rechaza `.` sin escapar; WAV/YAML corruptos y `corpus check` sin `fichero` ya no dan traceback; `carpeta_datos` unica; `--margen-s` negativo; `TOLERANCIA_DURACION_S` unica; mensaje de `state check` con el ritual) y docs/proceso (regla del HANDOFF en la rama, incidente de CI registrado, fila H.2 "Previos y entradas de F07", 5 videos, fotogramas en §0/B/ADR-0001/READMEs, lineamientos separados de hechos, Change Logs ordenados, `ci.yml` sin cancelar en main, test de rutas de Important Files). 389 casos, make check verde. Informe `docs/validation/AUDITORIA-2026-09-05-estructura.md`.
- 2026-09-05 · Incidente de CI en main: el commit `docs(handoff)` f452e6f (tras `stable/F05`) puso `state check` y la CI en rojo (run 34000376588) porque en main solo puede cambiar PROJECT_STATE.md tras el tag; revertido en de42ec1 (run 34000499649 verde). El `docs(state)` c97273f quedo cancelado por `cancel-in-progress` (run 34000351246) y su `make check` es local. El `docs(handoff)` de F04 (3b754f1) tambien estaba en rojo (run 33988126976) sin registro: main estuvo en rojo del 2026-09-05 19:46Z al 2026-09-06 00:08Z. Regla escrita en MASTER_PLAN §F: el HANDOFF se actualiza en la rama. Rama `feature/F05-auditoria-estructura` abierta a peticion del usuario para una auditoria global antes de F07.
- 2026-09-05 · F05 VALIDADA por el usuario (acepto las cuatro decisiones: cobertura completa a 1 fps sin perdida, Excel y ficha de Word hacia F07 y F10, sin copia de fotogramas en Drive, candidatos A-9 hacia F07). merge --no-ff a main (dd8de55); tag stable/F05. Pregunta del usuario respondida: las decisiones y la lista de obligatorios son modificables; los manifiestos no se editan, se reemplazan.
- 2026-09-05 · Material adicional del usuario ("Info extra de backtesting") integrado en el corpus por su instruccion antes de validar F05: v5 (`2026-09-05 21-03-59.mkv`, 365 s, FXReplay abril; transcrito `tr-v5-...-01a1ae03`, 99 segmentos; fotogramas `fr-v5-718ecabb`, 366), xlsx abril 2026 (38 operaciones) y 6 capturas de Analytics como `material_adicional`; `fuentes.yaml` y `manifest.yaml` (5 videos); hechos en Lineamientos (0,8 "SL por defecto", reentrada tras equal, RR sobre 1 %, 1:3 con 1:4 futuro, backtest abril 47 %/PF 4,01). Deuda: subir v5 a Drive.
- 2026-09-05 · F05 construida (ADR-0008): brief con revision de diseno por agente (7 bloqueantes aplicados: `fps=1` elegia el fotograma en n+0,47 s y reescribia el `pts`; `huecos` vacuo; referencias heredadas citables; "cinco obligatorios"; salidas incompletas; test AST inviable) y decision del usuario (maxima fidelidad sin restriccion de recursos: cobertura completa a 1 fps en PNG sin perdida, cambio de la tabla A). Cuatro videos extraidos (16 182 fotogramas, 8,9 GiB, ~11 min, `huecos: []`), determinismo 80/80 por `-ss -copyts`, obligatorios legibles (Excel 2,83/3,3; 4,08/3,94; 1,19537), candidatos A-9 y ficha de reglas en Word (V3 0:01:41) como hechos para F07. Informe WAITING_FOR_USER_VALIDATION. Auditoria de cierre (2 agentes) aplicada: A1 carpeta de trabajo decidida tambien por los manifiestos (otra build/maquina ya no es callejon sin salida), A2 `segundos_ausentes_ms` (referencias solo a fotogramas que existen; sin el campo, cobertura densa obligatoria), A3 `start_time != 0` rechazado, YAML estricto en guardias, `show` acotado por duracion; docs: resolucion v4, 8,9 GiB, Change Regimes con corpus/fotogramas, brief anotado, READMEs. CI rama: run 33992054088 verde (pre-auditoria) y run 33992911952 verde sobre a118352 (cierre).
- 2026-09-05 · F04 VALIDADA por el usuario (decisiones: A-12 queda como pregunta al trader; glosario v2 como paso previo a F07 con retranscripcion de los 4 videos; constantes de corte tecnicas; lo heredado de Whisper tiny no se cita). Commit de docs de la auditoria final reescrito con trailer `Fuente: ADR-0005` (tocaba knowledge/spec/README.md; CI lo detecto: run 33985993346 rojo, 33986995223 verde). merge --no-ff a main (a7f8b4b); tag stable/F04
- 2026-09-05 · AUDITORIA FINAL previa a validar F04 (2 agentes: bugs de codigo y estructura del plan). Codigo: `sha256_video` entra en la huella de la carpeta de trabajo (un video cambiado ya no reescribe el WAV ni falla tras la GPU con "motor no determinista"), cita de un instante en el borde exacto de un segmento, comodines cuantificados (`\\w+`, `\\d+`) rechazados en el glosario, `glossary apply --video` con video inexistente es error, temporal del manifiesto con prefijo `_` (no rompe `check` si queda huerfano), borde de fragmento con 1 ms de redondeo no cuenta como recorte, `cargar_todos` detecta ids repetidos y ciclos, asercion vacia de un test corregida. Docs: regimenes de cambio completos (manifiestos de datos y transcripciones), deuda tecnica de F04 con dueno (huella GPU, initial_prompt, palabras bajo corregida, hallazgo V4 1:28:20, fotogramas obligatorios de F05), regla de cita de F07 contra la cruda y secuencia glosario v2 -> retranscribir -> Drive -> F07, F05 depende de F04, plantillas de brief e informe con revision de diseno, auditoria de cierre y decisiones del usuario, MASTER_PLAN §F con el metodo supervisado, A-1..A-12, 33 marcas, Change Log del plan al dia; HANDOFF y READMEs alineados
- 2026-09-05 · F04 construida y auditada: cuatro videos transcritos con large-v3 (403 + 854 + 1031 + 1645 segmentos, cero cortes forzados, cero recortes), manifiestos inmutables tr-v1-...-00fcaf53, tr-v2-...-ac6b337b, tr-v3-...-570a315f, tr-v4-...-3f8c826e; determinismo verificado retranscribiendo un fragmento; 33 marcas heredadas revisadas (28 coinciden, 3 eran fotogramas, 2 con cifra distinta: 40/50 % y 2,3/2.83); auditoria de cierre sin agentes (limite de sesion) con 5 correcciones; hook sin resync; informe WAITING_FOR_USER_VALIDATION. CI verde: 3f73813 (run 33946879078), d1f3947 (33948083299), 69ea773 (33966530552)
- 2026-09-05 · AUDITORIA GENERAL de F04 (2 agentes: codigo/tests y docs/proceso) aplicada en la misma rama. Codigo: solape de milisegundos entre segmentos de Whisper se recorta y cuenta (antes abortaba tras la GPU), palabra con fin < inicio se iguala, reemplazo del glosario LITERAL (no plantilla de re.sub), alternancias envueltas en limites de palabra, nombre de motor validado antes de trabajar, `--reemplaza-a` comprobado antes de la GPU y del mismo video, manifiesto escrito atomicamente y con `reemplaza_a` inmutable, esquema del manifiesto valida fragmentos contiguos, duraciones, senales, huecos y cortes forzados, `comprobar` recomputa ms_con_habla/senales/huecos desde la cruda, carpeta por huella (`<motor>-<huella8>`) para retranscribir sin pisar la cruda anterior, WAV reextraido si cambia el video, sha256 del video por bloques, errores de CLI sin traceback, tests que no probaban lo que decian corregidos, ffmpeg obligatorio en CI. Docs: PROJECT_STATE (waiting, componentes, ADR-0007, A-12, deuda), READMEs de knowledge/scripts/hooks, MASTER_PLAN (tabla B, H.2 F07), brief y informe coherentes (33 marcas, margen 75 s), notas en ADR-0003/0005.
- 2026-09-05 · F04 en construccion: brief revisado por agente (8 hallazgos de fondo aceptados: muestras enteras, corte con min/max y forzados, glosario Unicode de dos alcances, manifiesto inmutable por transcripcion, corregida por recomputo, data/ para lo pesado, VAD y senales, vocabulario como initial_prompt); ADR-0007; faster-whisper large-v3 en la GTX 1650 a 3,6x tiempo real (grupo de dependencias `asr`); pipeline reanudable con motor falso testeado de extremo a extremo
- 2026-09-05 · ramas feature/F01-F15 fusionadas borradas (local y origin); rama feature/F04-transcription-pipeline abierta
- 2026-09-05 · cuenta demo FundedNext conectada en el MT5 de esta maquina; lectura de solo consulta: reloj de servidor GMT+3 con cierre 17:00 NY (decision 2 de F15 verificada en el broker real), escala 100000, M1 del 2026-07-02 coincide con Dukascopy a 1-2 puntos, parametros de instrumento/broker anotados en Technical Debt para F11/F33
- 2026-09-05 · MT5 instalado en la maquina de desarrollo (terminal build 6180, demo MetaQuotes conectada); lectura de solo consulta confirma escala 100000 y reloj de servidor GMT+3 con cierre a las 17:00 NY (decision 2 de F15 verificada en MetaQuotes-Demo; FundedNext pendiente). El adaptador MT5 (F17/F33) puede desarrollarse aqui
- 2026-09-04 · F15 VALIDADA por el usuario (con auditoria de arquitectura y de proceso previas); merge --no-ff a main (11ee1ac); tag stable/F15
- 2026-09-04 · F15 auditoria de arquitectura (agente) antes de fusionar: ADR-0006 (contrato de capas revisado para F25/F26/F30/F32, paquete comun con yaml_estricto/historial/documentos/ids/husos, accesores del registro por tipo declarado, SerieVelas.origen + ventana por instante + agregar_serie, validador de knowledge fuera del CLI, test AST sin float/Decimal en domain, test de accesores del registro); auditoria de proceso (agente): ritual de cierre reescrito con el orden real, cifras del informe corregidas, seccion "que debe decidir el usuario". 324 casos, 210 funciones
- 2026-09-04 · F15: auditoria de cierre aplicada (2 agentes), tres datasets reales congelados (ene/jul/ago 2026: 30150/32774/30257 velas M1) con manifiestos inmutables; H4 real del 2026-07-02 = goldens; CI verde (runs 33917006801, 33918894784); WAITING_FOR_USER_VALIDATION
- 2026-09-04 · REVISION GLOBAL de alineacion con las 8 fases (tras F15): sin bloqueos hacia F04-F33. Verificado: contrato de capas admite engine->data/domain, spec->config, cases->data; domain/velas.py sin float/Decimal (F18); tipos del registro y papeles del corpus ampliables sin romper (F10/F11); commits_sin_fuente listo para F11; cargar_serie con ventana para F14; regla de anclaje escrita en ADR-0005 para exportar en F29; ritual de merge/tag coincide con git log; main cumple state check. Pendientes conocidos: retirar en F11/sesion 1 los tests que afirman registro sin valores y feedback vacio; borrar ramas feature/F01-F09 fusionadas (decision del usuario); reloj de servidor aproximado hasta F17
- 2026-09-04 · F15 construida con revision de diseno previa por agente (brief corregido: sin velas de 3/5 h en datos reales, Vela en domain sin Decimal, huso_datos fuera del registro, id de dataset por hash, velas de borde `completa`); domain/velas, data/{velas,agregacion,dukascopy,dataset}, CLI data, 16 fixtures reales bi5, goldens H4 del 2026-07-02, hook y validate sobre data/manifests; ADR-0005; parametros huso_operativa (CONFIRMED) y anclaje_h4 (UNKNOWN, A-9)
- 2026-09-04 · rama feature/F15-market-data-ohlc abierta; brief y ADR-0005 (fuente Dukascopy M1 publica, precios enteros en puntos, tres relojes, anclaje por reloj de pared)
- 2026-09-04 · F09 VALIDADA por el usuario; merge --no-ff a main (2ff6450); tag stable/F09; proteccion de rama main activada en GitHub (enforce_admins, sin force-push ni borrado)
- 2026-09-04 · push de la auditoria de cierre (e99afba, con trailer Fuente: ADR-0002, ADR-0004 por tocar el comentario de parametros.yaml); CI Ubuntu verde (run 33912550454); Python 3.12 en local y CI
- 2026-09-04 · AUDITORIA DE CIERRE de F09 (3 agentes: codigo, plan/docs, infraestructura), antes de la validacion del usuario. Corregido: campos en blanco rompian el id de feedback/evidencia; `Fuente: ADR-9999` pasaba; detector de literales de negocio eludible; KeyError con `--sesion ""`; `feedback new`/`evidence new` validan contexto antes de escribir; fechas imposibles y digitos Unicode; supersede cruzado y ciclos; ficheros no-yaml; tracebacks con manifiesto/TOML/YAML corruptos; ancla por SHA con tag vigilado; clon superficial y repo anidado no evaluables; registro estricto (texto vacio, claves ajenas, limites en hora); instalador de hooks (worktree, hooksPath global, .bak, git ausente); hook con `uv run --locked`; `.python-version` 3.12; CI con permisos, concurrencia, timeout y ffprobe obligatorio; tests de integridad no eludibles; `feedback pending` filtra por `estrategia` (ADR-0004); docs coherentes (ejemplo del informe, H.2 anclaje H4, mapa de ambiguedades, READMEs). Un agente ejecuto por error una prueba en el repo real (rama `prueba/soft`, creada y borrada; solo quedan entradas de reflog)
- 2026-09-04 · push de la auditoria extrema (8 commits); CI Ubuntu verde (run 33909186793, d217a11); clon sin tags OK por ancla SHA, clon superficial ERROR explicito
- 2026-09-04 · AUDITORIA EXTREMA (3 agentes: codigo, plan/ejecucion, repositorio). Corregido: git decodificado en UTF-8 con quotepath=false (un commit con mayuscula acentuada anulaba la guardia de trailers en Windows); adiciones en commits de merge protegidas (`git log -m`); video_id y formato de id validados, `evidence new` contra fuentes.yaml; hook con rutas sin entrecomillar y tabulador; cargador YAML estricto (claves duplicadas, fechas como texto, tipos texto exigidos); InvalidOperation/NaN/Infinity/25:99 rechazados; guardias no evaluables son ERROR y el ancla de trazabilidad tiene tag + SHA; `state check` vigila que main solo cambie PROJECT_STATE tras el tag; corpus check sin KeyError; `make hooks` portable (Python) desde PowerShell; CI sin doble disparo, tags forzados, actions al dia; ADR-0004 (categorias de parametro, horas con huso, tzdata); lecturas ambiguas sin crecer por tick; contradicciones con Decimal; feedback con fecha = sesion y t0/t1 siempre validados; MASTER_PLAN H.2 con los riesgos de ejecucion absorbidos por funcionalidad; ambiguedades numeradas A-1..A-11; docs incoherentes corregidos. 122 funciones / 167 casos
- 2026-09-04 · push F09; CI Ubuntu verde (run 33894611220); hook de feedback probado
- 2026-09-04 · F09 construida: FeedbackRecord solo-anadir, guardia de historial generalizada, trailer Fuente en commits de spec/cases, capas refinadas; 106 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F09-expert-feedback-model abierta; brief escrito (feedback apply diferido a F11 por falta de esquema de spec)
- 2026-09-04 · F06 VALIDADA por el usuario; merge --no-ff a main (b6b82f2); tag stable/F06
- 2026-09-04 · lineamiento del usuario registrado: SL a 0,75/0,8 tras la entrada con TP fijo (contemplado en F21; dos preguntas abiertas para el trader)
- 2026-09-04 · push F06 tras auditoria global; CI Ubuntu verde (run 33893230602)
- 2026-09-04 · auditoria global: la guardia de historial no detectaba ediciones dentro de un merge (ahora compara blobs con el primer commit); make check ejecuta knowledge validate; coma decimal normalizada en contradicciones; 92 funciones de test
- 2026-09-04 · push F06; CI Ubuntu verde (run 33892467496); hook de evidencia probado en 5 escenarios
- 2026-09-04 · F06 construida: modelo de evidencia inmutable, contradicciones regeneradas, guardia de historial, hook; 89 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F06-evidence-model abierta; brief escrito
- 2026-09-04 · F03 VALIDADA por el usuario; merge --no-ff a main (77fdd44); tag stable/F03
- 2026-09-04 · push F03 tras auditoria; CI Ubuntu verde con ffmpeg (run 33891193380)
- 2026-09-04 · auditoria de F03: orden POSIX del manifiesto (Windows ordenaba sin mayusculas), corpus check detecta ficheros no inventariados, esquema de ficheros validado, ffmpeg en CI, xlsx/pdf binarios; 76 funciones de test
- 2026-09-04 · push de la rama F03; CI Ubuntu verde (run 33890615366)
- 2026-09-04 · F03 construida: fuentes.yaml, inventario.py, manifest.yaml real (4 videos con hash y duracion, 477 heredados, 17 adicionales), corpus inventory/check; 74 funciones de test; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · corpus recibido en local (4 videos identicos a Drive, _procesado heredado, material adicional: 2 xlsx FXReplay + 15 capturas); movido a corpus/ (gitignored); ffmpeg 9 instalado; rama feature/F03-corpus-inventory abierta
- 2026-09-04 · F02 VALIDADA por el usuario; merge --no-ff a main (dc3384d); tag stable/F02; FASE 0 CERRADA
- 2026-09-04 · segunda auditoria de F02: explicit-preview-rules; botsito config validate en make check; 65 funciones / 67 casos
- 2026-09-04 · auditoria de F02: prefijo duplicado en errores, limites con float, accesores tipados, property YAML; 63 funciones / 65 casos
- 2026-09-04 · push de la rama F02; CI Ubuntu verde (run 33883045053)
- 2026-09-04 · F02 construida: valores.py, registro.py, ajustes.py, parametros.yaml vacio, state check ampliado, test de literales real, ADR-0002/0003, sin .pre-commit-config; 59 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · rama feature/F02-config-and-parameter-registry abierta; brief escrito
- 2026-09-04 · F01 VALIDADA por el usuario; merge --no-ff a main (85cedc4); tag stable/F01; push de main
- 2026-09-04 · segunda auditoria: Last Stable Commit corregido (era 0b43244, main esta en 7baa27d), Next Feature = F02, brief de F01 y README actualizados
- 2026-09-04 · tercera auditoria: hook con modo 100755 en el indice, READMEs en todas las carpetas (sin exenciones), holdout/{1,2,3} fisico, mypy strict sobre tests
- 2026-09-04 · pruebas cruzadas: clon limpio, autocrlf=true, HEAD separado, PowerShell 7, Python 3.13 verdes; Linux pendiente del primer push. HALLAZGO: core.hooksPath relativo omitia el hook en main (sin el fichero); make hooks ahora copia a .git/hooks. Reprobado OK
- 2026-09-04 · push de la rama F01 autorizado; CI Ubuntu verde (run 33880866257). Linux verificado
- 2026-09-04 · F01 corregida: .gitattributes, tests de integridad del indice, hook anti-main, uv --locked; 26 tests; WAITING_FOR_USER_VALIDATION
- 2026-09-04 · auditoria de fases (docs/plan/AUDITORIA_FASES_2026-09-04.html): 4 criticos, 19 huecos; plan ampliado (MASTER_PLAN.md seccion H)
- 2026-09-03 · F01 construida; make check verde (21 tests, 3 contratos); WAITING_FOR_USER_VALIDATION
- 2026-09-03 · plan aprobado por el usuario · rama feature/F01-project-scaffold abierta · paquete botsito
- 2026-09-03 · repositorio inicializado en local · punto cero con documentacion · plan pendiente de validacion

# Registro de cierre · `trabajo/dieta-y-skills` (2026-10-01)

- Orden de cierre de Aleks, tras revisar `09a1bd1`; escrita aqui ANTES del merge, en la propia rama,
  porque en `main`, tras el tag, solo puede cambiar `PROJECT_STATE.md` (`state check`, regla 5).
  Decision del consultor del 2026-10-01.
- Tag: `stable/F36k-dieta-y-skills`. El merge es `git rev-parse "stable/F36k-dieta-y-skills^{commit}"`:
  su sha no existe hasta el merge, y el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama: `63efc02` (la dieta, CLAUDE.md, las skills y el borrado remoto), `e5e257f` (B1
  y B2 del revisor), `09a1bd1` (la revision del consultor) y el de este registro, que saca tambien el
  contrato.
- CI de Linux, con la rama empujada como `fix/dieta-y-skills`: `36911338342` (`63efc02`),
  `36913763335` (`e5e257f`) y `36920348532` (`09a1bd1`), cada uno con un solo fallo, el esperado:
  `test_state_check_ok_on_real_repo` por el nombre `fix/` frente a `trabajo/`. `36913763427`
  (`e5e257f`) se cancelo por concurrencia.
- Informe: `docs/validation/DIETA-Y-SKILLS.md`.

# Lo que quedo fuera del cierre de `stable/F36k-dieta-y-skills` (apuntado el 2026-10-01, al abrir `trabajo/cuarentena-por-defecto`)

- Hallazgo A1.5 de la primera ejecucion de `cerrar-rama`, del merge al borrado de las ramas: sin
  diferencias con `RITUAL.md`, salvo una que el runbook no menciona. **En `main`, `make check` da
  «1 skipped»**: es `tests/unit/test_contrato_rama.py:196`, el test del contrato real, que se salta
  porque `contrato.yaml` sale de la rama antes del merge («sin contrato.yaml en esta rama (en main
  sale antes del merge)»). Es lo esperado, no un fallo. No pudo entrar en
  `docs/validation/DIETA-Y-SKILLS.md`, porque en `main`, tras el tag, solo puede cambiar
  `PROJECT_STATE.md` (`state check`, regla 5).
- El cierre: merge `0744ece`, tag `stable/F36k-dieta-y-skills`, commit de estado `c95ab8b`, CI de
  `main` run `36924860137` en verde; `trabajo/dieta-y-skills` y `fix/dieta-y-skills` borradas.

# Archivo 2 · PROJECT_STATE.md de main en c95ab8b (2026-10-01), al abrir trabajo/cuarentena-por-defecto

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA. `trabajo/dieta-y-skills` quedo VALIDADA y cerrada en `main` el 2026-10-01 por orden de cierre explicita de Aleks tras la revision del consultor: tag `stable/F36k-dieta-y-skills`, informe docs/validation/DIETA-Y-SKILLS.md, sin ADR. LO SIGUIENTE: el I del Next Action.

## Stable Main State
0744ece · merge de `trabajo/dieta-y-skills` (tag `stable/F36k-dieta-y-skills`), sobre `stable/F36j-guardia-linux` (1f597cb). PROJECT_STATE lleva solo el presente y su historia vive en docs/state/HISTORIA.md, que solo se amplia; CLAUDE.md revisado; las skills `abrir-rama`, `cerrar-rama` e `ingerir-sesion`; la guardia deja borrar ramas remotas `trabajo/`, `feature/` y `fix/`. El registro del cierre (commits y runs de la CI de Linux), al final de HISTORIA.

## Last Stable Commit
0744ece · merge: la dieta de PROJECT_STATE, CLAUDE.md revisado, las skills del proyecto y el borrado remoto de ramas de trabajo · tag stable/F36k-dieta-y-skills

## Tests Currently Passing
1120 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`; el I, 2026-10-01, al cerrar `trabajo/guardias-claude`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 19 por preguntar -las 17 del barrido y 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

I. **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, «Next Action»); de ellas sigue pendiente lo que D dice -«El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor»- y lo que G dice: «pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6)».

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion…
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-29 | cuando nace la orden limite | pregunta | no | F20, F22 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos.
— ninguna desde el Archivo 1 (2026-10-01).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli.
— ninguna desde el Archivo 1 (2026-10-01).

# Registro de cierre · `trabajo/cuarentena-por-defecto` (2026-10-01)

- Orden de cierre de Aleks, tras revisar `0a7bed1`; escrita aqui ANTES del merge, en la propia rama,
  porque en `main`, tras el tag, solo puede cambiar `PROJECT_STATE.md` (`state check`, regla 5).
- Tag: `stable/F36l-cuarentena-por-defecto`. El merge es
  `git rev-parse "stable/F36l-cuarentena-por-defecto^{commit}"`: su sha no existe hasta el merge, y
  el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama: `b6dd620` (apertura), `d1f144f` (la CLI filtra por defecto), `e30765c`
  (tercera orden), `a4d37e8` (hallazgos del revisor), `bc77e2b` (cuarta y quinta orden), `14bb92c`
  (revisor, segunda pasada), `0faa9ae` (sexta orden: la evidencia con su propio criterio), `0a7bed1`
  (revisor, tercera pasada) y el de este registro, que saca tambien el contrato.
- CI de Linux, con la rama empujada como `fix/cuarentena-por-defecto`: `36936326358` (`e30765c`),
  `36938253913` (`a4d37e8`), `36944773639` (`bc77e2b`), `36946258608` (`14bb92c`), `36949045836`
  (`0faa9ae`) y `36950431596` (`0a7bed1`), cada uno con un solo fallo, el esperado:
  `test_state_check_ok_on_real_repo` por el nombre `fix/` frente a `trabajo/`.
- Informe: `docs/validation/CUARENTENA-POR-DEFECTO.md`. Encargo, con sus seis ordenes:
  `docs/encargos/trabajo-cuarentena-por-defecto.md`.

# Archivo 3 · PROJECT_STATE.md de main en 72d0d20 (2026-10-01), al abrir trabajo/ajustes-cierre

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36l-cuarentena-por-defecto`.

## Stable Main State
8a3b501 · merge de `trabajo/cuarentena-por-defecto` (tag `stable/F36l-cuarentena-por-defecto`), sobre `stable/F36k-dieta-y-skills` (0744ece). La CLI ensena el corpus filtrado por defecto -sesiones en cuarentena, tramos no citables y material reservado o sin sortear, con `src/botsito/corpus/cuarentena.py` como unica fuente- y dice cuanto oculto y por que; la evidencia tiene su propio criterio (solo un tramo no citable o un dia de `casos_ocultos`); la opcion que lo ensena todo y su equivalente en Python, solo para Aleks y para las funciones de `AUTORIZADOS`; la guardia bloquea esa opcion y 14 ficheros que copian texto oculto. Informe docs/validation/CUARENTENA-POR-DEFECTO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
8a3b501 · merge: la CLI enseña el corpus filtrado por defecto (cuarentena, tramos no citables y material reservado), la evidencia con su propio criterio y la guardia bloquea el contenido sin filtrar · tag stable/F36l-cuarentena-por-defecto

## Tests Currently Passing
1149 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`; el I, 2026-10-01, al cerrar `trabajo/guardias-claude`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 19 por preguntar -las 17 del barrido y 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

I. **HECHA, `stable/F36l-cuarentena-por-defecto` (2026-10-01).** Queda una sola cosa de lo que decia: el comentario de `knowledge/corpus/tramos_no_citables.yaml` no se cambio, porque el encargo protegia `knowledge/`. Era: **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, «Next Action»); de ellas sigue pendiente lo que D dice -«El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor»- y lo que G dice: «pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6)».

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion…
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-29 | cuando nace la orden limite | pregunta | no | F20, F22 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos.
— ninguna desde el Archivo 2 (2026-10-01).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli.
— ninguna desde el Archivo 2 (2026-10-01).

# Registro de cierre · `trabajo/ajustes-cierre` (2026-10-01)

- Orden de cierre de Aleks, tras revisar `f443eee`. Primer cierre con la regla nueva de `RITUAL.md`
  («Antes del merge: el contrato sale de la rama»): este registro y la fila de
  `docs/runbooks/ERRORES-RECURRENTES.md` van en el commit que saca el contrato, y el commit de estado
  no anade nada a Change Log ni a Completed Features.
- Tag: `stable/F36m-ajustes-cierre`. El merge es
  `git rev-parse "stable/F36m-ajustes-cierre^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama: `5cdbddf` (apertura: encargo, contrato y Archivo 3), `f443eee` (el comentario
  de `tramos_no_citables.yaml`, el registro y la fila obligatorios en todo cierre, y las frases de
  los runbooks sobre la CLI y la cruda; con el revisor pegado) y el de este registro, que saca
  tambien el contrato.
- CI: ninguna de la rama. No toca hooks ni la plataforma, asi que no se empujo como `fix/` (lo dice
  el encargo); la primera CI es la de `main` tras el cierre.
- Informe: `docs/validation/AJUSTES-CIERRE.md`. Encargo: `docs/encargos/trabajo-ajustes-cierre.md`.

# Archivo 4 · PROJECT_STATE.md de main en a093ffb (2026-10-01), al abrir feature/escenarios-por-sesion

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36m-ajustes-cierre`.

## Stable Main State
1591737 · merge de `trabajo/ajustes-cierre` (tag `stable/F36m-ajustes-cierre`), sobre `stable/F36l-cuarentena-por-defecto` (8a3b501), que dejo la CLI ensenando el corpus filtrado por defecto (`src/botsito/corpus/cuarentena.py`, la unica fuente; la evidencia con su propio criterio; la guardia bloquea la opcion que lo ensena todo y 14 ficheros que copian texto oculto). Esta rama, solo documentacion: todo cierre lleva, en el commit que saca el contrato, su registro en HISTORIA y su fila en ERRORES-RECURRENTES, y el commit de estado no anade nada a Change Log ni a Completed Features (docs/runbooks/RITUAL.md, skill cerrar-rama); `tramos_no_citables.yaml` y los runbooks dicen lo que hace hoy la CLI. Informe docs/validation/AJUSTES-CIERRE.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
1591737 · merge: todo cierre lleva su registro en HISTORIA y su fila en ERRORES-RECURRENTES; los documentos dicen que la CLI enseña el corpus filtrado · tag stable/F36m-ajustes-cierre

## Tests Currently Passing
1149 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`; el I, 2026-10-01, al cerrar `trabajo/guardias-claude`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 19 por preguntar -las 17 del barrido y 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

I. **HECHA, `stable/F36l-cuarentena-por-defecto` (2026-10-01)**, y el comentario de `knowledge/corpus/tramos_no_citables.yaml` que quedaba, en `stable/F36m-ajustes-cierre`. Era: **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, «Next Action»); de ellas sigue pendiente lo que D dice -«El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor»- y lo que G dice: «pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6)».

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion…
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-29 | cuando nace la orden limite | pregunta | no | F20, F22 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 3 (2026-10-01).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 3 (2026-10-01).

# Next Action HECHA · I · sale de PROJECT_STATE.md en feature/escenarios-por-sesion (2026-10-02)

Regla del consultor del 2026-10-02 (`docs/runbooks/RITUAL.md` y `docs/state/README.md`): una
entrada de Next Action que pasa a HECHA se mueve aqui en la misma rama que la cierra. La I se
cerro en `stable/F36l-cuarentena-por-defecto` y `stable/F36m-ajustes-cierre`, antes de la regla,
y sale ahora por orden del consultor. Su texto literal en PROJECT_STATE.md:

I. **HECHA, `stable/F36l-cuarentena-por-defecto` (2026-10-01)**, y el comentario de `knowledge/corpus/tramos_no_citables.yaml` que quedaba, en `stable/F36m-ajustes-cierre`. Era: **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

# Next Action HECHA · A3 b) · sale de PROJECT_STATE.md en feature/escenarios-por-sesion (2026-10-02)

La hace esta rama (orden de cierre del consultor; regla de `docs/runbooks/RITUAL.md`, punto 3).
Su texto literal en «Pendientes heredados (sin verificar)» de PROJECT_STATE.md:

- b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion…

# Next Action HECHA · B, C, D y G · sale de PROJECT_STATE.md en feature/escenarios-por-sesion (2026-10-02)

El resumen de lo hecho sale por orden de cierre del consultor; sus dos pendientes quedan en Next
Action como L (la revision de `ev-v7-001550-82e5cffc`) y M (el break even por el ASK, ADR-0065 §6).
Su texto literal en PROJECT_STATE.md:

B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, «Next Action»); de ellas sigue pendiente lo que D dice -«El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor»- y lo que G dice: «pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6)».

# Registro de cierre · `feature/escenarios-por-sesion` (2026-10-02)

- Orden de cierre de Aleks, tras revisar `32f1175` (`make check` sellado, 1813 pasados). Primer
  cierre con el punto 3 de `RITUAL.md` («Antes del merge: el contrato sale de la rama»): en este
  commit salen de PROJECT_STATE.md A3 b) y el resumen de B, C, D y G (arriba), y la primera linea
  de Next Action deja de nombrar la I.
- Tag: `stable/F36n-escenarios-por-sesion`. El merge es
  `git rev-parse "stable/F36n-escenarios-por-sesion^{commit}"`: su sha no existe hasta el merge, y
  el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `fad197e`: apertura: encargo, contrato y Archivo 4 de PROJECT_STATE;
  - `ae6c7b3`: Fase 0: lo que hay hoy, medido, y el diseno antes de implementar;
  - `066246b`: Fase 1: la toma tiene que ser de la sesion y cada liquidez nueva abre un escenario con sus intentos (ADR-0066);
  - `7ab42d6`: Fase 2: tests y tres dias dev de agosto antes y ahora, sin cobertura, con el revisor;
  - `a43641b`: ordenes 2 y 3: max_escenarios_por_sesion y orden_pendiente_al_abrir_escenario PROVISIONAL, la cadena v4 -> sesion 1;
  - `86a49e6`: su revisor, y el caso peor de cinco escenarios medido con un test;
  - `8626711`: orden 4: todo parametro PROVISIONAL cuelga de una ambiguedad ABIERTA; A-52 y A-53;
  - `4818e1c`: su revisor;
  - `76be592`: orden 5: lo HECHO del Next Action sale de PROJECT_STATE en la rama que lo cierra; la I a HISTORIA; sesgo_h4_tope_velas;
  - `32f1175`: su revisor;
  - y el de este registro, que saca tambien el contrato.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca hooks ni la plataforma, lo
  dice la orden de cierre. La primera CI es la de `main` tras el cierre.
- Informe: `docs/validation/ESCENARIOS-POR-SESION.md`. Encargo, con las cinco ordenes:
  `docs/encargos/feature-escenarios-por-sesion.md`.

# Archivo 5 · PROJECT_STATE.md de main en 487c64f (2026-10-02), al abrir trabajo/cerrar-a29-a36

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36n-escenarios-por-sesion` (2026-10-02).

## Stable Main State
8346b9b · merge de `feature/escenarios-por-sesion` (tag `stable/F36n-escenarios-por-sesion`): las sesiones son independientes -la toma tiene que ser de la sesion- y cada liquidez nueva abre un escenario con sus intentos; una ganadora termina el escenario y el dia sigue (RN-034 con RN-017, ADR-0066). PROVISIONAL en cinco parametros con su pregunta de la sesion 4 (5, 15, 18, 20 y 21); A-52 y A-53 abiertas, y un test exige que todo parametro PROVISIONAL cuelgue de una ambiguedad ABIERTA. Lo HECHO del Next Action sale de PROJECT_STATE en la rama que lo cierra (RITUAL.md, punto 3). Informe docs/validation/ESCENARIOS-POR-SESION.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
8346b9b · merge: sesiones independientes y varios escenarios por sesion (ADR-0066), A-52 y A-53, y lo HECHO del Next Action fuera de PROJECT_STATE · tag stable/F36n-escenarios-por-sesion

## Tests Currently Passing
1165 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 21 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, y la 20 y la 21 de `feature/escenarios-por-sesion`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

K. **Freno duro de peticiones al servidor: hoy el código solo cuenta las peticiones y nada impide pasar de las 2.000 al día de FTMO (medido en feature/escenarios-por-sesion). Rama propia antes de operar en una cuenta real** (orden del consultor del 2026-10-02; docs/validation/ESCENARIOS-POR-SESION.md §6.4).

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-29 | cuando nace la orden limite | pregunta | no | F20, F22 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 4 (2026-10-01).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 4 (2026-10-01).

# Registro de cierre · `trabajo/cerrar-a29-a36` (2026-10-02)

- Orden de cierre de Aleks, tras revisar `57b24f7` (`make check` sellado, 1814 pasados). A-29
  queda RESUELTA (`fb-2026-09-29-sesion-03-d3063920`); A-36 se cerro y el consultor la reabrio
  (`fb-2026-09-29-sesion-03-a0b61bc9`): va a la sesion 4 como pregunta 22.
- Tag: `stable/F36o-cerrar-a29-a36`. El merge es
  `git rev-parse "stable/F36o-cerrar-a29-a36^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `e7851f7`: apertura: encargo, contrato y Archivo 5;
  - `541a4f5`: A-29 y A-36 RESUELTAS con la respuesta grabada de la sesion 3; las citas verificadas por la via autorizada; el test antes/despues de A-29; la hoja de preguntas y SECCIONES_EXENTAS;
  - `19b09eb`: el revisor pegado y atendido;
  - `a7d06c9`: segunda orden: A-29 con la nota del contexto (fb-...-d3063920); A-36 reabierta (fb-...-a0b61bc9) y pregunta 22; cerrar una ambiguedad toca cinco sitios (AMBIGUEDADES.md y CLAUDE.md);
  - `57b24f7`: su revisor, y dos runbooks que decian cuatro;
  - `824ad9c`: orden de cierre: .claude/agents/revisor.md dice cinco sitios, y la deuda de REABRIR en Technical Debt;
  - y el de este registro, que saca tambien el contrato.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca hooks ni la plataforma, lo
  dice la orden de cierre. La primera CI es la de `main` tras el cierre.
- Ninguna entrada de Next Action queda HECHA por esta rama (`RITUAL.md`, punto 3): no sale nada
  de `PROJECT_STATE.md` en este commit.
- Informe: `docs/validation/CERRAR-A29-A36.md`. Encargo, con sus dos ordenes:
  `docs/encargos/trabajo-cerrar-a29-a36.md`.

# Archivo 6 · PROJECT_STATE.md de main en 695041d (2026-10-02), al abrir feature/freno-peticiones

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36o-cerrar-a29-a36` (2026-10-02).

## Stable Main State
34680ba · merge de `trabajo/cerrar-a29-a36` (tag `stable/F36o-cerrar-a29-a36`): A-29 RESUELTA con la respuesta grabada de la sesion 3 (`orden_limite_nace` CONFIRMED, el mismo valor; el motor no cambia, medido); A-36 se cerro y el consultor la reabrio: va a la sesion 4 como pregunta 22. Cerrar una ambiguedad toca cinco sitios (docs/runbooks/AMBIGUEDADES.md, con la hoja de preguntas). Sobre `stable/F36n-escenarios-por-sesion` (8346b9b), las sesiones independientes (ADR-0066). Informe docs/validation/CERRAR-A29-A36.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
34680ba · merge: A-29 RESUELTA y A-36 reabierta como pregunta 22; cerrar una ambiguedad toca cinco sitios · tag stable/F36o-cerrar-a29-a36

## Tests Currently Passing
1166 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

K. **Freno duro de peticiones al servidor: hoy el código solo cuenta las peticiones y nada impide pasar de las 2.000 al día de FTMO (medido en feature/escenarios-por-sesion). Rama propia antes de operar en una cuenta real** (orden del consultor del 2026-10-02; docs/validation/ESCENARIOS-POR-SESION.md §6.4).

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)
- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 5 (2026-10-02).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 5 (2026-10-02).

# Next Action HECHA · K · sale de PROJECT_STATE.md en feature/freno-peticiones (2026-10-02)

La hace esta rama (orden de cierre del consultor; `docs/runbooks/RITUAL.md`, punto 3). Su texto
literal en PROJECT_STATE.md:

K. **Freno duro de peticiones al servidor: hoy el código solo cuenta las peticiones y nada impide pasar de las 2.000 al día de FTMO (medido en feature/escenarios-por-sesion). Rama propia antes de operar en una cuenta real** (orden del consultor del 2026-10-02; docs/validation/ESCENARIOS-POR-SESION.md §6.4).

# Registro de cierre · `feature/freno-peticiones` (2026-10-02)

- Orden de cierre de Aleks, tras revisar `e34d536` (`make check` sellado, 1831 pasados). El freno
  de peticiones vive en el puerto del broker (ADR-0067), con sus umbrales PROVISIONAL bajo A-54.
- Tag: `stable/F36p-freno-peticiones`. El merge es
  `git rev-parse "stable/F36p-freno-peticiones^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `91b3291`: apertura: encargo, contrato y Archivo 6;
  - `ab1367f`: Fase 0: el inventario de peticiones y el diseno del freno, antes del codigo;
  - `652c75b`: el freno en el puerto del broker (ADR-0067): aviso, corte y bucle; A-54; los tests rotos a proposito;
  - `e34d536`: tras el revisor: solo el primer movimiento del stop protege (b1); cada negada al log; tests nuevos;
  - `913b023`: orden de cierre: lo que protege tras el corte por bucle, con su test; A-54 dice de donde sale; la deuda del esquema;
  - y el de este registro, que saca tambien el contrato y la K de Next Action.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca la plataforma, lo dice la
  orden de cierre. La primera CI es la de `main` tras el cierre.
- Informe: `docs/validation/FRENO-PETICIONES.md`. Encargo: `docs/encargos/feature-freno-peticiones.md`.

# Archivo 7 · PROJECT_STATE.md de main en 5947e55 (2026-10-02), al abrir feature/cierres-de-mercado

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36p-freno-peticiones` (2026-10-02).

## Stable Main State
b64e675 · merge de `feature/freno-peticiones` (tag `stable/F36p-freno-peticiones`): el freno de peticiones al servidor vive en el puerto del broker (ADR-0067, engine/freno.py): aviso en 1000, corte en 1500 y bucle de 5 iguales en 1 minuto, PROVISIONAL bajo A-54; lo que protege la cuenta (cancelar, cerrar, el primer stop a break even) sale siempre y cuenta. Sobre `stable/F36o-cerrar-a29-a36` (34680ba). Informe docs/validation/FRENO-PETICIONES.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
b64e675 · merge: el freno de peticiones al servidor en el puerto del broker (ADR-0067), A-54 · tag stable/F36p-freno-peticiones

## Tests Currently Passing
1183 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- El esquema de ambigüedades exige una cita de evidencia aunque la fuente sea una regla de FTMO (A-27, A-54): rama propia para admitir una fuente documental.
- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)
- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 6 (2026-10-02).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 6 (2026-10-02).

# Next Action HECHA · A3 e) · sale de PROJECT_STATE.md en feature/cierres-de-mercado (2026-10-02)

La hace esta rama (orden de cierre del consultor, punto 2; `docs/runbooks/RITUAL.md`, punto 3). Su
texto literal en «Pendientes heredados» de PROJECT_STATE.md, bajo «A3. **Ramas de codigo, en este
orden** (orden del consultor del 2026-09-29):»:

- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).

# Registro de cierre · `feature/cierres-de-mercado` (2026-10-02)

- Orden de cierre de Aleks, tras revisar `582e4c8` (`make check` sellado, 1860 pasados; sin CI de
  Linux por `fix/` porque no toca la plataforma). El bot no abre ni coloca en la ventana que R15 de
  FTMO prohibe antes de un cierre de mercado largo: predicado unico en el puerto del broker
  (ADR-0068), calendario versionado en `knowledge/cuentas/cierres/`, `cierre_pendientes`
  PROVISIONAL bajo A-55 y el huso del calendario PROVISIONAL bajo A-28.
- Tag: `stable/F36q-cierres-de-mercado`. El merge es
  `git rev-parse "stable/F36q-cierres-de-mercado^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `369d9f8`: apertura: encargo, contrato y Archivo 7;
  - `94b28ad`: Fase 0: la regla, los cierres de EURUSD en FTMO (API de simbolos y 43 Trading Updates) y el diseno, antes del codigo; el contrato se amplia a `knowledge/cuentas/`;
  - `227bc5e`: el predicado en el puerto del broker (ADR-0068), el calendario, los parametros de R15, A-55 y los tests, rotos a proposito;
  - `582e4c8`: tras el revisor: el huso del calendario PROVISIONAL bajo A-28 (a1), la cancelacion por cierre sin evento del servidor (a3), tests por el cableado (b1), la modificacion bajo A-55 (b2); el revisor pegado;
  - `4df3c5a`: orden de cierre: la renovacion del calendario en Next Action (N) y b2 decidido sin parametro propio;
  - y el de este registro, que saca tambien el contrato y la A3 e) de PROJECT_STATE.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca la plataforma, lo dice la
  orden de cierre. La primera CI es la de `main` tras el cierre.
- Informe: `docs/validation/CIERRES-DE-MERCADO.md`. Encargo: `docs/encargos/feature-cierres-de-mercado.md`.

# Archivo 8 · PROJECT_STATE.md de main en 7dcbb6a (2026-10-03), al abrir trabajo/fuentes-ftmo

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36q-cierres-de-mercado` (2026-10-02).

## Stable Main State
aaac17b · merge de `feature/cierres-de-mercado` (tag `stable/F36q-cierres-de-mercado`): el bot no abre ni coloca en la ventana que R15 de FTMO prohibe antes de un cierre de mercado largo (ADR-0068, domain/cierres.py): predicado unico en el puerto del broker, calendario versionado en knowledge/cuentas/cierres/ (cubre hasta el 7-10-2026, Next Action N), `cierre_pendientes` PROVISIONAL bajo A-55. Sobre `stable/F36p-freno-peticiones` (b64e675). Informe docs/validation/CIERRES-DE-MERCADO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
aaac17b · merge: la ventana que FTMO prohibe antes de un cierre de mercado largo, en el puerto del broker (ADR-0068), A-55 · tag stable/F36q-cierres-de-mercado

## Tests Currently Passing
1208 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026; vencido, el simulador no corre y en vivo el bot no coloca nada. Renovarlo cada semana desde las Trading Updates de FTMO hasta que el adaptador MT5 lea SymbolInfoSessionTrade (ADR-0068 §4); rama propia para automatizarlo antes de operar en real.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- El esquema de ambigüedades exige una cita de evidencia aunque la fuente sea una regla de FTMO (A-27, A-54): rama propia para admitir una fuente documental.
- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)
- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 7 (2026-10-02).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 7 (2026-10-02).

# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/fuentes-ftmo (2026-10-03)

La paga `stable/F36q-cierres-de-mercado` (ADR-0068: el broker no abre ni coloca en la ventana de R15) y lo que quedaba abierto ya lo llevan A-55 (las preguntas a soporte, enviadas el 2026-10-03 en el ticket VDW-DPMWR-965) y la entrada N de Next Action (la renovacion del calendario). Encargo de `trabajo/fuentes-ftmo`, punto 2; docs/validation/FUENTES-FTMO.md §3. Su texto literal en «Technical Debt»:

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).

# Registro de cierre · `trabajo/fuentes-ftmo` (2026-10-03)

- Orden de cierre de Aleks, en la segunda orden de la rama (copiada en
  `docs/encargos/trabajo-fuentes-ftmo.md`). Solo documentacion y knowledge: la respuesta de FTMO
  del 29-09-2026 y el correo de Aleks del 2026-10-03 (ticket VDW-DPMWR-965), literales en
  `docs/validation/FTMO-REGLAS.md`; A-54 y A-55 con sus preguntas enviadas (1-4 y 5-9 del correo);
  la deuda del gap trading a HISTORIA y la del tamano de posicion (R17, pregunta 10) en su lugar.
- Tag: `stable/F36r-fuentes-ftmo`. El merge es `git rev-parse "stable/F36r-fuentes-ftmo^{commit}"`:
  su sha no existe hasta el merge, y el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `c4adb52`: apertura: encargo, contrato y Archivo 8;
  - `0e69da5`: la respuesta literal del ticket como fuente; recuadros de correccion en CIERRES-DE-MERCADO.md; ADR-0068 con la frase literal; Technical Debt; A-54 y A-55;
  - `0b9c9a3`: tras el revisor (primera pasada): el sello en §5 del informe; el informe del revisor pegado;
  - `ecc8307`: segunda orden: el correo del 2026-10-03 como fuente, la numeracion 1-10 y el numero de pregunta en A-54, A-55 y R17;
  - `b2624ba`: segunda pasada del revisor: el informe recompuesto (§8 y §9 se habian pegado dentro de la cita de §7);
  - y el de este registro, que saca tambien el contrato.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca la plataforma. La primera CI
  es la de `main` tras el cierre.
- Informe: `docs/validation/FUENTES-FTMO.md`. Encargo: `docs/encargos/trabajo-fuentes-ftmo.md`.

# Archivo 9 · PROJECT_STATE.md de main en 60d540c (2026-10-03), al abrir trabajo/renovar-cierres

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36r-fuentes-ftmo` (2026-10-03).

## Stable Main State
36a9801 · merge de `trabajo/fuentes-ftmo` (tag `stable/F36r-fuentes-ftmo`): la respuesta de FTMO del 29-09 y el correo de Aleks del 2026-10-03 (ticket VDW-DPMWR-965), literales en docs/validation/FTMO-REGLAS.md; A-54 y A-55 con sus preguntas enviadas (1-4 y 5-9), R17 en la 10. Sobre `stable/F36q-cierres-de-mercado` (aaac17b). Informe docs/validation/FUENTES-FTMO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
36a9801 · merge: las fuentes escritas de FTMO (respuesta y correo del ticket VDW-DPMWR-965), A-54 y A-55 con sus preguntas enviadas · tag stable/F36r-fuentes-ftmo

## Tests Currently Passing
1208 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026; vencido, el simulador no corre y en vivo el bot no coloca nada. Renovarlo cada semana desde las Trading Updates de FTMO hasta que el adaptador MT5 lea SymbolInfoSessionTrade (ADR-0068 §4); rama propia para automatizarlo antes de operar en real.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- El esquema de ambigüedades exige una cita de evidencia aunque la fuente sea una regla de FTMO (A-27, A-54): rama propia para admitir una fuente documental.
- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 8 (2026-10-03).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 8 (2026-10-03).

# Registro de cierre · `trabajo/renovar-cierres` (2026-10-03)

- Orden de cierre de Aleks del 2026-10-03, revisada y aprobada. El calendario de cierres caduca por
  la FECHA SIMULADA, nunca por la de hoy (medido en un clon con el reloj adelantado), y no se
  renueva cada semana: se renueva por condicion (`docs/runbooks/RENOVAR-CIERRES.md`). Tests nuevos:
  el cable trampa del reloj permanente y el exit 2 de un dia posterior a `hasta` por la CLI. El YAML
  del calendario no se toco. `Tests Currently Passing` paso de 1208 a 1211 en la rama (lo exige
  `state check`; aceptado en la orden de cierre).
- Punto 0 de la orden: `git tag -l "stable/F99*"` y `git ls-remote --tags origin "stable/F99*"`
  salen vacios. El tag de ensayo de la Fase 0 solo existio en el clon desechable.
- Tag: `stable/F36s-renovar-cierres`. El merge es
  `git rev-parse "stable/F36s-renovar-cierres^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `4344f2f`: apertura: encargo, contrato y Archivo 9;
  - `21ffe85`: Fase 0: la caducidad medida (fecha simulada, no la de hoy), la fuente de octubre y el procedimiento;
  - `9565539`: segunda orden: el cable trampa permanente, el exit 2 por la CLI y el runbook;
  - `51ca48c`: tras el revisor: `gmtime()` saboteado, el dia con el calendario real, §0.3 marcado SUSTITUIDO; el revisor pegado;
  - y el de este registro, que saca tambien el contrato.
- CI: ninguna de la rama. No se empujo nunca (ni como `fix/`): no toca rutas ni el sistema de
  archivos. La primera CI es la de `main` tras el cierre.
- La linea N de Next Action la sustituye el commit de estado en `main`, con el texto de la orden
  de cierre.
- Informe: `docs/validation/RENOVAR-CIERRES.md`. Encargo: `docs/encargos/trabajo-renovar-cierres.md`.

# Archivo 10 · PROJECT_STATE.md de main en d942aff (2026-10-03), al abrir trabajo/reabrir-y-fuente-documental

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36s-renovar-cierres` (2026-10-03).

## Stable Main State
dfd1a6f · merge de `trabajo/renovar-cierres` (tag `stable/F36s-renovar-cierres`): el calendario de cierres caduca por la fecha simulada, nunca por la de hoy (tests del cable trampa del reloj y del exit 2 por la CLI), y se renueva por condicion (docs/runbooks/RENOVAR-CIERRES.md). Sobre `stable/F36r-fuentes-ftmo` (36a9801). Informe docs/validation/RENOVAR-CIERRES.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
dfd1a6f · merge: el calendario de cierres caduca por la fecha simulada; se renueva por condicion (RENOVAR-CIERRES.md) · tag stable/F36s-renovar-cierres

## Tests Currently Passing
1211 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- El esquema de ambigüedades exige una cita de evidencia aunque la fuente sea una regla de FTMO (A-27, A-54): rama propia para admitir una fuente documental.
- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 9 (2026-10-03).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 9 (2026-10-03).

# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/reabrir-y-fuente-documental (2026-10-03)

Las paga `trabajo/reabrir-y-fuente-documental`: la accion `REOPEN` del modelo de feedback (A-36 migrada con fb-2026-09-29-sesion-03-f3caeb2d, y `feedback pending` ya no la cuenta) y `fuentes_documentales` en las ambiguedades de clase `medicion` (A-27, A-28, A-54 y A-55 migradas a FTMO-REGLAS.md R11, R10, R13 y R15). Decisiones 1 a 4 del consultor del 2026-10-03; docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md. Su texto literal en «Technical Debt»:

- El esquema de ambigüedades exige una cita de evidencia aunque la fuente sea una regla de FTMO (A-27, A-54): rama propia para admitir una fuente documental.
- El modelo de feedback no tiene acción para REABRIR una ambigüedad: A-36 se reabrió con RESOLVE_UNKNOWN y valor "sin resolver" (fb-…-a0b61bc9), y feedback pending la cuenta como pendiente. Rama propia para una acción REOPEN. (docs/validation/CERRAR-A29-A36.md §8.2)

# Registro de cierre · `trabajo/reabrir-y-fuente-documental` (2026-10-03)

- Orden de cierre de Aleks del 2026-10-03, revisada y aprobada. La rama paga las dos deudas que
  pedia el encargo: la accion `REOPEN` del modelo de feedback (A-36 migrada con
  `fb-2026-09-29-sesion-03-f3caeb2d`; `feedback pending` ya no la cuenta) y `fuentes_documentales`
  en las ambiguedades de clase `medicion`, con ruta dentro de `docs/`, documento commiteado, ancla
  en un encabezado y, desde la tercera orden, `fila` de tabla. A-27 (R11), A-28 (R10), A-54 (R13) y
  A-55 (R15) citan `FTMO-REGLAS.md` en vez del item de FundedNext; la respuesta del ticket de A-55
  queda anclada a la seccion (es un recuadro, no una fila). Sin git, `knowledge validate` avisa de
  que «commiteado» no se comprobo. `Tests Currently Passing` paso de 1211 a 1239 en la rama.
- Decisiones de la orden de cierre: aceptados el AVISO sin git, el ancla a la seccion de la
  respuesta del ticket de A-55 y la linea de deuda de RN-029 a RN-032. Deuda nueva en este commit:
  las comprobaciones de historial que dicen «intacto» sin git (informe §4.2). Next Action no cambia.
- Punto 1 de la orden: la ultima letra cerrada era la s (`stable/F36s-renovar-cierres`); `t` libre
  en local y en `origin`.
- Tag: `stable/F36t-reabrir-y-fuente-documental`. El merge es
  `git rev-parse "stable/F36t-reabrir-y-fuente-documental^{commit}"`: su sha no existe hasta el
  merge, y el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `83b6452`: apertura: encargo, contrato y Archivo 10;
  - `b54db12`: Fase 0: el modelo de feedback, el caso de A-36 medido, las citas de relleno y la propuesta;
  - `63ab911`: Fase 1: `REOPEN`, las fuentes documentales, A-36 migrada, las cuatro migraciones, 19 tests y los documentos que repiten la regla;
  - `84e2a3c`: tras el revisor: lo ya reabierto no se reabre dos veces; recuadros SUSTITUIDO en el encargo; runs 195 y 196;
  - `5966079`: tercera orden: `fila` de tabla, el AVISO sin git, la deuda de RN-029 a RN-032;
  - `ac496fc`: el run 198 y la pasada corta del revisor;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux, empujada como `fix/` (la guardia nueva lee rutas):
  - run 195 (37158792667), `fix/trabajo-reabrir-y-fuente-documental`, 63ab911: ROJA en `contrato`
    antes de correr ningun test (el nombre de la orden no pasa `contrato_rama.py`; error del
    consultor, en ERRORES-RECURRENTES);
  - run 196 (37158869991), `fix/reabrir-y-fuente-documental`, 63ab911: 1 failed, 1883 passed, 8 skipped;
  - run 197 (37160166345), 84e2a3c: 1 failed, 1884 passed, 8 skipped;
  - run 198 (37164110797), 5966079: 1 failed, 1894 passed, 8 skipped;
  - run 199 (37164986983), ac496fc: 1 failed, 1894 passed, 8 skipped.
  En los cuatro ultimos el fallo es el UNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`, porque `PROJECT_STATE` declara `trabajo/...` y la rama es
  `fix/...`. El cierre borra las dos ramas `fix/` de `origin`.
- Informe: `docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md`. Encargo, con la segunda y la tercera
  orden: `docs/encargos/trabajo-reabrir-y-fuente-documental.md`.

# Archivo 11 · PROJECT_STATE.md de main en 48ccbd2 (2026-10-03), al abrir trabajo/historial-sin-git

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36t-reabrir-y-fuente-documental` (2026-10-03).

## Stable Main State
c76aaf6 · merge de `trabajo/reabrir-y-fuente-documental` (tag `stable/F36t-reabrir-y-fuente-documental`): la accion REOPEN reabre una ambiguedad RESUELTA (A-36 migrada; `feedback pending` ya no la cuenta) y una ambiguedad `medicion` cita una fuente documental -documento en docs/, commiteado, encabezado y fila de tabla- en vez de evidencia de relleno (A-27, A-28, A-54 y A-55 a FTMO-REGLAS.md R11, R10, R13 y R15); sin git, `knowledge validate` lo avisa. Sobre `stable/F36s-renovar-cierres` (dfd1a6f). Informe docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
c76aaf6 · merge: REOPEN reabre una ambiguedad; una medicion cita una fuente documental anclada a su fila (REABRIR-Y-FUENTE-DOCUMENTAL.md) · tag stable/F36t-reabrir-y-fuente-documental

## Tests Currently Passing
1239 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Las comprobaciones de historial (transcripciones, fotogramas, manifiestos, libros, días retirados, y por el código feedback y evidencia) imprimen "historial intacto" o "solo-añadir intacto" sin git, sin haber evaluado nada: dicen más de lo que comprueban. Rama corta propia para que digan que no se comprobó (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.2).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 10 (2026-10-03).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 10 (2026-10-03).

# Registro de cierre · `trabajo/historial-sin-git` (2026-10-03)

- Orden de cierre del consultor del 2026-10-03, ejecutada con `/cerrar-rama`. La rama hace que
  ninguna comprobacion de `knowledge validate` afirme lo que no evaluo: sin git, o con git y el
  historial no evaluable (`historial_evaluable`), las nueve comprobaciones de historial (libros,
  retirados, evidencia, feedback, trailers `Fuente:` con su ancla, manifiestos de datos,
  transcripciones, fotogramas y fuentes documentales) no dicen «intacto» ni «commits con Fuente»:
  un AVISO dice que NO se comprobo y por que. Con git la salida y el codigo de salida son los de
  antes. La clase `Historial` (`src/botsito/validation/knowledge.py`) es la unica puerta: por ella
  sale toda afirmacion de historial (`validar` da ERROR por una que no salga de `Historial.ok`) y,
  desde la segunda orden, es lo unico de `validation/` que lee git (un test por `ast` lo exige; las
  palabras quedan como segunda red). `Tests Currently Passing` paso de 1239 a 1246 en la rama.
- **Deuda PAGADA**: la de Technical Debt que apuntaba a `docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md`
  §4.2 («las comprobaciones de historial imprimen "historial intacto" o "solo-añadir intacto" sin
  git, sin haber evaluado nada»); su linea salio de `PROJECT_STATE.md` en la rama (5740220).
- Deuda NUEVA, de la segunda orden: las lecturas de git fuera de `validation/` que no pasan por
  `Historial` -las anclas de paquetes, fidelidad y dev-visto y la subida de `spec_version`- callan
  sin git (informe §3 y §6.1). Next Action no cambia.
- Letra: la ultima cerrada era la t (`stable/F36t-reabrir-y-fuente-documental`); `u` libre en local
  y en `origin`.
- Tag: `stable/F36u-historial-sin-git`. El merge es
  `git rev-parse "stable/F36u-historial-sin-git^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `1f29cf5`: apertura: encargo, contrato, Archivo 11 y el inventario de la Fase 0;
  - `5740220`: Fase 1: `Historial`, los avisos y seis tests, cada uno roto a proposito;
  - `ac08b5a`: el run 201, el sello y el informe del revisor;
  - `7c5737b`: segunda orden: en `validation/` solo `Historial` lee git, con su test por `ast`; la
    linea de deuda nueva;
  - `cab9eb1`: el run 202 y la pasada corta del revisor sobre el informe terminado;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux, empujada como `fix/historial-sin-git` (depende de que haya git o no):
  - run 201 (37170620167), 5740220: 1 failed, 1900 passed, 8 skipped;
  - run 202 (37173283083), 7c5737b (lleva tambien ac08b5a, que se habia quedado sin empujar):
    1 failed, 1901 passed, 8 skipped;
  - run 203 (37174448798), cab9eb1: 1 failed, 1901 passed, 8 skipped.
  En los tres el fallo es el UNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`, porque `PROJECT_STATE` declara `trabajo/...` y la rama es
  `fix/...`. El cierre borra `fix/historial-sin-git` de `origin`.
- Informe: `docs/validation/HISTORIAL-SIN-GIT.md`. Encargo, con la segunda orden y la orden de
  cierre: `docs/encargos/trabajo-historial-sin-git.md`.

# Archivo 12 · PROJECT_STATE.md de main en 48f9701 (2026-10-04), al abrir trabajo/sesion-04

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36u-historial-sin-git` (2026-10-03).

## Stable Main State
8e21fd1 · merge de `trabajo/historial-sin-git` (tag `stable/F36u-historial-sin-git`): sin git, o con git y el historial no evaluable, ninguna comprobacion de `knowledge validate` dice «intacto» ni «commits con Fuente»: un AVISO dice que NO se comprobo y por que; con git, la salida es la de antes. La clase `Historial` (validation/knowledge.py) es la unica puerta por la que sale una afirmacion de historial y lo unico de validation/ que lee git (test por ast). Sobre `stable/F36t-reabrir-y-fuente-documental` (c76aaf6). Informe docs/validation/HISTORIAL-SIN-GIT.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
8e21fd1 · merge: sin historial evaluado, knowledge validate no dice «intacto»; en validation/ solo Historial lee git (HISTORIAL-SIN-GIT.md) · tag stable/F36u-historial-sin-git

## Tests Currently Passing
1246 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 11 (2026-10-03).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 11 (2026-10-03).

# Next Action HECHA · F · sale de PROJECT_STATE.md en trabajo/sesion-04 (2026-10-04)

La hace esta rama: la sesion 4 se hizo con la hoja y se ingirio (orden de cierre del consultor del
2026-10-04; `docs/runbooks/RITUAL.md`, punto 3). Su texto literal en PROJECT_STATE.md:

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 22 por preguntar -las 17 del barrido, 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima, la 20 y la 21 de `feature/escenarios-por-sesion` y la 22 de `trabajo/cerrar-a29-a36`- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

# Registro de cierre · `trabajo/sesion-04` (2026-10-04)

- Orden de cierre del consultor del 2026-10-04, ejecutada a mano siguiendo `RITUAL.md`. La rama
  ingiere la sesion 4 con el trader como v10 (`drive_id: null`, 2026-10-04, en
  `SESIONES_EN_CUARENTENA`): transcripcion `tr-v10-large-v3-int8-float16-85e8af79` (1914
  segmentos), fotogramas `fr-v10-69219820` (7657), 21 tramos no citables de v10 (4 SIN AUDIO, 12 de
  la cuarentena mecanica, 3 de precaucion, 1 de conversacion personal y 1 de un mes con dias ocultos
  que la cuarentena no cubre) y 64 items `ev-v10-*`.
  - El informe da la extraccion por pregunta de S-1..S-24 (13 resuelven, 11 en parte). No resuelve
    nada en la spec: el destino de cada respuesta lo decide el consultor en la rama de activacion.
  - `scripts/transcribir_sesion.py` guarda la hoja y los textos de los codigos POR SESION
    (`--sesion`, `ORDEN_SESION_04`).
  - `Tests Currently Passing` paso de 1246 a 1251 funciones (1910 -> 1919 casos).
- Deuda NUEVA: falta un test que exija `Fuente:` en todo commit que toque
  `tramos_no_citables.yaml` (orden de cierre, decision 2).
- Pendientes (informe §6):
  - (a) la rama de cuarentena que oculte todo mes con dias en `casos_ocultos`, antes de activar la
    sesion 4 (entra como primer punto de Next Action);
  - (b) con el guion nuevo en `main`, `--solo-filtrar --sesion 03` sobre v9 (sha esperado
    `f7529459…`) y `--sesion 04` sobre v10.
- S-14 («12 puntos»): queda como ambiguedad del ASR para la rama de activacion (decision 3).
- Next Action: F sale aqui (arriba). En el commit de estado se reemplaza E (A-42 respondida en S-7,
  pendiente de activar antes del 25 de octubre con las horas en UTC), entra un primer punto nuevo
  (la rama de cuarentena) y H lleva una nota.
- Letra: la ultima cerrada era la u (`stable/F36u-historial-sin-git`); `v` libre en local y en
  `origin`.
- Tag: `stable/F36v-sesion-04`. El merge es `git rev-parse "stable/F36v-sesion-04^{commit}"`: su sha
  no existe hasta el merge, y el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `536e958`: apertura: encargo, contrato, Archivo 12 y el informe EN CURSO;
  - `cfec50b`: v10 en el corpus y en la cuarentena, transcripcion, fotogramas y los 16 primeros
    tramos no citables, antes de leer nada;
  - `c489685`: la extraccion, los 64 items, la hoja por sesion con su test roto a proposito, la
    fila de HOLDOUT y la revision del consultor;
  - `d28e6c7`: la CI 205 y el informe del revisor, con sus hallazgos arreglados;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux, empujada como `fix/sesion-04`:
  - run 205 (37224218115), c489685: 1 failed, 1910 passed, 8 skipped;
  - run 206 (37226574157), d28e6c7: 1 failed, 1910 passed, 8 skipped.
  En los dos el fallo es el UNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`. Un primer intento de commit y push se denego en modo
  automatico; despues Aleks los aprobo a la vista. El cierre borra `fix/sesion-04` de `origin`.
- Informe: `docs/validation/SESION-04-EXTRACCION.md`, con la revision del consultor, el informe del
  revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-sesion-04.md`. Hoja usada:
  `docs/sesion-4/HOJA-USADA.md`.

# Archivo 13 · PROJECT_STATE.md de main en e98815a (2026-10-04), al abrir trabajo/cuarentena-por-condicion

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36v-sesion-04` (2026-10-04).

## Stable Main State
eec79a0 · merge de `trabajo/sesion-04` (tag `stable/F36v-sesion-04`): la sesion 4 con el trader entra como v10, en cuarentena (transcripcion, fotogramas, 21 tramos no citables y 64 items ev-v10-*), con su extraccion por pregunta S-1..S-24 (13 resuelven, 11 en parte) y SIN resolver nada en la spec; scripts/transcribir_sesion.py guarda la hoja y los textos de los codigos por sesion (--sesion). Sobre `stable/F36u-historial-sin-git` (8e21fd1). Informe docs/validation/SESION-04-EXTRACCION.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
eec79a0 · merge: la sesion 4 con el trader (v10) ingerida, su extraccion por pregunta y la hoja por sesion (SESION-04-EXTRACCION.md) · tag stable/F36v-sesion-04

## Tests Currently Passing
1251 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

P. **Rama de cuarentena: ocultar todo mes con días en casos_ocultos (§6 del informe), antes de activar la sesión 4** (orden de cierre de `trabajo/sesion-04`, 2026-10-04; docs/validation/SESION-04-EXTRACCION.md §6, pendiente a).

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 12 (2026-10-04).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 12 (2026-10-04).

# Registro de cierre · `trabajo/cuarentena-por-condicion` (2026-10-04)

- Orden de cierre del consultor del 2026-10-04, ejecutada a mano siguiendo `RITUAL.md`: la skill
  `cerrar-rama` solo la invoca el usuario. La rama hace que la cuarentena del texto deje de ser una
  lista fija de meses y tape todo mes que no se pueda DEMOSTRAR libre:
  - (a) sin dias en `casos_ocultos` ni en `casos_reservados`, en ningun ano;
  - (b) fuera de `knowledge/cases/meses_reservados.yaml`, la fuente nueva, SOLO ANADIR, con 2026-02
    y 2026-03;
  - (c) las dos comprobadas. `cases.holdout.meses_libres` devuelve None ante cualquier fallo, y
    entonces se tapan los doce.
- Cambios en el codigo:
  - `MESES_FILTRADOS` pasa a ser `GRAFIAS_MES`, un diccionario de grafias de los doce meses;
  - `corpus.cuarentena` recibe los meses libres por argumento;
  - CLI, retrieval, `transcribir_sesion.py` y `ficheros_con_ocultos.py` los pasan;
  - `knowledge validate` vigila la fuente nueva, borrado del fichero incluido.
- Dos tramos de precaucion en v6, los unicos segmentos nuevos del escenario B. Las filtradas de
  sesion v7-v10 quedan en el escenario A (los doce meses), rehechas con el guion de `main`, y es
  desviacion aceptada hasta la rama siguiente.
- `Tests Currently Passing`: de 1251 a 1272 funciones (1919 a 1980 casos).
- Deuda: ninguna nueva en Technical Debt.
- Pendientes (informe §5): rehacer las filtradas de v7-v10 en B con el guion nuevo ya en `main`,
  que es el nuevo punto P de la Next Action; y `a18_buscar.py`, si se regenera su salida.
- Letra: la ultima cerrada era la v (`stable/F36v-sesion-04`); `w` libre en local y en `origin`.
- Tag: `stable/F36w-cuarentena-por-condicion`. El merge es
  `git rev-parse "stable/F36w-cuarentena-por-condicion^{commit}"`: su sha no existe hasta el merge,
  y el literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `ad4fd75`: apertura (encargo, contrato, Archivo 13) con la fase 0;
  - `8b5b7fc`: fase 1, la condicion, la fuente de (b) y los tests;
  - `5584d8b`: fase 2, antes y despues por video y las filtradas de sesion rehechas en A;
  - `7120217`: los hallazgos del revisor, con la CI 208 y su informe pegado;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux, empujada como `fix/cuarentena-por-condicion`:
  - run 208 (37241039661), 5584d8b: 1 failed, 1970 passed, 8 skipped;
  - run 209 (37244398309), 7120217: 1 failed, 1971 passed, 8 skipped.

  En los dos, el fallo es el UNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`, por el nombre `fix/`. El cierre borra
  `fix/cuarentena-por-condicion` de `origin`.
- Informe: `docs/validation/CUARENTENA-POR-CONDICION.md`, con las decisiones tras la fase 0, el
  informe del revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-cuarentena-por-condicion.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/cuarentena-por-condicion (consultor, 2026-10-04). Revisada: último commit 7120217, CI de Linux run 209 (37244398309) con el único fallo esperado, el de state check por el nombre fix/. Cópiala tal cual al informe y al registro del cierre en HISTORIA.
  >
  > TAG: stable/F36w-cuarentena-por-condicion. Antes de usarlo, comprueba en HISTORIA que la última letra es la v. Si no lo es, para y dímelo.
  >
  > DECISIONES QUE CIERRAN LA REVISIÓN
  > 1. La fuente de febrero en meses_reservados.yaml se queda como está, sin ADR.
  >    Por qué: no cambia qué se tapa, y «ciego, sin descargar» ya consta en CLAUDE.md. Déjalo declarado en el informe como desviación aceptada.
  > 2. Las filtradas de sesión en el escenario A son aceptables hasta la rama siguiente.
  >    Por qué: tapar de más no expone nada, y rehacerlas en B necesita el guion nuevo en main.
  >
  > HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
  > - importa · De Claude Code, no del revisor: en la primera medida de la fase 0, «set» suelto contaba como mes. Lección: toda medida de un filtro nuevo se compara con un caso negativo conocido antes de dar cifras.
  > - importa · Del revisor: el guion de la fase 0 importaba algo que la fase 1 eliminó, y la comprobación del contrato dejó de correr sin avisar. Lección para el revisor: después de cada fase que borra o renombra algo, correr la comprobación del contrato.
  > - Del consultor, nada que el revisor no viera.
  >
  > NEXT ACTION EN EL COMMIT DE ESTADO
  > Sustituye P por:
  > «P. Rama corta: rehacer con el guion de main las filtradas de sesión (v7–v10) en el escenario B. Medir antes con recuentos y marcas de tiempo, sin texto. Si algún ítem ev-* cae en un segmento que pasa a ocultarse, parar y avisar al consultor. Va antes de activar la sesión 4 (CUARENTENA-POR-CONDICION.md §5).»
  > No toques los demás puntos.
  >
  > RITUAL
  > Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
  > - registro y fila de ERRORES-RECURRENTES en la rama;
  > - merge y tag;
  > - commit de estado;
  > - make check sellado;
  > - push atómico de main y el tag;
  > - CI de main en verde;
  > - borrar trabajo/cuarentena-por-condicion en local y fix/cuarentena-por-condicion en origin.
  >
  > INFORME FINAL
  > Sha de main, tag y el sha al que apunta, run de la CI de main con su resultado, ramas que quedan y tamaño de PROJECT_STATE.

# Archivo 14 · PROJECT_STATE.md de main en f712650 (2026-10-04), al abrir trabajo/filtradas-escenario-b

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36w-cuarentena-por-condicion` (2026-10-04).

## Stable Main State
44f461d · merge de `trabajo/cuarentena-por-condicion` (tag `stable/F36w-cuarentena-por-condicion`): la cuarentena del texto deja de ser una lista fija de meses y tapa todo mes que no se pueda demostrar libre -sin dias en casos_ocultos ni en casos_reservados y fuera de knowledge/cases/meses_reservados.yaml (2026-02, 2026-03), la fuente nueva, SOLO ANADIR-; sin datos se tapan los doce (`cases.holdout.meses_libres`). Dos tramos de precaucion en v6; las filtradas de sesion v7-v10, en el escenario A hasta la rama siguiente (P). Sobre `stable/F36v-sesion-04` (eec79a0). Informe docs/validation/CUARENTENA-POR-CONDICION.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
44f461d · merge: la cuarentena del texto tapa todo mes que no se pueda demostrar libre (CUARENTENA-POR-CONDICION.md) · tag stable/F36w-cuarentena-por-condicion

## Tests Currently Passing
1272 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

P. Rama corta: rehacer con el guion de main las filtradas de sesión (v7–v10) en el escenario B. Medir antes con recuentos y marcas de tiempo, sin texto. Si algún ítem ev-* cae en un segmento que pasa a ocultarse, parar y avisar al consultor. Va antes de activar la sesión 4 (CUARENTENA-POR-CONDICION.md §5).

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 13 (2026-10-04).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 13 (2026-10-04).

# Next Action HECHA · P · sale de PROJECT_STATE.md en trabajo/filtradas-escenario-b (2026-10-04)

La hace esta rama, con el alcance que fijó el consultor: B medido en su sitio y no instalado (P2),
los tramos arreglados y el hueco documentado (segunda respuesta del consultor, punto 1, y punto 5:
«Y P se quita: pasa a HECHO con esta rama»; docs/validation/FILTRADAS-ESCENARIO-B.md). Lo que queda
pasa a Q. Su texto literal en PROJECT_STATE.md:

P. Rama corta: rehacer con el guion de main las filtradas de sesión (v7–v10) en el escenario B. Medir antes con recuentos y marcas de tiempo, sin texto. Si algún ítem ev-* cae en un segmento que pasa a ocultarse, parar y avisar al consultor. Va antes de activar la sesión 4 (CUARENTENA-POR-CONDICION.md §5).

# Registro de cierre · `trabajo/filtradas-escenario-b` (2026-10-04)

- Orden de cierre del consultor del 2026-10-04, ejecutada a mano siguiendo `RITUAL.md`: llegó en un
  texto pegado, y la skill `cerrar-rama` solo la invoca el usuario.
- **Punto P de la Next Action, con el alcance que fijó el consultor:**
  - las filtradas de sesión v7–v10 se midieron en el escenario B con el guion de `main`, y B no se
    instaló (parada P2); A sigue instalada;
  - v9 en B es byte a byte la de ANTES (`f7529459…a027b`);
  - se registraron 8 tramos no citables (solo añadir): 7 de v9, que completan los de la sesión 03
    con el segundo de margen, y el bloque de B de v10 de 1:55:27;
  - el ancla de `ev-v9-003456-9ef48fb5` se midió con la localización de `knowledge validate` y cae
    fuera del bloque. El tramo de 0:34:44 se queda sin margen por la condición del ancla, y la
    ventana del ítem se corrige en R;
  - quedó escrito el criterio de los límites de un tramo (`SESION-DE-PREGUNTAS.md`);
  - quedó documentado el hueco: las filtradas no aplican los tramos, y es Q.
- `HOLDOUT-EXPOSICIONES.md`: dos filas que complementan la del 2026-10-04 (v10), sin exposición nueva
  y sin quemar.
- Q y R entran en la Next Action, y P salió en la rama («Next Action HECHA · P», arriba).
- `Tests Currently Passing`: de 1272 a 1278 funciones (1980 a 1986 casos), con
  `tests/unit/test_tramos_de_sesion.py`.
- Deuda: ninguna nueva en Technical Debt; lo pendiente es Q y R.
- Letra: la última cerrada era la w (`stable/F36w-cuarentena-por-condicion`); `stable/F36x-*` no
  existe ni en local ni en `origin`.
- Tag: `stable/F36x-filtradas-escenario-b`. El merge es
  `git rev-parse "stable/F36x-filtradas-escenario-b^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `bbd2da8`: apertura (encargo, contrato, Archivo 14) con la fase 0;
  - `dca3101`: B medido en su sitio; parada P2 y método de los tramos de v9;
  - `819676a`: segunda respuesta, criterio de tramos y parada por un ítem de v9;
  - `ffc518d`: tercera respuesta; la comprobación por marcas del ancla falla en (b);
  - `f50b680`: ancla con validate, 8 tramos, criterio, test y hueco (commit y push hechos a mano por
    Aleks: el clasificador del modo automático los bloqueó);
  - `e2ee6cc`: quinta y sexta respuestas; fila complementaria en HOLDOUT-EXPOSICIONES;
  - `c4bf89b`: informe del revisor, sus hallazgos y la fila de ERRORES-RECURRENTES;
  - `0f70cf1`: séptima respuesta; Q y R corregidos, A3 y A4 en HOLDOUT-EXPOSICIONES;
  - y el de este registro, que saca también el contrato.
- CI de Linux, empujada como `fix/filtradas-escenario-b`:
  - run 211 (37259081415), `f50b680`: 1 failed, 1977 passed, 8 skipped;
  - run 212 (37260857834), `e2ee6cc`: 1 failed, 1977 passed, 8 skipped;
  - run 213 (37262859430), `c4bf89b`: 1 failed, 1977 passed, 8 skipped;
  - run 214 (37265185287), `0f70cf1`: 1 failed, 1977 passed, 8 skipped.

  En todos, el fallo es el ÚNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`, por el nombre `fix/`. Los commits anteriores a `f50b680` no se
  empujaron. El cierre borra `fix/filtradas-escenario-b` de `origin`.
- Informe: `docs/validation/FILTRADAS-ESCENARIO-B.md`, con las siete respuestas del consultor, el
  informe del revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-filtradas-escenario-b.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/filtradas-escenario-b (consultor, 2026-10-04). Revisada: último commit 0f70cf1, CI de Linux run 214 (37265185287) con el único fallo esperado, el de state check por el nombre fix/. Cópiala tal cual al informe y al registro del cierre en HISTORIA.
  >
  > TAG: stable/F36x-filtradas-escenario-b. Antes de usarlo, comprueba en HISTORIA que la última letra es la w (stable/F36w-cuarentena-por-condicion) y que stable/F36x-* no existe ni en local ni en origin. Si algo falla, para y dímelo.
  >
  > DESVIACIONES ACEPTADAS (ya en el informe; aquí solo se confirman)
  > 1. B se midió y no se instaló: A se queda en su sitio hasta Q, porque una parada no se relaja después de ver el dato.
  > 2. El tramo que completa el de 0:34:44 de v9 no se registró: sería idéntico al original, por la condición del ancla. La ventana del ítem se corrige en R.
  > 3. Q tapará la línea visible del segundo de margen en 12 tramos: tapar de más no expone nada.
  >
  > HALLAZGOS PARA ERRORES-RECURRENTES
  > La fila ya está en la rama, con los hallazgos del consultor y el de la sesión que vio el revisor. Del consultor, nada más que el revisor no viera.
  >
  > NEXT ACTION EN EL COMMIT DE ESTADO
  > Q y R ya entraron con la rama; no los toques. Añade solo este punto, después de R:
  > «S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.»
  > Los demás puntos no cambian.
  >
  > RITUAL
  > Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
  > - registro del cierre en HISTORIA en la rama, con stable/<tag>^{commit};
  > - merge y tag;
  > - commit de estado: solo sustituye Current Branch, Current Feature, Stable Main State y Last Stable Commit, y añade el punto S;
  > - make check sellado;
  > - push atómico de main y el tag, en un solo comando. Si el clasificador lo bloquea, para y dame el comando con «!»;
  > - CI de main en verde antes de borrar nada;
  > - borrar trabajo/filtradas-escenario-b en local y fix/filtradas-escenario-b en origin.
  >
  > INFORME FINAL
  > Sha de main, tag y el sha al que apunta, run de la CI de main con su resultado, ramas que quedan y tamaño de PROJECT_STATE.

# Archivo 15 · PROJECT_STATE.md de main en 0bf71a2 (2026-10-05), al abrir trabajo/filtradas-con-tramos

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36x-filtradas-escenario-b` (2026-10-05).

## Stable Main State
5e486dc · merge de `trabajo/filtradas-escenario-b` (tag `stable/F36x-filtradas-escenario-b`): las filtradas de sesion v7-v10 medidas en el escenario B y NO instaladas (siguen en A hasta Q); 8 tramos no citables nuevos (7 de v9 con el segundo de margen, y el bloque de B de v10 de 1:55:27); el ancla de ev-v9-003456-9ef48fb5, medida con la localizacion de validate, fuera del bloque (su ventana se corrige en R); el criterio de los limites de un tramo, en SESION-DE-PREGUNTAS.md; el hueco (las filtradas no aplican los tramos), documentado y llevado a Q. Dos filas en HOLDOUT-EXPOSICIONES que complementan la del 2026-10-04, sin quemar. Sobre `stable/F36w-cuarentena-por-condicion` (44f461d). Informe docs/validation/FILTRADAS-ESCENARIO-B.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
5e486dc · merge: tramos de sesion completados, ancla de v9 medida y el hueco de las filtradas documentado (FILTRADAS-ESCENARIO-B.md) · tag stable/F36x-filtradas-escenario-b

## Tests Currently Passing
1278 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con un test sintético que rompa la guardia a propósito. Tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10 en B con los tramos, y comprobar que lo tapado es B más los tramos, y nada destapado frente a A dentro de un tramo (FILTRADAS-ESCENARIO-B.md). Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera. La aplicación de un tramo a la filtrada tapa un segmento solo si se solapa con el tramo más de 0 ms: un segmento que empieza exactamente donde termina un tramo queda visible. Test sintético con ese caso de borde (v9, 0:34:56; FILTRADAS-ESCENARIO-B.md). Se acepta que la regla de más de 0 ms tape el segmento visible que cae en el segundo de margen de un tramo (12 casos (9 de tramos anteriores y 3 de esta rama), FILTRADAS-ESCENARIO-B.md); el informe de Q da su recuento.

R. Rama corta: corregir por su régimen la ventana declarada de ev-v9-003456-9ef48fb5 (empieza 2 s antes de su ancla, sobre la cola de un segmento en cuarentena; FILTRADAS-ESCENARIO-B.md §4.1).

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 14 (2026-10-04).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 14 (2026-10-04).

# Next Action HECHA · Q · sale de PROJECT_STATE.md en trabajo/filtradas-con-tramos (2026-10-05)

La hace esta rama: las filtradas de sesion tapan los tramos no citables de su video (orden de
cierre del consultor del 2026-10-05; `docs/runbooks/RITUAL.md`, punto 3). Lo que queda de ella
(rehacer las filtradas de v7-v10 y comprobarlas) pasa a la fase 0 de la activacion de la sesion
4, en el punto E. Su texto literal en PROJECT_STATE.md:

Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con un test sintético que rompa la guardia a propósito. Tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10 en B con los tramos, y comprobar que lo tapado es B más los tramos, y nada destapado frente a A dentro de un tramo (FILTRADAS-ESCENARIO-B.md). Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera. La aplicación de un tramo a la filtrada tapa un segmento solo si se solapa con el tramo más de 0 ms: un segmento que empieza exactamente donde termina un tramo queda visible. Test sintético con ese caso de borde (v9, 0:34:56; FILTRADAS-ESCENARIO-B.md). Se acepta que la regla de más de 0 ms tape el segmento visible que cae en el segundo de margen de un tramo (12 casos (9 de tramos anteriores y 3 de esta rama), FILTRADAS-ESCENARIO-B.md); el informe de Q da su recuento.

# Registro de cierre · `trabajo/filtradas-con-tramos` (2026-10-05)

- Orden de cierre del consultor del 2026-10-05, ejecutada a mano siguiendo `RITUAL.md`: llego en un
  texto pegado, y la skill `cerrar-rama` solo la invoca el usuario. Es el punto Q de la Next Action,
  hecho como tarea autonoma.
- **Lo que entra:**
  - `scripts/transcribir_sesion.py` tapa con `[NO CITABLE mm:ss–mm:ss]` todo segmento que se solape
    mas de 0 ms con un tramo de `tramos_no_citables.yaml` de su video. El borde de v9 (0:34:56)
    queda visible.
  - El video se declara con `--video`, obligatorio, y se comprueba por el sha256 del WAV del audio
    frente al `sha256_wav` de la transcripcion del corpus de ese video. Se midio igual en v7-v10.
  - Falla cerrado: sin video, con un video que no es sesion, con varios audios, con el fichero de
    tramos ausente, ilegible o invalido, o con un audio que no es del video, no escribe nada, ni la
    cruda, y sale con 2.
  - El registro da, sin texto, lo tapado por meses, por tramos y por ambos.
  - La skill `ingerir-sesion` pasa `--video` (solo esa linea de `.claude/`, autorizada).
- **Desviaciones aceptadas** (orden de cierre): `--video` obligatorio con su comprobacion; el cambio
  en `.claude/` limitado a ese comando; y el riesgo de un ffmpeg que no reprodujera el sha, que daria
  un falso rechazo y nunca un falso aceptado.
- `Tests Currently Passing`: de 1278 a 1301 funciones (1986 a 2019 casos), con
  `tests/unit/test_filtradas_con_tramos.py`.
- Deuda: ninguna nueva en Technical Debt. Lo que queda (rehacer las filtradas de v7-v10 y
  comprobarlas contra `FILTRADAS-ESCENARIO-B.md`) va a la fase 0 de la activacion de la sesion 4,
  en el punto E.
- Letra: la ultima cerrada era la x (`stable/F36x-filtradas-escenario-b`); `stable/F36y-*` no existe
  ni en local ni en `origin`.
- Tag: `stable/F36y-filtradas-con-tramos`. El merge es
  `git rev-parse "stable/F36y-filtradas-con-tramos^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `e9ce879`: apertura (encargo, contrato, Archivo 15) con la fase 0;
  - `bece406`: la regla de los tramos en el guion, los tests y las roturas;
  - `245a0fd`: el informe del revisor y sus hallazgos;
  - `dbd0f09`: la comprobacion del audio por el sha del WAV y la skill con `--video`;
  - `878b635`: la pasada corta del revisor;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux, empujada como `fix/filtradas-con-tramos`:
  - run 216 (37309388222), `bece406`: 1 failed, 2004 passed, 8 skipped;
  - run 217 (37312344759), `245a0fd`: 1 failed, 2004 passed, 8 skipped;
  - run 218 (37316869724), `dbd0f09`: 1 failed, 2010 passed, 8 skipped;
  - run 219 (37319081102), `878b635`: 1 failed, 2010 passed, 8 skipped.

  En todos, el fallo es el UNICO esperado (`RITUAL.md`): `state check` en
  `test_state_check_ok_on_real_repo`, por el nombre `fix/`. El cierre borra
  `fix/filtradas-con-tramos` de `origin`.
- Informe: `docs/validation/FILTRADAS-CON-TRAMOS.md`, con la respuesta del consultor, los dos
  informes del revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-filtradas-con-tramos.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/filtradas-con-tramos (consultor, 2026-10-05). Revisada: último commit 878b635, CI de Linux run 219 (37319081102) con el único fallo esperado, el de state check por el nombre fix/. Cópiala tal cual al informe y al registro del cierre en HISTORIA.
  >
  > TAG: stable/F36y-filtradas-con-tramos. Comprueba antes en HISTORIA que la última letra es la x y que stable/F36y-* no existe ni en local ni en origin. Si algo falla, para.
  >
  > DESVIACIONES ACEPTADAS
  > 1. --video obligatorio, comprobado por el sha256 del WAV del manifiesto de transcripción: falla cerrado y lo cubren tests de punta a punta.
  > 2. Cambio en .claude/ limitado al comando de la skill ingerir-sesion, autorizado por el consultor y comparado línea a línea por el revisor.
  > 3. Riesgo declarado: si otra versión de ffmpeg no reprodujera el sha, el guion rechazaría un audio bueno. Nunca aceptaría uno equivocado. Se verá en la fase 0 de la activación.
  >
  > HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
  > - importa · Del consultor: afirmó que SESION-04-EXTRACCION.md no tenía §4 por leer por el puente una copia de 861 líneas; en main tiene 1201. Lección: el puente puede dar ficheros viejos; antes de afirmar que falta algo en un fichero, se pide a Claude Code el recuento en git (git show main:<ruta> | wc -l).
  > - Del revisor: nada que el consultor viera y él no.
  >
  > NEXT ACTION EN EL COMMIT DE ESTADO (PROJECT_STATE está a 351 bytes del tope: escribe corto; si aun así se pasa, para y dímelo)
  > - Q sale, porque pasa a HISTORIA con este cierre.
  > - Al punto E (A-42) añade al final: «Antes de activarla, pregunta al trader a qué hora ve cerrar las velas de 4 horas en invierno (HOJA-ACTIVACION-S4, fuera del repo). La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee.»
  > - Añade después de S: «T. Rama corta trabajo/respuestas-ftmo: registrar la respuesta de FTMO del 2026-10-05 (ticket VDW-DPMWR-965) sin copiar el correo literal; prompt del consultor.»
  > - Los demás puntos no cambian.
  >
  > RITUAL
  > Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
  > - registro y fila de ERRORES-RECURRENTES en la rama;
  > - merge y tag;
  > - commit de estado;
  > - make check sellado;
  > - push atómico de main y el tag (si el clasificador lo bloquea, para y dame el comando con «!»);
  > - CI de main en verde;
  > - borrar trabajo/filtradas-con-tramos en local y fix/filtradas-con-tramos en origin.
  >
  > INFORME FINAL
  > Sha de main, tag y el sha al que apunta, run de la CI de main, ramas que quedan y tamaño de PROJECT_STATE.

# Archivo 16 · PROJECT_STATE.md de main en fffaa03 (2026-10-05), al abrir trabajo/ventana-ev-v9-003456

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36y-filtradas-con-tramos` (2026-10-05).

## Stable Main State
06adac1 · merge de `trabajo/filtradas-con-tramos` (tag `stable/F36y-filtradas-con-tramos`): las filtradas de sesion tapan con [NO CITABLE] los tramos no citables de su video (solape > 0 ms); `--video` obligatorio, comprobado por el sha256 del WAV frente al de la transcripcion; falla cerrado. Sobre `stable/F36x-filtradas-escenario-b` (5e486dc). Informe docs/validation/FILTRADAS-CON-TRAMOS.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
06adac1 · merge: las filtradas de sesion tapan los tramos no citables de su video, comprobado por el sha del audio (FILTRADAS-CON-TRAMOS.md) · tag stable/F36y-filtradas-con-tramos

## Tests Currently Passing
1301 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

R. Rama corta: corregir por su régimen la ventana declarada de ev-v9-003456-9ef48fb5 (empieza 2 s antes de su ancla, sobre la cola de un segmento en cuarentena; FILTRADAS-ESCENARIO-B.md §4.1).

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.

T. Rama corta trabajo/respuestas-ftmo: registrar la respuesta de FTMO del 2026-10-05 (ticket VDW-DPMWR-965) sin copiar el correo literal; prompt del consultor.

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**. Antes de activarla, pregunta al trader a qué hora ve cerrar las velas de 4 horas en invierno (HOJA-ACTIVACION-S4, fuera del repo). La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 15 (2026-10-05).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 15 (2026-10-05).

# Next Action HECHA · R · sale de PROJECT_STATE.md en trabajo/ventana-ev-v9-003456 (2026-10-05)

La hace esta rama: la ventana de ev-v9-003456-9ef48fb5 se corrigio por su regimen (orden de
cierre del consultor del 2026-10-05, punto 4; `docs/runbooks/RITUAL.md`, punto 3). Su texto
literal en PROJECT_STATE.md:

R. Rama corta: corregir por su régimen la ventana declarada de ev-v9-003456-9ef48fb5 (empieza 2 s antes de su ancla, sobre la cola de un segmento en cuarentena; FILTRADAS-ESCENARIO-B.md §4.1).

# Registro de cierre · `trabajo/ventana-ev-v9-003456` (2026-10-05)

- Orden de cierre del consultor del 2026-10-05, ejecutada a mano siguiendo `RITUAL.md`: llego en un
  texto pegado, y la skill `cerrar-rama` solo la invoca el usuario. Es el punto R de la Next Action.
- **Lo que entra:**
  - `ev-v9-003457-3e28e325` supersede a `ev-v9-003456-9ef48fb5`, con la ventana desde 0:34:57;
  - `ev-v10-010438-024f76b8` supersede a `ev-v10-010438-0d4e6798`, con la cita y la ventana
    recortadas antes del segmento 1058, que un tramo redondeado al segundo pisa;
  - los dos, por la via de `evidence new` en un anexo, sin que el texto pase por la sesion, con una
    primera pasada que la guardia rechazo;
  - el tramo de margen v9 0:34:44-0:34:57 (solo anadir);
  - A-46 cita el item nuevo de v9;
  - la condicion `ventana_no_citable` (la ventana de todo item activo no pisa un tramo ni un
    segmento que solape un tramo), en `knowledge validate`, `evidence new` y
    `evidence propose --check`;
  - recuadros en FILTRADAS-ESCENARIO-B, SESION-03 y SESION-04;
  - la medida de los segmentos visibles tapados por tramos redondeados (21 de cuarentena
    mecanica), para la fase 0 de E.
- Desviacion aceptada: A-42 nunca cito el item viejo de v10; anadirle el nuevo va con su
  activacion (punto E).
- `Tests Currently Passing`: de 1301 a 1309 funciones (2019 a 2027 casos).
- Deuda nueva en Technical Debt: nada avisa cuando la spec o las ambiguedades citan un item
  supersedido.
- Letra: la ultima cerrada era la y (`stable/F36y-filtradas-con-tramos`); `stable/F36z-*` no existe ni
  en local ni en `origin`.
- Tag: `stable/F36z-ventana-no-citable`. El merge es
  `git rev-parse "stable/F36z-ventana-no-citable^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `3667838`: apertura (encargo, contrato, Archivo 16) con la fase 0;
  - `809117b`: el tramo de margen, el item nuevo de v9, A-46, los recuadros y la parada en la
    condicion;
  - `41be086`: el item nuevo de v10 y la condicion activada, con sus tests y medidas;
  - `ce4f488`: el informe del revisor y sus hallazgos;
  - y el de este registro, que saca tambien el contrato.
- CI de Linux: ninguna; la rama no se empujo como `fix/`, porque no toca hooks, rutas ni nada que
  dependa de la plataforma (el informe y el revisor lo comprobaron). La CI corre en `main` tras el
  push.
- Informe: `docs/validation/VENTANA-EV-V9.md`, con las decisiones del consultor, el informe del
  revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-ventana-ev-v9-003456.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/ventana-ev-v9-003456 (consultor, 2026-10-05). Revisada: lista para cerrar.
  >
  > 1. Desviación de A-42: ACEPTADA. A-42 nunca citó ev-v10-010438-0d4e6798 (su evidencia es de v3, v4 y v9). Añadirle el ítem nuevo ev-v10-010438-024f76b8 toca al activarla en el punto E, no aquí. El error de la orden fue del consultor.
  >
  > 2. Tag: stable/F36z-ventana-no-citable. Antes de crearlo, comprueba en HISTORIA que la última letra cerrada es la y y que stable/F36z-* no existe ni en local ni en origin. Si la z ya está usada, para y dímelo.
  >
  > 3. Hallazgos del consultor para la fila de ERRORES-RECURRENTES, cada uno con su lección:
  >    a) IMPORTA · El consultor escribió en una orden que A-42 citaba el ítem de v10 sin leer ambiguedades.yaml. Claude Code lo midió y no lo aplicó. Lección (consultor): una referencia del repo se lee antes de ordenarla. Si no se puede leer, se escribe «verifica que…».
  >    b) IMPORTA · Los tramos no citables se registran con el inicio o el fin redondeados al segundo. Desde Q, el filtro tapa entero todo segmento que tocan, así que 21 segmentos visibles quedan tapados (1 en v7, 4 en v9 y 16 en v10), y una cita activa (v10) caía en uno de ellos. Nadie lo vio hasta que existió ventana_no_citable. Lección (revisor): cuando una rama cambia qué tapa un filtro, se mide qué ítems activos citan lo que pasa a quedar tapado.
  >    c) MENOR · FILTRADAS-ESCENARIO-B §4.3 afirmó sin medirlo que knowledge validate rechazaba esos ítems. Lección (revisor): lo que un informe dice que hace una comprobación se comprueba ejecutándola, no leyendo el informe.
  >
  > 4. En HISTORIA (registro del cierre, en la rama): R pasa a «Next Action HECHA · R» con su texto literal.
  >
  > 5. Commit de estado en main. Solo reemplaza las cuatro cabeceras y quita R del Next Action. Al punto E añade al final esta frase:
  >    «La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.»
  >    No toques Completed Features ni el Change Log. PROJECT_STATE tiene que seguir por debajo de 25.000 bytes.
  >
  > 6. Lo de siempre: push atómico de main y el tag, la CI de main en verde antes de borrar la rama, y luego borrar la rama local (no hay fix/ remota).
  >
  > 7. Informe final con:
  >    - sha de main;
  >    - el tag y a qué commit apunta;
  >    - el run de la CI de main, con tests pasados y saltados;
  >    - las ramas que quedan;
  >    - el tamaño de PROJECT_STATE.

# Archivo 17 · PROJECT_STATE.md de main en 54c69fe (2026-10-05), al abrir trabajo/respuestas-ftmo

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36z-ventana-no-citable` (2026-10-05).

## Stable Main State
f8b291c · merge de `trabajo/ventana-ev-v9-003456` (tag `stable/F36z-ventana-no-citable`): ev-v9-003457 y ev-v10-010438-024f76b8 corrigen por supersede las ventanas que pisaban un tramo no citable o un segmento que lo solapa; la ventana de todo item activo se comprueba en knowledge validate, evidence new y evidence propose --check. Sobre `stable/F36y-filtradas-con-tramos` (06adac1). Informe docs/validation/VENTANA-EV-V9.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
f8b291c · merge: la ventana de todo item activo no pisa lo no citable (VENTANA-EV-V9.md) · tag stable/F36z-ventana-no-citable

## Tests Currently Passing
1309 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.

T. Rama corta trabajo/respuestas-ftmo: registrar la respuesta de FTMO del 2026-10-05 (ticket VDW-DPMWR-965) sin copiar el correo literal; prompt del consultor.

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**. Antes de activarla, pregunta al trader a qué hora ve cerrar las velas de 4 horas en invierno (HOJA-ACTIVACION-S4, fuera del repo). La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee. La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).
- Nada avisa cuando la spec o las ambiguedades citan un item ev-* supersedido (medido el 2026-10-05, docs/validation/VENTANA-EV-V9.md).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 16 (2026-10-05).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 16 (2026-10-05).

# Technical Debt RESPONDIDA · sale de PROJECT_STATE.md en trabajo/respuestas-ftmo (2026-10-05)

La responde FTMO el 2026-10-05 en el ticket VDW-DPMWR-965, pregunta 10, sin cifra: no fija limites numericos de tamano, «sustancialmente mayor» depende del comportamiento historico del propio trader, y el riesgo fijo del 0,5 % desde el primer dia es el patron historico de la cuenta. No se repregunta (parafrasis del consultor; docs/validation/FTMO-REGLAS.md, recuadro del 2026-10-05). Encargo de `trabajo/respuestas-ftmo`, decision 3; docs/validation/RESPUESTAS-FTMO.md. No entra otra linea en su lugar. Su texto literal en «Technical Debt»:

- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP, CON RIESGO CONSTANTE, CUENTA COMO «substantially larger position sizes» (R17): el ticket VDW-DPMWR-965 no lo contesto el 2026-09-29; repreguntado el 2026-10-03, pregunta 10 del correo (docs/validation/FUENTES-FTMO.md).

# Next Action HECHA · T · sale de PROJECT_STATE.md en trabajo/respuestas-ftmo (2026-10-05)

La hace esta rama: la respuesta de FTMO del 2026-10-05 al ticket VDW-DPMWR-965 queda registrada sin
copiar el correo (orden de cierre del consultor del 2026-10-05, «NEXT ACTION EN EL COMMIT DE
ESTADO»; `docs/runbooks/RITUAL.md`, punto 3). Su texto literal en PROJECT_STATE.md:

T. Rama corta trabajo/respuestas-ftmo: registrar la respuesta de FTMO del 2026-10-05 (ticket VDW-DPMWR-965) sin copiar el correo literal; prompt del consultor.

# Registro de cierre · `trabajo/respuestas-ftmo` (2026-10-05)

- Orden de cierre del consultor del 2026-10-05, ejecutada a mano siguiendo `RITUAL.md`: llego en un
  texto pegado, y la skill `cerrar-rama` solo la invoca el usuario. Es el punto T de la Next Action.
  Un diagnostico previo, tras cerrarse la terminal por error, confirmo que no se habia ejecutado
  ningun paso del ritual (rama en `2bc23a1`, `main` = `origin/main` en `54c69fe`, sin tag F37a).
- **Lo que entra:**
  - en `docs/validation/FTMO-REGLAS.md`, un recuadro fechado con la respuesta de FTMO del
    2026-10-05 al ticket VDW-DPMWR-965, una fila por pregunta 1-10, en parafrasis del consultor y sin
    copiar el correo; «que cambia» dice «nada» en las diez;
  - A-54 y A-55: solo el campo `pregunta`, con su espejo en `docs/spec/ambiguedades.md`; siguen
    ABIERTAS, con la misma clase y bloqueante;
  - la linea de R17 sale de Technical Debt y pasa literal a HISTORIA, sin otra en su lugar;
  - en `docs/runbooks/RITUAL.md`, las dos lineas de antes del tag (mirar en HISTORIA el ultimo tag
    cerrado y que el nuevo no exista; agotadas las letras, el numero siguiente con la a) y que tras
    `stable/F36z` la serie sigue en `stable/F37a-<nombre>`;
  - dos anexos con su salida: `prueba_f37a.py` (el tag F37a frente a cada lector del formato, en un
    clon desechable) y `medir_freno_huso.py`.
- Desviacion aceptada: en A-54 y A-55 «respuesta pendiente» se sustituyo por la frase nueva en vez de
  anadirla, porque juntas el campo afirmaria algo falso; el resto del campo no cambia.
- `Tests Currently Passing`: no cambia (1309 funciones, 2027 casos).
- `PROJECT_STATE.md`: de 23.670 bytes en `main` a 23.611 en la rama; con T fuera, menos.
- Letra: la ultima cerrada era la z (`stable/F36z-ventana-no-citable`, registro de cierre de
  `trabajo/ventana-ev-v9-003456`); `stable/F37a-*` no existe ni en local ni en `origin`. Es el primer
  tag de la serie F37.
- Tag: `stable/F37a-respuestas-ftmo`. El merge es
  `git rev-parse "stable/F37a-respuestas-ftmo^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `64b6f60`: apertura (encargo, contrato, Archivo 17) con la fase 0;
  - `0e1457c`: la respuesta en FTMO-REGLAS.md, A-54 y A-55, R17 fuera de Technical Debt y las lineas
    de RITUAL;
  - `2bc23a1`: el informe del revisor y sus hallazgos;
  - y el de este registro, que saca tambien el contrato y T.
- CI de Linux: ninguna; la rama no se empujo como `fix/`, porque solo toca documentacion (ni
  `.claude/`, ni hooks, ni rutas). La CI corre en `main` tras el push.
- Informe: `docs/validation/RESPUESTAS-FTMO.md`, con la fase 0, la respuesta del consultor, el
  informe del revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-respuestas-ftmo.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/respuestas-ftmo (consultor, 2026-10-05). Revisada: último commit 2bc23a1, make check sellado con 2027 tests pasados. La rama solo toca documentación y no lleva fix/ ni CI de Linux. Cópiala tal cual al informe y al registro del cierre en HISTORIA. El diagnóstico tras cerrar la terminal confirmó que no se había ejecutado ningún paso del ritual.
  >
  > TAG: stable/F37a-respuestas-ftmo. Es el primero de la serie F37 (RITUAL.md, las dos líneas de esta rama). Comprueba antes que el último tag cerrado en HISTORIA es stable/F36z-ventana-no-citable y que stable/F37a-* no existe ni en local ni en origin. Si algo falla, para.
  >
  > DESVIACIÓN ACEPTADA
  > 1. En A-54 y A-55 se sustituyó «respuesta pendiente» por la frase nueva en vez de añadirla, porque juntas el campo afirmaría algo falso. El resto del campo no cambia.
  >
  > HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
  > - importa · Del consultor (ya en el §3 del informe): dio por existente en RITUAL.md una regla que solo estaba en las órdenes de cierre de F36y y F36z. Lección: antes de escribir en un encargo «junto a la regla X de <fichero>», se lee esa regla en el fichero; si no se puede leer, se escribe «comprueba si existe». La fase 0 lo detectó y paró, como debía.
  > - Del revisor: nada que el consultor viera y él no. Sus a-1, a-2, a-3 y b-1 están arreglados.
  >
  > NEXT ACTION EN EL COMMIT DE ESTADO
  > - T sale, porque pasa a HISTORIA con este cierre.
  > - Los demás puntos no cambian.
  >
  > RITUAL
  > Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
  > - registro del cierre y fila de ERRORES-RECURRENTES en la rama;
  > - merge y tag;
  > - commit de estado;
  > - make check sellado;
  > - push atómico de main y el tag (si el clasificador lo bloquea, para y dame el comando con «!»);
  > - CI de main en verde;
  > - borrar trabajo/respuestas-ftmo en local (no hay fix/ remota).
  > No toques .git/REBASE_HEAD: es un resto del 2026-09-23 y no hay ningún rebase en curso.
  >
  > INFORME FINAL
  > Sha de main, tag y el sha al que apunta, run de la CI de main, ramas que quedan y tamaño de PROJECT_STATE.
- T sale de `PROJECT_STATE.md` en este commit, en la rama, y no en el de estado: lo manda
  `RITUAL.md`, punto 3, porque su texto entra aqui en el mismo commit y en `main`, tras el tag,
  HISTORIA ya no puede cambiar. El resultado en `main` es el que pide la orden.

# Archivo 18 · PROJECT_STATE.md de main en 442a948 (2026-10-05), al abrir trabajo/guardias-citas

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F37a-respuestas-ftmo` (2026-10-05).

## Stable Main State
80eba7f · merge de `trabajo/respuestas-ftmo` (tag `stable/F37a-respuestas-ftmo`): la respuesta de FTMO del 2026-10-05 al ticket VDW-DPMWR-965, en un recuadro de FTMO-REGLAS.md sin copiar el correo; A-54 y A-55 la citan y siguen ABIERTAS; R17 sale de Technical Debt; RITUAL.md comprueba el tag antes de crearlo y, agotadas las letras, sigue en el número siguiente con la a. Sobre `stable/F36z-ventana-no-citable` (f8b291c). Informe docs/validation/RESPUESTAS-FTMO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
80eba7f · merge: la respuesta de FTMO del 2026-10-05 sin copiar el correo, y el tag tras agotar las letras (RESPUESTAS-FTMO.md) · tag stable/F37a-respuestas-ftmo

## Tests Currently Passing
1309 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**. Antes de activarla, pregunta al trader a qué hora ve cerrar las velas de 4 horas en invierno (HOJA-ACTIVACION-S4, fuera del repo). La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee. La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).
- Nada avisa cuando la spec o las ambiguedades citan un item ev-* supersedido (medido el 2026-10-05, docs/validation/VENTANA-EV-V9.md).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 17 (2026-10-05).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 17 (2026-10-05).

# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/guardias-citas (2026-10-06)

La paga G2: `tests/contract/test_tramos_fuente.py` exige `Fuente:` en todo commit que toque
`knowledge/corpus/tramos_no_citables.yaml` desde el ancla `c489685` (un sha, no una fecha), con
`commits_sin_fuente`; los commits anteriores al ancla no se tocan (`cfec50b`, `c489685` y `f443eee`
se listan en docs/validation/GUARDIAS-CITAS.md). Encargo de `trabajo/guardias-citas`, decision 4, y
respuesta del consultor a la fase 0, punto 5. No entra otra linea en su lugar. Su texto literal en
«Technical Debt»:

- Falta un test que exija Fuente: en todo commit que toque tramos_no_citables.yaml; los commits viejos no se tocan (docs/validation/SESION-04-EXTRACCION.md, orden de cierre).

# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/guardias-citas (2026-10-06)

La paga G1: `src/botsito/validation/citas_supersedidas.py`, conectada a `knowledge validate`,
niega en todo `knowledge/spec/` (tambien un fichero nuevo) un item ev-* supersedido que no comparte
valor escalar de YAML o linea de comentario con su sustituto. A-10 y A-18 pasaron a citar el item
vigente y el comentario de A-41 se reajusto; A-11 queda con una excepcion por par en G1 y entra en
su lugar una linea nueva de Technical Debt (respuesta del consultor del 2026-10-06 a la parada de
A-11, punto 3; docs/validation/GUARDIAS-CITAS.md §2, §3 y §8). Su texto literal en «Technical Debt»:

- Nada avisa cuando la spec o las ambiguedades citan un item ev-* supersedido (medido el 2026-10-05, docs/validation/VENTANA-EV-V9.md).

# Registro de cierre · `trabajo/guardias-citas` (2026-10-06)

- Orden de cierre del consultor del 2026-10-06, ejecutada a mano siguiendo `RITUAL.md`: llego en un
  texto pegado, y la skill `cerrar-rama` solo la invoca el usuario. Paga dos lineas de Technical
  Debt.
- **Lo que entra:**
  - G1 (`src/botsito/validation/citas_supersedidas.py`, conectada a `knowledge validate`): en todo
    `knowledge/spec/`, tambien un fichero nuevo, un item ev-* supersedido solo aparece en el mismo
    valor escalar de YAML o la misma linea de comentario que su sustituto; `EXCLUIDOS` vacia; UNA
    excepcion por par, (A-11, `ev-v4-001207-0c4ffd4b`), con caducidad;
  - G2 (`tests/contract/test_tramos_fuente.py`): `Fuente:` en todo commit que toque
    `tramos_no_citables.yaml` desde el ancla `c489685` (un sha); `commits_sin_fuente` gana el
    parametro opcional `que`, solo para el texto del mensaje;
  - A-10 (dos) y A-18 citan el sustituto de su item supersedido; el comentario de A-41 nombra en una
    linea al supersedido y a su sustituto;
  - las dos lineas de Technical Debt salen literales a HISTORIA, entra la de A-11 y el punto U de la
    Next Action;
  - la busqueda de candidatos para A-11 y lo que dice el repo de las fuentes documentales y del
    registro `fb-2026-09-09-sesion-01-76fd91ba` (informe §9.2-§9.3).
- Desviaciones aceptadas: G1 sin linea OK propia; la caducidad solo cuenta si el id esta
  supersedido en ese repo; la excepcion por par para A-11 en lugar de quitar el id (cambio de
  decision del consultor, §9).
- `Tests Currently Passing`: de 1309 a 1342 funciones (2027 a 2060 casos).
- Letra: la ultima cerrada era la a de F37 (`stable/F37a-respuestas-ftmo`); `stable/F37b-*` no existe
  ni en local ni en `origin`.
- Tag: `stable/F37b-guardias-citas`. El merge es
  `git rev-parse "stable/F37b-guardias-citas^{commit}"`: su sha no existe hasta el merge, y el
  literal queda en `Last Stable Commit` de `PROJECT_STATE.md`.
- Commits de la rama:
  - `2c22b15`: apertura (encargo, contrato, Archivo 18) con la fase 0;
  - `f48e912`: G2, G1 escrita sin conectar, A-10 y A-18 con el item vigente;
  - `44f4336`: el comentario de A-41 y la parada en A-11;
  - `d69aabd`: G1 conectada con la excepcion por par para A-11;
  - `65c3968`: el informe del revisor y sus hallazgos;
  - y el de este registro, que saca tambien el contrato y anade U a la Next Action.
- CI de Linux, por `fix/guardias-citas` (G2 lee la historia de git):
  - run 37481648537 sobre `d69aabd`: `failure` con el unico fallo esperado,
    `test_state_check_ok_on_real_repo` por el nombre `fix/` (1 failed, 2051 passed, 8 skipped);
  - run 37490820668 sobre `65c3968`: el mismo resultado (1 failed, 2051 passed, 8 skipped).
  La CI de `main` corre tras el push.
- Informe: `docs/validation/GUARDIAS-CITAS.md`, con la fase 0, las tres respuestas del consultor, el
  informe del revisor y la orden de cierre. Encargo: `docs/encargos/trabajo-guardias-citas.md`.
- La orden de cierre, tal cual:

  > Modelo: el que tengas · Esfuerzo: medio
  >
  > Orden de cierre de trabajo/guardias-citas (consultor, 2026-10-06). Revisada: último commit 65c3968, make check sellado con 2060 tests pasados, CI de Linux en fix/guardias-citas run 37481648537 (d69aabd) y run 37490820668 (65c3968), ambos con el único fallo esperado, el de state check por el nombre fix/. Cópiala tal cual al informe y al registro del cierre en HISTORIA, con los dos runs.
  >
  > TAG: stable/F37b-guardias-citas. Comprueba antes en HISTORIA que el último tag cerrado es stable/F37a-respuestas-ftmo y que stable/F37b-* no existe ni en local ni en origin. Si algo falla, para.
  >
  > DESVIACIONES ACEPTADAS
  > 1. G1 no escribe línea OK propia, solo ERROR, como ventana_no_citable. Ampliar test_historial_sin_git habría sido tocar una guardia existente, y un test aparte comprueba que knowledge validate falla cuando falla G1.
  > 2. La caducidad de la excepción solo cuenta como «sin uso» si el id está supersedido en ese repo, para no tocar los tres tests existentes que montan un knowledge/ mínimo. El test sobre el repo real, reforzado por el revisor, la vigila.
  > 3. Cambio de decisión del consultor sobre A-11, declarado en §9: excepción visible por par en lugar de quitar el id.
  >
  > HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
  > - importa · De la rama: A-11 figura RESUELTA y su respaldo citable no contiene el momento del stop; lo que lo decía estaba en un ítem supersedido. Lección: al supersedir un ítem que recorta su cita, se mira qué ambigüedades y reglas lo citan y si el sustituto sigue sosteniéndolas; desde hoy G1 lo hace saltar.
  > - menor · De la rama: la afirmación de un ítem puede decir más que su cita y nada lo mide (§8.3).
  > - Del revisor: nada que el consultor viera y él no.
  >
  > NEXT ACTION (donde lo mande RITUAL.md punto 3)
  > Añade después de S: «U. Pendiente del consultor: qué respalda A-11, que hoy va con excepción en G1 (GUARDIAS-CITAS.md §9.2 y §9.3), y si se mide que la afirmación de un ítem no diga más que su cita (§8.3).» Los demás puntos no cambian.
  >
  > RITUAL
  > Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
  > - registro del cierre y fila de ERRORES-RECURRENTES en la rama;
  > - merge y tag;
  > - commit de estado;
  > - make check sellado;
  > - push atómico de main y el tag (si el clasificador lo bloquea, para y dame el comando con «!»);
  > - CI de main en verde;
  > - borrar trabajo/guardias-citas en local y fix/guardias-citas en origin.
  > No toques .git/REBASE_HEAD.
  >
  > INFORME FINAL
  > Sha de main, tag y el sha al que apunta, run de la CI de main, ramas que quedan y tamaño de PROJECT_STATE.

# Archivo 19 · PROJECT_STATE.md de main en 25469ff (2026-10-06), al abrir trabajo/reloj-invierno

# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F37b-guardias-citas` (2026-10-06).

## Stable Main State
fe37973 · merge de `trabajo/guardias-citas` (tag `stable/F37b-guardias-citas`): G1, en `knowledge validate`, niega en todo knowledge/spec/ un item ev-* supersedido que no comparte valor o linea de comentario con su sustituto (una excepcion por par, A-11); G2 exige Fuente: en todo commit que toque tramos_no_citables.yaml desde c489685. Sobre `stable/F37a-respuestas-ftmo` (80eba7f). Informe docs/validation/GUARDIAS-CITAS.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
fe37973 · merge: G1, ningun item supersedido citado en knowledge/spec/, y G2, Fuente: en los tramos (GUARDIAS-CITAS.md) · tag stable/F37b-guardias-citas

## Tests Currently Passing
1342 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`), en este orden:

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos.

U. Pendiente del consultor: qué respalda A-11, que hoy va con excepción en G1 (GUARDIAS-CITAS.md §9.2 y §9.3), y si se mide que la afirmación de un ítem no diga más que su cita (§8.3).

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**. Antes de activarla, pregunta al trader a qué hora ve cerrar las velas de 4 horas en invierno (HOJA-ACTIVACION-S4, fuera del repo). La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee. La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).
- A-11 RESUELTA cita un ítem supersedido; su respaldo citable no dice el momento del stop; excepción en G1 hasta que decida el consultor (docs/validation/GUARDIAS-CITAS.md §8).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos. Desde `trabajo/ajustes-cierre` (2026-10-01) el cierre de una rama NO anade
aqui nada: lo cerrado va al `# Registro de cierre` de HISTORIA, en la rama (docs/runbooks/RITUAL.md).
— ninguna desde el Archivo 18 (2026-10-05).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. El cierre de
una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al registro de HISTORIA.
— ninguna desde el Archivo 18 (2026-10-05).
