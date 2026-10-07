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
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/medir_huecos.py .claude/hooks/guardia.py` | 32 casos: 28 `PASA`, 4 `NIEGA` (los tres controles y b4); literal en `medir_huecos-SALIDA.txt` |
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
| 15 `botsito` | `analizar_comando`, antes de `_analizar_cli` |

Un test lo comprueba leyendo el código con `ast`
(`test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta`): cada vía llama a la función
o a sus dos puertas (`_exigir_guion`, `_sin_guion`), `find` y `git` pasan por `_ejecucion_lanzada`,
y `R_EJECUCION` solo la escriben `exigir_ejecucion_verificable` y `_niega`.

### 1.2 Un hueco más, encontrado al implementar: el heredoc perdía su primera línea

El primer test que falló no era de la regla nueva: `cat > f.py <<'EOF'` + salto + cuerpo. Medido: en
`tokenizar`, el delimitador de un heredoc suele ser la última palabra de la línea, y al llegar al
salto todavía no estaba cerrado. Sin cerrarlo, **el cuerpo se tokenizaba como comandos de bash y su
primera línea se perdía del `cuerpo`**. En `main`, `python - <<'EOF'` con la ruta protegida en la
primera línea PASA (`f1-heredoc` en la comparación de §1.4). Es de la misma familia («lo que se
ejecuta es lo que se leyó») y la regla nueva lo necesitaba, así que se arregla aquí: el salto cierra
la palabra abierta si hay un heredoc esperando su delimitador. Ningún test existente cambia.

### 1.3 Los tests (`tests/unit/test_guardia_claude.py`, sobre el repositorio sintético)

Ocho funciones nuevas (81 casos), todas `test_ejecucion_*`:

| Test | Casos | Qué rompe |
|---|---|---|
| `…cambiada_en_el_mismo_comando_se_niega` | 17 | b1, b1', b2, b3, b3', b4, b4', b4'', b5, b5', b5'', b6, `tests/` creado en el mismo comando, `<(...)`, una copia en segundo plano a la vez, la salida a su propio guion, algo por la tubería antes |
| `…cada_via_pasa_por_la_condicion` | 18 | vías 2, 4, 5, 6 (directorio), 7, 8 (Bash y PowerShell, `&`), 9 (`./a.py`, `uv run a.py`, `python3.12`, `nice -n`, `timeout -s`, `winpty`), 10, 11 y el heredoc entero |
| `…lo_de_la_lista_cerrada_pasa` | 23 | cada elemento de la lista: `cd`, asignación literal suelta y delante del comando, `export`, `set -e`, `-u`, `-o pipefail`, `-euo pipefail`, cada filtro, lo de después en otro comando, `-X utf8`, `uv run --with`, `--version`, un `grep python`, `command -v python`, `pytest -p no:cacheprovider` |
| `…lo_de_fuera_de_la_lista_se_niega` | 19 | un programa inventado antes, un lector antes, dos ejecuciones, asignaciones y `export` no literales, `set -x`, una redirección antes, `tee`, `sort -o`, `uniq` con fichero, un filtro inventado, `python` solo, `-m json.tool`, `env -S`, una opción inventada de `uv run`, `pytest -p mi_plugin`, `pytest` sin rutas fuera de la raíz, un guion que no existe |
| `…un_guion_que_no_existe_dice_como_reescribirlo` | 1 | el mensaje: «no existe», «Write», «OTRA llamada» |
| `…make_solo_con_el_makefile_de_main` | 1 | con el de `main` pasa; cambiado, se niega y nombra a Aleks; `make -f` se niega |
| `…powershell_sin_ejecuciones_y_lo_demas_igual` | 1 | `Start-Process`, `.\x.ps1`, `make` se niegan; `git status`, `Get-Content`, `Write-Output` pasan |
| `…una_sola_funcion_y_ninguna_via_decide_por_su_cuenta` | 1 | el `ast` de §1.1 |

**Que fallan si se quita la condición** (`anexos/GUION-MISMO-COMANDO/sin_condicion.py`, salida en
`sin_condicion-SALIDA.txt`). Carga la guardia como el módulo que usan los tests, cambia una pieza EN
MEMORIA y corre los 81 casos en el mismo proceso:

| Mutación | Fallan | Restaurada |
|---|---|---|
| ninguna | 0 de 81 | — |
| «sin la condición» (`exigir_ejecucion_verificable` no hace nada) | **57 de 81**: exactamente los 57 que esperan una negación (17 + 18 + 19 + 3) | 0 fallan |
| «sin lo de antes» (`_exigir_comando_verificable` no hace nada) | 21 de 81 | 0 fallan |
| «sin la existencia» (un guion que no existe se lee como vacío, como en `main`) | 2 de 81 | 0 fallan |

`VEREDICTO: cada mutacion rompe sus tests y restaurada pasan`. Los 23 de la lista cerrada y el del
`ast` no dependen de quitar la condición, como debe ser.

**La guardia de antes, intacta:** los 236 casos que ya existían pasan, entre ellos los 32 de `RITUAL`
contra el repo real (`test_el_ritual_y_los_runbooks_pasan`). Un cambio en el fixture, declarado en
§1.7: el repo sintético lleva ahora un `Makefile` commiteado en su `main`.

### 1.4 La comparación caso a caso con `main` (`medir_huecos-FASE1-SALIDA.txt`)

`medir_huecos.py` admite ahora dos guardias y las compara: la de `main` (`git show
main:.claude/hooks/guardia.py`, en la carpeta de trabajo) y la de la rama, sobre los mismos 46 casos
del repo sintético. **Casos que `main` niega y la rama deja pasar: 0.** 32 pasan de PASA a NIEGA, y
14 no cambian:

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

**Todos los casos del encargo salen NIEGA**, salvo los del hallazgo 5. Los dos que siguen pasando y
no son del hallazgo 5 (`tests-nuevo`, `v-runpy`) no son casos del encargo: son el diseño de `tests/`
y el límite del punto 4 de la respuesta.

**Y sobre comandos reales** (`comandos_reales.py`, salida en `comandos_reales-SALIDA.txt`): las dos
guardias sobre los 444 comandos de Bash distintos de la transcripción de esta sesión, contra el repo
real. 342 con la misma decisión; **0 que `main` niega y la rama deja pasar**; **102 que `main` deja
pasar y la rama niega**. De esos 102, 7 nombran el material adicional o un backtest y solo se
cuentan; los otros 95, por su motivo: **90 llevan algo delante que no está en la lista cerrada**
-por el programa de delante: un `python` (34, casi todos `python - <<'EOF'` de esta sesión), un
`cat` (16), un `uv run` (12), un `git` (10: `git show ... >` delante de un guion, `git commit`
delante de un `python`...), un `grep` (7), un `sed` (4, uno `sed -i` delante de `pytest`), una
asignación seguida de otra ejecución (2), un `printf` (1), un `cp` (1)-; 2 llevan un `tee` detrás; 2
son `pytest` sin rutas en un `git worktree` (§1.6); y 1 lleva una sustitución de proceso. Ninguno es
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
| PowerShell se analiza por palabras | Un `Select-String python` se niega (falso positivo) | Aceptado: PowerShell no tiene ninguna ejecución admitida y ningún runbook lo usa |
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
| `uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider` | 317 casos, exit 0 (236 de antes + 81 nuevos) |
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/medir_huecos.py <guardia de main> .claude/hooks/guardia.py` | 46 casos; `Casos que main niega y la rama deja pasar: 0` |
| `PYTHONUTF8=1 python docs/validation/anexos/GUION-MISMO-COMANDO/comandos_reales.py <transcripcion> <guardia de main> .claude/hooks/guardia.py <repo>` | 444 distintos: 342 iguales, 102 PASA→NIEGA, 0 NIEGA→PASA |
| `uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py` | `VEREDICTO: cada mutacion rompe sus tests y restaurada pasan` |
| `uv run botsito state check` | `OK` (`Tests Currently Passing`: 1383 → 1391) |

**Dos medidas corregidas durante la fase 1**, declaradas: (1) `malo.sh` escribía la ruta con `\` de
Windows y sin comillas, que bash convierte en `C:Users...`: el guion medido no habría leído nada; se
escribe con `/`, y entonces la rama lo niega y `main` no. (2) La primera salida de
`comandos_reales.py` era binaria por las marcas de los mensajes (desviación 4). Y la regla nueva se
aplicó a los comandos de esta misma sesión desde que se escribió: cuatro de ellos se negaron (un
`git show ... > fichero` antes de un guion, un `sed -n` antes de `pytest`, un `sed -i` antes de
`botsito state check`) y se partieron en dos llamadas, como dice el mensaje.

### 1.10 CI de Linux

Pendiente.

### 1.11 Revisor

Pendiente.

## Estado

**EN CURSO (2026-10-07), fase 1.** Falta la CI de Linux y el revisor.
