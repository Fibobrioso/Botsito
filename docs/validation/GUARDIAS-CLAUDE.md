# Guardias de Claude Code: hooks, permisos, contrato de rama y revisor

Rama `trabajo/guardias-claude`, desde `main` en `41c9ed9`, el 2026-10-01. Encargo de Aleks, copiado
tal cual en `docs/encargos/trabajo-guardias-claude.md`: que las reglas de `CLAUDE.md` que hoy son
solo texto tengan un mecanismo que las haga cumplir. **No cambia motor, spec, knowledge ni ninguna
cifra**: no toca `src/`, `knowledge/` ni `config/`.

## 0. Inventario: cada prohibicion y lo que la hace cumplir HOY

Medido el 2026-10-01 sobre `41c9ed9`, ANTES de escribir codigo. **Una desviacion del encargo, dicha
con su nombre (hallazgo B1 del revisor):** la tabla se escribio en este informe antes que el codigo,
pero NO se entrego a Aleks por separado ni se commiteo antes: la sesion siguio con las fases 1 a 4
sin parar, y la rama llego con todo en el mismo commit (`3027599`). Fuentes: `CLAUDE.md`,
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
El hook lo cubre para la sesion (§1.2); el codigo no se toca en esta rama (§7, punto 4: la rama siguiente).

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
items antes de que existiera la cuarentena, y su dia reservado esta retirado (ADR-0041). **Tras la
revision, se mantiene solo con sus tramos no citables bloqueados** (§7, punto 2): sus ficheros de
texto se leen por trozos que no los toquen, las propuestas que copian segmentos de un tramo no se
abren, y la CLI no imprime un tramo.

### 1.3 Que deja pasar

- **Listar, medir y hashear** el material protegido: `ls`, `stat`, `du`, `wc -c`, `sha256sum` (y
  sus hermanos), `certutil -hashfile`, `find` sin `-exec` o con `-exec sha256sum`, `git
  check-ignore`, `git ls-files`, y `uv run botsito corpus inventory`. Glob siempre: listar nombres
  no es abrir (ADR-0021 §1).
- **La CLI del proyecto entera, que es la puerta**, salvo los cuatro subcomandos que imprimen una
  cruda en cuarentena (y `kb find` sin `--video`).
- **El codigo identico al de `main`** (`scripts/*.py`; hasta la revision bastaba con que estuviera
  commiteado y sin cambios, §7 punto 3): se miran solo sus argumentos. Si un
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
anade lo que un patron no expresa: `git -c core.hooksPath=...` y `git config core.hooksPath <x>`
(saltarse los hooks sin `--no-verify`, hallazgo A1 del revisor), `commit -n`, `push +rama`, `--force-with-lease`, `tag -f`,
`update-ref -d`, `branch -D`, `cherry-pick` y `rebase` (salvo `--abort`), `rm -rf` sobre una
ruta que contenga esas carpetas (`rm -rf .`), y en `main`: `add -A`, `commit -a`, `revert` y
`reset --hard`.

**`git push origin main` sin `BOTSITO_ALLOW_MAIN` NO se activa como `deny`, porque bloquearia el
ritual; tras la revision es una regla `ask` (§7, punto 1).**
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
- **El codigo de `main` es de confianza**: un guion identico al de `main` puede leer lo que quiera
  por dentro.
  Es la frontera del encargo: la barrera de ese codigo es `casos_reservados` y la compuerta.
- **PowerShell** se analiza mas tosco que Bash: por palabras, sin tokenizar; un comando con una
  ruta protegida solo pasa si todo el es de metadatos.
- **Lo que la salida de un comando permitido traiga**: `git log -p` sobre el holdout se bloquea
  solo cuando hay etiquetas seguidas en el; hoy no las hay.
- **El codigo de la CLI que imprime crudas** sigue igual (§0, fila 36): es la rama siguiente.
- **Una busqueda desde la raiz no se para por una propuesta con segmentos de un tramo**
  (`knowledge/_proposals/pr-v6-005000-010000-*.yaml` los tiene): pararla bloquearia toda busqueda
  del repo. Se para abrirla y buscar con una ruta dentro de `knowledge/_proposals/`.
- **Mayo, a mano** (observacion del revisor): `CLAUDE.md` deja leer sin puerta las filas de los 6
  dias `dev` de mayo (ADR-0025 §4), pero el hook bloquea abrir el libro de mayo entero, porque
  abrirlo ensena tambien las filas reservadas y los agregados. Las filas `dev` se siguen leyendo por
  el codigo (`casos ingerir`, el arnes). Si alguna tarea necesitara leerlas a mano, el hook la
  pararia: no es una prohibicion nueva de contenido, pero si un camino menos (§7, punto 4: mayo queda como esta).
- **El subagente revisor no se carga en caliente.** Escrito `.claude/agents/revisor.md`, Claude Code
  respondio «Agent type 'revisor' not found»: los subagentes se leen al arrancar la sesion. Su hook
  de solo lectura (`solo_lectura.py`) esta probado por sus tests, pero NO medido en vivo dentro del
  subagente (§6).

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

54 funciones nuevas, 230 casos, en tres ficheros; la suite pasa de 1055 funciones (1455 casos) a
1109 (1685). Dos se anadieron tras el revisor, una por cada hueco que encontro (§6), y seis tras la
revision del consultor (§7): los tramos de v6 en los ficheros, en la CLI y en las propuestas, los
tramos del repo real, el guion que no es el de `main` y la regla `ask`.

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

## 6. El informe del revisor, y que se hizo con cada hallazgo

**Como se paso.** El subagente `revisor` no estaba cargado (§1.7: los subagentes se leen al
arrancar), asi que se paso con un agente general en `sonnet` al que se le dio a leer
`.claude/agents/revisor.md` y `CLAUDE.md` con la orden de seguirlos al pie de la letra y de no
escribir. La guardia del proyecto si le aplicaba; su hook de solo lectura, no: en esta forma, el
«no escribe» lo sostuvo la orden, no el mecanismo. Reviso el commit `3027599` (arbol `1008399d`, el
del sello). Su informe va pegado TAL CUAL al final de este documento, despues del Estado, porque la
linea nueva de `CLAUDE.md` dice «al final del informe de la rama» (hallazgo B3).

| Hallazgo | Gravedad | Que se hizo |
|---|---|---|
| A1 · `core.hooksPath` salta los hooks sin `--no-verify` | importa | **Arreglado**: el hook bloquea `git -c core.hooksPath=...` y `git config [--unset] core.hooksPath ...` (y en PowerShell); leerlo pasa. Test `test_core_hookspath_es_saltarse_los_hooks` |
| A2 · `git -C <dir>` no movia la base de las rutas | importa | **Arreglado**: `-C` fija la base; `rev:ruta` va contra la raiz salvo `rev:./ruta`. Test `test_git_con_menos_c_resuelve_las_rutas_desde_su_directorio`, que fallaba antes del arreglo con `HEAD:./holdout/...` |
| A3 · `docs/HANDOFF.md` sin actualizar | menor | Se deja: el encargo no lo pide y la rama no cambia el estado del proyecto |
| B1 · la tabla de la fase 0 no se entrego antes del codigo | importa | **Declarado** en el §0: es una desviacion real del encargo |
| B2 · se deja pasar mas que stat, tamano, sha256 e inventario | menor | Declarado en el §1.3; el consultor restringio los guiones a los de `main` (§7, punto 3); del resto no dijo nada |
| B3 · el informe del revisor no quedaba al final | menor | Pegado al final, tras el Estado |
| Observacion · mayo a mano | — | Al §1.7; el consultor: mayo queda como esta (§7, punto 4) |

## 7. Lo que decidio el consultor (2026-10-01), y lo que se hizo

Revision del consultor sobre `23df399`, con orden de cierre. Las cinco decisiones:

1. **El push a `main`: regla `ask`, no `deny`.** Hecho: `permissions.ask` en `.claude/settings.json`
   con `git push * main*`, `git push *:main*` y `git push *refs/heads/main*`. El ritual sigue
   pudiendo empujar, pero Claude Code pide confirmacion; una tarea autonoma se queda esperando en
   vez de cerrar. Cierra las filas 2 y 46 del inventario. Test `test_el_push_a_main_pide_confirmacion`.
2. **v6: se mantiene la exencion, siempre que el hook bloquee sus tramos no citables** (0:41:00-0:50:11
   y 1:53:30-1:57:31). **Hoy no los bloqueaba**: se anadio. El hook lee
   `tramos_no_citables.yaml` y, para los videos con tramos que no estan en cuarentena (hoy solo v6;
   v7 y v9 ya estan enteros), bloquea: los ficheros de texto de su transcripcion salvo leidos por
   trozos (Read con `offset` y `limit`) que no toquen un tramo, con una linea de margen; las
   propuestas de `knowledge/_proposals/` con segmentos dentro de un tramo; y `frames show`, `kb at`,
   `transcript show` y `kb find` cuando su instante o su intervalo toca un tramo (o, en `kb find`, no
   esta acotado). Tests `test_v6_se_lee_salvo_sus_tramos_no_citables`,
   `test_la_cli_no_imprime_un_tramo_de_v6` (9 casos), `test_una_propuesta_con_segmentos_de_un_tramo`
   y `test_los_tramos_del_repo_real`. El comentario de `tramos_no_citables.yaml` («se puede leer y
   buscar con `kb find`») no se toca en esta rama: `knowledge/` es ruta protegida del contrato, y lo
   recogera la rama siguiente.
3. **Scripts: solo exentos los que estan tal cual en `main`.** Hecho: el hook compara el blob del
   fichero (`git hash-object`) con el de `main` (`git rev-parse main:<ruta>`, o `origin/main`). Un
   guion nuevo o cambiado en la rama en curso, aunque este commiteado, se lee entero; tambien
   `scripts/huso_por_velas.py` pierde su exencion si cambia. Test
   `test_solo_el_guion_de_main_es_codigo_revisado`: un guion nuevo de la rama que lee el libro de
   marzo queda bloqueado.
4. **Rama siguiente** (Next Action de `PROJECT_STATE.md`): «kb find, kb at, transcript show y corpus
   frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una
   opcion explicita que el hook bloquea». **Mayo queda como esta.**
5. **Estas cinco decisiones, anotadas aqui.**

Y las dos cosas que el consultor encontro y el revisor no (la 2 y la 3) van a
`docs/runbooks/ERRORES-RECURRENTES.md`.

## Estado

**Revisada por el consultor el 2026-10-01, con orden de cierre en `main`.** Las cinco decisiones del
§7, hechas en la rama antes del cierre. Antes de la revision decia: «Rama lista para revisión, NO
cerrada».

## Anexo · El informe del revisor, pegado tal cual

Sobre el commit `3027599`, ANTES de arreglar nada (lo que se hizo con cada hallazgo, en el §6).

## Informe del revisor · trabajo/guardias-claude · 2026-10-01

Base: `git merge-base main HEAD` = 41c9ed992fb50b34761488f9893c0cabf8346467. Un solo commit (3027599). `git status --short` vacío. `git rev-parse HEAD^{tree}` = 1008399d648cd01491a8087ead43a1e5319bfa58, el mismo árbol que el SELLO que me diste.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | importa | La guardia deja pasar el salto de los hooks por `core.hooksPath`, que equivale a `--no-verify` (regla «NUNCA --no-verify... los hooks son la puerta»). El informe y CLAUDE.md dicen que se bloquea el salto de hooks, y no es así. | `printf '{"tool_name":"Bash","tool_input":{"command":"git -c core.hooksPath=/dev/null commit -m x"},"cwd":"C:/Users/USER/Desktop/Bot v3"}' \| python .claude/hooks/guardia.py` → exit=0. Lo mismo con `git config core.hooksPath /dev/null` → exit=0. `grep -n "hooksPath" .claude/hooks/guardia.py` → sin resultados. `--no-verify` sí bloquea (exit=2). |
| A2 | importa | `git -C <dir> show HEAD:<ruta relativa>` esquiva el bloqueo del holdout: la ruta se resuelve contra el cwd, no contra `-C`. `-C` está en `GIT_CON_VALOR` (`.claude/hooks/guardia.py:1023`) pero no se aplica a la ruta. Hoy `holdout/{1,2,3}` solo tienen README, así que no hay fuga real, pero es un hueco de la barrera. | `git -C knowledge/cases show HEAD:holdout/1/x` → exit=0. `git -C knowledge/cases/holdout/1 show HEAD:x` → exit=0. `git show HEAD:knowledge/cases/holdout/1/x` → exit=2 (el control sí bloquea). |
| A3 | menor | `docs/HANDOFF.md` no se actualiza aunque el contrato lo permite y CLAUDE.md lo pone como paso 3 de «Por donde se empieza». No lo exige el encargo. | `git diff --stat main...HEAD` no lo lista; `contrato.yaml` lo permite. |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` → `CONTRATO: 19 ficheros dentro del contrato de trabajo/guardias-claude (riesgo medio, artefacto docs/validation/GUARDIAS-CLAUDE.md, 3 comprobaciones para el revisor)`, exit=0. Los tres pytest (`test_contrato_rama`, `test_guardia_claude`, `test_revisor`) pasan: 72+72+71 puntos, todos verdes. `make check` no lo ejecuté; su evidencia es lo que me diste (1670 passed, SELLO sobre el árbol 1008399…, PICO 283 MiB, que coincide con el árbol de HEAD) y GUARDIAS-CLAUDE.md §4. `uv run botsito state check` → OK.
- **Rutas protegidas.** Nada de la rama toca `src/`, `knowledge/`, `config/`, `data/`, `mql5/`, `tools/`, `scripts/git-hooks/`, `docs/adr/` ni `docs/spec/`.
- **Fuente:.** No se toca `knowledge/spec` ni `knowledge/cases`, así que no aplica.
- **Regímenes de cambio.** Todo el diff son ficheros nuevos (A) salvo `.gitignore`, `CLAUDE.md`, `Makefile`, `PROJECT_STATE.md`, `RITUAL.md` y `runbooks/README.md`, que son modificaciones permitidas. No hay evidencia, feedback, manifiestos, transcripciones ni `libros.yaml`.
- **Ambiguedades, ADR, tres guardias de `cita`, informes cerrados.** No aplican: no hay ambigüedades ni ADR nuevos, ni informes cerrados cambiados.
- **Holdout y exposición.** La rama no declara haber leído ningún libro, imagen, fotograma ni transcripción. Las dos sondas que cuenta el informe (§1.6) eran ficheros propios, no material del corpus.
- **Informe de la rama.** Existe y acaba en `## Estado` → «Rama lista para revisión, NO cerrada.».
- **Cifras.** No hay cifras de negocio en el código nuevo.
- **Pruebas del hook.** Bloquea las rutas con `..`, `//` y `./`; `cd x && cat rel`; `cp` del material; `xargs cat`; `python -c` que construye rutas; `unzip -p` sobre un xlsx de septiembre; Read de imagen del material adicional (también con mayúsculas distintas); `git push +HEAD:main`; `--no-verify`. Deja pasar `sha256sum`.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 20 hechos (6 de ellos de otra forma, declarada), 1 parcial, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama `trabajo/guardias-claude` desde main 41c9ed9 | Hecho | merge-base = 41c9ed992fb5… |
| 2 | Fase 0: inventario de reglas de CLAUDE.md, RITUAL y runbooks, con qué las hace cumplir hoy (test, hook, make check, CI, nada), y las «nada» son el alcance | Hecho | GUARDIAS-CLAUDE.md §0, 58 filas en 3 tablas, columna «Esta rama» y cierre de alcance en las líneas 96-98 |
| 3 | Fase 0: «Entrega la tabla antes de escribir código» | Parcial | La tabla está en el informe (§0), pero la rama es un único commit (3027599) y no puedo comprobar que se entregara antes del código. Es el hallazgo B1. |
| 4 | F1: hook PreToolUse en Python, Windows, PYTHONUTF8, sin dependencias nuevas, para Read, Grep, Glob y Bash | Hecho | `.claude/settings.json`: matcher `Read\|Grep\|Glob\|Bash\|PowerShell`, orden `PYTHONUTF8=1 python …guardia.py`. `pyproject.toml` y lockfile sin cambios. |
| 5 | F1: bloquea leer contenido de libros xlsx, imágenes, transcripciones y casos de meses reservados o sin sortear (`casos_reservados`, `casos_ocultos`, marzo) | Hecho | Probado: xlsx de septiembre y carpeta de marzo bloqueados; imagen del material adicional bloqueada; holdout bloqueado. §1.2 y `test_contra_el_repo_real_ve_lo_mismo_que_el_codigo` comparan con `casos_reservados`. |
| 6 | F1: permite solo stat, tamaño, sha256 y `botsito corpus inventory` | Hecho de otra forma (declarada) | §1.3 permite además `ls`, `du`, `wc -c`, `certutil`, `find`, `git ls-files`, `check-ignore`, la CLI del proyecto entera «que es la puerta» y los scripts commiteados. La ampliación se declara y se justifica brevemente. Ver B2. |
| 7 | F1: si no puede decidir un comando Bash, lo BLOQUEA y explica cómo reescribirlo | Hecho | `ls … \| xargs cat` → exit=2, mensaje «Como reescribirlo: rutas LITERALES…» |
| 8 | F1: el mensaje de bloqueo cita la regla de CLAUDE.md | Hecho | Todos los bloqueos de mis pruebas empiezan por «Regla: CLAUDE.md, …» |
| 9 | F1: deniega `--no-verify` en commit y push | Hecho | 24 patrones en `.claude/settings.json`, más el hook (exit=2). Pero ver A1 por `core.hooksPath`. |
| 10 | F1: deniega `push --force` y borrar tags | Hecho | `Bash(git push --force*)`, `Bash(git tag -d *)` y el hook; probado `+HEAD:main` → exit=2 |
| 11 | F1: deniega `git push origin main` sin BOTSITO_ALLOW_MAIN | Hecho de otra forma (declarada) | No se activa: §1.4 dice que bloquearía el ritual (`git push --atomic origin main stable/<tag>` y el push tras CI roja, que van sin la variable) y que una regla `deny` no distingue la variable. Deja la decisión al consultor en §7.1. Coincide con «si algo bloquearía el ritual, dilo y no lo actives». |
| 12 | F1: deniega `rm -rf` sobre data/, corpus/ y knowledge/ | Hecho | Patrones `rm -rf`/`-fr` en deny y el hook (`rm -rf .` también) |
| 13 | F1: `.claude/settings.local.json` en .gitignore y `settings.json` versionado | Hecho | `.gitignore` diff `+/.claude/settings.local.json`; `settings.json` está en el diff |
| 14 | F1: lo que bloquearía make check, la CI o el ritual, dilo y no lo actives | Hecho | §1.4: los hooks de Claude Code no ven `make` ni la CI. `test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual` sobre los 30 comandos reales. |
| 15 | F1: defensa en profundidad, `casos_reservados` y la compuerta no se tocan | Hecho | `src/` sin cambios; CLAUDE.md lo dice en la sección nueva |
| 16 | F2: `contrato.yaml` con rutas_permitidas, rutas_protegidas, comprobaciones, riesgo y artefacto | Hecho | `contrato.yaml`; el cargador estricto exige las claves (`scripts/contrato_rama.py:44,80-99`) |
| 17 | F2: make check compara el diff con el merge-base y falla nombrando cada fichero fuera de permitidas, dentro de protegidas y si falta el artefacto | Hecho | `scripts/contrato_rama.py:154-203`, objetivo `contrato` en el Makefile (diff). Mensajes por fichero. Prueba real contra la rama: `CONTRATO: 19 ficheros dentro del contrato…`. |
| 18 | F2: «En main el contrato se borra en el merge y no se exige» | Hecho de otra forma (declarada) | `scripts/contrato_rama.py:176-177` no lo exige en main. Se borra en un paso previo al merge (RITUAL.md «Antes del merge: el contrato sale de la rama»), no dentro del merge. §2 decisión 2 explica por qué: sellar en main a mitad de merge rompe `state check`. Es un paso nuevo en el ritual, con cambio en RITUAL.md. |
| 19 | F2: plantilla en `docs/runbooks/CONTRATO-DE-RAMA.md` con tres ejemplos (solo knowledge, motor, medición) | Hecho | Fichero con 167 líneas; un test carga los cuatro bloques (§2) |
| 20 | F2: contrato de esta rama como primer ejemplo | Hecho | `contrato.yaml`, reproducido en §2.3 |
| 21 | F3: `.claude/agents/revisor.md` con herramientas de solo lectura (Read, Grep, Glob, Bash sin escritura) | Hecho | frontmatter `tools: Read, Grep, Glob, Bash`; hook `solo_lectura.py` en el frontmatter para Bash |
| 22 | F3: dos ejes independientes con informe cada uno; (a) lista de reglas y (b) encargo en `docs/encargos/<rama>.md` | Hecho | `revisor.md` secciones «Eje (a)» y «Eje (b)»; formato de salida con dos informes |
| 23 | F3: cada hallazgo con evidencia y gravedad bloquea/importa/menor; no arregla nada | Hecho | `revisor.md` secciones «Gravedad» y primera frase |
| 24 | F3: línea nueva en CLAUDE.md, literal | Hecho | CLAUDE.md, «Como se trabaja»: «Antes de declarar una rama lista para revisión: guarda el encargo en docs/encargos/, pasa el revisor y pega su informe al final del informe de la rama.» |
| 25 | F3: métrica en `docs/runbooks/ERRORES-RECURRENTES.md` por rama (revisor / consultor después) | Hecho | Tabla con columnas «Hallazgos del revisor» y «Hallazgos del consultor despues», más «Que se le escapo» |
| 26 | F4: tests del hook (bloquea lectura reservada, deja pasar sha256, bloquea Bash indecidible) | Hecho | `tests/unit/test_guardia_claude.py`, 72 casos pasan; §4 nombra cada uno |
| 27 | F4: tests del contrato (falla con diff fuera, pasa con diff dentro) | Hecho | `tests/unit/test_contrato_rama.py`, 72 casos pasan |
| 28 | F4: test del revisor (existe, frontmatter válido, sin herramientas de escritura) | Hecho | `tests/unit/test_revisor.py`, 71 casos pasan |
| 29 | Encargo guardado en `docs/encargos/trabajo-guardias-claude.md` al empezar | Hecho | Existe, 48 líneas, cabecera «Copiado tal cual… el 2026-10-01». No puedo comprobar que sea byte a byte el prompt original. |
| 30 | Ritual normal con make check sellado, sin --no-verify | Hecho (evidencia indirecta) | El árbol de HEAD = el del SELLO que me diste. No ejecuté `make check`. |
| 31 | Pegar el informe del revisor en el informe de la rama, «lista para revisión, NO cerrada» | Pendiente de quien me llama | GUARDIAS-CLAUDE.md §6 dice «Pendiente: se pega aquí tras pasarlo». Este informe lo devuelvo yo, sin pegarlo (revisor.md, eje b punto 5). El estado final es el que pide el encargo. |
| 32 | Lo que no se toca: motor, spec, knowledge, cifras | Hecho | Diff sin `src/`, `knowledge/`, `config/` ni `docs/spec/` |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | importa | Fase 0 exige entregar la tabla del inventario ANTES de escribir código. La rama es un único commit con inventario, código y tests juntos, y el informe no dice que se entregara antes ni cuándo. No se puede comprobar. | `git log --format='%h %s' main..HEAD` → solo 3027599. GUARDIAS-CLAUDE.md §0 no menciona la entrega previa. |
| B2 | menor | «Permite solo stat, tamaño, sha256 y `botsito corpus inventory`». La rama permite muchas más cosas (CLI entera, `scripts/*.py` commiteados, `find -exec sha256sum`, etc.). Está declarado en §1.3, pero el motivo de dejar pasar la CLI y los scripts commiteados es una sola frase y esos scripts son confianza total (§1.7 lo reconoce). Conviene que el consultor lo apruebe de forma expresa. | `GUARDIAS-CLAUDE.md:153-160` |
| B3 | menor | El encargo y CLAUDE.md piden pegar el informe del revisor «al final del informe de la rama». El §6 está antes del `## Estado`, así que el informe pegado quedaría en medio y no al final. | `GUARDIAS-CLAUDE.md:314-316` frente a `:333-335` |

Cosas hechas fuera del encargo, todas declaradas en el informe: PowerShell en el matcher (§1.1); bloqueos adicionales de `cherry-pick`, `rebase`, `commit -n`, `branch -D`, `make check` sin fichero y heredoc sin comillas con `\` (§0 filas 5, 29, 32, 44; §1.4); `add -A`, `commit -a`, `revert` y `reset --hard` en main (filas 40 y 45); la cuarentena de crudas v7+ (fila 36); `hooks/solo_lectura.py`; `.claude/hooks` en ruff y `mypy --strict` (Makefile); el paso nuevo del ritual (RITUAL.md); la sección «Las guardias de Claude Code» en CLAUDE.md. Con una salvedad: el hook bloquea más cosas que el encargo enumera, y eso es decisión del consultor.

### Lo que no pude comprobar
- **`make check`.** No lo ejecuto (escribe). Me quedo con el dato que me diste y con que el árbol de HEAD coincide con el del SELLO.
- **Hook en vivo dentro de Claude Code.** Solo lo probé invocando `guardia.py` por stdin. Que Claude Code lo cargue, que bloquee con exit 2 y la latencia, no lo verifiqué. Mis pruebas con rutas de Windows con barras invertidas fallaron por el escapado de mi propio shell («el evento no es JSON»), no por el hook, así que esas rutas quedan sin probar.
- **Reglas `deny` de permisos.** No las medí en vivo; el propio informe (§1.6) dice lo mismo.
- **Que el encargo guardado sea copia literal** del prompt original: no tengo el original.
- **Posible cuarto caso del patrón «CLAUDE.md más estricto que el ADR».** El hook trata como no legible todo libro de un mes que no sea enero, abril o agosto, incluido mayo. ADR-0025 §4 permite abrir los 6 días `dev` de mayo, y el hook solo lo evita para la sesión (la ingesta por código sigue funcionando). Es una observación, no una medición. Quien revisa debería confirmar que ninguna tarea prevista necesita leer a mano filas dev de mayo.
- **Informe de exposiciones.** Para saber si hay una fila en `HOLDOUT-EXPOSICIONES.md` he tenido que fiarme de que la rama no abre material. No leí ese fichero.

### Comandos ejecutados
1. `git rev-parse HEAD^{tree}`; `git diff --stat main...HEAD`; `git status --short`
2. `cat contrato.yaml`; `uv run python scripts/contrato_rama.py`; `git log --format='%h %s' main..HEAD`; `git merge-base main HEAD`
3. `uv run pytest tests/unit/test_contrato_rama.py tests/unit/test_guardia_claude.py tests/unit/test_revisor.py -q` (y la misma con `--co` para contar)
4. `cat .claude/settings.json`; `git diff main...HEAD -- .gitignore CLAUDE.md Makefile PROJECT_STATE.md docs/runbooks/…` (varias veces, con salida recortada)
5. `cat -n docs/validation/GUARDIAS-CLAUDE.md`; `cat -n scripts/contrato_rama.py`; `sed -n 255,285p CLAUDE.md`
6. `uv run botsito state check`
7. `ls corpus …` y `ls knowledge/cases/holdout/1` (solo nombres)
8. Unas 26 invocaciones de `printf '<evento JSON>' | python .claude/hooks/guardia.py` con comandos Bash y Read de prueba (holdout, material adicional, `--no-verify`, `core.hooksPath`, `git -C`, push `+`, etc.), todas con rutas inexistentes o de metadatos
9. `grep -n "hooksPath\|core.hooks" .claude/hooks/guardia.py`; `grep -n '"-C"' .claude/hooks/guardia.py`
