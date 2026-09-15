# Auditoría ultracode — 2026-09-13

## 0. Veredicto de rumbo

### Veredicto: ROJO

**inferencia** (de [d1-interprete-06] y [d8-camino-motor-01]): escribir hoy F18-F24 garantiza rehacerlo, porque la spec que ese motor tendría que ejecutar, leída al pie de la letra, no coloca ni una orden, y la decisión que da forma al bucle (cierre de M1, tick o evento de orden) no está tomada en ningún ADR.

- **hecho** (§1.1-1.2): `make check` en verde, 663 passed, 0 failed; la capa de datos está estable (F15: 1 commit posterior a su tag, +2/−2) [exec-git-02]. Ese verde no mide lo que falta:

```
$ botsito.exe spec check
OK: 28 reglas de spec (25 vigentes, 24 con forma ejecutable), 10 terminos de glosario, hash del manifiesto al dia
$ grep -n 'id: A-2[4-9]' knowledge/spec/ambiguedades.yaml ; echo exit=$?
exit=1
# intérprete de juguete, eventos sintéticos de 2027, solo el vocabulario declarado (§4.1)
trazas_v5/s01b_jornada_vocabulario_estricto.txt  ->  colocaciones=0
```

- **hecho** [exec-git-01] (grave, MATIZADO): la spec cambió de versión MAYOR 9 veces en 64,6 h, 7 de ellas después de `stable/F11` (dos saltos admiten leerse como cierre de un piloto). Un motor escrito contra la spec validada en F11 habría ejecutado reglas que después cambiaron de sentido.
- **hecho** [d8-camino-motor, pregunta 3]: el plan no llega a la meta del dueño. `MASTER_PLAN.html:512`: «Habilita: la decisión de cuenta real, que no forma parte de este plan.» F30 y F32 miden contra el Strategy Tester; ningún criterio cubre "vivo en FundedNext".
- **hecho**: 156 hallazgos, 155 vivos tras los escépticos, 1 refutado; de los vivos, 33 graves y 31 medios que condicionan el motor (los 64 de la §2); ninguna dimensión caída.

### Qué impide hoy empezar el motor sin rehacerlo, por su nombre

**A. La spec no dice lo que F18-F22 tendría que ejecutar.** Todo **hecho**, con el enunciado ya corregido por los escépticos.

| # | Qué falta o está mal | ids | ruta:línea | cita | dictamen |
|---|---|---|---|---|---|
| 1 | Ninguna acción coloca la orden límite inicial ni retira una pendiente (`reentrar` coloca, pero solo tras un *equal*) | d2-fidelidad-huecos-01, d2-fidelidad-huecos-07, d1-interprete-06 | strategy_spec.yaml:151-155, 212-213 | «el motor de F22-F23 implementa esta lista y ninguna otra» | grave, MATIZADO |
| 2 | RN-005 prohíbe el lado de la liquidez donde opera el trader, en los dos sentidos | d2-literal-a-01, d2-fidelidad-huecos-02 | strategy_spec.yaml:495 | «el precio se desarrolla por debajo de la liquidez de M15 en sesgo alcista, o al reves» frente a v1 0:13:12 «Nuestra operativa tiene que estar por debajo» (sesgo alcista) | grave, CONFIRMADO |
| 3 | Qué nivel es la liquidez de M15: sin definición ejecutable; A-24..A-26 solo existen en la prosa de F14b | d2-fidelidad-huecos-05, d8-camino-motor-04 | strategy_spec.yaml:290-291; ambiguedades.yaml:399 (última, A-23) | «la liquidez marcada en M15 que hay que tomar antes de mirar M1» | grave, MATIZADO |
| 4 | La caja no tiene precio: nada dice qué es el nivel 0 ni el nivel 1, y "stop inicial" no se define en ningún otro sitio (ancla sin definir, no círculo) | d2-fidelidad-afirmaciones-01, d2-fidelidad-huecos-03 | glossary.yaml:96-108 | «la distancia entre la entrada y el extremo del stop inicial» | grave, MATIZADO |
| 5 | El breaker de M1 no es computable: qué pivote rompe, qué es el bloque de origen, mecha o cuerpo | d2-fidelidad-huecos-06, d2-literal-a-03 | strategy_spec.yaml:121-134, 547-561 | v4 0:59:20 «Pues es valido con mecha o con cuerpo» / 0:59:56 «Tiene que ser con cuerpo en M1» | grave, MATIZADO |
| 6 | Qué vela H4 fija el sesgo (dos lecturas incompatibles: sesgo distinto en 31 de 42 mañanas) y quién gana en una envolvente (15 de 88 sesiones) | d5-relojes-datos-01, d5-relojes-datos-02, d2-fidelidad-afirmaciones-04, d1-interprete-09 | strategy_spec.yaml:280-289, 440-465 | `vela_h4_previa`: «la vela H4 cerrada inmediatamente anterior al anclaje» | grave, MATIZADO |
| 7 | Cuándo se congelan stop y objetivo: RN-015 dispara al llenarse, contra su título; una entrada por *equal* nace sin objetivo | d2-fidelidad-huecos-04, d2-literal-b-04, d1-interprete-08 | strategy_spec.yaml:736-741, 772-806 | «el objetivo es fijo, se traza con la orden y no se mueve» | grave, MATIZADO |
| 8 | `equal` tiene tres sentidos y el break even no existe como resultado: la forma gasta cartucho donde el trader no | d2-literal-a-02, d2-literal-b-01, d2-literal-b-02 | strategy_spec.yaml:302-303 | «la operacion cerro sin ganancia ni perdida» frente a v6 1:23:19 «te genera una pérdida» | grave, MATIZADO |
| 9 | Nadie declara qué alimenta los acumuladores de pérdida, y el tope diario del 4,5 % se sobrepasa por construcción (4,865 % en `s05a`; resiste las 6 lecturas probadas) | d1-interprete-03, d1-interprete-04 | strategy_spec.yaml:362-377, 924-933 | los acumuladores solo llevan `base` y `reinicia_con` | grave / media, MATIZADO |

**B. Decisiones sin ADR que F18-F23 tomarían por defecto.**

| Decisión | ids | Lo que hay hoy | Coste de errarla |
|---|---|---|---|
| Reloj y modelo de eventos: cierre de M1, tick o evento de orden | d8-camino-motor-01 (grave, MATIZADO) | **hecho**: ningún ADR 0001-0025 lo fija. La "contradicción plan/spec" no se sostiene (el HTML es una instantánea congelada); la decisión sigue sin tomar | reescribir F18-F23 (d8, anexo B) |
| Reglamento de FundedNext | d8-camino-motor-02 (grave, MATIZADO) | **hecho**: ningún parámetro `prop_firm` guarda un límite de pérdida; `MASTER_PLAN.md:246` dice «5 % diario sobre equity a medianoche de servidor, 10 % total» sin cita; la única fuente, `ev-v4-012524-0ef85a89` (UNKNOWN), dice «el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí». **inferencia** (100 000 USD, 0,5 % por pérdida): el 9 % semanal del trader admite 18 pérdidas, más que ese 8 %. El reglamento real: SIN_VERIFICAR | módulo de riesgo; si el veto va sobre equity flotante, el bucle es por tick |
| Semántica de los hechos (F14b) y el evento que falta | d8-camino-motor-04 (grave, MATIZADO), d1-interprete-01 (media, MATIZADO) | **hecho**: `F14b-ciclo-de-vida-de-los-hechos.md:55-56` «**ninguna está documentada como la buena**»; sin un evento `se_marca_liquidez_m15`, las tres alternativas medidas (A, B, H) dejan el bot sin salida tras agotar cartuchos (`h04c`: 3 colocaciones, cartuchos=3). La H del juez no está lista: el contra-juez midió hasta 10 stops sobre la misma toma, y su coste real es 4 reglas nuevas y 19 tokens, no 3 y 17 (§4.7, §9.1) | reescribir F22 y las reglas nuevas |
| Lado BID/ASK y redondeo de stop y objetivo a puntos | d8-camino-motor-09 (media), d8-camino-motor-10 (menor), d5-relojes-datos-06 (media) | **hecho**: ADR-0005:10 fija el M1 de referencia en BID; `MASTER_PLAN.md:247` deja a F18 «stop al lado conservador» sin decir cuál; 0,8 × 137 = 109,6 puntos | rehacer la geometría de F21 y el llenado de F24 |
| Calendario de noticias para RN-028 | d8-camino-motor-06 (media, MATIZADO) | **hecho**: `spec status` «1 vigente(s) SIN CONDICION definida todavia: RN-028 (A-17)»; ninguna fila del plan trae esa fuente | tocar bucle, journal y replay después de F23 |
| Unidad por operación que el motor emite y F26 mide | d7-metodo-07 (grave, MATIZADO) | **hecho**: `kappa.py:52` «la sesion {sesion} aparece dos veces»; al menos 30 de las 68 operaciones de mayo no caben en la gramática; el brief de F14 deja D1/D2 abiertas | rehacer la interfaz de salida de F18-F24 |

**hecho** [d8-camino-motor-03] (media, MATIZADO): el reparto intérprete/código a mano sí existe en prosa (ADR-0019: árbol genérico que despacha por nombre a primitivas escritas a mano; F29 espejo sin traducción), pero falta dejarlo escrito como el que rige, y la `forma` no basta para interpretarse: `perdida_dia` y `perdida_semana` declaran el mismo `reinicia_con: reloj_dia_riesgo` (strategy_spec.yaml:366, 371).

**C. Lo que NO impide empezar.**
- **hecho** [d8-camino-motor-05] (media, MATIZADO): el bloqueo de F14 por F14b solo tiene nombre en `PROJECT_STATE.md:37`, sin commitear: «Lo siguiente es F14b (el ciclo de vida de los hechos), que BLOQUEA a F14». En HEAD, F14 estaba en espera por otros motivos, sin nombrar F14b; ni la tabla A ni el brief de F14 lo sostienen.
- **hecho** [exec-checks-01] (grave, MATIZADO): quitar 7 de las 8 comprobaciones de `problemas_de_spec` deja ruff, mypy, lint-imports y los 663 casos en verde. No obliga a rehacer el motor. Significa que hoy el verde no protege el contrato que el motor va a consumir.
- **hecho** [d7-metodo-06] (grave, MATIZADO): F26 necesita 36 unidades efectivas; holdout-1 da 10-14 y ninguna combinación de mayo llega. No bloquea escribir el motor: bloquea que su cifra autorice la cuenta fondeada.

### Las tres cosas que haría primero, en orden

**hecho** (§1.5, coste medido desde git; es densidad de actividad, no coste total [exec-git-03]): una funcionalidad completa cuesta de mediana 1,58 h activas y 6,64 h de reloj; las tres con reglas del trader (F11-F13), de media 5,99 h activas y 23,91 h de reloj; las 6 unidades de auditoría o decisión fuera del plan, de mediana 1,18 h activas y 2,09 h de reloj.

**1. Cerrar por ADR el bucle, antes de escribir una línea de F18.** Cuatro ADR (d8, anexo E): reglamento real de FundedNext leído (límite diario y total, base equity o balance, hora de corte, noticias, mensajes); reloj y modelo de eventos; lado BID/ASK y redondeo de niveles; y el reparto de ADR-0019 junto con la frontera MQL5. Además, decidir si el calendario de noticias es una funcionalidad propia.
- *Por qué primero.* **inferencia** (de d8, respuesta 2, que pone reloj y prop firm primero y segundo por coste de reescritura, y del anexo E, «nada de esto necesita holdout»): es lo que, mal elegido, reescribe F18-F23; la semántica de F14b (paso 3) está acoplada al reloj y va detrás.
- *Coste.* **hecho**: el coste de leer el reglamento no está en los datos. **inferencia** (usando como referencia las unidades de decisión, 1,18 h activas de mediana cada una): unas 5 h activas para los cuatro ADR, sin contar esa lectura.

**2. Corregir en la spec lo que ya está roto y tiene cita, y abrir como ambigüedades la geometría que falta. Todo antes de la sesión 2 con el trader.**
- *Corregir:* la acción que coloca la orden límite (el trader, `ev-v3-004201-bfeb3734`: «marco mi orden limit y ya está»), el lado de RN-005, el sentido de `equal` y el resultado break even, y el instante de stop y objetivo (RN-013/RN-015).
- *Abrir:* A-24..A-26 (liquidez de M15), nivel 0 y nivel 1 de la caja, breaker de M1, frontera de la zona de control, vela H4 del sesgo y envolvente. A-21 sigue ABIERTA y bloqueante para F20.
- **hipótesis** (§8.1.c): abrir los xlsx de enero, abril y agosto (143 operaciones, no son holdout) fijaría empíricamente el nivel 0 y el nivel 1 y quitaría preguntas al trader. Se comprueba midiendo esas operaciones contra sus velas.
- *Coste.* **inferencia** (es trabajo del tipo F11-F13): al menos una unidad de 5,99 h activas y 23,91 h de reloj de media, una versión MAYOR de la spec y una sesión con el trader, cuyo coste no está en los datos.
- 1 y 2 pueden ir en paralelo.

**3. Cerrar F14b con la H corregida por el contra-juez, detrás del ADR de eventos y de A-24..A-26. En paralelo, abrir F14 (decidiendo D1/D2 con la unidad por operación) y F16, y después F17, enmendando por escrito el orden E.**
- *H corregida:* sin la rama sin cita `se_marca_liquidez_m15` en `zona_perdida.caduca_con`, con el orden fijado dentro de un mismo evento y con una guardia de no más de tres colocaciones por toma; más las respuestas (i)-(iii) de §9.1.
- *Por qué ahora F16.* **hecho**: los ticks de la demo pedidos «desde hoy» el 2026-09-03 siguen sin grabarse (`git ls-files | grep -ic tick` → 0); que sean irrecuperables no está demostrado [d8-camino-motor-07].
- *Coste de H.* **hecho** (juez corregido por el contra-juez, §9.1): 4 reglas nuevas y 6 reescritas; hechos 6→5; tokens 20→19; 2 ADR y una enmienda de ADR-0018; 2 tests reescritos (`tests/unit/test_spec.py:814-821` y `:823-842`); cambiar `src/botsito/spec/modelo.py:1019-1029`; y se deshace F14b §0.
- *Coste de F14, F16 y F17.* **inferencia** [exec-git-06]: entre 3 × 1,58 y 3 × 5,99 h activas.
- **inferencia** (de [exec-git-01] y de que RN-013 figura a la vez en las correcciones del paso 2 y en las reescrituras de H): las correcciones de 2 y de 3 deberían entrar en una sola versión mayor de la spec, no en dos.


## 1. Lo que la ejecución dice (y los documentos no)

Todo lo que sigue se ejecutó el 2026-09-13 en esta máquina (Windows 11, venv del proyecto), sobre el repositorio real en `C:/Users/USER/Desktop/Bot v3`, HEAD `0a9612d`, salvo donde se indique "en un clon" — los clones viven bajo `%TEMP%\botsito-audit\` y nunca en el repositorio (detalle en "Cómo se ejecutó esta auditoría", al final). El criterio de toda la sección es el del encargo: qué impide hoy, por su nombre, empezar a escribir el motor (F18-F24) sin tener que rehacerlo.

### 1.1 `make check`, objetivo por objetivo

**hecho.** Los seis objetivos de `make check` salen en EXIT=0 sobre el working tree del repo original:

| objetivo | orden | EXIT | salida clave |
|---|---|---|---|
| lint | `make lint` | 0 | `All checks passed!` / `123 files already formatted` |
| types | `make types` | 0 | `Success: no issues found in 118 source files` |
| contracts | `make contracts` | 0 | `Analyzed 97 files, 481 dependencies.` / `Contracts: 4 kept, 0 broken.` |
| state | `make state` | 0 | `OK: rama 'main' - funcionalidad actual: Ninguna abierta. Lo siguiente es F14b ...` |
| config | `make config` | 0 | `OK: settings.example.toml (entorno backtest)` |
| knowledge | `make knowledge` | 0 | 9 OK + 2 AVISO; `real 1m11.771s` |

Los dos AVISO de `make knowledge` son: "1 citas localizadas con tiempos de segmento o parciales" y "11 items de evidencia con extractor llm sin propuesta que los respalde (p. ej. `ev-v6-000732-5945fd87`)". Este mismo resultado ya lo había medido hoy el orquestador sobre esta misma máquina: `make check` entero en verde, ruff OK, 123 ficheros formateados, mypy OK en 118, 4 contratos KEPT, 663 passed en 262 s sin skips visibles, state/config/knowledge OK con los mismos 2 AVISOS. Las dos medidas coinciden.

**[exec-checks-07] hecho (menor, MATIZADO).** Ese verde es del *working tree*, no del commit. Sobre un clon limpio de `0a9612d` (`git clone --no-hardlinks`), `botsito state check` da:
```
ERROR: PROJECT_STATE declara la rama 'trabajo/auditoria-de-material'; la rama actual es 'main'
ERROR: 'Last Stable Commit' dice 'b332639'; el tag stable/F13-auditoria apunta a 0a9612d
EXIT=1
```
y `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` falla igual. `git for-each-ref refs/remotes` da `refs/remotes/origin/main 1cf5aa2`: lo que hay publicado (según la referencia local del remoto; no se hizo `fetch`, prohibido) está incluso antes de ese commit. El escéptico de contexto lo corrige: esto no es un hallazgo nuevo, es el estado intermedio que el propio ritual declara a propósito — `docs/HANDOFF.md:192-193` dice literalmente "(`state check` falla a propósito entre el merge y el `docs(state)`)" — y deja de ser un rojo publicado en cuanto merge y `docs(state)` se empujan juntos. Lo que sí es cierto sin matiz: el "`make check` entero en verde" medido hoy, aquí y por el orquestador, no vale para lo que hay commiteado en `0a9612d`; vale para el working tree con el `docs(state)` todavía sin commitear. `exec-cli` verificó lo mismo de forma independiente y llegó al mismo EXIT=1 con los mismos dos ERROR.

`spec check` sobre ese mismo clon de HEAD sí sale en verde: `OK: 28 reglas de spec (25 vigentes, 24 con forma ejecutable), 10 terminos de glosario, hash del manifiesto al dia`, EXIT=0 — la inconsistencia es solo de `PROJECT_STATE.md` con el ritual, no de la spec.

### 1.2 pytest: passed / failed / skipped, y comparación con PROJECT_STATE

**hecho.** Ejecutado en 5 trozos con cobertura acumulada (`--cov-append`), más un trozo de control:

| trozo | ficheros | resultado | tiempo |
|---|---|---|---|
| contract | tests/contract (15) | 95 passed | 84.67 s |
| integration | tests/integration (1) | 11 passed | 12.94 s |
| unitA | test_adr .. test_dukascopy (10) | 133 passed | 169.14 s |
| unitB | test_evidence .. test_kit (6) | 179 passed | 118.36 s |
| unitC | test_motor_prompt .. test_yaml_estricto (14) | 245 passed | 34.00 s |
| unitC5 (control, re-ejecutado) | igual que unitC | 245 passed, EXIT=0 | 35.56 s |
| **total** | 46 | **663 passed, 0 skipped, 0 xfailed, 0 xpassed, 0 failed** | ~419 s (suma de trozos) |

`pytest --collect-only -q` da 663 casos; un `ast` sobre `tests/` da 473 funciones `test_` en 46 ficheros. `tests/golden`, `tests/regression` y `tests/differential` no tienen ningún fichero de test, solo `README.md`. Las duraciones más altas: `test_cli.py::test_knowledge_validate_real_repo` 64.09 s, `test_cli.py::test_cli_entrypoint_runs` 59.73 s, `test_kit.py::test_las_tres_guardias_semanticas_de_decidida_saltan_de_verdad` 47.45 s. La cifra "262 s" del orquestador y los "~419 s" de aquí no son el mismo experimento (una corrida única frente a 5 trozos con overhead de arranque cada uno); ambas dan 663 passed y 0 failed.

**Los 0 skipped son una propiedad de esta máquina**, no de la suite: hay 18 puntos de omisión estáticos (uno de ellos, `test_repository_integrity.py:50`, es un docstring del grep y no cuenta):

| ruta:línea | condición | salta aquí | salta en CI ubuntu |
|---|---|---|---|
| 5× `test_*_history.py` (git) | sin `.git`/sin git en PATH | no | no (fetch-depth 0) |
| `test_repository_integrity.py:60,62` | git ausente / no es repo | no | no |
| `test_golden_citas_f07.py:51` | `knowledge/evidence` vacío | no (367 ficheros) | no |
| `test_hoja_sesion_docx.py:50` | sin paquete en `knowledge/cases/kit/` | no (kit commiteado) | no |
| 4× ffmpeg (`test_fotogramas_ffmpeg.py:35`, `test_audio.py:34`, `test_pipeline_transcripcion.py:66`, `test_cli.py:213`) | sin ffmpeg y sin CI/`BOTSITO_EXIGE_FFPROBE` (si no, `pytest.fail`) | no (ffmpeg en PATH) | no (apt ffmpeg) |
| `test_inventario.py:51` | sin ffprobe | no | no |
| `test_inventario.py:174` | falta `manifest.yaml` | no | no |
| `test_cli.py:63` | HEAD separado | no (rama main) | no en push |
| `test_motor_prompt.py:135` | `importorskip("tokenizers")` | no (asr instalado) | **SÍ** |
| `test_motor_prompt.py:141` | sin large-v3 en caché | no (caché presente) | no se alcanza (salta antes en :135) |

**[exec-checks-08] inferencia (menor, CONFIRMADO).** `tokenizers` solo llega por `faster-whisper`, que está en el grupo `asr` de `pyproject.toml` (`[dependency-groups] asr = [faster-whisper, ...]`), y el CI hace `uv sync --locked --group dev`, sin `asr` — no hay `default-groups` en `pyproject.toml` que lo traiga por defecto. En local el venv tiene `tokenizers-0.23.2` y la caché HF con `large-v3`. **Cómo se comprobaría:** leer el log de un job de CI de `main`, sección "short test summary info", y buscar `SKIPPED [1] tests/unit/test_motor_prompt.py:135`; no se pudo, `gh` no está en PATH y el MCP de GitHub está caído (401). No hay dinero en juego: `corpus/motor_whisper.py` es de la maquinaria de conocimiento (F04, cerrada), no del motor.

**[exec-checks-09] hecho (menor, CONFIRMADO).** `PROJECT_STATE.md:117` dice: *"473 funciones de test (663 casos; parametrizadas x3, x5, x6, x7, x8, x9, x11, x13, x15, x18, x19 y x22)"*. Los totales (473 y 663) cuadran, pero la lista de multiplicidades no: no existe ninguna función x19 ni x22, y sí existen x2 (3 funciones), x4 (3) y x10 (1) que la frase no menciona. Reproducido con `pytest --collect-only` + `sed`/`uniq -c`: las multiplicidades reales por encima de x1 son exactamente {2,3,4,5,6,7,8,9,10,11,13,15,18} (443 funciones x1 + 220 casos extra = 663). Sin impacto de dinero; es una frase descriptiva mal actualizada, de la misma familia que 3.3.14 (véase 1.6).

### 1.3 Cobertura por módulo

**hecho.** Cobertura de líneas y ramas, in-process, unión de los 5 trozos (`coverage 7.16.0`, `branch_coverage True`, 60 ficheros medidos):

| módulo | sentencias | no ejecutadas | % líneas | % ramas | % combinado |
|---|---|---|---|---|---|
| spec/modelo.py | 446 | 37 | 91.7 | 90.3 | 91.2 |
| validation/knowledge.py | 359 | 64 | 82.2 | 77.9 | 81.0 |
| feedback/aplicar.py | 148 | 13 | 91.2 | 82.9 | 88.5 |
| config/registro.py | 315 | 27 | 91.4 | 88.5 | 90.4 |
| cases/paquete.py | 404 | 46 | 88.6 | 79.5 | 86.0 |
| data/agregacion.py | 84 | 2 | 97.6 | 93.8 | 96.6 |
| evidence/verificacion.py | 218 | 5 | 97.7 | 95.1 | 97.0 |
| cli.py | 1400 | 315 | 77.5 | 66.7 | 75.1 |
| domain/valores.py | 78 | 13 | 83.3 | 100.0 | 85.2 |
| domain/velas.py | 68 | 1 | 98.5 | 97.2 | 98.1 |
| spec/manifiesto.py | 100 | 18 | 82.0 | 73.7 | 79.7 |
| corpus/motor_whisper.py | 93 | 51 | 45.2 | 22.2 | 41.4 |
| **TOTAL (60 ficheros)** | **8536** | **945** | **88.9** | **84.3** | **87.6** |

Tres piezas concretas del camino al motor tienen cero ejecuciones en toda la suite, y hoy son inocuas porque el código es trivial y los 52 valores del registro se leen sin error a mano (`scripts/accesores.py`: "ok 52 err 0 sin valor 7"):

- **[exec-checks-05] hecho (menor, CONFIRMADO).** `latencia_ms` está declarado en `parametros.yaml:157-165` como `tipo: minutos` con `unidad: milisegundos de latencia supuesta entre senal y orden`. El registro tipa las unidades para que no se mezclen (ADR-0002; `TIPOS` en `registro.py:33-49` no incluye milisegundos). El accesor que F24 usaría es `Registro.minutos`, con 0 ejecuciones en la suite (`ML 207`). Hoy vale 0 y no se nota. Si el modelo de llenado de F24/F27 lee `registro.minutos("latencia_ms")`, un valor futuro de 250 (ms) se leería como 250 minutos de retraso simulado.
- **[exec-checks-06] hecho (menor, MATIZADO).** `Registro.puntos`, `.minutos` y `.lotes` (registro.py:204,207,210) nunca se ejecutan; tampoco `Fraccion.__sub__`, `__le__` y el `return` de `__lt__`, ni `Porcentaje.__add__/__sub__/__lt__/__le__` (solo se prueba que mezclar clases falla); `agregar_serie` (`data/agregacion.py:139-148`, docstring: *"lo que el motor (F18+) recibe"*) no tiene ni una llamada en `src/` ni en `tests/`. El escéptico confirma los hechos medibles (reproducidos con un plugin de `sys.monitoring` sobre 15 ficheros de test, 321 passed) y ajusta la severidad a menor: es exactamente el lotaje en lotes, el stop en puntos y la aritmética del 0,5 %/4,5 %/9 % — sin red de tests antes de que F18+ los use por primera vez con dinero real.
- **[exec-checks-10] inferencia (menor, CONFIRMADO).** `comprobar_forma` tiene una rama muerta: `if nombre == "hecho": continue` (modelo.py:915-916) nunca se alcanza, porque `_invocaciones` descarta antes toda clave de `_ESTRUCTURALES` (:587-588) y `"hecho"` está en ese conjunto (:639). **De qué dos hechos sale:** el filtrado anterior (:587-588) y la pertenencia de `"hecho"` a `_ESTRUCTURALES` (:639). **Cómo se comprobaría:** un test que pase `{"hecho": "x"}` a `_invocaciones` y compruebe que devuelve `[]`. Sin impacto: induce a leer mal el código, no deja pasar nada.

### 1.4 Las líneas de las siete guardias que ningún test ejecuta

**hecho.** `problemas_de_spec` (`validation/knowledge.py:94-213`) es la única puerta por la que `make knowledge`, `botsito spec check` y el CI ejecutan las 7 guardias semánticas de `spec/modelo.py` (`comprobar_literales`, `comprobar_contra`, `comprobar_decisiones`, `comprobar_precedencia`, `comprobar_consumo`, `comprobar_citas_revocadas`, `comprobar_forma`) más el manifiesto. `scripts/guardias.py` sobre el `cov.json` combinado marca sin ejecutar:

```
spec\modelo.py:comprobar_literales 348-389   | ML 364, 372 | MB 363->364, 369->372
spec\modelo.py:comprobar_decisiones 423-455  | ML 445, 446 | MB 444->445
spec\modelo.py:comprobar_precedencia 458-547 | ML 488, 541 | MB 487->488, 539->541
spec\modelo.py:comprobar_consumo 686-740     | ML 719      | MB 718->719
spec\modelo.py:comprobar_forma 864-1042      | ML 883,897,899,916,1002,1010 | MB 882->883, 896->897, 898->899, 915->916, 1001->1002, 1009->1010
validation\knowledge.py:problemas_de_spec 94-213 | ML 165,182,183,203,204 | MB 164->165
```

Bloque por bloque, qué denuncia cada línea y si hoy funciona cuando se le da un caso a propósito (variantes sobre el YAML de un clon, restaurado después):

| bloque | denuncia | verificado hoy |
|---|---|---|
| modelo.py:363-366 | literal de glosario que no está en su cita | no ejecutado, sin variante |
| modelo.py:369-372 | cita de una regla que no está en evidencia/feedback | no ejecutado (rama de salto) |
| modelo.py:444-446 | `decision` que apunta a un ADR inexistente | no ejecutado |
| modelo.py:487-491 | más de un `fallback` | **variante G: salta** (`hay 2 reglas 'fallback' (RN-013, RN-022)`) |
| modelo.py:539-546 | mismo grupo, parámetros subconjunto, sin `complementa` | **variante F: salta** |
| modelo.py:718-722 | `consumido_por` a una regla DESCARTADA | no ejecutado |
| modelo.py:882-886 | VIGENTE sin forma ejecutable | **variante C: salta** |
| modelo.py:896-897 | `pendiente_definicion` sin formato A-N | **variante B: salta** |
| modelo.py:898-902 | `pendiente_definicion` no es ambigüedad ABIERTA | **variante A: salta** |
| modelo.py:1009-1013 | hecho usado y no declarado en `hechos` | **variante D: salta** |
| knowledge.py:164-168 | regla vigente con parámetro UNKNOWN | **variante E: salta** |
| knowledge.py:182-183 | `ambiguedades.yaml` ilegible → apaga en silencio la comprobación de :898 | no ejecutado |

**[exec-checks-01] hecho (grave, MATIZADO).** Solo 5 tests llegan a `problemas_de_spec`, y todos sobre la spec real, que no tiene problemas (`test_cli_entrypoint_runs`, `test_knowledge_validate_real_repo`, `test_spec_check_corre_sobre_el_repo_real`, `test_la_puerta_de_spec_check_denuncia_y_nombra_ids`, `test_las_tres_guardias_semanticas_de_decidida_saltan_de_verdad`). El auditor mutó la puerta para descartar 7 de sus 8 comprobaciones (mutante M1) y la suite de 13 ficheros pertinentes siguió en verde (231 passed, 1 failed preexistente, ajeno). El escéptico de reproducción fue más lejos: en un clon, **borró literalmente** el código de esas 7 comprobaciones (no solo sus resultados), retirando también los imports y variables que quedaban sin uso —como haría un refactor limpio—, y `ruff`, `ruff format --check`, `mypy` ("Success: no issues found in 118 source files"), `lint-imports` ("4 kept") y **la suite completa de 663 casos** siguieron en verde, EXIT=0. El escéptico de contexto no encontró ningún ADR ni brief que declare esta ausencia de cobertura de mutación como decisión deliberada. Severidad confirmada como **grave**: si `comprobar_forma` o el bucle de UNKNOWN se caen de la puerta, una regla VIGENTE sin forma ejecutable, o que ejecuta un parámetro UNKNOWN como `spread_maximo`, pasa `make check` en verde, y el motor F18-F24 la implementaría desde prosa o con un valor sin confirmar — con la cuenta fondeada de por medio.

**[exec-checks-02] hecho (media, CONFIRMADO).** Las cinco ramas que deciden si una regla es ejecutable (modelo.py:882-886, 896-897, 898-902, 1009-1013; knowledge.py:164-168) funcionan de verdad hoy — las cinco variantes A-E de la tabla saltan con `EXIT=1` y el mensaje correcto—, pero ningún test las ejerce directamente: `test_toda_regla_vigente_tiene_forma_ejecutable` (test_spec.py:711-717) reimplementa el caso de :883 sobre la spec real (`sin_forma = [r.id for r in reglas if r.vigente and r.forma is None]`) en vez de invocar la guardia, y usa `forma is None` donde la guardia usa `not isinstance(r.forma, dict)`. La única prueba de que el contrato con el motor sigue en pie es que alguien rompa la spec real a mano.

**[exec-checks-03] hecho (media, MATIZADO).** De las cuatro denuncias de `comprobar_precedencia` (modelo.py:487-491 "más de un fallback"; :508-512 "mismo disparador sin `complementa`"; :522-528 "mismos parámetros"; :539-546 "subconjunto sin `complementa`"), :488 y :541 no las ejecuta ningún test que pueda llegar a la función (cierre estático confirmado por el escéptico); :509 y :524 solo las ejecuta `test_la_precedencia_no_la_decide_el_orden_del_fichero`, y su único `assert any(...)` lo satisface cualquiera de las dos: la "gemela" de RN-006 dispara ambas a la vez. Con un mutante que apaga solo :509 (`if False:`), la suite queda igual de verde (231 passed, 1 failed preexistente): la línea 509 no está fijada por separado. Es la precedencia lo que el motor usará para decidir qué regla gana en un mismo tick (ADR-0018); si se apaga la detección de disparador idéntico, dos reglas como RN-013 y RN-015 vuelven a competir y gana la que el orden del YAML favorezca.

**[exec-checks-04] hecho (menor, MATIZADO).** `comprobar_citas_revocadas` solo tiene casos positivos para predicados y acumuladores (test_spec.py:845-878); para reglas y glosario solo hay el golden "la spec real no cita nada revocado" (test_spec.py:881-899), así que vaciar `citados` en modelo.py:761-762 (mutante M2) deja la suite igual de verde. Tampoco se ejecutan nunca :364 (literal de glosario no citado), :445 (decisión a un ADR inexistente) ni :719 (`consumido_por` a una regla descartada). El escéptico rebaja la severidad a menor porque el impacto es indirecto: una regla podría seguir citando un registro del trader ya corregido (el caso del lotaje de ADR-0020) sin que nada salte.

### 1.5 Coste unitario medido desde git, y extrapolación a las 22 restantes

**hecho.** Sobre las 14 funcionalidades completas (rama → informe → merge `--no-ff` → tag), en orden topológico:

| grupo | reloj 1er commit→tag (h): mediana [mín–máx] | activo ≤2h (h): mediana [mín–máx] | commits: mediana [mín–máx] | src + insertadas: mediana |
|---|---|---|---|---|
| 14 completas | 6,64 [0,20–46,33] | 1,58 [0,30–6,67] | 13 [4–23] | 1314,5 [114–2025] |
| F01–F10+F15 (11, sin reglas del trader) | — | 1,31 [0,30–2,16] | — | — |
| **F11–F13 (3, primeras con reglas del trader)** | media **23,91** [7,87–46,33] | media **5,99** [5,50–6,67] | media 17,3 | media 1288 |
| 6 variantes (no son filas del plan) | 2,09 [0,05–26,22] | 1,18 [0,19–3,53] | 3,5 [1–20] | 54 [0–338] |

Una funcionalidad concreta, F11 (`feature/F11-strategy-spec-schema`, la primera con reglas del trader): del primer commit (09-09 17:55) al tag `stable/F11` (09-10 11:27:53) van 17,53 h de reloj y 6,67 h activas, 23 commits (10 de fix, tras un hueco de pausa de 10,9 h), y 1357 líneas de `src` + 1097 de `tests`. `author` y `committer` difieren solo en 10 commits de todo el historial (máximo 20,5 min), así que usar una u otra fecha no cambia el resultado en más de 0,35 h. Las horas activas dependen del umbral de pausa elegido: con 0,5/1/2/3/4 h dan 28,3/39,3/48,9/71,9/78,6 h sobre el total (221,4 h de calendario del primer commit al último tag) — **[exec-git-10] hecho (menor, MATIZADO)**, entre 1 y 3 h la cifra se mueve de −20 % a +47 % respecto a la de 2 h; el reloj (primer commit a tag), los commits y las líneas sí son cifras firmes.

**Extrapolación a las 22 unidades restantes (F14, F16-F35 y F14b) — [exec-git-06] inferencia (menor, MATIZADO):**

| escenario | activo | reloj de unidad | calendario (ciclo de trabajo 22,1 %) |
|---|---|---|---|
| E1: mediana de las 14 completas | 1,58 × 22 ≈ 34,8 h | 6,64 × 22 ≈ 146 h | ≈ 9,3 días |
| E2: media de F11–F13 | 5,99 × 22 ≈ 131,8 h | 23,91 × 22 ≈ 526 h | ≈ 27,6 días |
| + variantes al ritmo observado (6 por cada 14) | ≈ 14,5 h más | ≈ 73 h más | — |

**De qué dos hechos sale:** el coste unitario medido de las 14 completas (tabla de arriba) y el ciclo de trabajo global medido con umbral de 2 h (48,9 h activas / 221,4 h de calendario = 22,1 %). **Cómo se comprobaría:** aplicar el mismo método a F14 y F18 en cuanto tengan tag, y contar los cambios de versión mayor de la spec entre la apertura de la rama de F18 y su tag. El escéptico confirma la aritmética al decimal pero corrige el paso a calendario: con la razón coherente entre horas activas y horas de calendario realmente medida en las 20 ventanas de rama (5,34, no el ciclo global del 22,1 %), E2 sale en ~32,6 días y E1 en ~11 días — el orden de magnitud no cambia. El límite real de calendario no lo pone el ritual: lo pone F34 ("3 meses en umbral", `MASTER_PLAN.md:112`) y las esperas humanas (mediana de 4,26 h del informe al merge, máximo 25,11 h en F07).

**[exec-git-01] hecho (grave, MATIZADO).** Según su propia política de semver (ADR-0013:23, "mayor si una regla cambia de sentido o desaparece"), la spec declaró **9 cambios de versión MAYOR en 64,6 h**, de `1.0.0` (85de674, 09-09 19:36) a `10.0.0` (cea9a86, 09-12 12:10) — uno cada 7,2 h. El usuario validó F11 con la spec en `3.0.1` (tag `stable/F11`, 09-10 11:27:53); después de ese tag llegaron 7 más: `4.0.0`, `5.0.0`, `6.0.0`, `7.0.0`, `8.0.0`, `9.1.0` (tag `stable/F12`) y `10.0.0`. El hash del manifiesto cambió 13 veces después de `stable/F11`. Los propios mensajes de commit dicen qué cambió de sentido: *"el reloj del trader es civil, no un offset fijo, y eso movia todas las velas H4"* (94980a9), *"el freno de riesgo no frenaba y el break even era inalcanzable"* (fe9ee21), *"el 0,5 % se mide EN el 0,8, y eso invierte RN-012"* (eb19970), *"la auditoria encontro que se entraba sin liquidez"* (59b16f6), *"el bot no opera noticias"* (cea9a86). La versión se sube a mano (`cli.py:844`, comentario propio: "Recuerda subir spec_version si la spec cambio de verdad"); ninguna herramienta verifica que el nivel semver elegido sea el correcto. El escéptico de reproducción confirma los números exactos pero matiza que no todos los saltos "mayores" cumplen sin discusión el criterio del ADR-0013 (dos de ellos podrían leerse como el cierre de un piloto, no como cambio de sentido); el escéptico de contexto reproduce la secuencia completa y sube la severidad de vuelta a grave. Con impacto: un motor escrito contra la spec "validada" de `stable/F11` habría operado con reglas que después se declararon con otro sentido — lote mal calculado, freno de riesgo que no frenaba, entradas sin liquidez.

**[exec-git-02] hecho (grave, MATIZADO).** Tras `stable/F11`, los ficheros de `src/`+`tests/` nacidos en F11 (sin `cli.py`) recibieron **1706 líneas +/− en 15 commits** (11 de fix o auditoría, 1253 líneas): 1338 en F12, 357 en F13, 11 en F13-auditoria — el 70 % de lo que la propia F11 había insertado. `src/botsito/spec/modelo.py`, donde viven las 7 guardias semánticas, es el fichero más retrabajado del repositorio: 942 líneas después de su tag (925d3f6: *"el arreglo de los siete defectos estaba parcialmente mal, y la guardia era decorativa"*). Contraste: la capa de datos del mercado (F15, `data/` y `domain/velas.py`) solo tuvo 1 commit posterior a su tag, +2/−2. El escéptico de reproducción matiza el marco: en F11 `modelo.py` tenía 354 líneas y 3 guardias; F12 (Validación semántica, ya planificada como unidad separada) le añadió las otras 4, así que parte de esas 1706 líneas es la extensión prevista, no solo corrección — el diff neto de `modelo.py` de F11 a HEAD es +699/−11, y el 97 % de sus líneas de F11 siguen en HEAD según `blame`. El escéptico de contexto reproduce los mismos números exactos y no encuentra motivo para bajar la severidad: la guardia "decorativa" de 925d3f6 sí fue un defecto real posterior al tag. La inestabilidad está en la capa de reglas, no en la de datos, y eso es lo medible sin discusión.

**[exec-git-05] hecho (menor, MATIZADO, mueve la aguja).** De los 20 tags `stable/*`, 6 no son funcionalidades del `MASTER_PLAN` (F05-auditoria-1, F05-previos-F07, F10-sesion-01, F12-holdout, F13-decisiones, F13-auditoria): consumieron 36 commits, 9,2 h activas y 46,4 h de reloj (22-23 % del total de las 20 unidades). La rama `feature/F14-case-library` se creó el 09-12 a las 22:42:54 y **17 minutos después** se renombró a `trabajo/auditoria-de-material`; en todo el historial, F14 tiene **0 commits** en su rama original. F18, la primera funcionalidad del motor, depende de F11 y F14 (`MASTER_PLAN.md:94`). El escéptico confirma los hechos de git pero matiza que el propio plan prevé estas ramas de auditoría (`MASTER_PLAN.md:172-176`); lo que no matiza es el hecho central: el camino F14→F18 no ha empezado.

Los cinco restantes de exec-git son **menores** y todos MATIZADO por severidad ajustada, con el núcleo confirmado en cada caso: **[exec-git-03]** el coste unitario (tabla de arriba) reproduce exacto pero es "densidad de actividad en git", no coste total de trabajo, porque el reflog local no viaja a un clon (sin él, la mediana global baja a 1,09 h y F11-F13 a 5,94 h de media — sigue siendo ~6× más). **[exec-git-04]** 11 de 14 informes de validación nacen con `Estado: WAITING_FOR_USER_VALIDATION` a mitad de rama (mediana 0,50) y reciben fixes después (75 commits, 41 de fix/auditoría); el escéptico ubica el incumplimiento real solo en F11 y F05, porque la regla de HANDOFF que ordena "auditoría → correcciones → informe WAITING" nace el 09-05 y varias de las 14 son anteriores. **[exec-git-07]** `PROJECT_STATE.md` lo tocan 131 de 232 commits, creció de 7,7 a 127,5 KB (pico 147 KB), y su churn de 549 KB en líneas equivale al 64 % del de `src/`; medido por palabra (sus líneas son párrafos largos) el churn real es ~304 KB, el 39,5 % del de `src/` (769 KB). **[exec-git-08]** desde el 09-04 a las 20:58 (`697890e`) nadie ha tocado `domain/`, `engine/`, `mql5bridge/` ni `viewer/`: 139 commits después, 0 en esas carpetas; en toda la historia, 84 de 232 commits tocan `src/` y 84 son solo docs/`PROJECT_STATE.md`/README. **[exec-git-09]** HEAD está a mitad de ritual (merge y tag hechos, falta el `docs(state)`, `origin/main` sigue en `1cf5aa2`); ya se rompió antes en F01 (`docs(state)` antes que el tag) y F11 (26 min antes, con `amend`).

### 1.6 Veracidad de lo que imprime la CLI

**hecho.** Las 14 órdenes prescritas por el encargo salen con `exit 0` sobre el repo original (el `data check` del dataset de mayo no se ejecutó, por la regla de holdout). Los recuentos que la CLI imprime cuadran, contados de forma independiente con Python sobre los YAML: 28/25/24 reglas, 22 predicados, 13 acciones, 2 efectos, 6 hechos, 3 acumuladores, 20 tokens, 59 parámetros (50/7/2), 23 ambigüedades (14/3/6), 364 items de evidencia, 118 registros de feedback (73 activos). Las frases que fallan no son esos recuentos: son guardias que se anuncian y no se ejecutaron.

| frase impresa | fuente | veredicto |
|---|---|---|
| `59 parametros (8 sin confirmar)` | 9 parámetros no CONFIRMED en `parametros.yaml` | **FALSA** — [exec-cli-04] |
| `particiones anteriores al etiquetado` | 0 registros LABEL_CASE; la guardia no corre | **VACUA** — [exec-cli-03] |
| `kit check`: "sin diferencias que no explique la sesión" | sin datos, no compara nada | **FALSA sin datos** — [exec-cli-02] |
| A-22 "no las respondió el trader" | fb-...-3565552d: *"Si, incluimos noticias"* | **MATIZADA/FALSA para A-22** — [exec-cli-05] |
| `state check`: "Ninguna abierta ... tag stable/F13-auditoria" | cierta en el working tree; en HEAD, EXIT=1 | cierta solo en el working tree — [exec-checks-07] |
| resto (videos, transcripciones, extracciones, reglas, glosario, ambigüedades, feedback, evidencia) | contados con Python | **cierta** |

**[exec-cli-04] hecho (menor, MATIZADO).** `knowledge validate` imprime *"OK: registro con 59 parametros (8 sin confirmar)"*, pero `parametros.yaml` tiene **9** parámetros no CONFIRMED (7 UNKNOWN + 2 DEFAULT_AMBIGUOUS). El número sale de `no_confirmados()`, que por diseño declarado (ADR-0004, ADR-0015, `registro.py:167-174`) solo cuenta la categoría `estrategia`; el que falta es `reloj_dia_riesgo` (categoría `prop_firm`, DEFAULT_AMBIGUOUS, A-19 ABIERTA, valor "servidor"). El rótulo impreso no dice "de estrategia". `spec status`, en la misma sesión, sí suma 9 ("2 con un default nuestro, 7 sin valor"). Con dinero: `reloj_dia_riesgo` marca cuándo se reinician `perdida_dia` (tope 4,5 %) y `perdida_semana` (9 %) — `strategy_spec.yaml:366,371`; con el corte en el reloj equivocado, el bot podría sumar pérdidas de dos días de FundedNext como si fueran uno.

**[exec-cli-03] hecho (menor, MATIZADO).** La inmutabilidad de `particiones.yaml`/`ventanas.yaml` (`cases/paquete.py:641-643`) solo se aplica tras el primer `LABEL_CASE`, y hoy hay cero. `knowledge validate` aun así imprime "particiones anteriores al etiquetado", una verdad vacía. Reproducido en un clon: permutar el día `2026-05-04` de `holdout-1` a `dev` (y `2026-05-08` al revés) en `particiones.yaml`, o recortar `hasta_utc` y poner el `sha256` a ceros en `ventanas.yaml`, commiteado con cualquier `Fuente:` válida (probado con `ADR-0025` y `ADR-0011`), deja `knowledge validate` y `kit check` en `EXIT=0` con el mismo OK. Sin trailer, `knowledge validate` sí lo rechaza ("toca spec/cases sin trailer 'Fuente:'"), pero eso no protege el contenido. El escéptico confirma el núcleo y añade que la única prueba mecánica que cita ADR-0025 (`kit check` con los datos presentes) sí detecta una permutación cuando `data/` está disponible. Con dinero: F26 mide sobre `holdout-1` la fidelidad que decide pasar el bot a una cuenta fondeada de 100 000 USD.

**[exec-cli-02] hecho (menor, MATIZADO).** `kit check` (`cli.py:1360-1363`) imprime *"OK: {sesión} sin diferencias que no explique la sesion celebrada"* siempre que haya avisos, sin distinguir el aviso real de "sesión celebrada" del aviso "datos de los datasets ausentes en data/: solo esquema" (`paquete.py:559-563`), con el que no se recompone ni compara nada. Reproducido en un clon sin `data/` (el estado de cualquier clon o de la CI): `AVISO: ... datos ... ausentes: solo esquema` seguido de `OK: ... sin diferencias que no explique la sesion celebrada`, EXIT=0. El modo "solo esquema" está declarado (ADR-0011:63); lo que no está declarado es que el texto del OK afirme una comparación que no ocurrió.

**[exec-cli-05] hecho (menor, MATIZADO).** El registro `fb-2026-09-09-sesion-01-3565552d` (activo, CORRECT sobre `filtro_noticias`, respuesta literal *"...Si, incluimos noticias"*, `valor_canonico: "no"`) sale en `feedback pending --todos` como "(ok) ... categoria prop_firm: no se pregunta (ADR-0004)" — es decir, entre los reflejados, cuando sí se preguntó y la respuesta registrada fue la contraria a lo que hoy corre (`filtro_noticias: regla`, fuente ADR-0022). `spec status` pone A-22 bajo "Cerradas por decisión del consultor (no las respondió el trader)" con el mismo choque. Esto contradice el propio docstring de `feedback_pending` (`cli.py:1629`): "NUNCA AFIRMA MAS DE LO QUE PUEDE COMPROBAR". Con dinero: el backtest del trader opera noticias y el bot las descarta por RN-028 (gate sin condición, A-17 abierta); en F26 esas operaciones aparecerán como infidelidad del bot, sin que la CLI deje rastro de que la divergencia es deliberada.

**[exec-cli-06] hecho (menor, CONFIRMADO).** `spec status` (`cli.py:693`) llama "a propósito" a todos los UNKNOWN sin comprobar que tengan un REJECT que lo justifique, y el detalle (`cli.py:724-727`) usa `cargar_feedback` sin `activos()`, así que un REJECT ya supersedido seguiría contando. Hoy cuadra (los 7 UNKNOWN tienen un REJECT activo) y el defecto está latente: reproducido en un clon, tras un `RESOLVE_UNKNOWN` sobre `spread_maximo` con `supersede` del REJECT anterior, `spec status` lo sigue anunciando como "Sin valor A PROPOSITO, con su registro REJECT (leerlos falla)" mientras `feedback pending` ya lo cuenta entre los pendientes — las dos órdenes se contradicen.

**[exec-cli-01] hecho (menor, MATIZADO).** `data aggregate --help` sigue anunciando *"(A-9 sigue abierta)"* y el docstring de `cli.py:1823` dice que `anclaje_h4` "sigue UNKNOWN (A-9)"; ambos textos son de F15 (fa2eefa, 2026-09-04) y nadie los actualizó cuando A-9 quedó RESUELTA y `anclaje_h4` pasó a CONFIRMED (17:00 America/New_York, ADR-0017). La orden acepta cualquier ancla por argumento y no la contrasta con el registro. Reproducido con el mismo día (`2026-01-14`, invierno) y las dos anclas: con `17:00 America/New_York` la vela H4 de la mañana sale bajista (`10:00Z 116520→116500`, −20), con `23:00 Etc/GMT-2` sale alcista (`09:00Z 116474→116596`, +122) — ambas con EXIT=0. Ningún código de `src/` lee `anclaje_h4` del registro (solo el docstring y un comentario en `feedback/aplicar.py:274`). Con dinero: el sesgo H4 decide la dirección de toda operación; quien genere velas H4 o goldens siguiendo la ayuda de la CLI puede usar el ancla anterior a ADR-0017 e invertir el sesgo, sin que ninguna salida lo avise.

**[exec-cli-08] hecho (menor, CONFIRMADO).** El docstring de `feedback_pending` (`cli.py:1631-1636`, escrito en c9ba546, 09-12 15:44) sigue diciendo que `_contradicciones.yaml` *"seguia -y sigue- diciendo que stop.nivel esta ABIERTA"* y que hay *"los ocho CORRECT y REJECT"* sin mecanismo. Hoy `_contradicciones.yaml` es `contradicciones: []` desde 2003e61 (`knowledge validate` cuenta 0 abiertas), y son **9** los CORRECT/REJECT sin mecanismo (6+3), no 8: el noveno entró en b634d5d (09-13). Es la misma familia de defecto que 3.3.14/exec-cli-01: texto que describía un estado real y no se actualizó cuando el estado cambió.

**[exec-cli-07] hecho (media, MATIZADO).** No hay `CLAUDE.md` ni `.claude/` en la raíz del repositorio, ni en `~/.claude/CLAUDE.md`; `~/.claude/settings.json` no tiene hooks ni reglas de `deny` sobre `knowledge/` u holdout. A un agente solo le llega el índice `MEMORY.md` del usuario. Lo que existe como mecanismo: el pre-commit (rechaza commits en `main` sin `BOTSITO_ALLOW_MAIN=1`, y ediciones de `*.yaml` en `knowledge/evidence`, `knowledge/feedback`, `data/manifests`, `corpus/transcripciones` y `corpus/fotogramas`), `uv lock --check`, `lint-imports` y el trailer `Fuente:` exigido por `knowledge validate`. No protegen: nada editado sin commitear, `--no-verify`, un clon fresco (sin hook instalado), ni `knowledge/spec`, `knowledge/cases/kit|holdout`, `docs/adr` o `PREREGISTRO.md`. La guarda de lectura de holdout que ADR-0001 remite a "en tests" es un *stub*: `tests/conftest.py:17-25`, fixture `holdout_guard`, `return None`, sin `autouse`. El escéptico de reproducción matiza: esta ausencia de mecanismo para la *lectura* de holdout ya está declarada como deuda por escrito (el propio `conftest.py:19` dice "se implementa... en F14"; `ADR-0001:44-45` la fecha igual), y la única defensa viva es `test_domain_and_spec_never_mention_holdout`, que busca la cadena `"holdout"` solo en `src/botsito/domain` y `spec`. El escéptico de contexto sube la severidad de vuelta a media: el vacío de mecanismo para la *escritura* sin commitear y para agentes que trabajen fuera de esas dos carpetas no está declarado en ningún ADR. Con dinero: cuando se escriba F18-F24, un test o fixture de `domain/`/`spec/` que lea `knowledge/cases/holdout` pasaría todas las puertas, y la cifra de fidelidad de F26 —la que autoriza operar en la cuenta fondeada— quedaría contaminada sin que nada lo registre.

### 1.7 Lo que solo corre en Windows y no tiene veredicto

**hecho.** El único job de CI es `ubuntu-latest` (`ci.yml:15`); el job de Windows se aplaza a F29 y es solo para compilar MQL5. Ningún código Python del proyecto se ejecuta en Windows de forma automática hoy.

| ruta | qué hace | test que la ejecuta | dónde tiene veredicto |
|---|---|---|---|
| `cli.py:2145-2147` | stdout/stderr a UTF-8 y LF | `test_cli_data.py:124` (subproceso) | newline: solo Windows local; encoding: **ninguna** |
| `cli.py:42-51` | git con `quotepath=false` y utf-8 (`state check`) | `test_cli.py` (sin nombres no ASCII) | **ninguna** |
| `comun/historial.py:53` | `core.quotepath=false` | `test_evidence_history.py:123` | ambas plataformas |
| `comun/historial.py:56-57` | decodificar git en utf-8 | `test_feedback_history.py:87-92` | solo Windows local |
| `comun/historial.py:124-126` | `os.path.normcase` | ninguno lo discrimina | **ninguna** |
| `corpus/motor_whisper.py:40-52` | `add_dll_directory` CUDA | ninguno | **ninguna** (sin grupo asr en CI) |
| `corpus/inventario.py:279` | orden por cadena POSIX | `test_inventario.py:178` | solo Windows local |
| `data/velas.py:149` (y 12 más) | LF en escrituras | `test_velas.py:97` | solo Windows local |
| `data/dataset.py:344-350` | ruta relativa en manifiesto | `test_dataset.py:214` (solo `../`) | **ninguna** para `C:/` |
| `comun/husos.py:23-28` | nombre IANA exacto; rama sin tzdata | `test_agregacion.py:96` | guardia: ambas; rama sin tzdata: **ninguna** |
| `scripts/git-hooks/pre-commit` | main, inmutables, uv, lint-imports | `test_fotogramas_history.py:63` (busca una cadena) | **ninguna** |
| `scripts/instalar_hooks.py` | copia hooks | ninguno | **ninguna** |

**[exec-windows-01] inferencia (menor, MATIZADO, mueve la aguja).** Cuatro mutaciones de defectos que el proyecto ya sufrió en Windows hacen fallar su test aquí y, según el funcionamiento de Python en Linux (comprobado con el proxy `PYTHONUTF8=1` para M3; sin WSL ni docker para los demás, `wsl.exe --list` no instalado), pasarían en el CI:

```
M2 (cli.py sin reconfigure de newline): assert b'\r' not in ...  -> FALLA en Windows
M3 (historial._git con text=True):      UnicodeDecodeError 0x8d  -> FALLA en Windows, PASA con PYTHONUTF8=1
M5 (velas.py:149 sin newline):          b'\r' != b'\n'            -> FALLA en Windows
M6 (inventario.py:279 orden por Path):  '_procesado/alfa.md' != 'Material adicional/balance.jpeg' -> FALLA en Windows
```
No hay guardia estructural de LF: las 13 escrituras de texto de `src/` llevan `newline="\n"` por disciplina, sin ningún test de contrato que lo exija; cada escritor nuevo necesita su propio test, y ese test solo fallará en Windows. F18-F22 (dominio) quedan fuera de este riesgo: el contrato de importación les prohíbe `datetime`, `zoneinfo`, `os`, `pathlib`, `io`. F23-F24 (journal "mismo sha256", lectura de CSV, husos) sí dependen de plataforma, y su ejecución en la máquina Windows donde vive MT5 no tendría veredicto automático. **Cómo se comprobaría:** empujar cada mutación a una rama `feature/` por separado y ver el job ubuntu.

**[exec-windows-02] hecho (menor, CONFIRMADO).** El `encoding="utf-8"` del `reconfigure` de `cli.main` (`cli.py:2145-2147`) no lo discrimina ningún test en ninguna plataforma: el único test que invoca `main` por subproceso (`test_cli_data.py:124-176`) solo comprueba la ausencia de `\r`. Quitando `encoding` y dejando `newline`, ese test pasa igual y la CLI con salida redirigida muere con `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'` en cuanto imprime algo fuera de cp1252. Hoy funciona: a fichero y a tubería salen bytes UTF-8 y LF (`feedback trace "fb-→«ñ»"` → `342 206 222 302 253 303 261 302 273`, EXIT=0).

**[exec-windows-03] inferencia (menor, MATIZADO).** Si se pierde la decodificación UTF-8 de git (`text=True` en vez de `encoding='utf-8', errors='replace'`), `_git` devuelve `None` y `commits_sin_fuente(...) or []` da `[]` en Windows; PYTHONUTF8=1 lo arregla. El escéptico amplía el alcance real: la mutación rompe al menos 3 tests, no 1 (`test_trailer_fuente`, `test_repositorio_real`, `test_rutas_con_acento_y_espacio_se_vigilan`), pero corrige la conclusión práctica — el consumidor de producción, `knowledge validate` (`validation/knowledge.py:452-456`), sí distingue `None` de "sin problemas" y emite `ERROR: la comprobacion de trailers Fuente: no se pudo evaluar`. La pérdida sería solo de detección local en Windows antes de commitear, no de la guardia en producción.

**[exec-windows-04] hecho (menor, CONFIRMADO).** El único test del hook busca una cadena en su texto (`test_fotogramas_history.py:63`); el CI no instala hooks; `scripts/instalar_hooks.py` solo lo invoca `Makefile:15`. Con el hook bueno instalado en un clon: rechaza editar evidencia, rechaza commits en `main` sin `BOTSITO_ALLOW_MAIN=1`, rechaza si `uv` no está en PATH; **acepta** editar `particiones.yaml` de una sesión ya celebrada y `strategy_spec.yaml` sin trailer (eso lo caza el CI por el trailer); **acepta** `STOP_FRACCION = 0.8`, `VENTANA_INICIO = "07:00"`, `HUSO = "Europe/madrid"`, `RR = 3`, `RIESGO = 0.005` en `engine/__init__.py` — el contrato de literales de negocio solo caza `0.8` y `"07:00"`, no `"Europe/madrid"`, `3` ni `0.005`. En Windows, `ZoneInfo("Europe/madrid")` resuelve. `--no-verify` salta todo el hook siempre.

**[exec-windows-05] hecho (menor, CONFIRMADO).** `_anadir_dlls_cuda`, `MotorWhisper._cargar`, `describir`, `transcribir` y `_gpu` (`corpus/motor_whisper.py:40-52,124-136`) solo se alcanzan desde `cli.py:254,256` (`corpus transcribe`, a mano, con GPU real); ningún test los llama. En ubuntu el `hasattr(os, "add_dll_directory")` los deja inertes y el CI no instala el grupo `asr`. Sin impacto sobre el motor de trading: es la ruta de re-transcribir el corpus (F04, cerrada).

**[exec-windows-06] hecho (menor, CONFIRMADO).** La guardia de ruta de `dataset.py:344-350` (`or ".." in ruta`, `or ruta[0] in "/\\"`) rechaza `/x.csv`, `\x.csv` y `../x.csv`, pero **acepta** `C:/Windows/win.ini` y `C:\Windows\win.ini` — no contempla una letra de unidad como prefijo absoluto de Windows. Reproducido con un manifiesto sintético: `'C:/Windows/win.ini' ACEPTADA -> se une como C:\Windows\win.ini | comprobar: ['tamano distinto: C:/Windows/win.ini']`. El único caso de test existente es `../x.csv`. `cargar_serie` sí verifica el sha256 después, así que no entraría contenido distinto al declarado en el manifiesto; el hueco es de contención de `data/`, no de fidelidad.

**[exec-windows-07] hipótesis (menor, MATIZADO).** En Windows, `zoneinfo.TZPATH=()` y `tzdata` (fijado en `pyproject.toml:9` como `>=2026.3`, instalado 2026.3/IANA 2026c) es la única fuente de husos; en Linux, `zoneinfo` busca primero en los directorios del sistema y solo recurre al paquete si no encuentra la zona ahí (comportamiento documentado de la librería estándar). **De qué se sostiene:** lo medido en Windows (TZPATH vacío, versión de `tzdata`) es hecho; que el job `ubuntu-latest` use la base del sistema en vez de la de `uv.lock` es hipótesis, porque no se pudo mirar dentro del runner de CI. **Cómo se comprobaría:** en un job de CI, `python -c "import zoneinfo;print(zoneinfo.TZPATH)"` y `dpkg -s tzdata | grep Version`, comparando con IANA 2026c. Efecto colateral medido (no es del ámbito de esta dimensión, ver 3.1.2): `ZoneInfo("Europe/madrid")` y `ZoneInfo("Europe/MADRID")` resuelven conservando la clave mal escrita; `"europe/madrid"` y `"EUROPE/MADRID"` fallan.

**[exec-windows-08] inferencia (menor, MATIZADO).** El comentario de `ci.yml:26` ("la version la fija .python-version (la misma que en local)") es cierto solo a nivel de versión menor: `.python-version` dice `3.12`, y el venv local es CPython `3.12.10` de python.org. `uv python list 3.12` ofrece además `cpython-3.12.14-windows-x86_64-none <download available>`; en un laboratorio aislado, `uv python install` con `.python-version=3.12` y la 3.12.10 ya presente **descarga** la gestionada más reciente y la usa. CI y local no comparten parche ni distribución (`python-build-standalone` frente a python.org). Con dinero, bajo: solo afecta a la promesa de "mismo sha256" de F23 si algo del parche cambiara la salida.

### Cómo se ejecutó esta auditoría

El Workflow orquestado se abandonó tras tres intentos sin un solo agente terminado (peticiones de subagentes que superaban los 3 min y el vigilante reiniciaba desde cero; en el segundo intento se agotó además el límite de sesión). Esta auditoría se hizo con subagentes lanzados a mano, cada uno con su `RESULTADO.json` en disco, reanudados con su contexto cuando caían; el límite de sesión de la cuenta se alcanzó cinco veces. Por coste, a mitad de la verificación se recortaron tres cosas: la lente de impacto de los hallazgos graves (quedaron con reproducción + contexto, sin una tercera lente); los dictámenes que los propios auditores añadieron sobre el contexto del encargo (no las afirmaciones numeradas del prompt) quedaron sin escéptico, y se marcan así donde aparecen; y la segunda opinión de contexto se omitió cuando el primer escéptico ya MATIZABA un hallazgo medio, porque no podía cambiar el veredicto. La última tanda de verificaciones se hizo con Sonnet en lotes; los 17 investigadores, el intérprete de juguete, las dos alternativas de F14b, el escéptico del intérprete y el juez corrieron con Opus.

**Las órdenes de git que escriben (commit, checkout de restauración, reset, rebase) se ejecutaron solo en clones desechables bajo `%TEMP%\botsito-audit\`, nunca en el repositorio original.** Cada dimensión lo verificó por su cuenta al terminar (`git rev-parse --show-toplevel` apuntando a `Temp` antes de escribir, y `git status --short` del original mostrando solo el cambio del dueño en `PROJECT_STATE.md`, intacto de principio a fin). Un escéptico corrió un `rebase` y un `reset` para reproducir un hallazgo de historial: fue en su propio clon; el reflog del repositorio original no tiene entradas posteriores al merge del dueño de las 00:31 del 09-13.

Una incidencia de integridad: hacia las 19:18 (hora local) un agente no identificado dejó un fichero vacío sin versionar, `B_kv.txt`, en la raíz del repositorio original; desapareció minutos después. Las comprobaciones del orquestador contra la foto previa (refs, diff de `PROJECT_STATE.md`, stash, ramas, reflog) salieron intactas en las dos comprobaciones intermedias y en la final.

Exposiciones declaradas por los agentes, todas de bajo alcance y sin lectura de etiquetas ni de precios de mayo: en `exec-cli`, un intento anterior ejecutó `kit check --sesion 2026-09-09-sesion-01` sobre el repositorio original con `data/` presente, lo que recompone `ventanas.yaml` y por tanto lee las velas M1 de los días del kit —incluidos días de mayo de 2026— para calcular `sha256` y `n_velas`; no se leyeron etiquetas ni ninguna cifra del bot, la salida solo mostró dos AVISO, y no se repitió. Fuera del alcance de esta sección (dimensión `d7-metodo`), la misma orden se ejecutó una vez más por mandato explícito de una tarea del encargo, con el mismo resultado y la misma ausencia de lectura de etiquetas. En el resto de dimensiones de esta sección (`exec-checks`, `exec-git`, `exec-windows`) no se abrió ningún fichero de `knowledge/cases/holdout/` ni se leyó ninguna vela de mayo de 2026; donde se tocó `particiones.yaml` fue solo la asignación de días a partición (permitida) o, en `exec-windows`, una línea de comentario añadida sin leer el contenido.

Incidencias menores sin efecto en los resultados: relanzamientos por corte de sesión reaprovechando `NOTAS.md` y logs previos verificados antes de reutilizarlos; llamadas a Bash rechazadas temporalmente por el clasificador de modo automático, repetidas con Grep sin cambio en los resultados; un script de medición de tiempos (`medir.py`) que ordenaba commits por fecha en vez de por topología se sustituyó por uno con `--topo-order` tras detectar que falseaba empates de segundo; y varios `UnicodeEncodeError` de consola (cp1252) al imprimir texto con tildes o flechas, resueltos con `PYTHONIOENCODING=utf-8` o redirigiendo a fichero, sin efecto sobre las mutaciones ni las mediciones.


## 2. Bugs y riesgos graves

Orden: de más a menos aguja movida sobre "¿se puede empezar a escribir el motor (F18-F24) sin tener que rehacerlo después?", no por dimensión de auditoría. Cada hallazgo lleva sus ids de origen entre corchetes; cuando varias dimensiones cazaron el mismo defecto se fusionan citando todos los ids.

### A. La spec, tal como está escrita, no es ejecutable

**[1] [d2-fidelidad-huecos-01, d2-fidelidad-huecos-07, d1-interprete-06] Ninguna acción coloca la orden límite ni ninguna la cancela.**
**Hecho.** De las 13 acciones del vocabulario (`fijar, cerrar_a_mercado, reubicar_orden_limite, mover_stop, agrupar_estructura, dimensionar_lote, escribir_stop_en_la_orden, fijar_objetivo, realizar_perdida, gestionar_salida, reentrar, redondear_lote, abstenerse`) ninguna coloca la orden límite inicial; `se_da_esquema` solo aparece NEGADO, dentro del `ninguno_de` de RN-008; RN-011 se dispara con el evento `se_coloca_orden_limite`, que ninguna regla produce. La única acción que coloca una orden es `reentrar`, y solo la usa RN-019 tras un cierre por *equal*. Tampoco existe acción para retirar una pendiente: `orden_limite_pendiente` solo se apaga en RN-013, al llenarse; RN-002 (las 15:00) solo cierra `operacion_abierta`. **Dónde:** `knowledge/spec/strategy_spec.yaml:121-134` (se_da_esquema), `151-155` (se_coloca_orden_limite), `214-253` (acciones), `581-586` (RN-008), `664-677` (RN-011), `428-436` (RN-002), `741` (único apagado de orden_limite_pendiente). **Cita:** «se_coloca_orden_limite: descripcion: se envia la orden pendiente, con su lote, su stop y su objetivo» / RN-008 «entonces: prohibe: [abrir_operacion]» / RN-011 «cuando: todos_de: - se_coloca_orden_limite: {}».
Se reproduce:
```
$ python s2/forma.py
acciones: ['fijar','cerrar_a_mercado','reubicar_orden_limite','mover_stop','agrupar_estructura',
           'dimensionar_lote','escribir_stop_en_la_orden','fijar_objetivo','realizar_perdida',
           'gestionar_salida','reentrar','redondear_lote','abstenerse']
RN-008 gate cuando=['NO se_da_esquema','NO se_da_esquema'] prohibe=['abrir_operacion']
RN-011 disparador cuando=['se_coloca_orden_limite'] hace=['dimensionar_lote','escribir_stop_en_la_orden','fijar']
```
En el intérprete de juguete, con `colocacion_implicita=false` la jornada entera da `colocaciones=0` (trazas_v5/s01b); rellenando el hueco con una colocación implícita, una límite viva sobrevive a las 15:00 y se llena fuera de ventana:
```
trazas_v5/s06a_orden_viva_15h.txt
[15:00] disparan: gate=[RN-001, RN-008]                        # nada retira la pendiente
[16:10] BROKER llena la limite 1.10000 lote=6.25 stop=1.0992   # fuera de la ventana 07:00-15:00
[martes 15:00] BROKER cierra posicion por cierre_forzoso a 1.09950: pnl=-312.50
```
**Con dinero:** hecho/inferencia. Leída al pie de la letra, la spec no abre nunca una operación: cero operaciones, y F26 no tendría nada que comparar. Rellenando el hueco de forma razonable, una límite viva sobrevive a las 15:00, puede llenarse dentro de una ventana de noticias que RN-028 quiere bloquear (sanción de FundedNext aunque cierre en ganancia, ADR-0022) y pasar la noche o el fin de semana (hueco del domingo) con la cuenta fondeada expuesta.
**Veredicto:** reproducir MATIZADO (grave) — confirma que ninguna de las 13 acciones coloca ni cancela y que `reentrar` es la única que coloca una orden. contexto CONFIRMADO/MATIZADO (grave) en las dos piezas fusionadas.

**[2] [d2-literal-a-01, d2-fidelidad-huecos-02] RN-005 invierte el lado: prohíbe justo donde el trader opera.**
**Hecho.** La cita de RN-005 (`ev-v3-001600-ed45b091`, v3 0:16:00) sale de un ejemplo con sesgo H4 BAJISTA («Vela bajista envuelve a la vela anterior... existe una alta probabilidad de que continúen», v3 0:15:08); ahí «por debajo de esta liquidez de m15 es ruido» (0:16:14) y «la operativa esta por encima» (0:17:30). Con sesgo ALCISTA el trader dice lo simétrico (v1 0:01:22-0:03:28: «buscamos operaciones alcistas por lo cual la operativa tiene que darse por aquí por debajo»). Es decir: alcista → opera por debajo; bajista → opera por encima. RN-005 y el predicado que la sostiene dicen lo contrario. **Dónde:** `knowledge/spec/strategy_spec.yaml:495` (RN-005 cuando), `110` (esta_al_otro_lado_de), `322-327` (hecho sesgo). **Cita:** «cuando: el precio se desarrolla por debajo de la liquidez de M15 en sesgo alcista, o al reves» / «esta_al_otro_lado_de: descripcion: el precio se desarrolla del lado contrario al sesgo».
Se reproduce:
```
$ botsito.exe corpus transcript show --video v3 --t0 0:14:40 --t1 0:18:15 --capa corregida
[0:15:11.760] Vela bajista envuelve a la vela anterior, por lo tanto, valida...
[0:16:14.210] o sea por debajo de esta liquidez de m15 es ruido [...]
[0:16:30.170] llegar a la entrada correcta se tiene que desarrollar por encima
[0:17:30.270] la operativa esta por encima no por debajo, todo lo que haya por debajo es ruido
```
**Con dinero:** hecho. Implementada tal cual, RN-005 es un gate que gana siempre y veta todos los montajes del trader en las dos direcciones: el bot no opera nunca, o solo opera el lado que el trader llama "ruido de mercado" — con 0,5 % por operación y hasta tres cartuchos por zona, hasta 1,5 % de pérdida por montajes que el trader descarta explícitamente.
**Veredicto:** reproducir CONFIRMADO/MATIZADO (grave), contexto CONFIRMADO (grave). Sin corrección: la inversión se sostiene tal cual la describe el auditor.

**[3] [d2-fidelidad-afirmaciones-01, d2-fidelidad-huecos-03] La caja no tiene ancla citable ni precio: nadie dice qué es el nivel 0 ni el nivel 1.**
**Hecho.** `stop_fraccion_caja`, `lotaje_base` y `base_calculo_objetivo` se miden los tres sobre "la caja", definida en el glosario como «la distancia entre la entrada y el extremo del stop inicial». Ese "stop inicial" no aparece en ningún otro fichero de knowledge/spec, docs ni src, y desde A-11/ADR-0020 no hay más stop que el 0,8 — que es, a su vez, una fracción de la caja: la definición es circular. El literal citado (`ev-v2-003336`) no describe la caja. Los tres ítems que sí describían sus extremos («desde el punto anterior», «hasta el final del rango», «desde aquí hasta aquí») se sustituyeron (supersede) el 2026-09-12 por ítems que solo corrigen 0,75→0,80, así que la parte geométrica dejó de ser citable como evidencia activa. Ninguna regla, predicado, token ni parámetro dice qué precio es el nivel 0 (dónde va la límite) ni el nivel 1 (el extremo). **Dónde:** `knowledge/spec/glossary.yaml:96-108`; `parametros.yaml:335, 559-561, 775-776`. **Cita:** «la distancia entre la entrada y el extremo del stop inicial, dividida en niveles»; «`distancia_completa` es la caja entera, del nivel 0 al nivel 1».
Se reproduce:
```
$ python s2/refs2.py && python s2/matriz.py
| ev-v4-010605-a11249c0 | 1:06:05 | "Siempre se toma en la mecha el limite" | citado en spec: NO |
| ev-v1-001454-69cebe62 | 0:14:54 | "desde el punto mas abajo... se puede definir el stop loss" | citado: NO |
| ev-v4-000813-c916eac6 | 0:08:13 | nivel 0 = punto de entrada 1,19502 | citado: NO |
```
**Con dinero:** hecho/inferencia. Con la única caja documentada con precios (nivel 0 = 1,19502, nivel 0,75 = 1,19537): caja = 4,667 pips, stop = 3,733 pips, lote para 0,5 % de 100 000 = 13,39 lotes. Un pip más lejos o más cerca en el nivel 1 mueve el lote un 18-27 % y el objetivo entre 11 y 17 pips: cada pip de geometría inventada por F21 es riesgo real distinto del que autorizó el trader.
**Veredicto:** reproducir MATIZADO (grave) en ambos — confirma el hueco pero añade matices: hay ancla citable para dónde va la límite (bloque de origen del breaker / zona de control, no un precio suelto) aunque no para el precio exacto dentro de esa estructura. contexto MATIZADO (grave).

**[4] [d2-fidelidad-huecos-04, d2-literal-b-04, d1-interprete-08] Nadie dice cuándo se congela la geometría de la orden; una entrada por *equal* nace sin objetivo.**
**Hecho.** Hay tres instantes candidatos y la spec usa los tres sin elegir: (1) *colocación* — RN-011 dimensiona el lote y escribe el stop en `se_coloca_orden_limite`, cuya descripción promete «con su lote, su stop y su objetivo»; (2) *reubicación* — RN-006 mueve la orden con `reubicar_orden_limite: {a, cadencia}`, sin lote/stop/objetivo, sin decir si recalcula; (3) *llenado* — RN-013 ejecuta `escribir_stop_en_la_orden` («antes de que se active») DENTRO del evento `se_activa_entrada` (contradicción interna), y RN-015 fija el objetivo también en `se_activa_entrada`, contra su propio título («se traza con la orden y no se mueve»). Además, RN-015 solo dispara con `se_activa_entrada: {por: cualquier_esquema}`; una activación por *equal* (RN-010, `{por: equal}`) no casa con ese token, así que ni RN-013 ni RN-015 disparan: la posición vive sin objetivo. La base `caja_completa` del objetivo descansa en ADR-0014, cuyas dos premisas ya están revocadas (A-11: el stop viaja en la orden; ADR-0020: el lote se dimensiona sobre 0,8, no sobre la caja completa). **Dónde:** `strategy_spec.yaml:221-223, 542` (RN-006), `233-235, 736-741` (RN-013), `664-677` (RN-011), `772-806` (RN-015); `docs/adr/0014-base-de-calculo-del-objetivo.md:12-14, 61-64`.
Se reproduce:
```
$ python s2/forma.py
RN-006 disparador cuando=['orden_limite_pendiente','se_completa_zona_de_control'] hace=['reubicar_orden_limite']
RN-011 disparador cuando=['se_coloca_orden_limite'] hace=['dimensionar_lote','escribir_stop_en_la_orden','fijar']
RN-013 disparador cuando=['se_activa_entrada'] hace=['escribir_stop_en_la_orden','fijar','fijar']
RN-015 disparador cuando=['se_activa_entrada'] hace=['fijar_objetivo']
```
En el intérprete de juguete, una activación por *equal* llena sin TP (`trazas_v5/s08a_equal_geometrico.txt`: `BROKER llena la limite 1.10000 lote=6.25 stop=1.0992 tp=None` / `disparan: disparador=[RN-010]`, sin RN-015).
**Con dinero:** hecho/inferencia. Si el motor sigue la forma, toda orden sale sin TP y se le añade al llenarse (un spike o hueco en el mismo minuto puede cruzar ese nivel antes de que exista); las entradas activadas por *equal* corren sin el 1:3 hasta el stop, el break even o las 15:00, con otra distribución de resultados que F26 no podría atribuir a ninguna regla. La base del objetivo cambia la distancia al TP un 25 % (3,0 cajas frente a 2,4).
**Veredicto:** reproducir MATIZADO (grave) en las tres piezas. contexto MATIZADO (grave): distingue que el instante SÍ está decidido en prosa/ADR para stop y objetivo (colocación), y que el defecto es que las FORMAS ejecutables lo contradicen.

**[5] [d2-fidelidad-huecos-05] La liquidez de M15 sigue sin definición ejecutable.**
**Hecho.** Ya declarado en `AUDITORIA-2026-09-12-material.md §2.3` y en `F14b-ciclo-de-vida-de-los-hechos.md §1.2` (propuesta, no aplicada). De 56 ítems que mencionan la liquidez, ninguno de los que describen su nivel está citado en spec, glosario, parámetros o ambigüedades, y se contradicen entre sí: «la zona de liquidez tiene que ser la más reciente» frente a «el alto más alto... sería la liquidez» en un pullback complejo, frente a «todo lo que hay es liquidez». Las tres ambigüedades que F14b pide abrir (A-24, A-25, A-26) no existen: `ambiguedades.yaml` acaba en A-23. **Dónde:** `strategy_spec.yaml:290-291` (token liquidez_m15), `470-491` (RN-004); `ambiguedades.yaml:399` (última, A-23). **Cita:** «liquidez_m15: descripcion: la liquidez marcada en M15 que hay que tomar antes de mirar M1».
Se reproduce:
```
$ grep -n 'id: A-2[4-9]' knowledge/spec/ambiguedades.yaml ; echo exit=$?
exit=1
$ botsito.exe spec status
Ambiguedades abiertas sin parametro asociado: A-16, A-21    # ninguna de liquidez
```
**Con dinero:** hecho. Elegir "el pivote más reciente" o "el más extremo" son niveles distintos a varios pips; decide si `liquidez_tomada` se enciende y con ella si hay operación. Sin regla de re-marcado a las 11:00, el bot puede buscar ventas con una liquidez marcada para compras — operaciones de 0,5 % que no son las del trader.
**Veredicto:** reproducir MATIZADO (grave), contexto CONFIRMADO (grave).

**[6] [d2-fidelidad-huecos-06] El breaker de M1 no es computable.**
**Hecho.** Tres piezas sin definir: (1) qué rompe — el mapeo de pivotes en M1 vive en 10 ítems del corpus, 9 sin citar en ningún sitio; (2) qué es el "bloque de origen" — el formulario lo preguntó explícitamente y la respuesta fue sobre BOS-contra-CHoCH, no sobre velas; (3) con qué criterio — "mecha o cuerpo" está horneado en la descripción del predicado (justo lo que la cabecera de la spec prohíbe), y el trader CONFIRMÓ por escrito en la sesión 1 un ítem que dice lo contrario de lo que él mismo dice en la grabación citada (una rotura con mecha "no valida el trade", pero en el contexto que RN-007 cita el trader también dice que en M1 «es válido con mecha o con cuerpo»). **Dónde:** `strategy_spec.yaml:42-45` (doctrina de argumentos), `121-134` (se_da_esquema), `547-561` (RN-007); `glossary.yaml:24-33` (breaker). **Cita:** «Los dos marcan el bloque de origen con el breaker (BOS); el CHoCH no se usa. En M1 la ruptura vale con mecha o con cuerpo».
Se reproduce:
```
$ botsito.exe corpus transcript show --video v4 --t0 0:58:50 --t1 1:00:30
[0:59:20.304] Pues es valido con mecha o con cuerpo
[0:59:55.014] De liquidez en M15
```
**Con dinero:** hecho/inferencia. El breaker decide qué vela dispara la entrada. Entre "toca con mecha" y "cierra con cuerpo" la entrada cambia de vela y de precio; sobre 48-60 operaciones al mes a 0,5 % cada una, un criterio distinto del trader es otra estrategia con su nombre. Sin pivotes definidos, dos implementaciones razonables de F18 marcan breakers distintos sobre las mismas velas.
**Veredicto:** reproducir MATIZADO (grave), contexto CONFIRMADO (grave).

**[7] [d5-relojes-datos-01, d2-fidelidad-afirmaciones-04, d5-relojes-datos-02, d1-interprete-09(b)] RN-003 admite tres lecturas de qué vela H4 fija el sesgo, y la ruptura por los dos lados no está resuelta.**
**Hecho.** El token `vela_h4_previa` («cerrada inmediatamente anterior al anclaje») y `extremo_de_la_h4_anterior` («el máximo o el mínimo de la vela H4 PREVIA», su propio sujeto) se refieren de forma literal a la misma vela; leído al pie de la letra esa vela nunca supera su propio extremo. Con la lectura de la prosa (I1: última H4 cerrada al abrir sesión contra la anterior) y la lectura del token con `anclaje_h4=17:00 America/New_York` (I2), en 31 de 42 mañanas medidas las dos lecturas dan sesgos distintos. Y con criterio `mecha`, una H4 que rompe a la vez el máximo y el mínimo de la anterior deja `sentido_de_la_ruptura` sin definir: pasa en 15 de 88 sesiones medidas de enero y julio (17 %), y en el intérprete de juguete el sesgo resultante depende del orden en que se evalúan las dos rupturas (misma entrada, orden distinto → sesgo distinto). La única salida que el trader ofrecía para el caso envolvente, tomar el color de la vela, la descartó él mismo en la sesión 1. **Dónde:** `strategy_spec.yaml:280-289` (tokens), `440-465` (RN-003 forma).
Se reproduce:
```
$ python scripts/h4_sesgo.py   # enero y julio 2026, anclaje 17:00 America/New_York
== 2026-07-15
I1 rompe_arriba=True (h 114422 vs 114341) rompe_abajo=False
I2 rompe_arriba=False rompe_abajo=True                       # sesgo opuesto a I1
velas envolventes (rompe arriba Y abajo) con I1: 15 de 88 sesiones
```
```
trazas_v5/s07b_envolvente.txt: RN-003 fijar sesgo: None -> bajista
trazas_v5/s07c (mismas señales, otro orden): RN-003 fijar sesgo: None -> alcista
```
**Con dinero:** hecho. El 2026-07-15, con I1 el bot busca compras y con I2 ventas: cada operación en el sentido equivocado arriesga el 0,5 % completo, y el tope diario de 4,5 % admite nueve seguidas. F26 mediría como "infidelidad" una elección de implementación que nadie ha tomado.
**Veredicto:** reproducir MATIZADO (grave) en las cuatro piezas. contexto MATIZADO (grave): corrige que son dos lecturas incompatibles, no tres (la I3 autorreferencial es un defecto de redacción del diccionario, no una interpretación operable), y que A-1 (RESUELTA) fijó el criterio color/mecha pero no el ancla temporal.

**[8] [d2-fidelidad-afirmaciones-03, d1-interprete-09(a)] El sesgo no tiene valor inicial: sin ruptura previa, nada filtra la dirección de la entrada.**
**Hecho.** El hecho `sesgo` solo lo fija RN-003 con una ruptura; no declara valor antes de la primera ruptura, ni si se reinicia por sesión o por día. El único lugar donde el sesgo condiciona algo es RN-005, que exige el hecho ya fijado; `se_da_esquema` no lleva sentido, y ninguna otra regla lo mira. Con el sesgo sin fijar (arranque en frío, o un día con H4 interior desde el origen), ninguna regla impide entrar hacia cualquier lado. **Dónde:** `strategy_spec.yaml:321-327` (hecho sesgo), `502-509` (RN-005). **Cita:** «sesgo: descripcion: el sentido en el que se busca entrada / produce: [RN-003] / consume: [RN-005]».
Se reproduce:
```
trazas_v5/s07a_interior_sin_sesgo.txt
[08:05] esta_al_otro_lado_de{sentido: alcista} -> disparan: gate=[RN-008]     # RN-005 NO dispara
[08:10] H-01 colocacion implicita: se envia orden limite compra
ESTADO FINAL: hechos sin sesgo
```
**Con dinero:** hecho. En el primer día del bot, o tras cualquier reinicio en el que el motor no reconstruya el sesgo, el filtro direccional queda apagado: el bot puede tomar entradas contra el sesgo H4 que el trader nunca tomaría, a 0,5 % cada una.
**Veredicto:** reproducir MATIZADO (media), contexto MATIZADO (media): matiza que ninguna forma ejecutable liga el SENTIDO de la operación al sesgo en ningún caso (ni con él fijado): RN-005 filtra por posición del precio respecto a la liquidez, no por el sentido de la orden.

**[9] [d5-relojes-datos-03, d1-interprete-09(c)] `abre_sesion_operativa` no tiene reloj: la sesión de las 11:00 no existe en el registro ni en la spec.**
**Hecho.** RN-003 se dispara "al abrir una sesión", pero el registro solo tiene `ventana_inicio` 07:00 y `ventana_fin` 15:00. Que haya dos sesiones y que la segunda empiece a las 11:00 solo está en `knowledge/cases/kit/config.yaml` (datos de etiquetado, no la spec) y en prosa de A-14/A-15. El contrato de literales (`test_no_business_literals.py:35`) además prohíbe escribir "11:00" en `src`. **Dónde:** `strategy_spec.yaml:62-63, 458`; `knowledge/cases/kit/config.yaml:14-20`. **Cita:** «abre_sesion_operativa: descripcion: empieza una de las sesiones de la ventana» / kit `sesiones: - nombre: '07-11' ... - nombre: '11-15' desde: '11:00'».
Se reproduce:
```
$ grep -rnE '11:00|11-15|07-11' knowledge/spec/*.yaml
knowledge/spec/ambiguedades.yaml:244:  ¿el bot busca solo en las dos sesiones de 07-11 y 11-15...?
# simulación con sesgo acumulado por lectura I1: mes 1, sesiones 11:00=21; sesgo distinto según se recalcule o no = 7
```
**Con dinero:** hecho. Cambia el sentido de operación en la segunda sesión en 14 de 44 casos medidos: la mitad de la ventana operativa se opera con un sesgo que F18 tendría que inventar o sacar de un fichero de etiquetado que no es la spec.
**Veredicto:** reproducir MATIZADO (media), contexto (sin voto adicional en la pieza matriz): confirma el hueco y añade que el brief de F11 prometía convertir esa frontera en parámetro.

**[10] [d2-literal-a-02, d2-literal-b-01] `equal` significa tres cosas distintas, y las reglas usan el sentido que no dijo el trader.**
**Hecho.** El token tiene tres definiciones incompatibles: un RESULTADO de cierre a cero (spec:302-303, «la operación cerró sin ganancia ni pérdida»), una GEOMETRÍA de precio (glosario, «dos extremos al mismo precio») y un EVENTO de activación sin ruptura (parámetro `reentrada_tras_equal`). Dos consecuencias distintas: **(a)** RN-010 lo usa como causa de activación (`se_activa_entrada: {por: equal}`), pero en la grabación que RN-010 cita el trader lo usa como NIVEL de precio, no como resultado — quien implemente `tokens` según su descripción no puede evaluar "activarse por un resultado de cierre". **(b)** RN-019/RN-016 lo usan como resultado de cierre a cero para decidir si una reentrada gasta cartucho; pero el trader, en la grabación que sostiene esa reentrada, describe el cierre como una SALIDA CON PÉRDIDA («te genera una pérdida», v6 1:23:19), no un cierre a cero. Con la forma vigente ese caso cierra como "pérdida": RN-019 no dispara y RN-016 gasta un cartucho, contra el literal de RN-016 («tampoco es considerado un intento»). **Dónde:** `strategy_spec.yaml:302-303` (token equal), `617, 627` (RN-010), `822-892` (RN-016/RN-019); `glossary.yaml:74-78`; `parametros.yaml:483-488`.
Se reproduce:
```
$ grep -n "equal" knowledge/spec/strategy_spec.yaml
302:  equal:
303:    descripcion: la operacion cerro sin ganancia ni perdida
617:    cuando: la orden se activa por un equal y la estructura no llega a romperse
627:          - se_activa_entrada: {por: equal}
886:          - se_cierra_operacion: {resultado: equal}
```
```
$ botsito.exe corpus transcript show --video v6 --t0 1:22:40 --t1 1:25:10 --capa cruda
[1:23:19.690] o sea, te genera una pérdida
[1:23:53.250] nos genera una pérdida nuevamente actualizamos... al mismo nivel
```
**Con dinero:** hecho/inferencia. Con `cartuchos_max=3` por zona, cada *equal* perdedor gasta un cartucho que el trader no gasta: el bot entra antes en `detenido_por_cartuchos` y pierde justo las reentradas que el trader sí hace. Si el motor llamase *equal* al cierre a cero, reentraría tras cada break even, cosa que el trader no describió.
**Veredicto:** reproducir MATIZADO (media/grave) en ambas piezas; contexto CONFIRMADO/MATIZADO (grave). Corrección de contexto: el hallazgo se sostiene en su tesis principal; corrige solo un detalle secundario sobre si `vuelve_a_dar_el_esquema` tiene cita propia.

**[11] [d2-literal-b-02] El break even, que el trader excluye del contador de cartuchos, no existe como resultado y la forma lo contaría como pérdida.**
**Hecho.** Ante «¿una salida en break even gasta intento?» el trader responde que no. La spec solo tiene tres resultados (`equal, ganancia, perdida`); RN-014 lleva el stop exactamente a `OP.precio_entrada`, sin colchón, y no hay parámetro de comisión ni de colchón. Una salida por un stop en el precio de entrada, con deslizamiento o comisión, cierra en negativo: el token la clasifica como "cerró en negativo" y RN-016 sumaría un cartucho, contra su propio literal («un intento no es considerado un break even»). **Dónde:** `strategy_spec.yaml:302-307` (tokens de resultado), `767` (RN-014), `825` (RN-016). **Cita:** «perdida: descripcion: la operacion cerro en negativo».
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 0:51:10 --t1 0:53:40 --capa cruda
[0:51:29.695] Una salida en break even, gasta intento
[0:52:44.335] un intento no es considerado un break even
$ grep -n -i "comision|commission|swap" knowledge/spec/parametros.yaml    # sin salida
```
**Con dinero:** hecho/inferencia. Dos break even y una pérdida bastan para detener la zona (cartuchos), mientras el trader seguiría operando: el bot opera menos que el trader y pierde justo los setups en los que el trader vuelve a entrar, en una operativa donde RN-014 pone el break even con frecuencia (al romperse la zona de control posterior).
**Veredicto:** reproducir MATIZADO (media), contexto CONFIRMADO (grave).

**[12] [d2-literal-b-03] El tope semanal del 9 % sobre saldo actual, con reinicio semanal, no lo dijo el trader así.**
**Hecho.** RN-020 aplica `perdida_maxima_semanal=9` sobre `base_calculo_perdida_semanal=saldo_actual`, reiniciado cada semana. La única fuente es una síntesis escrita a mano del consultor durante la sesión (`fb-...-cf913a64`, «9% de la cuenta actual»); en la grabación, tras «Tope de pérdida de la semana», el tramo relevante va marcado `<no_habla>` y lo único legible ata el 9 % al LÍMITE de la cuenta: «El 10% se quedó en la cuenta... Vamos a ponerle 9%». No hay ni un "reinicio semanal" ni "cuenta actual" en lo audible. **Dónde:** `knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-cf913a64.yaml`; `parametros.yaml:642-653, 735-745`.
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 2:04:50 --t1 2:06:00 --capa cruda
[2:05:08.687] 10, que es el límite de la cuenta, o 9
[2:05:49.427] El 10% se quedó en la cuenta.
[2:05:55.427] Vamos a ponerle 9% para ese momento
```
**Con dinero:** hecho/inferencia. Un tope que se reinicia cada semana sobre el saldo actual no protege un límite TOTAL de la cuenta: con 4,5 % diario se puede perder 9 % en dos días, reiniciar la semana y seguir; tres semanas malas seguidas superan el 10 % acumulado sin tocar nunca el tope semanal, y eso es perder la cuenta fondeada.
**Veredicto:** reproducir MATIZADO (media), contexto CONFIRMADO (grave).

**[13] [d2-literal-b-05] RN-018 prohíbe entradas en paralelo, pero la forma solo cuenta posiciones y no impide una segunda orden pendiente.**
**Hecho.** El trader respondió "no" a si pueden darse dos entradas a la vez. La forma solo prohíbe `abrir_operacion` cuando las POSICIONES vivas alcanzan `operaciones_simultaneas_max`; con una límite pendiente y 0 posiciones el gate no dispara, y `orden_limite_pendiente` solo lo consume RN-006 para reubicar: nada impide colocar una segunda pendiente. Si hay dos, el broker las llena sin volver a pasar por el gate. **Dónde:** `strategy_spec.yaml:69-75` (operaciones_abiertas_alcanzan), `316-317, 328-331` (hechos), `855-874` (RN-018).
Se reproduce:
```
$ botsito.exe corpus transcript show --video v4 --t0 0:36:20 --t1 0:37:40 --capa cruda
[0:37:10.876] ya la respuesta es no
$ python scripts/usos.py
hechos orden_limite_pendiente: {'produce': ['RN-011','RN-013'], 'consume': ['RN-006']}   # RN-018 no la consume
```
**Con dinero:** hecho/inferencia. Dos posiciones de 0,5 % en paralelo sobre el mismo movimiento: 1 % de riesgo correlado donde el trader arriesga 0,5 %, y dos cartuchos gastados a la vez — acelera la llegada al tope diario del 4,5 %.
**Veredicto:** reproducir MATIZADO (media). Sin voto de contexto en esta pieza.

**[14] [d2-fidelidad-huecos-08] La zona de control no tiene frontera, y "limpia" (A-21) sigue sin criterio pese a darse por resuelta.**
**Hecho.** RN-009 cuenta zonas (tope 1) y RN-006/RN-014 necesitan "la zona", pero nada dice dónde empieza y acaba una zona ni qué es "el punto extremo anterior" que la completa. `OP.zona_de_entrada` (que RN-014 exige distinta de la anterior) no tiene escritor en ninguna acción, y en el primer esquema (definido "sin retroceso") no hay candidato para su valor. La salida que `AUDITORIA-2026-09-12 §6` propone para A-21 ("limpia = exactamente una zona de control") no la sostiene la frase de origen, que habla de la CALIDAD de una zona («que no haga mucho ruido... sea una zona limpia», v1 0:14:35), no de cuántas hay — ese conteo ya lo hace RN-009. **Dónde:** `glossary.yaml:35-63`; `strategy_spec.yaml:135-143, 271-272, 590-613, 763`; `ambiguedades.yaml:358-378` (A-21).
Se reproduce:
```
$ botsito.exe corpus transcript show --video v1 --t0 0:14:20 --t1 0:15:10 --capa cruda
[0:14:35.638] cuando se desarrolle esta zona de control... sea una zona limpia
$ sed -n 248p docs/validation/AUDITORIA-2026-09-12-material.md
| A-21 (zona limpia) | El corpus la operacionaliza: limpia = exactamente una zona de control...
```
**Con dinero:** hecho/inferencia. Si F20 corta las zonas distinto que el trader, RN-009 descarta montajes válidos o acepta los de dos zonas, y RN-006 reubica la orden a otro precio: cambian las operaciones, no solo su resultado.
**Veredicto:** reproducir MATIZADO (media), contexto MATIZADO (media): añade que ni pivote, retroceso, bloque de origen ni "decisional" están definidos, y que no está declarado como deuda en ningún ADR/brief.

**[15] [d2-fidelidad-huecos-09] Lo que el trader exige tras cerrar una operación no llega a ninguna regla, y RN-017 dice lo contrario tras una ganadora.**
**Hecho.** Tras una GANADORA el trader espera liquidez nueva de M15 antes de volver a operar (`ev-v6-003227-c4efcf49`); RN-017 permite buscar entradas de inmediato "con el límite de cartuchos intacto". Tras un STOP con cartuchos vivos, el trader exige que la zona de control se cierre y se forme otra FUERA de la anterior (`ev-v4-003820-299d7a15`); ninguna regla lo pide, y RN-006 volvería a colocar en la misma estructura. Es deuda declarada en `AUDITORIA-2026-09-12 §2.1` y en `F14b §3` (propuesta no aplicada). **Dónde:** `strategy_spec.yaml:835-853` (RN-017), `809-833` (RN-016).
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 0:32:20 --t1 0:32:35 --capa cruda
[0:32:27.6] ya aqui esta el trade ganador... pues tenemos que esperar nuevamente a que se desarrolle la liquidez
$ grep -rn 'ev-v4-003820|ev-v6-003227' knowledge/spec docs/plan docs/adr    # sin resultados en spec
```
**Con dinero:** hecho. Tras un stop, reentrar en la misma zona gasta los tres cartuchos en una estructura que el trader ya da por agotada (hasta 1,5 % de pérdida por liquidez en vez de 0,5 %). Tras una ganadora, seguir sobre la misma liquidez añade operaciones que el trader no toma.
**Veredicto:** reproducir/contexto MATIZADO (media): el hueco es real y declarado, pero RN-017 no contradice literalmente al trader ("se sigue operando" es cierto); el defecto es la regla que falta, no RN-017.

**[16] [d2-literal-a-03] RN-007: su literal solo renombra un término; el criterio real que dio el trader no está citado.**
**Hecho.** La pregunta P-09 era "¿cuándo dos velas cuentan como una estructura?"; la respuesta grabada es una corrección de TERMINOLOGÍA («Creo que no sería el término adecuado... sería considerado una estructura»), no un criterio. El valor `order_block_mayor` es la etiqueta que escribió el consultor en la hoja, y "el resto se trata como ruido" viene de un ítem que RN-007 no cita. El criterio operativo que el trader sí da en esa misma respuesta (vela contraria, o que la siguiente vela retroceda hasta cierto nivel) no está en ninguna parte de la spec. **Dónde:** `strategy_spec.yaml:547-552` (RN-007); `knowledge/cases/kit/2026-09-09-sesion-01/hoja_trader.md:74-80`.
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 1:38:30 --t1 1:41:20 --capa cruda
[1:38:48.617] Creo que no sería el término adecuado
[1:38:57.957] O sea, en el lenguaje del bot / sería considerado una estructura
[1:39:40.077] lo ideal sería que para considerar estructura... sería esta vela bajista
```
**Con dinero:** hecho/inferencia. El mapeo de M1 decide dónde se coloca y se reubica la orden límite: si el motor agrupa velas con un "order block mayor" que nadie ha definido en marco ni en tamaño, cada entrada sale en otro sitio y el stop y el lote cambian con ella.
**Veredicto:** reproducir MATIZADO (media): confirma que el literal solo corrige el término, pero matiza que ambos conceptos (`order_block_mayor`, "resto es ruido") sí tienen soporte en el trader, solo que RN-007 no los cita.

**[17] [d2-literal-a-04] RN-006 reubica en cada zona completada y RN-009 descarta con dos: ninguna dice cuándo empieza y acaba la cuenta.**
**Inferencia**, de dos hechos: el trader describe reubicaciones SUCESIVAS («vamos ahí bajando el límite bajando el límite», y el consultor resume «se actualiza cada nueva estructura», confirmado); y RN-009 descarta "dentro del mismo esquema" sin ligar el conteo a ningún esquema ni declarar su reinicio (a diferencia de los acumuladores, que sí llevan `reinicia_con`). Leídas juntas, la segunda reubicación de RN-006 podría ser la segunda zona que invalida RN-009, o el conteo de RN-009 podría ser de otra cosa — ninguna nota ni ambigüedad lo dice. **Dónde:** `strategy_spec.yaml:514-518, 537-542` (RN-006), `592-598, 609` (RN-009), `135-139` (zonas_desarrolladas_superan).
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 1:28:50 --t1 1:30:00 --capa cruda
[1:29:48.220] Y lo que entiendo por esto es que se actualiza cada nueva estructura, ¿cierto? Claro
```
**Con dinero:** inferencia. Con un contador sin alcance, el motor o bien descarta setups que el trader opera tras varias reubicaciones, o bien sigue reubicando y llena una orden que RN-009 debía haber descartado: en los dos casos cambia el número de operaciones respecto al trader.
**Veredicto:** reproducir CONFIRMADO (media). Sin voto de contexto en esta pieza.

**[18] [d2-literal-a-06] RN-004 no dice en qué marco (M1 o M15) cierra la vela "con cuerpo".**
**Inferencia.** Ni la regla, ni el parámetro (`liquidez_m15_criterio_toma`), ni el glosario dicen si la vela que cierra es la de M15 o la de M1; la cita solo dice "la vela" y "con cuerpo". El corpus apunta a los dos marcos en distintos pasajes («solo en m15 si esperamos a rompimiento tiene que ser con cuerpo» frente a un ejemplo enseñado sobre un gráfico de M1). **Dónde:** `strategy_spec.yaml:473-481` (RN-004); `parametros.yaml` `liquidez_m15_criterio_toma`.
Se reproduce:
```
$ botsito.exe corpus transcript show --video v6 --t0 1:49:20 --t1 1:49:44 --capa cruda
[1:49:33.240] Vas a ver lo que la vela se hace con el cuerpo
[1:49:37.180] Vas a con la mecha, lo perfore
```
**Con dinero:** inferencia. Esperar el cierre de M15 o el de M1 separa la toma de liquidez hasta 14 minutos y cambia qué tomas cuentan: con M1 el bot da por tomada liquidez que con M15 sería una mecha, y abre entradas que el trader no toma.
**Veredicto:** reproducir MATIZADO (menor), contexto MATIZADO (media): el corpus orienta hacia la vela de M15 sin zanjarlo del todo.

**[19] [d5-relojes-datos-05] La ventana del caso (00:00 Madrid) corta la H4 anterior de la sesión de las 07:00.**
**Hecho.** La H4 contra la que RN-003 compara la vela previa de la sesión de las 07:00 empieza a las 23:00 Madrid de la víspera (una hora antes del caso, dos en días de desajuste DST). `construir_caso` publica ese límite en `limites_h4`, pero su hash y su `n_velas` solo cubren `[desde, hasta)`: el caso declara una vela cuyas M1 no contiene entera. **Dónde:** `knowledge/cases/kit/config.yaml:7-11`; `src/botsito/cases/ventanas.py:97-139`.
Se reproduce:
```
$ python ventanas_debug.py    # 2026-07-15, ventana 00:00-15:00 Madrid
caso desde 2026-07-14T22:00Z ; limites_h4 incluye 2026-07-14T21:00Z (FUERA del caso)
maxima/minima vela completa: 114341 114156 ; solo con M1 del caso: 114341 114173
```
**Con dinero:** hecho/inferencia. El 2026-07-16 la vela completa no da ruptura y la truncada da sesgo bajista: un motor validado caso a caso (F14/F26) y otro en vivo con historia completa operarían en sentidos distintos esa mañana, y la divergencia se leería como infidelidad del bot cuando es un artefacto de la ventana del caso.
**Veredicto:** reproducir MATIZADO (media). Sin voto de contexto en esta pieza.

**[20] [d5-relojes-datos-06] El stop al 0,8 no cae en puntos enteros, y la regla de redondeo solo existe en el plan (no en la spec).**
**Hecho.** `stop_fraccion_caja` es `Fraccion('0.8')`; la distancia en puntos sale entera solo cuando la caja es múltiplo de 5. La spec tiene RN-027 para redondear el LOTE a la baja, y nada para el nivel del STOP. El plan promete "lado conservador" sin decir cuál lado es, y ni el valor del punto ni la divisa de la cuenta están declarados fuera de `saldo_inicial_cuenta` (USD). **Dónde:** `src/botsito/domain/valores.py:16-18, 34-63`; `docs/plan/MASTER_PLAN.md:247`.
Se reproduce:
```
>>> f.valor * 137          # caja de 137 puntos
Decimal('109.6')           # no es un punto entero
```
**Con dinero:** hecho. Sobre una caja de 137 puntos el stop cae a 109 o a 110 puntos y el lote pasa de 4,58 a 4,54. Sin regla escrita, Python (F18/F21) y MQL5 (F28/F29) pueden redondear distinto: la discrepancia que la doble implementación (H.2) quería evitar.
**Veredicto:** reproducir MATIZADO (media): la regla que falta está asignada a F18 y el valor del punto a F21 (deuda declarada), pero "lado conservador" no dice qué lado ni en qué orden se redondean stop y lote, y eso no está declarado.

### B. Lo que el intérprete de juguete demuestra en ejecución

**[21] [d1-interprete-01] Agotar los cartuchos (o tocar el tope) deja el bot sin salida para siempre, y un test lo exige así.**
**Hecho.** RN-016/RN-020 fijan `detenido_por_cartuchos`/`detenido_por_tope` con tokens durativos (`hasta_cartuchos_reinicio`, `hasta_el_corte_siguiente`) que ningún predicado del vocabulario resuelve: nada representa "la siguiente liquidez de M15". La exploración del grafo cerrado del intérprete encuentra 5 estados absorbentes, los 5 con `detenido_por_cartuchos` fijo. `test_spec.py:813-821` exige que el freno persista (autoconsumo deliberado), no que sea permanente, pero la spec no ofrece cómo calcular la expiración. **Dónde:** `strategy_spec.yaml:821-831` (RN-016), `924-933` (RN-020); `tests/unit/test_spec.py:815-821`.
Se reproduce:
```
$ PROF=40 MAXEST=6000 python escenarios.py
s04 #11: toca el stop -> RN-016 fijar detenido_por_cartuchos: None -> hasta_cartuchos_reinicio
s04 #13, #16, #19 (días distintos): la misma línea. 5 de 39 estados absorbentes, los 5 con el freno fijo.
```
**Con dinero:** hecho/inferencia. Tres stops seguidos (1,5 % de la cuenta, normal en una semana) apagan el bot de forma permanente en la cuenta fondeada: sin pérdida adicional, pero sin volver a operar sin intervención manual — que la spec tampoco dice cómo hacer.
**Veredicto:** reproducir/contexto MATIZADO (media): declarado ya en F14b y en 3.1.4; lo nuevo es que la otra salida (que el motor interprete la duración) tampoco se puede ejecutar hoy, porque `cartuchos_reinicio=siguiente_liquidez_m15` no tiene predicado.

**[22] [d1-interprete-02] Los hechos que copian el estado del broker se desincronizan y resucitan un conflicto que un ADR daba por cerrado.**
**Hecho.** `orden_limite_pendiente` y `operacion_abierta` los fijan reglas, no el broker, y no son mutuamente excluyentes en todas las rutas: RN-010 (activación por *equal*) enciende `operacion_abierta` y NO apaga `orden_limite_pendiente`. Con los dos hechos en "sí" y una posición viva, al completarse la siguiente zona RN-006 (reubicar) y RN-014 (break even) disparan en el mismo evento, ambas "disparador" y sin `complementa` — exactamente el conflicto que `ADR-0018:32-37` corrigió con la precondición de RN-006 para el caso normal. **Dónde:** `strategy_spec.yaml:624-631` (RN-010), `533-542` (RN-006), `756-767` (RN-014).
Se reproduce:
```
trazas_v5/s08a_equal_geometrico.txt
#4: BROKER llena la limite ... / RN-010 fijar operacion_abierta: None -> si   (orden_limite_pendiente sigue 'si')
#5: RN-006 reubicar_orden_limite a Z2: NO hay orden en el broker (hecho viejo)
    RN-014 break even: stop -> 1.10000
    EMPATE sin desempate: RN-006 y RN-014 clase=disparador conflicto=True
```
**Con dinero:** hecho/inferencia. Un motor que implemente la forma tal cual reubica una límite con una operación ya abierta (segunda exposición que RN-018 prohíbe) o, si la plataforma ignora la orden fantasma, el orden en que se resuelva el empate decide si se pone el break even — comportamiento que depende del fichero, no de una regla.
**Veredicto:** reproducir/contexto MATIZADO (media): matiza que la vía es concretamente "activación por *equal*, primer día", y que su alcance depende de una lectura de `por: equal` frente a `por: cualquier_esquema` que la spec no decide.

**[23] [d1-interprete-03] El acumulador del tope diario se alimenta con el riesgo nominal y solo cuando salta el stop: mide una cifra que no es la pérdida.**
**Hecho.** Ningún acumulador declara QUÉ lo alimenta (solo base y reinicio); la única acción que toca `perdida_dia` es `realizar_perdida` (RN-012), con el riesgo NOMINAL, y solo con `salta_stop`. Consecuencias ejecutadas: (a) un break even con costes reales cuenta como "pérdida" nominal completa y gasta un cartucho, contra el glosario («ni el break even... cuentan como uno»); (b) un cierre forzoso de RN-002 en pérdida NO suma nada a `perdida_dia`; (c) un stop con desfase de deslizamiento pierde más de lo que se contabiliza. **Dónde:** `strategy_spec.yaml:684-688, 707-715` (RN-012), `362-377` (acumuladores).
Se reproduce:
```
trazas_v5/s08f_tres_be_con_coste.txt
BROKER cierra por stop: pnl=-7.00 -> resultado=perdida
RN-012 realizar_perdida NOMINAL 499.97 -> perdida_dia=499.97      # 500 nominal por 7 USD reales
...
RN-016 fijar detenido_por_cartuchos ; perdida_dia=1499.79 (1.5 %)  # bot detenido por 21 USD reales
trazas_v5/s02_dia_dos.txt: cierre_forzoso pnl=-445.20 -> ESTADO FINAL perdida_dia 0.0   # infracuenta
```
**Con dinero:** hecho. En las dos direcciones: el bot se detiene tras 21 USD de pérdida real creyendo que perdió 1,5 %, y el freno del 4,5 % no ve pérdidas reales por cierres forzosos, deslizamientos o huecos.
**Veredicto:** reproducir MATIZADO (grave), contexto MATIZADO (media): la spec no declara qué alimenta los acumuladores en absoluto (no solo el caso nominal/neto); es una decisión que un motor tiene que tomar sin guía escrita.

**[24] [d1-interprete-04] El tope diario del 4,5 % se sobrepasa por construcción: se comprueba antes de abrir y no descuenta el riesgo de la operación que se abre.**
**Hecho.** `alcanza_tope` es "el acumulador llega al tope"; mientras `perdida_dia < 4,5 %` no hay prohibición, y la operación que se abre con 4,49 % acumulado arriesga otro 0,5 % más. Además RN-020 (gate) se evalúa antes que RN-012 (disparador) en el mismo evento: el freno se fija en el evento SIGUIENTE al stop que lo alcanza. **Dónde:** `strategy_spec.yaml:924-933` (RN-020), `76-82` (alcanza_tope).
Se reproduce:
```
$ python escenarios.py    # 12 intentos perdedores/día, cartuchos desactivados para aislar el tope
l.381 RN-012 realizar_perdida NOMINAL 477.94 -> perdida_dia=4388.99 (4.389 %)
l.386 [#30] EVENTO: esquema 10 (se coloca la 10ª orden con 4,389 % ya acumulado)
l.422 RN-012 realizar_perdida NOMINAL 475.56 -> perdida_dia=4864.54 (4.865 %)   # peor caso 4,5%+riesgo
```
**Con dinero:** hecho. Hasta ~0,48-0,5 % de la cuenta por encima del tope declarado (365-480 USD sobre 100 000): si el límite real de FundedNext está en esa franja, la cuenta se pierde con un bot que cumple su propia spec.
**Veredicto:** reproducir/contexto MATIZADO (media): confirma el mecanismo y precisa la cota (~4,87-4,98 % nominal según se mida sobre saldo inicial o actual).

**[25] [d1-interprete-05] La precedencia por clase contradice el flujo de datos: los gates que leen lo que produce un disparador lo leen un evento tarde.**
**Inferencia**, de dos hechos: ADR-0018 ordena las clases para resolver CONFLICTOS, no fases dentro de un evento; y tres gates consumen salidas de disparadores del MISMO evento (RN-027 redondea `lote_calculado`, que produce RN-011). Evaluando por clase o por instantánea, RN-027 ve el lote un evento después de colocar: la orden sale con el lote sin redondear y el redondeo llega con la posición ya abierta. **Dónde:** `strategy_spec.yaml:19-32` (precedencia), `1071-1083` (RN-027), `664-677` (RN-011).
Se reproduce:
```
trazas_v5/s03_stop_y_reentrada.txt
#3: RN-011 dimensionar_lote: 500.00/(0.00078*contrato) = 6.443299   (RN-027 no dispara en ese evento)
#4: BROKER llena la limite lote=6.443299 / RN-027 redondear_lote 6.443299 -> 6.44 aplicado a: POSICION YA ABIERTA
```
**Con dinero:** hecho/inferencia. En MT5 un volumen que no es múltiplo del paso se rechaza (orden perdida); en un simulador permisivo entra con más lote del que toca, y la pérdida supera el 0,5 % (502,58 frente a 500 en la traza).
**Veredicto:** reproducir MATIZADO (menor), contexto MATIZADO (media): la spec no declara el orden de evaluación DENTRO de un evento en ningún sentido, y tampoco tiene una acción que "envíe la orden" para poder expresar "calcular, redondear y enviar" en la forma.

### C. Las guardias que deberían proteger la spec se pueden apagar sin que salte nada

**[26] [exec-checks-01] `problemas_de_spec` puede perder 7 de sus 8 comprobaciones y la suite sigue en verde.**
**Hecho.** `problemas_de_spec` es la única puerta por la que `make knowledge`, `botsito spec check` y el CI ejecutan las guardias semánticas; los tests unitarios llaman a cada `comprobar_*` por separado, y la puerta solo se prueba con la spec real limpia y con un registro vacío (que solo rompe `comprobar_contra`). Solo 5 tests ejecutan la puerta completa, los tres sobre la spec real (que no tiene problemas). **Dónde:** `src/botsito/validation/knowledge.py:143-202`; `tests/unit/test_spec.py:1046-1051` (único caso negativo).
Se reproduce:
```
# clon con 8 de las 9 llamadas de comprobación borradas de la puerta (solo queda comprobar_contra)
$ ruff check && mypy && lint-imports && pytest    # 663 casos, EXIT=0 en los 4
```
**Con dinero:** hecho/inferencia. Si `comprobar_forma` o el bucle de UNKNOWN se caen de la puerta, una regla VIGENTE sin forma ejecutable, o que ejecuta un parámetro UNKNOWN como `spread_maximo`, pasa `make check` en verde y operaría en la cuenta real con una regla que nadie validó.
**Veredicto:** reproducir MATIZADO (media): reprodujo con un mutante más agresivo (borrado real de 8 de 9 comprobaciones, no solo descarte de resultados) y confirmó el mismo resultado. contexto CONFIRMADO (grave): no hay ADR ni brief que declare a propósito la ausencia de una puerta de cobertura/mutación sobre `problemas_de_spec`.

**[27] [exec-checks-02] Las ramas que deciden si una regla es ejecutable funcionan, pero solo la spec real las ejercita.**
**Hecho.** `cov.json` marca 5 ramas de `comprobar_forma`/`knowledge.py` que solo saltan de verdad si alguien rompe la spec REAL (no hay ningún test unitario que las dispare de forma aislada): regla VIGENTE sin forma, `pendiente_definicion` sin formato A-N, `pendiente_definicion` sobre ambigüedad cerrada, hecho usado y no declarado, y parámetro UNKNOWN en regla vigente. **Dónde:** `src/botsito/spec/modelo.py:882-902, 1009-1013`; `src/botsito/validation/knowledge.py:164-168`.
Se reproduce:
```
$ botsito.exe spec check    # con RN-013 sin forma, en un clon editado
ERROR: RN-013: es VIGENTE y no tiene forma ejecutable; el motor no puede implementarla sin interpretar su prosa
EXIT=1
```
**Con dinero:** hecho/inferencia. Un cambio que invierta o anule cualquiera de esas condiciones no rompe ningún test: la siguiente regla escrita para el motor podría entrar sin forma, o con un valor UNKNOWN, y operarse en real.
**Veredicto:** reproducir CONFIRMADO (media): las ramas SÍ saltan hoy sobre la spec real; el defecto es que la única prueba de que el contrato sigue en pie es romper la spec real, no un test dedicado.

**[28] [exec-checks-03] `comprobar_precedencia`: tres de sus cuatro denuncias no las fija ningún test por separado.**
**Hecho.** Dos ramas (más de un fallback; parámetros subconjunto sin `complementa`) no se ejecutan en toda la suite; una tercera (mismo disparador sin `complementa`) sí se ejecuta, pero el único test que la alcanza también satisface el mensaje de la cuarta rama a la vez (mismos parámetros), así que apagar solo una de las dos deja todo en verde. **Dónde:** `src/botsito/spec/modelo.py:487-491, 508-512, 539-546`; `tests/unit/test_spec.py:454-456`.
Se reproduce:
```
$ cov.json: ML 488, ML 541 (nunca ejecutadas)
# mutante: modelo.py:508 'if not any(...)' -> 'if False:'
$ pytest tests/unit/  -> 231 passed, 1 failed (preexistente, no relacionado)
```
**Con dinero:** hecho/inferencia. Si la detección de disparador idéntico se apaga, dos reglas como RN-013 y RN-015 vuelven a competir y gana la que esté antes en el YAML (orden editorial): el motor podría colocar el stop o el objetivo de la regla equivocada.
**Veredicto:** reproducir MATIZADO (media): precisa que son exactamente dos de las cuatro ramas las que no se ejecutan nunca, y que las otras dos se ejecutan juntas sin que ningún test aísle cuál de las dos falla.

**[29] [d3-guardias-forma-01] `forma` no tiene esquema: una forma vacía, una rama renombrada o una rama extra pasan todas las puertas y cuentan como ejecutables.**
**Hecho.** Nada exige que `forma` tenga `cuando`/`entonces` ni prohíbe otras claves; `es_ejecutable` solo mira que sea un dict sin `pendiente_definicion`. Reproducido en un clon: RN-027 con `forma: {}` pasa `spec check`, `knowledge validate` y los 60 tests de spec, y `spec status` la cuenta como ejecutable. Una rama hermana con nombre de clave estructural (`resultado:`) con un predicado inexistente entra en el hash y en `reglas.md` sin que caiga nada. **Dónde:** `src/botsito/spec/modelo.py:881-887, 910-913, 861`.
Se reproduce:
```
# RN-027 forma: {} (vacía) en un clon, spec_version subida, manifiesto y docs regenerados
$ botsito.exe spec check
OK: 28 reglas de spec (25 vigentes, 24 con forma ejecutable)...    # RN-027 cuenta como ejecutable
```
**Con dinero:** hecho/inferencia. El motor de F22-F23 "implementa esta lista y ninguna otra": con RN-027 vaciada, el lote no se redondea a `instrumento_lote_paso`; MT5 rechaza el volumen (operación perdida) o el puente lo redondea a su manera y arriesga por encima de lo autorizado, con el hash sellado y `make check` en verde.
**Veredicto:** reproducir/contexto MATIZADO (media): con formas vacías, 12 de 24 reglas ejecutables pasan igual; con rama quitada o renombrada, 17 de 24; con rama extra de nombre estructural, las 24.

**[30] [d3-guardias-forma-02] `tokens` es una puerta sin esquema ni clase: cualquier número o palabra declarado como token entra como argumento válido.**
**Hecho.** `cargar_vocabulario` acepta cualquier mapa en `tokens`, y da por bueno cualquier valor que sea clave de ese mapa; "un token NO lleva número" es solo un comentario. Reproducido: declarar el token `"15"` y usarlo como `paso: "15"` en RN-027, o el token `"9,5"` como tope de RN-020, o `mecha` como criterio de RN-003, pasan `spec check`, `knowledge validate` y pytest con hash nuevo. **Dónde:** `src/botsito/spec/modelo.py:565-569, 825-831, 843`.
Se reproduce:
```
# T3b: token "9,5" + alcanza_tope:{acumulador: perdida_dia, tope: "9,5"} en RN-020
$ botsito.exe spec check ; knowledge validate ; pytest    # rc 0/0/0, hash 08b49831752f
```
**Con dinero:** hecho. Cambiar el tope diario (4,5 % = 4 500 USD) por un token deja de pasar por `parametros.yaml`, la única puerta declarada (ADR-0002) para vigilar la regla de FundedNext; congelar el criterio de ruptura del sesgo en `mecha` por esta vía cambia el sentido de la operación sin que el registro lo controle.
**Veredicto:** reproducir MATIZADO (media): confirma con ediciones deliberadas más subida de `spec_version` y regeneración de manifiesto/docs (no es un accidente trivial, pero tampoco está bloqueado). contexto CONFIRMADO (grave).

**[31] [d3-guardias-forma-03] Las claves estructurales aceptan cualquier nombre de cualquier clase, sin declararlo.**
**Hecho.** `conocidos` une parámetros, ligaduras, tokens, hechos y acumuladores sin distinguir clase, y la obligación de declarar en `parametros` lo que la forma usa se salta en las 13 claves estructurales. `que: stop_fraccion_caja` (parámetro numérico como sujeto), `que: ganancia` (token de resultado) o `paso: perdida_dia` (acumulador en clave de valor) pasan todas las guardias. **Dónde:** `src/botsito/spec/modelo.py:626-642, 825-831, 958-964`.
Se reproduce:
```
# E3: no_es_multiplo_de:{que: ganancia, paso: perdida_dia} en RN-027
$ spec check ; knowledge validate ; pytest    # rc 0/0/0, hash 53f078e8b22c
```
**Con dinero:** hecho/inferencia. La guardia de RN-027 quedaría evaluando si 0,8 es múltiplo de 0,01 en lugar del lote: nunca redondearía. El motor tendría que construir su propio sistema de tipos porque la spec no le da ninguno con el que rechazar valores incoherentes en tiempo de carga.
**Veredicto:** reproducir/contexto CONFIRMADO (grave).

**[32] [d3-guardias-forma-04] `comprobar_consumo` cuenta como lector la lista `parametros`, aunque la forma nunca lea el valor.**
**Hecho.** La guardia de forma solo comprueba una dirección (lo usado está declarado); la inversa no existe, y `comprobar_consumo` toma la mera declaración como lectura. En la spec real hay 8 parámetros CONFIRMED que su forma no usa (`anclaje_h4`, `sesgo_h4_regla`, `broker_dst`, `broker_offset_base`, `instrumento_digitos`), y ADR-0019 ya anunciaba que uno de ellos "se queda sin trabajo". **Dónde:** `src/botsito/spec/modelo.py:709, 723`.
Se reproduce:
```
$ python listar_no_usados.py
RN-003 declara y su forma NO usa: ['anclaje_h4', 'sesgo_h4_regla']
RN-020 ... ['broker_dst', 'broker_offset_base']
```
**Con dinero:** hecho/inferencia. Quien implemente RN-020 desde la forma no tiene por dónde saber que el corte del tope diario va en reloj de servidor con desfase 120 min y DST de EE. UU.; si corta a medianoche UTC, la ventana se desplaza 2-3 h y el bot puede seguir abriendo cuando FundedNext ya cuenta el día como perdido.
**Veredicto:** reproducir/contexto CONFIRMADO (grave): un "lector de mentira" (declarar un parámetro sin usarlo) pasa la guardia igual que uno real (reproducido con `latencia_ms`); ajusta la cifra a 8 parámetros, no 9.

**[33] [d3-guardias-forma-05] La guardia de hechos cuenta como "producido" cualquier `hecho:` en `entonces`, sin mirar `fijar.a`.**
**Hecho.** El comentario de la guardia promete detectar un hecho que nadie produce; "producir" es solo nombrar el hecho en la rama `entonces`. Cambiar en RN-011 `fijar: {a: "si"}` por `a: "no"` deja el hecho sin nadie que lo encienda y a RN-006 inalcanzable, con `spec check`, `knowledge validate` y pytest en verde. **Dónde:** `src/botsito/spec/modelo.py:993-996, 785-786`.
Se reproduce:
```
# H3: RN-011 fijar orden_limite_pendiente: "si" -> "no"
$ spec check ; knowledge validate ; pytest    # rc 0/0/0, hash e163c4deb0ff
```
**Con dinero:** hecho/inferencia. Con esta mutación la orden límite nunca se reubicaría al completarse cada zona: el bot dejaría la orden en una zona vieja. Para el motor significa que la validación de alcanzabilidad de hechos no sirve como red.
**Veredicto:** reproducir MATIZADO (media): confirma, y añade que la guardia también cuenta formas de reglas DESCARTADAS como productoras/consumidoras.

**[34] [d3-tests-contrato-01] El contrato de literales deja pasar 40 de los 52 valores del registro, justo los que el motor usa en aritmética y en ramas.**
**Hecho.** ADR-0002 promete un test que prohíba literales de negocio fuera de `config/`; el código solo prohíbe 10 números (6 de ellos ni siquiera están en el registro) y 10 patrones de texto. De 52 parámetros con valor, solo caza en forma canónica 11-12 (8-9 de los 37 de estrategia). Pasan sin ofensa: `cartuchos_max=3`, `operaciones_simultaneas_max=1`, el riesgo escrito como `Decimal("0.005")`, cualquier hora como `time(15,0)`, los 22 enums de estrategia, `'Europe/madrid'`. **Dónde:** `tests/contract/test_no_business_literals.py:18-45, 129-138`.
Se reproduce:
```
# 104 literales inyectados en un engine/__init__.py de prueba
$ pytest tests/contract/test_no_business_literals.py    # 1 failed (26 ofensas), 18 passed
E __init__.py:10 literal 0.8 (stop en la caja...)        # el resto (enums, horas, enteros con valor propio) no aparece
```
**Con dinero:** hecho. Un motor que escriba `if cartuchos_usados >= 3` o `riesgo = saldo * Decimal("0.005")` pasa `make check`. Cuando el trader cambie un valor (ya ocurrió con el stop 0,75→0,8), el bot en la cuenta fondeada puede seguir operando con el valor viejo sin que nada salga en rojo.
**Veredicto:** reproducir MATIZADO (media): el contrato filtra por FORMA, no por uso; de los 41 que no caza, 30 son enums/booleanos que ninguna lista de literales prohibidos puede vigilar sin prohibir también el despacho legítimo — el hueco real son los enteros y lotes con valor propio. contexto CONFIRMADO (grave).

**[35] [d3-tests-contrato-04, d4-registro-07] Ninguna guardia comprueba que la opción con la que el código compara un enum exista; un typo da `False` en silencio.**
**Hecho.** `Registro.opcion` devuelve `str`; el contrato AST valida el nombre y el tipo del parámetro, pero no el literal contra el que se compara el resultado. `registro.opcion("sesgo_h4_criterio_ruptura") == "mechas"` (con "s" de más) pasa todas las guardias y en ejecución es `False` en silencio; el comentario que dice que TEXTOS_PROHIBIDOS vigila los enums es falso (0 de 22 enums de estrategia están en esa lista). **Dónde:** `tests/contract/test_registro_accessors.py:48-58`; `src/botsito/config/registro.py:196-198`.
Se reproduce:
```
>>> registro.opcion("sesgo_h4_criterio_ruptura")
'mecha'
>>> registro.opcion("sesgo_h4_criterio_ruptura") == "mechas"     # typo
False                                                             # y ninguna guardia lo detecta
```
**Con dinero:** hecho/inferencia. Una comparación mal escrita siempre es falsa y el bot toma en silencio la otra rama: sesgo H4 por cuerpo en vez de por mecha, o un reinicio de cartuchos que nunca ocurre. Opera una estrategia distinta de la del trader sin que ninguna puerta salga en rojo; solo lo delataría F26, gastando holdout.
**Veredicto:** reproducir CONFIRMADO/MATIZADO (media) en ambas piezas: mismo defecto verificado desde el contrato de tests y desde `registro.py`.

**[36] [d3-tests-contrato-05] La exención `# no-negocio:` es autoservicio: eximir cinco caracteres de "motivo" basta para saltarse el contrato de literales.**
**Hecho.** Basta un comentario `# no-negocio: <5+ caracteres>` en la línea para eximir TODOS los nodos que empiezan en ella, sea cual sea el valor. Ningún test lista las exenciones ni comprueba que el valor eximido no coincida con un valor del registro; hoy hay 9 en `src/`, dos sobre números que sí están en `NUMEROS_PROHIBIDOS`. **Dónde:** `tests/contract/test_no_business_literals.py:111, 123-127`.
Se reproduce:
```
# S12 = 0.8  # no-negocio: cualquier motivo de cinco letras
$ pytest tests/contract/test_no_business_literals.py
# S12 NO aparece entre las 26 ofensas; S01 = 0.8 (sin comentario) sí aparece
```
**Con dinero:** hecho/inferencia. Durante F18-F24, quien choque con el contrato tiene una salida que ningún revisor automático mira: un `Decimal("0.8")` horneado con el visto bueno de `make check`.
**Veredicto:** reproducir MATIZADO (media): confirma el mecanismo tal cual, sin corrección de fondo.

**[37] [d4-registro-04] El contrato AST de accesores no escala al motor: ignora `self.registro`, `obtener()`, nombres en variable y el estado UNKNOWN.**
**Hecho.** El contrato solo registra llamadas cuyo receptor es un nombre simple (`registro`, `reg`, `parametros`) con un literal `str` como primer argumento. No ve `self.registro.x(...)`, `obtener()` (fuera de `ACCESORES`), un nombre pasado en variable, ni `registro.parametros['x'].valor` (que da `None` si es UNKNOWN sin avisar). Como `domain` no puede importar `config` (import-linter), las lecturas del motor vivirán en `engine/`, casi seguro en estilo de clase. **Dónde:** `tests/contract/test_registro_accessors.py:34-44`.
Se reproduce:
```
# engine/trampa_d4.py: self.registro.fraccion("no_existe_1"); registro.obtener("no_existe_2");
# nombre="stop_fraccion_caja"; registro.decimal(nombre); registro.fraccion("stop_reduccion_fraccion")  # UNKNOWN
$ pytest tests/contract/test_registro_accessors.py tests/contract/test_no_business_literals.py
# el fichero trampa pasa los dos contratos
```
**Con dinero:** inferencia, de dos hechos (el contrato solo ve el patrón simple; 40 lecturas en estilo de clase lo evitarían todas). Un typo, un tipo equivocado o la lectura de un UNKNOWN no fallan en `make check`; fallan en vivo la primera vez que se ejecuta esa rama (break even, reducción de stop, corte del día), con la orden ya colocada y su SL dentro.
**Veredicto:** reproducir MATIZADO (media): queda por debajo de la letra de ADR-0006, no está declarado como deuda. contexto CONFIRMADO (grave).

**[38] [d6-evidencia-01] Superseder un ítem de evidencia no revoca sus citas: parámetro, regla, predicado y glosario pueden seguir citando el item retirado.**
**Hecho.** Las dos guardias de "cita revocada" construyen el conjunto de revocados solo desde registros de FEEDBACK; el bucle de parámetros además salta toda fuente que no sea `feedback`. `comprobar_contra` y `comprobar_literales` validan contra TODOS los ítems, retirados incluidos. Hoy es latente (ningún supersedido está citado por la spec), pero 4 parámetros tienen fuente `evidence`, entre ellos `operaciones_simultaneas_max`. **Dónde:** `src/botsito/validation/knowledge.py:133, 141, 147, 565`.
Se reproduce:
```
$ botsito.exe evidence new ... --supersede ev-v4-003710-c753f3d3
OK: knowledge/evidence/v4/ev-v4-003710-f32c06e4.yaml
# knowledge validate sigue OK citando el item supersedido
```
**Con dinero:** hecho/inferencia. Si la evidencia que sostiene `operaciones_simultaneas_max=1` (lo que impide una segunda operación, RN-018) se corrige por supersede, el registro sigue diciendo 1 y ninguna puerta avisa; en la dirección contraria, el bot ejecutaría un valor que el trader ya corrigió.
**Veredicto:** reproducir MATIZADO (media), contexto CONFIRMADO (grave). No mueve la aguja del motor hoy (es latente), pero compromete la fiabilidad futura del registro que el motor consumirá.

### D. Decisiones de arquitectura y método pendientes antes de escribir el motor

**[39] [d8-camino-motor-01] El reloj de evaluación del motor (tick vs. cierre de vela) no está decidido en ningún ADR, y hay rastros contradictorios.**
**Hecho.** F23 solo promete "bucle, reloj determinista"; F24 resuelve stop y objetivo "en el mismo minuto por orden de ticks"; una versión congelada del plan (HTML, del 2026-09-03) dice "reubicación solo al cierre de M1", mientras el registro fija `reubicacion_cadencia=al_romper`; el dominio solo conoce `MinutoUtc`, y `MilisegundoUtc` (el tick) se aplaza a F22. Los predicados mezclan eventos de mercado y de orden sin orden declarado entre ellos. **Dónde:** `knowledge/spec/parametros.yaml:494-504`; `src/botsito/domain/velas.py:21`; `docs/plan/MASTER_PLAN.md:99, 258`.
Se reproduce:
```
$ grep -n 'nombre: reubicacion_cadencia' -A5 knowledge/spec/parametros.yaml
    valor: "al_romper"                    # fuente fb-2026-09-09-sesion-01-6b29059d
$ sed -n 496p docs/plan/MASTER_PLAN.html
... reubicación solo al cierre de M1 con banda muerta ...     # instantánea congelada 2026-09-03
```
**Con dinero:** hecho/inferencia. Si F18-F21 se escriben sobre velas M1 cerradas y el reloj acaba siendo el tick (o al revés), hay que reescribir detección de ruptura, break even y reubicación. Dentro de una misma vela que toque a la vez el break even y el stop, la resolución por vela no decide si la operación es -0,5 % o 0.
**Veredicto:** reproducir MATIZADO (grave): ningún ADR fija la granularidad, y el plan vivo (Markdown) ya apunta al tick para F22-F24, remitiendo A-4/A-13 ahí — pendiente real, no contradicción activa. contexto MATIZADO (media): corrige que la cita "contradictoria" del HTML es una instantánea declarada CONGELADA (el Markdown manda), pero confirma que la decisión de granularidad sigue sin ADR.

**[40] [d8-camino-motor-02] Las reglas de FundedNext (tope diario/total, lote máximo) no tienen parámetros en el registro ni fuente citada, y las cifras del plan contradicen la única evidencia.**
**Hecho.** ADR-0004 decide que la categoría `prop_firm` guarda pérdida diaria y total, lote máximo, mensajes y consistencia; el registro real tiene 5 `prop_firm` y ninguno es eso. `MASTER_PLAN.md:246` fija el veto en "5 % diario sobre equity, 10 % total" sin citar nada; la única fuente del repositorio dice «8 %... de memoria» del propio trader, y ningún ADR, regla o plan la cita. El freno que sí existe es el del TRADER: 4,5 % diario y 9 % semanal (findings [12], [23], [24]), sin tope total. **Dónde:** `knowledge/spec/parametros.yaml` categoría `prop_firm`; `docs/adr/0004-...md:12-13`; `docs/plan/MASTER_PLAN.md:246`.
Se reproduce:
```
$ python filtra_prop_firm.py
prop_firm reales: filtro_noticias, reloj_dia_riesgo, cuenta_objetivo, cuenta_pruebas, saldo_inicial_cuenta
$ grep -n -i 'veto|equity|kill' knowledge/spec/*.yaml    # sin salida
```
**Con dinero:** hecho. Con 100 000 USD y 0,5 % por pérdida, el tope semanal del TRADER (9 %) permite 18 pérdidas en una semana: -9 % ya supera el 8 % total que dice la única evidencia citable, y la cuenta se pierde antes de que ningún freno de la spec salte.
**Veredicto:** reproducir MATIZADO (media): confirma el hueco de parámetros y de fuente; contexto CONFIRMADO (grave).

**[41] [d8-camino-motor-03] Nadie ha decidido si el motor Python interpreta la `forma` en ejecución o la reescribe a mano, ni qué cruza a MQL5.**
**Inferencia**, de tres hechos: la spec dice que "el motor de F22-F23 implementa esta lista [de acciones] y ninguna otra" (lenguaje de intérprete); ADR-0019 dice solo "F22 lo implementa"; y el plan describe F18-F21 como módulos específicos por tema (lenguaje de código a mano) con F29 "espejo... no traducido línea a línea". Además la `forma` no basta para interpretarla literalmente: `perdida_dia` y `perdida_semana` declaran el MISMO `reinicia_con` (`reloj_dia_riesgo`), así que un intérprete no puede saber cuál reinicia a medianoche y cuál el domingo sin leer el nombre del acumulador. **Dónde:** `docs/adr/0001-...md:32`; `strategy_spec.yaml:212-213, 362-377`.
Se reproduce:
```
$ grep -rn -i 'interpret' src tests --include=*.py    # ningún intérprete de forma en el repo
$ awk '/^acumuladores:/,/^tokens:/' strategy_spec.yaml
perdida_dia: ... reinicia_con: reloj_dia_riesgo
perdida_semana: ... reinicia_con: reloj_dia_riesgo    # mismo token para dos relojes distintos
```
**Con dinero:** inferencia. Si F18-F22 se escriben a mano, la `forma` validada por las siete guardias queda como documentación; si se escribe un intérprete, F29 ("espejo de F18-F21") deja de tener sentido. Elegir después obliga a rehacer F18-F22 o F29-F31; un intérprete que reinicie ambos acumuladores a medianoche por ambigüedad del nombre deja operar tras -9 % cada día.
**Veredicto:** contexto MATIZADO (media): corrige que ADR-0019 y la Fase 6 del plan (F28-F30) ya fijan el reparto real (F22 despacha por nombre a primitivas escritas a mano en F18-F21; F29 espejo sin traducción; paridad por equivalencia diferencial) — la decisión existe en prosa, dispersa, no ausente. reproducir MATIZADO (media): mantiene que las reglas de negocio no están en el contrato mecánico Python-MQL5 (solo parámetros y casos).

**[42] [d8-camino-motor-04] F14b no se puede cerrar como una decisión de método aislada; la regla de qué nivel es la liquidez M15 no está abierta en ningún sitio.**
**Inferencia.** La pregunta de F14b (¿un hecho se apaga con una regla, o se declara con la duración y el motor la interpreta?) es semántica del MOTOR, no de método: la opción "apagar con regla" necesita predicados que hoy no existen y que son eventos del motor ([39]); la opción "durativo" exige que el motor interprete tokens como `hasta_el_corte_siguiente` ([21]). Además, A-24/A-25/A-26 (qué nivel es la liquidez M15, hallazgo [5]) solo existen en la PROSA de F14b, no en `ambiguedades.yaml`, así que ni `spec status` ni el cuestionario de la sesión 2 las ven. **Dónde:** `docs/plan/features/F14b-ciclo-de-vida-de-los-hechos.md:53-56, 76-88`.
Se reproduce:
```
$ grep -n 'id: A-2[4-9]' knowledge/spec/ambiguedades.yaml ; echo exit=$?
exit=1
```
**Con dinero:** inferencia. Si se cierra F14b sin el modelo de eventos, la mitad de las reglas nuevas que F14b describe (6 reglas, 2 hechos, 3 tokens) se reescribe al llegar F23; con `liquidez_tomada` sin apagar, reentrada indefinida sobre la misma liquidez: tres pérdidas (1,5 %) cada vez que el precio vuelva.
**Veredicto:** reproducir/contexto MATIZADO (media): matiza que el trabajo de conocimiento de F19/F20 (liquidez M15) está DECLARADO aunque no registrado, y que A-21 sigue ABIERTA con `bloqueante: True` pese a que F12 (una de sus `resuelve_en`) ya cerró.

**[43] [d8-camino-motor-05] El bloqueo "F14b bloquea a F14" que serializa todo el camino crítico solo existe en un PROJECT_STATE sin commitear.**
**Hecho.** La única dependencia textual que detiene F14 (y con ella F18-F35) es una línea de `PROJECT_STATE.md` en el working tree, sin commitear. `MASTER_PLAN.md` no tiene fila F14b ni ACP/ADR que la inserte; el brief de F14 no depende de ella; las seis preguntas abiertas de F14 no tocan el ciclo de vida de los hechos. El propio fichero se contradice en otras líneas (`:34` dice "Siguiente: F13", `:400` pide decidir el reparto de mayo, ya decidido por ADR-0025). **Dónde:** `PROJECT_STATE.md:37` (frente a `34, 394, 398, 400`); `docs/plan/features/F14-case-library.md:3`.
Se reproduce:
```
$ grep -c F14b docs/plan/MASTER_PLAN.md docs/HANDOFF.md docs/plan/features/F14-case-library.md
0
0
0
$ git diff -- PROJECT_STATE.md
+Ninguna abierta. Lo siguiente es F14b (el ciclo de vida de los hechos), que BLOQUEA a F14: ...
```
**Con dinero:** inferencia. No cuesta dinero directo; cuesta calendario hasta la cuenta fondeada, con F34 (mínimo tres meses de sombra) detrás.
**Veredicto:** reproducir/contexto CONFIRMADO (media): en HEAD (commiteado) la dependencia existe pero SIN nombre ("F14 queda EN ESPERA: la auditoría encontró defectos de negocio..."); con nombre y como bloqueo formal solo aparece en el working tree.

**[44] [d8-camino-motor-06] RN-028 (el gate de noticias) exige un calendario externo que ninguna funcionalidad del plan provee.**
**Hecho.** ADR-0022 volvió bloqueante el filtro de noticias (RN-028, `pendiente_definicion: A-17`) — exactamente el caso en que el brief de F11 ya había anotado que haría falta "una fuente de datos y una funcionalidad propia, no un parámetro". El plan no la tiene (F15 es OHLC, F16/F17 son ticks) y el vocabulario no tiene predicado de noticia. **Dónde:** `docs/plan/features/F11-strategy-spec-schema.md:144-147`; `docs/adr/0022-...md:89`.
Se reproduce:
```
$ grep -n -i 'noticia|calendario|news' docs/plan/MASTER_PLAN.md    # sin fila en la tabla A
$ botsito.exe spec status
1 vigente(s) SIN CONDICION definida todavia: RN-028 (A-17)
```
**Con dinero:** hecho/inferencia. Sin ventana definida, o el bot opera noticias en la cuenta fondeada (el trader avisó de que FundedNext puede cerrarla aunque acabe en ganancia), o el calendario entra después de F23 como fuente de eventos nueva y obliga a tocar bucle, journal y replay ya escritos.
**Veredicto:** reproducir CONFIRMADO (media): ninguna fila del plan, ninguna ambigüedad y ningún ADR asigna esa fuente de datos.

**[45] [d8-camino-motor-07] F16/F17 están desbloqueadas por dependencia pero detrás de F14 por el orden del plan, y los ticks de la demo pedidos "desde hoy" siguen sin grabarse.**
**Hecho.** F16 depende solo de F15 (validada); por dependencia se podría abrir hoy, pero el orden E del plan la pone detrás de F11-F14. La investigación pidió grabar ticks de la demo "desde hoy" el 2026-09-03 porque el spread por hora "es irrecuperable a posteriori"; diez días después no hay un solo tick en el repositorio ni en `data/`. **Dónde:** `docs/plan/MASTER_PLAN.md:136-138, 222-226`; `docs/research/2026-09-03-...html:328`.
Se reproduce:
```
$ git ls-files | grep -ic tick
0
$ ls data/manifests
eurusd-m1-2026-{01,05,06,07,08}-*.yaml    # solo OHLC, ningún tick
```
**Con dinero:** inferencia. El perfil de spread por hora del broker real no se reconstruye a posteriori; sin él, el modelo de llenado de F24 y el colchón del stop a 0,8 se validan contra un spread supuesto.
**Veredicto:** reproducir CONFIRMADO (media): precisa que lo desbloqueado hoy por dependencia es F14 y F16 (no F16 y F17, que depende de F16 sin validar), y que "irrecuperable" no está demostrado (MT5 local ya guarda historial).

**[46] [d8-camino-motor-09] El lado del precio (BID/ASK) sobre el que se miden caja, llenado y stop no está decidido; los datos de referencia son solo BID.**
**Hecho.** Toda la geometría de F18-F21 se calculará sobre velas BID (ADR-0005), pero una compra límite se llena en ASK y el stop de una venta salta en ASK. Ningún ADR, regla ni parámetro dice en qué lado se trazan caja, entrada, stop y objetivo, ni en qué lado se evalúa el llenado; `modelo_llenado` no lo menciona. **Dónde:** `docs/adr/0005-...md:10`; `knowledge/spec/parametros.yaml:141` (modelo_llenado).
Se reproduce:
```
$ grep -rn -i -w 'ask|bid' knowledge/spec docs/adr    # ASK no aparece salvo dentro de nombres de fichero
```
**Con dinero:** hecho/inferencia. Un spread de 1 pip sobre una caja de 10 pips es el 10 % de la caja: decide si la límite se llena o no en el borde. Decidirlo tarde obliga a rehacer la geometría de F21 y el llenado de F24.
**Veredicto:** reproducir/contexto CONFIRMADO (media): que las velas de referencia sean solo BID está declarado con dueño (F16 decide "velas ASK o spread"), pero el lado de cálculo de la estrategia sigue sin decidir en ningún sitio.

**[47] [d7-metodo-07] La unidad que medirá la fidelidad de F26 no está decidida, y la gramática de etiquetado no representa al menos 30 de las 68 operaciones de mayo.**
**Hecho.** El proyecto maneja tres unidades incompatibles: ADR-0011 y `kappa.py` fijan una única decisión `{compra, venta, no_trade}` por `(caso, sesión H4)`; `PREREGISTRO.md` define "misma decisión" a nivel de OPERACIÓN (dirección, entrada, stop, objetivo); el brief de F14 deja abiertas D1 y D2. La spec permite varias operaciones por sesión (`cartuchos_max=3` por zona de liquidez); el material declarado lo confirma: 68 operaciones en 19 días, entre 1 y 7 por día. Con 19×2=38 huecos de sesión, al menos 30 operaciones no pueden ser la única decisión de su sesión, y la gramática las rechaza. **Dónde:** `src/botsito/cases/kappa.py:52`; `docs/validation/PREREGISTRO.md:17-18`.
Se reproduce:
```
>>> parsear_etiqueta("07-11: venta@08:37 e=1.15364 sl=1.15420; 07-11: venta@09:52; 11-15: no_trade")
EtiquetaError: la sesion 07-11 aparece dos veces
```
**Con dinero:** hecho/inferencia. Si F26 mide por sesión, el segundo y tercer cartucho —donde se concentran las pérdidas (33 de 68)— no se comparan nunca, y el bot puede aprobar con una gestión de reentradas distinta de la del trader. Condiciona la interfaz por operación que F18-F24 tendría que emitir para que F14/F26 la consuman.
**Veredicto:** reproducir/contexto CONFIRMADO (grave).

### E. Deuda del método de medición de F26 (no mueve la aguja del motor hoy, compromete la validación)

**[48] [d7-metodo-02] La reproducción byte a byte del reparto no prueba que se fijara antes de etiquetar; un paquete re-sorteado con otro seed también la pasa.**
**Hecho.** `comprobar()` saca el seed del mismo fichero que verifica y regenera desde él; si se re-sortea con otro seed, el `particiones.yaml` nuevo vuelve a reproducirse byte a byte. Lo único que queda probado es que el paquete es función determinista de (repo, datos, seed escrito), no cuándo se escribió ese seed. La única prueba de anterioridad es el historial de git, y esa depende de haber etiquetas `LABEL_CASE` de la misma sesión ([49]). **Dónde:** `src/botsito/cases/paquete.py:549, 50`; `docs/adr/0025-...md:64-69`.
Se reproduce:
```
$ PYTHONHASHSEED=0 python prueba_resorteo.py
seed nuevo 4; asignacion: {...distinta...}
comprobar paquete re-sorteado: ([], [])    # sigue "OK"
```
**Con dinero (indirecto):** hecho. ADR-0025 renunció a 4 días de desarrollo apoyándose en esta "prueba", que no distingue un reparto honesto de uno rehecho tras ver resultados: la cifra de F26 sobre holdout-1 solo la sostiene hoy el log manual de git, sin comprobación automática mientras no haya `LABEL_CASE` de la sesión 1.
**Veredicto:** reproducir MATIZADO (media): confirma el mecanismo tal cual lo describe ADR-0025 (que sí lo presenta con ese alcance). contexto CONFIRMADO (grave).

**[49] [d7-metodo-03] La guardia de ancestro solo protege frente a `LABEL_CASE` de la MISMA sesión que el paquete; las etiquetas de la ronda 2 no la arman.**
**Hecho.** `validar_paquetes` solo compara el commit de `particiones.yaml` con los `LABEL_CASE` cuyo campo `sesion` coincide con la carpeta del paquete; un `LABEL_CASE` de otra sesión sobre el mismo caso es válido por formato y no arma la guardia. El kit de kappa (ronda 2) necesita por construcción una sesión distinta. **Dónde:** `src/botsito/cases/paquete.py:641-643`.
Se reproduce:
```
# LABEL_CASE bajo 2026-09-20-sesion-02 sobre un caso de mayo; particiones.yaml reescrito después
$ botsito.exe knowledge validate
OK: ... 1 paquetes de sesion validos, particiones anteriores al etiquetado    # no detecta la reescritura
```
**Con dinero (indirecto):** hecho. Se puede reasignar qué días son holdout DESPUÉS de tener etiquetas, con `knowledge validate` en verde: la cifra de fidelidad que autorizaría operar en la cuenta fondeada podría medirse sobre días escogidos a posteriori.
**Veredicto:** reproducir MATIZADO (media): matiza que `kit check` en una máquina con `data/` sí denuncia la reescritura manual (exit 1); el hueco es solo en la puerta de CI/`knowledge validate` sin datos.

**[50] [d7-metodo-05] Los documentos no coinciden en qué partición da la cifra final de fidelidad.**
**Hecho.** `MASTER_PLAN.md` y `holdout/README.md` dejan holdout-1 para "discrepancias y corrección" y la nota final a holdout-2 (3 días medibles tras quemar 2026-05-14); `ADR-0021`, `HOLDOUT-EXPOSICIONES.md` y la fila de F26 del plan hacen de holdout-1 la nota (6 días). `ADR-0025` dice además que mayo nunca será la partición limpia de F26, mientras otros documentos lo tratan como el único material ciego que existe. `PREREGISTRO.md` exige declarar la partición y por qué, y no hay una respuesta coherente que copiar ahí. **Dónde:** `docs/plan/MASTER_PLAN.md:203`; `docs/adr/0021-...md:27-29`; `docs/adr/0025-...md:71-74`.
**Con dinero (indirecto):** hecho. Si gana la versión del plan, la cifra que habilita el paso a MQL5 y a la cuenta fondeada saldría de 3 días; si gana la de ADR-0025, no hay ninguna partición válida para la nota hasta que llegue un mes limpio sin fecha.
**Veredicto:** reproducir MATIZADO (menor): los documentos SÍ coinciden en que F26 abre holdout-1 y en que holdout-2 es la segunda oportunidad; el desacuerdo real es cuál decide. contexto CONFIRMADO (grave).

**[51] [d7-metodo-06] El mínimo de unidades para que la cifra de F26 tenga poder estadístico no está declarado, y holdout-1 no lo alcanza.**
**Hecho.** `PREREGISTRO.md` pide métrica, umbral y partición, pero no potencia, ancho de intervalo ni N mínimo. Para distinguir un acuerdo de 0,8 de uno de 0,6 (binomial exacta, α=0,05 unilateral, potencia 0,80) hacen falta 36-39 unidades independientes. Holdout-1 da 10-14 unidades efectivas (según se mida por sesión o por operación, con la correlación intra-día que impone el sesgo H4); ni los 12 días medibles de holdout juntos llegan. **Dónde:** `docs/validation/PREREGISTRO.md:15-24`.
Se reproduce:
```
$ python aritmetica_f26.py
n=12 k=11 potencia(0,8)=0.275
primer n con potencia>=0,80: 36 ; n a partir del cual siempre >=0,80: 39
sesion H4 rho=0.2: n_eff=10.0 IC95 Wilson de 0,8=[0.490,0.943] excluye 0,6: False
```
**Con dinero (indirecto):** hecho. Una nota de F26 sobre holdout-1 es compatible a la vez con un bot que replica al trader 9 de cada 10 veces y con uno que lo hace 5 de cada 10: decidir con esa cifra si se pone dinero de la cuenta fondeada es decidir sin información.
**Veredicto:** reproducir/contexto CONFIRMADO (grave).

---

**Hallazgos muertos en verificación: 1.** «La descripción de `lotaje_base` se corta a mitad de frase y el corte pasa a la documentación generada» [d2-fidelidad-afirmaciones-08] — REFUTADO: el texto no está cortado; el repositorio escribe sin tildes, y «y solo el» es «y solo él» («el nivel lo pone `stop_fraccion_caja` y nadie más»), la conclusión de la frase anterior sobre la doble base del lote.


## 3. Dictamen sobre las 17 afirmaciones sin verificar del prompt

### Tabla de dictámenes (3.3.1 - 3.3.17)

| nº | Dictamen | Evidencia (una línea) |
|---|---|---|
| 3.3.1 | MATIZADO | Sin lista blanca de claves: `entonce` (RN-027) y `si_no` hermana con `tope: 9.5` (RN-020) pasan spec check y knowledge validate, es_ejecutable()=True, hash y reglas.md; solo pytest caza `entonce` por accidente en un test de booleanos YAML; `forma: {}` o renombrar a `resultado:` pasan todo. |
| 3.3.2 | CONFIRMADO | Token `15` declarado + `redondear_lote.paso: "15"` en RN-027 pasa spec check, knowledge validate y pytest (rc 0), entra en el hash (7ed4678e9be6) y en reglas.md; los tokens ni siquiera se imprimen en docs/spec. |
| 3.3.3 | MATIZADO | La mutación se reproduce entera (`no_es_multiplo_de.que: stop_fraccion_caja` pasa spec check, knowledge validate y pytest), pero las claves estructurales son 13, no 9, y su valor SÍ se contrasta contra nombres declarados: lo que falta es la CLASE del nombre. |
| 3.3.4 | MATIZADO | La guardia de la línea 198 exige 3 de 37 valores (0.8, 0.5 y 4.5) y sus exenciones no cubren enteros, enums ni booleanos; pero TEXTOS_PROHIBIDOS sí caza 6 valores de estrategia en forma de texto (y `objetivo_rr` como "1:3"), y el contrato AST no cubre literales por diseño, no por tener 3 llamadas. |
| 3.3.5 | CONFIRMADO | En el clon, `CORRECT objetivo_rr=25` (máximo 10): `apply --check` sale 0 y lista el cambio; `apply` sale 1 con "valor 25 por encima del máximo 10". `parametros.yaml` queda intacto. |
| 3.3.6 | MATIZADO (disputado) | `validar_manifiesto` solo exige que `escala` sea entero positivo y que `dias`/`huecos` sean mapas; un manifiesto nuevo con `escala 10`, símbolo GBPUSD, `dias {presentes: -5, velas: muchas}` y `huecos {mayores: ninguno, menores: -1}` pasa `data check --hashes` y `knowledge validate`, antes y después de commitearlo; solo la guardia de historial frena la edición de manifiestos YA commiteados. |
| 3.3.7 | CONFIRMADO | Se supersedieron con `evidence new` los ítems citados por RN-018, el predicado `operaciones_abiertas_alcanzan`, el parámetro `operaciones_simultaneas_max` (valor contradictorio "3") y el glosario "flujo de órdenes"; `knowledge validate`, `spec check` y `kit check` salieron con exit 0. |
| 3.3.8 | MATIZADO (disputado) | Se creó con `evidence new` un ítem por cada guardia de ADR-0009 §5. Solo la de 4 tokens en audio lo rechazó; las otras cinco entraron y `knowledge validate` salió con exit 0 (370 ítems). Sobre los 364 ítems reales, 7 violan G4 o G6. |
| 3.3.9 | MATIZADO (disputado) | Sin `data/`, `knowledge validate` emite un AVISO por transcripción por 360 citas y sale con exit 0. Una cita inventada commiteada pasa sin `data/` (exit 0) y falla con las crudas (exit 1). |
| 3.3.10 | MATIZADO (disputado) | Sin `data/`, `comprobar()` retorna en `paquete.py:563` antes de construir y comparar; exit 0 con OK en el original (con datos, sí compara) y en el clon (sin datos, no compara, ni con el reparto mutado); ADR-0025:45-46 lo llama "la única prueba mecánica". |
| 3.3.11 | MATIZADO | `activos()` corre sobre los registros de TODAS las sesiones (kappa.py:146), y la guardia de feedback acepta un supersede entre sesiones; pero la unidad de la ronda 1 solo desaparece si el retiro de la ronda 2 hace supersede AL registro de la ronda 1 sin reetiquetar esa unidad. |
| 3.3.12 | MATIZADO | "historial intacto" sin evaluar solo ocurre sin `.git` (probado con evidencia borrada: exit 0). En clon `--depth 1` es ERROR explícito. `state check` sin tags pierde 2/5 comprobaciones en silencio; sin git pierde 3/5, una con AVISO. |
| 3.3.13 | MATIZADO | No son once sino 9 funciones y 13 casos, todos colgando de un único skip (`test_hoja_sesion_docx.py:50`) sin protección CI; quitar el paquete los omite (incluido el de holdout), pero el run queda ROJO por `test_registro_accessors.py:103`; en checkout limpio corren 95 passed, 0 skipped. |
| 3.3.14 | CONFIRMADO | `cli.py:1823` dice "`anclaje_h4` sigue UNKNOWN (A-9)" y `cli.py:2128` dice "(A-9 sigue abierta)", visible en `data aggregate --help`, pero `parametros.yaml:202-217` tiene `anclaje_h4` CONFIRMED "17:00" America/New_York y `ambiguedades.yaml:134-146` tiene A-9 RESUELTA. |
| 3.3.15 | MATIZADO | Cierto que la forma solo fija `sesgo` con ruptura (strategy_spec.yaml:455-465). Falso que eso sea "lo contrario" del literal: literal y corpus describen que el sesgo previo persiste hasta que haya ruptura. |
| 3.3.16 | MATIZADO | Confirmado que el literal no sostiene la definición y que el glosario rechaza `decision`. Matizado: no es un círculo lógico sino un ancla sin definir ("stop inicial" no aparece en ningún otro sitio), y "nivel 0/nivel 1" no están solo en el campo `unidad`. |
| 3.3.17 | MATIZADO | Cierto que "apenas toca" no sostiene "distinta de la de entrada y posterior" y que no hay `decision`. Falso que viva solo en notas y forma (está también en título y `cuando`) y que sea invención del equipo: el trader lo dice en v6 0:42:22 y lo recogen dos ítems de evidencia de v4. |

### Matices y disputas

**[3.3.1] hecho.** `comprobar_forma` (spec/modelo.py:910-913) no tiene lista blanca de claves dentro de `forma`: solo cruza con el catálogo y valida los argumentos de las ramas `cuando`/`entonces`; la guardia de efectos sí recorre el árbol entero. Prueba: una rama hermana `si_no: {todos_de: [{predicado_inexistente: {tope: 9.5}}]}` en RN-020 y renombrar `entonces` a `entonce` en RN-027 pasan `spec check` y `knowledge validate` (rc 0), con `es_ejecutable()=True`, entrando en el hash (`c8f617a85be2` / `89a33c4fdb0b`) y en `docs/spec/reglas.md`. Solo pytest caza `entonce` por accidente, en `test_ningun_argumento_de_la_spec_real_es_un_booleano_de_yaml_1_1` (modelo.py trata `entonce` como invocación de un argumento lista), no la mutación `si_no`.

**[3.3.3] hecho.** Las claves de `_ESTRUCTURALES` (modelo.py:626-642) son 13, no 9: `liga, distinta_de, posterior_a, que, contra, a, de, acumulador, cual, por, resultado, hecho, a_la_baja`. Solo eximen de declarar el parámetro en `parametros`; su valor sí pasa por `_problemas_de_argumento` (modelo.py:940-943: `if clave in _ESTRUCTURALES or not isinstance(valor, str): continue` solo salta esa exigencia, no el contraste) contra un espacio plano sin distinguir clases. Prueba: `que: cuerpo` (valor que no es nombre) se caza, pero `que: stop_fraccion_caja` (nombre válido de la clase equivocada) pasa `spec check`/`knowledge validate` con rc 0 (hash `6e0aea01ca9b`) porque RN-027 no lo declara y nadie lo exige.

**[3.3.4] hecho.** `tests/contract/test_no_business_literals.py:220-229` solo exige 3 de los 37 valores de estrategia con valor (0.8, 0.5, 4.5 — `stop_fraccion_caja`, `riesgo_por_operacion`, `perdida_maxima_diaria`), con el comentario "`continue  # textos, enums, horas y booleanos: los vigila TEXTOS_PROHIBIDOS`" (línea 225). Pero TEXTOS_PROHIBIDOS (líneas 34-45) sí caza en forma de texto 5 parámetros (`huso_grafico`, `anclaje_h4`, `ventana_inicio`, `ventana_fin`, `instrumento`) y el texto "1:3"; y el contrato AST de accesores (`test_registro_accessors.py`) no prohíbe ningún literal por diseño, no por tener solo 3 llamadas medidas (`hoja_docx.py:480/602`, `paquete.py:395`).

**[3.3.6] hecho (disputado — 2 escépticos MATIZADO frente a CONFIRMADO del auditor).** `dataset.py:301-302` dice "«Los valores que dan significado a los datos se validan, no solo se aceptan»", pero `escala` (líneas 325-332) solo pasa por `_entero_positivo`: acepta 1, 10 o 100001 sin cruzarla con el símbolo ni con `instrumento_digitos`; `dias`/`huecos` (líneas 373-374) solo se exige que sean mapas, con cualquier contenido. Prueba: un manifiesto nuevo con esos valores basura pasa `data check --hashes` y `knowledge validate` con rc 0 antes y después de commitearlo; solo la guardia de historial frena editar uno ya commiteado. Los dos escépticos discrepan en el alcance del reproche: uno limita la contradicción con el comentario a `escala` (día/huecos son recuentos derivados que nadie relee), el otro no distingue y solo aclara que no está declarado como deuda.

**[3.3.8] hecho (disputado — 2 escépticos MATIZADO frente a CONFIRMADO del auditor).** ADR-0009 §5 ("docs/adr/0009-verificacion-de-citas-y-propuestas-trazables.md:38") declara 7 guardias, no 5. De las 6 por ítem, `evidence new` (`cli.py:965`, vía `_EntornoEvidencia.comprobar`) solo aplica "cita ≥ 4 tokens" en audio — reproducido: rechaza con `ERROR: ... la cita tiene 3 tokens; el mínimo es 4` — y deja pasar las otras 4 (raíz de tema en `_temas.yaml`, valor presente en la cita, cita duplicada, señal ASR/duda ⇒ confianza no alta); `knowledge validate` no las reaplica. Prueba: sobre los 364 ítems reales, 7 las violan (G4 en dos grupos: `ev-v6-000732-*` y `ev-v6-021939-*`; G6 en uno: `ev-v6-013508-b4c88d87`). Los escépticos coinciden en el hueco pero corrigen que "nadie las vuelve a aplicar" es falso para la de 4 tokens (sí la reaplica `verificacion.py:234`).

**[3.3.9] hecho (disputado — 2 escépticos MATIZADO frente a CONFIRMADO del auditor).** ADR-0009:17-19 dice "«`knowledge validate` verifica SIEMPRE contra la cruda citada... nunca contra "la activa del momento"»". Sin `data/` (estado de CI: `.gitignore '/data/*'`, `ci.yml` no la trae), `knowledge validate` no localiza ninguna cita de audio, emite un AVISO agregado por transcripción (45+52+98+130+12+23=360 citas) y sale con exit 0; un ítem con cita inventada (`ev-v4-003710-f610cc8f`) pasa así y solo falla con las crudas presentes (exit 1). Los dos escépticos corrigen la lectura de la ADR: el "SIEMPRE" decide contra qué transcripción se verifica (la citada, nunca la activa), no que se verifique pese a faltar la cruda; esa degradación a aviso está diseñada y declarada en el brief F07 §5, su informe de validación y `knowledge/evidence/README.md:48`, aunque la propia ADR no nombra ese caso.

**[3.3.10] hecho (disputado — 2 escépticos MATIZADO frente a CONFIRMADO del auditor).** ADR-0025:45-46 dice "«`kit check` sigue dando exit 0 sobre el paquete de la sesión 1, y con él la única prueba mecánica de que las particiones se fijaron antes de etiquetar»". Sin `data/` (estado de cualquier clon), `comprobar()` retorna en `paquete.py:559-563` antes de construir y comparar; `kit check` sale con exit 0 incluso con `particiones.yaml` mutado. Prueba: ambos escépticos señalan que esa atribución es falsa según el código porque existe otra prueba de anterioridad que no necesita datos y sí corre en `make check`/CI: la guardia git de `validar_paquetes` en `knowledge validate` (`paquete.py:640-666`). Uno añade que el modo "solo esquema" está declarado desde F10 (ADR-0011:62-63, `test_kit.py:432-434`) y avisa por stderr, no es silencioso.

**[3.3.11] hecho.** `kappa.py:146` (`vivos = [r for r in activos(list(registros)) if r.sesion == sesion ...]`) aplica `activos()` a los registros de TODAS las sesiones antes de filtrar por la propia (`comun/documentos.py:103-106`, sin filtro de sesión), pese a que el docstring (kappa.py:143-144) dice "«Una corrección hecha en otra sesión NO retira la etiqueta de esta»". La guardia de feedback (`modelo.py:427-469`) solo exige mismo objetivo y orden temporal, nunca misma sesión. Prueba: en el escenario reproducido E2, un BORDERLINE de la ronda 2 hace supersede al `LABEL_CASE` de la ronda 1 sobre la misma unidad sin reetiquetarla, y `calcular()` da `unidades=2 po=1 kappa=1 avisos=[]`: la unidad desaparece en silencio. Si la ronda 2 sí la etiqueta (E3), falla con `EtiquetaError`, pero señalando a la ronda equivocada.

**[3.3.12] hecho.** `validation/knowledge.py:323-326` (`con_git = hay_git(repo)`; `if historial is None and con_git:`) es lo único que convierte "no evaluable" en fallo; sin ese `con_git`, un `git archive HEAD` (sin `.git`) imprime "OK: ... historial intacto" y "commits con Fuente" cinco veces con exit 0, sin evaluar ninguna guardia. Prueba: reproducido con un ítem de evidencia borrado (`ev-v6-003515-530fc093.yaml`) y comentarios añadidos a 4 manifiestos: todo pasa igual. En un clon superficial (`--depth 1`) da `ERROR: la guardia de historial de evidencia no se pudo evaluar (clon superficial...)` y exit 1; sin tags, ancla por SHA y sí detecta la mutación.

**[3.3.13] hecho.** Son 9 funciones y 13 casos, no once, los que dependen de la fixture `sesion` (`test_hoja_sesion_docx.py:46-51`: `if not sesiones: pytest.skip("no hay ningún paquete en knowledge/cases/kit/")`), sin la guardia CI/`BOTSITO_EXIGE_FFPROBE` que sí tienen los tests de ffmpeg. Aislado y con `CI=1` el fichero sale verde con 13 skipped. Prueba: en el run completo no hay verde silencioso — quitar el paquete del kit produce "2 failed, 80 passed, 13 skipped" porque `test_registro_accessors.py:103` hace assert sobre la misma `sesiones_del_kit`; con el paquete versionado en checkout limpio la suite da "95 passed in 90.26s", 0 skipped.

**[3.3.15] hecho.** La forma de RN-003 (`strategy_spec.yaml:455-465`) solo fija el hecho `sesgo` cuando la vela H4 previa rompe el extremo de la anterior, evaluado solo al abrir cada sesión (07:00/11:00 Madrid). Es falso llamar a esto "lo contrario" del literal ("«si no genera un rompimiento por encima... entonces seguiríamos operando bajista»", strategy_spec.yaml:447-450, fb-...-8eccf5c0): como los hechos son estado persistente (`hechos.sesgo` sin valor inicial declarado, apagable solo por el token "no"), una vela sin ruptura conserva el último sesgo, que es justo lo que dice el literal y el corpus (`kb at --video v6 --t 1:03:30`: "«...seguimos buscando bajistas... hasta que... el precio debería generar un breaker por encima»"). Lo no declarado son dos huecos distintos: el valor inicial en el arranque y qué lado gana en una ruptura a ambos lados.

**[3.3.16] hecho.** El literal citado (`ev-v2-003336-fc210a05`: "«yo calculo mi lotaje desde aquí... lo pongo en 0.75 y estoy guardándome 0.25»") no sostiene la definición de caja (`glossary.yaml:96-108`, "la distancia entre la entrada y el extremo del stop inicial"): no nombra la caja, sus extremos, los niveles ni el objetivo, y la definición cambió en el commit `59b16f6` (F12) sin tocar el literal. El glosario rechaza el campo `decision`: reproducido, "`ERROR: spec: glossary.yaml: término 9: campos desconocidos ['decision']`". No es un círculo lógico en sentido estricto sino un ancla sin definir — "stop inicial" no aparece definido en ningún otro sitio de la spec — y "nivel 0/nivel 1" no están solo en el campo `unidad` (`parametros.yaml:~335,~560`): también en dos descripciones, ADR-0014 y el kit.

**[3.3.17] hecho.** El literal de RN-014 ("«yo siempre lo he estado trabajando, o sea, apenas toca»", `fb-...-0ccafcba`, `strategy_spec.yaml:751`) responde a la pregunta tocar-o-cierre planteada por el consultor ("kb at --video v6 --t 0:56:10": "¿la vela ya esté consolidada o quieres que sea apenas toque?"), no a si la zona es distinta de la de entrada y posterior a ella. Eso sí lo dice el trader, pero en otro pasaje: v6 0:42:22, "«La condición es que después de la entrada, desarrolle otra zona de control y ponemos en break-even»" (`kb find "otra zona de control" --frase` da 10 resultados). Es cierto que RN-014 no declara `decision`, pero ni `strategy_spec.yaml:9-12` ni `comprobar_decisiones` la exigen aquí: los dos parámetros de RN-014 tienen fuente `feedback`, no `decision` del consultor.

### Reconfirmación 3.1.1 - 3.1.4

| nº | Dictamen | Evidencia (una línea) |
|---|---|---|
| 3.1.1 | CONFIRMADO | `modelo.py:384` hace `continue` si falta cita O literal; los 3 acumuladores tienen `literal=None`, una cita cambiada a un registro sin relación pasa todo, y `reglas.md:1036-1038` imprime `*«»*`; el mismo `continue` deja pasar a cualquier predicado sin literal. |
| 3.1.2 | MATIZADO | Nada del registro, `apply` ni `validate` canoniza los husos de tipo texto: `apply` escribe "Europe/madrid" y `knowledge validate` sale 0. Pero pytest lo caza (`huso_operativa` siempre; `huso_grafico` solo en sistema case-sensitive) y `paquete.construir` sí canoniza `huso_operativa` (y falla en Windows por ese camino). |
| 3.1.3 | CONFIRMADO | El grep de los 12 accesores con cualquier receptor da exactamente 3 llamadas en `src/`, las 3 `.texto(...)`: `hoja_docx.py:480` y `:602`, `paquete.py:395`. Ninguna con el nombre en variable ni desde `engine/`/`domain/`. |
| 3.1.4 | MATIZADO | 8 `fijar` y solo RN-013 apaga (`orden_limite_pendiente: no`); los dos tokens durativos (`hasta_el_corte_siguiente`, `hasta_cartuchos_reinicio`) tienen 0 lectores en `src/` y `tests/`; pero `sesgo` es multivalor y que persista sin ruptura es lo que dice el literal del trader, no un fallo de interruptor. |

Nota sobre el matiz: en 3.1.2 el hueco de canonización es real solo para el camino que no pasa por `paquete.construir`; en 3.1.4 solo `liquidez_tomada` y `operacion_abierta` (no `sesgo`) encajan en el patrón "se enciende y nunca se apaga".


## 4. El intérprete de juguete: qué hace la spec cuando se ejecuta

### 4.0 Qué es, y qué no inventa

**hecho.** El intérprete (`interprete.py`, ~500 líneas) carga `strategy_spec.yaml` con `botsito.spec.modelo.cargar_reglas/cargar_vocabulario` en solo lectura y ejecuta las 24 reglas ejecutables con precedencia por clase sobre eventos SINTÉTICOS con fechas de 2027, nunca sobre una vela real ni sobre holdout. Corrió 29 trazas más `s09_*`, una exploración de grafo cerrado y el experimento de F14b. La geometría (`rompe`, `se_da_esquema`, `se_completa_zona_de_control`, liquidez de M15) no existe en el repositorio: cada evento del escenario declara en `senales` qué predicados geométricos son ciertos; el reloj, los acumuladores, el bróker sintético, el lote y el stop los calcula el intérprete con `parametros.yaml`. Por evento aplica: corte de día de riesgo (17:00 America/New_York), sub-eventos de bróker (llenado/cierre), `candidatas` (reglas cuyo `cuando` nombra algo presente), evaluación por clase `gate > terminal > disparador > fallback`, acciones (bloqueadas si abren y hay `prohibe`), `EMPATE` para pares de la misma clase sin `complementa`, y sub-eventos de colocación/cierre forzoso.

**hecho.** Rellena 9 huecos que la spec no resuelve, todos conmutables por configuración (H-01 a H-09, tabla de 57 filas con 35 HUECO): colocación implícita de la orden, efecto por defecto permitido, evaluación por fases de clase, `abrir_operacion` bloquea colocar/reentrar pero no el llenado, tokens durativos leídos como valor opaco, un cartucho por cada cierre en pérdida, semana = día, `por: equal` no casa con `cualquier_esquema`, y sesión = `ventana_inicio`.

**sin_verificar.** La geometría es sintética: no se comprobó que ninguna vela real de mayo de 2026 produzca esas secuencias ni con qué frecuencia. El rechazo de MT5 a un volumen no múltiplo del paso y el efecto de fin de semana/overnight son conocimiento del bróker, no ejecutado. Qué mide exactamente FundedNext para su límite diario (A-19 abierta) es hipótesis. La exploración usa un alfabeto de 9 símbolos y una clave de estado que trocea pérdidas en unidades de 0,5 %: puede haber ciclos o estados sin salida fuera de esa abstracción. No se ejecutó pytest ni ninguna orden `botsito` sobre el repo real en ninguno de los cinco laboratorios de esta dimensión (d1, escéptico del intérprete, alternativa A, alternativa B, juez, contra-juez), y ninguno tuvo exposición a holdout ni a velas de mayo 2026: todo son eventos sintéticos de 2027, comprobado en cada caso con `find -mmin`, `find *.pyc -newermt` o `git status --short` (ninguna escritura salvo ` M PROJECT_STATE.md`, ajena a esta dimensión).

### 4.1 La traza de la jornada (extractos)

**hecho [d1-interprete-01/02/05/06].** `trazas_v5/s01_jornada_normal.txt`: 07:00 RN-003 fija sesgo alcista; 07:45 una mecha no toma liquidez; 08:00 RN-004 fija `liquidez_tomada: si`; 08:12 H-01 coloca (colocación implícita) y RN-011 dimensiona lote 6,25 con stop 1,0992; 08:20 el precio llena la límite: RN-013 y RN-015 disparan juntos (tp 1,103) y en ese MISMO tick disparan también RN-008 y RN-018 (gate); 08:40 RN-014 pone el break even; 09:30 toca el objetivo, +1875; 11:00 RN-003 NO dispara (sin evento de sesión); 15:00 RN-002 dispara sobre `OP=T1`, ya cerrada por el objetivo. Estado final citado literalmente: `{'sesgo': 'alcista', 'liquidez_tomada': 'si', 'orden_limite_pendiente': 'no', 'operacion_abierta': 'si'}` con `'posicion': false` — la operación sigue "abierta" en los hechos sin existir en el bróker.

**hecho.** `s01b_jornada_vocabulario_estricto.txt` (sin H-01, solo el vocabulario declarado): `colocaciones=0`. Leída al pie de la letra, sin rellenar el hueco de colocación, la jornada normal no abre ninguna operación [d1-interprete-06].

**hecho [d1-interprete-02].** `s02_dia_dos.txt`: #11 07:30 "HOY no se ha tomado ninguna liquidez de M15" y aun así H-01 coloca ("colocación implícita: se envía orden límite"); #12 07:40 RN-006 y RN-014 disparan juntos ("RN-014 mover_stop sobre OP=T1 que YA NO EXISTE"); #14 15:00 RN-002 vuelve a disparar sobre la OP ya cerrada. La pérdida del cierre forzoso, −445,20, no llega a `perdida_dia`.

Estos extractos fijan el vocabulario del resto de la sección: "coloca" es siempre H-01 rellenando un hueco, no una acción de la spec; "dispara" es un evento que la clase gana o empata; y los hechos que copian al bróker (`operacion_abierta`, `orden_limite_pendiente`) sobreviven al cierre real de la posición.

### 4.2 Los estados sin salida

**hecho [d1-interprete-01].** Con los tokens durativos leídos literalmente (valor opaco que nunca expira — elección H-05), la exploración de grafo cerrado con `PROF=40 MAXEST=6000` da:

```
EXPLORACION base_literal: estados=39 expandidos=39 aristas=261 aristas_con_colocacion=5
frontera no expandida: 0 ; SIN SALIDA: 5 (todos con detenido_por_cartuchos, cartuchos 3, OP_vieja True)
  testigo: ['toma_m15','esquema','toca_limite','toca_stop','esquema','toca_limite','toca_stop','esquema','toca_limite','toca_stop']
EXPLORACION durativos_interpretados: estados=213 expandidos=213 ... SIN SALIDA: 0
```

Es decir: tres pérdidas seguidas —1,5 % de la cuenta, un evento normal en una semana— bastan para que, en la lectura literal, el bot no vuelva a operar nunca. RN-020 (`detenido_por_tope`) tiene la misma forma y el mismo resultado.

**hecho [esceptico-interprete, conclusión sobre d1-interprete-01].** El absorbente de `detenido_por_tope` es artefacto puro de esa elección: su reinicio es `reloj_dia_riesgo`, que sí existe en el registro, y leerlo da 0 estados sin salida. El de `detenido_por_cartuchos` NO se resuelve solo cambiando la lectura: su reinicio es `siguiente_liquidez_m15`, y ningún predicado de `strategy_spec.yaml:47-208` representa "se marca liquidez nueva en M15"; la variante "interpretada" de d1 (213 estados, 0 sin salida) usa una señal inventada, `se_marca_liquidez_m15` (`interprete.py:388-391`), que es exactamente el hueco que F14b:23-24 ya declara. Ampliando la clave de estado (que d1 dejaba corta), la base literal pasa de 39 a 53 estados con los mismos 5 sin salida; con el evento inventado, de 213 a 313, con 0.

**hecho.** El bot muerto NO lo causa el test que exige `produce ⊆ consume` (`tests/unit/test_spec.py:815-821`): quitando de RN-016 la rama que se autoconsume, la exploración da los mismos 39 estados y 5 sin salida (RN-001 sigue leyendo el hecho). Esa parte del hallazgo original no se sostiene como causa; queda como MATIZADO — ver 4.3.

**hecho — la vida después de las tres alternativas.**

| lectura / variante | estados | sin salida | fuente |
|---|---|---|---|
| d1, literal (H-05, tokens opacos) | 39 | 5, todos `detenido_por_cartuchos` | [d1-interprete-01] |
| d1, durativos interpretados (evento inventado) | 213 | 0 | [d1-interprete-01] |
| Escéptico, clave ampliada, literal | 53 | 5 | esceptico-interprete |
| Escéptico, clave ampliada, con evento inventado | 313 | 0 | esceptico-interprete |
| Alternativa A (apagado por regla + clase `expira`) | 23.620 | 0, 3 ciclos de reentrada sin tomar liquidez | alternativa_regla, escenario (9) |
| Alternativa B (duración declarada + fase fija) | 8.227 | 0, 3 ciclos | alternativa_duracion, escenario (9) |
| Juez, híbrido H | 8.125 | 0, 21 pares de la misma clase sin conflicto | juez (1) |
| Contra-juez, BFS propia de H por día (`c05b`) | 69.786 | 0, pero **máximo 10 stops sin tomar liquidez nueva** en el mismo grafo | contra_juez, contraejemplo 2 |

**hecho.** Ninguna de las tres alternativas revividas (A, B, H) queda viva sin el mismo ingrediente que falta hoy: un evento `se_marca_liquidez_m15` con geometría. Sin él, las tres mueren igual tras agotar cartuchos: A no lo prueba aislado pero hereda el hueco (su `alcanza_reinicio(cartuchos)` "esconde dentro del motor la geometría de 'la siguiente liquidez de M15'"); B, sin ese evento, da `b04c`: 3 colocaciones y `detenido_por_cartuchos` fijo, con 104 estados sin salida en su BFS; H, igual, `h04c`: 3 colocaciones, cartuchos=3 al final. Las ambigüedades A-24, A-25 y A-26 que resolverían ese predicado **no están abiertas** (la última ambigüedad numerada es A-23) — es un riesgo común a las tres alternativas, no una elección de método.

**hecho [contra-juez].** El "0 sin salida" de H no significa lo que la tabla comparativa del juez sugiere. Su propia BFS completa (69.786 estados) contiene secuencias con hasta 10 pérdidas seguidas sobre la MISMA toma de liquidez sin que ninguna regla las corte por cartuchos ni por zona perdida — más del triple de los "tres cartuchos" que fija el trader (`fb-...-e3eedcaa`: *"sería 3 pérdidas [...] Tras 3 pérdidas Claro"*). Lo que las detiene en la práctica es el tope de pérdida diaria (~4,86 %), no el mecanismo que H dice que corrige. Detalle en 4.7.

### 4.3 Las preguntas del experimento

#### ¿Qué apaga `liquidez_tomada`, `operacion_abierta` y `sesgo`?

**hecho.** Nada. `contar_fijar.py` da `apagado_por=[]` para los tres; el único `fijar` a `"no"` en toda la spec es RN-013 sobre `orden_limite_pendiente`. Traza s01, estado final ya citado en 4.1: `liquidez_tomada: si`, `operacion_abierta: si`, sin posición viva. `sesgo` solo cambia de VALOR si RN-003 dispara con otra ruptura; nunca se apaga.

**[d1-interprete-09] MATIZADO, media.** *Enunciado del auditor:* el sesgo no protege nada cuando falta, depende del orden de las señales en una envolvente, y RN-003 no tiene reloj para la sesión de las 11:00. Cita: `strategy_spec.yaml` — hecho `sesgo`/`liga: S`/`esta_al_otro_lado_de: {que: liquidez_m15, sentido: S}` (505-509), RN-003 (455-465), `abre_sesion_operativa` (62-68), `sentido_de_la_ruptura` (280-281). Reproducción: `s07a_interior_sin_sesgo.txt` #3 `esta_al_otro_lado_de{sentido: alcista}` → `disparan: gate=[RN-008]` (RN-005 no dispara) → #4 "H-01 colocación implícita: se envía orden límite compra"; `s07b`/`s07c` (mismas señales en otro orden) fijan sesgo bajista o alcista según cuál se evalúe primero; `s01` #8 11:00 (la H4 rompió el mínimo) no dispara RN-003, el sesgo sigue alcista de las 07:00.

*Corrección de los dos escépticos:* el efecto "sin sesgo no hay freno" es real solo en **arranque en frío**, antes de la primera ruptura H4: `se_da_esquema` depende solo de `liquidez_tomada` (spec:129) y como ningún hecho de sesgo existe aún, RN-005 —el único consumidor de `sesgo` en una forma— no puede disparar y nada más prohíbe. Una vez fijado, `sesgo` no se apaga nunca (ya confirmado en 3.1.4) y una H4 interior en días posteriores CONSERVA el sesgo anterior, que es justo lo que dice RN-003 ("es el de la vela H4 previa cerrada", spec:444); la traza `s07a` no demuestra "cuando falta" en general, solo el caso frío. El orden en la envolvente y la falta de reloj para la sesión de las 11:00 SÍ se sostienen como huecos, ya citados como abiertos en `AUDITORIA-2026-09-12-material.md:240,249` ("H4 previa que rompe los dos extremos (y el sesgo del primer día)"), aunque no llegaron a `ambiguedades.yaml` ni a F14b. Severidad ajustada por ambos votos: media.

**hecho [esceptico-interprete, dictamen DEPENDE_DE].** El "no tiene reloj para la 11:00" es en parte artefacto de la elección H-09 (sesión = `ventana_inicio`): RN-003 declara `anclaje_h4` entre sus parámetros (spec:446) y con la sesión leída como borde de esa rejilla, RN-003 sí dispara a las 11:00 — pero solo en los días en que la rejilla casa; en los 28 días en que no casa (según la cita de d5), esa lectura tampoco da un borde a las 07:00. Depende de A-14/ADR-0017, que es de la dimensión de relojes, no de esta.

#### ¿Qué hace el bot el segundo día, si nada se apaga?

**hecho.** `s02_dia_dos.txt`: #11 07:30, coloca sin ninguna toma de M15 ese día ("HOY no se ha tomado ninguna liquidez de M15" → H-01 coloca igual); #12 07:40 RN-006 y RN-014 disparan juntos ("RN-014 mover_stop sobre OP=T1 que YA NO EXISTE"); #14 15:00 RN-002 cierra y vuelve a disparar sobre la OP ya cerrada. La pérdida del cierre forzoso, −445,20, no suma a `perdida_dia`.

**[d1-interprete-02] MATIZADO, media (auditor: grave).** *Enunciado del auditor:* los hechos que copian el estado del bróker se desincronizan y resucitan el par RN-006/RN-014, "el más caro" que ADR-0018:32-37 dio por cerrado; RN-014 mueve el stop de una operación muerta y RN-002 cierra una ya cerrada. Cita: `strategy_spec.yaml` RN-010 (624-631, `- gestionar_salida: {...}` / `- fijar: {hecho: operacion_abierta, a: "si"}`, sin apagar `orden_limite_pendiente`), RN-006 (533-542), RN-014 (756-767), RN-002 (428-436). Reproducción: `s08a_equal_geometrico.txt` #5 "EMPATE sin desempate ...: RN-006 y RN-014 clase=disparador acciones=[reubicar_orden_limite]/[mover_stop] conflicto=True"; `s02` #12 el mismo empate; `s01` #9 "RN-002 cerrar_a_mercado de OP=T1: NO hay posición viva; no-op".

*Corrección de los dos escépticos:* el residuo es real y nuevo por la vía `equal` (RN-010 enciende `operacion_abierta` sin apagar `orden_limite_pendiente`, algo que introdujo el propio commit de la auditoría del 12-09), pero el titular exagera el impacto: en las trazas citadas una de las dos acciones del "empate" siempre es un no-op (la orden fantasma no existe o la OP no existe) y el break even SÍ se llega a poner; no hay segunda exposición real, que es lo que hacía caro el defecto original de ADR-0018 (allí RN-006 ganaba por orden de fichero y el break even NO se ponía). El "conflicto=True" lo calcula el detector del intérprete por NOMBRE de la acción (`interprete.py:487-488`), sin distinguir que `reubicar_orden_limite` actúa sobre la orden y `mover_stop` sobre la posición. Con los dos hechos derivados directamente del bróker (variante `hb` del escéptico), el par desaparece en `s02`, `s08a` y en la BFS cerrada, y RN-002 deja de disparar sobre la OP cerrada.

**hecho [esceptico-interprete].** Confirmado: derivar `operacion_abierta` y `orden_limite_pendiente` del bróker (en vez de fijarlos por regla) resuelve el par RN-006/RN-014 en todas las trazas probadas. Es la base de la recomendación (1) del juez en 4.7.

#### ¿Qué interpretan `hasta_el_corte_siguiente` y `hasta_cartuchos_reinicio`?

**hecho.** Nadie: 0 lectores en `src/` y en `tests/` (grep). Solo aparecen en `strategy_spec.yaml:282,284,831,933`, en F14b y en `docs/spec/reglas.md` generado. `hasta_cartuchos_reinicio` ("hasta el reinicio que diga `cartuchos_reinicio`", spec:282-283) duplica una puerta que ya existe: es el `reinicia_con` del acumulador `cartuchos` (spec:376); `hasta_el_corte_siguiente` duplica el `reinicia_con: reloj_dia_riesgo` de `perdida_dia`/`perdida_semana` (spec:366,371). Es la elección H-05 la que produce el estado absorbente de 4.2: leídos como valor opaco (nunca expiran), no como referencia a esos reinicios.

Las tres alternativas de F14b coinciden en borrar estos dos tokens: A los sustituye por el predicado `alcanza_reinicio{acumulador, segun}`; B los sustituye por `caduca_con: [reinicio_de: <acumulador>]`; H los elimina sin sustituto, leyendo el freno directamente como `alcanza_tope` sobre el acumulador. Tokens totales: A los mantiene en 20 (2 fuera, 2 dentro); B pasa de 20 a 19; H de 20 a 17.

#### ¿Dispara RN-019 alguna vez? — "equal" tiene tres significados

**hecho.** `grep -l 'disparan:.*RN-019' trazas_v5/*.txt` da un único fichero: `s08c_be_mismo_evento.txt`, con `pnl` exactamente 0,00 y la re-formación del esquema en el mismo tick; aun así, "RN-019 reentrar BLOQUEADA por prohibe=[abrir_operacion]" (RN-008, gate, prohíbe abrir en todo evento sin `se_da_esquema`). Con 7 USD de coste (`s08d`) el break even pasa a ser "pérdida" y RN-019 no dispara; en eventos separados (`s08b`) tampoco.

**[d1-interprete-07] MATIZADO, menor (auditor: media).** Cita: `strategy_spec.yaml` RN-019 (883-890, `se_cierra_operacion: {resultado: equal}` / `vuelve_a_dar_el_esquema: {}`), RN-008 (580-586), token `equal` (302-303: "cerró sin ganancia ni pérdida"), `glossary.yaml:74-83` ("dos extremos al mismo precio"), `parametros.yaml:488` ("activación sin rotura" — un tercer significado, el que usa RN-010).

*Corrección de los dos escépticos:* "RN-008 bloquea la reentrada" es artefacto del escenario: `s08c` declara solo `vuelve_a_dar_el_esquema` sin `se_da_esquema`, mientras que `s08a`/`s08b` declaran las dos juntas; repitiendo `s08c` con `se_da_esquema` en el mismo evento, RN-008 no dispara y RN-019 reentra (1 reentrada). Lo que SÍ está ya declarado, en F14b:25-26 y :73-75 y en `AUDITORIA-2026-09-12-material.md` §2.4: el token `equal` está mal definido y con esa definición RN-019 casi nunca dispara, salvo el caso degenerado de `pnl` exactamente 0,00. Lo nuevo y menor: el tercer significado de `equal` en `parametros.yaml:488`.

**hecho [esceptico-interprete, DEPENDE_DE].** La rareza de RN-019 sale de tres elecciones combinadas: tratar `se_cierra_operacion` como pulso de un solo evento (cuando la prosa de RN-019 describe una secuencia, "un equal cierra la operación y el precio vuelve a dar el esquema", spec:878); pnl NETO de costes (ver 4.4, [d1-interprete-03]); y que el escenario `s08c` mande `vuelve_a_dar_el_esquema` sin `se_da_esquema`. Con el resultado del cierre persistente hasta la siguiente colocación y "vuelve a dar" = "se da otra vez", RN-019 reentra en `s08a`, `s08b` y `s08c`, y con lectura bruta también en `s08d`.

#### ¿Hay secuencias sin salida, o que reentren indefinidamente sobre la misma liquidez?

**hecho.** Las dos. Sin salida: los 5 estados de 4.2 en lectura literal. Reentrada indefinida: el ciclo `['esquema','toca_limite','toca_objetivo']` vuelve al mismo estado colocando sin tomar liquidez nueva, tanto en lectura literal como con los durativos interpretados (`s09_*`): interpretar los tokens no arregla `liquidez_tomada`, que no tiene duración en ninguna lectura. Tras un stop, el bot reentra en la MISMA zona Z1 (`s03` #6) pese a que F14b:70-72 cita que el corpus pide una zona nueva fuera de la anterior (`ev-v4-003820`); y tras la ganadora vuelve a colocar sobre la misma liquidez (`s03` #9).

**hecho [esceptico-interprete, SE_SOSTIENE esta parte].** Bajo la lectura más caritativa combinada (`hechos_broker` + `equal_es_esquema` + resultado bruto + fases de punto fijo + durativos interpretados), la BFS cerrada da `estados=305, SIN SALIDA: 0`, pero **el ciclo de reentrada persiste**: `['esquema','toca_limite','toca_objetivo']`. Ya está declarado en F14b:20-22 y :70-72; no es un hallazgo nuevo, pero ninguna lectura del intérprete lo elimina.

**hecho [alternativas y juez].** Los ciclos de reentrada CAMBIAN de forma pero no desaparecen en ninguna de las tres alternativas: A y B eliminan el ciclo "tras ganadora" (con RN-030/liquidez que caduca) pero dejan un ciclo de break even, `['esquema','toca_limite','zona','toca_stop']` (o su variante `zona_dentro`), que la BFS de H también reproduce (3 ciclos, ver tabla del juez). El propio literal del trader lo permite ("reentrada después de equal, tampoco es considerado un intento", `fb-...-aa2abe65`), y ninguna de las tres alternativas fija un límite explícito a esa reentrada; solo la ventana de las 15:00 la acota en algunas lecturas. El contra-juez añade que, en H, una rama SIN CITA de la caducidad de la nueva `zona_perdida` permite además reentrar en la MISMA zona donde saltó el stop (ver 4.7).

#### ¿Hay empates de precedencia sin desempate?

**hecho.** Con conflicto real, uno: RN-006/RN-014 (disparador; `s02` #12, `s08a` #5; también en la BFS). Sin conflicto de conducta pero empatados por letra (las dos "prohíben"), muchos pares gate-gate en el mismo evento: RN-001/RN-020 ×309, RN-001/RN-008 ×239, RN-008/RN-020 ×218, RN-008/RN-018 ×123, RN-008/RN-027 ×85, RN-018/RN-027 ×83, y en la BFS RN-016/RN-020. Por la letra de `strategy_spec.yaml:31-32` ("dos reglas de la MISMA clase que actúan sobre el mismo evento son un ERROR"), todos serían error de validación, y la guardia actual no ve ninguno. El diseño de F14b añade otro CON conflicto: RN-004/RN-030 fijan `liquidez_tomada` a "sí" y a "no" en el mismo evento. El fallback RN-022 no dispara en ninguna traza: RN-008 cubre su misma extensión y dispara en 639 de 857 evaluaciones.

**[d1-interprete-05] MATIZADO, menor/media (auditor: media; clase: inferencia).** *Enunciado del auditor:* la precedencia por clase contradice el flujo de datos — los gates que leen lo que produce un disparador lo leen un evento tarde; para que funcione haría falta ejecutar un disparador antes que un gate, "lo contrario de lo declarado". Cita: `strategy_spec.yaml:19-32` (precedencia), RN-027 (1071-1083, gate), RN-011 (664-677, disparador). Reproducción: `s03_stop_y_reentrada.txt` #3 "RN-011 dimensionar_lote ... = 6.443299" (RN-027 no es candidata en ese evento); #4 "BROKER llena la límite ... lote=6.443299" / "RN-027 redondear_lote 6.443299 → 6.44 aplicado a: POSICIÓN YA ABIERTA"; `s02_dia_dos.txt` #12 el redondeo llega un evento después de colocar.

*Corrección de los dos escépticos, con severidad rebajada a menor por el voto "reproducir":* "contradice" no se sostiene — `strategy_spec.yaml:19-32` y ADR-0018:11-13 dicen quién GANA un conflicto ("una prohibición gana siempre"), no en qué orden se evalúa el estado; el propio auditor lo admite en su tabla ("no dice si se re-evalúa entre clases"). Con un punto fijo con refracción (cada regla dispara como mucho una vez por evento, y tras cada disparo se vuelve a empezar por los gates) se conserva esa precedencia y RN-027 redondea ANTES del llenado en todos los escenarios, sin cambiar la conducta de ningún otro (reproducido: "escenarios 26 diferencias 0" salvo las líneas de redondeo, que pasan de tardías a puntuales en `s03`, `s04`, `s05a/b/c`, `s08f`). Lo que sí se sostiene, con severidad media por el voto "contexto": la spec NO declara la semántica de evaluación DENTRO de un evento (en qué orden se aplican las acciones que producen datos frente a los gates que los leen), y no hay ninguna acción que coloque la orden, así que "calcular lote, redondear y enviar" no se puede expresar en la forma actual.

**hecho [esceptico-interprete].** Con fases por punto fijo, el efecto secundario de "5" también desaparece del tope diario (ver 4.4, [d1-interprete-04]): con el stop y un esquema nuevo en el MISMO evento, sin punto fijo se abre una 11.ª orden con 4,889 % ya perdido (máximo 5,365 %); con punto fijo se queda en 10 y 4,885 %.

### 4.4 Otros hallazgos de esta dimensión, con coste en dinero

#### [d1-interprete-03] MATIZADO, grave (auditor: grave) — el acumulador del tope se alimenta con el riesgo nominal y solo cuando salta el stop

**Cita:** `strategy_spec.yaml` RN-012 (684-688, 707-715: "la pérdida es `riesgo_por_operacion` sobre `base_calculo_riesgo`, entera y sin fracción"), acumuladores (362-377), tokens de resultado (302-307). **Reproducción:** `s08f_tres_be_con_coste.txt` l.58 "pnl=-7.00 → resultado=perdida" / l.62 "RN-012 realizar_perdida NOMINAL 499.97 → perdida_dia=499.97" / l.163 "perdida_dia=1499.79 (1.500 %)" tras tres break-even de 7 USD reales (21 USD); `s02_dia_dos.txt` un cierre forzoso en pérdida (−445,20) no suma nada a `perdida_dia`; `s03_stop_y_reentrada.txt` un stop pierde 502,58 y contabiliza 497,49.

**Corrección de los dos escépticos:** el hueco de fondo se sostiene — ningún acumulador declara QUÉ lo alimenta (`strategy_spec.yaml:362-377` solo lleva `base` y `reinicia_con`) y la única acción que "contabiliza la pérdida" es `realizar_perdida` en RN-012, con argumentos nominales y sin enlace declarado a ningún acumulador; los tokens de resultado no dicen si es bruto o neto. Pero el titular presenta como spec lo que en parte es cableado del intérprete (H-06, "contabilidad implícita"): el que un break even con costes cuente como pérdida es artefacto de clasificar el cierre por pnl NETO (`interprete.py:179-183`); el glosario sostiene la lectura BRUTA ("Ni el break even [...] cuentan como uno", `glossary.yaml:88`), y con esa lectura el break even no gasta cartucho ni suma a `perdida_dia`. El 497,49 frente a 500,00 es artefacto del INSTANTE en que se calcula la base (el intérprete actualiza el saldo antes de calcular el 0,5 %, `interprete.py:181` y :296-297).

**hecho [esceptico-interprete, DEPENDE_DE].** Confirmado con variantes ejecutadas: con resultado BRUTO, `s08d` pasa de `perdida_dia=499.97`/cartuchos 1 a `perdida_dia=0.0`/cartuchos 0; `s08f` pasa de 3 stops y bot detenido a 4 colocaciones sin detención y `perdida_dia=0.0`. Con la base nominal fijada al dimensionar (`nomdim`), `s03` pasa de 497,49 a 500,00.

#### [d1-interprete-04] MATIZADO, media (auditor: grave) — el tope diario del 4,5 % se sobrepasa por construcción

**Cita:** `strategy_spec.yaml` RN-020 (924-933), `alcanza_tope` (76-82: "un acumulador llega al tope declarado"). **Reproducción:** `s05a_tope_literal.txt` l.381 "RN-012 ... perdida_dia=4388.99 (4.389 % s/ saldo_inicial_dia)"; l.386 se abre la 10.ª orden; l.422 "perdida_dia=4864.54 (4.865 %)"; l.430, en el evento SIGUIENTE, "RN-020 fijar detenido_por_tope: None → hasta_el_corte_siguiente".

**Este es el único de los nueve hallazgos que el escéptico del intérprete confirma SIN matizar (dictamen SE_SOSTIENE).** Razón, hecho ejecutado: `alcanza_tope` es "el acumulador llega al tope"; RN-020 lo comprueba ANTES de abrir sin descontar el riesgo de la operación que se abre, y la pérdida REAL llega a ~4,89 % en todas las lecturas de contabilidad probadas (nominal, efectiva, nominal-al-dimensionar, sobre saldo). No existe en la spec ni en ADR-0015/0018 una lectura prospectiva del tope. La subparte "un evento tarde" sí depende de las fases: con el stop y un esquema nuevo en el MISMO evento y sin punto fijo, se abre una 11.ª orden con 4,889 % ya perdido (máximo 5,365 %); con punto fijo se queda en 10 y 4,885 %. Los dos votos del escéptico general bajan la severidad de grave a media porque el desfase exacto (365 USD sobre 100.000 en el ejemplo, hasta ~0,48-0,5 % del saldo inicial en el peor caso) depende de qué base usa `riesgo_por_operacion` (saldo actual) frente al tope (saldo inicial del día) — el propio ADR-0020 ("de once pérdidas a nueve") no anticipa este sobrepaso.

**Este hallazgo no lo arregla ninguna de las tres alternativas de F14b** (A, B ni H): las tres heredan la misma comprobación reactiva de `alcanza_tope`; el juez lo repite como riesgo 2 de su lista en 4.7.

#### [d1-interprete-06] MATIZADO, grave (auditor: grave) — no hay acción que coloque la orden límite ni que la cancele

**Cita:** `strategy_spec.yaml:212-213` ("Cada acción declara sus argumentos igual que un predicado, y el motor de F22-F23 implementa esta lista y ninguna otra"), acciones 214-253, `se_coloca_orden_limite` (151-155, predicado sin productor). **Reproducción:** `s01b` con vocabulario estricto: `colocaciones=0`; `s06a_orden_viva_15h.txt` #4 15:00 nada toca la orden pendiente, #5 16:10 se llena fuera de ventana, martes 15:00 cierra en −312,50; `s14_rn009_con_orden_puesta.txt`: RN-009 prohíbe abrir pero la orden ya colocada se reubica (RN-006) y se llena igual.

**Corrección de los dos escépticos:** "no hay acción que coloque" es falso al pie de la letra — `reentrar` (spec:245-247) SÍ coloca, pero solo la dispara RN-019 tras un cierre en `equal`, y presupone una primera colocación que ninguna acción hace; bajo la lista cerrada (spec:212-213), la primera operación de un esquema no se abre nunca sin rellenar el hueco. Tampoco hay ninguna acción que retire una orden pendiente. Ambos escépticos buscaron contexto que lo declarara como deuda deliberada y no lo encontraron: F14b no habla de la orden, y `ambiguedades.yaml` no tiene ninguna pregunta sobre una orden pendiente al llegar `ventana_fin`.

**hecho [esceptico-interprete, DEPENDE_DE].** El efecto de la orden viva a las 16:10 depende de una lectura de "prohíbe" que la spec no declara: si prohibir `abrir_operacion` ("abrir una posición nueva") implica retirar una orden que la abriría, y el esquema se lee como estado (no como pulso), la orden se retira a las 15:00 sin tocar la jornada normal (variante `cancela`: `s06a` termina con `orden=False, saldo=100000.0`). Esa lectura choca con la letra de spec:212-213 ("esta lista y ninguna otra"): retirar la orden no está entre las 13 acciones.

**Las tres alternativas de F14b coinciden en que hace falta una acción `cancelar_orden_limite`** y una regla que la dispare a las 15:00 (A: RN-035; B: RN-031; H: nueva regla terminal), y las tres marcan esa regla como SIN CITA del hecho de retirar la orden pendiente (`kb find` sobre "cancelar"/"cancela"/"eliminar orden": 0 resultados).

#### [d1-interprete-08] MATIZADO, media (auditor: media) — una entrada activada por `equal` nace sin objetivo

**Cita:** `strategy_spec.yaml` RN-015 (771-806: "el objetivo es fijo, se traza con la orden y no se mueve" / forma `se_activa_entrada: {por: cualquier_esquema}`), RN-010 (624-631), `cualquier_esquema` (300-301: "cualquiera de los dos esquemas de entrada"). **Reproducción:** `s08a_equal_geometrico.txt` #4 "BROKER llena la límite ... tp=None" / "disparan: ... disparador=[RN-010]" (sin RN-015); `s08e_equal_es_esquema.txt` (variante: `por: equal` SÍ casa con `cualquier_esquema`): disparan RN-010, RN-013 y RN-015 juntos y la posición recibe objetivo.

**Corrección de los dos escépticos:** el titular desaparece si se lee `por: equal` como incluido en `cualquier_esquema` (lectura con apoyo textual: el título de RN-010 es "una entrada activada sin ruptura se gestiona COMO CUALQUIER OTRA", spec:616; el literal de RN-015 es "Siempre se fija el 1:3, no importa en qué escenario", spec:783), pero esa inclusión NO está definida en ningún código del repo (`grep cualquier_esquema|equal` en `src/*.py`: 0) y el propio auditor la marca HUECO. Es una inferencia sostenida por dos hechos, no un hecho ejecutado. Con la lectura literal separada (la que usa también `tests/unit/test_spec.py:830-834`), la entrada por `equal` nace y vive sin objetivo hasta el stop, el break even o las 15:00. Se sostiene además, por prosa contra forma, que RN-015 dice fijar el objetivo "en el mismo instante en que se traza la orden" (spec:775-776) pero su forma dispara con `se_activa_entrada` (al llenarse), no al colocar: en la vía normal el objetivo también llega al llenar (`tp=None` en todos los llenados), no al trazar.

### 4.5 Qué sobrevivió al escéptico del intérprete, y qué era artefacto

El escéptico del intérprete es una segunda pasada, específica de esta dimensión: copió el intérprete de d1, comprobó que reproduce los 26 escenarios sin diferencias, y después probó una a una y combinadas las lecturas alternativas que las citas permiten, para separar lo que depende de una elección de lo que es hecho puro.

| conclusión | dictamen | por qué |
|---|---|---|
| [d1-interprete-01] cartuchos absorbente | DEPENDE_DE | el absorbente de `detenido_por_tope` es artefacto (su reinicio existe, `reloj_dia_riesgo`); el de `detenido_por_cartuchos` no se resuelve sin inventar `se_marca_liquidez_m15` |
| [d1-interprete-02] RN-006/RN-014, empates gate-gate | DEPENDE_DE | desaparece derivando los hechos del bróker; la gravedad estaba exagerada incluso en literal (siempre hay un no-op) |
| [d1-interprete-03] contabilidad de pérdida | DEPENDE_DE | el break-even-como-pérdida es artefacto de leer el cierre en neto; el hueco de fondo (nadie declara quién alimenta el acumulador) se sostiene |
| [d1-interprete-04] tope 4,5 % sobrepasado | **SE_SOSTIENE** | único que resiste las 6 lecturas de contabilidad y fase probadas |
| [d1-interprete-05] precedencia y RN-027 | DEPENDE_DE | "contradice lo declarado" es artefacto de leer la precedencia como orden de evaluación; con punto fijo el redondeo llega a tiempo en las 26 trazas |
| [d1-interprete-06] sin colocar/cancelar | DEPENDE_DE / INFERENCIA | el efecto a las 16:10 depende de una lectura de "prohíbe" no declarada; el núcleo (ninguna acción coloca la primera orden) se sostiene |
| [d1-interprete-07] RN-019 casi nunca dispara | DEPENDE_DE | sale de tres elecciones combinadas (pulso vs. secuencia, neto, escenario que fabrica el bloqueo de RN-008); el hueco de fondo (token `equal`) ya está declarado en F14b |
| [d1-interprete-08] equal sin objetivo | DEPENDE_DE | desaparece si `equal` se incluye en `cualquier_esquema`, lectura sin código que la decida; con la lectura literal (la que usan los tests) se sostiene |
| [d1-interprete-09] sesgo sin freno | DEPENDE_DE / INFERENCIA | solo en arranque en frío, no "cuando falta" en general; el resto ya está declarado como abierto en `AUDITORIA-2026-09-12-material.md:249` |
| Pregunta F14b (experimento preliminar A) | DEPENDE_DE | es un hombre de paja: repite lo que F14b:42-45 ya dice; con una regla de apagado sin autoconsumo el bot reanuda sin empate |

**hecho.** Bajo la lectura más caritativa combinada (`hechos_broker` + `equal_es_esquema` + resultado bruto + fases de punto fijo + durativos interpretados) la BFS cerrada da `estados=305, SIN SALIDA: 0` — pero el ciclo de reentrada `['esquema','toca_limite','toca_objetivo']` persiste (ver 4.3, última pregunta). Una segunda combinación con señales persistentes de esquema/cierre y "prohíbe cancela" no llega a cerrarse (`frontera no expandida: 2347`): NO CONCLUYENTE.

**Elecciones concretas del intérprete de d1 que producían los titulares más fuertes**, verificadas una por una por el escéptico: H-05 (tokens `hasta_*` opacos → produce los 5 estados absorbentes); H-03 leyendo la precedencia como orden de evaluación (→ "órdenes invertidas" de RN-027); predicados de bróker/geometría como pulso de un solo evento (→ 1 de 29 disparos de RN-019); resultado del cierre por pnl NETO (→ break even = pérdida, contra `glossary.yaml:88`); `realizar_perdida` sobre el saldo YA reducido por la propia pérdida (→ 497,49 en vez de 500,00); H-08 (`equal` no casa con `cualquier_esquema`, contra el título de RN-010 y el literal de RN-015); H-09 (sesión = solo `ventana_inicio`, ignorando `anclaje_h4`); H-07 (semana = día, de donde salen las 50 colocaciones de `s05b`); el detector de empates por NOMBRE de acción, no por objeto; y el arranque en frío sin historia de H4.

### 4.6 La pregunta de F14b: dos alternativas completas

#### Alternativa A — apagado por regla

**hecho.** Todo hecho se apaga con una regla explícita que lo fija a `"no"`, disparada por flanco; los tokens durativos desaparecen y su duración pasa a reglas con un predicado nuevo, `alcanza_reinicio`. Catorce reglas nuevas (RN-029..RN-042, doce de una clase nueva `expira` evaluada ANTES que `gate`), una disparador (fija `zona_perdedora` con el stop, F14b §3) y un gate que frena la reentrada mientras esa zona exista. RN-016 y RN-020 dejan de leer el hecho que fijan y lo encienden con `"si"`; RN-013 cede su apagado a RN-042.

**Coste medido:** 14 reglas nuevas, 3 reescritas, 1 hecho nuevo (`zona_perdedora`; 5 más cambian su declaración con el campo nuevo `apaga`), 4 tokens tocados (2 nuevos: `cualquier_resultado`, `cualquier_activacion`; 2 borrados: `hasta_cartuchos_reinicio`, `hasta_el_corte_siguiente`), 2 ADR nuevos más enmiendas a ADR-0018/0019/0015, 6 preguntas al trader. Reglas vigentes 25 → 39; `fijar` 8 → 20 (12 de ellos apagados, antes solo 1); spec +362/−30 líneas.

**Reglas ya escritas que habría que reescribir:**

| regla | campo | cambio |
|---|---|---|
| RN-013 | `forma.entonces.hace` | se quita `fijar orden_limite_pendiente a "no"` (pasa a RN-042); sin esto la guardia G4 nueva falla |
| RN-016 | `forma.cuando` | de `cualquiera_de: [..., hecho: detenido_por_cartuchos]` a solo `todos_de: [...]`: deja de leer el hecho que fija |
| RN-016 | `forma.entonces.hace` | `a: hasta_cartuchos_reinicio` → `a: "si"`; la duración la dice RN-032 |
| RN-020 | `forma.cuando` | se quita `hecho: detenido_por_tope` del `cualquiera_de` |
| RN-020 | `forma.entonces.hace` | `a: hasta_el_corte_siguiente` → `a: "si"`; la duración la dicen RN-033/RN-034 |

**Veredicto propio del laboratorio A:** funciona en el juguete solo con tres añadidos que dejan de ser "apagado por regla" a secas: una clase `expira` evaluada antes que `gate` (enmienda de ADR-0018), la fase del `reinicia_con` declarada, y eventos de bróker/reloj serializados por el motor. Con eso: 0 estados sin salida en 23.620, desaparece el ciclo de reentrada sin liquidez, no se reentra en la zona perdedora. Queda el ciclo de break even, que nadie acota. Precio: 14 reglas nuevas (8 sin cita directa: 4 sin cita, 3 cita parcial, 1 indirecta), 3 reescritas, 2 ADR, 6 guardias nuevas, 1 test reescrito, 6 preguntas al trader. Dictamen del propio laboratorio: usar apagado por regla SOLO para el contexto de mercado con cita directa (liquidez tras ganadora/cartuchos, zona perdedora) y derivar el resto — la misma conclusión a la que llega el juez de forma independiente (4.7).

**Debilidades medidas, no solo enunciadas:** no elimina la duración interpretada, la mueve a la fase del `reinicia_con` (con la fase mal puesta, `s05d`: martes entero sin operar y, tras el corte semanal, muerto hasta el domingo); necesita la clase `expira` evaluada antes de gate, o pierde colocaciones (`s03y`: 1 frente a 2) y empata `si`/`no` por orden de fichero; el bot muerto de F14b §2 no lo quita el método sino que exista RN-032 (sin ella, 3 colocaciones y detenido); la guardia de precedencia de hoy no ve empates entre reglas hermanas con `complementa` declarado (falso positivo medido); y persiste el ciclo de reentrada por break even (4 veces seguidas en `s09_ciclo_break_even`).

#### Alternativa B — duración declarada

**hecho.** Cada hecho declara `caduca_con` en el vocabulario (no en las reglas): una lista de condiciones con al menos un predicado de evento por camino, o `reinicio_de: <acumulador>`, o `persistente`. El motor aplica, por evento: reinicios de acumulador → caducidades `reinicio_de` → árboles `caduca_con` sobre las señales del evento → reglas por clase → acciones → sub-eventos del bróker con las mismas fases. Ninguna regla apaga: se borra el token `"no"`. Cuatro reglas nuevas: RN-029/RN-030 (no reentrar en la zona perdida, cita `ev-v4-003820`), RN-031 (retirar la límite en `ventana_fin`, sin cita), RN-032 (tope semanal separado del diario, con corte propio).

**Coste medido:** 4 reglas nuevas, 4 reescritas, hechos 6 → 8 (`zona_perdida` y `detenido_por_tope_semana` nuevos), tokens 20 → 19, 2 predicados nuevos (`se_marca_liquidez_m15`, `se_cancela_orden_limite`), 1 acción nueva, `naturaleza` en los 24 predicados, `version_esquema` 3 → 4, spec 11.0.0, 2 ADR + 1 enmienda, 8 citas del trader necesarias (3 con cita directa, 5 sin cita o con cita parcial/indirecta).

**Reglas ya escritas que habría que reescribir:**

| regla | campo | cambio |
|---|---|---|
| RN-001 | `forma.cuando.cualquiera_de` (409-410) | `hecho: detenido_por_tope` se parte en `detenido_por_tope_dia` y `detenido_por_tope_semana` |
| RN-013 | `forma.entonces.hace` (741) | se borra `fijar orden_limite_pendiente a "no"`; lo cubre `caduca_con` del hecho, incluida la vía `equal` que RN-010 dejaba pendiente |
| RN-016 | `forma.cuando`/`hace` (822-831) | fuera el autoconsumo; `a: hasta_cartuchos_reinicio` → `a: "si"` |
| RN-020 | `forma.cuando`/`hace`/prosa/parámetros (894-935) | queda solo con la rama diaria; la semanal pasa a RN-032 |

**Veredicto propio del laboratorio B:** funciona para lo probado y cuesta más de lo que parece. Con caducidades solo por EVENTO, la fase fijada y RN-029..032: grafo cerrado de 8.227 estados, 0 sin salida, frente a 5 de 39 con la spec del repo; no reentra tras ganadora ni en la zona perdida; resincroniza las copias del bróker (desaparece RN-006/RN-014). Dictamen propio: para `liquidez_tomada`, `zona_perdida` y `sesgo` (contexto de mercado sin otro sitio donde vivir) la duración declarada es la forma correcta; para los frenos (`detenido_por_*`), B duplica el ciclo de vida que ya tienen los acumuladores; para las copias del bróker es menos robusta que derivarlas del bróker — el mismo dictamen híbrido al que llega A por su lado, y el juez de forma independiente.

**Debilidades medidas:** "el bot muerto se muda, no se va" — sin `se_marca_liquidez_m15`, `b04c` da 3 colocaciones y 104 estados sin salida en su BFS; la trampa de F14b §2 sigue siendo expresable (una caducidad por ESTADO en vez de por evento reproduce el bot muerto, y las guardias de hoy dan 0 quejas); depende de la fase (`b04d`=6 frente a `b04g`=5 con un tick de diferencia); dos puertas para el mismo freno (el hecho `detenido_por_*` no añade información sobre lo que ya dice `alcanza_tope`); reentrada indefinida tras `equal` (mismo ciclo que en A); la liquidez agotada se puede volver a tomar (el hecho no guarda QUÉ nivel se tomó); 5 piezas sin literal deciden comportamiento (caducidad en `ventana_fin`, corte semanal en domingo, retirar la límite a las 15:00).

**Comparación de coste, las dos alternativas y la recomendación del juez (H):**

| criterio | A · apagar con regla | B · duración declarada | H · híbrido (recomendado por el juez) |
|---|---|---|---|
| Reglas nuevas / reescritas | 14 / 3 (vigentes 25→39) | 4 / 4 | 3 / 6 (las 6 solo quitan ramas o `fijar`) |
| Hechos / tokens | 6→7 / 20→20 | 6→8 / 20→19 | 6→5 / 20→17 |
| Grafo cerrado, sin salida | 0 de 23.620 | 0 de 8.227 | 0 de 8.125 (ver 4.7, matizado por el contra-juez) |
| Duraciones sin cita directa | 8 de 14 reglas nuevas | 5 caducidades/reglas | 5 (las mismas de B); bróker y frenos no necesitan cita |
| Guardias estáticas | clase `expira` + 6 nuevas; 2 fallos invisibles a cualquier guardia | 7 nuevas + generador; 1 guardia total | la de B + "ningún hecho del bróker se fija" |
| ADR / tests | 2 ADR + 3 enmiendas; 1 test reescrito | 2 ADR + 1 enmienda; 1 test invertido | 2 ADR + enmienda a ADR-0018; 2 tests reescritos, deshace F14b §0 |

### 4.7 La recomendación del juez, y lo que le opuso su escéptico

**hecho.** El juez recomienda un HÍBRIDO H, en un solo ADR de método antes de F22: (1) `orden_limite_pendiente` y `operacion_abierta` dejan de ser hechos que fijan las reglas — son estado DERIVADO del bróker; (2) los frenos (`detenido_por_tope`, `detenido_por_cartuchos`) dejan de ser hechos — RN-016/RN-020 prohíben mientras `alcanza_tope` (leído como estado) sea verdadero, frenados por el `reinicia_con` que el acumulador ya declara; desaparecen los tokens `hasta_*`; (3) solo el contexto de mercado (`liquidez_tomada`, `zona_perdida` nueva, `sesgo` persistente) declara `caduca_con`; (4) se borra el token `"no"`: apagar con regla queda prohibido por construcción; (5) el mismo ADR fija la fase dentro de un evento.

**Justificación medida por el juez, punto por punto:** (1) grafo cerrado de H: `estados=8125, SIN SALIDA: 0` (`h_bfs`), frente a 5 de 39 de la spec del repo; con la fase del corte aplicada DESPUÉS de evaluar (error de implementación), B pierde 10 de 28 colocaciones y A muere hasta el corte siguiente, mientras H mantiene las 28 — "un error de fase cuesta en H un evento; en A y B, días o semanas". (2) fidelidad: H no necesita cita para 4 de sus duraciones (son definicionales o ya citadas en `reinicia_con`); tiene las mismas 5 sin cita que B. (3) guardias: H y B admiten una guardia total ("todo hecho declara origen"); hoy el código no la tiene (`modelo.py:1019-1029` exige productor real y rechaza `spec_h`, medido). (4) sin reescribir el motor: cambiar una duración en H es editar un `reinicia_con` o una entrada de `caduca_con`. (5) coste: 3 reglas nuevas y 6 reescritas (solo quitan ramas), hechos 6→5, tokens 20→17 — pero deshace F14b §0 y obliga a reescribir dos tests.

**Riesgo que el propio juez señala y que ninguna opción resuelve:** el evento `se_marca_liquidez_m15` no existe en los 22 predicados y depende de A-24/A-25/A-26, sin abrir (ver 4.2); y la contabilidad tardía dentro de un mismo evento puede dejar abrir una operación de más sobre el tope diario (11.ª orden con 4,889 % ya perdido, hasta 5,365 % máximo) — el mismo [d1-interprete-04], que ninguna alternativa de F14b arregla.

**Pregunta cerrada que el juez propone llevar al dueño**, con tres decisiones abiertas obligatorias en cualquier opción salvo aplazar: (i) ¿la liquidez tomada y no operada caduca en `ventana_fin`? (ii) ¿una límite pendiente a las 15:00 se retira? (iii) ¿se autoriza abrir A-24/A-25/A-26 (qué nivel es la liquidez de M15) como precondición de F19?

**hecho — el contra-juez no lo confirma: `se_sostiene: False`.** Cinco contraejemplos, todos ejecutados sobre una copia de `spec_h` y del intérprete del propio juez:

1. **Reentrada en la MISMA zona perdida.** `lab/spec_h/strategy_spec.yaml:374-385` declara `zona_perdida.caduca_con` con una rama SIN CITA (`se_marca_liquidez_m15`) que basta, por sí sola, para apagar `zona_perdida` sin exigir que la zona nueva esté "afuera", como sí exige el literal que RN-030 cita (`ev-v4-003820`). Reproducido en `c01_marca_sin_toma.py`: un día con una sola toma a las 08:00 produce **10 colocaciones seguidas en la misma zona**, frenadas solo por el tope de pérdida diaria (`perdida_dia=4864.54`, ~4,86 %) — no por cartuchos ni por `zona_perdida`.
2. **La BFS propia de H lo confirma a escala.** `c05b_bfs_por_dia.py` (69.786 estados, 0 sin salida) da como máximo de todo el grafo alcanzable **10 stops sin una toma nueva sobre la misma liquidez** — más del triple de los "tres cartuchos" que la tabla del juez presenta como garantía de H.
3. **Simultaneidad dentro del mismo evento, no cubierta por "el ADR fija la fase".** Cuando la 3.ª pérdida que agota cartuchos y una marca de liquidez nueva caen en el MISMO tick (`c02_perdida_y_marca.py`), el bot hace 4 colocaciones en vez de 3; un minuto después del mismo evento, 3. El ADR de fase que promete el juez no cubre qué pasa cuando dos eventos de fuente distinta (cierre y M15) coinciden en el mismo tick.
4. **Contabilidad tardía produce una operación de más, no solo puntos de pérdida.** Con la contabilidad de cartuchos aplazada un paso dentro del mismo evento (`c06_fase_contabilidad.py`), 4 colocaciones en vez de 3 sobre una zona con cartuchos ya agotados — el riesgo de fase que el juez sí midió, pero solo en puntos porcentuales de pérdida (4,889 %/5,365 %), también produce esta clase de violación.
5. **La contabilidad de costes que el juez lleva a la pregunta cerrada no coincide con lo que construyó.** `spec_h` tiene CUATRO reglas nuevas, no tres (RN-032 sí parte el tope semanal de RN-020, pese a que el juez escribe explícitamente que "no hace falta"); quedan 19 tokens vigentes, no 17; RN-020 conserva en su prosa y su cita una rama que su forma ya no evalúa; y la reescritura de RN-001 quita en silencio la prohibición de `buscar_entradas` durante un freno —vigente hoy en `strategy_spec.yaml:411`— sin que la lista de reescrituras del juez lo mencione ni exista una decisión que lo autorice.

**Ajuste que propone el contra-juez, antes de llevar H al dueño:** (1) sacar la rama SIN CITA `se_marca_liquidez_m15` (y probablemente `alcanza_hora ventana_fin`) de `zona_perdida.caduca_con`, dejando solo la rama citada (`se_completa_zona_de_control fuera_de ESTE`); si el trader decide que una liquidez nueva SÍ libera la zona perdida aunque no esté "afuera", esa decisión debe registrarse como tal, con la cifra medida (hasta 10 stops seguidos), y no colarse bajo la misma cita que protege RN-030; (2) el ADR de método debe fijar explícitamente el orden dentro de un MISMO evento cuando coinciden una pérdida que agota cartuchos y una marca de liquidez, y añadir una guardia que verifique que ninguna combinación de fases permite más de tres colocaciones sobre la misma toma; (3) corregir la contabilidad de costes de H antes de la pregunta cerrada: 4 reglas nuevas (no 3), 19 tokens vigentes (no 17), y decidir si RN-001 debe seguir prohibiendo `buscar_entradas` durante un freno.

**Conclusión de esta sección:** la pregunta cerrada al dueño, tal como la redactó el juez, no está lista para presentarse — su propio artefacto de verificación (la BFS y la copia de `spec_h`) contradice la garantía central que vende ("tres cartuchos por zona") y su tabla de coste tiene tres cifras equivocadas.

### 4.8 Incidencias del proceso

**hecho.** Los cinco laboratorios (d1, escéptico del intérprete, alternativa A, alternativa B, juez, contra-juez) declaran, cada uno por su cuenta, cero escrituras en el repositorio real: comprobado con `find -mmin`/`find *.pyc -newermt` sin resultados nuevos y `git status --short` mostrando solo ` M PROJECT_STATE.md` (ajeno a esta dimensión). Ninguno tuvo exposición a holdout ni a velas de mayo de 2026: todo evento es sintético, con fechas de 2027. Cuatro intentos anteriores del laboratorio d1 se cortaron dejando ficheros casi sin notas; se revisaron y corrigieron antes de reutilizarlos (empates en gate, `candidatas`, desempate en la traza, exploración rota con profundidad 0) — las trazas válidas son las de `trazas_v5/`. La ejecución de las alternativas A y B se cortó por límite de uso y se reanudó desde `NOTAS.md`; en B, tras el corte, `Edit` falló por ficheros no leídos en la sesión, así que los cambios se rehicieron con scripts reproducibles (`aplicar_b.py`, `parchear_interprete.py`) en vez de a mano. `pathlib.write_text` en Windows escribió CRLF en la copia de la spec de B (diferencia medida con `--strip-trailing-cr`). Un `grep -rln` sobre la raíz del repo recorrió `data/` unos 2 minutos antes de pararse con `TaskStop`, sin salida útil; se repitió con la herramienta `Grep`, que respeta `.gitignore`.

### 4.9 Ruta del intérprete desechable

Ninguno de estos árboles está en el repositorio ni se referencia desde él; son de usar y tirar.

- **d1 (base):** `C:/Users/USER/AppData/Local/Temp/botsito-audit/d1-interprete/` — `interprete.py`, `escenarios.py` → `trazas_v5/` (29 ficheros + `s09_*` + `00_resumen.txt`; la carpeta `trazas/` es de un intento anterior sin `candidatas` ni empates de gate, no usar), `experimento_f14b.py` → `f14b_*.txt`/`f14b_resumen.json`, `elecciones.py` → `elecciones.md`, `contar_fijar.py`, `NOTAS.md`.
- **Escéptico del intérprete:** `C:/Users/USER/AppData/Local/Temp/botsito-audit/f14b-esceptico-interprete/` — `variantes.py`, `exp_absorbente.py`, `exp_bfs.py`, `exp_tope.py`, `exp_fase_mismo_tick.py`, `correr_variantes.py`, trazas en `trazas_var/`.
- **Alternativa A:** `C:/Users/USER/AppData/Local/Temp/botsito-audit/f14b-alt-regla/lab/` — `alt/knowledge/spec/strategy_spec.yaml` (copia +362/−30 líneas), `guardias_alt.py`, `literales_alt.py`, `escenarios_alt.py` → `trazas_alt/<modo>/`.
- **Alternativa B:** `C:/Users/USER/AppData/Local/Temp/botsito-audit/f14b-alt-duracion/lab/` — `aplicar_b.py` → `spec_b/`, `parchear_interprete.py` → `interprete.py`, `guardias_hoy.py`, `escenarios_b.py` → `trazas_b/`, `explorar_variantes.py`.
- **Juez:** `C:/Users/USER/AppData/Local/Temp/botsito-audit/f14b-juez/` — `altB/escenarios_h.py` (spec `spec_h`), `fase_tarde.py`, `exp_absorbente.py`, `run_h_bfs.out`.
- **Contra-juez:** carpeta `lab/` sobre una copia de `spec_h` y del intérprete del juez (`c01_marca_sin_toma.py`, `c02_perdida_y_marca.py`, `c05b_bfs_por_dia.py`, `c06_fase_contabilidad.py`); **sin_verificar** — los datos no citan la ruta absoluta completa de esta carpeta, solo rutas relativas a `lab/`.

Orden típica de ejecución (d1): `cd .../d1-interprete && PROF=40 MAXEST=6000 "/c/Users/USER/Desktop/Bot v3/.venv/Scripts/python.exe" escenarios.py`; las demás carpetas usan el mismo intérprete de `/c/Users/USER/Desktop/Bot v3/.venv/Scripts/python.exe` sobre sus propias copias de la spec.


## 5. Fidelidad: lo que el trader hace y ninguna regla cubre

**Hecho.** El barrido cubrió 356 items de evidencia vivos, 73 registros de feedback vivos y las 25 reglas vigentes (28 con las 3 descartadas). Por contenido: 119 items cubiertos por una regla, 23 por una ambigüedad, 61 superados o descartados, 83 no operativos (ideas, meta, backtest) y **70 comportamientos operativos que no llegan a ninguna regla ni ambigüedad**, concentrados en entrada (23), liquidez (17) y mapeo (10) [d2-fidelidad-huecos, anexo §3]. Por cita pura, 139 de 176 items `RULE_STATEMENT` no los cita ningún fichero de `knowledge/spec`. Aparte, las 12 citas de RN-001..RN-013 (sin RN-003) y las 10 de RN-015..RN-028 existen, ninguna está supersedida y todos los literales aparecen en su registro citado: `spec check` da OK en los dos barridos [d2-literal-a, d2-literal-b]. El fallo no está en la existencia de la cita — está en lo que cada regla construye encima, y en lo que nadie escribió.

Todo lo que sigue se lee contra la pregunta que ordena la auditoría: ¿qué impide hoy, por su nombre, empezar a escribir el motor (F18-F24) sin tener que rehacerlo? Las tres partes de esta sección responden que no: hay comportamientos del trader sin regla, geometría que ninguna regla sitúa en precio, y afirmaciones de la spec que su propio literal no sostiene.

### 5.1 Lo que el trader hace y ninguna regla cubre

#### a) No existe la regla de entrada — [d2-fidelidad-huecos-01] — grave, MATIZADO, mueve la aguja

**Hecho.** Las 13 acciones del vocabulario (`strategy_spec.yaml:214-253`: fijar, cerrar_a_mercado, reubicar_orden_limite, mover_stop, agrupar_estructura, dimensionar_lote, escribir_stop_en_la_orden, fijar_objetivo, realizar_perdida, gestionar_salida, reentrar, redondear_lote, abstenerse) no incluyen ninguna que coloque una orden límite inicial. El predicado `se_da_esquema` (`:121-134`) solo aparece NEGADO, dentro del `ninguno_de` de RN-008 (`:581-586`). RN-011 (`:664-677`) reacciona al evento `se_coloca_orden_limite`, que ninguna regla produce.

```
$ python.exe s2/forma.py
RN-008 gate cuando= ['NO se_da_esquema', 'NO se_da_esquema'] prohibe= ['abrir_operacion']
RN-011 disparador cuando= ['se_coloca_orden_limite'] hace= ['dimensionar_lote', 'escribir_stop_en_la_orden', 'fijar']
predicados nunca en positivo: ['en_ventana', 'se_da_esquema']

$ botsito.exe --repo <repo> spec check
OK: 28 reglas de spec (25 vigentes, 24 con forma ejecutable), 10 terminos de glosario, hash del manifiesto al dia
```

El gesto que el trader describe una y otra vez no tiene regla que lo produzca: ev-v3-004201-bfeb3734 (v3 0:42:01) «Con el breaker ya me basta [...] apenas el breaker, o sea, marco mi orden limit y ya está»; ev-v1-000359-b0756c35 (0:03:59) «esperarías el breaker de aquí para que puedas entrar»; ev-v1-002740-7c96436f (0:27:40) «lo ideal y lo lógico sería tomarlo desde aquí, o sea, apenas se genere el breaker». **Hecho.** Un voto de contexto elevó esto a CONFIRMADO por lectura directa; el dictamen final que rige queda en MATIZADO porque la severidad se mantiene "grave" sin variación de fondo. Un motor que implemente la spec y nada más no coloca nunca una orden: cero operaciones, y F26 no tendría nada que comparar.

#### b) RN-005 prohíbe operar justo donde el trader opera — [d2-fidelidad-huecos-02, d2-literal-a-01] — grave, CONFIRMADO, mueve la aguja

**Hecho, confirmado en dos rondas de escéptico sin refutación posible.** RN-005 (`strategy_spec.yaml:495`) prohíbe «el precio se desarrolla por debajo de la liquidez de M15 en sesgo alcista, o al revés», y el predicado `esta_al_otro_lado_de` (`:109-110`) lo repite. Su cita (ev-v3-001600-ed45b091, v3 0:16:00) es un ejemplo con sesgo H4 **bajista** (v3 0:15:11 «Vela bajista envuelve a la vela anterior [...] alta probabilidad de que continúen»), en el que la liquidez de M15 está por ENCIMA (fotograma fr-v3-982da728/970000 y /1010000: línea "m15 lq" por encima del precio, panel 4H en rojo) y la operativa válida es «por encima» (0:16:30, 0:17:30).

```
$ botsito corpus transcript show --video v1 --t0 0:11:35 --t1 0:13:45 --capa cruda
[0:11:43] ... nuestro enfoque tiene que ser alcista
[0:13:12] Nuestra operativa tiene que estar por debajo
[0:13:40] ... yo buscaría que el precio llegue por debajo y me haga el esquema

$ botsito corpus transcript show --video v6 --t0 0:18:20 --t1 0:19:40 --capa cruda
[0:18:51] nosotros ya trazamos nuestra liquidez por encima [sesgo bajista]
```

En sesgo alcista (v1) el trader opera por debajo de la liquidez; en sesgo bajista (v3, v6) opera por encima. RN-005 prohíbe exactamente eso en los dos sentidos: «por debajo [...] en sesgo alcista, o al revés». Nada lo declara — ni ADR, ni PROJECT_STATE, ni ambigüedad — y la redacción es de 85de674 (2026-09-09), sin tocar desde entonces. Como `sesgo` solo lo consume RN-005 (`:327`), es el único filtro direccional de toda la spec, y está al revés. Implementada tal cual, RN-005 es un gate que veta las dos direcciones del trader: el bot no opera, o solo opera en el lado que el trader llama ruido («por debajo de esta liquidez de m15 es ruido», v3 0:16:14).

#### c) No existe cancelar una orden pendiente — [d2-fidelidad-huecos-07] — media, MATIZADO, mueve la aguja

**Hecho.** `orden_limite_pendiente` (`:328-331`) solo se apaga en un sitio, RN-013 al llenarse la orden (`:741`). Ninguna de las 13 acciones retira o hace expirar una orden ya enviada al broker. Los gates solo prohíben `abrir_operacion` («colocar una orden o abrir una posición nueva»), no dicen qué hacer con una límite que ya está en el mercado.

```
$ grep -rniE 'cancel|anular la orden|retirar la orden|quitar la orden|borrar la orden' \
  knowledge/spec knowledge/evidence knowledge/feedback docs/adr docs/plan docs/spec docs/HANDOFF.md
(sin coincidencias con un concepto de cancelación)
```

Situaciones del trader que exigen que la orden desaparezca y no llegan a regla: ev-v3-005147-53e7d7e4 «esta sería mi orden límite que no llega a romperlo [...] no hay entrada»; ev-v4-003619-137f4ffb «no se desarrolla el esquema [...] entonces no hay entrada»; el giro de sesgo de las 11:00; la ventana de noticias de RN-028 (sin forma, A-17). Una compra límite viva a las 15:00 se llenaría fuera de ventana, o dentro de la ventana de noticias que RN-028 quiere bloquear — con la sanción de FundedNext sobre la cuenta aunque la operación cierre en ganancia (ADR-0022).

#### d) Ninguna regla impide una segunda orden pendiente en paralelo — [d2-literal-b-05] — media, MATIZADO, mueve la aguja

**Hecho + inferencia** (de que la forma solo cuenta posiciones y de que el hueco anterior no cancela pendientes). El trader, ante la pregunta explícita «¿las entradas pueden darse en paralelo?», responde que no (v4 0:36:40-0:37:23). RN-018 (`:855-874`) solo prohíbe `abrir_operacion` cuando las **posiciones vivas** llegan a `operaciones_simultaneas_max`; el único predicado que lee es `operaciones_abiertas_alcanzan` («el número de posiciones vivas», `:69-70`). El hecho `orden_limite_pendiente` solo lo consume RN-006 para reubicar. Con una límite pendiente y 0 posiciones abiertas, ningún gate impide colocar una segunda pendiente, y si hay dos, el broker las llena sin volver a pasar por el gate. Riesgo con dinero: dos posiciones de 0,5 % en paralelo sobre el mismo movimiento son 1 % correlado donde el trader arriesga 0,5 %.

#### e) Nadie dice cuándo se congela la caja: la reubicación no redimensiona — [d2-fidelidad-huecos-04] — grave, MATIZADO, mueve la aguja

**Hecho.** Tres instantes candidatos y la spec usa los tres sin elegir: colocación (RN-011 dimensiona lote y escribe stop en `se_coloca_orden_limite`, cuya descripción promete además «su objetivo», `:151-152`); reubicación (RN-006, `reubicar_orden_limite: argumentos: [a, cadencia]`, `:221-223` y `:542` — sin lote, stop ni objetivo, y sin decir si reubicar vuelve a disparar RN-011); llenado (RN-013 escribe el stop «antes de que se active» **dentro** del evento `se_activa_entrada`, `:736-741`).

```
RN-006 disparador cuando= ['hecho:orden_limite_pendiente', 'se_completa_zona_de_control'] hace= ['reubicar_orden_limite']
RN-011 disparador cuando= ['se_coloca_orden_limite'] hace= ['dimensionar_lote', 'escribir_stop_en_la_orden', 'fijar']
RN-013 disparador cuando= ['se_activa_entrada'] hace= ['escribir_stop_en_la_orden', 'fijar', 'fijar']
```

El trader recalcula al mover la orden: ev-v4-002807-dd5f3718 (0:28:07) «voy ahí bajando bajando bajando, pero claro, para entrar con lotaje pues te tienes que poner a calcular»; ev-v4-002901-771b0402 (0:29:01) «ibas moviendo el SL, pues se calculaba». Ninguno de los dos está citado en `knowledge/spec`. **Impacto con dinero:** sobre la única caja con precios documentada (4,667 pips), un pip de reubicación sin recalcular mueve el lote entre 18 y 27 %.

#### f) Lo que el trader exige tras cerrar una operación no llega a regla — [d2-fidelidad-huecos-09] — media, MATIZADO, mueve la aguja

**Hecho.** Tras una GANADORA el trader espera liquidez nueva antes de seguir: ev-v6-003227-c4efcf49 (0:32:27,6) «ya aquí está el trade ganador, aquí no buscamos nada [...] tenemos que esperar nuevamente a que se desarrolle la liquidez». RN-017 (`:835-853`) permite `buscar_entradas` de inmediato, «con el límite de cartuchos intacto», y como `cartuchos_reinicio = siguiente_liquidez_m15`, esperar liquidez nueva también reiniciaría el contador: la regla y el trader discrepan en las dos cosas. Tras un STOP con cartuchos vivos el trader exige una zona de control nueva y **fuera** de la anterior: ev-v4-003820-299d7a15 (0:38:20) «no puedes volver a entrar hasta que nuevamente [...] se cierre esta zona de control y te genere otra [...] tiene que ser nuevamente afuera». Ninguna regla lo pide, y `liquidez_tomada` no se apaga por ningún mecanismo (dato ya confirmado en 3.1.4). Es deuda **declarada**: `docs/validation/AUDITORIA-2026-09-12-material.md` §2.1 y `docs/plan/features/F14b-ciclo-de-vida-de-los-hechos.md` §3 la nombran como propuesta no aplicada, bloqueada por la decisión de método que también bloquea F14.

#### g) El sesgo persiste, pero ninguna forma dice cuánto dura ni cuál es su valor inicial — [d2-fidelidad-afirmaciones-03, d2-fidelidad-afirmaciones-04] (afirmación 3.3.15) — media, MATIZADO, mueve la aguja

**Hecho + inferencia.** El hecho `sesgo` (`:321-327`) solo lo produce RN-003 (ruptura de la H4 previa) y solo lo consume RN-005. El trader describe un sesgo que se mantiene durante varias velas hasta la ruptura: v6 1:03:48-1:04:05 «terminó el cista, pero seguimos buscando bajistas [...] hasta que [...] el precio debería de generar un breaker por encima»; v3 1:09:48 «no operaríamos alcistas independientemente si aquí es rojo rojo rojo verde». **Corrección del escéptico (enunciado que rige):** la forma de RN-003 solo fija el hecho cuando la vela H4 previa rompe, y solo se evalúa al abrir cada sesión (07:00 y 11:00 Madrid); como los hechos son estado persistente por construcción (ningún mecanismo apaga `sesgo`, dato ya confirmado en 3.1.4), una vela sin ruptura NO deja el sesgo sin fijar — conserva el valor anterior, que es lo que dice el literal. Lo que de verdad falta, y que ni el auditor original ni la primera lectura vieron, son dos huecos reales: (1) el **valor inicial** — `hechos.sesgo` no tiene ninguno, así que el primer día, o tras cualquier reinicio sin historial, el sesgo no existe hasta la primera ruptura, y ninguna regla dice qué hacer mientras tanto; (2) la **envolvente** — con `sesgo_h4_criterio_ruptura = mecha`, una vela que rompe por mecha los dos extremos de la anterior deja `sentido_de_la_ruptura` sin ganador, y el propio trader la nombra como complicación: v3 1:16:07-1:16:33 «aquí hay variaciones [...] no considerar que a veces se envuelva [...] no tratar de buscar [...] a ver si envuelve». La salida que el trader ofrecía (tomar el color de la vela) la descartó la sesión 1 (fb-...-41f46b21: «Descarta la simplificación 'color de la vela anterior'»). Ninguna de las 23 ambigüedades trata el caso. El primer día del bot, o tras un reinicio sin sesgo reconstruido, el filtro direccional queda apagado y ninguna regla lo impide.

#### Cuadro resumen del 5.1

| Hueco | Regla más cercana | Cita del trader | Dictamen | ids |
|---|---|---|---|---|
| No hay acción que coloque la orden límite | RN-008 (niega), RN-011 (reacciona a un evento inexistente) | v3 0:42:01 «marco mi orden limit y ya está» | MATIZADO, grave | [d2-fidelidad-huecos-01] |
| RN-005 invierte el lado de la liquidez | RN-005 | v1 0:13:12 / v3 0:16:30 / v6 0:18:51 | CONFIRMADO, grave | [d2-fidelidad-huecos-02, d2-literal-a-01] |
| No existe cancelar una orden pendiente | ninguna | ev-v3-005147-53e7d7e4 | MATIZADO, media | [d2-fidelidad-huecos-07] |
| Nada impide una segunda pendiente en paralelo | RN-018 (solo posiciones) | v4 0:37:10 «ya la respuesta es no» | MATIZADO, media | [d2-literal-b-05] |
| Nadie dice cuándo se congela la caja | RN-006/RN-011/RN-013 | ev-v4-002807-dd5f3718 | MATIZADO, grave | [d2-fidelidad-huecos-04] |
| Tras ganar/perder, condición de reentrada no recogida | RN-017 (contradice), RN-016 | ev-v6-003227-c4efcf49 / ev-v4-003820-299d7a15 | MATIZADO, media | [d2-fidelidad-huecos-09] |
| Sesgo: valor inicial y envolvente sin declarar | RN-003/RN-005 | v3 1:16:07-1:16:33 | MATIZADO, media | [d2-fidelidad-afirmaciones-03, -04] |

### 5.2 La geometría que no existe

El dueño pregunta, para cada pieza de geometría, si el motor puede escribirse sin inventarla. La respuesta es no en las seis.

#### Liquidez de M15 — [d2-fidelidad-huecos-05] — grave, MATIZADO, mueve la aguja — ¿motor sin inventar?: **No**

**Hecho.** El token `liquidez_m15` (`:290-291`) solo tiene descripción («la liquidez marcada en M15 que hay que tomar antes de mirar M1»); RN-004 la trata como dada. De los 15+ items que describen qué nivel es la liquidez, **cero** están citados en spec, glosario, parámetros o ambigüedades (`ambiguedades.yaml` acaba en A-23; las A-24/25/26 que `F14b` §1.2 propone abrir no existen como entradas formales). El corpus da candidatos incompatibles: «la zona de liquidez tiene que ser la más reciente» (ev-v1-001334-96e8ca40); «el alto más alto [...] sería la liquidez» en un pullback complejo (ev-v3-001242-cbe6bdc3); «la zona de liquidez más baja, que me deja el precio» (ev-v3-001531-1b12a896); «por encima de este ya formado» (ev-v4-005053-885e2773). Ya está declarado en `AUDITORIA-2026-09-12-material.md` §2.3 y en `F14b` §1.2 como propuesta sin aplicar; lo que aporta este barrido es que, contado hoy, ninguna pieza que lo resolvería está citada, y que RN-004 tampoco está bajo el gate de ventana de RN-001, así que no hay ventana de búsqueda declarada.

#### Nivel 0 y nivel 1 de la caja — [d2-fidelidad-afirmaciones-01, d2-fidelidad-afirmaciones-02, d2-fidelidad-huecos-03] — grave, MATIZADO, mueve la aguja — ¿motor sin inventar?: **No**

**Hecho.** Todos los precios de una operación son fracciones de la caja: el lote (RN-011, `hasta stop_fraccion_caja`), el stop (RN-013), el objetivo (RN-015, `caja_completa`) y el break even (`OP.precio_entrada`). `glossary.yaml:96-108` define la caja como «la distancia entre la entrada y el extremo del stop inicial», y «stop inicial» no aparece en ningún otro fichero de `knowledge/spec`, `docs` ni `src` fuera de esa línea y su copia generada:

```
$ grep -rn -i 'stop inicial|stop_inicial|extremo del stop' knowledge/spec docs/adr docs/spec docs/plan docs/HANDOFF.md src
-> solo glossary.yaml:99 y docs/spec/glosario.md:21 (generado)
```

**Corrección del escéptico (enunciado que rige, afirmación 3.3.16):** no es un círculo lógico en sentido estricto — es un ancla sin definir. El literal citado por la definición (ev-v2-003336-fc210a05, «yo calculo mi lotaje desde aquí [...] lo pongo en 0.75 y estoy guardándome 0.25») no describe la caja ni sus extremos; sostenía la definición ANTERIOR («el lotaje se calcula sobre la caja completa y el stop se mueve al 0,8»), que F12 (commit 59b16f6, 2026-09-12) reescribió sin cambiar la cita. Los tres items que sí describían los extremos de la caja se sustituyeron el 2026-09-12 (commit 2003e61) por items que solo corrigen 0,75 a 0,80: ev-v2-003142-beb4ad3c «desde el punto anterior, bueno, anterior y el final» → ev-v6-021939-1c7cad28 (solo el número); ev-v4-001207-0c4ffd4b «el stop loss se pone hasta el final como del rango» → ev-v6-021939-b430a110 (solo el número); ev-v1-000448-346d6d90 «desde aquí hasta aquí» → ev-v6-013508-b4c88d87 (solo el número). Quedan en la cruda, no citables como evidencia activa.

**Sobre el nivel 0:** ningún texto de la spec dice «nivel 0 = entrada»; se deduce de `lotaje_base` («la distancia del nivel 0 a stop_fraccion_caja», `parametros.yaml:561`) y del único dato con precios (fotograma v4 0:12:30, FX Replay 30-ene-2026: nivel 0 = 1,19502 = entrada, nivel 0,75 = 1,19537), pero la ficha que el trader confirmó en v3 1:03:49 lee «Caja de Gann nivel 0,75 como umbral de invalidación y optimización del stop» (fotograma v3/003829000.png) — el umbral es el 0,75, no el 0, así que la lectura queda **coherente** con el fotograma de v4, y la "unica frase del corpus" que el auditor original leyó como contradictoria («nivel 0 con un bral de invalidación», ASR de v3 1:03:49) es el ASR leyendo mal esa misma fila en pantalla. `docs/HANDOFF.md:106-107` declara por qué la spec no escribe «nivel 0» («las reglas no admiten cifras [...] se escribe "la entrada" y "el extremo de la caja"»). Con todo, ningún fichero de `knowledge/spec` dice a qué **precio** exacto va la orden límite dentro de la estructura: ev-v4-010605-a11249c0 (v4 1:06:05) responde a la pregunta del formulario exacta sobre esto («¿la orden va en el borde de arriba, en el medio o el borde de abajo?») con «siempre se toma en la mecha», y la vela queda deíctica («en este caso iría aquí»). El nivel 1 (el extremo) tiene tres descripciones incompatibles en el corpus, ninguna citada: «desde el punto más abajo te genera la vela contraria» (ev-v1-001454-69cebe62, 0:14:54); «del punto más alto al punto más bajo» (ev-v3-004353-b7661782, 0:43:53).

**Impacto con dinero (hecho, aritmética de `docs/validation/F05-frame-extraction.md:178`):**

```
nivel 0 = 1,19502 ; nivel 0,75 = 1,19537  ->  caja = 4,667 pips
riesgo 0,5% de 100.000 -> lote 13,39 ; objetivo 14,00 pips
un pip mas lejos: lote 11,03 (-17,6%) ; objetivo 17,00 pips
un pip mas cerca: lote 17,05 (+27,3%) ; objetivo 11,00 pips
```

Dos implementaciones razonables de F21 (extremo del order block vs. extremo de la zona de control) dan lotes y objetivos distintos en cada operación, y el default que se elija sería una decisión de negocio no declarada.

#### Zona de control: sin frontera, y "limpia" (A-21) sin cuantificar — [d2-fidelidad-huecos-08, d2-literal-a-04] — media, MATIZADO/CONFIRMADO, mueve la aguja — ¿motor sin inventar?: **No**

**Hecho.** El glosario define «zona de control» como «el tramo que el precio deja antes de romper. Se da por COMPLETADA cuando rompe el punto extremo anterior» (`glossary.yaml:55-63`), sin decir dónde empieza ni qué es «el punto extremo anterior». RN-009 (`:592-613`) **cuenta** zonas («dentro del mismo esquema se desarrollan más zonas de las que admite», tope 1, literal WhatsApp «solo 1 zona control bro. si hay 2 se descarta»), y RN-006 **reubica** en cada zona completada, pero [d2-literal-a-04, CONFIRMADO] el predicado `zonas_desarrolladas_superan` (`:135-139`) solo tiene el argumento `[tope]` — sin `depende_de`, sin alcance por esquema, sin reinicio — mientras el trader describe reubicaciones sucesivas dentro del mismo montaje (v6 1:28:52-1:29:03 «vamos actualizando aquí y luego aquí»; v1 0:13:58 «vamos ahí bajando el límite bajando el límite»). Leídas juntas, la segunda reubicación de RN-006 podría ser la segunda zona que RN-009 debía haber descartado, y nada lo dice.

Sobre A-21 («zona limpia»): el corpus no la cuantifica — `kb find limpi --prefijo` da 12 apariciones y ninguna habla de velas, pips o número de zonas; la única frase que aplica «limpia» a una zona de control (v1 0:14:35) dice que esa zona «no haga mucho ruido», sobre su calidad, no sobre cuántas hay. `ambiguedades.yaml` (A-21) y `ADR-0019:111` afirman que «limpia» es «lo único de la geometría de entrada que sigue siendo cualitativo»: los hallazgos de esta sección (liquidez M15, nivel 0/1, breaker M1, frontera de zona de control) desmienten esa afirmación — hay más geometría cualitativa que esa.

#### Segundo esquema de entrada — [d2-fidelidad-huecos-08, d2-fidelidad-afirmaciones-05] — menor/media, MATIZADO, mueve la aguja — ¿motor sin inventar?: **No**

**Hecho.** Definido en prosa: «con un pequeño retroceso, pequeña zona de control y luego rompe» (ev-v4-000243-5f8875ce, `glossary.yaml:46-53`, predicado `se_da_esquema`). Sin frontera con el «retroceso complejo» que lo invalida (ev-v3-004942-7dabf446, «hay demasiadas zonas de control e invalida») ni con «genera un flujo de órdenes» (ev-v5-000038-6570a65f); «decisional» (ev-v5-000155-d079ac35) es un término que nadie define. RN-014 exige, para el break even, una zona `distinta_de: OP.zona_de_entrada` (`:271-272, 760-764`), y el **primer** esquema entra sin retroceso ni zona de control propia («Yo no espero ningún retroceso [...] con el breaker ya me basta», v3 0:42:01-0:42:30): el token `zona_de_entrada` no tiene contenido claro para la mitad de las entradas. La lectura del escéptico (afirmación relacionada, 3.3.17) matiza que el trader sí describe el disparador del break even como «otra zona de control» distinta y posterior en v6 (0:06:05, 0:21:28, 0:42:22: «La condición es que después de la entrada, desarrolle otra zona de control y ponemos en break-even»), y que ese disparador tiene soporte en items de otros videos (ev-v4-013122-d24f9c5e, ev-v4-004447-bc2e74ee) — el problema no es que la exigencia sea inventada, sino que no está definida qué estructura hace de "zona de entrada" en el primer esquema, y que el esquema de regla solo admite una cita, así que RN-014 no puede citar a la vez el QUÉ (otra zona de control) y el CUÁNDO (fb-0ccafcba, «apenas toca»).

#### Breaker de M1 — [d2-fidelidad-huecos-06, d2-literal-a-03] — grave, MATIZADO, mueve la aguja — ¿motor sin inventar?: **No**

**Hecho.** Tres piezas sin definir. (1) *Qué se rompe*: el mapeo de pivotes en M1 vive en 10 items del corpus, 9 sin citar en ningún fichero de spec: «la vela contraria [...] apenas se inicia [...] ya lo tomo como un punto» (ev-v4-005749-1e9325cb); «una vela roja marca un mínimo» (ev-v3-011540-5425b533, la única con cita, A-8/RESUELTA). RN-007 (`:547-561`) solo agrupa velas en un «order block mayor» sin nombrar la temporalidad. Su literal (fb-...-7ee9cabc) **solo corrige el término** de la hoja del consultor («creo que no sería el término adecuado [...] sería considerado una estructura»); ni `order_block_mayor` ni «el resto se trata como ruido» salen de esa cita — el segundo viene de ev-v3-010648-0039e34d, que RN-007 no cita [d2-literal-a-03]. (2) *Qué es el bloque de origen*: el formulario preguntó exactamente esto (v3 1:12:23) y la respuesta fue sobre BOS contra CHoCH, no sobre velas. (3) *Con qué criterio*: «mecha o cuerpo» está horneado en la descripción de `se_da_esquema` (`:121-127`) en vez de vivir en un parámetro — a diferencia de `liquidez_m15_criterio_toma`, que sí existe para M15 — y contradice un item que el propio trader **confirmó por escrito** en la sesión 1: fb-2026-09-09-sesion-01-9deda56d, «SI (una rotura con mecha no valida el trade)» sobre ev-v4-005319-dee95093 («mira aquí en m1 [...] me rompe aquí con mecha no hay validez»), frente a v4 0:59:53 «el breaker tiene que ser con cuerpo» y v6 0:38:05 «en M1 [...] es indiferente». Ese CONFIRM no está citado en spec, ambigüedad ni glosario.

```
$ botsito corpus transcript show --video v4 --t0 0:58:50 --t1 1:00:30 --capa cruda
[0:59:18] Claro, como te decia, en M1 / [0:59:20] Pues es valido con mecha o con cuerpo
[0:59:53] Claro, cuando hay breaker / [0:59:56] Tiene que ser con cuerpo en M1
```

Entre «toca con mecha» y «cierra con cuerpo» la entrada cambia de vela y de precio; sobre 48-60 operaciones al mes, dos implementaciones razonables de F18 marcan breakers distintos sobre las mismas velas.

### 5.3 Lo que la spec afirma sin que el literal lo sostenga (regla por regla)

| Regla / pieza | Cita | Lo que la forma o la prosa afirma | Lo que sostiene el literal | Dictamen (severidad) | ids |
|---|---|---|---|---|---|
| RN-005 | ev-v3-001600-ed45b091 | prohíbe abrir «por debajo [...] en sesgo alcista, o al revés» | ejemplo con sesgo bajista; el trader opera justo en el lado que la regla prohíbe (ver 5.1.b) | **CONFIRMADO**, grave | [d2-fidelidad-huecos-02, d2-literal-a-01] |
| `equal` (RN-010 causa / RN-016, RN-019 resultado) | fb-9626d3dd / fb-aa2abe65 / fb-060cd801 | resultado de cierre «sin ganancia ni pérdida» (token), usado además como causa de activación y como geometría | v6 1:23:13-1:23:19: el equal que saca la entrada «te genera una pérdida»; RN-019 no dispararía en ese caso real y RN-016 gastaría cartucho | MATIZADO, grave | [d2-literal-a-02, d2-literal-b-01] |
| Break even como resultado | RN-014 (`:745-769`) / RN-016 | RN-016 excluye el BE del contador («un intento no es considerado un break even», fb-aa2abe65) | no existe token `break_even`; los únicos resultados son `equal`/`ganancia`/`perdida`; el stop va exacto a `OP.precio_entrada` sin colchón, y con comisión el neto puede cerrar en negativo (no hay parámetro de comisión ni de colchón: grep vacío) | MATIZADO, grave | [d2-literal-b-02] |
| RN-020 (tope semanal 9 %) | fb-a85b6bc7 (síntesis del consultor) | `perdida_maxima_semanal=9` sobre `saldo_actual`, reinicio semanal | la grabación (v6 2:05:44-2:05:59, marcada `<no_habla>`) dice «El 10% se quedó en la cuenta [...] vamos a ponerle 9%», atándolo al límite del 10 % de la cuenta; no aparece «semana» ni «cuenta actual»; no hay parámetro de pérdida total | MATIZADO, grave | [d2-literal-b-03] |
| RN-003 (sesgo) | fb-8eccf5c0 | «si no genera un rompimiento [...] seguiríamos operando bajista» | sostenido — ver corrección en 5.1.g (persistencia sí implícita; faltan valor inicial y envolvente) | MATIZADO, media | [d2-fidelidad-afirmaciones-03, -04] |
| Caja (glosario) | ev-v2-003336-fc210a05 | «distancia [...] al extremo del stop inicial» | el literal habla de calcular el lote «desde aquí» y del 0,75/0,25; no describe extremos ni «stop inicial» — ver 5.2 | MATIZADO, grave | [d2-fidelidad-afirmaciones-01, -02, d2-fidelidad-huecos-03] |
| RN-014 (zona distinta y posterior) | fb-0ccafcba | «se pone al romperse la zona de control posterior», `distinta_de`/`posterior_a` | el literal citado responde a TOCAR-frente-a-CIERRE («apenas toca»), no a qué zona; el QUÉ sí lo dice el trader en v6 (0:06:05, 0:21:28, 0:42:22) pero sin item propio en ese video, y el esquema de regla solo admite una cita | MATIZADO, media | [d2-fidelidad-afirmaciones-05, -06] |
| RN-004 (marco de la vela) | fb-6e15504f | «una vela cierra con cuerpo al otro lado» | ni la regla, ni el parámetro, ni el glosario dicen si es la vela de M15 o de M1; el corpus apunta a los dos (v6 0:38:00 «solo en m15»; v4 0:15:35, ejemplo en gráfico de 1 minuto) | MATIZADO, media | [d2-literal-a-06] |
| RN-007 (mapeo M1) | fb-7ee9cabc | agrupa velas en `order_block_mayor`, «el resto es ruido» | el literal solo corrige un término de la hoja; ni el criterio ni «el resto es ruido» salen de esa cita — ver 5.2 (breaker M1) | MATIZADO, media | [d2-literal-a-03] |
| RN-006 / RN-009 (alcance del contador) | fb-6b29059d / fb-1b2203b0 | RN-006 reubica «al completarse cada zona»; RN-009 descarta con 2 «dentro del mismo esquema» | el predicado `zonas_desarrolladas_superan` no liga el conteo a ningún esquema ni declara reinicio — ver 5.2 (zona de control) | **CONFIRMADO**, media | [d2-literal-a-04] |
| RN-011 (nivel del SL en la orden) | fb-76fd91ba (REFERIDA) | el SL nace en la orden al 0,8 desde la colocación | el literal sostiene «el SL se pone junto a la orden límite», no el nivel 0,8 en ese instante (eso es ADR-0020); «un hueco no puede saltar al stop de rango completo» es inferencia del consultor | MATIZADO, media | (nota en anexo d2-literal-a) |
| RN-012 (pérdida "entera y sin fracción") | fb-17ed6193 (REFERIDO) | «la pérdida es [...] entera y sin fracción» | el literal solo sostiene la base del lote; RN-027 redondea el lote a la baja, así que la pérdida real es menor o igual al nominal por construcción, y un deslizamiento la hace mayor | MATIZADO, menor | [d2-literal-a-05] |
| RN-013 (instante del stop) | fb-bc829942 | escribe el stop «antes de que se active», ejecutado dentro de `se_activa_entrada` | el literal sostiene el NIVEL (0,80 en los dos esquemas), no el instante; contradicción interna en la propia regla | **CONFIRMADO**, menor | [d2-literal-a-07] |
| RN-015 (instante y base del objetivo) | fb-7fbbb2e7 | «se traza con la orden», forma dispara en `se_activa_entrada` (llenado); base `caja_completa` justificada porque «el stop todavía no se ha movido» | RN-011 ya escribe el stop en la orden desde la colocación (A-11); en ese instante ya existen las dos distancias, así que el argumento de la base no discrimina; RN-011 no escribe objetivo | MATIZADO, media | [d2-fidelidad-afirmaciones-07, d2-literal-b-04] |
| RN-018 (paralelas) | ev-v4-003710 | «no hay entradas en paralelo» | el literal sí lo sostiene para posiciones; la forma no cubre pendientes — ver 5.1.d | MATIZADO, media | [d2-literal-b-05] |
| RN-021 (spread) | fb-3565552d | «el spread no se filtra» | la cita y el literal son de `filtro_noticias`, no mencionan spread; el registro que sí trata spread (fb-672262d5) no está citado en RN-021 | MATIZADO, menor | [d2-literal-b-06] |
| RN-021/RN-028 (regresión de aplicación) | fb-3565552d | — | ese registro hace fallar `feedback apply --sesion 2026-09-09-sesion-01 --check` desde el commit del ADR-0022 (antes daba exit 0); no documentado en ningún `.md` | MATIZADO, menor | [d2-literal-b-07] |
| RN-002 (cierre 15:00) | fb-ffb528d7 (síntesis del consultor) | «se cierra a mercado» | el literal («la operativa se cierra a las 3pm») no nombra posiciones abiertas; sí existe una frase del trader que lo dice (ev-v4-011514-fe34ac7e) y la regla no la cita | MATIZADO, menor | [d2-literal-a-08] |
| RN-001 (frenos de riesgo) | fb-8741c388 | forma incluye `detenido_por_tope` y `detenido_por_cartuchos` | ni cita, ni prosa, ni notas de RN-001 los mencionan; solo el mensaje del commit fe9ee21 lo explica (aunque la sección `hechos` de la spec sí lo declara) | MATIZADO, menor | [d2-literal-a-09] |
| RN-026 (token de distancia mínima) | fb-c698bc6a | compara `stop_o_limite` | el token se describe como «el stop o el objetivo»; el enunciado y el parámetro dicen «stop o límite» (la orden límite, en el resto de la spec); tres redacciones incompatibles | MATIZADO, menor | [d2-literal-b-08] |
| RN-027 (gate sin `prohibe`) | fb-17ed6193 | redondea el lote a la baja | es el único gate vigente con forma que no prohíbe nada; `comprobar_forma` no exige `prohibe` a un gate | **CONFIRMADO**, menor | [d2-literal-b-09] |
| `cartuchos_reinicio` | fb-e3eedcaa | reinicio = `siguiente_liquidez_m15` | el literal de la fuente solo dice «3 pérdidas»; el reinicio por M15 viene de otro item (ev-v3-005617-f9d41904, «2 pérdidas»), citado solo en las notas, como confirmación tácita | MATIZADO, menor | [d2-literal-b-10] |
| Literales "cruda leída" fuera de la cruda | fb-694ec50a / fb-6e15504f | RN-001 cita «7AM»; RN-004 cita una pregunta reescrita | la cruda y la corregida de v6 dicen «7M», no «7AM»; la pregunta de RN-004 no está en la cruda tal cual. Barrido: 11 de 28 registros de vídeo fuera de la cruda en ±5 s | MATIZADO, menor | [d2-literal-a-10] |

**Hecho, transversal a la tabla:** ninguna de las 7 guardias semánticas (`comprobar_literales`, `comprobar_contra`, `comprobar_decisiones`, `comprobar_precedencia`, `comprobar_consumo`, `comprobar_citas_revocadas`, `comprobar_forma`) compara el literal contra la `forma` ejecutable de una regla, ni contrasta el `respuesta_literal` de un registro de vídeo con su transcripción — comprueban presencia de texto, no atribución ni consistencia con el efecto que la regla produce. Esto explica por qué 15 de las 21 filas de la tabla pasan `spec check` en verde: la guardia mira la cita, no lo que la regla hace con ella.

**Hipótesis abierta** (cómo se comprobaría): si el motor implementa las formas ejecutables tal cual están hoy —RN-005 invertida, `equal` con la definición de resultado, RN-020 con reinicio semanal, RN-015 disparando en el llenado— produciría un patrón de operaciones observable y distinto del trader (cero entradas o entradas en el lado de ruido, reentradas en el caso equivocado, un tope semanal que no protege la cuenta). Se comprobaría construyendo el intérprete de juguete de d1 sobre estas formas y comparando su traza contra un día del corpus con sesgo y liquidez conocidos; hoy no se ha ejecutado ningún intérprete (declarado como no verificado en d2-fidelidad-huecos y d2-fidelidad-afirmaciones).

### Nota de método

Las cuatro dimensiones que alimentan esta sección (d2-fidelidad-afirmaciones, d2-fidelidad-huecos, d2-literal-a, d2-literal-b) entregaron su barrido completo, con anexo y lista de no verificados; ninguna cayó. Todas declaran lo mismo por separado: cero escritura en el repositorio original, cero apertura de `knowledge/cases/holdout` y cero ejecución sobre velas de mayo de 2026. d2-literal-a declara una excepción menor y ya evaluada por el propio orquestador: leyó cifras agregadas de mayo ya publicadas en ADR-0020 (18/33/68, 21/27,6/28,2), sin abrir datos por operación ni etiqueta.


## 6. Método de medición: ¿podrá F26 afirmar algo?

**inferencia** (de la aritmética de 6.1, la disponibilidad real de 6.2 y los hallazgos [d7-metodo-01] a [d7-metodo-10]): no. Con el material declarado hoy —19 días de mayo de 2026, holdout ya repartido en tres tramos— F26 no llega al mínimo estadístico para distinguir un bot que replica al trader del que no lo hace, la unidad que debería medir no está decidida, la prueba mecánica que certifica que el reparto es anterior al etiquetado no prueba eso, y una fuente de error de medida (A-16) sigue sin cuantificar mientras el pre-registro exige fijar la tolerancia antes de abrir holdout.

| id | hallazgo (resumen) | severidad final | veredicto |
|---|---|---|---|
| [d7-metodo-01] | `kit check` sin `data/` imprime OK sin comparar nada; no está en `make check` ni en CI | menor | MATIZADO |
| [d7-metodo-02] | la reproducción byte a byte no prueba que el reparto sea anterior al etiquetado | grave | MATIZADO |
| [d7-metodo-03] | la guardia de ancestro solo protege frente a `LABEL_CASE` de la misma sesión | grave | MATIZADO |
| [d7-metodo-04] | un supersede de la ronda 2 borra la unidad de la ronda 1, contra su propio docstring | media | CONFIRMADO |
| [d7-metodo-05] | los documentos no coinciden en qué partición da la cifra final de fidelidad | grave | MATIZADO |
| [d7-metodo-06] | mínimo de 36 unidades efectivas; holdout-1 da 10-14, los tres holdout juntos 20-28 | grave | MATIZADO |
| [d7-metodo-07] | la unidad de F26 no está decidida; la gramática de `LABEL_CASE` no representa ≥30 de 68 operaciones | grave | MATIZADO |
| [d7-metodo-08] | A-16 (Oanda/Dukascopy) sin medir, no bloqueante, aplazada a F26 | media | MATIZADO |
| [d7-metodo-09] | el kappa de F10 no tiene ronda 1 ni camino para construir la ronda 2 | media | MATIZADO |
| [d7-metodo-10] | la ventana de exclusión de noticias (A-17) no existe | menor | MATIZADO |

### 6.1 El número mínimo: 36 unidades efectivas independientes

**hecho** (aritmética ejecutada con `aritmetica_f26.py`, stdlib + numpy 2.5.2; scipy no está en el venv). Para distinguir, con una binomial exacta y alfa 0,05 unilateral, un acuerdo bot-trader de 0,8 de uno de 0,6 con potencia 0,80, el primer n que la alcanza es **36** (k=27, potencia 0,832); la potencia oscila por debajo de 0,80 hasta n=38 y no vuelve a bajar de ahí desde n=39. La aproximación normal da 33 (unilateral) o 43 (bilateral):

| n | k | alfa real | potencia en p=0,8 |
|---|---|---|---|
| 6 | 6 | 0,047 | 0,262 |
| 12 | 11 | 0,020 | 0,275 |
| 14 | 12 | 0,040 | 0,448 |
| 22 | 18 | 0,027 | 0,543 |
| 30 | 23 | 0,044 | 0,761 |
| 33 | 25 | 0,044 | 0,800 |
| 35 | 27 | 0,026 | 0,745 |
| 40 | 30 | 0,035 | 0,839 |

Con un intervalo de confianza en vez de una prueba de hipótesis, el suelo es más alto: una semianchura de ±10 puntos alrededor de p=0,8 exige 60-70 unidades (Wald/Wilson/Clopper-Pearson) y alrededor de p=0,7, 78-88; ±15 puntos baja a 28-40 según p y método.

**hecho.** El acuerdo observado también hay que leerlo con su intervalo, no como cifra suelta. IC 95 % de una proporción de acuerdo (Wilson / Clopper-Pearson):

| n | p̂ | Wilson | Clopper-Pearson |
|---|---|---|---|
| 12 | 0,80 | [0,552; 0,953] | [0,516; 0,979] |
| 22 | 0,80 | [0,615; 0,927] | [0,597; 0,948] |
| 36 | 0,80 | [0,650; 0,902] | [0,640; 0,918] |
| 100 | 0,80 | [0,711; 0,867] | [0,708; 0,873] |

Con acuerdo del 100 % observado, la cota inferior unilateral al 95 % (0,05^(1/n)) tampoco compensa un n bajo: n=6 → 0,607; n=12 → 0,779; n=21 → 0,867.

**hecho.** Con tres categorías ({compra, venta, no_trade}), el kappa de Cohen tiene el mismo problema de varianza. Con marginales pe≈0,335 y kappa real 0,7 (po=0,801): SE asintótico×√n=0,601, hacen falta n=139 para que el IC inferior supere 0,6 y n=16 para que supere solo 0,4. Monte Carlo (20 000 simulaciones, kappa real 0,7): n=12 → SE empírico 0,180, percentiles 2,5-97,5 **[0,31; 1,00]**, P(kappa̅<0,4)=0,073; n=22 → SE 0,131, [0,42; 0,93]; n=36 → SE 0,101, [0,49; 0,87]; n=60 → SE 0,078, [0,54; 0,85]. Con n=12 un kappa real de 0,7 puede salir medido como 1,0 o como 0,3 sin que eso sea un desacuerdo real.

**hipótesis** (SIN_VERIFICAR; se comprobaría estimando el ICC intra-día y las marginales reales sobre los 6 días dev y sobre backtests de desarrollo de enero, abril y agosto, sin tocar holdout). Las unidades no son independientes dentro de un día: si el sesgo H4 se equivoca, arrastra la dirección de toda la sesión, y un fallo de llenado cambia cartuchos y `operacion_abierta` para el resto del día. Con n_eff = n / (1 + (m-1)·rho):

| unidad | partición | n | rho 0 | rho 0,1 | rho 0,2 | rho 0,3 |
|---|---|---|---|---|---|---|
| sesión H4 (m=2) | holdout-1 (6 d) | 12 | 12,0 | 10,9 | 10,0 | 9,2 |
| sesión H4 | 12 días de holdout medibles | 24 | 24,0 | 21,8 | 20,0 | 18,5 |
| operación (m≈3,58) | holdout-1 | 21,5 | 21,5 | 17,1 | 14,2 | 12,1 |
| operación | 12 días de holdout medibles | 42,9 | 42,9 | 34,1 | 28,3 | 24,2 |
| día (m=1) | holdout-1 | 6 | 6 | 6 | 6 | 6 |

Si el sesgo H4 arrastra la dirección de todo el día (rho cercano a 1), las unidades efectivas tienden al número de días: unos 36 días, con cualquier unidad de sub-día.

**Número mínimo: 36 unidades efectivas independientes.** Sostenido por la potencia de la binomial exacta contra 0,6; los intervalos de confianza y el kappa piden más, no menos.

### 6.2 Cuánto hay realmente: ninguna combinación de mayo llega

**hecho.** Particiones de mayo de 2026 declaradas en `particiones.yaml`:

| partición | días | notas |
|---|---|---|
| dev | 05-08, 05-12, 05-15, 05-18, 05-20, 05-28 | 6 días |
| holdout-1 | 05-04, 05-19, 05-21, 05-22, 05-26, 05-29 | 6 días |
| holdout-2 | 05-07, 05-11, 05-13, 05-14 | 4 días, 05-14 quemado → 3 medibles |
| holdout-3 | 05-05, 05-06, 05-27 | 3 días |

**inferencia** [d7-metodo-06] (de la tabla de 6.1 y esta partición): con la unidad sesión H4, holdout-1 da 12 unidades, 10 efectivas con rho 0,2; con la unidad operación (68 operaciones / 19 días ≈ 3,58/día), da ≈21,5 unidades, 14,2 efectivas. holdout-2 medible da 5-7 efectivas, holdout-3 igual. Los tres holdout juntos (12 días) dan 20 efectivas por sesión o 28 por operación. **Ninguna combinación de mayo llega a 36.** El IC de Wilson de un 0,8 observado en holdout-1 con 12 unidades es [0,517; 0,937] y con n_eff=10 es [0,490; 0,943]: ninguno de los dos excluye 0,6. `PREREGISTRO.md:15-24` exige métrica, umbral y partición, pero no un N mínimo, una potencia ni una anchura de intervalo, y ningún otro documento del proyecto lo declara (`grep` sobre `docs/plan`, `docs/adr` y `PREREGISTRO.md` no encuentra "potencia" ni "tamaño de muestra"). `docs/plan/features/F14-case-library.md:112` admite que "con seis días no se sostiene ninguna afirmación estadística" hablando de dev, y holdout-1 tiene esos mismos seis días. **Impacto:** una nota de F26 sobre holdout-1 es compatible a la vez con un bot que replica al trader 9 de cada 10 veces y con uno que lo hace 5 de cada 10.

**hecho** [d7-metodo-05]. Los documentos no coinciden en qué partición da la cifra que decide. `docs/plan/MASTER_PLAN.md:203` y `knowledge/cases/holdout/README.md:5-6` dejan holdout-1 para "discrepancias y corrección" y la "cifra final de fidelidad" para holdout-2 (3 días medibles tras quemar 2026-05-14); `docs/adr/0021-que-cuenta-como-abrir-un-holdout.md:27-28`, `docs/validation/HOLDOUT-EXPOSICIONES.md:24-25` y `PREREGISTRO.md:15/24` hacen de holdout-1 "la nota" (6 días) y de holdout-2 solo la segunda oportunidad si falla o hay que corregir. Además, `docs/adr/0025-el-reparto-de-mayo-no-se-toca.md:71-73` dice que mayo "nunca va a ser la partición limpia de la que salga la cifra de fidelidad de F26", mientras `HOLDOUT-EXPOSICIONES.md:40` y `PREREGISTRO.md:28` lo tratan como "el único material ciego que existe". Si gana la lectura del plan, la cifra que habilita pasar a MQL5 y a la cuenta fondeada saldría de 3 días; si gana la de ADR-0025, no hay ninguna partición válida para la nota hasta que llegue el mes limpio, sin fecha.

**hecho** [d7-metodo-07, mueve la aguja]. La unidad que mide F26 no está decidida, y hay tres versiones incompatibles en el propio proyecto: (a) `docs/adr/0011-kit-de-elicitacion.md §6` y `src/botsito/cases/kappa.py` usan (caso, sesión H4) con una sola decisión {compra, venta, no_trade}, 2 unidades por día; (b) `PREREGISTRO.md:17-18` define la "misma decisión" a nivel de operación (dirección, ventana, entrada, stop, objetivo, con tolerancia); (c) el brief de F14 deja abiertas D1 (¿la verdad sale del xlsx o de `LABEL_CASE`?) y D2 (¿un caso es un día o una operación?). La spec permite varias operaciones por sesión (`cartuchos_max=3` por zona de liquidez, no por día; `cartucho_criterio=solo_perdida`; `cartuchos_reinicio=siguiente_liquidez_m15`; tope diario 4,5 % con 0,5 % por operación ⇒ hasta ≈9 pérdidas), y el material lo confirma: 68 operaciones en 19 días, entre 1 y 7 por día. Con 19×2=38 huecos de sesión, al menos 68-38=30 operaciones no pueden ser la única decisión de su sesión, y la gramática las rechaza:

```
>>> parsear_etiqueta("07-11: venta@08:37 e=1.15364 sl=1.15420; 07-11: venta@09:52; 11-15: no_trade")
EtiquetaError: la sesion 07-11 aparece dos veces          # kappa.py:52
>>> parsear_etiqueta("07-11: venta@08:37 venta@09:52; 11-15: no_trade")
EtiquetaError: 07-11: 'venta@09:52' no es clave=valor
```

**Impacto:** si F26 mide por sesión, el segundo y el tercer cartucho —donde se concentran las pérdidas (33 de 68)— no se comparan nunca, y el bot puede aprobar con una gestión de reentradas distinta de la del trader. Esto además condiciona la interfaz del motor: lo que F18-F24 emita por operación es lo que consumirán el runner de F14 y el comparador de F26; fijar la unidad después de escribir el motor obliga a rehacer esa interfaz.

**hecho** [d7-metodo-09]. El kappa de F10 (consistencia del propio trader) tiene 0 registros `LABEL_CASE` hoy: la ronda 1 no existe. `knowledge/cases/kit/vistos.yaml:38-44` documenta un hueco de proceso sin cerrar: añadir mayo a la lista de "vistos" para poder sortear una sesión 2 invalida el paquete de la sesión 1 ("se piden 40 casos y el universo tiene 22"), y cambiar los cupos de `config.yaml` rompe `kit check` de la sesión 1 (`paquete.py:551-552` exige que `config.yaml` no cambie). Aun si se resolviera, el techo de la hoja actual son 6 días dev × 2 sesiones = 12 unidades, y con kappa real 0,7 el 95 % de las estimaciones en n=12 cae entre 0,31 y 1,00 (tabla de 6.1): no mediría nada.

### 6.3 La prueba de "el reparto es anterior al etiquetado" no prueba eso

**Afirmación 3.3.10** (¿`kit check` compara `particiones.yaml` en cada caso?). **hecho.** Depende de si hay datos de velas en `data/`:

```
$ botsito.exe --repo <original, con data/> kit check --sesion 2026-09-09-sesion-01
AVISO: .../cuestionario.yaml: ya no se genera igual, y es lo esperado...
AVISO: .../hoja_trader.md: ya no se genera igual, y es lo esperado...
OK: 2026-09-09-sesion-01 sin diferencias que no explique la sesion celebrada
EXIT=0                                          # aquí SÍ se comparó particiones.yaml y ventanas.yaml

$ botsito.exe --repo <clon sin data/> kit check --sesion 2026-09-09-sesion-01
AVISO: 2026-09-09-sesion-01: datos de los datasets ausentes en data/: solo esquema
OK: 2026-09-09-sesion-01 sin diferencias que no explique la sesion celebrada
EXIT=0                                          # aquí NO se comparó nada, ni con particiones.yaml mutado
```

`src/botsito/cases/paquete.py:555-563`: `if not hay_datos: avisos.append(f"{sesion}: datos de los datasets ausentes en {carpeta_datos.name}/: solo esquema"); return problemas, avisos` — el `return` está antes de `construir()` y de las comparaciones de las líneas 564-584. `src/botsito/cli.py:1360-1361` convierte ese aviso en `"OK: ... sin diferencias que no explique la sesion celebrada"` con exit 0, tanto en un clon limpio como con `particiones.yaml` mutado a mano. `kit check` no está en `Makefile: check = lint types contracts test state config knowledge`, y `ci.yml:28` solo corre `make check`: **la comparación del paquete real no se ejecuta nunca en CI** [d7-metodo-01]. Severidad ajustada a menor porque el mecanismo con datos sintéticos sí se prueba en CI y la reescritura manual sí se detecta en una máquina con `data/`.

**hecho** [d7-metodo-02]. Incluso con `data/`, la reproducción byte a byte no prueba anterioridad: `comprobar()` lee el seed del propio `particiones.yaml` (`paquete.py:549: seed = int(particiones["seed"])`) y regenera a partir de él. Un paquete re-sorteado con otro seed vuelve a pasar `comprobar()`:

```
asignacion seed 3: {'caso-xxxyyy-2026-05-06': 'holdout-1', ...}
comprobar paquete original (celebrada=True): ([], [])
seed nuevo 4; asignacion: {'caso-xxxyyy-2026-05-04': 'holdout-2', ...}
comprobar paquete RE-SORTEADO (celebrada=True): ([], [])
comprobar paquete RE-SORTEADO (celebrada=False): ([], [])
```
(reproducido sobre el kit sintético de `tests/unit/test_kit.py:161`, símbolo XXXYYY; **no** se recalculó sobre el paquete real de la sesión 1 para no recomputar velas reales de mayo — SIN_VERIFICAR en el paquete real, mismas funciones). En la sesión 1 el universo tiene 42 días (`ventanas.yaml:971: universo: 42`) contra 40 de cupo, así que el seed también decide qué 2 días quedan fuera; `ventanas.yaml` está exento de aviso duro en una sesión ya celebrada. `docs/adr/0025-el-reparto-de-mayo-no-se-toca.md:45-46` y `knowledge/cases/kit/config.yaml:41-43` llaman a esto "la prueba de que las particiones se fijaron antes de etiquetar", y ADR-0025 renunció a 4 días de desarrollo apoyado en esa premisa. Lo que la reproducción prueba es que el paquete es una función determinista de (repo, datos, seed escrito), no cuándo se escribió ese seed. La única prueba de anterioridad real es el historial de git de `particiones.yaml` (`bf9471c` 2026-09-08, `6266738` 2026-09-09), y no hay ningún test de historial sobre ese fichero: `tests/contract/test_kit_particiones.py:124-128` da por buena una reasignación mientras no haya etiquetas.

**hecho** [d7-metodo-03]. La guardia de ancestro (`paquete.py:641-643: etiquetas = [r for r in registros if r.sesion == sesion and r.accion == "LABEL_CASE"]; if not etiquetas: continue`) solo se arma con `LABEL_CASE` cuya sesión coincide con la carpeta del paquete. `feedback/modelo.py:390` valida el objetivo `caso` solo por formato, así que un `LABEL_CASE` registrado bajo otra sesión sobre un caso del paquete de la sesión 1 no arma la guardia:

```
# rama prueba-otra-sesion: LABEL_CASE bajo sesión 2026-09-20-sesion-02 sobre caso-eurusd-2026-05-08
# + particiones.yaml reescrito (05-04 holdout-1<->dev, 05-08 dev<->holdout-1)
$ botsito.exe --repo <clon> knowledge validate
OK: 23 ambiguedades registradas; 1 paquetes de sesion validos, particiones anteriores al etiquetado
EXIT=0

# CONTROL, rama prueba-misma-sesion: mismo LABEL_CASE bajo 2026-09-09-sesion-01, misma reescritura
validar_paquetes: ['2026-09-09-sesion-01: particiones.yaml cambio despues de su commit 6266738
  y ya hay LABEL_CASE de esa sesion (la asignacion es inmutable tras el etiquetado)']
```

`MASTER_PLAN.md:183` pone la "ronda 2 (kappa)" en la Sesión 2, y F14 (brief D1 abierto) no ha decidido con qué sesión registrará la verdad de mayo: las etiquetas que F26 usaría pueden caer, en la práctica, fuera de la única guardia de anterioridad que existe. No es indetectable en toda circunstancia: en una máquina con `data/`, `kit check` sí denuncia la reescritura manual; pero `kit check` sin `data/` (el caso de CI, hallazgo 01) no.

**Afirmación 3.3.11** (¿un supersede de otra sesión retira una etiqueta de la ronda que se está midiendo?). **hecho** [d7-metodo-04]. `activos()` (`src/botsito/comun/documentos.py:103-106`) filtra supersedidos sobre **todos** los registros, sin filtrar por sesión; `kappa.py:146: vivos = [r for r in activos(list(registros)) if r.sesion == sesion and r.accion == "LABEL_CASE"]` hereda ese alcance, contra su propio docstring (`kappa.py:143-144`: "Una corrección hecha en otra sesión NO retira la etiqueta de esta: cada sesión es una ronda"). `feedback/modelo.py:427-469` exige mismo objetivo y orden temporal en un supersede, nunca misma sesión.

```
E0 control (sin retiros): ronda1=4 unidades, ronda2=4, calcular: unidades=4 po=1 kappa=1
E2 (BORDERLINE de sesión 2 supersede el LABEL_CASE de sesión 1 sobre U):
  ronda1: ['...05-12|07-11', '...05-12|11-15']   (U desaparece EN SILENCIO)
  calcular: unidades=2 po=1 kappa=1 avisos=[]
E3 (LABEL_CASE de sesión 2 sobre U supersede el de sesión 1):
  calcular: EtiquetaError: las rondas no tienen las mismas unidades:
    solo en a [], solo en b ['...05-08|07-11', '...05-08|11-15']   (el error culpa a la ronda equivocada)
```

`tests/unit/test_kit.py:535-551` y `708-760` solo prueban supersede dentro de una misma sesión. Hoy sin daño (0 `LABEL_CASE` existen), pero `MASTER_PLAN.md:204` pre-registra un umbral de kappa sobre un cálculo que, en silencio, puede quedarse con menos unidades de las declaradas.

### 6.4 A-16: la divergencia Oanda/Dukascopy

**hecho.** El trader decidió mayo sobre velas de Oanda (FX Replay); el bot se mide sobre Dukascopy (A-23, DECIDIDA). Lo único medido compara otra pareja:

| pareja | días | velas | idénticas | mediana | p90 | máx |
|---|---|---|---|---|---|---|
| MT5/FundedNext vs. Dukascopy (−3h) | 1 (2026-06-10) | 1261 | 15 (1,2 %) | 2 pt | 3 pt | 20 pt |
| Oanda (FX Replay) vs. Dukascopy | 0 | — | — | — | — | — |

**inferencia** [d7-metodo-08] (de A-23 "MARGEN DECLARADO" sin número, y de `PREREGISTRO.md:17-18`). `knowledge/spec/ambiguedades.yaml:261-278` mantiene A-16 `estado: ABIERTA`, `bloqueante: false`, `resuelve_en: [F26]`. El anexo mismo lo admite: "Queda una tercera fuente en juego, que es la del trader: el backtestea en **FX Replay, que usa datos de Oanda**. Esta medición no la cubre" (`A-16-proveedor-de-datos-2026-09-09.md:52-53`). `PREREGISTRO.md:17-18` obliga a fijar la tolerancia de entrada, stop y objetivo antes de abrir holdout-1; A-16 se resuelve dentro de F26, que según `MASTER_PLAN.md:203-204` incluye un pre-registro previo a esa apertura, así que el orden no está necesariamente invertido, pero tampoco hay hoy ningún número de Oanda que poner en ese pre-registro. El sesgo tiene dos direcciones: si nadie ajusta nada, las decisiones que cambian por 1-20 puntos (romper un máximo H4, tocar la límite, llegar al 1:3) cuentan como desacuerdos del bot y la fidelidad sale sesgada a la baja, con la dependencia intra-día al alza (un fill que no ocurre cambia cartuchos y `operacion_abierta` el resto del día); si la tolerancia se elige después de ver los datos, es un grado de libertad a favor del bot.

**hipótesis** (cómo se comprobaría, sin tocar holdout): (1) Oanda M1 vs. Dukascopy en meses ya vistos con dataset congelado (enero y agosto de 2026: `data/manifests/eurusd-m1-2026-01-e37291d4.yaml`, `-2026-08-0d42230e.yaml`), por hora dentro de 07:00-15:00 Madrid, con el reloj de FX Replay alineado antes de medir; (2) precios de entrada y stop de los xlsx de enero y agosto contra Dukascopy en su minuto; (3) tasa de casi-rupturas sobre dev con el p99 de |delta|, que da la tasa esperada de decisiones cambiadas y el número de la tolerancia.

### 6.5 A-17: la ventana de exclusión de noticias tampoco existe

**hecho** [d7-metodo-10]. `docs/adr/0022-el-bot-no-opera-noticias-en-la-cuenta-fondeada.md:58-59` manda tratar como no-fallo del bot toda operación del trader hecha en noticia ("F26 la cita"), pero la ventana —qué eventos, cuántos minutos antes y después— es A-17, ABIERTA: "Sin esta respuesta, RN-028 sabe QUE bloquea y no CON QUE VENTANA" (`ambiguedades.yaml:290-291`). Sin ventana fijada antes de ver los desacuerdos, la exclusión es otro grado de libertad a favor del bot, y cada operación excluida sale de numerador y denominador, acortando aún más las 10-14 unidades efectivas de holdout-1.

### 6.6 Qué falta, por su nombre, para poder medir

1. Decidir la unidad de F26 y la fuente de verdad (F14 D1/D2), y adaptar la gramática de `LABEL_CASE` a varias operaciones por sesión [d7-metodo-07].
2. Un N mínimo declarado (36 efectivas) y el mes limpio del trader (`ADR-0021 §7`): mayo no llega en ninguna partición ni combinación [d7-metodo-06].
3. Fijar en `MASTER_PLAN.md:203`, `holdout/README.md`, ADR-0021 y ADR-0025 qué partición da la nota y qué papel tiene cada una [d7-metodo-05].
4. `PREREGISTRO.md` con métrica, tolerancias (después de medir A-16), tratamiento de noticias (después de cerrar A-17), N mínimo y potencia, y umbral de kappa con su N.
5. Una prueba de anterioridad del reparto que no dependa de la sesión del `LABEL_CASE` ni de tener `data/`: hoy la reproducción byte a byte no la da [d7-metodo-01, d7-metodo-02, d7-metodo-03].
6. La guarda de holdout de `tests/conftest.py:18`, hoy stub (ya declarada en ADR-0021 y F14; no se repite su evidencia aquí).
7. El motor F18-F24 y un comparador que además emita el ICC intra-día.
8. Una ronda 1 de `LABEL_CASE` (hoy 0) si se quiere el kappa del trader [d7-metodo-09].
9. Cerrar el hueco de `vistos.yaml` (mayo visto) antes de construir la sesión 2 [d7-metodo-09].

**hipótesis** (días necesarios, misma fórmula n_eff de 6.1, no verificada con rho real): para llegar a 36 unidades efectivas se necesitan del orden de 36 días si la unidad es el día, 20-24 si es la sesión H4 (rho 0,1-0,3) o 13-18 si es la operación. Los 19 días de mayo, en cualquier combinación de particiones, no llegan.

### 6.7 Sin verificar en esta dimensión

- El re-sorteo del hallazgo [d7-metodo-02] sobre el paquete **real** de la sesión 1: no se ejecutó para no recomputar velas de mayo; se demostró con el kit sintético de los tests, que pasa por las mismas funciones `comprobar`/`construir`/`escribir`.
- `kit build` de un paquete de sesión 2 [d7-metodo-09]: prohibido en el original, y el clon no tiene `data/`. La cifra "se piden 40 casos y el universo tiene 22" sale del comentario de `vistos.yaml:41`, no de una ejecución propia.
- Los valores reales de rho intra-día, las marginales del kappa y el número de operaciones por partición: exigirían abrir el xlsx (dev permitido, holdout prohibido). Se usó 68/19 por día y rho entre 0,1 y 0,3 como supuestos declarados, no medidos.
- La magnitud real de la divergencia Oanda/Dukascopy, el reloj de FX Replay, y si FX Replay usa bid, ask o mid de Oanda.
- Con qué campo de sesión registrará F14 la verdad de mayo (brief D1 abierto): el impacto real de [d7-metodo-03] depende de esa decisión todavía no tomada.
- No se corrió la suite de pytest ni `make check` en esta dimensión (lo cubre otro agente); solo se ejecutaron funciones concretas en scripts sueltos.

### 6.8 Alcance del método de esta auditoría

Por mandato explícito de la tarea, se ejecutó `kit check --sesion 2026-09-09-sesion-01` sobre el repositorio original **con** `data/`, orden que recalcula `n_velas` y sha256 de las ventanas de los 19 días de mayo (holdout incluido) pero no lee etiquetas ni mide ninguna cifra del bot ni muestra ningún precio (conforme a `ADR-0021 §1`). No se abrió ningún fichero dentro de `knowledge/cases/holdout/1`, `/2` ni `/3` (solo se listaron nombres), ni el xlsx de mayo; solo se leyeron los agregados ya declarados en `HOLDOUT-EXPOSICIONES.md` y la asignación de `particiones.yaml`. Las pruebas de re-sorteo, guardia de sesión y supersede se hicieron sobre un clon en `Temp` con datos sintéticos o commits de prueba (`Fuente: ADR-0011`); ninguna escritura tocó el repositorio original (`git status --short` al final solo mostraba `M PROJECT_STATE.md`, ya presente antes).

### 6.9 Notas para otras dimensiones

- d6-evidencia / d3-guardias-citas: `comun/documentos.py:103 activos()` tampoco distingue sesión para el feedback en general (mismo mecanismo que [d7-metodo-04]).
- d8-camino-motor: el hallazgo [d7-metodo-07] (unidad y gramática) condiciona la interfaz de salida del motor.
- exec-checks: `tests/contract/test_kit_particiones.py:124-128` fija como correcto reasignar particiones sin etiquetas.


## 7. Deuda menor

84 hallazgos por debajo del umbral que mueve la aguja del motor (F18-F24), de 91 evaluados en este corte; los 7 restantes (severidad media: d2-fidelidad-afirmaciones-06, d2-fidelidad-afirmaciones-07, d7-metodo-04, d7-metodo-08, d7-metodo-09, d8-camino-motor-08, exec-cli-07) se tratan en sus secciones de dimension, no aqui.

Todos con veredicto CONFIRMADO o MATIZADO (ninguno REFUTADO ni SIN_VERIFICAR en este corte): **hecho**, verificado por un esceptico; donde el veredicto fue MATIZADO, el enunciado de abajo es ya el corregido.

### exec-checks

| id | qué | ruta:línea |
|---|---|---|
| exec-checks-04 | Fidelidad de citas: revocadas en reglas y glosario, literal del glosario y decision inexistente sin test que las fije | src/botsito/spec/modelo.py 761-762, 363-366, 444-446, 718-722 |
| exec-checks-05 | latencia_ms esta declarado como tipo minutos con unidad milisegundos | knowledge/spec/parametros.yaml 157-165 |
| exec-checks-06 | Piezas que el motor leera con cero ejecuciones en la suite | src/botsito/config/registro.py ; src/botsito/domain/valores.py ; src/botsito/data/agregacion.py registro.py:203-210 ; valores.py:47-57, 75-89 ; agregacion.py:140-148 |
| exec-checks-07 | El HEAD commiteado de main falla state check; el verde local depende del PROJECT_STATE.md sin commitear | PROJECT_STATE.md (version de 0a9612d) 37 y 43 (git show HEAD:PROJECT_STATE.md) |
| exec-checks-08 | Cero skips es una propiedad de esta maquina: en CI se omite al menos el test del tokenizador real | tests/unit/test_motor_prompt.py ; .github/workflows/ci.yml 135-141 ; run: uv sync --locked --group dev |
| exec-checks-09 | Las multiplicidades de parametrizacion de PROJECT_STATE no existen | PROJECT_STATE.md 117 |
| exec-checks-10 | Rama muerta en comprobar_forma: una invocacion llamada 'hecho' nunca llega | src/botsito/spec/modelo.py 915-916 (y 587-588, 639) |

### exec-git

| id | qué | ruta:línea |
|---|---|---|
| exec-git-03 | Coste unitario medido: mediana de 6,64 h de reloj y 1,58 h activas por funcionalidad; las tres que ya tratan reglas del trader (F11-F13) cuestan de media 5,99 h activas, 4,6 veces lo de F01-F10+F15 | docs/HANDOFF.md (ritual) · historial de git HANDOFF.md:183-193 |
| exec-git-04 | El informe nace con 'Estado: WAITING_FOR_USER_VALIDATION' a mitad de rama, y en 11 de 14 funcionalidades llegan después commits de fix o auditoría: 75 commits posteriores al informe, 41 de fix o auditoría | docs/validation/F11-strategy-spec-schema.md (versión del commit 41d567f) · docs/HANDOFF.md F11-strategy-spec-schema.md@41d567f:3; HANDOFF.md:186-188 |
| exec-git-05 | 6 de los 20 tags (30 %) no son funcionalidades del plan; F14, de la que depende F18, se abrió como rama y 17 minutos después se renombró a una auditoría: 0 commits | docs/plan/MASTER_PLAN.md · reflog de HEAD (git log -g HEAD) MASTER_PLAN.md:88 y :94 |
| exec-git-06 | Extrapolación: al coste de F11-F13, las 22 unidades restantes son unas 132 h activas (~28 días de calendario con el ciclo medido); a la mediana global, unas 35 h (~9 días). F34 exige 3 meses de calendario pase lo que pase | docs/plan/MASTER_PLAN.md 112 |
| exec-git-07 | PROJECT_STATE.md: lo tocan 131 de 232 commits, creció de 7,7 a 127,5 KB, su churn en bytes (549 KB) equivale al 64 % del de todo src/, y solo el 20 % de ese churn es Change Log | PROJECT_STATE.md (HEAD 0a9612d) 22 y 405 |
| exec-git-08 | Desde el 09-04 a las 20:58 nadie ha tocado domain/, engine/, mql5bridge/ ni viewer/: 139 commits después, 0; y solo 84 de 232 commits tocan src/ | src/botsito/engine/__init__.py 1 |
| exec-git-09 | HEAD está a mitad de ritual: stable/F13-auditoria etiqueta el merge 0a9612d, pero no hay docs(state), PROJECT_STATE.md tiene cambios sin commitear y origin/main sigue en 1cf5aa2; el orden merge -> tag -> docs(state) ya se rompió en F01 y F11 | docs/HANDOFF.md 189-193 |
| exec-git-10 | Desde git las horas activas no se miden con precisión: los commits llegan en ráfagas del mismo segundo, y pasar el umbral de pausa de 1 a 3 h mueve el total de 39 a 72 h | historial de git (git log --all --format=%aI; git log -g HEAD) n/a (metadatos de commit) |

### exec-cli

| id | qué | ruta:línea |
|---|---|---|
| exec-cli-01 | `data aggregate` anuncia que A-9 sigue abierta y construye velas H4 con cualquier ancla sin contrastarla con anclaje_h4 CONFIRMED | src/botsito/cli.py 1823, 2128 |
| exec-cli-02 | `kit check` imprime 'OK ... sin diferencias que no explique la sesion celebrada' cuando no ha comparado nada | src/botsito/cli.py 1356-1363 (y src/botsito/cases/paquete.py:557-561) |
| exec-cli-03 | 'particiones anteriores al etiquetado' es una guardia que no se ejecuta: con cero LABEL_CASE se puede permutar el holdout o recortar ventanas y todo sigue en OK | src/botsito/cases/paquete.py 50, 569-583, 641-643 (texto impreso en src/botsito/validation/knowledge.py:630-632) |
| exec-cli-04 | 'registro con 59 parametros (8 sin confirmar)' cuando parametros.yaml tiene 9 sin CONFIRMED: falta reloj_dia_riesgo, el que reinicia el tope diario | src/botsito/validation/knowledge.py 236-238 (filtro en src/botsito/config/registro.py:167-174) |
| exec-cli-05 | La respuesta del trader sobre noticias ('no filtra') sale como 'reflejado ... no se pregunta', y A-22 como 'no las respondio el trader', aunque el bot corre con la opcion contraria | src/botsito/cli.py 1566-1567, 710 |
| exec-cli-06 | `spec status` dice 'sin valor a proposito' sin comprobarlo y cuenta REJECT ya supersedidos: contradice a `feedback pending` | src/botsito/cli.py 693, 724-727 |
| exec-cli-08 | Docstrings de cli.py con estados y recuentos rancios, de la misma clase que 3.3.14: 'stop.nivel ... y sigue ABIERTA' y 'los ocho CORRECT y REJECT' | src/botsito/cli.py 1631-1636 |

### exec-windows

| id | qué | ruta:línea |
|---|---|---|
| exec-windows-01 | Ningun codigo Python se ejecuta en Windows de forma automatica, y los arreglos de plataforma ya vividos solo se detectan en Windows local: F23-F24 heredarian ese punto ciego | .github/workflows/ci.yml 15, 28, 29 |
| exec-windows-02 | El encoding='utf-8' de cli.main no lo discrimina ningun test en ninguna plataforma | src/botsito/cli.py 2145-2147 |
| exec-windows-03 | Si se pierde la decodificacion UTF-8 de git, la guardia de trazabilidad devuelve 'sin problemas' en Windows y el unico test que lo vigila solo falla en Windows | src/botsito/comun/historial.py 12-14, 51-60 |
| exec-windows-04 | El hook pre-commit y su instalador no tienen veredicto automatico; lo que caza y lo que no, medido en un clon | scripts/git-hooks/pre-commit 11-12, 15-31, 33-49; tests/contract/test_fotogramas_history.py:62-63 |
| exec-windows-05 | La preparacion de DLL de CUDA y la carga real de faster-whisper no las ejecuta ningun test | src/botsito/corpus/motor_whisper.py 40-52, 124-136 |
| exec-windows-06 | validar_manifiesto acepta rutas con letra de unidad y en Windows comprobar() lee fuera de data/ | src/botsito/data/dataset.py 344-350, 386, 437 |
| exec-windows-07 | La base de husos que certifica el CI no es la fijada en uv.lock: en Windows solo existe tzdata 2026c, en ubuntu manda la del sistema | pyproject.toml 9 (y src/botsito/comun/husos.py:27, docs/adr/0004-categorias-de-parametro-y-horas-con-huso.md:19-20) |
| exec-windows-08 | El CI dice usar 'la misma' version de Python que en local y no la usa | .github/workflows/ci.yml 26 (y .python-version:1, .venv/pyvenv.cfg) |

### d1-interprete

| id | qué | ruta:línea |
|---|---|---|
| d1-interprete-07 | RN-019 casi nunca dispara y, cuando dispara, RN-008 le bloquea la reentrada; 'equal' tiene tres significados, no dos | knowledge/spec/strategy_spec.yaml 883-890 (RN-019), 580-586 (RN-008), 302-303 (token equal); glossary.yaml:74-83; parametros.yaml:488 |

### d2-fidelidad-afirmaciones

| id | qué | ruta:línea |
|---|---|---|
| d2-fidelidad-afirmaciones-02 | Ningun texto de la spec dice que el nivel 0 es la entrada; la unica frase del corpus que nombra el nivel 0 lo llama umbral de invalidacion | knowledge/spec/parametros.yaml 335, 560-561, 775-776 |
| d2-fidelidad-afirmaciones-05 | RN-014 exige una zona distinta de OP.zona_de_entrada, y en el primer esquema no hay zona de control de entrada | knowledge/spec/strategy_spec.yaml 271-272, 760-764 |

### d2-literal-a

| id | qué | ruta:línea |
|---|---|---|
| d2-literal-a-05 | RN-012 afirma una perdida 'entera y sin fraccion' que su cita no dice y que RN-027 y cualquier deslizamiento desmienten | knowledge/spec/strategy_spec.yaml 685-688 (RN-012 entonces), 239-241 (realizar_perdida), 713-715 (forma), 1053-1057 (RN-027) |
| d2-literal-a-07 | RN-013 ejecuta 'escribir el stop en la orden pendiente, antes de que se active' en el evento de activarse | knowledge/spec/strategy_spec.yaml 233-235 (accion), 674-677 (RN-011), 722-741 (RN-013) |
| d2-literal-a-08 | RN-002 cita la sintesis de hoja del consultor, que no dice 'cerrar posiciones', teniendo en el corpus al trader diciendolo | knowledge/spec/strategy_spec.yaml 416-427 (RN-002); knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-ffb528d7.yaml |
| d2-literal-a-09 | La forma de RN-001 contiene los dos frenos de riesgo y ni su cita, ni su prosa, ni sus notas lo mencionan | knowledge/spec/strategy_spec.yaml 382-399 (RN-001 prosa y notas), 400-412 (forma) |
| d2-literal-a-10 | Literales marcados 'cruda leida' que no estan en la cruda (RN-001 '7AM', pregunta de RN-004), y nada lo vigila | knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-694ec50a.yaml y fb-2026-09-09-sesion-01-6e15504f.yaml respuesta_literal y registrado_por; src/botsito/feedback/modelo.py:262 |

### d2-literal-b

| id | qué | ruta:línea |
|---|---|---|
| d2-literal-b-06 | RN-021 regula el spread y cita una frase que solo habla de noticias; la razon grabada para no filtrar depende de no operar noticias | knowledge/spec/strategy_spec.yaml 937-956 (RN-021), 182-191 (contexto_filtrable) |
| d2-literal-b-07 | El registro que citan RN-021, RN-028 y contexto_filtrable hace fallar feedback apply --check de la sesion 1, sin documentar | knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-3565552d.yaml; src/botsito/feedback/aplicar.py 3565552d:6-13; aplicar.py:166-171 y 214-215 |
| d2-literal-b-08 | RN-026 comprueba un token que dice «stop u objetivo» cuando la regla dice «stop o limite» | knowledge/spec/strategy_spec.yaml 294-295 (token), 1025-1027 y 1043-1044 (RN-026) |
| d2-literal-b-09 | RN-027 es un gate sin prohibe: el «no se opera» bajo el lote minimo no esta en la forma | knowledge/spec/strategy_spec.yaml 1054-1057, 1071-1082 |
| d2-literal-b-10 | cartuchos_reinicio: el registro que lo fija no contiene el reinicio en su literal | knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-e3eedcaa.yaml 9-19 |

### d3-guardias-citas

| id | qué | ruta:línea |
|---|---|---|
| d3-guardias-citas-01 | Citar evidencia SUPERSEDIDA no lo ve ninguna guardia: 'revocado' solo existe para feedback | src/botsito/validation/knowledge.py 133 (y 565, 577); src/botsito/spec/modelo.py:743-771 |
| d3-guardias-citas-02 | El vocabulario no exige la pareja cita/literal: un predicado puede perder el literal o la cita y todo sigue verde | src/botsito/spec/modelo.py 384, 417-419, 550-570 |
| d3-guardias-citas-03 | `efectos` queda fuera de las tres guardias de citas, pero spec_docs publica su cita: cita inexistente y frase inventada pasan | src/botsito/spec/modelo.py 382, 415, 763 (frente a src/botsito/cases/spec_docs.py:101 y 117-118) |
| d3-guardias-citas-04 | literal_coincide certifica tokens, no hablante ni sentido: la pregunta del consultor, o un recorte que quita el 'si no', pasan como literal del trader | src/botsito/spec/modelo.py 334-345 (y validation/knowledge.py:147-148) |
| d3-guardias-citas-05 | comprobar_decisiones solo exige que exista un fichero ADR con ese numero: un ADR sin relacion o SUPERSEDED pasan | src/botsito/spec/modelo.py 444-446 (ids desde validation/knowledge.py:21-27) |
| d3-guardias-citas-06 | La convencion 'registro referido por el consultor => la regla declara decision' no la comprueba ningun codigo | knowledge/spec/strategy_spec.yaml 9-12 |
| d3-guardias-citas-07 | spec check y knowledge validate divergen en citas revocadas de parametros, contra el docstring de la 'unica puerta' | src/botsito/validation/knowledge.py 100-104 y 576-584 |
| d3-guardias-citas-08 | Sin strategy_spec.yaml la capa semantica dice OK: problemas_de_spec devuelve lista vacia | src/botsito/validation/knowledge.py 130-132 |

### d3-guardias-forma

| id | qué | ruta:línea |
|---|---|---|
| d3-guardias-forma-06 | La precedencia (ADR-0018) solo detecta disparadores identicos byte a byte: invertir un `todos_de`, anidarlo o sumarse a un grupo ya exento pasa | src/botsito/spec/modelo.py 501, 507-508 |
| d3-guardias-forma-07 | docs/spec/parametros.md afirma que `spec check` impide cualquier numero en una forma; es falso y el documento generado lo repite con la spec mutada | src/botsito/cases/spec_docs.py 135-137 (impreso en docs/spec/parametros.md:7) |
| d3-guardias-forma-08 | La docstring de comprobar_precedencia dice 'exactamente un fallback'; el codigo solo rechaza mas de uno y una spec sin clausula else pasa spec check y knowledge validate | src/botsito/spec/modelo.py 478, 486-491 |

### d3-tests-contrato

| id | qué | ruta:línea |
|---|---|---|
| d3-tests-contrato-02 | La guardia 'la lista no puede quedarse atras del registro' solo sincroniza numeros no enteros: horas, textos, enteros y enums pueden cambiar y la lista sigue vigilando el valor viejo | tests/contract/test_no_business_literals.py 198-233 (225, 227) |
| d3-tests-contrato-03 | El contrato AST de accesores es ciego a cualquier lectura que no sea registro\|reg\|parametros.<accesor>("literal"): self.registro, obtener(), parametros[...] y los kwargs escapan | tests/contract/test_registro_accessors.py 13-26, 34-43 |
| d3-tests-contrato-06 | Los 13 casos de la hoja de sesion, incluido el anti-holdout, cuelgan de un skip sin proteccion CI; lo unico que pone el run en rojo es un assert de otro fichero, y solo se examina la ultima sesion | tests/contract/test_hoja_sesion_docx.py 46-51, 128-137 |
| d3-tests-contrato-07 | La guarda de holdout es un stub sin usos, y la unica viva (buscar la cadena 'holdout') se limita a domain y spec: el motor, que es quien mide cifras sobre dias, queda fuera de ambas | tests/conftest.py 17-24; tests/contract/test_import_contracts.py:103-106 |
| d3-tests-contrato-08 | Los patrones y los motivos de las listas son fragiles o estan viejos: 'T07:00', '7:00', 'Europe/madrid' y 'eurusd' pasan, y los motivos citan decisiones ya revertidas | tests/contract/test_no_business_literals.py 22-45 |

### d4-registro

| id | qué | ruta:línea |
|---|---|---|
| d4-registro-01 | La unica sesion con feedback no se puede aplicar hoy: `feedback apply --sesion 2026-09-09-sesion-01 --check` falla en main y make check no lo ve | src/botsito/feedback/aplicar.py 167-172 (y 214-215) |
| d4-registro-02 | `apply --check` no comprueba minimo/maximo; con la fuente en evidencia, el registro inaplicable queda vigente con knowledge validate en verde y `feedback pending` recomienda el apply que falla | src/botsito/feedback/aplicar.py 181-188 |
| d4-registro-03 | Los husos de tipo texto no se canonizan en ninguna puerta del registro: `feedback apply` escribe 'Europe/madrid' con knowledge validate en verde, y solo lo caza pytest, de rebote y segun la plataforma | src/botsito/config/registro.py 263-267 (y 333-340) |
| d4-registro-05 | El registro no puede verificar al cargar lo que un consumidor va a leer: UNKNOWN, nombre inexistente y tipo equivocado fallan en la lectura, con tres jerarquias de excepcion sin base comun | src/botsito/config/registro.py 82-95, 139-146, 212-220 |
| d4-registro-06 | La anotacion de lecturas DEFAULT_AMBIGUOUS, que alimenta el journal, vive por instancia, se registra aunque la lectura falle y no ve el acceso directo a .valor | src/botsito/config/registro.py 148-154 y 216-219 |
| d4-registro-08 | El contrato de literales deja fuera 5 de los 8 valores numericos de estrategia (3 cartuchos, 1:3, 9 % semanal, 1 operacion, 1 zona): 'ninguna cifra en el codigo' de F21 depende de disciplina | tests/contract/test_no_business_literals.py 18-33 |
| d4-registro-09 | `feedback apply` sin --check revienta con traceback si el bloque del parametro no tiene el formato esperado; --check lo daba por bueno | src/botsito/cli.py 870-873 y 903 |
| d4-registro-10 | El kit duplica fuera del registro valores de negocio que el registro tambien tiene (simbolo, fin de ventana, anclajes con huso) y nada compara las dos copias | knowledge/cases/kit/config.yaml 5-32 |

### d5-relojes-datos

| id | qué | ruta:línea |
|---|---|---|
| d5-relojes-datos-04 | La ruptura del sesgo no tiene umbral en puntos: 7 de 95 rupturas de enero y julio son de 1 a 9 puntos | knowledge/spec/strategy_spec.yaml; knowledge/spec/glossary.yaml strategy_spec.yaml:48-54; glossary.yaml:74-81; parametros.yaml:60 |
| d5-relojes-datos-07 | Solo hay precios BID y ninguna regla dice que lado de la cotizacion llena la entrada, salta el stop o toca el objetivo | src/botsito/data/dataset.py; src/botsito/data/dukascopy.py; knowledge/spec/parametros.yaml dataset.py:303-312; dukascopy.py:34; parametros.yaml (modelo_llenado, ~141-155) |
| d5-relojes-datos-08 | La escala no tiene guardia: el validador acepta cualquier entero positivo y quien concatena series no la compara, al contrario de lo que dice el dominio | src/botsito/data/dataset.py; src/botsito/cases/ventanas.py; src/botsito/domain/velas.py dataset.py:301-332, 373-374, 434-435; ventanas.py:168-179; velas.py:10-11 |
| d5-relojes-datos-09 | El reloj del servidor se declara dos veces sin guardia que las ate, y la descripcion de broker_dst contradice ADR-0017 | knowledge/spec/parametros.yaml 113-139, 184-213 |
| d5-relojes-datos-10 | La herramienta que agrega H4 y el README de los manifiestos siguen diciendo que anclaje_h4 es UNKNOWN y A-9 esta abierta | src/botsito/cli.py; data/manifests/README.md cli.py:1820-1825, 2128; README.md (seccion Comandos) |

### d6-evidencia

| id | qué | ruta:línea |
|---|---|---|
| d6-evidencia-02 | El CI no verifica ninguna cita contra la cruda: una cita inventada pasa make check del CI y solo la caza la maquina del dueno | src/botsito/evidence/modelo.py 384-387, 398-399 (validation/knowledge.py:303-306; docs/adr/0009:17-18) |
| d6-evidencia-03 | evidence new salta 5 de las 6 guardias de calidad por item de ADR-0009 §5, nada las reaplica, y 7 items reales ya las violan | src/botsito/cli.py 569-610, 965 (guardias en src/botsito/evidence/propuestas.py:393, 398, 430, 455, 460; solo las llaman cli.py:1013 y :1134) |
| d6-evidencia-04 | tramos_no_citables.yaml promete Fuente en cada commit y no esta bajo ninguna guardia: quitar el tramo del tercer esquema y citarlo pasa todo | src/botsito/comun/historial.py 33 (knowledge/corpus/tramos_no_citables.yaml:1-3) |
| d6-evidencia-05 | Reescribir historia publicada (amend + rebase) deja un item inmutable con la afirmacion invertida, con knowledge validate y los 23 tests de historial en verde | src/botsito/comun/historial.py 3, 201-213 (scripts/git-hooks/pre-commit:11-12; docs/adr/0003:39-42) |
| d6-evidencia-06 | Sin .git, knowledge validate certifica 'historial intacto' y 'commits con Fuente' sin evaluar nada, y los tests de historial se saltan | src/botsito/validation/knowledge.py 323-330, 436-456, 474-477, 544-549, 636, 646 |
| d6-evidencia-07 | state check sin tags stable/* omite en silencio 'Last Stable Commit' y la regla de main tras el tag | src/botsito/cli.py 73-79, 116-133 |
| d6-evidencia-08 | Las propuestas selladas no tienen guardia de historial y el sello se recalcula solo: la salida del LLM se reescribe y se vuelve a sellar sin error | src/botsito/evidence/propuestas.py 473-484 (directorios protegidos: src/botsito/comun/historial.py:28-32) |
| d6-evidencia-09 | El trailer Fuente solo exige que el id exista: un cambio en la spec citando un ADR ajeno pasa | src/botsito/comun/historial.py 281-289 |
| d6-evidencia-10 | Dos guardias de ADR-0009 §5 no se aplican ni en propose --check: el solape de tema contra la evidencia existente y los 4 tokens en citas de pantalla | src/botsito/evidence/propuestas.py 423, 449-451, 460-463 |

### d7-metodo

| id | qué | ruta:línea |
|---|---|---|
| d7-metodo-01 | kit check sin data/ imprime OK sin haber comparado nada, y no corre en make check ni en CI | src/botsito/cases/paquete.py 555-563 (y src/botsito/cli.py:1360-1361) |
| d7-metodo-10 | La divergencia por noticias que F26 debe excluir no se puede delimitar antes de medir: la ventana de A-17 no existe | docs/adr/0022-el-bot-no-opera-noticias-en-la-cuenta-fondeada.md 58-59 (y knowledge/spec/ambiguedades.yaml:290-291) |

### d8-camino-motor

| id | qué | ruta:línea |
|---|---|---|
| d8-camino-motor-10 | La regla de redondeo de niveles de precio a puntos no esta en la spec y el plan se la deja al motor | src/botsito/domain/valores.py 17-18 (y docs/plan/MASTER_PLAN.md:247; knowledge/spec/strategy_spec.yaml:1052-1083; docs/plan/MASTER_PLAN.html:388) |


## 8. Verificación empírica pendiente

Estado de todo lo que sigue: SIN_VERIFICAR. Esta sección no añade hallazgos: reúne lo que ninguna orden ejecutada dentro de este repositorio puede zanjar, agrupado primero por las cinco fronteras que señaló el dueño (demo de FundedNext, reglamento de la prop firm, un mes limpio del trader, el runner de Windows, el Strategy Tester) y después por todo lo demás que las 17 dimensiones declararon no verificado, fusionado por tema. Ninguna afirmación de este apartado es un defecto del proyecto: es el límite de lo que cabe comprobar leyendo el repositorio. Cobertura: 122 puntos declarados por 17 dimensiones (d8-camino-motor incluida), todos contabilizados una sola vez entre el §8.1 y el §8.2.

### 8.1 Las cinco fronteras que señaló el dueño

#### a) El terminal MT5 / la demo de FundedNext

- **hecho**: existe una cuenta demo (34891752) medida en PROJECT_STATE.md:366-374, que dio instrumento y reloj, no límites de riesgo [camino_motor, pregunta 3].
- **hecho**: F16 y F17 —los que grabarían tics de esa demo— no se han abierto. F16 depende solo de F15 (ya validada), pero el orden E del plan (MASTER_PLAN.md:136-137) los deja detrás de F14; F17 además depende de F16, sin empezar [camino_motor, tabla A y pregunta 1].
- **hecho**: la transcripción real con GPU del pipeline de audio (`add_dll_directory`, `MotorWhisper._cargar`) no se ejecutó en esta auditoría [exec-windows-07].
- **hecho**: que `PERIOD_H4` del terminal MT5 de FundedNext coincida con las 17:00 America/New_York en los días de desajuste no se verificó contra el terminal real; queda en ADR-0005 como aproximación que solo F17 puede comprobar [d5-relojes-datos-02].
- **hecho**: cómo reacciona MT5/FundedNext ante un volumen que no es múltiplo de 0,01 no se comprobó; quedan las dos hipótesis abiertas, rechazo o redondeo del puente [d3-guardias-forma-03, d1-interprete-02].
- **hipótesis** (cómo se comprobaría): abrir el terminal MT5 sobre la cuenta demo 34891752, dejarlo grabando tics durante F16/F17, y contrastar ahí el cierre real de H4, el volumen no múltiplo del paso y el efecto de fin de semana/desconexión que hoy son solo "conocimiento del broker" sin ejecutar [d1-interprete-02].

#### b) El reglamento de la prop firm (FundedNext)

- **hecho**: no se consultó ninguna fuente externa al reglamento; todo lo citado abajo sale del repositorio [d8-camino-motor-01].

```
$ python (parametros.yaml, categoria prop_firm)
filtro_noticias      CONFIRMED  regla     ADR-0022
reloj_dia_riesgo     DEFAULT_AMBIGUOUS servidor ADR-0015 A-19
cuenta_objetivo      CONFIRMED  fondeada  ADR-0012  consumido_por F33
cuenta_pruebas       CONFIRMED  demo      ADR-0012  consumido_por F17,F33
saldo_inicial_cuenta CONFIRMED  100000    ADR-0012  consumido_por F24,F33

$ cat knowledge/evidence/v4/ev-v4-012524-0ef85a89.yaml (extracto)
tipo: UNKNOWN
cita_literal: La idea creo que sería Funded Next ... 5% como drawdown máximo de
  pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí
```

  Ningún parámetro `prop_firm` guarda un límite de pérdida. MASTER_PLAN.md:246 añade, sin cita, "5 % diario sobre equity a medianoche de servidor, 10 % total" — que contradice el 8 % que el trader recuerda de memoria en la cita de arriba. docs/research/2026-09-03-del-corpus-al-bot.html:483 y :650 solo dan "2.000 mensajes diarios" y un enlace a simtrade.io, un tercero, no el reglamento oficial; el resto del fichero, fuera de las líneas 328/483/650, no se leyó [d8-camino-motor-08]. Los únicos frenos reales del repositorio son del trader, no de la prop firm: `perdida_maxima_diaria` = 4,5 % sobre `saldo_inicial_dia` y `perdida_maxima_semanal` = 9 % sobre `saldo_actual`.
- **inferencia** (de la aritmética sobre 100 000 USD y 0,5 % por pérdida con ADR-0020, ejecutada en camino_motor Anexo C): el freno semanal del trader (9 %) ya supera el 8 % que el propio trader recuerda como total, y dos semanas seguidas a ese freno erosionarían el saldo un 17,19 %, por encima del 10 % que MASTER_PLAN.md cita sin fuente.
- **hecho**: el signo neto de una salida en break-even (comisión y deslizamiento en FundedNext) no se midió [d2-literal-b-02]; si existe un límite semanal o solo uno total, y sobre qué base, no se leyó del reglamento [d2-literal-b-03].
- **hecho**: si FundedNext mide el límite diario sobre pérdida realizada o sobre equity flotante, y en qué franja cae su límite duro, sigue en A-19 ABIERTA; el impacto de "perder la cuenta" es hipótesis, no medición [d1-interprete-03].
- **hecho**: la línea "HECHO en F11" de MASTER_PLAN.md:245 podría referirse solo a instrumento/broker/ejecución; no se leyó el informe de F11 para saber si `prop_firm` quedó excluida a propósito [d8-camino-motor-07].
- **hipótesis** (cómo se comprobaría): leer el reglamento oficial de FundedNext (no un tercero como simtrade.io) y fijar por ADR los cinco datos que faltan: límite diario, límite total, base equity/balance, hora de corte, y política de noticias/consistencia/mensajes.

#### c) Un mes limpio del trader

- **hecho**: el material de fidelidad son 19 días de mayo de 2026 (6 dev, 13 holdout); los xlsx de enero, abril y agosto (entrada, SL y R de 143 operaciones) no se abrieron; el de mayo no se toca por ser holdout [d2-fidelidad-huecos-02].
- **hecho**: el re-sorteo no se ejecutó sobre el paquete real de la sesión 1 porque recomputaría sobre velas de mayo; se demostró con el kit sintético de los tests, que pasa por las mismas funciones comprobar/construir/escribir [d7-metodo-01].
- **hecho**: `kit build` de un paquete de sesión 2 está prohibido en el original y el clon no tiene `data/`; la cifra "se piden 40 casos y el universo tiene 22" sale de un comentario de `vistos.yaml:41`, no de una ejecución [d7-metodo-02].
- **hecho**: los valores reales de rho intra-día, las marginales del kappa y el número de operaciones por partición exigirían abrir el xlsx (permitido en dev, prohibido en holdout); se usaron como supuestos 68/19 por día y rho entre 0,1 y 0,3, sin medir [d7-metodo-03].
- **hipótesis** (cómo se comprobaría): abrir enero/abril/agosto —ya están en el repositorio, no son holdout— para fijar el nivel 0 y el nivel 1 empíricos de esas 143 operaciones, y pedir al trader un mes adicional posterior a mayo para no seguir descontando de los 13 días de holdout ya reservados a F26.

#### d) El runner de Windows en CI

- **hecho**: la CI corre en un único job ubuntu-latest; el job de Windows "se añade en F29" según el propio workflow y no existe hoy [camino_motor, tabla A, fila F29].
- **hecho**: no hay WSL ni Docker en esta máquina; que las mutaciones M2, M3, M5 y M6 pasarían en ubuntu-latest es inferencia (`os.linesep`, locale UTF-8 del runner, orden de `PosixPath`); para M3 se usó el proxy `PYTHONUTF8=1` [exec-windows-01].
- **hecho**: `uv lock --check` real dentro del hook no se ejecutó —el shim devolvió 0 sin correrlo, `uv lock` está prohibido—; `uv run --no-sync lint-imports` en un clon sin `.venv` tampoco, se sustituyó por el `lint-imports.exe` del venv [exec-windows-02].
- **hecho**: la versión de la base tz de ubuntu-latest, su `TZPATH`, y la versión exacta de Python que instala `uv python install` en CI no se comprobaron [exec-windows-03, exec-windows-04].
- **hecho**: el mojibake de la salida UTF-8 de la CLI en una consola PowerShell estándar no se comprobó de forma representativa: la sesión del arnés fuerza `PYTHONIOENCODING` y `OutputEncoding` a utf-8 [exec-windows-05].
- **hecho**: no se corrió ninguna suite completa contra una mutación en un runner real; "ningún test lo discrimina" en M1, M7, M8 y M9 se apoya en los tests concretos ejecutados y en grep de quién llama a esas funciones [exec-windows-08].
- **hecho**: que el job de CI falle en GitHub por `huso_grafico` en minúsculas es inferencia de una simulación local (tzdata en zip, `python -S`), no de una ejecución en ext4 ni en el runner [d4-registro-01, d4-registro-02].
- **hecho**: que los 13 casos de `test_hoja_sesion_docx` corran sin skip en ubuntu-latest es inferencia de un clon limpio en Windows (95 passed, 0 skipped); no se observó en el runner real, y no hay `gh` en PATH ni acceso al MCP de GitHub (401) para leer sus logs [d3-tests-contrato-01].
- **hipótesis** (cómo se comprobaría): un runner Windows real en CI (F29) y una máquina Linux real (WSL o Docker) para dejar de simular con proxies lo que hoy son inferencias sobre ubuntu-latest.

#### e) El Strategy Tester de MetaTrader 5

- **hecho**: el plan solo mide contra el Strategy Tester en F30 (100 % de decisiones, niveles ≤ 1 tick, con CI Windows) y F32 (> 95 % de operaciones, mediana de entrada < 0,3 pips, < 15 % de expectativa); ninguno de los dos criterios cubre "vivo en FundedNext" [camino_motor, Anexo D].
- **hecho**: hoy no hay nada que correr en el Strategy Tester —`src/botsito/engine/` tiene una línea—, así que el impacto en dinero es inferencia, no medición: los impactos de las guardias de forma mutadas [d3-guardias-forma-02] y los del registro (hallazgos 01, 04, 05, 06, 07, 08 y 10) [d4-registro-07] se calculan sin ejecutar nada; los números de los hallazgos 01 y 09 de d8-camino-motor (caja de 10 pips, resolución en la misma M1) son ilustrativos, no medidos sobre velas reales —medirlos sobre mayo está prohibido por ser holdout— [d8-camino-motor-05].
- **hipótesis** (cómo se comprobaría): que exista el motor (F18-F24) y el puente MQL5 (F28-F29) para correr F30 y F32 contra el Strategy Tester; hasta entonces cualquier cifra de "cuánto cuesta un fallo" es ilustración, no medición.

### 8.2 Todo lo demás declarado SIN_VERIFICAR, agrupado por tema

98 puntos restantes (122 totales menos los 24 ya citados en el §8.1), agrupados por tema para no repetir dimensión por dimensión. Convención: salvo que se indique otra etiqueta, cada bloque abre con lo declarado como **hecho** (lo que el propio agente no ejecutó, leyó o comprobó) y cierra con una **hipótesis** de cómo se comprobaría.

**Intérprete de `forma`, nunca construido.** **hecho**: ningún hallazgo de fidelidad, de guardias de forma o de camino al motor se demostró ejecutando un intérprete; todos salen de recorrer las formas en `s2/forma.py` o de deducir por los acumuladores [d2-fidelidad-afirmaciones-05, d2-fidelidad-huecos-07, d2-literal-b-04, d8-camino-motor-04]. **hipótesis**: construir el prototipo que d8-camino-motor da por inviable "sin código por nombre" y correrlo primero contra escenarios sintéticos.

**CI remota / GitHub: nada verificado de punta a punta.** **hecho**: el MCP de GitHub falla con 401 y no hay `gh` en PATH; no se comprobó ningún resultado real de un job de CI, el estado de la protección de rama de `main`, si el merge `0a9612d` y los tags `stable/*` llegaron al remoto (`origin/main` local = `1cf5aa2`), ni si `actions/checkout@v5` deja HEAD separado [exec-checks-01, exec-git-01, exec-cli-07, d6-evidencia-01, d6-evidencia-02]. **hipótesis**: arreglar la autenticación del MCP o instalar `gh`, y leer los logs de Actions y la configuración de protección de rama directamente.

**Cobertura y mutación: dirigida, no sistemática.** **hecho**: la cobertura es in-process (no mide subprocesos, que aquí son git y ffmpeg); los mutantes M1-M3 solo corrieron contra 13 de 46 ficheros de test; no se construyeron variantes para varias líneas de `modelo.py` (363-366, 444-446, 718-722, 1001-1002) ni de `knowledge.py` (182-183, 203-204); mypy no se comprobó sin el grupo `asr`; no hubo mutación sistemática, solo 3 mutantes dirigidos [exec-checks-02, exec-checks-03, exec-checks-04, exec-checks-05, exec-checks-06, exec-checks-07]. **hipótesis**: correr mutación sistemática sobre el 100 % de `modelo.py` y `knowledge.py`, y mypy en CI con el grupo `asr` incluido.

**Límites del historial de git para medir coste.** **hecho**: git no registra tiempo de trabajo real entre ráfagas de commits ni distingue horas de agente de horas del dueño; si los 9 cambios de `spec_version` cumplen el criterio de ADR-0013 no se auditó regla a regla; qué parte del retrabajo posterior a un tag es extensión legítima frente a corrección depende de los mensajes de commit; que el reflog local esté completo "lo parece" desde el commit inicial, sin forma de contrastarlo en otra máquina [exec-git-02, exec-git-03, exec-git-04, exec-git-05, exec-git-06]. **hipótesis**: registrar tiempo de forma explícita (no inferida de git) y auditar regla por regla los 9 saltos de `spec_version` contra ADR-0013.

**CLI vs YAML: recuentos y hashes no recomputados de forma independiente.** **hecho**: `data check` sobre mayo no se ejecutó (holdout); `kit check` con datos sobre un paquete manipulado no se probó (exige copiar velas de mayo); el hash de `spec_manifest.yaml` no se recomputó de forma independiente; la igualdad byte a byte de `docs/spec` con lo generado no se rehizo fuera de la CLI; los recuentos "11 items con extractor llm" y "1 cita con tiempos de segmento" no se recontaron por separado; `corpus check`/`transcript check`/`frames check` se contrastaron contra los registros de `knowledge/`, no contra tamaños en disco; los exit codes de dos comprobaciones de `run3.txt` en realidad vienen de `run2.txt` [exec-cli-01, exec-cli-02, exec-cli-03, exec-cli-04, exec-cli-05, exec-cli-06, exec-cli-08]. **hipótesis**: recomputar el hash del manifiesto y la generación de `docs/spec` de forma independiente de la CLI, y recontar a mano los dos recuentos citados.

**Hooks de git: no instalados ni probados en el clon.** **hecho**: ningún clon tenía hooks instalados; las mutaciones y violaciones se hicieron equivalente a `--no-verify`; no se comprobó si el trailer `Fuente:` bloquearía commitear mutaciones; el comportamiento de `instalar_hooks.py` con `core.hooksPath` global o en un worktree no se probó (tocaría configuración global del usuario); la nota "en Git Bash de Windows, lint-imports devuelve 1 al escribir en /dev/null" (`pre-commit:13-14`) no se verificó [exec-windows-06, d3-guardias-citas-04, d5-relojes-datos-04, d6-evidencia-05]. **hipótesis**: instalar los hooks en un clon desechable y commitear deliberadamente una violación para comprobar si el hook la detiene.

**Suite completa de pytest / `make check`: cada dimensión corrió su propio recorte.** **hecho**: por reparto de trabajo (hay un agente dedicado a exec-checks), cada dimensión ejecutó solo sus ficheros relevantes, no la suite completa: d3-guardias-citas (solo `test_spec.py`, `test_adr.py`, `test_spec_docs_generados.py`), d3-guardias-forma (solo `test_spec.py` y `test_spec_docs_generados.py`), d3-tests-contrato (solo `tests/contract`), d4-registro (`test_registro.py`, `test_kit.py`, `tests/contract`), d5-relojes-datos (8 ficheros de datos), d6-evidencia (5 ficheros de historial), d7-metodo (funciones sueltas de `scripts`), d8-camino-motor (solo `spec status`, `spec check`, `kb find`), d1-interprete (solo lectura y grep, ni pytest ni botsito) y d2-literal-a (ni `knowledge validate` ni `spec check` ni pytest, porque el orquestador ya los midió en verde) [d3-guardias-citas-01, d3-guardias-forma-01, d3-tests-contrato-02, d4-registro-04, d5-relojes-datos-08, d6-evidencia-08, d7-metodo-06, d8-camino-motor-06, d1-interprete-08, d2-literal-a-09]. Esto es reparto declarado, no un defecto; lo que sigue pendiente es que nadie corrió la suite completa contra una copia mutada a la vez, solo el `make check` en verde del original que reporta el orquestador.

**El clon carece de `data/`: pruebas dependientes de crudas/fotogramas no se ejercitaron.** **hecho**: sin `data/`, `kit check` sale en 0 por "datos ausentes: solo esquema" y no llega a `paquete.py:395-399`; con datos y `huso_operativa` en minúsculas no se probó, por no copiar `data/` ni tocar días de mayo [d3-guardias-citas-02, d4-registro-03]. **hipótesis**: correr esa comprobación en el repositorio original (no en un clon), con permiso explícito, o preparar un fixture con velas fuera de mayo.

**Transcripción no diarizada ni contrastada con el audio.** **hecho**: la transcripción no separa hablantes; en v6 0:06:05/0:21:28/0:42:22 y en v6 1:52:36/2:02:29/2:05:44-2:05:59/2:20:14 quién habla es atribución por contenido y vocativo ("bro"), no por audio; "7M" frente a "7AM" no se resolvió por audio, solo se verificó que el registro dice "cruda leída" y la cruda no lo contiene; las citas usan una sola capa (corregida o cruda según la dimensión) sin contrastar la otra [d2-fidelidad-afirmaciones-01, d2-fidelidad-huecos-03, d2-literal-a-03, d2-literal-b-01, d2-literal-b-07]. **hipótesis**: reescuchar los tramos señalados con las dos capas de transcripción a la vista y, si hay presupuesto, diarizar el corpus completo.

**Fotogramas no abiertos.** **hecho**: no se abrieron los fotogramas que resolverían el "aquí" de la mecha (v4 1:06:12), del punto más bajo (v1 0:14:54) y del bloque de origen; el fotograma `003906000.png` solo se miró para un caso, sin revisar el resto del tramo v6 1:04:54-1:05:22; no se midió qué vela o máximo ancla el nivel 1 en v4 0:12:30; no se revisó v6 0:35:07 (sin item, citado por AUDITORIA-2026-09-12 para A-21); RN-005 en v1 se validó solo por transcripción; no se miraron fotogramas de la hoja R-09 hacia v6 2:21:05; no se copiaron los 14 GB de `data/fotogramas`, así que las citas de pantalla se apoyan en manifiestos versionados, no en las imágenes [d2-fidelidad-afirmaciones-02, d2-fidelidad-afirmaciones-04, d2-fidelidad-huecos-01, d2-fidelidad-huecos-05, d2-literal-a-02, d2-literal-b-05, d6-evidencia-04]. **hipótesis**: abrir esos fotogramas puntuales con `corpus frames show` (no exigen holdout: son de v1/v4/v6) y, si se copia `data/fotogramas` completo, ejercitar `comprobar_fotogramas` con el `index.jsonl` presente.

**Documentos y preguntas referenciadas, no localizadas en el repo.** **hecho**: la ficha escrita original leída en v3 1:03:48 ("nivel 0 con un umbral de invalidación") no se localizó; el texto exacto de la pregunta enviada al trader el 2026-09-10 para A-11/RN-011 no está en el repo; la pregunta a la que responde el WhatsApp de RN-009 no se ve en la captura [d2-fidelidad-afirmaciones-03, d2-literal-a-05, d2-literal-a-07]. **hipótesis**: pedir al consultor o al trader esos dos textos y la ficha escrita de v3, si existen fuera del repositorio.

**Evidencia y registro: piezas sueltas no clasificadas o no ejecutadas.** **hecho**: no se revisó `knowledge/cases/kit/mapa_parametros.yaml` por si enlaza la geometría de la caja con `stop_fraccion_caja`; no se verificó si la hoja de la sesión 1 mostraba al trader M1 o M15 al confirmar `ev-v4-005319`; del desglose de 11 registros de vídeo que no casan con la cruda solo se analizaron los de las reglas propias de d2-literal-a; los literales que citan evidencia v2/v3 fuera de rango (`ev-v2-003256`) se leyeron por ADR-0014/A-18 sin abrir su transcripción; de 11 registros de feedback con "¿" solo se verificó por lectura que dos (`6e15504f`, `8741c388`) contienen la pregunta del consultor, el resto no se clasificó; `evidence new --extractor llm` (que exige propuesta) no se probó; la rama "duda del glosario" de G6 no se probó (solo la de señales del ASR); dos items de evidencia que se superseden entre sí solo se leyeron, no se ejecutaron; si el hash del manifiesto de spec debería cubrir comentarios de `ambiguedades.yaml` quedó solo anotado, fuera de dimensión [d2-fidelidad-afirmaciones-06, d2-fidelidad-huecos-08, d2-literal-a-06, d2-literal-a-08, d2-literal-b-06, d3-guardias-citas-05, d3-guardias-citas-06, d6-evidencia-03, d6-evidencia-06, d6-evidencia-07]. **hipótesis**: clasificar los 9 registros de feedback restantes, ejecutar `evidence new --extractor llm` una vez, y correr la rama de glosario de G6 con datos reales.

**Geometría y exploración de d1-interprete.** **hecho**: que alguna vela real produzca las secuencias sintéticas de geometría (rompe, se_da_esquema, zona de control, liquidez M15) no se comprobó; de las lecturas elegidas para los HUECO H-01..H-09 solo se ejecutaron algunas alternativas (s01b, s06a2, s08e, s11, s12, s13, s04b, s05b, s05c), otras semánticas de `hecho: X` no se exploraron; la exploración usa un alfabeto de 9 símbolos con pérdidas en unidades de 0,5 % (tope 12/20) sin señales de `equal`, envolvente ni 11:00, así que pueden existir ciclos o estados sin salida fuera de esa abstracción; las citas del corpus `ev-v4-003820` y `ev-v6-003227` se tomaron de F14b:66-72 sin abrir los items; la definición de "candidatas" es heurística (reglas cuyo `cuando` nombra algo presente) [d1-interprete-01, d1-interprete-04, d1-interprete-05, d1-interprete-06, d1-interprete-07]. **hipótesis**: correr el explorador con el alfabeto ampliado (`equal`, envolvente, 11:00) y contrastar la geometría sintética contra velas reales de un mes que no sea holdout.

**Reloj/eventos, BID/ASK y redondeo sin decidir.** **hecho**: en qué lado (BID/ASK) dibujan FX Replay y TradingView las velas sobre las que decide el trader no se comprobó; si otras claves de `_ESTRUCTURALES` (`liga`, `distinta_de`, `posterior_a`, `hecho`) usadas como rama hermana se comportan igual que `resultado:` es deducción de `modelo.py:587`, sin ejecutarlo [d8-camino-motor-02, d3-guardias-forma-04]. **hipótesis**: preguntar al trader/consultor qué lado usa su plataforma, y escribir un caso mutado por cada clave de `_ESTRUCTURALES` para ejecutar, no deducir, su comportamiento.

**Divergencia Oanda/Dukascopy y reloj de FX Replay (A-16).** **hecho**: ni el spread real ni la magnitud de la divergencia Oanda (FX Replay) frente a Dukascopy se midieron; tampoco si FX Replay usa bid, ask o mid de Oanda, ni su reloj; el hallazgo correspondiente se apoya en la ausencia de reglas, no en una cifra [d5-relojes-datos-03, d7-metodo-04]. **hipótesis**: descargar una muestra paralela Oanda/Dukascopy del mismo tramo y medir la divergencia real, tal como pide A-16.

**Huecos del contrato de tests frente al motor futuro.** **hecho**: que la guarda de holdout de F14 vaya a implementarse con el alcance spec/domain es inferencia de `conftest.py:21-22` y `MASTER_PLAN.md:59`, sin leer los briefs de F14; el contrato de literales no recorre `scripts/` ni `mql5/` (hoy solo README), así que si el EA de MQL5 escribe valores a mano ningún contrato de este repo lo vería (afirmado por lectura de `test_no_business_literals.py:145`, sin prueba); si la aritmética de `Porcentaje` impide mezclar en tiempo de ejecución un `Decimal('0.005')` horneado con un `Porcentaje` leído no se contrastó, porque no hay motor sobre el que probarlo [d3-tests-contrato-03, d3-tests-contrato-04, d3-tests-contrato-05]. **hipótesis**: extender el contrato de literales a `scripts/` y `mql5/` antes de F28, y escribir el primer caso de motor que mezcle `Decimal` y `Porcentaje` en cuanto exista F18.

**Registro: costes y journal sin medir.** **hecho**: que el journal de F23 use el `spec_hash` de una lectura distinta de la de los valores es inferencia de `spec/manifiesto.py:168-172` y `registro.py`, sin reproducir; el comportamiento del registro con varios hilos, y su coste en MT5/MQL5 (F28 exporta a `Params.mqh`, fuera del código actual), no se midió [d4-registro-05, d4-registro-06]. **hipótesis**: escribir un test que journalee con dos hashes distintos a propósito y otro con escritura concurrente desde varios hilos.

#### Sueltos, sin tema compartido con otro hallazgo

Todos con etiqueta **hecho** (declarado por el agente que los reportó).

| id | Qué se declaró no verificado |
|---|---|
| [d2-fidelidad-afirmaciones-07] | No se comprobó si la sesión 1 revocó el "cierre agresivo" al cerrar la vela H4 (v3 1:03:14); se dejó como pista para d2-fidelidad-huecos y esa dimensión no la recogió: la pista se pierde entre dimensiones. |
| [d2-fidelidad-huecos-04] | La matriz clasifica por tema con excepciones; algún ítem R o D individual podría estar mal asignado (los 70 H sí se revisaron uno a uno). |
| [d2-fidelidad-huecos-06] | Que "del lado contrario al sesgo" (`esta_al_otro_lado_de`) signifique abajo en sesgo alcista es lectura del agente; la prosa de RN-005 sí es literal ("por debajo […] en sesgo alcista"). |
| [d2-literal-a-01] | El sesgo H4 del ejemplo de v4 0:15:35-0:19:07 (FX Replay, 30 ene 2026) no se comprobó; no afecta a v1 ni a v3, que sí lo dicen. |
| [d2-literal-a-04] | El marco temporal de la vela de RN-004 no se resolvió: el corpus apunta a M15 (v6 0:38:00) y enseña en 1m (v4 0:15:35). |
| [d3-guardias-citas-03] | `kit check` sobre el clon mutado no se corrió: exige `--sesion` y no se averiguó la sesión válida (argparse rc=2). |
| [d3-guardias-forma-05] | `spec status` solo se verificó en F5. |
| [d5-relojes-datos-01] | Octubre de 2026 no se ejecutó por falta de datos; el desajuste se verificó con el fixture del 2025-10-27 y razonando sobre `agregacion.py`. |
| [d5-relojes-datos-05] | La lectura I2 del token `vela_h4_previa` es interpretación literal del agente; no se preguntó al trader ni al consultor. |
| [d5-relojes-datos-06] | La divisa de la cuenta fondeada se supuso USD (unidad de `saldo_inicial_cuenta`); con otra divisa cambia el valor del punto. |
| [d5-relojes-datos-07] | No se revisó si F14b ya define la historia previa del caso, salvo un grep de "envolvente\|ambos extremos\|outside" que no devolvió nada. |
| [d7-metodo-05] | Con qué campo de sesión registrará F14 la verdad de mayo sigue abierto (brief D1); el impacto real de ese hallazgo depende de esa decisión. |
| [d8-camino-motor-03] | Que la respuesta de F14b no cambie ninguna decisión D1-D6 de F14 es inferencia, sin revisión del diseño de F14. |
| [d8-camino-motor-08] | El contenido de docs/research/2026-09-03-del-corpus-al-bot.html fuera de las líneas 328, 483 y 650 no se leyó. |

### 8.3 Dimensiones caídas

Ninguna dimensión figura como CAÍDA en los datos entregados para esta sección.


## 9. Lo que el usuario tiene que decidir

Esta sección solo contiene preguntas cerradas: qué decide el dueño, con qué opciones y qué cuesta cada una. El criterio que ordena qué entra aquí es el mismo de todo el informe: si la decisión no cambia lo que hoy impide abrir F18-F24 sin rehacerlo después, no está. Fuente: dimensión d8-camino-motor (hallazgos d8-camino-motor-01 a 10), el juez de F14b y su contra-juez, y el resumen de d7-metodo.

### 9.1 El método de F14b: qué apaga un hecho, y en qué fase

**hecho.** F14b.md:55-56 deja la pregunta abierta: «¿Un hecho se apaga con una regla que lo pone en "no", o se declara con la duración dentro y el motor la interpreta?», y F14b.md:87-88 la llama «un ADR de método por sí sola» [d8-camino-motor-04].

**hecho.** El juez de F14b construyó tres opciones y las midió con un intérprete de juguete y BFS (grafo de estados) sobre cada una: A (apagar con regla, clase `expira`), B (duración declarada en 8 hechos) e H (híbrido: los hechos del broker se derivan del broker, los frenos leen el acumulador y su `reinicia_con`, y solo `liquidez_tomada` y `zona_perdida` declaran `caduca_con`). Recomendó H.

| Criterio | A · apagar con regla | B · duración declarada | H · híbrido (recomendado por el juez) |
|---|---|---|---|
| Estados sin salida (grafo cerrado) | 0 de 23.620 | 0 de 8.227 | 0 de 8.125 |
| Corte de día/semana con la fase mal puesta | martes parado y muerto hasta el corte semanal | 18 colocaciones en vez de 28 (semana entera parada) | 28, sin cambio: un evento de retraso, no una semana |
| Duraciones sin cita del trader | 8 de 14 reglas nuevas | 5 | 5 (broker y frenos no necesitan cita) |
| Reglas nuevas / reescritas | 14 / 3 (vigentes 25→39) | 4 / 4 | 3 / 6 (el juez afirma que las 6 solo quitan ramas) |
| Hechos / tokens | 6→7 / 20→20 | 6→8 / 20→19 | 6→5 / 20→17 |

**hecho, MATIZADO por el contra-juez (se_sostiene: false).** El contra-juez reprodujo el mismo intérprete y BFS de H y encontró que la recomendación, tal como está redactada, no se sostiene:
- La rama que en teoría impide reentrar en una zona perdida (`zona_perdida.caduca_con`) incluye `se_marca_liquidez_m15` **sin cita** (spec_h:385: «liquidez nueva y fin de ventana SIN CITA»), y esa rama no exige que la nueva zona esté "afuera" como pide el literal que H mismo cita (RN-030, ev-v4-003820-299d7a15: «tiene que ser nuevamente afuera»). Reproducido en `lab/c01_marca_sin_toma.py`: **10 colocaciones seguidas en la misma zona perdida** en una sola sesión, frenadas solo por el tope de pérdida diaria (perdida_dia=4864.54, ~4,86 %), no por cartuchos ni por `zona_perdida`.
- La BFS cerrada de H (69.786 estados, 0 sin salida, `lab/c05b_bfs_por_dia.py`) confirma el mismo mecanismo a escala: el máximo de stops sobre una misma toma de liquidez en **todo** el grafo alcanzable es 10, más del triple de los «tres cartuchos» que el trader fijó (fb-e3eedcaa: «Tras 3 perdidas... Claro») y que la tabla del juez presenta como la garantía de H.
- El "ADR de fase" que el juez promete como remedio no cubre la simultaneidad dentro del mismo evento: cuando la 3ª pérdida y una marca de liquidez nueva caen en el mismo tick, H coloca una orden de más (`lab/c02_perdida_y_marca.py`: 4 colocaciones en vez de 3); lo mismo si la contabilidad de cartuchos se aplica un paso tarde dentro del evento (`lab/c06_fase_contabilidad.py`: 4 en vez de 3, con FASE=tarde). El riesgo 2 que el propio juez había anotado solo lo midió en puntos porcentuales de pérdida, no en operaciones de más.
- La contabilidad de costes que se le presentaría al dueño está mal: `lab/spec_h/strategy_spec.yaml` tiene **4 reglas nuevas, no 3** (RN-032 separa el tope semanal de RN-020, justo la partición que el juez escribió que "no hacía falta"); quedan **19 tokens vigentes, no 17**; y la reescritura de RN-001 quita en silencio la prohibición de `buscar_entradas` durante un freno (vigente hoy en strategy_spec.yaml:411) sin que la lista de reescrituras del juez lo mencione ni exista una decisión que lo autorice.

**Ajuste que el contra-juez exige antes de llevar H al dueño** (no aprobar H tal cual): (1) sacar la rama sin cita `se_marca_liquidez_m15` (y probablemente `alcanza_hora ventana_fin`) de `zona_perdida.caduca_con`, dejando solo la rama citada; si el trader decide que una liquidez nueva sí libera la zona aunque no esté "afuera", que se registre como decisión explícita con la cifra medida (hasta 10 stops seguidos); (2) el ADR de método debe fijar el orden dentro de un mismo evento cuando coinciden una pérdida que agota cartuchos y una marca de liquidez, y añadir una guardia que verifique que ninguna combinación de fases permite más de tres colocaciones sobre la misma toma; (3) corregir la cifra de coste de H (4 reglas nuevas, 19 tokens) y añadir a la lista de reescrituras que RN-001 pierde la prohibición de `buscar_entradas` sin sustituto.

Esto también toca hallazgos ya reportados en otra dimensión con el mismo síntoma de fondo (bot que no encuentra salida o reentra sin control tras agotar cartuchos): d1-interprete-01 y d1-interprete-06 (grep del título en graves_titulos; no se repite su evidencia aquí).

**Pregunta cerrada 1 — forma del ADR de método de F14b (antes de escribir F22):**

| Opción | Qué hace | Coste declarado | Estado |
|---|---|---|---|
| **H corregido** | Hechos del broker derivados; frenos leen el acumulador; solo `liquidez_tomada` y `zona_perdida` caducan por evento, con la fase fijada en el ADR y **sin** la rama sin cita en `zona_perdida.caduca_con` | 4 reglas nuevas (no 3) y 6 reescritas; hechos 6→5; tokens 20→19 (no 17); 2 ADR + enmienda de ADR-0018; 2 tests reescritos; se deshace F14b §0 (RN-010 deja de fijar `operacion_abierta`) | Recomendado por el juez, **rechazado tal cual** por el contra-juez; exige el ajuste de arriba antes de presentarse |
| **B** | Duración declarada en los 8 hechos | 4 nuevas y 4 reescritas; hechos 6→8; tokens 20→19; 7 guardias nuevas; 2 ADR + 1 enmienda | Con la fase mal puesta, días y semanas enteras paradas (medido) |
| **A** | Apagar con regla, clase `expira` nueva | 14 nuevas (8 sin cita directa) y 3 reescritas; reglas vigentes 25→39; 6 guardias nuevas; 2 ADR + 3 enmiendas; 6 preguntas al trader | Mismo fallo de fase que B, más dos modos de fallo que ninguna guardia estática detecta (según el juez) |
| **0 · Aplazar** | No decidir ahora | F14 y con ella F18-F24 siguen bloqueadas; la spec del repo deja el bot muerto tras tres stops (5 estados sin salida medidos) y reentra de un día para otro | — |

En cualquier opción salvo 0, el dueño además tiene que contestar, cerrado:
- (i) ¿La liquidez tomada y no operada caduca en `ventana_fin`? SI por decisión / NO / preguntar al trader. Sin literal; cambia 0 frente a 1 operación al día siguiente.
- (ii) ¿Una límite pendiente a las 15:00 se retira? SI / NO / preguntar. Sin retirarla, se llena a las 16:10 (medido, d1 s06a).
- (iii) ¿Se autoriza abrir A-24, A-25 y A-26 (qué nivel es la liquidez de M15) como precondición de F19? SI / NO. Sin ese evento, ninguna opción (A, B o H) evita que el bot quede sin salida tras agotar cartuchos [d8-camino-motor-04].

### 9.2 El orden del camino al motor

**hecho.** El único documento que ata F14b a F14 es una línea sin commitear: PROJECT_STATE.md:37 «Lo siguiente es F14b (el ciclo de vida de los hechos), que BLOQUEA a F14». Ni MASTER_PLAN.md (F14 depende de F09, F11, F15 — F14-case-library.md:3), ni HANDOFF, ni el propio brief de F14b lo sostienen; el informe de auditoría de material sitúa el bloqueo en F18, no en F14 [d8-camino-motor-05, MATIZADO: el HEAD committeado sí tenía a F14 "EN ESPERA" por otros motivos —defectos de negocio en la spec—, pero sin nombrar a F14b].

**hecho.** Por dependencia textual (tabla A de MASTER_PLAN.md), F16 solo depende de F15 (validada) y hoy podría abrirse; pero el "orden E" (MASTER_PLAN.md:136-137 y 222-223: «la puerta es por dependencia... y por el orden E») la pone detrás de F11-F14 igualmente. F17 depende de F16, así que tampoco está desbloqueada hoy [d8-camino-motor-07, MATIZADO: no son "las únicas dos" desbloqueadas por dependencia — F14 también lo está y es la Next Feature del plan].

**hecho.** La investigación del 2026-09-03 pidió grabar ticks de la demo «desde hoy» porque el spread por hora es «irrecuperable a posteriori» (research:328). Diez días después, `git ls-files | grep -ic tick` da 0: ningún tick en el repositorio ni en `data/`.

**Pregunta cerrada 2 — camino crítico:**

| Opción | Secuencia | Coste / riesgo |
|---|---|---|
| **Declarado** (mantener PROJECT_STATE.md:37 y el orden E) | F14b → F14 → F18 → F19 → F20 → F22 → F23 → F24 → F26 → F28 → ... → F35 (17 eslabones) | Serializa F14 detrás de una decisión que no toca ninguna de sus preguntas D1-D6 (inferencia, a confirmar en la revisión de diseño de F14); deja sin fecha las cuatro decisiones de arquitectura de 9.3, que son las que de verdad obligan a reescribir; los ticks de demo siguen sin grabarse mientras tanto |
| **Propuesto por d8-camino-motor** | En paralelo desde hoy: los 4 ADR de arquitectura de 9.3 + ADR de método de F14b (después del de reloj/eventos) + F14 (brief ya escrito) + F16/F17 (enmendando el orden E) + abrir A-24..A-26 + corregir el token `equal` + funcionalidad de calendario de noticias. Después: F18 → (F19→F20) ∥ F21 → F22 → F23 → F24 | Exige enmendar el orden E por escrito (hoy documental, ninguna guardia de `state check` lo impide) y aceptar que F14 avance sin esperar a F14b |

Nota: F21 (geometría del riesgo, golden 4,08/3,94 ya en el corpus) no necesita los casos de sesgo de F18 y podría adelantarse si F18 separa los tipos de sesgo H4 (inferencia del d8-camino-motor, no verificada con prototipo).

### 9.3 Cuatro decisiones de arquitectura sin ADR (más dos menores) que F18-F23 tomarían por defecto

Estas son las que, si se yerran ahora, obligan a reescribir el motor después; ninguna depende de F14b resuelto primero salvo la última.

**(a) Reloj y modelo de eventos** [d8-camino-motor-01, MATIZADO]. **hecho.** Ningún ADR (0001-0025) fija si el motor evalúa al cerrar cada M1, en cada tick o en eventos de orden; `grep` sobre los 25 ADR solo encuentra "reloj" referido a husos horarios, nunca a la cadencia del bucle. El propio MASTER_PLAN.md ya enruta la decisión a F22 (`:258` "MilisegundoUtc... resuelta por el motor"). **Corregido por el contra-juez de ese hallazgo:** no es cierto que "plan y spec YA se contradigan" hoy — la cita de MASTER_PLAN.html:496 pertenece a una instantánea CONGELADA del 2026-09-03, y MASTER_PLAN.md (el vivo) manda cuando difieren.
Pregunta cerrada: ¿el motor evalúa por cierre de M1, por tick, o por evento de orden? Coste de no decidirlo ahora: se reescriben F18-F23 si la elección inicial no coincide con la que exige el reglamento real de FundedNext (ver b) — un veto medido sobre equity con flotante obligaría a evaluar por tick.

**(b) Reglas de FundedNext** [d8-camino-motor-02, MATIZADO]. **hecho.** ADR-0004:12-13 promete que la categoría `prop_firm` guarda «pérdida diaria y total, lote máximo, presupuesto de mensajes, reglas de consistencia»; los cinco parámetros reales con esa categoría (`filtro_noticias`, `reloj_dia_riesgo`, `cuenta_objetivo`, `cuenta_pruebas`, `saldo_inicial_cuenta`) no son ninguno de esos. La única fuente en el repositorio es un tramo de memoria del trader (ev-v4-012524-0ef85a89, tipo UNKNOWN): «5% como drawdown máximo de pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí»; MASTER_PLAN.md:246 fija «10 % total» sobre equity sin cita, y ADR-0022:89 admite que «el reglamento se lee en F33, meses después de que F22 implemente las reglas». **SIN_VERIFICAR** (declarado por el propio d8-camino-motor): no se consultó ninguna fuente externa (reglamento real de FundedNext); las cifras citadas son solo las que hay en el repositorio.
**hecho, con la aritmética hecha sobre 100.000 USD y 0,5 % por pérdida (ADR-0020):** el freno del trader que sí existe (9 % semanal sobre saldo actual, fb-...-a85b6bc7) permite 18 pérdidas en una semana, `-9 % > 8 %` total de la única evidencia; y dos semanas seguidas a -9 % dan 100.000 → 91.000 → 82.810, es decir -17,19 %, más que el 10 % que cita MASTER_PLAN.md:246 sin fuente.
Pregunta cerrada: ¿se lee el reglamento real de FundedNext ahora (antes de F21/F22) o se sigue difiriendo a F33? Coste de diferirlo: el módulo de riesgo de F21/F22 se escribe sobre una cifra sin fuente y se reescribe cuando se lea el reglamento; coste de leerlo ahora: ninguno declarado en los datos (falta este dato, no se ejecutó).

**(c) Intérprete de la `forma` o código a mano, y frontera con MQL5** [d8-camino-motor-03, MATIZADO]. **hecho.** ADR-0001:32 fija que el contrato Python-MQL5 cubre «parámetros y casos», no reglas; la tabla A describe F18-F21 como módulos por tema (código a mano), pero strategy_spec.yaml:212-213 dice que «el motor de F22-F23 implementa esta lista [de acciones] y ninguna otra» (lenguaje de intérprete). **Corregido por el contra-juez de ese hallazgo:** ADR-0019 sí fija el reparto (F12 valida que el predicado exista; F22 lo implementa mediante un árbol booleano genérico que despacha por nombre a primitivas escritas a mano en los módulos de dominio) y la fase 6 del plan (F28-F30) sí fija qué cruza a MQL5: el contrato mecánico cubre solo parámetros y casos, el dominio MQL5 se escribe a mano como espejo sin traducción línea a línea, y la paridad se demuestra por equivalencia diferencial. **hecho adicional que sigue en pie tras la corrección:** la `forma` no basta para interpretarse literalmente — `perdida_dia` y `perdida_semana` declaran el mismo `reinicia_con: reloj_dia_riesgo` (strategy_spec.yaml:366 y 371); un intérprete no distingue el reinicio diario del semanal sin código específico por nombre. **hipótesis no comprobada con prototipo** (declarado): que un intérprete puro sea inviable.
No es una decisión abierta de fondo (ADR-0019 ya la resuelve), pero sí falta declarar por escrito que el reparto híbrido (árbol genérico + primitivas nombradas) es el que rige, para que F18-F22 no se escriban como módulos aislados sin ese árbol.

**(d) Lado BID/ASK y redondeo de niveles** [d8-camino-motor-09 y d8-camino-motor-10, MATIZADOS, ambos severidad menor/media]. **hecho.** ADR-0005:10 fija el M1 de referencia en BID (`BID_candles_min_1.bi5`); ningún ADR, regla ni parámetro dice en qué lado se traza la caja, la entrada límite, el stop a 0,8 o el objetivo, ni en qué lado evalúa `modelo_llenado`. **Corregido por el contra-juez de ese hallazgo:** que los datos de referencia sean solo BID está declarado con dueño (el brief de F15 deja "velas ASK o spread" para F16). Sobre redondeo: la spec solo redondea el LOTE (RN-027, a la baja, decisión ADR-0016); el stop y el objetivo en puntos fraccionarios (ejemplo: 0,8 × 137 = 109,6) no tienen dirección de redondeo en ninguna regla — MASTER_PLAN.md:247 se lo deja a F18 con la frase «stop al lado conservador», sin decir hacia dónde ni cubrir el objetivo.
Pregunta cerrada: ¿en qué lado (BID/ASK) se mide cada nivel, y hacia dónde redondea el stop y el objetivo a puntos enteros? **SIN_VERIFICAR** (declarado): en qué lado dibujan FX Replay y TradingView las velas sobre las que decide el trader — no se comprobó. Coste de no decidirlo: se rehace la geometría de F21 y el llenado de F24 (impacto de ejemplo, no medido sobre velas reales: en una caja de 10 pips, 1 pip de spread es el 10 % de la caja).

**(e) Calendario de noticias para RN-028** [d8-camino-motor-06, MATIZADO]. **hecho.** ADR-0022 hizo el filtro de noticias bloqueante (RN-028, clase `gate`, `pendiente_definicion: A-17`), justo el supuesto en que F11:144-147 ya había anotado que haría falta «una fuente de datos nueva y una funcionalidad propia, no un parámetro». Ninguna fila de MASTER_PLAN (F15 OHLC, F16 ticks, F17 ticks de demo, F33 demo) trae ese calendario, y el vocabulario de 22 predicados no tiene ninguno de noticia.
Pregunta cerrada: ¿se abre una funcionalidad de calendario de noticias ahora (antes de F22/F23) o se opera sin filtro hasta que exista? Coste de no decidirlo: o el bot opera noticias en la cuenta fondeada —el trader avisó de que puede cerrarla aunque acabe en profit—, o el calendario entra después de F23 como fuente de eventos nueva y obliga a tocar bucle, journal y replay.

### 9.4 Lo que el método de medición de F26 exige decidir antes del pre-registro

**hecho.** El resumen de d7-metodo es directo: «Lo que tiene que hacer creíble la cifra de F26 no prueba lo que dice que prueba, y la muestra no alcanza para afirmar nada.» Cuatro problemas de construcción del kit (kit check pasa con exit 0 sin `data/` y sin comparar particiones; la reproducción byte a byte no prueba anterioridad porque lee el seed del propio fichero; la guardia de ancestro solo mira LABEL_CASE de la misma sesión; un supersede de ronda 2 puede borrar una unidad de ronda 1) están reportados en su propia dimensión con ids d7-metodo-02, 03 (no se repite su evidencia aquí).

**hecho (cálculo estadístico).** El mínimo para distinguir un acuerdo de 0,8 de uno de 0,6 (binomial exacta, alfa 0,05 unilateral, potencia 0,80) es **36 unidades efectivas independientes**; con aproximación normal, 33. Un intervalo de ±10 puntos alrededor de 0,8 pide 60-70 unidades, y alrededor de 0,7, 78-88. Traducido con rho=0,2: 36 si la unidad es el día, 22 si es la sesión H4, 16 si es la operación. **hecho.** holdout-1 tiene 6 días → 10-14 unidades efectivas; los tres holdout juntos, 12 días → 20-28 efectivas. Ninguna combinación de mayo llega a 36 [d7-metodo-06].

**Pregunta cerrada 3 — qué falta decidir antes de abrir PREREGISTRO.md, por su nombre:**

| Decisión pendiente | Qué falta | Referencia |
|---|---|---|
| Unidad de F26 | ADR-0011 §6 y `kappa.py` miden por (caso, sesión H4); PREREGISTRO:17-18 habla de operación con tolerancias de entrada/stop/objetivo; ADR-0021 dice «decisiones -hora, dirección, entrada, stop-»; el brief de F14 deja D1/D2 abiertas. La única unidad que existe en código (sesión) no representa al menos 30 de las 68 operaciones de mayo. Decidir: ¿sesión H4, operación, o decisión discreta? | d7-metodo-07 |
| N mínimo | Fijar 36 unidades efectivas como umbral explícito antes de medir, o aceptar que con el material actual F26 solo puede dar casos concretos y un intervalo que no excluye 0,6 | d7-metodo-06 |
| Qué partición da la nota | Los documentos no coinciden: holdout-1 (6 días) u holdout-2 (3 días medibles). Fijarlo en MASTER_PLAN:203, holdout/README.md, ADR-0021 y ADR-0025 | d7-metodo-05 |
| A-16 (Oanda vs. Dukascopy) | Bloqueante:false con `resuelve_en [F26]`, orden incompatible con PREREGISTRO:17-18 que exige fijar tolerancia antes de abrir. La única medición hoy es de un solo día (15 velas idénticas de 1261, p90 3 pt, máximo 20 pt). Antes de PREREGISTRO: medir Oanda vs. Dukascopy en enero/agosto por hora dentro de 07-15 Madrid; medir precios de entrada/stop de los xlsx contra Dukascopy; medir tasa de casi-rupturas con p99 de \|delta\| para fijar la cifra de tolerancia | metodo_resumen |
| Tratamiento de noticias en PREREGISTRO | Depende de cerrar A-17 (ver 9.3-e) | metodo_resumen |
| Gramática de LABEL_CASE | No representa al menos 30 de las 68 operaciones de mayo; hay que adaptarla a varias operaciones por sesión antes de construir la sesión 2 de etiquetado | metodo_resumen, d7-metodo-07 |
| Kappa del trader | Cero registros LABEL_CASE de ronda 1 hoy; si se quiere el kappa, hace falta una ronda 1 | metodo_resumen |

**hecho.** Sin resolver la unidad, el N mínimo y A-16 en ese orden, cualquier cifra de fidelidad que F26 produzca sobre mayo es, como mínimo, no concluyente frente al umbral de 36 unidades, y como máximo, no comparable entre documentos porque no está dicho qué partición la sostiene.

### 9.5 Checklist cerrado para el dueño

1. F14b: ¿H corregido, B, A o aplazar? (9.1) — y, en cualquier caso salvo aplazar: liquidez tomada en `ventana_fin` (sí/no/preguntar), límite a las 15:00 se retira (sí/no/preguntar), abrir A-24/A-25/A-26 (sí/no).
2. Camino crítico: ¿orden declarado (F14b→F14→fase 5) o el propuesto con los 4 ADR y F14/F16/F17 en paralelo, enmendando el orden E? (9.2)
3. Reloj/modelo de eventos del motor: cierre de M1, tick, o evento de orden. (9.3-a)
4. Reglas de FundedNext: ¿se lee el reglamento real ahora o se sigue difiriendo a F33? (9.3-b)
5. BID/ASK y redondeo de niveles: en qué lado se mide cada nivel; hacia dónde redondea el stop y el objetivo. (9.3-d)
6. Calendario de noticias para RN-028: ¿se abre una funcionalidad ahora o se opera sin filtro hasta que exista? (9.3-e)
7. F26: unidad de medida, N mínimo (36 efectivas), qué partición da la nota, y medir A-16 antes de fijar tolerancia en PREREGISTRO. (9.4)


