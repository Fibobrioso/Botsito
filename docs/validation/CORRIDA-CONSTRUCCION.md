# CORRIDA-CONSTRUCCION · R3.1, la corrida del arnés sobre la construcción vigente y la tabla de diferencias

Rama `trabajo/corrida-construccion`, abierta el 2026-10-14 desde `main` en 23316c8 (commit de
estado sobre el merge 87391b7, tag `stable/F37p-entrada-enero`). Encargo:
`docs/encargos/trabajo-corrida-construccion.md`. Tramo: R3 (R3.1 de `docs/plan/HOJA-DE-RUTA.md`;
F de la Next Action).

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git rev-parse HEAD main origin/main` → tres veces `23316c8484198a7d11185c48c7e3309411e0bad6`;
  `git status --short` vacío.
- Último tag de `docs/state/HISTORIA.md`: `stable/F37p-entrada-enero`;
  `git rev-parse "stable/F37p-entrada-enero^{commit}"` = `git rev-parse main^1` =
  `87391b7afde1b557122b805f26619a90cf5cd3d6`; `git ls-remote --tags origin stable/F37p-entrada-enero`
  → `3a7e46d1… refs/tags/stable/F37p-entrada-enero`.
- CI de `main` sobre `23316c8484198a7d11185c48c7e3309411e0bad6` por la API de check-runs con el sha
  literal: `python  completed  success` (run 38574376055).
- `git branch --list` → solo `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Estado

EN CURSO. Fase 0 (inventario sin tocar nada) pendiente; la escribe la skill `fase-cero` en su
commit.
