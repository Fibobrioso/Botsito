# Encargo · trabajo/recorrida-construccion

Dado por Aleks (consultor) el 2026-10-27, en un solo mensaje. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Encargo del consultor (2026-10-27) · trabajo/recorrida-construccion · tramo R4 (entrada R4.1 de la hoja de ruta, lo que queda; V y F de la Next Action)
>
> RAMA Y BASE
> - Rama nueva: trabajo/recorrida-construccion, desde main 88f97f7 (commit de estado sobre el merge d843dbc del tag stable/F38f-activar-sesion-05-motor; CI de main en verde según el cierre, run 40537113754: compruébala como manda abrir-rama, paso 1, sin guion ni bucle, y que es del sha de main). Si algo no cuadra, para y dímelo.
> - Ábrela con la skill abrir-rama (su paso 1 entero, ninguna otra rama), contrato con tramo R4 y artefacto docs/validation/RECORRIDA-CONSTRUCCION.md; la carpeta docs/validation/anexos/RECORRIDA-CONSTRUCCION/ nace en la fase 1 con su README. Recorrido: abrir-rama, fase-cero y entregar-rama; si este encargo y ellas chocan, ganan ellas y lo dices. Cópiate este encargo tal cual a docs/encargos/trabajo-recorrida-construccion.md.
> - Revisa /model antes de empezar: Fable 5.1, esfuerzo alto. Las corridas son largas: si las lanzas en segundo plano, Claude Code tiene que estar arrancado con CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 (CLAUDE.md, «Trampas medidas»); si no lo está, córrelas en primer plano o dímelo.
>
> OBJETIVO
> Correr por primera vez la corrida que cuenta por ADR-0070 §3 (arnés simulado sobre toda la construcción vigente, sin ninguna opción fuera de la lista cerrada), dejar en el repo su veredicto literal y su diff contra la línea base, repetir la corrida con la cuenta diaria para clasificar, y sacar de las dos lo que la sesión 6 necesita: los días en que el bot opera y el trader no (S-14) y las entradas que se llenan antes de que la alternancia exista (ACTIVAR-SESION-05-MOTOR.md §0.b.8; dibujo 3 de S-15).
>
> QUÉ NO CAMBIA
> - Nada de src/, tests/, knowledge/, el Makefile ni .claude/. Ningún parámetro, ninguna regla, ninguna decisión del motor, del bróker simulado, de la cuenta ni del freno. La corrida que cuenta corre sobre el código de main tal cual. Si para algo de este encargo hiciera falta tocar src/, PARADA.
> - criterio_fidelidad.yaml no se toca (ni umbrales, ni tolerancias, ni construccion ni su orden).
> - Ninguna ambigüedad se abre ni se cierra; A-35 y A-44 siguen bloqueantes y ABIERTAS; ADR-0083 sigue PROVISIONAL.
> - Los informes cerrados de docs/validation y las líneas base existentes no se editan. CABLEADO-SIMULADOR-LINEA-BASE.txt es evidencia inmutable.
> - La Next Action y la hoja de ruta no se tocan en la rama: sus líneas se preparan en el informe para el commit del contrato. De PROJECT_STATE.md solo lo que abrir-rama y state check exigen (hoy 22.924 bytes: verifícalo con wc -c).
>
> LO QUE SE PUEDE MIRAR Y LO QUE NO (léelo antes de correr nada)
> - Antes de leer casos dev, casos_reservados(repo) por recuento sobre los cuatro meses de construcción, declarado el mismo día (CLAUDE.md, «Material de DESARROLLO»).
> - Se mira, y va al informe: lo que el arnés escribe sobre los días dev de construcción (enero del 2 al 30, abril, julio del 1 al 17 y agosto de 2026): cobertura, precisión, parejas, embudo, órdenes, rechazos, peticiones, la curva y el veredicto de la cuenta, por mes y por día. Las fechas de días dev de construcción se escriben.
> - No se mira nada de mayo ni de ningún mes de medida o reservado: el arnés ya se niega y no se rodea. Ni marzo, ni febrero, ni septiembre, ni diciembre, ni julio del 18 en adelante, ni el corpus del trader (xlsx, vídeos, fotogramas, transcripciones). Los casos dev ya ingeridos sí se leen.
> - El calentamiento del arnés lee el mes anterior entero (engine/arnes.py, _mes_anterior): marzo para abril y junio para julio, que tienen días reservados, y julio entero para agosto; enero no tiene mes anterior (no hay M1 de 2025-12; ADR-0079). Ningún guion, tabla, informe ni mensaje de commit imprime una vela, una H4, un pivote de M15, un nivel, un precio, un instante ni una fecha anteriores al día dev al que pertenecen: aplica la regla «(antes del dia)» de anexos/VISOR-CONSTRUCCION/comun_visor.py y traza_por_cierre.py. Ojo con el primer día de abril y de julio: su primera H4 y su pivote tomado pueden venir del día de calendario anterior. Precedente: en R3.1 un guion imprimió una H4 del calentamiento con su fecha y un día de junio salió del holdout (ADR-0041, CORRIDA-CONSTRUCCION.md §11).
> - Ninguna cifra de esta rama fija ni cambia un valor (PROJECT_STATE, «Reglas vivas»: los parámetros no se optimizan contra resultados), ni las lecturas DEFAULT_AMBIGUOUS, ni el umbral (ADR-0070 §4).
>
> LO QUE SE DECIDE ANTES DE CORRER (va al informe, §0, en el commit de la fase 0; DECISIÓN DEL CONSULTOR, 2026-10-27, salvo lo que cita su ADR)
> 1. La corrida 1 de abajo es la que cuenta por ADR-0070 §3 (NOTA del 2026-10-26). Su línea «habilita medir el conjunto de medida (2026-05) (ADR-0070): …» se copia literal al informe.
> 2. Si dice «no»: se sigue construyendo, mayo no se toca y el umbral no cambia (ADR-0070 §4).
> 3. Si dice «sí»: PARADA, y nada de mayo. Por ADR-0070 §6, un «sí» habilita la rama de medida, con su propio ADR, y no la sustituye. Qué hace esa rama con A-35 y A-44 bloqueantes ABIERTAS y con los parámetros DEFAULT_AMBIGUOUS lo decido en ese ADR, antes de medir.
> 4. La clasificación por patrones se hace sobre la corrida 2 (cuenta diaria), como en R3.1; la corrida 1 da el veredicto y el camino de la cuenta, y también se clasifica, solo como contexto.
> 5. La lista «Entradas antes de la alternancia» (§0.b.8) es: cada orden LLENADA del bot cuyo llenado ocurrió con menos de dos zonas de control formadas desde la toma de su escenario, que es donde muerde RN-009 (ADR-0076 §2 y su NOTA; ADR-0085 §4). Por cada una, dos columnas: cuántas zonas había al llenar (0 o 1) y dónde estaba la orden (el punto de la referencia, el primer punto formado tras la toma, o un punto posterior al que la reubicó RN-006). Así entran S-10 (reubicada y llenada con 0 zonas) y S-10b (llenada con 1).
>
> AUTORIZACIÓN EXPRESA
> Se autoriza ejecutar uv run botsito motor arnes solo con los tres comandos de la fase 2, escritos exactamente así, y el guion de la fase 1 (f) con el comando literal que fijes en la PARADA y yo apruebe. Ningún otro comando del arnés ni del visor sin preguntármelo en una PARADA. El runbook ACTIVAR-A35-A44.md §5 manda además un motor visor --caso: en esta rama no se abre el visor, y eso va como desviación declarada del runbook. Las corridas y el guion nunca a la vez que make check; si una muere por memoria, no la relances sin decírmelo. Si la guardia o el clasificador niegan algo, no lo reescribas para esquivarlos: PARADA con el comando exacto y lo lanzo yo con «!».
>
> FASE 0 · INVENTARIO SIN TOCAR NADA (skill fase-cero, con el informe de la fase 0 commiteado como ella manda) → PARADA
> Lee código y documentos; no corras el arnés todavía. Cada punto con fichero:línea:
> a) Que con los comandos de la fase 2 la corrida 1 usa solo opciones de OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA (engine/arnes.py) y que su perfil y su fase efectivos son perfil_para_medir y la primera del perfil; que --diagnostico-a35 y --diagnostico-a44 se rechazan hoy (DiagnosticoRechazadoError, TopeRechazadoError) y que el motor no necesita ningún --diagnostico-*. Y el nombre real que escribirá la corrida 2 (nombre_etiquetado).
> b) Ticks: que cada día dev de los cuatro meses tiene ticks en sus manifiestos, y las horas perdidas que cubre el respaldo M1 (R3.1 contó 18, 17 dentro de sesiones; verifícalo). Si algún día dev no tiene ticks, PARADA: no se corre con --depuracion.
> c) Calentamiento: qué mes anterior carga cada mes hoy (arriba). Propón la fila de HOLDOUT-EXPOSICIONES del día por recuento, nunca por fechas, como las del 2026-10-14, 2026-10-17 y 2026-10-18, con línea propia para el guion de f), y que remita a las filas de lo que cada make check ya lee (2026-10-14 y 2026-10-27).
> d) Recuentos de partida contados en el repo: días dev y operaciones del trader por mes. Qué viene de vídeo, según ACTIVAR-SESION-05.md §0.b.7, por día donde haga falta: enero no; abril, solo un día grabado; julio, «sí, según el trader», sin comprobar hasta T; agosto, sus casos dev siguen saliendo del xlsx hasta que llegue la exportación del backtest en vídeo (NA:Q). Verifícalo.
> e) patrones.py de anexos/CORRIDA-CONSTRUCCION/ corta cada línea por «] » (patrones.py:57-58), y las líneas «Por sesion» llevan «] » en su propio cuerpo (arnes.py:319): sobre una salida sin rótulo, el sesgo queda en «?» y todo cae en P1 sin aviso. Mídelo. La copia va a anexos/RECORRIDA-CONSTRUCCION/ cortando el rótulo solo si la línea empieza por «[DIAGNOSTICO» (como comun_visor.py), con las mismas reglas literales: ni una regla se ajusta. Con un test de humo sobre una línea «Por sesion» real con rótulo y otra sin él, que rompa con la lectura vieja.
> f) La lista de la decisión 5: cómo se obtienen, para cada orden llenada, las zonas formadas desde la toma al llenar y dónde estaba la orden, con lo que dan la salida («Diferencias por operacion», «Ordenes», «Rechazos por motivo»; ninguna da las zonas) y la traza del motor. Mi opción por defecto: un guion en anexos/RECORRIDA-CONSTRUCCION/ que reuse estructura_m1.zonas_de_control y las funciones de engine/zonas.py sobre las M1 de los días dev, siguiendo traza_por_cierre.py pero sin el Diagnostico fijo de comun_visor.py (hoy se rechaza) y sin comparar contra salidas viejas. Si corre el motor día a día con la cuenta reiniciada, reproduce la corrida 2 y no la 1: dilo, y comprueba que sus órdenes llenadas coinciden una a una con las de la «Ordenes» de la corrida 2. Si solo se puede tocando src/, o la guardia niega el guion por nombrar data/, PARADA con la alternativa; no se rodea.
> g) La línea base: CABLEADO-SIMULADOR-LINEA-BASE.txt cubre abril y agosto (42 días, 77 operaciones del trader) con un motor que no daba ninguna operación, y no tiene las secciones de diferencias, órdenes, rechazos ni peticiones. Mide su fecha de entrada en git y di qué secciones del diff son comparables (CONJUNTO, operaciones del trader, el embudo de sesgo y «RN-003 al abrir» de abril y agosto) y cuáles cambian por construcción. Quién la nombra como vigente: R3.1 (respuesta a la PARADA de la fase 0, punto 5: hasta que A-35 y A-44 tuvieran valor) y ACTIVAR-A35-A44.md §5 y §5.1; busca más sobre rutas literales (tests/, src/, scripts/, docs/runbooks/, docs/validation/*.md). Mi opción por defecto: la salida de la corrida 1 pasa a ser la línea base vigente tal como queda en anexos, sin copia, y ACTIVAR-A35-A44.md gana una NOTA al principio de §5 que lo diga y declare la desviación del visor (contrato ampliado a ese runbook, solo la NOTA).
> h) Herencias, con grep sobre rutas literales: R4.1 y R4.2 de HOJA-DE-RUTA.md; ACTIVAR-A35-A44.md §5.1; ACTIVAR-SESION-05.md §3 (S-14) y §5; ACTIVAR-SESION-05-MOTOR.md §0.b.8, §2 y §3; las NOTAS de ADR-0076 §2 y de ADR-0085 §4 («la re-corrida lo mira»). Cualquier otra que nombre «la re-corrida».
> i) Lo que el arnés hace ahora y antes no, para medirlo en el informe: RN-020 evaluado (perdida_trader_* bajo A-44, con la magnitud DEFAULT_AMBIGUOUS y el huso de reinicio que toma; tope_trader.py), ADR-0086 (retira la pendiente al llegar al tope), RN-036 con racha_perdidas_reinicio = tras_la_detencion, RN-037, y detenido_por_tope y detenido_por_cartuchos en el embudo. Y la lista, del registro, de los parámetros DEFAULT_AMBIGUOUS con los que corre la corrida que cuenta, con su ambigüedad. Di también qué reinicia la cuenta diaria cada día además del saldo (la racha, el seguidor del tope; cableado.py).
> j) Tiempo y memoria esperados: PUNTO-USADO.md §4 dio entre 364 y 504 s y unos 632-634 MiB por corrida con el motor de entonces, y ACTIVAR-SESION-05 §0.b.2 midió solo abril con el de ahora (171,5 s, 235 MiB). Di si todo cabe en una sesión.
> PARADA con todo eso.
>
> FASE 1 · LA FILA DE EXPOSICIONES Y LOS GUIONES (con lo que decida en la PARADA)
> - La fila de HOLDOUT-EXPOSICIONES del día, ANTES de correr nada, en su propio commit, junto con docs/validation/anexos/RECORRIDA-CONSTRUCCION/README.md (qué es cada fichero y los comandos literales).
> - El guion de f) y la copia de patrones.py, cada uno con su test de humo sobre salidas sintéticas que rompa en los dos sentidos: una llenada con 0 zonas y otra con 1 salen en la lista con su columna; una con 2 o más zonas, no; una reubicada sale como reubicada. Los guiones viven en anexos y no los recoge make check: di cómo se corre su prueba y pega su salida.
> - make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre los ficheros tocados.
>
> FASE 2 · LAS CORRIDAS
> Sin --meses, sobre el código commiteado:
> 1. La que cuenta, cuenta arrastrada:
>    uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt
> 2. La de clasificar, cuenta diaria:
>    uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.txt
> 3. La 1 repetida con --salida en tu carpeta temporal, fuera del repo, y comparada con diff contra la commiteada; si no sale idéntica, PARADA. Borra la copia.
> Después, el guion de f) con su comando aprobado. Copia al informe las líneas TIEMPO y MEMORIA de cada corrida y el nombre final de cada fichero tal cual. Si alguna sale con exit distinto de 0, pide días fuera de la construcción o necesitara --depuracion, PARADA con el error literal.
> Y el diff de la línea base, a fichero:
>    diff docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION/diff-linea-base.txt
> (diff sale con código 1 cuando hay diferencias: no es un fallo). Si la guardia niega la redirección, PARADA con el comando.
>
> EL INFORME docs/validation/RECORRIDA-CONSTRUCCION.md
> - §0: lo que se decide antes de correr, con su fecha, y la fase 0.
> - Por corrida y por mes: operaciones del trader, puntuables del bot, parejas, cobertura y precisión. De la 1: la línea de veredicto literal; el veredicto de la cuenta sobre el tramo, el día y la regla en que la cuenta corta el tramo si lo corta; y las peticiones (total y máximo diario frente al límite de 2000 de FTMO, y si saltó algún umbral del freno de ADR-0067, que siguen PROVISIONALES bajo A-54), como dato informativo, igual que en R3.1. Que el tramo no es continuo (enero, y de abril a agosto con huecos) y que su curva es indicativa, como dijo R3.1.
> - Lo de i): cuántas sesiones detiene RN-020 y con qué regla, cuántas órdenes retira ADR-0086, cuántas veces actúan RN-036 y RN-037, y la lista de parámetros DEFAULT_AMBIGUOUS con los que corrió.
> - El diff contra la línea base, resumido por sección (qué es comparable y qué cambia por el motor o por la construcción más amplia), con el fichero entero en anexos.
> - Los patrones T0 y P1 a P7 de las dos corridas por mes, con la copia arreglada de patrones.py, y como contexto, nunca como referencia, los de PUNTO-USADO (anexos/PUNTO-USADO/patrones.txt y patrones-arrastrada.txt), con qué cambios del motor desde entonces los separan (ADR-0084 a 0086, RN-037, A-35 y A-44 con valor, la racha tras la detención, la caja entera). Sin ajustar nada para acercarlos. Las filas que tocan una hora perdida, marcadas como posible M.
> - El embudo por mes y los rechazos por motivo de las dos corridas.
> - La lista «Entradas antes de la alternancia» (decisión 5), por día y sesión, con sus dos columnas, su patrón (T0, P5, P6), su resultado en R y si la empareja el trader. Sin conclusiones: es para el dibujo 3 de S-15, y RN-009 no cambia.
> - La lista «Para S-14»: de la corrida 2, cada sesión de P6 (el bot opera y el trader no), por día y sesión, con el primer hecho del camino del bot, su resultado en R, si la cuenta arrastrada de la corrida 1 llega a esa sesión o la corta antes, y si ese día viene de vídeo (por día en abril; «según el trader» en julio). Los días los elijo yo al preparar la hoja de la sesión 6.
> - Encargo frente a lo hecho punto por punto con evidencia, desviaciones declaradas (entre ellas, la del visor del runbook), comandos literales ejecutados y las exposiciones del día.
>
> PARADA 2 · ENTREGA PARA MIRAR
> Commitea las salidas, el diff, los guiones y el informe hasta aquí y para. Yo leo y decido: si hay que clasificar algún patrón nuevo, días en el visor (no lo abras antes) y qué va a la hoja de la sesión 6.
>
> LAS LÍNEAS DEL CIERRE (prepáralas en el informe, medidas)
> - Next Action: V sale (R4.1 HECHA) y entra en HISTORIA bajo «# Next Action HECHA · V · …», con su texto literal (RITUAL.md, punto 3); F pasa a «La rama corta de la cuarentena por condición (Technical Debt, PRIORITARIA) antes de ingerir la sesión 6; la preparación de la sesión 6 (R4.2); R6a en los huecos.», comprobado contra test_hoja_de_ruta (la palabra de dependencia seguida de una letra suelta que no esté viva; SESGO-H4-COLOR.md §1.h, punto 2).
> - Hoja de ruta: R4.1 HECHA con su estado; R4.2 sin la re-corrida en «Depende de», con los recuentos de las dos listas en «Qué es»; NA:V fuera de los Refs de R4.1 y R4.2.
> - ADR-0070 §3: una NOTA fechada (el cuerpo no se toca) con el veredicto literal de la corrida 1; contrato ampliado al ADR solo para eso, en un commit propio, si la PARADA 2 lo aprueba.
> - Las líneas de la línea base que salgan de g).
> - PROJECT_STATE.md lo más corto posible y por debajo de 23.000 bytes con las líneas aplicadas (orden del consultor para este cierre; el tope del test es 25.000): mídelo con wc -c sobre una copia.
> - Hallazgos para ERRORES-RECURRENTES. Uno ya lo pongo yo: el encargo pedía clasificar con patrones.py una salida sin rótulo, y su lectura por «] » daba un P1 falso sin error; lo vio el auditor del consultor. Lección: un guion de anexos escrito para salidas rotuladas se prueba sobre una salida sin rótulo antes de reutilizarlo.
>
> REGLAS DE SIEMPRE
> - Si la rama cambiara el Makefile, la guardia niega todo make: no debe cambiarlo. Los pushes que niegue el clasificador los lanzo yo con «!». La CI se mira sin guion ni bucle que espere.
> - Toda exposición, el mismo día en HOLDOUT-EXPOSICIONES. Ningún texto commiteado lleva fechas de días reservados ni nada anterior al día dev al que pertenece.
> - Las búsquedas, sobre rutas literales, nunca sobre la raíz.
> - CI de Linux: no toca .claude/, hooks, rutas ni código de plataforma, así que no hace falta fix/. Si algo lo tocara, dilo en la PARADA.
>
> INFORME Y REVISOR
> Revisor (opus) sobre la rama, con estos alcances: (1) que la corrida 1 usó solo opciones de la lista cerrada, su salida no lleva rótulo DIAGNOSTICO y el veredicto del informe es el literal de la salida; (2) que nada de src/, tests/, knowledge/ ni .claude/ cambia (git diff main --stat); (3) que las tablas del informe dicen lo que dicen las salidas, comprobado a mano en tres filas de cada mes, en tres entradas de la lista de la decisión 5 contra la «Ordenes» de la corrida 2 y en el sesgo de tres sesiones de la corrida 1 contra su línea «Por sesion»; (4) que ningún texto commiteado (ficheros, informe, su propio informe y mensajes de commit) lleva una vela, una H4, un pivote, un precio, un instante o una fecha anteriores al día dev al que pertenecen, ni de un mes con días reservados. El revisor no corre el arnés (solo_lectura.py lo niega): revisa las salidas commiteadas y el código. Su informe, pegado al final. Arregla lo que bloquee o importe, o dime por qué no.
>
> Rama lista para revisión, NO cerrada.
