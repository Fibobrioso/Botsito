# La hoja que se llevó a la sesión 7b (2026-11-20 y 2026-11-21)

Rama `trabajo/sesion-08`. Escrita el 2026-11-21 desde el encargo del consultor
(`docs/encargos/trabajo-sesion-08.md`, «La hoja que se llevó») y las respuestas de Aleks
(`docs/validation/SESION-08-EXTRACCION.md` §0.3), contrastadas con la filtrada. **No lleva ninguna
cita del trader**: la hoja fue el PDF del consultor (`Sesion-7b-preguntas-trader.pdf`, 8 páginas),
hecho desde `docs/sesion-7/PREGUNTAS-7B.md`, que no va al repositorio; no hay hoja de notas
(respuesta d); y la fuente de cada respuesta es la voz (v20 y v21), no la hoja
(`docs/runbooks/SESION-DE-PREGUNTAS.md`). Del PDF se quitaron las líneas «Para Aleks», el §1 (el
bloque de días) y el §3. Las láminas salieron de una carpeta fuera del repositorio; qué carpeta es qué
sesión, y cuántas láminas se vieron de cada una, no se escriben aquí.

## 1. Dos vídeos, dos días

| Vídeo | Fecha | Duración | Lo que lleva |
|---|---|---|---|
| v20 | 2026-11-20 | 1:13:04 | S-1 a S-6, en el orden de la hoja, y S-7 al final |
| v21 | 2026-11-21 | 2:06:25 | el bloque de días: sesiones 1, 2, 3 y 4 y la primera reserva |

Id de sesión de los dos: `2026-11-20-sesion-08` (el del primer día).

## 2. Los códigos de voz

S-1 a S-7 de la 7b. S-n es la pregunta n de `docs/sesion-7/PREGUNTAS-7B.md`. **No son los de la 7a.**
La hoja los daba como «pregunta ese uno» … «fin de pregunta»; en la grabación se dijeron con otras
palabras en la mayoría (cuáles, en `SESION-08-EXTRACCION.md` §3.0), y por eso el guion solo detectó
dos. Cada filtrada se agrupó con la hoja de la 08 (`scripts/transcribir_sesion.py` de `main`,
`--sesion 08`, una por vídeo). El bloque de días no lleva códigos.

| código | título usado | n.º en PREGUNTAS-7B.md | ambigüedad o fuente | vídeo |
|---|---|---|---|---|
| S-1 | La mecha de un minuto que pasa tu alto de M15 y vuelve | 1 | A-35 | v20 |
| S-2 | Tus zonas de control y el momento del break even | 2 | RN-009 y A-13 | v20 |
| S-3 | Dónde pones el 0 de tu caja | 3 | A-48 | v20 |
| S-4 | Tu rango de 4 horas después de una ruptura | 4 | A-58 | v20 |
| S-5 | Para que el máximo de la verde sea tu punto, qué tiene que hacer la roja | 5 | S-22 | v20 |
| S-6 | El precio ya está más allá del 0 cuando se forma la caja | 6 | S-19 | v20 |
| S-7 | Una tarde que no está en el vídeo | 7 (material) | `VIDEO-JULIO.md` | v20 |

## 3. El orden de la sesión, y lo que no se hizo

Las siete preguntas, en el orden de la hoja, en v20 (respuesta b; medido en la filtrada). **Las leyó
y las dirigió el trader**: Aleks no estuvo toda la reunión (respuesta 3). Las seis frases de «Para
confirmar al final» se leyeron, cada una al final de su pregunta; la de S-5, a medias. **Ninguna
pregunta quedó sin hacer.** En S-1, S-2 y S-3 el trader pasó también a su gráfico real, sin decir el
día en voz; esos tramos no son citables (`SESION-08-EXTRACCION.md` §3.0). En el bloque de días no se
hizo la pregunta «¿siempre, solo en este caso, o de qué depende?» a ninguna corrección.

## 4. Los esquemas

Los del PDF, rotulados «Esquema inventado, no es un día real», con el marco escrito y sin precios ni
fechas: S-1 («M15» y «M1»), S-2 (dos dibujos, «M15» y «M1»), S-3 («M15» y «M1»), S-4 (dos dibujos, «4
horas»), S-5 («M1») y S-6 («M1»). S-7 no lleva esquema. La lista sale de `PREGUNTAS-7B.md`, no de la
pantalla: en esta rama no se abre ningún fotograma.

## 5. El bloque de días

Las sesiones de la tabla de `PREGUNTAS-7B.md` §1 que se hicieron, en su orden real, todas en v21:

| Orden real | Sesión de la tabla | Empieza (situada por la voz) |
|---|---|---|
| 1 | 1 · 2026-04-24, 07-11 | el arranque del vídeo; **la voz no la sitúa de forma visible** (no citable; el día queda gastado) |
| 2 | 2 · 2026-04-15, 11-15 | `[47:39]` (antes opera la sesión de 07 a 11 del mismo día) |
| 3 | 3 · 2026-04-27, 11-15 | `[71:35]` |
| 4 | 4 · 2026-01-19, 11-15 | `[87:23]` |
| 5 | reserva · 2026-01-21, 07-11 | `[112:19]` |

**No se hicieron** las reservas del 2026-01-22 (11-15) y del 2026-07-16 (07-11). Según Aleks, el
replay no se abrió antes de compartir pantalla (respuesta 5). En la sesión 2, la de 11 a 15 se operó
después de abrir sus láminas; en la 3, la 4 y la reserva, la sesión se operó antes de verlas.

## 6. Lo que dice la entrada c)

El trader todavía no ha contestado sobre febrero de 2026 grabado con su voz y su libro (la condición de
ADR-0096 para F26), la exportación de agosto (Q) ni diciembre con su voz (I). No hay capturas ni
material nuevo, y en lo leído de las filtradas no se habla de ello.
