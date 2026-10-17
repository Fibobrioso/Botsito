# SESGO-H4-COLOR · La regla del sesgo de H4 que el trader respondió por WhatsApp (R1.2)

Rama `trabajo/sesgo-h4-color`, abierta el 2026-10-17 desde `main` en 59c8ae7 (commit de estado
sobre el merge fa15a84, tag `stable/F37q-corrida-construccion`). Encargo:
`docs/encargos/trabajo-sesgo-h4-color.md`. Tramo: R1 (R1.2 de `docs/plan/HOJA-DE-RUTA.md`; W de la
Next Action). Modelo de la sesión: Fable 5.1, esfuerzo alto (`/model`, comprobado al abrir).

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git fetch origin` y `git status --short` vacío; `git rev-parse HEAD main origin/main` → tres
  veces `59c8ae72fc959d81753d22e6fc140ea75ea42bda`.
- El último tag de los registros de cierre de `docs/state/HISTORIA.md` es
  `stable/F37q-corrida-construccion`; `git rev-parse "stable/F37q-corrida-construccion^{commit}"` y
  `git rev-parse main^1` dan los dos `fa15a84405c5d371d2906833616278ad2e25c926`, y
  `git ls-remote --tags origin stable/F37q-corrida-construccion` lo trae
  (`579bff95968cb0060cd3c02a02c1d838173a0a0c refs/tags/stable/F37q-corrida-construccion`).
- La CI de `main` sobre su HEAD, consultada con `gh run view 38656985715` (como pide el encargo:
  ni curl ni guion): `status completed`, `conclusion success`, `headSha 59c8ae72…42bda`,
  `headBranch main`, `event push`, `workflowName ci`, creada el 2026-10-14T23:55:19Z.
- Ninguna otra rama: `git branch --list` da solo `main`; `git ls-remote --heads origin "fix/*"`
  vacío; `git ls-remote --heads origin` solo `refs/heads/main`.

Hecho al abrir: `docs/encargos/trabajo-sesgo-h4-color.md` (el encargo tal cual), `contrato.yaml`
(riesgo alto, tramo R1) y el Archivo 34 de `PROJECT_STATE.md` al final de `docs/state/HISTORIA.md`.

## Estado

EN CURSO. Fase 0 pendiente (skill `fase-cero`, con el agente `auditor-encargo`), con PARADA antes
de escribir código.
