"""Feedback solo-anadir en el historial de git y trazabilidad de los cambios de spec/casos (F09)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.evidence.historial import (
    DIRECTORIO_FEEDBACK,
    commits_sin_fuente,
    fuentes_de_mensaje,
    modificaciones_en_historial,
    modificaciones_preparadas,
)

FB = "knowledge/feedback/2026-09-20-sesion-01/fb-2026-09-20-sesion-01-aaaaaaaa.yaml"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / FB).parent.mkdir(parents=True)
    (tmp_path / FB).write_text("id: x\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "add")
    return tmp_path


@pytest.mark.contract
def test_feedback_modificar_y_borrar_se_detectan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK) == []
    (repo / FB).write_text("id: y\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo, DIRECTORIO_FEEDBACK)
    _git(repo, "commit", "-q", "-m", "edit")
    assert modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK) == [
        f"modificado desde {_primero(repo, FB)}: {FB}"
    ]
    _git(repo, "rm", "-q", FB)
    _git(repo, "commit", "-q", "-m", "del")
    assert modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK) == [f"borrado o renombrado: {FB}"]


@pytest.mark.contract
def test_trailer_fuente(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    spec.parent.mkdir(parents=True)
    spec.write_text("reglas: []\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "spec sin fuente")
    assert commits_sin_fuente(repo, None) == [
        f"{_head(repo)}: toca spec/cases sin trailer 'Fuente:'"
    ]
    spec.write_text("reglas: [1]\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "spec con fuente\n\nFuente: ev-v4-001533-1a2b3c4d, ADR-0002")
    problemas = commits_sin_fuente(repo, None, ids_validos={"ev-v4-001533-1a2b3c4d"})
    assert len(problemas or []) == 1 and "sin trailer" in (problemas or [""])[0]
    spec.write_text("reglas: [2]\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "mala\n\nFuente: ev-v4-000000-00000000 basura")
    ultimos = [
        p for p in commits_sin_fuente(repo, None, ids_validos=set()) or [] if _head(repo) in p
    ]
    assert any("inexistente" in p for p in ultimos) and any(
        "formato invalido" in p for p in ultimos
    )
    assert commits_sin_fuente(repo, "no-existe") is None


def test_fuentes_de_mensaje() -> None:
    assert fuentes_de_mensaje("x\n\nFuente: a, b c\nFuente: d") == ["a", "b", "c", "d"]
    assert fuentes_de_mensaje("sin trailer") == []


@pytest.mark.contract
def test_repositorio_real(repo: Path) -> None:
    v = modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK)
    if v is None:
        pytest.skip("sin git")
    assert v == []
    sin_fuente = commits_sin_fuente(repo, "stable/F06")
    assert sin_fuente in (None, []), "\n".join(sin_fuente or [])


def _primero(repo: Path, ruta: str) -> str:
    out = subprocess.run(
        ["git", "log", "--format=%H", "--diff-filter=A", "--", ruta],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return out[-1][:7]


def _head(repo: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short=7", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
