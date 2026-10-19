# Encargo · trabajo/punto-usado

Dado por Aleks (consultor) el 2026-10-18. Copiado tal cual (hasta que existió, el ADR que el
encargo manda escribir iba declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; salió del bloque en el commit que lo creó):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: trabajo/punto-usado (NA:Y, hoja de ruta R3.4). Encargo del consultor, 2026-10-18.
>
> 0. Apertura
> - Base: main f96b581, el commit de estado sobre el merge 3ae2933 (stable/F37u-plataforma-adelantada). Verifica con git main, origin/main y el tag, y que no hay otra rama de trabajo abierta. La CI de main de f96b581 la dio verde el cierre (run 39186492700, que no está escrito en el repo): compruébala con gh; si el clasificador niega gh, PARADA y la consulto yo con «!». Nunca con curl ni con un guion.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. Tramo R3.
> - Informe: docs/validation/PUNTO-USADO.md. Anexos: docs/validation/anexos/PUNTO-USADO/.
> - Skills: fase-cero (con el agente auditor-encargo) para la fase 0; comparar-con-main para probar los tests nuevos con el código de main; entregar-rama al final.
> - Revisa /model antes de empezar: Fable 5.1 en esfuerzo alto.
>
> 1. Por qué cambia Y, y el objetivo
> Y nació de la E de VISOR-CONSTRUCCION.md §2.d.4: tras llenarse la orden de un punto, el bot vuelve a colocar ese punto con otra caja, contra la decisión 1 de ADR-0064 («un punto ya usado no se vuelve a colocar. Usado es con la orden enviada, aceptada o rechazada»). Al preparar este encargo, el auditor del consultor encontró que el material del trader va en sentido contrario, y yo di por buena esa E sin buscarlo:
> - LA-CAJA-DEL-29-DE-ABRIL.md:236-243 (abril es construcción): dos ventas del xlsx con la misma entrada y el mismo stop; la primera pierde en el stop y la segunda va después, y el trader lo narra: «sería cuestión de poner otra reentrada aquí».
> - ADR-0066:51: tras una pérdida, un break even o un equal, el escenario sigue con los intentos que le queden. RN-018 lo apoya en su literal («para que tú puedas entrar nuevamente o bien te ha tocado stop loss»).
> - CORRIDA-CONSTRUCCION.md §4.5: P7 son «entradas repetidas del trader en el mismo nivel que el bot toma una vez», con destino V, pregunta 3.
> La decisión 1 de ADR-0064 (2026-09-30) se escribió como «la lectura más conservadora», antes de ADR-0066 (2026-10-01), y su única razón es el rechazo: no reintentarlo en cada M1 y no llenar el contador de R13 (ADR-0064:79-81).
>
> Y hoy el código hace las dos cosas mal (verifícalo en la fase 0):
> - usadas se apunta por ZONA (zonas.py:418-420), y con caja_se_fija = en_cada_cierre_m1 la zona es nivel@inicio#extremo (zonas.py:383-387). Tras un llenado y un stop, el punto solo vuelve a colocarse si el 1 cambió. Con la MISMA caja, que es el caso del 29 de abril, la zona sigue en usadas y toca_colocar_orden_limite niega: el bot no repite la reentrada del trader.
> - El rechazo por margen AL LLENAR (broker.py:813-832, ADR-0081 §4) no gasta el punto: marcar_rechazada solo se llama en el no envío (primitivas_broker.py:636) y en el rechazo al colocar (:653).
>
> Objetivo: fijar por ADR qué gasta un punto, que el código lo cumpla, con tests que rompen en main, y repetir la corrida de R3.1 con sus tres comandos.
>
> 2. Decisiones del consultor (2026-10-18; las tomo ANTES de ver las medidas, y las medidas no las cambian. Si la fase 0 encuentra un hecho que las contradiga —un ADR, una regla de la spec o algo que el trader ya dijera—, PARADA)
> D1. Gasta un punto, en su sesión, la orden que el bróker RECHAZA (al colocar o al llenar) o que el bot no envía (ADR-0081 §3). No lo gastan la reubicación (RN-006, con un 1 nuevo del mismo punto, ADR-0074, o con un punto nuevo, ADR-0064 §4) ni el llenado: cerrada la operación con una pérdida, un break even o un equal, el punto se puede volver a colocar, con la misma caja o con otra, con los cartuchos de siempre delante (RN-016). Tras una ganadora, RN-034 termina el escenario y no se vuelve a colocar nada (toca_colocar_orden_limite ya lo niega con escenario_terminado, zonas.py:466-467); esto no cambia. Por qué: el material del punto 1, y que la razón de la decisión 1 (no reintentar un rechazo) no alcanza a un llenado. Es PROVISIONAL hasta la pregunta 3 de V: cuántas veces reentra el trader en el mismo punto tras un stop, y con qué caja.
> D2. ADR nuevo, 0083 (lo verifico libre: el último es 0082 y nadie cita 0083), que enmienda la decisión 1 de ADR-0064 con D1, con su recuadro en ADR-0064 y una nota en ADR-0074 §4 («la decisión 1 de ADR-0064 no cambia») que remita al nuevo. Cita el 29 de abril, ADR-0066, RN-018, ADR-0081 §4 y CORRIDA-CONSTRUCCION §4.5 (P5 y P7). En el mismo trabajo se corrigen los docstrings (src/botsito/engine/zonas.py:41-45 y marcar_usada, :418-420) y la descripción de toca_colocar_orden_limite en knowledge/spec/strategy_spec.yaml:269-276 («que la sesion no haya usado»), que pasa a decir qué gasta un punto. Como toca la spec: spec_version subida, spec manifest --escribir y spec docs --escribir en el mismo commit, y trailer Fuente: ADR-0083.
> D3. Dos E, cada una con su test que rompe en main: (a) tras cerrarse con pérdida la operación de un punto, la orden de ese punto con la MISMA caja se vuelve a colocar; (b) el rechazo al llenar gasta el punto. La vía la propone la fase 0 (4.b).
> D4. Con la posición de un punto abierta no se coloca otra orden. Lo impide ya RN-011 (strategy_spec.yaml:1490-1495, ninguno_de orden_limite_pendiente y operacion_abierta), con RN-018 y operaciones_simultaneas_max = 1 (parametros.yaml:944-953). No cambia; un test lo fija por el cableado.
> D5. La reentrada sale por la vía normal de colocación (RN-011 y RN-015), con los gates delante, y la caja se calcula como siempre (caja_bloque, caja_se_fija). Esta rama no decide si la caja de la reentrada es la del primer intento: eso es la pregunta 3 de V.
>
> 3. Lo que NO cambia
> - Fuera de D1 a D3: la reubicación de ADR-0074 con la orden sin llenar, la geometría, el sesgo, la ventana, el lote y el límite de ADR-0081, RN-034, los cartuchos, y ninguna otra regla ni cifra.
> - Los informes y anexos cerrados no se editan. VISOR-CONSTRUCCION.md lleva recuadros de corrección, con fecha y rama, junto a todo lo que da la E por buena: §2.d.4, el párrafo de §2.h (:887), las dos filas de la tabla de §3.1 (la de P2, hacia :898, y la de los cartuchos agotados, hacia :906), §3.3 y la línea Y de §4.1 (hacia :1006). Dicen que la E se rehace en ADR-0083: volver al punto tras un stop no es el error; el error es no volver con la misma caja y no gastar el punto con el rechazo al llenar; y que lo aceptó el consultor sin buscar en el material del trader. El cuerpo queda intacto.
> - knowledge/cases y el holdout: la rama no los toca.
> - Las guardias, .claude/ y el Makefile. Si algo obliga a tocar el Makefile, PARADA: con el Makefile cambiado la guardia niega todo make a la sesión, y esos make check los lanzo yo con «!».
> - PROJECT_STATE, salvo lo que haga el ritual (21.911 bytes; verifícalo).
> - Si el clasificador niega un comando, no cambies de vía ni reescribas el comando: PARADA, y lo lanzo yo con «!».
>
> 4. Fase 0 (inventario sin tocar nada)
> a. Con fichero:línea, todos los caminos por los que termina una orden, y si gasta su punto hoy y con D1: llenada (y su operación cerrada por stop, break even, equal u objetivo); rechazada al colocar y al llenar; no enviada; cada ctx.broker.cancelar de primitivas_broker.py (verifico :681 RN-035, :694 RN-036, :714 escenario nuevo con se_retira, :753 reubicación); la cancelación de fin de día de cableado.py (hacia :303-309); _cancelar_por_cierre de broker.py (hacia :849-861, ventana prohibida, ADR-0068); y EXPIRADA (hacia :801-803). Si D1 cambia algún camino más que los dos de D3, PARADA.
> b. La vía. El llenado y el cierre llegan a _a_la_cuenta (cableado.py:349, el bloque LLENADA en :366-375), que no recibe el EstadoDia ni la sesión, y punto_de_zona vive en la memoria de la sesión. Propón cómo se libera una zona usada al cerrarse su operación sin ganar y cómo se gasta el punto con el rechazo al llenar (cambiar firmas, o hacerlo en las primitivas a partir de ctx.eventos), y por qué. _punto_nuevo (primitivas_broker.py:235-253) usa usadas en :241-243 para saber si la orden es de la sesión: si la vía cambia el sentido de usadas, di cómo queda _punto_nuevo, con su test.
> c. D4: la traza de 2026-07-13 11-15 (VISOR-CONSTRUCCION.md §2.d.4), donde o11, o12 y o13 se llenan en el mismo punto: ¿cada una se coloca después de cerrarse la anterior, y con qué caja?
> d. Los tests que dependen de marcar_usada, usadas y rechazados (al menos tests/unit/test_orden_stop_pivote.py :178-197, :210-237 y :312; tests/unit/test_escenarios_por_sesion.py:506; tests/unit/test_margen_lote.py :185 y :333; y test_cableado.py), cuáles cambian de resultado con D1 y cómo se rehacen sin rebajar lo que comprobaban.
> e. Lectura de material de las corridas: como declararon R3.1 y MARGEN-LOTE (HOLDOUT-EXPOSICIONES.md, filas del 2026-10-14 y del 2026-10-17), el calentamiento lee el M1 entero de marzo y de junio; se declara con su fila el mismo día de cada corrida y ANTES de correrla. La traza de 4.c es de un día dev: su lectura va en la fila de la fase 0. Ninguna salida ni el informe imprime fechas fuera de los días dev de construcción, salvo la línea de cobertura del calendario de cierres, como en R3.1.
> PARADA solo si a-e contradicen algo de este encargo o se da la PARADA de 4.a. Si no, entrega la fase 0 en el informe y sigue sin parar.
>
> 5. Fases
> Fase 1 · El campo y la medida antes del cambio. Añade AL FINAL de cada línea de «### Ordenes» el punto de la orden (la clave nivel@inicio de la vela contraria), para no desplazar las columnas que leen los guiones cerrados, con el régimen del campo bloqueadas de R3.1 (CORRIDA-CONSTRUCCION.md:1054): solo salida, ninguna decisión cambia, test sintético en los dos sentidos. make check sellado. Después, con su fila de exposiciones antes:
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/antes-diaria.txt
>    (el arnés añade al nombre el sufijo DIAGNOSTICO…), y su repetición fuera del repo para el diff de determinismo, como R3.1. Quitando el campo nuevo, tiene que salir igual que anexos/MARGEN-LOTE/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt (verifico su sha256 en e584077bf767818b97b3e7878024925bcbf017269e3112ab0d00aba89cef55e3); si no, PARADA. Con ella, un guion en los anexos, que reciba por argumento lo que lee, cuente por punto exacto y por sesión: las órdenes colocadas en el punto de una orden ya llenada de su sesión, separando las de la misma caja y las de otra, y las colocadas tras un rechazo del mismo punto.
> Fase 2 · Tests primero, en rojo sobre el código de main (con comparar-con-main), con el recuento de FAILED en el informe, por el cableado real (el camino que usa el arnés), no llamando solo a las funciones de zonas.py. Cada test dice qué caja construye a propósito:
> - tras cerrarse con pérdida la operación de un punto, y sin 1 nuevo, el mismo punto se vuelve a colocar con la misma caja (D3a; en main falla);
> - lo mismo con un 1 nuevo (pasa en los dos);
> - tras un break even, igual que tras la pérdida;
> - tras una ganadora, nada se vuelve a colocar (RN-034; pasa en los dos);
> - los cartuchos cortan la reentrada al agotarse (pasa en los dos);
> - tras un rechazo al llenar, el punto no se vuelve a colocar con ninguna caja (D3b; en main falla);
> - el rechazo al colocar y el no envío siguen gastando el punto;
> - con la posición abierta no se coloca otra orden (D4);
> - con la orden sin llenar, el 1 nuevo la reubica como hoy;
> - y los tests de 4.d, rehechos.
> Fase 3 · Código (D3), ADR-0083 y sus recuadros (D2), docstrings, spec y los recuadros de VISOR-CONSTRUCCION. Tests en verde y make check sellado.
> Fase 4 · Re-corrida con su fila de exposiciones antes. Los tres comandos de R3.1 tal cual, salvo la carpeta de --salida:
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/PUNTO-USADO/arrastrada.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/diaria.txt
>    uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/PUNTO-USADO/a35-inicio.txt
>    y la repetición de la 2 fuera del repo para el diff. Es una corrida con --diagnostico-*: no cuenta ni habilita mayo (ADR-0070 §3), no decide ningún parámetro y no se mide cobertura contra ningún umbral. En el informe van:
> - el recuento de la fase 1, antes y después;
> - las órdenes, las peticiones por día y los rechazos por motivo, antes y después;
> - las sesiones con detenido_por_cartuchos, antes y después, en particular las cuatro de VISOR-CONSTRUCCION.md §2.h;
> - la tabla T0 y P1-P7 con patrones.py de R3.1 (anexos/CORRIDA-CONSTRUCCION/) sobre la corrida 2, frente a MARGEN-LOTE.md §4.d, con P5 y P7 explicados aparte, porque son la pregunta 3 de V, y lo que pasa el 29 de abril en el bot.
>    Si cambian las parejas o la precisión, se dice y se explica por sesión; no se ajusta nada.
>
> En cada make check, copia al informe la línea PICO DE MEMORIA de make-check.log. Si test_nunca_bloquea_y_es_rapido falla por tiempo, no lo arregles ni lo repitas en bucle: córrelo suelto una vez, apunta los dos tiempos en el informe y sigue (va al carril G).
>
> 6. El informe
> Lleva:
> - el encargo frente a lo hecho, punto por punto, y las desviaciones;
> - la fase 0, las medidas y sus guiones;
> - lo que cambia para V: la pregunta 3 gana el ejemplo del 29 de abril y la caja de la reentrada (¿la del primer intento o una nueva?), con lo que hace el bot tras esta rama;
> - dos deudas que el auditor encontró y esta rama no arregla, como líneas para Technical Debt: RN-019 probablemente no dispara nunca en el motor (su forma pide por: activacion_sin_ruptura y la orden stop lleva por = primer_esquema; verifícalo), y su nota (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta cuando A-31 está RESUELTA;
> - «Líneas preparadas para el commit del contrato de la orden de cierre»:
>   · Y sale de la Next Action a HISTORIA, bajo «# Next Action HECHA · Y · …»;
>   · F queda en «J → V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno ni a J ni a V.»;
>   · en V, «de Y» sale de su «Depende de», y gana «la pregunta 3 con el ejemplo del 29 de abril y la caja de la reentrada (PUNTO-USADO.md)»;
>   · las dos líneas de Technical Debt;
>   · en la hoja de ruta, R3.4 cambia de título y de «Qué es» a lo que hizo esta rama y pasa a HECHA con su línea de Estado; en R4.1, NA:Y sale de los Refs y «R3.4 (NA:Y)» pasa a «R3.4 (HECHA)» en «Depende de». Comprueba en memoria que test_hoja_de_ruta.py y test_project_state.py pasan con esas líneas, como simular_cierre.py de VISOR-CONSTRUCCION.
>
> 7. Revisor
> El agente revisor (opus) sobre la rama, con los dos ejes de siempre: reglas y encargo. Que compruebe además que los tests de la fase 2 van por el cableado real y fallan en main por la razón que dicen, que ninguna consulta de CI se hizo con curl ni con un guion, y que ningún guion nuevo escribe en el repo con rutas sacadas de __file__. Su informe va pegado al final del informe, con lo arreglado y lo declarado.
>
> 8. CI
> Si la rama toca hooks, rutas o el sistema de archivos, push como fix/punto-usado y CI de Linux, con su run en el informe. Si no los toca, dilo con la lista de ficheros cambiados.
>
> Rama lista para revisión, NO cerrada.
