# PREREGISTRO-INVENTARIO · Lo que hace falta para rellenar PREREGISTRO.md (R5.1, entrada G) · primer tiempo: fase 0

> PLANTILLA hasta la fase 0 (la línea con que nació): EN CURSO.

Rama `trabajo/preregistro`, abierta el 2026-11-19 desde `main` en e490fe33 (commit de estado sobre
el merge 50f6a6fc del tag `stable/F39f-laminas-sesion-7b`). Encargo:
`docs/encargos/trabajo-preregistro.md`. Tramo: R5 (R5.1 de `docs/plan/HOJA-DE-RUTA.md`; la G de la
Next Action). Tag previsto: `stable/F39g-preregistro` (no existe ni en local ni en origin:
`git tag -l 'stable/F39g*'` y `git ls-remote --tags origin 'stable/F39g*'` vacíos). Riesgo: **alto**,
como manda el encargo (toca la puerta del holdout).

## La base, comprobada al abrir (skill `abrir-rama`, paso 1)

- `git rev-parse --short main` = `e490fe33`, y `git rev-parse main origin/main` da dos veces
  `e490fe3361701bb30f1d5708674d1acf0678d813`.
- `git rev-parse "stable/F39f-laminas-sesion-7b^{commit}"` = `50f6a6fc9293bdb5f9b72a54a9d394e10289b89f`
  = `git rev-parse main^1`; el tag está en origin (`git ls-remote --tags origin` lo da).
- CI de `main` sobre e490fe33: run **44576448998**, `completed` / `success`
  (`gh run view 44576448998 --json headSha,status,conclusion`: `headSha` =
  `e490fe3361701bb30f1d5708674d1acf0678d813`).
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## Estado

EN CURSO: fase 0.
