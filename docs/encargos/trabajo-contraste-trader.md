# Encargo · trabajo/contraste-trader

Dado por Aleks (consultor) el 2026-11-25, en un solo mensaje con el encargo y su añadido (A1-A5),
antes de abrir la rama. Copiado tal cual; el añadido va al final con el título que él pide, y su
A5, que llegó en el mismo mensaje tras A4, va dentro de él.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> ENCARGO DEL CONSULTOR (2026-11-25) · rama `trabajo/contraste-trader` · tag al cerrar: `stable/F39o-contraste-trader` (verifica con `abrir-rama`, contra origin, que el último tag es F39n)
>
> Antes de nada, revisa /model (Opus 5.5, alto).
>
> ## 0. Base y apertura
>
> - Base: `main` en `6c113d16` (el commit de estado del cierre de F39n; el merge `42fdb0b5` lleva el tag `stable/F39n-diagnostico-premisa`; CI de main 45670800735 en verde según ese cierre), sin ninguna otra rama. Verifícalo todo con la skill `abrir-rama`; si algo no cuadra, PARA y dilo.
> - Abre con `/abrir-rama trabajo/contraste-trader`: encargo copiado tal cual en `docs/encargos/trabajo-contraste-trader.md`, `contrato.yaml` y el Archivo de PROJECT_STATE en HISTORIA.
> - Contrato: tramo R4 (R4.7). Lista blanca, con lo protegido mandando (cada ruta de aquí sale además de `rutas_protegidas`): este encargo, `contrato.yaml`, `docs/validation/CONTRASTE-TRADER.md`, `docs/validation/HOLDOUT-EXPOSICIONES.md`, `knowledge/corpus/fuentes.yaml`, `knowledge/corpus/manifest.yaml` y `docs/adr/0100-la-premisa-se-mide-con-costes.md` (solo para el recuadro de D6). El resto de `knowledge/corpus/`, `knowledge/feedback/`, `knowledge/spec/`, `knowledge/cases/` y los demás ADR, protegidos. Ningún ADR nuevo: el bloque ids-inexistentes no declara ninguno.
> - Lecciones que aplican: la fila de HOLDOUT-EXPOSICIONES del día va ANTES del primer `make check` del día (y otra si pasas la medianoche); toda frase «la herramienta X da Y» se mide antes de escribirla; lo que escriba se ensaya antes en un clon desechable (CLAUDE.md, «Ensayos aislados»); el recuadro del ADR va en un commit propio de la rama, nunca en el `chore(cierre)`.
>
> ## 1. Objetivo
>
> Que entre al repo el contraste con el trader que ADR-0099 §6 manda hacer en su propia rama: lo que dijo el trader el 2026-11-23 por escrito y por audio, lo que se le enseñó durante el intercambio y su registro, para que lo lea el ADR de Aleks de ADR-0099 §7 (como tarde, la semana de los ingenieros, hacia el 2026-12-03). Entra también la petición escrita de los meses del backtest con costes, que ADR-0100 §2 pone como condición («los que Aleks le pidió por escrito, o los que él declare por escrito antes de empezar»). Tiene que quedar lista para revisión antes del 2026-12-01.
>
> ## 2. Qué NO cambia
>
> Spec (`parametros.yaml`, `strategy_spec.yaml`, `ambiguedades.yaml`: ninguna ambigüedad cambia de estado), `knowledge/cases/` (`meses_reservados.yaml` incluido), `knowledge/evidence/`, `knowledge/feedback/` (ningún registro: D1), `libros.yaml`, `tramos_no_citables.yaml`, `knowledge/corpus/transcripciones/`, motor, `src/`, `scripts/`, `.claude/`, los ADR salvo el recuadro de D6, `docs/plan/` (la hoja de ruta va en el cierre) y `PROJECT_STATE.md` (salvo el Archivo de la apertura). Ninguna corrida del arnés. Si algo pidiera tocar `src/`, `scripts/`, `.claude/` o `knowledge/cases/`, PARA: no es de esta rama.
>
> ## 3. El material
>
> Aleks lo copia antes de que empieces a `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/`, con el patrón de nombre de la carpeta. Las capturas no las abres (ADR-0038; la guardia lo impide): sus literales los transcribe el consultor en la respuesta a la PARADA.
>
> - (a) La captura del mensaje de Aleks con las cinco preguntas de la premisa del 2026-11-23 (no están en el repo y el informe las copia) y la de las respuestas escritas del trader (`mensaje-whatsapp-2026-11-23-0956-operativa-real.png`, y las que haya con el mismo patrón).
> - (b) Los audios del trader del 2026-11-23 (de las 09:59 a las 10:13, hora de Lima), hoy en `C:\Users\USER\Desktop\audios-trader-2026-11-23\`: siete y un duplicado, que transcribiste ese día con el ASR del corpus fuera de cualquier rama. Entran con el nombre `audio-whatsapp-2026-11-23-<HHMM>-<tema>.<ext>`; el duplicado no entra y el informe lo nombra por su sha256. Si la guardia te niega copiarlos, se lo dices a Aleks y los copia él.
> - (c) Lo que se le enseñó: la foto a la que el trader respondió mencionando «las 191 operaciones». No la tienes ni la buscas: la describe Aleks en la PARADA. 191 es el número de operaciones llenadas de la corrida (3), las del techo de −0,239 R (ADR-0099 §8; RECORRIDA-CONSTRUCCION-3.md §4), y ADR-0098 §3 C pedía el contraste «sin enseñarle ninguna cifra de esta medida».
> - (d) La petición escrita de los meses del backtest con costes: la captura del mensaje de Aleks que pide «ENERO 2024» con la configuración (comisión de 5 USD de ida y vuelta, spread de 0,2, apalancamiento 1:30 y deslizamiento apagado) y, si ya existe, la declaración escrita del trader del segundo mes. Solo capturas sin ningún resultado del backtest: si una trae alguno, no entra. Si aún no hay declaración del segundo mes, el informe lo dice y la rama no la espera.
>
> ## 4. Fase 0 (inventario; no escribe en el repo salvo la apertura y la fila de HOLDOUT)
>
> - 0.1 **La fila de HOLDOUT del día**, antes del primer `make check`, que incluye, escrita tarde y nombrada como desviación de ADR-0021 §4, una declaración del 2026-11-23: tu transcripción con ASR de los audios, hecha fuera de rama y sin cuarentena (qué ficheros, quién leyó ese texto y si nombra días o meses fuera de construcción, solo por recuento), y lo que vieron ese día Aleks y el consultor (las respuestas escritas y el resumen de los audios; ADR-0099 §8 dice que las vieron y ninguna fila lo declara). Comprueba antes que ninguna fila lo recoge (las del 2026-11-23 y del 2026-11-24, de `trabajo/puente-techo` y `trabajo/diagnostico-premisa`, dicen que no leyeron esos mensajes ni audios). Precedente de fila escrita tarde: la de `trabajo/sesion-08` del 2026-11-21 que cubre el 2026-11-20.
> - 0.2 **Localiza el material**: por fichero, nombre, tamaño y sha256; en los audios, también formato y duración, si se pueden medir sin que la guardia lo niegue (no la rodees: si la niega, dilo). Las capturas solo se cuentan y se hashean. Y comprueba que el vídeo de mapeo del trader y el backtest de diciembre de 2025 siguen fuera de `corpus/`.
> - 0.3 **El inventario, medido en un clon desechable**: si `uv run botsito corpus inventory` acepta los audios y las capturas nuevas en esa subcarpeta, y que el diff de `knowledge/corpus/manifest.yaml` son solo las entradas nuevas (el comando recorre el corpus entero: si cambia otra entrada, PARA).
> - 0.4 **Lo que nombra cada audio**: sobre tu transcripción del 2026-11-23, por audio, si nombra días o meses fuera de construcción o resultados de operaciones. Usa `scripts/barrido_dias.py` si su formato de entrada lo admite (pide una filtrada con líneas `[mm:ss] texto`); si no, el recuento a mano. En el informe y en la PARADA, solo recuentos; ninguna fecha reservada ni resultado.
> - 0.5 **El mapa de lo dicho**, una fila por audio y otra por captura escrita (estas, cuando el consultor transcriba): tema, si encaja con algún objetivo de `fb-` del esquema (`knowledge/feedback/README.md`) y si responde a algo pendiente: A-35 (Technical Debt de PROJECT_STATE: «va al trader por WhatsApp con el esquema del PDF y entra por «Mensajes del trader»»), A-43, A-48, A-58 y lo del WhatsApp del 2026-11-21 (A-35, A-43 y S-3; ACTIVAR-SESION-08.md:368). Lo que espera el consultor, por verificar contra la transcripción: (a) que el bot traza la caja «en una sola vela» en vez de por el esquema 1 o 2: material para A-48 y S-3 y para preparar la sesión siguiente (R4.6); (b) la regla: objetivo de 1:3 sobre la distancia 0-1 y stop protegido en el 0,8 (los parámetros de hoy: `objetivo_rr`, `base_calculo_objetivo` y `stop_fraccion_caja`; di literal si la voz dice la distancia 0-1 o «el stop», porque ADR-0100 §1 describe su forma de operar como «objetivo a 3 veces el stop»); (c) que el break even «solo cuesta la comisión»: opinión; (d) que operó algunas operaciones en FundedNext, compartidas en el grupo: premisa; (e) la logística de la reunión: nada; (f) «las 191 operaciones»: lo que se le enseñó. Si algún audio o captura es material de un mes que no es de construcción (un gráfico, un día operado), PARA: entraría en `meses_reservados.yaml` el mismo día (MIRAR-EL-MATERIAL.md), y eso no es de esta rama sin respuesta del consultor.
> - 0.6 El auditor `auditor-encargo` al empezar la fase 0, contra este encargo.
>
> ## 5. PARADA (única)
>
> Entrega: lo medido en 0.2, 0.3 y 0.4; la tabla de 0.5; la lista de capturas con su sha256, para que el consultor transcriba sus literales; para cada frase de los audios que el informe vaya a citar, el audio, el minuto y el texto del ASR, para que Aleks la compruebe escuchándola; lo que proponga el auditor; y esta pregunta a Aleks, que copias tal cual con su respuesta: «¿Qué era la foto a la que el trader respondió con "las 191 operaciones"? Qué documento, qué se veía (cifras de R, número de operaciones, porcentajes, meses) y cuándo se la mandaste.» Aleks contesta en la sesión lo suyo (la foto y las frases escuchadas); el consultor, los literales de las capturas y lo que la medida haya dejado abierto.
>
> ## 6. Decisiones dadas por adelantado (se aplican tras la PARADA salvo que la medida las contradiga; si la contradice, esperan a la respuesta)
>
> - D1. **Ningún registro de `fb-` en esta rama.** ADR-0099 §6 los pide «donde toque», y no toca en ninguno: (i) nada se cierra, como en `trabajo/activar-sesion-08`, que no creó ninguno; (ii) la premisa y el coste de FX Replay no tienen objetivo en el esquema, y el feedback no tiene acción de nota (feedback/modelo.py:37-51); (iii) un CONFIRM sobre el objetivo o el stop escondería la diferencia entre la regla dicha y su registro, que es una medición (A-56, ADR-0073 §3) y le toca al ADR de ADR-0099 §7; y (iv) con un audio suelto el validador no comprueba `t1` contra la duración (solo los vídeos del manifiesto la tienen), y el literal saldría de un ASR hecho fuera de rama. Ninguna ambigüedad cambia de estado; la línea de A-35 de Technical Debt sigue, y el informe dice si algo de esto la responde.
> - D2. **Los literales.** Los de las capturas, del consultor, con el sha256 de cada una, como en `fb-2026-10-04-sesion-04-d2e84172`. Los de los audios, del ASR del 2026-11-23, marcados así, solo las frases que Aleks haya comprobado escuchándolas en la PARADA y con el audio y el minuto de cada una. La transcripción no entra al repo (no hay en `main` nada que transcriba un audio suelto, y esta rama no cambia código): queda fuera, nombrada por su sha256, y la falta va a Technical Debt en el cierre.
> - D3. **`fuentes.yaml` amplía la subcarpeta «Mensajes del trader»**, cuya descripción hoy solo habla de capturas escritas: lo que entra y su fecha, que es el contraste de ADR-0099 §6, que por primera vez trae audios, y sus CAUTELAS: ningún nombre ni número del trader entra al repo; las capturas no las abre la sesión (ADR-0038); el trader dice que operó algunas operaciones en FundedNext, compartidas en el grupo: no se piden ni se abren, y si llega un historial, entra SIN ABRIR y un ADR fija antes quién lo lee (ADR-0099 §6, con ADR-0072 como precedente); lo que se le enseñó (c), con lo que diga Aleks.
> - D4. **Las capturas de (d)** entran con los literales del consultor; el informe dice qué meses quedan pedidos o declarados por escrito, cuándo y con qué configuración, sin juzgar si cumplen ADR-0100 §2: eso lo hace la rama de entrada del backtest.
> - D5. **Neutral**: el informe recoge lo dicho y lo enseñado sin leerlo contra la premisa ni contra ninguna cifra; esa lectura es del ADR de ADR-0099 §7.
> - D6. **Un recuadro en ADR-0100 §1**, en un commit propio y con el cuerpo intacto: la frase «su respuesta entra con su `fb-` por su propia rama» se corrige diciendo que esa respuesta no tiene objetivo de `fb-` en el esquema y que entra por `CONTRASTE-TRADER.md`. Ningún otro ADR se toca; si lo que diga Aleks de la foto pidiera corregir otro, espera a la respuesta.
> - D7. **HOLDOUT**: la fila tardía de 0.1; lo que se le enseñó (c), con la respuesta de Aleks, nombrado como posible desviación de ADR-0098 §3 C (la consecuencia la decide el ADR de §7, no esta rama); y lo que lea cada paso, el mismo día.
>
> ## 7. Informe y entrega
>
> - `docs/validation/CONTRASTE-TRADER.md`: qué entra (por fichero, con sha256); las cinco preguntas; la tabla de 0.5; los literales (D2); lo que se le enseñó; las cautelas; lo que va a la preparación de la sesión siguiente (R4.6) y al ADR de C; y las líneas propuestas para el cierre: la F, donde sale «el contraste con el trader (ADR-0099 §6)» de lo pendiente sin que PROJECT_STATE crezca (está en 24.850 bytes de 25.000; da el tamaño resultante), la hoja de ruta (R4.7), Technical Debt (la transcripción de audios sueltos que falta en `main`, D2) y la fila de ERRORES-RECURRENTES preparada con sus cuatro columnas.
> - Esta rama no toca la plataforma: no hace falta `fix/` ni CI de Linux, salvo que el revisor lo pida.
> - El subagente `revisor`, con estos alcances: holdout (ninguna fecha reservada ni resultado en lo commiteado, y las filas de HOLDOUT completas y de su día); cada literal contra su fuente (captura con sha256 o audio con minuto, comprobado por Aleks); `fuentes.yaml` solo amplía y el diff de `manifest.yaml` son solo entradas nuevas; diff vacío en spec, casos, evidencia, feedback, transcripciones, motor, `src/`, `scripts/`, `.claude/` y `docs/plan/`; el recuadro de D6, con el cuerpo del ADR intacto; la neutralidad de D5. Su informe, pegado al final del de la rama.
> - Termina con: «Rama lista para revisión, NO cerrada.»

## Añadido del consultor (2026-11-25)

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> AÑADIDO DEL CONSULTOR al encargo de `trabajo/contraste-trader` (2026-11-25, 16:10, hora de Lima). Cópialo al final de `docs/encargos/trabajo-contraste-trader.md` con el título «Añadido del consultor (2026-11-25)». Si la rama aún no está abierta, entra con la apertura; si ya lo está, en su propio commit. Donde choque con el encargo, manda esto.
>
> ## A1. Las capturas ya transcritas (sustituye a la parte del consultor de la PARADA para estas cuatro)
>
> Aleks se las mandó al consultor, y el consultor se las devolvió con estos nombres para que las guarde tal cual en `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/`. En 0.2 comprueba que el sha256 de cada fichero es exactamente el de abajo; si alguno no coincide, PARA. No las abras: los literales son estos.
>
> 1. `mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png`, sha256 `65a2d71e9e223dd87d4c4edf68d754cb59881e220923b68ff7faca799306f4ca`. Mensaje de Aleks al trader, el lunes 2026-11-23 a la 01:26. Una etiqueta de fecha («lunes») tapa la palabra «Estamos», que se lee en la cita de la captura 2. Literal:
> «Hola, ¿qué tal? Estamos ajustando el bot a las condiciones de una cuenta real (spread, comisión, ejecución) y para eso necesito saber cómo es tu operativa fuera del backtest. Son cinco preguntas cortas, puedes contestar con el número y la letra:
> 1. Esta misma estrategia de EURUSD, ¿la estás operando hoy en una cuenta real o de fondeo? a) Sí, y ya he cobrado retiros b) Sí, todavía sin retiros c) Ahora mismo solo en backtest. Si es a) o b), ¿desde cuándo más o menos? No necesito cifras.
> 2. ¿En qué firma o bróker es, y qué tipo de cuenta?
> 3. En esa cuenta, ¿haces exactamente lo mismo que en tus backtests de FX Replay (mismas sesiones, misma caja, mismo stop y mismo objetivo)? a) Igual b) Cambio algo: ¿qué?
> 4. Los resultados de tus backtests en FX Replay, ¿llevan ya descontados el spread y la comisión? a) Los dos b) Solo el spread c) Ninguno d) No lo sé
> 5. Más adelante, ¿podrías pasarme el historial exportado de esa cuenta (el archivo que da la plataforma, no capturas) de unas semanas? No lo mandes todavía: yo te digo de qué fechas.
> Estas van primero. Las otras que te mandé (las de M15 y las del PDF) pueden esperar a que tengas un rato. ¡Gracias!»
>
> 2. `mensaje-whatsapp-2026-11-23-0956-operativa-real.png`, sha256 `a635f76f3be4c89959822767268a6d8dfc3f115e801e68febe82fad7d9f7ef28`. Respuesta del trader del 2026-11-23 a las 09:56, citando la captura 1. Literal:
> «1-c
> 2-foundnext
> 3-si, todo igual
> 4-no se trabajo con spreads o comisión
> 5-las de fx replays que las envíe, ya no lo puedo enviar porque ya no tengo abiertas esas sesiones de backtest, pero están en el grupo los excels»
>
> 3. `mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png`, sha256 `33fa10d2728bb956951e5e283a9153ad37c4e74ac85fce8a6172fa6a7b139ed7`. Mensaje de Aleks del 2026-11-24 a las 17:18 (el día sale del «Ayer» de la captura 4, tomada el 2026-11-25; Aleks lo confirma en la PARADA). Literal:
> «Te propongo algo que nos va a sacar de dudas a los dos: un backtest de dos meses que no hayas hecho nunca, con los costes reales puestos. Serían junio y noviembre de 2024 (si ya hiciste alguno, dime y elegimos otro de la misma época del año).
> Cómo:
> 1. Operas exactamente igual que siempre: mismas cajas, mismo 0,8, mismo objetivo y mismo break even. No cambies nada por saber que hay costes.
> 2. En FX Replay: datos de OANDA como siempre, spread de 0,2 pips, comisión de 5 USD por lote ida y vuelta (2,5 por lado si te lo pide así) y el lote calculado para arriesgar el 0,5 % en cada operación.
> 3. Grábalo en vídeo con tu voz, como hiciste con julio, todas las sesiones enteras.
> 4. Al terminar cada mes me mandas el CSV completo y los vídeos. No hace falta que calcules nada, los números los saco yo.
> Antes de empezar, confírmame que FX Replay te deja poner el spread y la comisión así, y qué dos meses vas a hacer.»
>
> 4. `mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png`, sha256 `f47da4e8ffb5b787e8a6c4ed81e56a1186577f5fae6f3a0de5ff98502e5d57dc`. Conversación del 2026-11-24 («Ayer»). Literales de lo que se registra:
> - Trader, 17:19, citando la captura 3: «Entonces queda junio y noviembre 2024».
> - Aleks, 17:20: «si bro».
> - Aleks, 18:00: «Una cosa: si todavía no arrancaste el backtest, mejor hazlo de enero y julio de 2024 en vez de junio y noviembre. Si ya empezaste, sigue con esos, no pasa nada. Lo demás igual: spread 0,2, comisión 5 USD por lote, lote al 0,5 %, grabando con tu voz y exportando el libro completo. ¡Gracias!»
> - Trader, 18:01: una nota de voz de 0:14 (entra como audio, A2).
> - Aleks, 18:02: «esos si son definitivos xd».
> La captura trae además mensajes que no se registran ni se interpretan (dos de Aleks a las 18:00, una risa del trader a las 18:01 y un «dale bro» de Aleks a las 18:02), como en el precedente del 2026-10-14 (fuentes.yaml, «Mensajes del trader»).
>
> En las cuatro aparecen el nombre del grupo y los nombres de sus miembros: no entra ninguno al repo, y por eso no están en estos literales.
>
> ## A2. El audio del 2026-11-24
>
> Entra un audio más: la nota de voz del trader del 2026-11-24 a las 18:01 (0:14), que Aleks exporta de WhatsApp a la misma subcarpeta como `audio-whatsapp-2026-11-24-1801-valida-meses.<ext>`. Según Aleks, solo valida los meses. Recibe el mismo trato que los audios de (b): 0.2, 0.4 y 0.5, sin `fb-` (D1). Como no está transcrito, la frase que lo resume la comprueba Aleks escuchándolo en la PARADA.
>
> ## A3. Corrige (d) y D4
>
> - (d) era un error del consultor. La petición escrita de los meses es la secuencia de las capturas 3 y 4: Aleks propone junio y noviembre de 2024, el trader los acepta por escrito y Aleks pide por escrito enero y julio de 2024 si aún no había arrancado. El trader lo valida en el audio de A2 y Aleks los da por definitivos. «Apalancamiento 1:30» y «deslizamiento apagado» no salen en estas capturas: no se escriben como parte de la petición. Si Aleks tiene una captura de la configuración de FX Replay sin ningún resultado, entra con su literal en la respuesta a la PARADA; si no, el informe deja la configuración como la pedida.
> - D4 sigue igual: el informe pone la secuencia con sus horas y sus literales y no juzga si cumple ADR-0100 §2 («uno de cada mitad», «que no haya operado nunca», «por escrito»). Eso lo hace la rama de entrada del backtest. Sí dice, como hecho, que la petición de enero y julio no repite la pregunta de si ya los había hecho, que solo estaba en la captura 3, para junio y noviembre. Si antes de la PARADA llega una respuesta escrita del trader sobre eso, entra como captura más, con su sha256 y con el literal del consultor.
>
> ## A4. Para 0.5
>
> En la tabla, la captura 1 nombra «las de M15 y las del PDF» como preguntas que siguen pendientes (A-35, A-43 y S-3; ACTIVAR-SESION-08.md:368): el informe lo dice, sin cambiar ninguna ambigüedad.
>
> ## A5. Los nombres de las capturas
> Aleks las guardó con el nombre de Windows. En 0.2, comprueba el sha256 de cada una y, solo si coincide, renómbrala (renombrar no abre la imagen):
> - `Captura de pantalla 2026-11-25 160650.png` → `mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png` (65a2d71e…)
> - `Captura de pantalla 2026-11-25 160703.png` → `mensaje-whatsapp-2026-11-23-0956-operativa-real.png` (a635f76f…)
> - `Captura de pantalla 2026-11-25 160945.png` → `mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png` (33fa10d2…)
> - `Captura de pantalla 2026-11-25 161009.png` → `mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png` (f47da4e8…)
> Si la guardia te niega el cambio de nombre, no la rodees: díselo a Aleks y que los renombre él.

## Respuesta del consultor a la PARADA (2026-11-25), copiada tal cual

Llegó en un solo mensaje, con las respuestas de Aleks al final; las respuestas 2, 3 y 4, y la
segunda parte de la 5, llegaron vacías y se copian así.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA de `trabajo/contraste-trader` (2026-11-25, 18:40, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA, junto con las respuestas de Aleks que van al final de este mensaje.
>
> Veredicto: la fase 0 cumple el encargo y el añadido. Acepto las decisiones 0 a 6 con los matices de abajo.
>
> 0. Nombres y audio. Aleks renombra las capturas con tu orden «!». Después vuelve a calcular el sha256 de los cuatro nombres nuevos: tienen que ser los de A1, y si alguno no coincide, PARA. El audio de A2 NO entra: según Aleks (respuesta 5) es solo una risa. Corrección del añadido, error del consultor: A2 y A3 decían que el trader «valida» los meses en ese audio, y no es así. El informe pone la secuencia de las capturas 3 y 4 tal cual: el trader acepta por escrito junio y noviembre de 2024; Aleks pide por escrito enero y julio de 2024 si aún no había arrancado; el trader no contesta por escrito a eso (solo una nota de voz que, según Aleks, es una risa); y Aleks escribe «esos si son definitivos». Sin juzgar ADR-0100 §2 (D4). Sí dice, como hecho, que ninguna captura recoge que el trader no haya operado nunca enero ni julio de 2024.
>
> 1. Inventario: de acuerdo. Lo corres en la rama, compruebas que el diff es el del ensayo (11 entradas nuevas y el bloque resumen) con la raíz SIN cambiar, y después `uv run botsito corpus check --hashes`. Si cambia cualquier otra línea, PARA.
>
> 2. fuentes.yaml: de acuerdo. Amplías el párrafo de «Mensajes del trader» dentro de «Material adicional de su operativa», con la forma de la entrada del 2026-10-14 y las cautelas de D3. No creas una entrada propia.
>
> 3. D1 se mantiene: ningún `fb-`. El informe declara que esto se aparta del paso 4 de knowledge/feedback/README.md:79-82 («si trae una respuesta, registro de feedback»), y por qué: las respuestas no tienen objetivo en el esquema, nada se cierra y un CONFIRM escondería A-56. El README no se toca en esta rama. Precisarlo («si trae una respuesta a un objetivo del esquema») es una línea para «Carril: guardias y deuda» de la hoja de ruta en el cierre.
>
> 4. De acuerdo: el informe nombra Q, V18, A-13 y `ev-v4-012524-0ef85a89` (lo que ya hay de FundedNext) solo por su id, sin tocar ninguno.
>
> 5. De acuerdo: ninguna entrada nueva en la hoja de ruta. El cierre lo apunta en el «Qué es» de R4.7.
>
> 6. De acuerdo. Además, nada de esta rama crece PROJECT_STATE (está a 78 bytes del tope). Van todas a «Carril: guardias y deuda» en el cierre: las dos guardias que negaron medidas legítimas (ffprobe sobre .ogg, el guion de recuento y el cambio de nombre), la transcripción de audios sueltos que falta en `main` (D2) y la precisión del README (punto 3). Al informe solo van las líneas propuestas.
>
> 7. Los literales de los audios. Cuentan las frases que Aleks confirma en la respuesta 3. Donde Aleks corrige, la versión de Aleks es el literal, marcada «[corrige Aleks]». Donde confirma, va el texto del ASR tal cual. Tus cinco lecturas («13» → 1:3; «08»/«080» → 0,8/0,80; «pib» → pip; «funda de nex» → FundedNext; «esquema 12» → esquema 1 y 2) van como nota tuya al pie de la tabla, «lectura de la sesión», salvo las que Aleks diga que oye así. Ninguna frase que Aleks no haya escuchado entra al informe. Si la respuesta 3 está vacía, no entra ningún literal de audio: por cada audio, el fichero, su sha256, el minuto y el tema en una línea neutra, y la falta se dice.
>
> 8. Lo enseñado (D7). F10 y F11 dicen que el trader leyó «las 191 operaciones» y que comenta la fidelidad del bot y unos «Excel recalculados». Según Aleks (respuesta 1), la foto es parte del chat del trader con Gemini, y Aleks no leyó nada de esa parte para no tocar meses reservados. El informe y HOLDOUT lo declaran así: qué se le enseñó al trader queda SIN DETERMINAR; 191 coincide con el número de operaciones llenadas de la corrida (3) (ADR-0099 §8), y ADR-0098 §3 C pedía no enseñarle ninguna cifra de la medida; es una posible desviación que no se puede confirmar ni descartar. Lo mismo con las capturas del bot y los «Excel recalculados» si la respuesta 2 está vacía. No repites ninguna cifra que no sea el 191 que ya dijo él. La consecuencia la decide el ADR de ADR-0099 §7, no esta rama. Ningún ADR se toca por esto (D6 sigue siendo solo el recuadro de ADR-0100 §1).
>
> 9. Pregunta 4, la parte del consultor. Según el registro del consultor, el 2026-11-23 el consultor recibió de Aleks las respuestas escritas y un resumen de los audios en seis puntos hecho por esta sesión de Claude Code, no el texto del ASR. Y una exposición nueva, de hoy: el 2026-11-25 el consultor leyó, en las capturas de esta PARADA, las frases F1 a F14 del ASR. Va a la fila de HOLDOUT de hoy, antes del siguiente `make check`.
>
> 10. Después: aplicas D2 a D7, el recuadro de ADR-0100 §1 en su propio commit, el informe con las líneas propuestas para el cierre y la fila de ERRORES-RECURRENTES (con tu error del ScheduleWakeup y su lección: con un `make check` corriendo no se programa nada que escriba en `.claude/`; y el error del consultor del punto 0, que dio por buena una «validación» sin preguntar qué decía el audio). Luego el revisor con los alcances del encargo. Termina con «Rama lista para revisión, NO cerrada.»
>
> RESPUESTAS DE ALEKS:
> 1. La foto del «191»: «Eso es parte del chat de Gemini donde él metió varias cosas, y para no tocar meses reservados o algo, simplemente no leí NADA.»
> 2. Las capturas del bot y los «Excel recalculados»:
> 3. F1 a F14 escuchadas (cuáles confirmo y qué corrijo; la F5, «sin multiplicarlo» o «multiplicarlo»; cuáles de las cinco lecturas oigo así):
> 4. Lo que leí el día 23:
> 5. El audio de 0:14 «es solo un audio riéndose, no es necesario». Captura 3 y captura de la configuración de FX Replay:
