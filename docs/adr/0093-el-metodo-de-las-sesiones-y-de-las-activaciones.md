---
status: ACTIVE
date: 2026-11-11
phase: post-F14 (rama `trabajo/preparacion-sesion-7`, R4.3 y R0.3 de la hoja de ruta)
---

# 0093 · El método de las sesiones y de las activaciones

> Decisión del consultor del 2026-11-11 (encargo de `trabajo/preparacion-sesion-7`, F1 y D1-D6, y
> su respuesta a la PARADA de la fase 0, `docs/validation/PREPARACION-SESION-7.md`). Recoge
> `docs/plan/RUMBO-2026-11.md` §1 a) a e) (decisión de Aleks y del consultor del 2026-11-08) y el
> pivote de su §4 (enmienda del 2026-11-10; esquema aceptado por Aleks el 2026-11-09, números del
> consultor aprobados por Aleks el 2026-11-11). RUMBO no se toca: este ADR lo cita. **Cambia la
> regla 2 de `docs/runbooks/SESION-DE-PREGUNTAS.md`**, su cabecera y los pasos 5 y 6 de «Antes», y
> «Lo primero» de `docs/runbooks/LAMINAS.md`, con recuadros «Por qué cambió» en el mismo commit.

## Decision

### 1. Las preguntas

Las preguntas de una sesión con el trader salen de **diferencias medidas** entre el bot y el
trader (la clasificación de la corrida vigente), y cada una lleva **las filas que puede mover**,
con su fuente commiteada. **Como mucho seis técnicas por día de sesión**, y primero las que más
filas mueven y las que tocan el dinero (A-35, A-13) (RUMBO §1 a). Un día de sesión es una sesión
con su id: la 7a es `<AAAA-MM-DD>-sesion-07` y la 7b `<AAAA-MM-DD>-sesion-08` (encargo, D2).

Son **cerradas**, con opciones y «otra, ¿cuál?» en todas; **sin días ni fechas**; y con **esquemas
inventados rotulados como tales**, con el marco escrito dentro del dibujo. Es lo de las sesiones 4
a 6 (`docs/sesion-6/PREGUNTAS.md:32-42`; el recuadro del 2026-10-28 de SESION-DE-PREGUNTAS.md,
paso 2 de «Durante»). **Ninguna vuelve a preguntar lo que ya está decidido**: una pregunta «en
parte» lleva lo que ya dijo y pregunta solo lo que falta.

### 2. El bloque de días

Primero el **bloque técnico**, en abstracto. Después, por cada sesión del bloque (RUMBO §1 b):

1. **Aleks comprueba antes el día** con la línea de SESION-DE-PREGUNTAS.md, «Antes», paso 1 (tiene
   que salir `False`), y se lo dice al trader. **El trader abre él mismo el replay de ese día en FX
   Replay, ANTES de compartir pantalla**, en una sesión de replay nueva, sin marcas, sin backtests
   guardados y sin Analytics a la vista. Esto **sustituye la salvaguarda «el gráfico lo prepara
   Aleks, no el trader»** del recuadro del 2026-09-28 de la regla 2: el riesgo que cubría -que un
   gráfico traiga un día reservado sin que se sepa- lo cubren ahora la comprobación del día y que
   el replay se abre limpio y fuera de pantalla.
2. **El trader marca y opera la sesión** con pantalla y audio, diciendo qué ve y qué descarta. La
   fecha la ve porque la carga él: es un día de construcción.
3. **Después ve las láminas del bot de esa sesión** (`motor laminas`), que prepara Aleks:
   recortadas al instante de decidir, con la caja, la orden, el stop y el objetivo, sin fecha y sin
   nada posterior al corte, con la sustentación en su idioma (RUMBO §1 b: sesgo de H4, liquidez de
   M15, caja, 0 y 0,8; nunca ids de reglas). Una lámina de tipo a solo existe si la orden se llenó
   (`docs/runbooks/LAMINAS.md`, «Qué sale»): eso lo deja ver el conjunto, y se acepta porque es un
   día de construcción que el trader acaba de operar. **Ningún resultado se enseña.**
4. **Corrige**, y se le pregunta «¿siempre, solo en este caso, o de qué depende?».
5. **Si en pantalla aparece otro backtest, Analytics o material de un mes reservado**, se
   reconduce, el tramo se declara no citable el mismo día (SESION-DE-PREGUNTAS.md, «Después», paso
   4) y, **en la ingesta, ningún fotograma se abre antes de que la voz o un fotograma ya abierto
   sitúen el tramo en el día de construcción** (lección de `trabajo/video-julio`: el arranque de
   v13 enseñó otro backtest; ERRORES-RECURRENTES.md, su fila).

Enseñar un día de construcción no es abrir ni exponer un día reservado (ADR-0021 §1, por
exclusión: abrir es leer etiquetas o el detalle de un día reservado; y CLAUDE.md, «Que se puede
mirar», punto 2: las velas no son holdout), como ya decían los dos recuadros de la regla 2.

### 3. Los días

Solo sesiones que cumplan, **escritas por su condición y no por sus casos** (encargo, D3; la regla
del 2026-10-27, `RECORRIDA-CONSTRUCCION.md:1628`, y RUMBO §1 b los escribían por sus casos, «nunca el
1 de abril ni el 1 de julio», y dejaron pasar el 2 de enero):

- **a)** el día es dev de un mes de construcción según `cobertura_material` de
  `knowledge/cases/kit/config.yaml` (hoy enero del 2 al 30, abril del 1 al 29, julio del 1 al 17 y
  agosto del 3 al 31), comprobado con `casos_reservados` y `casos_ocultos`. El 30 de abril queda
  fuera;
- **b)** el día de mercado anterior no es reservado ni está fuera de construcción (hoy excluye el
  primer día de cada tramo: 2026-01-02, 2026-04-01, 2026-07-01 y 2026-08-03, calculados con la
  condición, `PREPARACION-SESION-7.md` §0.4). Lo que viene de más atrás no excluye el día: la lámina
  no lo dibuja y dice que viene de antes de la ventana, y en FX Replay son velas;
- **c)** ninguna hora perdida dentro de la sesión (`docs/validation/anexos/RESPALDO-M1/horas_perdidas.py`)
  ni ninguna fila «posible M» de la sesión.

Cada día se comprueba por la compuerta y se declara en `docs/validation/HOLDOUT-EXPOSICIONES.md`
el mismo día. Una exclusión dice a qué conjunto se aplica (respuesta a la PARADA, punto 17).

### 4. De la respuesta a la regla

**Cada respuesta se escribe primero como test sobre casos de construcción que rompe en `main`**
(RUMBO §1 c). **Cada activación declara ANTES qué filas de la clasificación vigente debería
convertir en pareja**, y corre **julio de 2026** (el único mes de construcción con vídeo,
provisional: `provisionales_con_video` de `criterio_fidelidad.yaml`, y el del pivote) en la rama,
con su delta de parejas y de operaciones de más frente a la línea base (RUMBO §1 d: «un mes de
construcción»; el mes fijo hace comparables los deltas).

- **La cifra dice si la respuesta se entendió, nunca ajusta un parámetro** (ADR-0092 §6). Si el
  delta de julio de una activación **no casa con lo que declaró**, la regla no se retoca hasta que
  la cifra salga: **PARADA**, y el consultor vuelve a la voz del trader y decide si la respuesta se
  entendió mal. **El delta nunca elige entre dos lecturas de un parámetro.**
- **El delta de cada activación es diagnóstico** (ADR-0092 §6): la única lectura de julio que
  decide algo es la del pivote (§6).

Esto fija lo que la NOTA de ADR-0092 §6 (2026-11-09) dejó al ADR del método («Cómo se convierte una
respuesta del trader en regla»). ADR-0092 no se toca.

### 5. Las clases

Las de la clasificación de las filas: **error nuestro, regla desconocida, efecto de la cuenta,
material incompleto** (p. ej., libros sin vídeo, S-14 de la sesión 5) **y sin clase**. **La
precisión se lee de verdad solo sobre meses con vídeo** (RUMBO §1 e).

### 6. El pivote

Pre-registrado antes de activar nada (RUMBO §4, enmienda del 2026-11-10). Las cifras, literales,
viven en `docs/plan/PIVOTES-SESION-7.yaml`, que fija `tests/unit/test_pivotes_sesion_7.py` por su
sha256: cambiar una cifra exige cambiar el test a la vista en el mismo commit.

- **Qué se mide:** la primera corrida de ADR-0070 §3 (con una cuenta por mes, ADR-0092 §8, y el
  `criterio_fidelidad.yaml` vigente) después de activar la 7b, incluida la rama de S-22 y S-19.
  Solo julio de 2026, el único mes con vídeo.
- **Línea base:** RECORRIDA-CONSTRUCCION-2.md §1.1 y §4, sobre
  `anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt`. **Parejas de julio** (T0, el
  criterio de ADR-0043): **14**. **Operaciones de más de julio** (operaciones del bot, llenadas,
  sin pareja en un día con operaciones del trader: P5 más P6 en sesión; TRAZAS-ABLACION.md:730-731):
  **39** (P5 37, P6 2). No es la columna «Operaciones de más» del Marcador de la hoja de ruta, que
  cuenta las órdenes del bot en un (día, sesión, dirección) sin operación del trader (425 en total).
- **Mínimo 1:** parejas de julio ≥ 19. **Mínimo 2:** operaciones de más de julio ≤ 33.
- **Salidas:** se cumplen los dos, se sigue; se cumple uno, una sesión más con el trader con el
  mismo método, y tras su activación se vuelve a leer con estos mismos números; no se cumple
  ninguno, se pivota: el objetivo pasa a un bot de alta precisión sobre los setups que sí
  reproducimos (RUMBO §4), y la puerta para operar en vivo sigue siendo ADR-0092.
- **Contingencia, escrita ahora:** si en esa corrida la cuenta de julio acaba SUSPENDIDA o deja de
  llenar por un freno de la cuenta antes del 17, el pivote se lee sobre la corrida diaria de
  contexto, y el informe lo dice.
- **Por qué esos números**, con la cuenta medida en la fase 0 (`PREPARACION-SESION-7.md` §0.3,
  `anexos/PREPARACION-SESION-7/pivote-julio.txt`): las preguntas de la 7a y la 7b pueden mover en
  julio **29 filas del trader**: las 30 del rango de H4 de VIDEO-JULIO.md §4.1 y §4.2 (`:657`) sin
  sus 10 P5, que son del bot (20), más las 8 con el gate RN-009 de TRAZAS-ABLACION.md 5.2 y la P2 de
  2026-07-03 07-11. De las 20 del rango, 2 son del 1 de julio (las P1 de 2026-07-01 07-11), que no
  va a la sesión como día: la pregunta es abstracta y las mueve igual; y de las 8 del gate, 4 son de
  2026-07-14 11-15, que tampoco va (hora perdida). En julio, de las **46 operaciones del trader con
  una operación del bot del mismo lado en su sesión** (T0 + P2 + P3 + P7 = 14 + 14 + 15 + 3), **14
  son pareja, un 30 %** (30,4 %): a esa tasa, 29 filas darían unas 9 parejas (8,8), y el mínimo
  pide algo más de la mitad, 5 (19 − 14). Las de más bajan si el sesgo de H4 deja de mandar al bot
  al otro lado (las 10 P5 del rango) y si cambia la colocación de 07-03 07-11 (o4, o5, o6 y o8); la
  ablación de RN-009 dice que una respuesta sobre las zonas de control también puede añadir de más
  y quitar parejas, y por eso el mínimo 2 es de un 15 % ((39 − 33) / 39 = 15,4 %). Si el trader
  confirma que deja entradas válidas sin tomar (F7 #10), el mínimo 2 puede fallar sin que el bot
  esté mal: la salida de ese caso es «una sesión más», no el pivote.
- **Lo visto antes de fijar los números** (al estilo de ADR-0092 §12): el consultor leyó
  RECORRIDA-CONSTRUCCION-2.md con sus anexos, TRAZAS-ABLACION.md con la ablación por regla y sus
  filas, VIDEO-JULIO.md §4 (las clases de las 81 filas de julio) y revisó las 47 láminas de
  `C:\Users\USER\Desktop\laminas-sesion-7-v5`. Las corridas posteriores a RECORRIDA-CONSTRUCCION-2
  sobre toda la construcción (TRAZAS-ABLACION y LAMINAS) repiten su línea base a 0 bytes.
- **ADR-0092 §6:** el pivote decide el método (seguir, una sesión más, pivotar), nunca un
  parámetro de la spec.

### 7. Lo que cambia en los runbooks

En el mismo commit, con recuadros «Por qué cambió» que copian dentro el texto anterior (la forma
de los dos de la regla 2):

- **la regla 2 de SESION-DE-PREGUNTAS.md**: el bloque de días puede enseñar las láminas del bot;
  los días salen de `cobertura_material` (el 30 de abril, fuera) y de §3; «sin la fecha visible»
  vale para las láminas y el PDF, no para el replay que carga el trader; y la salvaguarda nueva de
  §2, paso 1;
- **su cabecera** («si una sesión lleva además días que etiquetar, no es de este runbook»): el
  bloque de días no etiqueta, no hace paquete ni particiones, y sí es de este runbook;
- **el paso 5 de «Antes»** («ningún gráfico que no sea de los preparados según la regla 2»): en el
  bloque de días, la pantalla es el replay que abre el trader, y nada más (respuesta a la PARADA,
  punto 11);
- **el paso 6 de «Antes»**: desde la sesión 7, `motor laminas` en lugar de
  `scripts/graficos_sesion.py`, que queda como el precedente de la sesión 6;
- **«Lo primero» de `docs/runbooks/LAMINAS.md`**, que deja de decir que no se enseñan.

## Problema que resuelve

Hasta hoy el método de las sesiones vivía repartido: las reglas de SESION-DE-PREGUNTAS.md, que
prohibían enseñar la orden, el stop y el objetivo; la forma de las preguntas de las sesiones 4 a
6, sin escribir como regla; y RUMBO §1, que la escribía como rumbo y anunciaba este ADR. Sin él,
las láminas (R4.5) no se podían enseñar, una activación no tenía cómo decir si entendió la
respuesta, y el pivote de RUMBO §4 no estaba pre-registrado.

## Alternativas consideradas

- Que Aleks prepare el gráfico del día, como dice el recuadro del 2026-09-28.
- Sin bloque de días: solo preguntas en abstracto con esquemas.
- Que cada activación elija el mes de construcción que corre.
- Dejar los días como lista de casos («nunca el 1 de abril ni el 1 de julio»).
- Fijar el pivote después de ver las corridas de las activaciones.

## Por que elegimos esta opcion

El trader opera el día con su voz antes de ver lo del bot, así que lo que dice no sale de lo que
ve en la lámina; la lámina enseña lo que hace el bot que el trader va a corregir. Un mes fijo con
vídeo hace comparables los deltas, y la PARADA ante un delta que no casa impide que la cifra
decida un parámetro. La condición escrita incluye los casos que la lista dejó pasar. El pivote
fijado antes de activar nada no se puede ajustar a lo que salga.

## Por que descartamos las demas

- El gráfico que prepara Aleks ya no es necesario: el día de construcción lo carga el trader, que
  necesita su replay para operar con voz; la comprobación del día y el replay limpio cubren el
  riesgo.
- Solo preguntas en abstracto: las sesiones 4 a 6 dejaron preguntas sin contestar por falta de
  contexto (`ev-v17-004910-11d48393`).
- El mes elegido por cada activación: deltas de meses distintos no se suman.
- La lista de casos dejó pasar 2026-01-02 11-15.
- El pivote fijado después no sería un pre-registro.

## Impacto

- Recuadros en SESION-DE-PREGUNTAS.md (regla 2, cabecera, pasos 5 y 6 de «Antes») y en
  docs/runbooks/LAMINAS.md («Lo primero»).
- Las dos cadenas de `src/botsito/cli.py` que decían que las láminas no se enseñan (el docstring de
  `motor_laminas` y la ayuda de `motor laminas`).
- Una NOTA en la cabecera de docs/runbooks/ACTIVAR-A35-A44.md (la regla 2 vieja que repite, el
  reinicio de ADR-0089 y A-44 RESUELTA).
- `docs/plan/PIVOTES-SESION-7.yaml` y su test (F2 de la rama).
- Quedan viejos y no se tocan aquí (Technical Debt, propuesta del cierre): la constante de
  `scripts/graficos_sesion.py:66-71` y su test, que dicen ser la regla 2, y
  `src/botsito/engine/decisiones.py:7-8` («lo fijara el ADR del metodo»); y la skill
  `ingerir-sesion` no dice la regla de la ingesta de §2, paso 5.
- No cambia: el motor, la spec, las ambigüedades, el feedback, los casos, el holdout, ADR-0021 ni
  la puerta de ADR-0092.

## Fecha / fase

2026-11-11 · post-F14, rama `trabajo/preparacion-sesion-7` (R4.3; cierra R0.3).

## Estado

ACTIVE
