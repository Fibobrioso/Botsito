# RESPALDO-M1 · el respaldo M1 no evalúa contra precios anteriores a la decisión (Z, R3.5)

Rama `trabajo/respaldo-m1`, abierta el 2026-10-28 desde `main` 0e021bf (commit de estado sobre el
merge 89dc902, tag `stable/F38i-barrido-sesion-6`). Encargo: `docs/encargos/trabajo-respaldo-m1.md`.
Tramo R3 de `docs/plan/HOJA-DE-RUTA.md`.

## Apertura: la base, comprobada con git

| Comprobación | Salida |
|---|---|
| `git rev-parse main origin/main main^1` | 0e021bf9ca1b108089feda6e6d9f455bcda441be (dos veces) y 89dc9028a912991e47d3ce54cdd3915d2b932606 |
| `git rev-parse "stable/F38i-barrido-sesion-6^{commit}"` | 89dc9028a912991e47d3ce54cdd3915d2b932606 = `main^1`; en origin (`git ls-remote --tags origin stable/F38i-barrido-sesion-6`: e553e2a5…, el objeto del tag anotado) |
| último `- Tag: ` de HISTORIA | `stable/F38i-barrido-sesion-6` |
| `gh run view 40815230287 --json status,conclusion,headSha,headBranch,event` | `{"conclusion":"success","event":"push","headBranch":"main","headSha":"0e021bf9ca1b108089feda6e6d9f455bcda441be","status":"completed"}` |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` (y ningún `fix/*` en origin) |

Tag previsto del cierre: `stable/F38j-respaldo-m1` (el último es F38i).

## Estado

EN CURSO: apertura.
