"""Integridad del indice de git: lo que el plan espera esta versionado, sin CRLF, sin ignorados
inesperados. Nacio de dos incidentes reales en F01 (gitignore sin anclar; CRLF por escritura en
Windows). Ver docs/plan/AUDITORIA_FASES_2026-09-04.html.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tests.unit.test_tree import DOC_DIRS, PACKAGES, README_EXEMPT, ROOT_FILES

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".txt",
    ".json",
    ".jsonl",
    ".csv",
    ".html",
    ".mq5",
    ".mqh",
    ".ini",
    ".cfg",
    ".sh",
    "",
}
IGNORED_ALLOWLIST = (
    ".venv/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".import_linter_cache/",
    ".hypothesis/",
    ".coverage",
)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        pytest.skip(f"git no disponible o no es un repositorio: {result.stderr.strip()}")
    return result.stdout


def _tracked(repo: Path) -> set[str]:
    return {line.strip() for line in _git(repo, "ls-files").splitlines() if line.strip()}


def _expected_files(repo: Path) -> list[str]:
    files = list(ROOT_FILES)
    files += [f"{d}/README.md" for d in DOC_DIRS if d not in README_EXEMPT]
    files += [f"src/botsito/{p}/__init__.py" for p in PACKAGES]
    files += [
        "src/botsito/__init__.py",
        "src/botsito/cli.py",
        ".gitattributes",
    ]
    return files


@pytest.mark.contract
def test_expected_files_are_tracked(repo: Path) -> None:
    tracked = _tracked(repo)
    missing = [f for f in _expected_files(repo) if f not in tracked]
    assert not missing, f"existen en disco pero no estan en git (¿gitignore?): {missing}"


@pytest.mark.contract
def test_no_crlf_in_tracked_text_files(repo: Path) -> None:
    offenders: list[str] = []
    for rel in _tracked(repo):
        path = repo / rel
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
            continue
        if b"\r\n" in path.read_bytes():
            offenders.append(rel)
    assert offenders == [], f"ficheros de texto con CRLF: {offenders}"


@pytest.mark.contract
def test_gitattributes_normalizes_text(repo: Path) -> None:
    text = (repo / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in text


@pytest.mark.contract
def test_no_unexpected_ignored_paths(repo: Path) -> None:
    out = _git(repo, "status", "--ignored", "--porcelain")
    ignored = [line[3:] for line in out.splitlines() if line.startswith("!! ")]
    unexpected = [p for p in ignored if not any(a in p for a in IGNORED_ALLOWLIST)]
    # corpus/ y data/ (salvo manifests) se ignoran a proposito: son datos pesados
    unexpected = [p for p in unexpected if not p.startswith(("corpus/", "data/"))]
    assert unexpected == [], f"rutas ignoradas no previstas: {unexpected}"


@pytest.mark.contract
def test_gitignore_patterns_are_anchored(repo: Path) -> None:
    """Un patron `corpus/` sin barra inicial ignora src/botsito/corpus. Debe ser `/corpus/`."""
    lines = [
        line.strip()
        for line in (repo / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    for pattern in ("corpus", "data"):
        matching = [line for line in lines if line.lstrip("!/").rstrip("/*") == pattern]
        assert matching, f"falta el patron para {pattern}/"
        assert all(line.startswith(("/", "!/")) for line in matching), (
            f"patron sin anclar para {pattern}: {matching}"
        )
