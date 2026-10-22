# Sesión 5 con el trader: las preguntas, después del barrido

Rama `trabajo/barrido-sesion-5`, 2026-10-19, desde `main` en `e518707`. **Solo lectura y este
documento**: no cambia el motor, la spec, las ambigüedades, el feedback ni los casos. El inventario,
lo que se juntó y lo que quedó fuera, con su porqué: `docs/validation/BARRIDO-SESION-5.md` §1; las
decisiones del consultor del 2026-10-19, al final de ese informe.

> **Antes de grabar: la copia de seguridad A.4** (`docs/plan/HOJA-DE-RUTA.md`, carril de Aleks).
> La sesión 5 depende de ella y hoy no está hecha.

**La hoja es el PDF del consultor**, hecho con este documento, como en la sesión 4
(`docs/sesion-4/HOJA-USADA.md`). No sale de `scripts/hoja_preguntas.py`, que no se toca en esta
rama (decisión 3 del consultor). Al PDF van, de cada pregunta: el título, «Lo que nos has dicho»,
«Lo que todavía no sabemos», la pregunta con sus opciones, «Para precisar» y «Para confirmar al
final». **Las líneas «Para Aleks» no van a la hoja**: dicen de dónde sale la pregunta, qué hace hoy
el bot y, en S-3 y S-4, en qué lectura documentada cae cada opción.

**Los códigos S-1 a S-25 son de la sesión 5.** No son los de la sesión 4: allí S-13 era la vela de
4 horas que rompe por los dos lados y S-14 la vela casi plana; aquí S-23 y S-24 las confirman. Como
manda `docs/runbooks/SESION-DE-PREGUNTAS.md`, cada pregunta se abre diciendo en voz «pregunta» y su
código («pregunta ese uno», «pregunta ese veinticinco») y se cierra con «fin de pregunta». Sin eso
`scripts/transcribir_sesion.py` no la separa (nota de la sesión 3 en el runbook). Los textos de
estos códigos entran en ese script con la ingesta de la sesión (`CODIGOS_DE_SESION_TEXTO["05"]`),
no aquí.

**Desviaciones declaradas:**
1. **Las preguntas van cerradas, con opciones**, y con «otra, ¿cuál?» donde las opciones pueden
   sugerir. El runbook pide abiertas («Durante», punto 2); manda el encargo (D2), como en la
   sesión 4.
2. **El orden de las dos del sesgo es el contrario al de `SESGO-H4-COLOR.md` §4.4**: primero la de
   la vela que rompe con la mecha y cierra del color contrario (S-1), sin nada delante, y después
   la ruptura sin cuerpo (S-2), con lo que dijo por WhatsApp. Si S-2 fuera primero, su cita le
   leería la regla que decide S-1 (decisión 2 del consultor).
3. **S-6 lleva dos preguntas** (cuántas reentradas y qué caja), porque el encargo manda su texto
   tal cual (`PUNTO-USADO.md` §5).

**Cómo se leen:**
- **Esquemas inventados.** Donde dice «Esquema inventado, no es un día real», se enseña un dibujo
  con esas palabras rotuladas, sin precios ni fechas. **No se enseña ningún gráfico de un día
  real** (decisión 4). Los días de construcción en que se ve cada caso son la clave de Aleks y
  están en el informe (§2.c), no aquí. La única fecha que va a la hoja es la de S-6, el 29 de
  abril, por orden del encargo.
- **Nada en dinero** y ninguna cifra de VIABILIDAD-COMISION. Las horas, en el reloj del trader
  (Europe/Madrid).
- **Provisional hasta su respuesta:** ADR-0083 (qué gasta un punto) hasta S-6; ADR-0081 (el lote
  que no cabe) hasta S-5.
- **«En parte»**: la pregunta lleva lo que ya dijo y pregunta solo lo que falta.

## 0. Qué se abrió (exposición)

- **Evidencia y feedback**: los YAML de `knowledge/evidence/` (v4, v6, v7, v9 y v10) y de
  `knowledge/feedback/` (sesiones 1, 3 y 4) citados abajo, leídos con Read y Grep. Ninguno cae en un
  tramo de `knowledge/corpus/tramos_no_citables.yaml`: comprobado tramo a tramo para v6, v7, v9 y
  v10.
- **La CLI filtrada**: un `uv run botsito kb find "otra reentrada"`, sin `--video` (dos
  resultados, de v4 y de v5), para fijar el minuto de la cita de S-6. `kb at` y `kb find --video`
  no se usaron sobre v7 a v10, que la guardia niega.
- **Informes**: los que nombra el encargo (D1) y `LA-CAJA-DEL-29-DE-ABRIL.md`.
- **Nada más**: ninguna transcripción cruda ni filtrada a mano, ningún fotograma, ningún libro,
  ningún caso y ningún agregado. Los días de construcción que se nombran en el informe se
  comprobaron con `casos_ocultos` (todos `False`) y no se abrieron. **Todo esto está declarado** en
  `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-19 (hallazgo a1 del revisor: la primera versión decía
  que no había nada que declarar).

## 1. Las preguntas (25)

Ordenadas por impacto (D4): lo que más separa al bot del trader y lo que lo bloquea; la lista de
la corrida de construcción; las demás «en parte»; y las confirmaciones cortas. A la sesión 4, con
24 preguntas, le bastaron 2:07:36. Estas 25 se estiman en unas 2:13. **Si falta tiempo**: S-25 y
S-23 por WhatsApp, y S-18 a la sesión 6 (decisión 0 del consultor).

### Bloque 1 · El sesgo y lo que bloquea al bot

**S-1. Con el sesgo bajista, una vela de 4 horas rompe el máximo de la anterior solo con la mecha
y cierra roja**
- **Lo que nos has dicho:** — (se pregunta sobre el esquema).
- **Lo que todavía no sabemos:** qué manda cuando la mecha rompe por arriba y la vela cierra roja.
- **Esquema inventado, no es un día real:** dos velas de 4 horas. La primera, roja (sesgo
  bajista). La segunda pasa con la mecha por encima del máximo de la primera, vuelve y cierra roja.
- **Pregunta:** «Con el sesgo bajista, esta vela de 4 horas rompe por encima el máximo de la
  anterior, solo con la mecha, y cierra roja. Para la siguiente sesión, ¿cuál es tu sesgo?
  - (a) alcista;
  - (b) sigue bajista;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Importa lo lejos que llegue la mecha por encima del máximo?
  - ¿Importa lo grande que sea el cuerpo rojo?
  - ¿Lo decides al cierre de esa vela, o puedes cambiar de idea durante la vela siguiente?
- **Para confirmar al final:** «Con el sesgo bajista, si la vela de 4 horas rompe el máximo de la
  anterior solo con la mecha y cierra roja, el sesgo de la siguiente es ______».
- *Para Aleks (no va a la hoja): `SESGO-H4-COLOR.md` §4.4, pregunta 2; ADR-0080. Hoy el bot hace
  (b). Sin ninguna cita, y sin nombrar ninguna sesión anterior (D2 y decisión 2 del consultor).*

**S-2. La vela de 4 horas que rompe con la mecha y cierra sin cuerpo**
- **Lo que nos has dicho:**
  - por WhatsApp, el 2026-10-14 a las 14:55 (hora de Lima): «Para el cambio de sesgo, por ejemplo
    en el caso 1 la vela roja debe de haber roto con cuerpo o con mecha el bajo de la vela alcista
    Y terminar al cierre bajista» (`fb-2026-10-04-sesion-04-6e7da456`);
  - en la sesión 4, de la vela que rompe por los dos lados y cierra sin color: «si esta es una vela
    neutra, si esta es una vela neutra, no tiene ningún color, nosotros seguiríamos operando
    alcistas» (v10 1:40:05, `ev-v10-014005-7e2228f4`, `fb-2026-10-04-sesion-04-ca0afae6`).
- **Lo que todavía no sabemos:** qué pasa cuando rompe **un solo** lado y cierra exactamente donde
  abrió. No tiene color, y tu regla dice que tiene que terminar del color de la ruptura.
- **Esquema inventado, no es un día real:** dos velas de 4 horas. La primera, verde (sesgo
  alcista). La segunda pasa con la mecha por debajo del mínimo de la primera, no toca su máximo, y
  cierra exactamente en el precio de apertura: una cruz, sin cuerpo.
- **Pregunta:** «Esta vela de 4 horas rompe el mínimo de la anterior con la mecha y cierra
  exactamente donde abrió, sin color. ¿Cambia tu sesgo?
  - (a) sí, pasa a bajista, porque rompió el mínimo;
  - (b) no, sigue el sesgo que había, como con la vela neutra que rompe por los dos lados;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y si rompe el máximo con la mecha y cierra sin color, con el sesgo bajista?
  - ¿Cambia algo si la mecha pasa el mínimo por mucho, diez o veinte pips?
- **Para confirmar al final:** «Si la vela de 4 horas rompe un solo extremo con la mecha y cierra
  sin color, el sesgo ______».
- *Para Aleks (no va a la hoja): `SESGO-H4-COLOR.md` §4.4, pregunta 1; ADR-0080 §4 (D3, decisión
  provisional del consultor). Hoy el bot hace (b). En construcción no aparece ninguna.*

**S-3. Cuándo das por formado un alto o un bajo de M15** · en parte · A-35 (bloqueante)
- **Lo que nos has dicho** (sesión 4):
  - «a marcas un alto en m15 después el precio lo pasa por poco con la mecha y vuelve que haces
    pues no tiene la regla es que lo tiene que pasar con cuerpo no con mecha» (v10 1:24:56,
    `ev-v10-012456-9dc1d221`);
  - «y si lo pasa con cuerpo es que lo tiene que pasar con cuerpo es una verdad absoluta es lo
    mismo como un bajo de m15» (v10 1:25:26, `ev-v10-012526-15de61b8`);
  - antes, en tus vídeos: «Por encima de este ya formado» (v4 0:50:53, `ev-v4-005053-885e2773`).
- **Lo que todavía no sabemos:** en qué momento exacto un alto de M15 pasa a ser tu liquidez: «ya
  formado» cuándo.
- **Esquema inventado, no es un día real:** velas de 15 minutos. Tres verdes que suben; la tercera
  marca el alto. Detrás, una roja.
- **Pregunta:** «Aquí la tercera vela verde marca el alto. ¿En qué momento das ese alto por formado,
  para usarlo como liquidez?
  - (a) en cuanto empieza la vela roja de después, aunque todavía no haya cerrado;
  - (b) cuando la vela roja de después ya ha cerrado;
  - (c) otra, ¿cuál?»
  - *Para Aleks: (a) cae en `inicio_vela_contraria`; (b) en `cierre_vela_contraria`
    (`docs/runbooks/ACTIVAR-A35-A44.md` §1). Cualquier otra respuesta (un número de velas a cada
    lado, «cuando el precio ya lo probó»…) no cae en ninguna: se PARA y no se cierra A-35 (§4 del
    runbook).*
- **Para precisar:**
  - Si la vela de después no es roja sino una sin cuerpo, ¿cuenta como la vela de después?
  - Cuando el precio pasa ese alto solo con la mecha y vuelve, ¿sigues usando el mismo alto, o el
    de la mecha?
  - ¿Lo miras igual con un bajo de M15?
- **Para confirmar al final:** «Un alto de M15 está formado cuando ______, y si después el precio lo
  pasa solo con la mecha, mi alto sigue siendo ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.4. `liquidez_m15_pivote_formado` está
  UNKNOWN y RN-004 no corre sin ella. Lo de la mecha ya lo dijo (arriba); «sigo usando el mismo
  alto» solo se deduce, por eso va en «Para precisar».*

**S-4. El tope de la semana** · en parte · A-44 (bloqueante)
- **Lo que nos has dicho:**
  - sesión 4: «Ah, no, aquí hay un error No sería un 9% a la semana Sería un 4,5% de pérdida en el
    día» (v10 1:09:13, `ev-v10-010913-c4949417`); «para parar en un día pues con perder el 4.5
    paramos Hasta el día siguiente» (v10 1:09:50, `ev-v10-010950-7e5543df`); y, a la pregunta
    «la semana del 9% de pérdida contempla de lunes a viernes. o desde que empezó la racha de
    pérdidas», contestaste «bueno, sería desde que empezó la racha de pérdidas, ¿no?» (v10 1:10:21,
    `ev-v10-011021-02f5dcf3`);
  - sesión 3: «9 pérdidas seguidas O en un día Seguidas» (v9 1:11:39, `ev-v9-011139-a26a5b11`);
  - sesión 1, de sobre qué se mide el del día: «De la cuenta basado en el saldo, y que sea en el
    saldo inicial del día» (`fb-2026-09-09-sesion-01-bff260ea`).
- **Lo que todavía no sabemos:** si además del 4,5 % del día y de las 9 seguidas tienes un tope a la
  semana, y desde cuándo cuenta.
- **Pregunta:** «Además de parar el día con un 4,5 % perdido y de parar con 9 pérdidas seguidas,
  ¿tienes un tope de pérdida para la semana?
  - (a) no, solo el del día y las 9 seguidas;
  - (b) sí, el 9 % de la semana, de lunes a viernes;
  - (c) otra, ¿cuál?»
  - *Para Aleks: (a) cae en `perdida_trader_alcance: dia`; (b) en `ambos`, con el 9 % de
    `perdida_maxima_semanal` (CONFIRMED desde la sesión 1). «Desde que empezó la racha», si lo
    repite, no cae en ninguna lectura documentada: se PARA (`ACTIVAR-A35-A44.md` §1 y §4).*
- **Para precisar:**
  - Si no tienes tope de semana, ¿qué era el 9 % de la semana que nos dijiste en la primera
    sesión?
  - Si tienes tope de semana y lo tocas un miércoles, ¿vuelves el lunes siguiente?
- **Para confirmar al final:** «Paro el día al perder un ___ % del saldo con el que empiezo el día,
  paro tras 9 pérdidas seguidas, y a la semana ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.3, sin su segunda subpregunta (el
  saldo inicial del día ya está respondido, decisión 1 del consultor; por eso no se le pregunta si
  cuenta lo abierto). `perdida_maxima_semanal = 9` está CONFIRMED desde la sesión 1, y en la 4 dijo
  que «es un error»: la primera de «Para precisar» es esa contradicción. **Para activar A-44 hacen
  falta además `perdida_trader_magnitud` y `perdida_trader_unidad`** (UNKNOWN; `ACTIVAR-A35-A44.md`
  §1: «dia, más magnitud y unidad»), que esta pregunta no pide: la unidad sale de su «un 4,5% de
  pérdida en el día» (porcentaje, `ev-v10-010913-c4949417`) y la magnitud de «basado en el saldo»
  (saldo, `fb-2026-09-09-sesion-01-bff260ea`, que es un CORRECT sobre `perdida_maxima_diaria`, no
  sobre la magnitud). La confirmación final recoge en su voz la unidad (porcentaje) y la
  base (el saldo con el que empieza el día) de perdida_trader_magnitud y perdida_trader_unidad:
  decisión del consultor del 2026-10-19 sobre b10, porque bff260ea es un CORRECT sobre
  perdida_maxima_diaria y no basta como fuente.*

### Bloque 2 · La corrida de construcción (las preguntas 2 a 9)

**S-5. El lote que no cabe** · A-57
- **Lo que nos has dicho:** de esto, nada. Lo más cercano es de tu prueba de fondeo: «he entrado sin
  lotaje» (v4 0:24:57, `ev-v4-002457-5a2e88c6`) y «estaba operando con algo fijo es un lotaje fijo,
  muy bajo» (v4 1:29:00, `ev-v4-012900-8ef676ed`).
- **Lo que todavía no sabemos:** qué haces cuando el stop es tan corto que el lote de tu riesgo no
  cabe en la cuenta.
- **Pregunta:** «En la cuenta a la que va el bot, una orden puede llevar como mucho 50 lotes, y el
  apalancamiento es de 1:30. Cuando el stop es tan pequeño que el lote del 0,5 % pasa de lo que
  cabe, ¿qué haces?
  - (a) bajo el lote a lo que cabe y entro igual;
  - (b) no entro;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Te ha pasado en tu cuenta real? ¿Qué hiciste?
  - Si entras con menos lote, ¿cambias algo más (el stop, el objetivo)?
- **Para confirmar al final:** «Cuando el lote de mi riesgo no cabe en la cuenta, ______».
- *Para Aleks (no va a la hoja): `MARGEN-LOTE.md` §5; sustituye a la pregunta 2 de
  `CORRIDA-CONSTRUCCION.md` §4.5. Hoy el bot hace (a) (`lote_si_no_cabe = limitar`, ADR-0081,
  provisional). Si dice (b), `lote_si_no_cabe` pasa a `no_operar`.*

**S-6. Las reentradas en el mismo punto tras un stop, y su caja**
- **Lo que nos has dicho:**
  - el 29 de abril, en tu vídeo: «nos mitiga y nuevamente, pues, sería cuestión de poner otra
    reentrada aquí» (v5, en el tramo 0:03:35-0:04:15; `LA-CAJA-DEL-29-DE-ABRIL.md`);
  - sesión 3: «Sí, serían tres intentos por liquidez. [...] ¿El máximo es por día? No, no, por
    liquidez.» (v9 1:30:54, `fb-2026-09-29-sesion-03-68a21dc0`).
- **Lo que todavía no sabemos:** cuántas veces vuelves al mismo punto tras un stop, y con qué caja.
- **Pregunta** (texto de `PUNTO-USADO.md` §5, tal cual): «El 29 de abril, a las 09:55 vendiste en
  1.17064 con el stop en 1.17079, perdiste en el stop y a las 09:58 volviste a vender exactamente en
  el mismo nivel con el mismo stop ("sería cuestión de poner otra reentrada aquí"). ¿Cuántas veces
  reentras en el mismo punto tras un stop: una, dos, hasta agotar los tres cartuchos? ¿Y la caja de
  la reentrada es la del primer intento (el mismo stop) o la vuelves a trazar con lo que el precio
  hizo desde entonces?»
- **Para precisar:**
  - ¿Y tras un break even, vuelves al mismo punto?
  - ¿Cambia algo si entre el stop y la reentrada se forma otro punto de breaker?
  - ¿Repites alguna vez la entrada en el mismo nivel sin haber perdido antes?
- **Para confirmar al final:** «Tras un stop vuelvo al mismo punto ______ veces, con la caja
  ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 3 (P5 y P7), con
  `PUNTO-USADO.md` §5. Hoy el bot vuelve al mismo punto tras una pérdida o un break even, con la
  caja que diga el productor en ese cierre, hasta tres pérdidas por liquidez; tras una ganadora no
  vuelve (ADR-0083, provisional hasta esta respuesta). Las horas son de Madrid; el 29 de abril es
  de construcción.*

> **RECUADRO DE CORRECCIÓN (2026-10-21, rama `trabajo/previa-sesion-5`; encargo del consultor y su
> respuesta a la PARADA, decisión 1; `docs/validation/PREVIA-SESION-5.md` §1 y §5).** Motivo: la
> pregunta de abajo preguntaba «desde dónde trazas el 0» con opciones que son las del 1, y su esquema
> ponía el punto de breaker de una compra en un mínimo. En una compra el 0 es el punto, un ALTO de M1,
> arriba, donde va la orden de compra, y el 1 el otro extremo, abajo, del lado del stop
> (`knowledge/spec/parametros.yaml`, `orden_stop_punto`: «un BAJO en una venta»; `caja_bloque`: «el
> extremo opuesto -la maxima en una venta-»); en una venta, al revés. **Lo que va a la hoja del
> trader, y a `CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta, es el texto de este recuadro**; lo que
> no cambia («Lo que nos has dicho») se toma de abajo. El cuerpo de abajo queda intacto.
> - **Título:** «Los dos extremos de la caja: dónde pones el 0 y hasta dónde llevas el 1».
> - **Lo que todavía no sabemos:** «Hasta qué vela llevas el 1 de la caja, el extremo del lado del
>   stop, y si actualizar la caja con la vela abierta es lo que haces siempre o solo a veces.»
> - **Esquema inventado, no es un día real:** en M1, para una compra, un tramo de velas rojas
>   seguidas y después la subida. El 0, arriba, en el último alto de M1: el punto, donde va la orden
>   de compra. El 1, abajo, del lado del stop, con tres mínimos rotulados: el de la última vela roja;
>   el de todo el tramo de rojas seguidas; y el de todas las velas desde la que marca el punto hasta
>   que se pone la orden.
> - **Pregunta:** «Para esta compra, el 0 va en el punto de breaker, arriba, y el 1 en el otro
>   extremo, abajo, del lado del stop. ¿Hasta dónde llevas el 1?
>   - (a) hasta el mínimo de la última vela roja;
>   - (b) hasta el mínimo de todo el tramo de velas rojas seguidas;
>   - (c) hasta el mínimo de todas las velas desde la que marca el punto hasta que pones la orden;
>   - (d) otra, ¿cuál?»
> - **Para precisar:**
>   - «¿Y el 0: lo pones siempre en el último alto de M1 que se formó, o en el punto que marcaste en
>     la vela que tomó la liquidez?»
>   - «Dijiste que la caja "la puedes actualizar" mientras el precio avanza: ¿lo haces siempre, o
>     solo a veces? ¿Cuándo?»
>   - «En una venta, ¿es lo mismo al revés, con el 0 abajo y el 1 arriba?»
> - **Para confirmar al final:** «El 0 de mi caja va en ______, el 1 llega hasta ______, y la trazo
>   cuando la vela ______.»
> - *Para Aleks (no va a la hoja): (a) = r1, (b) = r4, (c) = r6 (el valor de hoy de caja_bloque); la
>   primera de «Para precisar» es orden_stop_punto (último alto de M1 = ultimo_pivote_m1, el valor de
>   hoy; el punto de la vela de la toma = referencia_de_la_toma); la de la vela abierta es A-49.*

**S-7. Qué vela pones como 0 de la caja, y si la trazas con la vela abierta** · en parte · A-48 y
A-49
- **Lo que nos has dicho:**
  - sesión 3: «se traza desde el posible punto de breaker, o sea el punto de breaker hasta el punto
    más alto» (v9 0:47:21, `ev-v9-004721-2e023ac6`);
  - en tus vídeos: «ya es cuando pueden ser velas consecutivas del mismo color» (v7 0:24:03,
    `ev-v7-002403-8344331d`);
  - sesión 4: «esperamos a que cierre la vela esa vela y lo trazamos desde allí» (v10 0:16:28,
    `ev-v10-001628-59a9a476`), y también «o si quieres, pues lo puedes actualizar, porque
    obviamente se ve el precio» (v10 0:19:35, `ev-v10-001935-d0f4ce50`).
- **Lo que todavía no sabemos:** si el 0 es siempre la mecha del punto de breaker o a veces otra
  vela del tramo, y si actualizar la caja con la vela abierta es lo que haces siempre o solo a
  veces.
- **Esquema inventado, no es un día real:** en M1, para una compra, un tramo de tres velas rojas
  seguidas y después la subida; el punto de breaker es el mínimo de la última roja.
- **Pregunta:** «Para esta compra, ¿desde dónde trazas el 0 de la caja?
  - (a) siempre desde la mecha del punto de breaker, el mínimo de la última vela roja;
  - (b) desde el mínimo de todo el tramo de velas rojas;
  - (c) depende, ¿de qué?»
- **Para precisar:**
  - Dijiste que la caja «la puedes actualizar» mientras el precio avanza: ¿lo haces siempre, o solo
    a veces? ¿Cuándo?
  - Si la última vela roja es muy pequeña, ¿pones el 0 en ella igual?
  - En una venta, ¿es lo mismo al revés?
- **Para confirmar al final:** «El 0 de mi caja es ______, y la trazo cuando la vela ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 4 (P2: entre la entrada
  del bot y la suya, de 4 a 52 puntos, 15 de las 18 filas entre 6 y 21), con A-48 y A-49
  (`ACTIVAR-SESION-04.md` §0.e.1). Hoy el bot: `orden_stop_punto = ultimo_pivote_m1`,
  `caja_bloque = r6`, `caja_se_fija = en_cada_cierre_m1`, todos DEFAULT_AMBIGUOUS, y solo con
  velas de M1 cerradas.*

**S-8. Una vela sin cuerpo dentro del tramo que marca el punto de breaker**
- **Lo que nos has dicho:** de una vela casi plana, «cuenta como si no existiera no se puede
  trazar, o sea allí no se puede trazar un punto de breaker» (v9 1:30:21,
  `fb-2026-09-29-sesion-03-ffab23dc`).
- **Lo que todavía no sabemos:** si esa vela sin cuerpo corta el tramo entre la verde y la roja.
- **Esquema inventado, no es un día real:** en M1, una vela verde; detrás, una o dos velas sin
  cuerpo (abren y cierran en el mismo precio); y luego una roja.
- **Pregunta:** «Después de una vela verde vienen una o dos velas sin cuerpo y luego una roja. Para
  tu orden de compra, ¿el máximo de la verde es un punto de breaker?
  - (a) sí, las velas sin cuerpo no cortan el tramo;
  - (b) no, la roja tiene que venir justo después de la verde;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si son tres velas sin cuerpo en vez de una?
  - En venta, lo mismo al revés: ¿es igual?
- **Para confirmar al final:** «Si entre la verde y la roja hay velas sin cuerpo, el máximo de la
  verde ______ es un punto de breaker».
- *Para Aleks (no va a la hoja): `VISOR-CONSTRUCCION.md` §3.2, pregunta A. Hoy el bot no ve ahí
  ningún punto. Es distinta de S-19, que va sobre la vela sin cuerpo en el retroceso.*

**S-9. Qué liquidez eliges cuando hay varias** · en parte
- **Lo que nos has dicho:**
  - «para el M1 para actualizar el punto de breaker vale la mecha y para la liquidez de M15 hace
    siempre falta cuerpo» (v9 0:42:17, `fb-2026-09-29-sesion-03-43e0f90e`);
  - «Vale, siempre la liquidez se va a ir actualizando Vamos a tratar de tomar la más reciente»
    (v10 1:46:37, `ev-v10-014637-70d27645`);
  - «Ahora, siempre el punto breaker va a ser el más reciente, el que genere, pues, la ruptura» (v10
    0:07:42, `ev-v10-000742-cd9d76b1`).
- **Lo que todavía no sabemos:** si «la más reciente» vale también cuando hay otro bajo más atrás,
  más bajo o más claro, que el precio podría ir a tomar.
- **Esquema inventado, no es un día real:** en M15, para una compra, tres bajos: uno de hace dos
  horas, más bajo; uno de hace una hora; y uno de hace media hora, el más alto de los tres.
- **Pregunta:** «Aquí hay tres bajos de M15. ¿Cuál es tu liquidez para comprar?
  - (a) el más reciente, aunque no sea el más bajo;
  - (b) el más bajo de los tres;
  - (c) el que más se vea, el más claro;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - Si el precio toma con cuerpo el más reciente y sigue bajando hacia el siguiente, ¿esperas a que
    tome ese también?
  - ¿Te fijas en algún bajo de un gráfico mayor, de 1 hora o de 4 horas?
- **Para confirmar al final:** «Cuando hay varios bajos de M15, mi liquidez es ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 5 (P3), con la de
  `VISOR-CONSTRUCCION.md` §3.2 (la compra sin toma de M15 visible para el bot). A-24 está DECIDIDA
  (ADR-0045: el más reciente ya formado); si contesta otra cosa, se le lleva al consultor. A-43,
  A-50 y A-53, que CORRIDA pone «junto», van en S-10, S-12 y S-13.*

**S-10. La misma liquidez tomada dos veces, antes y después de las 7** · en parte · A-43
- **Lo que nos has dicho:**
  - «si el precio toma ese liquidez antes de tu horario, ¿lo usas para operar a partir de las 7?
    Sí.» (v10 1:46:13, `fb-2026-10-04-sesion-04-c3d0c855`);
  - «Vale, siempre la liquidez se va a ir actualizando Vamos a tratar de tomar la más reciente»
    (v10 1:46:37, `ev-v10-014637-70d27645`).
- **Lo que todavía no sabemos:** si la misma liquidez, tomada a las 6:45 y otra vez a las 7:20,
  vale para entrar.
- **Esquema inventado, no es un día real:** en M15, un bajo. A las 6:45 una vela lo rompe con
  cuerpo; el precio vuelve por encima; a las 7:20 otra vela lo vuelve a romper con cuerpo.
- **Pregunta:** «El precio toma este bajo a las 6:45, vuelve por encima, y a las 7:20 lo toma otra
  vez. ¿Cuál es tu toma?
  - (a) la de las 7:20 vale, y opero con ella;
  - (b) esa liquidez ya se gastó a las 6:45: espero otra;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si entre las 6:45 y las 7:20 se formó un punto de breaker que no operaste?
  - ¿Y si la segunda toma es a las 6:55, todavía antes de las 7?
- **Para confirmar al final:** «Si una liquidez se toma antes de las 7 y otra vez después, mi toma
  es ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.5, solo la segunda parte. La primera
  (sí la usa) está CONFIRMED (`toma_antes_de_la_ventana = cuenta`) y no se vuelve a preguntar.*

**S-11. Una toma de la sesión de la mañana con el sesgo contrario**
- **Lo que nos has dicho:** «tú básicamente distingues ambas sesiones. O sea, cada uno es un mundo
  diferente. Claro, exacto. [...] No, no importa cómo terminó la primera operación.» (v9 0:32:53,
  `fb-2026-09-29-sesion-03-5021677e`).
- **Lo que todavía no sabemos:** qué pasa cuando la toma de la mañana iba contra el sesgo de la
  mañana y a favor del de la tarde.
- **Esquema inventado, no es un día real:** en M15, un alto. A las 10:54 una vela lo rompe con
  cuerpo; a las 11:00 cambia el sesgo de 4 horas de alcista a bajista.
- **Pregunta:** «En la sesión de 11 a 15 el sesgo es bajista, y en la de 7 a 11 era alcista. El alto
  de M15 que ahora es tu liquidez se rompió con cuerpo en la vela de las 10:54, todavía en la sesión
  de la mañana. ¿Esa toma vale para la sesión de la tarde, o esperas a que el precio tome otro alto
  después de las 11:00?
  - (a) vale, entro en la tarde con esa toma;
  - (b) no vale, espero otra;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si la toma fue en la última vela de M15 de la mañana, la que cierra a las 11:00?
  - ¿Lo miras igual al revés, con la mañana bajista y la tarde alcista?
- **Para confirmar al final:** «Una toma de la sesión de la mañana, con el sesgo de la tarde a su
  favor, ______ vale para la tarde».
- *Para Aleks (no va a la hoja): `VISOR-CONSTRUCCION.md` §3.2, pregunta B (texto tal cual). Hoy el
  bot hace (b) (ADR-0066). **A-46 está RESUELTA** («un mundo diferente»), respondida sin distinguir
  el sesgo: si contesta (a), A-46 se REABRE con un registro `REOPEN`
  (`docs/runbooks/AMBIGUEDADES.md`), no se cambia sin más. Se pregunta igual (encargo, D4). Lo que
  A-46 ya respondió (una toma de la mañana con el mismo sesgo) no se vuelve a preguntar: solo el
  sesgo contrario.*

> **RECUADRO DE CORRECCIÓN (2026-10-21, rama `trabajo/previa-sesion-5`; encargo del consultor y su
> respuesta a la PARADA, decisión 0; `docs/validation/PREVIA-SESION-5.md` §1 y §5).** Motivo: el
> segundo dibujo de abajo ponía, de una compra, «el 1 por encima y el 0 por debajo», que es imposible
> (en una compra el 0 es el punto, arriba, y el 1 el extremo de abajo: `orden_stop_punto` y
> `caja_bloque` de `knowledge/spec/parametros.yaml`); y la pregunta daba por bueno un lado del nivel
> tomado («la caja entera por encima») que es el que RN-005 llama ruido. El repo se contradice en ese
> lado y solo el trader lo puede decidir, así que S-12 pasa a tener dos partes, en este orden: el
> lado, y después la de A-50 sobre el lado que conteste. **El «Para Aleks» de abajo estaba mal**
> («opera el segundo dibujo solo si el 0 queda por encima», y en el encargo de esta rama «opera las
> dos: eso es (a)»): hoy el bot no opera ninguno de los dos dibujos; el error es del consultor
> (respuesta a la PARADA, punto 0). **Lo que va a la hoja del trader, y a
> `CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta, es el texto de este recuadro.** El cuerpo de abajo
> queda intacto.
> - **Título:** «De qué lado del nivel tomado va tu caja, y si la operas a caballo».
> - **Lo que nos has dicho:**
>   - en tus vídeos: «el precio puede o bien continuar o bien puede hacer lo que quiera, no me
>     importa nuestra operativa tiene que estar por debajo» (v1 0:13:06, `ev-v1-001306-f98e12e9`);
>   - sesión 3, de una compra: «no nos importa lo que haga por debajo, aquí no hay ninguna entrada,
>     tiene que ser todo por encima» (v9 0:49:19, `ev-v9-004919-c6bfb3ee`);
>   - sesión 4: «si la caja queda a nivel de la liquidez que se tomó, ¿descartas la entrada? Eso creo
>     que entonces a lo mejor tiene que ver con el igual [...] y no me da igual la respuesta es la ve
>     no me da igual» (v10 1:50:03, `ev-v10-015003-dd8ab1bf`, transcripción dudosa).
> - **Lo que todavía no sabemos:** en una compra, de qué lado del nivel tomado tiene que quedar tu
>   caja; y, si queda a caballo del nivel, si la operas.
> - **Primera parte, el lado.**
>   - **Esquema inventado, no es un día real:** para una compra, la línea del bajo de M15 que el
>     precio tomó, y dos cajas: una entera por encima de la línea y otra entera por debajo, sin decir
>     cuál vale.
>   - **Pregunta:** «En una compra, después de que el precio toma la liquidez de M15, ¿tu caja tiene
>     que quedar por encima o por debajo del nivel tomado?
>     - (a) por encima;
>     - (b) por debajo;
>     - (c) depende, ¿de qué?»
> - **Segunda parte, a caballo, sobre el lado que haya contestado.**
>   - **Esquema inventado, no es un día real:** la misma compra, con la caja cruzando la línea: el 0
>     arriba y el 1 abajo, uno a cada lado de la línea.
>   - **Pregunta:** «Y si la caja queda a caballo del nivel, con el 0 de tu lado y el 1 del otro, ¿la
>     operas?» Si contestó (b), por debajo: «Y si la caja queda a caballo del nivel, con el 1 de tu
>     lado y el 0 del otro, ¿la operas?» (en una compra el 0 está siempre arriba, así que con la caja
>     por debajo el lado del trader solo puede tener el 1).
> - **Para precisar:**
>   - ¿Y si el 0 queda justo en la línea, ni por encima ni por debajo?
>   - En venta, lo mismo al revés: ¿es igual?
> - **Para confirmar al final:** «En una compra, mi caja va ______ del nivel tomado, y si queda a
>   caballo, ______».
> - *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.6 y A-50. Hoy el bot sigue RN-005: en
>   una compra, la zona por encima del bajo tomado es ruido (`se_desarrolla_en_el_lado_de_ruido`, que
>   compara solo el 0: `engine/zonas.py:537-539`), y no opera ninguno de los dos dibujos del texto de
>   abajo, que tienen el 0 por encima de la línea. La respuesta a la primera parte decide si RN-005
>   sigue o se reabre; la segunda es A-50, y con (b) es justo la lectura de hoy (el 0 al otro lado es
>   ruido aunque el 1 quede del lado del trader).*

**S-12. Si la caja queda a caballo del nivel tomado** · en parte · A-50
- **Lo que nos has dicho:**
  - sesión 4: «si la caja queda a nivel de la liquidez que se tomó, ¿descartas la entrada? Eso creo
    que entonces a lo mejor tiene que ver con el igual [...] y no me da igual la respuesta es la ve
    no me da igual» (v10 1:50:03, `ev-v10-015003-dd8ab1bf`, transcripción dudosa);
  - sesión 3, de una compra: «no nos importa lo que haga por debajo, aquí no hay ninguna entrada,
    tiene que ser todo por encima» (v9 0:49:19, `ev-v9-004919-c6bfb3ee`).
- **Lo que todavía no sabemos:** si «todo por encima» es la caja entera o solo su 0.
- **Esquema inventado, no es un día real**, dos dibujos de una compra, con la línea del bajo de
  M15 que se tomó: en el primero la caja entera queda por encima de la línea; en el segundo el 1
  queda por encima y el 0 por debajo.
- **Pregunta:** «¿Operas las dos?
  - (a) las dos;
  - (b) solo la primera: la caja entera tiene que quedar por encima;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y si el 0 queda justo en la línea, ni por encima ni por debajo?
  - En venta, lo mismo al revés: ¿es igual?
- **Para confirmar al final:** «Frente al nivel tomado, lo que tiene que quedar de mi lado es
  ______».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.6. Hoy el bot mira solo el 0
  (`se_desarrolla_en_el_lado_de_ruido`, RN-005), y con eso opera el segundo dibujo solo si el 0
  queda por encima.*

> **RECUADRO DE CORRECCIÓN (2026-10-21, rama `trabajo/previa-sesion-5`; respuesta del consultor a
> la PARADA, decisión 2; `docs/validation/PREVIA-SESION-5.md` §1 y §5).** Motivo: en la segunda línea
> de «Para precisar», de una compra, el 1 de la caja es el mínimo del bloque, abajo (`caja_bloque`,
> `knowledge/spec/parametros.yaml`): mientras el precio baja a tomar otra liquidez, el 1 baja, no
> sube. **En la hoja del trader, y en `CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta, esa línea es:**
> «Si el 1 de la caja baja mucho (la caja se hace muy grande), ¿la sigues moviendo igual?» El resto
> de S-13 no cambia, y el cuerpo de abajo queda intacto.

**S-13. Hasta cuándo mueves una orden sin llenar, y cuándo la quitas** · en parte · A-53
- **Lo que nos has dicho:**
  - «si ocurre una vela verde, otra vela verde Pues simplemente lo vamos actualizando la caja
    Mientras no se desarrolle otro punto breaker» (v10 0:49:45, `ev-v10-004945-59ebac47`);
  - «sigue vivo hasta que se desarrolle otro posible punto de breaker claro, como digo, nuestro
    punto de breaker siempre va a ir en actualización» (v10 1:57:16, `ev-v10-015716-5ea2575f`);
  - del precio que toma otra liquidez con la orden puesta: «si tengo que elegir alguna opción, la
    dejo y la muevo cuando aparezca el nuevo punto de liquidez» (v10 1:58:31,
    `ev-v10-015831-fb95edf0`) y «Mientras no aparece el punto nuevo Se presiona la orden vieja ¿La
    operación vale? Sí, vale» (v10 2:01:14, `ev-v10-020114-55bdf502`); en la misma respuesta
    diste también por buena la de quitarla (`ACTIVAR-SESION-04.md`, tabla 0.a, S-21).
- **Lo que todavía no sabemos:** cuál de las dos haces cuando el precio toma otra liquidez con tu
  orden puesta, y si alguna vez la dejas quieta o la quitas antes de que acabe la sesión.
- **Esquema inventado, no es un día real:** en M1, una orden de compra puesta en el punto, sin
  llenar; el precio baja, toma con cuerpo otro bajo de M15 más abajo, y todavía no ha hecho un
  punto nuevo.
- **Pregunta:** «Con tu orden puesta sin llenar, el precio toma otra liquidez de M15. ¿Qué haces con
  la orden?
  - (a) la quito en ese momento y espero el punto de la liquidez nueva;
  - (b) la dejo, y la muevo cuando aparezca el punto nuevo; si se llena antes, vale;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Hay un tiempo máximo que dejas una orden sin llenar, aparte del final de la sesión?
  - Si el 1 de la caja sube mucho, ¿la sigues moviendo igual?
- **Para confirmar al final:** «Con la orden sin llenar, si el precio toma otra liquidez, la orden
  ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 6 (ADR-0074, S-4 de la
  sesión 4), con A-53 (`ACTIVAR-SESION-04.md` §0.e.7) y la candidata C7. C1 (la orden con una caja nueva) no se
  pregunta: la responde su propia cita, «no vamos a dejar en un punto de breaker antiguo»
  (`ev-v10-015716-5ea2575f`), con ADR-0074. Hoy el bot hace (b)
  (`orden_pendiente_al_abrir_escenario = se_mueve`, DEFAULT_AMBIGUOUS). La retirada a las 11 y a
  las 3 ya está respondida (S-22 pregunta solo el minuto).*

**S-14. Qué te hace no operar un día o una sesión**
- **Lo que nos has dicho:** de esto, todavía nada en general.
- **Lo que todavía no sabemos:** por qué hay días o sesiones de tu backtest sin ninguna operación
  en los que el bot sí opera.
- **Pregunta:** «Cuando un día o una sesión no operas nada, ¿qué suele ser?
  - (a) no hubo toma de liquidez de M15;
  - (b) hubo toma, pero ninguna zona te convenció;
  - (c) había noticias;
  - (d) no estabas delante del gráfico;
  - (e) otra, ¿cuál?»
- **Para precisar:**
  - ¿Dejas de operar una sesión si en la anterior ya ganaste o perdiste?
  - En tus backtests, ¿te saltabas alguna sesión entera a propósito?
- **Para confirmar al final:** «Si un día no opero, normalmente es porque ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 7 (P6: 33 filas, 21 en
  sesión y 12 en día; la deuda «el no_trade por ausencia no está decidido»). Las opciones dan cada
  una una causa medible; (d) es la ausencia.*

> **RECUADRO DE CORRECCIÓN (2026-10-21, rama `trabajo/previa-sesion-5`; respuesta del consultor a
> la PARADA, decisión 0; `docs/validation/PREVIA-SESION-5.md` §1 y §5).** Motivo: el «Para Aleks» de
> abajo da el lado de ruido de RN-005 por respondido con `ev-v9-004919-c6bfb3ee`, y no lo está: esa
> cita («tiene que ser todo por encima», de una compra) contradice a la de RN-005
> (`ev-v1-001306-f98e12e9`, «nuestra operativa tiene que estar por debajo»), que es lo que sigue hoy el
> bot (en una compra, por encima del bajo tomado es ruido). **Su última frase pasa a ser:** «El lado
> de ruido (RN-005) no se pregunta aquí: se pregunta en S-12, primera parte, porque RN-005 y
> `ev-v9-004919-c6bfb3ee` se contradicen.» Lo que va a la hoja de S-15 no cambia (el «Para Aleks» no
> va a la hoja), y el cuerpo de abajo queda intacto.

**S-15. Entrar en la segunda zona después de la toma**
- **Lo que nos has dicho:** de la zona limpia, «¿una zona se limpia si hay velas verdes y rojas o
  terrenos rojos? ¿Es solo eso? Claro, exacto.» (v10 1:17:25, `ev-v10-011725-3741e266`,
  `fb-2026-10-04-sesion-04-22d08cbf`).
- **Lo que todavía no sabemos:** si después de la toma, cuando el precio ya ha hecho un retroceso
  que no operaste, entras en el segundo.
- **Esquema inventado, no es un día real:** en M1, para una venta: la toma de liquidez; un primer
  retroceso (una zona) que no se opera; el precio sigue; un segundo retroceso y el punto de breaker.
- **Pregunta:** «Después de la toma, el precio hace un retroceso, sigue, y hace otro. En el segundo
  ves tu punto de breaker. ¿Entras?
  - (a) sí, si esa zona está limpia;
  - (b) no, solo entro en la primera zona después de la toma;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si el primer retroceso no estaba limpio, ¿el segundo cuenta como el primero?
  - ¿Cuántas zonas esperas, como mucho, después de la toma antes de dejarla?
- **Para confirmar al final:** «Después de la toma, entro en la zona número ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 8 (las 14 sesiones de
  §4.6), con los dos casos de `VISOR-CONSTRUCCION.md` §3.2: el bot ve el mismo punto que el trader
  y no entra porque ya cuenta dos zonas de control desde la toma (RN-009,
  `zonas_control_max_por_esquema = 1`). El lado de ruido (RN-005) no se pregunta: «tiene que ser
  todo por encima» (v9 0:49:19, `ev-v9-004919-c6bfb3ee`) ya lo dice, y lo que falta de él es S-12.*

**S-16. El precio ya está más allá del 0 cuando se forma la caja**
- **Lo que nos has dicho:** de dónde va la orden, «exactamente en el 0 contando la mecha Exactamente,
  sí [...] No depende de nada, siempre es la mecha» (v10 1:02:14, `ev-v10-010214-23a7fc0c`,
  `fb-2026-10-04-sesion-04-bbfb5c98`).
- **Lo que todavía no sabemos:** qué haces si, cuando se forma tu punto, el precio ya está por
  encima del 0 en una compra.
- **Esquema inventado, no es un día real:** en M1, para una compra: un tramo verde que termina en
  una roja pequeña que cierra en el 0 o a un punto; la vela siguiente abre ya por encima del 0.
- **Pregunta:** «Se forma tu punto y el precio ya está por encima del 0, donde iría tu orden de
  compra. ¿Qué haces?
  - (a) no entro: esa entrada se perdió;
  - (b) entro a mercado;
  - (c) pongo la orden en el 0 y espero a que el precio vuelva;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si está un punto por encima o diez?
  - En venta, lo mismo al revés: ¿es igual?
- **Para confirmar al final:** «Si el precio ya pasó el 0 cuando se forma la caja, ______».
- *Para Aleks (no va a la hoja): `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 9, con la forma de
  `VISOR-CONSTRUCCION.md` §3.2 (los cinco días de §2.g). Hoy el bróker rechaza la orden
  (`precio_invalido`, ADR-0057) y el punto se gasta (ADR-0083).*

### Bloque 3 · Las demás «en parte» y las de la sesión 4

**S-17. Cuándo pasas el stop a la entrada** · en parte · A-13
- **Lo que nos has dicho:**
  - sesión 1: «Sí, o sea, apenas toca. [...] yo siempre lo he estado trabajando, o sea, apenas
    toca» (v6 0:57:01, `ev-v6-005701-7ae2b8d3`);
  - sesión 3: «apenas toca, pues se pone en B la entrada. [...] Pues se mantiene en M1» (v9 0:55:43,
    `fb-2026-09-29-sesion-03-9f506366`; quedó registrado que después el stop no se mueve: lo FIRME
    de A-13 en `ambiguedades.yaml`);
  - sesión 4, en tu ejemplo: «cae ya apenas cierra por debajo estoy si lo hace con cuerpo mucho
    mejor entonces nosotros la entrada ya la pondríamos en break even» (v10 2:04:53,
    `ev-v10-020453-2d41dd25`), y «Pues siempre pongo exactamente en la entrada El stop» (v10
    2:04:10, `ev-v10-020410-e06f9581`).
- **Lo que todavía no sabemos:** cuando el precio rompe la zona de control que se forma después de
  tu entrada, si basta con que la toque o esperas a que la vela cierre pasada ella.
- **Esquema inventado, no es un día real:** en M1, una compra ya llenada; el precio sube, hace un
  retroceso (la zona de control) y vuelve a subir hacia el máximo de esa zona.
- **Pregunta:** «Después de tu entrada se forma esta zona de control. Para pasar el stop a la
  entrada cuando el precio la rompe, ¿esperas a que la vela de M1 cierre pasada la zona, o lo haces
  en cuanto el precio la toca?
  - (a) en cuanto toca;
  - (b) cuando cierra la vela pasada la zona, aunque sea solo con la mecha;
  - (c) cuando cierra con cuerpo pasada la zona;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - ¿Cambia algo si la zona de control es de una sola vela?
  - ¿Es lo mismo en compra y en venta?
- **Para confirmar al final:** «Pongo el stop en la entrada cuando el precio ______ la zona de
  control que se forma después de la entrada».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.2, sin «¿lo vuelves a mover?», que
  está respondida (decisión 1 del consultor). Hoy: `break_even_criterio_ruptura = mecha` y
  `break_even_condicion = tocar`, CONFIRMED; ADR-0065, al tick. Una respuesta (b) o (c) contradice
  un CONFIRMED. Qué se rompe ya está fijado y no se pregunta: la zona de control posterior a la
  entrada, no un nivel de precio (RN-014, `strategy_spec.yaml`; A-13).*

**S-18. Una línea de M1 que, rota con la mecha, te quite la entrada** · en parte · A-32 · *si
falta tiempo, a la sesión 6*
- **Lo que nos has dicho:** «Cuando, o sea, un nivel en M15, o sea, de liquidez en M15, si es roto
  con mecha, se anula la entrada, o sea, no hay entrada. Pero en M1, si tratamos de seguir el flujo
  en M1, es válido con mecha y cuerpo.» (v10 2:01:42, `ev-v10-020142-30fd2569`).
- **Lo que todavía no sabemos:** si existe alguna línea en M1 que, rota solo con la mecha, te quite
  la entrada.
- **Esquema inventado, no es un día real:** en M1, una línea horizontal dibujada; una vela la pasa
  con la mecha y cierra el cuerpo del otro lado.
- **Pregunta:** «¿Hay alguna línea en M1 que, si el precio la rompe solo con la mecha, te quite la
  entrada? ¿Cuál?
  - (a) no, en M1 la mecha siempre vale;
  - (b) sí, ¿cuál?»
- **Para precisar:**
  - ¿Dibujas en M1 líneas que no sean el punto de breaker ni la liquidez de M15?
  - Si es una línea que viene de M15, ¿la cuentas como de M15 aunque la mires en M1?
- **Para confirmar al final:** «En M1, una ruptura con mecha ______ me quita la entrada».
- *Para Aleks (no va a la hoja): `ACTIVAR-SESION-04.md` §0.e.8, en abstracto y sin el fotograma de
  v4 0:53:10 (decisión 5 del consultor).*

**S-19. Una vela sin cuerpo en medio del retroceso**
- **Lo que nos has dicho:** «¿una zona se limpia si hay velas verdes y rojas o terrenos rojos? ¿Es
  solo eso? Claro, exacto.» (v10 1:17:25, `ev-v10-011725-3741e266`).
- **Lo que todavía no sabemos:** si una vela sin cuerpo entre una verde y una roja cuenta como que
  los colores se alternan.
- **Esquema inventado, no es un día real:** en M1, el retroceso antes de romper el punto de
  breaker: una verde, una sin cuerpo, una roja.
- **Pregunta** (texto de ADR-0076 §4): «En el retroceso antes de romper el punto de breaker, si en
  medio hay una vela sin cuerpo (abre y cierra en el mismo precio) entre una verde y una roja, ¿eso
  cuenta como alternancia y te invalida la entrada, o la vela sin cuerpo no cuenta y sigues?
  - (a) cuenta como alternancia e invalida;
  - (b) no cuenta, sigo como si no estuviera;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y si la vela casi no tiene cuerpo, uno o dos puntos?
  - ¿Y si son dos velas sin cuerpo seguidas?
- **Para confirmar al final:** «En el retroceso, una vela sin cuerpo ______ cuenta como cambio de
  color».
- *Para Aleks (no va a la hoja): ADR-0076 §4, pregunta 1; `ACTIVAR-SESION-04-MOTOR.md` §5. A-21 está
  RESUELTA (la zona limpia).*

**S-20. El punto de breaker roto solo con la mecha de una vela contraria**
- **Lo que nos has dicho:** de la zona limpia, lo de S-19; y de M1: «en M1, si tratamos de seguir
  el flujo en M1, es válido con mecha y cuerpo» (v10 2:01:42, `ev-v10-020142-30fd2569`).
- **Lo que todavía no sabemos:** qué pesa más cuando una vela contraria rompe el punto con la mecha
  después de una alternancia.
- **Esquema inventado, no es un día real:** en M1, un retroceso con una verde y una roja
  alternadas; después, una vela de color contrario a la entrada pasa el punto de breaker solo con
  la mecha.
- **Pregunta** (texto de ADR-0076 §4): «Si la vela que rompe el punto de breaker es una vela
  contraria que lo pasa solo con la mecha, y antes hubo una verde y una roja alternadas, ¿la entrada
  vale o queda invalidada?
  - (a) vale, la mecha rompe;
  - (b) queda invalidada por la alternancia;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - ¿Y si no hubo alternancia antes, vale la mecha de una vela contraria?
  - ¿Importa de qué color es la vela que rompe?
- **Para confirmar al final:** «Una vela contraria que rompe el punto solo con la mecha, después de
  una alternancia, ______».
- *Para Aleks (no va a la hoja): ADR-0076 §4, pregunta 2; `ACTIVAR-SESION-04-MOTOR.md` §5.*

**S-21. La racha después de la novena pérdida**
- **Lo que nos has dicho:** «sería el día siguiente operaría ya es al día siguiente aunque las
  rachas sigue de un día a otro y una semana otra la racha sigue de un día a otro» (v10 1:08:04,
  `fb-2026-10-04-sesion-04-d1792021`, `fb-2026-10-04-sesion-04-fa5ef0f6`); y «un break even no se
  cuenta como cartucho [...] no corta la racha» (v10 1:06:53, `fb-2026-10-04-sesion-04-8e2d728a`).
- **Lo que todavía no sabemos:** si al volver al día siguiente la cuenta empieza de cero o sigue en
  nueve.
- **Pregunta** (texto de ADR-0077 §5): «Después de parar por 9 pérdidas seguidas, cuando vuelves al
  día siguiente:
  - (a) empiezas a contar de cero;
  - (b) sigues en 9 y una pérdida más te vuelve a parar ese día;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si con esa pérdida más vuelves a parar, ¿vuelves también al día siguiente?
  - ¿Te ha pasado en tus backtests o en tu cuenta?
- **Para confirmar al final:** «Al día siguiente de parar por 9 pérdidas, la racha empieza en
  ______».
- *Para Aleks (no va a la hoja): ADR-0077 §5 (lectura PROVISIONAL de la sesión: hoy el bot hace
  (b)); `ACTIVAR-SESION-04-MOTOR.md` §5.*

**S-22. El último minuto: a qué hora quitas la orden sin llenar**
- **Lo que nos has dicho:**
  - de la orden: «a ver si a las 11 tienes la orden puesta que no se ha llenado [...] claro, se
    quita [...] sí, se quita, porque siempre se va a ir actualizando la orden» (v10 0:54:27,
    `ev-v10-005427-1a0867af`, `fb-2026-10-04-sesion-04-766c8d2e`);
  - de la operación abierta: «siempre menos un minuto, antes de que cierre, pues, como tal, la
    sesión de cuatro horas» (v9 0:27:35, `ev-v9-002735-472432b8`).
- **Lo que todavía no sabemos:** el momento exacto en que quitas la orden sin llenar: con la
  operación abierta, un minuto antes, o a la hora en punto.
- **Pregunta** (texto de `ACTIVAR-SESION-04-MOTOR.md` §5): «Cuando llega la hora de cerrar -las 11 o
  las 3 en punto- y tienes una orden puesta que no se ha llenado, ¿en qué momento la quitas?
  - (a) a las 11 y a las 3 en punto, justo cuando cambia la vela;
  - (b) un minuto antes, cuando cierras la operación que tengas abierta;
  - (c) otra, ¿cuál?»
- **Para precisar:**
  - Si la orden se llena en ese último minuto, ¿la dejas o la cierras en seguida?
  - ¿Pones órdenes en el último minuto antes de las 11 o de las 3?
- **Para confirmar al final:** «A la hora de cerrar, quito la orden sin llenar a las ______».
- *Para Aleks (no va a la hoja): RN-035, tramo `ventana_fin`. Para la ORDEN, «un minuto antes» lo
  dijo el consultor en la sesión 4, no el trader (`ACTIVAR-SESION-04.md`, tabla 0.a, S-5); para la
  OPERACIÓN abierta lo dijo el trader en la sesión 3 (`ev-v9-002735-472432b8`;
  `cierre_h4_antelacion = 1`, CONFIRMED), y eso no se pregunta.*

### Bloque 4 · Confirmaciones cortas

**S-23. La vela de 4 horas sin color, con el sesgo bajista** · *si falta tiempo, por WhatsApp*
- **Lo que nos has dicho:** «si esta es una vela neutra, si esta es una vela neutra, no tiene ningún
  color, nosotros seguiríamos operando alcistas» (v10 1:40:05, `ev-v10-014005-7e2228f4`).
- **Lo que todavía no sabemos:** si con el sesgo bajista es igual. Lo dijiste con el sesgo alcista.
- **Esquema inventado, no es un día real:** dos velas de 4 horas. La primera, roja (sesgo bajista).
  La segunda rompe por arriba y por abajo y cierra sin color.
- **Pregunta** (texto de `ACTIVAR-SESION-04.md` §5): «Si la vela de 4 horas sin color viene con un
  sesgo bajista, ¿también se mantiene el bajista?
  - (a) sí, se mantiene el bajista;
  - (b) no, ¿qué pasa?»
- **Para precisar:**
  - ¿Y si la vela anterior a esa también era neutra?
  - ¿Lo miras igual al principio de la semana, con la primera vela de 4 horas del lunes?
- **Para confirmar al final:** «Con el sesgo bajista, una vela neutra de 4 horas deja el sesgo
  ______».
- *Para Aleks (no va a la hoja): ADR-0075; reserva anotada en `fb-2026-10-04-sesion-04-ca0afae6`.
  Hoy el bot hace (a).*

**S-24. La vela casi plana: de cuántos puntos**
- **Lo que nos has dicho:**
  - «cuenta como si no existiera no se puede trazar, o sea allí no se puede trazar un punto de
    breaker» (v9 1:30:21, `fb-2026-09-29-sesion-03-ffab23dc`);
  - en la sesión 4: «Es casi plana con 1 o 2 puntos, bueno, sí, podría considerarse casi, entre
    comillas, casi plana con 1 o 2 puntos del cuerpo o menos» (v10 1:43:10,
    `ev-v10-014310-2296423b`); y un minuto después, según cómo se oiga: «ahora si es casi plana con
    12 puntos ahí sí habría un pequeño cuerpo» (v10 1:44:38, `ev-v10-014438-95464201`,
    transcripción dudosa).
- **Lo que todavía no sabemos:** a partir de cuántos puntos de cuerpo una vela deja de ser casi
  plana. Lo que dijiste se puede oír de dos maneras: «1 o 2 puntos» o «12 puntos».
- **Esquema inventado, no es un día real:** tres velas de M1 con cuerpos de 1, 2 y 12 puntos.
- **Pregunta:** «¿Cuál de estas es casi plana, y no la usas para trazar un punto de breaker?
  - (a) solo la de 1 punto;
  - (b) las de 1 y 2 puntos;
  - (c) las tres, también la de 12;
  - (d) otra, ¿cuál?»
- **Para precisar:**
  - ¿Miras solo el cuerpo, o también las mechas?
  - ¿Es lo mismo en M15?
- **Para confirmar al final:** «Una vela de M1 es casi plana si su cuerpo es de ______ puntos o
  menos».
- *Para Aleks (no va a la hoja): RN-007, NA:H. El literal de 1:44:49 lo lee Aleks en su terminal;
  hasta que lo diga, la pregunta lleva las dos lecturas sin elegir (D7). Si lo lee antes de la
  sesión, el esquema se queda igual: las tres velas no sugieren ninguna.*

**S-25. El Excel de julio y los tres primeros vídeos** · *si falta tiempo, por WhatsApp*
- **Lo que nos has dicho:** nos lo comentaste de palabra el 13 de octubre, sin grabar.
- **Lo que todavía no sabemos:** que quede grabado.
- **Pregunta:** «El Excel de julio que nos mandaste, ¿es la exportación de los tres primeros vídeos
  de julio, los del 1 al 17?
  - (a) sí;
  - (b) no, ¿de cuáles?»
- **Para precisar:**
  - ¿Y el cuarto vídeo, el del final del mes, no tiene Excel?
  - ¿Hiciste todos los días de julio, o te saltaste alguno?
- **Para confirmar al final:** «El Excel de julio es la exportación de ______».
- *Para Aleks (no va a la hoja): `ENTRADA-JULIO.md` §8 y «Datos para la fase 3», punto 4. La rama
  de T (transcribir v11 a v14) lo comprobará además midiendo. La segunda de «Para precisar» no pide
  ninguna fecha.*

## 2. Para cerrar (sin código de voz)

Lo que no es de la operativa y hay que pedirle al trader. Ninguna fecha de ningún día.
- **Diciembre:** «El backtest de diciembre que nos mandaste, ¿lo grabaste en vídeo con tu voz, como
  los otros meses?» (NA:I: llegó sin vídeo; la respuesta la necesita el consultor para decidir si
  diciembre es construcción o reservado).
- **Agosto:** que mande la exportación del backtest de agosto que da por bueno, el grabado en vídeo
  (NA:Q; S-16 de la sesión 4).
- **Marzo:** que mande **por escrito** que el backtest de marzo es material que ya ha visto
  (`docs/validation/REGISTRO-MARZO.md` §2, paso 0; F09). Decirlo en voz no basta: tiene que ser
  escrito.

## 3. Lo que no va en la hoja

- **A-16, A-28, A-54, A-55 y A-56** son mediciones: se miden (demo de FTMO, la respuesta de FTMO,
  F26), no se preguntan.
- **RN-004 tras A-35 y RN-020 tras A-44** son la medida de después de activar
  (`docs/runbooks/ACTIVAR-A35-A44.md` §5.1), no preguntas.
- **Los dos pendientes de `feedback pending`** (`fb-2026-09-29-sesion-03-31fb311f` y
  `fb-2026-10-04-sesion-04-ca0afae6`, los dos CORRECT sobre RN-003) son el falso positivo de
  `docs/plan/HOJA-DE-RUTA.md` G.2, no respuestas por reflejar. El caso bajista del segundo es S-23.
- **Las candidatas C4, C5 y C6** tienen su ambigüedad RESUELTA (A-18, A-29, A-36); el consultor
  sacó C4 y C6 de la lista. C1 y C7 van dentro de S-13; C2 y C3 son A-48 y A-49 (S-7).
- **A-24** está DECIDIDA (ADR-0045); lo que tiene de pregunta lo cubren S-3 y S-9.
- **S-6 de la sesión 4** (el redondeo del stop) y **A-21** (la zona limpia): sacada por el consultor
  y RESUELTA.

## Estado

Escrito el 2026-10-19 con las decisiones del consultor a la PARADA de la fase 0. **25 preguntas**
(4, 12, 6 y 3 por bloque), **3 peticiones** en «Para cerrar» y **9 cosas fuera de la hoja**, con
su porqué. Ninguna cambia nada del motor, de la spec, de las ambigüedades ni del feedback; las
respuestas entran después, por la grabación y un registro por respuesta
(`docs/runbooks/SESION-DE-PREGUNTAS.md`, «Después»).
