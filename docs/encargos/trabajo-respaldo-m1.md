# Encargo · trabajo/respaldo-m1

Dado por Aleks (consultor) el 2026-10-28. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Encargo de rama: trabajo/respaldo-m1 (Z de la Next Action, R3.5 de la hoja de ruta). Consultor, 2026-10-28.
>
> 0. APERTURA
> - Base: main en 0e021bf (commit de estado del cierre de trabajo/barrido-sesion-6), sobre el merge 89dc902 con tag stable/F38i-barrido-sesion-6. Verifica con gh que la CI de main 40815230287 está en verde (no está escrita en el repo). La skill abrir-rama comprueba main, origin, el tag, la CI y que no hay otra rama.
> - Abre la rama con la skill abrir-rama: este prompt, tal cual, en docs/encargos/trabajo-respaldo-m1.md; contrato.yaml con tramo R3 · Una corrida del arnés sobre toda la construcción, y riesgo alto (toca el bróker); y el Archivo de PROJECT_STATE en HISTORIA.
> - Rutas del contrato: src/botsito/engine/llenado.py y, si la fase 0 lo pide, src/botsito/engine/broker.py; sus tests en tests/unit/; docs/adr/0051-el-modelo-de-llenado.md (solo una NOTA); docs/adr/0070-umbral-de-construccion-para-medir-mayo.md (solo una NOTA); docs/validation/RESPALDO-M1.md y docs/validation/anexos/RESPALDO-M1/ (con su README antes de correr nada: el arnés no crea la carpeta); docs/validation/HOLDOUT-EXPOSICIONES.md (solo filas nuevas). Y docs/runbooks/ACTIVAR-A35-A44.md solo si la PARADA decide que la línea base vigente cambia allí. Nada más sin ampliar el contrato a la vista y decirlo.
>
> 1. OBJETIVO
> En todo minuto sin ticks, el bróker simulado evalúa una orden contra la vela M1 cuyo cierre la colocó, con precios anteriores a la orden. Va contra ADR-0051 §2 («sin mirar al futuro: el motor decide con lo que ya cerró») y ADR-0056 §2 («el tick en que se decide no cuenta»). Lo midió trabajo/recorrida-construccion (RECORRIDA-CONSTRUCCION.md §2.8 c y PARADA 3): 2 llenadas así en la corrida que cuenta y 10 en la diaria.
>
> La CONDICIÓN que se corrige, y no el caso: ningún evento del modelo de llenado se evalúa contra un precio anterior al instante en que se decidió lo evaluado. Con ticks ya se cumple. Con el respaldo M1, mi lectura es que una vela solo puede evaluar algo si EMPIEZA EN O DESPUÉS del instante de su decisión (inicio de la vela >= instante), con ese instante tomado del propio objeto (ultimo_cambio_ms de la orden; abierta_ms y stop_movido_ms de la posición), y no del «desde» que usa _proximo_evento, que lleva el truco de «ahora - 1». No es una decisión cerrada: la forma exacta sale de la fase 0 y la decido en la PARADA. Dos formas que el auditor ya ha descartado, para que no se repitan: aplicar la condición sobre el desde_ms = max(ahora - 1, …), que apaga el respaldo para una orden que ya estaba pendiente; y excluir la vela que empieza justo en el instante de la decisión, que salta la vela siguiente a un llenado del respaldo (contra ADR-0057 §1) y rompe tests de main que colocan en el inicio exacto de una vela.
>
> Se prueba con tests que rompen en main, una NOTA en ADR-0051 y las dos corridas de recorrida-construccion repetidas.
>
> QUÉ NO CAMBIA: la spec (knowledge/spec/), los casos (knowledge/cases/), parametros.yaml, knowledge/simulador/llenado.yaml, el motor de la estrategia (zonas, sesgo, cartuchos, cuenta), ADR-0051 §1, §4 y §6, ADR-0057 §1 y ninguna cifra. Si arreglar Z exige tocar algo de esto, PARADA.
>
> 2. FASE 0 · INVENTARIO SIN TOCAR NADA (entrega antes de escribir código; PARADA al final)
> Mide, no razones: cada afirmación con fichero:línea o la salida de un comando.
>
> a) Cada lectura del respaldo M1 y cada precio que el bróker toma sin tick. Verifica que la lista es completa (grep de «.m1(», «cotizacion», «RESPALDO_M1», «_precio_de_mercado» y «precio_de_conversion» en src/). Lo que ha visto el auditor:
>    - en llenado.py: primer_llenado_limite, primer_llenado_stop y primera_salida (la condición «_fin_ms(vela) <= desde_ms», :160, :209 y :288) y Mercado.cotizacion (:93-113);
>    - en broker.py: _proximo_evento (:749 y :763), _peor_del_minuto (:910), _precio_de_mercado y precio_de_conversion (:935-964), y sus llamadores: _precio_infringido (:537, precio_invalido), colocar (:511), cerrar_a_mercado (:607), mover_stop (:665-669) y _marcar_hasta (:883-896, que pasa a cuenta.marcar en cableado.py:449-450, la peor equity que leen los topes);
>    - primitivas_broker.py (:542 y :585) y simulacion.py (:79, la repetición del trader, que también cambiaría).
>    Para cada una: a qué instante sirve, y si su vela puede llevar precios ANTERIORES a lo que evalúa (la condición de Z) o POSTERIORES al instante que cotiza (mirar al futuro). Dos posibles casos de futuro, que verificas y llevas a la PARADA sin arreglarlos: _peor_del_minuto acepta una vela cuyo fin llega hasta un minuto después de «hasta»; y _precio_de_mercado y precio_de_conversion, en un minuto con ticks pero sin ningún tick anterior al instante, caen a la vela de ese minuto y toman su cierre, que es posterior. Y la diferencia, en una misma colocación a cierre menos 1 ms, entre la M1 que usa cotizacion y la que usa precio_de_conversion.
> b) La deuda de COTIZAR. La línea de Technical Debt que la Z absorbió en recorrida-construccion hablaba de cotizar: cotizacion decide precio_invalido en el primer cierre de la ventana con la M1 de un minuto antes (VISOR-CONSTRUCCION.md §4.3, punto 6). Di si es la condición de Z o otra. En la PARADA decido si entra en esta rama o vuelve a Technical Debt con su texto; no puede desaparecer al cerrar Z.
> c) En qué instante se decide y se coloca una orden (verifica que es el cierre de la M1 menos 1 ms, cableado.py :297 y :313) y qué vale ultimo_cambio_ms al colocar (:522-523) y al modificar (:585, :805, :831, :837 y :863). Con eso explica, en los dos «NO» de §2.8 (2026-04-07 07-11 o1, en el borde de la ventana, y 2026-04-23 07-11 o3) y en el de hora perdida de la corrida 1 (2026-01-05 11-15 o20), qué vela llenó la orden y por qué entró. Lee las salidas commiteadas de docs/validation/anexos/RECORRIDA-CONSTRUCCION/ y los ticks de esos días dev; nada anterior a las 00:00Z del día.
> d) La vela del llenado frente a la salida. ADR-0051 §3 dice que en el respaldo, «dentro de una M1 que cubre la límite de entrada y luego el stop, se toma que la entrada se llenó y el stop saltó en la misma vela». ADR-0057 §1 (ACTIVE) dice lo contrario, «la salida se mira desde la vela siguiente», sin NOTA en ADR-0051, y test_broker_ordenes_stop.py :150-176 lo fija. Verifica qué hace el código hoy. Propón si la NOTA de esta rama en ADR-0051 recoge también esa contradicción en §3, remitiendo a ADR-0057 §1 sin cambiar lo que decide. Esta rama NO cambia la regla de ADR-0057 §1.
> e) Los eventos del respaldo que no son llenadas: 4 en la corrida 1 y 18 en la 2 (§2.8 c; costes_y_sesiones.py :416-436 solo marca las llenadas). Cuenta cuántos se evaluaron contra la vela en cuyo cierre se decidieron: stops movidos (ADR-0065 §3 y §5: sin ticks el break even se pone al cierre de la M1, con fuente respaldo_m1), salidas y modificaciones. Si los hay, entran en la corrección y en los tests.
> f) La forma de la corrección que propones, en una o dos frases y con su línea de código, y por qué es la condición y no el caso. Lo que tiene que seguir igual, y lo pruebas en la fase 1:
>    - una orden pendiente desde ANTES de una vela sin ticks sigue pudiendo llenarse en esa vela;
>    - el tick del último evento sigue pudiendo llenar otra pendiente («ahora - 1»);
>    - la salida tras un llenado del respaldo se mira desde la vela siguiente (ADR-0057 §1);
>    - los tests de main que colocan en el inicio exacto de una vela siguen pasando sin tocarlos. Verifica cuáles son (el auditor señala test_broker.py :222, test_broker_ordenes_stop.py :150-176 y los del respaldo de test_llenado.py :109-166). Si alguno tiene que cambiar, PARADA.
> g) Los guiones que la fase 2 va a reutilizar de docs/validation/anexos/RECORRIDA-CONSTRUCCION/:
>    - costes_y_sesiones.py fija su carpeta (AQUI, :28-29) e importa horas_perdidas de ella;
>    - patrones.py recibe el fichero por argumento pero importa horas_perdidas de su carpeta;
>    - lista_s14.py recibe la carpeta e importa patrones de ella;
>    - costes_y_sesiones.py y lista_s14.py leen además entradas-antes-alternancia.txt, que sale de entradas_antes_alternancia.py, otra corrida entera del motor con calentamiento.
>    Propón: o se vuelve a correr ese guion (con su fila de exposición), o las copias de anexos/RESPALDO-M1/ se adaptan para no necesitarlo. Las copias llevan horas_perdidas.py al lado y la raíz por argumento; los originales no se editan.
>    Además, la parte c de costes_y_sesiones solo compara colocada_ms == e.ms - 1, es decir, solo llenadas: propón cómo se amplía la copia a stops, salidas y modificaciones.
> h) La línea base vigente. Verifica quién la nombra hoy: la NOTA del 2026-10-27 de ADR-0070 §3, ACTIVAR-A35-A44.md :206-212 y el README de anexos/RECORRIDA-CONSTRUCCION, que dice que no se edita. Propón cómo pasa a serlo la corrida 1 de esta rama sin editar nada que no se edite.
> i) Recuentos de partida por la compuerta:
>    - casos_reservados y casos_ocultos por mes, solo recuentos, con un guion de la carpeta de trabajo que reciba la raíz por argumento y no imprima claves;
>    - los días dev de construcción;
>    - los manifiestos de ticks, que tienen que ser los cuatro de RECORRIDA-CONSTRUCCION.md §0.b.
>    Y el tiempo esperado de lo medido después: corridas de 299 a 343 s y unos 630 MiB (RECORRIDA §2), y make check de 1022 a 1170 s (BARRIDO-SESION-6).
> j) Herencias. Busca en la Next Action, los pendientes heredados, el final de HISTORIA y los informes de octubre todo lo que nombre el respaldo M1, ADR-0051, ADR-0057 §1 o «la vela que la colocó», y di qué entra y qué no. La deuda de engine/simulador_config.py (el spread supuesto por la hora de pared) NO entra: solo importa en los días de desfase (marzo del 9 al 27 y la semana del cambio de octubre), y ningún mes de construcción los tiene. Dilo con su fuente.
> k) Exposiciones. La lectura de la fase 0 (salidas y ticks de días dev) se declara el MISMO DÍA en HOLDOUT-EXPOSICIONES, en el commit de la fase 0. Y propones la fila de las fases 1 y 2, que declara:
>    - los make check de la rama, que leen el M1 de marzo (test_visor.py y test_preparar_a35.py);
>    - las pruebas del clon de comparar-con-main (precedente: la fila a1 de recorrida-construccion en ERRORES-RECURRENTES);
>    - el calentamiento de las corridas, con arnes.dias_de_mercado: el M1 entero de marzo para abril y de junio para julio, y julio entero para agosto (los días 18 a 31 de julio no están en ninguna partición ni son construcción);
>    - y, si se decide, la corrida de entradas_antes_alternancia.py.
>    Leer velas para calentar no es abrir (CLAUDE.md, punto 2 de «Que se puede mirar»; ADR-0033 §4). Ninguna etiqueta ni cifra del bot de un día reservado.
>
> PARADA con «Lo que necesito que decidas», numerado y con una recomendación por punto. Al menos: la forma de la corrección (f), lo que encuentres en a), la deuda de cotizar (b), la NOTA en §3 (d), los eventos que no son llenadas (e), los guiones (g), la línea base (h) y la fila (k).
>
> 3. FASE 1 · LA CORRECCIÓN Y SUS TESTS (tras mi respuesta)
> - Tests nuevos en tests/unit/ que ROMPEN en main y pasan en la rama. Se prueban con la skill comparar-con-main en un clon desechable, y el informe pega la salida de los dos lados:
>   1. una orden stop de entrada colocada en el cierre de una M1 sin ticks (cierre menos 1 ms), cuyo nivel cruza esa vela y no la siguiente: en main se llena con fuente respaldo_m1 al cierre de esa vela; en la rama, no;
>   2. lo mismo con una límite;
>   3. el borde de la ventana: la orden se coloca en el último milisegundo de un minuto sin ticks, los ticks empiezan en el minuto siguiente y solo se evalúa contra esos ticks;
>   4. lo que decida la PARADA sobre e): el stop movido o la salida contra la vela en cuyo cierre se decidió.
> - Y los del otro sentido, que pasan en main y en la rama: los cuatro puntos de f).
> - Docstring de llenado.py: la línea del respaldo (:13-15) dice la regla, como la de los ticks (:10-12), y la cabecera deja de decir «ADR-0051, PROPUESTO» (el ADR está ACTIVE).
> - NOTA en ADR-0051 §5 (y en §3 si así se decide en la PARADA), con fecha y rama, sin reescribir el cuerpo, con el texto que salga de la PARADA.
> - Si el arreglo toca una cifra, un parámetro o la spec: PARADA.
>
> 4. FASE 2 · LAS CORRIDAS REPETIDAS
> - Antes de correr nada, en su propio commit, la fila de exposiciones decidida en la PARADA.
> - Una cosa a la vez, en segundo plano con CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1, y nunca a la par de un make check. Si una muere por memoria, no se relanza sin decirlo.
>   1. uv run botsito motor arnes --simular --salida docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt (la que cuenta por ADR-0070: sin ningún --diagnostico-*).
>   2. uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RESPALDO-M1/diaria.txt. Verifica el nombre real del fichero que escribe: en recorrida-construccion fue «diaria.DIAGNOSTICO.cuenta=diaria.txt».
>   3. La repetición de la 1 en la carpeta de trabajo, diff contra la commiteada y borrar la copia (determinismo).
>   4. Lo que se decida en g).
> - Sobre las salidas nuevas, con las copias de g): los patrones de las dos corridas y la parte c ampliada.
>   - Criterio de hecho: CERO eventos (llenadas, stops, salidas, modificaciones) evaluados con una vela que empieza antes del instante de su decisión, en las dos corridas.
>   - Los demás eventos del respaldo, contados y explicados.
> - Qué cambia frente a recorrida-construccion, por corrida: el veredicto literal de la línea de ADR-0070 («habilita medir…»), cobertura, precisión, parejas y llenadas por mes, y desde qué día congela RN-032 la cuenta arrastrada, si cambia. Sin interpretar más allá de la cifra: la clasificación de diferencias es del consultor.
> - Los gráficos de S-14 de la sesión 6 salen de la corrida 2 de recorrida-construccion, y scripts/graficos_sesion.py dibuja la PRIMERA orden de cada sesión (canceladas incluidas: su M1 y su nivel). Para las 8 sesiones elegidas (BARRIDO-SESION-6.md §1.d, filas 18, 4, 6, 9, 17 y 20, y las de reserva 26 y 10), di si en la diaria nueva:
>   - siguen siendo P6 (el bot opera y el trader no);
>   - y su primera orden tiene la misma M1 de colocación, el mismo nivel y el mismo lado.
>   SIN imprimir ningún R. Si alguna cambia, PARADA antes de seguir: hay que rehacer ese gráfico antes de la sesión.
> - La NOTA de ADR-0070 §3 de esta rama, sin reescribir el cuerpo: el veredicto de la corrida 1 nueva y lo que se decida en h).
>
> 5. INFORME, REVISOR Y ENTREGA
> - docs/validation/RESPALDO-M1.md, con:
>   - la fase 0, la PARADA y mi respuesta tal cual;
>   - la corrección y los tests, con su salida en los dos lados;
>   - las corridas: comandos literales en orden, tiempos y PICO DE MEMORIA;
>   - las exposiciones;
>   - el encargo frente a lo hecho y las desviaciones.
> - Las líneas del cierre, preparadas y medidas sobre una copia, sin aplicar en la rama:
>   - sale Z de la Next Action, con su registro nuevo «# Next Action HECHA · Z · …» en HISTORIA (RITUAL, punto 3);
>   - F termina en «R6a en los huecos.», sin «y Z»;
>   - R3.5 gana su «Estado: HECHA» con la rama y el informe;
>   - R5.2 deja de nombrar NA:Z (si no, test_hoja_de_ruta rompe en cuanto Z sale) y pasa a nombrar R3.5, HECHA;
>   - lo que se decida en b) (la deuda de cotizar, si vuelve a Technical Debt);
>   - PROJECT_STATE medido con wc -c sobre la copia con todas las líneas: por debajo del tope de 25.000 bytes y, si se puede, de la alerta de 23.000 de ERRORES-RECURRENTES.
>   Comprueba la copia contra tests/unit/test_hoja_de_ruta.py.
> - La fila de ERRORES-RECURRENTES de la rama, preparada.
> - El revisor (opus), antes de declarar la rama lista, con estos alcances:
>   1. que cada test nuevo rompe en main por la causa de Z y no por otra;
>   2. que la condición se aplica en TODA lectura del respaldo del inventario, negando por defecto; que ADR-0057 §1 y lo que va por ticks no cambian; y que los tests de main de f) pasan sin tocarlos;
>   3. holdout: las filas el mismo día y antes de correr, nada anterior al día dev impreso, ningún R de las sesiones de S-14;
>   4. que las NOTAS de ADR-0051 y ADR-0070 no reescriben el cuerpo;
>   5. que las líneas del cierre pasan test_hoja_de_ruta sobre la copia, y que la deuda de cotizar no desaparece.
>   Su informe va pegado al final. Arregla lo que bloquee o importe, o di por qué no.
> - No toca hooks, rutas ni plataforma: el fix/ en la CI de Linux no es obligatorio. Si la skill entregar-rama lo empuja igual, pega el número de run.
>
> Reglas de siempre:
> - make check > make-check.log 2>&1 antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado, y leer el log (exit 0, ningún failed y la línea SELLO). Nunca --no-verify.
> - Mensajes de commit con Write y git commit -F.
> - Si la guardia o el clasificador niegan algo legítimo, PARADA con el comando exacto, y lo lanza Aleks con «!». No se rodea.
> - Una sola rama abierta: si el trader graba la sesión 6 mientras esta rama sigue abierta, la ingesta espera a que se cierre.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA (2026-10-29)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/respaldo-m1 (2026-10-29). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> Contexto de la decisión del punto 1. Tu fase 0 mide cuatro síntomas: los casos de Z, los 22 cancelados en el cierre de una M1 sin ticks (punto 8), la marca un minuto adelante de _peor_del_minuto (punto 2) y ADR-0065 §4 sin cumplir. Pensé que tenían una raíz común: el respaldo sella su evento en el cierre de la vela (k fin, ADR-0051 §5 y ADR-0057 §1), un milisegundo después de que el motor decida (k fin - 1). Por eso estudié una forma (c): sellar en k fin - 1. Mi auditor la probó con un prototipo en memoria sobre main, con datos sintéticos, y midió que (c) no es neutral fuera de las tres funciones de llenado.py:
> - la posición abierta por el respaldo cae en el minuto k, así que las marcas (broker.py:888 y :909-913) meten la vela del llenado. En la sonda, una marca de 970 por debajo de un stop de 990 llega a cuenta.marcar y a los topes antes de la decisión;
> - el break even por velas (primitivas_broker.py:279, m1_entre desde abierta_ms) mete la vela del llenado en la zona posterior de RN-014;
> - un llenado en la última vela de 07-11 pasa de la sesión 11-15 a la 07-11 (cableado.py:464-465);
> - cambian el fin de la ventana (la última vela pasa a evaluarse) y el borde de la ventana prohibida (ADR-0068);
> - rompen 5 tests de main, todos por ese milisegundo;
> - y choca con ADR-0057 §1, que también sella al cierre y está en «QUÉ NO CAMBIA».
> Así que (c) es otra rama con su propio ADR, no esta. Va como entrada nueva (punto 8), con lo que midió el auditor.
>
> 0. (a). El informe y las líneas del cierre dicen las dos cifras: 2 llenadas y 0 stops en la corrida 1; 10 llenadas y 2 stops en la 2.
>
> 1. (b), tal como la propones:
>    - las tres funciones del respaldo reciben el instante de la decisión de lo que evalúan, decidido_ms, que por defecto vale desde_ms. Una vela solo cuenta si EMPIEZA en o después de él. El instante sale del objeto: ultimo_cambio_ms en la orden; abierta_ms en la salida con el stop de nacimiento;
>    - la vela que contiene stop_movido_ms se evalúa con el stop ANTERIOR (ADR-0065 §4) y las siguientes con el nuevo;
>    - una orden modificada sigue la misma regla con su precio anterior.
>    Sin tocar desde, el «ahora - 1», los ticks, el instante del evento (sigue en el cierre de la vela, ADR-0051 §5 y ADR-0057 §1) ni _fin_ms, que también usa Mercado.cotizacion.
>    (b) no está prototipada. Los tests de main que la rozan (los de §0.f y los nueve ficheros del prototipo de (a)) tienen que pasar sin tocarlos. Si alguno tiene que cambiar, PARADA.
>    Los tests de la fase 1 cubren, además de los del encargo, el stop movido: una vela que toca el stop original y la entrada sale por el stop original, sin break even. Y la modificación de una orden con su precio anterior.
>
> 2. Los dos casos de futuro no se arreglan aquí.
>    - _peor_del_minuto entra en la letra nueva del punto 8, nombrado por su condición: acepta toda vela que EMPIEZA en o antes de «hasta», así que cuando se avanza hasta un instante redondo (cada evento del respaldo, una cancelación por ventana, una expiración) marca entera la vela siguiente. Va con su sonda 5 y con la del auditor (avanzar a un instante redondo marca la vela siguiente).
>    - _precio_de_mercado y precio_de_conversion van al punto 3.
>
> 3. (a), en una línea de Technical Debt que nombra la condición: «Las cotizaciones sin tick del bróker no usan la misma vela. En el cierre de la M1 k, Mercado.cotizacion (precio_invalido y stops_level, ADR-0057 §4) usa lo último cerrado antes del instante, que sin ticks es la M1 k-1 o el último tick anterior, y _precio_de_mercado y precio_de_conversion (cierre a mercado y margen) usan la k. Y en un minuto con ticks sin ninguno anterior al instante, estas dos toman el cierre de su vela; el motor no llega a ese caso (RESPALDO-M1.md §0.a y §0.b). Decidirlo es una NOTA o un ADR sobre ADR-0057 §4.»
>
> 4. (a). La NOTA va en ADR-0051 §5, con la condición de (b): la vela cuenta si empieza en o después de lo decidido, y la vela del stop movido se evalúa con el stop anterior. Y otra en §3: la salida tras un llenado del respaldo se mira desde la vela siguiente (ADR-0057 §1, el código y sus tests), sin cambiar lo que decide.
>
> 5. (a), con dos condiciones:
>    - censo_respaldo.py detecta Z por la condición general (el inicio de la vela del evento, (ms - 1) // 60000 en minutos, es anterior al instante decidido) y no solo por colocada == ms - 1. Así el criterio de hecho de la fase 2 no queda vacío por construcción.
>    - sesiones_s14.py toma el lado de «### Ordenes» si lo trae. Si no, la deducción por la caja 1 se comprueba en las 8 sesiones contra la diaria de RECORRIDA, y tiene que dar el mismo lado que dibujó scripts/graficos_sesion.py. Si alguna no cuadra, PARADA.
>
> 6. (a). El contrato se amplía a docs/runbooks/ACTIVAR-A35-A44.md en un commit a la vista, solo para la NOTA de §5.
>
> 7. (a).
>
> 8. (a), en UNA letra nueva de la Next Action, no en Technical Debt. Elígela con la regla de letras de DECISIONES-DE-PROCESO.md y di cuál es, con el grep. Su texto, en el cierre:
>    «<letra>. En el respaldo M1 el evento de una vela se sella en su cierre, un milisegundo después de que el motor decida (ADR-0051 §5, ADR-0057 §1). Por eso la vela k no se evalúa para lo que vivía en ella cuando el motor actúa en su cierre (22 de 1002 cancelaciones en la corrida diaria de recorrida-construccion, RESPALDO-M1.md §0.l), y _peor_del_minuto marca entera la vela siguiente cuando se avanza hasta un instante redondo. Rama propia con un ADR que enmiende esos dos ADR. Antes de decidir, se mide lo que el auditor de RESPALDO-M1 encontró en la forma «sellar en k fin - 1»: las marcas y m1_entre del break even empiezan a contar la vela del llenado, cambia la sesión de un llenado en la última vela de 07-11, cambian el fin de la ventana y el borde de ADR-0068, y rompen 5 tests de main por el milisegundo. Va antes de la próxima corrida del arnés que cuente (ADR-0070 §3).»
>    En la hoja de ruta entra R3.6 con esa letra (Refs NA:<letra> · ID:ADR-0051 · ID:ADR-0057; Depende de: R3.5; Quién: la sesión, con el encargo del consultor; Hecho cuando: el ADR está aceptado, un test que rompe en main pasa en la rama y las dos corridas están repetidas). R5.2 nombra la letra nueva en «Depende de», en lugar de NA:Z.
>    Comprueba la copia contra test_hoja_de_ruta.
>
> 9. (a). La NOTA de ADR-0051 dice que la repetición del trader sin ticks (ADR-0051 §8, REPETICION-TRADER-SALIDA.txt) ya no se reproduce igual, y que esta rama no la vuelve a correr.
>
> 10. (a). Antes de la fase 2, Aleks cierra Claude Code y lo vuelve a abrir con la variable puesta. Al empezar la fase 2, compruebas que vale 1 y escribes en el informe cómo lo has comprobado. Las corridas van sin la variable delante y en segundo plano. Si la variable no está puesta, PARADA antes de correr.
>
> Dos hallazgos del consultor para la fila de ERRORES-RECURRENTES de la rama, en el cierre. Los dos los encontró su auditor antes de que llegaran a la sesión:
> - En el encargo escribí la condición de Z como «una vela cuyo intervalo empieza en o antes de ese instante no cuenta», con la NOTA en el mismo sentido, sin medir el borde y sin leer ADR-0057 §1. Lección: una condición sobre instantes se escribe con el borde medido (qué vale exactamente en el instante de la decisión) y con todos los ADR que fijan ese borde.
> - En el primer borrador de esta respuesta propuse mover el sello del respaldo a k fin - 1, con una regla para que la sesión decidiera sola. No había buscado los otros lectores de abierta_ms y del minuto del evento (las marcas, el break even por velas, la sesión, la ventana). Y la regla se contradecía: pedía tests de main intactos y a la vez admitía que cambiaran. Lección: antes de proponer que se mueva un instante, se buscan con grep todos los que lo leen. Y una regla que deja decidir a la sesión no puede contradecirse ni tocar lo que «QUÉ NO CAMBIA» protege.
>
> Lo que sigue, en este orden: el commit con esta respuesta; la fase 1; Aleks reinicia Claude Code con la variable; la fase 2; el informe, el revisor y la entrega. make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA 2 (2026-10-29)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/respaldo-m1 (2026-10-29). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha, y aplícala.
>
> 1. (a). sesiones_s14.py compara, en las 8 sesiones, lo que el gráfico dibuja (la M1 de colocación y el punto de la primera orden) y, además, el precio y el lado deducido por la caja 1, que ya está validado en las 291 llenadas de la diaria de RECORRIDA cuyo lado se conoce. El informe dice que el lado se deduce, con esa validación. Si en alguna sesión cambia CUALQUIERA de las cuatro cosas (M1, punto, precio o lado deducido) entre la diaria de RECORRIDA y la nueva, o si deja de ser P6, PARADA antes de seguir, sin imprimir ningún R.
> 2. La letra H para el punto 8: aceptada, con su grep en el informe.
> 3. Un hallazgo más del consultor para la fila de ERRORES-RECURRENTES, en el cierre: en la respuesta a la PARADA pedí comparar «el mismo lado que dibujó scripts/graficos_sesion.py» sin leer el script, que no dibuja el lado (graficos_sesion.py:98-101). Lección: una comprobación contra un artefacto se escribe después de leer qué contiene ese artefacto.
> 4. Lo que sigue: el commit con esta respuesta; Aleks reinicia Claude Code con la variable; compruebas que vale 1 y escribes cómo lo has comprobado; la fase 2 como dice el encargo, una corrida cada vez, en segundo plano y nunca a la par de un make check; el informe, el revisor y la entrega. Si la variable no está puesta, PARADA antes de correr.
>
> make check en verde antes de cada commit. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.
