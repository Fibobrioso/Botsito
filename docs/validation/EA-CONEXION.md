# EA-CONEXION · el primer EA de la capa de MT5 que no decide operaciones (R6a.1)

Rama `trabajo/ea-conexion`, tramo R6a de `docs/plan/HOJA-DE-RUTA.md` (R6a.1; ADR-0082). Encargo del
consultor del 2026-10-19, copiado tal cual en `docs/encargos/trabajo-ea-conexion.md`.

## Apertura

Base comprobada el 2026-10-19 (skill `abrir-rama`, paso 1), con git y con `gh`:

- `git rev-parse main origin/main` → `9c456292e9eb656ef523a89e9f5d5893482b4979` las dos veces.
- `git rev-parse "stable/F37w-barrido-sesion-5^{commit}"` → `ff55b3d3e313aae4fd0069ca0fee2431faf7b4a0`
  = `main^1` (el merge); el tag esta en origin (`git ls-remote --tags origin`).
- CI de `main` sobre su HEAD, con `gh run list --branch main --commit 9c456292e9eb656ef523a89e9f5d5893482b4979`:
  run 39314463754, `completed` / `success` (ni curl ni guion, por orden del consultor).
- `git branch --list` → solo `main`; `git ls-remote --heads origin` de `fix/*`, `trabajo/*` y
  `feature/*` → vacio.

## Estado

EN CURSO: rama abierta; la fase 0 va en su commit.
