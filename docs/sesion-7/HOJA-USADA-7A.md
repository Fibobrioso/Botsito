# La hoja que se llevó a la sesión 7a (2026-11-16 y 2026-11-17)

Rama `trabajo/sesion-07`. Escrita el 2026-11-17 desde el encargo del consultor
(`docs/encargos/trabajo-sesion-07.md`, «La hoja que se llevó») y las respuestas a) a d) de Aleks
(`docs/validation/SESION-07-EXTRACCION.md` §0.0), contrastadas con la filtrada. **No lleva ninguna
cita del trader**: la hoja fue el PDF del consultor (`Sesion-7a-preguntas-trader.pdf`), hecho desde
`docs/sesion-7/PREGUNTAS-7A.md`, que no va al repositorio; Aleks no tiene hoja con notas (respuesta d);
y la fuente de cada respuesta es la voz (v18 y v19), no la hoja
(`docs/runbooks/SESION-DE-PREGUNTAS.md`). Del PDF se quitaron las líneas «Para Aleks» y el §1 entero
(el bloque de días). Las láminas las enseñó Aleks desde una carpeta fuera del repositorio; qué carpeta
es qué sesión, y cuántas láminas se enseñaron de cada una, no se escriben aquí.

## 1. Dos vídeos, dos días

| Vídeo | Fecha | Duración | Lo que lleva |
|---|---|---|---|
| v18 | 2026-11-16 | 1:52:26 | S-1 a S-6, en el orden de la hoja; el bloque de días: sesiones 1 y 2 |
| v19 | 2026-11-17 | 1:35:55 | el bloque de días: sesiones 3 y 4 y la reserva del 13 de abril |

Id de sesión de los dos: `2026-11-16-sesion-07` (el del primer día). La Next Action F la daba para el
domingo 2026-11-15.

## 2. Los códigos de voz

S-1 a S-6 de la 7a, dichos en voz como «pregunta S1» … «S1 cerrada». S-n es la pregunta n de
`docs/sesion-7/PREGUNTAS-7A.md`. **No son los de la sesión 6 ni los de la 7b.** Cada filtrada se
agrupó con la hoja de la 07 (`scripts/transcribir_sesion.py` de `main`, `--sesion 07`, una por
vídeo). El bloque de días no lleva códigos.

| código | título usado | n.º en PREGUNTAS-7A.md | ambigüedad o fuente | vídeo |
|---|---|---|---|---|
| S-1 | Qué vela es tu rango de H4, y cuándo lo das por actualizado | 1 | `VIDEO-JULIO.md` §7 #1 a #3 (su «Para Aleks»; RN-003) | v18 |
| S-2 | Cuándo pasas el stop a la entrada | 2 | A-13 | v18 |
| S-3 | Qué zonas cuentas como zonas de control de un esquema | 3 | RN-009 | v18 |
| S-4 | La mecha que pasa tu alto de M15, y la vela que lo toma | 4 | A-35 | v18 |
| S-5 | En qué momento pones la orden respecto de la ruptura de tu punto | 5 | ADR-0064; F7 #6 de `VIDEO-JULIO.md` (su «Para Aleks») | v18 |
| S-6 | Las entradas que dejas sin tomar en el backtest | 6 | F7 #10 de `VIDEO-JULIO.md` (su «Para Aleks») | v18 |

## 3. El orden de la sesión, y lo que no se hizo

Las seis preguntas, en el orden de la hoja, en v18 (respuesta b; medido en la filtrada). Las seis
frases de «Para confirmar al final» se leyeron, cada una al final de su pregunta y no juntas al
final; dos quedaron a medias (S-3 y S-4). **Ninguna pregunta técnica quedó sin hacer.** En S-4, la
pregunta 1 se leyó y no se contestó. En el bloque de días no se hizo la pregunta «¿siempre, solo en
este caso, o de qué depende?» a ninguna corrección.

## 4. Los esquemas inventados

Los de la hoja, todos INVENTADOS y rotulados «Esquema inventado, no es un día real», con el marco
escrito en el dibujo y sin precios ni fechas: S-1 («4 horas»), S-2 («M1»), S-3 («M15» y «M1»), S-4
(«M15», el de la pregunta 2) y S-5 («M1»). S-6 no lleva esquema. La lista sale de `PREGUNTAS-7A.md`,
no de la pantalla: en esta rama no se abre ningún fotograma. Para contestar S-1, S-2, S-4 y S-5 el
trader pasó también a su gráfico real con marcas (`SESION-07-EXTRACCION.md` §3 y §7).

## 5. El bloque de días

Las sesiones de la tabla de `PREGUNTAS-7A.md` §1 que se hicieron, en su orden real:

| Orden real | Sesión de la tabla | Vídeo | Empieza (situada por la voz) |
|---|---|---|---|
| 1 | 1 · 2026-07-07, 11-15 | v18 | `[39:28]` |
| 2 | 2 · 2026-07-02, 11-15 | v18 | `[63:15]` |
| 3 | 3 · 2026-07-03, 07-11 (según la respuesta b) | v19 | el arranque del vídeo; **su día cae en un bloque de cuarentena y la voz no lo sitúa** (PARADA 2 del informe) |
| 4 | 4 · 2026-07-15, 11-15 | v19 | `[28:42]` |
| 5 | reserva · 2026-04-13, 07-11 | v19 | `[44:03]`; el trader abrió antes, por error, el 15 de abril |

**No se hizo** la reserva del 2026-07-06, 07-11. Si el trader abrió cada replay antes de compartir
pantalla no se sabe (respuesta b). En la sesión 1 no marcó ni operó la sesión primero: fue directo a
las láminas, con trazos que ya tenía; en la 2 y la 4 borró trazos anteriores y operó ante la cámara.

## 6. WhatsApp (respuesta c)

El trader no contestó nada por WhatsApp a lo del proyecto (la fecha de la 7b, el vídeo de mapeo,
diciembre, la exportación de agosto): ninguna captura nueva en «Mensajes del trader». En lo leído de
las filtradas (todo, salvo la sesión que abre v19, en PARADA) no se habla de ello.
