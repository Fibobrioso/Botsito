# La hoja que se llevó a la sesión 6 (2026-11-04)

Rama `trabajo/sesion-06`. Escrita el 2026-11-05 desde el encargo del consultor
(`docs/encargos/trabajo-sesion-06.md`, «La hoja que se llevó») y las respuestas b), c) y d) de Aleks
(`docs/validation/SESION-06-EXTRACCION.md` §0.1). **No lleva ninguna cita del trader**: la hoja fue
el PDF del consultor (`Sesion-6-preguntas-trader.pdf`), hecho desde `docs/sesion-6/PREGUNTAS.md`, que
no va al repositorio; Aleks no tiene hoja con notas (respuesta d); y la fuente de cada respuesta es la
voz (v17), no la hoja (`docs/runbooks/SESION-DE-PREGUNTAS.md`). Del PDF se quitaron las líneas «Para
Aleks» y los gráficos de S-7 a S-12.

## 1. Un solo vídeo

| Vídeo | Fecha | Duración | Lo que lleva |
|---|---|---|---|
| v17 | 2026-11-04 | 1:59:59 | S-1 a S-8, S-13 a S-23 y «Para cerrar». El corte previsto en S-17 (decisión 0 de `BARRIDO-SESION-6.md`) no hizo falta |

Id de sesión: `2026-11-04-sesion-06`.

## 2. Los códigos de voz

S-1 a S-23, dichos en voz como «pregunta S1» … «S1 cerrado». S-n es la pregunta n de
`docs/sesion-6/PREGUNTAS.md`. **No son los de la sesión 5.** La filtrada se agrupó con la hoja de la
sesión 6 (`scripts/transcribir_sesion.py` de `main`, `--sesion 06`).

| código | título usado | n.º en PREGUNTAS.md | ambigüedad o fuente | vídeo |
|---|---|---|---|---|
| S-1 | La pérdida del día que te hace parar: solo con las cerradas o también con la abierta | 1 | A-44 | v17 |
| S-2 | Cuándo vuelves a contar desde cero después de parar por la pérdida del día | 2 | A-44 | v17 |
| S-3 | La mecha que mueve tu alto de M15, y la vela que lo toma después | 3 | A-35 | v17 |
| S-4 | En M15, una vela sin cuerpo entre las verdes y la roja | 4 | A-35 | v17 |
| S-5 | Después de la toma, un retroceso con alternancia y un punto nuevo limpio | 5 | `ACTIVAR-SESION-05-MOTOR.md` §2.5, dibujo 2 | v17 |
| S-6 | La orden puesta en el primer punto que se llena antes de que haya alternancia | 6 | `ACTIVAR-SESION-05-MOTOR.md` §2.5, dibujo 3; `RECORRIDA-CONSTRUCCION.md` §3 | v17 |
| S-7 | Gráfico 1 | 7 | `ACTIVAR-SESION-05.md` §3.12; `RECORRIDA-CONSTRUCCION.md` §4 | v17 |
| S-8 | Gráfico 2 | 8 | como S-7 | v17 (a medias) |
| S-9 | Gráfico 3 | 9 | como S-7 | no se hizo |
| S-10 | Gráfico 4 | 10 | como S-7 | no se hizo |
| S-11 | Gráfico 5 | 11 | como S-7 | no se hizo |
| S-12 | Gráfico 6 | 12 | como S-7 | no se hizo |
| S-13 | Cuándo pasas el stop a la entrada: al toque o al cierre de la vela de M1 | 13 | A-13 | v17 |
| S-14 | La orden sin llenar cuando el precio toma otra liquidez de M15 | 14 | A-53 | v17 |
| S-15 | La misma liquidez tomada antes de las 7 y otra vez después | 15 | A-43 | v17 |
| S-16 | Los dos extremos de la caja: qué velas dan el 1 | 16 | A-48 y A-49 | v17 |
| S-17 | Frente al nivel tomado: solo el 0 o la caja entera | 17 | A-50 | v17 |
| S-18 | Las reentradas en el mismo punto | 18 | ADR-0083 | v17 |
| S-19 | El precio ya está más allá del 0 cuando se forma la caja | 19 | `ACTIVAR-SESION-05.md` §3.9 | v17 |
| S-20 | La vela de 1 o 2 puntos en el retroceso, y la vela sin cuerpo con mechas largas | 20 | `ACTIVAR-SESION-05.md` §3.10; `ACTIVAR-SESION-05-MOTOR.md` §2.2 y §2.6 | v17 |
| S-21 | El punto de breaker roto con la mecha después de una alternancia | 21 | `ACTIVAR-SESION-05.md` §3.11; ADR-0076 §4; ADR-0085 | v17 |
| S-22 | Para que el máximo de la verde sea tu punto, ¿qué tiene que hacer la roja? | 22 | `ACTIVAR-SESION-05-MOTOR.md` §2.4 | v17 |
| S-23 | Una toma de la mañana, y por la tarde el mismo sesgo | 23 | A-46; `ACTIVAR-SESION-05.md` §3.13 | v17 |

## 3. El orden de la sesión, y las que no se hicieron

S-1 a S-8 y S-13 a S-23, en el orden de `PREGUNTAS.md` (respuesta b; medido en la filtrada). Una pausa
del trader en S-17, de 75:21 a 83:20.

**No se hicieron: S-9, S-10, S-11 y S-12** (gráficos 3 a 6). **S-8 quedó a medias**, sin decisión. Se
acordó en voz dejarlos para otro momento, rehechos. Según Aleks, «las de gráficos y ejemplos» no se
hicieron; la medida lo matiza: el gráfico 1 sí se contestó, y S-5 y S-6, que llevan los dibujos 2 y 3,
sí se preguntaron (`SESION-06-EXTRACCION.md` §0.1 y §2.4).

## 4. Los esquemas inventados

Los de la hoja, todos INVENTADOS y rotulados «Esquema inventado, no es un día real», sin precios ni
fechas: S-1, S-3 (dos), S-4, S-5 (dibujo 2), S-6 (dibujo 3), S-13, S-14, S-15, S-16, S-17 (dibujos A y
B), S-18, S-19, S-20, S-21, S-22 y S-23. Las que no llevan esquema: S-2 y los gráficos. La lista sale de
`PREGUNTAS.md`, no de la pantalla: en esta rama no se abre ningún fotograma. Para contestar, el trader
dibujó sobre ellos y compartió su gráfico de julio (respuesta a; `SESION-06-EXTRACCION.md` §2.4).

## 5. Los gráficos enseñados

| Gráfico | Limpio | Marcado | Cómo |
|---|---|---|---|
| gráfico 1 (S-7) | sí, primero | sí, después | por WhatsApp, durante la llamada |
| gráfico 2 (S-8) | sí, primero | sí, después | por WhatsApp, durante la llamada |
| gráficos 3 a 6 (S-9 a S-12) | no | no | no se hicieron |

Sin fecha visible. Qué día es cada uno vive solo en `clave.txt`, fuera del repositorio (decisión del
consultor del 2026-11-01). La hoja decía que los enseñaba Aleks en pantalla; se pasaron al trader por
WhatsApp, y él los abrió en su lado.

## 6. «Para cerrar» (sin código de voz)

Se hizo en voz, al final de v17 (respuesta c): diciembre (NA:I) y la exportación de agosto (NA:Q). No se
saltó y no hay capturas. Lo que contestó está en `SESION-06-EXTRACCION.md` §3.5.
