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
        # D2 del consultor (2026-10-06, trabajo/respaldo-a11): la afirmacion de cada item nuevo
        "La afirmacion de cada item de evidencia nuevo",
        # E5 de trabajo/entorno-code: la PARADA, sus respuestas tal cual y la tabla del encargo
        "Lo que necesito que decidas",
        "El encargo, punto por punto",
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


# E7 (trabajo/entorno-code; respuesta del consultor del 2026-10-11, punto 2): las formas de
# escribir de `botsito` que la lista no veia, medidas en `src/botsito/cli.py` (ENTORNO-CODE.md
# §0.a), y `--incluir-holdout`, que abre el holdout. Cada una, con su caso: si alguien la quita de
# `solo_lectura.py`, su caso falla.
@pytest.mark.parametrize(
    "comando",
    [
        "uv run botsito motor arnes --salida informe.txt",
        "uv run botsito motor arnes --meses 2025-01",  # sin --salida tambien: arnes escribe
        "uv run botsito motor visor --todos",  # por defecto en data/visor
        "uv run botsito motor visor --caso caso-x --salida otra",
        "uv run botsito kit hoja",  # un .docx en la raiz del repo
        "uv run botsito kit hoja --salida h.docx",
        "uv run botsito casos visto --mes 2025-01",  # construye y ancla
        "uv run botsito data download --dataset x",
        "uv run botsito data download-ticks --dataset x",
        "uv run botsito data aggregate --dataset d --periodo 240 --anclaje x --salida a.csv",
        "uv run botsito evidence contradictions",
        "uv run botsito evidence reject --propuesta p --item 1 --motivo m --decidido-por a",
        "uv run botsito evidence propose --salida p.yaml",
        "uv run botsito kit kappa --sesion-a a --sesion-b b --incluir-holdout --pregunta q",
        "uv run botsito motor arnes --salida x --check",  # --check no lo salva
    ],
)
def test_el_bash_de_los_agentes_que_leen_no_escribe_por_botsito(
    s: ModuleType, comando: str
) -> None:
    assert s.motivo(comando) is not None, comando


@pytest.mark.parametrize(
    "comando",
    [
        "uv run botsito data aggregate --dataset d --periodo 240 --anclaje x",  # a la pantalla
        "uv run botsito kit kappa --sesion-a a --sesion-b b",
        "uv run botsito kit check --sesion s",
        "uv run botsito casos check",
        "uv run botsito evidence list --tema t",
    ],
)
def test_lo_que_botsito_solo_lee_sigue_pasando(s: ModuleType, comando: str) -> None:
    assert s.motivo(comando) is None, comando


def test_el_auditor_de_encargos_tambien_solo_lee() -> None:
    texto = (RAIZ / ".claude" / "agents" / "auditor-encargo.md").read_text(encoding="utf-8")
    cabecera, _, cuerpo = texto[4:].partition("\n---\n")
    doc = yaml.safe_load(cabecera)
    assert doc["name"] == "auditor-encargo" and cuerpo.strip()
    assert {h.strip() for h in doc["tools"].split(",")} == HERRAMIENTAS_DE_LECTURA
    (entrada,) = doc["hooks"]["PreToolUse"]
    assert entrada["matcher"] == "Bash"
    orden = entrada["hooks"][0]["command"]
    assert "solo_lectura.py" in orden and "PYTHONUTF8=1" in orden


def test_incluir_holdout_dice_que_abre_el_holdout(s: ModuleType) -> None:
    motivo = s.motivo("uv run botsito kit kappa --sesion-a a --sesion-b b --incluir-holdout")
    assert motivo is not None and "abre el holdout" in motivo
