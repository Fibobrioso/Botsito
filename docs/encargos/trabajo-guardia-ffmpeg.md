# Encargo · trabajo/guardia-ffmpeg

Dado por Aleks (consultor) el 2026-10-22. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/guardia-ffmpeg (NA:K, la parte de ffprobe y ffmpeg; hoja de ruta G.1, carril de guardias y deuda), desde main en 8cfed04 (el commit de estado sobre el merge e044b15, que es al que apunta el tag stable/F37z-hoja-sesion-05). Antes, git fetch --prune; verifica con git las tres cosas y que no hay otra rama abierta, ni local ni en origin; si algo no cuadra, para y avísame. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con la fecha de hoy.
>
> POR QUÉ ESTA RAMA, Y POR QUÉ HOY
> Mañana, 2026-10-23, se graba la sesión 5, y su ingesta mide el audio del vídeo con ffmpeg (silencedetect y volumedetect, skill ingerir-sesion, paso 2) y saca el audio a un fichero FUERA del repo para transcribir_sesion.py --audio. Medido el 2026-10-22 por el auditor del consultor, llamando a decidir de la guardia de main con el texto de cada comando sobre vídeos inventados en una copia de main:
> - ffprobe sobre un vídeo, ffmpeg -i <vídeo> -af silencedetect=… -f null -, lo mismo con volumedetect, y la extracción del audio a un fichero dentro o fuera del repo: NIEGA, «no sabe con que se ejecuta» (regla del programa desconocido: _ejecucion_de_un_programa_desconocido trata como código cada argumento que es un fichero existente, troceando además cada argumento por = , ; y comillas);
> - ffmpeg o ffprobe sobre un vídeo de la carpeta de marzo: NIEGA, con el mensaje de motivo_fichero («ejecutar <ruta>. Regla: …»);
> - ffprobe sobre un vídeo que no existe: PASA.
> Tener ffprobe en SIN_LECTURA_DE_RUTAS no sirve: se consulta después del bloqueo. Sin esta rama, la ingesta para a mitad.
> Es la parte de ffprobe y ffmpeg de la K de la Next Action (ENTRADA-JULIO.md §0.d y §8), ampliada a volumedetect y a la extracción del audio, que es lo que pide la ingesta: ampliación declarada. Las otras dos partes de K (el falso positivo de exigir_sin_crudo y los tests de un clon de comparar-con-main) NO van aquí: siguen en K. G.1 no pasa a HECHA.
> PLAZO: lista para revisión hoy. Si mañana llega la grabación y no está cerrada, la ingesta espera.
>
> OBJETIVO
> Que la guardia deje exactamente cuatro formas de ffprobe y ffmpeg sobre un vídeo que no protege, y siga negando todo lo demás, con un test que rompa a propósito los dos sentidos.
>
> LA CONDICIÓN (decisión del consultor): una LISTA CERRADA de opciones, todo lo demás negado
> ffmpeg y ffprobe tienen cientos de opciones que escriben ficheros (-report, -vstats_file, -progress, -dump_attachment, -f tee), leen otros (amovie= o movie= en un filtro, -f concat, protocolos como concat: o subfile:, -/af, -filter_script) o vuelcan contenido (-show_data, -dump, -map a subtítulos). Por eso no se mira «la salida»: se permite solo lo que está en la lista, como hace ya la guardia con uv run.
> 1. Programa ffprobe. Opciones permitidas: -v, -loglevel, -hide_banner, -show_format, -show_streams, -show_entries, -of, -print_format, -select_streams, y un único fichero de entrada (posicional o con -i). Ninguna más.
> 2. Programa ffmpeg, medida de audio. Exactamente: opciones generales de la lista (-hide_banner, -nostdin, -nostats, -v, -loglevel, -y, -n), un -i, -vn, -sn, -dn, un -af cuyo valor es SOLO silencedetect=noise=<número>dB:d=<número> o SOLO volumedetect, y la salida -f null con «-» o el dispositivo nulo (NUL o /dev/null).
> 3. Programa ffmpeg, extracción de audio. Exactamente: las generales de la lista, un -i, -vn, -sn, -dn, opcionalmente -ac, -ar y -c:a o -acodec, y UNA salida que es un fichero con extensión .wav, .flac, .mp3 o .m4a FUERA de la raíz del repositorio (no reutilices EXTENSIONES_AUDIO de transcribir_sesion.py: lleva contenedores de vídeo). Sin -f, sin -map, sin -af, sin -filter_complex.
> 4. En las tres, cada fichero de entrada: ruta resoluble sin sustitución ni glob (un valor dinámico se niega), sin prefijo de protocolo (distinguiendo la letra de unidad de Windows), y que pase motivo_fichero: sobre los meses reservados, el material adicional, la carpeta de marzo o las imágenes sigue negado con su motivo.
> 5. El resto del análisis de la línea no cambia: tuberías, sustituciones, redirecciones de entrada, nombres de entorno (FFREPORT sigue negado). Una redirección de la salida estándar o de errores a un fichero DENTRO del repo se niega en estas formas.
> 6. La regla vive en su propia función y con su propia constante de regla, y entra en analizar_comando justo antes de la llamada a _ejecucion_de_un_programa_desconocido; así lo exige test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta. Declara en el informe que estas formas ya no pasan por exigir_ejecucion_verificable, y escríbelo en la cabecera de guardia.py como excepción a la familia 3. ffprobe sale de SIN_LECTURA_DE_RUTAS (cambio declarado). PowerShell queda fuera: allí no cambia nada.
> 7. «Fuera del repo» no protege el fichero de una lectura posterior: es aceptable porque es audio binario; dilo en el informe.
> Si al medir algo de esto no se puede comprobar con lo que la guardia ya sabe del comando, PARADA con tu propuesta.
>
> FASE 0 (corta, sin PARADA salvo sorpresa; entrega en el informe)
> - Reproduce la medida de arriba con el arnés de los tests (decidir con el texto del comando, sobre vídeos inventados en un repo de tmp_path; nunca ejecutando ffmpeg ni tocando el corpus). Si alguna decisión no es la de arriba, PARADA.
> - Los tests que tienen que seguir en verde: test_ejecucion_lo_que_no_esta_en_la_lista_es_una_ejecucion, test_ejecucion_lo_que_si_se_puede_decidir_pasa, test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta, test_el_ritual_y_los_runbooks_pasan y test_ninguna_denegacion_toca_el_ritual.
>
> FASE 1
> - La regla, como dice la condición.
> - Un test con una matriz de comandos y su decisión esperada: las cuatro formas permitidas, con rutas relativas y absolutas, y entre los negados, al menos: entrada protegida; dos -i; salida en el repo; salida a la salida estándar; -f distinto de null; -map; -filter_complex; -af con amovie= o con otro filtro; -report; -vstats_file; -progress; -dump_attachment; -f concat; una entrada con protocolo (concat:, subfile:, file:); ffprobe con -show_data, -o o -report; FFREPORT en el entorno; una redirección 2> dentro del repo; y ffmpeg dentro de una sustitución. Roto a propósito en los dos sentidos: sin la regla, las permitidas vuelven a negarse; con una opción de más en la lista (por ejemplo -map o -report), alguno de los negados pasa. Las salidas, al informe.
> - La misma matriz decidida con la guardia de main, cargada como hace test_la_guardia_frente_a_la_de_main_caso_a_caso pero en un test nuevo con decidir (el de caso a caso solo compara rutas): en el informe, la tabla de los casos que cambian de decisión, y ninguno fuera de las cuatro formas permitidas.
> - En la skill ingerir-sesion, paso 2, las formas exactas que deja la guardia (la medida de silencios y de volumen, y la extracción del audio fuera del repo), copiadas de la lista.
>
> REGLAS DE ESTA RAMA
> - Si la guardia o el clasificador niegan un comando: PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe (docs/runbooks/DECISIONES-DE-PROCESO.md, entrada del 2026-10-21). Durante la rama te vigila la guardia de main: no pruebes la regla nueva ejecutando ffmpeg.
> - La CI no se consulta con un guion ni con un bucle: un gh run view suelto cada vez.
> - Qué NO cambia: el motor, la spec, las ambigüedades, el feedback, los casos, el corpus, el Makefile y cualquier otra regla de la guardia salvo lo declarado.
>
> CIERRE DE LA RAMA
> Informe en docs/validation/GUARDIA-FFMPEG.md. make check sellado; push a fix/guardia-ffmpeg (git push origin trabajo/guardia-ffmpeg:refs/heads/fix/guardia-ffmpeg) y CI de Linux con solo el fallo esperado de state check (RITUAL.md: toda rama que toque .claude/hooks); dame los números de run. Después el revisor, lanzado con el informe YA TERMINADO, y su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
