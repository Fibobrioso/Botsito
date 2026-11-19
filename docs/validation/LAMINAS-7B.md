# LAMINAS-7B · El bloque de días de la 7b, PREGUNTAS-7B.md revisado y sus láminas (R4.3, entrada F)

> PLANTILLA hasta la fase 0 (la línea con que nació): la fase 0 ya está, abajo.

Rama `trabajo/laminas-sesion-7b`, abierta el 2026-11-18 desde `main` en b174d714 (commit de estado
sobre el merge cf33a916 del tag `stable/F39e-activar-sesion-07`). Encargo:
`docs/encargos/trabajo-laminas-sesion-7b.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
punto (1) de la F de la Next Action). Tag previsto: `stable/F39f-laminas-sesion-7b` (no existe ni en
local ni en origin: `git tag -l 'stable/F39f*'` y `git ls-remote --tags origin 'stable/F39f*'`
vacíos). Riesgo fijado al abrir como **alto**, como manda el encargo (alto si entra el arreglo de F2
en `src/botsito/engine/`, medio si no); se dirá al final cuál fue.

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `b174d714194fd1a61dc9ddc7b85407b979441a6e` dos veces; `git status --short` vacío.
- Último `- Tag:` de HISTORIA: `stable/F39e-activar-sesion-07`; `git rev-parse "stable/F39e-activar-sesion-07^{commit}"` = `git rev-parse main^1` = `cf33a9161293bf672dabf3e2f4e03084bf62df48`; en origin: `git ls-remote --tags origin stable/F39e-activar-sesion-07` da el objeto del tag anotado `1f1bac89…`.
- CI de `main` sobre su HEAD: `gh run view 44446460628` → `completed` / `success`, `headSha` `b174d714194fd1a61dc9ddc7b85407b979441a6e`, rama `main`, flujo `ci`.
- Ninguna otra rama: `git branch --list` solo `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Fase 0 (2026-11-18; skill fase-cero, sin tocar nada)

La PARADA de este encargo es condicional: cada paso cuya medida cuadra con la decisión del
consultor se hace, y lo que no cuadra va a la PARADA final. La fase 0 no para.

### 0.1 Lo que el encargo hereda

| # | Herencia | Dónde | Qué se hace aquí |
|---|---|---|---|
| 1 | Las láminas de la 7b, la revisión de `PREGUNTAS-7B.md` y `SESION_EN_CURSO = "08"` | ACTIVAR-SESION-07.md:660-677 («Para la rama siguiente»); recuadro D4 de `PREGUNTAS-7B.md:8-14` | F2, F3 |
| 2 | El 01-07 y el 01-13 tienen menos de 60 H4 cargadas (20 y 44) | ACTIVAR-SESION-07.md:450-455 y :662-665 | F1.1: salen |
| 3 | Las preguntas reformuladas (A-35 pregunta 1, A-58, las zonas de control, el margen del break even, A-43) | ACTIVAR-SESION-07.md:649-658 | F3 (A-43 pasa a §3 por el encargo; ACTIVAR:657 la llevaba a «Lo que nos has dicho» de su pregunta) |
| 4 | El 2026-04-15 no está gastado; el 2026-07-03 de 07 a 11 sí | ACTIVAR-SESION-07.md:668-672; respuesta del consultor a su PARADA final, punto 7 | F1.3, F1.4 |
| 5 | El `LaminaError` de RN-004 (punto 1) y b1 (punto 2) | LAMINAS-MOTIVOS.md:469-479; respuesta del consultor, :826 | F2.2 |
| 6 | La línea para la skill `activar-sesion` | ACTIVAR-SESION-07.md:706-709 | F4 |
| 7 | La F de la Next Action, punto (1) | `PROJECT_STATE.md`, Next Action | F nueva, para la orden de cierre |

### 0.2 El bloque de días: H4 cargadas y compuerta de ADR-0093 §3, hoy

Los dos guiones, en `anexos/LAMINAS-7B/` (su README), con su fila de HOLDOUT del día antes de
correrlos. `h4_cargadas.py` parte de `arranque.py` pero no imprime el sesgo (el encargo pide solo
esos dos datos; auditor, fila 17); `compuerta_7b.py` es `dias_d3.py` con las siete candidatas.

| Sesión | Papel | H4 cerradas cargadas al abrir | ≥ 60 | Compuerta (a, b, c) |
|---|---|---|---|---|
| 2026-04-24 07-11 | sesión 1 (entra) | 236 | sí | PASA |
| 2026-04-15 11-15 | sesión 2 | 195 | sí | PASA |
| 2026-04-27 11-15 | sesión 3 (entra) | 243 | sí | PASA |
| 2026-01-19 11-15 | sesión 4 | 69 | sí | PASA |
| 2026-01-21 07-11 | reserva | 80 | sí | PASA |
| 2026-01-22 11-15 | reserva | 87 | sí | PASA |
| 2026-07-16 07-11 | reserva | 200 | sí | PASA |

Las cinco que ya medía F1.3 dan lo mismo (195, 69, 80, 87, 200). La compuerta: 76 días `dev` de
construcción, 0 en `casos_ocultos` y 0 en `casos_reservados` (34 y 34, contados, sin imprimir ids);
ninguna de las siete con hora perdida ni fila «posible M» (`compuerta-7b.txt`).

### 0.3 Las filas de cada pregunta candidata, sobre fuentes commiteadas

| Pregunta | Filas (julio / total) | Fuente | Toca el dinero |
|---|---|---|---|
| A-35, la mecha que vuelve | sin recuento por fila | PREPARACION-SESION-7.md §0.3, A-6 (decide cada toma de M15) | sí |
| Las zonas de control (RN-009) | 8 en julio con el gate RN-009, línea base / — | TRAZAS-ABLACION.md 5.2 (no es un anexo de los tres que nombra el encargo; no hay otra) | — |
| El margen del break even (A-13) | sin recuento por fila | ninguna (las 100 `stop_movido` de `cuenta-por-mes.txt` son del break even al toque) | sí |
| A-58, el rango nuevo | sin recuento por fila de A-58 | la P1 de julio, que es lo que movía el rango, es 1 tras activar la 7a (`anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`; 20 en la base) | — |
| A-48, el 0 de la caja | **16 / 44 con el stop fuera; 7 / 24 P2 a 4-10 puntos**, línea base | `anexos/RECORRIDA-CONSTRUCCION-2/caja-stop.txt` (`grep -c "| stop fuera |"`: 44; de julio, 16); `anexos/PREPARACION-SESION-7/sustitutas.txt` («P2 4-10: 24 filas») | — |
| S-22, el punto de breaker | sin recuento por fila | quita el 52 % de los puntos de breaker (ACTIVAR-SESION-06-MOTOR.md:148-154), no por fila | — |
| S-19, el precio más allá del 0 | sin recuento por fila | 32 rechazos al colocar (TRAZAS-ABLACION.md 5.4), no por fila | — |
| §3 · la reentrada | **4 en julio tras activar la 7a** (P7; 3 en la base) / 4 en la base | `anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`; RECORRIDA-CONSTRUCCION-2.md:1319 | — |
| §3 · A-53 | sin recuento por fila | — | — |
| §3 · A-43 | sin recuento por fila | — | — |
| §3 · el breaker por la mecha más larga | sin recuento por fila | — | — |
| §3 · 2026-07-01 de 11 a 15 | **3** (1 P1 del trader y 2 P5 del bot, tras activar la 7a) / — | `anexos/ACTIVAR-SESION-07/delta-julio-base-f1.txt` (la sesión no cambia de F1 a F2: `delta-julio-f1-f2.txt`) | — |

**El orden de S-3 a S-6 que sale** (encargo, F3: de más a menos filas, las que no tienen recuento
detrás): **A-48** (la única con recuento) pasa a S-3, y **A-58** a S-4, delante de S-22 y S-19, en
el orden del encargo. S-1 y S-2 no se mueven. Cambia lo que el encargo daba por defecto (S-3 = A-58,
S-4 = A-48), por la regla del propio encargo.

**§3 con más filas que S-5 o S-6**: la reentrada (4) y la del 2026-07-01 (3) tienen más que S-22 y
S-19, que no tienen recuento (las dos de antes, B-7 con 3 y B-8 con 2, también). Va a la PARADA
final, sin cambiarlas (encargo, F3).

### El encargo frente al repo (auditor-encargo, 2026-11-18)

38 afirmaciones: 26 correctas, 3 incorrectas y 9 con matiz; 7 herencias que el encargo no recoge.
Lo que cambia algo, y qué se hizo:

| # | Hallazgo | Qué se hace |
|---|---|---|
| 24 | **INCORRECTA**: `filas-por-sesion.txt` no tiene filas de 2026-04-24 ni de 2026-04-27, y es de la corrida vieja | Se cuentan con el mismo guion (`filas_por_sesion.py`, idéntico al de `main`) sobre la misma fuente (`filas-por-sesion-7b.txt`). Desviación 1 |
| 41 | **INCORRECTA**: «Lo que nos has dicho» puede citar lo que cita SESION-07-EXTRACCION.md, pero solo se puede leer lo que cita PREGUNTAS-7B.md o ACTIVAR-SESION-07.md | Todo ítem de «Lo que nos has dicho» de las preguntas nuevas lo cita ACTIVAR-SESION-07.md, y se leyó. `ev-v19-011640-1fdc33a7` (solo en SESION-07-EXTRACCION.md) va citado en «Para Aleks» por esa extracción, sin leerlo |
| herencia 1 | La reserva 07-16 dice «es una pareja», y tras F1 ya no lo es (RN-032; ACTIVAR:505) | En §1: «era una pareja en la línea base y, tras activar la 7a, ya no» |
| herencia 3 | D4 pedía las filas «con la corrida nueva»; para enero y abril no hay ninguna commiteada | Desviación 1 |
| 9 | (b) choca con LAMINAS-MOTIVOS.md:537: la foto no dice si la otra causa de tope se cumple | F2.2: se mide lo que se puede (los cortes con `detenido_por_tope` encendido); si sale alguno, la segunda mitad va a la PARADA final |
| 12 | Un `LaminaError` aborta toda la llamada de `motor laminas`, no una sesión | F2: si pasa, las llamadas por separado que hagan falta para saber cuál (cada una, dos corridas) |
| herencia 6 | Hay otro `LaminaError` sin medir: `detenido_por_tope` con origen en RN-020 y RN-029 a la vez | Se mide igual en F2 (cualquier `LaminaError` lo dice) |
| 21 | «Las dos únicas» de `sustitutas.txt` solo es cierta con las tres condiciones juntas (01-08, 01-09 y 07-02 11-15 también «cumplen»: las dos primeras están en F1.3 y la tercera se usó en la 7a) y sobre las 20 filas que el fichero imprime de 44 | Se dice; no cambia la elección |
| 31 | En las filas de ERRORES-RECURRENTES de la 7a están la fecha al abrir cada gráfico, los esquemas y el «¿siempre…?»; borrar las marcas y operar antes de las láminas salen de SESION-07-EXTRACCION.md §5.1, punto 8; la fecha «después de abrir cada replay» no está escrita en ningún sitio | Los pasos de §1 se escriben como los decide el consultor (F1.5), con las dos fuentes nombradas |
| 34 | ADR-0093 §1 dice «las que más filas mueven y las que tocan el dinero», sin fijar cuál va antes | El orden «dinero primero» es lectura del consultor; se aplica y se dice |
| 42 | entregar-rama pone la CI antes del revisor | Gana la skill (el encargo lo dice) |
| 14 | «LAMINAS.md: sola» es `docs/runbooks/LAMINAS.md:34` | Se sigue ese |

### Lo que no pude medir (todavía)

- Si las láminas con el motor de F39e dan algún `LaminaError` (F2).
- La segunda mitad de (b): si, con `detenido_por_tope` encendido por una regla, la otra causa de
  tope también se cumple. La foto no lo guarda (LAMINAS-MOTIVOS.md:537).
- Las filas del bloque con el motor de F39e: no hay una corrida commiteada de enero ni de abril, y
  el encargo no autoriza ninguna fuera de `motor laminas`.

### Exposiciones

Dos filas del 2026-11-18 en `HOLDOUT-EXPOSICIONES.md`: la de la apertura (los `make check`) y la de
0.2 (las dos medidas, que calientan con el M1 de marzo y de junio, como el arnés). El conteo de
filas con `filas_por_sesion.py` (solo lee un anexo commiteado de construcción) se corrió antes de la
segunda fila: **escrita tarde para ese punto**, y lo dice.

## F1 · El bloque de días (CUADRA)

Las siete sesiones pasan hoy la compuerta y tienen 60 o más H4 (0.2). Lo hecho, en el §0 y el §1 de
`docs/sesion-7/PREGUNTAS-7B.md`, con la numeración de hoy (la caja es aún S-1; F3 renumera):
1. Salen 2026-01-13 07-11 y 2026-01-07 07-11 (44 y 20 H4 cargadas).
2. Entran 2026-04-24 07-11 y 2026-04-27 11-15 (de `sustitutas.txt`: «stop fuera», 0,62, «cumple»);
   «Sirve a» y las filas, de `sustitutas.txt` y de `filas-por-sesion-7b.txt`. Las reservas no
   cambian (salvo el «es una pareja» de 07-16, arriba).
3. El 2026-04-15 de 11 a 15 se queda como sesión 2; §1 dice que el trader ya lo marcó y lo operó en
   la 7a, por error, y el paso de la sesión de replay nueva y sin marcas va subrayado para ese día.
   La frase del pie («el bloque de días es la primera vez que se le oye operarlas») se corrige.
4. El 2026-07-03 de 07 a 11 no se usa.
5. Los pasos de cada sesión ganan lo aprendido en la 7a (F1.5 del encargo), en siete pasos
   numerados, más la línea del bloque técnico (solo esquemas; un ejemplo en su gráfico, solo de un
   día de construcción y con la fecha en voz alta).

3b (una sesión sin láminas sale) se mide en F2.

## Desviaciones

1. **Las filas de las dos sesiones que entran no salen de `filas-por-sesion.txt`**, que no las
   tiene: salen del mismo guion sobre la misma fuente (`anexos/LAMINAS-7B/filas-por-sesion-7b.txt`).
   Y son, como todas las de §1, de la línea base, anterior a activar la 7a; el recuadro D4 pedía «la
   corrida nueva», que para enero y abril no existe commiteada (auditor, fila 24 y herencia 3).

## Estado

EN CURSO: fase 0 y F1 hechas; F2 (las láminas) a continuación.
