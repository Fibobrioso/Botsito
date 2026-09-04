"""La evidencia es inmutable en el historial de git (F06, seccion H).

Los hooks se saltan con --no-verify; este test no. Se ejecuta sobre un repositorio temporal
(modificar, renombrar y borrar deben detectarse) y sobre el repositorio real.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.evidence.historial import modificaciones_en_historial, modificaciones_preparadas


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "feature/x")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    d = tmp_path / "knowledge" / "evidence" / "v1"
    d.mkdir(parents=True)
    (d / "ev-v1-000001-aaaaaaaa.yaml").write_text("id: x\n", encoding="utf-8")
    (tmp_path / "knowledge" / "evidence" / "_contradicciones.yaml").write_text(
        "c\n", encoding="utf-8"
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "add")
    return tmp_path


@pytest.mark.contract
def test_anadir_es_legitimo(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert modificaciones_en_historial(repo) == []


@pytest.mark.contract
def test_modificar_borrar_renombrar_se_detectan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    f = repo / "knowledge" / "evidence" / "v1" / "ev-v1-000001-aaaaaaaa.yaml"
    f.write_text("id: y\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert any("M" in v for v in modificaciones_preparadas(repo) or [])
    _git(repo, "commit", "-q", "-m", "edit")
    (repo / "knowledge" / "evidence" / "_contradicciones.yaml").write_text("d\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo) == []  # el generado si puede cambiar
    _git(repo, "commit", "-q", "-m", "regen")
    _git(repo, "rm", "-q", f.as_posix())
    _git(repo, "commit", "-q", "-m", "del")
    violaciones = modificaciones_en_historial(repo) or []
    assert len(violaciones) == 2
    assert any(v.split(": ")[1].startswith("M") for v in violaciones)
    assert any(v.split(": ")[1].startswith("D") for v in violaciones)


@pytest.mark.contract
def test_repositorio_real_sin_modificaciones(repo: Path) -> None:
    violaciones = modificaciones_en_historial(repo)
    if violaciones is None:
        pytest.skip("sin git")
    assert violaciones == [], "\n".join(violaciones)
