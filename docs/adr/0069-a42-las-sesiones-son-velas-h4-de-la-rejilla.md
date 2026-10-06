---
status: ACTIVE
date: 2026-10-06
phase: post-F14 (rama `trabajo/activacion-a42`)
---

# 0069 · A-42 RESUELTA: las dos sesiones son las velas H4 de la rejilla de `anclaje_h4` (H2b)

> Deja SUPERADA la lectura provisional de ADR-0059 (sesiones fijas en un reloj UTC+2 todo el año,
> la hipótesis H1 de `docs/validation/RELOJ-INVIERNO.md`), y enmienda ADR-0017 (puntos 1, 4 y 5) y
> ADR-0063 (§2, §4 y §5). Informe: `docs/validation/ACTIVACION-A42.md`.

## Decision

### 1. Qué es una sesión del trader: una vela H4 de la rejilla

Las dos sesiones en que opera son **las velas H4 de la rejilla de `anclaje_h4` (17:00
America/New_York) que empiezan en ancla + 8 h y ancla + 12 h**. En su gráfico, que va en
Europe/Madrid (§3), caen de 07:00 a 11:00 y de 11:00 a 15:00 casi todo el año; **en las semanas en
que Europa y EE. UU. no coinciden en el horario de verano caen de 06:00 a 10:00 y de 10:00 a
14:00**, porque la rejilla sigue a Nueva York y su gráfico a Madrid. Es la hipótesis H2b de
RELOJ-INVIERNO.md §1.

**H2b y no H2a** (decisión del consultor del 2026-10-06, con su porqué, copiada en el encargo):
- En S-7 (SESION-04-EXTRACCION.md §3.1, `ev-v10-010429-0c93f24a`) el trader dijo que desde el 25
  de octubre la primera sesión es «de 6 a 10» en su gráfico. H2a -07:00 a 15:00 de su reloj civil,
  lo que el motor hacía hasta hoy- no prevé ningún cambio en su gráfico (RELOJ-INVIERNO.md §7).
- Por escrito, el 2026-10-06, confirmó la vuelta a las 7 desde el lunes 2 de noviembre («1-B)»,
  respuesta a la pregunta de las 15:38 del consultor, con las opciones «a) a las 6 b) a las 7 c)
  otra, ¿cuál?»), que es lo que H2b predecía y H2a no (RELOJ-INVIERNO.md §7).
- La medida de enero (RELOJ-INVIERNO.md M2 y M3: 06:00-14:00 UTC, eje en UTC+1) ya había dejado
  fuera H1; enero no separa H2a de H2b.

En UTC, con zoneinfo: la ventana es 05:00-13:00 cuando Nueva York va en horario de verano y
06:00-14:00 cuando no. Frente a lo que el motor hacía (H2a), cambian 20 días laborables al año: en
2026, del 9 al 27 de marzo y del 26 al 30 de octubre (`anexos/ACTIVACION-A42/dias_distintos.txt`).

### 2. Cómo lo hace el bot: instantes UTC desde la rejilla, con zoneinfo, nunca un desfase fijo

El bot corre en el MT5 de FTMO, no en la plataforma del trader (RELOJ-INVIERNO.md §9). Su ventana
se fija en INSTANTES UTC calculados con zoneinfo a partir de la rejilla, por UNA sola puerta,
`src/botsito/engine/relojes.py`:

- **`reloj_sesiones` gana la opción `rejilla_h4` y pasa a valer eso**, `CONFIRMED`, con este ADR
  como fuente: es de categoría `ejecucion` y lo cambia una decisión, no un registro de feedback
  (ADR-0004). `civil_operativa` y `grafico` se quedan como opciones: no son H2b, pero por el mismo
  camino los tests calculan H2a y H1 y demuestran que fallan en las semanas del cambio.
- **Parámetro nuevo `sesiones_primera_vela_h4`**, entero, valor 3, `ejecucion`, fuente este ADR:
  la ventana empieza al abrir la TERCERA vela H4 del día de rejilla, contando desde el ancla
  (ancla + 8 h). La cifra vive en el registro, no en el código (ADR-0002).
- **El reloj de la rejilla**: marca `ventana_inicio` en el instante en que abre la vela número
  `sesiones_primera_vela_h4` del día de rejilla, y corre desde ahí. Una hora nominal H de un día
  operativo es el instante `apertura de esa vela + (H − ventana_inicio)`. La apertura sale de
  `limites_del_dia` (`data/agregacion.py`), la misma función que parte las velas H4 del bot sobre
  el huso del ancla. Las formas de RN-001 y RN-002 no cambian: siguen nombrando `ventana_inicio`,
  `ventana_fin`, `reloj_sesiones` y `dias_operables`; qué parámetros lee cada reloj vive en la
  tabla de `engine/relojes.py`, como `HUSO_DEL_RELOJ` desde ADR-0063.
- **`ventana_inicio` (07:00) y `ventana_fin` (15:00) conservan valor, huso y fuente** (los dos
  registros de la sesión 1). Pasan a ser las horas NOMINALES: las que marca su gráfico cuando
  Europa y EE. UU. coinciden en el horario, y las que nombran las sesiones del kit (`07-11`,
  `11-15`) y las etiquetas de los casos.
- **Guardias dentro de la puerta**, que fallan con nombre y no adivinan: cada límite de sesión
  tiene que ser un límite de la rejilla, y cada sesión una vela H4 entera; un día de rejilla con
  una vela irregular (el domingo de un cambio de hora) no es operable. Un test comprueba que
  ningún día laborable de 2024 a 2027 cae en esa guardia.

### 3. `huso_grafico` = `Europe/Madrid`, por la medida

El gráfico del trader va en Europe/Madrid, con su cambio de hora, y no en UTC+2 fijo:

- en enero el eje de su gráfico casa con Dukascopy con UTC+1 (mediana 2-4 puntos en tres
  fotogramas; con UTC+2, 33-151) y el «14:29:59 UTC+2» del pie es la hora del replay con el
  desfase de hoy (RELOJ-INVIERNO.md §5);
- sus dos capturas de gráfico H4 del 2026-10-06 (`mensaje-whatsapp-2026-10-06-1344-grafico-h4-oct-2024.jpeg`
  y `-nov-2024.jpeg`, leídas por el consultor; RELOJ-INVIERNO.md §12) ponen el ancla a las 22:00
  del domingo 27 al jueves 31 de octubre de 2024 y a las 23:00 del domingo 3 al jueves 7 de
  noviembre, con velas a las 14:00 y a las 15:00: lo que da la rejilla de 17:00 America/New_York
  en un eje Europe/Madrid, y no en Etc/GMT-2 (23:00 y 00:00; `anexos/ACTIVACION-A42/rejilla_h4_2024.txt`);
- el trader, a las 15:36: «la del 3 de noviembre empeiza las 23:00 pm».

La fuente del valor es este ADR, que cita la medida, y no un registro de feedback: lo que el
trader escribió -«según la configuración de la plataforma etc+2 madrid» (09:53), «1- Si esta
configurado UTC+2» (13:44)- dice UTC+2, que es el desfase que su selector enseña hoy, y leerlo como
Europe/Madrid afirmaría más que su cita (decisión D3 del consultor, ACTIVACION-A42.md §6.1).
Ninguna regla cuelga de `huso_grafico`: sirve para traducir lo que él dice y para pintar las horas
como él las ve.

### 4. A-42 queda RESUELTA, y qué se registra

- Registro `RESOLVE_UNKNOWN` sobre A-42, `trader_escrito`, con el literal entero de su burbuja de
  las 15:44 («1-B)» y «2-c) la orden se pone y se ejecuta cuando ocurre la mitiga ion»), la pregunta
  de las 15:38 en `notas`, y `rejilla_h4` como valor. La parte «2-c)» contesta a otra pregunta,
  sobre el stop, y no se interpreta (punto U).
- Registro `CONFIRM` sobre `ev-v10-010429-0c93f24a` con el mensaje de las 13:45, «si es por
  cuestion horaria se oepra a las 6».
- Los literales los transcribió el consultor de las capturas, que quedan en el corpus con su
  sha256: la guardia de Claude Code no deja abrir ninguna imagen del material adicional
  (ADR-0038). Escribe desde dos números, los dos suyos, confirmado por Aleks; ninguno entra aquí.
- **Quedan en el corpus, citados aquí y sin registro** (decisión D4): 09:53 «según la configuración
  de la plataforma etc+2 madrid»; 09:59 «xd» «sep» «seria cuestion que se adapte a lo que bote la
  plataforma»; 13:44 «1- Si esta configurado UTC+2»; 15:36 «la del 3 de noviembre empeiza las
  23:00 pm». Y los tres mensajes sobre el stop (13:46 «el stop conforme se vaya validando los
  puntos breaker se va acutalziando»; 15:36 «en cuanto el stop tiene que haber mitigacion apenas
  toque»; «2-c)») no se registran contra A-11 ni contra ningún parámetro y no se interpretan:
  contexto para el punto U.
- La evidencia de A-42 suma `ev-v10-010429-0c93f24a` y `ev-v10-010438-024f76b8` (S-7).

### 5. Lo que NO cambia

- **El reloj del día de riesgo**: `huso_operativa` sigue en Europe/Madrid y `comprobar_reloj_unico`
  sigue comparándolo con el perfil de la firma (ADR-0027, ADR-0053 §4, ADR-0063).
- **Ninguna regla de entrada, stop, objetivo ni gestión.** El cierre un minuto antes del fin de la
  vela H4 (`cierre_h4_antelacion`, ADR-0060) ya iba por la rejilla.
- **A-11 y el punto U.**
- **`cases/`** (kit, fidelidad, ingesta y hoja) sigue contando la ventana de cada caso en
  `huso_operativa`. Coincide con H2b en todo el material abierto (enero, abril, mayo, agosto y
  septiembre de 2026 no tienen ningún día en los 20 de §1), y **no coincide del 9 al 27 de marzo
  de 2026**: la ventana que el sorteo congelaría en `ventanas.yaml` saldría una hora tarde.
  **Pendiente con dueño: la rama de entrada de marzo, antes de su paso b** (PARADA B0 de
  `docs/runbooks/ENTRADA-MARZO.md`). Marzo no se abre ni se lista aquí.
- **Nada sobre el servidor de FTMO** (A-28, `broker_offset_base`, `broker_dst`): solo traduce sus
  marcas de tiempo, y se mide en la demo. La ventana de ticks de un mes de invierno (ADR-0063 §5)
  queda decidida por §1: 06:00-14:00 UTC, y 05:00-13:00 los 20 días del cambio.

## Problema que resuelve

A-42 preguntaba con qué reloj cuenta el trader su horario de 07:00 a 15:00. ADR-0017 respondió que
con su reloj civil (H2a); ADR-0059 leyó provisionalmente que con un reloj UTC+2 fijo (H1);
RELOJ-INVIERNO midió que en enero opera de 06:00 a 14:00 UTC, que descarta H1 y no separa H2a de
H2b; y el trader, en S-7 y por escrito, describió el comportamiento que solo H2b predice. Sin
resolverla, el bot abriría a las 06:00 UTC la semana del 26 de octubre de 2026 cuando el trader
abre a las 05:00, y ningún mes de invierno podía entrar desde el sorteo (B0).

## Alternativas consideradas

1. H2a: la ventana en el reloj civil del trader (`civil_operativa`, lo que hacía el motor).
2. H1: la ventana fija en un reloj UTC+2 (ADR-0059).
3. H2b escrita como horas de pared en el huso del ancla (01:00-05:00-09:00 America/New_York en
   `ventana_inicio` y `ventana_fin`).
4. H2b por la rejilla: las sesiones son velas H4 de `limites_del_dia`, con un parámetro que dice
   cuál es la primera (la elegida).
5. Igual que la 4, pero con los parámetros de la rejilla como argumentos nuevos en las formas de
   RN-001 y RN-002.

## Por que elegimos esta opcion

- La 4 dice lo mismo que el trader («la sesión de cuatro horas», «de 6 a 10 después del día 25»,
  «1-B)») y lo mismo que la medida de los dos cambios de hora, con zoneinfo y sin ningún desfase.
- Reusa la función que ya parte las velas del bot: la sesión y la vela H4 no pueden separarse por
  un redondeo distinto.
- Las formas, el kit y las etiquetas no cambian; cambia una opción, un entero y la puerta que ya
  existía desde ADR-0063.

## Por que descartamos las demas

- La 1 falla 20 días al año frente a lo que el trader dijo y confirmó por escrito.
- La 2 falla 91 días al año: todo el invierno (RELOJ-INVIERNO.md M2 y M3).
- La 3 separa `ventana_inicio` de su fuente (el trader dijo «7», no «1 de Nueva York»), rompe el
  test que ata las sesiones del kit a la ventana y expresa como hora de pared lo que el trader
  expresa como vela.
- La 5 mete en dos formas lo que es una propiedad del reloj, y el precedente de ADR-0063 es la
  tabla de `relojes.py`.

## Impacto

- **Registro:** `reloj_sesiones` (opción y valor `rejilla_h4`, `CONFIRMED`, fuente este ADR, sin
  `ambiguedad_id`); `sesiones_primera_vela_h4` (nuevo); `huso_grafico` (`Europe/Madrid`, fuente
  este ADR); descripciones de `anclaje_h4`, `ventana_inicio` y `ventana_fin`.
- **Spec:** A-42 `RESUELTA` con su evidencia ampliada; notas de RN-001 y RN-002 (el título de
  RN-001 y su «manda SU horario, no la rejilla» quedan corregidos); `docs/spec/` regenerado.
- **Feedback:** carpeta nueva `knowledge/feedback/2026-10-04-sesion-04/`, dos registros.
- **Código:** `engine/relojes.py` (la puerta), `engine/primitivas.py`, `engine/motor.py`,
  `engine/cableado.py`, `engine/arnes.py`, `engine/simulacion.py`, `engine/visor.py`, `cli.py` y
  dos scripts. En construcción no cambia ningún instante.
- **Tests:** `tests/unit/test_sesiones_rejilla_h4.py` (nuevo) con las fechas del encargo, la
  rotura de H2a y de H1, la prueba de que ninguna hora sale de un desfase fijo y la guardia de la
  vela irregular sobre 2024-2027; se actualizan los que fijaban el estado anterior.
- **Documentos:** recuadros en ADR-0017, ADR-0039, ADR-0059 (SUPERSEDED), R0 de ABRIL-Y-LA-CAJA,
  MIRAR-EL-MATERIAL, ENTRADA-MARZO (B0), el README de runbooks, el índice de ADR y `CLAUDE.md`. En
  Technical Debt, la deuda «EL «UTC+2 FIJO» FALLA EN ENERO» queda pagada; de la línea de Oanda y
  Dukascopy sigue viva la parte de la serie.
- **Pendiente con dueño:** `cases/` por la rejilla, en la rama de entrada de marzo (§5).

## Fecha / fase

2026-10-06 · post-F14, rama `trabajo/activacion-a42`.

## Estado

ACTIVE
