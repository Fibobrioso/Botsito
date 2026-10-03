# Encargo · trabajo/fuentes-ftmo

Dado por Aleks (consultor) el 2026-10-03. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/fuentes-ftmo, desde main (7dcbb6a, tag stable/F36q-cierres-de-mercado). Solo documentación y knowledge: no cambia motor ni cifras.
>
> 1. P0 de docs/validation/CIERRES-DE-MERCADO.md: guarda como fuente escrita la respuesta literal de soporte de FTMO al ticket VDW-DPMWR-965, recibida el 2026-09-29 a las 14:00:47 UTC desde support@ftmo.com, en respuesta al correo de Aleks del 2026-09-28. Va en el sitio donde el repo guarda las fuentes escritas de FTMO (mira cómo cita FTMO-REGLAS.md sus fuentes y sigue ese patrón), sin la firma ni las imágenes. Texto literal:
>
> «Dear Client,
>
> Thank you for reaching out to us.
>
> I would like to inform you that FTMO Account Swing allows trading during news releases and holding positions overnight or over the weekend. However, **gap trading is not permitted** when major global news, macroeconomic events, or corporate reports or earnings are scheduled and may affect the relevant market, or within two hours before a relevant market closes for at least two hours.
>
> **Commissions are charged differently depending on the platform: on MT4, they are deducted instantly, while on MT5, cTrader, and TradingView, 50% is charged at order opening and the remaining 50% at closing.**
>
> For more information, please visit this page: <https://ftmo.com/en/symbols/>
>
> If you have any other concerns, feel free to contact us again.»
>
>    Y una nota: el correo original preguntaba tres cosas (noticias y gap trading, tamaño de posición y comisión). La del tamaño de posición («substantially larger position sizes» con lote variable según el stop) NO se contestó. Aleks reenvió el 2026-10-03, en el mismo ticket, diez preguntas: mensajes al servidor (P1–P4), gap trading (P1–P3 de CIERRES-DE-MERCADO §0.6) y el tamaño de posición. Respuesta pendiente.
>    Cambia las citas que hoy dicen «traslado de Aleks» del ticket para que apunten a la fuente literal.
>
> 2. Technical Debt: la línea «PENDIENTE DE FTMO: EL BOT … HORAS PREVIAS…» quedó a medias tras F36q. Reescríbela para que diga solo lo que sigue abierto (lo que pregunta A-55 y la respuesta pendiente del ticket), o muévela a HISTORIA si ya está cubierta por A-55 y la línea N. Añade una línea sobre el tamaño de posición sin respuesta, si no hay ninguna que lo cubra.
>
> 3. Las ambigüedades A-54 (mensajes al servidor) y A-55 (gap trading) dicen que sus preguntas a soporte están enviadas el 2026-10-03, en el ticket VDW-DPMWR-965. spec docs --escribir en el mismo commit.
>
> PROJECT_STATE por debajo de 23.000 bytes. make check sellado, revisor con su informe pegado.
> «Rama lista para revisión, NO cerrada.»
