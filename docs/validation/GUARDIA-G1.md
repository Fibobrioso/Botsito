# GUARDIA-G1 · Los falsos positivos y los huecos de la guardia (K, B y C del carril G.1)

Rama `trabajo/guardia-g1`, abierta el 2026-11-04 desde `main` en 7a3a1ff (commit de apertura
cf1bc4a). Encargo: `docs/encargos/trabajo-guardia-g1.md`. Contrato: `contrato.yaml` (riesgo medio;
tramo «Carril: guardias y deuda»). La sesión corre en la nube (Linux, sin `data/` ni `corpus/`).

## 0. Apertura: la base, y lo que cambia por correr en la nube

**La base, comprobada con git (2026-11-04)**, tras `git fetch --prune origin`:

- `git rev-parse main origin/main` → `7a3a1ff2b9ed1b34df401ca092f0b3f69f2bbbff` dos veces.
- `git rev-parse "stable/F38k-margen-pendiente^{commit}"` y `git rev-parse 7a3a1ff^1` →
  `796be274c5c587f388501bb56ac3d4990dd554e5` las dos (`main` es el commit de estado sobre el merge).
- `git ls-remote --tags origin 'stable/F38k-margen-pendiente*'` → el objeto `2ef98f6c…` y su
  `^{}` `796be274…`: el tag está en origin. Es el último `stable/*` (`git tag -l 'stable/*'
  --sort=-creatordate`, la primera línea) y la última línea `- Tag: ` de HISTORIA (`:14279`).
- La CI de `main` sobre su HEAD: run 41258026188, `head_sha` 7a3a1ff2…, `status: completed`,
  `conclusion: success` (una consulta suelta).
- Ninguna otra rama: `git ls-remote --heads origin` → solo `refs/heads/main`; `git ls-remote --heads
  origin 'fix/*'` vacío. En local, además de `main`, está `claude/festive-darwin-lg9p31`: es la rama
  con la que el entorno de la nube arranca la sesión, en el mismo commit que `main` (7a3a1ff), sin
  trabajo; no es una rama de trabajo del proyecto.

**(1) La guardia corre en esta sesión.** `make check` sin fichero de salida, lanzado a propósito:

```
PreToolUse:Bash hook error: [command hook]: GUARDIA (.claude/hooks/guardia.py) bloquea: `make check` sin la salida a un fichero.
Regla: CLAUDE.md, «Trampas medidas»: «`make check` con la salida a un FICHERO, nunca a `/dev/null`»; la forma es `make check > make-check.log 2>&1`.
```

Su orden en `.claude/settings.json` es `PYTHONUTF8=1 python "$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py"`:
si el hook corre, hay un `python` en el PATH. El primer comando de la sesión, `which python python3`
(para enseñarlo), lo negó la guardia: es un falso positivo, medido en §1.f (f15).

**(2) `uv sync --locked --group dev` y `make check`.** El primer `make check` salió con 10 fallos,
todos por el clon de la nube, que es SUPERFICIAL («la guardia de historial de evidencia no se pudo
evaluar (clon superficial: haz git fetch --unshallow)»): los seis `test_repositorio_real` de
`tests/contract/` y cuatro que leen el historial. Con `git fetch --unshallow origin` (1251 commits
en HEAD) el segundo sale en verde y sella el commit de apertura (cf1bc4a):

```
3019 passed, 46 skipped in 454.69s (0:07:34)
SELLO: make check en verde sobre el arbol 3b5f89e17662cbec92a83fea480a63a2d0e9a12b
DURACION de make check: 490 s en total; por paso (s): test 455, knowledge 33, state 1, types 0, config 0, contracts 0, contrato 0, desellar 0, sellar 0, lint 0
PICO DE MEMORIA de make check: 142 MiB en `test` (RSS maxima del mayor proceso, linux)
``` La CI de main corre sin `data/`
(`.github/workflows/ci.yml`), y aquí tampoco hay `data/` (solo `data/manifests/`, que está en git)
ni `corpus/`.

**(3) Empujar a origin.** `git push --dry-run -u origin trabajo/guardia-g1` → `* [new branch]
trabajo/guardia-g1 -> trabajo/guardia-g1`; después el push de verdad, con el commit de apertura.

**Lo que la nube cambia.** Sin `corpus/` ni `data/` de verdad, la guardia NO encuentra material
protegido en el repo real de esta sesión: un recorrido recursivo de la raíz pasa aquí y en el
portátil de Aleks se niega. Por eso todo se mide en un repo SINTÉTICO (`medir_g1.py`, §1.a), con
ficheros de mentira donde el material protegido. Lo que es de Windows (`\.` como raíz de la
unidad) se simula en memoria; el clon de `C:/cm/` es un `git worktree add --detach` en un
directorio temporal fuera del repo sintético, que es lo que importa de `C:/cm/` (estar fuera de la
raíz).

## 1. Fase 0: el inventario

Método (GUION-MISMO-COMANDO.md §1.4): `docs/validation/anexos/GUARDIA-G1/medir_g1.py` llama a
`decidir()` de la guardia, y a `motivo()` de `solo_lectura.py`, sobre el TEXTO de cada caso, en un
repo sintético en un directorio temporal. No ejecuta ninguno de los comandos medidos. Salida entera:
`docs/validation/anexos/GUARDIA-G1/medir_g1-FASE0.txt` (98 casos; 43 negados hoy). Con dos guardias (la de `main`
y la de la rama) compara caso a caso y sale con 1 si un caso que `main` niega pasa en la rama sin
estar declarado: es el método de `medir_huecos.py`, ampliado con los casos de esta rama.

**Lo que hace la medida a propósito, declarado.** Las rutas protegidas del repo sintético van a
trozos dentro de `medir_g1.py` (`_p("knowledge", "cases")`, `"hol" + "dout"`), como en
`medir_huecos.py`: escritas enteras, la guardia las resolvería contra el directorio desde el que se
lanza el guion (el repo real) y negaría la medida. Una vez la negó así: escribí entera una ruta
sintética de `data/visor/` con el id de un caso de la fixture de los tests, que en el repo real es
un caso reservado (`R_CASO`); la compuse a trozos, como manda el encargo para las rutas protegidas.
Es justo el hueco C, que esta rama mide (§1.h).

### 1.a K1: la variable del mismo nombre que la opción

| Caso | Comando o guion | Hoy | Linux/Windows | Decide | Propuesta |
|---|---|---|---|---|---|
| a1 | `uv run python scripts/leer_demo.py`, el lector cambiado en la rama con `<opción> = ruta.read_bytes()` | NIEGA «pide el corpus SIN FILTRAR» | Linux | `guardia.py:195` (`CRUDO_PYTHON`, primera alternativa), desde `analizar_codigo` `:3783` | PASA |
| a2 | guion con `d = {"<opción>": 1}` | NIEGA, mismo motivo | Linux | `:195`, segunda alternativa | NIEGA (un dict con esa clave se puede desempaquetar con `**`) |
| a3 | guion con `f(<opción>=True)` | NIEGA | Linux | `:195` | NIEGA |
| a4 | guion con `f(<opción>=False)` | PASA | Linux | `:195` (`(?!False\b)`) | PASA |
| a5 | guion con `a.<opción> = True` | NIEGA | Linux | `:195` | NIEGA (un `Namespace` con el atributo puesto) |
| a6 | guion con `f(**{"<opción>": True})` | NIEGA | Linux | `:195` | NIEGA |
| a7 | `grep -n "<opción> = " src/botsito/x.py` | NIEGA «el comando pide el corpus SIN FILTRAR» | Linux | `:195` desde `analizar_bash` `:1292` (el texto ENTERO del comando) | PASA |
| a8 | `grep -rn -E "def \|<opción>=" src/botsito` | NIEGA | Linux | `:195` desde `:1292` | PASA |
| a9 | `uv run botsito kb find x --<opción>` | NIEGA | Linux | `:194` (`CRUDO_OPCION`) | NIEGA (sin cambio) |
| a10 | `python -c "print(dict(<opción>=True))"` | NIEGA | Linux | `:195` desde `:1292` | NIEGA (por el análisis del código en línea) |

**Medido en vivo, también:** esta sesión quiso leer, con `grep -rn -E 'crudo' src/botsito --include=*.py
| grep -E 'def |crudo='`, qué funciones de `src/` tienen el parámetro, y la guardia lo negó («el comando
pide el corpus SIN FILTRAR»): es el caso a8, un falso positivo de la misma regla. Su mensaje no
propone otra forma; no busqué el dato con otra herramienta. La propuesta se apoya en lo que ya dice
el repo (CLAUDE.md, «Las guardias de Claude Code», y `R_CRUDO`, `guardia.py:185-191`: la opción de
la CLI y su equivalente en Python, `crudo=True`, con los llamadores de `AUTORIZADOS` de
`tests/unit/test_cuarentena.py`).

**Por qué pasa.** `CRUDO_PYTHON` es un regex sobre TEXTO: casa con la palabra seguida de `=` y de
cualquier cosa que no sea `False` (una asignación a una variable local, un patrón de `grep`) o con
la palabra entre comillas seguida de `:`. Se aplica a dos cosas distintas: al texto entero de cada
comando de Bash y PowerShell (`:1292`, `:4354`) y al código que se ejecuta (`:3783`).

**Propuesta de condición (una función, negando por defecto): `_pide_la_opcion(codigo, es_python)`.**
- En CÓDIGO PYTHON que se parsea, por su árbol (`ast`), la FORMA de la opción: (1) un argumento con
  nombre `<opción>=` en cualquier llamada (no se sabe qué función es: puede ser una de
  `cuarentena.py` por otro nombre) cuyo valor no sea el literal `False`; (2) una clave `"<opción>"`
  en un dict literal, con valor que no sea `False` (puede ir a `**`); (3) un atributo `x.<opción>`
  asignado a algo que no sea `False`; (4) el literal `--cr…` de `CRUDO_OPCION` en cualquier texto.
  Una asignación a un NOMBRE suelto (`<opción> = ...`, a1) no es ninguna de las cuatro: pasa.
- En código Python que NO se parsea (SyntaxError): el regex de hoy, entero (negar por defecto).
- En el TEXTO de un comando de Bash o PowerShell: solo `CRUDO_OPCION`. `<opción>=True` en Bash no es
  nada; si el comando ejecuta Python (`python -c`, un heredoc, un guion), ese código pasa por el
  análisis de arriba, que es donde la forma significa algo (a10 sigue negado por ahí).
- Lo que se afloja, dicho por su nombre: el texto `<opción>=…` dentro de un COMENTARIO de Python, o
  de un comando de Bash que no ejecuta Python (a7, a8). Ninguno puede llamar a la cuarentena.

**`«<opción>»: …` y `"<opción>": …` en código que no llama a la cuarentena** (pregunta del encargo):
la guardia no puede saber si un dict llega a una función de `cuarentena.py` (`**`, `setattr`,
`json`), así que la clave en un dict literal sigue negada (a2, a6). Coste medido: ninguno de los
guiones de la carpeta de trabajo citados (leer_demo_ftmo, prevision.py, EA-CONEXION) la usa como
clave; los tres son la asignación a un nombre (a1).

### 1.b K2: los tests de un clon de comparar-con-main, fuera de la raíz

| Caso | Comando | Hoy | Linux/Windows | Decide | Propuesta |
|---|---|---|---|---|---|
| b1 | `cd <clon> && uv run pytest tests/unit/test_recorre.py -q` (fichero igual al de main) | NIEGA «el codigo recorre directorios … nombra material sensible» | Linux (el clon solo tiene que estar fuera de la raíz) | `_analizar_pytest` `:2201-2204` (fuera de `tests/` del repo es un guion) → `_exigir_guion_legible` `:3671-3672` (`rel is None`: no se compara con main) → `analizar_codigo` `:3809` | PASA |
| b2 | `uv run pytest <clon>/tests/unit/test_recorre.py -q` (desde el repo) | NIEGA, mismo motivo | Linux | idem | PASA |
| b3 | `cd <clon> && uv run pytest tests/unit/test_nuevo.py` (el test NUEVO de la rama, copiado al clon: igual byte a byte al del repo) | NIEGA | Linux | idem | PASA |
| b4 | lo mismo con un test del clon CAMBIADO (ni el de main ni el del repo) | NIEGA | Linux | idem | NIEGA (sin cambio) |
| b5 | `cd <clon> && uv run pytest -q` (sin rutas) | NIEGA «`pytest` sin rutas fuera de la raiz …» | Linux | `:2206-2210` | NIEGA (sin cambio) |
| b6 | dos pytest encadenados con `&&` en el clon | NIEGA (el primero, por b1; con la propuesta, por «antes va …») | Linux | `_exigir_lo_de_antes` `:3596` | NIEGA (sin cambio, §1.f) |
| b7 | `uv run pytest tests/unit/test_recorre.py` en el repo | PASA | — | `:2202` (exención de `tests/`) | PASA |
| b8 | test del clon con el literal `'/'` y un recorrido | NIEGA «el codigo nombra la carpeta /» (ACTIVAR-SESION-05.md §0.f, `test_kit.py`) | Linux | `analizar_codigo` `:3802-3808` (`/` CONTIENE la raíz: `contiene_la_raiz`) | PASA (igual al de main) |
| b9 | test del clon con `dict(<opción>=True)` (ENTORNO-CODE.md, G.1; ENTRADA-JULIO.md §9) | NIEGA «pide el corpus SIN FILTRAR» | Linux | `:3783` | PASA (igual al de main) |

**Cómo decide hoy qué es un test.** Dos vías, las dos atadas a la raíz del repo: (1)
`_analizar_pytest` (`:2199-2204`) da por revisado todo fichero cuya ruta, relativa a la raíz, esté
en `tests/` (la suite «corre con la guarda del holdout», `tests/guarda_holdout.py`); (2)
`_exigir_guion_legible` (`:3671-3673`) da por revisado un guion que sea EXACTAMENTE el blob de
`main` (`_igual_que_en_main`, `:3739-3762`), pero solo si `relativa()` no es `None`. Un clon de
`C:/cm/` está fuera de la raíz: `relativa()` da `None`, ninguna de las dos vías se mira, y el test
se lee como código sin revisar con `analizar_codigo`, que niega por el recorrido, por `/` o `\.`,
o por la opción.

**Propuesta: `_test_de_un_clon(ruta) -> bool`, negando por defecto.** Un fichero fuera de la raíz se
trata como el test del repo SOLO si: (1) está dentro de un `git worktree` de ESTE repositorio (su
carpeta raíz tiene un fichero `.git` con `gitdir: <raíz>/.git/worktrees/<n>`, comparado en forma
canónica); (2) su ruta relativa a esa carpeta empieza por `tests/`; y (3) sus bytes
(`git hash-object`) son el blob de esa ruta en `main` del repo real, O el fichero de esa misma ruta
en el árbol de trabajo del repo real (que dentro del repo ya está exento: es el test nuevo de la rama,
copiado al clon, b3). Lo que no se pueda comprobar (git falla, no hay `.git`, no casa) se lee como
hoy. Se usa en `_analizar_pytest` (como la exención de `tests/`) y en `_exigir_guion_legible`
(como `_igual_que_en_main`). Lo que NO cambia: `pytest` sin rutas fuera de la raíz (b5) y dos
ejecuciones en un mismo comando (b6).

Riesgo que se declara: como dentro del repo, la guardia no lee el `conftest.py` ni el `src/` que el
clon carga; son los de un commit del propio repo (el clon es `--detach` de `main` o de la rama).

### 1.c K3: `\.`, la raíz de la unidad en Windows

| Caso | Comando | Hoy | Linux/Windows | Decide | Propuesta |
|---|---|---|---|---|---|
| c1 | `cd <clon> && uv run pytest tests/unit/test_regex.py` (un test con `SEP = '\\.'` en un f-string de regex y un recorrido) | PASA en Linux; NIEGA con Windows simulado: «el codigo nombra la carpeta \., que contiene material protegido» | solo Windows (en Linux `\.` es un nombre de fichero) | `analizar_codigo` `:3793-3808`: `_absoluta('\\.')` en Windows es la raíz de la unidad, que CONTIENE la raíz (`:453-455`, `:538-540`) | PASA, por `_test_de_un_clon` |
| c2 | el mismo test en el repo, con Windows simulado | PASA | — | exención de `tests/` | PASA |

La simulación: `medir_g1.py` cambia `_absoluta` para que `\.` dé un directorio que contiene el repo
(lo que en Windows es `C:\`). En el repo no salta (c2) porque `tests/` está exento: K3 es K2. **No
propongo tocar `analizar_codigo`**: en código sin revisar, `\.` y `/` SON la raíz de la unidad si
se usan como ruta, y la guardia no distingue un separador de regex de una ruta. El encargo cita
`SOLO_WINDOWS` y «el monkeypatch de os.name / canonización» de `test_guardia_alias.py:39-42`: ahí
están `EN_WINDOWS` y `SOLO_WINDOWS`, que es un `skipif`, no un monkeypatch; lo que se simula en ese
fichero es `_canonica` (`_romper`, `:71-105`). En los tests de esta rama se simula `_absoluta` igual,
y lo que solo se pueda ver en Windows de verdad va con `SOLO_WINDOWS` (§1.i).

### 1.d K4: un patrón entre comillas con `=`

| Caso | Comando | Hoy | Linux/Windows | Decide | Propuesta |
|---|---|---|---|---|---|
| d1 | `grep -n "HUSO_CORTE =" src/botsito/x.py` | PASA | — | — | PASA |
| d2 | `grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py` | NIEGA «leer el contenido de .» | **Linux también**, con material en el repo (el sintético lo tiene; el de la nube no) | `candidatos_de_ruta` `:1278-1279` → `_absoluta('')` `:1176` → la raíz, recursiva | PASA |
| d3 | el comando entero de BARRIDO-SESION-6.md §2.1 (`…; grep -rln "huso_corte" knowledge/cuentas \| head -3`) | NIEGA, mismo motivo | Linux | idem (el primer `grep`) | PASA |
| d4 | `grep -n "Puntos = " src/botsito/x.py` | PASA | — | — | PASA |
| d5 | `grep -rn "^Puntos\|Puntos = " src/botsito/*.py \| head -3` | NIEGA «leer el contenido de  .» (dos espacios) | Linux también | `:1278-1279` → `' '` → `_absoluta` hace `strip()` → la raíz | PASA |
| d6 | `grep -rn --include=*.py` con cuatro `-e`, uno `"a21="` | NIEGA «leer el contenido de .» | Linux también | `:1278-1279` sobre `a21=` → `''` | PASA |
| d7 | el mismo con dos `-e` (sin `a21=`) | PASA | — | — | PASA |
| d7b | `grep -rn " " src/` (el patrón ES un espacio) | NIEGA «leer el contenido de  .» | Linux también | `_absoluta(' ')` → la raíz | ver decisión 4 |
| d8, d9 | `--exclude-dir=<holdout>`, `cat --x=<fichero del holdout>` | NIEGA | Linux | `:1278-1279` (lo que sí tiene que seguir) | NIEGA (sin cambio) |

**Qué lo dispara (encontrado, y se reproduce en Linux).** El AVISO del consultor midió los comandos
SIN `-r` (d1, d4), que pasan. Los de los informes llevaban `-r` (BARRIDO-SESION-6.md :540 y :612;
ACTIVAR-SESION-04-MOTOR.md :1384). `candidatos_de_ruta` da, para cada argumento, también lo que va
detrás del primer `=` (para `--x=ruta`): de `"HUSO_CORTE ="` sale `''`, de `"Puntos = "` sale `' '`,
de `"a21="` sale `''`. `_absoluta` empieza con `ruta.strip()` (`:1176`), así que los dos son el
directorio de trabajo, la raíz del repo; con `-r`, `grep` es recursivo y la raíz se recorre entera
(`motivo_directorio`), y en el portátil de Aleks la primera zona protegida que encuentra es una
captura de `Material adicional` (`R_CAPTURA`). El «.» del mensaje es el punto final de la frase
(`f"leer el contenido de {cand}.\n"` con `cand` vacío, `:1746`); con `' '` salen dos espacios, como
en BARRIDO-SESION-6.md :613. En la nube pasa porque aquí no hay `corpus/` (§0).

**Propuesta: `_candidato_vacio(c) -> bool`.** Lo que sale de partir por `=` no es una ruta si queda
vacío o en blanco (`c.strip() == ""`): `--x=` no nombra ningún fichero, y el patrón de `grep` no es
una ruta. El argumento ENTERO en blanco (d7b) es otra cosa: lo dejo a la decisión 4.

**La sospecha sobre `grep -rln` sobre una carpeta (BARRIDO-SESION-6.md :540-545): no se sostiene.**
`grep -rln "huso_corte" knowledge/cuentas | head -3` solo PASA (f10); la negativa era del primer
`grep` del mismo comando (d3).

### 1.e El hueco prioritario: listar la carpeta madre del holdout

| Caso | Comando o herramienta | Hoy | Decide | Propuesta |
|---|---|---|---|---|
| e1 | `git ls-files knowledge/cases \| grep -v <holdout>` | PASA | `GIT_SUBCOMANDOS` `:2507` («lectores que main deja pasar»): `ls-files` no está en `GIT_QUE_MUESTRA` y sus rutas no se miran | NIEGA |
| e2 | `git ls-files knowledge/cases` | PASA | idem | NIEGA |
| e3 | `git ls-files \| grep caso` (todo el repo) | PASA | idem | NIEGA |
| e4 | `ls -R knowledge/cases` | PASA | `LECTOR_DE_METADATOS` `:959-966` | NIEGA |
| e5 | `ls <holdout>/1` | PASA | idem | NIEGA |
| e6 | `find knowledge/cases -name '*.yaml'` | PASA | `_analizar_find` `:2088-2127` (solo mira `-exec`) | NIEGA |
| e14e | `find . -name '*.py'` (desde la raíz) | PASA | idem | NIEGA (falso positivo aceptado: la forma es `find src tests …`) |
| e7 | `git ls-tree -r --name-only HEAD knowledge/cases` | PASA | `:2507` | NIEGA |
| e14d | `git ls-tree --name-only HEAD <holdout>/1/` | PASA | idem | NIEGA |
| e8 | `tree knowledge` | PASA | `LECTOR_DE_METADATOS` | NIEGA |
| e9 | `du -a knowledge/cases` | PASA | idem | NIEGA |
| e14c | `sha256sum <holdout>/1/*` (el glob imprime los nombres) | PASA | idem | NIEGA |
| e10 | `rg --files knowledge/cases` | NIEGA (como lector recursivo) | `motivo_directorio` | NIEGA |
| e11 | `grep -rl x knowledge/cases` | NIEGA | idem | NIEGA |
| e12 | Glob `knowledge/cases/**/*.yaml` | PASA | `decidir` `:4488-4489` («listar nombres no es abrir (ADR-0021 §1)») | NIEGA |
| e13 | Glob `**/*.yaml` con `path: knowledge/cases` | PASA | idem | NIEGA |
| e19 | Glob `**/*.py` (desde la raíz) | PASA | idem | PASA (no alcanza ningún fichero de `holdout/{1,2,3}`) |
| e14 | PowerShell `Get-ChildItem -Recurse knowledge/cases` | PASA | `analizar_powershell` `:4351-4438` (sin lector, no niega) | NIEGA |
| e14b | PowerShell `Get-ChildItem <holdout>/1` | PASA | idem | NIEGA |
| e15 | `git ls-files <holdout> \| wc -l` | PASA | — | PASA (el recuento) |
| e16 | `git ls-files knowledge/cases/dev knowledge/cases/kit` | PASA | — | PASA (rutas literales que no lo contienen) |
| e17, e18 | `ls knowledge/cases`, `ls <holdout>` (no recursivos) | PASA | — | PASA (nombran `holdout`, `1`, `2`, `3`, `README.md`, no lo de dentro) |
| e20 | `uv run botsito corpus inventory` | PASA | la CLI es la puerta | PASA |

En el repo real, `git ls-files knowledge/cases/holdout | wc -l` da 4 (recuento; la forma que la
lección permite).

**Las dos reglas, contra los ADR.** ADR-0021 §1 dice qué es ABRIR un holdout: leer sus etiquetas o
medir una cifra del bot sobre sus días, «y solo estas dos». ADR-0033 §1, para la guarda de los
tests: «listar nombres (`os.listdir`, `os.scandir`) **no** cuenta», y §4: «las fechas ya están en
`particiones.yaml` para quien las quiera». CLAUDE.md («deja listarlo, medirlo y hashearlo») DESCRIBE
la guardia y está de acuerdo con los dos ADR. La lección de ERRORES-RECURRENTES.md (`:72`, activacion-a42:
«Nunca se lista una carpeta que contiene meses reservados»; `:78`, cases-rejilla: «ni filtrada con
`grep -v`», y (7): pasa a regla de la skill fase-cero; `:80`, la 4.ª vez y «que la guardia lo
niegue es prioritario dentro de G.1») es más estricta que los ADR y **no sale de ningún ADR**: sale
de las órdenes de cierre del consultor y está en la skill `fase-cero` (Límites, «Holdout, sin
excepciones»). **Manda el ADR en lo que dice**: listar no es abrir, y por eso un listado no es una
exposición que declarar. Pero los ADR no dicen que listar esté PERMITIDO como proceso, y negarlo no
bloquea ningún paso que el proceso exija (los recuentos de `kit build` y `casos_reservados` siguen):
no hay contradicción de fondo, hay una regla de proceso sin ADR. CLAUDE.md pide para eso «o se
corrige aquí o se cambia el ADR»: decisión 0.

**Propuesta: `_lista_nombres_del_holdout(...)`, negando por defecto.** Se niega un comando o
herramienta que IMPRIME NOMBRES de lo que hay dentro de `knowledge/cases/holdout/{1,2,3}/`:
- cuando su alcance es una de esas carpetas o algo de dentro (`ls <holdout>/1`, `git ls-tree HEAD
  <holdout>/1/`, un glob que se expande dentro, `Get-ChildItem <holdout>/1`);
- o una carpeta que las CONTIENE (`knowledge/cases/holdout`, `knowledge/cases`, `knowledge`, la raíz,
  cualquier ancestro) y el listado es recursivo: `ls -R`, `tree`, `find`, `du -a`, `git ls-files`
  (siempre recursivo, también sin rutas), `git ls-tree -r`, `rg --files`, `Get-ChildItem -Recurse`,
  y Glob cuyo patrón, resuelto contra su `path`, alcance un fichero de esas carpetas que no sea su
  `README.md`;
- y se deja pasar si lo único que sale es un RECUENTO: la tubería acaba en `wc` o en `grep -c`.

Los falsos positivos conocidos: `corpus inventory` y `kit build` pasan (la CLI, sin cambio);
`casos_reservados` en código en línea ya lo decide `analizar_codigo` (nombra `knowledge/cases` y
recorre: hoy se niega), sin cambio; `git ls-files` sin rutas y `find .` desde la raíz pasan a negarse
(la forma: rutas literales). **Cambia de sentido**
`tests/unit/test_guardia_claude.py::test_ejecucion_quinta_pasada_admite[git ls-files]` (`:1855`, que
asegura que `git ls-files` sin rutas PASA): con la propuesta, NIEGA, y el test pasa a decir lo
contrario por su nombre; `git ls-tree HEAD` (`:1856`, no recursivo) sigue pasando.

### 1.f El resto de G.1, y lo que encontró el auditor

| Caso | Comando | Hoy | Linux/Windows | Decide | Propuesta |
|---|---|---|---|---|---|
| f1 | (agentes) `git worktree list` | NIEGA «`git worktree` cambia el repositorio» | Linux | `solo_lectura.py:85` (`GIT_LEE`, `:36-41`) | PASA solo `worktree list` |
| f2 | (agentes) `git -C <clon> rev-parse HEAD` | NIEGA «`git <clon>` cambia …» | Linux | `solo_lectura.py:79` (el subcomando es el primer token sin guion: la ruta de `-C`) | PASA |
| f3 | (agentes) `git -c core.quotepath=false log -1` | NIEGA «`git core.quotepath=false` …» | Linux | `:79` | PASA en `solo_lectura` (que solo mira la escritura); la guardia lo sigue negando (f3b) |
| f3b | (guardia) `git -c core.quotepath=false log -1` | NIEGA «clave fuera de la lista cerrada» | Linux | `guardia.py:1806-1816` (`GIT_C_CLAVES`, vacía) | sin cambio salvo decisión 6 |
| f4 | (agentes) `git tag -l 'stable/F38*'` | NIEGA «`git tag` cambia …» | Linux | `solo_lectura.py:85` | PASA (`tag` solo con `-l`/`--list`, o sin argumentos) |
| f4b, f4c | (agentes) `git tag stable/x`, `git -C <clon> commit -m x` | NIEGA | Linux | idem | NIEGA (sin cambio; con la propuesta, por su subcomando real) |
| f5, f6, f7 | (guardia) `git tag -l …`, `git -C <clon> rev-parse`, `git worktree list` | PASA | — | — | PASA |
| f8 | `PYTHONIOENCODING=utf-8 python scripts/de_main.py` | NIEGA «no esta en la lista cerrada (`NOMBRES_DE_ENTORNO`)» | Linux | `:3044-3046`, `:2550-2561` | decisión 5 |
| f9 | `grep -n x PROJECT_STATE.md; uv run botsito state check` | NIEGA «antes, en el mismo comando, va `grep …`» | Linux | `_exigir_lo_de_antes` `:3596-3602` / `_es_preparacion` `:3516-3535` | decisión 6 |
| f9b | `uv run botsito state check …; uv run python <guion> …` (dos ejecuciones; esta sesión, al abrir la rama) | NIEGA | Linux | idem | NIEGA (sin cambio) |
| f10 | `grep -rln "huso_corte" knowledge/cuentas \| head -3` | PASA | — | — | PASA (§1.d) |
| f11 | guion con la ruta LITERAL de un manifiesto de ticks de enero | PASA | — | — | PASA |
| f12 | guion que recorre `Path('data/manifests/ticks').glob('*.yaml')` (carpeta literal) | PASA | — | — | PASA |
| f13 | guion que compone `Path('data') / 'manifests' / 'ticks'` y la recorre | NIEGA «el codigo nombra la carpeta data» | Linux, con `data/visor` y transcripciones en el repo (el sintético las tiene) | `analizar_codigo` `:3799-3808` | NIEGA (sin cambio: es C) |
| f14 | Read del manifiesto | PASA | — | — | PASA |
| f15 | `which python python3` (esta sesión, al empezar) | NIEGA «`which` lanza `python`» | Linux | `which` no está en `NO_EJECUTAN` (`:2437-2489`) → `_ejecucion_de_un_programa_desconocido` `:3132-3141` | PASA (decisión 7) |
| f16 | `rm x.txt && rmdir vacio` | NIEGA «antes … va `rm x.txt`» | Linux | `rmdir` no está en `NO_EJECUTAN` → es una ejecución; `rm` delante no es preparación | PASA (decisión 7) |
| f17 | `rmdir vacio` | PASA | — | — | PASA |
| f18 | `grep -rn "HUSO_CORTE =" src/` (la «regla de Analytics sobre src/» de H) | NIEGA «leer el contenido de .» | Linux también | §1.d | PASA |

**El manifiesto de ticks (CORRIDA-CONSTRUCCION.md §1.j; VISOR-CONSTRUCCION.md h8).** La ruta
literal de un manifiesto pasa (f11), y recorrer la carpeta literal también (f12). Lo que negó la
guardia era un guion que COMPONÍA la ruta desde `data` (f13: «el codigo nombra la carpeta data»;
`data` contiene `data/visor` y transcripciones en cuarentena). La propuesta de CORRIDA-CONSTRUCCION
(«que admita las rutas literales») ya se cumple; no hay que tocar nada, y la composición es C.

**Las dos negativas del diagnóstico de H que van a K** (las declaró el consultor el 2026-10-31; no
están escritas en el repo, así que las mido por su forma): el `grep -r` sobre `src/` «por la regla
de Analytics» es K4 (f18, mismo disparador); el `rm` encadenado con `rmdir` es f16. Las dos se
arreglan con las propuestas de 1.d y de la decisión 7.

### 1.g B: lo que el guion importa o ejecuta

| Caso | Guion (que ejecuta `trabajo/mod_malo.py`, que imprime el fichero falso del holdout) | Hoy |
|---|---|---|
| g0 | control: `mod_malo.py` directo | NIEGA «el codigo nombra <tmp>/…/secreto.yaml» |
| g1 | `sys.path.insert(0, 'trabajo'); import mod_malo` | PASA |
| g2 | `import mod_malo` (en la misma carpeta que el guion) | PASA |
| g3 | `runpy.run_path('trabajo/mod_malo.py')` | PASA |
| g4 | `exec(open('trabajo/mod_malo.py').read())` | PASA |
| g5 | `subprocess.run(['python', 'trabajo/mod_malo.py'])` | PASA |
| g6 | `importlib.import_module('mod_malo')` | PASA |
| g7 | `cd trabajo && python -c "import mod_malo"` (en línea) | PASA |
| g8 | `python -c "import runpy; runpy.run_path('trabajo/mod_malo.py')"` | PASA |
| g9 | `from botsito.cases.holdout import casos_reservados` (el paquete instalado) | PASA |

Decide `_exigir_guion_legible` → `analizar_codigo` (`:3780-3815`): lee el texto del guion y sus
literales, nunca lo que el guion carga.

**Cómo se resuelve hoy un import local** (lo que haría Python): `python <guion>` pone en
`sys.path[0]` la carpeta del guion; `python -c` y `python -` ponen `''` (el directorio de trabajo);
después van las rutas que el guion añade (`sys.path.insert`), la biblioteca estándar y el
`site-packages` del entorno, donde `botsito` está instalado editable (apunta a `src/`, código del
repo). `PYTHONPATH` no puede ir delante (no está en `NOMBRES_DE_ENTORNO`).

**Propuesta: `_lo_que_carga(codigo, ruta_del_guion, ctx)`, negando por defecto, solo para Python.**
- Se RESUELVEN y se leen (y se analizan como el guion, recursivo hasta 3 niveles; el cuarto se niega):
  `import x` / `from x import` / `importlib.import_module('literal')` / `runpy.run_module('literal')`
  cuyo módulo cae en un fichero de la carpeta del guion (o del directorio de trabajo con `-c`), de
  una ruta LITERAL añadida a `sys.path`, o del repo; `runpy.run_path('literal')`,
  `exec(open('literal').read())` y `exec(compile(open('literal')…))` por su ruta; el código literal
  de `exec('…')`/`eval('…')`.
- Se dejan como hoy: la biblioteca estándar y los paquetes de terceros del entorno (no son código de
  la rama), y `botsito.*` (el paquete del proyecto: lo mismo que `uv run botsito …`, que ya pasa sin
  leer `src/`; el blob de main no se mira tampoco ahí).
- Se NIEGA lo que no se puede resolver: `importlib.import_module`, `__import__`, `runpy.*`, `exec`,
  `eval`, `compile` con un argumento que no es literal; un módulo local que no existe al inspeccionar;
  `sys.path` cambiado con un valor no literal.
- `subprocess`, `os.system`, `os.popen`, `os.exec*`, `os.spawn*`, `Popen`: si el programa es un
  literal, la orden se monta con sus literales y se analiza como un comando de Bash (con sus partes no
  literales como «se construye al ejecutarse»); si el programa no es literal, o es un intérprete o un
  shell cuyo guion no es literal, se niega (decisión 2).
- Otros lenguajes (`node`, `perl`…): sin cambio, riesgo residual declarado (no hay ninguno en
  `scripts/` ni en los 503 comandos medidos de GUION-MISMO-COMANDO).

### 1.h C: las rutas compuestas

| Caso | Forma | Hoy |
|---|---|---|
| h5-joinpath | `Path('.').joinpath('knowledge', 'cases', '<holdout>', '1', 'secreto.yaml')` | PASA |
| h5-os-path-join | `os.path.join(…)` con las mismas partes | PASA |
| h5-barra | `Path('knowledge') / 'cases' / … / 'secreto.yaml'` | PASA |
| h5-fstring | `f'knowledge/cases/{zona}/1/secreto.yaml'` | NIEGA «nombra la carpeta knowledge/cases/» (por casualidad: el trozo literal `knowledge/cases/` es una carpeta de una zona) |
| h5-fstring-partes | `f'{a}/{b}/<holdout>/1/secreto.yaml'` | PASA |
| h5-concatenacion | `'knowledge' + '/' + 'cases' + '/<holdout>/1/secreto.yaml'` | PASA |
| h6-llaves | `cat 'knowledge/cases/'{<holdout>,dev}'/1/secreto.yaml'` | PASA |
| h7-url-file | `urlopen('file://<ruta absoluta del fichero falso>')` en un guion | PASA |
| h7b | `curl file://<ruta absoluta>` | PASA |
| h8 | `subprocess.run(['g' + 'h', 'run', 'view', '1'])` (la consulta de CI a trozos) | PASA |

Decide `analizar_codigo` (`:3780-3815`): mira cada literal ENTERO como ruta, y lo compuesto solo
cuando el código además recorre directorios. En Bash, `resolver` no expande las llaves que no van
en la cabeza del comando (`:1540-1552` solo mira el programa), y `curl` está en
`SIN_LECTURA_DE_RUTAS` (`:969`, solo mira su `@fichero`).

**La cifra de falsos positivos de la condición propuesta, sobre `main`**
(`docs/validation/anexos/GUARDIA-G1/contar_c.py`; salida, `contar_c-FASE0.txt`, con la lista por
fichero): de los 203 guiones `.py` de `scripts/` y `tests/` de `main`,
- variante ANCHA (el texto nombra un fragmento de `SENSIBLES` y el guion compone rutas en cualquier
  sitio): **96** (20 de `scripts/`, 76 de `tests/`);
- variante ESTRECHA (el fragmento sensible está en un texto que forma parte de la composición misma:
  un argumento de `joinpath`/`os.path.join`, un lado de `/` o `+`, una parte de un f-string): **44**
  (7 de `scripts/`: `a18_buscar.py`, `a35_fotogramas.py`, `buscar_ambiguedades.py`,
  `orden_stop_o_limite.py`, `transcribir_sesion.py`, `v5_criterio.py`, `viabilidad_trader.py`; 37 de
  `tests/`).

Ninguno de esos se niega HOY al ejecutarlo: los de `main` son código revisado (`_igual_que_en_main`)
y los de `tests/` están exentos. La condición solo los negaría cambiados en una rama, copiados a la
carpeta de trabajo o en un clon (que con `_test_de_un_clon` pasa si es idéntico). Es el coste para el
código NUEVO que se parezca a ellos.

**Propuesta: `_compone_ruta_sensible(codigo)`, negando por defecto**, en código Python que se parsea:
una composición (`joinpath`, `os.path.join`, `/` con un texto, `+` con un texto, un f-string con
partes) que tenga un fragmento de `SENSIBLES` en uno de sus textos (la variante ESTRECHA), O cuyo
resultado no se pueda calcular y que esté en un guion que nombre un fragmento sensible en cualquier
sitio y abra ficheros (la ANCHA, recortada a los que abren). Primero se intenta CALCULAR: si todas
las partes son literales (o variables asignadas una sola vez a un literal, como h5-fstring-partes),
la ruta se compone y se mira como un literal más (`motivo_fichero`/`motivo_ruta`): así h5-* se niegan
por su motivo real y una composición inocua (`Path('docs') / 'a.md'`) pasa. Lo que no se pueda
calcular y nombre algo sensible, se niega. En shell: las llaves que componen una ruta se EXPANDEN
(bash lo hace antes de ejecutar) y cada resultado se mira; `file://` (en `curl` y en un literal de
código) se lee como la ruta que nombra. La consulta de CI a trozos (h8) es la misma familia: con el
cálculo de las partes, `'g' + 'h'` es `gh` y lo decide la regla de la CI que ya hay.

### 1.i Lo que solo se puede ver en Windows, para Aleks con «!»

Lo de Windows se simula en los tests (como `_romper` de `test_guardia_alias.py`) y, donde la
simulación no llega, va con `SOLO_WINDOWS`. Para el portátil, después de la fase 1, desde la raíz
del repo y con la rama ya traída (`git fetch origin trabajo/guardia-g1`):

1. K3 de verdad (`\.` como raíz de la unidad), en un clon desechable:

```bash
git worktree add --detach C:/cm/g1 trabajo/guardia-g1
```

```bash
cd C:/cm/g1 && uv run pytest tests/unit/test_guardia_g1.py -q
```

   Antes de la rama: la guardia lo niega («el codigo nombra la carpeta \.» si el test lleva la
   constante); con la rama: pasa. Después, `git worktree remove --force C:/cm/g1` y `git worktree prune`.

2. K4 de verdad (con `corpus/` en el portátil), en la sesión de Claude Code de Aleks, pidiendo a
   Claude que lance:

```bash
grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py
```

   Con main: «leer el contenido de .»; con la rama: pasa.

3. El espacio final que Windows quita al abrir (`GetFullPathNameW`): `grep -rn " " src/botsito/x.py`
   (d7b), con la rama, según la decisión 4.

### 1.j Artifact, ArtifactData, DesignSync y claude-in-chrome

Hoy están en `permissions.deny` de `.claude/settings.json` (las cuatro de claude-in-chrome:
`file_upload`, `navigate`, `get_page_text`, `read_page`), y el `matcher` del hook es
`Read|Grep|Glob|Bash|PowerShell|Monitor`. Para mirarlas como un Read haría falta: (1) añadirlas al
`matcher` (cambia `.claude/settings.json`, que el encargo deja fuera salvo PARADA); (2) saber el
esquema de entrada de cada una en la versión de Claude Code de Aleks (qué campo lleva una ruta local:
`file_upload` lleva rutas; `navigate` una URL que puede ser `file://`; `get_page_text` y `read_page`
leen la página abierta, que puede ser un `file://` abierto antes); (3) una función por herramienta
que lleve sus rutas a `motivo_fichero`, y negar la entrada que no se reconozca (como `R_MONITOR`).
**No cabe en esta rama**: pide tocar `settings.json` y un esquema que no se puede medir aquí.
**Y un hallazgo de esta sesión**: en la nube hay herramientas que leen un fichero LOCAL por su ruta y
no están ni en `deny` ni en el `matcher`: `mcp__claude-artifacts__publish_files` (`files[].path`, «sus
bytes no pasan por ti»), y las de GitHub que suben contenido (`push_files`, `create_or_update_file`,
que llevan el contenido en la entrada, no una ruta). La primera es un hueco de la misma familia que j.
Texto propuesto para Technical Debt: «La guardia no mira las herramientas que leen un fichero local
fuera de Read/Grep/Glob/Bash/PowerShell/Monitor: Artifact, ArtifactData, DesignSync y cuatro de
claude-in-chrome están cerradas en `permissions.deny`; `mcp__claude-artifacts__publish_files` (en la
nube) no está ni en `deny` ni en el `matcher` (GUARDIA-G1.md §1.j). Rama propia: añadirlas al
`matcher` con su esquema y llevar sus rutas a `motivo_fichero`, negando la entrada que no se
reconozca.»

## 2. El encargo frente al repo (subagente auditor-encargo, 2026-11-04)

Lo que cambia lo que se pide va a «Lo que necesito que decidas»: e) sin ADR (decisión 0), el patrón
de Windows que no simula (§1.c), el ejemplo de K2 que deja fuera el test de la rama (decisión 3), lo
encadenado y `git -c` como reglas decididas (decisión 6), y las contradicciones del encargo con el
contrato (decisión 12). Dos matices del auditor que la medida de esta sesión precisa: #15 (el lector
de `main` pasa hoy; el caso de test es el lector CAMBIADO, a1) y #26 (sus medidas sobre el repo REAL
de la nube pasan porque aquí no hay `corpus/`; en el repo sintético, con material, los comandos con
`-r` se niegan: §1.d). Su informe, tal cual:

> **Auditoría del encargo · trabajo/guardia-g1 · 2026-11-04**
>
> Resumen: 52 afirmaciones; 33 correctas, 3 incorrectas, 16 con matiz. 9 herencias no recogidas, más 4 contradicciones internas del encargo o del contrato.
>
> Encargo auditado: `docs/encargos/trabajo-guardia-g1.md`. Las medidas en memoria las hice con `decidir()` de `.claude/hooks/guardia.py` y con `solo_lectura.motivo()` sobre el repo real, sin ejecutar ningún comando y sin nombrar material protegido.
>
> **Afirmaciones**
>
> | # | Afirmación (literal del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | «desde main en 7a3a1ff (el commit de estado sobre el merge 796be27, que es al que apunta el tag stable/F38k-margen-pendiente)» | CORRECTA | `git rev-parse main origin/main` da 7a3a1ff2…, y `git rev-list -n1 stable/F38k-margen-pendiente` da 796be27. |
> | 2 | Ese tag es el último stable y está en origin | CORRECTA | `git tag -l 'stable/*' --sort=-creatordate` lo da el primero. `git ls-remote --tags origin` da `refs/tags/stable/F38k-margen-pendiente^{}` = 796be27. |
> | 3 | «CI de main run 41258026188» en success | CORRECTA | `gh run view 41258026188` da `conclusion: success`, `headBranch: main`, `headSha: 7a3a1ff2…`. |
> | 4 | «no hay otra rama abierta» | MATIZ | En local existe `claude/festive-darwin-lg9p31`. Apunta a 7a3a1ff, es ancestro de main y no está en origin (`git ls-remote --heads origin` solo da main). Es la rama del arnés de la nube y conviene decirlo en la apertura. |
> | 5 | «Tag de cierre: stable/F38l-guardia-g1» | CORRECTA | Sigue la serie: F38k es el último. |
> | 6 | La orden del hook es `PYTHONUTF8=1 python "$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py"` | CORRECTA | `.claude/settings.json:80`, con el matcher `Read\|Grep\|Glob\|Bash\|PowerShell\|Monitor` (:76). En esta sesión el hook corre: me bloqueó tres comandos (lo explico en «Lo que no pude comprobar»). |
> | 7 | «la CI de main corre make check entero sin data/, ci.yml:28, así que make check sella igual aquí» | MATIZ | `ci.yml:28` es `make check`. Pero la CI instala ffmpeg (:24) y exige ffprobe (`BOTSITO_EXIGE_FFPROBE: "1"`, :18). Si aquí no hay ffprobe, los tests de vídeo se omiten en vez de fallar, así que no es «igual». Además `data/` existe en el clon: lleva `data/manifests/`, que se sigue en git (`.gitignore:3-4`). |
> | 8 | «_decide y _bash, hacia :127-134» de test_guardia_claude.py | CORRECTA | `tests/unit/test_guardia_claude.py:127-134`. |
> | 9 | «G.1 lleva desde el 2026-10-11 acumulando falsos positivos … y un hueco prioritario» | CORRECTA | `docs/plan/HOJA-DE-RUTA.md:526-528`: «Prioritario dentro de G.1 (consultor, 2026-10-11)». |
> | 10 | «K dice «rama propia, junto a B o C si cabe»» | CORRECTA | `PROJECT_STATE.md:48`. |
> | 11 | «NA:K, NA:B y NA:C; carril G.1 de la hoja de ruta» | MATIZ | Las `Refs` de G.1 son `NA:B · NA:C · NA:D · NA:K` (`HOJA-DE-RUTA.md:523`). D se queda fuera (lo dice el encargo), así que G.1 no puede pasar a HECHA en el cierre. |
> | 12 | «CRUDO_PYTHON (.claude/hooks/guardia.py:195)» | CORRECTA | `guardia.py:195`. |
> | 13 | «casa con `crudo = ruta.read_bytes()` de scripts/leer_demo_ftmo.py (hoy :107)» | CORRECTA | `scripts/leer_demo_ftmo.py:107`. |
> | 14 | «(DEMO-EJECUCION-1.md §3.3 y su revisor, a1)» | CORRECTA | §3.3 en `DEMO-EJECUCION-1.md:530`, el pasaje en :578-590 y a1 en :666. |
> | 15 | «hoy la comprobación del contrato de esa rama no se puede ejecutar» | MATIZ | Hoy sí se puede: el lector es idéntico al de main y la guardia lo da por revisado (`_igual_que_en_main`, `guardia.py:3672`). Lo medí: `decidir("uv run python scripts/leer_demo_ftmo.py")` da `None`. El falso positivo solo salta cuando el guion difiere de main o está en un clon (`DEMO-EJECUCION-1.md:585-586`). El caso de test tiene que montar esa condición. |
> | 16 | «dos guiones más de la carpeta de trabajo (prevision.py en MARGEN-PENDIENTE.md :380 y :421; EA-CONEXION.md :437 y :547)» | MATIZ | Las líneas son correctas, pero (a) los guiones no están en el repo: solo queda descrita su línea (`MARGEN-PENDIENTE.md:421`, `crudo = ORIGEN.read_text(…)`). (b) Hay un tercer caso: la sonda de `BARRIDO-SESION-6.md:691` («La sonda del guion con una variable `crudo`: PARADA»). Allí la decisión 6 del consultor (:470) dice que la guardia caza `crudo = …`, `crudo=None` y `"crudo": …`. |
> | 17 | «La regla va contra el corpus sin filtrar (la opción de la CLI y su equivalente en Python, CLAUDE.md «Las guardias de Claude Code»)» | CORRECTA | En CLAUDE.md, «La CLI ensena el corpus filtrado… La opción que lo enseña todo es solo de Aleks»; también `R_CRUDO`, `guardia.py:186-191`. La regla sale del encargo de `trabajo/cuarentena-por-defecto` (decisión del consultor), no de un ADR. |
> | 18 | «el parámetro de las funciones de cuarentena.py» | MATIZ | `src/botsito/corpus/cuarentena.py:21` dice que el contenido sin filtrar se pide con ese parámetro. No pude listar sus firmas: la guardia me negó el grep (ver «Lo que no pude comprobar»). |
> | 19 | K2: la guardia niega pytest sobre los tests de un clon en C:/cm/ (ENTRADA-JULIO.md §8) | CORRECTA | `ENTRADA-JULIO.md:668` es §8. Mecanismo: la exención de `tests/` exige ruta relativa a la raíz real (`guardia.py:2202`). En un clon, `relativa()` da None, el fichero pasa a guion y se analiza (`:3671-3690`). |
> | 20 | «ACTIVAR-SESION-05.md §0.f: test_kit.py, test_selector_orden_stop.py y test_renovar_cierres.py» | CORRECTA | `ACTIVAR-SESION-05.md:471-475` (motivos en :147). |
> | 21 | «ACTIVAR-SESION-05-MOTOR.md §0.d: pytest desde C:/cm/ y las dos ejecuciones encadenadas» | MATIZ | Está en `:235-241`. Pero la encadenada (`spec manifest --escribir` y `spec check` en una llamada) no es un falso positivo: es la regla «dos ejecuciones en un comando» aceptada en `trabajo/guion-mismo-comando` (caso `f1-dos`, `GUION-MISMO-COMANDO.md:358`). Abrirla choca con «sin aflojar ninguna regla que hoy funciona». La entrada K la incluye igual (`PROJECT_STATE.md:48`). |
> | 22 | «propón la condición (por ejemplo, que el fichero sea byte a byte el de main del repo real…)» | MATIZ | Con ese ejemplo no se cubre el uso para el que existe el clon. La skill `comparar-con-main` prueba un test «con el código de main» copiando el test DE LA RAMA dentro del clon (`.claude/skills/comparar-con-main/SKILL.md:66-68`). Ese test, por definición, no es el de main. Es lo que pasó en K3: el fichero del clon era la copia de la rama (`:131` frente a `:133`, `CUARENTENA-POR-CONDICION-2.md:548-549`). |
> | 23 | K3: «la constante `\.` de un f-string … que la guardia lee como «la carpeta \.»» (CUARENTENA-POR-CONDICION-2.md §2.e) | CORRECTA | `CUARENTENA-POR-CONDICION-2.md:543-553`; el mensaje sale de `guardia.py:3804-3807`. |
> | 24 | K4: «un grep con un patrón entre comillas que acaba en espacio («leer el contenido de .», BARRIDO-SESION-6.md §4: `"HUSO_CORTE ="` y `"Puntos = "`)» | CORRECTA | `BARRIDO-SESION-6.md:693-694`. |
> | 25 | «ACTIVAR-SESION-04-MOTOR.md (grep -rn --include=*.py con cuatro -e … se bloquea y con dos -e pasa)» | CORRECTA | `ACTIVAR-SESION-04-MOTOR.md:1384`; `HOJA-DE-RUTA.md:537-539`. |
> | 26 | AVISO: «`grep -n "HUSO_CORTE =" src/botsito/x.py`, `grep -n "Puntos = " src/botsito/x.py` y el grep con cuatro -e PASAN» | MATIZ | Lo que midió el consultor no son los comandos negados. Los literales eran: `grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py; grep -rln "huso_corte" knowledge/cuentas \| head -3` (`BARRIDO-SESION-6.md:540`) y `grep -rn "^Puntos\|Puntos = " src/botsito/domain/*.py \| head -3` (:612), con `-r`, un glob y un segundo grep encadenado. Los medí con `decidir()` sobre el repo REAL en Linux y PASAN los ocho (los dos literales, sus formas reducidas y el de cuatro y dos `-e`). La conclusión «no se reproduce en Linux» se sostiene, pero ahora con los literales. |
> | 27 | «guardia.py:2507 deja pasar ls-files a propósito («lectores que main deja pasar»)» | MATIZ | La cita está en `:2504` («Lectores y operaciones corrientes que `main` deja pasar») y `ls-files` en `:2507`. Es la lista cerrada de subcomandos de git de la regla de EJECUCIÓN (revisor, quinta pasada, B5). No es la decisión de dejar listar el holdout. Esa decisión es la política general: `guardia.py:11` («Se puede listar, medir y hashear») y `:4489` (Glob: «listar nombres no es abrir (ADR-0021 §1)»). Quitar `ls-files` de esa lista negaría todo `git ls-files`. |
> | 28 | «test_guardia_claude.py:1855 ASEGURA que pasa: ese test cambia de sentido» | MATIZ | El test asegura que pasa `"git ls-files"` a secas, sin ruta ni filtro (`:1855`, dentro de `test_ejecucion_quinta_pasada_admite`). No toca `knowledge/cases \| grep`. Solo cambia de sentido si la condición niega también el listado sin filtro de la raíz (que «imprime nombres» del holdout). Si no, no cambia y hace falta un test nuevo. |
> | 29 | ERRORES-RECURRENTES lo prohíbe en «(1) Nunca se lista una carpeta que contiene meses reservados…» de las filas de activacion-a42, cases-rejilla («ni filtrada con grep -v») y entorno-code («4.ª vez»), hacia :72-80 | MATIZ | La lección (1) está en `:72` (activacion-a42) y en `:78` (cases-rejilla, «ni filtrada con `grep -v`»). En `:80` (entorno-code) no hay lección (1): hay «una nota para G.1: es la 4.a vez…». La misma regla vive en la skill `fase-cero` (`.claude/skills/fase-cero/SKILL.md:30-32`), que no se cita. |
> | 30 | «CLAUDE.md dice que la guardia «deja listarlo, medirlo y hashearlo»» | CORRECTA | CLAUDE.md, «Las guardias de Claude Code», primer párrafo. También el mensaje `COMO_REESCRIBIR` de la guardia, que manda usar `ls` sobre el material protegido (`guardia.py:219-223`). |
> | 31 | «contrasta las dos contra ADR-0021 y ADR-0033 y di cuál manda» | MATIZ (lo que el repo ya dice) | El único ADR que habla de listar es `docs/adr/0033-la-guarda-y-la-puerta-del-holdout.md:17`: «listar nombres (`os.listdir`, `os.scandir`) **no** cuenta». ADR-0021 §1 define abrir como leer etiquetas o medir (`0021-…md:15-16`). Ningún ADR prohíbe listar (grep de «listar\|listado» en `docs/adr/`: solo 0033:17 y 0015). La lección de ERRORES-RECURRENTES y la de fase-cero son más estrictas que el ADR. Según CLAUDE.md («Una prohibición escrita aquí que no salga de un ADR se revisa contra el ADR»), negar exige un ADR o corregir la lección, y `docs/adr/` está en `rutas_protegidas` del contrato. |
> | 32 | «la consulta de CI … [Technical Debt la asigna a C]» y «las llaves de bash … y las URL file:/// (GUARDIA-ALIAS.md §9, b6 y b7, «van con la deuda C»)» | MATIZ | b6 y b7 están en §9 (`GUARDIA-ALIAS.md:768-769`). «van con la deuda C» está en §11.4 (`:913`) y en el texto entero de HISTORIA (`docs/state/HISTORIA.md:14242`). La deuda de la CI a trozos no se asigna a C: dice «Para el carril de guardias» (`HISTORIA.md:14228`). La une a C el encargo («la misma familia»). |
> | 33 | «GUARDIA-CI.md §5.2 y §9» | CORRECTA | §5.2 en `GUARDIA-CI.md:852` y §9 en `:1108`. |
> | 34 | «analizar_codigo (guardia.py:3780) solo mira literales enteros» | CORRECTA | `guardia.py:3780-3815`: `_literales` vía `ast.Constant` (:3818-3830); lo compuesto solo se niega si además recorre (:3809). |
> | 35 | «SENSIBLES, :3765» | CORRECTA | `guardia.py:3765-3777`. |
> | 36 | «GUION-MISMO-COMANDO.md §1.5, los seis casos h5-*» | CORRECTA | `GUION-MISMO-COMANDO.md:385-400`: joinpath, os.path.join, barra, fstring, fstring-partes y concatenación. Cinco pasan y uno se niega. |
> | 37 | «el método de GUION-MISMO-COMANDO.md §1.4 (docs/validation/anexos/GUION-MISMO-COMANDO/medir_huecos.py…)» | CORRECTA | §1.4 en `:347`; el guion existe en el anexo. |
> | 38 | B: «GUION-MISMO-COMANDO.md §0.c: import de un módulo local, runpy, exec(open(…)), subprocess» | CORRECTA | `GUION-MISMO-COMANDO.md:95-100`; `PROJECT_STATE.md:25`. |
> | 39 | «D (… GUION-MISMO-COMANDO.md §1.26) NO entra» | CORRECTA | `PROJECT_STATE.md:29`; `GUION-MISMO-COMANDO.md:1393-1430`. |
> | 40 | solo_lectura.py niega `git worktree list` | CORRECTA | Medido: `motivo('git worktree list')` da «`git worktree` cambia el repositorio…» (`worktree` no está en `GIT_LEE`, `solo_lectura.py:36-41`). La guardia principal lo deja pasar (`decidir` da None). |
> | 41 | «toma como subcomando el primer token sin guion (solo_lectura.py:80)» | MATIZ | Está en `:79`. La línea 80 es `ramas_que_leen`. |
> | 42 | «niega `git -C <clon> rev-parse` y `git -c k=v …` (ACTIVAR-SESION-05-MOTOR.md, revisor, hacia :1024)» | MATIZ | En solo_lectura las dos se niegan (medido: «`git /tmp/cm/main` cambia…», «`git core.quotepath=false` cambia…»). El revisor (`ACTIVAR-SESION-05-MOTOR.md:1023-1024`) solo nombra `-C` y `worktree list`. Y `git -c clave=valor` lo niega también, A PROPÓSITO, la guardia principal: «clave fuera de la lista cerrada», `GIT_C_CLAVES` vacía, «§1.27 punto 1, opción B» (`guardia.py:2516-2518`, medido). Arreglar solo_lectura no lo abre para la sesión, y abrirlo en guardia.py afloja una regla decidida. |
> | 43 | «`git tag -l stable/F38*` negado porque tag no está en GIT_LEE (GUARDIA-CI.md H11, hacia :289-291)» | CORRECTA | `GUARDIA-CI.md:289-291`. Medido: solo_lectura lo niega y la guardia principal lo deja pasar. |
> | 44 | «`PYTHONIOENCODING=utf-8 python …` negado por no estar en NOMBRES_DE_ENTORNO» | CORRECTA | `guardia.py:2550-2561`; medido con `decidir`. |
> | 45 | «el encadenado `grep …; uv run botsito state check` (BARRIDO-SESION-6.md §4, :688-691)» | MATIZ | Está en `:688-689`. No es un falso positivo: es la lista cerrada «lo de delante» aceptada en guion-mismo-comando. Lo dice `GUION-MISMO-COMANDO.md:369-381` («Ninguno es un fallo de la guardia: es la lista cerrada tal como se aceptó»; `grep` 9 casos). Medido: «antes, en el mismo comando, va `grep …`». |
> | 46 | «la sospecha sobre `grep -rln` sobre una carpeta (BARRIDO-SESION-6.md :540-545)» | CORRECTA | `BARRIDO-SESION-6.md:540-545`. |
> | 47 | «niega un guion … que nombre data/manifests/ticks/<manifiesto>.yaml … (CORRIDA-CONSTRUCCION.md §1.j; también VISOR-CONSTRUCCION.md :292, h8)» | MATIZ | Lo negado (`CORRIDA-CONSTRUCCION.md:374-379`) fue un guion que nombraba la CARPETA `data/manifests/ticks` («el codigo nombra la carpeta data»). No consta que se negara un fichero literal `<manifiesto>.yaml`: eso es la propuesta. h8 está bien (`VISOR-CONSTRUCCION.md:292`). |
> | 48 | «la negativa a ejecutar, en un clon …, un test de main que lleve el literal de la opción (ENTORNO-CODE.md, G.1)» | CORRECTA | `ENTORNO-CODE.md:729-731` (§6, que cita §4.5); `HOJA-DE-RUTA.md:533-535`. |
> | 49 | «SOLO_WINDOWS y el monkeypatch de os.name / canonización de tests/unit/test_guardia_alias.py (:39-42); úsalo» | INCORRECTA | `SOLO_WINDOWS` (`:40-42`) es un `skipif`: en Linux el test se OMITE, no simula Windows. En ningún test de la guardia hay un monkeypatch de `os.name` (grep de `os\.name\|ntpath` en `tests/unit/test_guardia*.py`: solo `test_guardia_ci.py:141`, que lo lee). Lo que se parchea son funciones de la guardia (`_canonica`, `_unidad_completa` :697, `_realpath` :735), y esos tests también van con `@SOLO_WINDOWS` (:677, :716). La guardia decide por `os.name` en `:1151`, `:1248` y `:1270`. Con ese patrón, los tests de K2 y K3 no correrían en la nube y sus «rotos a propósito» no se pueden enseñar desde aquí. |
> | 50 | j: «Technical Debt: hoy cerradas en permissions.deny; «junto a K»» | MATIZ | La línea está en `PROJECT_STATE.md:103` y el deny en `.claude/settings.json:52-58`. Pero el «junto a K (el alias de la raíz)» se escribió cuando K era el alias de la raíz (`HISTORIA.md`, archivos hacia :12150-12300: «K. PRIORITARIA … el alias de la raíz»), que cerró `stable/F38c-guardia-alias`. El puntero de la deuda está caducado; la K de hoy es otra. |
> | 51 | «PROJECT_STATE está en 21.784 bytes» | CORRECTA | `git show main:PROJECT_STATE.md \| wc -c` da 21784 (en la rama, 21814). |
> | 52 | Fase 3: «las dos negativas del diagnóstico de H que van a K (grep -r sobre src/ por la regla de Analytics… y rm encadenado con rmdir; las declaró el consultor el 2026-10-31)» | INCORRECTA (sin soporte en el repo) | `grep -rln rmdir docs/` solo da el propio encargo. La «regla de Analytics» solo sale en `BARRIDO-SESION-6.md:541,613`, que es la rama del barrido, no la de H. `RESPALDO-M1.md:879-881` enumera sus negativas (`grep -r` sin ruta, `pytest` sobre un directorio, …) y no trae `rmdir`. Si vienen del chat del consultor, el encargo tiene que copiarlas literales. |
>
> (Además, la #49 es la tercera INCORRECTA del recuento; las otras dos son la #52 y la contradicción de la fila 1 de la tabla siguiente, que el encargo afirma en QUÉ NO CAMBIA.)
>
> **Lo que el repo pide y el encargo no recoge**
>
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | 1 | Contradicción interna: QUÉ NO CAMBIA excluye «la de la CI», «la cuarentena» y «el alias de la raíz». Sin embargo h) mete la CI a trozos (regla de la CI), a) cambia `CRUDO_PYTHON` (regla de la cuarentena, `R_CRUDO`), y K3 (`\.` como raíz de unidad) y b6 (llaves) caen en la canonización de guardia-alias. | encargo:19 frente a :31, :33 y :38 | `guardia.py:186-196`; `HISTORIA.md:14242` |
> | 2 | Contradicción interna: la fase 3 corrige «CLAUDE.md, runbooks o skills», pero QUÉ NO CAMBIA dice «las skills» y el contrato protege `.claude/skills/`. Los recuadros en informes cerrados de `docs/validation/` y la ampliación de `medir_huecos.py` en su anexo de GUION-MISMO-COMANDO tampoco están en `rutas_permitidas`. | encargo:19, :26 y :50 | `contrato.yaml` (rutas_permitidas y rutas_protegidas) |
> | 3 | G.1 pide además que `cerrar-rama` diga que, si la rama cambia el Makefile, los `make check` los lanza Aleks con «!». El encargo no lo nombra, y las skills están fuera, así que tiene que decir que queda en G.1. | `HOJA-DE-RUTA.md:536-537`; `ENTORNO-CODE.md:737-738` | — |
> | 4 | G.2 dice que `--diagnostico-a47` y `--diagnostico-a27` «se retiran en G.1 o en rama propia». El encargo no lo dice, y `src/` está protegido. | `HOJA-DE-RUTA.md:556-558` | — |
> | 5 | El resto de la deuda de la CI: cliente fuera de la lista (`aiohttp`), espera a nivel de agente (`ScheduleWakeup`, `CronCreate`) y «no lee el código bajo `tests/` que se le pasa a pytest». Lo último toca de lleno a K2, que amplía esa exención. | `HISTORIA.md:14228` | — |
> | 6 | Las demás negativas en el clon de RESPALDO-M1: `pytest` sin rutas fuera de la raíz y `tests/regression` como directorio. Son de la familia K2; el informe las da por regla, no por falso positivo, y el encargo no dice qué hacer con ellas. | `RESPALDO-M1.md:356-358`, `:879-881` | — |
> | 7 | La contradicción entre consultores sobre renombrar `crudo`: `EA-CONEXION.md:547` («renombrar … es lo que pide la deuda K») frente a `DEMO-EJECUCION-1.md:812` («No se renombra la variable: eso sería rodear la guardia»). El encargo no la zanja. | ambos | — |
> | 8 | Si e) niega listar, hay que cambiar en la misma rama el mensaje `COMO_REESCRIBIR` («para el material protegido solo `stat`, `ls`…») y la cabecera de la guardia. Si no, quedan falsos. Y la regla de ERRORES-RECURRENTES abarca «una carpeta que contiene meses reservados» (también `data/`, `data/manifests/`: el auditor de corrida-construccion hizo `git ls-files data/manifests \| grep -c`), no solo la madre del holdout. | `guardia.py:11`, `:219-223`; `CORRIDA-CONSTRUCCION.md:372-373` | — |
> | 9 | `state check` exige que «Tests Currently Passing» sea el recuento real, y `make check` lo corre: cada fase que añade tests tiene que actualizar esa línea de `PROJECT_STATE.md` o no sella. | `src/botsito/cli.py:110`; `Makefile:54`; `MARGEN-PENDIENTE.md:381` | — |
> | 10 | La lección de margen-pendiente: lo que el consultor midió va en el encargo como «verifica que…», no como dato. El encargo da como dato el PASA de e) y el AVISO de d). La fase 0 lo vuelve a medir, pero conviene decirlo. | `ERRORES-RECURRENTES.md`, fila de `trabajo/margen-pendiente` (lección) | `MARGEN-PENDIENTE.md:1775` |
>
> **Comandos del encargo**: los diez existen y se ejecutan así (`git fetch --prune`; `gh run view` suelto, una vez, success; `uv sync --locked --group dev`, la línea de `ci.yml:27`; `make check > make-check.log 2>&1`; `make check` sin fichero, que la guardia niega; los tres `git push`, con la CI solo en `fix/**`, `ci.yml:4`; `uv run botsito state check`, que en `fix/` falla por Current Branch; `corpus inventory`, `cli.py:2932`; `casos_reservados`, `holdout.py:351`; el `pytest` del contrato, con `test_guardia_g1.py` aún por crear).
>
> **Lo que no pude comprobar**
>
> - El listado `git ls-files knowledge/cases | grep …` en memoria. No lo medí: mi encargo me prohíbe listar carpetas con meses reservados, y montar la ruta a trozos para que la guardia no lo vea sería rodearla. Me quedo con la medida del consultor y con `ENTORNO-CODE.md:950`, que dice que pasó entonces.
> - Las firmas de las funciones con el parámetro `crudo` en `src/`. La guardia me negó `grep -rn 'crudo: bool\|crudo=' src/botsito` («el comando pide el corpus SIN FILTRAR»). Es otro caso real de K1: un grep cuyo PATRÓN es el literal. No lo reescribí.
> - Si hay `python` y `ffprobe` en el PATH. `which python python3 ffprobe uv` lo negó la guardia («`which` lanza `python`»). Es otro posible falso positivo, para la tabla de f). Que el hook corre sí está probado, porque me bloqueó.
> - `knowledge/cases/holdout/README.md`. Lo quise leer para ver si dice algo de listar, y el clasificador lo negó. No insistí.
> - Un bucle `for f in …` para imprimir líneas. La guardia lo negó por `NOMBRES_DE_ENTORNO`; lo partí en `sed` encadenados, como permite su lista.
> - K2 y K3 en Windows y `C:/cm/`. No se pueden reproducir en Linux (ver la #49).
> - Las dos negativas «del diagnóstico de H» (#52): no están en el repo.
>
> **Lo más grave.** (1) El hueco prioritario e) no tiene base en ningún ADR: el único que habla de listar, ADR-0033 §1, dice que listar nombres «no cuenta», y la propia guardia cita ADR-0021 §1 para dejar listar (`guardia.py:4489`); negar exige un ADR (o una nota) o rebajar la lección, y `docs/adr/` está protegido en el contrato. (2) El patrón que el encargo manda reutilizar para Windows no existe tal como se describe: `SOLO_WINDOWS` omite el test en Linux y no hay monkeypatch de `os.name`. (3) La condición de ejemplo para K2 deja fuera el uso que la motiva: «byte a byte el de main» no cubre el test de la RAMA que corre comparar-con-main. Aparte: parte de lo que f) y K llaman falsos positivos (`git -c clave=valor`, el grep encadenado delante de `state check`, las dos ejecuciones encadenadas) son reglas decididas de guion-mismo-comando, y QUÉ NO CAMBIA contradice a a), h) y K3.

Nota sobre el auditor: el claim de su #26 de que el AVISO «se sostiene» lo contradice la medida de
§1.d: los comandos con `-r` SÍ se reproducen en Linux cuando el repo tiene material protegido; en el
repo real de la nube no lo tiene. Gana la medida.

## 3. Negativas de la guardia en esta sesión, y qué hice con cada una

| # | Comando (exacto) | Mensaje | Qué hice |
|---|---|---|---|
| n1 | `cd /home/user/Botsito && git status --short \| head; git branch -a; which python python3; python --version; cat .claude/settings.json \| head -60` | «ejecutar `which`: `which` lanza `python`, y lo que ejecute no se ve por sus argumentos» | La forma que propone (una cosa por llamada); `which` no lo volví a lanzar. Que hay `python` en el PATH lo prueba que el hook corre. Falso positivo: f15 |
| n2 | `uv run botsito state check 2>&1 \| tail -8; uv run python scripts/contrato_rama.py 2>&1 \| tail -8` | «ejecutar `python scripts/contrato_rama.py`: antes, en el mismo comando, va `uv run botsito state check`» | La forma que propone: dos llamadas. Es la regla decidida (f9b) |
| n3 | `grep -rn -E 'crudo' src/botsito --include=*.py \| grep -E 'def \|crudo=' \| head -40` (con el literal de la opción en el patrón) | «el comando pide el corpus SIN FILTRAR» | **PARADA de ese dato**: su mensaje no propone forma y no lo busqué con otra herramienta. Es K1 (a8). La propuesta de 1.a no lo necesita |
| n4 | `python <scratchpad>/medir_g1.py .claude/hooks/guardia.py …` con una ruta sintética de `data/visor/` escrita entera | «el codigo nombra data/visor/<caso>… (R_CASO)» | La ruta, a trozos, como manda el encargo para las rutas protegidas (§1, «Lo que hace la medida a propósito») |

El auditor declaró cuatro más en su informe (§2): el mismo `grep` de n3, el mismo `which` de n1, un
Read del README del holdout que negó el clasificador (no insistió) y un bucle `for` negado por
`NOMBRES_DE_ENTORNO` (siguió su forma).

**Exposiciones: ninguna.** Nada de esta fase lee material protegido real: en la nube no hay
`corpus/` ni `data/` y todo lo protegido es de mentira, en un directorio temporal. No hay fila en
HOLDOUT-EXPOSICIONES.

## Lo que no pude medir

- Windows de verdad (`\.`, `GetFullPathNameW` con espacios finales, `C:/cm/`): simulado; los
  comandos para Aleks, §1.i.
- Las dos negativas «del diagnóstico de H» (fase 3 del encargo): no están escritas en el repo
  (auditor, #52); las medí por su forma (f16, f18). Si el consultor las tiene literales, que las copie.
- Las firmas de `src/` con el parámetro de la opción: la guardia negó el `grep` (n3).
- El esquema de entrada de Artifact, ArtifactData, DesignSync y claude-in-chrome en la versión de
  Claude Code de Aleks (§1.j).

## Lo que necesito que decidas

0. **La base de e) (negar el listado del holdout).** Ningún ADR lo prohíbe: ADR-0033 §1 dice que
   listar nombres «no cuenta» y ADR-0021 §1 define abrir sin el listado; la prohibición vive en
   ERRORES-RECURRENTES (:72, :78, :80) y en la skill fase-cero. CLAUDE.md pide «o se corrige aquí o
   se cambia el ADR». Opciones: (a) un ADR nuevo, corto, en esta rama («listar los nombres de dentro
   de `holdout/{1,2,3}` no es abrir, pero la sesión no lo hace: se cuentan»), con `docs/adr/`
   abierto en el contrato solo para ese fichero y su índice; (b) la regla de la guardia cita tu
   respuesta a esta PARADA y las lecciones, CLAUDE.md se corrige, y el ADR queda como línea de
   Technical Debt; (c) no se niega: se rebaja la lección y el test de `:1855` no cambia.
   Recomiendo (a): es lo que pide CLAUDE.md para una prohibición sin ADR, y cuesta un fichero. Coste
   de (b): una regla de la guardia más estricta que su ADR, el patrón que CLAUDE.md dice que ya ha
   costado tres veces.
1. **El alcance de e).** Opciones: (a) la condición de §1.e entera: niega los listados que imprimen
   nombres de dentro de `holdout/{1,2,3}`, directos o recursivos desde cualquier ancestro (también
   `git ls-files` sin rutas y `find .` desde la raíz), Glob por lo que alcanza, PowerShell igual; deja
   el recuento (tubería que acaba en `wc` o `grep -c`) y los listados no recursivos de `holdout/` y de
   sus madres; cambia de sentido `test_ejecucion_quinta_pasada_admite[git ls-files]` (`:1855`) y se
   corrigen `COMO_REESCRIBIR` (`guardia.py:219-223`, que manda `ls` para lo protegido) y la cabecera
   (`:11`); (b) solo el listado de la madre CON un filtro detrás (`| grep`), que es lo que nombra la
   lección; `:1855` no cambia. Recomiendo (a): la lección dice que «el filtro va después de listar, y
   la lista ya se hizo», así que lo que cuenta es el alcance, no el filtro. Coste de (b): `git ls-files
   knowledge/cases` a secas, `ls -R` o un Glob siguen imprimiendo los nombres.
2. **K1, la forma de la opción.** Opciones: (a) §1.a: en Python, por el árbol (argumento con nombre,
   clave de dict, atributo asignado; `False` pasa; sin parsear, el regex de hoy); en el texto de Bash y
   PowerShell, solo la opción `--cr…`; (b) dejar el regex y quitarle solo la asignación a un nombre
   suelto. Recomiendo (a): nombra la forma, no la palabra (la lección del consultor en
   DEMO-EJECUCION-1.md :822), y quita también los `grep` negados (a7, a8, n3). Coste de (b): el `grep`
   con el literal sigue negado. Con (a) no hace falta renombrar ninguna variable (zanja la
   contradicción entre EA-CONEXION.md :547 y DEMO-EJECUCION-1.md :812, auditor, herencia 7).
3. **K2 y K3, los tests de un clon.** Opciones: (a) `_test_de_un_clon` de §1.b: un `git worktree` de
   ESTE repo, ruta bajo `tests/`, y bytes iguales al blob de `main` O al fichero del árbol de trabajo
   del repo real (el test de la rama copiado, que es el uso de comparar-con-main); K3 se resuelve por
   ahí y `analizar_codigo` no cambia; (b) solo el blob de `main`, como el ejemplo del encargo.
   Recomiendo (a): (b) deja fuera el uso que motiva K2 (auditor, #22; K3 fue un test de la rama en el
   clon). Coste de (a): el test copiado se fía de lo que ya está exento dentro del repo, ni más ni
   menos.
4. **K4, el candidato vacío.** Opciones: (a) lo que sale de partir por `=` no es una ruta si queda en
   blanco; el argumento ENTERO en blanco (d7b, `grep -rn " " src/`) sigue mirándose como hoy; (b)
   también el argumento entero en blanco deja de ser una ruta. Recomiendo (a): el `=` partido es un
   invento de la guardia; un argumento en blanco sí lo recibe el programa, y en Windows `" "` se abre
   como el directorio de trabajo (`GetFullPathNameW`), que no he podido medir. Coste de (a): d7b sigue
   negado (raro: un patrón que es solo espacios).
5. **`PYTHONIOENCODING` en `NOMBRES_DE_ENTORNO`.** Opciones: (a) entra, con su porqué: «elige la
   codificación de la entrada y salida estándar de Python; no carga código»; (b) no entra, y la forma
   sigue siendo sin la variable. Recomiendo (a): es de la misma clase que `PYTHONUTF8`, que ya está.
   Coste de (b): ninguno grave (la forma existe).
6. **Lo encadenado (f9, f9b, b6) y `git -c`.** Opciones: (a) sin cambio: es la lista cerrada de
   guion-mismo-comando («lo de delante», `_es_preparacion`), y `GIT_C_CLAVES` vacía es la opción B de
   §1.27; el mensaje ya da la forma (dos llamadas); (b) añadir a «lo de delante» lectores que no
   escriben (`grep`, `head`, `tail`, `wc`, `cat`, `ls`) sin redirecciones ni sustituciones.
   Recomiendo (a): son reglas decididas, no falsos positivos (auditor, #21, #42, #45), y el encargo
   dice «sin aflojar ninguna regla que hoy funciona». Coste de (a): una llamada más.
7. **`which` y `rmdir` en `NO_EJECUTAN`** (f15, f16; la lista «solo crece en una rama cuando un
   comando la pida», `guardia.py:2481`). Opciones: (a) entran los dos, con su porqué («busca un
   programa en el PATH, no lo ejecuta»; «borra un directorio vacío, no lee ni ejecuta»); (b) no.
   Recomiendo (a): es el mecanismo de la lista cerrada, no una excepción por nombre, y las dos
   negativas son de comandos reales (n1; la de H). Coste de (b): `which` sigue negado y `rmdir` no
   puede ir detrás de un `rm`.
8. **`solo_lectura.py` (f1-f4).** Opciones: (a) el subcomando se busca saltando las opciones globales
   de git (las de `GIT_CON_VALOR` de la guardia, con su valor); entran `worktree list` y `tag` solo
   para listar (sin argumentos, o con `-l`/`--list`); lo demás, como hoy; (b) sin cambio. Recomiendo
   (a): niega lo mismo que escribe (f4b, f4c siguen negados) y deja la vía de comparar-con-main. La
   guardia principal sigue negando `git -c` (decisión 6).
9. **B, lo que se resuelve.** Opciones: (a) §1.g: Python solo; se resuelven y se leen los imports, el
   `runpy`, el `exec(open(…))` y el `importlib` LITERALES que caen en la carpeta del guion, en una
   ruta literal de `sys.path` o en el repo, hasta 3 niveles; `botsito.*`, la biblioteca estándar y los
   paquetes de terceros, como hoy; lo no resoluble, negado; `subprocess`/`os.system` con programa
   literal se analiza como un comando de Bash y con programa no literal se niega; (b) negar todo
   `subprocess` en un guion que no sea de `main`. Recomiendo (a): (b) niega los guiones de trabajo
   que llaman a `git` (casi todos). Coste de (a): `botsito.*` sigue sin leerse, igual que la CLI.
10. **C, las rutas compuestas.** Opciones: (a) §1.h: primero se CALCULA la composición (partes
   literales o variables con un solo literal) y se mira como un literal; lo que no se puede calcular
   se niega si un texto de la composición lleva un fragmento sensible (variante ESTRECHA: 44 de 203
   guiones de main, 7 de `scripts/`); las llaves de Bash se expanden y `file://` se lee como su ruta;
   (b) la variante ANCHA (96 de 203). Recomiendo (a): niega los seis h5 por su motivo real y deja la
   composición inocua. Coste de (b): el doble de falsos positivos para el código nuevo.
11. **j, las herramientas fuera del `matcher`.** Opciones: (a) deuda con el texto de §1.j (que incluye
   `mcp__claude-artifacts__publish_files`, medida en esta sesión); (b) en esta rama, tocando
   `.claude/settings.json`. Recomiendo (a): pide `settings.json` y un esquema que aquí no se puede
   medir. El puntero «junto a K» de la deuda está caducado (era la K del alias; auditor, #50): el
   texto nuevo lo quita.
12. **Lo que el encargo y el contrato dicen a la vez.** QUÉ NO CAMBIA excluye la regla de la
   cuarentena y la de la CI, pero a) cambia `CRUDO_PYTHON` y h) mete la CI a trozos; y la fase 3
   corrige «skills» que QUÉ NO CAMBIA y el contrato protegen (auditor, herencias 1 y 2). Opciones: (a)
   a) y h) tocan esas reglas solo en lo que el encargo nombra; las skills no se tocan (la de
   fase-cero ya dice lo que decida e), y lo falso en ellas queda listado; los recuadros de informes
   cerrados, si hacen falta, amplían el contrato en su commit y se dice; (b) otra lectura que me
   digas. Recomiendo (a).
13. **Lo de G.1 que el encargo no nombra** (auditor, herencias 3 y 4): que `cerrar-rama` diga que con
   el Makefile cambiado los `make check` los lanza Aleks, y retirar `--diagnostico-a47`/`-a27` (toca
   `src/`). Recomiendo que sigan en G.1, fuera de esta rama (skills y `src/` protegidos), y que G.1
   no pase a HECHA en el cierre porque D sigue (auditor, #11).

Espero tu respuesta a la PARADA.


## Respuesta del consultor a la PARADA (2026-11-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/guardia-g1 (2026-11-04). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Un ADR corto en esta rama, con docs/adr/ abierto en el contrato solo para ese fichero y su índice (amplía el contrato en su propio commit y dilo). El ADR nombra la condición, no los casos: «listar los nombres de dentro de knowledge/cases/holdout/{1,2,3} no es abrir (ADR-0021 §1, ADR-0033 §1), pero es una exposición de proceso que la sesión no hace: se cuenta, no se imprime». Y enmienda la frase de CLAUDE.md «deja listarlo, medirlo y hashearlo» a «deja contarlo, medirlo y hashearlo por la CLI», en el mismo commit. Por qué: es lo que CLAUDE.md pide para una prohibición sin ADR, y es la 4.ª exposición.
> 1. (a), la condición de §1.e entera, con dos añadidos: (i) el test de :1855 cambia de sentido y su nombre nuevo dice lo que asegura; (ii) test_el_ritual_y_los_runbooks_pasan tiene que seguir pasando sin tocar ningún comando: lo comprobé (ningún runbook, skill ni comando del ritual usa git ls-files sin rutas, find ., ls -R ni git ls-tree -r); si en la fase 1 encuentras uno, PARADA antes de cambiarlo. Por qué: la lección es sobre el alcance, no sobre el filtro.
> 2. (a), la forma de la opción por el árbol de Python y solo --cr… en el texto de Bash y PowerShell. La clave en un dict literal sigue negada (a2, a6), como propones. Por qué: nombra la forma, no la palabra, y quita los grep negados (a7, a8, n3).
> 3. (a), _test_de_un_clon con el blob de main O el fichero del árbol de trabajo del repo real. Declara en el informe el riesgo que ya dices: el test copiado se fía de lo que dentro del repo ya está exento. Por qué: (b) deja fuera el uso que motiva K2.
> 4. (a): el candidato vacío o en blanco tras el = no es una ruta; el argumento entero en blanco (d7b) sigue como hoy. Por qué: el = partido es un invento de la guardia; un argumento en blanco sí lo recibe el programa.
> 5. (a): PYTHONIOENCODING entra en NOMBRES_DE_ENTORNO con su porqué.
> 6. (a): sin cambio en lo encadenado ni en git -c. Por qué: son reglas decididas en guion-mismo-comando, no falsos positivos.
> 7. (a): which y rmdir entran en NO_EJECUTAN, cada uno con su porqué en el comentario. Por qué: es el mecanismo de la lista cerrada.
> 8. (a): solo_lectura.py salta las opciones globales de git (las de GIT_CON_VALOR, con su valor) para encontrar el subcomando; entran worktree list y tag solo para listar; lo demás igual. Por qué: niega lo mismo que escribe y abre la vía de comparar-con-main.
> 9. (a), §1.g: Python solo, hasta 3 niveles, negar lo no resoluble, subprocess con programa literal como un comando de Bash y no literal negado. El mensaje de la negativa nombra el módulo o la llamada que no pudo resolver, para que la sesión sepa qué forma usar.
> 10. (a), la variante ESTRECHA con el cálculo previo de la composición, las llaves expandidas y file:// como su ruta. Añade a la fase 2 esta medida: para los 7 guiones de scripts/ que la estrecha marca, qué composición los marca y si con el cálculo la ruta resultante es inocua (es decir, si cambiados en una rama pasarían igual); la cifra real de coste es esa, no 44.
> 11. (a): j queda como deuda con el texto de §1.j, publish_files incluido, y el puntero «junto a K» desaparece de esa línea en las líneas del cierre.
> 12. (a): a) y h) tocan CRUDO_PYTHON y la regla de la CI solo en lo que el encargo nombra; las skills no se tocan (lo falso en ellas queda listado para el cierre); los recuadros de informes cerrados amplían el contrato en su commit y se dice.
> 13. De acuerdo: cerrar-rama y los flags de diagnóstico siguen en G.1, fuera de esta rama, y G.1 no pasa a HECHA.
>
> Desviaciones de la apertura: aceptadas y quedan declaradas (la CI consultada con una llamada suelta a la API en vez de gh run view, porque gh solo está permitido para búsquedas en la nube; el git fetch --unshallow del clon).
>
> Sigue sin parar: fase 1 en el orden del encargo (e, a, b, c, d, f), con el ADR y la enmienda de CLAUDE.md en el primer commit de la fase; después la fase 2 (B y C) y la fase 3. Tests primero, rotos a propósito en los dos sentidos, medir_g1.py antes y después, make check sellado por fase con PICO DE MEMORIA. Al terminar: push de la rama, push a fix/guardia-g1 con la CI de Linux y sus números de run, el revisor con el informe terminado, y la lista de §1.i para Aleks con los comandos exactos. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto.
>
> Rama lista para revisión, NO cerrada.

## 4. Fase 1: los falsos positivos y el hueco prioritario (e, a, b, c, d, f)

### 4.0 La respuesta, punto por punto

| Punto | Qué decía | Hecho |
|---|---|---|
| 0 | ADR corto, contrato ampliado en su commit, enmienda de CLAUDE.md en el mismo commit que el ADR | Contrato: commit 898040c. ADR-0088 (`docs/adr/0088-los-nombres-de-dentro-del-holdout-se-cuentan-no-se-listan.md`) y su fila del índice; CLAUDE.md, «Las guardias de Claude Code»: «deja contarlo, medirlo y hashearlo por la CLI; los nombres de dentro de `knowledge/cases/holdout/{1,2,3}` se cuentan, no se listan (ADR-0088…)». Los dos, en el commit de esta fase (el primero de la fase) |
| 1 | La condición de §1.e entera; `:1855` cambia de sentido con un nombre que dice lo que asegura; `test_el_ritual_y_los_runbooks_pasan` sin tocar ningún comando | §4.1. `test_listar_desde_la_raiz_imprime_los_nombres_del_holdout_y_se_niega`. El test del ritual pasa sin tocarlo (en la suite de `make check`) |
| 2 | La forma por el árbol; solo `--cr…` en Bash y PowerShell; la clave de dict sigue negada | §4.2 |
| 3 | `_test_de_un_clon` con el blob de main O el fichero del árbol; declarar el riesgo | §4.3; el riesgo, en su docstring y aquí abajo |
| 4 | El vacío tras el `=` no es una ruta; el argumento entero en blanco sigue | §4.5 |
| 5 | `PYTHONIOENCODING` en `NOMBRES_DE_ENTORNO` | §4.6 |
| 6 | Sin cambio en lo encadenado ni en `git -c` | Sin cambio; `test_f_lo_decidido_en_guion_mismo_comando_sigue_negado` lo fija |
| 7 | `which` y `rmdir` en `NO_EJECUTAN` | §4.6 |
| 8 | `solo_lectura.py` salta las opciones globales de git | §4.6 |
| 9, 10 | B y C | fase 2 |
| 11 | j como deuda, sin «junto a K» | fase 3 (líneas del cierre) |
| 12 | a) y h) solo en lo que nombra el encargo; skills sin tocar; recuadros con contrato ampliado | Hecho en esta fase: a) toca `CRUDO_PYTHON` solo como respaldo del código que no se parsea; ninguna skill tocada |
| 13 | `cerrar-rama` y los flags de diagnóstico siguen en G.1 | Sin tocar |

### 4.1 e) Listar el holdout (ADR-0088)

Una sola condición, `Politica.lista_dentro_del_holdout(ruta, recursivo)`: un listado imprime nombres
de dentro de `holdout/{1,2,3}` si su ruta es una de esas carpetas o algo de dentro que no sea un
fichero (un fichero NOMBRADO se mide y se hashea), o, si es recursivo, cualquier carpeta que las
contenga (también un ancestro de la raíz). La usan:
- **Bash** (`_lista_nombres_del_holdout`, en `analizar_comando`; para `find`, al final de
  `_analizar_find`, para que la regla de `-exec` hable primero, como fija la matriz de
  `test_guardia_ffmpeg.py`): `ls`/`dir`/`vdir` (recursivos con `-R`), `tree`, `du` (salvo `-s`),
  `find`, `git ls-files` (siempre recursivo; una ruta con comodín o con `:` alcanza todo) y
  `git ls-tree` (`-r`; `HEAD:<carpeta>`), con `-C`; y un comodín de CUALQUIER argumento
  (`sha256sum <holdout>/1/*`, `echo …/*/*`). Pasa si la tubería acaba en `wc` o en `grep -c` y el
  listado no escribe a un fichero (`_solo_sale_un_recuento`).
- **Glob** (`_patron_lista_el_holdout`): las llaves se expanden; si la parte literal del patrón es
  una carpeta cuyo listado alcanza el holdout, y el patrón casa con un fichero de dentro (salvo el
  README de cada partición) o con una sonda de caso (`caso-eurusd-2000-01-01.yaml`, porque es lo que
  guarda una partición aunque hoy solo tenga su README), se niega. Así `**/*.py` pasa y
  `knowledge/cases/**/*.yaml` no.
- **PowerShell** (`_powershell_lista_el_holdout`): `Get-ChildItem` y sus alias, con `-Recurse` (o su
  abreviatura) o con una ruta de dentro; `| Measure-Object` es un recuento. `gci`, `dir` y `ls` en
  PowerShell ya los niega main como ejecución.
- `COMO_REESCRIBIR` ya no manda `ls` para lo protegido, y la cabecera de la guardia lo dice.

**Cambian de sentido, por su nombre** (`tests/unit/test_guardia_claude.py`): `git ls-files` sin
rutas (`test_ejecucion_quinta_pasada_admite`, `:1855`, el que anunciaba el encargo) y
`find . -exec sha256sum {} +` (`test_ejecucion_cuarta_pasada_admite`, `:1784`; otro `find .` desde la
raíz, de los que la respuesta acepta negar). Los dos pasan a
`test_listar_desde_la_raiz_imprime_los_nombres_del_holdout_y_se_niega`, y en sus listas de
admitidos quedan con rutas literales (`git ls-files src docs`, `find src -exec sha256sum {} +`).
`git ls-tree HEAD` (`:1856`, no recursivo) sigue pasando. Ningún comando del ritual ni de los
runbooks cambió: `test_el_ritual_y_los_runbooks_pasan` pasa en la suite de `make check` (punto 1.ii).

### 4.2 a) La forma de la opción (K1)

`exigir_sin_crudo(texto, donde, es_python)`: en el texto de un comando de Bash o PowerShell solo
cuenta la opción de la CLI (`_opcion_en_el_texto`, `CRUDO_OPCION`); en código Python que se parsea,
`_pide_la_opcion` mira el árbol: argumento con nombre, clave de un dict literal, atributo o subíndice
asignados y `setattr`, con cualquier valor que no sea el literal `False`. Si no se parsea, o no es
Python, el regex de antes. **Dos formas que main dejaba pasar y ahora se niegan** (salieron al
escribir los tests): `k['<opción>'] = True` y `setattr(x, '<opción>', 1)`. Lo que se afloja, por su
nombre: el literal `<opción>=…` en un comentario de Python o en un comando de Bash que no ejecuta
Python.

### 4.3 b) y c) Los tests de un clon (K2, K3)

`_test_de_un_clon(ruta, raiz, con_el_arbol)`: fuera de la raíz, un fichero cuenta como test del repo
si está en un `git worktree` de este repositorio (su `.git` apunta a `<git común>/worktrees/`), su
ruta en él empieza por `tests/` y sus bytes son el blob de `main` o, en `pytest`, el fichero de esa
ruta en el árbol de trabajo del repo real. Se usa en `_analizar_pytest` (con el árbol) y en
`_exigir_guion_legible` (solo `main`). K3 se resuelve por aquí (`analizar_codigo` no cambia).
**Riesgo declarado** (punto 3): el test copiado se fía de lo que dentro del repo ya está exento, ni
más ni menos; como dentro del repo, no se lee el `conftest.py` ni el `src/` que carga el clon.

### 4.4 c) en Windows

Simulado como en `_romper` de `test_guardia_alias.py`: `_windows` cambia `_absoluta` para que `\.`
sea un directorio que contiene el repo y el clon. El test igual pasa; el cambiado se niega con «la
carpeta \.». Lo de Windows de verdad, en §1.i.

### 4.5 d) El vacío tras el `=` (K4)

`candidatos_de_ruta` ya no da lo de detrás del `=` si queda en blanco. Pasan los cuatro comandos de
los informes (BARRIDO-SESION-6.md :540 y :612, ACTIVAR-SESION-04-MOTOR.md :1384) y la negativa de H
(`grep -rn "HUSO_CORTE =" src/`); siguen negados `grep -rn " " src/` (el argumento entero en blanco),
`--exclude-dir=<holdout>`, `cat --x=<fichero del holdout>` y `cat ruta=<fichero del holdout>`.
**Hallazgo sin arreglar** (la respuesta solo decidió el `=`): `candidatos_de_ruta` parte también por
`:` (`rev:ruta`) y por `@`; un patrón como `"Puntos: "` daría el mismo candidato en blanco. Queda para
el cierre como línea de Technical Debt.

### 4.6 f) El resto de G.1

- `NO_EJECUTAN` gana `which` («busca un programa en el PATH… no lo ejecuta») y `rmdir` («borra un
  directorio VACÍO…»), con su porqué en el comentario; `NOMBRES_DE_ENTORNO` gana `PYTHONIOENCODING`.
- `solo_lectura.py`: `_subcomando_git` salta las opciones globales (las de `GIT_CON_VALOR` de la
  guardia, con su valor); entran `worktree list` y `tag` solo para listar (`_tag_que_lista`: sin
  argumentos o con `-l`/`--list`, y ninguna opción que cree, borre, firme o mueva). Siguen negados
  `git tag stable/x`, `git -C <clon> commit`, `git -c k=v commit`, `git worktree add/remove`.
- Sin cambio (punto 6): `grep …; uv run botsito state check`, dos ejecuciones encadenadas y
  `git -c k=v` en la guardia principal.

### 4.7 Tests rotos a propósito, en los dos sentidos

`tests/unit/test_guardia_g1.py`: 82 tests. **Antes del código** (los tests escritos primero, contra
la guardia de main): 49 fallan, 33 pasan
(`anexos/GUARDIA-G1/pytest-1-antes-del-codigo.txt`). **Con el código**: los 82 pasan
(`pytest-2-con-el-codigo.txt`). **Rotos a propósito** (`test_roto_a_proposito`, 18 casos; salida en
`pytest-roto-a-proposito-FASE1.txt`): cada pieza nueva, quitada (la forma mala vuelve a pasar) y
hecha negar o aceptar de más (la buena se niega, o la mala pasa):

```
ROTO | sin_listado | test_e_los_listados_del_holdout_se_niegan | falla: git ls-files knowledge/cases | grep -v holdout
ROTO | sin_listado | test_e_el_glob_que_alcanza_el_holdout_se_niega | falla: {'pattern': 'knowledge/cases/**/*.yaml'}
ROTO | sin_listado | test_e_powershell_que_lista_el_holdout_se_niega | falla: Get-ChildItem -Recurse knowledge/cases
ROTO | listado_de_mas | test_e_el_recuento_y_lo_literal_pasan | falla: git ls-files knowledge/cases/dev knowledge/cases/kit
ROTO | listado_de_mas | test_e_glob_y_powershell_que_no_alcanzan_el_holdout_pasan | falla: Get-ChildItem docs
ROTO | sin_forma | test_a_la_forma_de_la_opcion_en_python_se_niega | falla: argumento
ROTO | sin_forma | test_a_la_opcion_en_codigo_en_linea_y_en_la_cli_se_niega | falla: python -c "print(dict(<opción>=True))"
ROTO | regex_de_antes | test_a_una_variable_con_ese_nombre_y_los_grep_pasan | falla: leer.py
ROTO | sin_clon | test_b_los_tests_del_clon_iguales_al_de_main_o_al_del_repo_pasan | falla: cd <tmp>/cm/main && uv run pytest tests/unit/test_recorre.py -q
ROTO | clon_de_mas | test_b_lo_que_no_es_el_test_del_repo_se_sigue_negando | falla: cd <tmp>/cm/main && uv run pytest tests/unit/test_cambiado.py -q
ROTO | sin_clon | test_c_la_raiz_de_la_unidad_en_un_test_del_clon_igual_pasa | falla: assert 'el codigo nombra la carpeta \\., que contiene material protegido…
ROTO | clon_de_mas | test_c_la_raiz_de_la_unidad_en_un_test_cambiado_se_niega | falla: None
ROTO | candidato_de_antes | test_d_un_patron_con_igual_no_es_una_ruta | falla: grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py
ROTO | sin_candidato_igual | test_d_lo_que_sigue_siendo_una_ruta_se_mira | falla: grep -rn --exclude-dir=knowledge/cases/holdout x src
ROTO | subcomando_de_antes | test_f_solo_lectura_deja_leer_git_con_opciones_globales | falla: git -C <tmp>/cm/main rev-parse HEAD
ROTO | subcomando_de_mas | test_f_solo_lectura_sigue_negando_lo_que_escribe | falla: git tag stable/x
ROTO | sin_listas_nuevas | test_f_which_rmdir_y_pythonioencoding_pasan | falla: which python python3
ROTO | lo_decidido_abierto | test_f_lo_decidido_en_guion_mismo_comando_sigue_negado | falla: grep -n x PROJECT_STATE.md; uv run botsito state check
```

Tres casos de PowerShell del test se cambiaron al ejecutarlo: `gci -r …`, `dir -Recurse …` y
`ls <holdout>/1` ya los niega main como ejecución (su lista cerrada de PowerShell está vacía); el test
usa `Get-ChildItem`, que es lo que llega a la regla nueva.

### 4.8 La comparación caso a caso con la guardia de main

`medir_g1.py <guardia de main> <guardia de la rama>` (`anexos/GUARDIA-G1/medir_g1-FASE1.txt`), sale
con 0: de los 43 casos que main niega, **21 pasan en la rama, todos declarados** en
`CAMBIOS_DECLARADOS` con su punto de la respuesta (a1, a7, a8; b1, b2, b3, b8, b9; c1-win; d2, d3,
d5, d6, f18; f1, f2, f3, f4 en `solo_lectura`; f8; f15; f16). Y **16 que main dejaba pasar se niegan**:
exactamente los listados del holdout (e1-e9, e12, e13, e14, e14b, e14c, e14d, e14e). B y C (g y h)
siguen como en main: son la fase 2.

### 4.9 Desviaciones y negativas de la guardia en esta fase

- Tres negativas por encadenar en un mismo comando una copia o un `grep` con una ejecución (`cp …
  && uv run pytest`, `mkdir … && uv run pytest`, `grep … PROJECT_STATE.md; uv run pytest`) y una por
  `sed` detrás de `pytest`: errores de forma míos, con la forma que propone el mensaje (dos llamadas,
  o un filtro de su lista). Y `python -m py_compile` (la guardia solo admite `-m pytest`): un guion
  con Write ejecutado por su ruta, como dice el mensaje. Ninguna es un cambio de esta rama: son reglas
  de main.
- La comparación de §4.8 pide la guardia de `main` en un fichero: `git show main:… > <scratchpad>`,
  fuera del repo.

### 4.10 El ADR es el 0088, no el 0087 (desviación declarada)

El primer `make check` de esta fase salió en ROJO (exit 2, 5 fallos, todos de la misma comprobación):
«ERROR: id declarado inexistente que SI existe: docs/encargos/trabajo-activar-sesion-05-motor.md:8:
ADR-0087» y lo mismo en `docs/validation/ACTIVAR-SESION-05-MOTOR.md:28`. Esa rama dejó escrito
«ADR-0087 — el ADR que S-15 tendría si existiera la frontera (punto 9); aún no existe», y
`knowledge validate` exige que un id declarado inexistente siga sin existir. La respuesta del
consultor no fija el número: el ADR de esta rama pasa a ser el **0088**
(`docs/adr/0088-los-nombres-de-dentro-del-holdout-se-cuentan-no-se-listan.md`), con sus
referencias (guardia, tests, CLAUDE.md, índice, este informe), y el contrato cambia en el mismo
commit: permite `docs/adr/0088-*.md` y protege `docs/adr/0087*`. El 0087 queda libre para S-15:

```ids-inexistentes
ADR-0087 — reservado por trabajo/activar-sesion-05-motor para S-15; esta rama no lo crea
```

## Estado

FASE 0 HECHA y respondida (2026-11-04); contrato ampliado en su propio commit (898040c). FASE 1
HECHA (e, a, b, c, d, f; ADR-0088 y la enmienda de CLAUDE.md en su commit). EN CURSO: fase 2 (B y C).
