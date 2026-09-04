"""Ningun parametro de negocio vive fuera del registro (F02, ADR-0002).

Se inspecciona el AST de src/botsito/ (salvo config/, que ES el registro): constantes numericas y
de texto fuera de docstrings. Un valor de la lista solo puede aparecer leyendose del registro.
"""

from __future__ import annotations

import ast
import re
from decimal import Decimal
from pathlib import Path

import pytest

NUMEROS_PROHIBIDOS: dict[Decimal, str] = {
    Decimal("0.75"): "stop en la caja (RN-021)",
    Decimal("0.5"): "stop reducido / riesgo en fondeo",
    Decimal("0.25"): "nivel de la caja",
    Decimal("0.40"): "riesgo por operacion",
    Decimal("0.45"): "riesgo por operacion",
    Decimal("2000"): "limite de mensajes de la prop firm",
}
TEXTOS_PROHIBIDOS: dict[re.Pattern[str], str] = {
    re.compile(r"\b(07|11|15):00\b"): "ventana operativa (RN-002)",
    re.compile(r"\b1:3\b"): "objetivo riesgo/beneficio (RN-024)",
    re.compile(r"\bEURUSD\b"): "instrumento",
}


def _docstring_nodes(tree: ast.AST) -> set[int]:
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                ids.add(id(body[0].value))
    return ids


def _ofensas(py: Path) -> list[str]:
    tree = ast.parse(py.read_text(encoding="utf-8"))
    docstrings = _docstring_nodes(tree)
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or id(node) in docstrings:
            continue
        v = node.value
        if isinstance(v, bool):
            continue
        if isinstance(v, int | float):
            d = Decimal(repr(v)) if isinstance(v, float) else Decimal(v)
            if d in NUMEROS_PROHIBIDOS:
                out.append(f"{py.name}:{node.lineno} literal {v} ({NUMEROS_PROHIBIDOS[d]})")
        elif isinstance(v, str):
            for patron, motivo in TEXTOS_PROHIBIDOS.items():
                if patron.search(v):
                    out.append(f"{py.name}:{node.lineno} texto {v!r} ({motivo})")
    return out


@pytest.mark.contract
def test_no_business_literals_outside_registry(repo: Path) -> None:
    ofensas: list[str] = []
    for py in (repo / "src" / "botsito").rglob("*.py"):
        if "config" in py.parts:
            continue
        ofensas.extend(_ofensas(py))
    assert ofensas == [], "valores de negocio fuera del registro:\n" + "\n".join(ofensas)


@pytest.mark.contract
def test_el_detector_detecta(tmp_path: Path) -> None:
    py = tmp_path / "m.py"
    py.write_text(
        '"""0.75 en docstring no cuenta."""\nSTOP = 0.75\nVENTANA = "07:00"\n', encoding="utf-8"
    )
    assert len(_ofensas(py)) == 2
