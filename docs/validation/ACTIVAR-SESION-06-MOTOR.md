# ACTIVAR-SESION-06-MOTOR · El motor de la activación de la sesión 6 (R4.2, entrada F)

Rama `trabajo/activar-sesion-06-motor`, abierta el 2026-11-05 desde `main` en 04ec025 (commit de
estado sobre el merge df0e672 del tag `stable/F38n-activar-sesion-06`). Encargo:
`docs/encargos/trabajo-activar-sesion-06-motor.md`.

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `04ec0251ba6d80e713535bc2fdbabee8511db3a8` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F38n-activar-sesion-06^{commit}"` = `df0e6721dc72fea62990163e1ec7a94ad5a4c127` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F38n-activar-sesion-06` da `eec74e4a…` (el objeto del tag anotado).
- CI de `main`: `gh run view 42147004153` → `status: completed`, `conclusion: success`, `headSha: 04ec0251ba6d80e713535bc2fdbabee8511db3a8`, `headBranch: main`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Estado

EN CURSO: fase 0.
