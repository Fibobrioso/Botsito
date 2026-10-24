# GUARDIA-ALIAS · la guardia niega el material protegido escriba como se escriba la ruta

Rama: `trabajo/guardia-alias`, abierta el 2026-10-24 desde `main` en `af89a78` (commit de estado
sobre el merge `2cc3b93`, tag `stable/F38b-guardia-ci`). Encargo:
`docs/encargos/trabajo-guardia-alias.md`. Carril de guardias y deuda, G.1 de la hoja de ruta: paga
la línea PRIORITARIA de G.1 y la parte de K de la Next Action que habla del alias de la raíz en
`motivo_fichero` (lo que queda de K sigue en K). Tag de cierre previsto: `stable/F38c-guardia-alias`;
la ingesta de la sesión 5 pasa a F38d.

## Base comprobada al abrir

- `git fetch origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `af89a78802af71692221bcc941745d09330d4493` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38b-guardia-ci^{commit}"` =
  `2cc3b93b68eb662d993146a2a5c819bf4b45f6d4`; el tag está en origin
  (`git ls-remote --tags origin stable/F38b-guardia-ci`:
  `47d20ceae55cfe6575b4759a41209814c4179819 refs/tags/stable/F38b-guardia-ci`, el objeto del tag
  anotado). La última línea `- Tag:` de HISTORIA nombra ese mismo tag.
- CI de `main` sobre su HEAD, con una consulta suelta (`gh run view 40092378098 --json
  headSha,status,conclusion,event,headBranch`): `completed` / `success`, `headSha` `af89a78…`,
  rama `main`, evento `push`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`.
- `Current Feature` no está en WAITING_FOR_USER_VALIDATION.
- La carpeta del diagnóstico del 2026-10-24 existe en el scratchpad de la sesión anterior
  (`…\49e8894b-c04f-4137-9483-9024a98edd2b\scratchpad\diagK\`) con los cinco ficheros que nombra el
  encargo (DIAGNOSTICO-K.md, tabla.md, medir_k.py, existe.py, contar.py), más una subcarpeta
  `Bot v3 prueba` y un `errores.txt` vacío. Solo listada; su contenido se revisa en la fase 0.a.

## §0 · Fase 0

Medido el 2026-10-24 sobre c60a8d4 (la guardia es la de `main` af89a78: la rama no la ha tocado).
Todo lo que toca material protegido, EN MEMORIA con `decidir` de `.claude/hooks/guardia.py` y
`motivo` de `.claude/hooks/solo_lectura.py`, sobre el repo inventado de `medir_k.py` (la carpeta
de trabajo de la sesión, con ficheros falsos en los tres sitios protegidos: la carpeta de marzo del
material adicional, `holdout/1` y la cruda de v7). Las salidas completas, en
`docs/validation/anexos/GUARDIA-ALIAS/fase0/salidas.md`; los guiones, al lado. Las líneas de
`guardia.py` son las de c60a8d4.

### §0.0 · Comandos negados durante la fase 0 (regla 2 del encargo)

1. `mkdir -p …; wsl --status; wsl -e python3 --version` en un solo comando: negado por
   `R_EJECUCION` (un `mkdir` delante de una ejecución). Seguí la forma que propone la guardia: una
   llamada por comando.
2. `wsl -e python3 --version` suelto: negado por `R_EJECUCION` («`wsl` lanza `python3`, y lo que
   ejecute no se ve por sus argumentos»). Sin forma propuesta que valga. Consecuencia: la parte de
   Linux de 0.c no se midió aquí (va en «Lo que no pude medir»); la mide la CI de `fix/`.

### §0.a · El diagnóstico del 2026-10-24: existe, dice eso, y la cifra se confirma

> **CORRECCIÓN (2026-10-24, `trabajo/guardia-alias`, respuesta del consultor a la PARADA 2,
> punto 0).** Las 123 de abajo son lecturas que la guardia DEJABA PASAR, medidas en memoria. De las
> 99 de a/d, 18 (`\\?\`, UNC a `localhost` y `\\?\UNC\`, en Bash `cat` y Monitor) no abren el
> fichero tal como las escribe `medir_k.py`. En §3.4 di como causa la comilla doble de bash; es
> otra: la herramienta Bash de Claude Code vuelve `\\` una sola barra ANTES de bash, también entre
> comillas simples (revisor, a1). Escritas con las barras dobladas, sí abren, y la guardia, que
> veía el texto sin esa capa, las dejaba pasar (b1). Desde la PARADA 2 la guardia decide las dos
> lecturas (§11). El cuerpo de abajo queda como estaba.

- Los cinco ficheros existen en el scratchpad de la sesión anterior y están copiados en
  `docs/validation/anexos/GUARDIA-ALIAS/diagnostico/` (DIAGNOSTICO-K.md, tabla.md, medir_k.py,
  existe.py, contar.py). La carpeta trae además el repo inventado `Bot v3 prueba` (NO se copia:
  es un repo git con una carpeta falsa cuyo nombre la guardia protege) y un `errores.txt` vacío
  (no se copia). `tabla.md` venía con CRLF y se pasó a LF.
- Comprobación antes de copiar: ninguno lleva una fecha de un día reservado, un resultado ni
  una ruta protegida entera. `grep -c "Users\|2026-\|Desktop" tabla.md` = 0; DIAGNOSTICO-K.md
  solo nombra el 8.3 de la raíz REAL del repo (`BOTV3~1`, un metadato de la carpeta del repo, no
  del material) y las variables del shell; `medir_k.py` monta las tres rutas protegidas a trozos
  (`"corp" + "us"`, `"hol" + "dout"`, `"cru" + "da"`, `"Back" + "test marzo 2026"`) y usa en su
  `particiones.yaml` falso el id `caso-eurusd-2026-05-04`, el mismo que ya lleva
  `tests/unit/test_guardia_claude.py:64` commiteado: no es un día reservado real ni lo revela.
- `medir_k.py` re-pasado sobre el HEAD de la rama (c60a8d4): la tabla es idéntica byte a byte a
  la del diagnóstico (`diff` sin salida). **123 lecturas protegidas pasan**: 99 en a/d (6 formas
  × 5 herramientas × 3 ficheros = 90, más las tres formas sin prefijo de dispositivo -UNC, 8.3 y
  punto final- en PowerShell, 3 × 3 = 9: eso es «las tres sin `\\?\`» del encargo), 12 en b sobre
  carpetas inventadas (sin Glob, que lista), 6 en b' sobre el Escritorio y la carpeta del usuario
  reales (solo se decide si contienen zonas protegidas; nada se abre) y 6 en c (variables).
- `existe.py` ya lo midió el diagnóstico: las seis formas llegan al mismo fichero
  (`os.path.exists`); el «espacio final» no existe y sus 18 «pasa» no son fuga.

### §0.b · Dónde entra la ruta en cada herramienta

Cuatro piezas, en `guardia.py`:

| pieza | líneas | qué hace |
|---|---|---|
| `_absoluta(ruta, cwd)` | 1063-1073 | `strip`, `/c/…` y `/cygdrive/c/…` → `C:/…`, `~` → `expanduser`, relativa → `join(cwd)`, `normpath`. Sin `realpath`, sin quitar `\\?\`, `//?/` ni UNC, sin deshacer el 8.3 |
| `_normcase(ruta)` | 613-620 | `normpath`, `\` → `/`, minúsculas |
| `Politica.relativa(ruta)` | 432-439 | `_normcase(ruta)` contra `raiz_norm` (286: `_normcase(str(RAIZ))`, con `RAIZ = Path(__file__).resolve().parents[2]`, 86); `None` si no empieza por la raíz |
| `Politica.motivo_fichero(ruta)` | 447-490 | `basename` (450: `cruda-no-leer`; libro por nombre y mes, 453-455, SIN depender de `relativa`), `relativa` (452), y las zonas por `rel` (458-489) |
| `Politica.motivo_directorio` / `motivo_ruta` / `motivo_dentro_de_zona` | 514-548 / 574-581 / 583-591 | las tres empiezan por `relativa`; con `None` devuelven `None` (519-520, 587-588): **aquí pasa un directorio que CONTIENE la raíz** |

Por dónde entra cada herramienta (todas pasan por `_absoluta` antes de la política, salvo lo
dicho al final):

| herramienta | entrada → `_absoluta` → política | líneas |
|---|---|---|
| Read | `file_path` → `_absoluta` → `motivo_fichero` | 4217-4219 |
| Grep | `path` (o `cwd`) → `_absoluta` → `motivo_ruta(recursivo=True, respeta_ignore=True)` | 4232-4234 |
| Glob | nada: `None` siempre («listar nombres no es abrir», ADR-0021 §1) | 4241-4242 |
| Bash y Monitor | `analizar_bash` (1088) → `analizar_comando` (1325) → un lector: `_exigir_args_legibles` (1525-1548: cada valor y cada `candidatos_de_ruta` → `_absoluta` 1542 → `os.path.exists` o `motivo_fichero` 1543 → `motivo_ruta` 1545) y `_exigir_legible` (1551-1562: 1558) | 1491-1510 (grep/rg/tar), 1500 (`grep -r` sin ruta: `motivo_ruta(ctx.cwd)`) |
| Bash `find … -exec` | cada raíz → `_absoluta` → `motivo_ruta(recursivo=True)` | 1923 |
| Bash `git show/diff/log/grep` | `rev:ruta` → `_absoluta` (1783) → `relativa` + `motivo_ruta` (1784-1787) | 1765-1800 |
| Bash `rm -rf` | `_absoluta` → `relativa` | 1820 |
| Bash `cd` | destino → `_absoluta` → `ctx.cwd` (así todo lo relativo que siga cuelga de ahí) | 1377 |
| Bash `pytest` | cada ruta → `_absoluta` → `relativa` (¿es `tests/`?) | 2002 |
| Bash, un guion (`python x.py`, `./x`, `uv run x.py`, `bash x.sh`, `pwsh -File`) | `_es_fichero_de_la_rama` / `_es_fichero_programa` (3243-3261: `_absoluta` → `relativa`) → `_exigir_guion_legible` (3464-3472: `_absoluta` → `motivo_fichero` → `relativa` → `_igual_que_en_main`) → su CONTENIDO por `analizar_codigo` | 1361, 1420, 2182, 3464-3472 |
| Bash, código en línea y guiones (`python -c`, `bash -c`, heredocs, el guion leído) | `analizar_codigo` (3581-3617): cada literal → `_absoluta` (3594) → `motivo_fichero` (3597); si es directorio, `motivo_ruta(recursivo=recorre)` (3603) | 3581-3617 |
| Bash, un glob | el patrón → `_absoluta` → `glob.glob` (resultados reales del disco) | 1055 |
| Bash, la salida de una ejecución | `_normcase(_absoluta(v))` contra los guiones | 3436, 3441 |
| Bash `ffprobe`/`ffmpeg` | `_ffmpeg_ruta` → `_absoluta` (3045) → `_ffmpeg_formas_de_la_ruta` (3135-3143: la ruta, `os.path.realpath` y sin puntos ni espacios finales) → `motivo_fichero` por cada forma (3218) y `relativa` (3146, 3239, 3250, 3260) | 3045-3260 |
| PowerShell | `analizar_powershell` (4116): cada trozo entre comillas o palabra (4157-4158), salvo los que empiezan por `-` o `$` (4160), → `_absoluta` (4162) → `motivo_fichero` o, si es directorio, `motivo_dentro_de_zona` (4163-4165); `-Recurse` → `motivo_ruta(ctx.cwd, recursivo=True)`, solo el cwd (4187-4188) | 4116-4192 |

Se saltan `_absoluta`, y no importa: `_primer_protegido` (560-571) llama a `motivo_fichero` con
las rutas REALES que da `os.walk`; `lineas_de_tramo` (368) recibe una ruta que ya pasó por
`_absoluta`. **El único sitio que hoy canoniza es ffmpeg** (`_ffmpeg_formas_de_la_ruta`): es el
precedente, y la auditoría lo señala (el encargo no lo nombra). Si la canonización entra en
`_absoluta`, ffmpeg pasa por ella dos veces (sin daño: `realpath` es idempotente) y su test de
alias, solo Windows, en `tests/unit/test_guardia_ffmpeg.py` (protegido por el contrato) tiene
que seguir en verde.

Por qué pasan las seis formas: `_absoluta` las deja como están (`\\?\C:\…`, `//?/C:/…` →
`normpath` → `\\?\C:\…`; `\\localhost\C$\…`; `BOTV3P~1`; `Bot v3 prueba.`), `_normcase` las
baja a minúsculas con `/`, y ninguna EMPIEZA por `raiz_norm` → `relativa` es `None` → todo lo
que depende de `rel` devuelve `None`. `motivo_fichero` mira el nombre antes que `rel` (450-455),
por eso un libro con nombre 8.3 (`BACKTE~1.XLS`) tampoco lo vería: el `basename` también se
canoniza al canonizar la ruta.

### §0.c · Windows: `ctypes` y `realpath`; Linux

Medido con `fase0/tiempos.py` y `fase0/tiempos2.py` (tablas enteras en `fase0/salidas.md`),
Python 3.12.10 (el del sistema, que es el del hook, y el mismo de `uv run`):

| función | disponible | qué resuelve | qué NO resuelve | tiempo por ruta |
|---|---|---|---|---|
| `GetFullPathNameW` (ctypes) | sí | `.` y `..`, barras, el punto final, `//?/` → `\\?\` | deja `\\?\`, UNC y el 8.3; deja el espacio final | 3-4 µs |
| `GetLongPathNameW` (ctypes) | sí | el 8.3 → largo, el punto final | deja `\\?\` y UNC; **`None` si la ruta no existe** (también el espacio final) | 210-320 µs local; 3,5-3,9 ms en UNC `localhost` |
| `os.path.realpath` (ntpath 3.12, `GetFinalPathNameByHandle`) | sí, biblioteca estándar, y ya en uso (3141) | el 8.3, el punto final, **el espacio final**, `.` y `..`, `\\.\C:\` → `C:\`, enlaces y uniones, y una cola que no existe (resuelve el prefijo más largo que exista: `<R 8.3>\no\existe.txt` → `<R>\no\existe.txt`) | **deja `\\?\` cuando la entrada lo trae** (lo quita solo si lo añadió él), deja UNC como UNC (`\\localhost\C$\…` no pasa a `C:\…`), deja `\\otra-maquina\C$\…` tal cual | 40-200 µs local; 0,3-0,9 ms en UNC |
| `Path.resolve()` | sí | lo mismo que `realpath` | lo mismo | un 30-50 % más |

Lo que cuesta en el hook: la guardia corre en cada llamada, en un proceso nuevo, y llama a
`_absoluta` una vez por ruta candidata (en un `cat a b c`, tres; en un glob, una por patrón, no
por resultado; en `analizar_codigo`, una por literal de texto del guion, que en un guion largo son
cientos). Con `realpath` a 0,1 ms, cien literales son 10 ms; el peor caso medido en la suite de
la guardia hoy es un test de 6 s (`test_la_lista_de_la_guardia_es_la_que_se_calcula`), que no
pasa por `_absoluta`. Lo mido antes y después en la fase 1 (tiempo de la suite).

Lo que ninguna función hace sola, y hay que escribir: quitar `\\?\` y `//?/`; `\\?\UNC\<host>\X$\`
y `\\<host>\X$\` → `X:\` cuando `<host>` es la propia máquina (`localhost`, `127.0.0.1`, `::1`, el
nombre del equipo); y decidir qué se hace con lo que no se puede canonizar (`\\otra-maquina\…`,
`\\.\<dispositivo que no sea una unidad>`, `\\?\GLOBALROOT\…`, `\\?\Volume{…}\…`).

**Linux (CI):** no se pudo medir en local (§0.0: `wsl` negado). Lo que se sabe sin tocar el
disco (`posixpath.normpath`, en `salidas.md`): `\\?\C:\…`, `\\localhost\C$\…` y `\\?\UNC\…` son
en Linux UN nombre relativo con barras invertidas (`_absoluta` lo cuelga del cwd); `//?/C:/…`
conserva las dos barras iniciales (POSIX las respeta) y no cuelga de nada; el 8.3 no existe
(ext4 no tiene nombres cortos); el punto y el espacio finales son OTRO directorio. Ninguna de las
seis formas llega a un fichero en Linux: no hay fuga que cerrar allí, y `os.path.realpath` solo
resuelve enlaces. **Tests con `skip` fuera de Windows:** las seis formas de a/d y el punto final
(`existe.py` solo tiene sentido en NTFS), el «espacio final», las variables con `//?/` y con 8.3,
y lo no canonizable (UNC a otra máquina, `\\.\`). Corren en los dos sistemas: el contenedor (b),
las variables de Bash y PowerShell con rutas normales, lo bueno, y la regresión contra `main`. La
tabla «antes» de 123 es de Windows, y se declara así (lección de `trabajo/guardia-ci`,
ERRORES-RECURRENTES.md:95); la CI de `fix/guardia-alias` mide la de Linux.

### §0.d · El lector recursivo sobre una carpeta que contiene la raíz

| programa o herramienta | cómo lo ve hoy la guardia | línea | resultado sobre un contenedor |
|---|---|---|---|
| `grep -r`, `egrep -r`, `fgrep -r` | `recursivo` si lleva `-r`/`-R`/`--recursive` → `motivo_ruta(ruta, True)` → `motivo_directorio` → `relativa` `None` → `None` | 1491-1505, 519-520 | **pasa** |
| `rg` | siempre recursivo, `respeta_ignore` salvo `--no-ignore`/`-u` → ídem | 950, 1495-1499 | **pasa** (y la guardia no sabe si rg, desde fuera, aplica el `.gitignore` del repo al entrar: no medido) |
| `tar`, `zip`, `7z` | recursivos (`ARCHIVADORES`) → ídem | 951, 1496 | **pasa** |
| `find <contenedor> … -exec cat {} ;` | cada raíz → `motivo_ruta(recursivo=True)` → ídem | 1923 | **pasa** |
| `cp -r` / `rsync -r` desde el contenedor | `_exigir_legible(recursivo=True)` → ídem | 1472-1476 | **pasa** |
| `git grep` / `git log -p` con una ruta de fuera | `relativa` `None` → ni se mira | 1784 | pasa (git no sale del repo: no es fuga) |
| Grep (herramienta) | `motivo_ruta(ruta, True, respeta_ignore=True)` → ídem | 4232-4234 | **pasa** |
| Monitor | como Bash | 4243-4256 | **pasa** |
| Glob (herramienta) | `None` siempre | 4241-4242 | pasa (lista nombres: no es fuga, ADR-0021 §1) |
| PowerShell `Get-ChildItem -Recurse <x> \| Get-Content` | `-recurse` es «dinámico» y `gci`/`get-childitem` están en la lista de palabras sensibles → se niega SIN regla, apunte a donde apunte (también a `src/`); la comprobación con regla (4187-4188) solo mira el `cwd` | 4175-4188 | niega (sin regla) |
| un guion que recorre (`os.walk`, `glob`, `iterdir`…) con el contenedor en un literal | `analizar_codigo`: el literal es un directorio → `motivo_ruta(recursivo=True)` → ídem | 3595-3603 | **pasa** |

La causa es una: `motivo_directorio` (y `motivo_dentro_de_zona`) solo saben decidir sobre rutas
DENTRO de la raíz; una ruta que contiene la raíz es «fuera» y se deja. Sobre el Escritorio y la
carpeta del usuario REALES, con la política real, pasa igual (b': 6).

### §0.e · Las variables

Bash (`resolver`, 1011-1060), con el entorno del PROCESO del hook:

| forma | cómo se resuelve | línea | resultado |
|---|---|---|---|
| `$HOME`, `$USERPROFILE`, `${USERPROFILE}` | `os.environ[base]` si `base == nombre` (sin modificadores) | 1040-1041 | niega con regla, en las dos formas de HOME (`/c/Users/…` y `C:\Users\…`: `_absoluta` entiende las dos) |
| `$CLAUDE_PROJECT_DIR` | siempre la raíz (`str(ctx.politica.raiz)`), venga o no en el entorno | 1038-1039 | niega con regla |
| `$PWD` | `ctx.cwd` | 1037 | — |
| `~` | `os.path.expanduser` sobre el valor entero | 1049-1050 (y `_absoluta` 1067-1068) | niega con regla |
| `%USERPROFILE%` | no es una variable para Bash: texto literal | — | pasa, y no es fuga (Bash no lo expande) |
| `S="<raíz>"; cat "$S/…"` | la asignación se resuelve al leerla (1120) y `$S` vale su texto (1036) | 1120, 1036 | niega con regla |
| **`S="//?/<raíz>"; cat "$S/…"`** y **`S="<raíz 8.3>"; …`** | igual: `$S` vale el alias, y `_absoluta` no lo canoniza | 1036, 1063-1073 | **pasa**: no es un fallo de las variables, es el de a) con otra entrada |
| una variable que no se sabe | `DinamicoError` → un lector se niega (`_exigir_args_legibles`, 1535-1540) | 1042 | niega |

PowerShell (`analizar_powershell`, 4116-4192): **no resuelve ninguna variable**. Los trozos que
empiezan por `$` se saltan (4160), así que `$env:USERPROFILE\…` y `$env:CLAUDE_PROJECT_DIR\…` no
se miran como ruta; y el patrón de «dinámico» (4175-4177) exime `$env:` a propósito, así que
tampoco caen en «rutas que solo se saben al ejecutar». `$HOME\…` sí es «dinámico» y se niega sin
regla solo si el texto lleva una palabra sensible (4178-4180; sobre `x\y.txt` pasa, medido). `~`
sí se resuelve, porque `_absoluta` la expande (4162). `$r = '…'; Get-Content "$r\…"` se niega
antes, como ejecución (una asignación es `{`/ejecución en PowerShell, `R_EJECUCION`), no por la
ruta. La auditoría lo dice bien: las 6 de PowerShell no vienen «del entorno del hook» sino de no
resolver y de la exención de `$env:`.

### §0.f · `solo_lectura.py`

De las 123, 50 son comandos de Bash (22 `cat`, 18 guiones de Python, 6 `grep -r`, 4 `find -exec
cat`) y las 50 pasan también allí. No es una fuga suya: `solo_lectura.py` es, por diseño, «una
lista de lo que escribe, no de lo que lee: lo que no está aquí pasa» (su docstring, :14-16), solo
decide sobre Bash (:118) y no mira ninguna ruta de lectura; para los agentes de solo lectura, «la
guardia del proyecto (`guardia.py`) sigue corriendo además para todo» (:11-12). Las otras 73
(Read, Grep, PowerShell, Monitor) ni le llegan. **La medida no pide tocarlo**: lo que cierra las
50 es la misma condición en `guardia.py`, que corre antes para los agentes. (La auditoría
observa aparte que `solo_lectura.py` niega `git tag --list` como «cambia el repositorio», de la
misma familia que la línea de G.1 sobre `git worktree list`: fuera de esta rama.)

### §0.g · Lo bueno, la línea de base

97 filas: un fichero de `src/` en las 16 formas y 6 herramientas, y `grep -r x docs/`. Pasan
todas salvo 3, PowerShell `Get-Content` con `\\?\`, `//?/` y `\\?\UNC`: el `?` del prefijo casa
el comodín de «dinámico» y la carpeta de trabajo de la sesión cuelga de `AppData\`, que contiene
`data\`, palabra de `SENSIBLES`. Es un artefacto del sitio de la medida (con la raíz real, en
`Desktop`, ese `\\?\` sobre `src/` pasa; sobre un fichero protegido se niega sin regla por la
palabra del material). Y `Get-ChildItem -Recurse '<raíz>\src' | Get-Content` se niega sin regla
siempre (§0.d). La condición nueva no puede negar nada de estas 94 que hoy pasan, y además, por
la lección de `trabajo/guardia-ci` (ERRORES-RECURRENTES.md:95), en la fase 1 se vuelven a pasar
por `decidir` los programas de datos que pasaban en `main` (los 32 comandos de RITUAL.md que ya
fija `test_el_ritual_y_los_runbooks_pasan`, `rg`/`grep` con patrón sobre `docs/`, `wc -c`,
`sha256sum`, `stat`), no solo lo de la regla.

Tiempo de la suite de la guardia ANTES (`tests/unit/test_guardia_claude.py`,
`test_guardia_ffmpeg.py`, `test_guardia_ci.py`; 687 tests, Windows, `uv run pytest --durations=5`):
**178,89 s** (2 min 58 s), casi todo en el `setup` de los repos inventados (git) y no en las
llamadas a `decidir` (el `call` más lento, 5,82 s, es `test_la_lista_de_la_guardia_es_la_que_se_calcula`;
las 1.355 duraciones restantes bajan de 5 ms). El registro, en
`anexos/GUARDIA-ALIAS/fase0/pytest-antes.log`.

### §0.h · El encargo frente al repo (auditoría, `auditor-encargo`, 2026-10-24)

30 afirmaciones: 21 correctas, 0 incorrectas, 9 con matiz. Las que cambian algo:

1. **El OBJETIVO nombra `motivo_fichero`, pero el hueco no vive solo ahí.** La familia «carpeta
   que contiene el repo» (18 de 123) va por `motivo_ruta` → `motivo_directorio`, y Grep y el
   `-Recurse` de PowerShell por ahí; las tres dependen de `relativa` y de `_absoluta` (§0.b). El
   arreglo tiene que estar en `_absoluta` (o en `relativa`) y cubrir los ancestros de la raíz, no
   en `motivo_fichero`. Se trabaja con lo medido (decisión 0).
2. **Las 6 de PowerShell no salen «del entorno del hook»** (§0.e): PowerShell no resuelve
   variables y exime `$env:`. El texto de K y de G.1 lo dice así para Bash, donde sí es verdad;
   el del cierre lo dirá bien (fase 2).
3. **`solo_lectura.py` no mira lecturas por diseño** (§0.f): las 123 pasan por construcción, y
   «lo mismo en solo_lectura.py» no aplica.
4. **PROJECT_STATE está en 24.186 bytes en la rama** (23.955 en `main`; +231 del Current
   Feature de c60a8d4), así que el margen bajo el tope de 25.000 es de 814 bytes, no 1.045.
5. **ffmpeg pasa por `_absoluta`** (3045): «las formas de ffmpeg no cambian» es verdad en su
   regla, pero su decisión pasa por el código nuevo, y su test de alias (protegido por el
   contrato) tiene que seguir en verde sin tocarse (§0.b).
6. **«Las tres sin `\\?\`» del encargo** es ambiguo; leído con la tabla son UNC, 8.3 y punto
   final en PowerShell (§0.a).

Herencias que el repo pide y el encargo no recoge:

- **Technical Debt con dueño:** el docstring de `tests/contract/test_tramos_fuente.py:5` cita
  «PROJECT_STATE, Decisions and Rationale, 2026-09-04», que vive en
  `docs/runbooks/DECISIONES-DE-PROCESO.md`; «lo corrige la próxima rama que toque `tests/`»
  (PROJECT_STATE.md:146). Esta rama toca `tests/` y ese fichero no está en `rutas_permitidas`
  (decisión 7).
- **La regla fina de Artifact, ArtifactData, DesignSync y claude-in-chrome** (mirar sus rutas
  como un Read) «va en su propia rama del carril de guardias, junto a K (el alias de la raíz)»
  (PROJECT_STATE.md:105). Toca `.claude/settings.json`, protegido por el encargo (decisión 8).
- **Las lecciones de `trabajo/guardia-ci` y `trabajo/guardia-ffmpeg`** (ERRORES-RECURRENTES.md:94
  y :95): re-pasar los programas de datos de `main` y declarar de qué sistema es la tabla
  (hecho en §0.c y §0.g, y en la fase 1); y al revisor, pedirle también comillas y escapes de
  bash sobre la raíz (`$'…'`, `$"…"`), que el encargo no le pide (decisión 9).
- **El registro de cierre en HISTORIA y la fila de ERRORES-RECURRENTES** van en el commit del
  contrato aunque la orden solo nombre el punto Y (RITUAL.md:120-136): se preparan en la fase 2.

### §0.i · Lo que no pude medir

- **Linux de verdad** (0.c): `wsl` lo niega la guardia (§0.0). Queda lo razonado con
  `posixpath` y la CI de `fix/guardia-alias`, que mide la tabla «antes» en Linux.
- **PowerShell de verdad:** la herramienta no está cargada en esta sesión; se midió su análisis
  en memoria, como el diagnóstico.
- **`rg` real desde un contenedor:** si aplica el `.gitignore` del repo al entrar en él (importa
  para `respeta_ignore`). La condición propuesta no depende de eso: trata el contenedor como la
  raíz con el mismo `respeta_ignore` que ya recibe.
- **Enlaces simbólicos y uniones** (`mklink /J`) dentro o hacia dentro del repo: `realpath` los
  resuelve (medido en su documentación de 3.12, no con una unión real aquí).
- **`\\<nombre del equipo>\C$\…`:** no se midió (el nombre del equipo no se imprime); es la misma
  familia que `localhost` y `127.0.0.1`, que sí (`existe.py`, `tiempos2.py`).

### §0.j · Exposiciones

Ninguna. Nada se abrió del material del punto 3 de CLAUDE.md: las rutas protegidas de la medida
son ficheros falsos del repo inventado, montadas a trozos y sin imprimir; sobre el Escritorio y
la carpeta del usuario reales solo corrió `decidir` (metadatos: si contienen zonas protegidas).

## Lo que necesito que decidas

0. **Dónde se canoniza.** Opciones: (a) una función `_canonica(ruta)` llamada desde `_absoluta`
   al final (1063-1073), de modo que TODO lo que la política recibe ya es canónico (Read, Grep,
   Bash, Monitor, PowerShell, guiones, código en línea, ffmpeg, `cd`); (b) canonizar dentro de
   `Politica.relativa`, `motivo_fichero`, `motivo_ruta` y `motivo_dentro_de_zona`. Recomiendo
   (a): un solo sitio por el que pasan las 20 llamadas de §0.b, y el `basename` de
   `motivo_fichero` (450-455, el libro por nombre) también queda canónico. Coste de (b): cuatro
   sitios, y el nombre 8.3 de un libro seguiría sin verse.
1. **Con qué se canoniza.** Opciones: (a) `os.path.realpath` más lo que no hace solo -quitar
   `\\?\` y `//?/`, y pasar `\\?\UNC\<host>\X$` y `\\<host>\X$` a `X:` cuando `<host>` es la propia
   máquina- y después `normpath` y los puntos y espacios finales de cada tramo como en
   `_ffmpeg_formas_de_la_ruta`; (b) `GetFullPathNameW` + `GetLongPathNameW` por `ctypes`.
   Recomiendo (a): biblioteca estándar, ya en uso en la guardia (3141), resuelve el 8.3, los
   finales, `\\.\C:\`, enlaces y una cola que no existe (`GetLongPathNameW` da `None` si la ruta
   no existe, y habría que recorrer prefijos a mano), y cuesta 40-200 µs por ruta local. Coste
   de (b): más código, lo mismo que falta escribir, y `ctypes` solo existe en Windows (hay que
   ramificar). En las dos, la parte de prefijos solo con `os.name == "nt"`.
2. **Lo que no se puede canonizar** (`\\otra-maquina\X$\…`, `\\.\<no unidad>`,
   `\\?\GLOBALROOT\…`, `\\?\Volume{…}\…`, un UNC a un host que no es la propia máquina). Opciones:
   (a) `_absoluta` lanza `BloqueoError` con su regla, siempre (también para un `cd` o una
   redirección de salida, que no leen): negar por defecto, el mensaje dice la forma; (b) solo se
   niega cuando el que llama LEE contenido, y en los demás usos se deja tal cual. Recomiendo (a):
   es la regla de la casa (lo que no se sabe decidir y puede llegar a material protegido se
   niega), ninguna sesión usa esas formas, y (b) obliga a distinguir el uso en 20 llamadas.
   Coste de (a): un `cd \\otra\…` se niega aunque no abra nada.
3. **La propia máquina** para los UNC. Opciones: (a) lista cerrada: `localhost`, `127.0.0.1`,
   `::1`, `.` y `socket.gethostname()` (en minúsculas); (b) cualquier host se trata como la
   unidad local. Recomiendo (a): un host ajeno no es canonizable (decisión 2) y así se niega;
   con (b), `\\otra\C$\<ruta de la raíz>` se trataría como la raíz y se negaría solo si coincide,
   pero `\\otra\D$\x` pasaría leyendo un disco que no se conoce (no es material del repo, pero
   tampoco se sabe qué es). Coste de (a): un alias del equipo que no esté en la lista (un nombre
   DNS propio) se niega.
4. **El contenedor.** Opciones: (a) en `motivo_directorio` (y en `motivo_dentro_de_zona`), si la
   ruta canónica es un ANCESTRO de la raíz, se decide como si fuera la raíz, con el mismo
   `respeta_ignore` que se recibió (`grep -r`, `find -exec`, `rg`, Grep, Monitor, `cp -r`, un
   guion que recorre); (b) negar toda lectura recursiva fuera de la raíz. Recomiendo (a): cierra
   las 18 con la regla del primer fichero protegido que alcanza, y deja `grep -r x <carpeta
   hermana sin el repo>` como hoy. Coste de (b): niega `grep -r` sobre cualquier carpeta de
   fuera, también el scratchpad. Glob sigue en `None` (lista).
5. **PowerShell y las variables.** Opciones: (a) antes de mirar los trozos, sustituir `$env:X`,
   `${env:X}`, `$HOME`, `$PWD` y `~` con el entorno del hook (como `resolver` en Bash), y negar
   una variable que no se resuelve delante de un lector, lleve o no palabra sensible; (b) solo
   la sustitución, y lo demás como hoy. Recomiendo (a): es la misma regla que Bash (una ruta que
   no se sabe no se lee), ningún comando de la sesión ni de los runbooks usa PowerShell, y cierra
   las 2 formas de `$env:` y el `$HOME` sin palabra sensible. Coste de (a): `Get-Content
   "$PSScriptRoot\x"` y las automáticas se niegan.
6. **Skips en Linux** (§0.c). Opciones: (a) la canonización de prefijos y de 8.3 solo con
   `os.name == "nt"`, y los tests de esas formas con `skipif` fuera de Windows, declarados; la CI
   de `fix/` comprueba que en Linux ninguna de las seis formas llega a un fichero (la tabla
   «antes» de Linux) y que lo bueno y el contenedor pasan allí; (b) canonizar igual en los dos
   sistemas. Recomiendo (a): en Linux `\\?\C:\…` es un nombre de fichero legítimo y quitarle el
   prefijo sería inventar una ruta. Coste de (a): la CI no prueba el código de los prefijos.
7. **La deuda con dueño de `tests/contract/test_tramos_fuente.py:5`** (§0.h). Opciones: (a) se
   amplía el contrato con ese fichero en un commit y se corrige el docstring aquí (una línea), y
   la línea de Technical Debt sale en el cierre; (b) se declara que pasa a la siguiente rama que
   toque `tests/`. Recomiendo (a): la deuda nombra a esta rama, y son dos líneas. Coste de (b):
   tercera rama seguida que la deja.
8. **La regla fina de Artifact y claude-in-chrome** (PROJECT_STATE.md:105, «junto a K»).
   Opciones: (a) fuera de esta rama, y en el cierre su línea de Technical Debt sigue, apuntando a
   que la canonización ya existe; (b) entra aquí (toca `.claude/settings.json`, protegido por el
   encargo: PARADA). Recomiendo (a): el encargo deja `settings.json` fuera y esas herramientas
   están cerradas en `permissions.deny`; no leen nada hoy. Coste de (a): otra rama del carril.
9. **El encargo del revisor.** Opciones: (a) a las cinco formas de la raíz o de un contenedor se
   le añade «y con las comillas y escapes de bash sobre la raíz (`$'…'`, `$"…"`, una variable
   definida en el mismo comando)», por la fila de guardia-ffmpeg de ERRORES-RECURRENTES; (b) se
   deja como está. Recomiendo (a): es la lección escrita para «al revisor», y cuesta una línea.
   Coste de (b): ninguna, salvo repetir el error que la fila recoge.

Y tres cosas que no son decisión, dichas: el «espacio final» hoy no existe para `exists` pero
`realpath` lo resuelve a la raíz (medido), así que tras el cambio se niega (negar de más no abre
nada); `.claude/settings.json` no necesita cambio (el matcher ya lleva Read, Grep, Glob, Bash,
PowerShell y Monitor); y `solo_lectura.py` no se toca (§0.f).

## §1 · Respuesta del consultor a la PARADA 1 (2026-10-24), copiada tal cual

> Respuesta del consultor a la PARADA 1 de trabajo/guardia-alias (2026-10-24). Cópiala al informe, en su sección.
>
> 0. SÍ: _canonica dentro de _absoluta.
> 1. SÍ: os.path.realpath más los prefijos a mano (\\?\, //?/, \\?\UNC\, UNC a la propia máquina). Como realpath también resuelve junctions y symlinks, añade a los tests un disfraz más: una junction (mklink /J, en Windows) o un symlink dentro del repo inventado que apunte a un sitio protegido, negado al leer por él; y lo bueno, una junction a src/, pasando.
> 2. SÍ: lo no canonizable (UNC a otra máquina, \\.\, GLOBALROOT, Volume{…}) se niega siempre desde _absoluta, con un mensaje que diga que la ruta no se puede canonizar y cuál es la forma buena (la ruta normal desde la raíz o relativa).
> 3. SÍ: lista cerrada para la propia máquina: localhost, 127.0.0.1, ::1, . y el nombre del equipo (leído en el hook, no escrito en el código).
> 4. SÍ: un ancestro de la raíz se decide como la raíz, con su respeta_ignore.
> 5. SÍ: en PowerShell se resuelven $env:, $HOME, $PWD y ~; una variable que no se resuelve delante de un lector se niega.
> 6. SÍ: prefijos y 8.3 solo con os.name == "nt", y skips declarados en Linux. La CI de fix/ tiene que enseñar que en Linux pasan los demás.
> 7. SÍ: amplía el contrato a tests/contract/test_tramos_fuente.py en un commit propio y corrige su docstring (cita DECISIONES-DE-PROCESO.md, no PROJECT_STATE). La línea de Technical Debt que lo pide (PROJECT_STATE:146) sale en el commit del contrato del cierre y así gana bytes. Declara que trabajo/guardia-ci tocó tests/ y no la pagó: es un error del consultor, para la orden de cierre.
> 8. SÍ: la regla fina de Artifact y claude-in-chrome, fuera de esta rama (siguen negadas por permisos).
> 9. SÍ: el revisor añade comillas y escapes de bash sobre la raíz ($'…', $"…", barras invertidas), junto a sus cinco formas.
>
> PROJECT_STATE: margen de 814 bytes. En el cierre salen la parte de K que paga esta rama y la línea del punto 7; si aun así no cabe, PARADA antes de recortar nada más.
>
> Sigue con las fases 1 y 2 y la entrega, como dice el encargo.

## §2 · La respuesta, punto por punto

- **Punto 7, hecho en su commit propio:** `contrato.yaml` ampliado con
  `tests/contract/test_tramos_fuente.py`, y su docstring cita ahora
  `docs/runbooks/DECISIONES-DE-PROCESO.md` (Decisions and Rationale, 2026-09-04, la línea de la
  garantía de inmutabilidad contra el historial, :26) en vez de PROJECT_STATE. La línea de
  Technical Debt (PROJECT_STATE.md:146) sale en el commit del contrato del cierre. **Declarado,
  para la orden de cierre:** `trabajo/guardia-ci` (y antes `trabajo/guardia-ffmpeg`) tocaron
  `tests/` y no la pagaron; el consultor lo da como error suyo.
- **Puntos 0 a 6 y 9:** en §3 (código y tests). **Punto 8:** fuera de la rama; la línea de
  Technical Debt de Artifact y claude-in-chrome sigue (PROJECT_STATE.md:105). **Punto 9:** en el
  encargo del revisor (§6).

## §3 · Fase 1: la condición

### §3.1 · El código (`.claude/hooks/guardia.py`, +146 −7)

| pieza | línea | qué hace | punto |
|---|---|---|---|
| `R_ALIAS` | 172 | la regla, con su origen | 2, 5 |
| `_absoluta` → `_canonica` | 1093 | todo lo que la política recibe ya es canónico | 0 |
| `_propia_maquina` | 1109 | `localhost`, `127.0.0.1`, `::1`, `.` y el nombre del equipo, LEÍDO con `socket.gethostname()` (y su parte corta) | 3 |
| `_no_canonizable` | 1114 | `BloqueoError` con «no se puede canonizar» y la forma buena («desde la raíz» o relativa) | 2 |
| `_sin_prefijos` | 1123 | solo Windows: `\\?\X:` y `//?/X:` y `\\.\X:` → `X:`; `\\?\UNC\h\X$` y `\\h\X$` con `h` propia → `X:`; `GLOBALROOT`, `Volume{…}`, `\\.\pipe`, otra máquina o un recurso que no es `X$` → `_no_canonizable`; un prefijo sin nada detrás o un servidor sin recurso no nombra un fichero y se deja | 1-3, 6 |
| `_canonica` | 1149 | en Windows, `_sin_prefijos`, `normpath` y sin puntos y espacios finales; en los dos sistemas, `os.path.realpath` si es absoluta (8.3, finales, enlaces, uniones, la cola que no existe) | 1, 6 |
| `candidatos_de_ruta` | 1173 | `https://x/y` ya no da el candidato `//x/y` (sería un UNC a otra máquina y se negaría un `grep` de una URL) | — |
| `Politica.raiz_norm` | 298 | la raíz también canónica | 0 |
| `Politica.contiene_la_raiz` y `motivo_directorio` | 453, 540 | un ancestro de la raíz se recorre como la raíz, con el mismo `respeta_ignore` | 4 |
| `cd` sin destino | 1464 | `~` por `_absoluta` (canónica) | 0 |
| `_variables_powershell` | 4214 | `$env:X`, `${env:X}`, `$HOME`, `$PWD` (y `CLAUDE_PROJECT_DIR`, la raíz, como en Bash) | 5 |
| PowerShell, variable sin resolver | 4304 | delante de un lector, `R_ALIAS` | 5 |
| PowerShell, `?` del prefijo | 4312 | el `?` de `\\?\` no es un comodín: lo bueno con prefijo pasa (§0.g) | — |
| `decidir`, el `cwd` | 4355 | canónico, como todo lo que cuelga de él | 0 |
| cabecera, familia 1 | 25-30 | la condición, dicha | — |

La «excepción» del OSError (`_canonica`): si `realpath` lanza un `OSError` (en 3.12 no lanza en
modo no estricto salvo errores de Windows fuera de su lista), se compara la forma sin prefijos y
sin finales. No se niega, porque `_canonica` también pasa por cada literal de un guion y un
literal raro (`a?b`, `<x>`) negaría el guion entero. Es riesgo residual declarado (§5).

### §3.2 · Los tests (`tests/unit/test_guardia_alias.py`, 35 tests tras el revisor, 11 a 45 s)

En memoria, con `decidir`, sobre un repo inventado en `tmp_path` con espacio en el nombre y
ficheros falsos en tres sitios protegidos (marzo, `holdout/1`, la cruda de v7). Las rutas
protegidas se montan a trozos y los mensajes nombran el caso por su número, no por su ruta.

| test | qué exige | sistema |
|---|---|---|
| `test_cada_forma_de_la_raiz_se_niega_con_la_regla_del_sitio` (×3 sitios) | 15 formas (`\\?\`, `//?/`, UNC a `localhost`, a `127.0.0.1`, al nombre del equipo y con `/`, `\\?\UNC\localhost`, el punto final, `\\.\X:`, el 8.3 y el 8.3 con `//?/`, y los disfraces: MAYÚSCULAS, barras mezcladas, `.` y `..`, la unidad en minúscula, punto final con prefijo) × 6 herramientas (Bash `cat`, Read, Grep, PowerShell, Monitor, un guion de Python): la regla del sitio | Windows |
| `test_lo_bueno_pasa_con_cada_forma_de_la_raiz` | las mismas 15 formas sobre `src/`: pasa en las 6 | Windows |
| `test_lo_bueno_pasa_en_las_formas_de_siempre` | relativa, absoluta, `.`/`..`, y los programas de datos de `main`: `grep -rn`, `rg`, `wc -c`, `sha256sum` y `stat` sobre lo protegido, `ls` | los dos |
| `test_un_lector_recursivo_sobre_una_carpeta_que_contiene_la_raiz_se_niega` | `grep -r`, `grep -R`, `find -exec cat`, `cp -r`, `rg --no-ignore`, Grep y Monitor sobre la carpeta del repo y la de encima (y con `\\?\` y `//?/` en Windows): negado con regla | los dos |
| `test_rg_desde_fuera_respeta_lo_ignorado_como_desde_la_raiz` | `rg` sin `--no-ignore` desde fuera: `R_HOLDOUT` (no entra en lo ignorado, sí en el holdout) | los dos |
| `test_una_carpeta_hermana_sin_el_repo_pasa` | lo mismo sobre una carpeta sin el repo: pasa | los dos |
| `test_una_variable_de_bash_con_un_alias_se_niega` | `S="//?/<raíz>"`, `S='\\?\<raíz>'`, `S='//localhost/C$…'`, `S="<8.3>"` definidas en el mismo comando: `R_SIN_ABRIR`; `export S=…`: negado | Windows |
| `test_powershell_resuelve_env_home_pwd_y_tilde` | `$env:USERPROFILE`, una variable de entorno propia, `$env:CLAUDE_PROJECT_DIR`, `$HOME`, `$PWD`, `~`, `$ENV:userprofile` y barras con `..`: `R_SIN_ABRIR`; `${env:X}` y `gc` ya se niegan como ejecución | los dos |
| `test_powershell_niega_una_variable_que_no_resuelve_delante_de_un_lector` | `$env:NO_EXISTE` y `$algo` delante de `Get-Content`: `R_ALIAS` | los dos |
| `test_powershell_lo_bueno_y_lo_literal_pasan` | `$env:` y `$PWD` hacia `src/`, `%USERPROFILE%` literal, `Get-ChildItem $env:X` y `Write-Output $algo` sin lector, y `\\?\` hacia `src/`: pasan | los dos |
| `test_lo_que_no_se_puede_canonizar_se_niega_con_la_forma_buena` (×7) | otra máquina (`\\`, `//` y `\\?\UNC\`), un recurso de `localhost` que no es `X$`, `\\.\pipe`, `GLOBALROOT`, `Volume{…}`, en Bash, Read y Grep: `R_ALIAS`, «no se puede canonizar» y «desde la raíz» | Windows |
| `test_fuera_de_windows_los_prefijos_no_se_tocan` | en Windows `\\?\C:\x\y` → `C:\x\y`; fuera, `\\?\` queda en el nombre | los dos |
| `test_leer_por_una_union_o_un_enlace_hacia_lo_protegido_se_niega` | una unión (`mklink /J`; en Linux un enlace simbólico) en `docs/` hacia `holdout/1`: `R_HOLDOUT` en las 6 herramientas; otra hacia `src/`: pasa | los dos |
| `test_roto_a_proposito` (×14) | ver §3.3 | 8 en los dos, 6 solo Windows |

**En Linux van con `skip`** (punto 6), declarados: las 3 de formas y la de lo bueno con prefijos,
la de variables de Bash, las 7 de lo no canonizable y 6 roturas: 18 de 35. Las otras 17 corren en
los dos sistemas; la CI de `fix/` lo enseña (§7). Tras el revisor (b10), el contenedor lleva
también sus disfraces: MAYÚSCULAS, barras mezcladas con `..`, y `/./` al final.

**Contra la guardia de `main`** (antes del código; anexo `fase1/tests-contra-la-guardia-de-main.txt`,
con la versión del test de ese momento): fallaron todas las familias, lo que demuestra que el test
ve el agujero: las 3 de formas, lo bueno con prefijo en PowerShell, el contenedor, `rg` desde
fuera, las variables de Bash y las tres de PowerShell, las 7 de lo no canonizable, la de Linux y la
de la unión.

### §3.3 · Roto a propósito, en los dos sentidos

`test_roto_a_proposito` rompe una pieza (`_romper`) y exige que cada test que la pieza sostiene
FALLE. Salida, `anexos/GUARDIA-ALIAS/fase1/roturas.txt` (14 líneas, todas «falla»; las dos
últimas, de b9 del revisor: lo bueno de PowerShell con `todo_es_la_raiz`, «R_HOLDOUT», y los
prefijos en Windows con `identidad`, «'\\\\?\\C:\\x\\y' == 'C:\\x\\y'»):

| rotura | sentido | tests que tienen que fallar, y fallan |
|---|---|---|
| `identidad` (`_canonica` = `normpath`, como `main`) | lo protegido vuelve a pasar | formas (`\\?\ · Bash cat: pasa`), variables de Bash (`caso 0: pasa`), lo no canonizable (`('Bash', None)`), la unión (`…\docs\atajo\caso.yaml · Bash cat: pasa`) |
| `todo_es_la_raiz` (todo cae en el holdout) | lo bueno se niega | lo bueno con prefijos (`\\?\ · Bash cat: R_HOLDOUT`), lo bueno de siempre (`ruta 0 · Bash cat: R_HOLDOUT`), la carpeta hermana (`grep -r: R_HOLDOUT`) |
| `sin_contenedor` | el contenedor vuelve a pasar | el lector recursivo (`la carpeta del repo · grep -r: pasa`), `rg` desde fuera (`'pasa' == 'R_HOLDOUT'`) |
| `sin_variables_ps` | `$env:` vuelve a pasar | las dos de PowerShell (`caso 0: pasa`; `$env:…NO_EXISTE… None`) |
| `sin_no_canonizable` | otra máquina pasa | lo no canonizable (`('Bash', None)`) |

Primero lo monté con una variable de entorno (`GUARDIA_ALIAS_MUTANTE`, una corrida por mutante).
La guardia lo negó: el nombre no está en `NOMBRES_DE_ENTORNO` («Como reescribirlo: sin esa
variable»). Seguí esa forma, declarada: las roturas pasan a tests del propio fichero con
`monkeypatch`, como `test_sin_la_regla_las_permitidas_vuelven_a_negarse` de ffmpeg. Así quedan
en la suite y corren en cada `make check`.

### §3.4 · La tabla del diagnóstico, antes y después

`medir_k.py`, el mismo guion, sobre el mismo repo inventado: antes, `diagnostico/tabla.md`;
después, `fase1/tabla-despues.md`. Recuento de `contar.py`:

| bloque | filas | pasan antes | pasan después | fugas después |
|---|---|---|---|---|
| a/d, la raíz en sus formas | 288 | 117 (99 fugas + 18 del espacio final, que no existe) | 18 | 0 tal como están escritas; el hueco que las 18 representan sigue abierto (abajo, y b1) |
| b, contenedor inventado | 18 | 15 (12 fugas + 3 de Glob) | 3 (Glob) | 0 |
| b', contenedor real | 8 | 6 | 2 (Grep) | 0 (abajo) |
| c, variables | 24 | 9 (6 fugas + 3 de `%USERPROFILE%`) | 3 (`%USERPROFILE%`) | 0 |
| e, lo bueno | 97 | 3 negadas | 0 negadas | — |

Las que siguen pasando, una por una:

- **a/d, 18:** `\\?\`, UNC a `localhost` y `\\?\UNC\` en Bash `cat` y en Monitor, escritas por
  `medir_k.py` entre comillas dobles: la guardia ve `\?\C:\…` y `\localhost\C$\…` (que no son
  alias) y pasa. Escritas ASÍ no abren: medido sobre el fichero BUENO del repo inventado,
  `cat "\\?\C:\…\src\botsito\cli.py"` da «No such file or directory», y entre comillas simples
  también. **Corregido por el revisor (a1 y b1, §9):** la causa no es la comilla doble de bash
  sino la herramienta Bash de Claude Code, que quita un nivel de `\` ANTES de bash, también
  entre comillas simples. Con las barras DOBLADAS (`cat '\\\\?\\C:\\…'`, `cat '\\\\localhost\\C$\\…'`)
  bash recibe el prefijo bueno, `cat` abre el fichero bueno, y la guardia, que ve cuatro barras,
  lo deja pasar: también sobre lo protegido, en la rama y en `main`. **Así que estas 18 filas no
  son fugas tal como están escritas, pero el hueco que representan sigue abierto (b1), y la cifra
  de después no es 0.** Va a las decisiones del consultor (§8).
- **b', 2:** Grep sobre el Escritorio y la carpeta del usuario REALES se decide ahora como Grep
  sobre la raíz (punto 4, con `respeta_ignore`): no entra en `corpus/` ni `data/`, y en el resto
  del repo real la política no encuentra nada protegido, así que pasa, igual que Grep desde la
  raíz. Que Grep y `rg` desde fuera respetan el `.gitignore` del repo es lo que la guardia ya
  supone para ellos dentro; desde fuera no lo medí (§5).
- **b, 3 y c, 3:** Glob lista nombres (ADR-0021 §1) y `%USERPROFILE%` no lo expande nadie.

**Lo bueno:** las 97 pasan (antes, 3 negadas sin regla en PowerShell por el `?` del prefijo).

### §3.5 · `make check` y tiempos

Suite de la guardia (las tres de antes, 687 tests, Windows): **178,89 s antes, 159,41 s
después**. La segunda corrió a la vez que otras pruebas en la misma máquina: no se lee como una
mejora, sino como que no empeora. El test más lento sube de 5,82 s a 9,46 s
(`test_la_lista_de_la_guardia_es_la_que_se_calcula`, que no pasa por `_absoluta`; ruido de la
corrida simultánea). La suite nueva: 33 tests, 11,02 s. Los registros, en `fase0/pytest-antes.log`
y `fase1/pytest-despues.log`.

`make check` completo: ver §7.

## §4 · Fase 2: documentos

**Lo falso en runbooks y skills:** ninguno. La fase 0 no encontró ninguna afirmación de
`docs/runbooks/` ni de `.claude/skills/` sobre el alias de la raíz; lo que la contradice está en
el diagnóstico (§3.4, las 18 de comillas dobles), que es anexo de esta rama, y en el texto de K y
de G.1 sobre las variables de PowerShell (§0.e), que se reescribe abajo. `GUARDIA-FFMPEG.md` §9
dice que esas formas «pasan» la guardia, y era verdad: no lleva recuadro.

**Para el commit del contrato del cierre** (`RITUAL.md`, punto Y; no se toca en la rama):

1. **K de la Next Action** pierde su primera parte (la PRIORITARIA, que paga esta rama) y queda:

   > K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable
   > llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C
   > si cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los
   > dos sentidos. Y en la misma rama, el arreglo que queda de ENTRADA-JULIO.md §8: que reconozca
   > como tests los de un clon `git worktree add --detach` de comparar-con-main (`C:/cm/`), con su
   > test de los dos sentidos.

2. **G.1 de `docs/plan/HOJA-DE-RUTA.md`:** sale el punto «PRIORITARIO, porque lee material
   protegido» (líneas 428-431); `Refs` sigue con NA:K, porque K sigue. G.1 no pasa a HECHA.
3. **Technical Debt:** sale la línea del docstring de `test_tramos_fuente.py` (PROJECT_STATE.md:146,
   pagada en 38f03c4), y entra, en su sitio:

   > - Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza
   >   OSError la guardia compara la forma sin prefijos; Grep y `rg` sobre una carpeta que contiene
   >   la raíz se deciden como sobre la raíz, suponiendo, sin medirlo, que respetan su `.gitignore`.

4. **Bytes:** simulado en memoria (`scratchpad/simular_ps.py`) sobre el PROJECT_STATE de la rama:
   24.186 → **23.738** (K pierde 455 bytes, la línea de Technical Debt cambia de 276 a 283). Cabe
   bajo 25.000 con 1.262 de margen, antes de lo que el cierre cambie en Current Feature y Stable
   Main State. No hace falta recortar nada más.
5. **Registro en HISTORIA y fila de `ERRORES-RECURRENTES.md`** (RITUAL, puntos 1 y 2), con lo
   que dejen el revisor y el consultor. La señal de esta rama: una cifra de «fugas» medida en
   memoria que no se contrastó con lo que el programa de verdad abre (las 18 de comillas
   dobles); qué hacer: cada fila de «pasa» de una tabla de fugas se comprueba, una vez por
   forma, con el programa real sobre el fichero bueno del repo inventado.
6. **Declarado para la orden de cierre** (punto 7): `trabajo/guardia-ci` tocó `tests/` y no pagó la
   deuda del docstring; el consultor lo da como error suyo.

## §5 · Riesgos residuales

- **`realpath` con OSError:** se compara la forma sin prefijos (§3.1). No medí ninguna ruta que lo
  dispare en 3.12.
- **Grep y `rg` desde un contenedor:** se decide como desde la raíz con `respeta_ignore`; si
  ripgrep desde fuera NO aplicara el `.gitignore` del repo, entraría en `corpus/` y `data/`. `rg
  --no-ignore` desde fuera sí se niega (test). Sin medir con `rg` real, porque mediría sobre el
  Escritorio real.
- **Lo que el revisor encontró abierto** (§9, b1 a b7): las barras invertidas dobladas que la
  herramienta Bash deshace antes de bash, `~+` y `~-`, `/proc/cygdrive/c/`, la ruta relativa a la
  unidad `C:<rel>`, la ruta de proveedor de PowerShell `FileSystem::`, las llaves de bash y las URL
  `file:///`. Todas pasaban ya en `main`. Las decide el consultor (§8).
- **Una unidad de `subst` o mapeada** hacia una carpeta del disco del repo: la unidad sin barra de
  esa otra unidad (`D:x`) se deja pasar (§11.1), y `realpath` resuelve `subst` solo si la ruta es
  absoluta.
- **Un alias del equipo** que no sea `gethostname()` ni su parte corta (un nombre DNS propio, una
  IP de la red local) se niega como «otra máquina»: negar de más.
- **En Linux** la CI no prueba el código de prefijos ni de 8.3 (punto 6, declarado).

## §6 · El encargo del revisor

Con el informe terminado, sobre el último commit: (a) las reglas de la casa; (b) el encargo y la
respuesta a la PARADA 1, punto por punto; y, por el encargo y su punto 9, buscar cinco formas de
escribir la raíz o una carpeta que la contenga que la tabla no recoja, y además las comillas y
escapes de bash sobre la raíz (`$'…'`, `$"…"`, barras invertidas), y pasarlas por `decidir` EN
MEMORIA contra un repo inventado, sin leer nada real.

## §7 · Sello y CI

- **1422227** (el código): `make check` en Windows en verde, 2.890 passed en 1.023 s, sello sobre
  el árbol `0e03f244…`, `PICO DE MEMORIA de make check: 299 MiB en test`. Push a
  `fix/guardia-alias` (pasó, sin `!`). **CI de Linux, run 40132371656: failure**, con dos fallos:
  el esperado de state check (`test_state_check_ok_on_real_repo`) y uno mío,
  `test_powershell_resuelve_env_home_pwd_y_tilde`, «caso 6: R_ALIAS». El caso 6 es el disfraz
  `$ENV:userprofile`: en Linux el entorno distingue mayúsculas, no se resuelve y la guardia lo
  niega con `R_ALIAS`, que es lo correcto. El fallo era del test, que esperaba la regla del sitio.
  2.860 passed y 28 skipped (entre ellos los 17 de §3.2).
- **Arreglo:** ese disfraz se exige resuelto solo en Windows; en Linux se exige `R_ALIAS`.

- **ef23607** (el arreglo): `make check` en Windows en verde, 2.890 passed en 957 s, sello sobre
  el árbol `ed3e2a6a…`, `PICO DE MEMORIA de make check: 297 MiB en test`. **CI de Linux, run
  40134439368: solo el fallo esperado**, `test_state_check_ok_on_real_repo`; 2.861 passed, 28
  skipped. En Linux pasan los 16 tests de la rama que no son de Windows (punto 6).
- **El último commit** (el informe del revisor y los arreglos de a1, b8, b9 y b10, que tocan el
  test): `make check` sellado antes del commit y push a `fix/`; el número de su CI va en el mensaje
  de entrega a Aleks, para no abrir otro commit solo para escribirlo.

## §8 · El encargo, punto por punto, y lo que queda para el consultor

| # | Punto del encargo | Estado | Dónde |
|---|---|---|---|
| 1 | Base verificada (af89a78, tag en origin, CI de main, ninguna otra rama) | hecho | «Base comprobada al abrir» |
| 2 | Abrir con abrir-rama; encargo tal cual con fecha; tag F38c | hecho | c60a8d4; `docs/encargos/trabajo-guardia-alias.md` |
| 3 | Verificar el diagnóstico | hecho | §0.a |
| 4 | OBJETIVO: negar el material protegido escriba como se escriba la ruta | **parcial** | las seis formas del diagnóstico, el contenedor, las variables y los enlaces, cerrados (§3); el revisor encontró cinco formas más que bloquean y dos que importan, abiertas también en `main` (§9, b1-b7) |
| 5 | `solo_lectura.py` si la medida lo pide | hecho: no lo pide | §0.f |
| 6 | Lo bueno sigue pasando con cualquier forma de la raíz | hecho | §3.2, §3.4 (e: 0 negadas) |
| 7 | Qué no cambia | hecho | `git diff --name-status main...HEAD`: hooks, tests, docs, PROJECT_STATE, HISTORIA |
| 8 | Reglas de la rama: en memoria, rutas a trozos, PARADA ante una negativa salvo la forma propuesta | hecho | §0.0 y §3.3 (las negativas y la forma seguida) |
| 9 | Fase 0, a) a f), y PARADA | hecho (Linux de 0.c, por la CI) | §0, «Lo que necesito que decidas» |
| 10 | Fase 1: tests primero, rotos a propósito en los dos sentidos, con las dos salidas | hecho | §3.2, §3.3; b9 del revisor, arreglado |
| 11 | Un disfraz por familia | hecho | §3.2; b10 del revisor, arreglado |
| 12 | 8.3 y UNC con skip fuera de Windows, declarados | hecho | §3.2 |
| 13 | El código mínimo, con porqué y origen | hecho | §3.1 |
| 14 | La tabla del diagnóstico antes y después | hecho, corregida por el revisor | §3.4 |
| 15 | `make check` con PICO DE MEMORIA; tiempo de la suite antes y después | hecho | §3.5, §7 |
| 16 | Fase 2: lo falso en runbooks y skills | hecho: ninguno | §4 |
| 17 | Fase 2: textos para el punto Y y bytes de PROJECT_STATE | hecho | §4 (y la variante de abajo) |
| 18 | Push a fix/, CI de Linux con solo el fallo esperado, número de run | hecho | §7, run 40134439368 (y la del último commit, abajo) |
| 19 | El revisor con el informe terminado y su encargo de cinco formas, más las comillas y escapes (punto 9) | hecho | §6, §9 |
| P0-P9 | La respuesta a la PARADA 1 | hecho | §2, §3.1 |

**Lo arreglado del revisor en la rama:** a1 (la causa de las 18 filas, §3.4 y el comentario del
test), b8 (esta tabla), b9 (dos roturas más: 14) y b10 (disfraces del contenedor). a2 queda como
está: el docstring del test dice «123 lecturas protegidas que pasaban» la guardia, y es verdad; lo
que el revisor corrige es si abrían, que va en §3.4.

**Lo que necesito que decidas** (PARADA 2, ninguna de estas formas la abrió esta rama):

0. **b1, las barras invertidas dobladas** (la herramienta Bash quita un nivel de `\` antes de bash).
   Opciones: (a) en Bash y Monitor, la guardia decide también sobre el texto con un nivel de `\`
   menos, y niega si cualquiera de las dos lecturas llega a lo protegido; (b) negar en Bash toda
   ruta que empiece por `\\` (cuatro barras en el texto), como ya hace ffmpeg. Recomiendo (a): es
   la misma condición con la capa de la herramienta modelada, y (b) no cubre otras barras dentro.
   Coste de (b): menos código, más agujeros. Falta medir si PowerShell y Monitor quitan ese nivel.
1. **b2 a b5, traducciones que faltan en `_absoluta`:** `~+` y `~-` (`$PWD` y `$OLDPWD`),
   `/proc/cygdrive/X/`, la ruta relativa a la unidad `C:<rel>` (colgarla del cwd si la unidad es la
   del cwd, y si no `_no_canonizable`) y `FileSystem::` de PowerShell. Opciones: (a) se cierran aquí,
   con sus tests rotos a propósito, otro `make check`, otra CI y otra pasada del revisor; (b) una
   rama nueva, y la línea PRIORITARIA de K se queda con ellas. Recomiendo (a): leen material
   protegido, son de la misma familia que el OBJETIVO, y el arreglo de cada una es una línea de
   condición. Coste de (a): la rama se alarga (la ingesta de la sesión 5 espera).
2. **b6 y b7, las llaves de bash y las URL `file:///`:** son otro mecanismo (expansión y protocolo).
   Opciones: (a) a Technical Debt, con su evidencia, para la rama de C; (b) cerrarlas aquí.
   Recomiendo (a). Si es (b), en `file://` se recupera la ruta y se mira; en las llaves, negar un
   lector con `{…,…}` que no se expanda.
3. **Si 1 es (b):** la K del cierre no pierde su parte PRIORITARIA entera: queda «K. PRIORITARIA,
   porque lee material protegido: la guardia aún deja leer lo protegido con las barras dobladas de
   la herramienta Bash, `~+`/`~-`, `/proc/cygdrive/`, `C:<rel>` y `FileSystem::` (GUARDIA-ALIAS.md
   §9)», delante del resto de K. Medido en memoria con el mismo `simular_ps.py`: 23.960 bytes,
   1.040 de margen.

## §9 · Informe del revisor · trabajo/guardia-alias · 2026-10-24 (sobre ef23607), pegado tal cual

Revisión sobre ef23607 (árbol `ed3e2a6a…`), más la edición sin commitear de `docs/validation/GUARDIA-ALIAS.md` (§7 y Estado).

**Lo principal:** la rama hace casi todo lo que pide el encargo, pero no cumple su OBJETIVO («escriba como se escriba la ruta»). Encontré cinco formas de escribir la raíz y una vía de escape de bash que pasan la guardia sobre lo protegido. En los seis casos el programa de verdad abre el fichero bueno del repo inventado. Hay además dos formas de escribir la ruta que también abren. Todas pasan igual en `main`, así que no son regresiones: son huecos que la tabla no recoge.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | §3.4 corrige la cifra del diagnóstico: «esas 18 de a/d no eran fugas; la cifra real de antes era 105 … y queda en 0». Lo medido es cierto: con `\\?\` escrito tal cual, el `cat` de la herramienta Bash no abre. La conclusión no se sostiene, porque la herramienta quita un nivel de barras invertidas ANTES de bash, también entre comillas simples. La guardia decide sobre el texto con barras dobles, y bash recibe el prefijo bueno. Con las barras doblando el prefijo, el `cat` real abre y la guardia lo deja pasar (b1). No es la comilla doble de bash, como dicen §3.4 y el comentario de `tests/unit/test_guardia_alias.py:192-193`. | `printf '%s\|' '\\?\x' "\\?\y" '\\\\z' a\\b` → `\?\x\|\?\y\|\\z\|ab\|`, y `echo 'one\\two'` → `one\two`: un nivel menos, también entre comillas simples. Además, `cat '\\?\C:\…\Bot v3 prueba\src\botsito\cli.py'` → «No such file», y `cat '\\\\?\\C:\\…\\src\\botsito\\cli.py'` → `x = 1`. |
| a2 | menor | El docstring del test sigue diciendo «123 lecturas protegidas que pasaban»; el informe lo corrige a 105. | `tests/unit/test_guardia_alias.py:3`; `GUARDIA-ALIAS.md:499-500` |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` → «CONTRATO: 23 ficheros dentro del contrato de trabajo/guardia-alias (riesgo alto, …, 3 comprobaciones para el revisor)», exit 0.
- **pytest del contrato:** `test_guardia_alias.py` sola, 33 en verde. Las cuatro suites del contrato, exit 0 sin fallos.
- **`make check`:** `make-check.log:102` dice `SELLO: … sobre el arbol ed3e2a6ab42b961c0da0acd90d88aef283a7708e`, que es el árbol de ef23607 (`git rev-parse 'ef23607^{tree}'`). `:104` dice `PICO DE MEMORIA … 297 MiB`.
- **CI:** `gh run view 40134439368` → `failure`, headSha ef23607, `fix/guardia-alias`. Con `--log-failed`, el único fallo es `test_state_check_ok_on_real_repo` (1 failed, 2861 passed, 28 skipped).
- **Fuente:** la rama no toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout y material:** no se tocan. El informe declara «Ninguna» exposición (§0.j), lo que es coherente con que solo hubo ficheros falsos.
- **Regímenes de cambio:** no se toca ningún directorio inmutable ni `libros.yaml`. `HISTORIA.md` solo añade (168 líneas añadidas, 0 borradas).
- **Ambigüedades y ADR:** ninguno.
- **Informes cerrados:** ninguno cambiado (`GUARDIA-ALIAS.md` es `A`).
- **Las tres guardias de una `cita`:** no aplica.
- **Cifras:** no aplica, la rama no toca código de negocio.
- **Tres citas del informe contra su fuente, correctas:**
  - `PROJECT_STATE.md:146`: el docstring con dueño.
  - `PROJECT_STATE.md:105`: la línea de Artifact y claude-in-chrome.
  - `solo_lectura.py:11-16` y `:118`: «lista de lo que escribe»; solo decide sobre Bash.
  - También `DECISIONES-DE-PROCESO.md:26` y `HOJA-DE-RUTA.md:428-431`.
- **Evidencia nueva:** no hay.

### Eje (b) · Encargo
Resumen: 6 bloquea, 3 importa, 1 menor. Requisitos: 30 hechos, 4 parciales, 2 no hechos (los dos del cierre, que van después de este informe).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base verificada: af89a78, tag en origin, CI de main, ninguna otra rama | Hecho | informe, «Base comprobada al abrir» |
| 2 | Abrir con abrir-rama: encargo, contrato, Archivo en HISTORIA | Hecho | c60a8d4; HISTORIA solo añade |
| 3 | Encargo copiado tal cual, con fecha; tag F38c | Hecho | `docs/encargos/trabajo-guardia-alias.md:1-49` |
| 4 | Verificar que el diagnóstico existe y dice eso | Hecho | §0.a |
| 5 | OBJETIVO: negar escriba como se escriba la ruta | **Parcial** | b1-b5 (bloquea) y b6-b7 (importa) |
| 6 | `solo_lectura.py`, solo si la medida lo pide | Hecho (no lo pide) | §0.f; sin diff |
| 7 | Lo bueno sigue pasando con cualquier forma de la raíz | Hecho | `test_lo_bueno_pasa_con_cada_forma_de_la_raiz`; tabla e, 0 negadas |
| 8 | Qué no cambia (motor, spec, Makefile, settings, otras reglas, el resto de K) | Hecho | `git diff --name-status main...HEAD`: solo hooks, tests, docs, PS, HISTORIA |
| 9 | 0.a: copiar el diagnóstico tras comprobarlo; re-pasar `medir_k` (123) | Hecho | §0.a; anexo `diagnostico/` |
| 10 | 0.b: fichero:línea de cada llamada | Hecho | §0.b |
| 11 | 0.c: Windows, ctypes y tiempos | Hecho | §0.c |
| 12 | 0.c: Linux, `realpath` y skips | Parcial, declarado | §0.0 (`wsl` negado), §0.i; la CI de fix/ lo suple |
| 13 | 0.d: lectores recursivos | Hecho | §0.d |
| 14 | 0.e: variables | Hecho | §0.e |
| 15 | 0.f: `solo_lectura` | Hecho | §0.f |
| 16 | PARADA con tabla, propuesta y lo no clasificable | Hecho | «Lo que necesito que decidas» |
| 17 | Tests primero, cada uno roto a propósito, con las dos salidas | **Parcial** | b9 |
| 18 | Cada familia negada con su motivo | Hecho | §3.2 |
| 19 | Un disfraz por familia | Parcial | b10 |
| 20 | 8.3 y UNC con skip fuera de Windows, declarados | Hecho | `SOLO_WINDOWS`; §3.2, 17 de 33 |
| 21 | Código mínimo, con el porqué y el origen en un comentario | Hecho | `guardia.py`, bloque «la ruta canonica» |
| 22 | Tabla antes y después en el anexo | Hecho | `fase1/tabla-despues.md` |
| 23 | `make check` completo con PICO DE MEMORIA | Hecho | `make-check.log:102,104` |
| 24 | Tiempo de la suite antes y después | Hecho | §3.5 |
| 25 | Fase 2: lo falso en runbooks y skills | Hecho (ninguno) | §4 |
| 26 | Fase 2: textos para el punto Y (K, G.1, Technical Debt) y bytes de PS | Hecho | §4.1-4.4 |
| 27 | Push a fix/ y CI de Linux con solo el fallo esperado | Hecho | run 40134439368, comprobado |
| 28 | Revisor lanzado con el informe terminado, y su informe pegado al final | No hecho aún | es este informe; se pega después |
| 29 | «Rama lista para revisión, NO cerrada» | No hecho aún | Estado: «EN CURSO» (`:603`) |
| P0 | `_canonica` dentro de `_absoluta` | Hecho | diff de `_absoluta` |
| P1 | `realpath` más prefijos; test de unión y enlace en los dos sentidos | Hecho | `test_leer_por_una_union_o_un_enlace…` |
| P2 | Lo no canonizable se niega, con la forma buena | Hecho | `_no_canonizable`; test ×7 |
| P3 | Lista cerrada para la propia máquina, con el nombre leído | Hecho | `_propia_maquina` (`socket.gethostname()`) |
| P4 | Un ancestro de la raíz se decide como la raíz, con su `respeta_ignore` | Hecho | `contiene_la_raiz`, `motivo_directorio` |
| P5 | PowerShell: `$env:`, `$HOME`, `$PWD`, `~`; negar la variable sin resolver | Hecho | `_variables_powershell`; `:4304` |
| P6 | Solo en `nt`; skips; la CI enseña Linux | Hecho | run 40134439368 |
| P7 | Commit propio, docstring y declaración para el cierre | Hecho | 38f03c4; §2 |
| P8 | Artifact y claude-in-chrome, fuera de la rama | Hecho | §2 |
| P9 | El revisor añade comillas y escapes | Hecho | §6 |
| E5 | Respuestas copiadas tal cual; tabla «El encargo, punto por punto» | Copia Hecho; tabla **No** | `diff` encargo:53-68 contra informe:369-384 → IGUALES; tabla en b8 |

Hallazgos. Todo se midió en memoria con `decidir` de la rama, contra el repo inventado del fixture (espacio en el nombre, ficheros falsos en marzo, `holdout/1` y la cruda de v7), en el scratchpad. «Abre» se comprobó SOLO sobre `src/botsito/cli.py` del repo inventado. Las formas b1-b7 pasan también con la guardia de `main` (cargada de `git show main:…`): son huecos previos, no regresiones.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | **bloquea** | **Las barras invertidas dobladas en la herramienta Bash.** La herramienta quita un nivel de `\` antes de bash (a1). Con `cat '\\\\?\\<raíz>\\…'` y `cat '\\\\localhost\\C$\\…'` la guardia ve cuatro barras: `_sin_prefijos` no lo reconoce, la ruta no empieza por la raíz y pasa. Bash recibe `\\?\…` y abre. Va por Bash y Monitor. Los tests de la rama prueban la forma con dos barras, que con la herramienta real no abre. | En memoria, Q10, Q10b, Q11 y Q12 (cuatro barras con `?`, `localhost\C$` y `.`): **PASA** en Bash y en Monitor, en hold, marzo y bueno. Real con la herramienta Bash: `cat '\\\\?\\C:\\…\\src\\botsito\\cli.py'` → `x = 1`; `cat '\\\\localhost\\C$\\…\\cli.py'` → `x = 1`, rc=0. |
| b2 | **bloquea** | **`~+` y `~-`** (bash los vuelve `$PWD` y `$OLDPWD`). `_absoluta` y `resolver` los pasan por `expanduser`, que da el directorio del usuario `+` o `-`. | `cat ~+/'<HOLD>'`: PASA en Bash y Monitor, en los tres sitios. `cd '<R>/knowledge/cases' && cd .. && cat ~-/'hol''dout/1/caso.yaml'`: PASA. Real: `cat ~+/src/botsito/cli.py` y la forma con `~-` → ABRE (rc=0). |
| b3 | **bloquea** | **`/proc/cygdrive/c/…`**, el alias de unidad de MSYS. `_absoluta` solo traduce `/c/` y `/cygdrive/c/` (`guardia.py`, regex `^/(?:cygdrive/)?([a-zA-Z])…`). | `cat '/proc/cygdrive/c<R sin unidad>/<rel>'`: PASA en los tres sitios. Real sobre el bueno: ABRE (rc=0). `grep -r` sobre el contenedor escrito así sí se niega (R_SIN_ABRIR). |
| b4 | **bloquea** | **La ruta relativa a la unidad, `C:<rel>`** (sin barra tras los dos puntos). `_absoluta` no la cuelga del cwd y `_canonica` la deja «relativa», así que `relativa()` da `None`. | `C:<rel>`: PASA en un guion de Python (decidido justo tras escribirlo), Read, Grep, PowerShell y Bash `cat`, en los tres sitios. Real, con cwd en el repo inventado: `python -c "open(r'C:src\botsito\cli.py')"` ABRE; `powershell.exe … Get-Content 'C:src\botsito\cli.py'` ABRE. El `cat` de Git Bash NO abre (rc=1). |
| b5 | **bloquea** | **La ruta de proveedor de PowerShell**, `FileSystem::<raíz>\…` y `Microsoft.PowerShell.Core\FileSystem::…`: el trozo no es absoluto para `_absoluta`. | `Get-Content 'FileSystem::<R>\<rel>'`: PASA en los tres sitios; la forma larga, también. Real: `powershell.exe -Command "Get-Content 'FileSystem::<R>\src\botsito\cli.py'"` → ABRE. |
| b6 | importa | **Las llaves de bash**, `'<R>/'{<rel>,zz}`: la guardia no las expande. No es una forma de la raíz, pero el OBJETIVO dice «escriba como se escriba la ruta». | PASA en los tres sitios. Real sobre el bueno: el contenido sale por stdout (rc=1 solo por la rama `zz`). |
| b7 | importa | **Las URL `file:///`**: `python -c "urllib.request.urlopen('file:///<R>/…')"` y `curl -s 'file:///<R con %20>/…'`. Desde esta rama `candidatos_de_ruta` deja de dar un candidato a `x://…`, `file://` incluido; en `main` ya pasaban. | Las dos formas: PASA. Real: urllib ABRE; curl con `%20` ABRE (rc=0). Sin `%20`, curl no abre (rc=3). |
| b8 | importa | Falta la tabla «El encargo, punto por punto» de la skill `entregar-rama` (E5). Solo está «§2 · La respuesta, punto por punto», que cubre la respuesta a la PARADA y no el encargo. | `grep -n "punto por punto" GUARDIA-ALIAS.md` → solo `:386` y `:579` |
| b9 | importa | «Cada uno roto a propósito»: dos tests no se rompen nunca. `test_powershell_lo_bueno_y_lo_literal_pasan` (ninguna rotura de «lo bueno» la sostiene) y `test_fuera_de_windows_los_prefijos_no_se_tocan` no están en `ROTURAS`. | `tests/unit/test_guardia_alias.py:489-502` |
| b10 | menor | Disfraces: la familia del contenedor solo lleva los prefijos (`\\?\`, `//?/`), sin mayúsculas, barras mezcladas ni `.`/`..`. | `test_guardia_alias.py:265-270` |

Qué hacer con cada uno lo decide el consultor. Una lectura posible: b1 y b2 son del mismo motor (modelar la capa de la herramienta y los `~+`/`~-` de bash); b3-b5 son traducciones que faltan en `_absoluta`; b6 y b7 son de otro mecanismo (expansión y URL) y podrían ir a Technical Debt.

Las comillas y escapes de bash sobre la raíz (punto 9), probados en hold, marzo y cruda; todos niegan con la regla del sitio salvo `$'…'` con escapes:
- `$'…'` sin escapes: niega con la regla.
- `$'…'` con escapes y prefijo: niega sin R_ («el argumento `$'…'`…»). Niega, aunque sin regla con nombre.
- `$"…"`, y `$"//?/…"`.
- Barras invertidas sin comillas (`kno\wledge`, `Bot\ v3`).
- Barra invertida seguida de salto de línea a mitad de la ruta.
- Comillas pegadas (`"<R>"/'know'"ledge…"`).
- `C:\\…` sin comillas.
- `'\\?\'"<R>…"` (prefijo entre simples pegado a dobles).
- `pushd`: R_EJECUCION.
- Los flujos `::$INDEX_ALLOCATION` y `::$DATA` en Bash, Read y guion: niegan con la regla del sitio, porque `realpath` los resuelve (en `main` pasaban).
- `${C:\…}` en PowerShell: R_EJECUCION.

### Lo que no pude comprobar
- Si Read y Grep (herramientas de Claude Code) abren de verdad `C:<rel>` (b4). Solo medí la decisión de la guardia, PASA. Probarlo exigiría la herramienta real sobre una ruta relativa a la unidad; no lo intenté.
- Si Monitor y PowerShell quitan también un nivel de `\` (b1). No tengo esas herramientas cargadas. La decisión en memoria para Monitor es PASA.
- `$OLDPWD`: en memoria pasa, porque el proceso de mi Python sí tenía `OLDPWD` en el entorno. La guardia REAL negó mi `cat "$OLDPWD/…"` sobre el fichero bueno (sin regla con nombre, «se construye al ejecutarse»). No se cuenta como fuga, pero la decisión depende del entorno del hook.
- `make check`: no lo ejecuté (escribe); su evidencia es `make-check.log`. Tampoco `git write-tree`.
- `rg` real desde un contenedor: no lo medí, por la misma razón que el informe (habría que correrlo sobre el Escritorio real).
- Una unidad de `subst` o mapeada hacia el repo: haría falta cambiar el sistema.

### Comandos ejecutados
1. `git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`
2. Read: `docs/encargos/trabajo-guardia-alias.md`, `contrato.yaml`, `docs/validation/GUARDIA-ALIAS.md`, `tests/unit/test_guardia_alias.py`
3. `uv run python scripts/contrato_rama.py`
4. `git diff --name-status main...HEAD`; `git diff main -- docs/validation/GUARDIA-ALIAS.md | head -60`
5. `git diff main...HEAD -- .claude/hooks/guardia.py tests/contract/test_tramos_fuente.py PROJECT_STATE.md`
6. `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_alias.py`
7. `uv run pytest -q -p no:cacheprovider` con las cuatro suites del contrato (en segundo plano; exit 0)
8. `sed -n` y `grep -n` sobre `guardia.py`: `_absoluta`, `$'…'`, `cd`/`pushd`
9. `uv run python -` (heredoc con `'EOF'`): construye el repo inventado `…\scratchpad\rev9y5cbpqd\Bot v3 prueba` con git y ficheros falsos
10. `uv run python -` (cuatro sondas): `decidir` en memoria de la rama y de `main` (`git show main:.claude/hooks/guardia.py`); programas reales (bash `-s` y `-c`, `python -c`, `powershell.exe`, curl) solo sobre el `cli.py` del repo inventado
11. `cd <repo inventado> && cd src && cd .. && cat "$OLDPWD/botsito/cli.py"`: negado por la guardia real
12. `printf '%s|' '\\?\x' "\\?\y" '\\\\z' a\\b; echo; echo 'one\\two'`
13. `cat '\\\\?\\C:\\…\\Bot v3 prueba\\src\\botsito\\cli.py'`; `cat '\\?\C:\…\cli.py'`; `cat '\\\\localhost\\C$\\…\\cli.py'` (solo el fichero bueno inventado)
14. `ls -la make-check.log`; `grep -n "SELLO\|PICO DE MEMORIA" make-check.log`; `tail -c 300 make-check.log`; `git diff --numstat main...HEAD -- docs/state/HISTORIA.md PROJECT_STATE.md`; `grep -n "punto por punto\|…" GUARDIA-ALIAS.md`
15. `git rev-parse 'ef23607^{tree}'`; `sed -n` sobre ERRORES-RECURRENTES:94-95, PROJECT_STATE:105 y :146, DECISIONES-DE-PROCESO:26, solo_lectura.py:10-17 y :116-119, HOJA-DE-RUTA:426-432
16. `git show --stat 38f03c4`; `diff` de la respuesta (encargo:53-68 contra informe:369-384)
17. `gh run view 40134439368 --json …`; `gh run view 40134439368 --log-failed | grep …`

El repo inventado sigue en `C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Desktop-Bot-v3\76226a3b-7f68-4e43-9153-3301b3c01892\scratchpad\rev9y5cbpqd\`, fuera del repositorio; solo lleva ficheros falsos.

## §10 · Respuesta del consultor a la PARADA 2 (2026-10-24), copiada tal cual

> Respuesta del consultor a la PARADA 2 de trabajo/guardia-alias (2026-10-24). Cópiala al informe, en su sección.
>
> 0. SÍ: la guardia decide sobre el texto tal como llega y también con un nivel de \ menos (lo que hace la herramienta Bash antes de llegar a bash), en Bash y en Monitor, y niega si cualquiera de las dos lecturas llega a algo protegido. Tests en los dos sentidos con las 18 filas de barras dobladas (negadas) y su equivalente sobre src/ (pasando). Corrige en el informe la causa que diste en la fase 0, con un recuadro.
> 1. SÍ, en esta rama: ~+ y ~-, /proc/cygdrive/, C:<rel> (unidad sin barra, relativa al directorio de esa unidad) y el proveedor FileSystem:: de PowerShell, cada una con su línea de condición y su test en los dos sentidos; lo que no se pueda canonizar, negado como en el punto 2 de la respuesta 1. La ingesta espera: es mejor que entre con la guardia cerrada.
> 2. SÍ: las llaves de bash ({a,b} que componen una ruta) y las URL file:/// van a Technical Debt, juntas con la deuda C (rutas compuestas), no a K.
> 3. Con el punto 1 hecho aquí, la línea PRIORITARIA de G.1 y la parte de K que paga esta rama salen en el commit del contrato del cierre. Lo que queda de K (exigir_sin_crudo, los tests de un clon de comparar-con-main) sigue, y la línea de las llaves y file:/// entra en Technical Debt. Da la cifra de PROJECT_STATE simulada con eso; si pasa de 25.000, PARADA.
>
> Después: make check sellado, push a fix/guardia-alias y CI de Linux con un gh run view suelto, y una pasada CORTA del revisor solo sobre lo nuevo (los puntos 0 y 1, más sus cinco formas de antes, ahora negadas), con su informe pegado al final. Rama lista para revisión, NO cerrada.

## §11 · La respuesta a la PARADA 2, punto por punto

### §11.1 · El código (`.claude/hooks/guardia.py`)

| punto | pieza | línea | qué hace |
|---|---|---|---|
| 0 | `_lecturas_de_la_herramienta` y su uso en `decidir` | 1125, 4447 | Bash y Monitor se deciden sobre el texto tal como llega y, si lleva `\\`, también con un nivel de `\` menos (cada `\\` es una `\`, como lo deja la herramienta Bash); se niega si cualquiera de las dos lecturas llega a algo protegido. La segunda lectura va con un contexto nuevo |
| 1 | `_UNIDAD_MSYS` | 1087 | `/proc/cygdrive/c/…` es `C:/…`, como `/c/` y `/cygdrive/c/` |
| 1 | `_tilde_de_bash` (en `_absoluta` y en `resolver`, 1070) | 1092 | `~+` es el directorio de trabajo; `~-` (`$OLDPWD`) y `~+N`/`~-N` (la pila de `pushd`) no se saben al inspeccionar: `_no_canonizable`, `R_ALIAS` |
| 1 | `_relativa_a_unidad` (en `_absoluta`, 1140) | 1103 | solo Windows: `C:x` con la unidad del directorio de trabajo cuelga de él; con la unidad del repo pero otro directorio de trabajo, `_no_canonizable`; con otra unidad que la del repo, se deja (no puede caer bajo la raíz) |
| 1 | `_sin_proveedor` (en PowerShell, 4342) | 1119 | `FileSystem::` y `Microsoft.PowerShell.Core\FileSystem::`, en cualquier caja, se quitan antes de canonizar |

**Una decisión mía, declarada:** la unidad sin barra de OTRA unidad que la del repositorio
(`D:x`) se deja pasar en vez de negarse. Una ruta en otra unidad no puede caer bajo la raíz, que
el punto 2 de la respuesta 1 pone como condición («y pueda caer bajo la raíz», el OBJETIVO). Y
negarla negaría cualquier guion con un literal como `"x: %d"`, porque `analizar_codigo` pasa
cada literal por `_absoluta`. Riesgo: una unidad de `subst` que apunte a una carpeta del disco del
repo (§5).

### §11.2 · Los tests (`tests/unit/test_guardia_alias.py`, 50 tests, 15,6 s)

| test | qué exige | sistema |
|---|---|---|
| `test_las_barras_dobladas_de_la_herramienta_se_niegan` | las 18 filas de b1 con las barras dobladas (`\\?\`, UNC a `localhost` y `\\?\UNC\`, entre comillas simples y dobles, en Bash y Monitor, en los tres sitios): la regla del sitio; su equivalente sobre `src/`: pasa | Windows |
| `test_tilde_mas_y_tilde_menos_de_bash` | `~+` hacia el holdout en Bash y Monitor: `R_HOLDOUT`; `~+` hacia `src/`: pasa; `~-` y `~+1`: `R_ALIAS`; `~` sigue siendo la casa: pasa | los dos |
| `test_proc_cygdrive_es_la_unidad` | `/proc/cygdrive/c/<raíz>` hacia los tres sitios: la regla del sitio; hacia `src/`: pasa | Windows |
| `test_la_unidad_sin_barra_es_relativa_al_directorio_de_esa_unidad` | `C:<rel>` hacia los tres sitios en las 6 herramientas: la regla del sitio; hacia `src/`: pasa; `Z:x\y.txt`: pasa | Windows |
| `test_el_proveedor_filesystem_de_powershell` | `FileSystem::`, `Microsoft.PowerShell.Core\FileSystem::` y `filesystem::` hacia los tres sitios: la regla; hacia `src/`: pasa | los dos |
| `test_roto_a_proposito` (+10, 24 en total) | ver abajo | 4 en los dos, 6 solo Windows |

Las 96 decisiones de esos cinco tests, una por línea (forma, comillas, herramienta, regla), en
`anexos/GUARDIA-ALIAS/parada2/decisiones.txt`: 70 negadas con su regla y 26 que pasan, las 26
sobre `src/` o fuera de la raíz.

**Rotos a propósito, en los dos sentidos** (`fase1/roturas.txt`, 24 líneas, todas «falla»). Por
cada condición nueva, una rotura que la quita y otra que canoniza de más (`todo_es_la_raiz`):

| condición | sin ella | canonizando de más |
|---|---|---|
| las dos lecturas | `\\?\ · ' · Bash: pasa` | `\\?\ · ' · Bash: R_HOLDOUT` (sobre `src/`) |
| `~+` y `~-` | `caso 0 (~+ hacia el holdout, Bash): pasa` | `caso 2 (~+ hacia src, Bash): R_HOLDOUT` |
| `/proc/cygdrive/` | `caso 0 (marzo por /proc/cygdrive): pasa` | `caso 0 (…): R_HOLDOUT, se esperaba R_SIN_ABRIR` |
| `C:<rel>` | `caso 0 (marzo · Bash cat): pasa` | `caso 0 (…): R_HOLDOUT, se esperaba R_SIN_ABRIR` |
| `FileSystem::` | `caso 0 (FileSystem:: marzo): pasa` | `caso 0 (…): R_HOLDOUT, se esperaba R_SIN_ABRIR` |

**En Linux van con `skip`** las de barras dobladas, `/proc/cygdrive/` y `C:<rel>`, y sus 6
roturas. Corren en los dos sistemas `~+`/`~-` y `FileSystem::`, con sus 4 roturas.

**Las cinco formas del revisor, ahora:** b1 a b5 se niegan con la regla del sitio (b2 con `~-`, con
`R_ALIAS`). Medido en memoria sobre el repo inventado del test; nada se abrió del repo real.

### §11.3 · Lo demás

- **Regresión:** las tres suites de antes, 687 passed (223 s, con otras pruebas a la vez en la
  máquina). `PROJECT_STATE.md`: 1.690 funciones de test (+5).
- **La tabla del diagnóstico** (`medir_k.py` otra vez): idéntica a `fase1/tabla-despues.md`. Sus
  18 filas de a/d siguen pasando porque, TAL COMO están escritas, la herramienta las deja en
  `\?\…` y no abren; con las barras dobladas, que sí abren, se niegan (el test de arriba).
- **El recuadro** de la causa de la fase 0, en §0.a.
- **Las llaves y `file:///`** (punto 2): a Technical Debt, junto a la deuda C, en el commit del
  contrato del cierre (abajo); no se tocan aquí.

### §11.4 · Para el commit del contrato del cierre (sustituye a §4, puntos 1 a 4)

1. **K** pierde su parte PRIORITARIA y queda como en §4, punto 1 (`exigir_sin_crudo` y los tests de
   un clon de comparar-con-main).
2. **G.1:** sale el punto «PRIORITARIO, porque lee material protegido» (HOJA-DE-RUTA.md:428-431).
3. **Technical Debt:** sale la línea del docstring (PROJECT_STATE.md:146, pagada en 38f03c4) y
   entran dos:

   > - Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza
   >   OSError la guardia compara la forma sin prefijos; Grep y `rg` sobre una carpeta que contiene
   >   la raíz se deciden como sobre la raíz, suponiendo, sin medirlo, que respetan su `.gitignore`.
   > - La guardia no expande las llaves de bash que componen una ruta (`'<raíz>/'{a,b}`) ni mira las
   >   URL `file:///` (urllib, curl), que leen material protegido en `main` y en la rama
   >   (GUARDIA-ALIAS.md §9, b6 y b7): van con la deuda C de la Next Action (rutas compuestas).

4. **Bytes**, simulado en memoria (`anexos/GUARDIA-ALIAS/parada2/simular_ps.py`) sobre el
   PROJECT_STATE de la rama: 24.186 → **24.007**, 993 de margen bajo 25.000. K pierde 455 bytes y
   Technical Debt gana 276. Cabe: no hace falta PARADA.

## §12 · Informe del revisor · trabajo/guardia-alias · 2026-10-24 (pasada corta sobre `git diff f3a2f3e bcc70f7`), pegado tal cual

**Lo principal:** las cinco formas de mi pasada anterior (b1 a b5) se niegan ya con la regla del sitio, y su equivalente sobre `src/botsito/cli.py` pasa. No he encontrado ninguna regresión en el ritual ni en los comandos que leen datos. Quedan dos huecos que siguen leyendo material protegido, y los dos pasan igual en `main`. Uno son los disfraces de `/proc/cygdrive/` con `//` o `/./`. El otro es una forma nueva, `/proc/self/cwd/`. En los dos casos el `cat` real abrió el fichero bueno del repo inventado.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | menor | `fase1/roturas.txt` está en ISO-8859 y no en UTF-8: el `·` se ve como `�` en `git diff`. Ya lo estaba antes de este commit, y las 10 líneas nuevas siguen igual. | `file docs/validation/anexos/GUARDIA-ALIAS/fase1/roturas.txt` → `ISO-8859 text`; lo mismo con `git show f3a2f3e:…roturas.txt \| file -` |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` → «CONTRATO: 25 ficheros dentro del contrato de trabajo/guardia-alias (riesgo alto, artefacto docs/validation/GUARDIA-ALIAS.md, tramo 'Carril: guardias y deuda', 3 comprobaciones para el revisor)», exit 0.
- **pytest:**
  - `tests/unit/test_guardia_alias.py`: 50 en verde.
  - `test_guardia_claude.py`, `test_guardia_ci.py` y `test_guardia_ffmpeg.py`: exit 0 sin fallos (incluye `RITUAL` y `RITUAL_MAKE`).
- **Sello:** `make-check.log:102` dice `SELLO: … sobre el arbol 5d54c79d…`, que es `git rev-parse 'bcc70f7^{tree}'`. `:104` dice `PICO DE MEMORIA … 298 MiB`.
- **Ficheros que toca el commit:** hooks, tests, docs, el anexo y `PROJECT_STATE.md` (1685 → 1690). No toca `knowledge/`, holdout, ningún directorio inmutable ni ningún ADR. `GUARDIA-ALIAS.md` es nuevo en la rama (no es un informe cerrado).
- **Las respuestas del consultor:** la del encargo (líneas 72-79) y la del informe (817-824) son IGUALES (`diff`).
- **Las líneas que cita §11.1** (1070, 1087, 1092, 1103, 1119, 1125, 1140, 4342, 4447) corresponden al código.
- **El anexo `decisiones.txt`:** 96 líneas, de las que 26 «pasa», como dice §11.2. `roturas.txt`: 24 «falla».

### Eje (b) · Encargo (respuesta a la PARADA 2)
Resumen: 2 bloquea, 1 importa, 3 menor. Requisitos: 9 hechos, 1 parcial, 0 no hechos (3 pendientes que van después de esta pasada).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | P0: Bash y Monitor se deciden sobre el texto tal como llega y con un nivel de `\` menos; se niega si cualquiera de las dos lecturas llega a lo protegido | Hecho | `guardia.py:1125-1130` y `:4446-4448`. En memoria, b1 con 4 formas × 2 comillas × 2 herramientas: R_HOLDOUT, R_SIN_ABRIR y R_CUARENTENA; en `main`, «pasa» |
| 2 | P0: tests en los dos sentidos con las 18 filas dobladas, y su equivalente en `src/` | Hecho | `test_las_barras_dobladas_de_la_herramienta_se_niegan`; roturas `una_lectura` y `todo_es_la_raiz` |
| 3 | P0: recuadro que corrige la causa de la fase 0 | Hecho | `GUARDIA-ALIAS.md:50-57` |
| 4 | P1: `~+` y `~-` | Hecho | `:1088-1101`. En memoria: `~+` niega con la regla del sitio y `~+` hacia `src/` pasa. `~-` da R_ALIAS, también hacia `src/` (negar de más, declarado en §11.1) |
| 5 | P1: `/proc/cygdrive/` | **Parcial** | Ver b1: los disfraces pasan |
| 6 | P1: `C:<rel>` | Hecho | En las seis herramientas niega; hacia `src/` pasa; `C:..\…` desde `src` da R_HOLDOUT. La rama de `_no_canonizable` no tiene test (b3) |
| 7 | P1: `FileSystem::` y su forma larga | Hecho | Niega, con comillas y con `-LiteralPath`. `Microsoft.PowerShell.Core/FileSystem::` pasa la guardia, pero PowerShell real no la abre («No se encuentra ningún proveedor») |
| 8 | P1: lo que no se puede canonizar, negado como en la respuesta 1 | Hecho | `~-`, `~+1` y `C:<rel>` con el directorio de trabajo en otra unidad: R_ALIAS |
| 9 | P2/P3: llaves y `file:///` a Technical Debt; K y G.1 en el cierre; cifra de PS simulada | Hecho (texto preparado para el cierre) | §11.4. La cifra 24.007 no la comprobé |
| 10 | make check sellado | Hecho | `make-check.log:102` = árbol de bcc70f7 |
| — | CI de Linux, este informe pegado, «Rama lista para revisión» | Pendientes | Estado: «EN CURSO» (`GUARDIA-ALIAS.md:909`) |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | **bloquea** | **Los disfraces de `/proc/cygdrive/` pasan.** `_UNIDAD_MSYS` (`guardia.py:1087`) casa sobre el texto antes de normalizarlo. Por eso `/proc//cygdrive/c/…`, `/proc/cygdrive//c/…` y `/proc/./cygdrive/c/…` no se traducen a `C:`. Es la forma que pide el punto 1, y el encargo pedía un disfraz por familia. | En memoria, `cat '<forma>/<HOLD>'`: «pasa» en la rama y en `main`. Real, solo sobre el `cli.py` del repo inventado: con `/proc//cygdrive/c/…`, con `/proc/cygdrive//c/…` y con `/proc/./cygdrive/c/…` sale `x = 1`, rc=0. `/cygdrive//c/` y `/PROC/…` no abren (rc=1) |
| b2 | **bloquea** (va contra el OBJETIVO; no es regresión) | **`/proc/self/cwd/<rel>`** es un alias del directorio de trabajo, como `~+`, y no está entre las cinco formas. La guardia no lo traduce. | En memoria, `cat '/proc/self/cwd/<HOLD>'` con cwd en el repo inventado: «pasa» en la rama y en `main`. Real, `cat '/proc/self/cwd/src/botsito/cli.py'` → `x = 1`, rc=0. Si va aquí o a la deuda C lo decide el consultor |
| b3 | importa | **La rama `_no_canonizable` de `_relativa_a_unidad`** (la unidad del repo, con el directorio de trabajo en otra) no tiene test ni rotura. El punto 1 pide un test en los dos sentidos por cada forma. | `test_la_unidad_sin_barra_…` solo prueba la misma unidad y `Z:x\y.txt`. En memoria funciona: Read de `C:<rel>` con cwd `Z:\x` da R_ALIAS, igual hacia `src/` |
| b4 | menor | `test_proc_cygdrive_es_la_unidad` y los casos de `~-` y `~+1` solo prueban Bash, no Monitor. | `test_guardia_alias.py`, los casos de esos dos tests |
| b5 | menor | §5 dice «`C:x` en esa otra unidad se deja pasar», pero la decisión de §11.1 es sobre `D:x` (otra unidad). | `GUARDIA-ALIAS.md:588-589` frente a `:838-839` |
| b6 | menor | La segunda lectura niega `echo "x\\"`, con el motivo «una comilla doble sin cerrar», sin regla con nombre y sin decir que viene de la segunda lectura. En `main` pasaba. No hace daño: con la capa de la herramienta, bash recibe esa misma comilla sin cerrar. | En memoria, en la rama: «niega(sin R_): una comilla doble sin cerrar»; en `main`: «pasa» |

**Punto (3), la decisión de §11.1 y la segunda lectura:**
- **Lo que pasaba en `main` sigue pasando.** Comparé 22 comandos contra el repo REAL, en memoria, con la rama y con `main`. Salen IGUALES salvo b6:
  - con `\\`: `grep "…\\|…"`, `printf '%s\\n'`, `echo`, `ls` y `cat` de rutas `C:\\…`, `python -c`, `awk`, `sed`, `grep -rn '\\\\?'`, un heredoc `'EOF2'`;
  - de lectura de datos: `corpus frames show`, `corpus transcript show` (R_TRAMO en las dos), `kb find`, `kit check`, `pytest`, `make check > make-check.log 2>&1`;
  - con `~`: `echo ~-`, `echo '~-'`, `ls ~+`, `cd src && ls ~-`.
- **La unidad sin barra de otra unidad (`Z:x`) pasa y no abre nada del repo.** El único riesgo es el de `subst`, que está declarado (§5).

### Lo que no pude comprobar
- La CI de Linux de bcc70f7: no la esperé, por indicación de la sesión.
- Si Monitor quita de verdad un nivel de `\` (no tengo la herramienta), y si Read y Grep reales abren `C:<rel>`.
- En Linux, cómo resuelve `realpath` del hook `/proc/self/cwd`. Ahí `/proc/self/cwd` existe de forma nativa.
- La cifra 24.007 de PS (`simular_ps.py`): es un guion nuevo de la rama y no lo ejecuté.
- Exposiciones: ninguna. Todo se hizo sobre el repo inventado de la pasada anterior (`C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Desktop-Bot-v3\76226a3b-7f68-4e43-9153-3301b3c01892\scratchpad\rev9y5cbpqd\Bot v3 prueba`, con ficheros falsos), y los programas reales solo sobre su `src/botsito/cli.py`.

### Comandos ejecutados
1. `git branch --show-current; git status --short; git log --format='%h %s' f3a2f3e..bcc70f7; git diff --stat f3a2f3e bcc70f7`
2. `git diff f3a2f3e bcc70f7 --` de `.claude/hooks/guardia.py`, `tests/unit/test_guardia_alias.py`, el encargo, PS, `roturas.txt` y `GUARDIA-ALIAS.md`
3. `sed -n 4400,4470p` y `sed -n '/^def main/,…'` sobre `guardia.py`; `grep -n "def _no_canonizable"`; `sed -n <línea>p` de las 9 líneas de §11.1
4. Read: `GUARDIA-ALIAS.md` 1-80 y 677-911
5. `diff` del encargo (72-79) contra el informe (817-824) → IGUALES; `grep -n "comilla\|subst"` sobre el informe y el test
6. `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_alias.py` → 50 en verde
7. `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_claude.py tests/unit/test_guardia_ci.py tests/unit/test_guardia_ffmpeg.py` (en segundo plano) → exit 0
8. `ls` del scratchpad y del repo inventado; `find` con los nombres protegidos enmascarados
9. `uv run python - <<'EOF'` (×4): `decidir` en memoria de la rama y de `main` (`git show main:…`). El primero lo negó la guardia (literal `\\?\{R}`) y el tercero también (literal con `//proc`); los rehice con `chr(92)`/`chr(47)`
10. Programas reales en el repo inventado, solo sobre `cli.py`: `cat` con `/proc/self/cwd/`, `/PROC/cygdrive/`, `/proc//cygdrive/`, `/proc/cygdrive//c/`, `/cygdrive//c/` y `/proc/./cygdrive/`; `powershell.exe -NoProfile -Command "Get-Content 'Microsoft.PowerShell.Core/FileSystem::…cli.py'"`
11. `uv run python scripts/contrato_rama.py`. Antes, un comando compuesto con `f=…` lo negó la guardia (R_EJECUCION); lo partí en dos
12. `grep -n "SELLO\|PICO DE MEMORIA" make-check.log; git rev-parse 'bcc70f7^{tree}'; wc -l` y `grep -c` sobre los anexos; `file roturas.txt`, también la versión de f3a2f3e

## §13 · Lo hecho con la pasada corta

La CI de Linux de bcc70f7 (run **40140980135**) salió solo con el fallo esperado de state check:
2.868 passed y 38 skipped.

| hallazgo | qué se hizo |
|---|---|
| b1, disfraces de `/proc/cygdrive/` (bloquea) | `_sin_disfraz_posix` (en `_absoluta`): una ruta con UNA barra inicial se normaliza con `posixpath.normpath` (sin `//`, `/./` ni `..`) antes de casar `_UNIDAD_MSYS`. Una con dos barras (`//?/`, `//servidor/`) no se toca ahí. Test: cinco formas (con `//`, `/./` y `x/..`) × los tres sitios y `src/`, en Bash y Monitor |
| b2, `/proc/self/cwd/` (bloquea) | **Ampliación declarada:** no estaba entre las formas de la PARADA 2, pero es de la familia de `~+` (un alias del directorio de trabajo), lee material protegido, y la respuesta pide que la ingesta entre con la guardia cerrada. `/proc/self/cwd/` es el directorio de trabajo; `/proc/<pid>/…`, `/proc/thread-self/…` y `/proc/self/root`, `fd`, `exe`… no se saben: `_no_canonizable`. Test nuevo, `test_proc_self_cwd_es_el_directorio_de_trabajo`, en los dos sistemas |
| b3, la rama `_no_canonizable` de `C:<rel>` (importa) | test: Read de `C:<rel>` con el directorio de trabajo en otra unidad, hacia el holdout y hacia `src/`: `R_ALIAS` |
| b4, Monitor (menor) | `~-`, `~+1` y `/proc/cygdrive/` también en Monitor |
| b5, §5 (menor) | corregido: la unidad sin barra de OTRA unidad (`D:x`) |
| b6, `echo "x\\"` (menor) | se queda: la segunda lectura es lo que bash recibe de verdad, y ahí la comilla está sin cerrar. Declarado |
| a1, `roturas.txt` en ISO-8859 (menor) | los anexos `roturas.txt` y `decisiones.txt`, regenerados en UTF-8 desde el registro de pytest (que en la consola de Windows sale en cp1252) |

Roturas nuevas: `sin_disfraz_posix` contra `/proc/cygdrive/` y `/proc/self/cwd/`, y
`todo_es_la_raiz` contra `/proc/self/cwd/`. Ahora son **54 tests** y **27 roturas**, todas
«falla» (`fase1/roturas.txt`). Las decisiones de los seis tests de la PARADA 2 y de la pasada
corta están en `parada2/decisiones.txt`: 144, de las que 37 pasan, todas sobre `src/`, fuera de la
raíz o en la casa.

## Estado

EN CURSO: la respuesta a la PARADA 2 y la pasada corta del revisor aplicadas (§11, §13); falta
el sello, la CI de Linux y una pasada mínima del revisor sobre lo de §13.
