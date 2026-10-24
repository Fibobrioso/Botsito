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

## Estado

EN CURSO: fase 0 hecha; PARADA 1, a la espera de la respuesta del consultor a «Lo que necesito
que decidas». Sin código de la guardia escrito.
