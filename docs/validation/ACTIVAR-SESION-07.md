# ACTIVAR-SESION-07 · Las respuestas de la sesión 7a entran en la spec y en el motor (R4.3, entrada F)

> PLANTILLA hasta la fase 0: la tabla de activación la escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/activar-sesion-07`, abierta el 2026-11-18 desde `main` en f66743e3 (commit de estado
sobre el merge 5c047f31 del tag `stable/F39d-sesion-07`). Encargo:
`docs/encargos/trabajo-activar-sesion-07.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
punto (1) de la F de la Next Action). Tag previsto: `stable/F39e-activar-sesion-07` (no existe ni en
local ni en origin: `git tag -l` y `git ls-remote --tags origin 'stable/F39e*'` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `f66743e3d8ec7fc75769d17be75c34d55d2bc4a7` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39d-sesion-07^{commit}"` = `5c047f3115806a7a8cddc17614c7d40ba9bd2cfc` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39d-sesion-07` da `e5490708…` (el objeto del tag anotado).
- CI de `main`: `gh run view 44316126260` (suelto, sin guion) → `status: completed`, `conclusion: success`, `headSha: f66743e3d8ec7fc75769d17be75c34d55d2bc4a7`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Desviaciones de la apertura

- **A-58 no va en el bloque `ids-inexistentes` del encargo.** El encargo pide declarar el ADR nuevo y
  A-58; el bloque solo admite ids de fuente (`comun.ids.FUENTE`: `ev-*`, `fb-*`, `ADR-NNNN`), y
  `validation/ids_citados.py` da «declaracion de ids-inexistentes mal formada: linea sin un id al
  principio» con cualquier otra cosa. Esa guardia no comprueba ids de ambigüedad en `docs/`, así que
  A-58 no necesita declaración: solo va el ADR nuevo.

## Estado

EN CURSO: fase 0.
