# Encargo · trabajo/sesion-05

Dado por Aleks (consultor) el 2026-10-25, en cuatro mensajes seguidos. Copiado tal cual, los cuatro
en su orden, sin las líneas de aviso del principio y del final de cada mensaje (la primera línea de
cada uno, la línea entre paréntesis «(fin del mensaje N de 4; …)» de los tres primeros y la línea
«FIN DEL ENCARGO» del cuarto):

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/sesion-05 (NA:V, hoja de ruta R4.1, tramo R4), desde main en 7eef8cf (el commit de estado sobre el merge 68eaa83, que es al que apunta el tag stable/F38c-guardia-alias; CI de main run 40161007232). Antes, git fetch --prune. Verifica con git que main es ese commit, que ese tag es el último stable y está en origin, que la CI de main sobre su HEAD está en success (una consulta suelta), que no hay otra rama abierta, que scripts/transcribir_sesion.py de main ya tiene la hoja 05 (HOJAS["05"] y SESION_EN_CURSO = "05") y que docs/runbooks/DECISIONES-DE-PROCESO.md ya tiene la regla del 2026-10-21; si algo no cuadra, para y avísame. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo (los cuatro mensajes, sin las líneas de aviso del principio y del final de cada uno), con la fecha de hoy, con Write (lleva el literal de una opción que la guardia vigila: va con Write o Edit, y los mensajes de commit que lo lleven, con git commit -F). Tag de cierre: stable/F38d-sesion-05.
>
> LA SESIÓN 5 SE GRABÓ EN DOS PARTES
> El 2026-10-23 se llegó hasta S-17 (Aleks: «me quedé en la pregunta S17»); el 2026-10-25 se siguió hasta S-25 y «Para cerrar». Son DOS vídeos de una MISMA sesión, con la misma hoja y los mismos códigos de voz: los dos se ingieren en esta rama. Duraciones que da Aleks: la primera, 1 h 40 min; la segunda, unos 35 min (verifica con ffprobe y da las cifras exactas). Aleks dice que se respondió todo el PDF y que las dos grabaciones están completas.
> - Video_ids: v15 para la del 2026-10-23 y v16 para la del 2026-10-25 (verifica que son los siguientes libres: hoy fuentes.yaml acaba en v14). Las dos con drive_id null y las dos en SESIONES_EN_CUARENTENA de src/botsito/corpus/cuarentena.py.
> - Id de la sesión: 2026-10-23-sesion-05 (el día en que empezó), para la evidencia, el feedback y el informe; cada vídeo con su fecha en fuentes.yaml. Antes del registro, mide si fuentes.yaml, la evidencia, el feedback, la cuarentena, transcribir_sesion.py y sus tests admiten dos vídeos para un mismo id de sesión (busca si alguna sesión anterior se partió en dos vídeos y cómo se hizo). Si algo no lo admite sin tocar código, PARADA con tu propuesta.
> - S-17 puede estar en los dos vídeos (empezada en uno y seguida en el otro): busca su código en las dos filtradas e infórmala con los dos tramos si los hay. Cada cita es de un solo vídeo: una respuesta repartida entre los dos se cita en dos evidencias.
> - Precedente: la sesión 2 se partió en v7 y v8 el mismo día (fuentes.yaml; SESION-02-VIDEO-V8.md «CONTINÚA la misma sesión»). Esta es la primera repartida en dos DÍAS: para la activación, apunta en el informe que un feedback que cite v16 llevará fecha 2026-10-23 y recibido_el 2026-10-25 (modelo.py, la fecha es la de la sesión); verifica la línea.
>
> OBJETIVO
> Ingerir la sesión 5 con el trader y entregar el informe de extracción por pregunta, siguiendo la skill ingerir-sesion de principio a fin, para v15 y v16. Esta rama NO resuelve nada: no hay feedback apply, ni ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos ni en las cifras. ADR-0081 y ADR-0083 siguen PROVISIONALES. scripts/transcribir_sesion.py no se toca: se ejecuta el de main. El destino de cada respuesta lo decido yo después, en otra rama (V, R4.1).
>
> REGLAS DE ESTA RAMA
> - Si la guardia o el clasificador niegan un comando: PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe (docs/runbooks/DECISIONES-DE-PROCESO.md). La guardia es nueva desde trabajo/guardia-ci y trabajo/guardia-alias (Monitor en el matcher, la espera de la CI, la canonización de la raíz): si te niega algo que la skill ingerir-sesion manda hacer, es un hallazgo, PARADA con el comando y el mensaje.
> - La CI no se consulta con un guion ni con un bucle: un gh run view suelto cada vez; si hay que esperar, una espera sin consulta (sleep en segundo plano) y después otra consulta suelta.
> - La cruda no la lee nadie. Los fotogramas, solo por instante localizado en la filtrada, como manda la skill.
> - corpus/Estrategia del trader/ se lista solo en su primer nivel: debajo está el material adicional, con carpetas de meses reservados.
> - Toda consulta de casos_ocultos y toda lectura de una filtrada se declaran en docs/validation/HOLDOUT-EXPOSICIONES.md el mismo día, aunque el resultado sea «nada».
> - Nada escribe en el repositorio mientras corre make check (la transcripción y los fotogramas rompen el sello), y make check NO se lanza entre el registro de v15/v16 en fuentes.yaml y su alta en SESIONES_EN_CUARENTENA (en esa ventana falla a propósito). Se sella por fase, como manda la skill.
> - La laptop tiene 16 GB de RAM: antes de lanzar CADA transcripción (una por vídeo, nunca las dos a la vez), avísame en el terminal para que cierre programas, y espera mi «listo».
>
> ENTRADAS
> - Vídeos: los copio yo a corpus/Estrategia del trader/ antes de pegar esto, con su nombre de origen («Grabación de pantalla 2026-10-23 174536» y «Grabación de pantalla 2026-10-25 140140», con su extensión). Son los dos únicos vídeos del primer nivel de esa carpeta que no están en knowledge/corpus/fuentes.yaml; si hay otro número, para y pregúntame. La fecha de cada uno, del nombre del fichero.
> - Antes de nada, comprueba los dos días con la línea de docs/runbooks/SESION-DE-PREGUNTAS.md («Antes», paso 1): 2026-10-23 y 2026-10-25. Las dos tienen que imprimir False; si alguna imprime True, para y avísame. La del 2026-10-25 se comprueba DESPUÉS de grabar (no la pasé antes): desviación del paso 1, declárala en el informe y en HOLDOUT-EXPOSICIONES.md.
> - Antes del registro (y por tanto antes del inventario), pregúntame en el terminal, para cada uno de los dos vídeos:
>   a) si el trader compartió su pantalla o su replay, si habló de operaciones concretas de septiembre, marzo, diciembre o de cualquier mes que no sea abril, julio del 1 al 17, agosto o enero, o si dio cifras de resultados, y en qué minuto aproximado. Esos tramos se declaran no citables y en HOLDOUT-EXPOSICIONES.md el mismo día, sin leerlos;
>   b) el orden real de las preguntas, en qué vídeo va cada una y cuáles no se hicieron;
>   c) si leí el minuto 1:44:49 de v10 con --crudo y qué oí («1 o 2» o «12»). Si lo leí, va a S-24 como dato de Aleks, sin cita de v10;
>   d) si tengo la hoja con mis notas. Si la tengo, la copio yo a corpus/Estrategia del trader/Sesiones/2026-10-23-sesion-05/ y entra en el inventario como material adicional (SESION-DE-PREGUNTAS.md, «Después», paso 2); no la lee nadie.
>
> LA HOJA QUE SE LLEVÓ
> 1. La hoja fue el PDF del consultor (Sesion-5-preguntas-trader.pdf), hecho desde docs/sesion-5/PREGUNTAS.md; no va al repo. Del PDF se quitaron las líneas «Para Aleks». Donde PREGUNTAS.md lleva un RECUADRO DE CORRECCIÓN del 2026-10-21, la hoja llevó el texto del recuadro (verifica que son S-7, S-12, S-13 y S-15; los otros dos recuadros de PREGUNTAS.md no cambian la hoja: el del 2026-10-22 de trabajo/hoja-sesion-05, sobre los códigos en el guion, y el del 2026-10-23 de trabajo/guardia-ci, sobre A.4):
>    - S-7: lo que da el recuadro (título «Los dos extremos de la caja: dónde pones el 0 y hasta dónde llevas el 1», lo que todavía no sabemos, el esquema, la pregunta, para precisar y la confirmación); «Lo que nos has dicho» se tomó del cuerpo, como dice el propio recuadro;
>    - S-12: lo que da el recuadro, en dos partes: primero de qué lado del nivel tomado va la caja (la contradicción entre RN-005/ev-v1-001306-f98e12e9 y ev-v9-004919-c6bfb3ee) y después A-50, con la forma neutra «una parte de tu lado y otra del otro»;
>    - S-13: solo la línea de «Para precisar» que da el recuadro («Si el 1 de la caja baja mucho…»);
>    - S-15: la hoja no cambia (el recuadro corrige un «Para Aleks»; el lado se pregunta en S-12).
> 2. Los códigos de voz son S-1 a S-25 de la sesión 5, «pregunta ese uno» … «fin de pregunta». No son los de la sesión 4. Cada filtrada se hace con el guion de main y --sesion 05 (una por vídeo), y el registro dice con qué hoja se agrupó. Si algún código del 21 al 25 salió como «veinte y N», el detector lo abre como S-20 (HOJA-SESION-05.md §1): revisa a mano el bloque de S-20 de cada vídeo y declara lo que encuentres.
> 3. Escribe docs/sesion-5/HOJA-USADA.md con la forma de docs/sesion-4/HOJA-USADA.md: tabla código → título usado → n.º en PREGUNTAS.md → ambigüedad o fuente (la de la cabecera de cada pregunta; si la cabecera no trae ambigüedad, la fuente que da su «Para Aleks») → vídeo (v15 o v16); el orden real (respuesta b); las preguntas que no se hicieron; los textos de los recuadros que sustituyeron al cuerpo; los esquemas inventados que se enseñaron; las tres peticiones de «Para cerrar» (diciembre, agosto, marzo); y que la sesión se partió en dos días. Sin ninguna cita del trader. Y en docs/sesion-5/PREGUNTAS.md, un recuadro que diga que la hoja usada está en HOJA-USADA.md.
>
> EL RECORRIDO (la skill ingerir-sesion, explícito; todo, para cada vídeo)
> - Registro: entradas de v15 y v16 en fuentes.yaml (su naturaleza describe el vídeo entero, también lo que enseñó el trader y no solo lo que enseñó Aleks); test_inventario ampliado a v15 y v16; uv run botsito corpus inventory y uv run botsito corpus check --hashes.
> - Test roto a propósito: con v15 y v16 ya en fuentes.yaml y ANTES de añadirlos a SESIONES_EN_CUARENTENA, ejecuta tests/unit/test_cuarentena.py y la prueba de tests/unit/test_guardia_claude.py que deriva la cuarentena de fuentes.yaml, y enseña que fallan; después añádelos y enseña que pasan. Las salidas, al informe.
> - Audio: con las formas EXACTAS de ffprobe y ffmpeg del paso 2 de la skill ingerir-sesion (silencedetect a -50 dB y 30 s; volumedetect; y la extracción del audio a un fichero .wav, .flac, .mp3 o .m4a FUERA del repo y fuera de cualquier carpeta que lo contenga: C:\Users\USER\Desktop\sesion-05-audio\sesion-05-v15.wav y C:\Users\USER\Desktop\sesion-05-audio\sesion-05-v16.wav). Los DOS NOMBRES tienen que ser distintos: el guion nombra la cruda, la filtrada y el registro por el nombre del audio y en su carpeta, y con la plantilla sesion-NN.wav de la skill el segundo vídeo pisaría todo lo del primero; antes de la segunda transcripción, comprueba que los ficheros de v15 siguen ahí. Si la guardia niega una de esas formas, PARADA: no se reescribe. Cada corte, a tramos_no_citables.yaml con motivo «SIN AUDIO», y la puerta de la skill (ningún segmento con t1 dentro del corte).
> - Transcripción (corpus transcribe y transcript check), una por vídeo, con mi «listo» antes de cada una; cuarentena con el guion de main (--audio <el audio de ese vídeo, FUERA del repo> --sesion 05 --video v15, y lo mismo con v16) y los bloques en cuarentena a tramos_no_citables.yaml, sin contenido, en un commit propio por vídeo.
> - Fotogramas: frames extract y frames check (0 huecos, 0 extra), de los dos.
> - Verificación final de la skill: git diff --name-status main...HEAD sobre knowledge/evidence, knowledge/corpus/transcripciones, knowledge/corpus/fotogramas y data/manifests, solo A.
>
> EXTRACCIÓN
> Informe en docs/validation/SESION-05-EXTRACCION.md, con el paso 6 de la skill y la forma de SESION-04-EXTRACCION.md, incluida su tabla final (Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta):
> - por cada código S-n: el vídeo y el tramo (mm:ss), el literal de la FILTRADA y si resuelve / resuelve en parte / no resuelve; si dio la regla general o solo un ejemplo, si dijo «creo» y si cubre compra y venta;
> - van primero las dos bloqueantes, S-3 (A-35) y S-4 (A-44), con lo que pide docs/runbooks/ACTIVAR-A35-A44.md para activarlas (si la respuesta no cae en ninguna lectura documentada, dilo: es su PARADA de §4, que decido yo); después S-5 (A-57, de la que depende ADR-0081) y S-6 (la «pregunta 3» de la que depende ADR-0083); después el resto en el orden de la hoja;
> - S-12 en dos filas: S-12a (el lado, RN-005) y S-12b (A-50);
> - S-1 y S-2: si la respuesta casa o choca con la regla del color activa (ADR-0080) y con la contradicción con la sesión 1 que lleva SESGO-H4-COLOR.md;
> - «Para cerrar», sin código de voz (en v16): localiza a mano qué dijo de diciembre (si lo grabó en vídeo con su voz, NA:I), de la exportación de agosto (NA:Q) y de la confirmación de marzo, que tiene que ser por escrito (REGISTRO-MARZO.md): solo lo que dijo, sin decidir nada.
> Evidencia con evidence new (o propose/accept), citas copiadas de la filtrada fuera de TODOS los tramos de tramos_no_citables.yaml (los bloques en cuarentena, los cortes «SIN AUDIO» y los tramos declarados por la respuesta a), con la puerta de la skill; después evidence contradictions y knowledge validate en verde.
> Cobertura de V (Next Action, NA:V): una tabla que diga, de cada cosa que V pedía a la sesión 5 (las «en parte» A-13, A-32, A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14, que es H; si el xlsx de julio es la exportación de v11 a v13; A-57; las preguntas de VISOR-CONSTRUCCION.md §3.2; la pregunta 3 de PUNTO-USADO.md), con qué código se preguntó y si quedó cubierta, en parte o no. Y qué pasa con H tras el dato de 1:44:49 (respuesta c).
> Al final del informe, la lista de ficheros nuevos de v15 y v16 fuera de git (vídeos, audios, transcripciones) que tengo que añadir a la copia de seguridad A.4.
> PROJECT_STATE está en 23.733 bytes: lo que añada esta rama, bajo 25.000; si no cabe, PARADA antes de recortar nada.
>
> CIERRE DE LA RAMA
> make check sellado; push a fix/sesion-05 (git push origin trabajo/sesion-05:refs/heads/fix/sesion-05; si el clasificador lo niega, me lo dices y lo lanzo yo con «!») y CI de Linux con solo el fallo esperado de state check; dame el número de run. Después el revisor, lanzado con el informe YA TERMINADO, y su informe pegado al final. Ningún registro de cierre en HISTORIA ni cambios de Next Action más allá de lo que haga abrir-rama: eso va con la orden de cierre.
>
> Rama lista para revisión, NO cerrada.

## Ampliación declarada del 2026-10-25: la confirmación escrita de marzo

Dada por Aleks (consultor) el 2026-10-25, después de los cuatro mensajes y de sus respuestas a las
preguntas a) a d) (que van en el informe, `docs/validation/SESION-05-EXTRACCION.md` §0). Copiada tal
cual, sin su primera línea («AÑADIDO AL ENCARGO (consultor, 2026-10-25): la confirmación escrita de
marzo. Cópialo al encargo como ampliación declarada, en su sección, con la fecha de hoy.»):

> QUÉ ES
> En «Para cerrar» de v16, Aleks le pidió al trader en voz lo que dice la hoja (docs/sesion-5/PREGUNTAS.md, «Para cerrar», marzo): que mande POR ESCRITO que el backtest de marzo es material que ya ha visto (docs/validation/REGISTRO-MARZO.md §2, paso 0; F09). El trader contestó por WhatsApp durante la llamada. Aleks guardó la captura en corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-25-1358.png.
>
> REGLAS
> - La sesión NO abre la captura (ADR-0038; la guardia no deja abrir imágenes de esa carpeta). El literal lo transcribió el consultor de la captura y queda con su hash para verificarlo, como las capturas del 2026-10-14 (fuentes.yaml, descripción de «Mensajes del trader»).
> - Ningún nombre ni número del trader entra al repositorio.
>
> LO QUE SE REGISTRA
> - Literal, transcrito por el consultor: «Confirmado backtest de marzo», mensaje del trader del 2026-10-25 a las 13:58 (hora de Lima). El mensaje siguiente de la captura (14:01) no se registra ni se interpreta.
> - Contexto: es la respuesta a la petición en voz de «Para cerrar» de v16. Localiza esa petición en la filtrada de v16 solo si cae FUERA de un bloque en cuarentena; como nombra marzo, lo normal es que la cuarentena por condición la bloquee. Si es así, no la leas: el contexto queda como declaración de Aleks («en la llamada le pedí que me lo confirmara por escrito y en ese momento me lo envió»).
> - Registro: amplía la descripción de «Mensajes del trader» en knowledge/corpus/fuentes.yaml con la forma de la entrada del 2026-10-14 (qué es, quién transcribió el literal, que la sesión no la abre, que no se interpreta el otro mensaje), y pasa corpus inventory y corpus check --hashes.
> - En SESION-05-EXTRACCION.md, en «Para cerrar»/marzo: el literal, la hora, el contexto y que la confirmación es escrita.
>
> LO QUE NO SE HACE EN ESTA RAMA
> - No se toca knowledge/corpus/vistos.yaml (marzo en vistos es otro paso de REGISTRO-MARZO §2/ENTRADA-MARZO) ni la hoja de ruta.
> - Para la orden de cierre, deja preparado en el informe: A.3 pasa a HECHA (fecha de la sesión 5: 2026-10-23 y 2026-10-25; confirmación escrita de marzo recibida el 2026-10-25), con el texto nuevo de su Estado, y la línea de la Next Action o heredado 2 que la pedía, con su texto nuevo. Lo que siga pendiente del paso 0 (marzo en vistos.yaml), lo dices.
> - Declara en HOLDOUT-EXPOSICIONES.md, con fecha de hoy, que el mensaje solo nombra el mes (ninguna fecha, ningún resultado) y que nadie de la sesión ha abierto la captura.

## Respuesta del consultor a la PARADA de v16 (2026-10-25)

Copiada tal cual. La PARADA y cómo se aplicó: `docs/validation/SESION-05-EXTRACCION.md` §2.7.

> Respuesta del consultor a la PARADA de v16 (2026-10-25). Cópiala al informe, en su sección.
>
> 1. SÍ, opción (a): v16 de 0:30:41 a 0:31:37 entra en tramos_no_citables.yaml como tramo de precaución (motivo: el trader enseña su replay de julio y dice hasta qué día llegó su backtest, un día del 18 en adelante). El número no se escribe en ningún sitio: ni en el informe, ni en HOLDOUT-EXPOSICIONES.md, ni en un commit, ni en el chat. La respuesta a S-25 (0:31:37 a 0:32:10) queda fuera del tramo y se puede citar.
> 2. HOLDOUT-EXPOSICIONES.md, con fecha de hoy: la sesión leyó, al leer la filtrada de v16, el día en que acaba el backtest de julio del trader (un día del 18 al 31), sin ninguna operación, resultado ni detalle de ese día; el número no se registra. Y por qué pasó: el detector de la sesión (detector_julio.py, en el scratchpad) era más estrecho que la regla del encargo (solo un número junto a «julio» o «día»).
> 3. Para el resto de la rama: antes de leer cualquier filtrada (o volver a leer una), se pasa primero el barrido ancho (barrido_18_31.py, con el número enmascarado), y solo después se lee. Si sale otra línea con un día de julio del 18 en adelante, PARADA como esta. Copia los dos scripts del scratchpad a docs/validation/anexos/SESION-05/ para que el revisor los vea.
> 4. El segundo hallazgo (la fecha numérica seguida de coma que la cuarentena no tapa, con la prueba sintética) va preparado en el informe como una línea de Technical Debt para la orden de cierre, del carril de guardias y de la cuarentena por condición. No se arregla en esta rama.
> 5. El dato de hasta dónde llega el backtest de julio NO se usa para U (julio del 20 al 31) ni para nada más. Cuando toque U, el consultor se lo pregunta a Aleks o al trader por su vía.
>
> Sigue con v16 (tramos, informe, commit) y con lo que quede, como dice el encargo.

## Respuesta del consultor a la PARADA del make check de la extracción (2026-10-25)

Copiada tal cual. La PARADA y cómo se aplicó: `docs/validation/SESION-05-EXTRACCION.md` §7.1.

> Respuesta del consultor a la PARADA del make check de la extracción (2026-10-25). Cópiala al informe, en su sección.
>
> 1. El id inexistente del §7: bien corregido. Declara en el informe cómo se cazó (los tres tests) y la lección: un id de evidencia se cita solo después de que su fichero esté escrito, nunca antes.
> 2. SÍ: test_la_sesion_4_deja_en_parte_lo_que_dice_su_tabla lee solo SESION-04-EXTRACCION.md (es una comprobación de que el lector lee algo de la sesión 4, como dice su docstring). Amplía el contrato a ese fichero de test en un commit propio que lo declare. El test de la regla (una «en parte» no puede estar RESUELTA) sigue leyendo TODAS las extracciones y no se toca. Enseña en el informe que sigue pasando y que se rompe a propósito.
> 3. SÍ, opción (a): levanto la prohibición del añadido de marzo SOLO para este cambio. Se añade ID:A-48 a las Refs de R4.1 en docs/plan/HOJA-DE-RUTA.md, y nada más de la hoja de ruta (A.3 sigue preparada para la orden de cierre, no se aplica aquí). Amplía el contrato a HOJA-DE-RUTA.md en el mismo commit propio, declarándolo. La fila de S-7 se queda como está («A-48, A-49», «en parte»): no se toca la extracción para que pase un test.
> 4. El hallazgo de agosto (32:56 toca el tramo en cuarentena que empieza en 0:32:58 y evidence new lo rechaza): correcto no citarlo. En «Para cerrar», di que lo de agosto queda sin cita por ese motivo y qué se entiende sin citar (si dice que la exportación está o no), para que yo lo decida en la activación.
>
> Después: make check sellado, commit, push a fix/sesion-05, CI con un gh run view suelto y el revisor, como dice el encargo.
