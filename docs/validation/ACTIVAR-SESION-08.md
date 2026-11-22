# ACTIVAR-SESION-08 · La sesión 7b entra en la spec y en el motor, la respuesta de FTMO del 2026-11-20 y la auditoría del 2026-11-21 (R4.3, entrada F)

> PLANTILLA hasta la fase 0: la tabla de activación la escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/activar-sesion-08`, abierta el 2026-11-21 desde `main` en 00e6dc8b (commit de estado
sobre el merge f4b5a9a2 del tag `stable/F39j-sesion-08`). Encargo:
`docs/encargos/trabajo-activar-sesion-08.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
paso (2) de la F de la Next Action). Tag previsto: `stable/F39k-activar-sesion-08` (no existe ni en
local ni en origin: `git tag -l 'stable/F39k*'` y `git ls-remote --tags origin 'stable/F39k*'` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `00e6dc8b73c5f19ee228c4a642f6b5e0c78a9b84` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39j-sesion-08^{commit}"` = `f4b5a9a270cebb1de81a9d89cb659fbc26e9e713` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39j-sesion-08` da `ff8f7281…` (el objeto del tag anotado).
- CI de `main`: `gh run view 44978301993` (suelto, sin guion) → `status: completed`, `conclusion: success`, `headSha: 00e6dc8b73c5f19ee228c4a642f6b5e0c78a9b84`, rama `main`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Desviaciones de la apertura

- **La auditoría no estaba en el Escritorio al empezar.** `ls` no la encontró al comprobar la base;
  Aleks la dejó a mitad de la apertura (`C:\Users\USER\Desktop\AUDITORIA-2026-11-21.md`, 377 saltos
  de línea según `wc -l`). Entra en su commit propio, el primero tras la apertura (F7.1).
- **La orden `--comprobar` del contrato.** El encargo no da la orden y el contrato de la 7a nombraba
  `scripts/generar_capa.py`, que no existe; el contrato lleva la que documenta el propio guion
  (`src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k --comprobar`).

## Estado

EN CURSO: fase 0.
