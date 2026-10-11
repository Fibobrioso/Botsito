# ENTORNO-CODE · El entorno de trabajo de Claude Code (R0.2, entrada F)

Rama `trabajo/entorno-code`, abierta el 2026-10-10 desde `main` en d32db01 (commit de estado sobre
el merge 7823568, tag `stable/F37k-hoja-de-ruta`). Encargo: `docs/encargos/trabajo-entorno-code.md`.
Tramo: R0 (R0.2 de `docs/plan/HOJA-DE-RUTA.md`).

Antes de abrir se comprobó con git: `main` = `origin/main` = d32db01;
`git rev-parse "stable/F37k-hoja-de-ruta^{commit}"` = 7823568; la CI de `main` sobre d32db01 en
`completed` / `success` (API de check-runs con el sha literal); `git branch -a` solo da `main` y
`origin/main`, y `git ls-remote --heads origin` solo `main`. El paquete es la versión 2:
`.claude/agents/auditor-encargo.md` lleva «5. **El tramo**» (su línea 48).

## 0. Fase 0 · Inventario, sin escribir nada en el repo

Medido el 2026-10-10 sobre bb3e3fd (la apertura, encima de d32db01). El contraste de (a) y (c) lo
hizo un subagente de solo lectura siguiendo el encargo (el `auditor-encargo` del paquete aún no está
instalado: lo instala la fase 1); lo que más pesa se volvió a medir en la sesión («verificado»).
Nada de holdout, `data/`, crudas ni `_proposals`. ESPECIFICACION.md dice «revisado contra el repo en
26326b2»: desde entonces entraron `trabajo/cases-rejilla` y `trabajo/hoja-de-ruta`, así que todo se
contrasta contra d32db01.

### 0.a El paquete contra el repo

Paquete = `C:\Users\USER\Desktop\paquete-skills-code\`. Discrepancias, con su corrección mínima:

| Paquete:línea | Qué dice | Qué hay en el repo | Corrección propuesta |
|---|---|---|---|
| ESPECIFICACION.md:11-16 (E1) | rama, commit, artefacto, riesgo, encargo, Estado, ESPERANDO | el encargo pide además el tramo (encargo:14); está en `contrato.yaml` (`tramo: R0`) | el hook muestra el `tramo` |
| ESPECIFICACION.md:22 (E1) | `guardia.Arbol.motivo_fichero` | no hay clase `Arbol`: es `Politica` (`.claude/hooks/guardia.py:255`), `motivo_fichero(self, ruta)` en `:423`; pide ruta absoluta (`relativa()` devuelve None fuera de la raíz y solo quedan las reglas de nombre) | `guardia.Politica(raiz).motivo_fichero(str(raiz / rel))` (verificado) |
| ESPECIFICACION.md:13-14 (E1) | detecta «PARADA» o «Lo que necesito que decidas» | ningún informe usa hoy «Lo que necesito que decidas»; los encabezados de PARADA varían («## 1. PARADA», «Lo que decide el consultor (PARADA)», «PARADA 2») | detectar «PARADA» o «Lo que necesito que decidas» en cualquier encabezado `#`; el segundo existe desde `fase-cero` |
| ESPECIFICACION.md:35-36 (E2) | «16 de sus 26 filas» | la tabla tiene hoy 28 filas | recontado en 0.b |
| ESPECIFICACION.md:48-49 (E3) | `make rapido T=tests/unit/test_x.py` | la guardia niega todo argumento de `make` con `-` o `=` («solo se admiten objetivos; una opcion o una variable cambia que recetas corren», `guardia.py:1772` y `:1786-1789`, verificado) | `make rapido` sin variables (lint y types) y los tests con `uv run pytest <fichero>` aparte; o cambiar la guardia con su test (PARADA, punto 0) |
| ESPECIFICACION.md:63-66 (E4) | plantillas: `<`, `>`, `{`, `*` o `0N` | `.claude/skills/ingerir-sesion/SKILL.md:89` nombra `docs/validation/SESION-NN-EXTRACCION.md` (verificado), que no existe; con E4 tal cual el test fallaría sobre una skill que esta rama no puede tocar | añadir `NN` a las marcas de plantilla |
| ESPECIFICACION.md:76-79 (E5) | reescribir la frase «Las tareas repetidas tienen skill» | existe en `CLAUDE.md:21-22`; y `tests/unit/test_revisor.py:154-159` exige literal OTRA frase de CLAUDE.md («Antes de declarar una rama lista para revisión: …», verificado) | reescribir la de :21-22 y dejar intacta la que exige el test |
| ESPECIFICACION.md:83-85 (E5) | alinear ERRORES-RECURRENTES con RITUAL, «con recuadro si la sección es un texto cerrado» | la contradicción es real: `ERRORES-RECURRENTES.md:13` dice «Se apunta al declarar la rama lista» (verificado) y RITUAL (punto 2 del commit del contrato) y `cerrar-rama` dicen al cerrar. Pero el recuadro es el régimen de `docs/validation/` (CLAUDE.md, «Regimenes de cambio»); un runbook es vivo | editar :13 directamente, con fecha y rama en el texto |
| ESPECIFICACION.md:96-97 (E7) | solo falta `arnes` | falta `arnes` (`solo_lectura.py:37-40`; `motor arnes --salida`, `cli.py:3091`); y también escriben y faltan: `motor visor` (por defecto en `data/visor`), `kit hoja` (un .docx en la raíz), `casos visto` («construye y ancla»), `data download` y `download-ticks`, `data aggregate --salida`, `evidence contradictions` y `evidence reject`; y `kit kappa --incluir-holdout` ABRE el holdout y gasta la pregunta | PARADA, punto 2: solo `arnes` (la letra de E7) o la lista medida, con `--salida` como marca y negando `--incluir-holdout` |
| auditor-encargo.md:41-42 | los heredados se buscan en HISTORIA | viven en PROJECT_STATE («### Pendientes heredados») y en la hoja de ruta como `HER:n` | añadir PROJECT_STATE y `docs/plan/HOJA-DE-RUTA.md` a las fuentes |
| auditor-encargo.md:43-44 | grep de «pendiente con dueno» | el repo escribe «dueño» con ñ (p. ej. ACTIVACION-A42.md); sin ñ el grep da 0 | `grep -i "pendiente con due"` |
| auditor-encargo.md:46-47 | «Nunca `--help`» | no sale de CLAUDE.md ni de un ADR: es la lección del consultor sobre el comando prohibido (UMBRAL-MAYO.md; HISTORIA) | citar esa fuente (más estricto para un agente que solo lee: se queda) |
| auditor-encargo.md:48-50 | «una entrada de HOJA-DE-RUTA (la que lleva el `tramo`)», «la siguiente del camino crítico» | el `tramo` es el `## ` (R0), no la entrada `###` (R0.2) (`CONTRATO-DE-RAMA.md`; `scripts/contrato_rama.py`); la entrada se encuentra por su `NA:`; la hoja no define «camino crítico»: ordena por «Depende de», y la F dice que la hoja manda el orden | «el `tramo` es el `## `; la entrada es el `###` con la `NA:` del encargo; di si sus «Depende de» están HECHAS y si es la siguiente según la hoja y la F» |
| fase-cero/SKILL.md:29-41 | no dice quién lee la columna de fechas | ADR-0072 §2 y CLAUDE.md: la lee Aleks | añadir: «la columna de fechas no la lee la sesión ni el auditor: la lee Aleks (ADR-0072); si la fase 0 la necesita, PARADA» |
| activar-sesion/SKILL.md:24 | ejemplo de herencia: «el refiltrado de v7-v10, HISTORIA:4387 y :4414» | el refiltrado está HECHO (ACTIVACION-A42.md §2.2; respuesta 3 del consultor en `trabajo/hoja-de-ruta`; la E ya no lo lleva) | cambiar el ejemplo por el heredado 15 (A-18, hoja R1.1) y añadir la hoja de ruta a las fuentes |
| activar-sesion/SKILL.md:44-46 | el arnés, «las órdenes recientes lo prohíben salvo autorización» | cierto en los encargos; ADR-0070 no lo prohíbe: fija cuándo una corrida habilita mayo; la corrida es R3.1 | citar la hoja R3.1 y ADR-0070 §3 |
| activar-sesion/SKILL.md:55 | `grep -rn "A-n" CLAUDE.md docs/runbooks PROJECT_STATE.md` | la hoja de ruta lleva las A-nn como `ID:` | añadir `docs/plan/HOJA-DE-RUTA.md` |
| activar-sesion/SKILL.md:61-63 | `feedback new` con `--objetivo-tipo ambiguedad`, `RESOLVE_UNKNOWN`, `--recibido-el`, `--procedencia` | son obligatorias además `--sesion --fecha --medio --objetivo-id --accion --respuesta --registrado-por` (`cli.py:3222-3238`); `RESOLVE_UNKNOWN` va con `--accion` | el comando entero, como la plantilla de `knowledge/feedback/README.md`; para parámetros, `--valor-canonico` |
| entregar-rama/SKILL.md:20 | «toca la plataforma: … zoneinfo» | RITUAL no nombra zoneinfo; lo sostienen los encargos (cases-rejilla, activacion-a42) | citar esos encargos |
| entregar-rama/SKILL.md:55-56 | «aviso si pasa de 23.000 (el tope del test es 25.000)» | el consultor lo prohibió: «No hay ningún "margen de 23.000"… No lo vuelvas a citar» (`docs/encargos/trabajo-reabrir-y-fuente-documental.md:61`) | «`wc -c`; el tope es el de `test_project_state.py`; el saldo o el tope que fije el encargo» |
| entregar-rama/SKILL.md (falta, paso 4) | el informe completo no prepara las líneas del commit del contrato | RITUAL (puntos 3 y 4) y este encargo las piden; solo `activar-sesion` lo hace | añadir: «las líneas de la Next Action y de la hoja de ruta que salen, entran o cambian, preparadas para el commit del contrato; en la rama no se tocan» |
| entregar-rama/SKILL.md:38 y :63 | `gh run` para la CI | en esta máquina el clasificador niega `gh run list`; `gh run view <run> --log-failed` funciona, y el estado se lee por la API de check-runs con el sha literal (RITUAL) | «el estado, por la API de check-runs con el sha literal (RITUAL); el log, `gh run view <run> --log-failed`» |
| retomar-rama/SKILL.md:14-28 | no lee el tramo; no remite a «Por donde se empieza» | `contrato.yaml` lleva `tramo`; CLAUDE.md «Por donde se empieza» | añadir el tramo y su entrada de la hoja, y remitir a CLAUDE.md |
| `.claude/skills/abrir-rama/SKILL.md:81` (repo) | verificación: `git diff main --stat` = encargo, contrato, PROJECT_STATE y HISTORIA, «nada mas» | su propio paso 4 exige el artefacto estadiado en el primer commit | añadir el artefacto (E6 ya edita esa skill) |

**Lo que está bien** (comprobado por el subagente): todas las rutas que citan las piezas existen;
los encabezados de CLAUDE.md citados existen; las opciones de la CLI citadas existen (`feedback
trace|pending|apply --sesion --check`, `spec docs|manifest --escribir`, `motor arnes --salida`); lo
que da por hecho `comparar-con-main` es cierto (las tres claves de `[rutas]`, `.gitignore:19`, el
mensaje de `paquete.py` al faltar un manifiesto, `casos_reservados`); los cinco sitios de cerrar
una ambigüedad cuadran con AMBIGUEDADES.md; `pytest-xdist` no está ni en `pyproject.toml` ni en
`uv.lock`; `revisor.md` lleva `model: sonnet` y `test_revisor.py` admite `opus`; ninguna pieza
contradice los papeles de ADR-0072.

**E6, el paso 1 de `abrir-rama` hoy y lo que le falta.** Hoy: `git checkout main`, `git status
--short` vacío y `git rev-parse --short main` igual al sha del encargo (`abrir-rama/SKILL.md:43-44`).
Le falta, para cubrir E6 y lo que repite cada encargo a mano: (1) `git fetch origin` y
`main` = `origin/main`; (2) el último tag de HISTORIA (la última línea `- Tag: \`stable/…\`` de sus
registros de cierre, todos con esa forma) apunta al merge: `stable/<tag>^{commit}` = `main^1`, y está
en origin (`git ls-remote --tags`); (3) la CI de `main` en `success` por la API de check-runs con el
sha literal (RITUAL); (4) ninguna otra rama local (no solo `trabajo/*`: también `feature/*` y `fix/*`)
ni `fix/*` en origin; (5) si algo no cuadra, PARA. Y ampliar sus Entradas, Herramientas y
Verificación.

### 0.b E1, E2 y E3

**E1.** La función es `Politica(RAIZ).motivo_fichero(ruta)` (`.claude/hooks/guardia.py:255` y
`:423`); `estado_sesion.py` la importa como `solo_lectura.py:24` (`import guardia`, misma carpeta) y
la llama con la ruta ABSOLUTA de cada fichero de su lista cerrada antes de abrirlo. La lista:
`contrato.yaml`, `docs/encargos/<rama>.md`, el artefacto, `PROJECT_STATE.md` (y, si se muestra la
entrada del tramo, `docs/plan/HOJA-DE-RUTA.md`). El tramo sale de `contrato.yaml`. Git solo de
lectura (`branch --show-current`, `log -1 --oneline`).

**E2.** La tabla de `docs/runbooks/ERRORES-RECURRENTES.md` tiene hoy **28 filas** (en 26326b2 tenía
26). Leída su columna de hallazgos del consultor, fila a fila:

| Clase | Filas | Cuántas |
|---|---|---|
| sin hallazgos del consultor | `ajustes-cierre`, `cerrar-a29-a36`, `reabrir-y-fuente-documental` (este, un error del consultor sobre su propia orden) | 3 |
| con hallazgos, y la fila dice que el revisor los vio o que no se le escapó ninguno | `cuarentena-por-condicion`, `activacion-a42`, `adelgazar-estado` (lo vio como a2 y lo dio por menor), `cases-rejilla`, `hoja-de-ruta` | 5 |
| con hallazgos sin constancia de que el revisor los viera | `guardias-claude`, `dieta-y-skills`, `cuarentena-por-defecto`, `escenarios-por-sesion`, `freno-peticiones`, `cierres-de-mercado`, `fuentes-ftmo`, `renovar-cierres`, `historial-sin-git`, `sesion-04`, `filtradas-escenario-b`, `filtradas-con-tramos`, `ventana-ev-v9-003456`, `respuestas-ftmo`, `guardias-citas`, `reloj-invierno`, `respaldo-a11`, `umbral-mayo`, `guion-mismo-comando`, `demo-ejecucion-1` | **20** |

De las siete últimas filas, 4 están en la tercera clase (respaldo-a11, umbral-mayo,
guion-mismo-comando y demo-ejecucion-1). La cifra de la
especificación («16 de 26», «6 de las 7 últimas») no sale con este criterio: la tabla tiene dos
filas más y varias de la tercera clase son errores del consultor o de la sesión que el revisor no
tenía con qué ver (p. ej. `fuentes-ftmo`, `ventana-ev-v9-003456`, `respuestas-ftmo`). La propuesta de
E2 se sostiene igual: la fila de cada cierre anota desde esta rama el modelo del revisor.

**E3.** Medido el 2026-10-11 en un clon `git worktree add --detach` de `bb3e3fd` en la carpeta
temporal de la sesión, con su propio `.venv` (`uv sync --locked --group dev` y, solo en el clon,
`uv pip install pytest-xdist` 3.8.0: ni `pyproject.toml` ni `uv.lock` del repo se tocaron). Cada
paso de `make check` se ejecutó con su misma orden, cronometrado por un guion de la carpeta
temporal (la ampliación de `pico_memoria.py medir` para que apunte la duración es de la fase 1).

| Paso de `make check` | Segundos | Salida |
|---|---:|---|
| `contrato` | 0,6 | 0 |
| `lint` (ruff check / ruff format) | 1,4 / 0,2 | 0 |
| `types` (mypy / mypy --strict de las guardias) | 14,0 / 0,7 | 0 |
| `contracts` (lint-imports) | 2,2 | 0 |
| `test` (pytest en serie) | 1.084,2 | 1 (ver abajo) |
| `state` | 1,1 | 0 |
| `config` | 0,4 | 0 |
| `knowledge` | 82,8 | 0 |

Total ≈ 1.188 s (19,8 min); el 91 % es `test` y el 7 % `knowledge`.

El único fallo, el mismo en todas las ejecuciones (serie y las cinco en paralelo), es
`tests/unit/test_rutas_windows.py::test_las_rutas_por_defecto_con_el_rotulo_mas_largo_caben_en_este_repo`:
la ruta absoluta del clon en la carpeta temporal da 263 caracteres frente al límite de 259. Es del
sitio del clon, no del código: en el repo real el mismo test pasa (sello de `bb3e3fd`).

Los veinte tests más lentos (en serie, `--durations=20`):

| s | Test |
|---:|---|
| 81,8 | `tests/unit/test_citas_supersedidas.py::test_knowledge_validate_lleva_g1` |
| 80,5 | `tests/unit/test_retirados.py::test_el_repo_real_retira_uno_y_ninguna_salida_lo_nombra` |
| 78,5 | `tests/unit/test_cli.py::test_knowledge_validate_real_repo` |
| 76,2 | `tests/unit/test_cli.py::test_cli_entrypoint_runs` |
| 72,7 | `tests/unit/test_historial_sin_git.py::test_con_git_las_lineas_ok_son_las_de_main` |
| 56,8 | `tests/contract/test_evidence_history.py::test_repositorio_real_sin_modificaciones` |
| 32,8 | `tests/unit/test_kit.py::test_las_tres_guardias_semanticas_de_decidida_saltan_de_verdad` |
| 16,1 | `tests/contract/test_feedback_history.py::test_repositorio_real` |
| 11,8 | `tests/unit/test_historial_sin_git.py::test_sin_git_ninguna_linea_dice_intacto_y_cada_comprobacion_avisa` |
| 11,1 | `tests/unit/test_historial_sin_git.py::test_una_afirmacion_de_historial_que_no_pasa_por_historial_hace_fallar_validar` |
| 7,0 | `tests/contract/test_ensayo_marzo.py::test_ensayo_de_marzo_de_punta_a_punta` |
| 7,0 | `tests/unit/test_historia.py::test_historia_solo_se_amplia` |
| 6,3 | `tests/unit/test_historial_sin_git.py::test_con_git_y_el_proyecto_fuera_de_la_raiz_tampoco_dice_intacto` |
| 6,0 | `tests/unit/test_freno_peticiones.py::test_un_bucle_de_5000_peticiones_distintas_no_pasa_del_corte` |
| 4,6 | `tests/contract/test_repository_integrity.py::test_no_crlf_in_tracked_text_files` |
| 4,3 | `tests/unit/test_preparar_a21.py::test_sin_mirar_al_futuro_la_zona_existe_desde_el_cierre_del_breaker_con_cada_lectura` |
| 3,9 | `tests/unit/test_fidelidad_marzo.py::test_la_regla_del_mes_decide_los_cupos_y_queda_en_particiones` |
| 3,3 | `tests/contract/test_golden_citas_f07.py::test_las_citas_de_referencia_existen_como_evidencia` |
| 3,0 | `tests/unit/test_cli.py::test_pending_no_da_por_reflejado_lo_que_no_puede_comprobar` |
| 2,9 | `tests/unit/test_kit.py::test_paquete_determinista_y_check` |

Lo que dicen: los cinco primeros (≈ 390 s, el 36 % del paso `test`) ejecutan cada uno
`knowledge validate` sobre el repo real, que es lo mismo que el paso `knowledge` (82,8 s). Es la
palanca más grande que sale de la medida, y no es ninguna de las dos de E3.

Serie frente a `pytest -n auto` (12 procesadores lógicos; xdist no imprime cuántos trabajadores
levanta), las dos con `pico_memoria.py ejecutar`, que suma la memoria comprometida de todos los
procesos del árbol:

| Ejecución | Segundos | passed / skipped / failed | Mismos nombres y estados que en serie | Pico (MiB) |
|---|---:|---|---|---:|
| serie | 1.084,2 | 2.494 / 10 / 1 | — | 243 |
| `-n auto` 1 | 440,7 | 2.494 / 10 / 1 | sí, 0 diferencias | 1.161 |
| `-n auto` 2 | 409,8 | 2.494 / 10 / 1 | sí, 0 diferencias | 1.133 |
| `-n auto` 3 | 425,6 | 2.494 / 10 / 1 | sí, 0 diferencias | 1.138 |
| `-n auto` 4 | 419,4 | 2.494 / 10 / 1 | sí, 0 diferencias | 1.118 |
| `-n auto` 5 | 504,1 | 2.494 / 10 / 1 | sí, 0 diferencias | 1.156 |

La comparación es por nombre (`classname::name` del JUnit XML de cada ejecución contra el de la
serie), no solo por recuento.

- (a) Mismo resultado: sí, en las cinco.
- (b) La guarda del holdout con `-n auto`: `pytest -n auto -m provoca_holdout` da 9 passed y
  `pytest -n auto tests/unit/test_guarda_holdout.py` 18 passed: los tests que la provocan a
  propósito la siguen viendo saltar en cada trabajador.
- (c) Escrituras: `git status --porcelain` del clon, vacío tras las siete ejecuciones. Límite: no ve
  lo ignorado por `.gitignore` (`data/`, `corpus/`).
- (d) Memoria: el pico sube de 243 a 1.118-1.161 MiB (× 4,7), y el proceso mayor baja de 191 a
  175 MiB: sube por el número de trabajadores, no por un test. El tiempo baja de 18 a 7 minutos
  (× 2,5).
- La línea `PICO DE MEMORIA` mide lo mismo con xdist (la suma del árbol de procesos, que incluye a
  los trabajadores), así que sus cifras no se comparan con las de antes sin decirlo.

### 0.c Solapes y huecos

**Solapes con lo que ya hay** (ninguna contradicción salvo las de la tabla de 0.a):
- `fase-cero` y `abrir-rama`: `abrir-rama` dice que el artefacto «nace con el inventario» si el
  encargo lo pide; en la práctica nace con su cabecera y EN CURSO, y el inventario lo escribe
  `fase-cero` en su commit. Se alinea en `abrir-rama` (E6 ya la toca).
- `auditor-encargo` y el revisor (eje b): los dos parten el encargo en requisitos, uno al empezar y
  otro al acabar; comparten `solo_lectura.py`, cuyo mensaje solo nombra al revisor (se generaliza
  con E7).
- `entregar-rama` y el revisor: el paso 1 de `entregar-rama` (la tabla Hecho/Parcial/No hecho) es
  la misma que el eje (b) del revisor; redundancia buscada (E5 hace que el revisor compruebe que
  esa tabla está).
- `entregar-rama` y `cerrar-rama`: coherentes (la CI por `fix/` solo se repite si no está en verde;
  la fila de ERRORES-RECURRENTES la escribe `cerrar-rama`, que es lo que E5 alinea).
- `activar-sesion` e `ingerir-sesion`: complementarias (`ingerir-sesion` manda el cierre de
  ambigüedades a «otra rama»).
- `retomar-rama` y E1: misma regla de ESPERANDO; `retomar-rama` no remite a «Por donde se empieza»
  de CLAUDE.md (se añade).

**Lo que repiten los diez últimos encargos y ninguna pieza cubre** (hoja-de-ruta, cases-rejilla,
demo-ejecucion-1, adelgazar-estado, guion-mismo-comando, umbral-mayo, respaldo-a11, activacion-a42,
reloj-invierno, guardias-citas):

| Tarea repetida | Encargos | Cobertura |
|---|---|---|
| Escribir un ADR nuevo (número libre, `## Estado` ACTIVE, el ADR antes de citarlo; un id futuro rompe `knowledge validate`) | umbral-mayo, respaldo-a11, activacion-a42, demo-ejecucion-1, hoja-de-ruta | ninguna |
| Sacar líneas de PROJECT_STATE a HISTORIA con su texto literal y saldo de bytes ≤ 0 (`docs/state/README.md`) | guardias-citas, respaldo-a11, adelgazar-estado, reloj-invierno, activacion-a42, hoja-de-ruta | ninguna (`cerrar-rama` solo saca la Next Action HECHA) |
| Preparar las líneas de la Next Action y de la hoja de ruta para el commit del contrato | hoja-de-ruta, adelgazar-estado, umbral-mayo, respaldo-a11, activacion-a42, entorno-code | solo `activar-sesion`; falta en `entregar-rama` (0.a) |
| Material escrito del trader al corpus (renombrar, `fuentes.yaml`, `corpus inventory`) | activacion-a42, reloj-invierno | ninguna (y las imágenes son de Aleks: la guardia las bloquea a la sesión) |
| Registrar respuestas de FTMO o decisiones de Aleks, parafraseadas | guion-mismo-comando, cases-rejilla, demo-ejecucion-1 | ninguna |
| Congelar un CSV de la demo y leerlo con `scripts/leer_demo_ftmo.py` | demo-ejecucion-1; vuelve con las ejecuciones 2 y 3 (hoja A.1) | ninguna |
| Demostrar que un test falla si se quita la condición (mutación), no solo con el código de `main` | umbral-mayo, guion-mismo-comando, guardias-citas, respaldo-a11 | parcial (`comparar-con-main` cubre «falla con main») |
| Comparar con `main`, caso a caso, que no se pierde ninguna puerta o regla de un texto o una guardia | guion-mismo-comando, hoja-de-ruta, adelgazar-estado | parcial (`comparar-con-main` compara salidas, no reglas) |
| Recuadro de corrección en un informe cerrado o un ADR | activacion-a42, hoja-de-ruta, cases-rejilla, umbral-mayo | ninguna para hacerlo (el revisor lo comprueba después) |
| «Nadie ejecuta motor arnes», y comprobarlo al entregar | umbral-mayo, cases-rejilla, adelgazar-estado, demo-ejecucion-1, guion-mismo-comando | parcial (límite de `activar-sesion` y `comparar-con-main`; E7 lo hace cumplir al revisor y al auditor) |
| Notas del consultor para la orden de cierre escritas dentro del encargo | cases-rejilla | ninguna (`cerrar-rama` toma los hallazgos de la orden, no del encargo) |

## 1. Lo que necesito que decidas

0. **E3, `make rapido`.** La guardia niega `make` con variables (`T=`). Opciones: (a) `make rapido`
   sin variables: lint y types, y los tests con `uv run pytest <fichero>` aparte; (b) cambiar la
   guardia para admitir `T=<ruta de tests/>`, con un test que lo rompa. Recomiendo (a): no abre la
   guardia y deja el mismo efecto (iterar sin sellar). Coste de (b): un hueco nuevo en una guardia
   que niega por defecto, para ahorrar una línea.
1. **E3, `pytest-xdist`.** Medido (0.b): mismo resultado por nombre en las cinco, la guarda salta
   y nada escribió en el árbol del clon; pero el pico sube × 4,7 (243 → ~1.150 MiB) para bajar de
   18 a 7 minutos. Opciones: (a) no se añade por ahora, y en otra rama se mide la palanca que sale
   de la medida: los cinco tests que ejecutan `knowledge validate` sobre el repo real (≈ 390 s)
   compartiendo un solo resultado, sin subir la memoria; (b) se añade como opción, nunca por
   defecto (`make check` sigue en serie); (c) por defecto en `make check`. Recomiendo (a): la
   especificación dice que si el pico sube no se activa por defecto, y una opción que nadie usa al
   sellar no acorta el sello. Coste de (a): el sello sigue en ~20 minutos hasta esa rama.
2. **E7, el alcance.** Opciones: (a) solo `arnes`, como dice E7; (b) la lista medida en 0.a:
   `--salida` como marca de escritura, `arnes`, `visor`, `hoja`, `visto`, `download` (casa también
   `download-ticks`), `aggregate`, `contradictions` y `reject`, y negar `--incluir-holdout`.
   Recomiendo (b): el agente que solo lee no puede escribir por ninguno de esos caminos, y
   `--incluir-holdout` abre el holdout. Coste de (a): siete formas de escribir que siguen abiertas
   a dos agentes que dicen no escribir.
3. **E4, las plantillas.** Añadir `NN` a las marcas que el test ignora: sin ello falla sobre
   `ingerir-sesion` (que esta rama no puede tocar). Recomiendo añadirlo.
4. **E5, ERRORES-RECURRENTES línea 13.** Opciones: (a) editarla directamente («Se apunta al
   cerrar, en el commit del contrato», con fecha y rama); (b) recuadro de corrección. Recomiendo
   (a): un runbook es un texto vivo; el recuadro es el régimen de los informes cerrados.
5. **Las correcciones a las piezas del paquete (0.a)**: se copian con esas correcciones, cada una
   declarada en el informe. ¿Todas aceptadas? En especial: `entregar-rama` sin el «23.000» y con
   las líneas para el commit del contrato; `activar-sesion` sin el refiltrado como ejemplo y con el
   comando de `feedback new` entero; `auditor-encargo` con el tramo como `## ` y la entrada como
   `###`.
6. **E6, cuántas ramas**: «ninguna otra rama» incluye `feature/*` y `fix/*` en local (no solo
   `trabajo/*`), como dicen los encargos. Recomiendo así.
7. **E1, la hoja de ruta en el hook**: (a) mostrar solo el `tramo` (de `contrato.yaml`); (b) además
   el título de su entrada `###`, leyendo `docs/plan/HOJA-DE-RUTA.md` (que entra en la lista
   cerrada). Recomiendo (a): la entrada no se deduce del tramo sin el encargo, y el hook tiene que
   ser rápido y cerrado.
8. **Los huecos de 0.c**: no entran en esta rama. Propuesta: anotarlos en la hoja de ruta, carril de
   guardias y deuda, en el cierre (sobre todo «escribir un ADR» y «sacar líneas de PROJECT_STATE a
   HISTORIA», que aparecen en cinco y seis de los diez últimos encargos).

## 2. Respuesta del consultor a la PARADA (2026-10-11), tal cual

> Respuesta del consultor a la PARADA de trabajo/entorno-code (2026-10-11). Cópiala tal cual al final del encargo y en el informe.
>
> 0. make rapido: aceptado, sin variables, y los tests concretos con uv run pytest aparte. La guardia no se toca.
> 1. xdist: aceptado que no entra por ahora (el pico de memoria sube de unos 243 a unos 1.150 MiB). CAMBIO: la otra palanca medida entra EN ESTA RAMA y no en otra, porque es el objetivo de E3. Los cinco tests que ejecutan cada uno knowledge validate sobre el repo real pasan a compartir una sola ejecución (fixture de sesión, de solo lectura), con estas condiciones medidas en el informe: (a) cada test conserva sus aserciones tal cual; (b) la suite da el mismo resultado por nombre de test antes y después (passed, skipped y failed); (c) cada uno de los cinco sigue fallando si se rompe lo que vigila (un caso roto a propósito por test, en un clon --detach); (d) la duración de make check antes y después, y su pico de memoria. Si alguno de los cinco no puede compartir la ejecución sin perder lo que vigila, se queda como está y se dice por qué. Con la nueva cifra, xdist se vuelve a medir más adelante, en su propia rama si compensa.
> 2. E7: aceptado: se bloquea la lista medida (con --salida como marca de escritura) y se niega --incluir-holdout, no solo arnes. Cada forma, con un test que la rompe.
> 3. E4: aceptado: NN entra en las marcas de plantilla.
> 4. ERRORES-RECURRENTES.md:13: aceptado: se corrige directamente, porque un runbook es un texto vivo y no un informe cerrado. La corrección se dice en el informe.
> 5. Las correcciones de 0.a: aceptadas todas. Además, en comparar-con-main: los clones van en una ruta corta (por ejemplo, una carpeta de un solo nivel en la raíz del disco), porque en el clon de la medida un test falló por pasar del límite de 259 caracteres de Windows (263), y un fallo que solo existe en el clon no es una regresión. Si hay un test que lo provoque, va con su motivo en la skill.
> 6. E6: aceptado: «ninguna otra rama» cuenta también feature/* y fix/* locales, además de las trabajo/* y de fix/* en origin.
> 7. E1: aceptado: el hook muestra solo el tramo, sin el título.
> 8. Los huecos de 0.c: aceptado: se preparan para la hoja de ruta en el commit del contrato del cierre; no entran en esta rama.
> Y E2: la justificación del cambio del revisor a opus usa la cifra medida (20 de 28 filas; 4 de las 7 últimas), no la de la especificación.
>
> Sigue con la fase 1.

### 2.1 Añadido del consultor para esta noche (2026-10-11), tal cual

> Añadido para esta noche (consultor, 2026-10-11): Aleks no está hasta mañana. Cópialo al final del encargo y en el informe. Trabaja sin esperarme toda la fase 1 y la entrega (skill entregar-rama cuando esté instalada), hasta «Rama lista para revisión, NO cerrada». Si una pieza choca con algo medido y necesita decisión, NO pares la rama: apunta esa pieza como PARADA en el informe con sus opciones y tu recomendación, déjala sin hacer, y sigue con las demás. Nunca cierres ni toques main. Si una ejecución larga muere por memoria, no la relances: apúntalo y sigue con lo que no dependa de ella. Si el clasificador niega un push, deja el comando exacto en el informe para que Aleks lo lance por la mañana. Al terminar, el resumen final para Aleks de entregar-rama.

## 3. Fase 1 · Lo hecho

Commits de la fase 1: `248d8df` (las piezas, E1, E2, E4, E5, E6, E7 y la duración de E3) y
`efe7f92` (E3, la ejecución compartida de `knowledge validate`), cada uno con `make check` en
verde y su línea `SELLO`. El `Makefile` NO cambia: es la PARADA de §4.

### 3.1 Las piezas del paquete, instaladas con las correcciones de 0.a

Las cinco skills y el agente se copiaron del paquete (versión 2, sin CRLF) y se corrigieron solo
en lo que 0.a midió falso o en conflicto (respuesta 5: «aceptadas todas»). Cada corrección:

| Pieza | Corrección | Sale de |
|---|---|---|
| `auditor-encargo.md` | los heredados también en «Pendientes heredados» de `PROJECT_STATE.md` y como `HER:n` en la hoja de ruta | 0.a, fila auditor :41-42 |
| `auditor-encargo.md` | «pendiente con due» (el repo escribe «dueño») | 0.a, :43-44 |
| `auditor-encargo.md` | el «Nunca `--help`» cita su fuente (`UMBRAL-MAYO.md`, cabecera) | 0.a, :46-47 |
| `auditor-encargo.md` | el tramo es el `## `; la entrada es el `###` con la `NA:` del encargo; «Depende de» HECHO y la siguiente según la hoja, que manda el orden (no «camino crítico»; redacción corregida tras el revisor, a3) | 0.a, :48-50 |
| `fase-cero` | la columna de fechas la lee Aleks (ADR-0072); si la fase 0 la necesita, PARADA | 0.a, fase-cero :29-41 |
| `activar-sesion` | el ejemplo de herencia es el heredado 15 (A-18, R1.1), no el refiltrado HECHO; la hoja entre las fuentes | 0.a, :24 |
| `activar-sesion` | el arnés: la corrida de R3.1 y ADR-0070 («Decision», punto 3) | 0.a, :44-46 |
| `activar-sesion` | el grep de «quién la espera» incluye `docs/plan/HOJA-DE-RUTA.md` | 0.a, :55 |
| `activar-sesion` | `feedback new` con todas sus opciones obligatorias (`cli.py`), y `--valor-canonico` | 0.a, :61-63 |
| `entregar-rama` | zoneinfo citado de los encargos, no de RITUAL | 0.a, :20 |
| `entregar-rama` | sin el «23.000»: el tope es el del test y el saldo el del encargo | 0.a, :55-56 |
| `entregar-rama` | el paso 4 prepara las líneas de la Next Action y de la hoja para el commit del contrato | 0.a, paso 4 |
| `entregar-rama` | la CI con `gh run list` o, si se niega, por la API de check-runs con el sha escrito tal cual (las órdenes de cierre del consultor); el log con `gh run view --log-failed` (redacción corregida tras el revisor, §10.1) | 0.a, :38 y :63 |
| `entregar-rama` | **añadido, medido en esta rama:** si la rama cambia el `Makefile`, la guardia no deja ejecutar `make` y el `make check` lo lanza Aleks con «!» (§4) | medida de §4 |
| `retomar-rama` | el tramo y su entrada de la hoja; remite a «Por donde se empieza» y al hook de E1 | 0.a, :14-28 |
| `comparar-con-main` | los clones en una ruta corta, con el test que lo provoca y su motivo | respuesta 5 |

### 3.2 E1 · El hook de arranque

`.claude/hooks/estado_sesion.py` y su entrada `SessionStart` en `.claude/settings.json` (matcher
`startup|resume|clear|compact`, junto al `PreToolUse`, que no cambia). Imprime la rama y su
último commit; el contrato (artefacto, riesgo y tramo; respuesta 7: solo el tramo, sin título);
el encargo; la línea de `## Estado` del informe o «sin informe»; «ESPERANDO al consultor» si la
última PARADA del informe no tiene respuesta después y no hay tantas respuestas en el encargo; un
AVISO si las respuestas no están en los dos; en `main`, las letras vivas de la Next Action y «sin
rama abierta»; y «Para retomar: skill retomar-rama».

Cómo se vigila a sí mismo: solo `leer` abre ficheros, y solo los de `lista_cerrada`
(`contrato.yaml`, `PROJECT_STATE.md`, el encargo de la rama y el artefacto); cada uno pasa antes
por `guardia.Politica(raiz).motivo_fichero(ruta absoluta)` (0.b); si la guardia da motivo o
falla, no se lee y se dice. Git solo de lectura. Cualquier error es una línea y sale con 0.
Medido sobre el repo real: 0,16 s. `mypy --strict` pasa sobre él (`uv run mypy --strict` con las
otras dos guardias), pero la línea `types` del `Makefile` no lo incluye todavía (§4).

Tests (`tests/unit/test_estado_sesion.py`, 12; el duodécimo, tras el hallazgo a4 del revisor:
si la guardia no se puede importar, no se lee nada): rama con contrato; `main`; PARADA sin respuesta
(y con ella copiada en los dos, ya no espera); respuesta copiada solo al encargo; sin informe (sin
fichero y sin `artefacto`); un fichero que la guardia bloquea (un caso del holdout sintético en un
repo temporal: no se abre, y su contenido no sale); la lista cerrada y `leer` negando fuera de
ella; un test por AST que falla si cualquier otra función del hook abre un fichero; nunca
bloquea (repo real en menos de 2 s, fuera de un repo, raíz inexistente, error interno); y la
entrada de `settings.json`.

### 3.3 E2 · El revisor con opus

`.claude/agents/revisor.md`: `model: opus`. La justificación, con la cifra MEDIDA (respuesta,
«Y E2»): en la tabla de `ERRORES-RECURRENTES.md` hay hallazgos del consultor sin constancia de que
el revisor los viera en **20 de sus 28 filas**, y en **4 de las 7 últimas** (0.b). La tabla no
registraba el modelo; desde esta rama, «Como se rellena» pide anotarlo en cada fila, para medir el
cambio en las siguientes.

### 3.4 E3 · El tiempo de `make check`

**La duración en `make check`.** `scripts/pico_memoria.py medir` apunta ahora también los
segundos de cada orden, e `informe` imprime una línea `DURACION de make check: N s en total; por
paso (s): ...` y DESPUÉS, como última línea del log, la del pico, que no cambia
(`tests/unit/test_memoria.py`, dos tests). Es lo único de E3 que entra por ese camino: el
`Makefile` no cambia.

**`pytest-xdist`**: no entra (respuesta 1). `pyproject.toml` y `uv.lock`, sin cambios.

**Los cinco tests de `knowledge validate` (respuesta 1).** En `tests/conftest.py`, un fixture de
sesión, `validacion_del_repo`, ejecuta `knowledge.validar(REPO)` una vez y guarda
`(codigo, tupla de lineas)`; como los fixtures de sesión se crean antes que `holdout_guard`,
enciende la guarda del holdout a mano, la vigila igual (si ve una lectura, falla) y la deja como
estaba. Otro, `knowledge_validate_compartido`, de función, sustituye durante el test
`botsito.validation.knowledge.validar` por una que, SOLO para el repositorio real, devuelve ese
resultado (una lista nueva cada vez: ningún test puede cambiárselo a otro); con cualquier otra raíz
llama a la de verdad. `cli.knowledge_validate` importa `validar` al llamarla, así que la CLI recibe
el resultado sin cambiar nada de `src/`.

| Test | Usa el resultado compartido | Cambio en el fichero |
|---|---|---|
| `test_cli.py::test_knowledge_validate_real_repo` | sí | el `usefixtures` |
| `test_cli.py::test_cli_entrypoint_runs` | sí | el `usefixtures` |
| `test_retirados.py::test_el_repo_real_retira_uno_y_ninguna_salida_lo_nombra` | sí (solo su `knowledge validate`; sus otros comandos corren igual) | el `usefixtures` |
| `test_historial_sin_git.py::test_con_git_las_lineas_ok_son_las_de_main` | sí | el `usefixtures`, y `validar(REPO)` pasa a `knowledge.validar(REPO)` (el nombre importado al cargar el módulo no ve el fixture) |
| `test_citas_supersedidas.py::test_knowledge_validate_lleva_g1` | **no: se queda como está** | ninguno |

Por qué G1 se queda: ese test sustituye `citas_a_supersedidos` por una que falla y comprueba que
`validar` sale con ERROR; vigila que G1 esté CONECTADA a `validar`, y eso solo lo enseña una
ejecución con la pieza cambiada. Un resultado compartido, calculado con la pieza de verdad, no
puede mostrarlo.

Las condiciones de la respuesta, medidas en dos clones `--detach` de ruta corta (`C:\ecA` en
`248d8df`, antes del fixture; `C:\ecB` en `efe7f92`, después), cada uno con su `.venv`
(`uv sync --locked --group dev`; los dos importan su propio `botsito`):

- **(a) Las aserciones, tal cual.** El diff de los cuatro ficheros (`git diff 248d8df efe7f92 --
  tests/unit`) solo añade los `usefixtures` y cambia la llamada de `test_con_git`; ninguna línea
  `assert` cambia.
- **(b) El mismo resultado por nombre.** La suite entera en los dos clones a la vez, con JUnit XML:
  2.545 passed, 10 skipped y 0 failed en los dos, y la comparación nombre a nombre
  (`classname::name` y su estado) da **cero diferencias**. Los dos clones, sin cambios tras correr
  (`git status --porcelain` vacío). En la ruta corta, el test de las rutas de Windows que falló en
  la fase 0 pasa.
- **(c) Cada uno sigue fallando si se rompe lo que vigila**, en `C:\ecB` (con el fixture), un caso
  por test y el clon restaurado tras cada uno:

| Rotura a propósito (en el clon) | Test | Resultado |
|---|---|---|
| ninguna | los cinco | 5 passed (exit 0) |
| G1 desconectada: `fallos_g1, _vigilados = [], 0` en `validar` | G1 | 1 failed (exit 1) |
| el repo deja de validar: se borra el ADR-0071, que la spec cita | `test_knowledge_validate_real_repo` y `test_cli_entrypoint_runs` | 2 failed (exit 1) |
| `validar` añade a su salida el id del caso retirado | el del retirado | 1 failed (exit 1) |
| `validar` añade una línea «NO se comprobo» | el de las líneas OK con git | 1 failed (exit 1) |
| (tras el hallazgo b4 del revisor, en otro clon `C:\ecB` en `0c2cb22`) el despacho de `knowledge validate` en `cli.main` devuelve 1 | `test_cli_entrypoint_runs` | 1 failed (exit 1); con la misma rotura `test_knowledge_validate_real_repo` pasa (no pasa por `cli.main`): cada uno tiene su rotura propia |

  Las roturas están en `scratchpad/e3/e3c_romper.py` de la sesión (fuera del repo). La del
  retirado corrió con `pytest -q --tb=no -rN` y solo se guardó la última línea: el id del caso,
  que es de un día reservado, no salió a ningún log ni a la pantalla.

- **(d) Duración y pico de `make check`**, del propio `make-check.log` (la línea `DURACION`
  nueva), en el repo real, en la misma máquina:

| `make check` del commit | Total | `test` | `knowledge` | Pico |
|---|---:|---:|---:|---:|
| `248d8df` (antes) | 1.209 s | 1.121 s | 84 s | 294 MiB |
| `efe7f92` (después) | 952 s | 870 s | 79 s | 295 MiB |

Baja 257 s (un 21 %), con el mismo pico. Los cinco tests, en los clones: 370,7 s antes
(72,5 + 72,0 + 72,8 + 78,1 + 75,3) y 149,3 s después (G1 72,4; el primero que pide el fixture,
72,8; los otros tres, 0,0 + 0,0 + 4,1). El paso `knowledge` (84 s) sigue aparte: es el de
`make check`, no un test.

### 3.5 E4 · `tests/unit/test_skills.py`

Falla si una skill o un agente nombra entre comillas invertidas una ruta de `docs/`, `src/`,
`scripts/`, `tests/`, `knowledge/` o `.claude/` que no existe (plantillas fuera: `<`, `>`, `{`,
`*`, `0N` y `NN`, respuesta 3; el primer término del código, sin `:línea`); si nombra una skill o
un agente que no existe (junto a «skill», «subagente» o «agente»); si a una skill le falta `name`
igual a su carpeta o `description`; o si a un agente le falta `name`, `description`, `tools` o
`model`. Pasa sobre el repo real con las diez piezas. Tests del test: una ruta inexistente, un
`name` que no casa, una skill y un subagente que no existen, una skill sin `description`, una sin
cabecera y un agente sin `model` fallan, cada uno con un solo problema; cinco plantillas y una
ruta con `:línea` no fallan.

Dos cosas que la especificación no dice, declaradas: (1) la cabecera se lee como YAML y, si no lo
es, línea a línea `clave: valor`, como Claude Code: la `description` de `abrir-rama` (en `main`)
lleva «: » sin comillas y `yaml.safe_load` la rechaza; (2) el `name` de un agente tiene que ser su
fichero, como el de una skill su carpeta.

### 3.6 E5 · Lo nuevo, nombrado

- `CLAUDE.md`, «Por donde se empieza»: la lista completa de skills en el orden de una rama, las
  dos aparte y los dos agentes, una línea cada uno con cuándo se usa. La frase que
  `tests/unit/test_revisor.py` exige literal («Antes de declarar una rama lista para revisión: …»)
  no se tocó.
- `.claude/agents/revisor.md`, eje (b), punto 5 nuevo: si el encargo pedía FASE 0, «Lo que
  necesito que decidas» y cada respuesta tal cual en el informe y en el encargo; y «El encargo,
  punto por punto». `test_revisor.py` exige los dos fragmentos.
- `docs/runbooks/ERRORES-RECURRENTES.md`, «Como se rellena» (respuesta 4, sin recuadro): la fila
  del revisor se apunta al CERRAR, en el commit del contrato, como `RITUAL.md` y `cerrar-rama`;
  el texto dice qué decía antes, con fecha y rama. Y anota el modelo del revisor (E2).

### 3.7 E6 · `abrir-rama` comprueba la base entera

Paso 1: `git fetch origin`; `main` igual al sha del encargo y a `origin/main`; el último
`- Tag: ` de HISTORIA con `stable/<tag>^{commit}` = `main^1` y presente en origin; la CI de `main`
en `success` por la API de check-runs con el sha literal; ninguna otra rama local (`trabajo/*`,
`feature/*` ni `fix/*`, respuesta 6) ni `fix/*` en origin; si algo no cuadra, se para. Además,
por 0.a, la Verificación incluye el artefacto. (La frase del inventario del paso 4 se cambió en
`248d8df` por el solape de 0.c y se devolvió a la de `main` tras el hallazgo b2 del revisor: ese
solape no se puso a decisión; queda como punto 1 de §4, y la respuesta (a) la cambia: §4.2.)
Ninguna puerta que tenía se
quitó (`git diff 9fe3d44 248d8df -- .claude/skills/abrir-rama/SKILL.md`: solo amplía el paso 1,
Herramientas y Verificación, y cambia la frase del inventario).

### 3.8 E7 · `solo_lectura.py`

Además de lo que ya negaba: `--salida` en cualquier subcomando de `botsito`, y `arnes`, `visor`,
`hoja`, `visto`, `download` (también `download-ticks`), `contradictions` y `reject`, también con
`--check` (ninguno lo tiene); y `--incluir-holdout`, con su propio motivo («abre el holdout»). El
mensaje nombra a los dos agentes que lo usan. Tests en `tests/unit/test_revisor.py`: quince
comandos que tienen que bloquearse (uno por forma, más `arnes` sin `--salida` y `--check` que no
salva), cinco lecturas de `botsito` que siguen pasando, el motivo de `--incluir-holdout`, y que el
auditor tiene solo herramientas de lectura y su Bash pasa por `solo_lectura.py`.

### 3.9 Los tests nuevos, con el código de `main`

Skill `comparar-con-main`, «Para probar un test con el codigo de main»: en el clon `C:\ecB`, puesto
en `main` (d32db01), con `tests/unit/test_revisor.py`, `test_estado_sesion.py` y `test_skills.py`
de la rama copiados dentro: **21 failed, 55 passed, 8 errors**. Fallan las dos frases nuevas del
revisor, catorce de las quince formas de E7, el auditor, `--incluir-holdout`, la entrada de
`settings.json`, el test por AST y el de «nunca bloquea» (el hook no existe), y el de las piezas;
los 8 errores son los tests de E1 que cargan el hook. Pasan los tests antiguos, los tests
sintéticos de E4 (prueban el test, no el repo), el de las skills del repo (las tres de `main` no
señalan a la nada) y una forma de E7, `evidence propose --salida`, que `main` ya bloqueaba por
`propose`. Después, el clon se restauró y se retiró con los dos (`git worktree list` sin ellos).

### 3.10 Desviaciones declaradas

1. **El `Makefile` no cambió hasta la respuesta de §4.1** (§4): `make rapido` y la línea de
   `mypy --strict` del hook entran en el último commit, sellado por un `make check` que lanza
   Aleks (§4.2).
2. `tests/unit/test_memoria.py`, `test_medir_apunta_cada_paso_y_el_informe_da_el_mayor_y_limpia`:
   el informe tiene ahora dos líneas, así que lee la ÚLTIMA (la del pico, igual que antes) y
   comprueba además la de la duración. La línea del pico sigue siendo la última de
   `make-check.log` y mide lo mismo.
3. (Retirada.) `abrir-rama`, «el artefacto nace con el inventario» pasó en `248d8df` a «nace EN
   CURSO y el inventario lo escribe `fase-cero`»; el revisor (b2) vio que la respuesta 5 acepta
   las correcciones de 0.a y este cambio salía de 0.c, que no se puso a decisión. Se devolvió a
   la frase de `main` y va a §4, punto 1. Con la respuesta (a), entra la frase del consultor
   (§4.2).
4. Lo de E4 de §3.5 (cabecera tolerante y `name` del agente).
5. `entregar-rama` lleva un límite que el paquete no traía (§3.1, última fila de `entregar-rama`).

## 4. PARADA de esta noche: el `Makefile` (sin hacer hasta la respuesta de §4.1)

Lo medido: con el `Makefile` cambiado, la guardia de Claude Code niega TODO `make`, también
`make check`: «ejecutar `make rapido`: …\Makefile no es el de `main`: sus recetas son código de la
rama sin revisar. … Como reescribirlo: no se reescribe; lo lanza Aleks en su terminal con «!»».
Sin `make check` no hay sello y sin sello no hay commit, y Aleks no está esta noche. Por el
añadido, la pieza queda sin hacer y la rama sigue.

Lo que falta, preparado (diff contra `248d8df`):

```
-.PHONY: sync hooks check lint types ...
+.PHONY: sync hooks check rapido lint types ...
 types:
 	$(MEDIR) types -- mypy
-	$(MEDIR) types -- mypy --strict .claude/hooks/guardia.py .claude/hooks/solo_lectura.py scripts/contrato_rama.py
+	$(MEDIR) types -- mypy --strict .claude/hooks/guardia.py .claude/hooks/solo_lectura.py .claude/hooks/estado_sesion.py scripts/contrato_rama.py
+# Para iterar SIN SELLAR (E3, punto 0): lint, tipos y contratos, sin `desellar` ni `sellar` ni
+# variables; los tests concretos, con `uv run pytest <fichero>`.
+rapido: lint types contracts
```

Y un test que falle si `rapido` llega a `desellar`, `sellar` o `check`, o si alguna de sus recetas
nombra `sello_make_check`.

**Lo que necesito que decidas:**
0. Opciones: (a) Aleks estadía el cambio y lanza `! make check > make-check.log 2>&1`; la sesión
   lee el log y commitea; (b) sin `make rapido`, y `mypy --strict` del hook por un test que lo
   ejecute (el `Makefile` no cambia y la sesión sella sola); (c) se deja para otra rama.
   Recomiendo (a): es la letra de E1 y de la respuesta 0, y es un solo `make check`. Coste de (b):
   un test lento más y una guardia de tipos fuera del sitio donde viven las otras dos.
1. `abrir-rama`, paso 4 (solape de 0.c, hallazgo b2 del revisor). Hoy dice que, si el encargo pide
   un inventario, el artefacto «nace con el»; en la práctica nace con su cabecera y EN CURSO, y el
   inventario lo escribe la fase 0 en su commit (así se abrió esta rama, `bb3e3fd`). Opciones:
   (a) cambiar la frase a «nace con su cabecera y EN CURSO; la fase 0 la escribe `fase-cero` en su
   commit»; (b) dejarla. Recomiendo (a): la frase describe un orden que la skill `fase-cero` ya no
   sigue. Coste de (b): dos skills que dicen dos cosas sobre el mismo paso.

### 4.1 Respuesta del consultor a la PARADA de §4 (2026-10-11), tal cual

> Respuesta del consultor a la PARADA de ENTORNO-CODE.md §4 (2026-10-11). Cópiala tal cual al final del encargo y en el informe.
>
> 0. Makefile: (a). El consultor revisó el diff de §4 y lo aprueba tal cual: rapido = lint types contracts, sin desellar, sellar ni variables, y estado_sesion.py en mypy --strict. Aplícalo, añade el test que falla si rapido llega a desellar, sellar o check o si una de sus recetas nombra sello_make_check, y estadía todo. Después dime exactamente cuándo lanzar yo «! make check > make-check.log 2>&1»; cuando acabe, lee el log (exit 0, ningún failed, SELLO) y commitea. No reescribas el comando para que la guardia no lo vea.
> 1. abrir-rama, paso 4: (a): «nace con su cabecera y EN CURSO; la fase 0 la escribe fase-cero en su commit».
> Con los dos hechos: push a fix/entorno-code, CI de Linux con su número de run, y prepara §6 con la variante de F «E es lo siguiente» y R0.2 HECHA. Rama lista para revisión, NO cerrada.

### 4.2 Lo hecho con la respuesta

- **0, el `Makefile`**: el diff de §4, tal cual: `rapido` en `.PHONY`,
  `.claude/hooks/estado_sesion.py` en la línea de `mypy --strict` de `types`, y
  `rapido: lint types contracts` con su comentario, sin recetas propias ni variables. La línea
  `check:` no cambia. `uv run mypy --strict .claude/hooks/estado_sesion.py`: «Success: no issues
  found in 1 source file». Test nuevo, `tests/unit/test_make_rapido.py` (11 tests, tras el
  segundo revisor, §10.3): lee el `Makefile`, recorre lo que alcanza `rapido` por sus
  prerrequisitos (también los de una regla con varios objetivos) y por cualquier `make` o
  `$(MAKE)` de sus recetas (también la receta en línea tras `;`), con las variables expandidas
  (`+=` incluido), y falla si llega a `desellar`, `sellar` o `check` o si una receta nombra
  `sello_make_check`; lo que no sabe seguir (`include`, `define`, `!=`) es un problema, no un
  silencio. Comprueba además que `rapido` sea exactamente `lint types contracts` sin recetas y
  que el hook esté en `mypy --strict`. Se prueba contra roturas sintéticas: sin `rapido`; `rapido`
  con `sellar`, `desellar` o `check` de prerrequisito; a través de otro objetivo; por una regla
  con varios objetivos; con `$(MAKE) check`, `${MAKE} -f Makefile check`, `make check` y
  `$(UV) run make check` en una receta (y `> make-check.log` no cuenta como `make`); con una
  receta en línea; con `include`, `-include`, `define` y `!=`; y con `sello_make_check` en una
  receta, directo, escondido en una variable y sumado con `+=`. Con el `Makefile` de `main` falla
  (`no existe el objetivo rapido`). `rapido` corre sus pasos dentro de `medir`, que apunta en el
  acumulador del pico, en el directorio de git y no en el árbol: ni lo ve la huella ni es el
  sello, y el `empezar` de `desellar` lo borra al principio de cada `make check`. La sesión no ha
  lanzado `make rapido` ni `make check`: con este `Makefile` la guardia los niega, y el
  `make check` que sella este commit lo lanza Aleks con «!».
- **1, `abrir-rama`, paso 4**: la frase de la respuesta, literal salvo la mayúscula inicial:
  «Nace con su cabecera y EN CURSO; la fase 0 la escribe fase-cero en su commit», en lugar de «Si
  el encargo pide un inventario antes de tocar codigo, nace con el; si no, con su cabecera y un
  `## Estado` EN CURSO». (La primera versión añadía «(un `## Estado` EN CURSO)»; el segundo
  revisor, b3, vio que no era literal, y se quitó.)
- La respuesta, copiada al final del encargo y aquí; `PROJECT_STATE.md`, 1486 → 1494 funciones de
  test (mismos bytes; 1498 al final, §4.5 y §10.3).
- **El revisor** pasó antes de esta respuesta (§10), cuando `rapido` no existía. Lo que su
  alcance pide de él («que make rapido, si existe, no selle») lo comprueba ahora
  `test_make_rapido.py` dentro de `make check`. Tras la respuesta de §4.4 se pasó otra vez sobre
  todo lo de la tarde (§10.2).

### 4.3 PARADA: con el `Makefile` cambiado, `make check` no puede salir en verde

Lo medido: el `make check` que lanzó Aleks (2026-10-11, con todo lo de §4.2 estadiado) salió con
exit 2 y sin `SELLO`: «2 failed, 2562 passed in 1065.21s». Los dos fallos son
`tests/unit/test_guardia_claude.py::test_el_ritual_y_los_runbooks_pasan[make check > make-check.log 2>&1]`
y `[make hooks]`: ese test pasa los comandos del ritual por la guardia CONTRA EL REPO REAL y exige
que no los niegue, y la guardia niega todo `make` si el `Makefile` no es el de `main`
(`_igual_que_en_main`, la vía de `exigir_ejecucion_verificable` desde `f22179f`, 2026-10-07). Así
que ninguna rama que cambie el `Makefile` puede sellar, lo lance quien lo lance; desde esa fecha
ninguna lo había cambiado (`git log main -- Makefile`: el último, `3027599`, del 2026-10-01). No
hay commit: lo de §4.2 sigue estadiado, intacto.

**Lo que necesito que decidas:**
0. Opciones: (a) en ese test, para los dos comandos `make`, si el `Makefile` del repo no es el de
   `main` (la misma `_igual_que_en_main` de la guardia), exigir que la guardia los NIEGUE con
   «lo lanza Aleks en su terminal con «!»»; si es el de `main`, exigir que pasen, como hoy. La
   guardia no se toca; el test pasa a comprobar las dos caras. (b) Sacar los dos `make` de
   `RITUAL` y probarlos en un repo temporal con el `Makefile` igual al de `main` (ya hay tests así,
   `test_guardia_claude.py:1087` y `:1175`). (c) El `Makefile` vuelve al de `main` y `rapido` y la
   línea de `mypy --strict` pasan a otra rama, que chocará con lo mismo.
   Recomiendo (a): en `main` el test sigue igual de estricto, y en una rama que cambia el
   `Makefile` comprueba lo que la guardia tiene que hacer, que es negar. Coste de (b): el test deja
   de mirar el `Makefile` real. Coste de (c): no resuelve nada. Con (a) o (b), otro `make check`
   lanzado por Aleks (unos 18 minutos).

Hallazgo: el test del ritual suponía el Makefile de main; la primera rama que lo cambia lo rompe;
corregido en el test, la guardia sigue igual.

### 4.4 Respuesta del consultor a la PARADA §4.3 (2026-10-11), tal cual

> Modelo: Opus · Esfuerzo: alto (misma sesión, rama trabajo/entorno-code)
>
> Respuesta del consultor a la PARADA §4.3 (2026-10-11). Cópiala TAL CUAL al final del encargo y en el informe, y aplícala.
>
> Decisión: (a), con estas precisiones.
>
> 1. En tests/unit/test_guardia_claude.py, solo para los comandos de RITUAL cuyo programa es `make` ("make check > make-check.log 2>&1" y "make hooks"), la expectativa depende de si el Makefile del repo real es el de main:
>    - La condición la calcula el test con git, NO con `_igual_que_en_main` ni con otra función de la guardia: `git rev-parse --verify -q main:Makefile`, o si no `origin/main:Makefile`, frente a `git hash-object -- Makefile`, con cwd=RAIZ.
>    - Si coinciden: la guardia no niega (como hoy).
>    - Si difieren: la guardia niega, y el motivo contiene «lo lanza Aleks en su terminal con «!»».
>    - Si no hay ni main ni origin/main: el test FALLA con un mensaje que lo diga. No se salta.
>    - El resto de comandos de RITUAL no cambia. Si es más limpio, sepáralo en un test aparte para los dos `make`, pero el parametrizado de los demás sigue igual de estricto.
> 2. La guardia NO se toca.
> 3. El test que rompe a propósito, demostrado en el informe con comando y salida: con el Makefile de la rama, el test nuevo pasa y el actual falla (los 2 fallos del log). Y `uv run pytest tests/unit/test_guardia_claude.py -q` en verde. Es pytest, no make, así que lo puedes lanzar tú.
> 4. Al informe, en §4.3, una línea de hallazgo: «el test del ritual suponía el Makefile de main; la primera rama que lo cambia lo rompe; corregido en el test, la guardia sigue igual». En §6 añade a G.1: «el test del ritual quedó ciego al caso del Makefile cambiado hasta entorno-code (corregido)».
> 5. Después: git add de lo tocado, y me pasas a mí (Aleks) la línea exacta para lanzar `! make check > make-check.log 2>&1`. Cuando termine, lees el log (exit 0, ningún failed, la línea SELLO), haces el commit, push a fix/entorno-code, esperas la CI del ÚLTIMO commit (único fallo aceptado: state check por el nombre fix/) y dejas la rama «lista para revisión, NO cerrada». No hace falta otra pasada del revisor salvo que el diff vaya más allá del test y del informe. Si va más allá, la pasas y lo dices.

### 4.5 Lo hecho con la respuesta de §4.4

- **1, el test.** En `tests/unit/test_guardia_claude.py`, los dos `make` salen de `RITUAL` a
  `RITUAL_MAKE`, con su propio test,
  `test_los_make_del_ritual_pasan_si_el_makefile_es_el_de_main_y_si_no_los_lanza_aleks`. La
  condición la calcula `_makefile_es_el_de_main()` del test con git y `cwd=RAIZ`:
  `git rev-parse --verify -q main:Makefile`, si no `origin/main:Makefile`, frente a
  `git hash-object -- Makefile`. Si coinciden, la guardia no niega; si difieren, niega y el motivo
  contiene «lo lanza Aleks en su terminal con «!»»; si no hay ni `main` ni `origin/main`,
  `pytest.fail` con un mensaje que lo dice (no se salta). Los demás comandos de `RITUAL`, en el
  parametrizado de siempre, sin cambios. `test_ninguna_denegacion_toca_el_ritual`, que también
  recorría `RITUAL`, pasa a recorrer `RITUAL + RITUAL_MAKE`, para no perder los dos `make`. En la CI
  hay `origin/main`: `.github/workflows/ci.yml` hace el checkout con `fetch-depth: 0`.
- **2, la guardia**: sin tocar (`git diff --cached --stat main -- .claude/hooks/guardia.py`, vacío).
- **3, el test que rompe a propósito.** Con el `Makefile` de la rama:
  - el test ACTUAL falla. Hasta esta respuesta la rama no había tocado `test_guardia_claude.py`
    (`git log --oneline main..4b80c58 -- tests/unit/test_guardia_claude.py`: ningún commit; sin
    cambios estadiados en el `make check` de §4.3), así que el `make-check.log` de §4.3 es el test
    de `main` contra el `Makefile` de la rama: `make check > make-check.log 2>&1`, exit 2,
    «FAILED tests/unit/test_guardia_claude.py::test_el_ritual_y_los_runbooks_pasan[make check > make-check.log 2>&1]»,
    «FAILED tests/unit/test_guardia_claude.py::test_el_ritual_y_los_runbooks_pasan[make hooks]»,
    «2 failed, 2562 passed in 1065.21s».
  - el test NUEVO pasa, por la rama de «difieren» (`git rev-parse --verify -q main:Makefile`:
    `d0cbc2428b694c16ec23deb445385e997dcb3564`; `git hash-object -- Makefile`:
    `0cb536c0be4ce57d08e009248214773910863384`):
    `uv run pytest tests/unit/test_guardia_claude.py -k "make_del_ritual" -vv` →
    «…[make check > make-check.log 2>&1] PASSED», «…[make hooks] PASSED»,
    «2 passed, 556 deselected in 0.58s».
  - El fichero entero: `uv run pytest tests/unit/test_guardia_claude.py` → «558 passed in
    173.12s» (con `-q` además de los `addopts = "-q -ra"` de `pyproject.toml`, pytest no imprime
    la línea del recuento; por eso, sin `-q`).
  - Intenté además correr los tests en un clon `--detach` de `main` (`C:\ecA`), para ver la cara
    de «coinciden». La guardia de Claude Code niega ejecutar desde la sesión ese fichero fuera del
    repo real, el de `main` incluido: lleva `crudo=True` (prueba esa regla) y fuera del repo no
    cuenta como test. Con `cd C:/ecA && uv run pytest tests/unit/test_guardia_claude.py -k
    "ritual_y_los_runbooks and make"` (el fichero de `main`, sin copiar nada): «GUARDIA
    (.claude/hooks/guardia.py) bloquea: el codigo que se ejecuta pide el corpus SIN FILTRAR.»; lo
    mismo en el primer intento, que llevaba además una copia del de la rama. No se rodeó: el clon se retiró (`git worktree remove --force`, solo quedaba
    su `.venv` ignorado) y no hubo más medida. La cara de «coinciden» es la aserción de siempre
    (`motivo is None`), la misma que pasaba en `main`; en esta rama no se puede ejercitar sin
    devolver el `Makefile` al de `main`.
- **4**: el hallazgo, al final de §4.3; la línea de G.1, en §6.
- `PROJECT_STATE.md`: 1494 → 1495 funciones de test (mismos bytes); 1498 tras §10.3.

## 5. Lo que no cambia

`git diff --cached --stat main` con el último commit estadiado (31 ficheros): `.claude/` (las
piezas, el hook, `settings.json`, `solo_lectura.py`, `revisor.md`, `abrir-rama`), `CLAUDE.md`,
`Makefile`, `PROJECT_STATE.md`, `contrato.yaml`, el encargo, `ERRORES-RECURRENTES.md`,
`HOLDOUT-EXPOSICIONES.md`, HISTORIA (solo el Archivo 28), este informe, `scripts/pico_memoria.py`,
`tests/conftest.py` y nueve ficheros de `tests/unit/` (entre ellos `test_guardia_claude.py`, solo
el test de los `make` del ritual: §4.5). Nada de `src/`,
`knowledge/`, `config/`, `data/manifests/`, ni de `cerrar-rama` o `ingerir-sesion`
(`rutas_protegidas`; `scripts/contrato_rama.py` en verde). Ningún informe cerrado ni fichero
congelado. `ESPECIFICACION.md` no se copió.

- **Lo que sella `make check` no cambia**: en el `Makefile`, la línea `check:`, `desellar` y
  `sellar` son las de `main`; `types` comprueba un fichero más con `mypy --strict` (el hook) y
  `rapido` no llega al sello (`test_make_rapido.py`). `pico_memoria.py` solo añade una línea (la
  de la duración) ANTES de la del pico, que sigue siendo la última y mide lo mismo.
  `sello_make_check.py` y los hooks de git no se tocan.
- **Las puertas de `abrir-rama`**: las líneas que quita el diff de su `SKILL.md` son las del paso
  1, Herramientas, la frase del inventario y la Verificación, y cada una vuelve ampliada (el
  `checkout`, el `status` vacío, el sha del encargo y «se para y se pregunta» siguen). `cerrar-rama`
  e `ingerir-sesion` no cambian.
- **PROJECT_STATE.md**: 21.942 bytes frente a 21.959 de `main`: saldo −17 (solo cambian la rama,
  la funcionalidad actual y el recuento de tests, 1462 → 1498).

## 6. Preparado para el commit del contrato del cierre

En la rama no se tocan (RITUAL, puntos 3 y 4).

**Aviso para el cierre (segundo revisor, a1):** los `make check` del cierre que corren EN ESTA
RAMA llevan su `Makefile`, que no es el de `main`, y la guardia los niega a la sesión: los lanza
Aleks con «! make check > make-check.log 2>&1». Son el del commit del contrato
(`docs/runbooks/RITUAL.md:161`) y, si `pre-merge-commit` rechaza el merge, el de la vuelta a la
rama (`:201`). El del commit de estado en `main` (`:278`) ya corre con el `Makefile` de `main` tras
el merge, y lo puede lanzar la sesión. `cerrar-rama` no lo dice y no se toca en esta rama
(`rutas_protegidas`).

- **Next Action, F** (sustituye a la de hoy; §4 hecho, §4.2):
  `F. Orden de trabajo: E (R1.1 de la hoja de ruta) es lo siguiente; la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden.`
- **Hoja de ruta, R0.2**: se añade `- **Estado:** HECHA (\`stable/F37l-entorno-code\`; docs/validation/ENTORNO-CODE.md).`,
  y como la F sigue viva y una entrada HECHA no puede llevar una letra viva
  (`tests/unit/test_hoja_de_ruta.py`, sentido b; hallazgo b1 del revisor), su `- **Refs:** NA:F`
  pasa a `- **Refs:** —`, la `NA:F` entra en R1.1 (`- **Refs:** NA:F · NA:E · HER:15 · …`) y el
  «Depende de: R0.2 (NA:F).» de R1.1 pasa a «Depende de: R0.2.». Simulado en memoria con las
  funciones del test sobre `PROJECT_STATE.md` y la hoja de hoy más estas líneas y la F nueva:
  a, b y c, sin problemas (`scratchpad/simular_cierre.py` de la sesión, que no escribe; vuelto
  a correr tras §4.2).
- **Hoja de ruta, carril «guardias y deuda»** (respuesta 8), una entrada nueva:
  `### G.4 · Las tareas repetidas que ninguna skill cubre` con `Refs: NA:F` (viva: no es
  HECHA); `Qué es:` los huecos
  de 0.c (escribir un ADR nuevo; sacar líneas de PROJECT_STATE a HISTORIA con saldo ≤ 0; material
  escrito del trader al corpus; registrar respuestas de FTMO o de Aleks; congelar un CSV de la
  demo; demostrar un test por mutación; comparar reglas con main caso a caso; recuadros de
  corrección; las notas del consultor para la orden de cierre) y volver a medir `pytest-xdist` con
  la cifra nueva de E3 (respuesta 1); `Depende de: R0.2`; `Quién: la sesión, con el encargo del
  consultor`; `Hecho cuando: cada hueco tiene skill o se decide que no la necesita`.
- **Hoja de ruta, G.1 (la guardia de Claude Code)**, cuatro cosas medidas en esta rama, para su
  `Qué es`: la guardia no niega `git ls-files knowledge/cases | grep ...` (listar la carpeta madre
  del holdout con un filtro detrás; §10.1); `solo_lectura.py` niega `git worktree list`, que solo
  lee; la de la respuesta de §4.4, punto 4: «el test del ritual quedó ciego al caso del Makefile
  cambiado hasta entorno-code (corregido)»; y la guardia niega ejecutar desde la sesión, en un
  clon fuera del repo real, un test que lleve `crudo=True`, aunque sea el de `main` (§4.5): «probar
  un test con el código de `main`», de `comparar-con-main`, no sirve para esos tests.
- **ERRORES-RECURRENTES**, la fila de la rama, con el modelo del revisor: `opus` (§3.3). Revisor,
  primera pasada: 3 importa (a1, b1, b2) y 5 menor (a2, a3, a4, b3, b4), todos atendidos (§10.1);
  segunda pasada, sobre lo de la tarde: 3 importa (a1, a2, b1) y 3 menor (a3, b2, b3), todos
  atendidos (§10.3). Y el hallazgo de §4.3, que no vio ningún revisor sino el `make check`: el
  test del ritual suponía el `Makefile` de `main`.
- **G.1 o cerrar-rama**, para una rama siguiente: que `cerrar-rama` diga que, si la rama cambia el
  `Makefile`, los `make check` en la rama los lanza Aleks (aviso de arriba).

## 7. El encargo, punto por punto

| # | Requisito (encargo, respuesta del 2026-10-11 y añadido) | Estado | Evidencia |
|---|---|---|---|
| 1 | Verificar la base antes de abrir; abrir con `abrir-rama`, `tramo: R0` | Hecho | cabecera; `bb3e3fd` |
| 2 | Paquete versión 2 («5. **El tramo**») | Hecho | cabecera |
| 3 | Fase 0 (a), (b), (c) en el informe, y PARADA | Hecho | §0 y §1; `9fe3d44` |
| 4 | Fase 0 sin escribir en el repo; E3 en un clon `--detach`; xdist fuera del repo | Hecho | §0.b; `pyproject.toml` y `uv.lock` sin cambios |
| 5 | Respuesta y añadido copiados tal cual al encargo y al informe | Hecho | §2 y §2.1; comparación por programa: iguales |
| 6 | Piezas TAL CUAL salvo lo corregido, cada corrección declarada | Hecho | §3.1 |
| 7 | `ESPECIFICACION.md` no se copia | Hecho | §5 |
| 8 | E1, con sus tests (incluidos los que rompen a propósito) | Hecho; la línea del `Makefile`, tras la respuesta de §4.1 | §3.2; §4.2 |
| 9 | E2, justificado con la cifra medida (20 de 28; 4 de 7) | Hecho | §3.3 |
| 10 | E3, punto 0: `make rapido` sin variables; la guardia no se toca | Hecho tras la PARADA y su respuesta | §4, §4.1, §4.2 (la guardia no se tocó) |
| 11 | E3, punto 1: xdist no entra; los cinco tests comparten una ejecución, con (a)-(d) | Hecho (cuatro de cinco; G1 se queda, con su porqué) | §3.4 |
| 12 | E3: `pico_memoria.py medir` apunta la duración; la línea del pico mide lo mismo | Hecho | §3.4; `make-check.log` |
| 13 | E4, con `NN` en las plantillas y sus tests del test | Hecho | §3.5 |
| 14 | E5: `CLAUDE.md`, el revisor y ERRORES-RECURRENTES:13 sin recuadro, declarado | Hecho | §3.6 |
| 15 | E6: la base entera, con `feature/*` y `fix/*` locales | Hecho | §3.7 |
| 16 | E7: la lista medida y `--incluir-holdout`, cada forma con su test | Hecho | §3.8 |
| 17 | Respuesta 5: clones en ruta corta en `comparar-con-main`, con el test y su motivo | Hecho | §3.1; las medidas de §3.4 en `C:\ecA` y `C:\ecB` |
| 18 | Respuesta 8: los huecos de 0.c, preparados para la hoja, no hechos | Hecho | §6 |
| 19 | NO cambia: `src/`, spec, knowledge, parámetros, informes cerrados, lo que sella `make check`, las puertas de las skills | Hecho | §5 |
| 20 | Nada de holdout; saldo de PROJECT_STATE ≤ 0 | Hecho | §8; §5 (−17) |
| 21 | `make check` sellado antes de cada commit | Hecho | `9fe3d44`, `248d8df`, `efe7f92` y los siguientes; el último, con el `make check` que lanza Aleks |
| 22 | Push como `fix/entorno-code` y CI de Linux, con sus run | Hecho (el run del último commit, en el mensaje final) | §9 |
| 23 | Informe con fase 0, PARADA, respuesta, lo hecho, estado y las líneas de F y R0.2 | Hecho | este informe; §6 |
| 24 | Revisor con el alcance del encargo, pegado al final | Hecho; sus hallazgos, atendidos | §10 y §10.1 |
| 25 | Desde la fase 1, con sus propias skills; entrega con `entregar-rama` | Hecho | este recorrido es el de `entregar-rama` |
| 26 | Añadido: trabajar sin parar; lo que choca, PARADA en el informe y seguir; nunca tocar `main` | Hecho | §4; `main` sin tocar |
| 27 | Respuesta de §4.1, 0: el diff tal cual, el test de `rapido` (desellar, sellar, check, `sello_make_check`), todo estadiado y el `make check` lo lanza Aleks; sin reescribir el comando | Hecho | §4.2; `tests/unit/test_make_rapido.py` |
| 28 | Respuesta de §4.1, 1: la frase del paso 4 de `abrir-rama` | Hecho | §4.2 |
| 29 | Respuesta de §4.1: push a `fix/entorno-code` con su run, y §6 con «E es lo siguiente» y R0.2 HECHA | Hecho (el run del último commit, en el mensaje final) | §6; §9 |
| 30 | Respuesta de §4.4, 1: el test de los dos `make` del ritual, con la condición calculada con git (main, si no origin/main), que FALLA sin ninguno; el resto de `RITUAL`, igual de estricto | Hecho | §4.5 |
| 31 | Respuesta de §4.4, 2: la guardia no se toca | Hecho | §4.5 |
| 32 | Respuesta de §4.4, 3: con el `Makefile` de la rama, el test nuevo pasa y el actual falla, con comando y salida; `test_guardia_claude.py` en verde | Hecho | §4.5 |
| 33 | Respuesta de §4.4, 4: el hallazgo en §4.3 y la línea de G.1 en §6 | Hecho | §4.3; §6 |
| 34 | Respuesta de §4.4, 5: estadiar, `make check` por Aleks, commit, push, CI del ÚLTIMO commit; revisor solo si el diff va más allá del test y del informe | Hecho; el revisor, ver §10.2 | §9; §10.2 |

## 8. Exposiciones

De la sesión, ninguna. Del revisor, una, declarada el mismo día en
`docs/validation/HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-11): listó `knowledge/cases` con un
`grep` detrás, y la pantalla solo enseñó `knowledge/cases/retirados.yaml` (§10, §10.1). Nada de
holdout, `data/`, crudas, propuestas ni material del trader. El caso del holdout
de `test_estado_sesion.py` es sintético, en un repositorio temporal. La rotura de E3 que hace
imprimir el id del caso retirado corrió en el clon con `--tb=no -rN` y solo se guardó la última
línea de pytest: el id no salió a ningún log ni a la pantalla.

## 9. CI de Linux

La rama toca `.claude/` y hooks: se empuja como `fix/entorno-code` (`RITUAL.md`), con
`git push origin trabajo/entorno-code:refs/heads/fix/entorno-code` (el clasificador lo dejó pasar).

| Run | Commit | Resultado |
|---|---|---|
| 38122720438 | `0c2cb22` | `failure` solo por el fallo aceptado: `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, «PROJECT_STATE declara la rama 'trabajo/entorno-code'; la rama actual es 'fix/entorno-code'». 1 failed, 2.545 passed, 9 skipped (`gh run view 38122720438 --log-failed`) |
| 38124850342 | `4b80c58` | `failure` solo por el mismo fallo aceptado: 1 failed, 2.546 passed, 9 skipped |

Como en las ramas anteriores, ese fallo para `make` en el paso `test`, así que en Linux no
corren `state`, `config` ni `knowledge` (en Windows, verdes en cada `make check` de la rama). El
run del último commit de la rama va en el mensaje final.

## 10. El revisor

Subagente `revisor` (ya con `model: opus`, E2), lanzado sobre `0c2cb22` con el alcance del
encargo. Su informe, tal cual (no cita ningún tramo no citable: cero retiradas):

> ## Informe del revisor · trabajo/entorno-code (HEAD 0c2cb22) · 2026-10-11
>
> Base: `git merge-base main HEAD` = d32db01. Son 5 commits (bb3e3fd, 9fe3d44, 248d8df, efe7f92, 0c2cb22) y 27 ficheros. Cuando empecé, el árbol estaba limpio. Durante la revisión apareció sin commitear ` M docs/validation/ENTORNO-CODE.md`: es la sesión, que rellena el §9 con el run de la CI. Reviso HEAD y anoto ese cambio donde corresponde.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | `abrir-rama` atribuye a `RITUAL.md` lo de consultar la CI «con el sha LITERAL», pero RITUAL no lo dice: su orden monta el sha con `$(git rev-parse HEAD)`. La regla del sha literal sale de las órdenes de cierre del consultor y no de RITUAL. Es una afirmación que su cita no sostiene, y la skill y el runbook dan dos formas distintas de hacer la misma consulta. | `.claude/skills/abrir-rama/SKILL.md:53-54` («por la API de check-runs con el sha LITERAL (`RITUAL.md`)»). `docs/runbooks/RITUAL.md:317` (`curl ... /commits/$(git rev-parse HEAD)/check-runs`). `grep -n literal docs/runbooks/RITUAL.md` solo da :128 y :140, que hablan de otra cosa. La regla sí está en `docs/state/HISTORIA.md:5954` («consúltala con el sha de 40 caracteres escrito tal cual»). |
> | a2 | menor | En el paso 1 de `abrir-rama` no se sabe qué sha es «ese sha» de la CI. La viñeta anterior acaba con el merge (`main^1`), y RITUAL dice que la CI que cuenta es la del commit de estado, que es HEAD, «no la del merge». | `abrir-rama/SKILL.md:49-54`; `RITUAL.md:324-325` |
> | a3 | menor | Según `auditor-encargo`, la F «es la que fija el orden de trabajo». Pero la propia F y la hoja de ruta dicen que manda la hoja. Esa coletilla tampoco venía en la corrección propuesta en 0.a. | `.claude/agents/auditor-encargo.md:54-55`; `PROJECT_STATE.md:35` («la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden»); `docs/plan/HOJA-DE-RUTA.md:3`; corrección propuesta en `ENTORNO-CODE.md:40` |
> | a4 | menor | `estado_sesion.py` hace `import guardia` en el nivel del módulo, fuera de cualquier `try`. Si `guardia.py` no se pudiera importar, el hook saldría con traza y código 1, y no con «una línea y 0» como dice su cabecera. No bloquea la sesión, porque un SessionStart con salida distinta de 0 no bloquea, pero tampoco cumple la letra de «sale con 0 siempre». Ningún test cubre ese caso. | `.claude/hooks/estado_sesion.py:14`, `:25-27`; `tests/unit/test_estado_sesion.py:217-241` (rompen la raíz y `estado`, no el import) |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` da `CONTRATO: 27 ficheros dentro del contrato de trabajo/entorno-code (riesgo medio, artefacto docs/validation/ENTORNO-CODE.md, tramo 'R0', 3 comprobaciones para el revisor)`, con exit 0.
> - **Tests del contrato.** `uv run pytest tests/unit -p no:cacheprovider -k "skills or estado_sesion or solo_lectura or revisor or pico" -rA` da `89 passed, 2255 deselected`, exit 0. Aparte, `test_memoria.py`, `test_project_state.py`, `test_historia.py` y `test_revisor.py` dan `72 passed`.
> - **`make check`.** No lo ejecuté. Su evidencia es `make-check.log`: `2555 passed`, la línea `SELLO: make check en verde sobre el arbol a755a03db28b…`, que es igual a `git rev-parse HEAD^{tree}`, la línea `DURACION ... 927 s` y, la última, `PICO DE MEMORIA ... 294 MiB`.
> - **`mypy --strict`** sobre las tres guardias y `contrato_rama.py`, con `--cache-dir=nul`: `Success: no issues found in 4 source files`.
> - **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`.
> - **Régimen de cambios.** El diff está vacío sobre `knowledge/`, `data/manifests/`, `src/`, `config/`, `docs/adr/`, `Makefile`, `pyproject.toml`, `uv.lock`, `scripts/sello_make_check.py`, `cerrar-rama` e `ingerir-sesion`.
> - **Ambigüedades, ADR, citas de la spec, items de evidencia.** No se tocan.
> - **Informes cerrados.** Ninguno: en `docs/validation/` la rama solo añade `ENTORNO-CODE.md` (A).
> - **HISTORIA.** 192 inserciones y 0 líneas quitadas.
> - **PROJECT_STATE.** 21.942 bytes frente a 21.959 en `main`, saldo −17.
> - **Ensayos en clones.** Se hicieron con `git worktree --detach` (§3.4). En `.git/worktrees/` no quedan `ecA` ni `ecB`. Queda un `wt-ci` del 2026-09-29, ajeno a esta rama.
> - **Citas del informe que contrasté:** `guardia.py:255/:423` (Politica, motivo_fichero), `:1772` y `:1786-1789` (make con `-`/`=`), `ERRORES-RECURRENTES.md:13`, `docs/encargos/trabajo-reabrir-y-fuente-documental.md:61` (lo del «23.000»), `test_revisor.py:157-160`, `ingerir-sesion/SKILL.md:89` y `cli.py:3222-3251`. Todas dicen lo que el informe les atribuye.
>
> **Alcance 1, contradicciones.** Además de a1-a3, contrasté:
> - `activar-sesion` con `AMBIGUEDADES.md:26-55` (cinco sitios, REOPEN y supersede), con `cli.py` (`feedback new` y `PROCEDENCIAS`) y con ADR-0070 «Decision» punto 3;
> - `fase-cero` con ADR-0072 y con la regla de no listar carpetas con meses reservados de `ERRORES-RECURRENTES.md:70-77`;
> - `entregar-rama` con RITUAL (CI por `fix/`, fila de ERRORES al cerrar, puntos 3 y 4). Su cita de zoneinfo está en `trabajo-cases-rejilla.md:35`;
> - `comparar-con-main` con «Ensayos aislados»;
> - `CLAUDE.md` con `test_revisor.py`: la frase exigida sigue intacta;
> - `ERRORES-RECURRENTES.md:13-17` con `RITUAL.md:132-136` y `cerrar-rama`.
>
> Fuera de a1-a3 no encontré contradicción.
>
> **Alcance 2, puertas de las skills.** `cerrar-rama` e `ingerir-sesion` no cambian. En `abrir-rama` el diff solo amplía: siguen el `checkout`, el `status` vacío, el sha del encargo y «se para y se pregunta».
>
> **Alcance 3, el hook de arranque.**
> - Solo abre ficheros dentro de `leer`, que exige la lista cerrada y `Politica.motivo_fichero`. Ante cualquier motivo, incluido el de tramo, no lee.
> - Lo demás son `exists()` (medir, permitido) y git de lectura con `timeout=5`.
> - Lanzado a mano (`python .claude/hooks/estado_sesion.py`): 0,149 s y exit 0. Hoy imprime «ESPERANDO al consultor», y es correcto, por la PARADA del §4.
>
> **Alcance 4, `make rapido`.** El `Makefile` es el de `main` (diff vacío). Lo preparado en §4 (`rapido: lint types contracts`) no llega a `desellar`, `sellar` ni `check` (lo comprobé leyendo el `Makefile`): no sellaría. Solo dejaría en `.git` el acumulador de `pico_memoria`, y el `empezar` del siguiente `make check` lo borra.
>
> **Alcance 5, holdout.** La rama no toca nada de holdout. Hay una observación sobre la rotura del retirado en «Lo que no pude comprobar».
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 28 hechos, 4 parciales, 3 no hechos (uno es la PARADA declarada y dos esperan a este informe).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Verificar la base antes de abrir | Hecho | `ENTORNO-CODE.md:7-11`. Lo comprobé de nuevo: `stable/F37k-hoja-de-ruta^{commit}` = 7823568 y la CI de d32db01 da `python completed success` por la API de check-runs |
> | 2 | Abrir con `abrir-rama`: encargo tal cual, `tramo: R0`, Archivo en HISTORIA | Hecho | bb3e3fd; `contrato.yaml:4`; HISTORIA +192/−0 |
> | 3 | Paquete versión 2 | Hecho | el `auditor-encargo.md` del paquete lleva «5. **El tramo**» |
> | 4 | Piezas TAL CUAL salvo lo corregido, cada corrección declarada | Hecho | `diff --strip-trailing-cr` del paquete contra lo instalado, en las seis piezas: cada diferencia es una fila de §3.1 (`ENTORNO-CODE.md:288-305`) |
> | 5 | `ESPECIFICACION.md` no se copia | Hecho | `git diff --name-status` |
> | 6 | NO cambia src/, spec, knowledge, parámetros ni informes cerrados | Hecho | diff vacío |
> | 7 | NO cambia nada de lo que sella `make check` | Hecho | `Makefile` y `sello_make_check.py` sin cambios. `pico_memoria.py` solo añade la línea DURACION antes de la del PICO, que sigue siendo la última del log; lo pedía E3 de la especificación |
> | 8 | NO cambian las puertas de las tres skills | Hecho | ver alcance 2 (y b2) |
> | 9 | Papeles de ADR-0072 | Hecho | `fase-cero/SKILL.md:40-42` |
> | 10 | Nada de holdout | Hecho | §8 del informe; diff |
> | 11 | Saldo de PROJECT_STATE ≤ 0 | Hecho | −17 bytes |
> | 12 | Fase 0 a) | Hecho | §0.a |
> | 13 | Fase 0 b) E1, E2 y E3 | Hecho | §0.b (las medidas de E3 no se pueden reproducir: ver más abajo) |
> | 14 | Fase 0 c) | Hecho | §0.c |
> | 15 | Fase 0 sin escribir en el repo, y PARADA | Hecho | `git diff bb3e3fd 9fe3d44 --stat`: solo el informe |
> | 16 | Respuesta y añadido tal cual, en el encargo y en el informe | Hecho | `diff` de encargo:30-43 contra informe:258-271 y de encargo:47 contra informe:275: iguales |
> | 17 | E1: el hook y sus tests; el hook entra en `mypy --strict` del Makefile | Parcial (declarado) | 11 tests pasan; la línea `types` es la PARADA del §4 |
> | 18 | E2: opus, con la cifra medida (20 de 28; 4 de 7) | Hecho | `revisor.md:5`; §3.3 |
> | 19 | E3, respuesta 0: `make rapido` sin variables | No hecho: PARADA declarada | §4. El añadido lo permite («apunta esa pieza como PARADA … y sigue») |
> | 20 | E3, respuesta 1: los cinco tests de `knowledge validate` comparten una ejecución, con (a)-(d) | Hecho (4 de 5; G1 se queda y se dice por qué) | `tests/conftest.py:52-94`; §3.4; en el diff no cambia ninguna línea `assert` |
> | 21 | E3: la duración por paso en `pico_memoria` | Hecho | `make-check.log`, línea DURACION |
> | 22 | E4, con `NN` | Hecho | `test_skills.py:22`, tests del test en :133-174 |
> | 23 | E5: CLAUDE.md, el revisor y ERRORES-RECURRENTES:13 sin recuadro | Hecho | `CLAUDE.md:21-37`; `revisor.md:120-123`; `ERRORES-RECURRENTES.md:13-17` |
> | 24 | E6: la base entera, con `feature/*` y `fix/*` locales | Hecho | `abrir-rama/SKILL.md:44-58` |
> | 25 | E7: la lista medida y `--incluir-holdout`, cada forma con su test | Hecho | `solo_lectura.py:46-50`, `:90-93`; `test_revisor.py:167-225` (15 + 5 casos) |
> | 26 | Respuesta 5: clones en ruta corta, con el test y su motivo | Hecho | `comparar-con-main/SKILL.md:23-31` |
> | 27 | Respuesta 8: los huecos de 0.c preparados para la hoja | Hecho | §6, G.4 |
> | 28 | Las líneas de F y de R0.2 preparadas para el commit del contrato | Parcial | ver b1 |
> | 29 | `make check` sellado antes de cada commit | Hecho | SELLO = árbol de HEAD |
> | 30 | Push como `fix/entorno-code` y CI de Linux, con sus runs | Parcial | En HEAD el §9 dice «se anotan aquí». El cambio sin commitear añade el run 38122720438, que comprobé: `headSha` 0c2cb22, `failure`, `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, `1 failed, 2545 passed, 9 skipped`. Es el único fallo aceptado |
> | 31 | El revisor, pegado al final | No hecho (es este informe) | — |
> | 32 | «Rama lista para revisión, NO cerrada» | No hecho | `## Estado` de HEAD: «falta la entrega» |
> | 33 | Entrega con `entregar-rama` | Parcial (en curso) | §7, fila 25 |
> | 34 | «El encargo, punto por punto» | Hecho | §7 |
> | 35 | Nunca tocar `main` | Hecho | `ls-remote`: `main` en d32db01 |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | Las líneas preparadas para el commit del contrato rompen `make check`. R0.2 lleva `Refs: NA:F`, y lo preparado la marca HECHA mientras la F sigue viva («F. Orden de trabajo: E …»). `test_hoja_de_ruta.py` falla si una entrada HECHA lleva una letra viva. Hay que preparar también qué pasa con la `NA:F` de R0.2: quitarla de sus Refs o no marcarla HECHA. | `ENTORNO-CODE.md:545-549`; `tests/unit/test_hoja_de_ruta.py:144-145`. Lo simulé en memoria, con `problemas_b` sobre PROJECT_STATE y la hoja con esas dos líneas aplicadas, sin escribir nada. Salida: `['R0 «R0.2 · El entorno de trabajo del consultor y de la sesión»: NA:F esta HECHA y la letra sigue viva']` |
> | b2 | importa | El cambio del paso 4 de `abrir-rama` se justifica como «solape aceptado con la respuesta 5». El cambio quita «Si el encargo pide un inventario antes de tocar codigo, nace con el» y deja «nace EN CURSO; el inventario lo escribe `fase-cero`». Pero la respuesta 5 acepta «Las correcciones de 0.a», y este cambio sale de 0.c (solapes), que el §1 no puso a decisión: su punto 5 son las correcciones de 0.a y el 8 los huecos de 0.c. Está declarado, pero la aceptación que cita no lo cubre. | `ENTORNO-CODE.md:181-183`, `:241-245`, `:265`, `:484-485`; `git diff main...HEAD -- .claude/skills/abrir-rama/SKILL.md` (el hunk de `@@ -52,8 +66,9 @@`) |
> | b3 | menor | E5 pide «una línea cada uno con cuándo se usa». `ingerir-sesion`, `retomar-rama` y los dos agentes van juntos en un párrafo. | `CLAUDE.md:33-37`; ESPECIFICACION E5 |
> | b4 | menor | La respuesta 1 (c) pide «un caso roto a propósito por test». `test_knowledge_validate_real_repo` y `test_cli_entrypoint_runs` comparten una sola rotura (el borrado del ADR-0071). Los dos fallan, pero ninguna rotura mira algo propio de `cli.main`. | `ENTORNO-CODE.md:392` |
>
> Lo que la rama hace y el encargo no pide: la cabecera tolerante y el `name` del agente en E4, el límite del `Makefile` en `entregar-rama` y los cambios de `test_memoria.py`. Todo está declarado y justificado (§3.10). La línea de ERRORES-RECURRENTES que pide anotar el modelo del revisor sale de E2.
>
> ### Lo que no pude comprobar
> - **Una cosa que hice yo y hay que declarar.** Para localizar `retirados.yaml` ejecuté `git ls-files knowledge/cases | grep -i retir`. Eso lista la carpeta madre del holdout con un filtro detrás, que es lo que prohíbe `ERRORES-RECURRENTES.md:77` (lección 1). La pantalla solo enseñó `knowledge/cases/retirados.yaml`: ningún nombre de caso, ninguna fecha. La guardia no lo bloqueó. Como no puedo escribir, que la sesión decida si va a `HOLDOUT-EXPOSICIONES.md` hoy.
> - **La rotura del retirado (E3 c).** El guion `scratchpad/e3/e3c_romper.py:57-64` hace que `validar` emita a propósito los ids de `casos_retirados` (ocultos). Solo se guardó la última línea de pytest, con `--tb=no -rN`. No abrí `e3c.json`, así que no puedo confirmar que el id no llegó a ningún fichero.
> - **Medidas que ya no se pueden reproducir.** Las de la fase 0 en el clon (xdist, duraciones, los 20 más lentos), las de (b), (c) y (d) del §3.4 y el «21 failed, 55 passed, 8 errors» del §3.9 se hicieron en clones que ya no existen. `make-check.log` solo guarda el último `make check` (0c2cb22, 927 s), no los de 248d8df ni efe7f92.
> - **`git worktree list`.** `solo_lectura.py` lo bloquea aunque solo lee (pasaba ya en `main`). Lo sustituí con `ls .git/worktrees`.
> - **Lo que afirma `entregar-rama:42` del clasificador** («niega `gh run list`») no consta en el repo. Además choca con `cerrar-rama/SKILL.md:36`, que manda usar `gh run list`; es una skill protegida en esta rama.
> - **No ejecuté `make check`** ni nada que escriba.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. Read: el encargo, `contrato.yaml`, `ENTORNO-CODE.md`
> 3. `uv run python scripts/contrato_rama.py`
> 4. `git diff --name-status main...HEAD`; `tail`/`grep` de `make-check.log`
> 5. `git rev-parse HEAD^{tree}`; `sed -n 60,96p make-check.log`
> 6. `uv run pytest tests/unit -q -p no:cacheprovider -k "skills or estado_sesion or solo_lectura or revisor or pico"` (dos veces, la segunda con `-rA`)
> 7. `uv run pytest tests/unit/test_memoria.py tests/unit/test_project_state.py tests/unit/test_historia.py tests/unit/test_revisor.py -p no:cacheprovider`
> 8. `git log --format='%h%n%B----' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD -- knowledge/ data/manifests/ src/ config/ docs/adr/ .claude/skills/cerrar-rama .claude/skills/ingerir-sesion Makefile pyproject.toml uv.lock scripts/sello_make_check.py`
> 9. `git diff main...HEAD --` sobre abrir-rama, CLAUDE.md, ERRORES-RECURRENTES, revisor.md, settings.json, PROJECT_STATE.md, solo_lectura.py, pico_memoria.py, conftest.py y los tests
> 10. Grep/Read de RITUAL.md (:90-179, :300-339), AMBIGUEDADES.md, cli.py, feedback/modelo.py, HOJA-DE-RUTA.md, test_hoja_de_ruta.py, guardia.py, las seis piezas nuevas, ESPECIFICACION.md
> 11. `uv run python -B -c "…problemas_b…"` (la simulación en memoria de b1; el primer intento, con una variable de entorno, lo bloqueó la guardia)
> 12. `python .claude/hooks/estado_sesion.py` con `time`
> 13. `git ls-files knowledge/cases | grep -i retir` (declarado arriba)
> 14. `cat Makefile`
> 15. `uv run mypy --strict --cache-dir=nul …`; `git status --short --ignored`; `git diff --stat`
> 16. `gh run view 38122720438 --json …` y `--log-failed | grep`
> 17. `diff` de las respuestas entre el encargo y el informe; `git diff bb3e3fd HEAD -- docs/encargos/…`; `git diff bb3e3fd 9fe3d44 --stat`
> 18. `ls .git/worktrees`, `git branch --list`, `git ls-remote --heads origin` (`git worktree list` lo bloqueó solo_lectura)
> 19. `diff --strip-trailing-cr` del paquete contra lo instalado, en las seis piezas
> 20. `gh api …/commits/d32db01…/check-runs`; `git rev-parse "stable/F37k-hoja-de-ruta^{commit}"`
> 21. `grep` de `- Tag: ` en HISTORIA, de los heredados de PROJECT_STATE, de UMBRAL-MAYO, de ADR-0070 y de cases-rejilla

### 10.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Arreglado. `abrir-rama` cita la fuente real: las órdenes de cierre del consultor en `docs/state/HISTORIA.md` («consúltala con el sha de 40 caracteres escrito tal cual», :6521 y :6821), y dice que la orden de `RITUAL.md` lo monta con `$(git rev-parse HEAD)`. `entregar-rama` cita lo mismo |
| a2 | menor | Arreglado: el paso 1 dice que la CI es la de HEAD (el commit de estado, no el merge), con la frase de `RITUAL.md` |
| a3 | menor | Arreglado: «la siguiente según la hoja, que manda el orden (lo dicen la propia hoja y la F)» |
| a4 | menor | Arreglado: `import guardia` pasa dentro del `try` de `leer`; si no se puede importar, «la guardia no pudo decidir (ModuleNotFoundError)» y no se lee nada. Test nuevo: `test_si_la_guardia_no_se_puede_importar_no_se_lee_nada` |
| b1 | importa | Arreglado en §6: R0.2 deja `NA:F` (pasa a `—`), la `NA:F` viva entra en R1.1 y su «Depende de» se ajusta. Simulado en memoria con `problemas_a`, `problemas_b` y `problemas_c` del test: sin problemas |
| b2 | importa | Deshecho: la frase del paso 4 de `abrir-rama` vuelve a la de `main`, y el cambio es el punto 1 de la PARADA de §4 |
| b3 | menor | Arreglado: `CLAUDE.md` da una línea a `ingerir-sesion`, a `retomar-rama` y a cada agente |
| b4 | menor | Arreglado: rotura propia de `cli.main` (su despacho de `knowledge validate` devuelve 1), en un clon `C:\ecB` en `0c2cb22`: `test_cli_entrypoint_runs` falla y `test_knowledge_validate_real_repo` pasa (tabla de §3.4 (c)) |
| Lo que no pudo comprobar, 1 | — | Declarado el mismo día en `docs/validation/HOLDOUT-EXPOSICIONES.md` (el contrato se amplió con ese fichero, comentado). La guardia de Claude Code no bloqueó `git ls-files knowledge/cases \| grep`: listar la carpeta madre del holdout con un filtro detrás. Propuesta para la hoja, carril de guardias (G.1): que la guardia lo niegue |
| … 2 | — | `scratchpad/e3/outc/e3c.json` (de la sesión) guarda solo, por caso, el código de salida y la última línea de pytest, que es la de progreso (`F … [100%]`): ningún id. Los logs de pytest de esas roturas no se guardaron |
| … 3 | — | Cierto: las medidas viven en la carpeta temporal de la sesión (guiones y salidas: `scratchpad/e3/`), fuera del repo, y los clones se retiraron como manda `comparar-con-main`. Las cifras de `make check` de `248d8df` y `efe7f92` se copiaron al informe desde su `make-check.log` en el momento |
| … 4 | — | `solo_lectura.py` niega `git worktree list` porque `worktree` no está en `GIT_LEE` (ya en `main`). No es de esta rama: anotado para la hoja, carril de guardias |
| … 5 | — | Arreglado en `entregar-rama`: ya no dice que el clasificador niegue `gh run list` (en otras ramas pasó: `GUION-MISMO-COMANDO.md:1782`); usa `gh run list` o, si se niega, la API con el sha escrito tal cual |

### 10.2 El revisor, segunda pasada (lo de la tarde), tal cual

El diff de las dos respuestas de la tarde va más allá del test y del informe (`Makefile`,
`test_make_rapido.py`, `abrir-rama`), así que, por la respuesta de §4.4 (punto 5), se pasó el
revisor otra vez, sobre `git diff --cached 4b80c58` con todo estadiado y el informe terminado
salvo esta sección. Su informe, tal cual (nada de tramos no citables: ninguna retirada):

> ## Informe del revisor · trabajo/entorno-code (segunda pasada, solo el delta estadiado frente a 4b80c58) · 2026-10-11
>
> Alcance: `git diff --cached 4b80c58` (7 ficheros: Makefile, tests/unit/test_make_rapido.py, tests/unit/test_guardia_claude.py, .claude/skills/abrir-rama/SKILL.md, PROJECT_STATE.md, docs/encargos/trabajo-entorno-code.md, docs/validation/ENTORNO-CODE.md). No repito la primera pasada (§10).
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | Lo preparado para el cierre (§6) no dice que el `make check` del commit del contrato tampoco lo puede lanzar la sesión. Ese commit se hace EN LA RAMA, con el `Makefile` de la rama, que no es el de `main`, así que la guardia lo niega igual que ahora. Lo tiene que lanzar Aleks con «!». `cerrar-rama` no lo dice y no se puede cambiar en esta rama (`rutas_protegidas`). Solo lo dice `entregar-rama`. Tras el merge, el `make check` del commit de estado en `main` sí pasa, porque entonces el `Makefile` ya es el de `main`. | `docs/runbooks/RITUAL.md:157-164` (`git rm contrato.yaml` … `make check > make-check.log 2>&1` en la rama de trabajo); `.claude/hooks/guardia.py:3125-3132` (si el fichero no es igual al de `main` y el lenguaje es `make`, niega con «lo lanza Aleks en su terminal con «!»»); `ENTORNO-CODE.md:684-715` (§6 no lo menciona); Grep `Makefile\|«!»` en `.claude/skills`: solo `entregar-rama/SKILL.md:33-35`. |
> | a2 | importa | El informe remite a un §10.2 que no existe. La fila 34 dice «Hecho; el revisor, ver §10.2» y el Estado dice «otra pasada sobre lo de la tarde (§10.2)». La respuesta de §4.4, punto 5, pide pasar al revisor «y decirlo» si el diff va más allá del test y del informe. Aquí va más allá: entran el `Makefile`, `test_make_rapido.py` y `abrir-rama`, que nunca se commitearon. Mientras no esté pegado, el Estado afirma algo que no está. | Grep `^#{2,4} \|10\.2` en `ENTORNO-CODE.md`: encabezados hasta `### 10.1` (línea 915) y `## Estado` (933), ninguno `10.2`; menciones en las líneas 754 y 940. |
> | a3 | menor | La fila de ERRORES-RECURRENTES preparada en §6 solo cuenta la primera pasada del revisor («3 importa … y 5 menor, todos atendidos (§10.1)»). Hay que añadir esta. | `ENTORNO-CODE.md:714-715`. |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` → «CONTRATO: 31 ficheros dentro del contrato de trabajo/entorno-code (riesgo medio, artefacto docs/validation/ENTORNO-CODE.md, tramo 'R0', 3 comprobaciones para el revisor)». Coincide con los «31 ficheros» de §5.
> - **Comprobación 1 del contrato.** `uv run pytest tests/unit -k "skills or estado_sesion or solo_lectura or revisor or pico" -p no:cacheprovider` → «90 passed, 2263 deselected in 78.42s».
> - **Comprobación 3 (`make check`), sin ejecutar.** La evidencia es `make-check.log` (11-10, 09:23), que es el de §4.3:
>   - línea 6: CONTRATO con 30 ficheros;
>   - línea 14: `mypy --strict` con `estado_sesion.py` en «Success: no issues found in 4 source files»;
>   - líneas 103-105: los dos FAILED de `test_el_ritual_y_los_runbooks_pasan[...]` y «2 failed, 2562 passed in 1065.21s»;
>   - línea 106: «make: *** [Makefile:51: test] Error 1»;
>   - sin línea SELLO ni PICO DE MEMORIA.
>
>   Es lo que dice §4.3. El `make check` que sellará el commit todavía no existe.
> - **La guardia no se toca.** `git diff --cached --name-status main` no lista `.claude/hooks/guardia.py`.
> - **Lo que sella `make check`.** `git diff main -- Makefile`: solo tres cambios, que son `.PHONY`, la línea de `mypy --strict` y `rapido:` con su comentario. Las líneas `check:` (82), `desellar` (75-77) y `sellar` (79-80) son las de `main`.
> - **El acumulador de `rapido`.** Vive en el directorio de git (`scripts/pico_memoria.py:4`, `git rev-parse --git-path botsito-pico`) y `empezar` lo borra (`:7`, `:126`). §4.2 dice lo mismo.
> - **Sin knowledge/spec ni cases en el delta**, así que no aplican los trailers `Fuente:` ni las tres guardias de `cita`. Sin ADR, sin ambigüedades, sin evidencia nueva y sin informe cerrado tocado: ENTORNO-CODE.md es nuevo en la rama.
> - **PROJECT_STATE.md.**
>   - Tamaño: `wc -c` 21942, igual que `4b80c58` (21942). `main` tiene 21959, saldo −17.
>   - Recuento: 1486 → 1495, que son 8 de `test_make_rapido.py` y 1 nuevo en `test_guardia_claude.py`.
>   - `uv run botsito state check` → OK.
> - **Forma de los dos tests.**
>   - `uv run ruff check --no-cache` y `ruff format --check --no-cache` sobre los dos tests: «All checks passed!» y «2 files already formatted».
>   - `uv run mypy --cache-dir=nul` sobre los dos: «Success: no issues found in 2 source files».
> - **Las dos respuestas del consultor, copiadas.** Comparadas por programa entre el encargo y el informe: las dos idénticas (5/5 y 16/16 líneas).
> - **Afirmaciones del informe, medidas.**
>   - §4.3 «desde esa fecha ninguna lo había cambiado»: `git log main -- Makefile` → `3027599 2026-10-01`, y `f22179f` es del 2026-10-07.
>   - §4.5, los blobs `d0cbc24…` y `0cb536c…`: coinciden con la línea `index d0cbc24..0cb536c` del diff.
>   - §4.5 «558»: `collected 558 items`.
>   - §4.5, CI con `fetch-depth: 0`: `.github/workflows/ci.yml:22`.
>   - §4.2 «Con el Makefile de main falla»: `problemas(git show main:Makefile)` → `['no existe el objetivo `rapido`']`.
>   - §9, run 38124850342: `gh run view` da headSha `4b80c587…`, failure, y el único FAILED es `test_cli.py::test_state_check_ok_on_real_repo` con «1 failed, 2546 passed, 9 skipped».
> - **Contradicciones con runbooks, RITUAL, CLAUDE.md, la hoja de ruta o un ADR.** Ninguna, salvo lo de a1. La frase nueva de `abrir-rama` cuadra con `fase-cero` (su `description` es la que escribe el inventario). `CONTRATO-DE-RAMA.md` no dice nada contrario.
> - **Holdout.** No listé `knowledge/cases` ni nada de `data/`, `corpus/`, crudas o propuestas.
>
> ### Eje (b) · Encargo (las dos respuestas del consultor de la tarde)
> Resumen: 0 bloquea, 1 importa, 2 menor. Requisitos: 13 hechos (uno de otra forma, declarado), 1 parcial, 0 no hechos y 3 pendientes por secuencia: el `make check` de Aleks, el commit y el push/CI, que van después de esta pasada.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | §4.1-0: el diff del `Makefile` tal cual: `rapido = lint types contracts`, sin desellar, sellar ni variables, y `estado_sesion.py` en `--strict` | Hecho | `Makefile:5,41,45`; `git diff main -- Makefile` (tres cambios) |
> | 2 | §4.1-0: un test que falla si `rapido` llega a desellar, sellar o check, o si una receta nombra `sello_make_check` | Hecho, con huecos (b1, b2) | `tests/unit/test_make_rapido.py`; `uv run pytest tests/unit/test_make_rapido.py -v` → «8 passed in 0.42s» |
> | 3 | §4.1-0: estadiar todo | Hecho | `git status --short`: los 7 en la primera columna, nada sin seguir |
> | 4 | §4.1-0: Aleks lanza `make check` y después se lee el log y se commitea | Pendiente (secuencia) | el único log es el rojo de §4.3 |
> | 5 | §4.1-0: no reescribir el comando para que la guardia no lo vea | Hecho, según lo que alcanzo a ver | §4.2: la sesión no lanzó `make`; §4.5: el clon `C:\ecA` se retiró sin rodear la guardia |
> | 6 | §4.1-1: la frase del paso 4 de `abrir-rama` | Hecho (b3) | `.claude/skills/abrir-rama/SKILL.md:72-73` |
> | 7 | §4.1: push a `fix/entorno-code` con su run | Pendiente para el último commit; el de `4b80c58` está verificado | run 38124850342 |
> | 8 | §4.1: §6 con «E es lo siguiente» y R0.2 HECHA | Hecho | `ENTORNO-CODE.md:688-697` |
> | 9 | §4.4-1: la condición la calcula el test con git (`main:Makefile`, si no `origin/main:Makefile`, frente a `hash-object -- Makefile`, con cwd=RAIZ), no con la guardia | Hecho | `test_guardia_claude.py:846-865`; Grep `_igual_que_en_main` en el test: 0 apariciones. Misma semántica que `guardia.py:3210-3213` |
> | 10 | §4.4-1: si coinciden, no niega; si difieren, niega con «lo lanza Aleks en su terminal con «!»» | Hecho | `:872-879`; `uv run pytest tests/unit/test_guardia_claude.py -k make_del_ritual -vv` → los dos PASSED, «2 passed, 556 deselected in 2.19s» |
> | 11 | §4.4-1: sin `main` ni `origin/main`, FALLA (no se salta) | Hecho | `:858-862`, `pytest.fail` en el `else` del `for` |
> | 12 | §4.4-1: el resto de RITUAL, igual de estricto, y ningún otro test pierde los dos `make` | Hecho | De `RITUAL` (`:793-829`) solo salen las dos líneas `make`, y el parametrizado `:832-835` no cambia. Los únicos usos de `RITUAL` son `:832` y `:1021`, y `:1021` pasa a `RITUAL + RITUAL_MAKE` |
> | 13 | §4.4-2: la guardia no se toca | Hecho | `git diff --cached --name-status main`, sin `guardia.py` |
> | 14 | §4.4-3: con el `Makefile` de la rama, el nuevo pasa y el actual falla, con comando y salida | Hecho | `make-check.log:103-105` y el `-k make_del_ritual` de arriba |
> | 15 | §4.4-3: `uv run pytest tests/unit/test_guardia_claude.py -q` en verde | Hecho de otra forma, declarado: sin `-q` | §4.5 lo explica. Medido: `uv run pytest tests/unit/test_make_rapido.py -q` solo imprime los puntos, sin la línea de recuento (`addopts = "-q -ra"`, `pyproject.toml:39`) |
> | 16 | §4.4-4: la línea de hallazgo en §4.3 y la de G.1 en §6 | Hecho, literales | `ENTORNO-CODE.md:597-598` y `:710-711` |
> | 17 | §4.4-5: estadiar, línea para Aleks, `make check`, commit, push, CI del ÚLTIMO commit | Pendiente (secuencia) | — |
> | 18 | §4.4-5: si el diff va más allá, pasar el revisor y decirlo | Parcial: esta pasada existe, pero el §10.2 donde va no (a2) | `ENTORNO-CODE.md:754,940` |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | `test_make_rapido.py` no ve una regla con dos objetivos. Su docstring dice que `rapido` no llega al sello «ni por sus prerrequisitos», pero `rapido otro: sellar`, o `lint types: sellar`, añade `sellar` a `rapido` en GNU make y el test no lo ve. La causa es que `OBJETIVO` solo casa un nombre antes de `:`. La aserción de igualdad exacta sobre el `Makefile` real (`["lint","types","contracts"]`) tampoco lo caza, porque esa línea no se lee como de `rapido`. Así que esa rotura pasa los dos tests. | `tests/unit/test_make_rapido.py:1-4` (docstring) y `:14` (`OBJETIVO = re.compile(r"^([A-Za-z_][A-Za-z0-9_.-]*)\s*:(?!=)\s*(.*)$")`). Medido con `problemas()`: `"rapido otro: sellar\nrapido: lint\n"` → `[]` y `_leer(...)["rapido"]` → `(['lint'], [])`. |
> | b2 | menor | Otras formas que el detector no ve, aunque ninguna sale del `rapido` del `Makefile` real: `make check` escrito literal, o `$(UV) run make sellar`, en una receta (solo mira `$(MAKE)`); `include extra.mk`; y la ruta del sello escondida en una variable con `+=` o `define`. Con la igualdad exacta de `rapido`, solo cuentan si entran en las recetas de `lint`, `types` o `contracts`. Las ve el consultor al revisar, y la guardia no deja a la sesión ejecutar un `Makefile` cambiado. §4.2 describe bien el alcance («por cualquier `$(MAKE)`»). | Medido con `problemas(BASE + ...)`: `"\tmake check"` → `[]`; `"\t$(UV) run make sellar"` → `[]`; `"include extra.mk"` → `[]`; `"S += scripts/sello_make_check.py"` con `python $(S) sellar` → `[]`; `define S … endef` → `[]`. Las que sí ve: `$(MAKE) -f Makefile check` → `['`rapido` llega a `check`']`, y la receta en línea `rapido: ; python scripts/sello_make_check.py sellar` → `['`rapido` llega a `sellar`']`. |
> | b3 | menor | La frase del paso 4 no es literal: la respuesta dice «nace con su cabecera y EN CURSO; la fase 0 la escribe fase-cero en su commit», y la skill añade «(un `## Estado` EN CURSO)» y empieza con mayúscula. El sentido es el mismo y no se pierde ninguna puerta, pero §4.2 copia la frase de la skill sin decir que difiere de la de la respuesta. | `.claude/skills/abrir-rama/SKILL.md:72-73`; `docs/encargos/trabajo-entorno-code.md`, sección «Respuesta del consultor a la PARADA de ENTORNO-CODE.md §4», punto 1. |
>
> Lo que el delta hace y las respuestas no piden: nada fuera de ellas. `PROJECT_STATE.md` solo cambia el recuento de tests, la §5 y la §3.10 del informe se actualizan, y la tabla de §7 se amplía (filas 27-34).
>
> ### Lo que no pude comprobar
> - **El `make check` que sellará el commit.** No existe todavía, la guardia niega `make` con este `Makefile` y además escribe. Su evidencia será `make-check.log` (exit 0, ningún failed, la línea SELLO y la de PICO DE MEMORIA).
> - **La CI de Linux del último commit**, que aún no existe. En concreto, si en Linux la guardia niega `make` con el mismo motivo que espera el test nuevo: en Windows pasa, y la guardia ya ha divergido entre plataformas otras veces.
> - **La cara «coinciden» del test nuevo** (`motivo is None`). Con este `Makefile` no se ejercita; la ejercitará la CI de `main` tras el merge.
> - **La afirmación de §4.5 y §6** de que la guardia niega ejecutar desde la sesión, en un clon fuera del repo, un test que lleve `crudo=True`. No la reproduje, porque haría falta crear un clon (escribe). El código la hace plausible: fuera del repo `relativa()` no da ruta, el guion se analiza y `analizar_codigo` llama a `exigir_sin_crudo` (`guardia.py:3124-3141`, `:3234`). Pero el informe no cita la salida de la denegación.
> - **`uv run pytest tests/unit/test_guardia_claude.py` entero** («558 passed in 173.12s»). No lo relancé; solo vi «collected 558 items».
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git status --short && git diff --cached --stat 4b80c58`
> 2. `git diff --cached 4b80c58 -- Makefile tests/unit/test_make_rapido.py tests/unit/test_guardia_claude.py .claude/skills/abrir-rama/SKILL.md`
> 3. `git diff --cached 4b80c58 -- PROJECT_STATE.md docs/encargos/trabajo-entorno-code.md`
> 4. `git diff --cached 4b80c58 -- docs/validation/ENTORNO-CODE.md`
> 5. `git diff main -- Makefile; git diff 4b80c58 main --stat -- Makefile; git log --oneline -3 main; git merge-base main HEAD`
> 6. Grep y Read de `.claude/hooks/guardia.py` (líneas 158-172 y 3100-3240), Read de `Makefile` y Grep de `scripts/pico_memoria.py`
> 7. `grep -n "fetch-depth\|make check\|run: make" .github/workflows/ci.yml; grep -n addopts pyproject.toml; ls -la make-check.log; wc -c PROJECT_STATE.md; git show main:PROJECT_STATE.md | wc -c; git show 4b80c58:PROJECT_STATE.md | wc -c`
> 8. Grep de `FAILED|passed|SELLO|PICO DE MEMORIA|make: \*\*\*` y de `Success|CONTRATO|estado_sesion|Contracts` en `make-check.log` (una primera forma con `; date` la negó la guardia)
> 9. `uv run pytest tests/unit/test_make_rapido.py -v`
> 10. `uv run pytest tests/unit/test_guardia_claude.py -k make_del_ritual -vv`
> 11. `uv run pytest tests/unit/test_make_rapido.py -q`
> 12. Tres `uv run python -c` de solo lectura, que importan `problemas`/`_leer` de `tests/unit/test_make_rapido.py` sobre `Makefile` sintéticos (las formas de b1 y b2)
> 13. Grep de `RITUAL\b|RITUAL_MAKE` en `tests/` y Read de `test_guardia_claude.py:780-879` y `:1000-1030`
> 14. Grep y Read de `docs/runbooks/RITUAL.md` (líneas 150-299)
> 15. Grep de `ENTORNO-CODE.md` (encabezados, `«!»`, `10.2`, «Hallazgo:») y Read de `:684-718`
> 16. Grep de `Makefile|«!»` en `.claude/skills`; Grep en `fase-cero/SKILL.md` y en `CONTRATO-DE-RAMA.md`; Read de `abrir-rama/SKILL.md:60-79`
> 17. `uv run python scripts/contrato_rama.py`
> 18. `cat contrato.yaml; git diff --cached --name-status main`
> 19. `uv run pytest tests/unit -k "skills or estado_sesion or solo_lectura or revisor or pico" -p no:cacheprovider`
> 20. `uv run botsito state check`
> 21. Dos `uv run python -c` de solo lectura que comparan los bloques citados de las dos respuestas entre el encargo y el informe
> 22. Grep de `rapido|E3` en el encargo y Read de sus líneas 12-36
> 23. `uv run python -c` que aplica `problemas()` a `git show main:Makefile`, leído por subprocess (la forma con tubería la negó la guardia)
> 24. Grep de `make rapido` en CLAUDE.md, runbooks, skills y la hoja de ruta: ninguna mención
> 25. `git log -2 --format=... main -- Makefile; git log -1 ... f22179f`
> 26. `gh run view 38124850342 --json headSha,conclusion,headBranch`
> 27. `gh run view 38124850342 --log-failed | grep -E "FAILED|passed|failed"`
> 28. `uv run ruff check --no-cache ... && uv run ruff format --check --no-cache ...` sobre los dos tests
> 29. `uv run mypy --cache-dir=nul tests/unit/test_guardia_claude.py tests/unit/test_make_rapido.py`
> 30. `git status --short`, para confirmar que no quedó nada escrito
> 31. Grep de `_igual_que_en_main` en `test_guardia_claude.py`
>
> Ficheros relevantes:
> - C:\Users\USER\Desktop\Bot v3\tests\unit\test_make_rapido.py
> - C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_claude.py
> - C:\Users\USER\Desktop\Bot v3\Makefile
> - C:\Users\USER\Desktop\Bot v3\docs\validation\ENTORNO-CODE.md
> - C:\Users\USER\Desktop\Bot v3\docs\runbooks\RITUAL.md
> - C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py

### 10.3 Lo que se hizo con los hallazgos de la segunda pasada

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Arreglado en §6: un aviso para el cierre (los `make check` en la rama, `RITUAL.md:161` y `:201`, los lanza Aleks; el de `:278`, en `main`, no), y una línea para que `cerrar-rama` lo diga en una rama siguiente (aquí está en `rutas_protegidas`) |
| a2 | importa | Arreglado: esta sección y la anterior |
| a3 | menor | Arreglado: la fila de ERRORES-RECURRENTES de §6 cuenta las dos pasadas y el hallazgo de §4.3 |
| b1 | importa | Arreglado: `_leer` reparte los prerrequisitos de una regla con varios objetivos entre todos ellos. Test nuevo, `test_falla_si_una_regla_con_varios_objetivos_le_anade_el_sello` (`rapido otro: sellar` y `lint otro: check`), que con el lector de antes daba `[]` (medido por el revisor) |
| b2 | menor | Arreglado: `make` sin `$(...)` también cuenta (y `make-check.log` no), la receta en línea tras `;` se lee, `+=` suma, y `include`, `-include`, `sinclude`, `define` y `!=` son un problema («el test no sabe seguir»), no un silencio. Tests: `test_falla_si_una_receta_lanza_make_check` (cuatro formas y `> make-check.log`), `test_falla_si_una_receta_en_linea_sella`, `test_lo_que_no_sabe_seguir_es_un_problema` y la variante con `+=`. `uv run pytest tests/unit/test_make_rapido.py -vv` → «11 passed in 0.34s» |
| b3 | menor | Arreglado: la frase de la skill es la de la respuesta, literal salvo la mayúscula inicial; §4.2 lo dice |
| Lo que no pudo comprobar, 1-3 | — | Quedan para el `make check` de Aleks, la CI del último commit (en Linux se verá si la guardia niega `make` con el mismo motivo: si no, la CI falla en el test nuevo y se dice) y la CI de `main` tras el merge |
| … 4 | — | Arreglado: §4.5 cita ahora el comando y la salida de la denegación |
| … 5 | — | Medido por la sesión: «558 passed in 173.12s» (§4.5); se vuelve a ver en el `make check` |

## Estado

FASE 1 HECHA, con las dos PARADAS de la tarde respondidas y aplicadas: el `Makefile` (`make
rapido` sin sellar y el hook en `mypy --strict`) y la frase de `abrir-rama` (§4.1, §4.2), y el test
de los `make` del ritual, que suponía el `Makefile` de `main` (§4.3 a §4.5); la guardia, sin tocar.
El último commit lo sella un `make check` lanzado por Aleks. CI de Linux por `fix/entorno-code`
con solo el fallo aceptado (§9; el run del último commit, en el mensaje final); revisor pasado,
pegado y atendido (§10), y otra pasada sobre lo de la tarde, pegada y atendida (§10.2, §10.3). Lo preparado para el commit
del contrato, en §6, con «E es lo siguiente» y R0.2 HECHA.

Rama lista para revisión, NO cerrada.
