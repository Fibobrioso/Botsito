# F17-HISTORIAL · El historial de ticks del servidor de la demo de FTMO, con sus herramientas y sin correr, y el ajuste por cuenta de F17 (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/f17-historial`, abierta el 2026-11-25 desde `main` en 2dc4f7dd (commit de estado
sobre el merge 96b250fd del tag `stable/F39o-contraste-trader`). Encargo:
`docs/encargos/trabajo-f17-historial.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la A.5 se
cita en el informe; la F de la Next Action). Tag previsto: `stable/F39p-f17-historial` (no existe ni
en local ni en origin: `git tag -l "stable/F39p*"` y `git ls-remote --tags origin "stable/F39p*"`,
0 líneas).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main` (tras `git fetch origin`):
  `2dc4f7dd55b9c8bcffe7902486851c73ef81ea19` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39o-contraste-trader^{commit}"` = `git rev-parse main^1` =
  `96b250fd15297b443ec3d5e51771b84669ced7b0`; en origin, `98d6df47…` (el objeto del tag anotado) y
  `96b250fd…` (`^{}`). Es el último `- Tag: ` de HISTORIA y el último `stable/*` de origin.
- CI de `main` sobre su HEAD: la API de check-runs con el sha literal da el check `python`
  (139666601005) en `completed` / `success`; es el run 45747377112 del cierre de F39o.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`, y
  `git ls-remote --heads origin "fix/*"` sale vacío.
- Sesión en Opus 5.5, esfuerzo alto (`/model` y `/effort`).

## Estado

EN CURSO: apertura.
