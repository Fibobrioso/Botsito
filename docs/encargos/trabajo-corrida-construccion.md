# Encargo · trabajo/corrida-construccion

Dado por Aleks (consultor) el 2026-10-14. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Encargo del consultor (2026-10-14): R3.1, la corrida del arnés sobre la construcción vigente y la tabla de diferencias para clasificar.
>
> RAMA Y BASE
> - Rama nueva: trabajo/corrida-construccion, desde main. Antes de abrir, verifica con git que main está en 23316c8 (commit de estado sobre el merge 87391b7, tag stable/F37p-entrada-enero) y que la CI de main del 23316c8 está en verde; si algo no cuadra, para y dímelo.
> - Ábrela con la skill abrir-rama: este encargo literal a docs/encargos/trabajo-corrida-construccion.md, contrato.yaml con tramo: «R3 · Una corrida del arnés sobre toda la construcción», y el archivo en HISTORIA que pida la skill.
> - Revisa /model antes de empezar: este encargo va con Fable 5.1 y esfuerzo alto.
>
> OBJETIVO (una frase)
> Correr el arnés simulado sobre toda la construcción vigente (abril, julio del 1 al 17, agosto y enero del 2 al 30), con los diagnósticos que el motor aún necesita (A-35 y A-44), y dejar en el repo, por operación, la tabla de diferencias entre el bot y el trader para que yo las clasifique (error nuestro o regla desconocida) y salga de ahí el cuestionario de la sesión 5 (V, R4.1).
>
> QUÉ NO CAMBIA
> - Ningún parámetro, ninguna regla de la spec, ninguna decisión del motor, ni el bróker simulado, ni la capa de cuenta, ni el freno de peticiones.
> - criterio_fidelidad.yaml no se toca: ni umbrales, ni tolerancias, ni la lista construccion ni su ORDEN (siete ficheros de tests toman construccion[0]).
> - Nada de mayo ni de ningún mes de medida o reservado: el arnés ya se niega y no se rodea. Ni marzo, ni febrero, ni diciembre, ni septiembre, ni el corpus del trader (ni xlsx, ni vídeos, ni fotogramas, ni transcripciones). Los casos dev de construcción ya ingeridos sí se leen: son el material de desarrollo.
> - Esta corrida NO habilita mayo y NO es fidelidad: lleva --diagnostico-*, así que ADR-0070 §3 da «no», y el informe lo dice tal cual. Ningún resultado de esta rama se usa para fijar o cambiar un valor (PROJECT_STATE, Things That Must Not Be Changed, que sale de MASTER_PLAN: los parámetros no se optimizan contra resultados). La lectura de A-35 de la corrida principal, cierre_vela_contraria, se fija ANTES de correr y no por su resultado: es la de F35 y BE-AL-TICK, la única con historia comparable. Si la comparación de las dos lecturas de A-35 (corrida 3) muestra que una «empareja más», eso NO decide A-35: solo nombra días concretos para preguntárselos al trader.
> - El margen a 1:30 (Technical Debt) NO entra aquí: tiene su propia rama.
>
> AUTORIZACIÓN EXPRESA
> En esta rama se autoriza ejecutar `uv run botsito motor arnes`, solo con los tres comandos de la fase 2, escritos exactamente así (ADR-0070 lo permite para medir; los encargos anteriores lo prohibían porque no medían). Ningún otro comando del arnés ni del visor sin preguntármelo en una PARADA. Las corridas son largas: no las lances mientras corre make check, y si van en segundo plano, recuerda CLAUDE.md (CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1); si una muere por memoria, no la relances sin decírmelo. Si la guardia o el clasificador niegan alguno de esos tres, no lo reescribas para esquivarla: para y dime el comando exacto, y lo lanzo yo con «!».
>
> FASE 0 · INVENTARIO SIN TOCAR NADA (skill fase-cero) → PARADA
> Lee código y documentos; no corras el arnés todavía. Entrega, cada punto con fichero:línea:
> a) Los comandos de la fase 2, tal como el parser los acepta (cli.py: _opciones_diagnostico, _opciones_simulacion y el subparser de motor arnes), y el nombre real que escribirá cada uno (diagnostico.nombre_etiquetado añade el rótulo). Verifica que con el perfil ftmo-2step-swing-100k no hace falta --diagnostico-a27 (firma_stops_level_puntos CONFIRMED a 0, ADR-0071) ni --diagnostico-a47 (entrada_tipo_orden CONFIRMED, stop_en_ruptura), y que A-21 ya no tiene diagnóstico (ADR-0076).
> b) Ticks: que cada día dev de los cuatro meses tiene ticks en data/manifests/ticks/ (enero 1ce59681, abril 1d189bdd, julio 6e7dc7cd, agosto 75bd3a08), y qué hace el cableado con las horas perdidas (enero declara 5 de 189; verifica las de julio y agosto en sus manifiestos) frente a un día sin ticks, que cableado.py rechaza salvo con --depuracion (y --depuracion da «no»). Si algún día dev no tiene ticks, PARADA: no se corre con --depuracion.
> c) Calentamiento (engine/arnes.py, dias_de_mercado): qué mes anterior carga cada mes de construcción si existe su dataset M1 (hoy hay M1 de 2026-03 y 2026-06, que tienen días reservados). Hoy no existe M1 de 2025-12, así que enero calienta desde su propio mes (ENTRADA-ENERO.md §0.f). Confirma contra CLAUDE.md («Que se puede mirar y que no», punto 2) y ADR-0021 §1 / ADR-0033 que leer esas velas para calentar no es abrir un holdout, y propón su declaración en HOLDOUT-EXPOSICIONES el mismo día de la corrida, por recuento de días reservados cuyas velas se leen, nunca por fechas (el arnés, a diferencia de kit build/check, no lo declara solo). Di también si la llegada del M1 de julio cambia el calentamiento de agosto respecto a las corridas de BE-AL-TICK (antes de julio, agosto calentaba sin él).
> d) Qué da hoy el informe y qué le falta para clasificar: arnes.informe da recuentos por sesión pero no el detalle por operación; BE-AL-TICK sacó su volcado posición a posición con un envoltorio fuera del repo. Propón cómo se produce la tabla de la fase 1 con código commiteado. Mi decisión por defecto: una sección nueva «## Diferencias por operación» al final del informe del arnés, que no añade ninguna opción (ADR-0070: la lista cerrada no cambia), construida sobre el emparejamiento que ya existe (cases/criterio_fidelidad, medida.parejas). Antes de proponerla, busca TODOS los tests y líneas base que dependen del formato o del final del informe (test_arnes_motor, test_umbral_mayo, test_cableado, test_huecos_motor, ARNES-MOTOR-LINEA-BASE.txt, CABLEADO-SIMULADOR-LINEA-BASE.txt, HUECOS-MOTOR-LINEA-BASE.txt y los que encuentres) y di qué rompe. Si la sección rompe una línea base inmutable o un test que no se debe tocar, la alternativa es un guion en docs/validation/anexos/CORRIDA-CONSTRUCCION/ que use las mismas funciones del arnés; elige y justifica.
> e) Las horas de ticks perdidas de los cuatro manifiestos (verifica el total; enero 5), que el cableado cubre con el respaldo M1 y el spread supuesto: lista por día y hora, para marcar en la tabla las diferencias que caigan en ellas.
> e2) Tiempo y memoria esperados de una corrida de los cuatro meses con --simular (lo que digan informes anteriores de dos meses: F35-ORDEN-STOP-PIVOTE, BE-AL-TICK, MEMORIA-SUITE), y si las tres corridas caben en una sesión.
> f) Recuentos de partida, contados en el repo (no los cites de memoria): días dev y operaciones del trader por mes de construcción.
> g) Herencias que entran en esta rama, buscadas con grep: HER:25, HER:30 y HER:35 (RN-004 tras A-35, RN-020 tras A-44: no se mueven, porque A-35 y A-44 siguen «en parte»), y ADR-0074 §3 («la cadena entera por el cableado real» de caja_se_fija = en_cada_cierre_m1 es de R3.1: la corrida mide las peticiones por día con el cableado real frente a los umbrales del freno de ADR-0067). Cualquier otra que nombre R3.1 o «la corrida» en ENTRADA-JULIO.md, ENTRADA-ENERO.md, ACTIVAR-SESION-04*.md y HOJA-DE-RUTA.md.
> PARADA con todo eso. No escribas código antes de mi respuesta.
>
> FASE 1 · LA TABLA DE DIFERENCIAS (con lo que decida en la PARADA)
> Por cada operación del trader de construcción, una fila: día, sesión, lado, instante y precio de entrada del trader; si el bot la empareja (criterio de ADR-0043: 3 puntos de entrada, 15 minutos de llenado); si no, la operación del bot más cercana en esa misma sesión (lado, Δentrada en puntos, Δinstante en minutos) o «ninguna», y el primer hecho del embudo que no se produjo en esa sesión, con su primitiva si la hay. Y por cada operación del bot sin pareja (en sesiones con o sin operaciones del trader), su fila con lo mismo del otro lado. Ordenado por mes en el orden de construccion y por día. Determinista (dos corridas, mismo fichero byte a byte).
> Tests que rompen a propósito, en los dos sentidos, con datos sintéticos (ninguno corre el arnés real): una operación emparejada que sale como emparejada; una a 4 puntos o a 16 minutos que sale sin pareja con su Δ correcto; una sesión sin operación del bot que dice «ninguna» y el hecho que faltó; una operación del bot sin pareja en un día sin operaciones del trader. Y uno que compruebe que la sección no añade ninguna opción al comando (la lista de ADR-0070 sigue igual).
> make check en verde antes de commitear.
>
> FASE 2 · LAS TRES CORRIDAS
> Sobre el código de la fase 1 commiteado, sin --meses (todos los meses de construcción), a docs/validation/anexos/CORRIDA-CONSTRUCCION/:
> 1. Principal, cuenta arrastrada (como operará el bot):
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/arrastrada.txt
> 2. La misma con la cuenta reiniciada cada día (la estrategia sin el camino de la cuenta; sobre esta se clasifica):
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/diaria.txt
> 3. La otra lectura de A-35, con la cuenta diaria:
>    uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/a35-inicio.txt
> Cada --salida es distinta a propósito: comprobar_ruta no impide sobrescribir. El nombre final lleva el rótulo de nombre_etiquetado; cópialo tal cual al informe.
> (Si la fase 0 muestra que el parser o los nombres piden otra forma, la corrijo yo en la PARADA; no la cambies por tu cuenta.) Copia las líneas TIEMPO y MEMORIA de cada una al informe. Repite la 2 una vez con --salida fuera del repo (en tu carpeta temporal) y comprueba con diff que el informe sale idéntico; borra la copia.
> En el informe docs/validation/CORRIDA-CONSTRUCCION.md:
> - Por corrida y por mes: operaciones del trader, puntuables del bot, parejas, cobertura y precisión, y la línea de veredicto de ADR-0070 tal cual (será «no» por las opciones de diagnóstico; si dijera otra cosa, PARADA).
> - De la corrida 1: el veredicto de la cuenta sobre el tramo, el día y la regla en que la cuenta corta el tramo si lo corta, y las peticiones (total, máximo diario frente a 2000 y si saltó algún umbral del freno de ADR-0067), que es la medida que hereda ADR-0074 §3.
> - De la 3 frente a la 2: solo la lista de días y sesiones en que cambia alguna operación del bot o alguna pareja, con qué cambia. Sin elegir lectura.
> - El embudo agregado (dónde se paran las sesiones sin operación del bot), por mes.
> - Las 18 horas sobre respaldo M1 (o las que mida la fase 0 e), y qué filas de la tabla caen en ellas.
> - Como contexto y no como referencia: BE-AL-TICK §2 dio 2 de 77 (arrastrada) y 7 de 77 (diaria) sobre abril y agosto, 42 días dev, con el motor de antes de ADR-0074 a ADR-0077; hoy la construcción tiene más días (cuéntalos en la fase 0 f). Da las cifras de abril y agosto de esta corrida y di qué cambios del motor y del calentamiento las separan, sin ajustar nada para acercarlas.
> Si alguna corrida falla, sale con exit distinto de 0, o pide días fuera de la construcción, PARADA con el error literal; no se corre con --depuracion ni con --meses parcial para salir del paso.
>
> PARADA 2 · ENTREGA PARA CLASIFICAR
> Commitea las salidas y el informe hasta aquí y para. Yo leo la tabla de la corrida 2 por el puente en la carpeta de Aleks y clasifico cada diferencia: (E) error nuestro, a una rama de código; (R) regla desconocida, a una pregunta para la sesión 5; (D) depende de un diagnóstico (A-35 o A-44); (M) material o dato (ticks, libro, huso). Puede que te pida días concretos en el visor; no los abras antes.
>
> FASE 3 · LA CLASIFICACIÓN EN EL REPO (con mi respuesta)
> Copia mi clasificación literal al informe, una fila por diferencia con su clase y su destino, con mi fecha. Las (R) forman una lista «Para el cuestionario de la sesión 5» que V leerá; las (E), una lista de ramas candidatas con su fila de la tabla. Nada de esto cambia el código en esta rama.
>
> REGLAS DE SIEMPRE
> - Si una rama cambia el Makefile, la guardia niega todo make a la sesión: esta no debería cambiarlo; si hiciera falta, PARADA, y esos make check los lanza Aleks con «!». Los pushes que niegue el clasificador, también los lanza Aleks.
> - Las rutas del corpus se leen en fuentes.yaml (raíz: corpus/Estrategia del trader); aquí no hace falta abrir ninguna.
> - Al cambiar el informe del arnés, busca todos los tests que dependen de él y de su orden antes de tocarlo (fase 0 d).
> - Ningún texto commiteado lleva fechas de días reservados, ni recuentos por fecha de material reservado. Toda exposición, el mismo día en HOLDOUT-EXPOSICIONES.
> - PROJECT_STATE está en 23.624 bytes, cerca del tope de 25 KB: esta rama no lo toca (lo hará el cierre).
> - CI de Linux: no toca .claude/, hooks ni código de plataforma, así que no hace falta fix/; si la fase 1 tocara algo de eso, dilo en la PARADA.
>
> INFORME Y REVISOR
> - Hallazgos para las líneas del cierre: la Refs de R3.1 en HOJA-DE-RUTA no cita ID:ADR-0074 aunque hereda su §3; ADR-0070 §3 sigue diciendo «hoy A-21, A-35 y A-44» (no se edita: lo dice R3.1); docs/runbooks/ACTIVAR-A35-A44.md todavía cita --diagnostico-a21. Propón la corrección de cada uno.
> - El informe lleva: encargo frente a lo hecho punto por punto con evidencia, desviaciones declaradas, comandos literales ejecutados, las exposiciones del día y las líneas propuestas para el cierre (Next Action: F pasa a apuntar a V con la lista de (R); hoja de ruta: R3.1 HECHA y lo que dependa de ella; HER:25, 30 y 35 con lo que la corrida diga de ellos).
> - Revisor (opus) sobre la rama con dos alcances: que la tabla dice lo que el emparejamiento de ADR-0043 dice (comprobado a mano en tres filas de cada mes) y que nada de la rama cambia una decisión del motor (diff de src/ limitado a la sección o al guion de la fase 1). El revisor no puede correr el arnés (solo_lectura.py lo niega): revisa leyendo las salidas commiteadas y el código. Su informe, pegado al final.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-10-14)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/corrida-construccion (2026-10-14). Cópiala literal al informe, §1, bajo «Respuesta del consultor», con la fecha.
>
> 1. Decisión 0: (a). La sección «## Diferencias por operacion» es la última de arnes.informe; con --simular queda antes de la cola «## Simulacion», y cli.py no se toca. Porque nada del comando ni de la lista cerrada de ADR-0070 se mueve, y se encuentra por su encabezado.
> 2. Decisión 1: (a). El resumen y el embudo por mes van en la sección, calculados en arnes.py a partir de la misma Medida partida por mes, con tests sintéticos. Porque las cifras escritas a mano no tienen test.
> 3. Decisión 2: (a). La tabla no marca las horas perdidas; el informe lista las filas que caen en una de las 17 horas que caen dentro de las sesiones (y dice que la 18.ª queda fuera). Haz el cruce con un comando o guion que quede escrito en el informe, no a ojo, y pega su salida. Porque tocar cli.py para esto no compensa, pero el cruce tiene que poder repetirse.
> 4. Decisión 3: (a). La fase 1 commitea docs/validation/anexos/CORRIDA-CONSTRUCCION/README.md con qué es cada fichero y los tres comandos literales. Porque así la carpeta existe en git antes de correr.
> 5. Decisión 4: (a). Las salidas son diagnóstico etiquetado y no son una línea base; HER:30 y HER:35 siguen apuntando a CABLEADO-SIMULADOR-LINEA-BASE.txt hasta que A-35 y A-44 tengan valor. Porque una línea base no puede llevar nombre de diagnóstico.
> 6. Decisión 5: (a). Por mes en el orden de construccion (04, 07, 08, 01). Porque lo pide el encargo.
> 7. tramo: R3 en el contrato vale (scripts/contrato_rama.py lo acepta como equivalente).
> 8. La afirmación 28 del encargo era INCORRECTA y el error es mío: dije que el M1 de julio cambiaba el calentamiento de agosto sin mirar la fecha del manifiesto. En el informe, sustituye esa comparación por lo que mediste: lo que separa esta corrida de BE-AL-TICK es el motor desde ADR-0066 (con 0067, 0068, 0069, 0071, 0073 a 0077 y cases por la rejilla) y que la cuenta arrastrada recorre ahora enero, abril, julio y agosto. Propón en §1.k la fila para ERRORES-RECURRENTES: consultor y auditor del consultor dieron por cierto un cambio de calentamiento sin mirar cuándo entró el manifiesto. Lección: un «antes no estaba» se comprueba con la fecha de entrada del fichero en git.
> 9. Corrida 1 (cuenta arrastrada): se corre tal cual, sin cambiar el orden ni partir el tramo. El informe dice que el tramo no es continuo (enero, y luego de abril a agosto con huecos), que su veredicto de cuenta y su curva son indicativos, y que la clasificación se hace sobre la corrida 2. Junto al veredicto, la nota del margen que propones: el simulador no comprueba el margen (HER:37), así que puede llenar operaciones que FTMO rechazaría.
> 10. Agosto: sus casos dev salen de un xlsx que el trader no da por bueno (S-16, ADR-0073; NA:Q). En la tabla no se marca nada; en el informe, una línea que lo recuerda junto al resumen de agosto. Yo decido al clasificar si alguna diferencia de agosto es (M).
> 11. La lectura del M1 de marzo y junio para calentar: queda bien declarada la de hoy. Lo permanente (cada make check por test_huecos_motor.py:290-337 y cada corrida del arnés) va a las líneas del cierre como una línea de Technical Debt nueva y una fila única en HOLDOUT-EXPOSICIONES que la declare como exposición permanente por recuento. La propuesta de que dias_de_mercado imprima una línea LECTURA: va a G.2, en esa misma línea. No se cambia código para esto en esta rama.
> 12. Hallazgo 1.k.2 (ADR-0070) y 1.k.3 (runbook ACTIVAR-A35-A44.md): entran en ESTA rama, en la fase 3 y en un commit propio. Amplía el contrato con docs/adr/0070-umbral-de-construccion-para-medir-mayo.md (solo para añadir la NOTA, que es lo que permite el régimen de los ADR; el cuerpo no se edita) y docs/runbooks/ACTIVAR-A35-A44.md. La NOTA es la que propones en 1.k.2, añadiendo al final la cifra del veredicto que dé la corrida. En el runbook: las tres menciones de --diagnostico-a21 se marcan como «(ya no existe, ADR-0076)», y el comando del §5 lleva --simular para que se compare con una línea base escrita con --simular. Porque los dos llevan dos ramas pendientes y son texto.
> 13. Hallazgos 1.k.1 (Refs de R3.1 con ID:ADR-0074 · ID:ADR-0067 y la frase de las peticiones) y 1.k.5 (F apunta a V; antes, J y A.4): van a las líneas del cierre tal como los propones.
> 14. La guardia que bloqueó tu guion por nombrar data/manifests/ticks: bien declarado y bien no rodeado. Tu propuesta para G.1 va a las líneas del cierre como texto de G.1; no se toca .claude/ en esta rama.
> 15. La repetición de la corrida 2 con --salida fuera del repo, para el diff, queda autorizada como cuarto comando. Escríbelo literal en el README y en el informe, y borra la copia después.
>
> Sigue con la fase 1. Recuerda: make check en verde antes de cada commit, las corridas nunca a la vez que make check, y si la guardia o el clasificador niegan un comando, PARADA con el comando exacto y lo lanza Aleks con «!». Después, la fase 2 y la PARADA 2.
>
> Rama lista para revisión, NO cerrada.
