# MARGEN-LOTE · Qué hace el bot cuando el lote del 0,5 % no cabe en el margen o en el volumen (R3.3)

Rama `trabajo/margen-lote`, abierta el 2026-10-17 desde `main` en 9cf711e (commit de estado sobre
el merge 5296a31, tag `stable/F37r-sesgo-h4-color`). Encargo: `docs/encargos/trabajo-margen-lote.md`
(va fechado el 2026-10-18; el reloj de la máquina al abrir daba el 2026-10-17 a las 20:39, y las
fechas de este informe y de HOLDOUT-EXPOSICIONES son las reales).
Tramo: R3 (R3.3 de `docs/plan/HOJA-DE-RUTA.md`; E de la Next Action; heredado 37). Modelo de la
sesión: `claude-fable-5-1` según el entorno de la sesión; el esfuerzo lo fija `/model` en el
terminal de Aleks y la sesión no puede leerlo desde dentro.

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git fetch origin` y `git status --short` vacío; `git rev-parse --short main` → `9cf711e`;
  `git rev-parse main origin/main` → dos veces `9cf711ee36cd4a08de4d2ab7230ee9153eddd3d1`.
- El último tag de los registros de cierre de `docs/state/HISTORIA.md` es
  `stable/F37r-sesgo-h4-color`; `git rev-parse "stable/F37r-sesgo-h4-color^{commit}"` y
  `git rev-parse main^1` dan los dos `5296a31329af369e40cb23273c6cce91e2e0ae0e`, y
  `git ls-remote --tags origin stable/F37r-sesgo-h4-color` lo trae
  (`020d917c4e84e2738cb81194d95fac885b121940 refs/tags/stable/F37r-sesgo-h4-color`).
- La CI de `main` sobre su HEAD, consultada con `gh run view 39083113877` (como pide el encargo:
  ni curl ni guion): `status completed`, `conclusion success`, `headSha 9cf711ee…dd3d1`,
  `headBranch main`, workflow `ci`.
- Ninguna otra rama: `git branch --list` da solo `main`; `git ls-remote --heads origin "fix/*"`
  sale vacío.

## Estado

EN CURSO. Rama abierta; la fase 0 (inventario y PARADA) viene en el commit siguiente.
