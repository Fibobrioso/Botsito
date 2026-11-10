# Encargo · trabajo/trazas-ablacion

Dado por Aleks (consultor) el 2026-11-09. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Encargo del consultor (2026-11-09): rama trabajo/trazas-ablacion, el punto (1) de la entrada F de la Next Action (R4.4 de docs/plan/HOJA-DE-RUTA.md; docs/plan/RUMBO-2026-11.md §2), tramo R4. Ábrela con la skill abrir-rama, con riesgo alto (toca el motor), y copia este encargo tal cual en docs/encargos/trabajo-trazas-ablacion.md. Trabaja en la laptop (hacen falta las velas, los ticks y el arnés) y arranca Claude Code con CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1, porque habrá corridas largas. Antes de empezar, comprueba con /model que estás en Opus 5.5 con esfuerzo alto.
>
> BASE (compruébala con git al abrir, como manda abrir-rama): main y origin/main en 144e42c, commit de estado sobre el merge 129ea33, tag stable/F38u-video-julio (el último «- Tag:» de HISTORIA); CI de main sobre 144e42c: run 42681006516 en verde (compruébalo, yo no pude); ninguna otra rama local ni remota. Si algo no cuadra, PARADA antes del primer commit.
>
> OBJETIVO, en una frase: ver por qué decide el motor. Cuatro piezas:
> (a) una bitácora de decisiones por día y sesión: las tomas de M15 con su nivel y su instante, los escenarios (ADR-0066), las zonas y los puntos, la orden que se colocó por cada uno (o por qué no se colocó) y el gate que fija cada prohibición, no solo los frenos;
> (b) un diagnóstico de ablación que apaga una regla VIGENTE a la vez y dice qué parejas y qué operaciones de más cambian;
> (c) con (a), los días 2026-04-13, 2026-07-02, 2026-07-03 y 2026-07-14 medidos y la clase de sus filas propuesta;
> (d) el recorte de PROJECT_STATE.md, que está en 23.805 bytes con tope 25.000.
> 07-03 entra porque es el día de las 5 filas de «error nuestro (sospecha)» de VIDEO-JULIO.md §4.1 y de 2 de las 13 que T mandó a esta rama.
> Lo llamo «bitácora» y no «registro» ni «traza» porque esos nombres ya existen: Registro es el de parámetros (ADR-0002), y TrazaSesion y trazas_broker son del motor.
>
> QUÉ NO CAMBIA
> - Nada de lo que el motor decide ni de cómo se llena. No se tocan knowledge/spec/ (reglas, parámetros, ambigüedades), knowledge/cases/ (criterio_fidelidad.yaml, casos, libros), knowledge/evidence/ ni knowledge/feedback/. breaker_m1_criterio_ruptura sigue en mecha (ver «La tensión de 07-03»).
> - `motor arnes` y `motor visor` no cambian: ni opciones, ni salida. La bitácora y la ablación salen por un subcomando nuevo de `motor` (el nombre lo propones en la fase 0) que corre el arnés en proceso y no comparte _opciones_diagnostico. Así siguen intactos OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA (src/botsito/engine/arnes.py:74-82) y test_la_seccion_no_anade_ninguna_opcion_al_comando (tests/unit/test_diferencias_por_operacion.py:341-361). Si el diseño no puede cumplir esto, PARADA.
> - No se crea ningún ítem de evidencia. Cambio de destino de F7 #6 y #9 de VIDEO-JULIO.md, decidido ahora (antes, «la rama de trazas, si los necesita»): #6 es la voz de 07-03 y lo crea la rama de la preparación de la sesión 7 si la clase sale «contradicción con lo fijado», como #1, #2, #3 y #10; #9, la rama que active el break even.
> - RECORRIDA-CONSTRUCCION-2.md y VIDEO-JULIO.md son informes cerrados: no se tocan.
> - Sin fila en el Marcador de la hoja de ruta: la corrida base de esta rama repite la línea base (diff de 0 bytes) y las ablaciones son diagnóstico. La orden de cierre lo dirá.
> - Fuera de src/ y tests/: el informe docs/validation/TRAZAS-ABLACION.md y su anexo, HOLDOUT-EXPOSICIONES.md, una NOTA en ADR-0092 §6 (no reescribe el cuerpo, como la NOTA de §8), y PROJECT_STATE.md y docs/state/HISTORIA.md para el recorte. Más lo que abrir-rama escribe (docs/encargos/, el contrato y el Archivo de HISTORIA) y el número de «Tests Currently Passing» que pide state check. El contrato cubre exactamente eso.
>
> LO QUE SE PUEDE MIRAR (CLAUDE.md, «Que se puede mirar y que no»)
> - Solo construcción: los meses de `construccion` de knowledge/cases/criterio_fidelidad.yaml y sus casos dev, por la compuerta del arnés (dias_de_construccion y casos_ocultos). En la fase 0, compruébalo para los cuatro días con casos_reservados(repo) y casos_ocultos(repo), contando y sin imprimir ids.
> - Cada corrida del arnés y cada make check calientan con el M1 de marzo y el de junio (Technical Debt). HOLDOUT-EXPOSICIONES.md lleva una fila por cada día de trabajo de la rama, escrita ANTES de la primera corrida o del primer make check de ese día, que dice cuántas corridas del arnés se hicieron y de qué clase (base, bitácora, ablación).
> - No se lee ninguna transcripción ni ningún fotograma. La voz del trader sobre estos días ya está en VIDEO-JULIO.md §4 y §7, y se cita de ahí.
> - La salida del subcomando nuevo NO lleva R, PnL, rentabilidad ni porcentajes de cobertura o precisión: solo recuentos y qué sesiones y filas cambian. No se escribe el informe entero del arnés por cada ablación: el subcomando calcula en proceso lo que necesita y escribe solo eso. Si para comparar necesitas el informe entero de la corrida base, va a una carpeta ignorada de data/ y de él se leen solo los recuentos.
> - El fichero de salida lleva DIAGNOSTICO en el nombre y en cada línea, y un test lo exige. Cuidado con engine/diagnostico.py: nombre_etiquetado (:169-185) solo admite etiquetas que empiecen por «DIAGNOSTICO-A» o por la de la cuenta, y una «DIAGNOSTICO-ABLACION…» pasaría en silencio como si fuera de una ambigüedad. No la reutilices así: o una etiqueta y un nombrado propios, o se arregla esa función con su test. Es una decisión de la fase 0.
> - La nota para P5 (VIDEO-JULIO.md §10.4) sigue en pie: hasta que el trader explique F7 #10, una operación de más del bot no se da por error, y la ablación tampoco la llama así.
>
> LO QUE YA SE SABE (verifícalo en la fase 0, no lo copies)
> - TrazaSesion (src/botsito/engine/motor.py:206-214) lleva hechos fijados, primitivas no implementadas, acciones bloqueadas, reglas disparadas, anotaciones y empates. El intérprete acumula los prohibidos como un conjunto de efectos, sin la regla que los prohíbe (src/botsito/engine/interprete.py:129 y :260); `bloqueadas` lleva la regla que intenta la acción, no el gate que la prohíbe.
> - El visor no nombra las tomas de M15 ni los escenarios, y de los gates solo enseña los frenos (RECORRIDA-CONSTRUCCION-2.md, F3.4, «Lo que el visor NO muestra»).
> - El visor empieza cada día desde el capital (RECORRIDA-CONSTRUCCION-2.md, F3.4 (a)) y el arnés lleva una cuenta por mes (ADR-0092 §8). En 07-15 dieron órdenes distintas. La bitácora de un día sale de la misma corrida con la cuenta por mes, nunca de un día suelto.
> - La línea base es docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt, de `uv run botsito motor arnes --simular --salida <fichero>` (RECORRIDA-CONSTRUCCION-2.md:354: 339,5 s y pico de 635,6 MiB). El fichero no lleva sha, tiempo ni memoria (salen por pantalla), así que la repetición tiene que dar un diff de 0 bytes. F38t y F38u no tocaron src/.
> - 11 de las 32 reglas VIGENTE no disparan nunca en la línea base: RN-007, RN-008, RN-010, RN-019, RN-020, RN-021, RN-022, RN-026, RN-029, RN-030 y RN-031 (medido por mi auditor sobre cuenta-por-mes.txt; RN-019, además, en Technical Debt y PUNTO-USADO.md §1.h). Su ablación es el control: tiene que dar delta cero.
> - strategy_spec.yaml tiene 32 reglas VIGENTE (15 gate, 14 disparador, 2 terminal y 1 fallback) y 5 DESCARTADA; las 32 llegan al intérprete por reglas_ejecutables (interprete.py:363).
> - Precedente de guion en proceso: medir_f2_f3.py (ACTIVAR-SESION-06-MOTOR.md:118-130), que corría con la cuenta diaria y vivía fuera del repo.
>
> LA TENSIÓN DE 07-03 (decisión del consultor, escrita antes de medir)
> VIDEO-JULIO.md §4.1 propuso «error nuestro (sospecha)» para las 5 filas de 07-03 07-11 por v12 0:00:15-0:00:58 («aquí no había entrada porque es con mecha, sabemos que tiene que ser con cuerpo»). Pero la sesión 5 ya respondió A-32 (S-18; knowledge/spec/ambiguedades.yaml:864-898): «en M1 la mecha siempre vale»; la única ruptura que pide cuerpo es la que habilita la zona lineal de liquidez de M15, y una línea que viene de M15 cuenta como de M15 aunque se mire en M1. breaker_m1_criterio_ruptura = mecha, CONFIRMED (knowledge/spec/parametros.yaml:501-518). T no cruzó su clase con eso: es un error mío y va a la orden de cierre. Por eso aquí no se cambia nada, y la bitácora tiene que decir, para cada orden del bot en 07-03 07-11:
>  (i) qué toma de M15 abrió su escenario: nivel, instante, la vela que la toma y si cerró con cuerpo;
>  (ii) qué breaker de M1 formó su esquema, y si su ruptura fue con mecha o con cuerpo;
>  (iii) si la línea rota venía de M15 (la de la toma u otra).
> Con eso, cada fila se propone en una de estas clases, con su porqué:
>  - error nuestro: el bot tomó como de M1 una línea de M15, o dio por tomada con mecha una liquidez de M15. Se nombra la pieza, sin tocarla;
>  - contradicción con lo fijado: el breaker es de M1 y rompió con mecha, así que la voz de v12 choca con S-18. No se pisa: va a la sesión 7 como pregunta;
>  - otra (efecto de la cuenta, regla desconocida o sin clase).
> Las clases las decido yo en la PARADA final.
>
> FASE 0 (skill fase-cero, con el agente auditor-encargo sobre este encargo). No se escribe en el repo salvo la apertura.
> 0.1 La base y lo de mirar de arriba.
> 0.2 Antes de usar cada herramienta o salida, escribe qué campos da, medido sobre una ejecución (lección de F38t y F38u): TrazaSesion, ResultadoDia, el Evento del intérprete (ojo: hay otro Evento en llenado.py), las secciones del informe de `motor arnes --simular`, y en cableado.py dónde se abre un escenario, dónde se liga una zona y dónde se coloca una orden.
> 0.3 Qué decisiones del motor no son reglas RN (las de primitivas como las zonas usadas, el punto rechazado o los cartuchos, y los frenos de la cuenta). La ablación no las ve: lístalas.
> 0.4 El diseño que propones:
>   - La bitácora: dónde se engancha sin cambiar lo que el motor devuelve (un observador pasivo); texto determinista; sin mirar al futuro (cada línea con el instante en que el motor lo supo); y dónde se escribe (una carpeta ignorada de data/, y los cuatro días copiados al anexo).
>   - La ablación: un mecanismo genérico (se quita UNA regla del conjunto que recibe el intérprete, sin ningún caso especial por regla, y la spec y su sha no cambian); el nombrado y la etiqueta (ver arriba lo de nombre_etiquetado); el rechazo de un id que no sea VIGENTE, nombrándolo; y la comparación contra la corrida base de la propia rama, sin escribir R, PnL ni porcentajes.
>   - El subcomando nuevo: nombre, opciones y por qué no puede habilitar medir ni escribir la salida de una corrida que cuenta.
>   - El tiempo: la estimación medida de las corridas (base, bitácora y 32 ablaciones; a unos 340 s cada una, unas 3 h) y el PICO DE MEMORIA del último make check.
> 0.5 Herencias: busca «rama de trazas», «trazas del motor», «ablación», «R4.4» y «pendiente con dueño» en PROJECT_STATE, el final de HISTORIA, docs/validation/, docs/adr/ y docs/plan/. Todo lo que se deje a esta rama entra en ella, o se dice por qué no. Las conocidas:
>   · RECORRIDA-CONSTRUCCION-2.md:1355-1358, la pendiente con dueño: en 07-14 11-15, si las tres pérdidas sin RN-016 (o10, o12 y o14) son del mismo barrido; y lo no comprobable de 04-13 y 07-02;
>   · su F3.4: la fila de 2026-04-13 07-11 (:1283; a las 08:47, RN-011 da zona:59 y RN-015 «no», sin posición viva: qué gate lo prohíbe) y la de 2026-07-02 11-15 (:1282: las de 14:10 y 14:23 ya salieron «sí», RN-016 aplicado como está escrito; las no comprobables son las de 12:25 y 12:45);
>   · VIDEO-JULIO.md §4.1 y §4.2: las 5 de 07-03 07-11; las 13 «a la rama de trazas» (07-02 11-15 ×5, 07-03 11-15 ×2 y 07-14 11-15 ×6); y 07-02 14:10 y 14:23, regla desconocida («seguir tras tres pérdidas», con el bot detenido por RN-016 desde las 14:08);
>   · VIDEO-JULIO.md §10.4, RUMBO §2 y HOJA-DE-RUTA R4.4.
> 0.6 El recorte: los candidatos de F1, cada uno con su condición, su evidencia y los bytes que ahorra.
> PARADA al terminar la fase 0, siempre: es terreno nuevo del motor y el diseño de 0.4 lo apruebo yo antes de escribir código. Mientras esperas la respuesta, puedes hacer F1 en su commit.
>
> F1 · EL RECORTE DE PROJECT_STATE (commit propio)
> - Con docs/state/README.md, «Que sale de PROJECT_STATE, y con que criterio», condiciones (a) a (e) tal cual, negando por defecto: si hay duda, la línea se queda.
> - (e) alcanza a las líneas de Technical Debt de más de 200 bytes aún sin acortar (hay 22), pero solo ahorra 60 bytes o más en las de unos 271 o más (unas 9; las más largas, la del panel de FTMO, la del riesgo residual de ADR-0088 y la de la copia de seguridad de las crudas). Mídelas.
> - Lo que sale o se acorta va al final de HISTORIA, en su bloque por clase, con su texto literal.
> - Cifra antes y después. No hay cifra objetivo: si los criterios dan poco, se dice y no se fuerza.
> - La Next Action no se toca aquí: la cambia la orden de cierre.
>
> F2 · LA BITÁCORA (los tests primero)
> - La misma corrida decide lo mismo con la bitácora activada: mismas operaciones, órdenes y parejas, sobre un mes de construcción o contra un golden de main. Un observador que mute el estado tiene que hacer fallar el test: mutación comprobada.
> - Cada prohibición de la bitácora nombra el gate o los gates que la fijan; si dos gates prohíben lo mismo, salen los dos.
> - Sin mirar al futuro: ninguna línea lleva información posterior al instante de su evento.
> - Determinista: dos ejecuciones dan los mismos bytes.
>
> F3 · LA ABLACIÓN (los tests primero)
> - El subcomando nuevo no puede habilitar medir ni escribir donde escribe una corrida que cuenta, y `motor arnes` sigue con las mismas opciones (el test de :341-361, sin cambios).
> - La salida siempre va etiquetada y sin R, PnL ni porcentajes; un test lo exige.
> - Un id que no sea VIGENTE da un error que lo nombra.
> - Sin ablación, el conjunto de reglas que recibe el intérprete es idéntico al de main.
> - La ablación de una de las 11 que no disparan da delta cero sobre un mes de construcción (el control).
> - La NOTA en ADR-0092 §6, que solo aplica §6 a la ablación: sus recuentos son diagnóstico de construcción y ninguna rama de spec o de motor se justifica con ellos; las ramas de spec citan al trader (ev-, fb-). Cómo se convierte una respuesta en regla lo fijará el ADR del método (RUMBO §1, rama de la preparación de la sesión 7): la NOTA no lo adelanta. Lo mismo, en el docstring del diagnóstico.
>
> F4 · LAS CORRIDAS (una a la vez, nunca junto a un make check)
> 1. La base de la rama frente a la línea base: diff contra cuenta-por-mes.txt, que tiene que dar 0 bytes. Si da algo, PARADA.
> 2. La bitácora de los cuatro días, sesiones enteras, al anexo.
> 3. La ablación de las 32 VIGENTE, una a una. Tabla: la regla; las parejas que se ganan y se pierden (qué filas de RECORRIDA-CONSTRUCCION-2 §8); las operaciones de más que aparecen y desaparecen; el delta de órdenes colocadas; y si la corrida falló o se detuvo, con el error. Si alguna de las 11 del control no da delta cero, PARADA.
>
> F5 · LAS CLASES PROPUESTAS
> - Las 5 de 07-03 07-11, con (i) a (iii) y las clases de «La tensión de 07-03».
> - Las 13 «a la rama de trazas».
> - La pendiente con dueño: 07-14 (o10, o12 y o14: si son del mismo barrido, de qué toma y de qué escenario, y por qué RN-016 no frenó); 04-13 08:47 (qué gate prohibió); 07-02 (las de 12:25 y 12:45).
> - De la ablación: por cada regla con delta, una línea con las filas que mueve. Ninguna conclusión del tipo «quitar la regla».
> - Lo que vaya a la sesión 7 como pregunta, escrito como hecho medido y sin sugerir la respuesta.
> - Propuestas para la orden de cierre: el texto nuevo de F (sale el (1); F sigue viva, así que ningún encabezado de HECHA); R4.4 HECHA y sin NA:F en sus Refs, como R3.8 (si no, problemas_b de test_hoja_de_ruta.py la da por mala); y las líneas de Technical Debt nuevas. Cada una comprobada con las funciones de tests/unit/test_hoja_de_ruta.py sobre una copia.
>
> INFORME: docs/validation/TRAZAS-ABLACION.md, con el encargo frente a lo hecho, las desviaciones y los comandos tal como se ejecutaron.
> CI: la rama escribe ficheros nuevos en data/ y puede tocar el nombrado de rutas de diagnostico.py, así que por RITUAL.md se empuja como fix/trabajo-trazas-ablacion y pasa la CI de Linux antes de declararla lista; da el número de run. El único fallo aceptado es el de state check por el nombre fix/.
> REVISOR (agente revisor), con estos alcances: (1) que nada cambie lo que el motor decide (golden y mutación); (2) que `motor arnes` y `motor visor` no cambien, y la etiqueta y el nombrado de la salida; (3) el holdout y HOLDOUT-EXPOSICIONES; (4) el recorte frente a (a)-(e), línea a línea; (5) que las clases de 07-03 citen S-18 y A-32 y los hechos de la bitácora; (6) que ninguna salida nueva lleve R, PnL ni porcentajes. Su informe, pegado al final del tuyo.
> Termina con la PARADA final con las clases para que yo decida, y la frase «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-09)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/trazas-ablacion (2026-11-09). Cópiala tal cual al informe con la skill fase-cero y aplícala punto por punto.
>
> 0. El enganche. Campo observador opcional en MotorCableado para lo que no es del intérprete (tomas, escenarios, zonas, puntos, órdenes): de acuerdo. Pero el gate que prohíbe NO se deduce del orden de las disparadas: se apunta en el intérprete, en el sitio donde se prohíbe. Por qué: deducirlo del orden es la clase de error del revisor a1 de RECORRIDA-CONSTRUCCION-2 (atribuir a RN-032 el bloqueo de RN-015), y no cubre el caso que tú mismo mediste, un gate DESCONOCIDO que bloquea sin disparar: en interprete.py, quizas_prohibidos (:323-335) se rehace en cada pasada y no_implementadas acumula sin la pasada, así que no se puede reconstruir después. Cómo:
>    - el Evento gana un registro de quién prohíbe cada efecto (los gates que dispararon y lo prohibieron, en _ejecutar hacia :260) y, en cada acción bloqueada, qué gates lo hicieron, también los desconocidos de esa pasada (hacia :270-274). quizas_prohibidos puede pasar a llevar los ids, sin cambiar qué se bloquea;
>    - es solo registro: nada lo lee para decidir. Un test lo fija sobre el fixture, con un gate que dispara y uno desconocido prohibiendo lo mismo: salen los dos;
>    - la prueba de que no cambia ninguna decisión es la de F4.1: motor arnes con el código de la rama da un diff de 0 bytes contra cuenta-por-mes.txt.
>    Cambia lo que dije en el encargo (sin tocar el intérprete): lo dejo escrito como desviación decidida por mí.
>
> 1. Etiqueta y nombre: DIAGNOSTICO-DECISIONES con nombrado propio, y nombre_etiquetado arreglado para que «DIAGNOSTICO-A» solo acepte una ambigüedad (A seguida de cifras) y rechace todo lo demás, con su test que rompe en main. De acuerdo.
>
> 2. La relectura de 07-03: de acuerdo con medir el punto, su vela, la vela de M1 del llenado (con o sin cuerpo) y si la línea viene de M15. Añade dos datos por orden:
>    (a) si el llenado ocurrió ANTES o DESPUÉS de la primera vela de M1 que cierra más allá del punto;
>    (b) qué toma de M15 abrió el escenario y si su vela cerró con cuerpo.
>    Las clases propuestas quedan así:
>    - error nuestro: el punto o la toma tratan como de M1 una línea de M15, o la toma de M15 se dio con mecha;
>    - contradicción con lo fijado: el punto es un pivote de M1 y el llenado fue con mecha, contra la voz de v12 y con S-18 a favor del bot;
>    - y, si (a) dice que el bot entra antes de que ninguna M1 cierre más allá, propones además «regla desconocida: cuándo se coloca la orden respecto de la ruptura» (toca ADR-0064 y orden_limite_nace). No se cambia nada: decido yo en la PARADA final.
>
> 3. El subcomando: motor decisiones, de acuerdo. --carpeta es obligatorio y la raíz sale de ese argumento (CLAUDE.md, «Ensayos aislados», punto 2), con un test que niega una carpeta fuera de data/. Perfil y fase, los mismos por defecto que la línea base; sin --depuracion.
>
> 4. Los tests de F2 y F3 sobre el fixture sintético de test_cableado.py: de acuerdo. Ningún test lee meses reales. La prueba sobre la construcción entera es F4.
>
> 5. El Marcador: sin fila, declarado en el informe como excepción a HOJA-DE-RUTA.md:817, con el motivo (la corrida base repite la línea base con diff de 0 bytes y no es una corrida nueva; las ablaciones son diagnóstico). La orden de cierre lo dirá.
>
> 6. Un solo proceso, de acuerdo, con dos condiciones:
>    - cada ablación con un motor y un estado nuevos; las velas y los ticks pueden compartirse solo si son de lectura. Antes de las 32, la base corrida dos veces en el mismo proceso tiene que dar recuentos idénticos entre sí y a los de F4.1;
>    - el umbral de 1,5 GiB: si lo pasa, un proceso por ablación, dicho.
>
> 7. El control. El conjunto de control NO es mi lista de 11: lo calcula la bitácora de la base, como las VIGENTE que en toda la construcción ni disparan ni quedan desconocidas en ningún evento. Ese conjunto tiene que dar delta cero; si alguna no lo da, PARADA. RN-008 (que toca la memoria del día al evaluarse) y cualquiera que quede fuera del control se miden como las demás y se explican.
>
> 8. Herencias de tu auditor:
>    - traza_por_cierre.py se queda como está. El informe dice qué cubre la bitácora de lo que hacía y en qué se diferencia (cuenta por mes frente a día suelto);
>    - la deuda de la zona reutilizada (PUNTO-USADO.md §1.c y §4.f) entra en el análisis de 07-14: di, con la bitácora, si sus cierres contaron en los cartuchos de otro escenario y si eso explica que RN-016 no frenara;
>    - la carpeta desde un argumento, en el punto 3; los tests sin meses reales, en el punto 4.
>
> 9. Correcciones mías al encargo, que apuntas como desviaciones: la rama de CI es fix/trazas-ablacion (RITUAL.md:102), no fix/trabajo-trazas-ablacion; NA:F no aparece en ningún sitio del bloque de R4.4 al proponerla HECHA; las corridas pueden llevar unas 4 h.
>
> 10. Sigue. Haz F1 ya, en su commit. Después F2, F3 y F4 sin esperarme, con la PARADA condicional: paras solo si el diff de F4.1 no da 0 bytes, si la base repetida en proceso no cuadra, si alguna regla del control no da delta cero o si el diseño del punto 0 no puede ser solo registro. Si todo cuadra, sigue con F5 hasta la PARADA final, el revisor (agente revisor) y «Rama lista para revisión, NO cerrada». Antes de la primera corrida de cada día, su fila en HOLDOUT-EXPOSICIONES.md.
