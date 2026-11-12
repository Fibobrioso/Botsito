# Sesión 7b (sesion-08) con el trader: las preguntas y el bloque de días

Rama `trabajo/preparacion-sesion-7`, 2026-11-11, desde `main` en `e6b073f`. El método es el de
ADR-0093; el reparto, los días y las filas, de `docs/validation/PREPARACION-SESION-7.md` (§0.3 y
§0.4, con la respuesta del consultor a la PARADA de la fase 0). Es el segundo día de la sesión 7,
**7b (sesion-08)**; el primero, **7a (sesion-07)**, está en `docs/sesion-7/PREGUNTAS-7A.md`.

> **RECUADRO (2026-11-11, encargo de `trabajo/preparacion-sesion-7`, D4).** Las láminas de la 7b
> **no se generan en la rama de la preparación**: el bot cambia al activar la 7a, y la lámina tiene
> que enseñar lo que hace el bot que el trader va a corregir. Las genera con `motor laminas` la rama
> de activación de la 7a, con su motor, y **esa rama revisa este documento antes de la grabación**:
> lo que la 7a haya contestado o cambiado, las filas de cada pregunta con la corrida nueva, y si
> alguna de §3 (las que no caben) entra en lugar de otra. Esa rama pasa también `SESION_EN_CURSO` de
> `scripts/transcribir_sesion.py` a "08".

**La hoja es el PDF del consultor**, hecho con este documento, como en las sesiones 4 a 6. No sale
de `kit hoja` ni de `scripts/hoja_preguntas.py`. Al PDF van, de cada pregunta: el título, «Lo que
nos has dicho», «Lo que todavía no sabemos», la pregunta con sus opciones, «Para precisar» y «Para
confirmar al final». **No van al PDF**: las líneas «Para Aleks», el §1 (el bloque de días) y el §3.

**Los códigos S-1 a S-7 son de la 7b (sesion-08)**: S-1 a S-6, las técnicas; S-7, la pregunta de
material del final. No son los de la 7a. Cada pregunta se abre diciendo en voz «pregunta» y su
código («pregunta ese uno» … «pregunta ese siete») y se cierra con «fin de pregunta». Sus textos ya
están en `scripts/transcribir_sesion.py` (`CODIGOS_DE_SESION_TEXTO["08"]`).

**Cómo se leen:** como en la 7a (`PREGUNTAS-7A.md`, «Cómo se leen»): cerradas, con «otra, ¿cuál?»
en todas; esquemas inventados rotulados, con el marco escrito y lo de antes dibujado; el 0 de la
caja es el punto de la orden y el 1 el extremo del lado del stop; nada en dinero; las horas en el
reloj de Madrid; ninguna pregunta técnica lleva días ni fechas.

## 0. Qué se abrió (exposición)

- Evidencia y feedback de `knowledge/evidence/` y `knowledge/feedback/` citados abajo; los anexos
  commiteados de RECORRIDA-CONSTRUCCION-2. Ninguna transcripción cruda, ningún fotograma, ningún
  libro, ningún caso. Declarado en `docs/validation/HOLDOUT-EXPOSICIONES.md`, filas del 2026-11-11
  de esta rama.

## 1. El bloque de días (Para Aleks: no va al PDF)

Va **después** de las seis preguntas técnicas, y la pregunta de material (S-7) al final de todo
(ADR-0093 §2). Los días cumplen ADR-0093 §3, comprobados por la compuerta
(`PREPARACION-SESION-7.md` §0.4; `anexos/PREPARACION-SESION-7/dias-d3.txt` y `sustitutas.txt`).
**Sus láminas no existen todavía** (recuadro de arriba).

| Orden | Sesión | Sirve a | Filas de la clasificación (trader / bot) |
|---|---|---|---|
| 1 | 2026-01-13, 07-11 | S-1 (la caja: cociente 2,33 con el stop fuera y 2,07 en la entrada) | 8 (1 / 7) |
| 2 | 2026-04-15, 11-15 | el trader no opera y el bot sí (S-6 de la 7a); S-1 | 5 (0 / 5) |
| 3 | 2026-01-07, 07-11 | S-1 (cociente 3,14 con el stop fuera) | 4 (1 / 3) |
| 4 | 2026-01-19, 11-15 | S-1 (cociente 1,78 en la entrada) | 3 (3 / 0) |
| reserva | 2026-01-21, 07-11 | S-1 (cociente 0,50 en la entrada) | 3 (2 / 1) |
| reserva | 2026-01-22, 11-15 | el sesgo de H4 por una ruptura de 2 puntos (toca A-16) | 3 (3 / 0) |
| reserva | 2026-07-16, 07-11 | S-1 (cociente 0,34 con el stop fuera; es una pareja) | 1 (1 / 0) |

Las tres primeras de enero y la de abril no tienen vídeo del trader: el bloque de días es la
primera vez que se le oye operarlas.

**Por cada sesión**, los pasos de `PREGUNTAS-7A.md` §1 (ADR-0093 §2): Aleks comprueba el día y se lo
dice; el trader abre él mismo el replay, antes de compartir pantalla, en una sesión de replay nueva,
sin marcas, backtests ni Analytics; la opera con voz; después ve las láminas del bot de esa sesión,
sin fecha, sin nada posterior al corte y sin ningún resultado; corrige, y «¿siempre, solo en este
caso, o de qué depende?»; si aparece otro backtest, Analytics o un mes reservado, se reconduce y el
tramo es no citable el mismo día.

## 2. Las preguntas (6 técnicas y una de material)

Ordenadas por las filas que mueven (ADR-0093 §1); A-53 y A-43 no tienen recuento por fila.

**S-1. Dónde pones el 0 de tu caja** · en parte · A-48
- **Lo que nos has dicho:**
  - del 1: «entonces la respuesta sería al punto más alto de todas las velas desde el punto» (v17
    1:05:41, `ev-v17-010541-05a69879`);
  - «Una compra al revés, exactamente como lo hemos visto en el gráfico, sería el arriba del 0 y el 1
    abajo.» (v17 1:13:28, `ev-v17-011328-a701a547`).
- **Lo que todavía no sabemos:** de dónde sale el 0, el punto de la orden: si del último pivote de
  M1 o de la vela de la toma.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos): la toma de M15 en una venta;
  después el retroceso en M1 con su último pivote; la vela de la toma, con su propio pivote en otro
  sitio; dos posibles 0 rotulados A (el último pivote de M1) y B (el de la vela de la toma), y el 1
  dibujado igual para los dos.
- **Pregunta:** «¿Dónde pones el 0?
  - (a) en A;
  - (b) en B;
  - (c) en otro sitio, ¿cuál?»
- **Para precisar:** ¿Lo haces igual en una compra, al revés?
- **Para confirmar al final:** «Mi 0 es ______; el 1 es el punto más alto de todas las velas desde el
  punto, y el stop va a 0,8 de la caja».
- *Para Aleks (no va a la hoja): RECORRIDA-CONSTRUCCION-2.md:1335-1339 («¿de qué sale tu stop?») y
  `ACTIVAR-SESION-06.md:591-592` (el 0 de A-48). **El 1 está decidido y no se pregunta**:
  `caja_bloque` = `r6`, CONFIRMED (`parametros.yaml:726`; `ambiguedades.yaml:1557-1565`). A-48 sigue
  ABIERTA por el 0: `orden_stop_punto` = `ultimo_pivote_m1`, DEFAULT_AMBIGUOUS, lectura del consultor
  (`parametros.yaml:702`, opciones `ultimo_pivote_m1` y `referencia_de_la_toma`). (a) →
  `ultimo_pivote_m1` (lo de hoy); (b) → `referencia_de_la_toma`. La caja está DISPERSA en los dos
  sentidos (cociente entre la distancia entrada-stop del bot y la del trader de 0,21 a 9,25, mediana
  0,83; `caja-stop.txt`), así que no se pregunta «¿más lejos o más cerca?». Filas: julio 16 con el
  stop fuera y 7 P2 a 4-10 puntos; en total 44 y 24. Sesiones del bloque: 1, 3 y 4 (y las reservas
  2026-01-21 y 2026-07-16). (Hasta la revisión de la rama, esta pregunta lo era del 1, que ya está
  decidido: revisor, b1.)*

**S-2. Para que el máximo de la verde sea tu punto, qué tiene que hacer la roja** · en parte · S-22
- **Lo que nos has dicho:**
  - «porque tendría que el precio haber roto aquí con cuerpo o con mecha cualquiera de los dos para
    yo poder validar este punto breaker» (v17 1:53:07, `ev-v17-015307-0870a8ca`);
  - «la roja cierra dentro de la verde sin pasar su mínimo pues en este caso no podríamos nosotros o
    sea si desde este contexto de aquí no podríamos nosotros trazar aquí como un punto breaker» (v17
    1:53:18, `ev-v17-015318-1256caf7`).
- **Lo que todavía no sabemos:** si el último pivote no cumple, si vale el de antes o no hay punto; y
  si la roja tiene que pasar el mínimo de la última vela verde o el de toda la racha.
- **Esquema inventado, no es un día real** («M1» escrito): una racha de tres velas verdes; una roja
  que pasa el mínimo de la última verde, pero no el de la primera.
- **Pregunta:** «¿El máximo de la última verde es tu punto?
  - (a) sí: basta con pasar el mínimo de la última verde;
  - (b) no: tiene que pasar el mínimo de toda la racha;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si la roja no pasa ningún mínimo, ¿vale el punto de antes, o no hay punto?
  - ¿Basta con que lo pase con la mecha?
- **Para confirmar al final:** «El máximo de la verde es mi punto cuando la roja ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06-MOTOR.md:791` (decisión 2) y `ACTIVAR-SESION-06.md:606-608`.
  La frase de la mecha, con un «m15» dudoso: `ev-v17-015404-06ac0e9d`. Hoy el punto se forma con
  cualquier roja que cierra tras una racha verde (ADR-0085 §3; `domain/estructura_m1.py`,
  `ultimo_punto_de_ruptura`). La regla que pide quita el 52 % de los puntos de breaker con (a) y el
  69 % con (b) (`ACTIVAR-SESION-06-MOTOR.md:148-154`); va en rama propia con ADR. Sin recuento por
  fila.*

**S-3. El precio ya está más allá del 0 cuando se forma la caja** · en parte · S-19
- **Lo que nos has dicho:**
  - «si, o sea, se pone la orden igual, aquí ya se activaría la orden, es más, o sea, al ocurrir este
    rompimiento de aquí, ya a mí me habilita» (v17 1:41:03, `ev-v17-014103-8cf3e7fb`);
  - «con qué tipo de orden pues estamos trabajando el stop order si el precio está por encima vamos
    actualizando o sea el nivel de caja» (v17 1:42:35, `ev-v17-014235-f3375358`);
  - «como digo este 0 el el nivel del cero se tiene que ir actualizando conforme se vaya
    desarrollando, pues, nuevos, en este caso, serían nuevos altos.» (v17 1:43:50,
    `ev-v17-014350-ec133d13`).
- **Lo que todavía no sabemos:** si la orden entra, si esperas a que el 0 quede del lado bueno, o si
  la descartas.
- **Esquema inventado, no es un día real** («M1» escrito): una compra; cuando se forma la caja, el
  precio ya está por encima del 0.
- **Pregunta:** «¿Qué haces con la orden?
  - (a) entro, aunque el precio ya esté por encima del 0;
  - (b) espero a que el 0 quede del lado bueno y entonces la pongo;
  - (c) la descarto;
  - (d) muevo el 0 a los nuevos altos y pongo la orden ahí;
  - (e) otra, ¿cuál?»
- **Para precisar:** ¿Y si el precio vuelve por debajo del 0 antes de que pongas la orden?
- **Para confirmar al final:** «Si el precio ya está más allá del 0, ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06-MOTOR.md:792` (decisión 3: hasta la sesión 7,
  con la lectura del consultor apuntada: si dice «espero», 3.a y 4.a) y `:803`. Hoy la stop del lado
  equivocado se rechaza (`precio_invalido`, `engine/broker.py:543-555`) y el rechazo gasta el punto
  (ADR-0083 D1). (a) → colocar o entrar aunque el precio esté pasado el 0 (motor nuevo, con ADR);
  (b) → 3.a y 4.a de ACTIVAR-SESION-06-MOTOR (esperar a que el 0 quede del lado bueno); (c) → en
  efecto, lo de hoy (el punto se gasta); (d) → el 0 se actualiza con los nuevos altos y la stop va al
  0 nuevo: es la lectura que sostienen sus propias citas, `ev-v17-014235-f3375358` y
  `ev-v17-014350-ec133d13`, y la del consultor en `ACTIVAR-SESION-06.md:546-548` (el rechazo por
  precio inválido con el 0 vivo no gasta el punto, y la orden se vuelve a colocar en el siguiente
  cierre de M1 con el 0 actualizado, RN-006); va en la rama de S-19 (3.a y 4.a de
  `ACTIVAR-SESION-06-MOTOR.md:293-301`: sin gastar caja ni punto), con un ADR que enmiende ADR-0083
  D1, y rompería `tests/unit/test_punto_usado.py:343`. (La opción (d) entra por la respuesta del
  consultor a la PARADA final, punto 2.) Ningún parámetro existente: es la regla de la rama de S-19. Sin recuento por fila: 32 rechazos al colocar en la línea base (TRAZAS-ABLACION.md
  5.4).*

**S-4. Volver a entrar en el mismo punto: el «igual» y la caja** · en parte · ADR-0083 D1
- **Lo que nos has dicho:**
  - «tiene que haber un igual para poder repetir entre comillas esa misma entrada pero por lo general
    o sea si hay un error flow normal y demás o bien se gane se pierde y no se vuelve a repetir el
    mismo punto porque el precio va a ir desarrollando» (v17 1:30:09, `ev-v17-013009-5e47afdb`);
  - «si al volver a entrar que haces en el 0 y con el 1 de la caja como digo o sea nuevamente lo
    repito vamos a estar en constante actualización» (v17 1:38:15, `ev-v17-013815-9cf6f076`).
- **Lo que todavía no sabemos:** qué es para ti «un igual», y, al volver a entrar, si la caja es la
  del primer intento o una nueva.
- **Esquema inventado, no es un día real** («M1» escrito): una compra que salta el stop; después el
  precio vuelve al mismo bajo y hace otro igual; dos cajas dibujadas, la del primer intento y una
  nueva desde el último pivote.
- **Pregunta:** «¿Vuelves a entrar en ese punto, y con qué caja?
  - (a) sí, con la caja del primer intento;
  - (b) sí, con una caja nueva;
  - (c) no vuelvo a entrar;
  - (d) otra, ¿cuál?»
- **Para precisar:** ¿Qué tiene que hacer el precio para que sea «un igual»?
- **Para confirmar al final:** «Vuelvo a entrar en el mismo punto cuando ______, con la caja
  ______».
- *Para Aleks (no va a la hoja): ADR-0083:87-88 («Lo que pasa a la sesión 7») y
  `ACTIVAR-SESION-06.md:593-594`; también VIDEO-JULIO.md §7 #7. Hoy D1 deja volver a colocar el
  punto, con la misma caja o con otra, sin pedir un igual. (a) → la reentrada reusa la caja del
  primer intento; (b) → la caja se vuelve a trazar; (c) → el punto se gasta al cerrar, que cambia
  D1: las tres, con ADR (ningún parámetro existente); `cartuchos_max` = 3 no se toca. RN-019 no
  dispara nunca en el motor (Technical Debt). Filas: julio 3, en total 4 (P7, «la rama de RN-019»,
  RECORRIDA-CONSTRUCCION-2.md:1319).*

**S-5. La orden sin llenar cuando el precio toma otra liquidez de M15** · en parte · A-53
- **Lo que nos has dicho:**
  - «Tomar la liquidez más reciente O sea, la quito en ese momento Y espero el punto de la liquidez
    nueva O sea, la respuesta es la A la A la verdad no, como lo planteé aquí» (v17 0:57:30,
    `ev-v17-005730-76948af1`);
  - «este es el punto nuevo más tarde y este sería el que todavía seguiría activo porque para
    nosotros poder actualizar nuestro punto break posible mundo breaker tendríamos que esperar a que
    el precio llegue rompa allí» (v17 0:58:46, `ev-v17-005846-0891a9c9`).
- **Lo que todavía no sabemos:** qué pasa con la orden vieja en el minuto de la toma nueva.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos): la orden vieja puesta; el precio
  toma otra liquidez de M15 sin llenarla; más tarde, el punto nuevo.
- **Pregunta:** «En el minuto de la toma nueva, ¿qué pasa con la orden vieja?
  - (a) la quito;
  - (b) la dejo hasta el punto nuevo y la muevo;
  - (c) otra, ¿cuál?»
- **Para confirmar al final:** «Cuando el precio toma otra liquidez de M15 con mi orden sin llenar,
  la orden ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06.md:581-585`. Hoy `orden_pendiente_al_abrir_escenario`
  = `se_mueve`, DEFAULT_AMBIGUOUS (`parametros.yaml:889`), con A-53 ABIERTA. (a) → `se_retira`; (b) →
  `se_mueve`. También dijo «a es igual en compra y en venta o sea con lo explicado aquí sí o sea pero al revés y si
  antes de que aparezca el nuevo punto el precio toma todavía otra liquidez pues se va actualizando»
  (`ev-v17-005914-55580dc0`): por eso no se repregunta qué pasa con una tercera toma. Sin
  recuento por fila.*

**S-6. La liquidez tomada antes de las 7** · en parte · A-43
- **Lo que nos has dicho:**
  - «a ver operas operas enfocándote o sea después de las 7 de las 7 en adelante pero en m1 o sea O
    sea, antes de las 7 solo se usa para trazo de liquidez.» (v17 1:04:24, `ev-v17-010424-6d7f2d3f`);
  - «Entonces, como hemos visto en el gráfico, solo nos enfocamos, o sea, si vamos a usar el trazo de
    liquidez en M15, solo nos enfocamos, o sea, para el bias y demás, y saber qué hacer luego, a
    partir de las 7 a después, pues solo el trazo de liquidez de M15, como hemos visto aquí.» (v17
    1:03:21, `ev-v17-010321-352430e3`).
- **Lo que todavía no sabemos:** si una toma de liquidez de M15 hecha antes de las 7 vale para entrar
  después de las 7, y si la misma liquidez, tomada antes de las 7 y otra vez después, vale la
  segunda vez.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos, con las horas): (1) la toma a las
  6:30 y el punto a las 7:20; (2) la misma liquidez tomada a las 6:30 y otra vez a las 8:10.
- **Pregunta 1:** «En el dibujo 1, ¿entras?
  - (a) sí;
  - (b) no;
  - (c) otra, ¿cuál?»
- **Pregunta 2:** «En el dibujo 2, ¿vale la toma de las 8:10?
  - (a) sí;
  - (b) no, ya estaba gastada;
  - (c) otra, ¿cuál?»
- **Para confirmar al final:** «Una toma de antes de las 7 ______ para entrar después».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06.md:586-590`. Hoy `toma_antes_de_la_ventana` =
  `cuenta`, CONFIRMED (`parametros.yaml:821`), con A-43 ABIERTA. Pregunta 1 (a) → lo de hoy; (b) →
  un CORRECT a `no_cuenta`. Pregunta 2 (a) → una liquidez tomada antes de las 7 se puede volver a
  tomar después (lo de hoy, con `cuenta`); (b) → una liquidez ya tomada no vuelve a contar: no hay
  parámetro para eso, pediría una regla nueva. Sin recuento por fila.*

**S-7. Una tarde que no está en el vídeo** · material (no cuenta entre las seis)
- **Lo que todavía no sabemos:** en tu backtest grabado en vídeo hay una tarde que el vídeo no
  enseña y el libro sí (Aleks te dice cuál).
- **Pregunta:** «Esa tarde, ¿se grabó en otra parte?
  - (a) sí: ¿dónde?;
  - (b) no se grabó;
  - (c) otra, ¿cuál?»
- *Para Aleks (no va a la hoja): VIDEO-JULIO.md:935 (respuesta a la PARADA final, punto 1) y D6 del
  encargo. Es la tarde del 10 de julio (sesión 11-15): tres ventas en el libro, la sesión pasada en
  el vídeo y sin marcas. El día no va escrito en la pregunta: lo dice Aleks.*

## 3. Las que no caben en las seis (Para Aleks: no van al PDF)

Escritas para que la rama de activación de la 7a, al revisar este documento (recuadro de arriba),
cambie una por otra si la cifra nueva lo pide. Filas: `PREPARACION-SESION-7.md` §0.3.

| Cód. | Pregunta | De dónde sale | Filas (julio / total) |
|---|---|---|---|
| B-7 | Los dos esquemas: qué tiene que tener la zona para que valga, y si sin un punto breaker de ruptura nunca hay entrada | VIDEO-JULIO.md:625-627 | 3 / — |
| B-8 | Seguir entrando tras tres pérdidas en el mismo barrido | VIDEO-JULIO.md:628-630 | 2 / — |
| B-9 | La alternancia (RN-009, S-21): tres retrocesos en M1 y dónde pondría el punto | ACTIVAR-SESION-06.md:595-601 | se solapa con S-3 de la 7a |
| B-10 | A-46 por la toma: si la toma de la mañana vale por la tarde con el mismo sesgo (A-46 está RESUELTA: no se reabre; se pregunta solo por la toma, que no contestó) | ACTIVAR-SESION-06.md:602-605 | — |
