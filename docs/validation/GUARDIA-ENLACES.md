# GUARDIA-ENLACES · La guardia protege el material por lo que es, no solo por donde esta (G.8)

> PLANTILLA hasta la fase 0 (la línea con que nació): la rama acaba de abrirse.

Rama `trabajo/guardia-enlaces`, abierta el 2026-11-20 (18:27, reloj de la laptop en Lima, UTC-5)
desde `main` en 0562a77b (commit de estado sobre el merge fb1f02e9 del tag
`stable/F39h-guardias-holdout`). Encargo: `docs/encargos/trabajo-guardia-enlaces.md`. Tramo:
«Carril: guardias y deuda» (entrada G.8 de la hoja de ruta). Tag previsto:
`stable/F39i-guardia-enlaces`. Riesgo: **alto**, como manda el encargo.

## 0. Apertura: la base comprobada

- `git rev-parse main origin/main`: dos veces `0562a77ba0e58da25904801640c98f4287bd6a95`.
- `git rev-parse "stable/F39h-guardias-holdout^{commit}"` = `fb1f02e9712e63fcb4e75fd53cf3ac5a5eadd9ec`
  = `main^1`; en origin, `git ls-remote --tags origin stable/F39h-guardias-holdout` da
  `5050047e… refs/tags/stable/F39h-guardias-holdout` (tag anotado).
- CI de `main` sobre 0562a77b (check-runs con el sha literal): `python completed success`, run
  44821324976.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"`, vacío.

## Estado

EN CURSO: rama abierta; la fase 0 viene en el commit siguiente.
