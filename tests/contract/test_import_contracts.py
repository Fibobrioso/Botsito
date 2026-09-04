"""Contratos de importacion verificados por AST, independientes de import-linter.

import-linter corre en `make check`; este test es la segunda capa y se aplica aunque los
paquetes esten vacios (contrato declarado desde F01, ver ADR-0001).
"""

import ast
import tomllib
from pathlib import Path

import pytest

FORBIDDEN_FOR_DOMAIN = {
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
