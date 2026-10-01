"""El subagente revisor (`.claude/agents/revisor.md`, rama `trabajo/guardias-claude`): existe, su
frontmatter es valido, no tiene herramientas de escritura y su Bash no escribe."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[2]
REVISOR = RAIZ / ".claude" / "agents" / "revisor.md"
SOLO_LECTURA = RAIZ / ".claude" / "hooks" / "solo_lectura.py"
HERRAMIENTAS_DE_LECTURA = {"Read", "Grep", "Glob", "Bash"}
HERRAMIENTAS_QUE_ESCRIBEN = {"Write", "Edit", "MultiEdit", "NotebookEdit", "PowerShell"}


@pytest.fixture(scope="module")
def s() -> ModuleType:
    nombre = "solo_lectura"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SOLO_LECTURA)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def frontmatter() -> dict[str, Any]:
    texto = REVISOR.read_text(encoding="utf-8")
    assert texto.startswith("---\n")
    cabecera, _, cuerpo = texto[4:].partition("\n---\n")
    assert cuerpo.strip(), "el revisor no tiene instrucciones"
    doc = yaml.safe_load(cabecera)
    assert isinstance(doc, dict)
    return doc


def test_el_revisor_existe_y_su_frontmatter_es_valido() -> None:
    doc = frontmatter()
    assert doc["name"] == "revisor"
    assert isinstance(doc["description"], str) and len(doc["description"]) > 40
    assert doc.get("model") in {"sonnet", "opus", "haiku", "fable", "inherit"}
    assert set(doc) <= {"name", "description", "tools", "model", "hooks", "color"}


def test_el_revisor_no_tiene_herramientas_de_escritura() -> None:
    herramientas = {h.strip() for h in frontmatter()["tools"].split(",")}
    assert herramientas == HERRAMIENTAS_DE_LECTURA
    assert not herramientas & HERRAMIENTAS_QUE_ESCRIBEN


def test_su_bash_pasa_por_el_hook_de_solo_lectura() -> None:
    entradas = frontmatter()["hooks"]["PreToolUse"]
    assert [e["matcher"] for e in entradas] == ["Bash"]
    orden = entradas[0]["hooks"][0]["command"]
    assert "solo_lectura.py" in orden and "PYTHONUTF8=1" in orden
    assert SOLO_LECTURA.is_file()


def test_las_instrucciones_tienen_los_dos_ejes_y_las_tres_gravedades() -> None:
    texto = REVISOR.read_text(encoding="utf-8")
    for fragmento in (
        "Eje (a)",
        "Eje (b)",
        "**bloquea**",
        "**importa**",
        "**menor**",
        "docs/encargos/",
        "no arreglas nada",
        "CORRECT frente a RESOLVE",
        "Fuente:",
        "HOLDOUT-EXPOSICIONES",
        "contrato_rama.py",
        "recuadro de correccion",
    ):
        assert fragmento in texto, fragmento


@pytest.mark.parametrize(
    "comando",
    [
        "touch x",
        "echo hola > informe.md",
        "git commit -m x",
        "git checkout main",
        "git add -A",
        "git stash",
        "git branch nueva",
        "make check > make-check.log 2>&1",
        "rm make-check.log",
        "sed -i 's/a/b/' docs/a.md",
        "uv run botsito spec docs --escribir",
        "uv run botsito feedback new --sesion x",
        "uv sync",
        "python -c \"open('x', 'w').write('y')\"",
        "cat docs/a.md | tee copia.md",
    ],
)
def test_el_bash_del_revisor_no_escribe(s: ModuleType, comando: str) -> None:
    assert s.motivo(comando) is not None, comando


@pytest.mark.parametrize(
    "comando",
    [
        "git log --format='%h %s' main..HEAD",
        "git diff --stat main...HEAD",
        "git diff --name-status main...HEAD -- knowledge/evidence",
        "git status --short",
        "git branch --show-current",
        "git merge-base main HEAD",
        "git show HEAD:CLAUDE.md",
        "cat docs/validation/GUARDIAS-CLAUDE.md",
        "grep -n Fuente: docs/validation/GUARDIAS-CLAUDE.md",
        "uv run python scripts/contrato_rama.py",
        "uv run pytest tests/unit/test_revisor.py -q",
        "uv run botsito feedback apply --sesion x --check",
        "uv run botsito state check 2>&1",
        "ls docs/encargos",
    ],
)
def test_el_bash_del_revisor_lee(s: ModuleType, comando: str) -> None:
    assert s.motivo(comando) is None, comando


def test_el_proceso_de_solo_lectura_sale_con_2_o_0() -> None:
    def ejecutar(comando: str) -> int:
        evento = {"tool_name": "Bash", "tool_input": {"command": comando}}
        return subprocess.run(
            [sys.executable, str(SOLO_LECTURA)],
            input=json.dumps(evento),
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
            check=False,
        ).returncode

    assert ejecutar("touch x") == 2
    assert ejecutar("git status") == 0


def test_claude_md_manda_pasar_el_revisor_y_la_metrica_existe() -> None:
    claude = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
    assert (
        "Antes de declarar una rama lista para revisión: guarda el encargo en docs/encargos/, "
        "pasa el revisor y pega su informe al final del informe de la rama"
    ) in claude
    metrica = (RAIZ / "docs" / "runbooks" / "ERRORES-RECURRENTES.md").read_text(encoding="utf-8")
    assert "| Rama | Hallazgos del revisor | Hallazgos del consultor despues |" in metrica
