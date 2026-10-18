# PLATAFORMA-ADELANTADA · La capa de MT5 que no decide operaciones, adelantada antes de F26 (ADR-0082), y PROJECT_STATE adelgazado

Rama `trabajo/plataforma-adelantada`, abierta el 2026-10-18 desde `main` en 8642b8c (commit de
estado sobre el merge 7d3783d, tag `stable/F37t-visor-construccion`). Encargo:
`docs/encargos/trabajo-plataforma-adelantada.md`. Tramo: R0 («Lo que ordena el trabajo»; la rama
reordena la hoja de ruta y el tramo R6a aun no existe al abrirla). Modelo de la sesion: Opus,
esfuerzo medio, fijados por Aleks en su terminal antes del encargo.

```ids-inexistentes
ADR-0082 — el ADR que esta rama escribe en su fase 1; aún no existe
```

## Apertura: la base, comprobada con git

- `git rev-parse main origin/main`: `8642b8c2affe157e82ba9d73815fe7f1a62eaf32` las dos veces.
- `git rev-parse main^1` y `git rev-parse "stable/F37t-visor-construccion^{commit}"`:
  `7d3783dbc5e562fc97ad39a84532454fea9132b5` las dos; el tag esta en origin
  (`git ls-remote --tags origin stable/F37t-visor-construccion`: `2fe6cfd...`, el objeto del tag
  anotado). Es el ultimo `- Tag: ` de `docs/state/HISTORIA.md`.
- CI de `main` sobre 8642b8c2affe157e82ba9d73815fe7f1a62eaf32 (API de check-runs, sha literal):
  `python` · `completed` · `success`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.

## Estado

EN CURSO.
