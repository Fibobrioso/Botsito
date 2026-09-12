---
status: ACTIVE
date: 2026-09-10
phase: F11
---

# 0015 · Los relojes tras la auditoria: el del grafico es un default, y el dia de riesgo necesita el suyo


> **Enmienda (2026-09-11, ADR-0020).** La aritmetica de la seccion "Problema que resuelve" era la de la base vieja del lotaje: decia que cada perdida cuesta 0,4 % y que caben **once** antes de tocar el 4,5 %. Desde ADR-0020 el lote se dimensiona hasta el stop, cada perdida cuesta el **0,5 % entero** y el margen son **nueve**. Lo que este ADR decide -que el dia de riesgo necesita su propio reloj, `reloj_dia_riesgo`- no cambia; al contrario, con nueve perdidas el freno se toca antes.

## Decision

1. **`huso_grafico` baja de `CONFIRMED` a `DEFAULT_AMBIGUOUS`** con `ambiguedad_id: A-14`. El valor
   `Etc/GMT-2` se queda -el bot tiene que correr con algo- pero deja de afirmarse como un dato del
   trader: es una eleccion nuestra sobre una lectura de verano.
2. **Su `fuente` pasa a `ev-v3-000136-6160fcea`**, que es donde el trader habla de su grafico. El
   registro de feedback que lo sostenia, `fb-...-8384b085`, queda REVOCADO con un registro que lo
   supersede: su literal habla de la vela de las 23, no del reloj.
3. **ADR-0012 punto 5 queda CORREGIDO en su motivo.** Decia que "la sesion desmintio Europe/Madrid".
   No lo desmintio. La decision de alinear `huso_operativa` con `huso_grafico` se mantiene, pero por
   decision, no por una evidencia que no existe.
4. **A-14 se reescribe con TRES opciones** -offset fijo, Madrid, o el reloj del servidor- y pasa a
   listar los cuatro parametros que dependen de ella: `huso_grafico`, `anclaje_h4`,
   `ventana_inicio` y `ventana_fin`.
5. **`reloj_dia_riesgo`** (`prop_firm`, `servidor | grafico`, `DEFAULT_AMBIGUOUS` en `servidor`,
   `ambiguedad_id: A-19`): en que reloj cae la medianoche que reinicia el tope diario y el domingo
   que reinicia el semanal.
6. **`base_calculo_perdida_semanal`** (`estrategia`, `CONFIRMED` en `saldo_actual`): la base del
   tope semanal, que estaba en el literal del trader desde la sesion y no tenia donde guardarse.

## Problema que resuelve

**El reloj del grafico se afirmaba como un hecho y no lo es.** `huso_grafico = Etc/GMT-2` entraba
`CONFIRMED` citando `fb-...-8384b085`, cuyo literal completo es *"la vela empieza a las 23, la
primera vela de cuatro horas"*: no dice nada de husos. El UTC+2 salia de las `notas` del registro,
de una lectura de pantalla. Y **todas las lecturas del repositorio son de verano**:

- `ev-v3-000136-6160fcea`, el trader: *"yo lo tengo configurado como **utc mas 2 que son ahora ya
  madrid**"*. Su propia frase ata el UTC+2 a Madrid, y "ahora" es verano.
- `ev-v6-005830-48b30e48`: el fotograma muestra TradingView con `20:48:30 UTC+2`, del 2026-09-09,
  tambien verano. TradingView etiqueta igual un huso fijo que Madrid mientras el horario de verano
  este activo.
- `ev-v6-005810-5cb1ef06`, preguntado justamente por eso: *"Es la misma hora [...] Si es una hora
  mas, pues seria a las 8, o si es una hora menos, a las 6"*. El propio item lo anota: *"las dos
  mitades de la frase no dicen lo mismo"*.

**Etc/GMT-2 y Europe/Madrid son indistinguibles de mayo a octubre**, y no hay una sola observacion
de invierno. Afirmarlo `CONFIRMED` era afirmar lo que no se ha medido, sobre el parametro del que
cuelgan las tres horas de la operativa.

**Y el "dia" del freno diario no estaba definido.** Tras la correccion de la aritmetica de los
cartuchos, RN-020 es el unico freno del dia que existe: con 0,5 % de riesgo nominal y el stop en
0,8, cada perdida cuesta 0,4 %, asi que caben unas once perdidas seguidas antes de tocar el 4,5 %.
Pero "el saldo inicial del dia" no dice **cuando empieza el dia**, y los dos relojes candidatos se
separan una hora buena parte del año -la ficha de `broker_dst` ya lo decia: *"en verano el reloj va
a GMT+3 y el dia de riesgo se desplaza"*-. En una cuenta fondeada, equivocarse en el corte no
cuesta un trade: cuesta la cuenta.

## Alternativas consideradas

- **A. Dejar `huso_grafico` CONFIRMED** y confiar en que A-14 ya lo señalaba.
- **B. Ponerlo UNKNOWN** hasta medirlo en invierno.
- **C. Suponer el corte del dia** sin parametro, resolviendolo en el motor en F22.
- **D. Un solo parametro de reloj** para el grafico y para el corte de riesgo.

## Por que elegimos esta opcion

`DEFAULT_AMBIGUOUS` es exactamente lo que ADR-0012 punto 3 reservo para **"valores que inventamos
nosotros"**, y este lo es. El bot necesita un huso para correr; lo que no puede es decir que se lo
dijo el trader. Ademas, al bajarlo, `feedback pending` vuelve a listarlo y `spec status` lo saca en
revision, que es donde tiene que estar hasta que alguien mire el grafico en enero.

Que el corte del dia sea un **parametro** y no una suposicion del motor es ADR-0002 otra vez: el
valor vive en el registro o vive escondido. Y que sea de categoria `prop_firm` es deliberado: no es
una pregunta para el trader, es una comprobacion contra el panel de la cuenta, y asi
`no_confirmados()` -que es lo que se le lleva al trader- no se llena de cosas que no le tocan.

## Por que descartamos las demas

- **A**: A-14 solo listaba `anclaje_h4`, asi que `spec status` no sacaba en revision ni
  `huso_grafico` ni las dos horas de la ventana. El cruce en el que se apoya el informe de F11 no
  veia la raiz del problema. Y ademas la pregunta de A-14 no contemplaba el reloj del servidor,
  que es lo que `broker_dst` declara: tal como estaba escrita no podia dar con la respuesta buena.
- **B**: `UNKNOWN` significa "leerlo falla", y RN-001, RN-002 y RN-003 lo nombran. Habria dejado la
  ventana operativa entera sin poder ejecutarse por una duda que solo afecta a cuatro meses al año.
- **C**: es la deuda del §8 del informe de F11 -las reglas son prosa- aplicada al numero mas caro
  del sistema.
- **D**: son dos relojes distintos y hay que poder decirlo. El del grafico es donde el trader
  decide; el del servidor es donde se ejecuta y donde la prop firm cuenta. Juntarlos era justamente
  el error que esta auditoria encontro.

## Que sustituye de otros ADR

**Corrige ADR-0012 punto 5** en su motivo, no en su decision: `huso_operativa` sigue alineado con
`huso_grafico`, pero porque lo decidimos, no porque la sesion desmintiera Europe/Madrid. Lo que
decida A-14 mueve a los dos.

## Impacto

- El registro pasa de 52 a **54 parametros**. `no_confirmados()` sube de 6 a 7: `huso_grafico`
  vuelve a la lista de lo que falta cerrar con el trader.
- `spec status` saca ahora `huso_grafico`, `anclaje_h4`, `ventana_inicio` y `ventana_fin` bajo A-14.
- RN-020 nombra las dos bases y el reloj, y su **titulo deja de decir lo contrario que sus notas**.
- **A-14 es medible sin preguntar**: basta abrir su grafico en una fecha de invierno. Enero de 2026
  ya esta congelado en el corpus. **A-19 no se mide: se verifica en el panel de FundedNext.**

## Fecha / fase

2026-09-10, F11 (auditoria previa a la validacion).

## Estado

ACTIVE
