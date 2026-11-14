# SKILLS-METODO · tres skills al día con ADR-0093 y las lecciones registradas

PLANTILLA: este informe no trae tabla final de preguntas al trader; es una rama de documentos.

Rama `trabajo/skills-metodo` (tramo «Carril: guardias y deuda» de `docs/plan/HOJA-DE-RUTA.md`).
Encargo del consultor del 2026-11-14: `docs/encargos/trabajo-skills-metodo.md`.

Estado: EN CURSO.

## Apertura (2026-11-14)

Base comprobada con git y gh antes de abrir, tras `git fetch --prune origin`:

| Comprobación | Salida |
|---|---|
| `git rev-parse --short main` | `73b4e7a9` |
| `git rev-parse main origin/main` | `73b4e7a98cefd62dd820e28f0627ae7499ad5976` las dos veces |
| `git rev-parse "stable/F39b-dieta-estado^{commit}"` = `git rev-parse main^1` | `6054c4cee7fc6e2c735956f3a70944e765e591af` las dos |
| `git ls-remote --tags origin stable/F39b-dieta-estado` | `7d3bd785… refs/tags/stable/F39b-dieta-estado` (tag anotado; su commit, `6054c4ce…`) |
| Último `- Tag: ` de HISTORIA | `stable/F39b-dieta-estado` |
| CI de `main` en `73b4e7a9…` (check-runs, sha literal) | `python completed success`, run 43560175823 |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` en local y en origin |
| `stable/F39c-skills-metodo` | no existe ni en local (`git tag -l`) ni en origin (`git ls-remote --tags`) |
| Tramo | `## Carril: guardias y deuda` en `docs/plan/HOJA-DE-RUTA.md:700`, literal |
| `wc -c PROJECT_STATE.md` en main | 23879 |
| Modelo | Opus 5.5, esfuerzo medio (fijado con `/effort` por Aleks antes del encargo) |

Desviaciones de la apertura, declaradas:

1. La fila de `docs/validation/HOLDOUT-EXPOSICIONES.md` del 2026-11-14 entra en el commit de
   apertura (encargo, punto 0), y `rutas_permitidas` la incluye: la verificación de `abrir-rama`
   («`git diff main --stat` = encargo, contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y el
   artefacto, nada más») no se cumple al pie de la letra hasta que D3 b) la ajuste.
2. El encargo se escribió con Write en la carpeta de trabajo de la sesión, tal cual, y un guion de
   Python le antepuso `> ` a cada línea al copiarlo a `docs/encargos/trabajo-skills-metodo.md`; no
   pasó por ningún heredoc.
