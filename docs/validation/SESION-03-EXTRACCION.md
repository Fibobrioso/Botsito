# Sesión 03 con el trader: extracción de respuestas

> **Borrador. Nada se resuelve sin revisión del consultor.** Esta rama no activa ninguna regla, no
> cambia ningún parámetro y no crea ningún registro de feedback: cada «propuesta» de abajo es solo
> eso, y lo que tocaría se hará en otra rama después de la revisión (brief del 2026-09-29).

Rama `trabajo/sesion-03`, desde `main` 6cc88f4. Grabación de la sesión 3 (preguntas y respuestas),
ingerida como vídeo **v9** del corpus. Plantilla: `SESION-02-EXTRACCION.md`.

## 0. Lo primero

**El vídeo.** v9, `Grabación de pantalla 2026-09-29 164102.mp4`, 6.981.253.429 bytes, sha256
`dd4d730e…e964c45`, 1:44:34 (6273,9 s; vídeo y audio duran lo mismo). Registrado en
`knowledge/corpus/fuentes.yaml` e inventariado (`manifest.yaml`). Tiene 6274 fotogramas a 1 fps
(`fr-v9-8e4d4e98`) y una transcripción con el mismo motor que los demás vídeos
(`tr-v9-large-v3-int8-float16-dcd6e5bd`, 1664 segmentos). **Tiene dos cortes de audio de cero
digital**, de 28:49 a 29:53 y de 57:00 a 58:06 (§2). El consultor decidió seguir con este vídeo
(2026-09-29, opción 1).

**Preguntas hechas: las 29 de la hoja, todas**, en el orden de la hoja. Ninguna se quedó sin
preguntar. Tres no reciben respuesta útil (A-24, A-50 en su punto clave y E-1 en cuál de las dos
versiones vale); las demás se responden entera o parcialmente (tabla del §5).

**El protocolo de voz no se siguió, y la localización es a mano.** Los códigos se dijeron sueltos
(«A47», «A39», «Una A46», «A45…»), nunca con «pregunta» delante, y nunca se dijo «fin de pregunta».
La detección estricta de `scripts/transcribir_sesion.py`, que se amplió en esta rama para reconocer
E, S y G con su test, detectó **0 preguntas**, que es lo correcto: aflojarla para que casara un
código suelto devolvería los 17 falsos positivos de la sesión 01. Cada respuesta se localizó a mano
en la versión filtrada, usando como anclas esos códigos sueltos o el texto de la pregunta leída.
S-1, A-34, A-26 y G-2 no se nombraron; se localizan por el texto que se leyó. De E-3 solo queda una
marca ininteligible del ASR («vamos 5 a 5 más y 3…», 89:28).

**Holdout.** Se marcaron **11 tramos** en `tramos_no_citables.yaml`: 8 de la cuarentena mecánica y 3
por precaución. No se citan ni se describen. Además están los 2 tramos sin audio. Ningún fotograma
de v9 se abrió en esta rama. Declarado en `HOLDOUT-EXPOSICIONES.md`.

**Los cinco hallazgos que más cambian el bot** (en el orden del brief; el detalle, en el §3):

1. **Sesgo (S-1, A-34, A-26, A-39).**
   - «Siempre va a haber un sesgo», y no existe un sesgo no claro (15:29). Si la vela H4 rompe los
     dos extremos, decide su color (16:19).
   - Hoy el bot NO opera con sesgo AMBIGUO, que es 15 de 84 sesiones de construcción (RN-033,
     ADR-0044).
   - Además, cada operación se cierra un minuto antes de que venza su vela H4 (10:59 y 14:59 del
     gráfico), aunque el sesgo siguiente sea el mismo. Hoy el bot solo cierra al fin de la ventana
     (RN-002).
2. **Reentrada (A-46).** Las dos sesiones son «cada uno un mundo diferente» (32:56). No importa cómo
   terminó la primera operación (33:08), y no hay un máximo de escenarios por día: cada toma de
   liquidez de M15 puede dar una operación (33:18–33:38).
3. **Gestión (A-13, G-1, G-2, A-18, G-3).**
   - El break even se pone al tocar, en M1, exactamente en la entrada. Después, el stop se queda
     quieto.
   - No cierra a mano, y el objetivo es fijo: «o se gana o se pierde».
   - El objetivo es 3 veces la distancia del 0 al 1. El lote se calcula del 0 al 0,8, con el 0,5 %
     medido en el 0,8. Eso es la forma que ya tiene hoy el bot (y la V2 de VIABILIDAD-COMISION).
   - Una diferencia medida: el trader redondea el 0,8 **hacia fuera**, lo mínimo posible, y el bot
     trunca **hacia la entrada** (`ROUND_DOWN` en `escribir_stop_en_la_orden`).
   - No hay tamaño mínimo de caja.
4. **A-47.** «Aquí queda confirmado que se entra siempre por stop» / «Sí, exacto» (01:24–01:29). La
   orden se pone después de la toma de liquidez, sobre el posible punto de breaker, y se actualiza
   si se invalida o con el flujo.
5. **A-50.** La caja se traza desde el posible punto de breaker hasta el punto más alto, y todo tiene
   que desarrollarse más allá del nivel tomado. Pero a la pregunta concreta, «¿el 0 o el 1?», responde
   «no importa» y remite a sus ejemplos (51:23–51:30). **No resuelve A-50.**

## 1. Cómo se leyó

- `scripts/transcribir_sesion.py --solo-filtrar` sobre la cruda de v9. La cuarentena mecánica dio 29
  segmentos en 8 bloques. Solo se leyó la versión FILTRADA, fuera del repositorio; la cruda
  (`*.cruda-NO-LEER.*`) no se abrió. Los índices y motivos de los bloques salieron de un script que
  no imprime texto.
- Citas: el literal de la filtrada, con su `mm:ss` desde el inicio del audio.
- **La cruda no separa voces.** El hablante se atribuye por contexto: la pregunta la lee el
  consultor, la respuesta es del trader. Donde una línea mezcla a los dos se dice. Los ítems de
  evidencia lo declaran en `revisado_por`, y los que recogen una confirmación («Sí», «Claro,
  exacto») lo dicen en la afirmación.
- **La frase de confirmación.** En la sesión se leyó casi siempre como «para precisar…», y alguna
  vez como una paráfrasis del consultor que el trader confirma. En cada código se dice si la hubo y
  con qué palabras respondió.
- **Ítems de evidencia: 62**, todos `ev-v9-*`, creados con `botsito evidence new` (voz, extractor
  `llm`). El check mecánico de citas los aceptó; ninguno cae en un tramo no citable.
  `botsito evidence contradictions`: 0 contradicciones abiertas. Solo compara `valor` dentro de un
  mismo tema: las contradicciones de sentido son las del §4.
- **Sin registros de feedback.** El paso 5 del runbook (`feedback new` … `RESOLVE_UNKNOWN`) cierra
  cosas, y el brief dice que en esta rama no se resuelve nada. Esos registros van en la rama de
  después, con la revisión del consultor.
- **Códigos de sesión.** Desde la revisión del consultor (2026-09-29) están definidos, con el texto
  de la hoja, en `scripts/transcribir_sesion.py` (`CODIGOS_DE_SESION_TEXTO`). Al escribir el
  borrador, E-1, E-2 y E-3 no estaban definidos en ningún fichero y su significado se tomó de la
  grabación; coincide con la hoja.
  - S-1 = cómo decide el sesgo del día; G-1 = cerrar antes del stop; G-2 = dejar correr más allá del
    objetivo; G-3 = tamaño mínimo de caja.
  - E-1 = tus dos backtests de los mismos días (dicho a las 82:47);
  - E-2 = cómo operas los equals (86:38);
  - E-3 = cuando la vela cambia de color (89:28; en la sesión se preguntó además por la vela casi
    plana, 89:51).

## 2. Los dos cortes de audio y el audio de respaldo

| Corte | Pregunta en curso (marcadores) | Qué se oye justo antes y justo después | ¿Pudo tapar una respuesta o una confirmación? | Marca |
|---|---|---|---|---|
| **28:49–29:53** (1729,3–1793,1 s) | **A-39** (bloque de sesgo): «A39» a las 26:19; la siguiente, «Una A46», a las 30:36 | antes, 28:17 «pero un momento, vale, ahora vengo, voy a tomar agua»; después, 29:59 el consultor repregunta «y para precisar si el sesgo de la segunda sesión es el mismo…» | La respuesta principal (se cierra al vencer la vela H4) está antes del corte, y la confirmación, después (30:28). El corte coincide con una pausa anunciada, pero no se puede saber si en ese minuto se dijo algo. | **respuesta incompleta por audio** |
| **57:00–58:06** (3420,3–3486,1 s) | **A-13** (bloque de gestión): «gestión operativa a 3…» a las 51:38; la siguiente, «Estamos en el A40», a las 58:36 | antes, 56:44–56:50 una pausa («Para el cobro», «Me dijiste que vuelves, ¿no?»); después, 58:30 «Listo, bro. Volví.» | Las respuestas de A-13 y sus dos repreguntas (temporalidad y nivel) están antes del corte (56:12–56:41). Tampoco aquí se puede saber si se dijo algo en el corte. | **respuesta incompleta por audio** |

No se miró ningún fotograma de esos dos tramos. Los dos están en `tramos_no_citables.yaml` con
motivo «SIN AUDIO». También están en la `naturaleza` y en el comentario de procedencia de v9 en
`fuentes.yaml`. El inventario generado (`manifest.yaml`) no tiene campo de notas.

**Cómo añadir más adelante un audio de respaldo** (la grabación del móvil) **para rellenar SOLO esos
dos tramos.** Es solo el procedimiento: no existe herramienta para esto (el rescate de v8 fue a mano
con ffmpeg) y aquí no se implementa.

1. **Registrar el audio del móvil como fuente propia.** Entrada nueva en `fuentes.yaml`, con su hash,
   sus bytes y su `naturaleza` («respaldo de v9 para 28:49–29:53 y 57:00–58:06»). Ni el audio de v9
   ni su cruda se tocan: el manifiesto `tr-v9-…` y la cruda son inmutables.
2. **Medir el desfase entre los dos relojes.** Correlación cruzada de la envolvente de audio sobre
   una ventana común de 2–3 minutos antes de cada corte, y otra después; los dos desfases tienen que
   coincidir a unas décimas. Si no coinciden (el móvil deriva), se usa el desfase de cada corte por
   separado. Se anota en el informe con la cifra medida.
3. **Cortar del respaldo solo las dos ventanas**, con un margen de 10 s por lado, por tiempo de v9 más
   el desfase. El ensayo se hace en un `git worktree` temporal, y la raíz de salida sale de una
   variable de entorno, no de `sed` (CLAUDE.md).
4. **Transcribir esas dos ventanas con el mismo motor** (`large-v3`, `int8_float16`) y pasarles la
   **misma cuarentena mecánica** (`scripts/transcribir_sesion.py`) antes de que nadie las lea.
   Después se desplazan los tiempos al reloj de v9.
5. **Guardarlo como artefacto complementario**, con su propio manifiesto (`tr-v9r-…` o equivalente):
   segmentos solo dentro de los dos tramos, y referencia al audio de respaldo y al desfase medido.
   No se reescribe la cruda de v9.
6. **Estrechar o quitar las dos entradas «SIN AUDIO»** de `tramos_no_citables.yaml` en un commit con
   `Fuente:`. Una evidencia de esos minutos cita la transcripción de respaldo con `--transcripcion`,
   nunca la cruda de v9. Pero hoy `evidence new` exige que la transcripción citada sea la
   ACTIVA de su vídeo (medido en `src/botsito/cli.py`, la comprobación contra `activas`), y un vídeo
   tiene una sola activa. Por eso el paso 5 obliga a decidir antes entre dos caminos. El primero es
   registrar el respaldo como un vídeo nuevo del corpus (`v10`, con su propia transcripción activa),
   que no toca código. El segundo es una transcripción complementaria de v9, que toca `corpus` y
   `evidence`, porque convertirla en la activa dejaría sin validar los 62 ítems que citan la de hoy.
7. **Releer A-39 y A-13 solo en esos minutos** y cambiar su marca «respuesta incompleta por audio»
   con un recuadro de corrección en este informe.

## 3. Los cinco hallazgos, con su cita

### 3.1 Sesgo (S-1, A-34, A-26, A-39)

- **La vela anterior da el sesgo, y el sesgo es un rango.** 06:51–06:58: «que la vela anterior / o
  sea / la sesión que tú vas a operar / va a ser tu / tu bias». Y 09:04–09:12: «el sesgo es alcista
  / mientras que / no se mitigue, pues, con mecha o con cuerpo / por debajo de esta vela / que es
  nuestro rango». Basta un pip (13:14–13:18: «romper con mecha, con una mecha / base inclusive con
  un pip»). Coincide con RN-003.
- **No cambia dentro de la sesión.** 15:05–15:07: «para nosotros poder cambiar el sesgo / tendría que
  finalizar la vela de H4». Coincide con RN-003 («no cambia dentro de ella»).
- **Siempre a favor, y siempre hay sesgo.** 15:25–15:27: «no, o sea siempre es a favor del sesgo de
  H4 / no se puede operar en contra». 15:29: «Siempre va a haber un sesgo, bro, como te digo, o sea,
  no existe un cejo no claro».
- **Doble ruptura: decide el color** (A-34). 16:19–16:23: «importa el color de / importa el color de
  la vela». 17:49: «si llega a cubrir, o sea, a envolver tanto por arriba como por debajo, y en este
  caso cierra con cuerpo, pues la siguiente operativa va a ser bajista».
- **LO QUE CAMBIA EN EL BOT.** RN-003 declara AMBIGUO el sesgo con doble ruptura, y RN-033 prohíbe
  operar con él. Es una decisión conservadora del consultor (ADR-0044 §1-2), y la nota de RN-033 ya
  dice que «si el trader lo da, `ambiguo` desaparece». Medido sobre construcción el 2026-09-25: 15
  sesiones ambiguas de 84. La respuesta de A-34, más «siempre hay sesgo», deja RN-033 solo para
  `insuficiente`, que con `sesgo_h4_tope_velas` = 60 es residual (0 en construcción).
- **Cierre al vencer cada vela H4** (A-39). 27:35: «…siempre menos un minuto, antes de que cierre,
  pues, como tal, la sesión de cuatro horas»; 28:08: «si no ha llegado al objetivo, pues no importa,
  se cierra a las 12.59»; 30:28: «Indiferentemente se cierra, sí, si el sesgo es el mismo». Las
  horas que dice (10:59, 11:59, 12:59) se mezclan: el ASR, o el propio trader contando en dos
  relojes (A-42). Lo firme es «menos un minuto antes de que cierre la sesión de cuatro horas». Hoy
  la spec solo cierra al fin de la ventana (RN-002); `ev-v3-010304-4468cc20` ya lo decía y ninguna
  regla lo cita.

### 3.2 Reentrada (A-46)

32:42–32:58: «de 7 a 11 es, claro, la primera sesión / La segunda sesión, pues, de 11 a 3.» — (consultor)
«tú básicamente distingues ambas sesiones. / O sea, cada uno es un mundo diferente.» — (trader)
«Claro, exacto.» 33:08: «No, no importa cómo terminó la primera operación.» 33:18: «Pues, eso no lo
podemos definir.», y 33:26–33:38: «a cuantas tomas de liquidez / puede haber en M15 / por ejemplo
para esta sesión / tenemos 1, 2, 3 y 4 / y claro / en todas estas 4 se va a dar / una operación».

La pregunta leída (30:51) dice que el bot «traza una sola zona por día y no vuelve a buscar otra».
La respuesta es que cada toma nueva de M15 abre un escenario, sin tope de escenarios por día, y que
cada sesión es independiente. Lo segundo choca con el motor: `liquidez_tomada` no caduca al abrir la
sesión (nota de A-46 en `ambiguedades.yaml`), y solo `sesgo` caduca.

### 3.3 Gestión (A-13, G-1, G-2, A-18, G-3)

- **Break even al toque, en M1, en la entrada exacta.**
  - 55:48: «apenas toca, pues se pone en B la entrada.»
  - 56:12: «…con que el precio la toque, con que el precio la toque.» Es una línea mezclada: el
    consultor lee las opciones y el trader elige.
  - 56:21: «Pues se mantiene en M1, o sea, se mantiene en M1.»
  - 56:31–56:39: «a entrada, a entrada. / … / Yo he estado trabajando así, a entrada.»
- **El stop, quieto después del break even.** 58:56: «no hemos no no definimos parciales o sea lo
  dejamos ahí quieto».
- **Sin cierre a mano, y objetivo fijo.**
  - 59:23: «no cierro o sea yo dejo para hacerlo más lo más objetivo posible»; 59:32–59:39: «o bien
    se gana / o bien se pierde. O bien / ocurre break-even».
  - 60:53–61:00: «el objetivo es fijo / como bien sabemos bro / Ahora no lo gestionamos / Es fijo».
  - La única excepción que acepta es el cierre al vencer la sesión (59:39–59:49).
- **A-18.**
  - 62:32–62:49: el objetivo «desde el punto 0 al punto 1. / Y el objetivo es original 1, 3.»
  - 63:09–63:14: el lotaje «se calcularía a partir del 0 al 0.8.» Lo mismo a las 25:28–25:39: «hacer
    el cálculo en base a 1 / … / pero el cálculo del lotaje a 0.8».
  - 64:16–64:21: «¿El riesgo de 0.5 lo calculas con el stop en 1 o con el stop en 0.8? 0.8,
    ¿verdad?» — «Sí.»
  - Es lo que el bot ya hace: RN-011 dimensiona el lote hasta el stop, el 0,8 (ADR-0020); RN-015 con
    `base_calculo_objetivo: caja_completa` y `objetivo_rr: 3`. Es la V2 de
    `VIABILIDAD-COMISION.md`.
  - **La diferencia medida es el redondeo.** El trader, a la pregunta de hacia dónde (64:30–65:47):
    «Claro, tener un margen extra.» … «Claro, o sea, lo mínimo / O sea, lo mínimo posible / O sea, si
    es un pip, un pip y ya está».
  - El bot: `escribir_stop_en_la_orden` calcula la distancia del 0,8 con `ROUND_DOWN`
    (`src/botsito/engine/primitivas_broker.py:306`). Eso acerca el stop a la entrada, lo contrario.
- **G-3.** 66:20–66:22: «No existe / Yo creo que no / O sea, no existe como tal»; 66:31: «No, o sea,
  me es indiferente».

### 3.4 A-47

01:24: (consultor) «aquí queda confirmado que se entra siempre por stop» — 01:29 (trader) «Sí,
exacto». 01:43–01:46: «Lo primero es que primero se desarrolla una toma de liquidez / Para recién
nosotros poder trazar los posibles puntos de breaker». 05:38–05:45: «si invalida ese trade, pues se
va actualizando. / O si no, se va actualizando simplemente por el flujo de precio.» Coincide con lo
que se ve en pantalla en v7 y v8 (`ev-v7-000423-01b2c18a`, `ev-v8-003620-12670f0e`,
`ev-v8-003935-0a0b3f8e`). Choca con la palabra «límite» de `ev-v1-001358-a2b8ec0d`,
`ev-v3-002511-b12d67be` y `ev-v3-004201-bfeb3734`, y del texto de RN-006 y RN-011. El trader
también la dice en esta sesión: «alterizar la orden límite», 94:46. Es su vocabulario, no el tipo
de orden.

### 3.5 A-50

47:21–47:30: la caja «se traza desde el posible / punto de breaker, o sea el punto de breaker /
hasta el punto más alto». 49:20–49:25: «no nos importa lo que haga por debajo, aquí no hay ninguna
entrada, tiene que ser todo por encima / o sea, a partir de encima que se desarrolle». Y a la
confirmación (51:08–51:12, «¿Qué parte de la caja tiene que quedar más allá del nivel tomado? ¿El 0?
¿El 1? ¿La caja entera o no importa?»): 51:23 «¿El 0 o el 0? No, no importa», y 51:25–51:30 «Es que
como digo / Espero que con / Los ejemplos que he dado / Pueda corregir». «No importa» contesta en
contra de las dos opciones a la vez y remite a los ejemplos, así que **no resuelve**.

## 4. Pregunta por pregunta

Formato: **Citas** (literal de la filtrada) · **Resumen** · **Confirmación** · **Contradicciones**
(con ids) · **Propuesta** (qué tocaría) · **Ítems** creados.

### A-47 · el tipo de orden de entrada, stop o límite

- **Citas:** 00:48 (consultor) «A47, confirmación, tu orden entra cuando el precio rompe»; 01:24
  (consultor) «aquí queda confirmado que se entra siempre por stop» / 01:29 «Sí, exacto»; 01:43–01:46;
  05:38–05:45 (§3.4).
- **Resumen:** entra siempre con orden stop en la ruptura del punto de breaker; la orden se pone tras
  la toma de liquidez y se actualiza si se invalida o con el flujo.
- **Confirmación:** sí: «Sí, exacto» (01:29).
- **Contradicciones:** la palabra «límite» en `ev-v1-001358-a2b8ec0d`, `ev-v3-002511-b12d67be` y
  `ev-v3-004201-bfeb3734`, y en RN-006 y RN-011. Coincide con `ev-v7-000423-01b2c18a`,
  `ev-v8-003620-12670f0e` y `ev-v8-003935-0a0b3f8e`.
- **Propuesta:** **resuelve**.
  - `entrada_tipo_orden` = `stop_en_ruptura`, vía feedback.
  - A-47 pasa a RESUELTA, y el texto de RN-006 y RN-011 pasa de «orden límite» a «orden stop».
  - El broker con órdenes stop (ADR-0057) y el selector de A-47 (ADR-0058, PROVISIONAL, tag
    `stable/F23-selector-orden-stop`) ya están en `main`. Solo falta fijar el valor del parámetro.
- **Ítems:** `ev-v9-000124-d2afa992`, `ev-v9-000143-214aacde`, `ev-v9-000538-4bbf1c16`.

### S-1 · cómo decide el sesgo del día

- **Citas:** 06:51–06:58; 09:04–09:12; 10:32–10:40 «el sesgo va a estar cambiando / solo se va a
  mantener el sesgo / y entra en un rango / de una vela y no cumple los criterios / de invalidación»;
  13:14–13:18; 15:05–15:07; 15:25–15:27; 15:29 (§3.1).
- **Resumen:** el sesgo lo da la vela H4 anterior; se mantiene mientras el precio siga dentro del
  rango de esa vela; cambia cuando se rompe con mecha o cuerpo, aunque sea por un pip; no cambia
  dentro de la sesión; nunca se opera en contra, y siempre hay un sesgo.
- **Confirmación:** no hubo frase de confirmación explícita. Contesta a tres repreguntas: otras
  temporalidades (14:05, responde sobre las noticias, 14:35–14:40), cambio a mitad de sesión (15:05) y
  operar en contra (15:25).
- **Contradicciones:** con RN-033 y ADR-0044 §1-2 (con sesgo ambiguo o insuficiente no se opera)
  frente a «siempre va a haber un sesgo». Coincide con `ev-v3-000531-4d6375b6`,
  `ev-v2-000836-6dbfcd6b`, `ev-v3-010948-331c69aa`, `ev-v1-000126-ffb9640c` y
  `ev-v4-003431-3968a5ca`.
- **Propuesta:** **resuelve en parte**. S-1 no es una ambigüedad del registro. Confirma RN-003, y
  junto con A-34 **toca RN-033 y ADR-0044** (§3.1). Queda por medir si «el rango de una vela» del
  trader es lo mismo que la búsqueda hacia atrás de `sesgo_h4_al_abrir`.
- **Ítems:** `ev-v9-000651-6a11b3a1`, `ev-v9-000902-25db5bf5`, `ev-v9-001312-19e45e4a`,
  `ev-v9-001504-72aa462a`, `ev-v9-001522-8b8c4942`, `ev-v9-001529-ac28bb40`.

### A-34 · vela H4 previa que rompe ambos extremos

- **Citas:** 15:53–16:01 (pregunta leída); 16:19–16:23; 16:25–16:37 «O inclusive, si luego se
  devuelve / y no cierra por debajo con un cuerpo / pero la vela es roja / es que la siguiente /
  sesión, o sea, de H4 / … / va a ser bajista»; 17:49.
- **Resumen:** si la vela rompe los dos extremos, decide el color con que cierra: roja → bajista,
  verde → alcista.
- **Confirmación:** no hubo frase de confirmación aparte; la respuesta es directa y la ilustra en el
  gráfico.
- **Contradicciones:** con RN-003 y RN-033 (hoy el sesgo es AMBIGUO y no se opera, ADR-0044). La
  nota de RN-003 «el color de la vela NO decide» sigue valiendo para la ruptura de un solo extremo.
  Coincide con `ev-v3-001508-e1a49a38` y con la simplificación abierta de `ev-v3-011614-a5a05b0a`.
- **Propuesta:** **resuelve**.
  - Toca RN-003: en la doble ruptura decide el color de la vela.
  - Toca RN-033: `ambiguo` desaparece, y la regla queda para `insuficiente`.
  - A-34 pasa a RESUELTA, y el ADR que enmienda ADR-0044 §1.
- **Ítems:** `ev-v9-001617-4b47e01a`.

### A-26 · el flujo de M15 cuando va contra el sesgo de H4

- **Citas:** 19:17–19:25 «nosotros el sesgo ya nos define / Qué vamos a buscar / Luego nos enfocamos
  solo en M15 / Tratar de buscar, o sea, a favor»; 22:18 «porque ya luego cambia el sesgo a bajista
  / entonces ya no buscaríamos»; 22:41–22:55 «…flujo de órdenes m1 brutal la cual el precio pues
  respeta a pesar de que buscamos entradas alcistas … por más que queramos no vamos a entrar, o sea,
  si no se cumplen las condiciones que serían Raker y demás».
- **Resumen:** manda el sesgo. En M15 solo se busca a favor, y si el flujo va en contra no se entra
  porque no se cumplen las condiciones.
- **Confirmación:** no hubo frase de confirmación explícita.
- **Contradicciones:** ninguna; coincide con `ev-v4-001027-1b74d1a6` y `ev-v3-001242-cbe6bdc3`.
- **Propuesta:** **resuelve**. A-26 pasa a RESUELTA sin cambio de regla: el filtro direccional ya lo
  aplica el bot con `sesgo`.
- **Ítems:** `ev-v9-001915-d03d1565`.

### A-39 · qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo

- **Citas:** 26:35–26:44 «usualmente nosotros lo que hacemos es cerrar / … / va, o sea, se cierra /
  se cierra completamente»; 27:00 (consultor) «si estamos de 7 a 11 y se cierra o sea, ya son las
  11, entonces se cierra esa operación sin importar donde esté» / 27:06 «claro, por ejemplo»; 27:35;
  28:08; 30:28 (§3.1).
- **Resumen:** una operación abierta se cierra un minuto antes de que venza la vela H4 de su sesión,
  esté donde esté y sea cual sea el sesgo siguiente. De una **orden puesta** sin llenar no dice nada
  aquí; lo más cercano es A-38 («sigue vivo hasta que se desarrolle otro posible punto de breaker»).
- **Confirmación:** sí: a «¿se cierra indiferentemente si el sesgo es el mismo?» (30:21), «Claro.
  Indiferentemente se cierra, sí, si el sesgo es el mismo» (30:26–30:28).
- **Contradicciones:** con RN-002 y la spec, que solo cierran al fin de la ventana. Con
  `ev-v2-002441-504cbbe9`, donde era una «opción agresiva». Con `ev-v4-011514-fe34ac7e` (se cierra «en
  punto», no un minuto antes). Coincide con `ev-v3-010304-4468cc20`.
- **Propuesta:** **resuelve en parte — respuesta incompleta por audio** (corte 28:49–29:53, §2).
  - Una regla nueva: cierre al vencer cada sesión H4, un minuto antes.
  - La hora de RN-002 pasa de 15:00 a 14:59.
  - La orden pendiente queda abierta.
- **Ítems:** `ev-v9-002735-472432b8`, `ev-v9-002807-16d5946b`, `ev-v9-003026-0445965d`.

### A-46 · si una toma de liquidez de una sesión anterior del mismo día sigue valiendo en la siguiente

- **Citas:** 30:55 (pregunta leída); 32:42–32:58; 33:08; 33:18–33:38; 34:37–34:42 (consultor) «cambia
  algo si el sesgo h4 / en la segunda sesión es distinto al de la primera / me dijiste que son dos
  mundos distintos verdad» / «exacto»; 34:58 «No, porque son sesiones diferentes.»
- **Resumen:** cada sesión es un mundo aparte. No importa cómo terminó la primera operación, cada toma
  nueva de M15 abre un escenario, y no hay un máximo de escenarios por día.
- **Confirmación:** sí, a la paráfrasis del consultor: «Claro, exacto» (32:58) y «exacto» (34:42).
  A la pregunta literal («¿empiezas un escenario nuevo desde cero?», 30:55 y 31:05) no contesta con
  un sí directo: dice que tendría que verlo en el gráfico (32:20). La parte de 32:20–32:38 es un
  tramo no citable.
- **Contradicciones:**
  - Con el motor: `liquidez_tomada` no caduca al abrir la sesión, según la nota de A-46.
  - Con `ev-v4-003350-acb03ee7` («como máximo dos entradas por día»).
  - Con `ev-v1-000959-b82650ad`, `ev-v4-004936-d7004417` y `ev-v4-011351-74b8bb39` (el día termina
    con la primera ganadora). Esos tres ya estaban contradichos por `ev-v6-000732-*` y por RN-017.
  - Coincide con `ev-v4-005251-5cd62aaa` y RN-017.
- **Propuesta:** **resuelve**.
  - `liquidez_tomada` caduca al abrir cada sesión, como `sesgo`.
  - Cada toma nueva abre un escenario, sin tope diario de escenarios.
  - Lo que falta, porque no se le preguntó así: si una toma de la sesión 1 que todavía no dio
    entrada vale en la sesión 2. «Mundo diferente» dice que no, pero no es una respuesta literal.
- **Ítems:** `ev-v9-003253-2ac6060a`, `ev-v9-003303-818a0796`, `ev-v9-003318-c0503fe5`,
  `ev-v9-003456-9ef48fb5`.

### A-35 · cuándo un pivote de M15 está formado

- **Citas:**
  - 36:21–36:36 «…desde que se forma en este caso se formaría en estas dos velas en este par de
    velas porque básicamente el / El primero marca el máximo y el segundo te confirma que está
    retrocedido»;
  - 37:30–37:34 «priorizamos en este par de velas / pues donde está la mecha / el punto más alto»;
  - 38:06–38:14 «para yo poder validarlo eso como liquidez / Tendría que haber una vela contraria»;
  - 38:26–38:34 «…una zona de liquidez en M15 tiene que cerrar, o sea, por completo. / No tiene que
    estar en transcurso, o sea, tiene que cerrar para poder definir si trazamos o no».
- **Resumen:** el alto vale cuando lo forma un par de velas: la primera marca el máximo, y la segunda,
  contraria y cerrada, confirma el retroceso. El nivel es el punto más alto del par, mecha incluida.
- **Confirmación:** sí, a «el alto sigue valiendo…» (38:18–38:23): «tiene que cerrar, o sea, por
  completo» (38:26). A «¿y si después el precio lo supera un poco?» no hay respuesta directa: contesta
  sobre la vela contraria.
- **Contradicciones:** ninguna. Coincide con `ev-v4-005053-885e2773` y `ev-v6-003701-7613b381`.
- **Propuesta:** **resuelve en parte**.
  - `liquidez_m15_pivote_formado` = `cierre_vela_contraria`.
  - Queda abierto qué se hace si el precio supera un poco el alto.
  - Desbloquea RN-004 (A-35 es bloqueante).
- **Ítems:** `ev-v9-003621-f65f51a0`, `ev-v9-003826-740c4d95`.

### A-45 · en qué granularidad se evalúa «cierra con cuerpo» en la toma de liquidez de RN-004

- **Citas:**
  - 39:12–39:21 «…para validar la toma de liquidez en M15 / Tendría que ser con cuerpo»;
  - 39:38 (consultor) «En M15 o en M1.» / 39:40 «La vela de M1, en ese caso.»;
  - 40:38–40:46 «esta es la vela de M1 que rompe, o sea, la zona del índice de M15 / y lo hace con
    cuerpo, o sea, cierra por encima con cuerpo. / Si lo cerrara por debajo con mecha, no sería
    válido»;
  - 42:28–42:35;
  - A-25, 97:59–98:20 «tendríamos que irnos en M1. Eso no se / evalúa en M15 … lo importante / es
    como / toma la liquidez de M15 / pero en un minuto».
- **Resumen:** la toma de la liquidez de M15 la hace **una vela de M1** que cierra con cuerpo pasado
  el nivel. La mecha vale para actualizar el punto de breaker en M1, y no vale para la toma.
- **Confirmación:** sí, repitiendo la frase del consultor: «claro, para el M1 para actualizar / el
  punto de breaker vale la mecha / y para la liquidez de M15 / hace siempre falta cuerpo»
  (42:28–42:35).
- **Contradicciones:** afina `ev-v4-003849-3fe5161b`, `ev-v4-001533-73539d90` y
  `ev-v4-003942-cfffa382`, que decían «en M15 tiene que cerrar con cuerpo» sin la granularidad.
  RN-004 no la dice.
- **Propuesta:** **resuelve**. `liquidez_m15_criterio_toma` sigue siendo `cuerpo`, evaluado en la vela
  de M1. Toca el texto y la forma de RN-004, y la nota de A-43.
- **Ítems:** `ev-v9-004037-ca58e486`, `ev-v9-004217-c014bfdc`.

### A-43 · si una liquidez de M15 tomada antes de las 7 cuenta para operar después

- **Citas:** 43:45 «aquí creo que se ha confundido porque para hacerlo más rápido el backtesting lo
  estábamos trazando ya con anticipación…»; 44:37–44:46; 45:33 (consultor) «si la liquidez se formó
  antes de las 7, pero el precio la toma ya dentro.» / 45:40 «Es valio la entrada, sí.» / 45:44 «…se
  puede apoyar de liquidez, o sea, antes de las 7, pero, o sea, y toma, pero tiene que tomar para que
  se tome la entrada dentro de las 7».
- **Resumen:** una liquidez formada antes de las 7 vale. La toma tiene que ser dentro del horario.
- **Confirmación:** sí: «Es valio la entrada, sí» (45:40).
- **Contradicciones:** con el motor. Según la nota de A-43, hoy cuenta como toma dentro de la sesión
  la vela de M15 que cierra a las 07:00, y en construcción la toma del bot es esa en 7 de los 40 días
  con toma. Con A-45 (toma en M1) y esta respuesta, esa toma es anterior a las 7 y no contaría. Es una
  lectura: el caso exacto no se le preguntó.
- **Propuesta:** **resuelve en parte**. Una liquidez formada antes de las 7 vale; queda por confirmar
  que una toma anterior a las 7 no cuenta. Toca la forma de RN-004 y el hecho `liquidez_tomada`.
- **Ítems:** `ev-v9-004533-d075b080`.

### A-50 · para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera

- **Citas:** 47:21–47:30; 47:46–47:49 «no hay un punto de breaker y aparte de que nunca puede ser por
  debajo de una vela»; 49:20–49:25; 51:23–51:30 (§3.5).
- **Resumen:** la caja va del punto de breaker al punto más alto, y todo tiene que desarrollarse más
  allá del nivel tomado. A la pregunta del 0 o el 1 no contesta.
- **Confirmación:** la hubo (51:08–51:12). Respuesta: «¿El 0 o el 0? No, no importa / Es que como digo
  / Espero que con / Los ejemplos que he dado / Pueda corregir».
- **Contradicciones:** ninguna. Coincide con `ev-v1-001306-f98e12e9` y `ev-v3-001600-ed45b091`.
- **Propuesta:** **no resuelve**. A-50 sigue ABIERTA, con nota que cite el tramo. Para volver a
  preguntarla hacen falta los dos dibujos, uno con el 0 dentro y otro con el 0 fuera.
- **Ítems:** `ev-v9-004721-2e023ac6`, `ev-v9-004919-c6bfb3ee`.

### A-13 · break even al toque o con cuerpo

- **Citas:** 52:21–52:36 «se pasa a break even cuando / en esa vela verde se complete la zona de
  control / o sea, a la siguiente la vela roja / termina cerrando por debajo / … / el break even como
  tal»; 52:39 «inclusive a veces basta con que llegue o sea no necesariamente rompa por un pib»;
  54:06; 55:12–55:15 «apenas rompa este punto por debajo, / ya se protege en B la entrada»; 55:48;
  56:12; 56:21; 56:31–56:39.
- **Resumen:** completada la zona de control, apenas el precio toca, la entrada pasa a break even. Se
  mira en M1, y el break even va exactamente a la entrada, sin puntos para cubrir costes.
- **Confirmación:** sí: «¿estas cuatro las respondiste ya?» (56:05) → «…con que el precio la toque,
  con que el precio la toque» (56:12). Es una línea mezclada: el consultor lee las opciones y la
  respuesta es «con que la toque».
- **Contradicciones:**
  - Con `ev-v6-005359-e00e4b0f` («con cuerpo»); coincide con `ev-v6-005701-7ae2b8d3`.
  - RN-014 dice «al romperse».
  - `break_even_condicion` = `tocar` ya es CONFIRMED; `break_even_criterio_ruptura` está en
    DEFAULT_AMBIGUOUS con `mecha`.
- **Propuesta:** **resuelve en parte — respuesta incompleta por audio** (corte 57:00–58:06, §2).
  - `break_even_criterio_ruptura`: el toque, que es lo más cercano a `mecha`.
  - Nivel del break even: la entrada exacta.
  - Temporalidad: M1.
  - El texto de RN-014 pasa de «al romperse» a «al tocar».
- **Ítems:** `ev-v9-005219-3b98f54f`, `ev-v9-005543-1b52290e`, `ev-v9-005619-27ae7cd3`,
  `ev-v9-005631-c3b42381`.

### A-40 · qué se hace con el stop después del break even

- **Citas:** 58:43 (pregunta leída); 58:50 «Vale, o sea, como que tomar parciales, ¿verdad?» / 58:53
  (consultor) «Sí.» / 58:55 «No.» / 58:56 «no hemos no no definimos parciales o sea lo dejamos ahí
  quieto».
- **Resumen:** después del break even el stop se deja quieto.
- **Confirmación:** no hubo repregunta. Ojo: el trader entendió la pregunta como «tomar parciales», y
  el consultor lo aceptó.
- **Contradicciones:** con `ev-v3-003220-8805194d` y `ev-v3-003318-f1a2d27d` («protege poco a poco
  siguiendo el flujo»).
- **Propuesta:** **resuelve**. A-40 pasa a RESUELTA con «stop quieto», y se anota que la pregunta se
  entendió como de parciales.
- **Ítems:** `ev-v9-005850-8aae8764`.

### G-1 · cerrar antes del stop

- **Citas:** 59:06 «g1 cerrar una operación antes de que toque el stop…»; 59:23; 59:32–59:39; 59:39–59:49
  (consultor) «las únicas ocasiones donde se cierran es cuando termina la vela de 11 y de 15, ¿no?» /
  «Ah, claro, bueno, en ese caso sí, sí, sí. En ese caso sí».
- **Resumen:** no cierra a mano. Solo se cierra al vencer la sesión.
- **Confirmación:** sí: «en ese caso sí, sí, sí» (59:45).
- **Contradicciones:** ninguna. `ev-v2-002233-29e441c8` («cerrar antes de un BOS contrario es una
  opción, no una regla») queda descartado como regla.
- **Propuesta:** **resuelve**. No toca ninguna regla. Confirma RN-015, y el cierre de sesión es el de
  A-39.
- **Ítems:** `ev-v9-005916-d6a15b43`.

### G-2 · dejar correr más allá del objetivo

- **Citas:** 60:40–60:49 (pregunta leída); 60:53–61:00; 61:00 (consultor) «Ok, el objetivo es fijo y
  se deja / O se gana o se pierde / Y bueno, en este caso break even» / 61:06 «Exacto».
- **Resumen:** no deja correr: el objetivo es fijo.
- **Confirmación:** sí: «Exacto» (61:06).
- **Contradicciones:** con `ev-v5-000456-dfb95b24` y `ev-v5-000515-02b5bc7a` (ampliar a 1:4, abierto)
  y con `ev-v3-003318-f1a2d27d`. Coincide con `fb-2026-09-09-sesion-01-3add10a2` y con RN-015.
- **Propuesta:** **resuelve**. No toca ninguna regla: confirma RN-015.
- **Ítems:** `ev-v9-010053-e521e833`.

### A-18 · base sobre la que se mide el objetivo 1:3

- **Citas:** 25:28–25:39; 61:20–61:27 (pregunta leída); 62:32–62:49; 63:09–63:14; 64:16–64:21; 64:30–64:39
  (consultor) «Lo habíamos definido para abajo, ¿verdad? O sea, si es de alcista para abajo y si es
  bajista, pues, para arriba.» / «Claro, tener un margen extra.»; 65:27 «siempre dale un / pequeño
  margen, creo yo»; 65:43–65:47; 65:52 (consultor) «¿El objetivo es fijo o a veces lo mueves?» /
  65:56 «El objetivo 1.3 es pico [fijo]».
- **Resumen:**
  - El objetivo es 3 veces la distancia del 0 al 1.
  - El lote se calcula sobre el 0 al 0,8, con el 0,5 % de riesgo en el 0,8.
  - El 0,8 se redondea hacia fuera, lo mínimo posible.
  - A «¿en qué momento pasas el stop al 0,8, al poner la orden o cuando se ha llenado?» (61:27) **no
    contesta**.
- **Confirmación:** sí, a tres preguntas: «Sí» al 0,8 del riesgo (64:21), «Claro, tener un margen
  extra» al redondeo (64:39) y «El objetivo 1.3 es fijo» (65:56).
- **Contradicciones:** con el bot en el redondeo (§3.3, `primitivas_broker.py:306`, `ROUND_DOWN`).
  Coincide con ADR-0020, RN-011, RN-015, `base_calculo_objetivo: caja_completa`,
  `ev-v2-003256-0197f4e1` y `ev-v6-013508-b4c88d87`.
- **Propuesta:** **resuelve en parte**.
  - A-18 queda resuelta en la base: 0 a 1 para el objetivo y 0 a 0,8 para el lote. Coincide con el
    bot y con la V2 de VIABILIDAD-COMISION.
  - El redondeo del 0,8 hacia fuera es una regla nueva, o un cambio en `escribir_stop_en_la_orden`.
    Hay que medir antes cuántas operaciones cambia.
  - Sigue abierto el momento del paso al 0,8.
  - Lo que se habla de «un posible método de gestión de riesgo experimental» (64:57–65:04) es,
    según el propio consultor, una iteración futura: no se registra.
- **Ítems:** `ev-v9-002526-6a6579e6`, `ev-v9-010232-4b049a1e`, `ev-v9-010311-a13b0a41`,
  `ev-v9-010416-eb674c2f`, `ev-v9-010541-0c80d5cf`.

### G-3 · tamaño mínimo de caja

- **Citas:** 66:05–66:14 (pregunta leída: la mayoría de sus entradas miden 1 o 2 pips, algunas
  menos de 1); 66:20–66:22; 66:31.
- **Resumen:** no hay tamaño mínimo ni máximo de caja.
- **Confirmación:** sí, a la repregunta (66:26): «No, o sea, me es indiferente» (66:31).
- **Contradicciones:** ninguna en la evidencia. Tensión con el tope de 100 lotes del bot: en
  VIABILIDAD-COMISION ese tope deja fuera las operaciones de stop cortísimo.
- **Propuesta:** **resuelve**. No va ningún filtro de tamaño. El tope de lotes sigue siendo una
  restricción del broker, no del método.
- **Ítems:** `ev-v9-010620-ac899dd8`.

### A-42 · con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00

- **Citas:** 66:36 «¿Con qué reloj cuentas tu horario?». La respuesta cae casi entera en tres bloques
  de cuarentena (66:38–67:51). Fuera de ellos:
  - 67:40 «En invierno empieza»;
  - 67:41 (consultor) «Entonces cambia el horario para ti en invierno» / 67:45 «Sí»;
  - 67:54–68:00 (consultor) «Entonces en invierno / no empiezas a las 7 / o a las 6 sería / tu
    reloj, ¿no?» / 68:01 «Sí.»;
  - 68:03 (consultor) «¿Cambias la zona horaria del gráfico o la dejas como está?» / 68:09–68:13
    «Bueno, lo adapto. O sea, automáticamente se adapta. La plataforma la adapta.»;
  - 68:16–68:20 (consultor) «…pero las premisas para ti son las 6 en tu reloj», sin respuesta del
    trader.
- **Resumen:** en invierno empieza a las 6 de su reloj, no a las 7, y la plataforma adapta el
  gráfico sola.
- **Confirmación:** «Sí» a «a las 6 sería tu reloj» (68:01). La última paráfrasis del consultor no
  tiene respuesta.
- **Contradicciones:** con `huso_operativa` = `Europe/Madrid` (CONFIRMED, ADR-0017: «el trader opera
  siempre a la misma hora SUYA»). Si en invierno empieza a las 6 de su reloj, la hora que no cambia es
  la del gráfico, que es UTC+2 fijo (`huso_grafico` = `Etc/GMT-2`): 07:00 del gráfico son las 06:00
  de Madrid en invierno. **Es una lectura**: el tramo decisivo está en cuarentena, y el consultor
  tiene que revisarlo.
- **Propuesta:** **resuelve en parte**.
  - Si el consultor confirma la lectura, toca `huso_operativa` (a `Etc/GMT-2`), ADR-0017, la ventana
    de ticks de invierno 06–14 UTC y la parada de marzo (A-42 es bloqueante).
  - El texto de los tres bloques de cuarentena de 66:38–67:51, con máscara, va justo debajo. **A-42
    no se activa hasta que el consultor lo revise.**
- **Ítems:** `ev-v9-010753-063c8cb7`, `ev-v9-010809-68e4ea44`.

#### El tramo 66:38–67:51, con máscara (revisión del consultor, 2026-09-29)

Por orden del consultor, el texto de los segmentos 1075–1090 de la cruda (los tres bloques de
cuarentena y los cuatro segmentos que ya estaban en la filtrada) se sacó con **toda fecha, mes y
precio sustituidos** por `[FECHA]` o `[PRECIO]`. **La máscara se aplicó antes de imprimir nada**: el
script lee la cruda y solo escribe el texto enmascarado, así que nadie leyó ese tramo sin ella.

Qué sustituye la máscara:
- los doce meses, con las grafías del ASR que ya usa la cuarentena;
- cualquier número a tres palabras o menos de un mes, de un día de la semana o de «día», «mes» o
  «fecha»;
- las fechas numéricas y los números de cuatro cifras;
- dos o más números seguidos (aunque vayan unidos por «punto», «coma», «y» o «con»), que se tratan
  como un precio dictado.

Antes de pasarla por el tramo se probó con frases sintéticas (fechas con día y mes, en cifras y en
letras; precios en cifras y dictados; un número de día sin mes), y todas salieron enmascaradas.

```
[66:38] De nuevo esta pregunta
[66:41] aquí está lo que todavía no sabemos claro y ya recordé en el bactés de [FECHA] en el bactés de
[66:53] [FECHA] lo había hecho hace par de días pero como te había comentado se perdió el progreso por el
[66:59] hecho de que se me había actualizado la cuenta o sea la suscripción y todo eso entonces se me había
[67:06] eliminado. Inclusive de los otros backtests que te envié, o sea, está esto, o sea, falta, o sea, tendría que recopilar, pero en [FECHA] por ejemplo, cambia, en lugar de 7 sería 6, y creo que eso sería invierno, ¿verdad?
[67:30] En lugar de 7 a 6
[67:33] Y así
[67:34] O sea, una hora como que menos
[67:35] Eso es en [FECHA] pero en otras fechas es así
[67:38] Supongo, también
[67:40] En invierno empieza
[67:41] Entonces cambia el horario para ti en invierno
[67:45] Sí
[67:45] Sí, claro, claro, también porque
[67:48] Por la dirección geográfica, para mí en [FECHA]
[67:50] Es verano, para ti es invierno
```

**Qué contiene, respuesta al consultor:**
- **Ninguna operación, ningún precio y ningún resultado.** No sale ningún `[PRECIO]`, ni se dice
  ninguna cifra de ganancia, pérdida o número de operaciones.
- Los cinco `[FECHA]` son **nombres de mes**, y los cinco son de los cuatro meses con días
  reservados. El script lo cuenta sin decir cuál. No hay ningún número de día.
- **No son solo nombres de mes al hablar del cambio de hora.** Aparecen en dos contextos:
  1. **66:41–67:06:** el trader cuenta que hizo el backtest de ese mes hace un par de días y que
     perdió el progreso cuando se le actualizó la suscripción. Es un hecho sobre el material (que
     ese backtest existe y se perdió), no un dato de él.
  2. **67:06–67:35:** en ese mes, dice, el horario «cambia, en lugar de 7 sería 6, y creo que eso
     sería invierno», «una hora como que menos». Es el cambio de hora, pero dicho de ese backtest:
     que en él la hora de empezar es 6 y no 7. Es una propiedad del reloj del material, no una
     etiqueta ni una cifra de resultado. Se declara en `HOLDOUT-EXPOSICIONES.md` y **la decisión es
     del consultor**.
- 67:48–67:50 («Por la dirección geográfica, para mí en [FECHA] / Es verano, para ti es invierno»)
  suena al consultor, que vive en el otro hemisferio: se atribuye por contexto.
- **Para A-42:** la voz confirma que en invierno el horario pasa de 7 a 6, «una hora como que
  menos», pero no dice en qué reloj (el suyo o el del gráfico). La lectura de arriba sigue siendo
  una lectura. Los tres bloques siguen en `tramos_no_citables.yaml`: el texto enmascarado no es
  citable como evidencia.

### A-44 · magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana)

- **Citas:**
  - 68:42–68:56 (contexto leído: «en la sesión 1 quedaron, bueno, 4,5 el día y 9% de la semana»);
  - 69:24 «¿existe el tope? sí»;
  - 69:31–69:47 «…nuestra racha más mala, por así decirlo, fue de nueve, creo, ¿no? / Manejándolo a
    nueve pérdidas consecutivas, que creo que fue en enero»;
  - 71:30–71:33 «9 pérdidas como máximo / O sea, para / El tope es eso, 9 pérdidas como máximo»;
  - 71:39–71:54 (consultor) «¿cuánto la cifra?» / «9 pérdidas seguidas» / (consultor) «O en un día»
    / «Seguidas» / «Si son 8 seguidas / O sea, nada, no se detiene / hasta el noveno no / el último
    cartucho es el noveno»;
  - 72:07–72:10 «creo yo / siempre con saldo final / yo lo vería así»;
  - 72:50 «Claro. Ah, ya, o sea, es indiferente / de los días»;
  - 74:26–74:33 «…ya se elimina esto de aquí el 4,5 y el 9 no ahora se cuenta por / por número de
    pérdidas nada más, dado que es geométrico lo del cálculo». Esta línea parece el consultor
    resumiendo, y no tiene respuesta.
- **Resumen:** el tope no es un porcentaje: son 9 pérdidas seguidas, sin importar el día ni la semana.
  Con 8 no se para, y la novena es la última. El riesgo de la siguiente se calcula sobre el saldo
  final.
- **Confirmación:** sí: «Seguidas» (71:46) a «¿o en un día?».
- **Contradicciones:**
  - Con `fb-2026-09-09-sesion-01-4963aa6f` y `fb-2026-09-09-sesion-01-5e23d47c` (4,5 % sobre el
    saldo inicial del día), con `fb-2026-09-09-sesion-01-a85b6bc7` (9 % semanal) y con
    `ev-v4-012524-0ef85a89`.
  - Con RN-020 («el tope porcentual del trader es el único freno del día»).
  - `perdida_trader_alcance` no tiene opción para una racha (`sin_tope · dia · semana · ambos`), ni
    `perdida_trader_unidad` para un número de pérdidas.
- **Propuesta:** **resuelve con lectura NUEVA** (para: `ACTIVAR-A35-A44.md` §4, no se fuerza en la
  opción más cercana).
  - Toca los parámetros `perdida_trader_*`, a los que les faltan opciones.
  - Toca RN-020, la regla bloqueada por A-44. Deja de ser un tope porcentual.
  - Y hay que corregir los tres registros de la sesión 01 con registros nuevos, porque son de solo
    añadir.
  - **Abre una ambigüedad nueva:** qué corta la racha (una ganadora; un break even) y qué pasa tras
    la novena (¿se para hasta cuándo?). No se le preguntó.
- **Ítems:** `ev-v9-011128-a267338b`, `ev-v9-011139-a26a5b11`, `ev-v9-011206-148fc7f9`.

### A-21 · qué es una zona de control limpia, sin ruido

- **Citas:**
  - 75:55–76:15 «es indiferente el número de velas / … / empezamos desde nuestro punto de / breaker /
    es el punto más alto / … / no existe un número / de velas»;
  - 76:53–76:59 «…pero tendría que ser del mismo color que la vela anterior si es de / de otro color,
    no es válido»;
  - 77:04 (consultor) «¿Y este envolvente vale como bloque?» / 77:08 «Envolvente, sí.»;
  - 77:14–77:18 (consultor) «¿el cero de la caja va siempre en el extremo del bloque, mecha incluida,
    o ese es un poco dentro?» / «Mecha incluida, siempre.»;
  - 77:32 «No, porque el ejemplo está mal.»;
  - 77:58 «Y este esquema siempre va a existir.»;
  - 79:57 «esto limpio me refiero a que no haya, o sea, por ejemplo, una vela verde, una vela
    bajista, una vela verde, una bajista…»;
  - 82:18–82:24.
- **Resumen:**
  - El bloque es cualquier número de velas del mismo color que la anterior, y una envolvente vale.
  - El 0 va en el extremo del bloque, mecha incluida.
  - Una zona «limpia» es una sin alternancia de colores.
  - «¿Cuánto puede medir como máximo el pequeño retroceso del esquema 2?» (77:42) no se contesta.
- **Confirmación:** sí: «Mecha incluida, siempre» (77:18). «¿Las dos velas de la izquierda son un solo
  bloque?» → «No, porque el ejemplo está mal» (77:32).
- **Contradicciones:** `zona_control_limpia` solo tiene `solo_una_zona_de_control` y
  `sin_mecha_mas_alla_del_extremo`, y la respuesta no es ninguna de las dos. Coincide con R4 de
  `BLOQUE-DE-LA-CAJA.md` (el bloque = tramo de velas del mismo color) y con `ev-v7-002403-8344331d`.
- **Propuesta:** **resuelve en parte, con lectura NUEVA** para «limpia» (para, `ACTIVAR-A35-A44.md` §4).
  Toca:
  - `zona_control_limpia`, que necesita una opción nueva;
  - la regla del bloque de la caja (la ruptura ya tiene ADR-0055 y la preparación de A-21);
  - el máximo del retroceso, que sigue abierto.
- **Ítems:** `ev-v9-011555-81ec8beb`, `ev-v9-011655-c20a1c2d`, `ev-v9-011704-b5ddc3e3`,
  `ev-v9-011714-08536830`, `ev-v9-011957-4250c2b4`.

### E-1 · tus dos backtests de los mismos días

- **Citas:**
  - 82:47–83:01 (consultor) «E1, tus dos backtests / De los mismos días / Comparando tu backtest
    original / Del 3 al 11 de agosto / Con lo que hiciste en el video…»;
  - 83:06–83:14 «…para hacerlo / un poco más rápido, me he salteado / algunas operaciones de
    break-even»;
  - 83:40–83:44 (consultor) «cuando haces el mismo día dos veces y te sale distinto ¿cuál de las dos
    versiones es la buena por el bot?» / 83:47–83:50 «bueno, yo creo que / en este caso hay que usar
    / lo último / el último que fue el backtest completo»;
  - 84:01–84:07 «no, con las mismas reglas / no cambié ninguna»;
  - 84:09 (consultor) «las que no tomaste fue porque sabías que iban a ser en break-even, ¿no?» /
    84:12 «Sí, claro.»
- **Resumen:** las dos versiones se hicieron con las mismas reglas, y la diferencia son operaciones
  de break even que se saltó por ir rápido. Para el bot vale «el último, el backtest completo».
- **Confirmación:** sí: «Sí, claro» (84:12) a que las no tomadas eran de break even.
- **Contradicciones:** ninguna con la evidencia. Es agosto: material de desarrollo.
- **Propuesta:** **no resuelve** en lo que importa. «El último» y «el completo» pueden ser dos cosas
  distintas: el vídeo es el último en fecha y el que se saltó operaciones; el original es el completo.
  Queda para el consultor; no toca nada todavía.
- **Ítems:** `ev-v9-012347-eef7627f`, `ev-v9-012401-3fefa768`.

### A-30 · la orden límite pendiente al llegar el fin de la ventana

- **Citas:** 84:30–84:39 (pregunta leída, con el caso del vídeo en que descarta una entrada a 10
  minutos del final); 84:43; 85:08–85:21; 85:23–85:32 «el caso más extremo / si abre una operación a
  las / no sé, 2 y 58 / pm, normal que la abra y que la / cierre a las 3»; 85:45–85:48 (consultor) «59
  con un segundo / ya no debe haber operación» / «exacto».
- **Resumen:**
  - No hay hora límite para abrir: si hay operación, se toma y se cierra un minuto antes de la
    siguiente sesión.
  - El descarte del vídeo a 10 minutos fue para no distorsionar la muestra.
  - Qué hace con una orden sin llenar a la hora de cierre no lo dice expresamente.
- **Confirmación:** sí: «exacto» (85:48).
- **Contradicciones:** con `ev-v4-011514-fe34ac7e`: se cierra «en punto», no a las 14:59.
- **Propuesta:** **resuelve en parte**. Toca RN-002 (14:59 en vez de 15:00) y el cierre de sesión de
  A-39. La orden pendiente sigue abierta: se puede cruzar con A-38.
- **Ítems:** `ev-v9-012514-b5b6c84f`.

### A-31 · el stop entero de una entrada que se activó sin ruptura

- **Citas:** 86:07–86:17 (pregunta leída y respuesta en la misma línea) «…pues no importa o sea si
  llega a tocar el stop se considera como un loss y un trade parida y ya está o sea gasta un intento
  o no»; 86:28 «bueno si gasta un intento ok gastaría un intento porque se están contando si es loss
  si o sea gastaría un intento».
- **Resumen:** cuenta como pérdida y gasta un intento.
- **Confirmación:** sí: «gastaría un intento» (86:28). Es una línea mezclada: el consultor pregunta y
  el trader repite.
- **Contradicciones:** coincide con RN-010 («se gestiona como cualquier otra») y con
  `ev-v5-000246-17eff9e1`. Con RN-019 («se puede reentrar tras un equal sin gastar cartucho») hay
  tensión, y la aclara E-2.
- **Propuesta:** **resuelve**. A-31 pasa a RESUELTA. No toca ninguna regla (RN-010 y RN-016), salvo
  lo que diga E-2 sobre RN-019.
- **Ítems:** `ev-v9-012612-d9db2ee8`.

### E-2 · cómo operas los equals

- **Citas:** 86:38; 87:00–87:05 «me ha entrado una duda / … / mi palabra dice no…» (ASR confuso);
  88:09–88:12 «yo, este equal es válido / o sea, como si fuera un breaker»; 88:24–88:52 (el ejemplo);
  89:00–89:06 «…entonces cuando hay operativa en igual no se considera un tiro o sea no es
  indiferente no» (ASR confuso); 89:21 «cambia algo si es un igual hay un color respecto a tu
  sesgo» (sin respuesta clara).
- **Resumen:** un equal en M1 vale como punto de breaker. Si una operación que nace de un equal gasta
  un intento, el ASR no deja leerlo.
- **Confirmación:** no hubo frase de confirmación entendible.
- **Contradicciones:** posible choque con A-31. Coincide con `ev-v5-000527-c56ebe45` y con RN-019.
- **Propuesta:** **resuelve en parte**. El equal como punto de breaker es una nota para la regla del
  punto de breaker. Si el equal gasta un intento sigue abierto, y conviene escuchar 89:00–89:06
  (tramo citable).
- **Ítems:** `ev-v9-012809-4c13a3f4`.

### E-3 · cuando la vela cambia de color

- **Citas:** 89:28 «vamos 5 a 5 más y 3 cuando la vela cambia de color aquí está el contexto» (ASR);
  89:51 (consultor) «Cuando una vela está casi plana y no queda claro si es rojo o verde, ¿cómo la
  tratas?»; 89:56 «…en EURUSD muy rara vez me lo he topado»; 90:21–90:33 «o sea, no / cuenta como si
  no existiera / no se puede trazar, o sea / allí no se puede trazar / un punto de breaker /
  imposible».
- **Resumen:** una vela casi plana cuenta como si no existiera, y sobre ella no se traza punto de
  breaker.
- **Confirmación:** no hubo repregunta.
- **Contradicciones:** ninguna.
- **Propuesta:** **resuelve**. Es una nota para el mapeo de M1 (RN-007, y la regla del punto de
  breaker). Hay que definir antes en qué consiste «casi plana»: un umbral que el trader no dio.
- **Ítems:** `ev-v9-013021-ea0db73a`.

### A-41 · si hay un tope de entradas por día, aparte de los cartuchos

- **Citas:** 90:37–90:51 «ah, 41 / ¿cuántas entradas haces como máximo? / … / ¿cuántos serán? ¿tres o
  cuatro? / Eh, no sé, dime tú.»; 90:54 (consultor) «…un coge tres intentos por liquidez.» / 91:00
  «Sí, serían tres intentos por liquidez.» / 91:09 «¿El máximo es por día? No, no, por liquidez.» /
  91:12 «Sí.»; 91:19–91:21 (consultor) «¿Cuentan los break-even y las entradas invalidadas?» / «no
  cuentan».
- **Resumen:** tres intentos por liquidez, no por día. Los break even y las entradas invalidadas no
  cuentan.
- **Confirmación:** sí: «Sí, serían tres intentos por liquidez» (91:00). Ojo: la cifra la propuso el
  consultor tras un «no sé, dime tú» (90:51).
- **Contradicciones:** con `ev-v4-003350-acb03ee7` («dos entradas por día»), `ev-v3-004817-f2dfb955` y
  `ev-v3-000138-fc8f7905` (dos cartuchos), y con el título de RN-016 («el día se limita por
  cartuchos»). Coincide con `fb-2026-09-09-sesion-01-846fb0d7`, `fb-2026-09-09-sesion-01-2c92afe0`,
  `cartuchos_max` = 3 y `cartuchos_reinicio` = `siguiente_liquidez_m15`.
- **Propuesta:** **resuelve**. A-41 pasa a RESUELTA: no hay tope por día. El texto de RN-016 queda
  «por liquidez». Con A-46 no hay tope de escenarios.
- **Ítems:** `ev-v9-013054-d49a544e`, `ev-v9-013117-c683f9b5`.

### A-38 · cuándo se da por anulada una orden límite que el precio deja sin llenar

- **Citas:**
  - 91:21 «a 38 cuando cuando das por anulada una orden que no se llena»;
  - 92:07 «O sea, sigue vivo hasta que se desarrolle otra próxima, otro posible punto de breaker.»;
  - 92:42–92:52 «…siempre es objetivo, creo yo. Lo hemos definido siempre por objetivo. / Siempre
    por objetivo.»;
  - 93:15 «pues si el breaker es con mecha, no hay valía a la orden…»;
  - 93:33–93:39 «si se llegara a formar otra zona después, entonces sería cuestión / ya de actualizar
    / el punto de breaker»;
  - 93:57 «no pasa nada si se / vaya el precio»;
  - 94:37–94:48 «…es necesario que ocurra / el desarrollo de los esquemas / y si aparece / un punto de
    breaker nuevo / pues eso simplemente sería / alterizar [actualizar] la orden / límite».
- **Resumen:** la orden no se anula porque el precio se aleje. Sigue viva hasta que se desarrolla otro
  posible punto de breaker, y entonces se actualiza a él.
- **Confirmación:** a «¿pesa lo lejos que se vaya el precio o solo que se rompa el esquema o aparezca
  un punto nuevo?» (93:44–93:51) → «no pasa nada si se vaya el precio» (93:57) y lo de 94:37–94:48.
- **Contradicciones:** ninguna. Coincide con `ev-v4-010731-bb8af97c`, `ev-v4-010857-5bc906c9` y RN-006.
- **Propuesta:** **resuelve**. A-38 pasa a RESUELTA: sin caducidad por distancia ni por tiempo dentro
  de la sesión. Toca la tercera rama de ADR-0056, la vida de la orden stop.
- **Ítems:** `ev-v9-013205-85840dcc`, `ev-v9-013437-ffdd9c87`.

### A-24 · qué hace que marques un pivote de M15 y no otro

- **Citas:** 94:51–95:18 «A24 / ¿Cuál de varios saltos eliges? / Bueno, no me voy a decir / cuál
  eliges… / … está muy bien marcado lo que sería la liquidez…».
- **Resumen:** describe el ejemplo como bien marcado; no da un criterio nuevo.
- **Confirmación:** no la hubo.
- **Contradicciones:** ninguna.
- **Propuesta:** **no resuelve**. Sigue DECIDIDA por ADR-0045, sin cambios.
- **Ítems:** ninguno.

### A-25 · la vida de la marca de liquidez de M15

- **Citas:** 95:27–95:39 (pregunta leída); 96:29–96:38 «tenemos liquidez en M15 / y otra liquidez en
  M15, vale, esta sería la más reciente»; 97:20–97:47 (consultor) «entonces caso 1 / el alto nuevo
  queda más abajo…» / «…simplemente el más reciente claro / alto nuevo más bajo va a ser el que nos
  vamos a enfocar / en operar y si no / no se da entrada, pues seguimos / al más alto. / Y así
  consecutivamente.»; 97:49–98:20 (caso 2).
- **Resumen:**
  - Caso 1: con un alto nuevo más bajo, se opera primero sobre el más reciente, y si no da entrada,
    sobre el más alto.
  - Caso 2: si el precio pasa la marca solo con mecha en M15, la toma se evalúa en M1.
- **Confirmación:** sí, caso por caso: «el caso 1 está trazado tal cual / está bien» (97:31) y
  «correcto» (98:22), a la frase del consultor sobre M1.
- **Contradicciones:** ninguna. Coincide con `ev-v1-001334-96e8ca40`, `ev-v4-010921-31dd762d` y
  ADR-0045 (la más reciente).
- **Propuesta:** **resuelve en parte**. El caso 1 va a la regla de la marca: se opera primero sobre el
  alto más reciente y se sigue con el anterior. El caso 2 es A-45. Queda por ver cómo encaja con
  `cartuchos_reinicio` (los intentos, ¿por marca o por toma?).
- **Ítems:** `ev-v9-013736-463282d5`, `ev-v9-013757-e4c639db`.

### A-37 · en qué temporalidad se busca la vela contraria de la que sale el stop

- **Citas:** 98:26–98:49 (pregunta leída); 98:52–99:08 «…hay a veces velas envolventes / que solo nos
  bastarían / … / que envuelvan a la vela anterior / para nosotros poder trazar la caja»; 99:14
  (consultor) «Para precisar, M1, M15 u otra» / 99:18 «M1»; 99:19 (consultor) «¿Es la misma vela en
  la que pones la orden límite?» / 99:23–99:30 «Sí, o sea / La caja se trata desde el punto de
  breaker / Hasta el punto más alto / Se va actualizando eso / Hasta que ocurra el breaker».
- **Resumen:** M1. La caja va del punto de breaker al punto más alto y se actualiza hasta el breaker.
- **Confirmación:** sí: «M1» (99:18) y «Sí» (99:23).
- **Contradicciones:** ninguna. Coincide con `ev-v1-001454-69cebe62` y `ev-v7-002403-8344331d`.
- **Propuesta:** **resuelve**. A-37 pasa a RESUELTA. No cambia ninguna regla: confirma la temporalidad
  del mapeo de RN-011.
- **Ítems:** `ev-v9-013914-9fb86553`, `ev-v9-013923-0912f06b`.

## 5. Tabla de propuestas

| Código | Propuesta | Qué tocaría (en otra rama, tras la revisión) |
|---|---|---|
| A-47 | resuelve | `entrada_tipo_orden` = `stop_en_ruptura`; A-47 RESUELTA; texto de RN-006 y RN-011 («límite» → «stop»); el selector de ADR-0058 ya está en `main` |
| S-1 | resuelve en parte | confirma RN-003; con A-34, RN-033 y ADR-0044 («siempre hay sesgo») |
| A-34 | resuelve | RN-003 (doble ruptura: decide el color), RN-033 (`ambiguo` desaparece), ADR que enmiende ADR-0044 §1 |
| A-26 | resuelve | A-26 RESUELTA; ninguna regla |
| A-39 | resuelve en parte — **respuesta incompleta por audio** | regla nueva de cierre al vencer cada sesión H4 (un minuto antes); RN-002 a 14:59; la orden pendiente sigue abierta |
| A-46 | resuelve | `liquidez_tomada` caduca al abrir sesión; escenario nuevo por toma, sin tope diario |
| A-35 | resuelve en parte | `liquidez_m15_pivote_formado` = `cierre_vela_contraria`; desbloquea RN-004; «supera un poco» abierto |
| A-45 | resuelve | la toma de M15 se evalúa en la vela de M1 (cuerpo); texto y forma de RN-004 |
| A-43 | resuelve en parte | forma de RN-004 y `liquidez_tomada`: la toma, dentro del horario; confirmar la de antes de las 7 |
| A-50 | no resuelve | sigue ABIERTA; repreguntar con dos dibujos |
| A-13 | resuelve en parte — **respuesta incompleta por audio** | `break_even_criterio_ruptura` (toque); nivel = entrada exacta; M1; texto de RN-014 |
| A-40 | resuelve | A-40 RESUELTA (stop quieto) |
| G-1 | resuelve | ninguna regla (confirma RN-015; cierre de sesión en A-39) |
| G-2 | resuelve | ninguna regla (confirma RN-015) |
| A-18 | resuelve en parte | base confirmada (coincide con el bot); redondeo del 0,8 hacia fuera en `escribir_stop_en_la_orden`; momento del paso al 0,8, abierto |
| G-3 | resuelve | ningún filtro de tamaño |
| A-42 | resuelve en parte | si el consultor confirma: `huso_operativa` a `Etc/GMT-2`, ADR-0017, ventana de ticks de invierno, parada de marzo |
| A-44 | resuelve con lectura NUEVA + **abre ambigüedad nueva** | `perdida_trader_*` (faltan opciones), RN-020, corregir tres `fb` de la sesión 01; nueva: qué corta la racha de 9 |
| A-21 | resuelve en parte con lectura NUEVA | `zona_control_limpia` (opción nueva), regla del bloque de la caja; máximo del retroceso, abierto |
| E-1 | no resuelve | pregunta al consultor: ¿«el último» o «el completo»? |
| A-30 | resuelve en parte | RN-002 a 14:59; orden pendiente con A-38 |
| A-31 | resuelve | A-31 RESUELTA; ver E-2 frente a RN-019 |
| E-2 | resuelve en parte | nota del punto de breaker; ¿gasta intento?, abierto (escuchar 89:00–89:06) |
| E-3 | resuelve | nota del mapeo de M1; falta el umbral de «casi plana» |
| A-41 | resuelve | A-41 RESUELTA; RN-016 «por liquidez» |
| A-38 | resuelve | A-38 RESUELTA; vida de la orden stop (rama 3 de ADR-0056) |
| A-24 | no resuelve | nada (DECIDIDA, ADR-0045) |
| A-25 | resuelve en parte | regla de la marca de liquidez; encaje con `cartuchos_reinicio` |
| A-37 | resuelve | A-37 RESUELTA |

Cerrar cualquiera toca cuatro sitios más el test de `tests/unit/test_kit.py` y
`botsito spec docs --escribir` (CLAUDE.md). Nada de eso se hace aquí.

## 6. Lo que no se hizo, y por qué

- **Ningún fotograma de v9 abierto.** Las preguntas de esta rama se contestan por la voz. Un fotograma
  se abre solo por instante localizado (ADR-0038), y no hacía falta ninguno para decidir la
  propuesta. Si el consultor quiere ver el gráfico de un ejemplo (A-50, A-21), los instantes
  localizados son los de las citas.
- **Ningún registro de feedback, ningún parámetro, ninguna regla y ninguna ambigüedad cambiados.**
- **La cuarentena no se reconstruyó**, salvo los tres bloques de A-42 (66:38–67:51), que se sacaron
  **con máscara** por orden del consultor. Los otros cinco bloques siguen sin leer.
- **E-1, E-2 y E-3** se definieron tras la revisión del consultor, con el texto de la hoja, en
  `scripts/transcribir_sesion.py`.

## Estado

**Rama `trabajo/sesion-03`: REVISADA por el consultor el 2026-09-29 y cerrada en `main` por su
orden (tag `stable/F30-sesion-03`).** Extracción sobre la versión filtrada, con el tramo de A-42 con
máscara; 62 ítems de evidencia `ev-v9-*` nuevos; nada resuelto en esta rama. La activación de lo
que resuelve va en `trabajo/activar-sesion-03`; A-42 espera a la revisión del consultor.
