"""Contratos de importacion verificados por AST, independientes de import-linter.

import-linter corre en `make check`; este test es la segunda capa y se aplica aunque los
paquetes esten vacios (contrato declarado desde F01, ver ADR-0001).
"""

import ast
import tomllib
from pathlib import Path

import pytest

FORBIDDEN_FOR_DOMAIN = {
    "botsito.comun",
    "botsito.evidence",
    "botsito.feedback",
    "botsito.spec",
    "botsito.cases",
    "zoneinfo",
    "subprocess",
    "yaml",
    "hashlib",
    "botsito.engine",
    "botsito.data",
    "botsito.mql5bridge",
    "botsito.corpus",
    "botsito.viewer",
    "botsito.validation",
    "botsito.cli",
    "botsito.config",
    "MetaTrader5",
    "pandas",
    "polars",
    "numpy",
    "requests",
    "asyncio",
    "threading",
    "datetime",
    "time",
    "random",
    "os",
    "pathlib",
    "io",
}
FORBIDDEN_FOR_SPEC = {
    "botsito.engine",
    "botsito.data",
    "botsito.mql5bridge",
    "MetaTrader5",
    "pandas",
    "polars",
}


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _violations(pkg_dir: Path, forbidden: set[str]) -> list[str]:
    out: list[str] = []
    for py in pkg_dir.rglob("*.py"):
        for name in _imports(py):
            if any(name == f or name.startswith(f + ".") for f in forbidden):
                out.append(f"{py.name} importa {name}")
    return out


@pytest.mark.contract
def test_domain_is_pure(repo: Path) -> None:
    assert _violations(repo / "src" / "botsito" / "domain", FORBIDDEN_FOR_DOMAIN) == []


@pytest.mark.contract
def test_spec_does_not_depend_on_engine_or_data(repo: Path) -> None:
    assert _violations(repo / "src" / "botsito" / "spec", FORBIDDEN_FOR_SPEC) == []


@pytest.mark.contract
def test_domain_and_spec_never_mention_holdout(repo: Path) -> None:
    for pkg in ("domain", "spec"):
        for py in (repo / "src" / "botsito" / pkg).rglob("*.py"):
            assert "holdout" not in py.read_text(encoding="utf-8"), f"{py} menciona holdout"


@pytest.mark.contract
def test_importlinter_contracts_declared(repo: Path) -> None:
    cfg = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    contracts = cfg["tool"]["importlinter"]["contracts"]
    names = {c["name"] for c in contracts}
    assert any("domain es puro" in n for n in names)
    assert any(c["type"] == "layers" for c in contracts)


@pytest.mark.contract
def test_domain_sin_float_ni_decimal_fuera_de_valores(repo: Path) -> None:
    """H.2 (F18): en `domain/` los precios son enteros en puntos; `float` y `Decimal` solo en
    `valores.py`, donde viven Fraccion y Porcentaje."""
    ofensas: list[str] = []
    for py in sorted((repo / "src" / "botsito" / "domain").rglob("*.py")):
        if py.name == "valores.py":
            continue
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in {"float", "Decimal"}:
                ofensas.append(f"{py.name}:{node.lineno} {node.id}")
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                ofensas.append(f"{py.name}:{node.lineno} literal float {node.value}")
            if isinstance(node, ast.ImportFrom) and node.module == "decimal":
                ofensas.append(f"{py.name}:{node.lineno} import decimal")
    assert ofensas == [], ofensas


@pytest.mark.contract
def test_faster_whisper_solo_en_motor_whisper(repo: Path) -> None:
    """El grupo `asr` es opcional: solo `corpus/motor_whisper.py` puede cargar faster-whisper o
    ctranslate2, y lo hace con importlib para que el resto del paquete no dependa de ellos."""
    prohibidos = {"faster_whisper", "ctranslate2"}
    ofensas: list[str] = []
    for py in sorted((repo / "src" / "botsito").rglob("*.py")):
        if py.name == "motor_whisper.py":
            continue
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(
                a.name.split(".")[0] in prohibidos for a in node.names
            ):
                ofensas.append(f"{py.name}:{node.lineno}")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in prohibidos:
                ofensas.append(f"{py.name}:{node.lineno}")
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "import_module"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and str(node.args[0].value).split(".")[0] in prohibidos
            ):
                ofensas.append(f"{py.name}:{node.lineno} (importlib)")
    assert ofensas == [], ofensas
