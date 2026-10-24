# Fase 0 · salidas de las medidas (2026-10-24, rama `trabajo/guardia-alias` en c60a8d4)

Todas EN MEMORIA, sobre el repo INVENTADO `Bot v3 prueba` que crea `diagnostico/medir_k.py` en la
carpeta de trabajo de la sesión (con un espacio, para que tenga nombre 8.3). `<R>` es la raíz de
ese repo inventado; `<R 8.3>`, su nombre corto; `<R/>`, con barras `/`. Nada se abrió del repo
real. Python 3.12.10 (el del sistema, el mismo que `uv run`).

## 0.a · la re-medida de `medir_k.py` sobre el HEAD de la rama

`diff` entre `diagnostico/tabla.md` (la del 2026-10-24 sin rama, sobre `main` af89a78) y la
tabla re-medida sobre c60a8d4: sin diferencias (`diff exit: 0`). `contar.py` sobre la nueva:

```
a/d: 288 filas protegidas, 117 pasan la guardia
b contenedor: 18 filas, pasan 15        (las 3 de Glob no son fuga: listar no es abrir)
b' contenedor real: 8 filas, pasan 6
c variables: 24 filas, pasan 9          (las 3 de %USERPROFILE% no son fuga: nadie lo expande)
e (lo bueno): 97 filas, negadas 3       (PowerShell con \\?\, //?/ y \\?\UNC: ver 0.g)
```

117 de a/d incluye las 18 del «espacio final», que no existen (no son fuga): 99 fugas en a/d.
99 + 12 (b, sin Glob) + 6 (b' real) + 6 (c: S con `//?/`, S en 8.3, `$env:USERPROFILE`,
`$env:CLAUDE_PROJECT_DIR`, en las dos formas de HOME) = **123**, la cifra del encargo.

## 0.f · `contar_f.py` (cuáles de las 123 pasan también por `solo_lectura.py`)

```
fugas reales (guardia.py pasa): 117      (sin las 6 de b' real, que el guion no cuenta)
Counter({'a/d': 99, 'b': 12, 'c': 6})
de ellas, decididas tambien por solo_lectura.py (Bash): 46
  pasan alli: 46; niega: 0
  por herramienta: {'Bash cat': 22, 'python guion (literal)': 18, 'Bash grep -r': 3, 'Bash find -exec cat': 3}
las otras 71 no pasan por solo_lectura.py (Read, Grep, PowerShell, Monitor): {'Read': 18, 'Grep': 21, 'Monitor cat': 18, 'PowerShell Get-Content': 11, 'Monitor grep -r': 3}
```

Más las 4 de Bash de b' real (`grep -r` y `find -exec cat` sobre el Escritorio y la carpeta del
usuario): 50 de las 123 llegan a `solo_lectura.py`, y las 50 pasan allí.

## 0.c · `tiempos.py` (ctypes: GetFullPathNameW y GetLongPathNameW), 200 llamadas por forma

| forma | GetFullPathNameW -> | t full (us) | GetLongPathNameW -> | t long (us) | existe |
|---|---|---|---|---|---|
| absoluta | `<R>\src\botsito\cli.py` | 3.6 | `<R>\src\botsito\cli.py` | 269.9 | True |
| `\\?\` | `\\?\<R>\src\botsito\cli.py` | 3.5 | `\\?\<R>\src\botsito\cli.py` | 255.3 | True |
| `//?/` | `\\?\<R>\src\botsito\cli.py` | 3.4 | `\\?\<R>\src\botsito\cli.py` | 251.9 | True |
| UNC localhost | `\\localhost\C$\<R sin unidad>\src\botsito\cli.py` | 3.5 | igual | 3908.8 | True |
| `\\?\UNC\localhost` | `\\?\UNC\localhost\C$\<R sin unidad>\src\botsito\cli.py` | 3.5 | igual | 3550.0 | True |
| 8.3 | `<R 8.3>\src\botsito\cli.py` | 3.2 | `<R>\src\botsito\cli.py` | 316.2 | True |
| punto final | `<R>\src\botsito\cli.py` | 3.0 | `<R>\src\botsito\cli.py` | 210.0 | True |
| espacio final | `<R> \src\botsito\cli.py` | 3.1 | None | 11.6 | False |
| con . y .. | `<R>\src\botsito\cli.py` | 3.1 | `<R>\src\botsito\cli.py` | 209.3 | True |
| no existe | `<R>\no\existe.txt` | 3.1 | None | 11.8 | False |
| 8.3 no existe | `<R 8.3>\no\existe.txt` | 3.0 | None | 13.0 | False |

`os.path.normpath` / `posixpath.normpath` (lo que haría Linux sin tocar el disco):

```
- absoluta: nt='<R>\\src\\botsito\\cli.py' posix='<R>\\src\\botsito\\cli.py'
- \\?\: nt='\\\\?\\<R>\\src\\botsito\\cli.py' posix='\\\\?\\<R>\\src\\botsito\\cli.py'
- //?/: nt='\\\\?\\<R>\\src\\botsito\\cli.py' posix='//?/<R/>/src/botsito/cli.py'
- UNC localhost: nt y posix dejan la ruta tal cual (en posix es un nombre con barras invertidas)
- \\?\UNC\localhost: idem
```

`Politica.relativa(_absoluta(forma, <R>))` HOY: `absoluta`, `con . y ..` y `no existe` dan
`src/botsito/cli.py` (o `no/existe.txt`); las otras ocho, `None` (fuera del repo).

## 0.c · `tiempos2.py` (`os.path.realpath`, ntpath de 3.12: GetFinalPathNameByHandle), 50 llamadas

| forma | os.path.realpath -> | t (us) | Path.resolve() -> | t (us) |
|---|---|---|---|---|
| absoluta | `<R>\src\botsito\cli.py` | 87 | igual | 112 |
| `\\?\` | `\\?\<R>\src\botsito\cli.py` | 47 | igual | 73 |
| `//?/` | `\\?\<R>\src\botsito\cli.py` | 41 | igual | 89 |
| UNC localhost | `\\localhost\C$\<R sin unidad>\src\botsito\cli.py` | 694 | igual | 1392 |
| `\\?\UNC\localhost` | `\\?\UNC\localhost\C$\<R sin unidad>\src\botsito\cli.py` | 311 | igual | 1111 |
| UNC 127.0.0.1 | `\\127.0.0.1\C$\<R sin unidad>\src\botsito\cli.py` | 873 | igual | 1331 |
| 8.3 | `<R>\src\botsito\cli.py` | 85 | igual | 115 |
| punto final | `<R>\src\botsito\cli.py` | 81 | igual | 110 |
| espacio final | `<R>\src\botsito\cli.py` | 199 | igual | 234 |
| con . y .. | `<R>\src\botsito\cli.py` | 79 | igual | 112 |
| no existe | `<R>\no\existe.txt` | 150 | igual | 187 |
| 8.3 no existe | `<R>\no\existe.txt` | 151 | igual | 185 |
| `\\?\` no existe | `\\?\<R>\no\existe.txt` | 121 | igual | 172 |
| otra máquina (`\\otra-maquina\C$\x\y.txt`) | tal cual | 378 | igual | 513 |
| dispositivo (`\\.\C:\x\y.txt`) | `C:\x\y.txt` | 109 | igual | 133 |

`os.name: nt | sep: '\\' | altsep: '/'`.

## 0.e y 0.g · `ps_motivo.py` (PowerShell, por qué niega sin regla y por qué pasa `$env:`)

```
- src con \\?\: 'PowerShell lee contenido de rutas que solo se saben al ejecutar (variables, comodines o -Recurse) y puede llegar a material protegido. ...'
- src con //?/: (el mismo motivo)
- src absoluta: 'pasa'
- src con $env:USERPROFILE (no cae): 'pasa'
- src con $HOME: 'pasa'
- src con $r propia: "`$r = '<R>...` en PowerShell: no se admite ninguna ejecucion (su lista cerrada esta vacia). Regla: encargo de `trabajo/guion-mismo-comando` ..."
- gci -Recurse sobre el contenedor: (el motivo de «rutas que solo se saben al ejecutar»)
- gci -Recurse sobre src: (el mismo)
```

El «niega sin regla» de `\\?\` y `//?/` sobre `src/` sale de `guardia.py:4175-4180`: el `?` del
prefijo casa el comodín `[*?]` de «dinámico», y la carpeta de trabajo de la sesión está bajo
`AppData\`, que contiene `data\`, una palabra de `SENSIBLES`. Con la raíz real (`Desktop\Bot v3`)
ese mismo `\\?\` sobre `src/` PASA en PowerShell (no hay palabra sensible), y sobre un fichero
protegido se niega sin regla (la palabra sensible es la del material). No es un fallo de la
medida: es la misma comprobación tosca, y la condición nueva la vuelve una decisión con regla.

## Comandos negados durante la fase 0

1. `mkdir -p <scratchpad>/diagK; wsl --status ...; wsl -e python3 --version` (un solo comando):
   negado por `R_EJECUCION` («ejecutar `wsl`: antes, en el mismo comando, va `mkdir`»). Se siguió
   la forma que propone la guardia: una llamada por comando.
2. `wsl -e python3 --version` (suelto): negado por `R_EJECUCION` («`wsl` lanza `python3`, y lo que
   ejecute no se ve por sus argumentos»). No hay forma propuesta que valga: la medida de Linux
   (0.c) queda sin hacer en local y la hará la CI de `fix/guardia-alias`.
