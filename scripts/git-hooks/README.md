# scripts/git-hooks/
Hooks de git versionados. `make sync` (o `make hooks`) los COPIA a `.git/hooks/`.

Por que copiar y no `core.hooksPath`: con una ruta relativa, git busca el hook en la rama actual; si la
rama no contiene el fichero (por ejemplo `main` antes de integrar F01), git lo omite en silencio y el
commit pasa. Se comprobo en una prueba cruzada el 2026-09-04. Tras cambiar el hook hay que volver a
ejecutar `make hooks`.

- `pre-commit`: rechaza commits directos en `main` (salvo `BOTSITO_ALLOW_MAIN=1`, que solo usa el
  ritual de merge) y comprueba los contratos de importacion si hay `pyproject.toml`.

Los hooks son una comodidad local, no una garantia: se saltan con `--no-verify`. La garantia son los
tests en CI (`tests/contract/`), que comprueban el indice y, desde F06/F09, el historial de git.
