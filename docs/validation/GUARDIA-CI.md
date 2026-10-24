# GUARDIA-CI · la guardia niega esperar a la CI con una consulta repetida

Rama: `trabajo/guardia-ci`, abierta el 2026-10-23 desde `main` en `2a99e64` (commit de estado
sobre el merge `975c086`, tag `stable/F38a-guardia-ffmpeg`). Encargo:
`docs/encargos/trabajo-guardia-ci.md`. Carril de guardias y deuda; paga la línea de Technical Debt
de `PROJECT_STATE.md` «La guardia no niega un guion que espera a la CI en bucle» (la deuda vive
solo en Technical Debt, no en G.1 de la hoja de ruta, y el cierre no añade nada a G.1). Tag de
cierre previsto: `stable/F38b-guardia-ci`.

## Base comprobada al abrir

- `git fetch origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `2a99e64fa00d1ff4b0c45ee659614f1a21e2d110` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38a-guardia-ffmpeg^{commit}"` =
  `975c0863c1efbb567db7e9086590e7b67efec15e`; el tag está en origin
  (`git ls-remote --tags origin stable/F38a-guardia-ffmpeg`:
  `171d0d9e478e2addfa2212f817ff697e41910edf refs/tags/stable/F38a-guardia-ffmpeg`, el objeto del
  tag anotado).
- CI de `main` sobre su HEAD, por la API de check-runs con el sha de 40 caracteres escrito tal
  cual: job `python`, `completed` / `success`, run 39893825671.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.
- La línea de Technical Debt sigue abierta: `PROJECT_STATE.md:104`.

## 0. Fase 0 (2026-10-23)

Sin código en el repositorio. Las medidas, con dos guiones que cargan la guardia de `main` (igual
que la de la rama: la rama aún no la toca) y llaman a `decidir` en memoria, como
`tests/unit/test_guardia_claude.py` y `test_guardia_ffmpeg.py`; ninguno ejecuta un comando de la
tabla ni consulta la CI. Copiados en `docs/validation/anexos/GUARDIA-CI/` (`tabla_fase0.py`,
`esperar_run.py`, `pytest_lee.py`) con su salida, y junto a ellos las dos copias de los guiones del
incidente (`esperar_run_original.py` y `.sh`), que nunca se ejecutan.

### 0.a Cómo trata hoy la guardia cada forma

`<run>` = 39893825671 (el de la CI de `main` sobre `2a99e64`), `<API>` =
`https://api.github.com/repos/Fibobrioso/Botsito`, `<sha>` = el de `2a99e64`, de 40 caracteres.
«Pasa» es `decidir` → `None`. Las filas N10-N18 y B7-B12 son ampliaciones de esta fase 0.

| id | comando | debería | hoy | motivo de hoy |
|---|---|---|---|---|
| N1 | `while true; do gh run view <run> --json status; sleep 30; done` | negar | **pasa** | — |
| N2 | `until gh run view <run> --exit-status; do sleep 30; done` | negar | **pasa** | — |
| N3 | `for i in 1 2 3; do gh run view <run>; sleep 30; done` | negar | niega | otra regla: `R_EJECUCION`, «el bucle `for` fija `i`, que no esta en la lista (`NOMBRES_DE_ENTORNO`)» |
| N3b | lo mismo con `for n in ...` (`n` SÍ está en `NOMBRES_DE_ENTORNO`) | negar | **pasa** | — |
| N4 | `gh run view <run> && sleep 30 && gh run view <run>` | negar | **pasa** | — |
| N5 | `gh run watch <run>` | negar | **pasa** | — |
| N5b | `gh run watch <run> --exit-status` | negar | **pasa** | — |
| N6 | `watch -n 30 gh run view <run>` | negar | **pasa** | — |
| N7 | `python -c` con `subprocess.run(['gh','run','view',...])` y `time.sleep(30)` en un `while True` | negar | **pasa** | — |
| N7b | lo mismo en una línea, con una lista por comprensión | negar | **pasa** | — |
| N8 | `python <scratchpad>/esperar_run.py <run>` (rehecho desde EA-CONEXION.md §13: `gh run view --json` cada 30 s en un `while True`) | negar | **pasa** | — |
| N8b | `uv run python <scratchpad>/esperar_run.py <run>` | negar | **pasa** | — |
| N9 | PowerShell: `for ($i = 0; ...) { gh run view <run>; Start-Sleep -Seconds 30 }` | negar | niega | otra regla: `R_EJECUCION`, «un bloque de codigo `{ ... }` en PowerShell: no se admite ninguna ejecucion» |
| N9b | PowerShell: `while ($true) { gh run view <run>; Start-Sleep 30 }` | negar | niega | ídem |
| N9c | PowerShell: `gh run view <run>; Start-Sleep 30; gh run view <run>` | negar | niega | otra regla: `R_EJECUCION`, «`gh run view ...` en PowerShell: no se admite ninguna ejecucion» |
| N10 | `while true; do curl -s <API>/commits/<sha>/check-runs \| grep -o ...; sleep 30; done` | negar | **pasa** | — |
| N11 | `while true; do gh api repos/.../actions/runs/<run> --jq .status; sleep 30; done` | negar | **pasa** | — |
| N12 | `timeout 600 gh run watch <run>` | negar | **pasa** | — |
| N13 | `gh run view <run>; sleep 30; gh run view <run>` | negar | **pasa** | — |
| N14 | `gh pr checks 12 --watch` | negar | **pasa** | — |
| N15 | `sleep 300 && gh run view <run> --json status,conclusion` | ¿? (abajo, decisión 2) | pasa | — |
| N16 | `sleep 300; gh run view <run>` | ¿? (decisión 2) | pasa | — |
| N17 | `until curl -s <API>/commits/<sha>/check-runs \| grep -q completed; do sleep 30; done` | negar | **pasa** | — |
| N18 | `while sleep 30; do gh run view <run>; done` | negar | **pasa** | — |
| N8c | `python <anexo>/esperar_run_original.py <run>`: el guion REAL del incidente (EA-CONEXION.md §13), que el auditor encontró en el scratchpad de aquella sesión; copiado tal cual | negar | **pasa** | — |
| N8d | `sh <anexo>/esperar_run_original.sh <run>`: su versión en shell, la que la guardia negó entonces | negar | niega | otra regla: `R_EJECUCION`, «el nombre de entorno `run` no esta en la lista cerrada (`NOMBRES_DE_ENTORNO`)» (su `run="$1"`), no por el bucle |
| N19 | `python -c` con `subprocess.run(['curl','-s','<API>/commits/<sha>/check-runs'])` y `time.sleep(30)` en un `while True` (la familia de corrida-construccion, SESGO-H4-COLOR.md:1301) | negar | **pasa** | — |
| B1 | `gh run view <run> --json status,conclusion,headSha` | pasar | pasa | — |
| B2 | `gh run view <run> --log-failed` | pasar | pasa | — |
| B3 | `gh run view <run> --exit-status` | pasar | pasa | — |
| B4 | `gh run list --branch fix/x` | pasar | pasa | — |
| B5 | `gh run rerun <run>` | pasar | pasa | — |
| B6 | `sleep 120` | pasar | pasa | — |
| B7 | la de RITUAL.md:317: `curl -s --ssl-no-revoke <API>/commits/$(git rev-parse HEAD)/check-runs \| grep -o '"status"...'` | pasar | pasa | — |
| B8 | la de abrir-rama: `curl -s <API>/commits/<sha>/check-runs \| grep -E '"(name\|status\|conclusion\|html_url)"'` | pasar | pasa | — |
| B9 | `gh run list --branch fix/guardia-ci --limit 3` | pasar | pasa | — |
| B10 | `gh api repos/.../actions/runs/<run> --jq .status` | pasar | pasa | — |
| B11 | `gh run view <run> --log-failed \| tail -50` | pasar | pasa | — |
| B12 | `gh run view <run> --json jobs --jq '.jobs[].conclusion'` | pasar | pasa | — |
| B13 | la de `docs/HANDOFF.md:1051`: `curl -s <API>/commits/<sha>/check-runs` (auditor, H3) | pasar | pasa | — |

De las 25 formas que deberían negarse, hoy pasan 20; las cinco que se niegan (N3, N8d, N9, N9b,
N9c) lo hacen por otra regla (la variable del `for`, una asignación fuera de la lista o PowerShell
entero), y N3b enseña que la regla del `for` no es esta: con `n`, que está en la lista, el mismo
bucle pasa. El guion real del incidente (N8c) pasa hoy. Las dos dudosas (N15, N16) y las 13 buenas
pasan. Salida entera: `anexos/GUARDIA-CI/tabla_fase0-ANTES.txt`; los sha256 de las dos copias del
incidente: `esperar_run_original.py` `6bc9e0b2…d47530`, `esperar_run_original.sh`
`d2223984…a897d1`.

**Tiempo de la suite de la guardia antes del cambio:** `uv run pytest -p no:cacheprovider
tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py` → `572 passed in 181.20s`.

### 0.b Lo que la guardia ya ve, y dónde encaja la condición

- **El tokenizador** (`tokenizar`, `guardia.py:662-849`) deja `while`, `until`, `for`, `do` y
  `done` como palabras; `comandos` (`:868-926`) se salta las de `PALABRAS_CLAVE` (`:864`:
  `while`, `until`, `do`...) y `FINALES` (`:865`) al principio de un comando, así que de
  `while true; do gh run view X; sleep 30; done` salen tres comandos sueltos (`true`, `gh ...`,
  `sleep 30`) y **el bucle desaparece**. `for` no está en `PALABRAS_CLAVE`: `analizar_bash` lo
  trata aparte (`:1113-1129`) y solo para mirar su variable (`_exigir_for`, `:2694`). Ninguna
  pieza junta «hay un bucle» con «lo que va dentro».
- **`sleep`** está en `NO_EJECUTAN` (`:2250`) y en `LECTOR_DE_METADATOS` (`:933`): pasa siempre,
  vaya donde vaya. **`watch`** no está en ninguna lista: es un programa desconocido
  (`_ejecucion_de_un_programa_desconocido`, `:2910`), que solo se niega si un argumento es un
  fichero que existe o lanza un intérprete; `gh run view` no lo es, y pasa.
- **`gh`** está en `NO_EJECUTAN` (`:2256`) y en `SIN_LECTURA_DE_RUTAS` (`:940`); `_modo_que_ejecuta`
  (`:2494-2501`) solo mira que el subcomando esté en `GH_SUBCOMANDOS` (`:2304`: `run` y `api`
  están), así que `gh run watch` pasa. **`curl`** igual (`:2255`), y solo se mira un `@fichero`
  (`:1468-1474`).
- **`analizar_codigo`** (`:3565-3599`) mira los literales que son rutas y si el código recorre
  directorios; no mira ni llamadas a programas ni bucles. Es la que analiza `python -c`, un
  heredoc a un intérprete y un guion que no es el de `main` (`_exigir_guion_legible`, `:3442`); un
  `.sh` va a `analizar_bash` (`:3480-3481`).
- **PowerShell** (`analizar_powershell`, `:3698`) niega toda ejecución (`_ejecucion_en_powershell`,
  `:3647`), y `gh` no está en `PS_NO_EJECUTAN` (`:3635`): ya se niega todo, pero con el motivo de
  `R_EJECUCION`.
- **`decidir`** (`:3776`) solo despacha por herramienta.

**Dónde encaja con el menor cambio:** una función nueva, `_exigir_sin_espera_a_la_ci`, con su
regla `R_ESPERA_CI` y su `COMO_ESPERAR_CI` (el texto del encargo), llamada en tres sitios y al
PRINCIPIO de cada uno, para que su motivo gane al de `_exigir_for` y al de PowerShell (los tests
comprueban el motivo):

1. `analizar_bash`, justo después de `tokenizar` (`:1082`). Como `analizar_bash` es también la
   que analiza `bash -c`, un `.sh` y cada `$(...)`, la condición vale en todos los niveles.
2. `analizar_codigo`, al principio (`:3568`): `python -c`, heredocs y guiones sin revisar.
3. `analizar_powershell`, al principio (`:3701`).

No hace falta un analizador nuevo: en Bash se usan `tokenizar`, `comandos` y
`_quitar_envoltorios`; en código, `_literales` (`:3602`) y el texto.

### 0.b' La guardia de los agentes (`solo_lectura.py`)

`solo_lectura.py` niega `curl` (está en `ESCRIBEN`, `:31-35`) y deja `gh` y `sleep`: un
subagente con solo `solo_lectura.py` podría esperar con `while true; do gh run view X; sleep 30;
done`. Pero `guardia.py` corre TAMBIÉN para los subagentes (`solo_lectura.py:11-12`: «La guardia
del proyecto (`guardia.py`) sigue corriendo ademas para todo, tambien para estos agentes»; es el
`PreToolUse` de `.claude/settings.json`, sin filtro por agente). **Propuesta: la regla va solo en
`guardia.py`** (decisión 8), que los cubre a los dos; duplicarla en `solo_lectura.py` es una segunda copia que
mantener. Que el hook del proyecto corre para los subagentes no lo mide ningún test de este
repositorio (no se puede lanzar un subagente desde pytest); lo dice la cabecera de
`solo_lectura.py`, y lo vio el auditor de esta fase 0, al que `guardia.py` le bloqueó un comando
(su informe, H11). Medido también por él: hoy `solo_lectura.motivo()` da `None` para
`while true; do gh run view 1; sleep 30; done` y para `gh run watch 1`, y niega `curl` (está en
`ESCRIBEN`).

### 0.b'' Un hueco que esta rama no cierra: la herramienta `Monitor`

El matcher del hook es `Read|Grep|Glob|Bash|PowerShell` (`.claude/settings.json`, `PreToolUse`).
Esta sesión tiene además la herramienta `Monitor`, que ejecuta un comando de shell
(`command`) y cuya propia documentación pone de ejemplo, literalmente, un `while true` que llama a
`gh api` y `gh pr checks` cada 30 s. **La guardia no la ve en absoluto**: ni para la CI ni para
el material protegido. No la he usado. Decisión para el consultor (decisión 0).

### 0.c Qué mandan los runbooks y las skills

| sitio | forma | con la regla propuesta |
|---|---|---|
| `docs/runbooks/RITUAL.md:317-320` | `curl ... /commits/$(git rev-parse HEAD)/check-runs \| grep -o ...`; «se espera y se repite la misma línea» | pasa (B7): la consulta va sola y la repetición es a mano |
| `docs/runbooks/RITUAL.md:110` | `gh run rerun <run>` | pasa (B5) |
| `.claude/skills/abrir-rama/SKILL.md:38`, `:54-57` | la API de check-runs con el sha literal | pasa (B8) |
| `.claude/skills/entregar-rama/SKILL.md:41`, `:66-72` | `gh run list --branch fix/<x>`, check-runs con el sha literal, `gh run view <run> --log-failed`, `gh run rerun <run>`; «esperar el run» sin decir cómo | pasan (B2, B4, B5, B8); «esperar» no dice cómo, y la regla le da la forma |
| `.claude/skills/cerrar-rama/SKILL.md:36`, `:55`, `:94` | `gh run list --branch fix/<x>`, `curl` contra la API o `gh run` | pasan |

Ninguno dice `gh run watch` ni un bucle: no hay nada falso que corregir. Una mejora que propongo
(decisión 5): una línea en `entregar-rama` paso 7 y en `RITUAL.md` junto a «se espera y se repite la misma
línea», con la forma del mensaje de la guardia, para que «esperar» no se lea como un bucle. Las
formas sueltas que no estaban en el encargo: B9-B12 (`gh run list --limit`, `gh api` suelto,
`--log-failed | tail`, `--json jobs --jq`), que salen de informes de ramas anteriores; pasan hoy y
tienen que seguir pasando.

### 0.d Los sitios de la limpieza de V

- `PROJECT_STATE.md:54`, la línea de V: «Depende de R1.1, de R3.1 y de la copia de seguridad (A.4).»
- `docs/plan/HOJA-DE-RUTA.md:219-221`, el «Depende de» de R4.1: «R1.1, R3.1 (HECHA), R1.2 (HECHA),
  R3.2 (HECHA), R3.3 (HECHA), R3.4 (HECHA) y / la copia de / seguridad del carril de Aleks.», partido
  en tres líneas (no en dos), sin «A.4».
- A.4 está HECHA: `docs/plan/HOJA-DE-RUTA.md:420` («Estado: HECHA (2026-10-22, Aleks: ...)»).
- **Un tercero vivo**, que no es una dependencia de V pero dice lo contrario:
  `docs/sesion-5/PREGUNTAS.md:8-9`, «**Antes de grabar: la copia de seguridad A.4** ... La sesión 5
  depende de ella y hoy no está hecha.» (decisión 4).
- El resto de apariciones son informes cerrados que citan la línea de su momento (BARRIDO-SESION-5,
  CORRIDA-CONSTRUCCION, VISOR-CONSTRUCCION, PUNTO-USADO, SESGO-H4-COLOR, PREVIA-SESION-5,
  PLATAFORMA-ADELANTADA, ACTIVAR-SESION-04, HOJA-DE-RUTA; y los `simular_cierre.py` de sus anexos),
  encargos (copia literal) y HISTORIA: registro, no se tocan.
- `PROJECT_STATE.md:144` (Technical Debt, «Copia de seguridad ...: hecha hasta v10») ya es verdad y
  no pone A.4 como pendiente.

### 0.e Una afirmación del encargo que la medida contradice

El encargo dice que «La guardia lee como código sin revisar el fichero de test que se le pasa a
pytest (CLAUDE.md, guiones nuevos o cambiados; test_guardia_ffmpeg.py, cabecera)». **No es así
para un fichero bajo `tests/`**: `_analizar_pytest` (`guardia.py:1950-1998`) se lo salta
(`:1989-1990`, «La suite de `tests/` es codigo revisado y corre con la guarda del holdout»). Medido
con `pytest_lee.py` sobre un repo temporal, con el MISMO fichero (un literal de la carpeta de marzo)
dentro y fuera de `tests/`:

```
uv run pytest -q tests/unit/test_t.py	pasa
uv run python -m pytest -q tests/unit/test_t.py	pasa
uv run pytest -q otra/test_t.py	NIEGA: el codigo nombra corpus/.../Backtest marzo 2026/v.mp4.
uv run python tests/unit/test_t.py	NIEGA: el codigo nombra corpus/.../Backtest marzo 2026/v.mp4.
```

Así que la cabecera de `tests/unit/test_guardia_ffmpeg.py:6-7` («este fichero lo lee la guardia
como codigo cuando se le pasa a pytest») tampoco es exacta: solo lo lee si se ejecuta con
`python` directamente. Montar los literales a trozos en `test_guardia_ci.py` no hace daño y cubre
ese caso, así que lo mantengo; lo que cambia es el motivo que se escribe en su cabecera (decisión 6).

### 0.f La condición que propongo

**Regla** (`R_ESPERA_CI`): «docs/runbooks/DECISIONES-DE-PROCESO.md, entrada del 2026-10-21, punto
(2): «Ninguna consulta de la CI con un guion ni con un bucle» (origen: el guion de espera de
EA-CONEXION.md §13; encargo de trabajo/guardia-ci)». **Mensaje** (`COMO_ESPERAR_CI`), el del
encargo: «Como reescribirlo: una consulta suelta con `gh run view <run>`; si hay que esperar, una
espera sin consulta (`sleep` solo, o en segundo plano) y despues otra consulta suelta.»

Se niega un texto (Bash, código o PowerShell) que tenga a la vez **una consulta de CI** y **una
espera**, mirando el texto ENTERO: el nivel, sus `$(...)` y el contenido de cada argumento que
lleve espacios (que se tokeniza como Bash: `watch 'gh run view X'`, `alias c='gh run view X'`,
`xargs sh -c '...'`). Y `gh run watch` y `gh pr checks --watch`, siempre.

- **Consulta de CI, en Bash:** un comando (sin envoltorios: `timeout`, `nohup`, `env`, `command`...)
  cuyo programa, por su nombre (`gh`, `/usr/bin/gh`, `gh.exe`), sea `gh` con `run view|list|watch`,
  `pr checks` o `api` con una ruta de CI; o CUALQUIER programa (`curl`, `wget`...) con un argumento
  que contenga una ruta de CI: `actions/runs`, `check-runs`, `check-suites` (lista de la fase 0,
  ampliable: ¿`actions/jobs` y `commits/<sha>/status`? decisión 1). Y, solo si hay una espera, lo que no se
  puede decidir cuenta como consulta: un programa que se construye al ejecutarse (`$C`, `$(...)`)
  y un `gh` o un `curl` con un argumento que se construye al ejecutarse.
- **Espera, en Bash:** las palabras `while`, `until`, `for` o `select` en posición de comando; un
  comando `sleep` o `watch`; o una función de shell (`f() {...}`, `function f`), que puede
  llamarse a sí misma.
- **En código** (Python y otros): un literal que sea el programa `gh` (o termine en `/gh`,
  `gh.exe`), un literal con una ruta de CI, o `gh run|pr|api` en el texto; y un bucle o una espera
  en el texto (`while`, `for`, `until`, `sleep`, `setInterval`, `setTimeout`). Por el texto y no
  por el árbol: un `for` en un comentario niega, y lo que no se puede decidir se niega.
- **En PowerShell:** `gh` o una ruta de CI en el texto, y `while`, `for`, `foreach`, `do`, `until`,
  `Start-Sleep` o `sleep`.
- **Lo que NO es espera:** `timeout N` (pone un límite a una consulta, no la repite: `timeout 60 gh
  run view X` pasaría; con `gh run watch` dentro se niega por el `watch`), `| tail`, `| grep`, `&&`
  entre consultas sin `sleep` (dos consultas seguidas no esperan; decisión 2).


### 0.h El encargo frente al repo (auditor-encargo, 2026-10-23)

El subagente `auditor-encargo` contrastó 36 afirmaciones del encargo: 23 correctas, 5 incorrectas,
8 con matiz, y 12 requisitos del repo que el encargo no recoge. Aquí va lo que cambia el trabajo,
con su evidencia; el resto de su informe no cambia nada de lo de arriba.

**Incorrectas**

| # | afirmación del encargo | lo medido |
|---|---|---|
| 18 | «el esperar_run.py de EA-CONEXION.md §13 rehecho desde su descripción, no desde un fichero que no existe» | **existe**, con su versión `.sh`, en el scratchpad de la sesión de `trabajo/ea-conexion` (los cita el revisor en EA-CONEXION.md:1219 y :1257). Copiados al anexo y medidos: N8c pasa, N8d se niega por la asignación `run=`. El rehecho (N8) se queda: es la descripción del informe |
| 22 | «no hay un tercero vivo» | `docs/sesion-5/PREGUNTAS.md:8-9` (0.d; decisión 4) |
| 26 | «La guardia lee como código sin revisar el fichero de test que se le pasa a pytest» | no bajo `tests/`: `guardia.py:1989-1990`, así desde 2026-10-01 (GUION-MISMO-COMANDO.md:25); medido en 0.e. Lo mismo dicen, en falso, `test_guardia_ffmpeg.py:6-7` y GUARDIA-FFMPEG.md:150-153 (decisión 6) |
| 27 | «Hoy el for con gh run view y sleep ya se niega, pero por otra regla» | depende de la variable: con `n` o `d` (`guardia.py:2346-2347`) pasa (N3b) |
| 28 | «las dos ramas de guardia anteriores encontraron sus agujeros justo ahí (ERRORES-RECURRENTES.md, filas de trabajo/guardia-ffmpeg)» | hay UNA fila (ERRORES-RECURRENTES.md:94) y sus agujeros son otros: comillas `$'…'` y `$"…"`, el prefijo `file:`, un espacio final, un HLS disfrazado, el alias de la raíz y lo de antes y a la vez (`find -exec`, `cd -`, `\| tee`, `&`, `1<>`). Los tests de la fase 1 llevan las cuatro familias del encargo **y** las de esa fila que aplican a una consulta de CI (`$'…'`, `$"…"`, `&` y `\| tee`) |

**Con matiz, lo que importa**

- (5) §13 de EA-CONEXION documenta solo el caso de `ea-conexion`; el de `barrido-sesion-5` consta
  por referencia (ERRORES-RECURRENTES.md:91; HISTORIA), y hubo un caso anterior en
  `corrida-construccion`: curl y un guion Python tras una negativa de `gh api`
  (SESGO-H4-COLOR.md:1301), que es la fila N19.
- (6) La regla (2) de DECISIONES-DE-PROCESO.md:28 es más amplia que lo pedido: «Ninguna consulta
  de la CI con un guion» prohíbe también un guion con UNA consulta, sin bucle (decisión 3).
- (9) En PowerShell hasta la consulta suelta se niega (toda ejecución): los buenos son de Bash.
- (15) `cerrar-rama/SKILL.md:94-95` dice «la CI del commit de estado (HEAD) hasta "conclusion":
  "success"» sin decir cómo se espera (decisión 5).
- (23) La limpieza de V toca la Next Action y la hoja de ruta, que según `RITUAL.md:137-151`
  (punto Y) y `entregar-rama/SKILL.md:55-59` se cambian en el commit del contrato con la orden de
  cierre, no en la rama (decisión 7).
- (25) Ningún informe cerrado está en `rutas_permitidas`: corregir uno amplía el contrato.
- (31) `gh run view` necesita ya el número del run: el número sale de `gh run list --branch
  fix/guardia-ci` (B4, B9), una consulta suelta.

**Lo que el repo pide y el encargo no recoge**, lo que cambia el trabajo:

- H1. El orden: F de la Next Action pone las ramas de R6a en los huecos de espera, y K es
  PRIORITARIA (`PROJECT_STATE.md:32` y `:48`). El encargo explica el hueco hasta el 24 y elige esta
  rama; no lo discuto, lo dejo dicho. Esta rama no tiene `###` en la hoja (va por Technical Debt).
- H3. `docs/HANDOFF.md:1051` trae otra forma suelta (B13): pasa y seguirá pasando.
- H4. Las formas del ritual ya las fija `test_guardia_claude.py:991-1033`; las de las skills van a
  `test_guardia_ci.py`, porque `test_guardia_claude.py` no está en el contrato.
- H5. La salida de la línea de Technical Debt va a HISTORIA como `# Technical Debt PAGADA · sale de
  PROJECT_STATE.md en trabajo/guardia-ci (<fecha>)`, con su texto literal, en el commit del
  contrato (`docs/state/README.md:61-75`): se prepara en el informe.
- H11. En `solo_lectura.py` el auditor midió además que `git tag -l stable/F38*` se niega (`tag` no
  está en `GIT_LEE`), como el `git worktree list` que ya está en G.1 (HOJA-DE-RUTA.md:436). No es
  de esta rama: lo dejo anotado para G.1, no lo toco.
- H12. R4.1 pone «R1.1» sin «(HECHA)», y R1.1 está HECHA (HOJA-DE-RUTA.md:59): va con la limpieza
  de V (decisión 7).

### 0.i Lo que no pude medir

- Que `--exit-status` exista en el `gh` instalado: no se ejecuta `gh` en esta fase (ni `--help`).
- Que el hook del proyecto corra para los subagentes, por un test: solo por la cabecera de
  `solo_lectura.py` y por lo que vio el auditor (0.b').
- Si Claude Code bloquea un `sleep` largo en primer plano: el mensaje propone «sleep solo, o en
  segundo plano»; no lo he ejecutado.
- La partición de la sesión 5 en dos días (23 y 24-oct): no consta en el repositorio.

### 0.j Exposiciones

Ninguna. La fase 0 no leyó material del punto 3 de CLAUDE.md, transcripciones ni fotogramas. El
literal de la carpeta de marzo de `pytest_lee.py` es una ruta montada a trozos en un repo temporal
con un fichero inventado; no se abrió nada de marzo.

## Lo que necesito que decidas

0. **La herramienta `Monitor` queda fuera de la guardia entera** (0.b''). Opciones: (a) en esta
   rama, `Monitor` al matcher de `.claude/settings.json` y, en `decidir`, su `command` tratado como
   el de Bash, con su test, ampliando el contrato a `.claude/settings.json`; (b) una línea de
   Technical Debt y su propia rama del carril. Recomiendo (a): sin ella la regla nueva se rodea
   cambiando de herramienta, y el cambio es de dos líneas. Coste de (b): el hueco sigue abierto
   para la CI y para el material protegido hasta otra rama.
1. **Las rutas de CI.** Opciones: (a) las tres del encargo (`actions/runs`, `check-runs`,
   `check-suites`); (b) además `actions/jobs` y `commits/<sha>/status` (y `statuses`). Recomiendo
   (b): son la misma pregunta («¿ha terminado?») por otra puerta. Coste de (a): un bucle sobre
   `/status` pasaría.
2. **Una espera y UNA consulta en el mismo comando** (N15 `sleep 300 && gh run view X`, N16), y
   `timeout N gh run view X`. Opciones: (a) negar N15 y N16 (la letra del encargo: «en la misma
   línea de comandos que sleep»; el mensaje ya dice cómo: el `sleep` en una llamada y la consulta
   en otra) y dejar pasar `timeout N` con una consulta suelta (no repite nada); (b) dejar pasar
   N15/N16, porque no repiten. Recomiendo (a): una sola regla sin excepciones («consulta y espera
   en el mismo texto»), más difícil de rodear. Coste de (b): la condición tiene que contar
   consultas, y `sleep 30 && gh … && sleep 30 && gh …` queda en la frontera.
3. **Un guion o código con UNA consulta de CI, sin bucle** (DECISIONES-DE-PROCESO.md:28, punto 2:
   «Ninguna consulta de la CI con un guion»). Opciones: (a) la guardia niega toda consulta de CI
   desde código (`python -c`, heredoc, guion), con bucle o sin él, y en Bash suelto la deja; (b)
   solo con bucle o espera, como pide el encargo. Recomiendo (a): es la regla escrita, y en código
   «hay un bucle» se decide peor que «hay una consulta» (una lista por comprensión, una recursión o
   un `iter` sin palabra clave). Coste de (b): un guion que consulta y se relanza a mano pasaría,
   contra la regla.
4. **`docs/sesion-5/PREGUNTAS.md:8-9`**, el tercer sitio vivo, dice que A.4 «hoy no está hecha».
   Opciones: (a) recuadro de corrección junto al pasaje, con fecha y rama, ampliando el contrato a
   ese fichero; (b) dejarlo, porque es la hoja de antes de grabar. Recomiendo (a): es un documento
   vivo hasta que termine la sesión 5 (el 24 se graba el resto). Coste de (b): una afirmación falsa
   viva.
5. **Una línea en las skills y el ritual con la forma de esperar.** Ninguno dice un bucle (0.c),
   pero `entregar-rama` paso 7 dice «esperar el run» y `cerrar-rama:94-95` «hasta "conclusion":
   "success"», sin decir cómo. Opciones: (a) una línea en `entregar-rama` (paso 7), `cerrar-rama`
   (paso 7) y `RITUAL.md:320` con la forma del mensaje de la guardia; (b) nada, porque no hay nada
   falso. Recomiendo (a): «esperar» sin forma es lo que acabó en el guion dos veces. Coste de (b):
   la guardia lo para, pero tarde.
6. **La afirmación falsa sobre pytest** en `tests/unit/test_guardia_ffmpeg.py:6-7` y
   `GUARDIA-FFMPEG.md:150-153`. Opciones: (a) corregir aquí la cabecera del test (un comentario, no
   la regla de ffmpeg) y poner un recuadro en GUARDIA-FFMPEG.md, ampliando el contrato a los dos;
   (b) una línea de Technical Debt. Recomiendo (a): es la rama que lo ha medido, y en
   `test_guardia_ci.py` escribo el motivo verdadero de montar a trozos (cubre `python <test>`
   directo, no pytest). Coste de (b): el error se copia a la próxima rama de guardia, como se copió
   a este encargo.
7. **En qué commit va la limpieza de V.** Opciones: (a) se prepara en el informe (las líneas de
   `PROJECT_STATE.md:54` y `HOJA-DE-RUTA.md:219-221`, con «R1.1 (HECHA)» de H12) y entra en el
   commit del contrato con la orden de cierre, como mandan `RITUAL.md:137-151` y
   `entregar-rama:55-59`; (b) se hace en la rama, como dice la fase 2 del encargo, declarada como
   desviación. Recomiendo (a): es el ritual y no cuesta nada; en la rama compruebo en un clon
   desechable cuál de las dos formas («(A.4, HECHA el 2026-10-22)» o quitarla) dejan pasar
   `test_hoja_de_ruta.py` y `test_project_state.py`. Coste de (b): una desviación más que declarar
   en el cierre.
8. **`solo_lectura.py`.** Opciones: (a) la regla solo en `guardia.py`, que corre también para los
   agentes (0.b'); (b) además una copia en `solo_lectura.py`. Recomiendo (a): una sola regla que
   mantener. Coste de (b): dos condiciones que pueden divergir.

## Respuesta del consultor a la PARADA de la fase 0 (2026-10-23)

Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 (2026-10-23). Cópiala al informe, en su sección.
>
> 0. Monitor: SÍ, en esta rama. Amplía el contrato a .claude/settings.json en un commit propio que lo declare. Monitor entra en el matcher de PreToolUse de guardia.py y la guardia decide su comando con las mismas reglas que Bash; si el formato de su entrada no se reconoce, se niega. Tests en los dos sentidos: un Monitor que espera a la CI en bucle se niega, un Monitor que lee material protegido se niega (ruta montada a trozos) y un Monitor inocuo pasa (por ejemplo, esperar a que exista un fichero de la carpeta de trabajo sin leerlo). Además, en el informe: la lista de TODAS las herramientas de esta sesión que ejecutan comandos o leen ficheros, frente al matcher, con fichero:línea. Si aparece otra fuera del matcher que no sea Monitor, no la arregles: PARADA con la lista. Cuando cambie settings.json, di si la sesión tiene que reiniciarse para que el hook nuevo cargue y compruébalo con un caso negado de verdad, sin consultar la CI.
> 1. Rutas de CI: SÍ, añade actions/jobs y commits/<sha>/status y statuses.
> 2. SÍ, negar una espera y una consulta en el mismo comando (sleep 300 && gh run view). timeout N gh run view pasa. El mensaje de la negativa ya da la vía buena: la espera sola, o en segundo plano, y después la consulta suelta en otro comando.
> 3. SÍ, negar un guion con una sola consulta de CI aunque no tenga bucle: es la regla escrita de DECISIONES-DE-PROCESO.md («ninguna consulta de la CI con un guion»).
> 4. SÍ, un recuadro de corrección en docs/sesion-5/PREGUNTAS.md:8-9 (A.4 HECHA el 2026-10-22), ampliando el contrato. Que sea solo ese recuadro: el resto de PREGUNTAS.md lo toca la ingesta.
> 5. SÍ, una línea con la forma de esperar en entregar-rama, cerrar-rama y RITUAL.md:320, con el mismo texto que el mensaje de la negativa. Amplía el contrato a esas skills.
> 6. SÍ, corrige la cabecera de test_guardia_ffmpeg.py y pon un recuadro en GUARDIA-FFMPEG.md: la guardia no lee lo que está bajo tests/ (guardia.py:1989). Mi encargo repetía ese error; lo declaro como error del consultor para la orden de cierre. Como la guardia no lee tests/, los literales de test_guardia_ci.py no hace falta montarlos a trozos, salvo los que nombren material protegido, que siguen a trozos por costumbre.
> 7. SÍ: la limpieza de V se prepara en el informe y se aplica en el commit del contrato del cierre, como manda el punto Y de RITUAL. Lo mismo para la línea de Technical Debt que paga esta rama.
> 8. SÍ, la regla solo en guardia.py, siempre que se demuestre que corre para los subagentes: cita el fichero:línea de la configuración que lo hace y añade un test o una prueba en memoria que lo enseñe. Si no se puede demostrar, PARADA.
>
> También: el for con la variable n, que hoy pasa, entra en los tests junto a los que hoy se niegan por otra regla, comprobando el MOTIVO. Y la fila única de trabajo/guardia-ffmpeg en ERRORES-RECURRENTES: los tests de disfraz cubren los agujeros que dice esa fila, no los cuatro que nombraba mi encargo.
>
> Sigue con las fases 1 y 2 y la entrega tal como dice el encargo, con el revisor al final. Si tocar settings.json te deja sin poder ejecutar algo que antes hacías, PARADA.

## PARADA 2 · Las herramientas de esta sesión frente al matcher (2026-10-23)

Punto 0 de la respuesta: «la lista de TODAS las herramientas de esta sesión que ejecutan comandos o
leen ficheros, frente al matcher, con fichero:línea. Si aparece otra fuera del matcher que no sea
Monitor, no la arregles: PARADA con la lista». Aparecen varias. No he arreglado ninguna, no he
tocado `settings.json` ni la guardia, y no he usado ninguna de ellas.

**El matcher.** `.claude/settings.json:69`: `"matcher": "Read|Grep|Glob|Bash|PowerShell"`, con el
comando de `guardia.py` en `:73`. No hay otro hook de `PreToolUse` en la configuración de usuario
(`~/.claude/settings.json` no tiene `hooks`). Los dos agentes de solo lectura añaden
`solo_lectura.py` con `matcher: "Bash"` (`.claude/agents/revisor.md:8` y
`.claude/agents/auditor-encargo.md:8`), y su `tools:` es `Read, Grep, Glob, Bash` (`:4`).

**De dónde sale la lista.** Las herramientas son las que esta sesión tiene cargadas o diferidas, y
lo que hacen sale de la definición de cada una (sus parámetros), no de un fichero del repositorio:
eso no tiene `fichero:línea`, y lo digo. Cargué el esquema de las diferidas con `ToolSearch`, que
solo trae la definición: no llamé a ninguna.

| herramienta | qué hace con ficheros o comandos (el parámetro) | en el matcher |
|---|---|---|
| Read, Grep, Glob | leen ficheros o listan nombres | sí |
| Bash | ejecuta un comando (`command`, también con `run_in_background`) | sí |
| PowerShell | ejecuta un comando (no está cargada en esta sesión; el matcher la cubre) | sí |
| **Monitor** | ejecuta un comando de shell (`command`) cuya salida es el flujo de eventos | **no**: el punto 0 la arregla |
| **Artifact** | `publish` lee un fichero local (`file_path`, `files`, `file_paths` con `asset: true`) y lo publica en claude.ai; `read` con `path`/`out_dir` escribe | **no** |
| **ArtifactData** | `set`/`update` con `file_path`: «a local JSON file ... sent as the document», y `out_dir` escribe | **no** |
| **DesignSync** | `write_files` con `localPath`: «the tool reads from disk, encodes, and uploads ... contents never enter the model context» | **no** |
| **mcp__claude-in-chrome__file_upload** | sube a una página ficheros locales por su ruta (`paths`); la definición dice que solo los «shared with this session» | **no** |
| **mcp__claude-in-chrome__navigate** (con `get_page_text`, `read_page`, `javascript_tool`) | abre una URL; con `file:///...` un navegador abre un fichero local, y las otras tres leen la página. Que la extensión tenga permiso de `file://` no lo he medido | **no** |
| **EnterWorktree** | ejecuta `git worktree add` y cambia el directorio de la sesión; no lee contenido | **no** |
| Edit, Write, NotebookEdit | escriben; Edit y NotebookEdit exigen un Read previo del fichero en la conversación (lo dice su definición), y Write para sobrescribir uno existente. Un Read negado por la guardia los deja sin poder tocarlo. Write crea un fichero nuevo sin leer nada | no, cubiertas por el Read previo |
| Agent, Workflow | lanzan subagentes, cuyas herramientas pasan por el mismo hook (punto 8, por demostrar en la fase 1) | no, cubiertas a través del subagente |
| Skill | carga un `SKILL.md` de `.claude/skills/` | no; no lee nada fuera de las skills |
| CronCreate, ScheduleWakeup, RemoteTrigger | programan un prompt (o un disparador remoto); no ejecutan un comando ni leen un fichero por sí mismas | no; lo que ejecute el prompt pasa por el hook |
| Google Drive `create_file`, Gmail `create_draft`, Canva y Claude Docs | suben CONTENIDO que se les pasa (`textContent`, `base64Content`, `attachments.content`), no una ruta: para subir un fichero la sesión tendría que leerlo antes con Read o Bash | no, cubiertas por la lectura previa |
| ReadMcpResourceTool | lee un recurso de un servidor MCP por su URI; ninguno de los servidores configurados es de ficheros locales | no |

**Fuera del matcher, que no son Monitor:** Artifact, ArtifactData, DesignSync, `file_upload` y
`navigate` de claude-in-chrome (con sus lectores de página), y EnterWorktree. Las cinco primeras
pueden leer un fichero local y mandarlo fuera sin que la guardia lo vea (Artifact y DesignSync lo
publican o lo suben; Chrome lo abre o lo sube). EnterWorktree solo ejecuta git.

## Lo que necesito que decidas (PARADA 2)

0. **Las herramientas que leen un fichero local fuera del matcher** (Artifact, ArtifactData,
   DesignSync y `file_upload` de claude-in-chrome). Opciones: (a) en esta rama, añadirlas al
   matcher y que `decidir` mire sus rutas (`file_path`, `files`, `file_paths`, `localPath`,
   `paths`) con `motivo_fichero`, como un Read, y niegue lo que no reconoce; (b) una línea de
   Technical Debt y su propia rama del carril. Recomiendo (b): son cuatro formatos de entrada
   distintos, con sus tests, y esta rama es la de la CI; el riesgo hasta entonces es bajo, porque
   ninguna se usa en el trabajo del repositorio y todas piden aprobación o un plan antes de subir.
   Coste de (b): el hueco sigue abierto hasta esa rama.
1. **`navigate` de claude-in-chrome con `file://`.** Opciones: (a) lo mismo que el punto 0, mirando
   la ruta de una URL `file://`; (b) Technical Debt, con una medida primero de si la extensión
   abre `file://` en esta máquina. Recomiendo (b): sin esa medida no se sabe si el hueco existe.
2. **EnterWorktree.** Opciones: (a) dejarla fuera: solo ejecuta `git worktree add`, que la guardia
   deja pasar en Bash, y no lee contenido; (b) añadirla al matcher y negarla, porque cambia el
   directorio de la sesión. Recomiendo (a). Coste de (b): ninguno práctico, la skill
   `comparar-con-main` usa `git worktree add` por Bash.
3. **Sigo con el resto mientras tanto.** Opciones: (a) aplicar ya los puntos 0 a 8 de tu
   respuesta (Monitor incluido), que no dependen de esta PARADA; (b) esperar. Recomiendo (a): esta
   PARADA solo decide qué más entra en el matcher.

## Respuesta del consultor a la PARADA 2 (2026-10-23)

Copiada tal cual:

> Respuesta del consultor a la PARADA 2 (2026-10-23). Cópiala al informe, en su sección.
>
> 0. Artifact, ArtifactData, DesignSync y file_upload de claude-in-chrome: en esta rama NO se meten en el matcher ni en la guardia. Este repo no las necesita para nada, así que se cierran ya por permisos: añádelas a permissions.deny de .claude/settings.json (ya está en el contrato por el punto 0 de la respuesta 1), con su nombre EXACTO tal como aparece en tu lista de herramientas (las de MCP, con su prefijo mcp__…). La regla fina (mirar sus rutas como un Read, por si algún día hacen falta) va a una línea de Technical Debt para su propia rama del carril de guardias, junto a la línea PRIORITARIA del alias de la raíz (K).
> 1. navigate de claude-in-chrome: también a permissions.deny, y con él get_page_text y read_page (las que leerían una página file://). No hace falta medir si la extensión abre file://: el repo no usa el navegador. Va a la misma línea de Technical Debt.
> 2. EnterWorktree: fuera, de acuerdo; solo hace lo mismo que git worktree add por Bash, y eso la guardia ya lo deja pasar.
> 3. SÍ, aplica ya los puntos 0 a 8 de la respuesta 1, Monitor incluido.
>
> Para lo nuevo de los puntos 0 y 1:
> - Un test en test_guardia_ci.py (o donde estén hoy los de settings.json, test_guardia_claude.py:1131) que falle si alguno de esos nombres sale de permissions.deny, roto a propósito en los dos sentidos.
> - En cuanto settings.json cambie, prueba la negativa de verdad con una llamada inofensiva: Artifact con action list, y navigate a about:blank. Las dos tienen que salir negadas, y la salida va en el informe. No hagas ninguna llamada que lea o suba un fichero. Si alguna no sale negada (nombre mal escrito, o hace falta reiniciar la sesión), dilo y PARADA.
> - Si la sesión tiene que reiniciarse para cargar settings.json, dímelo antes de hacerlo y retoma con retomar-rama.
>
> Lo demás, como dicen el encargo y la respuesta 1.

## Ampliación del contrato (2026-10-23, commit propio)

Por las dos respuestas, `contrato.yaml` amplía `rutas_permitidas` en un commit que solo hace eso
(y copia esta respuesta):

| ruta | por qué |
|---|---|
| `.claude/settings.json` | respuesta 1, punto 0 (Monitor en el matcher); respuesta 2, puntos 0 y 1 (`permissions.deny`) |
| `tests/unit/test_guardia_claude.py` | no lo pidió el consultor, lo pide el repo: su `test_los_ajustes_registran_la_guardia_y_las_denegaciones` (`:1149-1153`) exige que el matcher sea EXACTAMENTE `{Read, Grep, Glob, Bash, PowerShell}`, y su `_casa_regla` (`:1132-1137`) hace `assert` de que toda regla de `deny` sea `Bash(...)`: con Monitor en el matcher y las herramientas en `deny`, los dos fallarían. Solo se tocan esas dos piezas |
| `tests/unit/test_guardia_ffmpeg.py` | respuesta 1, punto 6 (su cabecera, `:6-7`) |
| `docs/validation/GUARDIA-FFMPEG.md` | respuesta 1, punto 6 (un recuadro en `:150-153`) |
| `docs/sesion-5/PREGUNTAS.md` | respuesta 1, punto 4 (solo el recuadro de `:8-9`) |

## 1. Fase 1 · La condición (2026-10-23)

Aplicada la respuesta a la fase 0 (puntos 0-3 y 8) y la respuesta a la PARADA 2 (puntos 0, 1 y 3).

### 1.1 El código (`.claude/hooks/guardia.py`)

- **Una sección nueva, «esperar a la CI»**, con su comentario del porqué y el origen
  (EA-CONEXION.md §13 y DECISIONES-DE-PROCESO.md, 2026-10-21, punto 2): `R_ESPERA_CI`,
  `COMO_ESPERAR_CI` (el texto del encargo), `RUTA_DE_CI` (las tres del encargo más `actions/jobs`
  y `commits/<sha>/status(es)`, punto 1; tras deshacer `%XX` y sin mayúsculas), `huella_ci` (lo que
  un texto de Bash tiene de consulta y de espera, mirado entero: el nivel, sus `$(...)` y cada
  palabra con espacios leída como Bash), `exigir_sin_espera_a_la_ci` (la condición en Bash) y
  `_exigir_codigo_sin_ci` (en código).
- **Se llama en tres sitios, al principio de cada uno**, para que su motivo gane al de otras reglas:
  `analizar_bash` (justo tras `tokenizar`; vale en todos los niveles: `bash -c`, un `.sh`, cada
  `$(...)`), `analizar_codigo` (`python -c`, heredocs, guiones que no son los de `main`) y
  `analizar_powershell`.
- **`Contexto.en_codigo`**: lo pone `_analizar_codigo_de` al analizar un guion de shell o un
  `bash -c`; ahí toda consulta se niega, con espera o sin ella (punto 3).
- **`decidir`**: `HERRAMIENTAS_DE_COMANDO = {Bash, PowerShell, Monitor}`; Monitor se decide como
  Bash, y una entrada que no sea un `command` de texto con solo `command`, `description` y
  `timeout_ms` se niega con `R_MONITOR` (punto 0).
- La cabecera del módulo nombra la familia 4.
- **Una corrección en el camino, medida:** la primera versión negaba B7, la forma de RITUAL.md:317,
  porque leía como Bash el patrón de su `grep` (`"status": *"[^"]*"...`) y lo veía como un programa
  con comodín. Una palabra es un dato hasta que algo la ejecuta: de las palabras anidadas solo
  cuenta la consulta o la espera que se VE, no lo que no se puede decidir.

Lo que se niega (y lo que no), en una línea: en Bash, una consulta de CI y una espera (`while`,
`until`, `for`, `select`, `function`, `f()`, `sleep`, `watch`) en el mismo comando; `gh run
watch` y `gh pr checks --watch` siempre; lo que no se puede decidir (un programa, o un argumento de
`gh`/`curl`, que se construye al ejecutarse) junto a una espera, o un programa que se construye
junto a una consulta; en código, toda consulta; en PowerShell, consulta y espera. Pasa la consulta
suelta, y `timeout N` delante de una consulta (punto 2).

**Límite declarado:** en código la consulta se reconoce por el texto (un literal que sea el programa
`gh`, `gh run|pr|api|workflow`, o una ruta de la CI). Una cadena montada a trozos (`"g" + "h"`) o
un import dinámico la esquivan; en Bash, `eval` ya lo niega otra regla. Y en código lo que se niega
es la MENCIÓN: un guion que solo lleva `gh run view` como dato también se niega (PARADA 3).
**Cambiado tras la PARADA 3 (§5):** en código cuenta la mención con una vía de salida o con algo no
decidible; el `__import__` dinámico ya se niega; `"g" + "h"` queda como riesgo residual declarado.

### 1.2 Los tests (`tests/unit/test_guardia_ci.py`)

Fichero nuevo, 10 funciones y 84 casos, todo en memoria con `decidir` sobre un repo de `tmp_path`
(ningún comando se ejecuta, ninguno consulta la CI). Sus literales van enteros, salvo la ruta de
marzo (punto 6 de la respuesta: la guardia no lee `tests/`).

- `test_la_tabla`: 72 formas con su decisión ANTES (la de `main`) y DESPUÉS, comprobando el MOTIVO
  (la constante `R_*` que cita): N1-N19 de la fase 0, el `for n` (N3b) y las que hoy niega otra
  regla (N3, N8d, N9-N9c, D2, D4, D9, D13-D18), las rutas nuevas (R1-R4), un guion o código con UNA
  consulta (C1-C5, punto 3), los disfraces de la fila de `trabajo/guardia-ffmpeg` en
  ERRORES-RECURRENTES.md (D1-D12: `$'gh'`, `$'\x67h'`, `$"gh"`, `"gh "` con espacio final, la ruta
  del programa con `\` o `/` y en mayúsculas, `check%2Druns`, `find -exec`, `cd -`, `| tee`, `&`,
  `1<>`) y los del encargo (D13-D18: una variable, un alias, dos funciones, `xargs sh -c`,
  `$(echo gh)`); y 19 que pasan (B1-B19).
- `test_el_mensaje_dice_que_hacer`: el texto del encargo, literal.
- **Roto a propósito, en los dos sentidos:** `test_sin_la_regla_vuelve_lo_de_antes` (con la
  condición apagada, las 72 vuelven a su decisión de `main`: salida en
  `anexos/GUARDIA-CI/tabla-SIN-LA-REGLA.txt`) y
  `test_con_la_consulta_suelta_como_espera_las_buenas_se_niegan` (si `gh` contara como espera, las
  ocho buenas que consultan se negarían).
- Monitor: `test_monitor_se_decide_como_bash` (espera a la CI → `R_ESPERA_CI`; `cat` de la carpeta
  de marzo → `R_SIN_ABRIR`; `until test -f listo; do sleep 1; done` pasa),
  `test_monitor_con_una_entrada_que_no_se_reconoce_se_niega` (`ws`, sin `command`, `command` que no
  es texto, una clave de más → `R_MONITOR`) y, roto a propósito,
  `test_sin_monitor_en_decidir_el_que_lee_pasaria`.
- `test_un_subagente_se_decide_igual` (punto 8, en memoria).
- `settings.json`: `test_las_herramientas_que_el_repo_no_usa_estan_denegadas` y, roto a propósito
  en los dos sentidos, `test_si_falta_un_nombre_o_esta_mal_escrito_se_ve` (quitar cada nombre lo
  caza; escribirlo con `_` en vez de `-` también; con todos, nada).

**Las dos salidas** (tests primero): `anexos/GUARDIA-CI/pytest-1-antes-del-codigo.txt`, el fichero
contra la guardia SIN el código: 66 fallos (todos los que piden la regla nueva, Monitor y
`settings.json`; en esa versión B19 era `git log` y fallaba por el repo de prueba, y se cambió por
`wc -l`). `anexos/GUARDIA-CI/pytest-2-con-el-codigo.txt`: **84 passed in 16.99s**.

### 1.3 La tabla, antes y después

Medida por los tests (la columna «antes» es la decisión con la regla apagada, que reproduce la de
`main`: la de la fase 0 coincide en todas las filas que ya tenía). 53 negadas con `R_ESPERA_CI`
(39 que en `main` pasaban y 14 que `main` negaba por otra regla) y 19 que pasan antes y después.

| id | herramienta | antes (sin la regla = `main`) | después |
|---|---|---|---|
| N1 | Bash | pasa | R_ESPERA_CI |
| N2 | Bash | pasa | R_ESPERA_CI |
| N3 | Bash | R_EJECUCION | R_ESPERA_CI |
| N3b | Bash | pasa | R_ESPERA_CI |
| N4 | Bash | pasa | R_ESPERA_CI |
| N5 | Bash | pasa | R_ESPERA_CI |
| N5b | Bash | pasa | R_ESPERA_CI |
| N6 | Bash | pasa | R_ESPERA_CI |
| N7 | Bash | pasa | R_ESPERA_CI |
| N7b | Bash | pasa | R_ESPERA_CI |
| N8c | Bash | pasa | R_ESPERA_CI |
| N8b | Bash | pasa | R_ESPERA_CI |
| N8d | Bash | R_EJECUCION | R_ESPERA_CI |
| N9 | PowerShell | R_EJECUCION | R_ESPERA_CI |
| N9b | PowerShell | R_EJECUCION | R_ESPERA_CI |
| N9c | PowerShell | R_EJECUCION | R_ESPERA_CI |
| N10 | Bash | pasa | R_ESPERA_CI |
| N11 | Bash | pasa | R_ESPERA_CI |
| N12 | Bash | pasa | R_ESPERA_CI |
| N13 | Bash | pasa | R_ESPERA_CI |
| N14 | Bash | pasa | R_ESPERA_CI |
| N15 | Bash | pasa | R_ESPERA_CI |
| N16 | Bash | pasa | R_ESPERA_CI |
| N17 | Bash | pasa | R_ESPERA_CI |
| N18 | Bash | pasa | R_ESPERA_CI |
| N19 | Bash | pasa | R_ESPERA_CI |
| R1 | Bash | pasa | R_ESPERA_CI |
| R2 | Bash | pasa | R_ESPERA_CI |
| R3 | Bash | pasa | R_ESPERA_CI |
| R4 | Bash | pasa | R_ESPERA_CI |
| C1 | Bash | pasa | R_ESPERA_CI |
| C2 | Bash | pasa | R_ESPERA_CI |
| C3 | Bash | pasa | R_ESPERA_CI |
| C4 | Bash | pasa | R_ESPERA_CI |
| C5 | Bash | pasa | R_ESPERA_CI |
| D1 | Bash | pasa | R_ESPERA_CI |
| D2 | Bash | R_EJECUCION | R_ESPERA_CI |
| D3 | Bash | pasa | R_ESPERA_CI |
| D4 | Bash | R_EJECUCION | R_ESPERA_CI |
| D5 | Bash | pasa en Windows; `R_EJECUCION` en Linux (§6) | R_ESPERA_CI |
| D6 | Bash | pasa | R_ESPERA_CI |
| D7 | Bash | pasa | R_ESPERA_CI |
| D8 | Bash | pasa | R_ESPERA_CI |
| D9 | Bash | R_EJECUCION | R_ESPERA_CI |
| D10 | Bash | pasa | R_ESPERA_CI |
| D11 | Bash | pasa | R_ESPERA_CI |
| D12 | Bash | pasa | R_ESPERA_CI |
| D13 | Bash | R_EJECUCION | R_ESPERA_CI |
| D14 | Bash | R_EJECUCION | R_ESPERA_CI |
| D15 | Bash | R_EJECUCION | R_ESPERA_CI |
| D16 | Bash | R_EJECUCION | R_ESPERA_CI |
| D17 | Bash | R_EJECUCION | R_ESPERA_CI |
| D18 | Bash | R_EJECUCION | R_ESPERA_CI |
| B1 | Bash | pasa | pasa |
| B2 | Bash | pasa | pasa |
| B3 | Bash | pasa | pasa |
| B4 | Bash | pasa | pasa |
| B5 | Bash | pasa | pasa |
| B6 | Bash | pasa | pasa |
| B7 | Bash | pasa | pasa |
| B8 | Bash | pasa | pasa |
| B9 | Bash | pasa | pasa |
| B10 | Bash | pasa | pasa |
| B11 | Bash | pasa | pasa |
| B12 | Bash | pasa | pasa |
| B13 | Bash | pasa | pasa |
| B14 | Bash | pasa | pasa |
| B15 | Bash | pasa | pasa |
| B16 | Bash | pasa | pasa |
| B17 | Bash | pasa | pasa |
| B18 | Bash | pasa | pasa |
| B19 | Bash | pasa | pasa |


El guion de la fase 0 (`anexos/GUARDIA-CI/tabla_fase0.py`) ya no se podía ejecutar: lleva `gh run
view` como cadenas y la regla de código lo negaba (PARADA 3). Por eso la tabla de después salió de
los tests. Tras la respuesta a la PARADA 3 vuelve a pasar, y su salida de después está en §5.

### 1.4 `settings.json`, `Monitor` y las pruebas en vivo

- `.claude/settings.json`: `Monitor` en el matcher (`"Read|Grep|Glob|Bash|PowerShell|Monitor"`) y
  en `permissions.deny`, con su nombre exacto: `Artifact`, `ArtifactData`, `DesignSync`,
  `mcp__claude-in-chrome__file_upload`, `mcp__claude-in-chrome__navigate`,
  `mcp__claude-in-chrome__get_page_text` y `mcp__claude-in-chrome__read_page`.
- `tests/unit/test_guardia_claude.py` (ampliación declarada): el matcher esperado lleva `Monitor`, y
  `_casa_regla` devuelve `False` para una regla que no es `Bash(...)` en vez de fallar.
- **Pruebas en vivo, sin reiniciar la sesión** (`anexos/GUARDIA-CI/pruebas-en-vivo.txt`):
  `Artifact` con `action: list` → «Permission to use Artifact has been denied.»;
  `navigate` a `about:blank` → «Permission to use mcp__claude-in-chrome__navigate has been
  denied.»; `Monitor` con `for i in 1; do echo x; done` (inocuo) → «PreToolUse:Monitor hook error:
  ... GUARDIA (.claude/hooks/guardia.py) bloquea: ejecutar `for i` ...». **La sesión NO tiene que
  reiniciarse:** Claude Code cargó el matcher y los permisos en caliente, y desde ese momento dejó
  de ofrecer las siete herramientas («Denied by a permission rule»). Ninguna llamada leyó ni subió
  un fichero, y ninguna consultó la CI.
- **Lo que hacía antes y sigue pudiendo hacer**, medido después del cambio: Bash, `git`, `uv run
  pytest` sobre `tests/`, `make check` (en memoria con la ruta absoluta del repo: pasan) y los
  `python` de la carpeta de trabajo que no mencionan la CI. La excepción, `tabla_fase0.py`, fue la
  PARADA 3 (§5: resuelta, vuelve a pasar).

### 1.5 Los subagentes (punto 8)

- **La configuración que lo hace:** `.claude/settings.json:74-76` en la rama (`:69` en `main`,
  antes de que la rama añadiera siete líneas a `deny`; revisor, a1), el único `PreToolUse` del proyecto,
  con su `matcher` y sin filtro por agente; los dos agentes de solo lectura añaden a él
  `solo_lectura.py` con `matcher: "Bash"` (`.claude/agents/revisor.md:8`,
  `.claude/agents/auditor-encargo.md:8`), no lo sustituyen.
- **Prueba de verdad:** un subagente lanzado desde esta sesión ejecutó una vez `for i in 1; do echo
  x; done` y Claude Code le devolvió el bloqueo de `guardia.py`, entero, en
  `anexos/GUARDIA-CI/pruebas-en-vivo.txt` (y el auditor de la fase 0 ya lo había visto). **Prueba en
  memoria:** `test_un_subagente_se_decide_igual`, la misma decisión con los campos `agent_id` y
  `agent_type` en el evento. La regla va solo en `guardia.py`; `solo_lectura.py` no se toca.

### 1.6 Tiempos y `make check`

| suite | antes del cambio | después |
|---|---|---|
| `test_guardia_claude.py` + `test_guardia_ffmpeg.py` | 572 passed in 181.20s | 572 passed in 159.46s |
| las tres, con `test_guardia_ci.py` | — | 656 passed in 180.44s |
| `test_guardia_ci.py` sola | — | 84 passed in 16.99s |

La regla nueva no hace más lenta la suite (la diferencia de 181 a 159 s es ruido de la máquina).
El `make check` de este commit, con su `PICO DE MEMORIA`, va en el mensaje de la PARADA 3 y en el
informe del commit siguiente (un commit no puede llevar el resultado de su propio sello).

## 2. Fase 2 · Documentos

- **`docs/sesion-5/PREGUNTAS.md`**: un recuadro de corrección junto a `:8-9` (A.4 HECHA el
  2026-10-22), y nada más del fichero (punto 4).
- **`docs/validation/GUARDIA-FFMPEG.md`**: recuadro junto a `:150-153` (la guardia no lee `tests/`),
  con el cuerpo intacto; y la cabecera de `tests/unit/test_guardia_ffmpeg.py` corregida (punto 6).
  **Error del consultor, declarado para la orden de cierre** (punto 6, sus palabras): «Mi encargo
  repetía ese error».
- **La forma de esperar**, con el mismo texto que el mensaje de la negativa, en
  `entregar-rama/SKILL.md` (paso 7), `cerrar-rama/SKILL.md` (paso 7) y `RITUAL.md:320` (punto 5).
- **`PROJECT_STATE.md`**: la línea nueva de Technical Debt de las siete herramientas (respuesta a la
  PARADA 2, puntos 0 y 1), junto a la del guion de CI, y el recuento de tests (1655 → 1665).
- **La limpieza de V, medida en un clon desechable** (`git worktree add --detach`, quitado
  después): con la forma A («(A.4, HECHA el 2026-10-22)», y «R1.1 (HECHA)» de H12) y con la B
  (quitarla), `test_hoja_de_ruta.py` y `test_project_state.py` dan **19 passed** las dos veces:
  ninguno mira el contenido de «Depende de». Preparo la A, que es la costumbre de R4.1 (cada
  dependencia con su «(HECHA)»). Se aplica en el commit del contrato del cierre (punto 7).

## 3. Preparado para el commit del contrato del cierre (punto Y de RITUAL)

- **Next Action, V** (`PROJECT_STATE.md:54`): «Depende de R1.1, de R3.1 y de la copia de seguridad
  (A.4).» pasa a «Depende de R1.1, de R3.1 y de la copia de seguridad (A.4, HECHA el
  2026-10-22).»
- **`docs/plan/HOJA-DE-RUTA.md:219-221`**, el «Depende de» de R4.1:

  ```
  - **Depende de:** R1.1 (HECHA), R3.1 (HECHA), R1.2 (HECHA), R3.2 (HECHA), R3.3 (HECHA),
    R3.4 (HECHA) y la copia de seguridad del carril de Aleks (A.4, HECHA el 2026-10-22).
  ```
- **Technical Debt que sale**, condición (a) PAGADA (`docs/state/README.md`): la línea
  `PROJECT_STATE.md:104` («La guardia no niega un guion que espera a la CI en bucle ...»), con su
  texto literal, al final de HISTORIA bajo `# Technical Debt PAGADA · sale de PROJECT_STATE.md en
  trabajo/guardia-ci (<fecha del cierre>)`; evidencia: `tests/unit/test_guardia_ci.py` y el commit
  de esta fase.
- Lo de siempre del cierre: el registro en HISTORIA y la fila de ERRORES-RECURRENTES (con el error
  del consultor del punto 6). G.1 no recibe nada.

## 4. Las negativas en esta rama

| cuándo | comando | lo que dijo | qué hice |
|---|---|---|---|
| abrir-rama | `git show $(git log ...):PROJECT_STATE.md` | `git show` con un argumento que se construye al ejecutarse | la forma que propone: dos llamadas con el sha literal |
| tres veces (abrir, ampliar el contrato, la tabla) | `git add ... && uv run python scripts/contrato_rama.py`; `sed -i ... && python tabla_md.py` | «antes, en el mismo comando, va `git add ...`» (`R_EJECUCION`) | la forma que propone: cada uno en su llamada |
| tras el cambio, en memoria | `python docs/validation/anexos/GUARDIA-CI/tabla_fase0.py .` | `R_ESPERA_CI`, «el codigo consulta la CI» | PARADA 3; no lo ejecuté |
| tras la PARADA 3, dos veces | `uv run ruff format ... && ... && uv run pytest ...`; `grep -c ...; uv run botsito state check` | «ejecutar `pytest`/`botsito state check`: antes, en el mismo comando, va ...» (`R_EJECUCION`) | la forma que propone: cada uno en su llamada |

Ninguna del clasificador. Todas menos la PARADA 3 son de reglas de `main`, no de la regla nueva.
Aparte: `git worktree list` enseña un worktree de OTRA sesión
(`…/2ea2c3d2-…/scratchpad/wt-ci`, en `e7df30b`); no es de esta rama y no lo he tocado.

## PARADA 3 · La regla de código niega un guion que solo MENCIONA la CI (2026-10-23)

Encargo, «REGLAS DE ESTA RAMA»: «Si cambias la guardia y a partir de ese commit te niega algo que
antes hacías, es un hallazgo de la rama: PARADA con el comando y el mensaje.»

- **Comando** (decidido en memoria con `decidir`, NO ejecutado): `python
  docs/validation/anexos/GUARDIA-CI/tabla_fase0.py .`, el guion de la fase 0 que pasa la tabla por
  `decidir`.
- **Mensaje:** «esperar a la CI: `gh', 'run`: el codigo consulta la CI (un guion o codigo en linea),
  con espera o sin ella. Regla: docs/runbooks/DECISIONES-DE-PROCESO.md, entrada del 2026-10-21,
  punto (2) ...»
- **Por qué:** la regla de código (punto 3 de tu respuesta) reconoce la consulta por el TEXTO, y ese
  guion lleva `gh run view` como cadenas que le pasa a `decidir`; no llama a `gh` ni a la red.
- **A quién más afecta:** al revisor del cierre. El encargo le pide pasar cinco formas «por decidir
  EN MEMORIA, como los tests»; el revisor no tiene Write, así que lo haría con `uv run python -c`, y
  un `python -c` que lleva `gh run view` como dato se niega igual. Solo pasaría montando las cadenas
  a trozos, que es justo la forma de esquivar la regla (§1.1, límite).

## Lo que necesito que decidas (PARADA 3)

0. **Qué cuenta como consulta en código.** Opciones: (a) dejarlo como está, por el texto: se niega
   la mención aunque sea un dato, y el revisor (y cualquier guion de medida) monta las cadenas a
   trozos, que es lo que preveía tu encargo; (b) exigir además, en Python, una llamada que salga del
   proceso: `subprocess`, `os.system`/`os.popen`, `urllib`, `requests`, `http.client` o `socket` en
   el código; sin ninguna de ellas, una mención de `gh` es un dato y pasa. En los demás lenguajes,
   por el texto, como hoy. Recomiendo (b): separa el guion que consulta de verdad (los dos del
   incidente, C1-C5 y N19 importan `subprocess` o `urllib`) del que solo pasa cadenas a `decidir`,
   y no obliga al revisor a enseñar la forma de esquivar la regla. Coste de (b): un `__import__`
   dinámico de `subprocess` la esquiva, como `"g" + "h"` esquiva la (a): ninguna de las dos cierra
   el código del todo. Coste de (a): el revisor tiene que montar a trozos.
1. **El revisor**, si eliges (a): ¿le digo en su encargo que monte las cadenas a trozos, declarado
   en su informe? Recomiendo sí con (a); con (b) no hace falta.

## Respuesta del consultor a la PARADA 3 (2026-10-23)

Copiada tal cual:

> Respuesta del consultor a la PARADA 3 (2026-10-23). Cópiala al informe, en su sección.
>
> 0. Opción (a): en un guion o código en línea, la consulta de CI cuenta solo si el código menciona gh o una ruta de CI Y además tiene una vía de salir del proceso: subprocess, os.system, os.popen, os.exec*, os.spawn*, pty, asyncio.create_subprocess_*, urllib, requests, httpx, http.client o socket. Y, para cerrar el hueco del __import__ dinámico: __import__, importlib, exec, eval, compile y runpy también cuentan como vía de salida, porque con ellas no se puede decidir qué se importa (se niega por no decidible, con su mensaje).
>    Excepción, una y cerrada: cargar la propia guardia desde su ruta literal (.claude/hooks/guardia.py con importlib.util.spec_from_file_location, o la forma exacta que usen hoy tests/unit/test_guardia_ci.py y tabla_fase0.py), siempre que no haya otra vía de salida en el código. Su test, en los dos sentidos: tabla_fase0.py pasa; el mismo guion con un import de subprocess añadido, se niega; con importlib sobre cualquier otra ruta, se niega; y con la ruta de la guardia montada a trozos, se niega.
>    El "g"+"h" a trozos con una vía de salida tiene que salir negado: si la mención no se ve pero hay vía de salida y el código construye cadenas, aplica lo que la guardia ya hace con las rutas compuestas (analizar_codigo, deuda C); si no lo cubre, es riesgo residual declarado en el informe y en la línea de Technical Debt, no un arreglo nuevo en esta rama.
> 1. El revisor: con la opción (a) no monta nada a trozos. Hace sus pruebas en memoria con tabla_fase0.py o con un python -c que cargue la guardia por la excepción de arriba, y declara en su informe la forma que usó.
>
> Declara además en el informe y en la línea de Technical Debt que preparas para el cierre: como la guardia no lee el código que está bajo tests/ (guardia.py:1989), un test que espere a la CI pasaría. Es un hueco que ya existía, no de esta rama: no se arregla aquí.
>
> Después, el push a fix/guardia-ci, su CI de Linux consultada con gh run view suelto, y el revisor, como dice el encargo.

## 5. La respuesta a la PARADA 3, aplicada (2026-10-23)

**Antes, el sello de §1-§4:** el `make check` de `e43d5b2` salió con exit 0, ningún `failed`,
`2826 passed in 1109.27s`, `SELLO: make check en verde sobre el arbol 0292e735…` y `PICO DE
MEMORIA de make check: 298 MiB en test`.

**La etiqueta de la respuesta:** dice «Opción (a)» y describe la (b) de la PARADA (la mención
junto a una vía de salida). Aplico lo que describe, que no deja dudas, y lo digo aquí.

### 5.1 Punto 0: en código, la mención con una vía de salida

- `_exigir_codigo_sin_ci` niega solo si el código MENCIONA la CI y además:
  - **puede salir del proceso** (`_SALIDA_DEL_PROCESO`): `subprocess`, `pty`, `urllib`,
    `requests`, `httpx`, `socket`, `http.client`, una llamada `.system(`, `.popen(`, `.exec[lv]…(`,
    `.spawn…(` o `.posix_spawn…(`, o su `from os import`, y `create_subprocess_*`;
  - **o hace algo no decidible** (`_NO_DECIDIBLE_EN_CODIGO`): `__import__(`, `exec(`, `eval(`,
    `compile(` (el de Python, no `re.compile`), `runpy`, o `importlib` fuera de la excepción. El
    mensaje lo dice: «usa algo con lo que no se puede decidir que importa o ejecuta».
- **La excepción, una y cerrada** (`_carga_solo_la_guardia`, por el árbol de Python): todo uso de
  `importlib` es `import importlib` o `import importlib.util` sin alias ni `from`, y cada aparición
  es la raíz de una LLAMADA a `importlib.util.module_from_spec` o a
  `importlib.util.spec_from_file_location(_, <ruta de la guardia>)`. La ruta vale si es el literal
  `.claude/hooks/guardia.py` (o una ruta absoluta acabada así), si es `NOMBRE / ".claude" / "hooks"
  / "guardia.py"` (la forma exacta de `tabla_fase0.py` y de `test_guardia_ci.py`), o si es una
  variable asignada una sola vez a una de las dos. Montada a trozos (`+`, f-cadena, `join`) no vale.
- **Dos ajustes que la medida pidió**, sin cambiar la regla:
  1. La vía de salida se busca en el código Python **sin sus cadenas ni comentarios**
     (`_sin_cadenas`, con `tokenize`): `tabla_fase0.py` lleva `import subprocess` DENTRO de los
     comandos de su tabla, y con el texto entero se negaba. En otro lenguaje, o si no se tokeniza,
     cuenta el texto entero.
  2. En Bash, los argumentos de un programa que no ejecuta nada (`NO_EJECUTAN`, salvo `xargs`,
     `find`, `gh` y `curl`: `PROGRAMAS_DE_DATOS`) y el código de un intérprete son DATOS para
     esta regla. La forma del revisor (`python -c` que carga la guardia y le pasa `gh run watch 1`)
     la negaba la regla de Bash, que leía el código como Bash, y por lo mismo se negaría `grep "gh
     run watch" fichero` o un `git commit -m` que lo nombre. El código de un `python -c` lo decide
     ya la regla de código.
- **Los tests** (`tests/unit/test_guardia_ci.py`, ahora 14 funciones y 101 casos; el recuento de
  `PROJECT_STATE.md` pasa a 1669; salida en
  `anexos/GUARDIA-CI/pytest-3-tras-la-parada-3.txt`, **101 passed**):
  - `test_el_guion_de_la_fase_0_pasa_y_sus_variantes_no`, la excepción en los dos sentidos:

    ```
    tabla_fase0 | tal cual | pasa
    tabla_fase0 | con subprocess | R_ESPERA_CI
    tabla_fase0 | otra ruta | R_ESPERA_CI
    tabla_fase0 | a trozos | R_ESPERA_CI
    tabla_fase0 | literal a trozos | R_ESPERA_CI
    tabla_fase0 | literal | pasa
    ```
  - `test_en_codigo_la_mencion_cuenta_con_una_via_de_salida`, 14 casos: la forma del revisor y la
    mención sola pasan; `__import__`, `exec`, `eval`, `compile`, `runpy`,
    `importlib.import_module`, `from importlib import`, `os.system`, `requests` y `socket` se
    niegan; `re.compile` no cuenta como `compile`.
  - **Roto a propósito**, `test_sin_la_excepcion_el_guion_de_la_fase_0_se_niega`: sin la excepción,
    `tabla_fase0.py` se niega; con una excepción que aceptara cualquier ruta, el guion con
    `importlib` sobre otra ruta pasa.
  - `test_riesgo_residual_la_mencion_a_trozos_no_se_ve` deja escrito el riesgo residual (abajo).
  - Los 72 de la tabla, sin cambios: los C1-C5, N7, N7b, N8c, N8b y N19 siguen negados (todos
    importan `subprocess` o `urllib`).
- **Lo que hacía antes, otra vez de verdad:** `python docs/validation/anexos/GUARDIA-CI/tabla_fase0.py`
  se ejecutó (solo llama a `decidir`) y pasó la guardia. Su salida es la tabla de después con el
  mismo guion que midió la de antes (`anexos/GUARDIA-CI/tabla_fase0-DESPUES.txt`): las 27 formas N
  (incluido N8, el guion rehecho) con `R_ESPERA_CI` y las 13 B que pasan.
- La suite entera de la guardia: **673 passed in 168.08s**.

### 5.2 Riesgo residual y hueco declarados (punto 0 y su último párrafo)

- **`"g" + "h"` con una vía de salida pasa.** `analizar_codigo` solo mira rutas compuestas con
  literales del MATERIAL (la deuda C), no una mención de la CI montada a trozos; no lo cubre, y no
  se arregla aquí. Lo fija `test_riesgo_residual_la_mencion_a_trozos_no_se_ve`.
- **La guardia no lee el código bajo `tests/`** cuando se le pasa a pytest (`guardia.py`,
  `_analizar_pytest`, el `continue` de `rel.startswith("tests/")`): un test que esperara a la CI
  pasaría. Es un hueco anterior a esta rama: no se arregla aquí.

### 5.3 La línea de Technical Debt que entra en el cierre

Junto a la que sale (§3), esta, para el commit del contrato del cierre:

> - La guardia de Claude Code no ve una consulta de CI en código cuando la mención se monta a trozos (`"g" + "h"`) junto a una vía de salida, ni cuando la vía de salida es un cliente de Python fuera de la lista cerrada del consultor (`aiohttp`); no ve como bucle una espera hecha a nivel de agente (`ScheduleWakeup`, `CronCreate`) con una consulta suelta en cada despertar; y no lee el código bajo `tests/` que se le pasa a pytest (`_analizar_pytest`): un test que esperase a la CI pasaría. Riesgos residuales declarados en trabajo/guardia-ci (GUARDIA-CI.md §5.2 y §9; los fijan `test_riesgo_residual_la_mencion_a_trozos_no_se_ve` y `test_riesgo_residual_un_cliente_fuera_de_la_lista_pasa`); el hueco de `tests/` es anterior a la rama. Para el carril de guardias.

### 5.4 Punto 1: el revisor

Hace sus pruebas en memoria con `tabla_fase0.py` o con un `python -c` que cargue la guardia por la
excepción (la forma de `CARGA_REVISOR` en el test pasa), sin montar nada a trozos, y declara en su
informe la forma que usó.

## 6. La CI de Linux (`fix/guardia-ci`)

Esperas y consultas, como manda la regla: tras el push, una consulta suelta por la API de check-runs
con el sha literal (la forma de abrir-rama), que dio el número del run; después una espera sin
consulta (`sleep 1200` solo, en segundo plano) y otra consulta suelta con `gh run view <run> --json
status,conclusion,headSha,headBranch`; el log del fallo, con `gh run view <run> --log-failed`
filtrado con `grep`.

| commit | run | resultado |
|---|---|---|
| `74336c7` (la respuesta a la PARADA 3) | **40056337257** | `failure`: 2 failed, 2830 passed, 11 skipped. Uno, el aceptado: `test_state_check_ok_on_real_repo`. **El otro, no:** `test_sin_la_regla_vuelve_lo_de_antes` con `{'D5': 'R_EJECUCION'}` |
| `7926d57` (el arreglo de D5) | **40059054099** | `completed` / `failure` con **1 failed, 2831 passed, 11 skipped**: solo el aceptado, `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/guardia-ci'» y la rama es `fix/guardia-ci`). Puerta de RITUAL.md cumplida |

**El fallo de D5, medido:** D5 es `"C:\Program Files\GitHub CLI\gh.exe" run view` en un bucle. Su
decisión ANTES (la de `main`, con la regla apagada) depende del sistema: en Windows pasa, y en
Linux es `R_EJECUCION`, porque la guardia de `main` saca el nombre del programa con
`os.path.basename`, que en Linux no parte por `\`, y lee la ruta entera como un programa
desconocido. La DESPUÉS es `R_ESPERA_CI` en los dos (`_programa` parte por `/` y por `\`), así que
la regla nueva no tiene el agujero; lo que fallaba era la columna «antes» del test, medida solo en
Windows. Arreglo: la columna «antes» de D5 queda por sistema (`P if os.name == "nt" else X`), con
el porqué y el run en el comentario. Es la lección de `trabajo/guardias-claude`: Windows tapa lo
que Linux no.

**Medido al esperar el segundo run** (lo que §0.i dejaba sin medir): un `sleep 60` en PRIMER plano
lo bloquea Claude Code, no la guardia («Blocked: standalone sleep 60. To wait for a condition, use
Monitor with an until-loop ... To wait for a command you started, use run_in_background: true»).
Su sugerencia de un `Monitor` con bucle es justo lo que esta rama niega si consulta la CI; la otra
vía, el `sleep` solo en segundo plano, es la del mensaje de la guardia, y es la que se usó. La forma
de esperar del mensaje («`sleep` solo, o en segundo plano») vale, pero en la práctica es en segundo
plano.


## 7. El encargo, punto por punto

| # | requisito | estado | evidencia |
|---|---|---|---|
| 1 | Verificar las tres cosas, el tag en origin, la CI de `main` y ninguna otra rama | Hecho | «Base comprobada al abrir» |
| 2 | Abrir con `abrir-rama`: encargo tal cual con la fecha, contrato y Archivo en HISTORIA | Hecho | `4f534bb` |
| 3 | Comprobar que la línea de Technical Debt sigue abierta | Hecho | `PROJECT_STATE.md:104` |
| 4 | Objetivo 1: negar una consulta de CI en un bucle o con una espera | Hecho | §1, §5; `test_la_tabla` |
| 5 | Objetivo 2: no negar la consulta suelta (`view` con `--json`/`--log-failed`/`--exit-status`, `list --branch`, `rerun`) | Hecho | B1-B5, B9-B12, B14 |
| 6 | Objetivo 3: la limpieza de V | Hecho de otra forma | medida en un clon y preparada para el cierre (respuesta 1, punto 7): §2 y §3 |
| 7 | Qué cuenta como consulta (gh run, gh api y curl sobre las tres rutas) | Hecho, ampliado | más `actions/jobs` y `commits/<sha>/status(es)` (respuesta 1, punto 1) y `gh pr checks` (ampliación de la fase 0, declarada en §0.f) |
| 8 | Las formas sueltas de RITUAL, abrir-rama, entregar-rama y cerrar-rama siguen pasando; buscar si hay más | Hecho | B7, B8, B4, B5; una más, la de `docs/HANDOFF.md:1051` (B13) |
| 9 | Shell: consulta en `while`/`until`/`for`, en la línea de `sleep`, `watch` o un bucle; `gh run watch` siempre | Hecho | N1-N18; `timeout N` con una consulta suelta pasa (respuesta 1, punto 2) |
| 10 | Guion o código en línea con `gh`/`curl` y bucle o espera | Hecho de otra forma | por las respuestas 1 (punto 3) y 3 (punto 0): mención con una vía de salida, con espera o sin ella (§5.1) |
| 11 | Reutilizar `analizar_codigo` y lo que la guardia ya lee | Hecho | la condición se llama dentro de `analizar_codigo`; usa `_literales`, `tokenizar`, `comandos`, `_quitar_envoltorios` |
| 12 | El mensaje de la negativa, con la vía buena | Hecho | `COMO_ESPERAR_CI`; `test_el_mensaje_dice_que_hacer` |
| 13 | Qué no cambia (motor, spec, parámetros, ambigüedades, feedback, casos, holdout, corpus, `data/`, `tools/mql5/`, Makefile, `.github/`, ffmpeg, cuarentena, `motivo_fichero`, K) | Hecho | `git diff --stat main...HEAD` (§7.1); de `guardia.py` solo se quitan las líneas del despacho de `decidir`, la cabecera y la llamada de shell de `_analizar_codigo_de` |
| 14 | No leer material del punto 3, ni transcripciones ni fotogramas | Hecho | exposiciones: ninguna (§0.j) |
| 15 | Negativas: PARADA salvo la forma que propone la guardia, declarada | Hecho | §4 |
| 16 | La CI con `gh run view` suelto, nunca un guion ni un bucle | Hecho | §6: consultas sueltas y una espera sin consulta |
| 17 | Si la guardia cambiada niega algo de antes, PARADA | Hecho | PARADA 3 |
| 18 | Fase 0 a): la tabla en memoria | Hecho | §0.a |
| 19 | Fase 0 b): qué partes ven bucles y esperas, dónde encaja, `solo_lectura.py` | Hecho | §0.b, §0.b' |
| 20 | Fase 0 c): skills y runbooks | Hecho | §0.c |
| 21 | Fase 0 d): los sitios de V, y si hay un tercero | Hecho | §0.d: había un tercero (PREGUNTAS.md) |
| 22 | PARADA de la fase 0 | Hecho | `55d691a` |
| 23 | Tests primero, en un fichero propio, rotos en los dos sentidos con las dos salidas | Hecho | `pytest-1-antes-del-codigo.txt` (66 fallos con la guardia de `main`), `pytest-2` y `pytest-3`; `test_sin_la_regla_vuelve_lo_de_antes`, `test_con_la_consulta_suelta_como_espera...`, `test_sin_monitor_en_decidir...`, `test_sin_la_excepcion...`, `test_si_falta_un_nombre...` |
| 24 | Un disfraz por familia | Hecho | D1-D18 (las familias de la fila de `trabajo/guardia-ffmpeg`, respuesta 1, y las del encargo) |
| 25 | Lo no decidible se niega, con su test | Hecho | D2, D13, D18; en código `__import__`, `exec`, `eval`, `compile`, `runpy`, `importlib` |
| 26 | Literales a trozos en `test_guardia_ci.py` | Hecho de otra forma | la respuesta 1 (punto 6) lo quita: la guardia no lee `tests/`; solo la ruta de marzo, por costumbre |
| 27 | `pytest test_guardia_ci.py` y `make check` siguen pasando por la guardia | Hecho | §1.4, §5.1 |
| 28 | Los tests comprueban el MOTIVO | Hecho | `_regla`; N3, N8d, N9-N9c, D2, D4, D9, D13-D18 pasan de otra regla a `R_ESPERA_CI` |
| 29 | El código mínimo, con comentario del porqué y el origen | Hecho | sección «esperar a la CI» de `guardia.py`; no es pequeña (unas 400 líneas con Monitor y la excepción de la respuesta 3), cada pieza con su porqué |
| 30 | `make check` completo con `PICO DE MEMORIA`, y el tiempo de la suite antes y después | Hecho | §1.6, §5 |
| 31 | Fase 2: la limpieza de V, la que dejen pasar los tests, y decir cuál | Hecho | las dos pasan (19 passed); preparada la A (§2) |
| 32 | El Technical Debt del guion sale en el cierre, preparado | Hecho | §3, §5.3 |
| 33 | Lo falso de la fase 0 c), corregido | Hecho | nada falso; la forma de esperar, añadida (respuesta 1, punto 5) |
| 34 | Informe con la tabla de la fase 0 antes y después | Hecho | §1.3; `tabla_fase0-ANTES.txt` y `tabla_fase0-DESPUES.txt` |
| 35 | `make check` sellado, push a `fix/guardia-ci`, CI con solo el fallo de `state check`, número del run | Hecho | §6: run 40059054099 sobre `7926d57`, consultado con `gh run view` suelto |
| 36 | El revisor, con el informe terminado, con sus cinco formas en memoria; su informe pegado | Hecho | §8 (encontró 15, 10 pasaban), §9 lo hecho con cada hallazgo |

**Respuesta 1:** 0 (Monitor en el matcher y en `decidir`, contrato en un commit propio, sus tests en los dos sentidos, la lista de herramientas y la prueba en vivo sin reiniciar) Hecho, §1.4 y PARADA 2; 1 Hecho; 2 Hecho (N15, N16, B14); 3 Hecho, y matizado por la respuesta 3; 4 Hecho (solo el recuadro); 5 Hecho; 6 Hecho (y su error, declarado); 7 Hecho; 8 Hecho (§1.5); el `for n` con su motivo (N3b) Hecho; los disfraces de la fila de ffmpeg Hecho.
**Respuesta 2:** 0 y 1 (las siete en `deny`, con su test roto en los dos sentidos y la prueba en vivo de `Artifact list` y `navigate about:blank`) Hecho; 2 Hecho (EnterWorktree fuera); 3 Hecho; la línea de Technical Debt Hecho (`PROJECT_STATE.md`).
**Respuesta 3:** 0 Hecho (§5.1; la etiqueta «(a)» describía la (b), declarado); el riesgo residual y el hueco de `tests/` declarados (§5.2, §5.3); 1 en el encargo del revisor (§8).

**Desviaciones declaradas:** `tests/unit/test_guardia_claude.py` en el contrato sin que lo pidiera el consultor (lo exigía su test del matcher); `gh pr checks` como consulta y `function`/`f()` como espera, ampliaciones de la fase 0; dos ajustes de la respuesta 3 que pidió la medida (`_sin_cadenas` y `PROGRAMAS_DE_DATOS`, §5.1); y la salida 1 de los tests es de una versión anterior del fichero (B19 con `git log`; la columna «antes» de D4, D9 y D13-D16 aún sin medir), declarado en §1.2.

### 7.1 Lo que no cambia, medido

`git diff --stat main...HEAD`: `.claude/hooks/guardia.py`, `.claude/settings.json`, las skills
`cerrar-rama` y `entregar-rama`, `PROJECT_STATE.md`, `contrato.yaml`, el encargo, `RITUAL.md`,
`docs/sesion-5/PREGUNTAS.md`, `docs/state/HISTORIA.md` (solo el Archivo 44), este informe,
`GUARDIA-FFMPEG.md` (el recuadro), su anexo, y tres tests (`test_guardia_ci.py` nuevo;
`test_guardia_claude.py` y `test_guardia_ffmpeg.py`, siete y seis líneas). Nada de `src/`,
`knowledge/`, `data/`, `config/`, `scripts/`, `tools/`, `mql5/`, `Makefile` ni `.github/`.
`scripts/contrato_rama.py`: «29 ficheros dentro del contrato» en el último `make check`.
`PROJECT_STATE.md`: 23.777 bytes (tope 25.000).

## 8. Revisor

El subagente `revisor`, lanzado el 2026-10-23 sobre `7926d57` con este informe terminado (las
ediciones sin commitear eran la fila del run 40059054099 en §6, la fila 35 de §7, el `## Estado` y
el párrafo «Medido al esperar el segundo run», que él mismo señala), con el alcance del encargo:
sus dos ejes y cinco formas de esperar a la CI fuera de la tabla, en memoria. Su informe, tal cual.
No cita ningún tramo no citable: 0 retiradas. Se omite solo la línea que el arnés de Claude Code
antepuso al devolverlo («[harness: subagent output matched instruction-shaped pattern(s):
settings-json ...]»), que no es del revisor.

## Informe del revisor · trabajo/guardia-ci · 2026-10-23

HEAD 7926d57, base main 2a99e64. Además de lo commiteado, el árbol de trabajo tiene una edición sin commitear en `docs/validation/GUARDIA-CI.md` (12 líneas añadidas y 3 quitadas). Incluye la fila de §6 con el run 40059054099, la fila 35 de §7 y el `## Estado`, como dijiste. También incluye un párrafo nuevo de §6, «Medido al esperar el segundo run», que no estaba en tu lista.

**Forma usada para las pruebas en memoria:** `uv run python -c` con la carga exacta de la excepción: `import importlib.util, sys; spec = importlib.util.spec_from_file_location("g", ".claude/hooks/guardia.py"); g = importlib.util.module_from_spec(spec); sys.modules["g"] = g; spec.loader.exec_module(g)`. Después llama a `g.decidir({"tool_name": ..., "tool_input": {"command": ...}, "cwd": "C:/Users/USER/Desktop/Bot v3"}, g.Politica(g.RAIZ))`. El código no tiene ninguna vía de salida ni monta nada a trozos. La guardia dejó pasar las tres llamadas, así que la excepción funciona en la práctica para el revisor. No ejecuté de verdad ninguna forma ni consulté la CI.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | §1.5 cita `.claude/settings.json:69` como «la configuración que lo hace», que es justo la evidencia que pedía el punto 8 de la respuesta 1. En la rama, la línea 69 ya no es el matcher: lo era en `main`, y la propia rama la movió al añadir siete líneas a `deny`. Ahora el matcher está en `:76` (`PreToolUse` en `:74`). En la PARADA 2 (línea 393 del informe) la cita era correcta, porque se escribió antes del cambio. | `GUARDIA-CI.md:666`; `sed -n '67,70p' .claude/settings.json` da el hook `estado_sesion.py` y `"timeout": 10`; `grep -n '"matcher"' .claude/settings.json` da `76: "matcher": "Read\|Grep\|Glob\|Bash\|PowerShell\|Monitor"` |
| a2 | menor | La tabla §1.3 da a D5 «antes: pasa» sin decir que eso solo vale en Windows. En Linux es `R_EJECUCION`, y el test ya lo distingue. §6 lo explica, pero la tabla no remite allí. | `GUARDIA-CI.md:604`; `tests/unit/test_guardia_ci.py:141` (`P if os.name == "nt" else X`) |
| a3 | menor | La numeración de la fase 0 salta de 0.f a 0.h: no hay 0.g. | `GUARDIA-CI.md:210` y `:244` |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` → «CONTRATO: 29 ficheros dentro del contrato de trabajo/guardia-ci (riesgo alto, artefacto docs/validation/GUARDIA-CI.md, tramo 'Carril: guardias y deuda', 3 comprobaciones para el revisor)», exit 0.
- **Suites de la guardia.** `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_ci.py tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py` → exit 0, 673 puntos (9×72+25), coincide con el «673 passed» de §5.1. Añadí `-p no:cacheprovider` para no escribir la caché. La línea de resumen no salió en la salida capturada.
- **`make check`.** No lo ejecuté porque escribe. `make-check.log` da `2843 passed in 932.78s`, `SELLO: make check en verde sobre el arbol 75a18b1a9490f195ea481e110f328c7f6e99a11e`, igual a `git rev-parse 7926d57^{tree}`, y `PICO DE MEMORIA de make check: 297 MiB en test`.
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`: `git log ... -- knowledge/spec knowledge/cases` sale vacío.
- **Holdout y material.** Nada de `knowledge/`, `data/` ni `corpus/` en el diff. §0.j declara ninguna exposición. La ruta de marzo solo aparece montada a trozos, sobre un fichero inventado en `tmp_path`.
- **Regímenes de cambio.** No hay cambios en evidence, feedback, manifests, transcripciones, fotogramas ni `libros.yaml`. `HISTORIA.md` solo añade líneas: 0 líneas `-`.
- **Ambigüedades, ADR y citas de la spec.** No se tocan: no aplica.
- **Informes cerrados.** `GUARDIA-FFMPEG.md` solo gana un recuadro `>` con fecha y rama, junto al pasaje que corrige. `docs/sesion-5/PREGUNTAS.md` solo gana su recuadro (punto 4).
- **Citas del informe comprobadas:** `DECISIONES-DE-PROCESO.md:28`, con el texto citado literal; `HOJA-DE-RUTA.md:420` («Estado: HECHA (2026-10-22…»); `solo_lectura.py:11-12`; `guardia.py:1989-1990` de `main` (el `continue` de `tests/`); `PROJECT_STATE.md:104`. Todas sostienen lo que se afirma, salvo a1.
- **Cifras.** `PROJECT_STATE.md` pesa 23.777 bytes (cuadra con §7.1). 1669 tests = 1655 + las 14 funciones de `test_guardia_ci.py`.
- **El informe** existe y acaba en su `## Estado`.
- **Ensayos aislados.** La limpieza de V se ensayó con `git worktree add --detach`, según §2.

### Eje (b) · Encargo
Resumen: 0 bloquea, 7 importa, 0 menor. Requisitos: 29 hechos (4 de ellos «hecho de otra forma», todos declarados), 1 parcial, 0 no hechos, 1 en curso (este revisor).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Verificar la base (tag en origin, CI de main en success, ninguna otra rama) | Hecho | informe, «Base comprobada al abrir». La CI no la reconsulté. |
| 2 | Abrir con abrir-rama: encargo, contrato y Archivo en HISTORIA | Hecho | `4f534bb`; HISTORIA solo añade líneas |
| 3 | La línea de Technical Debt sigue abierta | Hecho | `PROJECT_STATE.md:104` |
| 4 | Objetivo 1: negar consulta + bucle o espera | Hecho, con huecos | `test_la_tabla`, 72 casos en verde; huecos en b1-b4 |
| 5 | Objetivo 2: la consulta suelta pasa | Hecho | B1-B5 y B9-B14; en memoria también pasan `gh run list --branch fix/guardia-ci --limit 3 --json databaseId,status,headSha` y `gh run view 40059054099 --json status,conclusion,headSha,headBranch` |
| 6 | Objetivo 3: la limpieza de V | Hecho de otra forma | preparada para el cierre por el punto 7 de la respuesta 1, declarado en §2 y §3 |
| 7 | Qué cuenta como consulta, más las rutas nuevas | Hecho | `RUTA_DE_CI` en `guardia.py`; R1-R4 |
| 8 | Las formas sueltas de los runbooks y las skills siguen pasando; buscar más | Hecho | B7, B8 y B13 en la tabla |
| 9 | Shell: bucle, `sleep`, `watch`; `gh run watch` siempre | Hecho | N1-N18 |
| 10 | Guion o código: `gh` o `curl` con bucle o espera | Hecho de otra forma | respuestas 1 (punto 3) y 3 (punto 0), declarado en §5.1; huecos en b2 |
| 11 | Reutilizar `analizar_codigo` | Hecho | `_exigir_codigo_sin_ci` se llama desde `analizar_codigo` |
| 12 | El mensaje de la negativa | Hecho | `COMO_ESPERAR_CI`; `test_el_mensaje_dice_que_hacer` |
| 13 | Lo que no cambia | Hecho | `git diff --name-status main...HEAD`: nada de `src/`, `knowledge/`, `data/`, `config/`, `scripts/`, `tools/`, `mql5/`, Makefile ni `.github/`. De `guardia.py` solo se quitan las líneas que §7 nombra. |
| 14 | No leer material del punto 3 | Hecho | §0.j; `HOLDOUT-EXPOSICIONES.md` sin tocar |
| 15 | Ante una negativa, PARADA o la forma que propone la guardia | Hecho | §4 |
| 16 | La CI con `gh run view` suelto | Hecho según §6 | sin verificar (está prohibido consultarla) |
| 17 | Si la guardia cambiada niega algo que antes se hacía, PARADA | Hecho para lo que vio (PARADA 3) | b5: queda una regresión sin ver |
| 18 | Fase 0 a-d y su PARADA | Hecho | §0.a-§0.d; `55d691a` |
| 19 | Tests primero, rotos en los dos sentidos, con las dos salidas | Hecho | `pytest-1` y `pytest-2`; cinco tests rotos a propósito |
| 20 | Un disfraz por familia (más la fila de guardia-ffmpeg) | Hecho | D1-D18 |
| 21 | Lo que no se puede decidir se niega, con su test | Hecho para lo que reconoce | D2, D13, D18; b3: `viddy` no |
| 22 | Literales a trozos | Hecho de otra forma | respuesta 1, punto 6 |
| 23 | pytest y `make check` siguen pasando por la guardia | Hecho | mi pytest pasó la guardia; `make-check.log` sellado |
| 24 | Los tests comprueban el MOTIVO | Hecho | `_regla`, `test_guardia_ci.py:238-244` |
| 25 | Código mínimo, con el porqué y el origen | Hecho | comentario de la sección; el tamaño está declarado |
| 26 | `make check` con `PICO DE MEMORIA` y los tiempos antes y después | Hecho | §1.6, §5 (lo que sale es el `make check` de `e43d5b2`) |
| 27 | Fase 2: V, Technical Debt y lo que la fase 0 c) halló falso | Hecho de otra forma / Hecho | §2, §3, §5.3 |
| 28 | Tabla de la fase 0 antes y después | Hecho | §1.3; `tabla_fase0-ANTES.txt` y `-DESPUES.txt` |
| 29 | `make check` sellado, push a `fix/`, CI y número del run | Parcial | push comprobado: `git ls-remote` da `7926d5779c…` en `refs/heads/fix/guardia-ci`. El `make check` del último commit no está en el informe (b6). |
| 30 | El revisor y su informe pegado | En curso | este informe |
| R1 | Respuesta 1, puntos 0-8, el `for n` y los disfraces | Hecho | contrato ampliado en commit propio (`babecf5`); tests de Monitor en los dos sentidos; prueba en vivo 2c de `pruebas-en-vivo.txt`; la cita del punto 8 es la de a1 |
| R2 | Respuesta 2, puntos 0-3 | Hecho | las siete herramientas en `deny` (diff de `settings.json`); test roto en los dos sentidos; `Artifact list` y `navigate about:blank` negadas en vivo |
| R3 | Respuesta 3, puntos 0 y 1, y el hueco de `tests/` | Hecho, con huecos | §5.1-§5.4; b2 |
| — | Respuestas copiadas tal cual en el encargo y en el informe | Hecho | las tres, comparadas por programa: IGUAL |
| — | «El encargo, punto por punto» | Hecho | §7 |

**Las formas de esperar a la CI que no están en §1.3 ni en §5.1, pasadas por `decidir` en memoria:**

| id | comando (Bash, salvo indicación) | resultado |
|---|---|---|
| K1 | `gh pr checks 12 --watch=true` (también como `Monitor`) | **PASA** |
| K2 | `viddy -n 30 gh run view 39893825671` (también como `Monitor`) | **PASA** |
| K4 | `while true; do gh pr view 12 --json statusCheckRollup; sleep 30; done` | **PASA** |
| K15 | `while true; do gh pr status; sleep 30; done` | **PASA** |
| K5 | `python -c "from os import *; import time` + `while True: system('gh run view …'); time.sleep(30)"` | **PASA** |
| K7 | `python -c "import os,time` + `while True: getattr(os,'system')('gh run view …'); time.sleep(30)"` | **PASA** |
| K6 | `node -e "setInterval(async()=>console.log(await (await fetch('<API>/commits/<sha>/check-runs')).text()),30000)"` | **PASA** |
| K12 | `node -e "setInterval(()=>console.log(require('child_process').execSync('gh run view …').toString()),30000)"` | **PASA** |
| K10 | `python -c` con `aiohttp` y `asyncio.sleep(30)` en un `while True` sobre `check-runs` | **PASA** |
| K11 | `gh run view R && timeout 300 tail -f Makefile; gh run view R` | **PASA** |
| K13 | `curl -sf --retry 50 --retry-delay 30 --retry-all-errors <check-runs>` | PASA (dudosa: reintenta solo si hay error, no espera a que termine) |
| K3 | `gh run view R; ping -n 300 127.0.0.1; gh run view R` | niega, pero por otra regla (`R_EJECUCION`: «antes, en el mismo comando, va `gh run view`») |
| K8 | `gh alias set w 'run watch'` y `gh w R` | niega (`R_EJECUCION`: subcomando fuera de la lista cerrada) |
| K9 | `while true; do gh workflow view ci.yml; sleep 30; done` | niega (`R_EJECUCION`: `gh workflow`) |
| K14 | `gh run view R; read -t 300 x; gh run view R` | niega (`R_EJECUCION`: `read` fija `x`) |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | `gh pr checks --watch=true` pasa, en Bash y en `Monitor`, aunque la rama declara que `gh pr checks --watch` se niega «siempre» (N14). La condición busca la palabra exacta `"--watch"`. Que `gh` acepte `--watch=true` es lo normal en pflag, pero no lo ejecuté. | `guardia.py`, `_consulta_gh`: `sub == ["pr", "checks"] and "--watch" in palabras[i:]`; salida en memoria: `K1 \| PASA`, `K1m Monitor \| PASA` |
| b2 | importa | En código, la vía de salida se reconoce solo por cómo se escribe y solo con nombres de Python. (1) `os.system`, que la respuesta 3 nombra expresamente, se esquiva con `from os import *` + `system(` (K5) o con `getattr(os,'system')` (K7). (2) `node -e` lo analiza la guardia como código (`node` está en `INTERPRETES`, `guardia.py:952`), pero `fetch(` y `execSync(` no están en `_SALIDA_DEL_PROCESO`: K6 y K12 pasan. (3) `aiohttp` no está en la lista cerrada del consultor: K10 pasa. No es el riesgo residual `"g"+"h"` que declara §5.2: aquí la mención se ve entera. | `_SALIDA_DEL_PROCESO` exige `\.system\s*\(` o `from os import … system`; salida: `K5 \| PASA`, `K7 \| PASA`, `K6 \| PASA`, `K12 \| PASA`, `K10 \| PASA` |
| b3 | importa | Hay esperas que no se reconocen. Un programa desconocido que envuelve una consulta (`viddy -n 30 gh run view`, K2) cuenta como consulta pero no como espera, en contra de «lo que no se pueda decidir se niega» (fase 1 del encargo). `timeout 300 tail -f` (K11) es una espera y no está en `PROGRAMAS_QUE_ESPERAN`. | `PROGRAMAS_QUE_ESPERAN = frozenset({"sleep", "watch"})`; `K2 \| PASA`, `K11 \| PASA` |
| b4 | importa | Hay consultas de CI que no se reconocen: `gh pr view --json statusCheckRollup` (K4) y `gh pr status` (K15), que preguntan lo mismo («¿ha terminado?»), pasan dentro de un `while … sleep`. Quedan fuera de la definición del encargo, pero la fase 0 ya la amplió a `gh pr checks` con ese mismo argumento. | `_consulta_gh` solo reconoce `run view\|list\|watch` y `pr checks`; `K4 \| PASA`, `K15 \| PASA` |
| b5 | importa | Regresión que no vio la PARADA 3: `rg -n "gh run watch" docs/runbooks`, una búsqueda de texto, pasa con la regla apagada (lo de `main`) y ahora se niega con `R_ESPERA_CI`. `rg` no está en `NO_EJECUTAN` ni en `PROGRAMAS_DE_DATOS`, así que su patrón se lee como Bash. Con `grep` y `git grep` pasa. La regla de la rama es: «te niega algo que antes hacías → hallazgo». | En memoria: `con la regla F2 \| NIEGA: esperar a la CI: \`gh run watch\`…`; `sin la regla F2 \| PASA`; `rg en NO_EJECUTAN: False \| rg en PROGRAMAS_DE_DATOS: False` |
| b6 | importa | La fila 35 de §7 dice «`make check` sellado … Hecho, §6», pero §6 solo trae la CI. El informe recoge únicamente el `make check` de `e43d5b2` (§5) y ninguno de `74336c7` ni de `7926d57`. La evidencia existe fuera del informe: `make-check.log` da 2843 passed, `SELLO` sobre el árbol de `7926d57` y `PICO DE MEMORIA` de 297 MiB. | `GUARDIA-CI.md:942` y `:788-790`; `make-check.log:77,101,103`; `git rev-parse 7926d57^{tree}` = `75a18b1a…` |
| b7 | importa | Lo que propone el mensaje («`sleep` solo») no se puede hacer en primer plano: Claude Code lo bloquea, y en su lugar sugiere un `Monitor` con bucle, que esta rama niega si consulta la CI. §6 lo declara, pero el texto que copiaron las skills y `RITUAL.md:320` sigue diciendo «`sleep` solo». Ese texto lo fijó el consultor (punto 5), así que la decisión de cambiarlo es suya. | `GUARDIA-CI.md` §6, párrafo sin commitear «Medido al esperar el segundo run»; diff de `RITUAL.md` y de las dos skills |

### Lo que no pude comprobar
- Los runs 40056337257 y 40059054099, y la CI de `main` 39893825671: el encargo prohíbe consultar la CI. Solo comprobé que `fix/guardia-ci` apunta a `7926d57` (`git ls-remote`).
- `make check`: escribe, así que no lo ejecuté. Lo sustituye `make-check.log`, cuyo sello coincide con el árbol de `7926d57`. Las ediciones sin commitear del informe necesitarán su propio `make check`.
- Que `gh` acepte `--watch=true` (K1), y lo que devuelven `gh pr view --json statusCheckRollup` y `gh pr status`: no ejecuté `gh`.
- Si `Monitor` tiene más parámetros que `command`, `description` y `timeout_ms`, y por tanto si `R_MONITOR` negaría un uso legítimo: no tengo esa herramienta en esta sesión. La rama prefiere negar ante la duda, así que es un riesgo de falso positivo, no un hueco.
- Que el hook corre para los subagentes lo confirmé de paso: la guardia de proyecto me bloqueó a mí (revisor) un `for c in …` con `R_EJECUCION`, el mismo mensaje que `pruebas-en-vivo.txt`.
- Un bucle hecho a nivel de agente (`ScheduleWakeup` o `CronCreate`, con consultas sueltas en cada despertar) no lo puede decidir `decidir`, y no lo probé.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read `docs/encargos/trabajo-guardia-ci.md`, `contrato.yaml` y `docs/validation/GUARDIA-CI.md` (entero, en dos tramos)
3. `uv run python scripts/contrato_rama.py`
4. `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_ci.py tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py 2>&1 | tail -15` (en segundo plano)
5. `git diff main...HEAD -- .claude/settings.json && git diff --name-status main...HEAD && git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases | head`
6. `git diff main...HEAD -- .claude/hooks/guardia.py`
7. `grep -n "_es_interprete\b" …` y `grep -n "^INTERPRETES\|^def _es_interprete" -A8 .claude/hooks/guardia.py`
8. `grep -nE … tests/unit/test_guardia_ci.py`; Read `tests/unit/test_guardia_ci.py` (líneas 1-94 y 176-470)
9. `uv run python -c '<carga por la excepción>; K1…K15 por g.decidir'`
10. `git diff main...HEAD -- docs/validation/GUARDIA-FFMPEG.md docs/sesion-5/PREGUNTAS.md docs/runbooks/RITUAL.md .claude/skills PROJECT_STATE.md tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py && git diff main...HEAD -- docs/state/HISTORIA.md | grep -c '^-[^-]'`
11. `git show main:.claude/hooks/guardia.py | sed -n '1986,1991p'`; `grep`/`sed` sobre `guardia.py`, `solo_lectura.py`, `settings.json`, `DECISIONES-DE-PROCESO.md`, `HOJA-DE-RUTA.md` y `PROJECT_STATE.md`
12. `ls -la make-check.log; grep -n "SELLO\|PICO DE MEMORIA\|passed in\|exit=" make-check.log | tail -8; grep -n … GUARDIA-CI.md; grep -n "Depende de R1.1" PROJECT_STATE.md`
13. `git rev-parse 7926d57^{tree} 74336c7^{tree} e43d5b2^{tree}; git log -3 --format='%h %ci'; sed -n '70,103p' make-check.log | grep …`
14. Read `docs/validation/anexos/GUARDIA-CI/pruebas-en-vivo.txt` y `tabla_fase0-DESPUES.txt`
15. `git diff --stat; git diff docs/validation/GUARDIA-CI.md | grep '^[-+]'; wc -c PROJECT_STATE.md`
16. `git ls-remote --heads origin fix/guardia-ci trabajo/guardia-ci`
17. `uv run python -c '<carga>; F1-F7, K1m y K2m (Monitor) por g.decidir'`
18. Read de la salida de la tarea de fondo (pytest)
19. `uv run python -c '<carga>; rg con la regla y sin ella (exigir_sin_espera_a_la_ci apagada en memoria)'`
20. `uv run python -c '<compara las tres respuestas copiadas en el encargo y en el informe>'`
21. `sed -n '67,70p' .claude/settings.json; git show main:.claude/settings.json | sed -n '67,70p'; grep -n "settings.json:69\|settings.json:7" GUARDIA-CI.md`
22. `for c in …; do git show --stat …; done`: **NEGADO por la guardia** («ejecutar `for c`: el bucle `for` fija `c`, que no esta en la lista (`NOMBRES_DE_ENTORNO`)»). Seguí con la forma equivalente de una sola llamada, sin bucle: `git log --stat --format='== %h %s' main..HEAD | grep -v '^$'`
23. Grep `^#+ .*(0\.g|§8|^## 8)` en `GUARDIA-CI.md` (sin resultados)

## 9. Lo que se hizo con los hallazgos del revisor

| # | gravedad | qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado**: §1.5 cita ahora `.claude/settings.json:74-76` en la rama (`:69` en `main`). La PARADA 2 se queda con `:69`, que era lo verdadero cuando se escribió. |
| a2 | menor | **Arreglado**: la fila D5 de §1.3 dice «pasa en Windows; `R_EJECUCION` en Linux (§6)». |
| a3 | menor | **Contestado**: no hay 0.g porque la sección de decisiones de la fase 0 iba a ser 0.g y salió con el título de la skill («Lo que necesito que decidas»); los §0.h-§0.j se citan en el informe y en las respuestas, así que no se renumeran. |
| b1 | importa | **Arreglado**: `gh pr checks` niega con `--watch` y con `--watch=<valor>` (`_consulta_gh`). Test K1. |
| b2 | importa | **Arreglado en parte, el resto contestado.** (1) `from os import *` cuenta como vía de salida y `getattr(os|subprocess|sys|builtins, ...)` como no decidible: son la misma `os.system` de la lista del consultor escrita de otra forma (K5, K7, F4). (2) En un lenguaje que la guardia no analiza (`node -e` y los demás que no son Python), la mención de la CI basta para negar: sus vías de salida no se pueden decidir con la lista de Python (K6, K12); el `lo que no se pueda decidir se niega` del encargo. (3) `aiohttp` **no**: la lista del consultor es cerrada, y ampliarla es decisión suya; queda como riesgo residual declarado, con su test (`test_riesgo_residual_un_cliente_fuera_de_la_lista_pasa`) y en la línea de Technical Debt del cierre (§5.3, ampliada). |
| b3 | importa | **Arreglado**: un programa que lanza `gh`, `curl` o `wget` y no es uno de ellos (`viddy`, `xargs`, `find -exec`, uno desconocido) cuenta como espera, porque puede repetirla (`LANZADORES_SIN_REPETICION`); y `tail -f`/`-F`/`--follow` también (K2, K11, K16). |
| b4 | importa | **Arreglado**: `gh pr status` y `gh pr view` con `statusCheckRollup` son consultas (K4, K15); `gh pr view --json title` sigue sin serlo (F3). Ampliación de «qué cuenta como consulta», con el mismo argumento con que la fase 0 añadió `gh pr checks`; declarada. |
| b5 | importa | **Arreglado y declarado como regresión cazada por el revisor** (la PARADA 3 no la vio): `rg`, `egrep`, `fgrep`, `ag`, `ack`, `less` y `more` entran en `PROGRAMAS_DE_DATOS`; `rg -n "gh run watch" docs/runbooks` vuelve a pasar (F2). No hubo PARADA porque no la sufrió la sesión, sino que la encontró el revisor en memoria, y el arreglo devuelve exactamente lo de `main`; se te dice aquí y en el mensaje de entrega. |
| b6 | importa | **Arreglado**: §6 trae el `make check` de cada commit con CI (abajo, §9.1). |
| b7 | importa | **Para el consultor**: el texto de las skills y de `RITUAL.md:320` es el que fijaste en la respuesta 1, punto 5 («`sleep` solo, o en segundo plano»); medido, `sleep` solo en primer plano lo bloquea Claude Code. Propuesta: «una espera sin consulta (`sleep` en segundo plano)». No lo cambio sin tu orden. |

Lo que el revisor no pudo comprobar y queda declarado: un bucle a nivel de agente (`ScheduleWakeup`
o `CronCreate`, con una consulta suelta en cada despertar) no pasa por la guardia como bucle: cada
consulta es suelta. Va a la línea de Technical Debt del cierre (§5.3).

### 9.1 Los `make check` de los commits con CI

| commit | `make check` | `PICO DE MEMORIA` |
|---|---|---|
| `e43d5b2` (fases 1 y 2) | exit 0, 2826 passed, `SELLO` sobre el árbol `0292e735…` | 298 MiB |
| `74336c7` (PARADA 3) | exit 0, 2843 passed in 914.16s, `SELLO` sobre el árbol `e328feaf…` | 297 MiB |
| `7926d57` (D5) | exit 0, 2843 passed in 932.78s, `SELLO` sobre el árbol `75a18b1a…` (`= 7926d57^{tree}`, revisor) | 297 MiB |
| el de los hallazgos del revisor | su `make check` y su run van en el mensaje de entrega: un commit no puede llevar su propio sello ni su propia CI | |

## Estado

LISTA PARA REVISIÓN. Fase 0 y tres PARADAS con sus respuestas aplicadas; la regla, Monitor y los
permisos, con sus tests (16 funciones, 115 casos) y sus pruebas en vivo; la CI de Linux de
`7926d57` con solo el fallo aceptado (run 40059054099); el revisor, con sus hallazgos arreglados o
contestados (§9). Pendiente de decisión del consultor: el texto «`sleep` solo» (b7) y la lista
cerrada de vías de salida (`aiohttp`, b2). El `make check` y el run del commit de los hallazgos del
revisor van en el mensaje de entrega. Lo que entra y sale en el cierre, preparado en §3 y §5.3.

Rama lista para revisión, NO cerrada.
