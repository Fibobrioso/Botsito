# Tareas del proyecto. `make check` es lo que corre el CI y lo que se exige antes de cada informe.
UV ?= uv
export PYTHONHASHSEED = 0

.PHONY: sync hooks check lint types test contracts regress state config

sync:
	$(UV) sync --locked --group dev
	$(MAKE) hooks

# Los hooks se COPIAN a .git/hooks: asi protegen tambien al cambiar a una rama que no los tenga
# (con core.hooksPath relativo, git omite en silencio el hook si el fichero no existe en la rama).
hooks:
	git config --unset core.hooksPath || true
	cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

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

check: lint types contracts test state config

# Regresion completa: en F01 equivale a check; desde F14 anade la biblioteca de casos.
regress: check
