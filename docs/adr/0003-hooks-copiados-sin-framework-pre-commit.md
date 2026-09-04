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

## Fecha / fase
2026-09-04 · F02

## Estado
ACTIVE
