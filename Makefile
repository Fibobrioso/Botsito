# Tareas del proyecto. `make check` es lo que corre el CI y lo que se exige antes de cada informe.
UV ?= uv

.PHONY: sync check lint types test contracts regress state

sync:
	$(UV) sync --group dev

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

check: lint types contracts test state

# Regresion completa: en F01 equivale a check; desde F14 anade la biblioteca de casos.
regress: check
