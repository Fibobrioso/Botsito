# scripts/git-hooks/
Hooks de git versionados. `make sync` (o `make hooks`) los COPIA a `.git/hooks/`.

Por que copiar y no `core.hooksPath`: con una ruta relativa, git busca el hook en la rama actual; si la
rama no contiene el fichero (por ejemplo `main` antes de integrar F01), git lo omite en silencio y el
commit pasa. Se comprobo en una prueba cruzada el 2026-09-04. Tras cambiar el hook hay que volver a
ejecutar `make hooks`.

- `pre-commit`: rechaza commits directos en `main` (salvo `BOTSITO_ALLOW_MAIN=1`, que solo usa el
  ritual de merge); rechaza modificar, renombrar o borrar `*.yaml` bajo `knowledge/evidence/`,
  `knowledge/feedback/`, `data/manifests/` (F15) y `knowledge/corpus/transcripciones/` (F04)
  (salvo `_*.yaml` generados), con rutas sin entrecomillar (`core.quotepath=false`) para que un
  nombre con acento o espacio no se cuele; exige `uv.lock` al dia (`uv lock --check`) y comprueba
  los contratos de importacion con `uv run --no-sync lint-imports` (sin tocar el entorno: un
  proceso largo, como una transcripcion en la GPU, puede tener abierto el ejecutable).

La copia la hace `scripts/instalar_hooks.py` (Python, no `cp`/`chmod`): el `make` de Windows
ejecuta las recetas con `cmd.exe` desde PowerShell.

Los hooks son una comodidad local, no una garantia: se saltan con `--no-verify`. La garantia son los
tests en CI (`tests/contract/`), que comprueban el indice y, desde F06/F09, el historial de git.
