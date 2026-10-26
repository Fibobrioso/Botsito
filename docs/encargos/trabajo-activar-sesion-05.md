# Encargo · trabajo/activar-sesion-05

Dado por Aleks (consultor) el 2026-10-25, en un solo mensaje. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Encargo del consultor (2026-10-25) · trabajo/activar-sesion-05 · tramo R4 (entrada R4.1 de la hoja de ruta; V de la Next Action)
>
> Rama nueva: trabajo/activar-sesion-05, desde main (b61c8f8, commit de estado sobre el merge baaf74b del tag stable/F38d-sesion-05; CI de main en verde, run 40266284524: compruébalo con un gh run view suelto, sin guion). Ábrela con la skill abrir-rama: base comprobada con git (su paso 1), contrato con tramo R4, riesgo alto (spec), artefacto docs/validation/ACTIVAR-SESION-05.md. El recorrido lo mandan las skills activar-sesion, fase-cero y entregar-rama. Si este encargo y ellas chocan, ganan ellas y lo dices.
>
> OBJETIVO
> Que lo que la sesión 5 cierra quede RESUELTO en la spec por su régimen; que A-35 y A-44 tengan valor en sus parámetros, aunque sigan ABIERTAS, para que el arnés corra sin ningún --diagnostico-*; y que lo que pide motor y lo que va a la sesión 6 quede escrito en el informe con mis decisiones, para la rama de motor y para la hoja de la sesión 6.
>
> QUÉ NO CAMBIA
> - Nada de src/botsito/engine ni src/botsito/domain: lo que pide código va a trabajo/activar-sesion-05-motor (su encargo lo escribo yo tras el cierre de esta). En tests/ solo entran los que cambian de sentido al fijar A-35 y A-44 (fase 0, b.5) y los que este encargo pide.
> - Nada fijado se pisa sin su régimen. Ninguna «en parte» de SESION-05-EXTRACCION.md §5 se cierra: A-35 y A-44 siguen ABIERTAS y bloqueantes.
> - Ningún registro de feedback sobre una ambigüedad «en parte»: lo que dejó claro va al informe y a la lista de la sesión 6, como en la sesión 4 (test_kit.py exige, por ejemplo, que no haya ninguno sobre A-49).
> - Ninguna cifra dentro de una forma ejecutable (ADR-0002).
> - Sin medidas agregadas: el arnés a secas se corre solo para comprobar que corre (código 0, sin etiqueta DIAGNOSTICO), su fichero va fuera del repo y no se resume, y el informe no da ninguna cifra de cobertura ni de operaciones. La corrida que cuenta va después de la rama de motor.
> - Material: ninguna filtrada se vuelve a leer. Las citas salen SOLO de los ítems de evidencia de SESION-05-EXTRACCION.md §8 y con el texto de cada ítem. Lo que la extracción cuenta fuera de un ítem se remite a su sección, sin citarlo. Si una cita necesaria no está en un ítem, PARADA. Nada de julio, diciembre, marzo, febrero ni de las crudas.
> - La Next Action y la hoja de ruta no se tocan en la rama: sus líneas se preparan en el informe para el commit del contrato. La tabla Known Ambiguities sí, porque test_project_state lo exige en el mismo commit que cierra cada una.
> - El Makefile, .claude/ y la guardia no se tocan.
>
> FECHAS DE LOS REGISTROS
> Id de sesión 2026-10-23-sesion-05. Un registro que cite v15: --fecha 2026-10-23 --recibido-el 2026-10-23. Uno que cite v16: --fecha 2026-10-23 --recibido-el 2026-10-25 (SESION-05-EXTRACCION.md §6 e; feedback/modelo.py:113).
>
> MIS DECISIONES (2026-10-25), sobre SESION-05-EXTRACCION.md §3, §4 y §5
> Las doy por adelantado para que la PARADA sea corta: la fase 0 las contrasta con lo medido y la PARADA dice cuáles cuadran y cuáles no.
>
> A. Lo que se activa en esta rama
> 1. A-35 (S-3). DESVIACIÓN DECLARADA de la regla «las en parte no fijan nada», con el precedente de A-43 en la sesión 4 (respuesta del consultor del 2026-10-11, punto 9; toma_antes_de_la_ventana fijado por feedback con A-43 ABIERTA):
>    - registro RESOLVE_UNKNOWN sobre el PARÁMETRO liquidez_m15_pivote_formado con --valor cierre_vela_contraria, citando ev-v15-000447-6699c708 (la respuesta, 04:47) y, en sus notas, ev-v15-000530-234d4a81 (la vela sin cuerpo no cuenta como vela de después). Es la opción (b) que el runbook ya tiene documentada, dicha como regla, sin «creo» y para compra y venta;
>    - NINGÚN registro sobre la ambigüedad: A-35 sigue ABIERTA y bloqueante por su segunda mitad («se actualiza el de la mecha», ev-v15-000553-9d95178a), que contradice lo que domain/pivotes_m15.py:24-26 deja hoy fijo y visible. Esa segunda mitad no abre una ambigüedad nueva porque ya es la pregunta de A-35; su mecanismo lo escribe la rama de motor con ADR y la sesión 6 la confirma; entonces se cierra A-35;
>    - la nota de A-35 en ambiguedades.yaml y RN-004 dicen todo esto, con la palabra «desviación». No contradice la sesión 4 (ev-v10-012456-9dc1d221): allí era cuándo queda TOMADO un alto, aquí qué alto se usa.
> 2. A-44 (S-4). La misma desviación declarada, con el mismo precedente:
>    - registros RESOLVE_UNKNOWN sobre los parámetros perdida_trader_alcance = dia y perdida_trader_unidad = porcentaje, citando ev-v15-000856-ee8f7ba3 («solo el del día y las 9 seguidas … la respuesta es la A») y ev-v15-000913-bdb12f92 («aquí hay un error, sería 9 pérdidas seguidas … a porcentajes, sería un 4,5»);
>    - perdida_trader_magnitud = saldo, por registro RESOLVE_UNKNOWN sobre el parámetro con la cita de ev-v15-000913-bdb12f92 y, en sus notas, el literal de RN-020 de la sesión 1 («De la cuenta basado en el saldo, y que sea en el saldo inicial del día», fb-2026-09-09-sesion-01-bff260ea). Es LECTURA DEL CONSULTOR y lo dice el registro: el trader traduce su tope a pérdidas cerradas (9 seguidas; el break even no cuenta, fb-2026-10-04-sesion-04-8e2d728a), y la única vez que habló de la base dijo «saldo». No es inocuo: RN-020 se evalúa en cada cierre de M1 con la peor equity del minuto (cableado.py, ADR-0053 §5), así que con equity una caída en abierto que se recupera pararía el día y con saldo no. Por eso la magnitud es la primera pregunta de la sesión 6, y el registro lo dice;
>    - perdida_trader_reinicio_huso se queda UNKNOWN («al día siguiente», sin reloj): el motor usa el corte del perfil y la traza lo marca SUPUESTO (tabla del runbook);
>    - perdida_maxima_semanal = 9 (CONFIRMED) no se borra ni cambia, porque ningún valor de su tipo significa «no hay»: con alcance = dia queda sin efecto. Es otra DESVIACIÓN DECLARADA, esta del runbook §1 (que pide un CORRECT para «un tope distinto de los de la sesión 1»): su descripcion y las notas de RN-020 dicen que el trader lo retiró, con la cita de ev-v15-000913-bdb12f92. Si la fase 0 ve una forma de CORRECT que lo deje sin efecto limpiamente, la propone en la PARADA;
>    - ningún registro sobre A-44: sigue ABIERTA y bloqueante;
>    - no hace falta ADR nuevo: esto lo escriben los registros, las notas y el informe. Si la fase 0 mide que alguno de estos registros no se puede escribir así (feedback apply, test_registro, el estado que queda), PARADA con la medida.
> 3. A-57 (S-5, que la extracción da como «resuelve»): RESUELTA. Registro RESOLVE_UNKNOWN sobre la ambigüedad con ev-v15-001758-c27d9c4c. lote_si_no_cabe es de categoría ejecucion: feedback apply no lo escribe, así que pasa a mano de DEFAULT_AMBIGUOUS a CONFIRMED con fuente decision ADR-0081 (verifica que test_provisional_cuelga_de_abierta y test_registro quedan en verde con eso). Las notas llevan las dos reservas («por ahora» y «creo», 17:58) y que contestó después de que Aleks planteara la disyuntiva, remitiendo a SESION-05-EXTRACCION.md §3.2 sin citarla. ADR-0081 deja de ser PROVISIONAL en D1: recuadro en el ADR y su fila del índice.
> 4. A-32 (S-18, la de v16): RESUELTA con ev-v16-000234-9a4fa375 y ev-v16-000603-6955d127: en M1 la mecha siempre vale, la única ruptura que pide cuerpo es la de la zona lineal de M15, y una línea que viene de M15 cuenta como de M15. Verifica que breaker_m1_criterio_ruptura = mecha y liquidez_m15_criterio_toma = cuerpo ya lo hacen y que ningún código descarta una entrada por una línea de M1 rota con mecha; si algo lo hace, PARADA.
> 5. Las que confirman lo que ya hace el bot, cada una con un registro CONFIRM (sin valor) y una línea en las notas de lo que confirma:
>    - S-1 (ev-v15-000049-3b294480, ev-v15-000138-ef123dfc): RN-003 / ADR-0080. Cierra la contradicción de ADR-0080 §9 con la sesión 1 a favor de la regla del color: recuadro en ADR-0080 §9 y lo mismo en las notas de RN-003. A-1 no se reabre.
>    - S-2 (ev-v15-000256-f3c52278): ADR-0080 §4 (D3) deja de ser decisión provisional del consultor: recuadro en §4, que dice que el caso bajista no lo dijo con sus palabras.
>    - S-9 (ev-v15-004448-aac87b77): A-24 / ADR-0045, la liquidez más reciente.
>    - S-11 (ev-v15-005839-f2e43c27): ADR-0066; A-46 no se reabre.
>    - S-12a (ev-v15-010104-23adba23): RN-005 sigue (en una compra la caja va por debajo del nivel tomado). CONFIRM sobre RN-005 y CORRECT sobre ev-v9-004919-c6bfb3ee con valor_resultante «por debajo del nivel tomado en una compra» (precedente de CORRECT sobre evidencia: fb-2026-09-09-sesion-01-2ba4c3e7).
>    - S-19 (ev-v16-000851-f5ae3b6f): ADR-0076 §4, pregunta 1. ANTES, mide con tests/unit/test_a21_series.py qué hace hoy el motor con una vela sin cuerpo en medio del retroceso (ADR-0076 §2 tiene una fila DISTINTO entre el motor y la lectura literal). Si el motor ya hace (b), CONFIRM; si no, va a la rama de motor y aquí no se registra nada.
>    - S-23 (ev-v16-002521-02c1be20, ev-v16-002641-e8e6eafc): ADR-0075; la reserva de fb-2026-10-04-sesion-04-ca0afae6 queda contestada.
> 6. ADR-0083 sigue PROVISIONAL: recuadro con lo que dijo en S-6 (ev-v15-002029-1ac081ae, ev-v15-002441-2e609b87, ev-v15-002729-30480ec5: cada reentrada es una decisión aparte, el punto tiene que volver a validarse rompiendo, en su ejemplo se actualiza el 0 y el 1 sigue, sin número de reentradas, y duda en voz de las de niveles iguales) y la pregunta que pasa a la sesión 6.
> 7. tests/unit/test_en_parte_no_se_cierra.py ya lee las dos extracciones por su glob; lo que falta es el test de control de la sesión 5 (hoy solo lo tiene la 4): que una «en parte» de la sesión 5 metida en RESUELTAS haga fallar.
>
> B. Lo que va a la rama de motor (en el informe, §«Para la rama de motor», cada una con su fuente y lo que hace hoy el código, fichero:línea; aquí no se toca código)
> 1. S-3, segunda mitad: la mecha de la vela contraria que pasa el extremo mueve el nivel a esa mecha (hoy pivotes_m15.py:24-26 dice lo contrario). ADR nuevo, A-35 sigue ABIERTA hasta la sesión 6.
> 2. S-8: las velas sin cuerpo dentro del tramo no cortan el punto de breaker; el máximo de la verde vale si el precio viene de un flujo bajista y luego cierra por debajo (VISOR-CONSTRUCCION.md §3.2, pregunta A).
> 3. S-24 y H: RN-007 con umbral cero. «Casi plana» pasa a «sin cuerpo» (cierre igual a la apertura), la definición que ya usan A-21 y pivotes_m15; sobre ella no se traza punto. La sesión 4 («1 o 2 puntos», ev-v10-014310-2296423b, en parte y con el ASR dudoso) la corrige S-24, explícita, con opciones y con confirmación: CORRECT sobre esa evidencia, en la rama de motor. Si mira o no las mechas de una vela sin cuerpo va a la sesión 6.
> 4. S-12b y A-50: parámetro nuevo (mi criterio: solo_el_0 / caja_entera) con caja_entera y A-50 ABIERTA: una caja se descarta por el lado de ruido solo si queda entera de ese lado. Hoy se_desarrolla_en_el_lado_de_ruido mira solo el 0 (zonas.py:522-538). La rama de motor mide si ese parámetro puede tener valor sin registro del trader (ADR-0004 y test_registro: es de estrategia) y, si no puede, PARADA allí.
> 5. S-15: entra en la zona más reciente que valide el punto, sin límite de zonas tras la toma; la orden se mueve de la primera a la segunda. RN-009 («solo 1 zona control, si hay 2 se descarta») no se borra: su literal es de la zona del retroceso, que es lo que mide «limpia» (ADR-0076); cambia el alcance del recuento, que pasa a ser el retroceso del punto vigente y no todo lo que hay desde la toma. ADR que lo diga. Si eso no se puede escribir sin contradecir el literal de RN-009, PARADA allí.
> 6. S-21: tras parar por 9 pérdidas, al día siguiente la racha empieza de cero. Opción nueva en racha_perdidas_reinicio (mi criterio: tras_la_detencion), CORRECT sobre el valor de la sesión 4 y recuadro en ADR-0077 §5. Mientras no se pare, la racha sigue de un día a otro (sesión 4).
> 7. S-22: la orden sin llenar se quita un minuto antes del final de la ventana, igual que la posición; en ese último minuto no se pone ninguna orden, y si una se llena ahí se cierra enseguida. Cierra el hueco que congela tests/unit/test_rn035_ventana_fin.py.
> 8. S-20, en parte: que la mecha de una vela de cualquier color rompe el punto. La rama de motor mira qué hace hoy el código y, si ya lo hace, solo lo apunta.
> 9. S-19, si la medida de A.5 dice que el motor no hace (b).
>
> C. La lista para la sesión 6 (en el informe; cada pregunta cerrada con opciones y «otra, ¿cuál?», en el lenguaje del trader, con esquemas de VELAS y el marco temporal escrito en el dibujo, que es lo que pidió en S-16 y S-17)
> - A-44: la magnitud, primero: «¿la pérdida del día la cuentas solo con las operaciones cerradas, o también con lo que vas perdiendo en la que tienes abierta?»; y el reloj del «día siguiente».
> - A-35: confirmar que, cuando la vela contraria pasa el alto con la mecha y cierra por debajo, el alto pasa a ser esa mecha (y lo mismo en el bajo).
> - A-13 (S-17): al toque o al cierre de M1, con velas dibujadas. Hasta entonces break_even_condicion = tocar (CONFIRMED) no se toca: su última frase y su confirmación son «apenas toque».
> - A-53 (S-13): la subpregunta del recuadro («si el 1 de la caja baja mucho») y si la orden que se llena antes del punto nuevo vale.
> - A-43 (S-10): si la MISMA liquidez, tomada antes de las 7 y otra vez después, vale la segunda vez.
> - A-49 y A-48 (S-7): con un esquema que no lleve el 0 en el último alto de M1, que es lo que no entendió.
> - A-50 (S-12b): confirmar «la caja entera» con dos dibujos.
> - ADR-0083 (S-6): cuántas veces reentra en el mismo punto, si la caja es nueva y qué pasa tras un break even.
> - S-16: el precio ya pasado del 0 al formarse la caja, con el esquema rehecho en M1 y con velas.
> - S-19 frente a S-24: en el retroceso, ¿una vela de 1 o 2 puntos cuenta como cambio de color?; y si una vela sin cuerpo con mechas largas cuenta como si no existiera.
> - S-20: qué pesa más, la mecha que rompe o la alternancia de antes.
> - S-14: los días de construcción en que el bot opera y él no (lo pidió él), cuando la re-corrida tras la rama de motor los dé.
> Nada de esto se pregunta con días reales ni con fechas.
>
> D. Lo que no es de spec y va a las líneas del cierre
> - S-14 y el final de v16: en sus backtests anteriores se saltaba sesiones que iban a acabar en break even, y en los grabados en vídeo no. Una línea en G (PREREGISTRO) y en R5.1 (F26 lo tiene en cuenta al elegir los libros que miden), y otra en la deuda de Technical Debt «el no_trade por ausencia no está decidido». Mide en la fase 0, por libros.yaml y sin abrir filas, qué libros de construcción vienen de un backtest grabado en vídeo y cuáles no.
> - S-25: lo mide T (R2.4); sin cambio.
> - Diciembre (NA:I): el diálogo no aclara si falta el envío o el vídeo; Aleks se lo pregunta al trader. NA:I no cambia.
> - Agosto (NA:Q): el trader cree que la exportación existe; Aleks se la vuelve a pedir. NA:Q no cambia.
> - La medida de la hora del mensaje de marzo (§3.5) se queda como está.
>
> FASE 0 (skill fase-cero; termina en PARADA, como manda activar-sesion en su paso 2)
> a. Tabla de activación (activar-sesion, paso 1): una fila por código de SESION-05-EXTRACCION.md §5 (S-1 a S-25, con S-12a y S-12b, y «Para cerrar»), con mi destino (A, B, C o D), los ítems que la citan, qué hace hoy el código (fichero:línea), el test que lo prueba y si cuadra con mi decisión.
> b. Mide, sin escribir nada:
>    1. que cada registro de A.1, A.2 y A.3 se puede escribir y aplicar así: feedback apply --check (en un clon desechable si hace falta escribir para verlo, skill comparar-con-main), test_registro (fuente feedback para un parámetro de estrategia; decision para uno de ejecucion), test_provisional_cuelga_de_abierta y el estado que queda en cada parámetro;
>    2. que, con esos valores, uv run botsito motor arnes --salida <fichero fuera del repo> corre a secas (código 0, sin DIAGNOSTICO-A35 ni DIAGNOSTICO-A44), y también con --simular; mídelo en el clon desechable;
>    3. que tope_del_registro con alcance dia y magnitud saldo no lanza, y qué lee de perdida_maxima_semanal con alcance dia;
>    4. la medida de S-19 (A.5) con test_a21_series.py;
>    5. todos los tests que cambian al fijar A-35 y A-44, no solo los del runbook (§2 y §3): busca además los que llaman al arnés o al visor con --diagnostico-a35, --diagnostico-a44 o Diagnostico(a44=…) contra el registro real, y los que esperan otra compuerta que hoy va detrás (el auditor del consultor señala test_sesiones_independientes.py:104-109, test_selector_orden_stop.py:141-146 y :180-185, test_renovar_cierres.py:185-190, test_rutas_windows.py:74-86, test_preparar_a35.py:419, test_kit.py:360 y :439-449, test_provisional_cuelga_de_abierta.py y test_registro.py:156: verifícalos uno a uno y di qué cambia en cada uno);
>    6. quién espera cada ambigüedad que se cierra (A-32, A-57) y cada parámetro que se fija: grep -rn en CLAUDE.md, docs/runbooks, PROJECT_STATE.md y docs/plan/HOJA-DE-RUTA.md;
>    7. el recuento de S-14 de D, por libros.yaml.
> c. PROJECT_STATE.md está en 24.412 bytes. Con las líneas del cierre ya contadas (salen las filas de A-32 y A-57, H y la V larga; entran una V corta, la línea de S-14 en G y la de Technical Debt), tiene que quedar en 23.000 o menos. Si no llega, propón qué se mueve por su régimen (docs/state/README.md), sin quitar nada vivo; si no cabe así, dilo en la PARADA.
> d. El plan de commits: uno por respuesta activada (A-35; A-44; A-57 con el recuadro de ADR-0081; A-32; uno con los CONFIRM y el CORRECT de A.5; uno con el recuadro de ADR-0083; uno con el test de control de A.7), y el informe.
>
> La PARADA trae, como mínimo: la tabla de a; lo medido en b, punto por punto; mis decisiones que no cuadran con lo medido, con la alternativa; y cada respuesta con «creo» o con un ejemplo sin regla general que yo esté activando.
>
> DESPUÉS DE MI RESPUESTA
> Cópiala tal cual al final del encargo y del informe y aplícala punto por punto (fase-cero). Cada respuesta activada sigue entero el paso 3 de activar-sesion, en su propio commit: los registros, feedback apply --check que propone solo los de esa respuesta, los cinco sitios de AMBIGUEDADES.md para lo que se cierra, tests/unit/test_kit.py, spec_version subida (hoy 18.1.3 en spec_manifest.yaml) con uv run botsito spec manifest --escribir y uv run botsito spec docs --escribir, uv run botsito knowledge validate antes de make check, y el trailer Fuente: en el cuerpo con ids fb-* que existen. Cada ADR enmendado o que deja de ser provisional, con su recuadro y su fila del índice. Los tests que congelaban «sin fijar» cambian de sentido a propósito, y el commit y el informe lo dicen.
>
> TESTS QUE ROMPEN A PROPÓSITO
> - Los que cambian de sentido al fijar A-35 y A-44, con la salida de main y la de la rama en el informe (skill comparar-con-main).
> - El test de control de A.7.
> - Uno, sobre un registro sintético, que falle si perdida_trader_magnitud se lee como equity con alcance dia y pase con saldo, para que una caída en abierto que se recupera no pare el día.
> - Todo test que necesite data/ se salta en la CI de Linux, como los demás.
>
> HOLDOUT
> - Nunca listes knowledge/cases ni ninguna carpeta madre de meses reservados con un filtro detrás: rutas literales en el propio comando. Dale esta regla también al revisor.
> - El fichero del arnés a secas no se commitea ni se resume.
> - Toda exposición, aunque sea dudosa, el mismo día en docs/validation/HOLDOUT-EXPOSICIONES.md y en el informe.
> - Ninguna fecha de día reservado ni ningún resultado de operación en nada de lo que escribas.
>
> ENTREGA (skill entregar-rama)
> - CI de Linux con git push origin trabajo/activar-sesion-05:refs/heads/fix/activar-sesion-05, y el número de run; solo se acepta el fallo de state check. La CI se consulta con un gh run view suelto, nunca con un guion ni en bucle.
> - Si el clasificador niega un push o la guardia un make, no lo rodees: dame el comando exacto y lo lanzo yo con «!».
> - Revisor (opus) con el informe terminado y cuatro alcances: (1) cada ambigüedad cerrada tiene sus cinco sitios, su test y su Fuente:, ninguna «en parte» se cerró, las dos desviaciones (A-35 y A-44) están declaradas con esa palabra en el registro, las notas y el informe, y nada contradice un ADR sin recuadro; (2) ninguna cita sale de fuera de los ítems de evidencia de SESION-05-EXTRACCION.md §8; (3) cada ADR enmendado o que deja de ser provisional tiene su recuadro y su fila del índice; (4) fecha y recibido_el de cada registro según el vídeo que cita. Su informe, pegado al final.
> - Al final del informe, las líneas preparadas para el commit del contrato:
>   - Next Action: V corta (sesión 5 activada en spec, con A-35 y A-44 operables y ABIERTAS; falta trabajo/activar-sesion-05-motor, con la lista de §«Para la rama de motor»); H sale (RN-007 con umbral cero, a la rama de motor); F = «la rama de motor de V; después la re-corrida del arnés y la sesión 6; R6a en los huecos»; la línea de S-14 en G.
>   - Hoja de ruta: R4.1 con Estado «spec HECHA (este tag); motor pendiente» y sus Refs sin NA:H (test_hoja_de_ruta) y sin A-32 ni A-57 si el test lo pide; R4.2 nueva, «Preparar y celebrar la sesión 6», con la lista de C, que depende de la rama de motor y de la re-corrida; la línea de S-14 en R5.1.
>   - La línea de S-14 en la deuda del no_trade por ausencia.
>   - El tamaño final de PROJECT_STATE con todo eso.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA (2026-10-26)

> Respuesta del consultor a la PARADA de trabajo/activar-sesion-05 (2026-10-26). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo medido lo contradice, PARADA 2.
>
> 0. (a). La desviación declarada de A.1 y A.2 manda sobre activar-sesion, con la palabra «desviación» en los registros, las notas y el informe. Motivo: sin ella el arnés no corre a secas hasta la sesión 6, y lo que se fija está dicho por el trader (A-35) o es un valor provisional a la vista (A-44, punto 1).
> 1. (b). perdida_trader_magnitud a DEFAULT_AMBIGUOUS, valor saldo, ambiguedad_id A-44, fuente fb-2026-09-09-sesion-01-bff260ea, a mano y sin registro de feedback; la lectura del consultor va en su descripción y en las notas de RN-020, y la magnitud es la primera pregunta de la sesión 6. Motivo: es un default nuestro bajo una ambigüedad ABIERTA (precedente orden_stop_punto), y un CONFIRMED pondría en boca del trader lo que no dijo. Corrige mi error: el encargo decía «registro RESOLVE_UNKNOWN sobre el parámetro» y eso contradecía ERRORES-RECURRENTES.md:84 y mi propia decisión del 2026-10-19 sobre b10. El test sintético saldo/equity se queda.
> 2. (b). La unidad lleva además ev-v10-010913-c4949417 en las notas, con la reserva del «creo» de ev-v15-000913-bdb12f92.
> 3. (a). S-1, S-2 y S-23, CONFIRM sobre RN-003; S-9 y S-11, sobre RN-004; S-12a, sobre RN-005, más el CORRECT sobre ev-v9-004919-c6bfb3ee. A-24 sigue DECIDIDA. Los recuadros de ADR-0080 §4 y §9, ADR-0066 y ADR-0075 citan esos registros. Corrige mi error: los objetivos del encargo (ADR y ambigüedades) no los admite CONFIRM (modelo.py:66).
> 4. (a). Arnés a secas y con --simular solo con --meses 2026-04, fichero fuera del repo y sin resumir, con la lectura del M1 de marzo declarada antes de correr (ya está). Corrige mi error: por ADR-0070 §3 la corrida sobre toda la construcción con --simular cuenta, y esa es la re-corrida que va después de la rama de motor.
> 5. (a). Una NOTA fechada en ADR-0053 §3.3 y §9, ADR-0054 §1 e Impacto y ADR-0070 §3, en los commits de A-35 y A-44, con sus filas del índice. Lo que añadí de más en el encargo, el recuadro de ADR-0066 y ADR-0075 por S-11 y S-23, va también como NOTA de una línea en el commit de las confirmaciones.
> 6. (a). Amplía el contrato a docs/runbooks/ACTIVAR-A35-A44.md, en un commit propio, con una NOTA al principio: activado el 2026-10-26, lo que se fijó y las tres desviaciones (la segunda mitad de A-35 no abre ambigüedad nueva; perdida_maxima_semanal sin CORRECT; la magnitud como DEFAULT_AMBIGUOUS). El cuerpo no se toca.
> 7. (a). Acortar la introducción de Technical Debt y dejar de la deuda de Oanda solo la parte viva de la serie, en el commit del contrato. Las candidatas sin abrir se quedan.
> 8. (a). Dos commits, con los cinco tests de CLI tocados dos veces, y cada commit en verde.
> 9. (a). Todas se activan, con su reserva escrita en las notas del registro.
>
> Además, lo que sale de §0.e:
> 10. B.1 (la segunda mitad de A-35): la rama de motor escribe lo que sostiene ev-v15-000553-9d95178a («se actualiza el de la mecha») y remite a SESION-05-EXTRACCION.md §3.1 para el ejemplo del replay, sin citarlo. Que sea la mecha de la vela contraria es lo que se pregunta en la sesión 6 para confirmarlo. Corrige mi error: el encargo restringía a la vela contraria con un tramo que no está en ningún ítem.
> 11. Lista de la sesión 6, S-14 (§0.e.13): los días en que el bot opera y él no se enseñan como permite la regla 2 de SESION-DE-PREGUNTAS.md (solo días de construcción, cortados antes de la orden y sin fecha), y la elección de los días la hago yo al preparar la hoja. Corrige la frase «nada de esto se pregunta con días reales», que era demasiado ancha: quédala como «ningún día reservado ni ninguna fecha».
> 12. §0.e.17 (RN-020 no retira la orden pendiente al llegar al tope): de acuerdo, entra en «Para la rama de motor» como punto 10, con RN-036 de modelo.
> 13. §0.e.18 (la medida de R4.1 con su diff): va en las líneas del cierre como la re-corrida que sigue a la rama de motor, no en esta rama.
> 14. §0.f (la guardia niega los tests de un clon en C:/cm/): hallazgo importa, de acuerdo. Ponlo en las líneas del cierre como ampliación de K, con los tres ficheros nuevos.
>
> Sigue lo que manda el encargo: un commit por respuesta, knowledge validate antes de make check, Fuente: en el cuerpo con ids que existen, CI de Linux por fix/activar-sesion-05 con su número de run (gh run view suelto), revisor (opus) con los cuatro alcances del encargo más un quinto (cada DEFAULT_AMBIGUOUS nuevo dice en su descripción que es lectura del consultor y bajo qué ambigüedad) y su informe pegado al final. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA 2 (2026-10-26)

Copiada tal cual.

> Respuesta del consultor a la PARADA 2 de trabajo/activar-sesion-05 (2026-10-26). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», y aplícala.
>
> 0. (b). S-11 sin registro: pasa a «en parte» en la lista de la sesión 6 (§3) con la pregunta «Una toma de la mañana, y en la tarde el MISMO sesgo: ¿esa toma vale para operar en la tarde? (a) sí, si el sesgo sigue igual; (b) no, cada sesión espera su propia toma; (c) otra, ¿cuál?», y sin NOTA en ADR-0066. A-46 sigue RESUELTA y el motor no cambia. El recuadro en la tabla final de SESION-05-EXTRACCION.md va en el commit del contrato del cierre. Corrige mi error: decidí el CONFIRM de S-11 copiando «A-46 no se reabre» de la extracción sin cruzar la cita con A-46.
> 1. (a). Los cinco registros se quedan como están, declarados en el informe (§6, fila 11); la lección va a ERRORES-RECURRENTES en el cierre.
> 2. (a). La V remite a §2 sin la lista y la línea de G va a su mitad, en el commit del contrato del cierre.
>
> Lo que toca en la rama: la lista de §3 con S-11, §5 con la V y la G recortadas y la mención a S-11 resuelta, y el Estado del informe. Un commit sellado, push a fix/activar-sesion-05 y su run con gh run view suelto. Sin revisor nuevo: son cambios de documentación que salen de esta respuesta.
>
> Rama lista para revisión, NO cerrada.
