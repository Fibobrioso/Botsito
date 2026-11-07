# Encargo · trabajo/demo-ejecuciones-2-3

Dado por Aleks (consultor) el 2026-11-06, en un solo mensaje. Copiado tal cual (el ADR que el
encargo manda escribir, ADR-0090, fue declarado aquí en el bloque `ids-inexistentes` que el propio
encargo traía, como exige `knowledge validate`, hasta el commit del punto 2 de la fase 1, que lo
crea y quita ese bloque, como el encargo manda):

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-06) · trabajo/demo-ejecuciones-2-3 · tramo «Carril: lo de Aleks» (A.1 de la hoja de ruta; A de la Next Action)
>
> Rama nueva: trabajo/demo-ejecuciones-2-3, desde main (a46eadd, commit de estado sobre el merge 4fa0920 del tag stable/F38o-activar-sesion-06-motor; CI de main en verde, run 42300034254: compruébalo con un gh run view suelto, sin guion). Ábrela con la skill abrir-rama: base comprobada con git, contrato con tramo: "Carril: lo de Aleks" (entre comillas), riesgo alto (cambia un valor que lee el bróker simulado y que mueve el saldo de la cuenta simulada), artefacto docs/validation/DEMO-EJECUCIONES-2-3.md. El recorrido lo mandan las skills fase-cero, comparar-con-main y entregar-rama; si este encargo y ellas chocan, ganan ellas y lo dices. Es rama de laptop: necesita data/demo_ftmo/ y los originales de MQL5\Files. Antes de usar el número 0090, grep de «0090» en docs/ y en Technical Debt (lección de F38l). Si el informe cita ADR-0090 antes de que exista, lleva su propio bloque ids-inexistentes, que sale en el mismo commit.
>
> Objetivo: congelar los CSV de las ejecuciones 2 y 3 de MedirDemoFTMO y fijar con un ADR nuevo, ADR-0090, lo que esas ejecuciones deciden: A-28; lo que ADR-0071 dejó esperando a ellas (la tarifa de la comisión, el nivel exacto de ADR-0057 §2, la ficha, los swaps y el deslizamiento); y el resultado del paso 8 (ADR-0081 §4).
>
> NO cambia: el código de src/ (motor, bróker simulado y límite del lote incluidos), la estrategia, strategy_spec.yaml, tools/mql5/MedirDemoFTMO.mq5, scripts/leer_demo_ftmo.py, el valor y el estado de anclaje_h4 y de reloj_dia_riesgo, el manifiesto de la ejecución 1 (inmutable) ni los informes cerrados (solo recuadros). Nadie ejecuta uv run botsito motor arnes. No se toca corpus, holdout ni material del trader.
>
> Declaración de Aleks (2026-11-06, en el chat del consultor): las tres ejecuciones se copiaron tal cual de MQL5\Files a data/demo_ftmo/, sin abrirlas con Excel, y los originales siguen allí. La 2, el 2026-10-29 con el script 1.1, en la prueba gratuita creada ese día. La 3, el 2026-11-05 con el script 1.2, terminada «completo» y sin nada abierto. La 3 corrió a las 20:35 del servidor, fuera de la franja de 9 a 18 de España del runbook, con Nueva York abierto.
>
> Lo que leyó el consultor el 2026-11-06 por el puente, en solo lectura. Son lecturas, no datos: VERIFICA cada una con sha256sum y con el lector, y si alguna no cuadra gana tu medida y lo dices con su nombre.
> - data/demo_ftmo/ tiene tres CSV: MedirDemoFTMO_20261009_153552.csv (9907 bytes, sha256 86f0df8b…, el del manifiesto de la 1), MedirDemoFTMO_20261029_194056.csv (10167 bytes, sha256 1b82f61b…) y MedirDemoFTMO_20261105_203519.csv (18991 bytes, sha256 59565621…).
> - Fila 31, desfase_servidor_gmt_min: 180, 180 y 120. Fila 32, desfase_local_gmt_min: −300 en las tres.
> - Paso 6 de la 2 y de la 3, con 1,00 lote: −2,50 al abrir y −2,50 al cerrar. La 2 tiene 2,0 puntos de deslizamiento en contra al abrir; el resto, 0. Paso 7: 0,0 en las dos.
> - Paso 4, nivel exacto: en la 2 la buy limit se llenó al instante y las otras tres quedaron vivas; en la 3 las dos stop se llenaron al instante y las dos limit quedaron vivas.
> - Paso 8 de la 3: p8_tasa_buy_stop 0;0; m1_colocar DONE con 26,71 lotes, margen al ask por encima del margen libre; m2, el margen y el margen libre no cambian; m3, las dos colocadas; m4_resultado no_salto.
>
> Herencias que entran (cada una se cumple o se dice por qué no): ADR-0071 §3 (la tarifa se mide en la 2), §4 (el nivel exacto espera a la 2 y la 3), §5 (el deslizamiento) y §6 (una diferencia en la ficha reabre A-27); el punto 4 de la respuesta a la PARADA de MARGEN-PENDIENTE.md (5,00 USD por lado «mientras el CSV de la ejecución 2 no esté congelado») y su regla de lectura del paso 8 (§0.d); ADR-0027 §4 (verificar anclaje_h4 contra la rejilla H4 real); la «verificación explícita» del panel dentro de A-28; la deuda técnica del CRLF (texto entero en HISTORIA); knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml (PROVISIONAL, «se revisa» con A-28); los heredados 10 y 27; y las entradas A y M de la Next Action. Busca además «la rama que congele», «ejecución 2», «ejecuciones 2 y 3» y «A-28» en PROJECT_STATE, en el final de HISTORIA, en HOJA-DE-RUTA, en los ADR y en los informes de octubre y noviembre, y añade lo que falte.
>
> FASE 0, inventario sin tocar knowledge/, docs/adr/ ni src/:
> a) La salida de uv run python scripts/leer_demo_ftmo.py data/demo_ftmo, pegada entera, contrastada con cada lectura del consultor de arriba.
> b) Los originales de MQL5\Files frente a las copias: sha256, bytes y fin de línea (recuento de CR) de los tres. Si la guardia no te deja leer fuera del repo, dale a Aleks el comando exacto de PowerShell, que lo lanza con «!» (la carpeta la abre él con Archivo → Abrir carpeta de datos).
> c) Una tabla medida → decisión de la 2 y la 3, como la de DEMO-EJECUCION-1.md: cada fila, a qué responde, qué dice hoy el repo y qué dice la medida.
> d) Quién lee broker_offset_base, broker_dst y firma_comision_usd_por_lote en src/, tests/ y scripts/, y por dónde llega la comisión al saldo, al tope del trader, a los límites de la firma, al margen libre y al lote, con fichero:línea. El auditor del consultor apunta a cableado.py, cuenta.py y primitivas_broker.py: verifícalo.
> e) Qué tests rompen con la comisión a 2,50, medido como manda comparar-con-main.
> f) Los rechazos por margen_libre (al colocar y al llenar) del informe o anexo más reciente del arnés sobre construcción (RECORRIDA-CONSTRUCCION.md y posteriores), sin ejecutar nada.
> g) Todas las frases de los documentos vivos que quedan falsas al decidir A-28 y al cambiar la comisión. Como mínimo verifica: parametros.yaml (cabecera :56-60, :146, :159-160, anclaje_h4 hacia :310, reloj_dia_riesgo hacia :1628, :1700, firma_apalancamiento hacia :2088-2091), la descripción de firma_comision_usd_por_lote en el perfil y el yaml de cierres :8-10.
> h) Las líneas del cierre, preparadas sobre una copia: A y M de la Next Action, heredados 10 y 27, Technical Debt (sale la del CRLF y entran las nuevas), A.1 (que lleva NA:M y HER:10: si pasa a HECHA, M y el grabador de F17 se mudan de entrada, y test_hoja_de_ruta lo comprueba), R6a.1, R6a.6, R6a.7, la fila F:F17 y «Fechas fijas». Con la previsión de PROJECT_STATE medida con wc -c, por debajo de 23.000.
>
> DECISIONES DEL CONSULTOR, POR ADELANTADO (2026-11-06):
> D1. Manifiestos. Dos nuevos, de la 2 y de la 3, escritos a mano con schema_demo_ftmo: 1 (data/manifests/README.md, «Demo de FTMO») y el de la 1 como modelo: script.version 1.1 y 1.2, con el sha256 de cada .mq5 y el commit que lo trajo (búscalo en la historia; ramas trabajo/demo-ejecucion-1 y trabajo/margen-pendiente), cuenta.tipo de la prueba del 2026-10-29, fin_de_linea medido y declarado_por con la declaración de Aleks. El de la 1 no se toca.
> D2. Originales y deuda del CRLF. Si cada original coincide con su copia en sha256, la deuda sale por (a) (docs/state/README.md), con esa evidencia y el fin de línea de los tres; lo medido el 2026-10-19 (EA-CONEXION.md §0.c) se explica o queda declarado como residual. Si algún original difiere de su copia, PARADA solo para ese fichero, y ese no se congela.
> D3. A-28 DECIDIDA por ADR-0090, como A-27 por ADR-0071: broker_offset_base = 120 y broker_dst = us, los dos CONFIRMED con fuente ADR-0090, que cita los tres manifiestos y su fila 31. Regla de lectura, escrita antes de que mires: discrimina el 29-oct, porque Europa cambió de hora el 25 y EE. UU. el 1-nov; con eu daría 120, con us 180, y con ninguno las tres saldrían iguales. Si las tres medidas no dejan una sola opción, PARADA. Di cuánto depende el desfase del reloj del ordenador (hora_gmt sale de TimeGMT) y por qué el −300 de la fila 32 lo acota. Añade como observación concordante el desfase del journal del 2026-10-21 (anexos/EA-CONEXION/demo-20261021-cierre/; verifica que da 10800 s). Ciérrala en sus sitios según docs/runbooks/AMBIGUEDADES.md: los cinco, test_kit con A-28 entre las DECIDIDAS, su fila fuera de Known Ambiguities dentro de la rama, y spec_version, uv run botsito spec manifest --escribir y uv run botsito spec docs --escribir en el mismo commit. Reescribe todas las frases de g).
> D4. anclaje_h4 (ADR-0027 §4). Inferir que la medianoche del servidor cae a las 17:00 de Nueva York no es la medida que pide §4. El valor y su estado no se tocan. ADR-0090 escribe esa cuenta como DERIVACIÓN, no como medida: con zoneinfo, del 2026-01-01 al 2027-12-31, con 120 y us, la medianoche del servidor cae a las 17:00 de Nueva York todos los días; si un solo día no cae ahí, PARADA. Con un recuadro en ADR-0027 §4, enmienda «en la misma medición»: la rejilla real la mide R6a.1, con el EA escribiendo en el journal de la demo la hora de apertura de las velas H4 (iTime), antes de R6a.7 y de F33. La descripción de anclaje_h4 lo dice, y la línea de R6a.1 va preparada para el cierre.
> D5. El panel (la verificación explícita de A-28). Si Aleks te declara, con fecha y hora, a qué hora se reinició el límite diario en el panel de la prueba, entra en ADR-0090 como declaración. Si cae a medianoche de España, reloj_dia_riesgo no cambia. Si cae a medianoche del servidor, PARADA (A-28 dice que entonces se reabre A-19). Si no te lo declara, A-28 se decide igual por su pregunta (desfase y calendario), y la verificación pasa con su texto entero a una línea propia para Aleks, preparada para la Next Action del cierre. El «dentro de A-28» de reloj_dia_riesgo se reescribe para que apunte a esa línea.
> D6. Comisión. firma_comision_usd_por_lote pasa de 5 a 2,50 por lote y lado (firma_comision_por_lado sigue en true), CONFIRMED con fuente ADR-0090, que cita las filas del paso 6 de la 2 y de la 3. Recuadro en ADR-0071 §3. Di cómo se lee el «commission: 5» de la API con esta medida, y si eso contesta el asterisco de «USD/LOT*» del heredado 27, sin cerrarlo, porque A.2 es de Aleks con FTMO. Sigue sin parar si solo rompen tests que fijan el importe de la comisión o un saldo que la incluye: cada uno se cambia con su porqué. PARADA si rompe cualquier otra cosa.
> D7. El paso 8 (ADR-0081 §4). Manda el lector con la regla de MARGEN-PENDIENTE.md §0.d. Si da M1 «no», M2 «no», M3 «no» y M4 «no concluyente», con la tasa de margen de la buy stop en 0, eso desmiente lo que ADR-0081 §4 da por hecho: que una pendiente stop reserva margen mientras vive y se comprueba al colocarla. Por eso ADR-0090 ENMIENDA ADR-0081 §4, con recuadro en §4 y fila en el índice; una NOTA no basta.
>   (a) El límite del lote del bot (ADR-0081 D1-D2) no cambia: el tope por margen lo pone el bot, y con M4 sin medir sigue abierto que MT5 compruebe el margen al llenar.
>   (b) El bróker simulado no cambia en esta rama. Su reserva de margen por pendiente y su comprobación al colocar quedan como SUPUESTO CONSERVADOR declarado, porque en construcción no han tenido efecto medido (lo que dé f). Si f encuentra algún rechazo por margen_libre, PARADA. Di también si, con una sola orden viva a la vez, la reserva puede cambiar el lote de alguna orden, con fichero:línea.
>   (c) Línea nueva de Technical Debt, con nombre: el bróker simulado reserva margen por pendiente stop y comprueba al colocar, la prueba de FTMO no (tasa 0), sin efecto medido; se decide antes de R6a.6, que no la porta al EA sin esa decisión.
>   (d) Para R6a.7: la tasa de margen de las pendientes stop es configuración del símbolo en la prueba, y la cuenta Swing real no la garantiza; el pre-vuelo la lee (SymbolInfoMarginRate) y la compara con lo esperado.
>   M4 queda declarado sin medir en ADR-0090 y no abre ambigüedad. (c) y (d) van entre las líneas preparadas para el cierre.
> D8. El nivel exacto (ADR-0057 §2). Sigue PROVISIONAL. ADR-0090 dice que las tres ejecuciones dieron tres patrones distintos, que este script no puede decidirlo porque no registra la cotización del servidor en el instante de la comprobación, y que no hay más ejecuciones previstas. Recuadros en ADR-0057 §2 y en ADR-0071 §4. El simulador no cambia. Línea preparada: lo observa el journal de R6a cuando el EA coloque órdenes en demo.
> D9. Ficha y swaps (paso 1). Compara la ficha de la 2 y la 3 con los valores CONFIRMED del registro y del perfil: los cinco de A-27, stops level y freeze level, volumen mínimo, máximo y paso, apalancamiento, swaps y modo de margen. Si todo coincide, ADR-0090 lo dice en una tabla. Si algo difiere, PARADA solo para eso (ADR-0071 §6).
> D10. Deslizamiento. deslizamiento_fijo_puntos de knowledge/simulador/llenado.yaml sigue en 0. ADR-0090 registra las observaciones de las tres ejecuciones (la 1, en ADR-0071 §4 y en DEMO-FTMO.md) y dice que no son un modelo: lo mide el grabador de F17 (heredado 10).
> D11. La hora de la 3. Se declara en el informe, en ADR-0090 y en DEMO-FTMO.md («Cuándo: tres veces»), comprobado con zoneinfo: 20:35 del servidor, 18:35 UTC, 19:35 de España y 13:35 de Lima, fuera de la franja; Nueva York abierto y Londres ya cerrado. La hora puede afectar al spread, al deslizamiento y al llenado de los pasos 6 y 7, y no afecta al desfase, a la comisión ni a la ficha. DEMO-FTMO.md recoge además las ejecuciones 2 y 3 y la prueba del 2026-10-29.
> D12. Lo que se queda vivo: M (ninguna ejecución la mide; MARGEN-PENDIENTE, punto 5 de la respuesta) y el grabador de spread y ticks (F17).
>
> PARADA CONDICIONAL: entrega la fase 0 en el informe y commitéala (skill fase-cero). Si todo lo medido cuadra con D1-D12, sigue con la fase 1 sin esperarme y lo dices en una línea. Lo que contradiga una decisión, o un caso que una decisión manda a PARADA, se para, y sigue lo que no dependa de ello. Nunca cierres.
>
> FASE 1, en este orden y un commit por punto:
> 1) Los dos manifiestos.
> 2) ADR-0090, con los recuadros de ADR-0081 §4, ADR-0071 §3 y §4, ADR-0057 §2 y ADR-0027 §4 y las filas del índice. El bloque ids-inexistentes sale de este encargo y del informe en este mismo commit.
> 3) La spec: A-28 DECIDIDA, broker_offset_base y broker_dst, las frases de g), Known Ambiguities, test_kit, spec_version, spec manifest --escribir y spec docs --escribir, y el yaml de cierres. Trailer Fuente: ADR-0090.
> 4) La comisión en el perfil y sus tests. Trailer Fuente: ADR-0090.
> 5) docs/runbooks/DEMO-FTMO.md.
> En cada commit: estadiar, uv run botsito state check, make check > make-check.log 2>&1, leer el log (exit 0, ningún failed y la línea SELLO) y commit; antes, ruff format, ruff check y mypy sobre lo tocado. Si la guardia o el clasificador niegan algo legítimo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> TESTS QUE ROMPEN A PROPÓSITO, cada uno con su salida contra main pegada (comparar-con-main): la comisión a 2,50 por lado (falla con 5); A-28 entre las DECIDIDAS de test_kit (falla en main); y, si ningún test comprueba que el sufijo del dataset_id de un manifiesto de la demo son los 8 primeros hex de su sha256, uno nuevo que falle con un sufijo que no case.
>
> CI: la rama no toca hooks, rutas ni plataforma, así que no hay fix/. Si acabaras tocando .claude/, hooks o src/, empuja fix/<rama> y pega el número del run.
>
> INFORME, en docs/validation/DEMO-EJECUCIONES-2-3.md: el encargo punto por punto; la fase 0; la tabla medida → decisión; lo que no pudiste medir; las líneas del cierre preparadas; la previsión de PROJECT_STATE; y la fila de ERRORES-RECURRENTES preparada, con estos errores del consultor:
> - (importa) La orden de cierre de F38n escribió en la Next Action y en la hoja de ruta «los tres CSV sin congelar», cuando la 1 está congelada desde el 2026-10-09. Lección: antes de dar por pendiente un paso, buscar su artefacto (aquí, data/manifests/demo_ftmo/).
> - (menor) El resumen del consultor del 2026-11-06 dio «deslizamiento 0», y la ejecución 2 trae 2,0 puntos en contra al abrir a mercado. Lección: una cifra de un CSV se lee por ejecución, no se resume.
> - (importa) El plan del consultor era una NOTA en ADR-0081 §4, cuando la medida desmiente lo que §4 da por hecho y lo que modela el bróker simulado; lo cazó su auditor antes de entregar el encargo. Lección: antes de decidir entre nota y enmienda, leer qué da por hecho el ADR y qué hace el código.
> Pasa el revisor (subagente revisor, opus) con estos alcances: reglas de la casa; encargo; inmutabilidad de los manifiestos; A-28 en sus cinco sitios; las frases que quedan falsas por A-28 y por la comisión (grep); que nada de src/ cambie; y que no salga ninguna fecha reservada. Pega su informe al final.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA (2026-11-06)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/demo-ejecuciones-2-3 (2026-11-06). Cópiala tal cual en el informe (skill fase-cero) y aplícala punto por punto.
>
> 0. Fin de línea de la ejecución 1: (a), como lo hiciste. El manifiesto no se toca, ADR-0090 lo corrige y DEMO-EJECUCION-1.md y EA-CONEXION.md §0.c llevan su recuadro. Porqué: un informe cerrado que afirma algo falso se corrige con un recuadro, y el sha256 del manifiesto sigue fijando los bytes buenos.
>
> 1. Swaps: (a), el valor del perfil no cambia. Porqué: un swap cambia cada día y no se fija con una lectura (ADR-0071 §5). Añadidos:
>    - ADR-0090 registra las tres lecturas con su fecha y sustituye el «pendiente de la decisión 1» por esta decisión.
>    - La descripción de firma_swap_largo_puntos y de firma_swap_corto_puntos dice que su valor es el de la API del 2026-09-25, que cambia con la fecha (las tres lecturas de la demo, en ADR-0090) y que no se renueva porque no decide nada. Trailer Fuente: ADR-0090.
>    - Verifica, y escribe en ADR-0090 con fichero:línea, que ninguna operación del bot puede seguir abierta a la medianoche del servidor (la ventana de la operativa y el cierre un minuto antes del fin de la H4). Si alguna puede, PARADA solo para esto.
>    - Que no se reabre A-27 lo dejas dicho en una línea, citando sus cinco parámetros.
>
> 2. La rejilla H4 real: (a), una entrada nueva R6a.8 «La rejilla H4 real en el journal», que depende de R6a.1 y de la que dependen R6a.7 y F33. Porqué: R6a.1 se cerró con su «Hecho cuando» cumplido. Va como línea preparada para el cierre. ADR-0090 y la descripción de anclaje_h4 citan R6a.8 por su nombre en el commit del punto 4, y test_hoja_de_ruta tiene que pasar con la línea aplicada sobre la copia.
>
> 3. La regresión del 7 de agosto: (a). La regresión declara COMISION_DE_LA_REGRESION = 5, igual que VOLUMEN_MAX_DE_LA_REGRESION y por el mismo camino (dataclasses.replace), con un comentario de una línea: es la tarifa supuesta hasta ADR-0090, y se conserva para que el corte en el tick del pico siga teniendo un caso real que lo pruebe. Test nuevo en el mismo fichero: con el perfil real (2,50 por lado), la cuenta de ese día queda EN_CURSO y su peor equidad es 95.515,78. Porqué: no se pierde la regresión del corte y la consecuencia de la medida queda escrita en un test.
>    - El informe y ADR-0090 dicen, en una línea, que con 5 USD por lado el simulador suspendía cuentas que con la tarifa medida no se suspenden. Las corridas anteriores a esta rama eran pesimistas en las suspensiones, y la re-corrida que cuenta (ADR-0070 §3) es la primera con la tarifa medida.
>    - Punto 4 de la fase 1: la comisión a 2,50 en el perfil, las dos regresiones, R6a.8 en ADR-0090 y anclaje_h4, en un commit con Fuente: ADR-0090. Los dos tests que rompen a propósito (2,50 frente a 5 en test_perfil_cuenta y EN_CURSO frente a SUSPENDIDA), con su salida contra main pegada (comparar-con-main).
>
> 4. Fila de ERRORES-RECURRENTES preparada: añade, del consultor, «(menor) D9 metió los swaps entre los datos que tenían que coincidir, cuando ADR-0071 §5 ya dice que cambian con la fecha, y costó una PARADA. Lección: antes de poner un valor en una comparación de igualdad, mirar si el repo lo da por variable».
>
> 5. Lo que sigue: el punto 4, make check en cada commit, el revisor (opus, con los alcances del encargo, más las dos regresiones y que la comisión no aparezca con 5 en ningún documento vivo salvo la constante declarada) y la entrega con entregar-rama, que incluye las líneas del cierre aplicadas sobre una copia y la previsión de PROJECT_STATE con wc -c. Al terminar, quita los clones C:\cm\m y C:\cm\r con git worktree remove y dilo en el informe. Si de aquí sale otra PARADA, es solo para lo suyo: sigue con lo demás. Nunca cierres.
>
> Rama lista para revisión, NO cerrada.

## Orden de cierre del consultor (2026-11-06)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/demo-ejecuciones-2-3 (consultor, 2026-11-06). Sigue la skill cerrar-rama y docs/runbooks/RITUAL.md con todas sus puertas. Antes de nada, confirma que el informe que vas a cerrar es el de bf87245 (86.671 bytes y la sección «## 3. El revisor»).
>
> Tag: stable/F38p-demo-ejecuciones-2-3 (comprueba que no existe ni en local ni en origin).
> Mensaje del merge: «merge: trabajo/demo-ejecuciones-2-3, las ejecuciones 2 y 3 de la demo congeladas, A-28 DECIDIDA (ADR-0090: 120 y us), la comisión a 2,50 por lado y ADR-0081 §4 enmendado».
>
> Hallazgos del consultor que el revisor no vio: ninguno. La fila de ERRORES-RECURRENTES es la de §1.4 del informe, con la columna del revisor rellena con su resumen de §3 (1 bloquea, 2 importa, 1 menor, y qué se hizo con cada uno, §3.1). Lección para el revisor: ninguna nueva.
>
> Commit del contrato (chore(cierre)), en la rama: todo lo de RITUAL más las líneas de §0.h del informe, con la R6a.3 (b1) y la deuda de los docstrings (b2) de §3.1, tal como se probaron en §3.2. Con estas decisiones:
> 1. Next Action:
>    - A sale HECHA a HISTORIA, con su texto literal.
>    - Entra la A nueva de §0.h: el panel del límite diario, más lo «Opcional» de las noticias.
>    - M se queda igual.
>    - F se reescribe así: «F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o): S-2, el tope del trader se reinicia al abrir la primera sesión del día siguiente (ADR-0089); S-4, en M15 la vela sin cuerpo no corta la racha y su mecha cuenta (ADR-0085 §2); A-44 RESUELTA. S-22 y S-19 a la sesión 7 (§d de ACTIVAR-SESION-06-MOTOR.md). Siguiente: H (fase 0: el diagnóstico de H del scratchpad de Claude Code, fuera del repo, medido con la comisión de 5: se vuelve a medir sobre el main de F38p), R y la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3); después, la preparación de la sesión 7». Todo lo que va detrás de «la preparación de la sesión 7» se copia literal de la F actual, sin tocarlo.
> 2. Heredados 10 y 27: como en §0.h.
> 3. Technical Debt:
>    - Sale la del CRLF, por (a).
>    - Entran la de la reserva de margen del bróker simulado (D7(c)) y la de los docstrings de los dos guiones (b2).
>    - NO entra la del fin_de_linea: LF del manifiesto de la ejecución 1: no le queda nada que hacer, y la verdad vive en ADR-0090 y en los recuadros de DEMO-EJECUCION-1.md y EA-CONEXION.md.
>    - Tampoco entra deuda por el swap cobrado a medianoche de huso_corte: vive en ADR-0090 §6 y no tiene efecto mientras ninguna operación pase la noche.
> 4. Hoja de ruta, como en §0.h y §3.1:
>    - A.1 pasa a HECHA.
>    - Entran A.5 y R6a.8.
>    - Cambian R6a.3, R6a.6, R6a.7 y F:F17.
>    - En «Fechas fijas» salen las dos líneas ya pasadas («La ejecución 2, hecha el 2026-10-29…» y «La semana del 26 al 30 de octubre…») y entra la del vencimiento de la prueba hacia el 12-nov, con su «sin comprobar».
>    - test_hoja_de_ruta y test_project_state en verde, y PROJECT_STATE por debajo de 23.000 bytes.
>
> Commit de estado en main, después del tag: solo Current Branch (main), Current Feature, Stable Main State y Last Stable Commit; ni la Next Action, ni Change Log, ni Completed Features. Current Feature: «Ninguna rama abierta. trabajo/demo-ejecuciones-2-3 cerrada en main el <fecha del cierre> (stable/F38p-demo-ejecuciones-2-3): las ejecuciones 2 y 3 de la demo congeladas; A-28 DECIDIDA (ADR-0090: 120 y us); la comisión del perfil a 2,50 por lado; ADR-0081 §4 enmendado.»
>
> make check sellado, y push atómico (git push --atomic origin main stable/F38p-demo-ejecuciones-2-3); Aleks confirma la regla ask. La CI que cuenta es la del commit docs(state) de main, y tiene que estar en verde antes de borrar la rama local. No hay fix/ que borrar.
>
> Informe final: sha de main, sha del merge, tag, número del run de la CI de main y su resultado, ramas que quedan (local y origin) y tamaño de PROJECT_STATE.md con wc -c.
