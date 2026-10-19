# PUNTO-USADO · Qué gasta un punto: la reentrada tras un stop y el rechazo al llenar (R3.4)

Rama `trabajo/punto-usado`, abierta el 2026-10-18 desde `main` en f96b581 (commit de estado sobre
el merge 3ae2933, tag `stable/F37u-plataforma-adelantada`). Encargo:
`docs/encargos/trabajo-punto-usado.md`. Tramo: R3 (R3.4 de `docs/plan/HOJA-DE-RUTA.md`; Y de la
Next Action). Modelo de la sesión: `claude-fable-5-1` según el entorno de la sesión; `/model` en el
terminal de Aleks dio «Fable 5.1 … `high` effort» al empezar.

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones de la skill `abrir-rama`, con su salida:

| Comprobación | Comando | Salida |
|---|---|---|
| `main` es el sha del encargo y es `origin/main` | `git rev-parse --short main`; `git rev-parse main origin/main` | `f96b581`; dos veces `f96b581bfbf93fa3fb6478f3fbc0261dcc0aa37b` |
| El último tag de HISTORIA apunta al merge bajo `main` | `git rev-parse "stable/F37u-plataforma-adelantada^{commit}"`; `git rev-parse main^1` | dos veces `3ae2933817c968de2eea27651416d5fdce6721a8`; `git ls-remote --tags origin stable/F37u-plataforma-adelantada` → `9546e31… refs/tags/stable/F37u-plataforma-adelantada` |
| La CI de `main` sobre su HEAD | `gh run view 39186492700 --json status,conclusion,headSha,headBranch,name` (con `gh`, como pide el encargo; ni curl ni guion) | `{"conclusion":"success","headBranch":"main","headSha":"f96b581bfbf93fa3fb6478f3fbc0261dcc0aa37b","name":"ci","status":"completed"}` |
| Ninguna otra rama | `git branch --list`; `git ls-remote --heads origin "fix/*"` | `* main`; vacío |

`PROJECT_STATE.md` en `main`: 21.911 bytes (`wc -c`), como dice el encargo. `git status --short`
vacío antes de abrir.

## Estado

EN CURSO. Abierta el 2026-10-18; la fase 0 va en el commit siguiente.
