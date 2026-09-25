# Tareas del proyecto. `make check` es lo que corre el CI y lo que se exige antes de cada informe.
UV ?= uv
export PYTHONHASHSEED = 0

.PHONY: sync hooks check lint types test contracts regress state config corpus knowledge desellar sellar

# El orden de `check` importa: `desellar` primero y `sellar` el ultimo, y `make` para en el primer
# objetivo que falla, asi que el sello solo se escribe con todo en verde. Sin paralelismo: con
# `-j`, `sellar` podria escribir el sello antes de que acabaran los tests.
.NOTPARALLEL:

sync:
	$(UV) sync --locked --group dev
	$(MAKE) hooks

# Los hooks se COPIAN al directorio de hooks de git: asi protegen tambien al cambiar a una rama
# que no los tenga (con core.hooksPath relativo, git omite en silencio el hook si el fichero no
# existe en la rama). Script Python y no cp/chmod: no depende del shell que make encuentre.
hooks:
	$(UV) run python scripts/instalar_hooks.py

# `scripts/` entra desde F12. Entonces el motivo era la hoja de la sesion, que vivia ahi y era el
# unico codigo que se ejecuta delante del trader sin red; en F13 se mudo a
# `src/botsito/cases/hoja_docx.py` y ahora tiene `mypy --strict` y los contratos encima. El lint
# se queda: `instalar_hooks.py` y `mover_sesion.py` siguen aqui y tocan el repositorio.
lint:
	$(UV) run ruff check src tests scripts
	$(UV) run ruff format --check src tests scripts

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

# El sello (scripts/sello_make_check.py, rama trabajo/blindaje): el hash del arbol ESTADIADO que
# acaba de pasar en verde. El hook de pre-commit rechaza un arbol sin sello. No sella si hay
# cambios sin estadiar o ficheros sin seguir: lo avisa, y el commit se rechazara.
desellar:
	$(UV) run python scripts/sello_make_check.py borrar

sellar:
	$(UV) run python scripts/sello_make_check.py sellar

check: desellar lint types contracts test state config knowledge sellar

# Regresion completa: en F01 equivale a check; desde F14 anade la biblioteca de casos.
regress: check
