# RECORRIDA-CONSTRUCCION-3 · La corrida (3): la 7b activada, sobre toda la construcción, el pivote de ADR-0093 §6 y la meta pre-registrada: el techo del trader y el R de las parejas (R4.3, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/recorrida-construccion-3`, abierta el 2026-11-22 desde `main` en 19c171d7 (commit de
estado sobre el merge f04868cc del tag `stable/F39k-activar-sesion-08`). Encargo:
`docs/encargos/trabajo-recorrida-construccion-3.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`;
el paso (3) de la F de la Next Action), más la medida de la meta (el ADR que pre-registra la fase P). Tag previsto:
`stable/F39l-recorrida-construccion-3` (no existe ni en local ni en origin: `git tag --list
"stable/F39l*"` y `git ls-remote --tags origin "stable/F39l*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `19c171d7af422bdcf5e75f1fc1cd3caa2ced0c70` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39k-activar-sesion-08^{commit}"` = `f04868ccb5fe23b80b21312d4519fa8742ecc3e8` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39k-activar-sesion-08` da `1d2fc835…` (el objeto del tag anotado).
- CI de `main`: `gh run view 45051429307` (suelto, sin guion) → `workflowName: ci`, `status: completed`, `conclusion: success`, `headSha: 19c171d7af422bdcf5e75f1fc1cd3caa2ced0c70` (2026-11-22T17:47:43Z). Es el run que dio el informe de cierre.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`.
- Sesión en Opus 5.5, esfuerzo alto; `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir en segundo plano.

## Desviaciones de la apertura

- **`META-TECHO-PAREJAS.yaml` no estaba en el Escritorio al empezar.** `ls` encontró solo
  el borrador del ADR de la meta; se le pidió a Aleks antes de abrir, sin reconstruirlo, y lo dejó. Los dos
  ficheros se leyeron enteros antes de abrir: ninguna fecha de día reservado ni ningún resultado.
- **La fila de HOLDOUT-EXPOSICIONES del día** se escribió y estadió (14:32, hora local) tras crear la
  rama y antes de cualquier otra escritura, lectura de material o `make check`.

## Estado

EN CURSO: apertura.
