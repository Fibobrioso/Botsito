# GUARDIA-CI · la guardia niega esperar a la CI con una consulta repetida

Rama: `trabajo/guardia-ci`, abierta el 2026-10-23 desde `main` en `2a99e64` (commit de estado
sobre el merge `975c086`, tag `stable/F38a-guardia-ffmpeg`). Encargo:
`docs/encargos/trabajo-guardia-ci.md`. Carril de guardias y deuda; paga la línea de Technical Debt
de `PROJECT_STATE.md` «La guardia no niega un guion que espera a la CI en bucle» (la deuda vive
solo en Technical Debt, no en G.1 de la hoja de ruta, y el cierre no añade nada a G.1). Tag de
cierre previsto: `stable/F38b-guardia-ci`.

## Base comprobada al abrir

- `git fetch origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `2a99e64fa00d1ff4b0c45ee659614f1a21e2d110` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38a-guardia-ffmpeg^{commit}"` =
  `975c0863c1efbb567db7e9086590e7b67efec15e`; el tag está en origin
  (`git ls-remote --tags origin stable/F38a-guardia-ffmpeg`:
  `171d0d9e478e2addfa2212f817ff697e41910edf refs/tags/stable/F38a-guardia-ffmpeg`, el objeto del
  tag anotado).
- CI de `main` sobre su HEAD, por la API de check-runs con el sha de 40 caracteres escrito tal
  cual: job `python`, `completed` / `success`, run 39893825671.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.
- La línea de Technical Debt sigue abierta: `PROJECT_STATE.md:104`.

## Estado

EN CURSO: rama abierta; falta la fase 0.
