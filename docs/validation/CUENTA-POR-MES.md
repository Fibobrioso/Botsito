# CUENTA-POR-MES · la cuenta del motor, una por mes (ADR-0092 §8)

Rama `trabajo/cuenta-por-mes`, abierta el 2026-11-07 desde `main` 8aeed0b
(tag `stable/F38r-metodo-fidelidad-rentabilidad`, merge a1907fa). Encargo:
`docs/encargos/trabajo-cuenta-por-mes.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.8 de la hoja de ruta; F de la Next Action).

## 0. La base, comprobada con git al abrir

- `git rev-parse HEAD` en main = `8aeed0b336c0e80ab1d7124096f04880e569ede7`; `origin/main` el mismo
  (`git fetch origin --prune`; `git ls-remote --heads origin` solo da `refs/heads/main`).
- `git rev-parse "stable/F38r-metodo-fidelidad-rentabilidad^{commit}"` =
  `a1907fa3d0dead56bc109cea6f680841c8e629cc` = `git rev-parse main^1`; el tag esta en origin
  (`git ls-remote --tags origin`, objeto 4323f6b).
- `gh run view 42440794180 --json headSha,conclusion,status,workflowName,headBranch`:
  `{"conclusion":"success","headBranch":"main","headSha":"8aeed0b336c0e80ab1d7124096f04880e569ede7","status":"completed","workflowName":"ci"}`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin "fix/*"` vacio.
- Modelo: Opus 5.5, el que pide el encargo.

## Estado

EN CURSO.
