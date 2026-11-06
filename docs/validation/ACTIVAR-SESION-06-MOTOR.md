# ACTIVAR-SESION-06-MOTOR · El motor de la activación de la sesión 6 (R4.2, entrada F)

Rama `trabajo/activar-sesion-06-motor`, abierta el 2026-11-05 desde `main` en 04ec025 (commit de
estado sobre el merge df0e672 del tag `stable/F38n-activar-sesion-06`). Encargo:
`docs/encargos/trabajo-activar-sesion-06-motor.md`.

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `04ec0251ba6d80e713535bc2fdbabee8511db3a8` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F38n-activar-sesion-06^{commit}"` = `df0e6721dc72fea62990163e1ec7a94ad5a4c127` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F38n-activar-sesion-06` da `eec74e4a…` (el objeto del tag anotado).
- CI de `main`: `gh run view 42147004153` → `status: completed`, `conclusion: success`, `headSha: 04ec0251ba6d80e713535bc2fdbabee8511db3a8`, `headBranch: main`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## 0. El encargo frente al repo (auditor)

El subagente `auditor-encargo` contrastó el encargo con el repo antes de medir: 54 afirmaciones,
35 correctas, 5 incorrectas y 14 con matiz; 10 herencias que el encargo no recoge. Lo que cambia el
trabajo, con lo que hice con cada cosa:

| # | Lo que dice el encargo | Lo que mide el repo | Qué hago |
|---|---|---|---|
| 15 | S-4: «la vela sin cuerpo no corta la racha», como dicho del trader | No lo dijo: «que no corta la racha es la conclusión de la extracción» (las notas de `ev-v17-002155-f2c95111`; `ambiguedades.yaml`, A-35). Es el error de `ERRORES-RECURRENTES.md:108`, repetido | El recuadro de ADR-0085 y el docstring lo dicen como conclusión de la extracción y lectura del consultor; los tres ítems, por lo que dice cada uno (la mecha como alto, dos o tres seguidas, en un bajo igual) |
| 22 | `test_pivotes_m15.py:149` cambia de sentido | No se rompe: llama a `pivotes_formados` con el valor por defecto (`corta_la_racha`), que no cambia. Medido en el clon (b.4): el prototipo de la fase 2 no rompe ningún test | Se reescribe A PROPÓSITO, como manda el encargo: prueba M15 con la lectura nueva y conserva una línea que dice que el valor por defecto sigue cortando |
| 26 | S-22 se aplica a `ultimo_punto_de_ruptura` «con las dos lecturas de `orden_stop_punto`» y NO a `referencia_del_breaker` | `ultimo_punto_de_ruptura` con `hasta` en la toma ES, por diseño, el pivote de `referencia_del_breaker` (`estructura_m1.py:204-206`), y `zonas.py:381` lo usa así con `referencia_de_la_toma`. Las dos órdenes del encargo se contradicen con esa lectura | PARADA, fase 3 (abajo) |
| 29, 30 | `test_estructura_m1.py:219` cambia «seguro» y `:65` «solo con (b)» | `:219` prueba `zona_posterior_completada` (RN-014) y `:65` prueba `referencia_del_breaker`: ninguno pasa por `ultimo_punto_de_ruptura`. Los que cambian son otros 20 tests, en 6 ficheros (b.4) | Al informe; fase 3 en la PARADA |
| 33 | Con `precio_invalido` «no marca, la zona sigue viva y la orden se vuelve a colocar» | `marcar_usada` se llama en `primitivas_broker.py:654`, ANTES del `isinstance(r, Rechazo)`: la caja queda usada y `toca_colocar_orden_limite` la descarta (`zonas.py:494-499`). Y nada espera a que el 0 quede del lado bueno: cada cierre de M1 volvería a enviar la orden, con su petición rechazada | PARADA, fase 4 (abajo) |
| 38 | 37 de 1.329 órdenes | La cifra existe (`ACTIVAR-SESION-06.md:201` y `:545`), pero sale de las corridas de RESPALDO-M1 del 2026-10-29, anteriores a los cambios de parámetros de F38n: no es la del motor de hoy | Se cita con su fecha y su corrida; no se vuelve a medir (no hace falta para decidir) |
| 43 | b.3 «con el arnés en el modo autorizado» | El arnés no tiene opción para las lecturas nuevas y su salida no imprime pivotes | Medido con el arnés EN PROCESO y una observación sin efecto (b.3): la corrida es la de `main` |
| H1 | — | El ADR de la fase 1 (número 0089) citado sin bloque `ids-inexistentes`: el primer `make check` de la apertura salió en rojo (5 failed, los cinco por ese id) | Bloque añadido al encargo, como en `trabajo/activar-sesion-05-motor`; el segundo `make check` selló |
| H2 | Cerrar A-44 reescribe el test de control de la sesión 6 | También rompe el de la sesión 5: `test_en_parte_no_se_cierra.py:98` y `:102` exigen A-44 «en parte» y ABIERTA | Se reescriben los dos A PROPÓSITO, con el motivo en su docstring |
| H3 | — | Los cinco sitios de A-44 incluyen RN-020 («El reloj del reinicio sigue UNKNOWN… A-44 SIGUE ABIERTA», `strategy_spec.yaml:2085-2087`) y las descripciones de `perdida_trader_alcance`, `perdida_trader_magnitud` y `perdida_trader_reinicio_huso` | Entran en el commit del cierre de A-44 |
| H4 | — | El texto de A-35 («el motor hoy la corta … va a la rama de motor», `ambiguedades.yaml:997-1000`) deja de ser verdad con la fase 2 | Entra en el commit de la fase 2, con `spec docs --escribir` |
| H5 | — | `tests/unit/test_hoja_preguntas.py:30` copia el orden con A-44 | Entra en el cierre de A-44 |
| H6 | — | La skill `activar-sesion` dice «"En parte" no se cierra» y «lo fijado no se pisa: si contradice un ADR, PARADA» | Choque declarado abajo |
| H7 | — | RN-007 tiene `cita` y `literal` propios | No aplica: la fase 3 no se hace |
| H8 | — | `scripts/embudo_77.py` llama a `ultimo_punto_de_ruptura` (`:712`) y a `tope_del_registro` (`:439`) | La fase 1 le llega por `cableado` sin tocarlo; se declara como deuda de guiones con los otros dos |
| H9 | — | `docs/runbooks/ACTIVAR-A35-A44.md:71` y `:126-127` siguen diciendo que el reinicio es `perdida_trader_reinicio_huso`, y no está en las rutas del contrato | No se toca; va a la deuda del informe |
| H10 | — | La deuda «Una zona del productor reutilizada en un escenario nuevo» (Technical Debt) toca la vida de la zona que S-19 cambia | Al informe, con la fase 4 |

Matices que no cambian lo pedido: 9 (con `alcance = dia` el corte de semana no tiene efecto hoy;
los tests de la semana van con un tope sintético `ambos`); 10 (`PROJECT_STATE.md:101` reserva el
0087 para S-15, no dice «no se rellena»: el ADR de la fase 1 se numera 0089 igual); 25 y H8 (`embudo_77.py`); 28
(«con cuerpo o con mecha» ya está en `ev-v17-015307-0870a8ca`; el «m15» dudoso solo en
`ev-v17-015404-06ac0e9d`); 34 (quien escribe el conjunto es `zonas.py:422`; los tres llamadores son
los del encargo); 35 (al colocar también rechazan el cierre de mercado y el freno,
`broker.py:511-517`); 46 (el tope del test es 25.000; los 23.000 son el margen del consultor);
53 («Fechas fijas» es una sola viñeta con la ejecución 2 y la 3, `HOJA-DE-RUTA.md:653-654`); 54
(«diagH\» no aparece en el repo: lo copio tal cual en la línea F preparada y lo señalo).

### Choques del encargo con las skills (ganan ellas, y lo digo)

- **«En parte» no se cierra** (`activar-sesion`, Límites). A-44 se cierra porque su «en parte» de
  S-2 fue por falta de opción en el enum, no por la respuesta (`SESION-06-EXTRACCION.md:768`, regla
  general «sí»): lo decide el consultor en el encargo (fase 1.5) y lo dicen el registro, el docstring
  de los dos tests de control y el recuadro de la extracción.
- **Lo fijado no se pisa; contra un ADR, PARADA** (`activar-sesion`). Las fases 3 y 4 enmiendan
  decisiones de ADR (ADR-0085 §3 y ADR-0083 D1) con recuadro, como pide el encargo; las dos quedan en
  la PARADA por otros motivos (abajo).
- **Ningún cambio de motor sin un test que falle antes** (`activar-sesion`): cada fase hecha lleva
  el suyo, probado en un clon de `main` (`comparar-con-main`).

## a. Tabla de las cuatro fases

| Fase | Hoy en el código | Llamadores | Test que lo prueba hoy | Criterio del encargo | ¿Cuadra? |
|---|---|---|---|---|---|
| 1 · S-2 | `SeguidorTope.avanzar` corta en la medianoche de `huso_reinicio` (`engine/tope_trader.py:230-240`); sin huso, el del perfil marcado SUPUESTO (`:191-194`) | `SeguidorTope(` solo en `engine/cableado.py:267`; `tope_del_registro` en `cli.py:2398` y `:2521` y en siete guiones de `scripts/` (corregido tras el revisor, a1: decía «en `cableado`», que no lo llama; §l) | `tests/unit/test_preparar_a44.py:145-162` (asierta `huso_supuesto`) y `:254-302` (los cortes) | el seguidor solo lo construye `cableado.py`; `primero` es la apertura en UTC; nadie más lee `perdida_trader_reinicio_huso` | **SÍ** (b.1) |
| 2 · S-4 | M15 con `corta_la_racha` (`domain/pivotes_m15.py:100-116`); M1 con `no_cuenta` (`domain/estructura_m1.py:135-137`) | `pivote_mas_reciente`: solo `engine/motor.py:156`; `pivotes_formados`: `estructura_m1.py:135` (M1, `no_cuenta`) y dos guiones con M1 sin `sin_cuerpo` | `tests/unit/test_pivotes_m15.py:149` | el único llamador de M15 es `motor.py` y el de M1 pasa `no_cuenta` | **SÍ** (b.1) |
| 3 · S-22 | el punto se forma con cualquier contraria que cierra tras la racha (`estructura_m1.py:201-224`) | `ultimo_punto_de_ruptura`: `engine/zonas.py:382` (con `hasta = idx_toma + 1` si `orden_stop_punto = referencia_de_la_toma`, `:381`) y `scripts/embudo_77.py:712`; `_pivotes_m1`: `:124` (`referencia_del_breaker`), `:167` (`zonas_de_control`), `:212` | 20 tests en 6 ficheros (b.4) | un único sitio del dominio y los demás usos de `_pivotes_m1` separables sin tocarlos | **NO** en lo que decide: la condición SÍ se puede poner solo en `ultimo_punto_de_ruptura` sin tocar `_pivotes_m1`, pero la decisión deja abierto qué es el punto cuando el último pivote no vale, y choca con la identidad del punto de la toma (PARADA) |
| 4 · S-19 | el rechazo al colocar marca la caja usada (`primitivas_broker.py:654`) y gasta el punto (`:655-659`) | `marcar_rechazada`: `primitivas_broker.py:639` (no envío), `:659` (rechazo al colocar), `cableado.py:165` (rechazo al llenar); el conjunto lo escribe `zonas.py:422` | `tests/unit/test_punto_usado.py:343` | los únicos que escriben «rechazados» son esos tres y el Rechazo llega a `:655` con su motivo | **NO** en lo que decide: el criterio se cumple, pero la premisa de la decisión no («no marca y la zona sigue viva»: la caja ya está usada en `:654`), y lo que hace el motor después no está decidido (PARADA) |

## b. Lo medido

### b.1 Los llamadores

Con `Grep` sobre `src/` y `scripts/` (y `tests/` donde se dice):

- `SeguidorTope(`: `src/botsito/engine/cableado.py:267` (el único); en tests, `test_preparar_a44.py`.
  `primero` es `min(d for _, d, _ in limites)` con `limites` de `dia.limites()`
  (`cableado.py:245-246`), en minutos UTC «por la puerta» (ADR-0069; `engine/motor.py:185-186`): la
  apertura de la primera sesión del día en UTC.
- `perdida_trader_reinicio_huso`: `engine/tope_trader.py:51` y `:192`; fuera, solo los tests
  (`test_preparar_a44.py:97`, `:219`) y el texto de la spec y de `knowledge/cases/kit/mapa_parametros.yaml:53`.
- `pivote_mas_reciente`: `engine/motor.py:156` (M15, sin `sin_cuerpo`). `pivotes_formados`:
  `domain/estructura_m1.py:135-137` (M1, `sin_cuerpo=SIN_CUERPO_NO_CUENTA`),
  `scripts/bloque_de_la_caja.py:204` y `scripts/caja_77_exploratoria.py:175` (M1, sin `sin_cuerpo`:
  leen con `corta_la_racha` y divergen de `estructura_m1.py`; deuda de guiones, no se tocan).
- `_pivotes_m1`: `estructura_m1.py:124` (`referencia_del_breaker`), `:167` (`zonas_de_control`) y
  `:212` (`ultimo_punto_de_ruptura`). `ultimo_punto_de_ruptura`: `engine/zonas.py:382` y
  `scripts/embudo_77.py:712`.
- `marcar_rechazada`: `engine/primitivas_broker.py:639` y `:659`, `engine/cableado.py:165`; la
  función escribe el conjunto en `engine/zonas.py:422`. `marcar_usada` va antes del rechazo en
  `primitivas_broker.py:654`.

### b.2 Lo que queda de A-44

Su pregunta (`ambiguedades.yaml`, A-44): «¿Hay alguna pérdida a partir de la cual dejas de operar?
¿Cuándo vuelves a empezar a contar?». Sus diez parámetros, leídos con un guion de la carpeta de
trabajo (`estados_a44.py`, solo lee `parametros.yaml` y `ambiguedades.yaml`):

| Parte | Parámetro | Hoy | Regla general |
|---|---|---|---|
| alcance | `perdida_trader_alcance` | CONFIRMED `dia` (`fb-2026-10-23-sesion-05-e9559876`) | sesión 5 |
| unidad | `perdida_trader_unidad` | CONFIRMED `porcentaje` (`fb-2026-10-23-sesion-05-1772d9ef`) | sesión 5 |
| magnitud | `perdida_trader_magnitud` | CONFIRMED `saldo` (`fb-2026-11-04-sesion-06-a1f5784d`) | sesión 6, S-1 |
| cifra del día | `perdida_maxima_diaria`, `base_calculo_perdida_diaria` | CONFIRMED 4,5 sobre `saldo_inicial_dia` (sesión 1) | sesión 1 |
| semana | `perdida_maxima_semanal`, `base_calculo_perdida_semanal` | CONFIRMED, SIN EFECTO con `alcance = dia` | sesión 5 |
| dinero | `perdida_trader_dia_usd`, `perdida_trader_semana_usd` | UNKNOWN, sin efecto con `porcentaje` | sesión 5 |
| reinicio | `perdida_trader_reinicio_huso` | UNKNOWN; el motor usa el corte del perfil, SUPUESTO | **sin regla hasta la fase 1**: con `perdida_trader_reinicio = primera_sesion_dia_siguiente` (S-2, `ev-v17-000250-a468bcec`) queda SIN EFECTO |

Con la fase 1 ninguna parte queda sin regla general: A-44 pasa a RESUELTA (fase 1.5).

### b.3 Los recuentos de las fases 2 y 3

**Antes de correr**, la compuerta (guion `recuentos.py` de la carpeta de trabajo, la raíz por
argumento, ninguna clave impresa): `casos_reservados` 34 (2026-05: 13; 2026-06: 11; 2026-09: 10) y
`casos_ocultos` 34, el mismo reparto; **0 en los cuatro meses de construcción**.

**Cómo:** el guion `medir_f2_f3.py` de la carpeta de trabajo corre el arnés EN PROCESO con
`motor arnes --simular --diagnostico-cuenta-diaria --salida <carpeta de trabajo>` (diagnóstico
etiquetado, no cuenta: ADR-0070 §3; la construcción por defecto, sin `--meses`) y OBSERVA dos
funciones sin cambiar lo que devuelven: la corrida es la de `main` (la salida la nombra
`diagnostico.nombre_etiquetado`: `diaria.DIAGNOSTICO.cuenta=diaria.txt`, en la carpeta de trabajo;
no se commitea ni se lee más que su línea `OK`). Fase 2: cada llamada de `engine/motor.py` a
`pivote_mas_reciente` se repite con la lectura nueva (la vela de cuerpo cero no corta y entra; las
de por delante del primer color, no), una copia de `_racha_anterior` en el guion. Fase 3: cada punto
que `ultimo_punto_de_ruptura` da al productor (`zonas.py:382`) se mira con (a) la contraria pasa con
la mecha el extremo opuesto de la ÚLTIMA vela con color de la racha y (b) el de TODA la racha (las
de cuerpo cero no entran, como en M1). Dos corridas (la segunda con las categorías de la fase 2
afinadas): `TIEMPO: 452.1 s; MEMORIA: pico del proceso de 640.2 MiB` y `TIEMPO: 428.5 s; MEMORIA:
pico del proceso de 640.3 MiB`, `exit=0` las dos, los mismos recuentos. Solo recuentos:

**Fase 2 (M15):**

| Mes | Llamadas | Con resultado distinto | Pivotes distintos consultados | Que cambian de nivel o de instante | Por qué cambian (parejas distintas) |
|---|---|---|---|---|---|
| 2026-01 | 23.237 | 335 | 208 | 4 | 3 otro pivote (otra contraria), 1 el mismo con otro nivel |
| 2026-04 | 23.477 | 160 | 196 | 1 | 1 otro pivote |
| 2026-07 | 15.073 | 247 | 114 | 3 | 3 otro pivote |
| 2026-08 | 24.198 | 422 | 200 | 5 | 5 otro pivote |
| **Total** | 85.985 | 1.164 | 718 | **13** | 12 otro pivote, 1 otro nivel; ninguno aparece donde `main` no daba ninguno |

«Otro pivote» es el caso de la vela sin cuerpo entre la racha y la contraria: con `corta_la_racha`
la racha se cortaba y el más reciente era otro, más antiguo; con la lectura nueva la contraria
forma el suyo.

**Fase 3 (puntos de breaker):**

| Mes | Puntos distintos | No se forman con (a), la última verde | Con (b), toda la racha |
|---|---|---|---|
| 2026-01 | 1.618 | 787 | 1.090 |
| 2026-04 | 1.528 | 804 | 1.065 |
| 2026-07 | 1.015 | 523 | 685 |
| 2026-08 | 1.540 | 836 | 1.072 |
| **Total** | **5.701** | **2.950 (52 %)** | **3.912 (69 %)** |

«Puntos distintos» son todos los que el productor vio en algún cierre de M1 (los intermedios
incluidos), no las órdenes colocadas.

### b.4 Los tests que cambian de sentido (en un clon de `main`)

Un clon desechable de `main` (`git worktree add --detach` en la carpeta de trabajo, con
`config/settings.local.toml` hacia el `data/` real), con el prototipo de cada fase y 31 ficheros de
test del motor (los que nombran pivotes, el punto, el cableado o el arnés):

- **Fase 2** (la lectura nueva y `motor.py` pidiéndola): `exit=0`, **ningún test falla**; tampoco
  `test_pivotes_m15.py:149`, que usa el valor por defecto.
- **Fase 3** (la lectura (a) en `ultimo_punto_de_ruptura`, saltando el pivote que no vale): **20
  fallan** en 6 ficheros: `test_caja_hasta_el_llenado.py` (2), `test_caja_lado_de_ruido.py` (2),
  `test_escenarios_por_sesion.py` (1), `test_orden_en_el_0_con_mecha.py` (1),
  `test_orden_stop_pivote.py` (9, entre ellos `test_son_las_funciones_de_r5_y_r6_de_caja_77`, que
  compara con el guion protegido `scripts/bloque_de_la_caja.py`, y
  `test_con_la_referencia_de_la_toma_el_punto_no_se_mueve`) y `test_velas_sin_cuerpo_m1.py` (5, los
  de ADR-0085: V, sin cuerpo, R ya no da el punto si la roja no pasa el mínimo de la verde). Ni
  `test_estructura_m1.py:65` ni `:219`.
- **Fase 1** cambia `test_preparar_a44.py:145-162` (asierta `huso_supuesto`): el diff de sentido, con
  la salida de `main`, va en la sección de la fase.
- **Fase 4**: no se prototipó (PARADA).

El clon se devolvió a `main` (`git checkout -- src`) tras cada prototipo; se quita al final de la rama.

### b.5 El flaky de `test_valores.py`

`tests/unit/test_valores.py:50-62`, `test_ida_y_vuelta_por_yaml_sin_perdida`: `@given` sin
`@settings` (no hay perfil de Hypothesis en el repo: solo `test_agregacion.py:305` pone
`deadline=None`), y cada ejemplo crea un directorio, escribe un YAML y lo lee: es IO de disco
dentro del plazo de 200 ms de Hypothesis. Lo que se registró en el cierre de F38n (352 ms frente a
200 ms, luego 15 ms al repetir) es exactamente el `Flaky` por `DeadlineExceeded` de Hypothesis: un
ejemplo lento la primera vez y rápido al repetirlo. Es solo el plazo: `@settings(deadline=None)`, en
un commit propio, como `test_agregacion.py:305`. (La cifra del cierre no está en el repo: la da el
encargo.)

### b.6 El tamaño de PROJECT_STATE

`git show main:PROJECT_STATE.md | wc -c` = 22.615; en la rama, tras la apertura, 22.732. El tope del
test es 25.000 (`tests/unit/test_project_state.py:21`); el margen del consultor, 23.000. Con la
fila de A-44 fuera de Known Ambiguities y la F preparada (§«Las líneas del cierre»), el tamaño
final se mide con `wc -c` en el informe final, simulando el cierre en memoria.

## c. El plan de commits

1. La apertura (hecho: encargo, contrato, Archivo 57).
2. Esta fase 0 y la PARADA, con su fila en HOLDOUT-EXPOSICIONES.
3. El flaky: `@settings(deadline=None)` en `test_valores.py`.
4. Fase 1: `perdida_trader_reinicio` (UNKNOWN → CONFIRMED por su registro), `tope_trader.py` y
   `cableado.py`, su ADR (el número 0089) con los recuadros de ADR-0053 §3.3 y §9 y sus filas del índice, los
   tests; `spec_version`, manifiesto y docs.
5. El cierre de A-44: su registro, los cinco sitios, `test_kit.py`, la hoja y su test, los dos tests
   de control y el recuadro de SESION-06-EXTRACCION.
6. Fase 2: `no_corta_y_cuenta`, `motor.py`, el recuadro de ADR-0085 §2 y su fila, el texto de A-35,
   los tests.
7. El informe: lo hecho, las líneas del cierre, el revisor.

Las fases 3 y 4 no tienen commit: se quedan en la PARADA.

## Lo que no pude medir

- **Que las dos corridas de b.3 salgan iguales byte a byte**: la guardia niega `cmp` sobre la salida
  («no sabe con qué se ejecuta `diaria.DIAGNOSTICO.cuenta=diaria.txt`»): toma el nombre del fichero
  por un programa. No la rodeé. Los recuentos de las dos son idénticos. Hallazgo de guardia
  (**menor**): entrada propuesta para el carril de guardias, «`cmp` y `diff` de dos ficheros de datos
  se leen como ejecutar».
- **Cuántos minutos queda el precio del lado malo del 0** en las órdenes de S-19 (lo que diría cuántas
  peticiones de más haría un reintento por cierre): pide simular con el cambio, y la autorización de
  las corridas es para medir las fases 2 y 3.
- **La cifra de 37 de 1.329 con el motor de hoy** (auditor, 38): no hace falta para decidir.

## Exposiciones

Fila del 2026-11-05 en `HOLDOUT-EXPOSICIONES.md`, en el commit de esta fase 0: (1) las dos corridas
del arnés de b.3 (diagnóstico, construcción, con la salida en la carpeta de trabajo), que leen las
M1 y los ticks de enero, abril, julio y agosto y, para calentar el sesgo H4, el M1 de marzo, junio y
julio, como las de RESPALDO-M1 (`anexos/RESPALDO-M1/README.md`); de ellas, solo los recuentos de
b.3; (2) `casos_reservados` y `casos_ocultos`, solo recuentos por mes; (3) el clon desechable de b.4,
cuyos tests leen el M1 de marzo como cada `make check`; (4) el auditor del encargo, que contó con
`grep -c` en las salidas de RESPALDO-M1 y vio una línea con un día de enero (desarrollo). Ningún
libro, imagen, fotograma, transcripción ni caso; ningún listado de `knowledge/cases`.

## d. La PARADA (condicional: el encargo corre de noche)

- **Fase 1 · S-2: CUADRA, se hace.** Y con ella A-44 pasa a RESUELTA (b.2).
- **Fase 2 · S-4: CUADRA, se hace.** 13 de 718 pivotes de M15 cambian (b.3); ningún test se rompe.
- **Flaky: es solo el plazo, se hace** en su commit.
- **Fase 3 · S-22: NO CUADRA, se deja, sin tocar su código.** La condición cabe en
  `ultimo_punto_de_ruptura` sin tocar `_pivotes_m1`, así que la letra del criterio se cumple; pero al
  medir salen dos cosas que la decisión no zanja y que mueven medio motor:
  1. **Qué pasa cuando el último pivote no vale.** Con (a) dejan de formarse 2.950 de 5.701 puntos
     (52 %). Si el punto es «el último pivote QUE VALE» (lo que probé en el clon), la orden va a un
     pivote más antiguo, a otro nivel; si es «ninguno hasta que uno valga», en esos cierres no hay
     orden. Las dos son lecturas de «para validar el punto» y dan motores distintos en la mitad de
     los puntos.
  2. **El punto de la toma.** Con `orden_stop_punto = referencia_de_la_toma` el punto de la orden es,
     por diseño, el pivote de `referencia_del_breaker` (`estructura_m1.py:204-206`, `zonas.py:381`).
     El encargo pide la condición «con las dos lecturas» y NO en `referencia_del_breaker`: con esa
     lectura el punto de la orden y la referencia que el breaker tiene que pasar dejarían de ser el
     mismo nivel. Hoy el valor es `ultimo_pivote_m1` (DEFAULT_AMBIGUOUS), así que no se nota, pero hay
     que decidirlo antes de escribir el código.
  Además rompe 20 tests en 6 ficheros (b.4), entre ellos la comparación con CAJA-77, que habría que
  reescribir como en ADR-0085 («la única diferencia es este punto»).
  **Alternativa que veo:** decidir 1 y 2 (abajo) y hacer la fase en una rama propia, antes de la
  re-corrida que cuenta; la lectura (b) y el «m15» dudoso, a la sesión 7 como ya estaba previsto.
- **Fase 4 · S-19: NO CUADRA, se deja, sin tocar su código.** El criterio se cumple (los tres
  llamadores, y el Rechazo llega a `:655` con `r.motivo`), pero la premisa no: la caja ya está usada
  en `primitivas_broker.py:654`, así que no marcar el rechazo no deja la orden «volver a colocarse»
  con la misma caja (con `caja_se_fija = en_cada_cierre_m1`, solo con otra caja del mismo punto). Y
  «en el siguiente cierre en el que el 0 vigente quede del lado bueno» no lo hace nadie: hoy el
  motor la volvería a enviar en cada cierre de M1 y el broker la rechazaría cada vez, con su
  petición contada al día (el freno de bucles no salta: 5 iguales en 1 minuto, `parametros.yaml`,
  `freno_bucle_repeticiones` y `freno_bucle_minutos`, DEFAULT_AMBIGUOUS bajo A-54; pero cada
  rechazo cuenta para el corte del día y para A-54).
  **Alternativa que veo:** con `precio_invalido` al colocar, ni la caja queda usada ni el punto
  gastado, y la orden NO se envía mientras la cotización del cierre la deje del lado malo (la misma
  comprobación de `broker.lado_equivocado`, sin petición); se envía en el primer cierre en que valga
  (RN-006 la mueve si el punto cambió). Es una decisión de ejecución nueva (no enviar), y por eso la
  pido.

## Lo que necesito que decidas

0. Fase 3, el pivote que no pasa la condición. Opciones: (a) el punto es el último pivote QUE VALE
   (se salta el que no); (b) no hay punto hasta que se forme uno que valga. Recomiendo (a): es la
   lectura literal de «el último punto formado», y el trader dijo cuándo un pivote ES punto, no que
   deje de haber punto. Coste de (b): en la mitad de los cierres con un punto nuevo no habría orden.
1. Fase 3, el punto de la toma con `referencia_de_la_toma`. Opciones: (a) la condición vale también
   allí y `referencia_del_breaker` queda como está, aceptando que con esa lectura (hoy no vigente)
   el punto de la orden y la referencia del breaker se separen; (b) la condición solo con
   `ultimo_pivote_m1`, y con `referencia_de_la_toma` el punto sigue siendo la referencia. Recomiendo
   (b): conserva la definición de `referencia_de_la_toma` («el pivote que el breaker tiene que
   pasar») y la lectura vigente recibe la regla entera. Coste de (a): dos niveles distintos con el
   mismo nombre.
2. Fase 3, dónde se hace. Opciones: (a) en una rama propia antes de la re-corrida que cuenta, con
   20 tests reescritos y la comparación de CAJA-77 al estilo de ADR-0085; (b) junto con la sesión 7,
   tras confirmar la mecha. Recomiendo (a): la regla está dicha dos veces y la re-corrida tiene que
   llevarla. Coste de (b): la re-corrida sale sin ella y habría que repetirla.
3. Fase 4, qué hace el motor tras un rechazo por precio inválido. Opciones: (a) no enviar mientras
   la cotización del cierre la deje del lado malo, y enviar en el primer cierre en que valga, sin
   gastar caja ni punto; (b) reenviar en cada cierre y dejar que el broker la rechace, sin gastar
   caja ni punto; (c) lo de hoy hasta la sesión 7. Recomiendo (a): es lo que dice la decisión («en el
   siguiente cierre en el que el 0 vigente quede del lado bueno») sin peticiones rechazadas a la
   firma (A-54). Coste de (b): una petición rechazada por minuto mientras dure, contada al día.
4. Fase 4, la caja. Con (a) o (b) del punto 3 hace falta que la caja no quede usada en `:654` cuando
   el rechazo es por precio inválido (o liberarla, como `liberar_usada`). Opciones: (a) no marcarla;
   (b) marcarla y liberarla en el mismo sitio. Recomiendo (a), por claridad. Coste de (b): ninguno
   salvo leerse peor.
5. La guardia y `cmp` (b.3). Opciones: (a) entrada en el carril de guardias para que `cmp` y `diff`
   de dos ficheros que no son guiones no se lean como ejecutar; (b) dejarlo. Recomiendo (a).

Mientras, la rama sigue con lo que cuadra: el flaky, la fase 1 con el cierre de A-44 y la fase 2.

## e. Tras la PARADA: lo que se hizo

La PARADA es condicional (encargo, «Esta rama corre sola de noche»): commiteada en d091c6c, la
rama siguió con lo que cuadra. Las fases 3 y 4 no se tocaron: ni su código ni sus tests.

| Commit | Qué | `make check` (sello, duración, pico) |
|---|---|---|
| b2f3562 | La apertura | `1ba8802d…`, 1223 s, 306 MiB (el primero, sin el bloque `ids-inexistentes`, salió en rojo: 5 failed) |
| d091c6c | Fase 0 y PARADA | `bb23d948…`, 1127 s, 309 MiB |
| 3f2bef2 | El flaky | `b3140c4e…`, 1197 s, 305 MiB |
| ed09769 | Fase 1 | `f278f084…`, 1086 s, 307 MiB (el primero salió en rojo: 1 failed, `test_state_check_ok_on_real_repo`, el recuento de tests de PROJECT_STATE sin subir; corregido y repetido) |
| 2a3cf76 | Cierre de A-44 | `b915dc4b…`, 1164 s, 305 MiB |
| e3adb44 | Fase 2 | `2bd43dc8…`, 1096 s, 306 MiB |

### e.1 Fase 1 · S-2 (ed09769)

- **Parámetro:** `perdida_trader_reinicio` (estrategia, enum `[medianoche_huso,
  primera_sesion_dia_siguiente]`, `consumido_por: [ADR-0089]`), nace UNKNOWN y queda CONFIRMED
  `primera_sesion_dia_siguiente` por `fb-2026-11-04-sesion-06-6886938e` (RESOLVE_UNKNOWN sobre el
  parámetro, t0 0:02:50, t1 0:03:15, notas solo con `ev-v17-000250-a468bcec`; el del viernes, en la
  descripción). `feedback apply --check` propuso solo ese (`+ perdida_trader_reinicio`, «1 cambian,
  3 ya estaban»). `perdida_trader_reinicio_huso` sigue UNKNOWN, «SIN EFECTO con
  perdida_trader_reinicio = primera_sesion_dia_siguiente». Sin el parámetro, el motor hace lo de
  antes (medianoche): no se adivina.
- **Motor:** `engine/tope_trader.py` (`TopeTrader.reinicio`; `tope_del_registro` no lee el huso ni
  marca SUPUESTO con la primera sesión; `SeguidorTope.abrir_dia` corta el día en la apertura y la
  semana si cambia la semana ISO respecto al último día con actividad; `avanzar` no corta con ese
  valor; la descripción dice «reinicio al abrir la primera sesion del dia siguiente (de sesion en
  sesion)»). `engine/cableado.py`: `abrir_dia(dia.dia, apertura, saldo)` al empezar cada día que
  corre, con la apertura de `primero` (UTC) y el saldo arrastrado.
- **ADR-0089** nuevo; recuadros en ADR-0053 §3.3 y §9; filas del índice de 0053 y 0089. El id sale
  del bloque `ids-inexistentes` del encargo.
- **Tests:** `tests/unit/test_reinicio_tope_trader.py` (8): bases distintas cuando el saldo cambia
  entre la medianoche y la apertura, la misma cuando no (con el instante del corte distinto), viernes
  → lunes, lunes sin sesiones, el mismo día otra vez, la medianoche sin efecto de `abrir_dia`, y los
  dos que fallan con `main`: el registro real y el cableado real con dos días seguidos (el mercado
  sintético de `test_cableado` y el mismo desplazado un día; correr dos veces el mismo día no se puede:
  la cuenta no retrocede).
- **Cambia de sentido A PROPÓSITO:**
  `test_preparar_a44.py::test_con_el_registro_real_el_tope_es_el_del_dia_en_porcentaje_sobre_el_saldo`
  (`:145-166`). Antes: `assert t.huso_supuesto and t.huso_reinicio is HUSO_PERFIL and SUPUESTO_HUSO
  in t.descripcion()`. Ahora: `assert t.reinicio == PRIMERA_SESION_DIA_SIGUIENTE` y `assert not
  t.huso_supuesto and SUPUESTO_HUSO not in t.descripcion()`.
- **Contra `main`** (clon `C:/cm/m7`, `git worktree add --detach` de `main`, con
  `config/settings.local.toml` hacia el `data/` real y los dos ficheros de test de la rama
  copiados): `uv run pytest -q tests/unit/test_reinicio_tope_trader.py tests/unit/test_preparar_a44.py`
  → `exit=2`:
  ```
  E   ImportError: cannot import name 'MEDIANOCHE_HUSO' from 'botsito.engine.tope_trader' (C:\cm\m7\src\botsito\engine\tope_trader.py)
  E   ImportError: cannot import name 'PRIMERA_SESION_DIA_SIGUIENTE' from 'botsito.engine.tope_trader' (C:\cm\m7\src\botsito\engine\tope_trader.py)
  ERROR tests/unit/test_reinicio_tope_trader.py
  ERROR tests/unit/test_preparar_a44.py
  ```
  En `main` el modo no existe y el corte es la medianoche del huso del perfil marcada SUPUESTO (lo
  que asertaba el test viejo, que en `main` pasa). En la rama: los 8 nuevos y el fichero entero de
  `test_preparar_a44.py`, en verde (y en cada `make check`).
- `spec_version` 18.5.10 → **18.6.0** (parámetro nuevo).

### e.2 El cierre de A-44 (2a3cf76)

- **Registro:** `fb-2026-11-04-sesion-06-c56ec7cf`, RESOLVE_UNKNOWN sobre la ambigüedad, con
  `ev-v17-000250-a468bcec` (sus notas, solo ese ítem).
- **Los cinco sitios:** el registro de parámetros (las descripciones de `perdida_trader_alcance` y
  `perdida_trader_magnitud`, que la daban ABIERTA); `ambiguedades.yaml` (RESUELTA; los dos ítems de
  S-2 en su `evidencia`; sigue `bloqueante: true`, como A-42 RESUELTA); RN-020 (su `cuando` dice el
  corte de `perdida_trader_reinicio`, que entra en sus `parametros`, y su nota; la fecha y el id del
  ADR no caben en el `cuando`: la guardia de literales los rechaza, ADR-0002); la tabla Known
  Ambiguities de PROJECT_STATE (sale la fila); la hoja de preguntas (`scripts/hoja_preguntas.py`,
  `ORDEN_SESION_02`) con su test (`test_hoja_preguntas.py`, `ORDEN`).
- **`test_kit.py`:** bloqueantes ABIERTAS = `{A-35}`; `EN_PARTE_SESION_4` pierde A-44, con su
  línea en el comentario; `RESUELTAS` la gana.
- **Los dos tests de control, A PROPÓSITO** (`test_en_parte_no_se_cierra.py`): el de la sesión 6 y
  el de la sesión 5 (herencia 2 del auditor: el encargo solo nombraba el de la 6). Antes exigían
  A-44 ABIERTA; ahora exigen las otras ABIERTAS y A-44 RESUELTA, con el motivo en el docstring («la
  “en parte” de S-2 era por falta de opción en el parámetro, no por la respuesta»). Lo que leen de
  las tablas no cambia. `test_ninguna_en_parte_esta_resuelta` no necesita cambio: en la última
  sesión que la nombra (la 6) A-44 sale «resuelve» y «en parte» a la vez, y el lector no la cuenta
  como «solo en parte».
- **SESION-06-EXTRACCION.md**, informe cerrado: RECUADRO DE CORRECCIÓN fechado tras la tabla final
  (§5), sin tocar la tabla ni el cuerpo.
- `spec_version` 18.6.0 → **18.6.1**. No hizo falta probar nada contra `main`: no hay código.

### e.3 Fase 2 · S-4 (e3adb44)

- **Dominio:** `domain/pivotes_m15.py`, `SIN_CUERPO_NO_CORTA_Y_CUENTA = "no_corta_y_cuenta"`;
  `_racha_anterior` guarda las de cuerpo cero en un pendiente y las mete en la racha solo cuando
  aparece otra vela del color: las de por delante de la primera con color no entran. El docstring
  dice que es LECTURA DEL CONSULTOR y que «no corta la racha» es la conclusión de la extracción
  (auditor, 15). El valor por defecto sigue siendo `corta_la_racha`; M1 sigue con `no_cuenta`.
- **Motor:** `engine/motor.py`, `DatosMercado.liquidez_m15` pide `no_corta_y_cuenta`.
- **ADR-0085:** recuadro fechado en §2 y su fila del índice. El texto de A-35 en
  `ambiguedades.yaml` deja de decir que el motor la corta (`spec docs --escribir`; el hash de la
  spec no cambia, porque `ambiguedades.yaml` no entra en él: `spec manifest` dio «hash al dia», y
  `spec_version` se queda en 18.6.1).
- **Deuda de guiones** (no se tocan, contrato): `scripts/bloque_de_la_caja.py:204` y
  `scripts/caja_77_exploratoria.py:175` llaman a `pivotes_formados` sobre M1 sin `sin_cuerpo` (leen
  con `corta_la_racha` y divergen de `estructura_m1.py`); y `scripts/embudo_77.py` construye el
  motor por `cableado`, así que hereda la fase 1 y la 2 sin tocarlo.
- **Tests:** `tests/unit/test_vela_sin_cuerpo_m15.py` (7): una, dos y tres seguidas en un alto
  (140, la mecha) y en un bajo (90); en medio de la racha (entra); por delante (no entra: el ALTO es
  el de las verdes, 134); solo velas sin cuerpo antes de la contraria (nada); el test por marco (en
  M1 el punto no lleva la mecha de la vela sin cuerpo, 1110 y no 1200); y uno por el camino real.
- **Cambia de sentido A PROPÓSITO:** `test_pivotes_m15.py::test_lo_fijo_y_visible_el_doji_corta_la_racha`,
  ahora `test_en_m15_el_doji_no_corta_la_racha_y_su_mecha_cuenta`. Antes:
  `assert pivotes_formados(con_doji, …) == []`. Ahora, con `sin_cuerpo=no_corta_y_cuenta`, un ALTO
  en 115 (la mecha del doji), y con el valor por defecto, `[]` como antes. En `main` no fallaba (la
  fase 0 lo midió: el prototipo no rompe ningún test); se reescribe porque lo manda el encargo.
- **Contra `main`** (el mismo clon `C:/cm/m7`, con `test_vela_sin_cuerpo_m15.py` y
  `test_pivotes_m15.py` de la rama): `exit=2`,
  ```
  E   ImportError: cannot import name 'SIN_CUERPO_NO_CORTA_Y_CUENTA' from 'botsito.domain.pivotes_m15' (C:\cm\m7\src\botsito\domain\pivotes_m15.py)
  ERROR tests/unit/test_vela_sin_cuerpo_m15.py
  ERROR tests/unit/test_pivotes_m15.py
  ```
  Y para ver el comportamiento y no solo el import, la serie del test por el camino real (V, V, V con
  alto 134, una vela sin cuerpo con la mecha en 140 y una roja) por `DatosMercado.liquidez_m15` con
  las lecturas del registro real, con un guion de la carpeta de trabajo (`camino_real_f2.py`, la
  raíz por argumento): en el clon de `main`, `liquidez_m15(ALTO): None`; en la rama,
  `liquidez_m15(ALTO): 140`.

## f. Lo que queda para el consultor y la deuda

- **La PARADA (§d), decisiones 0 a 5**: las fases 3 y 4 y la guardia con `cmp`.
- **Deuda de guiones:** los tres de e.3.
- **`docs/runbooks/ACTIVAR-A35-A44.md:71` y `:126-127`** siguen diciendo que el reinicio es
  `perdida_trader_reinicio_huso` (auditor, H9); el contrato no lo tiene en sus rutas y no se tocó.
- **La deuda «Una zona del productor reutilizada en un escenario nuevo»** (Technical Debt) toca la
  vida de la zona que S-19 cambiaría (auditor, H10): para la rama que haga la fase 4.
- **El docstring de cabecera de `engine/tope_trader.py`** sigue contando A-44 como «lo que NO dijo»
  en su primer párrafo (historia del módulo); la parte del reinicio ya dice los dos modos.
- **Hallazgo de guardia (menor):** la guardia negó `cmp` sobre dos salidas del arnés (b.3) y un
  `for` sobre tres ficheros de evidencia (los leí con Read, uno a uno, que es la forma que propone).
  También negó cargar los tests de la hoja de ruta con una ruta calculada en el simulador del
  cierre; con rutas literales, como propone, pasó.

## g. Exposiciones tras la PARADA

Fila del 2026-11-06 en `HOLDOUT-EXPOSICIONES.md`, en el commit de este informe: los `make check` de
la rama (los de la tabla de §e, dos de ellos en rojo, y los de este informe), que leen el M1 de
marzo como siempre; el clon
`C:/cm/m7` de `main` con los ficheros de test de la rama copiados (`test_reinicio_tope_trader.py`,
`test_preparar_a44.py`, `test_vela_sin_cuerpo_m15.py`, `test_pivotes_m15.py`; sintéticos y el
registro real, sin `data/`); el guion `camino_real_f2.py` (velas sintéticas); el simulador del
cierre (`PROJECT_STATE.md`, la hoja de ruta y HISTORIA, en memoria); y Read de tres ítems de
evidencia de v17 (`ev-v17-002155-f2c95111`, `ev-v17-002250-d6ca3ef8`, `ev-v17-002217-af442f84`).
Ningún día reservado, ninguna operación con su resultado.

## h. El encargo, punto por punto

| Punto | Estado | Dónde |
|---|---|---|
| Abrir con `abrir-rama`, base comprobada, contrato R4 riesgo alto | Hecho | «Base comprobada», b2f3562 |
| Fase 0: auditor, tabla, b.1-b.6, plan, PARADA commiteada | Hecho | §0, §a-§d, d091c6c |
| Fase 1 · S-2 | Hecha | §e.1, ed09769 |
| Fase 1.5 · A-44 RESUELTA | Hecha | §e.2, 2a3cf76 |
| Fase 2 · S-4 | Hecha | §e.3, e3adb44 |
| Fase 3 · S-22 | NO CUADRA: en la PARADA, sin código | §d, decisiones 0-2 |
| Fase 4 · S-19 | NO CUADRA: en la PARADA, sin código | §d, decisiones 3-4 |
| El flaky | Hecho, solo el plazo | b.5, 3f2bef2 |
| Sin corrida que cuente; solo `--diagnostico-cuenta-diaria` sobre construcción; solo recuentos | Hecho | b.3 |
| Citas solo de los ítems nombrados; notas de cada registro solo con su ítem | Hecho | e.1, e.2, e.3 |
| Next Action y hoja de ruta sin tocar; sus líneas, preparadas | Hecho | §i |
| Makefile, `.claude/` y la guardia sin tocar | Hecho | `git diff main --stat` |
| CI de Linux por `fix/`, revisor, «Rama lista para revisión, NO cerrada» | ver §j y §k | |

## i. Las líneas preparadas para el commit del contrato del cierre

Simuladas en memoria con el guion `simular_cierre.py` de la carpeta de trabajo (la raíz por
argumento; sustituciones exactas, cada una una vez; los tests de la hoja de ruta, `a`, `b` y `c`,
vacíos; los cuatro de `test_project_state`, en verde): **PROJECT_STATE queda en 22.977 bytes** con
la F nueva y la fila de A-44 ya fuera (el ritual cambia además Current Branch, Current Feature y las
secciones de `main`, que no se simulan). La primera versión de la F, con cada fase en una frase
larga, dejaba 23.213 bytes, por encima de los 23.000: se acortó.

- **Next Action F**, sustituida entera:
  > F. Sesión 6 ACTIVADA en spec (F38n) y motor (este tag): S-2, el tope del trader se reinicia al abrir la primera sesión del día siguiente (ADR-0089); S-4, en M15 la vela sin cuerpo no corta la racha y su mecha cuenta (ADR-0085 §2); S-22 no cuadró: falta qué es el punto si el último pivote no vale (alternativa: decidirlo y hacerlo antes de la re-corrida); S-19 no cuadró: la caja ya está usada (alternativa: no enviar mientras el 0 esté del lado malo); ACTIVAR-SESION-06-MOTOR.md §d. A-44 RESUELTA. Siguiente: H (diagH\ como fase 0), R y la re-corrida que cuenta (ADR-0070 §3); después, la rama de preparación de la sesión 7 (hoja + gráficos 2 a 6 con contexto, lista en ACTIVAR-SESION-06.md §«Para la sesión 7», más el 0 como máximo corriente de S-19 y la lectura (b) de S-22). El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo. R6a en los huecos.

  «diagH\» va tal cual lo trae el encargo: no aparece en el repo (auditor, 54) y parece texto roto;
  lo corrige el consultor.
- **Hoja de ruta**, R4.2: el segundo «Estado» se sustituye por
  > - **Estado:** activada en spec (`stable/F38n-activar-sesion-06`) y en el motor en lo que cuadró (este tag, ACTIVAR-SESION-06-MOTOR.md): S-2 y S-4 en el motor y A-44 RESUELTA; S-22 y S-19 quedan en la PARADA de ese informe (§d), a decidir por el consultor.

  No dice «HECHA»: con la F viva, `test_hoja_de_ruta` (b) lo rechaza («NA:F esta HECHA y la letra
  sigue viva»), medido en la simulación. R4.3, «Depende de:» pasa a «si la hoja sale de `kit hoja`,
  J.». «Fechas fijas»: la viñeta queda «La ejecución 2, hecha el 2026-10-29 en la prueba creada ese
  día (NA:A).» (sale «la 3, del 2 al 6 de noviembre»; la ejecución 2 y la 3 iban en la misma viñeta,
  auditor, 53).
- **ERRORES-RECURRENTES**, la fila de la rama: en la sesión, el primer `make check` de la apertura
  en rojo por un id de ADR futuro sin bloque y el de la fase 1 en rojo por el recuento de tests
  (`state check` antes de `make check`, otra vez); en la columna del consultor: (1) **importa**:
  la premisa de la fase 4 («no marca, la zona sigue viva») no era la del código (`marcar_usada` va
  antes del rechazo), y la fase 3 pedía la condición «con las dos lecturas» y no en
  `referencia_del_breaker`, que con `referencia_de_la_toma` es el mismo pivote; (2) **importa**: «no
  corta la racha» se volvió a atribuir al trader (`ERRORES-RECURRENTES.md:108`); (3) **menor**: los
  tests que «cambian de sentido» de la fase 3 (`test_estructura_m1.py:65` y `:219`) prueban otras
  funciones; (4) **menor**: el encargo citaba un ADR futuro sin el bloque `ids-inexistentes`.
  La columna del revisor, con lo que encuentre (§k).
- **El tamaño final de PROJECT_STATE**: 22.977 bytes con las líneas del cierre (simulado); en la
  rama, al cerrar este informe, 22.608 bytes.

## j. CI de Linux

- `git push origin trabajo/activar-sesion-06-motor:refs/heads/fix/activar-sesion-06-motor` (la rama
  local no se toca).
- **Run 42177503487** sobre b03cbbe (`headSha b03cbbed43d88bfe8e1e999b66402672a773312a`):
  `completed`, `failure`, con el único fallo aceptado (`gh run view 42177503487 --log-failed`):
  ```
  ERROR: PROJECT_STATE declara la rama 'trabajo/activar-sesion-06-motor'; la rama actual es 'fix/activar-sesion-06-motor'
  FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo - AssertionError: assert 1 == 0
  1 failed, 3183 passed, 47 skipped in 362.15s (0:06:02)
  ```
- La respuesta al revisor añade un commit; su run, en «Estado» (el que cuenta es el del último
  commit: revisor, b2).

## k. Informe del revisor

Subagente `revisor` (opus), lanzado con la CI de b03cbbe ya terminada y con los cinco alcances del
encargo y su regla de holdout. Pegado tal cual; no cita ningún tramo no citable (0 retiradas). Solo
sus títulos bajan un nivel, para caber en esta sección. Sus números de línea del informe
(«informe:NNN») son los de b03cbbe.

### Informe del revisor · trabajo/activar-sesion-06-motor · 2026-11-06

Rama en b03cbbe, base `main` 04ec025, 7 commits. El árbol de trabajo está limpio. El sello de `make-check.log` es el árbol de HEAD: `SELLO: … da7e8266182bc8af229bc0a20bb32c485a6a292d` = `git rev-parse "HEAD^{tree}"`, `3231 passed`, `PICO DE MEMORIA … 307 MiB`.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 5 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El inventario de la fase 0 nombra mal a quién llama a `tope_del_registro`.** El informe dice «`tope_del_registro` en `cableado` y en `scripts/embudo_77.py:439`». `cableado.py` no lo llama. Lo llaman `cli.py` y siete guiones más, y todos reciben ahora el modo nuevo. La «deuda de guiones» (§e.3, §f) solo nombra tres. El criterio de la fase 1 (que `SeguidorTope` solo lo construye `cableado` y que nadie más lee `perdida_trader_reinicio_huso`) sí se cumple. | `ACTIVAR-SESION-06-MOTOR.md:66`. Grep de `tope_del_registro` en `src` y `scripts`: `src/botsito/cli.py:2398`, `:2521`; `scripts/bloque_de_la_caja.py:267`, `caja_77_exploratoria.py:137`, `embudo_77.py:439`, `orden_stop_o_limite.py:427` y `:508`, `verificacion_a21.py:75`, `verificacion_a21_entradas.py:174`, `verificacion_a35_a44.py:205`. En `cableado.py`, ninguna llamada. |
| a2 | importa | **Un test no prueba lo que dice su docstring.** `test_por_el_cableado_el_corte_cae_en_la_apertura_de_la_primera_sesion` dice que corta «con el saldo arrastrado». Pero el mercado de los dos días es plano: `tc._mercado({})`, sin ruta. El BID se queda en BASE = 110.000 y la límite de compra está en ENTRADA = BASE-5, así que nunca se llena (lo saco de leer el código, no lo ejecuté). El saldo no cambia, y `saldo_corte_dia == motor.cuenta.saldo` (el saldo al FINAL del día 2) se cumpliría también con el capital inicial. Lo que sí prueba es el instante del corte (la apertura y no la medianoche). Lo de «arrastrado» solo lo prueban los sintéticos de `SeguidorTope`. | `tests/unit/test_reinicio_tope_trader.py:172`, `:196`; `tests/unit/test_cableado.py:61-62` (BASE, ENTRADA), `:94-114` (`ruta_bid.get(m, bid)`: plano sin ruta) |
| a3 | menor | El `cuando` de RN-020 lleva historia: «antes de la sesion seis, la medianoche que marca reloj_dia_riesgo». La fecha y el id del ADR los rechazó la guardia de literales (lo dice el informe), y la referencia quedó escrita con letras. La historia ya está en `notas`. | `knowledge/spec/strategy_spec.yaml:2037-2039`; `ACTIVAR-SESION-06-MOTOR.md:373-374` |
| a4 | menor | Los recuadros dicen «2026-11-05», pero se commitearon el 2026-11-06, y HOLDOUT-EXPOSICIONES fecha ese trabajo el 2026-11-06. | `git log --format='%h %ci'`: ed09769 2026-11-06 00:34, 2a3cf76 01:03, e3adb44 01:32 (-0500); `spec_manifest.yaml` `generado_el: "2026-11-06T05:38:33Z"`; recuadros en ADR-0053 (+141), ADR-0085 (+70), `SESION-06-EXTRACCION.md:795` |
| a5 | menor | Una cita apunta una línea antes: la fila S-2 de la tabla final de la extracción está en `:768`, no en `:767` (la 767 es S-1). | `ACTIVAR-SESION-06-MOTOR.md:53`; `SESION-06-EXTRACCION.md:767-768` |
| a6 | menor | `fb-…-c56ec7cf` es de procedencia `trader_grabado`, pero su `valor_resultante` lleva una conclusión de la sesión sobre otras partes: «con S-1 y la sesion 5, ninguna parte de A-44 queda sin regla general». Las `notas` están limpias. | `knowledge/feedback/2026-11-04-sesion-06/fb-2026-11-04-sesion-06-c56ec7cf.yaml:15-16` |
| a7 | menor | El clon de `main` sigue vivo, aunque el informe dice que se quita al final y la skill `comparar-con-main` lo pide al terminar. | `git worktree list` → `C:/cm/m7  04ec025 (detached HEAD)`; `ACTIVAR-SESION-06-MOTOR.md:179` |

**Comprobado sin hallazgos:**
- **Contrato:** `contrato_rama.py` da «CONTRATO: 34 ficheros dentro del contrato … exit=0».
- **Comprobaciones del contrato:**
  - `feedback apply --sesion 2026-11-04-sesion-06 --check`: «4 parametros; 0 cambian, 4 ya estaban», exit 0.
  - `knowledge validate`, sin redirigir: todo OK, «199 registros de feedback, historial intacto, commits con Fuente», exit 0.
  - `spec docs`, sin `--escribir`: «OK: docs/spec coincide con knowledge/spec/».
  - `make check`: lo sustituye `make-check.log` (sello = árbol de HEAD).
  - pytest de los 9 ficheros cambiados o nuevos, más `test_kit` y `test_adr`: exit 0.
- **Trailers `Fuente:`** en el cuerpo de ed09769, 2a3cf76 y e3adb44, con ids que existen (fb-6886938e, fb-c56ec7cf, ADR-0089, ADR-0085 y los tres ev-v17 de S-4).
- **Holdout:** nada bajo `knowledge/cases/`. Las exposiciones tienen fila el 2026-11-05 (fase 0) y el 2026-11-06 (tras la PARADA). El informe solo da recuentos por mes.
- **Régimen de cambios:**
  - `feedback/`: solo `A`.
  - `evidence/`, `manifests`, `corpus`: sin cambios.
  - HISTORIA, el encargo y los dos ADR enmendados: solo líneas añadidas.
  - `SESION-06-EXTRACCION.md` (informe cerrado): solo un recuadro `>` fechado tras la tabla final.
- **A-44:** `ambiguedades.yaml`, `docs/spec/ambiguedades.md`, la tabla de PROJECT_STATE, RN-020, el registro de parámetros y la hoja con su test van en el MISMO commit (2a3cf76). Las `evidencia` añadidas (000250, 000351) hablan del reinicio, no son de relleno.
- **ADR-0089:** `## Estado` ACTIVE.
- **Ningún sitio nuevo con `cita`**, así que las tres guardias de `modelo.py` no aplican.
- **Ninguna cifra en el código nuevo.**
- **Citas comprobadas contra su fuente:**
  - `ERRORES-RECURRENTES.md:108` (el «no corta la racha» atribuido).
  - `strategy_spec.yaml:2085-2087` en main.
  - `zonas.py:494-499`.
  - `primitivas_broker.py:654-659`.
  - `estructura_m1.py:204-206`.
  - `test_project_state.py:21`.
  - `test_agregacion.py:305`.
  - `HOJA-DE-RUTA.md:653-654`.
  - `ACTIVAR-A35-A44.md:71` y `:126-127`.
  - Los tres ítems de S-4 frente al recuadro de ADR-0085.
- **Ningún ítem de evidencia nuevo** (el punto 10 no aplica).

#### Eje (b) · Encargo
Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 28 hechos, 2 parciales, 4 no hechos (dos en la PARADA y dos pendientes por diseño: el revisor y la línea final).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con abrir-rama: contrato R4, riesgo alto, artefacto | Hecho | `contrato.yaml:2-4`; b2f3562 |
| 2 | Fase 0 a: la tabla de las cuatro fases | Hecho | informe:62-69 |
| 3 | b.1: los llamadores pedidos | Hecho (ver a1) | informe:73-92 |
| 4 | b.2: A-44 parte por parte | Hecho | informe:94-110 |
| 5 | b.3: los recuentos de las fases 2 y 3, solo recuentos | Hecho; las sumas cuadran (85.985, 1.164, 718, 13; 5.701, 2.950, 3.912) | informe:132-157 |
| 6 | b.4: qué tests cambian, con la salida de main | Parcial: nombres y recuentos, sin la salida pegada | informe:159-179 |
| 7 | b.5: flaky, `deadline=None` en commit propio | Hecho | 3f2bef2; `test_valores.py:50-54` |
| 8 | b.6: PROJECT_STATE < 23.000 | Hecho: 22.608 hoy (`wc -c`) y 22.977 en la simulación del cierre | informe:194-197, :477 |
| 9 | c: plan de commits | Hecho | informe:199-213 |
| 10 | d: PARADA commiteada | Hecho | d091c6c; informe:238-306 |
| 11 | 1.1: `perdida_trader_reinicio`, enum, UNKNOWN → CONFIRMED por RESOLVE_UNKNOWN, notas solo con su ítem | Hecho | `parametros.yaml` (+1573-1595); `fb-…-6886938e.yaml:6-16` |
| 12 | 1.1: `reinicio_huso` UNKNOWN, «SIN EFECTO con…» | Hecho | `parametros.yaml` (+1605-1607) |
| 13 | 1.2: corte en la apertura; semana ISO; medianoche igual que antes | Hecho | `tope_trader.py:262-297`; `cableado.py:270-274` |
| 14 | 1.2: la traza dice el modo, sin SUPUESTO | Hecho | `tope_trader.py:138-143` |
| 15 | 1.3: ADR-0089, recuadros en ADR-0053 §3.3 y §9, fila del índice | Hecho | `docs/adr/README.md` (filas 0053 y 0089) |
| 16 | 1.4: test que rompe en main, sintéticos con saldo distinto o igual, viernes → lunes, `test_preparar_a44` cambia de sentido | Hecho (ver a2) | `test_reinicio_tope_trader.py`; `test_preparar_a44.py:148-163` |
| 17 | 1.5: A-44 RESUELTA (registro, cinco sitios, `test_kit`, hoja, test de control con su motivo, recuadro en la extracción) | Hecho | 2a3cf76; `test_en_parte_no_se_cierra.py:93-110`, `:134-152`; `test_kit.py` |
| 18 | 2.1: `no_corta_y_cuenta`, las de por delante no entran, docstring «lectura del consultor» | Hecho | `pivotes_m15.py:75-78`, `:108-131` |
| 19 | 2.2: `motor.py` la pide; los dos guiones como deuda | Hecho | `motor.py:157-168`; informe:402-405 |
| 20 | 2.3: recuadro en ADR-0085 §2 y su fila | Hecho | ADR-0085 (+70-84); README |
| 21 | 2.4: tests (:149 cambia de sentido; dos y tres velas sin cuerpo; por delante; por marco; camino real que rompe en main) | Hecho | `test_pivotes_m15.py:150-164`; `test_vela_sin_cuerpo_m15.py` |
| 22 | 2.5: medida por mes | Hecho | informe:134-140 |
| 23 | Fase 3 (S-22) | No hecho: en la PARADA, declarado y sin tocar código | informe:243-260 |
| 24 | Fase 4 (S-19) | No hecho: en la PARADA, declarado y sin tocar código | informe:261-274 |
| 25 | Sin corrida que cuente; solo `--diagnostico-cuenta-diaria` sobre construcción | Hecho | informe:118-130; `RESPALDO-M1/README.md:5-6` |
| 26 | Citas solo de los ítems de «Para la rama de motor»; notas de cada registro solo con su ítem | Hecho: solo aparecen 000250, 000351, 002155, 002250 y 002217, todos en `ACTIVAR-SESION-06.md:510-525` | grep de ids añadidos en el diff |
| 27 | Next Action y hoja de ruta sin tocar; sus líneas, preparadas | Hecho | diff de PS sin Next Action; `docs/plan` fuera del diff; informe §i |
| 28 | Makefile, `.claude/` y la guardia sin tocar | Hecho | `git diff --name-status` |
| 29 | Exposiciones el mismo día | Hecho | `HOLDOUT-EXPOSICIONES.md` (+95-96) |
| 30 | CI de Linux por `fix/`, con el número de run en el informe | Parcial: el run 42177503487 existe sobre b03cbbe (completed; único fallo `test_state_check_ok_on_real_repo`: «la rama actual es 'fix/activar-sesion-06-motor'»), pero el informe no lo trae | informe:471, :510 («Faltan la CI de Linux (§j)») |
| 31 | El informe del revisor, pegado | No hecho (es este) | — |
| 32 | Líneas del cierre (F, R4.2, R4.3, Fechas fijas, ERRORES, tamaño) | Hecho. La F no va «una línea por fase»: se acortó por bytes, y está declarado | informe:473-506, :480 |
| 33 | «Rama lista para revisión, NO cerrada» | No hecho todavía | informe:508-510 |
| 34 | «El encargo, punto por punto» | Hecho | informe §h |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **No está pegado «el diff de sentido de cada test con la salida de main y la de la rama» que pide el encargo.** De main solo se pega el ImportError de la recolección, que no enseña ninguna aserción. De la rama no se pega nada: dice «en verde». En la fase 2 el comportamiento se enseñó aparte (`camino_real_f2.py`: None frente a 140). En la fase 1 no hay nada igual: el sentido en main se razona («lo que asertaba el test viejo, que en main pasa»), no se pega. En b.4 la fase 3 da nombres y recuentos sin la salida. | encargo:83, :76; informe:355-363, :417-426, :165-174 |
| b2 | importa | **El informe no trae la CI, aunque el revisor se lanzó con la CI ya terminada.** La skill pide el revisor «con el informe ya terminado» y dice que «el run que cuenta es el del ÚLTIMO commit». Al añadir §j y §k habrá otro commit y hará falta otro run. | `.claude/skills/entregar-rama/SKILL.md:75-76`; `gh run view 42177503487` → completed / failure, headSha b03cbbe; informe:471, :510 |
| b3 | menor | **Las fases 3 y 4 se marcan «NO CUADRA», pero el propio informe dice que el criterio escrito de cada una se cumple.** El encargo solo deja fuera las fases «cuya medida NO cuadre». La parada está declarada y argumentada en §d, pero la etiqueta no es exacta. Diría: «cuadra el criterio; se para por …». | encargo:16, :61, :68; informe:68-69, :243-244, :261-262 |

**Lo que el encargo no pedía y la rama hace (todo declarado):**
- el test de control de la sesión 5 (H2);
- `perdida_trader_reinicio` en los `parametros` de RN-020 y de A-44;
- el ítem del viernes en la `evidencia` de A-44;
- la vuelta a `medianoche_huso` si falta el parámetro (ADR-0089 §2);
- el texto de A-35 (H4).

**Lo que no se toca** (RN-004, RN-009, break even, caja, cartuchos; A-35, A-48 y A-53 DEFAULT_AMBIGUOUS): el diff de `src/` solo cambia `pivotes_m15.py`, `motor.py` (una llamada), `cableado.py` (`abrir_dia`) y `tope_trader.py`. El diff de `parametros.yaml` solo toca `perdida_trader_*`.

**¿Está justificada la PARADA de las fases 3 y 4?**
- **Fase 4: sí.** La premisa choca con el código. `marcar_usada` va en `primitivas_broker.py:654`, antes del `isinstance(r, Rechazo)` de `:655`, y `toca_colocar_orden_limite` descarta la zona usada (`zonas.py:494-499`). Sin marcar el rechazo, la misma caja no vuelve. Esperar a «que el 0 quede del lado bueno» es un mecanismo que no existe: hay que decidir no enviar.
- **Fase 3: defendible.**
  - La identidad que la frena es real: `ultimo_punto_de_ruptura` con `hasta` en la toma es el pivote de `referencia_del_breaker` (`estructura_m1.py:204-206`, `zonas.py:381`).
  - Pero hoy no muerde: `orden_stop_punto` está en `ultimo_pivote_m1` (`parametros.yaml:682-696`).
  - Lo que más pesa es lo medido: el 52 % de los puntos cambia y 20 tests caen, entre ellos la comparación con `scripts/bloque_de_la_caja.py`, que es ruta protegida (`contrato.yaml:36`). Además, el encargo preveía que cambiarían `test_estructura_m1.py:65` y `:219`, y esos no prueban `ultimo_punto_de_ruptura`. Lo comprobé: `:116-127` es `referencia_del_breaker`.
  - La lectura (a) que recomienda la decisión 0 es la misma que se prototipó. Se podía haber hecho declarándola; parar es la opción prudente en una rama nocturna de motor.

#### Lo que no pude comprobar
- **Los recuentos de b.3**: salen de guiones y salidas de la carpeta de trabajo, y volver a correr el arnés escribe.
- **Los 20 tests que caen con el prototipo de la fase 3 y los «0 rotos» de la fase 2**: se midieron con prototipos en un clon.
- **El `None` frente a `140` de `camino_real_f2.py` en main.**
- **Los sellos de los commits anteriores a HEAD**: solo está el `make-check.log` actual.
- **No ejecuté** `make check`, `spec docs --escribir` ni `knowledge validate > log` (escriben). En su lugar: el log existente, `spec docs` sin flag y `validate` sin redirigir.
- **Que el «Flaky por DeadlineExceeded» del cierre de F38n fuera solo el plazo**: la traza no está en el repo (el propio informe lo dice, :189-190).
- **Mi propia exposición, para que la sesión la declare** en HOLDOUT-EXPOSICIONES el 2026-11-06:
  - leí con Read cinco ítems de v17 (000250, 000351, 002155, 002250, 002217);
  - leí `knowledge/cases/kit/mapa_parametros.yaml` (Grep);
  - ejecuté pytest de `test_reinicio_tope_trader`, `test_vela_sin_cuerpo_m15`, `test_pivotes_m15`, `test_preparar_a44`, `test_en_parte_no_se_cierra`, `test_hoja_preguntas`, `test_valores`, `test_kit` y `test_adr`;
  - consulté el log de la CI.

  Ningún caso, libro, imagen, filtrada ni cruda; ninguna fecha de día reservado.

#### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `git log --format='=== %h%n%B' main..HEAD`
4. `git log --format='%h %s' main..HEAD -- knowledge/spec knowledge/cases`; `git log --format='%h' main..HEAD -- docs/encargos`; `git diff --name-status main...HEAD`
5. `git diff main...HEAD -- knowledge/spec/ambiguedades.yaml knowledge/spec/strategy_spec.yaml knowledge/spec/spec_manifest.yaml`
6. `git log -L '/^spec_version/,+1:knowledge/spec/spec_manifest.yaml' main` (filtrado)
7. `git diff main...HEAD -- src/`
8. `git diff main...HEAD -- docs/adr/ docs/validation/SESION-06-EXTRACCION.md docs/validation/HOLDOUT-EXPOSICIONES.md`
9. `git diff main...HEAD -- knowledge/spec/parametros.yaml scripts/hoja_preguntas.py`
10. `git diff main...HEAD -- PROJECT_STATE.md tests/unit/test_kit.py tests/unit/test_en_parte_no_se_cierra.py tests/unit/test_hoja_preguntas.py tests/unit/test_valores.py tests/unit/test_preparar_a44.py tests/unit/test_pivotes_m15.py`
11. pytest con `PYTHONDONTWRITEBYTECODE`: lo negó la guardia; no lo rodeé.
12. `uv run pytest -q -p no:cacheprovider` sobre los 7 ficheros, y después los 9 → exit 0
13. `uv run botsito feedback apply --sesion 2026-11-04-sesion-06 --check`
14. `uv run botsito knowledge validate`
15. `uv run botsito spec docs --help`; `uv run botsito spec docs`
16. `ls -la make-check.log && grep … make-check.log`. Un primer intento llevaba `git write-tree` encadenado por error mío: la guardia lo negó y no se ejecutó.
17. `git rev-parse "HEAD^{tree}"`; `git log -1 --format='%h %ci' HEAD`
18. `gh run view 42177503487 --json …`; `gh run view 42177503487 --log-failed | grep …` (dos veces)
19. `git diff --numstat main...HEAD -- …`; `wc -c PROJECT_STATE.md`
20. `git diff b2f3562 ed09769 -- docs/encargos/trabajo-activar-sesion-06-motor.md`
21. `git show --stat` de 2a3cf76, e3adb44 y ed09769
22. `git log --format='%h %ci' main..HEAD`
23. `sed`/`grep` de citas (ERRORES-RECURRENTES:108 y :37, ACTIVAR-A35-A44:71 y :125-128, HOJA-DE-RUTA:650-656, test_project_state:21, test_agregacion:303-306); un `for` sobre tres ítems lo negó la guardia y los leí con Read
24. `grep` de la skill `entregar-rama` y de `comparar-con-main`; `ls .claude/skills/`
25. `grep -n 0087 PROJECT_STATE.md`
26. `git worktree list && git branch --list`
27. Read/Grep: el encargo, `contrato.yaml`, el informe, los dos registros fb nuevos, fb-a1f5784d, fb-146c4789, siete ítems ev-v17, ADR-0089, `tope_trader.py`, `cableado.py`, `motor.py`, `pivotes_m15.py`, `estructura_m1.py`, `zonas.py`, `primitivas_broker.py`, `test_reinicio_tope_trader.py`, `test_vela_sin_cuerpo_m15.py`, `test_cableado.py`, `SESION-06-EXTRACCION.md:760-807`, `ACTIVAR-SESION-06.md:505-550`, `AMBIGUEDADES.md:1-60`, `parametros.yaml` (freno_bucle, orden_stop_punto), `RESPALDO-M1/README.md`, `mapa_parametros.yaml`

## l. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Corregido en la tabla de §a (fase 1, «Llamadores»): `tope_del_registro` lo llaman `cli.py:2398` y `:2521` y siete guiones (`bloque_de_la_caja.py:267`, `caja_77_exploratoria.py:137`, `embudo_77.py:439`, `orden_stop_o_limite.py:427` y `:508`, `verificacion_a21.py:75`, `verificacion_a21_entradas.py:174`, `verificacion_a35_a44.py:205`), no `cableado`. Todos reciben ahora `reinicio`; ninguno construye `SeguidorTope` (el criterio de la fase 1 sigue cumpliéndose: `SeguidorTope(` solo en `cableado.py`). Los siete guiones, a la deuda de guiones de §f, sin tocarlos. |
| a2 | importa | Arreglado: `test_por_el_cableado_el_corte_cae_en_la_apertura_de_la_primera_sesion` corre ahora el día 1 con `RUTA_STOP` (la orden se llena y salta el stop: el saldo baja) y aserta que el saldo de fin del día 1 es menor que el del corte inicial y que el corte del día 2 lleva ese saldo; el día 2 no tiene orden (la zona sintética solo se liga en el minuto del día 1). El docstring lo dice. En la rama: verde. |
| a3 | menor | Se queda: el `cuando` de RN-020 dice «antes de la sesion seis» en letras porque la guardia de literales no admite la fecha ni el id del ADR, y la historia completa está en `notas`. Si el consultor prefiere el `cuando` sin historia, es una línea. |
| a4 | menor | Declarado: los recuadros y los registros llevan la fecha de la decisión del consultor y del encargo (2026-11-05); los commits son del 2026-11-06 de madrugada (hora local, −0500), y HOLDOUT-EXPOSICIONES fecha el trabajo el día que se hizo. No se cambian. |
| a5 | menor | Corregido: `SESION-06-EXTRACCION.md:768` (la fila de S-2), en §0. |
| a6 | menor | Se queda, declarado: `knowledge/feedback/` es SOLO AÑADIR y el registro no se edita. Su `valor_resultante` resume el estado de A-44 tras el registro (lo que el cierre necesita decir), no una frase del trader; la `respuesta_literal` y las `notas` son solo de `ev-v17-000250-a468bcec`. |
| a7 | menor | Hecho: `git worktree remove --force C:/cm/m7` y `git worktree prune`; `git worktree list` solo da el repo, y `git branch --list`, `main` y la rama. |
| b1 | importa | Pegadas abajo, en «Las salidas de los tests contra `main` y en la rama». |
| b2 | importa | §j trae ahora el run de b03cbbe; el commit de esta respuesta lleva su propio run, en «Estado». |
| b3 | menor | De acuerdo con la etiqueta: en las fases 3 y 4 el criterio escrito CUADRA, y la PARADA es por lo medido que la decisión no zanja (§d lo dice en cada fase). Léase «cuadra el criterio; se para por …». La PARADA commiteada no se reescribe. |

Y la exposición del revisor (lo que él declara: Read de cinco ítems de v17, Grep de
`knowledge/cases/kit/mapa_parametros.yaml`, pytest de nueve ficheros de test y el log de la CI),
en la fila del 2026-11-06 de HOLDOUT-EXPOSICIONES.

### Las salidas de los tests contra `main` y en la rama (b1)

Clon `C:/cm/m7` (`git worktree add --detach` de `main`, con `config/settings.local.toml` hacia el
`data/` real), ya quitado.

**Fase 1.** El test que cambia de sentido, con su versión de `main` en el clon (`git checkout --
tests/unit/test_preparar_a44.py` dentro del clon), `uv run pytest -q -p no:cacheprovider
tests/unit/test_preparar_a44.py -k test_con_el_registro_real_el_tope_es_el_del_dia`:
```
.                                                                        [100%]
```
(pasa en `main`: allí el reinicio es el corte del perfil marcado SUPUESTO). Los ficheros de la rama
en el clon, la salida de §e.1 (`ImportError` de `MEDIANOCHE_HUSO` y `PRIMERA_SESION_DIA_SIGUIENTE`).
El comportamiento, con el guion `camino_real_f1.py` de la carpeta de trabajo (el seguidor con el
registro real del directorio en que corre, lunes y martes sintéticos con la medianoche de Praga en
medio; la raíz por argumento). En el clon de `main`:
```
descripcion: tope del trader: dia, sobre saldo, en porcentaje; dia 4.5 sobre saldo_inicial_dia; reinicio en Europe/Prague; SUPUESTO: reinicio con el huso de corte del perfil (el trader no dijo otro)
cortes: [('2030-01-14T23:00:00+00:00', 'dia')]
saldo al corte del dia: 99000
```
En la rama:
```
descripcion: tope del trader: dia, sobre saldo, en porcentaje; dia 4.5 sobre saldo_inicial_dia; reinicio al abrir la primera sesion del dia siguiente (de sesion en sesion)
cortes: [('2030-01-15T06:00:00+00:00', 'dia')]
saldo al corte del dia: 98000
```

**Fase 2.** En el clon de `main`, la salida de §e.3 (`ImportError` de
`SIN_CUERPO_NO_CORTA_Y_CUENTA`) y `camino_real_f2.py`: `liquidez_m15(ALTO): None`; en la rama,
`liquidez_m15(ALTO): 140`.

**En la rama**, los cuatro ficheros (`test_preparar_a44.py`, `test_reinicio_tope_trader.py`,
`test_vela_sin_cuerpo_m15.py`, `test_pivotes_m15.py`), con el arreglo de a2:
```
51 passed in 6.08s
```

**Fase 3 (b.4, el prototipo que no se commitea).** Los 20 que fallaron en el clon con la lectura (a)
en `ultimo_punto_de_ruptura` (log de la carpeta de trabajo, `f3_tests.log`):
```
FAILED tests/unit/test_caja_hasta_el_llenado.py::test_cada_maximo_nuevo_es_otra_zona_del_mismo_punto_y_el_0_no_se_mueve
FAILED tests/unit/test_caja_hasta_el_llenado.py::test_la_cota_de_peticiones_con_el_1_expandiendose_no_dispara_el_freno
FAILED tests/unit/test_caja_lado_de_ruido.py::test_la_caja_entera_del_lado_de_ruido_no_se_opera_con_ninguno[alcista]
FAILED tests/unit/test_caja_lado_de_ruido.py::test_la_caja_entera_del_lado_de_ruido_no_se_opera_con_ninguno[bajista]
FAILED tests/unit/test_escenarios_por_sesion.py::test_un_escenario_terminado_no_coloca_mas
FAILED tests/unit/test_orden_en_el_0_con_mecha.py::test_el_0_es_el_extremo_con_mecha_del_pivote_de_m1
FAILED tests/unit/test_orden_stop_pivote.py::test_el_punto_es_el_ultimo_bajo_en_una_venta_y_se_actualiza
FAILED tests/unit/test_orden_stop_pivote.py::test_la_caja_de_r6_r4_y_r1 - ass...
FAILED tests/unit/test_orden_stop_pivote.py::test_en_las_series_con_velas_sin_cuerpo_la_unica_diferencia_es_el_punto_de_adr_0085[venta]
FAILED tests/unit/test_orden_stop_pivote.py::test_en_las_series_con_velas_sin_cuerpo_la_unica_diferencia_es_el_punto_de_adr_0085[compra]
FAILED tests/unit/test_orden_stop_pivote.py::test_son_las_funciones_de_r5_y_r6_de_caja_77[venta]
FAILED tests/unit/test_orden_stop_pivote.py::test_son_las_funciones_de_r5_y_r6_de_caja_77[compra]
FAILED tests/unit/test_orden_stop_pivote.py::test_el_productor_liga_una_zona_por_punto_y_no_repite_un_punto_usado
FAILED tests/unit/test_orden_stop_pivote.py::test_con_la_referencia_de_la_toma_el_punto_no_se_mueve
FAILED tests/unit/test_orden_stop_pivote.py::test_con_la_caja_recalculada_un_1_nuevo_liga_otra_zona_del_mismo_punto
FAILED tests/unit/test_velas_sin_cuerpo_m1.py::test_verde_sin_cuerpo_roja_da_el_punto_en_el_maximo_de_la_verde[compra-1]
FAILED tests/unit/test_velas_sin_cuerpo_m1.py::test_verde_sin_cuerpo_roja_da_el_punto_en_el_maximo_de_la_verde[compra-3]
FAILED tests/unit/test_velas_sin_cuerpo_m1.py::test_verde_sin_cuerpo_roja_da_el_punto_en_el_maximo_de_la_verde[venta-1]
FAILED tests/unit/test_velas_sin_cuerpo_m1.py::test_verde_sin_cuerpo_roja_da_el_punto_en_el_maximo_de_la_verde[venta-3]
FAILED tests/unit/test_velas_sin_cuerpo_m1.py::test_por_el_camino_real_el_productor_liga_la_zona_del_punto
```
Con el prototipo de la fase 2 en el mismo clon, los 31 ficheros: `exit=0`, ninguno falla (log
`f2_tests.log`).

## Estado

Hecho lo que cuadró: fases 1 y 2, el cierre de A-44 y el flaky. Las fases 3 y 4 quedan en la PARADA (§d), con seis decisiones para el consultor. El revisor: 0 bloquea, 4 importa (arreglados), 6 menores (2 arreglados, 4 declarados; §l). CI de Linux: run 42177503487 sobre b03cbbe con el único fallo aceptado; el run del commit de esta respuesta al revisor, que es el último, se da en el mensaje final a Aleks (un informe no puede llevar el run de su propio commit). Rama lista para revisión, NO cerrada.

## Orden de cierre y respuesta a la PARADA (2026-11-06)

**RECUADRO (2026-11-06, orden de cierre).** Dada por Aleks (consultor) el 2026-11-06, tras revisar
la rama en `fix/activar-sesion-06-motor` (3e8cf85); llegó pegada, y después Aleks lanzó
`/cerrar-rama trabajo/activar-sesion-06-motor`. La sesión sigue `docs/runbooks/RITUAL.md`. Su
«Respuesta a la PARADA (§d)» contesta a las decisiones 0 a 5 de §«Lo que necesito que decidas»;
se aplica en el commit `chore(cierre)`, y lo que se apartó de la orden, en el registro del cierre
al final de `docs/state/HISTORIA.md`. Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/activar-sesion-06-motor (consultor, 2026-11-06). Revisada contra el diff de fix/activar-sesion-06-motor (3e8cf85) y el informe con el revisor pegado: se cierra con las fases 1 y 2, el cierre de A-44 y el flaky. Sigue RITUAL.md con la skill cerrar-rama; esta orden solo añade lo de abajo. El informe está cerrado: lo que entre va en recuadro.
>
> Tag: stable/F38o-activar-sesion-06-motor.
>
> Respuesta a la PARADA (§d), para copiar tal cual en un recuadro fechado al final del informe y del encargo:
> 0. (a) como lectura del consultor para la rama futura; se pregunta al trader en la sesión 7.
> 1. (b).
> 2. NINGUNA de las dos: la fase 3 NO se hace antes de la re-corrida. Motivo: quita el 52 % de los puntos de breaker y deja dos lecturas sin regla del trader (0 y la verde frente a la racha), más el «m15» dudoso de la frase de la mecha; una regla de ese tamaño se confirma en la sesión 7 con esquemas y se hace después en rama propia (los 20 tests y CAJA-77 al estilo de ADR-0085, entonces). Me aparto de la recomendación del informe y lo digo.
> 3. (c) hasta la sesión 7, con mi lectura apuntada: si el trader dice «espero», 3.a y 4.a. Motivo: «se pone igual, ya me habilita» (ev-v17-014103-8cf3e7fb) suena a entrar, no a esperar: son dos motores distintos y lo decide él. ADR-0083 D1 sigue como está.
> 4. (a), condicionado a 3.
> 5. (a): entrada en el carril de guardias de la hoja de ruta (cmp y diff de dos ficheros que no son guiones no se leen como ejecutar).
>
> Hallazgos del consultor que el revisor no vio (ninguno bloquea):
> - Menor: la F preparada lleva «diagH\» y la frase de alternativas de §d; va con el texto de abajo.
> - Menor: docs/runbooks/ACTIVAR-A35-A44.md:71 y :126-127 siguen diciendo que el reinicio es perdida_trader_reinicio_huso (§f): no se toca en el cierre; lo recojo para la rama de preparación de la sesión 7. Lección para el revisor: cuando una rama cambia el nombre del mecanismo, buscar el nombre viejo en los runbooks, no solo en src/.
> - Para mi columna de ERRORES-RECURRENTES, además de las cuatro que prepara §i: el informe de F38n (§«Para la rama de motor», punto 4) sitúa el rechazo al colocar en cableado.py:151-165 y es primitivas_broker.py:655-659; recuadro de corrección en ACTIVAR-SESION-06.md junto a ese punto, en este cierre.
>
> En el commit del contrato (chore(cierre)), todo lo de §i con esto encima:
> - Next Action F, sustituida entera por: «F. Sesión 6 ACTIVADA en spec (F38n) y motor (este tag): S-2, el tope del trader se reinicia al abrir la primera sesión del día siguiente (ADR-0089); S-4, en M15 la vela sin cuerpo no corta la racha y su mecha cuenta (ADR-0085 §2); A-44 RESUELTA. S-22 y S-19 NO se activan hasta la sesión 7 (decisión del consultor, 2026-11-06, ACTIVAR-SESION-06-MOTOR.md §d): S-22 quita el 52 % de los puntos de breaker y deja dos lecturas sin regla (qué punto vale si el último pivote no cumple; la última verde o la racha); S-19 depende de si la orden entra igual o espera a que el 0 quede del lado bueno. Siguiente: la rama corta de la demo (A), H (fase 0: el diagnóstico de H del scratchpad de Claude Code, fuera del repo), R y la re-corrida que cuenta (ADR-0070 §3); después, la preparación de la sesión 7 (hoja + gráficos 2 a 6 con contexto; lista en ACTIVAR-SESION-06.md §«Para la sesión 7», más S-22 y S-19 con sus esquemas y el 52 %). El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo. R6a en los huecos.» Si con esto PROJECT_STATE pasa de 23.000 bytes, recorta la frase de S-22 y S-19 a «S-22 y S-19 a la sesión 7 (§d del informe)» y dime el tamaño.
> - Hoja de ruta: R4.2 Estado como en §i, pero terminando en «S-22 y S-19 van a la sesión 7 (R4.3)»; R4.3 gana en su lista S-22 (con el 52 % y las dos lecturas) y S-19 (entra, espera o descarta), y «Depende de» como dice §i; «Fechas fijas» como dice §i; en el carril de guardias, entrada nueva: «cmp y diff de dos ficheros que no son guiones se leen como ejecutar (ACTIVAR-SESION-06-MOTOR.md §b.3): corregir en la próxima rama de guardia».
> - ERRORES-RECURRENTES: la fila de la rama con lo de §i y §k, y en mi columna las cuatro de §i más la de arriba.
> - Las entradas que salen de la Next Action van a HISTORIA bajo «# Next Action HECHA» con su texto literal.
>
> Después: merge a main, tag, commit de estado (solo Current Branch, Current Feature, Stable Main State y Last Stable Commit), make check sellado, push atómico de main y el tag (yo confirmo «1. Yes»), CI de main en verde antes de borrar, borrar trabajo/activar-sesion-06-motor en local y fix/activar-sesion-06-motor en origin.
>
> Informe final: sha de main, sha del merge, tag y su objeto, run de la CI de main, ramas que quedan, tamaño de PROJECT_STATE.md y lo que se apartó de esta orden.
