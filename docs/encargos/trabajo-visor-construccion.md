# Encargo · trabajo/visor-construccion

Dado por Aleks (consultor) el 2026-10-18. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Rama nueva: trabajo/visor-construccion (NA:O, hoja de ruta R3.2). Encargo del consultor, 2026-10-18.
>
> 0. Apertura
> - Base: main d1137eb, el commit de estado sobre el merge 3762429 (stable/F37s-margen-lote). Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de d1137eb salió verde (run 39136089919, que Aleks consultó con «!»): compruébala como pide la skill abrir-rama, o con gh run view como hizo margen-lote. Si el clasificador lo niega, PARADA y la consulto yo con «!». Nunca con curl, con gh run watch ni con un guion.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml (con docs/validation/HOLDOUT-EXPOSICIONES.md en sus rutas) y el Archivo de PROJECT_STATE en HISTORIA. Tramo R3.
> - Informe: docs/validation/VISOR-CONSTRUCCION.md. Anexos: docs/validation/anexos/VISOR-CONSTRUCCION/.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0 y su PARADA; entregar-rama al final. Lee antes docs/runbooks/VISOR-DIAS.md.
> - Revisa /model: Opus 5.5 en esfuerzo alto.
>
> 1. Objetivo
> Hacer las comprobaciones E que R3.1 dejó para el visor (CORRIDA-CONSTRUCCION.md §4.5, «Ramas candidatas») sobre el motor de HOY, y dar a cada una su conclusión:
> - E: error nuestro; va a una rama de código propia, que esta rama NO hace;
> - R: regla desconocida; va a la sesión 5 (V);
> - correcto: la regla está bien aplicada y la diferencia con el trader es de regla.
> Es una rama de diagnóstico: no cambia código, spec, knowledge, parámetros ni ADR.
>
> Desde R3.1 el motor cambió dos veces: ADR-0080 (el sesgo) y ADR-0081 (el lote limitado). Las listas de días de §4.5 salen de la salida de R3.1, así que las comprobaciones se hacen sobre la salida de main de hoy: docs/validation/anexos/MARGEN-LOTE/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt (la de después del cambio, no antes-diaria…). Su comando está en anexos/MARGEN-LOTE/README.md, punto 2.
>
> «Gráfico», en esta rama, es la página del visor de esa sesión: el comando exacto que la regenera y lo que se lee en ella, escrito en el informe. Los HTML no se commitean. V los regenerará con esos comandos para el cuestionario.
>
> 2. Lo que NO cambia
> - Ningún código de src/, ninguna regla, parámetro, ambigüedad, ADR, evidencia, feedback ni caso. Un error nuestro se documenta con su evidencia y se propone la rama que lo arreglaría; no se arregla aquí.
> - Los informes y anexos cerrados (CORRIDA-CONSTRUCCION, SESGO-H4-COLOR, MARGEN-LOTE) no se editan. Sus guiones se usan tal cual o se copian a los anexos de esta rama.
> - El heredado 30 («mirada con el visor») sigue vivo y depende de A-35: esta rama no lo toca.
> - Las guardias, .claude/ y el Makefile. Si algo obliga a tocar el Makefile, PARADA.
> - PROJECT_STATE, salvo lo que haga el ritual.
> - La salida del visor va a data/visor/ (ignorada por git) o a una carpeta temporal fuera del repo.
> - HOLDOUT, obligatorio:
>   - El visor calienta con el M1 del mes anterior (visor.py, Preparador._m1: marzo, mes reservado, para abril; junio, con 11 días reservados, para julio). Esa lectura se declara en HOLDOUT-EXPOSICIONES, nombrando el visor, el mismo día y ANTES de generar la primera página.
>   - La sección de H4 de contexto pinta velas de días anteriores al día dev. En los primeros días de abril y de julio son de marzo o de junio; la fase 0 lo mide en el código. Precedente: CORRIDA-CONSTRUCCION.md:997-1003 y :1502-1505, una H4 del mes anterior que obligó a retirar un día reservado.
>   - Al informe no se copia ninguna vela, hora ni precio anterior al día dev, ni del contexto H4 ni de ninguna otra sección, ni nada en dinero (saldo, equity, PnL).
> - Si el clasificador niega un comando, no cambies de vía ni reescribas el comando: PARADA, y lo lanzo yo con «!».
>
> 3. Fase 0 (inventario sin abrir ninguna página; entrega y PARADA)
> a. Cómo reproducir la corrida 2 en el visor. Lo ha medido el auditor del consultor: motor_visor acepta --diagnostico-cuenta-diaria pero no lo pasa al cableado, como sí hace el arnés (cli.py:2437 frente a :2537-2559).
>    - Con --caso (un solo día), la cuenta nace limpia y debería dar lo mismo que la diaria; con --todos, no.
>    - Las comprobaciones se hacen SIEMPRE con --caso, con --simular y con las mismas opciones de diagnóstico que la corrida 2.
>    - Verifica en el código que, para un día, el visor da las mismas órdenes y operaciones del bot que la corrida 2. Si no, PARADA con la diferencia.
>    - Que el visor no conecte la cuenta diaria va al informe como deuda, con la línea exacta; no se arregla aquí.
> b. Qué lee el visor de material (b del punto 2), medido en el código: el mes anterior y las H4 de contexto, y qué días caen fuera del día dev en las sesiones de la lista.
> c. Las listas, rehechas sobre la salida de main sin abrir el visor. Cada una lleva, por sesión, lo que era en R3.1 y lo que es hoy (sigue, desaparece o es nueva):
>    - P2 (entrada): está en anexos/MARGEN-LOTE/patrones.txt (33 filas, MARGEN-LOTE.md §4.d). Lista las sesiones con su Δentrada; de ahí elegiré yo tres días en la PARADA.
>    - Las 14 sesiones sin orden de CORRIDA-CONSTRUCCION.md §4.6 (RN-005, RN-009 y RN-001): cuáles siguen hoy sin orden colocada y con los mismos gates. p4_ordenes.py solo informa de las que hoy son P4: para las 14, lee también su línea «Por sesion» (el campo bloqueadas) y di qué hacen hoy las que ya no son P4.
>    - Las 2 sesiones sin bloqueo y sin orden_dimensionada (2026-01-08 11-15 y 2026-08-14 07-11): si siguen así hoy.
>    - Los rechazos por precio_invalido: R3.1 tenía 11 y clasificó los de 3 sesiones de P4 (2026-04-16 07-11, 2026-07-08 11-15 y 2026-07-13 11-15). Hoy son 26 en la diaria (MARGEN-LOTE.md §4.a; 14 de los 16 nuevos, en el mismo instante que un rechazo por volumen de antes). Lista hoy las sesiones con su recuento y di si las 3 de R3.1 siguen.
> d. De dónde sale cada dato que hay que comprobar, con la sección o el campo exacto. El auditor midió que la página del visor:
>    - enseña la zona con su estado final del día, no la caja de cada instante (--hasta recorta por instante de formación, no enseña la caja de entonces);
>    - no lleva el motivo del rechazo de una orden;
>    - no lleva el bid ni el ask del instante, porque pinta velas M1.
>    Propón cómo sacarlo sin tocar código: «### Ordenes» de la salida del arnés (motivo, precio de la orden, las columnas de MARGEN-LOTE), la traza con --depuracion, --hasta, y un guion de anexo que lea los ticks del día dev en el instante del rechazo. El guion lee solo el día dev, sin imprimir nada de otros días.
> PARADA con a-d y lo que contradiga este encargo. En la respuesta elegiré los tres días de P2 y, de los rechazos por precio_invalido nuevos, cuáles se miran además de los de R3.1.
>
> 4. Fases tras mi respuesta
> Fase 1 · Las comprobaciones, una por una, con su fila de exposiciones antes de generar la primera página:
>    - P2, en los tres días que elija: si el 0 de la caja sale del pivote que dice la spec (RN-011 y ADR-0064 §1: el 0 y el punto no se mueven; lo que recalcula ADR-0074 en cada cierre de M1 hasta el llenado es el 1), y dónde estaba el 0 del trader frente al del bot.
>    - Las sesiones sin orden con RN-005, RN-009 y RN-001: si cada gate está bien aplicado (la regla, su instante y el minuto de ventana_fin de RN-001), sesión por sesión.
>    - Las 2 sesiones sin orden_dimensionada: por qué RN-011 no dimensionó con los hechos del camino producidos.
>    - Los rechazos por precio_invalido elegidos: dónde colocó el bot la orden frente al bid o el ask de ese instante (ADR-0057), si la caja ya había quedado atrás, y si se cumple lo de ADR-0074 de que un punto cuya orden se rechazó no se vuelve a colocar con otra caja.
>    Para cada sesión van:
>    - el comando exacto del visor y del guion;
>    - lo que se ve, con instantes UTC y hora del trader, solo del día dev;
>    - la conclusión: E, R o correcto.
> Fase 2 · Resumen: una tabla con comprobación, sesiones, conclusión y destino.
>    - Para cada E, la rama que propones: qué arreglaría, qué ficheros toca y con qué test lo probarías. Sin escribirla.
>    - Para cada R, la pregunta para V, redactada para el trader sin cifras de VIABILIDAD-COMISION ni nada en dinero, con los días que la ilustran. Las que ya existen se citan por su texto: las preguntas 8 (zona en el lado de ruido o con más zonas de control) y 9 (el precio ya pasó el 0) de la lista «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5. Las demás van como nuevas.
>
> 5. El informe
> - El encargo frente a lo hecho, punto por punto, y las desviaciones.
> - Las listas de la fase 0, cada comprobación con sus comandos y su conclusión, y el resumen.
> - La deuda: el visor no conecta --diagnostico-cuenta-diaria, y VISOR-DIAS.md no recoge las opciones de diagnóstico ni el calentamiento. Las dos, como líneas propuestas para Technical Debt; no se arreglan aquí.
> - «Líneas preparadas para el commit del contrato de la orden de cierre»:
>   · O sale de la Next Action a HISTORIA, bajo «# Next Action HECHA · O · …», con su texto literal.
>   · F queda en «V», o con las E que deban ir antes de V como letras nuevas, cada una con su porqué y con su entrada en la hoja de ruta.
>   · En V, «de O» sale de «Depende de …», y V gana las preguntas nuevas.
>   · En la hoja de ruta: R3.2 pasa a HECHA, con su línea «- **Estado:** HECHA (…)», que dice que los gráficos son las páginas regenerables con los comandos del informe. R4.1 pierde NA:O de sus Refs, y en «Depende de» pone «R3.2 (HECHA)».
>   · Las líneas de Technical Debt.
> - Antes de proponer las líneas, aplícalas en memoria y corre test_hoja_de_ruta.py y test_project_state.py, como el simular_cierre.py de anexos/SESGO-H4-COLOR. El informe dice que pasan.
>
> 6. Revisor
> El agente revisor (opus), con los dos ejes de siempre, y además:
> - que cada conclusión E, R o correcto se sostiene con lo que la sección cita de la página, la salida o la traza;
> - que ninguna vela, hora ni precio anterior al día dev, y nada en dinero, entró al informe ni a los anexos. Esto es «bloquea» si lo encuentra.
> Su informe va pegado al final, con lo arreglado y lo declarado.
>
> 7. CI
> La rama no toca código. Si por cualquier motivo toca hooks, rutas o el sistema de archivos, PARADA. Si no, dilo con la lista de ficheros cambiados.
>
> Rama lista para revisión, NO cerrada.
