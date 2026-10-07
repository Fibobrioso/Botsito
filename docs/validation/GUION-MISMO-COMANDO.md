# La guardia solo ejecuta un guion si lo que se ejecuta es lo que leyó

Rama `trabajo/guion-mismo-comando`, abierta el 2026-10-07 desde `main` en cbfe4e4 (commit de estado
sobre el merge 9a313e0, tag `stable/F37f-umbral-mayo`; CI de `main` sobre
`cbfe4e493cbb3343ed0b8ab2464fec1fdc6beaaf`: run 37652207581, completed/success). Encargo:
`docs/encargos/trabajo-guion-mismo-comando.md`. Es el punto V de la Next Action: el hueco de
`RELOJ-INVIERNO.md` §4.5 en su forma general.

## 0. Fase 0, inventario sin tocar código

Todo lo de esta sección se leyó en `.claude/hooks/guardia.py` tal como está en `main` (cbfe4e4; la
rama no lo ha tocado) y se midió llamando a `decidir()` sobre el texto de cada comando, sin
ejecutar ninguno. El guion de medida y su salida están en
`docs/validation/anexos/GUION-MISMO-COMANDO/` (`medir_huecos.py` y `medir_huecos-SALIDA.txt`).

### 0.a Las vías por las que la guardia decide sobre algo que luego se EJECUTA

| # | Vía | Dónde (líneas de `guardia.py`) | Qué hace hoy | Si el fichero no existe o no se puede leer |
|---|---|---|---|---|
| 1 | Intérprete con guion: `python x.py`, `node`, `perl`, `ruby`, `deno`, `bun`, `Rscript`, `py`, `python3`, también tras `uv run`, `env`, `timeout`, `nice`, `nohup`, `exec`... | `analizar_comando` 1125 → `_analizar_interprete` 1605-1635 → `_exigir_guion` 1638-1662; envoltorios en `_quitar_envoltorios` 1057-1076 | Si el guion es IDÉNTICO al de `main` (`_igual_que_en_main`, 1665-1688: mismo blob en `main` u `origin/main`), es código revisado y solo mira sus argumentos (1649-1653). Si no, lo lee entero con `analizar_codigo` (literales de texto como rutas, 1706-1738) | **Pasa**: `read_text` con `OSError` deja `texto = ""` (1657-1660) y `analizar_codigo("")` no encuentra nada; solo se miran los argumentos. Y la comparación con `main` se hace sobre el disco de ANTES del comando |
| 2 | Shell con guion: `bash x.sh`, `sh`, `zsh`, `dash` | `_analizar_shell` 1584-1602 → `_exigir_guion` | Igual que 1, pero el guion se lee con `analizar_codigo(texto, es_python=False)`: solo los literales ENTRE COMILLAS (`_literales`, 1753), no como bash | **Pasa**, como 1. Además, con el fichero en disco, una ruta SIN comillas dentro del guion no se ve (medido: `v-bash-guion`) |
| 3 | Shell o intérprete con código en línea: `bash -c '...'`, `python -c '...'`, heredoc `python - <<'EOF'`, `bash <<'EOF'` | `_analizar_shell` 1585-1601 (`-c` → `analizar_bash`, heredoc → `analizar_bash`); `_analizar_interprete` 1610-1618 (`-c`) y 1626-1634 (heredoc) | Lee el código, que es lo que se ejecuta. Lo que ese código ejecute a su vez (`runpy.run_path`, `exec(open(...))`, `import` de un módulo local) no se lee | No aplica (no hay fichero), salvo lo que el código importa o ejecuta, que no se lee nunca |
| 4 | Intérprete con el código por la entrada estándar: `python < x.py`, `bash < x.sh` | `analizar_comando` 1088-1089 (la redirección `<` solo mira si el fichero ES protegido) y `_analizar_interprete` 1626-1634 (sin guion ni heredoc, pasa salvo tubería) | **No lee el guion**: pasa aunque exista (medido: `v-stdin`) | Pasa |
| 5 | Intérprete con módulo: `python -m <módulo>` | `_analizar_interprete` 1619-1625 | Solo `-m pytest` va a `_analizar_pytest`. Cualquier otro módulo -uno local del directorio, o de `src/`- **no se resuelve ni se lee**: solo se miran los argumentos | Pasa |
| 6 | pytest: `pytest x`, `uv run pytest x`, `python -m pytest x` | `analizar_comando` 1122-1124 → `_analizar_pytest` 1538-1554 | Lo que está bajo `tests/` es código revisado por diseño: corre con la guarda del holdout (`tests/guarda_holdout.py`), y no se lee (1551). Fuera de `tests/`, un `.py` que existe se lee como un guion (1553-1554) | **Pasa**: solo lee si `os.path.isfile` (1553). Y un DIRECTORIO fuera de `tests/` tampoco se lee (pytest recogería sus `test_*.py`: medido, `b6'`) |
| 7 | make: `make <objetivo>` | `analizar_comando` 1103-1105 → `_analizar_make` 1457-1464 | Solo exige que `make check`/`make regress` lleven la salida a un fichero. **El `Makefile` no se lee ni se compara con `main`**: sus recetas se ejecutan sin mirarlas (medido: `v-make`) | Pasa |
| 8 | PowerShell: la herramienta PowerShell, y `pwsh -c` / `powershell -c` desde Bash | `decidir` 1884 y `analizar_comando` 1128-1132 → `analizar_powershell` 1770-1840 | **No mira el contenido de ningún guion**: `python x.py` cuenta como «lectora» (`PS_LECTORES`, 1757) pero solo se comprueba si la RUTA `x.py` es protegida (1807-1816). Pasa aunque el guion exista y nombre material protegido (medido: `v-ps`, `v-ps-uv`, `v-pwsh-c`) | Pasa |
| 9 | Un programa que es un fichero: `./x.py`, `uv run x.py` (`uv run` se quita y queda `x.py` como programa), `python3.12 x.py` (no está en `INTERPRETES`), `nice -n 5 python x.py` (el envoltorio deja `-n` como programa) | La caída genérica de `analizar_comando`, 1161-1182 | Trata el programa como un lector: mira sus ARGUMENTOS como rutas, y el programa (el guion) no se lee nunca (medido: `v-uv-run`, `v-directo`, `v-version`, `v-nice`) | Pasa |
| 10 | `find ... -exec <prog>` | `_analizar_find` 1481-1510 | Solo mira si las raíces alcanzan material protegido recursivamente. El programa de `-exec` no se analiza: `find docs -exec python a.py \;` pasa (medido: `v-find`) | Pasa |
| 11 | Alias de git con `!`: `git -c alias.x='!cmd' x` | `_analizar_git` 1251-1316 | El valor de `-c` solo se mira para `core.hooksPath`; el alias ejecuta un shell que nadie lee (medido: `v-git-alias`) | Pasa |
| 12 | `xargs <prog>` | `_analizar_xargs` 1467-1478 | Niega todo salvo los lectores de metadatos | Niega |
| 13 | `eval`, `source`, `.` | `analizar_comando` 1106-1109 | Niega | Niega |
| 14 | `cmd /c` | `analizar_comando` 1135-1136 | Niega | Niega |
| 15 | La CLI del proyecto, `botsito ...` | `_analizar_cli` 1513-1535 | Es la puerta (`casos_reservados`, la cuarentena): se deja pasar salvo lo que imprime una cruda o un tramo. El código de `src/` que ejecuta -aunque la rama lo haya cambiado- no se lee | Pasa (por diseño) |
| 16 | Los hooks de git (`git commit` ejecuta `.git/hooks/pre-commit`) | — | Lo que ejecutan lo instala `make hooks` desde `scripts/git-hooks/`; la guardia no lo mira | — |

Y una más que no es una vía sino el hueco general: **todo lo que el mismo comando hace ANTES de la
ejecución** -un `cp`, un `cat >`, un `tee`, un `$(...)`, algo en segundo plano con `&`- no lo
modela nadie. La guardia decide sobre el disco tal como está al inspeccionar, y el comando puede
cambiarlo antes de ejecutar el guion. Es lo que pasó en `RELOJ-INVIERNO.md` §4.5.

### 0.b Los huecos, medidos

`medir_huecos.py` crea, en un directorio temporal fuera del repo, un repositorio SINTÉTICO con la
forma del real: `main` con un commit, la rama `trabajo/prueba`, y un fichero «protegido» de mentira
en `knowledge/cases/holdout/1/secreto.yaml` de ESE repo. El guion malo, `a.py` (nuevo en la rama,
sin seguir), imprime ese fichero. Después llama a `decidir()` con cada comando y el `cwd` del repo
sintético. No ejecuta ninguno.

**Una nota sobre cómo está escrito el guion de medida.** Dentro de `medir_huecos.py`, la ruta del
fichero de mentira se compone con `Path(...).joinpath("knowledge", "cases", "holdout", "1", ...)`
en vez de escribirla como un literal relativo. La razón: al lanzar `python medir_huecos.py`, la
guardia lee el guion (es nuevo) y resuelve cada literal contra el directorio desde el que se lanza;
un literal `knowledge/cases/holdout/1/secreto.yaml` se leería como el holdout REAL y bloquearía la
medida por un fichero que no se abre. Dentro del guion malo la ruta va ABSOLUTA, la del repo
sintético, y por eso la guardia sí la ve (control).

Primero el control: **`uv run python a.py` con `a.py` en disco → NIEGA** («el codigo nombra
.../holdout/1/secreto.yaml»). Si la guardia lee el guion, lo para. Lo que sigue mide si lo lee.

| Caso | Comando | Hoy |
|---|---|---|
| control | `uv run python a.py` | NIEGA |
| b1 | `cp a.py b.py && uv run python b.py` (b.py no existe al inspeccionar) | **PASA** |
| b1' | `cp a.py existente.py && uv run python existente.py` (existente.py es inocuo al inspeccionar) | **PASA** |
| b2 | `cp a.py scripts/de_main.py && uv run python scripts/de_main.py` (idéntico al de `main` al inspeccionar) | **PASA** |
| b3 | `cat > x.py <<'EOF'` … `EOF` y en otra línea `python x.py` | **PASA** |
| b3' | `cat > x.py <<'EOF' && python x.py` … `EOF` | **PASA** |
| b4 | `python x.py $(cp a.py x.py)` | NIEGA, pero por casualidad: el argumento `$(...)` es dinámico y el intérprete «lee» sus argumentos |
| b4' | `echo $(cp a.py x.py); python x.py` | **PASA** |
| b4'' | `X=$(cp a.py x.py) python x.py` | **PASA** |
| b5 | `cp a.py x.py & python x.py` | **PASA** |
| b5' | `cat a.py \| tee x.py && python x.py` | **PASA** |
| b5'' | `cat a.py \| tee x.py \| python x.py` | **PASA** |
| b6 | `cp a.py otros/test_nuevo.py && uv run pytest otros/test_nuevo.py` | **PASA** |
| b6-control | `uv run pytest suelto/test_malo.py` (existe) | NIEGA |
| b6' | `uv run pytest suelto` (directorio con `test_malo.py` dentro) | **PASA** |
| tests | `cp a.py tests/unit/test_nuevo.py && uv run pytest tests/unit/test_nuevo.py` | **PASA** (por diseño: `tests/` no se lee) |
| tests' | `uv run pytest tests/unit/test_malo.py` (nuevo en la rama, malo) | **PASA** (por diseño) |
| vía 9 | `uv run a.py` · `./a.py` · `python3.12 a.py` · `nice -n 5 python a.py` | **PASA** las cuatro |
| vía 4 | `python < a.py` | **PASA** |
| vía 5 | `python -m a` | **PASA** |
| vía 3 | `python -c "import runpy; runpy.run_path('a.py')"` | **PASA** |
| vía 2 | `bash malo.sh` (la ruta, sin comillas) | **PASA** |
| vía 2, control | `bash malo_entre_comillas.sh` | NIEGA |
| vía 10 | `find docs -exec python a.py \;` | **PASA** |
| vía 7 | `make x` (el `Makefile` de la rama ejecuta `python a.py`) | **PASA** |
| vía 11 | `git -c alias.x='!python a.py' x` | **PASA** |
| vía 8 | `pwsh -c "python a.py"` (Bash) · `python a.py` y `uv run python a.py` (herramienta PowerShell) | **PASA** las tres |

**De los seis casos del encargo, solo b4 se niega, y por casualidad; sus variantes b4' y b4''
pasan.** De las demás vías, todas pasan menos los controles. Salida literal en
`medir_huecos-SALIDA.txt`.

### 0.c Lo que la regla no puede cubrir, y propuesta para cada uno

| Límite | ¿En esta rama? |
|---|---|
| **Un proceso en segundo plano lanzado en una llamada ANTERIOR** que escribe el guion después de la inspección (o una ejecución en segundo plano de Claude Code que sigue viva). La guardia ve una sola llamada y el disco de ese instante. | No cabe: se declara como límite. Ninguna regla dentro de un comando lo ve. |
| **Lo que el guion importa o ejecuta a su vez**: un `import` de un módulo local, `runpy`, `exec(open(...))`, `subprocess` con otro guion; igual para el código en línea (`-c`, heredoc). La guardia lee el guion, no su grafo de dependencias. | Propongo **entrada nueva de la Next Action**: leer los módulos locales importados (los que resuelven a un fichero del repo o del directorio del guion) es un análisis distinto, con sus propios falsos positivos. En esta rama solo se niega lo que se puede decidir por la forma del comando. |
| **El código de `src/` que ejecuta la CLI** (`uv run botsito ...`, `python -c "from botsito ..."`), aunque la rama lo haya cambiado. La CLI es la puerta por diseño (`casos_reservados`, la cuarentena). | Lo cambiado en una llamada anterior queda como límite (igual que hoy). Lo cambiado EN EL MISMO COMANDO sí entra: propongo contar `botsito` como ejecución para la lista cerrada (d), así `cp x src/... && uv run botsito ...` se niega. |
| **`tests/`**: corre sin leerse por diseño, con la guarda del holdout como barrera. | Se mantiene la exención para lo que ya está en disco. Lo creado en el mismo comando cae por la lista cerrada (un `cp` antes no está en ella), sin tocar la exención. |
| **Los hooks de git** (`git commit` ejecuta lo que `make hooks` instaló). | Límite declarado: lo protegen el hook mismo y `make hooks`; no es una vía de esta rama. |
| **Un guion de shell se lee por sus literales entre comillas, no como bash** (vía 2, medido). | Propongo que **sí entre en esta rama**: es la misma vía y la misma condición (la guardia tiene que poder decidir sobre lo que se ejecuta). El guion `.sh`/`bash` se analiza con `analizar_bash`, como un `bash -c`. |
| **PowerShell** no tiene un análisis de comandos como el de Bash (vía 8). | Propongo **negar en PowerShell toda ejecución de un intérprete, shell, pytest o make sobre un guion** (la lista cerrada en PowerShell queda vacía), con el mensaje «usa la herramienta Bash». Ningún runbook ni skill nombra PowerShell (`grep -rli powershell docs/runbooks/ .claude/skills/`: nada), y los 32 comandos que comprueba `test_el_ritual_y_los_runbooks_pasan` son de Bash. |
| **`make`** con un `Makefile` cambiado en la rama (vía 7). | Decisión tuya (ver d). |

### 0.d La lista cerrada: propuesta

**Qué es «una ejecución»** (lo que activa la condición), cerrado: un intérprete o un shell con
guion, con `-c`, con heredoc, con `-m` o por la entrada estándar; `pytest` (también `-m pytest`);
`make`; `botsito`; un programa que es un fichero (`./x`, `uv run x.py`); `find -exec` de algo que no
sea un lector de metadatos; un alias de git con `!`. Lo que no se pueda clasificar con seguridad
como «no ejecuta código» no se presume: un programa desconocido sigue siendo un lector (hoy) y no una
ejecución, porque es del entorno y no de la rama; lo de la rama son FICHEROS, y un fichero como
programa es ejecución (vía 9).

**La condición, una sola función** (nombre propuesto: `exigir_ejecucion_verificable`), llamada
desde todas esas vías. Una ejecución pasa solo si se cumplen TODAS:

1. El intérprete se reconoce: `python`, `python3`, `pythonX.Y` (patrón), `py` y los de
   `INTERPRETES`; los envoltorios se quitan con sus opciones (`nice -n N`, `timeout -s X N`,
   `stdbuf -oL`...). Si no se reconoce, se niega.
2. El guion, si lo hay, es UNA ruta literal (hoy ya) y **existe y se puede leer al inspeccionar**.
   Si no existe o no se puede leer, se niega con el mensaje del encargo: «escribe el guion con la
   herramienta Write y ejecútalo en otra llamada».
3. El guion se lee: si es idéntico al de `main`, código revisado (como hoy); si no, se analiza
   entero: `.py` con `analizar_codigo`, un shell con `analizar_bash`. El `-m` de un módulo que no
   sea `pytest` se niega (no se resuelve qué fichero ejecuta). La entrada estándar (`< x`) se lee
   como un guion.
4. **Lo que va antes en el mismo comando** (todo comando anterior en la misma llamada, separado por
   `;`, `&&`, `||`, `&`, salto de línea, o la parte anterior de una tubería) está en esta lista
   cerrada, y nada más: `cd`; asignaciones con valor literal (`X=valor`, también las que preceden
   al propio comando: `PYTHONUTF8=1 python x.py`); `export X=valor` literal; `set -e`, `set -u`,
   `set -o pipefail` (y sus combinaciones `set -eu`, `set -euo pipefail`).
5. **Lo que va después en la misma tubería** son solo filtros que leen de la entrada estándar sin
   redirección de salida a fichero: `head`, `tail`, `grep`, `wc`, `sort`, `uniq`, `cut`. (`tee`
   no: escribe un fichero.)
6. En el comando entero no hay ninguna sustitución `$(…)` ni `` `…` ``, ni ninguna redirección de
   salida hacia el propio guion (ni hacia ningún fichero que la ejecución lea como código).
7. En PowerShell, la lista de lo admitido está vacía: toda ejecución se niega (0.c).

Lo que va DESPUÉS de la ejecución en otro comando (`; echo exit=$?`, `&& grep ...`) no cambia lo
ejecutado y no entra en la condición; si es otra ejecución, se juzga ella misma con la regla, y
entonces la primera está antes que ella y no está en la lista: **`python a.py && python b.py` se
niega** (`a.py` podría escribir `b.py`). Se hace en dos llamadas.

**Añadidos que propongo a tu punto de partida**, cada uno con su porqué y el comando real:

| Añadido | Porqué | Comando real que lo necesita |
|---|---|---|
| Las asignaciones que PRECEDEN al propio comando (`PYTHONUTF8=1 python x.py`) | Son parte de la ejecución, no algo que va antes; sin esto, el patrón de esta máquina en cp1252 se niega | En esta misma sesión: `cd ".../scratchpad" && PYTHONUTF8=1 python medir_huecos.py ".../guardia.py"`. Y el ritual: `BOTSITO_ALLOW_MAIN=1 git commit ...` (no es una ejecución, pero el mismo patrón) |
| `set -eu`, `set -euo pipefail` (combinaciones de tus tres) | Es la misma opción escrita junta | Forma habitual en bash; ningún runbook la usa hoy: si prefieres no admitir las combinaciones, se quita |
| Contar `botsito` como ejecución | Ejecuta el código de `src/` de la rama; un `cp` o `sed -i` antes en el mismo comando lo cambiaría (0.c) | `uv run botsito knowledge validate > knowledge-validate.log 2>&1` y los demás del ritual pasan igual: no llevan nada antes |

Y dos cosas que **no** propongo añadir, aunque hoy se usan, porque se pueden partir en dos llamadas:
`uv run botsito ...; uv run python scripts/contrato_rama.py` (una ejecución antes de otra) y
`python x.py 2>&1 | tee salida.txt` (`tee` escribe; se usa `> salida.txt 2>&1`).

**Comparación con lo que ya pasa:** los 32 comandos de `RITUAL` en `tests/unit/test_guardia_claude.py`
(el ritual y los runbooks, contra el repo real) no llevan nada antes de su ejecución, así que con la
lista propuesta pasan todos. Se comprobará en la fase 1 con el test que ya existe.

### PARADA

Antes de escribir código necesito tu respuesta a:

1. **La lista cerrada de 0.d**, con los tres añadidos (asignaciones que preceden al comando,
   combinaciones de `set`, `botsito` como ejecución) o sin alguno.
2. **Las vías que propongo meter en esta rama** además de la condición del mismo comando: el guion
   de shell leído como bash (vía 2), la entrada estándar leída como guion (vía 4), `-m` negado salvo
   `pytest` (vía 5), un fichero como programa y los intérpretes con versión (vía 9), `find -exec`
   (vía 10), el alias de git con `!` (vía 11) y PowerShell sin ejecuciones (vía 8). ¿Todas, o
   alguna queda como entrada de la Next Action?
3. **`make` con un `Makefile` distinto del de `main`** (vía 7). Opciones: (a) se niega `make` si el
   `Makefile` difiere de `main`, y lo ejecuta Aleks con `!`; (b) se leen las recetas del objetivo
   pedido con `analizar_bash` (variables de make sin resolver: más falsos positivos); (c) queda como
   límite declarado. Medido: de las ramas fusionadas en `main`, 10 tocaron el `Makefile`
   (`git log --first-parent main -- Makefile`), la última `trabajo/guardias-claude` el 2026-10-01, y
   tres desde el 2026-09-25. Con (a), en una rama así la sesión no puede correr `make check` y el
   sello lo pone Aleks con `!`: es el coste. Mi recomendación sigue siendo (a), porque es la misma
   regla que ya rige los guiones («solo el de `main` es código revisado») y (b) daría un análisis
   peor que el que tiene hoy un guion.
4. **Lo que importa el guion** (0.c): ¿entrada nueva de la Next Action, como propongo?

### 0.e Comandos de la fase 0 y sus salidas

| Comando | Salida |
|---|---|
| `git rev-parse main origin/main`; `git rev-parse "stable/F37f-umbral-mayo^{commit}"` | `cbfe4e493cbb3343ed0b8ab2464fec1fdc6beaaf` las dos; `9a313e0ad5d09cac0af613b6d477cb6be96c82d1` |
| `curl -s --ssl-no-revoke https://api.github.com/repos/Fibobrioso/Botsito/commits/cbfe4e493cbb3343ed0b8ab2464fec1fdc6beaaf/check-runs` | run 37652207581, `"status": "completed"`, `"conclusion": "success"` |
| `make check > make-check.log 2>&1` (commit de apertura `55b4a37`) | `2132 passed`; `SELLO: make check en verde sobre el arbol a9fe90eb…`; `exit=0` |
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/medir_huecos.py .claude/hooks/guardia.py` | 32 casos: 28 `PASA`, 4 `NIEGA` (los tres controles y b4); literal en `medir_huecos-SALIDA.txt`. Con la versión del guion de la fase 0 (commit `29bf2c1`): en la fase 1 se amplió y compara dos guardias (§1.4) |
| conteo por `ast` de `RITUAL` en `tests/unit/test_guardia_claude.py` | 32 comandos |
| `grep -rli powershell docs/runbooks/ .claude/skills/` | nada |
| `git log --first-parent main -- Makefile` | 10 merges; el último, 00ce911 (2026-10-01, guardias de Claude Code) |

**Una medida corregida durante la fase 0.** La primera pasada de `medir_huecos.py` dio `PASA` en el
control: el guion malo estaba COMMITEADO en el `main` del repo sintético, así que la guardia lo
trataba, con razón, como código revisado (vía 1). Se corrigió creando el guion malo después del
commit, sin seguir, como un guion nuevo de una rama; desde entonces el control da `NIEGA`. Las
cifras de arriba son de esa versión. No es un fallo de la guardia: es la regla de «solo el de
`main` es código revisado» funcionando.

**No se ejecutó `botsito motor arnes`** en esta rama, de ninguna forma, ni se abrió material
protegido: los comandos medidos solo se pasaron a `decidir()`, sobre un repo sintético en un
directorio temporal.

### Respuesta del consultor a la fase 0

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/guion-mismo-comando (2026-10-07). Cópiala tal cual en el informe, bajo §0, como «Respuesta del consultor a la fase 0».
>
> 1. Lista cerrada de 0.d: ACEPTADA con los tres añadidos. Las asignaciones que preceden al comando, solo con valor literal: X=$(…) o X=$Y no entran. Las combinaciones de set -e, -u y -o pipefail. Y botsito cuenta como ejecución. Lo aceptado incluye que python a.py && python b.py se niegue y se haga en dos llamadas. Porqué: es la condición nombrada que niega por defecto; los añadidos son la misma ejecución o la misma opción, no casos nuevos.
>
> 2. Vías: entran TODAS en esta rama, llamando a la misma función exigir_ejecucion_verificable. Son: el guion de shell leído con analizar_bash (2), la entrada estándar leída como guion (4), -m negado salvo pytest (5), el fichero como programa y los intérpretes con versión por patrón (9), find -exec de lo que no sea un lector de metadatos (10), el alias de git con ! (11) y PowerShell sin ninguna ejecución (8). Porqué: todas son la misma condición, «la guardia tiene que poder decidir sobre lo que se ejecuta», y dejarlas fuera sería enumerar.
>
> 3. make: opción (a). Si el Makefile difiere del de main, make se niega con un mensaje que diga que lo lanza Aleks con «!». Porqué: es la regla que ya rige los guiones («solo el de main es código revisado»). Declara además como límite que un make con el Makefile de main ejecuta código de la rama (src/, tests/, scripts/), igual que la CLI y la suite.
>
> 4. Lo que el guion importa o ejecuta a su vez (import local, runpy, exec, subprocess): entrada nueva de la Next Action, que entra en el commit del contrato del cierre. Su texto, tal cual: «La guardia lee el guion pero no lo que importa o ejecuta a su vez (import de un módulo local, runpy, exec, subprocess con otro guion), ni en un guion ni en el código en línea (GUION-MISMO-COMANDO.md §0.c). Rama propia: decidir qué módulos se resuelven y se leen, negando por defecto lo que no se pueda resolver.»
>
> 5. Hallazgo del consultor, que el informe no recoge: medir_huecos.py compone la ruta del fichero sintético con Path(...).joinpath("knowledge", "cases", "holdout", …), y la guardia no lo ve. analizar_codigo solo mira literales enteros, y a lo compuesto solo lo niega si además el código recorre directorios (CODIGO_QUE_RECORRE). Es decir, un guion nuevo puede leer el holdout real componiendo la ruta por partes (joinpath, os.path.join, el operador /, f-strings, concatenación). No fue rodear la guardia: el fichero era sintético y lo declaraste. Pero es un hueco de la puerta de lectura, distinto del de esta rama.
>    - En esta rama, solo medirlo: añade a medir_huecos.py los casos de joinpath, os.path.join, el operador / y un f-string sobre el fichero sintético, y escribe en el informe cuáles pasan hoy. No lo arregles aquí.
>    - Entrada nueva de la Next Action, en el mismo commit del contrato del cierre, tal cual: «La guardia no ve una ruta protegida compuesta por partes dentro de un guion (joinpath, os.path.join, el operador /, f-strings, concatenación): analizar_codigo solo mira literales enteros y niega lo compuesto solo si el código además recorre directorios (GUION-MISMO-COMANDO.md, hallazgo 5 del consultor). Rama propia: negar por defecto un guion que nombra un fragmento sensible y compone rutas, con un test que lo rompa a propósito.»
>    - Fila para ERRORES-RECURRENTES en el cierre: (importa, consultor; ni la sesión ni el revisor lo habrían visto, porque el medio de la medida era el hueco) un guion de medida que tuvo que componer una ruta para no chocar con la guardia mostraba otro hueco. Lección: cuando una medida tiene que esquivar una guardia para poder correr, ese esquive se mide como hueco antes de seguir.
>
> FASE 1, como dice el encargo, con lo decidido aquí:
> - Una sola función, exigir_ejecucion_verificable, llamada desde todas las vías de 0.a. Ninguna vía se arregla con código propio.
> - Tests que rompen la guardia a propósito: uno por cada caso de 0.b (b1 a b6 y sus variantes, y las vías 2, 4, 5, 7, 8, 9, 10 y 11). Uno por cada elemento de la lista cerrada que pasa. Uno con un programa inventado antes de la ejecución, que se niega. Uno de make con un Makefile distinto del de main, que se niega.
> - El anexo de mutaciones demuestra que esos tests fallan si se quita la condición.
> - Los 32 comandos de RITUAL en tests/unit/test_guardia_claude.py siguen pasando. Compara caso a caso con la guardia de main: ningún caso que hoy se niega pasa a pasar.
> - Vuelve a correr medir_huecos.py contra la guardia nueva y guarda la salida junto a la de la fase 0. Todos los casos del encargo deben salir NIEGA, salvo los del hallazgo 5, que siguen como están y se dice así.
> - CI de Linux: push de fix/trabajo-guion-mismo-comando y número de run.
> - Informe completo (encargo frente a lo hecho, desviaciones, comandos y salidas, límites, comparación con main) y revisor, con su informe pegado al final. Pídele expresamente que compruebe que la condición niega por defecto y que ninguna vía tiene código propio.
>
> Rama lista para revisión, NO cerrada.

## 1. Fase 1 · La condición, en una sola función

### 1.1 La función y las vías

**`exigir_ejecucion_verificable`** (`.claude/hooks/guardia.py`, definida tras `_exigir_guion_legible`;
`R_EJECUCION` es su regla) es la ÚNICA que decide si una ejecución pasa. Niega por defecto, en este
orden:

1. En PowerShell, toda ejecución: su lista cerrada está vacía (respuesta, punto 2).
2. Lo que la vía no sabe decidir (`indecidible`): un `-m` que no es `pytest`, una opción de `make`,
   un lanzador que la guardia no conoce, una opción de `uv run` que no conoce...
3. El comando (`_exigir_comando_verificable`): ninguna sustitución (`$(...)`, acentos graves,
   `<(...)`) en el comando, ni la ejecución dentro de una; las asignaciones que la preceden,
   literales; todo lo que va ANTES en el mismo comando, en la lista cerrada (`_es_preparacion`:
   `cd`, asignaciones literales, `export X=valor` literal, `set -e`/`-u`/`-o pipefail` y sus
   combinaciones, sin redirecciones); todo lo que va DETRÁS en su tubería, un filtro
   (`_es_filtro`: `head`, `tail`, `grep`, `wc`, `sort`, `uniq`, `cut`, sin redirigir su salida, sin
   `sort -o` ni el fichero de salida de `uniq`); si el comando lanza algo en segundo plano (`&`),
   todo lo demás corre a la vez y tiene que estar también en la lista; y la ejecución no redirige
   su salida a su propio guion.
4. Cada guion (`_exigir_guion_legible`): una ruta literal; ni protegido, ni un directorio; que
   EXISTA al inspeccionar («no existe al inspeccionar el comando», con «el guion, con la
   herramienta Write, y su ejecución en OTRA llamada»); si es el de `main`, código revisado; si no:
   un `Makefile` se niega («lo lanza Aleks en su terminal con «!»»), un guion de PowerShell o de
   lenguaje desconocido se niega, y uno de Python, de shell o de otro intérprete se lee entero.
5. El código en línea (`-c`, heredoc) se analiza: Python y los intérpretes con `analizar_codigo`,
   el shell con `analizar_bash` (como un `bash -c`), PowerShell con `analizar_powershell`.

**Quién la llama.** Todas las vías del inventario (§0.a), ninguna con decisión propia:

| Vía (§0.a) | Cómo llega a la función |
|---|---|
| 1 intérprete con guion | `_analizar_interprete` → `_exigir_guion` |
| 2 shell con guion | `_analizar_shell` → `_exigir_guion`; el guion se lee con `analizar_bash` |
| 3 código en línea y heredoc | `_analizar_interprete` y `_analizar_shell` (`-c`), `_sin_guion` (heredoc) |
| 4 la entrada estándar | `_sin_guion`: `< x` es el guion |
| 5 `-m` | `_analizar_interprete`: `-m pytest` → `_analizar_pytest`; otro, `indecidible` |
| 6 pytest | `_analizar_pytest`: lo de `tests/` sigue sin leerse; lo de fuera, guion; un directorio fuera de `tests/` se niega |
| 7 make | `_analizar_make`: el `Makefile` (con la grafía real de GNU make) es el guion |
| 8 PowerShell | `analizar_powershell` (`_ejecucion_en_powershell` encuentra la ejecución) y `_analizar_pwsh` desde Bash |
| 9 un fichero como programa, intérpretes con versión, envoltorios | `analizar_comando` → `_exigir_guion` (el lenguaje, por la extensión o el `#!`); `_es_interprete` reconoce `pythonX.Y`; `_quitar_envoltorios` quita las opciones de `nice`, `timeout`, `stdbuf`, `exec`, `env` y `uv run`, y lo que no sabe quitar lo pasa como `indecidible` |
| 10 `find -exec` | `_analizar_find` → `_ejecucion_lanzada`: lo lanzado se analiza como un comando que corre a la vez que `find`, que va delante |
| 11 alias de git con `!` | `_analizar_git` → `_ejecucion_lanzada` con `sh -c <alias>`, con `git` delante |
| 12 `xargs` | `_analizar_xargs`: lo que no es un lector de metadatos, `indecidible` (revisor, A1) |
| 13 `eval`, `source`, `.` | `analizar_comando`: `indecidible` (revisor, A1) |
| 14 `cmd /c` | `analizar_comando`: `indecidible` (revisor, A1) |
| 15 `botsito` | `analizar_comando`, antes de `_analizar_cli` |
| 16 los hooks de git | no es una vía de esta rama: límite (§1.6) |

Un test lo comprueba leyendo el código con `ast`
(`test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta`): cada vía llama a la función
o a sus dos puertas (`_exigir_guion`, `_sin_guion`), `find` y `git` pasan por `_ejecucion_lanzada`,
y `R_EJECUCION` solo la escriben `exigir_ejecucion_verificable` y `_niega`. Desde el revisor
(A1), además: ninguna de las vías de ejecución tiene un `raise` propio; `_envoltorios` y
`_opciones_cerradas` solo lanzan `IndecidibleError` (lo decide la función); y en
`analizar_comando` el único `raise` que queda es el de un lector recursivo sin ruta, que es una
regla de lectura.

### 1.2 Un hueco más, encontrado al implementar: el heredoc perdía su primera línea

El primer test que falló no era de la regla nueva: `cat > f.py <<'EOF'` + salto + cuerpo. Medido: en
`tokenizar`, el delimitador de un heredoc suele ser la última palabra de la línea, y al llegar al
salto todavía no estaba cerrado. Sin cerrarlo, **el cuerpo se tokenizaba como comandos de bash y su
primera línea se perdía del `cuerpo`**. En `main`, `python - <<'EOF'` con la ruta protegida en la
primera línea PASA (`f1-heredoc` en la comparación de §1.4). Es de la misma familia («lo que se
ejecuta es lo que se leyó») y la regla nueva lo necesitaba, así que se arregla aquí: el salto cierra
la palabra abierta si hay un heredoc esperando su delimitador. Ningún test existente cambia.

### 1.3 Los tests (`tests/unit/test_guardia_claude.py`, sobre el repositorio sintético)

Ocho funciones nuevas (103 casos tras el revisor; 81 antes), todas `test_ejecucion_*`:

| Test | Casos | Qué rompe |
|---|---|---|
| `…cambiada_en_el_mismo_comando_se_niega` | 20 | b1, b1', b2, b3, b3', b4, b4', b4'', b5, b5', b5'', b6, `tests/` creado en el mismo comando, `<(...)`, una copia en segundo plano a la vez, la salida a su propio guion, algo por la tubería antes; y (revisor, B1) `uv -q run`, `uv --no-cache run` y `/usr/bin/env` tras un `cp` |
| `…cada_via_pasa_por_la_condicion` | 27 | vías 2, 4, 5, 6 (directorio), 7, 8 (Bash y PowerShell, `&`), 9 (`./a.py`, `uv run a.py`, `python3.12`, `nice -n`, `timeout -s`, `winpty`), 10, 11 y el heredoc entero; y (revisor) `/usr/bin/env`, `uv --directory . run`, `uv tool run`, `uvx`, `{python,a.py}`, las vías 12-14 (`xargs python`, `eval`, `cmd /c`) y `git --config-env` |
| `…lo_de_la_lista_cerrada_pasa` | 26 | cada elemento de la lista: `cd`, asignación literal suelta y delante del comando, `export`, `set -e`, `-u`, `-o pipefail`, `-euo pipefail`, cada filtro, lo de después en otro comando, `-X utf8`, `uv run --with`, `--version`, un `grep python`, `command -v python`, `pytest -p no:cacheprovider`, `uv -q run`, `timeout 60`, `uv --version` |
| `…lo_de_fuera_de_la_lista_se_niega` | 26 | un programa inventado antes, un lector antes, dos ejecuciones, asignaciones y `export` no literales, `set -x`, una redirección antes, `tee`, `sort -o`, `uniq` con fichero, un filtro inventado, `python` solo, `-m json.tool`, `env -S`, una opción inventada de `uv run`, `pytest -p mi_plugin`, `pytest` sin rutas fuera de la raíz, un guion que no existe; y (revisor) `cd` a secas, `cd -`, `pytest -o addopts=…`, `pytest -c`, `pytest -n $X`, `timeout -n`, `timeout $X` |
| `…un_guion_que_no_existe_dice_como_reescribirlo` | 1 | el mensaje: «no existe», «Write», «OTRA llamada» |
| `…make_solo_con_el_makefile_de_main` | 1 | con el de `main` pasa; cambiado, se niega y nombra a Aleks; `make -f` se niega |
| `…powershell_sin_ejecuciones_y_lo_demas_igual` | 1 | `Start-Process`, `.\x.ps1`, `make` se niegan; `git status`, `Get-Content`, `Write-Output` pasan |
| `…una_sola_funcion_y_ninguna_via_decide_por_su_cuenta` | 1 | el `ast` de §1.1, con los `raise` (revisor, A1) |

**Que fallan si se quita la condición, y que fallan los que tienen que fallar**
(`anexos/GUION-MISMO-COMANDO/sin_condicion.py`, salida en `sin_condicion-SALIDA.txt`). Carga la
guardia como el módulo que usan los tests, cambia una pieza EN MEMORIA y corre los 103 casos en el
mismo proceso. Desde el revisor (A7), la condición está partida en piezas con nombre
(`_exigir_sin_expansiones`, `_exigir_lo_de_antes`, `_exigir_lo_de_a_la_vez`, `_exigir_salida_ajena`
y, aparte, `_exigir_guion_legible`), cada una con su mutación, y el veredicto ya no se conforma con
«que falle algo»:

| Mutación | Fallan | Lo que se exige |
|---|---|---|
| ninguna | 0 de 103 | — |
| «sin la condición» (`exigir_ejecucion_verificable` no hace nada) | 76 de 103 | **exactamente** los 76 que esperan una negación (de seis tests), ni uno más ni uno menos: sí |
| «sin las expansiones» | 3 | los 3 que solo niega esa pieza (`<(...)`, `X=$Y`, `X=$(...)`): fallan 3 |
| «sin lo de antes» | 12 | los 6 que solo niega esa pieza: fallan 6 |
| «sin lo de a la vez» | 5 | los 5 (`&`, `tee`, `sort -o`, `uniq` con fichero, un filtro inventado): fallan 5 |
| «sin la salida ajena» | 1 | el 1 (`> existente.py`): falla |
| «sin la existencia» (un guion que no existe se lee como vacío, como en `main`) | 2 | los 2: fallan 2 |

Restaurada cada mutación, fallan 0. `VEREDICTO: sin la condicion fallan exactamente los que esperan
una negacion; cada pieza rompe los suyos; restaurada, todo pasa`.

**La guardia de antes, intacta:** los 236 casos que ya existían pasan (339 en total con los nuevos), entre ellos los 32 de `RITUAL`
contra el repo real (`test_el_ritual_y_los_runbooks_pasan`). Un cambio en el fixture, declarado en
§1.7: el repo sintético lleva ahora un `Makefile` commiteado en su `main`.

### 1.4 La comparación caso a caso con `main` (`medir_huecos-FASE1-SALIDA.txt`)

`medir_huecos.py` admite ahora dos guardias y las compara: la de `main` (`git show
main:.claude/hooks/guardia.py`, en la carpeta de trabajo) y la de la rama, sobre los mismos 58 casos
del repo sintético (46 en la primera pasada, más 12 del revisor). **Casos que `main` niega y la rama
deja pasar: 0.** 39 pasan de PASA a NIEGA, y 19 no cambian:

| Caso | `main` | rama | Por qué |
|---|---|---|---|
| b1, b1', b2, b3, b3', b4', b4'', b5, b5', b5'', b6, b6', `tests-cp` (13) | PASA | **NIEGA** | lo de antes, la sustitución, el directorio o la existencia |
| vías 2, 4, 5, 7, 8 (3), 9 (4), 10, 11 (13) | PASA | **NIEGA** | la condición |
| `f1-heredoc`, `f1-proceso`, `f1-winpty`, `f1-uv-opcion`, `f1-a-si-mismo`, `f1-dos` | PASA | **NIEGA** | el heredoc entero (§1.2), `<(...)`, el lanzador, la opción de `uv run`, la salida al guion, dos ejecuciones |
| `control`, `b6-control`, `v-bash-control` | NIEGA | NIEGA | el guion se lee y nombra lo protegido |
| b4 (`python x.py $(cp a.py x.py)`) | NIEGA, por casualidad (el argumento es dinámico) | NIEGA, por la sustitución | |
| `inocuo`, `f1-admitido` (`cd . && PYTHONUTF8=1 python inocuo.py \| tail -3`) | PASA | PASA | lo admitido |
| `tests-nuevo` (un test nuevo y malo ya en disco, en `tests/`) | PASA | PASA | **por diseño**: `tests/` no se lee, corre con la guarda del holdout (§1.6) |
| `v-runpy` (`python -c "import runpy; runpy.run_path('a.py')"`) | PASA | PASA | **límite**: lo que el código ejecuta a su vez (respuesta, punto 4; entrada nueva de la Next Action) |
| `h5-*` (6) | 5 PASA, 1 NIEGA | igual | **hallazgo 5, solo medido** (§1.5) |
| `rv-uv-global`, `rv-env-ruta`, `rv-llaves`, `rv-uvx`, `rv-cd-solo`, `rv-pytest-o`, `rv-config-env` (7) | PASA | **NIEGA** | los arreglos del revisor (B1, B3, B4) |
| `rv-php`, `rv-setsid`, `rv-trap`, `rv-awk`, `rv-ps-proceso` (5) | PASA | PASA | **B2 del revisor: decisión del consultor** (§1.12) |

**Todos los casos del encargo salen NIEGA**, salvo los del hallazgo 5. Los dos que siguen pasando y
no son del hallazgo 5 (`tests-nuevo`, `v-runpy`) no son casos del encargo: son el diseño de `tests/`
y el límite del punto 4 de la respuesta.

**Y sobre comandos reales** (`comandos_reales.py`, salida en `comandos_reales-SALIDA.txt`): las dos
guardias sobre los 502 comandos de Bash distintos de la transcripción de esta sesión (la sesión
creció desde la primera pasada, con 444), contra el repo real. 398 con la misma decisión; **0 que
`main` niega y la rama deja pasar**; **104 que `main` deja pasar y la rama niega**. El desglose lo
calcula el guion sobre el motivo ENTERO (revisor, A5: la primera versión lo hacía sobre el motivo
recortado y la suma no cuadraba): 99 llevan algo delante que no está en la lista cerrada (el primer
programa de delante: `python` 34, `cat` 19, `git` 12, `uv` 12, `grep` 9, `sed` 6, `rm` 2, una
asignación seguida de otra ejecución 2, `sha256sum` 1, `printf` 1, `cp` 1); 2 son `pytest` sin rutas
en un `git worktree` (§1.6); 2 llevan algo detrás que no es un filtro (`tee`); 1 lleva una
sustitución. De los 104, 7 nombran el material adicional o un backtest y no se imprimen. Ninguno es
un fallo de la guardia: es la lista cerrada tal como se aceptó, y su coste es partir esos comandos
en dos llamadas.

### 1.5 El hallazgo 5, medido (no se arregla en esta rama)

Guiones en disco, nuevos en la rama, que leen el fichero sintético con la ruta compuesta por partes,
relativa a la raíz del repo sintético. Igual en `main` y en la rama:

| Caso | Cómo compone la ruta | Hoy |
|---|---|---|
| `h5-joinpath` | `Path('.').joinpath('knowledge', 'cases', 'holdout', '1', 'secreto.yaml')` | **PASA** |
| `h5-os.path.join` | `os.path.join('knowledge', 'cases', 'holdout', '1', 'secreto.yaml')` | **PASA** |
| `h5-barra` | `Path('knowledge') / 'cases' / 'holdout' / '1' / 'secreto.yaml'` | **PASA** |
| `h5-fstring` | `f'knowledge/cases/{zona}/1/secreto.yaml'` | NIEGA, porque su trozo literal `knowledge/cases/` es una carpeta de una zona con material protegido (`motivo_dentro_de_zona`) |
| `h5-fstring-partes` | `f'{a}/{b}/holdout/1/secreto.yaml'` con `a, b = 'knowledge', 'cases'` | **PASA** |
| `h5-concatenacion` | `'knowledge' + '/' + 'cases' + '/holdout/1/secreto.yaml'` | **PASA** |

Cinco de seis pasan: el hueco que vio el consultor existe. El único que se niega lo hace porque un
trozo literal coincide con una carpeta de zona, no porque la guardia entienda la composición.

### 1.6 Límites declarados

| Límite | Qué pasa | Dónde queda |
|---|---|---|
| Un proceso en segundo plano de una llamada ANTERIOR | La guardia ve una llamada y el disco de ese instante | Límite (fase 0) |
| Lo que el guion o el código en línea importan o ejecutan (`import` local, `runpy`, `exec`, `subprocess`) | No se lee (`v-runpy` PASA) | Entrada nueva de la Next Action, con el texto del consultor, en el commit del contrato del cierre |
| Una ruta protegida compuesta por partes (hallazgo 5) | §1.5 | Entrada nueva de la Next Action, con el texto del consultor, en el cierre |
| `make` con el `Makefile` de `main` ejecuta código de la rama (`src/`, `tests/`, `scripts/`), igual que la CLI y la suite | Pasa | Límite (respuesta, punto 3) |
| `tests/` y el código de `src/` que ejecuta la CLI | Lo que ya está en disco no se lee, por diseño; lo creado en el mismo comando lo niega la lista cerrada | Límite |
| Los hooks de git | Los instala `make hooks` | Límite |
| **Variables de entorno que cargan código, con valor literal** (`BASH_ENV`, `PYTHONPATH`, `PYTHONSTARTUP`, `NODE_OPTIONS`, `PERL5OPT`, `RUBYOPT`) | La lista admite asignaciones literales, y estas cambian qué se ejecuta: `BASH_ENV=x.sh bash y.sh` ejecuta `x.sh` | Nuevo, encontrado en la fase 1. Propuesta para el consultor: que las asignaciones admitidas sean una lista cerrada de NOMBRES (`PYTHONUTF8`, `PYTHONIOENCODING`, `BOTSITO_ALLOW_MAIN`, `LANG`, `LC_ALL`, `TZ`...), o entrada de la Next Action |
| **Otras claves de `git -c` que ejecutan un programa** (`core.pager`, `core.editor`, `core.sshCommand`, `diff.external`, `credential.helper`, `filter.*`) | Solo el alias con `!` pasa por la condición | Nuevo. Propuesta: una lista cerrada de claves admitidas en `git -c`, o entrada de la Next Action |
| Programas que ejecutan según su configuración (`npm run`, `tox`, `pre-commit run`) | Pasan como lectores | Nuevo; ninguno se usa en este proyecto. Límite |
| PowerShell se analiza por palabras | Un `Select-String python` se niega (falso positivo); y al revés, lo que no es una palabra reconocida pasa: `[System.Diagnostics.Process]::Start(...)`, `Start-Job { .\x }`, `cscript`, `.\x.exe` (revisor, B2) | Aceptado el falso positivo; lo que pasa, en la decisión de §1.12 |
| **Un programa que la guardia no conoce es un lector** (decisión de la fase 0, §0.d, aceptada): `php`, `lua`, `java`, `go run`, `awk -f`, `sed -f`, `ksh`, `fish -c`, `ipython`, `pypy3`, `setsid`, `sudo`, `watch`, `script -c`, `poetry run`, y `trap '…' EXIT` (`trap` está en la lista de lectores de metadatos) | Pasan, también con un `cp` delante (revisor, B2) | **Decisión del consultor** (§1.12) |
| Otras formas de cambiar lo que corre: `PYTEST_ADDOPTS`, `PATH`, `GIT_CONFIG_*` como asignaciones literales | Pasan: la lista admite cualquier nombre de variable con valor literal (revisor, B3 c) | Junto a las variables que cargan código (fila de arriba): decisión del consultor |
| **La suite en un `git worktree`** | `uv run pytest` sin rutas fuera de la raíz del repo se niega: el ensayo aislado de CLAUDE.md («un script que escribe archivos se ensaya en un clon desechable creado con `git worktree add`») ya no puede correr la suite allí desde la sesión (2 de los 102 comandos reales) | Decisión del consultor: lo lanza Aleks con `!`, o la exención de `tests/` se extiende al `tests/` de un worktree de este mismo repositorio |

### 1.7 Desviaciones

1. **El fixture del repo sintético lleva un `Makefile` commiteado en `main`.** `make check >
   make-check.log 2>&1` tenía que seguir pasando en `test_sin_la_opcion_los_mismos_comandos_pasan`, y
   ahora `make` exige el `Makefile` de `main` (respuesta, punto 3). No cambia ninguna aserción.
2. **El arreglo del heredoc (§1.2)**, que no pedía el encargo: sin él, la regla nueva negaba heredocs
   legítimos y `main` no leía la primera línea de un `python - <<'EOF'`.
3. **Lo que la fase 1 añadió para que cada vía sepa qué se ejecuta**, todo pasando por la función
   como `indecidible` y no con decisión propia:
   - los envoltorios se quitan con sus opciones (`nice -n 5`, `timeout -s KILL 5`, `stdbuf -oL`,
     `exec -a`, `env -u/-C`), y `env -S` se niega: antes, `nice -n 5 python a.py` dejaba `-n` como
     programa (`v-nice`);
   - las opciones de `uv run`, en una lista cerrada (las que toman valor y las que no, de uv 0.9);
     una que no está se niega, porque sin saber si toma valor no se sabe qué programa corre; y
     `uv run -m x` es `python -m x`;
   - un programa que la guardia no conoce y recibe el nombre de un intérprete o de un shell
     (`winpty python x`, `sudo bash x`) se niega, salvo los lectores de `LECTORES_CON_PATRON`
     (`grep`, `rg`, `sed`... cuyo «python» es un patrón);
   - el programa escrito como variable (`$PY x.py`) se resuelve si se sabe su valor; si no, se niega;
   - en `pytest`: `-p <plugin>` que no sea `no:...`, `--pyargs`, y `pytest` sin rutas fuera de la
     raíz del repo, se niegan; en `make`, una opción o una variable;
   - un intérprete sin guion ni código solo pasa con `--version`/`--help`;
   - el código de un heredoc SIN comillas que tenga `$` o acentos graves se niega (el shell lo
     expande antes);
   - `<(...)` y `>(...)` cuentan como sustitución.
4. **Los mensajes** mostraban las marcas internas de las variables (`\x00V…\x00`); `_niega` las
   escribe como `$VAR`. Lo encontró la comparación con los comandos reales (su salida salía binaria).
5. **La rama de la CI de Linux se llama `fix/guion-mismo-comando`, no `fix/trabajo-guion-mismo-comando`.**
   Con el nombre del encargo, la CI se paró en el contrato antes de los tests (run #232, §1.10):
   `scripts/contrato_rama.py` compara los nombres sin el prefijo, y `trabajo-guion-mismo-comando` no
   es `guion-mismo-comando`. Se empujó con el nombre de `RITUAL.md`
   (`trabajo/<rama>:refs/heads/fix/<rama>`). Las dos referencias remotas existen; se borran en el
   cierre, con las demás.

### 1.8 Encargo frente a lo hecho

| Lo pedido | Estado | Evidencia |
|---|---|---|
| Fase 0 a-d y PARADA | Hecho | §0 y su commit `29bf2c1` |
| Una sola función, `exigir_ejecucion_verificable`, desde todas las vías; ninguna vía con código propio | Hecho | §1.1; test por `ast` |
| Guion que no existe o no se lee → niega, diciendo «Write» y «otra llamada» | Hecho | `test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo` |
| Tests: cada caso de 0.b y variantes; vías 2, 4, 5, 7, 8, 9, 10 y 11; cada elemento de la lista cerrada; un programa inventado; `make` con otro `Makefile` | Hecho | §1.3 |
| Anexo de mutaciones | Hecho | `sin_condicion.py`: 57 de 81 sin la condición |
| Los 32 de `RITUAL` pasan; caso a caso, nada de lo que hoy se niega pasa a pasar | Hecho | §1.3 y §1.4: 0 casos NIEGA→PASA en el sintético y en 444 comandos reales |
| `medir_huecos.py` contra la guardia nueva, todos los casos del encargo NIEGA salvo el hallazgo 5 | Hecho | `medir_huecos-FASE1-SALIDA.txt`, §1.4 |
| Hallazgo 5: medirlo, sin arreglarlo | Hecho | §1.5 |
| Lista cerrada con los tres añadidos; `python a.py && python b.py` se niega | Hecho | §1.3 (`…lista_cerrada_pasa`, `…fuera_de_la_lista_se_niega`) |
| Vías 2, 4, 5, 9, 10, 11 y 8 en esta rama | Hecho | §1.1 |
| `make` opción (a) y su límite | Hecho | §1.1, §1.6 |
| Next Action: lo que importa el guion y el hallazgo 5, entradas nuevas | En el commit del contrato del cierre (respuesta, puntos 4 y 5) | — |
| Fila de ERRORES-RECURRENTES del hallazgo 5 | En el cierre | — |
| Decisiones registradas (repo público; demo de FTMO) | Hecho, copiadas tal cual en el encargo | `docs/encargos/trabajo-guion-mismo-comando.md`; la Next Action no tiene ninguna entrada sobre el repo público (`grep -n "público\|publico\|privad" PROJECT_STATE.md`: nada), así que en el cierre no sale nada por ese punto |
| No se toca motor, spec, `knowledge/`, cifras, `criterio_fidelidad.yaml`, `CLAUDE.md` | Hecho | `git diff --stat main`: solo `.claude/hooks/guardia.py`, su test, el informe, el encargo, el contrato, `PROJECT_STATE.md`, `HISTORIA.md` y los anexos |
| No se ejecuta `botsito motor arnes` ni se abre material protegido | Hecho | ningún comando de la rama lo hace; todos los tests y medidas, sobre rutas sintéticas |
| CI de Linux por `fix/trabajo-guion-mismo-comando` | §1.10 | — |
| Revisor, con su informe pegado | §1.11 | — |

### 1.9 Comandos y salidas de la fase 1

| Comando | Salida |
|---|---|
| `uv run ruff check .claude/hooks/guardia.py tests/unit/test_guardia_claude.py`; `ruff format` | limpio |
| `uv run mypy` | `Success: no issues found in 242 source files` |
| `uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider` | 339 casos, exit 0 (236 de antes + 103 nuevos; 317 en la primera pasada) |
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/medir_huecos.py <guardia de main> .claude/hooks/guardia.py` | 58 casos (46 en la primera pasada): 39 PASA→NIEGA, 19 iguales; `Casos que main niega y la rama deja pasar: 0` |
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/comandos_reales.py <transcripcion> <guardia de main> .claude/hooks/guardia.py <repo>` | 502 distintos: 398 iguales, 104 PASA→NIEGA, 0 NIEGA→PASA (en la primera pasada, 444: 342, 102, 0) |
| `uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py` | `VEREDICTO: sin la condicion fallan exactamente los que esperan una negacion; cada pieza rompe los suyos; restaurada, todo pasa` |
| `uv run botsito state check` | `OK` (`Tests Currently Passing`: 1383 → 1391) |

**Dos medidas corregidas durante la fase 1**, declaradas: (1) `malo.sh` escribía la ruta con `\` de
Windows y sin comillas, que bash convierte en `C:Users...`: el guion medido no habría leído nada; se
escribe con `/`, y entonces la rama lo niega y `main` no. (2) La primera salida de
`comandos_reales.py` era binaria por las marcas de los mensajes (desviación 4). Y la regla nueva se
aplicó a los comandos de esta misma sesión desde que se escribió: cuatro de ellos se negaron (un
`git show ... > fichero` antes de un guion, un `sed -n` antes de `pytest`, un `sed -i` antes de
`botsito state check`) y se partieron en dos llamadas, como dice el mensaje.

### 1.10 CI de Linux

| Run | Rama | Commit | Resultado |
|---|---|---|---|
| #232 (`37667745271`) | `fix/trabajo-guion-mismo-comando` (el nombre del encargo) | `f22179f` | `failure` en el contrato, ANTES de los tests: «contrato.yaml es de la rama 'trabajo/guion-mismo-comando' y esta es 'fix/trabajo-guion-mismo-comando'» (desviación 5) |
| #233 (`37668046004`) | `fix/guion-mismo-comando` | `f22179f` | `failure` con **1 failed, 2204 passed, 8 skipped**: el único fallo, `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/guion-mismo-comando'; la rama actual es 'fix/guion-mismo-comando'»), el aceptado. Ningún test de la guardia falla en Linux |

El commit con los arreglos del revisor se empuja a `fix/guion-mismo-comando` tras sellarse; su run se da en el mensaje al consultor y entra en este informe con el siguiente commit.

### 1.11 Informe del revisor (subagente `revisor`, 2026-10-07), tal cual

## Informe del revisor · trabajo/guion-mismo-comando · 2026-10-07

Rama `trabajo/guion-mismo-comando`, HEAD f22179f (arbol 61096193…, que es el que sella `make-check.log`), contra main cbfe4e4. Commits: 55b4a37, 29bf2c1, f22179f. Cambia 14 ficheros, todos dentro del contrato; no toca `src/`, `knowledge/`, `CLAUDE.md`, `.claude/settings.json`, agentes ni skills.

**Veredicto corto.** La parte «lo que va antes y lo que va detrás» niega por defecto de verdad. Lo que no niega por defecto es la decisión de qué es una ejecución. Esa decisión es una lista de nombres de programa, y comandos como `cp a.py b.py && uv -q run python b.py` (el caso b1 del encargo con una opción global de `uv`) PASAN. Es el patrón que dejó la lección de umbral-mayo, y el informe lo declara «Hecho». La rama no está lista.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 5 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | importa | El informe afirma «todas las vías… ninguna con decisión propia» (§1.1, §1.8 «Hecho»), y no es cierto. Las vías 12, 13 y 14 de §0.a (`xargs`, `eval`/`source`/`.`, `cmd /c`) siguen decidiendo con `raise BloqueoError` propio, y la tabla «Quién la llama» las omite sin decirlo. El test `test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta` no comprueba lo que su nombre dice. Solo exige que cada vía llame a alguna de las puertas (`llama(via) & puertas`) y que `R_EJECUCION` solo la escriban `_niega` y `exigir_ejecucion_verificable`. Una vía con un `raise` propio no lo detecta. | `.claude/hooks/guardia.py:1214-1217` (`eval`/`source`/`.`), `:1241-1242` (`cmd`), `:1621-1623` (`xargs`). Test: diff de `tests/unit/test_guardia_claude.py`, última función. §1.1 «Quién la llama» llega a la fila 15 y salta 12-14 y 16. |
| A2 | importa | §1.6 «Límites declarados» omite límites que mis mediciones demuestran (detalle en B1-B4). Los que faltan: intérpretes y lanzadores no listados (`php`, `awk -f`, `ksh`, `setsid ./x`, `watch "python x"`), `trap '…' EXIT`, la detección de PowerShell por palabras sueltas, `-o addopts=-p…`, `-c ini` y `PYTEST_ADDOPTS` frente a `pytest -p`, `git --config-env` y `GIT_CONFIG_*`, y `cd` sin argumentos. El límite de variables de entorno nombra seis (`BASH_ENV`, `PYTHONPATH`, …) y no `PATH`, `PYTEST_*` ni `GIT_CONFIG_*`. §0.d sí dice «un programa desconocido sigue siendo un lector», pero §1.6 no lo repite y §1.8 marca «Hecho» sin matices. | Salidas de B1-B4 más abajo; §1.6 completo. |
| A3 | menor | «Ningún caso que hoy se niega pasa a pasar» (§1.4, §1.8, §1.9) vale para los 46 y los 444 casos del informe, pero no como propiedad. Con 30000 secuencias aleatorias de fichas (semilla 7) contra `main` y la rama aparecen 8 casos NIEGA→PASA. Todos son degenerados: `timeout $X` sin comando, `timeout -n eval`, `pytest -n $X … tests/…` y `\| sh -n -m … <<EOF` (el heredoc manda sobre la tubería, lo que es correcto). La causa de los `timeout`: `_quitar_envoltorios` hace `[1:]` tras las opciones sin comprobar que hay duración. | Comprobación 4 más abajo; `guardia.py:1132-1133`. |
| A4 | menor | `.claude/hooks/solo_lectura.py:57` llama a `guardia._quitar_envoltorios`, que ahora puede lanzar `IndecidibleError`, y no la captura. Con `uv run --opcion-rara …` o `env -S x` el hook del revisor se cae, y una caída no bloquea. La guardia sí niega esos mismos comandos, así que el efecto neto sigue siendo «niega». | `solo_lectura.motivo('uv run --opcion-rara python x.py')` lanza `IndecidibleError`. |
| A5 | menor | Dos cifras o comandos del informe no se reproducen tal cual. (1) §1.4 desglosa los «90 con algo delante» y la suma es 87; faltan 3 porque `comandos_reales-SALIDA.txt` trunca el motivo de 3 rutas largas (líneas 79, 135 y 147). (2) El comando de §0.e que da «32 casos» ya no los da: `medir_huecos.py` se editó en la fase 1 y ahora imprime 46. | `grep -c "antes, en el mismo comando"` da 87, más 3 líneas truncadas «antes, e…» = 90. `medir_huecos.py` (46 casos) frente a `medir_huecos-SALIDA.txt` (32 líneas). |
| A6 | menor | Existe en el remoto una referencia extra, `origin/fix/guion-mismo-comando`, además de la pedida `origin/fix/trabajo-guion-mismo-comando`. Las dos apuntan a f22179f. | `git rev-parse HEAD origin/fix/guion-mismo-comando origin/fix/trabajo-guion-mismo-comando`: tres veces f22179f. |
| A7 | menor | `sin_condicion.py` da el veredicto con `bool(fallan)` (cualquier fallo vale). No comprueba que los fallos sean los esperados (57 / 21 / 2), y las tres mutaciones son gruesas. Ninguna ataca por separado las sustituciones, el `&`, los filtros o la salida al propio guion; «sin lo de antes» las agrupa. | `sin_condicion.py:103`. |

Comprobado sin hallazgos:
- Contrato: `uv run python scripts/contrato_rama.py` da «CONTRATO: 14 ficheros dentro del contrato…».
- `uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider`: 317 casos, todos pasan (236 antiguos más 81 nuevos).
- `uv run botsito state check`: OK. `Tests Currently Passing` 1383→1391 = 8 funciones `test_ejecucion_*` (`grep -c` da 8).
- `make-check.log`: `2213 passed`, ruff y mypy limpios, línea `SELLO … arbol 61096193…` igual a `git rev-parse HEAD^{tree}`, `exit=0`, `PICO DE MEMORIA 292 MiB`.
- Sin trailers `Fuente:` que exigir (no se toca `knowledge/spec` ni `cases`). Sin ADR, ambigüedades ni informes cerrados cambiados.
- `HISTORIA.md` solo se amplía (0 líneas borradas; añade `# Archivo 23`). Todo lo demás de `docs/` y `knowledge/` es `A`.
- Material protegido: nada se abre. `comandos_reales-SALIDA.txt` oculta 7 líneas de material adicional o backtest y el recuento coincide con el informe. Mis medidas usaron el repo real como `cwd`, scripts inexistentes y solo `decidir()`.
- Citas del informe contra la fuente: los números de línea de §0.a coinciden con `main:.claude/hooks/guardia.py` (`_exigir_guion` 1638, `_igual_que_en_main` 1665, `_analizar_pytest` 1538, `_analizar_make` 1457, `analizar_powershell` 1770). Las cifras de §1.3 (17+18+23+19+1+1+1+1 = 81) y de §1.4 (32 de PASA a NIEGA y 14 iguales) cuadran con el código y con `medir_huecos-FASE1-SALIDA.txt`.
- El hallazgo del heredoc (§1.2) está probado: `f1-heredoc` pasa en main y se niega en la rama (salida línea 100).

### Eje (b) · Encargo
Resumen: 1 bloquea, 4 importa, 1 menor. Requisitos: 24 hechos, 3 parciales, 1 no hecho.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| R1 | Abrir rama: comprobar sha, tag y CI; skill abrir-rama (encargo, contrato, HISTORIA) | Hecho | Cabecera del informe, commit 55b4a37, Archivo 23. La CI de main no pude consultarla. |
| R2 | Fase 0 a): vías, línea y comportamiento con fichero inexistente | Hecho | §0.a, 16 filas. |
| R3 | Fase 0 b): seis casos y variantes medidos con `decidir()` | Hecho | §0.b y `medir_huecos-SALIDA.txt`: 28 PASA, 4 NIEGA. |
| R4 | Fase 0 c): límites con propuesta | Hecho | §0.c. |
| R5 | Fase 0 d): lista cerrada con porqué de cada añadido | Hecho | §0.d. |
| R6 | PARADA: sin código antes de la respuesta | Hecho | `git show --stat 29bf2c1`: solo informe, salida y `medir_huecos.py`. |
| R7 | Una sola función con nombre propio | Hecho | `guardia.py:2169` `exigir_ejecucion_verificable`. |
| R8 | Llamada desde TODAS las vías del inventario | Parcial | Vías 1-11 y 15 llegan a la función. Las vías 12-14 siguen con `raise` propio (A1). |
| R9 | Guion inexistente o ilegible: se niega con «Write» y «otra llamada» | Hecho | `_niega` usa `COMO_EJECUTAR`. Test `…no_existe_dice_como_reescribirlo`. |
| R10 | Tests por caso de 0.b (b1-b6 y variantes) | Hecho | 17 casos en `…cambiada_en_el_mismo_comando_se_niega`. |
| R11 | Tests por vía (2, 4, 5, 7, 8, 9, 10, 11) | Hecho | 18 casos en `…cada_via_pasa_por_la_condicion`. |
| R12 | Un test por elemento de la lista cerrada que pasa | Hecho | 23 casos. |
| R13 | Un test con programa inventado antes; un test de make con otro Makefile | Hecho | `inventado && python inocuo.py`, `…make_solo_con_el_makefile_de_main`. |
| R14 | Anexo de mutaciones que falle si se quita la condición | Hecho | Lo ejecuté: 57/81 sin la condición, 21/81 sin lo de antes, 2/81 sin la existencia. «VEREDICTO: cada mutacion rompe sus tests y restaurada pasan». Salvedad en A7. |
| R15 | Los 32 de RITUAL y los 236 antiguos siguen pasando | Hecho | pytest, 317 sin fallos. |
| R16 | Caso a caso con main: nada que hoy se niega pasa a pasar | Hecho, con salvedad | 0 en los 46 y 444 del informe. Salvedad degenerada en A3. |
| R17 | `medir_huecos.py` contra la guardia nueva: todo NIEGA salvo el hallazgo 5 | Hecho para los casos del encargo | `medir_huecos-FASE1-SALIDA.txt`: 0 `!!`, 32 `->`. Pero formas triviales de b1 siguen pasando (B1). |
| R18 | Respuesta 1: tres añadidos y `python a.py && python b.py` se niega | Hecho | `_es_preparacion`; `botsito` en `analizar_comando:1224`; test `python inocuo.py && python existente.py`. |
| R19 | Respuesta 2: todas las vías en esta rama | Parcial | Entran, pero la detección de qué es una ejecución es una lista (B1, B2). |
| R20 | Respuesta 3: make opción (a) y límite declarado | Hecho | `_exigir_guion_legible` con `lenguaje == "make"`; límite en §1.6. |
| R21 | Respuesta 4: Next Action sobre lo que importa el guion | Hecho por ahora | Va en el commit del contrato del cierre (§1.6). |
| R22 | Respuesta 5: medir joinpath, `os.path.join`, `/` y f-string sin arreglar | Hecho | §1.5: 5 de 6 PASAN. `analizar_codigo` no se toca. Next Action y fila de ERRORES-RECURRENTES en el cierre. |
| R23 | Decisiones del encargo copiadas, y Next Action sin entrada del repo público | Hecho | `docs/encargos/…md`; `grep` de «público/privad» en `PROJECT_STATE.md` no da nada. |
| R24 | Informe: encargo frente a lo hecho, desviaciones, comandos, límites, comparación; estado al final | Hecho | §1.7-§1.9 y «Estado» EN CURSO. Límites incompletos en A2. |
| R25 | Lo que no cambia (motor, spec, knowledge, cifras, `criterio_fidelidad.yaml`, `CLAUDE.md`) | Hecho | `git diff --name-status`. |
| R26 | Nadie ejecuta `botsito motor arnes` ni abre material protegido | Hecho | Ningún comando medido lo hace. |
| R27 | CI de Linux: push de `fix/trabajo-guion-mismo-comando` y número de run | Parcial | La referencia está empujada a f22179f (más la sobrante de A6). Falta el número de run (§1.10 «Pendiente»). Un run sobre el último commit lo debe traer el informe antes de la revisión final. |
| R28 | Revisor, con informe pegado | No hecho | §1.11 «Pendiente» (este informe). |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | **bloquea** | La condición no niega por defecto en lo decisivo: qué cuenta como «ejecución». Eso lo decide una lista de nombres (`INTERPRETES`, `SHELLS`, `EJECUTORES`, el patrón `python\d.\d`, más ficheros por extensión o `./`). Lo que no se reconoce se trata como «lector» y pasa. Cuatro formas triviales del propio caso b1 (`cp a.py b.py && …`) PASAN: `uv` con una opción global antes de `run` (`_quitar_envoltorios` solo mira `argv[1] == "run"`), `/usr/bin/env` (la comparación es `c == "env"` sobre el texto, no sobre el nombre base), expansión de llaves como comando, y un programa con glob. | `decidir()` sobre cwd = repo real: `cp a.py b.py && uv run python b.py` NIEGA («antes… va cp»). PASA: `cp a.py b.py && uv -q run python b.py`; `cp a.py b.py && uv --no-cache run python b.py`; `cp a.py b.py && /usr/bin/env python b.py`; `cp a.py b.py && {python,b.py}`; `cp a.py b.py && /usr/bin/pyth* b.py` (si el glob casa). También PASAN, sin cp delante y con script inexistente: `uv --directory . run python nx.py`, `uv tool run python nx.py`, `uvx ./nx.py`, `{python,nx.py}`, `/usr/bin/env python nx.py`. Comparación: `env python nx.py` sí se niega. |
| B2 | importa | Lo no listado se trata como lector, y §0.d lo propone así pero §1.6 no lo declara. Con script inexistente o recién copiado, PASAN: `php nx.php`, `lua`, `julia`, `java`, `go run`, `awk -f nx.awk`, `sed -f nx.sed x`, `tclsh`, `npx tsx nx.ts`, `ksh nx.sh`, `fish -c "python nx.py"`, `ipython nx.py`, `pypy3 nx.py`, `setsid ./nx.py`, `sudo ./nx.py`, `watch ./nx.py`, `ionice ./nx.py`, `watch "python nx.py"`, `script -qc "python nx.py" /dev/null`, `poetry run ./nx.py`, `trap "python nx.py" EXIT`. Con `cp a.py b.py &&` delante: `php b.php`, `setsid ./b.py`, `awk -f b.py` y `trap "python b.py" EXIT` pasan. En PowerShell, «sin ninguna ejecución» es léxico: PASAN `.\nx.exe`, `./nx`, `Start-Job { .\nx }`, `[System.Diagnostics.Process]::Start("python","nx.py")`, `cscript nx.js`, `php nx.php`, `go run nx.go`, `java Nx`, `New-Object -ComObject WScript.Shell`. | Salidas de `decidir()`. `guardia.py:897-898` (`INTERPRETES`, `SHELLS`), `:1916` (`EJECUTORES`), `:1944-1946`, `:2310-2334` (`_ejecucion_en_powershell`), `:1271-1282` (programa desconocido: solo se niega si recibe el nombre de un intérprete). |
| B3 | importa | Variantes de vías que el informe da por cerradas, con el mismo fondo que lo que sí se niega. (a) Vía 11: el alias con `!` solo se detecta como `-c alias.x=!…` literal. PASAN `CMD='!python nx.py' git --config-env=alias.x=CMD x` y `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.x GIT_CONFIG_VALUE_0='!python nx.py' git x`. (b) pytest: el test exige que `pytest -p mi_plugin` se niegue, pero PASAN `pytest -o addopts=-pmi_plugin tests/unit/…`, `pytest -c nx.ini tests/unit/…` y `PYTEST_ADDOPTS=-pmi_plugin pytest tests/unit/…`: cargan un plugin que no se lee. (c) Las asignaciones literales admiten cualquier nombre: `export PATH=./evil && pytest tests/unit/…` y `PYTHONSTARTUP=nx.py python …` pasan. El informe lo reconoce solo para seis nombres. | Salidas de `decidir()` (comprobación 1). Test `…lo_de_fuera_de_la_lista_se_niega` con `uv run pytest -p mi_plugin tests/unit`. Límite en §1.6, fila de variables. |
| B4 | importa | `cd` sin argumentos está en la lista admitida, pero la guardia lo modela como «el cwd no cambia» y bash va a HOME. Lo que se lee y lo que se ejecuta pueden ser ficheros distintos, que es justo lo que la regla quiere impedir. | `cd && python scripts/contrato_rama.py` PASA (guardia: `analizar_comando`, `if prog == "cd": if args:` sin rama para cero argumentos, `guardia.py:1199-1204`; `_es_preparacion` admite `['cd']`). `cd - && python scripts/contrato_rama.py` se niega solo por casualidad. |
| B5 | importa | Las vías 12-14 no pasan por la función (ver A1, R8). Se propone resolverlo o declararlo. | `guardia.py:1214-1217`, `:1241-1242`, `:1621`. |
| B6 | menor | Falta el número de run de CI y hay una referencia remota sobrante (ver R27 y A6). | `git branch -r`. |

Los cuatro huecos de B1 y los de B2-B3 los reproduzco todos con `decidir()` sobre un script inexistente o recién copiado, sin ejecutar nada.

### Comprobaciones pedidas

**1. ¿Niega por defecto o enumera?** Respuesta partida.
- **Lo que va antes y a la vez: niega por defecto.** `_exigir_comando_verificable` (`guardia.py:2072-2120`) pide que todo lo anterior cumpla `_es_preparacion` (`:2012-2031`), que lo posterior en la tubería cumpla `_es_filtro` (`:2034-2048`) y que, si hay `&`, todo lo demás también esté en la lista. Cualquier otra cosa se niega, y la comprobé con ejemplos inventados. `_exigir_guion_legible` (`:2123-2157`) niega lo que no existe, lo que es un directorio, el Makefile distinto de main, PowerShell y los lenguajes desconocidos, y solo deja pasar el fichero que lee o el idéntico al de main.
- **Qué es una ejecución: enumerado.** La función solo se activa si la vía reconoce una ejecución. Todo lo demás cae en «lector» (`:1283`), y la lista es la de B1-B3. Esa es la parte que el encargo quería «negando por defecto».
- **Formas de ejecutar un guion recién creado que la guardia deja pasar:** las de B1 (`uv -q run`, `/usr/bin/env`, `{python,x}`, glob) y B2. Heredocs, pipes, `&`, `$(…)`, `<(…)`, `(…)`, funciones y comentarios no encontraron escape. Las variantes de heredoc `<<-EOF`, `\EOF`, `<<"EOF"` y `EOF ` las probé y se comportan bien.
- **Fallo abierto por excepción:** `main()` deja pasar si la guardia lanza una excepción en un comando que no menciona material. 30000 secuencias aleatorias de fichas no provocaron ninguna excepción en la rama ni en main.

**2. ¿Alguna vía con código propio?** Sí: las vías 12 (`xargs`), 13 (`eval`/`source`/`.`) y 14 (`cmd /c`) niegan con `raise` propio, pre-existente y sin cambios. Son denegaciones incondicionales, más estrictas que la función, pero contradicen «ninguna vía decide por su cuenta» (A1). Las vías 1-11 y 15 sí llegan a la función; los `raise BloqueoError` restantes en `_analizar_pytest`, `_analizar_make`, `_analizar_find` y `_analizar_git` son reglas previas (salida a fichero, material protegido, git), no la decisión de ejecución.

**3. ¿Los tests fallan si se quita la condición?** Sí. Ejecuté `uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py`: con la condición fallan 0 de 81. Sin la condición fallan 57 de 81 (17+18+19+3), sin lo de antes 21, sin la existencia 2, y restaurada vuelven a 0. Veredicto «cada mutacion rompe sus tests y restaurada pasan». Coincide con §1.3. Salvedad en A7.

**4. ¿Algún caso que main niega pasa en la rama?**
- 317 casos de `test_guardia_claude.py` pasan, incluidos los 32 de RITUAL.
- Cargué la guardia de main en memoria (`git show` + `exec`, sin escribir ficheros). Comparé 445 cadenas no sensibles de los tests (de rama y de main) por Bash y por PowerShell: 647 iguales, 243 de PASA a NIEGA y 0 de NIEGA a PASA.
- Con 30000 secuencias aleatorias, 8 de NIEGA a PASA, todas degeneradas (A3).
- Los casos con rutas protegidas no los repliqué; me apoyo en la suite y en el anexo del informe.

**5. ¿Cifras del informe frente a anexos?**
- §1.3, 81 casos: coincide.
- §1.4, 46 casos, 32 de PASA a NIEGA, 14 iguales, 0 `!!`: `grep -c "^->"` da 32 y `grep -c "^!!"` da 0.
- Fase 0, 28 PASA y 4 NIEGA: coincide.
- 444 comandos: 342 iguales, 102 PASA→NIEGA, 0 NIEGA→PASA: coincide con el encabezado de `comandos_reales-SALIDA.txt`.
- Los 102 son 90+2+2+1+7: coincide (87 itemizados y 3 truncados, A5).
- §1.5, 5 de 6 PASAN: coincide con `medir_huecos-FASE1-SALIDA.txt`.
- §1.9: mypy «242 source files» y ruff limpios coinciden con `make-check.log`.

### Lo que no pude comprobar
- **La CI de Linux** (el run de `fix/trabajo-guion-mismo-comando` y la CI de main sobre cbfe4e4): requiere `curl`, que mi Bash bloquea por escritura. El run 37652207581 del informe no lo verifiqué.
- **`make check` y `git write-tree`**: no los ejecuté. Comparé el `SELLO` del log con `git rev-parse HEAD^{tree}` y coinciden, pero eso no prueba que el log sea del contenido actual.
- **`comandos_reales.py`**: necesita la transcripción de la sesión, que vive fuera del repo; solo contrasté su salida committed.
- **Cambios de comportamiento con rutas protegidas reales**: no probé comandos que las nombren.
- **Mis medidas**: todo en memoria, sin repo sintético. Usé el repo real como `cwd` con scripts inexistentes y solo `decidir()`; no ejecuté ninguno de los comandos medidos. Las formas que dependen de un fichero real (por ejemplo `/usr/bin/pyth*`) no las ejecuté.
- **Si los huecos B1-B3 son explotables en esta máquina**: `php`, `lua`, `fish` y `ksh` pueden no estar instalados. Lo demostrado es que la guardia los deja pasar sin leer.

### Comandos ejecutados
1. `git log --format='%h %s' main..HEAD`
2. `git diff --stat main...HEAD`; `git status --short`; `git branch --show-current`
3. `uv run python scripts/contrato_rama.py`
4. `tail -5 make-check.log`; `git log -1 --format=...`; `git rev-parse HEAD^{tree}`; `grep -c passed make-check.log`
5. `git diff main...HEAD -- .claude/hooks/guardia.py`
6. `python -c` que carga `guardia.py` y llama a `decidir()` (≈9 tandas): scripts inexistentes y `cp … &&` delante; variantes de heredoc; PowerShell; `uv`; `git --config-env`; `cd` sin argumentos; wrappers y programas desconocidos
7. `uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py`
8. `uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider`
9. `python -c` que carga la guardia de main con `git show main:.claude/hooks/guardia.py` en memoria y compara con la rama: 445 cadenas de tests por Bash y PowerShell, y 30000 secuencias aleatorias de fichas
10. `python -c` que importa `solo_lectura` y llama a `motivo()` con `uv run --opcion-rara …` y `env -S …`
11. `git show main:.claude/hooks/guardia.py | grep -n …` (líneas de main); `git show --stat 29bf2c1 f22179f`; `git diff main...HEAD -- tests/unit/test_guardia_claude.py PROJECT_STATE.md contrato.yaml docs/state/HISTORIA.md`; `git diff --name-status main...HEAD`
12. `grep` de `Makefile`, de `PROJECT_STATE.md` y de las skills y RITUAL; `grep -c "^def test_ejecucion_"`; `uv run botsito state check`
13. `grep` sobre `medir_huecos-FASE1-SALIDA.txt`, `medir_huecos-SALIDA.txt` y `comandos_reales-SALIDA.txt` (conteos de §1.4 y §1.9); Grep (herramienta) sobre `comandos_reales-SALIDA.txt` y sobre `*.py` para importadores de `guardia`
14. `git branch -r`; `git rev-parse HEAD origin/fix/...`; `git log main..origin/fix/guion-mismo-comando`; `git log --format='%h%n%b' main..HEAD | grep -i "co-authored|Fuente"`

Ficheros relevantes: `C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_claude.py`, `C:\Users\USER\Desktop\Bot v3\.claude\hooks\solo_lectura.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\GUION-MISMO-COMANDO.md`, `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUION-MISMO-COMANDO\`.

### 1.12 Lo que se hizo con el revisor, y la PARADA

| # | Gravedad | Qué se hizo |
|---|---|---|
| B1 | bloquea | **En lo que cabe en lo aceptado, arreglado**: los envoltorios se reconocen por su NOMBRE (`/usr/bin/env`, `.../timeout.exe`), con sus opciones en listas cerradas (`OPCIONES_DE_ENVOLTORIO`: una que no está, `indecidible`); `uv` admite sus opciones globales antes de `run`, y `uv tool run` y `uvx` son como `uv run`; un programa con comodín o expansión de llaves es `indecidible`. Los cuatro casos de B1 y los cinco sin `cp` se niegan (tests y `rv-*`). **Lo que no cabe**, que qué es una ejecución sea en sí una lista cerrada, es la PARADA de abajo |
| B2 | importa | **PARADA**: contradice una decisión aceptada (§0.d). Medido abajo |
| B3 | importa | (a) `git --config-env` es `indecidible`; `GIT_CONFIG_*` como variable, a la PARADA. (b) `pytest -c`, `-o`/`--override-ini` y los valores dinámicos son `indecidible`; `PYTEST_ADDOPTS` como variable, a la PARADA. (c) Los nombres de variable, a la PARADA |
| B4 | importa | `cd` a secas lleva a HOME (`analizar_comando`) y deja de estar en la lista (`_es_preparacion` exige una ruta literal, y no `-`) |
| A1 / B5 | importa | Las vías 12-14 pasan por la función como `indecidible`; el test por `ast` exige ahora que ninguna vía de ejecución tenga un `raise` propio |
| A2 | importa | §1.6 recoge los límites que faltaban |
| A3 | menor | `timeout` exige una duración literal y sus opciones son una lista cerrada; un valor dinámico de una opción de `pytest` es `indecidible`. El caso del heredoc que manda sobre la tubería, sin cambio (correcto, dice el revisor) |
| A4 | menor | `_quitar_envoltorios` vuelve a no lanzar nunca, para `solo_lectura.py` (que no está en el contrato): la guardia usa `_envoltorios`, que sí lanza |
| A5 | menor | El desglose de los comandos reales lo calcula el guion sobre el motivo entero; §0.e dice que su salida es de la versión de la fase 0 del guion |
| A6 / B6 | menor | Desviación 5 y §1.10: el run de la CI está, y la referencia de más se explica y se borra en el cierre |
| A7 | menor | La condición, en piezas con nombre; una mutación por pieza; el veredicto exige que fallen exactamente los esperados (§1.3) |

**Comprobado tras los arreglos**: 339 casos de la guardia pasan (los 236 de antes, los 32 de `RITUAL`
incluidos); `sin_condicion.py` da su veredicto; la comparación con `main` sigue en 0 casos NIEGA→PASA
(58 sintéticos y 502 comandos reales).

**PARADA: ¿qué cuenta como una ejecución?** Hoy (decisión aceptada en §0.d) una ejecución es lo
que la guardia reconoce -intérpretes, shells, `pytest`, `make`, `botsito`, un fichero como programa,
los envoltorios conocidos- y **un programa que no conoce es un lector**. El revisor (B1, B2) dice que
eso es enumerar y lo da por bloqueante; tiene razón en el fondo, pero cambiarlo es revocar una
decisión tuya, así que no lo hago sin tu respuesta. Lo medí (experimento en la carpeta de trabajo,
sin tocar la guardia):

- **Variante**: todo programa FUERA de una lista cerrada de los que se sabe que no ejecutan código
  (los lectores de metadatos, los que no leen rutas, los lectores con patrón, los archivadores, `rg`,
  y `git`, `rm`, `mv`, `cp`, `rsync`, `scp`, `wc`, `certutil`, `ruff`, `mypy`, `lint-imports`, `jq`,
  `xxd`, `od`, `cmp`, `comm`, `tee`, `nl`, `column`, `paste`, `join`, `base64`, `iconv`,
  `dos2unix`, `unix2dos`, `strings`, `hexdump`, `fold`, `fmt`, `split`, `md5`, `sha1sum`, `cksum`)
  cuenta como ejecución y pasa por la función.
- **Coste**: sobre los 503 comandos reales distintos de esta sesión, **0** que la rama deja pasar y
  la variante niega.
- **Lo que gana**: `cp a.py b.php && php b.php` y `cp a.py b.py && setsid ./b.py` se niegan (lo de
  antes).
- **Lo que sigue sin cubrir**: lo que un programa desconocido ejecuta SIN nada delante (`php x.php`:
  la guardia no lee PHP), `trap '…' EXIT` (`trap` está entre los lectores de metadatos), `awk -f` y
  `sed -f` (lectores conocidos que ejecutan un programa de un fichero), y PowerShell por objeto
  (`[System.Diagnostics.Process]::Start`).

Opciones:
1. **(Recomendada)** Adoptar la variante en esta rama, y además sacar `trap` de los lectores de
   metadatos y tratar `awk -f`/`sed -f` como la ejecución de un fichero de lenguaje desconocido (se
   niega). Lo que un programa desconocido ejecuta sin nada delante queda como límite declarado. Y en
   la misma rama, decidir las variables de entorno (B3 c): una lista cerrada de NOMBRES admitidos en
   las asignaciones (`PYTHONUTF8`, `PYTHONIOENCODING`, `BOTSITO_ALLOW_MAIN`, `LANG`, `LC_ALL`, `TZ`)
   o dejarlo como entrada de la Next Action.
2. Mantener lo aceptado en §0.d y declarar B2 como límite, con una entrada de la Next Action.
3. Otra que decidas.

## Estado

**PARADA (2026-10-07), fase 1 hecha con los arreglos del revisor.** Falta tu respuesta a §1.12
(qué cuenta como una ejecución, y los nombres de variable); con ella, el cambio que decidas, su
`make check`, la CI de Linux del último commit y una segunda pasada del revisor. NO cerrada.
