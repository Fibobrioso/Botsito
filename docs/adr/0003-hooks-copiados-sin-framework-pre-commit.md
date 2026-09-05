---
status: ACTIVE
date: 2026-09-04
phase: F02
---

# 0003 · Hooks de git copiados desde scripts/git-hooks; sin framework pre-commit

## Decision
Los hooks viven versionados en `scripts/git-hooks/` y `make sync` los copia a `.git/hooks/`.
Se retira `.pre-commit-config.yaml`. La garantia real de cada regla es un test en CI; los hooks
son una comodidad local.

## Problema que resuelve
Tres mecanismos de hooks coexistian (framework pre-commit, `core.hooksPath`, copia manual) y se
pisaban. Ademas, una prueba cruzada demostro que `core.hooksPath` relativo omite el hook en silencio
cuando la rama actual no contiene el fichero.

## Alternativas consideradas
1. Framework pre-commit como unico mecanismo.
2. `core.hooksPath` apuntando a `scripts/git-hooks`.
3. Copia a `.git/hooks` (elegida).

## Por que elegimos esta opcion
No depende de la rama, no requiere instalar nada mas que git y uv, y el fichero fuente sigue
versionado y revisable.

## Por que descartamos las demas
(1) Anade una dependencia y sobrescribe `.git/hooks`; sus hooks no cubren la regla anti-main sin un
hook local igualmente. (2) Falla en silencio al cambiar de rama (verificado el 2026-09-04).

## Impacto
`Makefile` (`hooks`), `scripts/git-hooks/README.md`, eliminacion de `.pre-commit-config.yaml` y
de su entrada en `tests/unit/test_tree.py`.

## Limites (auditoria del 2026-09-04)
- El destino es `git rev-parse --git-path hooks` (en un worktree, `--git-dir/hooks` no se lee).
- Un `core.hooksPath` global o de sistema anula el hook: `instalar_hooks.py` aborta si lo detecta.
- `--no-verify` y reescribir el historial (`reset --soft`) saltan el hook. La garantia real es el
  test de historial en CI; una proteccion de rama en GitHub (sin force-push a `main`) cerraria el
  ultimo hueco y queda como recomendacion al abrir F15.
- Nota (2026-09-05): la proteccion de rama esta activada (Change Log de PROJECT_STATE, 4 sep) y
  el hook usa `uv lock --check` + `uv run --no-sync` para no tocar el entorno dentro de un commit.

## Fecha / fase
2026-09-04 · F02

## Estado
ACTIVE
