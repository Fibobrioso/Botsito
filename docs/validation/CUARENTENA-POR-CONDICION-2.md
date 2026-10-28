# CUARENTENA-POR-CONDICION-2 · Diciembre, la coma y el punto, y el barrido ancho en la skill (G.5)

Rama `trabajo/cuarentena-por-condicion-2`, abierta el 2026-10-28 desde `main` en 0fa9c81 (commit de
estado sobre el merge faf5ce2, tag `stable/F38g-recorrida-construccion`). Encargo:
`docs/encargos/trabajo-cuarentena-por-condicion-2.md`. Tramo: «Carril: guardias y deuda» (G.5 de
`docs/plan/HOJA-DE-RUTA.md`; F de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 0fa9c81; `git rev-parse main origin/main` da dos veces
  0fa9c81b5b26d47f884860ff4530eb0a37eb6b02; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38g-recorrida-construccion`;
  `git rev-parse "stable/F38g-recorrida-construccion^{commit}"` = `git rev-parse main^1` =
  faf5ce20a4dbcec47b7b18dbc4ff41420946e23b; `git ls-remote --tags origin stable/F38g-recorrida-construccion`
  devuelve el tag (6af57ae3…).
- La CI de `main` sobre 0fa9c81b5b26d47f884860ff4530eb0a37eb6b02, por la API de check-runs con el
  sha literal (`gh api repos/{owner}/{repo}/commits/<sha>/check-runs`): un check `python`,
  `completed` / `success`, run 40633309578 (el que cita el cierre).
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío, y
  `git ls-remote --heads origin` solo da `main`.

## Estado

EN CURSO.
