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

## Segunda orden: respuesta del consultor (2026-10-03)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Respuesta del consultor a trabajo/fuentes-ftmo:
>
> 1. El recuento: el error es del encargo. El correo del 2026-10-03 tiene DIEZ preguntas numeradas 1 a 10: 1–4 mensajes al servidor (A-54), 5–9 gap trading (5–7 = P1 a–d de CIERRES-DE-MERCADO §0.6; 8 = P2; 9 = P3; A-55) y 10 tamaño de posición (R17). Corrige donde el encargo o tus textos digan «P1–P4».
>
> 2. Guarda el correo como fuente escrita, igual que la respuesta del 29-09: enviado por Aleks (abriosotapia@gmail.com) a support@ftmo.com el 2026-10-03, como respuesta en el ticket VDW-DPMWR-965, asunto «Re: Clarification on Swing account rules for an automated EURUSD strategy - [VDW-DPMWR-965]». Texto literal:
>
> «Hello Guilherme,
>
> Thank you for your previous answer. I am preparing an FTMO Swing account on MT5 with an Expert Advisor, and I would like to follow the rules exactly, so I have a few follow-up questions.
>
> Server messages (2,000 per day)
> 1. Do rejected orders or rejected modification requests count towards the limit?
> 2. Does each modification of a pending order (price, stop loss or take profit) count as one message?
> 3. Do cancellations of pending orders and closing of positions count?
> 4. At what time, and in which time zone, is the daily count reset?
>
> Gap trading ("within two hours before a relevant market closes for at least two hours")
> 5. Does this also apply to placing pending orders (limit or stop) within those two hours, even if they are not filled?
> 6. If a pending order was placed before the two-hour window and gets filled within it, is that considered opening a trade within the window? Should such orders be cancelled before the window starts?
> 7. Is modifying the price of an existing pending order within the window treated as placing a new one?
> 8. For EURUSD, is the "relevant market" only the EURUSD trading session on your servers (as shown on the Symbols page and in the Trading Updates), or does the closure of other markets (for example, stock exchanges on Good Friday) also count?
> 9. Can you confirm that the daily EURUSD break (23:55 to 00:05 server time) does not count as a market closure for this rule?
>
> Position size (question 2 of my previous email, which was not answered)
> 10. The EA risks the same fixed percentage on every trade, so the lot size varies with the stop distance, and one trade can be up to about 5 times larger in lots than another with the same monetary risk. Does this count as "substantially larger position sizes"?
>
> Thank you in advance.
>
> Best regards,
> Alex»
>
>    En A-54, A-55 y la línea de R17, cita el número de pregunta del correo que les toca.
>
> 3. No saques nada más de PROJECT_STATE: el tope del test es 25.000; el margen de 23.000 es mío y la próxima rama es la limpieza de Technical Debt.
>
> make check sellado; revisor solo sobre lo que cambie, con su informe pegado.
>
> Orden de cierre, para cuando invoque /cerrar-rama: tag stable/F36r-fuentes-ftmo; hallazgos del consultor que el revisor no vio: 0 bloquea, 0 importa, 1 menor (el encargo numeraba mal las preguntas; el error fue mío y lo detectó la sesión, no el revisor). Lección para el revisor: cuando un encargo cita un recuento, comprobar que los grupos que nombra suman ese número.
