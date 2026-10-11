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

## Estado

PARADA (fase 0 entregada el 2026-10-11). Espera la respuesta del consultor a los puntos 0-8 de
«Lo que necesito que decidas»; nada de la fase 1 está empezado y el repo solo lleva este informe.
