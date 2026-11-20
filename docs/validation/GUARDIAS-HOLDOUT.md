# GUARDIAS-HOLDOUT · La fila del día en el sello (G2), dos huecos de test_hoja_de_ruta (H) y el estudio de G1

> PLANTILLA hasta la fase 0 (la línea con que nació): EN CURSO.

Rama `trabajo/guardias-holdout`, abierta el 2026-11-19 (21:07, reloj de la laptop en Lima, UTC-5)
desde `main` en fa592071 (commit de estado sobre el merge 2fc884ac del tag
`stable/F39g-preregistro`). Encargo: `docs/encargos/trabajo-guardias-holdout.md`. Tramo: «Carril:
guardias y deuda». Tag previsto: `stable/F39h-guardias-holdout` (no existe en origin:
`git ls-remote --tags origin "stable/F39h*"` vacío). Riesgo: **alto**, como manda el encargo.

## Apertura: la base comprobada

- `git rev-parse --short main` = `fa592071`; `git rev-parse main origin/main` da dos veces
  `fa592071fe071e12893709f28076062802312c76`.
- Último tag de HISTORIA: `stable/F39g-preregistro`; `git rev-parse "stable/F39g-preregistro^{commit}"`
  = `2fc884ac7b337d9d4ce8ced311f6acdb8cfd7125` = `git rev-parse main^1`; está en origin
  (`git ls-remote --tags origin stable/F39g-preregistro` no sale vacío).
- CI de `main` sobre fa592071: `gh run view 44653987599` → `{"conclusion":"success","headBranch":"main","headSha":"fa592071fe071e12893709f28076062802312c76","status":"completed","workflowName":"ci"}`.
  Es el run que el encargo nombraba, y está verde.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Estado

EN CURSO.
