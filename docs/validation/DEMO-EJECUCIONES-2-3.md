# DEMO-EJECUCIONES-2-3 · las ejecuciones 2 y 3 de MedirDemoFTMO, congeladas y decididas

Rama `trabajo/demo-ejecuciones-2-3`, abierta el 2026-11-06 desde `main` (a46eadd, commit de estado
sobre el merge 4fa0920 del tag `stable/F38o-activar-sesion-06-motor`). Encargo:
`docs/encargos/trabajo-demo-ejecuciones-2-3.md`. Tramo «Carril: lo de Aleks».

## Base comprobada al abrir (2026-11-06)

- `git rev-parse main origin/main`: `a46eaddc424d99c9caaf7eba5afd6af052894095` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38o-activar-sesion-06-motor^{commit}"` =
  `4fa09201a352dd46e6b4b78cbfec6ca9220ce6fa`; el tag esta en origin (`git ls-remote --tags`).
- CI de `main` sobre su HEAD: `gh run view 42300034254` → `completed` / `success`, headSha
  `a46eaddc424d99c9caaf7eba5afd6af052894095`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacio.

## Estado

EN CURSO: rama abierta; la fase 0 la escribe la skill fase-cero en su commit.
