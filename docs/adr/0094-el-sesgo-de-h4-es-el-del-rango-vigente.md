---
status: ACTIVE
date: 2026-11-18
phase: post-F14 (rama `trabajo/activar-sesion-07`, R4.3 de la hoja de ruta)
---

# 0094 · El sesgo de H4 es el del rango vigente (enmienda ADR-0044 §2, ADR-0060, ADR-0075 y ADR-0080)

> Decisiones del consultor del 2026-11-18 (encargo de `trabajo/activar-sesion-07`, F1). Lo dijo el
> trader en la sesión 7a (S-1, v18, 2026-11-16; `docs/validation/SESION-07-EXTRACCION.md` §3.3):
> `fb-2026-11-16-sesion-07-33fdaa6c` (CORRECT sobre RN-003). **Enmienda ADR-0044 §2, ADR-0060, ADR-0075 y ADR-0080**
> (recuadro en cada uno y fila del índice).

## Decision

### 1. Lo que dijo el trader

- **Qué vela es el rango**: ante una H4 verde grande y una roja posterior dentro de ella, «La
  respuesta es la letra A, claramente. El rango es la vela verde grande y sigo buscando compras.»
  (`ev-v18-000249-bb7b1c07`).
- **Cómo cambia el lado**: «bastaría con mecha o con cuerpo un rompimiento, pero para poder tener el
  enfoque, se tiene que definir el color de la vela» (`ev-v18-000408-c48297b1`): lo de ADR-0080.
- **Qué rango manda**: «el rango mayor sería esto de aquí. O sea, porque este rango todavía la
  liquidez, tanto por encima como por debajo, no sea mitigada … primero a tener en cuenta ese rango
  mayor que no ha sido mitigado y ya una vez mitigado pues se actualiza» (`ev-v18-000912-52594a58`).
- **Qué vela pasa a ser el rango nuevo**, en parte: «para nosotros poder definir nuestro nuevo
  rango tenemos que ver qué vela o sea si es alcista o bajista y rompe o por encima o por debajo»
  (`ev-v18-000822-57145b90`); no dice que el rango nuevo sean el alto y el bajo de esa vela.
- **Ya lo había dicho**: para él el sesgo es el del último rango, dure lo que dure (ADR-0060,
  `ev-v9-001529-ac28bb40`), y RN-003 llevaba en sus notas la reserva «suponiendo que no haya otro
  rango mayor» (sesión 4, S-13). En el bloque de días de la 7a corrige al bot con esta regla en dos
  sesiones de construcción (2026-07-07 y 2026-07-15, de 11 a 15: `ev-v18-004639-96f84da4`,
  `ev-v18-004718-01861c91`, `ev-v19-004104-6d9d48cc`); son ejemplos, sin «¿siempre…?», y solo
  sostienen lo dicho en el bloque técnico.

### 2. La regla

Se recorren HACIA DELANTE las H4 cerradas a la apertura de la sesión (por su hora de fin, ADR-0044
§3), con un estado: el **rango** (su alto, su bajo y la H4 que lo fijó) y el **lado**. Romper es
superar el extremo con `sesgo_h4_criterio_ruptura` (`mecha`), por poco que sea; igual es un equal y
no rompe (ADR-0044 §4).

- **a)** Una H4 que no supera ni el alto ni el bajo del rango no cambia nada. **Dicho**
  (`ev-v18-000249-bb7b1c07`).
- **b)** Una H4 que supera el alto del rango y cierra verde fija el lado alcista; la que supera el
  bajo y cierra roja, bajista. **El lado es lo dicho** (ADR-0080; `ev-v18-000408-c48297b1`). **Que
  el rango pase a ser esa vela, su alto y su bajo con el mismo criterio, es LECTURA DEL
  CONSULTOR** (A-58).
- **c)** Una H4 que supera los dos extremos: decide el color (ADR-0060) y el rango pasa a ser esa
  vela; sin cuerpo no decide (ADR-0075) y el rango no cambia.
- **d)** Una H4 que supera un extremo y cierra del color contrario, o sin cuerpo, no decide (ADR-0080,
  D1 y D3) **y el rango NO cambia. LECTURA DEL CONSULTOR** (A-58), apoyada en lo que el trader dice
  en su backtest de julio (`VIDEO-JULIO.md` §4.1; v11 0:00:38, `ev-v11-000038-fef9789d`, el ítem
  vigente de los dos de ese instante, que supersede a `ev-v11-000038-a322e483`): «este es nuestro
  rango Por lo general, como no ha sido mitigado Ni por debajo por una vela bajista Ni por arriba por
  una vela alcista Para actualizar el rango».
- **e)** El arranque: el rango inicial es la H4 situada `sesgo_h4_tope_velas` velas antes de la
  última cerrada, sin lado; si hay menos velas cargadas que el tope, la primera que haya. Si al
  llegar a la apertura ninguna vela decidió, INSUFICIENTE (RN-033), como hasta hoy. **Decisión del
  proyecto**, como el tope (ADR-0044 §2).

### 3. Lo que es parámetro y lo que no

- **La regla no es un parámetro ni un interruptor** entre la de ADR-0080 y esta: es la definición
  del trader. ADR-0080 D5 (y su alternativa 1) lo descartó para la exigencia del COLOR, por la misma
  razón; aquí se aplica por analogía, no porque ADR-0080 hablara del rango.
- **Lo que el trader no dijo sí es parámetro**: las lecturas b) y d) van en
  `sesgo_h4_rango_nuevo`, DEFAULT_AMBIGUOUS en `vela_que_rompe_con_su_color` (la opción que las
  describe), bajo la ambigüedad nueva **A-58** («cuando una H4 rompe tu rango, qué alto y qué bajo
  forman el rango nuevo; y si la vela que lo rompe cierra del color contrario, qué pasa con el
  rango»), de clase `pregunta` y no bloqueante. La otra opción del registro, `otra`, no la hace el
  motor: se niega con nombre hasta que el trader la diga.
- `sesgo_h4_criterio_ruptura` (`mecha`, CONFIRMED) y `sesgo_h4_tope_velas` (60, CONFIRMED por
  ADR-0044) no cambian.

### 4. El arranque y cuántas velas hay cargadas

ADR-0060 descartó una alternativa porque su resultado dependía de cuántas velas hubiera cargadas
(`0060`, «Por que descartamos las demas»). La regla e) vuelve a depender de ello: el rango inicial
es la H4 `sesgo_h4_tope_velas` antes de la última, o la primera cargada. Por eso, antes de la
corrida, la rama midió sobre todas las sesiones de construcción cuántas cambian de lado al pasar
el arranque de 60 a 120 velas, y cuántas tienen cargadas menos de 60 y menos de 120
(`docs/validation/ACTIVAR-SESION-07.md`, F1, punto 6; `anexos/ACTIVAR-SESION-07/arranque.py`). La
cifra es diagnóstico: no cambia el tope (ADR-0093 §4).

### 5. El motor

- `src/botsito/domain/sesgo.py`: la regla de §2. `ResultadoSesgo` gana, SOLO como registro, el
  alto, el bajo y la H4 del rango vigente (`rango_alto`, `rango_bajo`, `rango_vela`). Sus campos de
  antes cambian de significado así: `ruptura_puntos`, cuánto superó la H4 que fijó el lado el
  extremo del RANGO; `velas_miradas`, cuántas H4 se compararon con el rango; `doble_ruptura`, la que
  fijó el lado rompió los dos extremos del rango; las saltadas, las H4 que rompieron el rango sin
  decidir después de la que lo fijó (o desde el arranque).
- `engine/primitivas.py`: el predicado `sesgo_h4_al_abrir` con el sujeto nuevo de RN-003
  (`que: vela_h4_cerrada`, `contra: rango_h4_vigente`) y el argumento `rango_nuevo`; una anotación
  más por sesión, `sesgo_h4_rango` (alto, bajo e inicio de la H4 del rango), solo registro.
- El arnés no cambia de forma: la línea «Por sesion» sigue dando `rn003`.
- El visor y las láminas dicen el rango vigente (su alto, su bajo y la H4 que lo fijó) en lugar de
  «la H4 previa contra su anterior».

## Problema que resuelve

Con la regla de ADR-0080 el sesgo lo fijaba la H4 previa contra su anterior: una roja que rompe el
bajo de su anterior sin salir del rango mayor cambiaba el lado a bajista. El trader dice que no
(«El rango es la vela verde grande y sigo buscando compras») y lo corrige en el bloque de días. En
`VIDEO-JULIO.md` §4.1 y §4.2, 30 filas de julio (20 del trader en P1 y 10 del bot en P5 del otro
lado, en siete sesiones) se clasificaron como «regla desconocida: el rango de H4».

## Alternativas consideradas

1. Un parámetro o interruptor entre la regla de ADR-0080 y la del rango.
2. El rango nuevo como el anterior ampliado hasta el extremo roto, en vez de la vela que rompe.
3. Que la vela que rompe y cierra del color contrario también actualice el rango.
4. Reabrir A-1.
5. Arrancar el recorrido en la primera H4 cargada, sin tope.

## Por que elegimos esta opcion

- Es lo que dijo el trader en el bloque técnico, con una pregunta cerrada sobre un esquema, y lo
  aplica en el bloque de días; lo que no dijo queda separado, como lectura del consultor, en un
  parámetro con su ambigüedad.
- No pisa nada de lo fijado: el color, la neutra y el criterio de mecha siguen como los dejaron
  ADR-0060, ADR-0075 y ADR-0080.

## Por que descartamos las demas

1. **Interruptor**: es la definición del trader, no una opción del proyecto (§3).
2. **El rango ampliado** y 3. **la vela de color contrario actualiza**: son las otras lecturas de
   lo que el trader no dijo; van a la pregunta de A-58, y el delta de julio no elige entre ellas
   (ADR-0093 §4).
4. **Reabrir A-1**: su pregunta sigue contestada (la H4 decide; cambia cuando rompe); lo que cambia
   es contra qué rompe, que entra por el CORRECT sobre RN-003, como en ADR-0060, ADR-0075 y ADR-0080
   (§9).
5. **Sin tope**: haría depender el lado de cuánto historial hubiera cargado, sin límite; el tope de
   ADR-0044 lo acota y el punto 6 de la rama mide cuánto pesa.

## Impacto

- `knowledge/spec/strategy_spec.yaml`: RN-003 (título, `entonces`, `cita`, `literal`, forma y un
  párrafo en sus notas), el predicado `sesgo_h4_al_abrir` (descripción, argumentos, `cita` y
  `literal`), dos tokens nuevos (`vela_h4_cerrada`, `rango_h4_vigente`) y las notas de RN-033.
  `parametros.yaml`: `sesgo_h4_rango_nuevo` (nuevo, DEFAULT_AMBIGUOUS, A-58) y las descripciones de
  `sesgo_h4_regla` y `sesgo_h4_tope_velas`. `ambiguedades.yaml`: A-58 (nueva) y una nota en A-1, que
  no se reabre. `docs/spec/` regenerado.
- El motor, el visor y las láminas (§5); el arnés no cambia de forma. Los guiones de `scripts/` y
  los anexos de ramas cerradas no se tocan ni se corren: con el motor nuevo darían la regla nueva.
- La corrida de julio de ADR-0093 §4, con sus filas declaradas (las siete sesiones del rango de
  H4), diagnóstico: `docs/validation/ACTIVAR-SESION-07.md`.
- Pregunta para la 7b: A-58.

## Fecha / fase

2026-11-18, rama `trabajo/activar-sesion-07` (R4.3 de `docs/plan/HOJA-DE-RUTA.md`, punto (1) de la F
de la Next Action).

## Estado
ACTIVE
