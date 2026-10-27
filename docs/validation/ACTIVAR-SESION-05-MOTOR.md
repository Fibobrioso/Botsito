# ACTIVAR-SESION-05-MOTOR · Lo que la sesión 5 pide al motor (R4.1, entrada V)

Rama `trabajo/activar-sesion-05-motor`, abierta el 2026-10-26 desde `main` en 32904ee (commit de
estado sobre el merge 2c26fb2, tag `stable/F38e-activar-sesion-05`). Encargo:
`docs/encargos/trabajo-activar-sesion-05-motor.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`,
lo que queda; V de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 32904ee; `git rev-parse main origin/main` da dos veces
  32904ee0f0d2ebba44abef1c5183655b633fb5e7; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38e-activar-sesion-05`;
  `git rev-parse "stable/F38e-activar-sesion-05^{commit}"` = `git rev-parse main^1` =
  2c26fb215305ff6d50e0ad7d7d437025056d40b1; `git ls-remote --tags origin stable/F38e-activar-sesion-05`
  devuelve el tag.
- La CI de `main` sobre 32904ee0f0d2ebba44abef1c5183655b633fb5e7: `gh run view 40421174533`
  suelto, `completed` / `success`, `headBranch` main, `headSha` el mismo.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

Con la apertura entra la fila del 2026-10-26 de `docs/validation/HOLDOUT-EXPOSICIONES.md` con la
exposición del auditor del consultor (el `grep -rln` sobre la raíz de un clon de solo lectura), que
el encargo manda declarar en el primer commit.

## Estado

EN CURSO. Abierta; la fase 0 viene en su commit.
