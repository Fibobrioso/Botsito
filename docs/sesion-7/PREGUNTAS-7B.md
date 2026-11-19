# Sesión 7b (sesion-08) con el trader: las preguntas y el bloque de días

Rama `trabajo/preparacion-sesion-7`, 2026-11-11, desde `main` en `e6b073f`. El método es el de
ADR-0093; el reparto, los días y las filas, de `docs/validation/PREPARACION-SESION-7.md` (§0.3 y
§0.4, con la respuesta del consultor a la PARADA de la fase 0). Es el segundo día de la sesión 7,
**7b (sesion-08)**; el primero, **7a (sesion-07)**, está en `docs/sesion-7/PREGUNTAS-7A.md`.

> **Recuadro del 2026-11-18 (`trabajo/laminas-sesion-7b`; `docs/validation/LAMINAS-7B.md`).** Este
> documento está revisado con lo que dejó la 7a (ACTIVAR-SESION-07.md), por encargo del consultor
> del 2026-11-18; lo de antes está en git (`main` en b174d714). Qué cambió y por qué:
> - **El bloque de días (§1).** Salen 2026-01-13 de 07 a 11 y 2026-01-07 de 07 a 11: abren con
>   menos de 60 velas de 4 horas cargadas, y su sesgo sale del rango que arranca en la primera de
>   enero, no del que vería el trader (ACTIVAR-SESION-07.md F1.3); le haríamos corregir un efecto
>   de nuestros datos. Entran 2026-04-24 de 07 a 11 y 2026-04-27 de 11 a 15, de
>   `anexos/PREPARACION-SESION-7/sustitutas.txt`, elegidas sin mirar lo que hacen el bot ni el
>   trader en ellas. El 2026-04-15 de 11 a 15 se queda, con lo que pasó en la 7a dicho. Los pasos de
>   cada sesión ganan lo aprendido en la 7a.
> - **Las preguntas (§2).** Entran las tres que la 7a dejó sin contestar, reformuladas en
>   ACTIVAR-SESION-07.md: la mecha que vuelve en M15 (A-35), las zonas de control con el margen del
>   break even (RN-009 y A-13) y el rango de 4 horas después de una ruptura (A-58). Salen a §3 la
>   reentrada, A-53 y A-43. El orden es el de ADR-0093 §1: primero las que tocan el dinero, después
>   por las filas que mueven (LAMINAS-7B.md, 0.3).
> - **Las láminas** de la 7b ya existen: las generó esta rama, fuera del repositorio, y no se
>   describen aquí. Lo que el recuadro D4 de abajo encargaba a la activación de la 7a lo hizo esta
>   rama (ACTIVAR-SESION-07.md 0.5, fila 1).

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
- En la revisión del 2026-11-18 (`trabajo/laminas-sesion-7b`): los ítems de v18 y v19 citados
  abajo, que ya cita ACTIVAR-SESION-07.md, y los anexos commiteados de PREPARACION-SESION-7,
  RECORRIDA-CONSTRUCCION-2 y ACTIVAR-SESION-07. Ninguna transcripción cruda ni filtrada, ningún
  fotograma, ningún libro, ningún caso. Filas del 2026-11-18 de esa rama en
  `HOLDOUT-EXPOSICIONES.md`.

## 1. El bloque de días (Para Aleks: no va al PDF)

Va **después** de las seis preguntas técnicas, y la pregunta de material (S-7) al final de todo
(ADR-0093 §2). Las siete sesiones (las cuatro y las tres reservas) pasan la compuerta de ADR-0093 §3
y abren con 60 o más velas de 4 horas cargadas, medido el 2026-11-18 (`LAMINAS-7B.md`, 0.2;
`anexos/LAMINAS-7B/compuerta-7b.txt` y `h4-cargadas.txt`). Sus láminas las generó
`trabajo/laminas-sesion-7b`, fuera del repositorio; la clave la guarda Aleks.

| Orden | Sesión | Sirve a | Filas de la clasificación (trader / bot) |
|---|---|---|---|
| 1 | 2026-04-24, 07-11 | S-3 (la caja: cociente 0,62 con el stop fuera) | 5 (1 / 4) |
| 2 | 2026-04-15, 11-15 | el trader no opera y el bot sí (S-6 de la 7a); S-3 | 5 (0 / 5) |
| 3 | 2026-04-27, 11-15 | S-3 (cociente 0,62 con el stop fuera) | 3 (2 / 1) |
| 4 | 2026-01-19, 11-15 | S-3 (cociente 1,78 en la entrada) | 3 (3 / 0) |
| reserva | 2026-01-21, 07-11 | S-3 (cociente 0,50 en la entrada) | 3 (2 / 1) |
| reserva | 2026-01-22, 11-15 | el sesgo de H4 por una ruptura de 2 puntos (toca A-16) | 3 (3 / 0) |
| reserva | 2026-07-16, 07-11 | S-3 (cociente 0,34 con el stop fuera; era una pareja en la línea base y, tras activar la 7a, ya no: RN-032, ACTIVAR-SESION-07.md F1.4) | 1 (1 / 0) |

«Sirve a», de `anexos/PREPARACION-SESION-7/sustitutas.txt`; las filas, de la clasificación de la
línea base (`anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt`), contadas con
`filas_por_sesion.py` (`filas-por-sesion.txt` para las de antes y
`anexos/LAMINAS-7B/filas-por-sesion-7b.txt` para las siete). Las filas son de antes de activar la
7a, y el motor de las láminas es el de después: el recuadro D4 pedía las filas «con la corrida
nueva», y para enero y abril no hay ninguna commiteada (`LAMINAS-7B.md`, desviaciones).

Ninguna de las cuatro tiene vídeo del trader. **El 2026-04-15 de 11 a 15 ya lo abrió en la 7a**: por
error, en la reserva, lo marcó y lo operó (`SESION-07-EXTRACCION.md` §5.1, punto 9; ese tramo sigue
no citable). No vio ninguna lámina de ese día, y por eso se queda. En las otras tres, el bloque de
días es la primera vez que se le oye operarlas; en la del 04-15, la primera con el método del bloque.

**Por cada sesión**, los pasos de `PREGUNTAS-7A.md` §1 (ADR-0093 §2), con lo aprendido en la 7a
(`docs/runbooks/ERRORES-RECURRENTES.md`, filas de `trabajo/sesion-07` y `trabajo/activar-sesion-07`):
1. Aleks comprueba el día ANTES de grabar, y se lo dice.
2. El trader abre él mismo el replay, antes de compartir pantalla, en una sesión de replay nueva,
   sin marcas, backtests ni Analytics, y borra cualquier marca anterior. **En el 2026-04-15 de 11 a
   15, sobre todo: ese día ya lo marcó y lo operó en la 7a, así que tiene que ser una sesión de
   replay nueva y sin ninguna marca.**
3. Dice la fecha en voz alta al abrir cada gráfico, y otra vez después de abrir cada replay.
4. Opera la sesión entera, con voz, ANTES de ver ninguna lámina.
5. Después ve las láminas del bot de esa sesión, sin fecha, sin nada posterior al corte y sin ningún
   resultado.
6. Corrige, y en CADA corrección Aleks pregunta «¿siempre, solo en este caso, o de qué depende?».
7. Si aparece otro backtest, Analytics o un mes reservado, se reconduce y el tramo es no citable el
   mismo día.

En el bloque técnico (S-1 a S-6) solo se usan los esquemas. Si el trader quiere poner un ejemplo en
su gráfico, tiene que ser un día de construcción, y dice la fecha en voz alta al abrirlo.

## 2. Las preguntas (6 técnicas y una de material)

Ordenadas como manda ADR-0093 §1: primero las que tocan el dinero (S-1 y S-2), y después por las
filas que mueven (`LAMINAS-7B.md`, 0.3). S-3, la caja, es la única de las cuatro con recuento por
fila; S-4, S-5 y S-6 no lo tienen y van detrás.

**S-1. La mecha de un minuto que pasa tu alto de M15 y vuelve** · en parte · A-35
- **Lo que nos has dicho:**
  - del alto que forma la vela roja con su mecha: «La respuesta es la punta de la mecha.» (v18
    0:25:11, `ev-v18-002511-eec0acec`), y «pero bueno, mi alto de M15 es la punta de la mecha en el
    esquema planteado» (v18 0:27:29, `ev-v18-002729-38609240`);
  - de la mecha de una vela verde: «Pues si la mecha llega a ser más alto Que este alto De aquel
    alto O sea, sería así Entonces se trazaría desde aquí se trazaría desde allí» (v18 0:27:01,
    `ev-v18-002701-62875550`).
- **Lo que todavía no sabemos:** si, con tu alto ya formado, una vela de un minuto que lo pasa solo
  con la mecha y vuelve a cerrar por debajo lo mueve.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos): en M15, tres velas verdes y,
  detrás, la vela roja que forma el alto, con su mecha por encima de las verdes; el alto, rotulado A,
  en la punta de esa mecha. Después, en M1, una vela que pasa A solo con la mecha y cierra por
  debajo; la punta de esa mecha nueva, rotulada B.
- **Pregunta:** «Ya tienes tu alto de M15 en la punta de la mecha. Si después una vela de un minuto
  pasa ese alto solo con la mecha y vuelve a cerrar por debajo, ¿tu alto pasa a ser la punta de esa
  mecha nueva, o se queda donde estaba?
  - (a) se queda donde estaba, en A;
  - (b) pasa a ser la punta de la mecha nueva, B;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y si son varias velas de un minuto, una detrás de otra, las que lo pasan con la mecha?
  - ¿Lo haces igual en un bajo, al revés?
- **Para confirmar al final:** «Cuando una vela de un minuto pasa mi alto de M15 solo con la mecha y
  vuelve, mi alto ______».
- *Para Aleks (no va a la hoja): ACTIVAR-SESION-07.md, «Lo que no se activó» (A-35, pregunta 1) y
  F3 (S-4); `SESION-07-EXTRACCION.md` §3.1 y §5.1, punto 1. A-35 ABIERTA y bloqueante. Hoy
  `liquidez_m15_mecha_que_vuelve` = `solo_la_contraria`, DEFAULT_AMBIGUOUS, lectura del consultor
  (`parametros.yaml:595`, opciones `no_mueve`, `solo_la_contraria` y `cualquier_mecha`; ADR-0084).
  Con la pregunta 2 de la 7a ya contestada (la punta de la mecha de la roja): (a) →
  `solo_la_contraria` (lo de hoy), un CORRECT que lo fija y, con «siempre», cierra A-35 por sus
  sitios (`docs/runbooks/AMBIGUEDADES.md`); (b) → `cualquier_mecha`, un CORRECT con el valor nuevo;
  «otra» → A-35 sigue abierta con lo que diga. Toca el dinero: decide qué alto o bajo de M15 se toma
  (RN-004), en cada toma de la construcción. Sin recuento por fila (`PREPARACION-SESION-7.md` §0.3,
  A-6).*

**S-2. Tus zonas de control y el momento del break even** · en parte · RN-009 y A-13
- **Lo que nos has dicho:**
  - de las zonas de control del esquema de la 7a: «como zona de control en ese esquema a y b o sea a
    y b la respuesta sería esa de allí entonces es de otra cual solo a y b» (v18 0:21:15,
    `ev-v18-002115-bf40ec0b`), y «una zona de control es pues él es el desarrollo es la mitigación en
    un orden flow alcista del punto más alto a la condicional es que hay una vela roja vale luego una
    vela verde y cierre con cuerpo por encima» (v18 0:22:29, `ev-v18-002229-2be4ecf1`);
  - del break even: «la entrada tiene que cerrar por encima de su nivel alto de su de su máximo nivel
    para nosotros pues poder poner en break even porque nosotros esperamos a que cierre la vela»
    (v18 0:13:27, `ev-v18-001327-70f1d014`), «pasas el stop de la entrada cuando se se desarrolla una
    zona de control completamente validada» (v18 0:19:00, `ev-v18-001900-1581efbe`) y, en un gráfico,
    «cerrar con cuerpo sea mínimo al menos por un par de puntos o un pip» (v19 1:15:29,
    `ev-v19-011529-8ae8b581`).
- **Lo que todavía no sabemos:** (1) dónde están A y B respecto de la toma y del punto, y si con dos
  zonas de control el esquema te sirve; (2) si, para el break even, el cierre por encima del alto de
  tu zona de control pide un margen, cuánto, y si es siempre el mismo.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos), en dos dibujos: (1) el de la
  7a: la toma de la liquidez de M15 en una compra; después, el retroceso en M1 con tres bajos
  rotulados A, B y C, y el punto de breaker arriba; (2) una compra ya puesta, la zona de control que
  se forma después de la entrada, con su alto rotulado, y una vela de un minuto que cierra con
  cuerpo por encima de ese alto.
- **Pregunta 1:** «En el dibujo 1, A y B te valen como zonas de control y C no. ¿A y B son zonas del
  retroceso, después de tomar la liquidez, o de antes de romper el punto? Y si hay dos, ¿ese esquema
  te sirve o lo descartas?
  - primero: (a) del retroceso, después de tomar la liquidez; (b) de antes de romper el punto; (c)
    otra, ¿cuál?;
  - y con dos: (a) me sirve; (b) lo descarto; (c) otra, ¿cuál?»
- **Pregunta 2:** «En el dibujo 2: cuando la vela cierra por encima del alto de tu zona de control,
  ¿te basta con que cierre un punto por encima, o tiene que pasarlo por un margen? ¿Cuánto, y
  siempre el mismo?
  - (a) me basta con que cierre por encima;
  - (b) tiene que pasarlo por un margen: ¿cuánto?, ¿siempre el mismo?;
  - (c) otra, ¿cuál?»
- **Para precisar:** el bajo que deja la propia toma, ¿cuenta como zona de control?
- **Para confirmar al final:** «Mis zonas de control son las ______; si hay dos, el esquema ______.
  Para pasar a break even, la vela tiene que cerrar por encima del alto de la zona de control
  ______».
- *Para Aleks (no va a la hoja): ACTIVAR-SESION-07.md, «Lo que no se activó» (las zonas de control y
  el margen del break even), F2.3 y F3 (S-3); `SESION-07-EXTRACCION.md` §5.1, puntos 2 y 4 (la duda:
  la zona de control del esquema 2 es antes de romper el punto, y la del break even, después,
  `ev-v19-011640-1fdc33a7`). **Pregunta 1**: hoy el bot cuenta como zonas de control los pivotes de
  M1 del sentido de la entrada entre la toma y el breaker (`domain/estructura_m1.py`, que lee
  `engine/zonas.py`), y `zonas_control_max_por_esquema` = 1, CONFIRMED (A-20 RESUELTA,
  `parametros.yaml:1131`): con A y B, RN-009 descarta el esquema. Primero (a) → lo de hoy; (b) →
  solo cuentan las de antes de romper el punto: cambia la definición de
  `zonas_desarrolladas_superan`, con ADR (ningún parámetro existente). Con dos, «lo descarto» → lo
  de hoy; «me sirve» → va contra A-20, RESUELTA: no se activa; se REABRE con un registro `REOPEN`
  si el consultor lo decide (`docs/runbooks/AMBIGUEDADES.md`). **Pregunta 2**: hoy
  `break_even_condicion` = `cierre` y `break_even_criterio_ruptura` = `cuerpo`, CONFIRMED, sin
  margen; A-13 ABIERTA solo por él (`parametros.yaml:520`). (a) → A-13 se cierra sin margen, con su
  registro de feedback y sus cinco sitios; (b) con una cifra fija → un parámetro nuevo del registro
  (entero, en puntos; ADR-0002), con su registro de feedback, y la regla RN-014 que lo lea, con ADR;
  (b) con «depende» → A-13 sigue abierta con lo que diga. Toca el dinero por A-13 (el break even).
  Filas: las zonas de control, julio 8 con el gate RN-009 en la línea base (TRAZAS-ABLACION.md 5.2;
  no está en los anexos); el margen, sin recuento por fila.*

**S-3. Dónde pones el 0 de tu caja** · en parte · A-48
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

**S-4. Tu rango de 4 horas después de una ruptura** · en parte · A-58
- **Lo que nos has dicho:**
  - «La respuesta es la letra A, claramente. El rango es la vela verde grande y sigo buscando
    compras.» (v18 0:02:49, `ev-v18-000249-bb7b1c07`);
  - «para nosotros ver una continuidad o una reversión, bastaría con mecha o con cuerpo un
    rompimiento, pero para poder tener el enfoque, se tiene que definir el color de la vela» (v18
    0:04:08, `ev-v18-000408-c48297b1`);
  - «para nosotros poder definir nuestro nuevo rango tenemos que ver qué vela o sea si es alcista o
    bajista y rompe o por encima o por debajo» (v18 0:08:22, `ev-v18-000822-57145b90`);
  - «el rango mayor sería esto de aquí. O sea, porque este rango todavía la liquidez, tanto por
    encima como por debajo, no sea mitigada» … «y ya una vez mitigado pues se actualiza» (v18
    0:09:12, `ev-v18-000912-52594a58`).
- **Lo que todavía no sabemos:** cuando una vela de 4 horas rompe tu rango y cierra de su color, qué
  alto y qué bajo forman tu rango nuevo; y, si la que lo rompe cierra del color contrario, qué pasa
  con tu rango.
- **Esquema inventado, no es un día real** («4 horas» escrito), en dos dibujos: la vela de rango
  rotulada; (1) después, una vela que pasa su alto y cierra verde; (2) en otro dibujo, una vela que
  pasa su alto y cierra roja.
- **Pregunta:** «Cuando una vela de 4 horas rompe tu rango y cierra de su color, ¿tu rango nuevo va
  del alto al bajo de esa vela, o de otro sitio? Y si rompe tu rango pero cierra del color
  contrario, ¿tu rango sigue siendo el mismo o cambia?
  - en el dibujo 1: (a) del alto al bajo de esa vela; (b) de otro sitio: ¿cuál?; (c) otra, ¿cuál?;
  - en el dibujo 2: (a) sigue siendo el mismo; (b) cambia: ¿a cuál?; (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Marcas tu rango siempre en el gráfico de 4 horas, o a veces en otro?
  - ¿Lo haces igual cuando la ruptura es por abajo, al revés?
- **Para confirmar al final:** «Cuando una vela de 4 horas rompe mi rango y cierra de su color, mi
  rango nuevo es ______; si cierra del color contrario, mi rango ______».
- *Para Aleks (no va a la hoja): ACTIVAR-SESION-07.md, «Lo que no se activó» (A-58) y F1; ADR-0094
  (lecturas b y d). Hoy `sesgo_h4_rango_nuevo` = `vela_que_rompe_con_su_color`, DEFAULT_AMBIGUOUS,
  lectura del consultor (`parametros.yaml:475`, opciones `vela_que_rompe_con_su_color` y `otra`).
  (a) en los dos dibujos → `vela_que_rompe_con_su_color` (lo de hoy), un CORRECT que lo fija y, con
  «siempre», cierra A-58 por sus sitios (`docs/runbooks/AMBIGUEDADES.md`); cualquier otra respuesta
  → `otra`, que el motor niega con nombre: regla nueva con un ADR que enmiende ADR-0094. «A veces en
  otro gráfico» → A-58 sigue abierta con lo que diga. Sin recuento por fila de A-58: la clase que
  movía el rango, P1 de julio, es 1 tras activar la 7a (`anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`;
  es la de 2026-07-01 de 11 a 15, B-15 de §3).*

**S-5. Para que el máximo de la verde sea tu punto, qué tiene que hacer la roja** · en parte · S-22
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

**S-6. El precio ya está más allá del 0 cuando se forma la caja** · en parte · S-19
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
cambie una por otra si la cifra nueva lo pide. Filas: `PREPARACION-SESION-7.md` §0.3. Revisadas
el 2026-11-18 por `trabajo/laminas-sesion-7b` (recuadro de arriba): entran B-11 a B-15, con sus
filas contadas en `LAMINAS-7B.md`, 0.3. Ninguna entra en las seis por esta revisión: lo decide el
consultor.

| Cód. | Pregunta | De dónde sale | Filas (julio / total) |
|---|---|---|---|
| B-7 | Los dos esquemas: qué tiene que tener la zona para que valga, y si sin un punto breaker de ruptura nunca hay entrada | VIDEO-JULIO.md:625-627 | 3 / — |
| B-8 | Seguir entrando tras tres pérdidas en el mismo barrido | VIDEO-JULIO.md:628-630 | 2 / — |
| B-9 | La alternancia (RN-009, S-21): tres retrocesos en M1 y dónde pondría el punto | ACTIVAR-SESION-06.md:595-601 | se solapa con S-3 de la 7a |
| B-10 | A-46 por la toma: si la toma de la mañana vale por la tarde con el mismo sesgo (A-46 está RESUELTA: no se reabre; se pregunta solo por la toma, que no contestó) | ACTIVAR-SESION-06.md:602-605 | — |
| B-11 | Volver a entrar en el mismo punto: qué es «un igual» y, al volver, si la caja es la del primer intento o una nueva (la S-4 de antes de esta revisión; «un igual», `ev-v17-013009-5e47afdb`; la caja del segundo intento, `ev-v17-013815-9cf6f076`) | ADR-0083:87-88; ACTIVAR-SESION-06.md:593-594; VIDEO-JULIO.md §7 #7 | 4 (P7, tras activar la 7a: `anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`; 3 en la línea base) / 4 en la línea base (RECORRIDA-CONSTRUCCION-2.md:1319) |
| B-12 | A-53: en el minuto en que el precio toma otra liquidez de M15 con la orden sin llenar, si la orden vieja se quita o se mueve (la S-5 de antes de esta revisión; `ev-v17-005730-76948af1`, `ev-v17-005846-0891a9c9`, `ev-v17-005914-55580dc0`; y, del bloque de días de la 7a, como ejemplo, «se maneja una sola orden, no es que se deja pendiente otra orden aquí, otra orden aquí, no se va actualizando la orden», `ev-v18-011801-8b4f738d`) | ACTIVAR-SESION-06.md:581-585; ACTIVAR-SESION-07.md F3 | sin recuento por fila |
| B-13 | A-43: si una toma de liquidez de M15 hecha antes de las 7 vale para entrar después, y si la misma liquidez tomada antes y otra vez después vale la segunda vez (la S-6 de antes de esta revisión; `ev-v17-010424-6d7f2d3f`, `ev-v17-010321-352430e3`; y, del bloque de días de la 7a, como ejemplo, «se llega a mitigar con velas de m1 pero de la sesión del 7 en adelante si es una vez la mitigación antes de las 7 que antes del inicio de la sesión o de cada sesión no es válido», `ev-v19-012529-685ae24d`, `ev-v19-012650-4f9f20ec`, que va contra `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED) | ACTIVAR-SESION-06.md:586-590; ACTIVAR-SESION-07.md, «Lo que no se activó» | sin recuento por fila |
| B-14 | El punto de breaker sin vela contraria: si la segunda vela del mismo color, con la mecha más larga que la anterior, da un punto de breaker (`ev-v18-013614-cfd2b45d`, `ev-v19-011138-5c622b1f`, del bloque de días de la 7a, como ejemplos) | ACTIVAR-SESION-07.md F3 | sin recuento por fila |
| B-15 | En la sesión de las 11 del 2026-07-01: «El 1 de julio, en la sesión de las 11, dices que tu rango sigue alcista y buscas compras, y a las 12:59 vendes. ¿Qué te hizo vender ahí?» (lleva día: va al bloque de días, no a las técnicas, si el consultor la mete) | ACTIVAR-SESION-07.md F1.4 (iv) y «Lo que no se activó»; VIDEO-JULIO.md §4.1 | 3 (1 P1 del trader y 2 P5 del bot, tras activar la 7a: `anexos/ACTIVAR-SESION-07/delta-julio-base-f1.txt`) / — |
