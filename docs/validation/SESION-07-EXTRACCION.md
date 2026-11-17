# Sesión 7a con el trader: la extracción por pregunta y por sesión del bloque de días

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras, en
> `PREGUNTAS-7B.md`, en `SESION_EN_CURSO` ni en la hoja de ruta (R4.3 sigue ABIERTA). Cada
> «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de cada respuesta lo
> decide el consultor en la rama de activación de la 7a (encargo del 2026-11-17,
> `docs/encargos/trabajo-sesion-07.md`).

Rama `trabajo/sesion-07`, abierta el 2026-11-17 desde `main` en `ed5f9eef` (commit de estado sobre
el merge `0f420593`, tag `stable/F39c-skills-metodo`). Tramo R4 de la hoja de ruta (R4.3, NA:F).
Skill `ingerir-sesion`, de principio a fin, y ADR-0093 §2. Plantilla: `SESION-06-EXTRACCION.md`.
Tag de cierre previsto: `stable/F39d-sesion-07` (no existe ni en local ni en origin:
`git tag -l` y `git ls-remote --tags origin` vacíos).

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse main origin/main` da dos veces `ed5f9eef606488417d3a305a29714b4407cb3304`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F39c-skills-metodo`;
  `git rev-parse "stable/F39c-skills-metodo^{commit}"` = `git rev-parse main^1` =
  `0f420593008338e5140747443bee673df00ee81a`; `git ls-remote --tags origin` da
  `4691f0eb… refs/tags/stable/F39c-skills-metodo` (el objeto del tag anotado) y su `^{}`,
  `0f420593…`. Es también el primero de `git tag -l 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 43654960018`: `completed`,
  `success`, `headSha` `ed5f9eef606488417d3a305a29714b4407cb3304`, `push` en `main`.
- `git branch -a` solo da `main` y `origin/main`; `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"07": {` en la línea 251 de
  `CODIGOS_DE_SESION_TEXTO`, con 6 textos que son los títulos de S-1 a S-6 de
  `docs/sesion-7/PREGUNTAS-7A.md` (líneas 85, 125, 160, 192, 229 y 267) con la primera letra en
  minúscula; `"07": ORDEN_SESION_07` en `HOJAS` (línea 276); `SESION_EN_CURSO = "07"` (línea 281).
- `PROJECT_STATE.md` tras abrir: 23.519 bytes (`wc -c`; 23.428 en `main`).

## Decisiones de proceso de la rama

- Al buscar el contrato de `trabajo/sesion-06` como modelo, la guardia negó (solo lectura) un bucle
  `git log ... | while read h; do git show $h:contrato.yaml ...; done`: «`read` fija `h`, que no esta
  en la lista cerrada (`NOMBRES_DE_ENTORNO`)». Seguí la forma que propone su mensaje (sin `$(...)`,
  detrás solo `grep`/`head`): `git log --all --full-history --format='%h %s' -- contrato.yaml | grep
  -i 'abre trabajo/sesion'` y `git show 6c96499a:contrato.yaml` (`docs/runbooks/DECISIONES-DE-PROCESO.md`).
- La guardia negó `uv run botsito state check ...; uv run python scripts/contrato_rama.py ...` en un
  solo comando («antes, en el mismo comando, va `uv run botsito state check`»); seguí su forma: una
  llamada por ejecutable.
- **El primer `make check` de la apertura salió en rojo y sin sello** (exit 2; `1 failed, 3512
  passed, 6 xfailed in 1173.28s`): `tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths`,
  «rutas ignoradas no previstas: ['.claude/settings.local.json']». La causa: un
  `.claude/settings.local.json` de 298 bytes creado FUERA de esta sesión el 2026-11-16 a las 21:30
  (unas reglas `deny` de un MCP ajeno al proyecto). No lo toqué ni amplié el test (fuera del
  contrato): PARADA. Aleks lo resolvió sacándolo del repo. Primero dijo que ya lo había movido a su
  Escritorio, pero el fichero seguía en el repo con la misma hora; con su autorización expresa busqué la
  copia solo en el primer nivel de `C:\Users\USER\Desktop` (ni `settings.local.json` ni ningún
  `.json`; ninguna carpeta abierta) y, al no encontrarla, no borré nada: lo moví a
  `C:\Users\USER\Desktop\respaldo-settings\settings.local.json` (298 bytes, la misma hora) por orden
  suya, y comprobé que ya no está en el repo. Después, el sello de apertura se relanzó con lo mismo
  estadiado más estas líneas y la desviación de 0.1.

## 0. Lo primero

### 0.1 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-16`: `False`.
- `2026-11-17`: `False`.

**Desviación del paso 1, declarada**: según Aleks (2026-11-17), los dos días NO se comprobaron antes
de grabar; se comprobaron hoy, después, por la sesión. Declarada también en
`HOLDOUT-EXPOSICIONES.md` (2026-11-17). Precedente: `SESION-06-EXTRACCION.md` §0.2.

### 0.2 Los vídeos

Son los dos únicos vídeos del primer nivel de `corpus/Estrategia del trader/` que no estaban en
`fuentes.yaml`, que acababa en v17:
- `Grabación de pantalla 2026-11-16 145418.mp4`, 7.507.070.830 bytes (v18, el primer día);
- `Grabación de pantalla 2026-11-17 135357.mp4`, 6.332.347.809 bytes (v19, el segundo día).

La Next Action F daba la 7a para el domingo 2026-11-15: se grabó el 2026-11-16 y el 2026-11-17, y el
id de la sesión es `2026-11-16-sesion-07` (el del primer día; encargo, ENTRADAS). La orden de cierre
lo recoge.

## Estado

EN CURSO.
