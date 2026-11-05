# Sesión 6 con el trader: la extracción por pregunta

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras ni en la
> hoja de ruta. Cada «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de
> cada respuesta lo decide el consultor en otra rama (encargo del 2026-11-04,
> `docs/encargos/trabajo-sesion-06.md`).

Rama `trabajo/sesion-06`, abierta el 2026-11-04 desde `main` en `136280d` (commit de estado sobre el
merge `1cbf403`, tag `stable/F38l-guardia-g1`). Tramo R4 de la hoja de ruta (R4.2, NA:F). Skill
`ingerir-sesion`, de principio a fin. Plantilla: `SESION-05-EXTRACCION.md`. Tag de cierre previsto:
`stable/F38m-sesion-06`.

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse --short main` = `136280d`; `git rev-parse main origin/main` da dos veces
  `136280d11873a3bfcf38e937deace14c74525b97`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F38l-guardia-g1`;
  `git rev-parse "stable/F38l-guardia-g1^{commit}"` = `git rev-parse main^1` =
  `1cbf4038b8cc6789bea81728a1cd08bd5ab450a2`; `git ls-remote --tags origin stable/F38l-guardia-g1`
  da `a9cc6b0… refs/tags/stable/F38l-guardia-g1` (el objeto del tag anotado). Es también el primero
  de `git tag --list 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 41935014939`:
  `completed`, `success`, `headSha` `136280d11873a3bfcf38e937deace14c74525b97`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`
  (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"06": {` en la línea 216 de
  `CODIGOS_DE_SESION_TEXTO`, con 23 textos; `"06": ORDEN_SESION_06` en `HOJAS` (línea 250), con 23
  códigos; `SESION_EN_CURSO = "06"` (línea 252).

## 0. Lo primero

### 0.2 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-04`: `False`. **Desviación del paso 1, declarada** (encargo): la sesión se adelantó del 3
  al 4, y este día se comprobó DESPUÉS de grabar, no antes. Declarada también en
  `HOLDOUT-EXPOSICIONES.md` (2026-11-04).

### 0.3 El vídeo

Es el único vídeo del primer nivel de `corpus/Estrategia del trader/` que no estaba en
`fuentes.yaml`, que acababa en v16: `Grabación de pantalla 2026-11-04 142903.mp4`, 7.574.611.265
bytes.

## Estado

EN CURSO.
