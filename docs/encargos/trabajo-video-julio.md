# Encargo · trabajo/video-julio

Dado por Aleks (consultor) el 2026-11-08. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Encargo del consultor (2026-11-08): rama trabajo/video-julio, la entrada T de la Next Action (R2.4 de docs/plan/HOJA-DE-RUTA.md; ENTRADA-JULIO.md §5), la primera del orden de docs/plan/RUMBO-2026-11.md. Ábrela con la skill abrir-rama y copia este encargo tal cual en docs/encargos/trabajo-video-julio.md. Trabaja en la laptop (hacen falta el corpus, los vídeos y la GPU). Antes de empezar, comprueba con /model que estás en Opus 5.5 con esfuerzo alto.
>
> BASE (compruébala con git al abrir, como manda abrir-rama): main y origin/main en 5a54b46, commit de estado sobre el merge 86f306a, tag stable/F38t-recorrida-construccion-2 (el último «- Tag:» de HISTORIA); CI de main sobre 5a54b46: run 42550658681 en verde; ninguna otra rama local ni remota. Si algo no cuadra, PARADA antes del primer commit.
>
> OBJETIVO, en una frase: oír al trader sobre julio. Se transcriben v11 a v14, se comprueba qué días cubre cada vídeo y se compara el vídeo con los casos del libro de julio (días 1 a 17), operación por operación y hora por hora. Con eso se prepara la clasificación de las 81 filas de julio que RECORRIDA-CONSTRUCCION-2.md §8 dejó «sin clase hasta T», y el inventario de los días 20 a 31, que solo están en v14 y que el consultor necesita para decidir U.
>
> QUÉ NO CAMBIA
> - No se tocan src/, knowledge/spec/, knowledge/evidence/, knowledge/feedback/, knowledge/cases/dev/ ni ningún reparto, ni libros.yaml, parámetros, umbrales o tolerancias.
> - Los tests no cambian, salvo los que enumeran el corpus (0.3) y el que fija el valor antiguo de material_sin_video (F5).
> - No se corre el arnés, ni el motor, ni el visor. El lado del bot sale de lo ya commiteado en docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/ (para-clasificar.txt, patrones-cuenta-por-mes.txt, visor-sesiones.txt).
> - Lo único de knowledge/ que cambia:
>   · los manifiestos nuevos de transcripciones y fotogramas (inmutables desde su commit);
>   · la naturaleza de v11 a v14 y el comentario de knowledge/corpus/fuentes.yaml:116-118, más lo que corpus inventory regenere de ellos;
>   · el bloque material_sin_video de knowledge/cases/criterio_fidelidad.yaml (F5).
> - Fuera de knowledge/: el informe y su anexo, HOLDOUT-EXPOSICIONES.md y un RECUADRO DE CORRECCIÓN en ENTRADA-JULIO.md §5. El recuadro dice que la frase «con el guion de main y su cuarentena» era un error: scripts/transcribir_sesion.py falla cerrado con un vídeo que no es una sesión, y la vía es `corpus transcribe`. El cuerpo del informe no se toca.
> - El contrato cubre exactamente eso.
>
> LO QUE SE PUEDE MIRAR (CLAUDE.md, «Que se puede mirar y que no»)
> - Julio es construcción (ADR-0078). En la fase 0, compruébalo para el mes ENTERO, también del 18 al 31:
>   · casos_reservados(repo) y casos_ocultos(repo) por día, contando y sin imprimir ids;
>   · que 7 está en cases.holdout.meses_libres (hoy deberían salir 1, 4, 7, 8, 10 y 11: verifícalo).
> - LOS DÍAS 20 A 31 SE MIRAN EN ESTA RAMA. Decisión del consultor del 2026-11-08, con estos motivos:
>   · no tienen libro y no son construcción, pero tampoco reservados: julio no tiene ningún día en ninguna partición y está en vistos.yaml;
>   · ADR-0078 §3 manda decidir qué se hace con ellos DESPUÉS de transcribir v11 a v14.
>   La cautela de las sesiones 5 y 6 («julio del 18 en adelante», PARADA o no citable) fue una decisión para esas sesiones y no sale de ningún ADR. Queda levantada para v11 a v14. Siguen en pie dos cosas:
>   · los tramos no citables ya escritos, entre ellos v16 0:30:41-0:31:37;
>   · la decisión 5 de la respuesta a la PARADA de v16 (SESION-05-EXTRACCION.md): el dato de ese tramo no se usa.
>   Lo que v14 cubra se mide en v14, como fuente propia. Si algo tapa los días 20 a 31 (un tramo, la guardia o la CLI), PARADA: no se rodea.
> - EL TEXTO SE LEE SOLO POR LA CLI FILTRADA: uv run botsito corpus transcript show, uv run botsito kb find, uv run botsito kb at.
>   · Nunca con Read, Grep, cat ni guiones propios sobre data/transcripciones/. Ni la guardia ni tests/unit/test_cuarentena.py lo impiden para v11-v14 (auditor del consultor): es una regla de este encargo, por MIRAR-EL-MATERIAL.md (la CLI es la vía de lectura desde F36l).
>   · Propón para el cierre una línea de Technical Debt del carril de guardias: «la guardia no niega leer con Read las crudas de data/transcripciones/ de un vídeo sin cuarentena ni tramos».
>   · La cuarentena por condición tapa los meses no libres (hoy 2, 3, 5, 6, 9 y 12), las fechas numéricas, un día de la semana con número y «backtest» con la abreviatura de un mes tapado, más el segmento anterior y el siguiente. NO tapa un día de julio dicho con palabras.
>   · Di en el informe cuántos segmentos ocultó cada vídeo y por qué motivo, sin el texto.
> - FOTOGRAMAS: solo por instante localizado antes en la transcripción (ADR-0038).
>   · Se abren con uv run botsito corpus frames show --video <v> --t h:mm:ss [--n N] y Read sobre la ruta que imprime.
>   · Antes de abrir uno, comprueba con transcript show que en ±30 s no hay ningún segmento oculto. Si lo hay, ese instante no se abre y se apunta.
>   · Ninguna vista de Analytics ni panel de estadística, de ningún mes. FX Replay la enseña a veces dentro del vídeo: si la transcripción habla de estadísticas o del resultado del mes, ahí no se abre nada.
>   · Si un fotograma abierto así trae un agregado o una vista de Analytics, se declara el mismo día con sus cifras en HOLDOUT-EXPOSICIONES.md y ninguna se usa (ADR-0038 §2).
>   · Si enseña un gráfico de un mes que no sea julio de 2026, se cierra, no se describe, y PARADA con el vídeo y el instante.
> - Las seis capturas de resumen de Backtest Julio 2026 siguen sin abrirse.
> - Las cifras de resultados que el trader diga en voz (del mes o de una racha) no se copian ni se usan: se dice dónde están.
> - HOLDOUT-EXPOSICIONES.md lleva una fila por cada día de trabajo de la rama, escrita ANTES del primer make check de ese día (cada make check lee el M1 de marzo y calienta con el de junio: Technical Debt). La fila dice lo de julio que se leyó ese día:
>   · qué vídeos se transcribieron;
>   · cuántos fotogramas se abrieron y de qué vídeos;
>   · que se vieron los días 20 a 31 en v14, sin números de días en la fila más allá de «20 a 31».
>
> FASE 0 (skill fase-cero, con el agente auditor-encargo sobre este encargo). No se escribe en el repo salvo la apertura.
> 0.1 La base y lo de julio de arriba. Los cuatro .mkv de corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/ con los bytes y el sha256 de ENTRADA-JULIO.md §0.d (sha256sum, sin abrir nada). Si alguno no coincide, PARADA.
> 0.2 Antes de usar cada herramienta o salida, escribe qué campos da, medido sobre una ejecución. Es la lección de F38t: tres veces se pidió a una herramienta algo que no daba. Las de esta rama:
>   · corpus transcribe, transcript show, frames extract y frames show;
>   · los casos de julio (knowledge/cases/dev/caso-eurusd-2026-07-*.yaml);
>   · para-clasificar.txt, patrones-cuenta-por-mes.txt y visor-sesiones.txt.
>   Ya medido por el auditor del consultor, verifícalo: para-clasificar.txt no trae la regla que explica una orden del bot, solo los frenos pegados al «primer hecho que falta».
> 0.3 Qué cambia al registrar cuatro transcripciones y cuatro extracciones: qué tests o guardias cuentan o listan transcripciones, fotogramas o vídeos, y qué regenera corpus inventory al cambiar una naturaleza en fuentes.yaml. Los tests que solo enumeran el corpus se ponen al día en el mismo commit, diciendo por qué.
> 0.4 Qué tests leen material_sin_video y las validaciones de cargar_criterio. Se sabe que test_metodo_adr0092.py:445 afirma que 2026-07-08 cuenta como grabado; mira también test_criterio_campos_adr0092.py. Di qué rompería cada una de las dos salidas de F5.
> 0.5 Herencias: busca «video-julio», «rama del vídeo», «rama que transcriba», «lo comprueba la rama» y «hasta T» en PROJECT_STATE, el final de HISTORIA, docs/validation/, docs/adr/, knowledge/corpus/fuentes.yaml y knowledge/cases/*.yaml. Todo lo que se deje a esta rama entra en ella, o se dice por qué no. Las conocidas:
>   · ENTRADA-JULIO.md §5 y §8;
>   · ADR-0078 §3;
>   · fuentes.yaml:116-155;
>   · ADR-0092 §11 y el comentario de criterio_fidelidad.yaml (julio cuenta como grabado de forma provisional hasta T);
>   · RECORRIDA-CONSTRUCCION-2.md §8 (81 filas, destino T, y la pendiente con dueño de 07-02 y 07-14);
>   · S-25 de la sesión 5 (SESION-05-EXTRACCION.md, «S-25 · El Excel de julio y los tres primeros vídeos»): el trader cree que el Excel exporta los tres primeros vídeos y dice que «todo está grabado»; F2 y F3 lo contrastan.
> 0.6 Tiempo esperado. Las transcripciones de las sesiones tuvieron factor 0,20 (v17) y 0,32 (v16): estima los cuatro vídeos. Da también el PICO DE MEMORIA del último make check.
> Si todo cuadra con este encargo, NO pares: escribe la fase 0 en el informe y sigue. PARADA solo si algo no cuadra, con la decisión que necesitas y tu recomendación.
>
> F1 · TRANSCRIPCIÓN Y FOTOGRAMAS
> Uno a uno, nunca dos a la vez ni mientras corre un make check. Si los lanzas en segundo plano, arranca Claude Code con CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1.
>   uv run botsito corpus transcribe --video v11      (luego v12, v13 y v14)
>   uv run botsito corpus frames extract --video v11  (luego v12, v13 y v14)
>   uv run botsito corpus transcript check
>   uv run botsito corpus frames check
> - Si la guardia niega algo legítimo, no se rodea: PARADA con el comando exacto, y lo lanza Aleks con «!».
> - Los manifiestos nuevos van en su commit, sin editar.
> - Fuera de git, para Aleks: SHA256SUMS-v11-v14.txt con cada fichero de data/transcripciones/v11..v14 (ruta y sha256), en la carpeta de trabajo. El informe dice dónde está y cuántas líneas tiene, para que lo suba a «botsito copia a4».
>
> F2 · QUÉ CUBRE CADA VÍDEO
> Por vídeo, con la transcripción filtrada y con fotogramas localizados cuando la voz no baste: los días de julio que el trader opera o comenta, en orden, con el instante en que empieza cada uno. Contrástalo con lo que dijo (v11-v13 del 1 al 17; v14 desde el 20; S-25). Si un vídeo trae días de otro tramo, o algún día del 1 al 17 no aparece, se dice; no es PARADA.
>
> F3 · EL VÍDEO FRENTE AL LIBRO, DÍAS 1 A 17
> Antes de abrir nada, escribe en el informe este criterio, que fija el consultor:
> - La unidad son las operaciones de los 13 casos dev de julio. Para cada una: ¿aparece en el vídeo? Si aparece: día, dirección, entrada y stop leídos en pantalla, y la hora del gráfico.
> - «Coincide» quiere decir:
>   · mismo día y misma dirección;
>   · entrada y stop a 3 puntos o menos (tolerancia_entrada_puntos y tolerancia_stop_puntos de criterio_fidelidad.yaml). El libro y el gráfico son la misma serie de FX Replay, así que toda diferencia se apunta con su cifra;
>   · la hora del gráfico, en Europe/Madrid (UTC+2 en julio, ADR-0069), en el mismo minuto que instante_utc + 2 h. instante_utc es el llenado.
> - Las operaciones que el vídeo enseña y no están en los casos, y las de los casos que no se ven en el vídeo, se listan aparte, sin resolverlas.
> - Con lo medido, confirma o refuta que el libro está en Europe/Madrid (ENTRADA-JULIO.md §3.b). Es la comprobación de las «horas del libro» de T.
> Primero un piloto con tres operaciones de 2026-07-02 11-15. Si se localizan al menos dos con fecha, entrada y stop legibles, sigue con el mes entero; si no, PARADA con lo que viste y una propuesta.
> Los guiones van en docs/validation/anexos/VIDEO-JULIO/, con su salida.
>
> F4 · LAS 81 FILAS «SIN CLASE HASTA T»
> Son las de RECORRIDA-CONSTRUCCION-2.md §8: P1 20, P2 de más de 10 puntos 7, P3 15, P5 37 y P6 2, en 22 sesiones de los 13 días. Reprodúcelas con un guion del anexo sobre patrones-cuenta-por-mes.txt y para-clasificar.txt, y PARADA si no salen 81.
> Agrupadas por sesión, para cada fila:
>   · lo que el trader dice y hace en el vídeo en ese tramo: cita literal de la transcripción filtrada, con vídeo y h:mm:ss, y el fotograma si lo abriste;
>   · lo que hizo el bot, según para-clasificar.txt: el bot más cercano, Δentrada, Δinstante, el primer hecho que falta y los frenos;
>   · una clase PROPUESTA de RUMBO-2026-11.md §1 (e) (error nuestro, regla desconocida, efecto de la cuenta, material incompleto o sin clase), con su porqué en una línea. Tú propones; la clase la decide el consultor en la PARADA.
> Además:
> - Si propones «regla desconocida»: la pregunta para el trader en su idioma (sesgo de H4, liquidez de M15, caja, 0 y 0,8; nunca ids de reglas) y las filas que podría mover (RUMBO §1 a). No se escribe en ningún yaml.
> - Si propones «error nuestro»: qué pieza del motor sospechas, sin tocarla. Va a la rama de trazas (R4.x).
> - 07-02 y 07-14 están también en la pendiente con dueño de §8, que es de la rama de trazas. Aquí solo va lo que dice el trader; el motor lo mide esa rama.
> - Marca las filas del 1 de julio y las de sesiones con una hora de ticks perdida (verifica: 07-10 05h, 07-14 12h y 07-16 11h UTC, ENTRADA-JULIO.md §4).
> - Ninguna cifra de resultados del bot más allá de las que ya trae para-clasificar.txt.
>
> F5 · MATERIAL_SIN_VIDEO
> ADR-0092 §11 dice: «si T comprueba julio, el bloque se cambia en la rama que lo traiga, con su fuente». Con lo medido en F2 y F3:
> - si los 13 días dev están grabados en v11-v13 y ninguna operación de los casos que se ve en el vídeo deja de coincidir, 2026-07 sale de provisionales_con_video;
> - si no, 2026-07 pasa a meses y dias_con_video lleva los días de julio grabados que coinciden.
> En los dos casos:
> - fuente: VIDEO-JULIO.md §<sección>, y el comentario del bloque, al día;
> - un commit propio con «Fuente: ADR-0092» en el cuerpo del mensaje;
> - en el mismo commit, la naturaleza de v11 a v14 en fuentes.yaml y su comentario dicen lo comprobado;
> - se actualiza el test que fija el valor antiguo (test_metodo_adr0092.py:445 u otro que fije exactamente ese valor). Si rompe cualquier otro test o cargar_criterio, PARADA con el mensaje.
>
> F6 · LOS DÍAS 20 A 31 (para que el consultor decida U; no se extrae ningún caso)
> Por día: cuántas operaciones narra el trader en v14, y si en un fotograma localizado se leen día, dirección, entrada, stop y hora (cuéntalo; dos ejemplos como mucho). Ni casos, ni libros.yaml, ni reparto.
>
> F7 · CANDIDATAS A EVIDENCIA
> Los tramos de v11-v14 que sostendrían una regla o una respuesta (por ejemplo, el porqué de un descarte), con vídeo y h:mm:ss. No se crea ningún ítem: el consultor decide cuáles en la PARADA.
>
> INFORME: docs/validation/VIDEO-JULIO.md (plantilla _template.md). Lleva:
> - la base y la fase 0;
> - las cuatro transcripciones: id, segmentos y ocultos por motivo;
> - F2 a F7 con sus tablas;
> - lo que NO cambia, medido con git diff main --stat;
> - las exposiciones de cada día;
> - los make check de la rama: exit, passed, SELLO y PICO DE MEMORIA;
> - las propuestas para la orden de cierre, cada una comprobada contra test_hoja_de_ruta:
>   · T sale de la Next Action, HECHA. HISTORIA ya tiene un «Next Action HECHA · T» del 2026-10-05 y un «· U», y el test usa un conjunto, así que el registro nuevo lleva un encabezado que lo distinga (propón cuál). Que el test no vea su falta va también a la deuda del carril de guardias;
>   · R2.4 reescrita. Si U sigue viva, R2.4 no puede ir HECHA ni citar NA:T: propón el texto, por ejemplo R2.4 con solo NA:U y un Estado que diga que T está hecha, o lo que pase el test;
>   · U, con la decisión del consultor tras la PARADA; su «Depende de T» sale;
>   · F: el punto (1) sale y el resto se renumera;
>   · el Marcador no cambia, porque no hay corrida;
>   · las filas de §8 de RECORRIDA-CONSTRUCCION-2.md que reclasifique la PARADA, para la rama que use la clasificación;
>   · la línea de Technical Debt de la lectura de las crudas (arriba).
> Commits en el orden de CLAUDE.md: estadiar → make check > make-check.log 2>&1 → leer exit 0, ningún failed y la línea SELLO → commit. Nunca --no-verify. Los mensajes, escritos con Write y git commit -F. Nada escribe mientras corre make check.
>
> AL TERMINAR: el agente revisor (.claude/agents/revisor.md) con el alcance de este encargo. Su informe va tal cual al final del informe, con lo hecho con cada hallazgo.
> Después, PARADA final con lo que tiene que decidir el consultor:
>   · la clase de cada fila de F4, agrupadas por sesión y por clase propuesta;
>   · U (F6);
>   · las candidatas de F7;
>   · cualquier desviación.
> Termina con «Rama lista para revisión, NO cerrada». No se cierra nada sin la orden de Aleks.

## Respuesta del consultor a las cuatro preguntas de la fase 0 (2026-11-08)

Copiada tal cual:

> Respuesta del consultor a las cuatro preguntas de la fase 0 de trabajo/video-julio (2026-11-08). Cópiala tal cual en el informe, en su sección, y aplícala. No pares la rama: sigue con todo.
>
> 1. La decisión 1 de la PARADA de v16: opción (a), con este alcance.
>    - Sigue en pie para su objeto. El tramo v16 0:30:41-0:31:37 sigue siendo no citable. Su número no se escribe en ningún sitio como dato de v16, ni se compara con lo que dé v14 (y la decisión 5 tampoco cambia).
>    - No alcanza a v14. La decisión 1 se tomó bajo la cautela de «julio del 18 en adelante», que este encargo levanta para v11-v14 por ADR-0078 §3 y porque julio no tiene días en ninguna partición. Lo que v14 enseñe, días incluidos, se mide en v14 como fuente propia y se escribe en el informe (F2 y F6).
>    - La fila de HOLDOUT-EXPOSICIONES sigue diciendo solo «20 a 31», como manda el encargo.
>    - No hace falta la PARADA parcial: sigue con F1 a F7.
>
> 2. F5: de acuerdo con los goldens, y la segunda vía tampoco para.
>    - Los tres tests/golden/metodo_adr0092/main-*.txt fijan en su línea 18 el valor viejo («provisionales hasta que T lo compruebe: 2026-07»). Se regeneran en el commit de F5 por el procedimiento documentado (test_cuenta_por_mes.py:10, test_el_volcado_de_los_escenarios con -s), nunca a mano. El diff tiene que ser solo esa línea; si cambia cualquier otra, PARADA. Amplía el contrato a esos tres ficheros.
>    - Si F5 sale por la segunda vía, test_criterio_campos_adr0092.py:104 no fija el valor viejo: comprueba la regla «un día con vídeo cuyo mes no está en meses» y usa julio de ejemplo. Con julio en meses ya no queda ningún mes de construcción fuera de meses, así que se rehace ese caso para que siga probando la MISMA regla: la copia del criterio lleva meses sin un mes de construcción y dias_con_video con un día de ese mes. Antes de commitear, demuestra que el caso rehecho falla si se quita esa comprobación de cargar_criterio (en un clon desechable con git worktree add, como manda CLAUDE.md) y pega la salida en el informe. Amplía el contrato a ese test. PARADA solo si rompe cualquier otra cosa.
>
> 3. F4 de dos ficheros: de acuerdo. Las 39 filas P5 y P6 van sin primer hecho ni frenos, y el informe lo dice.
>
> 4. Los ocultos, por motivo a, b o c: de acuerdo. Nada sin filtrar.

## Respuesta del consultor a la PARADA 1 (2026-11-08)

Copiada tal cual (y en `docs/validation/VIDEO-JULIO.md`, «Respuesta del consultor a la PARADA 1»):

> Respuesta del consultor a la PARADA 1 de trabajo/video-julio (2026-11-08). Cópiala tal cual en el informe, en su sección, y aplícala. Desviación aceptada: los ocho manifiestos de F1 van en el commit de la fase 0 (c87cff5).
>
> 0. Qué cuenta como «un gráfico de un mes que no sea julio». Opción (a), precisada:
>    - Las velas de contexto de otros meses, a la izquierda de un gráfico de julio, se pueden ver. Las velas no son holdout (ADR-0021 §1; CLAUDE.md, «Que se puede mirar y que no», punto 2). No se describen, no se comparan con nada y no se usan. Se declaran una vez en la fila del día de HOLDOUT-EXPOSICIONES («fotogramas de v11-v14 con velas de contexto de meses anteriores a julio, sin marcas del trader»).
>    - Lo que NO se mira de otro mes:
>      · el cursor del replay situado fuera de julio de 2026;
>      · las marcas del trader (cajas, niveles, líneas, órdenes o posiciones) sobre velas de un día que no sea de julio de 2026;
>      · cualquier panel de operaciones o de estadística.
>      Si un fotograma lo trae, se cierra, no se describe, se apunta vídeo e instante y se declara el mismo día. No es PARADA: sigue con el siguiente instante localizado.
>    - PARADA solo si el trader opera o comenta en voz operaciones de otro mes. Es un tramo que podría tener que ir a tramos_no_citables.yaml, y eso lo decide el consultor.
>
> 1. El poco texto de v13 y v14: ni (a) ni (b). Primero se mide, sin que Aleks escuche nada:
>    1.1 Con ffmpeg (las formas de GUARDIA-FFMPEG.md: volumedetect y silencedetect=noise=-50dB:d=30), sobre v11 como control y sobre v13 y v14:
>        - el volumen medio del vídeo entero;
>        - los silencios de 30 s o más;
>        - el volumen medio de cada hueco sin texto de 5 minutos o más (con -ss y -t sobre el hueco).
>        Si la guardia niega el comando, PARADA con el comando exacto y lo lanza Aleks con «!».
>    1.2 Regla de decisión, escrita en el informe ANTES de medir:
>        - si los huecos de v13 o v14 no son silencio (menos de la mitad de su duración cae en un silencio de silencedetect y su volumen medio está a menos de 10 dB del de v11), el ASR se saltó voz;
>        - si son silencio, el texto es el que hay, y el informe dice dónde no habla el trader.
>    1.3 Si el ASR se saltó voz: retranscribe v13 y v14 con uv run botsito corpus transcribe --video v13 --reemplaza-a <su tr-id> --objetivo-s 300 --min-s 180 --max-s 420 (y lo mismo con v14). Uno a uno, nunca mientras corre un make check.
>        - Se queda la transcripción que cubra con texto más minutos de los huecos.
>        - Si la nueva tampoco los cubre, PARADA con lo medido: entonces Aleks escucha un minuto.
>        - Los manifiestos nuevos, en su commit, sin editar los anteriores.
>        - transcript check en verde, y el número de segmentos y de ocultos por motivo de las dos versiones, en el informe.
>    1.4 Haz 1.1 a 1.3 antes de F2 y F4 de los días de v13 y v14. El piloto de F3 (2026-07-02, en v11) y lo de v11 y v12 no esperan.
>
> 2. El SHA256SUMS:
>    - Regenéralo al final de F1 o de 1.3, con las transcripciones que queden activas y también las reemplazadas.
>    - Escríbelo en C:\Users\USER\Desktop\SHA256SUMS-v11-v14.txt (fuera del repo y de la carpeta temporal).
>    - El informe dice cuántas líneas tiene.
>
> Sigue sin parar hasta la PARADA final: F2, F3 con el piloto, F4 a F7 y el revisor.

## Respuesta del consultor a las PARADAS 2 y 3 (2026-11-09)

Copiada tal cual:

> Respuesta del consultor a las PARADAS 2 y 3 de trabajo/video-julio (2026-11-09). Cópiala tal cual en el informe, en su sección, y aplícala.
>
> PARADA 2. Aleks acaba de lanzar con «!» los cuatro comandos de §1.6, y sus líneas mean_volume están arriba en esta conversación. Cópialas al informe y aplica la regla de decisión escrita antes de medir: el umbral es -49,0 dB, a 10 dB del -39,0 de v11.
> - Si algún hueco de v14 da más de -49,0 dB, retranscribe v14 con el punto 1.3 de la respuesta a la PARADA 1 (--reemplaza-a, --objetivo-s 300, --min-s 180, --max-s 420), con su manifiesto en su commit. Se queda la transcripción que cubra con texto más minutos de los huecos. Si la nueva tampoco los cubre, PARADA con lo medido.
> - Si ninguno pasa de -49,0 dB, el texto es el que hay, y el informe dice dónde no habla el trader.
> - El volumen no distingue voz de música. El informe lo dice al lado de la decisión, sin cambiar la regla.
> - La negativa de la guardia a ffmpeg con -ss/-t sobre un vídeo del corpus es un falso positivo de la lista cerrada de GUARDIA-FFMPEG. Va como línea de Technical Debt del carril de guardias en las propuestas para la orden de cierre. Aquí no se toca la guardia.
>
> PARADA 3. La grabación no enseña el eje de precios y el stop nunca se ve: es un límite del instrumento, medido en el piloto, no un resultado. F3 sigue con (a) más (b), y este criterio se escribe en el informe ANTES de comparar el resto:
> - Tres categorías por operación de los 13 casos:
>   · COINCIDE: día, dirección y hora en Europe/Madrid (el mismo minuto que instante_utc + 2 h), con la entrada leída en el aviso de cierre a 3 puntos o menos;
>   · APARECE SIN ENTRADA LEGIBLE: día, dirección y hora por la marca del trader o por su voz, sin cifra de entrada (para cada operación busca antes su aviso de cierre);
>   · NO APARECE.
>   Además, CONTRADICE: aparece con otra dirección, a otra hora, o con la entrada a más de 3 puntos.
> - El stop va como «no legible» en todas, y el informe dice que el vídeo no sirve para el stop: la caja dispersa (A-48) se le pregunta al trader en directo en la sesión 7.
> - Las operaciones del vídeo que no están en los casos se listan aparte, como dice el encargo.
> - F5 cuenta así:
>   · primera vía (julio sale de provisionales_con_video): las operaciones de los 13 días están todas en COINCIDE o en APARECE, ninguna CONTRADICE y ninguna está en NO APARECE;
>   · si no, segunda vía, y dias_con_video lleva los días en que se cumple eso.
>   Es lo que pregunta material_sin_video (S-14): si las sesiones del libro están grabadas. El stop no cambia esa respuesta.
> - El piloto vale con dos COINCIDE (2 y 10 de julio, Δ 0) y la confirmación de que el libro está en Europe/Madrid.
>
> Sigue sin parar hasta la PARADA final: lo que quede de F2, F3 con este criterio, F4 a F7, el SHA256SUMS en el Escritorio y el revisor.

## Respuesta del consultor a la PARADA 4 (2026-11-09)

Copiada tal cual:

> Respuesta del consultor a la PARADA 4 de trabajo/video-julio (2026-11-09). Cópiala tal cual en el informe, en su sección, y aplícala. No hay más PARADAS por el ASR: sigue hasta la PARADA final.
>
> 0. El minuto de escucha no bloquea la rama. Aleks escuchará v14 de 0:10:00 a 0:11:00 cuando pueda y te dirá en un mensaje aparte lo que oye. Apúntalo en el informe cuando llegue, y con eso escribe la propuesta del punto 5. No se retranscribe nada más en esta rama: si el trader habla, el problema es la configuración del VAD, que corpus transcribe no expone y que vive en src/.
>
> 1. Versión activa: opción (a).
>    - La nueva queda activa.
>    - Donde solo la vieja tiene texto, se cita la vieja por su id (transcript show --transcripcion <id>), y cada cita del informe dice de qué id sale.
>    - Para localizar fotogramas vale el texto de cualquiera de las dos versiones: las dos transcriben el mismo vídeo, y lo que localiza una cuenta como localizado (ADR-0038 §1).
>
> 2. Una operación que cae en un hueco sin texto en ninguna de las dos versiones va como NO LOCALIZABLE (HUECO DEL ASR), separada de NO APARECE. En los huecos no se abre ningún fotograma: muestrear está prohibido (ADR-0038). Las 3 «sin ver» del 10 de julio se cuentan igual que NO LOCALIZABLE en F5: no están comprobadas.
>
> 3. F5 tiene una tercera salida.
>    - La primera vía exige que ninguna operación de los 13 días sea NO LOCALIZABLE ni «sin ver». Si alguna lo es, el bloque material_sin_video NO cambia: julio sigue provisional y los goldens no se tocan. Que una operación no esté comprobada no quiere decir que no esté grabada, y ADR-0092 §11 solo cambia el bloque si T lo comprueba.
>    - La segunda vía (julio a meses) solo si hay alguna NO APARECE o CONTRADICE de verdad. En ese caso, PARADA con la lista, porque decidir qué días son sin vídeo con huecos de por medio lo decide el consultor.
>    - El informe da, por día, cuántas operaciones hay en cada categoría.
>
> 4. F4 de los días 13 a 17 y F6 de los días 20 a 31, con lo que hay.
>    - Una fila sin voz en ninguna versión va como «sin clase (voz no transcrita)».
>    - Un día de F6 sin voz ni fotograma localizado va como «sin datos (hueco del ASR)».
>    - U espera a la rama del punto 5, y el informe lo propone así para el cierre.
>
> 5. Para la orden de cierre, propone una entrada nueva de la Next Action, del carril de infraestructura y después de T:
>    - exponer en corpus transcribe la configuración del VAD (o su desactivación), con tests;
>    - retranscribir v12, v13 y v14 con --reemplaza-a;
>    - volver a medir en los huecos lo de F2, F3, F4 y F6 de esta rama.
>    Pon tu propuesta de condición de entrada: si el minuto de Aleks dice que el trader habla, la entrada va; si dice que solo hay música o silencio, no va, y el informe dice que el trader opera callado en esos tramos.
>
> Sigue: F2, F3 y F4 de los días 13 a 17, F5 con el punto 3, F6, el cierre del informe, el revisor y la PARADA final.

## El minuto de escucha y la decisión del consultor (2026-11-09)

Copiado tal cual:

> El minuto de escucha (Aleks, 2026-11-09): en v14 de 0:10:00 a 0:11:00 el trader solo dice «bias bajista», y se oye a Aleks toser; no hay más voz. Apúntalo en el informe (respuesta a la PARADA 4, punto 0).
> Decisión del consultor con eso:
> - El trader habla en los huecos, pero poco: el VAD se salta frases cortas como esa. La entrada nueva del punto 5 va a la propuesta de cierre, en el carril de infraestructura y con prioridad baja, en los huecos: no va antes de las trazas, de las láminas ni de la preparación de la sesión 7.
> - U ya NO espera a esa rama. El stop no se ve en el vídeo, así que un caso de los días 20 a 31 sacado del vídeo no tendría stop. U lo decide el consultor en la PARADA final con lo que dé F6: quita del informe la frase «U espera a la rama del punto 5».
> Sigue hasta la PARADA final.
