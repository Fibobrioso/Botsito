"""Ningun parametro de negocio vive fuera del registro (F02, ADR-0002).

Se inspecciona el AST de src/botsito/ (salvo config/registro.py, que ES el registro): constantes
numericas, constantes de texto que son un numero (`Decimal("0.75")`, `Fraccion("0,75")`),
expresiones constantes (`3 / 4`, `"07" + ":00"`) y textos, fuera de docstrings. Un valor de la
lista solo puede aparecer leyendose del registro.
"""

from __future__ import annotations

import ast
import re
from decimal import Decimal, InvalidOperation
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


def _como_decimal(valor: object) -> Decimal | None:
    if isinstance(valor, bool):
        return None
    if isinstance(valor, int | float):
        return Decimal(repr(valor)) if isinstance(valor, float) else Decimal(valor)
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not re.fullmatch(r"[+-]?\d+(\.\d+)?", texto):
            return None
        try:
            return Decimal(texto)
        except InvalidOperation:
            return None
    return None


_NODOS_CONSTANTES = (
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.JoinedStr,
    ast.FormattedValue,
    ast.operator,
    ast.unaryop,
)


def _valor_constante(node: ast.AST) -> object | None:
    """Valor de una constante o de una expresion formada SOLO por constantes.

    `3 / 4`, `"07" + ":00"`, `f"{7:02d}:00"`, `-(-0.25)`: se evaluan porque no contienen nombres
    ni llamadas (todo nodo descendiente es constante u operador), asi que el eval es inocuo.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if not isinstance(node, ast.BinOp | ast.UnaryOp | ast.JoinedStr):
        return None
    if not all(isinstance(n, _NODOS_CONSTANTES) for n in ast.walk(node)):
        return None
    try:
        valor: object = eval(  # noqa: S307  # solo constantes y operadores, comprobado arriba
            compile(ast.Expression(body=node), "<const>", "eval"), {"__builtins__": {}}, {}
        )
    except (ZeroDivisionError, ValueError, TypeError, OverflowError):
        return None
    return valor


def _ofensas(py: Path) -> list[str]:
    tree = ast.parse(py.read_text(encoding="utf-8"))
    docstrings = _docstring_nodes(tree)
    out: list[str] = []
    for node in ast.walk(tree):
        if id(node) in docstrings:
            continue
        v = _valor_constante(node)
        if v is None or isinstance(v, bool):
            continue
        linea = getattr(node, "lineno", 0)
        d = _como_decimal(v)
        if d is not None and d in NUMEROS_PROHIBIDOS:
            out.append(f"{py.name}:{linea} literal {v!r} ({NUMEROS_PROHIBIDOS[d]})")
        if isinstance(v, str):
            for patron, motivo in TEXTOS_PROHIBIDOS.items():
                if patron.search(v):
                    out.append(f"{py.name}:{linea} texto {v!r} ({motivo})")
    return out


@pytest.mark.contract
def test_no_business_literals_outside_registry(repo: Path) -> None:
    ofensas: list[str] = []
    for py in (repo / "src" / "botsito").rglob("*.py"):
        if py.parts[-2:] == ("config", "registro.py"):
            continue  # el registro es la puerta; el resto de config/ SI se inspecciona
        ofensas.extend(_ofensas(py))
    assert ofensas == [], "valores de negocio fuera del registro:\n" + "\n".join(ofensas)


@pytest.mark.contract
def test_el_detector_detecta(tmp_path: Path) -> None:
    py = tmp_path / "m.py"
    py.write_text(
        '"""0.75 en docstring no cuenta."""\nSTOP = 0.75\nVENTANA = "07:00"\n', encoding="utf-8"
    )
    assert len(_ofensas(py)) == 2


@pytest.mark.contract
@pytest.mark.parametrize(
    "linea",
    [
        'Decimal("0.75")',
        'Fraccion("0,75")',
        'x = "0.5"',
        "x = 3 / 4",
        "x = 2 * 1000",
        'x = "07" + ":00"',
        'x = f"{7:02d}:00"',
        "x = -(-0.25)",
    ],
)
def test_el_detector_no_se_elude(tmp_path: Path, linea: str) -> None:
    py = tmp_path / "m.py"
    py.write_text(linea + "\n", encoding="utf-8")
    assert _ofensas(py), linea


@pytest.mark.contract
def test_el_detector_no_da_falsos_positivos(tmp_path: Path) -> None:
    py = tmp_path / "m.py"
    py.write_text('x = 1\ny = "a.b"\nz = 8 * 1024\nw = "0."\n', encoding="utf-8")
    assert _ofensas(py) == []
