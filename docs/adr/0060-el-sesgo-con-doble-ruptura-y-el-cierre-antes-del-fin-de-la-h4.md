---
status: ACTIVE
date: 2026-09-30
phase: post-F14 (rama `trabajo/nocturno-01oct`, sesión nocturna)
---

# 0060 · El sesgo con doble ruptura lo decide el color, y toda operación se cierra antes del fin de su vela H4 (PROPUESTO: pendiente de aceptación del consultor)

> **PROPUESTO.** Escrito en la sesión autónoma de la noche del 30 de septiembre al 1 de octubre de
> 2026 (`docs/nocturno/PLAN-01oct.md`, F32). Lo que el trader dijo en la sesión 3 ya estaba activado
> en la spec por `trabajo/activar-sesion-03`; aquí se lleva al motor, y lo que el trader NO dijo se
> decide con la lectura más conservadora y va marcado **DECISIÓN NOCTURNA**. Lo acepta o corrige el
> consultor; hasta entonces nada de lo que aquí se fija se toma por aceptado. El campo `status`
> dice ACTIVE solo porque la guardia de ADR (`tests/unit/test_adr.py`) no admite otro valor.

## Decision

### 1. Con doble ruptura, el sesgo es el del color con que cierra la vela

Si la vela H4 que fija el sesgo rompe **los dos** extremos de su anterior, el sesgo es el del
**color con que cierra**: verde —cierra por encima de su apertura—, alcista; roja, bajista. Es lo
que el trader respondió a A-34 en la sesión 3 («si rompe por los dos [...] importa el color de la
vela», `fb-2026-09-29-sesion-03-617f496a`, `fb-2026-09-29-sesion-03-31fb311f`,
`ev-v9-001617-4b47e01a`). **Enmienda ADR-0044 §1**, que lo dejaba en AMBIGUO a la espera de esa
respuesta. Con un solo extremo roto, el color sigue sin decidir nada (RN-003, notas).

- El color es el del **cuerpo**, cierre contra apertura, sea cual sea `sesgo_h4_criterio_ruptura`.
- La vela con doble ruptura **fija** el sesgo: la búsqueda hacia atrás de ADR-0044 §2 para en ella.
- Código: `domain/sesgo.py`. `ResultadoSesgo` gana `doble_ruptura`, y el motor lo anota por sesión
  (`sesgo_h4_doble_ruptura`) para que el informe del arnés y el visor digan cuántas son.

### 2. DECISIÓN NOCTURNA: la doble ruptura de una vela SIN CUERPO sigue siendo `ambiguo`

Una vela que rompe los dos extremos y cierra exactamente donde abrió no tiene color. El trader no
describió ese caso. Se conserva `ambiguo`, y con él RN-033 sigue prohibiendo operar en esa sesión:
es la lectura de ADR-0044 («la más conservadora donde no habla»). El token `ambiguo`, el valor del
hecho `sesgo` y la forma de RN-033 no cambian; cambia solo cuándo se produce. **Pregunta para la
sesión 4**, si el consultor la quiere abrir como ambigüedad: qué sesgo toma una vela sin cuerpo que
rompe los dos extremos.

### 3. `insuficiente` se conserva, como valor del proyecto y no del trader

El trader dijo que «siempre va a haber un sesgo» (`fb-2026-09-29-sesion-03-1168f036`,
`ev-v9-001529-ac28bb40`): para él el sesgo es el del último rango, dure lo que dure.
`insuficiente` no contradice eso: es lo que pasa cuando la búsqueda hacia atrás agota
`sesgo_h4_tope_velas` —un tope del proyecto, ADR-0044 §2, PROVISIONAL— sin encontrar ninguna
ruptura, o cuando faltan velas. RN-033 sigue prohibiendo con él. No se cambia el tope.

### 4. RN-002 cierra cuando a la vela H4 en curso le queda `cierre_h4_antelacion` o menos

El trader cierra toda operación «siempre menos un minuto, antes de que cierre [...] la sesión de
cuatro horas» (`fb-2026-09-29-sesion-03-c38c4aef`, `ev-v9-002735-472432b8`). Se escribe así:

- **Un parámetro nuevo, `cierre_h4_antelacion`**, `estrategia`, `minutos`, CONFIRMED con la cifra
  del trader. Su fuente es el ítem de evidencia que recoge la frase, y no el registro de
  feedback: ese registro es un CORRECT sobre la regla, no sobre un parámetro (§6). La cifra no
  va en la forma ni en el código (ADR-0002).
- **Un predicado nuevo, `vence_vela_h4`**, de fuente `reloj`, con dos argumentos: `anclaje` y
  `antelacion`. Da SÍ cuando a la vela H4 que contiene el minuto que acaba de cerrar le queda
  `antelacion` o menos para terminar.
- **La rejilla es la de `anclaje_h4`**, la misma que parte las velas del sesgo
  (`data/agregacion.py`), como pidió el consultor (`PROJECT_STATE.md`, Next Action A3.a). Los 337
  días del año en que la ventana coincide con dos velas H4 el cierre cae a las 10:59 y a las 14:59
  del trader; los otros 28 (RN-001, notas) cae donde termine la vela, a mitad de su sesión.
- **La forma de RN-002** pasa a `cualquiera_de [vence_vela_h4, alcanza_hora ventana_fin]` junto a
  la posición viva. **`ventana_fin` no se toca** y su cierre en punto se conserva como segunda rama.
- **El interruptor es el mismo**, `cierre_forzoso_fin_ventana`: no nace un segundo parámetro para
  apagar el cierre.

### 5. DECISIÓN NOCTURNA: el predicado vale también en el propio límite de la vela

El evento del minuto `t` es el cierre de la M1 `[t − 1, t)` (ADR-0028, ADR-0053 §5). Con la
antelacion del trader, `vence_vela_h4` da SÍ en el evento anterior al límite **y en el del propio
límite**. Así, una orden que se llene dentro del último minuto de la vela se cierra en el evento del
límite, antes de que empiece la vela siguiente: ninguna posición cruza de una vela H4 a otra. El
trader no describió ese caso (dijo además que no tiene hora límite para abrir,
`ev-v9-012514-b5b6c84f`); la alternativa era dejarla vivir hasta el fin de la vela siguiente.

### 6. Lo que NO se decide aquí

- **La orden pendiente al vencer la vela.** RN-002 cierra posiciones; no retira órdenes. A-39 sigue
  ABIERTA por el corte de audio y «por la orden pendiente», y `retirar_orden_limite` sigue
  declarada y sin regla que la use (A-30).
- **El reloj de la ventana** (A-42, ADR-0059). Esta regla no depende de él: mira la rejilla H4.
- **Qué registro cita cada regla.** RN-002, RN-003 y RN-033 siguen citando los registros de la
  sesión 1, como las dejó `trabajo/activar-sesion-03`, y sus tres CORRECT de la sesión 3 siguen
  saliendo como pendientes en `botsito feedback pending`, que da un CORRECT sobre una regla por
  reflejado solo cuando la regla lo cita. El motor ya hace lo que dicen; cambiar la `cita` y el
  `literal` de una regla es cosa del consultor. En RN-033 no es trivial: el registro dice que
  siempre hay sesgo, y la regla prohíbe justo en los dos casos que el trader no describió.
- **El cierre a mercado llega al cierre de la M1**, no al tick (ADR-0053 §2.1, para revisar con la
  demo).

## Problema que resuelve

Desde `stable/F31-activar-sesion-03` la spec decía dos cosas que el motor no hacía
(`docs/validation/ACTIVAR-SESION-03.md` §3, desalineaciones 1 y 2): que con la doble ruptura decide
el color, mientras `sesgo_h4_al_abrir` seguía fijando `ambiguo` y RN-033 prohibía operar; y que toda
operación se cierra un minuto antes del fin de su vela H4, mientras la forma de RN-002 cerraba solo
al llegar `ventana_fin`.

## Alternativas consideradas

1. Doble ruptura sin cuerpo: seguir buscando hacia atrás, como si esa vela no hubiera roto nada.
2. Doble ruptura sin cuerpo: `ambiguo`, y no se opera (la elegida).
3. Quitar `insuficiente` y buscar hacia atrás sin tope.
4. RN-002 con una hora fija del registro (dos parámetros, las 10:59 y las 14:59).
5. RN-002 con un predicado sobre la rejilla de `anclaje_h4` y la antelación en un parámetro (la
   elegida).
6. Un interruptor propio para el cierre de la vela H4, distinto de `cierre_forzoso_fin_ventana`.

## Por que elegimos esta opcion

- La 2 es la lectura de ADR-0044 donde el trader no habla, y no toca la forma de RN-033.
- La 5 dice lo que dijo el trader —«antes de que cierre la sesión de cuatro horas»— sobre la vela,
  no sobre el reloj de la ventana, y sigue valiendo los 28 días en que la vela no coincide con la
  sesión y cuando A-42 cambie el reloj de la ventana.

## Por que descartamos las demas

- La 1 inventa un sesgo que ninguna vela dio.
- La 3 cambia un tope que decidió el consultor (ADR-0044 §2) sin que lo haya pedido, y una
  búsqueda sin tope depende de cuántas velas haya cargadas.
- La 4 ata el cierre a la ventana y no a la vela: en las semanas de desfase cerraría a una hora en
  la que no termina ninguna vela H4, y duplicaría en dos parámetros lo que es una sola cifra.
- La 6 crea dos puertas para la misma decisión del trader, que cierra siempre (ADR-0002).

## Impacto

- **Código:** `src/botsito/domain/sesgo.py` (el color con doble ruptura, `doble_ruptura`);
  `engine/primitivas.py` (`vence_vela_h4` y la anotación por sesión); `engine/arnes.py` (una línea
  nueva en el informe: cuántas sesiones decide el color); `engine/visor.py` (lo dice en el detalle
  del sesgo).
- **Spec:** el predicado `vence_vela_h4`; el parámetro `cierre_h4_antelacion`; la forma, el título,
  el `cuando` y los parámetros de RN-002; el `entonces` de RN-003; las notas de RN-002, RN-003 y
  RN-033; las descripciones de `sesgo_h4_al_abrir` y del token `ambiguo`. `spec_version` **13.5.0 →
  14.0.0**: dos reglas cambian lo que el motor hace.
- **Tests:** `tests/unit/test_sesgo_h4.py` y `tests/unit/test_huecos_motor.py` cambian de sentido a
  propósito (la doble ruptura con cuerpo ya no es ambigua; la ambigua es la de una vela sin cuerpo);
  `tests/unit/test_cierre_vela_h4.py`, nuevo; y en `tests/unit/test_cableado.py`, el cierre de punta
  a punta sobre el día sintético de 2030.
- **Medido sobre construcción** (abril y agosto de 2026: 42 días `dev`, 84 sesiones, 49 con
  operaciones del trader), con `motor arnes` antes y después, en DIAGNÓSTICO —A-35
  `cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control` y, en la simulación,
  A-27 con 0 puntos—, así que **ninguna de estas cifras cuenta como medida de fidelidad**:
  - el sesgo de las 49 sesiones con operaciones del trader pasa de alcista 21, ambiguo 6 y bajista
    22 a **alcista 24 y bajista 25**; 6 de ellas las decide el color;
  - por operación del trader, de a favor 58, ambiguo 7 y en contra 12 a **a favor 62 y en contra
    15**: de las 7 operaciones que caían en una sesión con doble ruptura, 4 van a favor del color y
    3 en contra;
  - **RN-033 deja de dispararse**: de 15 sesiones de 84 a ninguna. No hay ninguna doble ruptura
    sin cuerpo ni ningún `insuficiente` en construcción;
  - `liquidez_tomada` se produce en 44 de las 49 sesiones, antes 38;
  - en la simulación, las operaciones del bot puntuables pasan de 6 a 5, con la misma cobertura
    (2 de 77). La que se pierde es de una segunda sesión cuyo día abría con una sesión ambigua:
    ahora la primera sesión tiene sesgo y toma, y el productor de la zona sigue usando la primera
    toma del día (la deuda de ADR-0055 §4, que es la funcionalidad siguiente del plan);
  - **RN-002 no llega a disparar** en estas corridas: ninguna posición del bot llega viva al fin de
    su vela H4. Lo que la sostiene es el test de punta a punta.

## Fecha / fase

2026-09-30 · sesión nocturna, rama `trabajo/nocturno-01oct`. `PROJECT_STATE.md`, Next Action A3.a.

## Estado

ACTIVE (PROPUESTO: pendiente de aceptación del consultor; el campo dice ACTIVE porque la guardia
de ADR no admite otro valor)
