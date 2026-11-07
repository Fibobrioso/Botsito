# METODO-FIDELIDAD-RENTABILIDAD · el método con el que se juzga al bot (ADR-0092)

```ids-inexistentes
ADR-0092 — lo crea la fase 1 de esta rama; el bloque sale en el mismo commit que lo crea
```

Rama `trabajo/metodo-fidelidad-rentabilidad`, abierta el 2026-11-07 desde `main` e01e28c
(tag `stable/F38q-sello-respaldo-m1`, merge 18f548e). Encargo:
`docs/encargos/trabajo-metodo-fidelidad-rentabilidad.md`. Tramo «R3 · Una corrida del arnés sobre
toda la construcción» (R3.7 de la hoja de ruta; R de la Next Action).

## 0. La base, comprobada con git al abrir

- `git rev-parse HEAD` en main = `e01e28cb72bf3a9c16c5cb975fa4cda27895e627`; `origin/main` el mismo
  (`git fetch origin --prune`; `git ls-remote --heads origin` solo da `refs/heads/main`).
- `git rev-parse "stable/F38q-sello-respaldo-m1^{commit}"` = `18f548e11447455f0bed34bea4e9d022752416e1`
  = `git rev-parse main^1`; el tag esta en origin (`git ls-remote --tags origin`, objeto 12703cc).
- `gh run view 42400168427 --json headSha,status,conclusion,headBranch,name`:
  `{"conclusion":"success","headBranch":"main","headSha":"e01e28cb72bf3a9c16c5cb975fa4cda27895e627","name":"ci","status":"completed"}`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin "fix/*"` vacio.
- `grep 0092` en `docs/` y en `PROJECT_STATE.md`: ningun ADR-0092 (solo trozos de shas y de offsets).

## Estado

EN CURSO: rama abierta; la fase 0 la escribe su commit.
