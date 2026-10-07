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

## Estado

**PARADA de la fase 0 (2026-10-07).** El inventario está hecho y medido (§0); no se ha escrito
ninguna línea de la guardia. Espera la respuesta del consultor a las cuatro preguntas de la PARADA.
