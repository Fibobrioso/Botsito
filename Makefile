# Tareas del proyecto. `make check` es lo que corre el CI y lo que se exige antes de cada informe.
UV ?= uv
export PYTHONHASHSEED = 0

.PHONY: sync hooks check lint types test contracts regress state config corpus knowledge

sync:
	$(UV) sync --locked --group dev
	$(MAKE) hooks

# Los hooks se COPIAN al directorio de hooks de git: asi protegen tambien al cambiar a una rama
# que no los tenga (con core.hooksPath relativo, git omite en silencio el hook si el fichero no
# existe en la rama). Script Python y no cp/chmod: no depende del shell que make encuentre.
hooks:
	$(UV) run python scripts/instalar_hooks.py

lint:
	$(UV) run ruff check src tests
	$(UV) run ruff format --check src tests

types:
	$(UV) run mypy

contracts:
	$(UV) run lint-imports

test:
	$(UV) run pytest

state:
	$(UV) run botsito state check

config:
	$(UV) run botsito config validate

knowledge:
	$(UV) run botsito knowledge validate

# Solo donde exista el corpus (no en CI): compara el manifiesto con el disco.
corpus:
	$(UV) run botsito corpus check --hashes

check: lint types contracts test state config knowledge

# Regresion completa: en F01 equivale a check; desde F14 anade la biblioteca de casos.
regress: check
