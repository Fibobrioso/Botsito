# Tareas del proyecto. `make check` es lo que corre el CI y lo que se exige antes de cada informe.
UV ?= uv
export PYTHONHASHSEED = 0

.PHONY: sync hooks check lint types test contracts regress state config corpus knowledge contrato desellar sellar

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

# El pico de memoria de make check (scripts/pico_memoria.py, rama trabajo/memoria-suite): cada paso
# corre dentro de `medir`, que apunta su pico en un acumulador del directorio de git, y `check`
# acaba con UNA linea `PICO DE MEMORIA` en make-check.log. Lo lleva el sistema operativo: no
# muestrea y no cuesta nada. Dentro de `uv run` los ejecutables del entorno estan en el PATH.
PICO = $(UV) run python scripts/pico_memoria.py
MEDIR = $(PICO) medir

# `scripts/` entra desde F12. Entonces el motivo era la hoja de la sesion, que vivia ahi y era el
# unico codigo que se ejecuta delante del trader sin red; en F13 se mudo a
# `src/botsito/cases/hoja_docx.py` y ahora tiene `mypy --strict` y los contratos encima. El lint
# se queda: `instalar_hooks.py` y `mover_sesion.py` siguen aqui y tocan el repositorio.
# `.claude/hooks` desde `trabajo/guardias-claude`: la guardia de Claude Code es codigo que decide
# que se puede leer, y lleva el mismo lint y `mypy --strict` que el resto.
lint:
	$(MEDIR) lint -- ruff check src tests scripts .claude/hooks
	$(MEDIR) lint -- ruff format --check src tests scripts .claude/hooks

types:
	$(MEDIR) types -- mypy
	$(MEDIR) types -- mypy --strict .claude/hooks/guardia.py .claude/hooks/solo_lectura.py scripts/contrato_rama.py

contracts:
	$(MEDIR) contracts -- lint-imports

test:
	$(MEDIR) test -- pytest

state:
	$(MEDIR) state -- botsito state check

config:
	$(MEDIR) config -- botsito config validate

knowledge:
	$(MEDIR) knowledge -- botsito knowledge validate

# El contrato de la rama (scripts/contrato_rama.py, docs/runbooks/CONTRATO-DE-RAMA.md): si hay un
# `contrato.yaml`, lo que la rama cambia contra el merge-base con main tiene que caber en el. Va
# el primero tras `desellar`: es rapido y dice pronto si la rama se ha salido de su encargo.
contrato:
	$(MEDIR) contrato -- python scripts/contrato_rama.py

# Solo donde exista el corpus (no en CI): compara el manifiesto con el disco.
corpus:
	$(UV) run botsito corpus check --hashes

# El sello (scripts/sello_make_check.py, rama trabajo/blindaje): el hash del arbol ESTADIADO que
# acaba de pasar en verde. El hook de pre-commit rechaza un arbol sin sello. No sella si hay
# cambios sin estadiar o ficheros sin seguir: lo avisa, y el commit se rechazara.
desellar:
	$(PICO) empezar
	$(MEDIR) desellar -- python scripts/sello_make_check.py borrar

sellar:
	$(MEDIR) sellar -- python scripts/sello_make_check.py sellar

check: desellar contrato lint types contracts test state config knowledge sellar
	@$(PICO) informe

# Regresion completa: en F01 equivale a check; desde F14 anade la biblioteca de casos.
regress: check
