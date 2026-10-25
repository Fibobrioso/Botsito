# Diagnóstico de K · el alias de la raíz en `motivo_fichero` (2026-10-24, sin rama)

Medido sobre `main` en `af89a78` (tras el cierre de `stable/F38b-guardia-ci`), EN MEMORIA: cada
forma por `decidir` de `.claude/hooks/guardia.py` y, para Bash, por `motivo` de
`.claude/hooks/solo_lectura.py`. Nada se ejecutó de verdad sobre material protegido ni sobre el
repo; ningún fichero del repo cambió.

## Cómo se midió

- `medir_k.py` (esta carpeta). Como los tests (`tests/unit/test_guardia_ci.py`), sobre un repo
  INVENTADO en esta carpeta, `Bot v3 prueba` (con espacio, para que tenga nombre 8.3:
  `BOTV3P~1`), con la estructura del real y ficheros falsos SIN SEGUIR en tres sitios protegidos:
  la carpeta de marzo (`R_SIN_ABRIR`), `knowledge/cases/holdout/1/` (`R_HOLDOUT`) y la cruda de v7
  (`R_CUARENTENA`). Hizo falta: la guardia de Bash solo mira rutas que EXISTEN (la primera pasada,
  con ficheros que no existían, daba «pasa» hasta en la forma relativa; la descarté).
- Las rutas protegidas se montaron a trozos y no se imprimen; la tabla dice forma, herramienta y el
  nombre de la regla.
- Metadatos de verdad (los únicos): el nombre 8.3 de la raíz REAL, `C:\Users\USER\Desktop\BOTV3~1`
  (`GetShortPathNameW`), y las variables que ve el shell: `HOME=/c/Users/USER` (forma Git Bash),
  `USERPROFILE=C:\Users\USER`, `CLAUDE_PROJECT_DIR` vacía en el shell (Claude Code la pone solo en el
  entorno del hook; la guardia la resuelve a la raíz). Las variables se midieron con `HOME` en las
  dos formas.
- `existe.py`: que cada forma llega de verdad al mismo fichero (`os.path.exists`, sobre el repo
  inventado): `\\?\`, `//?/`, `\\localhost\C$`, `\\?\UNC\localhost\C$`, el 8.3 y el punto final,
  SÍ; el espacio final, NO (Windows no lo quita en un tramo intermedio): sus «pasa» no son fuga.
- El bloque b) también contra el Escritorio y la carpeta del usuario REALES con la política del
  repo real (`b'`): la guardia solo mira si el directorio contiene zonas protegidas; no se abre nada.
- Las tres pasadas del guion tuvieron dos errores míos, corregidos antes de contar: la herramienta
  se pasaba con su etiqueta («Bash cat») y salía «pasa» siempre; y el borrado del repo inventado
  (objetos de git de solo lectura).

## Cuántas formas pasan hoy

**Tabla completa: `tabla.md` (436 filas). Recuento: `contar.py`.**

### a) y d): la raíz en sus formas, en las seis herramientas (Bash `cat`, Read, Grep, PowerShell `Get-Content`, Monitor `cat`, un guion de Python con el path en un literal entero), sobre tres ficheros protegidos: 288 filas, 117 pasan

| forma | ¿alias real? | pasa en | se niega en |
|---|---|---|---|
| relativa, absoluta `\` y `/`, Git Bash `/c/`, barras mezcladas, mayúsculas, minúsculas, `.` y `..`, por fuera y `..` | sí | ninguna | las seis (`R_SIN_ABRIR`/`R_HOLDOUT`/`R_CUARENTENA`) |
| `\\?\` | sí | Bash, Read, Grep, Monitor, Python | PowerShell («niega» sin regla: lo niega su análisis tosco, también para `src/`) |
| `//?/` | sí | Bash, Read, Grep, Monitor, Python | PowerShell (ídem) |
| `\\localhost\C$\…` (UNC a la propia máquina) | sí | **las seis** | — |
| `\\?\UNC\localhost\C$\…` | sí | Bash, Read, Grep, Monitor, Python | PowerShell (ídem) |
| **8.3 de la raíz** (`BOTV3P~1`; la real es `BOTV3~1`) | sí | **las seis** | — |
| **punto final** (`…\Bot v3 prueba.\…`) | sí | **las seis** | — |
| espacio final (`…\Bot v3 prueba \…`) | **no** (no existe) | las seis | — (no es fuga) |

**Fugas reales en a)/d): 99 filas, seis formas** (`\\?\`, `//?/`, UNC, `\\?\UNC`, 8.3 y punto
final), en Read y Grep de Claude Code también, y en Monitor. `solo_lectura.py` deja pasar todas las
lecturas (vigila escrituras); para los agentes manda `guardia.py`, que corre también para ellos.

### b) un directorio que CONTIENE el repo: 18 filas (inventado) + 8 (real), 21 pasan

| directorio | `grep -r` | `find … -exec cat` | Grep | Monitor `grep -r` | PowerShell `gci -Recurse \| gc` | Glob |
|---|---|---|---|---|---|---|
| el que contiene el repo inventado | **pasa** | **pasa** | **pasa** | **pasa** | niega (sin regla) | pasa (listar nombres no es abrir, ADR-0021 §1: no es fuga) |
| la carpeta de encima | **pasa** | **pasa** | **pasa** | **pasa** | niega | pasa (ídem) |
| el primero, con `\\?\` | **pasa** | **pasa** | **pasa** | **pasa** | niega | pasa (ídem) |
| **Escritorio REAL** (política real) | **pasa** | **pasa** | **pasa** | — | niega | — |
| **usuario REAL** | **pasa** | **pasa** | **pasa** | — | niega | — |

**Fugas reales en b): 18** (las de Glob, no). Un lector recursivo sobre una carpeta que contiene la
raíz no se mira como una lectura recursiva de la raíz.

### c) las variables: 24 filas, 9 pasan

| forma | Bash (`HOME` Git Bash) | Bash (`HOME` Windows) | PowerShell |
|---|---|---|---|
| `$HOME`, `$USERPROFILE`, `${USERPROFILE}`, `$CLAUDE_PROJECT_DIR`, `~` | niega | niega | `$HOME` niega (sin regla), `~` niega (`R_SIN_ABRIR`) |
| `%USERPROFILE%` | pasa | pasa | pasa — **no es fuga**: ni Bash ni `Get-Content` lo expanden |
| `$env:USERPROFILE` | — | — | **pasa** |
| `$env:CLAUDE_PROJECT_DIR` | — | — | **pasa** |
| variable propia `S="<raíz>"` | niega | niega | `$r = '<raíz>'`: niega (`R_EJECUCION`, `{`/asignación) |
| variable propia `S="//?/<raíz>"` | **pasa** | **pasa** | — |
| variable propia `S="<raíz 8.3>"` | **pasa** | **pasa** | — |

**Fugas reales en c): 6.** Las variables de Bash se resuelven bien con el entorno, en las dos formas
de `HOME`; lo que pasa es la VARIABLE CON UN ALIAS (vuelve a a)) y `$env:` en PowerShell, que el
análisis de PowerShell no resuelve.

### e) lo bueno: 97 filas, 3 negadas

Un fichero de `src/` pasa en todas las formas y herramientas, y `grep -r x docs/` pasa, salvo
PowerShell `Get-Content` con `\\?\`, `//?/` y `\\?\UNC` (niega sin regla, como en a)). Es la línea
de base que la condición nueva no puede empeorar.

## La propuesta: una sola condición

**Toda ruta se compara en su forma CANÓNICA, y lo que no se puede canonizar se niega.** Una función,
`_canonica(ruta, cwd)`, en el único sitio por el que pasan todas (`_absoluta`, que usan
`motivo_fichero` y `motivo_ruta` vía Bash, Read, Grep, PowerShell, Monitor y `analizar_codigo`):

1. Quitar los prefijos de dispositivo y de la máquina propia: `\\?\` y `//?/`; `\\?\UNC\<host>\<X>$\`
   y `\\<host>\<X>$\` con `<host>` en {`localhost`, `127.0.0.1`, `::1`, el nombre del equipo} → `X:\`.
   Un UNC a OTRA máquina o un `\\.\` (dispositivo) no se canoniza: si la ruta podría estar bajo la
   raíz, se niega.
2. `GetFullPathNameW` (Windows: resuelve `.`, `..`, las barras y los puntos finales que quita el
   sistema; en Linux, `os.path.abspath`).
3. `GetLongPathNameW` sobre el prefijo más largo que exista (deshace el 8.3; en Linux,
   `os.path.realpath`, que resuelve los enlaces).
4. `normcase`, y la comparación contra la raíz canónica, calculada una vez.

Y dos cosas que caen de la misma condición:

- **Un contenedor de la raíz:** si un lector RECURSIVO (`grep -r`, `rg`, `find … -exec`, Grep,
  `gci -Recurse`) apunta a una ruta canónica que CONTIENE la raíz canónica, se mira como una lectura
  recursiva de la raíz (`motivo_ruta(raíz, recursivo=True)`): se niega si alcanza material
  protegido.
- **PowerShell:** `$env:NOMBRE`, `$HOME` y `~` se resuelven con el entorno como en Bash (`resolver`);
  una variable que no se resuelve en una ruta, se niega.

Cierra a)-d): las 99 de a)/d), las 18 de b) y las 6 de c). No cambia e).

## Los tests que la romperían en los dos sentidos

Para un `tests/unit/test_guardia_alias.py` (repo de `tmp_path` con espacio en la raíz, como este):

1. **Cada forma de a)** (`\\?\`, `//?/`, UNC a `localhost`, `\\?\UNC`, 8.3, punto final) × las seis
   herramientas × los tres sitios protegidos: se niega con la regla del sitio (no sin regla).
   **Roto:** con `_canonica` cambiada por la identidad, vuelven a pasar (las 99 de hoy).
2. **Lo bueno** (`src/` en las mismas formas; `grep -r x docs/`): pasa. **Roto en el otro sentido:**
   con una `_canonica` que devolviera siempre la raíz, lo bueno se negaría.
3. **El contenedor:** `grep -r`, `find -exec cat`, Grep y Monitor sobre la carpeta que contiene la
   raíz (y con `\\?\`), se niegan; sobre una carpeta hermana sin el repo, pasan. **Roto:** sin la
   comprobación de contenedor, pasan.
4. **Variables:** `S="//?/<raíz>"` y `S="<8.3>"` en Bash, y `$env:USERPROFILE`/
   `$env:CLAUDE_PROJECT_DIR` en PowerShell, se niegan; `%USERPROFILE%` (literal) sigue pasando.
   **Roto:** sin resolver `$env:`, pasan.
5. **Lo que no se canoniza:** `\\otraMaquina\C$\…` y `\\.\…` con una ruta que podría estar bajo la
   raíz: se niegan con su mensaje.
6. **Solo Windows** (8.3, UNC, `GetLongPathNameW`): con `skipif` en Linux y dicho en el informe; en
   Linux, los mismos textos son nombres de fichero raros y la canonización tiene que dejarlos como
   están (la lección de D5 en `trabajo/guardia-ci`: la tabla «antes» se mide en los dos sistemas).
7. **Regresión contra `main`:** las formas de lectura que pasan hoy en `main` (los 32 de RITUAL, los
   lectores de `NO_EJECUTAN` y `rg`, la lección de b5) siguen pasando.

## Lo que no medí

- PowerShell de verdad: la herramienta no está cargada en esta sesión; se midió su análisis en
  memoria. La sesión tampoco se probó con `HOME` en forma Windows de verdad (solo en memoria).
- Un UNC a otra máquina, `\\.\`, los enlaces simbólicos y las uniones (`mklink /J`) dentro del repo.
- Si el hook recibe el `cwd` siempre absoluto (en `trabajo/guardia-ci` se vio que con `cwd` `.` la
  guardia no reconoce `tests/` ni el Makefile de `main`).
