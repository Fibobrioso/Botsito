# Sesión 7a (sesion-07) con el trader: las preguntas y el bloque de días

Rama `trabajo/preparacion-sesion-7`, 2026-11-11, desde `main` en `e6b073f`. El método es el de
ADR-0093; el reparto, los días y las filas, de `docs/validation/PREPARACION-SESION-7.md` (§0.3 y
§0.4, con la respuesta del consultor a la PARADA de la fase 0). La sesión 7 se graba en dos días:
este es el primero, **7a (sesion-07)**; el segundo, **7b (sesion-08)**, en
`docs/sesion-7/PREGUNTAS-7B.md`, se graba después de activar la 7a.

**La hoja es el PDF del consultor**, hecho con este documento, como en las sesiones 4 a 6. No sale
de `kit hoja` ni de `scripts/hoja_preguntas.py`, que no se tocan. Al PDF van, de cada pregunta: el
título, «Lo que nos has dicho», «Lo que todavía no sabemos», la pregunta con sus opciones, «Para
precisar» y «Para confirmar al final». **No van al PDF**: las líneas «Para Aleks» y el §1 entero
(el bloque de días).

**Los códigos S-1 a S-6 son de la 7a (sesion-07).** Cada pregunta se abre diciendo en voz
«pregunta» y su código («pregunta ese uno» … «pregunta ese seis») y se cierra con «fin de
pregunta»; sin eso `scripts/transcribir_sesion.py` no la separa. Sus textos ya están en ese guion
(`CODIGOS_DE_SESION_TEXTO["07"]`), antes de grabar.

**Cómo se leen:**
- **Preguntas cerradas**, con opciones y «otra, ¿cuál?» en todas. Si el trader no entiende una, se
  le describe la situación de otra manera, sin ofrecerle otras respuestas.
- **Esquemas inventados.** Donde dice «Esquema inventado, no es un día real», se enseña un dibujo
  con esas palabras rotuladas y **el marco escrito dentro del dibujo** («M1», «M15», «4 horas»), sin
  precios ni fechas. Como pidió en la sesión 6, cada esquema trae dibujado lo que pasó antes del
  momento de la pregunta, y la liquidez se marca con la línea de tendencia hasta donde se rompe, sin
  extenderla.
- **El 0 y el 1 de la caja**: el 0 es el punto de la orden y el 1 el extremo del lado del stop. En
  una compra, el 0 arriba y el 1 abajo; en una venta, al revés.
- **Nada en dinero.** Las horas, en el reloj de sus gráficos (el de Madrid).
- **Ninguna pregunta lleva días ni fechas**: los días van en el bloque de días (§1) y los dice
  Aleks en la sesión.
- **«En parte»**: la pregunta lleva lo que ya dijo y pregunta solo lo que falta.

## 0. Qué se abrió (exposición)

- Evidencia y feedback de `knowledge/evidence/` y `knowledge/feedback/` citados abajo; la
  transcripción **filtrada** de v11, v12 y v14 por la CLI (`corpus transcript show`), para los
  ítems nuevos de F3; los anexos commiteados de RECORRIDA-CONSTRUCCION-2, TRAZAS-ABLACION y
  VIDEO-JULIO.
- Ninguna transcripción cruda, ningún fotograma, ningún libro, ningún caso.
- Declarado en `docs/validation/HOLDOUT-EXPOSICIONES.md`, filas del 2026-11-11 de esta rama.

## 1. El bloque de días (Para Aleks: no va al PDF)

Va **después** de las seis preguntas técnicas (ADR-0093 §2). Los días cumplen ADR-0093 §3,
comprobados por la compuerta (`PREPARACION-SESION-7.md` §0.4 y
`anexos/PREPARACION-SESION-7/dias-d3.txt`). Las láminas de las seis sesiones están en
`C:\Users\USER\Desktop\laminas-sesion-7a-v2` (fuera del repositorio); **la clave (`clave.txt`) la
guarda Aleks y no se enseña**: qué carpeta es qué sesión no está en este documento.

| Orden | Sesión | Sirve a | Filas de la clasificación (trader / bot) |
|---|---|---|---|
| 1 | 2026-07-07, 11-15 | S-1, el rango de H4 | 9 (4 / 5) |
| 2 | 2026-07-02, 11-15 | S-3, las zonas de control | 10 (6 / 4) |
| 3 | 2026-07-03, 07-11 | S-5, cuándo se coloca la orden | 6 (2 / 4) |
| 4 | 2026-07-15, 11-15 | S-1, el rango de H4 | 5 (4 / 1) |
| reserva | 2026-04-13, 07-11 | S-3, las zonas de control | 4 (3 / 1) |
| reserva | 2026-07-06, 07-11 | S-1, el rango de H4 | 4 (4 / 0) |

**Por cada sesión, en este orden:**
1. **Antes**, Aleks comprueba el día con la línea de SESION-DE-PREGUNTAS.md, «Antes», paso 1 (tiene
   que salir `False`) y se lo dice al trader.
2. El trader **abre él mismo el replay de ese día en FX Replay, ANTES de compartir pantalla**, en
   una sesión de replay nueva, sin marcas, sin backtests guardados y sin Analytics a la vista.
3. El trader **marca y opera la sesión** con pantalla y audio, diciendo qué ve y qué descarta.
4. **Después**, Aleks le enseña las láminas del bot de esa sesión (su carpeta de
   `laminas-sesion-7a-v2`, por la clave): recortadas al instante de decidir, con la caja, la orden,
   el stop y el objetivo, sin fecha y sin nada posterior al corte. **Ningún resultado posterior al
   corte se enseña** (recuadro del 2026-11-12 en ADR-0093 §2). Las láminas de una sesión se enseñan
   en su orden, y el trader corrige cada una antes de pasar a la siguiente: la siguiente dice cómo
   acabaron las anteriores («Antes, en esta sesión: …»). Si la pantalla mide menos de 1.648
   píxeles de ancho, se aleja el zoom del navegador hasta que la lámina entre entera.
5. El trader **corrige**, y se le pregunta: «¿siempre, solo en este caso, o de qué depende?».
6. Si en pantalla aparece otro backtest, Analytics o material de un mes reservado, se reconduce y
   el tramo se declara no citable el mismo día (SESION-DE-PREGUNTAS.md, «Después», paso 4).

## 2. Las preguntas (6)

Ordenadas por las filas que mueven y por el dinero (ADR-0093 §1): el rango de H4 es la que más
filas mueve; el break even y A-35 tocan el dinero. **No se cumple** lo que pedía
`ACTIVAR-SESION-06.md:562` («El break even, la primera de la hoja»): va la segunda (respuesta del
consultor a la PARADA de la fase 0, punto 1).

**S-1. Qué vela es tu rango de H4, y cuándo lo das por actualizado** · en parte
- **Lo que nos has dicho:**
  - «el sesgo es alcista mientras que no se mitigue, pues, con mecha o con cuerpo por debajo de
    esta vela que es nuestro rango» (v9 0:09:02, `ev-v9-000902-25db5bf5`);
  - por escrito: «Para el cambio de sesgo, por ejemplo en el caso 1 la vela roja debe de haber roto
    con cuerpo o con mecha el bajo de la vela alcista Y terminar al cierre bajista»
    (`fb-2026-10-04-sesion-04-6e7da456`);
  - «si se llega a romper el rango, por ejemplo si estamos en rango bajista y llega a romperse por
    velas tiene que ser H4 para poderlo balear, no nos sirve M15, tiene que ser H4» (v17 1:57:41,
    `ev-v17-015741-8f9fd638`);
  - en tu backtest grabado en vídeo: «A ver, este es nuestro rango Por lo general, como no ha sido mitigado
    Ni por debajo por una vela bajista Ni por arriba por una vela alcista Para actualizar el rango
    Entonces nosotros nos enfocamos en buscar Traits alcistas» (v11 0:00:38, `ev-v11-000038-fef9789d`), y «es que es
    muy pero muy pero muy importante y es lo principal yo diría que un 70% o sea que uno defina bien
    el rango el el bias» (v12 0:06:50, `ev-v12-000650-370c4bd8`).
- **Lo que todavía no sabemos:** qué vela es «tu rango» cuando hay varias H4 seguidas, y qué tiene
  que pasar para que pase a ser otra.
- **Esquema inventado, no es un día real** («4 horas» escrito en el dibujo): una vela verde grande
  que rompe por encima de la anterior y cierra verde; detrás, cuatro velas de 4 horas pequeñas que
  quedan dentro de ella; la última de las cuatro es roja, pasa el bajo de la vela de antes (una de
  las pequeñas) y no llega al bajo de la verde grande.
- **Pregunta:** «En el dibujo, ¿cuál es tu rango, y qué lado operas después de la vela roja?
  - (a) el rango es la verde grande, y sigo buscando compras;
  - (b) el rango es la última vela pequeña antes de la roja, y la roja me pasa a ventas;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Qué vela pasa a ser tu rango nuevo cuando lo das por actualizado?
  - Cuando dices que no hay otro rango mayor, ¿qué es un rango mayor?
- **Para confirmar al final:** «Mi rango es ______; mi lado cambia cuando una vela de 4 horas
  ______».
- *Para Aleks (no va a la hoja): de VIDEO-JULIO.md:621-624 (su pregunta 1) y §7 #1 a #3. Ya
  decidido y no se pregunta: que la ruptura vale con mecha o con cuerpo (`sesgo_h4_criterio_ruptura`
  = `mecha`, CONFIRMED, `fb-2026-10-04-sesion-04-d2e84172`) y que la vela tiene que cerrar del
  color de la ruptura (ADR-0080 §1). Hoy el bot fija el lado con la ruptura de la H4 ANTERIOR
  (RN-003; `domain/sesgo.py:98`, `sesgo_h4`; ADR-0044 §2 y ADR-0080), no con un rango que dura
  varias H4. (a) → regla nueva de sesgo por rango, con ADR; (b) → lo de hoy. La reserva «suponiendo
  que no haya otro rango mayor» está en `strategy_spec.yaml:1127-1128`. Filas: julio 30 (20 del
  trader, P1; 10 del bot, P5 del otro lado), VIDEO-JULIO.md:657. Sesiones del bloque: 1 y 4 (y la
  reserva 2026-07-06 07-11).*

**S-2. Cuándo pasas el stop a la entrada** · en parte · A-13
- **Lo que nos has dicho:**
  - en la sesión 1: «apenas toca [...] yo siempre lo he estado trabajando, o sea, apenas toca»
    (`fb-2026-09-09-sesion-01-0ccafcba`);
  - en la sesión 6: «La respuesta es simple Apenas toque Se pone en break up No, no no es apenas
    toque es que la vela la siguiente vela cierre por encima es la condición cierre» (v17 0:51:11,
    `ev-v17-005111-8933dab2`), «la vela tiene que cerrar con un cuerpo por encima o sea de esta zona
    de aquí para poder poner en break even» (v17 0:52:00, `ev-v17-005200-4f93afa0`) y «rompimiento
    con cuerpo desarrollo de zona de control cierre con cuerpo» (v17 0:55:54,
    `ev-v17-005554-172ecbb2`);
  - y, en la misma sesión, la excepción del imbalance, «si ya hay un rompimiento con cuerpo
    demasiado fuerte en que sólo bastaría que llegue la mecha para yo poder poner en break y en la
    operativa» (v17 0:53:52, `ev-v17-005352-cda6245d`), y el margen, «Pero lo ideal sería dar como
    un poco de margen. O sea, ¿qué hace? O sea, cierra con cuerpo, no necesariamente por encima de
    aquí. Pero sí por encima de la zona de entrada.» (v17 0:54:54, `ev-v17-005454-90ce4feb`).
- **Lo que todavía no sabemos:** cuál de las dos es la tuya cuando no hay imbalance: al toque, o al
  cierre con cuerpo.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra puesta; la zona de
  control que se completa; y tres casos: (1) una vela de un minuto que toca el nivel y vuelve; (2)
  una que cierra con cuerpo por encima; (3) una que rompe fuerte dejando un hueco.
- **Pregunta:** «En cada caso, ¿ya mueves el stop a la entrada?
  - (a) sí;
  - (b) no, espero;
  - (c) otra, ¿cuál?»
- **Para precisar:** ¿Lo haces igual en una venta, al revés?
- **Para confirmar al final:** «Paso el stop a la entrada cuando ______ (la vela toca / la vela
  cierra con cuerpo por encima de la zona de entrada), salvo ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06.md:562-573`. Hoy: `break_even_condicion` =
  `tocar` (`parametros.yaml:981`, `fb-2026-09-09-sesion-01-0ccafcba`) y
  `break_even_criterio_ruptura` = `mecha` (`:484`, `fb-2026-09-29-sesion-03-2cff5008`), los dos
  CONFIRMED; la vigilancia al tick (`engine/cableado.py:322-326`). «Al cierre con cuerpo» → dos
  CORRECT con `supersede` (`cierre` y `cuerpo`). No mueve parejas: mueve el dinero, 100 líneas
  `stop_movido` frente a 247 operaciones llenadas y cerradas en la línea base
  (`anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`).*

**S-3. Qué zonas cuentas como zonas de control de un esquema** · en parte · RN-009
- **Lo que nos has dicho:**
  - por escrito: «solo 1 zona control bro. si hay 2 se descarta»
    (`fb-2026-09-09-sesion-01-1b2203b0`);
  - «aquí no habría un trade usando este modelo aquí por el hecho de que te genera dos zonas de
    control [...] es lo más probable que el precio rompa la zona de abajo y se revierta entonces por
    lo general sólo buscamos uno» (v4 0:19:09, `ev-v4-001909-54ac2edd`).
- **Lo que todavía no sabemos:** cuántas no se pregunta: una. Lo que no sabemos es **cuáles** cuentas
  como zonas de control.
- **Esquema inventado, no es un día real** («M15» y «M1» escritos en el dibujo): la toma de la
  liquidez de M15 en una compra; después, el retroceso en M1 deja tres bajos, rotulados A, B y C (A,
  el primero después de la primera vela verde del impulso; B y C, más arriba); el punto de breaker
  arriba.
- **Pregunta:** «En el dibujo, ¿cuáles cuentas como zonas de control de este esquema?
  - (a) A, B y C;
  - (b) solo una de ellas: ¿cuál?;
  - (c) ninguna;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - ¿Qué tiene que tener un bajo del retroceso para ser una zona de control?
  - El bajo que deja la propia toma, ¿es una zona de control?
- **Para confirmar al final:** «Una zona de control es ______; si en el esquema hay dos, lo
  descarto».
- *Para Aleks (no va a la hoja): TRAZAS-ABLACION.md:951-957 (5.5 punto 2), sin sus días; decisión c
  de su PARADA final (`:1393`). A-20 RESUELTA en el número (`zonas_control_max_por_esquema` = 1,
  `parametros.yaml:1071`). Hoy el bot cuenta como zonas de control todos los pivotes de M1 del
  sentido de la entrada que se forman después de la primera vela del impulso, entre la toma y el
  breaker (`domain/estructura_m1.py:153-176`, que lee `engine/zonas.py:471-490`): en el dibujo, (a).
  Otra respuesta → la definición de `pivotes_de_control`, con su ADR; el número no cambia. Filas:
  julio 8 con el gate RN-009 (TRAZAS-ABLACION.md:878-881); en total, la ablación de RN-009 gana 18 y
  pierde 13 (diagnóstico, `:916-923`). Sesiones del bloque: 2 (y la reserva 2026-04-13 07-11).*

**S-4. La mecha que pasa tu alto de M15, y la vela que lo toma** · en parte · A-35
- **Lo que nos has dicho:**
  - «Vale, en este caso sería pues en cuanto la vela roja de después ya cerrado, de esa manera pues
    nosotros tenemos de una manera más clara como trazar la zona lineal de liquidez en M15, la B.»
    (`fb-2026-10-23-sesion-05-03449065`);
  - «Ah, se actualiza el de la mecha Se actualiza el de la mecha» (v15 0:05:53,
    `ev-v15-000553-9d95178a`);
  - «bueno es que si vuelve al alto eso es indiferente tiene que cerrar con cuerpo o sea tiene que
    cerrar con cuerpo por encima de la zona lineal de m15» (v17 0:13:19, `ev-v17-001319-419307f6`), y
    «La vela que genere el rompimiento o la toma de liquidez de M15 Tiene que hacerlo con cuerpo Las
    velas que vengan después, no sé si es indiferente Si luego hace una mecha o demás» (v17 0:17:28,
    `ev-v17-001728-b7b9a32c`).
- **Lo que todavía no sabemos:** si una mecha de M1 que pasa tu alto de M15 y vuelve mueve ese alto,
  y, cuando la vela roja que forma el alto deja una mecha por encima de las verdes, cuál es el alto.
- **Pregunta 1:** «Después de formarse tu alto de M15, una vela de M1 lo pasa con la mecha y vuelve
  a cerrar por debajo. ¿Qué pasa con tu alto?
  - (a) se queda donde estaba;
  - (b) pasa a ser la punta de esa mecha;
  - (c) otra, ¿cuál?» (Y lo mismo en un bajo.)
- **Esquema inventado, no es un día real** («M15» escrito en el dibujo): tres velas verdes y, detrás,
  la vela roja que forma el alto, con una mecha que sube por encima de las verdes.
- **Pregunta 2:** «¿Tu alto es la punta de esa mecha, o el alto de las verdes?
  - (a) la punta de la mecha;
  - (b) el alto de las verdes;
  - (c) otra, ¿cuál?»
- **Para precisar:** ¿y si la mecha es de una vela verde?
- **Para confirmar al final:** «Mi alto de M15 es ______, y lo toma la vela que ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-06.md:574-580` y el recuadro del 2026-11-05 de
  ADR-0084. A-35 ABIERTA y bloqueante. Hoy: `liquidez_m15_pivote_formado` = `cierre_vela_contraria`
  (`parametros.yaml:522`, CONFIRMED) y `liquidez_m15_mecha_que_vuelve` = `solo_la_contraria`,
  DEFAULT_AMBIGUOUS, lectura del consultor (`:551`, opciones `no_mueve`, `solo_la_contraria` y
  `cualquier_mecha`; ADR-0084). Pregunta 1 (a) → ninguna mecha posterior mueve el nivel (lo de hoy);
  (b) → `cualquier_mecha`. (Hasta la revisión de la rama, la pregunta 1 enunciaba lo de hoy y
  pedía confirmarlo, como `ACTIVAR-SESION-06.md:574-577`; se reescribió para no sugerir el «sí»:
  revisor, b3.) Pregunta 2 (a) → `solo_la_contraria` (lo de hoy); (b) → `no_mueve`. La vela sin cuerpo en M15 (S-4 de la sesión 6) está resuelta y no se repregunta. No
  hay recuento por fila: decide cada toma de M15 (RN-004).*

**S-5. En qué momento pones la orden respecto de la ruptura de tu punto**
- **Lo que nos has dicho:**
  - en tu backtest grabado en vídeo: «aquí no había entrada porque es con mecha, sabemos que tiene que ser
    con cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker con cuerpo»
    (v12 0:00:15, `ev-v12-000015-7fc04520`);
  - en la sesión 5: «no, en M1 la mecha siempre vale pero, claro teniendo en cuenta el contexto
    también en el que se desarrolla, porque si es con una zona lineal de M15 [...] el rompimiento,
    para habilitar la zona lineal de M15, tiene que ser con cuerpo. Pero, si no, ya posterior a ello,
    se puede ser con mecha.» (v16 0:02:34, `ev-v16-000234-9a4fa375`).
- **Lo que todavía no sabemos:** cuándo colocas la orden: si ya está puesta cuando el precio llega
  a tu punto, o si la pones cuando ves cómo cierra la vela que llega.
- **Esquema inventado, no es un día real** («M1» escrito en el dibujo): una compra, con el punto de
  breaker marcado; una vela de un minuto llega al punto, lo pasa con la mecha y cierra por debajo;
  la siguiente cierra con cuerpo por encima.
- **Pregunta:** «¿En qué momento pones la orden de compra?
  - (a) antes de que el precio llegue al punto, para que entre en cuanto lo toque;
  - (b) cuando una vela de un minuto cierra por encima del punto;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - En el dibujo, ¿la primera vela (la de la mecha) te habría metido en la operación?
  - Ese cierre con cuerpo que dices en el vídeo, ¿lo miras en la vela de un minuto o en la de 15
    minutos?
- **Para confirmar al final:** «Pongo la orden ______, y entro cuando ______».
- *Para Aleks (no va a la hoja): TRAZAS-ABLACION.md:945-950 (5.5 punto 1), sin sus días ni horas;
  decisión a de su PARADA final (`:1391`). **La contradicción** que la pregunta tiene que deshacer:
  la voz de v12 (F7 #6, `ev-v12-000015-7fc04520`) pide cuerpo, y `ev-v16-000234-9a4fa375` (S-18 de la sesión 5,
  A-32 RESUELTA) dice que en M1 la mecha vale; TRAZAS-ABLACION la clasifica «contradicción con lo
  fijado» (decisión 0, `:1390`). Hoy la orden stop nace al aparecer el punto (`orden_limite_nace` =
  `al_aparecer_punto_de_breaker`, `parametros.yaml:668`; `orden_stop_punto` = `ultimo_pivote_m1`,
  `:702`; ADR-0064) y se llena en el tick que toca el nivel: en el dibujo, (a). (b) → una opción
  nueva de `orden_limite_nace`, con su ADR. Filas: julio 5 (2026-07-03 07-11: la P2 del trader y
  cuatro P5); es el mecanismo de toda orden stop del bot (247 llenadas). Sesión del bloque: 3.
  El tema de `ev-v12-000015-7fc04520` dice «breaker de M1» y su cita no dice M1: si el trader
  responde M15 (la segunda de «Para precisar»), no hay contradicción con S-18, y la activación de la
  7a lo escribe así; el ítem no se toca (es inmutable, y supersede exige el mismo tema). El tipo de
  orden no se pregunta: A-47 está RESUELTA (stop en la ruptura, `ambiguedades.yaml:1512-1519`;
  respuesta del consultor a la PARADA final, punto 1).*

**S-6. Las entradas que dejas sin tomar en el backtest**
- **Lo que nos has dicho:** en tu backtest grabado en vídeo: «aquí hay una entrada que no le voy a tomar
  para no afectar al mostreo» (v14 0:44:04, `ev-v14-004404-ab0281c6`).
- **Lo que todavía no sabemos:** si dejas entradas válidas sin tomar en el backtest, cuándo y por
  qué.
- **Pregunta:** «En tus backtests, ¿dejas entradas válidas sin tomar?
  - (a) no, las tomo todas;
  - (b) sí, a veces;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cuándo, y por qué? ¿Qué es «no afectar al muestreo»?
  - ¿Eso lo haces también operando en real?
- **Para confirmar al final:** «En el backtest dejo sin tomar las entradas que ______».
- *Para Aleks (no va a la hoja): VIDEO-JULIO.md:939 (respuesta a la PARADA final, punto 2) y D6 del
  encargo. No cambia ninguna regla del bot: decide cómo se leen las operaciones de más del bot (39 en
  julio, P5 37 y P6 2; 192 en toda la construcción). Hasta que lo explique, una operación de más no
  se da por error. Si dice (b), el mínimo 2 del pivote puede fallar sin que el bot esté mal
  (ADR-0093 §6: la salida es «una sesión más», no el pivote).*

## 3. Para cerrar

- **Para confirmar al final**, las seis frases, en orden.
- Después, el bloque de días (§1).
