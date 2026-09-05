"""Los manifiestos de datos son inmutables en el historial de git (F15, ADR-0005, H.2)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.comun.historial import (
    hay_git,
    modificaciones_en_historial,
    modificaciones_preparadas,
)
from botsito.data.dataset import DIRECTORIO_MANIFIESTOS

MAN = f"{DIRECTORIO_MANIFIESTOS}/prueba-deadbeef.yaml"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / MAN).parent.mkdir(parents=True)
    (tmp_path / MAN).write_text("dataset_id: x\n", encoding="utf-8")
    (tmp_path / DIRECTORIO_MANIFIESTOS / "README.md").write_text("doc\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "add")
    return tmp_path


@pytest.mark.contract
def test_manifiesto_modificar_y_borrar_se_detectan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS) == []
    (repo / MAN).write_text("dataset_id: y\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo, DIRECTORIO_MANIFIESTOS)
    _git(repo, "commit", "-q", "-m", "edit")
    assert modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS) == [
        f"modificado desde {_primero(repo)}: {MAN}"
    ]
    _git(repo, "rm", "-q", MAN)
    _git(repo, "commit", "-q", "-m", "del")
    assert modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS) == [
        f"borrado o renombrado: {MAN}"
    ]


@pytest.mark.contract
def test_readme_no_esta_protegido(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / DIRECTORIO_MANIFIESTOS / "README.md").write_text("otro\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo, DIRECTORIO_MANIFIESTOS) == []
    _git(repo, "commit", "-q", "-m", "doc")
    assert modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS) == []


@pytest.mark.contract
def test_repositorio_real(repo: Path) -> None:
    v = modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS)
    if v is None:
        assert not hay_git(repo), "hay git pero la guardia no se pudo evaluar"
        pytest.skip("sin git")
    assert v == []


def _primero(repo: Path) -> str:
    out = subprocess.run(
        ["git", "log", "--format=%H", "--diff-filter=A", "--", MAN],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return out[-1][:7]
