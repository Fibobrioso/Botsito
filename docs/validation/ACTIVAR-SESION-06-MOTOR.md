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
  S-2 fue por falta de opción en el enum, no por la respuesta (`SESION-06-EXTRACCION.md:767`, regla
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
| 1 · S-2 | `SeguidorTope.avanzar` corta en la medianoche de `huso_reinicio` (`engine/tope_trader.py:230-240`); sin huso, el del perfil marcado SUPUESTO (`:191-194`) | `SeguidorTope(` solo en `engine/cableado.py:267`; `tope_del_registro` en `cableado` y en `scripts/embudo_77.py:439` (que construye el motor por `cableado`) | `tests/unit/test_preparar_a44.py:145-162` (asierta `huso_supuesto`) y `:254-302` (los cortes) | el seguidor solo lo construye `cableado.py`; `primero` es la apertura en UTC; nadie más lee `perdida_trader_reinicio_huso` | **SÍ** (b.1) |
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

## Estado

Terminada en lo que cuadró (fases 1 y 2, el cierre de A-44 y el flaky); las fases 3 y 4, en la PARADA (§d) a la espera del consultor. Faltan la CI de Linux (§j) y el revisor (§k), que se añaden abajo.
