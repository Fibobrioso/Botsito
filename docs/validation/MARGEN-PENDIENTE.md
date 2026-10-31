# MARGEN-PENDIENTE · el script 1.2 de MedirDemoFTMO (paso 8, el margen de una pendiente stop) y PROJECT_STATE adelgazado

Rama `trabajo/margen-pendiente`, abierta el 2026-10-31 desde `main` 6948375 (commit de estado sobre
el merge 4b12a92, tag `stable/F38j-respaldo-m1`). Encargo: `docs/encargos/trabajo-margen-pendiente.md`.
Tramo «Carril: lo de Aleks» de `docs/plan/HOJA-DE-RUTA.md` (entrada A de la Next Action, A.1).

## Apertura: la base, comprobada con git

| Comprobación | Salida |
|---|---|
| `git rev-parse main origin/main main^1` | 6948375f9faf514e0b719495af9a46ccd3193320 (dos veces) y 4b12a9209dc23de9e988cd40058ab9ef80623032 |
| `git rev-parse "stable/F38j-respaldo-m1^{commit}"` | 4b12a9209dc23de9e988cd40058ab9ef80623032 = `main^1`; en origin (`git ls-remote --tags origin stable/F38j-respaldo-m1`: 25c6cc7d…, el objeto del tag anotado) |
| último `- Tag: ` de HISTORIA | `stable/F38j-respaldo-m1` (HISTORIA.md:14001) |
| `gh run view 40943847054 --json status,conclusion,headSha,headBranch,workflowName` | `{"conclusion":"success","headBranch":"main","headSha":"6948375f9faf514e0b719495af9a46ccd3193320","status":"completed","workflowName":"ci"}` |
| `git branch --list` / `git ls-remote --heads origin "fix/*"` | solo `main`; ningún `fix/*` en origin |
| `git worktree list` | el worktree `wt-ci` (e7df30b, detached) sigue, en la carpeta de otra sesión: no se toca |

## Estado

EN CURSO: rama abierta; la fase 0 va en su propio commit.
