# Guardias de Claude Code: hooks, permisos, contrato de rama y revisor

Rama `trabajo/guardias-claude`, desde `main` en `41c9ed9`, el 2026-10-01. Encargo de Aleks, copiado
tal cual en `docs/encargos/trabajo-guardias-claude.md`: que las reglas de `CLAUDE.md` que hoy son
solo texto tengan un mecanismo que las haga cumplir. **No cambia motor, spec, knowledge ni ninguna
cifra**: no toca `src/`, `knowledge/` ni `config/`.

## 0. Inventario: cada prohibicion y lo que la hace cumplir HOY

Medido el 2026-10-01 sobre `41c9ed9`, ANTES de escribir codigo. Fuentes: `CLAUDE.md`,
`docs/runbooks/RITUAL.md` y los demas `docs/runbooks/*.md`, buscando «nunca», «no se», «prohibido»,
«solo» y sus variantes. «Lo hace cumplir» se ha comprobado leyendo el mecanismo, no su descripcion:
`scripts/git-hooks/pre-commit` y `pre-merge-commit`, el `Makefile`, `.github/workflows/ci.yml`,
`src/botsito/comun/historial.py`, `src/botsito/cases/holdout.py`, `tests/guarda_holdout.py` y los
tests nombrados. Siglas: **PC** hook `pre-commit`, **PMC** `pre-merge-commit`, **MC** `make check`,
**CI** el mismo `make check` en GitHub (solo `main`, `feature/**`, `fix/**`).

La ultima columna dice que pone ESTA rama en las filas con «nada»: **H** el hook `PreToolUse`
(`.claude/hooks/guardia.py`), **P** una regla `deny` de permisos, **C** el contrato de rama
(`contrato.yaml`, en MC), **R** el subagente revisor (no bloquea: informa), **—** no se mecaniza
aqui, con el motivo.

### 0.1 `CLAUDE.md`

| # | Regla | Hoy la hace cumplir | Esta rama |
|---|---|---|---|
| 1 | Commit directo en `main` prohibido salvo con `BOTSITO_ALLOW_MAIN=1` | PC (rechaza en `main`) | — ya cubierta |
| 2 | El cierre en `main` (merge, tag, push) SOLO ante orden explicita de Aleks; una tarea autonoma o nocturna NUNCA cierra | **nada** | — **no se activa** (§1.4): la denegacion pedida de `git push origin main` sin la variable bloquearia el ritual tal como esta escrito |
| 3 | Ningun commit sin el sello de MC | PC y PMC (sello del arbol) | — ya cubierta |
| 4 | NUNCA `--no-verify` (commit ni merge) | **nada** sobre el salto en si; el historial (CI) caza despues sus efectos en evidencia, feedback y `Fuente:` | **H + P** |
| 5 | `cherry-pick` y `rebase` no se usan para meter trabajo | **nada** | **H** |
| 6 | Ensayo de un script que escribe: en un clon desechable (`git worktree add`), nunca con copias | **nada** | **R** (el hook no distingue un ensayo de un uso) |
| 7 | La raiz de un instalador sale de un argumento o variable, nunca de `sed` | **nada** | **R** |
| 8 | Nada escribe en el repo mientras corre MC | MC (huella del arbol al empezar y al sellar) | — ya cubierta |
| 9 | `knowledge/evidence/` inmutable | PC + test de historial (MC, CI) | — ya cubierta |
| 10 | Correccion de evidencia solo con `evidence new --supersede`, mismo tema | la guardia de la CLI | — ya cubierta |
| 11 | `knowledge/feedback/` solo anadir | PC + test de historial | — ya cubierta |
| 12 | `libros.yaml` solo anadir; ningun libro se lee sin su entrada | `knowledge validate` (MC) y el lector `corpus.libro` (sha) | la lectura CRUDA de un libro por la sesion: **nada** → **H** |
| 13 | `knowledge/spec/` y `knowledge/cases/` citan su fuente | test de historial `commits_sin_fuente`, con ids que existan (MC, CI) | — ya cubierta |
| 14 | Un informe CERRADO de `docs/validation/` no se reescribe: recuadro de correccion | **nada** (Technical Debt declarada) | **R**; y **C** con `rutas_protegidas` cuando una rama no deba tocar informes |
| 15 | `data/manifests/`, transcripciones y fotogramas del corpus inmutables | PC | — ya cubierta |
| 16 | `src/botsito/domain/` sin IO, reloj ni MetaTrader | import-linter (MC, PC) | — ya cubierta |
| 17 | `Fuente:` en el CUERPO, con ids `ev-*`, `fb-*`, `ADR-NNNN` que existan | test de historial | — ya cubierta |
| 18 | Un sitio nuevo con `cita` amplia las TRES guardias en el mismo commit | **nada** (ningun test detecta un sitio nuevo sin ampliar) | **R** |
| 19 | Las cifras no van en la forma ejecutable | `spec/modelo.py` (`_cifra_de_negocio`, `knowledge validate`) | — ya cubierta |
| 20 | `knowledge/cases/holdout/{1,2,3}/` no se lee sin la puerta de ADR-0033 | la puerta `botsito.cases.holdout` (codigo) y la guarda de auditoria de `tests/guarda_holdout.py` (solo dentro de pytest) | la lectura de la SESION (Read, Grep, Bash): **nada** → **H** |
| 21 | El detalle por operacion de los xlsx, en los dias reservados, no se lee | la ingesta y el arnes con `casos_ocultos` (codigo) | lectura cruda por la sesion: **nada** → **H** |
| 22 | Ningun AGREGADO sobre un rango con un dia reservado; no lo abre ninguna autorizacion | **nada** | **H** (bloquea el libro entero de un mes con dias reservados o sin sortear) |
| 23 | Capturas de Analytics de FX Replay, en bloque y de cualquier mes | **nada** | **H** (toda imagen del material adicional) |
| 24 | La columna de fechas de un backtest: solo el consultor, una vez, antes del sorteo | **nada** | **H** (la sesion no abre el libro) + **R** (la declaracion) |
| 25 | Un fotograma se abre por instante localizado, nunca por muestreo | **nada** | — el hook no sabe si un instante estaba localizado; **R** mira que cada fotograma abierto este declarado |
| 26 | Toda exposicion se declara el mismo dia en `HOLDOUT-EXPOSICIONES.md` | **nada** | **R** |
| 27 | Abrir una ambiguedad toca YAML y tabla; tocar su texto obliga a `spec docs --escribir` | `test_project_state.py` (ids y titulos) y `test_spec_docs_generados.py` | — ya cubierta |
| 28 | Cerrar una ambiguedad toca cuatro sitios | dos con guardia (tabla y `test_kit.py`); registro y regla de la spec, **nada** | **R** |
| 29 | Los regex, con Write; nunca en un heredoc sin comillas | **nada** | **H** (heredoc sin comillas con `\` dentro) |
| 30 | `## Estado` de un ADR se lee con `split()[0]` | `tests/unit/test_adr.py` | — ya cubierta |
| 31 | Un Bash de fondo muerto por memoria no se relanza sin permiso | **nada** | — no mecanizable: el hook no ve por que murio un proceso |
| 32 | MC con la salida a un FICHERO, nunca a `/dev/null` | **nada** | **H** |
| 33 | Un informe por rama en `docs/validation/`, con su estado al final | **nada** | **C** (`artefacto`) |
| 34 | Antes de escribir codigo, revision de diseno; se contesta midiendo | **nada** | **R** (eje b, contra el encargo) |
| 35 | Nada afirma mas de lo que su cita sostiene | **nada** | **R** |
| 36 | Las transcripciones CRUDAS de las sesiones con el trader (`*.cruda-NO-LEER.*`, v7 en adelante) no se leen: solo la version filtrada (`scripts/transcribir_sesion.py`) | **nada** fuera del propio script; y `corpus frames show`, `corpus transcript show`, `kb at` y `kb find` IMPRIMEN la cruda | **H** |

### 0.2 `docs/runbooks/RITUAL.md`

| # | Regla | Hoy la hace cumplir | Esta rama |
|---|---|---|---|
| 37 | `BOTSITO_ALLOW_MAIN=1` pegada al `git commit` | PC | — ya cubierta |
| 38 | MC antes del commit, el push despues | PC (sello) | — ya cubierta |
| 39 | `git status --short` vacio antes del merge; `diff --cached` con solo `PROJECT_STATE.md` | **nada** (puerta humana) | — es el ritual, que solo corre con orden de cierre; el hook no conoce la ventana |
| 40 | `git add PROJECT_STATE.md`, NUNCA `git add -A` | **nada** | **H** (en `main`: `add -A`, `--all`, `.` y `commit -a`) |
| 41 | `--no-verify` prohibido | ver fila 4 | **H + P** |
| 42 | `main` y el tag en el MISMO push `--atomic` | `tests/unit/test_push_atomico.py` (el texto del runbook) | — ya cubierta |
| 43 | `state check` solo en la ventana C; no se sella en `main` a mitad de merge | `state check` falla por diseno en A y B, asi que MC no sella | — ya cubierta |
| 44 | `git branch -d`, nunca `-D`, y solo con la CI en verde | **nada** | **H** (`-D`, `--delete --force`); la CI en verde: — puerta humana |
| 45 | Si la CI sale roja, no se revierte `main` | **nada** | **H** (`git revert` y `git reset --hard` en `main`) |
| 46 | Una tarea autonoma o nocturna NUNCA cierra | **nada** | — ver fila 2 |

### 0.3 Los demas runbooks

| # | Regla | Hoy la hace cumplir | Esta rama |
|---|---|---|---|
| 47 | ENTRADA-MARZO: la sesion NO abre el libro de marzo antes del paso c; en el paso a lo abre Aleks | **nada** | **H** |
| 48 | ENTRADA-MARZO: el sorteo NO se repite nunca | `fidelidad build` se niega (codigo) | — ya cubierta |
| 49 | ENTRADA-MARZO: no se toca el lector, la herramienta del huso ni `criterio_huso.yaml` sobre la marcha | **nada** | **C** (`rutas_protegidas`) |
| 50 | ENTRADA-MARZO PARADA B0: A-42 RESUELTA antes del sorteo | **nada** en codigo (`fidelidad build` no la mira) | **R** |
| 51 | ENTRADA-MARZO: el control del huso, sobre abril, nunca mayo | **nada** | **R** |
| 52 | ENTRADA-MARZO: toda lectura se declara el mismo dia | **nada** | **R** (fila 26) |
| 53 | ARNES-MOTOR y VISOR-DIAS: ningun mes de medida ni que no sea de construccion | el arnes y el visor se niegan (`casos_ocultos`) | — ya cubierta |
| 54 | VISOR-DIAS: la salida no se commitea | `.gitignore` (`/data/*`) | — ya cubierta |
| 55 | SESION-DE-PREGUNTAS: solo graficos de dias de construccion; nunca de medicion, holdout o retirado | la comprobacion `True`/`False` del paso 1, a mano | — es lo que se ensena al trader en pantalla, no una herramienta de la sesion |
| 56 | SESION-DE-PREGUNTAS: las respuestas entran solo por la grabacion y `feedback new` | validadores del feedback | — ya cubierta en lo mecanizable |
| 57 | ACTIVAR-A35-A44: un tope distinto de la sesion 1 no se sobrescribe; nada se ajusta por lo bajo | **nada** (revision del consultor antes de `feedback apply`) | **R** |
| 58 | DEMO-FTMO: solo EURUSD y lote minimo | el propio `MedirDemoFTMO.mq5` | — ya cubierta |

**Alcance que sale de aqui:** las filas 4, 5, 12, 20-24, 29, 32, 36, 40, 41, 44, 45 y 47 van al
hook; 4 y 41 tambien a permisos; 14, 33 y 49 al contrato; 6, 7, 14, 18, 25, 26, 28, 34, 35, 50, 51,
52 y 57 al revisor. Las filas 2 y 46 se quedan sin mecanismo, y el §1.4 dice por que.

**Una fila que no estaba en el encargo y sale del inventario: la 36.** `botsito corpus frames
show`, `corpus transcript show`, `kb at` y `kb find` IMPRIMEN el segmento crudo de la transcripcion
activa, tambien la de v7, v8 y v9, cuya cruda no lee nadie (`scripts/transcribir_sesion.py`). Para
`frames show` ya lo decia `docs/validation/SESION-02-VIDEO.md:73-75` («imprime el segmento crudo
mas cercano al instante pedido»); en el codigo no hay nada que lo impida.
El hook lo cubre para la sesion (§1.2); el codigo no se toca en esta rama (§7, punto 3).

## 1. La guardia: `.claude/settings.json` y `.claude/hooks/guardia.py` (fase 1)

### 1.1 Como se engancha

`.claude/settings.json` (versionado) registra UN hook `PreToolUse` con el matcher
`Read|Grep|Glob|Bash|PowerShell` y la orden `PYTHONUTF8=1 python
"$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py"`, que Claude Code ejecuta con Git Bash en Windows.
El guion es solo biblioteca estandar (corre con el Python del sistema, 3.12, no con el entorno del
proyecto), lee el evento JSON por stdin y sale con **2 y el motivo por stderr para bloquear**, o con
0 para dejar pasar: segun la documentacion de hooks de Claude Code, el 2 es el unico codigo que
bloquea de forma fiable. `.claude/settings.local.json` va al `.gitignore`
(`test_los_ajustes_locales_no_se_versionan`). Se anade PowerShell al matcher aunque el encargo
nombra Bash: la herramienta existe en esta maquina, y sin ella la guardia se rodearia cambiando de
shell.

### 1.2 Que protege, y de donde lo saca

Nada esta escrito a mano salvo lo que `CLAUDE.md` fija; lo demas se lee del repo en cada evento.

| Material | Como lo reconoce | Regla que cita el bloqueo |
|---|---|---|
| `knowledge/cases/holdout/{1,2,3}/`, salvo su README | la ruta | CLAUDE.md punto 3 + ADR-0033 |
| Libros del trader (`xlsx`, `csv`...) de un mes que no sea legible | el mes por el nombre del fichero o de su carpeta `Backtest <mes> <ano>`; legibles = enero, abril y agosto de 2026 MENOS los meses con un caso reservado | punto 3 (ADR-0021 §1, ADR-0037) si el mes tiene reservados; «lo minimo para fijar el universo» + ENTRADA-MARZO si esta sin sortear |
| Un libro `backtesting-analytics <MES> <ANO>` fuera del repo | el nombre, este donde este | la misma |
| Toda imagen del material adicional | la carpeta y la extension | punto 3 (capturas de Analytics) + ADR-0038 |
| Todo lo de una carpeta `Backtest <mes>` de un mes no legible | la carpeta | «lo minimo para fijar el universo» (marzo: REGISTRO-MARZO.md) |
| `corpus/.../Sesiones/` (la hoja RELLENADA de la sesion 1) | la ruta | punto 3: trae las etiquetas, tambien de los casos reservados |
| `data/transcripciones/<v>/` de una sesion en cuarentena, y todo `*cruda-NO-LEER*` | las sesiones son los videos de `fuentes.yaml` con `drive_id: null` menos v6 | punto 3 + `transcribir_sesion.py` |
| Un fichero de `knowledge/cases/` o `data/visor/` con un caso reservado en el nombre | los `particiones.yaml` commiteados, con la misma regla que `casos_reservados` | punto 3 (`casos_reservados`, `casos_ocultos`) |
| Un registro de feedback que etiquete un caso reservado (`LABEL_CASE`, `MARK_*`, `BORDERLINE`) | lo lee el hook, no la sesion | la misma |

**Los reservados no se desvian del codigo:** `test_contra_el_repo_real_ve_lo_mismo_que_el_codigo`
compara la lectura del hook con `casos_reservados(RAIZ)` y las particiones con `RESERVADAS`, y fija
las sesiones en cuarentena del repo real (`v7`, `v8`, `v9`) y los meses legibles (`2026-01`,
`2026-04`, `2026-08`). Si manana abril tuviera un dia reservado, su libro dejaria de leerse solo
(`test_un_mes_de_desarrollo_con_un_dia_reservado_deja_de_ser_legible`).

**La exencion de v6 es una decision, no un hecho** (§7, punto 2): su cruda se leyo y la citan 23
items antes de que existiera la cuarentena, y su dia reservado esta retirado (ADR-0041).

### 1.3 Que deja pasar

- **Listar, medir y hashear** el material protegido: `ls`, `stat`, `du`, `wc -c`, `sha256sum` (y
  sus hermanos), `certutil -hashfile`, `find` sin `-exec` o con `-exec sha256sum`, `git
  check-ignore`, `git ls-files`, y `uv run botsito corpus inventory`. Glob siempre: listar nombres
  no es abrir (ADR-0021 §1).
- **La CLI del proyecto entera, que es la puerta**, salvo los cuatro subcomandos que imprimen una
  cruda en cuarentena (y `kb find` sin `--video`).
- **El codigo commiteado y sin cambios** (`scripts/*.py`): se miran solo sus argumentos. Si un
  argumento es material protegido, se bloquea, salvo en `scripts/huso_por_velas.py`, que es el
  paso c de ENTRADA-MARZO y lee solo las filas `dev`. El codigo NUEVO o cambiado (un guion del
  scratchpad, `python -c`, un heredoc a `python -`, un `pytest` sobre un fichero fuera de `tests/`)
  se lee como codigo sin revisar: cada literal que sea una ruta se mira, y si recorre directorios
  que construye al ejecutarse y nombra material sensible, no se decide y se bloquea.
- **Grep** desde la raiz: medido el 2026-10-01 con un fichero sonda en `data/`, el Grep de Claude
  Code no entra en lo ignorado por git desde la raiz (`/corpus/`, `/data/*`), pero SI busca dentro
  de una carpeta ignorada cuando se le da su ruta. El hook reproduce eso: desde la raiz solo le
  importan las zonas seguidas por git (hoy, ninguna con contenido protegido); con una ruta dentro
  de `data/` o `corpus/`, todas.

### 1.4 Las denegaciones, y la que NO se activa

Van en dos capas, porque la documentacion de permisos dice que una regla `deny` de Bash «no es una
frontera de seguridad»: no ve `git -C . push --force` ni una bandera en otra posicion. En
`permissions.deny` van 24 patrones (`--no-verify` en commit, merge y push; `push --force` y `-f`;
`tag -d` y `--delete`; `push --delete` y `:refs/tags/`; `rm -rf` y `rm -fr` sobre `data`,
`corpus` y `knowledge`). El hook repite las mismas reglas analizando el comando por palabras, y
anade lo que un patron no expresa: `commit -n`, `push +rama`, `--force-with-lease`, `tag -f`,
`update-ref -d`, `branch -D`, `cherry-pick` y `rebase` (salvo `--abort`), `rm -rf` sobre una
ruta que contenga esas carpetas (`rm -rf .`), y en `main`: `add -A`, `commit -a`, `revert` y
`reset --hard`.

**`git push origin main` sin `BOTSITO_ALLOW_MAIN` NO se activa, porque bloquearia el ritual.**
`RITUAL.md` empuja `main` SIN esa variable dos veces: `git push --atomic origin main stable/<tag>`
en el cierre y `git push origin main` cuando la CI sale roja (la variable va pegada al `git
commit`, correccion 1, y solo la mira `pre-commit`). Ademas, una regla `deny` no podria
expresarla: la documentacion de permisos dice que «una regla deny o ask casa por encima de
cualquier asignacion inicial», asi que `Bash(git push origin main*)` bloquearia tambien
`BOTSITO_ALLOW_MAIN=1 git push origin main`. El hook si podria, pero bloquearia los dos pushes del
ritual. Las filas 2 y 46 del inventario -una tarea autonoma nunca cierra- se quedan como estan. Dos
formas de cerrarlas, para el consultor (§7, punto 1).

**Nada de esto toca `make check`, la CI ni el ritual.** Los hooks de Claude Code solo ven las
herramientas de la sesion: no los subprocesos de `make` ni la CI, que no ejecuta Claude Code. Y
los 30 comandos del ritual y de los runbooks pasan el hook y ninguna regla `deny` los casa
(`test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual`, sobre el repo
REAL, con la semantica de patrones de la documentacion).

### 1.5 Lo indecidible se bloquea, con su forma de reescribirlo

El hook tokeniza Bash el mismo (comillas, `$(...)`, acentos graves, variables, globs, heredocs,
redirecciones, `for ... in`) y resuelve lo que se puede: un glob se expande contra el disco, una
variable asignada en el propio comando se sustituye, `$(pwd)` y `$(git rev-parse ...)` se conocen.
Lo que queda dinamico **solo bloquea si el comando lee contenido**: `echo "$HOME"` o
`git commit -m "$(...)"` pasan, `cat "$F"`, `xargs cat`, `eval`, `while read f; do cat "$f"` y un
`find -exec` lector sobre material protegido no. El mensaje termina en «Como reescribirlo: rutas
LITERALES...». Un error interno del hook bloquea solo si el comando menciona material sensible; si
no, deja pasar.

### 1.6 Medido en esta sesion

Claude Code recogio `settings.json` en cuanto se escribio, sin reiniciar, y el hook bloqueo de
verdad tres veces: un guion de depuracion del scratchpad que nombraba la carpeta del material
adicional (el mensaje de entonces citaba la regla de las capturas sin decir que el motivo era
NOMBRAR la carpeta; se corrigio), una sonda inocua `sonda.cruda-NO-LEER.txt` abierta con Read, y un
`git push --force` de esta rama. **La latencia** es de unos 90 ms por llamada (tres ejecuciones del
proceso en 0,26 s, `test_el_proceso_sale_con_2_y_el_motivo_o_con_0 --durations`). **Las reglas
`deny` no se han medido en vivo**: el hook bloquea antes, y la unica prueba es el test que aplica
la semantica documentada.

### 1.7 Lo que no ve

- **Las lineas `!` del usuario**: la documentacion no dice si los hooks las ven. No se ha medido.
- **Si falta `python`** o el guion no esta, Claude Code trata la salida como error no bloqueante y
  la herramienta SE EJECUTA (falla abierto, segun la documentacion de hooks). Lo vigilan los
  tests, que ejecutan el guion como proceso en cada `make check`.
- **El codigo commiteado es de confianza**: un guion seguido puede leer lo que quiera por dentro.
  Es la frontera del encargo: la barrera de ese codigo es `casos_reservados` y la compuerta.
- **PowerShell** se analiza mas tosco que Bash: por palabras, sin tokenizar; un comando con una
  ruta protegida solo pasa si todo el es de metadatos.
- **Lo que la salida de un comando permitido traiga**: `git log -p` sobre el holdout se bloquea
  solo cuando hay etiquetas seguidas en el; hoy no las hay.
- **El codigo de la CLI que imprime crudas** sigue igual (§0, fila 36).

## 2. El contrato de rama (fase 2)

`scripts/contrato_rama.py`, llamado por `make check` justo despues de `desellar` (objetivo
`contrato`). Formato, patrones, la plantilla y los tres ejemplos -solo knowledge, motor y
medicion- en `docs/runbooks/CONTRATO-DE-RAMA.md`; un test carga los cuatro bloques con el mismo
cargador estricto. Compara contra el merge-base con `main` lo commiteado Y lo estadiado (el arbol
que se sella), y falla nombrando cada fichero fuera de `rutas_permitidas`, cada uno dentro de
`rutas_protegidas` (que mandan), y el artefacto si no esta estadiado.

**Medido en el primer `make check` de la rama:** dentro de `pico_memoria medir`, `python` no era el
del entorno del proyecto y el objetivo `contrato` salio en rojo con `No module named 'botsito'`. Se
arreglo como ya lo hace `scripts/huso_por_velas.py`, anadiendo `src/` al `sys.path` del guion.

Tres decisiones que el encargo no fijaba:

1. **`make check` no ejecuta las `comprobaciones`**: podrian escribir en el repositorio mientras
   corre (CLAUDE.md, «nada escribe mientras corre `make check`»). Las ejecuta el revisor.
2. **«En `main` el contrato se borra en el merge»** no se puede hacer DENTRO del merge: cambiar el
   arbol fusionado obliga a sellarlo en `main` a mitad de merge, y ahi `state check` falla por
   diseno (RITUAL.md, ventana A). Sale de la rama justo antes, con su sello, en un paso nuevo de
   `RITUAL.md` («Antes del merge: el contrato sale de la rama»). En `main`, `make check` no lo
   exige; y si se colara, la rama siguiente fallaria por **contrato heredado**: el campo `rama` se
   compara con la rama actual, sin prefijo, porque el cierre puede llevar `trabajo/x` a `feature/x`.
3. **El contrato de esta rama** (`contrato.yaml`, el primer ejemplo), tal cual:

```
rama: trabajo/guardias-claude
riesgo: medio  # toca make check y lo que Claude Code deja hacer; no toca motor, spec ni knowledge
artefacto: docs/validation/GUARDIAS-CLAUDE.md
rutas_permitidas: .claude/, .gitignore, CLAUDE.md, Makefile, PROJECT_STATE.md, docs/HANDOFF.md,
  docs/encargos/, docs/runbooks/{CONTRATO-DE-RAMA,ERRORES-RECURRENTES,README,RITUAL}.md,
  docs/validation/GUARDIAS-CLAUDE.md, scripts/contrato_rama.py y los tres tests nuevos
rutas_protegidas: src/, knowledge/, config/, data/, mql5/, tools/, scripts/git-hooks/, docs/adr/,
  docs/spec/
comprobaciones: los tres tests nuevos, scripts/contrato_rama.py y make check
```

## 3. El revisor (fase 3)

`.claude/agents/revisor.md`: `tools: Read, Grep, Glob, Bash`, `model: sonnet` (la memoria del
proyecto: Sonnet para verificar y redactar), y un hook `PreToolUse` propio en el frontmatter que
le quita a Bash lo que escribe (`.claude/hooks/solo_lectura.py`: redirecciones a fichero, `tee`,
`rm`, `mv`, `cp`, `make`, `sed -i`, los `git` que cambian el repo, `uv` fuera de `uv run`, los
`botsito` que escriben salvo con `--check`, y el `python -c` que abre para escribir). La guardia del
proyecto le aplica igual. Revisa en dos ejes con un informe cada uno -(a) las reglas de la casa,
en nueve puntos que siguen el inventario del §0, y (b) el encargo partido en requisitos-, y cada
hallazgo lleva evidencia y gravedad (bloquea, importa, menor). No ejecuta `make check` ni nada que
escriba: busca su evidencia.

`CLAUDE.md` lleva la linea del encargo, literal, en «Como se trabaja», y una seccion nueva, «Las
guardias de Claude Code», que dice que hace el hook, que es defensa en profundidad y que **una
guardia no se rodea**: si bloquea algo legitimo se corrige la guardia, no se reescribe el comando.
La metrica vive en `docs/runbooks/ERRORES-RECURRENTES.md`.

## 4. Tests (fase 4)

46 funciones nuevas, 215 casos, en tres ficheros; la suite pasa de 1055 funciones (1455 casos) a
1101 (1670).

- `tests/unit/test_guardia_claude.py`: **bloquea una lectura de material reservado** (ocho rutas,
  con Read y con Bash), **deja pasar un sha256** (y `stat`, `ls`, `du`, `wc -c`, `certutil`, `find
  -exec sha256sum`, `corpus inventory`), **bloquea un Bash indecidible** (siete formas); ademas la
  regla que cita cada bloqueo, lo que si se lee, Grep, la CLI, los guiones, las 26 operaciones
  prohibidas, el ritual y los runbooks, PowerShell, el proceso de punta a punta y los ajustes.
- `tests/unit/test_contrato_rama.py`: **falla con un diff fuera de las rutas permitidas y pasa con
  uno dentro**; ademas lo protegido, lo estadiado, el artefacto, sin contrato, en `main`, el
  heredado, el mal escrito, los patrones y los ejemplos del runbook.
- `tests/unit/test_revisor.py`: **el revisor existe, su frontmatter es valido y no tiene
  herramientas de escritura**; ademas su Bash no escribe (15 comandos) y lee (14), y `CLAUDE.md`
  lleva la linea.

## 5. Ficheros

**Nuevos:** `.claude/settings.json`, `.claude/hooks/guardia.py`, `.claude/hooks/solo_lectura.py`,
`.claude/agents/revisor.md`, `contrato.yaml`, `scripts/contrato_rama.py`,
`docs/encargos/trabajo-guardias-claude.md`, `docs/runbooks/CONTRATO-DE-RAMA.md`,
`docs/runbooks/ERRORES-RECURRENTES.md`, este informe y los tres tests.
**Cambiados:** `CLAUDE.md` (dos lineas en «Como se trabaja» y la seccion de las guardias),
`Makefile` (objetivo `contrato` en `check`; `.claude/hooks` en ruff y `mypy --strict` sobre los
dos hooks y el contrato), `.gitignore`, `docs/runbooks/RITUAL.md` (el paso del contrato),
`docs/runbooks/README.md` y `PROJECT_STATE.md` (Current Branch y el recuento de tests). **No se
toca** `src/`, `knowledge/`, `config/`, `data/`, ningun ADR ni ninguna cifra.

## 6. El informe del revisor

Pendiente: se pega aqui tras pasarlo sobre esta rama.

## 7. Que debe decidir el consultor

1. **El push a `main` sin la variable** (§1.4). (a) Dejarlo como esta; (b) una regla `ask` -no
   `deny`- para `git push * main*` y `git merge*` en `main`: Claude Code pediria confirmacion en
   cada push del ritual, que ya solo corre con orden de cierre, y una tarea nocturna se quedaria
   esperando en vez de cerrar; o (c) cambiar el ritual para que el push lleve tambien
   `BOTSITO_ALLOW_MAIN=1` y activar la regla en el hook. Recomendacion: (b), porque es exactamente
   «solo ante una orden explicita» y no cambia ninguna puerta.
2. **La exencion de v6** de la cuarentena (§1.2): ¿se mantiene?
3. **El codigo que imprime crudas** (§0, fila 36): ¿una rama que haga que `frames show`,
   `transcript show`, `kb at` y `kb find` no impriman texto de una sesion en cuarentena? Hoy solo
   lo para el hook, y solo para Claude Code.
4. **El modelo del revisor**: `sonnet`. Si el consultor encuentra lo que el revisor no vio
   (ERRORES-RECURRENTES), lo primero es probar con `opus`.

## Estado

Rama lista para revisión, NO cerrada.
