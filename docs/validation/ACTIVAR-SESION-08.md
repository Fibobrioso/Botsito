# ACTIVAR-SESION-08 · La sesión 7b entra en la spec y en el motor, la respuesta de FTMO del 2026-11-20 y la auditoría del 2026-11-21 (R4.3, entrada F)

Rama `trabajo/activar-sesion-08`, abierta el 2026-11-21 desde `main` en 00e6dc8b (commit de estado
sobre el merge f4b5a9a2 del tag `stable/F39j-sesion-08`). Encargo:
`docs/encargos/trabajo-activar-sesion-08.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
paso (2) de la F de la Next Action). Tag previsto: `stable/F39k-activar-sesion-08` (no existe ni en
local ni en origin: `git tag -l 'stable/F39k*'` y `git ls-remote --tags origin 'stable/F39k*'` vacíos).

```ids-inexistentes
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

## F2 · S-6 (S-19): la orden cuyo 0 queda del lado malo espera (ADR-0097)

**Con las palabras del encargo:** «DESVIACIÓN DECLARADA de "en parte no se cierra" y de "solo se
activan las reglas generales" (R4.6): no cierro nada. Cambio un comportamiento de ejecución que las
dos sesiones contradicen y lo dejo como LECTURA DEL CONSULTOR, bajo un parámetro DEFAULT_AMBIGUOUS y
una ambigüedad nueva que queda ABIERTA, como se hizo con ADR-0084 y ADR-0094.»

Cuadró en la fase 0 (0.5). Lo hecho, en un commit:

- **Tests antes que el código** (`tests/unit/test_orden_lado_malo.py`, 8): en compra y en venta, el
  precio vuelve y la orden se coloca en el primer cierre en que vale (el de Z+4, el primero cuya
  cotización —el último tick de la M1 de Z+3— deja el 0 del lado bueno); no vuelve, y no hay orden
  ni petición; con `se_gasta_el_punto`, el rechazo y el punto gastado de antes; la comprobación y el
  rechazo miran la misma cotización; y por el camino real, el 2026-07-08 (la o15 de 11 a 15 salía
  rechazada). **Con el código de `main` fallaron los 8**: los cinco que esperan (los dos en que el
  precio vuelve, los dos en que no vuelve y el del camino real), por el rechazo por `precio_invalido`
  (en compra, en venta y la o15 del 8 de julio); y los tres que nombran el parámetro o el método
  nuevo (el del registro, el de `se_gasta_el_punto` y el de la misma cotización), porque no
  existían (revisor, b9).
- **Los que congelaban el rechazo que gasta el punto, cambiados de sentido A PROPÓSITO:**
  `test_punto_usado.py` (`test_el_rechazo_al_colocar_sigue_gastando_el_punto` →
  `test_el_0_del_lado_malo_ya_no_gasta_el_punto_y_la_orden_espera`, y el de antes, con
  `se_gasta_el_punto`); `test_cableado.py` (`…_la_orden_se_rechaza` → `…_la_orden_no_se_envia`, y el
  de antes con `se_gasta_el_punto`); `test_vida_de_la_orden.py`, la fila de la orden rechazada, con
  `se_gasta_el_punto`. El ayudante `_registro_se_gasta` vive en `test_cableado.py`.
- **Un hallazgo del primer `make check` de F2 (6 fallos), y lo que se hizo:**
  - cinco goldens que comparan el informe de la simulación con `main` byte a byte
    (`test_cuenta_por_mes.py::test_la_salida_es_la_de_main`, dos casos, y
    `test_metodo_adr0092.py::test_lo_que_ya_salia_es_byte_a_byte_lo_de_main`, tres) fallaban por la
    sección nueva de esperas, que salía siempre, también vacía. Ahora **solo sale si hay alguna
    espera**: sin esperas el informe es el de antes, byte a byte;
  - `test_sello_respaldo.py::test_sin_ticks_el_punto_se_libera_y_se_vuelve_a_colocar_en_el_cierre_de_la_vela_del_stop`:
    **medido al fallar, con la opción de antes**: sin ticks, la cotización del cierre de Z+6 es la
    M1 anterior, todavía por encima del punto, así que la reentrada o2 se enviaba en ese cierre y el
    bróker la **rechazaba** por `precio_invalido` (el test miraba el instante y no el estado, y
    pasaba). Con la espera, o2 espera desde el cierre de Z+6 —donde el punto ya está libre, que es lo
    que el test fija de ADR-0091— y se coloca en el de Z+7, con la misma caja, y se llena. Cambia a
    propósito, con su porqué en el docstring. Es un caso más de la deuda de las cotizaciones sin tick
    (la k−1), y de por qué F2 importa: la reentrada tras un stop sin ticks moría por la cotización.
- **Motor:** `Broker.lado_equivocado_al_colocar` (`engine/broker.py`): la misma `Mercado.cotizacion`
  y la misma `lado_equivocado`, y `_precio_infringido` la llama (no hay una segunda copia).
  `colocar_orden_limite` (`engine/primitivas_broker.py`), tras el lote de ADR-0081 y antes de enviar:
  si es stop, `orden_stop_lado_malo` = `espera` y el 0 queda del lado malo, no envía, no marca la
  caja usada ni el punto gastado, y apunta la espera una vez por punto y sesión
  (`ContextoDia.esperas`); al enviarse la orden de ese punto, la espera lleva su id.
  `zonas.punto_de_la_zona`. **El orden con los otros motivos, declarado (revisor, b4; escrito
  también en ADR-0097 §1):** si a la vez el lote no cabe (ADR-0081) y el 0 queda del lado malo, manda
  el lote: no se envía y gasta el punto, como dice ADR-0083 D1. Pero si a la vez el 0 queda del lado
  malo y la orden caería en otro motivo de rechazo al colocar (el cierre de mercado, el freno, el
  volumen, las órdenes simultáneas, el stops level o el margen), **manda el lado malo**: no se envía
  y espera, sin gastar el punto, porque la comprobación va antes de enviar y el bróker no llega a
  mirar esos motivos. Es una decisión de implementación que la regla del encargo no dice; va a «Lo
  que no me convence», en la PARADA final.
- **Traza y salidas:** la sección «### Esperas …» del informe del arnés (`cableado.CABECERA_ESPERAS`,
  con «esperas: N (enviadas despues: M)»); en `motor decisiones`, «orden NO enviada en zona:X a las
  HH:MM: el 0 queda del lado malo; espera sin gastar la caja ni el punto (ADR-0097)» y, al enviarse,
  «orden oN: enviada tras esperar desde las HH:MM, cuando el 0 queda del lado bueno (ADR-0097)». Las
  láminas no enseñan la espera (leen solo los no envíos de ADR-0081): lo dice el ADR.
- **La vela que mira** (encargo, F2.2): la de `Mercado.cotizacion` en el instante del cierre de la M1
  k (`k·60000 − 1`): con ticks, el último tick anterior o igual; sin ticks, la M1 k−1. Es la misma
  con la que rechaza el bróker.
- **Spec:** `orden_stop_lado_malo` (estrategia, enum `[se_gasta_el_punto, espera]`,
  DEFAULT_AMBIGUOUS en `espera`, bajo A-59, fuente `ev-v20-010243-21636d5f`); **A-59 ABIERTA**
  (pregunta, no bloqueante, `resuelve_en` F20 y F22, con lo que se buscó en el corpus); la
  descripción de `toca_colocar_orden_limite` (auditor, H1); `spec_version` 19.0.5 → **19.1.0**
  (menor: un parámetro nuevo; ninguna forma cambia), `spec manifest --escribir` y `spec docs
  --escribir`. Ningún registro de feedback: A-59 no se cierra.
- **ADR-0097**, con recuadro en ADR-0083 §1 y en ADR-0064 (decisión 1) y su fila en el índice (y las
  de los dos); sale del bloque `ids-inexistentes` del encargo y de este informe.
- **PROJECT_STATE.md:** A-59 en Known Ambiguities (`test_kit.py`) y «Tests Currently Passing» a 2130
  (`state check`); 24.809 bytes.
- **De paso, una línea de Technical Debt que se paga** (auditor, H6): `engine/decisiones.py:7-8` ya
  dice que el método lo fija ADR-0093 (§4). La línea «Dos textos que ADR-0093 deja viejos» pierde esa
  mitad en la orden de cierre.
- `generar_capa.py --comprobar`: `Generado.mqh` al día (el parámetro nuevo no está en ENTRAN).

### F2, la corrida de julio (etiqueta `f2`, sobre 7592c73e)

Las tres órdenes de D0 (fila de HOLDOUT del 2026-11-22, antes de correr), y `delta_julio.py` contra
la base de esta rama:

- `pivote-julio-f2.txt`: **T0 10; P5 18 (16 mismo lado, 2 otro lado); P6 en sesión 2; operaciones de
  más 20**; P1 1, P2 8, P3 14, P4 32, P7 2.
- **Delta contra el control (la base de esta rama, 11 y 19): parejas −1, operaciones de más +1.
  Contra la línea base de `PIVOTES-SESION-7.yaml` (14 y 39): parejas −4, operaciones de más −19.**
- `delta-julio-base-f2.txt`: 86 → 87 filas; 0 sesiones cambian de rn003; **4 filas cambian de
  patrón, 2 aparecen, 1 desaparece**.
- La sección «### Esperas» de `julio-f2.txt`: **6 esperas, 3 enviadas después** (07-06 07-11, 1,
  enviada; 07-08 11-15, 1, nunca; 07-10 07-11, 4, dos enviadas).

**Si casan las filas declaradas (las de 2026-07-06 07-11, 2026-07-08 11-15 y 2026-07-10 07-11):**

- **(i) Ningún rechazo por `precio_invalido` al colocar en julio**: «Rechazos por motivo: ninguno»
  (en la base, 5). **Casa.**
- **(ii) Cada fila que cambia, una por una:**
  - 2026-07-06 07-11, aparece un P5 de más (compra): **sesión declarada**; es la orden que esperó
    desde las 05:06:59Z y se envió después (antes, rechazada).
  - 2026-07-10 07-11, aparece un P5 de más, desaparece otro y una P2 del trader pasa de Δentrada 4 a
    26 puntos: **sesión declarada**; las esperas de esa sesión (05:19:59Z, 05:21:59Z y 07:08:59Z) y
    las órdenes que salieron de ellas (o1 y o6, `motor decisiones`).
  - **2026-07-10 11-15, tres filas del trader pasan a P4 «sin orden»** (una T0 pareja y dos P7):
    **no es una sesión declarada; la explica un freno de la cuenta.** `motor decisiones --bitacora
    2026-07-10` (`data/activar-sesion-08/decisiones-f2/`): en la de 07 a 11 salen dos órdenes que
    esperaron (o1 y o6; «enviada tras esperar» solo en esas dos); o6 se llena y salta su stop, y
    después o7, colocada sin esperar, también; o8, colocada sin esperar, se llena a las 07:50Z; con
    esa secuencia, distinta de la de la base, desde las 09:52 (07:52Z) **RN-032** («no se abre una operación cuyo riesgo no cabe antes del límite de la firma») prohíbe
    abrir; sigue prohibiendo toda la sesión de 11 a 15 (desde su primer cierre, 11:00), así que la
    orden que en la base emparejaba con el trader (o15) ya no se coloca. En la base, RN-032 también
    disparaba ese día, pero después de o15. `motor decisiones` compara por día, sesión, lado, instante
    y entrada, y no ve el lote ni el stop: que el riesgo no quepa se lee de la prohibición de RN-032,
    no de un lote.
  - **Casa**, con la de 11 a 15 explicada por el freno.
- **(iii) Las peticiones del día más cargado no suben**: el 2026-07-02, 45 en la base y 45 tras F2.
  **Casa.** (El 2026-07-06 sube de 37 a 41 y el 2026-07-10 baja de 22 a 12; el máximo diario sigue
  siendo 45, tope 2000.)

**CASA.** Ninguna cifra de esta corrida decide un parámetro (ADR-0093 §4): `orden_stop_lado_malo`
sigue DEFAULT_AMBIGUOUS y A-59 ABIERTA. Para el consultor, sin decidir: el delta en parejas es −1, y
la que se pierde la quita un freno de la cuenta (RN-032), que es la tensión que ACTIVAR-SESION-07.md
dejó para antes de (3) («los frenos de la cuenta del mes … que mueven parejas de rebote en julio»).

## F3 · S-5 (S-22): NO SE ACTIVA

El motor no cambia. Lo que dijo el trader en la 7b (S-5, `SESION-08-EXTRACCION.md` §3.5): leyó las dos
opciones, dudó y pidió más planteamiento, y acabó en «una vela roja, una vela verde, o al revés, allí
se traza un punto» (`ev-v20-010049-b400e914`), que es lo que el bot hace hoy (ADR-0085 §3).

- **Las dos filas de «Para precisar» NO se activan**, aunque la tabla final las dé como «resuelve»
  (sin pasar ningún mínimo no hay punto, `ev-v20-010049-4cb7f481`; basta la mecha,
  `ev-v20-010049-12e69e6d`): responden dentro de una condición (que la roja pase un mínimo) que él
  mismo no afirmó, y sueltas no son una regla (decisión del consultor, F3).
- **Las lecturas del consultor del 2026-11-06 para esta fase** («el último pivote que vale»,
  ACTIVAR-SESION-06-MOTOR.md, respuesta a la PARADA, decisión 0) **quedan sin objeto**: no hay
  condición que haga que un pivote «no valga».
- Recuadro fechado en ADR-0085 §3, junto al del 2026-11-05: la «rama de motor» a la que aquel
  mandaba la condición (`trabajo/activar-sesion-06-motor`) la dejó en PARADA, el consultor la mandó a
  la sesión 7 «y después en rama propia», y esa rama es esta; la condición no entra.
- S-22 va a la sesión siguiente, dentro del bloque de días, sobre un día de construcción.
- Ni `ultimo_punto_de_ruptura`, ni `_pivotes_m1`, ni los 20 tests de ACTIVAR-SESION-06-MOTOR.md §d se
  tocan. (El 52 % es con la lectura (a); con la (b), el 69 %: ACTIVAR-SESION-06-MOTOR.md:154.)

## F4 · La zona de control pide una vela contraria (v21 [86:23], `ev-v21-012623-bbdaf48a`)

**Cuadró** (0.6): el motor ya lo cumple. No se toca el motor ni RN-009. Entra
`tests/unit/test_zona_control_vela_contraria.py` (4), que lo **congela**: para todas las secuencias
de colores de hasta 7 velas tras la toma (verde, roja y sin cuerpo; 3.279 por lado), en compra y en
venta, cada zona de control que cuenta `pivotes_de_control` tiene al menos una vela contraria al
impulso entre la primera vela del impulso y la que la forma; y todas del color del impulso no dan
ninguna zona. Pasa en `main` y en la rama (el dominio no cambia).

**Qué enseñaba la lámina y por qué él lo leyó como zona** (0.6): las dos zonas de control que contó el
bot el 2026-04-27 de 11 a 15 tienen dos velas rojas cada una; lo que él leyó como «zona» con todas
las velas verdes no lo dice nada de lo que se puede mirar (decisión 7 de la PARADA). Ningún registro
de feedback sobre RN-009 (el encargo lo prohíbe: se contradijo sobre las zonas en la misma sesión);
la constancia, en este informe y en la lista de la sesión siguiente.

## F5 · Lo que se registra sin tocar el motor

- **S-1 (A-35):** la descripción de `liquidez_m15_mecha_que_vuelve` gana solo lo citable: la mecha de
  una M1 que pasa el alto de M15 sin romper con cuerpo no es una toma de M15 sino liquidez de M1
  (`ev-v20-000138-82b9ab6a`, `ev-v20-000251-9f6188aa`); no dice dónde queda su alto. Sin valor nuevo;
  **A-35 ABIERTA**, `liquidez_m15_mecha_que_vuelve` sigue en `solo_la_contraria`, DEFAULT_AMBIGUOUS.
- **S-2, pregunta 1 (RN-009):** no resuelve y se contradijo en cuántas zonas (§5.1, punto 1 de la
  extracción). Nada se activa. A la sesión siguiente; él pidió dos veces una sesión para explicarlo
  (v21 [86:52] y [110:27], sin ítem propio).
- **S-2, pregunta 2 (A-13, el margen):** «otra», según el contexto, sin cifra. No se activa: **A-13
  sigue ABIERTA solo por el margen** y no nace ningún parámetro. El E21 de la auditoría queda sin
  objeto en su parte de la cifra; la otra parte, en la decisión 4 de la PARADA.
- **S-3 y S-4: lo que dijo sin duda, como notas que no fijan valor** (decisión 3 de la PARADA: por
  ahora solo aquí, porque F1 prohíbe tocar `orden_stop_punto`, `sesgo_h4_rango_nuevo`, A-48 y A-58):
  - S-3, la compra: «Ahora, para precisar, ¿lo haces igual en una compra? Exacto, lo hago igual en
    una compra.» (`ev-v20-004803-377e65aa`).
  - S-4, el dibujo 2: con una vela de color contrario que rompe por encima, sigue buscando
    alcistas y el rango queda en el mismo nivel, sin actualizarlo (`ev-v20-005520-80eba002`, la
    afirmación del ítem). Que lo deja así «hasta que puede romper con una vela» de su color lo dice
    la extracción en [55:41], donde acaba el ítem, sin ítem propio (revisor, b2).
  - S-4, siempre en H4: «siempre marca su rango en su temporalidad mayor»
    (`ev-v20-005723-f1eff54a`, la afirmación del ítem).
  - S-4, la ruptura por abajo, igual: **sin ítem de evidencia** (v20 [57:42]–[57:50], extracción
    §3.4); no se cita aquí más que por la extracción, y la evidencia está protegida en esta rama.
- **S-5:** lo de F3. **S-6:** lo de F2.
- **S-7:** resuelve una pregunta de material: la tarde del 10 de julio no se grabó
  (`ev-v20-011213-947092b6`). Recuadro fechado en `VIDEO-JULIO.md`, junto al pasaje de la pregunta
  (§10, «Bloque técnico, dos preguntas»).
- **B-15** (la fila P1 del 2026-07-01 de 11 a 15; la respuesta del consultor a la PARADA final de la
  7a la mandaba a la 7b): no se preguntó; va al bloque de días de la sesión siguiente.
- **Para la preparación de la sesión siguiente:** el 2026-04-24 de 07 a 11 queda gastado; las
  reservas del 2026-01-22 (de 11 a 15) y del 2026-07-16 (de 07 a 11) siguen sin usar.
- `spec_version` 19.1.0 → **19.1.1** (parche: solo una descripción), `spec manifest --escribir` y
  `spec docs --escribir`; trailer `Fuente:` con los dos ítems de S-1.

Este commit lleva también la corrida de julio tras F2 (arriba), que se hizo sobre 7592c73e: F3, F4 y
F5 no cambian el motor, así que la corrida es la del código de este commit. Desviación declarada:
F3, F4 y F5 van en un mismo commit, con la corrida de F2, para no gastar tres `make check` en
cambios que no tocan el motor.

## F6 · La respuesta de FTMO del 2026-11-20

### La respuesta de FTMO del 2026-11-20

FTMO contestó el 2026-11-20 (ticket MVT-CQNXT-065) al correo de Aleks del 2026-11-19 (las cuatro
preguntas están en la hoja de ruta, A.2). **El correo no se copia** (como el del 2026-10-05; el
repositorio es público): ningún texto de esta rama lleva frases en inglés del correo ni el nombre de
quien lo firma. **La fuente es la paráfrasis del consultor**, del encargo de esta rama (F6), tal cual:

> (1) Para el límite de 2.000 peticiones diarias solo cuentan las acciones de trading: abrir, cerrar y modificar órdenes, incluido mover el stop o el objetivo.
> (2) Las lecturas (precios, ticks, historial de velas, datos de la cuenta, órdenes y posiciones) no cuentan para ese límite ni se consideran hiperactividad, también leyendo una vez por vela de M1.
> (3) Se permite que las decisiones las calcule un programa propio en Python que manda las órdenes por el terminal de MT5, siempre que la estrategia cumpla sus condiciones y no sea alta frecuencia ni arbitraje de latencia. FTMO no pide el código.
> (4) Los límites de infraestructura valen igual para la cuenta Swing en MT5.

### Lo hecho (commit propio, sin motor)

- `docs/validation/FTMO-REGLAS.md` (informe cerrado): recuadro fechado junto a R13 (tras la tabla del
  §2) y otro al final de su §4.
- `docs/validation/RESPUESTAS-FTMO.md` (informe cerrado): recuadro al principio, que dice que hay
  una respuesta posterior y dónde está.
- A-54 (`ambiguedades.yaml`): su `pregunta` gana la respuesta y dice lo que falta (0.7): **si una
  petición rechazada cuenta, si una cancelación cuenta por separado y qué hace el servidor al
  pasarse**. **A-54 sigue ABIERTA.**
- Los cuatro `freno_*` (`parametros.yaml`): su descripción gana la respuesta y lo que falta; **siguen
  DEFAULT_AMBIGUOUS con su valor** (1000, 1500, 5 y 1). Están en ENTRAN de `generar_capa.py`, pero
  la descripción no entra en `Generado.mqh`: `generar_capa.py --comprobar` lo da al día.
- ADR-0082 §4 (D4): recuadro fechado, sin tocar el cuerpo ni el Estado. Dice qué quita la respuesta
  (la razón de descartar la alternativa 4 y la parte de D4 que se apoya en el tope: «un bucle de
  Python que sondea gasta presupuesto») y qué deja en pie, copiado de 0.7 sin añadir (el bot final es
  un EA y una capa en Python habría que tirarla en F29, que es la razón de descartar la 3; el
  Strategy Tester y el VPS sin cita de FTMO; la equivalencia de F30), y que reabrir D4 lo decide
  Aleks con un ADR nuevo, que no existe. No decide nada.
- `spec_version` 19.1.1 → **19.1.2** (parche: textos), `spec manifest --escribir`, `spec docs
  --escribir`; trailer `Fuente: ADR-0067, ADR-0082` (el precedente del 2026-10-05 usó los ADR del
  freno y de los cierres, 0e1457c7).
- **Lo que la respuesta no paga** (para A.2 en la orden de cierre): P-D1, lo del heredado 27 (la
  «maximum capital allocation rule» y el asterisco de «USD/LOT*») y la pregunta 6 de A-55 siguen sin
  respuesta; y no dice nada del modo de margen que espera R6a.7.

## F7 · Lo que la auditoría dejó sin dueño

1. **El documento: EN LA PARADA** (decisión 0). La auditoría cita `ADR-0087` en su línea 248, fuera
   de un bloque `ids-inexistentes`, y copiada tal cual no sella. No se ha copiado. Sigue en
   `C:\Users\USER\Desktop\AUDITORIA-2026-11-21.md` (377 líneas).
2. **El panel de FTMO, hecho** (los cuatro textos de la línea de Technical Debt, cada uno por su
   régimen): `docs/runbooks/DEMO-FTMO.md` (runbook, editado: «Hecho, sin ejecución (declarado por
   Aleks el 2026-11-07)»); la descripción de `reloj_dia_riesgo` (spec, con `spec docs`); ADR-0090 §1
   (recuadro); `FTMO-REGLAS.md` §3, R2 (recuadro). La fuente de los cuatro es el registro de HISTORIA
   «Next Action HECHA · A · el panel del límite diario». La línea sale de Technical Debt en la orden
   de cierre (abajo).
3. **A-16 NO se cierra:** recuadro fechado en ADR-0092 §10 que remite a ADR-0096 y a PREREGISTRO.md;
   el texto de A-16 gana la medida de METODO-FIDELIDAD-RENTABILIDAD.md §1.3 (183 de 198 dentro de la
   M1 del minuto, y que no contesta la pregunta) y la vela de otro color (`ev-v19-012924-64367863`,
   que entra en su `evidencia`), sin medir; `resuelve_en` sigue en F26. Las frases de R4.3 («la paga
   la activación de 7b») y de Technical Debt se corrigen en la orden de cierre (abajo).
4. **A-35 y `bloqueante` (E20): propuesta en la PARADA** (decisión 5), con lo que dio 0.8. No se ha
   cambiado.
5. **A-53 (E2), la reentrada de ADR-0083 D1 (E3) y A-43 (E6): no se activan.** Van como preguntas
   técnicas a la sesión siguiente (R4.6; abajo). A-43, además, la pregunta Aleks por WhatsApp antes
   de la corrida de (3); no ha llegado respuesta a la rama.
6. **S-23 frente a A-46 (E4): ya estaba decidido y no hay REOPEN** (ACTIVAR-SESION-06.md; el texto de
   A-46; B-10 de PREGUNTAS-7B.md). Sigue como pregunta B-10 para la sesión siguiente. **Esta nota
   cierra el E4 de la auditoría**; nada en la spec.
7. Lo de la orden de cierre, preparado abajo, en «Para la orden de cierre».

Este commit lleva F7.2 y F7.3 juntos (los dos son textos, sin motor), con spec 19.1.3 y trailer
`Fuente: ADR-0090, ADR-0092, ADR-0096, ev-v19-012924-64367863`.

## Para la rama y la sesión siguientes

**Para la corrida de (3)** (ADR-0070 §3 y el pivote de ADR-0093 §6):
- Lo que esta rama deja distinto en el motor: **solo F2** (`orden_stop_lado_malo` = `espera`,
  ADR-0097): la stop del lado malo espera sin gastar el punto. En julio, 0 rechazos por precio al
  colocar (antes 5), 10 parejas y 20 de más (antes 11 y 19). S-22 y F4 no cambian el motor.
- Las tensiones con que correría: `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED, frente al «no es
  válido» de la 7a (A-43, `ev-v19-012529-685ae24d`); `orden_pendiente_al_abrir_escenario` =
  `se_mueve`, DEFAULT_AMBIGUOUS (A-53); A-35 sin respuesta (`liquidez_m15_mecha_que_vuelve` en
  `solo_la_contraria`); RN-019, que no dispara nunca; `orden_stop_punto` y `sesgo_h4_rango_nuevo`,
  según decida el consultor la PARADA de F1; y los frenos de la cuenta del mes (RN-032, RN-036), que
  mueven parejas de rebote en julio (en esta rama, la pareja que se pierde la quita RN-032), que
  ACTIVAR-SESION-07.md:684 dejó al consultor «antes de (3)» (decisión 6).

**Para la sesión siguiente (R4.6)**, las preguntas que quedan, en el lenguaje del trader y sin
sugerir respuesta:
- **A-35** (si no contesta por WhatsApp): «Cuando la mecha de una vela de 1 minuto pasa tu alto de 15
  minutos y vuelve, ¿dónde queda tu alto de 15 minutos?».
- **Las zonas de control** (la sesión que él pidió dos veces): «¿Cuántas zonas de control puede haber
  antes de que rompa el punto?», y «En esta lámina, ¿qué es lo que ves como zona de control?» (F4).
- **El margen del break even** (A-13): «Cuando pones el break even, ¿cuánto tiene que pasar la vela el
  alto de tu zona de control?».
- **S-22, sobre un día real**: «Aquí, ¿cuál es tu punto?».
- **A-53**: «Si tienes una orden puesta y el precio toma otra liquidez de 15 minutos, ¿qué haces con
  la orden?».
- **La reentrada** (ADR-0083 D1, con RN-019): «Después de un stop, ¿vuelves a entrar en el mismo
  punto? ¿Cuántas veces, y con qué caja?».
- **A-43**: «Si la liquidez de 15 minutos se toma antes de las 7, ¿vale para entrar después de las
  7?».
- **B-10**: la de PREGUNTAS-7B.md, tal como está.
- **A-59** (nueva): «Cuando se forma la caja y el precio ya está más allá del 0, ¿qué haces con la
  orden?», sobre un día real, en compra y en venta.
- **Lo que salga de la PARADA de F1**: A-48 («En este día, ¿dónde pones tu 0?», señalando en la
  lámina) y A-58 (el dibujo 1: «Cuando la vela rompe tu rango y cierra de su color, ¿tu rango nuevo
  va del alto al bajo de esa vela?», sobre una H4 real).
- **B-15** (el 2026-07-01 de 11 a 15) y el día gastado del 2026-04-24, para la preparación; las
  reservas del 2026-01-22 y del 2026-07-16, sin usar.

## Para la orden de cierre (preparado, SIN aplicar)

**Con estas palabras (encargo, F3):** PIVOTES-SESION-7.yaml mide «después de activar la 7b, incluida
la rama de S-22 y S-19». Esta es esa rama. Que S-22 no cambie el motor es su resultado, no un hueco,
y el yaml no se toca. Tampoco se activan las filas del gate de RN-009 que el «por_que» del yaml
contaba (S-2, pregunta 1, no resolvió).

**Next Action:**
- AHORA: «(2026-10-08)» → «(2026-11-22)» (E13).
- **F, sustituida entera por:** «F. La sesión 7, en dos días con el método de ADR-0093 (R4.3; pivote
  en docs/plan/PIVOTES-SESION-7.yaml; línea base, RECORRIDA-CONSTRUCCION-2.md). La 7a
  (2026-11-16-sesion-07) ingerida y ACTIVADA (F39e: ADR-0094, A-58 abierta; break even al cierre, A-13
  abierta por el margen). La 7b (2026-11-20-sesion-08, v20 y v21) ingerida (F39j) y ACTIVADA
  (ACTIVAR-SESION-08.md, F39k): la stop cuyo 0 queda del lado malo espera (ADR-0097, A-59 abierta);
  S-22 no cambia el motor; A-48 y A-58 en la PARADA de esa rama. Siguiente: (3) la corrida de
  ADR-0070 §3 y la lectura del pivote (ADR-0093 §6), con su contingencia sin retocarla (decisión de
  Aleks del 2026-11-19; R4.3); antes, lo que el consultor decida de esa PARADA y la respuesta de A-43
  por WhatsApp. El vídeo de mapeo (recibido el 2026-11-18): SIN ABRIR y fuera del repo, no se ingiere;
  octubre y noviembre de 2026, reservados. C y R6a en los huecos; R5.7 después de (3), sobre esa
  corrida.» (E14: la F de hoy ya no repite «(3)»; el cierre de F39j la reescribió.)
- C: quitar «No va antes de las trazas, de las láminas ni de la preparación de la sesión 7.» (E15:
  las tres están hechas).
- J: «Rama propia antes de la próxima sesión que etiquete días (G.2).» en vez de «… que use la hoja»
  (E9, el texto de G.2).
- L: sale (E10: su motivo cayó; «caja_bloque ya no cuelga de ese ítem»), a HISTORIA como HECHA sin
  objeto; y G.2 pierde NA:L de sus Refs.
- N: «cubre hasta el 7-10-2026, ya pasado, y se renueva por condición» (E18).
- I: añadir «Pesa más desde la 7a: el sesgo de las sesiones de enero depende de diciembre (Technical
  Debt).» (E18). D: sin cambios (coherente con «sin prisa»).

**Technical Debt:**
- Sale la línea «El panel de FTMO quedó declarado el 2026-11-07…» (F7.2, pagada).
- La del visor (C1), ampliada: «- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py: la
  valida `_diagnostico_de`, :2250-2261; el arnés la aplica, :2438; `motor_visor`, :2479, no): la pone
  en el nombre y en el HTML y corre una cuenta por mes (ADR-0092 §8; VISOR-CONSTRUCCION.md §4.3;
  auditoría del 2026-11-21, C1). Dueño: rama corta del visor (conectarla o negarla).»
- RN-019 (la línea «RN-019 no dispara nunca…»), con dueño: «… Dueño: va con la reentrada de ADR-0083
  D1 (R4.6).»
- «Dos textos que ADR-0093 deja viejos…» pasa a uno: el de `engine/decisiones.py:7-8` lo corrigió esta
  rama (F2); queda el otro (H19 de PREPARACION-SESION-7.md §0.2).
- Las correcciones de texto de la auditoría (§2.5), localizadas en el PS de la rama (la auditoría
  numeraba sobre 5ae7c482):
  - la 86 (hoy PS:87, los docstrings de viabilidad): `viabilidad_comision.py:46` → `:45` (medido: el
    comentario «10 (perfil)» está en la 45);
  - la 100 (la del visor): corregida en la línea de C1, arriba;
  - la 92 (hoy PS:93, «Riesgo residual de B»): «, y un `getattr(os, ...)` no se ve» → «; un
    `getattr(os/sys, ...)` ya no se decide (auditoría del 2026-11-21, sin medir aquí)»;
  - la 119 (hoy PS:120, «`cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT») y la 123 (hoy
    PS:124, «EL FRACTAL 5/120 …»): no son deuda (un límite de git aceptado y un hallazgo); salen a
    HISTORIA;
  - la 124 (hoy PS:125, la guardia de `cobertura_material` en `universo()`): dudosa según la
    auditoría; queda como está hasta medirla (heredado 7), sin texto nuevo.
- Si el consultor acepta la decisión 5: la línea de A-35 pierde «y bloqueante».

**Saldo de PROJECT_STATE.md** (simulado en memoria con un guion de la carpeta de trabajo sobre el PS
de la rama, 24.809 bytes): AHORA +0, F −59, C −82, J −5, L −147, N +12, I +96, panel −158, visor
+131, RN-019 +51, decisiones +59, y §2.5: la 86 +0, la 92 +54, la 119 −131, la 123 −92:
**−271; queda en 24.538 bytes, por debajo de 25.000** (sin la de A-35, que depende de la decisión 5
y quita unos bytes).

**Hoja de ruta:**
- **R4.3**, Estado: «ABIERTA (la 7a, ingerida y activada, ACTIVAR-SESION-07.md; la 7b, ingerida en
  trabajo/sesion-08 y activada en trabajo/activar-sesion-08, ACTIVAR-SESION-08.md: la stop del lado
  malo espera, ADR-0097, y S-22 no cambia el motor; falta leer el pivote en (3)).» Y su «Hecho
  cuando»: «La deuda del panel de FTMO la paga la activación de 7b; A-16 sigue ABIERTA con la regla de
  ADR-0092 §9 (ADR-0096)».
- **R4.6**, «Qué es», al final: «Las preguntas técnicas que dejó la 7b: A-53, A-43, la reentrada de
  ADR-0083 D1 (con RN-019), B-10 y A-59 (ACTIVAR-SESION-08.md, "Para la sesión siguiente").» (E5.)
- **A.2**, Estado nuevo: «Registrada la respuesta del 2026-11-20 (ticket MVT-CQNXT-065),
  parafraseada (ACTIVAR-SESION-08.md, FTMO-REGLAS.md): las lecturas no cuentan para las 2.000
  peticiones; se permite un programa propio en Python que decide; los límites valen para Swing. Sin
  respuesta: P-D1, lo del heredado 27 y la pregunta 6 de A-55; de A-54, las rechazadas, las
  cancelaciones por separado y qué hace el servidor al pasarse. No paga lo que R6a.7 espera sobre el
  modo de margen. Reabrir ADR-0082 §4 es un ADR nuevo de Aleks.»
- **A.4**, «Hecho cuando»: «v6 a v21 están en Drive con su SHA256SUMS» (era «v6 a v10»).
- **A.5**, «Hecho cuando»: «el panel declarado (HECHO el 2026-11-07) y el grabador hecho; M, sin objeto
  mientras break_even_condicion sea cierre (NA:M)» (E11).
- **R2.3**, «Depende de»: «la exportación del trader; Aleks se la vuelve a pedir (NA:Q)» (E8: A.3
  está HECHA y no la trataba).
- **Fechas fijas**: sale la primera (la prueba que terminó el 11 de noviembre; E12).
- **G.8**, «Quién»: «el código, hecho (F39i); falta el traslado de Aleks» (E16).
- **R4.2**: sus dos líneas «Estado» en una (E17); **G.4**: Refs `NA:F` → `—` (no tiene que ver con la
  F).
- Lo que la auditoría da y el encargo no lleva a F7.7 (auditor, H4): E19 (R5.3 sin letra), E22
  (textos «PROVISIONAL» en parámetros CONFIRMED), C2, C6 y su §2.3; quedan para el consultor.

## El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde `main` en 00e6dc8b con `abrir-rama`; base y CI de `main` comprobadas (`gh run view` suelto) | Hecho | «Base comprobada»; run 44978301993, success, sobre 00e6dc8b; `e69bfd05` |
| 2 | Contrato: tramo R4, riesgo alto, artefacto, lista blanca con lo protegido mandando; carpetas de feedback anteriores protegidas una a una | Hecho | `contrato.yaml`; la ruta de PREGUNTAS-7B.md corregida en `f5ee88f7` (desviación de la apertura) |
| 3 | Tag previsto `stable/F39k-activar-sesion-08`, comprobado que no existe | Hecho | `git tag -l` y `git ls-remote` vacíos |
| 4 | ADR-0097 en un bloque `ids-inexistentes` del encargo; sale en el commit que lo crea; A-59 fuera del bloque; ningún otro ADR | Hecho | `e69bfd05` y `7592c73e` (el bloque sale); el informe declara además ADR-0087 en su propio bloque, porque lo nombra al hablar de la auditoría |
| 5 | La auditoría, del Escritorio, sin reconstruirla | Hecho de otra forma | no estaba al empezar; Aleks la dejó a mitad de la apertura; 377 líneas, no 378 |
| 6 | PARADA condicional: fase 0 entera y commiteada; las fases que cuadran se hacen; F1 siempre a la PARADA | Hecho | `f5ee88f7`; «Lo que necesito que decidas» (decisiones 0 a 7) |
| 7 | QUÉ NO CAMBIA: A-35 ABIERTA y su parámetro; S-22 sin tocar; RN-009, `pivotes_de_control` y `zonas_control_max_por_esquema`; `toma_antes_de_la_ventana`, `orden_pendiente_al_abrir_escenario`, ADR-0083 D1 PROVISIONAL, break_even_*; ninguna corrección del bloque activada salvo F4; sin corrida que cuente (nada al Marcador, PIVOTES-SESION-7.yaml intacto); PREREGISTRO.md y criterio_fidelidad.yaml intactos; sin cifras en formas; citas solo de ítems citables; ningún fotograma; Next Action y hoja de ruta sin tocar; Makefile, .claude/ y la guardia sin tocar; Generado.mqh sin cambio; el correo de FTMO sin copiar | Hecho | `git diff --stat main...HEAD` (abajo); `generar_capa.py --comprobar` al día en F2, F6 y F7; PROJECT_STATE solo cambia en Known Ambiguities (A-59), Tests Currently Passing y la cabecera de la rama |
| 8 | Fechas de los registros de feedback | No aplica | ningún registro de feedback en la rama (nada se cierra; F1 a la PARADA; F5 sin registro) |
| 9 | D0: las tres órdenes sueltas, sobre código commiteado; README antes de correr; al repo solo pivote y delta | Hecho | `anexos/ACTIVAR-SESION-08/` (README, pivote-julio-base, delta-julio-f39e-base, pivote-julio-f2, delta-julio-base-f2) |
| 10 | Control de D0 (desviación declarada: repetir la de F2 de la 7a), fila por fila si sigue en la laptop | Hecho | 0.2: idéntico, 86 filas, 0 cambios |
| 11 | Lecturas de calentamiento en la fila de HOLDOUT del día, antes de correr | Hecho | filas del 2026-11-21 (dos) y del 2026-11-22 (dos) |
| 12 | Fase 0, 0.1 a 0.9 | Hecho | §0.1-§0.9 |
| 13 | F1: solo se mide; a la PARADA con 0.3, 0.4 y las vías | Hecho | 0.3, 0.4; decisiones 1 y 2; nada tocado de `orden_stop_punto`, `sesgo_h4_rango_nuevo`, A-48 ni A-58 |
| 14 | F1, las notas de F5 que no fijan valor | Hecho de otra forma | solo en el informe (F5), por el choque con F1 (decisión 3) |
| 15 | F2: A-59 (pregunta, no bloqueante, con lo buscado en el corpus) y el parámetro DEFAULT_AMBIGUOUS en `espera`; tabla de PS | Hecho | `7592c73e`; `orden_stop_lado_malo` |
| 16 | F2: la comprobación con lo mismo que el bróker, sin duplicar; la vela que mira; traza y `motor decisiones` lo nombran distinto | Hecho | `Broker.lado_equivocado_al_colocar`; sección «### Esperas»; líneas de la bitácora |
| 17 | F2: ADR-0097, lo dicho frente a la lectura del consultor, recuadros en ADR-0083 y ADR-0064, filas del índice | Hecho | `docs/adr/0097-…`; recuadros; `docs/adr/README.md` |
| 18 | F2: tests antes del código, compra y venta, no vuelve, camino real que rompe en `main`; los que congelaban el rechazo cambian a propósito | Hecho | `test_orden_lado_malo.py` (8; los 8 fallaban con el `src/` de `main`, idéntico entonces: la rama no lo había tocado); cambios a propósito en `test_punto_usado`, `test_cableado`, `test_vida_de_la_orden` y `test_sello_respaldo` |
| 19 | F2: filas declaradas antes de correr con el cambio, y si casan | Hecho | 0.5 (declaradas en `f5ee88f7`); «F2, la corrida de julio»: CASA |
| 20 | F3: no se activa; recuadro en ADR-0085 §3; lo dice el informe, también de las dos filas de «Para precisar» | Hecho | `cb02d3a9` |
| 21 | F4: cuadra; un test lo congela; qué enseñaba la lámina | Hecho | `test_zona_control_vela_contraria.py`; 0.6; la lámina, sin respuesta medible (decisión 7) |
| 22 | F5: S-1 en la descripción, S-2, S-3/S-4, S-5, S-6, S-7 en VIDEO-JULIO, B-15, días gastados | Hecho | `cb02d3a9` (F5 en un commit con F3, F4 y la corrida de F2: desviación declarada) |
| 23 | F6: la paráfrasis entera en el informe; recuadros en FTMO-REGLAS (R13 y §4), RESPUESTAS-FTMO, ADR-0082 §4; A-54 y los cuatro `freno_*` sin cambiar valor ni estado | Hecho | `89ce3ad0` |
| 24 | F7.1: la auditoría en un commit propio, el primero tras la apertura | No hecho: en la PARADA | decisión 0 (ADR-0087 en su línea 248) |
| 25 | F7.2: los cuatro textos del panel | Hecho | commit de F7 |
| 26 | F7.3: A-16 no se cierra; recuadro en ADR-0092 §10; su texto gana §1.3 y la vela de otro color | Hecho | commit de F7 |
| 27 | F7.4: propuesta de `bloqueante` para A-35 | Hecho (propuesta) | decisión 5 |
| 28 | F7.5 y F7.6: A-53, la reentrada, A-43 y B-10, sin activar; la nota que cierra el E4 | Hecho | F7 |
| 29 | F7.7: lo de la orden de cierre, con bytes | Hecho | «Para la orden de cierre» (24.538 bytes) |
| 30 | Para la rama y la sesión siguientes | Hecho | su sección |
| 31 | Informe con todo lo pedido; PROJECT_STATE < 25.000 | Hecho | 24.809 bytes en la rama |
| 32 | Revisor con los seis alcances, push a `fix/` y CI, PARADA final | Hecho | «Informe del revisor» (0 bloquea, 7 importa, 6 menor; todos arreglados o contestados); run 45005647166 (solo el fallo aceptado); «PARADA final» |

**Lo que NO cambia, medido** (`git diff --stat main...HEAD` tras `46028e24`, 42 ficheros): ni el
`Makefile`, ni `.claude/`, ni `scripts/`, ni `src/botsito/mql5bridge/` ni `mql5/`, ni
`knowledge/evidence/`, `knowledge/feedback/`, `knowledge/cases/` ni `knowledge/corpus/`, ni
`docs/plan/` (la hoja de ruta y `PIVOTES-SESION-7.yaml`), ni `PREREGISTRO.md`, ni
`SESION-08-EXTRACCION.md` ni `PREGUNTAS-7B.md`. En `src/`, solo `engine/` (F2).

## Exposiciones declaradas

Cuatro filas de `docs/validation/HOLDOUT-EXPOSICIONES.md` de esta rama, cada una escrita antes de lo
que declara: 2026-11-21, la apertura y la fase 0; 2026-11-21, el control de D0, los `motor
decisiones` de 0.4 a 0.6 y las medidas de 0.3 y 0.6 (ampliada el mismo día, antes de correrlo, con el
cálculo de los pivotes de control del 2026-04-27); 2026-11-22, lo que lee la rama ese día (los `make
check`, la evidencia, `kb find --solo evidencia` y el test nuevo del 8 de julio, que calienta con
junio); 2026-11-22, la corrida de julio tras F2 y su `motor decisiones` del 2026-07-10. Lo único
reservado que se lee son velas para calentar el sesgo (marzo y junio de 2026), por el recuento.
**Ningún fotograma de v20 ni de v21 se ha abierto**, por ninguna vía; ninguna transcripción ni
filtrada; ningún libro, caso ni agregado.

## Informe del revisor

El subagente `revisor`, lanzado sobre `1a5cf2d2` con los seis alcances del encargo (fila de
`HOLDOUT-EXPOSICIONES.md` del 2026-11-22, declarada antes). Pegado tal cual; no cita nada de un tramo
no citable (0 retiradas).

### Informe del revisor · trabajo/activar-sesion-08 · 2026-11-22

Base `00e6dc8b` (merge-base con main). HEAD `1a5cf2d2`, 7 commits. Estadiado y sin commitear: una fila de `docs/validation/HOLDOUT-EXPOSICIONES.md`, la del revisor (`git diff --cached --stat`: 1 fichero, 1 línea añadida).

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | Una comprobación del contrato falla y ni el contrato ni el informe lo dicen. `contrato.yaml:57` pide `feedback apply --sesion 2026-11-20-sesion-08 --check`, que sale con 1 porque la rama no tiene registros de feedback (lo hace a propósito: fila 8 del «punto por punto», «No aplica»). Hay que quitar esa línea del contrato o dejar escrito en el informe que falla y por qué. | `uv run botsito feedback apply --sesion 2026-11-20-sesion-08 --check` → `ERROR: no hay ningun registro de la sesion 2026-11-20-sesion-08 (las que hay: … 2026-11-16-sesion-07)`, exit 1. `grep 'feedback apply' ACTIVAR-SESION-08.md`: sin resultados |
| a2 | menor | El informe aún empieza por el aviso de plantilla, que ya no es cierto. | `docs/validation/ACTIVAR-SESION-08.md:3` «> PLANTILLA hasta la fase 0: …» |
| a3 | menor | En la primera fila de HOLDOUT del 2026-11-22, el texto dice que los `make check` y el test del 8 de julio calientan con junio («mes con días reservados»), pero la columna del recuento solo nombra marzo. La fila del 2026-11-21 sí nombra los dos meses. | `HOLDOUT-EXPOSICIONES.md`, fila «lo que lee la rama este día»: «calienta con el M1 de junio de 2026 (mes con días reservados)» frente a «por el recuento: marzo de 2026 entero» |
| a4 | menor | El recuadro del §4 de FTMO-REGLAS dice «De lo de arriba … contesta qué cuenta como petición para R13». El §4 no pregunta eso: de R13 solo pregunta si los límites entran en el registro como `firma_*`. | `docs/validation/FTMO-REGLAS.md` §4, «PARA EL CONSULTOR», viñeta de R11/R13, y el recuadro del 2026-11-22 que la sigue |

Comprobado sin hallazgos:
- **Contrato:** `contrato_rama.py` da `CONTRATO: 42 ficheros dentro del contrato … 6 comprobaciones para el revisor` y `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-22 … estadiada`, exit 0.
- `generar_capa.py --comprobar` da `Generado.mqh: al dia (capa_hash 8d1f61bc…)`.
- `spec docs` (sin `--escribir`) da `OK: docs/spec coincide con knowledge/spec/`.
- `make-check.log`: `3607 passed, 6 xfailed`, `SELLO … sobre el arbol 79db7817…` (que es `HEAD^{tree}`), `PICO DE MEMORIA … 318 MiB`, y `knowledge validate` OK (753 ítems, historial intacto). La fila estadiada no está sellada: el commit siguiente necesita otro `make check`.
- **Trailers `Fuente:`:** los cuatro commits que tocan `knowledge/spec` los llevan en el cuerpo, y todos los ids existen (ADR-0067, 0082, 0090, 0092, 0096 y 0097; los ev-v17, ev-v19 y ev-v20 citados).
- **Holdout y material:** `knowledge/cases/` no se toca y no hay agregados. Toda lectura reservada está en filas del día.
- **Regímenes de cambio:** `knowledge/evidence`, `knowledge/feedback`, `data/manifests` y `knowledge/corpus` no se tocan.
- **Ambigüedades:** A-59 se abre en `7592c73e` junto con `docs/spec/ambiguedades.md` y su fila de PROJECT_STATE. A-54 y A-16 cambian cada una con su `.md` en el mismo commit. Ninguna se cierra.
- **ADR:** ADR-0097 tiene `## Estado` que empieza por «ACTIVE».
- **Informes cerrados:** FTMO-REGLAS, RESPUESTAS-FTMO, VIDEO-JULIO y los seis ADR con recuadro solo ganan líneas (`git diff --numstat`: 0 borradas en todos), y lo nuevo va en recuadros `>`. HISTORIA solo crece (+183/−0).
- **Lo demás:** no hay sitio nuevo con `cita` (las tres guardias no aplican). Ninguna cifra entra en una forma ejecutable (test_no_business_literals pasó en el make check). No hay ítems de evidencia nuevos (punto 10 sin objeto).
- **Tres citas del informe comprobadas contra su fuente:** ADR-0064:84-86, ADR-0083:24-30 y ACTIVAR-SESION-06-MOTOR.md:154 (52 % / 69 %) casan. Lo mismo `test_kit.py:379` (`assert abiertas == {"A-35"}`) y ADR-0057:107-108.

#### Eje (b) · Encargo
Resumen: 0 bloquea, 6 importa, 3 menor. Requisitos: 27 hechos, 4 parciales, 1 no hecho (en PARADA, como el propio encargo prevé).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con abrir-rama, base y CI de main | Hecho | informe §«Base comprobada»; `e69bfd05` |
| 2 | Contrato (R4, alto, artefacto, lista blanca, feedback anterior protegido una a una) | Hecho | `contrato.yaml:1-55` (ver a1 sobre una comprobación) |
| 3 | ADR-0097 en el bloque `ids-inexistentes` y fuera de él en su commit; A-59 fuera; ningún otro ADR | Hecho | `git show 7592c73e -- docs/encargos/…` (el bloque sale). ADR-0087 en el bloque del informe, declarado |
| 4 | D0: tres órdenes sueltas, README antes, al repo solo pivote y delta | Hecho | `anexos/ACTIVAR-SESION-08/` (5 ficheros) |
| 5 | Control de D0, fila por fila | Hecho | `delta-julio-f39e-base.txt`: 0 cambian, aparecen ni desaparecen |
| 6 | 0.1 a 0.9 | Hecho | informe:44-365 |
| 7 | F1 solo medido y en la PARADA, sin tocar `orden_stop_punto`, `sesgo_h4_rango_nuevo`, A-48 ni A-58 | Hecho | diff de `parametros.yaml` y `ambiguedades.yaml`: no aparecen |
| 8 | F1/F5: las notas que no fijan valor | Hecho de otra forma, declarado | decisión 3; informe:595-605 (ver b2) |
| 9 | F2.1: A-59, pregunta, no bloqueante, con lo buscado en el corpus; parámetro DEFAULT_AMBIGUOUS en `espera`; fila de PS | Hecho | `ambiguedades.yaml` (A-59); `parametros.yaml` (`orden_stop_lado_malo`); PS:76 |
| 10 | F2.2: comprobación con lo mismo que el bróker, sin duplicarla; qué vela mira; traza y bitácora lo nombran | Hecho | `broker.py:558-571`, `:584`; `primitivas_broker.py:664-682`; `decisiones.py` (dos líneas nuevas); `cableado.CABECERA_ESPERAS` |
| 11 | F2.3: ADR-0097, recuadros en 0083 y 0064, filas del índice | Hecho | ver b1 y b4 |
| 12 | F2.4: tests antes que el código, compra y venta, no vuelve, camino real; cambios de sentido declarados | Hecho | `test_orden_lado_malo.py` (8); docstrings «CAMBIA DE SENTIDO A PROPOSITO» (ver b5) |
| 13 | F2: filas declaradas antes y si casan | Hecho | declaradas en `f5ee88f7` (00:30), antes de `7592c73e` (01:56); (i), (ii) y (iii) comprobados en `julio-base.txt`/`julio-f2.txt` (ver b3) |
| 14 | F3: no se activa; recuadro en ADR-0085 §3; las dos filas de «Para precisar» | Hecho | ADR-0085, recuadro del 2026-11-22; informe:548-566 |
| 15 | F3: la frase del pivote en «Para la orden de cierre» | Hecho | informe:730-733 |
| 16 | F4: cuadra; test que congela; motor y RN-009 sin tocar | Hecho | `test_zona_control_vela_contraria.py`; `src/botsito/domain` fuera del diff |
| 17 | F5: S-1 en la descripción, sin valor | Hecho | `parametros.yaml` (`liquidez_m15_mecha_que_vuelve`) |
| 18 | F5: S-7, recuadro en VIDEO-JULIO | Hecho | VIDEO-JULIO.md:808-812 |
| 19 | F5: S-2, B-15, días gastados | Hecho | informe:589-613 |
| 20 | F6: paráfrasis entera en el informe | Hecho | informe:624-634 |
| 21 | F6.1: recuadros en FTMO-REGLAS (R13 y §4) y RESPUESTAS-FTMO | Hecho | ver a4 |
| 22 | F6.2: A-54 y los cuatro `freno_*` sin cambiar valor, estado ni ambigüedad | Hecho | diff de `parametros.yaml` (solo descripción); `--comprobar` al día |
| 23 | F6.3: recuadro en ADR-0082 §4 | Hecho | ADR-0082, recuadro del 2026-11-22 |
| 24 | F7.1: la auditoría, en commit propio | No hecho, en PARADA (decisión 0) | el encargo manda decirlo en la fase 0 si `knowledge validate` se queja; la línea 248 del fichero de Aleks trae «ADR-0087» (`grep -n ADR-0087`) |
| 25 | F7.2: los cuatro textos del panel | Hecho | DEMO-FTMO.md:159-166, `reloj_dia_riesgo`, ADR-0090 y FTMO-REGLAS (R2), recuadros |
| 26 | F7.3: A-16 no se cierra; recuadro en ADR-0092 §10 | Hecho | cifras comprobadas contra METODO-FIDELIDAD-RENTABILIDAD.md:886-889 |
| 27 | F7.4: propuesta de `bloqueante` | Hecho (propuesta) | decisión 5 |
| 28 | F7.5 y F7.6 | Hecho | informe:679-684 |
| 29 | F7.7: lo de la orden de cierre, con bytes | Parcial | ver b6 |
| 30 | Para la rama y la sesión siguientes | Hecho | informe:690-726 |
| 31 | Informe y tamaño de PROJECT_STATE | Parcial | 24.809 bytes (`wc -c`); a la tabla le faltan aún la CI y la PARADA final |
| 32 | Push a `fix/` y CI; dar el número del run | Parcial | run 45005647166 sobre `1a5cf2d2` (= `origin/fix/activar-sesion-08`): solo falla `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/activar-sesion-08'; la rama actual es 'fix/activar-sesion-08'»); `1 failed, 3510 passed, 102 skipped`. El número aún no está en el informe |
| 33 | PARADA final | Pendiente (va tras el revisor) | `## Estado` (informe:863) aún dice «faltan la CI de Linux y el revisor» |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | (Alcance 3) ADR-0097 descarta la alternativa (2) diciendo que la petición rechazada va «contada al día (FTMO, 2026-10-05)». Esa fuente no lo dice, y la propia rama escribe en A-54 que sigue sin respuesta. El §3 del mismo ADR sí lo cuenta bien («sin distinguir las rechazadas»). | ADR-0097, «Por que descartamos las demas», (2). FTMO-REGLAS.md, recuadro del 2026-10-05, pregunta 1: «No distingue rechazadas…». `ambiguedades.yaml`, A-54: «Sigue sin respuesta: si una petición RECHAZADA cuenta» |
| b2 | importa | (Alcance 1) La nota de F5 sobre S-4, dibujo 2, atribuye a `ev-v20-005520-80eba002` «hasta que lo rompa una vela de su color». Ni la cita ni la afirmación del ítem lo traen: la extracción lo pone en [55:41], que es justo donde acaba el ítem. | informe:599-601. Afirmación del ítem: «roto por encima con una vela de color contrario, sigue buscando alcistas y el rango queda en el mismo nivel, sin actualizarlo» (t1 0:55:41). SESION-08-EXTRACCION.md §3.4: «el mismo nivel lo dejamos hasta que puede romper con una vela…» (`[55:41]`) |
| b3 | importa | (F2, criterio ii) La explicación de 2026-07-10, de 11 a 15, dice «las órdenes enviadas tras esperar se llenan y saltan su stop (pos-o6, pos-o7, y después pos-o8)». En la bitácora solo o1 y o6 salen tras una espera; o7 y o8 se colocan sin esperar. La cadena con RN-032 puede seguir en pie, pero tal como está escrita afirma más de lo que muestra su fuente. | informe:530-533. `data/activar-sesion-08/decisiones-f2/bitacora.DIAGNOSTICO.2026-07-10.txt`: «enviada tras esperar» solo en las líneas 15 (o1) y 243 (o6); o7 (línea 249) y o8 (línea 330) sin ella; RN-032 desde la línea 336 (07:52Z); pos-o8 cerrada en la línea 345 (07:55:49Z) |
| b4 | importa | (Alcance 3 y código de F2) Hay un orden de prioridad no declarado. La comprobación del lado malo corre ANTES de enviar, y el bróker mira cierre, freno y límite de volumen ANTES que el precio. Así, una stop del lado malo que además cae en un cierre de mercado, en el corte del freno o en el límite de volumen ya no se rechaza ni gasta el punto: espera. ADR-0097 §1 dice que esos motivos «sí gastan el punto», y el informe solo declara la prioridad del lote (ADR-0081). Además, ni siquiera la del lote está escrita en el ADR. | `primitivas_broker.py:664-668` (antes de enviar) frente a `broker.py:526` (cierre), `:530` (freno), `:533` (límite) y `:535` (precio). ADR-0097 §1, segundo párrafo. Informe:478-480 (solo el lote) |
| b5 | importa | (F2.4) Un test no prueba lo que dice. El docstring de `test_el_broker_y_la_espera_miran_la_misma_cotizacion` afirma que «con la espera apagada, el broker rechaza justo en el cierre en que, con la espera encendida, la orden no se envia». El test solo corre con la espera encendida y consulta el método en dos instantes. Ningún test fija que el rechazo de `se_gasta_el_punto` caiga en `_cierre(Z)`. | `tests/unit/test_orden_lado_malo.py:234-244`; `:222-231` (no comprueba el instante del rechazo) |
| b6 | importa | (F7.7) Las correcciones de texto del §2.5 de la auditoría quedan sin preparar («la 124, a medir; la 119 y la 123 … a reclasificar … hay que localizarlas en el PS de la rama»), y el saldo de bytes las deja fuera. El encargo pedía dejarlas preparadas, con su cuenta de bytes. | informe:768-772 y :775-778 («sin las correcciones de §2.5, que no se han medido una a una») |
| b7 | menor | (Alcance 1) La descripción de `orden_stop_lado_malo` pone entre comillas «se pone igual»; la cita del ítem dice «se pone la orden igual». | `parametros.yaml` (`orden_stop_lado_malo`): «que la orden «se pone igual»»; `ev-v17-014103-8cf3e7fb`, `cita_literal` |
| b8 | menor | (Alcance 4) El informe dice del correo del 2026-11-20 que «su pie prohíbe compartirlo». La paráfrasis no lo dice y el informe no da fuente. Parece arrastrado del correo del 2026-10-05, que sí lo tenía documentado. | informe:627. FTMO-REGLAS.md, recuadro del 2026-10-05: «su pie prohíbe compartirlo» (de aquel correo) |
| b9 | menor | El reparto de los 8 tests que fallaban en main no cuadra: «los seis que esperan» son cinco (2 que vuelven, 2 que no vuelven y el del camino real); el sexto, el de `se_gasta_el_punto`, falla por otra razón. Y en DEMO-FTMO, «ese sábado» no tiene a qué referirse. | informe:449-451; `test_orden_lado_malo.py:176-231, :287`; `docs/runbooks/DEMO-FTMO.md:163` |

**Los alcances del encargo, uno por uno:**
- **(1) Tramos no citables y citas.** Contrasté contra `tramos_no_citables.yaml` las marcas que citan los recuadros, ADR-0097, A-59, A-16 y las descripciones: v20 1:00:49, 1:02:43, 1:03:54, 1:12:13 y 0:01:38-0:03:03; v21 1:23:48, 1:26:23, 1:59:33 y 2:01:34; los ítems de v17 y v19. Ninguna cae en un tramo, y las citas literales casan con su ítem, salvo b2 y b7.
- **(2) Bloque de días.** No se activó ninguna corrección como regla. Lo único es el test de F4, que congela sin tocar el motor ni RN-009 (`src/botsito/domain` fuera del diff; `strategy_spec.yaml` solo cambia una descripción).
- **(3) ADR-0097.** La regla de §1 es la del encargo, palabra por palabra en lo esencial. Separa «Dicho» de «Lectura del consultor» (§2), y la lectura copia el encargo tal cual. Reservas: b1 y b4. Lo que añade y no estaba en el encargo: la enumeración de motivos de rechazo de §1 y «Solo vale para la orden STOP en la ruptura (A-47)». Las dos son coherentes con el encargo.
- **(4) El correo de FTMO.** `grep` de frases inglesas típicas de correo y de nombres en las líneas añadidas: nada. Lo único que se cita en inglés («maximum capital allocation rule», «USD/LOT*») viene de las páginas de FTMO que ya estaban en FTMO-REGLAS. Matiz: b8.
- **(5) Cifras de corrida.** `orden_stop_lado_malo` se fijó por decisión del encargo y antes de correr. El informe:543 lo dice, y ningún valor cambió por el delta.
- **(6) Fotogramas.** El diff no nombra ningún `fr-v20` ni `fr-v21` ni `frames show` (la única mención está en una línea archivada en HISTORIA). Las lecturas de calentamiento tienen fila: la base y los `motor decisiones` (2026-11-21, marzo y junio), la corrida F2 y el test del 8 de julio (2026-11-22, junio), y los `make check`.

**Código de F2:**
- `lado_equivocado_al_colocar` reutiliza `Mercado.cotizacion` y `lado_equivocado`, y `_precio_infringido` la llama. Ya no hay segunda copia de la lógica, aunque la cotización se calcula dos veces con el mismo resultado (`broker.py:577-584`).
- La espera se lleva por (sesión, punto), sin gastar la caja ni el punto. La sección de esperas solo sale si hay alguna: sin esperas, el informe sale igual byte a byte. La bitácora nombra los dos estados.
- Los tests que cambian de sentido lo dicen en su docstring y conservan la opción anterior con `_registro_se_gasta`.
- Las cifras del informe salen igual en las salidas: base 5 rechazos `precio_invalido` al colocar y F2 «ninguno»; 6 esperas, 3 enviadas; 2026-07-02 con 45 peticiones en las dos.

#### Lo que no pude comprobar
- **Que no se abrió ningún fotograma de v20 ni de v21.** Las fechas de acceso no sirven (`find … -newerat '2026-11-21'` da 11.977 de 11.977, todos tocados al extraerse). Solo tengo la ausencia en el diff y las declaraciones de HOLDOUT.
- **Que los 8 tests de F2 fallaban con el `src/` de main y que el de F4 pasa en main.** Medirlo exige un clon desechable (comparar-con-main), que escribe. Lo que lo sustituye: `src/botsito/domain` no cambia, así que el de F4 es equivalente en main.
- **La comprobación del contrato `knowledge validate > knowledge-validate.log`** escribe un fichero, así que no la corrí. La sustituye su línea OK en `make-check.log` sobre el árbol de HEAD.
- **`spec docs --escribir`** escribe. Corrí `spec docs` sin la opción: OK.
- **`make check`** no lo corrí (escribe). Uso `make-check.log` y el run de CI.
- **La paráfrasis de FTMO contra el correo:** el correo no está en el repo, y la fuente es la paráfrasis.
- **Que el README de anexos se escribió «antes de correr»:** se commiteó con los resultados, en `f5ee88f7`.

#### Comandos ejecutados
(23 grupos de comandos de solo lectura: git log, diff y show de la rama; `contrato_rama.py`; `feedback apply --check` (exit 1); `generar_capa.py --comprobar`; `spec docs` sin escribir; Read y `cat` del ADR-0097, de los ítems citados y de `tramos_no_citables.yaml`; los diffs de spec, ADR, informes cerrados, código y tests; `pytest` de los tests de F2 y F4 y de una selección de `test_cableado.py`, en verde; `grep` de frases inglesas y de fotogramas; `wc -c PROJECT_STATE.md`; `gh run view 45005647166`. La lista entera, en su mensaje; aquí resumida, sin cambiar nada de lo de arriba.)

## Lo que se hizo con los hallazgos del revisor

- **a1 (importa), arreglado:** la comprobación `feedback apply --check` sale del contrato: la rama no
  tiene registros de feedback (nada se cierra), y la comprobación no tiene objeto.
- **a2 (menor), arreglado:** fuera el aviso de PLANTILLA del principio del informe.
- **a3 (menor), arreglado:** la columna del recuento de la fila del 2026-11-22 («lo que lee la rama
  este día») nombra también junio.
- **a4 (menor), arreglado:** el recuadro del §4 de FTMO-REGLAS dice ahora que la respuesta no contesta
  nada de lo que ese § deja abierto (de R13, solo si sus límites van al registro), y que lo de qué
  cuenta como petición lo preguntaba A-54.
- **b1 (importa), arreglado:** ADR-0097, descarte de la alternativa (2): «FTMO dijo el 2026-10-05
  que todo tipo de orden cuenta para el límite, sin distinguir las rechazadas, y no ha dicho si una
  rechazada cuenta (A-54 sigue sin esa respuesta); el freno de ADR-0067 sí las cuenta».
- **b2 (importa), arreglado:** la nota de S-4, dibujo 2, se queda con la afirmación del ítem; lo de
  «hasta que puede romper con una vela» va atribuido a la extracción ([55:41]), sin ítem.
- **b3 (importa), arreglado:** la explicación de 2026-07-10 de 11 a 15 dice ahora que solo o1 y o6
  salen tras una espera; o6 y o7 saltan su stop y o8 se llena; con esa secuencia, distinta de la base,
  RN-032 prohíbe desde las 07:52Z (comprobado en la bitácora: o8 llenada a las 07:50:14Z, su stop a
  las 07:55:49Z, ya con RN-032 prohibiendo).
- **b4 (importa), arreglado en el texto, y a la PARADA final:** el orden con los otros motivos queda
  escrito en ADR-0097 §1 y en el informe (F2): el lote de ADR-0081 manda (gasta el punto); con
  cualquier otro motivo de rechazo al colocar a la vez que el lado malo, manda el lado malo (espera).
  Es una decisión de implementación que la regla no dice; el código no cambia; va a «Lo que no me
  convence».
- **b5 (importa), arreglado:** `test_con_se_gasta_el_punto_…` fija que el rechazo cae en
  `_cierre(Z)`, y `test_el_broker_y_la_espera_miran_la_misma_cotizacion` corre las dos opciones y
  compara: el rechazo de `se_gasta_el_punto` cae en el mismo instante en que empieza la espera.
- **b6 (importa), arreglado:** las correcciones de §2.5 van preparadas con su texto y sus bytes en
  «Para la orden de cierre»; el saldo pasa a −271 (24.538 bytes).
- **b7 (menor), arreglado:** «se pone la orden igual», como el ítem (spec 19.1.4, con `spec docs`).
- **b8 (menor), arreglado:** fuera «su pie prohíbe compartirlo» para el correo del 2026-11-20; queda
  «como el del 2026-10-05; el repositorio es público».
- **b9 (menor), arreglado:** el reparto de los 8 (cinco que esperan y tres que nombran lo nuevo), y
  «el sábado 2026-11-07» en DEMO-FTMO.
- **Lo que el revisor no pudo comprobar**, contestado donde se puede: los 8 tests de F2 fallaron con
  el `src/` de `main` porque se corrieron ANTES de tocar `src/` (la rama solo había cambiado
  documentos: `git diff main -- src` vacío en ese momento), no en un clon (desviación de la skill
  `comparar-con-main`, declarada); el README de anexos se escribió en el scratchpad y se copió al
  repo antes de la primera corrida, aunque se commiteó con los resultados.

## El cierre de la rama: CI

- `git push origin trabajo/activar-sesion-08:refs/heads/fix/activar-sesion-08` sobre `1a5cf2d2`:
  **run 45005647166**, `1 failed, 3510 passed, 102 skipped`; el único fallo,
  `test_state_check_ok_on_real_repo` por el nombre `fix/` (el aceptado).
- El run del último commit (el de los hallazgos), en el mensaje final.

## PARADA final

**F1 (va siempre aquí).** A-48 (S-3): 0.3 enseña que, en el esquema inventado, `ultimo_pivote_m1` cae
en la base de la zona de control con un retroceso limpio (y coincide con «el punto más bajo de la zona
de control que valida», salvo la mecha de la vela que la abre), y se separa con estructura interna (el
0 sube al pivote interno y RN-009 cuenta dos zonas); `referencia_de_la_toma` no coincide en ninguna.
0.4, en las cuatro sesiones del bloque: el bot mueve el 0 a cada pivote nuevo (de 41 a 58 puntos
distintos por sesión), y las tres correcciones del 0 dicen que no va en la estructura interna. A-58
(S-4): el dibujo 2 es la lectura d) de hoy; el dibujo 1, la b), sin palabras que la confirmen. **El
trader no ha contestado** (ni S-3, ni A-35, ni A-43) mientras la rama estuvo abierta. Las vías, en las
decisiones 1 y 2. Nada de `orden_stop_punto`, `sesgo_h4_rango_nuevo`, A-48 ni A-58 se ha tocado.

**A-59, tal como quedó** (`knowledge/spec/ambiguedades.yaml`): título «qué haces con la orden cuando
se forma la caja y el precio ya está más allá del 0»; pregunta «Cuando se forma la caja y el precio
ya está más allá del 0, ¿qué haces con la orden: entras igual, esperas a que el 0 quede del lado
bueno, mueves el 0 o la descartas?», con lo de la sesión 6 y de la 7b citado de sus cinco ítems, la
lectura del consultor (`orden_stop_lado_malo` = `espera`, ADR-0097) y lo que se buscó en el corpus;
pregunta, no bloqueante, ABIERTA, `resuelve_en` F20 y F22.

**Los deltas.** Control (la base de esta rama) igual a la F2 de la 7a: 11 parejas y 19 de más, 86
filas idénticas. Tras F2: **10 parejas y 20 de más** (−1 y +1 contra el control; −4 y −19 contra la
línea base de 14 y 39). Las filas declaradas **casan**: 0 rechazos por precio al colocar (antes 5); las
filas que cambian son de las sesiones declaradas, salvo tres de 2026-07-10 de 11 a 15, que quita
RN-032 (freno de la cuenta); el 2026-07-02 sigue en 45 peticiones.

**Lo que quedó en PARADA** («Lo que necesito que decidas»): 0, la auditoría y ADR-0087 (F7.1); 1 y
2, F1 (A-48 y A-58); 3, dónde van las notas de S-3 y S-4; 4, la parte de E21 sin cifra; 5,
`bloqueante` de A-35 (F7.4); 6, los frenos de la cuenta antes de (3); 7, qué leyó el trader como zona
(F4).

**Lo que no me convence:**
- **El orden de F2 frente a los otros motivos de rechazo** (revisor, b4): con el 0 del lado malo, un
  cierre de mercado, el freno, el volumen, el stops level o el margen ya no gastan el punto, porque la
  orden no llega al bróker. Lo elegí por cómo está el código (la comprobación va antes de enviar) y lo
  declaré en ADR-0097; la regla no lo dice. Si prefieres que esos motivos manden, la comprobación
  tendría que ir después de los del bróker, y eso es otra API del bróker.
- **La pareja que se pierde la quita RN-032**, no la regla: la espera cambia la secuencia de la mañana
  del 10 de julio y el freno de la cuenta prohíbe antes. Es la tensión de los frenos de la cuenta que
  ACTIVAR-SESION-07.md dejó para antes de (3) (decisión 6).
- **Las láminas no enseñan la espera** (leen solo los no envíos de ADR-0081): si la sesión siguiente
  usa láminas de días con esperas, el trader no las verá dibujadas.
- **La reentrada sin ticks salía rechazada en `main`** (`test_sello_respaldo`): un test que pasaba
  sin mirar el estado. Puede haber más casos parecidos, sin medir, en los días sin ticks de la
  construcción; la corrida de (3) los dirá.
- **Las notas de S-3 y S-4** se quedan solo en el informe (decisión 3), y «la ruptura por abajo» no
  tiene ítem.
- **El encargo daba «PICO DE MEMORIA en la última línea» como señal de que la memoria cortó un `make
  check`**; es la última línea de todos (auditor). No hizo falta repetir ninguno.

## Estado

Rama lista para revisión, NO cerrada.
