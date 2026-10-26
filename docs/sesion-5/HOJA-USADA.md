# La hoja que se llevó a la sesión 5 (2026-10-23 y 2026-10-25)

Rama `trabajo/sesion-05`. Escrita el 2026-10-25 desde el encargo del consultor
(`docs/encargos/trabajo-sesion-05.md`, «La hoja que se llevó») y las respuestas b) y d) de Aleks
(`docs/validation/SESION-05-EXTRACCION.md` §0.1). **No lleva ninguna cita del trader**: la hoja fue
el PDF del consultor (`Sesion-5-preguntas-trader.pdf`), hecho desde `docs/sesion-5/PREGUNTAS.md`,
que no va al repositorio; Aleks no tiene hoja con notas (respuesta d); y la fuente de cada respuesta
es la voz (v15 y v16), no la hoja (`docs/runbooks/SESION-DE-PREGUNTAS.md`).

## 1. La sesión se partió en dos días

| Vídeo | Fecha | Duración | Lo que lleva |
|---|---|---|---|
| v15 | 2026-10-23 | 1:40:57 | S-1 a S-17 enteras y el arranque de S-18, que se corta al final de la grabación |
| v16 | 2026-10-25 | 34:50 | S-18 desde el principio, S-19 a S-25 y «Para cerrar» |

Es una sola sesión, con un solo id (`2026-10-23-sesion-05`), la misma hoja y los mismos códigos de
voz. La S-18 que vale es la de v16; la de v15 queda como incompleta (respuesta b).

## 2. Los códigos de voz

S-1 a S-25, dichos en voz como «pregunta ese uno» … «S1 cerrada». S-n es la pregunta n de
`docs/sesion-5/PREGUNTAS.md`. **No son los de la sesión 4**: allí S-13 era la vela de 4 horas que
rompe por los dos lados y S-14 la vela casi plana; aquí las confirman S-23 y S-24. La filtrada de
cada vídeo se agrupó con la hoja de la sesión 5 (`scripts/transcribir_sesion.py` de `main`,
`--sesion 05`).

| código | título usado | n.º en PREGUNTAS.md | ambigüedad o fuente | vídeo |
|---|---|---|---|---|
| S-1 | Con el sesgo bajista, una vela de 4 horas rompe el máximo de la anterior solo con la mecha y cierra roja | 1 | `SESGO-H4-COLOR.md` §4.4, pregunta 2; ADR-0080 | v15 |
| S-2 | La vela de 4 horas que rompe con la mecha y cierra sin cuerpo | 2 | `SESGO-H4-COLOR.md` §4.4, pregunta 1; ADR-0080 §4 | v15 |
| S-3 | Cuándo das por formado un alto o un bajo de M15 | 3 | A-35 | v15 |
| S-4 | El tope de la semana | 4 | A-44 | v15 |
| S-5 | El lote que no cabe | 5 | A-57 | v15 |
| S-6 | Las reentradas en el mismo punto tras un stop, y su caja | 6 | `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 3, con `PUNTO-USADO.md` §5 (ADR-0083) | v15 |
| S-7 | Los dos extremos de la caja: dónde pones el 0 y hasta dónde llevas el 1 (título del recuadro) | 7 | A-48 y A-49 | v15 |
| S-8 | Una vela sin cuerpo dentro del tramo que marca el punto de breaker | 8 | `VISOR-CONSTRUCCION.md` §3.2, pregunta A | v15 |
| S-9 | Qué liquidez eliges cuando hay varias | 9 | `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 5 | v15 |
| S-10 | La misma liquidez tomada dos veces, antes y después de las 7 | 10 | A-43 | v15 |
| S-11 | Una toma de la sesión de la mañana con el sesgo contrario | 11 | `VISOR-CONSTRUCCION.md` §3.2, pregunta B | v15 |
| S-12 | De qué lado del nivel tomado va tu caja, y si puede quedar a caballo (título del recuadro) | 12 | RN-005 frente a `ev-v9-004919-c6bfb3ee` (el lado), y A-50 | v15 |
| S-13 | Hasta cuándo mueves una orden sin llenar, y cuándo la quitas | 13 | A-53 | v15 |
| S-14 | Qué te hace no operar un día o una sesión | 14 | `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 7 | v15 |
| S-15 | Entrar en la segunda zona después de la toma | 15 | `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 8 | v15 |
| S-16 | El precio ya está más allá del 0 cuando se forma la caja | 16 | `CORRIDA-CONSTRUCCION.md` §4.5, pregunta 9 | v15 |
| S-17 | Cuándo pasas el stop a la entrada | 17 | A-13 | v15 |
| S-18 | Una línea de M1 que, rota con la mecha, te quite la entrada | 18 | A-32 | v15 (incompleta) y v16 |
| S-19 | Una vela sin cuerpo en medio del retroceso | 19 | ADR-0076 §4, pregunta 1 | v16 |
| S-20 | El punto de breaker roto solo con la mecha de una vela contraria | 20 | ADR-0076 §4, pregunta 2 | v16 |
| S-21 | La racha después de la novena pérdida | 21 | ADR-0077 §5 | v16 |
| S-22 | El último minuto: a qué hora quitas la orden sin llenar | 22 | RN-035 (`ventana_fin`) | v16 |
| S-23 | La vela de 4 horas sin color, con el sesgo bajista | 23 | ADR-0075 | v16 |
| S-24 | La vela casi plana: de cuántos puntos | 24 | RN-007 (NA:H) | v16 |
| S-25 | El Excel de julio y los tres primeros vídeos | 25 | `ENTRADA-JULIO.md` §8 | v16 |

## 3. El orden de la sesión, y las que no se hicieron

S-1 a S-25 en el orden del PDF, que es el de `PREGUNTAS.md` (respuesta b): S-1 a S-18 en v15, y
S-18 (repetida desde el principio) a S-25 en v16; después, «Para cerrar».

**Se hicieron todas.** Ninguna quedó para WhatsApp ni para la sesión 6, aunque `PREGUNTAS.md` lo
preveía para S-25 y S-23 (WhatsApp) y S-18 (sesión 6) si faltaba tiempo.

## 4. Los textos de los recuadros que sustituyeron al cuerpo

Donde `PREGUNTAS.md` lleva un RECUADRO DE CORRECCIÓN del 2026-10-21 (rama
`trabajo/previa-sesion-5`), la hoja llevó el texto del recuadro. Comprobado en `PREGUNTAS.md`: son
cuatro, y solo tres cambian la hoja.
- **S-7**: lo que da el recuadro (el título de arriba, «Lo que todavía no sabemos», el esquema, la
  pregunta, «Para precisar» y la confirmación); «Lo que nos has dicho», del cuerpo, como dice el
  propio recuadro.
- **S-12**: lo que da el recuadro, en dos partes: primero de qué lado del nivel tomado va la caja
  (RN-005 frente a `ev-v9-004919-c6bfb3ee`) y después A-50, en la forma neutra «una parte de tu lado
  y otra del otro».
- **S-13**: solo la línea de «Para precisar» que da el recuadro («Si el 1 de la caja baja mucho (la
  caja se hace muy grande), ¿la sigues moviendo igual?»). **En voz se leyó la línea del cuerpo, sin
  corregir** (`SESION-05-EXTRACCION.md` §3.3, S-13).
- **S-15**: la hoja no cambia; el recuadro corrige un «Para Aleks», que no va a la hoja.

Los otros dos recuadros de `PREGUNTAS.md` no cambian la hoja: el del 2026-10-22
(`trabajo/hoja-sesion-05`, los códigos en el guion) y el del 2026-10-23 (`trabajo/guardia-ci`,
A.4).

## 5. Los esquemas que se enseñaron

Los de la hoja, todos INVENTADOS y rotulados «Esquema inventado, no es un día real», sin precios ni
fechas: S-1, S-2, S-3, S-7 (el del recuadro), S-8, S-9, S-10, S-11, S-12 (el del recuadro), S-13,
S-15, S-16, S-17, S-18, S-19, S-20, S-23 y S-24. Las que no llevan esquema: S-4, S-5, S-6, S-14,
S-21, S-22 y S-25. **No se enseñó ningún gráfico de un día real desde la hoja.** El trader, para
contestar, compartió su propio replay (respuesta a de Aleks; `SESION-05-EXTRACCION.md` §2.3 y
§2.6).

La lista sale de `PREGUNTAS.md`, no de la pantalla: en esta rama no se abre ningún fotograma
(decisión 1 del consultor).

## 6. «Para cerrar» (sin código de voz, en v16)

Las tres peticiones de `PREGUNTAS.md` §2, que no son de la operativa:
- **Diciembre** (NA:I): si el backtest de diciembre lo grabó en vídeo con su voz.
- **Agosto** (NA:Q): que mande la exportación del backtest de agosto que da por bueno.
- **Marzo** (`REGISTRO-MARZO.md` §2, paso 0): que mande **por escrito** que el backtest de marzo es
  material que ya ha visto.

Lo que contestó está en `SESION-05-EXTRACCION.md` §3.5.
