# El visor de días de construcción

Cómo se mira un día para depurar una regla del motor. Escrito el 2026-09-25 en la rama
`trabajo/visor-dias`. Complementa a `ARNES-MOTOR.md`: el arnés da las cifras del conjunto; el
visor enseña UN día de un vistazo.

## Qué hace

Para un día `dev` de un mes de CONSTRUCCIÓN (hoy abril y agosto de 2026), genera una página HTML
autocontenida —sin JavaScript ni librerías— con:
- las **M1 de la ventana del día** (00:00-15:00 del trader), con una casilla para ver **M15**;
- las **H4 de contexto**: la previa y las que miró el sesgo, con la que rompió resaltada por sesión;
- las **operaciones del trader** (entrada y stop del caso, en su instante de llenado) y las del
  **bot** si el arnés las produjo. El objetivo se pinta DERIVADO por `objetivo_rr` y va marcado
  como tal: el caso no trae objetivo (ADR-0043);
- por sesión: el **sesgo** anotado por el motor y lo que dice `domain/sesgo.py`, los **hechos
  fijados en su instante**, el **embudo** con la misma lectura que el arnés y **dónde se para**
  (primitiva `NO_IMPLEMENTADA` o gate que prohibió), las reglas disparadas y los **avisos H3**;
- las **parejas del criterio de fidelidad** (qué operación del bot casa con cuál del trader).

## Cómo se corre

Un día:
```
uv run botsito motor visor --caso caso-eurusd-2026-04-01
```
Todos los días de construcción, con un índice (`index.html`) que enlaza cada página y dice por día
las sesiones con trader, las operaciones, las parejas, el sesgo y dónde se para el embudo:
```
uv run botsito motor visor --todos
```
Con `--meses AAAA-MM,AAAA-MM` solo esos meses, que tienen que ser de construcción. La salida va a
`data/visor/` (o a `--salida <carpeta>`): **está ignorada por git y NO se comitea**. Se abre el
HTML en el navegador; medido, todos los días de construcción tardan menos de diez segundos.

La vista se recorta a un instante con `--hasta HH:MM` (hora local del trader):
```
uv run botsito motor visor --caso caso-eurusd-2026-04-01 --hasta 09:30
```
Escribe `<caso>.hasta-0930.html` con solo lo cerrado y fijado hasta esa hora: es la forma de ver
lo que el motor SABÍA en ese momento, sin mirar al futuro.

## Cómo depurar una regla nueva con él

1. Escribe la primitiva y corre el arnés (`ARNES-MOTOR.md`): el embudo dice cuántas sesiones se
   paran ahora en cada primitiva.
2. Genera el visor de todos los días (`--todos`) y abre el índice: la columna «donde se para el
   embudo» localiza en qué sesiones tu regla dejó de ser el tope y qué viene después.
3. Abre un día con operaciones del trader donde la regla debería disparar y mira, en la calle de
   hechos, EN QUÉ INSTANTE fijó el hecho, y en el gráfico, si ese instante cae donde el trader
   entró (la pareja del criterio, naranja, se dibuja sola cuando casan).
4. Si el hecho se fija tarde o pronto, `--hasta` con la hora sospechosa enseña las velas cerradas y
   los hechos vivos justo entonces, que es lo único que la primitiva pudo ver.
5. Los avisos H3 de la sesión dicen si dos reglas de la misma clase dieron SÍ a la vez: la spec
   tiene que resolverlo, no el orden por id (ADR-0049).

## Cuándo se niega

Mismo mecanismo y mismos mensajes que el arnés (`arnes.dias_de_construccion`):
- **un mes de medida** (hoy mayo) o **cualquier mes que no sea de construcción** (marzo,
  septiembre, febrero...): `ERROR` y código 2, sin escribir nada;
- **un día oculto** (reservado o retirado) en el reparto del mes: `ERROR` y código 3 sin leer su
  caso. Un test con centinela (`tests/unit/test_visor.py`) lo comprueba.

## Lo que no hace

No mide nada sobre mayo, no abre ningún holdout, no toca la spec ni el motor, y no produce
operaciones del bot: pinta lo que el arnés de hoy produce. Cuando el bróker simulado exista, las
operaciones del bot y sus parejas aparecerán sin cambiar el visor.
