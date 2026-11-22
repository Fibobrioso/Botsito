# ACTIVAR-SESION-08 · La sesión 7b entra en la spec y en el motor, la respuesta de FTMO del 2026-11-20 y la auditoría del 2026-11-21 (R4.3, entrada F)

> PLANTILLA hasta la fase 0: la tabla de activación la escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/activar-sesion-08`, abierta el 2026-11-21 desde `main` en 00e6dc8b (commit de estado
sobre el merge f4b5a9a2 del tag `stable/F39j-sesion-08`). Encargo:
`docs/encargos/trabajo-activar-sesion-08.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
paso (2) de la F de la Next Action). Tag previsto: `stable/F39k-activar-sesion-08` (no existe ni en
local ni en origin: `git tag -l 'stable/F39k*'` y `git ls-remote --tags origin 'stable/F39k*'` vacíos).

```ids-inexistentes
ADR-0097 — el encargo lo manda escribir en F2; sale de este bloque en el commit que lo crea
ADR-0087 — no existe a propósito; lo nombra la auditoría del 2026-11-21 (decisión 0)
```

**Lo que la rama es, con las palabras del encargo:** la 7b salió floja (la dirigió el trader y nadie
hizo la pregunta de cada corrección), así que esta rama activa poco y lo dice.

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `00e6dc8b73c5f19ee228c4a642f6b5e0c78a9b84` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39j-sesion-08^{commit}"` = `f4b5a9a270cebb1de81a9d89cb659fbc26e9e713` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39j-sesion-08` da `ff8f7281…` (el objeto del tag anotado).
- CI de `main`: `gh run view 44978301993` (suelto, sin guion) → `status: completed`, `conclusion: success`, `headSha: 00e6dc8b73c5f19ee228c4a642f6b5e0c78a9b84`, rama `main`. (El auditor anota que ese número no está escrito en `main`: el registro de cierre de F39j solo da los runs de `fix/`; lo dio el encargo y lo comprobé con `gh`.)
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.
- Commit de apertura: `e69bfd05`, sellado (3593 passed, 6 xfailed; `SELLO` sobre el árbol `e24bd1a0`).

## Desviaciones de la apertura

- **La auditoría no estaba en el Escritorio al empezar.** `ls` no la encontró al comprobar la base;
  Aleks la dejó a mitad de la apertura (`C:\Users\USER\Desktop\AUDITORIA-2026-11-21.md`). Tiene
  **377 líneas** (`grep -c ""` y `wc -l`), no 378 como dice el encargo.
- **La orden `--comprobar` del contrato.** El encargo no da la orden y el contrato de la 7a nombraba
  `scripts/generar_capa.py`, que no existe; el contrato lleva la que documenta el propio guion
  (`src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k --comprobar`).
- **La ruta de `PREGUNTAS-7B.md` en `rutas_protegidas`.** El fichero está en
  `docs/sesion-7/PREGUNTAS-7B.md`, no en `docs/validation/` (el encargo, y antes el contrato de la 7a,
  la daban mal). Corregida en el commit de la fase 0.

## FASE 0

Inventario sin tocar código, spec ni knowledge. El auditor (`auditor-encargo`) contrastó el encargo
con el repo (101 afirmaciones: 85 correctas, 1 incorrecta, 15 con matiz, y 10 herencias); lo que
cambia algo va en «El encargo frente al repo», al final de la fase 0.

### 0.1 La tabla de activación

Una fila por fila de la tabla final de `SESION-08-EXTRACCION.md` §6. «Registro hoy»:
`uv run botsito feedback trace <A-n>` da «sin registros de feedback» para A-35, A-13, A-48 y A-58. Los
ítems son los activos (no supersedidos), leídos en `knowledge/evidence/v20/` y `v21/`.

| Fila | Ambigüedad | Ítems activos | Parámetro hoy | Destino del encargo | Lo que veo distinto |
|---|---|---|---|---|---|
| S-1 | A-35 | ev-v20-000138-584fefb5, ev-v20-000138-82b9ab6a, ev-v20-000251-9f6188aa | `liquidez_m15_mecha_que_vuelve` = `solo_la_contraria`, DEFAULT_AMBIGUOUS (`parametros.yaml:595`) | F5: la descripción gana lo citable, sin valor; A-35 ABIERTA | nada |
| S-1, varias velas / el bajo | A-35 | ninguno (tramo no citable) | — | no se activa | nada |
| S-2, pregunta 1 | RN-009 | ev-v20-003023-32448478, ev-v20-003058-8518a5ff, ev-v20-003129-47928a18 | `zonas_control_max_por_esquema` = 1, CONFIRMED (`:1131`) | F5: no se activa; sesión siguiente | nada |
| S-2, el bajo de la toma | RN-009 | ninguno (tramo no citable) | — | no se activa | nada |
| S-2, pregunta 2 | A-13 | ev-v20-002630-6271f57e, ev-v20-002700-955a2dc8, ev-v20-003151-ac4eb016, ev-v20-003753-ec404edc, ev-v20-010844-fa15fbbf | el margen no tiene parámetro | F5: no se activa; A-13 abierta solo por el margen | E21 tiene una segunda parte que no depende de la cifra (A-13 lista `break_even_criterio_ruptura`, ya CONFIRMED): decisión 4 |
| S-3 | A-48 | ev-v20-004617-72d169ee, ev-v20-004750-864a8f1e, ev-v20-004813-a28c4443; del bloque, ev-v21-012348-0582ea84 y ev-v21-020134-6ddd7cd6 | `orden_stop_punto` = `ultimo_pivote_m1`, DEFAULT_AMBIGUOUS (`:753`) | F1: se mide y va a la PARADA | 0.3 y 0.4 |
| S-3, la compra | A-48 | ev-v20-004803-377e65aa | — | F5: nota sin valor | dónde va la nota: decisión 3 |
| S-4, dibujo 1 | A-58 | ev-v20-005440-39656e1f | `sesgo_h4_rango_nuevo` = `vela_que_rompe_con_su_color`, DEFAULT_AMBIGUOUS (`:475`) | F1: PARADA | nada |
| S-4, dibujo 2 | A-58 | ev-v20-005520-80eba002 | el mismo | F5: nota sin valor | decisión 3 |
| S-4, la ruptura por abajo | A-58 | **ninguno** (v20 no tiene ítem de [57:42]–[57:50]) | — | F5: nota sin valor | sin ítem no se cita (regla del encargo): decisión 3 |
| S-4, siempre en H4 | A-58 | ev-v20-005723-f1eff54a | — | F5: nota sin valor | decisión 3 |
| S-5 | S-22 | ev-v20-010049-b400e914 | sin parámetro (ADR-0085 §3) | F3: no se activa | nada |
| S-5, sin pasar ningún mínimo / con la mecha | S-22 | ev-v20-010049-4cb7f481, ev-v20-010049-12e69e6d | — | F3: no se activan (la tabla final las da «resuelve») | nada |
| S-6 y S-6 si el precio vuelve | S-19 (sin ambigüedad) | ev-v20-010243-21636d5f, ev-v20-010354-ada60dca; de la sesión 6, ev-v17-014103-8cf3e7fb, ev-v17-014235-f3375358, ev-v17-014350-ec133d13 | sin parámetro | F2: regla nueva bajo A-59, DEFAULT_AMBIGUOUS, ADR-0097 | [63:44] no tiene ítem: lo citable de «solo toca esperar» es ev-v20-010354-ada60dca (1:03:54-1:03:59) |
| S-7 | VIDEO-JULIO.md | ev-v20-011213-947092b6 | — | F5: recuadro en VIDEO-JULIO.md | nada |
| Sesión 1 del bloque | — | ninguno (no citable) | — | nada | nada |
| Sesión 2 del bloque (04-15) | — | ev-v21-005504-e34f514d, ev-v21-005523-e4941a17 | — | ejemplos; 0.4 | operada tras abrir sus láminas (no a ciegas) |
| Sesión 3 del bloque (04-27) | — | ev-v21-012348-0582ea84, ev-v21-012455-6eb57ef2, ev-v21-012623-bbdaf48a | — | ejemplos, salvo [86:23] (F4); 0.4 y 0.6 | nada |
| Sesión 4 del bloque (01-19) | — | ev-v21-013735-a127e031, ev-v21-014454-7eb03316, ev-v21-014835-7e7bcd41, ev-v21-015148-54dd1a0c | — | ejemplos; 0.4 | nada |
| Reserva del bloque (01-21) | — | ev-v21-015933-c05aad41, ev-v21-020134-6ddd7cd6 | — | ejemplos; 0.4 | nada |

Reloj: ninguna respuesta trae horas. Premisas: siguen vigentes las de las siete preguntas.

### 0.2 El control de D0

Las tres órdenes del recuadro del 2026-11-18 de ADR-0093 §4, sueltas, sobre `e69bfd05` (el motor de
`main`: `git diff --stat stable/F39e-activar-sesion-07 main -- src/` solo da
`src/botsito/corpus/cuarentena.py`; ninguna rama posterior a F39e tocó el motor, y sus registros de
cierre en HISTORIA lo dicen; el auditor añade que be4684d2, dentro de la propia 7a y después de su
corrida F2, tocó solo comentarios y textos de `arnes.py`, `primitivas.py` y la spec).

- `motor arnes --simular --meses 2026-07` → `data/activar-sesion-08/julio-base.txt` (80,3 s, pico 154 MiB).
- `pivote_julio.py` → `anexos/ACTIVAR-SESION-08/pivote-julio-base.txt`: **T0 11; P5 17 (15 mismo lado,
  2 otro lado); P6 en sesión 2; operaciones de más 19; P1 1, P2 8, P3 14, P4 29, P7 4**. Idéntico,
  cifra a cifra, a `anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`.
- **Fila por fila**: `data/activar-sesion-07/patrones-julio-f2.txt` sigue en la laptop, así que la
  comparación es completa. `delta_julio.py` (F2 de la 7a → base de esta rama) →
  `anexos/ACTIVAR-SESION-08/delta-julio-f39e-base.txt`: 86 filas y 86, **0 cambian de patrón, 0
  aparecen, 0 desaparecen; 25 sesiones y 0 cambian de rn003**. Y las dos salidas de `patrones.py`
  solo difieren en su primera línea, que nombra el fichero (`diff` de las demás: 0 líneas).
- **El control REPRODUCE.** El delta de la base contra la línea base de `PIVOTES-SESION-7.yaml` (14 y
  39): parejas −3, operaciones de más −20; contra el control: 0 y 0.

### 0.3 F1, S-3: el esquema como velas sintéticas

Sin abrir ningún fotograma. Guion de la carpeta de trabajo de la sesión (no está en el repo), con
velas inventadas y las funciones de `main` (`ultimo_punto_de_ruptura`, `extremo_de_la_caja`,
`pivotes_de_control`). El esquema, según `docs/sesion-7/PREGUNTAS-7B.md:219-222`: «la toma de M15 en
una venta; después el retroceso en M1 con su último pivote; la vela de la toma, con su propio pivote
en otro sitio; dos posibles 0 rotulados A (el último pivote de M1) y B (el de la vela de la toma), y
el 1 dibujado igual para los dos».

**Lo que he tenido que suponer** (el PDF está fuera del repo): una venta con nueve velas —una subida
con un retroceso pequeño (que deja un BAJO antes de la toma), la vela de la toma, dos velas de impulso
bajista, el retroceso alcista de dos velas (la zona de control) y una vela que vuelve a bajar—; que la
primera vela del retroceso tiene una mecha por debajo del mínimo de la racha bajista; y una segunda
variante con una vela roja DENTRO del retroceso (estructura interna). Las cifras son puntos inventados.

| Variante | `ultimo_pivote_m1` (A, hoy) | `referencia_de_la_toma` (B) | Punto más bajo de la zona de control | Zonas de control que cuenta el motor |
|---|---|---|---|---|
| retroceso limpio | 0 = 935 (el mínimo de la racha bajista; 1 = 978) | 908 (el BAJO de antes de la toma) | 932 con la mecha de la vela que abre el retroceso; 935 sin ella | 1 |
| con estructura interna | 0 = **948** (el BAJO interno) | 908 | 932 / 935 | **2** |

**Lectura:** con el retroceso limpio, `ultimo_pivote_m1` cae en la base de la zona de control: es «el
punto más bajo de la zona de control que valida» (§3.3 de la extracción), salvo la mecha de la vela
contraria, que hoy no mueve el nivel (`no_mueve` en M1). Con estructura interna, el bot pone el 0 en
el pivote interno, más arriba, que es lo que el trader corrige en el bloque («eso es estructura
interna … de la zona de control que aquí no nos sirve», ev-v21-020134-6ddd7cd6), y además cuenta dos
zonas de control, con lo que RN-009 (tope 1) invalida el esquema. `referencia_de_la_toma` no coincide
en ninguna. Es una medida sobre un esquema inventado: dice qué lectura PUEDE casar, no cuál es la suya.

### 0.4 F1, las cuatro sesiones del bloque con `motor decisiones`

`motor decisiones --meses 2026-01,2026-04 --bitacora 2026-01-19,2026-01-21,2026-04-15,2026-04-27`
sobre `e69bfd05` (fila de HOLDOUT del día), en `data/activar-sesion-08/decisiones-base/`. La bitácora
dice qué punto (el 0) y qué caja (el 1) ligó el bot en cada cierre y qué orden colocó; **no dice a qué
punto de la lámina señalaba el trader**, y la extracción tampoco: en ninguna de las cuatro dice en voz
la caja, el 0 ni el 0,8 (§4.2-§4.5). Así que la comparación es de forma, no de nivel. Recuentos por
sesión (sin precios en el repositorio):

| Sesión | Tomas | Puntos distintos (vela contraria) | Cajas ligadas | Órdenes | Cierres prohibidos por RN-009 | Lo que la extracción dice que él pondría |
|---|---|---|---|---|---|---|
| 2026-04-15, 11-15 | 3 | 58 | 124 | 15 (stop, compra; todas colocadas) | 18 | «sería desde aquí … desde la zona de control interna de toda … el trazo desde allí no desde» ([63:42]–[64:56]; sin ítem propio) |
| 2026-04-27, 11-15 | 2 | 41 | 77 | 2 (colocadas) | 7 | el 0 «en ese alto», porque lo que tomó el bot «forma parte de [la zona] de control» (ev-v21-012348-0582ea84) |
| 2026-01-19, 11-15 | 2 | 51 | 107 | 4 (colocadas) | 9 | la caja hasta la vela de mecha mayor (ev-v21-014835-7e7bcd41; el 1, no el 0) |
| 2026-01-21, 07-11 | 2 | 50 | 100 | 8 (stop, venta; colocadas) | 6 | la caja desde el punto breaker más reciente, sin la estructura interna de la zona de control (ev-v21-015933-c05aad41, ev-v21-020134-6ddd7cd6) |

**Lectura, sin decidir:** en las cuatro el bot mueve el 0 a cada pivote nuevo de M1 (de 41 a 58 puntos
distintos por sesión, con `ultimo_pivote_m1`), también a los que forma el propio retroceso; las tres
correcciones del 0 dicen que el 0 no va en la estructura interna de la zona de control sino en su
extremo o en el punto breaker más reciente que la deja atrás. Es lo mismo que separa las dos variantes
de 0.3. La de 01-19 corrige el 1, no el 0 (`caja_bloque` = `r6` está CONFIRMED). Además, el
2026-04-27 de 07 a 11 (no es la sesión de la tabla) la primera orden del bot sale rechazada por
`precio_invalido`: un caso de S-19 en el bloque.

### 0.5 F2, S-19: el estado de hoy

**Dónde se rechaza y dónde se gasta** (líneas de hoy):
- el bróker rechaza la stop del lado equivocado en `Broker._precio_infringido`
  (`engine/broker.py:558-576`), que llama a `lado_equivocado` (`engine/llenado.py:274-283`) con la
  cotización de `Mercado.cotizacion(instante, spread_supuesto)` (`broker.py:565`); el rechazo se
  registra y cuenta como petición (`broker.py:541-549`);
- en `colocar_orden_limite` (`engine/primitivas_broker.py:611-663`) la caja queda usada ANTES de mirar
  el resultado (`marcar_usada`, `:656`) y, si es `Rechazo`, el punto se gasta (`marcar_rechazada`,
  `:661`, con el comentario «el rechazo al colocar gasta el punto (ADR-0083, D1; la decision 1 de
  ADR-0064)»);
- los tres llamadores de `marcar_rechazada` (`engine/zonas.py:420-427`): `primitivas_broker.py:641`
  (el no envío por el lote, ADR-0081), `:661` (el rechazo al colocar) y `engine/cableado.py:189` (el
  rechazo al llenar). Son los mismos tres que contó ACTIVAR-SESION-06-MOTOR.md §d, con las líneas
  desplazadas.

**Qué ADR lo sostiene y qué descartó.** ADR-0083 D1 (`docs/adr/0083-que-gasta-un-punto.md:24-30`, la
lista «Gasta el punto», con «precio inválido» en el primer guion), PROVISIONAL, que conserva para el
rechazo la decisión 1 de ADR-0064 (`0064-…md:84-86`: «Si el precio ya pasó el punto al colocarla, se
rechaza una vez y no se reintenta en cada M1, que llenaría el contador de peticiones (R13)»).
Alternativas descartadas: ADR-0083 (`:196-214`) consideró la decisión 1 al pie de la letra, D1 y
dejarlo como estaba; ninguna es «no enviar». ADR-0064, decisión 1, es una DECISIÓN sin alternativas:
lo que descarta es REINTENTAR (con petición) en cada M1. ADR-0056 §3 y ADR-0057 (alternativa 2:
«seguir llenándola a su precio, convertirla en orden a mercado, o rechazarla», `0057-…md:107-108`)
deciden qué hace el BRÓKER con una pendiente del lado equivocado, no si el bot la envía. **Ningún ADR
descarta expresamente no enviar.**

**Qué tests lo congelan:** `tests/unit/test_punto_usado.py:343`
(`test_el_rechazo_al_colocar_sigue_gastando_el_punto`, por el cableado real); con la orden stop y el
precio ya roto, `tests/unit/test_cableado.py:654` (`…_la_orden_se_rechaza`) y
`tests/unit/test_vida_de_la_orden.py:121` (`test_una_orden_rechazada_sale_con_el_motivo_…`);
`tests/unit/test_broker_ordenes_stop.py` prueba el bróker solo y no cambia.

**Ninguna ambigüedad abierta cubre S-19**: las abiertas son A-13, A-16, A-35, A-43, A-48, A-53, A-54,
A-55, A-56 y A-58 (leídas de `ambiguedades.yaml`); A-53 es la orden sin llenar cuando el precio toma
OTRA liquidez de M15.

**La condición se puede comprobar antes del envío con lo que el motor tiene en ese cierre:**
`colocar_orden_limite` tiene el bróker (`ctx.broker`), el instante (`ctx.instante_ms`), el lado y la
entrada; la comprobación sería la misma `lado_equivocado` con la misma `Mercado.cotizacion` que usa
`_precio_infringido`, expuesta por el bróker sin duplicar su lógica. **La vela que mira**, medida en
`llenado.py:99-119` y en la deuda «Las cotizaciones sin tick del bróker no usan la misma vela»: en el
cierre de la M1 k el instante es `k·60000 − 1`; con ticks, el último tick anterior o igual; sin ticks,
la M1 **k−1** (la última CERRADA antes del instante), no la k que acaba de cerrar. Es la misma
cotización con la que rechaza el bróker, que es lo que pide el encargo.

**La corrida base de julio** (`julio-base.txt`, «Rechazos por motivo» y «### Ordenes»): **5 rechazos,
todos `precio_invalido` al colocar, en 3 sesiones**: 2026-07-06 de 07 a 11 (1), 2026-07-08 de 11 a 15
(1) y 2026-07-10 de 07 a 11 (3). Ninguno al modificar ni al llenar. El día con más peticiones es el
2026-07-02 (45; tope de la firma, 2000).

**CUADRA** (los cuatro criterios del encargo se cumplen). **Filas declaradas antes de correr con el
cambio** (ADR-0093 §4): las de las sesiones **2026-07-06 07-11, 2026-07-08 11-15 y 2026-07-10 07-11**.
Casa si, tras F2: (i) en julio no queda ningún rechazo por `precio_invalido` al colocar; (ii) cada
fila de julio que cambie de patrón es de una de esas tres sesiones o se explica, una por una, por los
intentos o por un freno de la cuenta; (iii) las peticiones del 2026-07-02 no suben de 45. Cuántas
pasan a pareja no se declara.

**El parámetro que propongo:** `orden_stop_lado_malo`, `categoria: estrategia`, `tipo: enum`,
opciones `[se_gasta_el_punto, espera]`, DEFAULT_AMBIGUOUS en `espera` bajo A-59. Su fuente,
ev-v20-010243-21636d5f (la frase de la 7b).

**Lo que más toca F2 y el encargo no nombraba** (auditor, H1): la descripción de
`toca_colocar_orden_limite` (`strategy_spec.yaml:280-297`) dice «gasta el punto el rechazo del broker
(al colocar o al llenar)», que con F2 deja de ser cierto en este caso; cambia en el mismo commit, con
`spec_version`, `spec manifest --escribir` y `spec docs --escribir`; y los docstrings de
`zonas.py:41-46` y los comentarios de `primitivas_broker.py:629-631` y `:657-659`.

### 0.6 F4, la zona de control pide una vela contraria

**El recuento sobre la construcción** (guion de la carpeta de trabajo; las M1 de enero, abril, julio
y agosto de 2026, cada mes solo): `_pivotes_m1`, la función de la que salen las zonas de control
(`pivotes_de_control`, `estructura_m1.py:153-171`), forma **28.822 BAJOS y 28.821 ALTOS; 0 sin una
vela contraria al impulso en su racha** (por mes: enero 7.103 y 7.104, abril 7.363 y 7.362, julio
7.579 y 7.579, agosto 6.777 y 6.776; 0 en todos). Y por construcción: `_pivote_en`
(`pivotes_m15.py:180-196`) solo da pivote en una vela con color cuya racha anterior es del color
contrario (`_racha_anterior(..., -signo, ...)`), y una vela sin cuerpo nunca es contraria; una zona de
control de una compra es un BAJO, que exige una racha de velas rojas. **El motor ya lo cumple.**

**Lo que enseñaba la lámina** que corrige en v21 [86:06]–[87:20] (sesión 3, 2026-04-27 de 11 a 15):
la bitácora de esa sesión da 2 tomas (12:17 y 13:41, hora de Madrid), 2 órdenes y RN-009
prohibiendo desde las 12:27 (10:27Z) en 7 tramos; la bitácora apunta el gate y no las velas, así que
las calculé con las funciones de `main` (`pivotes_de_control` sobre las M1 de abril, tras la toma de
las 12:17; fila de HOLDOUT del día): desde el cierre de las 10:23Z hay 1 zona de control (un BAJO
cuya racha son **2 velas rojas**) y desde el de las 10:27Z, 2 (la segunda, también tras **2 velas
rojas**); con el tope de 1, RN-009 invalida. Las dos zonas que contó el bot tienen vela contraria.
**Qué vio él como zona sin vela roja no lo dice nada de lo que se puede mirar:** la lámina no se abre
(fotogramas del bloque) y su frase no nombra la zona. Lo probable, sin medir: que leyera como «zona» la
caja de una orden, que R6 traza desde el punto por velas del impulso; es lo que la decisión 7 deja al
consultor.

### 0.7 F6, FTMO del 2026-11-20

**Dónde vive cada texto que F6 actualiza** (el modelo, RESPUESTAS-FTMO.md §0.d):
- `docs/validation/FTMO-REGLAS.md` (informe cerrado, recuadros): R13 en la tabla del §2 (`:60`); el
  recuadro del 2026-10-05 con la respuesta del ticket VDW-DPMWR-965 (`:217-246`); el §4 «Lo que queda
  abierto» (`:283-310`), con R13 en «PARA EL CONSULTOR» (`:299-300`).
- `docs/validation/RESPUESTAS-FTMO.md` (informe cerrado): el recuadro va al principio.
- `knowledge/spec/ambiguedades.yaml`, A-54 (`:1823-1863`): `pregunta` en `:1825-1836`; `medicion`, no
  bloqueante, ABIERTA. La tabla de Known Ambiguities no cambia.
- `knowledge/spec/parametros.yaml`: `freno_peticiones_aviso` (`:1983`), `freno_peticiones_corte`
  (`:2001`), `freno_bucle_repeticiones` (`:2019`) y `freno_bucle_minutos` (`:2036`), los cuatro
  DEFAULT_AMBIGUOUS bajo A-54. Están en ENTRAN de `generar_capa.py` (`:74`, `:89-92`), pero `_parametros`
  (`:273-288`) no escribe la descripción: cambiarla no cambia `Generado.mqh` (se comprueba con
  `--comprobar` en su commit).
- `docs/adr/0082-…md` §4 (D4, `:71-89`), con recuadro.

**Qué dice hoy A-54**: pregunta tres cosas —«¿cuenta una petición rechazada, una modificación del
stop, una cancelación y un cierre?; ¿con qué reloj corta FTMO ese día?; ¿qué hace el servidor al
pasarse?»— y dice que se preguntó el 2026-10-03 y se respondió en parte el 2026-10-05.

**Lo que sigue sin respuesta tras el 2026-11-20**, contra el recuadro del 2026-10-05
(`FTMO-REGLAS.md:227-230`): el reloj está contestado desde el 2026-10-05 (00:00 CE(S)T, pregunta 4);
el 2026-10-05 dijo que «todo tipo de orden cuenta» sin distinguir rechazadas, modificaciones,
cancelaciones ni cierres; la paráfrasis del 2026-11-20 nombra abrir, cerrar y modificar (incluido
mover el stop o el objetivo) y que las lecturas no cuentan. **Sigue sin respuesta:** si una petición
RECHAZADA cuenta y si una CANCELACIÓN cuenta por separado (la del 2026-11-20 no las nombra), y qué
hace el servidor al pasarse (nunca se preguntó por correo: solo está en A-54). Coincide con la
lectura del encargo.

**El id que sirve de fuente**: el 2026-10-05 los commits que tocaron `knowledge/spec/` llevaron
`Fuente: ADR-0067, ADR-0068` (0e1457c7), los ADR del freno y de los cierres; aquí, `ADR-0067` (el
freno, que es lo que A-54 y los cuatro `freno_*` regulan) y `ADR-0082` (D4).

**D4 de ADR-0082 y sus razones** (`0082-…md:71-89` y `:203-210`):
- la capa es el EA porque el bot final es un EA (F29-F31; ADR-0001:20-21): una capa en Python habría
  que tirarla al llegar F29 (`:75-77`);
- de las cuatro razones de la investigación (`:78-85`): el tope de 2.000 peticiones vale en FTMO y «un
  bucle de Python que sondea gasta presupuesto; el EA reacciona a `OnTick`» (`:80-82`); el Strategy
  Tester y el VPS sin puente no tienen cita de FTMO (`:83-84`); la equivalencia entre dos
  implementaciones es la de F30 (`:85`);
- responde a BRECHA-EN-VIVO.md §1: se descarta el EA que recibe las decisiones de Python porque
  «exige un puente en vivo que choca con el tope de peticiones» (`:86-89`).
- Descartadas (`:203-210`): (1) deja esperando sin motivo de fidelidad lo que solo la demo puede medir;
  (2) una lista no dice qué hacer con lo que no está en ella; (3) «El bot final es un EA (F29-F31): la
  capa habría que tirarla al llegar F29 (D4)»; (4) «Exige un puente en vivo que choca con el tope de
  peticiones (D4)».
- **Lo que la respuesta del 2026-11-20 toca:** quita la razón del tope en (4) y en la primera de las
  cuatro razones (`:80-82`, el sondeo gasta presupuesto: las lecturas no cuentan) y deja en pie la
  razón de (3) y de `:75-77` (el bot final es un EA), las dos sin cita de FTMO (`:83-84`) y la de F30
  (`:85`). Eso es lo que copia el recuadro, sin añadir.

### 0.8 F7, el panel de FTMO y el campo bloqueante

**Los cuatro textos del panel** (la línea de Technical Debt, entera en `HISTORIA.md:16690`; el panel
quedó declarado el 2026-11-07, `HISTORIA.md:15579-15585`: el aviso de MetriX restablecía la pérdida
hacia las 00:00 de España, no a la medianoche del servidor):
- `docs/runbooks/DEMO-FTMO.md:159-162` («**Pendiente, sin ejecución:** mirar en el panel…»): runbook,
  se edita;
- la descripción de `reloj_dia_riesgo` (`parametros.yaml:1690`; el texto pendiente en `:1707-1711`, no
  en `:1646-1651` como dice la línea de Technical Debt): spec, se edita con `spec docs --escribir` y
  trailer; `reloj_dia_riesgo` está en ENTRAN, pero la descripción no entra en `Generado.mqh`;
- `docs/adr/0090-…md` §1 (`:71-77`): ADR, recuadro;
- `docs/validation/FTMO-REGLAS.md:253-254` («Lo que A-28 pedía era verlo además en el panel»): informe
  cerrado, recuadro.

**Qué lee el campo `bloqueante`** (para A-35):
- código: `cases/ambiguedades.py:45,90,169-170,218` (lo carga y valida); `cases/cuestionario.py:132`
  (las bloqueantes primero en el cuestionario); `cases/hoja_docx.py:381,510,544` y `cases/paquete.py:482`
  (la marca BLOQUEANTE en la hoja); `cases/spec_docs.py:250` (la marca en `docs/spec/`);
  `validation/knowledge.py:845-848` (una bloqueante no se puede cerrar por decisión del consultor);
- el MOTOR no lo lee: `engine/diagnostico.py:105-127` se niega a correr si `liquidez_m15_pivote_formado`
  está UNKNOWN, que es otra cosa (CONFIRMED desde ADR-0045);
- tests: `tests/unit/test_kit.py:373-380` (`assert abiertas == {"A-35"}`) y `:501-504` (la columna de la
  tabla de PROJECT_STATE);
- documentos: la tabla de Known Ambiguities (`PROJECT_STATE.md:68`, «si»), la línea de Technical Debt
  de A-35 (`:139`, «sigue ABIERTA y bloqueante») y la descripción de `liquidez_m15_pivote_formado`
  (`parametros.yaml:566`, «BLOQUEANTE de RN-004», E20).

### 0.9 Lo que se hereda, y los choques

**Herencia** (skill activar-sesion, «Entradas»): la F de la Next Action manda (2) esta rama y (3) la
corrida; R4.3 «Hecho cuando» dice «La deuda del panel de FTMO y A-16 la paga la activación de 7b»
(F7.2 y F7.3); la Technical Debt de A-35 tras la 7b; la de las cotizaciones sin tick (la vela de 0.5);
«Dos textos que ADR-0093 deja viejos» (`engine/decisiones.py:7-8`, que F2 hace más viejo: H6 del
auditor); la nota de RN-019 que cita A-31, RESUELTA (H5); `test_kit.py:706-707` (H7, si A-59 toca ese
fichero); y de ACTIVAR-SESION-07.md:684, «antes de (3), el consultor decide qué hacer con los frenos de
la cuenta del mes (RN-032 y RN-036)» (H10), que no está en «Para la corrida de (3)» del encargo.

**Choques de las decisiones con un ADR o con una respuesta anterior:**
- F2 con la respuesta del consultor del 2026-11-06 (decisión 3: «(c) hasta la sesión 7, con mi lectura
  apuntada: si el trader dice "espero", 3.a y 4.a»): no choca, la cumple; el encargo lo declara.
- F2 con ADR-0083 D1 y con la decisión 1 de ADR-0064: los enmienda en un caso; ADR-0097 con recuadro en
  los dos, como manda el encargo.
- F3 con el recuadro del 2026-11-05 de ADR-0085 §3: la «rama de motor» a la que mandaba la condición
  era `trabajo/activar-sesion-06-motor` (ACTIVAR-SESION-06.md, «Para la rama de motor»), que la dejó
  en PARADA, y el consultor la mandó «a la sesión 7 … y después en rama propia»
  (ACTIVAR-SESION-06-MOTOR.md:791). Que «esa rama es esta» es cierto por ese camino; el recuadro lo
  dirá así.
- F7.1 con la guardia de ids: abajo, decisión 0.

### El encargo frente al repo (auditor y lo medido)

1. **F7.1 no se puede hacer tal como está escrita.** La auditoría cita `ADR-0087` (que no existe, a
   propósito) en su línea 248 («| 96 | ADR-0087 en ids-inexistentes |…»), fuera de un bloque
   `ids-inexistentes`. `validation/ids_citados.py` revisa todo `docs/**` dentro de `knowledge validate`
   y solo exime un id declarado EN EL PROPIO DOCUMENTO. Copiada tal cual no sella. **No la he copiado**:
   decisión 0.
2. **F5 choca con F1** en las notas de S-3 y S-4: el precedente de «notas que no fijan valor» es la
   descripción del parámetro (ACTIVAR-SESION-07.md:621-624), que F1 prohíbe tocar
   (`orden_stop_punto`, `sesgo_h4_rango_nuevo`, A-48 y A-58); el feedback no tiene acción de nota
   (`feedback/modelo.py:37-51`); y «la ruptura por abajo» no tiene ítem de evidencia (la evidencia está
   protegida). Decisión 3.
3. **«PICO DE MEMORIA en la última línea del log»** es la última línea de TODO `make check` que termina
   (`scripts/pico_memoria.py:186`); la señal de que lo cortó la memoria es «system running low on
   memory» (CLAUDE.md, «Trampas medidas»). Uso esa.
4. **PROJECT_STATE.md cambia también en «Tests Currently Passing»** (F2 y F4 añaden tests, y `state
   check` exige el recuento real), además de la tabla de Known Ambiguities.
5. **La vía del WhatsApp** (F1 y A-35): `knowledge/corpus/` está entera en `rutas_protegidas` y lo
   protegido manda; añadir `knowledge/corpus/fuentes.yaml` a las permitidas no basta: hay que sacarla
   de las protegidas en ese commit. Y la guardia no deja abrir una imagen del material adicional: la
   sesión necesita el texto de la respuesta.
6. **E21** tiene una parte que no depende de la cifra (decisión 4).
7. **F3 y el 52 %**: el 52 % es con la lectura (a); con la (b), 69 % (ACTIVAR-SESION-06-MOTOR.md:154).
8. **F2 y ADR-0057 §4** (auditor, H8): ADR-0097 dirá qué vela mira la comprobación (la misma
   `Mercado.cotizacion`, que ya describe ADR-0057 §4); no cambia ADR-0057, así que no lleva recuadro ni
   entra en el contrato.
9. **La auditoría y el ADR de la meta de marzo** (su §3: «Y el ADR de las opciones de §1, si Aleks lo
   quiere antes de la corrida»): el encargo no lo pide y prohíbe declarar otro ADR; no se hace.

### Lo que no pude medir

- La paráfrasis de FTMO contra el correo: el correo no está en el repo, y la fuente es la paráfrasis.
- Si el trader ha contestado al WhatsApp del 2026-11-21 (A-35, A-43, S-3): nada ha llegado a la rama.
- Qué enseñaba la lámina, más allá de la bitácora: las láminas no se abren (están fuera del repo y son
  fotogramas del bloque).

### Exposiciones declaradas

Las dos filas de `HOLDOUT-EXPOSICIONES.md` del 2026-11-21 de esta rama (la apertura y la fase 0; el
control de D0, los `motor decisiones` y las medidas de 0.3 y 0.6), escritas antes de leer o correr.

## Lo que necesito que decidas

0. **F7.1, la auditoría con `ADR-0087`.** Opciones: (a) copiarla con una cabecera propia, como los
   encargos (un título, una línea de procedencia y el bloque `ids-inexistentes` con «ADR-0087 — la
   auditoría lo nombra a propósito: el 0087 no existe»), y el texto de la auditoría debajo, sin tocar
   ni una línea; (b) que Aleks corrija su fichero; (c) dejarla fuera del repo. Recomiendo (a): es el
   régimen de los encargos («copia literal» con su bloque delante) y el cuerpo queda intacto. Coste de
   (b): deja de ser la auditoría entregada.
1. **F1, S-3 (A-48)**: lo de 0.3 y 0.4. Opciones: (a) dejar `ultimo_pivote_m1` y pasarlo a CONFIRMED;
   (b) una opción nueva («el punto más bajo de la zona de control», sin la estructura interna) con su
   ADR; (c) a la sesión siguiente con la pregunta reformulada sobre un día real («¿dónde está el punto
   más bajo de tu zona de control aquí?», con el trader señalando en la lámina). Recomiendo (c),
   esperando antes la respuesta por WhatsApp: 0.3 enseña que A y «el punto más bajo» coinciden con el
   retroceso limpio y se separan con estructura interna, y cuál de las dos es la suya no lo dicen sus
   palabras. Coste de (a): fija un valor que el bloque corrige como ejemplo («sin la estructura
   interna»).
2. **F1, S-4 (A-58)**: el dibujo 2 es la lectura d) de ADR-0094, que ya es la de hoy; el dibujo 1 es
   la b), sin confirmar con palabras. Opciones: (a) `sesgo_h4_rango_nuevo` sigue DEFAULT_AMBIGUOUS y A-58
   ABIERTA solo por el dibujo 1, que va a la sesión siguiente («cuando la vela rompe y cierra de su
   color, ¿tu rango nuevo va del alto al bajo de esa vela?», sobre una H4 real); (b) pasarlo a
   CONFIRMED. Recomiendo (a): «otra» en los dos y «no sé» en [54:23].
3. **Las notas de F5 de S-3 y S-4.** Opciones: (a) solo en el informe, en «Lo que dijo y no fija nada»,
   sin tocar la spec, hasta que F1 se decida; (b) en la descripción de los dos parámetros, como en la
   7a, levantando para eso la prohibición de F1; (c) un ítem de evidencia nuevo para la ruptura por
   abajo, que esta rama no puede crear (evidencia protegida). Recomiendo (a), que es lo que hago
   mientras tanto.
4. **E21, la parte que no depende de la cifra**: A-13 sigue listando `break_even_criterio_ruptura`,
   CONFIRMED, en su campo `parametros`. Opciones: (a) dejarlo; (b) quitarlo en esta rama (toca
   `ambiguedades.yaml`; con `spec docs`). Recomiendo (a) aquí y que lo lleve la orden de cierre o la
   rama del margen: ese parámetro lo cerró la 7a como parte de A-13.
5. **F7.4, A-35 y `bloqueante`**: con lo de 0.8. Opciones: (a) `bloqueante: false`, porque el motor ya
   corre con un valor por defecto declarado (RN-004 VIGENTE; `liquidez_m15_mecha_que_vuelve`
   DEFAULT_AMBIGUOUS) y nada del motor lee el campo; cambian `ambiguedades.yaml`, la tabla de
   PROJECT_STATE (columna «si» → «no»), `test_kit.py:380` (el conjunto pasa a vacío y su comentario), la
   descripción de `liquidez_m15_pivote_formado` («BLOQUEANTE de RN-004») y la línea de Technical Debt de
   A-35; (b) dejarla. Recomiendo (a): «bloqueante» marca lo que hay que llevar sí o sí a una sesión
   (`test_kit.py:347`), y A-35 ya va por WhatsApp; lo que la mantiene viva es estar ABIERTA.
6. **H10, los frenos de la cuenta del mes antes de (3)** (ACTIVAR-SESION-07.md:684): lo dejo en «Para
   la corrida de (3)» como pendiente del consultor, salvo que lo dé por cubierto por la contingencia del
   2026-11-19.
7. **F4, qué leyó él como zona.** El motor ya lo cumple (0 de 57.643 pivotes sin vela contraria; las
   dos zonas de 2026-04-27 de 11 a 15, con dos velas rojas cada una), así que F4 cuadra en su
   criterio y entra el test que lo congela, sin tocar el motor ni RN-009. Lo que no puedo medir es
   qué enseñaba la lámina que él leyó como zona: si era la caja de una orden, lo que corrige es cómo
   se DIBUJA, no la regla. Opciones: (a) dejarlo así y preguntarlo en la sesión que él pidió sobre las
   zonas de control («en esta lámina, ¿qué es lo que ves como zona de control?»); (b) revisar las
   láminas de esa sesión con Aleks, que puede abrirlas. Recomiendo (a) con (b) si Aleks quiere: no
   cambia nada del motor. Régimen para dejar constancia sin tocar RN-009: una línea en la lista de la
   sesión siguiente y en este informe; ningún registro de feedback, como manda el encargo.

## Cómo sigue la rama sin esperar (PARADA condicional del encargo)

F1 va siempre a la PARADA. F2 CUADRA y F4 cuadra en lo medido (con la decisión 7 abierta): se hacen. F3, F5 (salvo las notas de
S-3 y S-4, decisión 3), F6 y F7.2, F7.3, F7.5, F7.6 y F7.7 no dependen de ninguna decisión de arriba y
se hacen. F7.1 (decisión 0) y F7.4 (decisión 5) esperan.

## Estado

EN CURSO: fase 0 escrita; sigue con las fases que cuadran.
