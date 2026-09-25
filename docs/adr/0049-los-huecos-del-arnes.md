---
status: ACTIVE
date: 2026-09-25
phase: post-F14 (rama `trabajo/huecos-motor`)
---

# 0049 · Los huecos del arnés

## Decision

Este ADR **complementa a ADR-0048 y no lo enmienda**: cierra, con las decisiones del consultor
del 2026-09-25, los seis huecos de interpretación que ADR-0048 registró en su «Impacto» (H1-H6)
«y no inventó». Las decisiones salen del informe de solo lectura de esa misma fecha, que la rama
recoge en `docs/validation/HUECOS-MOTOR.md` §1. Lo que aquí se decide se resuelve en la spec, en el
registro o en una ambigüedad; el código solo lo ejecuta. Todo lo demás de ADR-0048, ADR-0030,
ADR-0018, ADR-0028, ADR-0032 y ADR-0044 sigue tal cual.

### H1 · RN-003 frente a ADR-0044: opción (c)

1. **`ambiguo` e `insuficiente` son valores del hecho `sesgo`.** `hechos.sesgo.valores` pasa de
   `[sentido_de_la_ruptura]` a `[sentido_de_la_ruptura, ambiguo, insuficiente]`, y los dos nuevos
   son tokens declarados. Con ellos el hecho dice lo mismo que dice `domain/sesgo.py`
   (ADR-0044: «Salidas posibles: alcista, bajista, ambiguo e insuficiente»).
2. **RN-003 usa un predicado propio, `sesgo_h4_al_abrir`, en vez de `rompe`.** Declara sus cuatro
   argumentos —`que`, `contra`, `criterio` y **`tope: sesgo_h4_tope_velas`**— porque «todo
   argumento de valor es un nombre del registro» (ADR-0019 §1), y cubre la búsqueda hacia atrás
   de ADR-0044 §2, que `rompe` sobre «la vela H4 previa» no expresaba. Ata en
   `sentido_de_la_ruptura` el lado de la última ruptura o, cuando no hay lado, `ambiguo` o
   `insuficiente`. `rompe` sigue declarado en el vocabulario; ninguna regla lo invoca hoy.
3. **Cada sesión produce SIEMPRE su propio `sesgo` al abrir.** El predicado siempre tiene
   respuesta, así que RN-003 fija el hecho en cada apertura y **ninguna sesión hereda el sesgo de
   la anterior** (ADR-0044 §1 «en esa sesión» y §3 «se fija AL ABRIR»). No hace falta ninguna
   regla que lo borre.
4. **Un gate nuevo, RN-033, prohíbe `buscar_entradas` y `abrir_operacion` con `sesgo` ambiguo o
   insuficiente.** Es la forma ejecutable del «con cualquiera de los dos no se opera» de
   ADR-0044 §1-2, que hasta hoy vivía solo en la prosa de RN-003. Su `cita` sostiene que el
   sesgo alcista solo compra y el bajista solo vende; que sin lado no se opere es decisión
   (ADR-0044), y por eso declara `decision`.
5. **El nodo `hecho` admite `vale`**: `{hecho: sesgo, vale: ambiguo}` es verdadero solo si el
   hecho está fijado a ese valor. Es lo mínimo que hace expresable «con sesgo ambiguo» en el
   árbol de ADR-0019 §6, que solo sabía preguntar si un hecho está encendido. **Amplía ADR-0019**,
   como ADR-0032 §5 lo amplió con `valores`, y la guardia exige que `vale` sea un token declarado
   en los `valores` del hecho.
6. **Las guardias que lo vigilan.** Los `valores` de un hecho tienen que ser tokens declarados.
   El argumento `sentido` de un predicado con `lado_de_ruido` tiene que ser una LIGADURA, nunca
   un token: así `sentido: ambiguo` no pasa, que es el agujero que la spec temía al declarar
   `alcista` y `bajista` fuera de los tokens. Y `lado_de_ruido` sigue nombrando exactamente los
   dos sentidos.
7. **`lado_de_ruido` con `ambiguo` o `insuficiente`: no está definido, y no hace falta.** RN-005
   liga `S` al valor de `sesgo` y `se_desarrolla_en_el_lado_de_ruido` no tiene lado para esos
   dos. No se inventa uno: en esas sesiones RN-033 ya prohíbe lo único que RN-005 prohíbe, así
   que RN-005 no puede decidir nada. Cuando se escriba su primitiva, un `sentido` fuera de
   `lado_de_ruido` es un **error del intérprete, no un valor**.
8. **`sesgo_h4_tope_velas` es PROVISIONAL, y el registro no tiene ese estado.** ADR-0044 §2 lo
   llama «una decisión provisional del proyecto, no del trader» y su descripción en
   `parametros.yaml` ya lo dice con esa palabra. Pero `Estado` es `CONFIRMED`,
   `DEFAULT_AMBIGUOUS` o `UNKNOWN` (ADR-0012, `config/registro.py`): `DEFAULT_AMBIGUOUS` exige
   una ambigüedad del trader que no existe —el tope no es una pregunta para él— y `UNKNOWN` lo
   haría ilegible para el motor. **Se queda `CONFIRMED` con `fuente: decision ADR-0044` y la
   palabra PROVISIONAL en su descripción, que es lo que ya había; crear un estado nuevo del
   registro es un cambio de ADR-0002 y ADR-0012, y queda para el consultor.** No se inventa.

**Los cuatro ajustes de redacción sobre el H1 de ADR-0048**, medidos sobre construcción (42 días,
84 sesiones) el 2026-09-25 y que este ADR recoge en lugar de reescribir aquel:

- Donde ADR-0048 dice «ninguna forma expresa ese "no se opera"», lo concreto es que **la ausencia
  de `sesgo` no frenaba nada**: RN-005 es su único consumidor y solo prohíbe SI el hecho existe.
  Sin el hecho, el bot perdía su único filtro direccional; no quedaba neutral, quedaba más
  permisivo.
- Donde dice «si una sesión anterior del mismo día lo fijó, lo conserva», eso **chocaba con
  ADR-0044 §1** («AMBIGUO en esa sesión»): pasaba en 6 de 84 sesiones, 3 con operaciones del
  trader (4 operaciones).
- Donde dice «ADR-0044 añade la búsqueda hacia atrás», la búsqueda **no estaba en la forma**: se
  ejecutaba dentro de `rompe {que: vela_h4_previa}`, que además leía `sesgo_h4_tope_velas` sin
  nombrarlo, contra ADR-0019 §1. La forma y la primitiva diferían también con salida alcista o
  bajista: en 9 de 84 sesiones (5 de 49 con operaciones) el sesgo venía de una H4 anterior a la
  previa.
- Donde dice «el embudo cuenta esa sesión como sesión sin `sesgo` propio», es cierto, pero el
  embudo mide lo **producido**, no lo **vigente**: en las que heredaban escribía `sesgo:no`
  mientras el estado llevaba alcista o bajista.

### H2 · Qué es una sesión: opción (a)

Las sesiones del motor siguen saliendo de `knowledge/cases/kit/config.yaml` y **un test exige que
cubran exactamente `[ventana_inicio, ventana_fin)`**: contiguas, sin hueco ni solape, la primera
empieza en `ventana_inicio` y la última acaba en `ventana_fin`. Los dos sitios siguen existiendo;
la guardia caza la deriva. **El rango de eventos se queda en 07:00** hasta que responda el
trader: nace **A-43**, no bloqueante, que pregunta si una liquidez tomada antes de las 7 cuenta
para operar después. Afecta a RN-004. A-42 —con qué reloj cuenta las 7— sigue donde está.

### H3 · El orden dentro de una clase: opciones (b) y (c)

El recorrido por id se mantiene. **Un test de invariancia** corre el motor con el orden de cada
clase invertido y exige la misma traza. **Y un aviso en la traza** cuando dos reglas de la misma
clase dan SÍ en la misma pasada de un evento: el intérprete lo registra (`empates`), el motor lo
acumula por sesión y el informe lo lista. Una prioridad explícita queda excluida por ADR-0018.

### H4 · Sin ticks ni bróker: documentado, no construido

- **El gate DESCONOCIDO se mantiene ESTRICTO.** Una acción con efecto que un `gate` DESCONOCIDO
  podría prohibir no se ejecuta (ADR-0048 §2). La consecuencia, que ADR-0048 no decía: hoy diez
  gates están en DESCONOCIDO y prohíben `abrir_operacion` —RN-005, 008, 009, 016, 018, 020, 026,
  029, 031 y 032—, así que **escribir el bróker no basta para que la cobertura pase de 0**: hace
  falta poder evaluar todos esos gates.
- **Sin ticks, el camino intravela será pesimista a partir del OHLC de M1; con ticks, el orden
  real.** Lo fija el ADR del simulador.
- **El bróker y la capa de cuenta se construyen en las ramas del simulador** (Next Action 26 y
  31). Aquí no se toca nada de eso.

### H5 · `permite`: opción (a)

**`permite` nunca levanta un `prohibe`; documenta la ausencia de freno.** Es lo que ADR-0018 §1
implica y lo que las dos reglas que lo usan dicen: RN-017 («un trade ganador no apaga el día») y
RN-021 («el spread no se filtra»). El intérprete lo registra y no cambia nada. La opción (d) —que
un `permite` cuente como «regla de entrada que aplica» para el fallback RN-022— se decide al
escribir `ninguna_regla_de_entrada_aplica`.

### H6 · Estado entre días: opción (c), PROVISIONAL

**La estrategia empieza cada día de cero y la capa de cuenta persiste entre días dentro del
simulador.** Hoy es inofensivo: no hay acumuladores escritos y `sesgo` se recalcula desde las
velas con la búsqueda hacia atrás. El estado de estrategia entre días —cartuchos
(`cartuchos_reinicio: siguiente_liquidez_m15`, RN-016: «el contador NO es diario»), la marca de
liquidez y las órdenes— **queda pendiente de A-25, A-30 y A-38**, y se decide con ellas en el ADR
del simulador.

## Problema que resuelve

ADR-0048 registró seis huecos «y no inventó» ninguno, que era lo correcto en aquella rama. Pero un
hueco registrado sigue siendo un hueco: en cuanto se escriba RN-005 —la siguiente regla en orden
causal tras RN-004— el motor operaría con un sesgo que ADR-0044 dice que no se opera, y en seis
sesiones de construcción filtraría con el sesgo de la sesión anterior. Y sin una decisión sobre
H4 y H6, el ADR del simulador tendría que tomarlas de paso.

El informe de solo lectura del 2026-09-25 lo midió: 15 sesiones AMBIGUAS de 84, 0 INSUFICIENTES,
6 que heredaban y 9 en las que la forma y la primitiva no coincidían. Este ADR cierra lo que se
puede cerrar hoy y deja escrito, con su ambigüedad o su ADR, lo que no.

## Alternativas consideradas

- **H1 (a)** dejar la herencia y documentarla; **(b)** un gate «sin `sesgo` no se opera» más una
  regla que apague el hecho al abrir cada sesión; **(c)** ambiguo e insuficiente como valores del
  hecho, con un predicado propio y un gate (elegida); **(d)** cortar solo la herencia; **(e)**
  esperar a A-34.
- **H2 (a)** test de cobertura exacta (elegida); **(b)** llevar los límites de sesión al registro;
  **(c)** derivarlas de la rejilla de `anclaje_h4`.
- **H3 (a)** dejarlo; **(b)** test de invariancia (elegida); **(c)** aviso en ejecución (elegida).
- **H4** gate DESCONOCIDO estricto (elegida) o un modo de diagnóstico que no bloquee.
- **H5 (a)** documentar que no levanta nada (elegida); **(b)** quitar `permite`; **(c)** lista
  blanca; **(d)** contar para el fallback.
- **H6 (a)** todo de cero, provisional; **(b)** tramos con estado persistente; **(c)** híbrido
  (elegida); **(d)** calentamiento.

## Por que elegimos esta opcion

- **H1 (c) pone en el hecho lo que el dominio ya dice.** Un solo productor, sin herencia, y la
  prohibición es un `gate` que el embudo ve como tal. Cierra además el desajuste entre la forma y
  la primitiva: el predicado nombra el tope que lee.
- **H2 (a) no toca la spec** y caza lo único que hoy puede fallar: que los dos sitios se separen.
  Lo demás depende de A-42 y de A-43, que son del trader.
- **H3 (b) y (c) miden lo que ADR-0018 promete** —que el orden no tenga semántica— en vez de
  suponerlo.
- **H4 estricto** es la alternativa 3 que ADR-0048 rechazó, mantenida a propósito: un gate no
  escrito que dejara pasar inventaría operaciones.
- **H5 (a)** es lo que ADR-0018 §1 implica y no cambia el hash de ninguna regla.
- **H6 (c)** separa lo que ya se sabe —la cuenta persiste, porque la firma mide semanas y un total
  que «no se reinicia nunca»— de lo que el trader no ha dicho.

## Por que descartamos las demas

- **H1 (a)** contradice ADR-0044 §1-2 en cuanto exista RN-005. **(b)** necesita dos reglas
  (apagar y prohibir) porque `entonces` no admite una acción condicionada (ADR-0030), y sigue
  expresando el sesgo por ausencia. **(d)** no frena nada. **(e)** A-34 va en el último bloque de
  la hoja de la sesión 02 y puede quedarse sin preguntar; y INSUFICIENTE no depende de A-34.
- **H2 (b)** toca la spec y el kit para el mismo resultado que el test. **(c)** cambia la unidad
  de etiqueta de ADR-0043 en los 28 días de A-14 sin el trader.
- **H3** prioridad explícita: ADR-0018, alternativa B.
- **H4** un modo que no bloquee es la alternativa 3 de ADR-0048.
- **H5 (b)** enmienda ADR-0019 y cambia el hash sin ganar nada; **(c)** invertiría el sentido de
  RN-021.
- **H6 (b)** exige correr todos los días del tramo y un estado inicial, y con un mes con días
  reservados obliga a declarar por ADR-0033; lo decide el ADR de la medida, no este.

## Impacto

- **`knowledge/spec/strategy_spec.yaml`**: tokens `ambiguo` e `insuficiente`; predicado
  `sesgo_h4_al_abrir`; `hechos.sesgo.valores` y `consume`; la forma de RN-003; RN-033 (gate);
  notas de RN-005 y del predicado `se_desarrolla_en_el_lado_de_ruido`. `spec_version`
  **12.2.2 → 13.0.0**: RN-003 cambia lo que fija y nace una prohibición.
- **`src/botsito/spec/modelo.py`**: `vale` en el nodo `hecho`, `valores` de hecho como tokens, y
  `sentido` como ligadura en los predicados con `lado_de_ruido`.
- **`src/botsito/engine/`**: `vale` en el intérprete; la primitiva `sesgo_h4_al_abrir` sustituye
  a `rompe`; `empates` y el desempate por id (H3); el informe lista los gates disparados por
  sesión y los avisos de H3.
- **`knowledge/spec/ambiguedades.yaml`**: A-43. La hoja de la sesión 02 la lleva justo después
  de A-35.
- **`knowledge/spec/parametros.yaml`**: sin cambios (punto 8 de H1).
- **La línea base del arnés** se vuelve a escribir al lado de la anterior
  (`docs/validation/HUECOS-MOTOR-LINEA-BASE.txt`): cobertura 0, el diagnóstico por operación
  58/12/7 intacto, `sesgo` con valor en todas las sesiones y RN-033 disparado en las 15 ambiguas.
- **Lo que sigue abierto, con dueño**: A-34 (el sentido de la doble ruptura), A-42 y A-43 (el
  reloj y el rango de la sesión), A-25, A-30 y A-38 (el estado de estrategia entre días), el ADR
  del simulador (H4 y la capa de cuenta), y un estado PROVISIONAL del registro si el consultor lo
  quiere.

## Fecha / fase

2026-09-25 · post-F14, rama `trabajo/huecos-motor`. Decisiones del consultor sobre el informe de
solo lectura de la misma fecha. Next Action 29.

## Estado

ACTIVE
