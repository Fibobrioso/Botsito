# RENOVAR-CIERRES-2025 · El calendario de cierres de EURUSD del perfil FTMO 2-Step Swing 100k, renovado hacia atrás hasta cubrir 2025 (R5.4 y R5.6, letra I)

> PLANTILLA: informe de la rama `trabajo/renovar-cierres-2026-11-26`. Estado: EN CURSO (apertura). La
> fase 0, las Trading Updates leídas, los cierres que entran y los que no, las desviaciones, las
> comprobaciones, las líneas del cierre y el informe del revisor se escriben aquí según avanza la rama.

Rama `trabajo/renovar-cierres-2026-11-26`, abierta el 2026-11-26 desde `main` en 93a4fc29 (commit de
estado sobre el merge 4581f529 del tag `stable/F39q-f17-ordenes`). Encargo:
`docs/encargos/trabajo-renovar-cierres-2026-11-26.md`. Tramo: R5 (R5.4 y R5.6 de
`docs/plan/HOJA-DE-RUTA.md`; la letra I de la Next Action). Tag previsto:
`stable/F39r-renovar-cierres-2026-11-26`.

## Base comprobada (abrir-rama, paso 1)

- `git fetch origin`; `git status --short` vacío; `git rev-parse main origin/main`:
  `93a4fc2991b8a912b51072de7b8593cf0974883f` dos veces.
- `git rev-parse "stable/F39q-f17-ordenes^{commit}"` = `git rev-parse main^1` =
  `4581f529f2b5e7d3ff05d189fd2907746547a842`; en origin, `4ca20840…` (el objeto del tag anotado) y
  `4581f529…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 21967) y el último `stable/*`
  (`git tag --sort=-creatordate`: F39q, F39p, F39o).
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal
  `93a4fc2991b8a912b51072de7b8593cf0974883f` da el check `python` en `completed` / `success`, run
  **45922991122** (job 140257827342): confirma el número que vio el consultor.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.
