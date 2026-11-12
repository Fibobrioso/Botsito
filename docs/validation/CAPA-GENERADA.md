# CAPA-GENERADA · lo que la capa de MT5 recibe del repo, generado y con su hash

Rama `trabajo/capa-generada` (hoja de ruta R6a.2, tramo R6a; ADR-0082 D5). Encargo del consultor
del 2026-11-12: `docs/encargos/trabajo-capa-generada.md`.

## Apertura (2026-11-12)

Base comprobada con git y gh antes de abrir:

- `git rev-parse main origin/main`: `893ce6f57bc40f644415785063d6b27eb9ef8977` las dos veces
  (`git rev-parse --short main` = `893ce6f5`, el sha del encargo).
- `git rev-parse "stable/F38y-laminas-motivos^{commit}"` = `git rev-parse main^1` =
  `7d3002c87026573e5c24aada940e490be5907da1`; el tag esta en origin (`git ls-remote --tags`:
  `bd7686fc… refs/tags/stable/F38y-laminas-motivos`).
- CI de `main` sobre `893ce6f5…` (check-runs): `python completed success`, run 43217308040.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.
- `PROJECT_STATE.md` en main: 23.899 bytes.

Exposición: cada `make check` lee el M1 entero de marzo y calienta con el de junio (Technical Debt).
El primer `make check` de la apertura se lanzó sin la fila del día y se paró a medias para
escribirla; `docs/validation/HOLDOUT-EXPOSICIONES.md` entra en `rutas_permitidas` (lo señaló el
auditor del encargo, herencia 1) y la fila del 2026-11-12 de esta rama declara las dos lecturas.

## Fase 0

Pendiente.

## Estado

EN CURSO (abierta; fase 0 por hacer).
