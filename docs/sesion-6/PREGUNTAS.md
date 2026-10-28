# Sesión 6 con el trader: las preguntas, después del barrido

Rama `trabajo/barrido-sesion-6`, 2026-10-28, desde `main` en `b929de2`. **Solo lectura y este
documento** (y, en la rama, el guion de los gráficos de S-7 a S-12 y la hoja 06 del guion de
transcripción): no cambia el motor, la spec, las ambigüedades, el feedback ni los casos. El
inventario, lo que se juntó y lo que quedó fuera, con su porqué: `docs/validation/BARRIDO-SESION-6.md`
§1; las decisiones del consultor del 2026-10-28, al final de ese informe.

> **Antes de grabar: la copia de seguridad de v15 y v16 (crudas y audios, SESION-05-EXTRACCION.md
> §12) en el Drive de A.4.**

**La hoja es el PDF del consultor**, hecho con este documento, como en las sesiones 4 y 5. No sale de
`scripts/hoja_preguntas.py`, que no se toca. Al PDF van, de cada pregunta: el título, «Lo que nos has
dicho», «Lo que todavía no sabemos», la pregunta con sus opciones, «Para precisar» y «Para confirmar
al final». **Las líneas «Para Aleks» no van a la hoja**: dicen de dónde sale la pregunta, qué hace hoy
el bot (con su fichero y su línea) y, en las que tienen parámetro, en qué valor cae cada opción.
**Los gráficos de S-7 a S-12 tampoco van al PDF**: los enseña Aleks en pantalla.

**Los códigos S-1 a S-23 son de la sesión 6.** No son los de la sesión 5: allí S-14 era «qué te hace
no operar un día o una sesión» y S-15 «entrar en la segunda zona después de la toma»; aquí esos dos
temas son S-7 a S-12 y S-5 y S-6. Como manda `docs/runbooks/SESION-DE-PREGUNTAS.md`, cada pregunta
se abre diciendo en voz «pregunta» y su código («pregunta ese uno», «pregunta ese veintitrés») y se
cierra con «fin de pregunta». Sin eso `scripts/transcribir_sesion.py` no la separa. Los textos de
estos códigos ya están en ese guion (`CODIGOS_DE_SESION_TEXTO["06"]`, `trabajo/barrido-sesion-6`),
antes de grabar.

**Cómo se leen:**
- **Preguntas cerradas**, con opciones y «otra, ¿cuál?» en todas. Si el trader no entiende una, se
  le describe la situación de otra manera, sin ofrecerle otras respuestas.
- **Esquemas inventados.** Donde dice «Esquema inventado, no es un día real», se enseña un dibujo
  con esas palabras rotuladas y **el marco escrito dentro del dibujo** («M1», «M15», «4 horas»), sin
  precios ni fechas (lo pidió el trader en la sesión 5). La única excepción son los gráficos 1 a 6
  (S-7 a S-12): días reales de construcción, sin fecha.
- **El 0 y el 1 de la caja**: el 0 es el punto de la orden y el 1 el extremo del lado del stop. En
  una compra, el 0 arriba y el 1 abajo; en una venta, al revés.
- **Nada en dinero**. Las horas, en el reloj de sus gráficos (el de Madrid).
- **«En parte»**: la pregunta lleva lo que ya dijo y pregunta solo lo que falta.

## 0. Qué se abrió (exposición)

- **Evidencia y feedback**: los YAML de `knowledge/evidence/` citados abajo (v6, v9, v10, v15 y v16)
  y de `knowledge/feedback/` (sesiones 1, 3 y 5), leídos con Read y con un guion de la carpeta de
  trabajo que lee ficheros nombrados y se niega a leer los de `.claude/hooks/ficheros_con_ocultos.txt`
  (ninguno lo estaba). El de v6 (0:57:01) cae fuera de sus tramos no citables (0:41:00-0:50:11 y
  1:53:30-1:57:31).
- **Ninguna transcripción, ninguna filtrada, ningún fotograma, ningún libro, ningún caso**; ninguna
  consulta a `kb`.
- **Declarado** en `docs/validation/HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-28 de esta rama (fase 1).

## 1. Las preguntas (23)

Ordenadas por impacto (D4 y decisión 0 del consultor): las dos bloqueantes; lo que más separa al bot
del trader en la clasificación de la corrida diaria (P5 y P6); el resto, en el orden de
`ACTIVAR-SESION-05.md` §3 y después `ACTIVAR-SESION-05-MOTOR.md` §2; y la confirmación corta y «Para
cerrar». A la sesión 5, con 25 códigos, le bastaron 2:15:47 (5:26 por código). Estas 23 se estiman
en unas 1:53. **Si a la hora y media no se ha llegado a S-17, se corta ahí y S-17 a S-23 van a otro
día**, como en la 5 (decisión 0).

### Bloque 1 · Lo que bloquea al bot

**S-1. La pérdida del día que te hace parar: solo con las cerradas o también con la abierta** · en parte · A-44
- **Lo que nos has dicho:**
  - de la base: «De la cuenta basado en el saldo, y que sea en el saldo inicial del día» (por
    escrito, sesión 1, `fb-2026-09-09-sesion-01-bff260ea`);
  - del tope: «Sería un 4,5% de pérdida en el día» (v10 1:09:13, `ev-v10-010913-c4949417`) y «no
    solo el del día y las 9 seguidas la respuesta es la A» (v15 0:08:56, `ev-v15-000856-ee8f7ba3`).
- **Lo que todavía no sabemos:** si, para saber si has llegado a ese 4,5 % del día, cuentas solo las
  operaciones que ya cerraste o también lo que va perdiendo la que tienes abierta.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): un día con dos operaciones
  cerradas en pérdida y una tercera abierta que va perdiendo, toca un punto en el que, sumada a las
  dos, pasaría del tope, y después se recupera y cierra en break even.
- **Pregunta:** «La pérdida del día que te hace parar, ¿la cuentas solo con las operaciones que ya
  cerraste, o también con lo que vas perdiendo en la que tienes abierta?
  - (a) solo con las cerradas;
  - (b) también con la abierta;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - En el dibujo, cuando la abierta toca ese punto, ¿cierras ya o la dejas seguir?
  - Si la cuentas con la abierta, ¿miras lo que pierde en cada momento o solo cuando cierra la vela?
  - Si llegas al tope, ¿quitas también la orden que tuvieras puesta sin llenar?
- **Para confirmar al final:** «Paro cuando la pérdida del día llega al 4,5 % del saldo del inicio
  del día, contando ______ (solo las cerradas / también la abierta)».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.1. Hoy el bot cuenta solo las cerradas:
  `perdida_trader_magnitud` = `saldo`, DEFAULT_AMBIGUOUS bajo A-44, lectura del consultor
  (`knowledge/spec/parametros.yaml:1475-1476`), que lee `engine/tope_trader.py:176`. (a) → `saldo`
  (lo de hoy); (b) → `equity`. El 4,5 % (`perdida_maxima_diaria`, `parametros.yaml:1208-1209`) y la
  base (`base_calculo_perdida_diaria` = `saldo_inicial_dia`, `:1404-1405`) ya están CONFIRMED, y la
  orden sin llenar ya se retira al llegar al tope (ADR-0086, decisión del consultor): la tercera
  subpregunta solo confirma.*

**S-2. Cuándo vuelves a contar desde cero después de parar por la pérdida del día** · A-44
- **Lo que nos has dicho:** de la semana, «vuelvo el día siguiente y ya está» (v15 0:15:46,
  `ev-v15-001546-0dadd11e`).
- **Lo que todavía no sabemos:** a qué hora exacta empieza ese «día siguiente» para contar la pérdida
  desde cero.
- **Pregunta:** «Cuando paras por la pérdida del día, ¿cuándo vuelves a contar desde cero?
  - (a) a las 12 de la noche de tu hora;
  - (b) a las 12 de la noche de la hora del bróker;
  - (c) al abrir tu primera sesión del día siguiente;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - «Tu hora», ¿es la de tus gráficos (la de tus sesiones de 7 a 11 y de 11 a 3) o la de tu casa?
  - Si paras un viernes, ¿vuelves a contar desde cero el lunes, o pasa algo distinto el fin de
    semana?
- **Para confirmar al final:** «El tope es el 4,5 % del día contando ______, y vuelvo a contar desde
  cero a las 12 de la noche de ______ (o: al abrir ______)».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.1. Hoy `perdida_trader_reinicio_huso`
  está UNKNOWN (`parametros.yaml:1530`) y el bot usa la medianoche del huso de corte de la firma
  (`firma_huso_corte` = `Europe/Prague`, `knowledge/cuentas/ftmo-2step-swing-100k.yaml:74`), marcada
  como SUPUESTO (`engine/tope_trader.py:191-194`). El parámetro es un nombre IANA de huso
  (`parametros.yaml:1523-1524`): (a) → `Europe/Madrid` si «tu hora» es la de sus gráficos, o el huso
  de su casa si es la de su casa (la subpregunta lo decide); (b) → `Europe/Prague` si «el bróker» es
  FTMO y su corte del día (R2), lo mismo que hoy; si es el reloj del servidor de MT5, eso es A-28 y
  se mide. **(c) no cabe en ese parámetro**: si la elige, la activación necesita otro parámetro con
  su ADR.*

**S-3. La mecha que mueve tu alto de M15, y la vela que lo toma después** · en parte · A-35
- **Lo que nos has dicho:**
  - cuándo está formado: «en cuanto la vela roja de después ya cerrado» (v15 0:04:47,
    `ev-v15-000447-6699c708`);
  - si el precio lo pasa un poco con la mecha y vuelve: «Ah, se actualiza el de la mecha Se actualiza
    el de la mecha» (v15 0:05:53, `ev-v15-000553-9d95178a`);
  - y en la sesión 4: «lo tiene que pasar con cuerpo no con mecha» (v10 1:24:56,
    `ev-v10-012456-9dc1d221`).
- **Lo que todavía no sabemos:** de qué vela es la mecha que mueve tu alto: la de la propia vela roja
  que lo forma, o también la de una vela que viene después y lo pasa con la mecha y vuelve. Y si en
  un bajo es igual.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos en el dibujo): en M15, velas verdes
  y después una roja cuya mecha sube por encima del máximo de las verdes y cierra por debajo: el alto.
  Después, en M1, una vela que pasa ese alto solo con la mecha y vuelve a cerrar por debajo.
- **Pregunta:** «Marcas un alto en M15 cuando cierra la vela contraria. ¿La mecha que mueve el alto es
  la de la vela contraria que lo forma, o también la de una vela posterior que lo pasa y vuelve?
  - (a) solo la de la contraria;
  - (b) también la de una posterior;
  - (c) otra, ¿cuál?
  ¿Y lo mismo en un bajo?»
- **Para precisar:**
  - **(Esquema inventado, no es un día real, con «M15» y «M1» escritos.)** Una mecha posterior pasa
    tu alto y vuelve, y el alto sube a esa mecha. Después, una vela de M1 cierra con cuerpo por encima
    del alto de antes, pero por debajo de esa mecha. «¿Esa vela ha tomado tu liquidez?
    - (a) sí, cerró con cuerpo por encima del alto de antes;
    - (b) no, todavía no: tiene que cerrar por encima de la mecha;
    - (c) otra, ¿cuál?» (se pregunta conteste lo que conteste arriba).
  - Una vez una vela de M1 cierra con cuerpo por encima y toma tu alto, ¿una mecha que venga después
    lo vuelve a mover?
  - En un bajo, ¿es todo igual, al revés?
- **Para confirmar al final:** «La mecha que mueve mi alto es la de ______; en un bajo, ______; la
  vela que lo toma tiene que cerrar con cuerpo por encima de ______; y una vez tomado, el nivel
  ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.2, ampliada por
  `ACTIVAR-SESION-05-MOTOR.md` §2.1, y ADR-0084:41-48 (decisión 1 del consultor). Hoy
  `liquidez_m15_mecha_que_vuelve` = `cualquier_mecha`, DEFAULT_AMBIGUOUS bajo A-35, lectura del
  consultor (`parametros.yaml:554-555`): el bot hace (i) y (ii) (`engine/motor.py:156-172`). (a) →
  `solo_la_contraria`; (b) → `cualquier_mecha` (lo de hoy); «la mecha no mueve nada» →
  `no_mueve`. El bajo, en espejo, es DECISIÓN DEL CONSULTOR (ADR-0084:49-50). **El nivel se congela
  al tomarse es hoy una DECISIÓN DEL CONSULTOR con efecto visible** (ADR-0084:41-48;
  `domain/pivotes_m15.py:264-281`): la vela del primer «Para precisar» no toma la liquidez (la
  respuesta (b)), y tras la toma ninguna mecha mueve el nivel. Si contesta (a) al primer «Para
  precisar», esa decisión no se sostiene y hace falta ADR.*

**S-4. En M15, una vela sin cuerpo entre las verdes y la roja** · A-35
- **Lo que nos has dicho:**
  - en M15: «No cuenta como vela de después, no cuenta como vela de después si cierra sin cuerpo»
    (v15 0:05:30, `ev-v15-000530-234d4a81`);
  - en M1, dentro del tramo que marca el punto: «las velas sin cuerpo pues no cuentan, en venta lo
    mismo revés es igual» (v15 0:39:59, `ev-v15-003959-5898c61e`).
- **Lo que todavía no sabemos:** si en M15 esa vela sin cuerpo, puesta entre las verdes y la roja,
  corta la racha o se salta como en M1.
- **Esquema inventado, no es un día real** («M15» escrito en el dibujo): tres velas verdes de 15
  minutos, una cruz sin cuerpo y después una roja que cierra.
- **Pregunta:** «En M15, una racha de velas verdes, una vela sin cuerpo y después la roja que cierra:
  ¿la roja marca el alto de las verdes, o la vela sin cuerpo corta la racha y no hay alto?
  - (a) marca el alto;
  - (b) la corta, y no hay alto;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si marca el alto, ¿el alto es el máximo de las verdes o puede ser la mecha de la vela sin cuerpo?
  - ¿Y si son dos o tres velas sin cuerpo seguidas?
  - En un bajo, con rojas, la cruz y una verde, ¿igual?
- **Para confirmar al final:** «En M15, una vela sin cuerpo entre la racha y la vela contraria ______
  la racha; el alto es ______; y en un bajo, ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05-MOTOR.md` §2.3; ADR-0085:65-68. Hoy, en M15, la
  vela sin cuerpo corta la racha (`domain/pivotes_m15.py:67-71`, `corta_la_racha`, el valor por
  defecto que usa M15): (b). En M1 ya no la corta (ADR-0085 §2). Sin parámetro: (a) pediría que M15
  use `no_cuenta`, con su ADR.*

### Bloque 2 · Donde el bot entra y tú no

En la clasificación de la corrida diaria del bot (P5 y P6, `RECORRIDA-CONSTRUCCION.md` §2.6), lo que
más separa al bot del trader es que el bot entra mucho donde él no.

**S-5. Después de la toma, un retroceso con alternancia y un punto nuevo limpio** · en parte
- **Lo que nos has dicho:**
  - «Entro en la zona, no número Sino entro en la zona en la que el precio llega a activar» (v15
    1:26:16, `ev-v15-012616-d534455a`);
  - «siempre el punto breaker al más reciente y el más reciente y que cumple con las condiciones» (v16
    0:14:45, `ev-v16-001445-7ca4f033`).
- **Lo que todavía no sabemos:** si, cuando el primer retroceso después de la toma tiene
  alternancia, entras en el punto siguiente cuando su retroceso sí está limpio.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo; dibujo 2): una compra. La toma
  de un bajo de M15. Después, un primer punto con un retroceso con alternancia de colores. Después,
  un punto nuevo más reciente, y su retroceso limpio, todo rojo.
- **Pregunta:** «Después de la toma, el primer retroceso tiene alternancia; aparece un punto nuevo y su
  retroceso está limpio. ¿Entras en este segundo?
  - (a) sí;
  - (b) no;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si entras, ¿pones la orden en el punto nuevo en cuanto aparece, o esperas a ver el retroceso
    entero?
  - ¿Y si entre los dos puntos el precio no vuelve a la zona del primero?
- **Para confirmar al final:** «Si el primer retroceso tras la toma tiene alternancia y aparece un
  punto nuevo con el retroceso limpio, ______ en el segundo».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05-MOTOR.md` §2.5, dibujo 2 (rehecho por la orden de
  cierre del consultor del 2026-10-27, punto 5). Hoy RN-009 descarta colocar con más zonas de control
  que `zonas_control_max_por_esquema` = 1 (`parametros.yaml:1013-1014`; `engine/zonas.py:504`); el
  punto nuevo con su retroceso limpio lleva detrás la zona del primero. Sin registro y sin ADR:
  RN-009 no cambia en esta rama.*

**S-6. La orden puesta en el primer punto que se llena antes de que haya alternancia** · en parte
- **Lo que nos has dicho:** las mismas dos frases de S-5 (`ev-v15-012616-d534455a`,
  `ev-v16-001445-7ca4f033`).
- **Lo que todavía no sabemos:** si una entrada que se llena con la primera vela del retroceso, antes
  de que se vea si el retroceso tiene alternancia, la das por buena.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo; dibujo 3): una compra. La toma
  de un bajo de M15. El primer punto tras la toma (un alto de M1, el 0 de la caja, arriba) y la orden
  puesta en él. La primera vela verde del retroceso pasa el punto y llena la orden; todavía no hay
  ninguna alternancia.
- **Pregunta:** «La orden ya está puesta en el primer punto tras la toma y se llena con la primera vela
  verde del retroceso, antes de que haya alternancia. ¿Esa entrada vale?
  - (a) sí;
  - (b) no, había que esperar al punto siguiente;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si vale, ¿la habrías puesto tú en ese punto antes de ver el retroceso?
  - ¿Cambia algo si la vela que llena es la primera después del punto o la tercera?
- **Para confirmar al final:** «Una orden en el primer punto tras la toma que se llena antes de que
  haya alternancia ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05-MOTOR.md` §2.5, dibujo 3;
  `RECORRIDA-CONSTRUCCION.md` §3 (las llenadas con menos de dos zonas de control). Hoy esa entrada
  ENTRA: la orden nace en el primer punto tras la toma y se llena antes de que exista la alternancia,
  y RN-009 solo muerde al colocar o recolocar con dos o más zonas ya formadas (ADR-0085:93-99). (b)
  pediría cambiar RN-009 o el momento en que nace la orden, con su ADR.*

**S-7. Gráfico 1**
- **Lo que nos has dicho:**
  - «Vale, puede haber que no hubo toma de liquidez de M15.» (v15 1:10:23,
    `ev-v15-011023-5f0f2dd1`);
  - «Solo me he saltado a lo mejor para cuando en una sesión había break events, me lo he saltado.»
    (v15 1:19:12, `ev-v15-011912-0ae32588`);
  - «si un día no se opera es porque estaba enfermo» (v15 1:19:56, `ev-v15-011956-dce80292`).
- **Lo que todavía no sabemos:** por qué, en días concretos en que el bot habría entrado, tú no
  entraste.
- **Pregunta, primero sin gráfico, y después con el gráfico limpio y con el gráfico con la línea:**
  «Aquí el bot habría entrado y tú no. ¿Por qué no entraste?
  - (a) no hubo toma de liquidez de M15;
  - (b) la zona no estaba limpia;
  - (c) la sesión iba a acabar en break even y me la salté;
  - (d) no operé ese día;
  - (e) otra, ¿cuál?»
- **Para precisar:**
  - ¿Qué habrías esperado ver para entrar aquí?
  - ¿Dónde habrías marcado tú la liquidez de M15 de esta sesión?
- **Para confirmar al final:** «En el gráfico 1 no entré porque ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.12; `RECORRIDA-CONSTRUCCION.md` §4. Los
  pasos (regla 2 de `SESION-DE-PREGUNTAS.md`): la pregunta en abstracto; el gráfico limpio
  (`grafico-1-limpio.svg`); el mismo con la línea (`grafico-1-marcado.svg`). **La línea es el nivel
  donde el bot pondría su orden de entrada; el gráfico acaba en la vela en que el bot da la liquidez
  por tomada; no hay stop, objetivo, llenado ni resultado.** Los días y la línea salen del bot con la
  cuenta reiniciada cada día (la corrida 2, diagnóstico); con la cuenta arrastrada (la que cuenta, la
  corrida 1) el bot no llena ninguna orden desde la última sesión del 20 de enero, por RN-032
  (`RECORRIDA-CONSTRUCCION.md:1295-1298`). Las velas son de Dukascopy y las suyas de Oanda: pueden
  diferir un poco (Technical Debt, «LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY»). Qué día es
  cada gráfico, solo en `clave.txt` (fuera del repo). Sin parámetro: es la deuda «el no_trade por
  ausencia» y la lista de S-14 de la sesión 5.*

**S-8. Gráfico 2**
- La misma pregunta que S-7, con el gráfico 2, en los tres pasos.
- **Para confirmar al final:** «En el gráfico 2 no entré porque ______».
- *Para Aleks (no va a la hoja): como S-7, con `grafico-2-limpio.svg` y `grafico-2-marcado.svg`.*

**S-9. Gráfico 3**
- La misma pregunta que S-7, con el gráfico 3, en los tres pasos.
- **Para confirmar al final:** «En el gráfico 3 no entré porque ______».
- *Para Aleks (no va a la hoja): como S-7, con `grafico-3-limpio.svg` y `grafico-3-marcado.svg`.*

**S-10. Gráfico 4**
- La misma pregunta que S-7, con el gráfico 4, en los tres pasos.
- **Para confirmar al final:** «En el gráfico 4 no entré porque ______».
- *Para Aleks (no va a la hoja): como S-7, con `grafico-4-limpio.svg` y `grafico-4-marcado.svg`.*

**S-11. Gráfico 5**
- La misma pregunta que S-7, con el gráfico 5, en los tres pasos.
- **Para confirmar al final:** «En el gráfico 5 no entré porque ______».
- *Para Aleks (no va a la hoja): como S-7, con `grafico-5-limpio.svg` y `grafico-5-marcado.svg`.*

**S-12. Gráfico 6**
- La misma pregunta que S-7, con el gráfico 6, en los tres pasos.
- **Para confirmar al final:** «En el gráfico 6 no entré porque ______».
- *Para Aleks (no va a la hoja): como S-7, con `grafico-6-limpio.svg` y `grafico-6-marcado.svg`. Si
  un gráfico no se puede enseñar, `clave.txt` trae dos de reserva con su código libre.*

### Bloque 3 · El resto

**S-13. Cuándo pasas el stop a la entrada: al toque o al cierre de la vela de M1** · en parte · A-13
- **Lo que nos has dicho:**
  - «Sí, o sea, apenas toca. [...] yo siempre lo he estado trabajando, o sea, apenas toca» (v6
    0:57:01, `ev-v6-005701-7ae2b8d3`);
  - «cae ya apenas cierra por debajo estoy si lo hace con cuerpo mucho mejor entonces nosotros la
    entrada ya la pondríamos en break even» (v10 2:04:53, `ev-v10-020453-2d41dd25`);
  - en la sesión 5, en la misma respuesta: «tiene que cerrar por debajo o sea, con mecho o con
    cuerpo» (v15 1:35:10, `ev-v15-013510-6364e7e0`) y «inmediatamente apenas toque que se pone en
    break y en la entrada» (v15 1:36:05, `ev-v15-013605-c041b814`).
- **Lo que todavía no sabemos:** cuál de las dos es la tuya: al toque o al cierre de la vela.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra ya llenada; el
  precio sube, hace un retroceso (la zona de control) y vuelve a subir hacia el máximo de esa zona;
  una vela de M1 toca ese máximo con la mecha y cierra por debajo; la siguiente cierra por encima.
- **Pregunta:** «Cuando pasas el stop a la entrada, ¿lo haces en cuanto el precio toca el nivel o
  esperas a que cierre la vela de M1 más allá?
  - (a) al toque;
  - (b) al cierre de M1;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si es al cierre, ¿basta con que la mecha pase el nivel, o tiene que cerrar el cuerpo más allá?
  - En venta, ¿lo mismo al revés?
- **Para confirmar al final:** «Paso el stop a la entrada ______ (al toque / al cierre de M1), y si es
  al cierre, la vela tiene que ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.3. Hoy `break_even_condicion` = `tocar`,
  CONFIRMED (`parametros.yaml:931-932`), y el bot lo vigila al tick (`engine/cableado.py:320-326`); la
  ruptura de la zona con mecha (`break_even_criterio_ruptura` = `mecha`, `:476-477`). (a) → `tocar`
  (lo de hoy); (b) → `cierre`, y la primera subpregunta decide `mecha` o `cuerpo`. «Después el stop no
  se mueve» ya es firme (`knowledge/spec/ambiguedades.yaml:206-209`): no se pregunta.*

**S-14. La orden sin llenar cuando el precio toma otra liquidez de M15** · en parte · A-53
- **Lo que nos has dicho:**
  - «si tengo que elegir alguna opción, la dejo y la muevo cuando aparezca el nuevo punto de
    liquidez» (v10 1:58:31, `ev-v10-015831-fb95edf0`);
  - «Mientras no aparece el punto nuevo Se presiona la orden vieja ¿La operación vale? Sí, vale» (v10
    2:01:14, `ev-v10-020114-55bdf502`);
  - «es indiferente el tiempo» (v15 1:08:18, `ev-v15-010818-cc8e1e08`) y «la orden se actualiza en m1
    conforme se va desarrollando pues un nuevo punto» (v15 1:08:50, `ev-v15-010850-f0728663`);
  - y si el extremo nuevo queda muy lejos: «si el máximo nuevo queda muy lejos cambia algo es no es
    indiferente si el máximo es demasiado lejos o no» (v10 0:50:56, `ev-v10-005056-1a55d5b4`, que lo
    lee como «no cambia nada»), y «en una compra es lo mismo con un nuevo mínimo? Sí, es lo mismo»
    (v10 0:51:16, `ev-v10-005116-2a9ff066`).
- **Lo que todavía no sabemos:** la letra. En la sesión 4, en la misma frase, dijiste también «La A es
  verdadera», y en la sesión 5 la letra no se oyó bien.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos en el dibujo): una compra. La orden
  puesta en un punto, sin llenar. El precio baja, toma otro bajo de M15 (cierra con cuerpo por
  debajo) y más tarde aparece un punto nuevo.
- **Pregunta:** «Tienes una orden stop puesta, sin llenar, y el precio toma otra liquidez de M15.
  ¿Qué haces con la orden?
  - (a) la quito en ese momento y espero el punto de la liquidez nueva;
  - (b) la dejo, y la muevo cuando aparezca el punto de la liquidez nueva;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Es igual en compra y en venta?
  - ¿Y si antes de que aparezca el punto nuevo el precio toma todavía otra liquidez?
- **Para confirmar al final:** «Con la orden sin llenar, si el precio toma otra liquidez de M15, la
  orden ______; y si se llena antes de que aparezca el punto nuevo, la operación vale».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.4, **sin sus dos subpreguntas, que ya
  están contestadas** (D3 del encargo: no se repite): «si el 1 baja mucho» es el «máximo demasiado
  lejos» de la sesión 4 en espejo («en una compra es lo mismo», `ev-v10-005116-2a9ff066`), y «si se
  llena antes del punto nuevo, ¿vale?» es `ev-v10-020114-55bdf502`; las dos van a «Lo que nos has
  dicho» y a la confirmación. Hoy `orden_pendiente_al_abrir_escenario` = `se_mueve`,
  DEFAULT_AMBIGUOUS bajo A-53 (`parametros.yaml:854-855`; `engine/zonas.py:284-286`). (a) →
  `se_retira` (`engine/primitivas_broker.py:717`); (b) → `se_mueve` (lo de hoy). La candidata C1 (la
  orden con una caja nueva) la responde `ev-v10-015716-5ea2575f` con ADR-0074.*

**S-15. La misma liquidez tomada antes de las 7 y otra vez después** · en parte · A-43
- **Lo que nos has dicho:**
  - «si el precio toma ese liquidez antes de tu horario, ¿lo usas para operar a partir de las 7? Sí.»
    (v10 1:46:13, `ev-v10-014613-6cf002b2`);
  - «para confirmar al final si una liquidez se toma antes de las 7 y otra después, mi toma es la más
    reciente» (v15 0:51:26, `ev-v15-005126-5baccf2a`).
- **Lo que todavía no sabemos:** qué pasa cuando es la MISMA liquidez la que se toma dos veces: antes
  de las 7 y otra vez después.
- **Esquema inventado, no es un día real** («M15» escrito, y la línea de las 07:00 en el dibujo): un
  bajo de M15; una vela que lo cruza con cuerpo antes de la línea de las 7; el precio vuelve por
  encima; y otra vela que lo cruza con cuerpo después de las 7.
- **Pregunta:** «La MISMA liquidez de M15 se toma antes de las 7 y el precio vuelve y la toma otra vez
  después de las 7. ¿La segunda toma vale para operar?
  - (a) sí;
  - (b) no, solo cuenta la primera;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si solo cuenta la primera, ¿operas a partir de las 7 con ella, o ya no operas esa liquidez?
  - ¿Cambia algo si el precio vuelve muy por encima del nivel entre las dos tomas?
- **Para confirmar al final:** «Si la misma liquidez se toma antes de las 7 y otra vez después, opero
  con ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.5. Hoy la toma de antes de las 7 cuenta
  (`toma_antes_de_la_ventana` = `cuenta`, CONFIRMED, `parametros.yaml:788-789`;
  `engine/primitivas.py:304-309`), y la segunda toma del mismo pivote no abre escenario nuevo
  (`engine/zonas.py:292-294`): el bot opera desde las 7 con la primera. (a) y (b) con «opero desde las
  7 con ella» no cambian nada; (b) con «ya no opero esa liquidez» pediría una opción nueva con su
  ADR.*

**S-16. Los dos extremos de la caja: qué velas dan el 1** · en parte · A-48 y A-49
- **Lo que nos has dicho:**
  - «se traza desde el posible punto de breaker, o sea el punto de breaker hasta el punto más alto»
    (v9 0:47:21, `ev-v9-004721-2e023ac6`);
  - «esperamos el cierre, o sea, sea una vela verde o una vela roja, entonces trazaríamos el nivel 0
    desde aquí y el nivel 1 desde el punto más alto, donde cierra,» (v15 0:32:44,
    `ev-v15-003244-dcd8a834`);
  - «como estamos en un flujo alcista vamos utilizando el 1 conforme va desarrollándose.» (v15
    0:36:19, `ev-v15-003619-9fbc7f08`).
- **Lo que todavía no sabemos:** de qué velas sale el 1: solo de la última vela contraria, de las
  contrarias seguidas, o de todas las velas desde el punto.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo; el 0 NO está en el último bajo
  del dibujo): una venta. El punto, un bajo de M1 (el 0, abajo). Después, dos velas verdes seguidas,
  una roja pequeña, otra verde y la vela que rompe el punto. Las cinco velas tienen máximos distintos,
  y el más alto es el de la primera verde.
- **Pregunta:** «En este dibujo, el 0 de la caja es este punto. ¿Hasta dónde llevas el 1?
  - (a) al máximo de la última vela verde antes de la ruptura;
  - (b) al máximo de las verdes seguidas que acaban en esa última;
  - (c) al punto más alto de todas las velas desde el punto;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - ¿Trazas la caja cuando cierra la vela que rompe, o mientras se forma?
  - En una compra, al revés (el 0 arriba y el 1 abajo), ¿igual?
- **Para confirmar al final:** «El 0 de la caja va en el punto; el 1, en ______; trazo la caja
  ______ (al cierre / mientras se forma), y mientras no aparece otro punto, el 1 ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.6, con el esquema cambiado: el 0 no va en
  el último alto ni bajo de M1, lo que no entendió en la sesión 5. Hoy: `caja_bloque` = `r6`,
  DEFAULT_AMBIGUOUS bajo A-48 (`parametros.yaml:708-709`, descripción :698-706); `caja_se_fija` =
  `en_cada_cierre_m1` bajo A-49 (`:735-736`; `engine/zonas.py:389`); `orden_stop_punto` =
  `ultimo_pivote_m1` bajo A-48 (`:687-688`). (a) → `r1`; (b) → `r4`; (c) → `r6` (lo de hoy).
  «Al cierre» y «el 1 se va actualizando» casan con `en_cada_cierre_m1` (ADR-0074, sesión 4 S-4).*

**S-17. Frente al nivel tomado: solo el 0 o la caja entera** · en parte · A-50
- **Lo que nos has dicho:** «si el 0 queda justo en la la línea ni por encima ni por debajo eso es
  indiferente aquí no está por debajo pero es indiferente o sea el cero en este caso está por encima
  pero lo importante es eso o sea validar correctamente nuestro posible breaker» (v15 1:04:51,
  `ev-v15-010451-5b123278`), y que en una compra la caja «queda por debajo» (v15 1:01:04,
  `ev-v15-010104-23adba23`).
- **Lo que todavía no sabemos:** cuál de estas dos cajas descartas.
- **Esquemas inventados, no son días reales** (los dos con «M1» escrito y la línea del bajo de M15
  tomado): una compra. **Dibujo A:** el 0 (arriba) queda por encima de la línea y el 1 (abajo), por
  debajo: la caja a caballo. **Dibujo B:** la caja entera, el 0 y el 1, por encima de la línea.
- **Pregunta:** «En esta caja el 0 queda del lado de ruido pero el 1 no; en esta otra la caja entera
  queda del lado de ruido. ¿Cuál descartas?
  - (a) las dos;
  - (b) solo la que queda entera;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Importa cuánto se pasa el 0 de la línea?
  - Si descartas la de la caja entera, ¿esperas otra caja de ese mismo punto o dejas el punto?
- **Para confirmar al final:** «Frente al nivel tomado, descarto la caja cuando ______ queda del lado
  de ruido».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.7 = `ACTIVAR-SESION-05-MOTOR.md` §2.7.
  RN-005: en una compra la caja va por debajo del bajo tomado, y el lado de ruido es el de encima
  (`engine/zonas.py:553-554`). Hoy `caja_lado_de_ruido` = `caja_entera`, DEFAULT_AMBIGUOUS bajo A-50,
  lectura del consultor (`parametros.yaml:762-763`; `engine/zonas.py:548-558`): descarta B y no A.
  (a) → `solo_el_0`; (b) → `caja_entera` (lo de hoy); «ninguna» → otra, con ADR. «Compra y venta»
  ya lo contestó en la sesión 5 (S-12b): no se pregunta.*

**S-18. Las reentradas en el mismo punto** · en parte · ADR-0083
- **Lo que nos has dicho:**
  - «Sí, serían tres intentos por liquidez. [...] ¿El máximo es por día? No, no, por liquidez.»
    (sesión 3, v9 1:30:54, `fb-2026-09-29-sesion-03-68a21dc0`);
  - «O sea, solo vemos el punto, si te das cuenta El punto 1 Que allí, solo que Se actualiza del nivel
    0 Allí abajo, y ya está Entonces, claro, aquí sigue marcando el mismo nivel» (v15 0:24:41,
    `ev-v15-002441-2e609b87`);
  - «un posible punto breaker tiene que haber roto por encima porque si no está roto por encima,
    nosotros no lo validamos» (v15 0:27:29, `ev-v15-002729-30480ec5`);
  - y de los break even: «me da unas ganas de replantearme para poder quitar esa condicional cuando
    hay break even» (v15 0:20:29, `ev-v15-002029-1ac081ae`).
- **Lo que todavía no sabemos:** cuántas veces vuelves a entrar en el mismo punto después de un stop, y
  si después de un break even vuelves.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una venta. Un punto (un bajo
  de M1); una primera entrada que va al stop; el precio vuelve a romper el mismo punto.
- **Pregunta:** «Tras un stop en un punto, ¿cuántas veces vuelves a entrar en ese mismo punto?
  - (a) una más;
  - (b) hasta agotar los tres intentos de esa liquidez;
  - (c) ninguna;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - Tras un break even en ese punto, ¿vuelves a entrar en él? (a) sí; (b) no; (c) otra, ¿cuál?
  - Al volver a entrar, ¿qué haces con el 0 y con el 1 de la caja?
- **Para confirmar al final:** «Tras un stop en un punto, vuelvo a entrar en él ______ veces; tras un
  break even, ______; y al volver a entrar, el 0 ______ y el 1 ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.8. ADR-0083 es PROVISIONAL en D1. Hoy, tras
  una pérdida o un break even, el punto se vuelve a colocar, con la misma caja o con otra
  (`engine/zonas.py:41-49`, `liberar_usada` en `:438`, llamada en `engine/cableado.py:167`), hasta
  los 3 cartuchos por liquidez (`cartuchos_max`, `parametros.yaml:1039-1040`): (b), también tras un
  break even. (a) o (c), o «no tras un break even», piden ADR que enmiende ADR-0083.*

**S-19. El precio ya está más allá del 0 cuando se forma la caja**
- **Lo que nos has dicho:** — (no se resolvió en la sesión 5; se pregunta sobre el esquema rehecho).
- **Lo que todavía no sabemos:** qué haces si, cuando la caja ya está formada, el precio ya ha pasado
  el 0.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra. El punto (el 0,
  arriba) y la caja; cuando cierra la vela con la que se forma la caja, el precio ya está por encima
  del 0.
- **Pregunta:** «Cuando la caja se forma y el precio ya está más allá del 0, ¿pones la orden igual?
  - (a) sí, en el 0;
  - (b) no, espero otra caja;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si pones la orden igual, ¿con qué tipo de orden, si el precio ya está por encima?
  - ¿Cambia algo si el precio está solo un punto más allá, o muy lejos?
- **Para confirmar al final:** «Si al formarse la caja el precio ya está más allá del 0, ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.9 (S-16 de la sesión 5, «no resuelve»).
  Hoy la orden stop de compra por debajo del precio es del lado equivocado y el bróker la rechaza
  (`engine/broker.py:541-542`, ADR-0057), y ese rechazo gasta el punto (ADR-0083;
  `engine/zonas.py:41-44`): (b), sin parámetro. (a) pediría otro tipo de orden, con su ADR.*

**S-20. La vela de 1 o 2 puntos en el retroceso, y la vela sin cuerpo con mechas largas** · en parte
- **Lo que nos has dicho:**
  - del retroceso: «casi no tiene un cuerpo, uno o dos puntos igual, o sea, no pasa nada simplemente
    no se toma en cuenta» (v16 0:08:51, `ev-v16-000851-f5ae3b6f`);
  - del punto: «las 3 son válidas para trazar un punto breaker … sea un punto, dos puntos o 12
    puntos, sirve para nosotros poder trazar» (v16 0:27:46, `ev-v16-002746-31cbc565`), y «tiene que
    ser cero puntos … tiene que ser plana totalmente» (v16 0:28:41, `ev-v16-002841-8cfe382a`).
- **Lo que todavía no sabemos:** en el retroceso, si una vela de 1 o 2 puntos de cuerpo cuenta como
  cambio de color, cuando para trazar el punto sí cuenta.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra. El retroceso,
  rojo, con una vela verde de un punto de cuerpo en medio; y más allá una vela sin cuerpo con mechas
  largas.
- **Pregunta:** «En el retroceso, ¿una vela de 1 o 2 puntos de cuerpo cuenta como cambio de color?
  - (a) sí;
  - (b) no, como si no tuviera cuerpo;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - «Una vela sin cuerpo con mechas largas, ¿cuenta como si no existiera o miras sus mechas? (a) como
    si no existiera; (b) miro las mechas; (c) otra, ¿cuál?»
  - Si cuenta como si no tuviera cuerpo en el retroceso, ¿la sigues usando para trazar el punto?
- **Para confirmar al final:** «Una vela de 1 o 2 puntos de cuerpo, en el retroceso, ______ como
  cambio de color; para trazar el punto, ______; y de una vela sin cuerpo, sus mechas ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.10; el valor de hoy, de
  `ACTIVAR-SESION-05-MOTOR.md` §2.2 y §2.6. Las dos son DECISIÓN DEL CONSULTOR (ADR-0085:72-78): la
  vela de 1 o 2 puntos sigue siendo de su color (`domain/pivotes_m15.py:91-97`, `color`: cualquier
  cuerpo tiene color), (a); y la mecha de la vela sin cuerpo cuenta donde cuenta (romper un nivel, el
  1 de la caja), (b) de la subpregunta. Sin parámetro: lo contrario pide ADR. La pregunta principal
  es una sola; la de la vela sin cuerpo va en «Para precisar» con sus opciones (desviación declarada
  en el informe).*

**S-21. El punto de breaker roto con la mecha después de una alternancia** · en parte
- **Lo que nos has dicho:**
  - «siempre el punto breaker al más reciente y el más reciente y que cumple con las condiciones»
    (v16 0:14:45, `ev-v16-001445-7ca4f033`);
  - «no importa el color de la vela que rompe, puede ser una vela verde que ha hecho luego un
    retroceso pero ha sacado su mecha y ha tocado o sea ha roto esto el punto breaker entonces se
    valida» (v16 0:18:34, `ev-v16-001834-732a76b6`).
- **Lo que todavía no sabemos:** qué pesa más cuando las dos cosas se dan juntas: la mecha que rompe o
  la alternancia que hubo antes.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra. El retroceso con
  alternancia de colores; después, una vela roja que rompe el punto, el más reciente, solo con la
  mecha.
- **Pregunta:** «Si una vela de color contrario rompe el punto con la mecha pero antes hubo
  alternancia de colores, ¿qué pesa más: la mecha que rompe o la alternancia?
  - (a) la mecha, y entro;
  - (b) la alternancia, y no entro;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si la alternancia es de una sola vela?
  - En venta, al revés, ¿igual?
- **Para confirmar al final:** «Si el punto se rompe con la mecha después de una alternancia,
  ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.11; ADR-0076 §4, pregunta 2, y
  ADR-0085:87-91 (la única fila DISTINTO que queda). Hoy la mecha vale para romper en M1 (A-32
  RESUELTA) y la alternancia da dos zonas de control, que RN-009 descarta al colocar
  (`zonas_control_max_por_esquema` = 1, `parametros.yaml:1013-1014`; `engine/zonas.py:504`): (b).
  Sin parámetro: (a) pide ADR.*

**S-22. Para que el máximo de la verde sea tu punto, ¿qué tiene que hacer la roja?** · en parte
- **Lo que nos has dicho:** «tiene que cumplir esa condicional de que el precio, pues, haya venido de
  un order flow bajista. Esto haya llegado hasta aquí por debajo, aquí puede haber todas las velas
  que quiera, no pasa nada, pero luego nos tiene que romper, o sea, tiene que cerrar por debajo.»
  (v15 0:40:37, `ev-v15-004037-a2ab3980`).
- **Lo que todavía no sabemos:** si la roja tiene que cerrar por debajo del mínimo de la verde, o
  basta con que sea roja; y si hace falta que el precio venga bajando.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): el precio viene bajando; una
  vela verde; después una roja que cierra dentro del cuerpo de la verde, sin pasar su mínimo.
- **Pregunta:** «Para que el máximo de la verde sea punto de breaker, ¿la roja de después tiene que
  cerrar por debajo del mínimo de la verde, o basta con que sea roja?
  - (a) basta con que sea roja;
  - (b) tiene que cerrar por debajo;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y hace falta que el precio venga de un flujo bajista?
  - Si tiene que cerrar por debajo, ¿vale que lo pase solo con la mecha?
- **Para confirmar al final:** «El máximo de la verde es mi punto cuando la roja de después ______ y
  el precio ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05-MOTOR.md` §2.4. La condición de
  `ev-v15-004037-a2ab3980` no se aplica, DECISIÓN DEL CONSULTOR (ADR-0085:79-83): el motor forma el
  punto con cualquier roja que cierra tras una racha verde, sin flujo previo: (a). (b) con «cerrar»
  sería pedir cuerpo en M1, contra A-32 RESUELTA («en M1 la mecha siempre vale»,
  `ev-v16-000234-9a4fa375`): si lo elige, hay que preguntarle cómo casa con eso, y pide ADR.*

### Bloque 4 · La confirmación corta y «Para cerrar»

**S-23. Una toma de la mañana, y por la tarde el mismo sesgo** · en parte · A-46
- **Lo que nos has dicho:** «Si hay una continuidad de sesgo, sí. Pero si no, no. Esa es la respuesta
  que daría.» (v15 0:58:39, `ev-v15-005839-f2e43c27`); y en la sesión 3, de las dos sesiones del
  día: «cada uno es un mundo diferente» (`fb-2026-09-29-sesion-03-5021677e`, v9 0:32:53).
- **Lo que todavía no sabemos:** si, con el MISMO sesgo por la tarde, la toma de la mañana te vale
  para operar la tarde, o cada sesión espera su propia toma.
- **Esquema inventado, no es un día real** («M15» escrito, y la línea entre las dos sesiones en el
  dibujo): un día con el mismo sesgo de 4 horas en las dos sesiones; la toma de M15 en la primera, y
  ninguna en la segunda.
- **Pregunta:** «Una toma de la mañana, y en la tarde el MISMO sesgo: ¿esa toma vale para operar en la
  tarde?
  - (a) sí, si el sesgo sigue igual;
  - (b) no, cada sesión espera su propia toma;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si vale, ¿y si en la mañana ya operaste esa toma?
- **Para confirmar al final:** «Con el mismo sesgo por la tarde, la toma de la mañana ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-05.md` §3.13 (respuesta a la PARADA 2, punto 0
  (b)). A-46 está RESUELTA y no se toca: hoy una toma de una sesión anterior del día no cuenta
  (`engine/primitivas.py:286-287` y `:310`): (b). Si contesta (a), A-46 se REABRE con un registro
  `REOPEN` (`docs/runbooks/AMBIGUEDADES.md`).*

**Para cerrar** (sin código de voz)
- **Diciembre:** «¿Grabaste el backtest de diciembre con tu voz, en vídeo?». Lo que dijo: «Sí, sí, sí,
  lo grabo tal cual» (v16 0:32:28, `ev-v16-003228-b515b93e`). *Si ya lo contestó por WhatsApp, se
  salta.*
- **Agosto:** «¿Nos pasas la exportación del backtest de agosto grabado en vídeo?». Lo que dijo: «Sí,
  lo tiene, creo que sí está, bro» (v16 0:32:49, `ev-v16-003249-49af3f8b`). *Si ya lo contestó por
  WhatsApp, se salta.*
- *Para Aleks (no va a la hoja): NA:I y NA:Q de `PROJECT_STATE.md`. Sin fechas de días.*

## 2. Lo que no va a la hoja

Lo que el barrido dejó fuera, con su porqué, está en `docs/validation/BARRIDO-SESION-6.md` §1.a y
§1.b: las ambigüedades de medición (A-16, A-28, A-54, A-55, A-56), las candidatas C4, C5, C6 y C7, los
dos CORRECT de RN-003 pendientes (el falso positivo de G.2), la pregunta de ADR-0086 (descartada por
el consultor) y S-25 de la sesión 5 (la mide T).
