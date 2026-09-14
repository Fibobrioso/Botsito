---
status: ACTIVE
date: 2026-09-14
phase: post-F13 (habilita F18-F24)
---

# 0026 · La prop firm es FTMO, reto 2-Step, tipo de cuenta Swing

## Decision

1. **La firma es FTMO**, programa **FTMO Challenge: 2-Step** (reto → verificación → FTMO Account),
   **tipo de cuenta SWING**, tamaño **100.000 USD**. Se descarta FundedNext.
2. **Los topes de la firma entran en el registro como parámetros `prop_firm`** (`firma_*`) y son
   objeto distinto de los topes del trader: 5 % de pérdida diaria y 10 % de pérdida máxima, las dos
   sobre el **capital simulado inicial** y las dos medidas sobre **equity** (saldo + P/L flotante,
   swaps y comisiones). La máxima es **estática** en el 2-Step: capital inicial − 10 %, constante en
   las dos fases y en la cuenta fondeada.
3. **El límite del día se fija con el saldo a medianoche CE(S)T**, no con el capital inicial:
   `limite_del_dia = saldo_a_medianoche_CE(S)T − 0,05 × capital_inicial`. El ejemplo oficial de FTMO
   Academy va sobre una cuenta de 200.000: el día 1 el límite es 190.000 y, si el día cierra en
   204.000, el día 2 es 194.000. Escalado a 100.000 da 95.000 y, con un cierre en 102.000, 97.000.
   El escalado es cuenta nuestra, no una cita.
4. **El motor respeta siempre el más restrictivo** entre el freno del trader
   (`perdida_maxima_diaria`, `perdida_maxima_semanal`) y el de la firma. Es una regla de la spec y
   no un parámetro: **RN-029**, clase `gate`, `decision: ADR-0026`.
5. **El tipo Swing se elige en la compra y no se puede cambiar después**: FTMO lo dice como
   *«Change from Standard to Swing: Not allowed»*. Por eso esta decisión se toma antes de pagar.
6. **Lo que la demo de FundedNext midió ya no vale como medición.** Los cinco parámetros del
   instrumento pasan a DEFAULT_AMBIGUOUS bajo **A-27**: se conserva el valor como default declarado,
   no como medición heredada. Los dos del reloj del servidor pasan a UNKNOWN bajo **A-28**.
7. **La restricción de noticias desaparece con el tipo Swing**, y con ella el motivo de ADR-0022.
   `filtro_noticias` vuelve a `no`, RN-028 pasa a DESCARTADA, **A-17 queda DECIDIDA por este ADR** y
   **A-22 cambia de sentido**. La decisión y la enmienda viven en ADR-0022 (sección «Enmienda del
   2026-09-14»).

## Problema que resuelve

Tres a la vez.

**(a) La firma anterior prohíbe lo que el proyecto quiere hacer.** FundedNext: *«traders on account
sizes of $50,000 and above must trade manually and may not use Expert Advisors, trading bots, or
any automated tools»*. El objetivo —un bot en una cuenta fondeada de 100.000— es imposible ahí.

**(b) El reglamento de la firma no estaba en el repositorio.** ADR-0004 prometió que `prop_firm`
guardaría la pérdida diaria y total, el lote máximo y el presupuesto de mensajes, y ninguno de sus
parámetros era eso. La única fuente era la memoria del trader, marcada UNKNOWN
(`ev-v4-012524-0ef85a89`: *«el total es un 7, ¿no? O un 10. 8, 8»*).

**(c) El tipo de cuenta decide si hace falta un calendario económico**, que es una funcionalidad
entera con su fuente de datos.

## Alternativas consideradas

1. **FTMO 2-Step Swing** (elegida).
2. **FTMO 2-Step Standard.**
3. **FTMO 1-Step.**
4. **FundedNext con cuenta de menos de 50.000**, más su complemento de EA.
5. **El bot como generador de señales y ejecución manual.**

## Por que elegimos esta opcion

Porque el tipo Swing **borra una funcionalidad entera del camino crítico** y a la vez **devuelve
fidelidad**. FTMO: *«The Swing account type have no restrictions on trading during news
releases»*. El trader opera dentro de las noticias y su estrategia funciona ahí
(`fb-2026-09-09-sesion-01-3565552d`): un bot que se abstiene deja de hacer operaciones que él sí
hace. Con Swing no hay que abstenerse.

Y porque el tope **estático** del 2-Step es el único que se puede modelar sin inventar nada.

## Por que descartamos las demas

- **(2) Standard.** En la cuenta fondeada *«it is not permitted to open or close any trades [...]
  within a time window starting 2 minutes before and ending 2 minutes after the release of selected
  news announcements»*, y eso incluye que salte un stop o un objetivo ya colocados. Un bot que
  siempre tiene un stop en el mercado no puede garantizarlo sin un calendario fiable y sin lógica
  para retirar el stop antes de cada evento: una funcionalidad entera que toca bucle, journal y
  replay.
- **(3) 1-Step.** La pérdida máxima **arrastra** (se recalcula sobre el saldo más alto alcanzado) y
  lleva regla del mejor día al 50 %. Con una estrategia de acierto bajo y nueve pérdidas seguidas
  medidas en enero (`docs/validation/AUDITORIA-2026-09-12-material.md`), un tope con arrastre es
  mucho más hostil y más difícil de modelar.
- **(4) FundedNext por debajo de 50.000.** Obliga a bajar el tamaño, añade una tarifa recurrente,
  mantiene un tope por estrategia de bot, y su regla de noticias —recortar el 40 % del beneficio de
  lo operado entre 5 minutos antes y 5 después de una noticia de alto impacto correlacionada— sigue
  recortando fidelidad.
- **(5) Señales y ejecución manual.** Contradice la decisión de que el bot ejecuta, y las dos firmas
  prohíben pasar el reto con bot y operar a mano después, o al revés.

## Impacto

- **Sale del camino crítico la funcionalidad de calendario de noticias.** Queda como precondición
  del pre-vuelo de F33 para el día en que el bot corra en una cuenta con restricción (ADR-0022,
  enmienda).
- **Nacen once parámetros `firma_*`** con `fuente: ADR-0026`, y RN-029 consume los que el veto
  necesita.
- **El más restrictivo cambia según el saldo, y no es siempre el del trader.** El 4,5 % del trader se
  mide sobre el saldo inicial del día y el 5 % de la firma sobre el capital inicial. Por encima de
  5.000 / 0,045 = **111.111,11** de saldo al empezar el día, el 4,5 % del trader supera los 5.000 de
  la firma y manda la firma. El semanal del trader (9 %, sobre el saldo actual, se reinicia cada
  semana) tampoco cubre el total estático: dos semanas con un 8 % perdido cada una no tocan nunca el
  9 % semanal y rompen el 10 % total. Por eso RN-029 existe como regla propia y no como nota de
  RN-020.
- **Llegar al límite de la firma ES la infracción.** RN-029 no evita perder la cuenta: impide seguir
  operando y deja escrita la jerarquía. Lo que evita llegar son los frenos del trader y el margen
  que F21-F24 decidan dejar; ver «Que debe decidir el usuario» en el informe de la rama.
- **Pierden su fuente siete parámetros** medidos contra la demo de FundedNext el 2026-09-05. Los
  cinco del instrumento (`instrumento_digitos`, `instrumento_contrato`, `instrumento_lote_minimo`,
  `instrumento_lote_paso`, `instrumento_stops_level`) pasan a DEFAULT_AMBIGUOUS bajo A-27, porque
  RN-026 y RN-027 los ejecutan y una regla vigente no puede nombrar un UNKNOWN. Los dos del reloj
  (`broker_offset_base`, `broker_dst`) pasan a UNKNOWN bajo A-28 porque, tras ADR-0027, ninguna regla
  vigente ni ningún predicado los nombra: lo comprueban `comprobar_forma` y `comprobar_consumo`, no
  un supuesto.
- **Apalancamiento 1:30 en Swing** (1:100 en Standard). Con 0,5 % de riesgo sobre 100.000 (500 USD)
  y un stop a 11 pips, el lote es 500 / (11 × 10) = **4,545 lotes**, 454.545 de nocional en la
  divisa base y un margen de 454.545 × P / 30, donde P es el precio de EURUSD: 15.152 con P = 1,00 y
  19.697 con P = 1,30. Cabe de sobra **con ese stop, no con cualquiera**: el margen es
  166.667 × P / d, con d el stop en pips, y supera los 100.000 de la cuenta con un stop por debajo
  de 1,67 × P pips (1,95 pips con P = 1,17). F21 lo comprueba con la distribución real de cajas.
- **El límite de 2.000 peticiones al servidor por día** sigue siendo restricción de diseño de
  primera clase, ahora con fuente de FTMO: por encima es práctica prohibida (*«an excessive number
  of more than 2,000 server requests per day»*).
- **El pre-vuelo de F33 se reescribe** contra FTMO: especificaciones del símbolo, reloj del
  servidor, tipo de cuenta Swing y apalancamiento.
- Queda sin tocar lo que no es de la firma: ningún fichero de `knowledge/evidence/` ni de
  `knowledge/feedback/`. Ninguna de estas decisiones es del trader.

Fuentes del reglamento, leídas el 2026-09-14:
[Trading Objectives](https://ftmo.com/en/trading-objectives/) ·
[Maximum Daily Loss, FTMO Academy](https://academy.ftmo.com/lesson/maximum-daily-loss/) ·
[Forbidden Trading Practices](https://ftmo.com/en/forbidden-trading-practices/) ·
[Can I trade news?](https://ftmo.com/en/faq/can-i-trade-news/) ·
[Swing account type](https://ftmo.com/en/faq/ftmo-swing-account-type/) ·
[Account specifications](https://ftmo.com/en/faq/what-are-the-account-specifications/) ·
[Consistency rules](https://ftmo.com/en/faq/do-you-have-any-consistency-rules/) ·
[Instruments and strategies](https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/) ·
[FundedNext · Is EA allowed?](https://help.fundednext.com/en/articles/8020763-is-ea-allowed-in-fundednext) ·
[FundedNext · Is News Trading Allowed?](https://help.fundednext.com/en/articles/10701447-is-news-trading-allowed-at-fundednext).
Las citas se tomaron a través de un paso automático de lectura de página, no del HTML crudo; el
dueño las contrasta en el panel antes de comprar (informe de la rama, §«Lo que tiene que hacer el
dueño»).

## Fecha / fase

2026-09-14, después de F13 (decisión del consultor; el trader no interviene). Habilita F18-F24 y
reescribe el pre-vuelo de F33.

## Estado

ACTIVE
