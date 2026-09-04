# scripts/git-hooks/
Hooks de git versionados. `make sync` ejecuta `git config core.hooksPath scripts/git-hooks`.

- `pre-commit`: rechaza commits directos en `main` (salvo `BOTSITO_ALLOW_MAIN=1`, que solo usa el
  ritual de merge) y comprueba los contratos de importacion.

Los hooks son una comodidad local, no una garantia: se saltan con `--no-verify`. La garantia son los
tests en CI (`tests/contract/`), que comprueban el indice y, desde F06/F09, el historial de git.
