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

## Estado

EN CURSO · PARADA de la fase 0: espero la respuesta del consultor a «Lo que necesito que decidas».
