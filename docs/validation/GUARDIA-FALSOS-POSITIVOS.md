# GUARDIA-FALSOS-POSITIVOS · un literal «// » y cmp, sin abrir ningun hueco

Rama `trabajo/guardia-falsos-positivos` (carril «guardias y deuda»: G.6 de la hoja de ruta y la
deuda de la guardia que dejo `trabajo/capa-generada`). Encargo del consultor del 2026-11-12:
`docs/encargos/trabajo-guardia-falsos-positivos.md`.

## Apertura (2026-11-12)

Base comprobada con git y gh antes de abrir:

- `git rev-parse main origin/main`: `4ecd7f17e89cc5e4bd8b999435bdf104b5e23e32` las dos veces
  (`git rev-parse --short main` = `4ecd7f17`, el commit de estado de `stable/F38z-capa-generada`).
- `git rev-parse "stable/F38z-capa-generada^{commit}"` = `git rev-parse main^1` =
  `7bccf3103250f6d89e0877e993cda2e449a3423f`; el tag esta en origin (`git ls-remote --tags`:
  `fde7d35a… refs/tags/stable/F38z-capa-generada`). `trabajo/capa-generada` esta cerrada: su
  registro de cierre es el ultimo de `docs/state/HISTORIA.md` y `git ls-remote --heads origin` solo
  da `main`.
- CI de `main` sobre `4ecd7f17…` (check-runs, con `gh api`): `python completed success`, check-run
  131643256110. El clasificador no nego `gh`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.
- `PROJECT_STATE.md`: 24.380 bytes en main; 24.569 tras la apertura (tope 25.000 de
  `tests/unit/test_project_state.py`). El cierre tendra que recortar antes de anadir.

Exposicion: cada `make check` lee el M1 entero de marzo y calienta con el de junio (Technical
Debt); la fila del 2026-11-12 de esta rama en `docs/validation/HOLDOUT-EXPOSICIONES.md` se escribio
antes del primero.

Negativa de la guardia durante la apertura (no del objeto de la rama): un comando mio de solo
lectura con una variable de shell (`c=$(git log ...)`) lo nego `NOMBRES_DE_ENTORNO`; se reescribio
como la propia guardia propone («sin esa variable»), en dos llamadas.

## Fase 0

Pendiente.

## Estado

EN CURSO (abierta; fase 0 por hacer).
