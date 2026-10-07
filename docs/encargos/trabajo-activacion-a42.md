# Encargo · trabajo/activacion-a42

Dado por Aleks (consultor) el 2026-10-06. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva trabajo/activacion-a42, desde main en e97af27 (state commit tras stable/F37c-reloj-invierno, merge 49c3098). Verifica con git que main y origin/main están ahí antes de abrir. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-activacion-a42.md, su contrato.yaml y el archivo de PROJECT_STATE en HISTORIA.
>
> Objetivo: activar A-42 con la hipótesis H2b de RELOJ-INVIERNO.md. Las dos sesiones son las velas H4 de la rejilla de anclaje_h4 (17:00 America/New_York) que empiezan en ancla + 8 h y ancla + 12 h. En el gráfico del trader (Europe/Madrid) caen 07–11 y 11–15, salvo en las semanas en que Europa y EE. UU. no coinciden en el horario de verano. El bot fija su ventana en INSTANTES UTC calculados con zoneinfo, nunca con un desfase fijo (RELOJ-INVIERNO.md §9).
>
> Qué NO cambia: el reloj del día de riesgo (huso_operativa, ADR-0063); ninguna regla de entrada, stop, objetivo ni gestión; A-11 y el punto U. Febrero, marzo y julio no se tocan ni se listan. Marzo sigue sin abrir: si A-42 RESUELTA cumple la condición de la PARADA B0 de ENTRADA-MARZO.md, el informe lo dice y nada más; la entrada de marzo es otra rama.
>
> Decisión del consultor (2026-10-06), que entra al encargo con su porqué:
> - H2b y no H2a. En S-7 (SESION-04-EXTRACCION.md §3.1) el trader dijo que desde el 25 de octubre la primera sesión es «de 6 a 10» en su gráfico, y H2a no prevé ningún cambio (RELOJ-INVIERNO.md §7). Por escrito, el 2026-10-06, confirmó la vuelta a las 7 desde el lunes 2 de noviembre («1-B»), que es lo que H2b predecía y no había dicho.
> - El trader escribe desde dos números. Aleks confirmó el 2026-10-06 que los dos son suyos. Ningún nombre ni número entra al repo (es público); en el registro basta con «el trader, desde sus dos números, confirmado por Aleks».
>
> Material que entra, en corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/ (WhatsApp, 2026-10-06, hora de Lima). Renómbralos así antes de inventariarlos:
> - a.png → mensaje-whatsapp-2026-10-06-1344-graficos-h4-y-utc2.png
> - b.jpeg → mensaje-whatsapp-2026-10-06-1344-grafico-h4-oct-2024.jpeg
> - c.jpeg → mensaje-whatsapp-2026-10-06-1344-grafico-h4-nov-2024.jpeg
> - d.png → mensaje-whatsapp-2026-10-06-1345-se-opera-a-las-6-y-stop.png
> - e.png → mensaje-whatsapp-2026-10-06-1536-vela-3-nov-y-mitigacion.png
> - «Captura de pantalla 2026-10-06 154450.png» → mensaje-whatsapp-2026-10-06-1544-respuestas-1b-2c.png
> - «Captura de pantalla 2026-10-06 154630.png» → mensaje-whatsapp-2026-10-06-0953-reloj-grafico.png
> - «Captura de pantalla 2026-10-06 154806.png» → mensaje-whatsapp-2026-10-06-0959-reloj-grafico.png
> Literales, leídos por el consultor en las capturas (verifícalos tú contra cada imagen):
> - 09:53 «según la configuración de la plataforma etc+2 madrid»
> - 09:59 «xd» «sep» «seria cuestion que se adapte a lo que bote la plataforma»
> - 13:44 «1- Si esta configurado UTC+2», con dos capturas de su gráfico de 4 horas
> - 13:45 «si es por cuestion horaria se oepra a las 6»
> - 13:46 «el stop conforme se vaya validando los puntos breaker se va acutalziando»
> - 15:36 «la del 3 de noviembre empeiza las 23:00 pm» y «en cuanto el stop tiene que haber mitigacion apenas toque»
> - 15:44, respuesta al mensaje de las 15:38 (pregunta y opciones visibles en la misma captura): «1-B)» y «2-c) la orden se pone y se ejecuta cuando ocurre la mitiga ion» «Cion» «Del breakef» «Breaker point»
> Los mensajes sobre el stop (13:46, la segunda frase de las 15:36 y «2-c») NO se registran contra A-11 ni contra ningún parámetro, y no se interpretan: quedan en el corpus con su captura y el informe los cita como contexto para U.
>
> Fase 0, inventario sin tocar nada. Entrega antes de escribir código:
> a. Lista la carpeta Mensajes del trader: las 8 capturas, con nombre y tamaño. Si falta alguna o alguna no casa con su literal, PARA.
> b. Los dos pendientes que salieron de PROJECT_STATE al cerrar trabajo/reloj-invierno, con su texto literal tal como está en el registro de cierre de HISTORIA: (1) rehacer con --solo-filtrar --video las filtradas de v7–v10 y compararlas con FILTRADAS-ESCENARIO-B.md; (2) añadir ev-v10-010438-024f76b8 a la evidencia de A-42, partiendo de la medida de VENTANA-EV-V9.md. Haz el (1) aquí, con su resultado; si sale cualquier diferencia, PARA.
> c. Todo lo que depende del reloj de las sesiones: reloj_sesiones (valores admitidos y dónde se lee), huso_grafico, anclaje_h4, ventana_inicio, ventana_fin, el cierre un minuto antes de la vela H4, RN que los lean, código del motor y del simulador, tests, ADR-0039, ADR-0059, ADR-0063, R0 de ABRIL-Y-LA-CAJA, MIRAR-EL-MATERIAL, el comentario de A-42 y las dos líneas de Technical Debt sobre el «UTC+2 FIJO».
> d. Repite el guion de M4 (anexos/RELOJ-INVIERNO/rejilla_h4.py) sobre las semanas 2024-10-27/31 y 2024-11-03/07 y compáralo con las etiquetas del eje de b y c (§12 de RELOJ-INVIERNO.md).
> e. Tu propuesta de cómo meter H2b: valor nuevo de reloj_sesiones o cambio de los existentes, qué pasa con ventana_inicio y ventana_fin, qué ADR (nuevo, que deja superada la lectura provisional de ADR-0059), cómo se registra el feedback (carpeta de sesión, procedencia trader_escrito, objetivo A-42 con RESOLVE_UNKNOWN y los registros de parámetro que exija feedback apply) y qué tests rompen la guardia.
> f. Declaración en HOLDOUT-EXPOSICIONES.md de lo que se lea, el mismo día.
> PARADA: espera mi respuesta a la fase 0 antes de cambiar nada fuera del informe.
>
> Fase 1 (después de mi respuesta, por este orden y en commits separados, cada uno con su Fuente:):
> 1. Corpus: renombrado, fuentes.yaml (papel, fecha de entrega y cautelas: dos números del trader, sin nombres) y uv run botsito corpus inventory.
> 2. ADR nuevo con H2b, ANTES de citarlo en ningún sitio (knowledge/feedback/README.md, punto 6).
> 3. Registros de feedback, literales, con la ruta de la captura en notas, recibido_el 2026-10-06 y procedencia trader_escrito.
> 4. Spec: A-42 RESUELTA (los cuatro sitios, el test y uv run botsito spec docs --escribir, según CLAUDE.md, «Ambiguedades»), con ev-v10-010438-024f76b8 en su evidencia; huso_grafico a Europe/Madrid; la descripción de anclaje_h4 (RELOJ-INVIERNO.md §8.5).
> 5. Motor: la ventana en instantes UTC desde la rejilla, con zoneinfo. Tests que rompen a propósito, con fechas de calendario y sin leer datos: 2026-10-23 y 2026-10-26 (05:00 UTC), 2026-11-02 (06:00 UTC), un día de enero de 2026 (06:00 UTC), la semana 2025-03-10/14 (EE. UU. ya cambió y Europa no) y las dos semanas de 2024 de las capturas. Un test que falle si alguna hora de sesión sale de un desfase fijo.
> 6. Correcciones con recuadro: ADR-0039, ADR-0059, R0 de ABRIL-Y-LA-CAJA, MIRAR-EL-MATERIAL y el comentario de A-42. En Technical Debt, la deuda del «UTC+2 FIJO» queda pagada y se borra; lo que siga vivo de la línea de Oanda y Dukascopy se queda.
> La Next Action no se toca en esta rama: E sale en el commit del contrato, en el cierre.
>
> zoneinfo depende de la plataforma (tzdata en Windows): push de fix/activacion-a42 y CI de Linux con su número de run. make check y uv run botsito state check en verde. Informe en docs/validation/ACTIVACION-A42.md. Revisor con su informe pegado al final; que compruebe aparte que ninguna hora de sesión sale de un desfase fijo, que los tests de las semanas del cambio fallan con H2a y con H1, que no entró al repo ningún nombre ni número del trader y que no se leyó nada de febrero, marzo ni julio.
>
> Rama lista para revisión, NO cerrada.
