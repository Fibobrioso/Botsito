# CONTRASTE-TRADER · El contraste con el trader de ADR-0099 §6 y la petición escrita de los meses del backtest con costes (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/contraste-trader`, abierta el 2026-11-25 desde `main` en 6c113d16 (commit de estado
sobre el merge 42fdb0b5 del tag `stable/F39n-diagnostico-premisa`). Encargo y su añadido (A1-A5):
`docs/encargos/trabajo-contraste-trader.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la F
de la Next Action). Tag previsto: `stable/F39o-contraste-trader` (no existe ni en local ni en
origin: `git tag -l "stable/F39o*"` y `git ls-remote --tags origin "stable/F39o*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main` (tras `git fetch origin`):
  `6c113d161eb7e83bb185306b57a3bb6fa078eeaf` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39n-diagnostico-premisa^{commit}"` =
  `42fdb0b59c9fa2ea29c35c2551c43c8c1494452b` = `git rev-parse main^1` (el merge); en origin,
  `git ls-remote --tags origin "stable/F39n*"` da `518bbbe6…` (el objeto del tag anotado) y
  `42fdb0b5…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 21209) y el último `stable/*` de
  origin.
- CI de `main` sobre su HEAD: `gh run list --branch main --limit 2` → 45670800735, `6c113d16`,
  `completed`, `success`; la API de check-runs con el sha literal da el check `python`
  (139405198029) en `completed` / `success`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`, y
  `git ls-remote --heads origin "fix/*"` sale vacío.
- Sesión en Opus 5.5, esfuerzo alto (`/model` al empezar);
  `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`).

## Estado

EN CURSO: apertura.
