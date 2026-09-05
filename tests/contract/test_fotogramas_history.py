"""Los manifiestos de fotogramas son inmutables en el historial de git (F05, ADR-0008)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.comun.historial import (
    DIRECTORIO_FOTOGRAMAS,
    hay_git,
    modificaciones_en_historial,
    modificaciones_preparadas,
)

MAN = f"{DIRECTORIO_FOTOGRAMAS}/fr-v1-deadbeef.yaml"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / MAN).parent.mkdir(parents=True)
    (tmp_path / MAN).write_text("fotogramas_id: x\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "add")
    return tmp_path


@pytest.mark.contract
def test_modificar_y_borrar_se_detectan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert modificaciones_en_historial(repo, DIRECTORIO_FOTOGRAMAS) == []
    (repo / MAN).write_text("fotogramas_id: y\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo, DIRECTORIO_FOTOGRAMAS)
    _git(repo, "commit", "-q", "-m", "edit")
    assert modificaciones_en_historial(repo, DIRECTORIO_FOTOGRAMAS)
    _git(repo, "rm", "-q", MAN)
    _git(repo, "commit", "-q", "-m", "del")
    assert modificaciones_en_historial(repo, DIRECTORIO_FOTOGRAMAS) == [
        f"borrado o renombrado: {MAN}"
    ]


@pytest.mark.contract
def test_repositorio_real(repo: Path) -> None:
    v = modificaciones_en_historial(repo, DIRECTORIO_FOTOGRAMAS)
    if v is None:
        assert not hay_git(repo)
        pytest.skip("sin git")
    assert v == []


@pytest.mark.contract
def test_hook_protege_fotogramas(repo: Path) -> None:
    hook = (repo / "scripts" / "git-hooks" / "pre-commit").read_text(encoding="utf-8")
    assert DIRECTORIO_FOTOGRAMAS in hook
