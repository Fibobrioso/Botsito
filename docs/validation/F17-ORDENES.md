# F17-ORDENES · La medida de las órdenes stop y el grabador de ticks de la demo de FTMO, con sus herramientas y sin correr (R4.7, entrada F)

> PLANTILLA: informe de la rama `trabajo/f17-ordenes`. Estado: EN CURSO (apertura). La fase 0 y su
> PARADA, lo hecho tras la respuesta, el encargo punto por punto, las desviaciones, las líneas del
> cierre, la fila de ERRORES y el informe del revisor se escriben aquí según avanza la rama.

Rama `trabajo/f17-ordenes`, abierta el 2026-11-26 desde `main` en e8c20a80 (commit de estado sobre
el merge 8066b377 del tag `stable/F39p-f17-historial`). Encargo:
`docs/encargos/trabajo-f17-ordenes.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la A.5 se
cita en el informe; la F de la Next Action). Tag previsto: `stable/F39q-f17-ordenes`.

## Base comprobada (abrir-rama, paso 1)

- `git fetch origin`; `git status --short` vacío; `git rev-parse main origin/main`:
  `e8c20a808e60b7cffe333a60f2c3fbdc53712086` dos veces.
- `git rev-parse "stable/F39p-f17-historial^{commit}"` = `git rev-parse main^1` =
  `8066b377a4534348529c90fe89974a208409f19d`; en origin, `83a4e4d2…` (el objeto del tag anotado) y
  `8066b377…` (`^{}`). Es el último `- Tag: ` de HISTORIA y el último `stable/*` de origin
  (`git ls-remote --tags origin "refs/tags/stable/*"`, ordenado: F39n, F39o, F39p al final).
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal da el check `python` en
  `completed` / `success`, del run 45864298815 (el que cita el encargo).
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*" "trabajo/*"
  "feature/*"` sale vacío.

## Estado

EN CURSO: la rama abierta; la fase 0 viene en su commit.
