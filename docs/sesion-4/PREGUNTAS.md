# Sesión 4 con el trader: las preguntas, después del barrido

Rama `feature/barrido-sesion-4`, 2026-09-30, desde `main` en `3375249`. **Solo lectura y este
documento**: no cambia el motor, la spec, las ambigüedades ni el feedback.

**Cómo se hizo:**
1. Se reunieron todas las preguntas abiertas:
   - la F de Next Action y la A5 de `PROJECT_STATE.md`;
   - las 21 ambigüedades ABIERTAS de `knowledge/spec/ambiguedades.yaml`;
   - los 9 registros de `botsito feedback pending`;
   - las preguntas para el trader de `docs/validation/` y `docs/nocturno/`.
2. Cada una se buscó en el corpus ya ingerido, sesiones 1 a 3 y vídeos, con `botsito kb find` y
   `botsito kb at`, en los ítems de evidencia y en los registros de feedback.
3. Se juntaron las repetidas.

**Las preguntas van cerradas y sin gráficos, por orden del consultor.**
`docs/runbooks/SESION-DE-PREGUNTAS.md` pide preguntas abiertas, para no sugerir, y permite enseñar
gráficos de construcción. Para esta sesión manda el encargo: cada pregunta se hace con palabras y
con opciones cerradas, y **no se enseña ningún gráfico**. Donde las opciones pueden sugerir, se
añade «otra, ¿cuál?».

## 0. Qué se abrió (exposición)

- **Transcripción cruda** (`data/transcripciones/`), solo con `kb find` y `kb at`:
  - v3: 0:06:06, 0:33:18, 1:09:25–1:10:45;
  - v4: 0:29:01, 0:38:20–0:38:49, 0:50:53, 1:03:26–1:08:52;
  - v5: 0:02:46, 0:04:56, 0:05:15, 0:05:27;
  - v6: 0:08:21–0:08:56, 0:52:30–0:53:20, 1:03:01;
  - v7: 0:04:10, 0:06:07, 0:15:50, 0:16:30, 0:21:45–0:22:25, 0:44:59–0:45:29;
  - v9: 0:01:14–0:01:52, 0:05:24–0:05:58, 0:13:12–0:13:25, 0:47:21–0:48:27, 1:04:39,
    1:05:47, 1:11:09, 1:26:12–1:26:36, 1:29:51–1:30:34, 1:32:05–1:32:13.
- **Ninguno cae en un tramo de `knowledge/corpus/tramos_no_citables.yaml`**:
  - v6: 0:41:00–0:50:11 y 1:53:30–1:57:31;
  - v7: 0:15:34–0:15:48;
  - v9: los doce tramos de cuarentena, precaución y cortes de audio.

  De A-42 solo se usa lo que ya está fuera de la cuarentena, en `SESION-03-EXTRACCION.md`; el texto
  con máscara no es citable.
- **Evidencia y feedback**: los YAML de `knowledge/evidence/` y `knowledge/feedback/` citados abajo.
- **Informes**: `SESION-03-EXTRACCION.md`, `ACTIVAR-SESION-03.md`, `BLOQUE-DE-LA-CAJA.md`,
  `CAJA-77.md`, `NOCTURNO-01OCT.md` y `docs/nocturno/INFORME-01oct.md`.
- **Nada más**: ningún fotograma, ningún libro xlsx, ningún caso reservado u oculto y ningún
  agregado. No hay exposición nueva que declarar en `HOLDOUT-EXPOSICIONES.md`.

## 1. Las que hay que hacer (22)

> **Añadidas el 2026-10-02** (`feature/escenarios-por-sesion`, orden del consultor): la 20 y la 21 en
> la sección D, antes de la 19, que sigue yendo la última; y una segunda parte de la 15. Y la 22
> (`trabajo/cerrar-a29-a36`, orden del consultor), en la sección A, detrás de la 6: A-36 se reabrió.

Ordenadas por cuánto destraban:
- primero, lo que bloquea F35 y la vida de la orden;
- después, A-42, por el cambio de hora del 25 de octubre;
- después, las ambigüedades bloqueantes;
- al final, el resto.

Cada una lleva su estado tras el barrido y lo que ya dijo el trader, para que Aleks no pregunte lo
que ya está.

### A. La vida de la orden stop (F35)

**1. Cuándo pones la orden, una vez formado el mínimo (o máximo) en M1.** · PARCIAL · A-49, F35
§5.2. La añadió el consultor el 2026-09-30, al cerrar el barrido: va la primera de todas y abierta.
- **Pregunta:** «Cuando se forma el mínimo (o máximo) en M1, ¿pones la orden de inmediato o esperas
  a algo? ¿A qué?»
- **El barrido no la encontró respondida.** Lo grabado dice dónde va la orden: tras la toma, en el
  posible punto de breaker y con la mecha incluida. También dice que se actualiza con cada punto
  nuevo. No dice cuándo: es el «Falta» de la pregunta 2. En construcción, el bot pone la orden a
  0,9 minutos de mediana desde que se forma el pivote, y el trader entra a 2,5 (F35 §5.2).
- Va abierta y antes de la 2, que ofrece opciones, para no sugerirle la respuesta. Si la contesta
  aquí, la 2 solo se confirma.

**2. Cuándo un mínimo de M1 se convierte en tu punto de breaker.** · PARCIAL · F («¿pones la orden en
el último mínimo…?»), A-49 y el momento de entrada medido en F35 §5.2.
- **Ya dijo**:
  - la orden se pone después de la toma de liquidez: «primero se desarrolla una toma de liquidez
    para recién nosotros poder trazar los posibles puntos de breaker» (v9 0:01:43);
  - se actualiza con cada punto nuevo: «sigue vivo hasta que se desarrolle otra próxima, otro
    posible punto de breaker» (v9 1:32:07);
  - un punto se valida con la mecha: «apenas con una mecha aquí y ya podríamos validar ese punto
    como un posible breaker» (v7 0:22:01–0:22:45);
  - una vela casi plana no marca punto (v9 1:30:21).
- **Falta** en qué momento exacto el mínimo pasa a ser el punto donde se pone la orden. En
  construcción, el bot la pone a 0,9 minutos de mediana desde que se forma el pivote, y el trader
  entra a 2,5.
- **Pregunta:** «Después de la toma, cuando el precio marca un mínimo nuevo en M1 en una venta, ¿en
  qué momento pones ahí la orden stop?
  - (a) en cuanto cierra la vela que marca ese mínimo;
  - (b) cuando cierra la vela siguiente, que tiene que ser del color contrario;
  - (c) cuando el precio vuelve a acercarse a ese mínimo;
  - (d) otra, ¿cuál?
  ¿Y en una compra es lo mismo con el máximo?»

**3. El stop al poner la orden: ¿en el 1 o en el 0,8?** · PARCIAL · F («el stop en el 0,8 o en el
1»), A-18.
- **Ya dijo**:
  - «primer cálculo es de 13 a normal o sea desde el punto 1 y luego se recalcula» (v7 0:06:07);
  - el lote se calcula del 0 al 0,8: «se calcularía a partir del 0 al 0.8» (v9 1:03:11);
  - a la pregunta de cuándo pasa al 0,8 no contestó (v9 1:01:27, `SESION-03-EXTRACCION.md` A-18).
- **Lo que sugiere el libro:** en su backtest, el stop inicial está en el 1 de la caja en 3 de las 5
  cajas comparables (`CAJA-77.md` §2.1).
- **Pregunta:** «Cuando pones la orden, el stop, ¿dónde lo pones?
  - (a) ya en el 0,8;
  - (b) en el 1, y lo pasas al 0,8 cuando se llena la orden;
  - (c) en el 1, y lo pasas al 0,8 más tarde, ¿cuándo?;
  - (d) en el 1, y no lo mueves.»

**4. Si el precio sube más antes de llenarse, ¿se mueve el 1 de la caja?** · SIN RESPUESTA · A-49,
y la decisión 5 del ADR de F35 (`caja_se_fija`, en la rama `feature/F35-orden-stop-pivote`, sin integrar).
- **Ya dijo** que la caja va «desde el posible punto de breaker, o sea el punto de breaker hasta el
  punto más alto» (v9 0:47:21; también v7 0:15:50). No dijo si ese punto más alto se actualiza
  mientras la orden espera.
- **Pregunta:** «Con la orden ya puesta y sin llenar, si el precio sube un poco más y marca un
  máximo nuevo, ¿qué haces?
  - (a) muevo el 1 de la caja al máximo nuevo, y con él el stop y el lote;
  - (b) dejo la caja como estaba;
  - (c) otra.»

**5. La orden sin llenar al acabar la sesión o la ventana.** · PARCIAL · A-30 y la parte pendiente de
A-39.
- **Ya dijo**:
  - una operación abierta se cierra un minuto antes de que acabe su vela de 4 horas (v9 0:27:35);
  - una orden sin llenar «sigue vivo hasta que se desarrolle otra próxima, otro posible punto de
    breaker» (v9 1:32:07);
  - qué hace con la orden cuando acaba la sesión no lo dijo. El corte de audio de v9 0:28:49–0:29:53
    cae en esa respuesta.
- **Pregunta:** «Si a las 11 o a las 3 tienes una orden stop puesta que no se ha llenado, ¿qué haces
  con ella?
  - (a) la quito;
  - (b) la dejo y la sigo moviendo en la sesión siguiente;
  - (c) la dejo, pero solo hasta las 3;
  - (d) otra.»

**6. «Lo mínimo posible» al redondear el stop: ¿un punto o un pip entero?** · PARCIAL · F (el
redondeo), ADR-0061 §2.
- **Ya dijo** «lo mínimo posible o sea, si es un pip, un pip y ya está» (v9 1:05:41–1:05:50).
- Cuando dice «pip» suele querer decir lo mínimo:
  - «al menos por un pip o una milésima de pip» (v6 1:03:01);
  - «basta que rompa o sea con lo mínimo un pib» (v3 0:06:06).
- Es probable que sea un punto, pero no lo dijo.
- **Pregunta:** «Cuando el 0,8 no cae justo en un precio y lo redondeas hacia fuera, ¿cuánto lo
  mueves?
  - (a) a la última cifra, la quinta decimal (un punto);
  - (b) a la cuarta decimal (un pip entero, 10 puntos).»

**22. Dónde va la orden de entrada frente al 0 de la caja.** · PARCIAL · A-36, C6. La añadió el
consultor al reabrir A-36 (`trabajo/cerrar-a29-a36`).
- **Ya dijo**, del 0 de la caja: a «el cero de la caja va siempre en el extremo del bloque, mecha
  incluida, o ese es un poco dentro?», «Mecha incluida, siempre.» (v9 1:17:14–1:17:21). Habla del 0,
  no de dónde pone la orden.
- A-36 se preguntó sobre una orden límite, y la entrada es con orden stop (A-47).
- En pantalla hay una orden puesta unos puntos más allá del 0 (C6, de
  `DISENO-ENTRADA-RUPTURA.md` §2.8).
- **Pregunta:** «Cuando pones la orden de entrada, ¿va exactamente en el 0 de la caja, contando la
  mecha, o unos puntos más allá? Si va más allá, ¿cuántos?
  - (a) exactamente en el 0, contando la mecha;
  - (b) unos puntos más allá: ¿cuántos?;
  - (c) otra, ¿cuál?»

### B. El reloj de invierno (A-42), antes del 25 de octubre

**7. Con qué reloj empiezas a las 7 en invierno.** · PARCIAL · A-42 (bloqueante), F.
- **Ya dijo**, fuera de la cuarentena:
  - «En invierno empieza» (v9 1:07:40);
  - a «entonces en invierno no empiezas a las 7 o a las 6 sería tu reloj, ¿no?», «Sí» (v9 1:07:53);
  - «lo adapto. O sea, automáticamente se adapta. La plataforma la adapta» (v9 1:08:09).
- La respuesta principal está en un tramo no citable, y según la extracción dijo «creo».
- **Pregunta:** «El domingo 25 de octubre cambia la hora en España. Desde ese día, tu primera sesión,
  ¿cuándo empieza?
  - (a) a las 7:00 de tu reloj, como ahora;
  - (b) a las 6:00 de tu reloj;
  - (c) otra.»
- **Y, si responde (b):** «¿Y la segunda sesión y el cierre, también una hora antes: de 10 a 14?»

### C. Las ambigüedades que bloquean al bot

**8. Qué corta la racha de 9 pérdidas y cuándo vuelves a operar.** · SIN RESPUESTA · A-51
(bloqueante).
- **Ya dijo** que para con «9 pérdidas seguidas» (v9 1:11:30–1:11:54). No se le preguntó qué corta la
  racha.
- **Pregunta:** «Llevas 5 pérdidas seguidas y sale un break even. ¿La racha sigue en 5 o vuelve a
  empezar? (a) sigue en 5; (b) vuelve a cero.»
- **Segunda pregunta:** «Y si llegas a la novena, ¿cuándo vuelves a operar?
  - (a) al día siguiente;
  - (b) la semana siguiente;
  - (c) cuando revises qué pasó, sin fecha fija;
  - (d) otra.»

**9. El tope de pérdida: ¿porcentaje o 9 seguidas?** · CONTRADICTORIA · A-44 (bloqueante).
- **Sesión 1**: 4,5 % del día y 9 % de la semana (`fb-2026-09-09-sesion-01-4963aa6f`,
  `-5e23d47c` y `-a85b6bc7`).
- **Sesión 3**: «9 pérdidas como máximo / O sea, para / El tope es eso, 9 pérdidas como máximo»
  (v9 1:11:30) y «Seguidas» (v9 1:11:46).
- **Pregunta:** «¿Qué te hace parar de operar?
  - (a) solo las 9 pérdidas seguidas;
  - (b) solo perder el 4,5 % en un día o el 9 % en una semana;
  - (c) las dos cosas, lo que llegue antes.»

**10. Zona limpia.** · PARCIAL · A-21 (bloqueante).
- **Ya dijo**: «esto limpio me refiero a que no haya, o sea, por ejemplo, una vela verde, una vela
  bajista, una vela verde, una bajista» (v9 1:19:57).
- No contestó cuánto puede medir el retroceso del esquema 2 (v9 1:17:42).
- **Pregunta 1:** «Una zona está limpia si no hay velas verdes y rojas alternándose. ¿Es eso? (a) sí;
  (b) no, además…»
- **Pregunta 2:** «En el esquema 2, ¿cuántas velas puede tener como máximo el retroceso?
  - (a) una;
  - (b) dos o tres;
  - (c) no importa el número;
  - (d) otra.»

**11. El alto de M15 que el precio supera un poco.** · PARCIAL · A-35 (bloqueante).
- **Ya dijo**: el alto vale cuando cierra la vela contraria (v9 0:38:06–0:38:34).
- A «¿y si después el precio lo supera un poco?» no contestó.
- **Pregunta:** «Marcaste un alto en M15 y después el precio lo pasa por poco con la mecha y vuelve.
  ¿Qué haces?
  - (a) sigo usando el mismo alto;
  - (b) marco el nuevo;
  - (c) depende de si cierra la vela por encima.»

### D. El resto

**12. Las salidas por encima de 3 R.** · CONTRADICTORIA · G-2 y A-33 (A5 de Next Action).
- **Sesión 3**: «el objetivo es fijo como bien sabemos bro Ahora no lo gestionamos Es fijo»
  (v9 1:00:53).
- **Antes dijo**:
  - «existe la posibilidad de amplificar a 1.4 el RR pero creo que eso ya lo veremos más adelante»
    (v5 0:05:15);
  - «si tienes un 1 a 3 pero consideras que puede llegar a más entonces en ese caso pues más
    protegiendo» (v3 0:33:18).
- En su propio backtest, siete ganadoras salen entre 4,2 y 5,3 veces el stop del libro
  (`ACTIVAR-SESION-03.md` §4.1). Eso no se le enseña.
- **Pregunta:** «¿Alguna vez dejas correr una operación más allá de tres veces la caja?
  - (a) nunca, el objetivo es fijo;
  - (b) a veces, ¿cuándo?;
  - (c) antes sí, ahora no.»
- **Preparación pendiente**: medir la caja de esas siete operaciones en sus fotogramas antes de la
  sesión, solo en construcción, por instante localizado (`ACTIVAR-SESION-03.md` §4.1).

**13. La vela de 4 horas que rompe por los dos lados y cierra sin cuerpo.** · SIN RESPUESTA ·
ADR-0060 §2.
- **Ya dijo**: con doble ruptura decide el color (v9 0:16:17), y una vela M1 casi plana «cuenta como
  si no existiera» (v9 1:30:21). No dijo qué pasa en H4 sin color.
- **Pregunta:** «La vela de 4 horas rompe el máximo y el mínimo de la anterior y cierra justo donde
  abrió. ¿Qué sesgo tomas?
  - (a) alcista;
  - (b) bajista;
  - (c) el de la vela anterior;
  - (d) ese día no opero.»

**14. El umbral de la vela casi plana.** · PARCIAL · RN-007, E-3.
- **Ya dijo** que «cuenta como si no existiera» (v9 1:30:21), y «en EURUSD muy rara vez me lo he
  topado» (v9 1:29:56). No dio umbral.
- **Pregunta:** «¿Con cuánto cuerpo una vela de M1 deja de ser casi plana?
  - (a) solo si abre y cierra en el mismo precio;
  - (b) con 1 o 2 puntos de cuerpo o menos;
  - (c) otra cifra.»

**15. Una liquidez tomada antes de las 7.** · PARCIAL · A-43.
- **Ya dijo** que una liquidez formada antes de las 7 vale, pero «tiene que tomar para que se tome
  la entrada dentro de las 7» (v9 0:45:40–0:45:44). No se le preguntó por una toma anterior a las 7.
- **Pregunta:** «Si el precio toma esa liquidez a las 6:45, antes de tu horario, ¿la usas para
  operar a partir de las 7? (a) sí; (b) no, necesito otra toma dentro del horario.»
- **Y si contesta (b), una segunda parte** (añadida el 2026-10-02, `feature/escenarios-por-sesion`,
  orden del consultor): «¿Y si a las 6:45 la toma, el precio vuelve por encima y a las 7:20 la vuelve
  a tomar? (a) esa segunda toma ya vale, es dentro de tu horario; (b) no, esa liquidez ya está
  gastada y espero otra.» Hoy el motor hace (b), PROVISIONAL (`toma_antes_de_la_ventana`, ADR-0066):
  una liquidez tomada antes de abrir no vuelve a contar en la sesión aunque el precio la recupere.

**16. Cuál de tus dos backtests de agosto vale.** · PARCIAL · E-1.
- **Ya dijo** «hay que usar lo último, el último que fue el backtest completo» (v9 1:23:47–1:23:50).
  Pero el último en fecha (el vídeo) es el que se saltó operaciones de break even, y el completo es
  el original.
- **Pregunta:** «Para el bot, ¿qué backtest de agosto vale?
  - (a) el que hiciste primero, completo;
  - (b) el del vídeo.»

**17. Si solo el 0 de la caja cuenta frente al nivel tomado.** · PARCIAL · A-50.
- **Ya dijo** «¿El 0 o el 0? No, no importa» (v9 0:51:08–0:51:12), y que todo tiene que
  desarrollarse más allá del nivel. Queda por confirmar que no filtra.
- **Pregunta:** «Si la caja queda a caballo del nivel de la liquidez que se tomó, ¿descartas la
  entrada? (a) sí; (b) no, me da igual.»

**18. Los intentos: ¿por marca o por toma?** · PARCIAL · A-25.
- **Ya dijo**:
  - «Sí, serían tres intentos por liquidez» (v9 1:30:54);
  - con un alto nuevo más bajo, opera primero el más reciente (v9 1:37:20–1:37:47).
- **Pregunta:** «Si el precio toma un alto, gastas dos intentos, y luego toma otro alto más arriba,
  ¿empiezas de nuevo con tres? (a) sí; (b) no, me queda uno.»

**20. Cuántos escenarios puede haber en una sesión como máximo.** · PARCIAL · A-52 (la subpregunta
de A-46 que quedó sin número). La añadió el consultor el 2026-10-02 (`feature/escenarios-por-sesion`).
- **Ya dijo**:
  - las dos sesiones son «cada uno un mundo diferente» y «no importa cómo terminó la primera
    operación» (v9 0:32:53–0:33:11);
  - «Pues, eso no lo podemos definir. [...] en todas estas 4 se va a dar una operación» (v9
    0:33:18–0:33:40, `ev-v9-003318-c0503fe5`): no dio un número.
- **Antes dijo** «como máximo dos entradas por día» (`ev-v4-003350-acb03ee7`).
- Hoy el motor no pone tope (`max_escenarios_por_sesion` = `sin_limite`, PROVISIONAL): cada
  liquidez nueva tomada en la sesión abre un escenario, y en una tarde movida de construcción se
  abren cinco.
- **Pregunta:** «En una misma sesión, cada vez que el precio toma una liquidez nueva de M15,
  ¿vuelves a buscar entrada?
  - (a) sí, todas las veces, no hay máximo;
  - (b) hasta un número de liquidez por sesión, ¿cuántas?;
  - (c) otra, ¿cuál?»

**21. La orden puesta cuando el precio toma otra liquidez.** · SIN RESPUESTA · A-53 (lo que A-38 no
cubre). La añadió el consultor el 2026-10-02 (`feature/escenarios-por-sesion`).
- **Ya dijo** que la orden «sigue vivo hasta que se desarrolle otra próxima, otro posible punto de
  breaker» (v9 1:32:07). Eso es dentro de la misma liquidez; no se le preguntó qué pasa si, con la
  orden puesta y sin llenar, el precio toma OTRA liquidez de M15.
- Hoy el motor la deja viva y la mueve al primer punto de breaker de la liquidez nueva, PROVISIONAL
  (`orden_pendiente_al_abrir_escenario` = `se_mueve`, ADR-0066). Hasta ese punto, la orden vieja
  todavía se puede llenar.
- **Pregunta:** «Tienes una orden stop puesta, sin llenar, y el precio toma otra liquidez de M15.
  ¿Qué haces con la orden?
  - (a) la quito en ese momento y espero el punto de la liquidez nueva;
  - (b) la dejo, y la muevo cuando aparezca el punto de la liquidez nueva;
  - (c) otra, ¿cuál?»

**19. Las 7 capturas que venían con el backtest de marzo.** · SIN RESPUESTA ·
docs/validation/REGISTRO-MARZO.md. La añadió el consultor el 2026-09-30: va la última.
- Con el libro de marzo llegaron 7 imágenes JPEG con nombres sin significado. **No se han abierto
  ni se abrirán**: si son capturas de la pestaña Analytics, son agregados de un mes que tendrá días
  reservados. No se le enseña ninguna.
- **Pregunta:** «¿Qué son las 7 capturas que venían con el backtest de marzo?»
- **Nota para Aleks:** pregunta solo qué tipo de capturas son; si empieza a dar cifras, córtalo; el
  tramo va a cuarentena.

## 2. Las que ya están respondidas: no se vuelven a preguntar

| pregunta (de dónde viene) | respuesta del trader | cita literal | dónde |
|---|---|---|---|
| **Cuándo nace la orden** (A-29) | tras la toma, en los posibles puntos de breaker | «Lo primero es que primero se desarrolla una toma de liquidez Para recién nosotros poder trazar los posibles puntos de breaker» | v9 0:01:43–0:01:52, a la pregunta de 0:01:30 que ofrecía las tres lecturas (`ev-v9-000143-214aacde`); RESUELTA el 2026-10-02 (`fb-2026-09-29-sesion-03-d3063920`; el contexto, en `SESION-03-EXTRACCION.md` §3.4) |
| **Qué velas forman la caja: R1 o R4** (F, A-48) | la caja va del punto de breaker al punto más alto, que es R6, y el bloque es cualquier número de velas del mismo color | «se traza desde el posible punto de breaker, o sea el punto de breaker hasta el punto más alto»; «es indiferente el número de velas […] tendría que ser del mismo color que la vela anterior» | v9 0:47:21 (`ev-v9-004721-2e023ac6`); v7 0:15:50 (ítem creado en la rama F35, sin integrar); v9 1:15:55–1:16:59 |
| **Confirmación grabada de A-47** (F) | orden stop en la ruptura | «aquí queda confirmado que se entra siempre por stop» / «Sí, exacto» | v9 0:01:24–0:01:29 (`ev-v9-000124-d2afa992`) |
| **El break even al tick o al cierre** (F, A-13) | apenas toca, mirado en M1, a la entrada exacta | «Sí, o sea, apenas toca. […] yo siempre lo he estado trabajando, o sea, apenas toca»; «apenas toca, pues se pone en B la entrada» | v6 0:57:01 (`ev-v6-005701-7ae2b8d3`), a la pregunta «¿en el instante en que toca o esperas a que la vela cierre?» (v6 0:53:08); v9 0:55:43 (`fb-2026-09-29-sesion-03-9f506366`) |
| **Un equal, ¿gasta intento?** (E-2) | no | «una reentrada después de un equal […] no, no es considerado […] reentrada después de equal, tampoco es considerado un intento» | v6 0:52:52–0:53:04 (RN-019, `fb-2026-09-09-sesion-01-060cd801`); en v9 1:29:00 el ASR no se entiende |
| Siempre hay sesgo (pendiente de reflejar: RN-033) | siempre | «Siempre va a haber un sesgo, bro, como te digo, o sea, no existe un cejo no claro» | v9 0:15:29 (`fb-2026-09-29-sesion-03-1168f036`) |
| No cierra a mano (pendiente de reflejar: RN-015) | se gana, se pierde o break even | «no cierro o sea yo dejo para hacerlo más lo más objetivo posible […] o bien se gana o bien se pierde. O bien ocurre break-even» | v9 0:59:16 (`…-280cf8f7`) |
| Objetivo fijo (pendiente de reflejar: RN-015) | fijo | «el objetivo es fijo como bien sabemos bro Ahora no lo gestionamos Es fijo» | v9 1:00:53 (`…-3f69a5f7`) |
| La toma de M15 con cuerpo en M1 (pendiente de reflejar: `liquidez_m15_criterio_toma`) | cuerpo; la mecha solo para el punto de breaker | «para el M1 para actualizar el punto de breaker vale la mecha y para la liquidez de M15 hace siempre falta cuerpo» | v9 0:42:17 (`…-43e0f90e`) |
| Tres intentos por liquidez (pendiente de reflejar: `cartuchos_max`) | por liquidez, no por día | «Sí, serían tres intentos por liquidez. […] ¿El máximo es por día? No, no, por liquidez.» | v9 1:30:54 (`…-68a21dc0`) |
| Break even al tocar (pendiente de reflejar: RN-014) | tocar, M1, a la entrada | «apenas toca, pues se pone en B la entrada. […] se mantiene en M1 […] Yo he estado trabajando así, a entrada.» | v9 0:55:43–0:56:41 (`…-9f506366`) |
| Lote del 0 al 0,8 (pendiente de reflejar: `lotaje_base`) | del 0 al 0,8 | «se calcularía a partir del 0 al 0.8» | v9 1:03:11 (`…-d62c788a`) |
| Objetivo del 0 al 1 (pendiente de reflejar: `base_calculo_objetivo`) | 3 veces el 0 → 1 | «desde el punto 0 al punto 1. Y el objetivo es original 1, 3» | v9 1:02:32 (`…-f572f1a0`) |
| La vela casi plana no cuenta (pendiente de reflejar: RN-007) | no marca punto | «cuenta como si no existiera no se puede trazar, o sea allí no se puede trazar un punto de breaker» | v9 1:30:21 (`…-ffab23dc`); **el umbral sigue abierto: pregunta 14** |

Los nueve registros de `feedback pending` son respuestas grabadas que la spec todavía no cita (los
nueve «pendiente de reflejar»). **No son preguntas**: se reflejan en la spec en una rama propia.

## 3. Lo que no es para el trader

- **A-16, A-27 y A-28** son mediciones: el desfase OANDA–Dukascopy, las especificaciones de EURUSD
  en FTMO y el reloj del servidor de FTMO. Se miden en la demo (MedirDemoFTMO, Next Action A); no se
  preguntan.
- **A-32** (qué nivel marcaba una línea de v4 0:53:10) solo tiene sentido con el gráfico, y la
  propia ambigüedad dice «si no lo recuerdas, no pasa nada». Se deja fuera de esta hoja.
- **Lo que tapan los cortes de audio de v9**:
  - A-13 (0:57:00–0:58:06) ya está respondida en lo firme;
  - A-39 (0:28:49–0:29:53) va dentro de la pregunta 5.

  Si llega el audio de respaldo, se escucha antes de preguntar.
- **SOLO DE MEMORIA: ninguna.** La única que lo era, A-47 («cuando rompe», que Aleks recordaba), ya
  está grabada (v9 0:01:24–0:01:29).

## 4. Lo que el barrido encontró para el consultor

- **A-29 ya tiene respuesta grabada** (v9 0:01:43, a la pregunta que ofrecía las tres lecturas):
  `al_aparecer_punto_de_breaker`. **CERRADA el 2026-10-02** en `trabajo/cerrar-a29-a36`
  (`fb-2026-09-29-sesion-03-d3063920`; docs/validation/CERRAR-A29-A36.md).
- **La caja de R6 la dijo el trader dos veces** (v9 0:47:21 y v7 0:15:50): «desde el posible punto
  de breaker hasta el punto más alto». Es la lectura que F35 eligió por la medida. «R1 o R4» deja de
  ser la pregunta: es el punto de breaker y el punto más alto.
- **A-36** («Mecha incluida, siempre», v9 1:17:18): se cerró y **el consultor la reabrió el
  2026-10-02** (`fb-2026-09-29-sesion-03-a0b61bc9`): la cita habla del 0 de la caja, la pregunta se
  hizo sobre una orden límite, y está C6. Va como pregunta 22.
- **El break even al tocar, dicho como «no al cierre»** (v6 0:57:01, a la pregunta del instante), no
  es lo que hace ADR-0061 §5, que lo pone al cierre de la M1 que toca. Es una diferencia de
  implementación y no de pregunta.

## Estado

Barrido hecho y documento escrito. **Por preguntar: 22**: las 17 del barrido, 2 que añadió el consultor el 2026-09-30, la primera y la última, 2 más (la 20 y la 21) del 2026-10-02 (`feature/escenarios-por-sesion`), con una segunda parte de la 15, y la 22 (`trabajo/cerrar-a29-a36`). **Ya respondidas: 14**, que son las 5 de
arriba más las 9 de `feedback pending`. **Fuera de la hoja: 6**, que son 3 mediciones, A-32 y los
2 cortes de audio. **Ninguna** queda solo de memoria. Este documento no cambia nada del motor, de la spec, de las
ambigüedades ni del feedback; los parámetros PROVISIONAL de las preguntas 5, 15, 18, 20 y 21 los
puso `feature/escenarios-por-sesion` (ADR-0066), y se fijan con la respuesta.
