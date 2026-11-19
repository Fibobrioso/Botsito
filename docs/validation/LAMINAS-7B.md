# LAMINAS-7B · El bloque de días de la 7b, PREGUNTAS-7B.md revisado y sus láminas (R4.3, entrada F)

> PLANTILLA hasta la fase 0 (la línea con que nació): la fase 0 ya está, abajo.

Rama `trabajo/laminas-sesion-7b`, abierta el 2026-11-18 desde `main` en b174d714 (commit de estado
sobre el merge cf33a916 del tag `stable/F39e-activar-sesion-07`). Encargo:
`docs/encargos/trabajo-laminas-sesion-7b.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
punto (1) de la F de la Next Action). Tag previsto: `stable/F39f-laminas-sesion-7b` (no existe ni en
local ni en origin: `git tag -l 'stable/F39f*'` y `git ls-remote --tags origin 'stable/F39f*'`
vacíos). Riesgo fijado al abrir como **alto**, como manda el encargo (alto si entra el arreglo de F2
en `src/botsito/engine/`, medio si no); se dirá al final cuál fue.

```ids-inexistentes
ADR-0095 — el encargo lo reservaba para el arreglo de F2; F2 no encontró nada y no existe
```

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
| herencia 1 | La reserva 07-16 dice «es una pareja», y tras F1 ya no lo es (ACTIVAR:505) | En §1 sale la mención de la pareja (primero se escribió lo que había cambiado; el revisor, b4, vio que dejaba deducir algo de sus láminas) |
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

Cuatro filas en `HOLDOUT-EXPOSICIONES.md`. Tres son del 2026-11-18: la apertura (los `make check`),
0.2 (las dos medidas, que calientan con el M1 de marzo y de junio, como el arnés) y F2 (`motor
laminas`, que calienta igual). La cuarta, del 2026-11-19, cubre los `make check` del último commit
y, **escrita tarde** (revisor, a1), lo leído el 18: documentos y anexos commiteados de
construcción, 20 ítems de evidencia de v18 y v19 citados por ACTIVAR-SESION-07.md y la búsqueda
con conteo sobre los HTML de las láminas. El conteo de filas con `filas_por_sesion.py` se corrió
antes de la fila de 0.2: **escrita tarde para ese punto**, y lo dice. El `make check` del commit de
F2 a F4 empezó el 18 y acabó a las 00:07 del 19, y lo cubre la fila de la apertura.

## F1 · El bloque de días (CUADRA)

Las siete sesiones pasan hoy la compuerta y tienen 60 o más H4 (0.2). Lo hecho, en el §0 y el §1 de
`docs/sesion-7/PREGUNTAS-7B.md`, con la numeración de hoy (la caja es aún S-1; F3 renumera):
1. Salen 2026-01-13 07-11 y 2026-01-07 07-11 (44 y 20 H4 cargadas).
2. Entran 2026-04-24 07-11 y 2026-04-27 11-15 (de `sustitutas.txt`: «stop fuera», 0,62, «cumple»);
   «Sirve a» y las filas, de `sustitutas.txt` y de `filas-por-sesion-7b.txt`. Las reservas no
   cambian (salvo que en la de 07-16 sale «es una pareja», arriba).
3. El 2026-04-15 de 11 a 15 se queda como sesión 2; §1 dice que el trader ya lo marcó y lo operó en
   la 7a, por error, y el paso de la sesión de replay nueva y sin marcas va subrayado para ese día.
   La frase del pie («el bloque de días es la primera vez que se le oye operarlas») se corrige.
4. El 2026-07-03 de 07 a 11 no se usa.
5. Los pasos de cada sesión ganan lo aprendido en la 7a (F1.5 del encargo), en siete pasos
   numerados, más la línea del bloque técnico (solo esquemas; un ejemplo en su gráfico, solo de un
   día de construcción y con la fecha en voz alta).

3b (una sesión sin láminas sale) se mide en F2.

## F2 · Las láminas, b1 y el `LaminaError` de F38y

**F2.1.** Con el bloque commiteado (93a70ed4) y su fila de HOLDOUT del día, una llamada, sola, sin
ningún `make check` a la vez: `uv run botsito motor laminas --sesiones <las siete, en un orden
barajado que no se escribe aquí> --salida C:\Users\USER\Desktop\laminas-sesion-7b-v1`. Salió con 0:
las dos corridas de dentro (con y sin el recolector) dan lo mismo; 620 s y un pico de 644 MiB.
`clave.txt` está en esa carpeta, fuera del repositorio, y la guarda Aleks. Cuántas láminas tiene
cada sesión y de qué tipo se dijo en el terminal, no aquí (F2.4).

**F2.2, solo recuentos:**

| Medida | Resultado |
|---|---|
| (a) `LaminaError` porque RN-004 abre escenario en el mismo cierre en que RN-016 o RN-001 dispararon por los intentos | **0**: la llamada no dio ningún `LaminaError` (tampoco el otro que nadie había medido, `detenido_por_tope` con origen en RN-020 y RN-029 a la vez; auditor, herencia 6) |
| (b) b1: cortes con `detenido_por_tope` encendido por una regla | **0** cortes: ninguna lámina lleva la frase de RN-020 ni la de RN-029 (`FRASE_TOPE_POR_REGLA`, `laminas.py:506-511`; búsqueda con conteo sobre los HTML de la salida). Con el hecho encendido no hay lámina de tipo a (RN-001 prohíbe colocar), y en una de tipo b saldría su frase o un `LaminaError`. Con 0 cortes, la segunda mitad (si la otra causa también se cumple), que la foto no guarda, no hace falta medirla |

**3b**: todas las sesiones del bloque dan al menos una lámina; ninguna sale.

**F2.3: ninguna de las dos pasa.** No se toca el motor: ni `src/botsito/engine/` ni ADR-0095, el ADR que el encargo reservaba para el arreglo (se queda en el
bloque `ids-inexistentes` del encargo: desviación 6), ni la corrida de julio de D0, ni
v2. La carpeta v1 es la de las láminas de la 7b. Las dos quedan como Technical Debt propuesto para
el cierre (abajo). Así, el riesgo fue medio en lo hecho, aunque el contrato lo fijó alto al abrir,
como manda el encargo.

**F2.4**: en el terminal, por sesión, cuántas láminas y de qué tipo (a, las órdenes del bot
llenadas; b, las operaciones del trader sin pareja), para que Aleks y el consultor las revisen.

## F3 · `PREGUNTAS-7B.md` revisado, y la hoja 08

- **Recuadro fechado arriba** (como el de PREGUNTAS-7A.md): qué cambió y por qué.
- **Las seis técnicas**, en el orden de 0.3: S-1, la mecha de un minuto que vuelve (A-35, NUEVA);
  S-2, las zonas de control y el break even (RN-009 y A-13, NUEVA, con dos preguntas); **S-3, la
  caja (A-48, la S-1 de antes, como está)**; **S-4, el rango de 4 horas (A-58, NUEVA)**; S-5, S-22
  (la S-2 de antes, como está); S-6, S-19 (la S-3 de antes, como está); S-7, la de material, al
  final, como está. El encargo daba A-58 como S-3 y A-48 como S-4; su propia regla las cambia,
  porque A-48 es la única de las cuatro con recuento por fila (0.3). Desviación del consultor,
  declarada en el encargo: S-22 y S-19 siguen entre las seis sin recuento por fila.
- **Cada pregunta nueva** con sus partes, la pregunta cerrada con «otra, ¿cuál?», su línea «Para
  Aleks» con el destino de cada respuesta (parámetro, opción y régimen) y el esquema descrito. La
  pregunta es la reformulada de ACTIVAR-SESION-07.md, tal cual; en S-1 las opciones van en el
  orden del dibujo (A, el alto de antes; B, la mecha nueva), no en el de la frase. «Lo que nos has dicho», solo con ítems que cita ACTIVAR-SESION-07.md, leídos y
  copiados de su `cita_literal`. En S-4, el «Para precisar» que pide el encargo.
- **A §3**, en su tabla y sin título `**S-n.**`: B-11, la reentrada; B-12, A-53, con
  `ev-v18-011801-8b4f738d`; B-13, A-43, con las dos de v19 (copiada la literal del ítem, no la
  glosa de ACTIVAR-SESION-07.md:657, que va entre comillas pero no es literal); B-14, el punto de
  breaker por la mecha más larga de la segunda vela del mismo color; B-15, la del 2026-07-01 de
  11 a 15, que lleva día y por eso, si entra, va al bloque de días.
- **La hoja 08**: `CODIGOS_DE_SESION_TEXTO["08"]` con los siete títulos, `SESION_EN_CURSO = "08"`
  y su comentario al día. `test_la_sesion_en_curso_es_la_07` se sustituye A PROPÓSITO por
  `test_la_sesion_en_curso_es_la_08`, como aquel a la de la 06; `test_la_hoja_08_es_la_de_preguntas_7b`
  pasa (`uv run pytest -q tests/unit/test_transcribir_sesion.py tests/unit/test_hoja_preguntas.py`:
  todos en verde). El recuento de tests no cambia (uno sale y otro entra).

## F4 · La línea de la skill

En `.claude/skills/activar-sesion/SKILL.md`, sección «El metodo de ADR-0093 §4», la viñeta que
decía que cómo se corre julio no está escrito se sustituye por la línea preparada en
ACTIVAR-SESION-07.md:706-709, tal cual. La guardia no negó la edición.

## Para la orden de cierre (preparado, sin aplicar)

**La F nueva de la Next Action** (sustituye a la de hoy):

> F. La sesión 7, en dos días con el método de ADR-0093 (R4.3; pivote en docs/plan/PIVOTES-SESION-7.yaml; línea base, RECORRIDA-CONSTRUCCION-2.md). La 7a (id 2026-11-16-sesion-07) está ingerida (SESION-07-EXTRACCION.md) y ACTIVADA (ACTIVAR-SESION-07.md, F39e: sesgo de H4 por el rango vigente, ADR-0094, con A-58 abierta; break even al cierre y con cuerpo, A-13 abierta solo por el margen). La 7b está lista para grabar (LAMINAS-7B.md, F39f): el bloque de días revisado (sin las sesiones de enero con menos de 60 H4), PREGUNTAS-7B.md con A-35, las zonas de control y el margen del break even, A-48, A-58, S-22 y S-19, sus láminas generadas fuera del repo (la clave, con Aleks) y SESION_EN_CURSO en "08". Siguiente, en este orden: (2) grabar, ingerir y activar la 7b, con la rama de S-22 y S-19; (3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6); antes de (3), el consultor decide cómo cuentan los frenos de la cuenta del mes (RN-032 y RN-036; F1.4 y F2.4 de ACTIVAR-SESION-07.md). El vídeo de mapeo (recibido el 2026-11-18): SIN ABRIR y fuera del repo, no se ingiere; octubre y noviembre de 2026, reservados. C y R6a en los huecos; R5.7 después de (3), sobre esa corrida.

**La línea de Estado de R4.3**: «**Estado:** ABIERTA (la 7a, ingerida en trabajo/sesion-07 y
activada en trabajo/activar-sesion-07, ACTIVAR-SESION-07.md; la 7b, preparada en
trabajo/laminas-sesion-7b, LAMINAS-7B.md: láminas, preguntas revisadas y hoja 08; falta grabarla,
ingerirla y activarla).»

**El «Qué es» de R4.3, puesto al día** (sustituye a la frase del reparto de la 7b y a «Las láminas
de la 7b las genera la activación de la 7a»): «… 7b (sesion-08), revisada el 2026-11-18 con lo que
dejó la 7a (LAMINAS-7B.md): la mecha que vuelve en M15 (A-35), las zonas de control y el margen del
break even (RN-009 y A-13), dónde pone el 0 de la caja (A-48), el rango de 4 horas después de una
ruptura (A-58), S-22 y S-19, más el bloque de días y, al final, la tarde del 10 de julio
(docs/sesion-7/PREGUNTAS-7B.md; la reentrada, A-53 y A-43, entre las que no caben). Las láminas de
la 7b las generó trabajo/laminas-sesion-7b, con el motor de la activación de la 7a.» Y en sus
Refs, `ID:A-58` (auditor, herencia 5); en «Depende de», «el vídeo de mapeo del trader, si llega
antes» ya no aplica: llegó el 2026-11-18 y no se ingiere.

**Technical Debt** (líneas que se proponen):
- «b1: con `detenido_por_tope` encendido por una regla, la lámina calla la otra causa de tope si
  también se cumple (la foto no la guarda); en las láminas de la 7b, 0 cortes con el hecho
  encendido (LAMINAS-7B.md F2).»
- «`motor laminas` da `LaminaError` y no escribe nada si RN-004 apaga `detenido_por_cartuchos` en
  el mismo cierre en que RN-016 o RN-001 dispararon por él (la foto no guarda los hechos del
  principio del evento); en las láminas de la 7a y de la 7b no pasó (LAMINAS-MOTIVOS.md, LAMINAS-7B.md F2).»

**`PROJECT_STATE.md`**: 24.109 bytes en la rama (tope 25.000); la rama solo cambió en él la rama y
la funcionalidad actuales.

## Desviaciones

1. **Las filas de las dos sesiones que entran no salen de `filas-por-sesion.txt`**, que no las
   tiene: salen del mismo guion sobre la misma fuente (`anexos/LAMINAS-7B/filas-por-sesion-7b.txt`).
   Y son, como todas las de §1, de la línea base, anterior a activar la 7a; el recuadro D4 pedía «la
   corrida nueva», que para enero y abril no existe commiteada (auditor, fila 24 y herencia 3).
2. **El orden de S-3 y S-4 no es el que el encargo escribió** (A-58 en S-3, A-48 en S-4): lo
   cambia la regla del propio encargo («de más a menos filas, las que no tienen recuento detrás»),
   y se dice.
3. **La fila de HOLDOUT de 0.2, escrita tarde para el conteo de `filas_por_sesion.py`** (que solo
   lee un anexo commiteado de construcción).
4. **El riesgo del contrato se queda en alto** aunque F2 no tocó el motor: lo fijó así el encargo al
   abrir.
5. **El orden de la entrega es el de la skill entregar-rama** (CI antes del revisor), no el del
   encargo (revisor, push y CI): el encargo dice que gana la skill. El revisor corrió a la vez que
   la CI, sobre el commit que la CI probaba.
6. **ADR-0095 se queda en el bloque `ids-inexistentes` del encargo**, aunque el encargo manda
   sacarlo en el último commit si no existe: el texto del encargo, copiado tal cual, lo nombra dos
   veces, y sin el bloque `knowledge validate` falla («id citado que no existe»,
   `docs/encargos/trabajo-laminas-sesion-7b.md:12` y `:45`, medido el 2026-11-19). Gana la medida.
   Precedente: el ADR de S-15 de `trabajo-activar-sesion-05-motor.md`, que sigue en su bloque.
7. **En S-2, pregunta 2, la opción (a) dice «por poco que sea»** (revisor, b1): la frase de la
   pregunta es la reformulada de ACTIVAR-SESION-07.md:656, tal cual, y dice «un punto por encima»;
   la opción sola («me basta con que cierre por encima») se podía leer como un margen de un punto.

## Por qué cambió cada cosa

| Qué | Por qué |
|---|---|
| Salen 2026-01-13 y 2026-01-07 (07-11) | abren con 44 y 20 H4 cargadas: su sesgo sale del rango que arranca en la primera H4 de enero, no del que vería el trader (F1.1; ACTIVAR-SESION-07.md F1.3) |
| Entran 2026-04-24 07-11 y 2026-04-27 11-15 | las únicas de «stop fuera» con «cumple» que no estaban en el bloque, no se usaron en la 7a y no están entre las sesiones de enero con menos de 60 H4; sirven a la caja (F1.2) |
| El 2026-04-15 se queda, con lo de la 7a dicho | el único caso de «el trader no opera y el bot sí», y en la 7a no vio ninguna lámina de ese día (F1.3) |
| Los pasos de cada sesión | lo aprendido en la 7a (F1.5; ERRORES-RECURRENTES.md y SESION-07-EXTRACCION.md §5.1, punto 8) |
| La reserva 07-16 ya no dice «es una pareja» | la frase ya no era cierta (ACTIVAR-SESION-07.md:505), y la que la sustituyó daba un pasaje más a una deducción sobre sus láminas (revisor, b4; «Lo que necesito que decidas», punto 5) |
| S-1, A-35 | la pregunta 1 de la 7a no tuvo respuesta; decide cada toma de M15 (toca el dinero) |
| S-2, zonas de control y margen del break even | «otra: A y B» sin decir qué distingue a C; el margen, cifrado una vez en un ejemplo; A-13 toca el dinero |
| S-3 = A-48 y S-4 = A-58 | la regla del encargo: de más a menos filas; A-48 es la única con recuento (0.3) |
| S-5 y S-6 = S-22 y S-19, sin recuento | decisión del consultor: su rama es el punto (2) y sin respuesta no se abre |
| La reentrada, A-53 y A-43 a §3 | el encargo; A-53 y A-43 sin recuento por fila, y la reentrada pierde ante las dos que tocan el dinero |
| `SESION_EN_CURSO = "08"` y la hoja 08 | la 7a ya está grabada; la hoja 08 tiene que casar con los títulos de PREGUNTAS-7B.md (el test lo exige) |
| La línea de la skill | ACTIVAR-SESION-07.md la dejó preparada: lo que la skill decía que no estaba escrito ya lo está |
| El motor, sin tocar | F2.2: (a) = 0 y (b) = 0 |

## El encargo, punto por punto

| # | Punto | Estado | Dónde |
|---|---|---|---|
| 1 | Abrir con abrir-rama; base y CI de `main` comprobadas | Hecho | «Base comprobada» |
| 2 | Contrato: R4, riesgo alto, artefacto, lista blanca, tag F39f libre | Hecho | `contrato.yaml` |
| 3 | Encargo en `docs/encargos/` con el ADR reservado en `ids-inexistentes` | Hecho de otra forma: el ADR no existe, pero se queda en el bloque, porque sin él `knowledge validate` falla | encargo; desviación 6 |
| 4 | 0.1 herencias | Hecho | 0.1 |
| 5 | 0.2 H4 cargadas y compuerta, con guion commiteado y fila de HOLDOUT | Hecho | 0.2; `anexos/LAMINAS-7B/` |
| 6 | 0.3 filas por pregunta | Hecho | 0.3 |
| 7 | F1.1-F1.5 | Hecho; CUADRA | F1 |
| 8 | F1.3b, una sesión sin láminas | Medido: ninguna | F2 |
| 9 | F2.1 láminas en v1, sola, orden barajado fuera del repo | Hecho | F2.1 |
| 10 | F2.2 (a) y (b), solo recuentos | Hecho: 0 y 0 | F2.2 |
| 11 | F2.3 arreglo si pasa; si no, Technical Debt propuesto | No pasa ninguno: dos líneas propuestas | F2.3; «Para la orden de cierre» |
| 12 | F2.4 recuentos por sesión en el terminal | Hecho | — (no en el repo) |
| 13 | F3 recuadro, seis técnicas ordenadas, preguntas nuevas, §3, hoja 08, test sustituido | Hecho | F3 |
| 14 | F4 la línea de la skill | Hecho | F4 |
| 15 | Informe con 0.2, porqué de cada cambio, F2, 0.3 y lo de la orden de cierre; tamaño de PS | Hecho | este informe; «Por qué cambió cada cosa» |
| 16 | Revisor con los cuatro alcances; push a `fix/` y CI | Hecho | «La CI de Linux», «Informe del revisor» |
| 17 | PARADA final | Hecho | abajo |

## PARADA final (no detiene la entrega; la rama no se cierra)

**Lo que no cuadró:** nada de F1 ni de F2. Lo que cambia respecto del encargo está en
«Desviaciones» (el orden S-3/S-4 y las filas de las dos que entran).

**La tabla de filas de F3**: 0.3. **§3 con más filas que S-5 o S-6**: la reentrada (B-11, 4 en
julio) y la del 2026-07-01 (B-15, 3) tienen más que S-22 y S-19, que no tienen recuento; también
B-7 (3) y B-8 (2), de antes. No se cambió ninguna.

## Lo que necesito que decidas

0. **§3 frente a S-5 y S-6.** Opciones: (a) dejar S-22 y S-19 entre las seis, como declaró el
   consultor (su rama es el punto (2) y sin su respuesta no se puede abrir); (b) meter la reentrada
   (B-11) en lugar de S-19. Recomiendo (a): la reentrada mueve 4 filas, pero S-22 y S-19 bloquean
   una rama entera. Coste de (b): esa rama espera a otra sesión.
1. **El orden S-3 = A-48, S-4 = A-58.** Opciones: (a) dejarlo como sale de la regla de filas; (b)
   volver al del encargo. Recomiendo (a): es la regla del encargo, y A-58 no tiene recuento por
   fila. Coste de (b): ninguno, salvo que la hoja 08 y los títulos cambian.
2. **B-15 (2026-07-01) lleva día.** Opciones: (a) dejarla en §3; (b) llevarla al bloque de días como
   una pregunta de Aleks tras la sesión 4. Recomiendo (a): no tiene esquema y la 7b ya va llena.
   Coste de (b): un día de julio más que comprobar por la compuerta.
3. **S-2, pregunta 1, primera parte, no discrimina** (revisor, b2): en el dibujo 1, A, B y C están
   en el retroceso después de la toma y antes de romper el punto, así que «del retroceso, después
   de tomar la liquidez» y «de antes de romper el punto» describen los mismos bajos. La duda de
   SESION-07-EXTRACCION.md §5.1, punto 4, enfrenta «antes de romper el punto» (la zona del esquema)
   con «después» (la del break even). Opciones: (a) que el dibujo 1 del PDF lleve también una zona
   formada después de romper el punto, rotulada, y la opción (b) diga «después de romper el
   punto»; (b) dejar la frase reformulada tal cual. Recomiendo (a): sin ella la respuesta no cambia
   nada. Coste de (a): retocar el esquema y una opción, que son tuyos (la frase no se tocó aquí).
4. **S-2 vuelve a preguntar algo RESUELTO** (revisor, b3): «Y si hay dos, ¿ese esquema te sirve o lo
   descartas?» lo cerró A-20 («solo 1 zona control bro. si hay 2 se descarta»), y ADR-0093 §1 dice
   que ninguna pregunta vuelve a preguntar lo decidido. Es tu reformulada (ACTIVAR-SESION-07.md:655)
   y el encargo la manda; «Para Aleks» lo dice. Opciones: (a) quitar esa segunda parte y su hueco
   en «Para confirmar al final»; (b) dejarla, declarándola como la excepción de ADR-0093 §1 por la
   contradicción de la 7a. Recomiendo (a): A-20 lo dijo por escrito y sin dudas. Coste de (b):
   abrir la puerta a reabrir A-20 con un registro `REOPEN`.
5. **La reserva 07-16 y la clave** (revisor, b4): juntando ACTIVAR-SESION-07.md:504-505 y :600-603
   (desde el 07-13 el bot no abre en julio, con el motor de F39e), `docs/runbooks/LAMINAS.md:50-53`
   (qué es una lámina de tipo a y una de tipo b) y la fila de 07-16 de §1 (trader 1, bot 0), se
   puede deducir cuántas láminas tiene la sesión de 2026-07-16 de 07 a 11 y de qué tipo, aunque no
   qué carpeta es. Quitar la frase de §1 no lo arregla: los otros pasajes ya están en `main`.
   Opciones: (a) aceptarlo: es una reserva, y la carpeta no se deduce; (b) cambiar esa reserva por
   otra sesión que cumpla (habría que volver a pasar la compuerta y regenerar las láminas). Recomiendo
   (a). Coste de (b): otra llamada de `motor laminas`, una fila de HOLDOUT y v2.

**Lo que no me convence:**
1. Las filas de §1 son de la línea base, anterior a activar la 7a; las láminas, del motor de
   después. «Sirve a» puede no casar con lo que enseñan.
   No hay corrida commiteada de enero ni de abril con el motor nuevo, y este encargo no la autoriza.
2. El 2026-04-15: el trader ya lo operó una vez. Aunque abra un replay sin marcas, puede acordarse
   de lo que hizo; es la única sesión de «el trader no opera y el bot sí», y eso es lo que la hace
   valer, pero su primera vez ya no es ciega.
3. S-2 lleva dos preguntas con dos partes la primera; es la más larga de la hoja (y lleva b2 y b3).
4. El «0 de 27 cortes» de la primera versión del informe (b5) y la frase «era una pareja… ya no»
   de §1 (b4) siguen en la historia del commit 7eef7094, que no se reescribe.

## La CI de Linux (`fix/laminas-sesion-7b`)

| Run | Commit | Resultado |
|---|---|---|
| 44463029525 | 7eef7094 (F2 a F4) | `failure` por un solo test, el aceptado: `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/laminas-sesion-7b'; la rama actual es 'fix/laminas-sesion-7b'»); «1 failed, 3448 passed, 93 skipped» |
| el del último commit | — | en el mensaje final a Aleks (se lanza después de este commit) |

## Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Fila de HOLDOUT del 2026-11-19 que declara, escrita tarde, lo leído el 18 (documentos, anexos, 20 ítems de evidencia, la búsqueda con conteo sobre las láminas); §0 de PREGUNTAS-7B.md la nombra |
| a2 | menor | «Exposiciones» al día: cuatro filas |
| a3 | menor | La línea de PLANTILLA se queda: es la convención con que nacen los informes (abrir-rama, paso 4), y dice que la fase 0 ya está |
| a4 | menor | `## Estado` al día |
| b1 | importa | La opción (a) de S-2, pregunta 2: «me basta con que cierre por encima, por poco que sea»; la frase de la pregunta, tal cual (desviación 7) |
| b2 | importa | A la PARADA, punto 3: el esquema y la frase son del consultor |
| b3 | importa | A la PARADA, punto 4: es la reformulada que manda el encargo |
| b4 | importa | Sale de §1 la frase de la pareja de 07-16; lo que queda (pasajes ya en `main`), a la PARADA, punto 5 |
| b5 | menor | Sale el total de láminas del informe («0 cortes», sin el total) |
| b6 | menor | «Por qué cambió cada cosa», bloque nuevo |
| no comprobado | — | El orden de `--sesiones`: lo comprobó la sesión, sin escribirlo. Ninguno de los órdenes en que el repo lista las siete sesiones (§1, los anexos, su README) es el de la llamada |

## Informe del revisor (subagente `revisor`, 2026-11-19, sobre 7eef7094), tal cual

> Dos retiradas, marcadas en su sitio. (1) Una frase de b4, que decía el recuento y el tipo de las
> láminas de una sesión que se deducen juntando pasajes: el encargo prohíbe que un fichero del repo
> diga cuántas láminas tiene una sesión («QUÉ NO CAMBIA»). (2) El total de láminas, en tres sitios
> (b5, su comparación con las filas de §1 y «Lo que no pude comprobar»), que el informe ya no da
> (b5). Ninguna cita de un tramo no citable. Todo lo demás, tal cual.

### Informe del revisor · trabajo/laminas-sesion-7b · 2026-11-19

Revisión sobre HEAD 7eef7094 (base b174d714). El árbol de trabajo está limpio y son tres commits. Ficheros (`git diff --name-status main...HEAD`): 16, de ellos 7 con `A` y 9 con `M`. `src/` y `knowledge/` no cambian. En `tests/` solo cambia `tests/unit/test_transcribir_sesion.py`.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | `PREGUNTAS-7B.md` dice que la lectura de los ítems de v18 y v19 y de los anexos de PREPARACION-SESION-7, RECORRIDA-CONSTRUCCION-2 y ACTIVAR-SESION-07 está declarada en las «Filas del 2026-11-18 de esa rama». Ninguna de las tres filas que añade la rama lo dice. La de la apertura dice lo contrario: «Lo que lee la apertura: documentos del repo (el encargo, las skills, el contrato y `PROJECT_STATE.md`). **Nada más**». La de 0.2 solo nombra los dos guiones y `filas_por_sesion.py`, y la de F2 solo `motor laminas`. La afirmación no la sostiene lo que cita. | `C:\Users\USER\Desktop\Bot v3\docs\sesion-7\PREGUNTAS-7B.md:56-60`; `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md` (las tres líneas `+` del 2026-11-18) |
| a2 | menor | «Exposiciones» del informe habla de «Dos filas del 2026-11-18». Ya son tres, porque falta la de F2. Tampoco dice que se leyeron ítems de evidencia. | `C:\Users\USER\Desktop\Bot v3\docs\validation\LAMINAS-7B.md:111-116` |
| a3 | menor | Queda la línea de plantilla «PLANTILLA hasta la fase 0 (la línea con que nació)…». | `LAMINAS-7B.md:3` |
| a4 | menor | El Estado está desfasado. Dice «faltan `make check`, CI de Linux y revisor», pero el `make check` ya está sellado sobre HEAD y la CI ya corrió (run 44463029525, abajo). | `LAMINAS-7B.md:298`; `make-check.log` (SELLO) |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da: «CONTRATO: 16 ficheros dentro del contrato de trabajo/laminas-sesion-7b (riesgo alto, artefacto docs/validation/LAMINAS-7B.md, tramo 'R4', 3 comprobaciones para el revisor)», con exit 0.
- **`make check`**, no ejecutado; su evidencia es `make-check.log`:
  - «SELLO: make check en verde sobre el arbol 2e342e5a66bb09b3a8f59c2a4b87f76b43fe19ec», que es `git rev-parse HEAD^{tree}`.
  - «3536 passed, 6 xfailed». La única coincidencia de `failed` es ese «xfailed».
  - «PICO DE MEMORIA de make check: 319 MiB en `test`».
  - `knowledge validate` dentro del log: «OK: 710 items de evidencia, 0 contradicciones abiertas, historial intacto». No lo relancé aparte.
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases` (`git log main..HEAD -- knowledge/ data/manifests/` sale vacío).
- **Holdout.** Nada toca `knowledge/cases/holdout`.
- **Fechas.** Todas las que añade algún commit de la rama (`git log -p main..HEAD`, sin HISTORIA) caen en los tramos de construcción. Son 01-02…01-30, 04-01…04-29, 07-01…07-17 y 08-03/08-31, más fechas del proyecto. La compuerta da 0 días dev en `casos_reservados` y 0 en `casos_ocultos` (`compuerta-7b.txt:2-3`).
- **Regímenes de cambio.** No hay nada en `evidence/`, `feedback/`, `manifests/`, transcripciones, fotogramas ni `libros.yaml`.
  - `HISTORIA.md`: 178 líneas añadidas y 0 quitadas. Es el «# Archivo 74» de `main` en b174d714.
  - `HOLDOUT-EXPOSICIONES.md`: 3 líneas añadidas y 0 quitadas.
- **Ambigüedades, ADR y citas.** Ninguna ambigüedad cambia y no hay ADR nuevo ni cambiado. Ningún informe cerrado de `docs/validation/` se edita. No hay ningún sitio con `cita` nuevo.
- **`PROJECT_STATE.md`**: 24.109 bytes (`wc -c`), como dice el informe.
- **Citas del informe comprobadas contra su fuente:**
  - `laminas.py:506-511` es `FRASE_TOPE_POR_REGLA`, y el `LaminaError` está en :888-891.
  - `LAMINAS-MOTIVOS.md:537` sí dice que la foto no sabe si la otra causa se cumple.
  - `ACTIVAR-SESION-07.md:706-709` coincide letra a letra con la línea nueva de `SKILL.md`.
  - `runbooks/LAMINAS.md:34` sí dice «se lanza sola».
  - `caja-stop.txt`: 44 filas con «| stop fuera |», 16 de julio.
  - `sustitutas.txt:28`: «P2 4-10: 24 filas».
  - TRAZAS-ABLACION §5.2: 8 filas de julio con gate RN-009 (3+1+4).
- **Tests de la hoja.** `uv run pytest -q -p no:cacheprovider tests/unit/test_transcribir_sesion.py tests/unit/test_hoja_preguntas.py` sale todo en verde. `test_la_sesion_en_curso_es_la_08` PASSED y `test_la_hoja_08_es_la_de_preguntas_7b` PASSED.
- **CI.** `origin/fix/laminas-sesion-7b` = 7eef7094. El run 44463029525 sale `failure` por un solo test, `test_state_check_ok_on_real_repo`, con «PROJECT_STATE declara la rama 'trabajo/laminas-sesion-7b'; la rama actual es 'fix/laminas-sesion-7b'», que es el fallo aceptado. El resto: 3448 passed.

#### Eje (b) · Encargo
Resumen: 0 bloquea, 4 importa, 2 menor. Requisitos: 30 hechos (uno «de otra forma», declarado), 4 parciales, 0 no hechos, 3 pendientes o no verificables.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con abrir-rama: base y CI de `main` | Hecho | `LAMINAS-7B.md:13-18` |
| 2 | Contrato: R4, riesgo alto, artefacto, lista blanca | Hecho | `contrato.yaml:1-23`; `contrato_rama.py` OK |
| 3 | Tag F39f libre | Hecho | `git tag -l "stable/F39f*"` vacío |
| 4 | Encargo con ADR-0095 en `ids-inexistentes`, que sale en el último commit si no existe | Parcial (pendiente del último commit) | `docs/encargos/trabajo-laminas-sesion-7b.md:8-10` lo sigue llevando; `ls docs/adr` no tiene 0095 |
| 5 | 0.1 herencias | Hecho | `LAMINAS-7B.md:25-35` |
| 6 | 0.2 H4 y compuerta, con guion commiteado y fila de HOLDOUT | Hecho | `anexos/LAMINAS-7B/h4-cargadas.txt:2-8` (todas ≥ 60); `compuerta-7b.txt:12-22` (7 PASA); `compuerta_7b.py` solo cambia `CANDIDATAS` y el docstring frente a `dias_d3.py` (`git diff --no-index`) |
| 7 | 0.3 filas por pregunta | Hecho | `LAMINAS-7B.md:57-72` (TRAZAS-ABLACION, declarado como fuente fuera de los tres anexos) |
| 8 | F1.1 salen 01-13 y 01-07 | Hecho | `PREGUNTAS-7B.md:11-13`; tabla :70-78 |
| 9 | F1.2 entran 04-24 (sesión 1) y 04-27 (sesión 3); «Sirve a» y filas | Hecho de otra forma (filas de `filas-por-sesion-7b.txt`), declarado | Desviación 1, `LAMINAS-7B.md:229-232`; `sustitutas.txt:25-26` |
| 10 | Reservas sin cambio | Hecho | `PREGUNTAS-7B.md:76-78` |
| 11 | F1.3: 04-15 se queda como sesión 2, paso subrayado, pie corregido | Hecho | `PREGUNTAS-7B.md:87-98` |
| 12 | F1.3b | Hecho | `LAMINAS-7B.md:152` |
| 13 | F1.4: 07-03 no se usa | Hecho | no está en §1 |
| 14 | F1.5: los pasos | Hecho | `PREGUNTAS-7B.md:92-108` |
| 15 | F2.1 láminas en v1, orden barajado fuera del repo, fila de HOLDOUT | Hecho (la salida no es verificable desde el repo) | fila F2 de HOLDOUT; `LAMINAS-7B.md:138-143` |
| 16 | F2.2 (a) y (b) en recuentos | Hecho | `LAMINAS-7B.md:147-150` |
| 17 | F2.3: no pasa ninguno, motor sin tocar, dos líneas de Technical Debt | Hecho | `git diff main...HEAD --stat -- src/` vacío; `LAMINAS-7B.md:216-222` |
| 18 | F2.4 en el terminal | No verificable | fuera del repo |
| 19 | F3 recuadro fechado | Hecho | `PREGUNTAS-7B.md:8-25` |
| 20 | Orden: dinero primero, después filas (S-3 = A-48, S-4 = A-58 por la regla del encargo) | Hecho, dicho | `PREGUNTAS-7B.md:112-114`; `LAMINAS-7B.md:74-77` |
| 21 | S-1 con la reformulada | Hecho (igual que `ACTIVAR-SESION-07.md:654`) | `PREGUNTAS-7B.md:130-132` |
| 22 | S-2 con dos preguntas | Hecho (ver b1-b3) | `PREGUNTAS-7B.md:152-206` |
| 23 | A-58 y la línea nueva de «Para precisar» | Hecho | `PREGUNTAS-7B.md:263` |
| 24 | A-48, S-22, S-19 y S-7 «como está» | Hecho: solo cambian los títulos (hunks `-69 +208`, `-126 +303`) | `git diff -U0 main...HEAD -- docs/sesion-7/PREGUNTAS-7B.md` |
| 25 | Las partes y «Para Aleks» con destino | Hecho | S-1, S-2, S-4 |
| 26 | §3: reentrada, A-53, A-43, breaker por mecha, 07-01; sin `**S-n.**` | Hecho | `PREGUNTAS-7B.md:364-368` |
| 27 | PARADA si una de §3 tiene más filas que S-5 o S-6 | Hecho | `LAMINAS-7B.md:270-272` |
| 28 | Hoja 08, `SESION_EN_CURSO`, test sustituido | Hecho | `scripts/transcribir_sesion.py` diff; pytest arriba |
| 29 | F4: la línea de la skill | Hecho (una línea, tal cual) | `.claude/skills/activar-sesion/SKILL.md` diff |
| 30 | Informe: 0.2, «bloque final con el porqué de cada cambio», F2, 0.3, F nueva, R4.3, tamaño de PS | Parcial: no hay un bloque final de porqués; están repartidos por F1, F3 y Desviaciones | `LAMINAS-7B.md:118-241` |
| 31 | Revisor con los cuatro alcances, pegado | Pendiente (es este informe) | — |
| 32 | Push a `fix/` y número del run | Parcial: hecho, falta escribirlo | run 44463029525; no aparece en el informe |
| 33 | PARADA final | Hecho | `LAMINAS-7B.md:265-294` |
| 34 | QUÉ NO CAMBIA: ni spec ni motor | Hecho | diff sin `knowledge/` ni `src/` |
| 35 | Ninguna fecha reservada | Hecho | eje (a) |
| 36 | Ningún fichero describe una lámina ni deja deducir la clave | Parcial (b4) | abajo |
| 37 | «Rama lista para revisión, NO cerrada» | Pendiente | Estado «EN CURSO» |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Alcance 3, sugiere o confunde.** S-2, pregunta 2, pregunta «¿te basta con que cierre **un punto** por encima, o tiene que pasarlo por un margen?», pero la opción (a) es «me basta con que cierre por encima». «Un punto por encima» se puede leer como un margen de 1 punto. Además «Lo que nos has dicho» trae «mínimo al menos por un par de puntos o un pip». Un «(a)» podría significar «margen 1» y «Para Aleks» lo lleva a «A-13 se cierra sin margen». La frase viene tal cual de ACTIVAR:656, pero en la hoja choca con sus propias opciones. | `PREGUNTAS-7B.md:179-184`, `:163`, `:201-202`; `ACTIVAR-SESION-07.md:656` |
| b2 | importa | **Alcance 3, la pregunta no discrimina.** S-2, pregunta 1, primera parte. El dibujo 1 pone A, B y C en el retroceso de M1 después de la toma, con el punto de breaker arriba, es decir, antes de romperlo. Por eso (a) «del retroceso, después de tomar la liquidez» y (b) «de antes de romper el punto» describen los mismos bajos. Y «Para Aleks» lleva (a) a «lo de hoy» («los pivotes de M1 … entre la toma y el breaker», que también son de antes de romper el punto) y (b) a «cambia la definición». La duda de §5.1, punto 4, que el encargo manda llevar, enfrenta «antes de romper el punto» (esquema) con «después» (la zona del break even), y la pregunta no ofrece «después». | `PREGUNTAS-7B.md:168-178`, `:192-197`; `SESION-07-EXTRACCION.md:719-722`; encargo:55 |
| b3 | importa | **Vuelve a preguntar algo RESUELTO sin declararlo.** «Y si hay dos, ¿ese esquema te sirve o lo descartas?» y «si hay dos, el esquema ______» preguntan lo que cerró A-20, RESUELTA: «solo 1 zona control bro. si hay 2 se descarta». ADR-0093 §1 dice: «Ninguna vuelve a preguntar lo que ya está decidido». «Para Aleks» lo sabe («va contra A-20, RESUELTA»), pero el informe no lo declara ni lo lleva a «Lo que necesito que decidas». No lo marco como bloquea porque es el texto reformulado que ordena el encargo (F3, S-2, «la 1»); lo tiene que decidir el consultor. Es la lección (4) de la fila de `trabajo/preparacion-sesion-7`. | `PREGUNTAS-7B.md:174-178`, `:186-187`, `:197-199`; `knowledge/spec/ambiguedades.yaml:436-450`; `ADR-0093:30-31` |
| b4 | importa | **Alcance 1, deducción juntando pasajes.** La frase nueva de §1 sobre la reserva 07-16 («era una pareja en la línea base y, tras activar la 7a, ya no: RN-032») se puede juntar con cuatro pasajes. ACTIVAR:504-505 dice que desde el 07-15 el bot no abre. ACTIVAR:600-603, con F2, adelanta el freno al 07-13. LAMINAS.md:50-53 dice que una lámina de tipo a es una orden del bot llenada y una de tipo b una operación del trader sin pareja. Y `filas-por-sesion-7b.txt:7` da «trader 1, bot 0». [frase retirada: el recuento y el tipo de las láminas de esa sesión que se deducen] Eso es «cuántas tiene una sesión y de qué tipo» (encargo:26). Es una inferencia: solo vale si `motor laminas` repite la cuenta del mes de F2.4, y no lo pude comprobar sin abrir las láminas. No nombra ninguna carpeta. | `PREGUNTAS-7B.md:78`; `ACTIVAR-SESION-07.md:504-505`, `:600-603`; `docs/runbooks/LAMINAS.md:50-53`; `anexos/LAMINAS-7B/filas-por-sesion-7b.txt:7` |
| b5 | menor | El informe escribe el total de láminas (un total de cortes). No es por sesión y, solo, no deja casar carpetas: las filas de §1 suman 23, no ese total. Pero F2.4 manda los recuentos al terminal. | `LAMINAS-7B.md:150` |
| b6 | menor | El «bloque final con el porqué de cada cambio» que pide el encargo no existe como bloque; los porqués están repartidos. | encargo:70; `LAMINAS-7B.md:118-241` |

**Los cuatro alcances**
- **(1) Láminas y clave.** No hay ninguna tabla por carpeta, ningún nombre `sesion-NN` asociado a un día, ninguna descripción de una lámina concreta ni recuentos por sesión. Lo busqué en `git log -p main..HEAD`, todos los commits, con «sesion-0», «carpeta», «clave», «tipo a/b» y «cortes». El README de anexos (:3-5) lo dice expresamente. Quedan b4 (deducción condicional para 07-16) y b5 (el total).
  - La columna «trader / bot» de §1 y «el trader no opera y el bot sí» del 04-15 dejan ver la composición por tipo de cada sesión, pero las ordena el encargo (F1.2, F1.3) y lo acepta ADR-0093 §2.3. Para casar carpetas hacen falta las carpetas, que solo tienen quienes guardan la clave.
- **(2) Días del bloque.** Las siete pasan a), b) y c) de ADR-0093 §3: `compuerta-7b.txt:12-22`, sobre 76 días dev, 0 ocultos y 0 reservados. Todas tienen ≥ 60 H4: `h4-cargadas.txt:2-8` da 236, 195, 243, 69, 80, 87 y 200.
  - Las cinco que ya medía `arranque.py` dan lo mismo que en `ACTIVAR-SESION-07.md:451-453` (195, 69, 80, 87, 200). Eso respalda que restringir `dias` a los del bloque en `h4_cargadas.py` no cambia el recuento.
  - No volví a correr nada.
- **(3) Preguntas nuevas.** Los 17 ítems leídos existen en `knowledge/evidence/v18|v19/`. Los 17 los cita `ACTIVAR-SESION-07.md` (Grep: :46-54, :616-647).
  - Ninguno tiene t0 ni t1 dentro de un tramo de `tramos_no_citables.yaml:536-661`. Los más cercanos: v18 0:25:11-0:25:16, antes del tramo 0:25:18; v18 0:27:01, después de 0:26:56; v18 0:13:27-0:13:45, antes de 0:14:20; v18 0:19:00, después de 0:18:48; v19 1:11:38, después de 1:08:49.
  - Las 17 citas entre comillas de `PREGUNTAS-7B.md` son subcadenas literales de su `cita_literal`.
  - `ev-v19-011640-1fdc33a7` (solo en «Para Aleks», citado por SESION-07-EXTRACCION) existe y está fuera de tramos (1:16:40). No lo leí.
  - S-1 y S-4 no sugieren la respuesta. S-2 tiene b1, b2 y b3.
- **(4) Arreglo de motor.** No hubo. `git diff main...HEAD --stat -- src/ knowledge/` sale vacío y ADR-0095 no existe. Julio no cambia porque no se tocó código del motor.

#### Lo que no pude comprobar
- **El orden barajado de `--sesiones`.** El repo trae las siete sesiones en un orden distinto del de §1: 04-24, 04-27, 04-15, 01-19, 01-21, 01-22, 07-16 (`anexos/LAMINAS-7B/README.md:18` y `filas-por-sesion-7b.txt:1-7`). Si la llamada de `motor laminas` usó ese mismo orden, la carpeta `sesion-NN` de cada día se deduciría del repo. Lo tiene que confirmar Aleks contra `clave.txt`, sin escribirlo. No abrí ni las láminas ni la clave.
- La salida de F2 (v1), los recuentos de F2.4 en el terminal y el total de cortes de la búsqueda sobre los HTML: están fuera del repo, y por encargo no los abro.
- Qué ítems de evidencia leyó la sesión de verdad (el encargo limita la lectura); solo puedo ver lo que se cita.
- Si la fila de HOLDOUT de la apertura se escribió antes del primer `make check`, como dice.
- `knowledge validate` aparte: lo sustituye su línea OK en `make-check.log`. No ejecuté `make check`, ni `git write-tree`, ni ninguna corrida del motor.

#### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `git diff --name-status main...HEAD && ls make-check.log && tail -5 make-check.log`
4. `git rev-parse HEAD^{tree} HEAD~1^{tree}`; `grep -n "failed" make-check.log`
5. `git diff main...HEAD -- docs/sesion-7/PREGUNTAS-7B.md`
6. Read de encargo, `contrato.yaml`, `LAMINAS-7B.md`, `PREGUNTAS-7B.md`, ERRORES-RECURRENTES (líneas 118 y 124), `runbooks/LAMINAS.md`, `ACTIVAR-SESION-07.md:440-719`, `SESION-07-EXTRACCION.md:699-738`, `parametros.yaml:475-624`, `LAMINAS-MOTIVOS.md:466-481, 530-539`, `laminas.py:500-514, 870-904`, ADR-0093:17-131, los cuatro ficheros de `anexos/LAMINAS-7B/` y `sustitutas.txt`
7. `git log -p main..HEAD | grep -n -i -E "^\+.*(sesion-0…|carpeta|clave|…)"`
8. `git diff main...HEAD -- HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md SKILL.md transcribir_sesion.py test_transcribir_sesion.py`
9. Grep de los ids en `ACTIVAR-SESION-07.md`; `ls knowledge/evidence/v18 | grep …`; `ls knowledge/evidence/v19 | grep …`; Read de los 17 ítems
10. `grep -n -A6 "video(_id)?: ?v1[89]" knowledge/corpus/tramos_no_citables.yaml`; Read de :613-662
11. `git diff --no-index` de `dias_d3.py` contra `compuerta_7b.py` y de `arranque.py` contra `h4_cargadas.py`
12. `git log -p main..HEAD -- . ':(exclude)docs/state/HISTORIA.md' | grep "^+" | grep -o -E "20(25|26)-..-.." | sort | uniq -c`
13. `git diff main...HEAD --numstat -- HISTORIA.md HOLDOUT…`; `wc -c PROJECT_STATE.md`; `git log main..HEAD -- knowledge/ data/manifests/`
14. `grep` de `FRASE_TOPE_POR_REGLA` en `src/botsito`; `grep -c "| stop fuera |" caja-stop.txt`; `grep -n "P2 4-10" sustitutas.txt`; `grep` de los encabezados de TRAZAS-ABLACION y su §5.2
15. `grep -n -A14 "id: A-20$" knowledge/spec/ambiguedades.yaml`
16. `git diff main...HEAD -U0 -- PREGUNTAS-7B.md | grep "^@@"`; `git show main:docs/sesion-7/PREGUNTAS-7B.md | grep -n "^\*\*S-"`
17. `uv run pytest -q -p no:cacheprovider tests/unit/test_transcribir_sesion.py tests/unit/test_hoja_preguntas.py`, y la misma con `-k "sesion_en_curso or hoja_08" -rA`
18. `git for-each-ref refs/remotes/origin/fix refs/heads/fix`; `git rev-parse refs/remotes/origin/fix/laminas-sesion-7b HEAD`; `git log --format='%h %ad' main..HEAD`
19. `gh run list --branch fix/laminas-sesion-7b --limit 3 --json …`; `gh run view 44463029525 --log-failed | grep …`
20. `git tag -l "stable/F39f*"`; `git diff main...HEAD --stat -- src/ knowledge/ tests/`

La guardia me negó dos comandos, que reescribí sin rodearla: `sed … | fold`, que pasó a Read con offset, y un bucle `for` con `$id`, que pasó a `ls | grep` literal. `git branch -a` lo negó `solo_lectura.py`, y lo sustituí por `git for-each-ref`.

## Estado

Fase 0 y F1 a F4 hechas. F1 CUADRA. F2: (a) = 0 y (b) = 0, el motor no se toca y no hay
ADR-0095 (dos líneas de Technical Debt propuestas para el cierre). F3 y F4 hechas. Revisor: eje (a)
0 / 1 / 3 y eje (b) 0 / 4 / 2; hechos o llevados a la PARADA. Cinco decisiones para el consultor en
«Lo que necesito que decidas».

Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA final (2026-11-19), tal cual

> Modelo: Opus · Esfuerzo: medio
>
> Respuesta del consultor a la PARADA final de trabajo/laminas-sesion-7b (2026-11-19). Cópiala al final del informe, con la fecha, en un commit propio.
>
> 0. (a) S-22 y S-19 se quedan entre las seis. Porqué: sin su respuesta no se abre la rama del punto (2), y eso pesa más que las 4 filas de la reentrada.
> 1. (a) S-3 = A-48 y S-4 = A-58, como sale de la regla de filas.
> 2. (a) B-15 (2026-07-01) se queda en §3.
> 3. (a) En S-2, pregunta 1, la primera parte pasa a ser: «En el dibujo 1, A y B te valen como zonas de control y C no. ¿Se forman antes de romper el punto, o pueden formarse también después de romperlo?», con las opciones «(a) antes de romper el punto; (b) también después de romperlo; (c) otra, ¿cuál?». En «Esquema inventado» del dibujo 1 añade: «y, a la derecha del punto ya roto, un cuarto bajo rotulado D, formado después de la ruptura». La línea «Para Aleks» se ajusta: (a) → lo de hoy; (b) → cambia la definición de zonas_desarrolladas_superan, con ADR.
> 4. (a) Quita de S-2 «Y si hay dos, ¿ese esquema te sirve o lo descartas?», su línea de opciones «y con dos: …», su hueco en «Para confirmar al final» («si hay dos, el esquema ______») y lo de «si con dos zonas de control el esquema te sirve» de «Lo que todavía no sabemos». En «Para Aleks», una frase: A-20 está RESUELTA (una sola zona; con dos se descarta) y no se vuelve a preguntar (ADR-0093 §1); si el trader lo contradice por su cuenta, va a la extracción como contradicción con lo fijado.
> 5. (a) Se acepta: es una reserva y la carpeta no se deduce. Ningún texto nuevo añade pasajes a esa deducción.
> Sobre lo que no te convence: el punto 1 (filas de antes de activar la 7a) queda dicho en el informe y no se corre nada; el punto 2 (el 2026-04-15 ya no es ciego) se acepta, porque es la única sesión de su tipo; el 3 se arregla con 3 y 4; el 4, como está.
>
> Después: knowledge validate, make check, push a fix/laminas-sesion-7b y CI de Linux con su run. Las láminas no se regeneran (estos cambios no las tocan). Un informe corto con el sha del último commit, el número de commits y el run. No cierres.
