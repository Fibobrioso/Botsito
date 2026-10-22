# GUARDIA-FFMPEG · ffprobe y ffmpeg sobre un vídeo que no se protege, por lista cerrada

Rama: `trabajo/guardia-ffmpeg`, abierta el 2026-10-22 desde `main` en `8cfed04` (commit de estado
sobre el merge `e044b15`, tag `stable/F37z-hoja-sesion-05`). Encargo:
`docs/encargos/trabajo-guardia-ffmpeg.md`. NA:K (la parte de ffprobe y ffmpeg), hoja de ruta G.1,
carril de guardias y deuda.

## Base comprobada al abrir

- `git fetch --prune origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `8cfed041c59cb3db319346cc19330fff6ad96175` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F37z-hoja-sesion-05^{commit}"` =
  `e044b15dbafd3fa61923e8009acd0f1dbd1d9285`; el tag está en origin (`git ls-remote --tags`:
  `49d58cf… refs/tags/stable/F37z-hoja-sesion-05`), y es el último `- Tag:` de `docs/state/HISTORIA.md`.
- CI de `main` sobre `8cfed041c59cb3db319346cc19330fff6ad96175` (check-runs): `python completed
  success`, run 39806538052.
- Ninguna otra rama: `git branch --list -a` da solo `main` y `origin/main`; `git ls-remote --heads
  origin` da solo `refs/heads/main`.

## Estado

EN CURSO.
