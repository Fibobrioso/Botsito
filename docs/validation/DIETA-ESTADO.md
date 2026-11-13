# DIETA-ESTADO · PROJECT_STATE.md adelgazado antes de la sesion 7a

PLANTILLA: este informe no trae tabla final de preguntas al trader; es una rama de estado.

Rama `trabajo/dieta-estado` (tramo «Carril: guardias y deuda» de `docs/plan/HOJA-DE-RUTA.md`;
precedentes: `trabajo/adelgazar-estado` y `trabajo/margen-pendiente`). Encargo del consultor del
2026-11-13: `docs/encargos/trabajo-dieta-estado.md`.

## Apertura (2026-11-13)

Base comprobada con git y gh antes de abrir, tras `git fetch --prune origin`:

| Comprobación | Salida |
|---|---|
| `git rev-parse --short main` | `c473d4c9` |
| `git rev-parse main origin/main` | `c473d4c9c28956039ce69ae88989261d47e6349c` las dos veces |
| `git rev-parse "stable/F39a-guardia-falsos-positivos^{commit}"` = `git rev-parse main^1` | `e931459873e9b73f6bd6e05d97b91e2f3c7afe9e` las dos |
| `git ls-remote --tags origin "stable/F39a*"` | `36e8c914… refs/tags/stable/F39a-guardia-falsos-positivos` (`^{}` = `e9314598…`) |
| Último `- Tag: ` de HISTORIA | `stable/F39a-guardia-falsos-positivos` (HISTORIA:17953) |
| CI de `main` en `c473d4c9…` (check-runs) | `python completed success`, run 43459199788 |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` en local y en origin |
| `stable/F39b-dieta-estado` | no existe ni en local (`git tag -l`) ni en origin (`git ls-remote --tags`) |
| Tramo | `## Carril: guardias y deuda` en `docs/plan/HOJA-DE-RUTA.md:700`, literal |
| `wc -c PROJECT_STATE.md` en main | 24652 |

Desviación declarada (encargo, punto 0): la fila de `docs/validation/HOLDOUT-EXPOSICIONES.md` de
los `make check` del día entra en el commit de apertura, así que `git diff main --stat` de la
apertura trae un fichero más de los cinco que nombra la verificación de `abrir-rama`.

## Estado

EN CURSO.
