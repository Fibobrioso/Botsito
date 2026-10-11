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
| `auditor-encargo.md` | el tramo es el `## `; la entrada es el `###` con la `NA:` del encargo; «Depende de» HECHO y la siguiente según la hoja y la F (no «camino crítico») | 0.a, :48-50 |
| `fase-cero` | la columna de fechas la lee Aleks (ADR-0072); si la fase 0 la necesita, PARADA | 0.a, fase-cero :29-41 |
| `activar-sesion` | el ejemplo de herencia es el heredado 15 (A-18, R1.1), no el refiltrado HECHO; la hoja entre las fuentes | 0.a, :24 |
| `activar-sesion` | el arnés: la corrida de R3.1 y ADR-0070 («Decision», punto 3) | 0.a, :44-46 |
| `activar-sesion` | el grep de «quién la espera» incluye `docs/plan/HOJA-DE-RUTA.md` | 0.a, :55 |
| `activar-sesion` | `feedback new` con todas sus opciones obligatorias (`cli.py`), y `--valor-canonico` | 0.a, :61-63 |
| `entregar-rama` | zoneinfo citado de los encargos, no de RITUAL | 0.a, :20 |
| `entregar-rama` | sin el «23.000»: el tope es el del test y el saldo el del encargo | 0.a, :55-56 |
| `entregar-rama` | el paso 4 prepara las líneas de la Next Action y de la hoja para el commit del contrato | 0.a, paso 4 |
| `entregar-rama` | la CI por la API de check-runs con el sha literal; el log con `gh run view --log-failed` | 0.a, :38 y :63 |
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

Tests (`tests/unit/test_estado_sesion.py`, 11): rama con contrato; `main`; PARADA sin respuesta
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
alineado con 0.c y 0.a: el artefacto nace con su cabecera y EN CURSO (la fase 0 la escribe
`fase-cero` en su commit), y la Verificación incluye el artefacto. Ninguna puerta que tenía se
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

1. **El `Makefile` no cambia** (§4): `make rapido` y la línea de `mypy --strict` del hook quedan
   preparados, sin hacer.
2. `tests/unit/test_memoria.py`, `test_medir_apunta_cada_paso_y_el_informe_da_el_mayor_y_limpia`:
   el informe tiene ahora dos líneas, así que lee la ÚLTIMA (la del pico, igual que antes) y
   comprueba además la de la duración. La línea del pico sigue siendo la última de
   `make-check.log` y mide lo mismo.
3. `abrir-rama`, «el artefacto nace con el inventario» pasa a «nace EN CURSO y el inventario lo
   escribe `fase-cero`» (0.c, solape aceptado con la respuesta 5).
4. Lo de E4 de §3.5 (cabecera tolerante y `name` del agente).
5. `entregar-rama` lleva un límite que el paquete no traía (§3.1, última fila de `entregar-rama`).

## 4. PARADA de esta noche: el `Makefile` (pieza sin hacer)

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

## 5. Lo que no cambia

`git diff --stat main...HEAD` (27 ficheros): `.claude/` (las piezas, el hook, `settings.json`,
`solo_lectura.py`, `revisor.md`, `abrir-rama`), `CLAUDE.md`, `PROJECT_STATE.md`, `contrato.yaml`,
el encargo, `ERRORES-RECURRENTES.md`, HISTORIA (solo el Archivo 28), este informe,
`scripts/pico_memoria.py`, `tests/conftest.py` y siete ficheros de `tests/unit/`. Nada de `src/`,
`knowledge/`, `config/`, `data/manifests/`, ni de `cerrar-rama` o `ingerir-sesion`
(`rutas_protegidas`; `scripts/contrato_rama.py` en verde). Ningún informe cerrado ni fichero
congelado. `ESPECIFICACION.md` no se copió.

- **Lo que sella `make check` no cambia**: el `Makefile` es el de `main`, y `pico_memoria.py`
  solo añade una línea (la de la duración) ANTES de la del pico, que sigue siendo la última y
  mide lo mismo. `sello_make_check.py` y los hooks de git no se tocan.
- **Las puertas de `abrir-rama`**: las líneas que quita el diff de su `SKILL.md` son las del paso
  1, Herramientas, la frase del inventario y la Verificación, y cada una vuelve ampliada (el
  `checkout`, el `status` vacío, el sha del encargo y «se para y se pregunta» siguen). `cerrar-rama`
  e `ingerir-sesion` no cambian.
- **PROJECT_STATE.md**: 21.942 bytes frente a 21.959 de `main`: saldo −17 (solo cambian la rama,
  la funcionalidad actual y el recuento de tests, 1462 → 1485).

## 6. Preparado para el commit del contrato del cierre

En la rama no se tocan (RITUAL, puntos 3 y 4).

- **Next Action, F** (sustituye a la de hoy): si §4 se hace antes del cierre:
  `F. Orden de trabajo: E (R1.1 de la hoja de ruta) es lo siguiente; la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden.`
  Si no: `F. Orden de trabajo: el Makefile de trabajo/entorno-code (make rapido y mypy --strict del hook de arranque, PARADA de ENTORNO-CODE.md §4) y después E; la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden.`
- **Hoja de ruta, R0.2**: se añade `- **Estado:** HECHA (\`stable/F37l-entorno-code\`; docs/validation/ENTORNO-CODE.md).`
  (con §4 hecho; si no, la línea dice qué queda).
- **Hoja de ruta, carril «guardias y deuda»** (respuesta 8), una entrada nueva:
  `### G.4 · Las tareas repetidas que ninguna skill cubre` con `Refs: NA:F`; `Qué es:` los huecos
  de 0.c (escribir un ADR nuevo; sacar líneas de PROJECT_STATE a HISTORIA con saldo ≤ 0; material
  escrito del trader al corpus; registrar respuestas de FTMO o de Aleks; congelar un CSV de la
  demo; demostrar un test por mutación; comparar reglas con main caso a caso; recuadros de
  corrección; las notas del consultor para la orden de cierre) y volver a medir `pytest-xdist` con
  la cifra nueva de E3 (respuesta 1); `Depende de: R0.2`; `Quién: la sesión, con el encargo del
  consultor`; `Hecho cuando: cada hueco tiene skill o se decide que no la necesita`.
- **ERRORES-RECURRENTES**, la fila de la rama, con el modelo del revisor: `opus` (§3.3).

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
| 8 | E1, con sus tests (incluidos los que rompen a propósito) | Hecho, salvo la línea del `Makefile` | §3.2; §4 |
| 9 | E2, justificado con la cifra medida (20 de 28; 4 de 7) | Hecho | §3.3 |
| 10 | E3, punto 0: `make rapido` sin variables; la guardia no se toca | **No hecho: PARADA** | §4 (la guardia no se tocó) |
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
| 21 | `make check` sellado antes de cada commit | Hecho | `9fe3d44`, `248d8df`, `efe7f92` y los siguientes |
| 22 | Push como `fix/entorno-code` y CI de Linux, con sus run | Pendiente al escribir esto | §9 |
| 23 | Informe con fase 0, PARADA, respuesta, lo hecho, estado y las líneas de F y R0.2 | Hecho | este informe; §6 |
| 24 | Revisor con el alcance del encargo, pegado al final | Pendiente al escribir esto | §10 |
| 25 | Desde la fase 1, con sus propias skills; entrega con `entregar-rama` | Hecho | este recorrido es el de `entregar-rama` |
| 26 | Añadido: trabajar sin parar; lo que choca, PARADA en el informe y seguir; nunca tocar `main` | Hecho | §4; `main` sin tocar |

## 8. Exposiciones

Ninguna. Nada de holdout, `data/`, crudas, propuestas ni material del trader. El caso del holdout
de `test_estado_sesion.py` es sintético, en un repositorio temporal. La rotura de E3 que hace
imprimir el id del caso retirado corrió en el clon con `--tb=no -rN` y solo se guardó la última
línea de pytest: el id no salió a ningún log ni a la pantalla.

## 9. CI de Linux

La rama toca `.claude/` y hooks: se empuja como `fix/entorno-code` (`RITUAL.md`). Runs: se anotan
aquí al tenerlos.

## Estado

FASE 1 HECHA salvo el `Makefile` (PARADA de §4, sin hacer); falta la entrega: CI de Linux (§9) y
el revisor (§10).
